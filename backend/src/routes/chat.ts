import type { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import { PassThrough } from 'node:stream';
import { z } from 'zod';
import { contextoSituacion, unidades } from '../lib/situaciones.js';
import { query } from '../lib/db.js';
import { iaDisponible, responder, resumirSesion } from '../lib/ia.js';
import { openaiDisponible, transcribirOpenAI } from '../lib/ia_openai.js';
import { requiereAlumno, type Sesion } from '../lib/auth.js';

const EsquemaChat = z.object({
  idiomaMeta: z.string(), idiomaNativo: z.string().default('es'), nivel: z.number().int().min(1).max(10), tutorId: z.string().default('mia'),
  situacionId: z.number().int().min(1).max(50).optional(), situacion: z.string().optional(), objetivo: z.string().optional(),
  objetivoId: z.string().max(24).optional(), modo: z.enum(['practica', 'prueba']).default('practica'),
  historial: z.array(z.object({ rol: z.enum(['tutor', 'alumno']), texto: z.string() })).max(30),
});
type DatosChat = z.infer<typeof EsquemaChat>;

const objetivoInvalido = (d: DatosChat) =>
  !!d.objetivoId && (d.idiomaMeta !== 'en' || !unidades.find(u => u.id === d.situacionId)?.objetivos.some(o => o.id === d.objetivoId));

async function guardarTurno(s: Sesion, d: DatosChat, r: Awaited<ReturnType<typeof responder>>) {
  const ultimo = [...d.historial].reverse().find(t => t.rol === 'alumno')?.texto ?? '';
  await query('INSERT INTO conversaciones (usuario_id, situacion_id, nivel, idioma, tutor_id, mensaje_alumno, respuesta, modelo, tokens_entrada, tokens_salida) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)',
    [s.sub, d.situacionId ?? null, d.nivel, d.idiomaMeta, d.tutorId, ultimo, JSON.stringify(r.respuesta), r.modelo, r.entrada, r.salida]);
  await query('UPDATE usuarios SET ultima_actividad = now() WHERE id = $1', [s.sub]);
}

/**
 * Respuesta del tutor por SSE (frase, reply, final). `antes` corre dentro del
 * stream (p. ej. la transcripción de /chat/voz) y puede completar los datos.
 * Si el proveedor falla antes de emitir nada se reintenta una vez: un fallo
 * pasajero dejaba al alumno esperando sin respuesta.
 */
function responderSse(req: FastifyRequest, reply: FastifyReply, s: Sesion, preparar: (emit: (tipo: string, data: unknown) => void) => Promise<DatosChat | null>) {
  const output = new PassThrough();
  const started = performance.now();
  const controller = new AbortController();
  const deadline = setTimeout(() => controller.abort(), 45000);
  const emit = (tipo: string, data: unknown) => { if (!output.destroyed) output.write(`data: ${JSON.stringify({ tipo, data })}\n\n`); };
  reply.raw.on('close', () => { if (!output.readableEnded) controller.abort(); });
  reply.type('text/event-stream').header('cache-control', 'no-cache, no-transform').header('x-accel-buffering', 'no');
  const heartbeat = setInterval(() => { if (!output.destroyed) output.write(': keepalive\n\n'); }, 5000);
  void (async () => {
    try {
      const d = await preparar(emit);
      if (!d) { output.end(); return; }
      const contexto = await contextoSituacion(s.sub, d);
      const peticion = { ...d, contexto };
      let r: Awaited<ReturnType<typeof responder>> | undefined;
      for (let intento = 1; !r; intento++) {
        let emitido = false;
        try {
          r = await responder(peticion, texto => {
            emitido = true;
            req.log.info({ ms: Math.round(performance.now() - started) }, 'chat_reply_ready');
            emit('reply', texto);
          }, controller.signal, (texto, indice) => {
            emitido = true;
            if (indice === 0) req.log.info({ ms: Math.round(performance.now() - started) }, 'chat_primera_frase');
            emit('frase', { indice, texto });
          });
        } catch (e) {
          if (emitido || controller.signal.aborted || intento >= 2) throw e;
          req.log.warn({ err: String(e) }, 'chat_reintento');
        }
      }
      emit('final', r.respuesta);
      output.end();
      await guardarTurno(s, d, r);
      req.log.info({ ms: Math.round(performance.now() - started) }, 'chat_complete');
    } catch (e) {
      req.log.error({ err: String(e) }, 'chat_stream');
      if (!output.writableEnded) { emit('error', 'No se pudo completar la respuesta'); output.end(); }
    } finally { clearInterval(heartbeat); clearTimeout(deadline); }
  })();
  return reply.send(output);
}

export default async function rutas(app: FastifyInstance) {
  app.get('/chat/estado', async () => ({ ia: iaDisponible() }));

  /** Resumen al colgar la videollamada: logros, errores, vocabulario y hechos del alumno (se guardan para personalizar la siguiente llamada). */
  app.post('/chat/resumen', { preHandler: requiereAlumno }, async (req, reply) => {
    if (!iaDisponible()) return reply.code(503).send({ error: 'ia_no_configurada' });
    const s = req.user as Sesion;
    const d = z.object({
      idiomaMeta: z.string().max(5), idiomaNativo: z.string().max(5).default('es'), nivel: z.number().int().min(1).max(10), tutorId: z.string().max(40),
      historial: z.array(z.object({ rol: z.enum(['tutor', 'alumno']), texto: z.string().max(1200) })).max(40),
    }).parse(req.body);
    if (!d.historial.some(t => t.rol === 'alumno')) return reply.code(400).send({ error: 'sin_turnos' });
    try {
      const r = await resumirSesion(d);
      await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)', [s.sub, 'resumen_tutor', JSON.stringify({ idioma: d.idiomaMeta, tutorId: d.tutorId, nivel: d.nivel, turnos: d.historial.filter(t => t.rol === 'alumno').length, ...r })]);
      return r;
    } catch (e) {
      req.log.error({ err: String(e) }, 'chat_resumen');
      return reply.code(502).send({ error: 'resumen_error' });
    }
  });

  /**
   * Turno de voz en una sola petición (videollamada): audio del alumno →
   * transcripción (evento `transcripcion`) → respuesta del tutor por frases.
   * Ahorra el viaje de ida y vuelta entre /transcribir y /chat.
   * multipart: `datos` (JSON como /chat, historial SIN el turno nuevo) + `audio`.
   */
  app.post('/chat/voz', { preHandler: requiereAlumno }, async (req, reply) => {
    if (!iaDisponible() || !openaiDisponible()) return reply.code(503).send({ error: 'ia_no_configurada' });
    const s = req.user as Sesion;
    let crudo: unknown; let archivo: { buffer: Buffer; nombre: string; tipo: string } | null = null;
    for await (const parte of req.parts()) {
      if (parte.type === 'file') archivo = { buffer: await parte.toBuffer(), nombre: parte.filename || 'turno.webm', tipo: parte.mimetype || 'audio/webm' };
      else if (parte.fieldname === 'datos') { try { crudo = JSON.parse(String(parte.value)); } catch { crudo = undefined; } }
    }
    const parsed = EsquemaChat.safeParse(crudo);
    if (!parsed.success || !archivo?.buffer.length) return reply.code(400).send({ error: 'datos_invalidos' });
    const d = parsed.data;
    if (objetivoInvalido(d)) return reply.code(400).send({ error: 'objetivo_invalido' });
    const audio = archivo;
    return responderSse(req, reply, s, async emit => {
      const t0 = performance.now();
      const { texto } = await transcribirOpenAI(audio.buffer, audio.nombre, d.idiomaMeta, audio.tipo);
      req.log.info({ ms: Math.round(performance.now() - t0), bytes: audio.buffer.length }, 'chat_voz_transcripcion');
      emit('transcripcion', { texto });
      await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)', [s.sub, 'transcripcion', JSON.stringify({ idioma: d.idiomaMeta, caracteres: texto.length, bytes: audio.buffer.length, origen: 'videollamada' })]).catch(() => {});
      if (!texto.trim()) { emit('error', 'No te escuché bien. Mantén pulsado el micrófono mientras hablas.'); return null; }
      return { ...d, historial: [...d.historial, { rol: 'alumno' as const, texto }].slice(-30) };
    });
  });

  app.post('/chat', { preHandler: requiereAlumno }, async (req, reply) => {
    if (!iaDisponible()) return reply.code(503).send({ error: 'ia_no_configurada' });
    const s = req.user as Sesion;
    const d = EsquemaChat.parse(req.body);
    if (objetivoInvalido(d)) return reply.code(400).send({ error: 'objetivo_invalido' });
    if (req.headers.accept?.includes('text/event-stream')) return responderSse(req, reply, s, async () => d);
    let contexto: string;
    try { contexto = await contextoSituacion(s.sub, d); }
    catch (error) { req.log.error({ err: String(error) }, 'chat_contexto'); return reply.code(503).send({ error: 'contexto_no_disponible' }); }
    let r;
    try { r = await responder({ ...d, contexto }); }
    catch (e) { req.log.error({ err: String(e) }, 'ia'); return reply.code(502).send({ error: 'ia_error', detalle: String(e).slice(0, 200) }); }
    await guardarTurno(s, d, r);
    return r.respuesta;
  });
}
