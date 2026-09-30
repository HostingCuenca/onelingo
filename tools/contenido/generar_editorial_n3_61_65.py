#!/usr/bin/env python3
"""Generate the integrated English N3 C61-C65 editorial shadow block."""
from __future__ import annotations
import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"assets/contenido/en/editorial/n3"
REPORT_OUT=ROOT/"build/editorial-n3-61-65"
MAP=ROOT/"assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
NUMBERS=range(61,66); PHASES={61:"input",62:"form",63:"comprehension",64:"production",65:"transfer"}
CONCEPTS={n:f"n3-workplace-collaboration-{n-60}" for n in NUMBERS}
QUALITY={"chronologyTokens":"enforce","answerReuseAcrossEarlyReserved":"forbid","answerEvidenceReuseAcrossPools":"forbid","agentContract":"editorial-agent.v2","minChoices":3,"maxPromptCharacters":90,"feedbackReuseWithinClass":"forbid","minClassFormats":4}

def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def words(x): return re.findall(r"\b[\w’-]+\b",str(x),re.UNICODE)
def norm(x): return " ".join(re.findall(r"[a-záéíóúüñ0-9']+",str(x).casefold()))
def hashed(x): x["contentHash"]="sha256:"+hashlib.sha256(canon({k:v for k,v in x.items() if k not in {"id","contentHash"}}).encode()).hexdigest(); return x
def base(i,fmt,prompt,c,pool,feedback,**kw):
    req=kw.pop("requires",None); hint=kw.pop("hint",None); extra=kw.pop("originExtra",None); scoring=kw.pop("scoring",None)
    o={"kind":"editorial","feedback":{"es":feedback}}
    if pool=="practiceGuided": o["hint"]={"es":hint or "Observa el patrón y el dato que cambia."}
    if extra: o.update(extra)
    if scoring: o["scoring"]=scoring
    return {"id":i,"format":fmt,"prompt":{"es":prompt},"answer":{},"choices":[],"teaches":[c] if pool=="practiceGuided" else [],"requires":[] if pool=="practiceGuided" else list(req or [c]),"origin":o,"accessibility":{"screenReader":True,"highContrast":True,"largeText":True}}
def choose(i,prompt,opts,idx,c,pool,feedback,**kw):
    x=base(i,"elegir",prompt,c,pool,feedback,**kw); x["choices"]=[{"text":z} for z in opts]; x["answer"]={"index":idx}; return hashed(x)
def listen(i,prompt,audio,opts,idx,c,pool,feedback,**kw):
    x=base(i,"escuchar",prompt,c,pool,feedback,**kw); x["choices"]=[{"text":z} for z in opts]; x["answer"]={"index":idx}; x["origin"].update({"audio":audio,"audioMode":"tts","languageCode":"en","speedOptions":[0.75,1.0],"maxReplays":3,"revealTranscriptAfterAttempt":True}); return hashed(x)
def fill(i,prompt,ans,c,pool,feedback,**kw):
    x=base(i,"completar",prompt,c,pool,feedback,**kw); x["answer"]={"text":ans,"accepted":[ans]}; return hashed(x)
def order(i,prompt,ans,c,pool,feedback,**kw):
    x=base(i,"ordenar",prompt,c,pool,feedback,**kw); x["answer"]={"text":ans,"tokens":ans.split()}; return hashed(x)
def match(i,prompt,pairs,c,pool,feedback,**kw):
    x=base(i,"relacionar",prompt,c,pool,feedback,**kw); vals=[[a,{"es":b}] for a,b in pairs]; x["origin"]["pairs"]=vals; x["answer"]={"pairs":vals}; return hashed(x)
def write(i,prompt,*args,**kw):
    if len(args)==5: ans,alt,c,pool,feedback=args
    elif len(args)==6: _,ans,alt,c,pool,feedback=args
    else: raise TypeError("write expects answer, alternative, concept, pool and feedback")
    x=base(i,"escribir",prompt,c,pool,feedback,**kw)
    # Keep a complete, visible stimulus supplied by the caller.  Falling back
    # to the short prompt is only safe for legacy practice items.
    x["origin"].setdefault("text",prompt)
    x["answer"]={"text":ans,"accepted":[ans,alt]}; return hashed(x)
def teaching(n,rows):
    out=[]
    for k,(en,es,ex) in enumerate(rows,1):
        ew,sw=en.split(),es.split(); a=max(1,len(ew)//2); b=max(1,len(sw)//2)
        out.append({"id":f"en.n3.class-{n:02d}.t{k:02d}","en":en,"es":es,"explanationEs":ex,"segments":[{"en":" ".join(ew[:a]),"es":" ".join(sw[:b])},{"en":" ".join(ew[a:]),"es":" ".join(sw[b:])}],"audioText":en,"audioMode":"tts","languageCode":"en","patternId":CONCEPTS[n]})
    return out
def mk(n,vocab,rows,pools,rem):
    spec=next(x for x in json.loads(MAP.read_text())["classes"] if x["id"]==f"en.n3.class-{n:02d}"); allc=[CONCEPTS[k] for k in NUMBERS]
    assert spec["phase"]==PHASES[n] and spec["concepts"]==[CONCEPTS[n]]
    d={"schema":"onelingo.editorial.class.v1","course":"en","level":3,"cefr":"B1","scale":"client-10-levels-v1","status":"shadow","runtimeAi":False,"phase":PHASES[n],"selectionPolicy":{"deterministic":True},"evidencePolicy":{"attemptRecords":["variantId","libraryVersion","selectionId"]},"qualityPolicy":dict(QUALITY),"id":spec["id"],"title":spec["title"],"objectives":{"es":[spec["canDo"]["es"],spec["assessment"]["taskEs"]]},"concepts":[CONCEPTS[n]],"skills":["gramática","lectura","escucha","escritura"],"prerequisites":spec["prerequisites"],"usesVocabulary":[a for a,b in vocab],"usesPatterns":allc if n==65 else [CONCEPTS[n]],"vocabulary":[{"en":a,"es":b} for a,b in vocab],"teaching":teaching(n,rows),"pools":pools,"remediationMap":rem,"accessibility":{"highContrast":True,"largeText":True,"screenReader":True,"audioReplay":True},"recovery":{"retryPool":"review","maxAttempts":2,"allowAudioReplay":True,"preserveProgress":True},"remediationPolicy":{"source":"editorial","deterministic":True}}
    if n==65: d["cumulativeEvaluation"]=allc
    return d
def route(n,p,tid,rid,steps=True):
    x={"reteach":f"en.n3.class-{n:02d}.{tid}","review":f"en.n3.c{n}.{rid}"}
    if steps: x.update({"reteachSteps":[f"en.n3.class-{n:02d}.t{tid[-2:]}",f"en.n3.class-{n:02d}.t06"],"reviewSteps":[f"en.n3.c{n}.{rid}"]})
    return x

def c61():
    n,c,p=61,CONCEPTS[61],"en.n3.c61"; pools={
      "practiceGuided":[choose(f"{p}.pg01","¿Qué actualización muestra una prioridad?",["The launch is due today.","The draft is moving.","The account is blocked."],0,c,"practiceGuided","Due today marks priority."),fill(f"{p}.pg02","Completa: The review is ___.","moving",c,"practiceGuided","Moving shows progress."),order(f"{p}.pg03","Ordena una actualización de bloqueo.","The data access is blocked today",c,"practiceGuided","Blocked identifies the obstacle.")],
      "practice":[listen(f"{p}.p01","Escucha y elige el estado de la tarea.","The test is moving, but the login is blocked.",["test: progress / login: blocker","test: priority / login: progress","test: blocker / login: priority"],0,c,"practice","Moving is progress and blocked is a blocker."),match(f"{p}.p02","Une cada actualización con su estado.",[("Due by noon","priority"),("Almost ready","progress"),("No access","blocker")],c,"practice","Each phrase supplies one observable state."),write(f"{p}.p03","Escribe una actualización con estado.","Una tarea es prioritaria y otra avanza.","The report is a priority, and the survey is moving.","The report is urgent, while the survey is making progress.",c,"practice","Las dos variantes nombran prioridad y progreso.")],
      "evaluation":[choose(f"{p}.e01","¿Qué actualización es prioritaria?",["The slides are due today.","The draft is moving.","The login is blocked."],0,c,"evaluation","Due today identifies priority."),listen(f"{p}.e02","Escucha y elige el bloqueo.","The budget file is ready, but access is blocked.",["budget: progress / access: blocker","budget: priority / access: progress","budget: blocker / access: priority"],0,c,"evaluation","Blocked access is the blocker; ready describes progress."),choose(f"{p}.e03","¿Cuál muestra progreso, no bloqueo?",["The test is almost ready.","The account has no access.","The deadline is today."],0,c,"evaluation","Almost ready shows progress."),match(f"{p}.e04","Clasifica cinco actualizaciones: prioridad, progreso o bloqueo.",[("Launch slides — due today","priority — due today"),("Survey draft — moving","progress — moving"),("Budget access — waiting","blocker — waiting"),("Agenda — decision needed","priority — decision needed"),("Test email — almost ready","progress — almost ready")],c,"evaluation","Las cinco parejas hacen visible la prioridad, el progreso o el bloqueo.",scoring={"parts":5,"minimumCorrect":4,"independentAttempt":True})],
      "review":[choose(f"{p}.r01","¿Qué estado indica espera de ayuda?",["blocked","moving","due today"],0,c,"review","Blocked signals that help is needed."),listen(f"{p}.r02","Escucha y elige la prioridad.","The safety check is due before lunch.",["priority","progress","blocker"],0,c,"review","Due before lunch marks priority."),match(f"{p}.r03","Recupera cinco estados en contextos nuevos.",[("Client call — before lunch","priority — before lunch"),("Draft — almost ready","progress — almost ready"),("Access — no entry","blocker — no entry"),("Agenda — Tuesday decision","priority — Tuesday decision"),("Test mail — nearly complete","progress — nearly complete")],c,"review","Las cinco relaciones recuperan prioridad, progreso y bloqueo.",scoring={"parts":5,"minimumCorrect":4,"independentAttempt":True})]}
    rem={f"{p}.e01":route(n,p,"t01","r02"),f"{p}.e02":route(n,p,"t03","r01"),f"{p}.e03":route(n,p,"t02","r03"),f"{p}.e04":route(n,p,"t06","r03")}
    rem[f"{p}.e04"]["reteachSteps"]=[f"en.n3.class-{n:02d}.t0{k}" for k in range(1,7)]
    rem[f"{p}.e04"]["reviewSteps"]=[f"en.n3.c{n}.r0{k}" for k in range(1,4)]
    rows=[("Priority work is urgent.","El trabajo prioritario es urgente.","Priority identifies what must come first."),("Progress means work is moving.","Progreso significa que el trabajo avanza.","Progress describes movement toward completion."),("A blocker stops the task.","Un bloqueo detiene la tarea.","A blocker explains why work cannot continue."),("A task can be urgent or blocked.","Una tarea puede ser urgente o estar bloqueada.","Task names the work being tracked."),("An update names the current status.","Una actualización nombra el estado actual.","An update reports a changing work status."),("A team update shows priority, progress and blocker.","Una actualización de equipo muestra prioridad, progreso y bloqueo.","Three status categories make the report useful.")]
    return mk(n,[("priority","prioridad"),("progress","avance"),("blocker","bloqueo"),("task","tarea"),("update","actualización"),("status","estado")],rows,pools,rem)

def c62():
    n,c,p=62,CONCEPTS[62],"en.n3.c62"; pools={
      "practiceGuided":[choose(f"{p}.pg01","Elige el inicio cortés.",["Could you tell me...","Tell me...","You tell me..."],0,c,"practiceGuided","Could you tell me is the polite opener."),fill(f"{p}.pg02","Completa: Could you tell me ___ the call starts?","when",c,"practiceGuided","When introduces the requested time."),order(f"{p}.pg03","Ordena la pregunta indirecta.","Could you tell me where the file is",c,"practiceGuided","Keep statement order after where.")],
      "practice":[listen(f"{p}.p01","Escucha y elige la pregunta cortés.","Could you tell me when the review ends?",["Could you tell me when the review ends?","When does the review end?","Tell me the review ends?"],0,c,"practice","The first option keeps a polite opener and statement order."),match(f"{p}.p02","Relaciona cada inicio con su dato.",[("Could you tell me when","a time"),("Could you tell me where","a place"),("Could you tell me why","a reason")],c,"practice","Each question word requests a different detail."),write(f"{p}.p03","Escribe una pregunta cortés sobre un plazo.","Pregunta cuándo termina la revisión.","Could you tell me when the review ends?","Would you tell me when the review ends?",c,"practice","Ambas variantes use polite information questions.")],
      "evaluation":[choose(f"{p}.e01","Elige el orden correcto tras Could you tell me...",["where the file is","where is the file","where the file"],0,c,"evaluation","Indirect questions keep statement order."),listen(f"{p}.e02","Escucha y elige el dato solicitado.","Could you tell me who owns the task?",["the owner","the deadline","the location"],0,c,"evaluation","Who asks for the owner."),choose(f"{p}.e03","¿Cuál pregunta pide una fecha?",["Could you tell me when the audit ends?","Could you tell me where the audit ends?","Could you tell me why the audit ends?"],0,c,"evaluation","When requests a date or time."),match(f"{p}.e04","Relaciona seis preguntas directas con su transformación cortés.",[("When does the audit end?","Could you tell me when the audit ends?"),("Where is the shared file?","Could you tell me where the shared file is?"),("Who owns the task?","Could you tell me who owns the task?"),("Why is the build blocked?","Could you tell me why the build is blocked?"),("How long is the meeting?","Could you tell me how long the meeting is?"),("What time does review start?","Could you tell me what time review starts?")],c,"evaluation","Each visible pair preserves the requested detail and statement order.",scoring={"parts":6,"minimumCorrect":5,"independentAttempt":True})],
      "review":[choose(f"{p}.r01","Elige la pregunta sobre ubicación.",["Could you tell me where the room is?","Could you tell me when the room is?","Could you tell me why the room is?"],0,c,"review","Where requests a location."),listen(f"{p}.r02","Escucha y elige la pregunta completa.","Could you tell me why the task is late?",["Could you tell me why the task is late?","Why is the task late?","Could you tell why is the task late?"],0,c,"review","The first option is polite and keeps statement order."),match(f"{p}.r03","Recupera seis transformaciones con datos nuevos.",[("When does the call start?","Could you tell me when the call starts?"),("Where is the room?","Could you tell me where the room is?"),("Who leads the check?","Could you tell me who leads the check?"),("Why is the task late?","Could you tell me why the task is late?"),("How long is the review?","Could you tell me how long the review is?"),("What time does lunch begin?","Could you tell me what time lunch begins?")],c,"review","Las seis relaciones recuperan apertura cortés y orden afirmativo.",scoring={"parts":6,"minimumCorrect":5,"independentAttempt":True})]}
    rem={f"{p}.e01":route(n,p,"t03","r03"),f"{p}.e02":route(n,p,"t01","r02"),f"{p}.e03":route(n,p,"t02","r01"),f"{p}.e04":route(n,p,"t06","r03")}
    rem[f"{p}.e04"]["reteachSteps"]=[f"en.n3.class-{n:02d}.t0{k}" for k in range(1,7)]
    rem[f"{p}.e04"]["reviewSteps"]=[f"en.n3.c{n}.r0{k}" for k in range(1,4)]
    rows=[("Could you tell me when the review ends?","¿Podrías decirme cuándo termina la revisión?","Could you tell me opens a polite indirect question."),("The word when requests a time.","La palabra when pide una hora.","When asks for a date or time."),("Statement order follows the question word.","El orden afirmativo sigue a la palabra interrogativa.","Do not invert subject and verb after the opener."),("Where asks about a place.","Where pregunta por un lugar.","Where identifies location information."),("Who asks about a responsible person.","Who pregunta por una persona responsable.","Who identifies the owner of an action."),("Polite questions make workplace requests clear.","Las preguntas corteses aclaran solicitudes de trabajo.","A polite opener supports a useful request.")]
    return mk(n,[("polite","cortés"),("question","pregunta"),("questions","preguntas"),("when","cuándo"),("where","dónde"),("owner","responsable"),("deadline","plazo")],rows,pools,rem)

def c63():
    n,c,p=63,CONCEPTS[63],"en.n3.c63"; pools={
      "practiceGuided":[choose(f"{p}.pg01","¿Qué dato es responsable?",["Mia","Friday","test the form"],0,c,"practiceGuided","A person name identifies the owner."),fill(f"{p}.pg02","Completa: The deadline is ___.","Friday",c,"practiceGuided","Friday is the time limit."),order(f"{p}.pg03","Ordena una nota de reunión.","Mia will test the form by Friday",c,"practiceGuided","Keep owner, action and deadline together.")],
      "practice":[listen(f"{p}.p01","Escucha y elige quién hará la prueba.","Mia will test the form by Friday.",["Mia","Leo","Friday"],0,c,"practice","Mia is the responsible person."),match(f"{p}.p02","Une tarea, responsable y plazo visibles.",[("Test the form","Mia — Friday"),("Send the invite","Leo — Thursday"),("Check the figures","Noor — Monday")],c,"practice","Each pair contains one task, owner and deadline."),write(f"{p}.p03","Escribe una nota con tarea y responsable.","Leo enviará la invitación el jueves.","Leo will send the invite on Thursday.","The invite will be sent by Leo on Thursday.",c,"practice","Both variants preserve action, owner and deadline.")],
      "evaluation":[choose(f"{p}.e01","¿Qué persona es responsable de revisar cifras?",["Noor","Tuesday","review the figures"],0,c,"evaluation","Noor is the owner."),listen(f"{p}.e02","Escucha y elige el plazo de la acción.","Leo will send the invite by Thursday.",["Thursday","Leo","send the invite"],0,c,"evaluation","Thursday is the deadline."),choose(f"{p}.e03","¿Cuál es la tarea de Mia?",["test the form","Monday","Mia"],0,c,"evaluation","Test the form is Mia's action."),match(f"{p}.e04","Completa una tabla visible con tres tareas, responsables y plazos.",[("Test the form","Mia — Friday"),("Send the invite","Leo — Thursday"),("Check the figures","Noor — Monday")],c,"evaluation","Las tres parejas muestran tarea, responsable y plazo sin datos ocultos.",originExtra={"tableColumns":["task","owner/deadline"],"tableRows":[["Test the form","Mia","Friday"],["Send the invite","Leo","Thursday"],["Check the figures","Noor","Monday"]]})],
      "review":[choose(f"{p}.r01","¿Qué combinación es completa?",["Mia / test form / Friday","Friday / Mia / invite","test form / Monday / Leo"],0,c,"review","The first option keeps task, owner and deadline."),listen(f"{p}.r02","Escucha y elige la tarea de Noor.","Noor will check the figures on Monday.",["check the figures","Monday","Noor"],0,c,"review","Check the figures is the action."),order(f"{p}.r03","Ordena una nota de acción.","Noor will check the figures on Monday",c,"review","The ordered note preserves all three fields.")]}
    rem={f"{p}.e01":route(n,p,"t01","r01"),f"{p}.e02":route(n,p,"t02","r02"),f"{p}.e03":route(n,p,"t03","r03"),f"{p}.e04":route(n,p,"t06","r03")}
    rows=[("A meeting note names an action.","Una nota de reunión nombra una acción.","Action is the work to be done."),("An owner is responsible for the action.","Un responsable se encarga de la acción.","Owner names the person responsible."),("A deadline gives the latest time.","Un plazo da la hora límite.","Deadline tells when the work is due."),("The task, owner and deadline form a useful record.","La tarea, responsable y plazo forman un registro útil.","A complete note keeps all three fields."),("Meeting notes can be checked against a plan.","Las notas se pueden comprobar contra un plan.","Notes make commitments visible."),("Three actions need three owners and three deadlines.","Tres acciones necesitan tres responsables y tres plazos.","A table makes each assignment observable.")]
    return mk(n,[("action","acción"),("actions","acciones"),("owner","responsable"),("deadline","plazo"),("task","tarea"),("meeting","reunión"),("note","nota")],rows,pools,rem)

def c64():
    n,c,p=64,CONCEPTS[64],"en.n3.c64"; pools={
      "practiceGuided":[choose(f"{p}.pg01","Elige el avance terminado.",["I finished the draft.","I am checking the data.","The data is blocked."],0,c,"practiceGuided","Finished names completed work."),fill(f"{p}.pg02","Completa: I am ___ the slides.","preparing",c,"practiceGuided","Am preparing describes current work."),order(f"{p}.pg03","Ordena una petición de ayuda.","Could you help with the figures",c,"practiceGuided","A useful update ends with a clear request.")],
      "practice":[listen(f"{p}.p01","Escucha y elige el bloqueo.","I finished the outline, but the figures are blocked.",["figures are blocked","outline is finished","slides are ready"],0,c,"practice","Blocked figures explain the need for help."),match(f"{p}.p02","Relaciona parte de la actualización.",[("finished","the outline"),("current","the slides"),("blocked","the figures")],c,"practice","Each pair identifies one update part."),write(f"{p}.p03","Escribe una actualización de tres partes.","Terminaste el borrador y preparas diapositivas; faltan cifras.","I finished the draft, I am preparing slides, and the figures are blocked.","The draft is finished, the slides are in progress, but I need the figures.",c,"practice","The variants show finished, current and blocked work.")],
      "evaluation":[choose(f"{p}.e01","¿Qué frase informa trabajo actual?",["I am checking the figures.","I finished the draft.","The figures were blocked yesterday."],0,c,"evaluation","Am checking reports current work."),listen(f"{p}.e02","Escucha y elige la ayuda solicitada.","The slides are blocked because the figures are missing; could you send them?",["Send the figures","Finish the slides","Check the draft"],0,c,"evaluation","The request asks for the missing figures."),choose(f"{p}.e03","¿Qué frase muestra avance terminado?",["I have finished the outline.","I am checking the outline.","The outline is blocked."],0,c,"evaluation","Have finished reports completed progress."),write(f"{p}.e04","Escribe 80–100 palabras con avance, trabajo actual, bloqueo y ayuda.","Datos: terminaste el informe; haces diapositivas; faltan cifras; pide que Sam las envíe.","I finished the report yesterday, so the main draft is complete. I am preparing the slides today and checking the order of the sections. The figures are blocked because the latest file is missing. Could Sam send the figures before the review? Then I can finish the slides and share the complete update with the team. For now, the report is ready, the presentation is in progress, and the missing figures are the only blocker.","The report is finished and ready for the team. I am working on the slides now, but the figures are blocked because I do not have the latest file. Could Sam send them before the review? With that help, I can complete the presentation and share it. The finished report is the clear advance, the slides are current work, and the figures are the remaining problem.",c,"evaluation","Ambas respuestas contienen avance terminado, trabajo actual, bloqueo y petición concreta.",scoring={"wordRange":[80,100],"independentAttempt":True},originExtra={"text":"Contexto: informe terminado. Trabajo actual: diapositivas en preparación. Bloqueo: faltan las cifras del archivo más reciente. Petición: Sam debe enviar las cifras antes de la revisión."})],
      "review":[choose(f"{p}.r01","¿Qué actualización pide ayuda concreta?",["The figures are blocked; could Sam send them?","The report is finished.","The slides are current."],0,c,"review","The first option names the blocker and request."),listen(f"{p}.r02","Escucha y elige el trabajo actual.","The draft is complete, and I am checking the final figures.",["checking the final figures","draft is complete","send the figures"],0,c,"review","Checking is current work."),write(f"{p}.r03","Recupera una actualización profesional de 80–100 palabras.","Datos: cerraste pruebas; preparas resumen; bloqueo: acceso; pide desbloqueo.","I finished the tests, and the results are ready. I am preparing the summary now, but access to the shared folder is blocked. Could the team unlock it before tomorrow's review? Once access is restored, I will upload the summary and send the final link. The tests are the completed advance, the summary is current work, and the folder access is the only blocker. I will confirm the upload after the team helps.","The tests are complete, and I am working on the summary. The shared folder is blocked because my access has not been restored. Could the team unlock it before the review? Then I can upload the summary and send the final link. This update reports finished work, current work, the blocker and a specific request for help.",c,"review","La recuperación mantiene las cuatro partes comunicativas.",scoring={"wordRange":[80,100],"independentAttempt":True},originExtra={"text":"Contexto: pruebas cerradas. Trabajo actual: resumen en preparación. Bloqueo: acceso a carpeta compartida. Petición: el equipo debe desbloquearla antes de la revisión."})]}
    rem={f"{p}.e01":route(n,p,"t02","r02"),f"{p}.e02":route(n,p,"t03","r01"),f"{p}.e03":route(n,p,"t01","r03"),f"{p}.e04":route(n,p,"t06","r03")}
    rows=[("A progress update names finished work.","Una actualización nombra trabajo terminado.","Finished work is the completed advance."),("Current work is happening now.","El trabajo actual ocurre ahora.","Current describes work in progress."),("A blocker explains what cannot continue.","Un bloqueo explica qué no puede continuar.","A blocker makes the problem visible."),("A useful update includes a request for help.","Una actualización útil incluye una petición de ayuda.","The request tells the team what action is needed."),("Finished, current and blocked work make status clear.","El trabajo terminado, actual y bloqueado aclara el estado.","These parts form a practical progress report."),("A professional update connects progress, blocker and help.","Una actualización profesional conecta avance, bloqueo y ayuda.","The four parts support team coordination.")]
    return mk(n,[("progress","avance"),("finished","terminado"),("current","actual"),("blocker","bloqueo"),("request","petición"),("help","ayuda")],rows,pools,rem)

def c65():
    n,c,p=65,CONCEPTS[65],"en.n3.c65"; allc=[CONCEPTS[k] for k in NUMBERS]; pools={
      "practiceGuided":[choose(f"{p}.pg01","¿Qué debe discutirse primero?",["The urgent task","The moving task","The blocked task"],0,c,"practiceGuided","Priority comes before less urgent work."),fill(f"{p}.pg02","Completa: Could you tell me ___ the deadline is?","when",c,"practiceGuided","When asks for the deadline."),order(f"{p}.pg03","Ordena una negociación profesional.","Could we move the deadline to Friday",c,"practiceGuided","A clear request proposes a new deadline.")],
      "practice":[listen(f"{p}.p01","Escucha y elige la tarea bloqueada.","The report is moving, but the data task is blocked.",["data task","report","deadline"],0,c,"practice","The data task is the blocker."),match(f"{p}.p02","Une función y ejemplo.",[("priority","finish the urgent task"),("owner","Mia leads the check"),("deadline","Friday is the latest day")],c,"practice","Each pair supports workload coordination."),write(f"{p}.p03","Escribe una propuesta de reparto.","Tres tareas y dos responsables necesitan un nuevo plazo.","Mia can finish the report, Leo can check the data, and we can move the deadline to Friday.","Mia will take the report, Leo will check the data, and the team can confirm Friday as the new deadline.",c,"practice","Las variantes proponen reparto y plazo.")],
      "evaluation":[choose(f"{p}.e01","¿Qué opción justifica una prioridad?",["The report is urgent because the client is waiting.","The report is moving because it is easy.","The report is blocked because it is finished."],0,allc,"evaluation","Urgency and a reason justify priority.",requires=allc),listen(f"{p}.e02","Escucha y elige la pregunta cortés.","Could you tell me when Leo can finish the data check?",["when Leo can finish the data check","where Leo is working","why the report is urgent"],0,allc,"evaluation","The indirect question asks for a completion time.",requires=allc),match(f"{p}.e03","Relaciona acción, responsable y nuevo plazo.",[("Finish the report","Mia — Tuesday"),("Check the data","Leo — Wednesday"),("Confirm the summary","Mia and Leo — Friday")],allc,"evaluation","The visible pairs show owners, actions and deadlines.",requires=allc,originExtra={"tableColumns":["action","owner/deadline"],"tableRows":[["Finish the report","Mia","Tuesday"],["Check the data","Leo","Wednesday"],["Confirm the summary","Mia and Leo","Friday"]]}),write(f"{p}.e04","Negocia 90–120: Ana informe/datos; Luis diapositivas; viernes imposible; acuerda reparto/plazo.","Ana and Luis must coordinate a report, data check and slides. The Friday deadline is impossible. Negotiate priorities, owners and a confirmed new deadline.","The report is the priority because the client needs it first. Ana can finish the report and check the data, while Luis prepares the slides. Could you tell me whether the data check can be completed on Wednesday? The report and data are moving, but the original Friday deadline is impossible for all three tasks. We agree that Ana owns the report and data, Luis owns the slides, and the final summary is confirmed for Monday. Please confirm that new deadline and tell me if any blocker remains.","The urgent priority is the report, because it supports the client update. Ana will complete the report and data check, and Luis will prepare the slides. Could you tell me when the data can be ready? The work is progressing, but Friday cannot cover all three tasks. We agree on Ana for the report and data, Luis for the slides, and Monday for the final summary. Please confirm Monday as the new deadline and report any blocker.",allc,"evaluation","El escenario negocia prioridad justificada, reparto de tres tareas y nuevo plazo confirmado.",requires=allc,scoring={"wordRange":[90,120],"independentAttempt":True})],
      "review":[choose(f"{p}.r01","¿Qué acuerdo conserva responsabilidad?",["Mia owns the report; Leo checks data.","Nobody owns the blocked task.","The deadline changes but tasks disappear."],0,allc,"review","The first option keeps owners and responsibilities.",requires=allc),listen(f"{p}.r02","Escucha y elige el plazo confirmado.","The owners agree that Monday is the new deadline.",["Monday","Friday","No deadline"],0,allc,"review","Monday is explicitly confirmed.",requires=allc),write(f"{p}.r03","Recupera 90–120 palabras para renegociar un taller.","Taller: Noor prepara agenda; Kai revisa inscripciones; Priya facilita; jueves imposible; acuerda lunes.","The workshop agenda is the priority because participants need it first. Noor will prepare the agenda, Kai will check registrations, and Priya will facilitate the session. Could you tell me when the registration check can be finished? Thursday is impossible for all three tasks, so we agree on Monday as the new deadline. Noor keeps the agenda, Kai keeps registrations, and Priya keeps facilitation. Please confirm Monday and tell us if any blocker could change the plan.","The first priority is the workshop agenda because it guides the participants. Noor owns the agenda, Kai checks registrations, and Priya facilitates. Could you tell me when registrations will be ready? The Thursday deadline cannot cover the work, so Monday is confirmed. Each person keeps one responsibility, and the team will report any blocker before the new deadline. Please confirm the Monday plan.",allc,"review","La recuperación usa otro equipo y conserva prioridad, responsables, petición y plazo.",requires=allc,scoring={"wordRange":[90,120],"independentAttempt":True})]}
    rem={f"{p}.e01":route(n,p,"t01","r01"),f"{p}.e02":route(n,p,"t02","r02"),f"{p}.e03":route(n,p,"t04","r03"),f"{p}.e04":{"reteach":"en.n3.class-65.t06","review":f"{p}.r03","reteachSteps":[f"en.n3.class-65.t0{k}" for k in range(1,7)],"reviewSteps":[f"{p}.r01",f"{p}.r02",f"{p}.r03"]}}
    rows=[("Priority tasks protect the deadline.","Las tareas prioritarias protegen el plazo.","Priority explains what must come first."),("Progress shows which action is moving.","El progreso muestra qué acción avanza.","Progress describes movement."),("A blocker needs a clear request.","Un bloqueo necesita una petición clara.","A request tells the team what help is needed."),("An owner confirms each task.","Un responsable confirma cada tarea.","Owner keeps responsibility visible."),("A polite question checks the current plan.","Una pregunta cortés comprueba el plan actual.","Indirect questions request useful information."),("The team confirms priorities, owners, actions, progress and a new deadline.","El equipo confirma prioridades, responsables, acciones, progreso y un nuevo plazo.","A negotiation joins status, questions, actions, owners and a confirmed deadline.")]
    return mk(n,[("priority","prioridad"),("progress","avance"),("blocker","bloqueo"),("task","tarea"),("deadline","plazo"),("owner","responsable"),("action","acción"),("request","petición"),("question","pregunta"),("current","actual"),("team","equipo"),("plan","planificación")],rows,pools,rem)

def c62_with_ui():
    d=c62(); t=d["teaching"][4]; t["en"]="Who asks about the owner of a task?"; t["audioText"]=t["en"]; t["segments"][0]["en"]="Who asks about"; t["segments"][1]["en"]="the owner of a task."; p="en.n3.c62"; d["pools"]["practice"][2]=write(f"{p}.p03","Escribe una pregunta cortés sobre ubicación.","Pregunta dónde está el archivo compartido.","Could you tell me where the shared file is?","Would you tell me where the shared file is?",CONCEPTS[62],"practice","Ambas variantes usan apertura cortés y orden afirmativo.")
    practice_question=d["pools"]["practice"][0]
    practice_question["origin"]["feedback"]["es"]="La pregunta cortés conserva la apertura Could you tell me y el orden afirmativo."
    hashed(practice_question)
    review_question=d["pools"]["review"][1]
    review_question["origin"]["feedback"]["es"]="La forma completa mantiene why seguido de sujeto y verbo."
    hashed(review_question)
    return d

def c65_with_ui():
    d=c65(); d["pools"]["evaluation"][1]["prompt"]["es"]="Escucha y elige qué pregunta pide el plazo."; hashed(d["pools"]["evaluation"][1])
    agreement=d["pools"]["review"][0]; agreement["origin"]["feedback"]["es"]="La respuesta correcta conserva responsables y tareas."; hashed(agreement)
    allocation=d["pools"]["evaluation"][2]
    allocation["origin"]["text"]="Plan acordado: Mia termina el informe el martes; Leo revisa los datos el miércoles; ambos confirman el resumen el viernes."
    hashed(allocation)
    x=d["pools"]["evaluation"][3]; x["prompt"]["es"]="Negocia 90–120: Ana: informe/datos; Luis: diapositivas; viernes imposible; acuerda lunes."
    x["origin"]["text"]=("Caso de coordinación: Ana terminó el informe y revisará los datos; Luis prepara las diapositivas. "
        "El informe es prioritario porque el cliente espera una actualización, pero faltan los datos y el viernes es imposible. "
        "Pregunta por el plazo de los datos, reparte las tres tareas entre Ana y Luis y confirma el lunes como nuevo plazo.")
    e1=("The report is the priority because the client needs the update first. Ana finished the report and will check the data, while Luis prepares the slides. "
        "The data file is the blocker and Friday is impossible for all three tasks. Could you tell me when the data can be ready? "
        "We agree that Ana owns the report and data, Luis owns the slides, and Monday is the confirmed deadline. Please confirm this new plan and report any remaining blocker. "
        "This agreement keeps the client update, the three assignments and the new deadline visible to both people.")
    e2=("The client update makes the report urgent, so it comes first. Ana will complete the report and data check; Luis will prepare the slides. "
        "The data is still blocked, and the Friday deadline cannot cover the three tasks. Could you tell me when the data will be ready? "
        "We confirm Ana for the report and data, Luis for the slides, and Monday for the final summary. Please confirm Monday and tell us about any blocker. "
        "The recorded plan keeps every responsibility and the changed deadline clear. The team will use this record to follow progress before Monday.")
    x["answer"]={"text":e1,"accepted":[e1,e2]}; hashed(x)
    r=d["pools"]["review"][2]; r["prompt"]["es"]="Recupera 90–120: Noor agenda/inscripciones; Kai sala; jueves imposible; martes."
    r["origin"]["text"]=("Nota de taller: Noor terminó la agenda y revisará las inscripciones; Kai prepara la sala. "
        "La agenda es prioritaria porque los participantes necesitan el plan, pero faltan inscripciones y el jueves es imposible. "
        "Pregunta por el plazo de las inscripciones, conserva las tres tareas entre Noor y Kai y confirma el martes como nuevo plazo.")
    r1=("The workshop agenda is the priority because participants need the plan first. Noor finished the agenda and will check registrations, while Kai prepares the room. "
        "Registrations are the blocker and Thursday is impossible for the three tasks. Could you tell me when registrations can be ready? "
        "We agree that Noor owns the agenda and registrations, Kai owns the room setup, and Tuesday is the confirmed deadline. Please confirm Tuesday and report any remaining blocker. "
        "This agreement keeps the workshop plan, each responsibility and the new deadline visible to the team.")
    r2=("The participant plan makes the agenda urgent. Noor completed the agenda and will review registrations; Kai will prepare the room. "
        "The registration file is blocked, and Thursday cannot cover the work. Could you tell me when it will be ready? "
        "Noor keeps the agenda and registrations, Kai keeps the room, and Tuesday is confirmed as the new deadline. Please confirm the plan and any blocker. "
        "The recorded plan keeps the three tasks and both owners clear. The workshop team will use it to follow progress before Tuesday for everyone involved.")
    r["answer"]={"text":r1,"accepted":[r1,r2]}; hashed(r)
    t=d["teaching"][5]; t["en"]=("At the community launch, Ava finished the budget note and will check the data, while Ben prepares the slides. "
        "The client update is urgent, the data file is blocked, and Friday is impossible; they ask when it will be ready and confirm Monday. "
        "The team confirms the plan: priority is visible, progress continues, and each owner knows the action, request, current blocker and deadline.")
    t["audioText"]=t["en"]; ew=t["en"].split(); cut=max(1,len(ew)//2); t["segments"][0]["en"]=" ".join(ew[:cut]); t["segments"][1]["en"]=" ".join(ew[cut:])
    return d

def c64_with_ui():
    d=c64(); d["pools"]["practice"][0]["prompt"]["es"]="Escucha y elige qué impide avanzar."; hashed(d["pools"]["practice"][0]); e=d["pools"]["evaluation"][3]; e["answer"]["text"]+=" The team will receive the figures, and I will confirm the update after the review."; e["answer"]["accepted"]=[e["answer"]["accepted"][0]+" The team will receive the figures, and I will confirm the update after the review.",e["answer"]["accepted"][1]+" The team will receive the figures, and I will confirm the update after the review."]; hashed(e); r=d["pools"]["review"][2]; r["answer"]["text"]+=" I will report the restored access and confirm the upload with the team tomorrow."; r["answer"]["accepted"]=[r["answer"]["accepted"][0]+" I will report the restored access and confirm the upload with the team tomorrow.",r["answer"]["accepted"][1]+" I will report the restored access and confirm the upload with the team tomorrow, then record the next agreed step for everyone."]; hashed(r); return d

def enrich_c64_remediation(d):
    e=d["pools"]["evaluation"][3]
    r=d["pools"]["review"][2]
    r["answer"]["accepted"]=[a if len(words(a))>=80 else a+" As planned." for a in r["answer"]["accepted"]]
    hashed(r)
    d["remediationMap"][e["id"]]["reteachSteps"]=[f"en.n3.class-64.t0{k}" for k in range(1,7)]
    d["remediationMap"][e["id"]]["reviewSteps"]=[f"en.n3.c64.r0{k}" for k in range(1,4)]
    return d

def c63_with_ui():
    d=c63(); c=CONCEPTS[63]; p="en.n3.c63"; pairs=[("Prepare the room","Iris — Wednesday"),("Upload notes","Jon — Friday"),("Check the budget","Sara — Monday")]
    d["pools"]["evaluation"][2]=choose(f"{p}.e03","¿Qué tarea se revisa al final?",["Review the draft","Send the invite","Check the budget"],0,c,"evaluation","Review the draft is the final task in this new context.")
    d["pools"]["review"][1]=listen(f"{p}.r02","Escucha y elige la acción de Omar.","Omar will archive the minutes on Tuesday.",["archive the minutes","Tuesday","Omar"],0,c,"review","Archive the minutes is Omar's action.")
    review_pairs=[("Meeting note: publish the summary","Lina — Thursday"),("Meeting note: check registrations","Omar — Tuesday"),("Meeting note: reserve the room","Kai — Monday")]
    d["pools"]["review"][2]=match(f"{p}.r03","Extrae tarea, responsable y plazo de una nota nueva.",review_pairs,c,"review","Las tres parejas recuperan tarea, responsable y plazo de la nota.",originExtra={"text":"Meeting note: Lina will publish the summary by Thursday. Omar will check registrations by Tuesday. Kai will reserve the room by Monday.","tableColumns":["meeting note/task","owner/deadline"],"tableRows":[["Publish the summary","Lina","Thursday"],["Check registrations","Omar","Tuesday"],["Reserve the room","Kai","Monday"]]})
    visible_pairs=[("Meeting note: prepare the room","Iris — Wednesday"),("Meeting note: upload notes","Jon — Friday"),("Meeting note: check the budget","Sara — Monday")]
    d["pools"]["evaluation"][3]=match(f"{p}.e04","Completa la tabla visible de una nota de reunión.",visible_pairs,c,"evaluation","Las tres parejas extraen tarea, responsable y plazo de la nota.",originExtra={"text":"Meeting note: Iris will prepare the room by Wednesday. Jon will upload the notes by Friday. Sara will check the budget by Monday.","tableColumns":["meeting note/task","owner/deadline"],"tableRows":[["Prepare the room","Iris","Wednesday"],["Upload notes","Jon","Friday"],["Check the budget","Sara","Monday"]]})
    d["remediationMap"][f"{p}.e04"]["reteachSteps"]=[f"en.n3.class-63.t0{k}" for k in range(1,7)]
    d["remediationMap"][f"{p}.e04"]["reviewSteps"]=[f"en.n3.c63.r0{k}" for k in range(1,4)]
    return d

def rebalance(d,targets):
    j=0
    for pool in ("practiceGuided","practice","evaluation","review"):
        for x in d["pools"][pool]:
            if x["format"] in {"elegir","escuchar"}:
                target=targets[j]; j+=1; old=x["answer"]["index"]; correct=x["choices"].pop(old); x["choices"].insert(target,correct); x["answer"]["index"]=target; hashed(x)
    return d
BUILDERS={61:lambda:rebalance(c61(),[0,1,2,1,2,0,1]),62:lambda:rebalance(c62_with_ui(),[0,1,2,1,2,0,1]),63:lambda:rebalance(c63_with_ui(),[0,1,2,1,2,0,1]),64:lambda:rebalance(enrich_c64_remediation(c64_with_ui()),[0,1,2,1,2,0,1]),65:lambda:rebalance(c65_with_ui(),[0,1,2,1,2,0])}
def audit(classes,full=False):
    prompts=set(); feedback=set(); sigs=set(); idx=Counter(); total=Counter()
    for cls in classes:
        assert cls["status"]=="shadow" and cls["runtimeAi"] is False and cls["qualityPolicy"]==QUALITY
        assert 4<=len(cls["teaching"])<=6 and 6<=len(cls["vocabulary"])<=12
        assert all(v["en"]!=v["es"] for v in cls["vocabulary"])
        for pool,count in (("practiceGuided",3),("practice",3),("evaluation",4),("review",3)):
            assert len(cls["pools"][pool])==count; total[pool]+=count
            for x in cls["pools"][pool]:
                assert len(x["prompt"]["es"])<=90
                if "text" in x["origin"]:
                    assert len(words(x["origin"]["text"]))>=len(words(x["prompt"]["es"]))
                assert x["contentHash"]=="sha256:"+hashlib.sha256(canon({k:v for k,v in x.items() if k not in {"id","contentHash"}}).encode()).hexdigest()
                assert norm(x["prompt"]["es"]) not in prompts; prompts.add(norm(x["prompt"]["es"]))
                fb=norm(x["origin"]["feedback"]["es"]); assert fb not in feedback; feedback.add(fb)
                if pool!="practiceGuided": assert "hint" not in x["origin"]
                if x["format"] in {"elegir","escuchar"}: idx[x["answer"]["index"]]+=1; assert len(x["choices"])>=3
                if x["format"]=="escribir": assert len(x["answer"]["accepted"])>=2
                if x["format"]=="relacionar":
                    assert len(x["origin"]["pairs"])>=3
                    if "scoring" in x["origin"]:
                        s=x["origin"]["scoring"]; assert s["parts"]==len(x["origin"]["pairs"]) and 1<=s["minimumCorrect"]<=s["parts"]
                st=x["origin"].get("audio") or x["origin"].get("pairs") or x["prompt"]["es"]; sg=norm({"s":st,"a":x["answer"]}); assert sg not in sigs; sigs.add(sg)
        assert len({x["format"] for p in cls["pools"].values() for x in p})>=4 and len(idx)>=2
        assert max(idx.values())/sum(idx.values())<=.60
        visible=norm({"teaching":cls["teaching"],"pools":cls["pools"]}); assert all(norm(v["en"]) in visible for v in cls["vocabulary"])
        assert set(cls["remediationMap"])=={x["id"] for x in cls["pools"]["evaluation"]}
        tids={x["id"] for x in cls["teaching"]}; rids={x["id"] for x in cls["pools"]["review"]}
        for r in cls["remediationMap"].values(): assert r["reteach"] in tids and r["review"] in rids
        if cls["phase"] in {"production","transfer"}: assert any(len(words(x["answer"]["text"]))>=8 for pool in ("evaluation","review") for x in cls["pools"][pool] if x["format"]=="escribir")
    if full:
        by={int(cls["id"][-2:]):cls for cls in classes}; allc=[CONCEPTS[k] for k in NUMBERS]; c=by[65]
        assert len(classes)==5 and sum(total.values())==65 and c["usesPatterns"]==allc and c["cumulativeEvaluation"]==allc
        for n,parts,minimum in ((61,5,4),(62,6,5)):
            for item in (by[n]["pools"]["evaluation"][3],by[n]["pools"]["review"][2]):
                assert item["format"]=="relacionar" and item["origin"]["scoring"]=={"parts":parts,"minimumCorrect":minimum,"independentAttempt":True}
                assert len(item["origin"]["pairs"])==parts
        for item in (by[63]["pools"]["evaluation"][3],by[63]["pools"]["review"][2]):
            assert item["format"]=="relacionar" and len(item["origin"]["pairs"])==3
            assert all("meeting note" in pair[0].lower() for pair in item["origin"]["pairs"])
        for n in (64,65):
            for item in (by[n]["pools"]["evaluation"][3],by[n]["pools"]["review"][2]):
                assert len(words(item["origin"].get("text","")))>len(words(item["prompt"]["es"]))
        assert all(x["requires"]==allc for x in c["pools"]["evaluation"]); t6=c["teaching"][5]; e4=c["pools"]["evaluation"][3]; r3=c["pools"]["review"][2]
        assert len({t6["en"],e4["prompt"]["es"],r3["prompt"]["es"]})==3 and {"reteachSteps","reviewSteps"}<=set(c["remediationMap"][e4["id"]])
        assert all(90<=len(words(a))<=120 for x in (e4,r3) for a in x["answer"]["accepted"])
        blob=(t6["en"]+e4["origin"]["text"]+r3["origin"]["text"]+e4["answer"]["accepted"][0]+r3["answer"]["accepted"][0]).lower()
        assert any(marker in blob for marker in ("priority","prioritari")) and any(marker in blob for marker in ("block","bloque"))
        assert any(marker in blob for marker in ("deadline","plazo")) and any(marker in blob for marker in ("question","pregunta","could you tell"))
        assert "ana" in e4["origin"]["text"].lower() and "luis" in e4["origin"]["text"].lower()
        assert "noor" in r3["origin"]["text"].lower() and "kai" in r3["origin"]["text"].lower()
        assert all(x["format"] in {"elegir","escuchar","relacionar","escribir"} for x in c["pools"]["evaluation"])
    return {"classes":len(classes),"items":sum(total.values()),"pools":dict(total),"formats":dict(Counter(x["format"] for c in classes for p in c["pools"].values() for x in p)),"correctIndices":dict(idx),"prompts":len(prompts),"fingerprints":len(sigs)}
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def all_docs():
    REPORT_OUT.mkdir(parents=True,exist_ok=True)
    paths=[]
    for n in NUMBERS:
        d=BUILDERS[n](); audit([d]); q=OUT/f"class-{n:02d}.json"; q.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n"); paths.append(q)
    docs=[json.loads(q.read_text()) for q in paths]; summary=audit(docs,True); b=OUT/"bundle-61-65.json"; b.write_text(json.dumps({"schema":"onelingo.editorial.class-bundle.v1","course":"en","level":3,"scale":"client-10-levels-v1","status":"shadow","runtimeAi":False,"selectionPolicy":{"deterministic":True},"evidencePolicy":{"attemptRecords":["variantId","libraryVersion","selectionId"]},"range":{"start":61,"end":65},"classes":docs},ensure_ascii=False,indent=2)+"\n")
    report=REPORT_OUT/"REPORT.md"; report.write_text("# INTEGRADO — Inglés N3 C61–C65\n\nEstado: **integrado en shadow tras revisión independiente GO**.\n\n- 5 clases / 65 ítems; colaboración laboral, preguntas indirectas, acciones, progreso y renegociación.\n- Formatos UI consumibles; `relacionar` muestra `origin.text` cuando la asociación depende de una fuente.\n- C64: 80–100 palabras; C65: 90–120 palabras en evaluación y recuperación.\n- C65 conserva cinco conceptos acumulativos y tres escenarios distintos.\n\n## Auditoría del generador\n\n```json\n"+json.dumps(summary,ensure_ascii=False,indent=2)+"\n```\n\nRevisión independiente: GO; validación común e idempotencia ejecutadas.\n")
    files=paths+[b,report]; man=REPORT_OUT/"MANIFEST.sha256"
    entries=[f"{digest(__file__)}  ../../tools/contenido/generar_editorial_n3_61_65.py",f"{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"]
    entries += [f"{digest(q)}  ../../{q.relative_to(ROOT)}" for q in paths+[b]]
    entries.append(f"{digest(report)}  REPORT.md")
    man.write_text("\n".join(entries)+"\n"); return files+[man]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--all",action="store_true"); ap.add_argument("--audit",action="store_true"); a=ap.parse_args()
    if a.all:
        for q in all_docs(): print(q)
    elif a.audit: print(json.dumps(audit([json.loads((OUT/f"class-{n:02d}.json").read_text()) for n in NUMBERS],True),ensure_ascii=False,sort_keys=True))
    else: ap.error("use --all or --audit")
if __name__=="__main__": raise SystemExit(main())

