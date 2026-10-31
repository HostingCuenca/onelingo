/**
 * Tablas del informe a partir de los resultados de evaluar.mts (Markdown por la salida estándar).
 *
 *   cd backend && npx tsx ../tools/pruebas/eval_tutor/resumir.mts ../tools/pruebas/eval_tutor/resultados/gpt-4.1-mini.json [otro.json…] [--peores 8] [--detalle]
 */
import { readFileSync } from 'node:fs';
import { basename } from 'node:path';

const args = process.argv.slice(2);
const opt = (n: string) => { const i = args.indexOf(`--${n}`); return i >= 0 ? args[i + 1] : undefined; };
const archivos = args.filter((a, i) => a.endsWith('.json') && !args[i - 1]?.startsWith('--'));
const PEORES = Number(opt('peores') ?? 8);
const CRIT = ['a_errores', 'b_correccion', 'c_movimiento', 'd_nivel', 'e_humano', 'f_idioma', 'tarjeta'] as const;
const CATS = ['error_claro', 'correcta', 'error_menor', 'repite_bien', 'vuelve_a_fallar', 'error_repetido', 'autocorreccion', 'por_que', 'como_se_dice', 'bloqueo', 'monosilabos', 'nivel_alto'];

const PRECIOS: Record<string, [number, number, number]> = { 'gpt-5.6-luna': [0.2, 0.02, 1.2], 'gpt-5.4-mini': [0.75, 0.075, 4.5], 'gpt-4.1-mini': [0.4, 0.1, 1.6] };
const usd = (m: string, ent: number, cache: number, sal: number) => { const p = PRECIOS[m] ?? [0, 0, 0]; return ((ent - cache) * p[0] + cache * p[1] + sal * p[2]) / 1e6; };
const pct = (xs: number[], p: number) => { if (!xs.length) return NaN; const s = [...xs].sort((a, b) => a - b); return s[Math.min(s.length - 1, Math.ceil((p / 100) * s.length) - 1)]; };
const media = (xs: number[]) => xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : NaN;
const f0 = (x: number) => Number.isFinite(x) ? Math.round(x).toString() : '—';
const f2 = (x: number) => Number.isFinite(x) ? x.toFixed(2) : '—';
const porc = (x: number) => Number.isFinite(x) ? `${Math.round(x * 100)} %` : '—';

const runs = archivos.map(f => { const j = JSON.parse(readFileSync(f, 'utf8')); return { nombre: basename(f, '.json'), ...j }; });
const tasa = (cs: any[], k: string) => { const ap = cs.filter(c => c.juicio?.[k]?.aplica); return ap.length ? ap.filter(c => c.juicio[k].cumple).length / ap.length : NaN; };

console.log('### Resumen por modelo\n');
console.log(`| Modelo | Nota media (1-5) | ${CRIT.join(' | ')} | 1.ª frase p50/p90 (ms) | fin tutor p50/p90 | total p50/p90 | US$ tutor/turno (sin caché) | tokens entrada/salida (razon.) · % entrada en caché | fallos |`);
console.log(`|${'---|'.repeat(CRIT.length + 8)}`);
for (const r of runs) {
  const cs = r.casos.filter((c: any) => c.juicio);
  const ok = r.casos.filter((c: any) => !c.error);
  const ms = (k: string) => ok.map((c: any) => c.ms?.[k]).filter((x: any) => typeof x === 'number');
  const tk = (k: string) => media(ok.map((c: any) => c.tokens?.tutor?.[k] ?? 0));
  console.log(`| ${r.nombre} | ${f2(media(cs.map((c: any) => c.juicio.nota)))} | ${CRIT.map(k => porc(tasa(cs, k))).join(' | ')} | ${f0(pct(ms('primeraFrase'), 50))} / ${f0(pct(ms('primeraFrase'), 90))} | ${f0(pct(ms('tutorFin'), 50))} / ${f0(pct(ms('tutorFin'), 90))} | ${f0(pct(ms('total'), 50))} / ${f0(pct(ms('total'), 90))} | ${media(ok.map((c: any) => c.usd?.tutor ?? 0)).toFixed(5)} (${media(ok.map((c: any) => { const t = c.tokens.tutor; return usd(r.meta.modelo, t.entrada, 0, t.salida); })).toFixed(5)}) | ${f0(tk('entrada'))} / ${f0(tk('salida'))} (${f0(tk('razonamiento'))}) · ${porc(tk('cacheados') / tk('entrada'))} | ${r.casos.filter((c: any) => c.error).length} err, ${r.casos.filter((c: any) => c.reintento).length} reint. |`);
}

// Corrector: latencias reales (no en caché) de todas las ejecuciones, una por entrada.
const corr = new Map<string, any>();
for (const r of runs) for (const c of r.casos) if (c.ms?.corrector != null && !corr.has(c.id)) corr.set(c.id, c);
const msC = [...corr.values()].map(c => c.ms.corrector);
console.log(`\n### Corrector (corregirUltimo, ${process.env.OPENAI_MODELO_CORRECTOR ?? 'gpt-5.6-luna'})\n`);
console.log(`n=${msC.length} · p50 ${f0(pct(msC, 50))} ms · p90 ${f0(pct(msC, 90))} ms · máx ${f0(Math.max(...msC))} ms · US$/turno ${media([...corr.values()].map(c => c.usd?.corrector ?? 0)).toFixed(5)}`);

console.log('\n### Nota media y movimiento pedagógico (c) por categoría\n');
console.log(`| Categoría (n) | ${runs.map(r => `${r.nombre} nota · c`).join(' | ')} |`);
console.log(`|---|${runs.map(() => '---|').join('')}`);
for (const cat of CATS) {
  const n = runs[0].casos.filter((c: any) => c.categoria === cat).length;
  console.log(`| ${cat} (${n}) | ${runs.map(r => { const cs = r.casos.filter((c: any) => c.categoria === cat && c.juicio); return `${f2(media(cs.map((c: any) => c.juicio.nota)))} · ${porc(tasa(cs, 'c_movimiento'))}`; }).join(' | ')} |`);
}

console.log('\n### Por nivel\n');
console.log(`| Nivel | ${runs.map(r => r.nombre).join(' | ')} |`);
console.log(`|---|${runs.map(() => '---|').join('')}`);
for (const n of [1, 3, 6]) console.log(`| ${n} | ${runs.map(r => f2(media(r.casos.filter((c: any) => c.nivel === n && c.juicio).map((c: any) => c.juicio.nota)))).join(' | ')} |`);

for (const r of runs) {
  const cs = r.casos.filter((c: any) => c.juicio);
  const fallidos = (c: any) => CRIT.filter(k => c.juicio[k].aplica && !c.juicio[k].cumple).length;
  const peores = [...cs].sort((a, b) => a.juicio.nota - b.juicio.nota || fallidos(b) - fallidos(a)).slice(0, PEORES);
  console.log(`\n### ${PEORES} peores casos · ${r.nombre}\n`);
  for (const c of peores) console.log(`- **${c.id}** (${c.categoria}, ${c.idiomaMeta} N${c.nivel}) nota ${c.juicio.nota}, falla ${CRIT.filter(k => c.juicio[k].aplica && !c.juicio[k].cumple).join(', ') || '—'}: «${c.reply}» — ${c.juicio.resumen}`);
  if (args.includes('--detalle')) {
    console.log(`\n#### Fallos por criterio · ${r.nombre}\n`);
    for (const k of CRIT) for (const c of cs) if (c.juicio[k].aplica && !c.juicio[k].cumple) console.log(`- ${k} · ${c.id}: ${c.juicio[k].motivo}`);
  }
}
