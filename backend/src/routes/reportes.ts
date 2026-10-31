import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { query, uno } from '../lib/db.js';
import { requiereAdmin, requiereAlumno, type Sesion } from '../lib/auth.js';

/** Reportes por alumno y hora: frena el abuso sin estorbar a quien reporta de verdad. */
export const REPORTES_POR_HORA = 30;
export const ORIGENES_REPORTE = ['chat', 'llamada', 'situacion', 'ejercicio', 'otro'] as const;
export const MOTIVOS_REPORTE = ['ofensivo', 'incorrecto', 'inapropiado', 'otro'] as const;

const Reporte = z.object({
  origen: z.enum(ORIGENES_REPORTE),
  texto: z.string().trim().min(1).max(2000),
  motivo: z.enum(MOTIVOS_REPORTE),
  comentario: z.string().trim().max(500).default(''),
  contexto: z.object({
    idioma: z.string().max(10).optional(),
    tutorId: z.string().max(60).optional(),
    situacion: z.union([z.string().max(200), z.number().int()]).optional(),
  }).strip().default({}),
});

/**
 * Denunciar respuestas de la IA (política de contenido generado por IA de Google
 * Play): el alumno marca una respuesta del tutor (chat, videollamada…) y el
 * equipo la revisa en el panel (Panel → Reportes IA).
 */
export default async function rutas(app: FastifyInstance) {
  app.post('/reportes-ia', { preHandler: requiereAlumno }, async (req, reply) => {
    const s = req.user as Sesion;
    const d = Reporte.parse(req.body);
    const n = Number((await uno<{ n: number }>(`SELECT count(*)::int AS n FROM reportes_ia WHERE usuario_id = $1 AND creado_en > now() - interval '1 hour'`, [s.sub]))?.n ?? 0);
    if (n >= REPORTES_POR_HORA) return reply.code(429).header('retry-after', '3600').send({ error: 'demasiados_reportes' });
    const r = await uno<{ id: number }>(
      'INSERT INTO reportes_ia (usuario_id, origen, motivo, texto, comentario, contexto) VALUES ($1,$2,$3,$4,$5,$6) RETURNING id',
      [s.sub, d.origen, d.motivo, d.texto, d.comentario, JSON.stringify(d.contexto)],
    );
    return reply.code(201).send({ ok: true, id: r!.id });
  });

  // ── Panel ─────────────────────────────────────────────────────────────────
  const Filtro = z.object({ estado: z.enum(['', 'pendientes', 'revisados']).default(''), limite: z.coerce.number().int().min(1).max(500).default(200) });
  app.get('/admin/reportes-ia', { preHandler: requiereAdmin }, async (req) => {
    const f = Filtro.parse(req.query);
    const donde = f.estado === 'pendientes' ? 'WHERE NOT r.revisado' : f.estado === 'revisados' ? 'WHERE r.revisado' : '';
    const [filas, totales] = await Promise.all([
      query(`SELECT r.id, r.origen, r.motivo, r.texto, r.comentario, r.contexto, r.revisado, r.creado_en, u.id AS usuario_id, u.nombre, u.email
        FROM reportes_ia r JOIN usuarios u ON u.id = r.usuario_id ${donde} ORDER BY r.creado_en DESC LIMIT $1`, [f.limite]),
      uno<{ total: number; pendientes: number }>('SELECT count(*)::int AS total, count(*) FILTER (WHERE NOT revisado)::int AS pendientes FROM reportes_ia'),
    ]);
    return { reportes: filas, total: totales?.total ?? 0, pendientes: totales?.pendientes ?? 0 };
  });
  app.put('/admin/reportes-ia/:id', { preHandler: requiereAdmin }, async (req, reply) => {
    const { id } = z.object({ id: z.coerce.number().int().positive() }).parse(req.params);
    const { revisado } = z.object({ revisado: z.boolean() }).parse(req.body);
    const r = await uno('UPDATE reportes_ia SET revisado = $2 WHERE id = $1 RETURNING id, revisado', [id, revisado]);
    if (!r) return reply.code(404).send({ error: 'Reporte no encontrado' });
    return r;
  });
}
