// Videollamada con un tutor (Lumo 2D o tutores 3D) como una llamada real:
// llamada entrante / «Contestar», el tutor empieza hablando, mantener pulsado
// para hablar (como un audio de WhatsApp), subtítulos y colgar con resumen.
import {createAvatar} from './avatar.js?v=27';
import {createLumo} from './lumo.js?v=27';
import {envolvente, muestraEn, BANDAS_TIPICAS} from './voz.js?v=27';
import {createAvatarTH} from './avatar-th.js?v=14';
import {lineaDeVisemas, alineacionEstimada} from './visemas.js?v=1';
import {abrirEscucha, esEco, vivoDisponible} from './vivo.js?v=5';

const $ = id => document.getElementById(id), audio = $('audio');
// Todo lo que usa la conversación se carga ANTES de avisar a la app: si el
// aviso llegaba antes que topics.json, el saludo fallaba en silencio.
const [roster, units] = await Promise.all([
  fetch('./roster.json?v=34').then(r => r.json()),
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
// Llamada en vivo: micrófono abierto con transcripción en tiempo real; si no
// se puede (navegador, red, servidor sin clave) se vuelve a mantener pulsado.
let vivo = null, modoVivo = false, mudo = false, arrastre = '', finVozEn = 0, lineaActual = null;
// El tutor no empieza a hablar antes de esta hora: si el alumno hace una pausa
// a mitad de frase, la respuesta se prepara pero espera (y se descarta si sigue).
let retenerHasta = 0, rescate = null;
// Turno en curso: dónde empezó (historial, conversación, correcciones) para
// deshacerlo si el alumno sigue hablando antes de que el tutor se oiga.
let turno = null, enPuerta = false, ultimaVoz = 0;
// Frase que suena (y lo dicho justo antes, para el filtro de eco); generación
// de la escucha en vivo (una apertura vieja que termina tarde se cierra sola).
let itemActual = null, dichoReciente = '', genVivo = 0, ultimoParcialEn = 0, bloqueoPantalla = null;
const alumnoSuena = () => performance.now() - ultimaVoz < 600;
// Respuesta en camino que aún no se oye (esperando o arrancando el audio).
const noSeOye = () => sonando && (turno ? !turno.oido : enPuerta);
// Última palabra que deja la frase colgando: el alumno está pensando, no terminó.
const COLGANTES = {
  en: 'the a an and but or so because to of in on at with for from my your his her our their uh um er very',
  es: 'el la los las un una y pero o porque que de del en con para por mi tu su eh muy cuando',
  fr: 'le la les un une et mais ou parce que de du des en avec pour par mon ma mes euh très quand',
  de: 'der die das den dem ein eine und aber oder weil dass mit für von mein meine äh ähm sehr wenn',
  pt: 'o a os as um uma e mas ou porque que de do da em com para por meu minha hum muito quando',
  it: 'il lo la i gli le un una e ma o perché che di del in con per mio mia ehm molto quando',
  ru: 'и но или потому что в на с для мой э ну очень когда',
};
function fraseIncompleta(texto) {
  const t = texto.trim();
  if (!t || /(,|;|:|…|-|–|\.\.\.)$/.test(t)) return true;
  // La transcripción pone punto aunque la frase quede colgando («I went to the.»): se mira la palabra.
  const ultima = (t.toLowerCase().replace(/[.!?。！？]+$/u, '').match(/[\p{L}']+$/u) || [''])[0];
  return (COLGANTES[language()] || '').split(' ').includes(ultima);
}
// Silencio que se le da al alumno tras cerrar la frase: más si quedó colgando y en niveles bajos.
function paciencia(texto) {
  const bajo = (config?.nivel ?? 1) <= 2 ? 250 : 0;
  return (fraseIncompleta(texto) ? 1700 : 450) + bajo;
}
// Si el alumno se queda en blanco, el tutor le ayuda hablando (como un profesor):
// primero repite la pregunta más fácil y con opciones; después, una pista. Luego espera.
const ESPERAS_SILENCIO = [9000, 12000];
let silencioTimer = null, silencios = 0;
// Mientras piensa, una muletilla corta en su idioma si tarda: sin silencios muertos.
const RELLENOS = {en: ['Okay…', 'I see…', 'Right…'], es: ['A ver…', 'Ajá…', 'Entiendo…'], fr: ['D’accord…', 'Je vois…', 'Ah, oui…'], de: ['Okay…', 'Verstehe…', 'Ach so…'],
  pt: ['Entendi…', 'Certo…', 'Ah, sim…'], it: ['Capisco…', 'Allora…', 'Ah, sì…'], zh: ['好的…', '这样啊…', '我明白了…'], ja: ['そうですね…', 'なるほど…', 'ええと…'],
  ko: ['아, 그렇군요…', '네…', '그렇군요…'], ru: ['Так…', 'Понятно…', 'Ага…']};
let relleno = '', rellenos = 0;

const parametros = new URLSearchParams(location.search), embebido = parametros.has('embebido'), tutorInicial = parametros.get('tutor');
if (embebido) document.body.classList.add('embebido');
const languages = {en: 'inglés', es: 'español', fr: 'francés', de: 'alemán', pt: 'portugués', it: 'italiano', zh: 'chino', ja: 'japonés', ko: 'coreano', ru: 'ruso'};
// Tutores en vivo (6 × 2, ellas y ellos) con los especialistas del idioma primero
// (idioma de primera mano: personajes.ts) y luego Lumo.
const VIVOS = ['ana', 'elena', 'julia', 'chloe', 'nora', 'hana', 'lucas', 'tomas', 'frank', 'diego', 'erik', 'andre'];
const ESPECIALISTAS = {en: ['frank'], es: ['diego', 'tomas'], fr: ['lucas', 'andre'], de: ['nora'], pt: ['julia'], it: ['elena'], zh: ['ana'], ja: ['erik'], ko: ['hana'], ru: ['chloe']};
// Los tutores 3D de MakeHuman (amara, sofia…) están ocultos por ahora: no salen en la
// galería, aunque /avatar/<id> todavía los abre (tutores_3d.dart).
const preferred = Object.fromEntries(Object.entries(ESPECIALISTAS).map(([l, esp]) => [l, [...esp, ...VIVOS.filter(t => !esp.includes(t)), 'lumo']]));
const language = () => config?.idiomaMeta || 'en', languageName = () => languages[language()] || languages.en;
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
const headers = () => ({Authorization: `Bearer ${config.token}`});
const conLimite = (p, ms) => Promise.race([p, new Promise(r => setTimeout(r, ms))]);

const INSIGNIAS = {speaking: 'Hablando', 'voice-loading': 'Pensando…', thinking: 'Pensando…', listening: 'Te escucho', ready: 'Tu turno'};
function phase(label, value = 'ready') {
  $('state').textContent = label; $('stage').dataset.phase = value;
  const i = $('insignia'); i.textContent = enLlamada ? (value === 'ready' && mudo ? 'Micrófono en silencio' : INSIGNIAS[value] ?? '') : ''; i.hidden = !i.textContent;
  $('pedirPista').hidden = !(enLlamada && value === 'ready');
}
function status(t) { $('status').textContent = t; }
function error(e, reintentar, etiqueta = 'Reintentar') {
  const box = $('error'); box.replaceChildren();
  if (!e) return;
  box.append(e?.message || String(e));
  if (reintentar) { const b = el('button', null, etiqueta); b.type = 'button'; b.onclick = reintentar; box.append(b); }
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
    // La app la pausa al cambiar de pestaña o al irse a segundo plano (el visor sigue montado).
    if (c.type === 'onelingo-avatar-pausa') { window.onelingoPausa(); return; }
    if (c.type === 'onelingo-avatar-reanudar') { window.onelingoReanudar(); return; }
    if (c.type !== 'onelingo-avatar-init') return;
    const u = new URL(c.api);
    if (u.origin !== location.origin && u.hostname !== location.hostname && !['127.0.0.1', 'localhost'].includes(u.hostname)) return;
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
// En Android el visor va en un WebView: los avisos salen por su canal `OneLingo`.
const avisarApp = msg => window.OneLingo?.postMessage ? window.OneLingo.postMessage(msg) : parent.postMessage(msg, location.origin);
avisarApp('onelingo-avatar-ready');

function renderGallery() {
  const recommendations = preferred[language()] || preferred.en;
  const ordered = roster.tutors.filter(t => recommendations.includes(t.id) || t.id === tutorInicial).sort((a, b) => { const ai = recommendations.indexOf(a.id), bi = recommendations.indexOf(b.id); return (ai < 0 ? 99 : ai) - (bi < 0 ? 99 : bi); });
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
  // Avatares con visemas alineados: la boca sigue los tiempos de cada letra.
  reloj() {
    const hablando = sonando && !audio.paused && !audio.ended && audio.src !== SILENCIO;
    return {hablando, ms: audio.currentTime * 1000, linea: lineaActual};
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
    avatar = t.tipo === '2d' ? createLumo($('stage'), fuente) : t.tipo === 'th' ? createAvatarTH($('stage'), fuente, t.th) : createAvatar($('stage'), fuente);
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
  if (vivoDisponible()) abrirVivo();
  else navigator.mediaDevices?.getUserMedia?.({audio: true}).then(s => s.getTracks().forEach(t => t.stop())).catch(() => {});
  document.body.classList.remove('puede-llamar');
  enLlamada = true; inicioLlamada = Date.now(); iniciarReloj(); controls(); error('');
  mantenerPantalla();
  phase('Conectando…', 'thinking');
  vigilarConexion(epoch);
  setTimeout(calentarRellenos, 4000);
  if (cola.length) siguiente(epoch);
  else if (respuestaCompleta && !busy) { if (lastReply) encolar(lastReply, epoch); else void requestTutor(null, true); }
}
$('llamar').onclick = iniciarLlamada;
// En vivo se habla sin tocar la pantalla: si se apagaba, la página quedaba oculta y se cortaba la llamada.
function mantenerPantalla() {
  if (!enLlamada || bloqueoPantalla || !navigator.wakeLock) return;
  navigator.wakeLock.request('screen').then(l => { if (!enLlamada) { l.release().catch(() => {}); return; } bloqueoPantalla = l; l.onrelease = () => { bloqueoPantalla = null; }; }).catch(() => {});
}

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

// Las muletillas quedan en la caché de voz del servidor: después suenan al instante.
function calentarRellenos() {
  if (!enLlamada || !tutor) return;
  for (const f of RELLENOS[language()] || []) fetch(urlVoz(f, '', avatar?.alineado ? '/voz/alineada' : '/voz/stream'), {headers: headers()}).catch(() => {});
}
function ponerRelleno(version) {
  if (performance.now() < retenerHasta) return; // el alumno quizá sigue: nada de muletillas encima
  const lista = RELLENOS[language()] || []; if (!lista.length) return;
  relleno = lista[rellenos++ % lista.length]; encolar(relleno, version, undefined, true);
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
  cerrarVivo();
  enLlamada = false; clearInterval(reloj); controls();
  turno = null; arrastre = ''; clearTimeout(rescate);
  bloqueoPantalla?.release().catch(() => {}); bloqueoPantalla = null;
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
$('back').onclick = () => { if (embebido) { colgar(false); avisarApp('onelingo-avatar-salir'); return; } selection++; colgar(false); avatar?.dispose(); avatar = null; $('session').hidden = true; $('selection').hidden = false; };

// ---------- Voz del tutor ----------
function senalVoz() { if (!vozController) vozController = new AbortController(); return vozController.signal; }
// La voz es la nativa del idioma practicado según el género del avatar
// (rolDeVoz en backend/src/lib/voz.ts). Un texto largo lo divide el servidor
// por frases. `previo` (la frase anterior de la misma respuesta) va como
// previous_text: cada frase no empieza con entonación de inicio.
function urlVoz(text, previo = '', ruta = '/voz/stream') {
  const url = new URL(config.api + ruta);
  url.search = new URLSearchParams({texto: text, idioma: language(), voz: 'avatar_' + tutor.id, ...(previo ? {previo} : {})});
  return url;
}
let fraseAnterior = {version: -1, texto: ''};
// Voz que el servidor manda dentro de la respuesta (evento `voz`), por índice de frase.
let vozEnLinea = null;
let vozActiva = false; // el servidor confirmó que manda la voz en el stream
function vozDelStream(indice) {
  if (!vozEnLinea || !vozActiva || indice == null) return null;
  let item = vozEnLinea.get(indice);
  if (!item) { let ok; const p = new Promise(r => { ok = r; }); item = {p, ok}; vozEnLinea.set(indice, item); }
  return item;
}
const fraseAlineada = (d, text) => ({url: URL.createObjectURL(new Blob([Uint8Array.from(atob(d.audio), c => c.charCodeAt(0))], {type: 'audio/mpeg'})), env: null, texto: text,
  linea: d.alineacion ? lineaDeVisemas(d.alineacion, language()) : null});
function prepararFrase(text, version, indice) {
  const previo = fraseAnterior.version === version ? fraseAnterior.texto : '';
  fraseAnterior = {version, texto: text};
  // Con visemas: el MP3 llega junto con el tiempo de cada letra.
  if (avatar?.alineado) {
    const pedir = () => fetch(urlVoz(text, previo, '/voz/alineada'), {headers: headers(), signal: senalVoz()})
      .then(r => { if (!r.ok) throw Error(`La voz no está disponible (${r.status}).`); return r.json(); });
    const delStream = vozDelStream(indice);
    // Si la voz no llega en el stream (servidor viejo o fallo), se pide aparte.
    const datos = delStream ? conLimite(delStream.p, 4000).then(d => d?.audio ? d : pedir()) : pedir();
    return datos.then(d => fraseAlineada(d, text));
  }
  return fetch(urlVoz(text, previo), {headers: headers(), signal: senalVoz()})
    .then(r => { if (!r.ok) throw Error(`La voz no está disponible (${r.status}).`); return r.arrayBuffer(); })
    .then(async bytes => ({url: URL.createObjectURL(new Blob([bytes], {type: 'audio/mpeg'})), env: await envolvente(bytes).catch(() => null)}));
}
// Cada frase se descarga en cuanto llega (en paralelo a la que suena). Antes
// de contestar solo se descargan: suenan al empezar la llamada.
function encolar(text, version, indice, esRelleno = false) {
  const listo = prepararFrase(text, version, indice);
  listo.catch(() => {});
  cola.push({text, listo, relleno: esRelleno});
  if (enLlamada && !sonando) siguiente(version);
}
async function siguiente(version) {
  const item = cola.shift();
  if (!item || version !== epoch) return;
  sonando = true; enPuerta = true;
  if ($('stage').dataset.phase !== 'speaking') phase('Preparando voz…', 'voice-loading');
  try {
    const f = await item.listo;
    window.__marca?.('frase_lista');
    if (version !== epoch) { URL.revokeObjectURL(f.url); return; }
    // Pausa del alumno: la respuesta está lista pero se espera por si sigue
    // hablando. Si su voz suena (el micrófono lo sabe antes que la transcripción),
    // se sigue esperando; con ruido constante, como mucho 2,5 s más.
    const tope = Math.max(retenerHasta, performance.now()) + 2500;
    while (version === epoch && (performance.now() < retenerHasta || (alumnoSuena() && !turno?.oido && performance.now() < tope))) await new Promise(r => setTimeout(r, 40));
    enPuerta = false;
    if (version !== epoch) { URL.revokeObjectURL(f.url); return; }
    soltarURL(); urlActual = f.url; envActual = f.env; lineaActual = f.linea || null;
    dichoReciente = `${itemActual && !itemActual.relleno ? itemActual.text : ''} ${item.text}`; itemActual = item;
    window.__marca?.('play'); audio.src = f.url;
    // Audio guardado antes de existir la alineación: tiempos repartidos por la duración.
    if (f.texto && !f.linea) audio.addEventListener('loadedmetadata', () => { if (urlActual === f.url && isFinite(audio.duration)) lineaActual = lineaDeVisemas(alineacionEstimada(f.texto, audio.duration), language()); }, {once: true});
    await audio.play();
  } catch (e) {
    if (version !== epoch || vozController?.signal.aborted) return;
    enPuerta = false; terminarFrase(item, false);
  }
}
// Una frase termina una sola vez: un MP3 roto dispara `error` y además rechaza
// play(), y avanzar dos veces se saltaba una frase o sonaba con `sonando` falso.
function terminarFrase(item, oida) {
  if (!item || item.hecho) return;
  item.hecho = true; envActual = null; lineaActual = null;
  if (oida) finVozEn = performance.now();
  if (item.relleno) relleno = '';
  if (cola.length) siguiente(epoch); else { sonando = false; finTurno(); }
}
function soltarURL() { if (urlActual) { URL.revokeObjectURL(urlActual); urlActual = null; } }
function detenerVoz() {
  vozController?.abort(); vozController = null; fraseAnterior = {version: -1, texto: ''};
  for (const item of cola) item.listo.then(f => URL.revokeObjectURL(f.url), () => {});
  cola = []; sonando = false; enPuerta = false; envActual = null; lineaActual = null; itemActual = null;
  audio.pause(); audio.removeAttribute('src'); audio.load(); soltarURL();
}
audio.onplaying = () => {
  if (audio.src === SILENCIO) return;
  // La muletilla («Okay…») no es la respuesta: el alumno puede seguir y se deshace igual.
  if (turno && !itemActual?.relleno) turno.oido = true;
  phase('Hablando…', 'speaking');
  status(modoVivo ? (mudo ? 'Micrófono silenciado: toca 🎙 para hablar.' : 'Puedes interrumpir hablando.') : 'Mantén pulsado 🎙 para interrumpir y responder.');
};
audio.onended = () => { if (audio.src !== SILENCIO) terminarFrase(itemActual, true); };
audio.onerror = () => {
  if (!audio.getAttribute('src') || audio.src === SILENCIO || !sonando) return;
  terminarFrase(itemActual, false);
};
// El tutor terminó y no quedan frases por llegar: turno del alumno.
function finTurno() {
  if (!enLlamada || sonando || cola.length || !respuestaCompleta || busy || grab) return;
  phase(`En llamada · ${$('stage').dataset.reloj || '00:00'}`, 'ready');
  if (modoVivo) status(mudo ? 'Micrófono silenciado: toca 🎙 para hablar.' : 'Tu turno: habla cuando quieras.');
  else status(history.some(t => t.rol === 'alumno') ? 'Tu turno: mantén pulsado 🎙 para responder.' : 'Mantén pulsado 🎙 y responde en voz alta.');
  vigilarSilencio();
}
function vigilarSilencio() {
  clearTimeout(silencioTimer);
  if (!enLlamada || mudo || !lastReply || silencios >= ESPERAS_SILENCIO.length) return;
  silencioTimer = setTimeout(() => {
    // Escribiendo, leyendo la conversación o ya hablando: no se le interrumpe.
    if (!enLlamada || mudo || sonando || busy || grab || !$('form').hidden || !$('panel').hidden || $('stage').dataset.phase !== 'ready') return;
    void requestTutor({aviso: silencios++ ? 'pista' : 'silencio'}, false);
  }, ESPERAS_SILENCIO[silencios]);
}
$('pedirPista').onclick = () => { if (!enLlamada || busy) return; silencios = ESPERAS_SILENCIO.length; void requestTutor({aviso: 'pista'}, false); };
$('replay').onclick = () => { if (!lastReply || busy || !enLlamada) return; stop(); turno = null; encolar(lastReply, epoch); };

function stop() {
  clearTimeout(silencioTimer);
  epoch++; controller?.abort(); controller = null; detenerVoz();
  busy = false; respuestaCompleta = true; controls();
}

// ---------- Subtítulos, correcciones e ideas ----------
function limpiarTurno() {
  $('subTutor').textContent = ''; $('subTraduccion').hidden = true; $('verTraduccion').hidden = true; $('replay').hidden = true; $('reportar').hidden = true;
  $('subAlumno').hidden = true; ideas([]);
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
// · {aviso: 'silencio'|'pista'} (el alumno se quedó en blanco o pidió ayuda: no es un turno suyo)
async function requestTutor(entrada, opening = false) {
  if (busy || !config?.token || !tutor || !avatar) return;
  if (!opening) stop();
  const version = epoch;
  fraseAnterior = {version: -1, texto: ''}; // turno nuevo: sin frase anterior
  busy = true; respuestaCompleta = false; controls(); error(''); ultimoFallo = null;
  let frases = 0, final = false, transcrito = false;
  if (entrada?.texto || entrada?.audio) silencios = 0;
  turno = opening || entrada?.aviso ? null : {hist: history.length, dom: $('messages').childElementCount, corr: correcciones, oido: false, lastReply};
  if (!opening) {
    limpiarTurno();
    if (entrada?.texto) { mostrarAlumno(entrada.texto); burbuja(entrada.texto, 'mine'); history.push({rol: 'alumno', texto: entrada.texto}); }
    else if (entrada?.audio) mostrarAlumno('…');
    phase('Pensando…', 'thinking'); status('');
  } else if (enLlamada) phase('Conectando…', 'thinking');
  controller = new AbortController();
  const current = controller, timeout = setTimeout(() => current.abort(), 45000);
  vozEnLinea = avatar?.alineado ? new Map() : null; vozActiva = false;
  const conVoz = vozEnLinea ? '?voz=1' : '';
  try {
    const u = units.find(x => x.id === temaId);
    const datos = {idiomaMeta: language(), idiomaNativo: config.idiomaNativo, nivel: config.nivel, tutorId: 'avatar_' + tutor.id, historial: history.slice(-30), objetivo: config.contexto, ...(u ? {situacionId: u.id, situacion: u.nombre} : {}), ...(u && objetivoId ? {objetivoId} : {}), ...(entrada?.aviso ? {aviso: entrada.aviso} : {})};
    // Si la primera frase tarda, una muletilla («A ver…») llena el hueco como en una llamada real.
    if (enLlamada && (entrada?.texto || entrada?.audio)) setTimeout(() => { if (version === epoch && busy && !frases && !sonando && !cola.length) ponerRelleno(version); }, entrada.audio ? 1800 : 1000);
    let response;
    if (entrada?.audio) {
      const form = new FormData();
      form.append('datos', JSON.stringify(datos));
      form.append('audio', entrada.audio, entrada.tipo?.includes('mp4') ? 'turno.m4a' : 'turno.webm');
      response = await fetch(config.api + '/chat/voz' + conVoz, {method: 'POST', headers: headers(), body: form, signal: current.signal});
      // Servidor sin /chat/voz: transcribir y responder en dos pasos.
      if (response.status === 404) {
        const f2 = new FormData(); f2.append('idioma', language()); f2.append('audio', entrada.audio, entrada.tipo?.includes('mp4') ? 'turno.m4a' : 'turno.webm');
        const tr = await fetch(config.api + '/transcribir', {method: 'POST', headers: headers(), body: f2, signal: current.signal});
        if (!tr.ok) throw Error('No se pudo transcribir. Vuelve a intentarlo o escribe con ⌨️.');
        const texto = ((await tr.json()).texto || '').trim();
        if (!texto) throw Error('No te escuché bien. Mantén pulsado el micrófono mientras hablas.');
        transcrito = true; mostrarAlumno(texto); burbuja(texto, 'mine'); history.push({rol: 'alumno', texto});
        response = await fetch(config.api + '/chat' + conVoz, {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json', Accept: 'text/event-stream'}, body: JSON.stringify({...datos, historial: history.slice(-30)}), signal: current.signal});
      }
    } else {
      response = await fetch(config.api + '/chat' + conVoz, {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json', Accept: 'text/event-stream'}, body: JSON.stringify(datos), signal: current.signal});
    }
    if (!response.ok) throw Error(await bloqueoTutor(response) ?? (response.status === 401 ? 'Tu sesión ha caducado. Vuelve a iniciar sesión.' : `No se pudo conectar con el tutor (${response.status}).`));
    const reader = response.body.getReader(), decoder = new TextDecoder();
    let pending = '';
    const evento = raw => {
      if (version !== epoch) return;
      const line = raw.split('\n').find(l => l.startsWith('data: '));
      if (!line) return;
      const e = JSON.parse(line.slice(6));
      if (e.tipo === 'error') throw Error(e.data);
      if (e.tipo === 'transcripcion' && (e.data.texto || '').trim()) {
        transcrito = true;
        mostrarAlumno(e.data.texto); burbuja(e.data.texto, 'mine');
        history.push({rol: 'alumno', texto: e.data.texto});
      }
      // Cada frase terminada se muestra y se dice sin esperar al resto.
      if (e.tipo === 'frase') { $('subTutor').textContent = (frases ? $('subTutor').textContent + ' ' : '') + e.data.texto; frases++; encolar(e.data.texto, version, e.data.indice); }
      if (e.tipo === 'voz_activa') vozActiva = true;
      if (e.tipo === 'voz') { window.__marca?.('voz_llega', e.data.indice); vozDelStream(e.data.indice)?.ok(e.data); }
      if (e.tipo === 'reply' && !frases) { $('subTutor').textContent = e.data; frases++; encolar(e.data, version); }
      if (e.tipo === 'final') {
        final = true;
        const r = e.data;
        if (!frases) { frases++; encolar(r.reply, version); }
        lastReply = r.reply; $('subTutor').textContent = r.reply; $('replay').hidden = false; $('reportar').hidden = false;
        history.push({rol: 'tutor', texto: r.reply});
        const b = burbuja(r.reply);
        if (r.romanizacion) b.append(el('span', 'romanizacion', r.romanizacion));
        if (r.traduccion) {
          $('subTraduccion').textContent = r.traduccion; $('subTraduccion').hidden = true;
          $('verTraduccion').hidden = false; $('verTraduccion').textContent = 'Ver traducción';
          const d = el('details', 'traduccion'); d.append(el('summary', null, 'Ver traducción'), el('span', null, r.traduccion)); b.append(d);
        }
        const cs = r.corrections || [];
        // El tutor la dice en voz alta; por escrito queda en la conversación (💬).
        cs.forEach(correccion);
        correcciones += cs.length; actualizarContador();
        if (entrada?.aviso) ideas((r.suggestions || []).slice(0, 3));
      }
    };
    while (true) {
      const {done, value} = await reader.read();
      if (done) break;
      pending += decoder.decode(value, {stream: true});
      const parts = pending.split('\n\n'); pending = parts.pop();
      for (const p of parts) evento(p);
    }
    if (pending.trim()) evento(pending);
    if (!final) throw Error('La respuesta quedó incompleta.');
  } catch (e) {
    if (version === epoch && entrada?.aviso) console.warn('ayuda del tutor', e?.message); // sin aviso: el alumno sigue con su turno
    else if (version === epoch) {
      // Nunca dejar al alumno esperando: se explica y se ofrece reintentar.
      const msg = e.name === 'AbortError' ? 'El tutor tardó demasiado.' : (e.message || 'No se pudo responder.');
      if (entrada?.audio && !transcrito) { mostrarAlumno(''); ultimoFallo = entrada; }
      else if (!opening && !frases) ultimoFallo = {continuar: true};
      if (entrada?.texto && !frases) ultimoFallo = {continuar: true};
      // Lo que el tutor ya dijo cuenta para el siguiente turno (si no, no sabe que lo dijo).
      if (frases && !final && $('subTutor').textContent) { lastReply = $('subTutor').textContent; history.push({rol: 'tutor', texto: lastReply}); burbuja(lastReply); }
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
// Por qué no se abrió el micrófono, dicho al alumno (el nombre lo da el navegador).
function avisoMicrofono(e) {
  switch (e?.name) {
    case 'NotAllowedError': case 'SecurityError':
      return window.OneLingo ? 'OneLingo no tiene permiso del micrófono: actívalo en Ajustes › Apps › OneLingo › Permisos, o escribe con ⌨️.'
        : 'Activa el permiso del micrófono para hablar, o escribe con ⌨️.';
    case 'NotFoundError': return 'No encontramos un micrófono en este dispositivo. Puedes escribir con ⌨️.';
    case 'NotReadableError': case 'AbortError':
      return 'Otra app está usando el micrófono (una llamada o una grabadora). Ciérrala y vuelve a intentarlo, o escribe con ⌨️.';
    default: return 'No se pudo abrir el micrófono. Puedes escribir con ⌨️.';
  }
}
// Sin micrófono se pide el permiso: en la app Android, el diálogo del sistema
// (la app responde con onelingoMicrofono); en el navegador, un botón, porque su
// aviso de permiso solo aparece tras un toque.
let permisoPedido = false; // el diálogo sale solo una vez; luego, con el botón
function faltaMicrofono(e) {
  const permiso = e?.name === 'NotAllowedError' || e?.name === 'SecurityError';
  if (permiso && window.OneLingo && !permisoPedido) { permisoPedido = true; avisarApp('onelingo-avatar-permiso-microfono'); }
  error(avisoMicrofono(e), e?.name === 'NotFoundError' ? undefined : pedirPermisoMicrofono, 'Permitir micrófono');
}
function microfonoListo() {
  error(''); status('Micrófono listo: mantén pulsado 🎙 para hablar.');
  if (enLlamada && !modoVivo && vivoDisponible()) abrirVivo();
}
function pedirPermisoMicrofono() {
  if (window.OneLingo) { avisarApp('onelingo-avatar-permiso-microfono'); return; }
  pedirMicrofono().then(s => { s.getTracks().forEach(t => t.stop()); microfonoListo(); }).catch(e => error(avisoMicrofono(e)));
}
window.onelingoMicrofono = ok => ok ? microfonoListo()
  : error('OneLingo no tiene permiso del micrófono: actívalo en Ajustes › Apps › OneLingo › Permisos, o escribe con ⌨️.', pedirPermisoMicrofono, 'Permitir micrófono');
// Android tarda un instante en soltar el micrófono (al cerrar la escucha en vivo
// o colgar otra app): «ocupado» se reintenta una vez antes de avisar.
function pedirMicrofono() {
  const pedir = () => navigator.mediaDevices.getUserMedia({audio: {echoCancellation: true, noiseSuppression: true, autoGainControl: true}});
  return Promise.resolve().then(pedir).catch(e => {
    if (e?.name === 'OverconstrainedError') return navigator.mediaDevices.getUserMedia({audio: true});
    if (e?.name !== 'NotReadableError' && e?.name !== 'AbortError') throw e;
    return new Promise(r => setTimeout(r, 500)).then(pedir);
  });
}
function empezarGrabacion(x) {
  if (!enLlamada || grab) return;
  if (sonando || busy) stop(); // hablar interrumpe al tutor
  const mio = {x0: x, chunks: [], cancelado: false, soltado: false};
  grab = mio; error('');
  document.body.classList.add('grabando'); document.body.classList.remove('cancelando');
  phase('Te escucho…', 'listening'); limpiarTurno(); status('');
  $('hablarTexto').textContent = 'Habla… suelta para enviar · ← desliza para cancelar';
  controls();
  pedirMicrofono().then(stream => {
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
    console.warn('micrófono', e?.name, e?.message);
    if (grab === mio) terminarSinEnviar('');
    faltaMicrofono(e);
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
  if (modoVivo) { alternarMudo(); return; } // en vivo el botón solo silencia
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
hablar.addEventListener('keydown', e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); if (modoVivo) alternarMudo(); else empezarGrabacion(0); } });
hablar.addEventListener('keyup', e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); soltar(); } });
hablar.addEventListener('click', e => e.preventDefault());

// ---------- Llamada en vivo (micrófono abierto) ----------
const palabras = s => (s.trim().match(/[\p{L}\p{N}]+/gu) || []).length + ((/[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]/u.test(s) && s.trim().length >= 3) ? 1 : 0);
// Lo que el micrófono oye mientras el tutor habla (o justo después) puede ser su propia voz.
const tutorSuena = () => sonando && !enPuerta && !audio.paused && audio.src !== SILENCIO;
const tutorAudible = () => tutorSuena() || performance.now() - finVozEn < 1200;
// ¿Es eco? Contra lo que suena (no contra frases aún sin decir). Pasado el
// audio, una respuesta de 1–2 palabras («Tea», «Yes») es del alumno aunque
// repita la pregunta.
const pareceEco = texto => tutorAudible() && (tutorSuena() || palabras(texto) > 2) && esEco(texto, `${dichoReciente} ${relleno}`);
function textoVivo() { $('hablarTexto').textContent = mudo ? 'Silenciado · toca 🎙 para hablar' : 'Micrófono abierto · habla cuando quieras'; document.body.classList.toggle('mudo', mudo); }
// El servidor no deja usar al tutor: prueba gratuita agotada (402) o modo demo cerrado (403).
async function bloqueoTutor(r) {
  if (r.status === 402) return 'Tu prueba gratuita terminó. Elige un plan para seguir practicando con el tutor.';
  if (r.status === 403 && (await r.json().catch(() => ({}))).error === 'demo_cerrado') return 'El acceso de demostración está cerrado.';
  return null;
}
async function abrirVivo(motivo = 'inicio') {
  if (vivo || modoVivo) return;
  const gen = ++genVivo;
  modoVivo = true; mudo = false; arrastre = '';
  document.body.classList.add('vivo'); textoVivo();
  try {
    const h = await abrirEscucha({
      idioma: language(),
      // Al reconectar se cuenta cómo se cortó la sesión anterior (telemetría del servidor).
      pedirToken: async cierre => {
        const r = await fetch(config.api + '/llamada/token', {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json'}, body: JSON.stringify({motivo: cierre ? 'reconexion' : motivo, cierre})});
        if (!r.ok) throw Error(r.status === 429 ? 'Demasiadas llamadas seguidas.' : await bloqueoTutor(r) ?? `Sin escucha en vivo (${r.status}).`);
        return r.json();
      },
      onParcial: oirParcial, onFinal: oirFinal,
      onEstado: (e, detalle) => {
        if (gen !== genVivo) return;
        if (e === 'reconectando') status('Reconectando el micrófono…');
        if (e === 'escuchando' && $('stage').dataset.phase === 'ready') finTurno(); // quita «Reconectando…»
        if (e === 'error') { console.warn('escucha en vivo', detalle); volverAPulsar('Se cortó la escucha en vivo: mantén pulsado 🎙 para hablar.'); }
      },
    });
    // Se colgó, se cerró o se volvió a abrir mientras esta apertura esperaba: se descarta.
    if (gen !== genVivo || !modoVivo || !enLlamada) { h.cerrar(); return; }
    vivo = h; vivo.silenciar(mudo);
  } catch (e) {
    console.warn('escucha en vivo', e?.name, e?.message);
    if (gen !== genVivo || !modoVivo || !enLlamada) return;
    volverAPulsar(/Demasiadas/.test(e?.message) ? 'La escucha en vivo vuelve en unos minutos: mientras, mantén pulsado 🎙 para hablar.' : 'Mantén pulsado 🎙 para hablar.');
    if (e instanceof DOMException) faltaMicrofono(e); // fallo del micrófono, no del servidor
  }
}
function cerrarVivo() {
  const h = vivo; vivo = null; modoVivo = false; arrastre = ''; genVivo++;
  document.body.classList.remove('vivo', 'mudo');
  $('hablarTexto').textContent = 'Mantén pulsado para hablar';
  h?.cerrar();
}
function volverAPulsar(pista) { cerrarVivo(); if (enLlamada) { status(pista); controls(); } }
function alternarMudo() { mudo = !mudo; vivo?.silenciar(mudo); textoVivo(); if (mudo) mostrarAlumno(''); if (!sonando && !busy) finTurno(); }
// Mientras el alumno habla: se muestra lo que va diciendo y, si el tutor
// estaba hablando o pensando, se le interrumpe.
function oirParcial(texto) {
  if (!enLlamada || mudo || !texto.trim()) return;
  if (pareceEco(texto)) return;
  clearTimeout(silencioTimer); ultimoParcialEn = performance.now();
  if (noSeOye() || (busy && !sonando && !turno?.oido)) {
    // Seguía hablando tras una pausa: la respuesta en preparación se descarta y
    // lo ya dicho se junta con lo nuevo.
    recuperarTurno(); stop();
  } else if (sonando || busy) {
    // Ya oyó al tutor: una palabra suelta («yeah», «mm») no lo corta.
    if (palabras(texto) < 2) return;
    stop();
  }
  // Si lo nuevo no llega a cerrarse (ruido, una tos), se responde a lo que ya
  // había; cada parcial lo aplaza (si no, cortaba a mitad de una frase larga).
  if (arrastre) {
    clearTimeout(rescate);
    rescate = setTimeout(() => { if (arrastre && !busy && enLlamada && !mudo) { const t = arrastre; arrastre = ''; void requestTutor({texto: t}, false); } }, 3500);
  }
  if ($('stage').dataset.phase !== 'listening') { phase('Te escucho…', 'listening'); limpiarTurno(); status(''); }
  mostrarAlumno((arrastre ? arrastre + ' ' : '') + texto);
}
function oirFinal(texto) {
  if (!enLlamada || mudo) return;
  if (pareceEco(texto)) return;
  // Asentir («yeah», «mm-hm») mientras habla el tutor no es un turno.
  if (tutorSuena() && (!turno || turno.oido) && palabras(texto) < 2) return;
  if (noSeOye() || (busy && !sonando && !turno?.oido)) recuperarTurno();
  clearTimeout(rescate);
  const todo = (arrastre ? arrastre + ' ' : '') + texto; arrastre = '';
  stop();
  retenerHasta = performance.now() + paciencia(todo);
  void requestTutor({texto: todo}, false);
}
// Cada cuadro: el halo late con la voz del alumno; «Te escucho» aparece en cuanto
// suena su voz (sin esperar a la transcripción) y, si arranca mientras el tutor
// habla, el tutor baja la voz al instante. El eco del propio tutor (si el
// teléfono no lo cancela del todo) se estima mientras habla para no confundirlo.
let nivelSuave = 0, vozDesde = 0, calmaDesde = 0, ecoMedio = 0;
function animarNivel() {
  requestAnimationFrame(animarNivel);
  const n = enLlamada && vivo && !mudo ? vivo.nivel() : 0;
  nivelSuave = Math.max(n, nivelSuave * 0.86);
  document.body.style.setProperty('--nivel', Math.min(1, nivelSuave * 10).toFixed(3));
  const ahora = performance.now();
  // Solo con el tutor sonando de verdad se descuenta su eco (mientras se
  // descarga su voz, lo que entra por el micrófono es el alumno).
  const audible = sonando && !enPuerta && !audio.paused && !audio.ended && audio.src !== SILENCIO;
  const umbral = Math.max(0.035, audible ? ecoMedio * 3 : 0);
  if (n > umbral) { vozDesde ||= ahora; calmaDesde = 0; ultimaVoz = ahora; } else { vozDesde = 0; calmaDesde ||= ahora; }
  const hablando = vozDesde && ahora - vozDesde > 160;
  if (audible) {
    if (!hablando && audio.volume === 1) ecoMedio = ecoMedio * 0.97 + n * 0.03;
    if (hablando) audio.volume = 0.3;
    else if (audio.volume < 1 && ahora - calmaDesde > 500) audio.volume = 1;
  } else {
    if (audio.volume < 1) audio.volume = 1;
    // Retomó antes de que el tutor se oyera: «Te escucho» (el subtítulo se
    // queda por si solo fue una tos y el tutor sigue).
    if (hablando && enPuerta && $('stage').dataset.phase !== 'listening') phase('Te escucho…', 'listening');
    if (hablando && !busy && $('stage').dataset.phase === 'ready') { clearTimeout(silencioTimer); phase('Te escucho…', 'listening'); status(''); }
    // Era ruido (una tos, un golpe) y no llegó nada que transcribir: vuelve su turno.
    if ($('stage').dataset.phase === 'listening' && !busy && !sonando && !cola.length && !arrastre && !grab
      && ahora - Math.max(ultimaVoz, ultimoParcialEn) > 2500) finTurno();
  }
}
requestAnimationFrame(animarNivel);
// El alumno siguió hablando antes de oír al tutor: lo que dijo se junta con lo
// nuevo y la respuesta que no llegó a sonar se borra (historial, burbujas y
// correcciones), como si no hubiera existido.
function recuperarTurno() {
  if (!turno || turno.oido || history[turno.hist]?.rol !== 'alumno') return;
  arrastre = history[turno.hist].texto;
  history.length = turno.hist;
  const m = $('messages');
  while (m.childElementCount > turno.dom) m.lastElementChild.remove();
  correcciones = turno.corr; actualizarContador();
  // Ni «Repetir» ni el subtítulo deben quedarse con la respuesta descartada.
  lastReply = turno.lastReply; limpiarTurno();
  turno = null;
}

// ---------- Hoja inferior: conversación y temas ----------
function abrirPanel(cual) {
  $('panel').hidden = false;
  $('messages').hidden = cual !== 'conversacion';
  $('temas').hidden = cual !== 'temas';
  $('reporte').hidden = cual !== 'reporte';
  $('panelTitulo').textContent = cual === 'temas' ? '¿Qué quieres practicar?' : cual === 'reporte' ? 'Reportar respuesta' : 'Conversación';
  if (cual === 'temas') pintarTemas();
  else if (cual === 'conversacion') $('messages').lastElementChild?.scrollIntoView({block: 'end'});
}
// ---------- Reportar la última respuesta del tutor (política de IA de Google Play) ----------
// Misma API que la app (POST /reportes-ia) con el token de la sesión.
const MOTIVOS = [['ofensivo', 'Ofensiva'], ['incorrecto', 'Incorrecta'], ['inapropiado', 'Inapropiada'], ['otro', 'Otro motivo']];
let reporte = null;
function abrirReporte() {
  if (!lastReply || !config?.token) return;
  reporte = {texto: lastReply, motivo: null, enviando: false};
  $('reporteCita').textContent = lastReply;
  $('reporteComentario').value = ''; $('reporteAviso').textContent = '';
  $('reporte').querySelector('.reporte-gracias')?.remove();
  for (const n of $('reporte').children) n.hidden = false;
  const box = $('reporteMotivos'); box.replaceChildren();
  for (const [id, nombre] of MOTIVOS) {
    const b = el('button', null, nombre); b.type = 'button'; b.setAttribute('aria-pressed', 'false');
    b.onclick = () => { reporte.motivo = id; for (const x of box.children) x.setAttribute('aria-pressed', String(x === b)); $('reporteEnviar').disabled = false; };
    box.append(b);
  }
  $('reporteEnviar').disabled = true; $('reporteEnviar').textContent = 'Enviar reporte';
  abrirPanel('reporte');
}
$('reportar').onclick = abrirReporte;
$('reporte').onsubmit = async e => {
  e.preventDefault();
  if (!reporte?.motivo || reporte.enviando) return;
  reporte.enviando = true; $('reporteEnviar').disabled = true; $('reporteEnviar').textContent = 'Enviando…'; $('reporteAviso').textContent = '';
  const u = units.find(x => x.id === temaId);
  const cuerpo = {origen: 'llamada', texto: reporte.texto.slice(0, 2000), motivo: reporte.motivo, comentario: $('reporteComentario').value.trim().slice(0, 500),
    contexto: {idioma: language(), ...(tutor ? {tutorId: 'avatar_' + tutor.id} : {}), ...(u ? {situacion: String(u.nombre ?? u.id).slice(0, 200)} : {})}};
  try {
    const r = await fetch(config.api + '/reportes-ia', {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json'}, body: JSON.stringify(cuerpo)});
    if (!r.ok) throw new Error(r.status === 429 ? 'Enviaste muchos reportes. Inténtalo de nuevo más tarde.' : 'No se pudo enviar el reporte. Inténtalo de nuevo.');
    for (const n of $('reporte').children) n.hidden = true;
    $('reporte').append(el('p', 'reporte-gracias', 'Gracias, lo revisaremos.'));
    const enviado = reporte; setTimeout(() => { if (reporte === enviado) $('panel').hidden = true; }, 1800);
  } catch (x) {
    $('reporteAviso').textContent = x instanceof TypeError ? 'No se pudo conectar. Revisa tu conexión.' : x.message;
    reporte.enviando = false; $('reporteEnviar').disabled = false; $('reporteEnviar').textContent = 'Enviar reporte';
  }
};
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
// En segundo plano (o en otra pestaña de la app) ni se escucha ni habla el
// tutor; al volver, el micrófono en vivo se reabre.
let pausadaPorApp = false;
function pausarLlamada() {
  if (grab) cancelarGrabacion();
  if (modoVivo) { cerrarVivo(); document.body.dataset.reabrirVivo = '1'; }
  if (enLlamada) stop();
}
function reanudarLlamada() {
  if (document.hidden || pausadaPorApp || !enLlamada) return;
  mantenerPantalla();
  if (document.body.dataset.reabrirVivo) { delete document.body.dataset.reabrirVivo; abrirVivo('visible'); }
  // Se pausó durante el saludo: se vuelve a saludar.
  if (!lastReply && !busy && !history.some(t => t.rol === 'alumno')) { void requestTutor(null, true); return; }
  finTurno();
}
document.addEventListener('visibilitychange', () => document.hidden ? pausarLlamada() : reanudarLlamada());
window.onelingoPausa = () => { pausadaPorApp = true; pausarLlamada(); };
window.onelingoReanudar = () => { pausadaPorApp = false; reanudarLlamada(); };
controls();
