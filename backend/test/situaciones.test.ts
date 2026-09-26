import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { contextoSituacion, resumirCamino, unidades, lexicoSituaciones, materialSituacion } from '../src/lib/situaciones.js';
import { pool } from '../src/lib/db.js';
import { systemPrompt } from '../src/lib/ia.js';

test('all 50 units share stable objectives and identical frontend content', () => {
  const frontend = JSON.parse(readFileSync(new URL('../../assets/contenido/en/situaciones.json', import.meta.url), 'utf8'));
  assert.deepEqual(unidades, frontend);
  assert.deepEqual(unidades.map(u => u.id), Array.from({length: 50}, (_, i) => i + 1));
  const ids = unidades.flatMap(u => u.objetivos.map(o => o.id));
  assert.equal(new Set(ids).size, 150);
  for (const u of unidades) {
    assert.equal(u.objetivos.length, 3);
    assert.equal(new Set(u.vocabulario.map(w => w.es)).size, 3);
    assert.ok(u.objetivos.every(o => o.frase && o.traduccion && o.titulo));
  }
});
test('memory is bounded, language scoped, and does not treat clean chat as mastery', () => {
  const result = JSON.parse(resumirCamino({idiomaMeta: 'en', nivelInicial: 5, completadas: ['L1-001'], diagnostico: {idioma: 'fr', skills: {listening: 9}}, practicas: {
    old: {idioma: 'en', situacionId: 1, fecha: '2020', feedback: 'old'},
    current: {idioma: 'en', situacionId: 1, fecha: '2026', tipo: 'conversacion', feedback: 'clean', asistida: true},
    other: {idioma: 'es', situacionId: 1, feedback: 'foreign'},
    wrongUnit: {idioma: 'en', situacionId: 2, feedback: 'another situation'},
  }}, 'en', 1));
  assert.equal(result.evidencias.length, 2);
  assert.equal(result.evidencias[0].feedback, 'clean');
  assert.equal(result.evidencias[0].asistida, true);
  assert.equal(result.evidencias[0].resultado, undefined);
  assert.equal(result.competenciasDiagnostico, undefined);
  assert.deepEqual(result.leccionesRegistradas, ['L1-001']);
});
test('authoritative objective, authenticated history scope and no provider call for memory', async () => {
  const original = pool.query;
  const calls: any[] = [];
  (pool as any).query = async (sql: string, params: unknown[]) => {
    calls.push({sql, params});
    return {rows: sql.includes('FROM progreso') ? [{estado: {practicas: {}}}] : [{mensaje_alumno: 'I order soup', respuesta: {reply: 'What kind?', corrections: []}, fecha: '2026'}]};
  };
  try {
    const context = await contextoSituacion('student-a', {idiomaMeta: 'en', situacionId: 1, objetivoId: 's1-o2', modo: 'prueba', historial: []});
    assert.match(context, /Pedir y modificar un plato/);
    assert.match(context, /sin dar la respuesta/);
    assert.match(context, /NO permite medir pronunciación/);
    assert.deepEqual(calls[1].params, ['student-a', 'en', 1]);
    assert.match(calls[1].sql, /LIMIT 2/);
    assert.match(systemPrompt({idiomaMeta: 'en', idiomaNativo: 'es', nivel: 5, tutorId: 'mia', contexto: context}), /TURNOS ANTERIORES/);
    calls.length = 0;
    await contextoSituacion('student-a', {idiomaMeta:'en', situacionId: 1, historial: [{rol:'alumno'}, {rol:'alumno'}]});
    assert.equal(calls.length, 1, 'do not reload past conversations each turn');
    await assert.rejects(contextoSituacion('student-a', {idiomaMeta:'en', situacionId:1, objetivoId:'s2-o1', historial:[]}), /objetivo_invalido/);
  } finally { pool.query = original; }
});


test('expanded situational teaching matches app content and is scoped to one situation', () => {
  const frontend = JSON.parse(readFileSync(new URL('../../assets/contenido/en/situational_vocabulary.json', import.meta.url), 'utf8'));
  assert.deepEqual(lexicoSituaciones, frontend.situations);
  assert.equal(lexicoSituaciones.length, 50);
  assert.equal(lexicoSituaciones.flatMap(s => s.vocabulary).length, 400);
  assert.match(materialSituacion(1), /without cream/);
  assert.equal(materialSituacion(999), '');
  const context = JSON.parse(resumirCamino({practicas: {
    example: {idioma: 'en', situacionId: 1, tipo: 'comprobacion_guiada', correcta: true, conApoyo: true}
  }}, 'en', 1));
  assert.equal(context.evidencias[0].asistida, true);
  assert.equal(context.evidencias[0].resultado, true);
});
