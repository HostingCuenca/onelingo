/**
 * Revisión de calidad del tutor: últimas conversaciones, SOLO LECTURA y
 * anonimizadas (el alumno aparece como un código corto, sin correo ni nombre).
 * Sesión de base de datos en modo solo lectura: no puede escribir nada.
 *
 *   npx tsx src/herramientas/conversaciones.ts [--dias 3] [--llamadas 15] [--idioma en] [--chat]
 *
 * Por defecto solo videollamadas (tutor avatar_*); --chat incluye el chat escrito.
 */
import { createHash } from 'node:crypto';
import pg from 'pg';
import { config } from '../lib/config.js';

const arg = (n: string, d: string) => { const i = process.argv.indexOf(`--${n}`); return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };
const dias = Math.min(Math.max(Number(arg('dias', '3')) || 3, 1), 30);
const maxLlamadas = Math.min(Math.max(Number(arg('llamadas', '15')) || 15, 1), 60);
const idioma = /^[a-z]{2}$/.test(arg('idioma', '')) ? arg('idioma', '') : '';
const chat = process.argv.includes('--chat');

const alias = (id: string) => createHash('sha256').update(id).digest('hex').slice(0, 6);
const corto = (t: unknown, n = 400) => { const s = String(t ?? '').replace(/\s+/g, ' ').trim(); return s.length > n ? s.slice(0, n) + '…' : s; };
const lista = (v: unknown) => Array.isArray(v) ? v.map(x => corto(x, 120)).join(' · ') : '';

const cliente = new pg.Client({ connectionString: config.databaseUrl });
await cliente.connect();
try {
  await cliente.query('SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY');
  const { rows } = await cliente.query(
    `SELECT usuario_id::text AS u, idioma, nivel, tutor_id, situacion_id, mensaje_alumno, respuesta->>'reply' AS reply, fecha
       FROM conversaciones
      WHERE fecha > now() - make_interval(days => $1::int) AND ($2 = '' OR idioma = $2) AND ($3 OR tutor_id LIKE 'avatar\\_%')
      ORDER BY usuario_id, fecha`, [dias, idioma, chat]);

  // Una llamada = turnos seguidos del mismo alumno, idioma y tutor sin pausas de más de 20 min.
  type Llamada = { u: string; idioma: string; nivel: number; tutor: string; situacion: number | null; inicio: Date; fin: Date; turnos: { a: string; t: string }[] };
  const llamadas: Llamada[] = [];
  for (const r of rows) {
    const ult = llamadas.at(-1), fecha = new Date(r.fecha);
    if (!ult || ult.u !== r.u || ult.idioma !== r.idioma || ult.tutor !== r.tutor_id || fecha.getTime() - ult.fin.getTime() > 20 * 60_000)
      llamadas.push({ u: r.u, idioma: r.idioma, nivel: r.nivel, tutor: r.tutor_id, situacion: r.situacion_id, inicio: fecha, fin: fecha, turnos: [] });
    const l = llamadas.at(-1)!;
    l.fin = fecha; l.turnos.push({ a: corto(r.mensaje_alumno), t: corto(r.reply) });
  }
  const elegidas = llamadas.sort((a, b) => b.fin.getTime() - a.fin.getTime()).slice(0, maxLlamadas);

  const fichas = new Map<string, any>();
  for (const l of elegidas) {
    const k = `${l.u}|${l.idioma}`;
    if (fichas.has(k)) continue;
    const f = await cliente.query('SELECT datos FROM ficha_alumno WHERE usuario_id = $1 AND idioma = $2', [l.u, l.idioma]).catch(() => ({ rows: [] as any[] }));
    fichas.set(k, f.rows[0]?.datos ?? null);
  }

  console.log(`${elegidas.length} de ${llamadas.length} llamadas · últimos ${dias} días${idioma ? ` · ${idioma}` : ''}${chat ? ' · con chat escrito' : ' · solo videollamada'}\n`);
  for (const l of elegidas.reverse()) {
    const f = fichas.get(`${l.u}|${l.idioma}`);
    console.log(`=== Alumno ${alias(l.u)} · ${l.idioma} N${l.nivel} · ${l.tutor}${l.situacion ? ` · situación ${l.situacion}` : ''} · ${l.inicio.toISOString().slice(0, 16).replace('T', ' ')} UTC · ${l.turnos.length} turnos`);
    if (f) console.log(`    ficha · intereses: ${lista(f.intereses) || '—'} | pendiente: ${lista(f.pendiente) || '—'} | foco: ${corto(f.plan?.foco, 120) || '—'}`);
    for (const t of l.turnos) {
      if (t.a) console.log(`  A: ${t.a}`);
      if (t.t) console.log(`  T: ${t.t}`);
    }
    console.log('');
  }
} finally {
  await cliente.end();
}
