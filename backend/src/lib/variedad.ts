/**
 * Repetición del tutor, medida sin IA sobre el historial. La usan la nota de
 * cada turno (ia.ts) y el panel (Conversaciones IA). En las llamadas de
 * oct-nov 2026 el tutor repetía lo que el alumno acababa de decir («Coffee,
 * yes»), volvía a hacer preguntas ya respondidas («Do you live in Denver or
 * another city?» tres veces) y encadenaba preguntas de dos opciones.
 */
import type { AjustesTutor } from './ajustes_tutor.js';

type Espera = { tipo: 'repetir' | 'elegir' | 'responder'; modelo: string };
type Turno = { rol: 'tutor' | 'alumno'; texto: string; espera?: Espera };

/** Palabras de un texto (en chino y japonés sin espacios, pares de caracteres). */
export const piezas = (t: string) => {
  const s = t.toLocaleLowerCase().replace(/[\p{P}\p{S}]+/gu, ' ').trim();
  if (/[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]/u.test(s) && !/\s/.test(s)) return new Set([...s].map((c, i, a) => c + (a[i + 1] ?? '')));
  return new Set(s.split(/\s+/).filter(Boolean));
};
/** Parte común de dos textos respecto al más corto (0–1). */
export const parecido = (a: string, b: string) => {
  const x = piezas(a), y = piezas(b);
  if (!x.size || !y.size) return 0;
  let comunes = 0; for (const w of x) if (y.has(w)) comunes++;
  return comunes / Math.min(x.size, y.size);
};

const frases = (t: string) => t.split(/(?<=[.!?。！？])\s*/u).map(s => s.trim()).filter(Boolean);
export const preguntasDe = (t: string) => frases(t).filter(s => /[?？]$/.test(s));
/** Las dos primeras palabras («perfect i», «oh nice»); en chino o japonés, los 3 primeros caracteres. */
export function apertura(t: string) {
  const s = t.toLocaleLowerCase().replace(/[\p{P}\p{S}]+/gu, ' ').trim();
  if (!/\s/.test(s.slice(0, 12)) && /[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Hangul}]/u.test(s)) return s.slice(0, 3);
  return s.split(/\s+/).slice(0, 2).join(' ');
}
// «X or Y?» en los diez idiomas del curso.
const OPCION = /\s(or|o|ou|oder|или|还是|或者|それとも|아니면)\s|还是|それとも|아니면/iu;
export const esOpciones = (texto: string, espera?: Espera) =>
  espera ? espera.tipo === 'elegir' : preguntasDe(texto).some(q => OPCION.test(q));
/**
 * El tutor abre repitiendo lo que el alumno acaba de decir. No cuenta si le
 * había pedido repetir (celebrar su frase es lo esperado) ni si corrige (cita).
 */
export function esEco(tutor: string, alumno: string, pedido?: Espera) {
  // Si el alumno preguntó («And you?»), responder con sus mismas palabras es lo normal.
  if (!alumno.trim() || /[?？]/.test(alumno) || pedido?.tipo === 'repetir' || /[«»“”"„「」『』]/u.test(tutor)) return false;
  const primera = frases(tutor)[0] ?? '';
  return piezas(alumno).size >= 1 && piezas(primera).size <= 8 && parecido(primera, alumno) >= 0.6;
}
const normal = (t: string) => t.toLocaleLowerCase().normalize('NFKC').replace(/[\p{P}\p{S}\s]+/gu, ' ').trim();
export const frasesUsadas = (texto: string, evitar: string[]) => evitar.filter(f => normal(f) && ` ${normal(texto)} `.includes(` ${normal(f)} `));

/** Indicadores de repetición de una llamada (historial completo). */
export function medirRepeticion(historial: Turno[], evitar: string[] = []) {
  let preguntasRepetidas = 0, eco = 0, opciones = 0, aperturasRepetidas = 0, tutor = 0;
  const vistas: string[] = [], aperturas: string[] = [], muletillas = new Map<string, number>();
  // Por cada turno del tutor, qué se repitió (el panel lo marca en la conversación).
  const marcas: string[][] = [];
  historial.forEach((t, i) => {
    if (t.rol !== 'tutor') return;
    tutor++;
    const m: string[] = []; marcas.push(m);
    const previo = historial[i - 1]?.rol === 'alumno' ? historial[i - 1].texto : '';
    const pedido = [...historial.slice(0, i)].reverse().find(x => x.rol === 'tutor')?.espera;
    // Tras un silencio o una pista (turno del alumno vacío), repetir la pregunta más fácil es lo pedido.
    const trasAviso = historial[i - 1]?.rol === 'alumno' && !previo.trim();
    for (const q of preguntasDe(t.texto)) {
      if (!trasAviso && piezas(q).size >= 3 && vistas.some(v => parecido(v, q) >= 0.8)) { preguntasRepetidas++; if (!m.includes('pregunta repetida')) m.push('pregunta repetida'); }
      vistas.push(q);
    }
    if (esEco(t.texto, previo, pedido)) { eco++; m.push('eco'); }
    if (esOpciones(t.texto, t.espera)) { opciones++; m.push('dos opciones'); }
    const a = apertura(t.texto);
    if (a && aperturas.slice(-3).includes(a)) { aperturasRepetidas++; m.push('misma apertura'); }
    aperturas.push(a);
    for (const f of frasesUsadas(t.texto, evitar)) { muletillas.set(f, (muletillas.get(f) ?? 0) + 1); m.push(`«${f}»`); }
  });
  return { turnosTutor: tutor, preguntasRepetidas, eco, opciones, aperturasRepetidas, muletillas: Object.fromEntries(muletillas), marcas };
}

const corto = (t: string, n = 70) => (t.length > n ? `${t.slice(0, n - 1)}…` : t);

/**
 * Nota para el turno que viene: qué ya preguntó, cómo empezaron sus últimos
 * turnos y si se está repitiendo. Va junto al mensaje del alumno, donde el
 * modelo la sigue (en el prompt de sistema la olvidaba con la charla delante).
 */
export function notaVariedad(historial: Turno[], a: AjustesTutor): string {
  const tutor = historial.filter(t => t.rol === 'tutor');
  if (!tutor.length) return '';
  const notas: string[] = [];
  const ultimo = tutor[tutor.length - 1];
  const i = historial.lastIndexOf(ultimo);
  const alumnoAntes = historial[i - 1]?.rol === 'alumno' ? historial[i - 1].texto : '';
  const pedidoAntes = tutor[tutor.length - 2]?.espera;
  const preguntas = [...new Set(tutor.flatMap(t => preguntasDe(t.texto)).filter(q => piezas(q).size >= 3))].slice(-6);
  if (tutor.length >= 2 && preguntas.length) notas.push(`Ya preguntaste en esta llamada: ${preguntas.map(q => `«${corto(q)}»`).join(' ')}. No repitas ninguna ni otra con el mismo sentido: si ya te lo contó, úsalo y avanza.`);
  const aperturas = tutor.slice(-3).map(t => apertura(t.texto)).filter(Boolean);
  if (aperturas.length >= 2) notas.push(`Tus últimos turnos empezaron con: ${aperturas.map(x => `«${x}…»`).join(', ')}. Empieza este de otra forma.`);
  if (!a.eco && esEco(ultimo.texto, alumnoAntes, pedidoAntes)) notas.push('En tu turno anterior repetiste lo que dijo el alumno: esta vez no repitas sus palabras; reacciona con algo nuevo (tu opinión, un dato tuyo) y avanza.');
  const seguidas = tutor.slice(-2).filter(t => esOpciones(t.texto, t.espera)).length;
  if (a.opciones === 'pocas' ? seguidas >= 1 : seguidas >= 2) notas.push('Ya le hiciste preguntas de dos opciones: ahora una pregunta abierta (qué, cómo, por qué, cuéntame…), salvo que esté bloqueado.');
  const usadas = [...new Set(tutor.slice(-4).flatMap(t => frasesUsadas(t.texto, a.frasesEvitar)))];
  if (usadas.length) notas.push(`Dijiste ${usadas.map(f => `«${f}»`).join(', ')}, que no debes usar.`);
  if (a.enfoque === 'guiar') {
    const n = tutor.length + 1;
    if (n % 7 === 0) notas.push(`Turno ${n}: toca el mini repaso de la clase guiada (lo que ya dijo bien, en una frase) y el paso siguiente.`);
  }
  return notas.length ? `[Variedad, calculado por la app: ${notas.join(' ')}]` : '';
}
