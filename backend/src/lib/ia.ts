import Anthropic from '@anthropic-ai/sdk';
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';
import { z } from 'zod/v4';
import { config } from './config.js';
import { generarJsonGemini, geminiDisponible } from './ia_gemini.js';
import { generarJsonOpenAI, generarTutorStream, openaiDisponible } from './ia_openai.js';

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
  "avatar_amara": "Amara: paciente y cercano; haz una pregunta por turno, explica los errores con ejemplos breves y adapta la conversación a las prioridades del alumno.",
  "avatar_sofia": "Sofía: paciente y cercano; haz una pregunta por turno, explica los errores con ejemplos breves y adapta la conversación a las prioridades del alumno.",
  "avatar_lucia": "Lucía: paciente y cercano; haz una pregunta por turno, explica los errores con ejemplos breves y adapta la conversación a las prioridades del alumno.",
  "avatar_clara": "Clara: paciente y cercano; haz una pregunta por turno, explica los errores con ejemplos breves y adapta la conversación a las prioridades del alumno.",
  "avatar_mei": "Mei: paciente y cercano; haz una pregunta por turno, explica los errores con ejemplos breves y adapta la conversación a las prioridades del alumno.",
  "avatar_malik": "Malik: paciente y cercano; haz una pregunta por turno, explica los errores con ejemplos breves y adapta la conversación a las prioridades del alumno.",
  "avatar_mateo": "Mateo: paciente y cercano; haz una pregunta por turno, explica los errores con ejemplos breves y adapta la conversación a las prioridades del alumno.",
  "avatar_owen": "Owen: paciente y cercano; haz una pregunta por turno, explica los errores con ejemplos breves y adapta la conversación a las prioridades del alumno.",
  "avatar_daniel": "Daniel: paciente y cercano; haz una pregunta por turno, explica los errores con ejemplos breves y adapta la conversación a las prioridades del alumno.",
  "avatar_kenji": "Kenji: paciente y cercano; haz una pregunta por turno, explica los errores con ejemplos breves y adapta la conversación a las prioridades del alumno.",
  mia: 'Mia: amigable, paciente y cálida; anima mucho y corrige con suavidad.',
  leo: 'Leo: motivador y enérgico; celebra los aciertos y reta al alumno a decir un poco más.',
  sofia: 'Sofía: profesional y precisa; correcciones claras, registro formal, ejemplos de trabajo.',
  max: 'Max: directo y conciso; va al grano, corrige sin rodeos y no repite lo obvio.',
};
export function perfilNivel(n: number): string {
  if (n < 1) return 'Nivel 0 (Pre-A1): fundamentos, palabras y expresiones muy sencillas con apoyo.';
  if (n <= 2) return 'Niveles 1-2 (A1): expresiones cotidianas básicas, presentación personal y preguntas sencillas. Una pregunta por turno.';
  if (n <= 4) return 'Niveles 3-4 (A2): intercambios habituales, necesidades concretas, experiencias sencillas y planes.';
  if (n <= 6) return 'Niveles 5-6 (B1): temas familiares, relatos conectados, razones y opiniones con claridad.';
  if (n <= 8) return 'Niveles 7-8 (B2): argumentos claros, textos complejos, comparación de alternativas y comprensión de puntos de vista.';
  return 'Niveles 9-10 (C1): matices e información implícita, argumentos estructurados, flexibilidad de registro y precisión. No equivale a certificación.';
}

export const iaDisponible = () =>
  config.iaProveedor === 'openai' ? openaiDisponible() : config.iaProveedor === 'gemini' ? geminiDisponible() : config.anthropicApiKey.length > 0;
export const iaNombre = () =>
  config.iaProveedor === 'openai' ? config.openaiModelo : config.iaProveedor === 'gemini' ? config.geminiModelo : config.iaModelo;
const cliente = () => new Anthropic({ apiKey: config.anthropicApiKey });

export type Turno = { rol: 'tutor' | 'alumno'; texto: string };

export function systemPrompt(p: { idiomaMeta: string; idiomaNativo: string; nivel: number; tutorId: string; situacion?: string; objetivo?: string; contexto?: string }) {
  return `Eres ${TUTORES[p.tutorId] ?? TUTORES.mia}
Eres tutor de ${IDIOMAS[p.idiomaMeta] ?? p.idiomaMeta} en la app OneLingo para un alumno cuyo idioma nativo es ${IDIOMAS[p.idiomaNativo] ?? p.idiomaNativo}.
Perfil del alumno: ${perfilNivel(p.nivel)}
${p.situacion ? `Situación de práctica: "${p.situacion}". Interpreta el rol correspondiente (camarero, médico, recepcionista, entrevistador…) y mantén la escena viva.` : 'Conversación libre: sigue el tema que proponga el alumno y hazle preguntas.'}
${p.objetivo ? `Objetivo pedagógico de la situación: ${p.objetivo}` : ''}
${p.contexto ?? ''}
Reglas:
- Responde SIEMPRE en ${IDIOMAS[p.idiomaMeta] ?? p.idiomaMeta}; nunca en el idioma nativo salvo en 'traduccion' y en las explicaciones de 'corrections'.
- Ajusta longitud, vocabulario y velocidad al nivel; en niveles 1-3 usa frases muy cortas.
- Corrige solo errores reales del último mensaje del alumno (gramática, vocabulario, conjugación, orden de palabras); nunca inventes errores. Si el mensaje está en el idioma nativo, invítalo amablemente a intentarlo en el idioma meta y sugiere cómo.
- ${ROM[p.idiomaMeta] ? `Incluye la romanización (${ROM[p.idiomaMeta]}) en 'romanizacion'.` : "Deja 'romanizacion' vacío."}
- Sin emojis. Sé breve: 1-3 frases por turno.`;
}

export async function responder(p: { idiomaMeta: string; idiomaNativo: string; nivel: number; tutorId: string; situacion?: string; objetivo?: string; contexto?: string; historial: Turno[] }, onReply?: (texto: string) => void, signal?: AbortSignal) {
  if (config.iaProveedor === 'openai') {
    const mensajes = p.historial.map((t) => ({ role: (t.rol === 'alumno' ? 'user' : 'assistant') as 'user' | 'assistant', content: t.texto }));
    if (mensajes.length === 0 || mensajes[0].role !== 'user') mensajes.unshift({ role: 'user', content: '(El alumno abre la conversación. Saluda y empieza la situación.)' });
    const r = onReply && signal
      ? await generarTutorStream(systemPrompt(p), mensajes, onReply, signal)
      : await generarJsonOpenAI(systemPrompt(p), mensajes);
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
