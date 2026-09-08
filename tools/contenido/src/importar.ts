/**
 * Importa contenido escrito a mano desde semilla/<idioma>-nivel-N.txt y lo guarda
 * como content/<idioma>/nivel-N/unidad-NN.json (mismo formato que el generador).
 *
 * Formato (una línea por elemento, campos separados por " | "):
 *   # 3 | Título | Objetivo | Gramática                 ← empieza la unidad 3
 *   V palabra | [romanización |] traducción | ejemplo   ← vocabulario (8-10)
 *   F texto | [romanización |] traducción               ← frases (6-8)
 *   D quién | texto | [romanización |] traducción       ← diálogo (4-8)
 *   E incorrecto | correcto | explicación               ← errores típicos (2-4)
 *   X pregunta | op1 ; op2 ; op3 ; op4 | índice | explicación   ← examen (3-4)
 * La romanización solo se escribe en zh/ja/ko/ru; en el resto se omite.
 */
import fs from "node:fs";
import path from "node:path";
import { CODIGOS, IDIOMAS, UnidadSchema, FundamentosUnidadSchema, PreguntaDiagSchema, type Idioma } from "./esquema.js";
import { RAIZ, cargarPlan } from "./prompt.js";

const args = process.argv.slice(2);
const soloIdioma = args.find((a) => a.startsWith("--idioma="))?.split("=")[1];
const DIR = new URL("../semilla", import.meta.url).pathname;
const OUT = path.join(RAIZ, "content");
const sep = (l: string) => l.split("|").map((x) => x.trim());

/**
 * Nivel 0 (Fundamentos):
 *   # 1 | escritura|vocabulario | Título | Descripción
 *   S símbolo | cómo suena | nota en español | ejemplo          ← letra, sílaba o sonido
 *   V palabra | [romanización |] traducción | ejemplo            ← palabra suelta
 *   X pregunta | op1 ; op2 ; op3 ; op4 | índice | explicación
 */
function parsearFundamentos(idioma: Idioma, texto: string) {
  const rom = !!IDIOMAS[idioma].romanizacion;
  const unidades: { numero: number; contenido: any }[] = [];
  let u: any = null;
  let n = 0;
  for (const raw of texto.split("\n")) {
    n++;
    const linea = raw.trim();
    if (!linea || linea.startsWith("//")) continue;
    const tipo = linea[0];
    const c = sep(linea.slice(1).trim());
    try {
      if (tipo === "#") {
        u = { tipo: c[1], titulo: c[2], descripcion: c[3], items: [], examen: [] };
        unidades.push({ numero: Number(c[0]), contenido: u });
      } else if (!u) throw new Error("elemento antes de la cabecera # de unidad");
      else if (tipo === "S") {
        u.items.push({ simbolo: c[0], romanizacion: c[1], significado: c[2], ejemplo: c[3] ?? "" });
      } else if (tipo === "V") {
        const [simbolo, r, significado, ejemplo] = rom ? c : [c[0], "", c[1], c[2]];
        u.items.push({ simbolo, romanizacion: r ?? "", significado, ejemplo: ejemplo ?? "" });
      } else if (tipo === "X") {
        u.examen.push({ pregunta: c[0], opciones: c[1].split(";").map((x) => x.trim()), correcta: Number(c[2]), explicacion: c[3] });
      } else throw new Error(`tipo desconocido '${tipo}' en nivel 0`);
    } catch (e) {
      throw new Error(`${idioma} nivel 0 línea ${n}: ${String(e)}`);
    }
  }
  return unidades;
}

/**
 * Diagnóstico (semilla/<idioma>-diagnostico.txt), una pregunta por línea:
 *   Q nivel | skill | tipo | tema | instrucción | texto | opciones (a ; b ; c ; d) o - | correcta (índice, o respuestas aceptadas "x ; y", o -) | explicación
 * Tipos: eleccion, natural, significado, contexto, situacion, error, completar, corta, escucha, dictado, escritura.
 * En dictado, si correcta es "-", se acepta el propio texto. En escritura no hay respuesta.
 */
function parsearDiagnostico(idioma: Idioma, texto: string) {
  const out: any[] = [];
  let n = 0;
  for (const raw of texto.split("\n")) {
    n++;
    const linea = raw.trim();
    if (!linea || linea.startsWith("//")) continue;
    if (!linea.startsWith("Q")) throw new Error(`${idioma} diagnóstico línea ${n}: debe empezar por Q`);
    const c = sep(linea.slice(1).trim());
    if (c.length < 9) throw new Error(`${idioma} diagnóstico línea ${n}: faltan campos (${c.length}/9)`);
    const [nivel, skill, tipo, tema, instruccion, txt, ops, corr, explicacion] = c;
    const opciones = ops === "-" ? [] : ops.split(";").map((x) => x.trim()).filter(Boolean);
    let correcta = -1;
    let aceptadas: string[] = [];
    if (opciones.length > 0) correcta = Number(corr);
    else if (tipo === "dictado" && corr === "-") aceptadas = [txt];
    else if (corr !== "-") aceptadas = corr.split(";").map((x) => x.trim()).filter(Boolean);
    out.push({ nivel: Number(nivel), skill, tipo, tema, instruccion, texto: txt, opciones, correcta, aceptadas, explicacion });
  }
  return out;
}

function parsear(idioma: Idioma, nivel: number, texto: string) {
  const rom = !!IDIOMAS[idioma].romanizacion;
  const unidades: { numero: number; contenido: any }[] = [];
  let u: any = null;
  let n = 0;
  for (const raw of texto.split("\n")) {
    n++;
    const linea = raw.trim();
    if (!linea || linea.startsWith("//")) continue;
    const tipo = linea[0];
    const resto = linea.slice(1).trim();
    const c = sep(resto);
    try {
      if (tipo === "#") {
        u = { titulo: c[1], objetivo: c[2], gramatica: c[3], vocab: [], frases: [], dialogo: [], errores_tipicos: [], examen: [] };
        unidades.push({ numero: Number(c[0]), contenido: u });
      } else if (!u) throw new Error("elemento antes de la cabecera # de unidad");
      else if (tipo === "V") {
        const [palabra, r, traduccion, ejemplo] = rom ? c : [c[0], "", c[1], c[2]];
        u.vocab.push({ palabra, romanizacion: r ?? "", traduccion, ejemplo });
      } else if (tipo === "F") {
        const [t, r, traduccion] = rom ? c : [c[0], "", c[1]];
        u.frases.push({ texto: t, romanizacion: r ?? "", traduccion });
      } else if (tipo === "D") {
        const [quien, t, r, traduccion] = rom ? c : [c[0], c[1], "", c[2]];
        u.dialogo.push({ quien, texto: t, romanizacion: r ?? "", traduccion });
      } else if (tipo === "E") {
        u.errores_tipicos.push({ incorrecto: c[0], correcto: c[1], explicacion: c[2] });
      } else if (tipo === "X") {
        const opciones = c[1].split(";").map((x) => x.trim());
        u.examen.push({ pregunta: c[0], opciones, correcta: Number(c[2]), explicacion: c[3] });
      } else throw new Error(`tipo desconocido '${tipo}'`);
    } catch (e) {
      throw new Error(`${idioma} nivel ${nivel} línea ${n}: ${String(e)}`);
    }
  }
  return unidades;
}

let total = 0, errores = 0;
for (const idioma of CODIGOS) {
  if (soloIdioma && idioma !== soloIdioma) continue;
  const fd = path.join(DIR, `${idioma}-diagnostico.txt`);
  if (fs.existsSync(fd)) {
    const preguntas = parsearDiagnostico(idioma, fs.readFileSync(fd, "utf8"));
    let malas = 0;
    const buenas: any[] = [];
    preguntas.forEach((q, i) => {
      const v = PreguntaDiagSchema.safeParse(q);
      if (!v.success) { malas++; errores++; console.log(`✗ ${idioma} diagnóstico #${i + 1} (nivel ${q.nivel}): ${v.error.issues.map((x) => `${x.path.join(".")}: ${x.message}`).join("; ")}`); }
      else buenas.push(v.data);
    });
    fs.mkdirSync(path.join(OUT, idioma), { recursive: true });
    fs.writeFileSync(path.join(OUT, idioma, "diagnostico.json"), JSON.stringify({ idioma, generado: new Date().toISOString(), preguntas: buenas }, null, 2));
    const porNivel = buenas.reduce((m: Record<number, number>, q) => ((m[q.nivel] = (m[q.nivel] ?? 0) + 1), m), {});
    console.log(`✓ ${idioma} diagnóstico: ${buenas.length} preguntas${malas ? ` (${malas} con errores)` : ""} · por nivel ${JSON.stringify(porNivel)}`);
  }
  for (let nivel = 0; nivel <= 10; nivel++) {
    const f = path.join(DIR, `${idioma}-nivel-${nivel}.txt`);
    if (!fs.existsSync(f)) continue;
    if (nivel === 0) {
      const unidades = parsearFundamentos(idioma, fs.readFileSync(f, "utf8"));
      for (const { numero, contenido } of unidades) {
        const v = FundamentosUnidadSchema.safeParse(contenido);
        if (!v.success) { errores++; console.log(`✗ ${idioma} n0 u${numero}: ${v.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ")}`); continue; }
        const dir = path.join(OUT, idioma, "nivel-0");
        fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(path.join(dir, `unidad-${String(numero).padStart(2, "0")}.json`),
          JSON.stringify({ idioma, nivel: 0, unidad: numero, tema: contenido.titulo, cefr: "A0", modelo: "manual:onelingo", generado: new Date().toISOString(), contenido: v.data }, null, 2));
        total++;
      }
      console.log(`✓ ${idioma} nivel 0: ${unidades.length} unidades en semilla`);
      continue;
    }
    const temas = cargarPlan().niveles[nivel - 1];
    const unidades = parsear(idioma, nivel, fs.readFileSync(f, "utf8"));
    for (const { numero, contenido } of unidades) {
      const v = UnidadSchema.safeParse(contenido);
      if (!v.success) {
        errores++;
        console.log(`✗ ${idioma} n${nivel} u${numero}: ${v.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ")}`);
        continue;
      }
      const tema = temas.unidades.find((x: any) => x.numero === numero)?.tema ?? contenido.titulo;
      const dir = path.join(OUT, idioma, `nivel-${nivel}`);
      fs.mkdirSync(dir, { recursive: true });
      const fichero = { idioma, nivel, unidad: numero, tema, cefr: temas.cefr, modelo: "manual:onelingo", generado: new Date().toISOString(), contenido: v.data };
      fs.writeFileSync(path.join(dir, `unidad-${String(numero).padStart(2, "0")}.json`), JSON.stringify(fichero, null, 2));
      total++;
    }
    console.log(`✓ ${idioma} nivel ${nivel}: ${unidades.length} unidades en semilla`);
  }
}
console.log(`\n${total} unidades importadas, ${errores} con errores.`);
if (errores) process.exit(1);
