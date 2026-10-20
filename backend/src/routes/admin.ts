import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { config } from '../lib/config.js';
import { query, uno } from '../lib/db.js';
import { requiereAdmin, type Sesion } from '../lib/auth.js';
import { iaDisponible, iaNombre } from '../lib/ia.js';
import { vozDisponible } from '../lib/voz.js';
import { openaiDisponible } from '../lib/ia_openai.js';
import { geminiDisponible } from '../lib/ia_gemini.js';
import {
  aCsv, catalogoClases, catalogoConEspera, costeIa, costeVoz, DIAS_ABANDONO, diaDe, infoClase, NIVELES_TABLA, resumirClases,
  serieDias, tablaIdiomaNivel, tarifaDe, totalesCatalogo, USD_POR_MIL_CARACTERES_VOZ, ZONA_HORARIA, type FilaClase,
} from '../lib/analitica.js';
import { ajustesPago } from '../lib/pagos/planes.js';
import { filaDe, metricasSuscripciones, refrescarPlanesDerivados, suscripcionDe } from '../lib/pagos/suscripciones.js';

/**
 * Días en que cada alumno tuvo actividad ($1 = zona horaria): eventos,
 * turnos con el tutor, días que la app registra en `estado.diasActividad`
 * y la última actividad conocida. `h.hoy` es el día actual en esa zona.
 */
const DIAS_ACTIVOS = `dias_activos AS (
  SELECT usuario_id, (fecha AT TIME ZONE $1)::date AS dia FROM eventos
  UNION SELECT usuario_id, (fecha AT TIME ZONE $1)::date FROM conversaciones
  UNION SELECT p.usuario_id, d::date FROM progreso p,
    jsonb_array_elements_text(CASE WHEN jsonb_typeof(p.estado->'diasActividad') = 'array' THEN p.estado->'diasActividad' ELSE '[]'::jsonb END) d
    WHERE d ~ '^20[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
  UNION SELECT id, (ultima_actividad AT TIME ZONE $1)::date FROM usuarios
), h AS (SELECT (now() AT TIME ZONE $1)::date AS hoy)`;

/** Clases aprobadas, vistas y del legado de todos los alumnos o de los indicados. */
async function filasClases(ids?: string[]): Promise<FilaClase[]> {
  const filtro = ids ? 'WHERE p.usuario_id = ANY($1::uuid[])' : '';
  return query<FilaClase>(
    `WITH pr AS (SELECT p.usuario_id, p.estado, u.idioma_meta FROM progreso p JOIN usuarios u ON u.id = p.usuario_id ${filtro})
     SELECT pr.usuario_id, pr.idioma_meta AS idioma_usuario, split_part(e.k, ':', 2) AS unidad, split_part(e.k, ':', 3) AS clave,
            coalesce(e.v->>'aprobada', '') = 'true' AS aprobada, coalesce(e.v->>'fechaAprobada', e.v->>'fecha') AS fecha,
            CASE WHEN e.v->>'intentos' ~ '^[0-9]{1,6}$' THEN (e.v->>'intentos')::int ELSE 1 END AS intentos
     FROM pr, jsonb_each(CASE WHEN jsonb_typeof(pr.estado->'practicas') = 'object' THEN pr.estado->'practicas' ELSE '{}'::jsonb END) e(k, v)
     WHERE e.k ~ '^ruta:[^:]+:(evaluacion|visto)$' AND jsonb_typeof(e.v) = 'object'
     UNION ALL
     SELECT pr.usuario_id, pr.idioma_meta, c, 'legado', true, NULL, 1
     FROM pr, jsonb_array_elements_text(CASE WHEN jsonb_typeof(pr.estado->'completadas') = 'array' THEN pr.estado->'completadas' ELSE '[]'::jsonb END) c`,
    ids ? [ids] : [],
  );
}

const tituloDe = (unidad: string) => catalogoClases()?.get(unidad)?.titulo ?? '';
const conTitulo = <T extends { unidad: string }>(l: T[]) => l.map((x) => ({ ...x, titulo: tituloDe(x.unidad), ...infoClase(x.unidad) }));
const redondear = (n: number, d = 2) => Math.round(n * 10 ** d) / 10 ** d;
const suma = (l: any[], k: string) => l.reduce((a, x) => a + Number(x[k] ?? 0), 0);
const hoyLocal = () => new Date().toLocaleDateString('en-CA', { timeZone: ZONA_HORARIA });

export const FiltrosUsuarios = z.object({
  q: z.string().optional(),
  idioma: z.string().optional(),
  plataforma: z.string().optional(),
  estado: z.enum(['activos', 'inactivos', '']).optional(),
  plan: z.enum(['pago', 'prueba', '']).optional(),
  orden: z.enum(['ultima_actividad', 'creado_en', 'nombre', 'clases', 'xp', 'segundos', 'conversaciones']).default('ultima_actividad'),
  dir: z.enum(['asc', 'desc']).default('desc'),
  limite: z.coerce.number().int().min(1).max(5000).default(300),
});
const vacio = (v?: string) => (v?.trim() ? v.trim() : null);

/** Alumnos filtrados (hasta 5000), con sus clases completadas, ordenados. */
async function listarUsuarios(f: z.infer<typeof FiltrosUsuarios>) {
  await refrescarPlanesDerivados(); // cortesías o periodos que caducaron
  const filas = await query(
    `SELECT u.id, u.email, u.nombre, u.idioma_nativo, u.idioma_meta, u.plan_id, u.tutor_id, u.trial_segundos,
            CASE WHEN u.plataforma = '' THEN 'desconocida' ELSE u.plataforma END AS plataforma, u.es_demo,
            u.creado_en, u.ultima_actividad, coalesce(p.nivel_actual, u.nivel_inicial) AS nivel_actual,
            coalesce(p.xp, 0) AS xp, coalesce(p.racha, 0) AS racha, coalesce(p.segundos_estudio, 0) AS segundos,
            (SELECT count(*)::int FROM errores e WHERE e.usuario_id = u.id AND NOT e.practicado) AS errores_pendientes,
            (SELECT count(*)::int FROM conversaciones c WHERE c.usuario_id = u.id) AS conversaciones,
            u.ultima_actividad > now() - interval '7 days' AS activo
     FROM usuarios u LEFT JOIN progreso p ON p.usuario_id = u.id
     WHERE ($1::text IS NULL OR u.nombre ILIKE '%'||$1||'%' OR u.email ILIKE '%'||$1||'%')
       AND ($2::text IS NULL OR u.idioma_meta = $2)
       AND ($3::text IS NULL OR (CASE WHEN u.plataforma = '' THEN 'desconocida' ELSE u.plataforma END) = $3)
       AND ($4::text IS NULL OR ($4 = 'activos') = (u.ultima_actividad > now() - interval '7 days'))
       AND ($5::text IS NULL OR ($5 = 'pago') = (u.plan_id <> ''))
     ORDER BY u.ultima_actividad DESC LIMIT 5000`,
    [vacio(f.q), vacio(f.idioma), vacio(f.plataforma), vacio(f.estado), vacio(f.plan)],
  );
  const clases = filas.length ? resumirClases(await filasClases(filas.map((u) => u.id)), hoyLocal()).porUsuario : new Map();
  for (const u of filas) {
    const c = clases.get(u.id);
    u.clases = c?.clases ?? 0;
    u.ultima_clase = c?.ultima ?? null;
    u.nivel_clases = c?.nivelMax[u.idioma_meta] ?? null;
  }
  const signo = f.dir === 'asc' ? 1 : -1;
  const valor = (u: any) => (f.orden === 'ultima_actividad' || f.orden === 'creado_en' ? new Date(u[f.orden]).getTime() : u[f.orden]);
  filas.sort((a, b) => {
    const x = valor(a), y = valor(b);
    return signo * (typeof x === 'string' ? x.localeCompare(y, 'es') : Number(x) - Number(y));
  });
  return { total: filas.length, filas: filas.slice(0, f.limite) };
}

export const COLUMNAS_CSV = ['nombre', 'email', 'idioma_meta', 'idioma_nativo', 'plataforma', 'plan_id', 'creado_en', 'ultima_actividad',
  'activo', 'clases', 'nivel_clases', 'ultima_clase', 'xp', 'racha', 'segundos', 'conversaciones', 'errores_pendientes', 'trial_segundos'];

export default async function rutas(app: FastifyInstance) {
  app.post('/admin/login', async (req, reply) => {
    const { usuario, pin } = z.object({ usuario: z.string(), pin: z.string() }).parse(req.body);
    if (usuario !== config.adminUsuario || pin !== config.adminPin) return reply.code(401).send({ error: 'Usuario o PIN incorrectos' });
    return { token: app.jwt.sign({ sub: 'admin', rol: 'admin' } satisfies Sesion, { expiresIn: '12h' }) };
  });

  app.get('/admin/resumen', { preHandler: requiereAdmin }, async () => {
    const tz = ZONA_HORARIA;
    await catalogoConEspera(); // títulos y totales de clases (primera carga, como mucho 3 s)
    await refrescarPlanesDerivados(); // `plan_id` derivado de `suscripciones` (cortesías o periodos que caducaron)
    const { pruebaMinutos } = await ajustesPago();
    const [u] = await query(`SELECT count(*)::int AS total,
        count(*) FILTER (WHERE (creado_en AT TIME ZONE $1)::date = (now() AT TIME ZONE $1)::date)::int AS nuevos_hoy,
        count(*) FILTER (WHERE creado_en > now() - interval '7 days')::int AS nuevos7d,
        count(*) FILTER (WHERE creado_en > now() - interval '30 days')::int AS nuevos30d,
        count(*) FILTER (WHERE plan_id <> '')::int AS con_plan,
        count(*) FILTER (WHERE plan_id = '')::int AS en_prueba,
        count(*) FILTER (WHERE plan_id = '' AND trial_segundos >= $2)::int AS prueba_agotada,
        count(*) FILTER (WHERE es_demo)::int AS demo,
        (now() AT TIME ZONE $1)::date::text AS hoy
      FROM usuarios`, [tz, pruebaMinutos * 60]);
    const { hoy, ...usuarios } = u as Record<string, any>;
    const [activos] = await query(`WITH ${DIAS_ACTIVOS}
      SELECT count(DISTINCT usuario_id) FILTER (WHERE dia = h.hoy)::int AS dau,
             count(DISTINCT usuario_id) FILTER (WHERE dia > h.hoy - 7 AND dia <= h.hoy)::int AS wau,
             count(DISTINCT usuario_id) FILTER (WHERE dia > h.hoy - 30 AND dia <= h.hoy)::int AS mau
      FROM dias_activos, h`, [tz]);
    const reparto = await query(`
      SELECT 'plataforma' AS campo, CASE WHEN plataforma = '' THEN 'desconocida' ELSE plataforma END AS valor, count(*)::int AS n FROM usuarios GROUP BY 1, 2
      UNION ALL SELECT 'idioma_meta', idioma_meta, count(*)::int FROM usuarios GROUP BY 1, 2
      UNION ALL SELECT 'idioma_nativo', idioma_nativo, count(*)::int FROM usuarios GROUP BY 1, 2
      UNION ALL SELECT 'plan', CASE WHEN plan_id = '' THEN 'prueba' ELSE plan_id END, count(*)::int FROM usuarios GROUP BY 1, 2`);
    const porCampo = (c: string) => reparto.filter((r) => r.campo === c).map((r) => ({ valor: r.valor, usuarios: r.n })).sort((a, b) => b.usuarios - a.usuarios);

    const serie = await query(`WITH ${DIAS_ACTIVOS}, s AS (SELECT generate_series(h.hoy - 29, h.hoy, interval '1 day')::date AS dia FROM h)
      SELECT s.dia::text AS dia, coalesce(r.n, 0)::int AS registros, coalesce(a.n, 0)::int AS activos, coalesce(c.n, 0)::int AS conversaciones
      FROM s
      LEFT JOIN (SELECT (creado_en AT TIME ZONE $1)::date AS dia, count(*) AS n FROM usuarios WHERE creado_en > now() - interval '32 days' GROUP BY 1) r USING (dia)
      LEFT JOIN (SELECT dia, count(DISTINCT usuario_id) AS n FROM dias_activos GROUP BY 1) a USING (dia)
      LEFT JOIN (SELECT (fecha AT TIME ZONE $1)::date AS dia, count(*) AS n FROM conversaciones WHERE fecha > now() - interval '32 days' GROUP BY 1) c USING (dia)
      ORDER BY 1`, [tz]);

    const retencion = await query(`WITH ${DIAS_ACTIVOS}, reg AS (SELECT id, (creado_en AT TIME ZONE $1)::date AS dia FROM usuarios)
      SELECT v.n AS dias, count(*) FILTER (WHERE reg.dia <= h.hoy - v.n)::int AS base,
             count(*) FILTER (WHERE reg.dia <= h.hoy - v.n AND EXISTS (
               SELECT 1 FROM dias_activos d WHERE d.usuario_id = reg.id AND d.dia >= reg.dia + v.n))::int AS retenidos
      FROM reg, h, (VALUES (1), (7), (30)) v(n) GROUP BY v.n ORDER BY v.n`, [tz]);

    const alumnos = await query(`WITH ${DIAS_ACTIVOS}
      SELECT u.id,
        (EXISTS (SELECT 1 FROM eventos e WHERE e.usuario_id = u.id AND e.tipo = 'diagnostico') OR coalesce(p.estado ? 'diagnostico', false)) AS ubicacion,
        EXISTS (SELECT 1 FROM dias_activos d WHERE d.usuario_id = u.id AND d.dia > (u.creado_en AT TIME ZONE $1)::date) AS volvio
      FROM usuarios u LEFT JOIN progreso p ON p.usuario_id = u.id`, [tz]);
    const clases = resumirClases(await filasClases(), hoy);
    const nClases = (id: string) => clases.porUsuario.get(id)?.clases ?? 0;
    const embudo = [
      { paso: 'Registrados', usuarios: alumnos.length },
      { paso: 'Hicieron la prueba de ubicación', usuarios: alumnos.filter((a) => a.ubicacion).length },
      { paso: 'Completaron 1 clase', usuarios: alumnos.filter((a) => nClases(a.id) >= 1).length },
      { paso: 'Completaron 5 clases', usuarios: alumnos.filter((a) => nClases(a.id) >= 5).length },
      { paso: 'Volvieron otro día', usuarios: alumnos.filter((a) => a.volvio).length },
    ];
    const clasesPorDia = new Map<string, number>();
    for (const a of clases.aprobadas) { const d = diaDe(a.fecha); if (d) clasesPorDia.set(d, (clasesPorDia.get(d) ?? 0) + 1); }
    const porDia = serieDias(hoy, 30).map((dia) => ({
      ...(serie.find((s) => s.dia === dia) ?? { dia, registros: 0, activos: 0, conversaciones: 0 }), clases: clasesPorDia.get(dia) ?? 0,
    }));

    const totales = totalesCatalogo(catalogoClases());
    const tabla = tablaIdiomaNivel(clases.aprobadas).map((f) => ({ ...f, publicadas: NIVELES_TABLA.map((n) => totales[f.idioma]?.[n] ?? 0) }));

    const ubicacion = await query(`SELECT coalesce(datos->>'idioma', '?') AS idioma, count(*)::int AS pruebas, count(DISTINCT usuario_id)::int AS alumnos,
        round(avg(CASE WHEN datos->>'nivelElegido' ~ '^[0-9]{1,2}(\\.[0-9]+)?$' THEN (datos->>'nivelElegido')::numeric END), 1)::float AS nivel_medio
      FROM eventos WHERE tipo = 'diagnostico' GROUP BY 1 ORDER BY 2 DESC`);

    const ia = await query(`SELECT modelo, count(*)::int AS conversaciones, count(DISTINCT usuario_id)::int AS alumnos,
        coalesce(sum(tokens_entrada), 0)::bigint AS entrada, coalesce(sum(tokens_salida), 0)::bigint AS salida,
        count(*) FILTER (WHERE fecha > now() - interval '30 days')::int AS conversaciones30,
        coalesce(sum(tokens_entrada) FILTER (WHERE fecha > now() - interval '30 days'), 0)::bigint AS entrada30,
        coalesce(sum(tokens_salida) FILTER (WHERE fecha > now() - interval '30 days'), 0)::bigint AS salida30
      FROM conversaciones GROUP BY 1 ORDER BY 2 DESC`);
    const modelos = ia.map((m) => ({
      ...m, tarifa: tarifaDe(m.modelo || ''),
      coste: redondear(costeIa(m.modelo || '', m.entrada, m.salida), 4), coste30: redondear(costeIa(m.modelo || '', m.entrada30, m.salida30), 4),
    }));
    const iaPorIdioma = await query(`SELECT idioma, count(*)::int AS conversaciones, count(DISTINCT usuario_id)::int AS alumnos FROM conversaciones GROUP BY 1 ORDER BY 2 DESC`);
    const otrasIa = await query(`SELECT tipo, count(*)::int AS total, count(*) FILTER (WHERE fecha > now() - interval '30 days')::int AS ultimos30
      FROM eventos WHERE tipo IN ('transcripcion', 'revision_escritura', 'diagnostico_pregunta', 'diagnostico_escritura') GROUP BY 1 ORDER BY 2 DESC`);
    const audios = (await query(`SELECT idioma, count(*)::int AS audios, coalesce(sum(caracteres), 0)::int AS caracteres, coalesce(sum(usos), 0)::int AS usos,
        coalesce(sum(caracteres) FILTER (WHERE creado_en > now() - interval '30 days'), 0)::int AS caracteres30
      FROM audios GROUP BY 1 ORDER BY 3 DESC`)).map((a) => ({ ...a, coste: redondear(costeVoz(a.caracteres)), coste30: redondear(costeVoz(a.caracteres30)) }));

    const errores = await query(`SELECT skill, count(*)::int AS total, count(DISTINCT usuario_id)::int AS alumnos, count(*) FILTER (WHERE NOT practicado)::int AS pendientes
      FROM errores GROUP BY 1 ORDER BY 2 DESC`);
    const frecuentes = await query(`SELECT skill, correccion, n FROM (
        SELECT skill, correccion, count(*)::int AS n, row_number() OVER (PARTITION BY skill ORDER BY count(*) DESC, correccion) AS r FROM errores GROUP BY 1, 2) t
      WHERE r <= 3 ORDER BY skill, n DESC`);
    const [estudio] = await query(`SELECT coalesce(sum(xp), 0)::int AS xp, coalesce(sum(segundos_estudio), 0)::int AS segundos FROM progreso`);
    const [examenes] = await query(`SELECT count(*)::int AS total, count(*) FILTER (WHERE aprobado)::int AS aprobados, round(avg(pct))::int AS media FROM examenes`);

    return {
      hoy, zonaHoraria: tz,
      usuarios: { ...usuarios, ...activos },
      plataformas: porCampo('plataforma'), idiomasMeta: porCampo('idioma_meta'), idiomasNativos: porCampo('idioma_nativo'), planes: porCampo('plan'),
      porDia, embudo,
      retencion: retencion.map((r) => ({ ...r, pct: r.base ? Math.round((r.retenidos / r.base) * 100) : null })),
      clases: {
        total: clases.aprobadas.length, legado: clases.aprobadas.filter((a) => infoClase(a.unidad).legado).length,
        alumnos: clases.porUsuario.size, tabla,
        masHechas: conTitulo(clases.masHechas), abandonos: conTitulo(clases.abandonos), suspensos: conTitulo(clases.suspensos),
        diasAbandono: DIAS_ABANDONO, catalogo: catalogoClases() !== null,
      },
      ubicacion,
      ia: {
        modelos, porIdioma: iaPorIdioma, otras: otrasIa,
        conversaciones: suma(ia, 'conversaciones'), entrada: suma(ia, 'entrada'), salida: suma(ia, 'salida'),
        coste: redondear(suma(modelos, 'coste'), 4), coste30: redondear(suma(modelos, 'coste30'), 4),
      },
      voz: {
        porIdioma: audios, audios: suma(audios, 'audios'), caracteres: suma(audios, 'caracteres'), caracteres30: suma(audios, 'caracteres30'),
        coste: redondear(suma(audios, 'coste')), coste30: redondear(suma(audios, 'coste30')), usdPorMilCaracteres: USD_POR_MIL_CARACTERES_VOZ,
      },
      errores: errores.map((e) => ({ ...e, frecuentes: frecuentes.filter((f) => f.skill === e.skill).map((f) => ({ correccion: f.correccion, n: f.n })) })),
      estudio, examenes,
      pruebaMinutos, suscripciones: await metricasSuscripciones(),
    };
  });

  app.get('/admin/usuarios', { preHandler: requiereAdmin }, async (req) => listarUsuarios(FiltrosUsuarios.parse(req.query)));

  app.get('/admin/usuarios.csv', { preHandler: requiereAdmin }, async (req, reply) => {
    const { filas } = await listarUsuarios({ ...FiltrosUsuarios.parse(req.query), limite: 5000 });
    reply.header('content-type', 'text/csv; charset=utf-8')
      .header('content-disposition', `attachment; filename="alumnos-onelingo-${hoyLocal()}.csv"`);
    return '﻿' + aCsv(filas, COLUMNAS_CSV);
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
    // Los secretos de autenticación nunca salen hacia el panel.
    for (const k of ['password_hash', 'token_verificacion', 'token_reset', 'reset_expira']) delete usuario[k];
    await catalogoConEspera();
    const progreso = await uno('SELECT * FROM progreso WHERE usuario_id = $1', [id]);
    const errores = await query('SELECT * FROM errores WHERE usuario_id = $1 ORDER BY fecha DESC LIMIT 100', [id]);
    const examenes = await query('SELECT * FROM examenes WHERE usuario_id = $1 ORDER BY nivel', [id]);
    const eventos = await query('SELECT tipo, datos, fecha FROM eventos WHERE usuario_id = $1 ORDER BY fecha DESC LIMIT 50', [id]);
    const ubicacion = await query(`SELECT datos, fecha FROM eventos WHERE usuario_id = $1 AND tipo = 'diagnostico' ORDER BY fecha DESC LIMIT 10`, [id]);
    const conversaciones = await query(`SELECT id, fecha, idioma, nivel, situacion_id, mensaje_alumno, respuesta->>'reply' AS respuesta, modelo, tokens_entrada, tokens_salida
      FROM conversaciones WHERE usuario_id = $1 ORDER BY fecha DESC LIMIT 20`, [id]);
    const iaModelos = await query(`SELECT modelo, count(*)::int AS conversaciones, coalesce(sum(tokens_entrada), 0)::bigint AS entrada, coalesce(sum(tokens_salida), 0)::bigint AS salida
      FROM conversaciones WHERE usuario_id = $1 GROUP BY 1`, [id]);

    const filas = await filasClases([id]);
    const r = resumirClases(filas, hoyLocal());
    const totales = totalesCatalogo(catalogoClases());
    const progresoIdiomas = tablaIdiomaNivel(r.aprobadas).map((f) => ({
      idioma: f.idioma, total: f.total,
      niveles: NIVELES_TABLA.map((n, i) => ({ nivel: n, clases: f.niveles[i], publicadas: totales[f.idioma]?.[n] ?? null }))
        .filter((x) => x.clases > 0 || (x.publicadas ?? 0) > 0),
    }));
    const meta = progresoIdiomas.find((p) => p.idioma === usuario.idioma_meta);
    // Clases por nivel (1–10) del idioma que estudia ahora (antes contaba solo el prefijo `L<n>-`).
    const porNivel = Array.from({ length: 10 }, (_, i) => ({ nivel: i + 1, lecciones: meta?.niveles.find((x) => x.nivel === i + 1)?.clases ?? 0 }));
    const intentos = (u: string) => filas.find((f) => f.unidad === u && f.clave === 'evaluacion')?.intentos ?? 1;
    const ultimasClases = conTitulo(r.aprobadas.filter((a) => a.fecha).sort((a, b) => (b.fecha! > a.fecha! ? 1 : -1)).slice(0, 15)
      .map((a) => ({ unidad: a.unidad, fecha: a.fecha, intentos: intentos(a.unidad) })));
    const aprobadas = new Set(r.aprobadas.map((a) => a.unidad));
    const empezadas = conTitulo(filas.filter((f) => f.clave === 'visto' && !aprobadas.has(f.unidad)).map((f) => ({ unidad: f.unidad, fecha: f.fecha })));
    const ia = {
      conversaciones: suma(iaModelos, 'conversaciones'), entrada: suma(iaModelos, 'entrada'), salida: suma(iaModelos, 'salida'),
      coste: redondear(iaModelos.reduce((a, m) => a + costeIa(m.modelo || '', m.entrada, m.salida), 0), 4),
    };
    const fs = await filaDe(id);
    const suscripcion = { ...(await suscripcionDe(id)), nota: fs?.nota ?? '', stripeClienteId: fs?.stripe_cliente_id ?? null, stripeSuscripcionId: fs?.stripe_suscripcion_id ?? null, filaPlanId: fs?.plan_id ?? null };
    return {
      suscripcion,
      usuario, progreso, porNivel, progresoIdiomas, ultimasClases, empezadas, clases: r.aprobadas.length,
      legado: r.aprobadas.filter((a) => infoClase(a.unidad).legado).length,
      ubicacion, conversaciones, ia, errores, examenes, eventos,
    };
  });
}
