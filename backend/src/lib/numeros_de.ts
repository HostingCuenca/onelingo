/**
 * Cifras alemanas → palabras antes de sintetizar. Con `language_code: de`,
 * ElevenLabs Flash lee mal las cifras («1921» → «1991», «2024» → «22»,
 * «437» → «34»; calibración del 06-10-2026), así que la voz recibe el número
 * ya escrito: años como «neunzehnhunderteinundzwanzig», fechas como ordinales
 * («am 15. März» → «am fünfzehnten März») y «§» como «Paragraf».
 */

const UNIDADES = ['null', 'eins', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun',
  'zehn', 'elf', 'zwölf', 'dreizehn', 'vierzehn', 'fünfzehn', 'sechzehn', 'siebzehn', 'achtzehn', 'neunzehn'];
const DECENAS = ['', '', 'zwanzig', 'dreißig', 'vierzig', 'fünfzig', 'sechzig', 'siebzig', 'achtzig', 'neunzig'];
const MESES = 'Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember';
/** Tras estas palabras un número de cuatro cifras es una cantidad, no un año. */
const CANTIDAD = /^\s*(Euro|€|Dollar|\$|Prozent|%|Personen|Menschen|Leute|Meter|Kilometer|km|Kilo|Gramm|Stück|Tage|Tagen|Wörter|Wörtern|Seiten|Mal)\b/;

/** «ein» delante de hundert/tausend/und: einhundert, einundzwanzig. */
function hasta99(n: number): string {
  if (n < 20) return UNIDADES[n];
  const u = n % 10, d = Math.floor(n / 10);
  return u === 0 ? DECENAS[d] : `${u === 1 ? 'ein' : UNIDADES[u]}und${DECENAS[d]}`;
}

function hasta999(n: number): string {
  const c = Math.floor(n / 100), r = n % 100;
  const cien = c === 0 ? '' : `${c === 1 ? 'ein' : UNIDADES[c]}hundert`;
  return r === 0 ? cien || 'null' : cien + hasta99(r);
}

/** Cardinal: 437 → vierhundertsiebenunddreißig; 2024 → zweitausendvierundzwanzig. */
export function cardinalDe(n: number): string {
  if (!Number.isSafeInteger(n) || n < 0) return String(n);
  if (n < 1000) return hasta999(n);
  if (n < 1_000_000) {
    const m = Math.floor(n / 1000), r = n % 1000;
    return `${m === 1 ? 'ein' : hasta999(m)}tausend${r ? hasta999(r) : ''}`;
  }
  const mi = Math.floor(n / 1_000_000), r = n % 1_000_000;
  const millones = mi === 1 ? 'eine Million' : `${cardinalDe(mi)} Millionen`;
  return r ? `${millones} ${cardinalDe(r)}` : millones;
}

/** Año: 1950 → neunzehnhundertfünfzig; 2024 → zweitausendvierundzwanzig. */
export function anioDe(n: number): string {
  if (n >= 1100 && n < 2000) {
    const r = n % 100;
    return `${hasta99(Math.floor(n / 100))}hundert${r ? hasta99(r) : ''}`;
  }
  return cardinalDe(n);
}

/** Ordinal sin desinencia de caso: 1 → erst, 3 → dritt, 15 → fünfzehnt, 20 → zwanzigst. */
function raizOrdinal(n: number): string {
  if (n === 1) return 'erst';
  if (n === 3) return 'dritt';
  if (n === 7) return 'siebt';
  if (n === 8) return 'acht';
  const c = cardinalDe(n);
  return n < 20 ? `${c}t` : `${c}st`;
}

/** Normaliza un texto alemán para la voz: §, fechas, horas, decimales, años y cardinales. */
export function numerosEnPalabrasDe(texto: string): string {
  let t = texto
    .replace(/§§\s*/g, 'Paragrafen ')
    // Genitivo y dativo débiles: «des § 434» → «des Paragrafen».
    .replace(/\b(des|dem|den)\s+§\s*/g, '$1 Paragrafen ')
    .replace(/§\s*/g, 'Paragraf ')
    .replace(/(\d+)\s*%/g, '$1 Prozent')
    .replace(/(\d+)\s*€/g, '$1 Euro')
    // Separador de miles: 1.000 → 1000 (las fechas llevan espacio tras el punto: «15. März»).
    .replace(/\b\d{1,3}(?:\.\d{3})+\b/g, (m) => m.replace(/\./g, ''));
  // Fecha: «am 15. März» → «am fünfzehnten März»; «der 3. Mai» → «der dritte Mai».
  t = t.replace(new RegExp(`(\\b\\w+\\s+)?(\\d{1,2})\\.\\s*(${MESES})\\b`, 'g'), (_m, previa: string | undefined, d: string, mes: string) => {
    const nominativo = /^(der|Der)\s+$/.test(previa ?? '') || !previa;
    return `${previa ?? ''}${raizOrdinal(Number(d))}${nominativo ? 'e' : 'en'} ${mes}`;
  });
  // Hora: 7:15 Uhr → sieben Uhr fünfzehn; 9:00 Uhr → neun Uhr.
  t = t.replace(/\b(\d{1,2}):(\d{2})\s*Uhr\b/g, (_m, h: string, m: string) => {
    const hora = Number(h) === 1 ? 'ein' : cardinalDe(Number(h));
    return Number(m) ? `${hora} Uhr ${cardinalDe(Number(m))}` : `${hora} Uhr`;
  });
  t = t.replace(/\b1\s+Uhr\b/g, 'ein Uhr');
  // Decimal con coma: 3,5 → drei Komma fünf.
  t = t.replace(/\b(\d+),(\d+)\b/g, (_m, e: string, d: string) => `${cardinalDe(Number(e))} Komma ${[...d].map((x) => UNIDADES[Number(x)]).join(' ')}`);
  // Resto de cifras: años de cuatro cifras salvo que sigan unidades; lo demás, cardinal.
  return t.replace(/\b\d+\b/g, (m: string, pos: number, s: string) => {
    const n = Number(m);
    const esAnio = m.length === 4 && n >= 1100 && n < 2100 && !CANTIDAD.test(s.slice(pos + m.length));
    return esAnio ? anioDe(n) : cardinalDe(n);
  });
}
