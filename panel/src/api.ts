const BASE = '/api'
export class ApiError extends Error { status: number; datos?: any; constructor(m: string, s: number, d?: any) { super(m); this.status = s; this.datos = d } }
export const token = () => localStorage.getItem('onelingo.panel.token')
export const guardarToken = (t: string | null) => t ? localStorage.setItem('onelingo.panel.token', t) : localStorage.removeItem('onelingo.panel.token')
/** Evento que avisa a la app de que la sesión caducó o ya no vale: vuelve al login. */
export const SESION_CADUCADA = 'onelingo-panel:sesion-caducada'
const SIN_RED = 'No se pudo conectar con el servidor. Revisa tu conexión a internet y vuelve a intentar.'
const espera = (ms: number) => new Promise((r) => setTimeout(r, ms))
/** fetch con mensajes claros: sin red reintenta las lecturas una vez; un 401 cierra la sesión. */
async function pedir(ruta: string, init: RequestInit): Promise<Response> {
  const metodo = init.method ?? 'GET'
  let r: Response | null = null
  for (let intento = 0; intento < (metodo === 'GET' ? 3 : 1) && !r; intento++) {
    if (intento) await espera(800 * intento)
    try { r = await fetch(BASE + ruta, init) } catch { r = null }
  }
  if (!r) throw new ApiError(SIN_RED, 0)
  if (r.status === 401 && ruta !== '/admin/login' && token()) { guardarToken(null); window.dispatchEvent(new Event(SESION_CADUCADA)) }
  return r
}
export async function api<T = any>(ruta: string, op: { metodo?: string; cuerpo?: unknown } = {}): Promise<T> {
  const r = await pedir(ruta, {
    method: op.metodo ?? 'GET',
    // Sin cuerpo no se manda content-type: Fastify rechaza un JSON vacío (DELETE, POST sin datos).
    headers: { ...(op.cuerpo === undefined ? {} : { 'content-type': 'application/json' }), ...(token() ? { authorization: `Bearer ${token()}` } : {}) },
    body: op.cuerpo === undefined ? undefined : JSON.stringify(op.cuerpo),
  })
  const d = await r.json().catch(() => ({}))
  if (!r.ok) throw new ApiError(d.error ?? mensajeHttp(r.status), r.status, d)
  return d as T
}
const mensajeHttp = (s: number) => s >= 502 && s <= 504 ? 'El servidor se está reiniciando. Espera unos segundos y vuelve a intentar.' : `Error ${s}`
export const fecha = (v?: string | null) => v ? new Date(v).toLocaleString('es-EC', { dateStyle: 'short', timeStyle: 'short' }) : '—'
export const hace = (v?: string | null) => {
  if (!v) return '—'
  const m = Math.round((Date.now() - new Date(v).getTime()) / 60000)
  if (m < 1) return 'ahora'; if (m < 60) return `hace ${m} min`; if (m < 1440) return `hace ${Math.round(m / 60)} h`; return `hace ${Math.round(m / 1440)} d`
}
export const minutos = (s: number) => s < 3600 ? `${Math.round(s / 60)} min` : `${(s / 3600).toFixed(1)} h`
export const IDIOMAS: Record<string, string> = { en: 'Inglés', es: 'Español', fr: 'Francés', de: 'Alemán', pt: 'Portugués', it: 'Italiano', zh: 'Chino', ja: 'Japonés', ko: 'Coreano', ru: 'Ruso' }
export const NIVELES = ['Básico', 'Básico', 'Básico Av.', 'Intermedio', 'Intermedio', 'Interm. Av.', 'Avanzado', 'Avanzado', 'Av. Superior', 'Dominio']
export const PLANES: Record<string, string> = { '': 'Prueba gratuita', p1: '1 idioma · $20', p2: '2 idiomas · $30', p3: '3 idiomas · $40' }
export const SKILLS: Record<string, string> = { gramatica: 'Gramática', vocabulario: 'Vocabulario', conjugacion: 'Conjugación', listening: 'Listening', pronunciacion: 'Pronunciación', frases: 'Formación de frases', escritura: 'Escritura' }
/** Descarga un archivo de la API (con la sesión del panel). */
export async function descargar(ruta: string, nombre: string) {
  const r = await pedir(ruta, { headers: token() ? { authorization: `Bearer ${token()}` } : {} })
  if (!r.ok) throw new ApiError(mensajeHttp(r.status), r.status)
  const url = URL.createObjectURL(await r.blob())
  const a = document.createElement('a'); a.href = url; a.download = nombre; document.body.appendChild(a); a.click(); a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
export const PLATAFORMAS: Record<string, string> = { web: 'Web', android: 'Android', ios: 'iPhone / iPad', macos: 'Mac', windows: 'Windows', linux: 'Linux', desconocida: 'Sin dato' }
export const nivelCorto = (n: number | null | undefined) => n === null || n === undefined ? '—' : n === 0 ? 'F0' : `N${n}`
export const usd = (v: number) => `$${v < 1 ? v.toFixed(v < 0.01 && v > 0 ? 4 : 2) : v.toFixed(2)}`
export const num = (v: number) => Number(v ?? 0).toLocaleString('es')
/** Estado de una suscripción → [clase de pill, etiqueta]. */
export const ESTADOS: Record<string, [string, string]> = {
  activa: ['ok', 'Activa'], prueba_stripe: ['ok', 'Prueba (Stripe)'], impago: ['mal', 'Impago'], cancelada: ['trial', 'Cancelada'], vencida: ['mal', 'Vencida'], sin_plan: ['', 'Sin plan'],
}
