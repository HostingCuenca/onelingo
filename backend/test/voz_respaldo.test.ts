import { test } from 'node:test';
import assert from 'node:assert/strict';
import { anotarFalloEleven, elevenPausado, instruccionesRespaldo, reanudarEleven, vozRespaldo } from '../src/lib/voz_respaldo.js';

test('the backup voice keeps the gender and is stable for each tutor', () => {
  assert.ok(['ash', 'echo', 'onyx', 'cedar', 'verse'].includes(vozRespaldo('avatar_andre', 'Andre', 'tutor africano')));
  assert.ok(['coral', 'nova', 'shimmer', 'sage', 'marin'].includes(vozRespaldo('avatar_chloe', 'Chloe', 'mujer joven')));
  assert.equal(vozRespaldo('avatar_chloe', 'Chloe', ''), vozRespaldo('avatar_chloe', 'Chloe', ''));
  assert.match(instruccionesRespaldo('ja'), /japonés/);
});

test('quota errors pause ElevenLabs for a while; other errors do not', () => {
  reanudarEleven();
  anotarFalloEleven(new Error('ElevenLabs 500: boom'));
  assert.equal(elevenPausado(), false);
  anotarFalloEleven(new Error('ElevenLabs 401: {"detail":{"code":"quota_exceeded"}}'));
  assert.equal(elevenPausado(), true);
  reanudarEleven();
  assert.equal(elevenPausado(), false);
});
