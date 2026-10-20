/**
 * Cifras portuguesas (Brasil) → palabras antes de sintetizar. Con
 * `language_code: pt`, Flash v2.5 lee mal las cifras («4,8» → «quatro do
 * oito», «6h» → 18h, «5h50» → 17:50, «R$ 4.500», «60%»; medición del
 * 19-10-2026), así que la voz recibe el número escrito.
 *
 * Decisiones: horas «6h» → «seis horas», «5h50» → «cinco e cinquenta»,
 * «21:00» → «vinte e uma horas» (hora en femenino); «dia 1» y «1º de maio» →
 * «primeiro»; años como cardinal («dois mil e vinte e quatro»); importes
 * «R$ 19,90» → «dezenove reais e noventa centavos» (voz_texto.ts ya puso
 * «reais» detrás del número); rangos «1930–1939» → «… a …»; teléfonos y
 * códigos de 5+ cifras (o de 4+ tras «protocolo», «número»…), cifra a cifra.
 * Género: «uma/duas» y las centenas en femenino («duzentas») ante los
 * femeninos frecuentes y las terminaciones -ção/-dade.
 */
import { A, D, re, fueraDeUrls, telefonos, codigos, codigosTrasPalabra, unirMiles, restoCifras, siguientePalabra, leerDecimales, cifraACifra } from './numeros_comun.js';

const DIGITOS = ['zero', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove'] as const;
const HASTA19 = [...DIGITOS, 'dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove'];
const DEZENAS = ['', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta', 'setenta', 'oitenta', 'noventa'];
const CENTENAS = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos', 'seiscentos', 'setecentos', 'oitocentos', 'novecentos'];
const centena = (c: number, g: Genero) => (g === 'f' && c > 1 ? CENTENAS[c].replace(/os$/, 'as') : CENTENAS[c]);
const ORDINAIS = ['', 'primeiro', 'segundo', 'terceiro', 'quarto', 'quinto', 'sexto', 'sétimo', 'oitavo', 'nono', 'décimo'];
const MESES = 'janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro';

/** Femeninos frecuentes tras una cifra: «uma hora», «duas pessoas». */
const FEMININOS = new Set(['hora', 'horas', 'pessoa', 'pessoas', 'semana', 'semanas', 'vez', 'vezes', 'xícara', 'xícaras', 'página', 'páginas',
  'palavra', 'palavras', 'criança', 'crianças', 'mulher', 'mulheres', 'sala', 'salas', 'parte', 'partes', 'opção', 'opções', 'pergunta',
  'perguntas', 'aula', 'aulas', 'nota', 'notas', 'cidade', 'cidades', 'língua', 'línguas', 'coisa', 'coisas', 'colher', 'colheres', 'noite',
  'noites', 'parcela', 'parcelas', 'cláusula', 'cláusulas', 'linha', 'linhas', 'estrela', 'estrelas', 'fase', 'fases', 'etapa', 'etapas',
  'vaga', 'vagas', 'mesa', 'mesas', 'cama', 'camas', 'garrafa', 'garrafas', 'caixa', 'caixas', 'fatia', 'fatias', 'visita', 'visitas',
  'resposta', 'respostas', 'empresa', 'empresas', 'loja', 'lojas', 'reserva', 'reservas', 'família', 'famílias', 'escola', 'escolas',
  'turma', 'turmas', 'peça', 'peças', 'questão', 'questões', 'casa', 'casas', 'ligação', 'ligações', 'mala', 'malas', 'diária', 'diárias',
  'reunião', 'reuniões', 'decisão', 'decisões', 'sessão', 'sessões', 'opinião', 'opiniões']);
/** Terminaciones femeninas seguras: -ção, -dade («duzentas inscrições», «duas unidades»). */
const TERMINACAO_FEMININA = /(?:ção|ções|dade|dades)$/u;

type Genero = 'm' | 'f';

function hasta99(n: number, g: Genero = 'm'): string {
  const fem = (s: string) => (g === 'f' ? s.replace(/^um$/, 'uma').replace(/^dois$/, 'duas') : s);
  if (n < 20) return fem(HASTA19[n]);
  const u = n % 10;
  return u === 0 ? DEZENAS[Math.floor(n / 10)] : `${DEZENAS[Math.floor(n / 10)]} e ${fem(DIGITOS[u])}`;
}

function hasta999(n: number, g: Genero = 'm'): string {
  if (n === 100) return 'cem';
  const c = Math.floor(n / 100), r = n % 100;
  if (!c) return hasta99(r, g);
  return r ? `${centena(c, g)} e ${hasta99(r, g)}` : centena(c, g);
}

/**
 * Cardinal: 1999 → mil novecentos e noventa e nove; 2024 → dois mil e vinte
 * e quatro; 2500 → dois mil e quinhentos; 1250 → mil duzentos e cinquenta.
 * La «e» tras «mil» solo va si el resto es < 100 o una centena redonda.
 */
export function cardinalPt(n: number, g: Genero = 'm'): string {
  if (!Number.isSafeInteger(n) || n < 0) return String(n);
  if (n < 1000) return hasta999(n, g);
  const junta = (alto: string, r: number) => (r ? `${alto}${r < 100 || r % 100 === 0 ? ' e' : ''} ${hasta999(r, g)}` : alto);
  if (n < 1_000_000) {
    const m = Math.floor(n / 1000), r = n % 1000;
    return junta(m === 1 ? 'mil' : `${hasta999(m, g)} mil`, r);
  }
  const mi = Math.floor(n / 1_000_000), r = n % 1_000_000;
  const alto = mi === 1 ? 'um milhão' : `${cardinalPt(mi)} milhões`;
  return r ? `${alto}${r < 100 || (r < 1000 && r % 100 === 0) ? ' e' : ''} ${cardinalPt(r, g)}` : alto;
}

const generoAnte = (resto: string): Genero => {
  const p = siguientePalabra(resto);
  return FEMININOS.has(p) || TERMINACAO_FEMININA.test(p) ? 'f' : 'm';
};

/** Normaliza un texto portugués para la voz. */
export function numerosEnPalabrasPt(texto: string): string {
  return fueraDeUrls(texto, convertir);
}

/** Hora en femenino: 1 → uma, 2 → duas, 21 → vinte e uma. */
const hora = (h: number) => cardinalPt(h, 'f');

function convertir(texto: string): string {
  let t = texto.replace(/\b[Nn]\.?\s?º\s*(?=\d)/gu, 'número ');
  t = telefonos(t, (g) => cifraACifra(g, DIGITOS));
  t = codigosTrasPalabra(t, 'protocolo|Protocolo|número|código|senha|ramal|pedido|chamado|atendimento', DIGITOS);
  t = codigos(t, DIGITOS, /^\s*(reais|real|dólares|euros|%|pessoas)/u);
  t = t
    // R$ y US$ ya vienen detrás del número (voz_texto.ts); quedan € y $ sueltos.
    .replace(/€\s?(\d+(?:[.,]\d+)*)/gu, '$1 euros')
    .replace(/(\d)\s?€/gu, '$1 euros')
    .replace(/\$\s?(\d+(?:[.,]\d+)*)/gu, '$1 dólares');
  t = unirMiles(t, 'punto');
  t = t
    .replace(/(^|[\s(:])[−-](?=\d)/gu, '$1menos ')
    .replace(/(\d)\s?%/gu, '$1 por cento')
    .replace(/(\d)\s?°(?:\s?C\b)?/gu, '$1 graus')
    .replace(re(`(\\d)\\s?km/h${D}`), '$1 quilômetros por hora')
    .replace(re(`(\\d)\\s?(km|kg|g|ml|min)${D}`), (_m, d: string, u: string) =>
      `${d} ${{ km: 'quilômetros', kg: 'quilos', g: 'gramas', ml: 'mililitros', min: 'minutos' }[u]}`);
  // Hora: 6h → seis horas; 5h50 → cinco e cinquenta; 21:00 → vinte e uma horas.
  t = t.replace(re(`${A}(\\d{1,2})(?:\\s?h(\\d{2})?|:(\\d{2}))${D}`), (m, h: string, mh?: string, mc?: string) => {
    const hh = Number(h), mm = Number(mh ?? mc ?? '0');
    if (hh > 24 || mm > 59) return m;
    if (!mm) return `${hora(hh)} ${hh === 1 ? 'hora' : 'horas'}`;
    return `${hora(hh)} e ${cardinalPt(mm)}`;
  });
  // Ordinales: 1º, 1.º → primeiro; 1ª → primeira; «dia 1» y «1 de maio» → primeiro.
  t = t.replace(re(`${A}(\\d{1,2})\\.?(º|ª)(?![\\p{L}\\p{N}])`), (_m, d: string, suf: string) => {
    const n = Number(d);
    if (n < 1 || n > 10) return cardinalPt(n);
    return suf === 'ª' ? ORDINAIS[n].replace(/o$/, 'a') : ORDINAIS[n];
  });
  t = t.replace(re(`${A}1(\\s+de\\s+(?:${MESES}))`), 'primeiro$1').replace(re(`(\\b[Dd]ia\\s+)1${D}`), '$1primeiro');
  t = t.replace(re(`${A}(\\d{1,2})/(\\d{1,2})(?:/(\\d{4}))?${D}`), (m, d: string, me: string, an?: string) => {
    const dia = Number(d), mes = Number(me);
    if (!dia || dia > 31 || !mes || mes > 12) return m;
    return `${dia === 1 ? 'primeiro' : cardinalPt(dia)} de ${MESES.split('|')[mes - 1]}${an ? ` de ${cardinalPt(Number(an))}` : ''}`;
  });
  // Importe con centavos: 19,90 reais → dezenove reais e noventa centavos.
  t = t.replace(re(`${A}(\\d+)[,.](\\d{2})\\s+(reais|real|dólares|euros)${D}`), (_m, e: string, c: string, moeda: string) => {
    const inteiro = Number(e), cent = Number(c);
    const singular: Record<string, string> = { reais: 'real', real: 'real', dólares: 'dólar', euros: 'euro' };
    const plural: Record<string, string> = { reais: 'reais', real: 'reais', dólares: 'dólares', euros: 'euros' };
    const centavos = `${cardinalPt(cent)} ${cent === 1 ? 'centavo' : 'centavos'}`;
    if (!inteiro) return centavos;
    const base = `${cardinalPt(inteiro)} ${inteiro === 1 ? singular[moeda] : plural[moeda]}`;
    return cent ? `${base} e ${centavos}` : base;
  });
  // Decimales: 4,8 y 1.5 → quatro vírgula oito, um vírgula cinco (con punto y 3+ cifras, «ponto»).
  t = t.replace(re(`${A}(\\d+)([,.])(\\d+)${D}`), (_m, e: string, sep: string, d: string) =>
    `${cardinalPt(Number(e))} ${sep === ',' || d.length <= 2 ? 'vírgula' : 'ponto'} ${leerDecimales(d, (n) => cardinalPt(n), DIGITOS)}`);
  // Rangos: 1930–1939 → mil novecentos e trinta a mil novecentos e trinta e nove.
  t = t.replace(re(`${A}(\\d+)(?:\\s?–\\s?|-)(\\d+)${D}`), (_m, a: string, b: string) => `${cardinalPt(Number(a))} a ${cardinalPt(Number(b))}`);
  t = t.replace(/(\d)\s*\+\s*(?=\d)/gu, '$1 mais ').replace(/(\d)\s*×\s*(?=\d)/gu, '$1 vezes ');
  t = t.replace(re(`${A}1\\s+mil${D}`), 'mil'); // «R$ 1 mil» → mil reais
  return restoCifras(t, (n, _c, resto) => cardinalPt(n, generoAnte(resto)));
}
