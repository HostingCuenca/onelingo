/**
 * Voces de la clase bilingüe: cada tutor, con la voz nativa del alumno, lee una
 * frase de clase con el idioma meta dentro; se transcribe de vuelta con Scribe y
 * se mide cuánto se parece (CER) para ver si alguna voz pronuncia mal el idioma
 * meta. Deja los audios en la caché (la primera llamada ya los tiene).
 *   npx tsx src/herramientas/probar_voz_bilingue.ts [--nativos es,en] [--metas en,fr] [--tutores chloe,diego]
 */
import { config } from '../lib/config.js';
import { pool } from '../lib/db.js';
import { lenguaBase, obtenerAudio, rolDeVoz, VOCES } from '../lib/voz.js';

const arg = (n: string, d: string) => { const i = process.argv.indexOf(`--${n}`); return i > 0 ? process.argv[i + 1] : d; };
const TUTORES = arg('tutores', 'ana,elena,julia,chloe,nora,hana,lucas,tomas,frank,diego,erik,andre').split(',').map(t => `avatar_${t}`);
const MODELO: Record<string, string> = { en: 'I went to the park yesterday.', es: 'Ayer fui al parque.', fr: 'Hier, je suis allé au parc.', de: 'Gestern bin ich in den Park gegangen.', pt: 'Ontem eu fui ao parque.', it: 'Ieri sono andato al parco.', ja: 'きのう こうえんに いきました。', ko: '어제 공원에 갔어요.', zh: '我昨天去了公园。', ru: 'Вчера я ходил в парк.' };
const MARCO: Record<string, (f: string, M: string) => string> = {
  es: (f, M) => `¡Casi! Como fue ayer, en ${M} se dice: «${f}» A ver, dilo tú.`,
  en: (f, M) => `Almost! It was yesterday, so in ${M} we say: «${f}» Now you say it.`,
};
const NOMBRE: Record<string, Record<string, string>> = {
  es: { en: 'inglés', es: 'español', fr: 'francés', de: 'alemán', pt: 'portugués', it: 'italiano', ja: 'japonés', ko: 'coreano', zh: 'chino', ru: 'ruso' },
  en: { en: 'English', es: 'Spanish', fr: 'French', de: 'German', pt: 'Portuguese', it: 'Italian', ja: 'Japanese', ko: 'Korean', zh: 'Chinese', ru: 'Russian' },
};
const nativos = arg('nativos', 'es,en').split(',');
const plano = (t: string) => t.toLowerCase().normalize('NFKC').replace(/[^\p{L}\p{N}]/gu, '');
function cer(a: string, b: string) {
  const x = [...plano(a)], y = [...plano(b)], d = Array.from({ length: y.length + 1 }, (_, j) => j);
  for (let i = 1; i <= x.length; i++) { let prev = d[0]; d[0] = i; for (let j = 1; j <= y.length; j++) { const t = d[j]; d[j] = Math.min(d[j] + 1, d[j - 1] + 1, prev + (x[i - 1] === y[j - 1] ? 0 : 1)); prev = t; } }
  return d[y.length] / Math.max(1, x.length);
}
async function transcribir(buf: Buffer) {
  const fd = new FormData(); fd.append('model_id', 'scribe_v1'); fd.append('file', new Blob([new Uint8Array(buf)], { type: 'audio/mpeg' }), 'a.mp3');
  const r = await fetch('https://api.elevenlabs.io/v1/speech-to-text', { method: 'POST', headers: { 'xi-api-key': config.elevenApiKey }, body: fd });
  return r.ok ? String(((await r.json()) as { text: string }).text) : `STT ${r.status}`;
}
const filas: { nativo: string; meta: string; tutor: string; voz: string; cer: number; respaldo: boolean; oido: string }[] = [];
for (const nativo of nativos) {
  const metas = arg('metas', Object.keys(MODELO).join(',')).split(',').filter(m => m !== nativo);
  for (const meta of metas) for (const tutor of TUTORES) {
    const habla = `${nativo}+${meta}`, frase = MODELO[meta];
    const texto = (MARCO[nativo] ?? MARCO.es)(frase, (NOMBRE[nativo] ?? NOMBRE.es)[meta]);
    const voz = rolDeVoz(tutor, lenguaBase(habla));
    try {
      const a = await obtenerAudio({ texto, idioma: meta, voz: tutor, habla });
      const oido = await transcribir(a.buffer);
      // Lo que importa es la frase del idioma meta: se busca dentro de lo oído.
      filas.push({ nativo, meta, tutor: tutor.replace('avatar_', ''), voz: VOCES[voz]?.nombre ?? voz, cer: Math.round(cer(texto, oido) * 100) / 100, respaldo: !!a.respaldo, oido });
    } catch (e) { filas.push({ nativo, meta, tutor, voz, cer: 1, respaldo: false, oido: String(e).slice(0, 80) }); }
  }
}
console.table(filas.map(({ oido, ...f }) => f));
const malas = filas.filter(f => f.cer > 0.15);
console.log(`${filas.length} audios · CER medio ${Math.round(filas.reduce((a, f) => a + f.cer, 0) / filas.length * 100) / 100} · ${malas.length} por revisar (CER > 0,15)`);
for (const f of malas) console.log(`  ${f.nativo}+${f.meta} ${f.tutor} (${f.voz}) CER ${f.cer}: ${f.oido}`);
await pool.end();
