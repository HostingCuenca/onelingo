/**
 * Genera unidades de contenido con Claude.
 *
 *   npm run generar -- --idioma zh --nivel 1              # 20 unidades, modo directo
 *   npm run generar -- --idioma zh --nivel 1 --unidad 3   # una unidad
 *   npm run generar -- --todo --batch                     # 2 000 unidades vía Batches (50 % de coste)
 *   npm run generar -- --recoger msgbatch_xxx             # descarga los resultados de un batch
 *   npm run generar -- --todo --dry-run                   # solo cuenta y estima coste
 *
 * Opciones: --modelo claude-opus-5 (por defecto) · --concurrencia 4 · --forzar (regenera existentes)
 */
import fs from "node:fs";
import path from "node:path";
import Anthropic from "@anthropic-ai/sdk";
import { existsSync, readFileSync } from "node:fs";

/** Carga tools/contenido/.env (sin dependencia dotenv): KEY=valor por línea. */
function cargarEnv(ruta: string) {
  if (!existsSync(ruta)) return;
  for (const linea of readFileSync(ruta, "utf8").split("\n")) {
    const m = linea.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, "");
  }
}
cargarEnv(new URL("../.env", import.meta.url).pathname);
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";
import { CODIGOS, FicheroUnidadSchema, UnidadSchema, type FicheroUnidad, type Idioma } from "./esquema.js";
import { cargarPlan, RAIZ, systemPrompt, userPrompt, type PlanNivel } from "./prompt.js";
import { generarUnidadGemini } from "./gemini.js";

type Args = Record<string, string | boolean>;
function args(): Args {
  const a: Args = {};
  const v = process.argv.slice(2);
  for (let i = 0; i < v.length; i++) {
    const k = v[i];
    if (!k.startsWith("--")) continue;
    const next = v[i + 1];
    if (next && !next.startsWith("--")) { a[k.slice(2)] = next; i++; } else a[k.slice(2)] = true;
  }
  return a;
}

const A = args();
const PROVEEDOR = String(A.proveedor ?? (process.env.GEMINI_API_KEY && !process.env.ANTHROPIC_API_KEY ? "gemini" : "claude"));
const MODELO = String(A.modelo ?? (PROVEEDOR === "gemini" ? "gemini-flash-latest" : "claude-opus-5"));
const CONCURRENCIA = Number(A.concurrencia ?? 4);
const MAX_TOKENS = 16000;
const DIR_CONTENIDO = path.join(RAIZ, "content");
const DIR_ESTADO = path.join(RAIZ, "content/.estado");
fs.mkdirSync(DIR_ESTADO, { recursive: true });

type Tarea = { idioma: Idioma; nivel: PlanNivel; unidad: { numero: number; tema: string } };
const rutaUnidad = (t: Tarea) =>
  path.join(DIR_CONTENIDO, t.idioma, `nivel-${t.nivel.numero}`, `unidad-${String(t.unidad.numero).padStart(2, "0")}.json`);
const idTarea = (t: Tarea) => `${t.idioma}-n${t.nivel.numero}-u${String(t.unidad.numero).padStart(2, "0")}`;

function tareasPendientes(): Tarea[] {
  const plan = cargarPlan();
  const idiomas: Idioma[] = A.todo ? CODIGOS : [String(A.idioma ?? "en") as Idioma];
  const niveles = A.todo || !A.nivel ? plan.niveles : plan.niveles.filter((n) => n.numero === Number(A.nivel));
  const out: Tarea[] = [];
  for (const idioma of idiomas) {
    if (!CODIGOS.includes(idioma)) throw new Error(`Idioma desconocido: ${idioma}`);
    for (const nivel of niveles) {
      for (const unidad of nivel.unidades) {
        if (A.unidad && unidad.numero !== Number(A.unidad)) continue;
        const t = { idioma, nivel, unidad };
        if (!A.forzar && fs.existsSync(rutaUnidad(t))) continue;
        out.push(t);
      }
    }
  }
  return out;
}

function guardar(t: Tarea, contenido: unknown) {
  const fichero: FicheroUnidad = FicheroUnidadSchema.parse({
    idioma: t.idioma,
    nivel: t.nivel.numero,
    unidad: t.unidad.numero,
    tema: t.unidad.tema,
    cefr: t.nivel.cefr,
    modelo: `${PROVEEDOR}:${MODELO}`,
    generado: new Date().toISOString(),
    contenido: UnidadSchema.parse(contenido),
  });
  const ruta = rutaUnidad(t);
  fs.mkdirSync(path.dirname(ruta), { recursive: true });
  fs.writeFileSync(ruta, JSON.stringify(fichero, null, 2) + "\n");
}

const paramsDe = (t: Tarea): Anthropic.MessageCreateParamsNonStreaming => ({
  model: MODELO,
  max_tokens: MAX_TOKENS,
  system: [{ type: "text", text: systemPrompt(), cache_control: { type: "ephemeral" } }],
  messages: [{ role: "user", content: userPrompt(t.idioma, t.nivel, t.unidad) }],
  output_config: { format: zodOutputFormat(UnidadSchema), effort: "medium" },
});

async function directo(client: Anthropic, tareas: Tarea[]) {
  let hechas = 0, fallos = 0, tokensIn = 0, tokensOut = 0;
  const cola = [...tareas];
  const worker = async () => {
    while (cola.length) {
      const t = cola.shift()!;
      try {
        if (PROVEEDOR === "gemini") {
          const g = await generarUnidadGemini(systemPrompt(), userPrompt(t.idioma, t.nivel, t.unidad), MODELO, process.env.GEMINI_API_KEY ?? "");
          guardar(t, g.json);
          tokensIn += g.entrada; tokensOut += g.salida; hechas++;
          console.log(`✓ ${idTarea(t)} (${hechas}/${tareas.length}) gemini`);
          continue;
        }
        const r = await client.messages.parse(paramsDe(t));
        if (r.stop_reason === "refusal") throw new Error(`refusal: ${r.stop_details?.explanation ?? ""}`);
        if (!r.parsed_output) throw new Error("respuesta sin JSON válido");
        guardar(t, r.parsed_output);
        tokensIn += r.usage.input_tokens + (r.usage.cache_read_input_tokens ?? 0);
        tokensOut += r.usage.output_tokens;
        hechas++;
        console.log(`✓ ${idTarea(t)} (${hechas}/${tareas.length}) cache=${r.usage.cache_read_input_tokens ?? 0}`);
      } catch (e) {
        fallos++;
        const msg = e instanceof Anthropic.APIError ? `API ${e.status}: ${e.message}` : String(e);
        console.error(`✗ ${idTarea(t)}: ${msg}`);
        fs.appendFileSync(path.join(DIR_ESTADO, "errores.log"), `${new Date().toISOString()} ${idTarea(t)} ${msg}\n`);
      }
    }
  };
  await Promise.all(Array.from({ length: CONCURRENCIA }, worker));
  console.log(`\nHechas ${hechas}, fallos ${fallos}. Tokens entrada ${tokensIn}, salida ${tokensOut}.`);
}

async function batch(client: Anthropic, tareas: Tarea[]) {
  const requests = tareas.map((t) => ({ custom_id: idTarea(t), params: paramsDe(t) }));
  const b = await client.messages.batches.create({ requests });
  const indice = Object.fromEntries(tareas.map((t) => [idTarea(t), { idioma: t.idioma, nivel: t.nivel.numero, unidad: t.unidad.numero }]));
  fs.writeFileSync(path.join(DIR_ESTADO, `batch-${b.id}.json`), JSON.stringify({ id: b.id, creado: b.created_at, modelo: MODELO, tareas: indice }, null, 2));
  console.log(`Batch ${b.id} enviado con ${requests.length} unidades. Recoge con:\n  npm run generar -- --recoger ${b.id}`);
}

async function recoger(client: Anthropic, id: string) {
  const estado = JSON.parse(fs.readFileSync(path.join(DIR_ESTADO, `batch-${id}.json`), "utf8"));
  const plan = cargarPlan();
  const b = await client.messages.batches.retrieve(id);
  if (b.processing_status !== "ended") {
    console.log(`Todavía en proceso: ${JSON.stringify(b.request_counts)}. Vuelve a intentarlo más tarde.`);
    return;
  }
  let ok = 0, err = 0;
  for await (const r of await client.messages.batches.results(id)) {
    const meta = estado.tareas[r.custom_id];
    const nivel = plan.niveles.find((n) => n.numero === meta.nivel)!;
    const t: Tarea = { idioma: meta.idioma, nivel, unidad: nivel.unidades.find((u) => u.numero === meta.unidad)! };
    if (r.result.type !== "succeeded") { err++; console.error(`✗ ${r.custom_id}: ${r.result.type}`); continue; }
    const texto = r.result.message.content.find((c) => c.type === "text");
    if (!texto || texto.type !== "text") { err++; continue; }
    try {
      guardar(t, JSON.parse(texto.text));
      ok++;
    } catch (e) {
      err++;
      console.error(`✗ ${r.custom_id}: JSON inválido (${String(e).slice(0, 80)})`);
    }
  }
  console.log(`Guardadas ${ok}, con error ${err}.`);
}

async function main() {
  if (A.recoger) {
    await recoger(new Anthropic(), String(A.recoger));
    return;
  }
  const tareas = tareasPendientes();
  console.log(`Unidades pendientes: ${tareas.length} · proveedor ${PROVEEDOR} · modelo ${MODELO}`);
  if (tareas.length === 0) return;
  // Estimación: ~1 900 tokens de entrada (sistema cacheado) y ~1 700 de salida por unidad.
  const precio: Record<string, [number, number]> = { "claude-opus-5": [5, 25], "claude-sonnet-5": [2, 10], "claude-haiku-4-5": [1, 5] };
  const [pi, po] = precio[MODELO] ?? [5, 25];
  const coste = (tareas.length * (1900 * pi + 1700 * po)) / 1e6;
  console.log(`Coste estimado: $${coste.toFixed(2)} directo · $${(coste / 2).toFixed(2)} con --batch (cache aparte).`);
  if (A["dry-run"]) return;
  if (PROVEEDOR === "gemini") {
    if (!process.env.GEMINI_API_KEY) throw new Error("Falta GEMINI_API_KEY (o pásalo en .env)");
    if (A.batch) console.log("Batches solo con Claude; se usa modo directo.");
    await directo(new Anthropic({ apiKey: "no-usada" }), tareas);
    return;
  }
  const client = new Anthropic();
  if (A.batch) await batch(client, tareas);
  else await directo(client, tareas);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
