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
  /** Duraciones extra (planes mensuales): cobro cada `meses` meses. */
  duraciones: Duracion[]; usuarios: number;
  stripe_producto_id: string | null; stripe_precio_id: string | null; stripe_modo: string | null;
  stripe_precio_firma: string | null; stripe_sincronizado: boolean; stripe_error: string | null;
  actualizado_en?: string | Date;
};

export type Duracion = { meses: number; precio_centavos: number };
/** Price de una duración en el proveedor (historial `planes_precios`, sin archivar). */
export type PrecioDuracion = { precioId: string; firma: string; meses: number };

/**
 * Resultado (también parcial, si algo falla a medias) de sincronizar un plan.
 * `duraciones`: los Price vigentes de las duraciones; `duracionesArchivadas`, los que dejaron de usarse.
 */
export type SyncPlan = {
  productoId: string | null; precioId: string | null; firma: string | null; modo: ModoPago; precioNuevo: boolean; precioArchivado: string | null;
  duraciones?: (PrecioDuracion & { nuevo: boolean })[]; duracionesArchivadas?: string[];
};

export interface ProveedorPagos {
  readonly id: string;
  disponible(): boolean;
  modo(): ModoPago | null;
  /**
   * Producto/precio del plan en el proveedor y un precio por duración (`actuales`:
   * los que ya tiene en este modo). Rellena `out` a medida que avanza.
   */
  sincronizarPlan(plan: FilaPlan, out: SyncPlan, actuales?: PrecioDuracion[]): Promise<SyncPlan>;
  /** URL de la página de pago alojada para suscribirse al precio `precioId` (el mensual o el de una duración). */
  crearCheckout(d: { usuarioId: string; email: string; clienteId: string | null; plan: FilaPlan; precioId: string; meses: number; idiomas: string[]; exito: string; cancelar: string }): Promise<string>;
  /** Sesión de pago y suscripción resultante (objeto del proveedor), para confirmar sin webhook. */
  obtenerCheckout(sessionId: string): Promise<{ usuarioId: string | null; completada: boolean; suscripcion: any | null; clienteId: string | null; idiomas: string | null }>;
  obtenerSuscripcion(id: string): Promise<any>;
  /** URL del portal donde el alumno gestiona su suscripción (con `configuracion`, la de OneLingo). */
  crearPortal(clienteId: string, retorno: string, configuracion?: string | null): Promise<string>;
  /** Configuración del portal: cancelar, tarjeta, facturas y cambio de plan entre `productos`. */
  configurarPortal(d: { productos: ProductoPortal[]; actualId: string | null; retorno: string }): Promise<{ id: string; accion: 'actualizada' | 'creada'; productos: number; omitidos: number }>;
}

export const firmaPrecio = (p: Pick<FilaPlan, 'precio_centavos' | 'moneda' | 'intervalo'>) => `${p.precio_centavos}|${p.moneda}|${p.intervalo}`;
/** Firma del Price de una duración: «5500|usd|mes:3». */
export const firmaDuracion = (d: Duracion, moneda: string) => `${d.precio_centavos}|${moneda}|mes:${d.meses}`;
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
  async sincronizarPlan(plan, out, actuales = []) {
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
    // Duraciones: un Price recurrente cada N meses por duración; si cambia el importe, otro.
    out.duraciones = []; out.duracionesArchivadas = [];
    const usados = new Set<string>();
    for (const d of plan.intervalo === 'mes' ? plan.duraciones : []) {
      const f = firmaDuracion(d, plan.moneda);
      const previo = actuales.find((a) => a.firma === f && a.meses === d.meses && !usados.has(a.precioId));
      if (previo) { usados.add(previo.precioId); out.duraciones.push({ ...previo, nuevo: false }); continue; }
      const pr = await llamarStripe(s.secretKey, 'POST', '/prices', {
        product: out.productoId, unit_amount: d.precio_centavos, currency: plan.moneda,
        recurring: { interval: 'month', interval_count: d.meses }, metadata: { plan_id: plan.id, meses: d.meses }, nickname: `${nombre} · ${f}`,
      });
      usados.add(pr.id); out.duraciones.push({ precioId: pr.id, firma: f, meses: d.meses, nuevo: true });
    }
    for (const a of actuales) {
      if (usados.has(a.precioId)) continue;
      await llamarStripe(s.secretKey, 'POST', `/prices/${a.precioId}`, { active: false });
      out.duracionesArchivadas.push(a.precioId);
    }
    return out;
  },

  async crearCheckout(d) {
    const s = stripeConfig();
    const ses = await llamarStripe(s.secretKey, 'POST', '/checkout/sessions', {
      mode: 'subscription',
      line_items: [{ price: d.precioId, quantity: 1 }],
      client_reference_id: d.usuarioId,
      ...(d.clienteId ? { customer: d.clienteId } : { customer_email: d.email }),
      success_url: d.exito, cancel_url: d.cancelar,
      // Idiomas elegidos ("en,fr"; vacío en un plan de todos los idiomas): el webhook y «Confirmar» los guardan.
      metadata: { usuario_id: d.usuarioId, plan_id: d.plan.id, meses: d.meses, idiomas: d.idiomas.join(',') || undefined },
      subscription_data: { metadata: { usuario_id: d.usuarioId, plan_id: d.plan.id, meses: d.meses, idiomas: d.idiomas.join(',') || undefined } },
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
      idiomas: typeof ses?.metadata?.idiomas === 'string' ? ses.metadata.idiomas : null,
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
