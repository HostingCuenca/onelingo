import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { pool } from './lib/db.js';
const dir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'sql');
export async function migrar() {
  await pool.query('CREATE TABLE IF NOT EXISTS schema_migrations (nombre text PRIMARY KEY, aplicada_en timestamptz NOT NULL DEFAULT now())');
  const aplicadas = new Set((await pool.query('SELECT nombre FROM schema_migrations')).rows.map((r) => r.nombre));
  for (const f of (await readdir(dir)).filter((f) => f.endsWith('.sql')).sort()) {
    if (aplicadas.has(f)) continue;
    const c = await pool.connect();
    try {
      await c.query('BEGIN');
      await c.query(await readFile(path.join(dir, f), 'utf8'));
      await c.query('INSERT INTO schema_migrations (nombre) VALUES ($1)', [f]);
      await c.query('COMMIT');
      console.log('Migración aplicada:', f);
    } catch (e) { await c.query('ROLLBACK'); throw e; } finally { c.release(); }
  }
}
if (process.argv[1] && process.argv[1].endsWith('migrate.ts')) { await migrar(); await pool.end(); }
