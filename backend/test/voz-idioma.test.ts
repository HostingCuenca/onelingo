import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { codigoIdiomaVoz, cuerpoSintesis, hashAudio, hashAudioLegado, esAudioCorto, rolDeVoz, rolPedido, textoParaVoz, trocearTexto, NATIVAS, ROLES, VOCES, AJUSTES_VOZ } from '../src/lib/voz.js';

test('la síntesis fuerza el idioma en modelos v2.5 y no en los demás', () => {
  assert.equal(codigoIdiomaVoz('ja', 'eleven_flash_v2_5'), 'ja');
  assert.equal(codigoIdiomaVoz('pt', 'eleven_turbo_v2_5'), 'pt');
  assert.equal(codigoIdiomaVoz('ja', 'eleven_multilingual_v2'), undefined);
  assert.equal(codigoIdiomaVoz('xx', 'eleven_flash_v2_5'), undefined);
  assert.equal(cuerpoSintesis('あ', 'ja', 'eleven_flash_v2_5').language_code, 'ja');
  assert.equal('language_code' in cuerpoSintesis('あ', 'ja', 'eleven_multilingual_v2'), false);
});

test('la caché distingue idiomas, voz, modelo y ajustes; mismo texto y voz = mismo hash', () => {
  assert.equal(hashAudio('no', 'voz', 'm', 'es'), hashAudio('no', 'voz', 'm', 'es'));
  assert.equal(hashAudio('no', 'voz', 'm', 'es'), hashAudio('no', 'voz', 'm', 'es', { ...AJUSTES_VOZ }));
  assert.notEqual(hashAudio('no', 'voz', 'm', 'es'), hashAudio('no', 'voz', 'm', 'pt'));
  assert.notEqual(hashAudio('no', 'voz', 'm', 'es'), hashAudio('no', 'otra', 'm', 'es'));
  assert.notEqual(hashAudio('no', 'voz', 'm', 'es'), hashAudio('no', 'voz', 'm2', 'es'));
  assert.notEqual(hashAudio('no', 'voz', 'm', 'es'), hashAudio('no', 'voz', 'm', 'es', { ...AJUSTES_VOZ, style: 0.2 }));
  assert.notEqual(hashAudio('no', 'voz', 'm', 'es'), hashAudio('no', 'voz', 'm', 'es', { ...AJUSTES_VOZ, speed: 0.9 }));
  // Los cortos pregenerados conservan su clave anterior (inglés sin idioma).
  assert.equal(hashAudioLegado('no', 'voz', 'm', 'en'), hashAudioLegado('no', 'voz', 'm'));
  assert.notEqual(hashAudioLegado('no', 'voz', 'm', 'es'), hashAudioLegado('no', 'voz', 'm', 'en'));
  assert.notEqual(hashAudioLegado('no', 'voz', 'm', 'es'), hashAudio('no', 'voz', 'm', 'es'));
  assert.equal(cuerpoSintesis('Hola', 'es', 'eleven_flash_v2_5').voice_settings.style, 0);
  assert.equal(cuerpoSintesis('Hola', 'es', 'eleven_flash_v2_5', 'Antes.').previous_text, 'Antes.');
  assert.equal('previous_text' in cuerpoSintesis('Hola', 'es', 'eleven_flash_v2_5'), false);
});

test('audios cortos: letra, sílaba o palabra de 1–2 letras', () => {
  assert.equal(esAudioCorto('A', 'a.'), true);
  assert.equal(esAudioCorto('马', '马。'), true);
  assert.equal(esAudioCorto('你好', '你好'), false);
  assert.equal(esAudioCorto('Y', 'i griega.', 'letra'), true);
  assert.equal(esAudioCorto('casa', 'casa'), false);
});

test('zh y ja se leen sin los espacios entre palabras del contenido', () => {
  assert.equal(textoParaVoz('わたし は がくせい です', 'ja'), 'わたしはがくせいです');
  assert.equal(textoParaVoz('我 是 学生 (wǒ shì xuésheng)', 'zh'), '我是学生');
  assert.equal(textoParaVoz('저는 학생이에요', 'ko'), '저는 학생이에요');
  assert.equal(textoParaVoz('Hello  there', 'en'), 'Hello there');
});

const SELECCION: Record<string, [string, string, string, string, string]> = {
  // narradora, narrador, mujer_b, hombre_b, lumo (piloto de voces 2026-10-19)
  en: ['XrExE9yKIg1WjnnlVkGX', 'TX3LPaxmHKxFdv7VOQHJ', '56AoDkrOh6qfVPDXZ7Pt', 'UgBBYS2sOqTuMpoF3BR0', 'tnSpp4vdxKPjI9w0GnoV'],
  es: ['rixsIpPlTphvsJd2mI03', 'gbTn1bmCvNgk0QEAVyfM', '86V9x9hrQds83qf7zaGn', 'htFfPSZGJwjBv1CL0aMD', 'ajOR9IDAaubDK5qtLUqQ'],
  fr: ['kwhMCf63M8O3rCfnQ3oQ', 'aQROLel5sQbj1vuIVi6B', 'YxrwjAKoUKULGd0g8K9Y', 'kENkNtk0xyzG09WW40xE', 'FvmvwvObRqIHojkEGh5N'],
  de: ['lzvBSKYbNWDD0a6BaJSK', 'n6JEKnKG5a8I78SoBRry', 'v3V1d2rk6528UrLKRuy8', 'aTTiK3YzK3dXETpuDE2h', 'HRIShmNY56JGHVU1vXIt'],
  pt: ['7iqXtOF3wl3pomwXFY7G', 'Qrdut83w0Cr152Yb4Xn3', 'MZxV5lN3cv7hi1376O0m', '9pDzHy2OpOgeXM8SeL0t', 'RGymW84CSmfVugnA5tvA'],
  it: ['fQmr8dTaOQq116mo2X7F', 'HuK8QKF35exsCh2e7fLT', '6KQ52XTjdNd1FfUgGmV6', 'W71zT1VwIFFx3mMGH2uZ', 'Kq9pDHHIMmJsG9PEqOtv'],
  ru: ['EDpEYNf6XIeKYRzYcx4I', 'ogi2DyUAKJb7CEdqqvlU', 'Jbte7ht1CqapnZvc4KpK', 'rQOBu7YxCDxGiFdTm28w', 'AB9XsbSA4eLG12t2myjN'],
  ko: ['AW5wrnG1jVizOYY7R1Oo', 'PDoCXqBQFGsvfO0hNkEs', 'uyVNoMrnUku1dZyVEXwD', '4JJwo477JUAx3HV0T7n7', '8jHHF8rMqMlg8if2mOUe'],
  ja: ['4lOQ7A2l7HPuG7UIHiKA', 'j210dv0vWm7fCknyQpbA', 'WQz3clzUdMqvBf0jswZQ', 'b34JylakFZPlGS0BnwyY', 'B8gJV1IhpuegLxdpXFOE'],
  zh: ['ByhETIclHirOlWnWKhHc', 'MI36FIkp9wRP7cpWKPTl', '5eoK8NqMBsMdqUmImHNs', 'lt7GBaCoAHWbT7JSZ5Xs', 'NchRhc5KPgHwZagz6MrZ'],
};
const idDe = (voz: string | undefined, idioma: string) => VOCES[rolDeVoz(voz, idioma)].id;

test('cada idioma tiene su voz nativa para los cinco roles (ids de la selección)', () => {
  assert.deepEqual(Object.keys(NATIVAS).sort(), Object.keys(SELECCION).sort());
  for (const [idioma, ids] of Object.entries(SELECCION)) {
    ROLES.forEach((rol, i) => assert.equal(idDe(rol, idioma), ids[i], `${idioma} ${rol}`));
    assert.equal(new Set(ids).size, 5, `${idioma}: cinco voces distintas`);
  }
  // Hélène (desactivada), Chris (en) y Luna (it) ya no suenan.
  const ids = new Set(Object.values(VOCES).map((v) => v.id));
  for (const fuera of ['imRmmzTqlLHt9Do1HufF', 'iP95p4xoKVk53GoZ742B', 'BZc8d1MPTdZkyGbE9Sin']) assert.equal(ids.has(fuera), false);
});

test('tutores, avatares y roles se traducen a la voz nativa del idioma practicado', () => {
  for (const idioma of Object.keys(SELECCION)) {
    const [narradora, narrador, mujer, hombre, lumo] = SELECCION[idioma];
    assert.equal(idDe(undefined, idioma), narradora);
    assert.equal(idDe('no-existe', idioma), narradora);
    assert.equal(idDe('narrador', idioma), narrador);
    for (const t of ['mia', 'sofia', 'avatar_amara', 'avatar_sofia', 'avatar_lucia', 'avatar_clara', 'avatar_mei', 'mujer_b']) assert.equal(idDe(t, idioma), mujer, `${idioma} ${t}`);
    for (const t of ['leo', 'max', 'avatar_malik', 'avatar_mateo', 'avatar_owen', 'avatar_daniel', 'avatar_kenji', 'hombre_b']) assert.equal(idDe(t, idioma), hombre, `${idioma} ${t}`);
    assert.equal(idDe('avatar_lumo', idioma), lumo);
    assert.equal(idDe('lumo', idioma), lumo);
  }
  assert.equal(rolDeVoz('narradora', 'fr'), 'fr_caroline');
  assert.equal(rolDeVoz('avatar_nuevo', 'de'), 'de_petra');
  assert.equal(rolDeVoz('no-existe', 'xx'), 'en_matilda');
  assert.equal(rolDeVoz('de_julius', 'fr'), 'de_julius'); // clave directa (panel)
});

test('el género de cada avatar coincide con web/avatar/roster.json', () => {
  const roster = JSON.parse(readFileSync(new URL('../../web/avatar/roster.json', import.meta.url), 'utf8'));
  for (const t of roster.tutors as { id: string; gender: string }[]) {
    const esperado = t.id === 'lumo' ? 'lumo' : t.gender === 'female' ? 'mujer_b' : t.gender === 'male' ? 'hombre_b' : 'narradora';
    assert.equal(rolPedido(`avatar_${t.id}`), esperado, t.id);
  }
});

test('textos largos: trozos ≤ máximo, por frases, sin perder texto', () => {
  assert.deepEqual(trocearTexto('Hola.', 600), ['Hola.']);
  const frase = 'Esta es una frase de prueba bastante normal. ';
  const largo = frase.repeat(30).trim();
  const t = trocearTexto(largo, 600);
  assert.ok(t.length > 1);
  for (const x of t) { assert.ok(x.length <= 600); assert.ok(x.endsWith('.')); }
  assert.equal(t.join(' '), largo);
  const zh = '我们今天去学校。你呢？'.repeat(40);
  const tz = trocearTexto(zh, 100);
  for (const x of tz) { assert.ok(x.length <= 100); assert.ok(/[。？]$/.test(x)); }
  assert.equal(tz.join(''), zh);
  assert.deepEqual(trocearTexto('¿Vienes? «Sí.» Vale', 9), ['¿Vienes?', '«Sí.»', 'Vale']);
  // Una frase sin puntos: por comas, luego por palabras, al final a cuchillo.
  const comas = Array.from({ length: 40 }, (_, i) => `parte ${i}`).join(', ');
  for (const x of trocearTexto(comas, 50)) assert.ok(x.length <= 50);
  assert.deepEqual(trocearTexto('a'.repeat(25), 10), ['a'.repeat(10), 'a'.repeat(10), 'a'.repeat(5)]);
  assert.equal(trocearTexto('Dr. Weber kommt.', 600).length, 1);
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
  assert.equal(textoParaVoz('It costs 437 euros.', 'en'), 'It costs 437 euros.');
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
  assert.equal(textoParaVoz('0 · 1 · 2 · 3', 'ru'), 'ноль, один, два, три');
  assert.equal(textoParaVoz('와 / 과', 'ko'), '와, 과.');
  assert.equal(textoParaVoz('N 대신', 'ko'), '대신.');
  assert.equal(textoParaVoz('一定 是 / 肯定 是', 'zh'), '一定是，肯定是');
  assert.equal(textoParaVoz('才 / 就 + hora', 'zh'), '才，就。');
  assert.equal(textoParaVoz('ない + ように', 'ja'), 'ないように');
  assert.equal(textoParaVoz('볼 만한 + sustantivo', 'ko'), '볼 만한.');
  assert.equal(textoParaVoz('Pagamos hoje R$ 5.000 por mês.', 'pt'), 'Pagamos hoje cinco mil reais por mês.');
  assert.equal(textoParaVoz('À vista no Pix: R$ 6.480.', 'pt'), 'À vista no Pix: seis mil quatrocentos e oitenta reais.');
  assert.equal(textoParaVoz('Abierto 24/7', 'en'), 'Abierto 24/7');
  assert.equal(textoParaVoz('KTV 很 好玩', 'zh'), 'KTV很好玩');
});
