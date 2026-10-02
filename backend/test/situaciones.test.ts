import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { contextoSituacion, resumirCamino, situacionesDe, materialSituacion, objetivoValido, tramoDeNivel } from '../src/lib/situaciones.js';
import { pool } from '../src/lib/db.js';
import { systemPrompt } from '../src/lib/ia.js';

test('situaciones v2: copia generada idéntica a la fuente, 50 × 3 tramos', () => {
  const fuente = JSON.parse(readFileSync(new URL('../../assets/contenido/en/situaciones.json', import.meta.url), 'utf8'));
  const unidades = situacionesDe('en');
  assert.deepEqual(unidades.map(u => ({ id: u.id, tramos: u.tramos })), fuente.situaciones);
  assert.deepEqual(unidades.map(u => u.id), Array.from({length: 50}, (_, i) => i + 1));
  const ids = unidades.flatMap(u => Object.values(u.tramos).flatMap(t => t.objetivos.map(o => o.id)));
  assert.equal(new Set(ids).size, 450);
  for (const u of unidades) for (const t of Object.values(u.tramos)) {
    assert.equal(t.objetivos.length, 3);
    assert.equal(t.vocabulario.length, 10);
    assert.ok(t.objetivos.every(o => o.frase && o.traduccion && o.titulo));
  }
  assert.deepEqual(situacionesDe('de'), []);
  assert.deepEqual(situacionesDe('../x'), []);
});
test('objetivos de cualquier tramo son válidos solo en su situación', () => {
  assert.ok(objetivoValido('en', 1, 's1-o2'));
  assert.ok(objetivoValido('en', 1, 's1-i1'));
  assert.ok(objetivoValido('en', 1, 's1-a3'));
  assert.equal(objetivoValido('en', 2, 's1-i1'), false);
  assert.equal(objetivoValido('de', 1, 's1-o1'), false);
  assert.equal(tramoDeNivel(3), 'basico');
  assert.equal(tramoDeNivel(4), 'intermedio');
  assert.equal(tramoDeNivel(9), 'avanzado');
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


test('el material enseña solo el tramo pedido', () => {
  const u = situacionesDe('en')[0];
  const intermedio = materialSituacion(u, 'intermedio');
  assert.match(intermedio, /intermedio/);
  assert.ok(intermedio.includes(u.tramos.intermedio.vocabulario[0].en));
  assert.ok(!intermedio.includes(JSON.stringify(u.tramos.avanzado.vocabulario[0].en)));
  const context = JSON.parse(resumirCamino({practicas: {
    example: {idioma: 'en', situacionId: 1, tipo: 'comprobacion_guiada', correcta: true, conApoyo: true}
  }}, 'en', 1));
  assert.equal(context.evidencias[0].asistida, true);
  assert.equal(context.evidencias[0].resultado, true);
});

test('francés: situaciones bilingües, objetivos válidos y prompt con el título en español', async () => {
  const fr = situacionesDe('fr');
  assert.equal(fr.length, 50);
  assert.ok(objetivoValido('fr', 1, 's1-o1'));
  assert.ok(objetivoValido('fr', 50, 's50-a3'));
  assert.equal(objetivoValido('fr', 1, 's2-o1'), false);
  const original = pool.query;
  (pool as any).query = async () => ({ rows: [] });
  try {
    const ctx = await contextoSituacion('x', { idiomaMeta: 'fr', nivel: 2, situacionId: 1, objetivoId: 's1-o1', historial: [] });
    assert.ok(!ctx.includes('[object Object]'));
    assert.match(ctx, /Objetivo activo: /);
  } finally { pool.query = original; }
});
