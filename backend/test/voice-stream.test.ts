import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readdir, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { extraerReply, generarTutorStream } from '../src/lib/ia_openai.js';
import { obtenerAudioStream } from '../src/lib/voz.js';
import { config } from '../src/lib/config.js';
import { pool } from '../src/lib/db.js';
const originalFetch = globalThis.fetch;
const encoder = new TextEncoder();
const event = (j: unknown) => encoder.encode(`data: ${JSON.stringify(j)}\n\n`);

test('reply parser waits for closing string and handles escaped quotes/unicode', () => {
  assert.equal(extraerReply('{"reply":"hel'), undefined);
  assert.equal(extraerReply('{"reply":"Hi \\"'), undefined);
  const text = 'Say "hello". Café ☕';
  assert.equal(extraerReply('{"reply":' + JSON.stringify(text) + ',"corrections":['), text);
  assert.equal(extraerReply('{"corrections":[{"reply":"wrong"}]}'), undefined);
});

test('one LLM request emits reply before metadata; rejects interrupted SSE', async () => {
  let emit!: ReadableStreamDefaultController<Uint8Array>;
  let early!: () => void; const ready = new Promise<void>(r => early = r);
  let calls = 0;
  globalThis.fetch = async (_url, init) => {
    calls++; const body = JSON.parse(String(init?.body));
    assert.equal(body.stream, true);
    return new Response(new ReadableStream({ start(c) { emit = c; } }));
  };
  try {
    const result = generarTutorStream('test', [], t => { assert.equal(t, 'Hello!'); early(); }, new AbortController().signal);
    await Promise.resolve();
    const first = event({ choices: [{ delta: { content: '{"reply":"Hello!",' } }] });
    // Deliberately split the SSE framing across network packets.
    emit.enqueue(first.slice(0, 11)); emit.enqueue(first.slice(11));
    await ready;
    emit.enqueue(event({ choices: [{ delta: { content: '"corrections":[]}' } }] }));
    emit.enqueue(event({ choices: [], usage: { prompt_tokens: 10, completion_tokens: 20 } }));
    emit.enqueue(encoder.encode('data: [DONE]\n\n')); emit.close();
    assert.equal((await result).salida, 20); assert.equal(calls, 1);
    const interrupted = generarTutorStream('test', [], () => {}, new AbortController().signal);
    await Promise.resolve(); emit.enqueue(event({ choices: [{ delta: { content: '{"reply":"Hi"}' } }] })); emit.close();
    await assert.rejects(interrupted, /interrumpida/);
  } finally { globalThis.fetch = originalFetch; }
});

test('TTS delivers first bytes before EOF and caches only completed audio', async () => {
  const dir = await mkdtemp(`${tmpdir()}/onelingo-voice-`);
  const previousDir = config.audioDir; config.audioDir = dir;
  const query = pool.query; (pool as any).query = async () => ({ rows: [] });
  let upstream!: ReadableStreamDefaultController<Uint8Array>;
  let requests = 0;
  globalThis.fetch = async (url) => {
    assert.match(String(url), /\/stream\?output_format=/); requests++;
    return new Response(new ReadableStream({ start(c) { upstream = c; } }));
  };
  try {
    const audio = await obtenerAudioStream({ texto: 'Hello test', idioma: 'en' }, new AbortController().signal, () => {});
    const iter = audio.stream[Symbol.asyncIterator]();
    const first = iter.next(); upstream.enqueue(encoder.encode('first'));
    assert.equal((await first).value.toString(), 'first');
    assert.deepEqual(await readdir(dir), []);
    upstream.enqueue(encoder.encode('last')); upstream.close();
    for await (const _ of { [Symbol.asyncIterator]: () => iter }) { /* drain */ }
    const cached = await obtenerAudioStream({ texto: 'Hello test', idioma: 'en' }, new AbortController().signal, () => {});
    assert.equal(cached.cache, true); assert.equal(requests, 1);
    const other = await obtenerAudioStream({ texto: 'Interrupted test', idioma: 'en' }, new AbortController().signal, () => {});
    const it = other.stream[Symbol.asyncIterator](); const chunk = it.next(); upstream.enqueue(encoder.encode('partial')); await chunk;
    upstream.error(new Error('disconnected'));
    await assert.rejects(it.next());
    assert.equal((await readdir(dir)).filter(f => f.endsWith('.mp3')).length, 1);
  } finally { globalThis.fetch = originalFetch; config.audioDir = previousDir; pool.query = query; await rm(dir, { recursive: true }); }
});

test('HTTP chat flushes early reply before provider completes and keeps JSON compatibility', async () => {
  const { default: Fastify } = await import('fastify');
  const { default: jwt } = await import('@fastify/jwt');
  const { default: routes } = await import('../src/routes/chat.js');
  const app = Fastify(); await app.register(jwt, { secret: 'test-only-stream-secret' }); await app.register(routes);
  const provider = config.iaProveedor, key = config.openaiApiKey;
  config.iaProveedor = 'openai'; config.openaiApiKey = 'test';
  const query = pool.query; (pool as any).query = async () => ({ rows: [] });
  let upstream!: ReadableStreamDefaultController<Uint8Array>;
  let invoked!: () => void; const request = new Promise<void>(r => invoked = r);
  globalThis.fetch = async (url, options) => {
    if (!String(url).includes('api.openai.com')) return originalFetch(url, options);
    if (!JSON.parse(String(options?.body)).stream) return Response.json({ choices: [{ message: { content: JSON.stringify({ reply: 'Hello!', romanizacion: '', traduccion: 'Hola', corrections: [], suggestions: ['Hi', 'Hello'] }) } }], usage: {} });
    const response = new Response(new ReadableStream({ start(c) { upstream = c; } })); invoked(); return response;
  };
  try {
    const address = await app.listen({ host: '127.0.0.1', port: 0 });
    const pending = originalFetch(address + '/chat', { method: 'POST', headers: { authorization: `Bearer ${app.jwt.sign({ sub: 'test', rol: 'alumno' })}`, 'content-type': 'application/json', accept: 'text/event-stream' }, body: JSON.stringify({ idiomaMeta: 'en', nivel: 1, historial: [{ rol: 'alumno', texto: 'Hi' }] }) });
    await request;
    upstream.enqueue(event({ choices: [{ delta: { content: '{"reply":"Hello!",' } }] }));
    const response = await pending; assert.equal(response.status, 200);
    const reader = response.body!.getReader();
    assert.match(new TextDecoder().decode((await reader.read()).value), /"tipo":"reply"/);
    upstream.enqueue(event({ choices: [{ delta: { content: '"romanizacion":"","traduccion":"Hola","corrections":[],"suggestions":["Hi","Hello"]}' } }] }));
    upstream.enqueue(encoder.encode('data: [DONE]\n\n')); upstream.close();
    let rest = ''; while (true) { const n = await reader.read(); if (n.done) break; rest += new TextDecoder().decode(n.value); }
    assert.match(rest, /"tipo":"final"/);
    const legacy = await app.inject({ method: 'POST', url: '/chat', headers: { authorization: `Bearer ${app.jwt.sign({ sub: 'test', rol: 'alumno' })}` }, payload: { idiomaMeta: 'en', nivel: 1, historial: [{ rol: 'alumno', texto: 'Hi' }] } });
    assert.equal(legacy.statusCode, 200); assert.equal(legacy.json().reply, 'Hello!');
    assert.equal((await app.inject({ method: 'POST', url: '/chat', payload: {} })).statusCode, 401);
  } finally { globalThis.fetch = originalFetch; config.iaProveedor = provider; config.openaiApiKey = key; pool.query = query; await app.close(); }
});
