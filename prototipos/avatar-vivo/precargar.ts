/**
 * Deja en la caché de voz del backend todas las frases de prueba (frases.json)
 * con la voz de cada tutor en vivo, para que en la sala de pruebas suenen al
 * instante. Las frases que ya están no se vuelven a pedir a ElevenLabs.
 *
 *   cd backend && npx tsx ../prototipos/avatar-vivo/precargar.ts
 */
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { obtenerAudioAlineado } from '../../backend/src/lib/voz.js';

const RAIZ = path.dirname(fileURLToPath(import.meta.url));
// Sin await de primer nivel: tsx compila a CommonJS dentro de backend/.
async function main() {
  const frases: Record<string, string[]> = JSON.parse(await readFile(path.join(RAIZ, 'frases.json'), 'utf8'));
  const roster = JSON.parse(await readFile(path.join(RAIZ, '../../web/avatar/roster.json'), 'utf8'));
  const tutores: string[] = roster.tutors.filter((t: any) => t.tipo === 'th').map((t: any) => t.id);

  const tareas = tutores.flatMap((tutor) => Object.entries(frases).flatMap(([idioma, lista]) => lista.map((texto) => ({ tutor, idioma, texto }))));
  let nuevas = 0, cache = 0, fallos = 0, caracteres = 0;
  // De a 4 a la vez: la misma voz se repite entre tutores y la caché la resuelve.
  for (let i = 0; i < tareas.length; i += 4) {
    await Promise.all(tareas.slice(i, i + 4).map(async ({ tutor, idioma, texto }) => {
      try {
        const a = await obtenerAudioAlineado({ texto, idioma, voz: `avatar_${tutor}` });
        if (a.cache) cache++; else { nuevas++; caracteres += texto.length; }
        if (!a.alineacion) console.warn(`sin alineación: ${tutor}/${idioma}: ${texto.slice(0, 30)}`);
      } catch (e) { fallos++; console.error(`${tutor}/${idioma}: ${String(e).slice(0, 160)}`); }
    }));
  }
  console.log(`Frases: ${tareas.length} · nuevas ${nuevas} (${caracteres} caracteres) · ya en caché ${cache} · fallos ${fallos}`);
}
main().catch((e) => { console.error(e); process.exit(1); });
