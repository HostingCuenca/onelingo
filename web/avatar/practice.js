// Videollamada con un tutor (Lumo 2D o tutores 3D) como una llamada real:
// llamada entrante / «Contestar», el tutor empieza hablando, mantener pulsado
// para hablar (como un audio de WhatsApp), subtítulos y colgar con resumen.
import {createAvatar} from './avatar.js?v=27';
import {createLumo} from './lumo.js?v=27';
import {envolvente, muestraEn, BANDAS_TIPICAS} from './voz.js?v=27';

const $ = id => document.getElementById(id), audio = $('audio');
// Todo lo que usa la conversación se carga ANTES de avisar a la app: si el
// aviso llegaba antes que topics.json, el saludo fallaba en silencio.
const [roster, units] = await Promise.all([
  fetch('./roster.json?v=23').then(r => r.json()),
  fetch('./topics.json?v=26').then(r => r.json()),
]);

let config = null, tutor = null, avatar = null, history = [], epoch = 0, selection = 0, busy = false, controller = null;
let lastReply = '', ultimoFallo = null, temaId = null, objetivoId = null, enLlamada = false, inicioLlamada = 0, reloj = null, correcciones = 0;
// Voz: cada frase se descarga como MP3 (con su envolvente para la boca) y
// suena en orden por un <audio> normal. Sin WebAudio: en iPhone, al abrir el
// micrófono el AudioContext cambiaba de frecuencia y la voz se entrecortaba.
let cola = [], sonando = false, respuestaCompleta = true, vozController = null, envActual = null, urlActual = null;
const SILENCIO = silencioWav();
// Grabación al mantener pulsado (como los audios de WhatsApp).
let grab = null;

const parametros = new URLSearchParams(location.search), embebido = parametros.has('embebido'), tutorInicial = parametros.get('tutor');
if (embebido) document.body.classList.add('embebido');
const languages = {en: 'inglés', es: 'español', fr: 'francés', de: 'alemán', pt: 'portugués', it: 'italiano', zh: 'chino', ja: 'japonés', ko: 'coreano', ru: 'ruso'};
const preferred = {en: ['lumo', 'amara', 'sofia', 'clara'], es: ['lumo', 'lucia', 'mateo'], fr: ['lumo', 'clara', 'sofia'], de: ['lumo', 'daniel', 'owen'], pt: ['lumo', 'amara', 'mateo'], it: ['lumo', 'sofia', 'mateo'], zh: ['lumo', 'mei', 'kenji'], ja: ['lumo', 'kenji', 'mei'], ko: ['lumo', 'mei', 'kenji'], ru: ['lumo', 'owen', 'clara']};
const language = () => config?.idiomaMeta || 'en', languageName = () => languages[language()] || languages.en;
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
const headers = () => ({Authorization: `Bearer ${config.token}`});
const conLimite = (p, ms) => Promise.race([p, new Promise(r => setTimeout(r, ms))]);

function phase(label, value = 'ready') { $('state').textContent = label; $('stage').dataset.phase = value; }
function status(t) { $('status').textContent = t; }
function error(e, reintentar) {
  const box = $('error'); box.replaceChildren();
  if (!e) return;
  box.append(e?.message || String(e));
  if (reintentar) { const b = el('button', null, 'Reintentar'); b.type = 'button'; b.onclick = reintentar; box.append(b); }
}
function controls() {
  const listo = !!config?.token && !!avatar && !!$('stage').dataset.loaded;
  $('llamar').disabled = !listo;
  $('hablar').disabled = !enLlamada;
  $('teclado').disabled = !enLlamada;
  $('send').disabled = !enLlamada || busy;
  $('tema').disabled = !!grab;
  document.body.classList.toggle('en-llamada', enLlamada);
}

// ---------- Arranque e integración con la app ----------
window.addEventListener('message', event => {
  if (event.origin !== location.origin || event.source !== parent) return;
  try {
    const c = JSON.parse(event.data);
    if (c.type !== 'onelingo-avatar-init') return;
    const u = new URL(c.api);
    if (u.origin !== location.origin && !['127.0.0.1', 'localhost'].includes(u.hostname)) return;
    config = c;
    // Abierta desde una situación: empieza con su tema y objetivo.
    const temaInicial = units.find(x => x.id === c.tema);
    if (temaInicial) { temaId = temaInicial.id; objetivoId = c.objetivoId || null; $('temaNombre').textContent = temaInicial.nombre; }
    $('authStatus').textContent = c.token ? `Nivel ${c.nivel} · tutores para practicar ${languageName()}` : 'Inicia sesión en OneLingo para conversar con los tutores.';
    $('text').placeholder = `Escribe en ${languageName()}…`;
    if (!embebido) renderGallery();
    controls();
    if (embebido && tutorInicial && !tutor) { const t = roster.tutors.find(x => x.id === tutorInicial); if (t) select(t); }
  } catch { /* mensaje ajeno */ }
});
parent.postMessage('onelingo-avatar-ready', location.origin);

function renderGallery() {
  const recommendations = preferred[language()] || preferred.en;
  const ordered = [...roster.tutors].sort((a, b) => { const ai = recommendations.indexOf(a.id), bi = recommendations.indexOf(b.id); return (ai < 0 ? 99 : ai) - (bi < 0 ? 99 : bi); });
  $('gallery').replaceChildren();
  for (const t of ordered) {
    const b = el('button', 'tutor'), portrait = el('div', 'portrait'), img = el('img');
    img.src = t.portrait; img.alt = `Retrato de ${t.name}`; img.loading = 'lazy'; portrait.append(img);
    b.append(portrait, el('strong', null, t.name), el('small', null, t.tipo === '2d' ? 'Tu compañero de OneLingo' : `Tutor de ${languageName()} · ${t.voice_direction.split(' · ')[2] || 'conversacional'}`));
    if (recommendations.includes(t.id)) b.append(el('span', 'recommended', 'Recomendado'));
    b.onclick = () => select(t);
    $('gallery').append(b);
  }
}
if (!embebido) renderGallery();

// La boca del tutor sigue la envolvente de la frase que suena.
const fuente = {
  muestra() {
    const hablando = sonando && !audio.paused && !audio.ended && audio.src !== SILENCIO;
    if (!hablando) return {hablando: false, amplitud: 0, graves: 0, medios: 0, agudos: 0, sibilantes: 0};
    const m = muestraEn(envActual, audio.currentTime);
    if (m) return {hablando: true, ...m};
    // Sin envolvente (no se pudo decodificar): movimiento aproximado.
    const t = audio.currentTime;
    return {hablando: true, amplitud: .25 + .35 * Math.abs(Math.sin(t * 9)), graves: BANDAS_TIPICAS.graves * (1 + Math.sin(t * 5)), medios: BANDAS_TIPICAS.medios * (1 + Math.cos(t * 7)), agudos: BANDAS_TIPICAS.agudos, sibilantes: BANDAS_TIPICAS.sibilantes};
  },
};

function sinSesion() {
  if (config?.token) return false;
  phase('Inicia sesión para conversar', 'error');
  status('Inicia sesión en OneLingo para conversar con tu tutor.');
  return true;
}

async function select(t) {
  colgar(false);
  document.body.classList.remove('puede-llamar');
  avatar?.dispose(); avatar = null; tutor = t; history = []; lastReply = ''; correcciones = 0;
  limpiarTurno(); $('messages').replaceChildren(); actualizarContador();
  $('name').textContent = t.name;
  $('selection').hidden = true; $('session').hidden = false;
  $('loading').hidden = false; $('loading').textContent = `Cargando a ${t.name}…`;
  error(''); phase('Preparando…', 'loading'); controls();
  const version = ++selection;
  try {
    avatar = t.tipo === '2d' ? createLumo($('stage'), fuente) : createAvatar($('stage'), fuente);
    // El saludo (texto y voz) se prepara mientras carga el personaje: al
    // contestar, el tutor habla al instante.
    const carga = avatar.load(t.model, e => { if (version === selection && e.total) $('loading').textContent = `Cargando a ${t.name} · ${Math.round(e.loaded / e.total * 100)} %`; });
    if (!sinSesion()) void requestTutor(null, true);
    await carga;
    if (version !== selection) return;
    $('loading').hidden = true; controls();
    if (!sinSesion()) void autoiniciar(version);
  } catch (e) {
    if (version !== selection) return;
    avatar?.dispose(); avatar = null; error(e); status('No se pudo cargar el tutor. Regresa y vuelve a intentarlo.'); controls();
  }
}

// ---------- Llamada ----------
// 50 ms de silencio en WAV: reproducirlo dentro del toque desbloquea el
// elemento <audio> en iOS para las frases que llegan después.
function silencioWav() {
  const n = 2205, b = new ArrayBuffer(44 + n * 2), v = new DataView(b), s = (o, t) => [...t].forEach((c, i) => v.setUint8(o + i, c.charCodeAt(0)));
  s(0, 'RIFF'); v.setUint32(4, 36 + n * 2, true); s(8, 'WAVEfmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
  v.setUint32(24, 44100, true); v.setUint32(28, 88200, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true); s(36, 'data'); v.setUint32(40, n * 2, true);
  return URL.createObjectURL(new Blob([b], {type: 'audio/wav'}));
}

// Que el tutor empiece hablando: si el navegador permite audio sin toque
// (escritorio, Android) la llamada arranca sola; si no (iPhone), llamada
// entrante con «Contestar» en lugar de un silencio.
async function autoiniciar(version) {
  audio.src = SILENCIO;
  const sonido = await conLimite(audio.play().then(() => true, () => false), 600);
  if (version !== selection || enLlamada) return;
  if (sonido === true) { iniciarLlamada(); return; }
  llamadaEntrante();
}
function llamadaEntrante() {
  document.body.classList.add('puede-llamar');
  phase('Te está llamando…', 'ringing');
  $('llamaTexto').textContent = `${tutor.name} te está llamando…`;
  $('llamarTexto').textContent = 'Contestar';
  status('');
}

// Lo que exige un gesto (desbloquear el <audio> y pedir el micrófono) se hace
// de forma síncrona dentro del toque.
function iniciarLlamada() {
  if (enLlamada || !avatar || !config?.token) return;
  if (audio.src !== SILENCIO || audio.paused) { audio.src = SILENCIO; audio.play().catch(() => {}); }
  // Permiso del micrófono al empezar: así no aparece a mitad de mantener pulsado.
  navigator.mediaDevices?.getUserMedia?.({audio: true}).then(s => s.getTracks().forEach(t => t.stop())).catch(() => {});
  document.body.classList.remove('puede-llamar');
  enLlamada = true; inicioLlamada = Date.now(); iniciarReloj(); controls(); error('');
  phase('Conectando…', 'thinking');
  vigilarConexion(epoch);
  if (cola.length) siguiente(epoch);
  else if (respuestaCompleta && !busy) { if (lastReply) encolar(lastReply, epoch); else void requestTutor(null, true); }
}
$('llamar').onclick = iniciarLlamada;

// Un saludo normal tarda 1–2 s. Si a los 7 s sigue «Conectando…» sin voz, se
// cancela la petición colgada y se reintenta (2 veces); después se avisa.
function vigilarConexion(version, intento = 1) {
  setTimeout(() => {
    if (!enLlamada || version !== epoch || $('stage').dataset.phase !== 'thinking' || sonando || grab) return;
    if (intento > 2) {
      colgar(false); phase('No se pudo conectar', 'error');
      $('llamaTexto').textContent = 'No se pudo conectar'; $('llamarTexto').textContent = 'Volver a llamar';
      error('El tutor no responde. Revisa tu conexión y vuelve a llamar.');
      return;
    }
    const saludo = !history.some(t => t.rol === 'alumno');
    stop(); phase('Conectando…', 'thinking'); status(`Reconectando con ${tutor.name}…`);
    if (lastReply && saludo) encolar(lastReply, epoch); else void requestTutor(saludo ? null : {continuar: true}, saludo);
    vigilarConexion(epoch, intento + 1);
  }, 7000);
}

function iniciarReloj() {
  clearInterval(reloj);
  reloj = setInterval(() => {
    if (!enLlamada) return;
    const s = Math.floor((Date.now() - inicioLlamada) / 1000);
    $('stage').dataset.reloj = `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
    if ($('stage').dataset.phase === 'ready') $('state').textContent = `En llamada · ${$('stage').dataset.reloj}`;
  }, 1000);
}

function colgar(resumen = true) {
  const habia = enLlamada;
  stop();
  if (grab) cancelarGrabacion();
  enLlamada = false; clearInterval(reloj); controls();
  $('form').hidden = true;
  if (habia && tutor) {
    document.body.classList.add('puede-llamar');
    phase('Llamada terminada', 'ready');
    $('llamaTexto').textContent = 'Llamada terminada';
    $('llamarTexto').textContent = 'Volver a llamar';
    status('');
    if (resumen && history.some(t => t.rol === 'alumno')) void mostrarResumen();
  }
}
$('end').onclick = () => colgar(true);
// Integrada en la app, la flecha devuelve a «Tutores con IA» (la app no pone cabecera propia).
$('back').onclick = () => { if (embebido) { colgar(false); parent.postMessage('onelingo-avatar-salir', location.origin); return; } selection++; colgar(false); avatar?.dispose(); avatar = null; $('session').hidden = true; $('selection').hidden = false; };

// ---------- Voz del tutor ----------
function senalVoz() { if (!vozController) vozController = new AbortController(); return vozController.signal; }
function urlVoz(text) {
  const url = new URL(config.api + '/voz/stream');
  url.search = new URLSearchParams({texto: text.slice(0, 600), idioma: language(), voz: 'avatar_' + tutor.id});
  return url;
}
function prepararFrase(text) {
  return fetch(urlVoz(text), {headers: headers(), signal: senalVoz()})
    .then(r => { if (!r.ok) throw Error(`La voz no está disponible (${r.status}).`); return r.arrayBuffer(); })
    .then(async bytes => ({url: URL.createObjectURL(new Blob([bytes], {type: 'audio/mpeg'})), env: await envolvente(bytes).catch(() => null)}));
}
// Cada frase se descarga en cuanto llega (en paralelo a la que suena). Antes
// de contestar solo se descargan: suenan al empezar la llamada.
function encolar(text, version) {
  const listo = prepararFrase(text);
  listo.catch(() => {});
  cola.push({text, listo});
  if (enLlamada && !sonando) siguiente(version);
}
async function siguiente(version) {
  const item = cola.shift();
  if (!item || version !== epoch) return;
  sonando = true;
  if ($('stage').dataset.phase !== 'speaking') phase('Preparando voz…', 'voice-loading');
  try {
    const f = await item.listo;
    if (version !== epoch) { URL.revokeObjectURL(f.url); return; }
    soltarURL(); urlActual = f.url; envActual = f.env;
    audio.src = f.url;
    await audio.play();
  } catch (e) {
    if (version !== epoch || vozController?.signal.aborted) return;
    sonando = false; envActual = null;
    if (cola.length) siguiente(version); else finTurno();
  }
}
function soltarURL() { if (urlActual) { URL.revokeObjectURL(urlActual); urlActual = null; } }
function detenerVoz() {
  vozController?.abort(); vozController = null;
  for (const item of cola) item.listo.then(f => URL.revokeObjectURL(f.url), () => {});
  cola = []; sonando = false; envActual = null;
  audio.pause(); audio.removeAttribute('src'); audio.load(); soltarURL();
}
audio.onplaying = () => {
  if (audio.src === SILENCIO) return;
  phase('Hablando…', 'speaking');
  status('Mantén pulsado 🎙 para interrumpir y responder.');
};
audio.onended = () => {
  if (audio.src === SILENCIO) return;
  envActual = null;
  if (cola.length) { siguiente(epoch); return; }
  sonando = false; finTurno();
};
audio.onerror = () => {
  if (!audio.getAttribute('src') || audio.src === SILENCIO || !sonando) return;
  sonando = false; envActual = null;
  if (cola.length) siguiente(epoch); else finTurno();
};
// El tutor terminó y no quedan frases por llegar: turno del alumno.
function finTurno() {
  if (!enLlamada || sonando || cola.length || !respuestaCompleta || busy || grab) return;
  phase(`En llamada · ${$('stage').dataset.reloj || '00:00'}`, 'ready');
  status(history.some(t => t.rol === 'alumno') ? 'Tu turno: mantén pulsado 🎙 para responder.' : 'Mantén pulsado 🎙 y responde en voz alta.');
}
$('replay').onclick = () => { if (!lastReply || busy || !enLlamada) return; detenerVoz(); encolar(lastReply, epoch); };

function stop() {
  epoch++; controller?.abort(); controller = null; detenerVoz();
  busy = false; respuestaCompleta = true; controls();
}

// ---------- Subtítulos, correcciones e ideas ----------
function limpiarTurno() {
  $('subTutor').textContent = ''; $('subTraduccion').hidden = true; $('verTraduccion').hidden = true; $('replay').hidden = true;
  $('subAlumno').hidden = true; $('nota').hidden = true; ideas([]);
}
function mostrarAlumno(texto) { $('subAlumno').textContent = texto; $('subAlumno').hidden = !texto; }
function burbuja(text, kind = '') { const e = el('div', 'bubble ' + kind, text); $('messages').append(e); return e; }
function actualizarContador() { $('contador').hidden = !correcciones; $('contador').textContent = correcciones; }
function correccion(c) {
  const card = el('div', 'correccion'), fila = el('div', 'correccion-fila');
  fila.append(el('s', null, c.original), el('span', 'flecha', '→'), el('strong', null, c.correcto));
  card.append(el('span', 'correccion-titulo', 'Corrección'), fila);
  if (c.explicacion) card.append(el('small', null, c.explicacion));
  $('messages').append(card);
  return card;
}
function nota(c, card) {
  const n = $('nota'); n.replaceChildren('✏️ ', el('s', null, c.original), ' → ', el('b', null, c.correcto));
  n.hidden = false; n.onclick = () => { abrirPanel('conversacion'); card.scrollIntoView({block: 'center'}); };
}
// Ideas para responder: tocar una la envía como respuesta.
function ideas(lista) {
  const box = $('ideas'); box.replaceChildren(); box.hidden = !lista.length;
  if (!lista.length) return;
  box.append(el('span', 'ideas-titulo', 'Puedes decir'));
  for (const s of lista) { const b = el('button', 'idea', s); b.type = 'button'; b.onclick = () => requestTutor({texto: s}, false); box.append(b); }
}
$('verTraduccion').onclick = () => { const t = $('subTraduccion'); t.hidden = !t.hidden; $('verTraduccion').textContent = t.hidden ? 'Ver traducción' : 'Ocultar traducción'; };

// ---------- Turno: texto o voz → respuesta por frases ----------
// entrada: null (saludo) · {texto} · {audio, tipo} · {continuar: true} (reintento sin turno nuevo)
async function requestTutor(entrada, opening = false) {
  if (busy || !config?.token || !tutor || !avatar) return;
  if (!opening) stop();
  const version = epoch;
  busy = true; respuestaCompleta = false; controls(); error(''); ultimoFallo = null;
  let frases = 0, final = false, transcrito = false;
  if (!opening) {
    limpiarTurno();
    if (entrada?.texto) { mostrarAlumno(entrada.texto); burbuja(entrada.texto, 'mine'); history.push({rol: 'alumno', texto: entrada.texto}); }
    else if (entrada?.audio) mostrarAlumno('…');
    phase('Pensando…', 'thinking'); status('');
  } else if (enLlamada) phase('Conectando…', 'thinking');
  controller = new AbortController();
  const current = controller, timeout = setTimeout(() => current.abort(), 45000);
  try {
    const u = units.find(x => x.id === temaId);
    const datos = {idiomaMeta: language(), idiomaNativo: config.idiomaNativo, nivel: config.nivel, tutorId: 'avatar_' + tutor.id, historial: history.slice(-30), objetivo: config.contexto, ...(u ? {situacionId: u.id, situacion: u.nombre} : {}), ...(u && objetivoId ? {objetivoId} : {})};
    let response;
    if (entrada?.audio) {
      const form = new FormData();
      form.append('datos', JSON.stringify(datos));
      form.append('audio', entrada.audio, entrada.tipo?.includes('mp4') ? 'turno.m4a' : 'turno.webm');
      response = await fetch(config.api + '/chat/voz', {method: 'POST', headers: headers(), body: form, signal: current.signal});
      // Servidor sin /chat/voz: transcribir y responder en dos pasos.
      if (response.status === 404) {
        const f2 = new FormData(); f2.append('idioma', language()); f2.append('audio', entrada.audio, entrada.tipo?.includes('mp4') ? 'turno.m4a' : 'turno.webm');
        const tr = await fetch(config.api + '/transcribir', {method: 'POST', headers: headers(), body: f2, signal: current.signal});
        if (!tr.ok) throw Error('No se pudo transcribir. Vuelve a intentarlo o escribe con ⌨️.');
        const texto = ((await tr.json()).texto || '').trim();
        if (!texto) throw Error('No te escuché bien. Mantén pulsado el micrófono mientras hablas.');
        transcrito = true; mostrarAlumno(texto); burbuja(texto, 'mine'); history.push({rol: 'alumno', texto});
        response = await fetch(config.api + '/chat', {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json', Accept: 'text/event-stream'}, body: JSON.stringify({...datos, historial: history.slice(-30)}), signal: current.signal});
      }
    } else {
      response = await fetch(config.api + '/chat', {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json', Accept: 'text/event-stream'}, body: JSON.stringify(datos), signal: current.signal});
    }
    if (!response.ok) throw Error(response.status === 401 ? 'Tu sesión ha caducado. Vuelve a iniciar sesión.' : `No se pudo conectar con el tutor (${response.status}).`);
    const reader = response.body.getReader(), decoder = new TextDecoder();
    let pending = '';
    const evento = raw => {
      if (version !== epoch) return;
      const line = raw.split('\n').find(l => l.startsWith('data: '));
      if (!line) return;
      const e = JSON.parse(line.slice(6));
      if (e.tipo === 'error') throw Error(e.data);
      if (e.tipo === 'transcripcion') {
        transcrito = true;
        mostrarAlumno(e.data.texto); burbuja(e.data.texto, 'mine');
        history.push({rol: 'alumno', texto: e.data.texto});
      }
      // Cada frase terminada se muestra y se dice sin esperar al resto.
      if (e.tipo === 'frase') { $('subTutor').textContent = (frases ? $('subTutor').textContent + ' ' : '') + e.data.texto; frases++; encolar(e.data.texto, version); }
      if (e.tipo === 'reply' && !frases) { $('subTutor').textContent = e.data; frases++; encolar(e.data, version); }
      if (e.tipo === 'final') {
        final = true;
        const r = e.data;
        if (!frases) { frases++; encolar(r.reply, version); }
        lastReply = r.reply; $('subTutor').textContent = r.reply; $('replay').hidden = false;
        history.push({rol: 'tutor', texto: r.reply});
        const b = burbuja(r.reply);
        if (r.romanizacion) b.append(el('span', 'romanizacion', r.romanizacion));
        if (r.traduccion) {
          $('subTraduccion').textContent = r.traduccion; $('subTraduccion').hidden = true;
          $('verTraduccion').hidden = false; $('verTraduccion').textContent = 'Ver traducción';
          const d = el('details', 'traduccion'); d.append(el('summary', null, 'Ver traducción'), el('span', null, r.traduccion)); b.append(d);
        }
        const cs = r.corrections || [];
        cs.forEach((c, i) => { const card = correccion(c); if (i === 0) nota(c, card); });
        correcciones += cs.length; actualizarContador();
        ideas((r.suggestions || []).slice(0, 3));
      }
    };
    while (true) {
      const {done, value} = await reader.read();
      if (done) break;
      pending += decoder.decode(value, {stream: true});
      const parts = pending.split('\n\n'); pending = parts.pop();
      for (const p of parts) evento(p);
    }
    if (!final) throw Error('La respuesta quedó incompleta.');
  } catch (e) {
    if (version === epoch) {
      // Nunca dejar al alumno esperando: se explica y se ofrece reintentar.
      const msg = e.name === 'AbortError' ? 'El tutor tardó demasiado.' : (e.message || 'No se pudo responder.');
      if (entrada?.audio && !transcrito) { mostrarAlumno(''); ultimoFallo = entrada; }
      else if (!opening && !frases) ultimoFallo = {continuar: true};
      if (entrada?.texto && !frases) ultimoFallo = {continuar: true};
      phase('No se pudo responder', 'error');
      const reintento = ultimoFallo;
      error(msg, reintento || opening ? () => requestTutor(reintento, opening) : null);
    }
  } finally {
    clearTimeout(timeout);
    if (version === epoch) { busy = false; respuestaCompleta = true; controller = null; controls(); if ($('stage').dataset.phase !== 'error') finTurno(); }
  }
}
$('form').onsubmit = event => { event.preventDefault(); const t = $('text').value.trim(); if (!t || busy) return; $('text').value = ''; requestTutor({texto: t}, false); };
$('teclado').onclick = () => { const f = $('form'); f.hidden = !f.hidden; if (!f.hidden) $('text').focus(); };

// ---------- Mantener pulsado para hablar ----------
const hablar = $('hablar');
function empezarGrabacion(x) {
  if (!enLlamada || grab) return;
  if (sonando || busy) stop(); // hablar interrumpe al tutor
  const mio = {x0: x, chunks: [], cancelado: false, soltado: false};
  grab = mio; error('');
  document.body.classList.add('grabando'); document.body.classList.remove('cancelando');
  phase('Te escucho…', 'listening'); limpiarTurno(); status('');
  $('hablarTexto').textContent = 'Habla… suelta para enviar · ← desliza para cancelar';
  controls();
  navigator.mediaDevices.getUserMedia({audio: {echoCancellation: true, noiseSuppression: true, autoGainControl: true}}).then(stream => {
    if (grab !== mio || mio.soltado) { stream.getTracks().forEach(t => t.stop()); if (grab === mio) terminarSinEnviar('Mantén pulsado 🎙 mientras hablas.'); return; }
    mio.stream = stream;
    const mime = ['audio/webm;codecs=opus', 'audio/mp4', 'audio/webm'].find(t => MediaRecorder.isTypeSupported(t));
    mio.rec = new MediaRecorder(stream, mime ? {mimeType: mime} : {});
    mio.rec.ondataavailable = e => { if (e.data.size) mio.chunks.push(e.data); };
    mio.rec.onstop = () => finGrabacion(mio);
    mio.rec.start(250); mio.desde = performance.now();
    mio.limite = setTimeout(soltar, 60000);
    mio.cuenta = setInterval(() => { if (mio.cancelado) return; const s = Math.floor((performance.now() - mio.desde) / 1000); $('hablarTexto').textContent = `● 0:${String(s).padStart(2, '0')} · suelta para enviar · ← desliza para cancelar`; }, 250);
  }).catch(e => {
    if (grab === mio) terminarSinEnviar('');
    error(e?.name === 'NotAllowedError' ? 'Activa el permiso del micrófono para hablar, o escribe con ⌨️.' : 'No se pudo abrir el micrófono. Puedes escribir con ⌨️.');
  });
}
function terminarSinEnviar(pista) {
  const mio = grab; grab = null;
  if (mio) { clearTimeout(mio.limite); clearInterval(mio.cuenta); mio.stream?.getTracks().forEach(t => t.stop()); }
  document.body.classList.remove('grabando', 'cancelando');
  $('hablarTexto').textContent = 'Mantén pulsado para hablar';
  controls(); phase(`En llamada · ${$('stage').dataset.reloj || '00:00'}`, 'ready'); status(pista);
}
function soltar() {
  const mio = grab;
  if (!mio || mio.soltado) return;
  mio.soltado = true;
  if (!mio.rec) return; // aún abriendo el micrófono: se resuelve al llegar el permiso
  clearTimeout(mio.limite);
  // 250 ms más para no cortar la última sílaba.
  setTimeout(() => { if (mio.rec.state === 'recording') mio.rec.stop(); }, mio.cancelado ? 0 : 250);
}
function cancelarGrabacion() { const mio = grab; if (!mio) return; mio.cancelado = true; if (mio.rec) soltar(); else terminarSinEnviar(''); }
function finGrabacion(mio) {
  const dur = performance.now() - mio.desde;
  if (grab === mio) terminarSinEnviar('');
  if (mio.cancelado) { status('Mensaje cancelado.'); return; }
  if (dur < 700) { status('Mantén pulsado 🎙 mientras hablas y suelta al terminar.'); return; }
  const blob = new Blob(mio.chunks, {type: mio.rec.mimeType || 'audio/webm'});
  if (blob.size < 500) { status('No te escuché. Acércate al micrófono y vuelve a intentarlo.'); return; }
  void requestTutor({audio: blob, tipo: blob.type}, false);
}
hablar.addEventListener('pointerdown', e => {
  if (e.button > 0 || hablar.disabled) return;
  e.preventDefault();
  try { hablar.setPointerCapture(e.pointerId); } catch { /* sin captura */ }
  empezarGrabacion(e.clientX);
});
hablar.addEventListener('pointermove', e => {
  if (grab && !grab.cancelado && grab.x0 - e.clientX > 80) { grab.cancelado = true; document.body.classList.add('cancelando'); $('hablarTexto').textContent = 'Suelta para cancelar'; }
});
hablar.addEventListener('pointerup', soltar);
hablar.addEventListener('pointercancel', () => { if (grab) grab.cancelado = true; soltar(); });
hablar.addEventListener('lostpointercapture', soltar);
hablar.addEventListener('contextmenu', e => e.preventDefault());
hablar.addEventListener('keydown', e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); empezarGrabacion(0); } });
hablar.addEventListener('keyup', e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); soltar(); } });
hablar.addEventListener('click', e => e.preventDefault());

// ---------- Hoja inferior: conversación y temas ----------
function abrirPanel(cual) {
  $('panel').hidden = false;
  $('messages').hidden = cual !== 'conversacion';
  $('temas').hidden = cual !== 'temas';
  $('panelTitulo').textContent = cual === 'temas' ? '¿Qué quieres practicar?' : 'Conversación';
  if (cual === 'temas') pintarTemas();
  else $('messages').lastElementChild?.scrollIntoView({block: 'end'});
}
$('verConversacion').onclick = () => abrirPanel('conversacion');
$('cerrarPanel').onclick = () => { $('panel').hidden = true; };
$('tema').onclick = () => abrirPanel('temas');
function pintarTemas() {
  const box = $('temas'); box.replaceChildren();
  for (const u of [{id: null, nombre: 'Conversación libre'}, ...units]) {
    const b = el('button', 'opcion-tema', u.nombre); b.type = 'button';
    b.setAttribute('aria-pressed', String(u.id === temaId));
    b.onclick = () => elegirTema(u);
    box.append(b);
  }
}
// Cambiar de tema reinicia la conversación: el tutor abre la nueva situación.
function elegirTema(u) {
  $('panel').hidden = true;
  if (u.id === temaId) return;
  temaId = u.id; objetivoId = null; $('temaNombre').textContent = u.nombre;
  stop(); if (grab) cancelarGrabacion();
  history = []; lastReply = ''; limpiarTurno();
  burbuja(`Nuevo tema: ${u.nombre}`, 'feedback');
  void requestTutor(null, true);
}

// ---------- Resumen al colgar ----------
async function mostrarResumen() {
  abrirPanel('conversacion');
  const card = el('div', 'resumen'); card.append(el('h3', null, 'Resumen de la llamada'), el('p', null, 'Preparando…'));
  $('messages').append(card); card.scrollIntoView({block: 'end'});
  try {
    const r = await fetch(config.api + '/chat/resumen', {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json'}, body: JSON.stringify({idiomaMeta: language(), idiomaNativo: config.idiomaNativo, nivel: config.nivel, tutorId: 'avatar_' + tutor.id, historial: history.slice(-40)})});
    if (!r.ok) throw Error('No se pudo preparar el resumen.');
    const d = await r.json();
    card.replaceChildren(el('h3', null, 'Resumen de la llamada'));
    const seccion = (titulo, items) => { if (!items.length) return; card.append(el('h4', null, titulo)); const ul = el('ul'); for (const i of items) ul.append(i); card.append(ul); };
    seccion('Lo hiciste bien', (d.logros || []).map(t => el('li', null, t)));
    seccion('Para mejorar', (d.mejorar || []).map(m => { const li = el('li'); li.append(el('s', null, m.original), ' → ', el('strong', null, m.correcto), el('small', null, m.explicacion)); return li; }));
    seccion('Vocabulario de hoy', (d.vocabulario || []).map(v => { const li = el('li'); li.append(el('strong', null, v.palabra), ' · ' + v.significado); return li; }));
    if (d.siguientePaso) card.append(el('p', 'siguiente', d.siguientePaso));
    card.append(el('p', null, `${tutor.name} recordará esto en tu próxima llamada.`));
    card.scrollIntoView({block: 'end'});
  } catch (e) { card.replaceChildren(el('h3', null, 'Resumen de la llamada'), el('p', null, e.message)); }
}

window.addEventListener('offline', () => { stop(); error('No hay conexión. Vuelve a intentarlo cuando tengas internet.'); });
window.addEventListener('pagehide', () => { colgar(false); avatar?.dispose(); });
document.addEventListener('visibilitychange', () => { if (document.hidden && grab) cancelarGrabacion(); });
controls();
