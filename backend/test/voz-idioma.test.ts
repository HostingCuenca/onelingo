import { test } from 'node:test';
import assert from 'node:assert/strict';
import { codigoIdiomaVoz, cuerpoSintesis, hashAudio, rolDeVoz, textoParaVoz } from '../src/lib/voz.js';

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
  assert.equal(rolDeVoz('narradora', 'en'), 'sofia');
  assert.equal(rolDeVoz('avatar_lumo', 'fr'), 'avatar_lumo');
  assert.equal(rolDeVoz('no-existe', 'en'), 'sofia');
  assert.equal(rolDeVoz('no-existe', 'xx'), 'narradora');
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

test('en (americano), es (latino) y pt (Brasil) usan voces nativas; Lumo conserva la suya', () => {
  const esperadas: Record<string, [string, string]> = { en: ['sofia', 'chris_en'], es: ['isabel', 'enrique'], pt: ['fernanda', 'paulo'] };
  for (const [idioma, [narradora, narrador]] of Object.entries(esperadas)) {
    assert.equal(rolDeVoz(undefined, idioma), narradora);
    assert.equal(rolDeVoz('narrador', idioma), narrador);
    assert.equal(rolDeVoz('avatar_lumo', idioma), 'avatar_lumo');
  }
});

test('letras: modo letra dice el nombre; sin modo, una letra suelta es palabra en minúscula', () => {
  assert.equal(textoParaVoz('A', 'es'), 'a.');
  assert.equal(textoParaVoz('Y', 'es', 'letra'), 'i griega.');
  assert.equal(textoParaVoz('H', 'es', 'letra'), 'hache.');
  assert.equal(textoParaVoz('R', 'pt', 'letra'), 'erre.');
  assert.equal(textoParaVoz('J', 'de', 'letra'), 'Jott.');
  assert.equal(textoParaVoz('O, M, A', 'de', 'letra'), 'O, Emm, A.');
  assert.equal(textoParaVoz('В', 'ru', 'letra'), 'вэ.');
  assert.equal(textoParaVoz('C, A, T.', 'en', 'letra'), 'C, A, T.');
  assert.equal(textoParaVoz('W', 'en', 'letra'), 'W.');
  assert.equal(textoParaVoz('あ', 'ja', 'letra'), 'あ。');
  assert.equal(textoParaVoz('é', 'pt'), 'é.');
  assert.equal(textoParaVoz('I', 'en'), 'I.');
  assert.equal(textoParaVoz('は', 'ja'), 'は。');
  assert.equal(textoParaVoz('妈 (mā)', 'zh'), '妈。');
  assert.equal(textoParaVoz('Hola', 'es'), 'Hola');
  assert.equal(textoParaVoz('ㅏ', 'ko'), '아.');
  assert.equal(textoParaVoz('L-E-N-A', 'de', 'letra'), 'Ell, E, Enn, A.');
  assert.equal(textoParaVoz('ß', 'de', 'letra'), 'Eszett.');
  assert.equal(textoParaVoz('ㄴ, ㅏ, ㅁ, ㅜ', 'ko', 'letra'), '니은, 아, 미음, 우.');
});

test('la notación de la vista no se pronuncia', () => {
  assert.equal(textoParaVoz('das Medikament, -e', 'de'), 'das Medikament');
  assert.equal(textoParaVoz('hätte + Partizip II', 'de'), 'hätte, Partizip II');
  assert.equal(textoParaVoz('don / doña + nombre de pila', 'es'), 'don, doña, nombre de pila');
  assert.equal(textoParaVoz('Bitte reagieren Sie ___ bis zum 20. März.', 'de'), 'Bitte reagieren Sie … bis zum zwanzigsten März.');
  assert.equal(textoParaVoz('0 · 1 · 2 · 3', 'ru'), '0, 1, 2, 3');
  assert.equal(textoParaVoz('와 / 과', 'ko'), '와, 과.');
  assert.equal(textoParaVoz('N 대신', 'ko'), '대신.');
  assert.equal(textoParaVoz('一定 是 / 肯定 是', 'zh'), '一定是，肯定是');
  assert.equal(textoParaVoz('才 / 就 + hora', 'zh'), '才，就。');
  assert.equal(textoParaVoz('ない + ように', 'ja'), 'ないように');
  assert.equal(textoParaVoz('볼 만한 + sustantivo', 'ko'), '볼 만한.');
  assert.equal(textoParaVoz('Pagamos hoje R$ 5.000 por mês.', 'pt'), 'Pagamos hoje 5.000 reais por mês.');
  assert.equal(textoParaVoz('À vista no Pix: R$ 6.480.', 'pt'), 'À vista no Pix: 6.480 reais.');
  assert.equal(textoParaVoz('Abierto 24/7', 'en'), 'Abierto 24/7');
  assert.equal(textoParaVoz('KTV 很 好玩', 'zh'), 'KTV很好玩');
});
