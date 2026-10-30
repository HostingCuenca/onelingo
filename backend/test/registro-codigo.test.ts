/**
 * Registro y recuperación con código por correo (lib/codigos.ts, /auth/registro/*,
 * /auth/clave/*) contra una base TEMPORAL (`onelingo_test_codigo_<pid>`, se borra
 * al terminar); sin Postgres local se omiten. Sin SMTP: el código se lee de la
 * bandeja `correos`, como en el panel.
 */
import { after, before, test } from 'node:test';
import assert from 'node:assert/strict';
import pg from 'pg';
process.env.LOG_LEVEL = 'silent';
process.env.SMTP_HOST = '';
import { config } from '../src/lib/config.js';
config.jwtSecret = 'test-only-codigo-secret';

const urlBase = config.databaseUrl;
const NOMBRE_BD = `onelingo_test_codigo_${process.pid}`;
let hayBd = false;
try {
  const c = new pg.Client({ connectionString: urlBase, connectionTimeoutMillis: 2000 });
  await c.connect();
  await c.query(`CREATE DATABASE ${NOMBRE_BD}`);
  await c.end();
  const u = new URL(urlBase); u.pathname = '/' + NOMBRE_BD;
  config.databaseUrl = u.toString();
  hayBd = true;
} catch { /* sin Postgres local */ }
const sinBd = hayBd ? false : 'sin Postgres local';

const { pool } = await import('../src/lib/db.js');
const { migrar } = await import('../src/migrate.js');
const { crearApp } = await import('../src/app.js');
const { normalizarTelefono } = await import('../src/lib/codigos.js');
let app: Awaited<ReturnType<typeof crearApp>>;

before(async () => { if (!hayBd) return; await migrar(); app = await crearApp(); });
after(async () => {
  if (!hayBd) return;
  await app?.close();
  await pool.end();
  const c = new pg.Client({ connectionString: urlBase }); await c.connect();
  await c.query(`DROP DATABASE IF EXISTS ${NOMBRE_BD} WITH (FORCE)`); await c.end();
});

const post = (url: string, payload: object) => app.inject({ method: 'POST', url, payload });
const ultimoCodigo = async (para: string) =>
  (await pool.query('SELECT asunto FROM correos WHERE para = $1 ORDER BY id DESC LIMIT 1', [para])).rows[0]?.asunto.match(/^(\d{6}) /)?.[1] as string;
const DATOS = { email: 'Lucia@Codigo.test', password: 'clave-segura', nombre: 'Lucía', apellido: 'Pérez', telefono: '+1 (555) 123-4567', idiomaMeta: 'fr' };
const ponerEnviadoEn = (email: string, proposito: string, haceSegundos: number) =>
  pool.query(`UPDATE codigos_correo SET enviado_en = now() - make_interval(secs => $3) WHERE email = $1 AND proposito = $2`, [email, proposito, haceSegundos]);

test('teléfono: exige código de país y quita espacios, guiones y paréntesis', () => {
  assert.equal(normalizarTelefono('+1 (555) 123-4567'), '+15551234567');
  assert.equal(normalizarTelefono('+52 55 1234 5678'), '+525512345678');
  assert.equal(normalizarTelefono('555 123 4567'), null);
  assert.equal(normalizarTelefono('+0 123'), null);
});

test('registro con código: no crea la cuenta hasta verificar; luego entra verificada con apellido y teléfono', { skip: sinBd }, async () => {
  const r1 = await post('/auth/registro/codigo', DATOS);
  assert.equal(r1.statusCode, 200, r1.body);
  const email = 'lucia@codigo.test';
  assert.equal((await pool.query('SELECT 1 FROM usuarios WHERE email = $1', [email])).rowCount, 0);
  const codigo = await ultimoCodigo(email);
  assert.match(codigo, /^\d{6}$/);
  // El código nunca se guarda en claro.
  const fila = (await pool.query('SELECT codigo_hash, datos FROM codigos_correo WHERE email = $1', [email])).rows[0];
  assert.ok(!fila.codigo_hash.includes(codigo));
  assert.ok(!JSON.stringify(fila.datos).includes('clave-segura'));

  const otro = codigo === '000000' ? '111111' : '000000';
  const mal = await post('/auth/registro/verificar', { email, codigo: otro });
  assert.equal(mal.statusCode, 400);
  assert.match(mal.json().error, /Te quedan 4 intentos/);

  const ok = await post('/auth/registro/verificar', { email, codigo });
  assert.equal(ok.statusCode, 201, ok.body);
  assert.ok(ok.json().token);
  const u = (await pool.query('SELECT nombre, apellido, telefono, email_verificado, idioma_meta FROM usuarios WHERE email = $1', [email])).rows[0];
  assert.deepEqual(u, { nombre: 'Lucía', apellido: 'Pérez', telefono: '+15551234567', email_verificado: true, idioma_meta: 'fr' });
  // El código se consume: no sirve dos veces.
  assert.equal((await post('/auth/registro/verificar', { email, codigo })).statusCode, 410);
  // Y ya inicia sesión con su contraseña.
  assert.equal((await post('/auth/login', { email, password: 'clave-segura' })).statusCode, 200);
  // Registrarse otra vez con el mismo correo no manda código.
  assert.equal((await post('/auth/registro/codigo', DATOS)).statusCode, 409);
});

test('registro con código: valida los datos con mensajes claros', { skip: sinBd }, async () => {
  const sinApellido = await post('/auth/registro/codigo', { ...DATOS, email: 'a@codigo.test', apellido: ' ' });
  assert.equal(sinApellido.statusCode, 400);
  assert.equal(sinApellido.json().error, 'Escribe tu apellido.');
  // Con la app en inglés, el mensaje y el correo van en inglés.
  const en = await app.inject({ method: 'POST', url: '/auth/registro/codigo', headers: { 'x-idioma': 'en' }, payload: { ...DATOS, email: 'a@codigo.test', apellido: '' } });
  assert.equal(en.json().error, 'Enter your last name.');
  const enOk = await app.inject({ method: 'POST', url: '/auth/registro/codigo', headers: { 'x-idioma': 'en' }, payload: { ...DATOS, email: 'en@codigo.test' } });
  assert.equal(enOk.statusCode, 200);
  const asunto = (await pool.query("SELECT asunto FROM correos WHERE para = 'en@codigo.test'")).rows[0].asunto;
  assert.match(asunto, /^\d{6} is your OneLingo code$/);
  const sinPais = await post('/auth/registro/codigo', { ...DATOS, email: 'a@codigo.test', telefono: '555 123 4567' });
  assert.equal(sinPais.statusCode, 400);
  assert.match(sinPais.json().error, /código de país/);
});

test('código: reenvío tras 60 s, 5 intentos como máximo y caduca a los 10 minutos', { skip: sinBd }, async () => {
  const email = 'reenvio@codigo.test';
  assert.equal((await post('/auth/registro/codigo', { ...DATOS, email })).statusCode, 200);
  const pronto = await post('/auth/registro/codigo', { ...DATOS, email });
  assert.equal(pronto.statusCode, 429);
  assert.ok(pronto.json().reenviarEn > 0);
  await ponerEnviadoEn(email, 'registro', 61);
  assert.equal((await post('/auth/registro/codigo', { ...DATOS, email })).statusCode, 200);
  const codigo = await ultimoCodigo(email);
  const otro = codigo === '000000' ? '111111' : '000000';
  for (let i = 0; i < 5; i++) await post('/auth/registro/verificar', { email, codigo: otro });
  // Agotados los intentos, ni el código bueno sirve.
  assert.equal((await post('/auth/registro/verificar', { email, codigo })).statusCode, 429);

  await ponerEnviadoEn(email, 'registro', 61);
  assert.equal((await post('/auth/registro/codigo', { ...DATOS, email })).statusCode, 200);
  const nuevo = await ultimoCodigo(email);
  await pool.query("UPDATE codigos_correo SET expira = now() - interval '1 second' WHERE email = $1", [email]);
  assert.equal((await post('/auth/registro/verificar', { email, codigo: nuevo })).statusCode, 410);
});

test('olvidé mi contraseña con código: no revela si la cuenta existe y deja entrar con la nueva', { skip: sinBd }, async () => {
  const nadie = await post('/auth/clave/codigo', { email: 'nadie@codigo.test' });
  assert.equal(nadie.statusCode, 200);
  assert.equal(await ultimoCodigo('nadie@codigo.test'), undefined);

  const email = 'lucia@codigo.test';
  assert.equal((await post('/auth/clave/codigo', { email })).statusCode, 200);
  const codigo = await ultimoCodigo(email);
  const r = await post('/auth/clave/restablecer', { email, codigo, password: 'otra-clave-1' });
  assert.equal(r.statusCode, 200, r.body);
  assert.ok(r.json().token);
  assert.equal((await post('/auth/login', { email, password: 'clave-segura' })).statusCode, 401);
  assert.equal((await post('/auth/login', { email, password: 'otra-clave-1' })).statusCode, 200);
});

test('panel: el listado y el CSV traen apellido, teléfono y correo verificado', { skip: sinBd }, async () => {
  const { COLUMNAS_CSV } = await import('../src/routes/admin.js');
  for (const c of ['apellido', 'telefono', 'email_verificado']) assert.ok(COLUMNAS_CSV.includes(c), c);
  const login = await post('/admin/login', { usuario: config.adminUsuario, pin: config.adminPin });
  const token = login.json().token;
  const r = await app.inject({ method: 'GET', url: '/admin/usuarios?q=5551234', headers: { authorization: `Bearer ${token}` } });
  assert.equal(r.statusCode, 200, r.body);
  const fila = r.json().filas.find((f: any) => f.email === 'lucia@codigo.test');
  assert.equal(fila.apellido, 'Pérez');
  assert.equal(fila.telefono, '+15551234567');
  assert.equal(fila.email_verificado, true);
});
