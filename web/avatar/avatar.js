import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

// Animation follows the audio analyser, not a wall-clock timer or generated video.
// This is an amplitude-driven approximation, not phoneme-accurate alignment.
export function createAvatar(stage, audio, analyser) {
  const scene=new THREE.Scene(), camera=new THREE.PerspectiveCamera(33,1,.1,100);
  const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.9;
  stage.prepend(renderer.domElement);
  scene.add(new THREE.HemisphereLight(0xffe9d7,0x454051,1.05));
  for(const [c,i,p] of [[0xf8ffe8,3,[-3,5,4]],[0xcfe9ff,1.5,[3,3,1]],[0xadc7ff,2,[0,4,-3]]]){const l=new THREE.DirectionalLight(c,i);l.position.set(...p);scene.add(l);}
  const observer=new ResizeObserver(()=>{camera.aspect=stage.clientWidth/stage.clientHeight;camera.updateProjectionMatrix();renderer.setSize(stage.clientWidth,stage.clientHeight)});observer.observe(stage);
  let rig,head,body,restHead,restBody,morphs=[],frameId,disposed=false,previous=performance.now(),start=previous,lastRender=0;
  const values=new Uint8Array(analyser.fftSize), reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function disposeRig(root){root?.traverse(o=>{if(o.geometry)o.geometry.dispose();for(const m of (Array.isArray(o.material)?o.material:[o.material])){if(!m)continue;for(const v of Object.values(m))if(v?.isTexture)v.dispose();m.dispose()}})}
  async function load(url,onProgress){
    const gltf=await new GLTFLoader().loadAsync(url,onProgress);
    if(disposed){disposeRig(gltf.scene);return;}
    rig=gltf.scene;scene.add(rig);head=rig.getObjectByName('head');body=rig.getObjectByName('spine_03');
    if(!head||!body)throw Error('El rig del tutor no está disponible.');
    // El archivo conserva la pose abierta necesaria para el rig. Al mostrarlo,
    // llevamos los brazos junto al torso para una presencia natural de tutor.
    rig.updateMatrixWorld(true);
    for(const [side,x] of [['l',-.16],['r',.16]]){
      const arm=rig.getObjectByName(`upperarm_${side}`),forearm=rig.getObjectByName(`lowerarm_${side}`);
      if(!arm||!forearm)continue;
      const shoulder=new THREE.Vector3(),elbow=new THREE.Vector3();
      arm.getWorldPosition(shoulder);forearm.getWorldPosition(elbow);
      const current=elbow.sub(shoulder).normalize(),desired=new THREE.Vector3(x,-.985,.04).normalize();
      const delta=new THREE.Quaternion().setFromUnitVectors(current,desired);
      const world=new THREE.Quaternion();arm.getWorldQuaternion(world);world.premultiply(delta);
      const parentWorld=new THREE.Quaternion();arm.parent.getWorldQuaternion(parentWorld);
      arm.quaternion.copy(parentWorld.invert().multiply(world));
      arm.updateMatrixWorld(true);
    }
    restHead=head.quaternion.clone();restBody=body.quaternion.clone();
    rig.traverse(o=>{if(!o.isMesh)return;for(const m of (Array.isArray(o.material)?o.material:[o.material])){m.transparent=false;m.depthWrite=true;m.alphaTest=/afro|ponytail|bob|long01|short0|eyebrow|eyelash/.test(m.name)?.4:0;if(/afro|ponytail|braid|bob|long01|short0/.test(m.name)){m.roughness=.95;m.alphaTest=.12;}m.needsUpdate=true;}if(o.morphTargetDictionary)morphs.push(o)});
    rig.updateMatrixWorld(true);const p=new THREE.Vector3();head.getWorldPosition(p);camera.position.set(0,p.y+.015,1.15);camera.lookAt(0,p.y-.13,0);stage.dataset.loaded='true';
  }
  // 30 fps is sufficient for idle motion and amplitude lip movement. Rendering
  // the 30k-poly tutor at 60 fps competed with chat/audio callbacks on modest
  // phones and on software-rendered browsers.
  function frame(now){if(disposed)return;frameId=requestAnimationFrame(frame);if(now-lastRender<33)return;lastRender=now;const t=(now-start)/1000,dt=Math.min((now-previous)/1000,.05);previous=now;
    if(head){analyser.getByteTimeDomainData(values);let sum=0;for(const x of values)sum+=((x-128)/128)**2;
      const speaking=!audio.paused&&!audio.ended, amplitude=speaking?Math.min(1,Math.sqrt(sum/values.length)*7):0;
      const motion=reduced?0:.55, phase=t%4.3,blink=phase<.17?Math.sin(phase/.17*Math.PI):0;
      rig.position.y=Math.sin(t*1.5)*.002*motion;
      head.quaternion.copy(restHead).multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.sin(t*.82)*.018*motion,Math.sin(t*.61)*.055*motion,Math.sin(t*.43)*.025*motion)));
      body.quaternion.copy(restBody).multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.sin(t*.65)*.007*motion,Math.sin(t*.4)*.012*motion,0)));
      for(const m of morphs)for(const [n,i] of Object.entries(m.morphTargetDictionary)){let target=0;
        if(n==='viseme_aa')target=amplitude*.85;
        else if(n==='viseme_O')target=amplitude*.15;
        else if(n==='eyeBlinkLeft'||n==='eyeBlinkRight')target=blink;
        else if(n.startsWith('eyeSquint'))target=.12;
        else if(n.startsWith('mouthSmile'))target=speaking?.03:.14;
        m.morphTargetInfluences[i]=THREE.MathUtils.damp(m.morphTargetInfluences[i],target,35,dt);
      }stage.dataset.mouth=amplitude.toFixed(3);
    }renderer.render(scene,camera);
  }frameId=requestAnimationFrame(frame);
  return {load,dispose(){disposed=true;cancelAnimationFrame(frameId);observer.disconnect();disposeRig(rig);renderer.dispose();renderer.forceContextLoss();renderer.domElement.remove();delete stage.dataset.loaded;}};
}
