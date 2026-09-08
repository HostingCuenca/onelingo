import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { query } from '../lib/db.js';
import { config } from '../lib/config.js';
import { generarJsonOpenAI, openaiDisponible } from '../lib/ia_openai.js';
import { generarJsonGemini, geminiDisponible } from '../lib/ia_gemini.js';
import { requiereAlumno, type Sesion } from '../lib/auth.js';
import { generarPregunta, generarPerfil, diagIaDisponible } from '../lib/diag_ia.js';

const IDIOMAS: Record<string, string> = { en: 'inglés', es: 'español', fr: 'francés', de: 'alemán', pt: 'portugués', it: 'italiano', zh: 'chino mandarín', ja: 'japonés', ko: 'coreano', ru: 'ruso' };

const ESQUEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    puntuacion: { type: 'number', description: 'Nivel de escritura estimado de 1 a 10 (1 = principiante absoluto, 5 = B1, 7 = B2, 10 = C2)' },
    gramatica: { type: 'number' }, vocabulario: { type: 'number' }, coherencia: { type: 'number' }, naturalidad: { type: 'number' },
    correccion: { type: 'string', description: 'Versión corregida del texto conservando la idea del alumno' },
    comentario: { type: 'string', description: 'Comentario breve en el idioma nativo del alumno: qué hace bien y qué debe mejorar' },
    errores: { type: 'array', items: { type: 'string' }, description: 'Temas gramaticales o de vocabulario a reforzar, en el idioma nativo, cortos (p. ej. "concordancia sujeto-verbo", "ortografía")' },
  },
  required: ['puntuacion', 'gramatica', 'vocabulario', 'coherencia', 'naturalidad', 'correccion', 'comentario', 'errores'],
};
const ESQUEMA_GEMINI = {
  type: 'OBJECT',
  properties: {
    puntuacion: { type: 'NUMBER' }, gramatica: { type: 'NUMBER' }, vocabulario: { type: 'NUMBER' }, coherencia: { type: 'NUMBER' }, naturalidad: { type: 'NUMBER' },
    correccion: { type: 'STRING' }, comentario: { type: 'STRING' }, errores: { type: 'ARRAY', items: { type: 'STRING' } },
  },
  required: ['puntuacion', 'gramatica', 'vocabulario', 'coherencia', 'naturalidad', 'correccion', 'comentario', 'errores'],
};

export default async function rutas(app: FastifyInstance) {
  /** Evalúa la producción escrita del diagnóstico adaptativo (OpenAI; Gemini de respaldo). */
  app.post('/diagnostico/escritura', { preHandler: requiereAlumno }, async (req, reply) => {
    const s = req.user as Sesion;
    const d = z.object({
      idiomaMeta: z.string(), idiomaNativo: z.string().default('es'), nivelEstimado: z.number().min(0).max(10),
      consigna: z.string(), texto: z.string().min(1).max(2000),
    }).parse(req.body);
    const system = `Eres un evaluador experto de ${IDIOMAS[d.idiomaMeta] ?? d.idiomaMeta} para hispanohablantes (app OneLingo).
Evalúa un texto breve escrito por un alumno como parte de un diagnóstico adaptativo de nivel (escala 1-10: 1 principiante absoluto, 2 A1, 3 A2, 4 A2+, 5 B1, 6 B1+, 7 B2, 8 B2+/C1, 9 C1+, 10 C2).
Mide claridad, coherencia, gramática, vocabulario, ortografía, naturalidad y complejidad. No penalices en exceso errores ortográficos menores si la comunicación es clara.
Calibración: un texto que comunica una idea con claridad, usa estructuras correctas de nivel intermedio (p. ej. "will make people's jobs easier", "because", "achieve results faster") y solo tiene dos o tres errores de ortografía o puntuación vale 6 (B1+), no 4. Reserva 3-4 para textos con errores que dificultan entender la idea, y 8-10 para textos naturales, precisos y con estructuras complejas bien usadas.
La estimación previa del sistema es ${d.nivelEstimado.toFixed(1)}; usa el texto para confirmarla o corregirla.
Devuelve la corrección conservando la idea del alumno, un comentario en ${IDIOMAS[d.idiomaNativo] ?? 'español'} y una lista corta de temas a reforzar (en ${IDIOMAS[d.idiomaNativo] ?? 'español'}). Sin emojis.`;
    const user = `Consigna: ${d.consigna}\n\nTexto del alumno:\n${d.texto}`;
    try {
      let json: any, modelo: string;
      if (openaiDisponible()) {
        const r = await generarJsonOpenAI(system, [{ role: 'user', content: user }], ESQUEMA, config.openaiModeloEvaluacion);
        json = r.json; modelo = r.modelo;
      } else if (geminiDisponible()) {
        const r = await generarJsonGemini(system, [{ role: 'user', text: user }], ESQUEMA_GEMINI);
        json = r.json; modelo = r.modelo;
      } else {
        return reply.code(503).send({ error: 'ia_no_configurada' });
      }
      const clamp = (v: unknown) => Math.min(10, Math.max(1, Number(v) || 1));
      const salida = {
        puntuacion: clamp(json.puntuacion), gramatica: clamp(json.gramatica), vocabulario: clamp(json.vocabulario), coherencia: clamp(json.coherencia), naturalidad: clamp(json.naturalidad),
        correccion: String(json.correccion ?? ''), comentario: String(json.comentario ?? ''), errores: (json.errores ?? []).map(String).slice(0, 6), modelo,
      };
      await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)', [s.sub, 'diagnostico_escritura', JSON.stringify({ idioma: d.idiomaMeta, nivelEstimado: d.nivelEstimado, puntuacion: salida.puntuacion, palabras: d.texto.split(/\s+/).length })]).catch(() => {});
      return salida;
    } catch (e) {
      req.log.error({ err: String(e) }, 'diagnostico');
      return reply.code(502).send({ error: 'ia_error', detalle: String(e).slice(0, 200) });
    }
  });

  /** Pregunta de diagnóstico generada por la IA para el nivel, competencia y tipo que pide el motor adaptativo. */
  app.post('/diagnostico/pregunta', { preHandler: requiereAlumno }, async (req, reply) => {
    if (!diagIaDisponible()) return reply.code(503).send({ error: 'ia_no_configurada' });
    const s = req.user as Sesion;
    const d = z.object({
      idiomaMeta: z.string(), idiomaNativo: z.string().default('es'), nivel: z.number().int().min(0).max(10),
      skill: z.string(), tipo: z.string(), evitar: z.array(z.string()).max(40).default([]),
      declarado: z.number().optional(), estimacion: z.number().optional(), debilidades: z.array(z.string()).optional(), aciertos: z.number().optional(), fallos: z.number().optional(),
    }).parse(req.body);
    // Hasta dos intentos: la IA a veces devuelve una pregunta mal formada.
    let ultimo = '';
    for (let i = 0; i < 2; i++) {
      try {
        const q = await generarPregunta(d);
        await query('INSERT INTO eventos (usuario_id, tipo, datos) VALUES ($1, $2, $3)', [s.sub, 'diagnostico_pregunta', JSON.stringify({ idioma: d.idiomaMeta, nivel: d.nivel, skill: d.skill, tipo: d.tipo, modelo: q.modelo })]).catch(() => {});
        return q;
      } catch (e) { ultimo = String(e); req.log.warn({ err: ultimo }, 'diagnostico pregunta'); }
    }
    return reply.code(502).send({ error: 'ia_error', detalle: ultimo.slice(0, 200) });
  });

  /** Resumen narrativo y plan personalizado del diagnóstico. */
  app.post('/diagnostico/perfil', { preHandler: requiereAlumno }, async (req, reply) => {
    if (!diagIaDisponible()) return reply.code(503).send({ error: 'ia_no_configurada' });
    const d = z.object({ idiomaMeta: z.string(), idiomaNativo: z.string().default('es'), resultado: z.record(z.any()) }).parse(req.body);
    try { return await generarPerfil(d); }
    catch (e) { req.log.error({ err: String(e) }, 'diagnostico perfil'); return reply.code(502).send({ error: 'ia_error', detalle: String(e).slice(0, 200) }); }
  });

  app.get('/diagnostico/estado', async () => ({ ia: openaiDisponible() || geminiDisponible(), preguntas: diagIaDisponible() ? (geminiDisponible() ? 'gemini' : 'openai') : 'semilla', escritura: openaiDisponible() ? config.openaiModeloEvaluacion : geminiDisponible() ? config.geminiModelo : 'local' }));
}
