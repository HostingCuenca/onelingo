// Tiempo de cada letra (ElevenLabs «with-timestamps», vía /voz/alineada) →
// línea de tiempo de visemas de Oculus para mover la boca con las sílabas
// reales. Inglés, francés y alemán: módulos fonéticos de TalkingHead por
// palabra, repartidos en el tiempo real de la palabra. Español, portugués e
// italiano: reglas de lectura letra a letra. Ruso: letra a letra. Coreano,
// japonés y chino: por sílaba (vocal de la sílaba cuando se puede saber).
import {LipsyncEn} from './vendor/talkinghead/lipsync-en.mjs';
import {LipsyncFr} from './vendor/talkinghead/lipsync-fr.mjs';
import {LipsyncDe} from './vendor/talkinghead/lipsync-de.mjs';

const MODULOS = {en: new LipsyncEn(), fr: new LipsyncFr(), de: new LipsyncDe()};
const VOCAL = {a: 'aa', e: 'E', i: 'I', o: 'O', u: 'U'};
const LATINO = {b: 'PP', v: 'PP', m: 'PP', p: 'PP', f: 'FF', d: 'DD', t: 'DD', s: 'SS', z: 'SS', x: 'SS', ç: 'SS', n: 'nn', ñ: 'nn', l: 'nn', r: 'RR', j: 'kk', k: 'kk', w: 'U', y: 'I'};
const RUSO = {а: 'aa', я: 'aa', э: 'E', е: 'E', ё: 'O', и: 'I', ы: 'I', й: 'I', о: 'O', у: 'U', ю: 'U', б: 'PP', п: 'PP', м: 'PP', в: 'FF', ф: 'FF', д: 'DD', т: 'DD', н: 'nn', л: 'nn', р: 'RR', с: 'SS', з: 'SS', ц: 'SS', ш: 'CH', щ: 'CH', ж: 'CH', ч: 'CH', к: 'kk', г: 'kk', х: 'kk'};
// Vocal de cada sílaba hangul (índice de la vocal media, 21 posibles).
const VOCAL_KO = ['aa', 'aa', 'aa', 'E', 'O', 'E', 'O', 'E', 'O', 'aa', 'aa', 'E', 'O', 'U', 'O', 'E', 'U', 'U', 'U', 'I', 'I'];
const KANA = 'あかさたなはまやらわがざだばぱぁゃアカサタナハマヤラワガザダバパァャ|いきしちにひみりぎじぢびぴぃイキシチニヒミリギジヂビピィ|うくすつぬふむゆるぐずづぶぷぅゅっウクスツヌフムユルグズヅブプゥュッ|えけせてねへめれげぜでべぺぇエケセテネヘメレゲゼデベペェ|おこそとのほもよろをごぞどぼぽぉょオコソトノホモヨロヲゴゾドボポォョ'.split('|');
const vocalKana = c => { const i = KANA.findIndex(f => f.includes(c)); return i < 0 ? null : ['aa', 'I', 'U', 'E', 'O'][i]; };
const base = c => c === 'ñ' || c === 'ç' ? c : c.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

/** Visema de una letra/sílaba sola (sin contexto), o null si no se pronuncia. */
function visemaLetra(c, idioma) {
  if (idioma === 'ru') return RUSO[c.toLowerCase()] || null;
  if (idioma === 'ko') { const k = c.charCodeAt(0) - 0xAC00; return k >= 0 && k < 11172 ? VOCAL_KO[Math.floor((k % 588) / 28)] : null; }
  if (idioma === 'ja') { const v = vocalKana(c); if (v) return v; return /\p{Script=Han}/u.test(c) ? 'aa' : null; }
  if (idioma === 'zh') return /\p{Script=Han}/u.test(c) ? 'aa' : null;
  const b = base(c); return VOCAL[b] || LATINO[b] || null;
}

/** Línea de tiempo [{v, t, d}] en ms. `al` = {characters, character_start_times_seconds, character_end_times_seconds}. */
export function lineaDeVisemas(al, idioma) {
  if (!al?.characters?.length) return [];
  const ch = al.characters, ini = al.character_start_times_seconds, fin = al.character_end_times_seconds, out = [];
  const poner = (v, t, d) => {
    const ult = out[out.length - 1];
    if (ult && ult.v === v && t - (ult.t + ult.d) < 30) { ult.d = Math.max(ult.d, t + d - ult.t); return; }
    out.push({v, t: Math.round(t), d: Math.max(40, Math.round(d))});
  };
  const modulo = MODULOS[idioma];
  if (modulo) {
    // Por palabra: visemas del módulo, escalados al tiempo real de la palabra.
    let i = 0;
    while (i < ch.length) {
      if (/\s/.test(ch[i])) { i++; continue; }
      let j = i; while (j < ch.length && !/\s/.test(ch[j])) j++;
      const palabra = ch.slice(i, j).join(''), t0 = ini[i] * 1000, t1 = fin[j - 1] * 1000;
      const r = modulo.wordsToVisemes(modulo.preProcessText(palabra));
      const n = r?.visemes?.length || 0;
      if (n) {
        const total = r.times[n - 1] + r.durations[n - 1] || 1;
        for (let k = 0; k < n; k++) poner(r.visemes[k], t0 + r.times[k] / total * (t1 - t0), r.durations[k] / total * (t1 - t0));
      }
      i = j;
    }
    return out;
  }
  if (['es', 'pt', 'it'].includes(idioma)) {
    // Reglas de lectura (seseo latino): ch, qu/gu + e/i, c + e/i, ll, h muda.
    const b = ch.map(base);
    for (let i = 0; i < b.length; i++) {
      const c = b[i], s = b[i + 1] || '', s2 = b[i + 2] || '';
      const de = (k = i) => [ini[i] * 1000, (fin[k] - ini[i]) * 1000];
      if (VOCAL[c]) { poner(VOCAL[c], ...de()); continue; }
      if (c === 'h') continue;
      if (c === 'c') { if (s === 'h') { poner('CH', ...de(i + 1)); i++; } else poner(s && 'ei'.includes(s) ? 'SS' : 'kk', ...de()); continue; }
      if (c === 'q') { poner('kk', ...de(s === 'u' ? i + 1 : i)); if (s === 'u') i++; continue; }
      if (c === 'g') { if (s === 'u' && s2 && 'ei'.includes(s2)) { poner('kk', ...de(i + 1)); i++; } else poner('kk', ...de()); continue; }
      if (c === 'l' && s === 'l') { poner('I', ...de(i + 1)); i++; continue; }
      if (LATINO[c]) poner(LATINO[c], ...de());
    }
    return out;
  }
  // ru (letra a letra) y ko/ja/zh (por sílaba): una consonante breve al abrir
  // cada sílaba de CJK da el «abre y cierra» natural.
  for (let i = 0; i < ch.length; i++) {
    const v = visemaLetra(ch[i], idioma); if (!v) continue;
    const t = ini[i] * 1000, d = (fin[i] - ini[i]) * 1000;
    if (['ko', 'ja', 'zh'].includes(idioma) && d > 60) { poner('nn', t, d * 0.25); poner(v, t + d * 0.25, d * 0.75); }
    else poner(v, t, d);
  }
  return out;
}

/** Sin alineación (audio en caché de antes): reparte las letras a lo largo de la duración. */
export function alineacionEstimada(texto, duracionS) {
  const chars = [...texto], n = chars.length || 1, paso = duracionS / n;
  return {characters: chars, character_start_times_seconds: chars.map((_, i) => i * paso), character_end_times_seconds: chars.map((_, i) => (i + 1) * paso)};
}

/** Peso de cada visema en el instante `ms` (subida y bajada suaves de 60 ms). */
export function pesos(linea, ms) {
  const w = {};
  for (const x of linea) {
    if (ms < x.t - 60) break;
    if (ms > x.t + x.d + 60) continue;
    const nivel = x.v === 'PP' || x.v === 'FF' ? 0.9 : 0.65;
    const k = ms < x.t ? (ms - (x.t - 60)) / 60 : ms > x.t + x.d ? 1 - (ms - x.t - x.d) / 60 : 1;
    w[x.v] = Math.max(w[x.v] || 0, nivel * Math.max(0, Math.min(1, k)));
  }
  return w;
}
