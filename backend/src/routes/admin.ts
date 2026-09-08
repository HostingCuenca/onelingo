import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { config } from '../lib/config.js';
import { query, uno } from '../lib/db.js';
import { requiereAdmin, type Sesion } from '../lib/auth.js';
import { iaDisponible, iaNombre } from '../lib/ia.js';
import { vozDisponible } from '../lib/voz.js';
import { openaiDisponible } from '../lib/ia_openai.js';
import { geminiDisponible } from '../lib/ia_gemini.js';

export default async function rutas(app: FastifyInstance) {
  app.post('/admin/login', async (req, reply) => {
    const { usuario, pin } = z.object({ usuario: z.string(), pin: z.string() }).parse(req.body);
    if (usuario !== config.adminUsuario || pin !== config.adminPin) return reply.code(401).send({ error: 'Usuario o PIN incorrectos' });
    return { token: app.jwt.sign({ sub: 'admin', rol: 'admin' } satisfies Sesion, { expiresIn: '12h' }) };
  });

  app.get('/admin/resumen', { preHandler: requiereAdmin }, async () => {
    const [tot] = await query(`SELECT count(*)::int AS usuarios,
        count(*) FILTER (WHERE ultima_actividad > now() - interval '7 days')::int AS activos7d,
        count(*) FILTER (WHERE creado_en > now() - interval '7 days')::int AS nuevos7d,
        count(*) FILTER (WHERE plan_id <> '')::int AS con_plan FROM usuarios`);
    const [prog] = await query(`SELECT coalesce(sum(lecciones_completadas),0)::int AS lecciones, coalesce(sum(xp),0)::int AS xp,
        coalesce(sum(segundos_estudio),0)::int AS segundos FROM progreso`);
    const porIdioma = await query(`SELECT idioma_meta AS idioma, count(*)::int AS usuarios FROM usuarios GROUP BY 1 ORDER BY 2 DESC`);
    const porNivel = await query(`SELECT nivel_actual AS nivel, count(*)::int AS usuarios FROM progreso GROUP BY 1 ORDER BY 1`);
    const examenes = await query(`SELECT count(*)::int AS total, count(*) FILTER (WHERE aprobado)::int AS aprobados, round(avg(pct))::int AS media FROM examenes`);
    const errores = await query(`SELECT skill, count(*)::int AS total FROM errores GROUP BY 1 ORDER BY 2 DESC`);
    const actividad = await query(`SELECT date_trunc('day', fecha)::date AS dia, count(*)::int AS eventos, count(DISTINCT usuario_id)::int AS usuarios
        FROM eventos WHERE fecha > now() - interval '14 days' GROUP BY 1 ORDER BY 1`);
    return { ...tot, ...prog, porIdioma, porNivel, examenes: examenes[0], errores, actividad };
  });

  app.get('/admin/usuarios', { preHandler: requiereAdmin }, async (req) => {
    const { q } = z.object({ q: z.string().optional() }).parse(req.query);
    return query(
      `SELECT u.id, u.email, u.nombre, u.idioma_nativo, u.idioma_meta, u.plan_id, u.tutor_id, u.trial_segundos, u.plataforma,
              u.creado_en, u.ultima_actividad,
              coalesce(p.nivel_actual, u.nivel_inicial) AS nivel_actual, coalesce(p.lecciones_completadas,0) AS lecciones,
              coalesce(p.xp,0) AS xp, coalesce(p.racha,0) AS racha, coalesce(p.segundos_estudio,0) AS segundos,
              (SELECT count(*)::int FROM errores e WHERE e.usuario_id = u.id AND NOT e.practicado) AS errores_pendientes
       FROM usuarios u LEFT JOIN progreso p ON p.usuario_id = u.id
       WHERE $1::text IS NULL OR u.nombre ILIKE '%'||$1||'%' OR u.email ILIKE '%'||$1||'%'
       ORDER BY u.ultima_actividad DESC LIMIT 200`,
      [q?.trim() || null],
    );
  });

  app.get('/admin/correos', { preHandler: requiereAdmin }, async () => query('SELECT id, para, asunto, enviado, detalle, fecha, cuerpo FROM correos ORDER BY fecha DESC LIMIT 50'));
  app.get('/admin/conversaciones', { preHandler: requiereAdmin }, async () => query(
    `SELECT c.id, c.fecha, c.nivel, c.idioma, c.tutor_id, c.situacion_id, c.mensaje_alumno, c.respuesta, c.modelo, c.tokens_entrada, c.tokens_salida, u.nombre, u.email
     FROM conversaciones c JOIN usuarios u ON u.id = c.usuario_id ORDER BY c.fecha DESC LIMIT 100`));
  app.get('/admin/estado-ia', { preHandler: requiereAdmin }, async () => ({
    ia: iaDisponible(), modelo: iaNombre(), proveedor: config.iaProveedor, google: config.googleClientIds.length > 0, smtp: !!config.smtp.host,
    servicios: {
      openai: { activo: openaiDisponible(), uso: 'Tutor conversacional y transcripción de voz', modelo: config.openaiModelo },
      gemini: { activo: geminiDisponible(), uso: 'Generación y personalización de ejercicios', modelo: config.geminiModelo },
      elevenlabs: { activo: vozDisponible(), uso: 'Voces y audios de Listening (con caché)', modelo: config.elevenModelo },
    },
  }));

  app.get('/admin/usuarios/:id', { preHandler: requiereAdmin }, async (req, reply) => {
    const { id } = z.object({ id: z.string().uuid() }).parse(req.params);
    const usuario = await uno('SELECT * FROM usuarios WHERE id = $1', [id]);
    if (!usuario) return reply.code(404).send({ error: 'No existe' });
    const progreso = await uno('SELECT * FROM progreso WHERE usuario_id = $1', [id]);
    const errores = await query('SELECT * FROM errores WHERE usuario_id = $1 ORDER BY fecha DESC LIMIT 100', [id]);
    const examenes = await query('SELECT * FROM examenes WHERE usuario_id = $1 ORDER BY nivel', [id]);
    const eventos = await query('SELECT tipo, datos, fecha FROM eventos WHERE usuario_id = $1 ORDER BY fecha DESC LIMIT 50', [id]);
    const estado = progreso?.estado ?? {};
    const completadas: string[] = estado.completadas ?? [];
    const porNivel = Array.from({ length: 10 }, (_, i) => ({ nivel: i + 1, lecciones: completadas.filter((c) => c.startsWith(`L${i + 1}-`)).length }));
    return { usuario, progreso, porNivel, errores, examenes, eventos };
  });
}
