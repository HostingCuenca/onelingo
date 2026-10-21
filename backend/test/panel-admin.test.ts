import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { pool } from '../src/lib/db.js';
import {
  aCsv, costeIa, costeVoz, esperarCatalogo, infoClase, resumirClases, serieDias, tablaIdiomaNivel, tarifaDe, totalesCatalogo,
  TARIFA_IA_DESCONOCIDA, type FilaClase,
} from '../src/lib/analitica.js';

// El catálogo es único por proceso: se carga primero desde un contenido de prueba
// para que las rutas no lean el contenido real del repositorio.
test('catálogo de clases: títulos y totales desde <idioma>/ruta/*.json, sin curso.json', async () => {
  const raiz = await mkdtemp(path.join(os.tmpdir(), 'panel-catalogo-'));
  await mkdir(path.join(raiz, 'ja', 'ruta'), { recursive: true });
  await writeFile(path.join(raiz, 'ja', 'ruta', 'curso.json'), JSON.stringify({ unidades: [{ id: 'no.cuenta', titulo: 'x' }] }));
  await writeFile(path.join(raiz, 'ja', 'ruta', 'n1-b01.json'), JSON.stringify({ unidades: [
    { id: 'ja.n1.c01', titulo: { es: 'Saludar', en: 'Greet' }, nivelInterno: 1 },
    { id: 'ja.n1.c02', titulo: { es: 'Presentarse' }, nivelInterno: 1 },
  ] }));
  await writeFile(path.join(raiz, 'ja', 'ruta', 'roto.json'), '{no es json');
  const c = await esperarCatalogo([path.join(raiz, 'no-existe'), raiz]);
  assert.equal(c.size, 2);
  assert.equal(c.get('ja.n1.c01')?.titulo, 'Saludar');
  assert.deepEqual(totalesCatalogo(c), { ja: { 1: 2 } });
});

test('infoClase: ids de la ruta actual y del legado', () => {
  assert.deepEqual(infoClase('ja.n3.c06'), { idioma: 'ja', nivel: 3, legado: false });
  assert.deepEqual(infoClase('en.n10.class-50'), { idioma: 'en', nivel: 10, legado: false });
  assert.deepEqual(infoClase('en.n1.class-01'), { idioma: 'en', nivel: 1, legado: false });
  assert.deepEqual(infoClase('en.f0.primer-contacto'), { idioma: 'en', nivel: 0, legado: false });
  assert.deepEqual(infoClase('en.a1.posesivos'), { idioma: 'en', nivel: 1, legado: false });
  assert.deepEqual(infoClase('L3-012'), { idioma: null, nivel: 3, legado: true });
  assert.deepEqual(infoClase('L0-001'), { idioma: null, nivel: 0, legado: true });
  assert.deepEqual(infoClase('cualquier-cosa'), { idioma: null, nivel: null, legado: false });
  assert.deepEqual(infoClase('fr.c2.algo'), { idioma: 'fr', nivel: null, legado: false });
});

test('tarifas: por prefijo más largo y estimación por defecto', () => {
  assert.deepEqual(tarifaDe('gpt-4.1-mini-2025-04-14'), { entrada: 0.4, salida: 1.6 });
  assert.deepEqual(tarifaDe('gpt-4.1-2025-04-14'), { entrada: 2, salida: 8 });
  assert.deepEqual(tarifaDe('modelo-raro'), TARIFA_IA_DESCONOCIDA);
  assert.ok(Math.abs(costeIa('gpt-4.1-mini', 1_000_000, 500_000) - 1.2) < 1e-9);
  assert.ok(Math.abs(costeVoz(2000) - 0.22) < 1e-9);
});

const fila = (u: string, unidad: string, clave: FilaClase['clave'], aprobada: boolean, fecha: string | null, idioma = 'en'): FilaClase =>
  ({ usuario_id: u, idioma_usuario: idioma, unidad, clave, aprobada, fecha, intentos: 1 });

test('resumirClases: aprobadas sin duplicar, abandonos, suspensos y legado', () => {
  const r = resumirClases([
    fila('a', 'ja.n1.c01', 'visto', true, '2026-10-01T10:00:00', 'ja'),
    fila('a', 'ja.n1.c01', 'evaluacion', true, '2026-10-02T10:00:00', 'ja'),
    fila('a', 'ja.n2.c01', 'evaluacion', true, '2026-10-03T10:00:00', 'ja'),
    fila('a', 'ja.n2.c02', 'visto', true, '2026-10-01T10:00:00', 'ja'), // abandonada
    fila('b', 'ja.n1.c01', 'evaluacion', true, '2026-10-04T10:00:00'),
    fila('b', 'ja.n2.c02', 'visto', true, '2026-10-18T10:00:00'), // reciente: aún en curso
    fila('b', 'ja.n2.c02', 'evaluacion', false, '2026-10-18T10:00:00'), // suspensa
    fila('b', 'L1-001', 'legado', true, null),
    fila('b', 'L1-002', 'legado', true, null),
  ], '2026-10-19');
  assert.equal(r.aprobadas.length, 5);
  assert.equal(r.porUsuario.get('a')?.clases, 2);
  assert.deepEqual(r.porUsuario.get('a')?.nivelMax, { ja: 2 });
  assert.equal(r.porUsuario.get('b')?.clases, 3);
  assert.deepEqual(r.porUsuario.get('b')?.nivelMax, { ja: 1, en: 1 });
  assert.equal(r.porUsuario.get('b')?.ultima, '2026-10-04T10:00:00');
  assert.deepEqual(r.masHechas[0], { unidad: 'ja.n1.c01', alumnos: 2 });
  assert.ok(!r.masHechas.some((m) => m.unidad.startsWith('L')), 'el legado no entra en el ranking');
  assert.deepEqual(r.abandonos, [{ unidad: 'ja.n2.c02', alumnos: 1 }]);
  assert.deepEqual(r.suspensos, [{ unidad: 'ja.n2.c02', alumnos: 1 }]);
  const t = tablaIdiomaNivel(r.aprobadas);
  assert.deepEqual(t.find((x) => x.idioma === 'ja')?.niveles.slice(0, 3), [0, 2, 1]);
  assert.deepEqual(t.find((x) => x.idioma === 'en')?.niveles.slice(0, 2), [0, 2]);
});

test('serieDias y CSV', () => {
  assert.deepEqual(serieDias('2026-03-01', 3), ['2026-02-27', '2026-02-28', '2026-03-01']);
  assert.equal(serieDias('2026-10-19', 30).length, 30);
  assert.equal(aCsv([{ a: 'x;y', b: 'di "hola"', c: null }, { a: 1, b: true, c: 'ok' }], ['a', 'b', 'c']),
    'a;b;c\n"x;y";"di ""hola""";\n1;true;ok');
});

// ── Rutas (base simulada) ────────────────────────────────────────────────────

const U1 = '11111111-1111-4111-8111-111111111111', U2 = '22222222-2222-4222-8222-222222222222';
type Llamada = { sql: string; params: unknown[] };

function baseSimulada(llamadas: Llamada[]) {
  return async (sql: string, params: unknown[] = []) => {
    llamadas.push({ sql, params });
    const s = sql.replace(/\s+/g, ' ');
    const rows = (() => {
      if (s.includes('FROM usuarios u LEFT JOIN progreso p') && s.includes('AS activo')) return [
        { id: U1, nombre: 'Ana', email: 'ana@ejemplo.test', idioma_meta: 'ja', plataforma: 'android', creado_en: '2026-10-01T00:00:00Z', ultima_actividad: '2026-10-19T00:00:00Z', xp: 10, segundos: 60, conversaciones: 0, activo: true },
        { id: U2, nombre: 'Beto', email: 'beto@ejemplo.test', idioma_meta: 'en', plataforma: 'web', creado_en: '2026-10-02T00:00:00Z', ultima_actividad: '2026-10-18T00:00:00Z', xp: 5, segundos: 30, conversaciones: 2, activo: true },
      ];
      if (s.includes('WITH pr AS')) return [
        { usuario_id: U2, idioma_usuario: 'en', unidad: 'en.n1.class-01', clave: 'evaluacion', aprobada: true, fecha: '2026-10-10T10:00:00', intentos: 1 },
        { usuario_id: U2, idioma_usuario: 'en', unidad: 'en.n2.class-01', clave: 'evaluacion', aprobada: true, fecha: '2026-10-11T10:00:00', intentos: 2 },
        { usuario_id: U2, idioma_usuario: 'en', unidad: 'en.n2.class-02', clave: 'visto', aprobada: false, fecha: '2026-10-11T10:00:00', intentos: 1 },
      ];
      if (s.startsWith('SELECT * FROM usuarios WHERE id')) return params[0] === U2 ? [{ id: U2, nombre: 'Beto', idioma_meta: 'en', password_hash: 'secreto', token_reset: 'x', token_verificacion: 'y' }] : [];
      if (s.includes('count(*)::int AS total,') && s.includes('nuevos_hoy')) return [{ total: 2, nuevos_hoy: 0, nuevos7d: 1, nuevos30d: 2, con_plan: 0, en_prueba: 2, prueba_agotada: 0, demo: 0, hoy: '2026-10-19' }];
      if (s.includes('AS dau')) return [{ dau: 1, wau: 2, mau: 2 }];
      if (s.includes("'plataforma' AS campo")) return [{ campo: 'plataforma', valor: 'web', n: 1 }, { campo: 'plataforma', valor: 'android', n: 1 }, { campo: 'idioma_meta', valor: 'en', n: 1 }];
      if (s.includes('AS retenidos')) return [{ dias: 1, base: 2, retenidos: 1 }, { dias: 7, base: 1, retenidos: 0 }, { dias: 30, base: 0, retenidos: 0 }];
      if (s.includes('AS ubicacion,') && s.includes('AS volvio')) return [{ id: U1, ubicacion: true, volvio: true }, { id: U2, ubicacion: true, volvio: false }];
      if (s.includes('FROM conversaciones GROUP BY 1 ORDER BY 2 DESC') && s.includes('modelo')) return [{ modelo: 'gpt-4.1-mini-2025-04-14', conversaciones: 2, alumnos: 1, entrada: 1_000_000, salida: 0, conversaciones30: 2, entrada30: 1_000_000, salida30: 0 }];
      if (s.includes('FROM audios GROUP BY 1')) return [{ idioma: 'en', audios: 3, caracteres: 1000, usos: 5, caracteres30: 1000 }];
      if (s.includes('FROM errores GROUP BY 1 ORDER BY 2 DESC')) return [{ skill: 'gramatica', total: 3, alumnos: 2, pendientes: 1 }];
      if (s.includes('row_number()')) return [{ skill: 'gramatica', correccion: 'I have', n: 2 }];
      if (s.includes('FROM progreso`') || s.includes('sum(segundos_estudio)')) return [{ xp: 15, segundos: 90 }];
      if (s.includes('FROM examenes`') || s.includes('avg(pct)')) return [{ total: 0, aprobados: 0, media: null }];
      if (s.includes('FROM conversaciones WHERE usuario_id = $1 GROUP BY 1')) return [{ modelo: 'gpt-4.1-mini', conversaciones: 1, entrada: 100, salida: 50 }];
      return [];
    })();
    return { rows };
  };
}

async function montar(llamadas: Llamada[]) {
  const { default: Fastify } = await import('fastify');
  const { default: jwt } = await import('@fastify/jwt');
  const { default: rutas } = await import('../src/routes/admin.js');
  (pool as any).query = baseSimulada(llamadas);
  const app = Fastify(); await app.register(jwt, { secret: 'test-only-panel-secret' }); await app.register(rutas);
  return { app, admin: app.jwt.sign({ sub: 'admin', rol: 'admin' }), alumno: app.jwt.sign({ sub: U1, rol: 'alumno' }) };
}
const original = pool.query;

test('rutas del panel: piden sesión de administrador', async () => {
  const { app, alumno } = await montar([]);
  try {
    for (const url of ['/admin/resumen', '/admin/usuarios', '/admin/usuarios.csv', `/admin/usuarios/${U2}`]) {
      assert.equal((await app.inject({ url })).statusCode, 401, url);
      assert.equal((await app.inject({ url, headers: { authorization: `Bearer ${alumno}` } })).statusCode, 403, url);
    }
  } finally { await app.close(); (pool as any).query = original; }
});

test('/admin/usuarios: filtros como parámetros, clases calculadas y orden por clases', async () => {
  const llamadas: Llamada[] = [];
  const { app, admin } = await montar(llamadas);
  try {
    const r = await app.inject({ url: '/admin/usuarios?q=%20be%20&idioma=en&plataforma=web&estado=activos&plan=prueba&orden=clases&dir=desc', headers: { authorization: `Bearer ${admin}` } });
    assert.equal(r.statusCode, 200);
    const lista = llamadas.find((l) => l.sql.includes('AS activo'))!;
    assert.deepEqual(lista.params, ['be', 'en', 'web', 'activos', 'prueba']);
    const d = r.json();
    assert.equal(d.total, 2);
    assert.deepEqual(d.filas.map((u: any) => [u.nombre, u.clases, u.nivel_clases]), [['Beto', 2, 2], ['Ana', 0, null]]);
    const asc = (await app.inject({ url: '/admin/usuarios?orden=nombre&dir=asc&limite=1', headers: { authorization: `Bearer ${admin}` } })).json();
    assert.deepEqual(asc.filas.map((u: any) => u.nombre), ['Ana']);
    // Un orden no permitido se rechaza (la app lo convierte en 400 con su manejador de ZodError).
    assert.ok((await app.inject({ url: '/admin/usuarios?orden=email;drop', headers: { authorization: `Bearer ${admin}` } })).statusCode >= 400);
  } finally { await app.close(); (pool as any).query = original; }
});

test('/admin/usuarios.csv: descarga con cabecera y una fila por alumno', async () => {
  const { app, admin } = await montar([]);
  try {
    const r = await app.inject({ url: '/admin/usuarios.csv', headers: { authorization: `Bearer ${admin}` } });
    assert.equal(r.statusCode, 200);
    assert.match(String(r.headers['content-type']), /text\/csv/);
    assert.match(String(r.headers['content-disposition']), /attachment; filename="alumnos-onelingo-\d{4}-\d{2}-\d{2}\.csv"/);
    const lineas = r.body.replace(/^﻿/, '').split('\n');
    assert.equal(lineas.length, 3);
    assert.ok(lineas[0].startsWith('nombre;email;idioma_meta'));
    assert.ok(lineas.some((l) => l.startsWith('Beto;beto@ejemplo.test;en')));
  } finally { await app.close(); (pool as any).query = original; }
});

test('/admin/usuarios/:id: progreso por nivel con ids nuevos y sin secretos', async () => {
  const { app, admin } = await montar([]);
  try {
    const r = await app.inject({ url: `/admin/usuarios/${U2}`, headers: { authorization: `Bearer ${admin}` } });
    assert.equal(r.statusCode, 200);
    const d = r.json();
    assert.equal(d.usuario.password_hash, undefined);
    assert.equal(d.usuario.token_reset, undefined);
    assert.equal(d.usuario.token_verificacion, undefined);
    assert.equal(d.clases, 2);
    assert.deepEqual(d.porNivel.slice(0, 3), [{ nivel: 1, lecciones: 1 }, { nivel: 2, lecciones: 1 }, { nivel: 3, lecciones: 0 }]);
    assert.equal(d.ultimasClases[0].unidad, 'en.n2.class-01');
    assert.equal(d.ultimasClases[0].intentos, 2);
    assert.deepEqual(d.empezadas.map((c: any) => c.unidad), ['en.n2.class-02']);
    assert.equal(d.ia.conversaciones, 1);
    assert.equal((await app.inject({ url: `/admin/usuarios/${U1}`, headers: { authorization: `Bearer ${admin}` } })).statusCode, 404);
  } finally { await app.close(); (pool as any).query = original; }
});

test('/admin/resumen: usuarios, embudo, retención, clases, IA y voz', async () => {
  const { app, admin } = await montar([]);
  try {
    const r = await app.inject({ url: '/admin/resumen', headers: { authorization: `Bearer ${admin}` } });
    assert.equal(r.statusCode, 200);
    const d = r.json();
    assert.equal(d.hoy, '2026-10-19');
    assert.equal(d.usuarios.total, 2);
    assert.equal(d.usuarios.dau, 1);
    assert.equal(d.usuarios.hoy, undefined);
    assert.equal(d.porDia.length, 30);
    assert.equal(d.porDia.at(-1).dia, '2026-10-19');
    assert.equal(d.porDia.find((x: any) => x.dia === '2026-10-10').clases, 1);
    assert.deepEqual(d.embudo.map((e: any) => e.usuarios), [2, 2, 1, 0, 1]);
    assert.deepEqual(d.retencion.map((x: any) => x.pct), [50, 0, null]);
    assert.equal(d.clases.total, 2);
    assert.deepEqual(d.clases.tabla[0].niveles.slice(0, 3), [0, 1, 1]);
    assert.deepEqual(d.clases.abandonos.map((c: any) => c.unidad), ['en.n2.class-02']);
    assert.deepEqual(d.plataformas, [{ valor: 'web', usuarios: 1 }, { valor: 'android', usuarios: 1 }]);
    assert.equal(d.ia.coste, 0.4);
    assert.equal(d.voz.coste, 0.11);
    assert.deepEqual(d.errores[0].frecuentes, [{ correccion: 'I have', n: 2 }]);
  } finally { await app.close(); (pool as any).query = original; }
});

test('/admin/login: usuario sin distinguir mayúsculas ni espacios, PIN exacto y sesión de 30 días', async () => {
  const { config } = await import('../src/lib/config.js');
  const { app } = await montar([]);
  try {
    const entrar = (usuario: string, pin: string) => app.inject({ method: 'POST', url: '/admin/login', payload: { usuario, pin } });
    const ok = await entrar(` ${config.adminUsuario.toUpperCase()} `, ` ${config.adminPin} `);
    assert.equal(ok.statusCode, 200);
    const { exp, iat } = app.jwt.decode(ok.json().token) as { exp: number; iat: number };
    assert.equal(exp - iat, 30 * 24 * 3600);
    assert.equal((await entrar(config.adminUsuario, config.adminPin + 'x')).statusCode, 401);
    assert.equal((await entrar('otro', config.adminPin)).statusCode, 401);
  } finally { await app.close(); (pool as any).query = original; }
});
