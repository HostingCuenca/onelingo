import { test } from 'node:test';
import assert from 'node:assert/strict';
import { config } from '../src/lib/config.js';
import { pool } from '../src/lib/db.js';
const originalFetch = globalThis.fetch;
const sse = (...partes: string[]) => new Response(new ReadableStream({ start(c) {
  const enc = new TextEncoder();
  for (const p of partes) c.enqueue(enc.encode(`data: ${JSON.stringify({ choices: [{ delta: { content: p } }] })}\n\n`));
  c.enqueue(enc.encode('data: [DONE]\n\n')); c.close();
} }));
const RESTO = '"romanizacion":"","traduccion":"","corrections":[],"suggestions":["Yes"]}';

async function montar() {
  const { default: Fastify } = await import('fastify');
  const { default: jwt } = await import('@fastify/jwt');
  const { default: multipart } = await import('@fastify/multipart');
  const { default: routes } = await import('../src/routes/chat.js');
  const app = Fastify(); await app.register(jwt, { secret: 'test-only-voz-secret' }); await app.register(multipart); await app.register(routes);
  return app;
}

test('/chat/voz: transcribe, emits the transcript first and answers with the new turn in history', async () => {
  const app = await montar();
  const prev = { p: config.iaProveedor, k: config.openaiApiKey }; config.iaProveedor = 'openai'; config.openaiApiKey = 'test';
  const query = pool.query; (pool as any).query = async () => ({ rows: [] });
  let historialEnviado: any[] = [];
  globalThis.fetch = async (url, options) => {
    const u = String(url);
    if (u.includes('/audio/transcriptions')) return Response.json({ text: 'I like to read books.' });
    if (u.includes('/chat/completions')) { historialEnviado = JSON.parse(String(options?.body)).messages; return sse('{"reply":"Me too! What book', ' are you reading?",', RESTO); }
    return originalFetch(url, options);
  };
  try {
    const address = await app.listen({ host: '127.0.0.1', port: 0 });
    const form = new FormData();
    form.append('datos', JSON.stringify({ idiomaMeta: 'en', nivel: 1, tutorId: 'avatar_lumo', historial: [{ rol: 'tutor', texto: 'What do you like to do?' }] }));
    form.append('audio', new Blob([new Uint8Array(2000)], { type: 'audio/webm' }), 'turno.webm');
    const r = await originalFetch(address + '/chat/voz', { method: 'POST', headers: { authorization: `Bearer ${app.jwt.sign({ sub: 'test', rol: 'alumno' })}` }, body: form });
    const texto = await r.text();
    const eventos = texto.split('\n\n').filter(l => l.startsWith('data: ')).map(l => JSON.parse(l.slice(6)));
    assert.deepEqual(eventos[0], { tipo: 'transcripcion', data: { texto: 'I like to read books.' } });
    assert.ok(eventos.some(e => e.tipo === 'frase'));
    assert.equal(eventos.at(-1).tipo, 'final');
    assert.equal(historialEnviado.at(-1).content, 'I like to read books.');
    const sinAudio = new FormData(); sinAudio.append('datos', '{}');
    assert.equal((await originalFetch(address + '/chat/voz', { method: 'POST', headers: { authorization: `Bearer ${app.jwt.sign({ sub: 'test', rol: 'alumno' })}` }, body: sinAudio })).status, 400);
  } finally { globalThis.fetch = originalFetch; config.iaProveedor = prev.p; config.openaiApiKey = prev.k; pool.query = query; await app.close(); }
});

test('/chat retries once when the provider fails before emitting anything', async () => {
  const app = await montar();
  const prev = { p: config.iaProveedor, k: config.openaiApiKey }; config.iaProveedor = 'openai'; config.openaiApiKey = 'test';
  const query = pool.query; (pool as any).query = async () => ({ rows: [] });
  let llamadas = 0;
  globalThis.fetch = async (url, options) => {
    if (!String(url).includes('/chat/completions')) return originalFetch(url, options);
    llamadas++;
    if (llamadas === 1) return new Response(new ReadableStream({ start(c) { c.enqueue(new TextEncoder().encode(`data: ${JSON.stringify({ error: { message: 'temporal' } })}\n\n`)); c.close(); } }));
    return sse('{"reply":"Hello there, friend!",', RESTO);
  };
  try {
    const address = await app.listen({ host: '127.0.0.1', port: 0 });
    const r = await originalFetch(address + '/chat', { method: 'POST', headers: { authorization: `Bearer ${app.jwt.sign({ sub: 'test', rol: 'alumno' })}`, 'content-type': 'application/json', accept: 'text/event-stream' }, body: JSON.stringify({ idiomaMeta: 'en', nivel: 1, historial: [{ rol: 'alumno', texto: 'Hi' }] }) });
    const texto = await r.text();
    assert.equal(llamadas, 2);
    assert.match(texto, /"tipo":"final"/);
    assert.doesNotMatch(texto, /"tipo":"error"/);
  } finally { globalThis.fetch = originalFetch; config.iaProveedor = prev.p; config.openaiApiKey = prev.k; pool.query = query; await app.close(); }
});
