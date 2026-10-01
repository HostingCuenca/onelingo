import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { query } from '../lib/db.js';
import { revisarEscritura } from '../lib/ia.js';
import { openaiDisponible } from '../lib/ia_openai.js';
import { requiereAlumno, type Sesion } from '../lib/auth.js';

export default async function rutas(app: FastifyInstance) {
  /** Revisión con IA de una respuesta escrita de la ruta (frases y producción abierta). */
  app.post('/ejercicios/revisar', { preHandler: requiereAlumno }, async (req, reply) => {
    if (!openaiDisponible()) return reply.code(503).send({ error: 'ia_no_configurada' });
    const s = req.user as Sesion;
    const d = z.object({
      idiomaMeta: z.string().max(5), idiomaNativo: z.string().max(5).default('es'), nivel: z.number().min(0).max(10).default(3),
      itemId: z.string().max(160).optional(), consigna: z.string().max(500), texto: z.string().max(800).default(''),
      modelo: z.string().max(800).default(''), aceptadas: z.array(z.string().max(800)).max(12).default([]),
      respuesta: z.string().min(1).max(1500), abierta: z.boolean().default(false),
    }).parse(req.body);
    try {
      const r = await revisarEscritura(d);
      await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)', [s.sub, 'revision_escritura', JSON.stringify({ idioma: d.idiomaMeta, itemId: d.itemId, abierta: d.abierta, correcta: r.correcta })]).catch(() => {});
      return r;
    } catch (e) {
      req.log.error({ err: String(e) }, 'revision_escritura');
      return reply.code(502).send({ error: 'revision_error' });
    }
  });
}
