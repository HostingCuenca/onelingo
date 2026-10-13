import type { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import { z } from 'zod';
import { query } from '../lib/db.js';
import { config } from '../lib/config.js';
import { obtenerAudio, obtenerAudioStream, leerAudio, vozDisponible, VOCES, cuotaVoz, textoParaVoz, hashAudio } from '../lib/voz.js';
import { transcribirOpenAI, openaiDisponible } from '../lib/ia_openai.js';
import { requiereAlumno, requiereAdmin, type Sesion } from '../lib/auth.js';

/** Igual que requiereAlumno pero acepta `?token=` (reproductores de audio que no pueden mandar cabeceras). */
async function alumnoOToken(req: FastifyRequest, reply: FastifyReply) {
  const t = (req.query as any)?.token as string | undefined;
  if (t && !req.headers.authorization) req.headers.authorization = `Bearer ${t}`;
  return requiereAlumno(req, reply);
}
async function adminOToken(req: FastifyRequest, reply: FastifyReply) {
  const t = (req.query as any)?.token as string | undefined;
  if (t && !req.headers.authorization) req.headers.authorization = `Bearer ${t}`;
  return requiereAdmin(req, reply);
}

export default async function rutas(app: FastifyInstance) {
  app.get('/voz/estado', async () => ({
    voz: vozDisponible(), modelo: config.elevenModelo, transcripcion: openaiDisponible(),
    voces: Object.fromEntries(Object.entries(VOCES).map(([k, v]) => [k, { nombre: v.nombre, descripcion: v.descripcion }])),
  }));

  app.get('/voz/stream', { preHandler: alumnoOToken }, async (req, reply) => {
    const q = z.object({ texto: z.string().min(1).max(600), idioma: z.string().default('en'), voz: z.string().optional(), modo: z.enum(['letra']).optional() }).parse(req.query);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 30000);
    const started = performance.now();
    reply.raw.on('close', () => { clearTimeout(timer); controller.abort(); });
    try {
      const a = await obtenerAudioStream(q, controller.signal, () => req.log.info({ ms: Math.round(performance.now() - started) }, 'voz_first_chunk'));
      return reply.type('audio/mpeg').header('cache-control', 'private, no-store')
        .header('x-accel-buffering', 'no').header('x-voz-cache', a.cache ? 'hit' : 'miss').send(a.stream);
    } catch (e) {
      clearTimeout(timer);
      req.log.error({ err: String(e) }, 'voz_stream');
      return reply.code(502).send({ error: 'voz_error' });
    }
  });

  /** MP3 de un texto. Se genera la primera vez y luego sale de la caché (cabecera X-Voz-Cache). */
  app.get('/voz', { preHandler: alumnoOToken }, async (req, reply) => {
    const q = z.object({ texto: z.string().min(1), idioma: z.string().default('en'), voz: z.string().optional(), modo: z.enum(['letra']).optional(), token: z.string().optional() }).parse(req.query);
    try {
      const a = await obtenerAudio(q);
      return reply.type('audio/mpeg')
        .header('cache-control', 'public, max-age=31536000, immutable')
        .header('x-voz-cache', a.cache ? 'hit' : 'miss')
        .header('x-voz-hash', a.hash)
        .header('x-voz-voz', a.voz)
        .send(a.buffer);
    } catch (e) {
      req.log.error({ err: String(e) }, 'voz');
      return reply.code(502).send({ error: 'voz_error', detalle: String(e).slice(0, 200) });
    }
  });

  /** Pregenera en lote (p. ej. todos los textos de una lección) y devuelve los hashes. */
  app.post('/voz/lote', { preHandler: requiereAlumno }, async (req, reply) => {
    const d = z.object({ idioma: z.string(), voz: z.string().optional(), textos: z.array(z.string().min(1)).min(1).max(60) }).parse(req.body);
    const resultados: { texto: string; hash?: string; cache?: boolean; error?: string }[] = [];
    for (const texto of d.textos) {
      try { const a = await obtenerAudio({ texto, idioma: d.idioma, voz: d.voz }); resultados.push({ texto, hash: a.hash, cache: a.cache }); }
      catch (e) { resultados.push({ texto, error: String(e).slice(0, 120) }); }
    }
    return { resultados, generados: resultados.filter((r) => r.cache === false).length };
  });

  /** Audio ya generado, por hash (URL estable para reutilizar sin volver a llamar a la API). */
  app.get('/voz/audio/:hash', { preHandler: alumnoOToken }, async (req, reply) => {
    const { hash } = z.object({ hash: z.string() }).parse(req.params);
    const b = await leerAudio(hash);
    if (!b) return reply.code(404).send({ error: 'no_existe' });
    await query('UPDATE audios SET usos = usos + 1, ultimo_uso = now() WHERE hash = $1', [hash]).catch(() => {});
    return reply.type('audio/mpeg').header('cache-control', 'public, max-age=31536000, immutable').send(b);
  });

  /** Voz del alumno → texto (OpenAI). multipart: campo `audio` + campo `idioma`. */
  app.post('/transcribir', { preHandler: requiereAlumno }, async (req, reply) => {
    if (!openaiDisponible()) return reply.code(503).send({ error: 'transcripcion_no_configurada' });
    const s = req.user as Sesion;
    let idioma = 'en'; let archivo: { buffer: Buffer; nombre: string; tipo: string } | null = null;
    for await (const parte of req.parts()) {
      if (parte.type === 'file') archivo = { buffer: await parte.toBuffer(), nombre: parte.filename || 'audio.m4a', tipo: parte.mimetype || 'audio/m4a' };
      else if (parte.fieldname === 'idioma') idioma = String(parte.value);
    }
    if (!archivo || archivo.buffer.length === 0) return reply.code(400).send({ error: 'sin_audio' });
    try {
      const r = await transcribirOpenAI(archivo.buffer, archivo.nombre, idioma, archivo.tipo);
      await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)', [s.sub, 'transcripcion', JSON.stringify({ idioma, caracteres: r.texto.length, bytes: archivo.buffer.length })]).catch(() => {});
      return r;
    } catch (e) {
      req.log.error({ err: String(e) }, 'transcribir');
      return reply.code(502).send({ error: 'transcripcion_error', detalle: String(e).slice(0, 200) });
    }
  });

  // ---- Panel ----
  app.get('/admin/audios', { preHandler: requiereAdmin }, async () => {
    const [tot] = await query(`SELECT count(*)::int AS audios, coalesce(sum(caracteres),0)::int AS caracteres, coalesce(sum(bytes),0)::int AS bytes,
        coalesce(sum(usos),0)::int AS reproducciones FROM audios`);
    const porIdioma = await query('SELECT idioma, count(*)::int AS audios, sum(caracteres)::int AS caracteres FROM audios GROUP BY 1 ORDER BY 2 DESC');
    const porVoz = await query('SELECT voz, count(*)::int AS audios FROM audios GROUP BY 1 ORDER BY 2 DESC');
    const ultimos = await query('SELECT hash, idioma, voz, texto, caracteres, bytes, usos, creado_en, ultimo_uso FROM audios ORDER BY creado_en DESC LIMIT 100');
    return { ...tot, porIdioma, porVoz, ultimos, cuota: await cuotaVoz(), voces: VOCES, modelo: config.elevenModelo };
  });
  app.get('/admin/audios/:hash', { preHandler: adminOToken }, async (req, reply) => {
    const { hash } = z.object({ hash: z.string() }).parse(req.params);
    const b = await leerAudio(hash);
    if (!b) return reply.code(404).send({ error: 'no_existe' });
    return reply.type('audio/mpeg').send(b);
  });
  /** Prueba de voz desde el panel (genera o reutiliza). */
  app.post('/admin/audios/probar', { preHandler: requiereAdmin }, async (req, reply) => {
    const d = z.object({ texto: z.string().min(1), idioma: z.string().default('en'), voz: z.string().optional() }).parse(req.body);
    try {
      const a = await obtenerAudio(d);
      return { hash: a.hash, cache: a.cache, voz: a.voz, caracteres: a.caracteres, existiaHash: hashAudio(textoParaVoz(d.texto, d.idioma), VOCES[a.voz].id, config.elevenModelo, d.idioma) === a.hash };
    } catch (e) { return reply.code(502).send({ error: String(e).slice(0, 200) }); }
  });
}
