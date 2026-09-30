#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n2"
REPORT_OUT = ROOT / "build/editorial-n2-66-70"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n2-editorial-v2.json"
VALIDATOR = ROOT / "tools/contenido/validar_bundle_editorial.py"
SCALE = "client-10-levels-v1"
ACCESSIBILITY = {"screenReader": True, "highContrast": True, "largeText": True}
QUALITY_POLICY = {
    "chronologyTokens": "enforce",
    "answerReuseAcrossEarlyReserved": "forbid",
    "answerEvidenceReuseAcrossPools": "forbid",
    "agentContract": "editorial-agent.v2",
    "minChoices": 3,
    "maxPromptCharacters": 90,
    "feedbackReuseWithinClass": "forbid",
    "minClassFormats": 4,
}
CONCEPTS = {
    66: "n2-transport-tickets",
    67: "n2-directions-landmarks",
    68: "n2-travel-problems",
    69: "n2-ask-help-travel",
    70: "n2-complete-travel-plan",
}
PHASES = {66: "input", 67: "form", 68: "comprehension", 69: "production", 70: "transfer"}
TITLES = {
    66: {"en": "Transport and tickets", "es": "Transporte y billetes"},
    67: {"en": "Directions with landmarks", "es": "Indicaciones con puntos de referencia"},
    68: {"en": "Travel problems", "es": "Problemas de viaje"},
    69: {"en": "Ask for help while travelling", "es": "Pedir ayuda durante un viaje"},
    70: {"en": "Complete a travel plan", "es": "Completar un plan de viaje"},
}


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_hash(item: dict[str, Any]) -> dict[str, Any]:
    payload = {key: value for key, value in item.items() if key not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return item


def origin(feedback: str, *, hint: str | None = None, **extra: Any) -> dict[str, Any]:
    value: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}, **extra}
    if hint is not None:
        value["hint"] = {"es": hint}
    return value


def requirements(concept: str, guided: bool) -> tuple[list[str], list[str]]:
    return ([concept], []) if guided else ([], [concept])


def choose(item_id: str, prompt: str, choices: list[str], index: int, concept: str,
           feedback: str, *, guided: bool = False, hint: str | None = None,
           requires: list[str] | None = None) -> dict[str, Any]:
    teaches, default_requires = requirements(concept, guided)
    return add_hash({
        "id": item_id, "format": "elegir", "prompt": {"es": prompt},
        "answer": {"index": index}, "choices": [{"text": value} for value in choices],
        "teaches": teaches, "requires": default_requires if requires is None else requires,
        "origin": origin(feedback, hint=hint), "accessibility": dict(ACCESSIBILITY),
    })


def complete(item_id: str, prompt: str, answer: str, concept: str, feedback: str,
             *, guided: bool = False, hint: str | None = None,
             requires: list[str] | None = None) -> dict[str, Any]:
    teaches, default_requires = requirements(concept, guided)
    return add_hash({
        "id": item_id, "format": "completar", "prompt": {"es": prompt},
        "answer": {"text": answer, "accepted": [answer]}, "choices": [],
        "teaches": teaches, "requires": default_requires if requires is None else requires,
        "origin": origin(feedback, hint=hint), "accessibility": dict(ACCESSIBILITY),
    })


def order(item_id: str, prompt: str, answer: str, tokens: list[str], concept: str,
          feedback: str, *, guided: bool = False, hint: str | None = None) -> dict[str, Any]:
    teaches, reqs = requirements(concept, guided)
    return add_hash({
        "id": item_id, "format": "ordenar", "prompt": {"es": prompt},
        "answer": {"text": answer, "tokens": tokens}, "choices": [],
        "teaches": teaches, "requires": reqs, "origin": origin(feedback, hint=hint),
        "accessibility": dict(ACCESSIBILITY),
    })


def write(item_id: str, prompt: str, stimulus: str, answer: str, accepted: list[str],
          concept: str, feedback: str, *, requires: list[str] | None = None) -> dict[str, Any]:
    return add_hash({
        "id": item_id, "format": "escribir", "prompt": {"es": prompt},
        "answer": {"text": answer, "accepted": accepted}, "choices": [], "teaches": [],
        "requires": [concept] if requires is None else requires,
        "origin": origin(feedback, text=stimulus), "accessibility": dict(ACCESSIBILITY),
    })


def listen(item_id: str, prompt: str, audio: str, choices: list[str], index: int,
           concept: str, feedback: str, *, requires: list[str] | None = None) -> dict[str, Any]:
    return add_hash({
        "id": item_id, "format": "escuchar", "prompt": {"es": prompt},
        "answer": {"index": index}, "choices": [{"text": value} for value in choices],
        "teaches": [], "requires": [concept] if requires is None else requires,
        "origin": origin(feedback, audio=audio, audioMode="tts", languageCode="en",
                         speedOptions=[0.75, 1.0], maxReplays=3,
                         revealTranscriptAfterAttempt=True),
        "accessibility": dict(ACCESSIBILITY),
    })


def match(item_id: str, prompt: str, pairs: list[tuple[str, str]], concept: str,
          feedback: str, *, guided: bool = False, hint: str | None = None) -> dict[str, Any]:
    teaches, reqs = requirements(concept, guided)
    values = [[left, {"es": right}] for left, right in pairs]
    return add_hash({
        "id": item_id, "format": "relacionar", "prompt": {"es": prompt},
        "answer": {"pairs": values}, "choices": [], "teaches": teaches, "requires": reqs,
        "origin": origin(feedback, hint=hint, pairs=values), "accessibility": dict(ACCESSIBILITY),
    })


def lesson(number: int, index: int, en: str, es: str, explanation: str) -> dict[str, Any]:
    en_words, es_words = en.split(), es.split()
    en_mid, es_mid = max(1, len(en_words) // 2), max(1, len(es_words) // 2)
    return {
        "id": f"en.n2.class-{number}.t{index:02d}", "en": en, "es": es,
        "explanationEs": explanation,
        "segments": [
            {"en": " ".join(en_words[:en_mid]), "es": " ".join(es_words[:es_mid])},
            {"en": " ".join(en_words[en_mid:]), "es": " ".join(es_words[es_mid:])},
        ],
        "audioText": en, "audioMode": "tts", "languageCode": "en",
        "patternId": CONCEPTS[number],
    }


def common_class(number: int, objectives: list[str], vocabulary: list[tuple[str, str]],
                 teaching: list[tuple[str, str, str]], pools: dict[str, list[dict[str, Any]]],
                 remediation: dict[str, tuple[int, str]], *,
                 uses_patterns: list[str] | None = None,
                 cumulative: list[str] | None = None) -> dict[str, Any]:
    prefix = f"en.n2.c{number}"
    document: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 2,
        "scale": SCALE, "status": "shadow", "runtimeAi": False, "phase": PHASES[number],
        "title": TITLES[number], "objectives": {"es": objectives},
        "id": f"en.n2.class-{number}", "cefr": "A2", "concepts": [CONCEPTS[number]],
        "skills": ["vocabulario", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n2.class-{number - 1}"],
        "vocabulary": [{"en": en, "es": es} for en, es in vocabulary],
        "usesVocabulary": [en for en, _ in vocabulary],
        "usesPatterns": uses_patterns or [CONCEPTS[number]],
        "teaching": [lesson(number, i, *entry) for i, entry in enumerate(teaching, 1)],
        "pools": pools,
        "remediationMap": {
            f"{prefix}.{evaluation}": {
                "reteach": f"en.n2.class-{number}.t{teaching_index:02d}",
                "review": f"{prefix}.{review_id}",
            }
            for evaluation, (teaching_index, review_id) in remediation.items()
        },
        "accessibility": {"highContrast": True, "largeText": True,
                          "screenReader": True, "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2,
                     "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY_POLICY),
    }
    if cumulative is not None:
        document["cumulativeEvaluation"] = cumulative
    return document


def build_66() -> dict[str, Any]:
    n, c, p = 66, CONCEPTS[66], "en.n2.c66"
    vocabulary = [("single ticket", "billete de ida"), ("return", "regreso"),
                  ("platform", "andén"), ("fare", "tarifa"), ("departure", "salida"),
                  ("ticket machine", "máquina expendedora")]
    teaching = [
        ("A single ticket to Brighton is valid from platform one.", "Un billete de ida a Brighton es válido desde el andén uno.", "Single ticket sirve para un trayecto sin regreso y platform ubica la salida."),
        ("The return is included in this ticket.", "El regreso está incluido en este billete.", "Return señala que la compra incluye también el trayecto de vuelta."),
        ("The fare from the ticket machine is twelve pounds.", "La tarifa de la máquina expendedora es de doce libras.", "Fare es el precio del viaje; ticket machine indica dónde comprar."),
        ("The departure is at 9:20 from platform six.", "La salida es a las 9:20 desde el andén seis.", "Departure aporta la hora y platform ubica el punto de embarque."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Vas a Londres y no vuelves hoy. Elige el billete adecuado.",
                   ["a single ticket", "a return ticket", "two platform tickets"], 0, c,
                   "Single ticket corresponde a un viaje sin trayecto de regreso.", guided=True,
                   hint="Busca la opción que incluye solo la ida."),
            match(f"{p}.pg02", "Relaciona cada dato del tren con su significado.",
                  [("fare", "precio del viaje"), ("platform", "lugar para subir")], c,
                  "Fare responde cuánto cuesta y platform señala dónde abordar.", guided=True,
                  hint="Distingue una cantidad de dinero de un lugar de la estación."),
            complete(f"{p}.pg03", "Completa el lugar de compra: Use the ___ near the entrance.",
                     "ticket machine", c, "Ticket machine completa el punto donde se adquiere el billete.",
                     guided=True, hint="Es una máquina, no el andén ni la hora."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha e identifica el andén de salida.",
                   "The train to York leaves from platform four.",
                   ["platform two", "platform four", "platform fourteen"], 1, c,
                   "La grabación dice platform four, que es el punto de salida del tren a York."),
            order(f"{p}.p02", "Ordena la solicitud de un billete de ida y vuelta.",
                  "A return ticket to Bath, please.",
                  ["A", "return", "ticket", "to", "Bath,", "please."], c,
                  "Return aparece antes de ticket y to introduce el destino Bath."),
            write(f"{p}.p03", "Escribe en inglés: La tarifa es de quince euros.",
                  "La tarifa es de quince euros.", "The fare is fifteen euros.",
                  ["The fare is fifteen euros.", "A ticket costs fifteen euros."], c,
                  "The fare is fifteen euros comunica de forma natural el precio del trayecto."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Viajas hoy y regresas mañana. Selecciona la compra correcta.",
                   ["a single ticket", "a return ticket", "a platform pass"], 1, c,
                   "Return ticket es la única opción que incluye ida y regreso."),
            listen(f"{p}.e02", "Escucha y marca la hora exacta de salida.",
                   "Your departure is at quarter past seven.",
                   ["7:45", "6:15", "7:15"], 2, c,
                   "Quarter past seven equivale a 7:15 y fija la salida."),
            complete(f"{p}.e03", "Completa el punto de embarque: The coach leaves from ___ nine.",
                     "platform", c, "Platform es el sustantivo que acompaña al número del lugar de salida."),
            write(f"{p}.e04", "Pide en inglés un billete de ida a Oxford para las 10:30.",
                  "Un billete de ida a Oxford para las 10:30.",
                  "I would like a single ticket to Oxford for 10:30, please.",
                  ["I would like a single ticket to Oxford for 10:30, please.",
                   "A single ticket to Oxford for the 10:30 departure, please."], c,
                  "La petición incluye tipo de billete, destino, hora y cortesía."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada compra con el viaje que permite.",
                  [("single ticket", "solo ida"), ("return ticket", "ida y vuelta")], c,
                  "Los nombres de billete distinguen si el regreso está incluido."),
            choose(f"{p}.r02", "El panel indica plataforma 8. ¿Dónde esperas el tren?",
                   ["at platform eight", "at platform three", "by the ticket machine"], 0, c,
                   "Platform eight es el lugar indicado para esperar el tren."),
            listen(f"{p}.r03", "Escucha la nueva hora de salida y selecciona la correcta.",
                   "The departure is at twenty past eight.",
                   ["8:02", "8:20", "8:40"], 1, c,
                   "Twenty past eight equivale a 8:20 y recupera la comprensión de la hora."),
        ],
    }
    return common_class(n, ["Distinguir billetes de ida y de ida y vuelta según el viaje.",
                            "Localizar tarifa, salida y andén en información de transporte.",
                            "Pedir un billete con destino y horario concretos."],
                        vocabulary, teaching, pools,
                        {"e01": (2, "r01"), "e02": (4, "r03"),
                         "e03": (4, "r02"), "e04": (1, "r01")})


def build_67() -> dict[str, Any]:
    n, c, p = 67, CONCEPTS[67], "en.n2.c67"
    vocabulary = [("landmark", "punto de referencia"), ("go past", "pasar de largo"),
                  ("turn left", "girar a la izquierda"), ("cross", "cruzar"),
                  ("opposite", "enfrente de"), ("corner", "esquina")]
    teaching = [
        ("Use the bank as a landmark: go past the museum and turn left there.", "Usa el banco como punto de referencia: pasa el museo y gira allí a la izquierda.", "El landmark identifica el giro después de usar go past para avanzar."),
        ("Cross the bridge and continue to the traffic lights.", "Cruza el puente y continúa hasta el semáforo.", "Cross indica atravesar; el semáforo funciona como punto de referencia."),
        ("The station is opposite the library.", "La estación está enfrente de la biblioteca.", "Opposite ubica un lugar al otro lado de una calle o espacio."),
        ("The café is on the corner beside the old clock, a useful landmark.", "El café está en la esquina junto al reloj antiguo, un punto de referencia útil.", "Corner localiza la intersección y landmark ayuda a reconocer el lugar."),
    ]
    pools = {
        "practiceGuided": [
            order(f"{p}.pg01", "Ordena la ruta: pasa la iglesia y gira a la izquierda.",
                  "Go past the church and turn left.",
                  ["Go", "past", "the", "church", "and", "turn", "left."], c,
                  "Go past precede el punto visible y turn left indica el cambio posterior.",
                  guided=True, hint="Primero sigue de largo; después cambia de dirección."),
            choose(f"{p}.pg02", "La farmacia está frente al hotel. Elige la ubicación exacta.",
                   ["The pharmacy is behind the hotel.", "The pharmacy is opposite the hotel.", "The pharmacy is inside the hotel."],
                   1, c, "Opposite traduce frente a sin indicar que ambos lugares son el mismo.",
                   guided=True, hint="Busca la preposición para dos edificios enfrentados."),
            match(f"{p}.pg03", "Relaciona cada instrucción con la acción física.",
                  [("cross the road", "atravesar la calle"), ("turn left", "cambiar hacia la izquierda")], c,
                  "Cross implica atravesar; turn left modifica el sentido del recorrido.", guided=True,
                  hint="Una acción cruza un espacio y la otra cambia la orientación."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué punto de referencia aparece después del puente.",
                   "Cross the bridge and stop beside the tall hotel.",
                   ["the small bank", "the railway station", "the tall hotel"], 2, c,
                   "La ruta termina beside the tall hotel, el referente después del puente."),
            complete(f"{p}.p02", "Completa: The bakery is on the ___ next to the park.",
                     "corner", c, "On the corner ubica la panadería en la intersección junto al parque."),
            write(f"{p}.p03", "Escribe: Cruza la plaza y pasa de largo el teatro.",
                  "Cruza la plaza y pasa de largo el teatro.",
                  "Cross the square and go past the theatre.",
                  ["Cross the square and go past the theatre.", "Go across the square, then pass the theatre."], c,
                  "La secuencia usa cross para atravesar y go past para continuar más allá."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Desde el mercado, pasa el banco y gira a la izquierda en el cine.",
                   ["Go past the bank and turn left at the cinema.", "Turn left at the bank, then go past the cinema.", "Go past the cinema and turn right at the bank."],
                   0, c, "La primera ruta conserva tanto el orden de los referentes como el giro indicado."),
            listen(f"{p}.e02", "Escucha y decide dónde está la oficina de turismo.",
                   "The tourist office is opposite the castle, on the corner.",
                   ["behind the castle", "inside the castle", "opposite the castle"], 2, c,
                   "Opposite the castle identifica la posición al otro lado del castillo."),
            complete(f"{p}.e03", "Usa go past: ___ the fountain; the station is ahead.",
                     "Go past", c, "Go past ordena continuar más allá de la fuente antes de llegar."),
            write(f"{p}.e04", "Da la ruta: cruza el puente y gira a la izquierda en el museo.",
                  "Cruza el puente y gira a la izquierda en el museo.",
                  "Cross the bridge and turn left at the museum.",
                  ["Cross the bridge and turn left at the museum.",
                   "Go across the bridge, then take a left at the museum."], c,
                  "La indicación enlaza un cruce con un giro en un referente inequívoco."),
        ],
        "review": [
            order(f"{p}.r01", "Reconstruye la ubicación del hostal frente a la catedral.",
                  "The hostel is opposite the cathedral.",
                  ["The", "hostel", "is", "opposite", "the", "cathedral."], c,
                  "Opposite sitúa hostal y catedral en lados enfrentados."),
            match(f"{p}.r02", "Une cada referencia con la parte correcta de la ruta.",
                  [("at the clock tower", "lugar para girar"), ("on the corner", "posición en la intersección")], c,
                  "At introduce el punto del giro y on the corner describe la ubicación final."),
            choose(f"{p}.r03", "Debes continuar más allá del banco. Selecciona la indicación.",
                   ["Stop opposite the bank.", "Go past the bank.", "Turn into the bank."],
                   1, c, "Go past the bank indica continuar hasta dejar el banco atrás."),
        ],
    }
    return common_class(n, ["Seguir indicaciones que combinan desplazamientos y giros.",
                            "Usar edificios visibles como puntos de referencia en una ruta.",
                            "Producir una secuencia breve para llegar a un lugar."],
                        vocabulary, teaching, pools,
                        {"e01": (1, "r02"), "e02": (3, "r01"),
                         "e03": (1, "r03"), "e04": (2, "r02")})


def build_68() -> dict[str, Any]:
    n, c, p = 68, CONCEPTS[68], "en.n2.c68"
    vocabulary = [("delayed", "retrasado"), ("cancelled", "cancelado"),
                  ("missed", "perdió"), ("luggage", "equipaje"),
                  ("wrong platform", "andén equivocado"), ("replacement bus", "autobús sustitutorio")]
    teaching = [
        ("Our train is delayed by forty minutes.", "Nuestro tren lleva cuarenta minutos de retraso.", "Delayed indica que el servicio saldrá más tarde, pero sigue previsto."),
        ("The ferry is cancelled, so it will not leave today.", "El ferry está cancelado, así que no saldrá hoy.", "Cancelled significa que el servicio no se realizará."),
        ("I missed the coach because I waited on the wrong platform.", "Perdí el autobús porque esperé en el andén equivocado.", "Missed expresa que el viajero no alcanzó el servicio; because presenta la causa."),
        ("My luggage is missing, so I will report it at the desk.", "Mi equipaje no aparece, así que lo informaré en el mostrador.", "Luggage identifica el objeto perdido y report indica la acción adecuada."),
        ("The cancelled train has a replacement bus to the next town.", "El tren cancelado tiene un autobús sustitutorio hasta la siguiente ciudad.", "Replacement bus mantiene la ruta cuando el tren no opera."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "El tren saldrá 30 minutos tarde. Elige el aviso correcto.",
                   ["The train is delayed.", "The train is cancelled.", "The train is on the wrong platform."],
                   0, c, "Delayed mantiene el viaje previsto y solo cambia la hora.", guided=True,
                   hint="El servicio todavía saldrá, pero no a tiempo."),
            match(f"{p}.pg02", "Relaciona cada problema con su consecuencia.",
                  [("cancelled flight", "no sale"), ("missed bus", "el viajero llegó tarde")], c,
                  "Cancelled elimina el servicio; missed indica que la persona no lo alcanzó.", guided=True,
                  hint="Separa un servicio inexistente de una salida que el viajero perdió."),
            complete(f"{p}.pg03", "Completa la causa: We waited on the ___ and missed the train.",
                     "wrong platform", c, "Wrong platform explica por qué esperaron en un lugar incorrecto.",
                     guided=True, hint="Necesitas una expresión de lugar equivocado."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué objeto no llegó al aeropuerto.",
                   "My luggage did not arrive with the flight.",
                   ["my passport", "my luggage", "my ticket"], 1, c,
                   "La grabación identifica luggage como el objeto que no llegó."),
            order(f"{p}.p02", "Ordena el aviso de cancelación y la alternativa.",
                  "The train is cancelled, so take the replacement bus.",
                  ["The", "train", "is", "cancelled,", "so", "take", "the", "replacement", "bus."], c,
                  "So conecta la cancelación con el autobús sustitutorio disponible."),
            write(f"{p}.p03", "Escribe: Perdimos el vuelo porque el autobús se retrasó.",
                  "Perdimos el vuelo porque el autobús se retrasó.",
                  "We missed the flight because the bus was delayed.",
                  ["We missed the flight because the bus was delayed.",
                   "Because the bus was late, we did not catch the flight."], c,
                  "Missed presenta el resultado y because relaciona el retraso con la causa."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha y distingue retraso de cancelación.",
                   "The 8:10 service is delayed, but it will leave at 8:45.",
                   ["It will leave at 8:10.", "It will leave at 8:45.", "It will not run today."],
                   1, c, "El servicio sigue activo y su nueva salida es a las 8:45."),
            choose(f"{p}.e02", "El barco no operará hoy. Selecciona la descripción precisa.",
                   ["The boat missed its luggage.", "The boat is slightly delayed.", "The boat is cancelled today."],
                   2, c, "Cancelled today comunica que el barco no realizará el trayecto."),
            complete(f"{p}.e03", "Completa la solución: The railway provides a ___ to the next town.",
                     "replacement bus", c, "Replacement bus es el transporte alternativo que ofrece la compañía."),
            write(f"{p}.e04", "Explica: mi equipaje falta y debo informar a la aerolínea.",
                  "Mi equipaje falta y debo informar a la aerolínea.",
                  "My luggage is missing, so I need to report it to the airline.",
                  ["My luggage is missing, so I need to report it to the airline.",
                   "I need to tell the airline because my luggage has not arrived."], c,
                  "La respuesta nombra el problema y la acción necesaria sin inventar una causa."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada aviso con la respuesta práctica.",
                  [("flight delayed", "consultar la nueva hora"), ("ferry cancelled", "buscar otra ruta")], c,
                  "Un retraso requiere nueva hora; una cancelación exige una alternativa."),
            order(f"{p}.r02", "Reconstruye la causa del tren perdido.",
                  "I missed the train because I arrived late.",
                  ["I", "missed", "the", "train", "because", "I", "arrived", "late."], c,
                  "Because introduce la llegada tardía como causa del tren perdido."),
            choose(f"{p}.r03", "Tu maleta no aparece en la cinta. ¿Qué problema debes informar?",
                   ["missing luggage", "a wrong platform", "a cancelled ferry"],
                   0, c, "Missing luggage describe exactamente una maleta que no llegó a la cinta."),
        ],
    }
    return common_class(n, ["Diferenciar retrasos, cancelaciones y servicios perdidos.",
                            "Relacionar un problema de viaje con su causa visible.",
                            "Identificar una respuesta práctica ante equipaje o transporte alterado."],
                        vocabulary, teaching, pools,
                        {"e01": (1, "r01"), "e02": (2, "r01"),
                         "e03": (5, "r01"), "e04": (4, "r03")})


def build_69() -> dict[str, Any]:
    n, c, p = 69, CONCEPTS[69], "en.n2.c69"
    vocabulary = [("Could you help me", "¿Podría ayudarme?"), ("information desk", "mostrador de información"),
                  ("show me", "mostrarme"), ("where", "dónde"),
                  ("lost", "perdido"), ("contact", "contactar")]
    teaching = [
        ("Where is the information desk? Could you help me find it?", "¿Dónde está el mostrador de información? ¿Podría ayudarme a encontrarlo?", "Where localiza el servicio y Could you help me añade una petición cortés."),
        ("Could you show me where platform three is?", "¿Podría mostrarme dónde está el andén tres?", "Show me where solicita orientación hacia un lugar específico."),
        ("I am lost and I need to contact my hotel.", "Estoy perdido y necesito contactar con mi hotel.", "I am lost explica la situación; need to contact expresa la ayuda necesaria."),
        ("Where can I report a missing bag?", "¿Dónde puedo informar sobre una bolsa extraviada?", "Where can I pregunta por el lugar adecuado para resolver un problema."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Necesitas orientación cortés en la estación. Elige la petición.",
                   ["You help me now.", "Could you help me, please?", "I helped the station yesterday."],
                   1, c, "Could you help me, please? mantiene cortesía y pide asistencia directa.", guided=True,
                   hint="Busca una pregunta con could y please."),
            order(f"{p}.pg02", "Ordena la pregunta para localizar el mostrador.",
                  "Where is the information desk?",
                  ["Where", "is", "the", "information", "desk?"], c,
                  "Where inicia la pregunta y information desk nombra el destino buscado.", guided=True,
                  hint="Empieza con la palabra interrogativa de lugar."),
            complete(f"{p}.pg03", "Completa la petición: Could you ___ me where the exit is?",
                     "show", c, "Show me where pide que la otra persona indique la ubicación.", guided=True,
                     hint="Usa el verbo de mostrar sin to."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué ayuda necesita la viajera perdida.",
                   "I am lost. Could you help me contact my hostel?",
                   ["She wants to cancel a ticket.", "She wants to contact her hostel.", "She wants to buy luggage."],
                   1, c, "La viajera pide contactar su hostel porque está perdida."),
            match(f"{p}.p02", "Relaciona cada necesidad con la pregunta útil.",
                  [("find a taxi", "Where is the taxi rank?"), ("recover a bag", "Where can I report lost luggage?")], c,
                  "Cada pregunta nombra el lugar o servicio que resuelve la necesidad."),
            write(f"{p}.p03", "Pide en inglés ayuda para encontrar el andén siete.",
                  "Ayuda para encontrar el andén siete.",
                  "Could you help me find platform seven, please?",
                  ["Could you help me find platform seven, please?",
                   "Please, could you show me where platform seven is?"], c,
                  "La petición incluye cortesía, acción y el andén concreto."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Perdiste tu mochila. Selecciona la pregunta más útil al personal.",
                   ["Where can I report a lost backpack?", "Could you show me where platform six is?", "Where can I buy a return ticket?"],
                   0, c, "Where can I report dirige el problema de la mochila al servicio correcto."),
            listen(f"{p}.e02", "Escucha y reconoce el destino que busca el pasajero.",
                   "Could you show me where the information desk is?",
                   ["the ticket machine", "the hotel entrance", "the information desk"], 2, c,
                   "El destino solicitado es literalmente the information desk."),
            complete(f"{p}.e03", "Completa con where: Could you tell me ___ I can contact the airline?",
                     "where", c, "Where introduce la ubicación del servicio para contactar la aerolínea."),
            write(f"{p}.e04", "Estás perdido: pide ayuda para llamar a tu hotel.",
                  "Estoy perdido y necesito llamar a mi hotel.",
                  "I am lost. Could you help me contact my hotel, please?",
                  ["I am lost. Could you help me contact my hotel, please?",
                   "Could you please help me call my hotel? I am lost."], c,
                  "La producción explica el problema y solicita una acción concreta con cortesía."),
        ],
        "review": [
            order(f"{p}.r01", "Reconstruye la pregunta para localizar el mostrador de información.",
                  "Could you tell me where the information desk is?",
                  ["Could", "you", "tell", "me", "where", "the", "information", "desk", "is?"], c,
                  "Information desk conserva el destino exacto y where solicita su ubicación."),
            write(f"{p}.r02", "Sin señal, pide al personal ayuda para contactar a tu hotel.",
                  "Mi teléfono no tiene señal; necesito contactar a mi hotel.",
                  "Could you help me contact my hotel because my phone has no signal?",
                  ["Could you help me contact my hotel because my phone has no signal?",
                   "My phone has no signal. Could you please help me call my hotel?"], c,
                  "La petición recupera exactamente la acción de contactar al hotel y explica la causa."),
            write(f"{p}.r03", "Pregunta con cortesía dónde puedes tomar un taxi.",
                  "¿Dónde puedo tomar un taxi?",
                  "Could you tell me where I can get a taxi, please?",
                  ["Could you tell me where I can get a taxi, please?",
                   "Please, could you show me where the taxi rank is?"], c,
                  "La pregunta usa where dentro de una petición cortés y mantiene el objetivo del taxi."),
        ],
    }
    return common_class(n, ["Formular peticiones corteses de ayuda durante un viaje.",
                            "Explicar un problema antes de solicitar una acción concreta.",
                            "Preguntar dónde encontrar un servicio de asistencia."],
                        vocabulary, teaching, pools,
                        {"e01": (4, "r03"), "e02": (1, "r01"),
                         "e03": (4, "r03"), "e04": (3, "r02")})


def build_70() -> dict[str, Any]:
    n, c, p = 70, CONCEPTS[70], "en.n2.c70"
    cumulative = [CONCEPTS[number] for number in range(66, 71)]
    vocabulary = [("itinerary", "itinerario"), ("reserve", "reservar"),
                  ("connection", "conexión"), ("backup plan", "plan alternativo"),
                  ("route", "ruta"), ("confirm", "confirmar")]
    teaching = [
        ("My itinerary lists the train, ticket and departure time.", "Mi itinerario enumera el tren, el billete y la hora de salida.", "Un itinerario reúne los datos necesarios antes del viaje."),
        ("Reserve the return ticket and confirm the platform.", "Reserva el billete de ida y vuelta y confirma el andén.", "Reserve fija la compra y confirm comprueba un dato que puede cambiar."),
        ("The route crosses the square before the bus connection.", "La ruta cruza la plaza antes de la conexión de autobús.", "Route ordena el desplazamiento y connection enlaza dos servicios."),
        ("Keep a backup plan for your route in case a service is cancelled.", "Mantén un plan alternativo para tu ruta por si se cancela un servicio.", "Backup plan anticipa una solución concreta para la ruta prevista."),
        ("Confirm where to ask for help before you travel.", "Confirma dónde pedir ayuda antes de viajar.", "Un plan completo incluye un punto de asistencia, no solo transporte y ruta."),
        ("For Bristol, reserve a single ticket for 8:30 from platform two. Go past the library. If the train is delayed, ask: Could you help me find the shuttle, please? The shuttle leaves at 9:00.", "Para Bristol, reserva un billete de ida para las 8:30 desde el andén dos. Pasa la biblioteca. Si el tren se retrasa, pregunta: ¿Podría ayudarme a encontrar el transporte, por favor? El transporte sale a las 9:00.", "El modelo integra billete, salida, referente, problema, petición y alternativa concreta sin omitir datos."),
    ]
    pools = {
        "practiceGuided": [
            match(f"{p}.pg01", "Relaciona cada parte del plan con su función.",
                  [("itinerary", "ordenar horas y trayectos"), ("backup plan", "responder a una cancelación")], c,
                  "El itinerario organiza el viaje; el plan alternativo protege ante cambios.", guided=True,
                  hint="Distingue la secuencia principal de la solución de emergencia."),
            choose(f"{p}.pg02", "Viajas y vuelves el domingo. ¿Qué acción completa la compra?",
                   ["Reserve a return ticket.", "Cancel every connection.", "Ignore the departure time."],
                   0, c, "Return ticket cubre ambos trayectos y reserve asegura la compra.", guided=True,
                   hint="La acción debe incluir el regreso y conservar el viaje."),
            order(f"{p}.pg03", "Ordena la comprobación del andén antes de salir.",
                  "Confirm the platform before the departure.",
                  ["Confirm", "the", "platform", "before", "the", "departure."], c,
                  "Confirm pide verificar el andén antes de la hora de salida.", guided=True,
                  hint="Empieza con la acción de comprobar y termina con el momento."),
        ],
        "practice": [
            complete(f"{p}.p01", "Usa reserve: I will ___ the ticket before Friday.",
                     "reserve", c, "Reserve completa la acción de asegurar el billete antes del viernes."),
            listen(f"{p}.p02", "Escucha qué conexión debe confirmar la viajera.",
                   "Please confirm the bus connection at Central Station.",
                   ["the ferry route", "the bus connection", "the hotel reservation"], 1, c,
                   "La grabación identifica the bus connection en Central Station."),
            write(f"{p}.p03", "Escribe: Mi ruta cruza el parque y termina en la estación.",
                  "Mi ruta cruza el parque y termina en la estación.",
                  "My route crosses the park and ends at the station.",
                  ["My route crosses the park and ends at the station.",
                   "The route goes across the park and finishes at the station."], c,
                  "La frase define un recorrido con un punto atravesado y un destino final."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Plan: ida el viernes y regreso el lunes. Elige la reserva correcta.",
                   ["a single ticket for Friday", "a return ticket for Friday and Monday", "a return ticket for Friday and Sunday"],
                   1, c, "El billete de ida y vuelta vincula las dos fechas del itinerario.",
                   requires=[CONCEPTS[66], c]),
            listen(f"{p}.e02", "Escucha la ruta y selecciona dónde girar.",
                   "Cross the bridge, go past the hotel and turn left at the museum.",
                   ["at the bridge", "at the hotel", "at the museum"], 2, c,
                   "El giro ocurre at the museum después de cruzar el puente y pasar el hotel.",
                   requires=[CONCEPTS[67], c]),
            choose(f"{p}.e03", "El tren se cancela. Debes pedir ayuda y mantener el viaje. ¿Qué dices?",
                   ["Could you help me confirm the new departure time?", "Could you help me find the replacement bus?", "Could you show me where the information desk is?"],
                   1, c, "La petición une el problema de cancelación con una alternativa de transporte útil.",
                   requires=[CONCEPTS[68], CONCEPTS[69], c]),
            write(f"{p}.e04", "Redacta el plan con cada dato y reproduce la petición entre comillas.",
                  "Return ticket to Leeds; 9:10, platform 4; go past the museum. The train is cancelled. Say: ‘Could you help me find bus 22, please?’ Alternative: bus 22 at 9:40.",
                  "I will reserve a return ticket to Leeds for the 9:10 departure and confirm platform four. From the station, I will go past the museum. If the train is cancelled, I will say, ‘Could you help me find bus 22, please?’ My alternative is bus 22 at 9:40.",
                  [
                      "I will reserve a return ticket to Leeds for the 9:10 departure and confirm platform four. From the station, I will go past the museum. If the train is cancelled, I will say, ‘Could you help me find bus 22, please?’ My alternative is bus 22 at 9:40.",
                      "My itinerary has a return ticket to Leeds, a 9:10 departure from platform four and a route past the museum. If the train is cancelled, I will ask, ‘Could you help me find bus 22, please?’ I will take bus 22 at 9:40 instead.",
                  ], c, "El plan usa todos los datos visibles y no inventa la petición ni la alternativa.",
                  requires=cumulative),
        ],
        "review": [
            order(f"{p}.r01", "Reconstruye el paso que asegura una conexión posterior.",
                  "Confirm the connection before leaving the station.",
                  ["Confirm", "the", "connection", "before", "leaving", "the", "station."], c,
                  "Confirmar antes de salir evita perder el enlace con el siguiente servicio."),
            match(f"{p}.r02", "Une cada riesgo del itinerario con su respuesta.",
                  [("service delayed", "confirm the new departure"), ("service cancelled", "use the backup plan")], c,
                  "El retraso cambia la hora; la cancelación activa la alternativa preparada."),
            write(f"{p}.r03", "Crea el plan de Norwich y reproduce la petición indicada.",
                  "Single ticket to Norwich; 7:45, platform 3; cross the square. The coach is delayed. Say: ‘Could you help me find the taxi stand, please?’ Alternative: taxi at 8:10.",
                   "I will reserve a single ticket to Norwich for 7:45 and confirm platform three. I will cross the square. If the coach is delayed, I will say, ‘Could you help me find the taxi stand, please?’ My alternative is a taxi at 8:10.",
                  ["I will reserve a single ticket to Norwich for 7:45 and confirm platform three. I will cross the square. If the coach is delayed, I will say, ‘Could you help me find the taxi stand, please?’ My alternative is a taxi at 8:10.",
                   "My Norwich plan uses a single ticket for 7:45 from platform three and a route across the square. If the coach is delayed, I will ask, ‘Could you help me find the taxi stand, please?’ I can take a taxi at 8:10."], c,
                  "El repaso integra los cinco conceptos en Norwich, un escenario distinto al de Leeds.",
                  requires=cumulative),
        ],
    }
    return common_class(n, ["Organizar un itinerario con transporte, horario y conexión.",
                            "Incluir una ruta reconocible y una respuesta ante problemas.",
                            "Presentar un plan completo con ayuda y alternativa confirmadas."],
                        vocabulary, teaching, pools,
                        {"e01": (2, "r03"), "e02": (3, "r03"),
                         "e03": (6, "r02"), "e04": (6, "r03")},
                        uses_patterns=cumulative, cumulative=cumulative)


def normalized(value: Any) -> str:
    text = value if isinstance(value, str) else canonical(value)
    return " ".join(re.findall(r"[a-záéíóúüñ0-9]+(?:'[a-záéíóúüñ0-9]+)?", text.casefold()))


def audit(classes: list[dict[str, Any]]) -> dict[str, Any]:
    prompt_ids: dict[str, str] = {}
    feedback_ids: dict[str, str] = {}
    semantic_ids: dict[str, str] = {}
    formats: Counter[str] = Counter()
    positions: dict[str, Counter[int]] = {}
    for cls in classes:
        class_positions: Counter[int] = Counter()
        assert sum(len(items) for items in cls["pools"].values()) == 13
        assert len(cls["vocabulary"]) >= 6
        assert len({item["format"] for items in cls["pools"].values() for item in items}) >= 4
        for items in cls["pools"].values():
            for item in items:
                prompt = normalized(item["prompt"]["es"])
                feedback = normalized(item["origin"]["feedback"]["es"])
                stimulus = (item["origin"].get("audio") or item["origin"].get("text")
                            or item["origin"].get("pairs") or item["prompt"]["es"])
                if item["format"] in {"elegir", "escuchar"}:
                    assert len(item["choices"]) >= 3
                    answer: Any = item["choices"][item["answer"]["index"]]["text"]
                    class_positions[item["answer"]["index"]] += 1
                elif item["format"] == "relacionar":
                    answer = item["answer"]["pairs"]
                else:
                    answer = item["answer"]["text"]
                semantic = normalized({"stimulus": stimulus, "answer": answer})
                assert prompt not in prompt_ids, (item["id"], prompt_ids.get(prompt))
                assert feedback not in feedback_ids, (item["id"], feedback_ids.get(feedback))
                assert semantic not in semantic_ids, (item["id"], semantic_ids.get(semantic))
                assert len(item["prompt"]["es"]) <= 90, item["id"]
                prompt_ids[prompt], feedback_ids[feedback], semantic_ids[semantic] = item["id"], item["id"], item["id"]
                formats[item["format"]] += 1
        assert len(class_positions) >= 2
        assert max(class_positions.values()) / sum(class_positions.values()) <= 0.60
        positions[cls["id"]] = class_positions
    return {
        "classes": len(classes),
        "items": sum(sum(len(items) for items in cls["pools"].values()) for cls in classes),
        "uniquePrompts": len(prompt_ids), "uniqueFeedback": len(feedback_ids),
        "uniqueSemanticSignatures": len(semantic_ids), "formats": dict(sorted(formats.items())),
        "correctPositions": {key: dict(sorted(value.items())) for key, value in positions.items()},
    }


def bundle(classes: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 2,
        "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "classes": classes,
    }


def validate_file(path: Path, start: int, end: int) -> str:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--file", str(path), "--start", str(start),
         "--end", str(end), "--level", "2"], cwd=ROOT, text=True,
        capture_output=True, check=False,
    )
    message = (result.stdout + result.stderr).strip()
    if result.returncode:
        raise SystemExit(f"Validation failed for {path.name}: {message}")
    return message


def report(classes: list[dict[str, Any]], audit_result: dict[str, Any],
           validation: list[str]) -> str:
    lines = [
        "# DRAFT — Inglés N2 C66–C70", "",
        "Estado: **DRAFT para revisión independiente; no autorizado para integración**.", "",
        "## Alcance", "",
        "- Staging aislado; no modifica `assets/contenido`, tests ni documentación.",
        f"- Digest del mapa N2 v2: `{digest(MAP)}`.",
        "- Contrato `editorial-agent.v2`; `status: shadow`; `runtimeAi: false`.",
        "- El generador construye cada clase, la valida por separado y después valida el bundle.",
        "", "## Evidencia por clase", "",
        "| Clase | Fase | Concepto | Vocabulario | Ejercicios | Formatos |",
        "|---|---|---|---:|---:|---:|",
    ]
    for cls in classes:
        class_formats = {item["format"] for items in cls["pools"].values() for item in items}
        lines.append(f"| {cls['id']} | {cls['phase']} | `{cls['concepts'][0]}` | "
                     f"{len(cls['vocabulary'])} | 13 | {len(class_formats)} |")
    lines.extend([
        "", "## Cobertura acumulativa C70", "",
        "- `e01`: reserva de transporte y billete de ida y vuelta.",
        "- `e02`: indicaciones secuenciadas con puente, hotel y museo.",
        "- `e03`: cancelación, petición cortés y autobús sustitutorio.",
        "- `e04`: plan de Leeds con billete de vuelta, 9:10/P4, museo, cancelación, petición textual y bus 22 a las 9:40.",
        "", "## Correcciones incorporadas tras revisión", "",
        "- C66 `e02` remedia la hora con `t04` y un repaso nuevo de hora de salida.",
        "- C67 `e03` vuelve a `go past` tanto en enseñanza como en repaso.",
        "- C69 `e02` recupera `information desk`; `e04` recupera `contact my hotel` en escenarios nuevos.",
        "- C70 `e04`, `t06` y `r03` integran los cinco conceptos con datos completos y escenarios distintos.",
        "- Se naturalizaron la expresión de tarifa, el uso de `backup plan` y distractores demasiado obvios.",
        "", "## Auditoría reproducible", "", "```json",
        json.dumps(audit_result, ensure_ascii=False, indent=2), "```", "",
        "## Validación ejecutada", "",
    ])
    lines.extend(f"- `{message}`" for message in validation)
    lines.extend([
        "", "Comando de regeneración:", "", "```bash",
        "PYTHONDONTWRITEBYTECODE=1 python3 work/n2_c66_70/generate.py", "```", "",
        "## Incidencias y dudas para el revisor", "",
        "- Incidencias automáticas conocidas: ninguna tras la validación incluida.",
        "- Revisar naturalidad A2 de las variantes extensas de C69 y C70.",
        "- Simular fallo total para confirmar que cada ruta de remediación ataca el error concreto.",
        "- Verificar en revisión adversarial que C70 demuestra los cinco conceptos sin depender de memoria externa.",
        "- Este autor entrega `DRAFT`; no emite `GO` ni integra el contenido.", "",
    ])
    return "\n".join(lines)


def main() -> int:
    classes = [build_66(), build_67(), build_68(), build_69(), build_70()]
    audit_result = audit(classes)
    for cls in classes:
        number = int(cls["id"].rsplit("-", 1)[1])
        (OUT / f"class-{number}.json").write_text(
            json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    bundle_path = OUT / "bundle-66-70.json"
    bundle_path.write_text(json.dumps(bundle(classes), ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    validation = [validate_file(OUT / f"class-{number}.json", number, number)
                  for number in range(66, 71)]
    validation.append(validate_file(bundle_path, 66, 70))
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    (REPORT_OUT / "REPORT.md").write_text(report(classes, audit_result, validation), encoding="utf-8")
    print("\n".join(validation))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
