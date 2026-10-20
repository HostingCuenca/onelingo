/**
 * Eventos del webhook de Stripe: idempotentes por id de evento (tabla
 * `pagos_eventos`). Un evento ya procesado se responde 200 sin repetir nada;
 * uno que falló se reintenta cuando Stripe lo reenvía.
 */
import { query, uno } from '../db.js';
import { stripe } from './proveedor.js';
import { marcarImpago, sincronizarDesdeStripe } from './suscripciones.js';

/** Id de la suscripción de una factura (API anterior: `subscription`; desde 2025-03-31: `parent.subscription_details`). */
export function suscripcionDeFactura(inv: any): string | null {
  const s = inv?.subscription ?? inv?.parent?.subscription_details?.subscription ?? null;
  return typeof s === 'string' ? s : s?.id ?? null;
}

/** Aplica un evento ya verificado. Devuelve un resumen (sin datos personales). */
export async function aplicarEvento(ev: any): Promise<Record<string, unknown>> {
  const o = ev?.data?.object ?? {};
  switch (ev?.type) {
    case 'checkout.session.completed': {
      if (o.mode !== 'subscription' || !o.subscription) return { ignorado: 'no es una suscripción' };
      const sub = typeof o.subscription === 'string' ? await stripe.obtenerSuscripcion(o.subscription) : o.subscription;
      return sincronizarDesdeStripe(sub, { usuarioId: o.client_reference_id ?? o.metadata?.usuario_id ?? null, idiomas: o.metadata?.idiomas });
    }
    case 'customer.subscription.created':
    case 'customer.subscription.updated':
    case 'customer.subscription.deleted':
      return sincronizarDesdeStripe(o);
    case 'invoice.paid': {
      const id = suscripcionDeFactura(o);
      if (!id) return { ignorado: 'factura sin suscripción' };
      return sincronizarDesdeStripe(await stripe.obtenerSuscripcion(id));
    }
    case 'invoice.payment_failed': {
      const id = suscripcionDeFactura(o);
      if (!id) return { ignorado: 'factura sin suscripción' };
      return { impago: await marcarImpago(id) };
    }
    default:
      return { ignorado: 'tipo no usado' };
  }
}

export async function procesarWebhook(ev: any): Promise<{ status: number; cuerpo: Record<string, unknown> }> {
  if (typeof ev?.id !== 'string' || typeof ev?.type !== 'string') return { status: 400, cuerpo: { error: 'Evento sin id o tipo' } };
  const nuevo = await uno('INSERT INTO pagos_eventos (id, tipo) VALUES ($1, $2) ON CONFLICT (id) DO NOTHING RETURNING id', [ev.id, ev.type]);
  if (!nuevo) {
    const prev = await uno<{ procesado: boolean }>('SELECT procesado FROM pagos_eventos WHERE id = $1', [ev.id]);
    if (prev?.procesado) return { status: 200, cuerpo: { recibido: true, repetido: true } };
  }
  // Un evento del otro modo (test ↔ live) no corresponde a esta configuración.
  const modo = stripe.modo();
  if (modo && typeof ev.livemode === 'boolean' && ev.livemode !== (modo === 'live')) {
    await query('UPDATE pagos_eventos SET procesado = true, error = $2 WHERE id = $1', [ev.id, 'ignorado: otro modo']);
    return { status: 200, cuerpo: { recibido: true, ignorado: 'otro modo' } };
  }
  try {
    const r = await aplicarEvento(ev);
    await query('UPDATE pagos_eventos SET procesado = true, error = NULL WHERE id = $1', [ev.id]);
    return { status: 200, cuerpo: { recibido: true, ...r } };
  } catch (e: any) {
    await query('UPDATE pagos_eventos SET procesado = false, error = $2 WHERE id = $1', [ev.id, String(e?.message ?? e).slice(0, 500)]).catch(() => {});
    return { status: 500, cuerpo: { error: 'No se pudo procesar el evento; Stripe lo reintentará.' } };
  }
}
