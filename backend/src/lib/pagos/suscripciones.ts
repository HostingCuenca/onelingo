/**
 * Suscripciones (tabla `suscripciones`): el servidor es la autoridad del plan.
 * - Estado y acceso (funciones puras, testeables).
 * - Sincronización desde objetos de Stripe (webhook o «Confirmar» al volver de Checkout).
 * - Cortesía del administrador.
 * - `usuarios.plan_id` se mantiene como dato derivado (lo usan las analíticas).
 */
import type { FastifyReply, FastifyRequest } from 'fastify';
import { query, uno } from '../db.js';
import { ajustesPago, type ReglaCambioIdiomas } from './planes.js';
import { proveedorActivo } from './proveedor.js';
import type { ModoPago } from './stripe.js';
import { reflejarFamilia, salirDeFamilia } from './familia.js';

export type EstadoSus = 'activa' | 'prueba_stripe' | 'impago' | 'cancelada' | 'vencida';
export type FilaSus = {
  usuario_id: string; plan_id: string; origen: 'stripe' | 'cortesia' | 'familia'; estado: EstadoSus; cancela_al_final: boolean;
  periodo_fin: string | Date | null; stripe_cliente_id: string | null; stripe_suscripcion_id: string | null; stripe_precio_id: string | null;
  modo: ModoPago | null; nota: string; importe_centavos: number | null; moneda: string | null; intervalo: 'mes' | 'anio' | null;
  creado_en?: string | Date; cancelada_en?: string | Date | null; actualizado_en?: string | Date;
  idiomas?: string[] | null; periodo_inicio?: string | Date | null; ultimo_cambio_idiomas?: string | Date | null; todos_idiomas?: boolean;
  /** Meses del periodo del Price (planes de 3, 6 o 12 meses). */
  meses?: number | null;
  /** Miembro de un plan familiar (`origen = 'familia'`): quién paga. */
  titular_id?: string | null;
};

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const fecha = (v: string | Date | null | undefined) => (v ? new Date(v) : null);
const deUnix = (n: unknown) => (typeof n === 'number' && n > 0 ? new Date(n * 1000) : null);

// ── Idiomas (anexo pagos_contrato_idiomas.md) ────────────────────────────────
/** Los 10 idiomas de la app. */
export const CODIGOS_IDIOMA = ['en', 'fr', 'es', 'pt', 'de', 'it', 'zh', 'ja', 'ru', 'ko'] as const;
const esCodigo = (c: string) => (CODIGOS_IDIOMA as readonly string[]).includes(c);
const DIAS_CAMBIO_SIN_PERIODO = 30;

/** Lista de idiomas desde `metadata.idiomas` ("en,fr") o un array: minúsculas, válidos, sin repetidos. `null` si no viene. */
export function leerIdiomas(v: unknown): string[] | null {
  if (v === undefined || v === null) return null;
  const crudos = Array.isArray(v) ? v.map(String) : String(v).split(',');
  return [...new Set(crudos.map((x) => x.trim().toLowerCase()).filter(esCodigo))];
}

/**
 * Valida idiomas elegidos (mensaje para un 400, o `null` si están bien).
 * `n` = idiomas del plan (0 = todos: la lista debe ir vacía). `exactos`: tiene que
 * haber justo `n` (checkout); si no, entre 1 y `n` (cambios y cortesía).
 */
export function errorIdiomas(lista: string[], n: number, op: { exactos?: boolean; minimo?: number } = {}): string | null {
  const malos = lista.filter((c) => !esCodigo(c));
  if (malos.length) return `Código de idioma no válido: ${malos.join(', ')}. Usa: ${CODIGOS_IDIOMA.join(', ')}.`;
  const rep = lista.filter((c, i) => lista.indexOf(c) !== i);
  if (rep.length) return `Idioma repetido: ${[...new Set(rep)].join(', ')}.`;
  if (n === 0) return lista.length ? 'Este plan incluye todos los idiomas: no hay que elegirlos (envía una lista vacía).' : null;
  if (op.exactos && lista.length !== n) return `Este plan incluye ${n} ${n === 1 ? 'idioma' : 'idiomas'}: elige exactamente ${n} (has elegido ${lista.length}).`;
  const min = op.minimo ?? 1;
  if (lista.length < min) return 'Elige al menos un idioma.';
  if (lista.length > n) return `Este plan incluye ${n} ${n === 1 ? 'idioma' : 'idiomas'}: no puedes tener ${lista.length}.`;
  return null;
}

/** El servidor nunca guarda más idiomas que los del plan: se conservan los primeros. Con 0 (todos), sin recorte. */
export const ajustarAlPlan = (lista: string[], n: number) => (n > 0 ? lista.slice(0, n) : lista);

/** Idiomas de una fila: los elegidos, si son todos y cuántos faltan por elegir. */
export function idiomasDe(f: Pick<FilaSus, 'idiomas' | 'todos_idiomas'> | null | undefined, nPlan: number) {
  const todos = !!f && (nPlan === 0 || !!f.todos_idiomas);
  const idiomas = f ? ajustarAlPlan([...(f.idiomas ?? [])], nPlan) : [];
  return { idiomas, todos, porElegir: !f || todos ? 0 : Math.max(0, nPlan - idiomas.length) };
}

/** Acceso de pago en cada uno de los 10 idiomas. */
export function accesoPorIdioma(f: FilaSus | null | undefined, nPlan: number, ahora = new Date()): Record<string, boolean> {
  const general = tieneAcceso(f, ahora);
  const { idiomas, todos } = idiomasDe(f, nPlan);
  return Object.fromEntries(CODIGOS_IDIOMA.map((c) => [c, general && (todos || idiomas.includes(c))]));
}

/** ¿Pasar de `antes` a `despues` es cambiar un idioma? Reordenar o completar los «por elegir» no lo es. */
export const esCambioIdiomas = (antes: string[], despues: string[]) => antes.some((c) => !despues.includes(c));

/**
 * Regla `cambioIdiomas` para el alumno. `uno_por_periodo`: un cambio por periodo de
 * facturación (desde `periodo_inicio`; el siguiente, al empezar el próximo periodo)
 * o, sin periodo (cortesía), uno cada 30 días desde el último.
 */
export function reglaCambioIdiomas(regla: ReglaCambioIdiomas, f: FilaSus | null | undefined, ahora = new Date()): { regla: ReglaCambioIdiomas; permitido: boolean; proximoCambio: string | null } {
  const r = (permitido: boolean, proximo: Date | null = null) => ({ regla, permitido, proximoCambio: proximo ? proximo.toISOString() : null });
  if (!f || !tieneAcceso(f, ahora)) return r(false);
  if (regla === 'libre') return r(true);
  if (regla === 'solo_admin') return r(false);
  const ultimo = fecha(f.ultimo_cambio_idiomas);
  const inicio = fecha(f.periodo_inicio), fin = fecha(f.periodo_fin);
  if (f.origen === 'stripe' && inicio && fin) return !ultimo || ultimo < inicio ? r(true) : r(false, fin);
  const proximo = ultimo ? new Date(ultimo.getTime() + DIAS_CAMBIO_SIN_PERIODO * 86_400_000) : null;
  return !proximo || proximo <= ahora ? r(true) : r(false, proximo);
}

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
 * o cortesía sin fecha o con fecha futura. Familia (reflejo del titular):
 * `activa`/`prueba_stripe` sin fecha o con fecha futura, `cancelada` con fecha futura.
 */
export function tieneAcceso(f: Pick<FilaSus, 'origen' | 'estado' | 'periodo_fin'> | null | undefined, ahora = new Date()): boolean {
  if (!f) return false;
  const fin = fecha(f.periodo_fin);
  if (f.origen === 'cortesia') return !fin || fin > ahora;
  if (f.origen === 'familia') return f.estado === 'cancelada' ? !!fin && fin > ahora : (f.estado === 'activa' || f.estado === 'prueba_stripe') && (!fin || fin > ahora);
  if (f.estado === 'activa' || f.estado === 'prueba_stripe') return true;
  if (f.estado === 'cancelada') return !!fin && fin > ahora;
  return false;
}
/** Estado mostrado: una cortesía caducada se ve como «vencida». */
export function estadoEfectivo(f: FilaSus | null | undefined, ahora = new Date()): EstadoSus | 'sin_plan' {
  if (!f) return 'sin_plan';
  if (f.origen === 'cortesia') return tieneAcceso(f, ahora) ? 'activa' : 'vencida';
  if (f.origen === 'familia') return tieneAcceso(f, ahora) ? f.estado : 'vencida';
  return f.estado;
}

/** Datos de una suscripción de Stripe (compatibles con las versiones de API anteriores y posteriores a 2025-03-31). */
export function datosDeStripe(sub: any) {
  const item = sub?.items?.data?.[0];
  const precio = item?.price ?? item?.plan ?? sub?.plan ?? null;
  const finPeriodo = deUnix(sub?.current_period_end) ?? deUnix(item?.current_period_end);
  const inicioPeriodo = deUnix(sub?.current_period_start) ?? deUnix(item?.current_period_start);
  const status = String(sub?.status ?? '');
  const iv = precio?.recurring?.interval ?? precio?.interval;
  const cada = Number(precio?.recurring?.interval_count ?? precio?.interval_count ?? 1) || 1;
  return {
    estado: estadoDesdeStripe(status),
    cancela_al_final: status !== 'canceled' && (!!sub?.cancel_at_period_end || !!sub?.cancel_at),
    // Cancelada: hasta cuándo dura el acceso (fin real; si se canceló al momento, ya pasó).
    periodo_fin: status === 'canceled' ? deUnix(sub?.ended_at) ?? deUnix(sub?.canceled_at) ?? finPeriodo : finPeriodo,
    periodo_inicio: status === 'canceled' ? null : inicioPeriodo,
    stripe_cliente_id: typeof sub?.customer === 'string' ? sub.customer : sub?.customer?.id ?? null,
    stripe_suscripcion_id: String(sub?.id ?? ''),
    stripe_precio_id: precio?.id ?? null,
    importe_centavos: typeof precio?.unit_amount === 'number' ? precio.unit_amount : typeof precio?.amount === 'number' ? precio.amount : null,
    moneda: precio?.currency ?? null,
    intervalo: iv === 'year' ? 'anio' as const : iv === 'month' ? 'mes' as const : null,
    meses: iv === 'year' ? 12 * cada : iv === 'month' ? cada : null,
    modo: (sub?.livemode ? 'live' : 'test') as ModoPago,
    cancelada_en: status === 'canceled' ? deUnix(sub?.canceled_at) ?? deUnix(sub?.ended_at) ?? new Date() : null,
    precioPlan: (precio?.metadata?.plan_id || null) as string | null,
    suscripcionPlan: (sub?.metadata?.plan_id || null) as string | null,
    productoId: (typeof precio?.product === 'string' ? precio.product : precio?.product?.id ?? null) as string | null,
    usuarioPista: (sub?.metadata?.usuario_id || null) as string | null,
    idiomasPista: leerIdiomas(sub?.metadata?.idiomas),
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

/** MRR en USD de las suscripciones de Stripe que pagan (los anuales cuentan /12; los de N meses, /N). */
export function calcularMrr(filas: (Partial<FilaSus> & { plan_precio_centavos?: number | null; plan_intervalo?: string | null; plan_moneda?: string | null })[]) {
  let centavos = 0, otras = 0;
  for (const f of filas) {
    if (f.origen !== 'stripe' || f.estado !== 'activa') continue;
    const importe = f.importe_centavos ?? f.plan_precio_centavos ?? 0;
    const intervalo = f.intervalo ?? f.plan_intervalo ?? 'mes';
    const moneda = (f.moneda ?? f.plan_moneda ?? 'usd').toLowerCase();
    if (moneda !== 'usd') { otras++; continue; }
    centavos += importe / (Number(f.meses) > 1 ? Number(f.meses) : intervalo === 'anio' ? 12 : 1);
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
  OR (s.origen = 'stripe' AND (s.estado IN ('activa', 'prueba_stripe') OR (s.estado = 'cancelada' AND s.periodo_fin > now())))
  OR (s.origen = 'familia' AND ((s.estado IN ('activa', 'prueba_stripe') AND (s.periodo_fin IS NULL OR s.periodo_fin > now())) OR (s.estado = 'cancelada' AND s.periodo_fin > now())))`;

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

const idiomasDelPlan = async (planId: string) => Number((await uno<{ idiomas: number }>('SELECT idiomas FROM planes WHERE id = $1', [planId]))?.idiomas ?? 1);

/**
 * Idiomas al sincronizar: los de la fila si es la misma suscripción (el alumno pudo
 * cambiarlos después; la metadata de Stripe se queda con los de la compra), si no
 * los de `metadata.idiomas` (suscripción o Checkout Session). Se recortan al plan:
 * al bajar de 3 a 2 quedan los 2 primeros; al subir, los que faltan quedan «por elegir».
 */
export async function sincronizarDesdeStripe(sub: any, op: { usuarioId?: string | null; idiomas?: unknown } = {}) {
  const d = datosDeStripe(sub);
  if (!d.stripe_suscripcion_id) return { aplicada: false, motivo: 'sin id de suscripción' };
  let uid = [op.usuarioId, d.usuarioPista].find((x) => x && UUID.test(x)) ?? null;
  if (!uid) uid = (await uno<{ usuario_id: string }>('SELECT usuario_id FROM suscripciones WHERE stripe_suscripcion_id = $1', [d.stripe_suscripcion_id]))?.usuario_id ?? null;
  if (!uid && d.stripe_cliente_id) uid = (await uno<{ usuario_id: string }>('SELECT usuario_id FROM suscripciones WHERE stripe_cliente_id = $1 LIMIT 1', [d.stripe_cliente_id]))?.usuario_id ?? null;
  if (!uid || !(await uno('SELECT 1 FROM usuarios WHERE id = $1', [uid]))) return { aplicada: false, motivo: 'alumno desconocido' };
  const actual = await filaDe(uid);
  const plan = (await planDeStripe(d)) ?? actual?.plan_id ?? '';
  if (!debeAplicar(actual, d)) return { aplicada: false, motivo: 'otra suscripción o cortesía vigente', usuarioId: uid };
  const misma = actual?.origen === 'stripe' && actual.stripe_suscripcion_id === d.stripe_suscripcion_id;
  const deMetadata = leerIdiomas(op.idiomas) ?? d.idiomasPista;
  const base = misma && actual!.idiomas?.length ? actual!.idiomas : deMetadata ?? (misma ? actual!.idiomas ?? [] : []);
  const idiomas = ajustarAlPlan(base, await idiomasDelPlan(plan));
  await query(`INSERT INTO suscripciones (usuario_id, plan_id, origen, estado, cancela_al_final, periodo_fin, stripe_cliente_id, stripe_suscripcion_id, stripe_precio_id,
        modo, nota, importe_centavos, moneda, intervalo, creado_en, cancelada_en, actualizado_en, idiomas, periodo_inicio, todos_idiomas, meses, titular_id)
      VALUES ($1,$2,'stripe',$3,$4,$5,$6,$7,$8,$9,'',$10,$11,$12, now(), $13, now(), $14, $15, false, $16, NULL)
      ON CONFLICT (usuario_id) DO UPDATE SET plan_id=EXCLUDED.plan_id, origen='stripe', estado=EXCLUDED.estado, cancela_al_final=EXCLUDED.cancela_al_final,
        periodo_fin=EXCLUDED.periodo_fin, stripe_cliente_id=EXCLUDED.stripe_cliente_id, stripe_suscripcion_id=EXCLUDED.stripe_suscripcion_id,
        stripe_precio_id=EXCLUDED.stripe_precio_id, modo=EXCLUDED.modo, nota='', importe_centavos=EXCLUDED.importe_centavos, moneda=EXCLUDED.moneda,
        intervalo=EXCLUDED.intervalo, meses=EXCLUDED.meses, titular_id=NULL,
        creado_en = CASE WHEN suscripciones.origen = 'stripe' AND suscripciones.stripe_suscripcion_id = EXCLUDED.stripe_suscripcion_id THEN suscripciones.creado_en ELSE now() END,
        cancelada_en = CASE WHEN EXCLUDED.estado = 'cancelada' THEN coalesce(suscripciones.cancelada_en, EXCLUDED.cancelada_en) END,
        idiomas = EXCLUDED.idiomas, todos_idiomas = false,
        periodo_inicio = coalesce(EXCLUDED.periodo_inicio, CASE WHEN suscripciones.stripe_suscripcion_id = EXCLUDED.stripe_suscripcion_id THEN suscripciones.periodo_inicio END),
        ultimo_cambio_idiomas = CASE WHEN suscripciones.origen = 'stripe' AND suscripciones.stripe_suscripcion_id = EXCLUDED.stripe_suscripcion_id THEN suscripciones.ultimo_cambio_idiomas END,
        actualizado_en = now()`,
    [uid, plan, d.estado, d.cancela_al_final, d.periodo_fin, d.stripe_cliente_id, d.stripe_suscripcion_id, d.stripe_precio_id, d.modo,
      d.importe_centavos, d.moneda, d.intervalo, d.cancelada_en, idiomas, d.periodo_inicio, d.meses]);
  await actualizarPlanDerivado(uid);
  // Paga por su cuenta: deja de ser miembro de otra familia. Si su plan es familiar, sus miembros lo reflejan.
  if (actual?.origen === 'familia') await salirDeFamilia(uid, { conservarFila: true });
  await reflejarFamilia(uid);
  return { aplicada: true, usuarioId: uid, estado: d.estado, planId: plan, idiomas };
}

/** `invoice.payment_failed`: la suscripción pasa a impago (sin acceso). */
export async function marcarImpago(subId: string) {
  const f = await uno<{ usuario_id: string }>(`UPDATE suscripciones SET estado = 'impago', actualizado_en = now()
    WHERE stripe_suscripcion_id = $1 AND origen = 'stripe' AND estado IN ('activa', 'prueba_stripe', 'impago') RETURNING usuario_id`, [subId]);
  if (f) { await actualizarPlanDerivado(f.usuario_id); await reflejarFamilia(f.usuario_id); }
  return !!f;
}

/** Respuesta de `GET /usuarios/me/suscripcion` (contrato, punto 2). */
export async function suscripcionDe(usuarioId: string, ahora = new Date()) {
  const [f, a, u] = await Promise.all([filaDe(usuarioId), ajustesPago(), uno<{ trial_segundos: number; idioma_meta: string }>('SELECT trial_segundos, idioma_meta FROM usuarios WHERE id = $1', [usuarioId])]);
  const general = tieneAcceso(f, ahora);
  const nPlan = f ? await idiomasDelPlan(f.plan_id) : 1;
  const porIdioma = accesoPorIdioma(f, nPlan, ahora);
  const { idiomas, todos, porElegir } = idiomasDe(f, nPlan);
  const cambio = reglaCambioIdiomas(a.cambioIdiomas, f, ahora);
  const p = proveedorActivo();
  const usados = Math.max(0, Math.round(Number(u?.trial_segundos ?? 0)));
  const total = a.pruebaMinutos * 60;
  const usuariosPlan = f ? Number((await uno<{ usuarios: number }>('SELECT usuarios FROM planes WHERE id = $1', [f.plan_id]))?.usuarios ?? 1) : null;
  return {
    planId: general ? f!.plan_id : '',
    estado: estadoEfectivo(f, ahora),
    origen: f?.origen ?? null,
    /** Acceso de pago en el idioma meta actual del alumno (`usuarios.idioma_meta`). */
    acceso: !!porIdioma[u?.idioma_meta ?? ''],
    /** Acceso de pago en general (algún idioma). */
    accesoPlan: general,
    idiomaMeta: u?.idioma_meta ?? null,
    idiomasPlan: f ? nPlan : null,
    idiomas, todosLosIdiomas: general && todos, idiomasPorElegir: general ? porElegir : 0,
    cambioIdiomas: todos ? { ...cambio, permitido: false, proximoCambio: null } : cambio,
    accesoPorIdioma: porIdioma,
    periodoFin: f?.periodo_fin ? new Date(f.periodo_fin).toISOString() : null,
    cancelaAlFinal: !!f?.cancela_al_final,
    modo: f?.modo ?? null,
    /** Meses del periodo que paga (1, 3, 6, 12) y personas que cubre su plan. */
    meses: f?.origen === 'stripe' ? Number(f.meses ?? (f.intervalo === 'anio' ? 12 : 1)) : null,
    usuariosPlan,
    /** Miembro de un plan familiar: lo paga otra persona. */
    familiar: f?.origen === 'familia',
    puedeGestionar: !!(p && f?.origen === 'stripe' && f.stripe_cliente_id && f.modo === p.modo()),
    prueba: { minutos: a.pruebaMinutos, segundosUsados: usados, restanteSegundos: Math.max(0, total - usados), agotada: usados >= total },
  };
}

/**
 * ¿Puede el alumno usar al tutor (chat, voz, videollamada)? Con plan, sí; sin plan,
 * mientras le quede prueba (`usuarios.trial_segundos`, lo que reporta la app). Los
 * usuarios demo, además, solo con el modo demo abierto (Panel → Pagos).
 */
export async function bloqueoPractica(usuarioId: string, ahora = new Date()): Promise<{ status: 402 | 403; error: 'prueba_agotada' | 'demo_cerrado' } | null> {
  const [f, a, u] = await Promise.all([filaDe(usuarioId), ajustesPago(), uno<{ trial_segundos: number; es_demo: boolean }>('SELECT trial_segundos, es_demo FROM usuarios WHERE id = $1', [usuarioId])]);
  if (u?.es_demo && !a.demoActivo) return { status: 403, error: 'demo_cerrado' };
  if (tieneAcceso(f, ahora)) return null;
  if (Number(u?.trial_segundos ?? 0) >= a.pruebaMinutos * 60) return { status: 402, error: 'prueba_agotada' };
  return null;
}
/** preHandler tras `requiereAlumno` en las rutas que gastan IA. */
export async function requierePractica(req: FastifyRequest, reply: FastifyReply) {
  const b = await bloqueoPractica((req.user as { sub: string }).sub);
  if (b) return reply.code(b.status).send({ error: b.error });
}

// ── Cortesía ─────────────────────────────────────────────────────────────────
export class ErrorSus extends Error { constructor(m: string, public status: number, public extra: Record<string, unknown> = {}) { super(m); } }

/**
 * Cambia los idiomas de pago. El alumno, según la regla `cambioIdiomas` (completar
 * los «por elegir» o reordenar no cuenta como cambio); el administrador (`admin`)
 * sin regla. Siempre respeta el número de idiomas del plan. Se registra en `eventos`.
 */
export async function cambiarIdiomas(usuarioId: string, lista: string[], op: { admin?: boolean } = {}, ahora = new Date()) {
  const f = await filaDe(usuarioId);
  if (!f) throw new ErrorSus(op.admin ? 'El alumno no tiene suscripción ni cortesía.' : 'No tienes una suscripción.', op.admin ? 404 : 409);
  if (!op.admin && !tieneAcceso(f, ahora)) throw new ErrorSus('Tu suscripción no está activa.', 409);
  const nPlan = await idiomasDelPlan(f.plan_id);
  const { idiomas: antes, todos } = idiomasDe(f, nPlan);
  if (todos) throw new ErrorSus('El plan incluye todos los idiomas: no hay que elegirlos.', 400);
  const nueva = lista.map((c) => String(c).trim().toLowerCase());
  const error = errorIdiomas(nueva, nPlan);
  if (error) throw new ErrorSus(error, 400);
  const cambio = esCambioIdiomas(antes, nueva);
  if (cambio && !op.admin) {
    const r = reglaCambioIdiomas((await ajustesPago()).cambioIdiomas, f, ahora);
    if (!r.permitido) throw new ErrorSus(r.regla === 'solo_admin'
      ? 'Los idiomas del plan solo los cambia el soporte: pídelo desde la app.'
      : `Ya cambiaste un idioma en este periodo. Podrás cambiarlo de nuevo${r.proximoCambio ? ` a partir del ${r.proximoCambio.slice(0, 10)}` : ' más adelante'}.`, 403, { proximoCambio: r.proximoCambio });
  }
  await query(`UPDATE suscripciones SET idiomas = $2, ultimo_cambio_idiomas = CASE WHEN $3 THEN now() ELSE ultimo_cambio_idiomas END, actualizado_en = now() WHERE usuario_id = $1`,
    [usuarioId, nueva, cambio && !op.admin]);
  await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)',
    [usuarioId, op.admin ? 'cambio_idiomas_admin' : 'cambio_idiomas', JSON.stringify({ antes, despues: nueva, cambio, plan: f.plan_id })]);
  return suscripcionDe(usuarioId, ahora);
}

/**
 * Cortesía: `idiomas` = lista (hasta los del plan; los que falten quedan «por elegir»)
 * o 'todos'. Sin `idiomas`, el idioma meta del alumno.
 */
export async function darCortesia(usuarioId: string, d: { planId: string; idiomas?: string[] | 'todos'; hasta?: string | null; nota?: string }, ahora = new Date()) {
  const u = await uno<{ idioma_meta: string }>('SELECT idioma_meta FROM usuarios WHERE id = $1', [usuarioId]);
  if (!u) throw new ErrorSus('El alumno no existe.', 404);
  const p = await uno<{ archivado: boolean; idiomas: number }>('SELECT archivado, idiomas FROM planes WHERE id = $1', [d.planId]);
  if (!p) throw new ErrorSus('El plan no existe.', 400);
  if (p.archivado) throw new ErrorSus('El plan está archivado.', 400);
  const nPlan = Number(p.idiomas);
  const todos = d.idiomas === 'todos';
  let idiomas: string[] = [];
  if (Array.isArray(d.idiomas)) {
    idiomas = d.idiomas.map((c) => String(c).trim().toLowerCase());
    const error = nPlan === 0 && idiomas.length === 0 ? null : errorIdiomas(idiomas, nPlan, { minimo: 0 });
    if (error) throw new ErrorSus(error, 400);
  } else if (!todos && nPlan > 0 && esCodigo(u.idioma_meta)) idiomas = [u.idioma_meta];
  const hasta = d.hasta ? new Date(d.hasta) : null;
  if (hasta && !(hasta > ahora)) throw new ErrorSus('La fecha «hasta» debe ser futura.', 400);
  const actual = await filaDe(usuarioId);
  if (actual?.origen === 'stripe' && ['activa', 'prueba_stripe', 'impago'].includes(actual.estado))
    throw new ErrorSus('El alumno tiene una suscripción de Stripe en curso: gestiónala en Stripe antes de dar cortesía.', 409);
  // Se conserva el cliente de Stripe (si lo hubo) para reutilizarlo en un pago futuro.
  await query(`INSERT INTO suscripciones (usuario_id, plan_id, origen, estado, cancela_al_final, periodo_fin, nota, creado_en, actualizado_en, idiomas, todos_idiomas)
      VALUES ($1,$2,'cortesia','activa',false,$3,$4, now(), now(), $5, $6)
      ON CONFLICT (usuario_id) DO UPDATE SET plan_id=EXCLUDED.plan_id, origen='cortesia', estado='activa', cancela_al_final=false, periodo_fin=EXCLUDED.periodo_fin,
        nota=EXCLUDED.nota, stripe_suscripcion_id=NULL, stripe_precio_id=NULL, importe_centavos=NULL, moneda=NULL, intervalo=NULL,
        idiomas=EXCLUDED.idiomas, todos_idiomas=EXCLUDED.todos_idiomas, periodo_inicio=NULL, ultimo_cambio_idiomas=NULL,
        meses=NULL, titular_id=NULL, creado_en=now(), cancelada_en=NULL, actualizado_en=now()`,
    [usuarioId, d.planId, hasta, (d.nota ?? '').slice(0, 500), idiomas, todos]);
  await actualizarPlanDerivado(usuarioId);
  if (actual?.origen === 'familia') await salirDeFamilia(usuarioId, { conservarFila: true });
  await reflejarFamilia(usuarioId);
  return suscripcionDe(usuarioId, ahora);
}

export async function quitarCortesia(usuarioId: string) {
  const f = await uno(`DELETE FROM suscripciones WHERE usuario_id = $1 AND origen = 'cortesia' RETURNING usuario_id`, [usuarioId]);
  if (!f) throw new ErrorSus('El alumno no tiene cortesía.', 404);
  await actualizarPlanDerivado(usuarioId);
  await reflejarFamilia(usuarioId);
  return suscripcionDe(usuarioId);
}

// ── Panel ────────────────────────────────────────────────────────────────────
export const FILTROS_ESTADO = ['', 'con_acceso', 'activa', 'prueba_stripe', 'impago', 'cancelada', 'vencida', 'cortesia', 'familia', 'cancela_al_final'] as const;

/**
 * Desglose por idioma: suscriptores de Stripe con acceso y cortesías vigentes por
 * idioma, y MRR (USD) repartido a partes iguales entre los idiomas elegidos de cada
 * suscripción. «todos» = planes o cortesías de todos los idiomas; «por_elegir» =
 * suscripciones sin ningún idioma elegido todavía.
 */
export function desglosePorIdioma(filas: any[], ahora = new Date()) {
  const claves = [...CODIGOS_IDIOMA, 'todos', 'por_elegir'];
  const t: Record<string, { suscriptores: number; cortesias: number; mrr: number }> = Object.fromEntries(claves.map((k) => [k, { suscriptores: 0, cortesias: 0, mrr: 0 }]));
  for (const f of filas) {
    if (!tieneAcceso(f, ahora)) continue;
    const { idiomas, todos } = idiomasDe(f, Number(f.plan_idiomas ?? 1));
    const destino = todos ? ['todos'] : idiomas.length ? idiomas : ['por_elegir'];
    const mrr = f.origen === 'stripe' ? calcularMrr([f]).mrr : 0;
    for (const k of destino) {
      if (f.origen === 'cortesia') t[k].cortesias++; else t[k].suscriptores++;
      t[k].mrr += mrr / destino.length;
    }
  }
  return claves.map((idioma) => ({ idioma, ...t[idioma], mrr: Math.round(t[idioma].mrr * 100) / 100 }))
    .filter((x) => x.suscriptores || x.cortesias || CODIGOS_IDIOMA.includes(x.idioma as any));
}

/** `GET /admin/suscripciones`: filas (con buscador y filtros) y resumen de todas. */
export async function resumenAdmin(filtro: { estado?: string; q?: string; idioma?: string } = {}, ahora = new Date()) {
  const todas = await query(`SELECT s.*, u.nombre, u.email, p.nombre AS plan_nombre, p.precio_centavos AS plan_precio_centavos,
      p.intervalo AS plan_intervalo, p.moneda AS plan_moneda, p.idiomas AS plan_idiomas, t.email AS titular_email
    FROM suscripciones s JOIN usuarios u ON u.id = s.usuario_id LEFT JOIN planes p ON p.id = s.plan_id LEFT JOIN usuarios t ON t.id = s.titular_id
    ORDER BY s.actualizado_en DESC LIMIT 5000`);
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
    familia: todas.filter((f) => f.origen === 'familia' && tieneAcceso(f, ahora)).length,
    otroModo: todas.length - delModo.length,
    porIdioma: desglosePorIdioma(delModo, ahora),
  };
  const q = (filtro.q ?? '').trim().toLowerCase();
  const e = filtro.estado ?? '';
  const filas = todas
    .map((f) => ({ f, ...idiomasDe(f, Number(f.plan_idiomas ?? 1)) }))
    .map(({ f, idiomas, todos, porElegir }) => ({
      usuarioId: f.usuario_id, nombre: f.nombre, email: f.email, planId: f.plan_id, planNombre: f.plan_nombre?.es ?? f.plan_id,
      origen: f.origen, estado: estadoEfectivo(f, ahora), acceso: tieneAcceso(f, ahora), cancelaAlFinal: f.cancela_al_final,
      periodoFin: f.periodo_fin, modo: f.modo, importe: f.importe_centavos !== null ? f.importe_centavos / 100 : null, moneda: f.moneda,
      intervalo: f.intervalo ?? f.plan_intervalo, meses: f.meses ?? null, titularEmail: f.titular_email ?? null, nota: f.nota, stripeClienteId: f.stripe_cliente_id, stripeSuscripcionId: f.stripe_suscripcion_id,
      creadoEn: f.creado_en, actualizadoEn: f.actualizado_en,
      idiomas, todosLosIdiomas: todos, idiomasPorElegir: porElegir, idiomasPlan: Number(f.plan_idiomas ?? 1),
    }))
    .filter((f) => !q || `${f.nombre} ${f.email} ${f.planId} ${f.stripeClienteId ?? ''}`.toLowerCase().includes(q))
    .filter((f) => !filtro.idioma || f.todosLosIdiomas || f.idiomas.includes(filtro.idioma))
    .filter((f) => !e || (e === 'con_acceso' ? f.acceso : e === 'cortesia' || e === 'familia' ? f.origen === e : e === 'cancela_al_final' ? f.cancelaAlFinal : f.estado === e));
  return { resumen, filas: filas.slice(0, 500), total: filas.length };
}

/** Métricas para `/admin/resumen` (todas las suscripciones del modo actual). */
export async function metricasSuscripciones() {
  const r = await resumenAdmin().catch(() => null);
  return r?.resumen ?? null;
}
