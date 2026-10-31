/**
 * Requisitos de Google Play: eliminar la cuenta (`DELETE /usuarios/me`, lib/cuenta.ts)
 * y denunciar respuestas de la IA (`/reportes-ia`, routes/reportes.ts).
 * Contra una base TEMPORAL (`onelingo_test_cuenta_<pid>`, se borra al terminar);
 * sin Postgres local se omiten. Stripe se simula con `fetch` (clave inventada):
 * nunca se llama a Stripe de verdad.
 */
import { after, before, test } from 'node:test';
import assert from 'node:assert/strict';
import pg from 'pg';
process.env.LOG_LEVEL = 'silent';
process.env.SMTP_HOST = '';
process.env.STRIPE_SECRET_KEY = 'sk_test_' + 'cuentaPrueba0123456789'.repeat(3);
delete process.env.STRIPE_WEBHOOK_SECRET;
import { config } from '../src/lib/config.js';
config.jwtSecret = 'test-only-cuenta-secret';

const urlBase = config.databaseUrl;
const NOMBRE_BD = `onelingo_test_cuenta_${process.pid}`;
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
const { REPORTES_POR_HORA } = await import('../src/routes/reportes.js');
let app: Awaited<ReturnType<typeof crearApp>>;

// ── Stripe simulado ──────────────────────────────────────────────────────────
const st = { llamadas: [] as string[] };
const fetchOriginal = globalThis.fetch;
const json = (status: number, body: unknown) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
globalThis.fetch = (async (entrada: any, init: any = {}) => {
  const url = new URL(String(entrada));
  if (url.hostname !== 'api.stripe.com') return fetchOriginal(entrada, init);
  const metodo = init.method ?? 'GET', ruta = url.pathname.replace(/^\/v1/, '');
  st.llamadas.push(`${metodo} ${ruta}`);
  const m = /^\/subscriptions\/(\w+)$/.exec(ruta);
  if (metodo === 'DELETE' && m) {
    if (m[1] === 'sub_borrada') return json(404, { error: { message: 'No such subscription', type: 'invalid_request_error' } });
    if (m[1] === 'sub_falla') return json(500, { error: { message: 'Stripe se cayó', type: 'api_error' } });
    return json(200, { id: m[1], object: 'subscription', status: 'canceled' });
  }
  return json(404, { error: { message: `ruta simulada desconocida: ${metodo} ${ruta}` } });
}) as typeof fetch;

before(async () => { if (!hayBd) return; await migrar(); app = await crearApp(); });
after(async () => {
  globalThis.fetch = fetchOriginal;
  if (!hayBd) return;
  await app?.close();
  await pool.end();
  const c = new pg.Client({ connectionString: urlBase }); await c.connect();
  await c.query(`DROP DATABASE IF EXISTS ${NOMBRE_BD} WITH (FORCE)`); await c.end();
});

const tok = (sub: string, rol: 'alumno' | 'admin' = 'alumno') => ({ authorization: `Bearer ${app.jwt.sign({ sub, rol })}` });
const borrar = (sub: string) => app.inject({ method: 'DELETE', url: '/usuarios/me', headers: tok(sub) });
const crear = (email: string, demo = false) =>
  pool.query('INSERT INTO usuarios (email, nombre, apellido, telefono, es_demo) VALUES ($1, $2, $3, $4, $5) RETURNING id', [email, 'Nombre', 'Apellido', '+15551234567', demo])
    .then((r) => r.rows[0].id as string);
const existe = async (id: string) => (await pool.query('SELECT 1 FROM usuarios WHERE id = $1', [id])).rowCount === 1;
const cuenta = async (tabla: string, donde: string, valor: unknown) => (await pool.query(`SELECT count(*)::int AS n FROM ${tabla} WHERE ${donde}`, [valor])).rows[0].n as number;
const susStripe = (uid: string, subId: string, o: { estado?: string; modo?: string; cancelaAlFinal?: boolean } = {}) => pool.query(
  `INSERT INTO suscripciones (usuario_id, plan_id, origen, estado, modo, cancela_al_final, stripe_cliente_id, stripe_suscripcion_id, importe_centavos, moneda, meses)
   VALUES ($1, 'p1', 'stripe', $2, $3, $4, 'cus_prueba', $5, 2000, 'usd', 1)`, [uid, o.estado ?? 'activa', o.modo ?? 'test', !!o.cancelaAlFinal, subId]);

// ── Eliminar la cuenta ───────────────────────────────────────────────────────
test('eliminar cuenta: sin sesión 401; las cuentas demo NO se borran (403), Ana sigue entrando', { skip: sinBd }, async () => {
  assert.equal((await app.inject({ method: 'DELETE', url: '/usuarios/me' })).statusCode, 401);
  const ana = await crear('ana@onelingo.demo', true);
  const r = await borrar(ana);
  assert.equal(r.statusCode, 403, r.body);
  assert.equal(r.json().codigo, 'cuenta_demo');
  assert.ok(await existe(ana));
  // Aunque la marca es_demo falte, el dominio @onelingo.demo basta.
  const otra = await crear('Beto@OneLingo.Demo', false);
  assert.equal((await borrar(otra)).statusCode, 403);
  assert.ok(await existe(otra));
  // Y Ana sigue iniciando sesión.
  const login = await app.inject({ method: 'POST', url: '/usuarios/login', payload: { email: 'ana@onelingo.demo' } });
  assert.equal(login.statusCode, 200, login.body);
});

test('eliminar cuenta: borra usuario y datos, cancela Stripe y deja solo el registro de pago sin datos personales', { skip: sinBd }, async () => {
  const email = 'lucia@cuenta.test';
  const uid = await crear(email);
  const otro = await crear('otro@cuenta.test');
  await pool.query(`INSERT INTO progreso (usuario_id, estado) VALUES ($1, '{}')`, [uid]);
  await pool.query(`INSERT INTO errores (id, usuario_id, skill, original, correccion) VALUES ('e1', $1, 'gramatica', 'I has', 'I have')`, [uid]);
  await pool.query('INSERT INTO examenes (usuario_id, nivel, pct, aprobado) VALUES ($1, 1, 80, true)', [uid]);
  await pool.query(`INSERT INTO eventos (usuario_id, tipo) VALUES ($1, 'login'), ($2, 'login')`, [uid, otro]);
  await pool.query(`INSERT INTO conversaciones (usuario_id, nivel, idioma, tutor_id, mensaje_alumno, respuesta) VALUES ($1, 1, 'en', 'mia', 'hola', '{}')`, [uid]);
  await pool.query(`INSERT INTO correos (para, asunto, cuerpo) VALUES ($1, 'Tu código', 'x'), ('otro@cuenta.test', 'Tu código', 'x')`, [email.toUpperCase()]);
  await pool.query(`INSERT INTO codigos_correo (email, proposito, codigo_hash, expira) VALUES ($1, 'clave', 'h', now() + interval '10 minutes')`, [email]);
  await pool.query(`INSERT INTO cotizaciones (empresa, empleados, email, usuario_id) VALUES ('ACME', 5, $1, $2)`, [email, uid]);
  await pool.query(`INSERT INTO reportes_ia (usuario_id, origen, motivo, texto) VALUES ($1, 'chat', 'otro', 'x')`, [uid]);
  await susStripe(uid, 'sub_lucia');

  st.llamadas = [];
  const r = await borrar(uid);
  assert.equal(r.statusCode, 200, r.body);
  assert.deepEqual(r.json(), { ok: true, stripeCancelada: true, googlePlay: null });
  assert.deepEqual(st.llamadas, ['DELETE /subscriptions/sub_lucia']);
  assert.equal(await existe(uid), false);
  for (const t of ['progreso', 'errores', 'examenes', 'eventos', 'conversaciones', 'suscripciones', 'cotizaciones', 'reportes_ia']) {
    assert.equal(await cuenta(t, 'usuario_id = $1', uid), 0, t);
  }
  assert.equal(await cuenta('correos', 'lower(para) = $1', email), 0);
  assert.equal(await cuenta('codigos_correo', 'email = $1', email), 0);
  // Lo de otras cuentas no se toca.
  assert.ok(await existe(otro));
  assert.equal(await cuenta('eventos', 'usuario_id = $1', otro), 1);
  assert.equal(await cuenta('correos', 'para = $1', 'otro@cuenta.test'), 1);
  // Registro del pago: referencias de Stripe, sin correo ni nombre.
  const fila = (await pool.query(`SELECT * FROM cuentas_eliminadas WHERE stripe_suscripcion_id = 'sub_lucia'`)).rows[0];
  assert.equal(fila.origen_pago, 'stripe'); assert.equal(fila.estado_pago, 'cancelada'); assert.equal(fila.accion, 'cancelada_stripe');
  assert.equal(fila.importe_centavos, 2000);
  assert.ok(!JSON.stringify(fila).includes(email) && !JSON.stringify(fila).includes('Apellido') && !JSON.stringify(fila).includes('+1555'), 'sin datos personales');
  // El token viejo ya no sirve para borrar otra vez.
  assert.equal((await borrar(uid)).statusCode, 404);
});

test('eliminar cuenta: si Stripe falla no se borra nada (502); si la suscripción ya no existe en Stripe, se borra', { skip: sinBd }, async () => {
  const a = await crear('falla@cuenta.test');
  await susStripe(a, 'sub_falla');
  const r = await borrar(a);
  assert.equal(r.statusCode, 502, r.body);
  assert.equal(r.json().codigo, 'cancelacion_fallida');
  assert.match(r.json().error, /infoonelingo@gmail\.com/);
  assert.ok(await existe(a));
  assert.equal(await cuenta('suscripciones', 'usuario_id = $1', a), 1);

  const b = await crear('borrada@cuenta.test');
  await susStripe(b, 'sub_borrada');
  const r2 = await borrar(b);
  assert.equal(r2.statusCode, 200, r2.body);
  assert.equal(r2.json().stripeCancelada, false);
  assert.equal(await existe(b), false);
  assert.equal((await pool.query(`SELECT accion FROM cuentas_eliminadas WHERE stripe_suscripcion_id = 'sub_borrada'`)).rows[0].accion, 'ya_cancelada');

  // Suscripción ya cancelada: no se llama a Stripe.
  const c = await crear('cancelada@cuenta.test');
  await susStripe(c, 'sub_vieja', { estado: 'cancelada' });
  st.llamadas = [];
  assert.equal((await borrar(c)).statusCode, 200);
  assert.deepEqual(st.llamadas, []);
});

test('eliminar cuenta: suscripción real (live) que este servidor no puede cancelar → 503 y no se borra', { skip: sinBd }, async () => {
  const a = await crear('live@cuenta.test');
  await susStripe(a, 'sub_live', { modo: 'live' });
  st.llamadas = [];
  const r = await borrar(a);
  assert.equal(r.statusCode, 503, r.body);
  assert.equal(r.json().codigo, 'cancelacion_no_disponible');
  assert.deepEqual(st.llamadas, []);
  assert.ok(await existe(a));
});

test('eliminar cuenta: con Google Play activa se borra igual y avisa de cancelarla en Google Play', { skip: sinBd }, async () => {
  const uid = await crear('google@cuenta.test');
  await pool.query(`INSERT INTO suscripciones (usuario_id, plan_id, origen, estado, modo, google_token, google_producto, google_pedido, periodo_fin)
    VALUES ($1, 'p1', 'google', 'activa', 'test', 'tok-google', 'plan_p1', 'GPA.1234', now() + interval '20 days')`, [uid]);
  st.llamadas = [];
  const r = await borrar(uid);
  assert.equal(r.statusCode, 200, r.body);
  assert.deepEqual(r.json().googlePlay, { debeCancelar: true, producto: 'plan_p1' });
  assert.deepEqual(st.llamadas, []);
  assert.equal(await existe(uid), false);
  const fila = (await pool.query(`SELECT origen_pago, google_pedido, accion FROM cuentas_eliminadas WHERE google_pedido = 'GPA.1234'`)).rows[0];
  assert.deepEqual(fila, { origen_pago: 'google', google_pedido: 'GPA.1234', accion: 'cancelar_en_google_play' });

  // Ya cancelada en Google Play (no se renueva): no hace falta avisar.
  const otro = await crear('google2@cuenta.test');
  await pool.query(`INSERT INTO suscripciones (usuario_id, plan_id, origen, estado, cancela_al_final, modo, google_token, periodo_fin)
    VALUES ($1, 'p1', 'google', 'activa', true, 'test', 'tok-google-2', now() + interval '5 days')`, [otro]);
  assert.equal((await borrar(otro)).json().googlePlay.debeCancelar, false);
});

test('eliminar cuenta: el titular de un plan familiar se va y sus miembros pierden el reflejo', { skip: sinBd }, async () => {
  const titular = await crear('titular@cuenta.test');
  const miembro = await crear('miembro@cuenta.test');
  await pool.query(`INSERT INTO suscripciones (usuario_id, plan_id, origen, estado) VALUES ($1, 'familiar', 'cortesia', 'activa')`, [titular]);
  await pool.query(`INSERT INTO familia_miembros (titular_id, email, usuario_id) VALUES ($1, 'miembro@cuenta.test', $2), ($1, 'pendiente@cuenta.test', NULL)`, [titular, miembro]);
  await pool.query(`INSERT INTO suscripciones (usuario_id, plan_id, origen, estado, titular_id) VALUES ($1, 'familiar', 'familia', 'activa', $2)`, [miembro, titular]);
  await pool.query(`UPDATE usuarios SET plan_id = 'familiar' WHERE id = ANY($1)`, [[titular, miembro]]);

  assert.equal((await borrar(titular)).statusCode, 200);
  assert.ok(await existe(miembro));
  assert.equal(await cuenta('suscripciones', 'usuario_id = $1', miembro), 0);
  assert.equal(await cuenta('familia_miembros', 'titular_id = $1', titular), 0);
  assert.equal((await pool.query('SELECT plan_id FROM usuarios WHERE id = $1', [miembro])).rows[0].plan_id, '');
  // Cortesía: no es un pago, no deja registro.
  assert.equal(await cuenta('cuentas_eliminadas', 'plan_id = $1', 'familiar'), 0);
});

// ── Reportes de la IA ────────────────────────────────────────────────────────
test('reportes IA: se guardan con usuario y fecha; validan origen, motivo y longitudes', { skip: sinBd }, async () => {
  const uid = await crear('reporta@cuenta.test');
  const post = (payload: object, sub = uid) => app.inject({ method: 'POST', url: '/reportes-ia', headers: tok(sub), payload });
  assert.equal((await app.inject({ method: 'POST', url: '/reportes-ia', payload: { origen: 'chat', texto: 'x', motivo: 'otro' } })).statusCode, 401);
  const ok = await post({ origen: 'chat', texto: '  You are stupid.  ', motivo: 'ofensivo', comentario: 'Me insultó', contexto: { idioma: 'en', tutorId: 'mia', situacion: 12, extra: 'fuera' } });
  assert.equal(ok.statusCode, 201, ok.body);
  const fila = (await pool.query('SELECT usuario_id, origen, motivo, texto, comentario, contexto, revisado, creado_en FROM reportes_ia WHERE id = $1', [ok.json().id])).rows[0];
  assert.equal(fila.usuario_id, uid);
  assert.equal(fila.texto, 'You are stupid.');
  assert.deepEqual(fila.contexto, { idioma: 'en', tutorId: 'mia', situacion: 12 });
  assert.equal(fila.revisado, false);
  assert.ok(Date.now() - new Date(fila.creado_en).getTime() < 60_000);
  // Sin comentario ni contexto también vale (videollamada).
  assert.equal((await post({ origen: 'llamada', texto: 'Bonjour', motivo: 'incorrecto' })).statusCode, 201);

  assert.equal((await post({ origen: 'chat', texto: 'x', motivo: 'feo' })).statusCode, 400);
  assert.equal((await post({ origen: 'correo', texto: 'x', motivo: 'otro' })).statusCode, 400);
  assert.equal((await post({ origen: 'chat', texto: '   ', motivo: 'otro' })).statusCode, 400);
  assert.equal((await post({ origen: 'chat', texto: 'a'.repeat(2001), motivo: 'otro' })).statusCode, 400);
  assert.equal((await post({ origen: 'chat', texto: 'a'.repeat(2000), motivo: 'otro', comentario: 'b'.repeat(501) })).statusCode, 400);
  assert.equal((await post({ origen: 'chat', texto: 'a'.repeat(2000), motivo: 'otro', comentario: 'b'.repeat(500) })).statusCode, 201);
});

test(`reportes IA: máximo ${REPORTES_POR_HORA} por alumno y hora (429); otro alumno no se ve afectado`, { skip: sinBd }, async () => {
  const uid = await crear('insistente@cuenta.test');
  const otro = await crear('tranquilo@cuenta.test');
  const post = (sub: string) => app.inject({ method: 'POST', url: '/reportes-ia', headers: tok(sub), payload: { origen: 'chat', texto: 'x', motivo: 'otro' } });
  // Los de hace más de una hora no cuentan.
  await pool.query(`INSERT INTO reportes_ia (usuario_id, origen, motivo, texto, creado_en) SELECT $1, 'chat', 'otro', 'viejo', now() - interval '2 hours' FROM generate_series(1, 40)`, [uid]);
  for (let i = 0; i < REPORTES_POR_HORA; i++) assert.equal((await post(uid)).statusCode, 201, `reporte ${i + 1}`);
  const tope = await post(uid);
  assert.equal(tope.statusCode, 429);
  assert.equal(tope.json().error, 'demasiados_reportes');
  assert.equal((await post(otro)).statusCode, 201);
});

test('reportes IA en el panel: listado con alumno, filtro de pendientes y marcar revisado; solo admin', { skip: sinBd }, async () => {
  const uid = await crear('panel@cuenta.test');
  const r = await app.inject({ method: 'POST', url: '/reportes-ia', headers: tok(uid), payload: { origen: 'llamada', texto: 'Respuesta rara', motivo: 'inapropiado' } });
  const id = r.json().id;
  assert.equal((await app.inject({ url: '/admin/reportes-ia', headers: tok(uid) })).statusCode, 403);
  const admin = tok('admin', 'admin');
  const l = await app.inject({ url: '/admin/reportes-ia?estado=pendientes', headers: admin });
  assert.equal(l.statusCode, 200, l.body);
  const item = l.json().reportes.find((x: any) => x.id === id);
  assert.equal(item.email, 'panel@cuenta.test');
  assert.equal(item.motivo, 'inapropiado');
  assert.ok(l.json().pendientes >= 1);
  const marcar = await app.inject({ method: 'PUT', url: `/admin/reportes-ia/${id}`, headers: admin, payload: { revisado: true } });
  assert.deepEqual(marcar.json(), { id, revisado: true });
  const pend = await app.inject({ url: '/admin/reportes-ia?estado=pendientes', headers: admin });
  assert.ok(!pend.json().reportes.some((x: any) => x.id === id));
  assert.equal((await app.inject({ method: 'PUT', url: '/admin/reportes-ia/999999', headers: admin, payload: { revisado: true } })).statusCode, 404);
});
