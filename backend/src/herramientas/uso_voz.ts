/**
 * Consumo de voz (solo lectura): en qué se fueron los caracteres de ElevenLabs.
 *   npx tsx src/herramientas/uso_voz.ts [desde=AAAA-MM-DD]
 */
import pg from 'pg';
import { config } from '../lib/config.js';

const desde = process.argv[2] ?? new Date(Date.now() - 30 * 864e5).toISOString().slice(0, 10);
const c = new pg.Client({ connectionString: config.databaseUrl });
await c.connect();
await c.query('SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY');
const q = async (t: string, p: unknown[] = []) => (await c.query(t, p)).rows;
try {
  console.log('== audios sintetizados por día (UTC)');
  console.table(await q(`SELECT to_char(creado_en AT TIME ZONE 'UTC', 'MM-DD') dia, count(*)::int audios, sum(caracteres)::int caracteres
    FROM audios WHERE creado_en >= $1 AND caracteres > 0 GROUP BY 1 ORDER BY 1`, [desde]));
  console.log('== por voz e idioma');
  console.table(await q(`SELECT voz, idioma, count(*)::int audios, sum(caracteres)::int caracteres
    FROM audios WHERE creado_en >= $1 AND caracteres > 0 GROUP BY 1, 2 ORDER BY 4 DESC LIMIT 15`, [desde]));
  console.log('== videollamadas por alumno (código anónimo)');
  console.table(await q(`SELECT left(md5(usuario_id::text), 6) alumno, idioma, count(*)::int turnos, sum(length(respuesta->>'reply'))::int caracteres_reply
    FROM conversaciones WHERE fecha >= $1 AND tutor_id LIKE 'avatar%' GROUP BY 1, 2 ORDER BY 4 DESC LIMIT 10`, [desde]));
  console.log('== textos más largos');
  console.table(await q(`SELECT voz, idioma, caracteres, left(texto, 70) texto FROM audios WHERE creado_en >= $1 AND caracteres > 0 ORDER BY caracteres DESC LIMIT 8`, [desde]));
} finally {
  await c.end();
}
