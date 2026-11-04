import { test } from 'node:test';
import assert from 'node:assert/strict';
import { pool } from '../src/lib/db.js';
import { htmlCertificado, nivelSuperado, nombreCertificado, nuevoCodigo, type Certificado } from '../src/routes/certificados.js';

const UID = '11111111-1111-4111-8111-111111111111';
async function montar() {
  const { default: Fastify } = await import('fastify');
  const { default: jwt } = await import('@fastify/jwt');
  const { default: rutas } = await import('../src/routes/certificados.js');
  const app = Fastify(); await app.register(jwt, { secret: 'test-only-cert-secret' }); await app.register(rutas);
  return { app, alumno: { authorization: `Bearer ${app.jwt.sign({ sub: UID, rol: 'alumno' })}` } };
}

test('a level counts when all its classes or its test were passed', () => {
  const p = {
    'ruta:en.n1:completa': { tipo: 'nivel_completo', primeraFecha: '2026-10-20T15:00:00Z' },
    'ruta:en.n2:prueba': { aprobada: false, fecha: '2026-10-21T15:00:00Z' },
    'ruta:en.n3:prueba': { aprobada: true, fecha: '2026-10-22T15:00:00Z' },
  };
  assert.deepEqual(nivelSuperado(p, 'en', 'n1'), { via: 'clases', fecha: '2026-10-20T15:00:00Z' });
  assert.equal(nivelSuperado(p, 'en', 'n2'), null);
  assert.equal(nivelSuperado(p, 'fr', 'n1'), null);
  assert.equal(nivelSuperado(p, 'en', 'n3')?.via, 'prueba');
});

test('names and codes are printable', () => {
  assert.equal(nombreCertificado('  María   José  '), 'María José');
  assert.equal(nombreCertificado('roger.t@gmail.com'), 'roger.t');
  assert.match(nuevoCodigo(), /^[A-Z2-9]{5}-[A-Z2-9]{5}$/);
  assert.doesNotMatch(Array.from({ length: 200 }, nuevoCodigo).join(''), /[01OIL]/);
});

test('the public page escapes the name and speaks the learner language', () => {
  const c: Certificado = { codigo: 'ABCDE-FGHJK', idioma: 'en', nivel: 'n3', nombre: '<b>Ana</b>', via: 'clases', lengua: 'es', logrado_en: '2026-10-22T15:00:00Z', emitido_en: '2026-11-03T15:00:00Z' };
  const es = htmlCertificado(c);
  assert.match(es, /&lt;b&gt;Ana&lt;\/b&gt;/);
  assert.match(es, /por completar el <b>Nivel 3<\/b> del curso de <b>inglés<\/b>/);
  assert.match(es, /22 de octubre de 2026/);
  assert.match(es, /noindex/);
  const en = htmlCertificado({ ...c, lengua: 'en', via: 'prueba', idioma: 'ja' });
  assert.match(en, /for passing the <b>Level 3<\/b> test of the OneLingo <b>Japanese<\/b> course/);
  assert.match(en, /October 22, 2026/);
});

test('the server only issues a certificate the synced progress confirms', async () => {
  const original = pool.query;
  const sqls: { sql: string; params: unknown[] }[] = [];
  let practicas: Record<string, unknown> = {};
  (pool as any).query = async (sql: string, params: unknown[] = []) => {
    sqls.push({ sql, params });
    if (sql.includes('FROM usuarios')) return { rows: [{ nombre: 'Ana Pérez' }] };
    if (sql.includes('FROM progreso')) return { rows: [{ estado: { practicas } }] };
    if (sql.includes('INSERT INTO certificados')) return { rows: [{ codigo: params[0], idioma: params[2], nivel: params[3], nombre: params[4], via: params[5], lengua: params[6], logrado_en: params[7], emitido_en: '2026-11-03T15:00:00Z' }] };
    if (sql.includes('FROM certificados WHERE codigo')) return { rows: [] };
    return { rows: [] };
  };
  const { app, alumno } = await montar();
  try {
    const sin = await app.inject({ method: 'POST', url: '/certificados', headers: alumno, payload: { idioma: 'en', nivel: 'n2' } });
    assert.equal(sin.statusCode, 409);
    assert.equal(sqls.some((q) => q.sql.includes('INSERT INTO certificados')), false);

    practicas = { 'ruta:en.n2:completa': { primeraFecha: '2026-11-01T12:00:00Z' } };
    const r = await app.inject({ method: 'POST', url: '/certificados', headers: alumno, payload: { idioma: 'en', nivel: 'n2' } });
    assert.equal(r.statusCode, 200);
    const c = r.json();
    assert.equal(c.nombre, 'Ana Pérez');
    assert.equal(c.via, 'clases');
    assert.match(c.url, new RegExp(`/certificado/${c.codigo}$`));
    const ins = sqls.find((q) => q.sql.includes('INSERT INTO certificados'))!;
    assert.equal(ins.params[8], false, 'without a name the printed one is kept');

    const corregido = await app.inject({ method: 'POST', url: '/certificados', headers: alumno, payload: { idioma: 'en', nivel: 'n2', nombre: ' Ana  María Pérez ' } });
    assert.equal(corregido.json().nombre, 'Ana María Pérez');

    assert.equal((await app.inject({ method: 'POST', url: '/certificados', headers: alumno, payload: { idioma: 'en', nivel: 'f0' } })).statusCode >= 400, true, 'Fundamentos no lleva certificado');
    assert.equal((await app.inject({ method: 'POST', url: '/certificados', payload: { idioma: 'en', nivel: 'n2' } })).statusCode, 401);
    const falta = await app.inject({ method: 'GET', url: '/certificado/XXXXX-YYYYY' });
    assert.equal(falta.statusCode, 404);
    assert.match(falta.body, /Certificado no encontrado/);
  } finally { pool.query = original; await app.close(); }
});
