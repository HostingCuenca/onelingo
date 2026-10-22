/** Voz con ElevenLabs. Cada texto se sintetiza UNA vez: se guarda en AUDIO_DIR/<hash>.mp3 y en la tabla `audios`. */
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { mkdir, readFile, writeFile, stat, rename, unlink, link, copyFile, constants } from 'node:fs/promises';
import path from 'node:path';
import { Readable } from 'node:stream';
import { config } from './config.js';
import { query, uno } from './db.js';
import { numerosEnPalabrasDe } from './numeros_de.js';
import { numerosEnPalabrasEs } from './numeros_es.js';
import { numerosEnPalabrasFr } from './numeros_fr.js';
import { numerosEnPalabrasIt } from './numeros_it.js';
import { numerosEnPalabrasPt } from './numeros_pt.js';
import { numerosEnPalabrasRu } from './numeros_ru.js';
import { normalizarParaVoz } from './voz_texto.js';

/**
 * Voces nativas de ElevenLabs, una clave por idioma y locutor. Selección del
 * piloto de voces del 2026-10-19 (síntesis + transcripción de vuelta, CER por
 * voz; ver docs/claude-educacion/DESPLIEGUES.md). Hélène (fr, desactivada por
 * su dueña), Chris (en, tartamudeaba) y Luna (it, inventaba palabras) salieron.
 */
export const VOCES: Record<string, { id: string; nombre: string; descripcion: string }> = {
  en_matilda: { id: 'XrExE9yKIg1WjnnlVkGX', nombre: 'Matilda', descripcion: 'en · narradora · estadounidense, educativa' },
  en_liam: { id: 'TX3LPaxmHKxFdv7VOQHJ', nombre: 'Liam', descripcion: 'en · narrador · estadounidense' },
  en_cassidy: { id: '56AoDkrOh6qfVPDXZ7Pt', nombre: 'Cassidy', descripcion: 'en · mujer B · estadounidense' },
  en_mark: { id: 'UgBBYS2sOqTuMpoF3BR0', nombre: 'Mark', descripcion: 'en · hombre B · estadounidense' },
  en_hope: { id: 'tnSpp4vdxKPjI9w0GnoV', nombre: 'Hope', descripcion: 'en · Lumo · estadounidense, joven' },
  es_isabel: { id: 'rixsIpPlTphvsJd2mI03', nombre: 'Isabel', descripcion: 'es · narradora · mexicana, neutra' },
  es_enrique: { id: 'gbTn1bmCvNgk0QEAVyfM', nombre: 'Enrique', descripcion: 'es · narrador · mexicano' },
  es_marcela: { id: '86V9x9hrQds83qf7zaGn', nombre: 'Marcela', descripcion: 'es · mujer B · colombiana' },
  es_antonio: { id: 'htFfPSZGJwjBv1CL0aMD', nombre: 'Antonio', descripcion: 'es · hombre B · latino' },
  es_daniela: { id: 'ajOR9IDAaubDK5qtLUqQ', nombre: 'Daniela', descripcion: 'es · Lumo · latina, joven' },
  fr_caroline: { id: 'kwhMCf63M8O3rCfnQ3oQ', nombre: 'Caroline', descripcion: 'fr · narradora · estándar, clara' },
  fr_nicolas: { id: 'aQROLel5sQbj1vuIVi6B', nombre: 'Nicolas', descripcion: 'fr · narrador · parisino' },
  fr_lucie: { id: 'YxrwjAKoUKULGd0g8K9Y', nombre: 'Lucie', descripcion: 'fr · mujer B · estándar' },
  fr_marcel: { id: 'kENkNtk0xyzG09WW40xE', nombre: 'Marcel', descripcion: 'fr · hombre B · estándar' },
  fr_adina: { id: 'FvmvwvObRqIHojkEGh5N', nombre: 'Adina', descripcion: 'fr · Lumo · joven' },
  de_petra: { id: 'lzvBSKYbNWDD0a6BaJSK', nombre: 'Petra', descripcion: 'de · narradora · estándar, educativa' },
  de_julius: { id: 'n6JEKnKG5a8I78SoBRry', nombre: 'Julius', descripcion: 'de · narrador · estándar' },
  de_susi: { id: 'v3V1d2rk6528UrLKRuy8', nombre: 'Susi', descripcion: 'de · mujer B · estándar' },
  de_ben: { id: 'aTTiK3YzK3dXETpuDE2h', nombre: 'Ben', descripcion: 'de · hombre B · estándar, joven' },
  de_ela: { id: 'HRIShmNY56JGHVU1vXIt', nombre: 'Ela', descripcion: 'de · Lumo · joven' },
  pt_fernanda: { id: '7iqXtOF3wl3pomwXFY7G', nombre: 'Fernanda', descripcion: 'pt · narradora · brasileña' },
  pt_paulo: { id: 'Qrdut83w0Cr152Yb4Xn3', nombre: 'Paulo', descripcion: 'pt · narrador · brasileño' },
  pt_ana_dias: { id: 'MZxV5lN3cv7hi1376O0m', nombre: 'Ana Dias', descripcion: 'pt · mujer B · brasileña, joven' },
  pt_borges: { id: '9pDzHy2OpOgeXM8SeL0t', nombre: 'Borges', descripcion: 'pt · hombre B · brasileño, joven' },
  pt_roberta: { id: 'RGymW84CSmfVugnA5tvA', nombre: 'Roberta', descripcion: 'pt · Lumo · brasileña, joven' },
  it_sami: { id: 'fQmr8dTaOQq116mo2X7F', nombre: 'Sami', descripcion: 'it · narradora · estándar, pausada' },
  it_carmelo: { id: 'HuK8QKF35exsCh2e7fLT', nombre: 'Carmelo', descripcion: 'it · narrador · estándar' },
  it_anna: { id: '6KQ52XTjdNd1FfUgGmV6', nombre: 'Anna', descripcion: 'it · mujer B · estándar' },
  it_marcotrox: { id: 'W71zT1VwIFFx3mMGH2uZ', nombre: 'MarcoTrox', descripcion: 'it · hombre B · estándar' },
  it_kina: { id: 'Kq9pDHHIMmJsG9PEqOtv', nombre: 'Kina', descripcion: 'it · Lumo · joven' },
  ru_mariia: { id: 'EDpEYNf6XIeKYRzYcx4I', nombre: 'Mariia', descripcion: 'ru · narradora · Moscú, calmada' },
  ru_stanislav: { id: 'ogi2DyUAKJb7CEdqqvlU', nombre: 'Stanislav', descripcion: 'ru · narrador · Moscú (habla rápido)' },
  ru_kari: { id: 'Jbte7ht1CqapnZvc4KpK', nombre: 'Kari', descripcion: 'ru · mujer B · estándar, joven' },
  ru_artem: { id: 'rQOBu7YxCDxGiFdTm28w', nombre: 'Artem Lebedev', descripcion: 'ru · hombre B · estándar' },
  ru_larisa: { id: 'AB9XsbSA4eLG12t2myjN', nombre: 'Larisa Actrisa', descripcion: 'ru · Lumo · joven' },
  ko_jiyoung: { id: 'AW5wrnG1jVizOYY7R1Oo', nombre: 'Jiyoung', descripcion: 'ko · narradora · Seúl, cálida' },
  ko_chris: { id: 'PDoCXqBQFGsvfO0hNkEs', nombre: 'Chris', descripcion: 'ko · narrador · Seúl' },
  ko_anna_kim: { id: 'uyVNoMrnUku1dZyVEXwD', nombre: 'Anna Kim', descripcion: 'ko · mujer B · Seúl' },
  ko_yohan_koo: { id: '4JJwo477JUAx3HV0T7n7', nombre: 'Yohan Koo', descripcion: 'ko · hombre B · Seúl' },
  ko_han: { id: '8jHHF8rMqMlg8if2mOUe', nombre: 'Han', descripcion: 'ko · Lumo · joven' },
  ja_kyoko: { id: '4lOQ7A2l7HPuG7UIHiKA', nombre: 'Kyoko', descripcion: 'ja · narradora · Kantō, calmada' },
  ja_hinata: { id: 'j210dv0vWm7fCknyQpbA', nombre: 'Hinata', descripcion: 'ja · narrador · estándar' },
  ja_shizuka: { id: 'WQz3clzUdMqvBf0jswZQ', nombre: 'Shizuka', descripcion: 'ja · mujer B · estándar' },
  ja_kenzo: { id: 'b34JylakFZPlGS0BnwyY', nombre: 'Kenzo', descripcion: 'ja · hombre B · estándar' },
  ja_kuon: { id: 'B8gJV1IhpuegLxdpXFOE', nombre: 'Kuon', descripcion: 'ja · Lumo · joven' },
  zh_shanshan: { id: 'ByhETIclHirOlWnWKhHc', nombre: 'Shan Shan', descripcion: 'zh · narradora · mandarín de Pekín' },
  zh_evan: { id: 'MI36FIkp9wRP7cpWKPTl', nombre: 'Evan', descripcion: 'zh · narrador · mandarín de Pekín' },
  zh_yating: { id: '5eoK8NqMBsMdqUmImHNs', nombre: 'Yating Lin', descripcion: 'zh · mujer B · mandarín' },
  zh_xinghe: { id: 'lt7GBaCoAHWbT7JSZ5Xs', nombre: 'Xinghe Jiang', descripcion: 'zh · hombre B · mandarín estándar' },
  zh_macy: { id: 'NchRhc5KPgHwZagz6MrZ', nombre: 'Macy', descripcion: 'zh · Lumo · joven' },
};

/** Roles de voz. Cada idioma tiene una voz nativa para cada uno. */
export const ROLES = ['narradora', 'narrador', 'mujer_b', 'hombre_b', 'lumo'] as const;
export type Rol = (typeof ROLES)[number];

/** Voz nativa por idioma y rol (claves de VOCES). */
export const NATIVAS: Record<string, Record<Rol, string>> = {
  en: { narradora: 'en_matilda', narrador: 'en_liam', mujer_b: 'en_cassidy', hombre_b: 'en_mark', lumo: 'en_hope' },
  es: { narradora: 'es_isabel', narrador: 'es_enrique', mujer_b: 'es_marcela', hombre_b: 'es_antonio', lumo: 'es_daniela' },
  fr: { narradora: 'fr_caroline', narrador: 'fr_nicolas', mujer_b: 'fr_lucie', hombre_b: 'fr_marcel', lumo: 'fr_adina' },
  de: { narradora: 'de_petra', narrador: 'de_julius', mujer_b: 'de_susi', hombre_b: 'de_ben', lumo: 'de_ela' },
  pt: { narradora: 'pt_fernanda', narrador: 'pt_paulo', mujer_b: 'pt_ana_dias', hombre_b: 'pt_borges', lumo: 'pt_roberta' },
  it: { narradora: 'it_sami', narrador: 'it_carmelo', mujer_b: 'it_anna', hombre_b: 'it_marcotrox', lumo: 'it_kina' },
  ru: { narradora: 'ru_mariia', narrador: 'ru_stanislav', mujer_b: 'ru_kari', hombre_b: 'ru_artem', lumo: 'ru_larisa' },
  ko: { narradora: 'ko_jiyoung', narrador: 'ko_chris', mujer_b: 'ko_anna_kim', hombre_b: 'ko_yohan_koo', lumo: 'ko_han' },
  ja: { narradora: 'ja_kyoko', narrador: 'ja_hinata', mujer_b: 'ja_shizuka', hombre_b: 'ja_kenzo', lumo: 'ja_kuon' },
  zh: { narradora: 'zh_shanshan', narrador: 'zh_evan', mujer_b: 'zh_yating', hombre_b: 'zh_xinghe', lumo: 'zh_macy' },
};

/**
 * Lo que manda el cliente → rol. Tutores del chat (`providers.dart`) y avatares
 * de la videollamada (`web/avatar/roster.json`, por su `gender`; un test vigila
 * que coincidan). La apariencia no fija la voz: la pone el idioma practicado.
 */
const ALIAS: Record<string, Rol> = {
  mia: 'mujer_b', sofia: 'mujer_b', leo: 'hombre_b', max: 'hombre_b',
  avatar_lumo: 'lumo',
  avatar_ana: 'mujer_b', avatar_amara: 'mujer_b', avatar_sofia: 'mujer_b', avatar_lucia: 'mujer_b', avatar_clara: 'mujer_b', avatar_mei: 'mujer_b',
  avatar_malik: 'hombre_b', avatar_mateo: 'hombre_b', avatar_owen: 'hombre_b', avatar_daniel: 'hombre_b', avatar_kenji: 'hombre_b',
};

/** Rol pedido (rol, tutor o avatar); lo desconocido es la narradora. */
export function rolPedido(voz: string | undefined): Rol {
  const v = voz ?? '';
  return (ROLES as readonly string[]).includes(v) ? (v as Rol) : ALIAS[v] ?? 'narradora';
}

/**
 * Voz efectiva (clave de VOCES). El idioma es el del contenido: en el chat, el
 * tutor y la videollamada, el que se practica. Una clave de VOCES se acepta tal
 * cual (pruebas del panel). Un idioma sin voces usa las de inglés.
 */
export function rolDeVoz(voz: string | undefined, idioma: string): string {
  if (voz && VOCES[voz]) return voz;
  return (NATIVAS[idioma] ?? NATIVAS.en)[rolPedido(voz)];
}

export const vozDisponible = () => config.elevenApiKey.length > 0;

/** Conversor de cifras → palabras por idioma (solo donde la voz las lee mal). */
const CIFRAS_EN_PALABRAS: Record<string, (t: string) => string> = {
  de: numerosEnPalabrasDe, fr: numerosEnPalabrasFr, es: numerosEnPalabrasEs,
  pt: numerosEnPalabrasPt, it: numerosEnPalabrasIt, ru: numerosEnPalabrasRu,
};

/**
 * Quita la romanización "(…)" y la notación de la vista (ver voz_texto.ts):
 * solo se sintetiza lo que se pronuncia. `modo: 'letra'` lee nombres de letras.
 */
/**
 * Lecturas de kanji sueltos y jukujikun (tools/voz/lecturas_ja.py): sin contexto
 * la voz elige una lectura cualquiera (星 salió «ほしい»), así que se le pasa la
 * lectura en kana que enseña el curso.
 */
const LECTURAS_JA: Record<string, string> = (() => {
  const url = new URL('./lecturas_ja.json', import.meta.url);
  return existsSync(url) ? JSON.parse(readFileSync(url, 'utf8')) : {};
})();
const KANA = /^[\u3041-\u309f\u30a0-\u30ffー]+$/u;

/** Japonés: palabra corta con kanji → su lectura («星 (ほし)», «星» → «ほし»). */
function lecturaJa(t: string): string | undefined {
  const m = t.match(/^\s*([^\s()]+)\s*(?:\(([^)]*)\))?/u);
  if (!m || t.slice(m[0].length).replace(/\([^)]*\)/g, '').trim()) return undefined;
  const base = m[1].replace(/[。、！？!?.]+$/u, '');
  if (!LECTURAS_JA[base]) return undefined;
  const dada = m[2]?.split(/[,、;；]/)[0].trim();
  return dada && KANA.test(dada) ? dada : LECTURAS_JA[base];
}

export function textoParaVoz(t: string, idioma = 'en', modo?: string) {
  const lectura = idioma === 'ja' && !modo ? lecturaJa(t) : undefined;
  if (lectura) t = lectura;
  const nativo = t.replace(/\s*\([^)]*\)/g, '').replace(/\s+/g, ' ').trim();
  const limpio = normalizarParaVoz(nativo, idioma, modo);
  // En chino y japonés el contenido separa palabras con espacios para los
  // ejercicios; la voz debe leer la frase continua, sin pausas artificiales.
  // La coma que separa alternativas pasa a la de su escritura.
  if (idioma === 'zh') return limpio.replace(/, ?/g, '，').replace(/ /g, '');
  if (idioma === 'ja') return limpio.replace(/, ?/g, '、').replace(/ /g, '');
  // Las cifras se pasan escritas: Flash v2.5 las lee mal en de, fr, es, pt, it
  // y ru (ver numeros_<idioma>.ts). En inglés, coreano, japonés y chino las lee
  // bien y se quedan como están.
  const conversor = CIFRAS_EN_PALABRAS[idioma];
  return conversor ? conversor(limpio) : limpio;
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

/**
 * Ajustes de síntesis. style 0 (antes 0.2): más estable y con menos latencia,
 * según la documentación de ElevenLabs y el piloto del 2026-10-19. Forman parte
 * de la clave de caché: si cambian, se genera audio nuevo en vez de servir el viejo.
 */
export type AjustesVoz = { stability: number; similarity_boost: number; style: number; use_speaker_boost: boolean; speed?: number };
export const AJUSTES_VOZ: AjustesVoz = { stability: 0.5, similarity_boost: 0.75, style: 0, use_speaker_boost: true };
/** Ajustes propios de algunas voces: Stanislav (ru) habla rápido para alumnos (piloto: 17,4 car./s). */
const AJUSTES_POR_VOZ: Record<string, Partial<AjustesVoz>> = { ru_stanislav: { speed: 0.9 } };
export const ajustesDeVoz = (clave: string): AjustesVoz => ({ ...AJUSTES_VOZ, ...AJUSTES_POR_VOZ[clave] });

/**
 * Cuerpo de /v1/text-to-speech. `previo` va como `previous_text` (la frase
 * anterior): orienta la entonación de una respuesta dicha frase a frase.
 */
export function cuerpoSintesis(texto: string, idioma: string, modelo = config.elevenModelo, previo?: string, ajustes: AjustesVoz = AJUSTES_VOZ) {
  const language_code = codigoIdiomaVoz(idioma, modelo);
  return {
    text: texto, model_id: modelo, ...(language_code ? { language_code } : {}),
    ...(previo ? { previous_text: previo } : {}),
    voice_settings: { ...ajustes },
  };
}

const sha = (s: string) => createHash('sha256').update(s).digest('hex').slice(0, 40);
const claveAjustes = (a: AjustesVoz) =>
  `s${a.stability}|b${a.similarity_boost}|st${a.style}|sb${a.use_speaker_boost ? 1 : 0}${a.speed === undefined ? '' : `|v${a.speed}`}`;

/**
 * Clave de caché (versión 2): modelo + voz + idioma + ajustes + texto. Mismo
 * texto, misma voz y mismos ajustes = mismo hash, así que se reutiliza. Cambiar
 * la voz de un rol o los ajustes cambia el hash. `previous_text` no entra: solo
 * orienta la entonación y la frase se reutiliza igual en otro contexto.
 */
export function hashAudio(texto: string, vozId: string, modelo: string, idioma = 'en', ajustes: AjustesVoz = AJUSTES_VOZ) {
  return sha(`v2|${modelo}|${vozId}|${idioma}|${claveAjustes(ajustes)}|${texto}`);
}

/**
 * Clave anterior (v1: modelo|vozId|idioma|texto, sin ajustes; inglés sin
 * idioma). Con ella está todo lo generado antes de la v2, incluidos los cortos
 * pregenerados y verificados (tools/voz/pregenerar_cortos.py). Se consulta como
 * respaldo para no gastar créditos: incluye la voz, así que solo sirve audio de
 * la MISMA voz (con los ajustes de entonces: style 0.2, sin speed).
 */
export function hashAudioLegado(texto: string, vozId: string, modelo: string, idioma = 'en') {
  return sha(idioma === 'en' ? `${modelo}|${vozId}|${texto}` : `${modelo}|${vozId}|${idioma}|${texto}`);
}

const CJK = /[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Hangul}]/u;
/** Letra, sílaba o palabra de 1–2 letras: lo que cubre la pregeneración de cortos. */
export function esAudioCorto(original: string, normalizado: string, modo?: string) {
  const letras = normalizado.replace(/[\s\p{P}]/gu, '');
  if (!letras) return false;
  if (modo) return [...original.replace(/[\s\p{P}]/gu, '')].length <= 1;
  return [...letras].length <= (CJK.test(letras) ? 1 : 2);
}

/** Frases: cortes tras . ! ? … seguidos de espacio (o final) y tras 。！？. */
function frases(t: string): string[] {
  const cs = [...t], out: string[] = [];
  const cierre = (c?: string) => c !== undefined && /[»"”'’)\]」』]/u.test(c);
  let actual = '';
  for (let i = 0; i < cs.length; i++) {
    actual += cs[i];
    if (/[。！？]/u.test(cs[i])) {
      while (i + 1 < cs.length && (/[。！？]/u.test(cs[i + 1]) || cierre(cs[i + 1]))) actual += cs[++i];
      out.push(actual); actual = '';
    } else if (/[.!?…]/u.test(cs[i])) {
      let j = i, extra = '';
      while (j + 1 < cs.length && (/[.!?…]/u.test(cs[j + 1]) || cierre(cs[j + 1]))) extra += cs[++j];
      if (j + 1 >= cs.length || /\s/u.test(cs[j + 1])) {
        actual += extra; i = j;
        while (i + 1 < cs.length && /\s/u.test(cs[i + 1])) actual += cs[++i];
        out.push(actual); actual = '';
      }
    }
  }
  if (actual) out.push(actual);
  return out;
}
const cortarTras = (re: RegExp) => (t: string) => {
  const out: string[] = []; let a = '';
  for (const c of t) { a += c; if (re.test(c)) { out.push(a); a = ''; } }
  if (a) out.push(a);
  return out;
};
/** Si una frase no cabe: por cláusulas, luego por palabras y, al final, a cuchillo. */
const CORTES = [cortarTras(/[,;:，、；：]/u), cortarTras(/\s/u)];

/**
 * Divide un texto largo en trozos de como mucho `max` caracteres, juntando
 * frases enteras (respeta 。！？ y .!?). Un texto que cabe sale tal cual.
 */
export function trocearTexto(texto: string, max: number): string[] {
  if (texto.length <= max) return [texto];
  const trozos: string[] = [];
  let actual = '';
  const cerrar = () => { const t = actual.trim(); if (t) trozos.push(t); actual = ''; };
  const meter = (pieza: string, nivel: number): void => {
    if ((actual + pieza).trim().length <= max) { actual += pieza; return; }
    cerrar();
    if (pieza.trim().length <= max) { actual = pieza; return; }
    if (nivel < CORTES.length) { for (const p of CORTES[nivel](pieza)) meter(p, nivel + 1); return; }
    const cs = [...pieza.trim()];
    for (let i = 0; i < cs.length; i += max) { actual = cs.slice(i, i + max).join(''); if (i + max < cs.length) cerrar(); }
  };
  for (const f of frases(texto)) meter(f, 0);
  cerrar();
  return trozos;
}

/** Como mucho, tantos trozos por petición (protege la cuota mensual). */
export const VOZ_MAX_TROZOS = 6;
export const vozMaxTotal = () => config.vozMaxCaracteres * VOZ_MAX_TROZOS;

const dir = () => path.resolve(config.audioDir);
const enCurso = new Map<string, Promise<Buffer>>();

async function sintetizar(texto: string, vozId: string, idioma: string, previo?: string, ajustes = AJUSTES_VOZ): Promise<Buffer> {
  const url = `https://api.elevenlabs.io/v1/text-to-speech/${vozId}?output_format=mp3_44100_128`;
  let r!: Response;
  for (let i = 0; i < 3; i++) {
    r = await fetch(url, {
      method: 'POST',
      headers: { 'xi-api-key': config.elevenApiKey, 'content-type': 'application/json' },
      body: JSON.stringify(cuerpoSintesis(texto, idioma, config.elevenModelo, previo, ajustes)),
    });
    if (r.ok) return Buffer.from(await r.arrayBuffer());
    if ((r.status === 429 || r.status >= 500) && i < 2) { await new Promise((res) => setTimeout(res, 1000 * (i + 1))); continue; }
    break;
  }
  const detalle = await r.text().catch(() => '');
  throw new Error(`ElevenLabs ${r.status}: ${detalle.slice(0, 200)}`);
}

export type Audio = { hash: string; buffer: Buffer; cache: boolean; voz: string; caracteres: number };
export type PeticionVoz = { texto: string; idioma: string; voz?: string; modo?: string; previo?: string };
type Trozo = { texto: string; hash: string; legado: string; previo?: string };

/** Normaliza, elige la voz y divide en trozos con su clave de caché. */
function preparar(p: PeticionVoz) {
  const texto = textoParaVoz(p.texto, p.idioma, p.modo);
  if (!texto) throw new Error('texto_vacio');
  const partes = trocearTexto(texto, config.vozMaxCaracteres);
  if (partes.length > VOZ_MAX_TROZOS) throw new Error(`texto_demasiado_largo (${texto.length} > ${vozMaxTotal()})`);
  const rol = rolDeVoz(p.voz, p.idioma);
  const v = VOCES[rol];
  const ajustes = ajustesDeVoz(rol);
  const modelo = config.elevenModelo;
  const previo = p.previo ? textoParaVoz(p.previo, p.idioma).slice(-config.vozMaxCaracteres) || undefined : undefined;
  const trozos: Trozo[] = partes.map((t, i) => ({
    texto: t, hash: hashAudio(t, v.id, modelo, p.idioma, ajustes), legado: hashAudioLegado(t, v.id, modelo, p.idioma),
    previo: i === 0 ? previo : partes[i - 1],
  }));
  return { texto, rol, v, ajustes, trozos };
}

async function leerCache(hashes: (string | undefined)[]) {
  for (const hash of hashes) {
    if (!hash) continue;
    try { return { hash, buffer: await readFile(path.join(dir(), `${hash}.mp3`)) }; } catch { /* siguiente */ }
  }
  return null;
}
/**
 * Caché de un trozo: primero la clave v2; si no está, la legado (misma voz).
 * Un acierto legado se enlaza en disco bajo la v2 (hardlink; si no se puede,
 * copia) y se registra una fila alias en `audios` con 0 caracteres y 0 bytes
 * (no se gastó cuota ni disco), así la siguiente vez acierta directo.
 */
async function buscarTrozo(t: Trozo, idioma: string, rol: string, vozId: string) {
  const hit = await leerCache([t.hash, t.legado]);
  if (!hit || hit.hash === t.hash) return hit;
  void registrarUso(hit.hash);
  const desde = path.join(dir(), `${hit.hash}.mp3`), hasta = path.join(dir(), `${t.hash}.mp3`);
  const enlazado = await link(desde, hasta).then(() => true, (e: NodeJS.ErrnoException) =>
    e.code === 'EEXIST' ? true : copyFile(desde, hasta, constants.COPYFILE_EXCL).then(() => true, () => false));
  if (!enlazado) return hit;
  void query(`INSERT INTO audios (hash, idioma, voz, voz_id, modelo, texto, caracteres, bytes) VALUES ($1,$2,$3,$4,$5,$6,0,0)
         ON CONFLICT (hash) DO NOTHING`, [t.hash, idioma, rol, vozId, config.elevenModelo, t.texto]).catch(() => {});
  return { hash: t.hash, buffer: hit.buffer };
}
const registrarUso = (hash: string) =>
  query('UPDATE audios SET usos = usos + 1, ultimo_uso = now() WHERE hash = $1', [hash]).catch(() => {});
const registrarAudio = (hash: string, idioma: string, rol: string, vozId: string, texto: string, bytes: number) =>
  query(`INSERT INTO audios (hash, idioma, voz, voz_id, modelo, texto, caracteres, bytes) VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
         ON CONFLICT (hash) DO UPDATE SET usos = audios.usos + 1, ultimo_uso = now()`,
    [hash, idioma, rol, vozId, config.elevenModelo, texto, texto.length, bytes]);

/** Un trozo: de la caché (disco + tabla `audios`) o generado una sola vez. */
async function audioTrozo(t: Trozo, idioma: string, rol: string, vozId: string) {
  const hit = await buscarTrozo(t, idioma, rol, vozId);
  if (hit) { await registrarUso(hit.hash); return { ...hit, cache: true }; }
  if (!vozDisponible()) throw new Error('voz_no_configurada');
  // Generación con deduplicación de peticiones simultáneas.
  let pendiente = enCurso.get(t.hash);
  if (!pendiente) {
    pendiente = (async () => {
      await mkdir(dir(), { recursive: true });
      const buffer = await sintetizar(t.texto, vozId, idioma, t.previo, ajustesDeVoz(rol));
      await writeFile(path.join(dir(), `${t.hash}.mp3`), buffer);
      await registrarAudio(t.hash, idioma, rol, vozId, t.texto, buffer.length);
      return buffer;
    })().finally(() => enCurso.delete(t.hash));
    enCurso.set(t.hash, pendiente);
  }
  return { hash: t.hash, buffer: await pendiente, cache: false };
}

/**
 * Devuelve el MP3 de `texto` con la voz del rol `voz`; lo genera solo si no
 * existe. Un texto de más de `vozMaxCaracteres` se divide por frases: cada
 * trozo tiene su caché y los MP3 se unen (el unido se guarda con su propio hash).
 */
export async function obtenerAudio(p: PeticionVoz): Promise<Audio> {
  const q = preparar(p);
  if (q.trozos.length === 1) {
    const a = await audioTrozo(q.trozos[0], p.idioma, q.rol, q.v.id);
    return { hash: a.hash, buffer: a.buffer, cache: a.cache, voz: q.rol, caracteres: q.texto.length };
  }
  const hash = sha(`trozos|${q.trozos.map((t) => t.hash).join('|')}`);
  const unido = await leerCache([hash]);
  if (unido) return { hash, buffer: unido.buffer, cache: true, voz: q.rol, caracteres: q.texto.length };
  const partes: Buffer[] = [];
  let cache = true;
  for (const t of q.trozos) {
    const a = await audioTrozo(t, p.idioma, q.rol, q.v.id);
    partes.push(a.buffer); cache &&= a.cache;
  }
  const buffer = Buffer.concat(partes);
  await mkdir(dir(), { recursive: true }).then(() => writeFile(path.join(dir(), `${hash}.mp3`), buffer)).catch(() => {});
  return { hash, buffer, cache, voz: q.rol, caracteres: q.texto.length };
}

/**
 * Tiempo de cada letra del audio (ElevenLabs «with-timestamps»). La videollamada
 * en vivo mueve la boca del tutor con esto: sílabas reales, no el volumen.
 */
export type Alineacion = { characters: string[]; character_start_times_seconds: number[]; character_end_times_seconds: number[] };
export type AudioAlineado = Audio & { alineacion: Alineacion | null };

async function sintetizarAlineado(texto: string, vozId: string, idioma: string, previo?: string, ajustes = AJUSTES_VOZ) {
  const url = `https://api.elevenlabs.io/v1/text-to-speech/${vozId}/with-timestamps?output_format=mp3_44100_128`;
  let r!: Response;
  for (let i = 0; i < 3; i++) {
    r = await fetch(url, {
      method: 'POST',
      headers: { 'xi-api-key': config.elevenApiKey, 'content-type': 'application/json' },
      body: JSON.stringify(cuerpoSintesis(texto, idioma, config.elevenModelo, previo, ajustes)),
    });
    if (r.ok) {
      const d = await r.json() as { audio_base64?: string; alignment?: Alineacion | null; normalized_alignment?: Alineacion | null };
      if (!d.audio_base64) throw new Error('audio_vacio');
      return { buffer: Buffer.from(d.audio_base64, 'base64'), alineacion: d.alignment ?? d.normalized_alignment ?? null };
    }
    if ((r.status === 429 || r.status >= 500) && i < 2) { await new Promise((res) => setTimeout(res, 1000 * (i + 1))); continue; }
    break;
  }
  const detalle = await r.text().catch(() => '');
  throw new Error(`ElevenLabs ${r.status}: ${detalle.slice(0, 200)}`);
}

const leerAlineacion = (hash: string) =>
  readFile(path.join(dir(), `${hash}.json`), 'utf8').then((t) => JSON.parse(t) as Alineacion, () => null);

/** Une las alineaciones de varios trozos seguidos (cada uno empieza donde acabó el anterior). */
export function unirAlineaciones(partes: (Alineacion | null)[]): Alineacion | null {
  if (!partes.length || partes.some((a) => !a)) return null;
  const out: Alineacion = { characters: [], character_start_times_seconds: [], character_end_times_seconds: [] };
  let desfase = 0;
  for (const a of partes as Alineacion[]) {
    out.characters.push(...a.characters);
    out.character_start_times_seconds.push(...a.character_start_times_seconds.map((t) => +(t + desfase).toFixed(3)));
    out.character_end_times_seconds.push(...a.character_end_times_seconds.map((t) => +(t + desfase).toFixed(3)));
    desfase += a.character_end_times_seconds.at(-1) ?? 0;
  }
  return out;
}

const enCursoAlineado = new Map<string, Promise<{ buffer: Buffer; alineacion: Alineacion | null }>>();
/**
 * Un trozo con su alineación. Si el MP3 ya estaba en caché se reutiliza (no se
 * vuelve a pagar) y la alineación sale de `<hash>.json` si existe; si no, va
 * `null` y el cliente reparte las letras a lo largo del audio.
 */
async function trozoAlineado(t: Trozo, idioma: string, rol: string, vozId: string) {
  const hit = await buscarTrozo(t, idioma, rol, vozId);
  if (hit) { await registrarUso(hit.hash); return { hash: hit.hash, buffer: hit.buffer, alineacion: await leerAlineacion(hit.hash), cache: true }; }
  if (!vozDisponible()) throw new Error('voz_no_configurada');
  let pendiente = enCursoAlineado.get(t.hash);
  if (!pendiente) {
    pendiente = (async () => {
      await mkdir(dir(), { recursive: true });
      const r = await sintetizarAlineado(t.texto, vozId, idioma, t.previo, ajustesDeVoz(rol));
      await writeFile(path.join(dir(), `${t.hash}.mp3`), r.buffer);
      if (r.alineacion) await writeFile(path.join(dir(), `${t.hash}.json`), JSON.stringify(r.alineacion)).catch(() => {});
      await registrarAudio(t.hash, idioma, rol, vozId, t.texto, r.buffer.length);
      return r;
    })().finally(() => enCursoAlineado.delete(t.hash));
    enCursoAlineado.set(t.hash, pendiente);
  }
  const r = await pendiente;
  return { hash: t.hash, buffer: r.buffer, alineacion: r.alineacion, cache: false };
}

/** Como `obtenerAudio`, pero con el tiempo de cada letra (videollamada en vivo). */
export async function obtenerAudioAlineado(p: PeticionVoz): Promise<AudioAlineado> {
  const q = preparar(p);
  const partes = [];
  for (const t of q.trozos) partes.push(await trozoAlineado(t, p.idioma, q.rol, q.v.id));
  const hash = partes.length === 1 ? partes[0].hash : sha(`trozos|${q.trozos.map((t) => t.hash).join('|')}`);
  return {
    hash, voz: q.rol, caracteres: q.texto.length, cache: partes.every((x) => x.cache),
    buffer: partes.length === 1 ? partes[0].buffer : Buffer.concat(partes.map((x) => x.buffer)),
    alineacion: unirAlineaciones(partes.map((x) => x.alineacion)),
  };
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

/**
 * Stream the first generation; only complete audio becomes reusable cache.
 * Un texto largo (varios trozos) se sirve entero desde `obtenerAudio`.
 */
export async function obtenerAudioStream(p: PeticionVoz, signal: AbortSignal, onFirst: () => void) {
  const q = preparar(p);
  if (q.trozos.length > 1) {
    const a = await obtenerAudio(p);
    return { stream: Readable.from([a.buffer]), cache: a.cache, hash: a.hash };
  }
  const t = q.trozos[0], rol = q.rol, v = q.v, hash = t.hash;
  const ruta = path.join(dir(), `${hash}.mp3`);
  const hit = await buscarTrozo(t, p.idioma, rol, v.id);
  if (hit) {
    void registrarUso(hit.hash);
    return { stream: Readable.from([hit.buffer]), cache: true, hash: hit.hash };
  }
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
      body: JSON.stringify(cuerpoSintesis(t.texto, p.idioma, config.elevenModelo, t.previo, q.ajustes)),
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
        void registrarAudio(hash, p.idioma, rol, v.id, t.texto, buffer.length).catch(() => {});
      } catch (e) { reject(e); throw e; }
      finally { if (!complete) reject(new Error('audio_interrumpido')); await reader.cancel().catch(() => {}); reader.releaseLock(); }
    }
    return { stream: Readable.from(chunks()), cache: false, hash };
  } catch (e) { reject(e); throw e; }
}
