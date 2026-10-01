/** Proveedor OpenAI: tutor conversacional (Chat Completions con salida JSON estricta) y transcripción de voz. */
import { config } from './config.js';

/** Esquema JSON estricto (Structured Outputs exige additionalProperties:false y todas las claves en required). */
export const ESQUEMA_TUTOR_OPENAI = {
  type: 'object',
  additionalProperties: false,
  properties: {
    reply: { type: 'string', description: 'Respuesta del tutor en el idioma meta, adecuada al nivel' },
    romanizacion: { type: 'string', description: 'Romanización si el idioma no usa alfabeto latino; vacío si no aplica' },
    traduccion: { type: 'string', description: 'Traducción de la respuesta al idioma nativo del alumno' },
    corrections: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          original: { type: 'string' }, correcto: { type: 'string' }, explicacion: { type: 'string' },
          skill: { type: 'string', enum: ['gramatica', 'vocabulario', 'conjugacion', 'listening', 'pronunciacion', 'frases', 'escritura'] },
        },
        required: ['original', 'correcto', 'explicacion', 'skill'],
      },
    },
    suggestions: { type: 'array', items: { type: 'string' }, description: '2-3 respuestas cortas que el alumno podría decir a continuación' },
  },
  required: ['reply', 'romanizacion', 'traduccion', 'corrections', 'suggestions'],
};

export const openaiDisponible = () => config.openaiApiKey.length > 0;

async function conReintentos(hacer: () => Promise<Response>, intentos = 3): Promise<{ r: Response; j: any }> {
  let r!: Response, j: any;
  for (let i = 0; i < intentos; i++) {
    r = await hacer();
    j = await r.json().catch(() => ({}));
    if (r.ok) return { r, j };
    if ((r.status === 429 || r.status >= 500) && i < intentos - 1) { await new Promise((res) => setTimeout(res, 800 * (i + 1))); continue; }
    break;
  }
  throw new Error(`OpenAI ${r.status}: ${j?.error?.message ?? 'error'}`);
}

export async function generarJsonOpenAI(system: string, mensajes: { role: 'user' | 'assistant'; content: string }[], esquema: unknown = ESQUEMA_TUTOR_OPENAI, modelo = config.openaiModelo) {
  const { j } = await conReintentos(() => fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: `Bearer ${config.openaiApiKey}` },
    body: JSON.stringify({
      model: modelo,
      messages: [{ role: 'system', content: system }, ...mensajes],
      response_format: { type: 'json_schema', json_schema: { name: 'respuesta_tutor', strict: true, schema: esquema } },
      temperature: 0.7,
      max_tokens: 700,
    }),
  }));
  const m = j?.choices?.[0]?.message;
  if (m?.refusal) throw new Error(`OpenAI rechazó la petición: ${m.refusal}`);
  const texto: string = m?.content ?? '';
  if (!texto) throw new Error(`OpenAI sin contenido (${j?.choices?.[0]?.finish_reason ?? 'sin candidatos'})`);
  return { json: JSON.parse(texto), modelo: j?.model ?? modelo, entrada: j?.usage?.prompt_tokens ?? 0, salida: j?.usage?.completion_tokens ?? 0 };
}

const LOCALE_ISO: Record<string, string> = { en: 'en', es: 'es', fr: 'fr', de: 'de', pt: 'pt', it: 'it', zh: 'zh', ja: 'ja', ko: 'ko', ru: 'ru' };

/** Transcribe audio (m4a/mp3/wav/webm) al texto en el idioma indicado. */
export async function transcribirOpenAI(audio: Buffer, nombre: string, idioma: string, tipo = 'audio/m4a') {
  const fd = new FormData();
  fd.append('file', new Blob([new Uint8Array(audio)], { type: tipo }), nombre);
  fd.append('model', config.openaiModeloTranscripcion);
  fd.append('response_format', 'json');
  if (LOCALE_ISO[idioma]) fd.append('language', LOCALE_ISO[idioma]);
  const { j } = await conReintentos(() => fetch('https://api.openai.com/v1/audio/transcriptions', {
    method: 'POST', headers: { authorization: `Bearer ${config.openaiApiKey}` }, body: fd,
  }));
  return { texto: String(j?.text ?? '').trim(), modelo: config.openaiModeloTranscripcion };
}

/** Read a completed first JSON string without waiting for the remaining fields. */
export function extraerReply(texto: string): string | undefined {
  const m = /^\s*\{\s*"reply"\s*:\s*("(?:[^"\\]|\\.)*")/s.exec(texto);
  if (!m) return undefined;
  try { return JSON.parse(m[1]); } catch { return undefined; }
}

/**
 * Texto de `reply` ya recibido aunque la cadena JSON aún no se haya cerrado.
 * Se detiene antes de un escape incompleto para no decodificar medio carácter.
 */
export function replyParcial(texto: string): { texto: string; cerrado: boolean } | undefined {
  const m = /^\s*\{\s*"reply"\s*:\s*"/.exec(texto);
  if (!m) return undefined;
  let i = m[0].length, seguro = i;
  for (; i < texto.length; i++) {
    const c = texto[i];
    if (c === '"') { try { return { texto: JSON.parse(texto.slice(m[0].length - 1, i + 1)), cerrado: true }; } catch { return undefined; } }
    if (c === '\\') {
      const largo = texto[i + 1] === 'u' ? 6 : 2;
      if (i + largo > texto.length) break;
      i += largo - 1;
    }
    seguro = i + 1;
  }
  try { return { texto: JSON.parse(texto.slice(m[0].length - 1, seguro) + '"'), cerrado: false }; } catch { return undefined; }
}

const ABREVIATURAS = /(?:^|\s)(?:Mr|Mrs|Ms|Dr|St|Sr|Sra|Dra|etc|e\.g|i\.e|vs|p\.ej|[A-Z])\.$/;
/**
 * Frases terminadas dentro de `texto`: se corta tras . ! ? … (o sus formas
 * CJK) seguidos de espacio, o al final si la cadena está cerrada. Las frases
 * muy cortas («Ok.») se unen a la siguiente para no fragmentar la voz.
 */
export function frasesCompletas(texto: string, cerrado: boolean): string[] {
  const frases: string[] = [];
  let inicio = 0;
  const re = /[.!?…。！？]+["'”’)]*(?=\s)|[。！？]+/g;
  for (let m; (m = re.exec(texto));) {
    const fin = m.index + m[0].length;
    const trozo = texto.slice(inicio, fin).trim();
    if (ABREVIATURAS.test(trozo) || trozo.length < (/[\u3040-\u9fff\uac00-\ud7af]/.test(trozo) ? 4 : 12)) continue;
    frases.push(trozo); inicio = fin;
  }
  if (cerrado) { const resto = texto.slice(inicio).trim(); if (resto) frases.push(resto); }
  return frases;
}

export async function generarTutorStream(system: string, mensajes: { role: 'user' | 'assistant'; content: string }[], onReply: (texto: string) => void, signal: AbortSignal, onFrase?: (texto: string, indice: number) => void) {
  const r = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST', signal,
    headers: { 'content-type': 'application/json', authorization: `Bearer ${config.openaiApiKey}` },
    body: JSON.stringify({ model: config.openaiModelo,
      messages: [{ role: 'system', content: system + '\nEscribe reply primero; máximo 600 caracteres y una primera respuesta breve.' }, ...mensajes],
      response_format: { type: 'json_schema', json_schema: { name: 'respuesta_tutor', strict: true, schema: ESQUEMA_TUTOR_OPENAI } },
      temperature: 0.7, max_tokens: 700, stream: true, stream_options: { include_usage: true } }),
  });
  if (!r.ok || !r.body) throw new Error(`OpenAI ${r.status}`);
  const reader = r.body.getReader(); const decoder = new TextDecoder();
  let pending = '', texto = '', enviado = false, done = false, frasesEnviadas = 0;
  let modelo = config.openaiModelo, entrada = 0, salida = 0;
  try {
    while (true) {
      const next = await reader.read();
      pending += decoder.decode(next.value, { stream: !next.done });
      let end: number;
      while ((end = pending.indexOf('\n')) >= 0) {
        const line = pending.slice(0, end).trim(); pending = pending.slice(end + 1);
        if (!line.startsWith('data:')) continue;
        const data = line.slice(5).trim();
        if (data === '[DONE]') { done = true; continue; }
        const j = JSON.parse(data);
        if (j.error || j.choices?.[0]?.delta?.refusal) throw new Error('Respuesta rechazada');
        modelo = j.model ?? modelo;
        if (j.usage) { entrada = j.usage.prompt_tokens; salida = j.usage.completion_tokens; }
        texto += j.choices?.[0]?.delta?.content ?? '';
        // La voz arranca con la primera frase terminada, sin esperar al resto de la respuesta.
        if (onFrase && !enviado) {
          const parcial = replyParcial(texto);
          if (parcial) for (const f of frasesCompletas(parcial.texto, parcial.cerrado).slice(frasesEnviadas)) onFrase(f, frasesEnviadas++);
        }
        if (!enviado) {
          const reply = extraerReply(texto);
          if (reply?.trim() && reply.length <= 600) { enviado = true; onReply(reply); }
        }
      }
      if (next.done) break;
    }
    if (!done) throw new Error('Respuesta interrumpida');
    return { json: JSON.parse(texto), modelo, entrada, salida };
  } finally { await reader.cancel().catch(() => {}); reader.releaseLock(); }
}
