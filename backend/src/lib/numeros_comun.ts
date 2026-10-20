/**
 * Piezas comunes de los conversores de cifras para la voz (numeros_fr, _es,
 * _pt, _it, _ru). Cada idioma decide su forma hablada; aquí solo están los
 * cortes que son iguales en todos: teléfonos, códigos largos, separador de
 * miles, URLs que no se tocan y el «resto» de cifras sueltas.
 *
 * Una cifra solo se convierte si no va pegada a una letra: A1, B2, CO2, N1,
 * 2D, 1f468 (emoji) o «s1-b-f1» se quedan como están.
 */

/** No pegado a letra ni cifra (por delante / por detrás). */
export const A = '(?<![\\p{L}\\p{N}_])';
export const D = '(?![\\p{L}\\p{N}_])';
export const re = (s: string) => new RegExp(s, 'gu');

/** Aplica `fn` fuera de URLs y correos: ahí las cifras no se pronuncian sueltas. */
export function fueraDeUrls(t: string, fn: (s: string) => string): string {
  return t.split(/((?:https?:\/\/|www\.)\S+|[\w.+-]+@[\w-]+\.[\w.]+)/u).map((p, i) => (i % 2 ? p : fn(p))).join('');
}

/** Cifra a cifra: «099» → «cero nueve nueve». */
export const cifraACifra = (s: string, nombres: readonly string[]) => [...s].map((d) => nombres[Number(d)]).join(' ');

/**
 * Teléfonos: tres o más grupos de 2–4 cifras separados por espacio, punto o
 * guion que empiezan por 0 o por + («06 12 34 56 78», «099 123 456»), o un
 * bloque de 8+ cifras que empieza por 0 («0990000042»). `leerGrupo` decide
 * la forma (pares en francés, cifra a cifra en los demás); los grupos se
 * separan con coma para que la voz haga la pausa.
 */
export function telefonos(t: string, leerGrupo: (g: string) => string): string {
  return t
    .replace(re(`${A}((?:0\\d{1,3}|\\+\\d{1,3})(?:[ .\\-\\u00a0\\u202f]\\d{2,4}){2,})${D}`), (m) => m.split(/[ .\-\u00a0\u202f]/u).map(leerGrupo).join(', '))
    .replace(re(`${A}0\\d{7,}${D}`), (m) => leerGrupo(m));
}

/**
 * Códigos: cinco o más cifras seguidas sin separador (protocolo, expediente,
 * pedido) se leen cifra a cifra, salvo que sigan una moneda o una unidad
 * (`cantidad`): entonces es un importe mal escrito y lo lee el cardinal.
 */
export function codigos(t: string, nombres: readonly string[], cantidad: RegExp): string {
  return t.replace(re(`${A}\\d{5,}${D}`), (m: string, pos: number, s: string) =>
    cantidad.test(s.slice(pos + m.length)) ? m : cifraACifra(m, nombres));
}

/**
 * Quita el separador de miles: «18.000» / «18 000» (espacio, nbsp o espacio
 * fino) → «18000». En idiomas con punto, «1.250,50» → «1250,50».
 */
export function unirMiles(t: string, separador: 'punto' | 'espacio'): string {
  const sep = separador === 'punto' ? '\\.' : '[ \\u00a0\\u202f]';
  return t.replace(re(`(?<![\\p{L}\\p{N}_.,])\\d{1,3}(?:${sep}\\d{3})+(?!\\p{N}${separador === 'punto' ? '|\\.\\d' : ''})`), (m) => m.replace(/[.\u00a0\u202f ]/gu, ''));
}

/** Siguiente palabra tras una cifra (para concordar: «21 años» → veintiún). */
export function siguientePalabra(resto: string): string {
  return /^[\s\u00a0\u202f]+([\p{L}’']+)/u.exec(resto)?.[1]?.toLowerCase() ?? '';
}

/** Cifras sueltas que quedan: `fn(n, cifra, resto del texto, texto anterior)`. */
export function restoCifras(t: string, fn: (n: number, cifra: string, resto: string, antes: string) => string): string {
  return t.replace(re(`${A}\\d+${D}`), (m: string, pos: number, s: string) => fn(Number(m), m, s.slice(pos + m.length), s.slice(0, pos)));
}

/**
 * Tras una palabra que anuncia un código (protocolo, número, pedido…), 4+
 * cifras se leen cifra a cifra: «protocolo 4521» → «quatro cinco dois um».
 */
export function codigosTrasPalabra(t: string, palabras: string, nombres: readonly string[]): string {
  return t.replace(re(`(\\b(?:${palabras})[:\\s]+)(\\d{4,})${D}`), (_m, previa: string, d: string) => previa + cifraACifra(d, nombres));
}

/** Parte decimal: «5» → cinco, «25» → veinticinco; con cero delante o larga, cifra a cifra. */
export function leerDecimales(d: string, cardinal: (n: number) => string, nombres: readonly string[]): string {
  return d.startsWith('0') || d.length > 3 ? cifraACifra(d, nombres) : cardinal(Number(d));
}
