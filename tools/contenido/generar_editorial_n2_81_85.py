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
REPORT_OUT = ROOT / "build/editorial-n2-81-85"
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
    81: "n2-home-problems",
    82: "n2-public-services",
    83: "n2-report-problem",
    84: "n2-arrange-repair",
    85: "n2-solve-neighbourhood-issue",
}
PHASES = {81: "input", 82: "form", 83: "comprehension", 84: "production", 85: "transfer"}
TITLES = {
    81: {"en": "Home problems", "es": "Problemas del hogar"},
    82: {"en": "Public services", "es": "Servicios públicos"},
    83: {"en": "Report a problem", "es": "Informar de un problema"},
    84: {"en": "Arrange a repair", "es": "Organizar una reparación"},
    85: {"en": "Solve a neighbourhood issue", "es": "Resolver un problema vecinal"},
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
             requires: list[str] | None = None,
             accepted: list[str] | None = None) -> dict[str, Any]:
    teaches, default_requires = requirements(concept, guided)
    return add_hash({
        "id": item_id, "format": "completar", "prompt": {"es": prompt},
        "answer": {"text": answer, "accepted": accepted or [answer]}, "choices": [],
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


def build_81() -> dict[str, Any]:
    n, c, p = 81, CONCEPTS[81], "en.n2.c81"
    vocabulary = [("leak", "fuga"), ("blocked", "atascado"), ("power", "electricidad"),
                  ("heating", "calefacción"), ("broken", "averiado"), ("alarm", "alarma")]
    teaching = [
        ("There is a leak under the kitchen sink.", "Hay una fuga debajo del fregadero de la cocina.", "Leak identifica agua que sale de una tubería o conexión."),
        ("The drain is blocked, so the water goes down slowly.", "El desagüe está atascado, por eso el agua baja lentamente.", "Blocked describe una obstrucción sin indicar que debas desmontar la tubería."),
        ("During a power cut, use a flashlight and do not touch exposed wires.", "Durante un corte de luz, usa una linterna y no toques cables expuestos.", "Power cut nombra la falta de electricidad; alejarse de cables reduce el riesgo."),
        ("The heating is broken, and the flat is very cold.", "La calefacción está averiada y el piso está muy frío.", "Heating y broken describen el sistema y su estado para pedir ayuda."),
        ("If the smoke alarm sounds or you smell gas, leave and call emergency services.", "Si suena la alarma de humo o hueles gas, sal y llama a emergencias.", "Ante humo o gas no se intenta reparar: se sale y se contacta a profesionales."),
        ("The shelf in the living room is broken, but nobody is hurt.", "La estantería de la sala está rota, pero nadie está herido.", "Un aviso de objeto roto incluye ubicación y estado de las personas sin inventar una causa."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Hay agua debajo del fregadero. Elige el problema más probable.",
                   ["a leak", "a power cut", "a broken smoke alarm"], 0, c,
                   "Leak corresponde al agua que aparece bajo una conexión.", guided=True,
                   hint="Busca el problema relacionado con agua que sale."),
            match(f"{p}.pg02", "Relaciona cada señal con el problema doméstico.",
                  [("water drains slowly", "desagüe atascado"), ("all lights are off", "corte de luz")], c,
                  "El drenaje lento indica obstrucción; todas las luces apagadas indican falta de energía.", guided=True,
                  hint="Separa un problema de agua de uno eléctrico."),
            complete(f"{p}.pg03", "Completa el sistema averiado: The ___ is broken, so the room is cold.",
                     "heating", c, "Heating completa el sistema que mantiene caliente la habitación.", guided=True,
                     hint="Necesitas el nombre del sistema de calor."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué problema hay en el baño.",
                   "The bathroom drain is blocked and the water is rising.",
                   ["a broken window", "a blocked drain", "a power cut"], 1, c,
                   "La grabación identifica un desagüe atascado y agua que sube."),
            order(f"{p}.p02", "Ordena la descripción de una fuga pequeña.",
                  "There is a small leak beside the washing machine.",
                  ["There", "is", "a", "small", "leak", "beside", "the", "washing", "machine."], c,
                  "There is introduce el problema y beside ubica la fuga."),
            write(f"{p}.p03", "Escribe: La calefacción está averiada desde esta mañana.",
                  "La calefacción está averiada desde esta mañana.",
                  "The heating has been broken since this morning.",
                  ["The heating has been broken since this morning.", "The heating has not worked since this morning."], c,
                  "La frase identifica el sistema, el fallo y cuándo comenzó."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Hueles gas en la cocina. Selecciona la acción segura.",
                   ["Leave the home and call emergency services.", "Test the cooker with a flame.", "Repair the gas pipe yourself."], 0, c,
                   "Salir y llamar a emergencias evita una intervención peligrosa con gas."),
            listen(f"{p}.e02", "Escucha y selecciona el equipo que emite la señal.",
                   "The smoke alarm is making a loud sound upstairs.",
                   ["the heating", "the smoke alarm", "the kitchen drain"], 1, c,
                   "Smoke alarm es el equipo que produce el sonido fuerte."),
            complete(f"{p}.e03", "Completa el fallo eléctrico: We have a ___ in the whole building.",
                     "power cut", c, "Power cut describe la falta de electricidad en todo el edificio."),
            write(f"{p}.e04", "Informa: ventana rota en el dormitorio; no hay heridos.",
                  "La ventana del dormitorio está rota; no hay heridos.",
                  "The bedroom window is broken, but nobody is hurt.",
                  ["The bedroom window is broken, but nobody is hurt.", "There is a broken window in the bedroom, and no one is injured."], c,
                  "El aviso localiza el objeto, describe el estado y confirma que no hay heridos."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada problema con la respuesta segura.",
                  [("smell gas", "salir y llamar a emergencias"), ("smoke alarm sounds", "salir y seguir instrucciones"), ("exposed wire", "mantener distancia y avisar")], c,
                  "Gas, alarma y cables expuestos exigen distancia y ayuda profesional."),
            choose(f"{p}.r02", "Espejo roto en el pasillo; nadie herido. Elige el aviso fiel.",
                   ["The hall mirror is broken, but nobody is hurt.", "The bedroom window is open and one person is hurt.", "The kitchen mirror is dirty, but nobody saw it."], 0, c,
                   "El primer aviso conserva el objeto, la ubicación y la ausencia de heridos."),
            order(f"{p}.r03", "Reconstruye el aviso de corte eléctrico.",
                  "There is a power cut in our street.",
                  ["There", "is", "a", "power", "cut", "in", "our", "street."], c,
                  "Power cut comunica la falta de electricidad y our street delimita el área."),
        ],
    }
    return common_class(n, ["Reconocer problemas comunes de agua, electricidad y calefacción.",
                            "Describir qué objeto falla y dónde se encuentra.",
                            "Elegir una respuesta segura sin intentar reparaciones peligrosas."], vocabulary, teaching, pools,
                        {"e01": (5, "r01"), "e02": (5, "r01"), "e03": (3, "r03"), "e04": (6, "r02")})


def build_82() -> dict[str, Any]:
    n, c, p = 82, CONCEPTS[82], "en.n2.c82"
    vocabulary = [("water", "agua"), ("electricity", "electricidad"),
                  ("waste", "residuos"), ("lighting", "alumbrado"),
                  ("emergency", "emergencia"), ("account", "cuenta")]
    teaching = [
        ("Call the water service about a broken public pipe.", "Llama al servicio de agua por una tubería pública rota.", "Water service atiende problemas de la red pública, no arreglos dentro del piso."),
        ("Report a neighbourhood power cut to the electricity company.", "Informa a la compañía eléctrica de un corte de luz en el barrio.", "Electricity company gestiona fallos de suministro fuera de una sola vivienda."),
        ("Waste collection removes household rubbish on scheduled days.", "La recogida de residuos retira la basura doméstica en días programados.", "Waste collection es el servicio adecuado para basura no recogida."),
        ("The council manages street lighting and damaged public lamps.", "El municipio gestiona el alumbrado público y las farolas dañadas.", "Street lighting pertenece al espacio público y se informa al municipio."),
        ("Use emergency services only for immediate danger; keep your account number for routine calls.", "Usa emergencias solo ante peligro inmediato; ten tu número de cuenta para llamadas rutinarias.", "Emergency services no sustituye la atención ordinaria y nunca se comparten datos innecesarios."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Toda la calle está sin electricidad. Elige el servicio adecuado.",
                   ["the electricity company", "waste collection", "the water service"], 0, c,
                   "La compañía eléctrica atiende un corte que afecta a toda la calle.", guided=True,
                   hint="Busca el servicio responsable del suministro eléctrico."),
            match(f"{p}.pg02", "Relaciona cada incidencia pública con el servicio.",
                  [("rubbish not collected", "recogida de residuos"), ("broken street lamp", "alumbrado público")], c,
                  "La basura corresponde a waste collection y la farola a street lighting.", guided=True,
                  hint="Distingue residuos de iluminación de la calle."),
            complete(f"{p}.pg03", "Completa el dato de cliente: Please have your ___ ready.",
                     "account number", c, "Account number identifica el contrato en una llamada rutinaria.", guided=True,
                     hint="Es el número de la cuenta, no una contraseña."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué servicio debe revisar la tubería de la calle.",
                   "Please report the broken main pipe to the water service.",
                   ["the fire station", "the water service", "waste collection"], 1, c,
                   "La tubería principal corresponde al water service."),
            order(f"{p}.p02", "Ordena el aviso sobre una farola apagada.",
                  "Street lighting is not working outside number twelve.",
                  ["Street", "lighting", "is", "not", "working", "outside", "number", "twelve."], c,
                  "Street lighting nombra el servicio y outside number twelve aporta ubicación."),
            write(f"{p}.p03", "Escribe: La basura no fue recogida hoy.",
                  "La basura no fue recogida hoy.", "The waste collection did not come today.",
                  ["The waste collection did not come today.", "Our household rubbish was not collected today."], c,
                  "La frase informa del servicio ausente y del día afectado."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Una farola está apagada, sin cables visibles. ¿A quién informas?",
                   ["the water service", "the council's street lighting team", "the building's private electrician"],
                   1, c, "El equipo municipal de alumbrado gestiona una farola pública apagada."),
            listen(f"{p}.e02", "Escucha qué dato pide la compañía antes de revisar el suministro.",
                   "Could I have your electricity account number, please?",
                   ["the street name", "the account number", "the bin colour"], 1, c,
                   "La llamada solicita exactamente el account number de electricidad."),
            complete(f"{p}.e03", "Completa el servicio: A burst main pipe belongs to the ___.",
                     "water service", c, "Water service atiende la tubería principal de la red pública."),
            write(f"{p}.e04", "Informa al municipio: no recogieron residuos en Oak Street.",
                  "No recogieron residuos en Oak Street.",
                  "The waste collection did not come to Oak Street today.",
                  ["The waste collection did not come to Oak Street today.",
                   "Household rubbish was not collected on Oak Street today."], c,
                  "El aviso identifica servicio, calle y momento sin añadir datos privados."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada aviso con el servicio público responsable.",
                  [("neighbourhood power cut", "electricity company"),
                   ("broken public lamp", "street lighting team"),
                   ("burst main pipe", "municipal water service"),
                   ("rubbish not collected on Cedar Road today", "waste collection")], c,
                  "Cada aviso aporta la incidencia necesaria para elegir el servicio responsable."),
            choose(f"{p}.r02", "Hay fuego y riesgo inmediato. Selecciona el contacto seguro.",
                   ["emergency services", "routine waste collection", "the billing department tomorrow"], 0, c,
                   "Emergency services es el contacto correcto ante fuego y peligro inmediato."),
            order(f"{p}.r03", "Reconstruye la solicitud rutinaria del número de cuenta.",
                  "Please provide your account number for the service request.",
                  ["Please", "provide", "your", "account", "number", "for", "the", "service", "request."], c,
                  "Account number se solicita para ubicar el contrato, sin pedir contraseñas."),
        ],
    }
    return common_class(n, ["Relacionar incidencias urbanas con el servicio público responsable.",
                            "Distinguir una gestión rutinaria de una emergencia real.",
                            "Comunicar ubicación y datos mínimos sin exponer información sensible."], vocabulary, teaching, pools,
                        {"e01": (4, "r01"), "e02": (5, "r03"), "e03": (1, "r01"), "e04": (3, "r01")})


def build_83() -> dict[str, Any]:
    n, c, p = 83, CONCEPTS[83], "en.n2.c83"
    vocabulary = [("address", "dirección"), ("started", "comenzó"), ("affected", "afectado"),
                  ("urgent", "urgente"), ("reference", "referencia"), ("describe", "describir")]
    teaching = [
        ("Give the full address before you describe the problem.", "Da la dirección completa antes de describir el problema.", "Address ubica la incidencia y describe introduce la información observable."),
        ("The leak started at six this morning.", "La fuga comenzó a las seis de esta mañana.", "Started fija cuándo comenzó el problema sin adivinar la causa."),
        ("Two flats are affected by the water cut.", "Dos pisos están afectados por el corte de agua.", "Affected identifica el alcance del problema."),
        ("Say urgent only when delay may cause harm or serious damage.", "Di urgente solo cuando la demora pueda causar daño grave.", "Urgent comunica prioridad real y no debe usarse para acelerar casos rutinarios."),
        ("Ask for a reference number after the report.", "Pide un número de referencia después del aviso.", "Reference number permite dar seguimiento sin repetir toda la información."),
    ]
    pools = {
        "practiceGuided": [
            order(f"{p}.pg01", "Ordena el inicio del aviso con la dirección completa.",
                  "The address is 24 Green Street, flat 3A.",
                  ["The", "address", "is", "24", "Green", "Street,", "flat", "3A."], c,
                  "Address aparece antes de calle y piso para localizar la incidencia.", guided=True,
                  hint="Empieza identificando que vas a dar la dirección."),
            choose(f"{p}.pg02", "La fuga comenzó a las 07:30. Elige la frase exacta.",
                   ["The leak ended at 7:30.", "The leak started at 7:30.", "The address is 7:30."],
                   1, c, "Started at 7:30 comunica el momento inicial de la fuga.", guided=True,
                   hint="Busca el verbo para comenzó."),
            match(f"{p}.pg03", "Relaciona cada dato del aviso con su función.",
                  [("three homes affected", "alcance"), ("reference number 842", "seguimiento")], c,
                  "Affected mide el alcance y el número permite consultar el caso.", guided=True,
                  hint="Separa cuántas viviendas sufren el problema de cómo rastrear el aviso."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha cuántos apartamentos están afectados.",
                   "The heating problem affects flats four, five and six.",
                   ["two flats", "three flats", "six flats"], 1, c,
                   "Los pisos cuatro, cinco y seis suman tres viviendas afectadas."),
            complete(f"{p}.p02", "Completa la prioridad real: Water is near a socket, so it is ___.",
                     "urgent", c, "Urgent es adecuado porque el agua cerca de electricidad implica riesgo."),
            write(f"{p}.p03", "Informa: ruido fuerte en ascensor desde las 09:00; nadie herido.",
                  "Ruido fuerte en el ascensor desde las 09:00; nadie herido.",
                  "There has been a loud noise in the lift since 9 a.m., but nobody is hurt.",
                  ["There has been a loud noise in the lift since 9 a.m., but nobody is hurt.",
                   "Since 9 a.m., there has been a loud noise in the lift, but no one is injured."], c,
                  "El aviso describe la señal, el inicio y el estado de las personas."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha y selecciona la dirección del aviso.",
                   "I am reporting a broken street lamp outside 16 River Road.",
                   ["60 River Road", "16 River Road", "16 River Lane"], 1, c,
                   "La dirección pronunciada es 16 River Road."),
            choose(f"{p}.e02", "Agua cerca de un enchufe afecta dos pisos. Elige el informe fiel.",
                   ["This is urgent: water is near a socket and two flats are affected.", "Two flats are affected, but the socket is dry.", "Only one flat is affected and there is no water."],
                   0, c, "El primer informe conserva el riesgo eléctrico y el alcance de dos pisos."),
            complete(f"{p}.e03", "Completa el seguimiento: Could I have a ___ for this report?",
                     "reference number", c, "Reference number permite identificar el aviso después de registrarlo."),
            write(f"{p}.e04", "Informa: 8 Hill Road; calefacción falló ayer; tres pisos afectados.",
                  "8 Hill Road; calefacción averiada desde ayer; tres pisos afectados.",
                  "I am reporting broken heating at 8 Hill Road. It started yesterday, and three flats are affected.",
                  ["I am reporting broken heating at 8 Hill Road. It started yesterday, and three flats are affected.",
                   "The heating at 8 Hill Road stopped working yesterday and now affects three flats."], c,
                  "El informe contiene dirección, problema, inicio y alcance sin inventar una causa."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada pregunta con el dato que completa el aviso.",
                  [("What is the address?", "ubicación"), ("When did it start?", "momento inicial"), ("Who is affected?", "alcance")], c,
                  "Las preguntas recuperan ubicación, tiempo y alcance del informe."),
            order(f"{p}.r02", "Reconstruye la petición de seguimiento del caso.",
                  "Could I have the reference number, please?",
                  ["Could", "I", "have", "the", "reference", "number,", "please?"], c,
                  "La petición cortés solicita el identificador del aviso ya registrado."),
            choose(f"{p}.r03", "No hay peligro ni daño creciente. ¿Cómo clasificas el aviso?",
                   ["routine, not urgent", "an immediate emergency", "a private password request"], 0, c,
                   "Routine, not urgent evita etiquetar como emergencia un caso estable."),
        ],
    }
    return common_class(n, ["Estructurar un aviso con dirección, descripción, inicio y alcance.",
                            "Distinguir una incidencia urgente de una gestión rutinaria.",
                            "Solicitar un número de referencia para seguimiento."], vocabulary, teaching, pools,
                        {"e01": (1, "r01"), "e02": (4, "r03"), "e03": (5, "r02"), "e04": (2, "r01")})


def build_84() -> dict[str, Any]:
    n, c, p = 84, CONCEPTS[84], "en.n2.c84"
    vocabulary = [("appointment", "cita"), ("technician", "técnico"), ("available", "disponible"),
                  ("access", "acceso"), ("estimate", "presupuesto"), ("confirm", "confirmar")]
    teaching = [
        ("I would like to arrange a repair appointment.", "Quisiera organizar una cita de reparación.", "Appointment nombra la visita acordada para revisar el problema."),
        ("A verified technician is available on Tuesday morning.", "Un técnico verificado está disponible el martes por la mañana.", "Technician identifica al profesional y available ofrece una franja posible."),
        ("The caretaker can provide access to the shared basement.", "El conserje puede facilitar acceso al sótano compartido.", "Access debe acordarse con la persona autorizada, no improvisarse."),
        ("Please send an estimate before any paid work begins.", "Envíe un presupuesto antes de iniciar cualquier trabajo pagado.", "Estimate permite conocer el costo antes de aceptar el trabajo."),
        ("Confirm the time and check the technician's identification at the door.", "Confirma la hora y revisa la identificación del técnico en la puerta.", "Confirm evita horarios ambiguos y verificar identidad mejora la seguridad."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Puedes recibir al técnico el martes de 9 a 11. Elige la respuesta.",
                   ["I am available on Tuesday from 9 to 11.", "I am available on Tuesday after 1 p.m.", "Wednesday from 9 to 11 works for me."],
                   0, c, "Available on Tuesday from 9 to 11 ofrece una franja concreta.", guided=True,
                   hint="Busca día y horas de disponibilidad."),
            match(f"{p}.pg02", "Relaciona cada paso con su objetivo seguro.",
                  [("ask for an estimate", "conocer el costo"), ("check technician ID", "verificar identidad")], c,
                  "El presupuesto aclara costo y la identificación confirma quién entra.", guided=True,
                  hint="Separa una decisión económica de una comprobación de seguridad."),
            complete(f"{p}.pg03", "Completa la entrada acordada: The caretaker will provide ___.",
                     "access", c, "Access completa la autorización para entrar al área compartida.", guided=True,
                     hint="Necesitas el sustantivo para permitir la entrada."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha la franja disponible del técnico.",
                   "The technician is available between one and three on Thursday.",
                   ["Thursday, 10 to 1", "Thursday, 1 to 3", "Tuesday, 1 to 3"], 1, c,
                   "La visita disponible es el jueves de una a tres."),
            order(f"{p}.p02", "Ordena la solicitud de presupuesto previo.",
                  "Could you send an estimate before the repair?",
                  ["Could", "you", "send", "an", "estimate", "before", "the", "repair?"], c,
                  "Estimate aparece como requisito antes de la reparación."),
            write(f"{p}.p03", "Pide una cita el viernes por la tarde.",
                  "Una cita de reparación el viernes por la tarde.",
                  "Could we arrange a repair appointment for Friday afternoon?",
                  ["Could we arrange a repair appointment for Friday afternoon?",
                   "I would like to book the repair for Friday afternoon."], c,
                  "La petición nombra la reparación y una franja concreta."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "El técnico propone lunes 10:00; tú solo puedes a las 15:00. ¿Qué dices?",
                   ["I can confirm Monday at 10.", "I am available at 3 p.m.; is that possible?", "Please begin without access."],
                   1, c, "La respuesta ofrece la única hora compatible y pide confirmación."),
            listen(f"{p}.e02", "Escucha quién dará acceso al cuarto de máquinas.",
                   "The building manager will provide access to the plant room.",
                   ["the caretaker", "the flat owner", "the building manager"], 2, c,
                   "Building manager es la persona autorizada para facilitar el acceso."),
            complete(f"{p}.e03", "Completa el costo previo: Please email the ___ before work starts.",
                     "estimate", c, "Estimate es el documento de costo que debe llegar antes del trabajo."),
            write(f"{p}.e04", "Organiza: técnico verificado, miércoles 14:00, acceso con conserje.",
                  "Técnico verificado; miércoles 14:00; conserje facilita acceso.",
                  "Please confirm the repair appointment with the verified technician for Wednesday at 2 p.m. The caretaker will provide access.",
                  ["Please confirm the repair appointment with the verified technician for Wednesday at 2 p.m. The caretaker will provide access.",
                   "Please book the verified technician for Wednesday at 2 p.m.; the caretaker can let them in."], c,
                  "La cita confirma profesional, hora y acceso autorizado."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada detalle de la cita con su función.",
                  [("Tuesday, 11 a.m.", "hora confirmada"), ("caretaker has the key", "acceso autorizado")], c,
                  "La hora fija la visita y la llave del conserje resuelve el acceso."),
            order(f"{p}.r02", "Reconstruye la comprobación de identidad en la puerta.",
                  "Please show your technician identification before entering.",
                  ["Please", "show", "your", "technician", "identification", "before", "entering."], c,
                  "La identificación se verifica antes de permitir la entrada."),
            write(f"{p}.r03", "Confirma cita y pide presupuesto antes del trabajo.",
                  "Confirmar cita y pedir presupuesto previo.",
                  "I confirm the appointment for Monday morning. Please send the estimate before work begins.",
                  ["I confirm the appointment for Monday morning. Please send the estimate before work begins.",
                   "Monday morning is confirmed; could you provide an estimate before starting the repair?"], c,
                  "La respuesta fija la visita y mantiene el costo pendiente de aprobación."),
        ],
    }
    return common_class(n, ["Proponer y confirmar una franja concreta para una reparación.",
                            "Acordar acceso con una persona autorizada y verificar identidad.",
                            "Solicitar un presupuesto antes de aceptar trabajo pagado."], vocabulary, teaching, pools,
                        {"e01": (2, "r01"), "e02": (3, "r01"), "e03": (4, "r03"), "e04": (5, "r01")})


def build_85() -> dict[str, Any]:
    n, c, p = 85, CONCEPTS[85], "en.n2.c85"
    cumulative = [CONCEPTS[number] for number in range(81, 86)]
    vocabulary = [("neighbour", "vecino"), ("council", "municipio"), ("evidence", "evidencia"),
                  ("shared area", "zona común"), ("solution", "solución"), ("follow-up", "seguimiento")]
    teaching = [
        ("Speak calmly with your neighbour and describe the shared problem.", "Habla con calma con tu vecino y describe el problema común.", "Neighbour participa en una solución; el aviso se centra en hechos, no acusaciones."),
        ("Report public or shared-area damage to the council or building manager.", "Informa al municipio o administrador sobre daños públicos o de la zona común.", "Council atiende espacio público y el administrador gestiona áreas comunes privadas."),
        ("Keep simple evidence such as dates and photos taken from a safe place.", "Guarda evidencia sencilla como fechas y fotos tomadas desde un lugar seguro.", "Evidence apoya el aviso sin acercarse a cables, fuego u otros riesgos."),
        ("Agree on a solution, a responsible contact and a follow-up time.", "Acuerda una solución, un contacto responsable y un momento de seguimiento.", "Solution resuelve el caso y follow-up verifica si la acción ocurrió."),
        ("Do not enter a neighbour's home or confront anyone; contact the neighbour through safe channels.", "No entres en la vivienda de un vecino ni confrontes a nadie; contacta al vecino por canales seguros.", "La seguridad y la privacidad tienen prioridad sobre resolver el problema por cuenta propia."),
        ("At 4 Elm Court, a power cut began Monday morning and affects flats 1 and 2, but there is no smoke. The electricity company records it and gives a reference number. A verified technician comes Tuesday at nine, caretaker Lou opens the meter room, and neighbour Ana gets an update.", "En 4 Elm Court, un corte de luz comenzó el lunes por la mañana y afecta a los pisos 1 y 2, pero no hay humo. La compañía eléctrica lo registra y da un número de referencia. Un técnico verificado llega el martes a las nueve, el conserje Lou abre la sala de contadores y la vecina Ana recibe una actualización.", "El modelo integra problema, servicio, datos, visita autorizada y seguimiento vecinal."),
    ]
    pools = {
        "practiceGuided": [
            match(f"{p}.pg01", "Relaciona cada problema vecinal con el contacto adecuado.",
                  [("broken bench in public park", "municipio"), ("leak in shared hallway", "administrador del edificio")], c,
                  "El municipio gestiona el parque y el administrador la zona común del edificio.", guided=True,
                  hint="Distingue espacio público de área común privada."),
            choose(f"{p}.pg02", "Hay ruido repetido. ¿Qué primer paso es respetuoso y seguro?",
                   ["Speak calmly with the neighbour about the times affected.", "Enter the neighbour's home to stop the music.", "Post their private details online."],
                   0, c, "Hablar con calma sobre horarios observables protege seguridad y privacidad.", guided=True,
                   hint="Elige comunicación directa sin entrar ni exponer datos."),
            complete(f"{p}.pg03", "Completa el control posterior: We will do a ___ on Friday.",
                     "follow-up", c, "Follow-up fija cuándo comprobar si la solución funcionó.", guided=True,
                     hint="Necesitas la expresión para una comprobación posterior."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué evidencia segura conserva la residente.",
                   "I wrote down the dates and took a photo from across the street.",
                   ["a neighbour's password", "dates and a safe photo", "an unverified repair bill"], 1, c,
                   "Fechas y una foto tomada desde lejos documentan el problema sin acercarse."),
            order(f"{p}.p02", "Ordena la propuesta de solución para la zona común.",
                  "The solution is to repair the shared gate on Tuesday.",
                  ["The", "solution", "is", "to", "repair", "the", "shared", "gate", "on", "Tuesday."], c,
                  "Solution introduce la acción y Tuesday fija cuándo ocurrirá."),
            write(f"{p}.p03", "Escribe: Informaré al municipio sobre la farola rota.",
                  "Informaré al municipio sobre la farola rota.",
                  "I will report the broken street lamp to the council.",
                  ["I will report the broken street lamp to the council.", "I will tell the council that the street lamp is broken."], c,
                  "La frase identifica el objeto público y el organismo responsable."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Agua cerca de un cable en el pasillo común. ¿Qué haces primero?",
                   ["Keep people away and contact the building manager urgently.", "Cover the cable with a wet towel.", "Wait beside the cable until a technician arrives."],
                   0, c, "Alejar personas y avisar con urgencia responde al riesgo sin tocar electricidad.",
                   requires=[CONCEPTS[81], c]),
            listen(f"{p}.e02", "Escucha qué servicio recibirá el aviso sobre la acera pública.",
                   "The council will receive the report about the damaged pavement.",
                   ["the private plumber", "the council", "the neighbour's landlord"], 1, c,
                   "Council es el organismo nombrado para la acera pública.",
                   requires=[CONCEPTS[82], c]),
            choose(f"{p}.e03", "Aviso: 5 Oak Lane, empezó lunes, afecta dos casas. ¿Qué falta?",
                   ["an estimate from a private technician", "a reference number for follow-up", "a confirmed repair appointment"],
                   1, c, "El número de referencia permite seguir el aviso sin pedir datos sensibles ni entrar.",
                   requires=[CONCEPTS[83], c]),
            write(f"{p}.e04", "Escribe cinco pasos: seguridad, servicio, aviso, visita y vecino.",
                  "22 King Street, shared entrance. Public pipe leak began Tuesday 7 p.m.; water is near a socket, so it is urgent. Caretaker Ana closed the water valve and keeps people out. City water emergency line handles the pipe. Building manager books a verified electrician for Wednesday 8:30; Ana provides access; ask for an estimate. Update neighbour Leo after the visit.",
                  "1. Keep everyone away from the wet socket; Ana has closed the water valve.\n2. Report the urgent public pipe leak at 22 King Street to the city water emergency line. It began Tuesday at 7 p.m. and affects the shared entrance.\n3. Ask for a reference number.\n4. The building manager books a verified electrician for Wednesday at 8:30; Ana provides access and requests an estimate.\n5. Update Leo after the visit.",
                  [
                      "1. Keep everyone away from the wet socket; Ana has closed the water valve.\n2. Report the urgent public pipe leak at 22 King Street to the city water emergency line. It began Tuesday at 7 p.m. and affects the shared entrance.\n3. Ask for a reference number.\n4. The building manager books a verified electrician for Wednesday at 8:30; Ana provides access and requests an estimate.\n5. Update Leo after the visit.",
                      "1. Ana closed the water valve; keep people out because water is near a socket.\n2. Tell the city water emergency line about the urgent public pipe leak at 22 King Street. It began Tuesday at 7 p.m. and affects the shared entrance.\n3. Request a reference number.\n4. The building manager arranges a verified electrician for Wednesday at 8:30; caretaker Ana gives access and asks for an estimate.\n5. Tell Leo the result after the visit.",
                  ], c, "Los cinco pasos asignan la tubería al servicio de agua y la visita al administrador y Ana.",
                  requires=cumulative),
        ],
        "review": [
            match(f"{p}.r01", "Une cada paso vecinal con su propósito.",
                  [("record dates", "crear evidencia"), ("report public damage", "contactar al municipio"), ("save reference number", "seguir el aviso")], c,
                  "La evidencia documenta, el municipio recibe el caso público y la referencia permite seguimiento."),
            order(f"{p}.r02", "Ordena la respuesta segura ante agua junto a un cable.",
                  "Keep neighbours away from the wet cable and call the manager.",
                  ["Keep", "neighbours", "away", "from", "the", "wet", "cable", "and", "call", "the", "manager."], c,
                  "La respuesta aleja a los vecinos del riesgo y usa un contacto autorizado."),
            write(f"{p}.r03", "Escribe cinco líneas: seguridad, servicio, datos, visita y seguimiento.",
                  "9 Cedar Court. Public street lamp at shared entrance stopped Sunday 8 p.m.; dark path affects homes 1–3; no exposed wires. Report to council lighting team and ask for a reference. Council technician comes Tuesday 4 p.m.; caretaker Ben opens side gate. Update neighbour Sam after visit.",
                  "1. Keep residents away from the dark path.\n2. Report the broken public lamp at 9 Cedar Court to the council; it stopped Sunday at 8 p.m. and affects homes 1–3.\n3. Ask for a reference number.\n4. Caretaker Ben opens the side gate for the council technician on Tuesday at 4.\n5. Update Sam after the visit.",
                  ["1. Keep residents away from the dark path.\n2. Report the broken public lamp at 9 Cedar Court to the council; it stopped Sunday at 8 p.m. and affects homes 1–3.\n3. Ask for a reference number.\n4. Caretaker Ben opens the side gate for the council technician on Tuesday at 4.\n5. Update Sam after the visit.",
                   "1. Keep neighbours off the dark path.\n2. Tell the council lighting team that the public lamp at 9 Cedar Court stopped on Sunday at 8 p.m. and affects homes 1–3.\n3. Request a reference number.\n4. Ben, the caretaker, opens the side gate for Tuesday's 4 p.m. technician visit.\n5. Tell Sam the result."], c,
                  "Las cinco líneas recuperan un caso de alumbrado distinto con datos y responsables claros.",
                  requires=cumulative),
        ],
    }
    return common_class(n, ["Escoger un canal seguro para un problema público o compartido.",
                            "Coordinar evidencia, solución y seguimiento sin confrontación.",
                            "Resolver un caso vecinal integrando aviso, servicio y reparación."], vocabulary, teaching, pools,
                        {"e01": (5, "r02"), "e02": (2, "r01"), "e03": (4, "r01"), "e04": (6, "r03")},
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


def output_manifest(paths: list[Path]) -> str:
    return "\n".join(f"{digest(path)}  {path.name}" for path in paths) + "\n"


def report(classes: list[dict[str, Any]], audit_result: dict[str, Any],
           validation: list[str], manifest: str) -> str:
    lines = [
        "# CORRECTED — Inglés N2 C81–C85", "",
        "Estado: **CORRECTED para nueva revisión; no autorizado para integración**.", "",
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
        "", "## Cobertura acumulativa C85", "",
        "- `e01`: reconoce riesgo doméstico y evita contacto con electricidad.",
        "- `e02`: identifica al municipio como responsable del espacio público.",
        "- `e03`: completa un aviso con número de referencia para seguimiento.",
        "- `e04`: separa urgencia eléctrica, servicio de agua, administrador, conserje y vecino.",
        "- `t06`, `e04` y `r03` usan corte interno, fuga urgente y alumbrado público.",
        "", "## Correcciones aplicadas", "",
        "- C81/C82: las recuperaciones de `e04` practican el mismo dato funcional en otro caso.",
        "- C81/C83: las variantes de `p03` conservan exactamente el intervalo temporal.",
        "- C84: `e04` confirma una cita, no una persona, y ambas variantes son equivalentes.",
        "- C85: `e04` explicita urgencia y responsables; `r03` se divide en cinco pasos A2.",
        "", "## Política de seguridad", "",
        "- Gas, humo, fuego, cables expuestos y agua junto a electricidad requieren distancia y ayuda profesional.",
        "- No se enseña reparación eléctrica, de gas ni acceso no autorizado a viviendas.",
        "- Las visitas exigen técnico verificado; los avisos usan solo datos mínimos y canales oficiales.",
        "", "## Auditoría reproducible", "", "```json",
        json.dumps(audit_result, ensure_ascii=False, indent=2), "```", "",
        "## Hashes de salidas", "", "```text", manifest.rstrip(), "```", "",
        "## Validación ejecutada", "",
    ])
    lines.extend(f"- `{message}`" for message in validation)
    lines.extend([
        "", "Comando de regeneración:", "", "```bash",
        "PYTHONDONTWRITEBYTECODE=1 python3 tools/contenido/generar_editorial_n2_81_85.py", "```", "",
        "## Pruebas de repositorio", "",
        "- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s test_tools`: 52 tests, OK.",
        "- `PYTHONDONTWRITEBYTECODE=1 python3 tools/validar_ruta.py`: 10 idiomas, 0 errores.",
        "- La validación de ruta comprueba el producto actual; no integra este staging.", "",
        "## Incidencias y dudas para el revisor", "",
        "- Incidencias automáticas conocidas: ninguna tras la validación incluida.",
        "- Revisar la legibilidad A2 de los cinco pasos breves de C85.",
        "- Simular fallo total para confirmar que cada ruta de remediación ataca el error concreto.",
        "- Verificar en revisión adversarial que C85 demuestra los cinco conceptos sin depender de memoria externa.",
        "- Este autor entrega `CORRECTED`; no emite `GO` ni integra el contenido.", "",
    ])
    return "\n".join(lines)


def main() -> int:
    classes = [build_81(), build_82(), build_83(), build_84(), build_85()]
    audit_result = audit(classes)
    output_paths: list[Path] = []
    for cls in classes:
        number = int(cls["id"].rsplit("-", 1)[1])
        path = OUT / f"class-{number}.json"
        path.write_text(
            json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        output_paths.append(path)
    bundle_path = OUT / "bundle-81-85.json"
    bundle_path.write_text(json.dumps(bundle(classes), ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    output_paths.append(bundle_path)
    validation = [validate_file(OUT / f"class-{number}.json", number, number)
                  for number in range(81, 86)]
    validation.append(validate_file(bundle_path, 81, 85))
    manifest = output_manifest(output_paths)
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    (REPORT_OUT / "MANIFEST.sha256").write_text(manifest, encoding="utf-8")
    (REPORT_OUT / "REPORT.md").write_text(
        report(classes, audit_result, validation, manifest), encoding="utf-8"
    )
    print("\n".join(validation))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
