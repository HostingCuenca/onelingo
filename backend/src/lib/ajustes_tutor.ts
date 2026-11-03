import { z } from 'zod';
import { query } from './db.js';

/**
 * Ajustes del tutor IA que el administrador cambia desde el panel sin desplegar.
 * Se guardan versionados en `ajustes_tutor` (la última fila es la activa) y se
 * leen en memoria: ia.ts los aplica al armar el prompt de cada turno.
 */
export const AjustesTutor = z.object({
  /** guiar: clase con objetivo y pasos; equilibrado: charla que enseña; conversar: charla libre. */
  enfoque: z.enum(['guiar', 'equilibrado', 'conversar']).default('guiar'),
  /** Preguntas «¿X o Y?»: pocas (solo si se bloquea) o normal (a menudo en niveles bajos). */
  opciones: z.enum(['pocas', 'normal']).default('pocas'),
  /** Repetir lo que acaba de decir el alumno para confirmarlo («Coffee, yes»). */
  eco: z.boolean().default(false),
  /** Tras corregir en voz alta, pedirle que diga la frase completa. */
  pedirRepetir: z.boolean().default(true),
  /** Muletillas que el tutor no debe usar (en cualquier idioma). */
  frasesEvitar: z.array(z.string().trim().min(1).max(80)).max(40).default([]),
  /** Instrucciones extra del administrador, al final del diseño pedagógico. */
  instrucciones: z.string().trim().max(1500).default(''),
});
export type AjustesTutor = z.infer<typeof AjustesTutor>;

export const AJUSTES_TUTOR_DEFECTO: AjustesTutor = AjustesTutor.parse({
  // Las que más salían en las llamadas de oct-nov 2026.
  frasesEvitar: ['Just a small thing', 'Good choice', 'Sounds fun', 'Got it', 'That’s a great hobby', 'Pequeña cosa'],
});

let actual: AjustesTutor = AJUSTES_TUTOR_DEFECTO;
/** Ajustes vigentes (en memoria; se recargan al guardar). */
export const ajustesTutor = () => actual;

/** Lee la última versión guardada. Se llama al arrancar, tras migrar(). */
export async function cargarAjustesTutor() {
  const [f] = await query<{ datos: unknown }>('SELECT datos FROM ajustes_tutor ORDER BY id DESC LIMIT 1').catch(() => []);
  const r = f ? AjustesTutor.safeParse(f.datos) : null;
  actual = r?.success ? r.data : AJUSTES_TUTOR_DEFECTO;
  return actual;
}

export async function guardarAjustesTutor(datos: AjustesTutor, nota = '') {
  const a = AjustesTutor.parse(datos);
  await query('INSERT INTO ajustes_tutor (datos, nota) VALUES ($1, $2)', [a, nota.slice(0, 200)]);
  actual = a;
  return a;
}

export async function versionesTutor(limite = 20) {
  return query<{ id: number; datos: AjustesTutor; nota: string; creado_en: string }>(
    'SELECT id, datos, nota, creado_en FROM ajustes_tutor ORDER BY id DESC LIMIT $1', [limite]);
}
