/**
 * Planes y suscripciones con Stripe (fase 1, modo test).
 * - Funciones puras: sin base de datos ni red.
 * - Rutas y SQL: contra una base TEMPORAL creada en el Postgres local
 *   (`onelingo_test_pagos_<pid>`, se borra al terminar). Si no hay Postgres
 *   local, esas pruebas se omiten. Stripe se simula con `fetch`; nunca se
 *   llama a Stripe de verdad. Las claves son inventadas.
 */
import { after, before, test } from 'node:test';
import assert from 'node:assert/strict';
import pg from 'pg';
process.env.LOG_LEVEL = 'silent';
delete process.env.STRIPE_SECRET_KEY; delete process.env.STRIPE_WEBHOOK_SECRET;
import { config } from '../src/lib/config.js';

const rnd = (n: number, abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', s = 7) => Array.from({ length: n }, (_, i) => abc[(i * s + 3) % abc.length]).join('');
const FALSA = {
  sk: 'sk_test_' + rnd(60), rk: 'rk_test_' + rnd(60, undefined, 11), skLive: 'sk_live_' + rnd(60, undefined, 13), pk: 'pk_test_' + rnd(60),
  openai: 'sk-proj-' + rnd(40), eleven: 'sk_' + rnd(48, '0123456789abcdef'), whsec: 'whsec_' + rnd(32), invalida: 'sk_test_' + rnd(60, undefined, 17),
};
config.jwtSecret = 'test-only-pagos-secret';
config.publicUrl = 'https://onelingo.test/api';

// ── Base temporal ────────────────────────────────────────────────────────────
const urlBase = config.databaseUrl;
const NOMBRE_BD = `onelingo_test_pagos_${process.pid}`;
let hayBd = false;
try {
  const c = new pg.Client({ connectionString: urlBase, connectionTimeoutMillis: 2000 });
  await c.connect();
  await c.query(`CREATE DATABASE ${NOMBRE_BD}`);
  await c.end();
  const u = new URL(urlBase); u.pathname = '/' + NOMBRE_BD;
  config.databaseUrl = u.toString();
  hayBd = true;
} catch { /* sin Postgres local: se omiten las pruebas con base */ }
const sinBd = hayBd ? false : 'sin Postgres local';

const { pool } = await import('../src/lib/db.js');
const C = await import('../src/lib/conexiones.js');
const S = await import('../src/lib/pagos/stripe.js');
const Sus = await import('../src/lib/pagos/suscripciones.js');
const { crearApp } = await import('../src/app.js');
const { migrar } = await import('../src/migrate.js');

// ── Stripe simulado ──────────────────────────────────────────────────────────
type Llamada = { metodo: string; ruta: string; datos: URLSearchParams; auth: string };
const st = {
  llamadas: [] as Llamada[], n: 0,
  webhooks: [] as any[], portal: [] as any[], productos: new Map<string, any>(), precios: new Map<string, any>(),
  subs: new Map<string, any>(), sesiones: new Map<string, any>(), transacciones: [] as any[],
};
const id = (p: string) => `${p}_${++st.n}`;
const fetchOriginal = globalThis.fetch;
const json = (status: number, body: unknown) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
globalThis.fetch = (async (entrada: any, init: any = {}) => {
  const url = new URL(String(entrada));
  if (url.hostname !== 'api.stripe.com') return fetchOriginal(entrada, init);
  const metodo = init.method ?? 'GET';
  const datos = new URLSearchParams(metodo === 'POST' ? String(init.body ?? '') : url.search);
  const auth = String(init.headers?.authorization ?? '');
  const ruta = url.pathname.replace(/^\/v1/, '');
  st.llamadas.push({ metodo, ruta, datos, auth });
  if (auth === `Bearer ${FALSA.invalida}`) return json(401, { error: { message: 'Invalid API Key provided: sk_test_*********************abcd', type: 'invalid_request_error' } });
  const m = (re: RegExp) => re.exec(`${metodo} ${ruta}`);
  let r: RegExpExecArray | null;
  if (m(/^GET \/account$/)) return json(200, { id: 'acct_prueba', settings: { dashboard: { display_name: 'OneLingo pruebas' } }, charges_enabled: true });
  if (m(/^GET \/balance$/)) return json(200, { object: 'balance', livemode: false });
  if (m(/^GET \/webhook_endpoints$/)) return json(200, { data: st.webhooks });
  if (m(/^POST \/webhook_endpoints$/)) { const w = { id: id('we'), url: datos.get('url'), secret: FALSA.whsec }; st.webhooks.push(w); return json(200, w); }
  if ((r = m(/^POST \/webhook_endpoints\/(\w+)$/))) return json(200, st.webhooks.find((w) => w.id === r![1]));
  if ((r = m(/^DELETE \/webhook_endpoints\/(\w+)$/))) { st.webhooks = st.webhooks.filter((w) => w.id !== r![1]); return json(200, { deleted: true }); }
  if (m(/^GET \/billing_portal\/configurations$/)) return json(200, { data: st.portal });
  if (m(/^POST \/billing_portal\/configurations$/)) { const p = { id: id('bpc'), active: true, metadata: { origen: datos.get('metadata[origen]') }, datos }; st.portal.push(p); return json(200, p); }
  if ((r = m(/^POST \/billing_portal\/configurations\/(\w+)$/))) { const p = st.portal.find((c) => c.id === r![1]); if (!p) return json(404, { error: { message: 'No such configuration' } }); p.datos = datos; return json(200, p); }
  if (m(/^POST \/billing_portal\/sessions$/)) return json(200, { url: `https://billing.stripe.com/p/session/${id('bps')}` });
  if (m(/^POST \/products$/)) { const p = { id: id('prod'), name: datos.get('name'), metadata: { plan_id: datos.get('metadata[plan_id]') } }; st.productos.set(p.id, p); return json(200, p); }
  if ((r = m(/^POST \/products\/(\w+)$/))) return json(200, st.productos.get(r[1]));
  if (m(/^POST \/prices$/)) {
    const p = { id: id('price'), product: datos.get('product'), unit_amount: Number(datos.get('unit_amount')), currency: datos.get('currency'),
      recurring: { interval: datos.get('recurring[interval]'), interval_count: Number(datos.get('recurring[interval_count]') ?? 1) }, metadata: { plan_id: datos.get('metadata[plan_id]') }, active: true };
    st.precios.set(p.id, p); return json(200, p);
  }
  if ((r = m(/^POST \/prices\/(\w+)$/))) { const p = st.precios.get(r[1]); if (datos.get('active') === 'false') p.active = false; return json(200, p); }
  if (m(/^POST \/checkout\/sessions$/)) { const s: any = { id: id('cs_test'), url: '', status: 'open', client_reference_id: datos.get('client_reference_id'), subscription: null, metadata: {} }; s.url = `https://checkout.stripe.com/c/pay/${s.id}`; st.sesiones.set(s.id, s); return json(200, s); }
  if ((r = m(/^GET \/checkout\/sessions\/(\w+)$/))) { const s = st.sesiones.get(r[1]); return s ? json(200, { ...s, subscription: s.subscription ? st.subs.get(s.subscription) : null }) : json(404, { error: { message: 'No such checkout.session' } }); }
  if ((r = m(/^GET \/subscriptions\/(\w+)$/))) { const s = st.subs.get(r[1]); return s ? json(200, s) : json(404, { error: { message: 'No such subscription' } }); }
  if (m(/^GET \/balance_transactions$/)) return json(200, { data: st.transacciones, has_more: false });
  return json(404, { error: { message: `ruta simulada desconocida: ${metodo} ${ruta}` } });
}) as typeof fetch;
const llamadasA = (re: RegExp) => st.llamadas.filter((l) => re.test(`${l.metodo} ${l.ruta}`));

/** Suscripción de Stripe con la forma de la API actual (periodo en el item). */
function suscripcionStripe(o: { usuarioId?: string; precio: any; status?: string; cancelAlFinal?: boolean; fin?: number; inicio?: number; cliente?: string; endedAt?: number; idiomas?: string }) {
  const s = {
    id: id('sub'), object: 'subscription', status: o.status ?? 'active', customer: o.cliente ?? id('cus'), livemode: false,
    cancel_at_period_end: !!o.cancelAlFinal, cancel_at: null, canceled_at: o.endedAt ?? null, ended_at: o.endedAt ?? null,
    metadata: o.usuarioId ? { usuario_id: o.usuarioId, plan_id: o.precio.metadata?.plan_id, ...(o.idiomas !== undefined ? { idiomas: o.idiomas } : {}) } : {},
    items: { data: [{ price: o.precio, current_period_start: o.inicio ?? Math.floor(Date.now() / 1000) - 86400, current_period_end: o.fin ?? Math.floor(Date.now() / 1000) + 30 * 86400 }] },
  };
  st.subs.set(s.id, s);
  return s;
}

// ── Puras ────────────────────────────────────────────────────────────────────
test('clave de Stripe: sk_test y rk_test válidas; pk rechazada; OpenAI rechazada; sin confundir con ElevenLabs', () => {
  for (const k of [FALSA.sk, FALSA.rk, FALSA.skLive]) assert.equal(C.validarFormato('stripe', 'secretKey', ` ${k}\n`).ok, true);
  assert.equal(C.detectarProveedor(FALSA.sk), 'stripe');
  assert.equal(C.detectarProveedor(FALSA.eleven), 'elevenlabs');
  const pk = C.validarFormato('stripe', 'secretKey', FALSA.pk);
  assert.equal(pk.ok, false);
  assert.equal((pk as any).mensaje, 'Esta es la clave publicable; pega la secreta (sk_…)');
  const oai = C.validarFormato('stripe', 'secretKey', FALSA.openai);
  assert.equal(oai.ok, false);
  assert.match((oai as any).mensaje, /^Esta clave es de OpenAI, no de Stripe\./);
  assert.match((C.validarFormato('stripe', 'secretKey', FALSA.whsec) as any).mensaje, /secreto de webhook/);
  assert.match((C.validarFormato('elevenlabs', 'apiKey', FALSA.sk) as any).mensaje, /es de Stripe, no de ElevenLabs/);
  assert.equal(S.modoDeClave(FALSA.rk), 'test'); assert.equal(S.modoDeClave(FALSA.skLive), 'live');
  assert.equal(C.enmascarar(FALSA.sk), 'sk_test_…' + FALSA.sk.slice(-4));
  assert.equal(C.enmascarar(FALSA.rk), 'rk_test_…' + FALSA.rk.slice(-4));
});

test('codificación form anidada', () => {
  assert.equal(S.codificarForm({
    mode: 'subscription', line_items: [{ price: 'price_1', quantity: 1 }], subscription_data: { metadata: { plan_id: 'p1' } },
    enabled_events: ['a.b', 'c'], activo: false, nada: undefined, nulo: null, vacio: '', url: 'https://x.test/#/pago?estado=ok&session_id={CHECKOUT_SESSION_ID}',
  }), 'mode=subscription&line_items%5B0%5D%5Bprice%5D=price_1&line_items%5B0%5D%5Bquantity%5D=1&subscription_data%5Bmetadata%5D%5Bplan_id%5D=p1'
    + '&enabled_events%5B0%5D=a.b&enabled_events%5B1%5D=c&activo=false&vacio=&url=https%3A%2F%2Fx.test%2F%23%2Fpago%3Festado%3Dok%26session_id%3D%7BCHECKOUT_SESSION_ID%7D');
  const p = new URLSearchParams(S.codificarForm({ created: { gte: 1700000000 }, expand: ['subscription'] }));
  assert.equal(p.get('created[gte]'), '1700000000'); assert.equal(p.get('expand[0]'), 'subscription');
});

test('firma del webhook: válida, inválida, caducada, sin cabecera y varias v1', () => {
  const cuerpo = Buffer.from('{"id":"evt_1","type":"invoice.paid"}');
  const ahora = 1_800_000_000;
  const cab = S.firmarEvento(cuerpo, FALSA.whsec, ahora);
  assert.deepEqual(S.verificarFirma(cuerpo, cab, FALSA.whsec, ahora + 10), { ok: true, t: ahora });
  assert.equal(S.verificarFirma(cuerpo.toString('utf8'), cab, FALSA.whsec, ahora).ok, true);
  assert.deepEqual(S.verificarFirma(cuerpo, cab, 'whsec_otro', ahora), { ok: false, motivo: 'firma' });
  assert.deepEqual(S.verificarFirma(Buffer.from('{"id":"evt_2"}'), cab, FALSA.whsec, ahora), { ok: false, motivo: 'firma' });
  assert.deepEqual(S.verificarFirma(cuerpo, cab, FALSA.whsec, ahora + 301), { ok: false, motivo: 'caducada' });
  assert.deepEqual(S.verificarFirma(cuerpo, undefined, FALSA.whsec, ahora), { ok: false, motivo: 'sin_cabecera' });
  assert.deepEqual(S.verificarFirma(cuerpo, 'v1=abc', FALSA.whsec, ahora), { ok: false, motivo: 'formato' });
  // Durante la rotación del secreto Stripe manda varias v1: basta una válida.
  assert.equal(S.verificarFirma(cuerpo, `t=${ahora},v1=${'0'.repeat(64)},${cab.split(',')[1]}`, FALSA.whsec, ahora).ok, true);
});

test('acceso: activa, prueba, impago, cancelada con y sin periodo, cortesía con y sin fecha', () => {
  const ahora = new Date('2026-10-20T12:00:00Z'), futuro = '2026-11-20T00:00:00Z', pasado = '2026-10-01T00:00:00Z';
  const f = (origen: any, estado: any, periodo_fin: string | null) => ({ origen, estado, periodo_fin });
  assert.equal(Sus.tieneAcceso(f('stripe', 'activa', pasado), ahora), true);
  assert.equal(Sus.tieneAcceso(f('stripe', 'prueba_stripe', null), ahora), true);
  assert.equal(Sus.tieneAcceso(f('stripe', 'impago', futuro), ahora), false);
  assert.equal(Sus.tieneAcceso(f('stripe', 'vencida', futuro), ahora), false);
  assert.equal(Sus.tieneAcceso(f('stripe', 'cancelada', futuro), ahora), true);
  assert.equal(Sus.tieneAcceso(f('stripe', 'cancelada', pasado), ahora), false);
  assert.equal(Sus.tieneAcceso(f('stripe', 'cancelada', null), ahora), false);
  assert.equal(Sus.tieneAcceso(f('cortesia', 'activa', null), ahora), true);
  assert.equal(Sus.tieneAcceso(f('cortesia', 'activa', futuro), ahora), true);
  assert.equal(Sus.tieneAcceso(f('cortesia', 'activa', pasado), ahora), false);
  assert.equal(Sus.tieneAcceso(null, ahora), false);
  assert.equal(Sus.estadoEfectivo({ ...f('cortesia', 'activa', pasado) } as any, ahora), 'vencida');
  assert.equal(Sus.estadoEfectivo(null, ahora), 'sin_plan');
  assert.deepEqual(['active', 'trialing', 'past_due', 'unpaid', 'incomplete', 'canceled', 'incomplete_expired', 'paused'].map(Sus.estadoDesdeStripe),
    ['activa', 'prueba_stripe', 'impago', 'impago', 'impago', 'cancelada', 'vencida', 'vencida']);
  // Un evento tardío de otra suscripción sin acceso no pisa una cortesía vigente.
  assert.equal(Sus.debeAplicar({ origen: 'cortesia', estado: 'activa', periodo_fin: null, stripe_suscripcion_id: null } as any, { stripe_suscripcion_id: 'sub_x', estado: 'cancelada', periodo_fin: null }, ahora), false);
  assert.equal(Sus.debeAplicar({ origen: 'cortesia', estado: 'activa', periodo_fin: null, stripe_suscripcion_id: null } as any, { stripe_suscripcion_id: 'sub_x', estado: 'activa', periodo_fin: null }, ahora), true);
});

test('MRR: mensuales y anuales (/12), solo activas de Stripe en USD; usa el importe real del suscriptor', () => {
  const r = Sus.calcularMrr([
    { origen: 'stripe', estado: 'activa', importe_centavos: 2000, intervalo: 'mes', moneda: 'usd' },
    { origen: 'stripe', estado: 'activa', importe_centavos: 24000, intervalo: 'anio', moneda: 'usd' }, // 20/mes
    { origen: 'stripe', estado: 'activa', importe_centavos: null, intervalo: null, moneda: null, plan_precio_centavos: 3000, plan_intervalo: 'mes', plan_moneda: 'usd' },
    { origen: 'stripe', estado: 'activa', importe_centavos: 9999, intervalo: 'anio', moneda: 'eur' },
    { origen: 'stripe', estado: 'prueba_stripe', importe_centavos: 4000, intervalo: 'mes', moneda: 'usd' },
    { origen: 'stripe', estado: 'impago', importe_centavos: 4000, intervalo: 'mes', moneda: 'usd' },
    { origen: 'cortesia', estado: 'activa', importe_centavos: null },
  ] as any);
  assert.deepEqual(r, { mrr: 70, otrasMonedas: 1 });
  assert.deepEqual(Sus.calcularMrr([{ origen: 'stripe', estado: 'activa', importe_centavos: 1000, intervalo: 'anio', moneda: 'usd' }] as any), { mrr: 0.83, otrasMonedas: 0 });
});

test('datos de Stripe: periodo en la suscripción (API antigua) o en el item (API nueva) y cancelación al momento', () => {
  const precio = { id: 'price_x', unit_amount: 2000, currency: 'usd', recurring: { interval: 'year' }, metadata: { plan_id: 'p1' }, product: 'prod_x' };
  const vieja = Sus.datosDeStripe({ id: 'sub_v', status: 'active', customer: 'cus_1', current_period_end: 1_900_000_000, items: { data: [{ price: precio }] } });
  assert.equal(vieja.periodo_fin?.getTime(), 1_900_000_000_000);
  assert.equal(vieja.intervalo, 'anio'); assert.equal(vieja.precioPlan, 'p1'); assert.equal(vieja.suscripcionPlan, null); assert.equal(vieja.productoId, 'prod_x');
  const cancelada = Sus.datosDeStripe({ id: 'sub_c', status: 'canceled', customer: { id: 'cus_2' }, ended_at: 1_700_000_000, items: { data: [{ price: precio, current_period_end: 1_900_000_000 }] } });
  assert.equal(cancelada.periodo_fin?.getTime(), 1_700_000_000_000);
  assert.equal(cancelada.stripe_cliente_id, 'cus_2'); assert.equal(cancelada.cancela_al_final, false);
});

test('Customer Portal: parámetros de cambio de plan (price, create_prorations, products) y sin planes desactivado', () => {
  const f = new URLSearchParams(S.codificarForm(S.cuerpoPortal('https://app.test/#/pago?estado=portal', [
    { producto: 'prod_a', precio: 'price_a' }, { producto: 'prod_b', precio: 'price_b' },
  ])));
  assert.equal(f.get('features[subscription_update][enabled]'), 'true');
  assert.equal(f.get('features[subscription_update][default_allowed_updates][0]'), 'price');
  assert.equal(f.get('features[subscription_update][default_allowed_updates][1]'), null);
  assert.equal(f.get('features[subscription_update][proration_behavior]'), 'create_prorations');
  assert.deepEqual([f.get('features[subscription_update][products][0][product]'), f.get('features[subscription_update][products][0][prices][0]')], ['prod_a', 'price_a']);
  assert.deepEqual([f.get('features[subscription_update][products][1][product]'), f.get('features[subscription_update][products][1][prices][0]')], ['prod_b', 'price_b']);
  assert.equal(f.get('features[subscription_cancel][mode]'), 'at_period_end');
  assert.equal(f.get('default_return_url'), 'https://app.test/#/pago?estado=portal');
  assert.equal(f.get('metadata[origen]'), 'onelingo');
  const vacio = new URLSearchParams(S.codificarForm(S.cuerpoPortal('https://app.test', [])));
  assert.equal(vacio.get('features[subscription_update][enabled]'), 'false');
  assert.ok(![...vacio.keys()].some((k) => k.includes('[products]') || k.includes('default_allowed_updates')));
  const once = new URLSearchParams(S.codificarForm(S.cuerpoPortal('https://app.test', Array.from({ length: 11 }, (_, i) => ({ producto: `prod_${i}`, precio: `price_${i}` })))));
  assert.equal(once.get('features[subscription_update][products][9][product]'), 'prod_9');
  assert.equal(once.get('features[subscription_update][products][10][product]'), null, 'Stripe admite 10');
});

test('idiomas: validación, acceso por idioma, qué es un cambio y regla cambioIdiomas', () => {
  assert.equal(Sus.errorIdiomas(['en', 'fr'], 2, { exactos: true }), null);
  assert.match(Sus.errorIdiomas(['en'], 2, { exactos: true })!, /elige exactamente 2/);
  assert.match(Sus.errorIdiomas(['en', 'en'], 2)!, /repetido/);
  assert.match(Sus.errorIdiomas(['xx'], 2)!, /no válido/);
  assert.equal(Sus.errorIdiomas([], 0, { exactos: true }), null);
  assert.match(Sus.errorIdiomas(['en'], 0, { exactos: true })!, /todos los idiomas/);
  assert.match(Sus.errorIdiomas(['en', 'fr', 'de'], 2)!, /no puedes tener 3/);
  assert.match(Sus.errorIdiomas([], 2)!, /al menos un idioma/);
  assert.deepEqual(Sus.leerIdiomas(' EN,fr,xx,en '), ['en', 'fr']); assert.equal(Sus.leerIdiomas(undefined), null);
  assert.deepEqual(Sus.ajustarAlPlan(['en', 'fr', 'de'], 2), ['en', 'fr']); assert.deepEqual(Sus.ajustarAlPlan(['en'], 0), ['en']);
  assert.equal(Sus.esCambioIdiomas(['en', 'fr'], ['fr', 'en']), false, 'reordenar');
  assert.equal(Sus.esCambioIdiomas(['en'], ['en', 'fr']), false, 'completar «por elegir»');
  assert.equal(Sus.esCambioIdiomas(['en', 'fr'], ['en', 'de']), true);
  const ahora = new Date('2026-10-20T12:00:00Z');
  const base = { usuario_id: 'u', plan_id: 'p2', origen: 'stripe', estado: 'activa', cancela_al_final: false, periodo_fin: '2026-11-01T00:00:00Z', periodo_inicio: '2026-10-01T00:00:00Z',
    idiomas: ['en', 'fr'], todos_idiomas: false } as any;
  const acc = Sus.accesoPorIdioma(base, 2, ahora);
  assert.equal(Object.keys(acc).length, 10); assert.deepEqual(Object.keys(acc).filter((k) => acc[k]), ['en', 'fr']);
  assert.ok(Object.values(Sus.accesoPorIdioma({ ...base, todos_idiomas: true }, 2, ahora)).every(Boolean), 'cortesía «todos»');
  assert.ok(Object.values(Sus.accesoPorIdioma(base, 0, ahora)).every(Boolean), 'plan de 0 = todos');
  assert.ok(!Object.values(Sus.accesoPorIdioma({ ...base, estado: 'impago' }, 2, ahora)).some(Boolean));
  assert.deepEqual(Sus.idiomasDe({ ...base, idiomas: ['en'] }, 3), { idiomas: ['en'], todos: false, porElegir: 2 });
  // uno_por_periodo con periodo de Stripe: un cambio desde periodo_inicio; el siguiente, al acabar el periodo.
  assert.deepEqual(Sus.reglaCambioIdiomas('uno_por_periodo', base, ahora), { regla: 'uno_por_periodo', permitido: true, proximoCambio: null });
  assert.deepEqual(Sus.reglaCambioIdiomas('uno_por_periodo', { ...base, ultimo_cambio_idiomas: '2026-10-05T00:00:00Z' }, ahora),
    { regla: 'uno_por_periodo', permitido: false, proximoCambio: '2026-11-01T00:00:00.000Z' });
  assert.equal(Sus.reglaCambioIdiomas('uno_por_periodo', { ...base, ultimo_cambio_idiomas: '2026-09-25T00:00:00Z' }, ahora).permitido, true, 'periodo anterior');
  // Cortesía sin periodo: cada 30 días desde el último cambio.
  const cort = { ...base, origen: 'cortesia', periodo_fin: null, periodo_inicio: null };
  assert.deepEqual(Sus.reglaCambioIdiomas('uno_por_periodo', { ...cort, ultimo_cambio_idiomas: '2026-10-10T00:00:00Z' }, ahora),
    { regla: 'uno_por_periodo', permitido: false, proximoCambio: '2026-11-09T00:00:00.000Z' });
  assert.equal(Sus.reglaCambioIdiomas('uno_por_periodo', { ...cort, ultimo_cambio_idiomas: '2026-09-10T00:00:00Z' }, ahora).permitido, true);
  assert.deepEqual(Sus.reglaCambioIdiomas('libre', { ...base, ultimo_cambio_idiomas: '2026-10-19T00:00:00Z' }, ahora), { regla: 'libre', permitido: true, proximoCambio: null });
  assert.deepEqual(Sus.reglaCambioIdiomas('solo_admin', base, ahora), { regla: 'solo_admin', permitido: false, proximoCambio: null });
  assert.equal(Sus.reglaCambioIdiomas('libre', { ...base, estado: 'vencida' }, ahora).permitido, false, 'sin acceso no hay cambios');
});

test('desglose por idioma: suscriptores, cortesías y MRR repartido a partes iguales', () => {
  const ahora = new Date('2026-10-20T12:00:00Z');
  const fila = (o: object) => ({ origen: 'stripe', estado: 'activa', periodo_fin: null, importe_centavos: 3000, moneda: 'usd', intervalo: 'mes', plan_idiomas: 2, todos_idiomas: false, ...o });
  const d = Sus.desglosePorIdioma([
    fila({ idiomas: ['en', 'fr'] }),                                   // 30/mes → 15 en + 15 fr
    fila({ idiomas: ['en'], importe_centavos: 24000, intervalo: 'anio', plan_idiomas: 1 }), // 20/mes → en
    fila({ idiomas: [], plan_idiomas: 0, importe_centavos: 5000 }),     // todos
    fila({ idiomas: [] }),                                             // por elegir
    fila({ origen: 'cortesia', idiomas: ['fr'], importe_centavos: null }),
    fila({ idiomas: ['de'], estado: 'impago' }),                       // sin acceso: no cuenta
  ], ahora);
  const de = (k: string) => d.find((x) => x.idioma === k);
  assert.deepEqual(de('en'), { idioma: 'en', suscriptores: 2, cortesias: 0, mrr: 35 });
  assert.deepEqual(de('fr'), { idioma: 'fr', suscriptores: 1, cortesias: 1, mrr: 15 });
  assert.deepEqual(de('todos'), { idioma: 'todos', suscriptores: 1, cortesias: 0, mrr: 50 });
  assert.deepEqual(de('por_elegir'), { idioma: 'por_elegir', suscriptores: 1, cortesias: 0, mrr: 30 });
  assert.deepEqual(de('de'), { idioma: 'de', suscriptores: 0, cortesias: 0, mrr: 0 });
  assert.equal(d.length, 12);
});

// ── Rutas contra la base temporal ────────────────────────────────────────────
let app: Awaited<ReturnType<typeof crearApp>>;
let U1 = '', U2 = '', U3 = '';
const tok = (sub: string, rol: 'alumno' | 'admin' = 'alumno') => ({ authorization: `Bearer ${app.jwt.sign({ sub, rol })}` });
const admin = () => tok('admin', 'admin');

before(async () => {
  if (!hayBd) return;
  await migrar();
  app = await crearApp();
  const ins = (email: string) => pool.query('INSERT INTO usuarios (email, nombre, trial_segundos) VALUES ($1, $2, 600) RETURNING id', [email, email.split('@')[0]]).then((r) => r.rows[0].id as string);
  U1 = await ins('ana@pagos.test'); U2 = await ins('beto@pagos.test'); U3 = await ins('carla@pagos.test');
});
after(async () => {
  globalThis.fetch = fetchOriginal;
  if (!hayBd) return;
  await app?.close();
  await pool.end();
  const c = new pg.Client({ connectionString: urlBase }); await c.connect();
  await c.query(`DROP DATABASE IF EXISTS ${NOMBRE_BD} WITH (FORCE)`); await c.end();
});

test('migraciones 006, 007 y 008: idempotentes, 3 planes semilla (y el Familiar de 010) y p2 destacado', { skip: sinBd }, async () => {
  const { readFile } = await import('node:fs/promises');
  await pool.query(await readFile(new URL('../sql/006_pagos.sql', import.meta.url), 'utf8')); // segunda vez: sin efecto ni error
  const r = await pool.query('SELECT id, precio_centavos, idiomas, nombre->>\'en\' AS en, jsonb_array_length(incluye->\'en\') AS ventajas FROM planes ORDER BY orden');
  assert.deepEqual(r.rows, [
    { id: 'p1', precio_centavos: 2000, idiomas: 1, en: 'One language', ventajas: 5 },
    { id: 'p2', precio_centavos: 3000, idiomas: 2, en: 'Two languages', ventajas: 4 },
    { id: 'p3', precio_centavos: 4000, idiomas: 3, en: 'Three languages', ventajas: 4 },
    { id: 'familiar', precio_centavos: 6000, idiomas: 1, en: 'Family', ventajas: 4 },
  ]);
  assert.equal((await pool.query('SELECT prueba_minutos FROM ajustes_pago')).rows[0].prueba_minutos, 60);
  const destacados = async () => (await pool.query('SELECT id FROM planes WHERE destacado ORDER BY id')).rows.map((f) => f.id);
  assert.deepEqual(await destacados(), ['p2'], 'p2 destacado («POPULAR»)');
  // 007 en una base con la semilla anterior (p2 sin destacar, sin editar): lo corrige; dos veces, sin efecto.
  const m7 = await readFile(new URL('../sql/007_pagos_portal.sql', import.meta.url), 'utf8');
  await pool.query("UPDATE planes SET destacado = false WHERE id = 'p2'");
  await pool.query(m7); await pool.query(m7);
  assert.deepEqual(await destacados(), ['p2']);
  // Si el administrador ya lo editó (actualizado_en distinto), 007 no pisa su decisión.
  await pool.query("UPDATE planes SET destacado = false, actualizado_en = actualizado_en + interval '1 second' WHERE id = 'p2'");
  await pool.query(m7);
  assert.deepEqual(await destacados(), []);
  await pool.query("UPDATE planes SET destacado = true, actualizado_en = creado_en WHERE id = 'p2'");
  // 008 (idiomas por suscripción) dos veces: sin error; regla por defecto y `idiomas` admite 0 pero no 11.
  const m8 = await readFile(new URL('../sql/008_pagos_idiomas.sql', import.meta.url), 'utf8');
  await pool.query(m8); await pool.query(m8);
  assert.equal((await pool.query('SELECT cambio_idiomas FROM ajustes_pago')).rows[0].cambio_idiomas, 'uno_por_periodo');
  await assert.rejects(pool.query("UPDATE planes SET idiomas = 11 WHERE id = 'p1'"));
  await assert.rejects(pool.query("UPDATE ajustes_pago SET cambio_idiomas = 'otra'"));
});

test('GET /planes sin Stripe: 4 planes con duraciones, pagos no disponibles; checkout 503', { skip: sinBd }, async () => {
  const r = await app.inject({ url: '/planes' });
  assert.equal(r.statusCode, 200);
  const d = r.json();
  assert.deepEqual(d.pagos, { disponible: false, modo: null });
  assert.equal(d.pruebaMinutos, 60); assert.equal(d.moneda, 'usd');
  assert.deepEqual(d.planes.map((p: any) => [p.id, p.precio, p.intervalo]), [['p1', 20, 'mes'], ['p2', 30, 'mes'], ['p3', 40, 'mes'], ['familiar', 60, 'mes']]);
  // Tabla de precios: 1, 3, 6 y 12 meses; el Familiar cubre 4 personas.
  assert.deepEqual(d.planes.map((p: any) => [p.id, p.usuarios, p.duraciones.map((x: any) => `${x.meses}:${x.precio}`).join(' ')]), [
    ['p1', 1, '1:20 3:55 6:110 12:220'], ['p2', 1, '1:30 3:85 6:170 12:320'], ['p3', 1, '1:40 3:110 6:220 12:450'], ['familiar', 4, '1:60 3:165 6:335 12:600'],
  ]);
  assert.deepEqual(d.planes[0].nombre, { es: 'Un idioma', en: 'One language' });
  assert.equal((await app.inject({ method: 'POST', url: '/pagos/checkout', headers: tok(U1), payload: { planId: 'p1' } })).statusCode, 503);
  assert.equal((await app.inject({ method: 'POST', url: '/pagos/checkout', payload: { planId: 'p1' } })).statusCode, 401);
});

test('GET /planes no muestra planes ocultos ni archivados; panel: crear, editar, ocultar y archivar', { skip: sinBd }, async () => {
  const c = await app.inject({ method: 'POST', url: '/admin/planes', headers: admin(), payload: {
    nombre: { es: 'Anual total', en: 'Yearly all' }, incluye: { es: ['Todo'], en: ['Everything'] }, idiomas: 10, precio: 240, intervalo: 'anio', orden: 4,
  } });
  assert.equal(c.statusCode, 201);
  assert.equal(c.json().plan.id, 'anual-total');
  assert.equal(c.json().plan.stripe.estado, 'sin stripe');
  assert.ok((await app.inject({ url: '/planes' })).json().planes.some((p: any) => p.id === 'anual-total' && p.precio === 240 && p.intervalo === 'anio'));
  const e = await app.inject({ method: 'PUT', url: '/admin/planes/anual-total', headers: admin(), payload: { visible: false, destacado: true } });
  assert.equal(e.statusCode, 200);
  assert.ok(!(await app.inject({ url: '/planes' })).json().planes.some((p: any) => p.id === 'anual-total'), 'oculto');
  await app.inject({ method: 'PUT', url: '/admin/planes/anual-total', headers: admin(), payload: { visible: true } });
  assert.equal((await app.inject({ method: 'POST', url: '/admin/planes/anual-total/archivar', headers: admin(), payload: {} })).statusCode, 200);
  assert.ok(!(await app.inject({ url: '/planes' })).json().planes.some((p: any) => p.id === 'anual-total'), 'archivado');
  assert.equal((await app.inject({ method: 'PUT', url: '/admin/planes/p1', headers: admin(), payload: { precio: 0.1 } })).statusCode, 400);
  assert.equal((await app.inject({ method: 'POST', url: '/admin/planes', headers: tok(U1), payload: {} })).statusCode, 403);
  assert.equal((await app.inject({ method: 'DELETE', url: '/admin/planes/anual-total', headers: admin() })).statusCode, 200);
});

test('PUT /usuarios/me/progreso: ignora el planId del cliente y la prueba no baja (JSON normal fuera del webhook)', { skip: sinBd }, async () => {
  const put = (trialSegundos: number) => app.inject({ method: 'PUT', url: '/usuarios/me/progreso', headers: tok(U2), payload: { planId: 'p3', trialSegundos, xp: 5 } });
  const r = await put(900);
  assert.equal(r.statusCode, 200);
  assert.equal(r.json().planId, '');
  const u = (await pool.query('SELECT plan_id, trial_segundos FROM usuarios WHERE id = $1', [U2])).rows[0];
  assert.deepEqual(u, { plan_id: '', trial_segundos: 900 });
  await put(100); // la app manda menos (otro dispositivo): no baja
  assert.equal((await pool.query('SELECT trial_segundos FROM usuarios WHERE id = $1', [U2])).rows[0].trial_segundos, 900);
  const g = (await app.inject({ url: '/usuarios/me/progreso', headers: tok(U2) })).json();
  assert.equal(g.estado.planId, ''); assert.equal(g.estado.trialSegundos, 900);
  const s = (await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(U2) })).json();
  assert.deepEqual(s.prueba, { minutos: 60, segundosUsados: 900, restanteSegundos: 2700, agotada: false });
  assert.equal(s.estado, 'sin_plan'); assert.equal(s.acceso, false);
});

test('cortesía con y sin fecha: da acceso, el PUT no la quita, se puede retirar', { skip: sinBd }, async () => {
  const url = `/admin/usuarios/${U3}/cortesia`;
  assert.equal((await app.inject({ method: 'POST', url, headers: admin(), payload: { planId: 'p2', hasta: '2020-01-01T00:00:00Z' } })).statusCode, 400);
  assert.equal((await app.inject({ method: 'POST', url, headers: admin(), payload: { planId: 'nada' } })).statusCode, 400);
  const sin = await app.inject({ method: 'POST', url, headers: admin(), payload: { planId: 'p2', nota: 'beca' } });
  assert.equal(sin.statusCode, 200);
  assert.equal(sin.json().acceso, true); assert.equal(sin.json().periodoFin, null); assert.equal(sin.json().origen, 'cortesia');
  const me = (await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(U3) })).json();
  assert.equal(me.planId, 'p2'); assert.equal(me.acceso, true); assert.equal(me.puedeGestionar, false);
  await app.inject({ method: 'PUT', url: '/usuarios/me/progreso', headers: tok(U3), payload: { planId: '' } });
  assert.equal((await pool.query('SELECT plan_id FROM usuarios WHERE id = $1', [U3])).rows[0].plan_id, 'p2', 'derivado');
  const hasta = new Date(Date.now() + 7 * 86400_000).toISOString();
  const con = (await app.inject({ method: 'POST', url, headers: admin(), payload: { planId: 'p1', hasta } })).json();
  assert.equal(con.planId, 'p1'); assert.equal(con.periodoFin, hasta);
  // Caducada: sin acceso; el panel la ve «vencida» y el plan derivado se limpia al refrescar.
  await pool.query("UPDATE suscripciones SET periodo_fin = now() - interval '1 minute' WHERE usuario_id = $1", [U3]);
  const venc = (await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(U3) })).json();
  assert.equal(venc.acceso, false); assert.equal(venc.estado, 'vencida'); assert.equal(venc.planId, '');
  await Sus.refrescarPlanesDerivados();
  assert.equal((await pool.query('SELECT plan_id FROM usuarios WHERE id = $1', [U3])).rows[0].plan_id, '');
  const q = await app.inject({ method: 'DELETE', url, headers: admin() });
  assert.equal(q.statusCode, 200); assert.equal(q.json().estado, 'sin_plan');
  assert.equal((await app.inject({ method: 'DELETE', url, headers: admin() })).statusCode, 404);
});

test('Stripe en Conexiones: pk rechazada sin llamar; 401 «Clave inválida»; guardar crea webhook, portal y planes', { skip: sinBd }, async () => {
  st.llamadas = [];
  const pk = await app.inject({ method: 'PUT', url: '/admin/conexiones/stripe', headers: admin(), payload: { secretKey: FALSA.pk } });
  assert.equal(pk.statusCode, 400);
  assert.equal(pk.json().errores.secretKey, 'Esta es la clave publicable; pega la secreta (sk_…)');
  assert.equal(st.llamadas.length, 0);
  const inv = await app.inject({ method: 'PUT', url: '/admin/conexiones/stripe', headers: admin(), payload: { secretKey: FALSA.invalida } });
  assert.equal(inv.statusCode, 422);
  assert.match(inv.json().verificacion.mensaje, /^Clave inválida: Stripe la rechazó/);
  assert.equal((await pool.query('SELECT count(*)::int AS n FROM conexiones')).rows[0].n, 0);

  st.llamadas = [];
  const ok = await app.inject({ method: 'PUT', url: '/admin/conexiones/stripe', headers: admin(), payload: { secretKey: FALSA.sk, urlApp: 'https://app.onelingo.test/' } });
  assert.equal(ok.statusCode, 200, ok.body);
  const det = ok.json().verificacion.detalles.join(' ');
  assert.match(det, /MODO TEST/); assert.match(det, /Webhook creado en https:\/\/app\.onelingo\.test\/api\/stripe\/webhook/);
  assert.match(det, /Customer Portal configurado: .*cambio de plan entre 4 planes/); assert.match(det, /Planes sincronizados con Stripe: 4/);
  assert.equal(llamadasA(/^POST \/billing_portal\/configurations/).length, 1, 'una sola configuración del portal al vincular');
  const we = llamadasA(/^POST \/webhook_endpoints$/)[0].datos;
  assert.deepEqual(we.getAll('enabled_events[0]').concat(we.getAll('enabled_events[5]')), ['checkout.session.completed', 'invoice.payment_failed']);
  assert.ok(llamadasA(/./).every((l) => l.auth === `Bearer ${FALSA.sk}`));
  const fila = (await pool.query("SELECT datos FROM conexiones WHERE proveedor = 'stripe'")).rows[0];
  assert.ok(!fila.datos.includes(FALSA.sk) && !fila.datos.includes(FALSA.whsec), 'cifrado');
  assert.equal(C.stripeConfig().webhookSecret === FALSA.whsec, true);
  const g = await app.inject({ url: '/admin/conexiones', headers: admin() });
  assert.ok(!g.body.includes(FALSA.sk) && !g.body.includes(FALSA.whsec), 'sin claves en el resumen');
  const s = g.json().proveedores.find((p: any) => p.id === 'stripe');
  assert.equal(s.origen, 'panel'); assert.equal(s.modo, 'test'); assert.equal(s.webhook, true); assert.equal(s.clave, 'sk_test_…' + FALSA.sk.slice(-4));
  assert.deepEqual(Object.keys(s.campos), ['secretKey', 'urlApp']);
  const pl = (await app.inject({ url: '/planes' })).json();
  assert.deepEqual(pl.pagos, { disponible: true, modo: 'test' });
  const prod = llamadasA(/^POST \/products$/)[0].datos;
  assert.equal(prod.get('metadata[plan_id]'), 'p1');
  const pr = llamadasA(/^POST \/prices$/)[0].datos;
  assert.deepEqual([pr.get('unit_amount'), pr.get('currency'), pr.get('recurring[interval]')], ['2000', 'usd', 'month']);
  // Volver a guardar con la misma clave: reutiliza el webhook (conocemos su secreto).
  const otra = await app.inject({ method: 'PUT', url: '/admin/conexiones/stripe', headers: admin(), payload: { urlApp: 'https://app.onelingo.test' } });
  assert.match(otra.json().verificacion.detalles.join(' '), /Webhook reutilizado/);
  assert.equal(st.webhooks.length, 1);
});

test('checkout y confirmar sin webhook; 409 con suscripción activa; portal', { skip: sinBd }, async () => {
  st.llamadas = [];
  // Validación de idiomas (p2 incluye 2): número exacto, códigos válidos y sin repetidos; 400 sin llamar a Stripe.
  const mal = async (idiomas: unknown) => (await app.inject({ method: 'POST', url: '/pagos/checkout', headers: tok(U1), payload: { planId: 'p2', idiomas } }));
  assert.match((await mal(['en'])).json().error, /^Este plan incluye 2 idiomas: elige exactamente 2 \(has elegido 1\)\.$/);
  assert.match((await mal(undefined)).json().error, /elige exactamente 2 \(has elegido 0\)/);
  assert.match((await mal(['en', 'xx'])).json().error, /^Código de idioma no válido: xx\./);
  assert.match((await mal(['en', 'EN'])).json().error, /^Idioma repetido: en\.$/);
  assert.equal((await mal(['en', 'fr', 'de'])).statusCode, 400);
  assert.equal(llamadasA(/^POST \/checkout\/sessions$/).length, 0);
  const r = await app.inject({ method: 'POST', url: '/pagos/checkout', headers: tok(U1), payload: { planId: 'p2', idiomas: ['EN', 'fr'] } });
  assert.equal(r.statusCode, 200, r.body);
  assert.match(r.json().url, /^https:\/\/checkout\.stripe\.com\//);
  const d = llamadasA(/^POST \/checkout\/sessions$/)[0].datos;
  assert.equal(d.get('mode'), 'subscription'); assert.equal(d.get('client_reference_id'), U1);
  assert.equal(d.get('customer_email'), 'ana@pagos.test'); assert.equal(d.get('customer'), null);
  assert.equal(d.get('success_url'), 'https://app.onelingo.test/#/pago?estado=ok&session_id={CHECKOUT_SESSION_ID}');
  assert.equal(d.get('cancel_url'), 'https://app.onelingo.test/#/pago?estado=cancelado');
  assert.equal(d.get('subscription_data[metadata][usuario_id]'), U1);
  assert.equal(d.get('subscription_data[metadata][idiomas]'), 'en,fr'); assert.equal(d.get('metadata[idiomas]'), 'en,fr');
  const precioP2 = (await pool.query("SELECT stripe_precio_id FROM planes WHERE id = 'p2'")).rows[0].stripe_precio_id;
  assert.equal(d.get('line_items[0][price]'), precioP2); assert.equal(d.get('line_items[0][quantity]'), '1');

  // El alumno paga (simulado) y vuelve: «Confirmar» consulta la sesión.
  const sesion = st.sesiones.values().next().value;
  sesion.metadata = { usuario_id: U1, plan_id: 'p2', idiomas: 'en,fr' };
  const sub = suscripcionStripe({ precio: st.precios.get(precioP2) }); // sin metadata: los idiomas salen de la sesión
  sesion.status = 'complete'; sesion.subscription = sub.id;
  assert.equal((await app.inject({ method: 'POST', url: '/pagos/confirmar', headers: tok(U2), payload: { sessionId: sesion.id } })).statusCode, 403, 'sesión ajena');
  const c = await app.inject({ method: 'POST', url: '/pagos/confirmar', headers: tok(U1), payload: { sessionId: sesion.id } });
  assert.equal(c.statusCode, 200);
  assert.deepEqual([c.json().planId, c.json().estado, c.json().origen, c.json().acceso, c.json().modo, c.json().puedeGestionar], ['p2', 'activa', 'stripe', true, 'test', true]);
  assert.equal((await pool.query('SELECT plan_id FROM usuarios WHERE id = $1', [U1])).rows[0].plan_id, 'p2');
  assert.deepEqual([c.json().idiomas, c.json().todosLosIdiomas, c.json().idiomasPorElegir], [['en', 'fr'], false, 0]);
  assert.deepEqual(Object.entries(c.json().accesoPorIdioma).filter(([, v]) => v).map(([k]) => k), ['en', 'fr']);
  assert.equal(Object.keys(c.json().accesoPorIdioma).length, 10);
  const otra = await app.inject({ method: 'POST', url: '/pagos/checkout', headers: tok(U1), payload: { planId: 'p3' } });
  assert.equal(otra.statusCode, 409); assert.equal(otra.json().portal, true);
  // Cortesía rechazada si ya paga por Stripe.
  assert.equal((await app.inject({ method: 'POST', url: `/admin/usuarios/${U1}/cortesia`, headers: admin(), payload: { planId: 'p3' } })).statusCode, 409);
  const portal = await app.inject({ method: 'POST', url: '/pagos/portal', headers: tok(U1) });
  assert.match(portal.json().url, /^https:\/\/billing\.stripe\.com\//);
  const pd = llamadasA(/^POST \/billing_portal\/sessions$/)[0].datos;
  assert.equal(pd.get('customer'), sub.customer); assert.equal(pd.get('return_url'), 'https://app.onelingo.test/#/pago?estado=portal');
  assert.equal(pd.get('configuration'), (await pool.query('SELECT stripe_portal_id FROM ajustes_pago')).rows[0].stripe_portal_id);
  assert.match(pd.get('configuration') ?? '', /^bpc_/);
  assert.equal((await app.inject({ method: 'POST', url: '/pagos/portal', headers: tok(U2) })).statusCode, 409);
  // Login: el estado devuelto lleva el plan del servidor.
  await pool.query(`INSERT INTO progreso (usuario_id, estado) VALUES ($1, '{"planId":"p3","trialSegundos":5}') ON CONFLICT (usuario_id) DO UPDATE SET estado = EXCLUDED.estado`, [U1]);
  const g = (await app.inject({ url: '/usuarios/me/progreso', headers: tok(U1) })).json();
  assert.equal(g.estado.planId, 'p2'); assert.equal(g.estado.trialSegundos, 600);
});

const enviar = (ev: object, op: { secreto?: string; t?: number } = {}) => {
  const cuerpo = JSON.stringify(ev);
  return app.inject({ method: 'POST', url: '/stripe/webhook', headers: { 'content-type': 'application/json; charset=utf-8', 'stripe-signature': S.firmarEvento(cuerpo, op.secreto ?? FALSA.whsec, op.t) }, payload: cuerpo });
};
const evento = (type: string, object: any, idEv = id('evt')) => ({ id: idEv, object: 'event', type, livemode: false, created: Math.floor(Date.now() / 1000), data: { object } });
const estadoDe = async (u: string) => (await app.inject({ url: '/usuarios/me/suscripcion', headers: tok(u) })).json();

test('webhook: firma válida, inválida y caducada; evento repetido idempotente', { skip: sinBd }, async () => {
  const precio = st.precios.get((await pool.query("SELECT stripe_precio_id FROM planes WHERE id = 'p1'")).rows[0].stripe_precio_id);
  const sub = suscripcionStripe({ usuarioId: U2, precio, idiomas: 'en' });
  const ev = evento('customer.subscription.created', sub);
  assert.equal((await enviar(ev, { secreto: 'whsec_falso' })).statusCode, 400);
  assert.equal((await enviar(ev, { t: Math.floor(Date.now() / 1000) - 600 })).statusCode, 400);
  const sinFirma = await app.inject({ method: 'POST', url: '/stripe/webhook', headers: { 'content-type': 'application/json' }, payload: JSON.stringify(ev) });
  assert.equal(sinFirma.statusCode, 400);
  assert.equal((await pool.query('SELECT count(*)::int AS n FROM pagos_eventos')).rows[0].n, 0, 'nada registrado con firma mala');
  const r = await enviar(ev);
  assert.equal(r.statusCode, 200, r.body); assert.equal(r.json().aplicada, true);
  assert.equal((await estadoDe(U2)).planId, 'p1');
  assert.deepEqual((await estadoDe(U2)).idiomas, ['en'], 'idiomas de metadata.idiomas de la suscripción');
  // invoice.paid repetido: la segunda vez no se consulta a Stripe ni se reprocesa.
  const inv = evento('invoice.paid', { id: 'in_1', parent: { subscription_details: { subscription: sub.id } } });
  st.llamadas = [];
  assert.equal((await enviar(inv)).statusCode, 200);
  assert.equal(llamadasA(/^GET \/subscriptions\//).length, 1);
  const rep = await enviar(inv);
  assert.equal(rep.statusCode, 200); assert.equal(rep.json().repetido, true);
  assert.equal(llamadasA(/^GET \/subscriptions\//).length, 1);
  assert.equal((await pool.query('SELECT count(*)::int AS n FROM pagos_eventos WHERE procesado')).rows[0].n, 2);
});

test('webhook: created → updated con cancel_at_period_end → payment_failed → deleted', { skip: sinBd }, async () => {
  const precio = st.precios.get((await pool.query("SELECT stripe_precio_id FROM planes WHERE id = 'p3'")).rows[0].stripe_precio_id);
  const sub = suscripcionStripe({ precio, cliente: 'cus_carla' });
  // created sin metadata: llega por checkout.session.completed con client_reference_id.
  st.sesiones.set('cs_test_carla', { id: 'cs_test_carla', status: 'complete', client_reference_id: U3, subscription: sub.id });
  assert.equal((await enviar(evento('checkout.session.completed', { id: 'cs_test_carla', mode: 'subscription', subscription: sub.id, client_reference_id: U3, metadata: { idiomas: 'ja,en,ko' } }))).statusCode, 200);
  let e = await estadoDe(U3);
  assert.deepEqual([e.planId, e.estado, e.acceso, e.cancelaAlFinal, e.idiomas], ['p3', 'activa', true, false, ['ja', 'en', 'ko']]);
  // updated: cancela al final del periodo (sigue con acceso).
  sub.cancel_at_period_end = true;
  await enviar(evento('customer.subscription.updated', { ...sub }));
  e = await estadoDe(U3);
  assert.deepEqual([e.estado, e.acceso, e.cancelaAlFinal], ['activa', true, true]);
  assert.ok(new Date(e.periodoFin) > new Date());
  // payment_failed: impago, sin acceso.
  await enviar(evento('invoice.payment_failed', { id: 'in_2', subscription: sub.id }));
  e = await estadoDe(U3);
  assert.deepEqual([e.estado, e.acceso, e.planId], ['impago', false, '']);
  assert.equal((await pool.query('SELECT plan_id FROM usuarios WHERE id = $1', [U3])).rows[0].plan_id, '');
  // deleted al momento: cancelada y sin acceso (terminó ya).
  const fin = Math.floor(Date.now() / 1000) - 5;
  await enviar(evento('customer.subscription.deleted', { ...sub, status: 'canceled', ended_at: fin, canceled_at: fin }));
  e = await estadoDe(U3);
  assert.deepEqual([e.estado, e.acceso, e.cancelaAlFinal], ['cancelada', false, false]);
  // Un evento de otro modo (live) se ignora.
  const live = await enviar({ ...evento('customer.subscription.updated', { ...sub, status: 'active' }), livemode: true });
  assert.equal(live.json().ignorado, 'otro modo');
  assert.equal((await estadoDe(U3)).estado, 'cancelada');
});

test('cambio de precio: nuevo Price, el viejo se archiva y los suscriptores conservan el suyo', { skip: sinBd }, async () => {
  const antes = (await pool.query("SELECT stripe_precio_id, stripe_producto_id FROM planes WHERE id = 'p2'")).rows[0];
  st.llamadas = [];
  const r = await app.inject({ method: 'PUT', url: '/admin/planes/p2', headers: admin(), payload: { precio: 35 } });
  assert.equal(r.statusCode, 200);
  assert.equal(r.json().sync.ok, true); assert.equal(r.json().sync.precioNuevo, true);
  assert.equal(r.json().plan.stripe.estado, 'sincronizado');
  const despues = (await pool.query("SELECT stripe_precio_id, stripe_producto_id FROM planes WHERE id = 'p2'")).rows[0];
  assert.notEqual(despues.stripe_precio_id, antes.stripe_precio_id);
  assert.equal(despues.stripe_producto_id, antes.stripe_producto_id);
  assert.equal(llamadasA(/^POST \/prices$/)[0].datos.get('unit_amount'), '3500');
  assert.equal(st.precios.get(antes.stripe_precio_id).active, false, 'el viejo se archiva');
  assert.equal(llamadasA(/subscriptions/).length, 0, 'no se toca ninguna suscripción');
  const s = (await pool.query('SELECT stripe_precio_id, importe_centavos FROM suscripciones WHERE usuario_id = $1', [U1])).rows[0];
  assert.deepEqual(s, { stripe_precio_id: antes.stripe_precio_id, importe_centavos: 3000 });
  // Solo cambiar el nombre no crea otro Price.
  st.llamadas = [];
  await app.inject({ method: 'PUT', url: '/admin/planes/p2', headers: admin(), payload: { nombre: { es: 'Dos idiomas', en: 'Two languages' } } });
  assert.equal(llamadasA(/^POST \/prices$/).length, 0);
  // Fallo de Stripe: se guarda igual, «sin sincronizar» y se puede reintentar.
  const fetchSim = globalThis.fetch;
  globalThis.fetch = (async () => json(500, { error: { message: 'Stripe caído' } })) as typeof fetch;
  try {
    const f = await app.inject({ method: 'PUT', url: '/admin/planes/p2', headers: admin(), payload: { precio: 36 } });
    assert.equal(f.statusCode, 200); assert.equal(f.json().sync.ok, false);
    assert.equal(f.json().plan.precio, 36); assert.equal(f.json().plan.stripe.estado, 'sin sincronizar');
  } finally { globalThis.fetch = fetchSim; }
  st.llamadas = [];
  const re = await app.inject({ method: 'POST', url: '/admin/planes/p2/sincronizar', headers: admin() });
  assert.equal(re.json().plan.stripe.estado, 'sincronizado'); assert.equal(re.json().portal.ok, true);
  const nuevo = (await pool.query("SELECT stripe_precio_id FROM planes WHERE id = 'p2'")).rows[0].stripe_precio_id;
  const pc = llamadasA(/^POST \/billing_portal\/configurations\/bpc_\w+$/).at(-1)!.datos;
  assert.equal(pc.get('features[subscription_update][products][1][prices][0]'), nuevo, 'el portal ofrece el Price actual de p2');
  const hist = (await pool.query("SELECT precio_id, archivado_en IS NOT NULL AS archivado FROM planes_precios WHERE plan_id = 'p2' ORDER BY creado_en, precio_id")).rows;
  assert.ok(hist.some((h) => h.precio_id === antes.stripe_precio_id && h.archivado), 'el Price viejo queda en el historial, archivado');
  assert.ok(hist.some((h) => h.precio_id === nuevo && !h.archivado));
});

test('Customer Portal: se actualiza al archivar y restaurar un plan (solo planes visibles y sincronizados)', { skip: sinBd }, async () => {
  const productos = (d: URLSearchParams) => [0, 1, 2, 3].map((i) => d.get(`features[subscription_update][products][${i}][product]`)).filter(Boolean);
  const prod = async (id: string) => (await pool.query('SELECT stripe_producto_id FROM planes WHERE id = $1', [id])).rows[0].stripe_producto_id;
  const [p1, p2, p3, fam] = [await prod('p1'), await prod('p2'), await prod('p3'), await prod('familiar')];
  st.llamadas = [];
  const a = await app.inject({ method: 'POST', url: '/admin/planes/p3/archivar', headers: admin(), payload: {} });
  assert.equal(a.statusCode, 200); assert.equal(a.json().portal.ok, true); assert.equal(a.json().portal.productos, 3);
  const cfg = llamadasA(/^POST \/billing_portal\/configurations\/bpc_\w+$/);
  assert.equal(cfg.length, 1, 'actualiza la configuración guardada, no crea otra');
  assert.deepEqual(productos(cfg[0].datos), [p1, p2, fam]);
  // Cada producto ofrece su Price mensual y los de 3, 6 y 12 meses.
  const precios = (d: URLSearchParams, i: number) => [0, 1, 2, 3, 4].map((j) => d.get(`features[subscription_update][products][${i}][prices][${j}]`)).filter(Boolean);
  const p1Precios = [(await pool.query("SELECT stripe_precio_id FROM planes WHERE id = 'p1'")).rows[0].stripe_precio_id,
    ...(await pool.query("SELECT precio_id FROM planes_precios WHERE plan_id = 'p1' AND meses > 1 AND archivado_en IS NULL ORDER BY meses")).rows.map((r) => r.precio_id)];
  assert.equal(p1Precios.length, 4);
  assert.deepEqual(precios(cfg[0].datos, 0), p1Precios);
  assert.equal(cfg[0].datos.get('features[subscription_update][default_allowed_updates][0]'), 'price');
  assert.equal(cfg[0].datos.get('features[subscription_update][proration_behavior]'), 'create_prorations');
  st.llamadas = [];
  await app.inject({ method: 'POST', url: '/admin/planes/p3/archivar', headers: admin(), payload: { archivado: false } });
  const v = await app.inject({ method: 'PUT', url: '/admin/planes/p3', headers: admin(), payload: { visible: true } });
  assert.equal(v.json().portal.productos, 4);
  assert.deepEqual(productos(llamadasA(/^POST \/billing_portal\/configurations\/bpc_\w+$/).at(-1)!.datos), [p1, p2, p3, fam]);
  assert.equal(st.portal.length, 1);
});

test('webhook: cambio de plan en el portal (subscription.updated) cambia plan_id por el Price nuevo, también con un Price archivado', { skip: sinBd }, async () => {
  const subId = (await pool.query('SELECT stripe_suscripcion_id, stripe_precio_id FROM suscripciones WHERE usuario_id = $1', [U1])).rows[0];
  const sub = st.subs.get(subId.stripe_suscripcion_id);
  const precioViejoP2 = st.precios.get(subId.stripe_precio_id);
  assert.equal(precioViejoP2.active, false, 'U1 sigue en el Price archivado de p2');
  // Cambia a p3 en el portal: la metadata de la suscripción sigue diciendo p2 (la de la compra).
  const precioP3 = st.precios.get((await pool.query("SELECT stripe_precio_id FROM planes WHERE id = 'p3'")).rows[0].stripe_precio_id);
  sub.metadata = { usuario_id: U1, plan_id: 'p2' };
  sub.items.data[0].price = precioP3;
  let r = await enviar(evento('customer.subscription.updated', { ...sub }));
  assert.equal(r.statusCode, 200, r.body); assert.equal(r.json().planId, 'p3');
  let e = await estadoDe(U1);
  assert.deepEqual([e.planId, e.estado, e.acceso], ['p3', 'activa', true]);
  assert.equal((await pool.query('SELECT plan_id FROM usuarios WHERE id = $1', [U1])).rows[0].plan_id, 'p3');
  let f = (await pool.query('SELECT plan_id, stripe_precio_id, importe_centavos FROM suscripciones WHERE usuario_id = $1', [U1])).rows[0];
  assert.deepEqual(f, { plan_id: 'p3', stripe_precio_id: precioP3.id, importe_centavos: 4000 });
  // Sube de 2 a 3 idiomas: conserva los 2 y el tercero queda «por elegir»; completarlo no cuenta como cambio.
  assert.deepEqual([e.idiomas, e.idiomasPorElegir], [['en', 'fr'], 1]);
  const comp = await app.inject({ method: 'PUT', url: '/usuarios/me/suscripcion/idiomas', headers: tok(U1), payload: { idiomas: ['en', 'fr', 'de'] } });
  assert.equal(comp.statusCode, 200, comp.body); assert.deepEqual([comp.json().idiomas, comp.json().idiomasPorElegir], [['en', 'fr', 'de'], 0]);
  assert.equal((await pool.query('SELECT ultimo_cambio_idiomas FROM suscripciones WHERE usuario_id = $1', [U1])).rows[0].ultimo_cambio_idiomas, null);
  assert.equal(comp.json().cambioIdiomas.permitido, true);
  // Vuelve al Price archivado de p2, sin metadata ni Product reconocible: solo lo encuentra el historial.
  sub.metadata = { usuario_id: U1, plan_id: 'p3' };
  sub.items.data[0].price = { ...precioViejoP2, metadata: {}, product: 'prod_desconocido' };
  r = await enviar(evento('customer.subscription.updated', { ...sub }));
  assert.equal(r.json().planId, 'p2');
  e = await estadoDe(U1);
  assert.equal(e.planId, 'p2');
  f = (await pool.query('SELECT plan_id, stripe_precio_id, importe_centavos, idiomas FROM suscripciones WHERE usuario_id = $1', [U1])).rows[0];
  // Baja de 3 a 2: se conservan los 2 primeros (el servidor nunca guarda más que los del plan).
  assert.deepEqual(f, { plan_id: 'p2', stripe_precio_id: precioViejoP2.id, importe_centavos: 3000, idiomas: ['en', 'fr'] });
});

test('panel: /admin/suscripciones con resumen (MRR) y /admin/resumen con métricas y minutos de prueba', { skip: sinBd }, async () => {
  const precioAnual = { id: 'price_anual', unit_amount: 24000, currency: 'usd', recurring: { interval: 'year' }, metadata: { plan_id: 'p1' } };
  await enviar(evento('customer.subscription.created', suscripcionStripe({ usuarioId: U2, precio: precioAnual })));
  const r = await app.inject({ url: '/admin/suscripciones', headers: admin() });
  assert.equal(r.statusCode, 200);
  const d = r.json();
  // U1: p2 a 30/mes (precio antiguo conservado) + U2: 240/año = 20/mes. U3 cancelada no cuenta.
  assert.equal(d.resumen.mrr, 50);
  assert.equal(d.resumen.activas, 2); assert.equal(d.resumen.canceladas30, 1); assert.equal(d.resumen.nuevas30, 3);
  const q = (await app.inject({ url: '/admin/suscripciones?q=carla&estado=cancelada', headers: admin() })).json();
  assert.deepEqual(q.filas.map((f: any) => f.email), ['carla@pagos.test']);
  assert.equal((await app.inject({ url: '/admin/suscripciones?estado=raro', headers: admin() })).statusCode, 400);
  await app.inject({ method: 'PUT', url: '/admin/pagos/ajustes', headers: admin(), payload: { pruebaMinutos: 30, moneda: 'usd' } });
  const res = (await app.inject({ url: '/admin/resumen', headers: admin() })).json();
  assert.equal(res.pruebaMinutos, 30); assert.equal(res.suscripciones.mrr, 50); assert.equal(res.usuarios.con_plan, 2);
  assert.equal((await app.inject({ url: '/planes' })).json().pruebaMinutos, 30);
  const det = (await app.inject({ url: `/admin/usuarios/${U1}`, headers: admin() })).json();
  assert.equal(det.suscripcion.planId, 'p2'); assert.equal(det.suscripcion.origen, 'stripe');
});

test('panel: desglose por idioma y filtro por idioma en /admin/suscripciones', { skip: sinBd }, async () => {
  const d = (await app.inject({ url: '/admin/suscripciones', headers: admin() })).json();
  const de = (k: string) => d.resumen.porIdioma.find((x: any) => x.idioma === k);
  // U1: p2 [en, fr] a 30/mes; U2: anual p1 (240/año = 20/mes) sin idiomas en la metadata → «por elegir».
  assert.deepEqual([de('en').suscriptores, de('en').mrr, de('fr').mrr, de('por_elegir').suscriptores, de('por_elegir').mrr], [1, 15, 15, 1, 20]);
  const u1 = d.filas.find((f: any) => f.usuarioId === U1);
  assert.deepEqual([u1.idiomas, u1.todosLosIdiomas, u1.idiomasPorElegir, u1.idiomasPlan], [['en', 'fr'], false, 0, 2]);
  const fr = (await app.inject({ url: '/admin/suscripciones?idioma=fr', headers: admin() })).json();
  assert.deepEqual(fr.filas.map((f: any) => f.usuarioId), [U1]);
  assert.equal((await app.inject({ url: '/admin/suscripciones?idioma=xx', headers: admin() })).statusCode, 400);
});

test('cambioIdiomas: uno_por_periodo (proximoCambio), libre y solo_admin; el admin edita sin regla; queda en eventos', { skip: sinBd }, async () => {
  const put = (idiomas: string[], h = tok(U1)) => app.inject({ method: 'PUT', url: '/usuarios/me/suscripcion/idiomas', headers: h, payload: { idiomas } });
  const ajustes = (cambioIdiomas: string) => app.inject({ method: 'PUT', url: '/admin/pagos/ajustes', headers: admin(), payload: { pruebaMinutos: 60, moneda: 'usd', cambioIdiomas } });
  assert.equal((await app.inject({ url: '/admin/pagos/ajustes', headers: admin() })).json().cambioIdiomas, 'uno_por_periodo');
  let e = await estadoDe(U1);
  assert.deepEqual(e.cambioIdiomas, { regla: 'uno_por_periodo', permitido: true, proximoCambio: null });
  let r = await put(['en', 'de']);
  assert.equal(r.statusCode, 200, r.body); assert.deepEqual(r.json().idiomas, ['en', 'de']);
  assert.deepEqual([r.json().cambioIdiomas.permitido, r.json().cambioIdiomas.proximoCambio], [false, r.json().periodoFin]);
  assert.equal((await put(['de', 'en'])).statusCode, 200, 'reordenar no es un cambio');
  r = await put(['en', 'it']);
  assert.equal(r.statusCode, 403); assert.match(r.json().error, /Ya cambiaste un idioma en este periodo/);
  assert.equal(r.json().proximoCambio, e.periodoFin);
  // Empieza otro periodo de facturación (renovación por el webhook): vuelve a poder.
  const sub = st.subs.get((await pool.query('SELECT stripe_suscripcion_id FROM suscripciones WHERE usuario_id = $1', [U1])).rows[0].stripe_suscripcion_id);
  const ahoraS = Math.floor(Date.now() / 1000);
  sub.items.data[0].current_period_start = ahoraS + 5; sub.items.data[0].current_period_end = ahoraS + 35 * 86400;
  await enviar(evento('customer.subscription.updated', { ...sub }));
  assert.deepEqual((await estadoDe(U1)).idiomas, ['de', 'en'], 'la renovación conserva los idiomas de la fila, no los de la metadata');
  assert.equal((await put(['en', 'it'])).statusCode, 200);
  // libre: sin límite.
  await ajustes('libre');
  assert.equal((await put(['en', 'ru'])).statusCode, 200); assert.equal((await put(['en', 'ko'])).statusCode, 200);
  // solo_admin: 403 sin fecha; el admin sí puede (respetando el número de idiomas del plan).
  await ajustes('solo_admin');
  r = await put(['en', 'ja']);
  assert.equal(r.statusCode, 403); assert.deepEqual(Object.keys(r.json()).sort(), ['error', 'proximoCambio']); assert.equal(r.json().proximoCambio, null);
  assert.equal((await estadoDe(U1)).cambioIdiomas.permitido, false);
  const antesUlt = (await pool.query('SELECT ultimo_cambio_idiomas FROM suscripciones WHERE usuario_id = $1', [U1])).rows[0].ultimo_cambio_idiomas;
  const adm = (idiomas: unknown) => app.inject({ method: 'PUT', url: `/admin/usuarios/${U1}/suscripcion/idiomas`, headers: admin(), payload: { idiomas } });
  r = await adm(['ja', 'zh']);
  assert.equal(r.statusCode, 200, r.body); assert.deepEqual(r.json().idiomas, ['ja', 'zh']);
  assert.equal((await adm(['ja', 'zh', 'ru'])).statusCode, 400);
  assert.equal((await app.inject({ method: 'PUT', url: `/admin/usuarios/${U1}/suscripcion/idiomas`, headers: tok(U1), payload: { idiomas: ['en'] } })).statusCode, 403);
  assert.deepEqual((await pool.query('SELECT ultimo_cambio_idiomas FROM suscripciones WHERE usuario_id = $1', [U1])).rows[0].ultimo_cambio_idiomas, antesUlt, 'el admin no gasta el cambio del alumno');
  const ev = (await pool.query(`SELECT tipo, datos FROM eventos WHERE usuario_id = $1 AND tipo LIKE 'cambio_idiomas%' ORDER BY id`, [U1])).rows;
  assert.ok(ev.some((x) => x.tipo === 'cambio_idiomas' && x.datos.cambio === true && x.datos.antes.join() === 'en,fr' && x.datos.despues.join() === 'en,de'));
  assert.ok(ev.some((x) => x.tipo === 'cambio_idiomas' && x.datos.cambio === false), 'completar/reordenar también se registra, sin contar');
  assert.equal(ev.filter((x) => x.tipo === 'cambio_idiomas_admin').length, 1);
  assert.equal((await ajustes('otra')).statusCode, 400);
  await ajustes('uno_por_periodo');
  await adm(['en', 'fr']);
});

test('cortesía con idiomas o «todos»; acceso según idioma_meta; regla de 30 días sin periodo', { skip: sinBd }, async () => {
  const U4 = (await pool.query("INSERT INTO usuarios (email, nombre, idioma_meta) VALUES ('dora@pagos.test', 'dora', 'en') RETURNING id")).rows[0].id as string;
  const cort = (payload: object) => app.inject({ method: 'POST', url: `/admin/usuarios/${U4}/cortesia`, headers: admin(), payload });
  const put = (idiomas: string[]) => app.inject({ method: 'PUT', url: '/usuarios/me/suscripcion/idiomas', headers: tok(U4), payload: { idiomas } });
  // Sin cortesía: sin acceso en ningún idioma.
  let e = await estadoDe(U4);
  assert.equal(e.acceso, false); assert.ok(!Object.values(e.accesoPorIdioma).some(Boolean));
  assert.equal((await put(['en'])).statusCode, 409);
  // «todos» en un plan de 2: todos los idiomas, nada que elegir ni cambiar.
  let r = await cort({ planId: 'p2', idiomas: 'todos' });
  assert.equal(r.statusCode, 200, r.body);
  assert.deepEqual([r.json().todosLosIdiomas, r.json().idiomasPorElegir, r.json().acceso, r.json().cambioIdiomas.permitido], [true, 0, true, false]);
  assert.ok(Object.values(r.json().accesoPorIdioma).every(Boolean));
  assert.equal((await put(['en', 'fr'])).statusCode, 400);
  // Lista: el que falta queda «por elegir»; `acceso` = acceso en el idioma meta.
  r = await cort({ planId: 'p2', idiomas: ['fr'] });
  assert.deepEqual([r.json().idiomas, r.json().idiomasPorElegir, r.json().acceso, r.json().accesoPlan, r.json().accesoPorIdioma.fr], [['fr'], 1, false, true, true]);
  await pool.query("UPDATE usuarios SET idioma_meta = 'fr' WHERE id = $1", [U4]);
  assert.equal((await estadoDe(U4)).acceso, true, 'acceso en el idioma meta (fr)');
  // Completar no cuenta; un cambio sí; el siguiente, a los 30 días.
  assert.equal((await put(['fr', 'it'])).statusCode, 200);
  assert.equal((await estadoDe(U4)).cambioIdiomas.permitido, true);
  assert.equal((await put(['de', 'it'])).statusCode, 200);
  r = await put(['de', 'ru']);
  assert.equal(r.statusCode, 403);
  const dias = (new Date(r.json().proximoCambio).getTime() - Date.now()) / 86_400_000;
  assert.ok(dias > 29.9 && dias <= 30, `proximoCambio a 30 días (${dias})`);
  // Validación de la cortesía.
  assert.match((await cort({ planId: 'p2', idiomas: ['fr', 'fr'] })).json().error, /repetido/);
  assert.match((await cort({ planId: 'p2', idiomas: ['fr', 'de', 'it'] })).json().error, /no puedes tener 3/);
  assert.equal((await cort({ planId: 'p2', idiomas: ['zz'] })).statusCode, 400);
  // Sin idiomas: el idioma meta del alumno.
  r = await cort({ planId: 'p1' });
  assert.deepEqual(r.json().idiomas, ['fr']);
  assert.equal((await app.inject({ method: 'DELETE', url: `/admin/usuarios/${U4}/cortesia`, headers: admin() })).statusCode, 200);
  await pool.query('DELETE FROM usuarios WHERE id = $1', [U4]);
});

test('plan de 0 idiomas («Todos los idiomas»): checkout sin selector, confirmar da acceso en los 10', { skip: sinBd }, async () => {
  const c = await app.inject({ method: 'POST', url: '/admin/planes', headers: admin(), payload: {
    id: 'todo', nombre: { es: 'Todos los idiomas', en: 'All languages' }, incluye: { es: ['Todo'], en: ['Everything'] }, idiomas: 0, precio: 60, intervalo: 'mes', orden: 9,
  } });
  assert.equal(c.statusCode, 201, c.body);
  assert.equal((await app.inject({ url: '/planes' })).json().planes.find((p: any) => p.id === 'todo').idiomas, 0);
  assert.equal((await app.inject({ method: 'PUT', url: '/admin/planes/todo', headers: admin(), payload: { idiomas: 11 } })).statusCode, 400);
  const U5 = (await pool.query("INSERT INTO usuarios (email, nombre, idioma_meta) VALUES ('eva@pagos.test', 'eva', 'ko') RETURNING id")).rows[0].id as string;
  const mal = await app.inject({ method: 'POST', url: '/pagos/checkout', headers: tok(U5), payload: { planId: 'todo', idiomas: ['en'] } });
  assert.equal(mal.statusCode, 400); assert.match(mal.json().error, /todos los idiomas/);
  st.llamadas = [];
  const r = await app.inject({ method: 'POST', url: '/pagos/checkout', headers: tok(U5), payload: { planId: 'todo', idiomas: [] } });
  assert.equal(r.statusCode, 200, r.body);
  const d = llamadasA(/^POST \/checkout\/sessions$/)[0].datos;
  assert.equal(d.get('subscription_data[metadata][idiomas]'), null);
  const sesion = [...st.sesiones.values()].at(-1);
  const sub = suscripcionStripe({ precio: st.precios.get((await pool.query("SELECT stripe_precio_id FROM planes WHERE id = 'todo'")).rows[0].stripe_precio_id) });
  sesion.status = 'complete'; sesion.subscription = sub.id;
  const e = (await app.inject({ method: 'POST', url: '/pagos/confirmar', headers: tok(U5), payload: { sessionId: sesion.id } })).json();
  assert.deepEqual([e.planId, e.todosLosIdiomas, e.idiomasPorElegir, e.acceso, e.idiomasPlan], ['todo', true, 0, true, 0]);
  assert.ok(Object.values(e.accesoPorIdioma).every(Boolean));
  assert.equal(e.cambioIdiomas.permitido, false);
  await pool.query('DELETE FROM usuarios WHERE id = $1', [U5]);
  assert.equal((await app.inject({ method: 'DELETE', url: '/admin/planes/todo', headers: admin() })).statusCode, 200);
});

test('tutor: 402 con la prueba agotada y sin plan; modo demo cerrado: sin registro, sin entrada y 403 al tutor', { skip: sinBd }, async () => {
  const ajustes = (demoActivo?: boolean) => app.inject({ method: 'PUT', url: '/admin/pagos/ajustes', headers: admin(), payload: { pruebaMinutos: 60, moneda: 'usd', ...(demoActivo === undefined ? {} : { demoActivo }) } });
  await ajustes(true);
  const U6 = (await pool.query("INSERT INTO usuarios (email, nombre, trial_segundos) VALUES ('dora@pagos.test', 'dora', 3600) RETURNING id")).rows[0].id as string;
  for (const url of ['/chat', '/llamada/token']) {
    const r = await app.inject({ method: 'POST', url, headers: tok(U6), payload: {} });
    assert.equal(r.statusCode, 402, url); assert.equal(r.json().error, 'prueba_agotada');
  }
  await pool.query('UPDATE usuarios SET trial_segundos = 3599 WHERE id = $1', [U6]);
  assert.notEqual((await app.inject({ method: 'POST', url: '/chat', headers: tok(U6), payload: {} })).statusCode, 402);
  // Con cortesía vigente no cuenta la prueba.
  await pool.query('UPDATE usuarios SET trial_segundos = 9000 WHERE id = $1', [U6]);
  await pool.query("INSERT INTO suscripciones (usuario_id, plan_id, origen, estado) VALUES ($1, '', 'cortesia', 'activa')", [U6]);
  assert.notEqual((await app.inject({ method: 'POST', url: '/chat', headers: tok(U6), payload: {} })).statusCode, 402);

  const demo = { email: 'eva@onelingo.demo', nombre: 'Eva' };
  const reg = await app.inject({ method: 'POST', url: '/usuarios/registro', payload: demo });
  assert.equal(reg.statusCode, 201);
  const tDemo = { authorization: `Bearer ${reg.json().token}` };
  assert.notEqual((await app.inject({ method: 'POST', url: '/chat', headers: tDemo, payload: {} })).statusCode, 403);
  assert.equal((await app.inject({ url: '/planes' })).json().demoActivo, true);

  assert.equal((await ajustes(false)).json().demoActivo, false);
  assert.equal((await ajustes()).json().demoActivo, false, 'sin el campo no cambia');
  assert.equal((await app.inject({ url: '/planes' })).json().demoActivo, false);
  assert.equal((await app.inject({ method: 'POST', url: '/usuarios/registro', payload: demo })).statusCode, 403);
  assert.equal((await app.inject({ method: 'POST', url: '/usuarios/login', payload: { email: demo.email } })).statusCode, 403);
  const r = await app.inject({ method: 'POST', url: '/chat', headers: tDemo, payload: {} });
  assert.equal(r.statusCode, 403); assert.equal(r.json().error, 'demo_cerrado');

  // La demo de pruebas con cortesía sin vencimiento sigue entrando tras el lanzamiento.
  await pool.query("INSERT INTO suscripciones (usuario_id, plan_id, origen, estado, todos_idiomas) SELECT id, 'p3', 'cortesia', 'activa', true FROM usuarios WHERE email = $1", [demo.email]);
  assert.equal((await app.inject({ method: 'POST', url: '/usuarios/login', payload: { email: demo.email } })).statusCode, 200);
  assert.notEqual((await app.inject({ method: 'POST', url: '/chat', headers: tDemo, payload: {} })).statusCode, 403);
  assert.equal((await app.inject({ method: 'POST', url: '/usuarios/registro', payload: { ...demo, email: 'otra@onelingo.demo' } })).statusCode, 403, 'una demo nueva sigue cerrada');

  await ajustes(true);
  await pool.query("DELETE FROM usuarios WHERE email IN ('dora@pagos.test', 'eva@onelingo.demo')");
});

const nuevoAlumno = (email: string, meta = 'en') => pool.query('INSERT INTO usuarios (email, nombre, trial_segundos, idioma_meta) VALUES ($1, $2, 600, $3) RETURNING id', [email, email.split('@')[0], meta]).then((r) => r.rows[0].id as string);

test('duraciones: checkout por 3 meses con su Price (cada 3 meses), meses en la suscripción, MRR /3; panel valida y crea Price nuevo al cambiar el importe', { skip: sinBd }, async () => {
  const u = await nuevoAlumno('dora@pagos.test');
  st.llamadas = [];
  assert.equal((await app.inject({ method: 'POST', url: '/pagos/checkout', headers: tok(u), payload: { planId: 'p1', idiomas: ['en'], meses: 5 } })).statusCode, 400);
  const r = await app.inject({ method: 'POST', url: '/pagos/checkout', headers: tok(u), payload: { planId: 'p1', idiomas: ['en'], meses: 3 } });
  assert.equal(r.statusCode, 200, r.body);
  const d = llamadasA(/^POST \/checkout\/sessions$/)[0].datos;
  const precio = st.precios.get(d.get('line_items[0][price]')!);
  assert.deepEqual([precio.unit_amount, precio.recurring.interval, precio.recurring.interval_count], [5500, 'month', 3]);
  assert.equal(d.get('subscription_data[metadata][meses]'), '3');
  const sesion = [...st.sesiones.values()].at(-1);
  sesion.metadata = { usuario_id: u, plan_id: 'p1', idiomas: 'en' };
  sesion.status = 'complete'; sesion.subscription = suscripcionStripe({ precio }).id;
  const c = (await app.inject({ method: 'POST', url: '/pagos/confirmar', headers: tok(u), payload: { sessionId: sesion.id } })).json();
  assert.deepEqual([c.planId, c.meses, c.acceso], ['p1', 3, true]);
  assert.equal(Sus.calcularMrr([{ origen: 'stripe', estado: 'activa', importe_centavos: 5500, intervalo: 'mes', meses: 3, moneda: 'usd' }]).mrr, 18.33);
  // Panel: un plan anual no lleva duraciones; meses repetidos, 400.
  assert.equal((await app.inject({ method: 'PUT', url: '/admin/planes/p1', headers: admin(), payload: { intervalo: 'anio', duraciones: [{ meses: 3, precio: 50 }] } })).statusCode, 400);
  assert.equal((await app.inject({ method: 'PUT', url: '/admin/planes/p1', headers: admin(), payload: { duraciones: [{ meses: 3, precio: 50 }, { meses: 3, precio: 52 }] } })).statusCode, 400);
  // Cambiar el de 3 meses: Price nuevo, el anterior se archiva; los de 6 y 12 se conservan.
  const antes = (await pool.query("SELECT precio_id, meses FROM planes_precios WHERE plan_id = 'p1' AND meses > 1 AND archivado_en IS NULL ORDER BY meses")).rows;
  const e = await app.inject({ method: 'PUT', url: '/admin/planes/p1', headers: admin(), payload: { duraciones: [{ meses: 3, precio: 54 }, { meses: 6, precio: 110 }, { meses: 12, precio: 220 }] } });
  assert.equal(e.statusCode, 200, e.body); assert.equal(e.json().sync.ok, true);
  const despues = (await pool.query("SELECT precio_id, meses FROM planes_precios WHERE plan_id = 'p1' AND meses > 1 AND archivado_en IS NULL ORDER BY meses")).rows;
  assert.notEqual(despues[0].precio_id, antes[0].precio_id);
  assert.deepEqual(despues.slice(1), antes.slice(1));
  assert.equal(st.precios.get(antes[0].precio_id).active, false);
  // El webhook encuentra el plan por el Price archivado de 3 meses.
  assert.equal(await Sus.planDeStripe({ stripe_precio_id: antes[0].precio_id, precioPlan: null, productoId: null, suscripcionPlan: null }), 'p1');
  await app.inject({ method: 'PUT', url: '/admin/planes/p1', headers: admin(), payload: { duraciones: [{ meses: 3, precio: 55 }, { meses: 6, precio: 110 }, { meses: 12, precio: 220 }] } });
});

test('plan familiar: el titular añade por correo (con cuenta: acceso al momento; sin cuenta: al entrar), hasta 3; quitar, salir y fin del titular', { skip: sinBd }, async () => {
  const titular = await nuevoAlumno('fam.titular@pagos.test');
  const hijo = await nuevoAlumno('fam.hijo@pagos.test', 'fr');
  const propia = await nuevoAlumno('fam.propia@pagos.test');
  const fam = (u: string) => app.inject({ url: '/usuarios/me/familia', headers: tok(u) }).then((r) => r.json());
  const invitar = (email: string) => app.inject({ method: 'POST', url: '/usuarios/me/familia', headers: tok(titular), payload: { email } });
  assert.equal((await invitar('fam.hijo@pagos.test')).statusCode, 409, 'sin plan familiar');
  assert.equal((await app.inject({ method: 'POST', url: `/admin/usuarios/${titular}/cortesia`, headers: admin(), payload: { planId: 'familiar' } })).statusCode, 200);
  assert.deepEqual([(await fam(titular)).rol, (await fam(titular)).plazas], ['titular', 3]);
  assert.equal((await invitar('FAM.titular@pagos.test')).statusCode, 400, 'su propio correo');
  // Con cuenta: acceso inmediato, con su idioma meta y su propio progreso.
  const a = await invitar(' Fam.Hijo@pagos.test ');
  assert.equal(a.statusCode, 200, a.body);
  assert.deepEqual(a.json().miembros.map((m: any) => [m.email, m.estado]), [['fam.hijo@pagos.test', 'activo']]);
  const sh = await estadoDe(hijo);
  assert.deepEqual([sh.planId, sh.origen, sh.familiar, sh.accesoPlan, sh.idiomas, sh.puedeGestionar, sh.usuariosPlan], ['familiar', 'familia', true, true, ['fr'], false, 4]);
  assert.deepEqual([(await fam(hijo)).rol, (await fam(hijo)).titular.email], ['miembro', 'fam.titular@pagos.test']);
  assert.equal((await pool.query('SELECT plan_id FROM usuarios WHERE id = $1', [hijo])).rows[0].plan_id, 'familiar');
  // Quien ya paga lo suyo no entra; un correo en otra familia tampoco.
  await app.inject({ method: 'POST', url: `/admin/usuarios/${propia}/cortesia`, headers: admin(), payload: { planId: 'p2' } });
  assert.match((await invitar('fam.propia@pagos.test')).json().error, /ya tiene su propio plan/);
  assert.equal((await invitar('fam.hijo@pagos.test')).statusCode, 409);
  // Sin cuenta: queda pendiente y se activa cuando entra con ese correo.
  assert.equal((await invitar('fam.nueva@pagos.test')).json().miembros[1].estado, 'pendiente');
  assert.ok((await pool.query("SELECT 1 FROM correos WHERE para = 'fam.nueva@pagos.test'")).rowCount, 'invitación por correo');
  const nueva = await nuevoAlumno('fam.nueva@pagos.test', 'de');
  const sn = await estadoDe(nueva);
  assert.deepEqual([sn.planId, sn.origen, sn.idiomas], ['familiar', 'familia', ['de']]);
  // Hasta 3 personas además del titular.
  assert.equal((await invitar('fam.tres@pagos.test')).statusCode, 200);
  assert.match((await invitar('fam.cuatro@pagos.test')).json().error, /ya tiene a 3 personas/);
  // Quitar a uno: pierde el acceso. Salir: también.
  const q = await app.inject({ method: 'POST', url: '/usuarios/me/familia/quitar', headers: tok(titular), payload: { email: 'fam.nueva@pagos.test' } });
  assert.equal(q.json().miembros.length, 2);
  assert.equal((await estadoDe(nueva)).accesoPlan, false);
  assert.equal((await app.inject({ method: 'POST', url: '/usuarios/me/familia/salir', headers: tok(nueva) })).statusCode, 404);
  // El titular pierde su plan: los miembros también; al recuperarlo, vuelven.
  await app.inject({ method: 'DELETE', url: `/admin/usuarios/${titular}/cortesia`, headers: admin() });
  assert.equal((await estadoDe(hijo)).accesoPlan, false);
  await app.inject({ method: 'POST', url: `/admin/usuarios/${titular}/cortesia`, headers: admin(), payload: { planId: 'familiar' } });
  assert.equal((await estadoDe(hijo)).accesoPlan, true);
  // Cambia a un plan de una persona: los miembros quedan sin plan.
  await app.inject({ method: 'POST', url: `/admin/usuarios/${titular}/cortesia`, headers: admin(), payload: { planId: 'p1' } });
  assert.equal((await estadoDe(hijo)).accesoPlan, false);
  assert.equal((await fam(titular)).rol, null);
  await app.inject({ method: 'POST', url: `/admin/usuarios/${titular}/cortesia`, headers: admin(), payload: { planId: 'familiar' } });
  const s = await app.inject({ method: 'POST', url: '/usuarios/me/familia/salir', headers: tok(hijo) });
  assert.equal(s.statusCode, 200); assert.equal(s.json().rol, null);
  assert.equal((await estadoDe(hijo)).accesoPlan, false);
  // Panel: filtro «familia».
  const p = (await app.inject({ url: '/admin/suscripciones?estado=familia', headers: admin() })).json();
  assert.ok(p.filas.every((f: any) => f.origen === 'familia'));
});

test('cotizaciones del plan Empresarial: con o sin sesión, validación, panel y límite por IP', { skip: sinBd }, async () => {
  const datos = { empresa: 'Acme', empleados: 50, idiomas: ['en', 'fr'], mensaje: 'Para el equipo de ventas', email: 'rrhh@acme.test', nombre: 'Lía' };
  const ip = { 'x-forwarded-for': '203.0.113.7' };
  const r = await app.inject({ method: 'POST', url: '/cotizaciones', headers: ip, payload: datos });
  assert.equal(r.statusCode, 201, r.body);
  assert.equal((await app.inject({ method: 'POST', url: '/cotizaciones', headers: ip, payload: { ...datos, idiomas: [] } })).statusCode, 400);
  assert.equal((await app.inject({ method: 'POST', url: '/cotizaciones', headers: { ...ip, ...tok(U2) }, payload: { ...datos, empresa: 'Beta' } })).statusCode, 201);
  const l = (await app.inject({ url: '/admin/cotizaciones', headers: admin() })).json();
  assert.equal(l.nuevas, 2);
  assert.deepEqual(l.cotizaciones.map((c: any) => [c.empresa, c.usuarioId]), [['Beta', U2], ['Acme', null]]);
  assert.equal((await app.inject({ url: '/admin/cotizaciones' })).statusCode, 401);
  assert.equal((await app.inject({ method: 'PUT', url: `/admin/cotizaciones/${r.json().id}`, headers: admin(), payload: { estado: 'contactada', nota: 'Propuesta enviada' } })).statusCode, 200);
  assert.equal((await app.inject({ url: '/admin/cotizaciones?estado=contactada', headers: admin() })).json().cotizaciones[0].nota, 'Propuesta enviada');
  for (let i = 0; i < 3; i++) await app.inject({ method: 'POST', url: '/cotizaciones', headers: ip, payload: datos });
  assert.equal((await app.inject({ method: 'POST', url: '/cotizaciones', headers: ip, payload: datos })).statusCode, 429);
});
