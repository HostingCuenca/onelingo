#!/usr/bin/env python3
"""Generate the integrated English N3 C56-C60 editorial shadow block."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n3"
REPORT_OUT = ROOT / "build/editorial-n3-56-60"
MAP_CANDIDATES = (
    ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json",
    Path("/home/roggrt/Documents/onelingo/assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"),
)
MAP = next((path for path in MAP_CANDIDATES if path.exists()), MAP_CANDIDATES[0])
NUMBERS = range(56, 61)
CONCEPTS = {n: f"n3-natural-collocations-{n - 55}" for n in NUMBERS}
PHASES = {56: "input", 57: "form", 58: "comprehension", 59: "production", 60: "transfer"}
SCALE = "client-10-levels-v1"
QUALITY = {
    "chronologyTokens": "enforce", "answerReuseAcrossEarlyReserved": "forbid",
    "answerEvidenceReuseAcrossPools": "forbid", "agentContract": "editorial-agent.v2",
    "minChoices": 3, "maxPromptCharacters": 90,
    "feedbackReuseWithinClass": "forbid", "minClassFormats": 4,
}


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def norm(value: Any) -> str:
    return " ".join(re.findall(r"[a-záéíóúüñ0-9']+", str(value).casefold()))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashed(item: dict[str, Any]) -> dict[str, Any]:
    payload = {k: v for k, v in item.items() if k not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return item


def base(item_id: str, fmt: str, prompt: str, concept: str, pool: str, feedback: str,
         *, requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": hint or "Relaciona el verbo de apoyo con el sustantivo completo."}
    return {
        "id": item_id, "format": fmt, "prompt": {"es": prompt},
        "answer": {}, "choices": [],
        "teaches": [concept] if pool == "practiceGuided" else [],
        "requires": [] if pool == "practiceGuided" else list(requires or [concept]),
        "origin": origin,
        "accessibility": {"screenReader": True, "highContrast": True, "largeText": True},
    }


def choose(item_id: str, prompt: str, options: list[str], index: int, concept: str,
           pool: str, feedback: str, **kwargs: Any) -> dict[str, Any]:
    item = base(item_id, "elegir", prompt, concept, pool, feedback, **kwargs)
    item["choices"] = [{"text": option} for option in options]
    item["answer"] = {"index": index}
    return hashed(item)


def listen(item_id: str, prompt: str, audio: str, options: list[str], index: int,
           concept: str, pool: str, feedback: str, **kwargs: Any) -> dict[str, Any]:
    item = base(item_id, "escuchar", prompt, concept, pool, feedback, **kwargs)
    item["choices"] = [{"text": option} for option in options]
    item["answer"] = {"index": index}
    item["origin"].update({
        "audio": audio, "audioMode": "tts", "languageCode": "en",
        "speedOptions": [0.75, 1.0], "maxReplays": 3,
        "revealTranscriptAfterAttempt": True,
    })
    return hashed(item)


def fill(item_id: str, prompt: str, answer: str, concept: str, pool: str,
         feedback: str, **kwargs: Any) -> dict[str, Any]:
    assert prompt.count("___") == 1
    item = base(item_id, "completar", prompt, concept, pool, feedback, **kwargs)
    item["answer"] = {"text": answer, "accepted": [answer]}
    return hashed(item)


def order(item_id: str, prompt: str, answer: str, concept: str, pool: str,
          feedback: str, **kwargs: Any) -> dict[str, Any]:
    item = base(item_id, "ordenar", prompt, concept, pool, feedback, **kwargs)
    item["answer"] = {"text": answer, "tokens": answer.split()}
    return hashed(item)


def match(item_id: str, prompt: str, pairs: list[tuple[str, str]], concept: str,
          pool: str, feedback: str, *, scoring: dict[str, Any] | None = None,
          **kwargs: Any) -> dict[str, Any]:
    item = base(item_id, "relacionar", prompt, concept, pool, feedback, **kwargs)
    values = [[left, {"es": right}] for left, right in pairs]
    assert len({right for _, right in pairs}) == len(pairs), "matchPairs needs unique right labels"
    item["answer"] = {"pairs": values}
    item["origin"]["pairs"] = values
    if scoring is not None:
        item["origin"]["scoring"] = scoring
    return hashed(item)


def write(item_id: str, prompt: str, stimulus: str, answer: str, alternative: str,
          concept: str, pool: str, feedback: str, **kwargs: Any) -> dict[str, Any]:
    item = base(item_id, "escribir", prompt, concept, pool, feedback, **kwargs)
    item["origin"]["text"] = stimulus
    item["answer"] = {"text": answer, "accepted": [answer, alternative]}
    return hashed(item)


def teaching(n: int, rows: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    result = []
    for index, (english, spanish, explanation) in enumerate(rows, 1):
        en_words, es_words = english.split(), spanish.split()
        en_mid, es_mid = max(1, len(en_words) // 2), max(1, len(es_words) // 2)
        result.append({
            "id": f"en.n3.class-{n:02d}.t{index:02d}", "en": english, "es": spanish,
            "explanationEs": explanation,
            "segments": [
                {"en": " ".join(en_words[:en_mid]), "es": " ".join(es_words[:es_mid])},
                {"en": " ".join(en_words[en_mid:]), "es": " ".join(es_words[es_mid:])},
            ],
            "audioText": english, "audioMode": "tts", "languageCode": "en",
            "patternId": CONCEPTS[n],
        })
    return result


def make_class(n: int, objectives: list[str], vocabulary: list[tuple[str, str]],
               rows: list[tuple[str, str, str]], pools: dict[str, list[dict[str, Any]]],
               remap: dict[str, tuple[str, str]], *, cumulative: bool = False) -> dict[str, Any]:
    specs = json.loads(MAP.read_text(encoding="utf-8"))["classes"]
    spec = next(entry for entry in specs if entry["id"] == f"en.n3.class-{n}")
    assert spec["phase"] == PHASES[n] and spec["concepts"] == [CONCEPTS[n]]
    assert spec["prerequisites"] == [f"en.n3.class-{n - 1:02d}"]
    all_concepts = [CONCEPTS[k] for k in NUMBERS]
    doc: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 3,
        "cefr": "B1", "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "phase": PHASES[n], "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY), "id": f"en.n3.class-{n:02d}",
        "title": spec["title"], "objectives": {"es": objectives},
        "concepts": [CONCEPTS[n]],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n3.class-{n - 1:02d}"],
        "usesVocabulary": [english for english, _ in vocabulary],
        "usesPatterns": all_concepts if cumulative else [CONCEPTS[n]],
        "vocabulary": [{"en": english, "es": spanish} for english, spanish in vocabulary],
        "teaching": teaching(n, rows), "pools": pools,
        "remediationMap": {
            item_id: {"reteach": reteach, "review": review}
            for item_id, (reteach, review) in remap.items()
        },
        "accessibility": {"highContrast": True, "largeText": True,
                          "screenReader": True, "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2,
                     "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if cumulative:
        doc["cumulativeEvaluation"] = all_concepts
    return doc


def build_56() -> dict[str, Any]:
    n, c, p = 56, CONCEPTS[56], "en.n3.c56"
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Completa la combinación: ___ a mistake.",
                   ["do", "take", "make"], 2, c, "practiceGuided",
                   "Make a mistake es la combinación natural para cometer un error.",
                   hint="Mistake suele acompañar a make."),
            fill(f"{p}.pg02", "Completa una rutina: I ___ breakfast at seven.",
                 "have", c, "practiceGuided", "Have breakfast nombra la comida habitual.",
                 hint="Para comidas, usa have."),
            order(f"{p}.pg03", "Ordena la combinación para descansar.",
                  "We take a break after lunch.", c, "practiceGuided",
                  "Take a break es la combinación fija para una pausa.",
                  hint="Coloca take antes de a break."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige la combinación usada.",
                   "Could you do me a favour and close the window?",
                   ["do a favour", "make a favour", "have a favour"], 0, c, "practice",
                   "Do a favour expresa ayudar a otra persona."),
            match(f"{p}.p02", "Relaciona cada situación con una combinación natural.",
                  [("wash the plates after dinner", "do the washing-up"),
                   ("use a camera at the concert", "take a photo"),
                   ("speak to a client by phone", "make a phone call")],
                  c, "practice", "Cada contexto activa una combinación frecuente distinta."),
            write(f"{p}.p03", "Escribe una frase natural sobre una cita médica.",
                  "Necesitas reservar una cita con el dentista para el martes.",
                  "I need to make an appointment with the dentist for Tuesday.",
                  "I must make an appointment to see the dentist on Tuesday.", c, "practice",
                  "Las variantes mantienen make an appointment y el martes indicado."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Elige la combinación natural para actividad física.",
                   ["make exercise", "do exercise", "have exercise"], 1, c, "evaluation",
                   "Do exercise es la opción natural para actividad física general."),
            listen(f"{p}.e02", "Escucha y selecciona la combinación exacta.",
                   "Please take a seat while the manager checks your form.",
                   ["have a seat", "make a seat", "take a seat"], 2, c, "evaluation",
                   "Take a seat es la invitación fija para sentarse."),
            choose(f"{p}.e03", "¿Qué combinación completa una experiencia agradable?",
                   ["have a good time", "do a good time", "make a good time"], 0, c,
                   "evaluation", "Have a good time describe disfrutar de una experiencia."),
            match(f"{p}.e04", "Clasifica doce situaciones con make, do, take o have.",
                  [("an error in an email", "make a mistake"),
                   ("reserve a time with a doctor", "make an appointment"),
                   ("contact the office by telephone", "make a phone call"),
                   ("clean plates after a meal", "do the washing-up"),
                   ("physical activity at home", "do exercise"),
                   ("help a neighbour with a box", "do a favour"),
                   ("stop work for ten minutes", "take a break"),
                   ("use a camera on holiday", "take a photo"),
                   ("sit down in the waiting room", "take a seat"),
                   ("eat the first meal of the day", "have breakfast"),
                   ("feel pain in your head", "have a headache"),
                   ("enjoy a party with friends", "have a good time")],
                  c, "evaluation", "Las doce relaciones muestran verbo de apoyo y sustantivo compatible.",
                  scoring={"parts": 12, "minimumCorrect": 10, "independentAttempt": True}),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué verbo completa ___ progress on the report?",
                   ["have", "make", "take"], 1, c, "review",
                   "Make progress es la combinación natural para avanzar."),
            order(f"{p}.r02", "Ordena una experiencia agradable nueva.",
                  "They have fun at the festival.", c, "review",
                  "Have fun recupera have para una experiencia agradable."),
            match(f"{p}.r03", "Recupera doce combinaciones en contextos nuevos.",
                  [("choose steps for next week", "make a plan"),
                   ("create an unwanted loud sound", "make a noise"),
                   ("move forward with the project", "make progress"),
                   ("complete school tasks at home", "do homework"),
                   ("clean and organise the home", "do housework"),
                   ("try as hard as possible", "do your best"),
                   ("travel on public transport", "take a bus"),
                   ("look briefly at the new design", "take a look"),
                   ("write information during a talk", "take notes"),
                   ("eat a midday meal", "have lunch"),
                   ("speak with a colleague about a problem", "have a conversation"),
                   ("face a difficulty with the printer", "have a problem")],
                  c, "review", "El repaso usa doce situaciones inéditas para recuperar los cuatro verbos.",
                  scoring={"parts": 12, "minimumCorrect": 10, "independentAttempt": True}),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-56.t02", f"{p}.r03"),
             f"{p}.e02": ("en.n3.class-56.t03", f"{p}.r03"),
             f"{p}.e03": ("en.n3.class-56.t04", f"{p}.r02"),
             f"{p}.e04": ("en.n3.class-56.t06", f"{p}.r03")}
    return make_class(n,
        ["Reconocer combinaciones frecuentes con make, do, take y have.",
         "Clasificar doce situaciones mediante su collocation natural."],
        [("make", "hacer/crear"), ("do", "hacer/realizar"), ("take", "tomar"),
         ("have", "tener/tomar"), ("mistake", "error"), ("break", "pausa"),
         ("appointment", "cita"), ("favour", "favor")],
        [("Use make for a result such as a mistake.",
          "Usa make para un resultado como un error.", "Make combina con resultados creados."),
         ("Use do for an activity such as exercise.",
          "Usa do para una actividad como ejercicio.", "Do suele acompañar tareas o actividades."),
         ("Use take for an action such as a break.",
          "Usa take para una acción como una pausa.", "Take forma expresiones fijas de acción."),
         ("Use have for an experience such as breakfast.",
          "Usa have para una experiencia como el desayuno.", "Have aparece con comidas y experiencias."),
         ("Learn each make, do, take or have combination, not one word alone.",
          "Aprende la combinación completa, no una palabra aislada.", "El sustantivo decide el verbo natural."),
         ("Classify twelve everyday situations by matching each noun meaning with its complete make, do, take or have combination. Ten accurate classifications show reliable recognition.",
          "Clasifica doce situaciones con la combinación completa de make, do, take o have.",
          "La evidencia requiere verbo de apoyo, sustantivo compatible y diez aciertos.")],
        pools, remap)


def build_57() -> dict[str, Any]:
    n, c, p = 57, CONCEPTS[57], "en.n3.c57"
    pools = {
        "practiceGuided": [
            fill(f"{p}.pg01", "Completa: We must ___ the deadline on Friday.",
                 "meet", c, "practiceGuided", "Meet the deadline significa terminar a tiempo.",
                 hint="Deadline combina con meet."),
            choose(f"{p}.pg02", "El equipo debe elegir hoy. ¿Qué combinación corresponde?",
                   ["take a decision", "do a decision", "make a decision"], 2,
                   c, "practiceGuided", "Make a decision expresa elegir una opción.",
                   hint="Decision combina con make."),
            order(f"{p}.pg03", "Ordena la instrucción para una conferencia.",
                  "Please take notes during the talk.", c, "practiceGuided",
                  "Take notes es la combinación natural para registrar información.",
                  hint="Coloca take delante de notes."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y selecciona la tarea académica.",
                   "Before writing the report, the students need to do research online.",
                   ["make research", "do research", "take research"], 1, c, "practice",
                   "Do research expresa investigar antes de escribir."),
            match(f"{p}.p02", "Relaciona cada necesidad con su combinación.",
                  [("finish by the agreed date", "meet a deadline"),
                   ("choose between two suppliers", "make a decision"),
                   ("record key points in class", "take notes")],
                  c, "practice", "Cada situación exige la collocation de trabajo o estudio adecuada."),
            write(f"{p}.p03", "Redacta un mensaje con do research en futuro.",
                  "Mina investigará precios mañana antes de la reunión.",
                  "Mina will do research on prices tomorrow before the meeting.",
                  "Tomorrow, Mina will do research into prices before the meeting.",
                  c, "practice", "Las variantes conservan futuro, investigación, precios y reunión."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Elige la collocation para acabar a tiempo.",
                   ["meet the deadline", "take the deadline", "make the deadline longer"],
                   0, c, "evaluation", "Meet the deadline comunica que el trabajo termina dentro del plazo."),
            listen(f"{p}.e02", "Escucha y elige la forma verbal completa.",
                   "Yesterday, the committee made a decision about the new schedule.",
                   ["makes a decision", "made a decision", "did a decision"], 1,
                   c, "evaluation", "Made a decision combina la collocation exacta con pasado."),
            choose(f"{p}.e03", "¿Qué mensaje usa take notes con el tiempo adecuado?",
                   ["She took notes during yesterday's interview.",
                    "She takes notes during yesterday's interview.",
                    "She did notes during yesterday's interview."], 0, c, "evaluation",
                   "Took notes mantiene la collocation y concuerda con yesterday."),
            match(f"{p}.e04", "Completa seis mensajes con collocation y tiempo adecuados.",
                  [("The report is due Friday; finish it on time.", "We must meet the deadline on Friday."),
                   ("The team chose the blue design yesterday.", "The team made a decision yesterday."),
                   ("Record the main points in tomorrow's lecture.", "Please take notes during tomorrow's lecture."),
                   ("They are investigating suppliers this week.", "They are doing research on suppliers this week."),
                   ("The client needs our choice now.", "We need to make a decision now."),
                   ("Sara finished before Tuesday's due time.", "Sara met the deadline by Tuesday.")],
                  c, "evaluation", "Los seis mensajes combinan forma exacta y tiempo verbal indicado.",
                  scoring={"parts": 6, "minimumCorrect": 5, "independentAttempt": True}),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué forma comunica una decisión ya tomada?",
                   ["take a decision yesterday", "made a decision yesterday",
                    "make a decision tomorrow"], 1, c, "review",
                   "Made a decision yesterday expresa una elección terminada."),
            order(f"{p}.r02", "Ordena un mensaje de investigación actual.",
                  "We are doing research on local transport.", c, "review",
                  "Are doing research mantiene la collocation en presente continuo."),
            match(f"{p}.r03", "Recupera seis mensajes de trabajo y estudio.",
                  [("The application is due Monday; finish before then.", "I will meet the deadline on Monday."),
                   ("Our group selected option C this morning.", "We made a decision this morning."),
                   ("Write the important details during Friday's call.", "Take notes during Friday's call."),
                   ("Leo investigated customer needs last week.", "Leo did research on customer needs last week."),
                   ("The manager wants our choice by noon.", "We must make a decision by noon."),
                   ("Nora submitted the essay before its due date.", "Nora met the essay deadline.")],
                  c, "review", "El repaso exige las mismas cuatro collocations en seis contextos nuevos.",
                  scoring={"parts": 6, "minimumCorrect": 5, "independentAttempt": True}),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-57.t01", f"{p}.r03"),
             f"{p}.e02": ("en.n3.class-57.t02", f"{p}.r01"),
             f"{p}.e03": ("en.n3.class-57.t03", f"{p}.r03"),
             f"{p}.e04": ("en.n3.class-57.t06", f"{p}.r03")}
    return make_class(n,
        ["Usar cuatro collocations frecuentes de trabajo y estudio.",
         "Completar seis mensajes con forma y tiempo adecuados."],
        [("deadline", "plazo"), ("decision", "decisión"), ("notes", "notas"),
         ("research", "investigación"), ("meet", "cumplir"), ("make", "tomar/hacer"),
         ("take", "tomar"), ("do", "hacer")],
        [("Meet a deadline means finish on time.",
          "Meet a deadline significa terminar a tiempo.", "Meet cambia de forma según el tiempo verbal."),
         ("Make a decision means choose an option.",
          "Make a decision significa elegir una opción.", "Made marca una decisión pasada."),
         ("Take notes means record important information.",
          "Take notes significa registrar información importante.", "Took es el pasado de take."),
         ("Do research means investigate a topic.",
          "Do research significa investigar un tema.", "Doing expresa una investigación en curso."),
         ("Keep the deadline, decision, notes or research collocation while changing the tense.",
          "Mantén la collocation al cambiar el tiempo verbal.", "El verbo se flexiona; el sustantivo se conserva."),
         ("Complete six work or study messages. Select the exact collocation and change its verb to match each time marker. Five accurate messages meet the target.",
          "Completa seis mensajes con la collocation y el tiempo verbal adecuados.",
          "La evidencia conjunta exige forma exacta, tiempo correcto y cinco aciertos." )],
        pools, remap)


def build_58() -> dict[str, Any]:
    n, c, p = 58, CONCEPTS[58], "en.n3.c58"
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Elige la corrección natural de take a decision.",
                   ["make a decision", "do a decision", "have a decision"], 0,
                   c, "practiceGuided", "Make a decision conserva la intención de elegir.",
                   hint="Decision combina con make."),
            listen(f"{p}.pg02", "Escucha y decide si la combinación es natural.",
                   "We need to meet the deadline by Thursday.",
                   ["Natural: finish on time", "Unnatural: use take", "Unnatural: use have"],
                   0, c, "practiceGuided", "Meet the deadline es natural y significa acabar a tiempo.",
                   hint="Meet se usa con deadline."),
            order(f"{p}.pg03", "Ordena la corrección para registrar información.",
                  "Please take notes during the interview.", c, "practiceGuided",
                  "Take notes corrige el calco do notes.",
                  hint="Notes combina con take."),
        ],
        "practice": [
            match(f"{p}.p01", "Relaciona tres mensajes con su corrección o confirmación.",
                  [("We made research before choosing.", "change to did research — investigated"),
                   ("She took a break after lunch.", "keep took a break — rested"),
                   ("They did progress this week.", "change to made progress — advanced")],
                  c, "practice", "Cada respuesta conserva la intención y corrige solo la combinación impropia."),
            choose(f"{p}.p02", "¿Qué mensaje suena natural en inglés?",
                   ["We did an appointment for Monday.", "We took an appointment for Monday.",
                    "We made an appointment for Monday."], 2, c, "practice",
                   "Made an appointment es la combinación natural para reservar una cita."),
            write(f"{p}.p03", "Corrige el calco sin cambiar su intención.",
                  "I did a phone call to confirm the booking.",
                  "I made a phone call to confirm the booking.",
                  "I made a call to confirm the booking.", c, "practice",
                  "Las variantes mantienen llamada y confirmación mediante make."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "¿Qué corrección conserva la intención de investigar?",
                   ["make a research", "do research", "take research"], 1, c,
                   "evaluation", "Do research expresa investigar sin alterar la intención."),
            listen(f"{p}.e02", "Escucha y selecciona la combinación impropia.",
                   "First, make a decision. Then, do research and take a deadline.",
                   ["make a decision", "do research", "take a deadline"], 2, c,
                   "evaluation", "Take a deadline es impropio; la forma natural es meet a deadline."),
            write(f"{p}.e03", "Corrige una combinación y justifica el cambio.",
                  "We must do notes during the client call.",
                  "Use take notes because the intention is to record information during the client call.",
                  "Change do notes to take notes; the message means recording information on the call.",
                  c, "evaluation", "La corrección nombra take notes y explica la intención de registrar datos."),
            match(f"{p}.e04", "Corrige tres de seis mensajes y justifica la intención.",
                  [("We need to take a decision today.", "change: make a decision — choose today"),
                   ("Please meet the deadline on Friday.", "keep: meet the deadline — finish by Friday"),
                   ("Mina will make research on prices.", "change: do research — investigate prices"),
                   ("The team made progress this week.", "keep: made progress — advanced this week"),
                   ("Leo did notes during the call.", "change: took notes — recorded call details"),
                   ("We had a meeting at noon.", "keep: had a meeting — met at noon")],
                  c, "evaluation", "Las seis relaciones identifican tres calcos, los corrigen y recuperan su intención."),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué forma significa registrar información?",
                   ["do notes", "have notes", "take notes"], 2,
                   c, "review", "Take notes conserva la intención de registrar información."),
            listen(f"{p}.r02", "Escucha y elige la corrección natural.",
                   "The draft is due Friday, so we must meet the deadline.",
                   ["meet the deadline", "take the deadline", "do the deadline"], 0,
                   c, "review", "Meet the deadline corrige el calco y conserva el viernes."),
            match(f"{p}.r03", "Recupera tres correcciones en seis mensajes nuevos.",
                  [("Sara made a mistake in the total.", "keep: made a mistake — produced an error"),
                   ("We must do a choice by noon.", "change: make a choice — choose by noon"),
                   ("They are taking research on users.", "change: doing research — investigating users"),
                   ("Please take a seat near the door.", "keep: take a seat — sit near the door"),
                   ("I made breakfast at the café at seven; I mean I ate there.",
                    "change: had breakfast — ate at the café at seven"),
                   ("Omar did his best in the test.", "keep: did his best — tried fully")],
                  c, "review", "La recuperación distingue tres mensajes naturales y corrige tres calcos nuevos."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-58.t02", f"{p}.r03"),
             f"{p}.e02": ("en.n3.class-58.t03", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-58.t04", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-58.t06", f"{p}.r03")}
    return make_class(n,
        ["Detectar combinaciones poco naturales y recuperar su intención.",
         "Corregir tres calcos dentro de seis mensajes."],
        [("natural", "habitual"), ("translated", "traducido literalmente"),
         ("intention", "intención"), ("correct", "corregir"),
         ("decision", "decisión"), ("research", "investigación"),
         ("notes", "notas"), ("deadline", "plazo")],
        [("A natural collocation sounds usual to English speakers.",
          "Una collocation natural suena habitual para hablantes de inglés.", "La combinación completa se aprende como unidad."),
         ("A translated combination may use the wrong support verb.",
          "Una combinación traducida puede usar el verbo de apoyo equivocado.", "El sustantivo ayuda a detectar el calco."),
         ("Meet a deadline means finish by the required time.",
          "Meet a deadline significa terminar dentro del plazo.", "Take a deadline no conserva la forma natural."),
         ("Correct do notes to take notes without changing the intention.",
          "Corrige do notes a take notes sin cambiar la intención.", "El mensaje todavía significa registrar información."),
         ("Explain why you correct each combination and which intention it preserves.",
          "Explica cada corrección con el significado que conserva.", "La justificación demuestra comprensión, no solo memoria."),
         ("Read six messages. Keep the three natural collocations, correct the three translated combinations, and state the intention preserved by every correction.",
          "Lee seis mensajes, conserva tres combinaciones naturales y corrige tres calcos.",
          "La tarea integrada exige intención entendida, forma natural y tres justificaciones.")],
        pools, remap)


def build_59() -> dict[str, Any]:
    n, c, p = 59, CONCEPTS[59], "en.n3.c59"
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "¿Qué edición mejora do a decision?",
                   ["make a decision", "take a decision note", "have a decision"], 0,
                   c, "practiceGuided", "Make a decision corrige la combinación y conserva elegir.",
                   hint="Decision combina con make."),
            fill(f"{p}.pg02", "Completa la edición: Please ___ notes during the call.",
                 "take", c, "practiceGuided", "Take notes es apropiado para una nota de trabajo.",
                 hint="Usa el verbo natural antes de notes."),
            order(f"{p}.pg03", "Ordena una petición clara y profesional.",
                  "Please do research before Thursday's meeting.", c, "practiceGuided",
                  "Do research mantiene un registro directo y profesional.",
                  hint="Sitúa la acción antes del plazo."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada edición con el significado conservado.",
                  [("make progress", "advance with the work"),
                   ("meet the deadline", "finish on time"),
                   ("take a break", "stop briefly to rest")],
                  c, "practice", "Cada mejora mantiene el significado original con una forma natural."),
            listen(f"{p}.p02", "Escucha y elige la edición más apropiada.",
                   "Original note: We need to make research before choosing a supplier.",
                   ["We need to take research before choosing.",
                    "We need to do research before choosing a supplier.",
                    "We need to have a research supplier."], 1, c, "practice",
                   "Do research corrige la combinación y conserva la selección del proveedor."),
            write(f"{p}.p03", "Edita dos collocations sin cambiar los datos.",
                  "Please do a plan today and make notes in the 4 pm meeting.",
                  "Please make a plan today and take notes in the 4 pm meeting.",
                  "Today, please make a plan and take notes during the meeting at four.",
                  c, "practice", "Las variantes conservan hoy, la reunión de las cuatro y ambas acciones."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Se debe decidir antes de mediodía. Elige la edición fiel.",
                   ["Please do a decision by noon.", "Please make a decision tomorrow.",
                    "Please make a decision by noon."], 2, c, "evaluation",
                   "Please make a decision by noon es natural, preciso y cortés."),
            listen(f"{p}.e02", "Escucha y selecciona la mejora exacta.",
                   "The note says, We made progress and then took a short break.",
                   ["made progress / took a break", "did progress / made a break",
                    "had progress / did a break"], 0, c, "evaluation",
                   "Made progress y took a break son las dos combinaciones naturales."),
            write(f"{p}.e03", "Corrige una nota breve y conserva su plazo.",
                  "We must take a deadline and finish the draft by Friday.",
                  "We must meet the deadline and finish the draft by Friday.",
                  "To meet the deadline, we must finish the draft by Friday.",
                  c, "evaluation", "Las respuestas corrigen meet the deadline y mantienen Friday."),
            write(f"{p}.e04", "Edita en 70–90 palabras una nota con cuatro collocations impropias.",
                  "Equipo de proyecto. Datos: decidir el proveedor hoy; Marta investiga precios antes del martes y comparte resultados; Leo registra notas en la llamada con el cliente del miércoles; avanzar con el borrador antes del plazo del viernes. Original: do a decision, make research, do notes, do progress.",
                  "Team, we need to make a decision about the supplier today. Marta will do research on prices before Tuesday and share the results with everyone. Leo will take notes during Wednesday's client call, so no detail is lost. We must also make progress on the draft before Friday's deadline. Please keep these tasks and dates unchanged when you update the plan. This edited note uses natural collocations while preserving every person, action and deadline from the original message.",
                  "Please make a decision on the supplier today. Before Tuesday, Marta will do research on prices and send the findings to the team. Leo will take notes in the client call on Wednesday to keep its details clear. The group must make progress on the draft before the Friday deadline. These four edits replace the literal combinations but retain the same responsibilities, sequence and dates. Please use this version as the clear project update for everyone.",
                  c, "evaluation", "Las versiones corrigen cuatro collocations y conservan personas, acciones y plazos."),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué oración corrige make a deadline?",
                   ["The group will take its deadline on Monday.",
                    "The group will meet its deadline on Monday.",
                    "The group will do its deadline on Monday."], 1,
                   c, "review", "Will meet its deadline expresa cumplir el plazo del lunes."),
            order(f"{p}.r02", "Ordena dos collocations naturales después del trabajo.",
                  "The team made progress and took a short break.", c, "review",
                  "Made progress y took a short break corrigen las dos combinaciones."),
            write(f"{p}.r03", "Recupera en 70–90 palabras cuatro ediciones nuevas.",
                  "Equipo médico. Datos: decidir turno hoy; Ana investiga proveedores el lunes y comparte opciones; Joel descansa a las 2; Iris reserva y confirma cita para el jueves. Original: take a decision, make research, make a break, do an appointment.",
                  "Team, we need to make a decision about the new shift today. Ana will do research on suppliers on Monday and report the options. Joel should take a break at two, as the schedule already states. Iris must make an appointment for Thursday and confirm it with the clinic. These four corrected collocations preserve the original people, dates and actions. Please send this edited note to the medical team so everyone follows the same clear and professional plan.",
                  "Please make a decision on the new shift today. On Monday, Ana will do research on suppliers and share the options. Joel will take a break at two according to the schedule. Iris will make an appointment for Thursday and confirm it with the clinic. The four natural collocations replace the literal versions without changing any responsibility, date or action. This concise version is appropriate for the medical team and keeps the coordination message easy to follow.",
                  c, "review", "La recuperación corrige cuatro calcos nuevos y conserva todos los datos del equipo."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-59.t02", f"{p}.r03"),
             f"{p}.e02": ("en.n3.class-59.t05", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-59.t06", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-59.t06", f"{p}.r03")}
    return make_class(n,
        ["Editar cuatro collocations impropias sin cambiar el mensaje.",
         "Producir una nota natural de 70–90 palabras y registro apropiado."],
        [("edit", "editar"), ("improve", "mejorar"), ("meaning", "significado"),
         ("register", "registro"), ("decision", "decisión"), ("research", "investigación"),
         ("notes", "notas"), ("progress", "progreso")],
        [("Edit the collocation, not the message meaning or facts.",
          "Edita la collocation, no los datos del mensaje.", "Personas, acciones y fechas se mantienen."),
         ("Improve do a decision to make a decision.",
          "Mejora do a decision a make a decision.", "La elección conserva su significado."),
         ("Improve make research to do research.",
          "Mejora make research a do research.", "La acción de investigar no cambia."),
         ("Improve do notes to take notes.",
          "Mejora do notes a take notes.", "La acción sigue siendo registrar información."),
         ("Use make progress and take a break in an appropriate register.",
          "Usa make progress y take a break en un registro apropiado.", "Las dos combinaciones mejoran una actualización de trabajo."),
         ("Team, please make a choice about the route today. Nia will do research on train prices by Monday, and Omar will take notes during Tuesday's planning call. We must meet the booking deadline on Wednesday. These four edits preserve the original people, actions and dates while removing the literal combinations do a choice, take research, make notes and make a deadline. Please use this clear version when you update the travel group.",
          "El modelo corrige cuatro collocations en una nota de viaje sin alterar datos.",
          "La producción demuestra cuatro mejoras, significado conservado y registro apropiado.")],
        pools, remap)


def build_60() -> dict[str, Any]:
    n, c, p = 60, CONCEPTS[60], "en.n3.c60"
    all_concepts = [CONCEPTS[k] for k in NUMBERS]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "¿Qué combinación comunica una elección del grupo?",
                   ["do a decision", "make a decision", "have a decision"], 1,
                   c, "practiceGuided", "Make a decision expresa la elección que debe cerrar el grupo.",
                   hint="Decision combina con make."),
            fill(f"{p}.pg02", "Completa el seguimiento: Please ___ notes in the call.",
                 "take", c, "practiceGuided", "Take notes registra la información necesaria para el seguimiento.",
                 hint="Notes combina con take."),
            order(f"{p}.pg03", "Ordena una instrucción con plazo.",
                  "We must meet the deadline on Friday.", c, "practiceGuided",
                  "Meet the deadline fija claramente el plazo del equipo.",
                  hint="Coloca meet antes de the deadline."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada necesidad con una collocation meta.",
                  [("choose the final design", "make a decision"),
                   ("investigate material prices", "do research"),
                   ("record details in the meeting", "take notes"),
                   ("finish by Friday", "meet the deadline")],
                  c, "practice", "Las cuatro relaciones preparan decisión, investigación, notas y plazo."),
            listen(f"{p}.p02", "Escucha y selecciona la acción de seguimiento.",
                   "After the meeting, Sara will send the notes to the whole group.",
                   ["Choose the venue", "Research the prices", "Send the notes"], 2,
                   c, "practice", "Send the notes es el seguimiento explícito después de la reunión."),
            write(f"{p}.p03", "Redacta una coordinación breve con dos collocations.",
                  "Hoy: decidir proveedor. Mañana: Luis investiga precios.",
                  "We will make a decision about the supplier today. Luis will do research on prices tomorrow.",
                  "Today we will make the supplier decision; tomorrow Luis will do research on prices.",
                  c, "practice", "Las variantes conservan responsable, días y dos combinaciones naturales."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "¿Qué mensaje expresa una coordinación natural?",
                   ["We do a decision and take a deadline.",
                    "We make research and do notes.",
                    "We make a decision and meet the deadline."], 2, c, "evaluation",
                   "Make a decision y meet the deadline son combinaciones naturales y operativas."),
            listen(f"{p}.e02", "Escucha y elige el dato de investigación.",
                   "Arun will do research on printing costs by Wednesday.",
                   ["Arun investigates printing costs by Wednesday",
                    "Bia records meeting details on Thursday",
                    "Clara sends the follow-up on Friday"], 0, c, "evaluation",
                   "La primera opción conserva responsable, investigación y miércoles."),
            write(f"{p}.e03", "Corrige dos calcos en el aviso sin cambiar el lunes.",
                  "We must take research and make notes before Monday.",
                  "We must do research and take notes before Monday.",
                  "Before Monday, we must do research and take notes.",
                  c, "evaluation", "Las respuestas corrigen research y notes y conservan Monday."),
            write(f"{p}.e04", "Resuelve en 80–110 palabras la coordinación de una exposición.",
                  "Exposición comunitaria: decidir diseño hoy; Arun investiga costes de impresión antes del miércoles y comparte cifras; Bia toma notas en reunión del jueves; propuesta final vence viernes a las 15:00; Clara envía seguimiento con notas y diseño después. Borrador literal: do a decision, make research, do notes, take the deadline.",
                  "Team, we need to make a decision about the exhibition layout today. Arun will do research on printing costs before Wednesday and share the figures. Bia will take notes during Thursday's meeting so every change is recorded. We must meet the final proposal deadline at three on Friday. After the meeting, Clara will send a follow-up message with Bia's notes and the chosen layout. Please keep these responsibilities and times unchanged. This clear plan covers the decision, research, notes, deadline and required follow-up for the community exhibition.",
                  "Please make a decision on the exhibition layout today. Before Wednesday, Arun will do research on printing costs and report the figures. Bia will take notes at the Thursday meeting to record each change. The group must meet the proposal deadline at three on Friday. Clara will send the follow-up after the meeting, including the notes and final layout. This concise coordination message keeps every person, action and time from the brief while using the four target collocations naturally and clearly.",
                  c, "evaluation", "Las variantes integran cuatro collocations y todos los datos de coordinación.",
                  requires=all_concepts),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué opción contiene investigación y notas naturales?",
                   ["make research / do notes", "take research / make notes",
                    "do research / take notes"], 2, c, "review",
                   "Do research y take notes son las combinaciones naturales requeridas."),
            listen(f"{p}.r02", "Escucha y recupera responsable, tarea y plazo.",
                   "Priya will do research on venue costs before Thursday.",
                   ["Priya records venue notes on Friday",
                    "Priya researches venue costs before Thursday",
                    "Arun researches printing costs before Wednesday"], 1,
                   c, "review",
                   "La opción correcta conserva a Priya, los costes del lugar y el jueves."),
            write(f"{p}.r03", "Recupera en 80–110 palabras una coordinación de estudio.",
                  "Proyecto de estudio: decidir tema el lunes; Mei investiga fuentes el martes y comparte lista; Jon toma notas en entrevista del miércoles; borrador vence viernes al mediodía; Sara sube archivo y envía seguimiento con enlace después. Borrador literal: take a decision, make research, make notes, do the deadline.",
                  "Study group, we will make a decision about the project topic on Monday. Mei will do research on suitable sources on Tuesday and share her list. Jon will take notes during Wednesday's interview so the evidence is recorded. We must meet the draft deadline at noon on Friday. After the draft is complete, Sara will upload the file and send a follow-up message with the link. This plan keeps every responsibility, day and action clear while using the four target collocations naturally in one concise update.",
                  "Please make a decision on the study topic on Monday. On Tuesday, Mei will do research on sources and share the list. Jon will take notes in Wednesday's interview to preserve its evidence. The team must meet the draft deadline at noon on Friday. Sara will then upload the file and send the follow-up with its link. This concise message includes all people, dates and actions from the brief, and it uses decision, research, notes and deadline collocations naturally for clear coordination.",
                  c, "review", "La recuperación demuestra los cinco conceptos en un escenario de estudio distinto.",
                  requires=all_concepts),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-60.t06", f"{p}.r03"),
             f"{p}.e02": ("en.n3.class-60.t03", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-60.t03", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-60.t06", f"{p}.r03")}
    return make_class(n,
        ["Resolver una coordinación sin calcos literales.",
         "Integrar decisión, investigación, notas, plazo y seguimiento en 80–110 palabras."],
        [("coordinate", "coordinar"), ("decision", "decisión"),
         ("research", "investigación"), ("notes", "notas"),
         ("deadline", "plazo"), ("follow-up", "seguimiento"),
         ("concise", "conciso"), ("complete", "completo")],
        [("Coordinate by naming every person, action and time.",
          "Coordina nombrando cada persona, acción y momento.", "La información completa evita suposiciones."),
         ("Make a decision records the group's choice.",
          "Make a decision registra la elección del grupo.", "La collocation sustituye el calco do a decision."),
         ("Do research and take notes support the next action.",
          "Do research y take notes apoyan la siguiente acción.", "Investigación y notas deben tener responsables."),
         ("Meet the deadline states when the work must finish.",
          "Meet the deadline indica cuándo debe terminar el trabajo.", "El plazo se conserva de forma exacta."),
         ("A concise follow-up confirms what happens next.",
          "Un seguimiento conciso confirma qué ocurre después.", "El cierre asigna una acción concreta."),
         ("The workshop draft used do a decision, take research, make notes and make a deadline. Here is the edited message. Team, please make a decision about the venue today. Nia will do research on transport costs by Monday. Leo will take notes during Tuesday's planning call. We must meet the booking deadline on Friday. After the call, Sam will send a follow-up email with Leo's notes and the selected venue. This concise version keeps every person, action and time, corrects all four literal combinations and gives the workshop team a complete plan.",
          "El modelo coordina un taller con decisión, investigación, notas, plazo y seguimiento.",
          "El escenario demuestra los cinco conceptos mediante cuatro collocations y datos completos." )],
        pools, remap, cumulative=True)


BUILDERS = {56: build_56, 57: build_57, 58: build_58, 59: build_59, 60: build_60}


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’-]+\b", text))


def get_item(cls: dict[str, Any], pool: str, suffix: str) -> dict[str, Any]:
    return next(item for item in cls["pools"][pool] if item["id"].endswith(suffix))


def audit(classes: list[dict[str, Any]], full: bool) -> dict[str, Any]:
    totals: Counter[str] = Counter()
    formats: Counter[str] = Counter()
    indices: Counter[int] = Counter()
    prompts: dict[str, str] = {}
    signatures: dict[str, str] = {}
    allowed_formats = {"elegir", "escuchar", "completar", "ordenar", "relacionar", "escribir"}
    for cls in classes:
        number = int(cls["id"].split("-")[-1])
        assert cls["status"] == "shadow" and cls["runtimeAi"] is False
        assert cls["phase"] == PHASES[number] and cls["qualityPolicy"] == QUALITY
        assert 6 <= len(cls["vocabulary"]) <= 12 and 4 <= len(cls["teaching"]) <= 6
        local_formats: set[str] = set()
        local_indices: Counter[int] = Counter()
        feedbacks: list[str] = []
        for pool, expected in (("practiceGuided", 3), ("practice", 3),
                               ("evaluation", 4), ("review", 3)):
            assert len(cls["pools"][pool]) == expected
            totals[pool] += expected
            for item in cls["pools"][pool]:
                assert item["format"] in allowed_formats
                assert len(item["prompt"]["es"]) <= 90, (item["id"], len(item["prompt"]["es"]))
                payload = {k: v for k, v in item.items() if k not in {"id", "contentHash"}}
                assert item["contentHash"] == "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
                prompt_key = norm(item["prompt"]["es"])
                assert prompt_key not in prompts, (item["id"], prompts.get(prompt_key))
                prompts[prompt_key] = item["id"]
                feedbacks.append(item["origin"]["feedback"]["es"])
                local_formats.add(item["format"])
                formats[item["format"]] += 1
                scoring = item["origin"].get("scoring")
                if scoring is not None:
                    assert item["format"] == "relacionar"
                    assert scoring["parts"] == len(item["answer"]["pairs"])
                    assert 1 <= scoring["minimumCorrect"] <= scoring["parts"]
                if pool != "practiceGuided":
                    assert "hint" not in item["origin"]
                if item["format"] in {"elegir", "escuchar"}:
                    assert len(item["choices"]) >= 3
                    index = item["answer"]["index"]
                    assert 0 <= index < len(item["choices"])
                    indices[index] += 1
                    local_indices[index] += 1
                if item["format"] == "completar":
                    assert item["prompt"]["es"].count("___") == 1
                    assert len(item["answer"]["accepted"]) == 1
                if item["format"] == "relacionar":
                    assert "audio" not in item["origin"]
                    pairs = item["answer"]["pairs"]
                    rights = [pair[1]["es"] for pair in pairs]
                    assert len(rights) == len(set(rights))
                if item["format"] == "escribir":
                    accepted = item["answer"]["accepted"]
                    assert len(accepted) >= 2 and len({norm(text) for text in accepted}) >= 2
                stimulus = (item["origin"].get("audio") or item["origin"].get("text") or
                            item["origin"].get("pairs") or item["prompt"]["es"])
                signature = canonical({"stimulus": stimulus, "answer": item["answer"]}).casefold()
                assert signature not in signatures, (item["id"], signatures.get(signature))
                signatures[signature] = item["id"]
        assert len(local_formats) >= 4
        assert len(feedbacks) == len(set(feedbacks))
        assert len(local_indices) >= 2 and max(local_indices.values()) / sum(local_indices.values()) <= 0.60
        visible = canonical({"teaching": cls["teaching"], "pools": cls["pools"]}).casefold()
        for entry in cls["vocabulary"]:
            assert entry["en"].casefold() in visible, (cls["id"], entry["en"])
        eval_ids = {item["id"] for item in cls["pools"]["evaluation"]}
        assert set(cls["remediationMap"]) == eval_ids
        teaching_ids = {item["id"] for item in cls["teaching"]}
        review_ids = {item["id"] for item in cls["pools"]["review"]}
        for route in cls["remediationMap"].values():
            assert route["reteach"] in teaching_ids and route["review"] in review_ids
        reserved_formats = {item["format"] for pool in ("evaluation", "review")
                            for item in cls["pools"][pool]}
        assert "escuchar" in reserved_formats and "escribir" in local_formats

    if full:
        assert len(classes) == 5 and sum(totals.values()) == 65
        c56, c57, c58, c59, c60 = classes
        c56e04 = get_item(c56, "evaluation", ".e04")
        c56r03 = get_item(c56, "review", ".r03")
        assert len(c56e04["answer"]["pairs"]) == 12
        assert len(c56r03["answer"]["pairs"]) == 12
        for item in (c56e04, c56r03):
            assert item["origin"]["scoring"] == {
                "parts": 12, "minimumCorrect": 10, "independentAttempt": True,
            }
            rights = [pair[1]["es"] for pair in item["answer"]["pairs"]]
            assert sum(text.startswith("make ") for text in rights) == 3
            assert sum(text.startswith("do ") for text in rights) == 3
            assert sum(text.startswith("take ") for text in rights) == 3
            assert sum(text.startswith("have ") for text in rights) == 3

        for item in (get_item(c57, "evaluation", ".e04"),
                     get_item(c57, "review", ".r03")):
            assert len(item["answer"]["pairs"]) == 6
            assert item["origin"]["scoring"] == {
                "parts": 6, "minimumCorrect": 5, "independentAttempt": True,
            }
            evidence = canonical(item["answer"]).casefold()
            for phrase in ("meet the deadline", "decision", "notes", "research"):
                assert phrase in evidence

        for item in (get_item(c58, "evaluation", ".e04"),
                     get_item(c58, "review", ".r03")):
            assert len(item["answer"]["pairs"]) == 6
            rights = [pair[1]["es"] for pair in item["answer"]["pairs"]]
            assert sum(text.startswith("change:") for text in rights) == 3
            assert sum(text.startswith("keep:") for text in rights) == 3
            assert all(" — " in text for text in rights)
        assert "i mean i ate there" in canonical(get_item(c58, "review", ".r03")).casefold()

        for text in (c59["teaching"][-1]["en"],
                     *get_item(c59, "evaluation", ".e04")["answer"]["accepted"],
                     *get_item(c59, "review", ".r03")["answer"]["accepted"]):
            assert 70 <= word_count(text) <= 90, word_count(text)
        for item in (get_item(c59, "evaluation", ".e04"),
                     get_item(c59, "review", ".r03")):
            evidence = canonical(item["answer"]).casefold()
            assert sum(phrase in evidence for phrase in (
                "make a decision", "do research", "take notes", "make progress",
                "take a break", "make an appointment")) >= 4
        c59_source = get_item(c59, "evaluation", ".e04")["origin"]["text"].casefold()
        assert "proveedor" in c59_source and "cliente" in c59_source

        all_concepts = [CONCEPTS[n] for n in NUMBERS]
        assert c60["usesPatterns"] == all_concepts
        assert c60["cumulativeEvaluation"] == all_concepts
        e04 = get_item(c60, "evaluation", ".e04")
        r03 = get_item(c60, "review", ".r03")
        assert e04["requires"] == all_concepts and r03["requires"] == all_concepts
        assert "draft used" in c60["teaching"][-1]["en"].casefold()
        for item in (e04, r03):
            source = item["origin"]["text"].casefold()
            assert "borrador literal" in source
            assert source.count(",") >= 3
        closure_texts = [c60["teaching"][-1]["en"], *e04["answer"]["accepted"],
                         *r03["answer"]["accepted"]]
        for text in closure_texts:
            lower = text.casefold()
            assert 80 <= word_count(text) <= 110, word_count(text)
            for phrase in ("make a decision", "do research", "take notes", "meet the"):
                assert phrase in lower, (phrase, text)
            assert "follow-up" in lower
        joined = " ".join(closure_texts).casefold()
        assert all(marker in joined for marker in ("workshop", "exhibition", "study"))
        assert len({norm(c60["teaching"][-1]["en"]), norm(e04["answer"]["text"]),
                    norm(r03["answer"]["text"])}) == 3
        assert c56["remediationMap"]["en.n3.c56.e03"]["review"] == "en.n3.c56.r02"
        assert c60["remediationMap"]["en.n3.c60.e02"]["review"] == "en.n3.c60.r02"
    return {
        "classes": len(classes), "items": sum(totals.values()), "pools": dict(totals),
        "formats": dict(sorted(formats.items())), "correctIndices": dict(sorted(indices.items())),
        "prompts": len(prompts), "fingerprints": len(signatures),
    }


def verify_in_memory() -> dict[str, Any]:
    first = [BUILDERS[n]() for n in NUMBERS]
    second = [BUILDERS[n]() for n in NUMBERS]
    assert canonical(first) == canonical(second), "non-deterministic in-memory generation"
    return audit(first, True)


def write_class(n: int) -> Path:
    doc = BUILDERS[n]()
    audit([doc], False)
    path = OUT / f"class-{n:02d}.json"
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_bundle() -> tuple[Path, dict[str, Any]]:
    classes = [json.loads((OUT / f"class-{n:02d}.json").read_text(encoding="utf-8"))
               for n in NUMBERS]
    summary = audit(classes, True)
    bundle = {
        "schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 3,
        "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "range": {"start": 56, "end": 60}, "classes": classes,
    }
    path = OUT / "bundle-56-60.json"
    path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path, summary


def write_report(paths: list[Path], summary: dict[str, Any]) -> Path:
    hashes = "\n".join(f"{digest(path)}  {path.name}" for path in paths)
    text = f"""# INTEGRADO — Inglés N3 C56–C60

Estado: **integrado en shadow tras revisión independiente GO**.

## Cobertura

- Bloque `natural-collocations`, fases `input → form → comprehension → production → transfer`.
- Cinco clases, 65 ejercicios, `editorial-agent.v2`, `shadow` y `runtimeAi: false`.
- C56 materializa doce clasificaciones; C57 seis mensajes; C58 seis mensajes y tres correcciones.
- C59 mantiene 70–90 palabras y C60 mantiene 80–110 en enseñanza, evaluación y recuperación.
- C60 usa tres escenarios distintos: taller, exposición comunitaria y proyecto de estudio.

## Compatibilidad del reproductor

Las tareas compuestas usan `relacionar`, el único formato cuyo reproductor consume
`origin.scoring.parts` y `minimumCorrect`. C56 e04/r03 aplican 10/12 y C57 e04/r03
aplican 5/6; las aserciones verifican tanto el formato como los contadores efectivos.

## Auditoría interna

```json
{json.dumps(summary, ensure_ascii=False, indent=2)}
```

El generador construye dos veces en memoria, compara la forma canónica y ejecuta aserciones
de conteos, formatos, evidencia, rangos y cierre acumulativo antes de escribir.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/contenido/generar_editorial_n3_56_60.py --all
for n in 56 57 58 59 60; do python3 tools/contenido/validar_bundle_editorial.py --file assets/contenido/en/editorial/n3/class-$n.json --start $n --end $n --level 3; done
python3 tools/contenido/validar_bundle_editorial.py --file assets/contenido/en/editorial/n3/bundle-56-60.json --start 56 --end 60 --level 3
```

## Hashes

```text
{hashes}
```

Revisión independiente: `GO`; integración únicamente en `shadow`.
"""
    path = REPORT_OUT / "REPORT.md"
    path.write_text(text, encoding="utf-8")
    return path


def write_all() -> list[Path]:
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    memory_summary = verify_in_memory()
    class_paths = [write_class(n) for n in NUMBERS]
    bundle, summary = write_bundle()
    assert summary == memory_summary
    report = write_report(class_paths + [bundle], summary)
    files = class_paths + [bundle, report]
    manifest = REPORT_OUT / "MANIFEST.sha256"
    entries = [
        f"{digest(Path(__file__))}  ../../tools/contenido/generar_editorial_n3_56_60.py",
        f"{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json",
    ]
    entries.extend(f"{digest(path)}  ../../{path.relative_to(ROOT)}" for path in class_paths + [bundle])
    entries.append(f"{digest(report)}  REPORT.md")
    manifest.write_text("\n".join(entries) + "\n", encoding="utf-8")
    return files + [manifest]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-number", type=int, choices=NUMBERS)
    parser.add_argument("--bundle", action="store_true")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if args.class_number:
        print(write_class(args.class_number))
    elif args.bundle:
        print(write_bundle()[0])
    elif args.audit:
        docs = [json.loads((OUT / f"class-{n:02d}.json").read_text(encoding="utf-8"))
                for n in NUMBERS]
        print(json.dumps(audit(docs, True), ensure_ascii=False, sort_keys=True))
    elif args.all:
        for path in write_all():
            print(path)
    else:
        parser.error("choose --class-number, --bundle, --audit or --all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

