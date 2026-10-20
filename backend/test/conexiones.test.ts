import { test } from 'node:test';
import assert from 'node:assert/strict';
import { config } from '../src/lib/config.js';
import { pool } from '../src/lib/db.js';

// Claves inventadas (nunca reales). Se fijan ANTES de importar conexiones.ts,
// que guarda al cargarse los valores del «servidor» para poder restaurarlos.
const rnd = (n: number, abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') => Array.from({ length: n }, (_, i) => abc[(i * 7 + 3) % abc.length]).join('');
const FALSA = {
  eleven: 'sk_' + rnd(48, '0123456789abcdef'),
  elevenHex: rnd(32, '0123456789abcdef'),
  openai: 'sk-proj-' + rnd(40),
  openaiLegado: 'sk-' + rnd(48),
  svc: 'sk-svcacct-' + rnd(40),
  admin: 'sk-admin-' + rnd(40),
  gemini: 'AIza' + rnd(35),
  geminiAuth: 'AQ.' + rnd(60),
  anthropic: 'sk-ant-api03-' + rnd(40),
};
const SERVIDOR = { eleven: 'sk_' + rnd(40, 'fedcba9876543210'), openai: 'sk-proj-' + rnd(44, 'ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210'), gemini: '' };
config.elevenApiKey = SERVIDOR.eleven; config.elevenModelo = 'eleven_flash_v2_5';
config.openaiApiKey = SERVIDOR.openai; config.openaiModelo = 'gpt-4.1-mini'; config.openaiModeloEvaluacion = 'gpt-4.1'; config.openaiModeloTranscripcion = 'gpt-4o-mini-transcribe';
config.geminiApiKey = SERVIDOR.gemini; config.geminiModelo = 'gemini-flash-latest';
config.jwtSecret = 'test-only-conexiones-secret';
delete process.env.OPENAI_ADMIN_KEY;
const C = await import('../src/lib/conexiones.js');

const todasLasFalsas = [...Object.values(FALSA), SERVIDOR.eleven, SERVIDOR.openai];
/** Comprueba que un texto no contiene ninguna clave completa, sin imprimirla si falla. */
function sinClaves(texto: string, donde: string) {
  for (const k of todasLasFalsas) if (k) assert.ok(!texto.includes(k), `${donde}: contiene una clave completa`);
}

// ── fetch simulado ───────────────────────────────────────────────────────────
const fetchOriginal = globalThis.fetch;
type Resp = { status: number; body: unknown } | 'colgar';
async function conFetch(rutas: (url: string, headers: Record<string, string>) => Resp, fn: (llamadas: string[]) => Promise<void>) {
  const llamadas: string[] = [];
  globalThis.fetch = (async (url: any, init: any) => {
    llamadas.push(String(url));
    const r = rutas(String(url), Object.fromEntries(Object.entries(init?.headers ?? {})) as Record<string, string>);
    if (r === 'colgar') return new Promise((_, rej) => init?.signal?.addEventListener('abort', () => rej(init.signal.reason ?? Object.assign(new Error('timeout'), { name: 'TimeoutError' }))));
    return new Response(JSON.stringify(r.body), { status: r.status, headers: { 'content-type': 'application/json' } });
  }) as typeof fetch;
  try { await fn(llamadas); } finally { globalThis.fetch = fetchOriginal; }
}
const SUB_OK = { tier: 'creator', status: 'active', character_count: 1200, character_limit: 100000, next_character_count_reset_unix: 1793491200 };
const MODELOS_11 = [{ model_id: 'eleven_flash_v2_5' }, { model_id: 'eleven_multilingual_v2' }];
const MODELOS_OAI = { data: [{ id: 'gpt-4.1-mini' }, { id: 'gpt-4.1' }, { id: 'gpt-4o-mini-transcribe' }] };

// ── base simulada ────────────────────────────────────────────────────────────
const queryOriginal = pool.query;
const tabla = new Map<string, { datos: string; verificacion: string | null }>();
function baseSimulada() {
  (pool as any).query = async (sql: string, params: any[] = []) => {
    const s = sql.replace(/\s+/g, ' ');
    if (s.startsWith('SELECT proveedor, datos')) return { rows: [...tabla].map(([proveedor, f]) => ({ proveedor, datos: f.datos, actualizado_en: '2026-10-20T00:00:00Z', verificacion: f.verificacion ? JSON.parse(f.verificacion) : null })) };
    if (s.startsWith('INSERT INTO conexiones')) { tabla.set(params[0], { datos: params[1], verificacion: params[2] }); return { rows: [{ actualizado_en: '2026-10-20T12:00:00Z' }] }; }
    if (s.startsWith('DELETE FROM conexiones')) { tabla.delete(params[0]); return { rows: [] }; }
    if (s.startsWith('UPDATE conexiones')) return { rows: [] };
    if (s.includes('FROM audios')) return { rows: [{ audios: 10, caracteres: 5000, audios_mes: 2, caracteres_mes: 1000 }] };
    if (s.includes('FROM conversaciones')) return { rows: [{ modelo: 'gpt-4.1-mini', conversaciones: 3, entrada: 1_000_000, salida: 0 }, { modelo: 'gemini-flash-latest', conversaciones: 1, entrada: 1000, salida: 1000 }] };
    return { rows: [] };
  };
}
const restaurarBase = () => { (pool as any).query = queryOriginal; tabla.clear(); };

// ── Pruebas puras ────────────────────────────────────────────────────────────
test('detectarProveedor: formatos de cada proveedor', () => {
  assert.equal(C.detectarProveedor(FALSA.eleven), 'elevenlabs');
  assert.equal(C.detectarProveedor(FALSA.elevenHex), 'elevenlabs');
  assert.equal(C.detectarProveedor(FALSA.openai), 'openai');
  assert.equal(C.detectarProveedor(FALSA.openaiLegado), 'openai');
  assert.equal(C.detectarProveedor(FALSA.svc), 'openai');
  assert.equal(C.detectarProveedor(FALSA.admin), 'openai-admin');
  assert.equal(C.detectarProveedor(FALSA.gemini), 'gemini');
  assert.equal(C.detectarProveedor(FALSA.geminiAuth), 'gemini');
  assert.equal(C.detectarProveedor(FALSA.anthropic), 'anthropic');
  assert.equal(C.detectarProveedor('AIzaCorta'), null);
  assert.equal(C.detectarProveedor('hola'), null);
});

test('validarFormato: clave de OpenAI en ElevenLabs se rechaza con mensaje claro', () => {
  const r = C.validarFormato('elevenlabs', 'apiKey', FALSA.openai);
  assert.equal(r.ok, false);
  assert.match((r as any).mensaje, /^Esta clave es de OpenAI, no de ElevenLabs\. Las claves de ElevenLabs empiezan con sk_/);
  sinClaves((r as any).mensaje, 'mensaje');
  assert.match((C.validarFormato('openai', 'apiKey', FALSA.eleven) as any).mensaje, /es de ElevenLabs, no de OpenAI/);
  assert.match((C.validarFormato('gemini', 'apiKey', FALSA.anthropic) as any).mensaje, /es de Anthropic/);
  assert.match((C.validarFormato('openai', 'apiKey', FALSA.admin) as any).mensaje, /Admin key/);
  assert.match((C.validarFormato('openai', 'adminKey', FALSA.openai) as any).mensaje, /no una Admin key/);
  assert.equal(C.validarFormato('openai', 'adminKey', FALSA.admin).ok, true);
  assert.match((C.validarFormato('gemini', 'apiKey', 'abc') as any).mensaje, /demasiado corta/);
  const raro = C.validarFormato('gemini', 'apiKey', 'XYZ' + rnd(30));
  assert.equal(raro.ok, true); assert.match((raro as any).aviso, /no es el habitual/);
});

test('limpiarClave: quita espacios, saltos de línea y comillas pegados', () => {
  assert.equal(C.limpiarClave(`  "${FALSA.eleven}"\n`), FALSA.eleven);
  assert.equal(C.limpiarClave(FALSA.openai.slice(0, 20) + '\n ' + FALSA.openai.slice(20)), FALSA.openai);
  const r = C.validarFormato('elevenlabs', 'apiKey', ` ${FALSA.eleven}\r\n`);
  assert.ok(r.ok && r.clave === FALSA.eleven, 'la clave limpia coincide');
});

test('enmascarar: prefijo no secreto + últimos 4, nunca más', () => {
  assert.equal(C.enmascarar(FALSA.eleven), 'sk_…' + FALSA.eleven.slice(-4));
  assert.equal(C.enmascarar(FALSA.openai), 'sk-proj-…' + FALSA.openai.slice(-4));
  assert.equal(C.enmascarar(FALSA.svc), 'sk-svcac…' + FALSA.svc.slice(-4));
  assert.equal(C.enmascarar(FALSA.gemini), 'AIza…' + FALSA.gemini.slice(-4));
  assert.equal(C.enmascarar(FALSA.elevenHex), '…' + FALSA.elevenHex.slice(-4));
  assert.equal(C.enmascarar('corta'), '••••');
  assert.equal(C.enmascarar(''), null);
  for (const k of Object.values(FALSA)) assert.ok((C.enmascarar(k) ?? '').length <= 13, 'máscara corta');
});

test('cifrado: ida y vuelta, IV distinto y error con otro secreto', () => {
  const datos = { apiKey: FALSA.eleven, modelo: 'eleven_v3' };
  const a = C.cifrar(datos, 's1'), b = C.cifrar(datos, 's1');
  assert.notEqual(a, b);
  assert.ok(a.startsWith('v1:'));
  sinClaves(a, 'texto cifrado');
  assert.deepEqual(C.descifrar(a, 's1'), datos);
  assert.throws(() => C.descifrar(a, 's2'));
  assert.throws(() => C.descifrar('v1:' + Buffer.from('basura-basura-basura-basura-basura').toString('base64'), 's1'));
});

test('aplicar y restaurar sobre config', () => {
  C.aplicar('elevenlabs', { apiKey: FALSA.eleven, modelo: 'eleven_v3' });
  assert.ok(config.elevenApiKey === FALSA.eleven, 'aplica la clave');
  assert.equal(config.elevenModelo, 'eleven_v3');
  C.aplicar('elevenlabs', { modelo: 'eleven_multilingual_v2' }); // sin clave: hereda la del servidor
  assert.ok(config.elevenApiKey === SERVIDOR.eleven, 'hereda la del servidor');
  C.restaurar('elevenlabs');
  assert.ok(config.elevenApiKey === SERVIDOR.eleven, 'restaura la clave');
  assert.equal(config.elevenModelo, 'eleven_flash_v2_5');
  C.aplicar('openai', { adminKey: FALSA.admin });
  assert.ok(C.adminKeyActual() === FALSA.admin, 'admin key aplicada');
  C.restaurar('openai');
  assert.equal(C.adminKeyActual(), '');
});

// ── Verificación con fetch simulado ──────────────────────────────────────────
test('ElevenLabs 200: válida, cuota y modelo; manda la clave en xi-api-key', async () => {
  await conFetch((url, h) => {
    assert.ok(h['xi-api-key'] === FALSA.eleven, 'cabecera xi-api-key');
    return url.endsWith('/v1/user/subscription') ? { status: 200, body: SUB_OK } : { status: 200, body: MODELOS_11 };
  }, async (llamadas) => {
    const r = await C.verificar('elevenlabs', { apiKey: FALSA.eleven });
    assert.equal(r.verificacion?.nivel, 'ok');
    assert.match(r.verificacion!.detalles!.join(' '), /Plan creator/);
    assert.ok(llamadas.every((u) => !u.includes(FALSA.eleven)), 'la clave no va en la URL');
    sinClaves(JSON.stringify(r), 'verificación');
  });
});

test('ElevenLabs 401 inválida → error «Clave inválida»', async () => {
  await conFetch(() => ({ status: 401, body: { detail: { status: 'invalid_api_key', message: 'Invalid API key' } } }), async () => {
    const r = await C.verificar('elevenlabs', { apiKey: FALSA.eleven });
    assert.equal(r.ok, false); assert.equal(r.verificacion?.nivel, 'error');
    assert.match(r.verificacion!.mensaje, /^Clave inválida/);
  });
});

test('ElevenLabs 400 «API key is invalid» → error «Clave inválida»', async () => {
  await conFetch(() => ({ status: 400, body: { detail: { status: 'invalid_api_key', message: 'API key is invalid.' } } }), async () => {
    const r = await C.verificar('elevenlabs', { apiKey: FALSA.eleven });
    assert.equal(r.verificacion?.nivel, 'error');
    assert.match(r.verificacion!.mensaje, /^Clave inválida: ElevenLabs la rechazó \(API key is invalid\.\)/);
  });
});

test('ElevenLabs 401 missing_permissions → válida con aviso de consumo', async () => {
  await conFetch((url) => url.endsWith('/subscription')
    ? { status: 401, body: { detail: { status: 'missing_permissions', message: 'The API key you used is missing the permission user_read to execute this operation.' } } }
    : { status: 200, body: MODELOS_11 }, async () => {
    const r = await C.verificar('elevenlabs', { apiKey: FALSA.eleven });
    assert.equal(r.ok, true); assert.equal(r.verificacion?.nivel, 'aviso');
    assert.match(r.verificacion!.mensaje, /sin permiso «User/);
  });
});

test('formato de otro proveedor: rechazada SIN llamar al proveedor', async () => {
  await conFetch(() => { throw new Error('no debía llamar'); }, async (llamadas) => {
    const r = await C.verificar('elevenlabs', { apiKey: FALSA.openai });
    assert.equal(r.ok, false);
    assert.match(r.errores!.apiKey, /es de OpenAI, no de ElevenLabs/);
    assert.equal(llamadas.length, 0);
  });
});

test('OpenAI: modelos ausentes → aviso; 401 → inválida; admin key consulta costos', async () => {
  await conFetch((url, h) => {
    if (url.includes('/organization/costs')) { assert.ok(h.authorization === `Bearer ${FALSA.admin}`, 'admin en Bearer'); return { status: 200, body: { data: [] } }; }
    return { status: 200, body: { data: [{ id: 'gpt-4.1-mini' }] } };
  }, async (llamadas) => {
    const r = await C.verificar('openai', { apiKey: FALSA.openai, adminKey: FALSA.admin });
    assert.equal(r.verificacion?.nivel, 'aviso');
    assert.match(r.verificacion!.detalles!.join(' '), /«gpt-4\.1» no aparece/);
    assert.match(r.verificacion!.detalles!.join(' '), /Admin key válida/);
    assert.ok(llamadas.some((u) => /organization\/costs\?start_time=\d+/.test(u)));
  });
  await conFetch(() => ({ status: 401, body: { error: { message: `Incorrect API key provided: ${FALSA.openai}.`, code: 'invalid_api_key' } } }), async () => {
    const r = await C.verificar('openai', { apiKey: FALSA.openai });
    assert.equal(r.verificacion?.nivel, 'error');
    assert.match(r.verificacion!.mensaje, /^Clave inválida/);
    sinClaves(r.verificacion!.mensaje, 'mensaje del proveedor');
  });
});

test('Gemini 403 «denied access»: se muestra el mensaje del proveedor tal cual', async () => {
  await conFetch(() => ({ status: 403, body: { error: { code: 403, message: 'Your project has been denied access. Please contact support.', status: 'PERMISSION_DENIED' } } }), async () => {
    const r = await C.verificar('gemini', { apiKey: FALSA.gemini });
    assert.equal(r.verificacion?.nivel, 'error');
    assert.match(r.verificacion!.mensaje, /403.*Your project has been denied access/);
  });
  await conFetch((_u, h) => { assert.ok(h['x-goog-api-key'] === FALSA.geminiAuth, 'cabecera'); return { status: 200, body: { models: [{ name: 'models/gemini-flash-latest' }] } }; }, async () => {
    const r = await C.verificar('gemini', { apiKey: FALSA.geminiAuth });
    assert.equal(r.verificacion?.nivel, 'ok');
  });
});

test('timeout: error legible sin colgarse', async () => {
  await conFetch(() => 'colgar', async () => {
    const r = await C.verificar('openai', { apiKey: FALSA.openai }, { timeoutMs: 50 });
    assert.equal(r.verificacion?.nivel, 'error');
    assert.match(r.verificacion!.mensaje, /tiempo de espera agotado/);
  });
});

// ── Guardar / eliminar / cargar ──────────────────────────────────────────────
test('guardar: solo si la verificación no da error; cifra, aplica y se recarga; eliminar restaura', async () => {
  baseSimulada();
  try {
    await conFetch(() => ({ status: 401, body: { detail: { status: 'invalid_api_key', message: 'Invalid API key' } } }), async () => {
      const r = await C.guardar('elevenlabs', { apiKey: FALSA.eleven });
      assert.equal(r.ok, false); assert.equal(tabla.size, 0);
      assert.ok(config.elevenApiKey === SERVIDOR.eleven, 'no se aplicó');
    });
    await conFetch((url) => url.endsWith('/subscription') ? { status: 200, body: SUB_OK } : { status: 200, body: MODELOS_11 }, async () => {
      const r = await C.guardar('elevenlabs', { apiKey: `  ${FALSA.eleven}\n`, modelo: 'eleven_multilingual_v2' });
      assert.equal(r.ok, true);
      assert.ok(config.elevenApiKey === FALSA.eleven, 'aplicada en caliente');
      const fila = tabla.get('elevenlabs')!;
      sinClaves(fila.datos, 'fila guardada');
      assert.deepEqual(C.descifrar(fila.datos, config.jwtSecret), { apiKey: FALSA.eleven, modelo: 'eleven_multilingual_v2' });
      // Vacío = conserva la clave y solo cambia el modelo.
      const r2 = await C.guardar('elevenlabs', { apiKey: '', modelo: 'eleven_v3' });
      assert.equal(r2.ok, true);
      assert.ok(config.elevenApiKey === FALSA.eleven, 'conserva la clave');
      assert.equal(config.elevenModelo, 'eleven_v3');
    });
    // Reinicio simulado: se vuelve al .env y cargarConexiones aplica lo guardado.
    C.restaurar('elevenlabs');
    await C.cargarConexiones();
    assert.ok(config.elevenApiKey === FALSA.eleven, 'recargada al arrancar');
    // Otro JWT_SECRET: no se puede descifrar → .env + aviso.
    const secreto = config.jwtSecret; config.jwtSecret = 'otro-secreto';
    await C.cargarConexiones();
    config.jwtSecret = secreto;
    assert.ok(config.elevenApiKey === SERVIDOR.eleven, 'usa el .env');
    const e = C.resumen().proveedores.find((p) => p.id === 'elevenlabs')!;
    assert.match(e.avisos.join(' '), /no se pudo descifrar/);
    await C.cargarConexiones();
    await C.eliminar('elevenlabs');
    assert.equal(tabla.size, 0);
    assert.ok(config.elevenApiKey === SERVIDOR.eleven, 'vuelve al servidor');
    assert.equal(config.elevenModelo, 'eleven_flash_v2_5');
  } finally { restaurarBase(); C.restaurar('elevenlabs'); }
});

// ── Rutas ────────────────────────────────────────────────────────────────────
async function montar() {
  const { default: Fastify } = await import('fastify');
  const { default: jwt } = await import('@fastify/jwt');
  const { default: rutas } = await import('../src/routes/conexiones.js');
  const app = Fastify(); await app.register(jwt, { secret: 'test-only-panel-secret' }); await app.register(rutas);
  return { app, admin: { authorization: `Bearer ${app.jwt.sign({ sub: 'admin', rol: 'admin' })}` }, alumno: { authorization: `Bearer ${app.jwt.sign({ sub: 'x', rol: 'alumno' })}` } };
}

test('rutas: piden administrador; GET no filtra claves; verificar rechaza formato ajeno; consumo con fallos aislados', async () => {
  baseSimulada();
  const { app, admin, alumno } = await montar();
  try {
    for (const [method, url] of [['GET', '/admin/conexiones'], ['GET', '/admin/conexiones/consumo'], ['POST', '/admin/conexiones/openai/verificar'], ['PUT', '/admin/conexiones/openai'], ['DELETE', '/admin/conexiones/openai']] as const) {
      assert.equal((await app.inject({ method, url })).statusCode, 401, url);
      assert.equal((await app.inject({ method, url, headers: alumno })).statusCode, 403, url);
    }
    C.aplicar('openai', { adminKey: FALSA.admin });
    const g = await app.inject({ url: '/admin/conexiones', headers: admin });
    assert.equal(g.statusCode, 200);
    sinClaves(g.body, 'GET /admin/conexiones');
    const d = g.json();
    const oai = d.proveedores.find((p: any) => p.id === 'openai');
    assert.equal(oai.origen, 'panel'); assert.equal(oai.claveOrigen, 'servidor');
    assert.equal(oai.clave, 'sk-proj-…' + SERVIDOR.openai.slice(-4));
    assert.equal(oai.adminKey, 'sk-admin…' + FALSA.admin.slice(-4));
    assert.equal(d.proveedores.find((p: any) => p.id === 'gemini').origen, 'sin configurar');
    assert.equal(d.proveedores.find((p: any) => p.id === 'elevenlabs').origen, 'servidor');
    C.restaurar('openai');

    await conFetch(() => { throw new Error('no debía llamar'); }, async (llamadas) => {
      const r = await app.inject({ method: 'POST', url: '/admin/conexiones/elevenlabs/verificar', headers: admin, payload: { apiKey: FALSA.openai } });
      assert.equal(r.statusCode, 400);
      assert.match(r.json().errores.apiKey, /Esta clave es de OpenAI, no de ElevenLabs/);
      sinClaves(r.body, 'respuesta de verificar');
      assert.equal(llamadas.length, 0);
    });
    assert.equal((await app.inject({ method: 'POST', url: '/admin/conexiones/anthropic/verificar', headers: admin, payload: {} })).statusCode, 404);

    await conFetch((url) => {
      if (url.includes('elevenlabs')) throw new Error('caída de red');
      return { status: 200, body: {} };
    }, async () => {
      const r = await app.inject({ url: '/admin/conexiones/consumo', headers: admin });
      assert.equal(r.statusCode, 200);
      const c = r.json();
      assert.equal(c.elevenlabs.tipo, 'error'); assert.equal(c.elevenlabs.onelingo.caracteres_mes, 1000);
      assert.equal(c.openai.tipo, 'estimado'); assert.ok(Math.abs(c.openai.estimado.coste - 0.4) < 1e-9);
      assert.equal(c.gemini.tipo, 'estimado'); assert.match(c.gemini.enlace, /aistudio\.google\.com/);
      sinClaves(r.body, 'consumo');
    });
  } finally { await app.close(); restaurarBase(); }
});
