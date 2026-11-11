/**
 * Informes de videollamada en el panel: los de cada alumno (retroalimentación
 * para él) y la calidad por tutor (para mejorar el tutor con llamadas reales).
 */
import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { query } from '../lib/db.js';
import { requiereAdmin } from '../lib/auth.js';
import { CRITERIOS } from '../lib/informe_llamada.js';

const promedio = (c: string) => `round(avg((evaluacion->'puntos'->>'${c}')::numeric), 1)::float AS "${c}"`;

export default async function rutas(app: FastifyInstance) {
  app.get('/admin/usuarios/:id/informes', { preHandler: requiereAdmin }, async (req) => {
    const { id } = z.object({ id: z.string().uuid() }).parse(req.params);
    return query(`SELECT id, idioma, nivel, tutor_id AS "tutorId", explica, turnos, resumen, evaluacion, tecnico, nota::float, creado_en AS "creadoEn"
      FROM informes_llamada WHERE usuario_id = $1 ORDER BY creado_en DESC LIMIT 50`, [id]);
  });

  /** Calidad de las llamadas: promedio por tutor, problemas más repetidos y últimas llamadas. */
  app.get('/admin/informes-llamada', { preHandler: requiereAdmin }, async (req) => {
    const { dias, tutor } = z.object({ dias: z.coerce.number().int().min(1).max(365).default(30), tutor: z.string().max(40).default('') }).parse(req.query);
    const filtro = `creado_en > now() - make_interval(days => $1::int) AND ($2 = '' OR tutor_id = $2)`;
    const porTutor = await query(`SELECT tutor_id AS "tutorId", count(*)::int AS llamadas, count(evaluacion)::int AS evaluadas,
        round(avg(nota), 1)::float AS nota, ${Object.keys(CRITERIOS).map(promedio).join(', ')},
        coalesce(sum((tecnico->>'frasesRespaldo')::int), 0)::int AS "frasesRespaldo", coalesce(sum((tecnico->>'frasesTutor')::int), 0)::int AS "frasesTutor",
        coalesce(sum((tecnico->>'turnosVivo')::int), 0)::int AS "turnosVivo", coalesce(sum((tecnico->>'turnosPulsar')::int), 0)::int AS "turnosPulsar",
        coalesce(sum((tecnico->>'cortesVivo')::int), 0)::int AS "cortesVivo"
      FROM informes_llamada WHERE ${filtro} GROUP BY tutor_id ORDER BY llamadas DESC`, [dias, tutor]);
    const problemas = await query(`SELECT p->>'criterio' AS criterio, count(*)::int AS veces, (array_agg(p->>'cita' ORDER BY i.creado_en DESC))[1:3] AS ejemplos
      FROM informes_llamada i, jsonb_array_elements(coalesce(i.evaluacion->'problemas', '[]')) p
      WHERE ${filtro.replace(/creado_en/g, 'i.creado_en').replace('tutor_id', 'i.tutor_id')} GROUP BY 1 ORDER BY veces DESC`, [dias, tutor]);
    const recientes = await query(`SELECT i.id, i.usuario_id AS "usuarioId", u.nombre, u.apellido, i.idioma, i.nivel, i.tutor_id AS "tutorId", i.explica, i.turnos,
        i.nota::float, i.evaluacion->>'recomendacion' AS recomendacion, i.tecnico, i.creado_en AS "creadoEn"
      FROM informes_llamada i JOIN usuarios u ON u.id = i.usuario_id WHERE ${filtro.replace(/creado_en/g, 'i.creado_en').replace('tutor_id', 'i.tutor_id')} ORDER BY i.creado_en DESC LIMIT 60`, [dias, tutor]);
    return { criterios: CRITERIOS, porTutor, problemas, recientes };
  });
}
