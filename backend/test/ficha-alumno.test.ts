import { test } from 'node:test';
import assert from 'node:assert/strict';
import { pool } from '../src/lib/db.js';
import { actualizarFicha, textoFicha, type FichaAlumno } from '../src/lib/ficha_alumno.js';
import { contextoSituacion } from '../src/lib/situaciones.js';

const ficha: FichaAlumno = {
  sobreMi: ['Se llama Roger', 'Vive con sus padres', 'Es contador'], intereses: ['cantar', 'café'], objetivo: 'Hablar en el trabajo',
  comoHabla: 'Frases cortas, se queda a mitad de frase', domina: ['I like to…', 'I live with…'],
  errores: [{ patron: 'presente por pasado', ejemplo: 'Yesterday I go', correcto: 'Yesterday I went', veces: 4 }],
  comoAprende: ['Dale el comienzo de la frase cuando se queda a medias', 'Se molesta si le repites una pregunta'],
  plan: { foco: 'pasado simple de verbos frecuentes', porque: 'lo confunde con el presente', siguientes: ['preguntas con did'], avance: 'lo usa bien 3 veces sin ayuda' },
  pendiente: ['su grupo de canto'],
};

test('the profile reads like a teacher notebook: who, method and plan', () => {
  const t = textoFicha(ficha);
  assert.match(t, /Quién es: Se llama Roger; Vive con sus padres/);
  assert.match(t, /Errores que repite: presente por pasado \(«Yesterday I go» → «Yesterday I went», 4 veces\)/);
  assert.match(t, /CÓMO APRENDE \(su metodología: aplícala\): Dale el comienzo/);
  assert.match(t, /PLAN: foco actual «pasado simple de verbos frecuentes»[\s\S]*después: preguntas con did/);
  assert.doesNotMatch(textoFicha({ ...ficha, objetivo: '', pendiente: [] }), /Para qué aprende|Quedó pendiente/);
});

test('every turn carries the profile; a new learner is met first', async () => {
  const original = pool.query;
  let conFicha = true;
  (pool as any).query = async (sql: string) => ({ rows: sql.includes('FROM ficha_alumno') ? (conFicha ? [{ datos: ficha, actualizado_en: '2026-11-03' }] : []) : sql.includes('FROM progreso') ? [{ estado: {} }] : [] });
  try {
    const turno = await contextoSituacion('u1', { idiomaMeta: 'en', historial: [{ rol: 'alumno', texto: 'Hi' }, { rol: 'tutor', texto: 'Hi!' }, { rol: 'alumno', texto: 'I am fine' }] });
    assert.match(turno, /FICHA DEL ALUMNO[\s\S]*no le preguntes lo que ya figura aquí[\s\S]*Se llama Roger/);
    conFicha = false;
    assert.match(await contextoSituacion('u1', { idiomaMeta: 'en', historial: [] }), /PRIMERA VEZ CON ESTE ALUMNO/);
    assert.doesNotMatch(await contextoSituacion('u1', { idiomaMeta: 'en', historial: [{ rol: 'alumno', texto: 'a' }, { rol: 'alumno', texto: 'b' }] }), /PRIMERA VEZ/);
  } finally { pool.query = original; }
});

test('the profile is only rebuilt after enough new turns, without calling the AI', async () => {
  const original = pool.query, fetchOriginal = globalThis.fetch;
  let llamadasIa = 0;
  globalThis.fetch = (async () => { llamadasIa++; throw new Error('no debe llamar'); }) as typeof fetch;
  (pool as any).query = async (sql: string) => ({ rows: sql.includes('FROM conversaciones')
    ? [{ id: '9', mensaje_alumno: 'Hi', respuesta: { reply: 'Hi!' } }, { id: '8', mensaje_alumno: '[silencio]', respuesta: { reply: 'Tea?' } }, { id: '7', mensaje_alumno: 'Tea', respuesta: { reply: 'Nice' } }]
    : [] });
  try {
    assert.equal(await actualizarFicha('u1', 'en', 'es', 1), null);
    assert.equal(llamadasIa, 0);
  } finally { pool.query = original; globalThis.fetch = fetchOriginal; }
});
