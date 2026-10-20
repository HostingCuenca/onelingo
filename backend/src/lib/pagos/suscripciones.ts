/**
 * Suscripciones (tabla `suscripciones`): el servidor es la autoridad del plan.
 * - Estado y acceso (funciones puras, testeables).
 * - Sincronización desde objetos de Stripe (webhook o «Confirmar» al volver de Checkout).
 * - Cortesía del administrador.
 * - `usuarios.plan_id` se mantiene como dato derivado (lo usan las analíticas).
 */
import { query, uno } from '../db.js';
import { ajustesPago } from './planes.js';
import { proveedorActivo } from './proveedor.js';
import type { ModoPago } from './stripe.js';

export type EstadoSus = 'activa' | 'prueba_stripe' | 'impago' | 'cancelada' | 'vencida';
export type FilaSus = {
  usuario_id: string; plan_id: string; origen: 'stripe' | 'cortesia'; estado: EstadoSus; cancela_al_final: boolean;
  periodo_fin: string | Date | null; stripe_cliente_id: string | null; stripe_suscripcion_id: string | null; stripe_precio_id: string | null;
  modo: ModoPago | null; nota: string; importe_centavos: number | null; moneda: string | null; intervalo: 'mes' | 'anio' | null;
  creado_en?: string | Date; cancelada_en?: string | Date | null; actualizado_en?: string | Date;
};

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const fecha = (v: string | Date | null | undefined) => (v ? new Date(v) : null);
const deUnix = (n: unknown) => (typeof n === 'number' && n > 0 ? new Date(n * 1000) : null);

// ── Puras ────────────────────────────────────────────────────────────────────
/** Estado de Stripe → estado de OneLingo. */
export function estadoDesdeStripe(status: string): EstadoSus {
  switch (status) {
    case 'active': return 'activa';
    case 'trialing': return 'prueba_stripe';
    case 'past_due': case 'unpaid': case 'incomplete': return 'impago';
    case 'canceled': return 'cancelada';
    default: return 'vencida'; // incomplete_expired, paused…
  }
}

/**
 * Acceso: `activa` o `prueba_stripe`; `cancelada` con `periodo_fin` futuro;
 * o cortesía sin fecha o con fecha futura.
 */
export function tieneAcceso(f: Pick<FilaSus, 'origen' | 'estado' | 'periodo_fin'> | null | undefined, ahora = new Date()): boolean {
  if (!f) return false;
  const fin = fecha(f.periodo_fin);
  if (f.origen === 'cortesia') return !fin || fin > ahora;
  if (f.estado === 'activa' || f.estado === 'prueba_stripe') return true;
  if (f.estado === 'cancelada') return !!fin && fin > ahora;
  return false;
}
/** Estado mostrado: una cortesía caducada se ve como «vencida». */
export function estadoEfectivo(f: FilaSus | null | undefined, ahora = new Date()): EstadoSus | 'sin_plan' {
  if (!f) return 'sin_plan';
  if (f.origen === 'cortesia') return tieneAcceso(f, ahora) ? 'activa' : 'vencida';
  return f.estado;
}

/** Datos de una suscripción de Stripe (compatibles con las versiones de API anteriores y posteriores a 2025-03-31). */
export function datosDeStripe(sub: any) {
  const item = sub?.items?.data?.[0];
  const precio = item?.price ?? item?.plan ?? sub?.plan ?? null;
  const finPeriodo = deUnix(sub?.current_period_end) ?? deUnix(item?.current_period_end);
  const status = String(sub?.status ?? '');
  const iv = precio?.recurring?.interval ?? precio?.interval;
  return {
    estado: estadoDesdeStripe(status),
    cancela_al_final: status !== 'canceled' && (!!sub?.cancel_at_period_end || !!sub?.cancel_at),
    // Cancelada: hasta cuándo dura el acceso (fin real; si se canceló al momento, ya pasó).
    periodo_fin: status === 'canceled' ? deUnix(sub?.ended_at) ?? deUnix(sub?.canceled_at) ?? finPeriodo : finPeriodo,
    stripe_cliente_id: typeof sub?.customer === 'string' ? sub.customer : sub?.customer?.id ?? null,
    stripe_suscripcion_id: String(sub?.id ?? ''),
    stripe_precio_id: precio?.id ?? null,
    importe_centavos: typeof precio?.unit_amount === 'number' ? precio.unit_amount : typeof precio?.amount === 'number' ? precio.amount : null,
    moneda: precio?.currency ?? null,
    intervalo: iv === 'year' ? 'anio' as const : iv === 'month' ? 'mes' as const : null,
    modo: (sub?.livemode ? 'live' : 'test') as ModoPago,
    cancelada_en: status === 'canceled' ? deUnix(sub?.canceled_at) ?? deUnix(sub?.ended_at) ?? new Date() : null,
    precioPlan: (precio?.metadata?.plan_id || null) as string | null,
    suscripcionPlan: (sub?.metadata?.plan_id || null) as string | null,
    productoId: (typeof precio?.product === 'string' ? precio.product : precio?.product?.id ?? null) as string | null,
    usuarioPista: (sub?.metadata?.usuario_id || null) as string | null,
  };
}

/**
 * ¿Se aplica la suscripción de Stripe `nueva` sobre la fila `actual`?
 * Sí si no hay fila, si es la misma suscripción, si la nueva da acceso o si
 * la actual ya no lo da. No: un evento tardío de una suscripción vieja no pisa
 * una cortesía vigente ni otra suscripción con acceso.
 */
export function debeAplicar(actual: FilaSus | null | undefined, nueva: Pick<FilaSus, 'stripe_suscripcion_id' | 'estado' | 'periodo_fin'>, ahora = new Date()) {
  if (!actual) return true;
  if (actual.origen === 'stripe' && actual.stripe_suscripcion_id === nueva.stripe_suscripcion_id) return true;
  if (tieneAcceso({ origen: 'stripe', estado: nueva.estado, periodo_fin: nueva.periodo_fin }, ahora)) return true;
  return !tieneAcceso(actual, ahora);
}

/** MRR en USD de las suscripciones de Stripe que pagan (los anuales cuentan /12). */
export function calcularMrr(filas: (Partial<FilaSus> & { plan_precio_centavos?: number | null; plan_intervalo?: string | null; plan_moneda?: string | null })[]) {
  let centavos = 0, otras = 0;
  for (const f of filas) {
    if (f.origen !== 'stripe' || f.estado !== 'activa') continue;
    const importe = f.importe_centavos ?? f.plan_precio_centavos ?? 0;
    const intervalo = f.intervalo ?? f.plan_intervalo ?? 'mes';
    const moneda = (f.moneda ?? f.plan_moneda ?? 'usd').toLowerCase();
    if (moneda !== 'usd') { otras++; continue; }
    centavos += intervalo === 'anio' ? importe / 12 : importe;
  }
  return { mrr: Math.round(centavos) / 100, otrasMonedas: otras };
}

// ── Base de datos ────────────────────────────────────────────────────────────
export const filaDe = (usuarioId: string) => uno<FilaSus>('SELECT * FROM suscripciones WHERE usuario_id = $1', [usuarioId]);

/** `usuarios.plan_id` = plan con acceso o ''. */
export async function actualizarPlanDerivado(usuarioId: string) {
  const f = await filaDe(usuarioId);
  const plan = tieneAcceso(f) ? f!.plan_id : '';
  await query('UPDATE usuarios SET plan_id = $2 WHERE id = $1 AND plan_id IS DISTINCT FROM $2', [usuarioId, plan]);
  return plan;
}

/** Acceso en SQL (alias `s`), igual que `tieneAcceso`. */
export const ACCESO_SQL = `(s.origen = 'cortesia' AND (s.periodo_fin IS NULL OR s.periodo_fin > now()))
  OR (s.origen = 'stripe' AND (s.estado IN ('activa', 'prueba_stripe') OR (s.estado = 'cancelada' AND s.periodo_fin > now())))`;

/**
 * Pone al día `usuarios.plan_id` de quienes tienen fila en `suscripciones`
 * (p. ej. una cortesía o un periodo que caducó). No toca a quienes no tienen
 * fila: su `plan_id` antiguo (elegido en la app antes de la fase 1) se conserva.
 */
export async function refrescarPlanesDerivados() {
  await query(`UPDATE usuarios u SET plan_id = x.plan FROM (
      SELECT s.usuario_id, CASE WHEN ${ACCESO_SQL} THEN s.plan_id ELSE '' END AS plan FROM suscripciones s) x
    WHERE x.usuario_id = u.id AND u.plan_id IS DISTINCT FROM x.plan`);
}

/** Plan efectivo de un alumno según el servidor ('' = sin plan). */
export async function planEfectivo(usuarioId: string) {
  const f = await filaDe(usuarioId);
  return tieneAcceso(f) ? f!.plan_id : '';
}

/**
 * Sincroniza una suscripción de Stripe con la fila del alumno. El alumno sale de
 * `usuarioId` (client_reference_id), de `metadata.usuario_id` o de una fila con
 * la misma suscripción o el mismo cliente. El plan sale del Price ACTUAL de la
 * suscripción (tras un cambio de plan en el portal, `subscription.metadata.plan_id`
 * sigue diciendo el plan de la compra): `planes.stripe_precio_id` o el historial
 * `planes_precios` (incluye Prices archivados), luego `metadata.plan_id` del Price,
 * el Product del plan, `metadata.plan_id` de la suscripción y, por último, la fila actual.
 */
/** Plan de una suscripción de Stripe por su Price actual (ver sincronizarDesdeStripe). */
export async function planDeStripe(d: Pick<ReturnType<typeof datosDeStripe>, 'stripe_precio_id' | 'precioPlan' | 'productoId' | 'suscripcionPlan'>): Promise<string | null> {
  const existe = async (id: string | null) => (id && (await uno('SELECT 1 FROM planes WHERE id = $1', [id])) ? id : null);
  if (d.stripe_precio_id) {
    const r = await uno<{ id: string }>(`SELECT id FROM planes WHERE stripe_precio_id = $1
      UNION ALL SELECT pp.plan_id FROM planes_precios pp JOIN planes p ON p.id = pp.plan_id WHERE pp.precio_id = $1 LIMIT 1`, [d.stripe_precio_id]);
    if (r) return r.id;
  }
  return (await existe(d.precioPlan))
    ?? (d.productoId ? (await uno<{ id: string }>('SELECT id FROM planes WHERE stripe_producto_id = $1 LIMIT 1', [d.productoId]))?.id ?? null : null)
    ?? (await existe(d.suscripcionPlan));
}

export async function sincronizarDesdeStripe(sub: any, op: { usuarioId?: string | null } = {}) {
  const d = datosDeStripe(sub);
  if (!d.stripe_suscripcion_id) return { aplicada: false, motivo: 'sin id de suscripción' };
  let uid = [op.usuarioId, d.usuarioPista].find((x) => x && UUID.test(x)) ?? null;
  if (!uid) uid = (await uno<{ usuario_id: string }>('SELECT usuario_id FROM suscripciones WHERE stripe_suscripcion_id = $1', [d.stripe_suscripcion_id]))?.usuario_id ?? null;
  if (!uid && d.stripe_cliente_id) uid = (await uno<{ usuario_id: string }>('SELECT usuario_id FROM suscripciones WHERE stripe_cliente_id = $1 LIMIT 1', [d.stripe_cliente_id]))?.usuario_id ?? null;
  if (!uid || !(await uno('SELECT 1 FROM usuarios WHERE id = $1', [uid]))) return { aplicada: false, motivo: 'alumno desconocido' };
  const actual = await filaDe(uid);
  const plan = (await planDeStripe(d)) ?? actual?.plan_id ?? '';
  if (!debeAplicar(actual, d)) return { aplicada: false, motivo: 'otra suscripción o cortesía vigente', usuarioId: uid };
  await query(`INSERT INTO suscripciones (usuario_id, plan_id, origen, estado, cancela_al_final, periodo_fin, stripe_cliente_id, stripe_suscripcion_id, stripe_precio_id,
        modo, nota, importe_centavos, moneda, intervalo, creado_en, cancelada_en, actualizado_en)
      VALUES ($1,$2,'stripe',$3,$4,$5,$6,$7,$8,$9,'',$10,$11,$12, now(), $13, now())
      ON CONFLICT (usuario_id) DO UPDATE SET plan_id=EXCLUDED.plan_id, origen='stripe', estado=EXCLUDED.estado, cancela_al_final=EXCLUDED.cancela_al_final,
        periodo_fin=EXCLUDED.periodo_fin, stripe_cliente_id=EXCLUDED.stripe_cliente_id, stripe_suscripcion_id=EXCLUDED.stripe_suscripcion_id,
        stripe_precio_id=EXCLUDED.stripe_precio_id, modo=EXCLUDED.modo, nota='', importe_centavos=EXCLUDED.importe_centavos, moneda=EXCLUDED.moneda,
        intervalo=EXCLUDED.intervalo,
        creado_en = CASE WHEN suscripciones.origen = 'stripe' AND suscripciones.stripe_suscripcion_id = EXCLUDED.stripe_suscripcion_id THEN suscripciones.creado_en ELSE now() END,
        cancelada_en = CASE WHEN EXCLUDED.estado = 'cancelada' THEN coalesce(suscripciones.cancelada_en, EXCLUDED.cancelada_en) END,
        actualizado_en = now()`,
    [uid, plan, d.estado, d.cancela_al_final, d.periodo_fin, d.stripe_cliente_id, d.stripe_suscripcion_id, d.stripe_precio_id, d.modo,
      d.importe_centavos, d.moneda, d.intervalo, d.cancelada_en]);
  await actualizarPlanDerivado(uid);
  return { aplicada: true, usuarioId: uid, estado: d.estado, planId: plan };
}

/** `invoice.payment_failed`: la suscripción pasa a impago (sin acceso). */
export async function marcarImpago(subId: string) {
  const f = await uno<{ usuario_id: string }>(`UPDATE suscripciones SET estado = 'impago', actualizado_en = now()
    WHERE stripe_suscripcion_id = $1 AND origen = 'stripe' AND estado IN ('activa', 'prueba_stripe', 'impago') RETURNING usuario_id`, [subId]);
  if (f) await actualizarPlanDerivado(f.usuario_id);
  return !!f;
}

/** Respuesta de `GET /usuarios/me/suscripcion` (contrato, punto 2). */
export async function suscripcionDe(usuarioId: string, ahora = new Date()) {
  const [f, a, u] = await Promise.all([filaDe(usuarioId), ajustesPago(), uno<{ trial_segundos: number }>('SELECT trial_segundos FROM usuarios WHERE id = $1', [usuarioId])]);
  const acceso = tieneAcceso(f, ahora);
  const p = proveedorActivo();
  const usados = Math.max(0, Math.round(Number(u?.trial_segundos ?? 0)));
  const total = a.pruebaMinutos * 60;
  return {
    planId: acceso ? f!.plan_id : '',
    estado: estadoEfectivo(f, ahora),
    origen: f?.origen ?? null,
    acceso,
    periodoFin: f?.periodo_fin ? new Date(f.periodo_fin).toISOString() : null,
    cancelaAlFinal: !!f?.cancela_al_final,
    modo: f?.modo ?? null,
    puedeGestionar: !!(p && f?.origen === 'stripe' && f.stripe_cliente_id && f.modo === p.modo()),
    prueba: { minutos: a.pruebaMinutos, segundosUsados: usados, restanteSegundos: Math.max(0, total - usados), agotada: usados >= total },
  };
}

// ── Cortesía ─────────────────────────────────────────────────────────────────
export class ErrorSus extends Error { constructor(m: string, public status: number) { super(m); } }

export async function darCortesia(usuarioId: string, d: { planId: string; hasta?: string | null; nota?: string }, ahora = new Date()) {
  if (!(await uno('SELECT 1 FROM usuarios WHERE id = $1', [usuarioId]))) throw new ErrorSus('El alumno no existe.', 404);
  const p = await uno<{ archivado: boolean }>('SELECT archivado FROM planes WHERE id = $1', [d.planId]);
  if (!p) throw new ErrorSus('El plan no existe.', 400);
  if (p.archivado) throw new ErrorSus('El plan está archivado.', 400);
  const hasta = d.hasta ? new Date(d.hasta) : null;
  if (hasta && !(hasta > ahora)) throw new ErrorSus('La fecha «hasta» debe ser futura.', 400);
  const actual = await filaDe(usuarioId);
  if (actual?.origen === 'stripe' && ['activa', 'prueba_stripe', 'impago'].includes(actual.estado))
    throw new ErrorSus('El alumno tiene una suscripción de Stripe en curso: gestiónala en Stripe antes de dar cortesía.', 409);
  // Se conserva el cliente de Stripe (si lo hubo) para reutilizarlo en un pago futuro.
  await query(`INSERT INTO suscripciones (usuario_id, plan_id, origen, estado, cancela_al_final, periodo_fin, nota, creado_en, actualizado_en)
      VALUES ($1,$2,'cortesia','activa',false,$3,$4, now(), now())
      ON CONFLICT (usuario_id) DO UPDATE SET plan_id=EXCLUDED.plan_id, origen='cortesia', estado='activa', cancela_al_final=false, periodo_fin=EXCLUDED.periodo_fin,
        nota=EXCLUDED.nota, stripe_suscripcion_id=NULL, stripe_precio_id=NULL, importe_centavos=NULL, moneda=NULL, intervalo=NULL,
        creado_en=now(), cancelada_en=NULL, actualizado_en=now()`,
    [usuarioId, d.planId, hasta, (d.nota ?? '').slice(0, 500)]);
  await actualizarPlanDerivado(usuarioId);
  return suscripcionDe(usuarioId, ahora);
}

export async function quitarCortesia(usuarioId: string) {
  const f = await uno(`DELETE FROM suscripciones WHERE usuario_id = $1 AND origen = 'cortesia' RETURNING usuario_id`, [usuarioId]);
  if (!f) throw new ErrorSus('El alumno no tiene cortesía.', 404);
  await actualizarPlanDerivado(usuarioId);
  return suscripcionDe(usuarioId);
}

// ── Panel ────────────────────────────────────────────────────────────────────
export const FILTROS_ESTADO = ['', 'con_acceso', 'activa', 'prueba_stripe', 'impago', 'cancelada', 'vencida', 'cortesia', 'cancela_al_final'] as const;

/** `GET /admin/suscripciones`: filas (con buscador y filtro) y resumen de todas. */
export async function resumenAdmin(filtro: { estado?: string; q?: string } = {}, ahora = new Date()) {
  const todas = await query(`SELECT s.*, u.nombre, u.email, p.nombre AS plan_nombre, p.precio_centavos AS plan_precio_centavos,
      p.intervalo AS plan_intervalo, p.moneda AS plan_moneda
    FROM suscripciones s JOIN usuarios u ON u.id = s.usuario_id LEFT JOIN planes p ON p.id = s.plan_id ORDER BY s.actualizado_en DESC LIMIT 5000`);
  const modo = proveedorActivo()?.modo() ?? null;
  const delModo = todas.filter((f) => f.origen !== 'stripe' || !modo || f.modo === modo);
  const hace30 = new Date(ahora.getTime() - 30 * 86_400_000);
  const stripeM = delModo.filter((f) => f.origen === 'stripe');
  const { mrr, otrasMonedas } = calcularMrr(stripeM);
  const resumen = {
    modo,
    activas: stripeM.filter((f) => f.estado === 'activa' || f.estado === 'prueba_stripe').length,
    mrr, otrasMonedas,
    nuevas30: stripeM.filter((f) => f.creado_en && new Date(f.creado_en) >= hace30).length,
    canceladas30: stripeM.filter((f) => f.cancelada_en && new Date(f.cancelada_en) >= hace30).length,
    impagos: stripeM.filter((f) => f.estado === 'impago').length,
    cortesias: todas.filter((f) => f.origen === 'cortesia' && tieneAcceso(f, ahora)).length,
    otroModo: todas.length - delModo.length,
  };
  const q = (filtro.q ?? '').trim().toLowerCase();
  const e = filtro.estado ?? '';
  const filas = todas
    .map((f) => ({
      usuarioId: f.usuario_id, nombre: f.nombre, email: f.email, planId: f.plan_id, planNombre: f.plan_nombre?.es ?? f.plan_id,
      origen: f.origen, estado: estadoEfectivo(f, ahora), acceso: tieneAcceso(f, ahora), cancelaAlFinal: f.cancela_al_final,
      periodoFin: f.periodo_fin, modo: f.modo, importe: f.importe_centavos !== null ? f.importe_centavos / 100 : null, moneda: f.moneda,
      intervalo: f.intervalo ?? f.plan_intervalo, nota: f.nota, stripeClienteId: f.stripe_cliente_id, stripeSuscripcionId: f.stripe_suscripcion_id,
      creadoEn: f.creado_en, actualizadoEn: f.actualizado_en,
    }))
    .filter((f) => !q || `${f.nombre} ${f.email} ${f.planId} ${f.stripeClienteId ?? ''}`.toLowerCase().includes(q))
    .filter((f) => !e || (e === 'con_acceso' ? f.acceso : e === 'cortesia' ? f.origen === 'cortesia' : e === 'cancela_al_final' ? f.cancelaAlFinal : f.estado === e));
  return { resumen, filas: filas.slice(0, 500), total: filas.length };
}

/** Métricas para `/admin/resumen` (todas las suscripciones del modo actual). */
export async function metricasSuscripciones() {
  const r = await resumenAdmin().catch(() => null);
  return r?.resumen ?? null;
}
