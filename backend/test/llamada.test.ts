import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, rm, writeFile, readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { esperarGuardados, obtenerAudio, obtenerAudioAlineado, unirAlineaciones } from '../src/lib/voz.js';
import { puedeEmitir, TOKENS_POR_HORA } from '../src/routes/llamada.js';
import { config } from '../src/lib/config.js';
import { pool } from '../src/lib/db.js';

const originalFetch = globalThis.fetch;
const alin = (texto: string, paso = 0.1) => ({
  characters: [...texto], character_start_times_seconds: [...texto].map((_, i) => +(i * paso).toFixed(3)),
  character_end_times_seconds: [...texto].map((_, i) => +((i + 1) * paso).toFixed(3)),
});

/** ElevenLabs simulado: «with-timestamps» devuelve el texto como audio y una alineación de 0,1 s por letra. */
async function conMock(fn: (urls: string[], dir: string) => Promise<void>) {
  const dir = await mkdtemp(`${tmpdir()}/onelingo-alineada-`);
  const prev = { dir: config.audioDir, key: config.elevenApiKey, max: config.vozMaxCaracteres };
  config.audioDir = dir; config.elevenApiKey = 'test'; config.vozMaxCaracteres = 60;
  const query = pool.query; (pool as any).query = async () => ({ rows: [] });
  const urls: string[] = [];
  globalThis.fetch = async (url, init) => {
    urls.push(String(url));
    const b = JSON.parse(String(init?.body));
    if (String(url).includes('/with-timestamps')) return Response.json({ audio_base64: Buffer.from(`[${b.text}]`).toString('base64'), alignment: alin(b.text) });
    return new Response(`[${b.text}]`);
  };
  try { await fn(urls, dir); } finally {
    await esperarGuardados();
    globalThis.fetch = originalFetch; pool.query = query;
    config.audioDir = prev.dir; config.elevenApiKey = prev.key; config.vozMaxCaracteres = prev.max;
    await rm(dir, { recursive: true });
  }
}

test('unirAlineaciones: cada trozo empieza donde acabó el anterior; si falta una, null', () => {
  const u = unirAlineaciones([alin('ab'), alin('cd')])!;
  assert.deepEqual(u.characters, ['a', 'b', 'c', 'd']);
  assert.deepEqual(u.character_start_times_seconds, [0, 0.1, 0.2, 0.3]);
  assert.deepEqual(u.character_end_times_seconds, [0.1, 0.2, 0.3, 0.4]);
  assert.equal(unirAlineaciones([alin('ab'), null]), null);
  assert.equal(unirAlineaciones([]), null);
});

test('voz alineada: se genera una vez con tiempos, se guarda junto al MP3 y luego sale de la caché', () => conMock(async (urls, dir) => {
  const a = await obtenerAudioAlineado({ texto: 'Hola, ¿cómo estás?', idioma: 'es' });
  assert.equal(a.cache, false);
  await esperarGuardados(); // se entrega antes de guardar
  assert.match(urls[0], /\/with-timestamps\?/);
  assert.equal(a.buffer.toString(), '[Hola, ¿cómo estás?]');
  assert.equal(a.alineacion?.characters.join(''), 'Hola, ¿cómo estás?');
  assert.deepEqual(JSON.parse(await readFile(path.join(dir, `${a.hash}.json`), 'utf8')), a.alineacion);
  const b = await obtenerAudioAlineado({ texto: 'Hola, ¿cómo estás?', idioma: 'es' });
  assert.equal(b.cache, true); assert.equal(urls.length, 1); assert.deepEqual(b.alineacion, a.alineacion);
  // La voz normal reutiliza el mismo MP3 (misma clave de caché).
  const c = await obtenerAudio({ texto: 'Hola, ¿cómo estás?', idioma: 'es' });
  assert.equal(c.cache, true); assert.equal(c.hash, a.hash); assert.equal(urls.length, 1);
}));

test('voz alineada: un MP3 que ya existía sin tiempos no se vuelve a pagar (alineación null)', () => conMock(async (urls) => {
  const viejo = await obtenerAudio({ texto: 'Ya estaba en caché.', idioma: 'es' });
  assert.equal(urls.length, 1);
  const a = await obtenerAudioAlineado({ texto: 'Ya estaba en caché.', idioma: 'es' });
  assert.equal(a.cache, true); assert.equal(a.hash, viejo.hash); assert.equal(a.alineacion, null); assert.equal(urls.length, 1);
}));

test('voz alineada: texto largo por trozos con los tiempos unidos', () => conMock(async (urls) => {
  const largo = 'Primera frase del texto largo. Segunda frase, algo más larga que la primera. Tercera y última frase.';
  const a = await obtenerAudioAlineado({ texto: largo, idioma: 'es' });
  assert.equal(urls.length, 3);
  const al = a.alineacion!;
  assert.equal(al.characters.length, al.character_start_times_seconds.length);
  for (let i = 1; i < al.character_start_times_seconds.length; i++) assert.ok(al.character_start_times_seconds[i] >= al.character_start_times_seconds[i - 1]);
}));

test('token de llamada: como mucho TOKENS_POR_HORA por alumno y hora', () => {
  const t0 = 1_000_000;
  for (let i = 0; i < TOKENS_POR_HORA; i++) assert.equal(puedeEmitir('u-limite', t0 + i), true);
  assert.equal(puedeEmitir('u-limite', t0 + 100), false);
  assert.equal(puedeEmitir('otro', t0 + 100), true);
  assert.equal(puedeEmitir('u-limite', t0 + 3_600_001), true);
});
