import { test } from 'node:test';
import assert from 'node:assert/strict';
import { frasesCompletas, generarTutorStream, replyParcial } from '../src/lib/ia_openai.js';
import { resumirHechos } from '../src/lib/situaciones.js';
import { systemPrompt } from '../src/lib/ia.js';
const originalFetch = globalThis.fetch;
const encoder = new TextEncoder();
const event = (j: unknown) => encoder.encode(`data: ${JSON.stringify(j)}\n\n`);

test('partial reply decodes open strings and stops before half escapes', () => {
  assert.deepEqual(replyParcial('{"reply":"Hello there. How'), { texto: 'Hello there. How', cerrado: false });
  assert.deepEqual(replyParcial('{"reply":"Say \\"hi\\".","x":1'), { texto: 'Say "hi".', cerrado: true });
  assert.deepEqual(replyParcial('{"reply":"Caf\\u00'), { texto: 'Caf', cerrado: false });
  assert.deepEqual(replyParcial('{"reply":"a\\'), { texto: 'a', cerrado: false });
  assert.equal(replyParcial('{"corrections":[]'), undefined);
});

test('sentences split only when finished; short ones and abbreviations merge', () => {
  assert.deepEqual(frasesCompletas('Great job today! What did you', false), ['Great job today!']);
  assert.deepEqual(frasesCompletas('Ok. That sounds lovely. And you?', true), ['Ok. That sounds lovely.', 'And you?']);
  assert.deepEqual(frasesCompletas('I met Mr. Smith at the station. Nice', false), ['I met Mr. Smith at the station.']);
  assert.deepEqual(frasesCompletas('今日はいい天気ですね。散歩しましょう', true), ['今日はいい天気ですね。', '散歩しましょう']);
  // Stable as text grows: earlier sentences never change.
  const full = 'That is a great question! Let me think about it. What do you prefer?';
  let seen: string[] = [];
  for (let i = 1; i <= full.length; i++) {
    const now = frasesCompletas(full.slice(0, i), i === full.length);
    assert.deepEqual(now.slice(0, seen.length), seen); seen = now;
  }
  assert.equal(seen.join(' '), full);
});

test('stream emits each sentence before the reply is complete', async () => {
  let emit!: ReadableStreamDefaultController<Uint8Array>;
  globalThis.fetch = async () => new Response(new ReadableStream({ start(c) { emit = c; } }));
  const frases: string[] = []; let reply = '';
  try {
    const result = generarTutorStream('t', [], t => { reply = t; }, new AbortController().signal, (f, i) => { assert.equal(i, frases.length); frases.push(f); });
    await Promise.resolve();
    emit.enqueue(event({ choices: [{ delta: { content: '{"reply":"Nice to meet you, Ana! Where' } }] }));
    await new Promise(r => setTimeout(r, 5));
    assert.deepEqual(frases, ['Nice to meet you, Ana!']); assert.equal(reply, '');
    emit.enqueue(event({ choices: [{ delta: { content: ' do you live?","romanizacion":"","traduccion":"","corrections":[],"suggestions":[]}' } }] }));
    emit.enqueue(encoder.encode('data: [DONE]\n\n')); emit.close();
    await result;
    assert.deepEqual(frases, ['Nice to meet you, Ana!', 'Where do you live?']);
    assert.equal(reply, 'Nice to meet you, Ana! Where do you live?');
  } finally { globalThis.fetch = originalFetch; }
});

test('learner facts are bounded data and video-call rules only for avatars', () => {
  const hechos = resumirHechos([{ fecha: '2026-09-30T10:00:00Z', datos: { hechos: ['Trabaja como enfermera', 'x'.repeat(500)], mejorar: [{ correcto: 'I went' }], siguientePaso: 'Practicar el pasado' } }]);
  const parsed = JSON.parse(hechos);
  assert.equal(parsed[0].fecha, '2026-09-30'); assert.equal(parsed[0].hechos[1].length, 160);
  assert.deepEqual(parsed[0].aMejorar, ['I went']);
  const base = { idiomaMeta: 'en', idiomaNativo: 'es', nivel: 3 };
  assert.match(systemPrompt({ ...base, tutorId: 'avatar_lumo' }), /Lumo[\s\S]*VIDEOLLAMADA/);
  assert.doesNotMatch(systemPrompt({ ...base, tutorId: 'mia' }), /VIDEOLLAMADA/);
  assert.notEqual(systemPrompt({ ...base, tutorId: 'avatar_amara' }), systemPrompt({ ...base, tutorId: 'avatar_sofia' }).replace('Sofía', 'Amara'));
});
