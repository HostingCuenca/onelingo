import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { conGananciaVoz, ffmpegDisponible, gananciaVoz, medirLufs, normalizarVolumen, OBJETIVO_LUFS } from '../src/lib/volumen.js';

/** 2 s de ruido rosa (se mide como la voz) a `db` dB, en MP3 (solo si hay ffmpeg). */
function tono(db: number): Buffer {
  const r = spawnSync(process.env.FFMPEG ?? 'ffmpeg', ['-hide_banner', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anoisesrc=color=pink:duration=2:amplitude=0.5',
    '-af', `volume=${db}dB`, '-c:a', 'libmp3lame', '-b:a', '128k', '-f', 'mp3', 'pipe:1']);
  return r.stdout;
}

test('la ganancia de cada voz la lleva al objetivo y se limita', () => {
  assert.equal(gananciaVoz('ru_mariia'), OBJETIVO_LUFS - -11.6);
  assert.ok(gananciaVoz('it_anna') > 20, 'it_anna era la más baja');
  assert.equal(gananciaVoz('voz_sin_medir'), 0);
});

test('un clip bajo y uno alto quedan al mismo volumen', async (t) => {
  if (!(await ffmpegDisponible())) return t.skip('sin ffmpeg');
  for (const db of [-15, 5]) {
    const lufs = await medirLufs(await normalizarVolumen(tono(db)));
    assert.ok(lufs !== null && Math.abs(lufs - OBJETIVO_LUFS) < 1.5, `${db} dB → ${lufs} LUFS`);
  }
});

test('lo que no es MP3 sale tal cual', async () => {
  const basura = Buffer.from('no es audio');
  assert.equal(await normalizarVolumen(basura), basura);
  const partes: Buffer[] = [];
  async function* trozos() { yield basura; }
  for await (const p of conGananciaVoz(trozos(), 'it_anna')) partes.push(p);
  assert.deepEqual(Buffer.concat(partes), basura);
});

test('el streaming aplica la ganancia de la voz', async (t) => {
  if (!(await ffmpegDisponible())) return t.skip('sin ffmpeg');
  const mp3 = tono(-30);
  async function* trozos() { for (let i = 0; i < mp3.length; i += 2048) yield mp3.subarray(i, i + 2048); }
  const partes: Buffer[] = [];
  for await (const p of conGananciaVoz(trozos(), 'zh_shanshan')) partes.push(p);
  const antes = await medirLufs(mp3), despues = await medirLufs(Buffer.concat(partes));
  assert.ok(antes !== null && despues !== null && despues - antes > 12, `${antes} → ${despues}`);
});
