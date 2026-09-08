/**
 * Empaqueta las unidades en los assets que lee la app:
 *   assets/contenido/<idioma>/nivel-N.json  → { nivel, idioma, unidades: [...] }
 * Solo escribe niveles completos (20 unidades) salvo --parcial.
 */
import fs from "node:fs";
import path from "node:path";
import { CODIGOS, FicheroUnidadSchema, FicheroFundamentosSchema, FicheroDiagSchema } from "./esquema.js";
import { RAIZ } from "./prompt.js";

const parcial = process.argv.includes("--parcial");
const DIR = path.join(RAIZ, "content");
const DEST = path.join(RAIZ, "assets/contenido");
let escritos = 0;
for (const idioma of CODIGOS) {
  // Diagnóstico adaptativo: banco de preguntas del idioma.
  const fdiag = path.join(DIR, idioma, "diagnostico.json");
  if (fs.existsSync(fdiag)) {
    const d = FicheroDiagSchema.parse(JSON.parse(fs.readFileSync(fdiag, "utf8")));
    fs.mkdirSync(path.join(DEST, idioma), { recursive: true });
    fs.writeFileSync(path.join(DEST, idioma, "diagnostico.json"), JSON.stringify(d));
    escritos++;
    console.log(`✓ ${idioma} diagnóstico: ${d.preguntas.length} preguntas`);
  }
  // Nivel 0 (Fundamentos): número de unidades variable, esquema propio.
  const dir0 = path.join(DIR, idioma, "nivel-0");
  if (fs.existsSync(dir0)) {
    const unidades = fs.readdirSync(dir0).filter((x) => x.endsWith(".json"))
      .map((f) => FicheroFundamentosSchema.parse(JSON.parse(fs.readFileSync(path.join(dir0, f), "utf8"))))
      .sort((a, b) => a.unidad - b.unidad);
    if (unidades.length > 0) {
      fs.mkdirSync(path.join(DEST, idioma), { recursive: true });
      fs.writeFileSync(path.join(DEST, idioma, "nivel-0.json"), JSON.stringify({ idioma, nivel: 0, generado: new Date().toISOString(), unidades: unidades.map((u) => ({ numero: u.unidad, ...u.contenido })) }));
      escritos++;
      console.log(`✓ ${idioma} nivel 0: ${unidades.length} unidades (Fundamentos)`);
    }
  }
  for (let n = 1; n <= 10; n++) {
    const dir = path.join(DIR, idioma, `nivel-${n}`);
    if (!fs.existsSync(dir)) continue;
    const unidades = fs
      .readdirSync(dir)
      .filter((x) => x.endsWith(".json"))
      .map((f) => FicheroUnidadSchema.parse(JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"))))
      .sort((a, b) => a.unidad - b.unidad);
    if (unidades.length === 0) continue;
    if (unidades.length < 20 && !parcial) { console.log(`· ${idioma} nivel ${n}: ${unidades.length}/20, omitido (usa --parcial)`); continue; }
    const salida = {
      idioma, nivel: n, generado: new Date().toISOString(),
      unidades: unidades.map((u) => ({ numero: u.unidad, tema: u.tema, ...u.contenido })),
    };
    fs.mkdirSync(path.join(DEST, idioma), { recursive: true });
    fs.writeFileSync(path.join(DEST, idioma, `nivel-${n}.json`), JSON.stringify(salida));
    escritos++;
    console.log(`✓ ${idioma} nivel ${n}: ${unidades.length} unidades`);
  }
}
console.log(`\n${escritos} ficheros escritos en assets/contenido/. Ejecuta 'flutter build' para incluirlos.`);
