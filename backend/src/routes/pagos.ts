import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { requiereAdmin, requiereAlumno, type Sesion } from '../lib/auth.js';
import { uno } from '../lib/db.js';
import { stripeConfig } from '../lib/conexiones.js';
import { idPortal, plan, sincronizarPlan } from '../lib/pagos/planes.js';
import { proveedorActivo } from '../lib/pagos/proveedor.js';
import { ErrorStripe, verificarFirma } from '../lib/pagos/stripe.js';
import { darCortesia, ErrorSus, filaDe, FILTROS_ESTADO, quitarCortesia, resumenAdmin, sincronizarDesdeStripe, suscripcionDe } from '../lib/pagos/suscripciones.js';
import { procesarWebhook } from '../lib/pagos/webhook.js';

const SIN_PAGOS = { error: 'Los pagos aún no están disponibles (Stripe no está vinculado).' };
const EN_CURSO = ['activa', 'prueba_stripe', 'impago'];
const errorProveedor = (e: unknown) => ({ error: `Stripe: ${e instanceof Error ? e.message : String(e)}`.slice(0, 400) });

/**
 * Suscripciones del alumno, Checkout, Customer Portal, webhook de Stripe y
 * suscripciones/cortesías en el panel (docs/PANEL_ADMIN.md → «Planes y suscripciones»).
 */
export default async function rutas(app: FastifyInstance) {
  // ── Alumno ─────────────────────────────────────────────────────────────────
  app.get('/usuarios/me/suscripcion', { preHandler: requiereAlumno }, async (req) => suscripcionDe((req.user as Sesion).sub));

  app.post('/pagos/checkout', { preHandler: requiereAlumno }, async (req, reply) => {
    const uid = (req.user as Sesion).sub;
    const { planId } = z.object({ planId: z.string().min(1).max(40) }).parse(req.body);
    const p = proveedorActivo();
    if (!p) return reply.code(503).send(SIN_PAGOS);
    const f = await filaDe(uid);
    if (f?.origen === 'stripe' && EN_CURSO.includes(f.estado)) return reply.code(409).send({ error: 'Ya tienes una suscripción activa: gestiónala desde el portal.', portal: true });
    let pl = await plan(planId);
    if (!pl || pl.archivado || !pl.visible) return reply.code(404).send({ error: 'Ese plan no está disponible.' });
    if (!(pl.stripe_sincronizado && pl.stripe_modo === p.modo() && pl.stripe_precio_id)) {
      await sincronizarPlan(planId);
      pl = await plan(planId);
      if (!pl?.stripe_precio_id || pl.stripe_modo !== p.modo()) return reply.code(503).send({ error: 'El plan no está sincronizado con Stripe. Inténtalo más tarde.' });
    }
    const u = await uno<{ email: string }>('SELECT email FROM usuarios WHERE id = $1', [uid]);
    if (!u) return reply.code(404).send({ error: 'Usuario no encontrado' });
    const urlApp = stripeConfig().urlApp;
    try {
      const url = await p.crearCheckout({
        usuarioId: uid, email: u.email, clienteId: f?.stripe_cliente_id && f.modo === p.modo() ? f.stripe_cliente_id : null, plan: pl,
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
    if (c.completada && c.suscripcion) await sincronizarDesdeStripe(c.suscripcion, { usuarioId: uid });
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
    const f = z.object({ estado: z.enum(FILTROS_ESTADO).default(''), q: z.string().max(200).default('') }).parse(req.query);
    return resumenAdmin(f);
  });

  const uid = (p: unknown) => z.object({ id: z.string().uuid() }).parse(p).id;
  app.post('/admin/usuarios/:id/cortesia', { preHandler: requiereAdmin }, async (req, reply) => {
    const d = z.object({ planId: z.string().min(1).max(40), hasta: z.string().datetime({ offset: true }).nullable().optional(), nota: z.string().max(500).default('') }).parse(req.body);
    try { return await darCortesia(uid(req.params), d); } catch (e) { if (e instanceof ErrorSus) return reply.code(e.status).send({ error: e.message }); throw e; }
  });
  app.delete('/admin/usuarios/:id/cortesia', { preHandler: requiereAdmin }, async (req, reply) => {
    try { return await quitarCortesia(uid(req.params)); } catch (e) { if (e instanceof ErrorSus) return reply.code(e.status).send({ error: e.message }); throw e; }
  });
}
