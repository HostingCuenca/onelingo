// Lumo que habla, al estilo del Video Call de Duolingo: personaje 2D con
// bocas (visemas) sobre una base sin boca, sincronizadas con la voz real.
// Nada de vídeo generado: 7 imágenes (~80 KB) y la misma interfaz que el
// avatar 3D (load/dispose), así reutiliza toda la conversación y la voz.
// Reglas de Lumo: un solo personaje y sin rebotes; solo cambia la boca y una
// leve inclinación de cabeza al «pensar» (sin ella con movimiento reducido).
import { repartir } from './voz.js?v=27';

const BOCAS = ['cerrada', 'a', 'e', 'o', 'u', 'm'];
// Tiempo mínimo de cada boca: evita parpadeos entre formas (≈ 12 cambios/s).
const BOCA_MIN_MS = 80;

/**
 * Visema según la energía por bandas ya normalizada (`repartir`):
 * graves → O/U, medios → A, agudos y sibilantes → E; casi silencio → M.
 */
export function elegirBoca(hablando, amplitud, reparto) {
  if (!hablando) return 'cerrada';
  if (amplitud < 0.06) return 'm';
  const { graves, medios } = reparto, agudos = Math.max(reparto.agudos, reparto.sibilantes);
  if (graves >= medios && graves >= agudos) return amplitud > 0.45 ? 'o' : 'u';
  if (agudos > medios * 1.1) return amplitud > 0.7 ? 'a' : 'e';
  return 'a';
}

/** `fuente.muestra()` → { hablando, amplitud, graves, medios, agudos, sibilantes }. */
export function createLumo(stage, fuente) {
  const capa = document.createElement('div');
  capa.className = 'lumo2d';
  const base = new Image();
  base.alt = 'Lumo';
  base.className = 'lumo-base';
  const bocas = Object.fromEntries(BOCAS.map(n => {
    const img = new Image();
    img.alt = '';
    img.className = 'lumo-boca';
    img.hidden = n !== 'cerrada';
    return [n, img];
  }));
  capa.append(base, ...Object.values(bocas));
  stage.prepend(capa);
  const reducido = matchMedia('(prefers-reduced-motion: reduce)').matches, depurar = new URLSearchParams(location.search).has('depurar');
  let actual = 'cerrada', cambio = 0, frameId, ultimo = 0, eliminado = false, cargado = false;

  function mostrar(n, ahora) {
    if (n === actual || ahora - cambio < BOCA_MIN_MS) return;
    bocas[actual].hidden = true; bocas[n].hidden = false; actual = n; cambio = ahora;
  }

  async function load(dir) {
    const url = n => new URL(`${dir}${n}.webp?v=lumo1`, location.href).href;
    base.src = url('base');
    for (const n of BOCAS) bocas[n].src = url(`boca-${n}`);
    // Todas cargadas antes de hablar: cambiar de boca nunca deja un hueco.
    // `decode()` solo como mejora y con límite: en pestañas ocultas (o con la
    // app en segundo plano) puede no resolverse nunca y dejaba «Cargando…».
    const cargada = img => new Promise((ok, fallo) => {
      if (img.complete && img.naturalWidth) return ok();
      img.addEventListener('load', () => ok(), { once: true });
      img.addEventListener('error', () => fallo(new Error('No se pudo cargar a Lumo. Revisa tu conexión.')), { once: true });
    }).then(() => Promise.race([img.decode().catch(() => {}), new Promise(r => setTimeout(r, 1500))]));
    await Promise.all([base, ...Object.values(bocas)].map(cargada));
    if (eliminado) return;
    cargado = true;
    stage.dataset.loaded = 'true';
  }

  function frame(ahora) {
    if (eliminado) return;
    frameId = requestAnimationFrame(frame);
    if (!cargado || ahora - ultimo < 33) return;
    ultimo = ahora;
    const m = fuente.muestra();
    mostrar(elegirBoca(m.hablando, m.amplitud, repartir(m)), ahora);
    if (depurar && m.hablando) (window.__bocas ||= []).push(actual);
    const fase = stage.dataset.phase;
    capa.classList.toggle('pensando', !reducido && !m.hablando && (fase === 'thinking' || fase === 'voice-loading'));
    stage.dataset.mouth = actual;
  }
  frameId = requestAnimationFrame(frame);

  return {
    load,
    dispose() {
      eliminado = true;
      cancelAnimationFrame(frameId);
      capa.remove();
      delete stage.dataset.loaded;
    },
  };
}
