/**
 * Eliminar la cuenta desde la app (`DELETE /usuarios/me`, requisito de Google Play).
 *
 * - Las cuentas demo (`@onelingo.demo` o `es_demo`) no se borran: 403. Ana nunca
 *   pierde el acceso.
 * - Stripe: una suscripción en curso se cancela en el acto (sin más cobros). Si no
 *   se puede cancelar, NO se borra nada (502/503) para no seguir cobrando a una
 *   cuenta que ya no existe.
 * - Google Play: el servidor no la cancela; se borra igual y la respuesta avisa
 *   (`googlePlay.debeCancelar`) de que el alumno debe cancelarla en Google Play.
 * - Se borra el usuario y, en cascada, su progreso, errores, exámenes, eventos,
 *   conversaciones, suscripción, familia y reportes; además sus correos, códigos
 *   pendientes y cotizaciones. De una suscripción de pago queda una fila sin datos
 *   personales en `cuentas_eliminadas` (lo que la ley obliga a conservar).
 * - Los miembros de su plan familiar pierden el reflejo y su `plan_id` se recalcula.
 */
import { pool, query, uno } from './db.js';
import { proveedorActivo } from './pagos/proveedor.js';
import { ErrorStripe } from './pagos/stripe.js';
import { actualizarPlanDerivado, esDePago, filaDe } from './pagos/suscripciones.js';

export const CORREO_SOPORTE = 'infoonelingo@gmail.com';
export const esCorreoDemo = (email: string) => email.trim().toLowerCase().endsWith('@onelingo.demo');
const EN_CURSO = ['activa', 'prueba_stripe', 'impago'];

export class ErrorCuenta extends Error {
  constructor(m: string, public status: number, public codigo: string) { super(m); }
}

export type ResultadoEliminar = {
  ok: true;
  /** Suscripción de Stripe cancelada en el acto. */
  stripeCancelada: boolean;
  /** Suscripción de Google Play que sigue viva: el alumno debe cancelarla en Google Play. */
  googlePlay: { debeCancelar: boolean; producto: string | null } | null;
};

export async function eliminarCuenta(usuarioId: string): Promise<ResultadoEliminar> {
  const u = await uno<{ email: string; es_demo: boolean }>('SELECT email, es_demo FROM usuarios WHERE id = $1', [usuarioId]);
  if (!u) throw new ErrorCuenta('La cuenta no existe.', 404, 'cuenta_inexistente');
  if (u.es_demo || esCorreoDemo(u.email)) throw new ErrorCuenta('Las cuentas de demostración no se pueden eliminar.', 403, 'cuenta_demo');
  const email = u.email.trim().toLowerCase();
  const f = await filaDe(usuarioId);

  // 1. Stripe: cancelar antes de borrar nada.
  let stripeCancelada = false, accion = '';
  if (f?.origen === 'stripe' && f.stripe_suscripcion_id && EN_CURSO.includes(f.estado)) {
    const p = proveedorActivo();
    if (p && p.modo() === f.modo) {
      try {
        await p.cancelarSuscripcion(f.stripe_suscripcion_id);
        stripeCancelada = true; accion = 'cancelada_stripe';
      } catch (e) {
        // Ya no existe en Stripe (cancelada o borrada): no hay nada que cobrar.
        if (e instanceof ErrorStripe && e.status === 404) accion = 'ya_cancelada';
        else throw new ErrorCuenta(`No pudimos cancelar tu suscripción. Inténtalo de nuevo en unos minutos o escríbenos a ${CORREO_SOPORTE}.`, 502, 'cancelacion_fallida');
      }
    } else if (f.modo === 'live' && !f.cancela_al_final) {
      // Suscripción real que no podemos tocar desde aquí: seguiría cobrando.
      throw new ErrorCuenta(`No pudimos cancelar tu suscripción ahora. Escríbenos a ${CORREO_SOPORTE} y la eliminamos por ti.`, 503, 'cancelacion_no_disponible');
    } else accion = f.cancela_al_final ? 'cancelaba_al_final' : 'modo_prueba_sin_cancelar';
  }

  // 2. Google Play: no se cancela desde el servidor; se avisa.
  let googlePlay: ResultadoEliminar['googlePlay'] = null;
  if (f?.origen === 'google') {
    const debeCancelar = (f.estado === 'activa' || f.estado === 'impago') && !f.cancela_al_final;
    googlePlay = { debeCancelar, producto: f.google_producto ?? null };
    accion = debeCancelar ? 'cancelar_en_google_play' : 'google_sin_renovacion';
  }

  // 3. Borrado en una transacción.
  const miembros = (await query<{ usuario_id: string }>(`SELECT usuario_id FROM suscripciones WHERE titular_id = $1 AND origen = 'familia'`, [usuarioId]))
    .map((m) => m.usuario_id);
  const c = await pool.connect();
  try {
    await c.query('BEGIN');
    if (f && esDePago(f.origen)) {
      await c.query(`INSERT INTO cuentas_eliminadas (origen_pago, plan_id, estado_pago, modo, stripe_cliente_id, stripe_suscripcion_id, google_pedido, importe_centavos, moneda, meses, accion)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)`,
      [f.origen, f.plan_id ?? '', stripeCancelada ? 'cancelada' : f.estado, f.modo ?? null, f.stripe_cliente_id ?? null, f.stripe_suscripcion_id ?? null,
        f.google_pedido ?? null, f.importe_centavos ?? null, f.moneda ?? null, f.meses ?? null, accion]);
    }
    await c.query('DELETE FROM correos WHERE lower(para) = $1', [email]);
    await c.query('DELETE FROM codigos_correo WHERE lower(email) = $1', [email]);
    await c.query('DELETE FROM cotizaciones WHERE usuario_id = $1', [usuarioId]);
    // Invitaciones a su correo (pendientes o ya vinculadas) en el plan familiar de otra persona.
    await c.query('DELETE FROM familia_miembros WHERE usuario_id = $1 OR lower(email) = $2', [usuarioId, email]);
    // El resto cae en cascada: progreso, errores, examenes, eventos, conversaciones,
    // suscripciones (la suya y los reflejos de sus miembros), familia_miembros y reportes_ia.
    await c.query('DELETE FROM usuarios WHERE id = $1', [usuarioId]);
    await c.query('COMMIT');
  } catch (e) {
    await c.query('ROLLBACK').catch(() => {});
    throw e;
  } finally { c.release(); }

  for (const m of miembros) await actualizarPlanDerivado(m);
  return { ok: true, stripeCancelada, googlePlay };
}
