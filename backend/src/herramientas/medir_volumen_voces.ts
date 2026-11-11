/**
 * Solo lectura: sonoridad real (LUFS) de los audios guardados en la caché en
 * los últimos días, por voz y modelo. Sirve para ver si la ganancia fija de la
 * videollamada (LUFS_VOZ en lib/volumen.ts) deja todas las voces al mismo nivel.
 *   npx tsx src/herramientas/medir_volumen_voces.ts [--dias 7] [--por-voz 6]
 */
import path from 'node:path';
import { readFile } from 'node:fs/promises';
import { config } from '../lib/config.js';
import { query, pool } from '../lib/db.js';
import { medirLufs, OBJETIVO_LUFS } from '../lib/volumen.js';

const arg = (n: string, d: string) => { const i = process.argv.indexOf(`--${n}`); return i > 0 ? process.argv[i + 1] : d; };
const dias = Number(arg('dias', '7')), porVoz = Number(arg('por-voz', '6'));

const filas = await query<{ hash: string; voz: string; modelo: string; idioma: string; texto: string }>(
  `SELECT hash, voz, modelo, idioma, texto FROM (
     SELECT hash, voz, modelo, idioma, texto, row_number() OVER (PARTITION BY voz, modelo ORDER BY creado_en DESC) AS n
     FROM audios WHERE creado_en > now() - make_interval(days => $1::int) AND bytes > 0 AND caracteres >= 25) x
   WHERE n <= $2 ORDER BY voz, modelo`, [dias, porVoz]);

const grupos = new Map<string, number[]>();
for (const f of filas) {
  try {
    const lufs = await medirLufs(await readFile(path.join(config.audioDir, `${f.hash}.mp3`)));
    if (lufs === null) continue;
    const k = `${f.voz} · ${f.modelo}`;
    grupos.set(k, [...(grupos.get(k) ?? []), lufs]);
  } catch { /* archivo ausente */ }
}
const r = (x: number) => Math.round(x * 10) / 10;
const tabla = [...grupos].map(([k, v]) => ({ voz: k, clips: v.length, media: r(v.reduce((a, b) => a + b, 0) / v.length), min: r(Math.min(...v)), max: r(Math.max(...v)), desvio: r(v.reduce((a, b) => a + b, 0) / v.length - OBJETIVO_LUFS) }));
console.log(`objetivo ${OBJETIVO_LUFS} LUFS · ${filas.length} audios de los últimos ${dias} días`);
console.table(tabla.sort((a, b) => Math.abs(b.desvio) - Math.abs(a.desvio)));
await pool.end();
