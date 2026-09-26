import {createAvatar} from './avatar.js?v=15';
const $=id=>document.getElementById(id), audio=$('audio');
const roster=await (await fetch('./roster.json')).json();
let config=null,tutor=null,avatar=null,ctx,analyser,history=[],busy=false,controller=null,audioController=null,audioURL=null,epoch=0,lastReply='',recorder=null,micStream=null,silenceTimer=null,recordingEpoch=0,micSource=null,selection=0;
const languages={en:'inglés',es:'español',fr:'francés',de:'alemán',pt:'portugués',it:'italiano',zh:'chino',ja:'japonés',ko:'coreano',ru:'ruso'};
const preferred={en:['amara','sofia','clara'],es:['lucia','mateo'],fr:['clara','sofia'],de:['daniel','owen'],pt:['amara','mateo'],it:['sofia','mateo'],zh:['mei','kenji'],ja:['kenji','mei'],ko:['mei','kenji'],ru:['owen','clara']};
const language=()=>config?.idiomaMeta||'en',languageName=()=>languages[language()]||languages.en;
const status=t=>$('status').textContent=t;
function phase(label,value='ready'){$('state').textContent=label;$('stage').dataset.phase=value;}
function error(e){$('error').textContent=e?.message||String(e)}
function headers(){return {'Authorization':`Bearer ${config.token}`}}
function controls(){const disabled=!config?.token||!avatar||!$('stage').dataset.loaded||busy||!!recorder;$('send').disabled=disabled;$('text').disabled=busy;$('topic').disabled=busy||!!recorder;$('mic').disabled=busy||!config?.token||!avatar;}
window.addEventListener('message',event=>{
 if(event.origin!==location.origin||event.source!==parent)return;
 try{const c=JSON.parse(event.data);if(c.type!=='onelingo-avatar-init')return;const u=new URL(c.api);if(u.origin!==location.origin&&!['127.0.0.1','localhost'].includes(u.hostname))return;config=c;$('authStatus').textContent=c.token?`Nivel ${c.nivel} · tutores para practicar ${languageName()}`:'Inicia sesión en OneLingo para conversar con los tutores.';$('selectionCopy').textContent=`Elige a tu tutor de ${languageName()}. Puedes escribir o hablar; recibirás una respuesta y correcciones adaptadas a tu nivel.`;$('messageLabel').textContent=`Tu mensaje en ${languageName()}`;renderGallery();controls();}catch{}
});
parent.postMessage('onelingo-avatar-ready',location.origin);
const units=await (await fetch('./topics.json')).json();
for(const u of units){const o=document.createElement('option');o.value=u.id;o.textContent=u.nombre;$('topic').append(o)}
function renderGallery(){
 const recommendations=preferred[language()]||preferred.en,ordered=[...roster.tutors].sort((a,b)=>{const ai=recommendations.indexOf(a.id),bi=recommendations.indexOf(b.id);return (ai<0?99:ai)-(bi<0?99:bi)});
 $('gallery').replaceChildren();
 for(const t of ordered){const b=document.createElement('button');b.className='tutor';const portrait=document.createElement('div');portrait.className='portrait';const img=document.createElement('img');img.src=t.portrait;img.alt=`Retrato de ${t.name}`;img.loading='lazy';portrait.append(img);const name=document.createElement('strong');name.textContent=t.name;const voice=document.createElement('small');voice.textContent=`Tutor de ${languageName()} · ${t.voice_direction.split(' · ')[2]||'conversacional'}`;b.append(portrait,name,voice);if(recommendations.includes(t.id)){const badge=document.createElement('span');badge.className='recommended';badge.textContent='Recomendado';b.append(badge)}b.onclick=()=>select(t);$('gallery').append(b)}
}
renderGallery();
function ensureAudio(){if(!ctx){ctx=new AudioContext();analyser=ctx.createAnalyser();analyser.fftSize=512;ctx.createMediaElementSource(audio).connect(analyser);analyser.connect(ctx.destination);}return ctx.resume();}
async function select(t){stop();avatar?.dispose();avatar=null;tutor=t;history=[];lastReply='';$('messages').replaceChildren();bubble(`${t.name} iniciará la conversación cuando termine de cargar.`,'feedback');$('name').textContent=`${t.name} · ${languageName()}`;$('selection').hidden=true;$('session').hidden=false;controls();$('loading').hidden=false;$('loading').style.display='grid';$('loading').textContent=`Cargando ${t.name}…`;$('error').textContent='';phase('Preparando tutor','loading');const version=++selection;
 try{await ensureAudio();avatar=createAvatar($('stage'),audio,analyser);await avatar.load(t.model,e=>{if(version===selection&&e.total)$('loading').textContent=`Cargando ${t.name} · ${Math.round(e.loaded/e.total*100)} %`});if(version!==selection)return;$('loading').style.display='none';controls();await requestTutor('',true);}
 catch(e){if(version!==selection)return;avatar?.dispose();avatar=null;error(e);status('No se pudo cargar el tutor. Regresa y vuelve a intentarlo.');controls();}
}
function cancelRecording(){recordingEpoch++;clearInterval(silenceTimer);if(recorder){recorder.onstop=null;recorder.stop();recorder=null;}micStream?.getTracks().forEach(t=>t.stop());micStream=null;micSource?.disconnect();micSource=null;$('mic').textContent='🎙 Hablar';}
function stop(){epoch++;controller?.abort();controller=null;audioController?.abort();audioController=null;audio.pause();audio.removeAttribute('src');audio.load();if(audioURL){URL.revokeObjectURL(audioURL);audioURL=null;}cancelRecording();busy=false;phase('Tu turno');controls();status('Puedes continuar cuando quieras.');}
$('stop').onclick=stop;
$('back').onclick=()=>{selection++;stop();avatar?.dispose();avatar=null;$('session').hidden=true;$('selection').hidden=false;};
$('topic').onchange=()=>{stop();history=[];lastReply='';$('messages').replaceChildren();bubble(`${tutor.name} iniciará esta situación.`,'feedback');void requestTutor('',true);};
function bubble(text,kind=''){const e=document.createElement('div');e.className='bubble '+kind;e.textContent=text;$('messages').append(e);e.scrollIntoView({block:'nearest'});return e;}
async function speak(text,version){
 audioController?.abort();audioController=new AbortController();const signal=audioController.signal;audio.pause();if(audioURL)URL.revokeObjectURL(audioURL);
 const url=new URL(config.api+'/voz/stream');url.search=new URLSearchParams({texto:text.slice(0,600),idioma:language(),voz:'avatar_'+tutor.id});
 const began=performance.now();audio.dataset.ttsStartedAt=began;phase('Preparando voz','voice-loading');status('La respuesta está lista. Preparando la voz…');
 try{const response=await fetch(url,{headers:headers(),signal});if(!response.ok)throw Error(`La voz no está disponible (${response.status}). Puedes seguir leyendo.`);if(version!==epoch)return;
  if(window.MediaSource&&MediaSource.isTypeSupported('audio/mpeg')){
   const media=new MediaSource();audioURL=URL.createObjectURL(media);audio.src=audioURL;
   await new Promise((resolve,reject)=>{const abort=()=>reject(new DOMException('Cancelado','AbortError'));signal.addEventListener('abort',abort,{once:true});media.addEventListener('sourceopen',()=>{signal.removeEventListener('abort',abort);resolve()},{once:true})});
   if(version!==epoch)return;const buffer=media.addSourceBuffer('audio/mpeg'),reader=response.body.getReader();let first=true;
   while(true){const {done,value}=await reader.read();if(done)break;if(version!==epoch)return;await new Promise((resolve,reject)=>{const cleanup=()=>{buffer.removeEventListener('updateend',ok);buffer.removeEventListener('error',fail);signal.removeEventListener('abort',fail)};const ok=()=>{cleanup();resolve()};const fail=()=>{cleanup();reject(Error('Audio interrumpido'))};buffer.addEventListener('updateend',ok,{once:true});buffer.addEventListener('error',fail,{once:true});signal.addEventListener('abort',fail,{once:true});try{buffer.appendBuffer(value)}catch(e){cleanup();reject(e)}});
    if(first){first=false;audio.play().catch(()=>status('Pulsa reproducir para escuchar al tutor.'));}
   }if(media.readyState==='open')media.endOfStream();
  }else{audioURL=URL.createObjectURL(await response.blob());if(version!==epoch)return;audio.src=audioURL;await audio.play().catch(()=>status('Pulsa reproducir para escuchar al tutor.'));}
  audio.dataset.voice=tutor.id;audio.dataset.preparedMs=Math.round(performance.now()-began);
 }catch(e){if(version===epoch&&!signal.aborted)error(e)}
}
audio.onplaying=()=>{const now=performance.now();phase(`${tutor?.name||'El tutor'} está hablando`,'speaking');status('Escucha al tutor. Puedes interrumpir para responder.');audio.dataset.playedAt=now;const turn=Number(audio.dataset.turnStartedAt);if(turn)audio.dataset.firstAudioMs=Math.round(now-turn);};
audio.onended=()=>{phase('Tu turno');status('Te toca. Puedes escribir o hablar.');};
audio.onerror=()=>{if(audio.getAttribute('src')){phase('Voz no disponible','error');error('No se pudo reproducir la voz. Revisa tu conexión y pulsa Repetir voz.');}};
$('replay').onclick=async()=>{if(!lastReply||busy)return;await ensureAudio();speak(lastReply,epoch)};
$('form').onsubmit=event=>{event.preventDefault();send()};
async function send(){const text=$('text').value.trim();if(!text||busy||!config?.token)return;await requestTutor(text,false);}
async function requestTutor(text,opening=false){if(busy||!config?.token||!tutor||!avatar)return;await ensureAudio();if(!opening)stop();const version=epoch;busy=true;controls();$('error').textContent='';if(!opening){$('text').value='';bubble(text,'mine');history.push({rol:'alumno',texto:text});}let answer=null,replied=false;controller=new AbortController();const current=controller;const timeout=setTimeout(()=>current.abort(),45000);const turnStarted=performance.now();audio.dataset.turnStartedAt=turnStarted;delete audio.dataset.firstAudioMs;delete audio.dataset.replyReadyMs;phase(opening?`${tutor.name} inicia la conversación`:'Pensando','thinking');status(opening?`${tutor.name} está preparando el saludo…`:'El tutor está preparando su respuesta…');
 const u=units.find(u=>u.id===Number($('topic').value));
 try{const response=await fetch(config.api+'/chat',{method:'POST',headers:{...headers(),'Content-Type':'application/json','Accept':'text/event-stream'},signal:current.signal,body:JSON.stringify({idiomaMeta:language(),idiomaNativo:config.idiomaNativo,nivel:config.nivel,tutorId:'avatar_'+tutor.id,historial:history.slice(-30),objetivo:config.contexto,...(u?{situacionId:u.id,situacion:u.nombre}: {})})});
  if(!response.ok)throw Error(response.status===401?'Tu sesión ha caducado. Vuelve a iniciar sesión.':`No se pudo conectar con el tutor (${response.status}).`);
  const reader=response.body.getReader(),decoder=new TextDecoder();let pending='',final=false;
  function event(raw){if(version!==epoch)return;const line=raw.split('\n').find(l=>l.startsWith('data: '));if(!line)return;const e=JSON.parse(line.slice(6));if(e.tipo==='error')throw Error(e.data);
   if(e.tipo==='reply'&&!replied){replied=true;audio.dataset.replyReadyMs=Math.round(performance.now()-turnStarted);lastReply=e.data;answer=bubble(e.data);speak(e.data,version);}
   if(e.tipo==='final'){final=true;const r=e.data;if(!replied){lastReply=r.reply;answer=bubble(r.reply);speak(r.reply,version);}else answer.textContent=r.reply;history.push({rol:'tutor',texto:r.reply});if(r.traduccion)bubble(r.traduccion,'feedback');for(const c of r.corrections||[])bubble(`${c.original} → ${c.correcto}\n${c.explicacion}`,'feedback');}
  }
  while(true){const {done,value}=await reader.read();if(done)break;pending+=decoder.decode(value,{stream:true});const parts=pending.split('\n\n');pending=parts.pop();for(const p of parts)event(p);}if(!final)throw Error('La respuesta quedó incompleta. Puedes volver a intentarlo.');
 }catch(e){if(version===epoch){phase('No se pudo responder','error');error(e.name==='AbortError'?'El tutor tardó demasiado. Puedes volver a intentarlo.':e);if(!replied&&!opening){$('text').value=text;history.pop();}}}
 finally{clearTimeout(timeout);if(version===epoch){busy=false;controller=null;controls();}}
}
$('mic').onclick=async()=>{
 if(recorder){recorder.stop();return;}if(busy)return;await ensureAudio();stop();const version=epoch,myRecording=++recordingEpoch;$('error').textContent='';
 try{const stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true},video:false});if(version!==epoch){stream.getTracks().forEach(t=>t.stop());return;}micStream=stream;
 const mime=['audio/webm;codecs=opus','audio/mp4','audio/webm'].find(t=>MediaRecorder.isTypeSupported(t));recorder=new MediaRecorder(stream,mime?{mimeType:mime}:{});const current=recorder,chunks=[],source=ctx.createMediaStreamSource(stream),meter=ctx.createAnalyser();meter.fftSize=1024;source.connect(meter);micSource=source;const samples=new Float32Array(meter.fftSize);let spoken=false,lastSpeech=performance.now(),start=lastSpeech;
 current.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
 current.onstop=async()=>{clearInterval(silenceTimer);source.disconnect();stream.getTracks().forEach(t=>t.stop());recorder=null;micStream=null;$('mic').textContent='🎙 Hablar';if(version!==epoch||myRecording!==recordingEpoch)return;busy=true;controls();status('Transcribiendo tu mensaje…');const transcribe=new AbortController();controller=transcribe;const timer=setTimeout(()=>transcribe.abort(),30000);let autoSend=false;
  try{const blob=new Blob(chunks,{type:current.mimeType});if(!spoken||blob.size<300)throw Error('No se detectó voz. Inténtalo de nuevo más cerca del micrófono.');const form=new FormData();form.append('idioma',language());form.append('audio',blob,current.mimeType.includes('mp4')?'turn.m4a':'turn.webm');const r=await fetch(config.api+'/transcribir',{method:'POST',headers:headers(),body:form,signal:transcribe.signal});if(!r.ok)throw Error('No se pudo transcribir. Puedes escribir tu mensaje.');const data=await r.json();if(version!==epoch)return;$('text').value=data.texto||'';autoSend=!!data.texto&&!$('review').checked;status('Revisa tu mensaje y pulsa Enviar.');}
  catch(e){if(version===epoch)error(e)}finally{clearTimeout(timer);if(version===epoch){busy=false;controller=null;controls();}}
  if(autoSend&&version===epoch)send();
 };
 current.start();$('mic').textContent='■ Terminar';$('state').textContent='Te escucho';status('Habla con calma. Se cierra tras 3 segundos de silencio.');controls();
 silenceTimer=setInterval(()=>{meter.getFloatTimeDomainData(samples);let sum=0;for(const x of samples)sum+=x*x;const now=performance.now();if(Math.sqrt(sum/samples.length)>.012){spoken=true;lastSpeech=now;}if((spoken&&now-lastSpeech>=3000)||(!spoken&&now-start>15000)||now-start>60000){clearInterval(silenceTimer);if(current.state==='recording')current.stop();}},100);
 }catch(e){cancelRecording();error(e.name==='NotAllowedError'?'Activa el permiso del micrófono en tu navegador.':e);controls();}
};
window.addEventListener('offline',()=>{stop();error('No hay conexión. Tus mensajes se conservan en esta conversación.');});
window.addEventListener('pagehide',()=>{stop();avatar?.dispose();ctx?.close();});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
controls();
