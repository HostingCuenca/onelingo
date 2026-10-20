/**
 * Cifras rusas → palabras antes de sintetizar. Con `language_code: ru`, Flash
 * v2.5 confunde años (1147 → 1947/1167, 1911 → 1919), no los declina («в 1911
 * году») y «Статья 2.» sale «Статья да» (medición del 19-10-2026), así que la
 * voz recibe el número escrito.
 *
 * Decisiones: año con «год» → ordinal en su caso, declinando solo la última
 * palabra («в 1911 году» → «в тысяча девятьсот одиннадцатом году»; «к 2030
 * году» → «к две тысячи тридцатому году», dativo; «с 1990 года» → genitivo;
 * «2020 год» → nominativo; «2020 г.» según la preposición). Lo demás, cardinal
 * en nominativo (один/одна, два/две ante femeninos frecuentes). Porcentajes y
 * unidades concuerdan (1 процент, 2–4 процента, 5+ процентов). Decimales
 * «4,8» → «четыре целых восемь десятых». Horas «8:30» → «восемь тридцать»,
 * «9:00» → «девять ноль-ноль». Rangos «2–4» → «от двух до четырёх» (con años,
 * con raya). Teléfonos y códigos de 5+ cifras, cifra a cifra.
 */
import { A, D, re, fueraDeUrls, telefonos, codigos, unirMiles, restoCifras, siguientePalabra, cifraACifra } from './numeros_comun.js';

const CIFRAS = ['ноль', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять'] as const;
const HASTA19 = [...CIFRAS, 'десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать', 'семнадцать',
  'восемнадцать', 'девятнадцать'];
const DECENAS = ['', '', 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто'];
const CENTENAS = ['', 'сто', 'двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот', 'семьсот', 'восемьсот', 'девятьсот'];
// Genitivo (para «от … до …»).
const GEN_HASTA19 = ['ноля', 'одного', 'двух', 'трёх', 'четырёх', 'пяти', 'шести', 'семи', 'восьми', 'девяти', 'десяти', 'одиннадцати',
  'двенадцати', 'тринадцати', 'четырнадцати', 'пятнадцати', 'шестнадцати', 'семнадцати', 'восемнадцати', 'девятнадцати'];
const GEN_DECENAS = ['', '', 'двадцати', 'тридцати', 'сорока', 'пятидесяти', 'шестидесяти', 'семидесяти', 'восьмидесяти', 'девяноста'];
const GEN_CENTENAS = ['', 'ста', 'двухсот', 'трёхсот', 'четырёхсот', 'пятисот', 'шестисот', 'семисот', 'восьмисот', 'девятисот'];
// Raíces de ordinal: первый, второй, третий…
const ORD_HASTA19 = ['нулев', 'перв', 'втор', 'трет', 'четвёрт', 'пят', 'шест', 'седьм', 'восьм', 'девят', 'десят', 'одиннадцат',
  'двенадцат', 'тринадцат', 'четырнадцат', 'пятнадцат', 'шестнадцат', 'семнадцат', 'восемнадцат', 'девятнадцат'];
const ORD_DECENAS = ['', '', 'двадцат', 'тридцат', 'сороков', 'пятидесят', 'шестидесят', 'семидесят', 'восьмидесят', 'девяност'];
const ORD_CENTENAS = ['', 'сот', 'двухсот', 'трёхсот', 'четырёхсот', 'пятисот', 'шестисот', 'семисот', 'восьмисот', 'девятисот'];
/** Raíces con desinencia tónica «-ой»: второй, шестой, седьмой, восьмой, сороковой. */
const TONICAS = new Set(['нулев', 'втор', 'шест', 'седьм', 'восьм', 'сороков']);

/** Caso del ordinal (masculino salvo fem/neutro/plural). */
export type Caso = 'nom' | 'gen' | 'dat' | 'prep' | 'instr' | 'fem' | 'femAcus' | 'femOblicuo' | 'neutro' | 'plural';
/** Desinencias: [dura -ый, tónica -ой, «трет-» (третий)]. */
const DESINENCIAS: Record<Caso, [string, string, string]> = {
  nom: ['ый', 'ой', 'ий'], gen: ['ого', 'ого', 'ьего'], dat: ['ому', 'ому', 'ьему'], prep: ['ом', 'ом', 'ьем'], instr: ['ым', 'ым', 'ьим'],
  fem: ['ая', 'ая', 'ья'], femAcus: ['ую', 'ую', 'ью'], femOblicuo: ['ой', 'ой', 'ьей'], neutro: ['ое', 'ое', 'ье'], plural: ['ых', 'ых', 'ьих'],
};

/** Femeninos frecuentes: «одна минута», «две недели». */
const FEMENINOS = new Set(['минута', 'минуты', 'неделя', 'недели', 'книга', 'книги', 'страница', 'страницы', 'комната', 'комнаты', 'станция',
  'станции', 'остановка', 'остановки', 'ошибка', 'ошибки', 'задача', 'задачи', 'строка', 'строки', 'копейка', 'копейки', 'чашка', 'чашки',
  'бутылка', 'бутылки', 'статья', 'статьи', 'девушка', 'девушки', 'женщина', 'женщины', 'сестра', 'сестры', 'дочь', 'дочери', 'ночь', 'ночи',
  'часть', 'части', 'улица', 'улицы', 'буква', 'буквы', 'группа', 'группы', 'секунда', 'секунды', 'подруга', 'подруги']);

/** Forma según el número: 1 процент, 2 процента, 5 процентов (11–14 → процентов). */
export function formaPorNumero(n: number, [uno, pocos, muchos]: readonly [string, string, string]): string {
  const dos = n % 100, u = n % 10;
  if (dos >= 11 && dos <= 14) return muchos;
  if (u === 1) return uno;
  if (u >= 2 && u <= 4) return pocos;
  return muchos;
}

type Genero = 'm' | 'f';

function unidad(u: number, g: Genero): string {
  if (g === 'f' && u === 1) return 'одна';
  if (g === 'f' && u === 2) return 'две';
  return HASTA19[u];
}

function hasta999(n: number, g: Genero = 'm'): string {
  const c = Math.floor(n / 100), r = n % 100;
  const partes: string[] = c ? [CENTENAS[c]] : [];
  if (r >= 20) {
    partes.push(DECENAS[Math.floor(r / 10)]);
    if (r % 10) partes.push(unidad(r % 10, g));
  } else if (r || !c) partes.push(unidad(r, g));
  return partes.join(' ');
}

/** Cardinal: 1147 → тысяча сто сорок семь; 2030 → две тысячи тридцать. */
export function cardinalRu(n: number, g: Genero = 'm'): string {
  if (!Number.isSafeInteger(n) || n < 0) return String(n);
  if (n < 1000) return hasta999(n, g);
  if (n < 1_000_000) {
    const m = Math.floor(n / 1000), r = n % 1000;
    const miles = m === 1 ? 'тысяча' : `${hasta999(m, 'f')} ${formaPorNumero(m, ['тысяча', 'тысячи', 'тысяч'])}`;
    return r ? `${miles} ${hasta999(r, g)}` : miles;
  }
  const mi = Math.floor(n / 1_000_000), r = n % 1_000_000;
  const millones = mi === 1 ? 'миллион' : `${cardinalRu(mi)} ${formaPorNumero(mi, ['миллион', 'миллиона', 'миллионов'])}`;
  return r ? `${millones} ${cardinalRu(r, g)}` : millones;
}

function genHasta999(n: number): string {
  const c = Math.floor(n / 100), r = n % 100;
  const partes: string[] = c ? [GEN_CENTENAS[c]] : [];
  if (r >= 20) {
    partes.push(GEN_DECENAS[Math.floor(r / 10)]);
    if (r % 10) partes.push(GEN_HASTA19[r % 10]);
  } else if (r || !c) partes.push(GEN_HASTA19[r]);
  return partes.join(' ');
}

/** Cardinal en genitivo: 2 → двух; 20 → двадцати; 1500 → тысячи пятисот. */
export function genitivoRu(n: number): string {
  if (n < 1000) return genHasta999(n);
  if (n < 1_000_000) {
    const m = Math.floor(n / 1000), r = n % 1000;
    const miles = m === 1 ? 'тысячи' : `${genHasta999(m).replace(/одного$/, 'одной')} ${m % 10 === 1 && m % 100 !== 11 ? 'тысячи' : 'тысяч'}`;
    return r ? `${miles} ${genHasta999(r)}` : miles;
  }
  return cardinalRu(n);
}

function desinencia(raiz: string, caso: Caso): string {
  const tipo = raiz === 'трет' ? 2 : TONICAS.has(raiz) ? 1 : 0;
  return raiz + DESINENCIAS[caso][tipo];
}

/**
 * Ordinal: solo se declina la última palabra; las anteriores quedan en
 * cardinal («тысяча девятьсот одиннадцатом»). 2000 → двухтысячный.
 */
export function ordinalRu(n: number, caso: Caso = 'nom'): string {
  if (!Number.isSafeInteger(n) || n < 0 || n >= 1_000_000) return cardinalRu(n);
  const r = n % 100;
  if (r) {
    const previo = n - r ? `${cardinalRu(n - r)} ` : '';
    if (r < 20) return previo + desinencia(ORD_HASTA19[r], caso);
    const d = Math.floor(r / 10), u = r % 10;
    return u ? `${previo}${DECENAS[d]} ${desinencia(ORD_HASTA19[u], caso)}` : previo + desinencia(ORD_DECENAS[d], caso);
  }
  if (n % 1000) {
    const previo = n - (n % 1000) ? `${cardinalRu(n - (n % 1000))} ` : '';
    return previo + desinencia(ORD_CENTENAS[(n % 1000) / 100], caso);
  }
  const m = n / 1000;
  const prefijo = m === 1 ? '' : genHasta999(m).replace(/одного$/, 'одно').replace(/\s+/g, '');
  return desinencia(`${prefijo}тысячн`, caso);
}

/** Decimal: 4,8 → четыре целых восемь десятых; 3,25 → три целых двадцать пять сотых. */
function decimalRu(entero: string, fraccion: string): string {
  const e = Number(entero), f = Number(fraccion);
  const denominador = (['десят', 'сот', 'тысячн'] as const)[fraccion.length - 1];
  if (!denominador) return `${cardinalRu(e)} запятая ${cifraACifra(fraccion, CIFRAS)}`;
  const enteros = `${cardinalRu(e, 'f')} ${formaPorNumero(e, ['целая', 'целых', 'целых'])}`;
  return `${enteros} ${cardinalRu(f, 'f')} ${formaPorNumero(f, [`${denominador}ая`, `${denominador}ых`, `${denominador}ых`])}`;
}

/** Unidades que concuerdan con el número. */
const UNIDADES: Record<string, { formas: [string, string, string]; genero: Genero }> = {
  '%': { formas: ['процент', 'процента', 'процентов'], genero: 'm' },
  $: { formas: ['доллар', 'доллара', 'долларов'], genero: 'm' },
  '€': { formas: ['евро', 'евро', 'евро'], genero: 'm' },
  '₽': { formas: ['рубль', 'рубля', 'рублей'], genero: 'm' },
  руб: { formas: ['рубль', 'рубля', 'рублей'], genero: 'm' },
  мин: { formas: ['минута', 'минуты', 'минут'], genero: 'f' },
  км: { formas: ['километр', 'километра', 'километров'], genero: 'm' },
  кг: { formas: ['килограмм', 'килограмма', 'килограммов'], genero: 'm' },
};

/** «5 %» → пять процентов; «2,5 %» → две целых пять десятых процента (genitivo singular). */
function conUnidad(cifra: string, uni: string): string {
  const { formas, genero } = UNIDADES[uni];
  const [e, f] = cifra.split(',');
  if (f !== undefined) return `${decimalRu(e, f)} ${formas[1]}`;
  const n = Number(e);
  return `${cardinalRu(n, genero)} ${formaPorNumero(n, formas)}`;
}

/** Preposición ante «N году» / «N г.»: к, по → dativo; с, до, от… → genitivo; в, о → prepositivo. */
const DATIVO = /(?:^|[\s«(])(?:к|К|ко|Ко|по|По)\s+$/u;
const GENITIVO = /(?:^|[\s«(])(?:с|С|со|Со|до|До|от|От|после|После|около|Около|начала|конца|середины)\s+$/u;
const PREPOSITIVO = /(?:^|[\s«(])(?:в|В|во|Во|о|О|об|Об|при|При)\s+$/u;

/** Sufijos de ordinal: 1-й, 2-го, 5-м, 1990-х. */
const SUFIJOS: Record<string, Caso> = {
  й: 'nom', ый: 'nom', ой: 'nom', го: 'gen', ого: 'gen', му: 'dat', ому: 'dat', м: 'prep', ом: 'prep',
  я: 'fem', ая: 'fem', е: 'neutro', ое: 'neutro', х: 'plural', ых: 'plural',
};

/** Divisiones de un texto legal: el número se lee como ordinal concertado con el sustantivo. */
const DIVISIONES: Record<string, Caso> = {
  статья: 'fem', Статья: 'fem', статью: 'femAcus', статье: 'femOblicuo', статьи: 'femOblicuo',
  глава: 'fem', Глава: 'fem', главу: 'femAcus', главе: 'femOblicuo', главы: 'femOblicuo',
  пункт: 'nom', Пункт: 'nom', пункте: 'prep', пункта: 'gen', пункту: 'dat',
  подпункт: 'nom', Подпункт: 'nom', подпункте: 'prep', подпункта: 'gen',
  раздел: 'nom', Раздел: 'nom', разделе: 'prep', раздела: 'gen',
};

/** Normaliza un texto ruso para la voz. */
export function numerosEnPalabrasRu(texto: string): string {
  return fueraDeUrls(texto, convertir);
}

function convertir(texto: string): string {
  let t = telefonos(texto, (g) => cifraACifra(g, CIFRAS));
  t = codigos(t, CIFRAS, /^\s*(%|₽|€|\$|руб|доллар|евро|человек)/u);
  t = t.replace(/([$€])\s?(\d+(?:[\s\u00a0\u202f]\d{3})*(?:,\d+)?)/gu, '$2 $1');
  t = unirMiles(t, 'espacio');
  t = t.replace(/(^|[\s(:])[−-](?=\d)/gu, '$1минус ');
  // Años: «в 1911 году», «к 2030 году», «с 1990 года», «2020 год», «в 2020 г.».
  t = t.replace(re(`${A}(\\d{4})(\\s+)(году|года|годом|год|г\\.)(?![\\p{L}\\p{N}])`), (m: string, d: string, esp: string, palabra: string, pos: number, s: string) => {
    const n = Number(d);
    if (n < 1000 || n > 2100) return m;
    const antes = s.slice(0, pos);
    const caso: Caso = palabra === 'году' ? (DATIVO.test(antes) ? 'dat' : 'prep')
      : palabra === 'года' ? 'gen'
        : palabra === 'годом' ? 'instr'
          : palabra === 'год' ? 'nom'
            : DATIVO.test(antes) ? 'dat' : GENITIVO.test(antes) ? 'gen' : PREPOSITIVO.test(antes) ? 'prep' : 'nom';
    const sustantivo = palabra !== 'г.' ? palabra : { dat: 'году', gen: 'года', prep: 'году' }[caso as string] ?? 'год';
    return `${ordinalRu(n, caso)}${esp}${sustantivo}`;
  });
  // Artículos y apartados: «Статья 2» → «Статья вторая», «в пункте 2» → «в пункте втором».
  t = t.replace(re(`(?<![\\p{L}])(${Object.keys(DIVISIONES).join('|')})(\\s+)(\\d{1,3})${D}`), (_m, nombre: string, esp: string, d: string) =>
    `${nombre}${esp}${ordinalRu(Number(d), DIVISIONES[nombre])}`);
  // Ordinales con sufijo: 1-й → первый; 1990-х → тысяча девятьсот девяностых.
  t = t.replace(re(`${A}(\\d+)-(й|ый|ой|го|ого|му|ому|м|ом|я|ая|е|ое|х|ых)(?![\\p{L}\\p{N}])`), (_m, d: string, suf: string) => ordinalRu(Number(d), SUFIJOS[suf]));
  // Hora: 8:30 → восемь тридцать; 9:00 → девять ноль-ноль; 8:05 → восемь ноль пять.
  t = t.replace(re(`${A}(\\d{1,2}):(\\d{2})${D}`), (m, h: string, mi: string) => {
    const hh = Number(h), mm = Number(mi);
    if (hh > 24 || mm > 59) return m;
    const minutos = mm === 0 ? 'ноль-ноль' : mm < 10 ? `ноль ${cardinalRu(mm)}` : cardinalRu(mm);
    return `${cardinalRu(hh)} ${minutos}`;
  });
  // Número con unidad: 5 % → пять процентов; 45 мин. → сорок пять минут.
  t = t.replace(re(`${A}(\\d+(?:,\\d+)?)[\\s\\u00a0\\u202f]?(%|₽|€|\\$|руб|мин|км|кг)(?![\\p{L}\\p{N}])`), (_m, n: string, uni: string) => conUnidad(n, uni));
  t = t.replace(/(\d)\s?°(?:\s?C\b)?/gu, '$1 градусов');
  // Decimales: 4,8 → четыре целых восемь десятых; 1.2 → один точка два.
  t = t.replace(re(`${A}(\\d+),(\\d+)${D}`), (_m, e: string, f: string) => decimalRu(e, f));
  t = t.replace(re(`${A}(\\d+)\\.(\\d+)${D}`), (_m, a: string, b: string) => `${cardinalRu(Number(a))} точка ${cardinalRu(Number(b))}`);
  // Rangos: 2–4 → от двух до четырёх; con años, con raya.
  t = t.replace(re(`${A}(\\d+)(?:\\s?[–—]\\s?|-)(\\d+)${D}`), (_m, a: string, b: string) => {
    const x = Number(a), y = Number(b);
    return x >= 1000 || y >= 1000 ? `${cardinalRu(x)} — ${cardinalRu(y)}` : `от ${genitivoRu(x)} до ${genitivoRu(y)}`;
  });
  t = t.replace(/(\d)\s*\+\s*(?=\d)/gu, '$1 плюс ').replace(/(\d)\s*×\s*(?=\d)/gu, '$1 умножить на ');
  return restoCifras(t, (n, _c, resto) => cardinalRu(n, FEMENINOS.has(siguientePalabra(resto)) ? 'f' : 'm'));
}
