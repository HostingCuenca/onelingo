import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { query } from '../lib/db.js';
import { config } from '../lib/config.js';
import { requiereAlumno, type Sesion } from '../lib/auth.js';
import { requierePractica } from '../lib/pagos/suscripciones.js';

/** Tokens por alumno y hora (cada llamada pide uno al empezar y otro si se reconecta). */
export const TOKENS_POR_HORA = 30;
const emitidos = new Map<string, number[]>();
export function puedeEmitir(usuario: string, ahora = Date.now()) {
  const recientes = (emitidos.get(usuario) ?? []).filter((t) => ahora - t < 3_600_000);
  if (recientes.length >= TOKENS_POR_HORA) { emitidos.set(usuario, recientes); return false; }
  recientes.push(ahora); emitidos.set(usuario, recientes); return true;
}
/** Si ElevenLabs no dio el token, no cuenta para el límite. */
const devolver = (usuario: string) => { emitidos.get(usuario)?.pop(); };
/** Segundos hasta que vuelva a haber cupo (cabecera Retry-After del 429). */
export const esperaCupo = (usuario: string, ahora = Date.now()) =>
  Math.max(1, Math.ceil(((emitidos.get(usuario)?.[0] ?? ahora) + 3_600_000 - ahora) / 1000));

/**
 * Al reconectar, la página cuenta cómo se cortó la sesión anterior (código y
 * motivo del cierre, segundos abierta, estado del audio, último aviso de
 * Scribe) y por qué pide el token: así se ve en `eventos` por qué se corta en
 * móviles. Las páginas viejas no mandan cuerpo.
 */
const Telemetria = z.object({
  motivo: z.enum(['inicio', 'reconexion', 'visible', 'reintento', 'manual']).optional(),
  cierre: z.object({
    codigo: z.number().int().optional(), razon: z.string().max(120).optional(), segundos: z.number().min(0).max(100_000).optional(),
    audio: z.string().max(20).optional(), aviso: z.string().max(160).optional(),
  }).nullish(),
}).catch({});

/**
 * Videollamada en vivo. El navegador transcribe el micrófono directamente con
 * ElevenLabs (Scribe v2 Realtime, por WebSocket) usando un token de un solo uso
 * que caduca a los 15 minutos: la clave de ElevenLabs nunca sale del servidor y
 * el audio del alumno no pasa por aquí (menos latencia).
 */
export default async function rutas(app: FastifyInstance) {
  app.post('/llamada/token', { preHandler: [requiereAlumno, requierePractica] }, async (req, reply) => {
    const s = req.user as Sesion;
    if (!config.elevenApiKey) return reply.code(503).send({ error: 'voz_no_configurada' });
    const datos = Telemetria.parse(req.body ?? {});
    if (!puedeEmitir(s.sub)) {
      req.log.warn({ ...datos }, 'llamada_token_limite');
      return reply.code(429).header('retry-after', String(esperaCupo(s.sub))).send({ error: 'demasiadas_llamadas' });
    }
    const r = await fetch('https://api.elevenlabs.io/v1/single-use-token/realtime_scribe', { method: 'POST', headers: { 'xi-api-key': config.elevenApiKey } })
      .catch(() => null);
    if (!r) { devolver(s.sub); return reply.code(502).send({ error: 'transcripcion_no_disponible' }); }
    if (!r.ok) {
      devolver(s.sub);
      req.log.error({ status: r.status, detalle: (await r.text().catch(() => '')).slice(0, 200) }, 'llamada_token');
      return reply.code(502).send({ error: 'transcripcion_no_disponible' });
    }
    const { token } = await r.json() as { token?: string };
    if (!token) { devolver(s.sub); return reply.code(502).send({ error: 'transcripcion_no_disponible' }); }
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)', [s.sub, 'llamada_token', JSON.stringify(datos)]).catch(() => {});
    return { token, url: 'wss://api.elevenlabs.io/v1/speech-to-text/realtime', modelo: 'scribe_v2_realtime', caducaEnSegundos: 900 };
  });
}
