/**
 * Planes (tabla `planes`) y ajustes de pago (tabla `ajustes_pago`).
 * El administrador los edita desde el panel; al guardar se sincronizan con el
 * proveedor de pagos si está vinculado. Si la sincronización falla, el plan se
 * guarda igual y queda «sin sincronizar» (botón «Reintentar»).
 */
import { z } from 'zod';
import { query, uno } from '../db.js';
import { registrarAlGuardarStripe, stripeConfig } from '../conexiones.js';
import { PRUEBA_MINUTOS_POR_DEFECTO } from '../analitica.js';
import { firmaDuracion, proveedorActivo, stripe, type Duracion, type FilaPlan, type PrecioDuracion, type SyncPlan } from './proveedor.js';

// ── Ajustes ──────────────────────────────────────────────────────────────────
/** Regla para que el alumno cambie un idioma de su plan por otro (anexo de idiomas). */
export const REGLAS_CAMBIO_IDIOMAS = ['libre', 'uno_por_periodo', 'solo_admin'] as const;
export type ReglaCambioIdiomas = typeof REGLAS_CAMBIO_IDIOMAS[number];
export type Ajustes = { pruebaMinutos: number; moneda: string; cambioIdiomas: ReglaCambioIdiomas; demoActivo: boolean };
export async function ajustesPago(): Promise<Ajustes> {
  const f = await uno<{ prueba_minutos: number; moneda: string; cambio_idiomas?: string; demo_activo?: boolean }>('SELECT * FROM ajustes_pago WHERE id').catch(() => undefined);
  const regla = REGLAS_CAMBIO_IDIOMAS.find((r) => r === f?.cambio_idiomas) ?? 'uno_por_periodo';
  return { pruebaMinutos: Number.isFinite(Number(f?.prueba_minutos)) ? Number(f!.prueba_minutos) : PRUEBA_MINUTOS_POR_DEFECTO, moneda: f?.moneda || 'usd', cambioIdiomas: regla, demoActivo: f?.demo_activo ?? true };
}
export const AjustesEntrada = z.object({
  pruebaMinutos: z.number().int().min(0).max(10_000),
  moneda: z.string().trim().toLowerCase().regex(/^[a-z]{3}$/, 'Código de moneda de 3 letras (usd, eur…)'),
  cambioIdiomas: z.enum(REGLAS_CAMBIO_IDIOMAS).optional(),
  demoActivo: z.boolean().optional(),
});
export async function guardarAjustes(a: z.infer<typeof AjustesEntrada>) {
  await query(`INSERT INTO ajustes_pago (id, prueba_minutos, moneda, cambio_idiomas, demo_activo, actualizado_en) VALUES (true, $1, $2, coalesce($3, 'uno_por_periodo'), coalesce($4, true), now())
    ON CONFLICT (id) DO UPDATE SET prueba_minutos = EXCLUDED.prueba_minutos, moneda = EXCLUDED.moneda,
      cambio_idiomas = coalesce($3, ajustes_pago.cambio_idiomas), demo_activo = coalesce($4, ajustes_pago.demo_activo), actualizado_en = now()`,
    [a.pruebaMinutos, a.moneda, a.cambioIdiomas ?? null, a.demoActivo ?? null]);
  return ajustesPago();
}

// ── Formato ──────────────────────────────────────────────────────────────────
const texto = (v: any) => ({ es: String(v?.es ?? ''), en: String(v?.en ?? '') });
const lista = (v: any) => ({ es: Array.isArray(v?.es) ? v.es.map(String) : [], en: Array.isArray(v?.en) ? v.en.map(String) : [] });
const duraciones = (v: any): Duracion[] => (Array.isArray(v) ? v : [])
  .map((d) => ({ meses: Number(d?.meses), precio_centavos: Number(d?.precio_centavos) }))
  .filter((d) => Number.isInteger(d.meses) && d.meses > 1 && Number.isFinite(d.precio_centavos) && d.precio_centavos > 0)
  .sort((a, b) => a.meses - b.meses);
export function normalizar(f: any): FilaPlan {
  return {
    ...f, nombre: texto(f.nombre), descripcion: texto(f.descripcion), incluye: lista(f.incluye), precio_centavos: Number(f.precio_centavos), idiomas: Number(f.idiomas), orden: Number(f.orden),
    duraciones: f.intervalo === 'mes' ? duraciones(f.duraciones) : [], usuarios: Math.max(1, Number(f.usuarios ?? 1) || 1),
  };
}
/** Forma pública del contrato (`GET /planes`). */
export function aPublico(f: FilaPlan) {
  return {
    id: f.id, nombre: f.nombre, descripcion: f.descripcion, incluye: f.incluye, idiomas: f.idiomas,
    precio: Math.round(f.precio_centavos) / 100, moneda: f.moneda, intervalo: f.intervalo, destacado: f.destacado, orden: f.orden,
    /** Personas que cubre (Familiar: 4) y opciones de duración (la de 1 mes es `precio`). */
    usuarios: f.usuarios,
    duraciones: [...(f.intervalo === 'mes' ? [{ meses: 1, precio: Math.round(f.precio_centavos) / 100 }] : []),
      ...f.duraciones.map((d) => ({ meses: d.meses, precio: Math.round(d.precio_centavos) / 100 }))],
  };
}
/** Estado de sincronización para el panel. */
export function estadoSync(f: FilaPlan) {
  const p = proveedorActivo();
  if (!p) return { estado: 'sin stripe' as const, error: null };
  if (f.stripe_sincronizado && f.stripe_modo === p.modo() && f.stripe_precio_id) return { estado: 'sincronizado' as const, error: null };
  return { estado: 'sin sincronizar' as const, error: f.stripe_error };
}

// ── Lectura ──────────────────────────────────────────────────────────────────
export async function planesPublicos() {
  const [a, filas] = await Promise.all([ajustesPago(), query('SELECT * FROM planes WHERE visible AND NOT archivado ORDER BY orden, id')]);
  const p = proveedorActivo();
  return { moneda: a.moneda, pruebaMinutos: a.pruebaMinutos, demoActivo: a.demoActivo, pagos: { disponible: !!p, modo: p?.modo() ?? null }, planes: filas.map((f) => aPublico(normalizar(f))) };
}
export async function plan(id: string): Promise<FilaPlan | null> {
  const f = await uno('SELECT * FROM planes WHERE id = $1', [id]);
  return f ? normalizar(f) : null;
}
export async function listarPlanesAdmin() {
  const filas = await query(`SELECT p.*, (SELECT count(*)::int FROM suscripciones s WHERE s.plan_id = p.id) AS suscriptores FROM planes p ORDER BY p.archivado, p.orden, p.id`);
  const p = proveedorActivo();
  return {
    planes: filas.map((f) => { const n = normalizar(f); return { ...aPublico(n), visible: n.visible, archivado: n.archivado, suscriptores: f.suscriptores ?? 0,
      stripe: { ...estadoSync(n), productoId: n.stripe_producto_id, precioId: n.stripe_precio_id, modo: n.stripe_modo }, actualizadoEn: f.actualizado_en } }),
    ajustes: await ajustesPago(), pagos: { disponible: !!p, modo: p?.modo() ?? null },
  };
}

// ── Escritura ────────────────────────────────────────────────────────────────
const TextoCorto = (max: number, min = 0) => z.object({ es: z.string().trim().min(min).max(max), en: z.string().trim().max(max).default('') });
const Ventajas = z.array(z.string().trim().min(1).max(160)).max(20).default([]);
const Duraciones = z.array(z.object({ meses: z.number().int().min(2).max(24), precio: z.number().min(0.5, 'Stripe no cobra menos de 0,50').max(100_000) })).max(6)
  .refine((l) => new Set(l.map((d) => d.meses)).size === l.length, 'Hay dos duraciones con los mismos meses');
const PlanBase = z.object({
  id: z.string().trim().toLowerCase().regex(/^[a-z0-9][a-z0-9-]{0,39}$/, 'Solo minúsculas, números y guiones').optional(),
  nombre: TextoCorto(80, 1),
  descripcion: TextoCorto(500).default({ es: '', en: '' }),
  incluye: z.object({ es: Ventajas, en: Ventajas }).default({ es: [], en: [] }),
  idiomas: z.number().int().min(0).max(10), // 0 = todos los idiomas
  precio: z.number().min(0.5, 'Stripe no cobra menos de 0,50').max(100_000),
  moneda: z.string().trim().toLowerCase().regex(/^[a-z]{3}$/).optional(),
  intervalo: z.enum(['mes', 'anio']),
  destacado: z.boolean().default(false),
  visible: z.boolean().default(true),
  orden: z.number().int().min(0).max(10_000).default(0),
  /** Precios por 3, 6 o 12 meses (solo en planes mensuales). */
  duraciones: Duraciones.default([]),
  /** Personas que cubre el plan (el titular incluido). */
  usuarios: z.number().int().min(1).max(10).default(1),
});
const sinDuracionesAnuales = (d: { intervalo?: string; duraciones?: unknown[] }) => d.intervalo !== 'anio' || !d.duraciones?.length;
const MSG_ANUAL = { message: 'Las duraciones son para planes mensuales: un plan anual no las lleva.', path: ['duraciones'] };
export const PlanEntrada = PlanBase.refine(sinDuracionesAnuales, MSG_ANUAL);
export const PlanCambios = PlanBase.omit({ id: true }).partial().extend({ archivado: z.boolean().optional() }).refine(sinDuracionesAnuales, MSG_ANUAL);
const centavosDe = (l: { meses: number; precio: number }[]) => l.map((d) => ({ meses: d.meses, precio_centavos: Math.round(d.precio * 100) })).sort((a, b) => a.meses - b.meses);

const slug = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'plan';
export class ErrorPlan extends Error { constructor(m: string, public status: number) { super(m); } }

export async function crearPlan(d: z.infer<typeof PlanEntrada>) {
  const base = d.id ?? slug(d.nombre.es);
  let id = base;
  for (let i = 2; await uno('SELECT 1 FROM planes WHERE id = $1', [id]); i++) {
    if (d.id) throw new ErrorPlan(`Ya existe un plan con el id «${id}».`, 409);
    id = `${base}-${i}`.slice(0, 40);
  }
  const moneda = d.moneda ?? (await ajustesPago()).moneda;
  await query(`INSERT INTO planes (id, nombre, descripcion, incluye, idiomas, precio_centavos, moneda, intervalo, destacado, visible, orden, duraciones, usuarios)
    VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)`,
    [id, JSON.stringify(d.nombre), JSON.stringify(d.descripcion), JSON.stringify(d.incluye), d.idiomas, Math.round(d.precio * 100), moneda, d.intervalo, d.destacado, d.visible, d.orden,
      JSON.stringify(centavosDe(d.duraciones)), d.usuarios]);
  return sincronizarPlan(id);
}

export async function actualizarPlan(id: string, d: z.infer<typeof PlanCambios>) {
  const a = await plan(id);
  if (!a) throw new ErrorPlan('El plan no existe.', 404);
  const n = {
    nombre: d.nombre ?? a.nombre, descripcion: d.descripcion ?? a.descripcion, incluye: d.incluye ?? a.incluye,
    idiomas: d.idiomas ?? a.idiomas, precio_centavos: d.precio !== undefined ? Math.round(d.precio * 100) : a.precio_centavos,
    moneda: d.moneda ?? a.moneda, intervalo: d.intervalo ?? a.intervalo, destacado: d.destacado ?? a.destacado,
    visible: d.visible ?? a.visible, orden: d.orden ?? a.orden, archivado: d.archivado ?? a.archivado,
    duraciones: d.duraciones ? centavosDe(d.duraciones) : a.duraciones, usuarios: d.usuarios ?? a.usuarios,
  };
  if (n.intervalo === 'anio' && n.duraciones.length) {
    if (d.duraciones?.length) throw new ErrorPlan(MSG_ANUAL.message, 400);
    n.duraciones = []; // pasó a anual: las duraciones dejan de ofrecerse
  }
  await query(`UPDATE planes SET nombre=$2, descripcion=$3, incluye=$4, idiomas=$5, precio_centavos=$6, moneda=$7, intervalo=$8, destacado=$9,
      visible=$10, orden=$11, archivado=$12, duraciones=$13, usuarios=$14, stripe_sincronizado=false, actualizado_en=now() WHERE id=$1`,
    [id, JSON.stringify(n.nombre), JSON.stringify(n.descripcion), JSON.stringify(n.incluye), n.idiomas, n.precio_centavos, n.moneda, n.intervalo,
      n.destacado, n.visible, n.orden, n.archivado, JSON.stringify(n.duraciones), n.usuarios]);
  return sincronizarPlan(id);
}

/** Archivar = deja de ofrecerse (y se desactiva en Stripe); los suscriptores lo conservan. */
export const archivarPlan = (id: string, archivado = true) => actualizarPlan(id, archivado ? { archivado: true, visible: false } : { archivado: false });

/** Borrado físico solo si nadie lo usa (ni suscripciones ni `usuarios.plan_id`). */
export async function borrarPlan(id: string) {
  const a = await plan(id);
  if (!a) throw new ErrorPlan('El plan no existe.', 404);
  const [u] = await query(`SELECT (SELECT count(*)::int FROM suscripciones WHERE plan_id = $1) + (SELECT count(*)::int FROM usuarios WHERE plan_id = $1) AS n`, [id]);
  if ((u?.n ?? 0) > 0) throw new ErrorPlan('Hay alumnos con este plan: archívalo en lugar de borrarlo.', 409);
  if (a.stripe_producto_id && proveedorActivo() && a.stripe_modo === stripe.modo()) await archivarPlan(id).catch(() => {}); // desactiva el Product
  await query('DELETE FROM planes WHERE id = $1', [id]);
  return { ok: true };
}

/**
 * Sincroniza un plan con el proveedor (si está vinculado) y devuelve su fila para el panel.
 * Después actualiza el Customer Portal (cambio de plan entre los planes visibles),
 * salvo `portal:false` (sincronizarTodos lo hace una vez al final).
 */
export async function sincronizarPlan(id: string, op: { portal?: boolean } = {}) {
  const a = await plan(id);
  if (!a) throw new ErrorPlan('El plan no existe.', 404);
  const p = proveedorActivo();
  let sync: { ok: boolean; error?: string; precioNuevo?: boolean } = { ok: false, error: 'Stripe no está vinculado: el plan se sincronizará al vincularlo.' };
  if (p) {
    const out: SyncPlan = { productoId: null, precioId: null, firma: null, modo: p.modo()!, precioNuevo: false, precioArchivado: null };
    let error: string | null = null;
    const actuales = a.stripe_modo === out.modo ? await preciosDuraciones(id, out.modo) : [];
    try { await p.sincronizarPlan(a, out, actuales); } catch (e: any) { error = String(e?.message ?? e).slice(0, 300) || 'Error desconocido'; }
    // Se guarda también lo conseguido a medias (p. ej. el Product creado aunque falle el Price).
    await query(`UPDATE planes SET stripe_producto_id=$2, stripe_precio_id=$3, stripe_precio_firma=$4, stripe_modo=$5, stripe_sincronizado=$6, stripe_error=$7 WHERE id=$1`,
      [id, out.productoId, out.precioId, out.firma, out.modo, !error, error]);
    await guardarHistorialPrecios(id, a, out);
    sync = error ? { ok: false, error } : { ok: true, precioNuevo: out.precioNuevo };
  }
  const portal = p && op.portal !== false ? await actualizarPortal() : undefined;
  return { plan: (await listarPlanesAdmin()).planes.find((x) => x.id === id), sync, ...(portal ? { portal } : {}) };
}

/** Historial `planes_precios`: el Price anterior y el nuevo del plan; marca el archivado. */
async function guardarHistorialPrecios(id: string, a: FilaPlan, out: SyncPlan) {
  const filas: [string, string | null, string | null][] = [];
  if (a.stripe_precio_id && a.stripe_modo === out.modo) filas.push([a.stripe_precio_id, a.stripe_modo, a.stripe_precio_firma]);
  if (out.precioId) filas.push([out.precioId, out.modo, out.firma]);
  for (const [precio, modo, firma] of filas) {
    await query('INSERT INTO planes_precios (precio_id, plan_id, modo, firma) VALUES ($1,$2,$3,$4) ON CONFLICT (precio_id) DO NOTHING', [precio, id, modo, firma]);
  }
  for (const d of out.duraciones ?? []) {
    await query('INSERT INTO planes_precios (precio_id, plan_id, modo, firma, meses) VALUES ($1,$2,$3,$4,$5) ON CONFLICT (precio_id) DO NOTHING', [d.precioId, id, out.modo, d.firma, d.meses]);
  }
  for (const archivado of [out.precioArchivado, ...(out.duracionesArchivadas ?? [])]) {
    if (archivado) await query('UPDATE planes_precios SET archivado_en = coalesce(archivado_en, now()) WHERE precio_id = $1', [archivado]);
  }
}

/** Prices vigentes de las duraciones de un plan en un modo (historial `planes_precios`). */
export async function preciosDuraciones(planId: string, modo: string): Promise<PrecioDuracion[]> {
  const filas = await query<{ precio_id: string; firma: string; meses: number }>(`SELECT precio_id, firma, meses FROM planes_precios
    WHERE plan_id = $1 AND modo = $2 AND meses > 1 AND archivado_en IS NULL ORDER BY meses, creado_en`, [planId, modo]);
  return filas.map((f) => ({ precioId: f.precio_id, firma: f.firma, meses: Number(f.meses) }));
}

/**
 * Price para suscribirse a `meses` (1 = el mensual del plan). null si el plan no
 * ofrece esa duración o aún no está sincronizada en el modo del proveedor.
 */
export async function precioParaCheckout(pl: FilaPlan, meses: number, modo: string): Promise<string | null> {
  if (meses === 1 || pl.intervalo === 'anio') return meses === 1 && pl.stripe_modo === modo ? pl.stripe_precio_id : null;
  const d = pl.duraciones.find((x) => x.meses === meses);
  if (!d || pl.stripe_modo !== modo) return null;
  return (await preciosDuraciones(pl.id, modo)).find((x) => x.meses === meses && x.firma === firmaDuracion(d, pl.moneda))?.precioId ?? null;
}

export type EstadoPortal = { ok: boolean; productos: number; omitidos: number; error?: string };
/**
 * Configuración del Customer Portal con cambio de plan entre los Price actuales
 * de los planes visibles, no archivados y sincronizados en el modo en uso
 * (por `orden`, hasta 10). Guarda su id en `ajustes_pago`. Un fallo no rompe el
 * guardado del plan: se devuelve el error para avisar en el panel.
 */
export async function actualizarPortal(): Promise<EstadoPortal | undefined> {
  const p = proveedorActivo();
  if (!p) return undefined;
  const modo = p.modo();
  // Cada producto con su Price mensual y los de sus duraciones vigentes.
  const filas = await query<{ producto: string; precio: string; precios: string[] }>(`SELECT p.stripe_producto_id AS producto, p.stripe_precio_id AS precio,
      array_prepend(p.stripe_precio_id, coalesce((SELECT array_agg(pp.precio_id ORDER BY pp.meses) FROM planes_precios pp
        WHERE pp.plan_id = p.id AND pp.modo = $1 AND pp.meses > 1 AND pp.archivado_en IS NULL), '{}')) AS precios
    FROM planes p
    WHERE p.visible AND NOT p.archivado AND p.stripe_sincronizado AND p.stripe_modo = $1 AND p.stripe_producto_id IS NOT NULL AND p.stripe_precio_id IS NOT NULL
    ORDER BY p.orden, p.id`, [modo]);
  const aj = await uno<{ stripe_portal_id: string | null; stripe_portal_modo: string | null }>('SELECT stripe_portal_id, stripe_portal_modo FROM ajustes_pago WHERE id');
  try {
    const r = await p.configurarPortal({ productos: filas, actualId: aj?.stripe_portal_modo === modo ? aj.stripe_portal_id : null, retorno: `${stripeConfig().urlApp}/#/pago?estado=portal` });
    await query(`INSERT INTO ajustes_pago (id, stripe_portal_id, stripe_portal_modo) VALUES (true, $1, $2)
      ON CONFLICT (id) DO UPDATE SET stripe_portal_id = EXCLUDED.stripe_portal_id, stripe_portal_modo = EXCLUDED.stripe_portal_modo`, [r.id, modo]);
    return { ok: true, productos: r.productos, omitidos: r.omitidos };
  } catch (e: any) {
    return { ok: false, productos: 0, omitidos: 0, error: String(e?.message ?? e).slice(0, 300) || 'Error desconocido' };
  }
}

/** Id de la configuración del portal de OneLingo en el modo en uso (la crea si falta). */
export async function idPortal(): Promise<string | null> {
  const modo = proveedorActivo()?.modo();
  if (!modo) return null;
  const leer = async () => {
    const aj = await uno<{ stripe_portal_id: string | null; stripe_portal_modo: string | null }>('SELECT stripe_portal_id, stripe_portal_modo FROM ajustes_pago WHERE id');
    return aj?.stripe_portal_modo === modo ? aj.stripe_portal_id : null;
  };
  return (await leer()) ?? ((await actualizarPortal())?.ok ? leer() : null);
}

export const textoPortal = (r: EstadoPortal | undefined) => !r ? null : r.ok
  ? `Customer Portal configurado: cancelar al final del periodo, tarjeta, facturas y ${r.productos ? `cambio de plan entre ${r.productos} planes${r.omitidos ? ` (${r.omitidos} sin incluir: Stripe admite 10)` : ''}` : 'sin cambio de plan (no hay planes visibles sincronizados)'}.`
  : `No se pudo configurar el Customer Portal (${r.error}). Reintenta sincronizando un plan.`;

/** Todos los planes (al vincular Stripe). Devuelve líneas para la verificación. */
export async function sincronizarTodos(): Promise<string[]> {
  if (!proveedorActivo()) return [];
  const ids = (await query<{ id: string }>('SELECT id FROM planes ORDER BY orden, id')).map((f) => f.id);
  const fallos: string[] = [];
  for (const id of ids) { const r = await sincronizarPlan(id, { portal: false }); if (!r.sync.ok) fallos.push(`${id}: ${r.sync.error}`); }
  const portal = textoPortal(await actualizarPortal());
  return [fallos.length ? `Planes: ${ids.length - fallos.length} de ${ids.length} sincronizados. Fallaron ${fallos.join(' · ')}` : `Planes sincronizados con Stripe: ${ids.length}.`, ...(portal ? [portal] : [])];
}
registrarAlGuardarStripe(sincronizarTodos);
