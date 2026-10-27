import type { FastifyInstance, FastifyReply } from 'fastify';
import { z } from 'zod';
import { requiereAdmin } from '../lib/auth.js';
import {
  AjustesEntrada, actualizarPlan, ajustesPago, archivarPlan, borrarPlan, crearPlan, ErrorPlan, guardarAjustes, listarPlanesAdmin,
  PlanCambios, PlanEntrada, planesPublicos, sincronizarPlan,
} from '../lib/pagos/planes.js';
import { actualizarCotizacion, CotizacionCambios, CotizacionEntrada, crearCotizacion, ESTADOS_COTIZACION, listarCotizaciones } from '../lib/pagos/cotizaciones.js';
import type { Sesion } from '../lib/auth.js';

/** Límite simple por IP para el formulario público de cotización: 5 por hora. */
const envios = new Map<string, number[]>();
const demasiados = (ip: string, ahora = Date.now()) => {
  const l = (envios.get(ip) ?? []).filter((t) => ahora - t < 3_600_000);
  if (l.length >= 5) return true;
  l.push(ahora); envios.set(ip, l);
  if (envios.size > 5000) envios.clear();
  return false;
};

/** Planes: catálogo público y edición desde el panel (docs/PANEL_ADMIN.md → «Planes y suscripciones»). */
export default async function rutas(app: FastifyInstance) {
  const id = (p: unknown) => z.object({ id: z.string().min(1).max(40) }).parse(p).id;
  const conError = async (reply: FastifyReply, fn: () => Promise<unknown>) => {
    try { return await fn(); } catch (e) { if (e instanceof ErrorPlan) return reply.code(e.status).send({ error: e.message }); throw e; }
  };

  /** Pública: sin sesión. Solo planes visibles y no archivados, por `orden`. */
  app.get('/planes', async () => planesPublicos());

  app.get('/admin/planes', { preHandler: requiereAdmin }, async () => listarPlanesAdmin());
  app.post('/admin/planes', { preHandler: requiereAdmin }, async (req, reply) =>
    conError(reply, async () => reply.code(201).send(await crearPlan(PlanEntrada.parse(req.body)))));
  app.put('/admin/planes/:id', { preHandler: requiereAdmin }, async (req, reply) =>
    conError(reply, () => actualizarPlan(id(req.params), PlanCambios.parse(req.body))));
  app.post('/admin/planes/:id/archivar', { preHandler: requiereAdmin }, async (req, reply) =>
    conError(reply, () => archivarPlan(id(req.params), z.object({ archivado: z.boolean().default(true) }).parse(req.body ?? {}).archivado)));
  app.post('/admin/planes/:id/sincronizar', { preHandler: requiereAdmin }, async (req, reply) => conError(reply, () => sincronizarPlan(id(req.params))));
  app.delete('/admin/planes/:id', { preHandler: requiereAdmin }, async (req, reply) => conError(reply, () => borrarPlan(id(req.params))));

  /** Plan Empresarial: con o sin sesión (si la hay, se guarda quién la pidió). */
  app.post('/cotizaciones', async (req, reply) => {
    const d = CotizacionEntrada.parse(req.body);
    // Detrás de Apache, `req.ip` es el proxy: la IP del cliente va en X-Forwarded-For.
    if (demasiados(String(req.headers['x-forwarded-for'] ?? req.ip).split(',')[0].trim())) return reply.code(429).send({ error: 'Demasiadas solicitudes. Inténtalo más tarde.' });
    let uid: string | null = null;
    try { await req.jwtVerify(); const s = req.user as Sesion; if (s.rol === 'alumno') uid = s.sub; } catch { /* sin sesión */ }
    return reply.code(201).send(await crearCotizacion(d, uid));
  });
  app.get('/admin/cotizaciones', { preHandler: requiereAdmin }, async (req) =>
    listarCotizaciones(z.object({ estado: z.enum(['', ...ESTADOS_COTIZACION]).default('') }).parse(req.query).estado));
  app.put('/admin/cotizaciones/:id', { preHandler: requiereAdmin }, async (req, reply) => {
    const { id: n } = z.object({ id: z.coerce.number().int().positive() }).parse(req.params);
    const r = await actualizarCotizacion(n, CotizacionCambios.parse(req.body));
    return r ? { ok: true } : reply.code(404).send({ error: 'La solicitud no existe.' });
  });

  app.get('/admin/pagos/ajustes', { preHandler: requiereAdmin }, async () => ajustesPago());
  app.put('/admin/pagos/ajustes', { preHandler: requiereAdmin }, async (req) => guardarAjustes(AjustesEntrada.parse(req.body)));
}
