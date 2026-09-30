#!/usr/bin/env python3
"""Regenera las clases editoriales de Inglés N2 C56-C60."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n2"
SCALE = "client-10-levels-v1"
CONCEPTS = {
    56: "n2-have-to-necessity",
    57: "n2-must-rules",
    58: "n2-should-advice",
    59: "n2-explain-rules-advice",
    60: "n2-practical-advice-guide",
}
PHASES = {56: "input", 57: "form", 58: "comprehension", 59: "production", 60: "transfer"}
TITLES = {
    56: ("Have to and don't have to", "Have to y don't have to"),
    57: ("Must and mustn't", "Must y mustn't"),
    58: ("Should and shouldn't", "Should y shouldn't"),
    59: ("Explain rules and advice", "Explicar reglas y consejos"),
    60: ("A practical advice guide", "Una guía práctica de consejos"),
}
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
EXPECTED_BLOCK_INDICES = Counter({0: 7, 1: 6, 2: 7})


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def add_hash(item: dict[str, Any]) -> dict[str, Any]:
    payload = {key: value for key, value in item.items() if key not in {"id", "contentHash"}}
    item["contentHash"] = digest(payload)
    return item


def access() -> dict[str, bool]:
    return {"screenReader": True, "highContrast": True, "largeText": True}


def base_item(
    item_id: str,
    fmt: str,
    prompt: str,
    concept: str,
    pool: str,
    feedback: str,
    *,
    requires: list[str] | None = None,
    hint: str | None = None,
) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": hint or "Identifica primero la función comunicativa de la oración."}
    return {
        "id": item_id,
        "format": fmt,
        "prompt": {"es": prompt},
        "answer": {},
        "choices": [],
        "teaches": [concept] if pool == "practiceGuided" else [],
        "requires": [] if pool == "practiceGuided" else list(requires or [concept]),
        "origin": origin,
        "accessibility": access(),
    }


def choice(
    item_id: str,
    prompt: str,
    options: list[str],
    index: int,
    concept: str,
    pool: str,
    feedback: str,
    *,
    requires: list[str] | None = None,
    hint: str | None = None,
) -> dict[str, Any]:
    item = base_item(item_id, "elegir", prompt, concept, pool, feedback, requires=requires, hint=hint)
    item["choices"] = [{"text": value} for value in options]
    item["answer"] = {"index": index}
    return add_hash(item)


def listen(
    item_id: str,
    prompt: str,
    audio: str,
    options: list[str],
    index: int,
    concept: str,
    pool: str,
    feedback: str,
    *,
    requires: list[str] | None = None,
    hint: str | None = None,
) -> dict[str, Any]:
    item = base_item(item_id, "escuchar", prompt, concept, pool, feedback, requires=requires, hint=hint)
    item["choices"] = [{"text": value} for value in options]
    item["answer"] = {"index": index}
    item["origin"].update(
        {
            "audio": audio,
            "audioMode": "tts",
            "languageCode": "en",
            "speedOptions": [0.75, 1.0],
            "maxReplays": 3,
            "revealTranscriptAfterAttempt": True,
        }
    )
    return add_hash(item)


def complete(
    item_id: str,
    prompt: str,
    answer: str,
    concept: str,
    pool: str,
    feedback: str,
    *,
    requires: list[str] | None = None,
    hint: str | None = None,
) -> dict[str, Any]:
    item = base_item(item_id, "completar", prompt, concept, pool, feedback, requires=requires, hint=hint)
    item["answer"] = {"text": answer, "accepted": [answer]}
    return add_hash(item)


def order(
    item_id: str,
    prompt: str,
    answer: str,
    concept: str,
    pool: str,
    feedback: str,
    *,
    requires: list[str] | None = None,
    hint: str | None = None,
) -> dict[str, Any]:
    item = base_item(item_id, "ordenar", prompt, concept, pool, feedback, requires=requires, hint=hint)
    item["answer"] = {"text": answer, "tokens": answer.split()}
    return add_hash(item)


def write(
    item_id: str,
    prompt: str,
    stimulus: str,
    answer: str,
    alternative: str,
    concept: str,
    pool: str,
    feedback: str,
    *,
    requires: list[str] | None = None,
    hint: str | None = None,
) -> dict[str, Any]:
    item = base_item(item_id, "escribir", prompt, concept, pool, feedback, requires=requires, hint=hint)
    item["answer"] = {"text": answer, "accepted": [answer, alternative]}
    item["origin"]["text"] = stimulus
    return add_hash(item)


def match(
    item_id: str,
    prompt: str,
    pairs: list[tuple[str, str]],
    concept: str,
    pool: str,
    feedback: str,
    *,
    requires: list[str] | None = None,
    hint: str | None = None,
) -> dict[str, Any]:
    item = base_item(item_id, "relacionar", prompt, concept, pool, feedback, requires=requires, hint=hint)
    values = [[left, {"es": right}] for left, right in pairs]
    item["answer"] = {"pairs": values}
    item["origin"]["pairs"] = values
    return add_hash(item)


def teaching(class_number: int, entries: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    concept = CONCEPTS[class_number]
    result = []
    for number, (english, spanish, explanation) in enumerate(entries, 1):
        en_words = english.split()
        es_words = spanish.split()
        en_mid = max(1, len(en_words) // 2)
        es_mid = max(1, len(es_words) // 2)
        result.append(
            {
                "id": f"en.n2.class-{class_number}.t{number:02d}",
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
                "patternId": concept,
            }
        )
    return result


def common_class(
    number: int,
    objectives: list[str],
    vocabulary: list[tuple[str, str]],
    lessons: list[tuple[str, str, str]],
    pools: dict[str, list[dict[str, Any]]],
    remediation: dict[str, tuple[str, str]],
    *,
    cumulative: list[str] | None = None,
    uses_patterns: list[str] | None = None,
) -> dict[str, Any]:
    concept = CONCEPTS[number]
    prefix = f"en.n2.c{number}"
    result: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1",
        "course": "en",
        "level": 2,
        "cefr": "A2",
        "scale": SCALE,
        "status": "shadow",
        "runtimeAi": False,
        "phase": PHASES[number],
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY_POLICY),
        "id": f"en.n2.class-{number}",
        "title": {"en": TITLES[number][0], "es": TITLES[number][1]},
        "objectives": {"es": objectives},
        "concepts": [concept],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n2.class-{number - 1}"],
        "usesVocabulary": [english for english, _ in vocabulary],
        "usesPatterns": list(uses_patterns or [concept]),
        "vocabulary": [{"en": english, "es": spanish} for english, spanish in vocabulary],
        "teaching": teaching(number, lessons),
        "pools": pools,
        "remediationMap": {
            eval_id: {"reteach": reteach, "review": review}
            for eval_id, (reteach, review) in remediation.items()
        },
        "accessibility": {
            "highContrast": True,
            "largeText": True,
            "screenReader": True,
            "audioReplay": True,
        },
        "recovery": {
            "retryPool": "review",
            "maxAttempts": 2,
            "allowAudioReplay": True,
            "preserveProgress": True,
        },
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if cumulative is not None:
        result["cumulativeEvaluation"] = cumulative
    assert set(result["remediationMap"]) == {f"{prefix}.e0{i}" for i in range(1, 5)}
    return result


def build_56() -> dict[str, Any]:
    n, c, p = 56, CONCEPTS[56], "en.n2.c56"
    pools = {
        "practiceGuided": [
            choice(
                f"{p}.pg01",
                "La empresa exige identificación. Elige la obligación correcta.",
                [
                    "Staff have to wear an ID badge.",
                    "Staff don't have to wear an ID badge.",
                    "Staff mustn't wear an ID badge.",
                ],
                0,
                c,
                "practiceGuided",
                "Have to expresa el requisito externo de llevar identificación.",
                hint="Busca have to cuando una empresa o norma crea la obligación.",
            ),
            complete(
                f"{p}.pg02",
                "Usa has to: Maya ___ register before the morning shift.",
                "has to",
                c,
                "practiceGuided",
                "Has to concuerda con Maya y mantiene la necesidad de registrarse.",
                hint="Con he, she o un nombre singular se usa has to.",
            ),
            order(
                f"{p}.pg03",
                "Ordena la pregunta sobre el uniforme de los visitantes.",
                "Do visitors have to wear a uniform?",
                c,
                "practiceGuided",
                "Do inicia la pregunta y have to conserva la idea de requisito.",
                hint="Empieza con Do, sigue con el sujeto y termina con el verbo base.",
            ),
        ],
        "practice": [
            write(
                f"{p}.p01",
                "Escribe en inglés: Debemos revisar el horario antes del turno.",
                "Debemos revisar el horario antes del turno.",
                "We have to check the schedule before the shift.",
                "Before the shift, we have to check the schedule.",
                c,
                "practice",
                "Have to check comunica una tarea exigida antes de comenzar el turno.",
            ),
            listen(
                f"{p}.p02",
                "Escucha y elige la frase que indica que algo no es necesario.",
                "You don't have to bring equipment; we provide it.",
                [
                    "You have to bring your own equipment.",
                    "You don't have to bring equipment; we provide it.",
                    "You mustn't use the equipment.",
                ],
                1,
                c,
                "practice",
                "Don't have to significa que traer equipo no es necesario porque ya lo proporcionan.",
            ),
            match(
                f"{p}.p03",
                "Relaciona palabras de necesidad y organización con su significado.",
                [("necessary", "necesario"), ("schedule", "horario")],
                c,
                "practice",
                "Necessary nombra una necesidad y schedule organiza los horarios de trabajo.",
            ),
        ],
        "evaluation": [
            choice(
                f"{p}.e01",
                "La capacitación es obligatoria. Elige la oración que expresa ese requisito.",
                [
                    "New staff don't have to attend the safety class.",
                    "New staff mustn't attend the safety class.",
                    "New staff have to attend the safety class.",
                ],
                2,
                c,
                "evaluation",
                "Have to attend convierte la capacitación obligatoria en un requisito claro.",
            ),
            complete(
                f"{p}.e02",
                "La oficina cierra los domingos: Leo ___ wear a uniform that day.",
                "doesn't have to",
                c,
                "evaluation",
                "Doesn't have to indica ausencia de necesidad y concuerda con Leo.",
            ),
            write(
                f"{p}.e03",
                "Escribe: Ana tiene que registrar su identificación antes del turno nocturno.",
                "Ana tiene que registrar su identificación antes del turno nocturno.",
                "Ana has to register her ID before the night shift.",
                "Before the night shift, Ana has to register her ID.",
                c,
                "evaluation",
                "Has to register expresa el requisito de Ana y sitúa la acción antes del turno.",
            ),
            listen(
                f"{p}.e04",
                "Escucha y elige la pregunta sobre una obligación externa.",
                "Do contractors have to follow this schedule?",
                [
                    "Are contractors following this schedule today?",
                    "Do contractors have to follow this schedule?",
                    "Should contractors follow a different schedule?",
                ],
                1,
                c,
                "evaluation",
                "Do contractors have to pregunta si el horario es obligatorio para ellos.",
            ),
        ],
        "review": [
            match(
                f"{p}.r01",
                "Relaciona cada expresión con la función que comunica.",
                [("have to wear an ID badge", "obligación"), ("don't have to bring equipment", "no es necesario")],
                c,
                "review",
                "Have to marca obligación, mientras don't have to elimina la necesidad.",
            ),
            order(
                f"{p}.r02",
                "Ordena la pregunta sobre el registro de Nora.",
                "Does Nora have to register before noon?",
                c,
                "review",
                "Does Nora have to mantiene have en forma base dentro de la pregunta.",
            ),
            write(
                f"{p}.r03",
                "Escribe: No tenemos que traer uniformes para la visita.",
                "No tenemos que traer uniformes para la visita.",
                "We don't have to bring uniforms for the visit.",
                "For the visit, we do not have to bring uniforms.",
                c,
                "review",
                "Don't have to bring aclara que los uniformes no son necesarios en la visita.",
            ),
        ],
    }
    remediation = {
        f"{p}.e01": (f"en.n2.class-{n}.t01", f"{p}.r01"),
        f"{p}.e02": (f"en.n2.class-{n}.t02", f"{p}.r03"),
        f"{p}.e03": (f"en.n2.class-{n}.t03", f"{p}.r02"),
        f"{p}.e04": (f"en.n2.class-{n}.t04", f"{p}.r02"),
    }
    return common_class(
        n,
        [
            "Distinguir obligación externa de ausencia de necesidad con have to y don't have to.",
            "Formar afirmaciones, negativas y preguntas de necesidad en contextos laborales.",
            "Comunicar por escrito requisitos concretos con persona, acción y momento.",
        ],
        [
            ("badge", "credencial"),
            ("uniform", "uniforme"),
            ("shift", "turno"),
            ("register", "registrarse"),
            ("ID", "identificación"),
            ("equipment", "equipo"),
            ("necessary", "necesario"),
            ("schedule", "horario"),
        ],
        [
            (
                "Employees have to wear an ID badge during every shift.",
                "Los empleados tienen que llevar una credencial en cada turno.",
                "Have to expresa una obligación externa creada por el lugar de trabajo.",
            ),
            (
                "It isn't necessary to bring equipment; you don't have to bring it.",
                "No es necesario traer equipo; no tienes que traerlo.",
                "Don't have to significa ausencia de necesidad, no una prohibición.",
            ),
            (
                "Maya has to register before her first shift.",
                "Maya tiene que registrarse antes de su primer turno.",
                "Con he, she o un nombre singular, have to cambia a has to.",
            ),
            (
                "Do visitors have to wear a uniform?",
                "¿Los visitantes tienen que llevar uniforme?",
                "Las preguntas de obligación usan do o does antes del sujeto.",
            ),
        ],
        pools,
        remediation,
    )


def build_57() -> dict[str, Any]:
    n, c, p = 57, CONCEPTS[57], "en.n2.c57"
    pools = {
        "practiceGuided": [
            choice(
                f"{p}.pg01",
                "La norma de seguridad exige casco. Elige la regla correcta.",
                [
                    "Workers should wear a helmet in this area.",
                    "Workers must wear a helmet in this area.",
                    "Workers don't have to wear a helmet in this area.",
                ],
                1,
                c,
                "practiceGuided",
                "Must wear presenta el casco como una regla obligatoria de seguridad.",
                hint="Must expresa una regla firme; should solo comunica consejo.",
            ),
            complete(
                f"{p}.pg02",
                "Usa mustn't: You ___ touch the emergency button without permission.",
                "mustn't",
                c,
                "practiceGuided",
                "Mustn't touch prohíbe usar el botón sin permiso.",
                hint="La acción está prohibida, así que necesitas mustn't.",
            ),
            order(
                f"{p}.pg03",
                "Ordena la regla de acceso por la entrada principal.",
                "Everyone must use the main entrance.",
                c,
                "practiceGuided",
                "Must va antes del verbo base use para formular la regla de entrada.",
                hint="Coloca must entre el sujeto y el verbo base.",
            ),
        ],
        "practice": [
            write(
                f"{p}.p01",
                "Escribe: Debes obtener permiso en el mostrador de seguridad.",
                "Debes obtener permiso en el mostrador de seguridad.",
                "You must get permission at the safety desk.",
                "At the safety desk, you must get permission.",
                c,
                "practice",
                "Must get permission comunica una condición obligatoria para obtener acceso.",
            ),
            listen(
                f"{p}.p02",
                "Escucha y selecciona la prohibición durante una emergencia.",
                "Passengers mustn't block the emergency exit.",
                [
                    "Passengers should avoid the emergency exit.",
                    "Passengers don't have to use the emergency exit.",
                    "Passengers mustn't block the emergency exit.",
                ],
                2,
                c,
                "practice",
                "Mustn't block prohíbe obstruir una salida que debe quedar libre.",
            ),
            match(
                f"{p}.p03",
                "Relaciona cada aviso con el tipo de regla.",
                [("Wear a helmet", "obligación"), ("Do not touch", "prohibición")],
                c,
                "practice",
                "Wear a helmet exige protección; Do not touch impide una acción peligrosa.",
            ),
        ],
        "evaluation": [
            choice(
                f"{p}.e01",
                "El protocolo exige lavarse las manos. Elige la regla firme.",
                [
                    "Kitchen staff must wash their hands before work.",
                    "Kitchen staff should wash their hands before work.",
                    "Kitchen staff don't have to wash their hands before work.",
                ],
                0,
                c,
                "evaluation",
                "Must wash expresa el requisito obligatorio del protocolo de cocina.",
            ),
            complete(
                f"{p}.e02",
                "Solo personal autorizado: Guests ___ enter through this door.",
                "mustn't",
                c,
                "evaluation",
                "Mustn't enter convierte el acceso restringido en una prohibición inequívoca.",
            ),
            write(
                f"{p}.e03",
                "Escribe la regla: gafas obligatorias; no tocar las muestras.",
                "En el laboratorio, las gafas son obligatorias y está prohibido tocar las muestras.",
                "In the lab, you must wear safety glasses and mustn't touch the samples.",
                "You must wear safety glasses in the lab, and you must not touch the samples.",
                c,
                "evaluation",
                "Must wear y mustn't touch separan obligación y prohibición dentro del laboratorio.",
            ),
            listen(
                f"{p}.e04",
                "Escucha y elige la instrucción indicada por la señal.",
                "This sign says we must use the west entrance.",
                [
                    "This sign suggests the west entrance.",
                    "This sign says the west entrance is optional.",
                    "This sign says we must use the west entrance.",
                ],
                2,
                c,
                "evaluation",
                "Must use muestra que la señal impone una entrada específica.",
            ),
        ],
        "review": [
            match(
                f"{p}.r01",
                "Relaciona las reglas con obligación o prohibición.",
                [("must protect your eyes", "obligación"), ("mustn't touch the sign", "prohibición")],
                c,
                "review",
                "Must exige protegerse y mustn't impide tocar una señal de seguridad.",
            ),
            order(
                f"{p}.r02",
                "Ordena la prohibición durante una emergencia.",
                "You mustn't use the lift during an emergency.",
                c,
                "review",
                "Mustn't use expresa que el ascensor está prohibido durante la emergencia.",
            ),
            write(
                f"{p}.r03",
                "Escribe: Los ciclistas deben usar casco y no bloquear la entrada.",
                "Los ciclistas deben usar casco y no bloquear la entrada.",
                "Cyclists must wear a helmet and mustn't block the entrance.",
                "Cyclists must wear helmets, and they must not block the entrance.",
                c,
                "review",
                "La oración combina una protección obligatoria y una acción prohibida.",
            ),
        ],
    }
    remediation = {
        f"{p}.e01": (f"en.n2.class-{n}.t01", f"{p}.r01"),
        f"{p}.e02": (f"en.n2.class-{n}.t02", f"{p}.r02"),
        f"{p}.e03": (f"en.n2.class-{n}.t03", f"{p}.r03"),
        f"{p}.e04": (f"en.n2.class-{n}.t04", f"{p}.r01"),
    }
    return common_class(
        n,
        [
            "Interpretar must como regla obligatoria y mustn't como prohibición explícita.",
            "Construir normas breves con modal y verbo base sin añadir to.",
            "Redactar instrucciones de seguridad que combinen obligación y prohibición.",
        ],
        [
            ("helmet", "casco"),
            ("entrance", "entrada"),
            ("emergency", "emergencia"),
            ("permission", "permiso"),
            ("safety", "seguridad"),
            ("touch", "tocar"),
            ("sign", "señal"),
            ("protect", "proteger"),
        ],
        [
            (
                "Workers must wear a helmet in the safety area.",
                "Los trabajadores deben usar casco en la zona de seguridad.",
                "Must comunica una regla firme y va seguido del verbo base wear.",
            ),
            (
                "Visitors mustn't touch the red emergency button.",
                "Los visitantes no deben tocar el botón rojo de emergencia.",
                "Mustn't expresa prohibición; no significa que la acción sea opcional.",
            ),
            (
                "During an emergency, everyone must use the main entrance.",
                "Durante una emergencia, todos deben usar la entrada principal.",
                "Must y mustn't no cambian con la persona y siempre conservan el verbo base.",
            ),
            (
                "A safety sign can protect visitors: You mustn't enter without permission.",
                "Una señal de seguridad puede proteger a los visitantes: no deben entrar sin permiso.",
                "Las señales usan must o mustn't para comunicar reglas directas y visibles.",
            ),
        ],
        pools,
        remediation,
    )


def build_58() -> dict[str, Any]:
    n, c, p = 58, CONCEPTS[58], "en.n2.c58"
    pools = {
        "practiceGuided": [
            choice(
                f"{p}.pg01",
                "Leo tiene dolor de cabeza. Elige un consejo adecuado.",
                [
                    "Leo has to finish his shift before he rests.",
                    "Leo doesn't have to change his schedule today.",
                    "Leo should rest in a quiet room.",
                ],
                2,
                c,
                "practiceGuided",
                "Should rest ofrece una recomendación útil sin convertirla en obligación.",
                hint="Should introduce un consejo; must comunica una regla firme.",
            ),
            complete(
                f"{p}.pg02",
                "Completa el consejo: You ___ use the screen for hours without a break.",
                "shouldn't",
                c,
                "practiceGuided",
                "Shouldn't use aconseja evitar un hábito que puede cansar la vista.",
                hint="La recomendación es evitar la acción, así que usa shouldn't.",
            ),
            order(
                f"{p}.pg03",
                "Ordena el consejo para una tos que empeora.",
                "You should make an appointment for that cough.",
                c,
                "practiceGuided",
                "Should make recomienda pedir una cita a causa de la tos.",
                hint="Coloca should antes del verbo base make.",
            ),
        ],
        "practice": [
            write(
                f"{p}.p01",
                "Escribe: Para reducir el estrés, deberías caminar después del trabajo.",
                "Para reducir el estrés, deberías caminar después del trabajo.",
                "To reduce stress, you should walk after work.",
                "You should take a walk after work to reduce stress.",
                c,
                "practice",
                "Should walk presenta una acción recomendable para reducir el estrés.",
            ),
            listen(
                f"{p}.p02",
                "Escucha y elige el consejo sobre una rutina saludable.",
                "You shouldn't skip breakfast; a healthy meal can improve your morning.",
                [
                    "You shouldn't skip breakfast; a healthy meal can improve your morning.",
                    "You have to eat breakfast before seven every morning.",
                    "You don't have to change your breakfast routine.",
                ],
                0,
                c,
                "practice",
                "Shouldn't skip aconseja conservar un desayuno saludable para mejorar la mañana.",
            ),
            match(
                f"{p}.p03",
                "Relaciona cada problema con una acción útil.",
                [("headache", "rest in a quiet room"), ("cough", "make an appointment")],
                c,
                "practice",
                "El descanso puede ayudar con el dolor de cabeza y una cita permite revisar la tos.",
            ),
        ],
        "evaluation": [
            choice(
                f"{p}.e01",
                "Una amiga está agotada. Elige el consejo, no una regla.",
                [
                    "She has to finish all her work before bedtime.",
                    "She should go to bed earlier.",
                    "She doesn't have to change her sleep schedule.",
                ],
                1,
                c,
                "evaluation",
                "Should go ofrece una recomendación razonable para alguien agotado.",
            ),
            complete(
                f"{p}.e02",
                "El café causa dolor de cabeza: You ___ drink it late at night.",
                "shouldn't",
                c,
                "evaluation",
                "Shouldn't drink aconseja evitar el café tarde por su efecto negativo.",
            ),
            write(
                f"{p}.e03",
                "Escribe el consejo: descansa de la pantalla porque te duelen los ojos.",
                "Descansa de la pantalla porque te duelen los ojos.",
                "You should take a screen break because your eyes hurt.",
                "You should look away from the screen and rest your eyes because they hurt.",
                c,
                "evaluation",
                "Should take y because conectan el consejo con la razón visible.",
            ),
            listen(
                f"{p}.e04",
                "Escucha y selecciona la pregunta que solicita consejo.",
                "What should I do to reduce stress?",
                [
                    "What should I do to reduce stress?",
                    "What mustn't I do in the laboratory?",
                    "What don't I have to do before the meeting?",
                ],
                0,
                c,
                "evaluation",
                "What should I do pide una recomendación para manejar el estrés.",
            ),
        ],
        "review": [
            match(
                f"{p}.r01",
                "Relaciona la forma de consejo con su función.",
                [("should", "acción recomendable"), ("shouldn't", "acción que conviene evitar")],
                c,
                "review",
                "Should propone una acción útil y shouldn't recomienda evitarla.",
            ),
            order(
                f"{p}.r02",
                "Ordena el consejo para pedir una cita en la clínica.",
                "You should call the clinic for an appointment.",
                c,
                "review",
                "Should call recomienda contactar la clínica para obtener una cita.",
            ),
            write(
                f"{p}.r03",
                "Escribe: Para mejorar el sueño, deberías apagar la pantalla temprano.",
                "Para mejorar el sueño, deberías apagar la pantalla temprano.",
                "To improve your sleep, you should turn off the screen early.",
                "You should switch off the screen early to improve your sleep.",
                c,
                "review",
                "Should turn off formula un consejo saludable con un propósito concreto.",
            ),
        ],
    }
    remediation = {
        f"{p}.e01": (f"en.n2.class-{n}.t01", f"{p}.r01"),
        f"{p}.e02": (f"en.n2.class-{n}.t02", f"{p}.r01"),
        f"{p}.e03": (f"en.n2.class-{n}.t03", f"{p}.r03"),
        f"{p}.e04": (f"en.n2.class-{n}.t04", f"{p}.r02"),
    }
    return common_class(
        n,
        [
            "Distinguir consejos con should y acciones que conviene evitar con shouldn't.",
            "Relacionar recomendaciones de salud cotidiana con una razón comprensible.",
            "Pedir y redactar consejos breves para problemas comunes de nivel A2.",
        ],
        [
            ("rest", "descansar"),
            ("cough", "tos"),
            ("screen", "pantalla"),
            ("appointment", "cita"),
            ("healthy", "saludable"),
            ("headache", "dolor de cabeza"),
            ("stress", "estrés"),
            ("improve", "mejorar"),
        ],
        [
            (
                "You should rest if you have a headache.",
                "Deberías descansar si tienes dolor de cabeza.",
                "Should ofrece un consejo; no presenta la acción como una obligación.",
            ),
            (
                "You shouldn't stare at a screen when your eyes hurt.",
                "No deberías mirar una pantalla cuando te duelen los ojos.",
                "Shouldn't recomienda evitar una acción que puede empeorar el problema.",
            ),
            (
                "You should make an appointment because your cough is getting worse.",
                "Deberías pedir una cita porque tu tos está empeorando.",
                "Because añade la razón que sostiene la recomendación.",
            ),
            (
                "What should I change to build a healthy routine and improve my sleep?",
                "¿Qué debería cambiar para crear una rutina saludable y mejorar mi sueño?",
                "What should I change permite pedir consejo sobre un cambio concreto.",
            ),
        ],
        pools,
        remediation,
    )


def build_59() -> dict[str, Any]:
    n, c, p = 59, CONCEPTS[59], "en.n2.c59"
    pools = {
        "practiceGuided": [
            choice(
                f"{p}.pg01",
                "El registro es obligatorio. Elige la regla, no el consejo.",
                [
                    "Visitors must sign in at reception.",
                    "Visitors should sign in if they have time.",
                    "Visitors don't have to sign in at reception.",
                ],
                0,
                c,
                "practiceGuided",
                "Must sign in presenta el registro como una regla obligatoria.",
                hint="Una regla firme usa must; un consejo usa should.",
            ),
            complete(
                f"{p}.pg02",
                "El boleto es digital: You ___ print it before the visit.",
                "don't have to",
                c,
                "practiceGuided",
                "Don't have to print indica que la copia en papel es opcional.",
                hint="La acción no es necesaria, pero tampoco está prohibida.",
            ),
            order(
                f"{p}.pg03",
                "Ordena el consejo y la razón sobre la fila de entrada.",
                "You should arrive early because the line is long.",
                c,
                "practiceGuided",
                "Should arrive comunica consejo y because explica la razón.",
                hint="Empieza con el sujeto, añade should y deja la razón después de because.",
            ),
        ],
        "practice": [
            write(
                f"{p}.p01",
                "Escribe la regla: Los visitantes deben mostrar identificación en la entrada.",
                "Los visitantes deben mostrar identificación en la entrada.",
                "Visitors must show ID at the entrance.",
                "At the entrance, visitors have to show ID.",
                c,
                "practice",
                "Must show presenta la identificación como requisito de acceso.",
            ),
            listen(
                f"{p}.p02",
                "Escucha y elige el consejo, no la obligación.",
                "You should bring water; it is useful advice for a hot day.",
                [
                    "You must bring water; it is a required rule.",
                    "You mustn't bring water into the building.",
                    "You should bring water; it is useful advice for a hot day.",
                ],
                2,
                c,
                "practice",
                "Should bring presenta el agua como recomendación útil, no como requisito.",
            ),
            match(
                f"{p}.p03",
                "Relaciona cada palabra con su valor dentro de una norma.",
                [("required", "obligatorio"), ("optional", "no obligatorio"), ("reason", "explicación")],
                c,
                "practice",
                "Required exige, optional permite elegir y reason explica por qué existe la indicación.",
            ),
        ],
        "evaluation": [
            choice(
                f"{p}.e01",
                "El aviso recomienda silencio, pero no lo exige. Elige la frase adecuada.",
                [
                    "Visitors must speak quietly in the hall.",
                    "Visitors should speak quietly in the hall.",
                    "Visitors mustn't speak in the hall.",
                ],
                1,
                c,
                "evaluation",
                "Should speak quietly conserva el carácter recomendado del aviso.",
            ),
            complete(
                f"{p}.e02",
                "La fotografía está prohibida: Guests ___ take pictures inside.",
                "mustn't",
                c,
                "evaluation",
                "Mustn't take transforma la prohibición del aviso en una regla directa.",
            ),
            write(
                f"{p}.e03",
                "Redacta: casco obligatorio; llevar agua es consejo porque hace calor.",
                "Casco obligatorio; llevar agua es consejo porque hace calor.",
                "Visitors must wear a helmet, and they should bring water because it is hot.",
                "Visitors have to wear a helmet; they should also carry water because it is hot.",
                c,
                "evaluation",
                "Must distingue la regla y should presenta el agua como consejo con razón.",
            ),
            listen(
                f"{p}.e04",
                "Escucha y elige la prohibición explicada por el aviso.",
                "The notice says you mustn't enter because the floor is wet.",
                [
                    "The notice says you shouldn't enter because the floor may be slippery.",
                    "The notice says you don't have to use this entrance while the floor is wet.",
                    "The notice says you mustn't enter because the floor is wet.",
                ],
                2,
                c,
                "evaluation",
                "Mustn't enter comunica la prohibición y because aporta su causa.",
            ),
        ],
        "review": [
            match(
                f"{p}.r01",
                "Relaciona cada modal con el tipo de mensaje.",
                [("must / mustn't", "regla"), ("should / shouldn't", "consejo")],
                c,
                "review",
                "Must y mustn't regulan acciones; should y shouldn't orientan decisiones.",
            ),
            order(
                f"{p}.r02",
                "Ordena la indicación sobre el boleto impreso.",
                "Visitors don't have to bring a printed ticket.",
                c,
                "review",
                "Don't have to bring explica que el boleto impreso es opcional.",
            ),
            write(
                f"{p}.r03",
                "Redacta: hablar bajo es regla; apagar notificaciones es consejo.",
                "Hablar bajo es regla; apagar notificaciones es consejo.",
                "Visitors must speak quietly and should turn off phone notifications.",
                "Visitors have to speak quietly; they should silence phone notifications.",
                c,
                "review",
                "La producción separa el comportamiento exigido de la recomendación práctica.",
            ),
        ],
    }
    remediation = {
        f"{p}.e01": (f"en.n2.class-{n}.t03", f"{p}.r01"),
        f"{p}.e02": (f"en.n2.class-{n}.t04", f"{p}.r01"),
        f"{p}.e03": (f"en.n2.class-{n}.t01", f"{p}.r03"),
        f"{p}.e04": (f"en.n2.class-{n}.t04", f"{p}.r01"),
    }
    return common_class(
        n,
        [
            "Clasificar indicaciones como regla, ausencia de necesidad o consejo.",
            "Explicar una regla o recomendación con una razón explícita y pertinente.",
            "Redactar mensajes que separen con claridad lo obligatorio de lo recomendable.",
        ],
        [
            ("rule", "regla"),
            ("advice", "consejo"),
            ("required", "obligatorio"),
            ("optional", "opcional"),
            ("prohibited", "prohibido"),
            ("reason", "razón"),
            ("visitor", "visitante"),
            ("notice", "aviso"),
        ],
        [
            (
                "Visitors must sign in; this is a required rule.",
                "Los visitantes deben registrarse; esta es una regla obligatoria.",
                "Must presenta la acción como una regla que el visitante debe cumplir.",
            ),
            (
                "Visitors have to show ID, but a printed ticket is optional.",
                "Los visitantes tienen que mostrar identificación, pero el boleto impreso es opcional.",
                "Have to marca necesidad externa; optional indica que otra acción no es necesaria.",
            ),
            (
                "You should arrive early; this is advice, not a rule.",
                "Deberías llegar temprano; es un consejo, no una regla.",
                "Should formula una recomendación que ayuda, pero no obliga.",
            ),
            (
                "The notice gives the reason: Entry is prohibited, so visitors mustn't use this door.",
                "El aviso da la razón: la entrada está prohibida, por eso los visitantes no deben usar esta puerta.",
                "Una explicación combina la indicación con una razón clara mediante because o so.",
            ),
        ],
        pools,
        remediation,
        uses_patterns=[CONCEPTS[number] for number in range(56, 60)],
    )


def build_60() -> dict[str, Any]:
    n, c, p = 60, CONCEPTS[60], "en.n2.c60"
    c56, c57, c58, c59 = (CONCEPTS[number] for number in range(56, 60))
    all_concepts = [CONCEPTS[number] for number in range(56, 61)]
    pools = {
        "practiceGuided": [
            choice(
                f"{p}.pg01",
                "La lista es obligatoria y dan los materiales. Elige la instrucción completa.",
                [
                    "You should read the checklist, and you may bring your own supplies.",
                    "You have to complete the checklist, but you don't have to bring supplies.",
                    "You must complete the checklist and bring all the supplies.",
                ],
                1,
                c,
                "practiceGuided",
                "Have to marca el paso obligatorio y don't have to elimina una carga innecesaria.",
                hint="Separa lo exigido de lo que ya proporciona la organización.",
            ),
            complete(
                f"{p}.pg02",
                "Usa mustn't: Visitors ___ enter the storage room.",
                "mustn't",
                c,
                "practiceGuided",
                "Mustn't enter convierte la advertencia en una prohibición directa.",
                hint="Una advertencia de acceso prohibido necesita mustn't.",
            ),
            order(
                f"{p}.pg03",
                "Ordena la recomendación sobre el contacto de primeros auxilios.",
                "You should save the first aid contact number.",
                c,
                "practiceGuided",
                "Should save presenta una precaución práctica para una emergencia.",
                hint="Coloca should antes del verbo base save.",
            ),
        ],
        "practice": [
            write(
                f"{p}.p01",
                "Escribe: Debes leer la advertencia; no necesitas llamar al contacto ahora.",
                "Debes leer la advertencia; no necesitas llamar al contacto ahora.",
                "You have to read the warning, but you don't have to call the contact now.",
                "Read the warning first; you do not have to call the contact now.",
                c,
                "practice",
                "La frase separa la lectura obligatoria de una llamada que aún no es necesaria.",
            ),
            listen(
                f"{p}.p02",
                "Escucha y elige la regla y el consejo sobre herramientas calientes.",
                "You must wear gloves, and you shouldn't touch hot tools.",
                [
                    "You must wear gloves, and you shouldn't touch hot tools.",
                    "You don't have to wear gloves, but you should ask before using hot tools.",
                    "You should wear gloves, and you mustn't use hot tools without help.",
                ],
                0,
                c,
                "practice",
                "Must wear fija la protección y shouldn't touch añade una recomendación preventiva.",
            ),
            match(
                f"{p}.p03",
                "Relaciona cada parte de la guía con su propósito.",
                [("warning", "evitar un peligro"), ("recommendation", "ofrecer ayuda práctica")],
                c,
                "practice",
                "La advertencia previene peligro y la recomendación orienta una decisión útil.",
            ),
        ],
        "evaluation": [
            choice(
                f"{p}.e01",
                "La guía exige actuar ante una lesión. Elige la instrucción obligatoria.",
                [
                    "You don't have to contact the first aid officer after an injury.",
                    "You shouldn't contact the first aid officer after an injury.",
                    "You must contact the first aid officer after an injury.",
                ],
                2,
                c,
                "evaluation",
                "Must contact presenta el aviso a primeros auxilios como acción obligatoria.",
                requires=[c57, c],
            ),
            complete(
                f"{p}.e02",
                "La guía proporciona materiales: Participants ___ bring their own supplies.",
                "don't have to",
                c,
                "evaluation",
                "Don't have to bring aclara que los materiales propios no son necesarios.",
                requires=[c56, c],
            ),
            write(
                f"{p}.e03",
                "Traduce la guía al inglés respetando cada etiqueta funcional.",
                "Requisito externo: registrarse. No es necesario traer materiales: se prestan. Regla: usar zapatos cerrados. Prohibición: entrar solo al taller. Consejos: llevar agua y no tocar herramientas calientes porque pueden quemar.",
                "Visitors have to sign in, but they don't have to bring supplies. They must wear closed shoes and mustn't enter the workshop alone. They should carry water and shouldn't touch hot tools because they can cause burns.",
                "Visitors must sign in and wear closed shoes; supplies are provided, so they do not have to bring any. They must not enter the workshop alone. They should take water and should avoid hot tools because burns are possible.",
                c,
                "evaluation",
                "La guía integra necesidad, regla, prohibición, consejo y una razón preventiva.",
                requires=all_concepts,
            ),
            listen(
                f"{p}.e04",
                "Escucha y selecciona la recomendación de la guía práctica.",
                "Recommendation: You should keep the emergency contact on your phone.",
                [
                    "Recommendation: You should keep the emergency contact on your phone.",
                    "Rule: You must keep the emergency contact on the notice board.",
                    "Optional step: You don't have to save it if the front desk is open.",
                ],
                0,
                c,
                "evaluation",
                "Should keep identifica una recomendación útil dentro de la guía.",
                requires=[c58, c],
            ),
        ],
        "review": [
            match(
                f"{p}.r01",
                "Relaciona cada elemento de la guía con su función.",
                [
                    ("checklist", "pasos que deben revisarse"),
                    ("warning", "peligro o prohibición"),
                    ("provided supplies", "materiales que no necesitas traer"),
                ],
                c,
                "review",
                "La lista organiza pasos, la advertencia previene riesgo y los materiales provistos evitan cargas.",
            ),
            order(
                f"{p}.r02",
                "Ordena la prohibición en la entrada de primeros auxilios.",
                "You mustn't block the entrance to the first aid room.",
                c,
                "review",
                "Mustn't block mantiene libre la entrada a la sala de primeros auxilios.",
            ),
            write(
                f"{p}.r03",
                "Traduce la guía de visita respetando las funciones indicadas.",
                "Requisito externo: registrarse. No es necesario traer materiales: se entregan. Regla: usar casco. Prohibición: usar la puerta roja. Consejos: llegar temprano y no correr porque el piso está mojado.",
                "Visitors have to sign in, but they don't have to bring supplies. They must wear a helmet and mustn't use the red door. They should arrive early and shouldn't run because the floor is wet.",
                "Visitors have to register and must wear helmets; supplies are provided, so they do not have to bring any. They must not use the red door. They should come early and should avoid running because the floor is wet.",
                c,
                "review",
                "La recuperación integra necesidad, regla, prohibición y consejos con una razón.",
            ),
        ],
    }
    remediation = {
        f"{p}.e01": (f"en.n2.class-{n}.t03", f"{p}.r02"),
        f"{p}.e02": (f"en.n2.class-{n}.t02", f"{p}.r01"),
        f"{p}.e03": (f"en.n2.class-{n}.t05", f"{p}.r03"),
        f"{p}.e04": (f"en.n2.class-{n}.t04", f"{p}.r01"),
    }
    return common_class(
        n,
        [
            "Organizar una guía práctica en pasos obligatorios, advertencias y recomendaciones.",
            "Elegir have to, must o should según la fuerza comunicativa necesaria.",
            "Redactar una guía autocontenida que explique reglas y consejos con razones.",
        ],
        [
            ("guide", "guía"),
            ("checklist", "lista de verificación"),
            ("warning", "advertencia"),
            ("recommendation", "recomendación"),
            ("first aid", "primeros auxilios"),
            ("contact", "contacto"),
            ("supplies", "materiales"),
            ("practical", "práctico"),
        ],
        [
            (
                "A practical guide separates rules, warnings, and recommendations.",
                "Una guía práctica separa reglas, advertencias y recomendaciones.",
                "Separar funciones ayuda a entender qué es obligatorio, qué está prohibido y qué se aconseja.",
            ),
            (
                "You have to complete the checklist, but you don't have to bring supplies.",
                "Tienes que completar la lista, pero no necesitas traer materiales.",
                "Have to marca el paso necesario y don't have to elimina una necesidad.",
            ),
            (
                "A warning says you must keep the first aid room entrance clear and mustn't block it.",
                "Una advertencia dice que debes mantener libre la entrada de primeros auxilios y no bloquearla.",
                "Must y mustn't presentan una regla de seguridad y su prohibición asociada.",
            ),
            (
                "You should save the emergency contact because help may be needed.",
                "Deberías guardar el contacto de emergencia porque puede necesitarse ayuda.",
                "Should añade una recomendación práctica y because explica su utilidad.",
            ),
            (
                "Workshop guide: Visitors have to sign in; they don't have to bring supplies; they must wear closed shoes and mustn't enter alone; they should carry water and shouldn't touch hot tools because burns are possible.",
                "Guía del taller: los visitantes tienen que registrarse; no necesitan traer materiales; deben usar zapatos cerrados y no deben entrar solos; deberían llevar agua y no deberían tocar herramientas calientes porque pueden quemarse.",
                "La guía integra requisito externo y ausencia de necesidad, regla y prohibición, además de consejo, prevención y una razón con because.",
            ),
        ],
        pools,
        remediation,
        cumulative=all_concepts,
        uses_patterns=all_concepts,
    )


BUILDERS = {56: build_56, 57: build_57, 58: build_58, 59: build_59, 60: build_60}


def semantic_normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.casefold()).strip()


def observable_blob(cls: dict[str, Any]) -> str:
    payload = {"teaching": cls["teaching"], "pools": cls["pools"]}
    return canonical(payload).casefold()


def audit(classes: list[dict[str, Any]], *, require_full_block: bool) -> dict[str, Any]:
    banned = re.compile(r"\b(?:idea trabajada|modelo de la clase|contexto nuevo|frase indicada)\b", re.I)
    all_signatures: dict[str, str] = {}
    all_prompts: set[str] = set()
    block_indices: Counter[int] = Counter()
    totals: Counter[str] = Counter()

    for cls in classes:
        number = int(cls["id"].rsplit("-", 1)[1])
        concept = CONCEPTS[number]
        assert cls["phase"] == PHASES[number]
        assert cls["status"] == "shadow" and cls["runtimeAi"] is False
        assert cls["qualityPolicy"] == QUALITY_POLICY
        assert 4 <= len(cls["teaching"]) <= 6
        assert 6 <= len(cls["vocabulary"]) <= 12
        assert cls["prerequisites"] == [f"en.n2.class-{number - 1}"]

        items = [(pool, item) for pool, pool_items in cls["pools"].items() for item in pool_items]
        assert {pool: len(pool_items) for pool, pool_items in cls["pools"].items()} == {
            "practiceGuided": 3,
            "practice": 3,
            "evaluation": 4,
            "review": 3,
        }
        assert len(items) == 13
        assert len({item["format"] for _, item in items}) >= 4
        assert any(item["format"] == "escuchar" for _, item in items)
        assert any(item["format"] == "escribir" for _, item in items)

        class_feedback: list[str] = []
        class_indices: Counter[int] = Counter()
        for pool, item in items:
            totals[pool] += 1
            prompt = item["prompt"]["es"]
            assert 1 <= len(prompt) <= 90, (item["id"], len(prompt), prompt)
            assert not banned.search(prompt), (item["id"], prompt)
            assert prompt not in all_prompts, item["id"]
            all_prompts.add(prompt)

            feedback = item["origin"]["feedback"]["es"].casefold()
            class_feedback.append(feedback)
            if pool == "practiceGuided":
                assert "hint" in item["origin"] and item["teaches"] == [concept]
                assert item["requires"] == []
            else:
                assert "hint" not in item["origin"]
                assert item["teaches"] == [] and item["requires"]

            if item["format"] in {"elegir", "escuchar"}:
                assert len(item["choices"]) >= 3
                index = item["answer"]["index"]
                assert 0 <= index < len(item["choices"])
                class_indices[index] += 1
                block_indices[index] += 1
            if item["format"] == "completar":
                assert "___" in item["prompt"]["es"], item["id"]
                assert item["answer"]["accepted"] == [item["answer"]["text"]], item["id"]
            if item["format"] == "escribir":
                accepted = item["answer"].get("accepted", [])
                assert len(accepted) >= 2
                assert len({semantic_normalize(value) for value in accepted}) >= 2, item["id"]

            signature = canonical(
                {
                    "prompt": item["prompt"],
                    "answer": item["answer"],
                    "stimulus": item["origin"].get("audio")
                    or item["origin"].get("text")
                    or item["origin"].get("pairs"),
                }
            ).casefold()
            assert signature not in all_signatures, (item["id"], all_signatures.get(signature))
            all_signatures[signature] = item["id"]

        assert len(class_feedback) == len(set(class_feedback)), cls["id"]
        assert len(class_indices) >= 2 and max(class_indices.values()) / sum(class_indices.values()) <= 0.60

        blob = observable_blob(cls)
        for entry in cls["vocabulary"]:
            assert entry["en"].casefold() in blob, (cls["id"], entry["en"])

        eval_ids = {item["id"] for item in cls["pools"]["evaluation"]}
        assert set(cls["remediationMap"]) == eval_ids
        teaching_ids = {item["id"] for item in cls["teaching"]}
        review_ids = {item["id"] for item in cls["pools"]["review"]}
        for mapping in cls["remediationMap"].values():
            assert mapping["reteach"] in teaching_ids
            assert mapping["review"] in review_ids

        if cls["phase"] in {"production", "transfer"}:
            reserved = [
                item
                for pool in ("evaluation", "review")
                for item in cls["pools"][pool]
                if item["format"] == "escribir"
            ]
            assert reserved
            assert any(len(re.findall(r"\b[\w’-]+\b", item["answer"]["text"])) >= 8 for item in reserved)

    if require_full_block:
        assert block_indices == EXPECTED_BLOCK_INDICES, block_indices
        close = classes[-1]
        expected = [CONCEPTS[number] for number in range(56, 61)]
        assert close["cumulativeEvaluation"] == expected
        assert close["usesPatterns"] == expected
        cumulative_write = next(
            item for item in close["pools"]["evaluation"] if item["id"] == "en.n2.c60.e03"
        )
        assert cumulative_write["requires"] == expected
        answer = cumulative_write["answer"]["text"].casefold()
        for marker in ("have to", "don't have to", "must wear", "mustn't", "should carry", "shouldn't", "because"):
            assert marker in answer, marker

    return {
        "classes": len(classes),
        "items": sum(totals.values()),
        "pools": dict(totals),
        "correctIndices": dict(sorted(block_indices.items())),
        "fingerprints": len(all_signatures),
        "prompts": len(all_prompts),
    }


def write_class(number: int) -> Path:
    document = BUILDERS[number]()
    audit([document], require_full_block=False)
    path = OUT / f"class-{number}.json"
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_bundle() -> Path:
    classes = [json.loads((OUT / f"class-{number}.json").read_text(encoding="utf-8")) for number in range(56, 61)]
    audit(classes, require_full_block=True)
    bundle = {
        "schema": "onelingo.editorial.class-bundle.v1",
        "course": "en",
        "level": 2,
        "scale": SCALE,
        "status": "shadow",
        "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "range": {"start": 56, "end": 60},
        "classes": classes,
    }
    path = OUT / "bundle-56-60.json"
    path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-number", type=int, choices=range(56, 61))
    parser.add_argument("--bundle", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()

    if args.class_number is not None:
        print(write_class(args.class_number))
    elif args.bundle:
        print(write_bundle())
    elif args.audit:
        classes = [
            json.loads((OUT / f"class-{number}.json").read_text(encoding="utf-8"))
            for number in range(56, 61)
        ]
        print(json.dumps(audit(classes, require_full_block=True), ensure_ascii=False, sort_keys=True))
    else:
        parser.error("choose --class-number, --bundle, or --audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
