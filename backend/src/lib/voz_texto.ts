/**
 * Texto que recibe la voz. El contenido trae notación para la vista (plurales
 * alemanes «, -e», alternativas «a / b», fórmulas «N + V», huecos «___») y
 * letras sueltas que ElevenLabs lee mal aisladas: una «A» sale muda, «R» en
 * portugués suena «É, hein?» y «馬» pierde el tono (calibración 2026-10-13,
 * síntesis + transcripción de vuelta). Aquí se deja solo lo que se pronuncia.
 */

/** Nombre de cada letra, escrito como se pronuncia en su idioma. */
const NOMBRES: Record<string, Record<string, string>> = {
  // Inglés americano: la voz lee bien la mayúscula con punto («H.» → aitch).
  en: {},
  es: {
    a: 'a', b: 'be', c: 'ce', d: 'de', e: 'e', f: 'efe', g: 'ge', h: 'hache', i: 'i', j: 'jota', k: 'ka',
    l: 'ele', m: 'eme', n: 'ene', ñ: 'eñe', o: 'o', p: 'pe', q: 'cu', r: 'erre', s: 'ese', t: 'te', u: 'u',
    v: 've', w: 'doble ve', x: 'equis', y: 'i griega', z: 'zeta',
  },
  pt: {
    a: 'á', b: 'bê', c: 'cê', d: 'dê', e: 'é', f: 'efe', g: 'gê', h: 'agá', i: 'i', j: 'jota', k: 'cá',
    l: 'ele', m: 'eme', n: 'ene', o: 'ó', p: 'pê', q: 'quê', r: 'erre', s: 'esse', t: 'tê', u: 'u',
    v: 'vê', w: 'dáblio', x: 'xis', y: 'ípsilon', z: 'zê', ç: 'cê cedilha',
  },
  it: {
    a: 'a', b: 'bi', c: 'ci', d: 'di', e: 'e', f: 'effe', g: 'gi', h: 'acca', i: 'i', j: 'i lunga', k: 'cappa',
    l: 'elle', m: 'emme', n: 'enne', o: 'o', p: 'pi', q: 'cu', r: 'erre', s: 'esse', t: 'ti', u: 'u',
    v: 'vu', w: 'doppia vu', x: 'ics', y: 'ipsilon', z: 'zeta',
  },
  fr: {
    a: 'a', b: 'bé', c: 'cé', d: 'dé', e: 'euh', f: 'effe', g: 'gé', h: 'hache', i: 'i', j: 'ji', k: 'ka',
    l: 'elle', m: 'emme', n: 'enne', o: 'o', p: 'pé', q: 'ku', r: 'erre', s: 'esse', t: 'té', u: 'u',
    v: 'vé', w: 'double vé', x: 'ixe', y: 'i grec', z: 'zède', ç: 'cé cédille',
  },
  de: {
    a: 'A', b: 'Be', c: 'Ce', d: 'De', e: 'E', f: 'Eff', g: 'Ge', h: 'Ha', i: 'I', j: 'Jott', k: 'Ka',
    l: 'Ell', m: 'Emm', n: 'Enn', o: 'O', p: 'Pe', q: 'Ku', r: 'Err', s: 'Ess', t: 'Te', u: 'U',
    v: 'Vau', w: 'We', x: 'Ix', y: 'Ypsilon', z: 'Zett', ä: 'Ä', ö: 'Ö', ü: 'Ü', ß: 'Eszett',
  },
  ru: {
    а: 'а', б: 'бэ', в: 'вэ', г: 'гэ', д: 'дэ', е: 'е', ё: 'ё', ж: 'жэ', з: 'зэ', и: 'и', й: 'и краткое',
    к: 'ка', л: 'эль', м: 'эм', н: 'эн', о: 'о', п: 'пэ', р: 'эр', с: 'эс', т: 'тэ', у: 'у', ф: 'эф',
    х: 'ха', ц: 'цэ', ч: 'че', ш: 'ша', щ: 'ща', ъ: 'твёрдый знак', ы: 'ы', ь: 'мягкий знак', э: 'э',
    ю: 'ю', я: 'я',
  },
};

/** Jamo suelto del coreano («ㄴ», «ㅏ»): su nombre; aislado la voz no lo pronuncia. */
const JAMO: Record<string, string> = {
  ㄱ: '기역', ㄴ: '니은', ㄷ: '디귿', ㄹ: '리을', ㅁ: '미음', ㅂ: '비읍', ㅅ: '시옷', ㅇ: '이응', ㅈ: '지읒', ㅊ: '치읓',
  ㅋ: '키읔', ㅌ: '티읕', ㅍ: '피읖', ㅎ: '히읗', ㄲ: '쌍기역', ㄸ: '쌍디귿', ㅃ: '쌍비읍', ㅆ: '쌍시옷', ㅉ: '쌍지읒',
  ㅏ: '아', ㅑ: '야', ㅓ: '어', ㅕ: '여', ㅗ: '오', ㅛ: '요', ㅜ: '우', ㅠ: '유', ㅡ: '으', ㅣ: '이', ㅐ: '애', ㅒ: '얘',
  ㅔ: '에', ㅖ: '예', ㅘ: '와', ㅙ: '왜', ㅚ: '외', ㅝ: '워', ㅞ: '웨', ㅟ: '위', ㅢ: '의',
};

const FIN: Record<string, string> = { ja: '。', zh: '。' };
const fin = (idioma: string) => FIN[idioma] ?? '.';
const LETRA = /^\p{L}$/u;

/**
 * Nombre de una letra para la voz. Sin tabla (ja, ko, zh: kana, hangul,
 * hanzi) la letra ya es la sílaba que se pronuncia.
 */
export function nombreLetra(letra: string, idioma: string): string {
  const tabla = NOMBRES[idioma];
  if (idioma === 'en') return letra.toUpperCase();
  return tabla?.[letra.toLowerCase()] ?? JAMO[letra] ?? letra;
}

/** «C, A, T» o «B V» deletreado: cada letra por su nombre, separadas por comas. */
function deletrear(texto: string, idioma: string): string {
  const partes = texto.split(/[\s,.;·/\-–]+/u).filter(Boolean);
  return partes.map((p) => (p.length === 1 || [...p].length === 1 ? nombreLetra(p, idioma) : p)).join(', ') + fin(idioma);
}

/** Notación de la vista que no se pronuncia. */
function quitarNotacion(t: string, idioma: string): string {
  let s = t
    .replace(/_{2,}/g, '…') // hueco de completar
    .replace(/\s*[·•]\s*/g, ', ')
    // «N + V» se lee como pausa; en ja/zh «ない + ように» es la forma unida («ないように»).
    .replace(/(?<!\d)\s*\+\s*(?!\d)/g, idioma === 'ja' || idioma === 'zh' ? '' : ', ')
    .replace(/(\D?)\s*\/\s*(\D?)/g, (m, a, b) => (/\d/.test(a + b) || (!a && !b) ? m : `${a}, ${b}`)) // alternativas: «와 / 과», no «24/7»
    .replace(/\s*=\s*/g, ': ');
  if (idioma === 'de') s = s.replace(/,\s*[-–]\S*\s*$/u, ''); // «das Medikament, -e»
  // «R$ 5.000» sale «ele 5 imboás»: la moneda va detrás, en palabras.
  if (idioma === 'pt') s = s.replace(/R\$\s*([\d.,]*\d)/g, '$1 reais').replace(/US\$\s*([\d.,]*\d)/g, '$1 dólares');
  if (idioma === 'ja' || idioma === 'zh' || idioma === 'ko') {
    // Comodines de fórmula (N, V, A) y guiones de sufijo («-ㄴ데요»).
    s = s.replace(/(^|[\s,(])[NVA](?![A-Za-z])/g, '$1').replace(/(^|[\s,])-(?=\S)/g, '$1');
    // Glosas en minúscula del apoyo («才 / 就 + hora», «볼 만한 + sustantivo»); las siglas (KTV) se quedan.
    if (/[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Hangul}]/u.test(s)) {
      s = s.replace(/(?<!\p{Script=Latin})(?=\p{Ll})\p{Script=Latin}+(?!\p{Script=Latin})/gu, '');
    }
  }
  return s.replace(/\s+,/g, ',').replace(/,\s*,/g, ',').replace(/^[\s,]+|[\s,]+$/g, '').replace(/\s+/g, ' ');
}

/**
 * `modo: 'letra'` = nombre de letras (Nivel 0: «el nombre de las letras»,
 * «toca la letra que oyes», deletreo). Sin modo, una letra suelta es una
 * palabra («a», «y», «в», «は») y va en minúscula.
 */
export function normalizarParaVoz(texto: string, idioma: string, modo?: string): string {
  if (modo === 'letra') return deletrear(texto.trim(), idioma);
  const s = quitarNotacion(texto, idioma);
  if (!s) return s;
  const letras = s.replace(/[\s\p{P}]/gu, '');
  // Muy corto y sin puntuación final: la voz lo corta o lo lee sin entonación.
  const corto = [...letras].length <= 3 && !/[.!?。！？…]$/u.test(s);
  if (JAMO[letras]) return JAMO[letras] + fin(idioma);
  if (LETRA.test(letras) && idioma !== 'en') return letras.toLowerCase() + fin(idioma);
  return corto ? s + fin(idioma) : s;
}
