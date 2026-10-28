/**
 * Google Play Billing: suscripciones compradas dentro de la app Android
 * (`suscripciones.origen = 'google'`). La app compra con la Billing Library y
 * envía el token de compra a `POST /pagos/google/verificar`; las renovaciones,
 * cancelaciones y reembolsos llegan como notificaciones RTDN (Pub/Sub push a
 * `POST /pagos/google/rtdn`). En ambos casos el servidor consulta la compra en
 * la API Google Play Developer (purchases.subscriptionsv2) con una cuenta de
 * servicio: nunca se fía de lo que manda la app ni de la notificación.
 *
 * Convención de ids en Play Console (docs/PANEL_ADMIN.md → «Google Play»):
 * producto `plan_<id del plan>` y un plan base por duración: `mes-1`, `mes-3`, `mes-6`, `mes-12`.
 *
 * Variables del servidor (.env):
 * - GOOGLE_PLAY_CUENTA_SERVICIO: ruta al JSON de la cuenta de servicio (o el JSON en una línea).
 * - GOOGLE_PLAY_PAQUETE: nombre del paquete (por defecto com.torisoftt.onelingo).
 * - GOOGLE_PLAY_RTDN_TOKEN: secreto de la URL de las notificaciones (`?token=`).
 */
import { createSign, timingSafeEqual } from 'node:crypto';
import { readFileSync } from 'node:fs';
import type { ModoPago } from './stripe.js';

export type CuentaServicio = { client_email: string; private_key: string; token_uri?: string };
export class ErrorGoogle extends Error { constructor(m: string, public status: number) { super(m); } }

const API = 'https://androidpublisher.googleapis.com/androidpublisher/v3';
const ALCANCE = 'https://www.googleapis.com/auth/androidpublisher';
const TIMEOUT_MS = 10_000;

let leida: { crudo: string; cuenta: CuentaServicio | null; error: string | null } | null = null;
/** Cuenta de servicio de GOOGLE_PLAY_CUENTA_SERVICIO (ruta o JSON), leída una vez por valor. */
function cuentaServicio(): { cuenta: CuentaServicio | null; error: string | null } {
  const crudo = (process.env.GOOGLE_PLAY_CUENTA_SERVICIO ?? '').trim();
  if (leida?.crudo === crudo) return leida;
  let cuenta: CuentaServicio | null = null, error: string | null = null;
  if (crudo) {
    try {
      const j = JSON.parse(crudo.startsWith('{') ? crudo : readFileSync(crudo, 'utf8'));
      if (typeof j?.client_email === 'string' && typeof j?.private_key === 'string') cuenta = { client_email: j.client_email, private_key: j.private_key, token_uri: j.token_uri };
      else error = 'El JSON no es de una cuenta de servicio (faltan client_email o private_key).';
    } catch (e: any) { error = `No se pudo leer la cuenta de servicio: ${String(e?.message ?? e).slice(0, 200)}`; }
  }
  leida = { crudo, cuenta, error };
  return leida;
}

/** Configuración en uso (solo para el servidor: la cuenta de servicio nunca sale de aquí). */
export function googleConfig() {
  const { cuenta, error } = cuentaServicio();
  return { paquete: (process.env.GOOGLE_PLAY_PAQUETE || 'com.torisoftt.onelingo').trim(), cuenta, error, tokenRtdn: process.env.GOOGLE_PLAY_RTDN_TOKEN ?? '' };
}
export const googleDisponible = () => !!googleConfig().cuenta;

/** ¿El `?token=` de una notificación es el configurado? (comparación en tiempo constante). */
export function tokenRtdnValido(recibido: string) {
  const esperado = googleConfig().tokenRtdn;
  if (!esperado || !recibido) return false;
  const a = Buffer.from(recibido), b = Buffer.from(esperado);
  return a.length === b.length && timingSafeEqual(a, b);
}

// ── OAuth 2.0 de cuenta de servicio (JWT firmado RS256, sin SDK) ─────────────
let acceso: { email: string; token: string; vence: number } | null = null;
async function tokenAcceso(c: CuentaServicio): Promise<string> {
  if (acceso && acceso.email === c.client_email && acceso.vence > Date.now() + 60_000) return acceso.token;
  const ahora = Math.floor(Date.now() / 1000);
  const aud = c.token_uri || 'https://oauth2.googleapis.com/token';
  const b64 = (o: unknown) => Buffer.from(JSON.stringify(o)).toString('base64url');
  const cuerpo = `${b64({ alg: 'RS256', typ: 'JWT' })}.${b64({ iss: c.client_email, scope: ALCANCE, aud, iat: ahora, exp: ahora + 3600 })}`;
  const firma = createSign('RSA-SHA256').update(cuerpo).sign(c.private_key, 'base64url');
  const r = await fetch(aud, {
    method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion: `${cuerpo}.${firma}` }),
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  const j: any = await r.json().catch(() => null);
  if (!r.ok || typeof j?.access_token !== 'string') throw new ErrorGoogle(`La cuenta de servicio no obtuvo acceso: ${j?.error_description ?? j?.error ?? r.status}`, 502);
  acceso = { email: c.client_email, token: j.access_token, vence: Date.now() + Number(j.expires_in ?? 3600) * 1000 };
  return acceso.token;
}

/** Llamada a la API Google Play Developer sobre el paquete configurado (`ruta` empieza con `/`). */
export async function llamarGoogle(metodo: 'GET' | 'POST', ruta: string, cuerpo?: unknown): Promise<any> {
  const c = googleConfig();
  if (!c.cuenta) throw new ErrorGoogle(c.error ?? 'Google Play no está configurado.', 503);
  const r = await fetch(`${API}/applications/${encodeURIComponent(c.paquete)}${ruta}`, {
    method: metodo,
    headers: { authorization: `Bearer ${await tokenAcceso(c.cuenta)}`, ...(cuerpo !== undefined ? { 'content-type': 'application/json' } : {}) },
    body: cuerpo !== undefined ? JSON.stringify(cuerpo) : undefined,
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  const texto = await r.text().catch(() => '');
  let j: any = null; try { j = texto ? JSON.parse(texto) : {}; } catch { /* no es JSON */ }
  if (!r.ok) throw new ErrorGoogle(String(j?.error?.message ?? `Google Play respondió ${r.status}`).slice(0, 300), r.status);
  return j ?? {};
}

export const obtenerCompra = (token: string) => llamarGoogle('GET', `/purchases/subscriptionsv2/tokens/${encodeURIComponent(token)}`);
/** Hay 3 días para reconocer una compra; si no, Google la reembolsa. */
export const reconocerCompra = (producto: string, token: string) =>
  llamarGoogle('POST', `/purchases/subscriptions/${encodeURIComponent(producto)}/tokens/${encodeURIComponent(token)}:acknowledge`, {});

// ── Convención de ids (puras) ────────────────────────────────────────────────
/** Producto de Play Console de un plan: `plan_p1`, `plan_familiar`. */
export const productoDePlan = (planId: string) => `plan_${planId.toLowerCase().replace(/[^a-z0-9_.]/g, '_')}`;
/** Plan base de una duración: `mes-1`, `mes-3`… */
export const planBaseDeMeses = (meses: number) => `mes-${meses}`;
export function mesesDePlanBase(id: unknown): number | null {
  const m = /^mes-(\d{1,2})$/.exec(String(id ?? ''));
  return m && Number(m[1]) >= 1 ? Number(m[1]) : null;
}

/** Estado de Google → estado de OneLingo. En el periodo de gracia sigue el acceso. */
export function estadoDesdeGoogle(s: string): 'activa' | 'impago' | 'cancelada' | 'vencida' {
  switch (s) {
    case 'SUBSCRIPTION_STATE_ACTIVE': case 'SUBSCRIPTION_STATE_IN_GRACE_PERIOD': return 'activa';
    case 'SUBSCRIPTION_STATE_CANCELED': return 'cancelada';
    case 'SUBSCRIPTION_STATE_ON_HOLD': case 'SUBSCRIPTION_STATE_PENDING': return 'impago';
    default: return 'vencida'; // EXPIRED, PAUSED, PENDING_PURCHASE_CANCELED
  }
}

const restarMeses = (d: Date, n: number) => { const r = new Date(d); r.setUTCMonth(r.getUTCMonth() - n); return r; };

/** Datos de una compra (`SubscriptionPurchaseV2`) para la fila de `suscripciones`. */
export function datosDeGoogle(v: any) {
  const item = v?.lineItems?.[0] ?? {};
  const estado = estadoDesdeGoogle(String(v?.subscriptionState ?? ''));
  const fin = item.expiryTime ? new Date(item.expiryTime) : null;
  const planBase = typeof item.offerDetails?.basePlanId === 'string' ? item.offerDetails.basePlanId : null;
  const meses = mesesDePlanBase(planBase);
  const precio = item.autoRenewingPlan?.recurringPrice;
  return {
    estado,
    cancela_al_final: estado === 'activa' && item.autoRenewingPlan?.autoRenewEnabled === false,
    periodo_fin: fin && !Number.isNaN(fin.getTime()) ? fin : null,
    // La API no da el inicio del periodo actual: el fin menos la duración del plan base.
    periodo_inicio: estado === 'activa' && fin && meses ? restarMeses(fin, meses) : null,
    google_producto: typeof item.productId === 'string' ? item.productId : null,
    google_plan_base: planBase,
    google_pedido: typeof v?.latestOrderId === 'string' ? v.latestOrderId : null,
    importe_centavos: precio ? Math.round(Number(precio.units ?? 0) * 100 + Number(precio.nanos ?? 0) / 1e7) : null,
    moneda: typeof precio?.currencyCode === 'string' ? precio.currencyCode.toLowerCase() : null,
    meses,
    intervalo: meses === 12 ? 'anio' as const : 'mes' as const,
    modo: (v?.testPurchase ? 'test' : 'live') as ModoPago,
    usuarioPista: (v?.externalAccountIdentifiers?.obfuscatedExternalAccountId || null) as string | null,
    tokenAnterior: (v?.linkedPurchaseToken || null) as string | null,
    reconocida: v?.acknowledgementState === 'ACKNOWLEDGEMENT_STATE_ACKNOWLEDGED',
  };
}

/**
 * Cuerpo de una notificación RTDN (push de Pub/Sub: `message.data` en base64).
 * Devuelve el token de la compra afectada o `null` (prueba, otro paquete, producto único…).
 */
export function tokenDeRtdn(cuerpo: any, paquete: string): { token: string | null; motivo?: string } {
  const data = cuerpo?.message?.data;
  if (typeof data !== 'string') return { token: null, motivo: 'sin message.data' };
  let n: any;
  try { n = JSON.parse(Buffer.from(data, 'base64').toString('utf8')); } catch { return { token: null, motivo: 'data no es JSON' }; }
  if (n?.packageName !== paquete) return { token: null, motivo: 'otro paquete' };
  if (n?.testNotification) return { token: null, motivo: 'notificación de prueba' };
  const token = n?.subscriptionNotification?.purchaseToken ?? (n?.voidedPurchaseNotification?.productType === 1 ? n.voidedPurchaseNotification.purchaseToken : null);
  return typeof token === 'string' && token ? { token } : { token: null, motivo: 'no es de una suscripción' };
}
