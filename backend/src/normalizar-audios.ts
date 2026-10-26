/**
 * Lleva los MP3 ya guardados en la caché de voz a OBJETIVO_LUFS (ver lib/volumen.ts).
 * Los nuevos ya se guardan así; esto es para los generados antes. Se puede
 * repetir: un clip que ya está en el objetivo se deja como está.
 *   npm run normalizar-audios
 */
import { readdir, readFile, rename, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { config } from './lib/config.js';
import { ffmpegDisponible, medirLufs, normalizarVolumen, OBJETIVO_LUFS } from './lib/volumen.js';

const dir = path.resolve(config.audioDir);
if (!(await ffmpegDisponible())) { console.error('Falta ffmpeg (instálalo o define FFMPEG).'); process.exit(1); }
const archivos = (await readdir(dir)).filter((f) => f.endsWith('.mp3'));
let cambiados = 0, iguales = 0, fallidos = 0, hechos = 0;

async function uno(nombre: string) {
  const ruta = path.join(dir, nombre);
  try {
    const original = await readFile(ruta);
    const lufs = await medirLufs(original);
    if (lufs === null || Math.abs(lufs - OBJETIVO_LUFS) < 1) { iguales++; return; }
    const nuevo = await normalizarVolumen(original);
    if (nuevo === original) { iguales++; return; }
    const temp = `${ruta}.${process.pid}.vol`;
    await writeFile(temp, nuevo);
    await rename(temp, ruta);
    cambiados++;
  } catch (e) {
    fallidos++;
    console.error(nombre, String(e).slice(0, 160));
  } finally {
    if (++hechos % 200 === 0) console.log(`${hechos}/${archivos.length}`);
  }
}

const cola = [...archivos];
await Promise.all(Array.from({ length: 4 }, async () => { for (let f = cola.shift(); f; f = cola.shift()) await uno(f); }));
console.log(`Listo: ${cambiados} ajustados, ${iguales} ya estaban bien o sin medir, ${fallidos} con error, de ${archivos.length}.`);
