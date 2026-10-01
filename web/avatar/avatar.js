import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
// Geometría y formas de la cara comprimidas con meshopt (modelos 6 → 2 MB).
import {MeshoptDecoder} from './vendor/meshopt_decoder.module.js';
import {repartir} from './voz.js?v=27';

// La boca sigue la envolvente de la voz (voz.js), no un temporizador ni un vídeo.
// La boca combina visemas según el reparto de energía por bandas de frecuencia
// (graves → O/U, medios → A, agudos → E/I, sibilantes → S): no es alineación
// fonética exacta, pero ya no es un simple abrir y cerrar.
// Estados como el Video Call de Duolingo: «pensando» (cabeza inclinada, mirada
// arriba) mientras llega la respuesta y «escuchando» (atento) mientras hablas.
export function createAvatar(stage, fuente) {
  const scene=new THREE.Scene(), camera=new THREE.PerspectiveCamera(33,1,.1,100);
  // ?retrato: conserva el último cuadro para generar los retratos de la galería
  // (sin parpadeo y con un plano algo más abierto).
  const retrato=new URLSearchParams(location.search).has('retrato');
  const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:retrato});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.9;
  stage.prepend(renderer.domElement);
  scene.add(new THREE.HemisphereLight(0xffe9d7,0x454051,1.05));
  for(const [c,i,p] of [[0xf8ffe8,3,[-3,5,4]],[0xcfe9ff,1.5,[3,3,1]],[0xadc7ff,2,[0,4,-3]]]){const l=new THREE.DirectionalLight(c,i);l.position.set(...p);scene.add(l);}
  const observer=new ResizeObserver(()=>{camera.aspect=stage.clientWidth/stage.clientHeight;camera.updateProjectionMatrix();renderer.setSize(stage.clientWidth,stage.clientHeight)});observer.observe(stage);
  let rig,head,body,restHead,restBody,morphs=[],frameId,disposed=false,previous=performance.now(),start=previous,lastRender=0;
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function disposeRig(root){root?.traverse(o=>{if(o.geometry)o.geometry.dispose();for(const m of (Array.isArray(o.material)?o.material:[o.material])){if(!m)continue;for(const v of Object.values(m))if(v?.isTexture)v.dispose();m.dispose()}})}
  async function load(url,onProgress){
    const gltf=await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).loadAsync(url,onProgress);
    if(disposed){disposeRig(gltf.scene);return;}
    rig=gltf.scene;scene.add(rig);head=rig.getObjectByName('head');body=rig.getObjectByName('spine_03');
    if(!head||!body)throw Error('El rig del tutor no está disponible.');
    // El archivo conserva la pose abierta necesaria para el rig. Al mostrarlo,
    // bajamos los brazos con una separación natural (antes quedaban pegados
    // al torso y se veían retraídos).
    rig.updateMatrixWorld(true);
    for(const [side,x] of [['l',-.16],['r',.16]]){
      const arm=rig.getObjectByName(`upperarm_${side}`),forearm=rig.getObjectByName(`lowerarm_${side}`);
      if(!arm||!forearm)continue;
      const shoulder=new THREE.Vector3(),elbow=new THREE.Vector3();
      arm.getWorldPosition(shoulder);forearm.getWorldPosition(elbow);
      const current=elbow.sub(shoulder).normalize(),desired=new THREE.Vector3(-x*1.6,-.95,.06).normalize();
      const delta=new THREE.Quaternion().setFromUnitVectors(current,desired);
      const world=new THREE.Quaternion();arm.getWorldQuaternion(world);world.premultiply(delta);
      const parentWorld=new THREE.Quaternion();arm.parent.getWorldQuaternion(parentWorld);
      arm.quaternion.copy(parentWorld.invert().multiply(world));
      arm.updateMatrixWorld(true);
    }
    restHead=head.quaternion.clone();restBody=body.quaternion.clone();
    rig.traverse(o=>{if(!o.isMesh)return;for(const m of (Array.isArray(o.material)?o.material:[o.material])){m.transparent=false;m.depthWrite=true;m.alphaTest=/afro|ponytail|bob|long01|short0|eyebrow|eyelash/.test(m.name)?.4:0;if(/afro|ponytail|braid|bob|long01|short0/.test(m.name)){m.roughness=.95;m.alphaTest=.12;}m.needsUpdate=true;}if(o.morphTargetDictionary)morphs.push(o)});
    rig.updateMatrixWorld(true);const p=new THREE.Vector3();head.getWorldPosition(p);camera.position.set(0,p.y+.05,retrato?1.08:1.12);camera.lookAt(0,retrato?p.y-.1:p.y-.03,0);// plano de videollamada: cabeza, hombros y pecho
    stage.dataset.loaded='true';
  }
  // 30 fps is sufficient for idle motion and amplitude lip movement. Rendering
  // the 30k-poly tutor at 60 fps competed with chat/audio callbacks on modest
  // phones and on software-rendered browsers.
  function frame(now){if(disposed)return;frameId=requestAnimationFrame(frame);if(now-lastRender<33)return;lastRender=now;const t=(now-start)/1000,dt=Math.min((now-previous)/1000,.05);previous=now;
    if(head){const muestra=fuente.muestra(),speaking=muestra.hablando,amplitude=speaking?muestra.amplitud:0;
      const {graves:sLow,medios:sMid,agudos:sHigh,sibilantes:sSib}=repartir(muestra);
      const mood=stage.dataset.phase, thinking=(mood==='thinking'||mood==='voice-loading')&&!speaking, listening=mood==='listening'&&!speaking;
      const motion=reduced?0:.55, phase=t%4.3,blink=!retrato&&phase<.17?Math.sin(phase/.17*Math.PI):0;
      rig.position.y=Math.sin(t*1.5)*.002*motion;
      // Pensando: inclina la cabeza y mira un poco hacia arriba. Escuchando: leve asentimiento.
      const tiltX=thinking?-.06:listening?Math.sin(t*2.2)*.025:0, tiltZ=thinking?.07:0;
      head.quaternion.copy(restHead).multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.sin(t*.82)*.018*motion+tiltX,Math.sin(t*.61)*.055*motion,Math.sin(t*.43)*.025*motion+tiltZ)));
      body.quaternion.copy(restBody).multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.sin(t*.65)*.007*motion,Math.sin(t*.4)*.012*motion,0)));
      for(const m of morphs)for(const [n,i] of Object.entries(m.morphTargetDictionary)){let target=0;
        if(n==='viseme_aa')target=amplitude*(.35+sMid*.9);
        else if(n==='viseme_O')target=amplitude*sLow*.9;
        else if(n==='viseme_U')target=amplitude*sLow*.35;
        else if(n==='viseme_E')target=amplitude*sHigh*.8;
        else if(n==='viseme_I')target=amplitude*sHigh*.35;
        else if(n==='viseme_SS')target=amplitude*sSib*1.2;
        else if(n==='viseme_PP')target=speaking&&amplitude<.06?.35:0;
        else if(n.startsWith('browInnerUp'))target=thinking?.35:0;
        else if(n==='eyeBlinkLeft'||n==='eyeBlinkRight')target=blink;
        // Mirada: arriba al pensar; al frente (a ti) al escuchar y al hablar.
        else if(n==='eyeLookUpLeft'||n==='eyeLookUpRight')target=thinking?.4:0;
        else if(n==='eyeLookOutLeft')target=thinking?.18:0;
        else if(n==='eyeLookInRight')target=thinking?.18:0;
        else if(n.startsWith('eyeSquint'))target=listening?.2:.12;
        else if(n.startsWith('mouthSmile'))target=speaking?.03:.14;
        m.morphTargetInfluences[i]=THREE.MathUtils.damp(m.morphTargetInfluences[i],target,35,dt);
      }stage.dataset.mouth=amplitude.toFixed(3);
    }renderer.render(scene,camera);
  }frameId=requestAnimationFrame(frame);
  return {load,dispose(){disposed=true;cancelAnimationFrame(frameId);observer.disconnect();disposeRig(rig);renderer.dispose();renderer.forceContextLoss();renderer.domElement.remove();delete stage.dataset.loaded;}};
}
