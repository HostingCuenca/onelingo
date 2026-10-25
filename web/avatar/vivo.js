// Llamada en vivo: micrófono abierto transcrito en tiempo real por ElevenLabs
// (Scribe v2 Realtime) directamente desde el navegador, con un token de un solo
// uso que da el servidor (la clave nunca llega aquí). El servidor de
// ElevenLabs decide cuándo terminaste de hablar (VAD) y manda el texto final;
// mientras hablas llegan textos parciales (sirven para interrumpir al tutor).
//
// Audio: PCM 16 kHz mono en trozos de 100 ms desde un AudioWorklet.

const TROZO = 1600; // 100 ms a 16 kHz
const WORKLET = `class Captura extends AudioWorkletProcessor {
  constructor() { super(); this.buf = new Float32Array(${TROZO}); this.n = 0; }
  process(entradas) {
    const c = entradas[0] && entradas[0][0]; if (!c) return true;
    for (let i = 0; i < c.length; i++) { this.buf[this.n++] = c[i]; if (this.n === ${TROZO}) { this.port.postMessage(this.buf.slice()); this.n = 0; } }
    return true;
  }
}
registerProcessor('captura-16k', Captura);`;

function aBase64(f32) {
  const b = new Uint8Array(f32.length * 2), v = new DataView(b.buffer);
  for (let i = 0; i < f32.length; i++) { const s = Math.max(-1, Math.min(1, f32[i])); v.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true); }
  let txt = ''; for (let i = 0; i < b.length; i += 0x8000) txt += String.fromCharCode(...b.subarray(i, i + 0x8000));
  return btoa(txt);
}

export const vivoDisponible = () => !!(window.AudioWorkletNode && window.WebSocket && navigator.mediaDevices?.getUserMedia);

/**
 * Abre micrófono + transcripción. `pedirToken()` → {token, url, modelo}.
 * Eventos: onParcial(texto), onFinal(texto), onEstado('escuchando'|'cerrado'|'error', detalle).
 */
export async function abrirEscucha({pedirToken, idioma, onParcial, onFinal, onEstado}) {
  let cerrado = false, silenciado = false, ws = null, ctx = null, stream = null, nodo = null, reintentos = 0;
  stream = await navigator.mediaDevices.getUserMedia({audio: {echoCancellation: true, noiseSuppression: true, autoGainControl: true, channelCount: 1}});
  // Si algo falla antes de devolver el control (token 429/503, worklet), se
  // suelta el micrófono: si no, quedaba encendido el resto de la llamada.
  const soltar = () => { cerrado = true; try { ws?.close(); } catch {} stream?.getTracks().forEach(t => t.stop()); try { nodo?.disconnect(); } catch {} ctx?.close().catch(() => {}); };
  try {
  ctx = new AudioContext({sampleRate: 16000});
  const url = URL.createObjectURL(new Blob([WORKLET], {type: 'text/javascript'}));
  await ctx.audioWorklet.addModule(url); URL.revokeObjectURL(url);
  nodo = new AudioWorkletNode(ctx, 'captura-16k');
  ctx.createMediaStreamSource(stream).connect(nodo);
  // El nodo no suena: se conecta a un destino mudo para que el navegador lo procese.
  const mudo = ctx.createGain(); mudo.gain.value = 0; nodo.connect(mudo).connect(ctx.destination);
  nodo.port.onmessage = e => {
    if (cerrado || !ws || ws.readyState !== 1) return;
    const datos = silenciado ? new Float32Array(TROZO) : e.data; // silenciado: se manda silencio (la sesión sigue viva)
    ws.send(JSON.stringify({message_type: 'input_audio_chunk', audio_base_64: aBase64(datos), commit: false, sample_rate: 16000}));
  };

  async function conectar() {
    const t = await pedirToken();
    if (cerrado) return;
    const q = new URLSearchParams({model_id: t.modelo || 'scribe_v2_realtime', token: t.token, audio_format: 'pcm_16000', commit_strategy: 'vad',
      vad_silence_threshold_secs: '0.8', min_speech_duration_ms: '250', ...(idioma ? {language_code: idioma} : {})});
    ws = new WebSocket(`${t.url}?${q}`);
    ws.onopen = () => { reintentos = 0; onEstado?.('escuchando'); };
    ws.onmessage = e => {
      let m; try { m = JSON.parse(e.data); } catch { return; }
      if (m.message_type === 'partial_transcript') onParcial?.(m.text || '');
      else if (m.message_type === 'committed_transcript' || m.message_type === 'committed_transcript_with_timestamps') { if ((m.text || '').trim()) onFinal?.(m.text.trim()); }
      else if (m.error) onEstado?.('error', `${m.message_type}: ${m.error}`);
    };
    ws.onclose = () => {
      if (cerrado) return;
      // La sesión se corta (límite de tiempo, red): se reabre con otro token.
      if (reintentos++ < 3) { onEstado?.('reconectando'); setTimeout(() => conectar().catch(err => onEstado?.('error', String(err?.message || err))), 600 * reintentos); }
      else onEstado?.('error', 'Se perdió la conexión de la transcripción.');
    };
  }
  await conectar();
  } catch (err) { soltar(); throw err; }
  if (ctx.state === 'suspended') await ctx.resume().catch(() => {});

  return {
    silenciar(v) { silenciado = v; },
    get silenciado() { return silenciado; },
    cerrar() {
      cerrado = true;
      try { ws?.close(); } catch { /* ya cerrado */ }
      nodo?.disconnect(); stream?.getTracks().forEach(t => t.stop()); ctx?.close().catch(() => {});
      onEstado?.('cerrado');
    },
  };
}

/**
 * ¿Es el eco del propio tutor? Si casi todas las palabras de lo transcrito
 * están en lo que el tutor está diciendo, se ignora (el altavoz se cuela en el
 * micrófono aunque el navegador cancele eco).
 */
export function esEco(oido, dichoPorTutor) {
  const pal = s => (s || '').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '').match(/[\p{L}\p{N}]+/gu) || [];
  const o = pal(oido); if (!o.length) return true;
  const d = new Set(pal(dichoPorTutor)); if (!d.size) return false;
  // Escrituras sin espacios (zh/ja): se compara por caracteres.
  if (o.length === 1 && o[0].length > 3 && /[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]/u.test(o[0])) {
    const cs = [...o[0]], todo = [...d].join(''); return cs.filter(c => todo.includes(c)).length / cs.length >= 0.7;
  }
  return o.filter(w => d.has(w)).length / o.length >= 0.6;
}
