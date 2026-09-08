import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { query } from '../lib/db.js';
import { iaDisponible, responder } from '../lib/ia.js';
import { requiereAlumno, type Sesion } from '../lib/auth.js';

export default async function rutas(app: FastifyInstance) {
  app.get('/chat/estado', async () => ({ ia: iaDisponible() }));

  app.post('/chat', { preHandler: requiereAlumno }, async (req, reply) => {
    if (!iaDisponible()) return reply.code(503).send({ error: 'ia_no_configurada' });
    const s = req.user as Sesion;
    const d = z.object({
      idiomaMeta: z.string(), idiomaNativo: z.string().default('es'), nivel: z.number().int().min(1).max(10), tutorId: z.string().default('mia'),
      situacionId: z.number().int().optional(), situacion: z.string().optional(), objetivo: z.string().optional(),
      historial: z.array(z.object({ rol: z.enum(['tutor', 'alumno']), texto: z.string() })).max(30),
    }).parse(req.body);
    let r;
    try { r = await responder({ ...d, historial: d.historial }); }
    catch (e) { req.log.error({ err: String(e) }, 'ia'); return reply.code(502).send({ error: 'ia_error', detalle: String(e).slice(0, 200) }); }
    const ultimo = [...d.historial].reverse().find((t) => t.rol === 'alumno')?.texto ?? '';
    await query('INSERT INTO conversaciones (usuario_id, situacion_id, nivel, idioma, tutor_id, mensaje_alumno, respuesta, modelo, tokens_entrada, tokens_salida) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)',
      [s.sub, d.situacionId ?? null, d.nivel, d.idiomaMeta, d.tutorId, ultimo, JSON.stringify(r.respuesta), r.modelo, r.entrada, r.salida]);
    await query('UPDATE usuarios SET ultima_actividad = now() WHERE id = $1', [s.sub]);
    return r.respuesta;
  });
}
