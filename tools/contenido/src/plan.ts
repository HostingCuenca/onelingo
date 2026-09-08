/** Muestra el plan curricular (niveles, MCER y temas) para revisión. */
import { cargarPlan } from "./prompt.js";
const plan = cargarPlan();
for (const n of plan.niveles) {
  console.log(`\nNivel ${n.numero} · ${n.nombre} · MCER ${n.cefr} · ~${n.horas_aprox} h · ${n.vocabulario_acumulado} palabras`);
  console.log(`  Gramática: ${n.gramatica}`);
  console.log(`  Unidades: ${n.unidades.map((u) => `${u.numero}. ${u.tema}`).join(" · ")}`);
}
