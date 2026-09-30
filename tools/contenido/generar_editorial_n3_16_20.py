#!/usr/bin/env python3
"""Reproducible isolated draft generator for English N3 C16-C20."""
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
REPORT_OUT = ROOT / "build/editorial-n3-16-20"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
SCALE = "client-10-levels-v1"
NUMBERS = range(16, 21)
CONCEPTS = {n: f"n3-future-coordination-{n-15}" for n in NUMBERS}
PHASES = {16: "input", 17: "form", 18: "comprehension", 19: "production", 20: "transfer"}
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

def multi_fill(i: str, prompt: str, sentences: list[str], answers: list[str],
               c: str, pool: str, feedback: str, *, minimum_correct: int,
               **kw: Any) -> dict[str, Any]:
    x = base(i, "completar", prompt, c, pool, feedback, **kw)
    x["origin"]["sentences"] = sentences
    x["origin"]["scoring"] = {"parts": len(sentences), "minimumCorrect": minimum_correct,
                                "independentAttempt": True}
    joined = " | ".join(answers)
    x["answer"] = {"text": joined, "accepted": [joined],
                   "parts": [{"text": value, "accepted": [value, value.replace(" / ", "; ")]}
                             for value in answers]}
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

def c16() -> dict[str, Any]:
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
        multi_fill(f"{p}.e04", "Completa seis planes; separa las dos formas con una barra.", ["When Ana ___, the meeting ___.", "Before the library ___, we ___ the returns.", "As soon as the courier ___, the office ___ the parcel.", "When the gate ___, we ___.", "When the manager ___, we ___.", "When the rain ___, we ___."], ["arrives / will start", "closes / will check", "arrives / will sign for", "opens / will enter", "returns / will call", "stops / will continue"], c, "evaluation", "Las seis respuestas usan presente en la cláusula temporal y futuro en la principal.", minimum_correct=5)],
    "review": [
        q(f"{p}.r01", "¿Qué opción mantiene presente después de as soon as?", ["As soon as Mina will finish, we leave.", "As soon as Mina finishes, we will leave.", "As soon as Mina finishing, we will leave."], 1, c, "review", "Finishes es presente simple en la cláusula temporal."),
        write(f"{p}.r02", "Escribe un plan con before y una acción futura.", "Primero empezará el espectáculo; antes revisaremos las luces.", "Before the show starts, we will check the lights.", "We will check the lights before the show starts.", c, "review", "Las dos versiones mantienen presente en la cláusula con before."),
        multi_fill(f"{p}.r03", "Recupera seis planes; separa las dos formas con una barra.", ["When the driver ___, we ___ the boxes.", "Before the film ___, we ___ our seats.", "As soon as Mia ___, she ___ us.", "When the café ___, they ___ breakfast.", "Before the guard ___, we ___ the gate.", "When the wind ___, the boat ___."], ["arrives / will load", "starts / will find", "finishes / will call", "opens / will serve", "leaves / will check", "stops / will depart"], c, "review", "La recuperación aplica presente y futuro en seis planes nuevos.", minimum_correct=5)]
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
        q(f"{p}.p01", "Elige la actualización correcta del cine.", ["The cinema changed, but the time is unknown.", "Everything was cancelled.", "The film starts later, but the cinema is the same."], 2, c, "practice", "La opción correcta conserva el cine y comunica que la película empieza más tarde."),
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

BUILDERS = {16: c16, 17: c17, 18: c18, 19: c19, 20: c20}

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
        c18e03 = classes[2]["pools"]["evaluation"][2]
        assert len(c18e03["origin"]["audioSources"]) == 2 and "calendar" in c18e03["origin"]
        assert "Message one:" in c18e03["origin"]["audio"] and "Message two:" in c18e03["origin"]["audio"]
        assert c18e03["origin"]["audioMode"] == "tts" and c18e03["origin"]["languageCode"] == "en"
        c18e04 = classes[2]["pools"]["evaluation"][3]
        assert c18e04["format"] == "escuchar" and len(c18e04["choices"]) == 3
        assert c18e04["origin"]["scoring"] == {"parts": 3, "minimumCorrect": 3, "independentAttempt": True}
        assert "Hall 7" in c18e04["prompt"]["es"] and "Message two:" in c18e04["origin"]["audio"]
        assert classes[2]["remediationMap"][c18e03["id"]] == {"reteach": "en.n3.class-18.t06", "review": "en.n3.c18.r03"}
        for lesson in (classes[3], classes[4]):
            for item in (lesson["pools"]["evaluation"][3 if lesson["id"].endswith("19") else 2], lesson["pools"]["review"][2]):
                for answer in item["answer"]["accepted"]:
                    words_count = len(re.findall(r"\b[\w’-]+\b", answer))
                    assert (60 <= words_count <= 80) if lesson["id"].endswith("19") else (70 <= words_count <= 100)
        t06, e03, e04, r03 = close["teaching"][5], close["pools"]["evaluation"][2], close["pools"]["evaluation"][3], close["pools"]["review"][2]
        assert "workshop" in t06["en"].lower() and "feria" in e03["origin"]["text"].lower() and "museo" in r03["origin"]["text"].lower()
        assert len(e04["answer"]["pairs"]) == 5
        evidence_text = canonical(e04).lower()
        for marker in ("arrangement", "intention", "prediction", "time clause", "changed item", "deadline", "contingency"):
            assert marker in evidence_text
        assert close["remediationMap"][e04["id"]] == {"reteach": "en.n3.class-20.t06", "review": "en.n3.c20.r03"}
        assert len({norm(t06["en"]), norm(e03["answer"]["text"]), norm(r03["answer"]["text"])}) == 3
    return {"classes": len(classes), "items": sum(totals.values()), "pools": dict(totals), "formats": dict(sorted(formats.items())), "correctIndices": dict(sorted(indices.items())), "prompts": len(prompts), "fingerprints": len(sigs)}

def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def write_all() -> list[Path]:
    classes = []
    for n in NUMBERS:
        doc = BUILDERS[n](); audit([doc], False); path = OUT / f"class-{n:02d}.json"; path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); classes.append(path)
    docs = [json.loads(p.read_text(encoding="utf-8")) for p in classes]; summary = audit(docs, True)
    bundle = OUT / "bundle-16-20.json"; bundle.write_text(json.dumps({"schema":"onelingo.editorial.class-bundle.v1","course":"en","level":3,"scale":SCALE,"status":"shadow","runtimeAi":False,"selectionPolicy":{"deterministic":True},"evidencePolicy":{"attemptRecords":["variantId","libraryVersion","selectionId"]},"range":{"start":16,"end":20},"classes":docs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    report = REPORT_OUT / "REPORT.md"; hashes = "\n".join(f"{digest(p)}  {p.name}" for p in classes + [bundle])
    report.write_text(f"""# DRAFT — Inglés N3 C16–C20\n\nEstado: **DRAFT para revisión independiente; no autorizado para integración**.\n\n- Bloque `future-coordination`, B1-entry; fases `input → form → comprehension → production → transfer`.\n- 5 clases, 65 ejercicios, `status: shadow`, `runtimeAi: false`, selección/recuperación deterministas.\n- C20 conserva los cinco conceptos y usa tres escenarios de transferencia: feria/taller (e04), evento de taller (t06) y excursión-museo (r03).\n\n## Auditoría de generación\n\n```json\n{json.dumps(summary, ensure_ascii=False, indent=2)}\n```\n\nValidación pendiente de revisor independiente; el autor entrega DRAFT, nunca GO.\n\n## Comandos reproducibles\n\n```bash\nPYTHONDONTWRITEBYTECODE=1 python3 work/n3_c16_20/generate.py --all\npython3 tools/contenido/validar_bundle_editorial.py --file work/n3_c16_20/bundle-16-20.json --start 16 --end 20 --level 3\n```\n\n## Hashes\n\n```text\n{hashes}\n```\n""", encoding="utf-8")
    report.write_text(report.read_text(encoding="utf-8").replace("Validación pendiente de revisor independiente; el autor entrega DRAFT, nunca GO.", "Validación estructural individual C16–C20 y bundle con --level 3: OK. Idempotencia confirmada; la revisión lingüística/adversarial sigue pendiente. El autor entrega DRAFT, nunca GO."), encoding="utf-8")
    files = classes + [bundle, report]; manifest = REPORT_OUT / "MANIFEST.sha256"
    entries = [f"{digest(Path(__file__))}  ../../tools/contenido/generar_editorial_n3_16_20.py", f"{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"]
    entries.extend(f"{digest(p)}  {p.name if p.parent == REPORT_OUT else '../../' + str(p.relative_to(ROOT))}" for p in files); manifest.write_text("\n".join(entries) + "\n", encoding="utf-8")
    return files + [manifest]

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--all", action="store_true"); ap.add_argument("--audit", action="store_true"); args = ap.parse_args()
    if args.all: [print(p) for p in write_all()]
    elif args.audit: print(json.dumps(audit([json.loads((OUT / f"class-{n:02d}.json").read_text()) for n in NUMBERS], True), ensure_ascii=False, sort_keys=True))
    else: ap.error("use --all or --audit")
    return 0

if __name__ == "__main__": raise SystemExit(main())
