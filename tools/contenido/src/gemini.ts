/** Proveedor Gemini para el pipeline (REST generateContent con responseSchema). */
const ESQUEMA_UNIDAD = {
  type: 'OBJECT',
  properties: {
    titulo: { type: 'STRING' }, objetivo: { type: 'STRING' }, gramatica: { type: 'STRING' },
    vocab: { type: 'ARRAY', items: { type: 'OBJECT', properties: { palabra: { type: 'STRING' }, romanizacion: { type: 'STRING' }, traduccion: { type: 'STRING' }, ejemplo: { type: 'STRING' } }, required: ['palabra', 'romanizacion', 'traduccion', 'ejemplo'] } },
    frases: { type: 'ARRAY', items: { type: 'OBJECT', properties: { texto: { type: 'STRING' }, romanizacion: { type: 'STRING' }, traduccion: { type: 'STRING' } }, required: ['texto', 'romanizacion', 'traduccion'] } },
    dialogo: { type: 'ARRAY', items: { type: 'OBJECT', properties: { quien: { type: 'STRING' }, texto: { type: 'STRING' }, romanizacion: { type: 'STRING' }, traduccion: { type: 'STRING' } }, required: ['quien', 'texto', 'romanizacion', 'traduccion'] } },
    errores_tipicos: { type: 'ARRAY', items: { type: 'OBJECT', properties: { incorrecto: { type: 'STRING' }, correcto: { type: 'STRING' }, explicacion: { type: 'STRING' } }, required: ['incorrecto', 'correcto', 'explicacion'] } },
    examen: { type: 'ARRAY', items: { type: 'OBJECT', properties: { pregunta: { type: 'STRING' }, opciones: { type: 'ARRAY', items: { type: 'STRING' } }, correcta: { type: 'INTEGER' }, explicacion: { type: 'STRING' } }, required: ['pregunta', 'opciones', 'correcta', 'explicacion'] } },
  },
  required: ['titulo', 'objetivo', 'gramatica', 'vocab', 'frases', 'dialogo', 'errores_tipicos', 'examen'],
};

export async function generarUnidadGemini(system: string, prompt: string, modelo: string, apiKey: string): Promise<{ json: unknown; entrada: number; salida: number; modelo: string }> {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelo}:generateContent`;
  const cuerpo = {
    systemInstruction: { parts: [{ text: system }] },
    contents: [{ role: 'user', parts: [{ text: prompt + '\nDevuelve entre 8 y 10 palabras, entre 6 y 8 frases, entre 4 y 8 réplicas, 2-4 errores típicos, 3-4 preguntas con exactamente 4 opciones cada una.' }] }],
    generationConfig: { responseMimeType: 'application/json', responseSchema: ESQUEMA_UNIDAD, temperature: 0.8 },
  };
  let r!: Response, j: any;
  for (let intento = 0; intento < 5; intento++) {
    r = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json', 'x-goog-api-key': apiKey }, body: JSON.stringify(cuerpo) });
    j = await r.json();
    if (r.ok) break;
    if ((r.status === 503 || r.status === 429) && intento < 4) { await new Promise((res) => setTimeout(res, 1500 * (intento + 1))); continue; }
    throw new Error(`Gemini ${r.status}: ${j?.error?.message ?? 'error'}`);
  }
  const texto = j?.candidates?.[0]?.content?.parts?.map((p: any) => p.text ?? '').join('') ?? '';
  if (!texto) throw new Error(`Gemini sin contenido (${j?.candidates?.[0]?.finishReason ?? 'sin candidatos'})`);
  return { json: JSON.parse(texto), entrada: j?.usageMetadata?.promptTokenCount ?? 0, salida: j?.usageMetadata?.candidatesTokenCount ?? 0, modelo: j?.modelVersion ?? modelo };
}
