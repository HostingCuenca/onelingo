/** Voz con ElevenLabs. Cada texto se sintetiza UNA vez: se guarda en AUDIO_DIR/<hash>.mp3 y en la tabla `audios`. */
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile, stat, rename, unlink } from 'node:fs/promises';
import path from 'node:path';
import { Readable } from 'node:stream';
import { config } from './config.js';
import { query, uno } from './db.js';

/** Voces por rol: los 4 tutores de la app + narradores neutros para lecciones y Listening. */
export const VOCES: Record<string, { id: string; nombre: string; descripcion: string }> = {
  "avatar_amara": {"id": "M6ic45wruJGWAxLFEMNK", "nombre": "Amara", "descripcion": "Zoe · afroamericana · conversacional"},
  "avatar_sofia": {"id": "XrExE9yKIg1WjnnlVkGX", "nombre": "Sofía", "descripcion": "Matilda · estadounidense · educativa"},
  "avatar_lucia": {"id": "k6aNMn2EN3T8vpJSBhQw", "nombre": "Lucía", "descripcion": "Patty · inglés con acento mexicano suave"},
  "avatar_clara": {"id": "Xb7hH8MSUJpSbSDYk0k2", "nombre": "Clara", "descripcion": "Alice · británica · educativa"},
  "avatar_mei": {"id": "c3xntgIY160tGkH7rVz2", "nombre": "Mei", "descripcion": "June · inglés de Hong Kong"},
  "avatar_malik": {"id": "nC4IsZ5gKXknABmkgWvl", "nombre": "Malik", "descripcion": "El Diamond · afroamericano · educativo"},
  "avatar_mateo": {"id": "sKTDlVG8kX7aLD9sGp9s", "nombre": "Mateo", "descripcion": "José · inglés puertorriqueño"},
  "avatar_owen": {"id": "JBFqnCBsd6RMkjVDRZzb", "nombre": "Owen", "descripcion": "George · británico · cálido"},
  "avatar_daniel": {"id": "CwhRBWXzGAHq8TQ4Fs17", "nombre": "Daniel", "descripcion": "Roger · estadounidense · tranquilo"},
  "avatar_kenji": {"id": "2Jg786yPJ6zSdiI0EAAH", "nombre": "Kenji", "descripcion": "Masaki · inglés con acento japonés"},
  mia: { id: 'EXAVITQu4vr4xnSDxMaL', nombre: 'Sarah', descripcion: 'Tutora amigable: cálida y tranquilizadora' },
  leo: { id: 'TX3LPaxmHKxFdv7VOQHJ', nombre: 'Liam', descripcion: 'Tutor motivador: enérgico y cercano' },
  sofia: { id: 'XrExE9yKIg1WjnnlVkGX', nombre: 'Matilda', descripcion: 'Tutora profesional: clara y experta' },
  max: { id: 'pNInz6obpgDQGcFmaJgB', nombre: 'Adam', descripcion: 'Tutor directo: firme y conciso' },
  narradora: { id: 'Xb7hH8MSUJpSbSDYk0k2', nombre: 'Alice', descripcion: 'Narradora de lecciones y Listening' },
  narrador: { id: 'JBFqnCBsd6RMkjVDRZzb', nombre: 'George', descripcion: 'Narrador de diálogos y Listening' },
};

export const vozDisponible = () => config.elevenApiKey.length > 0;

/** Quita la romanización "(…)" y normaliza espacios: solo se sintetiza el texto nativo. */
export function textoParaVoz(t: string, idioma = 'en') {
  const limpio = t.replace(/\s*\([^)]*\)/g, '').replace(/\s+/g, ' ').trim();
  // En chino y japonés el contenido separa palabras con espacios para los
  // ejercicios; la voz debe leer la frase continua, sin pausas artificiales.
  return idioma === 'zh' || idioma === 'ja' ? limpio.replace(/ /g, '') : limpio;
}

/** Idiomas que Flash/Turbo v2.5 pueden forzar con `language_code` (ISO 639-1). */
const IDIOMAS_FORZABLES = new Set(['en', 'es', 'fr', 'de', 'pt', 'it', 'zh', 'ja', 'ko', 'ru']);

/**
 * Código de idioma para ElevenLabs. Sin él, el modelo adivina el idioma y en
 * textos cortos («あ», «Je», «ciao») pronuncia con acento de la voz (inglés).
 * Solo los modelos v2.5 lo admiten; los demás devolverían error.
 */
export function codigoIdiomaVoz(idioma: string, modelo = config.elevenModelo) {
  return /v2_5/.test(modelo) && IDIOMAS_FORZABLES.has(idioma) ? idioma : undefined;
}

export function cuerpoSintesis(texto: string, idioma: string, modelo = config.elevenModelo) {
  const language_code = codigoIdiomaVoz(idioma, modelo);
  return {
    text: texto, model_id: modelo, ...(language_code ? { language_code } : {}),
    voice_settings: { stability: 0.5, similarity_boost: 0.75, style: 0.2, use_speaker_boost: true },
  };
}

/**
 * Clave de caché. Incluye el idioma: el mismo texto en dos idiomas («no») debe
 * sonar distinto. Inglés conserva la clave anterior para reutilizar su caché,
 * que ya se generó en inglés.
 */
export function hashAudio(texto: string, vozId: string, modelo: string, idioma = 'en') {
  const base = idioma === 'en' ? `${modelo}|${vozId}|${texto}` : `${modelo}|${vozId}|${idioma}|${texto}`;
  return createHash('sha256').update(base).digest('hex').slice(0, 40);
}

const dir = () => path.resolve(config.audioDir);
const enCurso = new Map<string, Promise<Buffer>>();

async function sintetizar(texto: string, vozId: string, idioma: string): Promise<Buffer> {
  const url = `https://api.elevenlabs.io/v1/text-to-speech/${vozId}?output_format=mp3_44100_128`;
  let r!: Response;
  for (let i = 0; i < 3; i++) {
    r = await fetch(url, {
      method: 'POST',
      headers: { 'xi-api-key': config.elevenApiKey, 'content-type': 'application/json' },
      body: JSON.stringify(cuerpoSintesis(texto, idioma)),
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
  const texto = textoParaVoz(p.texto, p.idioma);
  if (!texto) throw new Error('texto_vacio');
  if (texto.length > config.vozMaxCaracteres) throw new Error(`texto_demasiado_largo (${texto.length} > ${config.vozMaxCaracteres})`);
  const rol = VOCES[p.voz ?? ''] ? (p.voz as string) : 'narradora';
  const v = VOCES[rol];
  const hash = hashAudio(texto, v.id, config.elevenModelo, p.idioma);
  const ruta = path.join(dir(), `${hash}.mp3`);

  // 1) Caché en disco + registro de uso.
  try {
    const buffer = await readFile(ruta);
    await query('UPDATE audios SET usos = usos + 1, ultimo_uso = now() WHERE hash = $1', [hash]).catch(() => {});
    return { hash, buffer, cache: true, voz: rol, caracteres: texto.length };
  } catch { /* no existe: generar */ }

  if (!vozDisponible()) throw new Error('voz_no_configurada');

  // 2) Generación con deduplicación de peticiones simultáneas.
  let pendiente = enCurso.get(hash);
  if (!pendiente) {
    pendiente = (async () => {
      await mkdir(dir(), { recursive: true });
      const buffer = await sintetizar(texto, v.id, p.idioma);
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

/** Stream the first generation; only complete audio becomes reusable cache. */
export async function obtenerAudioStream(p: { texto: string; idioma: string; voz?: string }, signal: AbortSignal, onFirst: () => void) {
  const texto = textoParaVoz(p.texto, p.idioma);
  if (!texto || texto.length > config.vozMaxCaracteres) throw new Error('texto_invalido');
  const rol = VOCES[p.voz ?? ''] ? p.voz! : 'narradora';
  const v = VOCES[rol]; const hash = hashAudio(texto, v.id, config.elevenModelo, p.idioma);
  const ruta = path.join(dir(), `${hash}.mp3`);
  try {
    const buffer = await readFile(ruta);
    void query('UPDATE audios SET usos = usos + 1, ultimo_uso = now() WHERE hash = $1', [hash]).catch(() => {});
    return { stream: Readable.from([buffer]), cache: true, hash };
  } catch { /* cache miss */ }
  const pending = enCurso.get(hash);
  if (pending) return { stream: Readable.from([await pending]), cache: true, hash };
  let resolve!: (b: Buffer) => void, reject!: (e: unknown) => void;
  const promise = new Promise<Buffer>((yes, no) => { resolve = yes; reject = no; });
  enCurso.set(hash, promise);
  void promise.catch(() => {}).finally(() => enCurso.delete(hash));
  try {
    const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${v.id}/stream?output_format=mp3_44100_128`, {
      method: 'POST', signal,
      headers: { 'xi-api-key': config.elevenApiKey, 'content-type': 'application/json' },
      body: JSON.stringify(cuerpoSintesis(texto, p.idioma)),
    });
    if (!response.ok || !response.body) throw new Error(`ElevenLabs ${response.status}`);
    const reader = response.body.getReader();
    async function* chunks() {
      const all: Buffer[] = []; let complete = false;
      try {
        while (true) {
          const next = await reader.read();
          if (next.done) break;
          if (!all.length) onFirst();
          const chunk = Buffer.from(next.value); all.push(chunk); yield chunk;
        }
        if (!all.length) throw new Error('audio_vacio');
        const buffer = Buffer.concat(all);
        await mkdir(dir(), { recursive: true });
        const temp = `${ruta}.${process.pid}.part`;
        try { await writeFile(temp, buffer); await rename(temp, ruta); }
        finally { await unlink(temp).catch(() => {}); }
        complete = true; resolve(buffer);
        void query(`INSERT INTO audios (hash, idioma, voz, voz_id, modelo, texto, caracteres, bytes) VALUES ($1,$2,$3,$4,$5,$6,$7,$8) ON CONFLICT (hash) DO UPDATE SET usos = audios.usos + 1, ultimo_uso = now()`,
          [hash, p.idioma, rol, v.id, config.elevenModelo, texto, texto.length, buffer.length]).catch(() => {});
      } catch (e) { reject(e); throw e; }
      finally { if (!complete) reject(new Error('audio_interrumpido')); await reader.cancel().catch(() => {}); reader.releaseLock(); }
    }
    return { stream: Readable.from(chunks()), cache: false, hash };
  } catch (e) { reject(e); throw e; }
}
