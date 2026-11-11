// Videollamada con un tutor (Lumo 2D o tutores 3D) como una llamada real:
// llamada entrante / «Contestar», el tutor empieza hablando, mantener pulsado
// para hablar (como un audio de WhatsApp), subtítulos y colgar con resumen.
import {createAvatar} from './avatar.js?v=27';
import {createLumo} from './lumo.js?v=27';
import {envolvente, muestraEn, BANDAS_TIPICAS} from './voz.js?v=27';
import {createAvatarTH} from './avatar-th.js?v=14';
import {lineaDeVisemas, alineacionEstimada} from './visemas.js?v=1';
import {abrirEscucha, esEco, escrituraAjena, vivoDisponible} from './vivo.js?v=6';
import {t, nombreTema, traducirPagina} from './textos.js?v=2';

const $ = id => document.getElementById(id), audio = $('audio');
// Idioma de la interfaz (?ui=en|es, el de la app): antes de cargar nada.
traducirPagina();
// Todo lo que usa la conversación se carga ANTES de avisar a la app: si el
// aviso llegaba antes que topics.json, el saludo fallaba en silencio.
const [roster, units] = await Promise.all([
  fetch('./roster.json?v=34').then(r => r.json()),
  fetch('./topics.json?v=27').then(r => r.json()),
]);

let config = null, tutor = null, avatar = null, history = [], epoch = 0, selection = 0, busy = false, controller = null;
// Partes de la última respuesta con su idioma (las explicaciones en el idioma del alumno suenan con su pronunciación).
let ultimasPartes = {texto: '', partes: []};
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
let reintentoVivo = null, reintentosVivo = 0, errorVivo = '';
// Datos técnicos de la llamada para su informe (se mandan al colgar con el resumen).
const statsVacias = () => ({turnosVivo: 0, turnosPulsar: 0, cortesVivo: 0, reintentosVivo: 0, frasesTutor: 0, frasesRespaldo: 0, avisos: {}, ultimoErrorVivo: ''});
let stats = statsVacias();
const contarFrase = respaldo => { stats.frasesTutor++; if (respaldo) stats.frasesRespaldo++; };
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
// Si el alumno se queda en blanco, el tutor toma la iniciativa hablando (como un
// profesor): a los ~4 s le pregunta de qué quiere hablar con temas y una frase
// modelo (o, en una situación o una repetición, se lo pone más fácil); si sigue
// callado, una pista. Luego espera. Antes eran 9 s y el tutor elegía el tema.
const ESPERAS_SILENCIO = [4000, 9000], AVISOS_SILENCIO = ['iniciativa', 'pista'];
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
const language = () => config?.idiomaMeta || 'en', languageName = () => t(languages[language()] || languages.en);
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
const headers = () => ({Authorization: `Bearer ${config.token}`});
const conLimite = (p, ms) => Promise.race([p, new Promise(r => setTimeout(r, ms))]);

const INSIGNIAS = {speaking: t('Hablando'), 'voice-loading': t('Pensando…'), thinking: t('Pensando…'), listening: t('Te escucho'), ready: t('Tu turno')};
function phase(label, value = 'ready') {
  $('state').textContent = label; $('stage').dataset.phase = value;
  const i = $('insignia'); i.textContent = enLlamada ? (value === 'ready' && mudo ? t('Micrófono en silencio') : INSIGNIAS[value] ?? '') : ''; i.hidden = !i.textContent;
  $('pedirPista').hidden = !(enLlamada && value === 'ready');
}
function status(t) { $('status').textContent = t; }
function error(e, reintentar, etiqueta = t('Reintentar')) {
  const box = $('error'); box.replaceChildren();
  if (!e) return;
  // Los mensajes de los módulos (lumo.js, avatar.js) también se traducen.
  box.append(t(e?.message || String(e)));
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
  pintarExplica();
}

// ---------- Idioma de las explicaciones ----------
// El porqué de las correcciones, la regla y las pistas: en el idioma del alumno
// (el tutor las dice en su idioma, con la misma voz) o en el de la llamada.
// Por defecto en el suyo hasta el nivel 5; la elección se recuerda por idioma.
const claveExplica = () => `onelingo.explica.${language()}`;
function explica() {
  if (!config || !config.idiomaNativo || config.idiomaNativo === language()) return 'meta';
  try { const v = localStorage.getItem(claveExplica()); if (v === 'nativo' || v === 'meta') return v; } catch { /* sin almacenamiento */ }
  return (config.nivel || 1) <= 5 ? 'nativo' : 'meta';
}
function pintarExplica() {
  const b = $('explica'), propio = config?.idiomaNativo;
  b.hidden = !config || !propio || propio === language();
  if (b.hidden) return;
  const idioma = explicaActual() === 'nativo' ? t(languages[propio] || propio) : languageName();
  $('explicaNombre').textContent = t('Explica en {idioma}', {idioma});
  b.setAttribute('aria-label', t('El tutor te explica en {idioma}. Toca para cambiar.', {idioma}));
}
$('explica').onclick = () => {
  const nuevo = explicaActual() === 'nativo' ? 'meta' : 'nativo';
  try { localStorage.setItem(claveExplica(), nuevo); } catch { /* solo esta sesión */ }
  sesionExplica = nuevo; pintarExplica();
  const idioma = nuevo === 'nativo' ? t(languages[config.idiomaNativo] || config.idiomaNativo) : languageName();
  status(t('Desde la próxima respuesta, el tutor te explica en {idioma}.', {idioma}));
};
// Sin localStorage la elección dura lo que la página.
let sesionExplica = null;
const explicaActual = () => sesionExplica || explica();

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
    if (temaInicial) { temaId = temaInicial.id; objetivoId = c.objetivoId || null; $('temaNombre').textContent = nombreTema(temaInicial); }
    $('authStatus').textContent = c.token ? t('Nivel {nivel} · tutores para practicar {idioma}', {nivel: c.nivel, idioma: languageName()}) : t('Inicia sesión en OneLingo para conversar con los tutores.');
    $('text').placeholder = t('Escribe en {idioma}…', {idioma: languageName()});
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
  for (const tu of ordered) {
    const b = el('button', 'tutor'), portrait = el('div', 'portrait'), img = el('img');
    img.src = tu.portrait; img.alt = t('Retrato de {nombre}', {nombre: tu.name}); img.loading = 'lazy'; portrait.append(img);
    b.append(portrait, el('strong', null, tu.name), el('small', null, tu.tipo === '2d' ? t('Tu compañero de OneLingo') : t('Tutor de {idioma} · {estilo}', {idioma: languageName(), estilo: tu.voice_direction.split(' · ')[2] || 'conversacional'})));
    if (recommendations.includes(tu.id)) b.append(el('span', 'recommended', t('Recomendado')));
    b.onclick = () => select(tu);
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
  phase(t('Inicia sesión para conversar'), 'error');
  status(t('Inicia sesión en OneLingo para conversar con tu tutor.'));
  return true;
}

async function select(tu) {
  colgar(false);
  document.body.classList.remove('puede-llamar');
  avatar?.dispose(); avatar = null; tutor = tu; history = []; lastReply = ''; correcciones = 0;
  limpiarTurno(); $('messages').replaceChildren(); actualizarContador();
  $('name').textContent = tu.name;
  $('selection').hidden = true; $('session').hidden = false;
  $('loading').hidden = false; $('loading').textContent = t('Cargando a {nombre}…', {nombre: tu.name});
  error(''); phase(t('Preparando…'), 'loading'); controls();
  const version = ++selection;
  try {
    avatar = tu.tipo === '2d' ? createLumo($('stage'), fuente) : tu.tipo === 'th' ? createAvatarTH($('stage'), fuente, tu.th) : createAvatar($('stage'), fuente);
    // El saludo (texto y voz) se prepara mientras carga el personaje: al
    // contestar, el tutor habla al instante.
    const carga = avatar.load(tu.model, e => { if (version === selection && e.total) $('loading').textContent = t('Cargando a {nombre} · {pct} %', {nombre: tu.name, pct: Math.round(e.loaded / e.total * 100)}); });
    if (!sinSesion()) void requestTutor(null, true);
    await carga;
    if (version !== selection) return;
    $('loading').hidden = true; controls();
    if (!sinSesion()) void autoiniciar(version);
  } catch (e) {
    if (version !== selection) return;
    avatar?.dispose(); avatar = null; error(e); status(t('No se pudo cargar el tutor. Regresa y vuelve a intentarlo.')); controls();
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
  phase(t('Te está llamando…'), 'ringing');
  $('llamaTexto').textContent = t('{nombre} te está llamando…', {nombre: tutor.name});
  $('llamarTexto').textContent = t('Contestar');
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
  enLlamada = true; inicioLlamada = Date.now(); stats = statsVacias(); iniciarReloj(); controls(); error('');
  mantenerPantalla();
  phase(t('Conectando…'), 'thinking');
  vigilarConexion(epoch);
  setTimeout(calentarRellenos, 4000);
  if (cola.length) siguiente(epoch);
  else if (respuestaCompleta && !busy) { if (lastReply) decirUltima(epoch); else void requestTutor(null, true); }
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
      colgar(false); phase(t('No se pudo conectar'), 'error');
      $('llamaTexto').textContent = t('No se pudo conectar'); $('llamarTexto').textContent = t('Volver a llamar');
      error(t('El tutor no responde. Revisa tu conexión y vuelve a llamar.'));
      return;
    }
    const saludo = !history.some(t => t.rol === 'alumno');
    stop(); phase(t('Conectando…'), 'thinking'); status(t('Reconectando con {nombre}…', {nombre: tutor.name}));
    if (lastReply && saludo) decirUltima(epoch); else void requestTutor(saludo ? null : {continuar: true}, saludo);
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
    if ($('stage').dataset.phase === 'ready') $('state').textContent = t('En llamada · {tiempo}', {tiempo: $('stage').dataset.reloj});
  }, 1000);
}

function colgar(resumen = true) {
  const habia = enLlamada;
  stop();
  if (grab) cancelarGrabacion();
  cerrarVivo();
  enLlamada = false; clearInterval(reloj); clearTimeout(reintentoVivo); reintentosVivo = 0; errorVivo = ''; controls();
  turno = null; arrastre = ''; clearTimeout(rescate);
  bloqueoPantalla?.release().catch(() => {}); bloqueoPantalla = null;
  $('form').hidden = true; mostrarCorreccion(null);
  if (habia && tutor) {
    document.body.classList.add('puede-llamar');
    phase(t('Llamada terminada'), 'ready');
    $('llamaTexto').textContent = t('Llamada terminada');
    $('llamarTexto').textContent = t('Volver a llamar');
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
function urlVoz(text, previo = '', ruta = '/voz/stream', habla = '') {
  const url = new URL(config.api + ruta);
  url.search = new URLSearchParams({texto: text, idioma: language(), voz: 'avatar_' + tutor.id, ...(previo ? {previo} : {}), ...(habla ? {habla} : {})});
  return url;
}
let fraseAnterior = {version: -1, texto: '', habla: ''};
// Voz que el servidor manda dentro de la respuesta (evento `voz`), por índice de frase.
let vozEnLinea = null;
let vozActiva = false; // el servidor confirmó que manda la voz en el stream
function vozDelStream(indice) {
  if (!vozEnLinea || !vozActiva || indice == null) return null;
  let item = vozEnLinea.get(indice);
  if (!item) { let ok; const p = new Promise(r => { ok = r; }); item = {p, ok}; vozEnLinea.set(indice, item); }
  return item;
}
const fraseAlineada = (d, text, habla) => ({url: URL.createObjectURL(new Blob([Uint8Array.from(atob(d.audio), c => c.charCodeAt(0))], {type: 'audio/mpeg'})), env: null, texto: text, habla,
  linea: d.alineacion ? lineaDeVisemas(d.alineacion, habla || language()) : null});
// `habla`: la frase es una explicación en el idioma del alumno (misma voz, su pronunciación).
function prepararFrase(text, version, indice, habla = '') {
  const previo = fraseAnterior.version === version && fraseAnterior.habla === habla ? fraseAnterior.texto : '';
  fraseAnterior = {version, texto: text, habla};
  // Con visemas: el MP3 llega junto con el tiempo de cada letra.
  if (avatar?.alineado) {
    const pedir = () => fetch(urlVoz(text, previo, '/voz/alineada', habla), {headers: headers(), signal: senalVoz()})
      .then(r => { if (!r.ok) throw Error(t('La voz no está disponible ({estado}).', {estado: r.status})); return r.json(); });
    const delStream = vozDelStream(indice);
    // Si la voz no llega en el stream (servidor viejo o fallo), se pide aparte.
    const datos = delStream ? conLimite(delStream.p, 4000).then(d => d?.audio ? d : pedir()) : pedir();
    return datos.then(d => { contarFrase(d?.respaldo); return fraseAlineada(d, text, habla); });
  }
  return fetch(urlVoz(text, previo, '/voz/stream', habla), {headers: headers(), signal: senalVoz()})
    .then(r => { if (!r.ok) throw Error(t('La voz no está disponible ({estado}).', {estado: r.status})); contarFrase(r.headers.get('x-voz-origen') === 'respaldo'); return r.arrayBuffer(); })
    .then(async bytes => ({url: URL.createObjectURL(new Blob([bytes], {type: 'audio/mpeg'})), env: await envolvente(bytes).catch(() => null)}));
}
// Cada frase se descarga en cuanto llega (en paralelo a la que suena). Antes
// de contestar solo se descargan: suenan al empezar la llamada.
// Vuelve a decir la última respuesta frase a frase, cada una en su idioma.
function decirUltima(version) {
  if (ultimasPartes.texto === lastReply && ultimasPartes.partes.length) for (const p of ultimasPartes.partes) encolar(p.texto, version, undefined, false, p.habla);
  else encolar(lastReply, version);
}
function encolar(text, version, indice, esRelleno = false, habla = '') {
  const listo = prepararFrase(text, version, indice, habla);
  listo.catch(() => {});
  cola.push({text, listo, relleno: esRelleno});
  if (enLlamada && !sonando) siguiente(version);
}
async function siguiente(version) {
  const item = cola.shift();
  if (!item || version !== epoch) return;
  sonando = true; enPuerta = true;
  if ($('stage').dataset.phase !== 'speaking') phase(t('Preparando voz…'), 'voice-loading');
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
    if (f.texto && !f.linea) audio.addEventListener('loadedmetadata', () => { if (urlActual === f.url && isFinite(audio.duration)) lineaActual = lineaDeVisemas(alineacionEstimada(f.texto, audio.duration), f.habla || language()); }, {once: true});
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
  phase(t('Hablando…'), 'speaking');
  status(t(modoVivo ? (mudo ? 'Micrófono silenciado: toca 🎙 para hablar.' : 'Puedes interrumpir hablando.') : 'Mantén pulsado 🎙 para interrumpir y responder.'));
};
audio.onended = () => { if (audio.src !== SILENCIO) terminarFrase(itemActual, true); };
audio.onerror = () => {
  if (!audio.getAttribute('src') || audio.src === SILENCIO || !sonando) return;
  terminarFrase(itemActual, false);
};
// El tutor terminó y no quedan frases por llegar: turno del alumno.
function finTurno() {
  if (!enLlamada || sonando || cola.length || !respuestaCompleta || busy || grab) return;
  phase(t('En llamada · {tiempo}', {tiempo: $('stage').dataset.reloj || '00:00'}), 'ready');
  if (modoVivo) status(t(mudo ? 'Micrófono silenciado: toca 🎙 para hablar.' : 'Tu turno: habla cuando quieras.'));
  else status(t(history.some(h => h.rol === 'alumno') ? 'Tu turno: mantén pulsado 🎙 para responder.' : 'Mantén pulsado 🎙 y responde en voz alta.'));
  vigilarSilencio();
}
function vigilarSilencio() {
  clearTimeout(silencioTimer);
  if (!enLlamada || mudo || !lastReply || silencios >= ESPERAS_SILENCIO.length) return;
  silencioTimer = setTimeout(() => {
    // Escribiendo, leyendo la conversación o ya hablando: no se le interrumpe.
    if (!enLlamada || mudo || sonando || busy || grab || !$('form').hidden || !$('panel').hidden || $('stage').dataset.phase !== 'ready') return;
    void requestTutor({aviso: AVISOS_SILENCIO[silencios++]}, false);
  }, ESPERAS_SILENCIO[silencios]);
}
$('pedirPista').onclick = () => { if (!enLlamada || busy) return; silencios = ESPERAS_SILENCIO.length; void requestTutor({aviso: 'pista'}, false); };
$('replay').onclick = () => { if (!lastReply || busy || !enLlamada) return; stop(); turno = null; decirUltima(epoch); };

function stop() {
  clearTimeout(silencioTimer);
  // Si el tutor ya dio su respuesta entera, la petición sigue en segundo plano:
  // así llegan su corrección escrita y el servidor guarda el turno (sin guardar,
  // la llamada siguiente no sabía qué errores ya se habían corregido).
  epoch++; if (!controller?.respondida) controller?.abort(); controller = null; detenerVoz();
  busy = false; respuestaCompleta = true; controls();
}

// ---------- Subtítulos, correcciones e ideas ----------
function limpiarTurno() {
  $('subTutor').textContent = ''; $('subTraduccion').hidden = true; $('verTraduccion').hidden = true; $('replay').hidden = true; $('reportar').hidden = true;
  $('subAlumno').hidden = true; ideas([]);
}
// La corrección del turno, en pantalla y no solo en 💬: se queda mientras el
// alumno repite la frase y se va cuando el tutor vuelve a hablar.
function mostrarCorreccion(c) {
  const box = $('subCorreccion'); box.replaceChildren(); box.hidden = !c;
  if (!c) return;
  const fila = el('div', 'correccion-fila');
  fila.append(el('s', null, c.original), el('span', 'flecha', '→'), el('strong', null, c.correcto));
  box.append(fila);
  if (c.explicacion) box.append(el('small', null, c.explicacion));
}
function mostrarAlumno(texto) { $('subAlumno').textContent = texto; $('subAlumno').hidden = !texto; }
function burbuja(text, kind = '') { const e = el('div', 'bubble ' + kind, text); $('messages').append(e); return e; }
function actualizarContador() { $('contador').hidden = !correcciones; $('contador').textContent = correcciones; }
function correccion(c, despues) {
  const card = el('div', 'correccion'), fila = el('div', 'correccion-fila');
  fila.append(el('s', null, c.original), el('span', 'flecha', '→'), el('strong', null, c.correcto));
  card.append(el('span', 'correccion-titulo', t('Corrección')), fila);
  if (c.explicacion) card.append(el('small', null, c.explicacion));
  if (despues) despues.after(card); else $('messages').append(card);
  return card;
}
// Ideas para responder: tocar una la envía como respuesta.
function ideas(lista) {
  const box = $('ideas'); box.replaceChildren(); box.hidden = !lista.length;
  if (!lista.length) return;
  box.append(el('span', 'ideas-titulo', t('Puedes decir')));
  for (const s of lista) { const b = el('button', 'idea', s); b.type = 'button'; b.onclick = () => requestTutor({texto: s}, false); box.append(b); }
}
$('verTraduccion').onclick = () => { const sub = $('subTraduccion'); sub.hidden = !sub.hidden; $('verTraduccion').textContent = t(sub.hidden ? 'Ver traducción' : 'Ocultar traducción'); };

// ---------- Turno: texto o voz → respuesta por frases ----------
// entrada: null (saludo) · {texto} · {audio, tipo} · {continuar: true} (reintento sin turno nuevo)
// · {aviso: 'iniciativa'|'pista'} (el alumno se quedó en blanco o pidió ayuda: no es un turno suyo)
async function requestTutor(entrada, opening = false) {
  if (busy || !config?.token || !tutor || !avatar) return;
  if (!opening) stop();
  const version = epoch;
  fraseAnterior = {version: -1, texto: ''}; // turno nuevo: sin frase anterior
  busy = true; respuestaCompleta = false; controls(); error(''); ultimoFallo = null;
  let frases = 0, final = false, transcrito = false, burbujaTutor = null, turnoTutor = null, espera = null;
  const partes = [];
  if (entrada?.texto || entrada?.audio) silencios = 0;
  if (entrada?.aviso) stats.avisos[entrada.aviso] = (stats.avisos[entrada.aviso] || 0) + 1;
  turno = opening || entrada?.aviso ? null : {hist: history.length, dom: $('messages').childElementCount, corr: correcciones, oido: false, lastReply};
  if (!opening) {
    limpiarTurno();
    if (entrada?.texto) { mostrarAlumno(entrada.texto); burbuja(entrada.texto, 'mine'); history.push({rol: 'alumno', texto: entrada.texto}); }
    else if (entrada?.audio) mostrarAlumno('…');
    phase(t('Pensando…'), 'thinking'); status('');
  } else if (enLlamada) phase(t('Conectando…'), 'thinking');
  controller = new AbortController();
  const current = controller, timeout = setTimeout(() => current.abort(), 45000);
  vozEnLinea = avatar?.alineado ? new Map() : null; vozActiva = false;
  const conVoz = vozEnLinea ? '?voz=1' : '';
  try {
    const u = units.find(x => x.id === temaId);
    const datos = {idiomaMeta: language(), idiomaNativo: config.idiomaNativo, nivel: config.nivel, tutorId: 'avatar_' + tutor.id, explica: explicaActual(), historial: history.slice(-30), objetivo: config.contexto, ...(u ? {situacionId: u.id, situacion: u.nombre} : {}), ...(u && objetivoId ? {objetivoId} : {}), ...(entrada?.aviso ? {aviso: entrada.aviso} : {})};
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
        const f2 = new FormData(); f2.append('idioma', language()); if (config.idiomaNativo) f2.append('nativo', config.idiomaNativo); f2.append('audio', entrada.audio, entrada.tipo?.includes('mp4') ? 'turno.m4a' : 'turno.webm');
        const tr = await fetch(config.api + '/transcribir', {method: 'POST', headers: headers(), body: f2, signal: current.signal});
        if (!tr.ok) throw Error(t('No se pudo transcribir. Vuelve a intentarlo o escribe con ⌨️.'));
        const texto = ((await tr.json()).texto || '').trim();
        if (!texto) throw Error(t('No te escuché bien. Mantén pulsado el micrófono mientras hablas.'));
        transcrito = true; mostrarAlumno(texto); burbuja(texto, 'mine'); history.push({rol: 'alumno', texto});
        response = await fetch(config.api + '/chat' + conVoz, {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json', Accept: 'text/event-stream'}, body: JSON.stringify({...datos, historial: history.slice(-30)}), signal: current.signal});
      }
    } else {
      response = await fetch(config.api + '/chat' + conVoz, {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json', Accept: 'text/event-stream'}, body: JSON.stringify(datos), signal: current.signal});
    }
    if (!response.ok) throw Error(await bloqueoTutor(response) ?? (response.status === 401 ? t('Tu sesión ha caducado. Vuelve a iniciar sesión.') : t('No se pudo conectar con el tutor ({estado}).', {estado: response.status})));
    const reader = response.body.getReader(), decoder = new TextDecoder();
    let pending = '';
    // Lo que el tutor dijo entra al historial en cuanto llega su texto entero
    // (evento `reply`), no al final: el final espera al corrector y, si el
    // alumno contestaba antes, el tutor olvidaba que le había pedido repetir.
    const anotarTutor = texto => {
      if (burbujaTutor) return burbujaTutor;
      lastReply = texto; ultimasPartes = {texto, partes}; turnoTutor = {rol: 'tutor', texto, ...(espera ? {espera} : {})}; history.push(turnoTutor); burbujaTutor = burbuja(texto);
      $('replay').hidden = false; $('reportar').hidden = false;
      current.respondida = true;
      return burbujaTutor;
    };
    // El alumno ya habló encima: solo se apuntan la corrección y la traducción de ese turno.
    const enSegundoPlano = e => {
      if (e.tipo !== 'final' || !burbujaTutor?.isConnected) return;
      const cs = e.data.corrections || [];
      let ref = burbujaTutor; for (const c of cs) ref = correccion(c, ref);
      correcciones += cs.length; actualizarContador();
      if (turno) { turno.dom += cs.length; turno.corr += cs.length; }
    };
    const evento = raw => {
      const line = raw.split('\n').find(l => l.startsWith('data: '));
      if (!line) return;
      const e = JSON.parse(line.slice(6));
      // Lo que el tutor espera (repetir, elegir, responder) viaja con su turno
      // en el historial: el servidor sabe así si el alumno está repitiendo.
      if (e.tipo === 'espera') { espera = e.data; if (turnoTutor) turnoTutor.espera = e.data; return; }
      if (version !== epoch) { enSegundoPlano(e); return; }
      if (e.tipo === 'error') throw Error(e.data);
      if (e.tipo === 'transcripcion' && (e.data.texto || '').trim()) {
        transcrito = true;
        mostrarAlumno(e.data.texto); burbuja(e.data.texto, 'mine');
        history.push({rol: 'alumno', texto: e.data.texto});
      }
      // Cada frase terminada se muestra y se dice sin esperar al resto.
      if (e.tipo === 'frase') { if (!frases) mostrarCorreccion(null); $('subTutor').textContent = (frases ? $('subTutor').textContent + ' ' : '') + e.data.texto; frases++; partes.push({texto: e.data.texto, habla: e.data.habla || ''}); encolar(e.data.texto, version, e.data.indice, false, e.data.habla || ''); }
      if (e.tipo === 'voz_activa') vozActiva = true;
      if (e.tipo === 'voz') { window.__marca?.('voz_llega', e.data.indice); vozDelStream(e.data.indice)?.ok(e.data); }
      if (e.tipo === 'reply') { if (!frases) { mostrarCorreccion(null); $('subTutor').textContent = e.data; frases++; encolar(e.data, version); } anotarTutor(e.data); }
      if (e.tipo === 'final') {
        final = true;
        const r = e.data;
        if (!frases) { mostrarCorreccion(null); frases++; encolar(r.reply, version); }
        $('subTutor').textContent = r.reply;
        if (r.espera) espera = r.espera;
        const b = anotarTutor(r.reply);
        if (espera) turnoTutor.espera = espera;
        if (lastReply !== r.reply) { if (ultimasPartes.texto === lastReply) ultimasPartes.texto = r.reply; lastReply = r.reply; b.textContent = r.reply; const h = history.findLastIndex(x => x.rol === 'tutor'); if (h >= 0) history[h].texto = r.reply; }
        if (r.romanizacion) b.append(el('span', 'romanizacion', r.romanizacion));
        if (r.traduccion) {
          $('subTraduccion').textContent = r.traduccion; $('subTraduccion').hidden = true;
          $('verTraduccion').hidden = false; $('verTraduccion').textContent = t('Ver traducción');
          const d = el('details', 'traduccion'); d.append(el('summary', null, t('Ver traducción')), el('span', null, r.traduccion)); b.append(d);
        }
        const cs = r.corrections || [];
        // El tutor la dice en voz alta; por escrito queda en la conversación (💬).
        let ref = b; for (const c of cs) ref = correccion(c, ref);
        correcciones += cs.length; actualizarContador();
        if (enLlamada) mostrarCorreccion(cs[0] || null);
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
    if (!final) throw Error(t('La respuesta quedó incompleta.'));
  } catch (e) {
    if (version === epoch && entrada?.aviso) console.warn('ayuda del tutor', e?.message); // sin aviso: el alumno sigue con su turno
    else if (version === epoch) {
      // Nunca dejar al alumno esperando: se explica y se ofrece reintentar.
      const msg = e.name === 'AbortError' ? t('El tutor tardó demasiado.') : t(e.message || 'No se pudo responder.');
      if (entrada?.audio && !transcrito) { mostrarAlumno(''); ultimoFallo = entrada; }
      else if (!opening && !frases) ultimoFallo = {continuar: true};
      if (entrada?.texto && !frases) ultimoFallo = {continuar: true};
      // Lo que el tutor ya dijo cuenta para el siguiente turno (si no, no sabe que lo dijo).
      if (frases && !burbujaTutor && $('subTutor').textContent) { lastReply = $('subTutor').textContent; history.push({rol: 'tutor', texto: lastReply}); burbuja(lastReply); }
      phase(t('No se pudo responder'), 'error');
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
      return t(window.OneLingo ? 'OneLingo no tiene permiso del micrófono: actívalo en Ajustes › Apps › OneLingo › Permisos, o escribe con ⌨️.'
        : 'Activa el permiso del micrófono para hablar, o escribe con ⌨️.');
    case 'NotFoundError': return t('No encontramos un micrófono en este dispositivo. Puedes escribir con ⌨️.');
    case 'NotReadableError': case 'AbortError':
      return t('Otra app está usando el micrófono (una llamada o una grabadora). Ciérrala y vuelve a intentarlo, o escribe con ⌨️.');
    default: return t('No se pudo abrir el micrófono. Puedes escribir con ⌨️.');
  }
}
// Sin micrófono se pide el permiso: en la app Android, el diálogo del sistema
// (la app responde con onelingoMicrofono); en el navegador, un botón, porque su
// aviso de permiso solo aparece tras un toque.
let permisoPedido = false; // el diálogo sale solo una vez; luego, con el botón
function faltaMicrofono(e) {
  const permiso = e?.name === 'NotAllowedError' || e?.name === 'SecurityError';
  if (permiso && window.OneLingo && !permisoPedido) { permisoPedido = true; avisarApp('onelingo-avatar-permiso-microfono'); }
  error(avisoMicrofono(e), e?.name === 'NotFoundError' ? undefined : pedirPermisoMicrofono, t('Permitir micrófono'));
}
function microfonoListo() {
  error(''); status(t('Micrófono listo: mantén pulsado 🎙 para hablar.'));
  if (enLlamada && !modoVivo && vivoDisponible()) abrirVivo();
}
function pedirPermisoMicrofono() {
  if (window.OneLingo) { avisarApp('onelingo-avatar-permiso-microfono'); return; }
  pedirMicrofono().then(s => { s.getTracks().forEach(t => t.stop()); microfonoListo(); }).catch(e => error(avisoMicrofono(e)));
}
window.onelingoMicrofono = ok => ok ? microfonoListo()
  : error(t('OneLingo no tiene permiso del micrófono: actívalo en Ajustes › Apps › OneLingo › Permisos, o escribe con ⌨️.'), pedirPermisoMicrofono, t('Permitir micrófono'));
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
  phase(t('Te escucho…'), 'listening'); limpiarTurno(); status('');
  $('hablarTexto').textContent = t('Habla… suelta para enviar · ← desliza para cancelar');
  controls();
  pedirMicrofono().then(stream => {
    if (grab !== mio || mio.soltado) { stream.getTracks().forEach(t => t.stop()); if (grab === mio) terminarSinEnviar(t('Mantén pulsado 🎙 mientras hablas.')); return; }
    mio.stream = stream;
    const mime = ['audio/webm;codecs=opus', 'audio/mp4', 'audio/webm'].find(t => MediaRecorder.isTypeSupported(t));
    mio.rec = new MediaRecorder(stream, mime ? {mimeType: mime} : {});
    mio.rec.ondataavailable = e => { if (e.data.size) mio.chunks.push(e.data); };
    mio.rec.onstop = () => finGrabacion(mio);
    mio.rec.start(250); mio.desde = performance.now();
    mio.limite = setTimeout(soltar, 60000);
    mio.cuenta = setInterval(() => { if (mio.cancelado) return; const s = Math.floor((performance.now() - mio.desde) / 1000); $('hablarTexto').textContent = t('● 0:{s} · suelta para enviar · ← desliza para cancelar', {s: String(s).padStart(2, '0')}); }, 250);
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
  $('hablarTexto').textContent = t('Mantén pulsado para hablar');
  controls(); phase(t('En llamada · {tiempo}', {tiempo: $('stage').dataset.reloj || '00:00'}), 'ready'); status(pista);
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
  if (mio.cancelado) { status(t('Mensaje cancelado.')); return; }
  if (dur < 700) { status(t('Mantén pulsado 🎙 mientras hablas y suelta al terminar.')); return; }
  const blob = new Blob(mio.chunks, {type: mio.rec.mimeType || 'audio/webm'});
  if (blob.size < 500) { status(t('No te escuché. Acércate al micrófono y vuelve a intentarlo.')); return; }
  stats.turnosPulsar++;
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
  if (grab && !grab.cancelado && grab.x0 - e.clientX > 80) { grab.cancelado = true; document.body.classList.add('cancelando'); $('hablarTexto').textContent = t('Suelta para cancelar'); }
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
// Ya callado, solo cuenta su última frase: tras «We say «I went to the park». Can you say it?»,
// el alumno que repite el modelo enseguida no es eco (antes se descartaba y la llamada se quedaba esperando).
const pareceEco = texto => tutorAudible() && (tutorSuena() || palabras(texto) > 2) && esEco(texto, `${tutorSuena() ? dichoReciente : itemActual?.text || ''} ${relleno}`);
function textoVivo() { $('hablarTexto').textContent = t(mudo ? 'Silenciado · toca 🎙 para hablar' : 'Micrófono abierto · habla cuando quieras'); document.body.classList.toggle('mudo', mudo); }
// El servidor no deja usar al tutor: prueba gratuita agotada (402) o modo demo cerrado (403).
async function bloqueoTutor(r) {
  if (r.status === 402) return t('Tu prueba gratuita terminó. Elige un plan para seguir practicando con el tutor.');
  if (r.status === 403 && (await r.json().catch(() => ({}))).error === 'demo_cerrado') return t('El acceso de demostración está cerrado.');
  return null;
}
async function abrirVivo(motivo = 'inicio') {
  if (vivo || modoVivo) return;
  const gen = ++genVivo;
  modoVivo = true; mudo = false; arrastre = '';
  document.body.classList.add('vivo'); textoVivo();
  try {
    const h = await abrirEscucha({
      // Con el idioma fijo, Scribe traducía lo dicho en el idioma del alumno
      // («¿Qué significa went?» → «What does "went" mean?»). Sin fijarlo
      // transcribe cada frase en la lengua en que se dijo, y el idioma meta
      // sale igual de bien (probado en los 10 idiomas, frases cortas incluidas).
      idioma: config.idiomaNativo && config.idiomaNativo !== language() ? undefined : language(),
      // Al reconectar se cuenta cómo se cortó la sesión anterior (telemetría del servidor).
      pedirToken: async cierre => {
        const r = await fetch(config.api + '/llamada/token', {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json'}, body: JSON.stringify({motivo: cierre ? 'reconexion' : motivo, cierre: cierre ?? (errorVivo ? {aviso: errorVivo.slice(0, 160)} : undefined)})});
        if (!r.ok) throw Error(r.status === 429 ? 'Demasiadas llamadas seguidas.' : await bloqueoTutor(r) ?? `Sin escucha en vivo (${r.status}).`);
        return r.json();
      },
      // Lo escrito en otro alfabeto (ruido que Scribe tomó por hindi, árabe…) no es del alumno.
      onParcial: tx => { if (!escrituraAjena(tx, language(), config.idiomaNativo)) oirParcial(tx); },
      onFinal: tx => { if (escrituraAjena(tx, language(), config.idiomaNativo)) console.info('escucha: descartado, otro alfabeto'); else oirFinal(tx); },
      onEstado: (e, detalle) => {
        if (gen !== genVivo) return;
        if (e === 'reconectando') status(t('Reconectando el micrófono…'));
        if (e === 'escuchando' && $('stage').dataset.phase === 'ready') finTurno(); // quita «Reconectando…»
        if (e === 'error') { console.warn('escucha en vivo', detalle); errorVivo = String(detalle ?? 'error'); stats.cortesVivo++; stats.ultimoErrorVivo = errorVivo.slice(0, 160); volverAPulsar(t('Se cortó la escucha en vivo: mantén pulsado 🎙 para hablar.'), true); }
      },
    });
    // Se colgó, se cerró o se volvió a abrir mientras esta apertura esperaba: se descarta.
    if (gen !== genVivo || !modoVivo || !enLlamada) { h.cerrar(); return; }
    vivo = h; vivo.silenciar(mudo); reintentosVivo = 0; errorVivo = '';
  } catch (e) {
    console.warn('escucha en vivo', e?.name, e?.message);
    if (gen !== genVivo || !modoVivo || !enLlamada) return;
    errorVivo = String(e?.message ?? e?.name ?? 'error');
    // Sin permiso de micrófono no se reintenta: lo arregla el alumno.
    volverAPulsar(t(/Demasiadas/.test(e?.message) ? 'La escucha en vivo vuelve en unos minutos: mientras, mantén pulsado 🎙 para hablar.' : 'Mantén pulsado 🎙 para hablar.'), !(e instanceof DOMException));
    if (e instanceof DOMException) faltaMicrofono(e); // fallo del micrófono, no del servidor
  }
}
function cerrarVivo() {
  const h = vivo; vivo = null; modoVivo = false; arrastre = ''; genVivo++;
  document.body.classList.remove('vivo', 'mudo');
  $('hablarTexto').textContent = t('Mantén pulsado para hablar');
  h?.cerrar();
}
// Si la escucha en vivo se corta (red, cuota de transcripción), la llamada
// sigue con «mantén pulsado» y vuelve sola a la escucha en vivo: antes se
// quedaba en pulsar hasta colgar.
const ESPERAS_REINTENTO_VIVO = [15000, 30000, 60000, 120000];
function volverAPulsar(pista, reintentar = false) {
  cerrarVivo();
  if (!enLlamada) return;
  status(pista); controls();
  clearTimeout(reintentoVivo);
  if (reintentar && reintentosVivo < ESPERAS_REINTENTO_VIVO.length && vivoDisponible())
    reintentoVivo = setTimeout(function intentar() {
      if (!enLlamada || modoVivo) return;
      // Mientras graba con el botón o la pestaña está oculta, se espera un poco más.
      if (grab || busy || document.hidden) { reintentoVivo = setTimeout(intentar, 5000); return; }
      stats.reintentosVivo++; abrirVivo('reintento');
    }, ESPERAS_REINTENTO_VIVO[reintentosVivo++]);
}
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
  if ($('stage').dataset.phase !== 'listening') { phase(t('Te escucho…'), 'listening'); limpiarTurno(); status(''); }
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
  stats.turnosVivo++;
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
    if (hablando && enPuerta && $('stage').dataset.phase !== 'listening') phase(t('Te escucho…'), 'listening');
    if (hablando && !busy && $('stage').dataset.phase === 'ready') { clearTimeout(silencioTimer); phase(t('Te escucho…'), 'listening'); status(''); }
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
  // No llegó a oírse: se cancela de verdad (ni tarjeta ni turno guardado).
  if (controller) controller.respondida = false;
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
  $('panelTitulo').textContent = t(cual === 'temas' ? '¿Qué quieres practicar?' : cual === 'reporte' ? 'Reportar respuesta' : 'Conversación');
  if (cual === 'temas') pintarTemas();
  else if (cual === 'conversacion') $('messages').lastElementChild?.scrollIntoView({block: 'end'});
}
// ---------- Reportar la última respuesta del tutor (política de IA de Google Play) ----------
// Misma API que la app (POST /reportes-ia) con el token de la sesión.
const MOTIVOS = [['ofensivo', t('Ofensiva')], ['incorrecto', t('Incorrecta')], ['inapropiado', t('Inapropiada')], ['otro', t('Otro motivo')]];
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
  $('reporteEnviar').disabled = true; $('reporteEnviar').textContent = t('Enviar reporte');
  abrirPanel('reporte');
}
$('reportar').onclick = abrirReporte;
$('reporte').onsubmit = async e => {
  e.preventDefault();
  if (!reporte?.motivo || reporte.enviando) return;
  reporte.enviando = true; $('reporteEnviar').disabled = true; $('reporteEnviar').textContent = t('Enviando…'); $('reporteAviso').textContent = '';
  const u = units.find(x => x.id === temaId);
  const cuerpo = {origen: 'llamada', texto: reporte.texto.slice(0, 2000), motivo: reporte.motivo, comentario: $('reporteComentario').value.trim().slice(0, 500),
    contexto: {idioma: language(), ...(tutor ? {tutorId: 'avatar_' + tutor.id} : {}), ...(u ? {situacion: String(u.nombre ?? u.id).slice(0, 200)} : {})}};
  try {
    const r = await fetch(config.api + '/reportes-ia', {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json'}, body: JSON.stringify(cuerpo)});
    if (!r.ok) throw new Error(t(r.status === 429 ? 'Enviaste muchos reportes. Inténtalo de nuevo más tarde.' : 'No se pudo enviar el reporte. Inténtalo de nuevo.'));
    for (const n of $('reporte').children) n.hidden = true;
    $('reporte').append(el('p', 'reporte-gracias', t('Gracias, lo revisaremos.')));
    const enviado = reporte; setTimeout(() => { if (reporte === enviado) $('panel').hidden = true; }, 1800);
  } catch (x) {
    $('reporteAviso').textContent = x instanceof TypeError ? t('No se pudo conectar. Revisa tu conexión.') : x.message;
    reporte.enviando = false; $('reporteEnviar').disabled = false; $('reporteEnviar').textContent = t('Enviar reporte');
  }
};
$('verConversacion').onclick = () => abrirPanel('conversacion');
$('cerrarPanel').onclick = () => { $('panel').hidden = true; };
$('tema').onclick = () => abrirPanel('temas');
function pintarTemas() {
  const box = $('temas'); box.replaceChildren();
  for (const u of [{id: null, nombre: 'Conversación libre', en: t('Conversación libre')}, ...units]) {
    const b = el('button', 'opcion-tema', nombreTema(u)); b.type = 'button';
    b.setAttribute('aria-pressed', String(u.id === temaId));
    b.onclick = () => elegirTema(u);
    box.append(b);
  }
}
// Cambiar de tema reinicia la conversación: el tutor abre la nueva situación.
function elegirTema(u) {
  $('panel').hidden = true;
  if (u.id === temaId) return;
  temaId = u.id; objetivoId = null; $('temaNombre').textContent = nombreTema(u);
  stop(); if (grab) cancelarGrabacion();
  history = []; lastReply = ''; limpiarTurno();
  burbuja(t('Nuevo tema: {tema}', {tema: nombreTema(u)}), 'feedback');
  void requestTutor(null, true);
}

// ---------- Resumen al colgar ----------
async function mostrarResumen() {
  abrirPanel('conversacion');
  const card = el('div', 'resumen'); card.append(el('h3', null, t('Resumen de la llamada')), el('p', null, t('Preparando…')));
  $('messages').append(card); card.scrollIntoView({block: 'end'});
  try {
    const r = await fetch(config.api + '/chat/resumen', {method: 'POST', headers: {...headers(), 'Content-Type': 'application/json'}, body: JSON.stringify({idiomaMeta: language(), idiomaNativo: config.idiomaNativo, nivel: config.nivel, tutorId: 'avatar_' + tutor.id, historial: history.slice(-40), explica: explicaActual(),
      tecnico: {...stats, duracionSegundos: Math.round((Date.now() - inicioLlamada) / 1000), dispositivo: /Android/i.test(navigator.userAgent) ? 'android' : /iPhone|iPad/i.test(navigator.userAgent) ? 'ios' : 'web'}})});
    if (!r.ok) throw Error(t('No se pudo preparar el resumen.'));
    const d = await r.json();
    card.replaceChildren(el('h3', null, t('Resumen de la llamada')));
    const seccion = (titulo, items) => { if (!items.length) return; card.append(el('h4', null, titulo)); const ul = el('ul'); for (const i of items) ul.append(i); card.append(ul); };
    seccion(t('Lo hiciste bien'), (d.logros || []).map(t => el('li', null, t)));
    seccion(t('Para mejorar'), (d.mejorar || []).map(m => { const li = el('li'); li.append(el('s', null, m.original), ' → ', el('strong', null, m.correcto), el('small', null, m.explicacion)); return li; }));
    seccion(t('Vocabulario de hoy'), (d.vocabulario || []).map(v => { const li = el('li'); li.append(el('strong', null, v.palabra), ' · ' + v.significado); return li; }));
    if (d.siguientePaso) card.append(el('p', 'siguiente', d.siguientePaso));
    card.append(el('p', null, t('{nombre} recordará esto en tu próxima llamada.', {nombre: tutor.name})));
    card.scrollIntoView({block: 'end'});
  } catch (e) { card.replaceChildren(el('h3', null, t('Resumen de la llamada')), el('p', null, t(e.message))); }
}

window.addEventListener('offline', () => { stop(); error(t('No hay conexión. Vuelve a intentarlo cuando tengas internet.')); });
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
