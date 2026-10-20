/**
 * Cifras francesas → palabras antes de sintetizar. Con `language_code: fr`,
 * Flash v2.5 lee mal las cifras («74» → 64, «2:45», «8 h 15», «18 000» con
 * espacio fino, «96 €»; medición del 19-10-2026), así que la voz recibe el
 * número escrito.
 *
 * Decisiones: ortografía tradicional (guiones por debajo de cien: «soixante
 * et onze», «quatre-vingts», «deux cent un», «deux mille vingt»); horas «8 h
 * 15», «8h15» y «2:45» → «huit heures quinze», «deux heures quarante-cinq»
 * (forma neutra, sin «moins le quart»); «1er» → «premier», «2e» →
 * «deuxième»; años como cardinal («mille neuf cent quarante-cinq»); precios
 * «2,50 €» → «deux euros cinquante»; teléfonos por pares («zéro six, douze,
 * trente-quatre…»); códigos de 5+ cifras, cifra a cifra; rangos «1950-1960» →
 * «… à …»; «un» pasa a «une» ante los femeninos frecuentes («vingt et une
 * heures», «une fois»).
 */
import { A, D, re, fueraDeUrls, telefonos, codigos, unirMiles, restoCifras, siguientePalabra, leerDecimales, cifraACifra } from './numeros_comun.js';

const CHIFFRES = ['zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf'] as const;
const JUSQUA19 = [...CHIFFRES, 'dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf'];
const DIZAINES = ['', '', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante', 'quatre-vingt', 'quatre-vingt'];
const MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];

/** Femeninos frecuentes tras una cifra: «une heure», «vingt et une personnes». */
const FEMININS = new Set(['heure', 'heures', 'fois', 'semaine', 'semaines', 'personne', 'personnes', 'année', 'années', 'page', 'pages', 'minute',
  'minutes', 'seconde', 'secondes', 'nuit', 'nuits', 'journée', 'journées', 'chambre', 'chambres', 'place', 'places', 'étoile', 'étoiles',
  'fille', 'filles', 'femme', 'femmes', 'classe', 'classes', 'table', 'tables', 'pièce', 'pièces', 'voiture', 'voitures', 'lettre', 'lettres',
  'question', 'questions', 'phrase', 'phrases', 'ligne', 'lignes', 'étape', 'étapes', 'partie', 'parties', 'raison', 'raisons', 'salle', 'salles',
  'rue', 'rues', 'règle', 'règles', 'tasse', 'tasses', 'bouteille', 'bouteilles', 'idée', 'idées', 'langue', 'langues', 'leçon', 'leçons']);

function jusqua99(n: number, fem = false): string {
  const un = fem ? 'une' : 'un';
  if (n === 1) return un;
  if (n < 20) return JUSQUA19[n];
  const d = Math.floor(n / 10), u = n % 10;
  if (d === 7 || d === 9) return `${DIZAINES[d]}${d === 7 && u === 1 ? ' et ' : '-'}${JUSQUA19[10 + u]}`;
  if (u === 0) return d === 8 ? 'quatre-vingts' : DIZAINES[d];
  if (u === 1 && d !== 8) return `${DIZAINES[d]} et ${un}`;
  return `${DIZAINES[d]}-${u === 1 ? un : CHIFFRES[u]}`;
}

/** `final`: «cents»/«quatre-vingts» llevan s solo al final del número. */
function jusqua999(n: number, fem = false, final = true): string {
  const c = Math.floor(n / 100), r = n % 100;
  const cent = c === 0 ? '' : c === 1 ? 'cent' : `${CHIFFRES[c]} cent${r === 0 && final ? 's' : ''}`;
  let reste = r ? jusqua99(r, fem) : '';
  if (!final && r === 80) reste = 'quatre-vingt';
  return [cent, reste].filter(Boolean).join(' ') || 'zéro';
}

/** Cardinal: 71 → soixante et onze ; 80 000 → quatre-vingt mille ; 2020 → deux mille vingt. */
export function cardinalFr(n: number, fem = false): string {
  if (!Number.isSafeInteger(n) || n < 0) return String(n);
  if (n < 1000) return jusqua999(n, fem);
  if (n < 1_000_000) {
    const m = Math.floor(n / 1000), r = n % 1000;
    return [m === 1 ? 'mille' : `${jusqua999(m, false, false)} mille`, r ? jusqua999(r, fem) : ''].filter(Boolean).join(' ');
  }
  const mi = Math.floor(n / 1_000_000), r = n % 1_000_000;
  return [mi === 1 ? 'un million' : `${cardinalFr(mi)} millions`, r ? cardinalFr(r, fem) : ''].filter(Boolean).join(' ');
}

/** Ordinal: 1 → premier/première; 2 → deuxième; 5 → cinquième; 9 → neuvième; 21 → vingt et unième. */
export function ordinalFr(n: number, fem = false): string {
  if (n === 1) return fem ? 'première' : 'premier';
  const c = cardinalFr(n);
  if (c.endsWith('cinq')) return `${c}uième`;
  if (c.endsWith('neuf')) return `${c.slice(0, -1)}vième`;
  if (c.endsWith('s') && /(cents|vingts)$/.test(c)) return `${c.slice(0, -1)}ième`;
  if (c.endsWith('e')) return `${c.slice(0, -1)}ième`;
  return `${c}ième`;
}

const femininAvant = (resto: string) => FEMININS.has(siguientePalabra(resto));

/** Teléfono por pares: «06» → zéro six; «12» → douze; «0622335567» → zéro six, vingt-deux… */
function paire(g: string): string {
  if (g.length > 2 && g.length % 2 === 0) return (g.match(/\d\d/g) ?? []).map(paire).join(', ');
  if (g.length !== 2) return cifraACifra(g, CHIFFRES);
  return g.startsWith('0') ? `zéro ${CHIFFRES[Number(g[1])]}` : cardinalFr(Number(g));
}

/** Normaliza un texto francés para la voz. */
export function numerosEnPalabrasFr(texto: string): string {
  return fueraDeUrls(texto, convertir);
}

const heures = (h: number) => `${cardinalFr(h, true)} ${h > 1 ? 'heures' : 'heure'}`;

function convertir(texto: string): string {
  let t = texto.replace(/\b[Nn]°\s*(?=\d)/gu, 'numéro ');
  t = telefonos(t, paire);
  t = codigos(t, CHIFFRES, /^\s*(euros?|€|dollars?|\$|%|personnes)/u);
  t = t
    .replace(/€\s?(\d+(?:[\u00a0\u202f ]\d{3})*(?:[.,]\d+)?)/gu, '$1 €')
    .replace(/\$\s?(\d+(?:[\u00a0\u202f ]\d{3})*(?:[.,]\d+)?)/gu, '$1 $');
  t = unirMiles(t, 'espacio');
  t = t
    .replace(/(\d)[\s\u00a0\u202f]?€/gu, '$1 euros')
    .replace(/(\d)[\s\u00a0\u202f]?\$/gu, '$1 dollars')
    .replace(/(^|[\s(:])[−-](?=\d)/gu, '$1moins ')
    .replace(/(\d)[\s\u00a0\u202f]?%/gu, '$1 pour cent')
    .replace(/(\d)[\s\u00a0\u202f]?°(?:\s?C\b)?/gu, '$1 degrés')
    .replace(re(`(\\d)[\\s\\u00a0\\u202f]?km/h${D}`), '$1 kilomètres heure')
    .replace(re(`(\\d)[\\s\\u00a0\\u202f]?(km|kg|g|ml|min)${D}`), (_m, d: string, u: string) =>
      `${d} ${{ km: 'kilomètres', kg: 'kilos', g: 'grammes', ml: 'millilitres', min: 'minutes' }[u]}`);
  // Hora: 8 h 15, 8h15, 8 h, 2:45 → huit heures quinze, deux heures quarante-cinq.
  t = t.replace(re(`${A}(\\d{1,2})(?:[\\s\\u00a0\\u202f]?h(?:[\\s\\u00a0\\u202f]?(\\d{2}))?|:(\\d{2}))${D}`), (m, h: string, mh?: string, mc?: string) => {
    const hh = Number(h), mm = Number(mh ?? mc ?? '0');
    if (hh > 24 || mm > 59) return m;
    return mm ? `${heures(hh)} ${cardinalFr(mm, true)}` : heures(hh);
  });
  // Ordinales: 1er, 1re, 1ère → premier, première; 2e, 2ème, 2nd → deuxième.
  t = t.replace(re(`${A}(\\d+)(er|re|ère|e|ème|è|nd|nde)${D}`), (_m, d: string, suf: string) =>
    ordinalFr(Number(d), suf === 're' || suf === 'ère'));
  // Fechas: 12/03 → douze mars.
  t = t.replace(re(`${A}(\\d{1,2})/(\\d{1,2})(?:/(\\d{4}))?${D}`), (m, d: string, mo: string, an?: string) => {
    const jour = Number(d), mois = Number(mo);
    if (!jour || jour > 31 || !mois || mois > 12) return m;
    return `${jour === 1 ? 'premier' : cardinalFr(jour)} ${MOIS[mois - 1]}${an ? ` ${cardinalFr(Number(an))}` : ''}`;
  });
  // Importe con céntimos: 2,50 euros → deux euros cinquante.
  t = t.replace(re(`${A}(\\d+)[,.](\\d{2})\\s+(euros?|dollars?)${D}`), (_m, e: string, c: string, mon: string) => {
    const entier = Number(e), cent = Number(c);
    const unite = mon.replace(/s$/, '');
    if (!entier) return `${cardinalFr(cent)} ${unite === 'euro' ? 'centimes' : 'cents'}`;
    const base = `${cardinalFr(entier)} ${entier > 1 ? `${unite}s` : unite}`;
    return cent ? `${base} ${cardinalFr(cent)}` : base;
  });
  // Decimales: 4,8 y 1.5 → quatre virgule huit, un virgule cinq (con punto y 3+ cifras, «point»).
  t = t.replace(re(`${A}(\\d+)([,.])(\\d+)${D}`), (_m, e: string, sep: string, d: string) =>
    `${cardinalFr(Number(e))} ${sep === ',' || d.length <= 2 ? 'virgule' : 'point'} ${leerDecimales(d, (n) => cardinalFr(n), CHIFFRES)}`);
  // Rangos: 1950-1960 → mille neuf cent cinquante à mille neuf cent soixante.
  t = t.replace(re(`${A}(\\d+)(?:\\s?–\\s?|-)(\\d+)${D}`), (_m, a: string, b: string) => `${cardinalFr(Number(a))} à ${cardinalFr(Number(b))}`);
  t = t.replace(/(\d)\s*\+\s*(?=\d)/gu, '$1 plus ').replace(/(\d)\s*×\s*(?=\d)/gu, '$1 fois ');
  return restoCifras(t, (n, _c, resto) => cardinalFr(n, femininAvant(resto)));
}
