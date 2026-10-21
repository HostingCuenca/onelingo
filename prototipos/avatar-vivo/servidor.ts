/**
 * Piloto local de TalkingHead (no se despliega). Sirve esta carpeta y
 * POST /tts → ElevenLabs «with-timestamps»: audio + tiempo de cada letra, para
 * mover la boca con las sílabas reales. La clave sale de la config del backend
 * (se arranca desde backend/ para que lea su .env); nunca llega al navegador.
 * Las respuestas se guardan en cache/ para no pagar dos veces la misma frase.
 *
 *   cd backend && npx tsx ../prototipos/avatar-vivo/servidor.ts
 */
import { createServer } from 'node:http';
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { config } from '../../backend/src/lib/config.js';
import { VOCES, NATIVAS, cuerpoSintesis, ajustesDeVoz, type Rol } from '../../backend/src/lib/voz.js';

const RAIZ = path.dirname(fileURLToPath(import.meta.url));
const PUERTO = Number(process.env.PUERTO ?? 8197);
const TIPOS: Record<string, string> = { '.html': 'text/html; charset=utf-8', '.mjs': 'text/javascript', '.js': 'text/javascript', '.glb': 'model/gltf-binary', '.png': 'image/png', '.json': 'application/json' };

async function tts(texto: string, idioma: string, rol: Rol) {
  const clave = NATIVAS[idioma]?.[rol];
  if (!clave) throw new Error(`Sin voz para ${idioma}/${rol}`);
  const voz = VOCES[clave];
  const cuerpo = cuerpoSintesis(texto, idioma, config.elevenModelo, undefined, ajustesDeVoz(clave));
  const archivo = path.join(RAIZ, 'cache', createHash('sha256').update(JSON.stringify([voz.id, cuerpo])).digest('hex').slice(0, 24) + '.json');
  try { return JSON.parse(await readFile(archivo, 'utf8')); } catch { /* no está en caché */ }
  const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voz.id}/with-timestamps?output_format=mp3_44100_128`, {
    method: 'POST', headers: { 'xi-api-key': config.elevenApiKey, 'content-type': 'application/json' }, body: JSON.stringify(cuerpo),
  });
  if (!r.ok) throw new Error(`ElevenLabs ${r.status}: ${(await r.text()).slice(0, 200)}`);
  const d = await r.json() as { audio_base64: string; alignment: unknown; normalized_alignment: unknown };
  const res = { voz: voz.nombre, audio: d.audio_base64, alineacion: d.alignment ?? d.normalized_alignment, caracteres: texto.length };
  await writeFile(archivo, JSON.stringify(res));
  return res;
}

createServer(async (req, res) => {
  try {
    const url = new URL(req.url ?? '/', 'http://x');
    if (req.method === 'POST' && url.pathname === '/tts') {
      let b = ''; for await (const c of req) b += c;
      const { texto, idioma, rol } = JSON.parse(b);
      if (typeof texto !== 'string' || !texto.trim() || texto.length > 400) throw new Error('Texto vacío o demasiado largo');
      res.writeHead(200, { 'content-type': 'application/json' }); res.end(JSON.stringify(await tts(texto.trim(), idioma, rol)));
      return;
    }
    if (req.method === 'POST' && url.pathname === '/captura') {
      // Solo para comparar looks a resolución completa: guarda el lienzo en render/<nombre>.png.
      let b = ''; for await (const c of req) b += c;
      const { nombre, png } = JSON.parse(b);
      if (!/^[a-z0-9-]{1,40}$/.test(nombre) || !String(png).startsWith('data:image/png;base64,')) throw new Error('Captura inválida');
      await writeFile(path.join(RAIZ, 'render', `${nombre}.png`), Buffer.from(String(png).split(',')[1], 'base64'));
      res.writeHead(204).end(); return;
    }
    const ruta = path.normalize(path.join(RAIZ, url.pathname === '/' ? 'index.html' : decodeURIComponent(url.pathname)));
    if (!ruta.startsWith(RAIZ + path.sep) || ruta.includes(`${path.sep}cache${path.sep}`)) { res.writeHead(403).end(); return; }
    const datos = await readFile(ruta);
    res.writeHead(200, { 'content-type': TIPOS[path.extname(ruta)] ?? 'application/octet-stream', 'cache-control': 'no-cache' }); res.end(datos);
  } catch (e: any) {
    res.writeHead(e?.code === 'ENOENT' ? 404 : 500, { 'content-type': 'application/json' }); res.end(JSON.stringify({ error: e?.message ?? String(e) }));
  }
}).listen(PUERTO, '127.0.0.1', () => console.log(`Piloto avatar en http://127.0.0.1:${PUERTO} · voz ${config.elevenApiKey ? 'lista' : 'SIN CLAVE'}`));
