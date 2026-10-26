import { test } from 'node:test';
import assert from 'node:assert/strict';
import { frasesCompletas, generarJsonOpenAI, generarTutorStream, replyParcial } from '../src/lib/ia_openai.js';
import { correccionesPrevias, resumirHechos, tipoCambio } from '../src/lib/situaciones.js';
import { depurarCorrecciones, promptCorrector, systemPrompt } from '../src/lib/ia.js';
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

test('every roster tutor has its own full character sheet', async () => {
  const { readFile } = await import('node:fs/promises');
  const { tutoresConFicha, fichaTutor } = await import('../src/lib/personajes.js');
  const roster = JSON.parse(await readFile(new URL('../../web/avatar/roster.json', import.meta.url), 'utf8'));
  const ids = [...roster.tutors.map((t: any) => `avatar_${t.id}`), 'mia', 'leo', 'sofia', 'max'];
  for (const id of ids) {
    assert.ok(tutoresConFicha().includes(id), `sin ficha: ${id}`);
    const f = fichaTutor(id);
    for (const parte of ['Tu vida:', 'Cómo conversas:', 'Cómo enseñas:', 'Evita:', 'tutor de IA de OneLingo']) assert.ok(f.includes(parte), `${id} sin ${parte}`);
    assert.doesNotMatch(f, /Ecuador|Quito|Guayaquil|Cuenca/);
  }
  assert.equal(new Set(ids.map(fichaTutor)).size, ids.length); // todas distintas
});

test('cada tutor en vivo conoce un idioma de primera mano y todos los idiomas tienen especialista', async () => {
  const { idiomaEspecial, fichaTutor } = await import('../src/lib/personajes.js');
  const idiomas = ['en', 'es', 'fr', 'de', 'pt', 'it', 'ru', 'ko', 'ja', 'zh'];
  const vivos = ['ana', 'elena', 'julia', 'chloe', 'nora', 'hana', 'lucas', 'tomas', 'frank', 'diego', 'erik', 'andre'].map((t) => `avatar_${t}`);
  const de = vivos.map((t) => idiomaEspecial(t));
  for (const [i, l] of de.entries()) assert.ok(l && idiomas.includes(l), vivos[i]);
  for (const l of idiomas) assert.ok(de.includes(l), `sin especialista: ${l}`);
  // Con su idioma aporta cultura y uso real; con otro, solo lo menciona.
  assert.match(fichaTutor('avatar_erik', 'ja'), /especialidad es el japonés, justo el que practica/);
  assert.match(fichaTutor('avatar_erik', 'en'), /Hoy el alumno practica inglés: hablas en ese idioma todo el tiempo/);
  assert.doesNotMatch(fichaTutor('mia', 'en'), /especialidad es el/);
});

test('the safety net drops corrections that teach nothing', () => {
  const c = (original: string, correcto: string) => ({ original, correcto, explicacion: '', skill: 'gramatica' as const });
  const quedan = (m: string, ...cs: ReturnType<typeof c>[]) => depurarCorrecciones(m, cs).map(x => x.correcto);
  // Dictado por voz: solo mayúsculas y puntuación.
  assert.deepEqual(quedan('hola me llamo john', c('hola me llamo john', 'Hola, me llamo John.')), []);
  // Autocorrección en el mismo mensaje.
  assert.deepEqual(quedan('Et dimanche je suis allé à le... au parc.', c('à le', 'au')), []);
  // Cita algo que el alumno no dijo.
  assert.deepEqual(quedan('Et dimanche je suis allé à le... au parc.', c('à le parc', 'au parc')), []);
  assert.deepEqual(quedan('Et dimanche je suis allé à le... au parc.', c('à le... au parc', 'au parc')), []);
  assert.deepEqual(quedan('This one is more better', c('more better', 'better')), ['better']);
  // Errores reales se quedan, aunque la forma buena aparezca más adelante en otro sitio.
  assert.deepEqual(quedan('Yesterday I go to the cinema', c('I go', 'I went')), ['I went']);
  assert.deepEqual(quedan('I am agree, is more comfortable', c('I am agree', 'I agree'), c('is more', 'it is more')), ['I agree', 'it is more']);
  assert.deepEqual(quedan('毎日学校を行きます。', c('学校を行きます', '学校に行きます')), ['学校に行きます']);
});

test('corrections already made in the call reach the tutor so repeats get a hint', () => {
  assert.equal(correccionesPrevias([]), '');
  assert.equal(correccionesPrevias([{ respuesta: { corrections: [] } }, { respuesta: null }]), '');
  const t = correccionesPrevias([{ respuesta: { corrections: [{ original: 'I go to the park', correcto: 'I went to the park', skill: 'conjugacion', explicacion: 'x' }] } }]);
  assert.match(t, /YA CORREGIDO/);
  assert.match(t, /I went to the park/);
  assert.doesNotMatch(t, /explicacion/);
});

test('the "X or Y?" hint is only offered when one word changed', () => {
  assert.deepEqual(tipoCambio('Meine Schwester hat Lehrerin', 'Meine Schwester ist Lehrerin'), { tipo: 'palabra', opciones: ['hat', 'ist'] });
  assert.deepEqual(tipoCambio('영화를 봐요', '영화를 봤어요'), { tipo: 'palabra', opciones: ['봐요', '봤어요'] });
  assert.deepEqual(tipoCambio('Il mela', 'La mela'), { tipo: 'palabra', opciones: ['il', 'la'] });
  assert.deepEqual(tipoCambio('Morgen ich gehe zum Arzt', 'Morgen gehe ich zum Arzt'), { tipo: 'orden' });
  assert.deepEqual(tipoCambio('I am agree', 'I agree'), { tipo: 'otro' });
  assert.deepEqual(tipoCambio('我的老师是很好', '我的老师很好'), { tipo: 'otro' });
  assert.match(correccionesPrevias([{ respuesta: { corrections: [{ original: 'Morgen ich gehe', correcto: 'Morgen gehe ich', skill: 'gramatica' }] } }]), /"tipo":"orden"/);
});

test('the prompt teaches how to correct and teach', () => {
  const p = systemPrompt({ idiomaMeta: 'en', idiomaNativo: 'es', nivel: 2, tutorId: 'avatar_frank' });
  assert.match(p, /CÓMO CORREGIR/);
  assert.match(p, /CÓMO ENSEÑAR/);
  assert.match(p, /Como máximo 1 corrección/);
  assert.match(p, /inglés estadounidense/);
  assert.match(systemPrompt({ idiomaMeta: 'es', idiomaNativo: 'en', nivel: 5, tutorId: 'avatar_diego' }), /Como máximo 2 correcciones[\s\S]*sin regionalismos/);
});

test('a network cut before the answer is retried, a cancellation is not', async () => {
  let llamadas = 0;
  globalThis.fetch = async () => {
    if (++llamadas === 1) throw new TypeError('fetch failed');
    return Response.json({ choices: [{ message: { content: '{"ok":true}' } }] });
  };
  try {
    assert.deepEqual((await generarJsonOpenAI('t', [], {})).json, { ok: true });
    assert.equal(llamadas, 2);
    llamadas = 0;
    globalThis.fetch = async () => { llamadas++; throw Object.assign(new Error('cancelado'), { name: 'AbortError' }); };
    await assert.rejects(generarTutorStream('t', [], () => {}, new AbortController().signal), /cancelado/);
    assert.equal(llamadas, 1);
  } finally { globalThis.fetch = originalFetch; }
});

test('the tutor keeps its limits and the corrector knows each language traps', () => {
  const p = systemPrompt({ idiomaMeta: 'ja', idiomaNativo: 'es', nivel: 2, tutorId: 'avatar_erik' });
  assert.match(p, /LÍMITES[\s\S]*número de emergencias[\s\S]*'reply' va en japonés aunque el alumno te pida responder en otro idioma/);
  assert.match(promptCorrector('ja', 'es', 2), /会う・乗る・なる・似る llevan に/);
  assert.match(promptCorrector('zh', 'es', 2), /我很高兴/);
  assert.doesNotMatch(promptCorrector('xx', 'es', 2), /Trampas típicas/);
});
