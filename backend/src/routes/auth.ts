import type { FastifyInstance } from 'fastify';
import { randomBytes } from 'node:crypto';
import bcrypt from 'bcryptjs';
import { OAuth2Client } from 'google-auth-library';
import { z } from 'zod';
import { config } from '../lib/config.js';
import { enviarCorreo, plantilla } from '../lib/correo.js';
import { query, uno } from '../lib/db.js';
import { requiereAlumno, type Sesion } from '../lib/auth.js';

const google = new OAuth2Client();
const tokenDe = (app: FastifyInstance, id: string) => app.jwt.sign({ sub: id, rol: 'alumno' } satisfies Sesion);

export default async function rutas(app: FastifyInstance) {
  /** Registro con correo y contraseña. Devuelve sesión y envía correo de verificación. */
  app.post('/auth/registro', async (req, reply) => {
    const d = z.object({
      email: z.string().email(), password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres'), nombre: z.string().min(1),
      idiomaNativo: z.string().default('es'), idiomaMeta: z.string().default('en'), nivelInicial: z.number().int().min(1).max(10).default(1), plataforma: z.string().default(''),
    }).parse(req.body);
    const email = d.email.toLowerCase();
    const existe = await uno('SELECT id, password_hash, google_id FROM usuarios WHERE email = $1', [email]);
    if (existe && (existe.password_hash || existe.google_id)) return reply.code(409).send({ error: 'Ya existe una cuenta con ese correo. Inicia sesión.' });
    const hash = await bcrypt.hash(d.password, 10);
    const tokenVerif = randomBytes(24).toString('hex');
    const u = existe
      ? await uno('UPDATE usuarios SET password_hash=$2, nombre=$3, idioma_nativo=$4, idioma_meta=$5, nivel_inicial=$6, plataforma=$7, token_verificacion=$8, es_demo=false, ultima_actividad=now() WHERE id=$1 RETURNING id', [existe.id, hash, d.nombre, d.idiomaNativo, d.idiomaMeta, d.nivelInicial, d.plataforma, tokenVerif])
      : await uno('INSERT INTO usuarios (email, nombre, idioma_nativo, idioma_meta, nivel_inicial, plataforma, trial_inicio, password_hash, token_verificacion) VALUES ($1,$2,$3,$4,$5,$6, now(), $7, $8) RETURNING id', [email, d.nombre, d.idiomaNativo, d.idiomaMeta, d.nivelInicial, d.plataforma, hash, tokenVerif]);
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1,$2,$3)', [u!.id, 'registro', JSON.stringify({ metodo: 'password', idiomaMeta: d.idiomaMeta })]);
    const url = `${config.publicUrl}/auth/verificar?token=${tokenVerif}`;
    await enviarCorreo(email, 'Confirma tu correo en OneLingo', plantilla(`¡Hola, ${d.nombre}!`, 'Gracias por registrarte. Confirma tu correo para proteger tu cuenta y recuperar tu contraseña si la olvidas.', { texto: 'Confirmar correo', url }));
    return reply.code(201).send({ id: u!.id, token: tokenDe(app, u!.id), verificado: false });
  });

  app.get('/auth/verificar', async (req, reply) => {
    const { token } = z.object({ token: z.string() }).parse(req.query);
    const u = await uno('UPDATE usuarios SET email_verificado = true, token_verificacion = NULL WHERE token_verificacion = $1 RETURNING nombre', [token]);
    reply.type('text/html');
    return plantilla(u ? `Correo confirmado, ${u.nombre}` : 'Enlace no válido', u ? 'Ya puedes volver a la app de OneLingo.' : 'Este enlace ya se usó o ha caducado.');
  });

  /** Inicio de sesión con correo y contraseña. Devuelve el progreso guardado en el servidor. */
  app.post('/auth/login', async (req, reply) => {
    const { email, password } = z.object({ email: z.string().email(), password: z.string() }).parse(req.body);
    const u = await uno('SELECT id, password_hash, es_demo FROM usuarios WHERE email = $1', [email.toLowerCase()]);
    if (!u || !u.password_hash || !(await bcrypt.compare(password, u.password_hash))) return reply.code(401).send({ error: 'Correo o contraseña incorrectos' });
    await query('UPDATE usuarios SET ultima_actividad = now() WHERE id = $1', [u.id]);
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1,$2,$3)', [u.id, 'login', JSON.stringify({ metodo: 'password' })]);
    const p = await uno('SELECT estado FROM progreso WHERE usuario_id = $1', [u.id]);
    return { id: u.id, token: tokenDe(app, u.id), estado: p?.estado ?? null };
  });

  /** Inicio de sesión con Google: la app manda el idToken; se verifica contra los client IDs configurados. */
  app.post('/auth/google', async (req, reply) => {
    const { idToken, idiomaNativo, idiomaMeta, nivelInicial, plataforma } = z.object({
      idToken: z.string(), idiomaNativo: z.string().default('es'), idiomaMeta: z.string().default('en'), nivelInicial: z.number().int().default(1), plataforma: z.string().default(''),
    }).parse(req.body);
    if (config.googleClientIds.length === 0) return reply.code(503).send({ error: 'Google Sign-In no está configurado en el servidor (GOOGLE_CLIENT_IDS)' });
    let payload;
    try {
      const ticket = await google.verifyIdToken({ idToken, audience: config.googleClientIds });
      payload = ticket.getPayload();
    } catch { return reply.code(401).send({ error: 'Token de Google no válido' }); }
    if (!payload?.email || !payload.sub) return reply.code(401).send({ error: 'Google no devolvió un correo' });
    const email = payload.email.toLowerCase();
    const nombre = payload.name ?? email.split('@')[0];
    const existe = await uno('SELECT id FROM usuarios WHERE google_id = $1 OR email = $2', [payload.sub, email]);
    const u = existe
      ? await uno('UPDATE usuarios SET google_id=$2, email_verificado=true, ultima_actividad=now() WHERE id=$1 RETURNING id', [existe.id, payload.sub])
      : await uno('INSERT INTO usuarios (email, nombre, idioma_nativo, idioma_meta, nivel_inicial, plataforma, trial_inicio, google_id, email_verificado) VALUES ($1,$2,$3,$4,$5,$6, now(), $7, true) RETURNING id', [email, nombre, idiomaNativo, idiomaMeta, nivelInicial, plataforma, payload.sub]);
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1,$2,$3)', [u!.id, existe ? 'login' : 'registro', JSON.stringify({ metodo: 'google' })]);
    const p = await uno('SELECT estado FROM progreso WHERE usuario_id = $1', [u!.id]);
    return { id: u!.id, token: tokenDe(app, u!.id), nombre, email, estado: p?.estado ?? null, nuevo: !existe };
  });

  app.post('/auth/recuperar', async (req) => {
    const { email } = z.object({ email: z.string().email() }).parse(req.body);
    const u = await uno('SELECT id, nombre FROM usuarios WHERE email = $1', [email.toLowerCase()]);
    if (u) {
      const token = randomBytes(24).toString('hex');
      await query("UPDATE usuarios SET token_reset=$2, reset_expira = now() + interval '1 hour' WHERE id=$1", [u.id, token]);
      await enviarCorreo(email, 'Restablece tu contraseña de OneLingo', plantilla(`Hola, ${u.nombre}`, 'Recibimos una solicitud para cambiar tu contraseña. El enlace vale una hora.', { texto: 'Cambiar contraseña', url: `${config.publicUrl}/auth/restablecer?token=${token}` }));
    }
    return { ok: true, mensaje: 'Si el correo existe, te enviamos un enlace para restablecer la contraseña.' };
  });

  app.get('/auth/restablecer', async (req, reply) => {
    const { token } = z.object({ token: z.string() }).parse(req.query);
    reply.type('text/html');
    return plantilla('Nueva contraseña', `<form method="post" action="${config.publicUrl}/auth/restablecer-form" style="display:flex;flex-direction:column;gap:10px;max-width:320px"><input type="hidden" name="token" value="${token}"/><input name="password" type="password" minlength="6" placeholder="Nueva contraseña" required style="padding:10px;border:1px solid #ddd;border-radius:8px"/><button style="background:#4519BB;color:#fff;border:0;padding:12px;border-radius:10px;font-weight:700">Guardar</button></form>`);
  });

  const restablecer = async (token: string, password: string) => {
    const u = await uno('SELECT id FROM usuarios WHERE token_reset = $1 AND reset_expira > now()', [token]);
    if (!u) return false;
    await query('UPDATE usuarios SET password_hash=$2, token_reset=NULL, reset_expira=NULL, email_verificado=true WHERE id=$1', [u.id, await bcrypt.hash(password, 10)]);
    return true;
  };
  app.post('/auth/restablecer', async (req, reply) => {
    const { token, password } = z.object({ token: z.string(), password: z.string().min(6) }).parse(req.body);
    if (!(await restablecer(token, password))) return reply.code(400).send({ error: 'El enlace no es válido o caducó' });
    return { ok: true };
  });
  app.post('/auth/restablecer-form', async (req, reply) => {
    const body = req.body as Record<string, string>;
    const ok = await restablecer(String(body.token ?? ''), String(body.password ?? ''));
    reply.type('text/html');
    return plantilla(ok ? 'Contraseña actualizada' : 'Enlace no válido', ok ? 'Ya puedes entrar en la app con tu nueva contraseña.' : 'Pide un enlace nuevo desde la app.');
  });

  /** Estado guardado en el servidor (para restaurar progreso en otro dispositivo). */
  app.get('/usuarios/me/progreso', { preHandler: requiereAlumno }, async (req) => {
    const s = req.user as Sesion;
    const p = await uno('SELECT estado, actualizado_en FROM progreso WHERE usuario_id = $1', [s.sub]);
    const u = await uno('SELECT email, nombre, email_verificado FROM usuarios WHERE id = $1', [s.sub]);
    return { estado: p?.estado ?? null, actualizado: p?.actualizado_en ?? null, usuario: u };
  });
}
