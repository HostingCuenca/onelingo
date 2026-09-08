const BASE = '/api'
export class ApiError extends Error { status: number; constructor(m: string, s: number) { super(m); this.status = s } }
export const token = () => localStorage.getItem('onelingo.panel.token')
export const guardarToken = (t: string | null) => t ? localStorage.setItem('onelingo.panel.token', t) : localStorage.removeItem('onelingo.panel.token')
export async function api<T = any>(ruta: string, op: { metodo?: string; cuerpo?: unknown } = {}): Promise<T> {
  const r = await fetch(BASE + ruta, {
    method: op.metodo ?? 'GET',
    headers: { 'content-type': 'application/json', ...(token() ? { authorization: `Bearer ${token()}` } : {}) },
    body: op.cuerpo === undefined ? undefined : JSON.stringify(op.cuerpo),
  })
  const d = await r.json().catch(() => ({}))
  if (!r.ok) throw new ApiError(d.error ?? `Error ${r.status}`, r.status)
  return d as T
}
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
