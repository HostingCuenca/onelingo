import type { FastifyInstance } from 'fastify';
import { PassThrough } from 'node:stream';
import { z } from 'zod';
import { contextoSituacion, unidades } from '../lib/situaciones.js';
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
      situacionId: z.number().int().min(1).max(50).optional(), situacion: z.string().optional(), objetivo: z.string().optional(),
      objetivoId: z.string().max(24).optional(), modo: z.enum(['practica', 'prueba']).default('practica'),
      historial: z.array(z.object({ rol: z.enum(['tutor', 'alumno']), texto: z.string() })).max(30),
    }).parse(req.body);
    if (d.objetivoId && (d.idiomaMeta !== 'en' || !unidades.find(u => u.id === d.situacionId)?.objetivos.some(o => o.id === d.objetivoId))) {
      return reply.code(400).send({ error: 'objetivo_invalido' });
    }
    let contexto: string;
    try { contexto = await contextoSituacion(s.sub, d); }
    catch (error) { req.log.error({ err: String(error) }, 'chat_contexto'); return reply.code(503).send({ error: 'contexto_no_disponible' }); }
    const peticion = { ...d, contexto };
    const streaming = req.headers.accept?.includes('text/event-stream');
    const controller = new AbortController();
    const deadline = setTimeout(() => controller.abort(), 40000);
    if (streaming) {
      const output = new PassThrough();
      const started = performance.now();
      const emit = (tipo: string, data: unknown) => {
        if (!output.destroyed) output.write(`data: ${JSON.stringify({ tipo, data })}\n\n`);
      };
      reply.raw.on('close', () => { if (!output.readableEnded) controller.abort(); });
      reply.type('text/event-stream').header('cache-control', 'no-cache, no-transform').header('x-accel-buffering', 'no');
      const heartbeat = setInterval(() => { if (!output.destroyed) output.write(': keepalive\n\n'); }, 5000);
      void (async () => {
        try {
          const r = await responder(peticion, texto => {
            req.log.info({ ms: Math.round(performance.now() - started) }, 'chat_reply_ready');
            emit('reply', texto);
          }, controller.signal);
          emit('final', r.respuesta);
          output.end();
          const ultimo = [...d.historial].reverse().find(t => t.rol === 'alumno')?.texto ?? '';
          await query('INSERT INTO conversaciones (usuario_id, situacion_id, nivel, idioma, tutor_id, mensaje_alumno, respuesta, modelo, tokens_entrada, tokens_salida) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)', [s.sub, d.situacionId ?? null, d.nivel, d.idiomaMeta, d.tutorId, ultimo, JSON.stringify(r.respuesta), r.modelo, r.entrada, r.salida]);
          await query('UPDATE usuarios SET ultima_actividad = now() WHERE id = $1', [s.sub]);
          req.log.info({ ms: Math.round(performance.now() - started) }, 'chat_complete');
        } catch (e) {
          req.log.error({ err: String(e) }, 'chat_stream');
          if (!output.writableEnded) { emit('error', 'No se pudo completar la respuesta'); output.end(); }
        } finally { clearInterval(heartbeat); clearTimeout(deadline); }
      })();
      return reply.send(output);
    }
    clearTimeout(deadline);
    let r;
    try { r = await responder(peticion); }
    catch (e) { req.log.error({ err: String(e) }, 'ia'); return reply.code(502).send({ error: 'ia_error', detalle: String(e).slice(0, 200) }); }
    const ultimo = [...d.historial].reverse().find((t) => t.rol === 'alumno')?.texto ?? '';
    await query('INSERT INTO conversaciones (usuario_id, situacion_id, nivel, idioma, tutor_id, mensaje_alumno, respuesta, modelo, tokens_entrada, tokens_salida) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)',
      [s.sub, d.situacionId ?? null, d.nivel, d.idiomaMeta, d.tutorId, ultimo, JSON.stringify(r.respuesta), r.modelo, r.entrada, r.salida]);
    await query('UPDATE usuarios SET ultima_actividad = now() WHERE id = $1', [s.sub]);
    return r.respuesta;
  });
}
