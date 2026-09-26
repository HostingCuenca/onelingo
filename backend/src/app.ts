import Fastify from 'fastify';
import cors from '@fastify/cors';
import jwt from '@fastify/jwt';
import sensible from '@fastify/sensible';
import formbody from '@fastify/formbody';
import multipart from '@fastify/multipart';
import { ZodError } from 'zod';
import { config } from './lib/config.js';
import { pool } from './lib/db.js';
import rutasUsuarios from './routes/usuarios.js';
import rutasAdmin from './routes/admin.js';
import rutasAuth from './routes/auth.js';
import rutasChat from './routes/chat.js';
import rutasVoz from './routes/voz.js';
import rutasDiagnostico from './routes/diagnostico.js';

export async function crearApp() {
  const app = Fastify({ logger: { level: process.env.LOG_LEVEL ?? 'info' }, bodyLimit: 2 * 1024 * 1024 });
  await app.register(cors, { origin: true, methods: ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'] });
  await app.register(sensible);
  await app.register(formbody);
  await app.register(multipart, { limits: { fileSize: 15 * 1024 * 1024, files: 1 } });
  await app.register(jwt, { secret: config.jwtSecret });
  app.setErrorHandler((err: any, req, reply) => {
    if (err instanceof ZodError) return reply.code(400).send({ error: 'Datos inválidos', detalles: err.issues.map((i) => `${i.path.join('.')}: ${i.message}`) });
    const status = err.statusCode ?? 500;
    if (status >= 500) req.log.error(err);
    return reply.code(status).send({ error: status >= 500 ? 'Error interno' : err.message });
  });
  app.get('/salud', async () => { await pool.query('SELECT 1'); return { ok: true, hora: new Date().toISOString() }; });
  await app.register(rutasUsuarios);
  await app.register(rutasAuth);
  await app.register(rutasChat);
  await app.register(rutasVoz);
  await app.register(rutasDiagnostico);
  await app.register(rutasAdmin);
  return app;
}
