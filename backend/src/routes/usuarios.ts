import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { query, uno } from '../lib/db.js';
import { requiereAlumno, type Sesion } from '../lib/auth.js';

const Registro = z.object({
  email: z.string().email(),
  nombre: z.string().min(1),
  idiomaNativo: z.string().default('es'),
  idiomaMeta: z.string().default('en'),
  nivelInicial: z.number().int().min(1).max(10).default(1),
  plataforma: z.string().default(''),
});

/** Estado completo tal como lo guarda la app (ProgressState.toJson). */
const Estado = z.object({
  onboardingDone: z.boolean().optional(),
  nombre: z.string().optional(),
  idiomaNativo: z.string().optional(),
  idiomaMeta: z.string().optional(),
  nivelInicial: z.number().optional(),
  fundamentos: z.boolean().optional(),
  diagnostico: z.record(z.any()).optional(),
  practicas: z.record(z.any()).default({}),
  completadas: z.array(z.string()).default([]),
  puntuaciones: z.record(z.number()).default({}),
  examenes: z.record(z.number()).default({}),
  errores: z.array(z.object({
    id: z.string(), skill: z.string(), original: z.string(), correccion: z.string(),
    explicacion: z.string().default(''), fecha: z.string(), origen: z.string().default(''), practicado: z.boolean().default(false),
  })).default([]),
  xp: z.number().default(0),
  racha: z.number().default(0),
  ultimoDia: z.string().optional(),
  segundosEstudio: z.number().default(0),
  trialInicio: z.string().nullable().optional(),
  trialSegundos: z.number().default(0),
  tutorId: z.string().default('mia'),
  planId: z.string().default(''),
}).passthrough();

function nivelActual(estado: z.infer<typeof Estado>): number {
  let n = estado.nivelInicial ?? 1;
  while (n < 10 && (estado.examenes[String(n)] ?? 0) >= 65) n++;
  return n;
}

export default async function rutas(app: FastifyInstance) {
  app.post('/usuarios/registro', async (req, reply) => {
    const d = Registro.parse(req.body);
    const email = d.email.toLowerCase();
    const existente = await uno('SELECT id FROM usuarios WHERE email = $1', [email]);
    const u = existente
      ? await uno('UPDATE usuarios SET nombre=$2, idioma_nativo=$3, idioma_meta=$4, nivel_inicial=$5, plataforma=$6, ultima_actividad=now() WHERE email=$1 RETURNING id', [email, d.nombre, d.idiomaNativo, d.idiomaMeta, d.nivelInicial, d.plataforma])
      : await uno('INSERT INTO usuarios (email, nombre, idioma_nativo, idioma_meta, nivel_inicial, plataforma, trial_inicio, es_demo) VALUES ($1,$2,$3,$4,$5,$6, now(), true) RETURNING id', [email, d.nombre, d.idiomaNativo, d.idiomaMeta, d.nivelInicial, d.plataforma]);
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)', [u!.id, existente ? 'login' : 'registro', JSON.stringify({ idiomaMeta: d.idiomaMeta })]);
    const token = app.jwt.sign({ sub: u!.id, rol: 'alumno' } satisfies Sesion);
    return reply.code(existente ? 200 : 201).send({ id: u!.id, token });
  });

  app.post('/usuarios/login', async (req, reply) => {
    const { email } = z.object({ email: z.string().email() }).parse(req.body);
    const u = await uno('SELECT id FROM usuarios WHERE email = $1', [email.toLowerCase()]);
    if (!u) return reply.code(404).send({ error: 'Usuario no encontrado' });
    await query('UPDATE usuarios SET ultima_actividad = now() WHERE id = $1', [u.id]);
    await query('INSERT INTO eventos (usuario_id, tipo) VALUES ($1, $2)', [u.id, 'login']);
    return { id: u.id, token: app.jwt.sign({ sub: u.id, rol: 'alumno' } satisfies Sesion) };
  });

  app.put('/usuarios/me/progreso', { preHandler: requiereAlumno }, async (req) => {
    const s = req.user as Sesion;
    const estado = Estado.parse(req.body);
    const nivel = nivelActual(estado);
    await query(
      `INSERT INTO progreso (usuario_id, estado, nivel_actual, lecciones_completadas, xp, racha, segundos_estudio, actualizado_en)
       VALUES ($1,$2,$3,$4,$5,$6,$7, now())
       ON CONFLICT (usuario_id) DO UPDATE SET estado=EXCLUDED.estado, nivel_actual=EXCLUDED.nivel_actual,
         lecciones_completadas=EXCLUDED.lecciones_completadas, xp=EXCLUDED.xp, racha=EXCLUDED.racha,
         segundos_estudio=EXCLUDED.segundos_estudio, actualizado_en=now()`,
      [s.sub, JSON.stringify(estado), nivel, estado.completadas.length, estado.xp, estado.racha, estado.segundosEstudio],
    );
    await query(
      `UPDATE usuarios SET nombre = COALESCE($2, nombre), idioma_nativo = COALESCE($3, idioma_nativo), idioma_meta = COALESCE($4, idioma_meta),
         plan_id=$5, tutor_id=$6, trial_segundos=$7, trial_inicio = COALESCE($8::timestamptz, trial_inicio), ultima_actividad=now() WHERE id=$1`,
      [s.sub, estado.nombre ?? null, estado.idiomaNativo ?? null, estado.idiomaMeta ?? null, estado.planId, estado.tutorId, estado.trialSegundos, estado.trialInicio ?? null],
    );
    for (const e of estado.errores) {
      await query(
        `INSERT INTO errores (id, usuario_id, skill, original, correccion, explicacion, origen, practicado, fecha)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) ON CONFLICT (usuario_id, id) DO UPDATE SET practicado = EXCLUDED.practicado`,
        [e.id, s.sub, e.skill, e.original, e.correccion, e.explicacion, e.origen, e.practicado, e.fecha],
      );
    }
    for (const [nivelStr, pct] of Object.entries(estado.examenes)) {
      await query(
        `INSERT INTO examenes (usuario_id, nivel, pct, aprobado, fecha) VALUES ($1,$2,$3,$4, now())
         ON CONFLICT (usuario_id, nivel) DO UPDATE SET pct = EXCLUDED.pct, aprobado = EXCLUDED.aprobado, fecha = now()`,
        [s.sub, Number(nivelStr), pct, pct >= 65],
      );
    }
    return { ok: true, nivelActual: nivel };
  });

  app.post('/usuarios/me/eventos', { preHandler: requiereAlumno }, async (req) => {
    const s = req.user as Sesion;
    const { tipo, datos } = z.object({ tipo: z.string().min(1), datos: z.record(z.any()).default({}) }).parse(req.body);
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1,$2,$3)', [s.sub, tipo, JSON.stringify(datos)]);
    await query('UPDATE usuarios SET ultima_actividad = now() WHERE id = $1', [s.sub]);
    return { ok: true };
  });
}
