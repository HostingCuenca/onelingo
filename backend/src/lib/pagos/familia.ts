/**
 * Plan familiar (`planes.usuarios > 1`): el titular paga y añade por correo a
 * `usuarios - 1` personas (tabla `familia_miembros`). Cada miembro tiene su
 * propia fila en `suscripciones` con `origen = 'familia'`, reflejo de la del
 * titular: mismo plan y estado, sus propios idiomas y progreso.
 * - El reflejo se rehace con cada cambio del titular (Stripe, cortesía).
 * - Un correo sin cuenta queda pendiente hasta que alguien entra con él.
 * - La fila de un miembro nunca pisa una suscripción o cortesía propia vigente.
 */
import { query, uno } from '../db.js';
import { enviarCorreo, esc, plantilla } from '../correo.js';
import { stripeConfig } from '../conexiones.js';
import { actualizarPlanDerivado, ajustarAlPlan, CODIGOS_IDIOMA, ErrorSus, filaDe, tieneAcceso, type FilaSus } from './suscripciones.js';

type PlanFamilia = { usuarios: number; idiomas: number; nombre: { es?: string; en?: string } };
const planDe = (id: string) => uno<PlanFamilia>('SELECT usuarios, idiomas, nombre FROM planes WHERE id = $1', [id]);
const normalizarCorreo = (e: string) => e.trim().toLowerCase();

/** ¿La fila da derecho a invitar? Acceso propio (no de familia) a un plan de varias personas. */
async function plazasDe(f: FilaSus | null | undefined): Promise<number> {
  if (!f || f.origen === 'familia' || !tieneAcceso(f)) return 0;
  return Math.max(0, Number((await planDe(f.plan_id))?.usuarios ?? 1) - 1);
}

/**
 * Estado del reflejo a partir del titular. Stripe activa: sin fecha (lo
 * mantiene al día el siguiente evento); cancelada: hasta el fin del periodo;
 * cortesía: hasta su fecha. Sin acceso, el miembro queda sin plan.
 */
function reflejo(t: FilaSus) {
  if (t.origen === 'cortesia') return { estado: 'activa' as const, fin: t.periodo_fin, cancela: false };
  if (t.estado === 'cancelada') return { estado: 'cancelada' as const, fin: t.periodo_fin, cancela: false };
  return { estado: t.estado, fin: null, cancela: t.cancela_al_final };
}

/** Rehace las filas de los miembros del titular. Seguro de llamar con cualquier alumno. */
export async function reflejarFamilia(titularId: string) {
  const miembros = await query<{ usuario_id: string }>('SELECT usuario_id FROM familia_miembros WHERE titular_id = $1 AND usuario_id IS NOT NULL', [titularId]);
  if (!miembros.length) return;
  const t = await filaDe(titularId);
  const p = t ? await planDe(t.plan_id) : null;
  const familiar = !!t && t.origen !== 'familia' && Number(p?.usuarios ?? 1) > 1;
  for (const { usuario_id: uid } of miembros) {
    const actual = await filaDe(uid);
    if (!familiar) {
      if (actual?.origen === 'familia') await query(`DELETE FROM suscripciones WHERE usuario_id = $1 AND origen = 'familia'`, [uid]);
    } else {
      // Una suscripción o cortesía propia vigente manda sobre la familia.
      if (actual && actual.origen !== 'familia' && tieneAcceso(actual)) continue;
      const r = reflejo(t!);
      const nPlan = Number(p!.idiomas);
      const meta = (await uno<{ idioma_meta: string }>('SELECT idioma_meta FROM usuarios WHERE id = $1', [uid]))?.idioma_meta ?? '';
      const mismos = actual?.origen === 'familia' && actual.plan_id === t!.plan_id && actual.idiomas?.length;
      const idiomas = mismos ? actual!.idiomas! : nPlan > 0 && (CODIGOS_IDIOMA as readonly string[]).includes(meta) ? [meta] : [];
      await query(`INSERT INTO suscripciones (usuario_id, plan_id, origen, estado, cancela_al_final, periodo_fin, titular_id, idiomas, nota, creado_en, actualizado_en)
          VALUES ($1, $2, 'familia', $3, $4, $5, $6, $7, '', now(), now())
        ON CONFLICT (usuario_id) DO UPDATE SET plan_id = EXCLUDED.plan_id, origen = 'familia', estado = EXCLUDED.estado, cancela_al_final = EXCLUDED.cancela_al_final,
          periodo_fin = EXCLUDED.periodo_fin, titular_id = EXCLUDED.titular_id, idiomas = EXCLUDED.idiomas, todos_idiomas = false, nota = '',
          stripe_suscripcion_id = NULL, stripe_precio_id = NULL, importe_centavos = NULL, moneda = NULL, intervalo = NULL, meses = NULL, periodo_inicio = NULL,
          creado_en = CASE WHEN suscripciones.origen = 'familia' THEN suscripciones.creado_en ELSE now() END, cancelada_en = NULL, actualizado_en = now()`,
        [uid, t!.plan_id, r.estado, r.cancela, r.fin, titularId, ajustarAlPlan(idiomas, nPlan)]);
    }
    await actualizarPlanDerivado(uid);
  }
}

/** Invitaciones pendientes a este correo: pasan a la cuenta (al entrar en la app). */
export async function vincularInvitaciones(usuarioId: string) {
  const u = await uno<{ email: string }>('SELECT email FROM usuarios WHERE id = $1', [usuarioId]);
  if (!u?.email) return;
  const filas = await query<{ titular_id: string }>(`UPDATE familia_miembros SET usuario_id = $1
    WHERE email = $2 AND usuario_id IS NULL AND titular_id <> $1 AND NOT EXISTS (SELECT 1 FROM familia_miembros WHERE usuario_id = $1) RETURNING titular_id`,
  [usuarioId, normalizarCorreo(u.email)]);
  for (const f of filas) await reflejarFamilia(f.titular_id);
}

/** `GET /usuarios/me/familia`: titular (con sus miembros y plazas) o miembro (con su titular). */
export async function familiaDe(usuarioId: string) {
  const f = await filaDe(usuarioId);
  const plazas = await plazasDe(f);
  const pertenece = await uno<{ titular_id: string; nombre: string; email: string }>(`SELECT m.titular_id, u.nombre, u.email FROM familia_miembros m
    JOIN usuarios u ON u.id = m.titular_id WHERE m.usuario_id = $1`, [usuarioId]);
  const miembros = await query<{ email: string; nombre: string | null; usuario_id: string | null; creado_en: Date }>(`SELECT m.email, u.nombre, m.usuario_id, m.creado_en
    FROM familia_miembros m LEFT JOIN usuarios u ON u.id = m.usuario_id WHERE m.titular_id = $1 ORDER BY m.creado_en`, [usuarioId]);
  return {
    rol: plazas > 0 ? 'titular' as const : pertenece ? 'miembro' as const : null,
    plazas,
    miembros: miembros.map((m) => ({ email: m.email, nombre: m.nombre ?? '', estado: m.usuario_id ? 'activo' as const : 'pendiente' as const, desde: m.creado_en })),
    titular: pertenece ? { nombre: pertenece.nombre, email: pertenece.email } : null,
    /** Miembro con acceso por la familia (no por un plan propio). */
    accesoFamiliar: f?.origen === 'familia' && tieneAcceso(f),
  };
}

/** El titular añade a alguien por correo. Si ya tiene cuenta, el acceso es inmediato. */
export async function invitarMiembro(titularId: string, correo: string) {
  const email = normalizarCorreo(correo);
  const f = await filaDe(titularId);
  const plazas = await plazasDe(f);
  if (!plazas) throw new ErrorSus('Tu plan no es familiar: elige el plan Familiar para añadir a otras personas.', 409);
  const t = await uno<{ email: string; nombre: string }>('SELECT email, nombre FROM usuarios WHERE id = $1', [titularId]);
  if (normalizarCorreo(t?.email ?? '') === email) throw new ErrorSus('Ese es tu propio correo: tú ya estás en el plan.', 400);
  const n = Number((await uno<{ n: number }>('SELECT count(*)::int AS n FROM familia_miembros WHERE titular_id = $1', [titularId]))?.n ?? 0);
  if (n >= plazas) throw new ErrorSus(`Tu plan ya tiene a ${plazas} ${plazas === 1 ? 'persona' : 'personas'} además de ti. Quita a alguien para añadir a otra.`, 409);
  if (await uno('SELECT 1 FROM familia_miembros WHERE email = $1', [email])) throw new ErrorSus('Esa persona ya está en un plan familiar.', 409);
  const u = await uno<{ id: string }>('SELECT id FROM usuarios WHERE lower(email) = $1', [email]);
  if (u) {
    const propia = await filaDe(u.id);
    if (propia && propia.origen !== 'familia' && tieneAcceso(propia)) throw new ErrorSus('Esa cuenta ya tiene su propio plan.', 409);
    if (await uno('SELECT 1 FROM familia_miembros WHERE titular_id = $1', [u.id])) throw new ErrorSus('Esa persona es titular de otro plan familiar.', 409);
  }
  await query('INSERT INTO familia_miembros (titular_id, email, usuario_id) VALUES ($1, $2, $3)', [titularId, email, u?.id ?? null]);
  if (u) await reflejarFamilia(titularId);
  const quien = esc(t?.nombre || t?.email || 'Alguien');
  const plan = esc((await planDe(f!.plan_id))?.nombre?.es || 'Familiar');
  const urlApp = stripeConfig().urlApp || 'https://onelingo.org';
  await enviarCorreo(email, `${t?.nombre || 'Alguien'} te invitó a su plan de OneLingo`, plantilla('Te invitaron a OneLingo',
    u ? `${quien} te añadió a su plan <b>${plan}</b>. Ya tienes acceso: abre la app con este correo y elige tu idioma.`
      : `${quien} te añadió a su plan <b>${plan}</b>. Crea tu cuenta en OneLingo con este correo (${esc(email)}) y tendrás acceso al curso completo.`,
    { texto: 'Abrir OneLingo', url: urlApp })).catch(() => false);
  return familiaDe(titularId);
}

/** El titular quita a un miembro (o una invitación pendiente). */
export async function quitarMiembro(titularId: string, correo: string) {
  const m = await uno<{ usuario_id: string | null }>('DELETE FROM familia_miembros WHERE titular_id = $1 AND email = $2 RETURNING usuario_id', [titularId, normalizarCorreo(correo)]);
  if (!m) throw new ErrorSus('Esa persona no está en tu plan.', 404);
  if (m.usuario_id) {
    await query(`DELETE FROM suscripciones WHERE usuario_id = $1 AND origen = 'familia' AND titular_id = $2`, [m.usuario_id, titularId]);
    await actualizarPlanDerivado(m.usuario_id);
  }
  return familiaDe(titularId);
}

/**
 * El miembro deja la familia. `conservarFila`: su fila ya es otra (compró su
 * propio plan o recibió una cortesía) y solo se borra la pertenencia.
 */
export async function salirDeFamilia(usuarioId: string, op: { conservarFila?: boolean } = {}) {
  const m = await uno<{ titular_id: string }>('DELETE FROM familia_miembros WHERE usuario_id = $1 RETURNING titular_id', [usuarioId]);
  if (!m) {
    if (op.conservarFila) return null;
    throw new ErrorSus('No eres parte de un plan familiar.', 404);
  }
  if (!op.conservarFila) {
    await query(`DELETE FROM suscripciones WHERE usuario_id = $1 AND origen = 'familia'`, [usuarioId]);
    await actualizarPlanDerivado(usuarioId);
  }
  return familiaDe(usuarioId);
}
