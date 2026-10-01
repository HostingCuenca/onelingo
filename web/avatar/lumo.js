// Lumo que habla, al estilo del Video Call de Duolingo: personaje 2D con
// bocas (visemas) sobre una base sin boca, sincronizadas con el audio real.
// Nada de vídeo generado: 7 imágenes (~80 KB) y la misma interfaz que el
// avatar 3D (load/dispose), así reutiliza toda la conversación y la voz.
// Reglas de Lumo: un solo personaje y sin rebotes; solo cambia la boca y una
// leve inclinación de cabeza al «pensar» (sin ella con movimiento reducido).
const BOCAS = ['cerrada', 'a', 'e', 'o', 'u', 'm'];
// Tiempo mínimo de cada boca: evita parpadeos entre formas (≈ 12 cambios/s).
const BOCA_MIN_MS = 80;

// Reparto típico de la energía de la voz por bandas (medido con las voces de
// los tutores). Cada banda se compara con su valor típico: así ninguna domina
// solo por tener más frecuencias.
export const BANDAS_TIPICAS = { graves: 0.18, medios: 0.247, agudos: 0.277, sibilantes: 0.261 };

/** Visema según la energía por bandas (graves → O/U, medios → A, agudos → E). */
export function elegirBoca(hablando, amplitud, bandas) {
  if (!hablando) return 'cerrada';
  if (amplitud < 0.06) return 'm';
  const total = bandas.graves + bandas.medios + bandas.agudos + bandas.sibilantes || 1;
  const r = n => bandas[n] / total / BANDAS_TIPICAS[n];
  const graves = r('graves'), medios = r('medios'), agudos = Math.max(r('agudos'), r('sibilantes'));
  if (graves >= medios && graves >= agudos) return amplitud > 0.45 ? 'o' : 'u';
  if (agudos > medios * 1.1) return amplitud > 0.7 ? 'a' : 'e';
  return 'a';
}

export function createLumo(stage, audio, analyser) {
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
  const valores = new Uint8Array(analyser.fftSize), freq = new Uint8Array(analyser.frequencyBinCount);
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
    // Todas decodificadas antes de hablar: cambiar de boca nunca deja un hueco.
    await Promise.all([base, ...Object.values(bocas)].map(i => i.decode()));
    if (eliminado) return;
    cargado = true;
    stage.dataset.loaded = 'true';
  }

  function frame(ahora) {
    if (eliminado) return;
    frameId = requestAnimationFrame(frame);
    if (!cargado || ahora - ultimo < 33) return;
    ultimo = ahora;
    const hablando = !audio.paused && !audio.ended;
    let amplitud = 0, graves = 0, medios = 0, agudos = 0, sibilantes = 0;
    if (hablando) {
      analyser.getByteTimeDomainData(valores);
      let suma = 0;
      for (const x of valores) suma += ((x - 128) / 128) ** 2;
      amplitud = Math.min(1, Math.sqrt(suma / valores.length) * 7);
      analyser.getByteFrequencyData(freq);
      const bin = analyser.context.sampleRate / analyser.fftSize;
      for (let i = 1; i < freq.length; i++) {
        const f = i * bin, v = freq[i] * freq[i];
        if (f < 600) graves += v; else if (f < 2000) medios += v; else if (f < 5000) agudos += v; else if (f < 9000) sibilantes += v;
      }
    }
    mostrar(elegirBoca(hablando, amplitud, { graves, medios, agudos, sibilantes }), ahora);
    if (depurar && hablando) { const t = graves + medios + agudos + sibilantes || 1; (window.__bandas ||= []).push([amplitud, graves / t, medios / t, agudos / t, sibilantes / t]); }
    const fase = stage.dataset.phase;
    capa.classList.toggle('pensando', !reducido && !hablando && (fase === 'thinking' || fase === 'voice-loading'));
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
