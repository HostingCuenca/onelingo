import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { IDIOMAS, SIN_ESPACIOS, type Idioma } from "./esquema.js";

const aqui = path.dirname(fileURLToPath(import.meta.url));
export const RAIZ = path.resolve(aqui, "../../..");

export type PlanNivel = {
  numero: number; nombre: string; cefr: string; descripcion: string; gramatica: string;
  horas_aprox: number; vocabulario_acumulado: number; unidades: { numero: number; tema: string }[];
};
export type Plan = { version: number; niveles: PlanNivel[] };

export function cargarPlan(): Plan {
  return JSON.parse(fs.readFileSync(path.join(RAIZ, "content/plan-curricular.json"), "utf8"));
}

/** Prompt de sistema estable (se cachea): reglas pedagógicas comunes a todas las unidades. */
export function systemPrompt(): string {
  return `Eres el autor de contenido de OneLingo, una app para hispanohablantes que aprenden idiomas.
Escribes unidades didácticas alineadas al Marco Común Europeo (MCER) y a los manuales de referencia
de cada idioma (English File, Aula Internacional, Alter Ego+, Menschen, Nuovo Espresso, Português XXI,
HSK Standard Course, Genki, Sejong Korean, Поехали!). El alumno ve: flashcards (palabra + traducción),
ejercicios de elegir, completar huecos, ordenar palabras, dictado, unir parejas, repetir en voz alta,
un diálogo de situación real y preguntas de examen.

Reglas:
- Todo lo que sea explicación, traducción, objetivo o gramática va en español neutro (Latinoamérica/España).
- El vocabulario y las frases van SOLO en el idioma meta, sin traducción dentro del texto nativo.
- Usa vocabulario y estructuras estrictamente del nivel MCER indicado; nunca por encima.
- Las frases deben ser naturales, útiles en la vida real y reutilizar el vocabulario de la unidad.
- En idiomas sin espacios entre palabras (chino, japonés) escribe las frases y el diálogo separando cada
  palabra con un espacio (como en los manuales para principiantes) para que la app pueda ordenar palabras.
- Si el idioma no usa alfabeto latino, rellena SIEMPRE la romanización (pinyin con tonos, Hepburn,
  romanización revisada del coreano, transliteración del cirílico). Si usa alfabeto latino, déjala vacía.
- Los errores típicos deben ser los que cometen hispanohablantes en ese idioma (interferencia del español).
- Las preguntas de examen deben poder responderse con lo aprendido en la unidad; una sola opción correcta.
- Sin emojis. Sin comentarios fuera del JSON.`;
}

export function userPrompt(idioma: Idioma, nivel: PlanNivel, unidad: { numero: number; tema: string }): string {
  const meta = IDIOMAS[idioma];
  const rom = meta.romanizacion ? `Romanización obligatoria: ${meta.romanizacion}.` : "Este idioma usa alfabeto latino: deja 'romanizacion' vacía.";
  const espacios = SIN_ESPACIOS.includes(idioma) ? "Separa cada palabra con un espacio en frases y diálogo." : "";
  const idiomaExamen = nivel.numero <= 3 ? "Las preguntas del examen van en español; las opciones en el idioma meta." : "Preguntas y opciones del examen en el idioma meta.";
  return `Idioma meta: ${meta.nombre} (${meta.nativo}).
Nivel OneLingo ${nivel.numero} de 10 · ${nivel.nombre} · MCER ${nivel.cefr}.
Descripción del nivel: ${nivel.descripcion}
Gramática esperada en este nivel: ${nivel.gramatica}
Vocabulario acumulado objetivo al terminar el nivel: ${nivel.vocabulario_acumulado} palabras.

Unidad ${unidad.numero} de 20: "${unidad.tema}".
${rom} ${espacios}
${idiomaExamen}

Genera la unidad completa siguiendo el esquema: 8-10 palabras de vocabulario con ejemplo, 6-8 frases,
un diálogo de 4-8 réplicas en una situación real relacionada con el tema, 2-4 errores típicos de
hispanohablantes y 3-4 preguntas de examen.`;
}
