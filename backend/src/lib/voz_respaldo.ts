/**
 * Voz de respaldo con OpenAI cuando ElevenLabs falla (cuota agotada, clave
 * inválida, caída). El 10-11-2026 la cuota mensual se agotó y el tutor de la
 * videollamada se quedó mudo: con esto sigue hablando, con otra voz.
 *
 * El audio de respaldo se guarda con su propia clave de caché (nunca bajo la de
 * ElevenLabs): cuando ElevenLabs vuelve, cada texto se genera otra vez con la
 * voz buena del tutor.
 */
import { createHash } from 'node:crypto';
import { mkdir, readFile, rename, unlink, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { config } from './config.js';

const NOMBRE_ES: Record<string, string> = {
  en: 'inglés', es: 'español', fr: 'francés', de: 'alemán', pt: 'portugués', it: 'italiano', zh: 'chino mandarín', ja: 'japonés', ko: 'coreano', ru: 'ruso',
};

/** Voces masculinas del catálogo (por nombre o descripción); el resto, femeninas. */
const MASCULINO = /\b(hombre|narrador|Andre|Erik|Frank|Tomas|Amadou|Anatole|Andrey|Andy|Antonio|Artem|Ben|Borges|Carmelo|Chris|Corrado|Elias|Enrique|Evan|François|Guan|Han|Hyuk|Ishibashi|Jason|Jin|João|Joe|Jon|Julius|Kenzo|Liam|Lorenzo|Lucas|Marcel|Marco\w*|Mark|Maxime|Min-joon|Nicolas|Otani|Otto|Paulo|Peter|Prince|Sami|Sebastian|Stanislav|Taehyung|Timo|Tony|Tristan|VASKO|Victor|Yamato|Yohan|Young|Yuri)\b/;
const FEMENINAS = ['coral', 'nova', 'shimmer', 'sage', 'marin'];
const MASCULINAS = ['ash', 'echo', 'onyx', 'cedar', 'verse'];

/**
 * Cada tutor de la videollamada con su voz de OpenAI propia (no se repite entre
 * ellos): con 5 voces por género elegidas por hash, varios sonaban iguales.
 */
export const VOZ_AVATAR: Record<string, string> = {
  avatar_chloe: 'coral', avatar_hana: 'nova', avatar_julia: 'shimmer', avatar_nora: 'sage', avatar_ana: 'marin', avatar_elena: 'alloy',
  avatar_andre: 'onyx', avatar_erik: 'verse', avatar_frank: 'ash', avatar_tomas: 'cedar', avatar_lucas: 'echo', avatar_diego: 'ballad',
};

/** Voz de OpenAI estable para cada tutor o voz del catálogo, del mismo género. */
export function vozRespaldo(rol: string, nombre: string, descripcion: string) {
  if (VOZ_AVATAR[rol]) return VOZ_AVATAR[rol];
  const lista = MASCULINO.test(`${nombre} ${descripcion}`) ? MASCULINAS : FEMENINAS;
  const n = createHash('sha1').update(rol).digest()[0];
  return lista[n % lista.length];
}

/** Indicaciones de pronunciación: el idioma del texto, como nativo, con tono de profesor. */
export const instruccionesRespaldo = (lengua: string) =>
  lengua.includes('+')
    ? `Habla en ${NOMBRE_ES[lengua.split('+')[0]] ?? lengua} con pronunciación nativa y natural, y di las frases en ${NOMBRE_ES[lengua.split('+')[1]] ?? 'el otro idioma'} con su pronunciación correcta, como un profesor particular cálido y claro, a ritmo tranquilo.`
    : `Habla en ${NOMBRE_ES[lengua] ?? lengua} con pronunciación nativa y natural, como un profesor particular cálido y claro, a ritmo tranquilo.`;

/** ElevenLabs en pausa tras un error de cuota o de clave: no se le vuelve a preguntar en cada frase. */
let pausadoHasta = 0;
export const elevenPausado = () => Date.now() < pausadoHasta;
export function anotarFalloEleven(e: unknown) {
  const m = String(e);
  if (/ElevenLabs 40[12]|quota_exceeded/.test(m)) pausadoHasta = Date.now() + 15 * 60_000;
}
export const reanudarEleven = () => { pausadoHasta = 0; };

export const respaldoDisponible = () => config.openaiApiKey.length > 0;

const enCurso = new Map<string, Promise<Buffer>>();

/**
 * MP3 del texto con la voz de respaldo (caché en disco con clave propia).
 * `procesar` ajusta el volumen antes de guardarlo.
 */
export async function sintetizarRespaldo(texto: string, lengua: string, voz: string, procesar: (b: Buffer) => Promise<Buffer> = async (b) => b): Promise<{ hash: string; buffer: Buffer; cache: boolean }> {
  const modelo = config.openaiModeloVozRespaldo;
  const hash = createHash('sha1').update(`respaldo|${modelo}|${voz}|${lengua}|${texto}`).digest('hex');
  const ruta = path.join(path.resolve(config.audioDir), `${hash}.mp3`);
  const guardado = await readFile(ruta).catch(() => null);
  if (guardado?.length) return { hash, buffer: guardado, cache: true };
  let pendiente = enCurso.get(hash);
  if (!pendiente) {
    pendiente = (async () => {
      const r = await fetch('https://api.openai.com/v1/audio/speech', {
        method: 'POST', signal: AbortSignal.timeout(15_000),
        headers: { authorization: `Bearer ${config.openaiApiKey}`, 'content-type': 'application/json' },
        body: JSON.stringify({ model: modelo, voice: voz, input: texto, instructions: instruccionesRespaldo(lengua), response_format: 'mp3' }),
      });
      if (!r.ok) throw new Error(`OpenAI voz ${r.status}: ${(await r.text().catch(() => '')).slice(0, 200)}`);
      const crudo = Buffer.from(await r.arrayBuffer());
      if (!crudo.length) throw new Error('OpenAI voz: audio vacío');
      const buffer = await procesar(crudo);
      await mkdir(path.dirname(ruta), { recursive: true });
      const temp = `${ruta}.${process.pid}.part`;
      await writeFile(temp, buffer).then(() => rename(temp, ruta)).catch(() => unlink(temp).catch(() => {}));
      return buffer;
    })().finally(() => enCurso.delete(hash));
    enCurso.set(hash, pendiente);
  }
  return { hash, buffer: await pendiente, cache: false };
}
