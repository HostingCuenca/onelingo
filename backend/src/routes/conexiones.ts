import type { FastifyInstance, FastifyReply } from 'fastify';
import { requiereAdmin } from '../lib/auth.js';
import { consumo, eliminar, esProveedor, guardar, resumen, verificar } from '../lib/conexiones.js';

/**
 * Conexiones con ElevenLabs, OpenAI y Gemini desde el panel (docs/PANEL_ADMIN.md → «Conexiones»).
 * Ninguna respuesta lleva una clave completa; los cuerpos con claves no se registran.
 */
export default async function rutas(app: FastifyInstance) {
  const proveedor = (p: string, reply: FastifyReply) => {
    if (esProveedor(p)) return p;
    reply.code(404).send({ error: 'Proveedor desconocido (elevenlabs, openai o gemini).' });
    return null;
  };
  const cuerpo = (b: unknown) => (b && typeof b === 'object' && !Array.isArray(b) ? b as Record<string, unknown> : {});

  app.get('/admin/conexiones', { preHandler: requiereAdmin }, async () => resumen());
  app.get('/admin/conexiones/consumo', { preHandler: requiereAdmin }, async () => consumo());

  app.post('/admin/conexiones/:proveedor/verificar', { preHandler: requiereAdmin }, async (req, reply) => {
    const p = proveedor((req.params as any).proveedor, reply); if (!p) return reply;
    const r = await verificar(p, cuerpo(req.body));
    if (r.errores) return reply.code(400).send({ error: 'Revisa los campos marcados.', ...r });
    return r;
  });

  app.put('/admin/conexiones/:proveedor', { preHandler: requiereAdmin }, async (req, reply) => {
    const p = proveedor((req.params as any).proveedor, reply); if (!p) return reply;
    const r = await guardar(p, cuerpo(req.body));
    if (r.errores) return reply.code(400).send({ error: 'Revisa los campos marcados.', ...r });
    if (!r.ok) return reply.code(422).send({ error: r.verificacion?.mensaje ?? 'La verificación falló: no se guardó.', ...r });
    return { ...r, conexiones: resumen() };
  });

  app.delete('/admin/conexiones/:proveedor', { preHandler: requiereAdmin }, async (req, reply) => {
    const p = proveedor((req.params as any).proveedor, reply); if (!p) return reply;
    await eliminar(p);
    return { ok: true, conexiones: resumen() };
  });
}
