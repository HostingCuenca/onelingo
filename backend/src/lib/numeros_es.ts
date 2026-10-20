/**
 * Cifras españolas → palabras antes de sintetizar (español latino neutro).
 * Con `language_code: es`, Flash v2.5 lee mal las cifras («Unas 60 palabras»
 * → 160, «1.200», «8:15», «82 %»; medición del 19-10-2026), así que la voz
 * recibe el número escrito.
 *
 * Decisiones: horas «8:15» → «ocho y quince» (hasta las 12) y «16:40» →
 * «dieciséis cuarenta» (reloj de 24 h), «9:00» → «nueve»; «el 1 de mayo» →
 * «el primero de mayo» (uso latinoamericano); años como cardinal («dos mil
 * treinta y cinco»); rangos «1930–1939» → «mil novecientos treinta a mil
 * novecientos treinta y nueve»; importes «12,50 dólares» → «doce dólares con
 * cincuenta»; teléfonos y códigos de 5+ cifras (o de 4+ tras «número»,
 * «pedido»…), cifra a cifra; el 911, «nueve once». «uno» se apocopa ante
 * sustantivo («veintiún años», «un dólar», no en años: «en 2031 coordinaba»)
 * y pasa a femenino, igual que las centenas, ante los femeninos frecuentes y
 * -ión/-dad («una hora», «trescientas personas»; «las 340» → trescientas).
 */
import { A, D, re, fueraDeUrls, telefonos, codigos, codigosTrasPalabra, unirMiles, restoCifras, siguientePalabra, leerDecimales, cifraACifra } from './numeros_comun.js';

const DIGITOS = ['cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve'] as const;
const HASTA29 = [...DIGITOS, 'diez', 'once', 'doce', 'trece', 'catorce', 'quince', 'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve',
  'veinte', 'veintiuno', 'veintidós', 'veintitrés', 'veinticuatro', 'veinticinco', 'veintiséis', 'veintisiete', 'veintiocho', 'veintinueve'];
const DECENAS = ['', '', '', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa'];
const CENTENAS = ['', 'ciento', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos', 'seiscientos', 'setecientos', 'ochocientos', 'novecientos'];
const ORDINALES = ['', 'primero', 'segundo', 'tercero', 'cuarto', 'quinto', 'sexto', 'séptimo', 'octavo', 'noveno', 'décimo'];
const MESES = 'enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre';
const NOMBRE_MES = MESES.split('|').filter((m) => m !== 'setiembre');

/** Femeninos frecuentes tras una cifra: «una hora», «veintiuna personas». */
const FEMENINOS = new Set(['hora', 'horas', 'persona', 'personas', 'semana', 'semanas', 'vez', 'veces', 'palabra', 'palabras', 'página', 'páginas',
  'letra', 'letras', 'pregunta', 'preguntas', 'clase', 'clases', 'noche', 'noches', 'mujer', 'mujeres', 'cuadra', 'cuadras', 'habitación',
  'habitaciones', 'plaza', 'plazas', 'mesa', 'mesas', 'cosa', 'cosas', 'parte', 'partes', 'opción', 'opciones', 'razón', 'razones', 'idea', 'ideas',
  'foto', 'fotos', 'taza', 'tazas', 'botella', 'botellas', 'entrada', 'entradas', 'cuota', 'cuotas', 'unidad', 'unidades', 'caja', 'cajas',
  'frase', 'frases', 'línea', 'líneas', 'estrella', 'estrellas', 'calle', 'calles', 'sala', 'salas', 'visita', 'visitas', 'cuenta', 'cuentas',
  'tarea', 'tareas', 'vuelta', 'vueltas', 'aula', 'puerta', 'puertas', 'planta', 'cama', 'camas', 'manzana', 'manzanas', 'fila', 'filas',
  'respuesta', 'respuestas', 'encuesta', 'encuestas', 'empresa', 'empresas', 'tienda', 'tiendas', 'reserva', 'reservas', 'familia', 'familias',
  'escuela', 'escuelas', 'casa', 'casas', 'obra', 'obras', 'firma', 'firmas', 'cuadra', 'llamada', 'llamadas', 'consulta', 'consultas']);
/** Terminaciones femeninas seguras: -ión, -dad, -tud («doscientas habitaciones», «veintiuna ciudades»). */
const TERMINACION_FEMENINA = /(?:ión|iones|dad|dades|tud|tudes)$/u;
/** Tras estas palabras la cifra no va ante sustantivo: «uno de cada tres», «el 21 y el 22». */
const NO_SUSTANTIVO = new Set(['de', 'del', 'y', 'o', 'u', 'a', 'al', 'en', 'es', 'son', 'se', 'por', 'para', 'con', 'que', 'como', 'más', 'menos',
  'ni', 'pero', 'sin', 'si', 'no', 'ya', 'lo', 'la', 'el', 'las', 'los', 'le', 'me', 'te', 'nos', 'hay', 'fue', 'era', 'será', 'está', 'están', 'e',
  'entre', 'hasta', 'desde', 'sobre', 'tras', 'según', 'cuando', 'donde', 'pues', 'también', 'solo', 'sólo', 'dice', 'significa', 'tiene',
  'contra', 'cada', 'esta', 'esa', 'ahora', 'nunca', 'toda', 'todas', 'otra', 'otras', 'mientras', 'apenas', 'fuera', 'sea', 'hacia']);

type Forma = 'uno' | 'un' | 'una';

function hasta99(n: number, forma: Forma = 'uno'): string {
  let s: string;
  if (n < 30) s = HASTA29[n];
  else {
    const u = n % 10;
    s = u === 0 ? DECENAS[Math.floor(n / 10)] : `${DECENAS[Math.floor(n / 10)]} y ${DIGITOS[u]}`;
  }
  if (forma === 'uno' || n % 10 !== 1 || n === 11) return s;
  if (n === 21) return forma === 'un' ? 'veintiún' : 'veintiuna';
  return s.replace(/uno$/, forma);
}

function hasta999(n: number, forma: Forma = 'uno'): string {
  if (n === 100) return 'cien';
  const c = Math.floor(n / 100), r = n % 100;
  // Centenas en femenino ante sustantivo femenino: doscientas personas.
  const centena = forma === 'una' && c > 1 ? CENTENAS[c].replace(/os$/, 'as') : CENTENAS[c];
  return [c ? centena : '', r || !c ? hasta99(r, forma) : ''].filter(Boolean).join(' ');
}

/** Cardinal: 21 → veintiuno; 1500 → mil quinientos; 21000 → veintiún mil. */
export function cardinalEs(n: number, forma: Forma = 'uno'): string {
  if (!Number.isSafeInteger(n) || n < 0) return String(n);
  if (n < 1000) return hasta999(n, forma);
  if (n < 1_000_000) {
    const m = Math.floor(n / 1000), r = n % 1000;
    return [m === 1 ? 'mil' : `${hasta999(m, forma === 'una' ? 'una' : 'un')} mil`, r ? hasta999(r, forma) : ''].filter(Boolean).join(' ');
  }
  const mi = Math.floor(n / 1_000_000), r = n % 1_000_000;
  return [mi === 1 ? 'un millón' : `${cardinalEs(mi, 'un')} millones`, r ? cardinalEs(r, forma) : ''].filter(Boolean).join(' ');
}

/**
 * Forma de «uno» (y de las centenas) según lo que sigue: sustantivo femenino,
 * sustantivo, o nada. Sin sustantivo detrás, «las»/«unas» delante marcan
 * femenino: «las 340» (visitas) → trescientas cuarenta.
 */
function formaAnte(resto: string, antes: string): Forma {
  const p = siguientePalabra(resto);
  if (!p || NO_SUSTANTIVO.has(p)) return /\b(?:las|unas)\s+$/iu.test(antes) ? 'una' : 'uno';
  return FEMENINOS.has(p) || (TERMINACION_FEMENINA.test(p) && !/^(?:avi|cami|gorri)ón/u.test(p)) ? 'una' : 'un';
}

const MONEDA: Record<string, [string, string]> = { dólares: ['dólar', 'dólares'], dólar: ['dólar', 'dólares'], euros: ['euro', 'euros'], euro: ['euro', 'euros'], pesos: ['peso', 'pesos'], soles: ['sol', 'soles'] };

/** Normaliza un texto español para la voz. */
export function numerosEnPalabrasEs(texto: string): string {
  return fueraDeUrls(texto, convertir);
}

function convertir(texto: string): string {
  let t = texto.replace(/\b[Nn]\.?\s?º\s*(?=\d)/gu, 'número ');
  t = telefonos(t, (g) => cifraACifra(g, DIGITOS));
  t = codigosTrasPalabra(t, 'número|código|pedido|expediente|folio|ticket|cédula|contraseña', DIGITOS);
  t = codigos(t, DIGITOS, /^\s*(dólares|euros|pesos|%|personas)/u);
  t = t
    .replace(/(?:US\$|\$)\s?(\d+(?:[.,]\d+)*)/gu, '$1 dólares')
    .replace(/€\s?(\d+(?:[.,]\d+)*)/gu, '$1 euros')
    .replace(/(\d)\s?€/gu, '$1 euros')
    .replace(/(\d)\s?\$/gu, '$1 dólares');
  t = unirMiles(t, 'punto');
  t = t
    .replace(/(^|[\s(:])[−-](?=\d)/gu, '$1menos ')
    .replace(/(\d)\s?%/gu, '$1 por ciento')
    .replace(/(\d)\s?°(?:\s?C\b)?/gu, '$1 grados')
    .replace(re(`(\\d)\\s?km/h${D}`), '$1 kilómetros por hora')
    .replace(re(`(\\d)\\s?(km|kg|g|ml)${D}`), (_m, d: string, u: string) => `${d} ${{ km: 'kilómetros', kg: 'kilos', g: 'gramos', ml: 'mililitros' }[u]}`);
  // Hora: 8:15 → ocho y quince; 16:40 → dieciséis cuarenta; 9:00 → nueve.
  t = t.replace(re(`${A}(\\d{1,2}):(\\d{2})${D}`), (m, h: string, mi: string) => {
    const hh = Number(h), mm = Number(mi);
    if (hh > 24 || mm > 59) return m;
    const hora = cardinalEs(hh, 'una');
    if (!mm) return hora;
    return hh > 12 ? `${hora} ${cardinalEs(mm)}` : `${hora} y ${cardinalEs(mm)}`;
  });
  // Ordinales: 1.º → primero, 3.ª → tercera, 1.er → primer (más allá de 10, cardinal).
  t = t.replace(re(`${A}(\\d{1,2})\\.?(º|ª|er)(?![\\p{L}\\p{N}])`), (m, d: string, suf: string) => {
    const n = Number(d);
    if (n < 1 || n > 10) return `${cardinalEs(n)}`;
    if (suf === 'er') return n === 1 ? 'primer' : n === 3 ? 'tercer' : ORDINALES[n];
    return suf === 'ª' ? ORDINALES[n].replace(/o$/, 'a') : ORDINALES[n];
  });
  // Fechas: «el 1 de mayo» → «el primero de mayo»; «16/05» → «dieciséis de mayo».
  t = t.replace(re(`${A}1(\\s+de\\s+(?:${MESES}))`), 'primero$1');
  t = t.replace(re(`${A}(\\d{1,2})/(\\d{1,2})(?:/(\\d{4}))?${D}`), (m, d: string, me: string, an?: string) => {
    const dia = Number(d), mes = Number(me);
    if (!dia || dia > 31 || !mes || mes > 12) return m;
    return `${dia === 1 ? 'primero' : cardinalEs(dia)} de ${NOMBRE_MES[mes - 1]}${an ? ` de ${cardinalEs(Number(an))}` : ''}`;
  });
  // Importe con céntimos: 12,50 dólares → doce dólares con cincuenta.
  t = t.replace(re(`${A}(\\d+)[,.](\\d{2})\\s+(dólares|dólar|euros|euro|pesos|soles)${D}`), (_m, e: string, c: string, mon: string) => {
    const [uno, varios] = MONEDA[mon.toLowerCase()] ?? [mon, mon];
    const entero = Number(e), cent = Number(c);
    if (!entero) return `${cardinalEs(cent, 'un')} centavos`;
    const base = `${cardinalEs(entero, 'un')} ${entero === 1 ? uno : varios}`;
    return cent ? `${base} con ${cardinalEs(cent)}` : base;
  });
  // Decimales: 4,8 y 1.5 → cuatro coma ocho, uno coma cinco (con punto y 3+ cifras, «punto»).
  t = t.replace(re(`${A}(\\d+)([,.])(\\d+)${D}`), (_m, e: string, sep: string, d: string) =>
    `${cardinalEs(Number(e))} ${sep === ',' || d.length <= 2 ? 'coma' : 'punto'} ${leerDecimales(d, (n) => cardinalEs(n), DIGITOS)}`);
  // Rangos: 1930–1939 → mil novecientos treinta a mil novecientos treinta y nueve.
  t = t.replace(re(`${A}(\\d+)(?:\\s?–\\s?|-)(\\d+)${D}`), (_m, a: string, b: string) => `${cardinalEs(Number(a))} a ${cardinalEs(Number(b))}`);
  t = t.replace(/(\d)\s*\+\s*(?=\d)/gu, '$1 más ').replace(/(\d)\s*×\s*(?=\d)/gu, '$1 por ');
  // «1 mil» → mil; el 911 se dice «nueve once».
  t = t.replace(re(`${A}1\\s+mil${D}`), 'mil').replace(re(`${A}911${D}`), 'nueve once');
  return restoCifras(t, (n, _c, resto, antes) => {
    // Un año no se apocopa ante el verbo o el nombre que sigue: «En 2031 coordinaba», «En 2001 Emma».
    const p = siguientePalabra(resto);
    if (n >= 1000 && n <= 2100 && !MONEDA[p]) return cardinalEs(n, FEMENINOS.has(p) ? 'una' : 'uno');
    return cardinalEs(n, formaAnte(resto, antes));
  });
}
