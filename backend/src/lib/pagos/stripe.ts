/**
 * Cliente REST mínimo de Stripe (sin SDK: el servidor despliega archivo por
 * archivo, sin `npm install`) y verificación de la firma del webhook.
 *
 * - Peticiones a https://api.stripe.com/v1 con `Authorization: Bearer <clave>`
 *   y cuerpos `application/x-www-form-urlencoded` anidados
 *   (`line_items[0][price]=…`), como hacen los SDK oficiales.
 * - Firma del webhook: cabecera `Stripe-Signature: t=<unix>,v1=<hex>[,v1=…]`;
 *   v1 = HMAC-SHA256(secreto, `${t}.${cuerpoCrudo}`). Tolerancia 5 min.
 *   Fuente: docs.stripe.com/webhooks#verify-manually.
 *
 * Nunca se registra ni se devuelve una clave completa.
 */
import { createHmac, timingSafeEqual } from 'node:crypto';

export const API_STRIPE = 'https://api.stripe.com/v1';
export const TOLERANCIA_FIRMA_S = 300;
export type ModoPago = 'test' | 'live';

/** Eventos que escucha el webhook (contrato, punto 6). */
export const EVENTOS_WEBHOOK = [
  'checkout.session.completed',
  'customer.subscription.created',
  'customer.subscription.updated',
  'customer.subscription.deleted',
  'invoice.paid',
  'invoice.payment_failed',
] as const;

// ── Codificación form anidada ────────────────────────────────────────────────
/**
 * `{ a: { b: [ { c: 1 } ] }, d: true }` → `a[b][0][c]=1&d=true`.
 * `undefined` y `null` se omiten; una cadena vacía se envía (Stripe la usa para borrar).
 */
export function codificarForm(datos: Record<string, unknown>): string {
  const pares: string[] = [];
  const recorrer = (clave: string, v: unknown) => {
    if (v === undefined || v === null) return;
    if (Array.isArray(v)) { v.forEach((x, i) => recorrer(`${clave}[${i}]`, x)); return; }
    if (v instanceof Date) { pares.push(`${encodeURIComponent(clave)}=${Math.floor(v.getTime() / 1000)}`); return; }
    if (typeof v === 'object') { for (const [k, x] of Object.entries(v as Record<string, unknown>)) recorrer(`${clave}[${k}]`, x); return; }
    pares.push(`${encodeURIComponent(clave)}=${encodeURIComponent(String(v))}`);
  };
  for (const [k, v] of Object.entries(datos)) recorrer(k, v);
  return pares.join('&');
}

// ── Claves ───────────────────────────────────────────────────────────────────
/** Modo de una clave secreta o restringida (`sk_test_`, `rk_live_`…). */
export function modoDeClave(clave: string): ModoPago | null {
  const m = /^(?:sk|rk)_(test|live)_/.exec(clave);
  return m ? (m[1] as ModoPago) : null;
}
export const esRestringida = (clave: string) => /^rk_/.test(clave);

// ── Llamadas ─────────────────────────────────────────────────────────────────
export class ErrorStripe extends Error {
  constructor(mensaje: string, public status: number, public tipo: string | null = null, public codigo: string | null = null) { super(mensaje); }
}

/** Quita de un texto cualquier aparición de la clave (por si el proveedor la repite). */
function sinClave(texto: string, clave: string) {
  return clave && clave.length >= 8 ? texto.split(clave).join(clave.slice(0, 8) + '…' + clave.slice(-4)) : texto;
}

export type OpcionesStripe = { timeoutMs?: number; idempotencia?: string };

/**
 * Llama a la API de Stripe. GET/DELETE llevan los datos en la query; POST, en
 * el cuerpo form. Lanza `ErrorStripe` con el mensaje de Stripe si no es 2xx.
 */
export async function llamarStripe<T = any>(clave: string, metodo: 'GET' | 'POST' | 'DELETE', ruta: string, datos: Record<string, unknown> = {}, op: OpcionesStripe = {}): Promise<T> {
  const form = codificarForm(datos);
  const url = API_STRIPE + ruta + (metodo !== 'POST' && form ? (ruta.includes('?') ? '&' : '?') + form : '');
  const headers: Record<string, string> = { authorization: `Bearer ${clave}` };
  if (metodo === 'POST') headers['content-type'] = 'application/x-www-form-urlencoded';
  if (op.idempotencia) headers['idempotency-key'] = op.idempotencia;
  let r: Response;
  try {
    r = await fetch(url, { method: metodo, headers, body: metodo === 'POST' ? form : undefined, signal: AbortSignal.timeout(op.timeoutMs ?? 15_000) });
  } catch (e: any) {
    const t = e?.name === 'TimeoutError' || e?.name === 'AbortError';
    throw new ErrorStripe(t ? 'Stripe no respondió a tiempo.' : `No se pudo conectar con Stripe: ${String(e?.message ?? e).slice(0, 200)}`, 0, 'red');
  }
  const texto = await r.text().catch(() => '');
  let j: any = null; try { j = JSON.parse(texto); } catch { /* no es JSON */ }
  if (!r.ok) {
    // Stripe enmascara la clave con asteriscos («sk_test_*****abcd»): se acortan para que quepa en el panel.
    const m = sinClave(String(j?.error?.message ?? texto.slice(0, 200) ?? ''), clave).replace(/\*{4,}/g, '…').replace(/\s+/g, ' ').trim().slice(0, 400);
    throw new ErrorStripe(m || `Stripe respondió ${r.status}`, r.status, j?.error?.type ?? null, j?.error?.code ?? null);
  }
  return j as T;
}

// ── Firma del webhook ────────────────────────────────────────────────────────
export type ResultadoFirma = { ok: true; t: number } | { ok: false; motivo: 'sin_cabecera' | 'formato' | 'caducada' | 'firma' };

const hmac = (secreto: string, t: number | string, cuerpo: string | Buffer) =>
  createHmac('sha256', secreto).update(`${t}.`).update(cuerpo).digest('hex');

/** Verifica `Stripe-Signature` contra el cuerpo CRUDO (Buffer o texto exacto). */
export function verificarFirma(cuerpo: string | Buffer, cabecera: string | undefined, secreto: string, ahoraS = Math.floor(Date.now() / 1000), toleranciaS = TOLERANCIA_FIRMA_S): ResultadoFirma {
  if (!cabecera) return { ok: false, motivo: 'sin_cabecera' };
  let t: number | null = null;
  const firmas: string[] = [];
  for (const parte of cabecera.split(',')) {
    const i = parte.indexOf('=');
    if (i < 0) continue;
    const k = parte.slice(0, i).trim(), v = parte.slice(i + 1).trim();
    if (k === 't' && /^\d+$/.test(v)) t = Number(v);
    else if (k === 'v1') firmas.push(v);
  }
  if (t === null || !firmas.length) return { ok: false, motivo: 'formato' };
  const esperada = Buffer.from(hmac(secreto, t, cuerpo), 'utf8');
  const valida = firmas.some((f) => { const b = Buffer.from(f, 'utf8'); return b.length === esperada.length && timingSafeEqual(b, esperada); });
  if (!valida) return { ok: false, motivo: 'firma' };
  if (Math.abs(ahoraS - t) > toleranciaS) return { ok: false, motivo: 'caducada' };
  return { ok: true, t };
}

/** Cabecera `Stripe-Signature` para un cuerpo (pruebas y simulaciones locales). */
export function firmarEvento(cuerpo: string | Buffer, secreto: string, t = Math.floor(Date.now() / 1000)) {
  return `t=${t},v1=${hmac(secreto, t, cuerpo)}`;
}

// ── Configuración de la cuenta al vincular ───────────────────────────────────
export type WebhookActual = { id?: string; secreto?: string };

/**
 * Crea o actualiza el webhook endpoint de OneLingo en `url`.
 * - Si el guardado (`actual.id`) existe con esa URL y conocemos su secreto, se
 *   actualiza (eventos) y se reutiliza.
 * - Si existe uno con esa URL pero no conocemos su secreto (Stripe solo lo da
 *   al crearlo), se borra y se crea de nuevo.
 */
export async function configurarWebhook(clave: string, url: string, actual: WebhookActual, op: OpcionesStripe = {}): Promise<{ id: string; secreto: string; accion: 'reutilizado' | 'creado' | 'recreado' }> {
  const lista = await llamarStripe<{ data: any[] }>(clave, 'GET', '/webhook_endpoints', { limit: 100 }, op);
  const conUrl = (lista?.data ?? []).filter((w) => w?.url === url);
  const nuestro = conUrl.find((w) => w.id === actual.id);
  if (nuestro && actual.secreto) {
    await llamarStripe(clave, 'POST', `/webhook_endpoints/${nuestro.id}`, { enabled_events: [...EVENTOS_WEBHOOK], disabled: false }, op);
    return { id: nuestro.id, secreto: actual.secreto, accion: 'reutilizado' };
  }
  for (const w of conUrl) await llamarStripe(clave, 'DELETE', `/webhook_endpoints/${w.id}`, {}, op);
  // El nuestro anterior en otra URL (cambió la URL de la app): se borra para no dejarlo huérfano.
  const viejo = actual.id ? (lista?.data ?? []).find((w) => w.id === actual.id && w.url !== url) : null;
  if (viejo) await llamarStripe(clave, 'DELETE', `/webhook_endpoints/${viejo.id}`, {}, op).catch(() => {});
  const nuevo = await llamarStripe<{ id: string; secret: string }>(clave, 'POST', '/webhook_endpoints', {
    url, enabled_events: [...EVENTOS_WEBHOOK], description: 'OneLingo: planes y suscripciones', metadata: { origen: 'onelingo' },
  }, op);
  if (!nuevo?.id || !nuevo?.secret) throw new ErrorStripe('Stripe no devolvió el secreto del webhook.', 500);
  return { id: nuevo.id, secreto: nuevo.secret, accion: conUrl.length ? 'recreado' : 'creado' };
}

// ── Customer Portal ──────────────────────────────────────────────────────────
/** Máximo de productos con cambio de plan en una configuración del portal (docs de Stripe). */
export const MAX_PRODUCTOS_PORTAL = 10;
/** Producto con su Price mensual y, si tiene, los de sus duraciones (`precios`). */
export type ProductoPortal = { producto: string; precio: string; precios?: string[] };

/**
 * Cuerpo de la configuración del Customer Portal de OneLingo. Parámetros
 * comprobados en docs.stripe.com/api/customer_portal/configurations/create y
 * /update (`features.subscription_update.{enabled, default_allowed_updates,
 * proration_behavior, products[].product, products[].prices}`; hasta 10 productos).
 * Cambio de plan: entre los Price actuales de los planes visibles y sincronizados,
 * con prorrateo. Sin planes, el cambio de plan se desactiva.
 */
export function cuerpoPortal(urlRetorno: string, productos: ProductoPortal[]) {
  const lista = productos.slice(0, MAX_PRODUCTOS_PORTAL);
  return {
    business_profile: { headline: 'OneLingo: gestiona tu suscripción' },
    default_return_url: urlRetorno,
    features: {
      customer_update: { enabled: true, allowed_updates: ['email', 'address'] },
      invoice_history: { enabled: true },
      payment_method_update: { enabled: true },
      subscription_cancel: { enabled: true, mode: 'at_period_end' },
      subscription_update: lista.length
        ? { enabled: true, default_allowed_updates: ['price'], proration_behavior: 'create_prorations', products: lista.map((p) => ({ product: p.producto, prices: p.precios?.length ? p.precios : [p.precio] })) }
        : { enabled: false },
    },
    metadata: { origen: 'onelingo' },
  };
}

/**
 * Crea o actualiza la configuración del portal de OneLingo (no toca la
 * configuración por defecto de la cuenta: la sesión del portal la pide por id).
 * Orden: la guardada (`actualId`) → una activa con `metadata.origen=onelingo` → nueva.
 */
export async function configurarPortal(clave: string, d: { urlRetorno: string; productos: ProductoPortal[]; actualId?: string | null }, op: OpcionesStripe = {}): Promise<{ id: string; accion: 'actualizada' | 'creada'; productos: number; omitidos: number }> {
  const cuerpo = cuerpoPortal(d.urlRetorno, d.productos);
  const n = Math.min(d.productos.length, MAX_PRODUCTOS_PORTAL), omitidos = d.productos.length - n;
  const actualizar = async (id: string) => {
    const r = await llamarStripe<{ id: string }>(clave, 'POST', `/billing_portal/configurations/${encodeURIComponent(id)}`, cuerpo, op);
    return { id: r?.id ?? id, accion: 'actualizada' as const, productos: n, omitidos };
  };
  if (d.actualId) {
    try { return await actualizar(d.actualId); } catch (e) { if (!(e instanceof ErrorStripe && e.status === 404)) throw e; }
  }
  const l = await llamarStripe<{ data: any[] }>(clave, 'GET', '/billing_portal/configurations', { active: true, limit: 100 }, op);
  const nuestra = (l?.data ?? []).find((c) => c?.metadata?.origen === 'onelingo' && c?.active !== false && c?.id !== d.actualId);
  if (nuestra) return actualizar(nuestra.id);
  const c = await llamarStripe<{ id: string }>(clave, 'POST', '/billing_portal/configurations', cuerpo, op);
  if (!c?.id) throw new ErrorStripe('Stripe no devolvió la configuración del portal.', 500);
  return { id: c.id, accion: 'creada', productos: n, omitidos };
}
