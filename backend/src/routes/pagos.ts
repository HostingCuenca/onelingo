import type { FastifyInstance, FastifyReply } from 'fastify';
import { z } from 'zod';
import { requiereAdmin, requiereAlumno, type Sesion } from '../lib/auth.js';
import { uno } from '../lib/db.js';
import { stripeConfig } from '../lib/conexiones.js';
import { idPortal, plan, precioParaCheckout, sincronizarPlan } from '../lib/pagos/planes.js';
import { proveedorActivo } from '../lib/pagos/proveedor.js';
import { ErrorStripe, verificarFirma } from '../lib/pagos/stripe.js';
import {
  cambiarIdiomas, CODIGOS_IDIOMA, darCortesia, ErrorSus, errorIdiomas, filaDe, FILTROS_ESTADO, quitarCortesia, refrescarGoogle, resumenAdmin,
  sincronizarDesdeGoogle, sincronizarDesdeStripe, suscripcionDe, tieneAcceso,
} from '../lib/pagos/suscripciones.js';
import { ErrorGoogle, googleConfig, googleDisponible, tokenDeRtdn, tokenRtdnValido } from '../lib/pagos/google.js';
import { procesarWebhook } from '../lib/pagos/webhook.js';
import { familiaDe, invitarMiembro, quitarMiembro, salirDeFamilia, vincularInvitaciones } from '../lib/pagos/familia.js';

const SIN_PAGOS = { error: 'Los pagos aún no están disponibles (Stripe no está vinculado).' };
const EN_CURSO = ['activa', 'prueba_stripe', 'impago'];
const Idiomas = z.array(z.string().max(10)).max(10);
const conErrorSus = async (reply: FastifyReply, fn: () => Promise<unknown>) => {
  try { return await fn(); } catch (e) { if (e instanceof ErrorSus) return reply.code(e.status).send({ error: e.message, ...e.extra }); throw e; }
};
const errorProveedor = (e: unknown) => ({ error: `Stripe: ${e instanceof Error ? e.message : String(e)}`.slice(0, 400) });

/**
 * Suscripciones del alumno, Checkout, Customer Portal, webhook de Stripe, compras
 * de Google Play (verificación y RTDN) y suscripciones/cortesías en el panel
 * (docs/PANEL_ADMIN.md → «Planes y suscripciones» y «Google Play»).
 */
export default async function rutas(app: FastifyInstance) {
  // ── Alumno ─────────────────────────────────────────────────────────────────
  app.get('/usuarios/me/suscripcion', { preHandler: requiereAlumno }, async (req) => {
    const uid = (req.user as Sesion).sub;
    await vincularInvitaciones(uid); // invitación a un plan familiar hecha antes de que tuviera cuenta
    await refrescarGoogle(uid).catch((e) => req.log.warn({ err: String(e?.message ?? e) }, 'no se pudo refrescar la compra de Google Play'));
    return suscripcionDe(uid);
  });

  // Plan familiar: el titular añade o quita personas por correo; un miembro puede salir.
  const Correo = z.object({ email: z.string().trim().email('Correo no válido').max(200) });
  app.get('/usuarios/me/familia', { preHandler: requiereAlumno }, async (req) => familiaDe((req.user as Sesion).sub));
  app.post('/usuarios/me/familia', { preHandler: requiereAlumno }, async (req, reply) =>
    conErrorSus(reply, () => invitarMiembro((req.user as Sesion).sub, Correo.parse(req.body).email)));
  app.post('/usuarios/me/familia/quitar', { preHandler: requiereAlumno }, async (req, reply) =>
    conErrorSus(reply, () => quitarMiembro((req.user as Sesion).sub, Correo.parse(req.body).email)));
  app.post('/usuarios/me/familia/salir', { preHandler: requiereAlumno }, async (req, reply) =>
    conErrorSus(reply, () => salirDeFamilia((req.user as Sesion).sub)));

  /** Cambiar o completar los idiomas del plan (regla `cambioIdiomas`; 403 con `proximoCambio` si no toca). */
  app.put('/usuarios/me/suscripcion/idiomas', { preHandler: requiereAlumno }, async (req, reply) => {
    const { idiomas } = z.object({ idiomas: Idiomas }).parse(req.body);
    return conErrorSus(reply, () => cambiarIdiomas((req.user as Sesion).sub, idiomas));
  });

  app.post('/pagos/checkout', { preHandler: requiereAlumno }, async (req, reply) => {
    const uid = (req.user as Sesion).sub;
    const { planId, idiomas: elegidos, meses } = z.object({ planId: z.string().min(1).max(40), idiomas: Idiomas.default([]), meses: z.number().int().min(1).max(24).default(1) }).parse(req.body);
    const idiomas = elegidos.map((c) => c.trim().toLowerCase());
    const p = proveedorActivo();
    if (!p) return reply.code(503).send(SIN_PAGOS);
    const f = await filaDe(uid);
    if (f?.origen === 'stripe' && EN_CURSO.includes(f.estado)) return reply.code(409).send({ error: 'Ya tienes una suscripción activa: gestiónala desde el portal.', portal: true });
    if (f?.origen === 'google' && (tieneAcceso(f) || f.estado === 'impago')) return reply.code(409).send({ error: 'Ya tienes una suscripción de Google Play: gestiónala desde la app en Android.' });
    let pl = await plan(planId);
    if (!pl || pl.archivado || !pl.visible) return reply.code(404).send({ error: 'Ese plan no está disponible.' });
    const malIdiomas = errorIdiomas(idiomas, Number(pl.idiomas), { exactos: true });
    if (malIdiomas) return reply.code(400).send({ error: malIdiomas });
    if (meses > 1 && !pl.duraciones.some((d) => d.meses === meses)) return reply.code(400).send({ error: `Este plan no se ofrece por ${meses} meses.` });
    let precioId = pl.stripe_sincronizado ? await precioParaCheckout(pl, meses, p.modo()!) : null;
    if (!precioId) {
      await sincronizarPlan(planId);
      pl = await plan(planId);
      precioId = pl ? await precioParaCheckout(pl, meses, p.modo()!) : null;
      if (!precioId) return reply.code(503).send({ error: 'El plan no está sincronizado con Stripe. Inténtalo más tarde.' });
    }
    const u = await uno<{ email: string }>('SELECT email FROM usuarios WHERE id = $1', [uid]);
    if (!u) return reply.code(404).send({ error: 'Usuario no encontrado' });
    const urlApp = stripeConfig().urlApp;
    try {
      const url = await p.crearCheckout({
        usuarioId: uid, email: u.email, clienteId: f?.stripe_cliente_id && f.modo === p.modo() ? f.stripe_cliente_id : null, plan: pl!, precioId, meses, idiomas,
        exito: `${urlApp}/#/pago?estado=ok&session_id={CHECKOUT_SESSION_ID}`, cancelar: `${urlApp}/#/pago?estado=cancelado`,
      });
      return { url };
    } catch (e) { req.log.warn({ err: e instanceof ErrorStripe ? e.message : String(e) }, 'checkout falló'); return reply.code(502).send(errorProveedor(e)); }
  });

  /** Respaldo del webhook (que en local no llega): consulta la sesión y sincroniza. */
  app.post('/pagos/confirmar', { preHandler: requiereAlumno }, async (req, reply) => {
    const uid = (req.user as Sesion).sub;
    const { sessionId } = z.object({ sessionId: z.string().regex(/^cs_[A-Za-z0-9_]{6,250}$/, 'Id de sesión de Checkout no válido') }).parse(req.body);
    const p = proveedorActivo();
    if (!p) return reply.code(503).send(SIN_PAGOS);
    let c;
    try { c = await p.obtenerCheckout(sessionId); } catch (e) { return reply.code(e instanceof ErrorStripe && e.status === 404 ? 404 : 502).send(errorProveedor(e)); }
    if (c.usuarioId !== uid) return reply.code(403).send({ error: 'Esta sesión de pago no es tuya.' });
    if (c.completada && c.suscripcion) await sincronizarDesdeStripe(c.suscripcion, { usuarioId: uid, idiomas: c.idiomas });
    return suscripcionDe(uid);
  });

  app.post('/pagos/portal', { preHandler: requiereAlumno }, async (req, reply) => {
    const uid = (req.user as Sesion).sub;
    const p = proveedorActivo();
    if (!p) return reply.code(503).send(SIN_PAGOS);
    const f = await filaDe(uid);
    if (!f?.stripe_cliente_id || f.modo !== p.modo()) return reply.code(409).send({ error: 'No tienes una suscripción de Stripe que gestionar.' });
    // Configuración de OneLingo (cambio de plan entre los planes visibles); sin ella, la por defecto de la cuenta.
    const configuracion = await idPortal().catch(() => null);
    try { return { url: await p.crearPortal(f.stripe_cliente_id, `${stripeConfig().urlApp}/#/pago?estado=portal`, configuracion) }; }
    catch (e) { return reply.code(502).send(errorProveedor(e)); }
  });

  // ── Google Play ────────────────────────────────────────────────────────────
  /**
   * La app Android compró una suscripción: el servidor consulta la compra en Google,
   * la guarda con los idiomas elegidos y la reconoce. Solo si responde 200 la app
   * completa la compra (si nadie la reconoce en 3 días, Google la reembolsa).
   */
  app.post('/pagos/google/verificar', { preHandler: requiereAlumno }, async (req, reply) => {
    const uid = (req.user as Sesion).sub;
    const { token, idiomas } = z.object({
      token: z.string().min(10).max(4096).regex(/^[A-Za-z0-9._:-]+$/, 'Token de compra no válido'), idiomas: Idiomas.default([]),
    }).parse(req.body);
    if (!googleDisponible()) return reply.code(503).send({ error: 'Los pagos con Google Play aún no están disponibles.' });
    try {
      const r = await sincronizarDesdeGoogle(token, { usuarioId: uid, idiomas: idiomas.map((c) => c.trim().toLowerCase()) });
      if (!r.aplicada) return reply.code(409).send({ error: 'La compra no está activa.', motivo: r.motivo });
    } catch (e) {
      if (e instanceof ErrorSus) return reply.code(e.status).send({ error: e.message });
      if (e instanceof ErrorGoogle && (e.status === 404 || e.status === 410 || e.status === 400)) return reply.code(404).send({ error: 'Google Play no reconoce esta compra.' });
      req.log.warn({ err: e instanceof Error ? e.message : String(e) }, 'verificar compra de Google Play falló');
      return reply.code(502).send({ error: `Google Play: ${e instanceof Error ? e.message : String(e)}`.slice(0, 400) });
    }
    return suscripcionDe(uid);
  });

  /**
   * Notificaciones en tiempo real (RTDN) de Google Play: push de Pub/Sub a
   * `/pagos/google/rtdn?token=<GOOGLE_PLAY_RTDN_TOKEN>`. Se vuelve a consultar la
   * compra en Google (el aviso solo dice cuál cambió). Un 5xx hace que Pub/Sub reintente.
   */
  app.post('/pagos/google/rtdn', async (req, reply) => {
    const { token: secreto } = z.object({ token: z.string().max(200).default('') }).parse(req.query ?? {});
    if (!tokenRtdnValido(secreto)) return reply.code(403).send({ error: 'Token no válido' });
    const n = tokenDeRtdn(req.body, googleConfig().paquete);
    if (!n.token) return { recibido: true, ignorado: n.motivo };
    try {
      const r = await sincronizarDesdeGoogle(n.token);
      return { recibido: true, aplicada: r.aplicada, ...(r.aplicada ? { estado: (r as any).estado } : { motivo: (r as any).motivo }) };
    } catch (e) {
      if (e instanceof ErrorGoogle && (e.status === 404 || e.status === 410)) return { recibido: true, ignorado: 'compra desconocida' };
      req.log.error({ err: e instanceof Error ? e.message : String(e) }, 'RTDN de Google Play: error al procesar');
      return reply.code(500).send({ error: 'No se pudo procesar; Pub/Sub lo reintentará.' });
    }
  });

  // ── Webhook (cuerpo crudo: parser propio solo en este contexto) ────────────
  await app.register(async (w) => {
    w.removeContentTypeParser('application/json');
    w.addContentTypeParser('application/json', { parseAs: 'buffer', bodyLimit: 1024 * 1024 }, (_req, cuerpo, hecho) => hecho(null, cuerpo));
    w.post('/stripe/webhook', async (req, reply) => {
      const secreto = stripeConfig().webhookSecret;
      if (!secreto) return reply.code(503).send({ error: 'Webhook de Stripe no configurado' });
      const cuerpo = req.body;
      if (!Buffer.isBuffer(cuerpo)) return reply.code(400).send({ error: 'Se esperaba JSON' });
      const f = verificarFirma(cuerpo, req.headers['stripe-signature'] as string | undefined, secreto);
      if (!f.ok) return reply.code(400).send({ error: `Firma no válida (${f.motivo})` });
      let ev: any;
      try { ev = JSON.parse(cuerpo.toString('utf8')); } catch { return reply.code(400).send({ error: 'JSON no válido' }); }
      const r = await procesarWebhook(ev);
      if (r.status >= 500) req.log.error({ evento: ev.id, tipo: ev.type }, 'webhook de Stripe: error al procesar');
      return reply.code(r.status).send(r.cuerpo);
    });
  });

  // ── Panel ──────────────────────────────────────────────────────────────────
  app.get('/admin/suscripciones', { preHandler: requiereAdmin }, async (req) => {
    const f = z.object({ estado: z.enum(FILTROS_ESTADO).default(''), q: z.string().max(200).default(''), idioma: z.enum(['', ...CODIGOS_IDIOMA]).default('') }).parse(req.query);
    return resumenAdmin(f);
  });

  const uid = (p: unknown) => z.object({ id: z.string().uuid() }).parse(p).id;
  app.post('/admin/usuarios/:id/cortesia', { preHandler: requiereAdmin }, async (req, reply) => {
    const d = z.object({
      planId: z.string().min(1).max(40), idiomas: z.union([Idiomas, z.literal('todos')]).optional(),
      hasta: z.string().datetime({ offset: true }).nullable().optional(), nota: z.string().max(500).default(''),
    }).parse(req.body);
    return conErrorSus(reply, () => darCortesia(uid(req.params), d));
  });
  /** El administrador edita los idiomas: sin la regla de cambios, pero con el número de idiomas del plan. */
  app.put('/admin/usuarios/:id/suscripcion/idiomas', { preHandler: requiereAdmin }, async (req, reply) => {
    const { idiomas } = z.object({ idiomas: Idiomas }).parse(req.body);
    return conErrorSus(reply, () => cambiarIdiomas(uid(req.params), idiomas, { admin: true }));
  });
  app.delete('/admin/usuarios/:id/cortesia', { preHandler: requiereAdmin }, async (req, reply) => {
    return conErrorSus(reply, () => quitarCortesia(uid(req.params)));
  });
}
