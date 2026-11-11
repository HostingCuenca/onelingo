import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { query } from '../lib/db.js';
import { requiereAdmin } from '../lib/auth.js';
import { AJUSTES_TUTOR_DEFECTO, AjustesTutor, ajustesTutor, guardarAjustesTutor, versionesTutor } from '../lib/ajustes_tutor.js';
import { estadoTurno, iaDisponible, responder, type Turno } from '../lib/ia.js';
import { medirRepeticion, notaVariedad } from '../lib/variedad.js';
import { actualizarFicha } from '../lib/ficha_alumno.js';
import { contextoSituacion } from '../lib/situaciones.js';

const TurnoEntrada = z.object({
  rol: z.enum(['tutor', 'alumno']), texto: z.string().max(2000),
  espera: z.object({ tipo: z.enum(['repetir', 'elegir', 'responder']), modelo: z.string().max(400) }).optional(),
});
const Prueba = z.object({
  ajustes: AjustesTutor,
  idiomaMeta: z.string().regex(/^[a-z]{2}$/), idiomaNativo: z.string().regex(/^[a-z]{2}$/).default('es'),
  nivel: z.number().int().min(0).max(10), tutorId: z.string().regex(/^[a-z_]{2,30}$/),
  historial: z.array(TurnoEntrada).max(40),
  // Opcional: responder como a ese alumno (con su ficha y su contexto).
  usuarioId: z.string().uuid().optional(),
});

type Fila = { id: number; fecha: string; usuario_id: string; nombre: string; email: string; idioma: string; nivel: number; tutor_id: string; situacion_id: number | null; mensaje_alumno: string; respuesta: any };
/** Pausa entre turnos que separa dos llamadas del mismo alumno con el mismo tutor. */
const PAUSA_MS = 20 * 60_000;
const AVISOS = new Set(['[silencio]', '[pista]']);

/** Turnos guardados (uno por petición) agrupados en llamadas, con sus indicadores de repetición. */
export function agruparLlamadas(filas: Fila[], evitar: string[]) {
  const llamadas: { clave: string; filas: Fila[] }[] = [], ultima = new Map<string, { fin: number; l: { clave: string; filas: Fila[] } }>();
  for (const f of [...filas].sort((a, b) => +new Date(a.fecha) - +new Date(b.fecha))) {
    const clave = `${f.usuario_id}|${f.tutor_id}|${f.idioma}`, t = +new Date(f.fecha), u = ultima.get(clave);
    if (u && t - u.fin < PAUSA_MS) { u.l.filas.push(f); u.fin = t; continue; }
    const l = { clave, filas: [f] }; llamadas.push(l); ultima.set(clave, { fin: t, l });
  }
  return llamadas.reverse().map(({ filas: fs }) => {
    const historial: Turno[] = fs.flatMap((f) => [
      ...(f.mensaje_alumno ? [{ rol: 'alumno' as const, texto: AVISOS.has(f.mensaje_alumno) ? '' : f.mensaje_alumno }] : []),
      { rol: 'tutor' as const, texto: String(f.respuesta?.reply ?? ''), ...(f.respuesta?.espera ? { espera: f.respuesta.espera } : {}) },
    ]);
    const p = fs[0], { marcas, ...indicadores } = medirRepeticion(historial, evitar);
    return {
      inicio: p.fecha, fin: fs[fs.length - 1].fecha, alumno: p.nombre, email: p.email, usuarioId: p.usuario_id,
      idioma: p.idioma, nivel: p.nivel, tutorId: p.tutor_id, situacionId: p.situacion_id,
      indicadores,
      turnos: fs.map((f, i) => ({ id: f.id, marcas: marcas[i] ?? [], fecha: f.fecha, alumno: f.mensaje_alumno, tutor: f.respuesta?.reply ?? '', espera: f.respuesta?.espera ?? null,
        correcciones: (f.respuesta?.corrections ?? []).map((c: any) => ({ original: c.original, correcto: c.correcto })) })),
    };
  });
}

export default async function rutas(app: FastifyInstance) {
  app.get('/admin/tutor', { preHandler: requiereAdmin }, async () => ({
    actual: ajustesTutor(), defecto: AJUSTES_TUTOR_DEFECTO, versiones: await versionesTutor(), ia: iaDisponible(),
  }));

  app.put('/admin/tutor', { preHandler: requiereAdmin }, async (req) => {
    const { ajustes, nota } = z.object({ ajustes: AjustesTutor, nota: z.string().max(200).default('') }).parse(req.body);
    return { actual: await guardarAjustesTutor(ajustes, nota), versiones: await versionesTutor() };
  });

  // Un turno del tutor con los ajustes que se están editando, sin guardarlos ni registrar la conversación.
  app.post('/admin/tutor/probar', { preHandler: requiereAdmin }, async (req, reply) => {
    const d = Prueba.parse(req.body);
    if (!iaDisponible()) return reply.code(503).send({ error: 'La IA no está configurada en el servidor' });
    const historial = d.historial as Turno[];
    if (historial[historial.length - 1]?.rol !== 'alumno') return reply.code(400).send({ error: 'El último turno debe ser del alumno' });
    const t0 = Date.now();
    const contexto = d.usuarioId ? await contextoSituacion(d.usuarioId, { idiomaMeta: d.idiomaMeta, nivel: d.nivel, historial }) : undefined;
    const r = await responder({ idiomaMeta: d.idiomaMeta, idiomaNativo: d.idiomaNativo, nivel: d.nivel, tutorId: d.tutorId, historial, ajustes: d.ajustes, contexto });
    return {
      reply: r.respuesta.reply, espera: r.respuesta.espera ?? null, traduccion: r.respuesta.traduccion,
      correcciones: r.respuesta.corrections.map((c) => ({ original: c.original, correcto: c.correcto, explicacion: c.explicacion })),
      notas: [estadoTurno(historial, undefined, d.idiomaMeta), notaVariedad(historial, d.ajustes)].filter(Boolean), modelo: r.modelo, ms: Date.now() - t0,
    };
  });

  // Alumnos con ficha, para probar el tutor como si hablara con uno de ellos.
  app.get('/admin/fichas', { preHandler: requiereAdmin }, async () => query(
    `SELECT f.usuario_id, f.idioma, f.actualizado_en, u.nombre, u.email FROM ficha_alumno f JOIN usuarios u ON u.id = f.usuario_id ORDER BY f.actualizado_en DESC LIMIT 200`));
  // Lo que el tutor sabe de cada alumno, por idioma (se ve en el detalle del alumno).
  app.get('/admin/usuarios/:id/fichas', { preHandler: requiereAdmin }, async (req) => {
    const { id } = z.object({ id: z.string().uuid() }).parse(req.params);
    return query('SELECT idioma, datos, actualizado_en FROM ficha_alumno WHERE usuario_id = $1 ORDER BY actualizado_en DESC', [id]);
  });
  app.post('/admin/usuarios/:id/fichas/:idioma', { preHandler: requiereAdmin }, async (req, reply) => {
    const { id, idioma } = z.object({ id: z.string().uuid(), idioma: z.string().regex(/^[a-z]{2}$/) }).parse(req.params);
    const u = await query<{ idioma_nativo: string; nivel: number }>('SELECT u.idioma_nativo, coalesce(p.nivel_actual, u.nivel_inicial, 1) AS nivel FROM usuarios u LEFT JOIN progreso p ON p.usuario_id = u.id WHERE u.id = $1', [id]);
    if (!u[0]) return reply.code(404).send({ error: 'No existe' });
    const ficha = await actualizarFicha(id, idioma, u[0].idioma_nativo || 'es', Math.min(10, Math.max(1, Number(u[0].nivel) || 1)), 1);
    return ficha ? { ok: true } : reply.code(409).send({ error: 'No hay conversaciones nuevas en ese idioma, o ya se está actualizando' });
  });

  app.get('/admin/practicas', { preHandler: requiereAdmin }, async (req) => {
    const { dias } = z.object({ dias: z.coerce.number().int().min(1).max(60).default(7) }).parse(req.query);
    const filas = await query<Fila>(
      `SELECT c.id, c.fecha, c.usuario_id, u.nombre, u.email, c.idioma, c.nivel, c.tutor_id, c.situacion_id, c.mensaje_alumno, c.respuesta
       FROM conversaciones c JOIN usuarios u ON u.id = c.usuario_id
       WHERE c.fecha > now() - make_interval(days => $1) ORDER BY c.fecha DESC LIMIT 3000`, [dias]);
    return { dias, llamadas: agruparLlamadas(filas, ajustesTutor().frasesEvitar) };
  });
}
