/**
 * Referidos (solo seguimiento): el admin crea un código por vendedor; el alumno
 * lo escribe al registrarse o después, una sola vez; el panel muestra quién
 * trajo a quién y cuántos pagan. No da descuentos ni premios: qué hacer con
 * esa información lo decide el admin.
 */
import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { query, uno } from '../lib/db.js';
import { requiereAdmin, requiereAlumno, type Sesion } from '../lib/auth.js';
import { idiomaDe } from '../lib/codigos.js';

/** «ana lopez 2» → «ANA-LOPEZ-2»; sin tildes ni símbolos. */
export const normalizarCodigo = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toUpperCase().trim()
  .replace(/[\s_]+/g, '-').replace(/[^A-Z0-9-]/g, '').replace(/-+/g, '-').replace(/^-|-$/g, '').slice(0, 20);
const Codigo = z.string().transform(normalizarCodigo).pipe(z.string().regex(/^[A-Z0-9-]{3,20}$/, 'El código debe tener de 3 a 20 letras, números o guiones'));

const T = {
  invalido: { es: 'Ese código no existe o ya no está activo. Revísalo con quien te lo dio.', en: 'That code does not exist or is no longer active. Check it with whoever gave it to you.' },
  yaTiene: { es: 'Tu cuenta ya tiene un código de referido.', en: 'Your account already has a referral code.' },
};

/** Pagando = suscripción activa de pago (Stripe o Google Play), no cortesía ni familia. */
const PAGANDO = `s.estado IN ('activa', 'prueba_stripe') AND s.origen IN ('stripe', 'google')`;

export default async function rutas(app: FastifyInstance) {
  /** La app lo comprueba antes de crear la cuenta, para avisar si está mal escrito. */
  app.get('/referidos/validar', async (req) => {
    const r = Codigo.safeParse((req.query as any)?.codigo ?? '');
    if (!r.success) return { valido: false };
    return { valido: !!(await uno('SELECT 1 FROM referidos WHERE codigo = $1 AND activo', [r.data])), codigo: r.data };
  });

  app.get('/usuarios/me/referido', { preHandler: requiereAlumno }, async (req) => {
    const s = req.user as Sesion;
    const u = await uno<{ referido_codigo: string | null }>('SELECT referido_codigo FROM usuarios WHERE id = $1', [s.sub]);
    return { codigo: u?.referido_codigo ?? null };
  });

  /** Una sola vez por cuenta: luego solo el admin puede cambiarlo. */
  app.post('/usuarios/me/referido', { preHandler: requiereAlumno }, async (req, reply) => {
    const s = req.user as Sesion, en = idiomaDe(req);
    const r = Codigo.safeParse((req.body as any)?.codigo ?? '');
    if (!r.success) return reply.code(400).send({ error: T.invalido[en] });
    if (!(await uno('SELECT 1 FROM referidos WHERE codigo = $1 AND activo', [r.data]))) return reply.code(404).send({ error: T.invalido[en] });
    const u = await uno('UPDATE usuarios SET referido_codigo = $2, referido_en = now() WHERE id = $1 AND referido_codigo IS NULL RETURNING id', [s.sub, r.data]);
    if (!u) return reply.code(409).send({ error: T.yaTiene[en] });
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1,$2,$3)', [s.sub, 'referido', JSON.stringify({ codigo: r.data })]);
    return { codigo: r.data };
  });

  /** Códigos con sus números: registrados, pagando ahora e ingreso mensual estimado. */
  app.get('/admin/referidos', { preHandler: requiereAdmin }, async () => {
    const codigos = await query(`SELECT r.codigo, r.vendedor, r.nota, r.activo, r.creado_en AS "creadoEn",
        count(u.id)::int AS registrados,
        count(u.id) FILTER (WHERE ${PAGANDO})::int AS pagando,
        count(u.id) FILTER (WHERE s.usuario_id IS NOT NULL AND s.origen IN ('stripe', 'google'))::int AS "pagaronAlgunaVez",
        coalesce(sum(CASE WHEN ${PAGANDO} THEN CASE s.intervalo WHEN 'anio' THEN s.importe_centavos / 12.0 ELSE s.importe_centavos END END), 0)::float / 100 AS "mensual",
        max(u.referido_en) AS "ultimo"
      FROM referidos r LEFT JOIN usuarios u ON u.referido_codigo = r.codigo LEFT JOIN suscripciones s ON s.usuario_id = u.id
      GROUP BY r.codigo ORDER BY r.activo DESC, registrados DESC, r.creado_en DESC`);
    const sinCodigo = await uno<{ n: number }>('SELECT count(*)::int AS n FROM usuarios WHERE referido_codigo IS NULL AND NOT es_demo');
    return { codigos, sinCodigo: sinCodigo?.n ?? 0 };
  });

  /** Alumnos que trajo un código. */
  app.get('/admin/referidos/:codigo', { preHandler: requiereAdmin }, async (req, reply) => {
    const codigo = normalizarCodigo((req.params as any).codigo ?? '');
    const r = await uno('SELECT codigo, vendedor, nota, activo, creado_en AS "creadoEn" FROM referidos WHERE codigo = $1', [codigo]);
    if (!r) return reply.code(404).send({ error: 'No existe ese código' });
    const alumnos = await query(`SELECT u.id, u.nombre, u.apellido, u.email, u.idioma_meta AS "idiomaMeta", u.creado_en AS "registro", u.referido_en AS "referidoEn",
        s.plan_id AS plan, s.origen, s.estado, (${PAGANDO}) AS pagando
      FROM usuarios u LEFT JOIN suscripciones s ON s.usuario_id = u.id WHERE u.referido_codigo = $1 ORDER BY u.referido_en DESC NULLS LAST LIMIT 500`, [codigo]);
    return { ...r, alumnos };
  });

  app.post('/admin/referidos', { preHandler: requiereAdmin }, async (req, reply) => {
    const d = z.object({ codigo: z.string().default(''), vendedor: z.string().trim().min(1, 'Escribe el nombre del vendedor').max(80), nota: z.string().trim().max(300).default('') }).parse(req.body);
    const codigo = Codigo.safeParse(d.codigo || d.vendedor);
    if (!codigo.success) return reply.code(400).send({ error: codigo.error.issues[0].message });
    const r = await uno('INSERT INTO referidos (codigo, vendedor, nota) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING RETURNING codigo', [codigo.data, d.vendedor, d.nota]);
    if (!r) return reply.code(409).send({ error: `Ya existe el código ${codigo.data}` });
    return reply.code(201).send({ codigo: codigo.data });
  });

  app.patch('/admin/referidos/:codigo', { preHandler: requiereAdmin }, async (req, reply) => {
    const codigo = normalizarCodigo((req.params as any).codigo ?? '');
    const d = z.object({ vendedor: z.string().trim().min(1).max(80).optional(), nota: z.string().trim().max(300).optional(), activo: z.boolean().optional() }).parse(req.body);
    const r = await uno(`UPDATE referidos SET vendedor = coalesce($2, vendedor), nota = coalesce($3, nota), activo = coalesce($4, activo) WHERE codigo = $1 RETURNING codigo`,
      [codigo, d.vendedor ?? null, d.nota ?? null, d.activo ?? null]);
    if (!r) return reply.code(404).send({ error: 'No existe ese código' });
    return { ok: true };
  });

  /** El admin asigna o quita el código de un alumno (p. ej. si el vendedor lo avisa después). */
  app.put('/admin/usuarios/:id/referido', { preHandler: requiereAdmin }, async (req, reply) => {
    const { id } = z.object({ id: z.string().uuid() }).parse(req.params);
    const bruto = (req.body as any)?.codigo;
    const codigo = bruto ? normalizarCodigo(String(bruto)) : null;
    if (codigo && !(await uno('SELECT 1 FROM referidos WHERE codigo = $1', [codigo]))) return reply.code(404).send({ error: 'No existe ese código' });
    const u = await uno('UPDATE usuarios SET referido_codigo = $2, referido_en = CASE WHEN $2::text IS NULL THEN NULL ELSE now() END WHERE id = $1 RETURNING id', [id, codigo]);
    if (!u) return reply.code(404).send({ error: 'No existe el alumno' });
    return { codigo };
  });
}
