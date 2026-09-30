#!/usr/bin/env python3
"""Generate the isolated English N2 C76-C80 editorial draft."""

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
    76: "n2-symptoms-body-states",
    77: "n2-advice-common-problems",
    78: "n2-appointments-instructions",
    79: "n2-describe-health-event",
    80: "n2-health-conversation",
}
PHASES = {76: "input", 77: "form", 78: "comprehension", 79: "production", 80: "transfer"}
TITLES = {
    76: ("Symptoms and body states", "Síntomas y estados físicos"),
    77: ("Advice for common problems", "Consejos para problemas comunes"),
    78: ("Appointments and instructions", "Citas e instrucciones"),
    79: ("Describe what happened", "Describir lo sucedido"),
    80: ("Health conversation", "Conversación sobre salud"),
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
EXPECTED_INDICES = Counter({0: 7, 1: 6, 2: 7})


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def hashed(item: dict[str, Any]) -> dict[str, Any]:
    item["contentHash"] = digest({k: v for k, v in item.items() if k not in {"id", "contentHash"}})
    return item


def base(item_id: str, fmt: str, prompt: str, concept: str, pool: str, feedback: str,
         requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": hint or "Identifica la función comunicativa antes de responder."}
    return {
        "id": item_id, "format": fmt, "prompt": {"es": prompt}, "answer": {}, "choices": [],
        "teaches": [concept] if pool == "practiceGuided" else [],
        "requires": [] if pool == "practiceGuided" else list(requires or [concept]),
        "origin": origin,
        "accessibility": {"screenReader": True, "highContrast": True, "largeText": True},
    }


def q(i: str, prompt: str, options: list[str], index: int, c: str, pool: str, feedback: str,
      *, requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    x = base(i, "elegir", prompt, c, pool, feedback, requires, hint)
    x["choices"] = [{"text": value} for value in options]
    x["answer"] = {"index": index}
    return hashed(x)


def l(i: str, prompt: str, audio: str, options: list[str], index: int, c: str, pool: str,
      feedback: str, *, requires: list[str] | None = None) -> dict[str, Any]:
    x = base(i, "escuchar", prompt, c, pool, feedback, requires)
    x["choices"] = [{"text": value} for value in options]
    x["answer"] = {"index": index}
    x["origin"].update({"audio": audio, "audioMode": "tts", "languageCode": "en",
                        "speedOptions": [0.75, 1.0], "maxReplays": 3,
                        "revealTranscriptAfterAttempt": True})
    return hashed(x)


def f(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str,
      *, requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    x = base(i, "completar", prompt, c, pool, feedback, requires, hint)
    x["answer"] = {"text": answer, "accepted": [answer]}
    return hashed(x)


def o(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str,
      *, requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    x = base(i, "ordenar", prompt, c, pool, feedback, requires, hint)
    x["answer"] = {"text": answer, "tokens": answer.split()}
    return hashed(x)


def w(i: str, prompt: str, stimulus: str, answer: str, alternative: str, c: str, pool: str,
      feedback: str, *, requires: list[str] | None = None) -> dict[str, Any]:
    x = base(i, "escribir", prompt, c, pool, feedback, requires)
    x["origin"]["text"] = stimulus
    x["answer"] = {"text": answer, "accepted": [answer, alternative]}
    return hashed(x)


def m(i: str, prompt: str, pairs: list[tuple[str, str]], c: str, pool: str, feedback: str,
      *, requires: list[str] | None = None) -> dict[str, Any]:
    x = base(i, "relacionar", prompt, c, pool, feedback, requires)
    values = [[left, {"es": right}] for left, right in pairs]
    x["answer"] = {"pairs": values}
    x["origin"]["pairs"] = values
    return hashed(x)


def teachings(number: int, rows: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    result = []
    for index, (en, es, explanation) in enumerate(rows, 1):
        en_words, es_words = en.split(), es.split()
        em, sm = max(1, len(en_words) // 2), max(1, len(es_words) // 2)
        result.append({
            "id": f"en.n2.class-{number}.t{index:02d}", "en": en, "es": es,
            "explanationEs": explanation,
            "segments": [{"en": " ".join(en_words[:em]), "es": " ".join(es_words[:sm])},
                         {"en": " ".join(en_words[em:]), "es": " ".join(es_words[sm:])}],
            "audioText": en, "audioMode": "tts", "languageCode": "en",
            "patternId": CONCEPTS[number],
        })
    return result


def make_class(number: int, objectives: list[str], vocab: list[tuple[str, str]],
               lesson_rows: list[tuple[str, str, str]], pools: dict[str, list[dict[str, Any]]],
               remap: dict[str, tuple[str, str]], *, uses: list[str] | None = None,
               cumulative: list[str] | None = None) -> dict[str, Any]:
    doc: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 2, "cefr": "A2",
        "scale": SCALE, "status": "shadow", "runtimeAi": False, "phase": PHASES[number],
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY_POLICY), "id": f"en.n2.class-{number}",
        "title": {"en": TITLES[number][0], "es": TITLES[number][1]},
        "objectives": {"es": objectives}, "concepts": [CONCEPTS[number]],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n2.class-{number - 1}"],
        "usesVocabulary": [en for en, _ in vocab], "usesPatterns": uses or [CONCEPTS[number]],
        "vocabulary": [{"en": en, "es": es} for en, es in vocab],
        "teaching": teachings(number, lesson_rows), "pools": pools,
        "remediationMap": {key: {"reteach": a, "review": b} for key, (a, b) in remap.items()},
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True,
                          "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2, "allowAudioReplay": True,
                     "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if cumulative is not None:
        doc["cumulativeEvaluation"] = cumulative
    return doc


def build_76() -> dict[str, Any]:
    n, c, p = 76, CONCEPTS[76], "en.n2.c76"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Luis tiene dolor de cabeza y cansancio. Elige su descripción.",
              ["He has a headache and feels tired.", "He has a cough and feels dizzy.",
               "He has a sore throat and a fever."], 0, c, "practiceGuided",
              "Headache nombra el dolor de cabeza y tired describe su falta de energía.",
              hint="Relaciona cada síntoma con la información dada sobre Luis."),
            f(f"{p}.pg02", "Completa el estado físico: She has a cough and a sore ___.", "throat", c,
              "practiceGuided", "Sore throat es la expresión fija para dolor de garganta.",
              hint="Después de sore se necesita la parte del cuerpo afectada."),
            o(f"{p}.pg03", "Ordena la reacción segura de alguien que siente mareo.",
              "I feel dizzy, so I am sitting down.", c, "practiceGuided",
              "Feel dizzy expresa mareo y sitting down comunica una respuesta prudente.",
              hint="Presenta primero el estado y después la acción con so."),
        ],
        "practice": [
            w(f"{p}.p01", "Escribe en inglés los dos síntomas de Nina.",
              "Nina tiene tos y dolor de garganta.", "Nina has a cough and a sore throat.",
              "Nina has a sore throat and a cough.", c, "practice",
              "Has a cough y has a sore throat comunican los dos síntomas sin diagnosticar."),
            l(f"{p}.p02", "Escucha y elige el estado físico que menciona el hablante.",
              "I feel dizzy, but I do not have a headache.",
              ["The speaker feels tired and has pain.", "The speaker has a headache.",
               "The speaker feels dizzy."], 2, c, "practice",
              "La persona afirma feel dizzy y niega explícitamente el dolor de cabeza."),
            m(f"{p}.p03", "Relaciona cada palabra con el estado que describe.",
              [("dizzy", "mareado"), ("tired", "sin energía")], c,
              "practice", "Dizzy expresa mareo y tired describe falta de energía."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Marta no tiene energía. Selecciona la descripción precisa.",
              ["Marta feels dizzy.", "Marta feels tired.", "Marta has a cough."], 1, c,
              "evaluation", "Feels tired describe falta de energía sin añadir otro síntoma."),
            f(f"{p}.e02", "Usa pain para completar el síntoma: I have ___ in my back.", "pain", c,
              "evaluation", "Pain completa la descripción localizada en la espalda."),
            w(f"{p}.e03", "Describe en inglés el estado de Omar con los datos dados.",
              "Omar: mareado y cansado; se sienta.",
              "Omar feels dizzy and tired, so he is sitting down.",
              "Omar is tired and feels dizzy, so he sits down.", c, "evaluation",
              "La respuesta reúne dizzy, tired y la acción de sentarse sin inferir una causa."),
            l(f"{p}.e04", "Escucha y selecciona únicamente los dos datos mencionados.",
              "I have a fever and pain in my back.",
              ["A cough and a sore throat", "Tiredness and a headache", "A fever and back pain"],
              2, c, "evaluation",
              "El audio nombra fever y back pain; no incluye tos ni dolor de cabeza."),
        ],
        "review": [
            m(f"{p}.r01", "Relaciona los términos con una descripción corporal exacta.",
              [("fever", "estado con temperatura corporal alta"),
               ("pain", "molestia localizada en el cuerpo")], c, "review",
              "La relación recupera temperatura y ubicación del dolor como datos observables."),
            o(f"{p}.r02", "Ordena la descripción de dos síntomas de Elena.",
              "Elena has a cough and a sore throat.", c, "review",
              "La oración recupera cough y sore throat como síntomas distintos."),
            w(f"{p}.r03", "Redacta en inglés el estado de Leo y su reacción.",
              "Leo: dolor de cabeza, cansancio y se sienta.",
              "Leo has a headache and feels tired, so he sits down.",
              "Leo feels tired and has a headache, so he is sitting down.", c, "review",
              "La recuperación integra headache, tired y una acción segura en una sola descripción."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n2.class-{n}.t01", f"{p}.r03"),
             f"{p}.e02": (f"en.n2.class-{n}.t04", f"{p}.r01"),
             f"{p}.e03": (f"en.n2.class-{n}.t03", f"{p}.r03"),
             f"{p}.e04": (f"en.n2.class-{n}.t04", f"{p}.r01")}
    return make_class(n,
        ["Nombrar síntomas cotidianos y estados físicos con have y feel.",
         "Separar una descripción corporal de una explicación o diagnóstico.",
         "Comunicar por escrito dos síntomas y una reacción segura."],
        [("headache", "dolor de cabeza"), ("cough", "tos"), ("sore throat", "dolor de garganta"),
         ("dizzy", "mareado"), ("tired", "cansado"), ("fever", "fiebre"),
         ("pain", "dolor"), ("feel", "sentirse")],
        [("I have a headache and I feel tired.", "Tengo dolor de cabeza y me siento cansado.",
          "Have presenta un síntoma; feel introduce un estado físico."),
         ("She has a cough and a sore throat.", "Ella tiene tos y dolor de garganta.",
          "Cough y sore throat son descripciones de síntomas cotidianos."),
         ("He feels dizzy, so he sits down.", "Él se siente mareado, así que se sienta.",
          "Feel dizzy nombra el mareo y so conecta una reacción segura."),
         ("I have a fever and pain in my back.", "Tengo fiebre y dolor en la espalda.",
          "Fever y pain informan estados físicos; no explican su causa."),
         ("Describe how you feel; do not guess a diagnosis.",
          "Describe cómo te sientes; no adivines un diagnóstico.",
          "Una conversación A2 comunica hechos y deja el diagnóstico a profesionales.")], pools, remap)


def build_77() -> dict[str, Any]:
    n, c, p, prior = 77, CONCEPTS[77], "en.n2.c77", CONCEPTS[76]
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Ana está cansada. Elige el consejo general adecuado.",
              ["You should continue working without a break.", "You should rest and drink water.",
               "You shouldn't drink any water today."], 1, c, "practiceGuided",
              "Should rest and drink water ofrece autocuidado general sin prometer un resultado.",
              hint="Elige una recomendación sencilla, no un diagnóstico."),
            f(f"{p}.pg02", "Usa la contracción shouldn't: You ___ stay on your feet if dizzy.",
              "shouldn't", c, "practiceGuided",
              "Shouldn't stay on your feet desaconseja una acción cuando hay mareo.",
              hint="La situación pide evitar la acción, así que usa la forma negativa."),
            o(f"{p}.pg03", "Ordena el consejo sobre pedir orientación profesional.",
              "You should contact a health professional if it does not improve.", c,
              "practiceGuided",
              "Should contact presenta un paso prudente si el problema no mejora.",
              hint="Empieza con el sujeto y une la condición final con if."),
        ],
        "practice": [
            w(f"{p}.p01", "Escribe el consejo para Nina con acción y duración.",
              "Nina: beber agua y descansar treinta minutos.",
              "Nina should drink water and rest for thirty minutes.",
              "Nina should rest for thirty minutes and drink water.", c, "practice",
              "Las variantes conservan a Nina, el agua y los treinta minutos de descanso."),
            l(f"{p}.p02", "Escucha y selecciona la acción que se desaconseja.",
              "You feel dizzy, so you shouldn't drive.",
              ["Resting", "Drinking water", "Driving"], 2, c, "practice",
              "Shouldn't drive identifica con precisión la acción que debe evitarse."),
            m(f"{p}.p03", "Relaciona cada expresión con su función comunicativa.",
              [("should", "consejo general"), ("shouldn't", "acción desaconsejada")], c,
              "practice", "Should recomienda y shouldn't indica qué conviene evitar."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Pablo tiene dolor de cabeza. Elige el consejo seguro y general.",
              ["You should rest in a quiet place.", "You should keep working without a break.",
               "You shouldn't rest until the evening."], 0, c, "evaluation",
              "Rest in a quiet place es la recomendación prudente para el problema descrito.",
              ),
            f(f"{p}.e02", "Usa la contracción shouldn't: You ___ ignore dizziness while standing.",
              "shouldn't", c, "evaluation",
              "Shouldn't ignore desaconseja continuar sin atender el mareo."),
            w(f"{p}.e03", "Redacta el paso indicado si el problema no mejora.",
              "Situación: el malestar continúa; acción: contactar a un profesional de salud.",
              "You should contact a health professional if the problem does not improve.",
              "If the problem does not improve, you should contact a health professional.", c,
              "evaluation", "La condición y la acción profesional se mantienen en ambas variantes.",
              ),
            l(f"{p}.e04", "Escucha y elige qué afirma realmente el mensaje.",
              "This advice may help you feel better, but it is not a diagnosis.",
              ["The advice guarantees recovery.", "The advice replaces professional care.",
               "The advice may help but is not a diagnosis."], 2, c, "evaluation",
              "El mensaje limita el consejo: puede ayudar, pero no constituye un diagnóstico."),
        ],
        "review": [
            m(f"{p}.r01", "Relaciona cada situación con el tipo de consejo.",
              [("feels dizzy", "should sit down"), ("is already sitting", "shouldn't stand quickly")],
              c, "review", "Cada relación conecta el estado físico con una respuesta prudente.",
              ),
            o(f"{p}.r02", "Ordena el paso condicionado por la falta de mejoría.",
              "Contact a health professional if the problem does not improve.", c, "review",
              "La secuencia conserva la condición que justifica buscar orientación profesional."),
            w(f"{p}.r03", "Escribe un consejo y aclara su alcance.",
              "Consejo: descansar; aclaración: consejo general, no diagnóstico.",
              "You should rest; this is general advice, not a diagnosis.",
              "This is general advice, not a diagnosis: you should rest.", c, "review",
              "La recuperación combina should con un límite explícito sobre el alcance del consejo."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n2.class-{n}.t01", f"{p}.r03"),
             f"{p}.e02": (f"en.n2.class-{n}.t02", f"{p}.r01"),
             f"{p}.e03": (f"en.n2.class-{n}.t04", f"{p}.r02"),
             f"{p}.e04": (f"en.n2.class-{n}.t03", f"{p}.r03")}
    return make_class(n,
        ["Dar consejos generales con should y shouldn't ante problemas cotidianos.",
         "Indicar cuándo contactar a un profesional si un problema no mejora.",
         "Aclarar que un consejo de autocuidado no es un diagnóstico."],
        [("rest", "descansar"), ("water", "agua"), ("should", "debería"),
         ("shouldn't", "no debería"), ("better", "mejor"), ("improve", "mejorar"),
         ("professional", "profesional"), ("advice", "consejo")],
        [("You should rest and drink water.", "Deberías descansar y beber agua.",
          "Should introduce una recomendación general y prudente."),
         ("You shouldn't stay on your feet if you feel dizzy.",
          "No deberías seguir de pie si te sientes mareado.",
          "Shouldn't marca una acción desaconsejada ante un estado concreto."),
         ("This advice may help you feel better; it is not a diagnosis.",
          "Este consejo puede ayudarte a sentirte mejor; no es un diagnóstico.",
          "Advice no promete mejorar ni sustituye una evaluación profesional."),
         ("If the problem does not improve, contact a health professional.",
          "Si el problema no mejora, contacta a un profesional de salud.",
          "If establece la condición para buscar orientación profesional."),
         ("Should gives advice; it does not guarantee an outcome.",
          "Should da consejo; no garantiza un resultado.",
          "La forma comunica recomendación, no certeza médica.")], pools, remap,
        uses=[prior, c])


def build_78() -> dict[str, Any]:
    n, c, p, advice = 78, CONCEPTS[78], "en.n2.c78", CONCEPTS[77]
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige una petición cortés para reservar una cita.",
              ["I would like to cancel my appointment.", "I would like to confirm my appointment.",
               "I would like to make an appointment."], 2, c, "practiceGuided",
              "Would like to make an appointment formula la petición de reserva con cortesía.",
              hint="Busca una petición completa con would like y make an appointment."),
            f(f"{p}.pg02", "Completa el rol: The ___ confirms the check-up for Tuesday.",
              "receptionist", c, "practiceGuided",
              "Receptionist identifica a la persona que confirma la cita en recepción.",
              hint="Escribe el nombre del rol que organiza las citas."),
            o(f"{p}.pg03", "Ordena las dos instrucciones previas a la cita.",
              "Please arrive ten minutes early and bring the completed form.", c,
              "practiceGuided",
              "Arrive early y bring the form son dos acciones distintas antes de la cita.",
              hint="Empieza con Please y une ambas acciones con and."),
        ],
        "practice": [
            w(f"{p}.p01", "Escribe una petición de cita con lugar y día.",
              "Cita en la clínica para el lunes.",
              "I would like to make an appointment at the clinic for Monday.",
              "For Monday, I would like to make an appointment at the clinic.", c, "practice",
              "Las variantes conservan la petición, el lugar y el día de la cita."),
            l(f"{p}.p02", "Escucha y selecciona la hora confirmada para el chequeo.",
              "The receptionist confirms your check-up for Tuesday at ten thirty.",
              ["Tuesday at ten thirty", "Tuesday at ten", "Thursday at ten thirty"], 0, c,
              "practice", "El audio confirma Tuesday at ten thirty sin cambiar día ni hora."),
            m(f"{p}.p03", "Relaciona cada término de la cita con su significado.",
              [("form", "formulario"), ("instructions", "indicaciones")], c, "practice",
              "Form nombra el documento e instructions nombra los pasos que deben seguirse."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Sofía necesita una cita nueva para el lunes. Elige su petición.",
              ["Could you confirm my Monday appointment?",
               "I need to cancel my clinic appointment for Monday.",
               "Could I book a clinic appointment for Monday?"], 2, c, "evaluation",
              "Could I book pide una cita nueva y conserva el lugar y el lunes."),
            f(f"{p}.e02", "Usa el verbo confirm: Could you ___ the appointment time, please?", "confirm", c,
              "evaluation", "Confirm verifica la hora exacta dentro de una petición cortés."),
            w(f"{p}.e03", "Redacta las instrucciones de llegada y documento.",
              "Llegar quince minutos antes y traer el formulario completo.",
              "Please arrive fifteen minutes early and bring the completed form.",
              "Bring the completed form and please arrive fifteen minutes early.", c, "evaluation",
              "Las dos instrucciones mantienen el margen de quince minutos y el formulario completo."),
            l(f"{p}.e04", "Escucha y elige la respuesta que aclara una indicación.",
              "Please arrive early. If anything is unclear, ask the receptionist.",
              ["Bring the completed form without asking.",
               "Ask the receptionist if something is unclear.",
               "Confirm the appointment time again."], 1, c, "evaluation",
              "El mensaje indica consultar a recepción cuando una instrucción no esté clara."),
        ],
        "review": [
            m(f"{p}.r01", "Relaciona cada gestión con la persona o dato correspondiente.",
              [("make an appointment", "clinic"), ("confirm the time", "receptionist")], c,
              "review", "La reserva se hace en la clínica y la hora se confirma con recepción."),
            o(f"{p}.r02", "Ordena la instrucción de preparación para el chequeo.",
              "Arrive early and bring your completed form for the check-up.", c, "review",
              "La recuperación reúne llegada anticipada, documento y propósito de la visita."),
            w(f"{p}.r03", "Escribe una pregunta cortés para aclarar la instrucción.",
              "No sabes si debes traer el formulario.",
              "Could you tell me if I need to bring the form, please?",
              "I am not sure about the form; could you explain if I need to bring it?", c, "review",
              "Ambas variantes piden aclarar si el formulario forma parte de la instrucción."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n2.class-{n}.t01", f"{p}.r01"),
             f"{p}.e02": (f"en.n2.class-{n}.t05", f"{p}.r01"),
             f"{p}.e03": (f"en.n2.class-{n}.t03", f"{p}.r02"),
             f"{p}.e04": (f"en.n2.class-{n}.t04", f"{p}.r03")}
    return make_class(n,
        ["Pedir y confirmar una cita con día y hora concretos.",
         "Comprender instrucciones logísticas antes de un chequeo.",
         "Solicitar aclaración cuando una indicación no esté clara."],
        [("appointment", "cita"), ("clinic", "clínica"), ("arrive", "llegar"),
         ("form", "formulario"), ("instructions", "indicaciones"),
         ("receptionist", "recepcionista"), ("check-up", "chequeo"),
         ("confirm", "confirmar")],
        [("I would like to make an appointment at the clinic.",
          "Me gustaría hacer una cita en la clínica.",
          "Would like convierte la reserva de appointment en una petición cortés."),
         ("The receptionist confirms the check-up for Tuesday at ten.",
          "La recepcionista confirma el chequeo para el martes a las diez.",
          "Confirm debe conservar tanto el día como la hora acordados."),
         ("Please arrive ten minutes early and bring the completed form.",
          "Llega diez minutos antes y trae el formulario completo, por favor.",
          "La instrucción contiene dos acciones logísticas independientes."),
         ("Follow the clinic instructions and ask if anything is unclear.",
          "Sigue las indicaciones de la clínica y pregunta si algo no está claro.",
          "Pedir aclaración evita adivinar una instrucción desconocida."),
         ("Could you confirm the appointment time, please?",
          "¿Podría confirmar la hora de la cita, por favor?",
          "Could you y please forman una solicitud cortés de confirmación.")], pools, remap,
        uses=[advice, c])


def build_79() -> dict[str, Any]:
    n, c, p, symptoms = 79, CONCEPTS[79], "en.n2.c79", CONCEPTS[76]
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige el relato que sitúa un hecho durante una espera.",
              ["Yesterday, I suddenly felt dizzy while I was waiting.",
               "Tomorrow, I may wait if I feel better.",
               "I always wait because dizziness has one cause."], 0, c, "practiceGuided",
              "Yesterday, suddenly y while sitúan el estado dentro de una secuencia pasada.",
              hint="Busca un momento pasado, un cambio repentino y una acción en curso."),
            f(f"{p}.pg02", "Completa el hecho pasado: I ___ near the door and hurt my knee.", "fell", c,
              "practiceGuided", "Fell es el pasado de fall y precede al resultado hurt my knee.",
              hint="La narración necesita el pasado irregular de fall."),
            o(f"{p}.pg03", "Ordena las acciones posteriores a la caída.",
              "Then I sat down and called the clinic.", c, "practiceGuided",
              "Then introduce los siguientes pasos sin inventar la causa del evento.",
              hint="Empieza con el conector y conserva ambas acciones pasadas."),
        ],
        "practice": [
            w(f"{p}.p01", "Escribe en orden los dos hechos ocurridos junto a la puerta.",
              "Primero: se cayó. Después: se lastimó la rodilla.",
              "I fell near the door, and then I hurt my knee.",
              "Near the door, I fell and then hurt my knee.", c, "practice",
              "Las variantes mantienen lugar, caída y lesión en el mismo orden factual."),
            l(f"{p}.p02", "Escucha y selecciona qué ocurrió después de la llamada.",
              "After the call, I made an appointment for Friday.",
              ["The speaker cancelled Friday.", "The speaker made an appointment for Friday.",
               "The speaker called after the appointment."], 1, c, "practice",
              "After the call ubica la cita como la acción posterior y conserva Friday."),
            m(f"{p}.p03", "Relaciona cada conector con su función en el relato.",
              [("while", "acción en curso"), ("then", "acción siguiente")], c, "practice",
              "While enmarca una acción en curso y then hace avanzar la secuencia."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Selecciona el inicio que responde cuándo y cómo comenzó el evento.",
              ["Yesterday, I suddenly felt dizzy.",
               "Yesterday, I felt tired after the appointment.",
               "I felt dizzy, so I sat down later."], 0, c, "evaluation",
              "Yesterday responde cuándo y suddenly indica cómo comenzó, sin dar un diagnóstico."),
            f(f"{p}.e02", "Usa el pasado de hurt: I fell and ___ my arm.", "hurt", c, "evaluation",
              "Hurt conserva la descripción de lo sucedido sin atribuir una causa médica."),
            w(f"{p}.e03", "Redacta el relato con los cuatro pasos indicados.",
              "Ayer: mareo mientras caminaba; caída; se sentó; después llamó a la clínica.",
              "Yesterday, while I was walking, I felt dizzy and fell. Then I sat down and called the clinic.",
              "While I was walking yesterday, I felt dizzy and fell; then I sat down and called the clinic.",
              c, "evaluation",
              "La respuesta conserva tiempo, acción en curso, caída y dos acciones posteriores."),
            l(f"{p}.e04", "Escucha y elige el resumen que informa hechos sin adivinar causas.",
              "This morning I felt tired, sat down, and made an appointment. I do not know the cause.",
              ["The speaker names a definite illness.", "The speaker reports events and does not know the cause.",
               "The speaker gives treatment instructions."], 1, c, "evaluation",
              "El resumen conserva los hechos y reconoce que la causa no se conoce."),
        ],
        "review": [
            m(f"{p}.r01", "Relaciona cada expresión con evidencia o conjetura.",
              [("I felt dizzy yesterday", "hecho informado"),
               ("It was definitely an illness", "conjetura no confirmada")], c, "review",
              "La recuperación separa una experiencia observable de una conclusión no confirmada.",
              ),
            o(f"{p}.r02", "Ordena la secuencia de caída, dolor y descanso.",
              "I fell, hurt my ankle, and then sat down.", c, "review",
              "La secuencia mantiene tres hechos concretos en su orden temporal."),
            w(f"{p}.r03", "Escribe otro relato factual con cierre de cita.",
              "Esta mañana: tos durante el trabajo; descansó; después pidió cita.",
              "This morning, I coughed while I was working, rested, and then made an appointment.",
              "While I was working this morning, I coughed; then I rested and made an appointment.",
              c, "review", "Ambas variantes ordenan el síntoma, el descanso y la cita sin explicar la causa."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n2.class-{n}.t01", f"{p}.r03"),
             f"{p}.e02": (f"en.n2.class-{n}.t02", f"{p}.r02"),
             f"{p}.e03": (f"en.n2.class-{n}.t03", f"{p}.r03"),
             f"{p}.e04": (f"en.n2.class-{n}.t05", f"{p}.r01")}
    return make_class(n,
        ["Narrar un episodio físico con marcadores de tiempo y orden.",
         "Describir caída, dolor y acciones posteriores sin adivinar causas.",
         "Producir un relato de ocho o más palabras con una secuencia completa."],
        [("happened", "sucedió"), ("yesterday", "ayer"), ("suddenly", "de repente"),
         ("while", "mientras"), ("fell", "se cayó"), ("hurt", "se lastimó"),
         ("then", "después"), ("after", "después de")],
        [("Yesterday, I suddenly felt dizzy while I was waiting.",
          "Ayer, de repente me sentí mareado mientras esperaba.",
          "Yesterday ubica el hecho, suddenly marca el cambio y while enmarca la espera."),
         ("I fell near the door and hurt my knee.",
          "Me caí cerca de la puerta y me lastimé la rodilla.",
          "Fell y hurt informan dos hechos pasados en orden."),
         ("Then I sat down and called the clinic.",
          "Después me senté y llamé a la clínica.",
          "Then introduce las acciones realizadas a continuación."),
         ("After the call, I made an appointment.",
          "Después de la llamada, hice una cita.",
          "After relaciona una acción posterior con un evento ya mencionado."),
         ("Describe what happened; do not guess the cause.",
          "Describe lo que sucedió; no adivines la causa.",
          "Un relato útil distingue los hechos de una explicación no confirmada.")], pools, remap,
        uses=[symptoms, c])


def build_80() -> dict[str, Any]:
    n, c, p = 80, CONCEPTS[80], "en.n2.c80"
    all_c = [CONCEPTS[x] for x in range(76, 81)]
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la apertura que comunica dos síntomas con claridad.",
              ["I would like an appointment for my headache.",
               "I have a headache and feel dizzy.",
               "You should rest if you feel dizzy."], 1, c, "practiceGuided",
              "Have a headache y feel dizzy abren la conversación con dos datos corporales.",
              hint="Busca una descripción directa, sin diagnóstico ni consejo todavía."),
            f(f"{p}.pg02", "Completa la respuesta profesional: You ___ sit down and rest.", "should", c,
              "practiceGuided", "Should sit down and rest ofrece consejo general con fuerza adecuada.",
              hint="La respuesta es una recomendación, no una obligación ni un diagnóstico."),
            o(f"{p}.pg03", "Ordena la petición y la confirmación de una cita.",
              "I would like an appointment; could you confirm the time?", c, "practiceGuided",
              "La secuencia primero solicita la cita y después pide confirmar la hora.",
              hint="Coloca la petición antes de la pregunta de confirmación."),
        ],
        "practice": [
            w(f"{p}.p01", "Escribe dos turnos: síntoma y consejo general.",
              "Paciente: tos y dolor de garganta. Profesional: beber agua y descansar.",
              "Patient: I have a cough and a sore throat. Health worker: You should drink water and rest.",
              "Patient: I have a sore throat and a cough. Health worker: You should rest and drink water.",
              c, "practice", "Las variantes mantienen roles, dos síntomas y dos acciones de autocuidado.",
              requires=[CONCEPTS[76], CONCEPTS[77], c]),
            l(f"{p}.p02", "Escucha y selecciona el dato que la recepción confirma.",
              "Receptionist: Your appointment is Friday at two. Please arrive early.",
              ["A Friday appointment at two", "A Thursday visit with no time",
               "A Friday appointment at twelve"], 0, c, "practice",
              "Reception confirma Friday at two; early es una instrucción, no una nueva hora.",
              requires=[CONCEPTS[78], c]),
            m(f"{p}.p03", "Relaciona cada turno con la función que cumple.",
              [("Yesterday I fell near the door", "describe lo sucedido"),
               ("Could you confirm the time?", "verifica la cita")], c, "practice",
              "Un turno relata el evento pasado y el otro solicita confirmación logística.",
              requires=[CONCEPTS[78], CONCEPTS[79], c]),
        ],
        "evaluation": [
            q(f"{p}.e01", "El paciente informa mareo y dolor de espalda. Elige su turno.",
              ["You should arrive early with a form.", "I would like Friday at two.",
               "I feel dizzy and have pain in my back."], 2, c, "evaluation",
              "La opción correcta informa mareo y dolor de espalda sin añadir consejo ni cita.",
              requires=[CONCEPTS[76], c]),
            f(f"{p}.e02", "Usa should para aconsejar: You ___ avoid standing while dizzy.", "should", c,
              "evaluation", "Should comunica consejo general sin convertirlo en diagnóstico o garantía.",
              requires=[CONCEPTS[77], c]),
            l(f"{p}.e03", "Escucha y elige todos los datos de la cita e instrucciones.",
              "Your appointment is Monday at nine. Arrive ten minutes early and bring the form.",
              ["Monday at nine; arrive early; bring the form",
               "Monday at ten; arrive early; bring an ID",
               "Tuesday at nine; arrive on time; bring the form"], 0, c, "evaluation",
              "La opción conserva Monday at nine, diez minutos antes y el formulario.",
              requires=[CONCEPTS[78], c]),
            w(f"{p}.e04", "Redacta el diálogo con los datos indicados y conserva los cinco pasos.",
              "Paciente: ayer se mareó, cayó y se lastimó la rodilla; aún tiene dolor. "
              "Profesional: consejo general de sentarse y descansar; no es diagnóstico. "
              "Paciente: pide cita para jueves 11:00. Recepción: confirma e indica llegar diez "
              "minutos antes con formulario. Paciente: confirma el plan.",
              "Patient: Yesterday I felt dizzy, fell, and hurt my knee. It still hurts. Health worker: You should sit down and rest; this is general advice, not a diagnosis. Patient: I would like an appointment for Thursday at 11:00. Receptionist: Confirmed. Please arrive ten minutes early and bring the form. Patient: Thank you. I confirm the time and instructions.",
              "Patient: I felt dizzy yesterday, fell, and hurt my knee. I still have pain. Health worker: You should rest and sit down; this is general advice, not a diagnosis. Patient: Could I have an appointment on Thursday at 11:00? Receptionist: Yes, it is confirmed. Bring the form and arrive ten minutes early. Patient: Thank you; I confirm the appointment and the instructions.",
              c, "evaluation",
              "El diálogo conserva el evento, estado actual, consejo limitado, cita, instrucciones y cierre.",
              requires=all_c),
        ],
        "review": [
            m(f"{p}.r01", "Relaciona cada turno con síntoma o relato pasado.",
              [("I feel tired now", "estado actual"), ("I fell yesterday", "hecho pasado")], c,
              "review", "La recuperación separa cómo se siente alguien ahora de lo que ocurrió antes.",
              requires=[CONCEPTS[76], CONCEPTS[79], c]),
            o(f"{p}.r02", "Ordena la cita con hora y las dos instrucciones logísticas.",
              "Your appointment is Wednesday at ten; arrive early and bring the form.", c, "review",
              "La recuperación conserva miércoles a las diez, llegada anticipada y formulario.",
              requires=[CONCEPTS[78], c]),
            w(f"{p}.r03", "Redacta la recuperación completa con todos los datos dados.",
              "Paciente: esta mañana tos y dolor de garganta durante el trabajo. Profesional: "
              "agua y descanso como consejo general, no diagnóstico. Recepción: cita viernes 2:00; "
              "llegar quince minutos antes con identificación. Paciente: confirma.",
              "Patient: This morning I had a cough and a sore throat while I was working. Health worker: You should drink water and rest; this is general advice, not a diagnosis. Receptionist: Your appointment is Friday at 2:00. Please arrive fifteen minutes early and bring your ID. Patient: Thank you. I confirm the appointment and instructions.",
              "Patient: While I was working this morning, I had a sore throat and a cough. Health worker: You should rest and drink water; this is general advice, not a diagnosis. Receptionist: I confirm Friday at 2:00. Bring your ID and arrive fifteen minutes early. Patient: Thank you; I confirm the time and instructions.",
              c, "review", "La recuperación integra los cinco conceptos en un contexto nuevo y completo.",
              requires=all_c),
        ],
    }
    remap = {f"{p}.e01": (f"en.n2.class-{n}.t01", f"{p}.r01"),
             f"{p}.e02": (f"en.n2.class-{n}.t02", f"{p}.r03"),
             f"{p}.e03": (f"en.n2.class-{n}.t04", f"{p}.r02"),
             f"{p}.e04": (f"en.n2.class-{n}.t05", f"{p}.r03")}
    return make_class(n,
        ["Sostener una conversación de salud A2 sin ofrecer un diagnóstico.",
         "Integrar síntomas, consejo general, cita, relato pasado e instrucciones.",
         "Confirmar por escrito un plan completo con roles y datos concretos."],
        [("symptom", "síntoma"), ("advice", "consejo"), ("appointment", "cita"),
         ("describe", "describir"), ("confirm", "confirmar"),
         ("conversation", "conversación"), ("health", "salud"),
         ("follow-up", "seguimiento")],
        [("Patient: I have a headache and feel dizzy. Receptionist: Thank you. Please describe each symptom.",
          "Paciente: Tengo dolor de cabeza y mareo. Recepción: Gracias. Describe cada síntoma.",
          "Una conversación de health comienza con un symptom descrito de forma concreta."),
         ("Health worker: You should sit down and rest. This is general advice, not a diagnosis.",
          "Profesional: Deberías sentarte y descansar. Es consejo general, no diagnóstico.",
          "Advice seguro recomienda una acción y declara su alcance limitado."),
         ("Patient: I would like an appointment. Receptionist: I can book Friday at two.",
          "Paciente: Quisiera una cita. Recepción: Puedo reservar el viernes a las dos.",
          "Los roles permiten pedir y ofrecer una appointment con datos precisos."),
         ("Receptionist: Please arrive early. Patient: Could you confirm the time?",
          "Recepción: Llega antes. Paciente: ¿Podría confirmar la hora?",
          "Confirm verifica la información antes del follow-up."),
         ("Patient: This morning I felt tired while working. Health worker: You should rest; this is general advice, not a diagnosis. Receptionist: Your appointment is Tuesday at nine. Please arrive ten minutes early with the form. Patient: Thank you; I confirm the plan.",
          "Paciente: Esta mañana me sentí cansado mientras trabajaba. Profesional: Deberías descansar; es consejo general, no diagnóstico. Recepción: Tu cita es el martes a las nueve. Llega diez minutos antes con el formulario. Paciente: Gracias; confirmo el plan.",
          "El modelo integra relato, consejo, cita, instrucciones y confirmación en una conversation completa.")],
        pools, remap, uses=all_c, cumulative=all_c)


BUILDERS = {76: build_76, 77: build_77, 78: build_78, 79: build_79, 80: build_80}


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.casefold()).strip()


def audit(classes: list[dict[str, Any]], full: bool) -> dict[str, Any]:
    banned_prompt = re.compile(
        r"\b(?:esta frase|esta oración|lo anterior|el modelo|frase indicada|idea trabajada)\b", re.I)
    signatures: dict[str, str] = {}
    prompts: set[str] = set()
    indices: Counter[int] = Counter()
    totals: Counter[str] = Counter()
    for cls in classes:
        number = int(cls["id"].rsplit("-", 1)[1])
        concept = CONCEPTS[number]
        assert cls["phase"] == PHASES[number]
        assert cls["status"] == "shadow" and cls["runtimeAi"] is False
        assert cls["qualityPolicy"] == QUALITY_POLICY
        assert cls["prerequisites"] == [f"en.n2.class-{number - 1}"]
        assert 4 <= len(cls["teaching"]) <= 6 and 6 <= len(cls["vocabulary"]) <= 12
        assert {k: len(v) for k, v in cls["pools"].items()} == {
            "practiceGuided": 3, "practice": 3, "evaluation": 4, "review": 3}
        items = [(pool, item) for pool, values in cls["pools"].items() for item in values]
        assert len(items) == 13 and len({item["format"] for _, item in items}) >= 4
        assert any(item["format"] == "escribir" for _, item in items)
        assert any(item["format"] == "escuchar" for _, item in items)
        feedbacks: list[str] = []
        local_indices: Counter[int] = Counter()
        for pool, item in items:
            totals[pool] += 1
            prompt = item["prompt"]["es"]
            assert 1 <= len(prompt) <= 90, (item["id"], len(prompt), prompt)
            assert not banned_prompt.search(prompt), (item["id"], prompt)
            assert prompt not in prompts, item["id"]
            prompts.add(prompt)
            feedbacks.append(item["origin"]["feedback"]["es"].casefold())
            if pool == "practiceGuided":
                assert item["teaches"] == [concept] and item["requires"] == []
                assert "hint" in item["origin"]
            else:
                assert item["teaches"] == [] and item["requires"]
                assert "hint" not in item["origin"]
            if item["format"] in {"elegir", "escuchar"}:
                assert len(item["choices"]) >= 3
                index = item["answer"]["index"]
                assert 0 <= index < len(item["choices"])
                local_indices[index] += 1
                indices[index] += 1
            if item["format"] == "completar":
                assert "___" in prompt
                assert item["answer"]["accepted"] == [item["answer"]["text"]]
            if item["format"] == "escribir":
                accepted = item["answer"].get("accepted", [])
                assert len(accepted) >= 2
                assert len({normalize(value) for value in accepted}) >= 2
            signature = canonical({"prompt": item["prompt"], "answer": item["answer"],
                                   "stimulus": item["origin"].get("audio")
                                   or item["origin"].get("text")
                                   or item["origin"].get("pairs")}).casefold()
            assert signature not in signatures, (item["id"], signatures.get(signature))
            signatures[signature] = item["id"]
        assert len(feedbacks) == len(set(feedbacks)), cls["id"]
        assert len(local_indices) >= 2 and max(local_indices.values()) / sum(local_indices.values()) <= .60
        visible = canonical({"teaching": cls["teaching"], "pools": cls["pools"]}).casefold()
        for entry in cls["vocabulary"]:
            assert entry["en"].casefold() in visible, (cls["id"], entry["en"])
        eval_ids = {item["id"] for item in cls["pools"]["evaluation"]}
        assert set(cls["remediationMap"]) == eval_ids
        teach_ids = {item["id"] for item in cls["teaching"]}
        review_ids = {item["id"] for item in cls["pools"]["review"]}
        for mapping in cls["remediationMap"].values():
            assert mapping["reteach"] in teach_ids and mapping["review"] in review_ids
        if cls["phase"] in {"production", "transfer"}:
            reserved = [item for pool in ("evaluation", "review") for item in cls["pools"][pool]
                        if item["format"] == "escribir"]
            assert reserved
            assert any(len(re.findall(r"\b[\w’-]+\b", item["answer"]["text"])) >= 8
                       and len(item["answer"].get("accepted", [])) >= 2 for item in reserved)
    if full:
        assert indices == EXPECTED_INDICES, indices
        close = classes[-1]
        expected = [CONCEPTS[x] for x in range(76, 81)]
        assert close["cumulativeEvaluation"] == expected and close["usesPatterns"] == expected
        integrated = next(x for x in close["pools"]["evaluation"] if x["id"] == "en.n2.c80.e04")
        assert integrated["requires"] == expected
        text = integrated["answer"]["text"].casefold()
        for marker in ("felt dizzy", "hurt my knee", "should", "not a diagnosis",
                       "appointment", "thursday at 11:00", "arrive ten minutes early",
                       "form", "yesterday", "confirm"):
            assert marker in text, marker
    return {"classes": len(classes), "items": sum(totals.values()), "pools": dict(totals),
            "correctIndices": dict(sorted(indices.items())), "fingerprints": len(signatures),
            "prompts": len(prompts)}


def write_class(number: int) -> Path:
    document = BUILDERS[number]()
    audit([document], False)
    path = OUT / f"class-{number}.json"
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_bundle() -> Path:
    classes = [json.loads((OUT / f"class-{n}.json").read_text(encoding="utf-8"))
               for n in range(76, 81)]
    audit(classes, True)
    bundle = {"schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 2,
              "scale": SCALE, "status": "shadow", "runtimeAi": False,
              "selectionPolicy": {"deterministic": True},
              "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
              "range": {"start": 76, "end": 80}, "classes": classes}
    path = OUT / "bundle-76-80.json"
    path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-number", type=int, choices=range(76, 81))
    parser.add_argument("--bundle", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    if args.class_number is not None:
        print(write_class(args.class_number))
    elif args.bundle:
        print(write_bundle())
    elif args.audit:
        classes = [json.loads((OUT / f"class-{n}.json").read_text(encoding="utf-8"))
                   for n in range(76, 81)]
        print(json.dumps(audit(classes, True), ensure_ascii=False, sort_keys=True))
    else:
        parser.error("choose --class-number, --bundle, or --audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
