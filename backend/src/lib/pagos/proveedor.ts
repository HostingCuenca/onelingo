/**
 * Interfaz de proveedor de pagos y su implementación con Stripe.
 *
 * Las rutas y la lógica de planes/suscripciones hablan con `proveedorActivo()`,
 * no con Stripe directamente: para añadir Paddle, Kushki u otro basta con
 * implementar `ProveedorPagos` (checkout alojado, portal, consulta de la
 * suscripción y sincronización del catálogo) y elegirlo aquí. Fase 1: solo Stripe.
 */
import { stripeConfig } from '../conexiones.js';
import { configurarPortal, llamarStripe, type ModoPago, type ProductoPortal } from './stripe.js';

export type Texto = { es: string; en: string };
export type FilaPlan = {
  id: string; nombre: Texto; descripcion: Texto; incluye: { es: string[]; en: string[] };
  idiomas: number; precio_centavos: number; moneda: string; intervalo: 'mes' | 'anio';
  destacado: boolean; visible: boolean; orden: number; archivado: boolean;
  stripe_producto_id: string | null; stripe_precio_id: string | null; stripe_modo: string | null;
  stripe_precio_firma: string | null; stripe_sincronizado: boolean; stripe_error: string | null;
  actualizado_en?: string | Date;
};

/** Resultado (también parcial, si algo falla a medias) de sincronizar un plan. */
export type SyncPlan = { productoId: string | null; precioId: string | null; firma: string | null; modo: ModoPago; precioNuevo: boolean; precioArchivado: string | null };

export interface ProveedorPagos {
  readonly id: string;
  disponible(): boolean;
  modo(): ModoPago | null;
  /** Producto/precio del plan en el proveedor. Rellena `out` a medida que avanza. */
  sincronizarPlan(plan: FilaPlan, out: SyncPlan): Promise<SyncPlan>;
  /** URL de la página de pago alojada para suscribirse. */
  crearCheckout(d: { usuarioId: string; email: string; clienteId: string | null; plan: FilaPlan; exito: string; cancelar: string }): Promise<string>;
  /** Sesión de pago y suscripción resultante (objeto del proveedor), para confirmar sin webhook. */
  obtenerCheckout(sessionId: string): Promise<{ usuarioId: string | null; completada: boolean; suscripcion: any | null; clienteId: string | null }>;
  obtenerSuscripcion(id: string): Promise<any>;
  /** URL del portal donde el alumno gestiona su suscripción (con `configuracion`, la de OneLingo). */
  crearPortal(clienteId: string, retorno: string, configuracion?: string | null): Promise<string>;
  /** Configuración del portal: cancelar, tarjeta, facturas y cambio de plan entre `productos`. */
  configurarPortal(d: { productos: ProductoPortal[]; actualId: string | null; retorno: string }): Promise<{ id: string; accion: 'actualizada' | 'creada'; productos: number; omitidos: number }>;
}

export const firmaPrecio = (p: Pick<FilaPlan, 'precio_centavos' | 'moneda' | 'intervalo'>) => `${p.precio_centavos}|${p.moneda}|${p.intervalo}`;
export const intervaloStripe = (i: string) => (i === 'anio' ? 'year' : 'month');

export const stripe: ProveedorPagos = {
  id: 'stripe',
  disponible: () => { const s = stripeConfig(); return !!(s.secretKey && s.modo); },
  modo: () => stripeConfig().modo,

  /**
   * Product con `metadata.plan_id` (se actualiza nombre/estado) y Price
   * recurrente. Los Price son inmutables: si cambió el importe, la moneda o el
   * intervalo se crea otro, pasa a ser el `default_price` y el anterior se
   * archiva (`active=false`). Los suscriptores actuales conservan su Price:
   * no se toca ninguna suscripción. Los ids de otro modo (test↔live) no sirven
   * y se crean de nuevo.
   */
  async sincronizarPlan(plan, out) {
    const s = stripeConfig();
    const modo = s.modo!;
    const mismoModo = plan.stripe_modo === modo;
    out.modo = modo;
    out.productoId = mismoModo ? plan.stripe_producto_id : null;
    out.precioId = mismoModo ? plan.stripe_precio_id : null;
    out.firma = mismoModo ? plan.stripe_precio_firma : null;
    const nombre = plan.nombre.es || plan.nombre.en || plan.id;
    const producto = { name: nombre, active: !plan.archivado, metadata: { plan_id: plan.id } };
    if (out.productoId) {
      await llamarStripe(s.secretKey, 'POST', `/products/${out.productoId}`, { ...producto, description: plan.descripcion.es || '' });
    } else {
      const p = await llamarStripe(s.secretKey, 'POST', '/products', { ...producto, description: plan.descripcion.es || undefined });
      out.productoId = p.id;
    }
    const firma = firmaPrecio(plan);
    if (!out.precioId || out.firma !== firma) {
      const anterior = out.precioId;
      const pr = await llamarStripe(s.secretKey, 'POST', '/prices', {
        product: out.productoId, unit_amount: plan.precio_centavos, currency: plan.moneda,
        recurring: { interval: intervaloStripe(plan.intervalo) }, metadata: { plan_id: plan.id }, nickname: `${nombre} · ${firma}`,
      });
      out.precioId = pr.id; out.firma = firma; out.precioNuevo = true;
      await llamarStripe(s.secretKey, 'POST', `/products/${out.productoId}`, { default_price: pr.id });
      if (anterior) {
        await llamarStripe(s.secretKey, 'POST', `/prices/${anterior}`, { active: false });
        out.precioArchivado = anterior;
      }
    }
    return out;
  },

  async crearCheckout(d) {
    const s = stripeConfig();
    const ses = await llamarStripe(s.secretKey, 'POST', '/checkout/sessions', {
      mode: 'subscription',
      line_items: [{ price: d.plan.stripe_precio_id, quantity: 1 }],
      client_reference_id: d.usuarioId,
      ...(d.clienteId ? { customer: d.clienteId } : { customer_email: d.email }),
      success_url: d.exito, cancel_url: d.cancelar,
      metadata: { usuario_id: d.usuarioId, plan_id: d.plan.id },
      subscription_data: { metadata: { usuario_id: d.usuarioId, plan_id: d.plan.id } },
    });
    if (!ses?.url) throw new Error('Stripe no devolvió la URL de pago.');
    return ses.url;
  },

  async obtenerCheckout(sessionId) {
    const s = stripeConfig();
    const ses = await llamarStripe(s.secretKey, 'GET', `/checkout/sessions/${encodeURIComponent(sessionId)}`, { expand: ['subscription'] });
    let sus = ses?.subscription ?? null;
    if (typeof sus === 'string') sus = await this.obtenerSuscripcion(sus);
    return {
      usuarioId: ses?.client_reference_id ?? ses?.metadata?.usuario_id ?? null,
      completada: ses?.status === 'complete',
      suscripcion: sus,
      clienteId: typeof ses?.customer === 'string' ? ses.customer : ses?.customer?.id ?? null,
    };
  },

  async obtenerSuscripcion(id) {
    return llamarStripe(stripeConfig().secretKey, 'GET', `/subscriptions/${encodeURIComponent(id)}`);
  },

  async crearPortal(clienteId, retorno, configuracion) {
    const r = await llamarStripe(stripeConfig().secretKey, 'POST', '/billing_portal/sessions', { customer: clienteId, return_url: retorno, configuration: configuracion || undefined });
    if (!r?.url) throw new Error('Stripe no devolvió la URL del portal.');
    return r.url;
  },

  async configurarPortal(d) {
    return configurarPortal(stripeConfig().secretKey, { urlRetorno: d.retorno, productos: d.productos, actualId: d.actualId });
  },
};

/** Proveedor en uso (fase 1: Stripe si está vinculado). */
export const proveedorActivo = (): ProveedorPagos | null => (stripe.disponible() ? stripe : null);
