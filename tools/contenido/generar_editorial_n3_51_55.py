#!/usr/bin/env python3
"""Generate the integrated English N3 C51-C55 editorial shadow block."""
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
REPORT_OUT = ROOT / "build/editorial-n3-51-55"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
SCALE = "client-10-levels-v1"
NUMBERS = range(51, 56)
CONCEPTS = {n: f"n3-phrasal-actions-{n-50}" for n in NUMBERS}
PHASES = {51: "input", 52: "form", 53: "comprehension", 54: "production", 55: "transfer"}
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

def multipart_complete(i: str, prompt: str, source: str, sentences: list[str], canonical_parts: list[str], alternate_parts: list[list[str]], c: str, pool: str, feedback: str) -> dict[str, Any]:
    """Four independently completable inferences with visible result clues."""
    x = base(i, "completar", prompt, c, pool, feedback)
    x["origin"].update({"text": source, "sentences": sentences,
                         "scoring": {"parts": len(canonical_parts), "minimumCorrect": len(canonical_parts), "independentAttempt": True}})
    parts = [{"text": value, "accepted": [value] + list(alts)} for value, alts in zip(canonical_parts, alternate_parts)]
    joined = " | ".join(canonical_parts)
    alt_joined = " | ".join(alts[0] if alts else value for value, alts in zip(canonical_parts, alternate_parts))
    x["answer"] = {"text": joined, "accepted": [joined, alt_joined], "parts": parts}
    return hashed(x)

def replace_teaching(row: dict[str, Any], english: str) -> dict[str, Any]:
    row["en"] = english; row["audioText"] = english
    ew, sw = english.split(), row["es"].split(); ce=max(1,len(ew)//2); cs=max(1,len(sw)//2)
    row["segments"]=[{"en":" ".join(ew[:ce]),"es":" ".join(sw[:cs])},{"en":" ".join(ew[ce:]),"es":" ".join(sw[cs:])}]
    return row

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
        q(f"{p}.r01", "Elige el reporte que mantiene hablante y lugar.", ["Dina said the keys were in the office.", "The office said Dina had keys.", "Dina told were the keys outside."], 0, c, "review", "Dina es la hablante y office es el lugar conservado."),
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
        q(f"{p}.p02", "Elige el reporte que conserva acción y hora.", ["Nia said she would print it at nine.", "Nia said she would call at nine.", "Nia told nine to print it."], 0, c, "practice", "Print y nine conservan los dos datos de la fuente."),
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
        q(f"{p}.e01", "¿Qué resumen mantiene tres hablantes separados?", ["Aisha, Leo and Marta all said the same thing.", "Aisha gave a time, Leo changed it, and Marta confirmed the room.", "Marta told that Aisha was Leo."], 1, c, "evaluation", "La segunda opción conserva las funciones de los tres hablantes.", requires=all_c),
        listen(f"{p}.e02", "Escucha y elige el dato final confirmado.", "Aisha can meet Tuesday at three. Leo can only meet at four. Marta says Room Two is free at four.", ["Tuesday at three outside", "Monday at four in Room One", "Tuesday at four in Room Two"], 2, c, "evaluation", "La disponibilidad conjunta fija martes a las cuatro en Room Two.", requires=all_c),
        write(f"{p}.e03", "Reporta el aviso y su acción sin cambiar datos.", "Nora: I can arrive at 5. Tell Sam to open Room 3 at 4:45.", "Nora said she could arrive at five and told Sam to open Room Three at four forty-five.", "Nora said that she could arrive at five; Sam had to open Room Three at four forty-five.", c, "evaluation", "El reporte conserva hablante, perspectiva, receptor, sala y horas.", requires=all_c),
        write(f"{p}.e04", "Escucha la cadena y resuélvela en 80–110 palabras.", "Tres avisos de una clínica; atribuye, transmite acciones y confirma horario.",
              "Aisha said she could meet on Tuesday at three and told Leo to bring the agenda. Leo said he could not meet at three but could meet at four, and he told Marta to book Room Two. Marta said Room Two was free at four and asked Aisha to confirm by noon. Leo must bring the agenda, Marta must book the room, and Aisha must confirm the full plan promptly. The final team meeting is Tuesday at four in Room Two.",
              "Aisha said that Tuesday at three worked for her, and she told Leo to bring the agenda. Leo said he was unavailable at three but could attend at four; he told Marta to book Room Two. Marta reported that Room Two was free at four and asked Aisha to confirm before noon. Therefore Leo brings the agenda, Marta books the room, and Aisha confirms the complete plan promptly. The team has now firmly fixed Tuesday at four in Room Two.", c, "evaluation", "La solución usa said y told, atribuye tres voces y confirma el nuevo horario.", requires=all_c, originExtra={"audio": "Message one. Aisha: I can meet Tuesday at three. Tell Leo to bring the agenda. Message two. Leo: I cannot meet at three, but I can meet at four. Tell Marta to book Room Two. Message three. Marta: Room Two is free at four. Ask Aisha to confirm by noon.", **audio_meta}),
    ], "review": [
        q(f"{p}.r01", "¿Qué opción conserva perspectiva y acción?", ["Tia said she would call and told Max to send the code.", "Tia told she calls and Max said to the code.", "Max said Tia was the code."], 0, c, "review", "She would call adapta la perspectiva y told Max conserva la acción."),
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

def c51() -> dict[str, Any]:
    n,c,p=51,CONCEPTS[51],"en.n3.c51"
    pools={"practiceGuided":[q(f"{p}.pg01","La sala está oscura: elige la acción útil.",["pick up the lamp","turn on the lamp","fill in the lamp"],1,c,"practiceGuided","Turn on the lamp resuelve la falta de luz.",hint="Relaciona el resultado deseado con la situación."),listen(f"{p}.pg02","Escucha y elige qué debe hacer Lina.","Lina cannot find her keys, so she checks every pocket.",["look for her keys","turn on her keys","fill in her keys"],0,c,"practiceGuided","Look for expresa buscar algo perdido.",hint="Escucha qué objeto no encuentra."),match(f"{p}.pg03","Une cada situación con la acción adecuada.",[("A parcel waits at reception","pick up the parcel"),("A blank application is on the desk","fill in the application")],c,"practiceGuided","Cada verbo completo responde a una situación concreta.",hint="Piensa en el resultado de cada acción.")],"practice":[q(f"{p}.p01","Elige la acción para usar una pantalla apagada.",["look for the screen","fill in the screen","turn on the screen"],2,c,"practice","Turn on activa la pantalla apagada."),listen(f"{p}.p02","Escucha y marca la acción realizada.","Tom collected the medicine from the pharmacy desk.",["filled in the medicine","picked up the medicine","looked for the desk"],1,c,"practice","Picked up describe recoger la medicina en el mostrador."),match(f"{p}.p03","Relaciona problema y solución contextual.",[("The address is missing on the form","fill in the address"),("Your glasses are not in their case","look for the glasses"),("The printer has no power","turn on the printer")],c,"practice","Las soluciones usan el phrasal verb completo y su objeto.")],"evaluation":[q(f"{p}.e01","¿Qué acción permite completar una solicitud?",["pick up each box","look for a desk","fill in every field"],2,c,"evaluation","Fill in every field completa la solicitud."),listen(f"{p}.e02","Escucha y selecciona el resultado.","Mara turned on the heater, and the room became warm.",["She completed a form","She collected a heater","She activated the heater"],2,c,"evaluation","La consecuencia cálida confirma que activó el calentador."),q(f"{p}.e03","El móvil falta: elige una respuesta contextual.",["Look for it under the chair.","Fill it in under the chair.","Turn it on under the chair."],0,c,"evaluation","Look for it responde a la pérdida del móvil."),match(f"{p}.e04","Relaciona cinco situaciones con acciones completas.",[("The office is dark","turn on the office light"),("The parcel is ready at Desk Four","pick up the parcel at Desk Four"),("The keys are missing after lunch","look for the keys after lunch"),("The contact form has empty fields","fill in the contact form"),("The oven is hot after dinner","turn off the oven")],c,"evaluation","Cuatro de cinco relaciones demuestran significado contextual y verbo completo.",scoring={"parts":5,"minimumCorrect":4,"independentAttempt":True})],"review":[q(f"{p}.r01","Elige qué hacer con un formulario vacío.",["fill in the form","pick up the form's light","look for every answer outside"],0,c,"review","Fill in the form corresponde al documento vacío."),listen(f"{p}.r02","Escucha y elige la acción que produjo el resultado.","After Jo pressed the switch, the fan started moving.",["Jo looked for the fan","Jo turned on the fan","Jo filled in the fan"],1,c,"review","El ventilador en movimiento muestra que Jo lo encendió."),match(f"{p}.r03","Recupera cinco acciones en contextos nuevos.",[("A badge waits at security","pick up the badge"),("A survey has unanswered boxes","fill in the survey"),("The hall is dark","turn on the hall lights"),("A ticket is missing","look for the ticket"),("The radio is noisy at bedtime","turn off the radio")],c,"review","La recuperación clasifica cinco contextos distintos.",scoring={"parts":5,"minimumCorrect":4,"independentAttempt":True})]}
    rows=[("Turn on the light when the room is dark.","Enciende la luz cuando la sala esté oscura.","Turn on activa un equipo."),("Pick up the parcel when reception calls.","Recoge el paquete cuando llame recepción.","Pick up describe recoger algo listo."),("Look for the key when it is missing.","Busca la llave cuando falte.","Look for responde a una pérdida."),("Fill in the form before the appointment.","Completa el formulario antes de la cita.","Fill in completa campos de un documento."),("Turn off the oven when cooking ends.","Apaga el horno al terminar.","Turn off detiene un equipo."),("A complete phrasal verb fits its context.","Un verbo frasal completo encaja en su contexto.","Context aclara el significado sin traducir partes." )]
    rem={f"{p}.e01":(f"en.n3.class-{n}.t04",f"{p}.r01"),f"{p}.e02":(f"en.n3.class-{n}.t01",f"{p}.r02"),f"{p}.e03":(f"en.n3.class-{n}.t03",f"{p}.r03"),f"{p}.e04":(f"en.n3.class-{n}.t06",f"{p}.r03")}
    return make_class(n,["Reconocer phrasal verbs por su contexto.","Relacionar cinco situaciones y acciones completas."],[("turn on","encender"),("pick up","recoger"),("look for","buscar"),("fill in","completar"),("turn off","apagar"),("context","contexto")],rows,pools,rem)

def c52() -> dict[str, Any]:
    n,c,p=52,CONCEPTS[52],"en.n3.c52"
    pools={"practiceGuided":[order(f"{p}.pg01","Ordena la instrucción con pronombre.","Turn it off before you leave",c,"practiceGuided","El pronombre it va entre turn y off.",hint="Coloca it dentro del verbo frasal."),q(f"{p}.pg02","Elige la posición correcta de them.",["Pick up them now.","Pick them up now.","Them pick up now."],1,c,"practiceGuided","Pick them up coloca el pronombre en medio.",hint="El pronombre no puede ir después de la partícula."),match(f"{p}.pg03","Une objeto y orden correcta.",[("the form","fill in the form"),("it","fill it in")],c,"practiceGuided","El sustantivo admite posición final; el pronombre va en medio.",hint="Compara nombre y pronombre.")],"practice":[order(f"{p}.p01","Ordena una instrucción con pick up.","Pick the tickets up at noon",c,"practice","El objeto nominal puede aparecer entre pick y up."),q(f"{p}.p02","Selecciona la orden correcta con it.",["Turn off it now.","Turn it off now.","It turn now off."],1,c,"practice","Turn it off respeta la posición obligatoria del pronombre."),match(f"{p}.p03","Relaciona cada objeto con una orden natural.",[("the computer","turn the computer off"),("them","pick them up"),("this section","fill this section in")],c,"practice","Cada orden coloca el objeto de forma válida.")],"evaluation":[order(f"{p}.e01","Ordena la instrucción sobre la lámpara.","Turn the lamp off after lunch",c,"evaluation","El sustantivo the lamp puede ir entre verbo y partícula."),q(f"{p}.e02","Elige la única orden correcta con them.",["Pick up them at reception.","Pick them up at reception.","Them pick at reception up."],1,c,"evaluation","Pick them up mantiene el pronombre dentro del verbo."),order(f"{p}.e03","Ordena la instrucción sobre el formulario.","Fill it in before the meeting",c,"evaluation","Fill it in coloca el pronombre antes de in."),match(f"{p}.e04","Reordena seis instrucciones y relaciónalas.",[("off / turn / the monitor","turn the monitor off"),("off / turn / it","turn it off"),("up / pick / the keys","pick the keys up"),("up / pick / them","pick them up"),("in / fill / the form","fill the form in"),("in / fill / it","fill it in")],c,"evaluation","Cinco de seis órdenes prueban sustantivos posibles y pronombres intermedios.",scoring={"parts":6,"minimumCorrect":5,"independentAttempt":True})],"review":[q(f"{p}.r01","¿Qué orden coloca bien el pronombre?",["Fill in it today.","Fill it in today.","It fill today in."],1,c,"review","Fill it in es la estructura correcta."),order(f"{p}.r02","Ordena una instrucción con objeto nominal.","Pick the medicine up before five",c,"review","The medicine puede ocupar la posición central."),match(f"{p}.r03","Recupera seis órdenes con objetos nuevos.",[("off / turn / the radio","turn the radio off"),("off / turn / it","turn it off now"),("up / pick / the badge","pick the badge up"),("up / pick / them","pick them up later"),("in / fill / this page","fill this page in"),("in / fill / it","fill it in carefully")],c,"review","La recuperación comprueba seis posiciones sin repetir la evaluación.",scoring={"parts":6,"minimumCorrect":5,"independentAttempt":True})]}
    rows=[("Turn the screen off after work.","Apaga la pantalla después del trabajo.","Un objeto nominal puede ir en medio."),("Turn it off after work.","Apágala después del trabajo.","El pronombre debe ir entre turn y off."),("Pick the parcel up at reception.","Recoge el paquete en recepción.","Pick up admite un sustantivo central."),("Pick it up at reception.","Recógelo en recepción.","It no puede ir después de up."),("Fill the form in before noon.","Completa el formulario antes del mediodía.","Fill in admite nombre central."),("Fill it in before noon.","Complétalo antes del mediodía.","La forma separable conserva el pronombre central." )]
    rem={f"{p}.e01":(f"en.n3.class-{n}.t01",f"{p}.r02"),f"{p}.e02":(f"en.n3.class-{n}.t04",f"{p}.r01"),f"{p}.e03":(f"en.n3.class-{n}.t06",f"{p}.r03"),f"{p}.e04":(f"en.n3.class-{n}.t06",f"{p}.r03")}
    return make_class(n,["Colocar nombres y pronombres en verbos separables.","Reordenar seis instrucciones con un umbral de cinco."],[("turn off","apagar"),("pick up","recoger"),("fill in","completar"),("object","objeto"),("pronoun","pronombre"),("particle","partícula")],rows,pools,rem)

def c53() -> dict[str, Any]:
    n,c,p=53,CONCEPTS[53],"en.n3.c53"
    pools={"practiceGuided":[listen(f"{p}.pg01","Escucha e infiere la acción.","The room was dark. Ava pressed the switch, and now we can see.",["filled in a form","turned on the light","picked up a parcel"],1,c,"practiceGuided","La consecuencia visible permite inferir turn on.",hint="Usa el resultado final."),q(f"{p}.pg02","El paquete ya no está en recepción: ¿qué ocurrió?",["Someone picked it up.","Someone looked for the lamp.","Someone filled it in."],0,c,"practiceGuided","Picked it up explica que ya no esté allí.",hint="Relaciona ausencia y recogida."),match(f"{p}.pg03","Une cada resultado con la acción inferida.",[("The form has no empty boxes","filled it in"),("The missing key is now on the desk","looked for and found the key")],c,"practiceGuided","El resultado permite reconstruir la acción.",hint="Observa qué cambió.")],"practice":[listen(f"{p}.p01","Escucha y elige la acción realizada.","Ben needed the fan. He pressed its button, and cool air started moving.",["looked for the button","turned on the fan","filled in the fan"],1,c,"practice","El aire en movimiento confirma que encendió el ventilador."),q(f"{p}.p02","El documento está completo: selecciona la acción.",["turned it off","picked it up outside","filled it in"],2,c,"practice","Filled it in produce un documento completo."),listen(f"{p}.p03","Escucha e identifica la acción de Sol.","Sol checked under the seats until she found her wallet.",["looked for her wallet","turned on her wallet","filled in her wallet"],0,c,"practice","La búsqueda bajo los asientos indica look for.")],"evaluation":[listen(f"{p}.e01","Escucha y selecciona la acción realizada.","The office was cold. Nia pressed the heater switch, and warm air came out.",["picked up the heater","turned on the heater","filled in the heater"],1,c,"evaluation","El aire caliente es el resultado de turn on."),listen(f"{p}.e02","Escucha y marca lo que hizo Omar.","Omar went to Desk Two. He returned with the parcel in his hands.",["looked for a desk","filled in the parcel","picked up the parcel"],2,c,"evaluation","Volver con el paquete muestra que lo recogió."),listen(f"{p}.e03","Escucha y elige la acción inferida.","Mia checked her bag and every drawer. Finally, she found the missing pass.",["looked for the pass","turned off the pass","filled in the drawer"],0,c,"evaluation","Revisar varios lugares hasta encontrarlo es look for."),listen(f"{p}.e04","Escucha cuatro diálogos y elige las acciones en orden.","Dialogue one. The screen was black; Jo pressed the power button, and it lit up. Dialogue two. Kim went to reception and returned carrying the package. Dialogue three. Luis checked every pocket until he found his card. Dialogue four. Bea wrote in every empty box, and the application was complete.",["turn on / pick up / look for / fill in","pick up / turn on / fill in / look for","look for / fill in / turn on / pick up"],0,c,"evaluation","Los resultados revelan turn on, pick up, look for y fill in en orden.",scoring={"parts":4,"minimumCorrect":4,"independentAttempt":True})],"review":[q(f"{p}.r01","La radio empezó a sonar: ¿qué acción ocurrió?",["Someone filled it in.","Someone turned it on.","Someone picked it up at reception."],1,c,"review","El sonido es consecuencia de encender la radio."),listen(f"{p}.r02","Escucha y selecciona la acción de Eli.","Eli visited the service desk and left holding his repaired phone.",["turned on the desk","picked up his phone","looked for a form"],1,c,"review","Salir con el teléfono indica que lo recogió."),listen(f"{p}.r03","Recupera cuatro inferencias con resultados nuevos.","Dialogue one. The lamp began to shine after Rae touched the switch. Dialogue two. Max left the pharmacy carrying his medicine. Dialogue three. Ana searched each shelf and found her notebook. Dialogue four. Ivo completed all blank lines on the card.",["turned on / picked up / looked for / filled in","filled in / looked for / picked up / turned on","picked up / filled in / turned on / looked for"],0,c,"review","La recuperación usa cuatro consecuencias diferentes.",scoring={"parts":4,"minimumCorrect":4,"independentAttempt":True})]}
    rows=[("A dark room becomes bright when you turn on a light.","Una sala oscura se ilumina al encender la luz.","La consecuencia aclara la acción."),("A parcel in your hands means you picked it up.","Un paquete en tus manos indica que lo recogiste.","El resultado permite inferir pick up."),("Checking many places shows you look for something.","Revisar varios lugares muestra que buscas algo.","La situación señala una búsqueda."),("A complete form shows someone filled it in.","Un formulario completo indica que alguien lo llenó.","El documento terminado revela la acción."),("The situation, action and result form one clue.","La situación, acción y resultado forman una pista.","Los tres elementos sostienen la inferencia."),("Infer the phrasal verb from the observed result.","Infiere el verbo frasal por el resultado observado.","Observed result evita depender de traducción literal." )]
    rem={f"{p}.e01":(f"en.n3.class-{n}.t01",f"{p}.r01"),f"{p}.e02":(f"en.n3.class-{n}.t02",f"{p}.r02"),f"{p}.e03":(f"en.n3.class-{n}.t03",f"{p}.r03"),f"{p}.e04":(f"en.n3.class-{n}.t05",f"{p}.r03")}
    return make_class(n,["Inferir acciones mediante situación y consecuencia.","Resolver cuatro diálogos con evidencia observable."],[("situation","situación"),("action","acción"),("result","resultado"),("infer","inferir"),("observed","observado"),("clue","pista")],rows,pools,rem)

def c54() -> dict[str, Any]:
    n,c,p=54,CONCEPTS[54],"en.n3.c54"
    pools={"practiceGuided":[q(f"{p}.pg01","¿Qué acción debe ir primero en la oficina?",["Turn on the scanner.","Pick up a future parcel.","Fill in a missing machine."],0,c,"practiceGuided","Encender el escáner permite usarlo después.",hint="Busca la acción que prepara el equipo."),order(f"{p}.pg02","Ordena una instrucción con pronombre.","Pick it up at the service desk",c,"practiceGuided","Pick it up coloca el pronombre en medio.",hint="Pon it antes de up."),match(f"{p}.pg03","Relaciona paso y objetivo.",[("fill in the collection form","record your details"),("turn on the scanner","read the parcel code")],c,"practiceGuided","Cada paso tiene un propósito práctico.",hint="Observa qué permite hacer cada acción.")],"practice":[listen(f"{p}.p01","Escucha y elige el orden útil.","First collect the package. Then complete the form. Finally, start the scanner.",["pick up / fill in / turn on","fill in / turn off / look for","turn on / look for / pick up"],0,c,"practice","La secuencia conserva las tres instrucciones del audio."),q(f"{p}.p02","Elige la instrucción correcta con pronombre.",["Pick up it at Desk Five.","Pick it up at Desk Five.","It pick at Desk Five up."],1,c,"practice","Pick it up usa la posición correcta."),write(f"{p}.p03","Escribe tres pasos breves en orden.","Paquete en Desk 3; formulario azul; tableta apagada.","First, pick the package up at Desk Three. Next, fill in the blue form. Finally, turn the tablet on.","Pick it up at Desk Three, fill the blue form in, and then turn on the tablet.",c,"practice","Las variantes incluyen tres acciones completas y ordenadas.")],"evaluation":[q(f"{p}.e01","¿Qué nota contiene tres acciones completas?",["Package, form and screen are nearby.","Pick up the parcel, fill in the form and turn on the screen.","Pick the form, fill the parcel and look screen."],1,c,"evaluation","La segunda nota expresa las tres acciones requeridas."),order(f"{p}.e02","Ordena la instrucción sobre el formulario.","Fill it in before you collect the parcel",c,"evaluation","Fill it in mantiene el pronombre central y el orden útil."),listen(f"{p}.e03","Escucha y marca el último paso.","Pick up the box at reception, fill in the receipt, and turn on the label printer.",["collect the box","complete the receipt","start the label printer"],2,c,"evaluation","La impresora se enciende al final."),write(f"{p}.e04","Redacta 70–90 palabras con tres instrucciones prácticas.","Paquete: Desk 4. Formulario: código K28. Equipo: lector verde. Orden: recoger, completar, encender.","First, go to Desk Four and pick up the parcel with your name on it. Next, fill in the collection form and write code K28 in the reference box. Check that every required field is complete. Finally, turn on the green reader and place the parcel code under it. Keep the receipt after the reader confirms the number. These steps complete the collection in a clear and useful order.","At Desk Four, pick the parcel up after staff check your name. Then fill the collection form in, using K28 as the reference code, and check all required fields. After that, turn the green reader on and scan the code on the parcel. Wait for its confirmation and keep your receipt. The three instructions place each object correctly and guide the user through the collection process in order.",c,"evaluation","Las notas incluyen recoger, completar y encender con objetos correctos y orden útil.",originExtra={"scoring":{"wordRange":[70,90],"independentAttempt":True}})],"review":[q(f"{p}.r01","Elige la primera acción para retirar una caja.",["Pick up the box at reception.","Fill in the light.","Turn on the reception."],0,c,"review","Pick up the box inicia la retirada."),match(f"{p}.r02","Une instrucción y objeto correcto.",[("fill it in","registration card"),("turn it on","ticket machine"),("pick it up","reserved envelope")],c,"review","Cada pronombre remite a un objeto compatible."),write(f"{p}.r03","Escribe 70–90 palabras para otro trámite.","Sobre: Window 2. Tarjeta: número B17. Equipo: terminal azul. Orden: recoger, completar, encender.","First, pick up the reserved envelope at Window Two and check your name. Next, fill in the registration card, including number B17 in the reference field. Review the card so no required box is empty. Finally, turn on the blue terminal and enter the envelope code. Wait until the terminal confirms it, and keep both the card and receipt. This order makes the three practical actions easy to follow.","Go to Window Two and pick the reserved envelope up after checking your name. Fill the registration card in with reference B17, then review every required box. Next, turn the blue terminal on and enter the envelope code. Wait for the confirmation before keeping the card and receipt. These three complete instructions use each object clearly and lead the visitor through the different process in a useful order.",c,"review","La recuperación aplica las tres acciones a un trámite distinto.",originExtra={"scoring":{"wordRange":[70,90],"independentAttempt":True}})]}
    rows=[("Pick up the parcel at Desk Four first.","Primero recoge el paquete en el Desk Four.","La primera instrucción fija acción y lugar."),("Fill in the collection form next.","Luego completa el formulario de recogida.","La segunda instrucción usa el documento correcto."),("Turn on the green reader finally.","Finalmente enciende el lector verde.","La tercera instrucción prepara el equipo."),("Place an object clearly in every instruction.","Coloca un objeto claro en cada instrucción.","Object placement evita ambigüedad."),("Use first, next and finally for useful order.","Usa primero, luego y finalmente para un orden útil.","Order hace operativa la nota."),("A practical note joins three complete actions.","Una nota práctica une tres acciones completas.","Practical instructions deben poder seguirse." )]
    rem={f"{p}.e01":(f"en.n3.class-{n}.t06",f"{p}.r02"),f"{p}.e02":(f"en.n3.class-{n}.t02",f"{p}.r02"),f"{p}.e03":(f"en.n3.class-{n}.t03",f"{p}.r03"),f"{p}.e04":(f"en.n3.class-{n}.t06",f"{p}.r03")}
    return make_class(n,["Dar tres instrucciones prácticas completas.","Ordenar recogida, formulario y encendido."],[("pick up","recoger"),("fill in","completar"),("turn on","encender"),("object","objeto"),("order","orden"),("practical","práctico")],rows,pools,rem)

def c55() -> dict[str, Any]:
    n,c,p=55,CONCEPTS[55],"en.n3.c55"; allc=[CONCEPTS[k] for k in NUMBERS]; meta=_audio()
    pools={"practiceGuided":[q(f"{p}.pg01","¿Qué acción inicia una rutina de pérdida?",["Look for the missing item.","Turn on the form.","Fill in the pickup point."],0,c,"practiceGuided","Look for inicia la búsqueda del objeto.",hint="Empieza por localizar lo perdido."),listen(f"{p}.pg02","Escucha y marca el dato para el formulario.","The missing bag is red, and its case number is L nine.",["blue bag, case B9","red bag, case L9","red phone, case L8"],1,c,"practiceGuided","Red bag y L9 son los datos exactos.",hint="Conserva color y código."),order(f"{p}.pg03","Ordena la confirmación de recogida.","Pick it up at the information desk at four",c,"practiceGuided","La confirmación fija objeto, lugar y hora.",hint="Pon it entre pick y up.")],"practice":[match(f"{p}.p01","Relaciona fase y acción.",[("search","look for the wallet"),("report","fill in the lost-item form"),("collection","pick it up at reception")],c,"practice","Las tres fases resuelven la pérdida en orden."),q(f"{p}.p02","Elige la instrucción correcta con pronombre.",["Pick up it after six.","Pick it up after six.","It pick after six up."],1,c,"practice","Pick it up coloca el pronombre correctamente."),write(f"{p}.p03","Cierra una rutina breve de objeto perdido.","Buscas gafas; formulario G6; recogida en Gate 2 a las 5.","Look for the glasses, fill in form G6, and pick them up at Gate Two at five.","First look for the glasses; then complete form G6 and collect them at Gate Two at five.",c,"practice","Las variantes incluyen búsqueda, reporte y recogida confirmada.")],"evaluation":[listen(f"{p}.e01","Escucha y elige la búsqueda descrita.","I checked under every seat and inside my backpack for the missing camera.",["filled in a camera","looked for the camera","turned on every seat"],1,c,"evaluation","Revisar varios lugares describe look for.",requires=allc),q(f"{p}.e02","¿Qué orden coloca bien el objeto?",["Pick it up at Desk Six.","Pick up it at Desk Six.","It pick Desk Six up."],0,c,"evaluation","Pick it up conserva el pronombre central.",requires=allc),listen(f"{p}.e03","Escucha e infiere el resultado.","Nora completed every field with case code M four. The clerk accepted the report.",["She turned on a bag.","She picked up a code.","She filled in the form."],2,c,"evaluation","El reporte aceptado muestra que completó el formulario.",requires=allc),write(f"{p}.e04","Escucha la llamada y resuelve el caso en 80–110 palabras.","Llamada de estación; describe búsqueda, formulario y recogida.","I looked for my black backpack under the platform seats and beside the ticket machine, but I could not find it. The station agent told me to fill in the lost-item form with case code S24 and my phone number. She then confirmed that the bag was at the information desk. I will pick it up there on Tuesday at five and show my identification. This plan records the search, completes the report and confirms the collection point and time.","First, I looked for the black backpack beneath the platform seats and near the ticket machine. When it was still missing, I filled the lost-item form in with code S24 and my phone number. The agent said the backpack had reached the information desk. I will pick it up on Tuesday at five and bring identification. The three steps explain where I searched, how I reported the loss and exactly where and when collection is confirmed.",c,"evaluation","La solución integra contexto, objeto bien colocado, inferencia, instrucciones y cierre.",requires=allc,originExtra={"audio":"Station call. You say: I lost my black backpack. I looked under the platform seats and beside the ticket machine. The agent says: Fill in the lost-item form with case code S24 and your phone number. We found the bag. Pick it up at the information desk on Tuesday at five, and bring identification.",**meta,"scoring":{"wordRange":[80,110],"independentAttempt":True}})],"review":[q(f"{p}.r01","Elige el paso que documenta la pérdida.",["Turn on the suitcase.","Fill in the lost-item report.","Pick up an empty field."],1,c,"review","Fill in the report registra la pérdida.",requires=allc),match(f"{p}.r02","Une evidencia y fase de solución.",[("checked the café tables","search described"),("entered code C31","form completed"),("Desk One at noon","collection confirmed")],c,"review","Las evidencias hacen observables las tres fases.",requires=allc),write(f"{p}.r03","Escucha otro caso y resuélvelo en 80–110 palabras.","Llamada de biblioteca; conserva búsqueda, reporte y recogida.","I looked for my blue tablet on the reading tables and near the charging shelf, but it was not there. The librarian asked me to fill in the lost-property form with code B31 and my email address. Later, she said the tablet was safe at the main service desk. I will pick it up on Saturday at noon and bring my library card. The response describes the search, completes the correct form and confirms a clear place and time for collection.","First, I looked for the blue tablet across the reading tables and beside the charging shelf. Because I did not find it, I filled the lost-property form in with B31 and my email address. The librarian later confirmed that it was at the main service desk. I will pick it up there on Saturday at noon with my library card. These steps preserve the search locations, the report details and the exact collection arrangement.",c,"review","El caso de biblioteca recupera los cinco conceptos en un escenario distinto.",requires=allc,originExtra={"audio":"Library call. You say: My blue tablet is missing. I looked on the reading tables and near the charging shelf. The librarian says: Fill in the lost-property form with B31 and your email. We found the tablet. Pick it up at the main service desk on Saturday at noon, and bring your library card.",**meta,"scoring":{"wordRange":[80,110],"independentAttempt":True}})]}
    rows=[("Look for the lost suitcase near the airport seats.","Busca la maleta perdida cerca de los asientos del aeropuerto.","El contexto inicia una búsqueda concreta."),("Fill the lost-item form in with code A18.","Completa el formulario con el código A18.","El objeto nominal puede ir dentro del verbo separable."),("The clerk found it, so the observed result ends the search.","El empleado la encontró, así que el resultado observado cierra la búsqueda.","La consecuencia permite inferir qué ocurrió."),("Pick it up at Airport Desk Seven at three.","Recógela en Airport Desk Seven a las tres.","La instrucción usa pronombre central y lugar exacto."),("Confirm the collection point and time in the final plan.","Confirma el punto y la hora de recogida en el plan final.","El cierre vuelve útil la rutina."),("At the airport, I looked for my grey suitcase beside the baggage belts. I filled the lost-item form in with code A18 and my email. The clerk said it was at Desk Seven. I will pick it up there at three with my passport. The search, form and collection are now confirmed.","En el aeropuerto busqué la maleta, completé el reporte y confirmé la recogida.","El modelo integra los cinco conceptos en un caso aeroportuario." )]
    rem={f"{p}.e01":(f"en.n3.class-{n}.t01",f"{p}.r02"),f"{p}.e02":(f"en.n3.class-{n}.t04",f"{p}.r02"),f"{p}.e03":(f"en.n3.class-{n}.t03",f"{p}.r01"),f"{p}.e04":(f"en.n3.class-{n}.t06",f"{p}.r03")}
    return make_class(n,["Resolver un objeto perdido mediante tres fases.","Confirmar búsqueda, formulario y recogida."],[("look for","buscar"),("fill in","completar"),("pick up","recoger"),("search","búsqueda"),("form","formulario"),("collection","recogida")],rows,pools,rem,uses=allc,cumulative=allc)

_c51_raw, _c52_raw, _c53_raw, _c54_raw, _c55_raw = c51, c52, c53, c54, c55
def scored(x: dict[str, Any], parts: int, minimum: int) -> dict[str, Any]:
    x["origin"]["scoring"]={"parts":parts,"minimumCorrect":minimum,"independentAttempt":True}
    return hashed(x)
def extend_answer(x: dict[str, Any], first: str, second: str) -> dict[str, Any]:
    x["answer"]["accepted"][0] += first; x["answer"]["accepted"][1] += second
    x["answer"]["text"] = x["answer"]["accepted"][0]
    return hashed(x)
def align_teaching(d: dict[str, Any], token: str) -> dict[str, Any]:
    for row in d["teaching"]:
        if token not in norm(row["en"]):
            row["en"] += f" This {token} is clear."
            row["audioText"] = row["en"]
            ew=row["en"].split(); es=row["es"].split(); ce=max(1,len(ew)//2); cs=max(1,len(es)//2)
            row["segments"]=[{"en":" ".join(ew[:ce]),"es":" ".join(es[:cs])},{"en":" ".join(ew[ce:]),"es":" ".join(es[cs:])}]
    return d
def c51() -> dict[str, Any]:
    d=_c51_raw(); c=CONCEPTS[51]
    d["pools"]["practice"][2]=write("en.n3.c51.p03","Escribe soluciones para tres problemas.","Dirección ausente; gafas perdidas; impresora apagada.","Fill in the address, look for the glasses, and turn on the printer.","Fill the address in, look for the glasses, then turn the printer on.",c,"practice","Las soluciones usan tres phrasal verbs completos con sus objetos.")
    d["pools"]["review"][0]=q("en.n3.c51.r01","El formulario está vacío: ¿qué acción completa sus campos?",["fill in the form","look for the form","pick up the form"],0,c,"review","Fill in the form completa los campos; las otras acciones no los completan.")
    replace_teaching(d["teaching"][5],"A dark room needs turn on; a ready parcel needs pick up; a missing key needs look for; a blank form needs fill in; a hot oven needs turn off.")
    return align_teaching(d,"context")
def c52() -> dict[str, Any]:
    d=_c52_raw(); c=CONCEPTS[52]
    d["pools"]["practice"][1]=listen("en.n3.c52.p02","Escucha y selecciona la orden correcta.","The computer is still on. Please switch it off now.",["Turn off it now.","Turn it off now.","It turn now off."],1,c,"practice","Turn it off respeta la posición obligatoria del pronombre.")
    d["pools"]["practice"][2]=write("en.n3.c52.p03","Escribe tres órdenes con objetos distintos.","Computadora; llaves; sección del formulario.","Turn the computer off, pick the keys up, and fill this section in.","Turn it off, pick them up, and fill it in.",c,"practice","Las variantes colocan nombres o pronombres de forma válida.")
    d["pools"]["evaluation"][1]=q("en.n3.c52.e02","Elige: pronoun como object antes de particle.",["Pick them up at reception.","Pick up them at reception.","Them pick at reception up."],0,c,"evaluation","Pick them up mantiene el pronombre dentro del verbo.")
    d["pools"]["review"][0]=q("en.n3.c52.r01","¿Qué orden coloca bien el pronombre?",["Fill in it today.","It fill today in.","Fill it in today."],2,c,"review","Fill it in es la estructura correcta.")
    d["pools"]["review"][1]=listen("en.n3.c52.r02","Escucha y elige la instrucción bien ordenada.","The medicine is ready. Collect it before five.",["Pick up it before five.","Pick it up before five.","It pick before five up."],1,c,"review","Pick it up coloca el pronombre entre verbo y partícula.")
    d["pools"]["review"][2]=match("en.n3.c52.r03","Recupera seis órdenes con contextos nuevos.",[("quietly / off / turn / the radio","turn the radio off quietly"),("quietly / off / turn / it","turn it off quietly"),("at noon / up / pick / the badge","pick the badge up at noon"),("at noon / up / pick / them","pick them up at noon"),("carefully / in / fill / this page","fill this page in carefully"),("carefully / in / fill / it","fill it in carefully")],c,"review","La recuperación comprueba seis posiciones en instrucciones nuevas.",scoring={"parts":6,"total":6,"minimumCorrect":5,"independentAttempt":True})
    d["remediationMap"]["en.n3.c52.e01"]={"reteach":"en.n3.class-52.t01","review":"en.n3.c52.r03"}
    replace_teaching(d["teaching"][5],"Use the six patterns: turn the monitor off, turn it off, pick the keys up, pick them up, fill the form in, and fill it in.")
    return align_teaching(d,"object")
def c53() -> dict[str, Any]:
    d=_c53_raw(); c=CONCEPTS[53]
    d["pools"]["evaluation"][0]=listen("en.n3.c53.e01","Escucha y selecciona la acción realizada.","The office was cold. Nia pressed the heater switch, and warm air came out.",["repaired the heater","turned on the heater","opened the heater vent"],1,c,"evaluation","El aire caliente tras pulsar el interruptor muestra que encendió el calentador.")
    d["pools"]["evaluation"][1]=q("en.n3.c53.e02","Omar vuelve de Desk Two con el paquete: ¿qué hizo?",["looked for a desk","filled in the parcel","picked up the parcel"],2,c,"evaluation","Volver con el paquete muestra que lo recogió.")
    d["pools"]["evaluation"][2]=listen("en.n3.c53.e03","Escucha y elige la acción inferida.","Mia checked her bag and every drawer. Finally, she found the missing pass.",["looked for the pass","put the pass in a drawer","checked the pass details"],0,c,"evaluation","Revisar varios lugares hasta encontrarlo es look for.")
    source=("Four result notes: Jo pressed a switch and a dark room became bright. Kim returned from reception carrying a parcel. "
            "Luis checked every pocket and then held his missing card. Bea wrote in every empty box and the application had no blanks.")
    sentences=["The dark room became bright after Jo pressed a switch: she ___.",
               "Kim returned carrying the parcel from reception: she ___.",
               "Luis checked every pocket before holding the card: he ___.",
               "Bea wrote in every empty box and left no blanks: she ___."]
    d["pools"]["evaluation"][3]=multipart_complete("en.n3.c53.e04","Completa cuatro inferencias según cuatro resultados visibles.",source,sentences,["turned on the light","picked up the parcel","looked for the card","filled in the application"],[["switched on the light"],["collected the parcel"],["searched for the card"],["completed the application"]],c,"evaluation","Cada respuesta infiere una acción distinta a partir del resultado, no de una palabra revelada.")
    review_source=("Four new result notes: Rae touched a switch and the lamp began to shine. Max left the pharmacy carrying medicine. "
                   "Ana searched each shelf and then held her notebook. Ivo wrote in every blank line and the card was complete.")
    review_sentences=["The lamp began to shine after Rae touched a switch: she ___.",
                      "Max left the pharmacy carrying medicine: he ___.",
                      "Ana searched each shelf before holding her notebook: she ___.",
                      "Ivo wrote in every blank line and the card was complete: he ___ ."]
    d["pools"]["review"][2]=multipart_complete("en.n3.c53.r03","Recupera cuatro inferencias con resultados nuevos.",review_source,review_sentences,["turned on the lamp","picked up the medicine","looked for the notebook","filled in the card"],[["switched on the lamp"],["collected the medicine"],["searched for the notebook"],["completed the card"]],c,"review","La recuperación exige cuatro inferencias independientes con resultados nuevos.")
    replace_teaching(d["teaching"][4],"Infer turn on when a device becomes active, pick up when an object is carried away, look for when a search finds something, and fill in when blanks disappear.")
    replace_teaching(d["teaching"][5],"For four clues, connect the situation, the observed result and one action: light, parcel, found object and completed form.")
    d["pools"]["review"][0]=write("en.n3.c53.r01","Escribe la acción inferida por el resultado.","La radio empezó a sonar después de pulsar el botón.","Someone turned on the radio.","The radio was turned on.",c,"review","Las variantes expresan la acción inferida por el sonido.")
    d["remediationMap"]["en.n3.c53.e04"]={"reteach":"en.n3.class-53.t05","review":"en.n3.c53.r03"}
    return align_teaching(d,"clue")
def c54() -> dict[str, Any]:
    d=_c54_raw()
    d["pools"]["practiceGuided"][0]=q("en.n3.c54.pg01","¿Qué paso va primero para recoger el paquete?",["Pick up the parcel at Desk Four","Fill in the collection form","Turn on the green reader"],0,CONCEPTS[54],"practiceGuided","Pick up inicia la secuencia; las otras acciones vienen después.",hint="Observa el orden de las tres acciones.")
    d["pools"]["practiceGuided"][2]=match("en.n3.c54.pg03","Relaciona cada paso con su propósito.",[("check the desk number","find the collection point"),("show identification","prove who owns the parcel")],CONCEPTS[54],"practiceGuided","Los propósitos preparan una recogida segura.",hint="Relaciona cada paso con su resultado.")
    d["pools"]["practice"][1]["prompt"]["es"]="Elige la instrucción de paquete con pronombre."
    d["pools"]["practice"][1]=hashed(d["pools"]["practice"][1])
    d["pools"]["evaluation"][1]["prompt"]["es"]="Ordena el formulario antes de recoger el paquete."
    d["pools"]["evaluation"][1]=hashed(d["pools"]["evaluation"][1])
    e=d["pools"]["evaluation"][3]; e["prompt"]["es"]="Escucha y redacta 70–90 palabras con tres instrucciones."; e["origin"].update({"audio":"Collect a parcel at Desk Four after staff check your name. Fill in the collection form with code K28 and every required field. Turn on the green reader, scan the parcel code, wait for confirmation and keep the receipt.",**_audio()}); e["answer"]["accepted"]=[a+" Follow this order." for a in e["answer"]["accepted"]]; e["answer"]["text"]=e["answer"]["accepted"][0]; hashed(e)
    r=d["pools"]["review"][2]; r["prompt"]["es"]="Escucha otro trámite y redacta 70–90 palabras."; r["origin"].update({"audio":"Collect a reserved envelope at Window Two after staff check your name. Fill in the registration card with B17 and every required box. Turn on the blue terminal, enter the envelope code, wait for confirmation and keep the card and receipt.",**_audio()}); r["answer"]["accepted"]=[a+" Follow this order." for a in r["answer"]["accepted"]]; r["answer"]["text"]=r["answer"]["accepted"][0]; hashed(r)
    d["pools"]["review"][0]=q("en.n3.c54.r01","¿Qué paso completa el documento de recogida?",["Fill in the registration card","Pick up the reserved envelope","Turn on the blue terminal"],0,CONCEPTS[54],"review","Fill in completa el documento; las otras acciones pertenecen a pasos distintos.")
    rows=[("A practical first step is to pick up the badge at reception.","Un primer paso práctico es recoger la credencial.","Usa otro objeto y lugar."),("A practical next step is to fill in the visitor card.","Luego completa la tarjeta de visitante.","Nombra un documento distinto."),("A practical final step is to turn on the room projector.","Finalmente enciende el proyector.","No anticipa el equipo evaluado."),("A practical instruction places each object clearly.","Una instrucción práctica coloca cada objeto claramente.","Object placement evita ambigüedad."),("A practical note uses first, next and finally for order.","Una nota práctica usa primero, luego y finalmente.","Order vuelve útil la secuencia."),("At the community centre, first pick up the visitor badge at reception. Next, fill in the attendance card with your group name and meeting number. Check that the contact field is complete. Finally, turn on the room projector, enter the session code and wait for the welcome screen. Keep the badge and card during the workshop. This practical note gives three complete actions, correct objects and a useful order for every participant.","En el centro comunitario se recoge una credencial, se completa una tarjeta y se enciende un proyector.","El modelo integrado tiene 70–90 palabras y otro escenario." )]
    d["teaching"]=teaching(54,rows); d["remediationMap"]["en.n3.c54.e02"]={"reteach":"en.n3.class-54.t04","review":"en.n3.c54.r02"}
    return d
def c55() -> dict[str, Any]:
    d=_c55_raw()
    allc=[CONCEPTS[k] for k in NUMBERS]
    d["pools"]["evaluation"][0]=listen("en.n3.c55.e01","Escucha y elige la búsqueda descrita.","I checked under every seat and inside my backpack for the missing camera.",["checked the camera settings","looked for the camera","left the camera under a seat"],1,CONCEPTS[55],"evaluation","Revisar varios lugares para hallar la cámara describe look for.",requires=allc)
    d["pools"]["evaluation"][2]=listen("en.n3.c55.e03","Escucha e infiere el resultado.","Nora completed every field with case code M four. The clerk accepted the report.",["checked the case code","picked up the report","filled in the form"],2,CONCEPTS[55],"evaluation","El reporte aceptado después de completar cada campo muestra que llenó el formulario.",requires=allc)
    d["pools"]["review"][0]=q("en.n3.c55.r01","¿Qué paso registra una pérdida?",["Fill in the lost-item report","Look for the missing backpack","Pick up the backpack at the desk"],0,CONCEPTS[55],"review","Fill in the report registra los datos; buscar y recoger son fases distintas.",requires=allc)
    model="At the airport, I looked for my grey suitcase beside the baggage belts and near the exit, but I could not find it. I filled the lost-item form in with case code A18, my email and my passport number. The clerk said the suitcase had been found at Desk Seven. I will pick it up there at three and show my passport. These instructions preserve the context, place the object correctly, infer the result, and confirm the search, completed form and collection time."
    row=d["teaching"][5]; row["en"]=model; row["audioText"]=model
    ew=model.split(); es=row["es"].split(); ce=len(ew)//2; cs=max(1,len(es)//2)
    row["segments"]=[{"en":" ".join(ew[:ce]),"es":" ".join(es[:cs])},{"en":" ".join(ew[ce:]),"es":" ".join(es[cs:])}]
    for item in (d["pools"]["evaluation"][3],d["pools"]["review"][2]):
        item["answer"]["accepted"][1]+=" This confirms the stated collection place and time."
        item["answer"]["text"]=item["answer"]["accepted"][0]; hashed(item)
    d["remediationMap"]["en.n3.c55.e02"]={"reteach":"en.n3.class-55.t04","review":"en.n3.c55.r03"}
    return align_teaching(d,"search")
BUILDERS = {51:c51,52:c52,53:c53,54:c54,55:c55}

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
        c51e04 = classes[0]["pools"]["evaluation"][3]
        assert c51e04["format"] == "relacionar" and len(c51e04["answer"]["pairs"]) == 5 and c51e04["origin"]["scoring"]["minimumCorrect"] == 4
        c52e04 = classes[1]["pools"]["evaluation"][3]
        assert c52e04["format"] == "relacionar" and len(c52e04["answer"]["pairs"]) == 6 and c52e04["origin"]["scoring"]["minimumCorrect"] == 5
        c53e04 = classes[2]["pools"]["evaluation"][3]; c53r03 = classes[2]["pools"]["review"][2]
        for item in (c53e04, c53r03):
            assert item["format"] == "completar" and len(item["origin"]["sentences"]) == 4 and len(item["answer"]["parts"]) == 4
            assert item["origin"]["scoring"] == {"parts": 4, "minimumCorrect": 4, "independentAttempt": True}
            assert all("___" in sentence for sentence in item["origin"]["sentences"])
        for lesson, lo, hi in ((classes[3], 70, 90), (classes[4], 80, 110)):
            for item in (lesson["pools"]["evaluation"][3], lesson["pools"]["review"][2]):
                assert item["format"] == "escribir"
                for answer in item["answer"]["accepted"]:
                    assert lo <= len(re.findall(r"\b[\w’-]+\b", answer)) <= hi
        t06, e04, r03 = close["teaching"][5], close["pools"]["evaluation"][3], close["pools"]["review"][2]
        assert "airport" in t06["en"].lower() and "estación" in e04["origin"]["text"].lower() and "biblioteca" in r03["origin"]["text"].lower()
        for item in (e04, r03):
            evidence = canonical(item).lower()
            for marker in ("look", "fill", "pick", "form"):
                assert marker in evidence
        assert close["remediationMap"][e04["id"]] == {"reteach": "en.n3.class-55.t06", "review": "en.n3.c55.r03"}
        assert len({norm(t06["en"]), norm(e04["answer"]["text"]), norm(r03["answer"]["text"])}) == 3
    return {"classes": len(classes), "items": sum(totals.values()), "pools": dict(totals), "formats": dict(sorted(formats.items())), "correctIndices": dict(sorted(indices.items())), "prompts": len(prompts), "fingerprints": len(sigs)}

def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def write_all() -> list[Path]:
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    classes = []
    for n in NUMBERS:
        doc = BUILDERS[n](); audit([doc], False); path = OUT / f"class-{n:02d}.json"; path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); classes.append(path)
    docs = [json.loads(p.read_text(encoding="utf-8")) for p in classes]; summary = audit(docs, True)
    bundle = OUT / "bundle-51-55.json"; bundle.write_text(json.dumps({"schema":"onelingo.editorial.class-bundle.v1","course":"en","level":3,"scale":SCALE,"status":"shadow","runtimeAi":False,"selectionPolicy":{"deterministic":True},"evidencePolicy":{"attemptRecords":["variantId","libraryVersion","selectionId"]},"range":{"start":51,"end":55},"classes":docs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = REPORT_OUT / "REPORT.md"; hashes = "\n".join(f"{digest(p)}  {p.name}" for p in classes + [bundle])
    report.write_text(f"""# INTEGRADO — Inglés N3 C51–C55\n\nEstado: **integrado en shadow tras revisión independiente GO**.\n\n- Bloque `phrasal-actions`, B1-entry; 5 clases, 65 ejercicios, shadow/no-AI.\n- Umbrales: C51 4/5, C52 5/6, C53 cuatro diálogos; C54 70–90 y C55 80–110 palabras.\n- C55 integra cinco conceptos en aeropuerto, estación y biblioteca.\n\n## Auditoría\n```json\n{json.dumps(summary,ensure_ascii=False,indent=2)}\n```\n\nValidación estructural e idempotencia: OK. Revisión independiente: GO; integración únicamente en shadow.\n""",encoding="utf-8")
    files = classes + [bundle, report]
    manifest = REPORT_OUT / "MANIFEST.sha256"
    entries = [
        f"{digest(Path(__file__))}  ../../tools/contenido/generar_editorial_n3_51_55.py",
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

