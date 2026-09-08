/**
 * Generación dinámica de preguntas de diagnóstico con IA (Gemini; OpenAI de respaldo).
 * El motor adaptativo de la app decide nivel, competencia y tipo; la IA redacta la pregunta.
 */
import { config } from './config.js';
import { generarJsonGemini, geminiDisponible } from './ia_gemini.js';
import { generarJsonOpenAI, openaiDisponible } from './ia_openai.js';

const IDIOMAS: Record<string, string> = { en: 'inglés', es: 'español', fr: 'francés', de: 'alemán', pt: 'portugués de Brasil', it: 'italiano', zh: 'chino mandarín (caracteres simplificados, con pinyin entre paréntesis)', ja: 'japonés (con romaji Hepburn entre paréntesis)', ko: 'coreano (con romanización revisada entre paréntesis)', ru: 'ruso (con transliteración latina entre paréntesis)' };
const NO_LATINO = ['zh', 'ja', 'ko', 'ru'];

const SKILLS: Record<string, string> = {
  comprension: 'comprensión (lectura o escucha de un texto corto y responder sobre su contenido)',
  vocabulario: 'vocabulario (palabras, colocaciones, expresiones y su significado)',
  gramatica: 'gramática (estructuras, concordancia, artículos, partículas, casos, declinaciones o clasificadores según el idioma)',
  tiempos: 'tiempos verbales y aspecto (formas verbales, conjugación, pasado/presente/futuro, formas corteses)',
  expresiones: 'expresiones naturales (la forma más natural o idiomática de decir algo, registro formal/informal)',
  contexto: 'comprensión contextual (inferir intención, tono o implicación de un texto corto)',
  cotidiano: 'comunicación cotidiana (qué decir en una situación real: tienda, médico, trabajo, transporte)',
  escritura: 'producción escrita (consigna para escribir 3-7 frases)',
};

const TIPOS: Record<string, string> = {
  eleccion: 'eleccion: pregunta con exactamente 4 opciones y una correcta; "texto" contiene la pregunta o la frase con un hueco "___".',
  natural: 'natural: 4 formas de decir algo en el idioma meta, solo una es natural y correcta; "texto" describe brevemente la situación en el idioma nativo.',
  significado: 'significado: "texto" es una palabra, colocación o expresión en el idioma meta; 4 opciones con su significado en el idioma nativo.',
  contexto: 'contexto: "texto" es un texto corto (1-3 frases) en el idioma meta; "instruccion" contiene la pregunta en el idioma nativo; 4 opciones en el idioma nativo.',
  situacion: 'situacion: "texto" describe una situación real en el idioma nativo; 4 opciones son frases en el idioma meta, solo una es adecuada y correcta.',
  error: 'error: 4 frases en el idioma meta, exactamente una contiene un error gramatical; "texto" = "Elige la incorrecta."; la correcta es la frase con error; la explicación dice cuál es el error.',
  completar: 'completar: "texto" es una frase en el idioma meta con un solo hueco "___" (puede indicar el verbo entre paréntesis); sin opciones; "aceptadas" lista 1-4 respuestas válidas (solo la palabra o palabras del hueco).',
  corta: 'corta: pregunta con respuesta de una o dos palabras en el idioma meta; sin opciones; "aceptadas" lista las respuestas válidas.',
  escucha: 'escucha: "texto" es UNA frase natural en el idioma meta (6-14 palabras, sin romanización) que el alumno solo OYE; 4 opciones en el idioma nativo con lo que significa o lo que se dijo (hora, cantidad, motivo...), solo una correcta.',
  dictado: 'dictado: "texto" es UNA frase natural en el idioma meta (5-12 palabras, sin romanización) que el alumno oye y debe escribir; sin opciones; "aceptadas" = [el mismo texto].',
  escritura: 'escritura: "texto" es la consigna (en el idioma nativo, con la pregunta también en el idioma meta) para escribir 3-7 frases; sin opciones ni aceptadas; "explicacion" es la rúbrica breve.',
};

const ESQUEMA_GEMINI = {
  type: 'OBJECT',
  properties: {
    instruccion: { type: 'STRING' }, texto: { type: 'STRING' },
    opciones: { type: 'ARRAY', items: { type: 'STRING' } }, correcta: { type: 'INTEGER' },
    aceptadas: { type: 'ARRAY', items: { type: 'STRING' } }, explicacion: { type: 'STRING' }, tema: { type: 'STRING' },
  },
  required: ['instruccion', 'texto', 'opciones', 'correcta', 'aceptadas', 'explicacion', 'tema'],
};
const ESQUEMA_OPENAI = {
  type: 'object', additionalProperties: false,
  properties: {
    instruccion: { type: 'string' }, texto: { type: 'string' }, opciones: { type: 'array', items: { type: 'string' } }, correcta: { type: 'integer' },
    aceptadas: { type: 'array', items: { type: 'string' } }, explicacion: { type: 'string' }, tema: { type: 'string' },
  },
  required: ['instruccion', 'texto', 'opciones', 'correcta', 'aceptadas', 'explicacion', 'tema'],
};

export function nivelDescripcion(n: number): string {
  const t: Record<number, string> = {
    0: 'Pre-A1 absoluto: reconocer letras o el sistema de escritura, números 1-10, colores y palabras sueltas',
    1: 'A1.1: presente de ser/tener, saludos, números, familia, frases de 3-6 palabras',
    2: 'A1.2: pasado y futuro básicos, rutinas, preguntas y negaciones, adjetivos sencillos',
    3: 'A2: verbos irregulares frecuentes, comparativos, cantidades, carteles y notas, situaciones reales sencillas',
    4: 'A2+: tiempos perfectos básicos, modales de obligación y permiso, correos cortos, verbos compuestos frecuentes',
    5: 'B1: condicionales simples, presente perfecto frente a pasado, oraciones de relativo, opiniones, llamadas y citas',
    6: 'B1+: segundo condicional, pasado perfecto, voz pasiva, estilo indirecto, quejas corteses, inferencia',
    7: 'B2: tercer condicional e inversiones, futuro perfecto, verbos compuestos avanzados, expresiones idiomáticas, tono y matiz',
    8: 'B2+/C1: condicionales mixtos, oraciones escindidas, subjuntivo o equivalente, colocaciones precisas, hedging y registro formal',
    9: 'C1: cláusulas de participio, modismos avanzados, registro y tacto, elipsis y sustitución, matices de significado',
    10: 'C2: precisión léxica fina, estructuras poco frecuentes, ironía y tono, textos densos, argumentación matizada',
  };
  return t[Math.max(0, Math.min(10, Math.round(n)))];
}

export type PeticionPregunta = {
  idiomaMeta: string; idiomaNativo: string; nivel: number; skill: string; tipo: string;
  evitar: string[]; declarado?: number; estimacion?: number; debilidades?: string[]; aciertos?: number; fallos?: number;
};

export function promptPregunta(p: PeticionPregunta): { system: string; user: string } {
  const meta = IDIOMAS[p.idiomaMeta] ?? p.idiomaMeta;
  const nativo = IDIOMAS[p.idiomaNativo]?.split(' (')[0] ?? 'español';
  const system = `Eres un motor de evaluación adaptativa de idiomas (app OneLingo). Redactas UNA pregunta de diagnóstico a la vez.
Idioma meta: ${meta}. Idioma nativo del alumno: ${nativo}. Todas las instrucciones, opciones de significado y explicaciones van en ${nativo}; el material lingüístico (frases, opciones de forma, textos) va en ${meta}.
Escala interna 1-10 (1 principiante absoluto, 5 B1, 7 B2, 10 C2). La pregunta debe corresponder EXACTAMENTE a la dificultad pedida, ni más fácil ni más difícil.
Reglas:
- No traduzcas mecánicamente ejercicios pensados para inglés: genera ejercicios lingüísticamente apropiados para ${meta} (partículas, clasificadores, casos, formas corteses, tonos, género gramatical, según corresponda).
- ${NO_LATINO.includes(p.idiomaMeta) ? 'En opciones y textos que el alumno LEE, escribe el texto nativo seguido de la romanización entre paréntesis; en los tipos escucha y dictado el campo "texto" va SIN romanización (se sintetiza en voz).' : 'No incluyas romanizaciones.'}
- Exactamente una opción correcta; las incorrectas deben ser plausibles (errores típicos de hispanohablantes), no absurdas. Sin repetir opciones. Nunca uses "todas las anteriores".
- "correcta" es el índice (0-3) de la opción correcta; si no hay opciones, -1.
- "tema" es un nombre corto y concreto del punto evaluado (p. ej. "third conditional", "partícula は", "caso genitivo tras нет"), útil para un plan de refuerzo.
- "explicacion" breve (1-2 frases) en ${nativo}, con la razón. Sin emojis. No menciones que eres una IA.
- Varía el contenido: no repitas ninguna de las preguntas ya hechas que se te indiquen.`;
  const user = `Genera una pregunta de tipo "${p.tipo}" para la competencia "${SKILLS[p.skill] ?? p.skill}" con dificultad ${p.nivel}/10 (${nivelDescripcion(p.nivel)}).
Formato del tipo: ${TIPOS[p.tipo] ?? p.tipo}
${p.declarado != null ? `Contexto del alumno: nivel declarado ${p.declarado}, estimación actual ${p.estimacion?.toFixed(1)}, aciertos ${p.aciertos ?? 0}, fallos ${p.fallos ?? 0}${p.debilidades?.length ? `, debilidades detectadas: ${p.debilidades.join(', ')}` : ''}.` : ''}
${p.evitar.length ? `Preguntas ya hechas (no las repitas ni uses el mismo contenido):\n- ${p.evitar.slice(-20).join('\n- ')}` : ''}`;
  return { system, user };
}

export const diagIaDisponible = () => geminiDisponible() || openaiDisponible();

/** Gemini a veces tarda o devuelve 503 en picos de demanda: si no responde en `ms`, se pasa a OpenAI. */
function conTimeout<T>(p: Promise<T>, ms: number): Promise<T> {
  return new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(new Error(`timeout ${ms} ms`)), ms);
    p.then((v) => { clearTimeout(t); resolve(v); }, (e) => { clearTimeout(t); reject(e); });
  });
}
const GEMINI_MS = Number(process.env.GEMINI_TIMEOUT_MS ?? 12000);

export async function generarPregunta(p: PeticionPregunta) {
  const { system, user } = promptPregunta(p);
  let json: any, modelo: string;
  if (geminiDisponible()) {
    try {
      const r = await conTimeout(generarJsonGemini(system, [{ role: 'user', text: user }], ESQUEMA_GEMINI), GEMINI_MS);
      json = r.json; modelo = r.modelo;
    } catch (e) {
      console.warn('[diagnostico] Gemini falló, se usa OpenAI:', String(e).slice(0, 120));
      if (!openaiDisponible()) throw e;
      const r = await generarJsonOpenAI(system, [{ role: 'user', content: user }], ESQUEMA_OPENAI);
      json = r.json; modelo = r.modelo;
    }
  } else {
    const r = await generarJsonOpenAI(system, [{ role: 'user', content: user }], ESQUEMA_OPENAI);
    json = r.json; modelo = r.modelo;
  }
  const opciones: string[] = Array.isArray(json.opciones) ? json.opciones.map(String).filter(Boolean).slice(0, 4) : [];
  const conOpciones = !['completar', 'corta', 'dictado', 'escritura'].includes(p.tipo);
  let correcta = Number.isInteger(json.correcta) ? json.correcta : -1;
  let aceptadas: string[] = Array.isArray(json.aceptadas) ? json.aceptadas.map(String).filter(Boolean) : [];
  const texto = String(json.texto ?? '').trim();
  if (conOpciones) {
    if (opciones.length < 3 || correcta < 0 || correcta >= opciones.length) throw new Error('pregunta_invalida: opciones');
    aceptadas = [];
  } else {
    correcta = -1;
    if (p.tipo === 'dictado') aceptadas = [texto];
    if (p.tipo !== 'escritura' && aceptadas.length === 0) throw new Error('pregunta_invalida: aceptadas');
    if (p.tipo === 'completar' && !texto.includes('___')) throw new Error('pregunta_invalida: hueco');
  }
  if (!texto) throw new Error('pregunta_invalida: texto');
  return {
    nivel: p.nivel, skill: p.skill, tipo: p.tipo, tema: String(json.tema ?? p.skill).slice(0, 60),
    instruccion: String(json.instruccion ?? ''), texto, opciones: conOpciones ? opciones : [], correcta, aceptadas, explicacion: String(json.explicacion ?? ''), modelo,
  };
}

const ESQUEMA_PERFIL_GEMINI = {
  type: 'OBJECT',
  properties: { resumen: { type: 'STRING' }, recomendaciones: { type: 'ARRAY', items: { type: 'STRING' } }, plan: { type: 'ARRAY', items: { type: 'STRING' } } },
  required: ['resumen', 'recomendaciones', 'plan'],
};
const ESQUEMA_PERFIL_OPENAI = {
  type: 'object', additionalProperties: false,
  properties: { resumen: { type: 'string' }, recomendaciones: { type: 'array', items: { type: 'string' } }, plan: { type: 'array', items: { type: 'string' } } },
  required: ['resumen', 'recomendaciones', 'plan'],
};

/** Resumen narrativo y plan personalizado a partir del resultado numérico. */
export async function generarPerfil(p: { idiomaMeta: string; idiomaNativo: string; resultado: any }) {
  const meta = IDIOMAS[p.idiomaMeta]?.split(' (')[0] ?? p.idiomaMeta;
  const nativo = IDIOMAS[p.idiomaNativo]?.split(' (')[0] ?? 'español';
  const system = `Eres un profesor de ${meta} que explica el resultado de un diagnóstico adaptativo a un alumno hispanohablante (app OneLingo). Escribe en ${nativo}, sin emojis, en segunda persona, concreto y motivador pero honesto.
Devuelve: "resumen" (3-5 frases: nivel, qué hace bien, dónde falla y por qué no se le baja o sube más), "recomendaciones" (3-5 puntos concretos y accionables sobre lo que debe reforzar, con ejemplos de estructuras), y "plan" (4-6 pasos ordenados para las próximas dos semanas: qué unidades o temas practicar, en qué orden, y qué usar de la app: lecciones, práctica con el tutor, listening).`;
  const user = `Resultado del diagnóstico (JSON): ${JSON.stringify(p.resultado).slice(0, 4000)}`;
  if (geminiDisponible()) {
    try { const r = await conTimeout(generarJsonGemini(system, [{ role: 'user', text: user }], ESQUEMA_PERFIL_GEMINI), GEMINI_MS); return { ...r.json, modelo: r.modelo }; } catch (e) { console.warn('[diagnostico] Gemini falló (perfil), se usa OpenAI:', String(e).slice(0, 120)); if (!openaiDisponible()) throw e; }
  }
  const r = await generarJsonOpenAI(system, [{ role: 'user', content: user }], ESQUEMA_PERFIL_OPENAI);
  return { ...r.json, modelo: r.modelo };
}
