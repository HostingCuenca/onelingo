import { createHmac, randomInt, timingSafeEqual } from 'node:crypto';
import { config } from './config.js';
import { query, uno } from './db.js';

/**
 * Códigos de 6 dígitos por correo (registro y recuperar la contraseña). Vale
 * 10 minutos, admite 5 intentos, se reenvía tras 60 s y como mucho 5 veces por
 * hora. Se guarda como HMAC con el secreto del servidor, nunca en claro.
 */
export type Proposito = 'registro' | 'clave';
export const VIGENCIA_S = 600, ESPERA_REENVIO_S = 60, MAX_INTENTOS = 5, MAX_ENVIOS_HORA = 5;

const huella = (email: string, proposito: Proposito, codigo: string) =>
  createHmac('sha256', config.jwtSecret).update(`${proposito}:${email}:${codigo}`).digest('hex');

/** Texto en los dos idiomas de la interfaz; la app manda el suyo en `x-idioma`. */
export type Txt = { es: string; en: string };
export const idiomaDe = (req: { headers: Record<string, unknown> }): keyof Txt =>
  String(req.headers['x-idioma'] ?? req.headers['accept-language'] ?? 'es').toLowerCase().startsWith('en') ? 'en' : 'es';

export class ErrorCodigo extends Error { constructor(public txt: Txt, public status: number, public extra: Record<string, unknown> = {}) { super(txt.es); } }

/** Crea (o renueva) el código y devuelve sus 6 dígitos para mandarlos por correo. */
export async function emitirCodigo(email: string, proposito: Proposito, datos: Record<string, unknown> = {}, ahora = new Date()) {
  const previo = await uno<{ enviado_en: Date; primer_envio: Date; envios: number }>(
    'SELECT enviado_en, primer_envio, envios FROM codigos_correo WHERE email = $1 AND proposito = $2', [email, proposito]);
  if (previo) {
    const espera = ESPERA_REENVIO_S - Math.floor((ahora.getTime() - new Date(previo.enviado_en).getTime()) / 1000);
    if (espera > 0) throw new ErrorCodigo({ es: `Espera ${espera} s para pedir otro código.`, en: `Wait ${espera} s to request another code.` }, 429, { reenviarEn: espera });
    const enLaHora = ahora.getTime() - new Date(previo.primer_envio).getTime() < 3600_000;
    if (enLaHora && previo.envios >= MAX_ENVIOS_HORA) throw new ErrorCodigo({ es: 'Pediste demasiados códigos. Inténtalo dentro de una hora.', en: 'Too many codes requested. Try again in an hour.' }, 429, { reenviarEn: 3600 });
  }
  const codigo = String(randomInt(0, 1_000_000)).padStart(6, '0');
  await query(
    `INSERT INTO codigos_correo (email, proposito, codigo_hash, datos, intentos, envios, primer_envio, enviado_en, expira)
     VALUES ($1, $2, $3, $4, 0, 1, $5, $5, $5::timestamptz + make_interval(secs => $6))
     ON CONFLICT (email, proposito) DO UPDATE SET codigo_hash = EXCLUDED.codigo_hash, datos = EXCLUDED.datos, intentos = 0,
       envios = CASE WHEN codigos_correo.primer_envio > $5::timestamptz - interval '1 hour' THEN codigos_correo.envios + 1 ELSE 1 END,
       primer_envio = CASE WHEN codigos_correo.primer_envio > $5::timestamptz - interval '1 hour' THEN codigos_correo.primer_envio ELSE $5 END,
       enviado_en = $5, expira = EXCLUDED.expira`,
    [email, proposito, huella(email, proposito, codigo), JSON.stringify(datos), ahora.toISOString(), VIGENCIA_S]);
  return codigo;
}

const DEMASIADOS: Txt = { es: 'Demasiados intentos. Pide un código nuevo.', en: 'Too many attempts. Request a new code.' };

/** Comprueba el código: si es correcto lo consume y devuelve los datos guardados. */
export async function verificarCodigo(email: string, proposito: Proposito, codigo: string, ahora = new Date()) {
  const f = await uno<{ codigo_hash: string; datos: Record<string, unknown>; intentos: number; expira: Date }>(
    'SELECT codigo_hash, datos, intentos, expira FROM codigos_correo WHERE email = $1 AND proposito = $2', [email, proposito]);
  if (!f || new Date(f.expira) <= ahora) throw new ErrorCodigo({ es: 'El código caducó. Pide uno nuevo.', en: 'The code expired. Request a new one.' }, 410);
  if (f.intentos >= MAX_INTENTOS) throw new ErrorCodigo(DEMASIADOS, 429);
  const esperado = Buffer.from(f.codigo_hash, 'hex');
  const dado = Buffer.from(huella(email, proposito, codigo.replace(/\D/g, '')), 'hex');
  if (!timingSafeEqual(esperado, dado)) {
    await query('UPDATE codigos_correo SET intentos = intentos + 1 WHERE email = $1 AND proposito = $2', [email, proposito]);
    const quedan = MAX_INTENTOS - f.intentos - 1;
    throw new ErrorCodigo(quedan > 0 ? { es: `Código incorrecto. Te quedan ${quedan} intentos.`, en: `Wrong code. ${quedan} attempts left.` } : DEMASIADOS, 400, { intentosRestantes: quedan });
  }
  await query('DELETE FROM codigos_correo WHERE email = $1 AND proposito = $2', [email, proposito]);
  return f.datos;
}

/** Teléfono con código de país: «+593 99 123 4567» → «+593991234567». Null si no es válido. */
export function normalizarTelefono(t: string) {
  const limpio = t.replace(/[\s().-]/g, '');
  return /^\+[1-9]\d{6,14}$/.test(limpio) ? limpio : null;
}
