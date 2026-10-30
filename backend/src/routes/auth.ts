import type { FastifyInstance } from 'fastify';
import { randomBytes } from 'node:crypto';
import bcrypt from 'bcryptjs';
import { OAuth2Client } from 'google-auth-library';
import { z } from 'zod';
import { config } from '../lib/config.js';
import { enviarCorreo, esc, plantilla, plantillaCodigo } from '../lib/correo.js';
import { ErrorCodigo, emitirCodigo, idiomaDe, normalizarTelefono, verificarCodigo, type Txt } from '../lib/codigos.js';
import { query, uno } from '../lib/db.js';
import { requiereAlumno, type Sesion } from '../lib/auth.js';
import { planEfectivo } from '../lib/pagos/suscripciones.js';

/**
 * Estado guardado con el plan del servidor (autoridad del plan) y la prueba
 * usada que nunca baja (máximo entre lo guardado y `usuarios.trial_segundos`).
 */
async function estadoConPlan(usuarioId: string, estado: any) {
  if (!estado || typeof estado !== 'object') return estado ?? null;
  const u = await uno<{ trial_segundos: number }>('SELECT trial_segundos FROM usuarios WHERE id = $1', [usuarioId]);
  return { ...estado, planId: await planEfectivo(usuarioId), trialSegundos: Math.max(Number(estado.trialSegundos ?? 0) || 0, Number(u?.trial_segundos ?? 0)) };
}

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
    // Una cuenta antigua sin contraseña solo la reclama su dueño, con el enlace
    // de recuperación al correo; registrarse encima se la quitaba a cualquiera.
    if (existe && !email.endsWith('@onelingo.demo')) return reply.code(409).send({ error: 'Ya existe una cuenta con ese correo. Usa «¿Olvidaste tu contraseña?» para entrar.' });
    const hash = await bcrypt.hash(d.password, 10);
    const tokenVerif = randomBytes(24).toString('hex');
    const u = existe
      ? await uno('UPDATE usuarios SET password_hash=$2, nombre=$3, idioma_nativo=$4, idioma_meta=$5, nivel_inicial=$6, plataforma=$7, token_verificacion=$8, es_demo=false, ultima_actividad=now() WHERE id=$1 RETURNING id', [existe.id, hash, d.nombre, d.idiomaNativo, d.idiomaMeta, d.nivelInicial, d.plataforma, tokenVerif])
      : await uno('INSERT INTO usuarios (email, nombre, idioma_nativo, idioma_meta, nivel_inicial, plataforma, trial_inicio, password_hash, token_verificacion) VALUES ($1,$2,$3,$4,$5,$6, now(), $7, $8) RETURNING id', [email, d.nombre, d.idiomaNativo, d.idiomaMeta, d.nivelInicial, d.plataforma, hash, tokenVerif]);
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1,$2,$3)', [u!.id, 'registro', JSON.stringify({ metodo: 'password', idiomaMeta: d.idiomaMeta })]);
    const url = `${config.publicUrl}/auth/verificar?token=${tokenVerif}`;
    await enviarCorreo(email, 'Confirma tu correo en OneLingo', plantilla(`¡Hola, ${esc(d.nombre)}!`, 'Gracias por registrarte. Confirma tu correo para proteger tu cuenta y recuperar tu contraseña si la olvidas.', { texto: 'Confirmar correo', url }));
    return reply.code(201).send({ id: u!.id, token: tokenDe(app, u!.id), verificado: false });
  });

  /**
   * Registro con código (desde 0.5.5): 1) `/auth/registro/codigo` valida los datos
   * y manda un código de 6 dígitos al correo; 2) `/auth/registro/verificar` crea
   * la cuenta, ya verificada, solo si el código es correcto. Mensajes y correos
   * en el idioma de la app (`x-idioma`: es o en).
   */
  const DatosRegistro = z.object({
    email: z.string().trim().email(), password: z.string().min(6), nombre: z.string().trim().min(1).max(60), apellido: z.string().trim().min(1).max(60),
    telefono: z.string().trim().min(1),
    idiomaNativo: z.string().default('es'), idiomaMeta: z.string().default('en'), nivelInicial: z.number().int().min(1).max(10).default(1), plataforma: z.string().default(''),
  });
  const T = {
    email: { es: 'Escribe un correo válido.', en: 'Enter a valid email.' },
    password: { es: 'La contraseña debe tener al menos 6 caracteres.', en: 'The password must be at least 6 characters.' },
    nombre: { es: 'Escribe tu nombre.', en: 'Enter your first name.' },
    apellido: { es: 'Escribe tu apellido.', en: 'Enter your last name.' },
    telefono: { es: 'Escribe tu teléfono con el código de país, por ejemplo +1 555 123 4567.', en: 'Enter your phone with the country code, for example +1 555 123 4567.' },
    ocupada: { es: 'Ya existe una cuenta con ese correo. Inicia sesión.', en: 'An account with this email already exists. Log in.' },
    antigua: { es: 'Ya existe una cuenta con ese correo. Usa «¿Olvidaste tu contraseña?» para entrar.', en: 'An account with this email already exists. Use "Forgot your password?" to get in.' },
    datos: { es: 'Datos inválidos.', en: 'Invalid data.' },
  } satisfies Record<string, Txt>;
  /** Primer campo con error → su mensaje en el idioma de la app. */
  const errorDatos = (e: z.ZodError, idioma: keyof Txt) => (T[e.issues[0]?.path[0] as keyof typeof T] ?? T.datos)[idioma];
  const cuentaOcupada = async (email: string): Promise<{ existe: any; error: Txt | null }> => {
    const existe = await uno('SELECT id, password_hash, google_id FROM usuarios WHERE email = $1', [email]);
    if (!existe) return { existe: null, error: null };
    if (existe.password_hash || existe.google_id) return { existe, error: T.ocupada };
    if (!email.endsWith('@onelingo.demo')) return { existe, error: T.antigua };
    return { existe, error: null };
  };
  const errorCodigo = (req: any, reply: any, e: unknown) => {
    if (e instanceof ErrorCodigo) return reply.code(e.status).send({ error: e.txt[idiomaDe(req)], ...e.extra });
    throw e;
  };
  const correoCodigo = (idioma: keyof Txt, nombre: string, codigo: string, proposito: 'registro' | 'clave') => idioma === 'en'
    ? { asunto: `${codigo} is your OneLingo code`, html: plantillaCodigo(`Hi, ${esc(nombre)}!`, proposito === 'registro' ? 'Here is your code to create your OneLingo account:' : 'Here is your code to set a new OneLingo password:', codigo, 'en') }
    : { asunto: proposito === 'registro' ? `${codigo} es tu código de OneLingo` : `${codigo} es tu código para cambiar la contraseña`, html: plantillaCodigo(proposito === 'registro' ? `¡Hola, ${esc(nombre)}!` : `Hola, ${esc(nombre)}`, proposito === 'registro' ? 'Este es tu código para crear tu cuenta en OneLingo:' : 'Este es tu código para crear una contraseña nueva en OneLingo:', codigo, 'es') };

  app.post('/auth/registro/codigo', async (req, reply) => {
    const idioma = idiomaDe(req);
    const r = DatosRegistro.safeParse(req.body);
    if (!r.success) return reply.code(400).send({ error: errorDatos(r.error, idioma) });
    const d = r.data, email = d.email.toLowerCase();
    const telefono = normalizarTelefono(d.telefono);
    if (!telefono) return reply.code(400).send({ error: T.telefono[idioma] });
    const { error } = await cuentaOcupada(email);
    if (error) return reply.code(409).send({ error: error[idioma] });
    let codigo: string;
    try {
      codigo = await emitirCodigo(email, 'registro', {
        nombre: d.nombre, apellido: d.apellido, telefono, passwordHash: await bcrypt.hash(d.password, 10),
        idiomaNativo: d.idiomaNativo, idiomaMeta: d.idiomaMeta, nivelInicial: d.nivelInicial, plataforma: d.plataforma,
      });
    } catch (e) { return errorCodigo(req, reply, e); }
    const c = correoCodigo(idioma, d.nombre, codigo, 'registro');
    await enviarCorreo(email, c.asunto, c.html);
    return { ok: true, email, vigenciaSegundos: 600, reenviarEn: 60 };
  });

  app.post('/auth/registro/verificar', async (req, reply) => {
    const { email: correo, codigo } = z.object({ email: z.string().trim().email(), codigo: z.string().trim().min(4).max(12) }).parse(req.body);
    const email = correo.toLowerCase();
    let d: any;
    try { d = await verificarCodigo(email, 'registro', codigo); } catch (e) { return errorCodigo(req, reply, e); }
    // Pudo registrarse por otro camino mientras tanto (Google, otra pestaña).
    const { existe, error } = await cuentaOcupada(email);
    if (error) return reply.code(409).send({ error: error[idiomaDe(req)] });
    const u = existe
      ? await uno('UPDATE usuarios SET password_hash=$2, nombre=$3, apellido=$4, telefono=$5, idioma_nativo=$6, idioma_meta=$7, nivel_inicial=$8, plataforma=$9, email_verificado=true, token_verificacion=NULL, es_demo=false, ultima_actividad=now() WHERE id=$1 RETURNING id',
        [existe.id, d.passwordHash, d.nombre, d.apellido, d.telefono, d.idiomaNativo, d.idiomaMeta, d.nivelInicial, d.plataforma])
      : await uno('INSERT INTO usuarios (email, nombre, apellido, telefono, idioma_nativo, idioma_meta, nivel_inicial, plataforma, trial_inicio, password_hash, email_verificado) VALUES ($1,$2,$3,$4,$5,$6,$7,$8, now(), $9, true) RETURNING id',
        [email, d.nombre, d.apellido, d.telefono, d.idiomaNativo, d.idiomaMeta, d.nivelInicial, d.plataforma, d.passwordHash]);
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1,$2,$3)', [u!.id, 'registro', JSON.stringify({ metodo: 'password', verificacion: 'codigo', idiomaMeta: d.idiomaMeta })]);
    return reply.code(201).send({ id: u!.id, token: tokenDe(app, u!.id), verificado: true });
  });

  /** Olvidé mi contraseña con código: 1) pedir el código; 2) código + contraseña nueva → sesión. */
  app.post('/auth/clave/codigo', async (req, reply) => {
    const r = z.object({ email: z.string().trim().email() }).safeParse(req.body);
    if (!r.success) return reply.code(400).send({ error: T.email[idiomaDe(req)] });
    const email = r.data.email.toLowerCase();
    const u = await uno('SELECT id, nombre FROM usuarios WHERE email = $1 AND NOT es_demo', [email]);
    // La respuesta no dice si la cuenta existe; solo se manda el correo si existe.
    if (u) {
      let codigo: string;
      try { codigo = await emitirCodigo(email, 'clave'); } catch (e) { return errorCodigo(req, reply, e); }
      const c = correoCodigo(idiomaDe(req), u.nombre, codigo, 'clave');
      await enviarCorreo(email, c.asunto, c.html);
    }
    return { ok: true, vigenciaSegundos: 600, reenviarEn: 60 };
  });

  app.post('/auth/clave/restablecer', async (req, reply) => {
    const idioma = idiomaDe(req);
    const r = z.object({ email: z.string().trim().email(), codigo: z.string().trim().min(4).max(12), password: z.string().min(6) }).safeParse(req.body);
    if (!r.success) return reply.code(400).send({ error: errorDatos(r.error, idioma) });
    const email = r.data.email.toLowerCase();
    try { await verificarCodigo(email, 'clave', r.data.codigo); } catch (e) { return errorCodigo(req, reply, e); }
    const u = await uno('UPDATE usuarios SET password_hash=$2, token_reset=NULL, reset_expira=NULL, email_verificado=true, ultima_actividad=now() WHERE email=$1 RETURNING id, nombre', [email, await bcrypt.hash(r.data.password, 10)]);
    if (!u) return reply.code(404).send({ error: idioma === 'en' ? 'There is no account with this email.' : 'No existe una cuenta con ese correo.' });
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1,$2,$3)', [u.id, 'login', JSON.stringify({ metodo: 'codigo_clave' })]);
    const p = await uno('SELECT estado FROM progreso WHERE usuario_id = $1', [u.id]);
    return { id: u.id, token: tokenDe(app, u.id), nombre: u.nombre, estado: await estadoConPlan(u.id, p?.estado) };
  });

  app.get('/auth/verificar', async (req, reply) => {
    const { token } = z.object({ token: z.string() }).parse(req.query);
    const u = await uno('UPDATE usuarios SET email_verificado = true, token_verificacion = NULL WHERE token_verificacion = $1 RETURNING nombre', [token]);
    reply.type('text/html');
    return plantilla(u ? `Correo confirmado, ${esc(u.nombre)}` : 'Enlace no válido', u ? 'Ya puedes volver a la app de OneLingo.' : 'Este enlace ya se usó o ha caducado.');
  });

  /** Inicio de sesión con correo y contraseña. Devuelve el progreso guardado en el servidor. */
  app.post('/auth/login', async (req, reply) => {
    const { email, password } = z.object({ email: z.string().email(), password: z.string() }).parse(req.body);
    const u = await uno('SELECT id, nombre, password_hash, es_demo FROM usuarios WHERE email = $1', [email.toLowerCase()]);
    if (!u || !u.password_hash || !(await bcrypt.compare(password, u.password_hash))) return reply.code(401).send({ error: 'Correo o contraseña incorrectos' });
    await query('UPDATE usuarios SET ultima_actividad = now() WHERE id = $1', [u.id]);
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1,$2,$3)', [u.id, 'login', JSON.stringify({ metodo: 'password' })]);
    const p = await uno('SELECT estado FROM progreso WHERE usuario_id = $1', [u.id]);
    return { id: u.id, token: tokenDe(app, u.id), nombre: u.nombre, estado: await estadoConPlan(u.id, p?.estado) };
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
    const nombre = payload.given_name ?? payload.name ?? email.split('@')[0];
    const apellido = payload.given_name ? (payload.family_name ?? '') : '';
    const existe = await uno('SELECT id FROM usuarios WHERE google_id = $1 OR email = $2', [payload.sub, email]);
    const u = existe
      ? await uno('UPDATE usuarios SET google_id=$2, email_verificado=true, ultima_actividad=now() WHERE id=$1 RETURNING id', [existe.id, payload.sub])
      : await uno('INSERT INTO usuarios (email, nombre, apellido, idioma_nativo, idioma_meta, nivel_inicial, plataforma, trial_inicio, google_id, email_verificado) VALUES ($1,$2,$3,$4,$5,$6,$7, now(), $8, true) RETURNING id', [email, nombre, apellido, idiomaNativo, idiomaMeta, nivelInicial, plataforma, payload.sub]);
    await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1,$2,$3)', [u!.id, existe ? 'login' : 'registro', JSON.stringify({ metodo: 'google' })]);
    const p = await uno('SELECT estado FROM progreso WHERE usuario_id = $1', [u!.id]);
    const datos = await uno<{ telefono: string }>('SELECT telefono FROM usuarios WHERE id = $1', [u!.id]);
    return { id: u!.id, token: tokenDe(app, u!.id), nombre, email, estado: await estadoConPlan(u!.id, p?.estado), nuevo: !existe, faltaTelefono: !datos?.telefono };
  });

  app.post('/auth/recuperar', async (req) => {
    const { email } = z.object({ email: z.string().email() }).parse(req.body);
    const u = await uno('SELECT id, nombre FROM usuarios WHERE email = $1', [email.toLowerCase()]);
    if (u) {
      const token = randomBytes(24).toString('hex');
      await query("UPDATE usuarios SET token_reset=$2, reset_expira = now() + interval '1 hour' WHERE id=$1", [u.id, token]);
      await enviarCorreo(email, 'Restablece tu contraseña de OneLingo', plantilla(`Hola, ${esc(u.nombre)}`, 'Recibimos una solicitud para cambiar tu contraseña. El enlace vale una hora.', { texto: 'Cambiar contraseña', url: `${config.publicUrl}/auth/restablecer?token=${token}` }));
    }
    return { ok: true, mensaje: 'Si el correo existe, te enviamos un enlace para restablecer la contraseña.' };
  });

  app.get('/auth/restablecer', async (req, reply) => {
    const { token } = z.object({ token: z.string() }).parse(req.query);
    reply.type('text/html');
    // El token va dentro del HTML: solo el formato que generamos (sin esto, un
    // enlace con ?token="><script>… ejecutaba código en onelingo.org).
    if (!/^[0-9a-f]{48}$/.test(token)) return plantilla('Enlace no válido', 'Pide un enlace nuevo desde la app.');
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
  /** Datos de contacto del alumno (Google no da el teléfono: la app lo pide después). */
  app.get('/usuarios/me/contacto', { preHandler: requiereAlumno }, async (req) =>
    uno('SELECT nombre, apellido, email, telefono, email_verificado FROM usuarios WHERE id = $1', [(req.user as Sesion).sub]));
  app.put('/usuarios/me/contacto', { preHandler: requiereAlumno }, async (req, reply) => {
    const idioma = idiomaDe(req);
    const r = z.object({ nombre: z.string().trim().min(1).max(60), apellido: z.string().trim().min(1).max(60), telefono: z.string().trim() }).safeParse(req.body);
    if (!r.success) return reply.code(400).send({ error: errorDatos(r.error, idioma) });
    const telefono = normalizarTelefono(r.data.telefono);
    if (!telefono) return reply.code(400).send({ error: T.telefono[idioma] });
    return uno('UPDATE usuarios SET nombre=$2, apellido=$3, telefono=$4 WHERE id=$1 RETURNING nombre, apellido, email, telefono, email_verificado', [(req.user as Sesion).sub, r.data.nombre, r.data.apellido, telefono]);
  });

  app.get('/usuarios/me/progreso', { preHandler: requiereAlumno }, async (req) => {
    const s = req.user as Sesion;
    const p = await uno('SELECT estado, actualizado_en FROM progreso WHERE usuario_id = $1', [s.sub]);
    const u = await uno('SELECT email, nombre, email_verificado FROM usuarios WHERE id = $1', [s.sub]);
    return { estado: await estadoConPlan(s.sub, p?.estado), actualizado: p?.actualizado_en ?? null, usuario: u };
  });
}
