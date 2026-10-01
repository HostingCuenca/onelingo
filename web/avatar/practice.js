import {createAvatar} from './avatar.js?v=23';
import {createLumo} from './lumo.js?v=23';
const $=id=>document.getElementById(id), audio=$('audio');
const roster=await (await fetch('./roster.json?v=23')).json();
let config=null,tutor=null,avatar=null,ctx,analyser,history=[],busy=false,controller=null,audioController=null,audioURL=null,epoch=0,lastReply='',recorder=null,micStream=null,silenceTimer=null,recordingEpoch=0,micSource=null,selection=0;
// Voz por frases: la primera se reproduce en streaming en cuanto llega y las
// siguientes se descargan mientras tanto y suenan a continuación.
let colaVoz=[],vozActiva=false;
// Silencio que cierra el turno de voz. 3 s se sentía como lag; 1,2 s es el
// rango habitual de los asistentes de voz sin cortar pausas naturales.
const FIN_SILENCIO_MS=1200;
// Modo integrado en la app: la galería y la cabecera las pone Flutter; aquí
// solo el escenario y la conversación con el tutor elegido (?embebido&tutor=id).
const parametros=new URLSearchParams(location.search), embebido=parametros.has('embebido'), tutorInicial=parametros.get('tutor');
if(embebido)document.body.classList.add('embebido');
const languages={en:'inglés',es:'español',fr:'francés',de:'alemán',pt:'portugués',it:'italiano',zh:'chino',ja:'japonés',ko:'coreano',ru:'ruso'};
// Lumo va primero en todos los idiomas; después, los tutores 3D recomendados.
const preferred={en:['lumo','amara','sofia','clara'],es:['lumo','lucia','mateo'],fr:['lumo','clara','sofia'],de:['lumo','daniel','owen'],pt:['lumo','amara','mateo'],it:['lumo','sofia','mateo'],zh:['lumo','mei','kenji'],ja:['lumo','kenji','mei'],ko:['lumo','mei','kenji'],ru:['lumo','owen','clara']};
const language=()=>config?.idiomaMeta||'en',languageName=()=>languages[language()]||languages.en;
const status=t=>$('status').textContent=t;
function phase(label,value='ready'){$('state').textContent=label;$('stage').dataset.phase=value;}
function error(e){$('error').textContent=e?.message||String(e)}
function headers(){return {'Authorization':`Bearer ${config.token}`}}
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!=null)e.textContent=text;return e;}
function controls(){const disabled=!config?.token||!avatar||!$('stage').dataset.loaded||busy||!!recorder;$('send').disabled=disabled;$('text').disabled=busy;$('topic').disabled=busy||!!recorder;$('mic').disabled=busy||!config?.token||!avatar;$('end').disabled=busy||!!recorder||!history.some(t=>t.rol==='alumno');}
window.addEventListener('message',event=>{
 if(event.origin!==location.origin||event.source!==parent)return;
 try{const c=JSON.parse(event.data);if(c.type!=='onelingo-avatar-init')return;const u=new URL(c.api);if(u.origin!==location.origin&&!['127.0.0.1','localhost'].includes(u.hostname))return;config=c;$('authStatus').textContent=c.token?`Nivel ${c.nivel} · tutores para practicar ${languageName()}`:'Inicia sesión en OneLingo para conversar con los tutores.';$('selectionCopy').textContent=`Elige a tu tutor de ${languageName()}. Puedes escribir o hablar; recibirás una respuesta y correcciones adaptadas a tu nivel.`;$('messageLabel').textContent=`Tu mensaje en ${languageName()}`;renderGallery();controls();if(embebido&&tutorInicial&&!tutor){const t=roster.tutors.find(x=>x.id===tutorInicial);if(t)select(t);}}catch{}
});
parent.postMessage('onelingo-avatar-ready',location.origin);
const units=await (await fetch('./topics.json')).json();
for(const u of units){const o=document.createElement('option');o.value=u.id;o.textContent=u.nombre;$('topic').append(o)}
function renderGallery(){
 const recommendations=preferred[language()]||preferred.en,ordered=[...roster.tutors].sort((a,b)=>{const ai=recommendations.indexOf(a.id),bi=recommendations.indexOf(b.id);return (ai<0?99:ai)-(bi<0?99:bi)});
 $('gallery').replaceChildren();
 for(const t of ordered){const b=document.createElement('button');b.className='tutor';const portrait=document.createElement('div');portrait.className='portrait';const img=document.createElement('img');img.src=t.portrait;img.alt=`Retrato de ${t.name}`;img.loading='lazy';portrait.append(img);const name=document.createElement('strong');name.textContent=t.name;const voice=document.createElement('small');voice.textContent=t.tipo==='2d'?'Tu compañero de OneLingo · el más ligero':`Tutor de ${languageName()} · ${t.voice_direction.split(' · ')[2]||'conversacional'}`;b.append(portrait,name,voice);if(recommendations.includes(t.id)){const badge=document.createElement('span');badge.className='recommended';badge.textContent='Recomendado';b.append(badge)}b.onclick=()=>select(t);$('gallery').append(b)}
}
renderGallery();
function ensureAudio(){if(!ctx){ctx=new AudioContext();analyser=ctx.createAnalyser();analyser.fftSize=512;ctx.createMediaElementSource(audio).connect(analyser);analyser.connect(ctx.destination);}return ctx.resume();}
async function select(t){stop();avatar?.dispose();avatar=null;tutor=t;history=[];lastReply='';$('messages').replaceChildren();ideas([]);bubble(`${t.name} te saluda enseguida.`,'feedback');$('name').textContent=`${t.name} · ${languageName()}`;$('selection').hidden=true;$('session').hidden=false;$('stage').classList.toggle('dosd',t.tipo==='2d');controls();$('loading').hidden=false;$('loading').style.display='grid';$('loading').textContent=`Cargando ${t.name}…`;$('error').textContent='';phase('Preparando tutor','loading');const version=++selection;
 try{await ensureAudio();avatar=t.tipo==='2d'?createLumo($('stage'),audio,analyser):createAvatar($('stage'),audio,analyser);
  // El saludo (texto y voz) se pide en paralelo: no espera a que el modelo termine de descargarse.
  const carga=avatar.load(t.model,e=>{if(version===selection&&e.total)$('loading').textContent=`Cargando ${t.name} · ${Math.round(e.loaded/e.total*100)} %`});
  void requestTutor('',true);
  await carga;if(version!==selection)return;$('loading').style.display='none';controls();}
 catch(e){if(version!==selection)return;avatar?.dispose();avatar=null;error(e);status('No se pudo cargar el tutor. Regresa y vuelve a intentarlo.');controls();}
}
function cancelRecording(){recordingEpoch++;clearInterval(silenceTimer);if(recorder){recorder.onstop=null;recorder.stop();recorder=null;}micStream?.getTracks().forEach(t=>t.stop());micStream=null;micSource?.disconnect();micSource=null;$('mic').textContent='🎙 Hablar';}
function stop(){epoch++;controller?.abort();controller=null;audioController?.abort();audioController=null;colaVoz=[];vozActiva=false;audio.pause();audio.removeAttribute('src');audio.load();if(audioURL){URL.revokeObjectURL(audioURL);audioURL=null;}cancelRecording();busy=false;phase('Tu turno');controls();status('Puedes continuar cuando quieras.');}
$('stop').onclick=stop;
$('back').onclick=()=>{selection++;stop();avatar?.dispose();avatar=null;$('session').hidden=true;$('selection').hidden=false;};
$('topic').onchange=()=>{stop();history=[];lastReply='';$('messages').replaceChildren();ideas([]);bubble(`${tutor.name} iniciará esta situación.`,'feedback');void requestTutor('',true);};
function bubble(text,kind=''){const e=el('div','bubble '+kind,text);$('messages').append(e);e.scrollIntoView({block:'nearest'});return e;}
// Tarjeta de corrección: lo que dijiste (tachado), la forma correcta y por qué.
function correccion(c){const card=el('div','correccion');const fila=el('div','correccion-fila');fila.append(el('s',null,c.original),el('span','flecha','→'),el('strong',null,c.correcto));card.append(el('span','correccion-titulo','Corrección'),fila);if(c.explicacion)card.append(el('small',null,c.explicacion));$('messages').append(card);card.scrollIntoView({block:'nearest'});}
// Ideas para responder: frases cortas que el alumno puede decir o escribir.
function ideas(lista){const box=$('ideas');box.replaceChildren();box.hidden=!lista.length;if(!lista.length)return;box.append(el('span','ideas-titulo','Ideas para responder'));for(const s of lista){const b=el('button','idea',s);b.type='button';b.onclick=()=>{$('text').value=s;$('text').focus();};box.append(b);}}
function completarRespuesta(burbuja,r){
 if(r.romanizacion)burbuja.append(el('span','romanizacion',r.romanizacion));
 if(r.traduccion){const d=el('details','traduccion');d.append(el('summary',null,'Ver traducción'),el('span',null,r.traduccion));burbuja.append(d);}
}
function audioURLPara(text){const url=new URL(config.api+'/voz/stream');url.search=new URLSearchParams({texto:text.slice(0,600),idioma:language(),voz:'avatar_'+tutor.id});return url;}
async function speak(text,version){
 audioController?.abort();audioController=new AbortController();const signal=audioController.signal;colaVoz=[];vozActiva=true;audio.pause();if(audioURL)URL.revokeObjectURL(audioURL);
 const url=audioURLPara(text);
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
 }catch(e){if(version===epoch&&!signal.aborted){error(e);vozActiva=false;siguienteFrase(version);}}
}
// Frases 2, 3…: se descargan ya (en paralelo a la que suena) y se encolan.
function encolarFrase(text,version){
 if(!vozActiva&&!colaVoz.length){speak(text,version);return;}
 const signal=audioController?.signal;
 const blob=fetch(audioURLPara(text),{headers:headers(),signal}).then(r=>{if(!r.ok)throw Error(`La voz no está disponible (${r.status}).`);return r.blob();});
 blob.catch(()=>{});colaVoz.push({text,blob});
 if(!vozActiva)siguienteFrase(version);
}
async function siguienteFrase(version){
 const item=colaVoz.shift();if(!item||version!==epoch)return;vozActiva=true;
 try{const b=await item.blob;if(version!==epoch)return;if(audioURL)URL.revokeObjectURL(audioURL);audioURL=URL.createObjectURL(b);audio.src=audioURL;await audio.play();}
 catch(e){if(version===epoch&&!audioController?.signal.aborted){vozActiva=false;siguienteFrase(version);}}
}
audio.onplaying=()=>{const now=performance.now();phase(`${tutor?.name||'El tutor'} está hablando`,'speaking');status('Escucha al tutor. Puedes interrumpir para responder.');audio.dataset.playedAt=now;const turn=Number(audio.dataset.turnStartedAt);if(turn&&!audio.dataset.firstAudioMs)audio.dataset.firstAudioMs=Math.round(now-turn);};
audio.onended=()=>{if(colaVoz.length){siguienteFrase(epoch);return;}vozActiva=false;phase('Tu turno');status('Te toca. Puedes escribir o hablar.');};
audio.onerror=()=>{if(audio.getAttribute('src')){phase('Voz no disponible','error');error('No se pudo reproducir la voz. Revisa tu conexión y pulsa Repetir voz.');}};
$('replay').onclick=async()=>{if(!lastReply||busy)return;await ensureAudio();speak(lastReply,epoch)};
$('form').onsubmit=event=>{event.preventDefault();send()};
async function send(){const text=$('text').value.trim();if(!text||busy||!config?.token)return;await requestTutor(text,false);}
async function requestTutor(text,opening=false){if(busy||!config?.token||!tutor||!avatar)return;await ensureAudio();if(!opening)stop();const version=epoch;busy=true;controls();$('error').textContent='';ideas([]);if(!opening){$('text').value='';bubble(text,'mine');history.push({rol:'alumno',texto:text});}let answer=null,replied=false,frases=0;controller=new AbortController();const current=controller;const timeout=setTimeout(()=>current.abort(),45000);const turnStarted=performance.now();audio.dataset.turnStartedAt=turnStarted;delete audio.dataset.firstAudioMs;delete audio.dataset.replyReadyMs;delete audio.dataset.firstSentenceMs;phase(opening?`${tutor.name} inicia la conversación`:'Pensando','thinking');status(opening?`${tutor.name} está preparando el saludo…`:'El tutor está preparando su respuesta…');
 const u=units.find(u=>u.id===Number($('topic').value));
 try{const response=await fetch(config.api+'/chat',{method:'POST',headers:{...headers(),'Content-Type':'application/json','Accept':'text/event-stream'},signal:current.signal,body:JSON.stringify({idiomaMeta:language(),idiomaNativo:config.idiomaNativo,nivel:config.nivel,tutorId:'avatar_'+tutor.id,historial:history.slice(-30),objetivo:config.contexto,...(u?{situacionId:u.id,situacion:u.nombre}: {})})});
  if(!response.ok)throw Error(response.status===401?'Tu sesión ha caducado. Vuelve a iniciar sesión.':`No se pudo conectar con el tutor (${response.status}).`);
  const reader=response.body.getReader(),decoder=new TextDecoder();let pending='',final=false;
  function event(raw){if(version!==epoch)return;const line=raw.split('\n').find(l=>l.startsWith('data: '));if(!line)return;const e=JSON.parse(line.slice(6));if(e.tipo==='error')throw Error(e.data);
   // Cada frase terminada se muestra y se dice sin esperar al resto.
   if(e.tipo==='frase'&&!replied){if(!frases){audio.dataset.firstSentenceMs=Math.round(performance.now()-turnStarted);answer=bubble('');}answer.textContent=(answer.textContent+' '+e.data.texto).trim();frases++;encolarFrase(e.data.texto,version);}
   if(e.tipo==='reply'&&!replied){replied=true;audio.dataset.replyReadyMs=Math.round(performance.now()-turnStarted);lastReply=e.data;if(frases)answer.textContent=e.data;else{answer=bubble(e.data);speak(e.data,version);}}
   if(e.tipo==='final'){final=true;const r=e.data;if(!replied&&!frases){answer=bubble(r.reply);speak(r.reply,version);}else answer.textContent=r.reply;lastReply=r.reply;completarRespuesta(answer,r);history.push({rol:'tutor',texto:r.reply});for(const c of r.corrections||[])correccion(c);ideas((r.suggestions||[]).slice(0,3));controls();}
  }
  while(true){const {done,value}=await reader.read();if(done)break;pending+=decoder.decode(value,{stream:true});const parts=pending.split('\n\n');pending=parts.pop();for(const p of parts)event(p);}if(!final)throw Error('La respuesta quedó incompleta. Puedes volver a intentarlo.');
 }catch(e){if(version===epoch){phase('No se pudo responder','error');error(e.name==='AbortError'?'El tutor tardó demasiado. Puedes volver a intentarlo.':e);if(!replied&&!frases&&!opening){$('text').value=text;history.pop();}}}
 finally{clearTimeout(timeout);if(version===epoch){busy=false;controller=null;controls();}}
}
// Terminar la llamada: resumen con logros, correcciones, vocabulario y el
// siguiente paso. El servidor guarda los «hechos del alumno» para personalizar
// la próxima llamada.
$('end').onclick=async()=>{
 if(busy||!history.some(t=>t.rol==='alumno'))return;stop();const version=epoch;busy=true;controls();phase('Preparando tu resumen','thinking');status('Preparando el resumen de la llamada…');
 try{const r=await fetch(config.api+'/chat/resumen',{method:'POST',headers:{...headers(),'Content-Type':'application/json'},body:JSON.stringify({idiomaMeta:language(),idiomaNativo:config.idiomaNativo,nivel:config.nivel,tutorId:'avatar_'+tutor.id,historial:history.slice(-40)})});
  if(!r.ok)throw Error('No se pudo preparar el resumen. Puedes seguir practicando.');const d=await r.json();if(version!==epoch)return;
  const card=el('div','resumen');card.append(el('h3',null,'Resumen de la llamada'));
  const seccion=(titulo,items)=>{if(!items.length)return;card.append(el('h4',null,titulo));const ul=el('ul');for(const i of items)ul.append(i);card.append(ul);};
  seccion('Lo hiciste bien',(d.logros||[]).map(t=>el('li',null,t)));
  seccion('Para mejorar',(d.mejorar||[]).map(m=>{const li=el('li');li.append(el('s',null,m.original),document.createTextNode(' → '),el('strong',null,m.correcto),el('small',null,m.explicacion));return li;}));
  seccion('Vocabulario de hoy',(d.vocabulario||[]).map(v=>{const li=el('li');li.append(el('strong',null,v.palabra),document.createTextNode(' · '+v.significado));return li;}));
  if(d.siguientePaso)card.append(el('p','siguiente',d.siguientePaso));
  $('messages').append(card);card.scrollIntoView({block:'nearest'});phase('Llamada terminada');status(`${tutor.name} recordará esto en tu próxima llamada.`);
 }catch(e){if(version===epoch){phase('Tu turno');error(e);}}
 finally{if(version===epoch){busy=false;controls();}}
};
$('mic').onclick=async()=>{
 if(recorder){recorder.stop();return;}if(busy)return;await ensureAudio();stop();const version=epoch,myRecording=++recordingEpoch;$('error').textContent='';
 try{const stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true},video:false});if(version!==epoch){stream.getTracks().forEach(t=>t.stop());return;}micStream=stream;
 const mime=['audio/webm;codecs=opus','audio/mp4','audio/webm'].find(t=>MediaRecorder.isTypeSupported(t));recorder=new MediaRecorder(stream,mime?{mimeType:mime}:{});const current=recorder,chunks=[],source=ctx.createMediaStreamSource(stream),meter=ctx.createAnalyser();meter.fftSize=1024;source.connect(meter);micSource=source;const samples=new Float32Array(meter.fftSize);let spoken=false,lastSpeech=performance.now(),start=lastSpeech;
 current.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
 current.onstop=async()=>{clearInterval(silenceTimer);source.disconnect();stream.getTracks().forEach(t=>t.stop());recorder=null;micStream=null;$('mic').textContent='🎙 Hablar';if(version!==epoch||myRecording!==recordingEpoch)return;busy=true;controls();status('Transcribiendo tu mensaje…');phase('Pensando','thinking');const transcribe=new AbortController();controller=transcribe;const timer=setTimeout(()=>transcribe.abort(),30000);let autoSend=false;
  try{const blob=new Blob(chunks,{type:current.mimeType});if(!spoken||blob.size<300)throw Error('No se detectó voz. Inténtalo de nuevo más cerca del micrófono.');const form=new FormData();form.append('idioma',language());form.append('audio',blob,current.mimeType.includes('mp4')?'turn.m4a':'turn.webm');const r=await fetch(config.api+'/transcribir',{method:'POST',headers:headers(),body:form,signal:transcribe.signal});if(!r.ok)throw Error('No se pudo transcribir. Puedes escribir tu mensaje.');const data=await r.json();if(version!==epoch)return;$('text').value=data.texto||'';autoSend=!!data.texto&&!$('review').checked;status('Revisa tu mensaje y pulsa Enviar.');}
  catch(e){if(version===epoch){error(e);phase('Tu turno');}}finally{clearTimeout(timer);if(version===epoch){busy=false;controller=null;controls();}}
  if(autoSend&&version===epoch)send();
 };
 current.start();$('mic').textContent='■ Terminar';phase('Te escucho','listening');status('Habla con calma. Se envía cuando dejas de hablar (o pulsa Terminar).');controls();
 silenceTimer=setInterval(()=>{meter.getFloatTimeDomainData(samples);let sum=0;for(const x of samples)sum+=x*x;const now=performance.now();if(Math.sqrt(sum/samples.length)>.012){spoken=true;lastSpeech=now;}if((spoken&&now-lastSpeech>=FIN_SILENCIO_MS)||(!spoken&&now-start>15000)||now-start>60000){clearInterval(silenceTimer);if(current.state==='recording')current.stop();}},100);
 }catch(e){cancelRecording();error(e.name==='NotAllowedError'?'Activa el permiso del micrófono en tu navegador.':e);controls();}
};
window.addEventListener('offline',()=>{stop();error('No hay conexión. Tus mensajes se conservan en esta conversación.');});
window.addEventListener('pagehide',()=>{stop();avatar?.dispose();ctx?.close();});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
controls();
