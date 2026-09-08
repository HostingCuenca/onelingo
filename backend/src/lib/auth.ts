import type { FastifyReply, FastifyRequest } from 'fastify';
export type Sesion = { sub: string; rol: 'alumno' | 'admin' };
export async function requiereAlumno(req: FastifyRequest, reply: FastifyReply) {
  try { await req.jwtVerify(); } catch { return reply.code(401).send({ error: 'Sesión inválida' }); }
  const s = req.user as Sesion;
  if (s.rol !== 'alumno') return reply.code(403).send({ error: 'Solo alumnos' });
}
export async function requiereAdmin(req: FastifyRequest, reply: FastifyReply) {
  try { await req.jwtVerify(); } catch { return reply.code(401).send({ error: 'Sesión inválida' }); }
  const s = req.user as Sesion;
  if (s.rol !== 'admin') return reply.code(403).send({ error: 'Solo administradores' });
}
