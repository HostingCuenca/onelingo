/**
 * Consumo de créditos de ElevenLabs por día y por producto (TTS, transcripción…),
 * según la propia API de ElevenLabs. Solo lectura.
 *   npx tsx src/herramientas/consumo_eleven.ts [días=35] [desglose=product_type|model|voice|api_keys]
 */
import { config } from '../lib/config.js';

const dias = Number(process.argv[2] ?? 35), desglose = process.argv[3] ?? 'product_type';
const h = { 'xi-api-key': config.elevenApiKey };
const sub: any = await (await fetch('https://api.elevenlabs.io/v1/user/subscription', { headers: h })).json();
console.log(`plan ${sub.tier} · usados ${sub.character_count} de ${sub.character_limit} · renueva ${new Date(sub.next_character_count_reset_unix * 1000).toISOString().slice(0, 10)}`);
const fin = Date.now(), inicio = fin - dias * 864e5;
const u = new URL('https://api.elevenlabs.io/v1/usage/character-stats');
u.search = new URLSearchParams({ start_unix: String(inicio), end_unix: String(fin), breakdown_type: desglose, aggregation_interval: 'day', ...(['api_keys', 'all_api_keys', 'user', 'resource'].includes(desglose) ? { include_workspace_metrics: 'true' } : {}) }).toString();
const r = await fetch(u, { headers: h });
const j: any = await r.json();
if (!r.ok) { console.log(r.status, JSON.stringify(j).slice(0, 300)); process.exit(1); }
const filas: Record<string, Record<string, number>> = {};
const totales: Record<string, number> = {};
j.time.forEach((t: number, i: number) => {
  const dia = new Date(t).toISOString().slice(5, 10);
  for (const [k, serie] of Object.entries(j.usage as Record<string, number[]>)) {
    const v = Math.round(serie[i] ?? 0);
    if (!v) continue;
    (filas[dia] ??= {})[k] = v;
    totales[k] = (totales[k] ?? 0) + v;
  }
});
console.table(filas);
console.log('totales:', totales);
