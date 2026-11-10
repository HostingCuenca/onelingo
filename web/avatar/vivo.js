// Llamada en vivo: micrófono abierto transcrito en tiempo real por ElevenLabs
// (Scribe v2 Realtime) directamente desde el navegador, con un token de un solo
// uso que da el servidor (la clave nunca llega aquí). El servidor de
// ElevenLabs decide cuándo terminaste de hablar (VAD) y manda el texto final;
// mientras hablas llegan textos parciales (sirven para interrumpir al tutor).
//
// Audio: PCM 16 kHz mono en trozos de 100 ms desde un AudioWorklet.

const TROZO = 1600; // 100 ms a 16 kHz
// Errores de Scribe que reconectar no arregla (los demás vienen seguidos del cierre).
const FATALES = new Set(['auth_error', 'quota_exceeded', 'unaccepted_terms']);
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
 * Abre micrófono + transcripción. `pedirToken(cierre)` → {token, url, modelo};
 * `cierre` es null al empezar y, al reconectar, cómo se cortó la sesión
 * anterior (código, motivo, segundos abierta, estado del audio, último aviso
 * del servidor): el servidor lo guarda para saber por qué se corta en móviles.
 * Eventos: onParcial(texto), onFinal(texto), onEstado('escuchando'|'reconectando'|'cerrado'|'error', detalle).
 */
/**
 * Sin idioma fijo, Scribe a veces convierte ruido (un alumno que conducía) en
 * frases en hindi o árabe. Se descarta lo que esté escrito sobre todo en un
 * alfabeto que no es ni el del idioma de la clase ni el del alumno.
 */
const ESCRITURAS = {
  latin: /\p{Script=Latin}/u, han: /\p{Script=Han}/u, kana: /[\p{Script=Hiragana}\p{Script=Katakana}]/u,
  hangul: /\p{Script=Hangul}/u, cirilico: /\p{Script=Cyrillic}/u,
};
const ESCRITURA_DE = {zh: ['han'], ja: ['kana', 'han'], ko: ['hangul'], ru: ['cirilico']};
export function escrituraAjena(texto, ...idiomas) {
  const permitidas = new Set(idiomas.filter(Boolean).flatMap(i => ESCRITURA_DE[i] ?? ['latin']));
  // Las siglas y nombres en letras latinas son normales en cualquier idioma.
  permitidas.add('latin');
  const letras = [...String(texto)].filter(c => /\p{L}/u.test(c));
  if (!letras.length) return false;
  const propias = letras.filter(c => [...permitidas].some(e => ESCRITURAS[e].test(c))).length;
  return propias / letras.length < 0.5;
}

export async function abrirEscucha({pedirToken, idioma, onParcial, onFinal, onEstado}) {
  let cerrado = false, silenciado = false, ws = null, ctx = null, stream = null, nodo = null, reintentos = 0, analizador = null, muestras = null;
  let espera = null, abiertaEn = 0, parcial = '', aviso = '', cierre = null;
  const cola = []; // audio dicho mientras se reconecta (hasta 3 s), se manda al abrir
  stream = await navigator.mediaDevices.getUserMedia({audio: {echoCancellation: true, noiseSuppression: true, autoGainControl: true, channelCount: 1}});
  // Si algo falla antes de devolver el control (token 429/503, worklet), se
  // suelta el micrófono: si no, quedaba encendido el resto de la llamada.
  const soltar = () => { cerrado = true; clearTimeout(espera); try { ws?.close(); } catch {} stream?.getTracks().forEach(t => t.stop()); try { nodo?.disconnect(); } catch {} ctx?.close().catch(() => {}); };
  try {
  ctx = new AudioContext({sampleRate: 16000});
  const url = URL.createObjectURL(new Blob([WORKLET], {type: 'text/javascript'}));
  await ctx.audioWorklet.addModule(url); URL.revokeObjectURL(url);
  nodo = new AudioWorkletNode(ctx, 'captura-16k');
  const fuente = ctx.createMediaStreamSource(stream);
  fuente.connect(nodo);
  // Volumen de la voz para el efecto visual y para callar al tutor al instante.
  // Fuera del try: nivel() lo lee después (antes era const aquí y nivel() fallaba siempre).
  analizador = ctx.createAnalyser(); analizador.fftSize = 512; fuente.connect(analizador);
  muestras = new Float32Array(analizador.fftSize);
  // El nodo no suena: se conecta a un destino mudo para que el navegador lo procese.
  const mudo = ctx.createGain(); mudo.gain.value = 0; nodo.connect(mudo).connect(ctx.destination);
  const enviar = datos => ws.send(JSON.stringify({message_type: 'input_audio_chunk', audio_base_64: aBase64(datos), commit: false, sample_rate: 16000}));
  nodo.port.onmessage = e => {
    if (cerrado) return;
    const datos = silenciado ? new Float32Array(TROZO) : e.data; // silenciado: se manda silencio (la sesión sigue viva)
    if (ws?.readyState === 1) enviar(datos);
    else if (!silenciado) { cola.push(datos); if (cola.length > 30) cola.shift(); }
  };
  // Un AudioContext suspendido (llamada entrante, foco de audio) deja de mandar audio sin avisar.
  ctx.onstatechange = () => { if (!cerrado && ctx.state !== 'running' && ctx.state !== 'closed') ctx.resume().catch(() => {}); };

  async function conectar() {
    if (cerrado) return;
    const t = await pedirToken(cierre);
    if (cerrado) return;
    const q = new URLSearchParams({model_id: t.modelo || 'scribe_v2_realtime', token: t.token, audio_format: 'pcm_16000', commit_strategy: 'vad',
      vad_silence_threshold_secs: '0.5', min_speech_duration_ms: '250', ...(idioma ? {language_code: idioma} : {})});
    ws = new WebSocket(`${t.url}?${q}`);
    ws.onopen = () => { abiertaEn = performance.now(); aviso = ''; while (cola.length) enviar(cola.shift()); onEstado?.('escuchando'); };
    ws.onmessage = e => {
      let m; try { m = JSON.parse(e.data); } catch { return; }
      if (m.message_type === 'partial_transcript') { parcial = m.text || ''; onParcial?.(parcial); }
      else if (m.message_type === 'committed_transcript' || m.message_type === 'committed_transcript_with_timestamps') { parcial = ''; if ((m.text || '').trim()) onFinal?.(m.text.trim()); }
      else if (m.message_type !== 'session_started') {
        aviso = `${m.message_type}${m.error ? ': ' + m.error : ''}`.slice(0, 160);
        // Solo lo que no se arregla reconectando apaga la escucha; lo demás, si
        // el servidor corta la sesión, lo resuelve onclose.
        if (FATALES.has(m.message_type)) { soltar(); onEstado?.('error', aviso); }
      }
    };
    ws.onclose = e => {
      if (cerrado) return;
      const segundos = abiertaEn ? Math.round((performance.now() - abiertaEn) / 1000) : 0;
      cierre = {codigo: e.code, razon: (e.reason || '').slice(0, 120), segundos, audio: ctx.state, aviso};
      abiertaEn = 0;
      // Lo que iba diciendo ya no lo confirmará el servidor: se entrega tal cual.
      if (parcial.trim()) { onFinal?.(parcial.trim()); parcial = ''; }
      // La cuenta solo vuelve a cero tras una sesión larga: un corte en bucle
      // (cada 20 s en algunos móviles) pedía tokens sin fin.
      if (segundos >= 60) reintentos = 0;
      if (reintentos++ < 3) { onEstado?.('reconectando'); espera = setTimeout(() => conectar().catch(err => onEstado?.('error', String(err?.message || err))), 1000 * 2 ** (reintentos - 1)); }
      else onEstado?.('error', 'Se perdió la conexión de la transcripción.');
    };
  }
  await conectar();
  } catch (err) { soltar(); throw err; }
  if (ctx.state === 'suspended') await ctx.resume().catch(() => {});

  return {
    silenciar(v) { silenciado = v; },
    /** RMS de la voz en este instante (0 silenciado). */
    nivel() {
      if (silenciado || cerrado) return 0;
      analizador.getFloatTimeDomainData(muestras);
      let suma = 0; for (const x of muestras) suma += x * x;
      return Math.sqrt(suma / muestras.length);
    },
    get silenciado() { return silenciado; },
    cerrar() {
      cerrado = true; clearTimeout(espera);
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
