import pg from 'pg';
import { config } from './config.js';
pg.types.setTypeParser(20, (v) => Number(v)); // bigint → number
export const pool = new pg.Pool({ connectionString: config.databaseUrl, max: 10 });
export async function query<T extends pg.QueryResultRow = any>(texto: string, params: unknown[] = []): Promise<T[]> {
  return (await pool.query<T>(texto, params)).rows;
}
export async function uno<T extends pg.QueryResultRow = any>(texto: string, params: unknown[] = []): Promise<T | undefined> {
  return (await pool.query<T>(texto, params)).rows[0];
}
