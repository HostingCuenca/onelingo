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

// Mirada a la cámara. TalkingHead mueve los ojos con los blendshapes eyeLook*
// suponiendo el recorrido de Ready Player Me; los Rocketbox giran mucho menos
// por unidad (7–20°), así que nunca llegaban a mirarte. Al cargar se mide
// cuántos grados da cada blendshape en este modelo y, en cada cuadro, se
// apunta cada ojo a la cámara compensando el giro de la cabeza.
const MIRADA = ['eyesLookUp', 'eyesLookDown', 'eyeLookInLeft', 'eyeLookOutLeft', 'eyeLookInRight', 'eyeLookOutRight'];
function medirOjo(head, lado) {
  const hueso = head.armature.getObjectByName(lado + 'Eye');
  let res = null;
  head.armature.traverse(m => {
    if (res || !hueso || !m.isSkinnedMesh || !m.morphTargetDictionary) return;
    const bi = m.skeleton.bones.indexOf(hueso); if (bi < 0) return;
    const g = m.geometry, p = g.attributes.position, si = g.attributes.skinIndex, sw = g.attributes.skinWeight;
    const idx = [];
    for (let v = 0; v < p.count; v++) for (let c = 0; c < 4; c++) if (si.getComponent(v, c) === bi && sw.getComponent(v, c) > 0.5) { idx.push(v); break; }
    if (idx.length < 8) return;
    // De la malla en pose de enlace al espacio local del hueso del ojo.
    const aHueso = new THREE.Matrix4().multiplyMatrices(m.skeleton.boneInverses[bi], m.bindMatrix);
    const centro = new THREE.Vector3().applyMatrix4(aHueso.clone().invert());
    const x = new THREE.Vector3(), y = new THREE.Vector3();
    const grados = k => {
      const d = g.morphAttributes.position?.[m.morphTargetDictionary[k + lado]]; if (!d) return 0;
      const a = [];
      for (const v of idx) { x.fromBufferAttribute(p, v).sub(centro); y.fromBufferAttribute(d, v).add(x); if (y.distanceToSquared(x) > 1e-12) a.push(x.angleTo(y)); }
      a.sort((q, r) => q - r); return a.length ? a[a.length >> 1] : 0;
    };
    // Hacia dónde mira el ojo en reposo: el casquete delantero del globo (iris).
    const frente = new THREE.Vector3();
    for (const v of idx) { x.fromBufferAttribute(p, v).sub(centro).normalize(); if (x.z > 0.85) frente.add(x); }
    if (frente.lengthSq() === 0) return;
    const fwd = frente.transformDirection(aHueso);
    const arriba = new THREE.Vector3(0, 1, 0).transformDirection(aHueso);
    const izq = new THREE.Vector3().crossVectors(arriba, fwd).normalize(); // izquierda del avatar (+x de la malla)
    arriba.crossVectors(fwd, izq).normalize();
    res = {hueso, fwd, izq, arriba, sube: grados('eyeLookUp'), baja: grados('eyeLookDown'), dentro: grados('eyeLookIn'), fuera: grados('eyeLookOut')};
  });
  return res && res.sube > 0.01 && res.baja > 0.01 && res.dentro > 0.01 && res.fuera > 0.01 ? res : null;
}

function prepararMirada(head) {
  const L = medirOjo(head, 'Left'), R = medirOjo(head, 'Right');
  if (!L || !R || !MIRADA.every(k => head.mtAvatar[k])) return null;
  for (const k of MIRADA) head.mtAvatar[k].max = 2.5; // un poco más allá del blendshape para alcanzar la cámara
  const cam = new THREE.Vector3(), pos = new THREE.Vector3(), q = new THREE.Quaternion(), t = new THREE.Vector3(), e = new THREE.Vector3();
  let sacada = {y: 0, x: 0, hasta: 0};
  const poner = (k, v) => { const o = head.mtAvatar[k]; o.realtime = Math.min(2.5, Math.max(0, v)); o.needsUpdate = true; };
  const angulos = o => {
    o.hueso.getWorldPosition(pos); o.hueso.getWorldQuaternion(q);
    t.subVectors(cam, pos).normalize();
    const f = t.dot(e.copy(o.fwd).applyQuaternion(q)), iz = t.dot(e.copy(o.izq).applyQuaternion(q)), ar = t.dot(e.copy(o.arriba).applyQuaternion(q));
    return {y: Math.atan2(iz, f) + sacada.y, x: Math.asin(Math.max(-1, Math.min(1, ar))) + sacada.x};
  };
  return {
    mirar(ms) {
      // Microsacadas: saltos de ~1° cada poco, como al mirar a alguien a los ojos.
      if (ms > sacada.hasta) sacada = {y: (Math.random() - 0.5) * 0.04, x: (Math.random() - 0.5) * 0.03, hasta: ms + 600 + Math.random() * 1800};
      head.camera.getWorldPosition(cam);
      const a = angulos(L), b = angulos(R);
      // Positivo = hacia la izquierda del avatar: el izquierdo mira «afuera», el derecho «adentro».
      poner('eyeLookOutLeft', a.y > 0 ? a.y / L.fuera : 0); poner('eyeLookInLeft', a.y < 0 ? -a.y / L.dentro : 0);
      poner('eyeLookInRight', b.y > 0 ? b.y / R.dentro : 0); poner('eyeLookOutRight', b.y < 0 ? -b.y / R.fuera : 0);
      const x = (a.x + b.x) / 2;
      poner('eyesLookUp', x > 0 ? x / ((L.sube + R.sube) / 2) : 0); poner('eyesLookDown', x < 0 ? -x / ((L.baja + R.baja) / 2) : 0);
    },
    soltar() { for (const k of MIRADA) { head.mtAvatar[k].realtime = null; head.mtAvatar[k].needsUpdate = true; } },
    medidas: {L, R},
  };
}

export function createAvatarTH(stage, fuente, ajustes = {}) {
  const nodo = document.createElement('div'); nodo.className = 'lienzo-th'; stage.prepend(nodo);
  const head = new TalkingHead(nodo, {
    lipsyncModules: [], lipsyncLang: 'en', cameraView: 'upper', cameraRotateEnable: false, cameraPanEnable: false, cameraZoomEnable: false,
    modelFPS: 30, modelPixelRatio: Math.min(devicePixelRatio, 1.5), avatarMood: 'happy',
    // Como en una videollamada: mira al alumno casi siempre y mueve poco la cabeza.
    avatarIdleEyeContact: 0.9, avatarSpeakingEyeContact: 0.95, avatarIdleHeadMove: 0.1, avatarSpeakingHeadMove: 0.15,
  });
  // Las miradas al azar de TalkingHead bajan hasta 0.6 rad (parece que mira
  // al suelo): se acotan a un vistazo corto alrededor de la cámara.
  for (const fase of ['idle', 'speaking']) for (const alt of head.animTemplateEyes?.[fase]?.alt || []) {
    const acotar = (vs, k, lim) => { if (vs?.[k]) vs[k] = vs[k].map(r => Array.isArray(r) ? [Math.max(r[0], -lim), Math.min(r[1], lim)] : r); };
    acotar(alt.vs, 'eyesRotateX', 0.12); acotar(alt.vs, 'eyesRotateY', 0.3);
  }
  // Cara amable. El ánimo «happy» de TalkingHead apenas sonríe (0.2) y sus
  // gestos al azar incluyen cejas fruncidas, nariz arrugada y labios
  // apretados: con los Rocketbox parecía que estaban molestos.
  const feliz = head.animMoods?.happy;
  if (feliz) feliz.baseline = {...feliz.baseline, mouthSmile: 0.75, cheekSquintLeft: 0.06, cheekSquintRight: 0.06, browInnerUp: 0.05, eyesLookDown: 0};
  head.mtRandomized = head.mtRandomized.filter(k => !/browDown|noseSneer|mouthPress|mouthFrown|mouthRoll|mouthShrug|cheekPuff/.test(k));
  const contraluz = new THREE.DirectionalLight();
  contraluz.target.position.set(0, 1.5, 0); head.scene.add(contraluz, contraluz.target);
  function iluminar() {
    head.renderer.toneMapping = THREE.NeutralToneMapping; head.renderer.toneMappingExposure = LUZ.exp; head.scene.environmentIntensity = LUZ.env;
    head.lightAmbient.color.set(LUZ.amb[0]); head.lightAmbient.intensity = LUZ.amb[1];
    head.lightDirect.color.set(LUZ.key[0]); head.lightDirect.intensity = LUZ.key[1]; head.lightDirect.position.set(...LUZ.key[2]);
    contraluz.color.set(LUZ.rim[0]); contraluz.intensity = LUZ.rim[1]; contraluz.position.set(...LUZ.rim[2]); head.lightSpot.intensity = 0;
    head.scene.traverse(m => { if (m.isMesh) for (const x of [].concat(m.material)) x.needsUpdate = true; });
  }

  let frame = 0, disposed = false, boca = false, fase = '', mirada = null;
  function tick(ms) {
    if (disposed) return;
    frame = requestAnimationFrame(tick);
    const mt = head.mtAvatar; if (!mt?.viseme_aa) return;
    // Pensando mira a otro lado (lookAhead de TalkingHead); el resto, a ti.
    if (mirada) { if (stage.dataset.phase === 'thinking') mirada.soltar(); else mirada.mirar(ms || 0); }
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
      // Cabeza y tronco giran apenas (±5–7°): con el giro completo de
      // TalkingHead parecía que buscaba algo a los lados.
      for (const [k, lim] of [['headRotateX', 0.06], ['headRotateY', 0.07], ['headRotateZ', 0.04], ['bodyRotateX', 0.05], ['bodyRotateY', 0.06], ['bodyRotateZ', 0.03]]) {
        const o = head.mtAvatar[k]; if (o) { o.min = -lim; o.max = lim; }
      }
      // Cada modelo sonríe con otra fuerza (en los Rocketbox la comisura sube
      // ≈4 mm, en Avaturn el doble): se busca la misma sonrisa de ~3 mm. Más (6 mm, ×1,6 en
      // Rocketbox) saca el blendshape de su rango y deforma la cara frente a su referencia.
      let mm = 0;
      head.armature.traverse(o => {
        const i = o.morphTargetDictionary?.mouthSmileLeft, d = i === undefined ? null : o.geometry.morphAttributes.position?.[i];
        if (d) for (let v = 0; v < d.count; v++) mm = Math.max(mm, Math.hypot(d.getX(v), d.getY(v), d.getZ(v)));
      });
      if (feliz && mm > 0 && head.mtAvatar.mouthSmile) {
        feliz.baseline.mouthSmile = Math.min(1, Math.max(0.4, 0.0029 / (mm * 0.8)));
        head.mtAvatar.mouthSmile.max = 2; head.setMood('happy');
      }
      mirada = prepararMirada(head); nodo.mirada = mirada;
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
