import { z } from "zod";

/** Idiomas del contrato y sus reglas de escritura. */
export const IDIOMAS = {
  en: { nombre: "inglés", nativo: "English", romanizacion: null },
  es: { nombre: "español", nativo: "Español", romanizacion: null },
  fr: { nombre: "francés", nativo: "Français", romanizacion: null },
  de: { nombre: "alemán", nativo: "Deutsch", romanizacion: null },
  pt: { nombre: "portugués (Brasil)", nativo: "Português", romanizacion: null },
  it: { nombre: "italiano", nativo: "Italiano", romanizacion: null },
  zh: { nombre: "chino mandarín (caracteres simplificados)", nativo: "普通话", romanizacion: "pinyin con marcas de tono" },
  ja: { nombre: "japonés", nativo: "日本語", romanizacion: "romaji Hepburn" },
  ko: { nombre: "coreano", nativo: "한국어", romanizacion: "romanización revisada del coreano" },
  ru: { nombre: "ruso", nativo: "Русский", romanizacion: "transliteración latina simplificada (BGN/PCGN)" },
} as const;
export type Idioma = keyof typeof IDIOMAS;
export const CODIGOS = Object.keys(IDIOMAS) as Idioma[];
export const SIN_ESPACIOS: Idioma[] = ["zh", "ja"];

/** Una unidad generada: alimenta las 5 lecciones de la app y el banco del examen. */
export const UnidadSchema = z.object({
  titulo: z.string().describe("Título de la unidad en español, corto"),
  objetivo: z.string().describe("Qué sabrá hacer el alumno al terminar (una frase, tipo 'can do' del MCER)"),
  gramatica: z.string().describe("Punto gramatical de la unidad explicado en español en 2-3 frases"),
  vocab: z
    .array(
      z.object({
        palabra: z.string().describe("Palabra o expresión en el idioma meta, escritura nativa"),
        romanizacion: z.string().describe("Romanización si el idioma no usa alfabeto latino; cadena vacía si no aplica"),
        traduccion: z.string().describe("Traducción al español"),
        ejemplo: z.string().describe("Frase de ejemplo corta en el idioma meta que use la palabra"),
      }),
    )
    .min(8)
    .max(10),
  frases: z
    .array(
      z.object({
        texto: z.string().describe("Frase completa en el idioma meta (con espacios entre palabras aunque el idioma no los use)"),
        romanizacion: z.string().describe("Romanización o cadena vacía"),
        traduccion: z.string().describe("Traducción natural al español"),
      }),
    )
    .min(6)
    .max(8),
  dialogo: z
    .array(
      z.object({
        quien: z.string().describe("Rol del hablante, p. ej. 'Camarero' o 'Ana'"),
        texto: z.string().describe("Réplica en el idioma meta"),
        romanizacion: z.string(),
        traduccion: z.string(),
      }),
    )
    .min(4)
    .max(8)
    .describe("Diálogo breve de situación real que use el vocabulario y la gramática de la unidad"),
  errores_tipicos: z
    .array(
      z.object({
        incorrecto: z.string(),
        correcto: z.string(),
        explicacion: z.string().describe("Explicación en español de por qué es un error habitual para hispanohablantes"),
      }),
    )
    .min(2)
    .max(4),
  examen: z
    .array(
      z.object({
        pregunta: z.string().describe("Pregunta en español o en el idioma meta según el nivel"),
        opciones: z.array(z.string()).length(4),
        correcta: z.number().int().min(0).max(3),
        explicacion: z.string(),
      }),
    )
    .min(3)
    .max(4)
    .describe("Preguntas para el banco del examen final del nivel"),
});
export type Unidad = z.infer<typeof UnidadSchema>;

/** Fichero de unidad en disco: metadatos + contenido. */
export const FicheroUnidadSchema = z.object({
  idioma: z.enum(CODIGOS as [Idioma, ...Idioma[]]),
  nivel: z.number().int().min(1).max(10),
  unidad: z.number().int().min(1).max(20),
  tema: z.string(),
  cefr: z.string(),
  modelo: z.string(),
  generado: z.string(),
  contenido: UnidadSchema,
});
export type FicheroUnidad = z.infer<typeof FicheroUnidadSchema>;

/** Nivel 0 · Fundamentos: letras y sonidos, números, colores y palabras sueltas (sin frases). */
export const FundamentosUnidadSchema = z.object({
  tipo: z.enum(["escritura", "vocabulario"]),
  titulo: z.string(),
  descripcion: z.string(),
  items: z
    .array(z.object({ simbolo: z.string(), romanizacion: z.string(), significado: z.string(), ejemplo: z.string() }))
    .min(5)
    .max(48),
  examen: z
    .array(z.object({ pregunta: z.string(), opciones: z.array(z.string()).length(4), correcta: z.number().int().min(0).max(3), explicacion: z.string() }))
    .min(2)
    .max(4),
});
export const FicheroFundamentosSchema = z.object({
  idioma: z.enum(CODIGOS as [Idioma, ...Idioma[]]),
  nivel: z.literal(0),
  unidad: z.number().int().min(1).max(12),
  tema: z.string(),
  cefr: z.string(),
  modelo: z.string(),
  generado: z.string(),
  contenido: FundamentosUnidadSchema,
});

/** Diagnóstico adaptativo: banco de preguntas por nivel, competencia y tipo. */
export const TIPOS_DIAG = ["eleccion", "natural", "significado", "contexto", "situacion", "error", "completar", "corta", "escucha", "dictado", "escritura"] as const;
export const SKILLS_DIAG = ["comprension", "vocabulario", "gramatica", "tiempos", "expresiones", "contexto", "cotidiano", "escritura"] as const;
export const PreguntaDiagSchema = z.object({
  nivel: z.number().int().min(0).max(10),
  skill: z.enum(SKILLS_DIAG),
  tipo: z.enum(TIPOS_DIAG),
  tema: z.string().min(2),
  instruccion: z.string(),
  texto: z.string().min(1),
  opciones: z.array(z.string()).max(5),
  correcta: z.number().int().min(-1).max(4),
  aceptadas: z.array(z.string()),
  explicacion: z.string(),
}).refine((q) => q.tipo === "escritura" ? true : q.opciones.length >= 2 ? q.correcta >= 0 && q.correcta < q.opciones.length : q.aceptadas.length >= 1, {
  message: "las preguntas con opciones necesitan índice correcto; las de texto, respuestas aceptadas",
});
export const FicheroDiagSchema = z.object({ idioma: z.enum(CODIGOS as [Idioma, ...Idioma[]]), generado: z.string(), preguntas: z.array(PreguntaDiagSchema).min(10) });
