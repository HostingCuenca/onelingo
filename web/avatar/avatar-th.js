// Tutor 3D con TalkingHead (MIT): parpadeo, mirada, gestos e iluminación de
// retrato. La voz sigue sonando por el <audio> de practice.js (en iPhone el
// WebAudio se entrecortaba al abrir el micrófono): aquí solo se mueve la cara.
// La boca sigue la línea de visemas de la frase que suena (visemas.js),
// leída del reloj del <audio> en cada cuadro por el canal «realtime» de
// TalkingHead, que manda sobre sus animaciones.
import * as THREE from 'three';
import {TalkingHead} from './vendor/talkinghead/talkinghead.mjs';
import {pesos} from './visemas.js?v=1';

const VISEMAS = ['aa', 'E', 'I', 'O', 'U', 'PP', 'SS', 'TH', 'DD', 'FF', 'kk', 'nn', 'RR', 'CH', 'sil'];
// Retrato: tono Neutral (no lava la piel como ACES), luz principal cálida
// delante y arriba, ambiente bajo para dar volumen y contraluz lila de marca
// detrás del pelo.
const LUZ = {exp: 1.03, env: 0.7, amb: ['#fff4ec', 0.6], key: ['#ffefe0', 3.2, [-1.5, 3.1, 3.1]], rim: ['#c9baff', 3.2, [1.3, 2.8, -3.4]]};

// Pelo «fantasma»: las capas de pelo semitransparentes (BLEND) se dibujan sin
// profundidad y se ve la cara a través. Dos pasadas: núcleo sólido que escribe
// profundidad y una copia suave encima solo para los bordes de cada mechón.
function arreglarPelo(escena) {
  const capas = [];
  escena.traverse(o => { if (o.isMesh && !o.userData.peloSuave && [].concat(o.material).some(m => /hair|ponytail|bob|braid|afro/i.test(m.name))) capas.push(o); });
  for (const o of capas) {
    const base = [].concat(o.material)[0];
    const solido = base.clone(); Object.assign(solido, {transparent: false, depthWrite: true, alphaTest: 0.55, side: THREE.DoubleSide});
    const suave = base.clone(); Object.assign(suave, {transparent: true, depthWrite: false, alphaTest: 0.02, side: THREE.DoubleSide});
    o.material = solido; o.renderOrder = 1;
    const copia = o.clone(); copia.material = suave; copia.renderOrder = 2; copia.userData.peloSuave = true;
    if (o.morphTargetInfluences) copia.morphTargetInfluences = o.morphTargetInfluences;
    o.parent.add(copia);
  }
}

export function createAvatarTH(stage, fuente, ajustes = {}) {
  const nodo = document.createElement('div'); nodo.className = 'lienzo-th'; stage.prepend(nodo);
  const head = new TalkingHead(nodo, {
    lipsyncModules: [], lipsyncLang: 'en', cameraView: 'upper', cameraRotateEnable: false, cameraPanEnable: false, cameraZoomEnable: false,
    modelFPS: 30, modelPixelRatio: Math.min(devicePixelRatio, 1.5), avatarMood: 'happy', avatarIdleEyeContact: 0.6, avatarSpeakingEyeContact: 0.8,
  });
  const contraluz = new THREE.DirectionalLight();
  contraluz.target.position.set(0, 1.5, 0); head.scene.add(contraluz, contraluz.target);
  function iluminar() {
    head.renderer.toneMapping = THREE.NeutralToneMapping; head.renderer.toneMappingExposure = LUZ.exp; head.scene.environmentIntensity = LUZ.env;
    head.lightAmbient.color.set(LUZ.amb[0]); head.lightAmbient.intensity = LUZ.amb[1];
    head.lightDirect.color.set(LUZ.key[0]); head.lightDirect.intensity = LUZ.key[1]; head.lightDirect.position.set(...LUZ.key[2]);
    contraluz.color.set(LUZ.rim[0]); contraluz.intensity = LUZ.rim[1]; contraluz.position.set(...LUZ.rim[2]); head.lightSpot.intensity = 0;
    head.scene.traverse(m => { if (m.isMesh) for (const x of [].concat(m.material)) x.needsUpdate = true; });
  }

  let frame = 0, disposed = false, boca = false, fase = '';
  function tick() {
    if (disposed) return;
    frame = requestAnimationFrame(tick);
    const mt = head.mtAvatar; if (!mt?.viseme_aa) return;
    const r = fuente.reloj?.();
    if (r?.hablando && r.linea?.length) {
      const w = pesos(r.linea, r.ms);
      for (const v of VISEMAS) { const o = mt['viseme_' + v]; if (o) { o.realtime = w[v] || 0; o.needsUpdate = true; } }
      boca = true; head.isSpeaking = true;
    } else if (boca) {
      for (const v of VISEMAS) { const o = mt['viseme_' + v]; if (o) { o.realtime = null; o.needsUpdate = true; } }
      boca = false; head.isSpeaking = false;
    }
    // Estados de la llamada: pensando mira un poco arriba; escuchando, atento a ti.
    const p = stage.dataset.phase;
    if (p !== fase) {
      fase = p;
      if (p === 'thinking') { head.lookAhead?.(600); head.setMood?.('neutral'); }
      else if (p === 'listening') { head.lookAtCamera?.(1500); head.setMood?.('happy'); }
      else if (p === 'speaking' || p === 'ready') head.setMood?.('happy');
    }
  }

  nodo.cabeza = head; // para depurar desde la consola
  return {
    alineado: true, // pide la voz con los tiempos de cada letra (/voz/alineada)
    async load(url, onProgress) {
      await head.showAvatar({url, body: ajustes.body || 'F', avatarMood: 'happy', lipsyncLang: 'en', baseline: ajustes.baseline || {}}, onProgress);
      if (disposed) return;
      arreglarPelo(head.scene); iluminar();
      stage.dataset.loaded = 'true';
      tick();
    },
    dispose() {
      disposed = true; cancelAnimationFrame(frame);
      try { head.stop(); head.dispose?.(); } catch { /* ya liberado */ }
      nodo.remove(); delete stage.dataset.loaded;
    },
  };
}
