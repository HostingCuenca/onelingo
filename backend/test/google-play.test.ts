/**
 * Suscripciones de Google Play Billing (lib/pagos/google.ts y rutas /pagos/google/*).
 * - Funciones puras: sin base de datos ni red.
 * - Rutas y SQL: contra una base TEMPORAL (`onelingo_test_google_<pid>`, se borra
 *   al terminar); sin Postgres local se omiten. Google (OAuth y la API Google Play
 *   Developer) se simula con `fetch`; la cuenta de servicio es una clave RSA
 *   generada aquí. Nunca se llama a Google de verdad.
 */
import { after, before, test } from 'node:test';
import assert from 'node:assert/strict';
import { createVerify, generateKeyPairSync } from 'node:crypto';
import pg from 'pg';
process.env.LOG_LEVEL = 'silent';
delete process.env.STRIPE_SECRET_KEY; delete process.env.STRIPE_WEBHOOK_SECRET;
const claves = generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIVADA = claves.privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const CORREO_SA = 'onelingo-pagos@proyecto-prueba.iam.gserviceaccount.com';
process.env.GOOGLE_PLAY_CUENTA_SERVICIO = JSON.stringify({ type: 'service_account', client_email: CORREO_SA, private_key: PRIVADA, token_uri: 'https://oauth2.googleapis.com/token' });
process.env.GOOGLE_PLAY_PAQUETE = 'com.torisoftt.onelingo';
process.env.GOOGLE_PLAY_RTDN_TOKEN = 'rtdn-secreto-de-prueba-123';
import { config } from '../src/lib/config.js';
config.jwtSecret = 'test-only-google-secret';
config.publicUrl = 'https://onelingo.test/api';

const urlBase = config.databaseUrl;
const NOMBRE_BD = `onelingo_test_google_${process.pid}`;
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
const G = await import('../src/lib/pagos/google.js');
const Sus = await import('../src/lib/pagos/suscripciones.js');
const { crearApp } = await import('../src/app.js');
const { migrar } = await import('../src/migrate.js');

// ── Google simulado ──────────────────────────────────────────────────────────
const gp = {
  compras: new Map<string, any>(), reconocidas: [] as string[], tokensOAuth: 0, llamadasApi: [] as string[],
  firmaValida: true,
};
const ACCESO = 'ya29.acceso-de-prueba';
const fetchOriginal = globalThis.fetch;
const json = (status: number, body: unknown) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
globalThis.fetch = (async (entrada: any, init: any = {}) => {
  const url = new URL(String(entrada));
  if (url.hostname === 'oauth2.googleapis.com') {
    const p = new URLSearchParams(String(init.body));
    const [cab, cuerpo, firma] = String(p.get('assertion')).split('.');
    gp.firmaValida = createVerify('RSA-SHA256').update(`${cab}.${cuerpo}`).verify(claves.publicKey, firma, 'base64url');
    const c = JSON.parse(Buffer.from(cuerpo, 'base64url').toString());
    if (!gp.firmaValida || c.iss !== CORREO_SA || c.scope !== 'https://www.googleapis.com/auth/androidpublisher') return json(400, { error: 'invalid_grant' });
    gp.tokensOAuth++;
    return json(200, { access_token: ACCESO, expires_in: 3599, token_type: 'Bearer' });
  }
  if (url.hostname !== 'androidpublisher.googleapis.com') return fetchOriginal(entrada, init);
  if (init.headers?.authorization !== `Bearer ${ACCESO}`) return json(401, { error: { message: 'Request is missing required authentication credential.' } });
  const ruta = decodeURIComponent(url.pathname).replace('/androidpublisher/v3/applications/com.torisoftt.onelingo', '');
  gp.llamadasApi.push(`${init.method ?? 'GET'} ${ruta}`);
  let m = /^\/purchases\/subscriptionsv2\/tokens\/(.+)$/.exec(ruta);
  if (m && (init.method ?? 'GET') === 'GET') {
    const c = gp.compras.get(m[1]);
    return c ? json(200, c) : json(404, { error: { message: 'The purchase token was not found.' } });
  }
  m = /^\/purchases\/subscriptions\/([^/]+)\/tokens\/(.+):acknowledge$/.exec(ruta);
  if (m && init.method === 'POST') {
    gp.reconocidas.push(m[2]);
    const c = gp.compras.get(m[2]); if (c) c.acknowledgementState = 'ACKNOWLEDGEMENT_STATE_ACKNOWLEDGED';
    return json(200, {});
  }
  return json(404, { error: { message: `ruta simulada desconocida: ${ruta}` } });
}) as typeof fetch;

const dias = (n: number) => new Date(Date.now() + n * 86_400_000).toISOString();
/** Compra (`SubscriptionPurchaseV2`) guardada en el Google simulado. */
function compra(token: string, o: { usuario?: string; producto?: string; planBase?: string; estado?: string; fin?: string; renueva?: boolean; precio?: [string, number]; anterior?: string; prueba?: boolean }) {
  const c: any = {
    kind: 'androidpublisher#subscriptionPurchaseV2', regionCode: 'US', latestOrderId: `GPA.0000-${token.slice(-4)}`,
    subscriptionState: o.estado ?? 'SUBSCRIPTION_STATE_ACTIVE', acknowledgementState: 'ACKNOWLEDGEMENT_STATE_PENDING',
    ...(o.usuario ? { externalAccountIdentifiers: { obfuscatedExternalAccountId: o.usuario } } : {}),
    ...(o.anterior ? { linkedPurchaseToken: o.anterior } : {}),
    ...(o.prueba !== false ? { testPurchase: {} } : {}),
    lineItems: [{
      productId: o.producto ?? 'plan_p1', expiryTime: o.fin ?? dias(30),
      autoRenewingPlan: { autoRenewEnabled: o.renueva ?? true, recurringPrice: { currencyCode: o.precio?.[0] ?? 'USD', units: String(Math.floor(o.precio?.[1] ?? 20)), nanos: Math.round(((o.precio?.[1] ?? 20) % 1) * 1e9) } },
      offerDetails: { basePlanId: o.planBase ?? 'mes-1' },
    }],
  };
  gp.compras.set(token, c);
  return c;
}
const notificacion = (token: string, tipo = 2) => ({
  message: { messageId: '1', data: Buffer.from(JSON.stringify({ version: '1.0', packageName: 'com.torisoftt.onelingo', eventTimeMillis: String(Date.now()), subscriptionNotification: { version: '1.0', notificationType: tipo, purchaseToken: token, subscriptionId: 'plan_p1' } })).toString('base64') },
  subscription: 'projects/x/subscriptions/onelingo-rtdn',
});

let app: Awaited<ReturnType<typeof crearApp>>;
let U1 = '', U2 = '', U3 = '';
const tok = (sub: string, rol: 'alumno' | 'admin' = 'alumno') => ({ authorization: `Bearer ${app.jwt.sign({ sub, rol })}` });
const TOKEN = (n: number) => `token-compra-${'x'.repeat(30)}.${n}`;

before(async () => {
  if (!hayBd) return;
  await migrar();
  app = await crearApp();
  const ins = (email: string) => pool.query("INSERT INTO usuarios (email, nombre, trial_segundos, idioma_meta) VALUES ($1, $2, 600, 'en') RETURNING id", [email, email.split('@')[0]]).then((r) => r.rows[0].id as string);
  U1 = await ins('ana@google.test'); U2 = await ins('beto@google.test'); U3 = await ins('carla@google.test');
});
after(async () => {
  globalThis.fetch = fetchOriginal;
  if (!hayBd) return;
  await app?.close();
  await pool.end();
  const c = new pg.Client({ connectionString: urlBase }); await c.connect();
  await c.query(`DROP DATABASE IF EXISTS ${NOMBRE_BD} WITH (FORCE)`); await c.end();
});

// ── Puras ────────────────────────────────────────────────────────────────────
test('ids de Play Console: producto por plan y plan base por duración', () => {
  assert.equal(G.productoDePlan('p1'), 'plan_p1');
  assert.equal(G.productoDePlan('Familiar'), 'plan_familiar');
  assert.equal(G.productoDePlan('plan-x'), 'plan_plan_x');
  assert.equal(G.planBaseDeMeses(3), 'mes-3');
  assert.equal(G.mesesDePlanBase('mes-12'), 12);
  assert.equal(G.mesesDePlanBase('anual'), null);
  assert.equal(G.mesesDePlanBase('mes-0'), null);
});

test('estado de Google: gracia da acceso, en espera es impago, pausada y vencida no', () => {
  assert.equal(G.estadoDesdeGoogle('SUBSCRIPTION_STATE_ACTIVE'), 'activa');
  assert.equal(G.estadoDesdeGoogle('SUBSCRIPTION_STATE_IN_GRACE_PERIOD'), 'activa');
  assert.equal(G.estadoDesdeGoogle('SUBSCRIPTION_STATE_CANCELED'), 'cancelada');
  assert.equal(G.estadoDesdeGoogle('SUBSCRIPTION_STATE_ON_HOLD'), 'impago');
  assert.equal(G.estadoDesdeGoogle('SUBSCRIPTION_STATE_PENDING'), 'impago');
  assert.equal(G.estadoDesdeGoogle('SUBSCRIPTION_STATE_PAUSED'), 'vencida');
  assert.equal(G.estadoDesdeGoogle('SUBSCRIPTION_STATE_EXPIRED'), 'vencida');
});

test('datos de una compra: precio, meses, inicio del periodo, renovación apagada y modo', () => {
  const fin = '2026-12-15T10:00:00.000Z';
  const d = G.datosDeGoogle(compra('t-puro', { usuario: 'u-1', producto: 'plan_p2', planBase: 'mes-3', fin, renueva: false, precio: ['USD', 84.99] }));
  assert.equal(d.estado, 'activa');
  assert.equal(d.cancela_al_final, true);
  assert.equal(d.importe_centavos, 8499);
  assert.equal(d.moneda, 'usd');
  assert.equal(d.meses, 3);
  assert.equal(d.intervalo, 'mes');
  assert.equal(d.periodo_fin?.toISOString(), fin);
  assert.equal(d.periodo_inicio?.toISOString(), '2026-09-15T10:00:00.000Z');
  assert.equal(d.modo, 'test');
  assert.equal(d.usuarioPista, 'u-1');
  assert.equal(d.reconocida, false);
  assert.equal(G.datosDeGoogle(compra('t-puro2', { planBase: 'mes-12', prueba: false })).intervalo, 'anio');
  assert.equal(G.datosDeGoogle(compra('t-puro3', { prueba: false })).modo, 'live');
});

test('RTDN: token de la suscripción; prueba, otro paquete y basura se ignoran', () => {
  assert.deepEqual(G.tokenDeRtdn(notificacion('abc'), 'com.torisoftt.onelingo'), { token: 'abc' });
  assert.equal(G.tokenDeRtdn(notificacion('abc'), 'com.otra.app').motivo, 'otro paquete');
  const prueba = { message: { data: Buffer.from(JSON.stringify({ packageName: 'com.torisoftt.onelingo', testNotification: { version: '1.0' } })).toString('base64') } };
  assert.equal(G.tokenDeRtdn(prueba, 'com.torisoftt.onelingo').motivo, 'notificación de prueba');
  const anulada = { message: { data: Buffer.from(JSON.stringify({ packageName: 'com.torisoftt.onelingo', voidedPurchaseNotification: { purchaseToken: 'vvv', productType: 1 } })).toString('base64') } };
  assert.deepEqual(G.tokenDeRtdn(anulada, 'com.torisoftt.onelingo'), { token: 'vvv' });
  assert.equal(G.tokenDeRtdn({ message: { data: '%%%' } }, 'com.torisoftt.onelingo').token, null);
  assert.equal(G.tokenDeRtdn({}, 'com.torisoftt.onelingo').motivo, 'sin message.data');
});

test('acceso de Google: activa con margen de un día tras el fin; cancelada hasta el fin', () => {
  const ahora = new Date('2026-11-01T00:00:00Z');
  const f = (estado: any, fin: string | null) => ({ origen: 'google' as const, estado, periodo_fin: fin });
  assert.equal(Sus.tieneAcceso(f('activa', '2026-11-10T00:00:00Z'), ahora), true);
  assert.equal(Sus.tieneAcceso(f('activa', '2026-10-31T12:00:00Z'), ahora), true, 'renovación aún no avisada');
  assert.equal(Sus.tieneAcceso(f('activa', '2026-10-29T00:00:00Z'), ahora), false);
  assert.equal(Sus.tieneAcceso(f('cancelada', '2026-11-05T00:00:00Z'), ahora), true);
  assert.equal(Sus.tieneAcceso(f('cancelada', '2026-10-31T00:00:00Z'), ahora), false);
  assert.equal(Sus.tieneAcceso(f('impago', '2026-11-10T00:00:00Z'), ahora), false);
  assert.equal(Sus.estadoEfectivo({ ...f('activa', '2026-10-20T00:00:00Z'), usuario_id: 'x' } as any, ahora), 'vencida');
  assert.deepEqual(Sus.calcularMrr([{ origen: 'google', estado: 'activa', importe_centavos: 5500, moneda: 'usd', meses: 3 }]), { mrr: 18.33, otrasMonedas: 0 });
});

// ── Rutas ────────────────────────────────────────────────────────────────────
test('GET /planes: Google Play disponible, producto y planes base por plan', { skip: sinBd }, async () => {
  const d = (await app.inject({ url: '/planes' })).json();
  assert.deepEqual(d.google, { disponible: true, paquete: 'com.torisoftt.onelingo' });
  const p2 = d.planes.find((p: any) => p.id === 'p2');
  assert.deepEqual(p2.google, { producto: 'plan_p2', planesBase: ['mes-1', 'mes-3', 'mes-6', 'mes-12'] });
});

test('verificar: guarda la compra con sus idiomas, la reconoce y da acceso; el JWT va firmado', { skip: sinBd }, async () => {
  compra(TOKEN(1), { usuario: U1, producto: 'plan_p2', planBase: 'mes-3', precio: ['USD', 85] });
  const sinSesion = await app.inject({ method: 'POST', url: '/pagos/google/verificar', payload: { token: TOKEN(1) } });
  assert.equal(sinSesion.statusCode, 401);
  const r = await app.inject({ method: 'POST', url: '/pagos/google/verificar', headers: tok(U1), payload: { token: TOKEN(1), idiomas: ['EN', 'fr'] } });
  assert.equal(r.statusCode, 200, r.body);
  const s = r.json();
  assert.equal(s.planId, 'p2'); assert.equal(s.origen, 'google'); assert.equal(s.estado, 'activa');
  assert.equal(s.meses, 3); assert.deepEqual(s.idiomas, ['en', 'fr']); assert.equal(s.accesoPorIdioma.fr, true); assert.equal(s.accesoPorIdioma.de, false);
  assert.deepEqual(s.google, { producto: 'plan_p2', planBase: 'mes-3' });
  assert.equal(s.puedeGestionar, false);
  assert.equal(gp.firmaValida, true);
  assert.deepEqual(gp.reconocidas, [TOKEN(1)]);
  const fila = (await pool.query('SELECT importe_centavos, moneda, modo, google_pedido, periodo_inicio FROM suscripciones WHERE usuario_id = $1', [U1])).rows[0];
  assert.equal(fila.importe_centavos, 8500); assert.equal(fila.moneda, 'usd'); assert.equal(fila.modo, 'test');
  assert.match(fila.google_pedido, /^GPA\./); assert.ok(fila.periodo_inicio);
  assert.equal((await pool.query('SELECT plan_id FROM usuarios WHERE id = $1', [U1])).rows[0].plan_id, 'p2');
  // Verificarla otra vez (la app reintenta): mismos idiomas aunque no los mande, sin reconocerla de nuevo.
  const otra = await app.inject({ method: 'POST', url: '/pagos/google/verificar', headers: tok(U1), payload: { token: TOKEN(1) } });
  assert.deepEqual(otra.json().idiomas, ['en', 'fr']);
  assert.equal(gp.reconocidas.length, 1);
  assert.equal(gp.tokensOAuth, 1, 'el token de acceso se reutiliza');
});

test('verificar: compra de otra cuenta 403, token desconocido 404, token con caracteres raros 400', { skip: sinBd }, async () => {
  compra(TOKEN(2), { usuario: U1, producto: 'plan_p1' });
  const ajena = await app.inject({ method: 'POST', url: '/pagos/google/verificar', headers: tok(U2), payload: { token: TOKEN(2) } });
  assert.equal(ajena.statusCode, 403);
  assert.match(ajena.json().error, /otra cuenta/);
  const nada = await app.inject({ method: 'POST', url: '/pagos/google/verificar', headers: tok(U2), payload: { token: TOKEN(99) } });
  assert.equal(nada.statusCode, 404);
  const raro = await app.inject({ method: 'POST', url: '/pagos/google/verificar', headers: tok(U2), payload: { token: 'abc/../../x?y=1' } });
  assert.equal(raro.statusCode, 400);
});

test('RTDN: sin token 403; cancelación mantiene el acceso hasta el fin; vencida lo quita', { skip: sinBd }, async () => {
  const sinToken = await app.inject({ method: 'POST', url: '/pagos/google/rtdn', payload: notificacion(TOKEN(1)) });
  assert.equal(sinToken.statusCode, 403);
  const malo = await app.inject({ method: 'POST', url: '/pagos/google/rtdn?token=otro', payload: notificacion(TOKEN(1)) });
  assert.equal(malo.statusCode, 403);
  const url = `/pagos/google/rtdn?token=${process.env.GOOGLE_PLAY_RTDN_TOKEN}`;
  // El alumno cancela en Play: sigue con acceso hasta el fin del periodo pagado.
  Object.assign(gp.compras.get(TOKEN(1)), { subscriptionState: 'SUBSCRIPTION_STATE_CANCELED' });
  gp.compras.get(TOKEN(1)).lineItems[0].autoRenewingPlan.autoRenewEnabled = false;
  const r = await app.inject({ method: 'POST', url, payload: notificacion(TOKEN(1), 3) });
  assert.equal(r.statusCode, 200, r.body);
  assert.equal(r.json().estado, 'cancelada');
  let s = (await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(U1) })).json();
  assert.equal(s.estado, 'cancelada'); assert.equal(s.accesoPlan, true); assert.deepEqual(s.idiomas, ['en', 'fr']);
  // Vence: sin acceso.
  Object.assign(gp.compras.get(TOKEN(1)), { subscriptionState: 'SUBSCRIPTION_STATE_EXPIRED' });
  gp.compras.get(TOKEN(1)).lineItems[0].expiryTime = dias(-1);
  await app.inject({ method: 'POST', url, payload: notificacion(TOKEN(1), 13) });
  s = (await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(U1) })).json();
  assert.equal(s.estado, 'vencida'); assert.equal(s.accesoPlan, false); assert.equal(s.planId, '');
  // Prueba de Play Console y compra desconocida: 200 sin hacer nada (Pub/Sub no reintenta).
  const prueba = { message: { data: Buffer.from(JSON.stringify({ packageName: 'com.torisoftt.onelingo', testNotification: {} })).toString('base64') } };
  assert.equal((await app.inject({ method: 'POST', url, payload: prueba })).json().ignorado, 'notificación de prueba');
  assert.equal((await app.inject({ method: 'POST', url, payload: notificacion(TOKEN(77)) })).json().ignorado, 'compra desconocida');
});

test('cambio de plan en Play: el token nuevo enlaza al anterior y reemplaza la fila; el aviso viejo no la pisa', { skip: sinBd }, async () => {
  compra(TOKEN(3), { usuario: U3, producto: 'plan_p1' });
  await app.inject({ method: 'POST', url: '/pagos/google/verificar', headers: tok(U3), payload: { token: TOKEN(3), idiomas: ['de'] } });
  compra(TOKEN(4), { usuario: U3, producto: 'plan_p3', planBase: 'mes-12', anterior: TOKEN(3) });
  Object.assign(gp.compras.get(TOKEN(3)), { subscriptionState: 'SUBSCRIPTION_STATE_EXPIRED' });
  const url = `/pagos/google/rtdn?token=${process.env.GOOGLE_PLAY_RTDN_TOKEN}`;
  await app.inject({ method: 'POST', url, payload: notificacion(TOKEN(4), 4) });
  let s = (await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(U3) })).json();
  assert.equal(s.planId, 'p3'); assert.equal(s.meses, 12); assert.deepEqual(s.idiomas, ['de'], 'conserva los idiomas; los otros 2 quedan por elegir');
  assert.equal(s.idiomasPorElegir, 2);
  // Llega tarde el aviso de que la compra anterior venció: no toca la nueva.
  const viejo = await app.inject({ method: 'POST', url, payload: notificacion(TOKEN(3), 13) });
  assert.equal(viejo.json().aplicada, false);
  s = (await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(U3) })).json();
  assert.equal(s.planId, 'p3'); assert.equal(s.estado, 'activa');
});

test('refresco sin RTDN: periodo vencido se vuelve a consultar y toma la renovación', { skip: sinBd }, async () => {
  await pool.query("UPDATE suscripciones SET periodo_fin = now() - interval '2 hours', actualizado_en = now() - interval '1 hour' WHERE usuario_id = $1", [U3]);
  gp.compras.get(TOKEN(4)).lineItems[0].expiryTime = dias(365);
  const antes = gp.llamadasApi.length;
  const s = (await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(U3) })).json();
  assert.equal(gp.llamadasApi.length > antes, true);
  assert.ok(new Date(s.periodoFin).getTime() > Date.now() + 300 * 86_400_000);
  // Recién consultada: no se vuelve a pedir.
  const despues = gp.llamadasApi.length;
  await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(U3) });
  assert.equal(gp.llamadasApi.length, despues);
});

test('Familiar comprado en Play: los miembros tienen acceso; no se puede dar cortesía encima', { skip: sinBd }, async () => {
  compra(TOKEN(5), { usuario: U2, producto: 'plan_familiar', planBase: 'mes-1', precio: ['USD', 60] });
  const r = await app.inject({ method: 'POST', url: '/pagos/google/verificar', headers: tok(U2), payload: { token: TOKEN(5), idiomas: ['it'] } });
  assert.equal(r.statusCode, 200, r.body);
  assert.equal(r.json().usuariosPlan, 4);
  const inv = await app.inject({ method: 'POST', url: '/usuarios/me/familia', headers: tok(U2), payload: { email: 'ana@google.test' } });
  assert.equal(inv.statusCode, 200, inv.body);
  const ana = (await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(U1) })).json();
  assert.equal(ana.familiar, true); assert.equal(ana.planId, 'familiar'); assert.equal(ana.accesoPlan, true);
  const cort = await app.inject({ method: 'POST', url: `/admin/usuarios/${U2}/cortesia`, headers: tok(U2, 'admin'), payload: { planId: 'p1' } });
  assert.equal(cort.statusCode, 409);
  assert.match(cort.json().error, /Google Play/);
  const panel = (await app.inject({ url: '/admin/suscripciones?estado=google', headers: tok(U2, 'admin') })).json();
  assert.deepEqual(panel.filas.map((f: any) => f.email).sort(), ['beto@google.test', 'carla@google.test'], 'filtro «google»: solo compras de Play');
  assert.equal(panel.resumen.google, 2, 'beto (familiar) y carla (p3)');
});

test('sin cuenta de servicio: GET /planes la marca no disponible y verificar responde 503', { skip: sinBd }, async () => {
  const antes = process.env.GOOGLE_PLAY_CUENTA_SERVICIO;
  process.env.GOOGLE_PLAY_CUENTA_SERVICIO = '';
  try {
    assert.equal((await app.inject({ url: '/planes' })).json().google.disponible, false);
    const r = await app.inject({ method: 'POST', url: '/pagos/google/verificar', headers: tok(U1), payload: { token: TOKEN(1) } });
    assert.equal(r.statusCode, 503);
  } finally { process.env.GOOGLE_PLAY_CUENTA_SERVICIO = antes; }
});
