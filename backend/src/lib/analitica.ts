/**
 * Analíticas del panel de administración: funciones puras (testeables) y
 * tarifas para estimar costes. Lo que mide cada métrica está en
 * docs/PANEL_ADMIN.md.
 */
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

/** Zona horaria en la que se cuentan los días (registros, activos…). */
export const ZONA_HORARIA = 'America/Guayaquil';

/** Minutos de prueba gratis (igual que `segundosPruebaGratis` en lib/core/content/catalog.dart). */
export const SEGUNDOS_PRUEBA = 60 * 60;

/** Una clase empezada y sin aprobar cuenta como abandonada pasados estos días. */
export const DIAS_ABANDONO = 2;

/**
 * Tarifas de IA en USD por millón de tokens (entrada, salida). Se busca por
 * prefijo del modelo guardado en `conversaciones.modelo` (gana el más largo):
 * "gpt-4.1-mini-2025-04-14" usa "gpt-4.1-mini". Revisa los precios del
 * proveedor y cámbialos aquí; el resto del panel se recalcula solo.
 */
export const TARIFAS_IA: Record<string, { entrada: number; salida: number }> = {
  'gpt-4.1-mini': { entrada: 0.4, salida: 1.6 },
  'gpt-4.1-nano': { entrada: 0.1, salida: 0.4 },
  'gpt-4.1': { entrada: 2, salida: 8 },
  'gpt-4o-mini': { entrada: 0.15, salida: 0.6 },
  'gpt-4o': { entrada: 2.5, salida: 10 },
  'gemini': { entrada: 0.3, salida: 2.5 },
  'claude': { entrada: 5, salida: 25 },
};
/** Si el modelo no coincide con ninguna tarifa (estimación conservadora). */
export const TARIFA_IA_DESCONOCIDA = { entrada: 2, salida: 8 };

/**
 * ElevenLabs: USD estimados por cada 1.000 caracteres sintetizados. Depende
 * del plan contratado (créditos/mes ÷ precio) y del modelo (flash gasta ~0,5
 * créditos por carácter). Ajusta este valor a tu factura real.
 */
export const USD_POR_MIL_CARACTERES_VOZ = 0.11;

export function tarifaDe(modelo: string) {
  const m = modelo.toLowerCase();
  let mejor = '';
  for (const k of Object.keys(TARIFAS_IA)) if (m.startsWith(k) && k.length > mejor.length) mejor = k;
  return mejor ? TARIFAS_IA[mejor] : TARIFA_IA_DESCONOCIDA;
}

export function costeIa(modelo: string, entrada: number, salida: number) {
  const t = tarifaDe(modelo);
  return (entrada * t.entrada + salida * t.salida) / 1_000_000;
}

export const costeVoz = (caracteres: number) => (caracteres / 1000) * USD_POR_MIL_CARACTERES_VOZ;

export type InfoClase = { idioma: string | null; nivel: number | null; legado: boolean };

/**
 * Idioma y nivel (0 = Fundamentos, 1–10) de una clase completada.
 * - Ruta actual: `ja.n3.c06`, `en.n1.class-01`, `en.f0.primer-contacto`,
 *   `en.a1.posesivos` (bloque A1 = nivel 1).
 * - Legado: `L3-012` (lecciones antiguas, sin idioma en el id).
 */
export function infoClase(id: string): InfoClase {
  const legado = /^L(\d{1,2})-\d+$/.exec(id);
  if (legado) return { idioma: null, nivel: Number(legado[1]), legado: true };
  const [idioma, tramo] = id.split('.');
  if (!idioma || !tramo || !/^[a-z]{2}$/.test(idioma)) return { idioma: null, nivel: null, legado: false };
  let nivel: number | null = null;
  const n = /^n(\d{1,2})$/.exec(tramo);
  if (n) nivel = Number(n[1]);
  else if (tramo === 'f0') nivel = 0;
  else if (/^a1(-|$)/.test(tramo)) nivel = 1;
  else if (/^a2(-|$)/.test(tramo)) nivel = 2;
  return { idioma, nivel: nivel !== null && nivel <= 10 ? nivel : null, legado: false };
}

/** Columnas de la tabla idioma × nivel. */
export const NIVELES_TABLA = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

export type Aprobada = { usuario_id: string; unidad: string; fecha: string | null; idioma_usuario?: string };

/** Cuenta clases por idioma y nivel. Las del legado toman el idioma del alumno. */
export function tablaIdiomaNivel(clases: Aprobada[]) {
  const t = new Map<string, Record<number, number>>();
  for (const c of clases) {
    const i = infoClase(c.unidad);
    const idioma = i.idioma ?? c.idioma_usuario ?? '?';
    if (i.nivel === null) continue;
    const fila = t.get(idioma) ?? {};
    fila[i.nivel] = (fila[i.nivel] ?? 0) + 1;
    t.set(idioma, fila);
  }
  return [...t.entries()]
    .map(([idioma, fila]) => ({ idioma, niveles: NIVELES_TABLA.map((n) => fila[n] ?? 0), total: Object.values(fila).reduce((a, b) => a + b, 0) }))
    .sort((a, b) => b.total - a.total);
}

/** Día local `yyyy-mm-dd` de una fecha ISO guardada por la app (hora local del dispositivo). */
export function diaDe(fecha: string | null | undefined): string | null {
  if (!fecha) return null;
  const m = /^(\d{4}-\d{2}-\d{2})/.exec(fecha);
  return m ? m[1] : null;
}

/** Serie continua de `dias` días terminando en `hoy` (yyyy-mm-dd). */
export function serieDias(hoy: string, dias: number): string[] {
  const fin = new Date(`${hoy}T12:00:00Z`);
  return Array.from({ length: dias }, (_, i) => {
    const d = new Date(fin); d.setUTCDate(fin.getUTCDate() - (dias - 1 - i));
    return d.toISOString().slice(0, 10);
  });
}

/** CSV con separador `;` (Excel en español) y comillas cuando hace falta. */
export function aCsv(filas: Record<string, unknown>[], columnas: string[]): string {
  const celda = (v: unknown) => {
    const s = v === null || v === undefined ? '' : v instanceof Date ? v.toISOString() : String(v);
    return /[;"\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  return [columnas.join(';'), ...filas.map((f) => columnas.map((c) => celda(f[c])).join(';'))].join('\n');
}

// ── Catálogo de clases (títulos y totales por nivel) ─────────────────────────
// La API no empaqueta el contenido: se lee, si existe, de la web publicada
// (`../web/assets/assets/contenido`) o del repositorio (`assets/contenido`).
// Se carga una sola vez, archivo a archivo, y solo se conservan id/título/nivel.

export type ClaseCatalogo = { titulo: string; idioma: string; nivel: number | null };
let catalogo: Map<string, ClaseCatalogo> | null = null;
let cargando: Promise<void> | null = null;

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', '..');
export const RAICES_CONTENIDO = [
  path.join(raiz, 'web', 'assets', 'assets', 'contenido'),
  path.join(raiz, 'assets', 'contenido'),
  path.join(raiz, 'build', 'web', 'assets', 'assets', 'contenido'),
];

const textoDe = (t: unknown) => typeof t === 'string' ? t : t && typeof t === 'object' ? String((t as any).es ?? Object.values(t)[0] ?? '') : '';

async function cargarCatalogo(raices: string[]) {
  const m = new Map<string, ClaseCatalogo>();
  for (const base of raices) {
    let idiomas: string[];
    try { idiomas = await readdir(base); } catch { continue; }
    for (const idioma of idiomas) {
      let archivos: string[];
      try { archivos = (await readdir(path.join(base, idioma, 'ruta'))).filter((f) => f.endsWith('.json') && f !== 'curso.json'); } catch { continue; }
      for (const f of archivos) {
        try {
          const j = JSON.parse(await readFile(path.join(base, idioma, 'ruta', f), 'utf8'));
          for (const u of j?.unidades ?? []) {
            if (typeof u?.id !== 'string' || m.has(u.id)) continue;
            m.set(u.id, { titulo: textoDe(u.titulo), idioma, nivel: typeof u.nivelInterno === 'number' ? u.nivelInterno : infoClase(u.id).nivel });
          }
        } catch { /* archivo ilegible: se omite */ }
      }
    }
    if (m.size) break; // la primera raíz con contenido manda
  }
  catalogo = m;
}

/** Catálogo si ya está cargado; si no, empieza a cargarlo y devuelve null. */
export function catalogoClases(raices = RAICES_CONTENIDO): Map<string, ClaseCatalogo> | null {
  if (catalogo) return catalogo;
  cargando ??= cargarCatalogo(raices).catch(() => { catalogo = new Map(); });
  return null;
}

/** Espera al catálogo (tests y primera carga). */
export async function esperarCatalogo(raices = RAICES_CONTENIDO) {
  catalogoClases(raices);
  await cargando;
  return catalogo!;
}

/** Total de clases publicadas por idioma y nivel según el catálogo. */
export function totalesCatalogo(c: Map<string, ClaseCatalogo> | null) {
  const t: Record<string, Record<number, number>> = {};
  for (const v of c?.values() ?? []) {
    if (v.nivel === null) continue;
    (t[v.idioma] ??= {})[v.nivel] = (t[v.idioma][v.nivel] ?? 0) + 1;
  }
  return t;
}

// ── Clases a partir de `progreso.estado` ────────────────────────────────────

/**
 * Una fila por evidencia relevante del estado sincronizado:
 * - `evaluacion`: `practicas['ruta:<unidad>:evaluacion']` (aprobada = clase completada);
 * - `visto`: `practicas['ruta:<unidad>:visto']` (el alumno abrió la clase);
 * - `legado`: id de `completadas` (lecciones antiguas `L<n>-<nnn>`).
 */
export type FilaClase = {
  usuario_id: string; idioma_usuario: string; unidad: string;
  clave: 'evaluacion' | 'visto' | 'legado'; aprobada: boolean; fecha: string | null; intentos: number;
};

export type ResumenClases = {
  aprobadas: Aprobada[];
  porUsuario: Map<string, { clases: number; ultima: string | null; nivelMax: Record<string, number> }>;
  masHechas: { unidad: string; alumnos: number }[];
  abandonos: { unidad: string; alumnos: number }[];
  suspensos: { unidad: string; alumnos: number }[];
};

const top = (m: Map<string, number>, n = 10) =>
  [...m.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, n).map(([unidad, alumnos]) => ({ unidad, alumnos }));

export function resumirClases(filas: FilaClase[], hoy: string, diasAbandono = DIAS_ABANDONO): ResumenClases {
  const limite = serieDias(hoy, diasAbandono + 1)[0]; // vistas ese día o antes
  const aprobadasSet = new Set<string>();
  const aprobadas: Aprobada[] = [];
  for (const f of filas) {
    if (f.clave === 'visto' || (f.clave === 'evaluacion' && !f.aprobada)) continue;
    const k = `${f.usuario_id}|${f.unidad}`;
    if (aprobadasSet.has(k)) continue;
    aprobadasSet.add(k);
    aprobadas.push({ usuario_id: f.usuario_id, unidad: f.unidad, fecha: f.fecha, idioma_usuario: f.idioma_usuario });
  }
  const porUsuario: ResumenClases['porUsuario'] = new Map();
  const masHechas = new Map<string, number>();
  for (const a of aprobadas) {
    const u = porUsuario.get(a.usuario_id) ?? { clases: 0, ultima: null, nivelMax: {} };
    u.clases++;
    if (a.fecha && (!u.ultima || a.fecha > u.ultima)) u.ultima = a.fecha;
    const i = infoClase(a.unidad), idioma = i.idioma ?? a.idioma_usuario ?? '?';
    if (i.nivel !== null) u.nivelMax[idioma] = Math.max(u.nivelMax[idioma] ?? 0, i.nivel);
    porUsuario.set(a.usuario_id, u);
    if (!infoClase(a.unidad).legado) masHechas.set(a.unidad, (masHechas.get(a.unidad) ?? 0) + 1);
  }
  const abandonos = new Map<string, number>(), suspensos = new Map<string, number>();
  for (const f of filas) {
    if (aprobadasSet.has(`${f.usuario_id}|${f.unidad}`)) continue;
    if (f.clave === 'evaluacion') suspensos.set(f.unidad, (suspensos.get(f.unidad) ?? 0) + 1);
    const dia = diaDe(f.fecha);
    if (f.clave === 'visto' && dia && dia <= limite) abandonos.set(f.unidad, (abandonos.get(f.unidad) ?? 0) + 1);
  }
  return { aprobadas, porUsuario, masHechas: top(masHechas), abandonos: top(abandonos), suspensos: top(suspensos) };
}

/** Catálogo esperando como mucho `ms` a que termine la primera carga. */
export async function catalogoConEspera(ms = 3000) {
  const listo = catalogoClases();
  if (listo) return listo;
  await Promise.race([cargando, new Promise((r) => setTimeout(r, ms).unref())]);
  return catalogo;
}
