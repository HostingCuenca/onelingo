import { test } from 'node:test';
import assert from 'node:assert/strict';
import { AJUSTES_TUTOR_DEFECTO, AjustesTutor } from '../src/lib/ajustes_tutor.js';
import { esEco, esOpciones, medirRepeticion, notaVariedad } from '../src/lib/variedad.js';
import { systemPrompt, type Turno } from '../src/lib/ia.js';
import { agruparLlamadas } from '../src/routes/tutor_ia.js';

const t = (rol: Turno['rol'], texto: string, espera?: Turno['espera']): Turno => ({ rol, texto, ...(espera ? { espera } : {}) });
const base = { idiomaMeta: 'en', idiomaNativo: 'es', nivel: 1, tutorId: 'avatar_frank' };

// Llamada real del 01-11-2026 (Frank, inglés N1): el alumno se quejó «Why do you repeat?».
const denver: Turno[] = [
  t('tutor', 'I’m Frank. Nice to meet you, Roger! Do you live in Denver or another city?'),
  t('alumno', 'I live with... Eh, my parents and my parents.'),
  t('tutor', 'You live with your parents. Do you live in Denver or another city?'),
  t('alumno', 'I live in a- And you?'),
  t('tutor', 'I live in Denver. Do you live in Denver or another city?'),
  t('alumno', 'You live with them or another city?'),
];

test('repeated questions, echoes and "X or Y?" chains are measured per call', () => {
  const m = medirRepeticion(denver);
  assert.equal(m.preguntasRepetidas, 2);
  assert.equal(m.opciones, 3);
  assert.equal(m.eco, 1);
  assert.ok(esEco('Coffee, yes. Do you drink it in the morning?', 'Coffee.'));
  // Celebrar la frase que le pidió repetir, o corregirla citando, no es eco.
  assert.ok(!esEco('Perfect, I went! What did you do there?', 'I went to the park.', { tipo: 'repetir', modelo: 'I went to the park.' }));
  assert.ok(!esEco('We say «I went to the park». Can you say it?', 'I go to the park.'));
  assert.ok(esOpciones('Where do you practice: at home or at work?'));
  assert.ok(esOpciones('¿Lo tomas caliente o frío?'));
  assert.ok(!esOpciones('What do you usually eat?', { tipo: 'responder', modelo: '' }));
  assert.deepEqual(medirRepeticion([t('tutor', 'Hi! Just a small thing: we say it.')], ['Just a small thing']).muletillas, { 'Just a small thing': 1 });
});

test('the turn note lists questions already asked and stops option chains', () => {
  const n = notaVariedad(denver, AJUSTES_TUTOR_DEFECTO);
  assert.match(n, /^\[Variedad, calculado por la app:/);
  assert.match(n, /Ya preguntaste en esta llamada: «Do you live in Denver or another city\?»/);
  assert.match(n, /pregunta abierta/);
  assert.match(n, /Empieza este de otra forma/);
  assert.equal(notaVariedad([t('alumno', 'Hi')], AJUSTES_TUTOR_DEFECTO), '');
  const eco = notaVariedad([t('alumno', 'Coffee.'), t('tutor', 'Coffee, yes. Morning or night?'), t('alumno', 'Morning.')], AJUSTES_TUTOR_DEFECTO);
  assert.match(eco, /repetiste lo que dijo el alumno/);
  assert.doesNotMatch(notaVariedad([t('alumno', 'Coffee.'), t('tutor', 'Coffee, yes. Morning or night?'), t('alumno', 'Morning.')], { ...AJUSTES_TUTOR_DEFECTO, eco: true }), /repetiste/);
  // Con «normal», una sola pregunta de opciones no dispara el aviso.
  assert.doesNotMatch(notaVariedad([t('tutor', 'Tea or coffee?'), t('alumno', 'Tea.')], { ...AJUSTES_TUTOR_DEFECTO, opciones: 'normal' }), /pregunta abierta/);
});

test('panel settings change the prompt: guided lesson, no echo, banned phrases, extra instructions', () => {
  const guiar = systemPrompt({ ...base, ajustes: AJUSTES_TUTOR_DEFECTO });
  assert.match(guiar, /CLASE GUIADA/);
  assert.match(guiar, /propón EL FOCO de hoy/);
  assert.match(guiar, /sin repetir ni parafrasear sus palabras/);
  assert.match(guiar, /NO TE REPITAS/);
  assert.match(guiar, /Nunca digas: "Just a small thing"/);
  assert.match(guiar, /solo si no logra responder/);
  const charla = systemPrompt({ ...base, ajustes: AjustesTutor.parse({ enfoque: 'conversar', opciones: 'normal', eco: true, pedirRepetir: false, instrucciones: 'Habla de deportes.' }) });
  assert.doesNotMatch(charla, /CLASE GUIADA/);
  assert.match(charla, /A Golden Retriever\? I love them!/);
  assert.match(charla, /en vez de pedirle que la repita/);
  assert.match(charla, /INDICACIONES DEL EQUIPO PEDAGÓGICO[\s\S]*Habla de deportes\.[\s\S]*FORMA\./);
  // Con situación, el foco es el objetivo de la escena.
  assert.match(systemPrompt({ ...base, situacion: 'Café', ajustes: AJUSTES_TUTOR_DEFECTO }), /El foco de la clase es el objetivo de la situación/);
});

test('saved turns are grouped into calls by learner, tutor and pauses', () => {
  const fila = (id: number, min: number, alumno: string, reply: string, tutor = 'avatar_frank') => ({
    id, fecha: new Date(Date.UTC(2026, 10, 1, 12, min)).toISOString(), usuario_id: 'u1', nombre: 'Ana', email: 'a@x', idioma: 'en', nivel: 1,
    tutor_id: tutor, situacion_id: null, mensaje_alumno: alumno, respuesta: { reply, corrections: [] },
  });
  const ls = agruparLlamadas([
    fila(1, 0, '', 'Hi! Tea or coffee?'), fila(2, 1, 'Coffee.', 'Coffee, yes. Hot or cold?'), fila(3, 2, '[silencio]', 'Hot or cold?'),
    fila(4, 50, '', 'Hello again!'), fila(5, 51, 'Hi', 'Hey!', 'avatar_chloe'),
  ], []);
  assert.equal(ls.length, 3);
  const primera = ls[ls.length - 1];
  assert.equal(primera.turnos.length, 3);
  assert.equal(primera.indicadores.eco, 1);
  assert.equal(primera.indicadores.opciones, 3);
});
