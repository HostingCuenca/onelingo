/**
 * Cifras italianas → palabras antes de sintetizar. Con `language_code: it`,
 * Flash v2.5 lee mal las cifras con punto de miles («90.000 euro», «400.000
 * euro»; medición del 19-10-2026), así que la voz recibe el número escrito.
 *
 * Decisiones: números juntos como se escriben («milletrecento», «ventuno»,
 * «ventitré», «quattrocentomila»); horas «8:30» → «otto e trenta»; años como
 * cardinal («duemilaventi»); importes «12,50 euro» → «dodici euro e
 * cinquanta»; teléfonos y códigos de 5+ cifras, cifra a cifra; rangos
 * «1930–1939» → «… a …»; «1» ante sustantivo → «un»/«una».
 */
import { A, D, re, fueraDeUrls, telefonos, codigos, unirMiles, restoCifras, siguientePalabra, leerDecimales, cifraACifra } from './numeros_comun.js';

const CIFRE = ['zero', 'uno', 'due', 'tre', 'quattro', 'cinque', 'sei', 'sette', 'otto', 'nove'] as const;
const FINO19 = [...CIFRE, 'dieci', 'undici', 'dodici', 'tredici', 'quattordici', 'quindici', 'sedici', 'diciassette', 'diciotto', 'diciannove'];
const DECINE = ['', '', 'venti', 'trenta', 'quaranta', 'cinquanta', 'sessanta', 'settanta', 'ottanta', 'novanta'];
const ORDINALI = ['', 'primo', 'secondo', 'terzo', 'quarto', 'quinto', 'sesto', 'settimo', 'ottavo', 'nono', 'decimo'];
const MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];

/** Femeninos frecuentes tras «1»: «una volta», «una persona». */
const FEMMINILI = new Set(['ora', 'persona', 'volta', 'settimana', 'pagina', 'parola', 'notte', 'camera', 'stanza', 'tazza', 'bottiglia', 'cosa',
  'parte', 'domanda', 'lezione', 'classe', 'stella', 'via', 'linea', 'fermata', 'casa', 'giornata', 'sera', 'mattina', 'lettera', 'frase']);
/** Tras estas palabras la cifra no va ante sustantivo: «uno di loro», «il 21 e il 22». */
const NON_SOSTANTIVO = new Set(['di', 'del', 'e', 'o', 'a', 'al', 'in', 'è', 'sono', 'si', 'per', 'con', 'che', 'come', 'più', 'meno', 'ma',
  'se', 'non', 'già', 'lo', 'la', 'il', 'le', 'gli', 'da', 'dal', 'su', 'tra', 'fra', 'fino', 'mi', 'ti', 'ci']);

function fino99(n: number): string {
  if (n < 20) return FINO19[n];
  const d = DECINE[Math.floor(n / 10)], u = n % 10;
  if (u === 0) return d;
  if (u === 1 || u === 8) return d.slice(0, -1) + CIFRE[u]; // ventuno, ventotto
  return d + (u === 3 ? 'tré' : CIFRE[u]);
}

function fino999(n: number): string {
  const c = Math.floor(n / 100), r = n % 100;
  const cento = c === 0 ? '' : c === 1 ? 'cento' : `${CIFRE[c]}cento`;
  if (!r) return cento || 'zero';
  const resto = fino99(r);
  // centotto, centottanta: se elide la «o» ante «ott-».
  return cento && resto.startsWith('ott') ? cento.slice(0, -1) + resto : cento + resto;
}

/** Cardinal: 1300 → milletrecento; 21 000 → ventunmila; 400 000 → quattrocentomila. */
export function cardinaleIt(n: number): string {
  if (!Number.isSafeInteger(n) || n < 0) return String(n);
  if (n < 1000) return fino999(n);
  if (n < 1_000_000) {
    const m = Math.floor(n / 1000), r = n % 1000;
    const mila = m === 1 ? 'mille' : `${fino999(m).replace(/uno$/, 'un')}mila`;
    return r ? mila + fino999(r) : mila;
  }
  const mi = Math.floor(n / 1_000_000), r = n % 1_000_000;
  const milioni = mi === 1 ? 'un milione' : `${cardinaleIt(mi)} milioni`;
  return r ? `${milioni} ${cardinaleIt(r)}` : milioni;
}

/** «1» ante sustantivo: un euro, una volta; si no, uno. */
function unoDavanti(resto: string): string {
  const p = siguientePalabra(resto);
  if (!p || NON_SOSTANTIVO.has(p)) return 'uno';
  return FEMMINILI.has(p) ? 'una' : 'un';
}

/** Normaliza un texto italiano para la voz. */
export function numerosEnPalabrasIt(texto: string): string {
  return fueraDeUrls(texto, convertir);
}

function convertir(texto: string): string {
  let t = texto.replace(/\b[Nn]\.?\s?°\s*(?=\d)/gu, 'numero ');
  t = telefonos(t, (g) => cifraACifra(g, CIFRE));
  t = codigos(t, CIFRE, /^\s*(euro|dollari|%|persone)/u);
  t = t
    .replace(/€\s?(\d+(?:[.,]\d+)*)/gu, '$1 euro')
    .replace(/(\d)\s?€/gu, '$1 euro')
    .replace(/\$\s?(\d+(?:[.,]\d+)*)/gu, '$1 dollari');
  t = unirMiles(t, 'punto');
  t = t
    .replace(/(^|[\s(:])[−-](?=\d)/gu, '$1meno ')
    .replace(/(\d)\s?%/gu, '$1 per cento')
    .replace(re(`(\\d)\\s?km/h${D}`), '$1 chilometri orari')
    .replace(re(`(\\d)\\s?(km|kg|g|ml|min)${D}`), (_m, d: string, u: string) =>
      `${d} ${{ km: 'chilometri', kg: 'chili', g: 'grammi', ml: 'millilitri', min: 'minuti' }[u]}`);
  // Hora: 8:30 → otto e trenta; 13:00 → tredici.
  t = t.replace(re(`${A}(\\d{1,2}):(\\d{2})${D}`), (m, h: string, mi: string) => {
    const hh = Number(h), mm = Number(mi);
    if (hh > 24 || mm > 59) return m;
    const ora = hh === 1 ? "l'una" : cardinaleIt(hh);
    return mm ? `${ora} e ${cardinaleIt(mm)}` : ora;
  });
  t = t.replace(/(\d)\s?°(?:\s?C\b)?/gu, '$1 gradi');
  // Ordinales: 1º → primo, 1ª → prima.
  t = t.replace(re(`${A}(\\d{1,2})\\.?(º|ª)(?![\\p{L}\\p{N}])`), (_m, d: string, suf: string) => {
    const n = Number(d);
    if (n < 1 || n > 10) return cardinaleIt(n);
    return suf === 'ª' ? ORDINALI[n].replace(/o$/, 'a') : ORDINALI[n];
  });
  t = t.replace(re(`${A}(\\d{1,2})/(\\d{1,2})(?:/(\\d{4}))?${D}`), (m, d: string, me: string, an?: string) => {
    const g = Number(d), mese = Number(me);
    if (!g || g > 31 || !mese || mese > 12) return m;
    return `${g === 1 ? 'primo' : cardinaleIt(g)} ${MESI[mese - 1]}${an ? ` ${cardinaleIt(Number(an))}` : ''}`;
  });
  // Importe con céntimos: 12,50 euro → dodici euro e cinquanta.
  t = t.replace(re(`${A}(\\d+)[,.](\\d{2})\\s+(euro|dollari)${D}`), (_m, e: string, c: string, val: string) => {
    const intero = Number(e), cent = Number(c);
    if (!intero) return `${cardinaleIt(cent)} centesimi`;
    const base = `${intero === 1 ? 'un' : cardinaleIt(intero)} ${intero === 1 && val === 'dollari' ? 'dollaro' : val}`;
    return cent ? `${base} e ${cardinaleIt(cent)}` : base;
  });
  // Decimales: 4,8 y 1.5 → quattro virgola otto, uno virgola cinque (con punto y 3+ cifras, «punto»).
  t = t.replace(re(`${A}(\\d+)([,.])(\\d+)${D}`), (_m, e: string, sep: string, d: string) =>
    `${cardinaleIt(Number(e))} ${sep === ',' || d.length <= 2 ? 'virgola' : 'punto'} ${leerDecimales(d, cardinaleIt, CIFRE)}`);
  t = t.replace(re(`${A}(\\d+)(?:\\s?–\\s?|-)(\\d+)${D}`), (_m, a: string, b: string) => `${cardinaleIt(Number(a))} a ${cardinaleIt(Number(b))}`);
  t = t.replace(/(\d)\s*\+\s*(?=\d)/gu, '$1 più ').replace(/(\d)\s*×\s*(?=\d)/gu, '$1 per ');
  return restoCifras(t, (n, _c, resto) => (n === 1 ? unoDavanti(resto) : cardinaleIt(n)));
}
