/**
 * Letras con tiempo (ElevenLabs «with-timestamps») → visemas de Oculus para
 * TalkingHead. Reglas de lectura del español (seseo latino); sirve también,
 * aproximado, para portugués e italiano. Cada visema dura lo que ElevenLabs
 * dice que duran sus letras, así la boca va con las sílabas reales.
 */
const VOCAL = { a: 'aa', e: 'E', i: 'I', o: 'O', u: 'U' };
const CONS = { b: 'PP', v: 'PP', m: 'PP', p: 'PP', f: 'FF', d: 'DD', t: 'DD', s: 'SS', z: 'SS', x: 'SS', n: 'nn', ñ: 'nn', l: 'nn', r: 'RR', j: 'kk', k: 'kk', w: 'U', y: 'I' };
const base = (c) => c === 'ñ' ? c : c.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

export function visemasLatinos(al) {
  const ch = al.characters.map(base), ini = al.character_start_times_seconds, fin = al.character_end_times_seconds;
  const out = { visemes: [], vtimes: [], vdurations: [] };
  const poner = (v, i, j = i) => {
    const t = ini[i] * 1000, d = Math.max(40, (fin[j] - ini[i]) * 1000), n = out.visemes.length - 1;
    if (n >= 0 && out.visemes[n] === v && t - (out.vtimes[n] + out.vdurations[n]) < 30) { out.vdurations[n] = t + d - out.vtimes[n]; return; }
    out.visemes.push(v); out.vtimes.push(Math.round(t)); out.vdurations.push(Math.round(d));
  };
  for (let i = 0; i < ch.length; i++) {
    const c = ch[i], s = ch[i + 1] ?? '', s2 = ch[i + 2] ?? '';
    if (VOCAL[c]) { poner(VOCAL[c], i); continue; }
    if (c === 'h') continue; // muda
    if (c === 'c') { if (s === 'h') { poner('CH', i, i + 1); i++; } else poner('ei'.includes(s) && s ? 'SS' : 'kk', i); continue; }
    if (c === 'q') { poner('kk', i, s === 'u' ? i + 1 : i); if (s === 'u') i++; continue; }
    if (c === 'g') { if (s === 'u' && 'ei'.includes(s2) && s2) { poner('kk', i, i + 1); i++; } else poner('kk', i); continue; }
    if (c === 'l' && s === 'l') { poner('I', i, i + 1); i++; continue; }
    if (CONS[c]) poner(CONS[c], i);
  }
  return out;
}

/** Palabras con su inicio y duración (ms), para el lip-sync propio de TalkingHead (en, fr, de). */
export function palabras(al) {
  const r = { words: [], wtimes: [], wdurations: [] }; let actual = '', t0 = 0, t1 = 0;
  const cerrar = () => { if (actual.trim()) { r.words.push(actual.trim()); r.wtimes.push(Math.round(t0 * 1000)); r.wdurations.push(Math.round((t1 - t0) * 1000)); } actual = ''; };
  al.characters.forEach((c, i) => {
    if (/\s/.test(c)) { cerrar(); return; }
    if (!actual) t0 = al.character_start_times_seconds[i];
    actual += c; t1 = al.character_end_times_seconds[i];
  });
  cerrar();
  return r;
}
