import type { FastifyInstance, FastifyReply } from 'fastify';
import { z } from 'zod';
import { requiereAdmin } from '../lib/auth.js';
import {
  AjustesEntrada, actualizarPlan, ajustesPago, archivarPlan, borrarPlan, crearPlan, ErrorPlan, guardarAjustes, listarPlanesAdmin,
  PlanCambios, PlanEntrada, planesPublicos, sincronizarPlan,
} from '../lib/pagos/planes.js';

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

  app.get('/admin/pagos/ajustes', { preHandler: requiereAdmin }, async () => ajustesPago());
  app.put('/admin/pagos/ajustes', { preHandler: requiereAdmin }, async (req) => guardarAjustes(AjustesEntrada.parse(req.body)));
}
