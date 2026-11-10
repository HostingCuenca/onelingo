/** Prueba local del respaldo de voz: pide audio con ElevenLabs y cae a OpenAI si falla. */
import { obtenerAudio, obtenerAudioAlineado, obtenerAudioStream } from '../lib/voz.js';
import { elevenPausado } from '../lib/voz_respaldo.js';
const casos = [
  { texto: 'Nice! What would you like to talk about today?', idioma: 'en', voz: 'avatar_chloe' },
  { texto: '昨日、公園に行きました。', idioma: 'ja' },
  { texto: 'Como fue ayer, se dice went.', idioma: 'en', habla: 'es' },
];
for (const c of casos) {
  const t0 = Date.now();
  try {
    const a = await obtenerAudioAlineado(c as any, true);
    console.log(c.idioma, c.voz ?? '-', 'alineado', a.hash.slice(0, 8), a.buffer.length, 'B', a.alineacion ? 'con alineación' : 'sin alineación', Date.now() - t0, 'ms', 'pausado:', elevenPausado());
  } catch (e) { console.log('ERROR', c.texto, String(e).slice(0, 200)); }
}
const s = await obtenerAudioStream({ texto: 'Tell me, what did you do this weekend?', idioma: 'en', voz: 'avatar_chloe' }, AbortSignal.timeout(20000), () => console.log('primer audio'));
let n = 0; for await (const ch of s.stream) n += (ch as Buffer).length;
console.log('stream', s.hash.slice(0, 8), n, 'B');
const b = await obtenerAudio({ texto: 'Tell me, what did you do this weekend?', idioma: 'en', voz: 'avatar_chloe' });
console.log('repetido', b.hash === s.hash ? 'misma caché' : 'otra', b.cache);
process.exit(0);
