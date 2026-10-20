/**
 * Conexiones con los proveedores externos (ElevenLabs, OpenAI, Gemini, Stripe)
 * configurables desde el panel: el administrador cambia claves y modelos sin
 * tocar el servidor. Lo guardado en el panel (tabla `conexiones`, cifrado)
 * tiene prioridad sobre el `.env`; borrarlo vuelve a los valores del `.env`.
 *
 * Los consumidores (voz.ts, ia_openai.ts, ia_gemini.ts…) leen `config.x` en
 * cada llamada, así que basta con mutar `config` para aplicar al instante.
 *
 * NUNCA se devuelve ni se registra una clave completa: solo `enmascarar()`.
 * Documentación: docs/PANEL_ADMIN.md → «Conexiones».
 */
import { createCipheriv, createDecipheriv, createHash, randomBytes } from 'node:crypto';
import { config } from './config.js';
import { query } from './db.js';
import { costeIa, costeVoz } from './analitica.js';
import { configurarWebhook, ErrorStripe, esRestringida, llamarStripe, modoDeClave, type ModoPago } from './pagos/stripe.js';

export type ProveedorId = 'elevenlabs' | 'openai' | 'gemini' | 'stripe';
type PropConfig = 'elevenApiKey' | 'elevenModelo' | 'openaiApiKey' | 'openaiModelo' | 'openaiModeloEvaluacion' | 'openaiModeloTranscripcion' | 'geminiApiKey' | 'geminiModelo';
/**
 * `prop`: propiedad de `config` a la que va el campo (null = se guarda aparte, en `extras`).
 * `oculto`: lo rellena el servidor (p. ej. el secreto del webhook de Stripe); no se edita ni se muestra.
 * `tipo`: validación de los campos no secretos (nombre de modelo o URL).
 */
type CampoDef = { prop: PropConfig | null; secreto: boolean; etiqueta: string; oculto?: boolean; tipo?: 'modelo' | 'url' };
type DefProveedor = { nombre: string; uso: string; clave?: string; campos: Record<string, CampoDef>; sugerencias: Record<string, string[]> };

/** Campos que se pueden configurar por proveedor y la propiedad de `config` a la que van. */
export const PROVEEDORES: Record<ProveedorId, DefProveedor> = {
  elevenlabs: {
    nombre: 'ElevenLabs', uso: 'Voz: audios de las clases y del Listening (con caché)',
    campos: {
      apiKey: { prop: 'elevenApiKey', secreto: true, etiqueta: 'Clave de API' },
      modelo: { prop: 'elevenModelo', secreto: false, etiqueta: 'Modelo de voz' },
    },
    sugerencias: { modelo: ['eleven_flash_v2_5', 'eleven_turbo_v2_5', 'eleven_multilingual_v2', 'eleven_v3'] },
  },
  openai: {
    nombre: 'OpenAI', uso: 'Tutor conversacional, evaluación de escritura y transcripción de voz',
    campos: {
      apiKey: { prop: 'openaiApiKey', secreto: true, etiqueta: 'Clave de API (proyecto)' },
      modelo: { prop: 'openaiModelo', secreto: false, etiqueta: 'Modelo del tutor' },
      modeloEvaluacion: { prop: 'openaiModeloEvaluacion', secreto: false, etiqueta: 'Modelo de evaluación' },
      modeloTranscripcion: { prop: 'openaiModeloTranscripcion', secreto: false, etiqueta: 'Modelo de transcripción' },
      adminKey: { prop: null, secreto: true, etiqueta: 'Admin key (opcional, para ver el costo real)' },
    },
    sugerencias: {
      modelo: ['gpt-4.1-mini', 'gpt-4.1-nano', 'gpt-4o-mini', 'gpt-4.1'],
      modeloEvaluacion: ['gpt-4.1', 'gpt-4.1-mini', 'gpt-4o'],
      modeloTranscripcion: ['gpt-4o-mini-transcribe', 'gpt-4o-transcribe', 'whisper-1'],
    },
  },
  gemini: {
    nombre: 'Gemini', uso: 'Generación de ejercicios y diagnóstico (respaldo)',
    campos: {
      apiKey: { prop: 'geminiApiKey', secreto: true, etiqueta: 'Clave de API' },
      modelo: { prop: 'geminiModelo', secreto: false, etiqueta: 'Modelo' },
    },
    sugerencias: { modelo: ['gemini-flash-latest', 'gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.5-flash-lite'] },
  },
  stripe: {
    nombre: 'Stripe', uso: 'Pagos: suscripciones con Stripe Checkout y Customer Portal', clave: 'secretKey',
    campos: {
      secretKey: { prop: null, secreto: true, etiqueta: 'Clave secreta o restringida (sk_… / rk_…)' },
      urlApp: { prop: null, secreto: false, etiqueta: 'URL pública de la app', tipo: 'url' },
      webhookSecret: { prop: null, secreto: true, etiqueta: 'Secreto del webhook', oculto: true },
      webhookId: { prop: null, secreto: false, etiqueta: 'Webhook', oculto: true },
      modo: { prop: null, secreto: false, etiqueta: 'Modo', oculto: true },
    },
    sugerencias: {},
  },
};
export const esProveedor = (p: string): p is ProveedorId => p === 'elevenlabs' || p === 'openai' || p === 'gemini' || p === 'stripe';
const campoClave = (p: ProveedorId) => PROVEEDORES[p].clave ?? 'apiKey';

/**
 * Valores del servidor (.env) tal como estaban al arrancar, para «volver a la
 * configuración del servidor». La Admin key de OpenAI no está en config.ts:
 * opcionalmente sale de OPENAI_ADMIN_KEY.
 */
const ORIGINAL: Record<PropConfig, string> = {
  elevenApiKey: config.elevenApiKey, elevenModelo: config.elevenModelo,
  openaiApiKey: config.openaiApiKey, openaiModelo: config.openaiModelo,
  openaiModeloEvaluacion: config.openaiModeloEvaluacion, openaiModeloTranscripcion: config.openaiModeloTranscripcion,
  geminiApiKey: config.geminiApiKey, geminiModelo: config.geminiModelo,
};
/**
 * Campos sin propiedad en `config` (Admin key de OpenAI y todo Stripe): valor
 * del servidor (variables opcionales del entorno) y valor en uso.
 * Stripe no está en el `.env` de hoy: su origen inicial es «sin configurar».
 */
const EXTRA_SERVIDOR: Record<string, string> = {
  'openai.adminKey': process.env.OPENAI_ADMIN_KEY ?? '',
  'stripe.secretKey': process.env.STRIPE_SECRET_KEY ?? '',
  'stripe.webhookSecret': process.env.STRIPE_WEBHOOK_SECRET ?? '',
};
const extras: Record<string, string> = { ...EXTRA_SERVIDOR };
/** URL pública de la app por defecto: `config.publicUrl` sin `/api` final. */
export const urlAppPorDefecto = () => config.publicUrl.replace(/\/+$/, '').replace(/\/api$/, '');
const extraServidor = (p: ProveedorId, campo: string) => p === 'stripe' && campo === 'urlApp' ? urlAppPorDefecto() : EXTRA_SERVIDOR[`${p}.${campo}`] ?? '';
const extraActual = (p: ProveedorId, campo: string) => extras[`${p}.${campo}`] || extraServidor(p, campo);
export const adminKeyActual = () => extraActual('openai', 'adminKey');

/** Configuración de Stripe en uso (solo para el servidor; nunca se envía al panel). */
export function stripeConfig() {
  const secretKey = extraActual('stripe', 'secretKey');
  return {
    secretKey, urlApp: extraActual('stripe', 'urlApp').replace(/\/+$/, ''),
    webhookSecret: extraActual('stripe', 'webhookSecret'), webhookId: extraActual('stripe', 'webhookId'),
    modo: (modoDeClave(secretKey) ?? null) as ModoPago | null,
  };
}
/** Se llama tras guardar Stripe (lo registra lib/pagos/planes.ts para sincronizar los planes). */
let alGuardarStripe: (() => Promise<string[]>) | null = null;
export function registrarAlGuardarStripe(fn: () => Promise<string[]>) { alGuardarStripe = fn; }

export type Verificacion = { ok: boolean; nivel: 'ok' | 'aviso' | 'error'; mensaje: string; detalles?: string[]; verificadoEn: string };
type Estado = { datos: Record<string, string> | null; actualizadoEn: string | null; verificacion: Verificacion | null; avisos: string[] };
const estado: Record<ProveedorId, Estado> = {
  elevenlabs: { datos: null, actualizadoEn: null, verificacion: null, avisos: [] },
  openai: { datos: null, actualizadoEn: null, verificacion: null, avisos: [] },
  gemini: { datos: null, actualizadoEn: null, verificacion: null, avisos: [] },
  stripe: { datos: null, actualizadoEn: null, verificacion: null, avisos: [] },
};

// ── Detección y formato de claves ────────────────────────────────────────────
/**
 * Formatos de clave (comprobados el 20-10-2026):
 * - OpenAI: claves de proyecto `sk-proj-…` (las actuales por defecto), de
 *   cuenta de servicio `sk-svcacct-…`, de usuario `sk-None-…` y las antiguas
 *   `sk-` + 48 alfanuméricos; las Admin keys de organización `sk-admin-…`.
 *   Fuentes: community.openai.com (hilo «How to create an API secret key with
 *   prefix sk- only», respuesta del equipo) y el cookbook de Usage/Costs API
 *   (developers.openai.com/cookbook/examples/completions_usage_api).
 * - Gemini: las «standard keys» de Google Cloud empiezan con `AIza` y tienen
 *   39 caracteres; desde 2026 Google AI Studio emite «auth keys» con prefijo
 *   `AQ.` (ai.google.dev/gemini-api/docs/api-key y discuss.ai.google.dev,
 *   hilos «Gemini API key start from AQ»). Se aceptan ambas.
 * - ElevenLabs: `sk_` + hexadecimal (guion bajo); las cuentas antiguas tienen
 *   32 caracteres hexadecimales sin prefijo. ElevenLabs no publica el formato
 *   en su documentación (elevenlabs.io/docs/api-reference/authentication solo
 *   indica la cabecera `xi-api-key`); se confirma con la llamada real.
 * - Anthropic: `sk-ant-…` (solo para reconocerla y rechazarla con un mensaje claro).
 * - Stripe: secretas `sk_test_`/`sk_live_`, restringidas `rk_test_`/`rk_live_`,
 *   publicables `pk_test_`/`pk_live_` y secretos de webhook `whsec_`
 *   (docs.stripe.com/keys, 20-10-2026).
 */
export type TipoClave = 'openai' | 'openai-admin' | 'gemini' | 'elevenlabs' | 'anthropic' | 'stripe' | 'stripe-publicable' | 'stripe-webhook';
export function detectarProveedor(clave: string): TipoClave | null {
  const c = limpiarClave(clave);
  if (/^(sk|rk)_(test|live)_[A-Za-z0-9]{10,}$/.test(c)) return 'stripe';
  if (/^pk_(test|live)_/.test(c)) return 'stripe-publicable';
  if (/^whsec_/.test(c)) return 'stripe-webhook';
  if (/^sk-ant-/.test(c)) return 'anthropic';
  if (/^sk-admin-/.test(c)) return 'openai-admin';
  if (/^sk-(proj|svcacct|None)-/.test(c) || /^sk-[A-Za-z0-9_-]{20,}$/.test(c)) return 'openai';
  if (/^AIza[0-9A-Za-z_-]{35}$/.test(c) || /^AQ\.[A-Za-z0-9._-]{20,}$/.test(c)) return 'gemini';
  if (/^sk_[A-Za-z0-9]{20,}$/.test(c) || /^[a-f0-9]{32,}$/i.test(c)) return 'elevenlabs';
  return null;
}
const NOMBRE_TIPO: Record<TipoClave, string> = { openai: 'OpenAI', 'openai-admin': 'OpenAI (Admin key de organización)', gemini: 'Google Gemini', elevenlabs: 'ElevenLabs', anthropic: 'Anthropic (Claude)', stripe: 'Stripe', 'stripe-publicable': 'Stripe (clave publicable)', 'stripe-webhook': 'Stripe (secreto de webhook)' };
const PISTA: Record<TipoClave, string> = {
  elevenlabs: 'Las claves de ElevenLabs empiezan con sk_ (o, en cuentas antiguas, son 32 caracteres hexadecimales).',
  openai: 'Las claves de OpenAI empiezan con sk-proj- (clave de proyecto) o sk-.',
  'openai-admin': 'Las Admin keys de OpenAI empiezan con sk-admin- y se crean en Organization → Admin keys.',
  gemini: 'Las claves de Gemini empiezan con AIza (39 caracteres) o, las nuevas de Google AI Studio, con AQ.',
  anthropic: 'Las claves de Anthropic empiezan con sk-ant-.',
  stripe: 'Las claves de Stripe para el servidor empiezan con sk_test_ o rk_test_ (modo test) y sk_live_ o rk_live_ (modo real).',
  'stripe-publicable': 'Pega la clave secreta (sk_…) o una restringida (rk_…).',
  'stripe-webhook': 'El secreto del webhook lo configura OneLingo solo al guardar; pega la clave secreta (sk_…) o una restringida (rk_…).',
};

/** Quita espacios, saltos de línea y comillas pegados por error. */
export function limpiarClave(clave: string) {
  return String(clave ?? '').replace(/\s+/g, '').replace(/^["'`]+|["'`]+$/g, '');
}

/** Tipo de clave que espera cada campo secreto. */
const ESPERADO: Record<string, TipoClave> = { 'elevenlabs.apiKey': 'elevenlabs', 'openai.apiKey': 'openai', 'openai.adminKey': 'openai-admin', 'gemini.apiKey': 'gemini', 'stripe.secretKey': 'stripe' };

/**
 * Valida el formato de una clave para un campo. Una clave reconocida como de
 * otro proveedor se rechaza sin llamar a nadie; un formato desconocido pasa
 * (lo decide la verificación real, por si el proveedor cambia de formato).
 */
export function validarFormato(proveedor: ProveedorId, campo: string, valor: string): { ok: true; clave: string; aviso?: string } | { ok: false; mensaje: string } {
  const clave = limpiarClave(valor);
  const esperado = ESPERADO[`${proveedor}.${campo}`];
  if (!esperado) return { ok: false, mensaje: 'Campo de clave desconocido.' };
  if (clave.length < 20) return { ok: false, mensaje: `La clave es demasiado corta. ${PISTA[esperado]}` };
  if (!/^[\x21-\x7e]+$/.test(clave)) return { ok: false, mensaje: `La clave tiene caracteres no válidos. ${PISTA[esperado]}` };
  const tipo = detectarProveedor(clave);
  if (tipo === esperado) return { ok: true, clave };
  if (tipo === 'openai-admin' && esperado === 'openai') return { ok: false, mensaje: 'Esta es una Admin key de OpenAI: va en el campo «Admin key», no en la clave de API. Las claves de proyecto empiezan con sk-proj-.' };
  if (tipo === 'stripe-publicable' && esperado === 'stripe') return { ok: false, mensaje: 'Esta es la clave publicable; pega la secreta (sk_…)' };
  if (tipo === 'stripe-webhook' && esperado === 'stripe') return { ok: false, mensaje: `Este es un secreto de webhook (whsec_…), no una clave de API. ${PISTA['stripe-webhook']}` };
  if (tipo === 'openai' && esperado === 'openai-admin') return { ok: false, mensaje: 'Esta es una clave de proyecto de OpenAI, no una Admin key. Las Admin keys empiezan con sk-admin- y se crean en Organization → Admin keys.' };
  if (tipo) return { ok: false, mensaje: `Esta clave es de ${NOMBRE_TIPO[tipo]}, no de ${PROVEEDORES[proveedor].nombre}. ${PISTA[esperado]}` };
  return { ok: true, clave, aviso: `El formato no es el habitual de ${PROVEEDORES[proveedor].nombre}; se comprobará con el proveedor.` };
}

const MODELO_VALIDO = /^[A-Za-z0-9._:\/-]{1,80}$/;
/** URL http(s) sin espacios, query ni fragmento (p. ej. https://onelingo.app). */
export function validarUrl(v: string): string | null {
  const s = v.trim().replace(/\/+$/, '');
  if (s.length > 200 || /\s/.test(s)) return null;
  try { const u = new URL(s); return (u.protocol === 'https:' || u.protocol === 'http:') && !u.search && !u.hash && !u.username ? s : null; } catch { return null; }
}

/** `sk_…a1b2`: prefijo no secreto (hasta 8 caracteres) + últimos 4. Nunca más. */
export function enmascarar(clave: string | null | undefined): string | null {
  const c = limpiarClave(clave ?? '');
  if (!c) return null;
  if (c.length < 16) return '••••';
  const prefijo = (/^(sk_test_|sk_live_|rk_test_|rk_live_|whsec_|sk-proj-|sk-svcacct-|sk-admin-|sk-None-|sk-ant-|sk_|sk-|AIza|AQ\.)/.exec(c)?.[1] ?? '').slice(0, 8);
  return `${prefijo}…${c.slice(-4)}`;
}

// ── Cifrado ──────────────────────────────────────────────────────────────────
const claveCifrado = (secreto: string) => createHash('sha256').update('onelingo-conexiones:' + secreto).digest();
/** AES-256-GCM → `v1:` + base64(iv[12] | tag[16] | datos). */
export function cifrar(datos: unknown, secreto = config.jwtSecret) {
  const iv = randomBytes(12);
  const c = createCipheriv('aes-256-gcm', claveCifrado(secreto), iv);
  const cuerpo = Buffer.concat([c.update(JSON.stringify(datos), 'utf8'), c.final()]);
  return 'v1:' + Buffer.concat([iv, c.getAuthTag(), cuerpo]).toString('base64');
}
/** Lanza si el texto no se puede descifrar (otro secreto o datos alterados). */
export function descifrar<T = any>(texto: string, secreto = config.jwtSecret): T {
  if (!texto.startsWith('v1:')) throw new Error('Formato de cifrado desconocido');
  const b = Buffer.from(texto.slice(3), 'base64');
  const d = createDecipheriv('aes-256-gcm', claveCifrado(secreto), b.subarray(0, 12));
  d.setAuthTag(b.subarray(12, 28));
  return JSON.parse(Buffer.concat([d.update(b.subarray(28)), d.final()]).toString('utf8'));
}

// ── Aplicar sobre config ─────────────────────────────────────────────────────
/** Valores efectivos de un proveedor: lo del panel o, si no, lo del servidor. */
export function aplicar(proveedor: ProveedorId, datos: Record<string, string> | null) {
  for (const [campo, def] of Object.entries(PROVEEDORES[proveedor].campos)) {
    const v = datos?.[campo];
    if (def.prop) (config as any)[def.prop] = v ? v : ORIGINAL[def.prop];
    else extras[`${proveedor}.${campo}`] = v ? v : extraServidor(proveedor, campo);
  }
  estado[proveedor].datos = datos && Object.keys(datos).length ? datos : null;
}
export const restaurar = (proveedor: ProveedorId) => aplicar(proveedor, null);

/** Valores en uso ahora mismo (para verificar «lo actual»). */
export function valoresActuales(proveedor: ProveedorId): Record<string, string> {
  const r: Record<string, string> = {};
  for (const [campo, def] of Object.entries(PROVEEDORES[proveedor].campos)) {
    r[campo] = def.prop ? String((config as any)[def.prop] ?? '') : extraActual(proveedor, campo);
  }
  return r;
}
const valorServidor = (proveedor: ProveedorId, campo: string) => {
  const def = PROVEEDORES[proveedor].campos[campo];
  return def.prop ? ORIGINAL[def.prop] : extraServidor(proveedor, campo);
};

/** Lee la tabla y aplica lo guardado sobre `config`. Se llama al arrancar, tras migrar(). */
export async function cargarConexiones() {
  let filas: { proveedor: string; datos: string; actualizado_en: string | null; verificacion: Verificacion | null }[] = [];
  try { filas = await query('SELECT proveedor, datos, actualizado_en, verificacion FROM conexiones'); }
  catch { return; } // sin tabla: se queda todo como en el .env
  for (const f of filas) {
    if (!esProveedor(f.proveedor)) continue;
    const e = estado[f.proveedor];
    try {
      aplicar(f.proveedor, descifrar(f.datos));
      e.actualizadoEn = f.actualizado_en ? new Date(f.actualizado_en).toISOString() : null; e.verificacion = f.verificacion; e.avisos = [];
    } catch {
      restaurar(f.proveedor);
      e.avisos = ['La configuración guardada en el panel no se pudo descifrar (¿cambió JWT_SECRET en el servidor?). Se usa la del servidor (.env). Vuelve a guardar la clave.'];
    }
  }
}

// ── Verificación con el proveedor (solo llamadas de lectura, sin coste) ──────
export const TIMEOUT_MS = 10_000;
type Opciones = { timeoutMs?: number };

/** Mensaje del proveedor sin la clave (por si la repite) y recortado. */
function mensajeProveedor(j: any, texto: string, claves: string[]) {
  let m = j?.error?.message ?? j?.detail?.message ?? (typeof j?.detail === 'string' ? j.detail : '') ?? '';
  if (!m) m = texto.slice(0, 200);
  for (const k of claves) if (k && k.length >= 8) m = m.split(k).join(enmascarar(k) ?? '••••');
  return String(m).replace(/\s+/g, ' ').trim().slice(0, 400);
}
async function pedir(url: string, init: RequestInit, timeoutMs: number) {
  const r = await fetch(url, { ...init, signal: AbortSignal.timeout(timeoutMs) });
  const texto = await r.text().catch(() => '');
  let j: any = null; try { j = JSON.parse(texto); } catch { /* no es JSON */ }
  return { status: r.status, ok: r.ok, j, texto };
}
function errorDeRed(nombre: string, e: any, timeoutMs: number): Verificacion {
  const t = e?.name === 'TimeoutError' || e?.name === 'AbortError';
  return res('error', t ? `Sin respuesta de ${nombre} en ${Math.round(timeoutMs / 1000)} s (tiempo de espera agotado). Inténtalo de nuevo.` : `No se pudo conectar con ${nombre}: ${String(e?.message ?? e).slice(0, 200)}`);
}
const res = (nivel: Verificacion['nivel'], mensaje: string, detalles?: string[]): Verificacion =>
  ({ ok: nivel !== 'error', nivel, mensaje, ...(detalles?.length ? { detalles } : {}), verificadoEn: new Date().toISOString() });

const fmt = (n: number) => Number(n ?? 0).toLocaleString('es');

export type CuotaEleven = { plan: string; estado: string | null; usados: number; limite: number; reinicio: string | null };
const cuotaDe = (j: any): CuotaEleven => ({
  plan: String(j?.tier ?? '?'), estado: j?.status ?? null, usados: Number(j?.character_count ?? 0), limite: Number(j?.character_limit ?? 0),
  reinicio: j?.next_character_count_reset_unix ? new Date(j.next_character_count_reset_unix * 1000).toISOString() : null,
});
const claveInvalidaEleven = (j: any, texto: string) => j?.detail?.status === 'invalid_api_key' || /api key is invalid|invalid api key/i.test(String(j?.detail?.message ?? texto));
const faltaPermiso = (j: any) => j?.detail?.status === 'missing_permissions' || /missing the permission/i.test(String(j?.detail?.message ?? ''));

async function verificarEleven(v: Record<string, string>, op: Opciones): Promise<Verificacion & { cuota?: CuotaEleven | null }> {
  const t = op.timeoutMs ?? TIMEOUT_MS, h = { 'xi-api-key': v.apiKey };
  try {
    const s = await pedir('https://api.elevenlabs.io/v1/user/subscription', { headers: h }, t);
    const detalles: string[] = [];
    let nivel: Verificacion['nivel'] = 'ok', mensaje = 'Clave válida.', cuota: CuotaEleven | null = null;
    if (s.ok) {
      cuota = cuotaDe(s.j);
      detalles.push(`Plan ${cuota.plan}: ${fmt(cuota.usados)} de ${fmt(cuota.limite)} caracteres usados este periodo.`);
      if (cuota.limite > 0 && cuota.usados >= cuota.limite) { nivel = 'aviso'; mensaje = 'Clave válida, pero la cuota del periodo está agotada: no se generarán audios nuevos hasta la renovación.'; }
      if (cuota.estado && ['past_due', 'free_disabled', 'incomplete'].includes(cuota.estado)) { nivel = 'aviso'; mensaje = `Clave válida, pero la suscripción está en estado «${cuota.estado}». Revisa la facturación en ElevenLabs.`; }
    } else if (s.status === 401 && faltaPermiso(s.j)) {
      nivel = 'aviso'; mensaje = 'Válida, pero sin permiso «User → Read/Access»: no se podrá mostrar el consumo. Actívalo en ElevenLabs → Developers → API Keys → Editar.';
    } else if (s.status === 401 || claveInvalidaEleven(s.j, s.texto)) {
      // ElevenLabs responde 401, o 400 «API key is invalid» según el caso (comprobado el 20-10-2026).
      return res('error', `Clave inválida: ElevenLabs la rechazó (${mensajeProveedor(s.j, s.texto, [v.apiKey]) || s.status}).`);
    } else {
      return res('error', `ElevenLabs respondió ${s.status}: ${mensajeProveedor(s.j, s.texto, [v.apiKey])}`);
    }
    // Modelo configurado (si la clave puede leer modelos).
    const m = await pedir('https://api.elevenlabs.io/v1/models', { headers: h }, t).catch(() => null);
    if (m?.ok && Array.isArray(m.j) && v.modelo) {
      if (!m.j.some((x: any) => x?.model_id === v.modelo)) { if (nivel === 'ok') nivel = 'aviso'; detalles.push(`El modelo «${v.modelo}» no aparece en tu cuenta de ElevenLabs.`); }
      else detalles.push(`Modelo «${v.modelo}» disponible.`);
    } else if (m && faltaPermiso(m.j)) detalles.push('La clave no tiene permiso «Models»: no se pudo comprobar el modelo.');
    detalles.push('Para generar audios la clave necesita el permiso «Text to Speech».');
    return { ...res(nivel, mensaje, detalles), cuota };
  } catch (e) { return errorDeRed('ElevenLabs', e, t); }
}

/** Unix del día 1 del mes actual (UTC). */
export const inicioDeMes = (d = new Date()) => Math.floor(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), 1) / 1000);

async function verificarOpenAI(v: Record<string, string>, op: Opciones): Promise<Verificacion> {
  const t = op.timeoutMs ?? TIMEOUT_MS;
  try {
    const r = await pedir('https://api.openai.com/v1/models', { headers: { authorization: `Bearer ${v.apiKey}` } }, t);
    if (r.status === 401) return res('error', `Clave inválida: OpenAI la rechazó (${mensajeProveedor(r.j, r.texto, [v.apiKey])}).`);
    if (!r.ok) return res('error', `OpenAI respondió ${r.status}: ${mensajeProveedor(r.j, r.texto, [v.apiKey])}`);
    const ids = new Set<string>((r.j?.data ?? []).map((m: any) => String(m?.id)));
    const detalles: string[] = [];
    let nivel: Verificacion['nivel'] = 'ok';
    for (const [campo, et] of [['modelo', 'tutor'], ['modeloEvaluacion', 'evaluación'], ['modeloTranscripcion', 'transcripción']] as const) {
      const id = v[campo];
      if (!id) continue;
      if (ids.has(id)) detalles.push(`Modelo de ${et} «${id}» disponible.`);
      else { nivel = 'aviso'; detalles.push(`El modelo de ${et} «${id}» no aparece en la lista de modelos de esta clave.`); }
    }
    let mensaje = nivel === 'ok' ? 'Clave válida.' : 'Clave válida, pero falta algún modelo (revisa los detalles).';
    detalles.push('La lista de modelos no comprueba el saldo: si el tutor falla con «insufficient_quota», revisa Billing en OpenAI.');
    if (v.adminKey) {
      const c = await pedir(`https://api.openai.com/v1/organization/costs?start_time=${inicioDeMes()}&limit=1`, { headers: { authorization: `Bearer ${v.adminKey}` } }, t);
      if (c.ok) detalles.push('Admin key válida: se mostrará el costo real del mes.');
      else return res('error', `Admin key rechazada (${c.status}): ${mensajeProveedor(c.j, c.texto, [v.adminKey, v.apiKey])}`, detalles);
    }
    return res(nivel, mensaje, detalles);
  } catch (e) { return errorDeRed('OpenAI', e, t); }
}

async function verificarGemini(v: Record<string, string>, op: Opciones): Promise<Verificacion> {
  const t = op.timeoutMs ?? TIMEOUT_MS;
  try {
    // Cabecera en vez de ?key= para que la clave no viaje en la URL.
    const r = await pedir('https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000', { headers: { 'x-goog-api-key': v.apiKey } }, t);
    const msg = () => mensajeProveedor(r.j, r.texto, [v.apiKey]);
    const invalida = r.status === 401 || (r.status === 400 && /API_KEY_INVALID|API key not valid/i.test(r.texto));
    if (invalida) return res('error', `Clave inválida: Google la rechazó (${msg()}).`);
    if (r.status === 403) return res('error', `Google denegó el acceso (403): ${msg()}`, ['Revisa en Google AI Studio que el proyecto de la clave tenga acceso a la Gemini API y facturación activa.']);
    if (!r.ok) return res('error', `Gemini respondió ${r.status}: ${msg()}`);
    const nombres = new Set<string>((r.j?.models ?? []).map((m: any) => String(m?.name ?? '').replace(/^models\//, '')));
    if (v.modelo && !nombres.has(v.modelo)) return res('aviso', 'Clave válida, pero el modelo configurado no aparece.', [`El modelo «${v.modelo}» no está en la lista de modelos de esta clave.`]);
    return res('ok', 'Clave válida.', v.modelo ? [`Modelo «${v.modelo}» disponible.`] : undefined);
  } catch (e) { return errorDeRed('Gemini', e, t); }
}

/**
 * Stripe: `GET /v1/account` (clave secreta) o `GET /v1/balance` (restringida,
 * que puede no tener permiso de cuenta). Ambas son lecturas gratuitas.
 * Una clave inventada responde 401 «Invalid API Key provided».
 */
async function verificarStripe(v: Record<string, string>, op: Opciones): Promise<Verificacion> {
  const t = op.timeoutMs ?? TIMEOUT_MS;
  const modo = modoDeClave(v.secretKey);
  const detalles: string[] = [];
  let nivel: Verificacion['nivel'] = 'ok';
  try {
    if (esRestringida(v.secretKey)) {
      const b = await llamarStripe(v.secretKey, 'GET', '/balance', {}, { timeoutMs: t });
      detalles.push(`Clave restringida válida (${b?.livemode ? 'modo real' : 'modo test'}). Comprueba que tenga los permisos de «¿Cómo obtengo la clave?».`);
    } else {
      const a = await llamarStripe(v.secretKey, 'GET', '/account', {}, { timeoutMs: t });
      const nombre = a?.settings?.dashboard?.display_name || a?.business_profile?.name || a?.email || '';
      detalles.push(`Cuenta ${a?.id ?? '?'}${nombre ? ` · ${nombre}` : ''}.`);
      if (a?.charges_enabled === false && modo === 'live') { nivel = 'aviso'; detalles.push('La cuenta aún no puede cobrar en modo real: completa la activación en Stripe.'); }
    }
  } catch (e) {
    if (e instanceof ErrorStripe) {
      if (e.status === 401) return res('error', `Clave inválida: Stripe la rechazó (${e.message}).`);
      if (e.status === 403) return res('error', `La clave no tiene permiso para leer ${esRestringida(v.secretKey) ? 'el saldo (Balance → Read)' : 'la cuenta'}: ${e.message}`);
      if (e.status === 0) return res('error', e.message);
      return res('error', `Stripe respondió ${e.status}: ${e.message}`);
    }
    return errorDeRed('Stripe', e, t);
  }
  detalles.unshift(modo === 'live' ? 'MODO REAL: los cobros son de verdad.' : 'MODO TEST: pagos simulados (tarjeta 4242 4242 4242 4242).');
  const url = v.urlApp ? validarUrl(v.urlApp) : null;
  if (!url) return res('error', 'Falta la URL pública de la app (https://…).', detalles);
  if (/^http:\/\/|\/\/(localhost|127\.|0\.0\.0\.0|\[::1\])/.test(url)) {
    nivel = 'aviso';
    detalles.push('La URL de la app es local o sin https: Stripe no podrá entregar el webhook. Los pagos se confirman igual con «Confirmar» al volver de Checkout.');
  }
  return res(nivel, nivel === 'ok' ? 'Clave válida.' : 'Clave válida, con avisos.', detalles);
}

/**
 * Valores finales a verificar/guardar: lo enviado (limpio y validado) sobre
 * lo actual. Un campo de clave vacío conserva la clave en uso.
 */
export function prepararValores(proveedor: ProveedorId, cuerpo: Record<string, unknown>) {
  const actuales = valoresActuales(proveedor);
  const cambios: Record<string, string> = {};
  const errores: Record<string, string> = {};
  const avisos: string[] = [];
  for (const [campo, def] of Object.entries(PROVEEDORES[proveedor].campos)) {
    if (def.oculto) continue; // los rellena el servidor
    const bruto = cuerpo?.[campo];
    if (bruto === undefined || bruto === null) continue;
    if (typeof bruto !== 'string') { errores[campo] = 'Valor no válido.'; continue; }
    if (def.secreto) {
      if (!limpiarClave(bruto)) continue; // vacío = conservar
      const f = validarFormato(proveedor, campo, bruto);
      if (!f.ok) { errores[campo] = f.mensaje; continue; }
      if (f.aviso) avisos.push(f.aviso);
      cambios[campo] = f.clave;
    } else {
      const m = bruto.trim();
      if (!m) continue;
      if (def.tipo === 'url') {
        const u = validarUrl(m);
        if (!u) { errores[campo] = 'URL no válida: usa https://dominio (sin espacios, ? ni #).'; continue; }
        cambios[campo] = u; continue;
      }
      if (!MODELO_VALIDO.test(m)) { errores[campo] = 'Nombre de modelo no válido (solo letras, números y . _ - : /).'; continue; }
      cambios[campo] = m;
    }
  }
  if (proveedor === 'openai' && cuerpo?.quitarAdminKey === true) cambios.adminKey = '';
  const valores = { ...actuales, ...cambios };
  const ck = campoClave(proveedor);
  if (!valores[ck]) errores[ck] ??= 'Falta la clave de API.';
  return { valores, cambios, errores, avisos };
}

/** Verifica unos valores ya preparados contra el proveedor (sin guardar). */
export async function verificarValores(proveedor: ProveedorId, v: Record<string, string>, op: Opciones = {}): Promise<Verificacion> {
  const r = proveedor === 'elevenlabs' ? await verificarEleven(v, op) : proveedor === 'openai' ? await verificarOpenAI(v, op)
    : proveedor === 'stripe' ? await verificarStripe(v, op) : await verificarGemini(v, op);
  const { cuota: _c, ...limpio } = r as any;
  return limpio;
}

type ResultadoOperacion = { ok: boolean; verificacion?: Verificacion; errores?: Record<string, string>; avisos?: string[] };

/** POST …/verificar: lo enviado o lo actual, sin guardar. */
export async function verificar(proveedor: ProveedorId, cuerpo: Record<string, unknown> = {}, op: Opciones = {}): Promise<ResultadoOperacion> {
  const p = prepararValores(proveedor, cuerpo);
  if (Object.keys(p.errores).length) return { ok: false, errores: p.errores };
  const verificacion = await verificarValores(proveedor, p.valores, op);
  if (!Object.keys(p.cambios).length) {
    // Se verificó lo que está en uso: se recuerda como «última verificación».
    estado[proveedor].verificacion = verificacion;
    if (estado[proveedor].datos) await query('UPDATE conexiones SET verificacion = $2 WHERE proveedor = $1', [proveedor, JSON.stringify(verificacion)]).catch(() => {});
  }
  return { ok: verificacion.ok, verificacion, avisos: p.avisos };
}

/** PUT: valida, verifica y, si no hay error, cifra, guarda y aplica en caliente. */
export async function guardar(proveedor: ProveedorId, cuerpo: Record<string, unknown> = {}, op: Opciones = {}): Promise<ResultadoOperacion> {
  const p = prepararValores(proveedor, cuerpo);
  if (Object.keys(p.errores).length) return { ok: false, errores: p.errores };
  let verificacion = await verificarValores(proveedor, p.valores, op);
  if (!verificacion.ok) return { ok: false, verificacion, avisos: p.avisos };
  if (proveedor === 'stripe') {
    const s = await prepararStripe(p.valores, op);
    Object.assign(p.valores, s.valores);
    verificacion = { ...verificacion, nivel: verificacion.nivel === 'ok' && s.aviso ? 'aviso' : verificacion.nivel, detalles: [...(verificacion.detalles ?? []), ...s.detalles] };
  }
  // Se guarda solo lo que difiere del servidor: lo demás sigue heredando del .env.
  const datos: Record<string, string> = {};
  for (const campo of Object.keys(PROVEEDORES[proveedor].campos)) {
    const v = p.valores[campo] ?? '';
    if (v && v !== valorServidor(proveedor, campo)) datos[campo] = v;
  }
  if (!Object.keys(datos).length) {
    await query('DELETE FROM conexiones WHERE proveedor = $1', [proveedor]);
    restaurar(proveedor);
    estado[proveedor].actualizadoEn = null;
  } else {
    const filas = await query<{ actualizado_en: string }>(
      `INSERT INTO conexiones (proveedor, datos, actualizado_en, verificacion) VALUES ($1, $2, now(), $3)
       ON CONFLICT (proveedor) DO UPDATE SET datos = EXCLUDED.datos, actualizado_en = now(), verificacion = EXCLUDED.verificacion
       RETURNING actualizado_en`, [proveedor, cifrar(datos), JSON.stringify(verificacion)]);
    aplicar(proveedor, datos);
    estado[proveedor].actualizadoEn = filas[0]?.actualizado_en ? new Date(filas[0].actualizado_en).toISOString() : new Date().toISOString();
  }
  estado[proveedor].verificacion = verificacion; estado[proveedor].avisos = [];
  if (proveedor === 'stripe' && alGuardarStripe) {
    const d = await alGuardarStripe().catch((e) => [`No se pudieron sincronizar los planes: ${String(e?.message ?? e).slice(0, 200)}`]);
    if (d.length) verificacion.detalles = [...(verificacion.detalles ?? []), ...d];
  }
  return { ok: true, verificacion, avisos: p.avisos };
}

/**
 * Al vincular Stripe: modo y webhook (crea o reutiliza el endpoint y guarda su
 * secreto); después, planes y Customer Portal (alGuardarStripe). Un fallo aquí no impide guardar la clave: se
 * avisa y los pagos se confirman con «Confirmar» al volver de Checkout.
 */
async function prepararStripe(v: Record<string, string>, op: Opciones) {
  const valores: Record<string, string> = { modo: modoDeClave(v.secretKey) ?? '' };
  const detalles: string[] = [];
  let aviso = false;
  const o = { timeoutMs: op.timeoutMs ?? TIMEOUT_MS };
  const misma = v.secretKey === extraActual('stripe', 'secretKey');
  const url = `${v.urlApp}/api/stripe/webhook`;
  try {
    const w = await configurarWebhook(v.secretKey, url, misma ? { id: extraActual('stripe', 'webhookId'), secreto: extraActual('stripe', 'webhookSecret') } : {}, o);
    valores.webhookId = w.id; valores.webhookSecret = w.secreto;
    detalles.push(`Webhook ${w.accion === 'reutilizado' ? 'reutilizado' : w.accion === 'creado' ? 'creado' : 'recreado'} en ${url}.`);
  } catch (e: any) {
    aviso = true; valores.webhookId = ''; valores.webhookSecret = '';
    detalles.push(`No se pudo crear el webhook (${String(e?.message ?? e).slice(0, 200)}). Sin webhook, el pago se confirma al volver de Checkout («Confirmar»); las renovaciones y cancelaciones no se actualizarán solas.`);
  }
  // El Customer Portal (con cambio de plan) se configura después, al sincronizar los planes (alGuardarStripe).
  return { valores, detalles, aviso };
}

/** DELETE: borra lo del panel y vuelve a los valores del servidor (.env). */
export async function eliminar(proveedor: ProveedorId) {
  await query('DELETE FROM conexiones WHERE proveedor = $1', [proveedor]);
  restaurar(proveedor);
  Object.assign(estado[proveedor], { actualizadoEn: null, verificacion: null, avisos: [] });
}

/** GET /admin/conexiones: estado sin claves (solo enmascaradas). */
export function resumen() {
  const proveedores = (Object.keys(PROVEEDORES) as ProveedorId[]).map((id) => {
    const def = PROVEEDORES[id], e = estado[id], v = valoresActuales(id), ck = campoClave(id);
    const panel = !!e.datos;
    const claveServidor = valorServidor(id, ck);
    const origen = panel ? 'panel' : claveServidor ? 'servidor' : 'sin configurar';
    const modelos: Record<string, string> = {};
    const visibles = Object.entries(def.campos).filter(([, c]) => !c.oculto);
    for (const [campo, c] of visibles) if (!c.secreto) modelos[campo] = v[campo];
    return {
      id, nombre: def.nombre, uso: def.uso, origen,
      claveOrigen: e.datos?.[ck] ? 'panel' : claveServidor ? 'servidor' : 'ninguna',
      clave: enmascarar(v[ck]), configurada: !!v[ck],
      ...(id === 'openai' ? { adminKey: enmascarar(v.adminKey) } : {}),
      ...(id === 'stripe' ? { modo: modoDeClave(v.secretKey), webhook: !!v.webhookSecret } : {}),
      modelos, campos: Object.fromEntries(visibles.map(([k, c]) => [k, { etiqueta: c.etiqueta, secreto: c.secreto }])),
      sugerencias: id === 'stripe' ? { urlApp: [urlAppPorDefecto()] } : def.sugerencias,
      ultimaVerificacion: e.verificacion, actualizadoEn: e.actualizadoEn, avisos: e.avisos,
    };
  });
  return { iaProveedor: config.iaProveedor, proveedores };
}

// ── Consumo ──────────────────────────────────────────────────────────────────
const proveedorDeModelo = (m: string) => /^gemini/i.test(m) ? 'gemini' : /^claude/i.test(m) ? 'anthropic' : 'openai';
const redondear = (v: number, d = 4) => Math.round(v * 10 ** d) / 10 ** d;

async function iaDelMes() {
  const filas = await query<{ modelo: string; conversaciones: number; entrada: number; salida: number }>(
    `SELECT coalesce(modelo, '') AS modelo, count(*)::int AS conversaciones, coalesce(sum(tokens_entrada), 0)::bigint AS entrada, coalesce(sum(tokens_salida), 0)::bigint AS salida
     FROM conversaciones WHERE fecha >= date_trunc('month', now()) GROUP BY 1`).catch(() => []);
  return filas.map((f) => ({ ...f, proveedor: proveedorDeModelo(f.modelo), coste: redondear(costeIa(f.modelo, f.entrada, f.salida)) }));
}

async function consumoEleven(op: Opciones) {
  const t = op.timeoutMs ?? TIMEOUT_MS;
  const [local] = await query<{ audios: number; caracteres: number; audios_mes: number; caracteres_mes: number }>(
    `SELECT count(*)::int AS audios, coalesce(sum(caracteres), 0)::bigint AS caracteres,
       count(*) FILTER (WHERE creado_en >= date_trunc('month', now()))::int AS audios_mes,
       coalesce(sum(caracteres) FILTER (WHERE creado_en >= date_trunc('month', now())), 0)::bigint AS caracteres_mes FROM audios`).catch(() => []);
  const onelingo = local ? { ...local, costeMesEstimado: redondear(costeVoz(local.caracteres_mes), 2) } : null;
  if (!config.elevenApiKey) return { tipo: 'sin configurar', onelingo, nota: 'Configura una clave para ver la cuota.' };
  try {
    const s = await pedir('https://api.elevenlabs.io/v1/user/subscription', { headers: { 'xi-api-key': config.elevenApiKey } }, t);
    if (s.ok) return { tipo: 'real', cuota: cuotaDe(s.j), onelingo };
    if (faltaPermiso(s.j)) return { tipo: 'sin permiso', onelingo, nota: 'La clave no tiene el permiso «User → Read/Access»: actívalo en ElevenLabs para ver la cuota.' };
    return { tipo: 'error', onelingo, nota: `ElevenLabs respondió ${s.status}: ${mensajeProveedor(s.j, s.texto, [config.elevenApiKey])}` };
  } catch (e) { return { tipo: 'error', onelingo, nota: errorDeRed('ElevenLabs', e, t).mensaje }; }
}

async function consumoOpenAI(op: Opciones, ia: Awaited<ReturnType<typeof iaDelMes>>) {
  const t = op.timeoutMs ?? TIMEOUT_MS;
  const propias = ia.filter((f) => f.proveedor === 'openai');
  const estimado = { coste: redondear(propias.reduce((a, f) => a + f.coste, 0)), conversaciones: propias.reduce((a, f) => a + f.conversaciones, 0), modelos: propias };
  const adminKeyOpenAI = adminKeyActual();
  if (adminKeyOpenAI) {
    try {
      let total = 0, moneda = 'usd', pagina: string | null = null, vueltas = 0;
      const porConcepto = new Map<string, number>();
      do {
        const url: string = `https://api.openai.com/v1/organization/costs?start_time=${inicioDeMes()}&bucket_width=1d&limit=31&group_by=line_item${pagina ? `&page=${encodeURIComponent(pagina)}` : ''}`;
        const r = await pedir(url, { headers: { authorization: `Bearer ${adminKeyOpenAI}` } }, t);
        if (!r.ok) return { tipo: 'estimado', estimado, nota: `No se pudo leer el costo real (OpenAI ${r.status}: ${mensajeProveedor(r.j, r.texto, [adminKeyOpenAI])}). Se muestra el estimado.` };
        for (const b of r.j?.data ?? []) for (const x of b?.results ?? []) {
          const v = Number(x?.amount?.value ?? 0); total += v; moneda = x?.amount?.currency ?? moneda;
          const k = x?.line_item ?? 'otros'; porConcepto.set(k, (porConcepto.get(k) ?? 0) + v);
        }
        pagina = r.j?.has_more ? r.j?.next_page ?? null : null;
      } while (pagina && ++vueltas < 5);
      return {
        tipo: 'real', moneda, costeMes: redondear(total, 2), desde: new Date(inicioDeMes() * 1000).toISOString(),
        porConcepto: [...porConcepto].map(([concepto, coste]) => ({ concepto, coste: redondear(coste, 2) })).sort((a, b) => b.coste - a.coste),
        estimado,
      };
    } catch (e) { return { tipo: 'estimado', estimado, nota: errorDeRed('OpenAI', e, t).mensaje + ' Se muestra el estimado.' }; }
  }
  return { tipo: 'estimado', estimado, nota: 'Estimado con los tokens del tutor registrados y las tarifas de analitica.ts (no incluye transcripción ni evaluación). Para ver el costo real añade una Admin key de OpenAI.' };
}

function consumoGemini(ia: Awaited<ReturnType<typeof iaDelMes>>) {
  const propias = ia.filter((f) => f.proveedor === 'gemini');
  const enlace = 'https://aistudio.google.com/usage';
  if (!propias.length) return { tipo: 'sin datos', enlace, nota: 'Google no ofrece el consumo por API: revísalo en Google AI Studio → Usage.' };
  return {
    tipo: 'estimado', enlace, estimado: { coste: redondear(propias.reduce((a, f) => a + f.coste, 0)), conversaciones: propias.reduce((a, f) => a + f.conversaciones, 0), modelos: propias },
    nota: 'Estimado con los tokens registrados en conversaciones (la generación de ejercicios no se registra). El consumo real está en Google AI Studio → Usage.',
  };
}

/**
 * Stripe: ingresos del mes resumidos desde `GET /v1/balance_transactions`
 * (cobros menos reembolsos, comisiones y neto por moneda) y suscripciones
 * activas de Stripe según la tabla `suscripciones`.
 */
async function consumoStripe(op: Opciones) {
  const s = stripeConfig();
  const [loc] = await query<{ activas: number }>(
    `SELECT count(*) FILTER (WHERE origen = 'stripe' AND estado IN ('activa', 'prueba_stripe') AND modo IS NOT DISTINCT FROM $1)::int AS activas FROM suscripciones`, [s.modo]).catch(() => []);
  const activas = loc?.activas ?? 0;
  if (!s.secretKey) return { tipo: 'sin configurar', activas, nota: 'Vincula Stripe para ver los ingresos.' };
  try {
    const porMoneda = new Map<string, { bruto: number; comisiones: number; neto: number; cobros: number; reembolsos: number }>();
    let despues: string | null = null, vueltas = 0;
    do {
      const r: any = await llamarStripe(s.secretKey, 'GET', '/balance_transactions', { created: { gte: inicioDeMes() }, limit: 100, ...(despues ? { starting_after: despues } : {}) }, { timeoutMs: op.timeoutMs ?? TIMEOUT_MS });
      for (const b of r?.data ?? []) {
        if (!['charge', 'payment', 'refund', 'payment_refund'].includes(b?.type)) continue;
        const m = String(b.currency ?? 'usd'), x = porMoneda.get(m) ?? { bruto: 0, comisiones: 0, neto: 0, cobros: 0, reembolsos: 0 };
        x.bruto += Number(b.amount ?? 0); x.comisiones += Number(b.fee ?? 0); x.neto += Number(b.net ?? 0);
        if (b.type.includes('refund')) x.reembolsos++; else x.cobros++;
        porMoneda.set(m, x);
      }
      despues = r?.has_more ? r?.data?.at(-1)?.id ?? null : null;
    } while (despues && ++vueltas < 5);
    const c = (v: number) => Math.round(v) / 100;
    return {
      tipo: 'real', modo: s.modo, activas,
      ingresos: [...porMoneda].map(([moneda, x]) => ({ moneda, bruto: c(x.bruto), comisiones: c(x.comisiones), neto: c(x.neto), cobros: x.cobros, reembolsos: x.reembolsos })),
      ...(vueltas >= 5 ? { nota: 'Más de 500 movimientos este mes: se muestran los 500 más recientes.' } : {}),
    };
  } catch (e: any) {
    const m = e instanceof ErrorStripe ? (e.status === 403 ? 'La clave no tiene permiso «Balance → Read» para ver los ingresos.' : `Stripe respondió ${e.status}: ${e.message}`) : errorDeRed('Stripe', e, op.timeoutMs ?? TIMEOUT_MS).mensaje;
    return { tipo: 'error', modo: s.modo, activas, nota: m };
  }
}

/** GET /admin/conexiones/consumo: todos en paralelo; un fallo no tumba a los otros. */
export async function consumo(op: Opciones = {}) {
  const ia = await iaDelMes();
  const [e, o, g, st] = await Promise.allSettled([consumoEleven(op), consumoOpenAI(op, ia), Promise.resolve(consumoGemini(ia)), consumoStripe(op)]);
  const val = (r: PromiseSettledResult<any>) => r.status === 'fulfilled' ? r.value : { tipo: 'error', nota: 'No se pudo calcular el consumo.' };
  return { mes: new Date(inicioDeMes() * 1000).toISOString().slice(0, 7), elevenlabs: val(e), openai: val(o), gemini: val(g), stripe: val(st) };
}
