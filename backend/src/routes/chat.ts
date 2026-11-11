import type { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import { PassThrough } from 'node:stream';
import { z } from 'zod';
import { contextoSituacion, objetivoValido } from '../lib/situaciones.js';
import { query } from '../lib/db.js';
import { iaDisponible, responder, resumirSesion } from '../lib/ia.js';
import { guardarInforme, Tecnico } from '../lib/informe_llamada.js';
import { openaiDisponible, transcribirOpenAI } from '../lib/ia_openai.js';
import { requiereAlumno, type Sesion } from '../lib/auth.js';
import { requierePractica } from '../lib/pagos/suscripciones.js';
import { actualizarFicha } from '../lib/ficha_alumno.js';
import { obtenerAudioAlineado, vozDisponible } from '../lib/voz.js';
import { indicacionEnSuIdioma, separadorDeLenguas, sinCorchetes } from '../lib/explicaciones.js';

const EsquemaChat = z.object({
  idiomaMeta: z.string().max(5), idiomaNativo: z.string().max(5).default('es'), nivel: z.number().int().min(1).max(10), tutorId: z.string().max(40).default('mia'),
  situacionId: z.number().int().min(1).max(50).optional(), situacion: z.string().max(4000).optional(), objetivo: z.string().max(4000).optional(),
  objetivoId: z.string().max(24).optional(), modo: z.enum(['practica', 'prueba']).default('practica'),
  // Videollamada: silencio largo o botón «Pista» (no es un turno del alumno).
  aviso: z.enum(['silencio', 'iniciativa', 'pista']).optional(),
  // Videollamada: el porqué de las correcciones y las pistas en el idioma del alumno o en el de la llamada.
  explica: z.enum(['nativo', 'meta']).optional(),
  // Topes: sin ellos, el límite de 2 MB del cuerpo dejaba mandar prompts enormes.
  historial: z.array(z.object({
    rol: z.enum(['tutor', 'alumno']), texto: z.string().max(4000),
    espera: z.object({ tipo: z.enum(['repetir', 'elegir', 'responder']), modelo: z.string().max(400) }).optional(),
  })).max(30),
});
type DatosChat = z.infer<typeof EsquemaChat>;

/** Una voz que tarda más que esto va como error (la página la pide aparte) y no retiene el final del stream. */
const VOZ_TOPE_MS = 8000;
const conTope = <T>(p: Promise<T>, ms: number) => {
  let t: NodeJS.Timeout | undefined;
  return Promise.race([p, new Promise<never>((_, mal) => { t = setTimeout(() => mal(new Error('voz_tardo')), ms); })]).finally(() => clearTimeout(t));
};

const objetivoInvalido = (d: DatosChat) =>
  !!d.objetivoId && !objetivoValido(d.idiomaMeta, d.situacionId, d.objetivoId);

async function guardarTurno(s: Sesion, d: DatosChat, r: Awaited<ReturnType<typeof responder>>) {
  const ultimo = d.aviso ? `[${d.aviso}]` : [...d.historial].reverse().find(t => t.rol === 'alumno')?.texto ?? '';
  await query('INSERT INTO conversaciones (usuario_id, situacion_id, nivel, idioma, tutor_id, mensaje_alumno, respuesta, modelo, tokens_entrada, tokens_salida) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)',
    [s.sub, d.situacionId ?? null, d.nivel, d.idiomaMeta, d.tutorId, ultimo, JSON.stringify(r.respuesta), r.modelo, r.entrada, r.salida]);
  await query('UPDATE usuarios SET ultima_actividad = now() WHERE id = $1', [s.sub]);
  // Cada pocos turnos el tutor pone al día lo que sabe del alumno, sin hacerle esperar.
  void actualizarFicha(s.sub, d.idiomaMeta, d.idiomaNativo, d.nivel).catch((e) => console.warn('ficha:', String(e).slice(0, 200)));
}

/**
 * Respuesta del tutor por SSE (frase, reply, final). `antes` corre dentro del
 * stream (p. ej. la transcripción de /chat/voz) y puede completar los datos.
 * Si el proveedor falla antes de emitir nada se reintenta una vez: un fallo
 * pasajero dejaba al alumno esperando sin respuesta.
 * Con `?voz=1` (videollamada) la voz de cada frase se genera en cuanto la frase
 * existe y viaja en el mismo stream (evento `voz`): ahorra la ida y vuelta de
 * pedirla aparte y la síntesis corre mientras el modelo sigue escribiendo.
 */
function responderSse(req: FastifyRequest, reply: FastifyReply, s: Sesion, preparar: (emit: (tipo: string, data: unknown) => void) => Promise<DatosChat | null>) {
  const output = new PassThrough();
  const started = performance.now();
  const controller = new AbortController();
  const deadline = setTimeout(() => controller.abort(), 45000);
  const emit = (tipo: string, data: unknown) => { if (!output.destroyed && !output.writableEnded) output.write(`data: ${JSON.stringify({ tipo, data })}\n\n`); };
  reply.raw.on('close', () => { if (!output.readableEnded) controller.abort(); });
  reply.type('text/event-stream').header('cache-control', 'no-cache, no-transform').header('x-accel-buffering', 'no');
  const heartbeat = setInterval(() => { if (!output.destroyed && !output.writableEnded) output.write(': keepalive\n\n'); }, 5000);
  const conVoz = (req.query as { voz?: string })?.voz === '1' && vozDisponible();
  const voces: Promise<void>[] = [];
  let fraseAnterior: { texto: string; habla?: string } = { texto: '' };
  // La página sabe así que la voz vendrá en el stream (si no, la pide aparte sin esperar).
  if (conVoz) output.write(`data: ${JSON.stringify({ tipo: 'voz_activa', data: true })}\n\n`);
  void (async () => {
    try {
      const d = await preparar(emit);
      if (!d) { output.end(); return; }
      const contexto = await contextoSituacion(s.sub, d);
      const peticion = { ...d, contexto };
      // Las explicaciones en el idioma del alumno llegan entre corchetes: cada
      // parte es una frase propia (otra pronunciación) y el alumno no ve los corchetes.
      const separar = separadorDeLenguas(peticion.idiomaMeta);
      let partes = 0;
      const emitirFrase = (texto: string, habla?: string) => {
        const indice = partes++;
        if (indice === 0) req.log.info({ ms: Math.round(performance.now() - started) }, 'chat_primera_frase');
        emit('frase', { indice, texto, ...(habla ? { habla } : {}) });
        if (conVoz && !controller.signal.aborted) {
          // Cada frase se mide y se lleva al mismo volumen (~75 ms): con la ganancia fija de la
          // voz, en prod variaban hasta 7 dB entre turnos (prueba del 11-11).
          // La frase anterior orienta la entonación solo si es del mismo idioma.
          const previo = fraseAnterior.habla === habla ? fraseAnterior.texto : ''; fraseAnterior = { texto, habla };
          voces.push(conTope(obtenerAudioAlineado({ texto, idioma: peticion.idiomaMeta, voz: peticion.tutorId, previo: previo || undefined, habla }), VOZ_TOPE_MS)
            .then((a) => {
              if (indice === 0) req.log.info({ ms: Math.round(performance.now() - started), cache: a.cache }, 'chat_primera_voz');
              emit('voz', { indice, audio: a.buffer.toString('base64'), alineacion: a.alineacion, respaldo: !!a.respaldo });
            })
            .catch((e) => { req.log.warn({ err: String(e) }, 'chat_voz'); emit('voz', { indice, error: true }); }));
        }
      };
      // La ayuda en el idioma del alumno se junta y suena una sola vez al final del
      // turno, con la voz nativa de ese idioma del mismo tutor: frase a frase,
      // alternando idiomas, se oía raro (11-11).
      let ayuda: string[] = [];
      let r: Awaited<ReturnType<typeof responder>> | undefined;
      for (let intento = 1; !r; intento++) {
        let emitido = false;
        ayuda = [];
        try {
          r = await responder(peticion, texto => {
            emitido = true;
            req.log.info({ ms: Math.round(performance.now() - started) }, 'chat_reply_ready');
            emit('reply', sinCorchetes(texto));
          }, controller.signal, (frase) => {
            emitido = true;
            for (const { texto, nativo, corchete } of separar(frase)) {
              // Lo que iba entre corchetes es una indicación, aunque viniera en el idioma meta.
              if (nativo || corchete) ayuda.push(texto); else emitirFrase(texto);
            }
          }, (espera) => emit('espera', espera));
        } catch (e) {
          if (emitido || controller.signal.aborted || intento >= 2) throw e;
          req.log.warn({ err: String(e) }, 'chat_reintento');
        }
      }
      if (ayuda.length) emitirFrase(await indicacionEnSuIdioma(ayuda.join(' '), peticion.idiomaMeta, peticion.idiomaNativo), peticion.idiomaNativo);
      r = { ...r, respuesta: { ...r.respuesta, reply: sinCorchetes(r.respuesta.reply) } };
      emit('final', r.respuesta);
      await Promise.all(voces);
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
      explica: z.enum(['meta', 'nativo']).default('meta'), tecnico: Tecnico.default({}),
    }).parse(req.body);
    if (!d.historial.some(t => t.rol === 'alumno')) return reply.code(400).send({ error: 'sin_turnos' });
    // Informe de la llamada (evaluación del tutor + datos técnicos): después de responder, sin espera para el alumno.
    const informe = (resumen: Awaited<ReturnType<typeof resumirSesion>> | null) => void guardarInforme({ usuarioId: s.sub, ...d, resumen })
      .catch((e) => req.log.warn({ err: String(e) }, 'informe_llamada'));
    try {
      const r = await resumirSesion(d);
      informe(r);
      await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)', [s.sub, 'resumen_tutor', JSON.stringify({ idioma: d.idiomaMeta, tutorId: d.tutorId, nivel: d.nivel, turnos: d.historial.filter(t => t.rol === 'alumno').length, ...r })]);
      // Al colgar, la ficha recoge la llamada entera aunque fuera corta.
      void actualizarFicha(s.sub, d.idiomaMeta, d.idiomaNativo, d.nivel, 1).catch((e) => req.log.warn({ err: String(e) }, 'ficha'));
      return r;
    } catch (e) {
      informe(null);
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
  app.post('/chat/voz', { preHandler: [requiereAlumno, requierePractica] }, async (req, reply) => {
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
      const { texto } = await transcribirOpenAI(audio.buffer, audio.nombre, d.idiomaMeta, audio.tipo, d.idiomaNativo);
      req.log.info({ ms: Math.round(performance.now() - t0), bytes: audio.buffer.length }, 'chat_voz_transcripcion');
      await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)', [s.sub, 'transcripcion', JSON.stringify({ idioma: d.idiomaMeta, caracteres: texto.length, bytes: audio.buffer.length, origen: 'videollamada' })]).catch(() => {});
      // Antes de emitirla: una transcripción vacía dejaba un turno del alumno
      // en blanco y «Reintentar» lo mandaba al modelo.
      if (!texto.trim()) { emit('error', 'No te escuché bien. Mantén pulsado el micrófono mientras hablas.'); return null; }
      emit('transcripcion', { texto });
      return { ...d, historial: [...d.historial, { rol: 'alumno' as const, texto }].slice(-30) };
    });
  });

  app.post('/chat', { preHandler: [requiereAlumno, requierePractica] }, async (req, reply) => {
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
    r = { ...r, respuesta: { ...r.respuesta, reply: sinCorchetes(r.respuesta.reply) } };
    await guardarTurno(s, d, r);
    return r.respuesta;
  });
}
