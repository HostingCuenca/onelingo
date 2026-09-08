/** Voz con ElevenLabs. Cada texto se sintetiza UNA vez: se guarda en AUDIO_DIR/<hash>.mp3 y en la tabla `audios`. */
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { config } from './config.js';
import { query, uno } from './db.js';

/** Voces por rol: los 4 tutores de la app + narradores neutros para lecciones y Listening. */
export const VOCES: Record<string, { id: string; nombre: string; descripcion: string }> = {
  mia: { id: 'EXAVITQu4vr4xnSDxMaL', nombre: 'Sarah', descripcion: 'Tutora amigable: cálida y tranquilizadora' },
  leo: { id: 'TX3LPaxmHKxFdv7VOQHJ', nombre: 'Liam', descripcion: 'Tutor motivador: enérgico y cercano' },
  sofia: { id: 'XrExE9yKIg1WjnnlVkGX', nombre: 'Matilda', descripcion: 'Tutora profesional: clara y experta' },
  max: { id: 'pNInz6obpgDQGcFmaJgB', nombre: 'Adam', descripcion: 'Tutor directo: firme y conciso' },
  narradora: { id: 'Xb7hH8MSUJpSbSDYk0k2', nombre: 'Alice', descripcion: 'Narradora de lecciones y Listening' },
  narrador: { id: 'JBFqnCBsd6RMkjVDRZzb', nombre: 'George', descripcion: 'Narrador de diálogos y Listening' },
};

export const vozDisponible = () => config.elevenApiKey.length > 0;

/** Quita la romanización "(…)" y normaliza espacios: solo se sintetiza el texto nativo. */
export function textoParaVoz(t: string) {
  return t.replace(/\s*\([^)]*\)/g, '').replace(/\s+/g, ' ').trim();
}

export function hashAudio(texto: string, vozId: string, modelo: string) {
  return createHash('sha256').update(`${modelo}|${vozId}|${texto}`).digest('hex').slice(0, 40);
}

const dir = () => path.resolve(config.audioDir);
const enCurso = new Map<string, Promise<Buffer>>();

async function sintetizar(texto: string, vozId: string): Promise<Buffer> {
  const url = `https://api.elevenlabs.io/v1/text-to-speech/${vozId}?output_format=mp3_44100_128`;
  let r!: Response;
  for (let i = 0; i < 3; i++) {
    r = await fetch(url, {
      method: 'POST',
      headers: { 'xi-api-key': config.elevenApiKey, 'content-type': 'application/json' },
      body: JSON.stringify({ text: texto, model_id: config.elevenModelo, voice_settings: { stability: 0.5, similarity_boost: 0.75, style: 0.2, use_speaker_boost: true } }),
    });
    if (r.ok) return Buffer.from(await r.arrayBuffer());
    if ((r.status === 429 || r.status >= 500) && i < 2) { await new Promise((res) => setTimeout(res, 1000 * (i + 1))); continue; }
    break;
  }
  const detalle = await r.text().catch(() => '');
  throw new Error(`ElevenLabs ${r.status}: ${detalle.slice(0, 200)}`);
}

export type Audio = { hash: string; buffer: Buffer; cache: boolean; voz: string; caracteres: number };

/** Devuelve el MP3 de `texto` con la voz del rol `voz`; lo genera solo si no existe. */
export async function obtenerAudio(p: { texto: string; idioma: string; voz?: string }): Promise<Audio> {
  if (!vozDisponible()) throw new Error('voz_no_configurada');
  const texto = textoParaVoz(p.texto);
  if (!texto) throw new Error('texto_vacio');
  if (texto.length > config.vozMaxCaracteres) throw new Error(`texto_demasiado_largo (${texto.length} > ${config.vozMaxCaracteres})`);
  const rol = VOCES[p.voz ?? ''] ? (p.voz as string) : 'narradora';
  const v = VOCES[rol];
  const hash = hashAudio(texto, v.id, config.elevenModelo);
  const ruta = path.join(dir(), `${hash}.mp3`);

  // 1) Caché en disco + registro de uso.
  try {
    const buffer = await readFile(ruta);
    await query('UPDATE audios SET usos = usos + 1, ultimo_uso = now() WHERE hash = $1', [hash]);
    return { hash, buffer, cache: true, voz: rol, caracteres: texto.length };
  } catch { /* no existe: generar */ }

  // 2) Generación con deduplicación de peticiones simultáneas.
  let pendiente = enCurso.get(hash);
  if (!pendiente) {
    pendiente = (async () => {
      await mkdir(dir(), { recursive: true });
      const buffer = await sintetizar(texto, v.id);
      await writeFile(ruta, buffer);
      await query(
        `INSERT INTO audios (hash, idioma, voz, voz_id, modelo, texto, caracteres, bytes) VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
         ON CONFLICT (hash) DO UPDATE SET usos = audios.usos + 1, ultimo_uso = now()`,
        [hash, p.idioma, rol, v.id, config.elevenModelo, texto, texto.length, buffer.length]);
      return buffer;
    })().finally(() => enCurso.delete(hash));
    enCurso.set(hash, pendiente);
  }
  const buffer = await pendiente;
  return { hash, buffer, cache: false, voz: rol, caracteres: texto.length };
}

export async function leerAudio(hash: string): Promise<Buffer | null> {
  if (!/^[a-f0-9]{40}$/.test(hash)) return null;
  const ruta = path.join(dir(), `${hash}.mp3`);
  try { await stat(ruta); return await readFile(ruta); } catch { return null; }
}

/** Estado de la cuota mensual en ElevenLabs (para el panel). */
export async function cuotaVoz() {
  if (!vozDisponible()) return null;
  try {
    const r = await fetch('https://api.elevenlabs.io/v1/user/subscription', { headers: { 'xi-api-key': config.elevenApiKey } });
    if (!r.ok) return null;
    const j: any = await r.json();
    return { plan: j.tier, usados: j.character_count, limite: j.character_limit, reinicio: j.next_character_count_reset_unix ? new Date(j.next_character_count_reset_unix * 1000).toISOString() : null };
  } catch { return null; }
}

export const vozExiste = (hash: string) => uno('SELECT hash FROM audios WHERE hash = $1', [hash]);
