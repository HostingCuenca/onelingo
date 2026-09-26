/** Proveedor Gemini (REST generateContent con salida JSON estructurada). */
import { config } from './config.js';

const ESQUEMA_TUTOR = {
  type: 'OBJECT',
  properties: {
    reply: { type: 'STRING', description: 'Respuesta del tutor en el idioma meta, adecuada al nivel' },
    romanizacion: { type: 'STRING', description: 'Romanización si el idioma no usa alfabeto latino; vacío si no aplica' },
    traduccion: { type: 'STRING', description: 'Traducción de la respuesta al idioma nativo del alumno' },
    corrections: {
      type: 'ARRAY',
      items: {
        type: 'OBJECT',
        properties: {
          original: { type: 'STRING' }, correcto: { type: 'STRING' }, explicacion: { type: 'STRING' },
          skill: { type: 'STRING', enum: ['gramatica', 'vocabulario', 'conjugacion', 'listening', 'pronunciacion', 'frases', 'escritura'] },
        },
        required: ['original', 'correcto', 'explicacion', 'skill'],
      },
    },
    suggestions: { type: 'ARRAY', items: { type: 'STRING' }, description: '2-3 respuestas cortas que el alumno podría decir a continuación' },
  },
  required: ['reply', 'romanizacion', 'traduccion', 'corrections', 'suggestions'],
};

export const geminiDisponible = () => config.geminiApiKey.length > 0;

let cuotaBloqueadaHasta = 0;

export async function generarJsonGemini(system: string, turnos: { role: 'user' | 'model'; text: string }[], esquema: unknown = ESQUEMA_TUTOR, modelo = config.geminiModelo) {
  if (Date.now() < cuotaBloqueadaHasta) throw new Error('Gemini: cuota temporalmente agotada');
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelo}:generateContent`;
  const cuerpo = {
    systemInstruction: { parts: [{ text: system }] },
    contents: turnos.map((t) => ({ role: t.role, parts: [{ text: t.text }] })),
    generationConfig: { responseMimeType: 'application/json', responseSchema: esquema, temperature: 0.7 },
  };
  let r!: Response, j: any;
  for (let intento = 0; intento < 4; intento++) {
    r = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json', 'x-goog-api-key': config.geminiApiKey }, body: JSON.stringify(cuerpo), signal: AbortSignal.timeout(12000) });
    j = await r.json();
    if (r.ok) break;
    if (r.status === 429) { cuotaBloqueadaHasta = Date.now() + 90000; throw new Error('Gemini 429: cuota agotada; usar respaldo'); }
    // 503 (alta demanda) y 429 (cuota): reintento con espera creciente.
    if ((r.status === 503 || r.status === 429) && intento < 3) { await new Promise((res) => setTimeout(res, 800 * (intento + 1))); continue; }
    throw new Error(`Gemini ${r.status}: ${j?.error?.message ?? 'error'}`);
  }
  const texto = j?.candidates?.[0]?.content?.parts?.map((p: any) => p.text ?? '').join('') ?? '';
  if (!texto) throw new Error(`Gemini sin contenido (${j?.candidates?.[0]?.finishReason ?? 'sin candidatos'})`);
  return { json: JSON.parse(texto), modelo: j?.modelVersion ?? modelo, entrada: j?.usageMetadata?.promptTokenCount ?? 0, salida: j?.usageMetadata?.candidatesTokenCount ?? 0 };
}
