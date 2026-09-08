/** Valida todos los ficheros de content/<idioma>/nivel-N/unidad-NN.json y resume la cobertura. */
import fs from "node:fs";
import path from "node:path";
import { CODIGOS, FicheroUnidadSchema, IDIOMAS, type Idioma } from "./esquema.js";
import { RAIZ } from "./prompt.js";

const DIR = path.join(RAIZ, "content");
let total = 0, errores = 0;
const cobertura: Record<string, number[]> = {};
for (const idioma of CODIGOS) {
  cobertura[idioma] = Array(10).fill(0);
  for (let n = 1; n <= 10; n++) {
    const dir = path.join(DIR, idioma, `nivel-${n}`);
    if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".json"))) {
      total++;
      try {
        const j = FicheroUnidadSchema.parse(JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")));
        const rom = IDIOMAS[j.idioma as Idioma].romanizacion;
        const problemas: string[] = [];
        for (const v of j.contenido.vocab) {
          if (rom && !v.romanizacion) problemas.push(`sin romanización: ${v.palabra}`);
          if (!rom && v.romanizacion) problemas.push(`romanización sobrante: ${v.palabra}`);
        }
        const palabras = new Set(j.contenido.vocab.map((v) => v.palabra.toLowerCase()));
        if (palabras.size !== j.contenido.vocab.length) problemas.push("vocabulario repetido");
        for (const q of j.contenido.examen) if (new Set(q.opciones).size !== 4) problemas.push("opciones de examen repetidas");
        if (problemas.length) { errores++; console.log(`⚠ ${idioma} n${n} ${f}: ${problemas.join("; ")}`); }
        else cobertura[idioma][n - 1]++;
      } catch (e) {
        errores++;
        console.log(`✗ ${idioma} n${n} ${f}: ${String(e).slice(0, 120)}`);
      }
    }
  }
}
console.log(`\nFicheros: ${total} · con problemas: ${errores}`);
console.log("Cobertura (unidades válidas por nivel 1..10):");
for (const idioma of CODIGOS) console.log(`  ${idioma}: ${cobertura[idioma].map((x) => String(x).padStart(2)).join(" ")}  (${cobertura[idioma].reduce((a, b) => a + b, 0)}/200)`);
process.exit(errores ? 1 : 0);
