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

test('francés usa voces nativas: Hélène narra y Nicolas en diálogos', async () => {
  const { rolDeVoz } = await import('../src/lib/voz.js');
  assert.equal(rolDeVoz(undefined, 'fr'), 'helene');
  assert.equal(rolDeVoz('narrador', 'fr'), 'nicolas');
  assert.equal(rolDeVoz('narradora', 'en'), 'narradora');
  assert.equal(rolDeVoz('avatar_lumo', 'fr'), 'avatar_lumo');
  assert.equal(rolDeVoz('no-existe', 'en'), 'narradora');
});

test('alemán usa voces nativas: Petra narra y Julius en diálogos', async () => {
  const { rolDeVoz } = await import('../src/lib/voz.js');
  assert.equal(rolDeVoz(undefined, 'de'), 'petra');
  assert.equal(rolDeVoz('narrador', 'de'), 'julius');
  assert.equal(rolDeVoz('avatar_lumo', 'de'), 'avatar_lumo');
});

test('it, ru, ko, ja y zh usan voces nativas para narrar y para los diálogos', async () => {
  const { rolDeVoz } = await import('../src/lib/voz.js');
  const esperadas: Record<string, [string, string]> = {
    it: ['luna', 'carmelo'],
    ru: ['mariia', 'stanislav'],
    ko: ['jiyoung', 'chris_ko'],
    ja: ['kyoko', 'hinata'],
    zh: ['shanshan', 'evan'],
  };
  for (const [idioma, [narradora, narrador]] of Object.entries(esperadas)) {
    assert.equal(rolDeVoz(undefined, idioma), narradora);
    assert.equal(rolDeVoz('narrador', idioma), narrador);
    assert.equal(rolDeVoz('avatar_lumo', idioma), 'avatar_lumo');
  }
});

test('alemán: las cifras se leen en palabras (años, fechas, horas, §, decimales)', () => {
  const v = (t: string) => textoParaVoz(t, 'de');
  assert.equal(v('Der Dichter starb 1950.'), 'Der Dichter starb neunzehnhundertfünfzig.');
  assert.equal(v('Sie wurde 1921 geboren.'), 'Sie wurde neunzehnhunderteinundzwanzig geboren.');
  assert.equal(v('Das war im Jahr 2024.'), 'Das war im Jahr zweitausendvierundzwanzig.');
  assert.equal(v('Laut § 437 BGB hat der Käufer Rechte.'), 'Laut Paragraf vierhundertsiebenunddreißig BGB hat der Käufer Rechte.');
  assert.equal(v('im Sinne des § 434 BGB'), 'im Sinne des Paragrafen vierhundertvierunddreißig BGB');
  assert.equal(v('Es kostet 1950 Euro.'), 'Es kostet eintausendneunhundertfünfzig Euro.');
  assert.equal(v('Wir zahlen 1.000 €.'), 'Wir zahlen eintausend Euro.');
  assert.equal(v('bis zum 15. März'), 'bis zum fünfzehnten März');
  assert.equal(v('Der 3. Mai ist ein Freitag.'), 'Der dritte Mai ist ein Freitag.');
  assert.equal(v('um 7:15 Uhr'), 'um sieben Uhr fünfzehn');
  assert.equal(v('um 1 Uhr'), 'um ein Uhr');
  assert.equal(v('bei 3,5 %'), 'bei drei Komma fünf Prozent');
  assert.equal(v('Wir haben 21 Gäste und 101 Stühle.'), 'Wir haben einundzwanzig Gäste und einhunderteins Stühle.');
  assert.equal(v('Ich bin 15, mein Vater ist 50.'), 'Ich bin fünfzehn, mein Vater ist fünfzig.');
  assert.equal(textoParaVoz('Es kostet 437 Euro.', 'fr'), 'Es kostet 437 Euro.');
});
