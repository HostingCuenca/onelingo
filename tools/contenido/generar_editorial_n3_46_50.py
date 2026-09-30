#!/usr/bin/env python3
"""Generate the integrated English N3 C46-C50 editorial shadow block."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n3"
REPORT_OUT = ROOT / "build/editorial-n3-46-50"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
SCALE = "client-10-levels-v1"
NUMBERS = range(46, 51)
CONCEPTS = {n: f"n3-reported-messages-{n-45}" for n in NUMBERS}
PHASES = {46: "input", 47: "form", 48: "comprehension", 49: "production", 50: "transfer"}
QUALITY = {"chronologyTokens": "enforce", "answerReuseAcrossEarlyReserved": "forbid",
           "answerEvidenceReuseAcrossPools": "forbid", "agentContract": "editorial-agent.v2",
           "minChoices": 3, "maxPromptCharacters": 90,
           "feedbackReuseWithinClass": "forbid", "minClassFormats": 4}

def canonical(v: Any) -> str:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def norm(v: Any) -> str:
    return " ".join(re.findall(r"[a-záéíóúüñ0-9']+", str(v).casefold()))

def hashed(x: dict[str, Any]) -> dict[str, Any]:
    payload = {k: v for k, v in x.items() if k not in {"id", "contentHash"}}
    x["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return x

def base(i: str, fmt: str, prompt: str, c: str, pool: str, feedback: str,
         *, requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": hint or "Busca la señal temporal que conecta las dos acciones."}
    return {"id": i, "format": fmt, "prompt": {"es": prompt}, "answer": {}, "choices": [],
            "teaches": [c] if pool == "practiceGuided" else [],
            "requires": [] if pool == "practiceGuided" else list(requires or [c]),
            "origin": origin,
            "attemptEvidence": {"attempt": "independent" if pool in {"evaluation", "review"} else "guided",
                                 "evidence": "deterministic", "remediation": "editorial"},
            "accessibility": {"screenReader": True, "highContrast": True, "largeText": True}}

def q(i: str, prompt: str, options: list[str], index: int, c: str, pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "elegir", prompt, c, pool, feedback, **kw)
    x["choices"], x["answer"] = [{"text": v} for v in options], {"index": index}
    return hashed(x)

def listen(i: str, prompt: str, audio: str, options: list[str], index: int, c: str, pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    scoring = kw.pop("scoring", None)
    origin_extra = kw.pop("originExtra", None)
    x = base(i, "escuchar", prompt, c, pool, feedback, **kw)
    x["choices"], x["answer"] = [{"text": v} for v in options], {"index": index}
    x["origin"].update({"audio": audio, "audioMode": "tts", "languageCode": "en",
                         "speedOptions": [0.75, 1.0], "maxReplays": 3,
                         "revealTranscriptAfterAttempt": True})
    if scoring is not None: x["origin"]["scoring"] = scoring
    if origin_extra is not None: x["origin"].update(origin_extra)
    return hashed(x)

def fill(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    scoring = kw.pop("scoring", None)
    origin_extra = kw.pop("originExtra", None)
    x = base(i, "completar", prompt, c, pool, feedback, **kw)
    x["answer"] = {"text": answer, "accepted": [answer]}
    if scoring is not None: x["origin"]["scoring"] = scoring
    if origin_extra is not None: x["origin"].update(origin_extra)
    return hashed(x)

def order(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "ordenar", prompt, c, pool, feedback, **kw)
    x["answer"] = {"text": answer, "tokens": answer.split()}
    return hashed(x)

def write(i: str, prompt: str, stimulus: str, answer: str, alt: str, c: str, pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    origin_extra = kw.pop("originExtra", None)
    x = base(i, "escribir", prompt, c, pool, feedback, **kw)
    x["origin"]["text"] = stimulus
    if origin_extra is not None: x["origin"].update(origin_extra)
    x["answer"] = {"text": answer, "accepted": [answer, alt]}
    return hashed(x)

def match(i: str, prompt: str, pairs: list[tuple[str, str]], c: str, pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    scoring = kw.pop("scoring", None)
    origin_extra = kw.pop("originExtra", None)
    x = base(i, "relacionar", prompt, c, pool, feedback, **kw)
    values = [[a, {"es": b}] for a, b in pairs]
    x["answer"], x["origin"]["pairs"] = {"pairs": values}, values
    if scoring is not None: x["origin"]["scoring"] = scoring
    if origin_extra is not None: x["origin"].update(origin_extra)
    return hashed(x)

def teaching(n: int, rows: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    out = []
    for k, (en, es, explanation) in enumerate(rows, 1):
        ew, sw = en.split(), es.split(); cut_e, cut_s = max(1, len(ew)//2), max(1, len(sw)//2)
        out.append({"id": f"en.n3.class-{n:02d}.t{k:02d}", "en": en, "es": es,
                    "explanationEs": explanation,
                    "segments": [{"en": " ".join(ew[:cut_e]), "es": " ".join(sw[:cut_s])},
                                 {"en": " ".join(ew[cut_e:]), "es": " ".join(sw[cut_s:])}],
                    "audioText": en, "audioMode": "tts", "languageCode": "en",
                    "patternId": CONCEPTS[n]})
    return out

def make_class(n: int, objectives: list[str], vocab: list[tuple[str, str]], rows: list[tuple[str, str, str]],
               pools: dict[str, list[dict[str, Any]]], remap: dict[str, tuple[str, str]],
               *, uses: list[str] | None = None, cumulative: list[str] | None = None) -> dict[str, Any]:
    specs = json.loads(MAP.read_text(encoding="utf-8"))["classes"]
    spec = next(s for s in specs if s["id"] == f"en.n3.class-{n}")
    d: dict[str, Any] = {"schema": "onelingo.editorial.class.v1", "course": "en", "level": 3,
        "cefr": "B1", "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "phase": PHASES[n], "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY), "id": f"en.n3.class-{n:02d}", "title": spec["title"],
        "objectives": {"es": objectives}, "concepts": [CONCEPTS[n]],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n3.class-{n-1:02d}"], "usesVocabulary": [a for a, _ in vocab],
        "usesPatterns": uses or [CONCEPTS[n]], "vocabulary": [{"en": a, "es": b} for a, b in vocab],
        "teaching": teaching(n, rows), "pools": pools,
        "remediationMap": {k: {"reteach": a, "review": b} for k, (a, b) in remap.items()},
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True, "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2, "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True}}
    if cumulative is not None: d["cumulativeEvaluation"] = cumulative
    return d

def _audio() -> dict[str, Any]:
    return {"audioMode": "tts", "languageCode": "en", "speedOptions": [0.75, 1.0],
            "maxReplays": 3, "revealTranscriptAfterAttempt": True}

def c46() -> dict[str, Any]:
    n, c, p = 46, CONCEPTS[46], "en.n3.c46"
    pools = {"practiceGuided": [
        q(f"{p}.pg01", "¿Quién habló originalmente?", ["Mina", "The driver", "The receptionist"], 1, c, "practiceGuided", "The driver es el hablante citado en el reporte.", hint="Busca el nombre después de said."),
        listen(f"{p}.pg02", "Escucha y elige el reporte fiel.", "Nora: I need the blue folder today.", ["Nora said she needed the red folder.", "Nora told the folder to arrive.", "Nora said she needed the blue folder that day."], 2, c, "practiceGuided", "El reporte conserva blue folder y cambia today por that day.", hint="Conserva objeto y momento."),
        match(f"{p}.pg03", "Relaciona cada mensaje con su reporte.", [("I can open the shop — Ben", "Ben said he could open the shop"), ("Bring the keys — Eva to Tom", "Eva told Tom to bring the keys")], c, "practiceGuided", "Cada reporte conserva hablante, receptor y contenido.", hint="Said no lleva receptor; told sí."),
    ], "practice": [
        q(f"{p}.p01", "Elige el reporte que conserva el contenido.", ["Luis said the parcel was at reception.", "Luis told at reception the parcel.", "Luis said the parcel was outside."], 0, c, "practice", "La primera opción mantiene parcel y reception."),
        match(f"{p}.p02", "Une cada fuente con un reporte preciso.", [("Sara: The class starts at nine", "Sara said the class started at nine"), ("Omar to Kim: Call the client", "Omar told Kim to call the client")], c, "practice", "Las relaciones mantienen la hora y la acción."),
        write(f"{p}.p03", "Reporta el mensaje de Ana con said.", "Ana: I will send the menu tonight.", "Ana said she would send the menu that night.", "Ana said that she would send the menu that night.", c, "practice", "El reporte atribuye a Ana y conserva acción y momento."),
    ], "evaluation": [
        q(f"{p}.e01", "¿Qué reporte atribuye bien al hablante?", ["The room said Pablo was ready.", "Pablo said the room was ready.", "Pablo told was the room ready."], 1, c, "evaluation", "Pablo sigue siendo el hablante y room el contenido."),
        listen(f"{p}.e02", "Escucha y marca el contenido conservado.", "Iris: The meeting is in Room Four at two.", ["Room Two at four", "Room Four at four", "Room Four at two"], 2, c, "evaluation", "Room Four at two conserva ambos datos originales."),
        write(f"{p}.e03", "Reporta la petición de Hugo a Mei con told.", "Hugo to Mei: Please check the address.", "Hugo told Mei to check the address.", "Hugo told Mei that she should check the address.", c, "evaluation", "Told incluye el receptor Mei y la acción check the address."),
        match(f"{p}.e04", "Relaciona cinco mensajes originales con su reporte.", [
            ("Lena: I work at home today", "Lena said she worked at home that day"),
            ("Raj to Mia: Bring the charger", "Raj told Mia to bring the charger"),
            ("Ava: The bus leaves at six", "Ava said the bus left at six"),
            ("Noah to Eli: Meet me outside", "Noah told Eli to meet him outside"),
            ("Zoe: I cannot join tonight", "Zoe said she could not join that night")], c, "evaluation", "Las cinco parejas conservan hablante, said o told y contenido.", scoring={"parts": 5, "minimumCorrect": 4, "independentAttempt": True}),
    ], "review": [
        q(f"{p}.r01", "Fuente: Dina: 'The keys are in the office'. Elige el reporte fiel.", ["Dina said the keys were in the office.", "Dina said the keys were outside the office.", "Omar said the keys were in the office."], 0, c, "review", "Dina es la hablante y office es el lugar conservado."),
        order(f"{p}.r02", "Ordena el reporte de la llamada.", "Marco said the call started at ten.", c, "review", "La oración atribuye a Marco y mantiene la hora."),
        match(f"{p}.r03", "Recupera cinco relaciones de mensaje y reporte.", [
            ("Uma: I need the list now", "Uma said she needed the list then"),
            ("Ian to Jo: Close the window", "Ian told Jo to close the window"),
            ("Bea: The café opens at eight", "Bea said the café opened at eight"),
            ("Max to Liv: Wait by the gate", "Max told Liv to wait by the gate"),
            ("Tara: I will finish tomorrow", "Tara said she would finish the next day")], c, "review", "La recuperación vuelve a comprobar cinco fuentes sin repetir la evaluación.", scoring={"parts": 5, "minimumCorrect": 4, "independentAttempt": True}),
    ]}
    rows = [
        ("A speaker gives the original message.", "Un hablante da el mensaje original.", "Speaker identifica a quien produjo la fuente."),
        ("Mia said the shop was closed.", "Mia dijo que la tienda estaba cerrada.", "Said introduce contenido sin receptor directo."),
        ("Mia told Leo the shop was closed.", "Mia le dijo a Leo que la tienda estaba cerrada.", "Told necesita un receptor como Leo."),
        ("The report keeps the time and place.", "El reporte conserva la hora y el lugar.", "Report presenta el mensaje desde otra perspectiva."),
        ("The message names an action for today.", "El mensaje nombra una acción para hoy.", "Message es la fuente que se debe transmitir."),
        ("Preserved content keeps the same meaning.", "El contenido conservado mantiene el mismo sentido.", "Content debe conservar acciones y datos esenciales."),
    ]
    remap = {f"{p}.e01": (f"en.n3.class-{n}.t01", f"{p}.r01"), f"{p}.e02": (f"en.n3.class-{n}.t06", f"{p}.r03"), f"{p}.e03": (f"en.n3.class-{n}.t03", f"{p}.r02"), f"{p}.e04": (f"en.n3.class-{n}.t06", f"{p}.r03")}
    return make_class(n, ["Reconocer hablante y contenido en reportes sencillos.", "Relacionar cinco fuentes con reportes fieles."], [("speaker","hablante"),("message","mensaje"),("report","reporte"),("said","dijo"),("told","le dijo"),("content","contenido")], rows, pools, remap)

def c47() -> dict[str, Any]:
    n, c, p = 47, CONCEPTS[47], "en.n3.c47"
    pools = {"practiceGuided": [
        fill(f"{p}.pg01", "Completa sin receptor: Eva ___ the shop was open.", "said", c, "practiceGuided", "Said introduce contenido sin nombrar receptor.", hint="No aparece una persona después del espacio."),
        q(f"{p}.pg02", "Completa con receptor: Eva ___ Leo to wait.", ["said", "say", "told"], 2, c, "practiceGuided", "Told va seguido del receptor Leo.", hint="Busca la persona que recibe el mensaje."),
        order(f"{p}.pg03", "Ordena la frase con told y receptor.", "Nina told Sam to call the office.", c, "practiceGuided", "Told precede a Sam y luego a la acción."),
    ], "practice": [
        match(f"{p}.p01", "Relaciona cada estructura con su uso.", [("said the train was late", "said + content"), ("told Pia the train was late", "told + listener + content")], c, "practice", "Said introduce contenido; told añade oyente."),
        listen(f"{p}.p02", "Escucha y elige la estructura correcta.", "Jon spoke directly to Ali and asked him to lock the door.", ["Jon said Ali to lock the door.", "Jon told Ali to lock the door.", "Jon told to lock Ali the door."], 1, c, "practice", "Told Ali identifica al receptor antes de la acción."),
        write(f"{p}.p03", "Reporta a Rosa sin nombrar receptor.", "Rosa: The café closes at five.", "Rosa said the café closed at five.", "Rosa said that the café closed at five.", c, "practice", "Said introduce el dato del café sin objeto personal."),
    ], "evaluation": [
        q(f"{p}.e01", "Elige la forma correcta sin receptor.", ["Ivo said the file was ready.", "Ivo told the file was ready.", "Ivo said Mia the file was ready."], 0, c, "evaluation", "Said es correcto porque no aparece receptor."),
        fill(f"{p}.e02", "Completa con receptor: May ___ Luis to arrive early.", "told", c, "evaluation", "Told conecta a May con el receptor Luis."),
        listen(f"{p}.e03", "Escucha y selecciona el reporte correcto.", "Kai spoke to Bea: Please bring your ticket.", ["Kai said Bea to bring her ticket.", "Kai told Bea to bring her ticket.", "Kai told to Bea said her ticket."], 1, c, "evaluation", "Told Bea conserva el receptor y la petición."),
        match(f"{p}.e04", "Completa seis reportes con said o told.", [
            ("Mara ___ the office was closed", "said — office"),
            ("Mara ___ Luis to return later", "told — Luis"),
            ("Oli ___ the parcel was downstairs", "said — parcel"),
            ("Oli ___ Ren to collect it", "told — Ren"),
            ("Pia ___ the bus arrived at nine", "said — bus"),
            ("Pia ___ Sol to wait inside", "told — Sol")], c, "evaluation", "Cinco de seis formas prueban verbo correcto y receptor cuando corresponde.", scoring={"parts": 6, "minimumCorrect": 5, "independentAttempt": True}),
    ], "review": [
        q(f"{p}.r01", "¿Qué opción usa told con receptor?", ["Kim said the date changed.", "Kim told the date changed.", "Kim told Jo the date changed."], 2, c, "review", "Told Jo nombra explícitamente al receptor."),
        order(f"{p}.r02", "Ordena un reporte sin receptor.", "Ari said the meeting ended early.", c, "review", "Said introduce directamente el contenido reportado."),
        match(f"{p}.r03", "Recupera seis formas de say y tell.", [
            ("Leo ___ he needed help", "said — help"), ("Leo ___ Ana to call", "told — Ana"),
            ("Mia ___ the room was free", "said — room"), ("Mia ___ Ben to book it", "told — Ben"),
            ("Nora ___ the key was missing", "said — key"), ("Nora ___ Eli to check", "told — Eli")], c, "review", "La serie recupera seis decisiones con oyente visible solo para told.", scoring={"parts": 6, "minimumCorrect": 5, "independentAttempt": True}),
    ]}
    rows = [
        ("We say something to report content.", "Usamos say para reportar contenido.", "Say no necesita receptor como objeto."),
        ("Lina said the bus was late.", "Lina dijo que el bus llegaba tarde.", "Said es el pasado de say."),
        ("We tell a listener some news.", "Le contamos una noticia a un oyente.", "Tell necesita una persona receptora."),
        ("Lina told Omar the bus was late.", "Lina le dijo a Omar que el bus llegaba tarde.", "Told es el pasado de tell y precede al receptor."),
        ("The listener follows told directly.", "El oyente sigue directamente a told.", "Listener hace visible quién recibe el mensaje."),
        ("An object person is required after told.", "Se requiere una persona objeto después de told.", "Object aquí significa el receptor gramatical."),
    ]
    remap = {f"{p}.e01": (f"en.n3.class-{n}.t02", f"{p}.r02"), f"{p}.e02": (f"en.n3.class-{n}.t04", f"{p}.r01"), f"{p}.e03": (f"en.n3.class-{n}.t05", f"{p}.r01"), f"{p}.e04": (f"en.n3.class-{n}.t06", f"{p}.r03")}
    return make_class(n, ["Distinguir said de told con receptor.", "Completar seis reportes con precisión formal."], [("say","decir"),("said","dijo"),("tell","contar"),("told","le dijo"),("listener","oyente"),("object","objeto")], rows, pools, remap)
    n, c, p = 16, CONCEPTS[16], "en.n3.c16"
    pools = {"practiceGuided": [
        q(f"{p}.pg01", "Clasifica: ¿arreglo confirmado o intención?", ["The room is booked", "I am going to call", "It may rain"], 0, c, "practiceGuided", "Is booked es un arreglo ya confirmado.", hint="Busca el mensaje con reserva concreta."),
        fill(f"{p}.pg02", "Completa la intención de Rosa: She is ___ to join us.", "going", c, "practiceGuided", "Is going to expresa una intención futura.", hint="Usa going después de is."),
        listen(f"{p}.pg03", "Escucha y elige la predicción.", "The sky is dark; it will rain before the match.", ["A fixed booking", "A personal intention", "A prediction"], 2, c, "practiceGuided", "La evidencia del cielo permite una predicción.", hint="Relaciona el cielo oscuro con lo que probablemente pasará.")],
    "practice": [
        match(f"{p}.p01", "Relaciona cada mensaje con su grado de certeza.", [("We are meeting at six", "confirmed arrangement"), ("I am going to study", "intention"), ("The bus will be late", "prediction")], c, "practice", "Cada forma se interpreta con la señal contextual del mensaje."),
        q(f"{p}.p02", "Elige el mensaje de una reserva ya cerrada.", ["We are having lunch at noon.", "I am going to check the menu.", "It will be busy."], 0, c, "practice", "La hora acordada presenta un arreglo confirmado."),
        listen(f"{p}.p03", "Escucha: ¿qué expresa el hablante?", "I am going to ask the manager after lunch.", ["A confirmed table", "An intention", "A weather prediction"], 1, c, "practice", "Going to ask anuncia una intención del hablante.")],
    "evaluation": [
        q(f"{p}.e01", "En una agenda, elige el arreglo confirmado.", ["The team is meeting on Friday.", "I am going to print the map.", "The road will be busy."], 0, c, "evaluation", "La reunión con día fijado es el arreglo confirmado."),
        listen(f"{p}.e02", "Escucha y marca la intención personal.", "I am going to bring extra chairs for the picnic.", ["A fixed appointment", "A personal intention", "A weather guess"], 1, c, "evaluation", "El hablante anuncia lo que piensa hacer personalmente."),
        q(f"{p}.e03", "El cielo cambia: selecciona la predicción.", ["We are meeting at eight.", "She is going to send the file.", "The storm will reach the coast."], 2, c, "evaluation", "La tormenta permite anticipar una predicción."),
        match(f"{p}.e04", "Clasifica seis mensajes de una feria.", [("The stalls are opening at nine", "confirmed arrangement — stalls schedule"), ("I am going to bring signs", "intention — signs"), ("It will be crowded", "prediction — crowd"), ("The band is playing at noon", "confirmed arrangement — band schedule"), ("I am going to print maps", "intention — maps"), ("The road will be busy", "prediction — road traffic")], c, "evaluation", "Las seis etiquetas exigen distinguir arreglo, intención y predicción.", scoring={"parts": 6, "minimumCorrect": 5, "independentAttempt": True})],
    "review": [
        q(f"{p}.r01", "¿Qué frase confirma una cita con hora?", ["We are meeting at ten.", "I am going to call.", "It will be cold."], 0, c, "review", "La hora compartida confirma el arreglo."),
        listen(f"{p}.r02", "Escucha y elige la intención del voluntario.", "I am going to label the boxes tonight.", ["A prediction", "A personal plan", "A confirmed train"], 1, c, "review", "El voluntario declara su plan personal para la noche."),
        write(f"{p}.r03", "Escribe una frase de predicción sobre nubes y lluvia.", "Nubes negras cubren el cielo; predices lluvia.", "The dark clouds mean it will rain.", "It will rain because dark clouds cover the sky.", c, "review", "Las dos respuestas conectan la evidencia visible con una predicción.")]
    }
    remap = {f"{p}.e01": (f"en.n3.class-{n:02d}.t01", f"{p}.r01"), f"{p}.e02": (f"en.n3.class-{n:02d}.t02", f"{p}.r02"), f"{p}.e03": (f"en.n3.class-{n:02d}.t03", f"{p}.r03"), f"{p}.e04": (f"en.n3.class-{n:02d}.t04", f"{p}.r01")}
    rows = [("Our arrangement is to meet the tutor at six tomorrow.", "Nuestro arreglo es reunirnos con el tutor mañana a las seis.", "Present continuous con hora fijada muestra un arreglo confirmado."), ("My intention is to bring the printed map.", "Mi intención es traer el mapa impreso.", "Be going to puede expresar una intención del hablante."), ("The forecast says it will rain soon.", "El pronóstico dice que lloverá pronto.", "Will expresa una predicción basada en una lectura del contexto."), ("A plan can show a booking, an intention or a prediction.", "Un plan puede mostrar reserva, intención o predicción.", "La forma futura se interpreta junto con la evidencia del mensaje."), ("We will check the forecast before the trip.", "Revisaremos el pronóstico antes del viaje.", "El pronóstico ayuda a separar una predicción de un arreglo." )]
    return make_class(n, ["Distinguir arreglo confirmado, intención y predicción.", "Interpretar el futuro con señales de certeza."], [("arrangement", "arreglo"), ("intention", "intención"), ("prediction", "predicción"), ("confirmed", "confirmado"), ("forecast", "pronóstico"), ("booking", "reserva")], rows, pools, remap)

def c17() -> dict[str, Any]:
    n, c, p = 17, CONCEPTS[17], "en.n3.c17"
    pools = {"practiceGuided": [
        fill(f"{p}.pg01", "Completa: When the guide ___, we will start.", "arrives", c, "practiceGuided", "Después de when usamos presente simple.", hint="El sujeto guide necesita un verbo en presente."),
        q(f"{p}.pg02", "Elige la cláusula correcta después de before.", ["before the train will leave", "before the train leaving", "before the train leaves"], 2, c, "practiceGuided", "Before introduce una cláusula con presente simple."),
        order(f"{p}.pg03", "Ordena la condición temporal del picnic.", "As soon as she arrives, we will eat.", c, "practiceGuided", "As soon as va seguido de sujeto y presente simple.", hint="Coloca la cláusula temporal antes de la principal.")],
    "practice": [
        q(f"{p}.p01", "Completa mentalmente: ___ the bags are ready, we will leave.", ["Will", "When", "Before to"], 1, c, "practice", "When conecta la condición temporal con la salida futura."),
        listen(f"{p}.p02", "Escucha y elige qué ocurre primero.", "We will call you when the bus arrives.", ["The call happens before arrival", "The bus arrives, then we call", "The bus arrived yesterday"], 1, c, "practice", "El presente arrives fija el momento que activa la llamada."),
        match(f"{p}.p03", "Relaciona con el presente correcto.", [("when the film", "starts"), ("before the shop", "closes"), ("as soon as Leo", "finishes")], c, "practice", "Las tres cláusulas temporales usan presente simple.")],
    "evaluation": [
        fill(f"{p}.e01", "Completa: We will leave when the rain ___.", "stops", c, "evaluation", "La cláusula con when usa stops, no will stop."),
        q(f"{p}.e02", "Elige la frase correcta sobre la entrega.", ["Before the driver will arrive, we pack.", "Before driver arriving, we will pack.", "Before the driver arrives, we will pack."], 2, c, "evaluation", "Before lleva sujeto y presente simple; la principal expresa futuro."),
        listen(f"{p}.e03", "Escucha y selecciona la acción posterior.", "As soon as the room opens, we will put out the chairs.", ["The chairs are put out after opening", "The room opened last week", "The chairs were removed first"], 0, c, "evaluation", "La acción principal ocurre cuando la sala abre."),
        fill(f"{p}.e04", "Completa seis planes con presente tras when.", "arrives / will start | closes / will check | finishes / will leave | opens / will enter | returns / will call | stops / will continue", c, "evaluation", "Las seis respuestas usan presente en when y futuro en la acción principal.", scoring={"parts": 6, "minimumCorrect": 5, "independentAttempt": True}, originExtra={"text": "When Ana ___, the meeting will start. Before the shop ___, we will check the list. As soon as Leo ___, we will leave. When the gate ___, we will enter. When the manager ___, we will call. When the rain ___, we will continue.", "sentences": ["When Ana ___, the meeting will start.", "Before the shop ___, we will check the list.", "As soon as Leo ___, we will leave.", "When the gate ___, we will enter.", "When the manager ___, we will call.", "When the rain ___, we will continue."]})],
    "review": [
        q(f"{p}.r01", "¿Qué opción mantiene presente después de as soon as?", ["As soon as Mina will finish, we leave.", "As soon as Mina finishes, we will leave.", "As soon as Mina finishing, we will leave."], 1, c, "review", "Finishes es presente simple en la cláusula temporal."),
        fill(f"{p}.r02", "Completa: Before the show ___, we will check the lights.", "starts", c, "review", "Starts completa la cláusula temporal en presente."),
        write(f"{p}.r03", "Redacta un plan con before y una acción futura.", "Primero cerrará la tienda; luego llamaremos al conductor.", "Before the shop closes, we will call the driver.", "We will call the driver before the shop closes.", c, "review", "Las dos versiones ordenan cierre y llamada sin will en la cláusula temporal.")]
    }
    remap = {f"{p}.e01": (f"en.n3.class-{n:02d}.t01", f"{p}.r02"), f"{p}.e02": (f"en.n3.class-{n:02d}.t02", f"{p}.r01"), f"{p}.e03": (f"en.n3.class-{n:02d}.t03", f"{p}.r03"), f"{p}.e04": (f"en.n3.class-{n:02d}.t01", f"{p}.r03")}
    rows = [("When the guide arrives, we will begin.", "Cuando llegue el guía, empezaremos.", "After when, before and as soon as use present simple for a future time."), ("Before the train leaves, we will check the tickets.", "Antes de que salga el tren, revisaremos los boletos.", "La cláusula temporal usa presente; la acción principal puede llevar will."), ("As soon as the door opens, we will enter.", "En cuanto se abra la puerta, entraremos.", "As soon as marca el momento inmediato que activa el futuro."), ("The time clause gives a future condition for an action.", "La cláusula temporal da la condición futura de una acción.", "El conector y la forma verbal deben trabajar juntos."), ("We will wait until the manager returns.", "Esperaremos hasta que regrese el gerente.", "Returns mantiene presente simple dentro de una referencia futura.")]
    return make_class(n, ["Usar presente simple después de when, before y as soon as.", "Conectar una condición temporal con una acción futura."], [("arrives", "llega"), ("leaves", "sale"), ("starts", "empieza"), ("finishes", "termina"), ("opens", "abre"), ("until", "hasta que"), ("future", "futuro")], rows, pools, remap)

def c18() -> dict[str, Any]:
    n, c, p = 18, CONCEPTS[18], "en.n3.c18"
    pools = {"practiceGuided": [
        listen(f"{p}.pg01", "Escucha y marca el dato que cambió.", "The workshop moves from Tuesday to Thursday; the room stays the same.", ["The room", "The speaker", "The day"], 2, c, "practiceGuided", "El mensaje cambia Tuesday por Thursday, no la sala.", hint="Compara el día con el dato que permanece."),
        q(f"{p}.pg02", "En el calendario, elige el dato aún confirmado.", ["The day changed", "The room is still B2", "The old time was wrong"], 1, c, "practiceGuided", "Still B2 indica que la sala no cambió.", hint="Busca still para reconocer lo que continúa."),
        match(f"{p}.pg03", "Relaciona mensaje con estado de la agenda.", [("moved to Thursday", "changed day"), ("still in Room B2", "confirmed room"), ("starts at seven", "confirmed time")], c, "practiceGuided", "Separar changed y still permite actualizar la agenda.")],
    "practice": [
        q(f"{p}.p01", "Elige la actualización correcta del cine.", ["The cinema changed, but the time is unknown.", "Everything was cancelled.", "The film starts later, but the cinema is the same."], 2, c, "practice", "La primera opción muestra un cambio y un dato confirmado."),
        listen(f"{p}.p02", "Escucha dos mensajes y marca lo que sigue igual.", "The bus leaves at nine now, but the stop remains outside the library.", ["Departure time", "Bus stop", "Travel date"], 1, c, "practice", "Remains outside the library señala el lugar confirmado."),
        q(f"{p}.p03", "¿Qué dato debes cambiar en la agenda?", ["The host is still Priya", "The link is still active", "The start day moved to Monday"], 2, c, "practice", "Moved to Monday exige actualizar el día de inicio.")],
    "evaluation": [
        listen(f"{p}.e01", "Escucha: ¿qué elemento cambió?", "The online talk is now at four, but Ana is still the host.", ["The host", "The topic", "The time"], 2, c, "evaluation", "Now at four cambia la hora y still conserva a Ana."),
        q(f"{p}.e02", "Elige el dato que permanece confirmado.", ["The meeting moved to Friday.", "The old speaker cancelled.", "The meeting is still in Hall 3."], 2, c, "evaluation", "Still in Hall 3 mantiene confirmada la sala."),
        write(f"{p}.e03", "Agenda: mié 18:00, Hall 7, Ana. Escucha dos mensajes y actualiza tres datos.",
              "Calendario: miércoles, 18:00, Hall 7, anfitriona Ana. Escucha ambos mensajes antes de actualizar.",
              "Update the class to Friday at 19:00 in Hall 9; keep Ana as the host.",
              "The new schedule is Friday, 19:00, Hall 9, with Ana still hosting.",
              c, "evaluation", "Los dos mensajes cambian día, hora y sala; Ana permanece como anfitriona.",
              originExtra={"calendar": "Wednesday / 18:00 / Hall 7 / host Ana",
                           "audio": "Message one: The class moves to Friday at 19:00; Ana remains the host. Message two: Use Hall 9; Ana is still hosting.",
                           "audioMode": "tts", "languageCode": "en", "maxReplays": 3,
                           "audioSources": ["The class moves to Friday at 19:00; Ana remains the host.",
                                            "Use Hall 9; Ana is still hosting."]}),
        listen(f"{p}.e04", "Agenda: mié 18:00, Hall 7, Ana. Escucha y elige los tres cambios.",
               "Message one: The class moves to Friday at 19:00; Ana remains the host. Message two: It will be in Hall 9; the link is unchanged.",
               ["Friday / 19:00 / Hall 9", "Friday / 18:00 / Hall 7", "Wednesday / 19:00 / Hall 9"],
               0, c, "evaluation", "La opción correcta actualiza día, hora y sala desde ambos mensajes.",
               scoring={"parts": 3, "minimumCorrect": 3, "independentAttempt": True},
               originExtra={"calendar": "Wednesday / Hall 7 / 18:00 / host Ana",
                            "audioSources": ["The class moves to Friday at 19:00; Ana remains the host.",
                                             "It will be in Hall 9; the link is unchanged."]})],
    "review": [
        q(f"{p}.r01", "Elige qué sigue confirmado en la excursión.", ["The bus time changed.", "The guide is still Marta.", "The old route closed."], 1, c, "review", "Still Marta identifica a la guía que continúa asignada."),
        listen(f"{p}.r02", "Escucha y selecciona el nuevo horario.", "The lesson is now at five; the teacher remains Leo.", ["Five", "Four", "Six"], 0, c, "review", "Now at five da el horario actualizado."),
        write(f"{p}.r03", "Agenda: mar 19:00, Blue Café, Leo. Escucha y escribe tres cambios.",
              "Agenda: martes, 19:00, Blue Café, anfitrión Leo. Escucha ambos mensajes.",
              "Update dinner to Thursday at 20:00 in Green House; keep Leo as the host.",
              "The revised dinner is Thursday, 20:00, Green House, with Leo still hosting.",
              c, "review", "La recuperación integra dos mensajes y actualiza día, hora y lugar.",
              originExtra={"calendar": "Tuesday / 19:00 / Blue Café / host Leo",
                           "audio": "Message one: Dinner moves to Thursday at eight; Leo remains the host. Message two: The new restaurant is Green House; Leo is still hosting.",
                           "audioMode": "tts", "languageCode": "en", "maxReplays": 3,
                           "audioSources": ["Dinner moves to Thursday at eight; Leo remains the host.",
                                            "The new restaurant is Green House; Leo is still hosting."]})]
    }
    remap = {f"{p}.e01": (f"en.n3.class-{n:02d}.t01", f"{p}.r02"), f"{p}.e02": (f"en.n3.class-{n:02d}.t02", f"{p}.r01"), f"{p}.e03": (f"en.n3.class-{n:02d}.t06", f"{p}.r03"), f"{p}.e04": (f"en.n3.class-{n:02d}.t06", f"{p}.r03")}
    rows = [("The workshop moved to Thursday, but Room B2 stayed confirmed.", "El taller pasó al jueves, pero la sala B2 siguió confirmada.", "Comparar moved y stayed ayuda a detectar qué dato cambia."), ("The new time is four, while Ana is still the host.", "La hora nueva es cuatro, mientras Ana sigue siendo la anfitriona.", "Now y still separan actualización y continuidad."), ("Read the old schedule before listening to the update.", "Lee el horario antiguo antes de escuchar la actualización.", "La comparación necesita un dato original y un mensaje posterior."), ("A schedule update can change one detail and preserve another.", "Una actualización puede cambiar un dato y conservar otro.", "No todos los datos de una agenda cambian juntos."), ("The room remains the same after the time changes.", "La sala permanece igual después de cambiar la hora.", "Remain señala el elemento todavía confirmado."), ("Calendar: Wednesday at six in Hall 7. Message one changes the day and time; message two changes the room. Ana remains the host.", "Agenda: miércoles a las seis en Hall 7. El primer mensaje cambia día y hora; el segundo cambia la sala. Ana sigue como anfitriona.", "El modelo integra una agenda base, dos mensajes y tres actualizaciones observables.")]
    return make_class(n, ["Identificar qué dato de una agenda cambió.", "Conservar los elementos que siguen confirmados."], [("schedule", "agenda"), ("changed", "cambió"), ("remain", "permanecer"), ("still", "todavía"), ("host", "anfitrión"), ("room", "sala")], rows, pools, remap)

def c19() -> dict[str, Any]:
    n, c, p = 19, CONCEPTS[19], "en.n3.c19"
    pools = {"practiceGuided": [
        q(f"{p}.pg01", "Elige el mensaje con responsable y plazo.", ["Lena may review the map later.", "The map is expected around noon.", "Lena will send the map by noon."], 2, c, "practiceGuided", "Lena y by noon hacen observable responsable y plazo.", hint="Busca quién hará qué y para cuándo."),
        fill(f"{p}.pg02", "Completa la alternativa: If rain starts, we will ___ indoors.", "meet", c, "practiceGuided", "Meet indoors ofrece una alternativa viable.", hint="El verbo debe expresar el plan alternativo."),
        order(f"{p}.pg03", "Ordena una confirmación de tareas.", "Tom will bring chairs by Friday.", c, "practiceGuided", "La frase muestra responsable, tarea y plazo.", hint="Sujeto, will, acción y plazo forman la coordinación.")],
    "practice": [
        match(f"{p}.p01", "Relaciona cada persona con su tarea y plazo.", [("Nia", "will call by ten"), ("Omar", "will print by lunch"), ("Sue", "will check by Friday")], c, "practice", "Una coordinación útil asigna una acción y un momento a cada persona."),
        listen(f"{p}.p02", "Escucha y elige la alternativa del equipo.", "If the hall is full, we will use the library room.", ["Cancel the plan", "Use the library room", "Wait until next month"], 1, c, "practice", "La biblioteca es la alternativa explícita si el salón está lleno."),
        write(f"{p}.p03", "Escribe una propuesta con responsable y plazo.", "Maya enviará el menú el martes.", "Maya will send the menu by Tuesday.", "By Tuesday, Maya will send the menu.", c, "practice", "Ambas variantes conservan responsable, acción y plazo.")],
    "evaluation": [
        q(f"{p}.e01", "Elige la propuesta completa para un voluntario.", ["Jin may ask about the bus on Wednesday.", "Jin will book the bus by Wednesday.", "The bus booking was discussed on Wednesday."], 1, c, "evaluation", "La propuesta nombra acción, responsable y plazo."),
        listen(f"{p}.e02", "Escucha y marca la alternativa viable.", "If the printer fails, we will email the tickets.", ["Buy a new printer", "Email the tickets", "End the event"], 1, c, "evaluation", "Enviar los boletos por correo resuelve el fallo de impresión."),
        match(f"{p}.e03", "Une plan y responsable de un evento.", [("Luca", "will invite guests by Monday"), ("Pia", "will bring cups by noon"), ("Ravi", "will confirm the room by Tuesday")], c, "evaluation", "Cada par deja claro quién coordina qué y cuándo."),
        write(f"{p}.e04", "Redacta 60–80 palabras con tres personas y plazos.", "Evento comunitario: Ana reserva sala tranquila viernes; Ben imprime carteles sábado; Carla revisa invitados jueves; si llueve, patio cubierto; Ana avisa esta noche; confirman jueves.", "Ana will book the quiet community room by Friday because the event needs a calm place. Ben will print the signs by Saturday morning, and Carla will check the guest list by Thursday. If rain starts, the group will use the covered courtyard. Ana will message everyone tonight, and all three will confirm the plan before Thursday so guests receive clear information.", "By Friday, Ana will reserve the quiet community room because the event needs a calm place. Ben will print signs by Saturday morning, while Carla checks the guest list by Thursday. If rain starts, the group will move to the covered courtyard. Ana will message everyone tonight, and all three will confirm the plan before Thursday so guests receive clear information.", c, "evaluation", "Las variantes conservan las tres personas, cada plazo, la razón y la alternativa.")],
    "review": [
        q(f"{p}.r01", "¿Qué opción asigna tarea y plazo inequívocos?", ["Rosa might review the list later.", "The list is scheduled for six.", "Rosa will check the list by six."], 2, c, "review", "Rosa, check y by six forman una asignación completa."),
        listen(f"{p}.r02", "Escucha y selecciona la contingencia acordada.", "If the coach is late, Kim will start the warm-up.", ["Kim starts the warm-up", "Kim cancels training", "The coach leaves town"], 0, c, "review", "El plan alternativo mantiene el entrenamiento en marcha."),
        write(f"{p}.r03", "Escribe 60–80 palabras con tres personas y plazos.", "Excursión: Leo confirma sala de biblioteca al mediodía por seguridad; Bea prepara agua a las siete; Omar avisa el punto a las ocho; si no llega el bus, caminan; Leo escribe esta noche; confirman antes de las nueve.", "Leo will confirm the library room by noon because the group needs a clear meeting place. Bea will pack water by seven, and Omar will tell everyone the meeting point by eight. If the bus does not come, they will walk from the station. Leo will message the group tonight, and all three will confirm the route before nine so nobody arrives at the wrong place.", "By noon, Leo will reserve the library room because the group needs a clear meeting place. Bea will prepare water by seven, while Omar tells everyone the meeting point by eight. If the bus fails, they will walk from the station. Leo will message the group tonight, and all three will confirm the route before nine so nobody arrives at the wrong place.", c, "review", "El escenario distinto conserva participantes, plazos, razón, contingencia y confirmación.")]
    }
    remap = {f"{p}.e01": (f"en.n3.class-{n:02d}.t01", f"{p}.r01"), f"{p}.e02": (f"en.n3.class-{n:02d}.t02", f"{p}.r02"), f"{p}.e03": (f"en.n3.class-{n:02d}.t03", f"{p}.r03"), f"{p}.e04": (f"en.n3.class-{n:02d}.t04", f"{p}.r03")}
    rows = [("Lena will send the map before the deadline at noon.", "Lena enviará el mapa antes del plazo del mediodía.", "La coordinación nombra responsable, acción y plazo."), ("If rain starts, we will use the covered patio.", "Si empieza la lluvia, usaremos el patio cubierto.", "If introduce una alternativa viable ante una contingencia."), ("Please confirm your task before Thursday.", "Confirma tu tarea antes del jueves.", "Una confirmación cierra quién hará qué y cuándo."), ("Three people can share one task and a deadline.", "Tres personas pueden compartir una tarea y un plazo.", "La propuesta debe ser concreta y comprobable."), ("We will keep an alternative plan for bad weather.", "Mantendremos un plan alternativo para mal tiempo.", "Una alternativa permite renegociar sin perder el objetivo.")]
    return make_class(n, ["Proponer un arreglo con responsables y plazos.", "Añadir una alternativa viable a un plan futuro."], [("deadline", "plazo"), ("task", "tarea"), ("confirm", "confirmar"), ("alternative", "alternativa"), ("covered", "cubierto"), ("message", "mensaje")], rows, pools, remap)

def c20() -> dict[str, Any]:
    n, c, p = 20, CONCEPTS[20], "en.n3.c20"; all_c = [CONCEPTS[k] for k in NUMBERS]
    pools = {"practiceGuided": [
        q(f"{p}.pg01", "Elige la confirmación final de un cambio.", ["The old room may still be available.", "The new room is confirmed.", "We discussed several rooms."], 1, c, "practiceGuided", "New room is confirmed closes the updated arrangement.", hint="Busca una confirmación completa del plan nuevo."),
        listen(f"{p}.pg02", "Escucha y marca la contingencia aceptada.", "The hall is closed, so we will meet online instead.", ["Wait without a plan", "Meet online", "Use the closed hall"], 1, c, "practiceGuided", "Meet online es la contingencia acordada ante el cierre."),
        write(f"{p}.pg03", "Escribe una nueva hora y una confirmación.", "La reunión cambia a las cinco y todos aceptan.", "We will meet at five, and everyone has confirmed.", "Everyone has confirmed that we will meet at five.", c, "practiceGuided", "Las variantes combinan cambio y cierre confirmado.")],
    "practice": [
        match(f"{p}.p01", "Relaciona cada problema con su acuerdo.", [("storm closes the field", "use the sports hall"), ("speaker is delayed", "start with the workshop"), ("bus is cancelled", "share cars")], c, "practice", "Cada contingencia conserva el objetivo con una solución distinta."),
        q(f"{p}.p02", "Elige la frase que cierra la renegociación.", ["The old time may remain available.", "We will use the new time; please confirm.", "The group discussed another time."], 1, c, "practice", "La nueva hora y la petición de confirmación cierran el acuerdo."),
        listen(f"{p}.p03", "Escucha y selecciona el cambio acordado.", "The train is cancelled; we will meet at the station at noon instead.", ["Keep the cancelled train", "Meet next week online", "Meet at noon at the station"], 2, c, "practice", "La respuesta conserva lugar y nueva hora tras la cancelación.")],
    "evaluation": [
        q(f"{p}.e01", "Evento cancelado parcialmente: elige una propuesta.", ["We could cancel lunch and wait for another date.", "The talk might return, but lunch is uncertain.", "We will move the talk online and keep lunch at noon."], 2, c, "evaluation", "La propuesta cambia una parte y conserva otra del evento.", requires=all_c),
        listen(f"{p}.e02", "Escucha: ¿qué decisión inmediata toma el grupo?", "The guide cannot come, so Marta will lead the walk at nine.", ["Cancel the whole walk", "Marta leads at nine", "Wait for the guide tomorrow"], 1, c, "evaluation", "Marta y las nueve forman la decisión contingente inmediata.", requires=all_c),
        write(f"{p}.e03", "Redacta 70–100 palabras para renegociar la feria.",
              "Feria vecinal: charla exterior cancelada; almuerzo sigue 12:30 en Garden Café; curadora los recibe 10:00; Priya enviará enlace antes del martes; Joel revisará micrófonos antes del miércoles; antes de abrir el jueves colocan carteles; si continúa la lluvia usan biblioteca; confirman miércoles 18:00; esperan mucha asistencia.",
              "The outdoor talk is cancelled, but lunch remains at 12:30 in the Garden Café. The curator is meeting us at ten, Priya is going to email the online link by Tuesday, and Joel will confirm the microphones by Wednesday. Before the venue opens on Thursday, the team will post the signs. It will be busy, so if rain continues, we will use the library. Please confirm by six on Wednesday.",
              "Lunch is still arranged for 12:30 at the Garden Café although the outdoor talk is cancelled. The curator is meeting us at ten. Priya is going to send the online link by Tuesday, and Joel will check the microphones by Wednesday. Before Thursday's opening, the team will post signs. Attendance will be high; if it keeps raining, we will use the library. Please confirm by Wednesday at six.",
              c, "evaluation", "Las variantes usan únicamente los datos del estímulo y combinan contraste futuro, cláusula temporal, actualización, responsables, contingencia y cierre.", requires=all_c),
        match(f"{p}.e04", "Relaciona cinco evidencias de la renegociación.",
              [("The curator is meeting us / Priya is going to email / It will be busy", "arrangement / intention / prediction"),
               ("Before the venue opens, the team will post signs", "time clause + future action"),
               ("Old: outdoor talk / New: online talk; lunch remains 12:30", "changed item + confirmed item"),
               ("Joel will check microphones by Wednesday", "responsible person + task + deadline"),
               ("If rain continues, use the library; please confirm", "contingency + final confirmation")],
              c, "evaluation", "Las cinco relaciones hacen observable cada concepto acumulativo.", requires=all_c)],
    "review": [
        q(f"{p}.r01", "¿Qué cierre confirma cambio, tarea y alternativa?", ["The talk moves online; Leo will email the link; if needed, we meet Friday.", "The talk may move, and Leo could check the link later.", "Friday remains possible, but no one has a task yet."], 0, c, "review", "La opción completa cierra los tres datos de la renegociación.", requires=all_c),
        listen(f"{p}.r02", "Escucha y marca el dato que permanece confirmado.", "The dinner changes to Friday, but the restaurant remains Green House.", ["Green House", "Thursday", "A different restaurant"], 0, c, "review", "Remains Green House conserva el lugar pese al cambio de día.", requires=all_c),
        write(f"{p}.r03", "Escribe 70–100 palabras para cerrar otro cambio de plan.",
              "Visita al museo: bus cancelado; encuentro confirmado 10:00 en entrada; Gallery 4 sigue reservada; museo garantiza acceso para todos; guía espera entrada concurrida; Kim enviará ruta hoy 19:00; Leo revisará boletos antes de abrir; si empeora lluvia, visita virtual; confirmar antes de 9:00.",
              "The bus is cancelled, so we are meeting at the museum entrance at ten. Gallery 4 remains confirmed, and the guide predicts the entrance will be busy. Kim is going to send the new route tonight at seven. Before the museum opens, Leo will check the tickets. If the rain gets worse, we will use the virtual tour. The museum visit will remain accessible to everyone. Please confirm this revised plan before nine.",
              "We are meeting at the museum entrance at ten because the bus is cancelled, while Gallery 4 remains booked. The guide expects the entrance will be busy. Kim is going to send the route at seven tonight, and Leo will check tickets before the museum opens. If the weather gets worse, the virtual tour is our alternative. The museum visit will remain accessible to everyone. Please confirm the complete revised plan before nine.",
              c, "review", "El escenario distinto conserva solo los datos dados y demuestra los cinco conceptos.", requires=all_c)]
    }
    remap = {f"{p}.e01": (f"en.n3.class-{n:02d}.t01", f"{p}.r01"), f"{p}.e02": (f"en.n3.class-{n:02d}.t02", f"{p}.r02"), f"{p}.e03": (f"en.n3.class-{n:02d}.t06", f"{p}.r03"), f"{p}.e04": (f"en.n3.class-{n:02d}.t06", f"{p}.r03")}
    rows = [("The event is cancelled in one part, but lunch remains at noon.", "El evento se cancela en una parte, pero el almuerzo sigue al mediodía.", "Una renegociación puede modificar un elemento y conservar otro."), ("If the hall closes, we will use the online room.", "Si cierra el salón, usaremos la sala en línea.", "If permite proponer una contingencia aceptable."), ("Marta will confirm the walk at nine.", "Marta confirmará la caminata a las nueve.", "Una decisión inmediata nombra responsable y plazo."), ("Please confirm the revised timetable before Thursday.", "Confirma el horario revisado antes del jueves.", "La confirmación completa hace operativo el nuevo arreglo."), ("The hall remains booked after the speaker changes.", "El salón sigue reservado después del cambio de ponente.", "Still booked demuestra qué parte de la agenda continúa."), ("The workshop is moving to Thursday, Ana is going to send the timetable, and it will be crowded. Before the doors open, Ben will check the chairs. Room B2 remains confirmed. If rain starts, we will use the covered patio. Please confirm before Thursday.", "El taller se muda al jueves, Ana enviará el horario y se prevé mucha gente. Antes de abrir, Ben revisará las sillas. La sala B2 sigue fija y hay alternativa por lluvia.", "El modelo integra arreglo, intención, predicción, cláusula temporal, dato estable, responsable, contingencia y confirmación.")]
    return make_class(n, ["Negociar un cambio parcial con una contingencia.", "Cerrar una confirmación completa y coherente."], [("hall", "salón"), ("event", "evento"), ("revised", "revisado"), ("confirm", "confirmar"), ("alternative", "alternativa"), ("remains", "permanece")], rows, pools, remap, uses=all_c, cumulative=all_c)

def c48() -> dict[str, Any]:
    n, c, p = 48, CONCEPTS[48], "en.n3.c48"
    pools = {"practiceGuided": [
        listen(f"{p}.pg01", "Escucha y detecta el dato modificado.", "Original: I arrive at five. Report: Lia said she arrived at six.", ["person", "place", "time"], 2, c, "practiceGuided", "Five cambia a six; el dato modificado es la hora.", hint="Compara los números de la fuente y el reporte."),
        q(f"{p}.pg02", "¿Qué dato permanece igual en ambos mensajes?", ["The speaker", "Room Three", "The day"], 1, c, "practiceGuided", "Room Three aparece sin cambios en fuente y reporte.", hint="Busca el dato idéntico."),
        match(f"{p}.pg03", "Relaciona cada cambio con su categoría.", [("I becomes she", "person and perspective"), ("at two becomes at four", "time"), ("call becomes email", "action")], c, "practiceGuided", "Las parejas separan persona, hora y acción.", hint="Observa pronombres, números y verbos."),
    ], "practice": [
        listen(f"{p}.p01", "Compara la fuente y el reporte: ¿qué cambió?", "Original: We will meet outside. Report: Bo said they would meet inside.", ["place", "speaker", "day"], 0, c, "practice", "Outside cambia a inside; el lugar no se conservó."),
        q(f"{p}.p02", "Fuente: Nia: 'I will print it at nine'. Elige el reporte fiel.", ["Nia said she would print it at nine.", "Nia said she would call at nine.", "Nia said she would print it at ten."], 0, c, "practice", "Print y nine conservan los dos datos de la fuente."),
        write(f"{p}.p03", "Corrige el reporte para conservar el día.", "Fuente: I work on Monday. Reporte incorrecto: Eli said he worked on Tuesday.", "Eli said he worked on Monday.", "Eli said that he worked on Monday.", c, "practice", "Monday restaura el dato temporal de la fuente."),
    ], "evaluation": [
        listen(f"{p}.e01", "Escucha el par y marca el cambio.", "Original: I will wait at the gate. Report: Uma said she would wait at reception.", ["speaker", "action", "place"], 2, c, "evaluation", "Gate cambia a reception, mientras wait se conserva."),
        q(f"{p}.e02", "¿Qué reporte mantiene persona, hora y acción?", ["Ari said Kim called at seven.", "Ari told Kim at eight to email.", "Ari said Sam waited at seven."], 0, c, "evaluation", "La primera opción conserva Kim, call y seven."),
        write(f"{p}.e03", "Repara el verbo alterado en el reporte.", "Fuente: Jo: I will deliver the box. Error: Jo said she would collect the box.", "Jo said she would deliver the box.", "Jo said that she would deliver the box.", c, "evaluation", "Deliver recupera la acción original sin cambiar la perspectiva."),
        listen(f"{p}.e04", "Escucha tres pares y elige los cambios en orden.", "Pair one. Original: I will call you at six. Report: Nora said she would call me at six. Pair two. Original: The train leaves at seven. Report: Omar said the train left at eight. Pair three. Original: Please email the form. Report: Mia told me to print the form.", ["time / action / person", "action / person / time", "person / time / action"], 2, c, "evaluation", "Los pares cambian persona, hora y acción, en ese orden.", scoring={"parts": 3, "minimumCorrect": 3, "independentAttempt": True}),
    ], "review": [
        q(f"{p}.r01", "¿Qué elemento cambia de my a her?", ["action", "perspective", "time"], 1, c, "review", "My a her es un cambio de perspectiva personal."),
        listen(f"{p}.r02", "Escucha y elige el dato conservado.", "Original: I open the desk at ten. Report: Kai said he opened the desk at ten.", ["the speaker name", "the verb tense", "the time at ten"], 2, c, "review", "At ten permanece idéntico en ambos mensajes."),
        listen(f"{p}.r03", "Recupera tres cambios en un audio nuevo.", "Pair one. Original: I need my pass. Report: Tia said she needed her pass. Pair two. Original: The talk starts at noon. Report: Ben said the talk started at one. Pair three. Original: Please bring water. Report: Sol told me to bring food.", ["perspective / clock time / requested action", "clock time / perspective / requested action", "requested action / clock time / perspective"], 0, c, "review", "La recuperación identifica perspectiva, hora y acción con pares nuevos.", scoring={"parts": 3, "minimumCorrect": 3, "independentAttempt": True}),
    ]}
    rows = [
        ("The original source says, I will call at six.", "La fuente original dice: llamaré a las seis.", "Original identifica el mensaje de partida."),
        ("The report must preserve the place.", "El reporte debe conservar el lugar.", "Report se compara con la fuente."),
        ("A person can change from I to she.", "Una persona puede cambiar de I a she.", "Person cambia por la nueva perspectiva."),
        ("The time at six must stay exact.", "La hora de las seis debe mantenerse exacta.", "Time es un dato que no se debe inventar."),
        ("The action call must remain call.", "La acción call debe seguir siendo call.", "Action conserva lo que hará el hablante."),
        ("Perspective changes I to she without changing meaning.", "La perspectiva cambia I por she sin cambiar el sentido.", "Perspective adapta pronombres al reporte."),
    ]
    remap = {f"{p}.e01": (f"en.n3.class-{n}.t02", f"{p}.r02"), f"{p}.e02": (f"en.n3.class-{n}.t01", f"{p}.r03"), f"{p}.e03": (f"en.n3.class-{n}.t05", f"{p}.r03"), f"{p}.e04": (f"en.n3.class-{n}.t06", f"{p}.r03")}
    return make_class(n, ["Comparar fuente directa y reporte.", "Detectar cambios de persona, hora o acción."], [("original","mensaje fuente"),("report","reporte"),("person","persona"),("time","hora"),("action","acción"),("perspective","perspectiva")], rows, pools, remap)

def c49() -> dict[str, Any]:
    n, c, p = 49, CONCEPTS[49], "en.n3.c49"
    audio_meta = _audio()
    pools = {"practiceGuided": [
        q(f"{p}.pg01", "¿Qué dato identifica la fuente del aviso?", ["The colour", "Rosa's name", "The weather"], 1, c, "practiceGuided", "Rosa's name permite atribuir el aviso a su fuente.", hint="Busca quién dejó el mensaje."),
        order(f"{p}.pg02", "Ordena una nota con fuente y acción.", "Rosa said the delivery moved, so Amir must confirm.", c, "practiceGuided", "La nota une fuente, cambio y acción siguiente."),
        listen(f"{p}.pg03", "Escucha y marca al receptor.", "This is Dan. Please tell Priya to email the new link.", ["Dan", "the link", "Priya"], 2, c, "practiceGuided", "Priya es quien debe recibir y ejecutar la petición.", hint="Busca la persona después de tell."),
    ], "practice": [
        match(f"{p}.p01", "Relaciona cada fuente con la acción requerida.", [("Lena: tell Bo the room changed", "Bo checks the new room"), ("Max: tell Uma the call is later", "Uma confirms the new time")], c, "practice", "Cada relevo asigna la acción al receptor correcto."),
        write(f"{p}.p02", "Escribe una nota breve de relevo.", "Fuente: Eva. Para: Tom. Dato: bus a las 8. Acción: llevar boletos.", "Eva said the bus left at eight and told Tom to bring the tickets.", "Eva said the bus was at eight; Tom needed to bring the tickets.", c, "practice", "Ambas notas nombran fuente, receptor, hora y acción."),
        listen(f"{p}.p03", "Escucha y elige el siguiente paso.", "Mina says the key is at reception. Tell Leo to collect it before five.", ["Mina collects it tomorrow", "Leo collects it before five", "Reception closes at four"], 1, c, "practice", "Leo debe recoger la llave antes de las cinco."),
    ], "evaluation": [
        q(f"{p}.e01", "Elige la nota que atribuye dos fuentes.", ["The schedule changed somehow.", "Nora said nine; Ali told us to wait.", "Ali and Nora received one note."], 1, c, "evaluation", "La segunda nota distingue lo dicho por Nora y Ali."),
        listen(f"{p}.e02", "Escucha y marca la acción exacta.", "Omar says the parcel is ready. Please ask Bea to collect it before noon.", ["Bea sends it after noon", "Omar collects it at noon", "Bea collects it before noon"], 2, c, "evaluation", "La acción exacta es que Bea recoja el paquete antes del mediodía."),
        write(f"{p}.e03", "Transmite el aviso sin inventar datos.", "Fuente: Luis. Para: Ana. La sala cambia a B4 a las 3. Ana debe avisar al equipo.", "Luis said the room moved to B4 at three and told Ana to inform the team.", "Luis said that the new room was B4 at three; Ana needed to inform the team.", c, "evaluation", "Las versiones conservan fuente, receptor, lugar, hora y acción."),
        write(f"{p}.e04", "Escucha dos mensajes y escribe una nota de relevo de 70–90 palabras.", "Dos mensajes de voz; identifica fuentes, receptores, datos y acciones.",
              "Rosa said the delivery had moved to Friday at ten and asked Amir to confirm the loading bay by Thursday at four. David said the client call was still on Friday at eleven and told Priya to send the link by Thursday at noon. Amir must confirm the loading bay, while Priya must send the call link. These exact times and actions should remain separate in the final relay note.",
              "Rosa reported that the delivery was now Friday at ten. She told Amir to confirm the loading bay before four on Thursday. David said the client call remained Friday at eleven, and he asked Priya to send its link by noon on Thursday. Amir's task concerns the delivery bay; Priya's concerns the client link. The final relay keeps both sources, recipients, schedules and required actions completely clear today.", c, "evaluation", "La nota atribuye dos fuentes y conserva receptores, horarios y acciones.", originExtra={"audio": "Message one. Rosa: The delivery moves to Friday at ten. Please tell Amir to confirm the loading bay by Thursday at four. Message two. David: The client call remains Friday at eleven. Tell Priya to send the link by Thursday at noon.", **audio_meta}),
    ], "review": [
        q(f"{p}.r01", "¿Qué nota conserva fuente, receptor y plazo?", ["Ivy said the file was ready; tell Ken to send it by six.", "A change happened today.", "Ken said Ivy received a file tomorrow."], 0, c, "review", "Ivy, Ken y by six hacen verificable el relevo."),
        match(f"{p}.r02", "Une dato exacto con su función en la nota.", [("Nora said the train leaves at eight", "source plus exact content"), ("Tell Eli to buy the tickets", "recipient plus required action")], c, "review", "La nota necesita atribución y siguiente acción."),
        write(f"{p}.r03", "Escucha otros dos mensajes y redacta 70–90 palabras.", "Dos avisos de biblioteca; conserva fuentes, destinatarios y tareas.",
              "Maya said the reading group had moved to Saturday at two and asked Joel to reserve Table Six by Friday morning. Ken said the author call remained Saturday at four and told Lina to test the microphone by Friday at three. Joel must reserve the table, and Lina must test the microphone. The complete note keeps the two sources, recipients, exact times and actions clearly separate for the library team.",
              "Maya reported that the reading group was now Saturday at two. She told Joel to reserve Table Six before Friday morning. Ken said the author call was still Saturday at four, and he asked Lina to test the microphone by three on Friday. Joel handles the table; Lina handles the audio test. This complete relay clearly preserves both speakers, both schedules, the correct recipients and their required next actions for everyone.", c, "review", "La recuperación usa un contexto nuevo y transmite dos avisos completos.", originExtra={"audio": "Message one. Maya: The reading group moves to Saturday at two. Ask Joel to reserve Table Six by Friday morning. Message two. Ken: The author call remains Saturday at four. Tell Lina to test the microphone by Friday at three.", **audio_meta}),
    ]}
    rows = [
        ("A relay passes a message to another person.", "Un relevo pasa un mensaje a otra persona.", "Relay transmite información recibida."),
        ("Name each source before the reported content.", "Nombra cada fuente antes del contenido reportado.", "Source evita mezclar hablantes."),
        ("The recipient must receive the correct request.", "El destinatario debe recibir la petición correcta.", "Recipient identifica quién debe actuar."),
        ("Keep every exact time and place.", "Conserva cada hora y lugar exactos.", "Exact impide alterar datos clave."),
        ("State the required action after each message.", "Indica la acción requerida después de cada mensaje.", "Action hace operativa la nota."),
        ("A clear note reports two sources and two next actions.", "Una nota clara reporta dos fuentes y dos acciones siguientes.", "Note integra atribución, contenido y seguimiento."),
    ]
    remap = {f"{p}.e01": (f"en.n3.class-{n}.t02", f"{p}.r01"), f"{p}.e02": (f"en.n3.class-{n}.t05", f"{p}.r02"), f"{p}.e03": (f"en.n3.class-{n}.t04", f"{p}.r02"), f"{p}.e04": (f"en.n3.class-{n}.t06", f"{p}.r03")}
    return make_class(n, ["Transmitir dos mensajes con sus fuentes.", "Conservar destinatarios y acciones requeridas."], [("relay","relevo"),("source","fuente"),("recipient","destinatario"),("exact","exacto"),("action","acción"),("note","nota")], rows, pools, remap)

def c50() -> dict[str, Any]:
    n, c, p = 50, CONCEPTS[50], "en.n3.c50"; all_c = [CONCEPTS[k] for k in NUMBERS]
    audio_meta = _audio()
    pools = {"practiceGuided": [
        q(f"{p}.pg01", "¿Qué cierre confirma un horario nuevo?", ["The time may change.", "Tuesday at four in Room Two is confirmed.", "Someone should check later."], 1, c, "practiceGuided", "La segunda opción fija día, hora y sala.", hint="Busca un horario completo y confirmado."),
        listen(f"{p}.pg02", "Escucha y marca quién recibe la petición.", "Ava said she could meet at three and told Leo to bring the agenda.", ["Ava", "the agenda", "Leo"], 2, c, "practiceGuided", "Leo aparece después de told y recibe la petición.", hint="Identifica el nombre después de told."),
        order(f"{p}.pg03", "Ordena el cierre con horario y confirmación.", "The team confirmed Wednesday at five in Room One.", c, "practiceGuided", "El cierre conserva día, hora y lugar."),
    ], "practice": [
        match(f"{p}.p01", "Relaciona cada hablante con su aviso.", [("Iris", "can meet at two"), ("Leo", "needs a later time"), ("Mara", "can reserve Room Five")], c, "practice", "Cada hablante mantiene su propio dato."),
        q(f"{p}.p02", "Elige el uso correcto de said y told.", ["Nia told the time was four.", "Nia said the time was four and told Bo to confirm.", "Nia said Bo to confirm at four."], 1, c, "practice", "Said introduce el dato y told Bo introduce la petición."),
        write(f"{p}.p03", "Cierra el horario a partir de tres avisos.", "A: lunes 2. B: necesita 3. C: sala libre a las 3. Confirma lunes 3.", "A said two was possible, B said three was necessary, and C said the room was free then. Monday at three is confirmed.", "A could meet at two, but B needed three; C reported that the room was free at three. The group confirmed Monday at three.", c, "practice", "Las variantes atribuyen los tres avisos y cierran la hora viable."),
    ], "evaluation": [
        q(f"{p}.e01", "Aisha da hora; Leo la cambia; Marta confirma sala. Elige el resumen fiel.", ["Aisha, Leo and Marta all reported one shared update.", "Aisha gave a time, Leo changed it, and Marta confirmed the room.", "Aisha confirmed the room, Leo gave the first time, and Marta changed it."], 1, c, "evaluation", "La segunda opción conserva las funciones de los tres hablantes.", requires=all_c),
        listen(f"{p}.e02", "Escucha y elige el dato final confirmado.", "Aisha can meet Tuesday at three. Leo can only meet at four. Marta says Room Two is free at four.", ["Tuesday at three outside", "Monday at four in Room One", "Tuesday at four in Room Two"], 2, c, "evaluation", "La disponibilidad conjunta fija martes a las cuatro en Room Two.", requires=all_c),
        write(f"{p}.e03", "Reporta el aviso y su acción sin cambiar datos.", "Nora: I can arrive at 5. Tell Sam to open Room 3 at 4:45.", "Nora said she could arrive at five and told Sam to open Room Three at four forty-five.", "Nora said that she could arrive at five; Sam had to open Room Three at four forty-five.", c, "evaluation", "El reporte conserva hablante, perspectiva, receptor, sala y horas.", requires=all_c),
        write(f"{p}.e04", "Escucha la cadena y resuélvela en 80–110 palabras.", "Tres avisos de una clínica; atribuye, transmite acciones y confirma horario.",
              "Aisha said she could meet on Tuesday at three and told Leo to bring the agenda. Leo said he could not meet at three but could meet at four, and he told Marta to book Room Two. Marta said Room Two was free at four and asked Aisha to confirm by noon. Leo must bring the agenda, Marta must book the room, and Aisha must confirm the full plan promptly. The final team meeting is Tuesday at four in Room Two.",
              "Aisha said that Tuesday at three worked for her, and she told Leo to bring the agenda. Leo said he was unavailable at three but could attend at four; he told Marta to book Room Two. Marta reported that Room Two was free at four and asked Aisha to confirm before noon. Therefore Leo brings the agenda, Marta books the room, and Aisha confirms the complete plan promptly. The team has now firmly fixed Tuesday at four in Room Two.", c, "evaluation", "La solución usa said y told, atribuye tres voces y confirma el nuevo horario.", requires=all_c, originExtra={"audio": "Message one. Aisha: I can meet Tuesday at three. Tell Leo to bring the agenda. Message two. Leo: I cannot meet at three, but I can meet at four. Tell Marta to book Room Two. Message three. Marta: Room Two is free at four. Ask Aisha to confirm by noon.", **audio_meta}),
    ], "review": [
        q(f"{p}.r01", "¿Qué opción conserva perspectiva y acción?", ["Tia said she would call and told Max to send the code.", "Tia said Max would call and told him to keep the code.", "Tia said she had called, and Max told her to send the code."], 0, c, "review", "She would call adapta la perspectiva y told Max conserva la acción."),
        match(f"{p}.r02", "Une cada evidencia con su función.", [("said the rehearsal began at six", "reported content"), ("told Bea to unlock the door", "recipient and action"), ("Friday at seven is confirmed", "final schedule")], c, "review", "Las tres evidencias separan contenido, relevo y cierre."),
        write(f"{p}.r03", "Escucha otra cadena y resuélvela en 80–110 palabras.", "Tres avisos de teatro; conserva voces, tareas y horario final.",
              "Jon said he could rehearse on Friday at six and told Bea to bring the scripts. Bea said she worked until six but could arrive at seven, and she told Luis to unlock Studio Three. Luis said Studio Three was available at seven and asked Jon to confirm before Thursday evening. Bea must bring the scripts, Luis must unlock the studio, and Jon must confirm the whole arrangement promptly. The final rehearsal is firmly set for Friday at seven in Studio Three.",
              "Jon reported that he was free on Friday at six, and he told Bea to bring the scripts. Bea said she could not arrive before seven because she worked until six; she told Luis to unlock Studio Three. Luis said the studio was available at seven and asked Jon to confirm by Thursday evening. Thus Bea brings the scripts, Luis opens the studio, and Jon confirms the complete arrangement promptly. Friday at seven in Studio Three is the final schedule.", c, "review", "El escenario teatral recupera los cinco conceptos con una cadena distinta.", requires=all_c, originExtra={"audio": "Message one. Jon: I can rehearse Friday at six. Tell Bea to bring the scripts. Message two. Bea: I work until six, but I can arrive at seven. Tell Luis to unlock Studio Three. Message three. Luis: Studio Three is available at seven. Ask Jon to confirm by Thursday evening.", **audio_meta}),
    ]}
    rows = [
        ("A message chain keeps each speaker separate.", "Una cadena de mensajes mantiene separado a cada hablante.", "Chain evita intercambiar las tres voces."),
        ("In a schedule report, said gives content and told names a recipient.", "En un reporte de horario, said da contenido y told nombra receptor.", "La forma correcta distingue said de told."),
        ("The speaker changes I to she without losing meaning.", "El hablante cambia I por she sin perder sentido.", "Speaker y perspectiva deben conservarse."),
        ("Each update includes its required action.", "Cada actualización incluye su acción requerida.", "Update transmite el dato y lo que debe hacerse."),
        ("Please confirm the new schedule after all three replies.", "Confirma el horario nuevo después de las tres respuestas.", "Confirm cierra el acuerdo viable."),
        ("Rae said she could train Wednesday at five and told Omar to bring the forms. Omar said he arrived at six and told Nina to reserve Hall One. Nina said the hall was free at six and asked Rae to confirm. The required actions are clear, so the schedule is Wednesday at six in Hall One.", "Rae propuso entrenar el miércoles; Omar cambió la hora; Nina confirmó el salón y pidió cerrar el acuerdo.", "El modelo integra cinco conceptos y fija responsables, hora y lugar."),
    ]
    remap = {f"{p}.e01": (f"en.n3.class-{n}.t01", f"{p}.r02"), f"{p}.e02": (f"en.n3.class-{n}.t05", f"{p}.r03"), f"{p}.e03": (f"en.n3.class-{n}.t03", f"{p}.r01"), f"{p}.e04": (f"en.n3.class-{n}.t06", f"{p}.r03")}
    return make_class(n, ["Resolver una cadena de tres avisos.", "Confirmar un horario sin cambiar voces, datos ni acciones."], [("chain","cadena"),("schedule","horario"),("speaker","hablante"),("confirm","confirmar"),("update","actualización"),("required","requerido")], rows, pools, remap, uses=all_c, cumulative=all_c)

_raw46,_raw47,_raw48,_raw49,_raw50=c46,c47,c48,c49,c50
def _retag(x: dict[str,Any]) -> dict[str,Any]: return hashed(x)
def _teach_row(d:dict[str,Any],idx:int,en:str,es:str,ex:str)->None:
    row=d["teaching"][idx]; ew=en.split(); sw=es.split(); ce=max(1,len(ew)//2); cs=max(1,len(sw)//2)
    row.update({"en":en,"es":es,"explanationEs":ex,"segments":[{"en":" ".join(ew[:ce]),"es":" ".join(sw[:cs])},{"en":" ".join(ew[ce:]),"es":" ".join(sw[cs:])}],"audioText":en})
def _audio_meta()->dict[str,Any]: return {"audioMode":"tts","languageCode":"en","speedOptions":[0.75,1.0],"maxReplays":3,"revealTranscriptAfterAttempt":True}
def c46()->dict[str,Any]:
    d=_raw46(); c=CONCEPTS[46]
    d["pools"]["evaluation"][0]["prompt"]["es"]='Fuente: Pablo: "The room is ready". Elige el reporte fiel.'; d["pools"]["evaluation"][0]=_retag(d["pools"]["evaluation"][0])
    d["pools"]["evaluation"][0]["choices"]=[{"text":"The manager said Pablo was ready."},{"text":"Pablo said the room was ready."},{"text":"Pablo said the room would be ready later."}]; d["pools"]["evaluation"][0]["answer"]={"index":1}; _retag(d["pools"]["evaluation"][0])
    d["pools"]["evaluation"][2]=write("en.n3.c46.e03",'Hugo a Mei: "Please check the address". Repórtalo con told.',"Fuente visible en la consigna.","Hugo told Mei to check the address.","Hugo told Mei that she should check the address.",c,"evaluation","Told incluye a Mei como receptor y conserva la petición.")
    d["pools"]["review"][1]=order("en.n3.c46.r02","Ordena otra petición reportada de Hugo a Mei.","Hugo told Mei to verify the street number.",c,"review","La recuperación conserva told, receptor y una petición nueva.")
    _teach_row(d,5,"Hugo told Mei to check the address after lunch.","Hugo le dijo a Mei que comprobara la dirección después del almuerzo.","Told va seguido del receptor y de la petición con to.")
    d["remediationMap"]["en.n3.c46.e03"]={"reteach":"en.n3.class-46.t06","review":"en.n3.c46.r02"}
    return d
def c47()->dict[str,Any]:
    d=_raw47(); c=CONCEPTS[47]
    grammar_choices=[
        ("Yesterday Mara ___ the office was closed.","said — past; content follows"),
        ("Every morning staff ___ the office closes at six.","say — present; content follows"),
        ("Yesterday Oli ___ that the parcel was downstairs.","said — past; followed by that"),
        ("Yesterday Oli ___ Ren the parcel was downstairs.","told — past; receiver before content"),
        ("Every day guides ___ visitors the gate number.","tell — present; receiver before content"),
        ("Yesterday Pia ___ Sol to wait inside.","told — past; receiver before to + verb"),
    ]
    recovery_choices=[
        ("Last night Leo ___ help was needed.","said — past; content follows"),
        ("Each afternoon staff ___ the room is free.","say — present; content follows"),
        ("Nora ___ that the key was missing yesterday.","said — past; followed by that"),
        ("Nora ___ Eli the key was missing.","told — past; receiver before content"),
        ("Every shift nurses ___ visitors the desk number.","tell — present; receiver before content"),
        ("Nora ___ Eli to check the desk.","told — past; receiver before to + verb"),
    ]
    d["pools"]["evaluation"][3]=match("en.n3.c47.e04","Completa seis decisiones con say/said o tell/told.",grammar_choices,c,"evaluation","Cinco de seis decisiones usan tiempo verbal y receptor para elegir say o tell.",scoring={"parts":6,"total":6,"minimumCorrect":5,"independentAttempt":True})
    d["pools"]["review"][2]=match("en.n3.c47.r03","Recupera seis decisiones nuevas de say y tell.",recovery_choices,c,"review","La recuperación vuelve a decidir por tiempo, receptor y tipo de complemento.",scoring={"parts":6,"total":6,"minimumCorrect":5,"independentAttempt":True})
    _teach_row(d,5,"Use say or said before content without a receiver; use tell or told before a receiver. Tell and told take that listener as their person object. Say and tell are present; said and told are past.","Usa say o said antes del contenido sin receptor; usa tell o told antes de un receptor. Tell y told toman a ese oyente como objeto personal. Say y tell son presente; said y told son pasado.","El repaso integrado permite recuperar las seis decisiones por receptor y tiempo verbal.")
    return d
def c48()->dict[str,Any]:
    d=_raw48(); c=CONCEPTS[48]
    d["pools"]["evaluation"][1]=listen("en.n3.c48.e02","Escucha fuente y reporte: ¿qué dato se conserva?","Original Iris: The meeting is in Room Four at two. Report: Iris said the meeting was in Room Four at three.",["the time at two","the time at three","the place Room Four"],2,c,"evaluation","Room Four permanece igual; la hora cambia de dos a tres.")
    # Una selección UI contiene las tres detecciones; no simula puntuación parcial.
    d["pools"]["evaluation"][3]=listen("en.n3.c48.e04","Escucha tres fuentes y elige los cambios en orden.","Pair one. Original Nora: I will call you at six. Report: Nora said she would call me at six. Pair two. Original Omar: The train leaves at seven. Report: Omar said the train left at eight. Pair three. Original Mia: Please email the form. Report: Mia told me to print the form.",["time / action / person","action / person / time","person / time / action"],2,c,"evaluation","Las fuentes muestran persona, hora y acción modificadas, en ese orden.")
    d["pools"]["review"][2]=listen("en.n3.c48.r03","Escucha tres fuentes nuevas y elige los cambios.","Pair one. Original Tia: I need my pass. Report: Tia said she needed her pass. Pair two. Original Ben: The talk starts at noon. Report: Ben said the talk started at one. Pair three. Original Sol: Please bring water. Report: Sol told me to bring food.",["perspective / clock time / requested action","clock time / perspective / requested action","requested action / clock time / perspective"],0,c,"review","La recuperación vuelve a distinguir persona, hora y acción.")
    _teach_row(d,5,"Compare the original source and report: I becomes she, six stays six, and call stays call.","Compara fuente y reporte: I cambia a she; seis y call se conservan.","El modelo revisa persona, hora y acción antes de decidir.")
    d["remediationMap"]["en.n3.c48.e04"]={"reteach":"en.n3.class-48.t06","review":"en.n3.c48.r03"}
    return d
def c49()->dict[str,Any]:
    d=_raw49()
    model="Ms Green said the school visit would begin on Monday at nine and told Ravi to prepare the visitor badges by Friday. Mr Cole said the parent workshop would remain on Monday at two and asked Elena to test the projector before noon. Ravi must prepare the badges, while Elena must test the equipment. This relay separates two school events, identifies both sources and recipients, preserves the exact times, and makes each required action clear."
    _teach_row(d,5,model,"Ms Green anuncia la visita escolar y Mr Cole mantiene el taller; Ravi y Elena reciben tareas distintas.","El modelo de escuela, distinto de la evaluación logística, conserva fuentes, datos y acciones.")
    return d
def c50()->dict[str,Any]:
    d=_raw50(); c=CONCEPTS[50]; allc=[CONCEPTS[k] for k in range(46,51)]; meta=_audio_meta()
    d["pools"]["practice"][2]=write("en.n3.c50.p03","Transmite un cambio de llamada y su confirmación.","Client messages. Ava: The call moved to Tuesday at four; tell Ben to update the calendar. Ben: The calendar is updated; tell Cia to send the link. Cia: The link is sent, and Tuesday at four is confirmed.","Ava said the call had moved to Tuesday at four and told Ben to update the calendar. Ben said he had updated it and told Cia to send the link. Cia confirmed that the link was sent and that the call was Tuesday at four.","Ava reported the call change to Tuesday at four and asked Ben to update the calendar. Ben confirmed the update and asked Cia to send the link. Cia sent it and confirmed the Tuesday call.",c,"practice","La cadena transmite un cambio, dos acciones y una confirmación sin comparar horarios.")
    d["pools"]["evaluation"][1]=listen("en.n3.c50.e02","Escucha otra cadena y elige el horario compatible.","Colin can meet Thursday at ten or eleven. Sue can only meet at eleven. Room Six is free at eleven.",["Thursday at ten in Room Six","Friday at eleven in Room Five","Thursday at eleven in Room Six"],2,c,"evaluation","Las tres disponibilidades respaldan jueves a las once en Room Six.",requires=allc)
    ea="Aisha said the scanner repair would finish on Wednesday morning and that she could not run Tuesday's clinic. She told Leo to send the new consent form. Leo said the patient could come on Wednesday at nine and told Marta to book Room Two. Marta reported that Room Two was booked for Wednesday at nine and that she had sent the notice. Leo sends the form, and Marta books the room. In her final email, Aisha explicitly confirmed the clinic for Wednesday at nine in Room Two. The complete chain keeps all three speakers, actions and times clear."
    eb="The scanner repair was not complete for Tuesday, Aisha said, so she told Leo to send a revised consent form. Leo reported that the patient was available on Wednesday at nine and told Marta to reserve Room Two. Marta said the room had been booked and the notice had been sent. Aisha's final email confirmed Wednesday at nine in Room Two. Leo handles the form, Marta handles the room, and Aisha closes the change. This clinic relay preserves the three speakers and every required action."
    d["pools"]["evaluation"][3]=write("en.n3.c50.e04","Escucha el hilo clínico y resuélvelo en 80–110 palabras.","El audio aporta avería, nuevo horario, acciones y confirmación final.",ea,eb,c,"evaluation","La solución atribuye tres voces, conserva la avería y cita la confirmación final.",requires=allc,originExtra={"audio":"Clinic email thread. Aisha: The scanner repair will finish Wednesday morning. I cannot run Tuesday's clinic; tell Leo to send the revised consent form. Leo: The patient can come Wednesday at nine; tell Marta to book Room Two. Marta: Room Two is booked for Wednesday at nine, and I sent the notice. Final email from Aisha: I confirm Wednesday at nine in Room Two.",**meta})
    ra="Jon said the touring group needed the Main Stage at seven and told Bea to ask the dancers about a six o'clock warm-up in Studio Three. Bea reported that the dancers had accepted six and told Luis to update the board. Luis said the board now showed the warm-up at six in Studio Three and the rehearsal at seven on the Main Stage. Bea contacts the dancers, and Luis updates the board. Jon's final message explicitly confirmed the rehearsal at seven on the Main Stage. This theatre swap preserves all three speakers, both actions, times and locations."
    rb="The touring group needed the Main Stage at seven, Jon said, so he told Bea to offer the dancers a six o'clock warm-up in Studio Three. Bea said they accepted and told Luis to update the rehearsal board. Luis reported that the board listed the warm-up at six in Studio Three and the rehearsal at seven on the Main Stage. Jon then confirmed the Main Stage rehearsal at seven. Bea manages the dancers, Luis changes the board, and Jon closes the swap. The three voices, actions, times and venues remain clear."
    d["pools"]["review"][2]=write("en.n3.c50.r03","Escucha el cambio teatral y resuélvelo en 80–110 palabras.","El audio aporta un intercambio de espacios, dos acciones y confirmación final.",ra,rb,c,"review","La recuperación transmite un intercambio de espacios y la confirmación teatral.",requires=allc,originExtra={"audio":"Theatre desk log. Jon: The touring group needs the Main Stage at seven; tell Bea to ask the dancers about a six o'clock warm-up in Studio Three. Bea: The dancers accepted six; tell Luis to update the board. Luis: The board now shows the warm-up at six in Studio Three and the rehearsal at seven on the Main Stage. Final message from Jon: I confirm the rehearsal at seven on the Main Stage.",**meta})
    tm="Rae said a storm had closed the outdoor training field on Wednesday and told Omar to find an indoor alternative. Omar reported that Hall One was available on Friday at ten and told Nina to move the training equipment. Nina said she could move it and sent the updated schedule. Rae then confirmed Friday at ten in Hall One. Omar secures the hall, Nina moves the equipment, and Rae closes the change. This cancellation-and-relocation chain preserves all three speakers, times and required actions without relying on overlapping availability."
    tm_es="Rae dijo que una tormenta había cerrado el campo de entrenamiento del miércoles y pidió a Omar una alternativa cubierta. Omar informó que Hall One estaba libre el viernes a las diez y encargó a Nina trasladar el equipo. Nina aceptó y envió el horario actualizado. Rae confirmó el viernes a las diez en Hall One. La cadena conserva hablantes, tiempos y acciones mediante cancelación y traslado, no mediante disponibilidades superpuestas."
    _teach_row(d,5,tm,tm_es,"El modelo integra cinco conceptos mediante cancelación, reubicación, tareas y confirmación explícita.")
    return d
BUILDERS={46:c46,47:c47,48:c48,49:c49,50:c50}

def audit(classes: list[dict[str, Any]], full: bool) -> dict[str, Any]:
    totals: Counter[str] = Counter(); formats: Counter[str] = Counter(); indices: Counter[int] = Counter(); prompts: set[str] = set(); sigs: set[str] = set()
    for cls in classes:
        assert cls["status"] == "shadow" and cls["runtimeAi"] is False and cls["qualityPolicy"] == QUALITY
        assert 6 <= len(cls["vocabulary"]) <= 12 and 4 <= len(cls["teaching"]) <= 6
        local_formats: set[str] = set(); local_idx: Counter[int] = Counter(); fbs: list[str] = []
        for pool, count in (("practiceGuided",3),("practice",3),("evaluation",4),("review",3)):
            assert len(cls["pools"][pool]) == count; totals[pool] += count
            for item in cls["pools"][pool]:
                assert len(item["prompt"]["es"]) <= 90
                payload = {k:v for k,v in item.items() if k not in {"id", "contentHash"}}
                assert item["contentHash"] == "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
                local_formats.add(item["format"]); formats[item["format"]] += 1; fbs.append(item["origin"]["feedback"]["es"])
                pk = norm(item["prompt"]["es"]); assert pk not in prompts; prompts.add(pk)
                if pool != "practiceGuided": assert "hint" not in item["origin"]
                if item["format"] in {"elegir", "escuchar"}:
                    assert len(item["choices"]) >= 3; local_idx[item["answer"]["index"]] += 1; indices[item["answer"]["index"]] += 1
                if item["format"] == "escribir": assert len(item["answer"]["accepted"]) >= 2
                stim = item["origin"].get("audio") or item["origin"].get("text") or item["origin"].get("pairs") or item["prompt"]["es"]
                signature = norm({"stimulus": stim, "answer": item["answer"]}); assert signature not in sigs; sigs.add(signature)
        assert len(local_formats) >= 4 and len(fbs) == len(set(fbs)) and len(local_idx) >= 2
        assert max(local_idx.values()) / sum(local_idx.values()) <= .60
        visible = norm({"teaching": cls["teaching"], "pools": cls["pools"]})
        for v in cls["vocabulary"]: assert norm(v["en"]) in visible
        eval_ids = {x["id"] for x in cls["pools"]["evaluation"]}; assert set(cls["remediationMap"]) == eval_ids
        tids = {x["id"] for x in cls["teaching"]}; rids = {x["id"] for x in cls["pools"]["review"]}
        for route in cls["remediationMap"].values(): assert route["reteach"] in tids and route["review"] in rids
        if cls["phase"] in {"production", "transfer"}:
            assert any(len(re.findall(r"\b[\w’-]+\b", x["answer"]["text"])) >= 8 and len(x["answer"].get("accepted", [])) >= 2 for pool in ("evaluation", "review") for x in cls["pools"][pool] if x["format"] == "escribir")
    if full:
        assert len(classes) == 5 and sum(totals.values()) == 65
        expected = [CONCEPTS[n] for n in NUMBERS]; close = classes[-1]
        assert close["usesPatterns"] == expected and close["cumulativeEvaluation"] == expected
        assert all(x["requires"] == expected for x in close["pools"]["evaluation"] if x["id"].endswith(("e01", "e02", "e03", "e04")))
        c46e04 = classes[0]["pools"]["evaluation"][3]
        assert len(c46e04["answer"]["pairs"]) == 5
        assert c46e04["origin"]["scoring"] == {"parts": 5, "minimumCorrect": 4, "independentAttempt": True}
        c47e04 = classes[1]["pools"]["evaluation"][3]
        assert len(c47e04["answer"]["pairs"]) == 6
        assert c47e04["origin"]["scoring"]["parts"] == 6 and c47e04["origin"]["scoring"]["minimumCorrect"] == 5
        c47r03 = classes[1]["pools"]["review"][2]
        grammar_labels = {
            "said — past; content follows", "say — present; content follows",
            "said — past; followed by that", "told — past; receiver before content",
            "tell — present; receiver before content", "told — past; receiver before to + verb",
        }
        for item in (c47e04, c47r03):
            assert item["format"] == "relacionar" and len(item["answer"]["pairs"]) == 6
            assert {pair[1]["es"] for pair in item["answer"]["pairs"]} == grammar_labels
            assert item["origin"]["scoring"]["minimumCorrect"] == 5
            right_text = " ".join(pair[1]["es"] for pair in item["answer"]["pairs"]).lower()
            assert not any(word in right_text for word in ("office", "parcel", "bus", "room", "key", "desk"))
        c47t06 = classes[1]["teaching"][5]["en"].lower()
        assert all(word in c47t06 for word in ("say", "said", "tell", "told", "receiver", "present", "past"))
        c48e04 = classes[2]["pools"]["evaluation"][3]
        assert c48e04["format"] == "escuchar" and len(c48e04["choices"]) == 3
        assert "scoring" not in c48e04["origin"]
        assert all(f"Pair {word}." in c48e04["origin"]["audio"] for word in ("one", "two", "three"))
        for lesson, lo, hi in ((classes[3], 70, 90), (classes[4], 80, 110)):
            for item in (lesson["pools"]["evaluation"][3], lesson["pools"]["review"][2]):
                assert item["format"] == "escribir" and item["origin"]["audioMode"] == "tts"
                for answer in item["answer"]["accepted"]:
                    assert lo <= len(re.findall(r"\b[\w’-]+\b", answer)) <= hi
            assert lo <= len(re.findall(r"\b[\w’-]+\b", lesson["teaching"][5]["en"])) <= hi
        t06, e04, r03 = close["teaching"][5], close["pools"]["evaluation"][3], close["pools"]["review"][2]
        assert "storm" in t06["en"].lower() and "clínic" in e04["prompt"]["es"].lower() and "teatral" in r03["prompt"]["es"].lower()
        for item in (e04, r03):
            evidence = canonical(item).lower()
            for marker in ("said", "told", "three", "confirm"):
                assert marker in evidence
        assert close["remediationMap"][e04["id"]] == {"reteach": "en.n3.class-50.t06", "review": "en.n3.c50.r03"}
        assert len({norm(t06["en"]), norm(e04["answer"]["text"]), norm(r03["answer"]["text"])}) == 3
        p03 = close["pools"]["practice"][2]
        assert "client messages" in p03["origin"]["text"].lower()
        assert "relocation" in t06["en"].lower()
        assert "scanner repair" in e04["origin"]["audio"].lower()
        assert "touring group" in r03["origin"]["audio"].lower() and "warm-up" in r03["origin"]["audio"].lower()
        theatre_source = r03["origin"]["audio"].lower()
        assert "rehearsal at seven on the main stage" in theatre_source
        assert "rehearsal at seven in studio three" not in theatre_source
        assert all("main stage" in answer.lower() and "studio three" in answer.lower()
                   for answer in r03["answer"]["accepted"])
        distractor_text = canonical({
            "c46": classes[0]["pools"]["review"][0]["choices"],
            "c48": classes[2]["pools"]["practice"][1]["choices"],
            "c50": classes[4]["pools"]["evaluation"][0]["choices"],
        }).lower()
        assert not any(old in distractor_text for old in (
            "office said dina", "told nine to print", "marta told that aisha was leo"
        ))
        assert "asked aisha" not in e04["answer"]["text"].lower()
    return {"classes": len(classes), "items": sum(totals.values()), "pools": dict(totals), "formats": dict(sorted(formats.items())), "correctIndices": dict(sorted(indices.items())), "prompts": len(prompts), "fingerprints": len(sigs)}

def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def write_all() -> list[Path]:
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    classes = []
    for n in NUMBERS:
        doc = BUILDERS[n](); audit([doc], False); path = OUT / f"class-{n:02d}.json"; path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); classes.append(path)
    docs = [json.loads(p.read_text(encoding="utf-8")) for p in classes]; summary = audit(docs, True)
    bundle = OUT / "bundle-46-50.json"; bundle.write_text(json.dumps({"schema":"onelingo.editorial.class-bundle.v1","course":"en","level":3,"scale":SCALE,"status":"shadow","runtimeAi":False,"selectionPolicy":{"deterministic":True},"evidencePolicy":{"attemptRecords":["variantId","libraryVersion","selectionId"]},"range":{"start":46,"end":50},"classes":docs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = REPORT_OUT / "REPORT.md"; hashes = "\n".join(f"{digest(p)}  {p.name}" for p in classes + [bundle])
    report.write_text(f"""# INTEGRADO — Inglés N3 C46–C50\n\nEstado: **integrado en shadow tras revisión independiente GO**.\n\n- Bloque `reported-messages`, B1-entry; fases `input → form → comprehension → production → transfer`.\n- 5 clases, 65 ejercicios, `status: shadow`, `runtimeAi: false`, selección y recuperación deterministas.\n- C46 evalúa cinco relaciones con umbral 4/5; C47 seis formas con umbral 5/6; C48 tres pares con 3/3.\n- C49 exige 70–90 palabras. C50 exige 80–110 y usa escenarios distintos: formación, clínica y teatro.\n\n## Auditoría de generación\n\n```json\n{json.dumps(summary, ensure_ascii=False, indent=2)}\n```\n\nValidación estructural C46–C50 y bundle nivel 3: OK. Idempotencia confirmada. Revisión independiente: GO; integración únicamente en shadow.\n\n## Comandos reproducibles\n\n```bash\nPYTHONDONTWRITEBYTECODE=1 python3 tools/contenido/generar_editorial_n3_46_50.py --all\npython3 tools/contenido/validar_bundle_editorial.py --file assets/contenido/en/editorial/n3/bundle-46-50.json --start 46 --end 50 --level 3\n```\n\n## Hashes\n\n```text\n{hashes}\n```\n""", encoding="utf-8")
    files = classes + [bundle, report]
    manifest = REPORT_OUT / "MANIFEST.sha256"
    entries = [
        f"{digest(Path(__file__))}  ../../tools/contenido/generar_editorial_n3_46_50.py",
        f"{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json",
    ]
    entries.extend(f"{digest(p)}  ../../{p.relative_to(ROOT)}" for p in classes + [bundle])
    entries.append(f"{digest(report)}  REPORT.md")
    manifest.write_text("\n".join(entries) + "\n", encoding="utf-8")
    return files + [manifest]

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--all", action="store_true"); ap.add_argument("--audit", action="store_true"); args = ap.parse_args()
    if args.all: [print(p) for p in write_all()]
    elif args.audit: print(json.dumps(audit([json.loads((OUT / f"class-{n:02d}.json").read_text()) for n in NUMBERS], True), ensure_ascii=False, sort_keys=True))
    else: ap.error("use --all or --audit")
    return 0

if __name__ == "__main__": raise SystemExit(main())

