import { test } from 'node:test';
import assert from 'node:assert/strict';
import { separadorDeLenguas, sinCorchetes } from '../src/lib/explicaciones.js';
import { frasesCompletas } from '../src/lib/ia_openai.js';
import { systemPrompt } from '../src/lib/ia.js';

test('explanations in brackets are split by language, even across sentences', () => {
  const separar = separadorDeLenguas('ja');
  assert.deepEqual(separar('いいですね！[Como fue ayer, se dice «行きました», no «行く».] 昨日、公園に行きました。'), [
    { texto: 'いいですね！', nativo: false },
    { texto: 'Como fue ayer, se dice «行きました», no «行く».', nativo: true, corchete: true },
    { texto: '昨日、公園に行きました。', nativo: false },
  ]);
  const otra = separadorDeLenguas('en');
  assert.deepEqual(otra('Nice! [Como fue ayer,'), [{ texto: 'Nice!', nativo: false }, { texto: 'Como fue ayer,', nativo: true, corchete: true }]);
  assert.deepEqual(otra('se dice «went».] Say it?'), [{ texto: 'se dice «went».', nativo: true, corchete: true }, { texto: 'Say it?', nativo: false }]);
  assert.deepEqual(otra('[ ]'), []);
});

test('without brackets, a Latin sentence in a non-Latin course is the learner language', () => {
  const separar = separadorDeLenguas('ja');
  assert.equal(separar('Como fue ayer, se dice «行きました».')[0].nativo, true);
  assert.equal(separar('昨日は何をしましたか？')[0].nativo, false);
  assert.equal(separadorDeLenguas('fr')('Comment ça va ?')[0].nativo, false);
});

test('a bracketed sentence in the course script is spoken as the course language', () => {
  const separar = separadorDeLenguas('ja');
  assert.equal(separar('[昨日のことなので「いきました」と言います。]')[0].nativo, false);
  // Pero sigue siendo una indicación: va al final y se pasa a su idioma (indicacionEnSuIdioma).
  assert.equal(separadorDeLenguas('ja')('[昨日のことなので「いきました」と言います。]')[0].corchete, true);
  assert.equal(separar('[Se dice «いきました».]')[0].nativo, true);
  assert.equal(separadorDeLenguas('en')('[Because it was yesterday.]')[0].nativo, true, 'mismo alfabeto: manda el corchete');
});

test('the learner never sees the brackets', () => {
  assert.equal(sinCorchetes('Nice! [Como fue ayer, se dice «went».] Say it?'), 'Nice! Como fue ayer, se dice «went». Say it?');
  assert.equal(sinCorchetes('Oh [ya]  .'), 'Oh ya.');
});

test('a closing bracket ends the sentence for the voice', () => {
  assert.deepEqual(frasesCompletas('Great, nice try! [Como fue ayer, se dice «went».] Can you say it?', true),
    ['Great, nice try!', '[Como fue ayer, se dice «went».]', 'Can you say it?']);
  assert.deepEqual(frasesCompletas('Great, nice try![Como fue ayer, se dice «went».]', true), ['Great, nice try!', '[Como fue ayer, se dice «went».]']);
  assert.deepEqual(frasesCompletas('On va pratiquer « j’aime… » et « je n’aime pas… ». Et toi ?', true), ['On va pratiquer « j’aime… » et « je n’aime pas… ».', 'Et toi ?']);
});

test('only the video call in native mode asks for bracketed explanations', () => {
  const base = { idiomaMeta: 'ja', idiomaNativo: 'es', nivel: 2, tutorId: 'avatar_chloe' };
  const nativo = systemPrompt({ ...base, explica: 'nativo' });
  assert.match(nativo, /eligió que le EXPLIQUES en español/);
  assert.match(nativo, /entre corchetes/);
  // La indicación en su idioma va al final del turno, en un solo bloque.
  assert.match(nativo, /昨日、公園に行きました。 言ってみて！ \[Como fue ayer, se dice «いきました», no «いく». Di la frase completa.\]»/);
  assert.match(nativo, /INDICACIONES, no para traducir/);
  assert.match(systemPrompt({ ...base, idiomaMeta: 'es', idiomaNativo: 'en', explica: 'nativo' }), /Your turn!|¡Te toca! \[It was yesterday, so we say «fui», not «voy». Say the whole sentence.\]/);
  assert.doesNotMatch(nativo, /tu voz solo habla japonés/);
  const meta = systemPrompt({ ...base, explica: 'meta' });
  assert.doesNotMatch(meta, /EXPLIQUES/);
  assert.match(meta, /botón «Explica en…»/);
  assert.match(meta, /tu voz solo habla japonés/);
  assert.doesNotMatch(systemPrompt({ ...base, tutorId: 'mia', explica: 'nativo' }), /EXPLIQUES/, 'el chat escrito no cambia');
  assert.doesNotMatch(systemPrompt({ ...base, idiomaNativo: 'ja', explica: 'nativo' }), /EXPLIQUES/);
});

test('the transcription also expects the learner language', async () => {
  const { pistaTranscripcion } = await import('../src/lib/ia_openai.js');
  assert.equal(pistaTranscripcion('ja', 'es'), 'Clase de japonés. El alumno habla español: puede hablar en japonés, en español o mezclar ambos.');
  assert.match(pistaTranscripcion('es', 'en') ?? '', /^Spanish class\. The learner's own language is English/);
  assert.equal(pistaTranscripcion('ja', 'ja'), undefined);
  assert.equal(pistaTranscripcion('ja'), undefined);
  assert.equal(pistaTranscripcion('ja', 'xx'), undefined);
});

test('after about 4 silent seconds the tutor takes the initiative and asks the learner for the topic', async () => {
  const { notaAviso } = await import('../src/lib/ia.js');
  const n = notaAviso('iniciativa');
  assert.match(n, /pregúntale de qué le gustaría hablar/);
  assert.match(n, /frase modelo/);
  assert.match(n, /situación de práctica, no salgas de la escena/);
  assert.match(n, /Nunca impongas tú un tema/);
  assert.match(systemPrompt({ idiomaMeta: 'en', idiomaNativo: 'es', nivel: 2, tutorId: 'avatar_chloe' }), /TEMAS\. El tema lo elige el alumno/);
});

test('beginners in native mode get every question translated; topics are offered, not imposed', async () => {
  const base = { idiomaMeta: 'en', idiomaNativo: 'es', tutorId: 'avatar_chloe', explica: 'nativo' as const };
  assert.match(systemPrompt({ ...base, nivel: 1 }), /NIVEL INICIAL: casi no entiende inglés/);
  assert.doesNotMatch(systemPrompt({ ...base, nivel: 4 }), /NIVEL INICIAL/);
  assert.doesNotMatch(systemPrompt({ ...base, nivel: 1, explica: 'meta' }), /NIVEL INICIAL/);
  const { textoFicha } = await import('../src/lib/ficha_alumno.js');
  const f = { sobreMi: [], intereses: [], objetivo: '', comoHabla: '', domina: [], errores: [], comoAprende: [], plan: { foco: '', porque: '', siguientes: [], avance: '' }, pendiente: ['Decir qué celebra en su fiesta'] };
  assert.match(textoFicha(f), /nunca lo impongas/);
});

test('solo se traduce la indicación si puede estar en el idioma meta', async () => {
  const { indicacionDudosa } = await import('../src/lib/explicaciones.js');
  assert.equal(indicacionDudosa('Repite la frase completa.', 'ja'), false);
  assert.equal(indicacionDudosa('もう一度言ってください。', 'ja'), true);
  assert.equal(indicacionDudosa('Rispondi: sì o no.', 'it'), true, 'con letras latinas no se puede saber');
});
