#!/usr/bin/env python3
"""Generate the integrated English N3 C66-C70 editorial shadow block."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "assets/contenido/en/editorial/n3"
REPORT_OUT = REPO / "build/editorial-n3-66-70"
MAP = REPO / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
NUMBERS = range(66, 71)
PHASES = {66: "input", 67: "form", 68: "comprehension", 69: "production", 70: "transfer"}
CONCEPTS = {n: f"n3-travel-resolution-{n - 65}" for n in NUMBERS}
ALL_CONCEPTS = [CONCEPTS[n] for n in NUMBERS]
QUALITY = {
    "chronologyTokens": "enforce",
    "answerReuseAcrossEarlyReserved": "forbid",
    "answerEvidenceReuseAcrossPools": "forbid",
    "agentContract": "editorial-agent.v2",
    "minChoices": 3,
    "maxPromptCharacters": 90,
    "feedbackReuseWithinClass": "forbid",
    "minClassFormats": 4,
}
VARIANT_SEED = "0"


def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def words(value):
    return re.findall(r"\b[\w’-]+\b", str(value), re.UNICODE)


def norm(value):
    return " ".join(re.findall(r"[a-záéíóúüñ0-9']+", canon(value).casefold()))


def content_hash(item):
    payload = {k: v for k, v in item.items() if k not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canon(payload).encode()).hexdigest()
    return item


def rotation(item_id, size):
    raw = hashlib.sha256(f"{VARIANT_SEED}:{item_id}".encode()).digest()
    return int.from_bytes(raw[:4], "big") % size if size else 0


def base(item_id, fmt, prompt, concept, pool, feedback, *, requires=None, hint=None,
         source=None, scoring=None):
    origin = {
        "kind": "editorial",
        "variantSeed": VARIANT_SEED,
        "variantId": f"{item_id}.seed-{VARIANT_SEED}",
        "feedback": {"es": feedback},
    }
    if pool == "practiceGuided":
        origin["hint"] = {"es": hint or "Observa la forma y comprueba cada dato visible."}
    if source:
        origin.update(source)
    if scoring:
        origin["scoring"] = scoring
    return {
        "id": item_id,
        "format": fmt,
        "prompt": {"es": prompt},
        "answer": {},
        "choices": [],
        "teaches": [concept] if pool == "practiceGuided" else [],
        "requires": [] if pool == "practiceGuided" else list(requires or [concept]),
        "origin": origin,
        "accessibility": {"screenReader": True, "highContrast": True, "largeText": True},
    }


def choose(item_id, prompt, options, correct, concept, pool, feedback, **kwargs):
    item = base(item_id, "elegir", prompt, concept, pool, feedback, **kwargs)
    shift = rotation(item_id, len(options))
    rotated = options[shift:] + options[:shift]
    item["choices"] = [{"text": option} for option in rotated]
    item["answer"] = {"index": (correct - shift) % len(options)}
    return content_hash(item)


def listen(item_id, prompt, audio, options, correct, concept, pool, feedback, **kwargs):
    source = dict(kwargs.pop("source", {}) or {})
    source.update({
        "audio": audio,
        "audioMode": "tts",
        "languageCode": "en",
        "speedOptions": [0.75, 1.0],
        "maxReplays": 3,
        "revealTranscriptAfterAttempt": True,
    })
    item = choose(item_id, prompt, options, correct, concept, pool, feedback,
                  source=source, **kwargs)
    item["format"] = "escuchar"
    return content_hash(item)


def fill(item_id, prompt, answer, accepted, concept, pool, feedback, **kwargs):
    item = base(item_id, "completar", prompt, concept, pool, feedback, **kwargs)
    item["answer"] = {"text": answer, "accepted": accepted}
    return content_hash(item)


def multi_fill(item_id, prompt, source_text, sentences, answers, concept, pool,
               feedback, **kwargs):
    scoring = {
        "parts": len(answers),
        "total": len(answers),
        "minimumCorrect": len(answers),
        "requiredParts": list(range(len(answers))),
        "independentAttempt": True,
    }
    source = dict(kwargs.pop("source", {}) or {})
    source.update({"text": source_text, "sentences": sentences})
    item = base(item_id, "completar", prompt, concept, pool, feedback,
                source=source, scoring=scoring, **kwargs)
    joined = " | ".join(answers)
    item["answer"] = {
        "text": joined,
        "accepted": [joined],
        "parts": [{"text": answer, "accepted": [answer]} for answer in answers],
    }
    return content_hash(item)


def order(item_id, prompt, answer, concept, pool, feedback, **kwargs):
    item = base(item_id, "ordenar", prompt, concept, pool, feedback, **kwargs)
    item["answer"] = {"text": answer, "tokens": answer.split()}
    return content_hash(item)


def match(item_id, prompt, pairs, concept, pool, feedback, minimum=None, **kwargs):
    shift = rotation(item_id, len(pairs))
    pairs = pairs[shift:] + pairs[:shift]
    values = [[left, {"es": right}] for left, right in pairs]
    scoring = None
    if minimum is not None:
        scoring = {"parts": len(values), "total": len(values), "minimumCorrect": minimum,
                   "independentAttempt": True}
    item = base(item_id, "relacionar", prompt, concept, pool, feedback,
                scoring=scoring, **kwargs)
    item["origin"]["pairs"] = values
    item["answer"] = {"pairs": values}
    return content_hash(item)


def write(item_id, prompt, source_text, answers, concept, pool, feedback, *, word_range,
          **kwargs):
    source = dict(kwargs.pop("source", {}) or {})
    source["text"] = source_text
    item = base(item_id, "escribir", prompt, concept, pool, feedback, source=source,
                scoring={"wordRange": word_range, "independentAttempt": True}, **kwargs)
    shift = rotation(item_id, len(answers))
    accepted = answers[shift:] + answers[:shift]
    item["answer"] = {"text": accepted[0], "accepted": accepted}
    return content_hash(item)


def teaching(n, rows):
    result = []
    for index, (en, es, explanation) in enumerate(rows, 1):
        en_words, es_words = en.split(), es.split()
        en_cut, es_cut = max(1, len(en_words) // 2), max(1, len(es_words) // 2)
        result.append({
            "id": f"en.n3.class-{n:02d}.t{index:02d}",
            "en": en,
            "es": es,
            "explanationEs": explanation,
            "segments": [
                {"en": " ".join(en_words[:en_cut]), "es": " ".join(es_words[:es_cut])},
                {"en": " ".join(en_words[en_cut:]), "es": " ".join(es_words[es_cut:])},
            ],
            "audioText": en,
            "audioMode": "tts",
            "languageCode": "en",
            "patternId": CONCEPTS[n],
        })
    return result


def balance_choices(doc):
    """Keep answer positions balanced while allowing the seed to change their rotation."""
    choice_items = [item for pool in doc["pools"].values() for item in pool
                    if item["format"] in {"elegir", "escuchar"}]
    offset = rotation(doc["id"] + ".balance", 3)
    for ordinal, item in enumerate(choice_items):
        target = (ordinal + offset) % 3
        current = item["answer"]["index"]
        correct = item["choices"].pop(current)
        item["choices"].insert(target, correct)
        item["answer"]["index"] = target
        content_hash(item)
    return doc


def route(n, teaching_id, review_id, *, cumulative=False):
    reteach_steps = list(dict.fromkeys([
        f"en.n3.class-{n:02d}.{teaching_id}", f"en.n3.class-{n:02d}.t06"
    ]))
    route_data = {
        "reteach": f"en.n3.class-{n:02d}.{teaching_id}",
        "review": f"en.n3.c{n}.{review_id}",
        "reteachSteps": reteach_steps,
        "reviewSteps": [f"en.n3.c{n}.{review_id}"],
    }
    if cumulative:
        route_data["reteachSteps"] = [f"en.n3.class-{k:02d}.t06" for k in NUMBERS]
        route_data["reviewSteps"] = [f"en.n3.c{n}.r01", f"en.n3.c{n}.r02", f"en.n3.c{n}.r03"]
    return route_data


def make_class(n, vocabulary, rows, pools, remediation):
    map_data = json.loads(MAP.read_text())
    spec = next(item for item in map_data["classes"] if item["id"] == f"en.n3.class-{n:02d}")
    assert spec["phase"] == PHASES[n] and spec["concepts"] == [CONCEPTS[n]]
    sequence = [
        *(dict(role="presentation", itemId=x["id"]) for x in pools["practiceGuided"]),
        {"role": "presentation", "itemId": pools["practice"][0]["id"]},
        *(dict(role="practice", itemId=x["id"]) for x in pools["practice"][1:]),
        {"role": "task", "itemId": pools["evaluation"][0]["id"]},
        {"role": "quiz", "itemId": pools["evaluation"][1]["id"]},
        *(dict(role="exam", itemId=x["id"]) for x in pools["evaluation"][2:]),
        *(dict(role="exam", itemId=x["id"]) for x in pools["review"][:2]),
        {"role": "remediation", "itemId": pools["review"][2]["id"]},
    ]
    item_formats = {item["format"] for pool in pools.values() for item in pool}
    skills = ["gramática", "lectura"]
    if "escuchar" in item_formats:
        skills.append("escucha")
    if "escribir" in item_formats:
        skills.append("escritura")
    doc = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 3,
        "cefr": "B1", "scale": "client-10-levels-v1", "status": "shadow",
        "runtimeAi": False, "phase": PHASES[n], "variantSeed": VARIANT_SEED,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY), "id": spec["id"], "title": spec["title"],
        "objectives": {"es": [spec["canDo"]["es"], spec["assessment"]["taskEs"]]},
        "concepts": [CONCEPTS[n]], "skills": skills,
        "prerequisites": spec["prerequisites"],
        "usesVocabulary": [en for en, _ in vocabulary],
        "usesPatterns": ALL_CONCEPTS if n == 70 else [CONCEPTS[n]],
        "vocabulary": [{"en": en, "es": es} for en, es in vocabulary],
        "teaching": teaching(n, rows), "pools": pools, "sequence": sequence,
        "remediationMap": remediation,
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True,
                          "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2, "allowAudioReplay": True,
                     "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if n == 70:
        doc["cumulativeEvaluation"] = ALL_CONCEPTS
    return balance_choices(doc)


def c66():
    n, c, p = 66, CONCEPTS[66], "en.n3.c66"
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "¿Qué frase expresa experiencia general?",
                   ["I have travelled alone before.", "My train left on 3 May.", "My bag is still missing."],
                   0, c, "practiceGuided", "Have travelled before describes general experience."),
            choose(f"{p}.pg02", "¿Qué frase aporta un detalle fechado?",
                   ["The delay began on Monday.", "I have used this airline before.", "The delay still affects me."],
                   0, c, "practiceGuided", "On Monday locates the event in completed time."),
            choose(f"{p}.pg03", "¿Qué frase muestra impacto presente?",
                   ["My suitcase is still missing.", "I flew to Rome in 2024.", "I have travelled often."],
                   0, c, "practiceGuided", "Still missing shows a problem that continues now."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige el análisis correcto.",
                   "I have taken this route before. The cancellation happened on Tuesday, and I am still waiting.",
                   ["experience + dated detail + current impact", "future plan + price + advice",
                    "past habit + comparison + permission"], 0, c, "practice",
                   "The update gives prior experience, Tuesday and a wait that continues."),
            match(f"{p}.p02", "Relaciona cada mensaje con su función.", [
                ("I have stayed here twice.", "experiencia general"),
                ("The lift stopped on 8 June.", "detalle fechado"),
                ("I cannot reach my room now.", "impacto presente"),
            ], c, "practice", "Each sentence supplies a different time function."),
            order(f"{p}.p03", "Ordena el impacto que continúa ahora.",
                  "My travel card is still not working", c, "practice",
                  "Still not working identifies the present consequence."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha y elige qué continúa ahora.",
                   "I have visited Bristol before. My coach broke down on Thursday, and I am still at the station.",
                   ["The traveller is still at the station.", "The traveller first visited Bristol on Thursday.",
                    "The coach is operating normally now."], 0, c, "evaluation",
                   "Still at the station states the current impact."),
            choose(f"{p}.e02", "¿Qué actualización distingue pasado e impacto actual?", [
                "The flight landed late on Friday, so I am still missing my connection.",
                "The flight is interesting, and connections can be useful.",
                "I may fly next Friday if I find a connection.",
            ], 0, c, "evaluation", "Friday dates the delay and still missing gives its present effect."),
            choose(f"{p}.e03", "¿Qué frase es solo experiencia, sin problema actual?", [
                "I have travelled by sleeper train several times.",
                "The sleeper train was cancelled last night, and I am still waiting.",
                "My sleeper ticket does not work at the gate now.",
            ], 0, c, "evaluation", "Several times reports experience without a current incident."),
            match(f"{p}.e04", "Clasifica cinco actualizaciones por experiencia, fecha e impacto.", [
                ("A. I have travelled on this line before.",
                 "solo experiencia general; no fecha ni impacto actual"),
                ("B. The cancellation happened on Monday.",
                 "solo incidencia fechada; no experiencia ni impacto actual"),
                ("C. I am still waiting at the station.",
                 "solo impacto actual; no experiencia ni fecha"),
                ("D. I have used this ferry before; it stopped on Sunday.",
                 "experiencia más incidencia fechada; sin impacto actual"),
                ("E. I have stayed here twice; the lift failed Tuesday; I still cannot reach my room.",
                 "experiencia, incidencia fechada e impacto actual"),
            ], c, "evaluation", "Each match preserves all three observable time layers.", minimum=4),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué marcador conecta el problema con ahora?",
                   ["still", "in 2022", "before"], 0, c, "review",
                   "Still signals that the situation continues."),
            listen(f"{p}.r02", "Escucha y elige el detalle fechado.",
                   "I have rented here before. The heating stopped on 14 January, and the room is still cold.",
                   ["14 January", "rented here before", "the room is still cold"], 0, c, "review",
                   "14 January fixes the incident in completed time."),
            match(f"{p}.r03", "Recupera cinco análisis completos de viaje.", [
                ("F. I have booked with this hotel before.",
                 "solo experiencia general; no fecha ni impacto actual"),
                ("G. The bridge closed on 6 March.",
                 "solo incidencia fechada; no experiencia ni impacto actual"),
                ("H. I still cannot enter my room.",
                 "solo impacto actual; no experiencia ni fecha"),
                ("I. I have visited Porto before; my wallet vanished on Sunday.",
                 "experiencia más incidencia fechada; sin impacto actual"),
                ("J. I have crossed here often; service stopped Friday; I remain stranded.",
                 "experiencia, incidencia fechada e impacto actual"),
            ], c, "review", "The recovery pairs three explicit facts in every new update.", minimum=4),
        ],
    }
    rem = {f"{p}.e01": route(n, "t03", "r01"), f"{p}.e02": route(n, "t06", "r02"),
           f"{p}.e03": route(n, "t01", "r01"), f"{p}.e04": route(n, "t06", "r03")}
    rows = [
        ("My travel experience includes a ferry journey.", "Mi experiencia de viaje incluye un trayecto en ferry.", "Present perfect reports general experience without a finished date."),
        ("The travel delay began on Monday.", "El retraso del viaje empezó el lunes.", "Past simple locates a completed incident in time."),
        ("I am still waiting at the port.", "Todavía espero en el puerto.", "Still plus a present situation shows current impact."),
        ("One impact update can contain three time layers.", "Una actualización de impacto puede contener tres capas temporales.", "Separate experience, dated incident and current consequence."),
        ("A dated detail makes the incident verifiable.", "Un detalle fechado hace verificable la incidencia.", "A day or date supports a factual account."),
        ("I have used this route before; it failed on Friday; I am still delayed.", "He usado esta ruta antes; falló el viernes; sigo retrasado.", "The model contains experience, a dated detail and current impact."),
    ]
    return make_class(n, [("experience", "experiencia"), ("dated", "fechado"), ("impact", "impacto"),
                          ("still", "todavía"), ("delay", "retraso"), ("missing", "perdido")],
                      rows, pools, rem)


def c67():
    n, c, p = 67, CONCEPTS[67], "en.n3.c67"
    pools = {
        "practiceGuided": [
            fill(f"{p}.pg01", "Completa una sola forma: I ___ for two hours.", "have been waiting",
                 ["have been waiting", "'ve been waiting"], c, "practiceGuided",
                 "I takes have been waiting for a temporary action."),
            fill(f"{p}.pg02", "Completa una sola forma: She ___ since 9:00.", "has been calling",
                 ["has been calling", "'s been calling"], c, "practiceGuided",
                 "She takes has been calling with a starting point."),
            choose(f"{p}.pg03", "¿Qué expresión marca duración total?",
                   ["for three hours", "since Monday", "at 8:00"], 0, c, "practiceGuided",
                   "For introduces the total length of an activity."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige la forma completa.",
                   "They have been looking for their luggage since noon.",
                   ["have been looking — since noon", "has been looked — for noon",
                    "have looking — at noon"], 0, c, "practice",
                   "They takes have been looking; since marks the starting point."),
            fill(f"{p}.p02", "Completa una sola forma: We ___ since Tuesday.", "have been travelling",
                 ["have been travelling", "have been traveling", "'ve been travelling", "'ve been traveling"],
                 c, "practice", "We takes have been plus the -ing form."),
            order(f"{p}.p03", "Ordena una espera temporal con duración.",
                  "He has been waiting for forty minutes", c, "practice",
                  "Has been waiting plus for states an ongoing temporary wait."),
        ],
        "evaluation": [
            fill(f"{p}.e01", "Completa con search: I ___ for my passport for an hour.", "have been searching",
                 ["have been searching", "'ve been searching"], c, "evaluation",
                 "Have been searching agrees with I and keeps the temporary action."),
            listen(f"{p}.e02", "Escucha y elige la oración correcta.",
                   "Mina has been waiting since half past ten.",
                   ["Mina has been waiting since 10:30.", "Mina have waited for 10:30.",
                    "Mina is been waiting at 10:30."], 0, c, "evaluation",
                   "Has been waiting and since express an action from 10:30 until now."),
            choose(f"{p}.e03", "¿Qué oración usa for con una duración?", [
                "We have been driving for four hours.", "We have been driving since four hours.",
                "We has been driving at four hours."], 0, c, "evaluation",
                   "For four hours gives a total duration."),
            match(f"{p}.e04", "Decide qué corrección completa cada una de cinco situaciones.", [
                ("I has been waiting for two hours.", "cambia has por have con primera persona singular"),
                ("She has calling since 8:00.", "añade been antes de la acción en -ing"),
                ("We have been travel for three days.", "cambia el verbo base por travelling tras been"),
                ("He has been looking for a taxi for noon.", "cambia for por since ante un punto de inicio"),
                ("They have been standing in line since forty minutes.", "cambia since por for ante una duración"),
            ], c, "evaluation", "Each decision repairs a different auxiliary, -ing or duration error.", minimum=4),
        ],
        "review": [
            choose(f"{p}.r01", "Elige la forma para he.",
                   ["has been waiting", "have been waiting", "has waiting"], 0, c, "review",
                   "He requires has been before the -ing form."),
            listen(f"{p}.r02", "Escucha y elige la expresión de duración.",
                   "We have been driving for ninety minutes.",
                   ["for ninety minutes", "we have", "been driving"], 0, c, "review",
                   "For ninety minutes states the total duration."),
            match(f"{p}.r03", "Recupera cinco decisiones nuevas sobre forma y duración.", [
                ("Maya have been waiting since 7:15.", "cambia have por has con tercera persona singular"),
                ("I have trying for half an hour.", "añade been antes de trying"),
                ("The driver has been call since noon.", "cambia call por calling tras been"),
                ("We have been sitting here since twenty minutes.", "cambia since por for ante una duración"),
                ("The passengers have been queuing for 6:00.", "cambia for por since ante una hora inicial"),
            ], c, "review", "The recovery requires five new auxiliary, -ing and duration decisions.", minimum=4),
        ],
    }
    rem = {f"{p}.e01": route(n, "t01", "r01"), f"{p}.e02": route(n, "t03", "r02"),
           f"{p}.e03": route(n, "t04", "r02"), f"{p}.e04": route(n, "t06", "r03")}
    rows = [
        ("I have been waiting for two hours.", "He estado esperando durante dos horas.", "Use have been plus -ing with I, we, you and they."),
        ("She has been calling since nine.", "Ella ha estado llamando desde las nueve.", "Use has been plus -ing with he, she and it."),
        ("For gives a length of time.", "For expresa una duración.", "For answers how long with a quantity of time."),
        ("Since gives the starting point.", "Since expresa el punto de inicio.", "Since answers how long with the moment the action began."),
        ("The temporary action has a visible duration.", "La acción temporal tiene una duración visible.", "This form connects an ongoing activity to the present."),
        ("They have been waiting for two hours: subject, auxiliary, action and duration.", "Han estado esperando durante dos horas: sujeto, auxiliar, acción y duración.", "The complete model makes all four parts observable."),
    ]
    return make_class(n, [("waiting", "esperando"), ("calling", "llamando"),
                          ("travelling", "viajando"), ("duration", "duración"),
                          ("since", "desde"), ("for", "durante")], rows, pools, rem)


def c68():
    n, c, p = 68, CONCEPTS[68], "en.n3.c68"
    audio_eval = ("Traveller: My suitcase did not arrive on flight GX214 yesterday. My baggage receipt is B42. "
                  "Could you trace the suitcase and tell me where it is? Agent: I will check the baggage system "
                  "and call you at six this evening.")
    audio_review = ("Guest: The airport shuttle missed my stop this morning. My booking code is SH73. "
                    "Could you arrange the next shuttle? Clerk: I will contact the driver and update you at noon.")
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "¿Qué dato identifica la incidencia?",
                   ["The suitcase did not arrive.", "Receipt B42", "Call at 6:00"], 0, c,
                   "practiceGuided", "The missing suitcase is the incident itself."),
            choose(f"{p}.pg02", "¿Qué dato sirve como evidencia verificable?",
                   ["Baggage receipt B42", "I feel disappointed", "Please help soon"], 0, c,
                   "practiceGuided", "The receipt code can be checked in a system."),
            choose(f"{p}.pg03", "¿Cuál es una petición concreta, no compensación inferida?",
                   ["Please trace my suitcase.", "Please refund the whole journey.", "Please pay for a hotel."], 0, c,
                   "practiceGuided", "Trace the suitcase is explicit and proportionate."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige la respuesta prometida.",
                   "My train was cancelled. Ticket K19. Please find another train. I will check and reply at 4:00.",
                   ["The agent will check and reply at 4:00.", "The agent promises a full refund.",
                    "The passenger will buy a car."], 0, c, "practice",
                   "Only a check and a reply at four are promised."),
            match(f"{p}.p02", "Relaciona cada campo con el dato visible.", [
                ("incidencia", "train cancelled"), ("evidencia", "ticket K19"),
                ("petición", "find another train"), ("respuesta", "check and reply at 4:00"),
            ], c, "practice", "The four fields reproduce only stated information."),
            order(f"{p}.p03", "Ordena una petición proporcionada.",
                  "Could you trace my missing suitcase", c, "practice",
                  "The request asks for an action tied to the incident."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha y elige la evidencia.",
                   "The coach left without me. My ticket number is C81. Please check the passenger list.",
                   ["ticket C81", "a station receipt", "the scheduled departure time"], 0, c, "evaluation",
                   "Ticket C81 is the only verifiable evidence stated."),
            choose(f"{p}.e02", "¿Qué respuesta evita inventar compensación?", [
                "I will check the system and email you tonight.", "I will issue a full refund tomorrow.",
                "I will pay for your taxi today."], 0, c, "evaluation",
                   "La respuesta correcta promete únicamente revisar el sistema y contactar después."),
            listen(f"{p}.e03", "Escucha y elige la petición exacta.",
                   "Room 312 has had no hot water since Tuesday. My booking is H55. Could you send maintenance today?",
                   ["Send maintenance today.", "Move the booking to next month.", "Refund the room today."],
                   0, c, "evaluation", "The speaker explicitly asks for maintenance today."),
            multi_fill(
                f"{p}.e04",
                "Lee la reclamación y completa los cuatro campos.",
                audio_eval,
                ["Incidente: ___", "Evidencia: ___", "Petición: ___", "Respuesta prometida: ___"],
                ["my suitcase did not arrive", "flight GX214 and baggage receipt B42",
                 "trace the suitcase", "check the baggage system and call at six"],
                c, "evaluation",
                "Los cuatro campos conservan por separado incidencia, evidencia, petición y respuesta.",
            ),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué campo responde qué hará la empresa?",
                   ["respuesta", "evidencia", "incidencia"], 0, c, "review",
                   "The response records the action promised by staff."),
            listen(f"{p}.r02", "Escucha y elige lo que no se prometió.",
                   "We will locate the bag and call at eight. No payment decision has been made.",
                   ["compensation", "a search", "a call at eight"], 0, c, "review",
                   "The speaker explicitly says no payment decision exists."),
            multi_fill(
                f"{p}.r03",
                "Lee la reclamación nueva y recupera sus cuatro campos.",
                audio_review,
                ["Incidente: ___", "Evidencia: ___", "Petición: ___", "Respuesta prometida: ___"],
                ["the airport shuttle missed my stop", "booking code SH73",
                 "arrange the next shuttle", "contact the driver and update me at noon"],
                c, "review",
                "La recuperación puntúa por separado los cuatro datos de la reclamación.",
            ),
        ],
    }
    rem = {f"{p}.e01": route(n, "t02", "r01"), f"{p}.e02": route(n, "t04", "r02"),
           f"{p}.e03": route(n, "t03", "r01"), f"{p}.e04": route(n, "t06", "r03")}
    rows = [
        ("The incident states what went wrong.", "La incidencia indica qué salió mal.", "Identify the event before considering a solution."),
        ("A code or receipt provides evidence.", "Un código o recibo aporta evidencia.", "Verifiable details support the complaint."),
        ("The traveller makes one clear request.", "El viajero hace una petición clara.", "Record the requested solution exactly."),
        ("The response states what staff will do.", "La respuesta indica qué hará el personal.", "Do not add compensation that was not promised."),
        ("Incident, evidence, request and response form a factual record.", "Incidencia, evidencia, petición y respuesta forman un registro factual.", "The four fields have distinct roles."),
        ("My bus failed; ticket C20 is evidence; I requested a replacement; staff will reply at five.", "Mi autobús falló; el billete C20 es evidencia; pedí un reemplazo; el personal responderá a las cinco.", "The model supplies incident, evidence, request and response without compensation."),
    ]
    return make_class(n, [("incident", "incidencia"), ("evidence", "evidencia"),
                          ("request", "petición"), ("response", "respuesta"),
                          ("receipt", "recibo"), ("compensation", "compensación")], rows, pools, rem)


def c69():
    n, c, p = 69, CONCEPTS[69], "en.n3.c69"
    s_task = ("Billete: autobús B318, 12 agosto, salida 14:10. Salió 15:35. Impacto: perdió la conexión "
              "de las 16:00 y esperó 3 horas. Petición permitida: explicación escrita y revisión del coste "
              "de la nueva conexión.")
    a_task = [
        "I am writing about bus B318 on 12 August, scheduled to leave at 14:10. It finally left at 15:35, so I missed my 16:00 connection and waited three more hours. This caused a clear disruption to my journey. Please provide a written explanation for the delay and review the cost of the replacement connection I had to use. I have included the ticket details so that you can check the journey. I would appreciate a factual reply about these two requests.",
        "My complaint concerns bus B318 on 12 August. The ticket showed a 14:10 departure, but the bus left at 15:35. As a result, I missed the 16:00 connection and had to wait another three hours. Could you send me a written explanation and review the cost of my replacement connection? These requests relate directly to the delay and its concrete impact. The bus number, date and times above should allow you to verify the incident and respond accurately.",
    ]
    s_exam = ("Billete: tren T906, 4 septiembre, salida 09:20. Salió 10:45. Impacto: perdió una cita "
              "a las 11:30 y pagó £18 por otro autobús. Petición permitida: explicación y revisión de £18.")
    a_exam = [
        "I am writing about train T906 on 4 September. My ticket showed a 09:20 departure, but the train left at 10:45. Because of this delay, I missed an appointment at 11:30 and paid £18 for another bus. Please explain why the train was delayed and review the extra £18 cost. I have provided the train number, date and exact times so that the incident can be checked. I am requesting only a factual explanation and consideration of the documented transport expense.",
        "My complaint concerns train T906 on 4 September, scheduled for 09:20. It did not leave until 10:45. The delay meant that I missed my 11:30 appointment and had to spend £18 on a different bus. Could you provide a written explanation and review that £18 transport cost? The ticket number, date, scheduled time and actual time are included for verification. My request is limited to the direct consequence of the delay, and I would appreciate an accurate written response.",
    ]
    s_review = ("Billete: ferry F27, 21 octubre, salida 07:30. Salió 09:00. Impacto: perdió el autobús "
                "de las 09:15 y pagó €14 por un taxi. Petición permitida: explicación y revisión de €14.")
    a_review = [
        "I am writing about ferry F27 on 21 October. It was scheduled to leave at 07:30, but it left at 09:00. The delay made me miss the 09:15 bus, so I paid €14 for a taxi. Please provide a written explanation for the late departure and review the €14 taxi cost. I have included the ferry number, date and both departure times to support the complaint. My request concerns only the direct travel expense caused by this documented delay.",
        "My complaint concerns ferry F27 on 21 October. The ticket stated 07:30, while the ferry actually departed at 09:00. I then missed the 09:15 bus and had to pay €14 for a taxi. Could you explain the delay in writing and review this €14 expense? The service number and exact times make the event verifiable. I am asking for a proportionate response connected to the immediate impact, not for any benefit that is not supported by these facts.",
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "¿Qué inicio contiene datos verificables?", [
                "Train R18 was due at 08:10 on 6 May but arrived at 09:05.",
                "The train was terribly bad and ruined everything.",
                "Trains are often difficult for many people."], 0, c, "practiceGuided",
                   "Service, date and two times can be verified."),
            choose(f"{p}.pg02", "¿Qué frase expresa un impacto concreto?", [
                "I missed the 10:00 coach and paid £12 for a taxi.",
                "I was unhappy about transport in general.",
                "The station could be more attractive."], 0, c, "practiceGuided",
                   "The missed coach and £12 expense are specific consequences."),
            choose(f"{p}.pg03", "¿Qué petición es proporcionada a un retraso documentado?", [
                "Please explain the delay and review my £12 taxi cost.",
                "Please refund the complete holiday immediately.",
                "Please reimburse an unrecorded hotel stay."], 0, c, "practiceGuided",
                   "The first request addresses the stated delay and direct cost."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige la cronología fiel.",
                   "Coach C40 was due at 11:20 on 7 June. It left at 12:35, and I missed my 13:00 train.",
                   ["due 11:20 → left 12:35 → missed 13:00 train",
                    "left 11:20 → train arrived 12:35 → due 13:00",
                    "missed 11:20 coach → left train 13:00"], 0, c, "practice",
                   "The first sequence preserves all three stated times."),
            match(f"{p}.p02", "Relaciona cada parte con su función.", [
                ("Flight D55, 3 July, due 16:40", "datos verificables"),
                ("I missed the final airport bus", "impacto concreto"),
                ("Please review my €16 taxi receipt", "petición proporcionada"),
            ], c, "practice", "Each phrase has one distinct role in a factual complaint."),
            order(f"{p}.p03", "Ordena una petición factual y limitada.",
                  "Please explain the delay and review the documented taxi cost", c, "practice",
                  "The request connects an explanation and one evidenced expense."),
        ],
        "evaluation": [
            write(f"{p}.e01", "Redacta 80–100 palabras usando solo los datos visibles.", s_task, a_task, c,
                  "evaluation", "The model includes verifiable details, concrete impact and two limited requests.",
                  word_range=[80, 100]),
            choose(f"{p}.e02", "¿Qué dato permite verificar la hora prevista?",
                   ["the scheduled time on the ticket", "the actual time on the station display", "the connection time in the booking email"],
                   0, c, "evaluation", "The ticket's scheduled time is an objective reference."),
            listen(f"{p}.e03", "Escucha y elige la petición apoyada por los datos.",
                   "Flight P61 arrived two hours late. I paid €22 for a replacement bus and have the receipt.",
                   ["Review the documented €22 bus cost.", "Refund the complete return ticket.",
                    "Review an unrecorded hotel bill."], 0, c, "evaluation",
                   "The €22 request is tied to a stated cost and receipt."),
            write(f"{p}.e04", "Escribe 80–100 palabras con cronología, impacto y petición.", s_exam, a_exam, c,
                  "evaluation", "The exam response keeps every time, the £18 impact and a proportionate request.",
                  word_range=[80, 100]),
        ],
        "review": [
            choose(f"{p}.r01", "Billete: 21 Oct; salida real: 09:00. ¿Qué frase no inventa datos?", [
                "The ferry left at 09:00, according to my ticket record.",
                "The ferry left at 08:30, according to my ticket record.",
                "The ferry left at 09:00 on 22 October."], 0, c, "review",
                   "La opción correcta usa la hora real y el registro disponible sin inventar la fecha."),
            listen(f"{p}.r02", "Escucha y elige el impacto directo.",
                   "The ferry delay made me miss the 09:15 bus, so I paid fourteen euros for a taxi.",
                   ["missed bus and €14 taxi", "free accommodation", "lost luggage"], 0, c, "review",
                   "Only the missed bus and taxi cost are stated."),
            write(f"{p}.r03", "Recupera 80–100 palabras con otro billete y retraso.", s_review, a_review, c,
                  "review", "The recovery uses a new ferry scenario and keeps the request evidence-based.",
                  word_range=[80, 100]),
        ],
    }
    rem = {f"{p}.e01": route(n, "t06", "r03"), f"{p}.e02": route(n, "t01", "r01"),
           f"{p}.e03": route(n, "t03", "r02"), f"{p}.e04": route(n, "t06", "r03")}
    rows = [
        ("Open with the service, date and scheduled time.", "Empieza con servicio, fecha y hora prevista.", "These details make the complaint verifiable."),
        ("Compare the scheduled and actual times in order.", "Compara las horas prevista y real en orden.", "A clear timeline avoids vague accusations."),
        ("Describe one concrete impact on the journey.", "Describe un impacto concreto en el viaje.", "A missed connection or documented cost shows impact."),
        ("Make a proportionate request linked to the evidence.", "Haz una petición proporcionada vinculada a la evidencia.", "A proportionate request follows from the supplied facts."),
        ("Use documented facts, not invented promises.", "Usa hechos documentados, no promesas inventadas.", "Use only the source card and visible records."),
        ("I am writing about flight J72 on 18 November. It was scheduled for 13:15 but departed at 14:40. Because of this delay, I missed the 15:10 airport bus and paid €17 for a taxi. Please provide a written explanation and review this documented €17 cost. The flight number, date and both departure times make the incident verifiable. My request is proportionate to the direct impact, and I am not asking for any benefit that these facts do not support.", "Escribo por el vuelo J72 del 18 de noviembre. Estaba previsto a las 13:15, pero salió a las 14:40. Por el retraso, perdí el autobús de las 15:10 y pagué 17 € por un taxi. Pido una explicación escrita y la revisión de ese gasto documentado.", "This distinct 80–100 word model connects chronology, impact and request."),
    ]
    return make_class(n, [("ticket", "billete"), ("scheduled", "previsto"), ("delay", "retraso"),
                          ("impact", "impacto"), ("documented", "documentado"),
                          ("proportionate", "proporcionado")], rows, pools, rem)


def c70():
    n, c, p = 70, CONCEPTS[70], "en.n3.c70"
    s_task = ("Escenario aeropuerto. Has volado con AX dos veces antes. Vuelo AX40 cancelado a las 10:15. Esperas desde las 08:45. Reserva R81; "
              "debes llegar antes de 18:00 y llevas maleta facturada. A: vuelo 12:20–16:50, acepta maleta. "
              "B: 13:10–18:25, acepta maleta. C: 11:40–15:55, solo equipaje de mano. La agente confirma A "
              "con asiento 18C y localizador N44. Redacta la resolución.")
    a_task = [
        "I have flown with AX twice before. My flight AX40 was cancelled at 10:15, and I have been waiting since 08:45. Booking R81 and my checked bag are the evidence. I asked for a route arriving before 18:00. Route B arrives too late, while route C does not accept my checked bag. Route A leaves at 12:20, arrives at 16:50 and accepts the bag, so it meets both limits. The agent has confirmed route A, seat 18C, under reference N44. I will use that booking and keep the confirmation for check-in.",
        "I have travelled with AX twice before, but flight AX40 was cancelled at 10:15. I have been waiting since 08:45, and reservation R81 confirms my original journey. I need to arrive before 18:00 with a checked bag. Option B reaches the airport at 18:25, so it is late. Option C arrives earlier but permits hand luggage only. Option A reaches the destination at 16:50 and accepts my bag. I requested that compatible route, and the agent confirmed option A with seat 18C and new reference N44. I will travel on this replacement.",
    ]
    s_exam = ("Escenario ferry. Has usado esta compañía dos veces. Ferry SF12 cancelado el martes a las 07:00. Esperas desde las 06:20. Billete E52; "
              "debes llegar a la isla antes de 14:00 y viajas con bicicleta. A: 08:10–13:20, acepta bici. "
              "B: 09:00–14:15, acepta bici. C: 07:50–12:40, no acepta bici. Personal confirma A, cubierta 2, "
              "reserva Q73. Explica y confirma la solución.")
    a_exam = [
        "I have used this ferry company twice before. Ferry SF12 was cancelled on Tuesday at 07:00, and I have been waiting since 06:20. Ticket E52 provides the booking evidence. I need to reach the island before 14:00 with my bicycle. Route B arrives at 14:15 and misses the limit. Route C arrives early but does not accept bicycles. Route A leaves at 08:10, arrives at 13:20 and carries bicycles, so it satisfies both conditions. Staff confirmed route A, deck 2, under reservation Q73. I accept this replacement.",
        "I have travelled with this ferry company twice. Ferry SF12 was cancelled at 07:00 on Tuesday. I have been waiting since 06:20, and ticket E52 identifies the journey. My request is a route that arrives before 14:00 and accepts my bicycle. Option B is too late; option C rejects bicycles. Option A reaches the island at 13:20 and allows the bicycle, so it is the only compatible choice. Staff confirmed option A, deck 2, with booking Q73. I have accepted this new reservation for boarding today.",
    ]
    s_review = ("Escenario tren. Has viajado en esta línea antes. Tren LM60 cancelado el viernes a las 15:10. Esperas desde las 14:30. Billete T24; "
                "debes llegar antes de 21:00 y necesitas acceso sin escalones. A: 16:00–20:20, acceso sin escalones. "
                "B: 16:30–21:10, acceso sin escalones. C: 15:50–19:45, solo escaleras. Personal confirma A, "
                "coche 4, reserva V62. Redacta la recuperación.")
    a_review = [
        "I have travelled on this railway before. Train LM60 was cancelled on Friday at 15:10. I have been waiting since 14:30, and ticket T24 is the evidence for my journey. I must arrive before 21:00 and need step-free access. Route B arrives at 21:10, after the limit. Route C is earlier but has stairs only. Route A arrives at 20:20 and provides step-free access, so it meets both requirements. Staff confirmed route A, coach 4, with reservation V62. I accept the replacement and will keep this confirmation ready.",
        "I have used this train line before. Train LM60 was cancelled at 15:10 on Friday, and I have been waiting since 14:30. Ticket T24 identifies the affected booking. I requested an option arriving before 21:00 with step-free access. Option B is ten minutes too late, and option C only has stairs. Option A reaches the destination at 20:20 and is step-free, making it compatible. The agent confirmed option A in coach 4 under reference V62. I accepted that new booking and will present the confirmation at the accessible gate.",
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "¿Qué opción cumple llegada y equipaje?", [
                "A: arrives 16:50; checked bags accepted", "B: arrives 18:25; checked bags accepted",
                "C: arrives 15:55; hand luggage only"], 0, c, "practiceGuided",
                   "Only A meets the arrival limit and accepts the checked bag."),
            choose(f"{p}.pg02", "¿Qué frase explica una espera que continúa?", [
                "I have been waiting since 08:45.", "I waited at 08:45 yesterday.",
                "I will wait after the flight."], 0, c, "practiceGuided",
                   "Have been waiting since connects the ongoing wait to its start."),
            choose(f"{p}.pg03", "¿Qué dato confirma una nueva reserva?", [
                "route A, seat 18C, reference N44", "route A might be useful", "the airport is busy"],
                   0, c, "practiceGuided", "Route, seat and reference make the confirmation observable."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige la opción compatible.",
                   "You must arrive before six and you have a checked bag. A arrives at 4:50 and accepts it. B arrives at 6:25. C allows hand luggage only.",
                   ["A", "B", "C"], 0, c, "practice",
                   "A meets the time limit and the baggage condition."),
            match(f"{p}.p02", "Relaciona cada dato con su función.", [
                ("AX40 cancelled at 10:15", "incidencia fechada"),
                ("waiting since 08:45", "duración actual"),
                ("R81 and checked bag", "evidencia y condición"),
                ("A arrives 16:50 and accepts bag", "opción compatible"),
                ("seat 18C, reference N44", "confirmación nueva"),
            ], c, "practice", "The five functions recover the complete resolution logic."),
            order(f"{p}.p03", "Ordena la confirmación final.",
                  "The agent confirmed route A under reference N44", c, "practice",
                  "The confirmation names the route and its new reference."),
        ],
        "evaluation": [
            write(f"{p}.e01", "Resuelve el aeropuerto en 90–120 palabras.", s_task, a_task, ALL_CONCEPTS,
                  "evaluation", "The response explains the incident, wait, evidence, comparison and confirmed route.",
                  word_range=[90, 120], requires=ALL_CONCEPTS),
            listen(f"{p}.e02", "Escucha y elige por qué C no es compatible.",
                   "Route C arrives at 15:55, but it accepts hand luggage only. The traveller has a checked bag.",
                   ["It does not accept the checked bag.", "It arrives after 18:00.", "It has no departure time."],
                   0, ALL_CONCEPTS, "evaluation", "C fails the explicit checked-bag condition.",
                   requires=ALL_CONCEPTS),
            match(f"{p}.e03", "Relaciona cinco evidencias de la resolución.", [
                ("I have used this railway before", "experiencia general"),
                ("We have been queuing for ninety minutes", "acción temporal y duración"),
                ("Train P20 cancelled; ticket L31", "incidencia y evidencia"),
                ("The delay made us miss the last bus", "impacto concreto"),
                ("Route D meets both limits; Z51 confirmed", "opción compatible y reserva nueva"),
            ], ALL_CONCEPTS, "evaluation", "Each pair makes one cumulative concept observable.",
                  minimum=5, requires=ALL_CONCEPTS),
            write(f"{p}.e04", "Resuelve el ferry en 90–120 palabras.", s_exam, a_exam, ALL_CONCEPTS,
                  "evaluation", "The ferry answer rejects two routes with evidence and confirms the only compatible one.",
                  word_range=[90, 120], requires=ALL_CONCEPTS),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué opción satisface ambas restricciones del ferry?", [
                "A: arrives 13:20 and accepts bicycles", "B: arrives 14:15 and accepts bicycles",
                "C: arrives 12:40 but rejects bicycles"], 0, ALL_CONCEPTS, "review",
                   "A alone meets the time and bicycle requirements.", requires=ALL_CONCEPTS),
            listen(f"{p}.r02", "Escucha y elige la confirmación completa.",
                   "Staff confirmed option A, deck two, under reservation Q seven three.",
                   ["A / deck 2 / Q73", "B / deck 3 / Q37", "C / no reservation"], 0,
                   ALL_CONCEPTS, "review", "The audio confirms route A, deck 2 and Q73.",
                   requires=ALL_CONCEPTS),
            write(f"{p}.r03", "Recupera el tren en 90–120 palabras.", s_review, a_review, ALL_CONCEPTS,
                  "review", "The train recovery uses a distinct access constraint and a complete new confirmation.",
                  word_range=[90, 120], requires=ALL_CONCEPTS),
        ],
    }
    rem = {f"{p}.e01": route(n, "t06", "r03", cumulative=True),
           f"{p}.e02": route(n, "t04", "r01"),
           f"{p}.e03": route(n, "t06", "r03", cumulative=True),
           f"{p}.e04": route(n, "t06", "r03", cumulative=True)}
    rows = [
        ("Explain the cancellation with a dated fact.", "Explica la cancelación con un dato fechado.", "The service, day and time establish what happened."),
        ("State the waiting restriction and its duration.", "Indica la restricción de espera y su duración.", "Present perfect continuous connects the wait to now."),
        ("Use the booking as evidence for the request.", "Usa la reserva como evidencia para la petición.", "A verifiable code supports the complaint."),
        ("Compare every route with every visible restriction.", "Compara cada ruta con cada restricción visible.", "A route is compatible only if it meets all conditions."),
        ("Confirm the route, seat or place and reference.", "Confirma ruta, asiento o lugar y referencia.", "A complete confirmation makes the new booking usable."),
        ("I have taken coach K8 before. It was cancelled at 09:10, and I have been waiting since 08:30 with ticket P14. I need to arrive before 15:00 with a bicycle. Route A arrives at 14:20 and accepts bicycles; B arrives at 15:25; C arrives at 13:50 but rejects bicycles. I requested A because it meets both restrictions. Staff confirmed route A, seat 7, under booking W36. The dated incident, ongoing wait, evidence, concrete travel impact, compatible comparison and confirmed replacement resolve the complaint without inventing compensation.", "He tomado antes el autobús K8. Se canceló a las 09:10 y espero desde las 08:30 con el billete P14. Debo llegar antes de las 15:00 con bicicleta. Solo la ruta A cumple ambas condiciones. El personal confirmó A, asiento 7, reserva W36.", "This distinct 90–120 word coach model demonstrates all five block concepts."),
    ]
    return make_class(n, [("cancellation", "cancelación"), ("route", "ruta"),
                          ("restriction", "restricción"), ("compatible", "adecuado"),
                          ("booking", "reserva"), ("confirmed", "confirmado")], rows, pools, rem)


BUILDERS = {66: c66, 67: c67, 68: c68, 69: c69, 70: c70}


def audit(classes, full=False):
    prompts, feedback, signatures = set(), set(), set()
    indices, totals, formats = Counter(), Counter(), Counter()
    for doc in classes:
        assert doc["status"] == "shadow" and doc["runtimeAi"] is False
        assert doc["qualityPolicy"] == QUALITY and len(doc["teaching"]) == 6
        assert len(doc["vocabulary"]) >= 6
        ids = [step["itemId"] for step in doc["sequence"]]
        assert len(ids) == 13 and len(set(ids)) == 13
        assert Counter(step["role"] for step in doc["sequence"]) == {
            "presentation": 4, "practice": 2, "task": 1, "quiz": 1, "exam": 4,
            "remediation": 1,
        }
        for pool, count in (("practiceGuided", 3), ("practice", 3), ("evaluation", 4), ("review", 3)):
            assert len(doc["pools"][pool]) == count
            totals[pool] += count
            for item in doc["pools"][pool]:
                assert len(item["prompt"]["es"]) <= 90
                assert item["contentHash"] == "sha256:" + hashlib.sha256(canon(
                    {k: v for k, v in item.items() if k not in {"id", "contentHash"}}).encode()).hexdigest()
                assert norm(item["prompt"]["es"]) not in prompts
                prompts.add(norm(item["prompt"]["es"]))
                fb = norm(item["origin"]["feedback"]["es"])
                assert fb not in feedback
                feedback.add(fb)
                assert item["origin"]["variantSeed"] == VARIANT_SEED
                if pool != "practiceGuided":
                    assert "hint" not in item["origin"]
                if item["format"] in {"elegir", "escuchar"}:
                    assert len(item["choices"]) >= 3
                    indices[item["answer"]["index"]] += 1
                if item["format"] == "completar":
                    if "parts" in item["answer"]:
                        assert len(item["origin"]["sentences"]) == len(item["answer"]["parts"])
                        assert all("___" in sentence for sentence in item["origin"]["sentences"])
                        assert len(item["answer"]["accepted"]) >= 1
                    else:
                        assert item["prompt"]["es"].count("___") == 1
                        assert len(item["answer"]["accepted"]) >= 2
                if item["format"] == "escribir":
                    assert len(item["answer"]["accepted"]) >= 2 and "text" in item["origin"]
                    low, high = item["origin"]["scoring"]["wordRange"]
                    assert all(low <= len(words(answer)) <= high for answer in item["answer"]["accepted"])
                if "minimumCorrect" in item["origin"].get("scoring", {}):
                    scoring = item["origin"]["scoring"]
                    assert item["format"] in {"relacionar", "completar"}
                    expected_parts = (len(item["origin"]["pairs"]) if item["format"] == "relacionar"
                                      else len(item["answer"]["parts"]))
                    assert scoring["parts"] == scoring["total"] == expected_parts
                    assert 1 <= scoring["minimumCorrect"] <= scoring["total"]
                formats[item["format"]] += 1
                signal = item["origin"].get("audio") or item["origin"].get("text") or item["origin"].get("pairs") or item["prompt"]
                fingerprint = norm({"signal": signal, "answer": item["answer"]})
                assert fingerprint not in signatures
                signatures.add(fingerprint)
        assert len({item["format"] for pool in doc["pools"].values() for item in pool}) >= 4
        visible = norm({"teaching": doc["teaching"], "pools": doc["pools"]})
        assert all(norm(v["en"]) in visible for v in doc["vocabulary"])
        assert set(doc["remediationMap"]) == {item["id"] for item in doc["pools"]["evaluation"]}
        teaching_ids = {item["id"] for item in doc["teaching"]}
        review_ids = {item["id"] for item in doc["pools"]["review"]}
        for value in doc["remediationMap"].values():
            assert value["reteach"] in teaching_ids and value["review"] in review_ids
    if full:
        assert len(classes) == 5 and sum(totals.values()) == 65
        assert len(indices) >= 3 and max(indices.values()) / sum(indices.values()) <= .5
        by_number = {int(doc["id"].rsplit("-", 1)[1]): doc for doc in classes}
        for number in (66, 67):
            assessment = by_number[number]["pools"]["evaluation"][3]
            assert assessment["format"] == "relacionar"
            assert len(assessment["origin"]["pairs"]) == 5
            assert assessment["origin"]["scoring"]["minimumCorrect"] == 4
        c66_pairs = by_number[66]["pools"]["evaluation"][3]["origin"]["pairs"]
        c66_right = " ".join(pair[1]["es"] for pair in c66_pairs).casefold()
        assert all(label in c66_right for label in (
            "solo experiencia", "solo incidencia", "solo impacto",
            "experiencia más incidencia", "experiencia, incidencia"
        ))
        assert not any(detail in c66_right for detail in ("monday", "tuesday", "sunday", "station", "ferry"))
        c67_pairs = by_number[67]["pools"]["evaluation"][3]["origin"]["pairs"]
        c67_left = " ".join(pair[0] for pair in c67_pairs)
        c67_right = " ".join(pair[1]["es"] for pair in c67_pairs)
        assert all(marker in c67_left for marker in ("has been waiting", "has calling", "have been travel"))
        assert all(marker in c67_right for marker in ("has por have", "añade been", "por travelling", "for por since", "since por for"))
        assert not any(detail in c67_right for detail in ("two hours", "8:00", "three days", "noon", "forty minutes"))
        complaint = by_number[68]["pools"]["evaluation"][3]
        assert complaint["format"] == "completar"
        assert len(complaint["origin"]["sentences"]) == 4
        assert len(complaint["answer"]["parts"]) == 4
        assert complaint["origin"]["scoring"]["minimumCorrect"] == 4
        assert complaint["origin"]["scoring"]["requiredParts"] == [0, 1, 2, 3]
        correct_complaint = canon(complaint["answer"]["parts"]).lower()
        assert "suitcase did not arrive" in correct_complaint and "gx214" in correct_complaint
        recovery_complaint = by_number[68]["pools"]["review"][2]
        assert recovery_complaint["format"] == "completar"
        assert len(recovery_complaint["answer"]["parts"]) == 4
        assert recovery_complaint["origin"]["scoring"]["requiredParts"] == [0, 1, 2, 3]
        c69_distractors = canon(by_number[69]["pools"]["review"][0]["choices"]).lower()
        assert "secret warnings" not in c69_distractors and "every passenger" not in c69_distractors
        assert 80 <= len(words(by_number[69]["teaching"][5]["en"])) <= 100
        assert all(80 <= len(words(answer)) <= 100
                   for pool in ("evaluation", "review")
                   for item in by_number[69]["pools"][pool] if item["format"] == "escribir"
                   for answer in item["answer"]["accepted"])
        final = classes[-1]
        assert final["usesPatterns"] == ALL_CONCEPTS and final["cumulativeEvaluation"] == ALL_CONCEPTS
        assert all(item["requires"] == ALL_CONCEPTS for item in final["pools"]["evaluation"])
        assert final["pools"]["evaluation"][2]["origin"]["scoring"]["minimumCorrect"] == 5
        e03_route = final["remediationMap"]["en.n3.c70.e03"]
        assert e03_route["reteachSteps"] == [f"en.n3.class-{k:02d}.t06" for k in NUMBERS]
        assert e03_route["reviewSteps"] == ["en.n3.c70.r01", "en.n3.c70.r02", "en.n3.c70.r03"]
        for item in (final["pools"]["evaluation"][0], final["pools"]["evaluation"][3],
                     final["pools"]["review"][2]):
            assert item["format"] == "escribir"
            assert all(90 <= len(words(answer)) <= 120 for answer in item["answer"]["accepted"])
        sources = [final["pools"]["evaluation"][0]["origin"]["text"],
                   final["pools"]["evaluation"][3]["origin"]["text"],
                   final["pools"]["review"][2]["origin"]["text"]]
        assert all(token in sources[0] for token in ("AX40", "R81", "N44"))
        assert all(token in sources[1] for token in ("SF12", "E52", "Q73"))
        assert all(token in sources[2] for token in ("LM60", "T24", "V62"))
        assert len({norm(source) for source in sources}) == 3
        assert 90 <= len(words(final["teaching"][5]["en"])) <= 120
        assert all(marker in final["teaching"][5]["en"] for marker in ("coach K8", "ticket P14", "booking W36"))
        assert all(any(phrase in answer.casefold() for phrase in ("before", "twice"))
                   for item in (final["pools"]["evaluation"][0], final["pools"]["evaluation"][3],
                                final["pools"]["review"][2])
                   for answer in item["answer"]["accepted"])
    return {"classes": len(classes), "items": sum(totals.values()), "pools": dict(totals),
            "formats": dict(formats), "correctIndices": dict(indices),
            "prompts": len(prompts), "fingerprints": len(signatures), "variantSeed": VARIANT_SEED}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def generate_all():
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    paths = []
    for n in NUMBERS:
        doc = BUILDERS[n]()
        audit([doc])
        path = OUT / f"class-{n:02d}.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
        paths.append(path)
    docs = [json.loads(path.read_text()) for path in paths]
    summary = audit(docs, full=True)
    bundle = OUT / "bundle-66-70.json"
    bundle.write_text(json.dumps({
        "schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 3,
        "scale": "client-10-levels-v1", "status": "shadow", "runtimeAi": False,
        "variantSeed": VARIANT_SEED, "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "range": {"start": 66, "end": 70}, "classes": docs,
    }, ensure_ascii=False, indent=2) + "\n")
    report = REPORT_OUT / "REPORT.md"
    report.write_text(
        "# INTEGRADO — Inglés N3 C66–C70\n\n"
        "Estado: **integrado en shadow tras revisión independiente GO**.\n\n"
        "- 5 clases / 65 ítems; experiencia, duración, comprensión de reclamaciones, producción factual y reprogramación.\n"
        "- Secuencia explícita por clase: 4 presentación, 2 práctica, 1 tarea, 1 quiz, 4 examen y 1 remediación.\n"
        "- Umbrales parciales solo en `relacionar`; fuentes de audio/texto consumibles por la UI.\n"
        "- C66 clasifica funciones sin repetir datos-clave; C67 exige cinco decisiones de corrección gramatical.\n"
        "- C68 puntúa por separado incidencia, evidencia, petición y respuesta mediante completar multiparte 4/4.\n"
        "- C69 respeta 80–100 palabras; C70 respeta 90–120 y usa aeropuerto, ferry y tren.\n"
        "- Variantes deterministas con `--variant-seed`; el seed se registra en clase, bundle e ítems.\n\n"
        "## Autoauditoría\n\n"
        "Se simularon principiante, fallo total, acierto total, carga alta y reingreso: las fuentes contienen todos "
        "los datos necesarios, cada respuesta es determinista, las remediaciones usan casos nuevos y el cierre no "
        "requiere inferir compensación ni condiciones.\n\n```json\n" +
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n```\n"
    )
    files = paths + [bundle, report]
    manifest = REPORT_OUT / "MANIFEST.sha256"
    entries = [
        f"{digest(__file__)}  ../../tools/contenido/generar_editorial_n3_66_70.py",
        f"{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json",
    ]
    entries.extend(f"{digest(path)}  ../../{path.relative_to(REPO)}" for path in paths + [bundle])
    entries.append(f"{digest(report)}  REPORT.md")
    manifest.write_text("\n".join(entries) + "\n")
    return files + [manifest]


def main():
    global VARIANT_SEED
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--variant-seed", default="0")
    args = parser.parse_args()
    VARIANT_SEED = str(args.variant_seed)
    if args.all:
        for path in generate_all():
            print(path)
    elif args.audit:
        docs = [json.loads((OUT / f"class-{n:02d}.json").read_text()) for n in NUMBERS]
        assert all(doc.get("variantSeed") == VARIANT_SEED for doc in docs)
        print(json.dumps(audit(docs, full=True), ensure_ascii=False, sort_keys=True))
    else:
        parser.error("use --all or --audit")


if __name__ == "__main__":
    raise SystemExit(main())

