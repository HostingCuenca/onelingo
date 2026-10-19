import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { obtenerAudio, obtenerAudioStream, hashAudio, hashAudioLegado, textoParaVoz, VOCES, rolDeVoz } from '../src/lib/voz.js';
import { config } from '../src/lib/config.js';
import { pool } from '../src/lib/db.js';

const originalFetch = globalThis.fetch;

/** ElevenLabs simulado: devuelve el texto pedido como «audio» y guarda los cuerpos. */
async function conMock(fn: (cuerpos: any[], dir: string, filas: { sql: string; params: any[] }[]) => Promise<void>) {
  const dir = await mkdtemp(`${tmpdir()}/onelingo-trozos-`);
  const prev = { dir: config.audioDir, key: config.elevenApiKey, max: config.vozMaxCaracteres };
  config.audioDir = dir; config.elevenApiKey = 'test'; config.vozMaxCaracteres = 60;
  const query = pool.query; const filas: { sql: string; params: any[] }[] = [];
  (pool as any).query = async (sql: string, params: any[] = []) => { filas.push({ sql, params }); return { rows: [] }; };
  const cuerpos: any[] = [];
  globalThis.fetch = async (url, init) => {
    assert.match(String(url), /api\.elevenlabs\.io\/v1\/text-to-speech\//);
    const b = JSON.parse(String(init?.body)); cuerpos.push(b);
    return new Response(`[${b.text}]`);
  };
  try { await fn(cuerpos, dir, filas); } finally {
    globalThis.fetch = originalFetch; pool.query = query;
    config.audioDir = prev.dir; config.elevenApiKey = prev.key; config.vozMaxCaracteres = prev.max;
    await rm(dir, { recursive: true });
  }
}

test('texto largo: se sintetiza por trozos (con previous_text), se une y queda en caché', () => conMock(async (cuerpos) => {
  const largo = 'Primera frase del texto largo. Segunda frase, algo más larga que la primera. Tercera y última frase.';
  const a = await obtenerAudio({ texto: largo, idioma: 'es' });
  assert.equal(a.cache, false);
  assert.equal(cuerpos.length, 3);
  for (const c of cuerpos) { assert.ok(c.text.length <= 60); assert.equal(c.voice_settings.style, 0); }
  assert.equal(cuerpos[0].previous_text, undefined);
  assert.equal(cuerpos[1].previous_text, cuerpos[0].text);
  assert.equal(a.buffer.toString(), cuerpos.map((c) => `[${c.text}]`).join(''));
  const otra = await obtenerAudio({ texto: largo, idioma: 'es' });
  assert.equal(otra.cache, true); assert.equal(otra.hash, a.hash); assert.equal(cuerpos.length, 3);
  // Un trozo ya generado se reutiliza dentro de otro texto largo.
  await obtenerAudio({ texto: 'Primera frase del texto largo.', idioma: 'es' });
  assert.equal(cuerpos.length, 3);
  // Por stream, un texto largo se sirve entero desde la caché.
  const s = await obtenerAudioStream({ texto: largo, idioma: 'es' }, new AbortController().signal, () => {});
  assert.equal(s.cache, true);
}));

test('respaldo a la clave anterior (misma voz): se sirve, se enlaza bajo la v2 y deja fila alias', () => conMock(async (cuerpos, dir, filas) => {
  const v = VOCES[rolDeVoz('narradora', 'es')];
  const m = config.elevenModelo;
  // Corto pregenerado y frase normal generados antes de la v2 con la misma voz.
  await writeFile(path.join(dir, `${hashAudioLegado(textoParaVoz('A', 'es'), v.id, m, 'es')}.mp3`), 'corto');
  await writeFile(path.join(dir, `${hashAudioLegado('Hola, ¿qué tal?', v.id, m, 'es')}.mp3`), 'viejo');
  const a = await obtenerAudio({ texto: 'A', idioma: 'es' });
  assert.equal(a.cache, true); assert.equal(a.buffer.toString(), 'corto');
  const b = await obtenerAudio({ texto: 'Hola, ¿qué tal?', idioma: 'es' });
  assert.equal(b.cache, true); assert.equal(b.buffer.toString(), 'viejo'); assert.equal(cuerpos.length, 0);
  const v2 = hashAudio('Hola, ¿qué tal?', v.id, m, 'es');
  assert.equal(b.hash, v2);
  assert.equal((await readFile(path.join(dir, `${v2}.mp3`))).toString(), 'viejo'); // enlazado bajo la v2
  const alias = filas.find((f) => f.sql.includes('INSERT') && f.params[0] === v2);
  assert.ok(alias); assert.match(alias.sql, /DO NOTHING/); assert.match(alias.sql, /,0,0\)/);
  // Por stream también; y un trozo de texto largo cae en su legado si existía entero.
  const s = await obtenerAudioStream({ texto: 'Hola, ¿qué tal?', idioma: 'es' }, new AbortController().signal, () => {});
  assert.equal(s.cache, true);
  const f1 = 'Primera frase del texto largo que ya existía.', f2 = 'Segunda frase, esta sí es nueva para la voz.';
  await writeFile(path.join(dir, `${hashAudioLegado(f1, v.id, m, 'es')}.mp3`), 'f1');
  const largo = await obtenerAudio({ texto: `${f1} ${f2}`, idioma: 'es' });
  assert.equal(cuerpos.length, 1); assert.equal(cuerpos[0].text, f2);
  assert.equal(largo.buffer.toString(), `f1[${f2}]`);
  // Otra voz (narrador) no aprovecha el audio de la narradora.
  const n = await obtenerAudio({ texto: 'Hola, ¿qué tal?', idioma: 'es', voz: 'narrador' });
  assert.equal(n.cache, false); assert.equal(cuerpos.length, 2);
}));

test('Stanislav (ru narrador) sintetiza a speed 0.9; la narradora sin speed', () => conMock(async (cuerpos) => {
  await obtenerAudio({ texto: 'Привет!', idioma: 'ru', voz: 'narrador' });
  await obtenerAudio({ texto: 'Привет!', idioma: 'ru' });
  assert.equal(cuerpos[0].voice_settings.speed, 0.9);
  assert.equal('speed' in cuerpos[1].voice_settings, false);
}));

test('stream por frase: manda previous_text y no lo usa en la clave', () => conMock(async (cuerpos) => {
  const s = await obtenerAudioStream({ texto: 'Ciao!', idioma: 'it', voz: 'avatar_kenji', previo: 'Come stai?' }, new AbortController().signal, () => {});
  for await (const _ of s.stream) { /* drain */ }
  assert.equal(cuerpos[0].previous_text, 'Come stai?');
  assert.equal(cuerpos[0].language_code, 'it');
  const r = await obtenerAudioStream({ texto: 'Ciao!', idioma: 'it', voz: 'avatar_kenji', previo: 'Altro.' }, new AbortController().signal, () => {});
  assert.equal(r.cache, true); assert.equal(r.hash, s.hash); assert.equal(cuerpos.length, 1);
}));
