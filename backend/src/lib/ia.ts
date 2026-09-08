import Anthropic from '@anthropic-ai/sdk';
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';
import { z } from 'zod/v4';
import { config } from './config.js';
import { generarJsonGemini, geminiDisponible } from './ia_gemini.js';
import { generarJsonOpenAI, openaiDisponible } from './ia_openai.js';

export const RespuestaTutor = z.object({
  reply: z.string().describe('Respuesta del tutor en el idioma meta, adecuada al nivel'),
  romanizacion: z.string().describe('Romanización de la respuesta si el idioma no usa alfabeto latino; vacío si no aplica'),
  traduccion: z.string().describe('Traducción de la respuesta al idioma nativo del alumno'),
  corrections: z.array(z.object({
    original: z.string(), correcto: z.string(), explicacion: z.string().describe('Explicación breve en el idioma nativo del alumno'),
    skill: z.enum(['gramatica', 'vocabulario', 'conjugacion', 'listening', 'pronunciacion', 'frases', 'escritura']),
  })).describe('Errores del último mensaje del alumno; vacío si estaba bien'),
  suggestions: z.array(z.string()).min(2).max(3).describe('Respuestas cortas que el alumno podría decir a continuación, en el idioma meta'),
});
export type RespuestaTutor = z.infer<typeof RespuestaTutor>;

const IDIOMAS: Record<string, string> = { en: 'inglés', es: 'español', fr: 'francés', de: 'alemán', pt: 'portugués', it: 'italiano', zh: 'chino mandarín', ja: 'japonés', ko: 'coreano', ru: 'ruso' };
const ROM: Record<string, string> = { zh: 'pinyin con tonos', ja: 'romaji Hepburn', ko: 'romanización revisada', ru: 'transliteración latina' };
const TUTORES: Record<string, string> = {
  mia: 'Mia: amigable, paciente y cálida; anima mucho y corrige con suavidad.',
  leo: 'Leo: motivador y enérgico; celebra los aciertos y reta al alumno a decir un poco más.',
  sofia: 'Sofía: profesional y precisa; correcciones claras, registro formal, ejemplos de trabajo.',
  max: 'Max: directo y conciso; va al grano, corrige sin rodeos y no repite lo obvio.',
};
export function perfilNivel(n: number): string {
  if (n <= 2) return 'Nivel 1-2 (A1): frases de 3-8 palabras, presente simple, vocabulario de 300-600 palabras muy frecuentes, habla despacio, una pregunta por turno, repite las palabras clave.';
  if (n === 3) return 'Nivel 3 (A2): frases cortas, pasado simple y futuro básico, vocabulario cotidiano de ~1 000 palabras, pide detalles sencillos.';
  if (n <= 5) return 'Nivel 4-5 (B1): conversación natural pero clara, todos los tiempos básicos, condicional, ~2 000 palabras, pide opiniones y explicaciones.';
  if (n <= 7) return 'Nivel 6-7 (B2): conversación fluida, expresiones idiomáticas comunes, phrasal verbs/equivalentes, introduce imprevistos y matices, exige respuestas más largas.';
  if (n <= 9) return 'Nivel 8-9 (C1): lenguaje natural y rico, ironía, registro variable, argumentación, debate; corrige matices y colocaciones.';
  return 'Nivel 10 (C2): dominio; habla como un nativo culto a velocidad normal, con humor, referencias culturales y situaciones inesperadas.';
}

export const iaDisponible = () =>
  config.iaProveedor === 'openai' ? openaiDisponible() : config.iaProveedor === 'gemini' ? geminiDisponible() : config.anthropicApiKey.length > 0;
export const iaNombre = () =>
  config.iaProveedor === 'openai' ? config.openaiModelo : config.iaProveedor === 'gemini' ? config.geminiModelo : config.iaModelo;
const cliente = () => new Anthropic({ apiKey: config.anthropicApiKey });

export type Turno = { rol: 'tutor' | 'alumno'; texto: string };

export function systemPrompt(p: { idiomaMeta: string; idiomaNativo: string; nivel: number; tutorId: string; situacion?: string; objetivo?: string }) {
  return `Eres ${TUTORES[p.tutorId] ?? TUTORES.mia}
Eres tutor de ${IDIOMAS[p.idiomaMeta] ?? p.idiomaMeta} en la app OneLingo para un alumno cuyo idioma nativo es ${IDIOMAS[p.idiomaNativo] ?? p.idiomaNativo}.
Perfil del alumno: ${perfilNivel(p.nivel)}
${p.situacion ? `Situación de práctica: "${p.situacion}". Interpreta el rol correspondiente (camarero, médico, recepcionista, entrevistador…) y mantén la escena viva.` : 'Conversación libre: sigue el tema que proponga el alumno y hazle preguntas.'}
${p.objetivo ? `Objetivo pedagógico de la situación: ${p.objetivo}` : ''}
Reglas:
- Responde SIEMPRE en ${IDIOMAS[p.idiomaMeta] ?? p.idiomaMeta}; nunca en el idioma nativo salvo en 'traduccion' y en las explicaciones de 'corrections'.
- Ajusta longitud, vocabulario y velocidad al nivel; en niveles 1-3 usa frases muy cortas.
- Corrige solo errores reales del último mensaje del alumno (gramática, vocabulario, conjugación, orden de palabras); nunca inventes errores. Si el mensaje está en el idioma nativo, invítalo amablemente a intentarlo en el idioma meta y sugiere cómo.
- ${ROM[p.idiomaMeta] ? `Incluye la romanización (${ROM[p.idiomaMeta]}) en 'romanizacion'.` : "Deja 'romanizacion' vacío."}
- Sin emojis. Sé breve: 1-3 frases por turno.`;
}

export async function responder(p: { idiomaMeta: string; idiomaNativo: string; nivel: number; tutorId: string; situacion?: string; objetivo?: string; historial: Turno[] }) {
  if (config.iaProveedor === 'openai') {
    const mensajes = p.historial.map((t) => ({ role: (t.rol === 'alumno' ? 'user' : 'assistant') as 'user' | 'assistant', content: t.texto }));
    if (mensajes.length === 0 || mensajes[0].role !== 'user') mensajes.unshift({ role: 'user', content: '(El alumno abre la conversación. Saluda y empieza la situación.)' });
    const r = await generarJsonOpenAI(systemPrompt(p), mensajes);
    const parsed = RespuestaTutor.parse({ ...r.json, suggestions: (r.json.suggestions ?? []).slice(0, 3) });
    return { respuesta: parsed, modelo: r.modelo, entrada: r.entrada, salida: r.salida };
  }
  if (config.iaProveedor === 'gemini') {
    const turnos = p.historial.map((t) => ({ role: (t.rol === 'alumno' ? 'user' : 'model') as 'user' | 'model', text: t.texto }));
    if (turnos.length === 0 || turnos[0].role !== 'user') turnos.unshift({ role: 'user', text: '(El alumno abre la conversación. Saluda y empieza la situación.)' });
    const r = await generarJsonGemini(systemPrompt(p), turnos);
    const parsed = RespuestaTutor.parse({ ...r.json, suggestions: (r.json.suggestions ?? []).slice(0, 3) });
    return { respuesta: parsed, modelo: r.modelo, entrada: r.entrada, salida: r.salida };
  }
  const c = cliente();
  const mensajes: Anthropic.MessageParam[] = p.historial.map((t) => ({ role: t.rol === 'alumno' ? 'user' : 'assistant', content: t.texto }));
  if (mensajes.length === 0 || mensajes[0].role !== 'user') mensajes.unshift({ role: 'user', content: '(El alumno abre la conversación. Saluda y empieza la situación.)' });
  const r = await c.messages.parse({
    model: config.iaModelo,
    max_tokens: 4096,
    system: [{ type: 'text', text: systemPrompt(p), cache_control: { type: 'ephemeral' } }],
    messages: mensajes,
    output_config: { format: zodOutputFormat(RespuestaTutor), effort: 'low' },
  });
  if (r.stop_reason === 'refusal' || !r.parsed_output) throw new Error('La IA no devolvió una respuesta válida');
  return { respuesta: r.parsed_output, modelo: r.model, entrada: r.usage.input_tokens + (r.usage.cache_read_input_tokens ?? 0), salida: r.usage.output_tokens };
}
