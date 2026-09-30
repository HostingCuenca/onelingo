#!/usr/bin/env python3
"""Generate the integrated English N3 C41-C45 editorial shadow block."""
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
REPORT_OUT = ROOT / "build/editorial-n3-41-45"
_MAP_CANDIDATES = (
    ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json",
    Path("/home/roggrt/Documents/onelingo/assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"),
)
MAP = next((path for path in _MAP_CANDIDATES if path.exists()), _MAP_CANDIDATES[0])
NUMBERS = range(41, 46)
CONCEPTS = {n: f"n3-processes-services-{n - 40}" for n in NUMBERS}
PHASES = {41: "input", 42: "form", 43: "comprehension", 44: "production", 45: "transfer"}
SCALE = "client-10-levels-v1"
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


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text: str) -> str:
    return " ".join(re.findall(r"[a-záéíóúüñ0-9']+", text.casefold()))


def hashed(item: dict[str, Any]) -> dict[str, Any]:
    payload = {k: v for k, v in item.items() if k not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return item


def base(item_id: str, fmt: str, prompt: str, concept: str, pool: str, feedback: str,
         *, requires: list[str] | None = None, hint: str | None = None,
         scoring: dict[str, Any] | None = None) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": hint or "Identifica el elemento afectado y la forma verbal."}
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
    item = base(item_id, "completar", prompt, concept, pool, feedback, **kwargs)
    item["answer"] = {"text": answer, "accepted": [answer]}
    return hashed(item)


def multi_fill(item_id: str, prompt: str, sentences: list[str], answers: list[str],
               concept: str, pool: str, feedback: str, *, scoring: dict[str, Any],
               source: str | None = None, **kwargs: Any) -> dict[str, Any]:
    item = base(item_id, "completar", prompt, concept, pool, feedback,
                scoring=scoring, **kwargs)
    item["origin"]["sentences"] = sentences
    if source:
        item["origin"]["text"] = source
    joined = " | ".join(answers)
    item["answer"] = {"text": joined, "accepted": [joined],
                      "parts": [{"text": value,
                                  "accepted": [value, value.replace(" / ", "; ")]}
                                for value in answers]}
    return hashed(item)


def order(item_id: str, prompt: str, answer: str, concept: str, pool: str,
          feedback: str, **kwargs: Any) -> dict[str, Any]:
    item = base(item_id, "ordenar", prompt, concept, pool, feedback, **kwargs)
    item["answer"] = {"text": answer, "tokens": answer.split()}
    return hashed(item)


def match(item_id: str, prompt: str, pairs: list[tuple[str, str]], concept: str,
          pool: str, feedback: str, **kwargs: Any) -> dict[str, Any]:
    item = base(item_id, "relacionar", prompt, concept, pool, feedback, **kwargs)
    values = [[left, {"es": right}] for left, right in pairs]
    item["answer"] = {"pairs": values}
    item["origin"]["pairs"] = values
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
            "id": f"en.n3.class-{n:02d}.t{index:02d}",
            "en": english,
            "es": spanish,
            "explanationEs": explanation,
            "segments": [
                {"en": " ".join(en_words[:en_mid]), "es": " ".join(es_words[:es_mid])},
                {"en": " ".join(en_words[en_mid:]), "es": " ".join(es_words[es_mid:])},
            ],
            "audioText": english,
            "audioMode": "tts",
            "languageCode": "en",
            "patternId": CONCEPTS[n],
        })
    return result


def make_class(n: int, objectives: list[str], vocabulary: list[tuple[str, str]],
               teaching_rows: list[tuple[str, str, str]],
               pools: dict[str, list[dict[str, Any]]],
               remap: dict[str, tuple[str, str]], *, cumulative: bool = False) -> dict[str, Any]:
    if n == 45:
        vocabulary = [*vocabulary, ("stage", "etapa")]
    spec = json.loads(MAP.read_text(encoding="utf-8"))["classes"][n - 1]
    expected_prerequisite = f"en.n3.class-{n - 1:02d}"
    assert spec["phase"] == PHASES[n]
    assert spec["concepts"] == [CONCEPTS[n]]
    assert spec["prerequisites"] == [expected_prerequisite]
    all_concepts = [CONCEPTS[k] for k in NUMBERS]
    doc: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1",
        "course": "en", "level": 3, "cefr": "B1", "scale": SCALE,
        "status": "shadow", "runtimeAi": False, "phase": PHASES[n],
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY),
        "id": f"en.n3.class-{n:02d}", "title": spec["title"],
        "objectives": {"es": objectives}, "concepts": [CONCEPTS[n]],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [expected_prerequisite],
        "usesVocabulary": [english for english, _ in vocabulary],
        "usesPatterns": all_concepts if cumulative else [CONCEPTS[n]],
        "vocabulary": [{"en": english, "es": spanish} for english, spanish in vocabulary],
        "teaching": teaching(n, teaching_rows), "pools": pools,
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


def build_41() -> dict[str, Any]:
    n, c, p = 41, CONCEPTS[41], "en.n3.c41"
    score = {"unit": "process-analysis", "total": 5, "minimumCorrect": 4,
             "criteria": ["be-participle", "process-result", "agent-status"]}
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "¿Qué oración centra el resultado de un servicio?",
                   ["The assistant prints each card.", "Customers wait beside the desk.",
                    "Each card is printed after payment."], 2, c, "practiceGuided",
                   "Is printed presenta el resultado sobre card sin exigir un agente.",
                   hint="Busca be + participio y el elemento afectado."),
            fill(f"{p}.pg02", "Completa: Parcels ___ weighed before delivery.", "are", c,
                 "practiceGuided", "Are concuerda con parcels y precede a weighed.",
                 hint="El sujeto parcels es plural."),
            order(f"{p}.pg03", "Ordena el resultado del proceso de lavado.",
                  "The uniforms are washed every evening.", c, "practiceGuided",
                  "Are washed forma present passive y uniforms recibe la acción.",
                  hint="Coloca are antes del participio washed."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige qué resultado se destaca.",
                   "At this pharmacy, prescriptions are checked before medicine is given out.",
                   ["Prescriptions receive a check", "The pharmacy changes its address",
                    "Customers check the pharmacist"], 0, c, "practice",
                   "Are checked centra el resultado de revisar las recetas."),
            match(f"{p}.p02", "Une cada pasiva con el resultado del proceso.",
                  [("Tickets are scanned at the gate.", "tickets receive a scan"),
                   ("Fresh bread is packed at noon.", "bread is put into packages"),
                   ("Rooms are cleaned after checkout.", "rooms receive cleaning")],
                  c, "practice", "Cada sujeto recibe la acción expresada por be + participio."),
            write(f"{p}.p03", "Explica el resultado y si aparece el agente.",
                  "The water is tested every Monday.",
                  "Result: the water receives a test every Monday. Agent: not stated.",
                  "The water is the affected result; it is tested weekly, and no agent is named.",
                  c, "practice", "Ambas respuestas distinguen resultado y ausencia de agente."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "¿Cuál es el resultado en The forms are stored online?",
                   ["Someone stores the office", "The forms are kept online", "Online staff fill forms"],
                   1, c, "evaluation", "The forms es el sujeto afectado y are stored expresa el resultado."),
            listen(f"{p}.e02", "Escucha y elige el análisis correcto.",
                   "Customer names are removed before the survey results are shared.",
                   ["Customers remove the survey", "The agent is every customer",
                    "Names receive removal; the agent is not stated"], 2, c, "evaluation",
                   "Are removed muestra el resultado sobre names y no nombra a quien actúa."),
            choose(f"{p}.e03", "¿Qué grupo forma present passive?",
                   ["is collected", "has collected", "will collect"], 0, c, "evaluation",
                   "Is collected combina be en presente con el participio collected."),
            multi_fill(f"{p}.e04", "Escribe pasiva, resultado y agente; sepáralos con barras.",
                  ["The parcels are labelled by the clerk. Passive ___ / result ___ / agent ___.",
                   "The keys are copied at the desk. Passive ___ / result ___ / agent ___.",
                   "The soup is prepared in the kitchen. Passive ___ / result ___ / agent ___.",
                   "The windows are cleaned by a contractor. Passive ___ / result ___ / agent ___.",
                   "The bicycles are checked by mechanics. Passive ___ / result ___ / agent ___."],
                  ["are labelled / parcels / clerk", "are copied / keys / not stated",
                   "is prepared / soup / not stated", "are cleaned / windows / contractor",
                   "are checked / bicycles / mechanics"],
                  c, "evaluation", "Cada análisis identifica la pasiva, el resultado y si el agente está expresado.",
                  scoring=score),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué sujeto recibe la acción en The batteries are tested?",
                   ["The tester", "The batteries", "The test room"], 1, c, "review",
                   "The batteries recibe la acción expresada por are tested."),
            multi_fill(f"{p}.r02", "Recupera pasiva, resultado y agente; sepáralos con barras.",
                  ["Library cards are issued by receptionists. Passive ___ / result ___ / agent ___.",
                   "The floor is polished each night. Passive ___ / result ___ / agent ___.",
                   "Samples are examined by a technician. Passive ___ / result ___ / agent ___.",
                   "Orders are confirmed by email. Passive ___ / result ___ / agent ___.",
                   "The bins are emptied by the caretaker. Passive ___ / result ___ / agent ___."],
                  ["are issued / library cards / receptionists", "is polished / floor / not stated",
                   "are examined / samples / technician", "are confirmed / orders / not stated",
                   "are emptied / bins / caretaker"],
                  c, "review", "La recuperación identifica forma, resultado y agente en cinco pasivas nuevas.",
                  scoring=score),
            order(f"{p}.r03", "Ordena una pasiva sobre un servicio diario.",
                  "The counters are disinfected every morning.", c, "review",
                  "Are disinfected describe el resultado habitual sobre counters."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-41.t02", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-41.t04", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-41.t03", f"{p}.r03"),
             f"{p}.e04": ("en.n3.class-41.t06", f"{p}.r02")}
    return make_class(n,
        ["Reconocer present passive en servicios habituales.",
         "Distinguir agente y resultado en cinco descripciones."],
        [("process", "proceso"), ("result", "resultado"), ("agent", "agente"),
         ("label", "etiquetar"), ("check", "revisar"), ("prepare", "preparar")],
        [("A process describes how a result is produced.",
          "Un proceso describe cómo se produce un resultado.", "La pasiva centra el elemento afectado."),
         ("The result comes before the passive verb.",
          "El resultado aparece antes del verbo pasivo.", "Ese sujeto recibe la acción."),
         ("Present passive in a process uses am, is or are plus a participle.",
          "La pasiva presente usa am, is o are más participio.", "La forma de be concuerda con el sujeto."),
         ("The agent can be omitted when it is unknown or unimportant.",
          "El agente puede omitirse cuando no se conoce o no importa.", "By introduce al agente solo si es útil."),
         ("Staff print each label; in passive, orders are checked and meals are prepared.",
          "Se imprimen etiquetas, se revisan pedidos y se preparan comidas.", "Printed, checked y prepared son participios."),
         ("In five descriptions, find be plus participle, name the result and state whether an agent is given. Four complete analyses meet the target.",
          "En cinco descripciones, localiza la pasiva, el resultado y el agente.",
          "La tarea integrada exige tres datos por descripción y cuatro análisis correctos.")],
        pools, remap)


def build_42() -> dict[str, Any]:
    n, c, p = 42, CONCEPTS[42], "en.n3.c42"
    score = {"unit": "service-notice", "total": 6, "minimumCorrect": 5,
             "criteria": ["affected-subject", "was-or-were", "past-participle"]}
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Elige la pasiva para una reparación terminada.",
                   ["They repair the lift.", "The lift was repaired yesterday.",
                    "The lift is repairing yesterday."], 1, c, "practiceGuided",
                   "Was repaired expresa una acción terminada sobre lift.",
                   hint="Busca was/were + participio."),
            fill(f"{p}.pg02", "Completa: The lights ___ replaced on Tuesday.", "were", c,
                 "practiceGuided", "Were concuerda con lights y forma la pasiva pasada.",
                 hint="El sujeto afectado es plural."),
            order(f"{p}.pg03", "Ordena el aviso de una puerta reparada.",
                  "The back door was fixed this morning.", c, "practiceGuided",
                  "Was fixed mantiene door como sujeto afectado.",
                  hint="Coloca was delante de fixed."),
        ],
        "practice": [
            match(f"{p}.p01", "Une sujetos con avisos terminados.",
                  [("The taps", "were replaced last week"),
                   ("The heating", "was tested on Monday"),
                   ("The chairs", "were delivered yesterday")], c, "practice",
                  "Was acompaña al singular y were a los plurales antes del participio."),
            listen(f"{p}.p02", "Escucha y elige el aviso correcto.",
                   "The two damaged screens were removed after the inspection.",
                   ["The inspection was removed", "The screens remove damage",
                    "The screens were removed"], 2, c, "practice",
                   "Were removed concuerda con screens y comunica el cambio terminado."),
            write(f"{p}.p03", "Convierte el registro en un aviso pasivo.",
                  "Tuesday: staff cleaned the storage room.",
                  "The storage room was cleaned on Tuesday.",
                  "On Tuesday, the storage room was cleaned.", c, "practice",
                  "Las variantes conservan room + was + cleaned y la fecha dada."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Completa: The faulty cable ___ removed at noon.",
                   ["was", "were", "is"], 0, c, "evaluation",
                   "Was concuerda con cable y sitúa la retirada en el pasado."),
            listen(f"{p}.e02", "Escucha y selecciona la forma exacta.",
                   "The booking records were updated after the system check.",
                   ["was updated", "were updated", "were update"], 1, c, "evaluation",
                   "Records exige were y updated aporta el participio correcto."),
            choose(f"{p}.e03", "¿Qué aviso mantiene packages como sujeto afectado?",
                   ["Staff delivered the packages.", "The packages was delivered.",
                    "The packages were delivered."], 2, c, "evaluation",
                   "The packages were delivered mantiene sujeto plural, were y participio."),
            multi_fill(f"{p}.e04", "Redacta seis avisos pasivos desde las notas.",
                  ["window · replace · Monday → ___", "forms · check · yesterday → ___",
                   "alarm · test · Friday → ___", "rooms · paint · June → ___",
                   "parcel · collect · noon → ___", "keys · return · Tuesday → ___"],
                  ["The window was replaced on Monday.", "The forms were checked yesterday.",
                   "The alarm was tested on Friday.", "The rooms were painted in June.",
                   "The parcel was collected at noon.", "The keys were returned on Tuesday."],
                  c, "evaluation", "Cada producción conserva sujeto afectado, was/were, participio y tiempo.",
                  scoring=score),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué forma completa The sign ___ installed yesterday?",
                   ["was", "were", "has"], 0, c, "review",
                   "Was installed concuerda con sign y describe una instalación terminada."),
            order(f"{p}.r02", "Ordena un aviso sobre varias mesas.",
                  "The tables were moved after lunch.", c, "review",
                  "Were moved forma la pasiva pasada con un sujeto plural."),
            multi_fill(f"{p}.r03", "Recupera seis avisos pasivos desde notas nuevas.",
                  ["gate · lock · 8 pm → ___", "invoices · send · Monday → ___",
                   "roof · inspect · March → ___", "computers · restart · noon → ___",
                   "badge · issue · Friday → ___", "shelves · build · May → ___"],
                  ["The gate was locked at 8 pm.", "The invoices were sent on Monday.",
                   "The roof was inspected in March.", "The computers were restarted at noon.",
                   "The badge was issued on Friday.", "The shelves were built in May."],
                  c, "review", "La recuperación produce seis pasivas con concordancia y participio adecuados.",
                  scoring=score),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-42.t02", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-42.t03", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-42.t04", f"{p}.r02"),
             f"{p}.e04": ("en.n3.class-42.t06", f"{p}.r03")}
    return make_class(n,
        ["Formar past passive para cambios y reparaciones terminadas.",
         "Completar seis avisos con al menos cinco formas correctas."],
        [("repair", "reparación"), ("notice", "aviso"), ("affected", "afectado"),
         ("replace", "reemplazar"), ("deliver", "entregar"), ("return", "devolver")],
        [("A finished repair can be reported in past passive.",
          "Una reparación terminada puede comunicarse en pasiva pasada.", "El objeto afectado encabeza el aviso."),
         ("Use was with one affected subject.", "Usa was con un sujeto afectado singular.", "The gate was locked."),
         ("Use were with plural affected subjects.", "Usa were con sujetos afectados plurales.", "The lights were replaced."),
         ("In each notice, keep the past participle after was or were.",
          "Mantén el participio después de was o were.", "Delivered y built no cambian por número."),
         ("A repair date or time shows when the change was completed.",
          "Una fecha u hora muestra cuándo terminó el cambio.", "El dato temporal debe conservarse."),
         ("Complete six notices from subject, action and time notes. Each needs the affected subject, was or were, and the correct participle; five complete notices meet the target.",
          "Completa seis avisos desde notas de sujeto, acción y tiempo.",
          "La evidencia integrada comprueba concordancia, participio y dato temporal.")],
        pools, remap)


def build_43() -> dict[str, Any]:
    n, c, p = 43, CONCEPTS[43], "en.n3.c43"
    score = {"unit": "status-record", "total": 6, "minimumCorrect": 5,
             "requiredParts": [4, 5],
             "criteria": ["four-stages-in-order", "current-status", "closing-date"]}
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "¿Qué etapa ocurre primero en una solicitud?",
                   ["The repair is confirmed", "The item is repaired", "The request is received"],
                   2, c, "practiceGuided", "La recepción de la solicitud inicia el proceso.",
                   hint="Busca la entrada del caso antes de cualquier revisión."),
            order(f"{p}.pg02", "Ordena cuatro etapas de una reparación.",
                  "The request was received. The item was inspected. It was repaired. Completion was confirmed.",
                  c, "practiceGuided", "Recepción, revisión, reparación y confirmación forman la secuencia.",
                  hint="La confirmación solo aparece después de la reparación."),
            fill(f"{p}.pg03", "Completa: The device ___ now being tested.", "is", c,
                 "practiceGuided", "Is being tested marca la etapa actualmente en curso.",
                 hint="Device es singular y el proceso sigue activo."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada registro con su etapa.",
                  [("Request logged at 09:00", "reception"),
                   ("Damage checked at 10:30", "review"),
                   ("New part fitted at 14:00", "repair")], c, "practice",
                  "Logged, checked y fitted sitúan cada acción en el proceso."),
            listen(f"{p}.p02", "Escucha y elige el estado actual.",
                   "The request was received this morning and the printer was inspected. It is now being repaired. Confirmation will be sent tomorrow.",
                   ["The printer is being repaired", "Confirmation was sent yesterday",
                    "The request has not arrived"], 0, c, "practice",
                   "Is now being repaired identifica la etapa vigente entre hechos terminados."),
            write(f"{p}.p03", "Resume estado actual y fecha de cierre.",
                  "Bike received Monday; checked Tuesday; now repaired; closes Thursday.",
                  "The bike is now being repaired, and the request closes on Thursday.",
                  "Repair is the current stage; completion is scheduled for Thursday.",
                  c, "practice", "Las variantes conservan la etapa vigente y el cierre del jueves."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Received, reviewed, repaired, confirmed: ¿qué va tercero?",
                   ["confirmed", "repaired", "received"], 1, c, "evaluation",
                   "Repaired ocupa la tercera posición después de recepción y revisión."),
            listen(f"{p}.e02", "Escucha y selecciona la fecha de cierre.",
                   "The parcel was received on Monday. It is being checked now, and the case will close on 18 July.",
                   ["Monday", "Today", "18 July"], 2, c, "evaluation",
                   "Will close on 18 July indica la fecha final del caso."),
            choose(f"{p}.e03", "¿Qué oración identifica una etapa pendiente?",
                   ["Confirmation has not been sent yet.", "The item was received yesterday.",
                    "The inspection was completed at ten."], 0, c, "evaluation",
                   "Has not been sent yet marca confirmation como pendiente."),
            multi_fill(f"{p}.e04", "Extrae seis datos del registro F18.",
                  ["Stage 1: ___", "Stage 2: ___", "Stage 3: ___", "Stage 4: ___",
                   "Current status: ___", "Closure date: ___"],
                  ["request received on 3 May", "request reviewed on 4 May",
                   "repair in progress", "confirmation planned for 6 May", "repair", "6 May"],
                  c, "evaluation", "La extracción conserva el orden, el estado actual y la fecha final.",
                  scoring=score,
                  source="F18: The request was received on 3 May and reviewed on 4 May. Repair is now in progress. Confirmation is planned for 6 May, when the case will close."),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué dato responde cuál es el estado actual?",
                   ["Received last Friday", "Being inspected now", "Closes next Monday"],
                   1, c, "review", "Being inspected now expresa la etapa que está en curso."),
            order(f"{p}.r02", "Reconstruye una secuencia completa de servicio.",
                  "The form was received. It was reviewed. The change was made. Confirmation was sent.",
                  c, "review", "La secuencia conserva recepción, revisión, acción y confirmación."),
            multi_fill(f"{p}.r03", "Recupera seis datos del registro K7.",
                  ["First stage: ___", "Second stage: ___", "Third stage: ___", "Fourth stage: ___",
                   "Current status: ___", "Closure date: ___"],
                  ["case received on 9 August", "case reviewed on 10 August",
                   "replacement in progress", "confirmation due on 12 August",
                   "replacement", "12 August"],
                  c, "review", "La recuperación extrae cuatro etapas, estado actual y fecha de cierre.",
                  scoring=score,
                  source="K7: The case was received on 9 August and reviewed on 10 August. Replacement is currently in progress. Confirmation is due on 12 August, the closure date."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-43.t02", f"{p}.r02"),
             f"{p}.e02": ("en.n3.class-43.t05", f"{p}.r03"),
             f"{p}.e03": ("en.n3.class-43.t04", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-43.t06", f"{p}.r03")}
    return make_class(n,
        ["Seguir recepción, revisión, reparación y confirmación.",
         "Identificar estado actual y fecha de cierre en un aviso."],
        [("request", "solicitud"), ("stage", "etapa"), ("receive", "recibir"),
         ("review", "revisar"), ("confirmation", "confirmación"), ("closure", "cierre")],
        [("A service request moves through ordered stages.",
          "Una solicitud de servicio avanza por etapas ordenadas.", "El registro permite reconstruir la secuencia."),
         ("Reception records that the request was received.",
          "La recepción registra que la solicitud fue recibida.", "Es la primera etapa."),
         ("Review checks the item before repair.",
          "La revisión comprueba el objeto antes de repararlo.", "La reparación depende de la revisión."),
         ("The current stage tells what is happening now.",
          "El estado actual indica qué ocurre ahora.", "Now, currently y pending ayudan a localizarlo."),
         ("The closing date tells when confirmation is completed.",
          "La fecha de cierre indica cuándo termina la confirmación.", "No la confundas con la recepción."),
         ("Read one notice, order reception, review, repair and confirmation, then report the current status and closing date. Keep every date attached to its stated stage.",
          "Ordena cuatro etapas y comunica el estado actual y la fecha de cierre.",
          "La tarea integrada evita inventar etapas o mover fechas entre acciones.")],
        pools, remap)


def build_44() -> dict[str, Any]:
    n, c, p = 44, CONCEPTS[44], "en.n3.c44"
    score = {"unit": "process-explanation", "total": 3, "minimumCorrect": 3,
             "criteria": ["three-passive-stages", "logical-order", "consistent-tense"]}
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Elige una secuencia pasiva y lógica.",
                   ["The form is collected, checked and returned.",
                    "The form collects, is checking and returned.",
                    "The form is returned before it is received."], 0, c, "practiceGuided",
                   "La primera opción mantiene tres etapas pasivas en orden posible.",
                   hint="Comprueba forma verbal y orden de las acciones."),
            order(f"{p}.pg02", "Ordena tres etapas para gestionar un abrigo.",
                  "The coat is collected. It is inspected. It is returned.", c, "practiceGuided",
                  "La recogida precede a la inspección y la devolución.",
                  hint="Empieza cuando el servicio recibe el objeto."),
            fill(f"{p}.pg03", "Completa: First, the request ___ recorded.", "is", c,
                 "practiceGuided", "Is recorded mantiene el presente pasivo del proceso.",
                 hint="Request es singular y el proceso es habitual."),
        ],
        "practice": [
            match(f"{p}.p01", "Une conectores con etapas de un préstamo.",
                  [("First", "the device is collected"), ("Next", "it is inspected"),
                   ("Finally", "it is returned")], c, "practice",
                  "Los conectores hacen visible el orden lógico de las tres pasivas."),
            listen(f"{p}.p02", "Escucha y elige el tiempo verbal coherente.",
                   "This is our usual process: each sample is received, is tested and is stored.",
                   ["past active", "present passive", "future passive"], 1, c, "practice",
                   "Las tres formas is + participio describen un proceso habitual."),
            write(f"{p}.p03", "Explica tres etapas de una solicitud habitual.",
                  "collect at desk; check details; return by email",
                  "First, the request is collected at the desk. Next, its details are checked. Finally, a response is returned by email.",
                  "The request is first received at the desk, then its details are reviewed, and finally the answer is sent by email.",
                  c, "practice", "Las variantes conservan tres etapas pasivas y un solo marco temporal."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "¿Qué etapa sigue a The parcel is collected?",
                   ["It was delivered last year.", "Customers collect a receipt.",
                    "It is checked for damage."], 2, c, "evaluation",
                   "La revisión del daño es la siguiente etapa lógica del proceso actual."),
            listen(f"{p}.e02", "Escucha y elige la secuencia coherente.",
                   "The application is received, its details are verified, and the result is sent.",
                   ["receive, verify, send", "send, receive, verify", "verify, send, receive"],
                   0, c, "evaluation", "La secuencia avanza de recepción a verificación y envío."),
            choose(f"{p}.e03", "¿Qué opción mantiene present passive en tres etapas?",
                   ["is logged, was checked, sends", "is logged, is checked, is closed",
                    "logs, checks, closes"], 1, c, "evaluation",
                   "Is logged, is checked, is closed conserva la pasiva presente."),
            write(f"{p}.e04", "Describe en 70–90 palabras cómo se gestionan libros donados.",
                  "Habitual: recoger en recepción; revisar estado; clasificar por tema; entregar a biblioteca escolar. Agente desconocido.",
                  "First, donated books are collected at reception. Next, each book is checked for damage, so unsuitable copies are separated. The usable books are then sorted by subject and placed in labelled boxes. Finally, the boxes are delivered to the school library. The same present passive is used throughout because this is the usual process and the staff member is not important. The four stages follow the order given: collection, review, sorting and delivery.",
                  "Donated books are first received at the front desk. Their condition is then reviewed, and damaged copies are separated. After that, suitable books are organised by subject and packed in labelled boxes. In the final stage, the boxes are taken to the school library. The process stays in present passive because it happens regularly and no agent is named. This order clearly moves from collection and checking to classification and delivery.",
                  c, "evaluation", "Ambas explicaciones usan etapas pasivas ordenadas y presente coherente.",
                  scoring=score),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué cierre mantiene la pasiva del proceso?",
                   ["Finally, staff return it.", "Finally, it returning.",
                    "Finally, it is returned."], 2, c, "review",
                   "It is returned conserva el sujeto afectado y present passive."),
            order(f"{p}.r02", "Ordena una gestión completa en pasado.",
                  "The device was collected. It was tested. It was delivered.", c, "review",
                  "Las tres etapas usan past passive y siguen un orden funcional."),
            write(f"{p}.r03", "Recupera en 70–90 palabras el proceso de una tarjeta perdida.",
                  "Terminado ayer: formulario recibido; identidad revisada; tarjeta desactivada; reemplazo enviado. Agente no indicado.",
                  "Yesterday, the lost-card form was received through the service portal. The account holder's identity was then checked against the submitted details. After the review was completed, the missing card was deactivated to prevent further use. Finally, a replacement card was sent to the registered address. Past passive is maintained across the four stages because the process finished yesterday and the agent is not given. The sequence moves logically from reception and review to deactivation and delivery.",
                  "The lost-card request was received online yesterday. Next, the customer's identity was verified from the information on the form. Once that review was complete, the old card was deactivated. A replacement was finally delivered to the registered address. Every stage is expressed in past passive because the whole process is finished and no agent is named. The explanation follows the stated order: receiving the request, checking identity, disabling the card and sending its replacement.",
                  c, "review", "La recuperación conserva los hechos dados, el orden y la pasiva pasada.",
                  scoring=score),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-44.t02", f"{p}.r02"),
             f"{p}.e02": ("en.n3.class-44.t04", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-44.t03", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-44.t06", f"{p}.r03")}
    return make_class(n,
        ["Explicar un proceso breve sin repetir un agente desconocido.",
         "Conectar tres o más etapas pasivas en 70–90 palabras."],
        [("handle", "gestionar"), ("collect", "recoger"), ("inspect", "revisar"),
         ("sort", "clasificar"), ("return", "devolver"), ("stage", "etapa")],
        [("Explain how staff handle an object or request.",
          "Explica cómo se gestiona un objeto o solicitud.", "La pasiva evita repetir un agente desconocido."),
         ("Start when staff collect the object or receive the request.",
          "Empieza con recogida o recepción.", "La entrada inicia el proceso."),
         ("Use one passive tense consistently at every stage.",
          "Usa un tiempo pasivo de forma coherente.", "El proceso habitual usa presente; el terminado, pasado."),
         ("Connect each stage in logical order.",
          "Conecta cada etapa en orden lógico.", "First, next y finally hacen visible la secuencia."),
         ("Include review before return or delivery.",
          "Incluye la revisión antes de devolución o entrega.", "La revisión decide cómo continúa el objeto."),
         ("First, reusable containers are collected from the café counter. Next, each container is inspected for cracks, and damaged ones are separated. The safe containers are then washed and dried. Finally, they are returned to the serving area for the next day. Present passive is kept through the explanation because this is the usual process and no agent is identified. The stages remain clear: collection, inspection, cleaning and return, in that logical order.",
          "El modelo explica la recogida, revisión, limpieza y devolución habitual de recipientes.",
          "Cuatro etapas pasivas, orden lógico y presente coherente satisfacen la tarea.")],
        pools, remap)


def build_45() -> dict[str, Any]:
    n, c, p = 45, CONCEPTS[45], "en.n3.c45"
    all_concepts = [CONCEPTS[k] for k in NUMBERS]
    score = {"unit": "service-resolution", "total": 5, "minimumCorrect": 5,
             "criteria": ["present-passive", "past-passive", "ordered-stages",
                          "pending-status", "specific-request"]}
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "¿Qué dato identifica una etapa pendiente?",
                   ["The request was received on Monday.", "Delivery is still being arranged.",
                    "The parcel was checked at noon."], 1, c, "practiceGuided",
                   "Still being arranged marca delivery como etapa actual pendiente.",
                   hint="Busca still, pending o not yet."),
            fill(f"{p}.pg02", "Completa: The item ___ being tested now.", "is", c,
                 "practiceGuided", "Is being tested expresa una acción pasiva en curso.",
                 hint="Item es singular y now señala el presente."),
            order(f"{p}.pg03", "Ordena una petición concreta sobre confirmación.",
                  "Please confirm when the collection will be arranged.", c, "practiceGuided",
                  "La petición pregunta por la etapa pendiente collection.",
                  hint="Empieza con Please confirm y nombra la acción pendiente."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada dato con su función en la consulta.",
                  [("The case was opened yesterday.", "finished action"),
                   ("The replacement is being prepared.", "current action"),
                   ("Please confirm the dispatch date.", "specific request")], c, "practice",
                  "Los tres datos separan pasado terminado, presente en curso y petición."),
            listen(f"{p}.p02", "Escucha y selecciona la etapa aún pendiente.",
                   "The phone was inspected and the screen was replaced. Final testing is being completed, but collection has not been arranged.",
                   ["screen replacement", "phone inspection", "collection"], 2, c, "practice",
                   "Has not been arranged identifica collection como pendiente."),
            write(f"{p}.p03", "Formula una petición sobre la etapa pendiente.",
                  "Registro: revisión terminada; reembolso aún no enviado.",
                  "The review was completed. The refund has not been sent; please confirm when it will be issued.",
                  "The case was reviewed, but the refund is still pending. Please give me its issue date.",
                  c, "practice", "Las variantes nombran el hecho terminado, el pendiente y una solicitud concreta."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "¿Qué oración expresa una acción actual en pasiva?",
                   ["The laptop is being tested now.", "The laptop was tested yesterday.",
                    "A technician tests laptops."], 0, c, "evaluation",
                   "Is being tested now sitúa la acción pasiva en curso."),
            listen(f"{p}.e02", "Escucha y elige la acción ya terminada.",
                   "The repair request was received on 8 April. A new battery is being fitted, and the final check is still pending.",
                   ["The final check", "The request was received", "The battery fitting"],
                   1, c, "evaluation", "Was received marca la acción concluida el 8 April."),
            choose(f"{p}.e03", "¿Qué petición corresponde a delivery not arranged?",
                   ["Why was the item inspected?", "Who designed the product?",
                    "Please confirm when delivery will be arranged."], 2, c, "evaluation",
                   "La tercera opción solicita exactamente la fecha de gestión de delivery."),
            write(f"{p}.e04", "Resuelve en 80–110 palabras el estado de una reparación.",
                  "Portátil L24: recibido 8 April; diagnóstico 9 April; teclado reemplazado 10 April; prueba final en curso; recogida no programada. Pide fecha y hora de recogida.",
                  "I am checking the status of laptop L24. The request was received on 8 April, the diagnosis was completed on 9 April, and the keyboard was replaced on 10 April. The final test is being carried out now, so that is the current stage. Collection has not been scheduled and remains the only pending step. The order is reception, diagnosis, replacement, testing and collection. Please confirm the date and time when collection will be arranged, so I know when I can receive the repaired laptop.",
                  "Could you update me on laptop L24? Its request was received on 8 April. Diagnosis was finished on 9 April, and the keyboard was replaced on 10 April. A final test is being completed at present. After that, collection is still pending because no appointment is scheduled. The record therefore moves from reception to diagnosis, replacement, testing and collection. Please tell me exactly when collection will be booked and provide its date and time, so I can plan to receive the laptop.",
                  c, "evaluation", "Las respuestas integran pasivas, orden, pendiente y petición sobre recogida.",
                  requires=all_concepts, scoring=score),
        ],
        "review": [
            choose(f"{p}.r01", "¿Qué respuesta identifica estado y acción pendiente?",
                   ["Testing is happening; dispatch still needs a date.",
                    "The service is useful and the office is large.",
                    "A customer bought the item last year."], 0, c, "review",
                   "La primera opción separa testing actual de dispatch aún sin fecha."),
            match(f"{p}.r02", "Reconstruye el registro de una tarjeta nueva.",
                  [("Application was received on 2 June", "reception"),
                   ("Identity was checked on 3 June", "review"),
                   ("Card is being printed now", "current action"),
                   ("Delivery has no date", "pending stage")], c, "review",
                  "Cada dato se vincula con una etapa explícita sin agregar información."),
            write(f"{p}.r03", "Recupera en 80–110 palabras el estado de un paquete.",
                  "Paquete P63: recibido 14 September; dirección revisada 15 September; preparado 16 September; etiqueta se imprime ahora; despacho no confirmado. Pide fecha de despacho.",
                  "I need an update on parcel P63. The order was received on 14 September, the address was checked on 15 September, and the parcel was prepared on 16 September. Its label is being printed now, which is the current action. Dispatch has not been confirmed, so it is the pending stage. The process runs from reception to address review, preparation, labelling and dispatch. Please confirm the exact date when the parcel will be dispatched and tell me when that confirmation will be sent.",
                  "Please check parcel P63 for me. The order was received on 14 September. Its address was reviewed on 15 September, and the parcel was prepared on 16 September. The shipping label is being printed at present. Dispatch is still pending because it has not been confirmed. The ordered stages are reception, review, preparation, labelling and dispatch. Please provide the exact dispatch date and confirm when the parcel will leave, using the existing record rather than adding a new delivery estimate.",
                  c, "review", "La recuperación integra los cinco criterios con un registro distinto.",
                  requires=all_concepts, scoring=score),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-45.t02", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-45.t03", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-45.t05", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-45.t06", f"{p}.r03")}
    return make_class(n,
        ["Resolver un problema de estado desde un registro cerrado.",
         "Pedir acción sobre una etapa pendiente en 80–110 palabras."],
        [("status", "estado"), ("pending", "pendiente"), ("request", "solicitud"),
         ("current", "actual"), ("dispatch", "despacho"), ("confirm", "confirmar")],
        [("Start from the service-status record, not from assumptions.",
          "Parte del registro de estado, no de suposiciones.", "Solo se usan fechas y acciones visibles."),
         ("Use present passive for the current action.",
          "Usa pasiva presente para la acción actual.", "Is being processed señala lo que ocurre ahora."),
         ("Use past passive for a completed status action.",
          "Usa pasiva pasada para una acción terminada.", "Was received recupera el historial."),
         ("Keep each recorded stage in order.",
          "Mantén las etapas registradas en orden.", "El orden revela qué paso debe venir después."),
         ("Name the pending stage and request a concrete action.",
          "Nombra la etapa pendiente y pide una acción concreta.", "La petición debe referirse a ese paso."),
         ("I am asking about suitcase B17. The report was received on 5 March, and the ownership details were checked on 6 March. The suitcase was located on 7 March. It is now being held at the airport service desk. Delivery has not been arranged, so that is the pending stage. The record moves from reception to identity review, location, holding and delivery. Please confirm the exact date and time when delivery will be arranged and tell me when that booking will be sent.",
          "El modelo resuelve un registro de equipaje con acción actual, pasadas, orden, pendiente y petición.",
          "Los cinco conceptos aparecen como evidencia observable en un único mensaje.")],
        pools, remap, cumulative=True)


BUILDERS = {41: build_41, 42: build_42, 43: build_43, 44: build_44, 45: build_45}


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’-]+\b", text))


def get_item(cls: dict[str, Any], pool: str, suffix: str) -> dict[str, Any]:
    return next(item for item in cls["pools"][pool] if item["id"].endswith(suffix))


def assert_scoring(item: dict[str, Any], total: int, passed: int) -> None:
    scoring = item["origin"]["scoring"]
    assert scoring["total"] == total and scoring["minimumCorrect"] == passed
    assert scoring["criteria"]


def audit(classes: list[dict[str, Any]], full: bool) -> dict[str, Any]:
    totals: Counter[str] = Counter()
    formats: Counter[str] = Counter()
    indices: Counter[int] = Counter()
    prompts: dict[str, str] = {}
    fingerprints: dict[str, str] = {}
    for cls in classes:
        assert cls["status"] == "shadow" and cls["runtimeAi"] is False
        assert cls["phase"] == PHASES[int(cls["id"].split("-")[-1])]
        assert cls["qualityPolicy"] == QUALITY
        assert 6 <= len(cls["vocabulary"]) <= 12 and 4 <= len(cls["teaching"]) <= 6
        local_formats: set[str] = set()
        local_indices: Counter[int] = Counter()
        feedbacks: list[str] = []
        for pool, expected in (("practiceGuided", 3), ("practice", 3),
                               ("evaluation", 4), ("review", 3)):
            assert len(cls["pools"][pool]) == expected
            totals[pool] += expected
            for item in cls["pools"][pool]:
                assert len(item["prompt"]["es"]) <= 90, (item["id"], len(item["prompt"]["es"]))
                payload = {k: v for k, v in item.items() if k not in {"id", "contentHash"}}
                assert item["contentHash"] == "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
                prompt_key = norm(item["prompt"]["es"])
                assert prompt_key not in prompts, (item["id"], prompts.get(prompt_key))
                prompts[prompt_key] = item["id"]
                feedbacks.append(item["origin"]["feedback"]["es"])
                local_formats.add(item["format"])
                formats[item["format"]] += 1
                if pool != "practiceGuided":
                    assert "hint" not in item["origin"]
                if item["format"] in {"elegir", "escuchar"}:
                    assert len(item["choices"]) >= 3
                    index = item["answer"]["index"]
                    assert 0 <= index < len(item["choices"])
                    indices[index] += 1
                    local_indices[index] += 1
                if item["format"] == "escribir":
                    accepted = item["answer"]["accepted"]
                    assert len(accepted) >= 2 and len({norm(text) for text in accepted}) >= 2
                stimulus = item["origin"].get("audio") or item["origin"].get("text") or item["origin"].get("pairs") or item["prompt"]["es"]
                signature = canonical({"stimulus": stimulus, "answer": item["answer"]}).casefold()
                assert signature not in fingerprints, (item["id"], fingerprints.get(signature))
                fingerprints[signature] = item["id"]
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

    if full:
        assert len(classes) == 5 and sum(totals.values()) == 65
        c41, c42, c43, c44, c45 = classes
        for pool in ("evaluation", "review"):
            item = get_item(c41, pool, ".e04" if pool == "evaluation" else ".r02")
            assert item["format"] == "completar" and len(item["answer"]["parts"]) == 5
            assert_scoring(item, 5, 4)
        for pool, suffix in (("evaluation", ".e04"), ("review", ".r03")):
            item = get_item(c42, pool, suffix)
            assert_scoring(item, 6, 5)
            assert item["format"] == "completar" and len(item["answer"]["parts"]) == 6
            part_text = " ".join(part["text"] for part in item["answer"]["parts"]).casefold()
            assert len(re.findall(r"\b(was|were)\b", part_text)) == 6
        for pool, suffix in (("evaluation", ".e04"), ("review", ".r03")):
            item = get_item(c43, pool, suffix)
            assert_scoring(item, 6, 5)
            assert item["format"] == "completar" and len(item["answer"]["parts"]) == 6
            assert item["origin"].get("text")
            text = canonical({"origin": item["origin"], "answer": item["answer"]}).casefold()
            assert all(token in text for token in ("received", "review", "current"))
        for text in (c44["teaching"][-1]["en"],
                     *get_item(c44, "evaluation", ".e04")["answer"]["accepted"],
                     *get_item(c44, "review", ".r03")["answer"]["accepted"]):
            assert 70 <= word_count(text) <= 90, word_count(text)
            passive_count = len(re.findall(r"\b(?:is|are|was|were)\s+(?:\w+ed|sent|given|taken|built)\b", text.casefold()))
            assert passive_count >= 3, (passive_count, text)
        all_concepts = [CONCEPTS[n] for n in NUMBERS]
        assert c45["usesPatterns"] == all_concepts
        assert c45["cumulativeEvaluation"] == all_concepts
        e04 = get_item(c45, "evaluation", ".e04")
        r03 = get_item(c45, "review", ".r03")
        assert e04["requires"] == all_concepts and r03["requires"] == all_concepts
        assert_scoring(e04, 5, 5)
        assert_scoring(r03, 5, 5)
        closure_texts = [c45["teaching"][-1]["en"], *e04["answer"]["accepted"],
                         *r03["answer"]["accepted"]]
        for text in closure_texts:
            lower = text.casefold()
            assert 80 <= word_count(text) <= 110, word_count(text)
            assert re.search(r"\b(is|are) (?:now )?being \w+", lower)
            assert re.search(r"\b(was|were) \w+", lower)
            assert any(token in lower for token in ("pending", "not been arranged", "not been confirmed"))
            assert "please" in lower and any(token in lower for token in ("date", "time", "when"))
        joined = " ".join(closure_texts).casefold()
        assert all(token in joined for token in ("suitcase b17", "laptop l24", "parcel p63"))
        assert len({"suitcase", "laptop", "parcel"}) == 3
    return {
        "classes": len(classes), "items": sum(totals.values()), "pools": dict(totals),
        "formats": dict(sorted(formats.items())), "correctIndices": dict(sorted(indices.items())),
        "prompts": len(prompts), "fingerprints": len(fingerprints),
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
    classes = [json.loads((OUT / f"class-{n:02d}.json").read_text(encoding="utf-8")) for n in NUMBERS]
    summary = audit(classes, True)
    bundle = {
        "schema": "onelingo.editorial.class-bundle.v1",
        "course": "en", "level": 3, "scale": SCALE,
        "status": "shadow", "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "range": {"start": 41, "end": 45}, "classes": classes,
    }
    path = OUT / "bundle-41-45.json"
    path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path, summary


def write_report(paths: list[Path], summary: dict[str, Any]) -> Path:
    hashes = "\n".join(f"{digest(path)}  {path.name}" for path in paths)
    text = f"""# GO — Inglés N3 C41–C45

Estado: **GO independiente; integrado en shadow, no autorizado para activación**.

## Cobertura

- Bloque `processes-services`: `input → form → comprehension → production → transfer`.
- Cinco clases, 65 ejercicios, contrato `editorial-agent.v2`, `shadow` y `runtimeAi: false`.
- Las tareas compuestas incluyen `origin.scoring` con unidad, total, umbral y criterios.
- C44 respeta 70–90 palabras; C45 respeta 80–110 palabras.
- C45 usa tres escenarios distintos: equipaje, portátil y paquete.

## Auditoría interna

```json
{json.dumps(summary, ensure_ascii=False, indent=2)}
```

El generador construye el bloque dos veces en memoria, compara la forma canónica y ejecuta
aserciones sustantivas antes de escribir. La entrega fue probada con clases individuales y
bundle level 3, además de dos ejecuciones consecutivas con hashes idénticos.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/contenido/generar_editorial_n3_41_45.py --all
for n in 41 42 43 44 45; do python3 tools/contenido/validar_bundle_editorial.py --file assets/contenido/en/editorial/n3/class-$n.json --start $n --end $n --level 3; done
python3 tools/contenido/validar_bundle_editorial.py --file assets/contenido/en/editorial/n3/bundle-41-45.json --start 41 --end 45 --level 3
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
    memory_summary = verify_in_memory()
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    class_paths = [write_class(n) for n in NUMBERS]
    bundle, summary = write_bundle()
    assert summary == memory_summary
    report = write_report(class_paths + [bundle], summary)
    files = class_paths + [bundle, report]
    manifest = REPORT_OUT / "MANIFEST.sha256"
    entries = [
        f"{digest(Path(__file__))}  ../../tools/contenido/generar_editorial_n3_41_45.py",
        f"{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json",
    ]
    entries.extend(f"{digest(path)}  {path.name if path.parent == REPORT_OUT else '../../' + str(path.relative_to(ROOT))}" for path in files)
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
        docs = [json.loads((OUT / f"class-{n:02d}.json").read_text(encoding="utf-8")) for n in NUMBERS]
        print(json.dumps(audit(docs, True), ensure_ascii=False, sort_keys=True))
    elif args.all:
        for path in write_all():
            print(path)
    else:
        parser.error("choose --class-number, --bundle, --audit or --all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
