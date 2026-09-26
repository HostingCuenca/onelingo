import { test } from 'node:test';
import assert from 'node:assert/strict';
import { codigoIdiomaVoz, cuerpoSintesis, hashAudio, textoParaVoz } from '../src/lib/voz.js';

test('la síntesis fuerza el idioma en modelos v2.5 y no en los demás', () => {
  assert.equal(codigoIdiomaVoz('ja', 'eleven_flash_v2_5'), 'ja');
  assert.equal(codigoIdiomaVoz('pt', 'eleven_turbo_v2_5'), 'pt');
  assert.equal(codigoIdiomaVoz('ja', 'eleven_multilingual_v2'), undefined);
  assert.equal(codigoIdiomaVoz('xx', 'eleven_flash_v2_5'), undefined);
  assert.equal(cuerpoSintesis('あ', 'ja', 'eleven_flash_v2_5').language_code, 'ja');
  assert.equal('language_code' in cuerpoSintesis('あ', 'ja', 'eleven_multilingual_v2'), false);
});

test('la caché distingue idiomas y conserva la clave inglesa anterior', () => {
  const anterior = hashAudio('no', 'voz', 'm');
  assert.equal(hashAudio('no', 'voz', 'm', 'en'), anterior);
  assert.notEqual(hashAudio('no', 'voz', 'm', 'es'), anterior);
  assert.notEqual(hashAudio('no', 'voz', 'm', 'es'), hashAudio('no', 'voz', 'm', 'pt'));
});

test('zh y ja se leen sin los espacios entre palabras del contenido', () => {
  assert.equal(textoParaVoz('わたし は がくせい です', 'ja'), 'わたしはがくせいです');
  assert.equal(textoParaVoz('我 是 学生 (wǒ shì xuésheng)', 'zh'), '我是学生');
  assert.equal(textoParaVoz('저는 학생이에요', 'ko'), '저는 학생이에요');
  assert.equal(textoParaVoz('Hello  there', 'en'), 'Hello there');
});
