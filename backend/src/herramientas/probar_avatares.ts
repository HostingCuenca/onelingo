/**
 * Prueba de los tutores de la videollamada: una llamada simulada por avatar
 * (idiomas, niveles y modo de explicación distintos) con el prompt y el
 * `responder` reales, la voz real de las primeras respuestas (¿ElevenLabs o
 * respaldo?, ¿qué voz?) y la misma evaluación pedagógica que se guarda de las
 * llamadas reales. Escribe un informe en docs/claude-educacion/pruebas-tutor/
 * y, con --guardar, los informes en la base LOCAL (alumno de pruebas).
 *
 *   npx tsx src/herramientas/probar_avatares.ts [--avatares chloe,andre] [--turnos 6] [--frases-voz 2] [--guardar]
 */
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { responder, type Turno } from '../lib/ia.js';
import { generarJsonOpenAI } from '../lib/ia_openai.js';
import { evaluarLlamada, CRITERIOS, type Evaluacion } from '../lib/informe_llamada.js';
import { separadorDeLenguas, sinCorchetes } from '../lib/explicaciones.js';
import { obtenerAudioAlineado, rolDeVoz, VOCES } from '../lib/voz.js';
import { config } from '../lib/config.js';
import { query, uno } from '../lib/db.js';

const arg = (n: string, d: string) => { const i = process.argv.indexOf(`--${n}`); return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };
const TURNOS = Number(arg('turnos', '6'));
const FRASES_VOZ = Number(arg('frases-voz', '2'));
const GUARDAR = process.argv.includes('--guardar');

type Caso = { avatar: string; idioma: string; nativo: string; nivel: number; explica: 'nativo' | 'meta'; alumno: string };
const PERSONA: Record<string, string> = {
  bajo: 'Empiezas desde cero: entiendes muy poco. Respondes con 1 a 4 palabras, con errores, y a veces dices en tu idioma que no entiendes o preguntas qué significa algo.',
  medio: 'Tienes nivel básico: frases cortas y sencillas con errores típicos (tiempos verbales, artículos, orden). A veces preguntas en tu idioma cómo se dice algo.',
  alto: 'Tienes nivel intermedio: frases completas con algún error. Cuentas cosas de tu vida y a veces te desvías del tema.',
};
const persona = (n: number) => PERSONA[n <= 2 ? 'bajo' : n <= 4 ? 'medio' : 'alto'];
const CASOS: Caso[] = [
  { avatar: 'avatar_chloe', idioma: 'en', nativo: 'es', nivel: 1, explica: 'nativo', alumno: persona(1) },
  { avatar: 'avatar_andre', idioma: 'en', nativo: 'es', nivel: 3, explica: 'meta', alumno: persona(3) },
  { avatar: 'avatar_frank', idioma: 'en', nativo: 'es', nivel: 6, explica: 'meta', alumno: persona(6) },
  { avatar: 'avatar_julia', idioma: 'fr', nativo: 'es', nivel: 2, explica: 'nativo', alumno: persona(2) },
  { avatar: 'avatar_erik', idioma: 'de', nativo: 'es', nivel: 4, explica: 'meta', alumno: persona(4) },
  { avatar: 'avatar_nora', idioma: 'pt', nativo: 'es', nivel: 3, explica: 'nativo', alumno: persona(3) },
  { avatar: 'avatar_tomas', idioma: 'it', nativo: 'es', nivel: 2, explica: 'nativo', alumno: persona(2) },
  { avatar: 'avatar_hana', idioma: 'ja', nativo: 'es', nivel: 1, explica: 'nativo', alumno: persona(1) },
  { avatar: 'avatar_lucas', idioma: 'ko', nativo: 'es', nivel: 2, explica: 'nativo', alumno: persona(2) },
  { avatar: 'avatar_ana', idioma: 'zh', nativo: 'es', nivel: 3, explica: 'meta', alumno: persona(3) },
  { avatar: 'avatar_diego', idioma: 'ru', nativo: 'es', nivel: 2, explica: 'nativo', alumno: persona(2) },
  { avatar: 'avatar_elena', idioma: 'es', nativo: 'en', nivel: 3, explica: 'nativo', alumno: persona(3) },
];
const IDIOMA_ALUMNO: Record<string, string> = { es: 'español', en: 'inglés' };

async function hablaAlumno(c: Caso, historial: Turno[]) {
  const msgs = historial.map(t => ({ role: (t.rol === 'tutor' ? 'user' : 'assistant') as 'user' | 'assistant', content: t.texto }));
  const r = await generarJsonOpenAI(`Haces de alumno adulto en una videollamada para aprender (${c.idioma}). Tu idioma es el ${IDIOMA_ALUMNO[c.nativo]}. ${c.alumno}
Responde SOLO lo que dirías en voz alta, una o dos frases, sin comillas.`, msgs, { type: 'object', additionalProperties: false, properties: { texto: { type: 'string' } }, required: ['texto'] }, config.openaiModelo);
  return String(r.json.texto);
}

type Voz = { texto: string; habla: string; vozClave: string; vozNombre: string; respaldo: boolean; ms: number; error?: string };
async function vozDe(c: Caso, reply: string): Promise<Voz[]> {
  const partes = c.explica === 'nativo' ? separadorDeLenguas(c.idioma)(reply) : [{ texto: sinCorchetes(reply), nativo: false }];
  const out: Voz[] = [];
  for (const p of partes) {
    const habla = p.nativo ? c.nativo : '';
    const clave = rolDeVoz(c.avatar, c.idioma), t0 = Date.now();
    try {
      const a = await obtenerAudioAlineado({ texto: p.texto, idioma: c.idioma, voz: c.avatar, habla: habla || undefined }, true);
      out.push({ texto: p.texto, habla, vozClave: clave, vozNombre: VOCES[clave]?.nombre ?? '?', respaldo: !!a.respaldo, ms: Date.now() - t0 });
    } catch (e) { out.push({ texto: p.texto, habla, vozClave: clave, vozNombre: VOCES[clave]?.nombre ?? '?', respaldo: false, ms: Date.now() - t0, error: String(e).slice(0, 120) }); }
  }
  return out;
}

type Resultado = { caso: Caso; transcripcion: { rol: 'tutor' | 'alumno' | 'aviso'; texto: string }[]; voces: Voz[]; evaluacion: Evaluacion | null; error?: string };
async function llamada(c: Caso): Promise<Resultado> {
  const historial: Turno[] = [], transcripcion: Resultado['transcripcion'] = [], voces: Voz[] = [];
  const tutor = async (aviso?: 'iniciativa') => {
    const r = await responder({ idiomaMeta: c.idioma, idiomaNativo: c.nativo, nivel: c.nivel, tutorId: c.avatar, explica: c.explica, historial: [...historial], aviso } as any);
    historial.push({ rol: 'tutor', texto: r.respuesta.reply }); transcripcion.push({ rol: 'tutor', texto: r.respuesta.reply });
    if (voces.filter(v => !v.habla).length < FRASES_VOZ * 2 && transcripcion.filter(t => t.rol === 'tutor').length <= FRASES_VOZ) voces.push(...await vozDe(c, r.respuesta.reply));
  };
  try {
    await tutor();
    for (let i = 0; i < TURNOS; i++) {
      // A mitad de la llamada, el alumno se queda callado: el tutor toma la iniciativa.
      if (i === Math.floor(TURNOS / 2)) { transcripcion.push({ rol: 'aviso', texto: 'iniciativa' }); await tutor('iniciativa'); }
      const a = await hablaAlumno(c, historial);
      historial.push({ rol: 'alumno', texto: a }); transcripcion.push({ rol: 'alumno', texto: a });
      await tutor();
    }
    const evaluacion = await evaluarLlamada({ idiomaMeta: c.idioma, idiomaNativo: c.nativo, nivel: c.nivel, explica: c.explica, historial: transcripcion as any });
    return { caso: c, transcripcion, voces, evaluacion };
  } catch (e) { return { caso: c, transcripcion, voces, evaluacion: null, error: String(e).slice(0, 300) }; }
}

async function enParalelo<T, R>(xs: T[], n: number, f: (x: T) => Promise<R>) {
  const out: R[] = new Array(xs.length); let i = 0;
  await Promise.all(Array.from({ length: n }, async () => { while (i < xs.length) { const k = i++; out[k] = await f(xs[k]); console.log(`  listo ${k + 1}/${xs.length}`); } }));
  return out;
}

const elegidos = arg('avatares', '').split(',').filter(Boolean).map(a => a.startsWith('avatar_') ? a : `avatar_${a}`);
const casos = elegidos.length ? CASOS.filter(c => elegidos.includes(c.avatar)) : CASOS;
console.log(`${casos.length} llamadas simuladas · ${TURNOS} turnos · voz en las ${FRASES_VOZ} primeras respuestas`);
const resultados = await enParalelo(casos, 4, llamada);

const fecha = new Date().toISOString().slice(0, 10) + (arg('sufijo', '') ? `-${arg('sufijo', '')}` : '');
const nombre = (a: string) => a.replace('avatar_', '').replace(/^./, m => m.toUpperCase());
const media = (xs: number[]) => xs.length ? Math.round(xs.reduce((a, b) => a + b, 0) / xs.length * 10) / 10 : 0;
const ev = resultados.filter(r => r.evaluacion);
const criterios = Object.keys(CRITERIOS) as (keyof typeof CRITERIOS)[];
const md: string[] = [
  `# Prueba de los tutores de la videollamada · ${fecha}`, '',
  `${resultados.length} llamadas simuladas (alumno de IA, ${TURNOS} turnos, un silencio a mitad de llamada), prompt y \`responder\` reales, voz real en las ${FRASES_VOZ} primeras respuestas y evaluación con la rúbrica de \`lib/informe_llamada.ts\` (la misma de las llamadas reales).`, '',
  `**Nota media:** ${media(ev.map(r => r.evaluacion!.nota))}/10 · ${criterios.map(c => `${c} ${media(ev.map(r => r.evaluacion!.puntos[c]))}`).join(' · ')} (de 1 a 5).`, '',
  '| Tutor | Idioma | Nivel | Explica | Nota | ' + criterios.join(' | ') + ' | Voz | Respaldo |',
  '|---|---|---|---|---|' + criterios.map(() => '---').join('|') + '|---|---|',
  ...resultados.map(r => {
    const e = r.evaluacion, v = r.voces.filter(x => !x.habla);
    return `| ${nombre(r.caso.avatar)} | ${r.caso.idioma} | N${r.caso.nivel} | ${r.caso.explica} | ${e ? e.nota : 'error'} | ${criterios.map(c => e?.puntos[c] ?? '–').join(' | ')} | ${v[0]?.vozNombre ?? '?'} | ${r.voces.filter(x => x.respaldo).length}/${r.voces.length} |`;
  }), '',
];
const vocesPorIdioma = new Map<string, string[]>();
for (const r of resultados) { const v = r.voces.find(x => !x.habla); if (v) vocesPorIdioma.set(r.caso.idioma, [...(vocesPorIdioma.get(r.caso.idioma) ?? []), v.vozClave]); }
md.push(`**Voces:** ${resultados.reduce((a, r) => a + r.voces.length, 0)} frases sintetizadas, ${resultados.reduce((a, r) => a + r.voces.filter(x => x.respaldo).length, 0)} con la voz de respaldo, ${resultados.reduce((a, r) => a + r.voces.filter(x => x.error).length, 0)} con error. Latencia media ${media(resultados.flatMap(r => r.voces.map(x => x.ms)))} ms.`, '');
for (const r of resultados) {
  const e = r.evaluacion;
  md.push(`## ${nombre(r.caso.avatar)} · ${r.caso.idioma} N${r.caso.nivel} · explica ${r.caso.explica}${e ? ` · ${e.nota}/10` : ''}`, '');
  if (r.error) md.push(`**Error:** ${r.error}`, '');
  if (e) {
    if (e.bien.length) md.push('**Bien:** ' + e.bien.join(' · '), '');
    if (e.problemas.length) md.push('**Problemas:**', ...e.problemas.map(p => `- (${p.criterio}) «${p.cita}» → ${p.mejor}`), '');
    md.push(`**Alumno:** ${e.alumno.nivelReal}${e.alumno.dificultades.length ? ` Dificultades: ${e.alumno.dificultades.join('; ')}.` : ''}`, '', `**Recomendación:** ${e.recomendacion}`, '');
  }
  const v = r.voces.filter(x => !x.habla)[0];
  if (v) md.push(`**Voz:** ${v.vozNombre} (\`${v.vozClave}\`)${r.voces.some(x => x.respaldo) ? ' · con frases de respaldo' : ' · todo ElevenLabs'}${r.voces.some(x => x.error) ? ` · errores: ${r.voces.filter(x => x.error).map(x => x.error).join('; ')}` : ''}`, '');
  md.push('<details><summary>Transcripción</summary>', '', ...r.transcripcion.map(t => t.rol === 'aviso' ? `- *(silencio: ${t.texto})*` : `- **${t.rol === 'tutor' ? 'T' : 'A'}:** ${t.texto}`), '', '</details>', '');
}
const dir = path.resolve('..', 'docs', 'claude-educacion', 'pruebas-tutor');
await mkdir(dir, { recursive: true });
await writeFile(path.join(dir, `${fecha}.md`), md.join('\n'));
await writeFile(path.join(dir, `${fecha}.json`), JSON.stringify(resultados, null, 1));
console.log(`informe: docs/claude-educacion/pruebas-tutor/${fecha}.md`);
console.log(`nota media ${media(ev.map(r => r.evaluacion!.nota))}`);
for (const r of resultados) console.log(nombre(r.caso.avatar), r.caso.idioma, `N${r.caso.nivel}`, r.evaluacion?.nota ?? r.error, r.voces.filter(x => !x.habla)[0]?.vozClave, `respaldo ${r.voces.filter(x => x.respaldo).length}/${r.voces.length}`);

if (GUARDAR) {
  if (/onelingo\.org|179\.197/.test(config.databaseUrl)) throw new Error('--guardar es solo para la base local');
  const u = await uno<{ id: string }>(`INSERT INTO usuarios (email, nombre, apellido, idioma_nativo, idioma_meta, es_demo) VALUES ('pruebas-tutor@onelingo.demo', 'Pruebas', 'Tutor', 'es', 'en', true)
    ON CONFLICT (email) DO UPDATE SET nombre = EXCLUDED.nombre RETURNING id`);
  for (const r of resultados) await query(`INSERT INTO informes_llamada (usuario_id, idioma, nivel, tutor_id, explica, turnos, evaluacion, tecnico, nota) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)`,
    [u!.id, r.caso.idioma, r.caso.nivel, r.caso.avatar, r.caso.explica, r.transcripcion.filter(t => t.rol === 'alumno').length, r.evaluacion, { frasesTutor: r.voces.length, frasesRespaldo: r.voces.filter(x => x.respaldo).length, prueba: true }, r.evaluacion?.nota ?? null]);
  console.log('informes guardados en la base local (alumno pruebas-tutor@onelingo.demo)');
}
process.exit(0);
