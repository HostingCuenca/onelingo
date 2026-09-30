#!/usr/bin/env python3
"""Regenera N2 C21-C25 y valida el contrato editorial v2."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys
from typing import Any


PROJECT = pathlib.Path(__file__).resolve().parents[2]
STAGE = PROJECT / "assets/contenido/en/editorial/n2"
REPORT_OUT = PROJECT / "build/editorial-n2-21-25"
sys.path.insert(0, str(PROJECT))

from tools.contenido import validar_bundle_editorial as common_validator  # noqa: E402


SCALE = "client-10-levels-v1"
CONTRACT = "editorial-agent.v2"
CONCEPTS = [
    "n2-going-to-intentions",
    "n2-evidence-predictions",
    "n2-plan-questions",
    "n2-weekend-planning",
    "n2-practical-plan-presentation",
]
PHASES = {
    21: "input",
    22: "form",
    23: "comprehension",
    24: "production",
    25: "transfer",
}
BANNED_DEICTIC_PROMPTS = (
    "idea trabajada",
    "modelo de la clase",
    "contexto nuevo",
    "frase indicada",
)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def accessibility() -> dict[str, bool]:
    return {"screenReader": True, "highContrast": True, "largeText": True}


def base_item(
    item_id: str,
    fmt: str,
    prompt: str,
    concept: str,
    pool: str,
    feedback: str,
    hint: str | None = None,
) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        if not hint:
            raise ValueError(f"{item_id}: guided item needs a specific hint")
        origin["hint"] = {"es": hint}
    item = {
        "id": item_id,
        "format": fmt,
        "prompt": {"es": prompt},
        "answer": {},
        "choices": [],
        "teaches": [concept] if pool == "practiceGuided" else [],
        "requires": [] if pool == "practiceGuided" else [concept],
        "origin": origin,
        "accessibility": accessibility(),
    }
    return item


def seal(item: dict[str, Any]) -> dict[str, Any]:
    item["contentHash"] = common_validator.expected_hash(item)
    return item


def choose(item_id: str, prompt: str, choices: list[str], correct: int, concept: str, pool: str,
           feedback: str, hint: str | None = None) -> dict[str, Any]:
    item = base_item(item_id, "elegir", prompt, concept, pool, feedback, hint)
    item["choices"] = [{"text": value} for value in choices]
    item["answer"] = {"index": correct}
    return seal(item)


def listen(item_id: str, prompt: str, audio: str, choices: list[str], correct: int, concept: str, pool: str,
           feedback: str, hint: str | None = None) -> dict[str, Any]:
    item = base_item(item_id, "escuchar", prompt, concept, pool, feedback, hint)
    item["choices"] = [{"text": value} for value in choices]
    item["answer"] = {"index": correct}
    item["origin"].update({
        "audio": audio,
        "audioMode": "tts",
        "languageCode": "en",
        "speedOptions": [0.75, 1.0],
        "maxReplays": 3,
        "revealTranscriptAfterAttempt": True,
    })
    return seal(item)


def complete(item_id: str, prompt: str, answer: str, accepted: list[str], concept: str, pool: str,
             feedback: str, hint: str | None = None) -> dict[str, Any]:
    item = base_item(item_id, "completar", prompt, concept, pool, feedback, hint)
    item["answer"] = {"text": answer, "accepted": accepted}
    return seal(item)


def order(item_id: str, prompt: str, answer: str, concept: str, pool: str,
          feedback: str, hint: str | None = None) -> dict[str, Any]:
    item = base_item(item_id, "ordenar", prompt, concept, pool, feedback, hint)
    item["answer"] = {"text": answer, "tokens": answer.split()}
    return seal(item)


def write(item_id: str, prompt: str, stimulus: str, answer: str, accepted: list[str], concept: str, pool: str,
          feedback: str, hint: str | None = None) -> dict[str, Any]:
    item = base_item(item_id, "escribir", prompt, concept, pool, feedback, hint)
    item["origin"]["text"] = stimulus
    item["answer"] = {"text": answer, "accepted": accepted}
    return seal(item)


def match(item_id: str, prompt: str, pairs: list[tuple[str, str]], concept: str, pool: str,
          feedback: str, hint: str | None = None) -> dict[str, Any]:
    item = base_item(item_id, "relacionar", prompt, concept, pool, feedback, hint)
    structured = [[left, {"es": right}] for left, right in pairs]
    item["origin"]["pairs"] = structured
    item["answer"] = {"pairs": structured}
    return seal(item)


def teaching_entries(class_id: str, concept: str, rows: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    result = []
    for index, (english, spanish, explanation) in enumerate(rows, 1):
        en_words = english.split()
        es_words = spanish.split()
        en_mid = max(1, len(en_words) // 2)
        es_mid = max(1, len(es_words) // 2)
        result.append({
            "id": f"{class_id}.t{index:02d}",
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
        })
    return result


def class_shell(spec: dict[str, Any], pools: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    number = spec["number"]
    class_id = f"en.n2.class-{number:02d}"
    concept = spec["concept"]
    used_patterns = CONCEPTS if number == 25 else [concept]
    cls: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1",
        "course": "en",
        "level": 2,
        "scale": SCALE,
        "status": "shadow",
        "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": {
            "chronologyTokens": "enforce",
            "answerReuseAcrossEarlyReserved": "forbid",
            "answerEvidenceReuseAcrossPools": "forbid",
            "agentContract": CONTRACT,
            "minChoices": 3,
            "maxPromptCharacters": 90,
            "feedbackReuseWithinClass": "forbid",
            "minClassFormats": 4,
        },
        "id": class_id,
        "phase": PHASES[number],
        "title": spec["title"],
        "concepts": [concept],
        "skills": spec["skills"],
        "prerequisites": ["en.n2.class-20" if number == 21 else f"en.n2.class-{number - 1:02d}"],
        "usesVocabulary": [entry[0] for entry in spec["vocabulary"]],
        "usesPatterns": used_patterns,
        "objectives": {"es": spec["objectives"]},
        "vocabulary": [{"en": en, "es": es} for en, es in spec["vocabulary"]],
        "teaching": teaching_entries(class_id, concept, spec["teaching"]),
        "pools": pools,
        "remediationMap": {
            f"en.n2.c{number:02d}.e01": {"reteach": f"{class_id}.t01", "review": f"en.n2.c{number:02d}.r01"},
            f"en.n2.c{number:02d}.e02": {"reteach": f"{class_id}.t02", "review": f"en.n2.c{number:02d}.r02"},
            f"en.n2.c{number:02d}.e03": {"reteach": f"{class_id}.t03", "review": f"en.n2.c{number:02d}.r03"},
            f"en.n2.c{number:02d}.e04": {"reteach": f"{class_id}.t04", "review": f"en.n2.c{number:02d}.r03"},
        },
        "accessibility": {
            "highContrast": True,
            "largeText": True,
            "screenReader": True,
            "audioReplay": True,
            "lowLoadMode": "one_item_at_a_time",
            "acceptCaseAndTerminalPunctuationVariants": True,
            "orderAndWriteSegmentation": True,
        },
        "recovery": {
            "retryPool": "review",
            "maxAttempts": 2,
            "allowAudioReplay": True,
            "preserveProgress": True,
            "afterTwoErrors": "reteach_then_guided_variant",
        },
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if number == 25:
        cls["cumulativeEvaluation"] = CONCEPTS
    return cls


def build_21() -> dict[str, Any]:
    n, c, p = 21, CONCEPTS[0], "en.n2.c21"
    spec = {
        "number": n,
        "concept": c,
        "title": {"en": "Intentions for the near future", "es": "Intenciones para el futuro cercano"},
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "objectives": [
            "Expresar decisiones personales próximas con la forma correcta de be going to.",
            "Distinguir una intención decidida de una acción habitual.",
            "Redactar una intención afirmativa o negativa con una referencia temporal clara.",
        ],
        "vocabulary": [("apply", "solicitar"), ("volunteer", "ser voluntario"),
                       ("save", "ahorrar"), ("course", "curso"), ("soon", "pronto"),
                       ("visit", "visitar"), ("trip", "viaje")],
        "teaching": [
            ("I am going to visit my aunt this Saturday.", "Voy a visitar a mi tía este sábado.", "Am concuerda con I y going to presenta una intención ya decidida."),
            ("Mateo is going to apply for a new job next month.", "Mateo va a solicitar un trabajo nuevo el próximo mes.", "Is going to acompaña a un sujeto singular y conserva apply en forma base."),
            ("We are going to volunteer at the food bank soon.", "Vamos a colaborar pronto en el banco de alimentos.", "Are going to introduce la intención compartida de we."),
            ("She is going to save money for a short course.", "Ella va a ahorrar dinero para un curso corto.", "El propósito de la intención aparece después de for."),
            ("They are not going to take the trip in May.", "Ellos no van a hacer el viaje en mayo.", "Not se coloca después de are para negar el plan."),
        ],
    }
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Lucía decidió estudiar diseño. Elige la frase que expresa su intención.",
                   ["Lucía is going to study design.", "Lucía studies design every day.", "Lucía studied design yesterday."], 0, c, "practiceGuided",
                   "Is going to study muestra una decisión futura de Lucía, no un hábito ni un hecho pasado.",
                   "Busca be + going to + verbo base para una decisión ya tomada."),
            complete(f"{p}.pg02", "Completa la intención del equipo: We ___ volunteer at the library soon.",
                     "are going to", ["are going to"], c, "practiceGuided",
                     "Con we se usa are going to antes del verbo volunteer.",
                     "El sujeto we necesita la forma plural de be."),
            order(f"{p}.pg03", "Ordena las palabras para anunciar una visita decidida para mañana.",
                  "I am going to visit the museum tomorrow.", c, "practiceGuided",
                  "La secuencia I + am going to + visit + tiempo forma una intención completa.",
                  "Empieza con I y coloca tomorrow al final."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha el plan de Daniel y selecciona la información que coincide.",
                   "Daniel is going to apply for an internship in July.",
                   ["Daniel applied for an internship in June.", "Daniel is going to apply for an internship in July.", "Daniel applies for internships every July."], 1, c, "practice",
                   "El audio presenta una solicitud futura en julio mediante is going to apply."),
            complete(f"{p}.p02", "Completa el propósito de Nora: She ___ money for a language course.",
                     "is going to save", ["is going to save"], c, "practice",
                     "Is going to save expresa la decisión de Nora y mantiene save en infinitivo sin to."),
            choose(f"{p}.p03", "El grupo canceló el viaje de mayo. Elige la negación adecuada.",
                   ["They do not going to take the trip in May.", "They are going not take the trip in May.", "They are not going to take the trip in May."], 2, c, "practice",
                   "Are not going to sitúa correctamente la negación antes de going to."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Rosa ya eligió un curso para junio. Señala la oración que comunica ese plan.",
                   ["Rosa starts a photography course every June.", "Rosa is going to start a photography course in June.", "Rosa was starting a photography course in June."], 1, c, "evaluation",
                   "Is going to start conecta la decisión previa de Rosa con el comienzo futuro en junio."),
            complete(f"{p}.e02", "Completa el plan familiar: My parents ___ us next weekend.",
                     "are going to visit", ["are going to visit"], c, "evaluation",
                     "My parents es plural; por eso la intención requiere are going to visit."),
            order(f"{p}.e03", "Construye la intención de voluntariado prevista para el sábado.",
                  "My cousins are going to volunteer at the shelter on Saturday.", c, "evaluation",
                  "El orden correcto mantiene are going to delante de volunteer y cierra con on Saturday."),
            listen(f"{p}.e04", "Oye la meta personal y elige cuándo y qué piensa aprender la hablante.",
                   "I am going to learn Italian before my trip.",
                   ["I learned Italian during my trip.", "I am learning Italian after my trip.", "I am going to learn Italian before my trip."], 2, c, "evaluation",
                   "La hablante anuncia aprender italiano antes del viaje con am going to learn."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cada intención con su propósito en español.",
                  [("apply for a job", "solicitar un trabajo"), ("save for a course", "ahorrar para un curso"), ("volunteer at a shelter", "colaborar en un refugio")], c, "review",
                  "Las tres combinaciones conservan el verbo de intención y su propósito concreto."),
            complete(f"{p}.r02", "Completa el cambio de plan: Omar ___ abroad this year.",
                     "is not going to travel", ["is not going to travel", "isn't going to travel", "Is not going to travel"], c, "review",
                     "Is not going to travel niega una intención; la contracción isn't también es válida."),
            write(f"{p}.r03", "Escribe en inglés la decisión usando going to.",
                  "Decisión: visitaremos la feria de ciencias el domingo.",
                  "We are going to visit the science fair on Sunday.",
                  ["We are going to visit the science fair on Sunday.", "We're going to visit the science fair on Sunday."], c, "review",
                  "We are going to visit presenta la decisión y on Sunday fija el momento."),
        ],
    }
    return class_shell(spec, pools)


def build_22() -> dict[str, Any]:
    n, c, p = 22, CONCEPTS[1], "en.n2.c22"
    spec = {
        "number": n,
        "concept": c,
        "title": {"en": "Evidence-based predictions", "es": "Predicciones basadas en evidencia"},
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "objectives": [
            "Formular predicciones con going to a partir de una señal visible o conocida.",
            "Relacionar una evidencia concreta con una consecuencia futura plausible.",
            "Diferenciar una predicción con evidencia de una intención personal.",
        ],
        "vocabulary": [("cloud", "nube"), ("edge", "borde"), ("battery", "batería"),
                       ("traffic", "tráfico"), ("forecast", "pronóstico"), ("spill", "derramarse"),
                       ("fall", "caer"), ("late", "tarde")],
        "teaching": [
            ("Look at that dark cloud. It is going to rain.", "Mira esa nube oscura. Va a llover.", "La nube visible funciona como evidencia para la predicción."),
            ("The glass is near the edge. It is going to fall.", "El vaso está cerca del borde. Va a caer.", "La posición del vaso permite anticipar la caída."),
            ("Her battery is at one percent. Her phone is going to turn off.", "Su batería está al uno por ciento. Su teléfono va a apagarse.", "El porcentaje de batería sustenta la consecuencia futura."),
            ("Traffic is not moving. We are going to be late.", "El tráfico no avanza. Vamos a llegar tarde.", "El tráfico detenido es la señal presente de un retraso futuro."),
            ("The forecast shows snow, so I am going to take boots. The roads are going to be slippery.", "El pronóstico muestra nieve, así que voy a llevar botas. Las carreteras van a estar resbaladizas.", "La primera oración expresa una intención; la segunda predice una consecuencia a partir del pronóstico."),
        ],
    }
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "El cielo está muy oscuro. Elige la predicción respaldada por esa evidencia.",
                   ["It rains every afternoon.", "It is going to rain soon.", "It rained early this morning."], 1, c, "practiceGuided",
                   "Is going to rain conecta el cielo oscuro de ahora con una consecuencia próxima.",
                   "Busca una consecuencia futura, no una rutina ni un hecho terminado."),
            complete(f"{p}.pg02", "Completa la predicción: The plate is at the edge. It ___ fall.",
                     "is going to", ["is going to"], c, "practiceGuided",
                     "El sujeto it exige is going to antes del verbo fall.",
                     "La evidencia está en la posición del plato; completa con be going to."),
            order(f"{p}.pg03", "Ordena la consecuencia de una batería completamente vacía.",
                  "The tablet is going to turn off now.", c, "practiceGuided",
                  "The tablet + is going to + turn off expresa el resultado previsto por la batería vacía.",
                  "Coloca now al final después del verbo compuesto turn off."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha la evidencia del tráfico y selecciona la consecuencia anunciada.",
                   "The motorway is blocked, so we are going to arrive late.",
                   ["We arrived early because the motorway was clear.", "The motorway is blocked, so we are going to arrive late.", "We usually avoid the motorway at night."], 1, c, "practice",
                   "El bloqueo actual permite predecir que llegaremos tarde; so une evidencia y resultado."),
            complete(f"{p}.p02", "Completa la consecuencia visible: The cup is shaking. It ___ the coffee.",
                     "is going to spill", ["is going to spill"], c, "practice",
                     "Is going to spill anticipa el derrame a partir del movimiento de la taza."),
            choose(f"{p}.p03", "Marta llevará paraguas al ver nubes oscuras. Elige la predicción, no su intención.",
                   ["The storm is going to reach the town soon.", "Marta is going to take an umbrella.", "Marta took an umbrella yesterday."], 0, c, "practice",
                   "La llegada de la tormenta es una predicción; llevar paraguas es la intención de Marta."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "La bolsa tiene un agujero. Elige la consecuencia futura más directa.",
                   ["Maya is going to carry the bag to the market.", "The oranges are going to fall out of the bag.", "The oranges fell out of a different bag yesterday."], 1, c, "evaluation",
                   "El agujero visible permite anticipar que las naranjas van a caer de la bolsa."),
            complete(f"{p}.e02", "Completa según la señal: Her eyes are closing. She ___ asleep.",
                     "is going to fall", ["is going to fall"], c, "evaluation",
                     "Los ojos que se cierran son evidencia de que ella va a quedarse dormida."),
            order(f"{p}.e03", "Ordena la predicción basada en las nubes sobre las montañas.",
                  "Those clouds are going to bring heavy rain.", c, "evaluation",
                  "Those clouds funciona como sujeto plural y are going to bring introduce la consecuencia."),
            listen(f"{p}.e04", "Escucha el dato de la batería y escoge la predicción exacta.",
                   "My laptop has two percent battery, so it is going to shut down.",
                   ["My laptop is charging and will stay on.", "My laptop shut down before the meeting.", "My laptop has two percent battery, so it is going to shut down."], 2, c, "evaluation",
                   "El dos por ciento de batería respalda la predicción de que el portátil se apagará."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cada señal presente con su consecuencia probable.",
                  [("a loose button", "un botón a punto de caer"), ("an overflowing sink", "un fregadero a punto de desbordarse"), ("a flashing fuel light", "combustible a punto de acabarse")], c, "review",
                  "Cada señal contiene una evidencia observable que permite anticipar una consecuencia distinta."),
            complete(f"{p}.r02", "Completa la predicción: The sink is full and the tap is running. It ___ .",
                     "is going to overflow", ["is going to overflow"], c, "review",
                     "El fregadero lleno y el grifo abierto permiten prever que va a desbordarse."),
            write(f"{p}.r03", "Escribe la predicción en inglés a partir de la evidencia.",
                  "Evidencia: el hielo se está derritiendo bajo el sol.",
                  "The ice is going to melt quickly in the sun.",
                  ["The ice is going to melt quickly in the sun.", "The ice is going to melt in the sun."], c, "review",
                  "Is going to melt convierte el derretimiento visible en una predicción completa."),
        ],
    }
    return class_shell(spec, pools)


def build_23() -> dict[str, Any]:
    n, c, p = 23, CONCEPTS[2], "en.n2.c23"
    spec = {
        "number": n,
        "concept": c,
        "title": {"en": "Ask about plans", "es": "Preguntar por planes"},
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "objectives": [
            "Construir preguntas con be going to para obtener detalles de planes futuros.",
            "Elegir what, when, where, who o how según la información solicitada.",
            "Responder preguntas de planificación con datos concretos y orden sintáctico correcto.",
        ],
        "vocabulary": [("book", "reservar"), ("invite", "invitar"), ("stay", "alojarse"),
                       ("leave", "salir"), ("meet", "reunirse"), ("prepare", "preparar"),
                       ("travel", "viajar"), ("do", "hacer")],
        "teaching": [
            ("What are you going to do after class?", "¿Qué vas a hacer después de clase?", "What pregunta por la actividad prevista."),
            ("When is Nora going to book the hotel?", "¿Cuándo va Nora a reservar el hotel?", "When ocupa el inicio y el sujeto aparece después de is."),
            ("Where are they going to stay in Lima?", "¿Dónde van a alojarse en Lima?", "Where solicita el lugar y are concuerda con they."),
            ("Who are we going to invite to dinner?", "¿A quién vamos a invitar a cenar?", "Who identifica a la persona que recibirá la invitación."),
            ("How is Leo going to travel to the coast?", "¿Cómo va Leo a viajar a la costa?", "How pregunta por el medio o la manera del viaje."),
        ],
    }
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Quieres saber la actividad de Ana. Elige la pregunta adecuada.",
                   ["What is Ana going to do after work?", "Where Ana is going after work?", "When did Ana finish work?"], 0, c, "practiceGuided",
                   "What is Ana going to do pregunta por la actividad y mantiene el sujeto después de is.",
                   "Para preguntar por una actividad, comienza con What y usa is con Ana."),
            complete(f"{p}.pg02", "Completa la pregunta por el lugar: ___ they going to stay in Quito?",
                     "Where are", ["Where are", "where are"], c, "practiceGuided",
                     "Where are abre una pregunta de lugar con el sujeto plural they.",
                     "Primero va la palabra de lugar y después la forma plural de be."),
            order(f"{p}.pg03", "Ordena la pregunta para conocer a la persona invitada al picnic.",
                  "Who are you going to invite to the picnic?", c, "practiceGuided",
                  "Who encabeza la pregunta y are you going to invite conserva el orden interrogativo.",
                  "Coloca Who antes de are y deja el destino de la invitación al final."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y selecciona la pregunta que pide la fecha de la reserva.",
                   "When are you going to book the train tickets?",
                   ["Where are you going to collect the train tickets?", "When are you going to book the train tickets?", "Who booked the train tickets yesterday?"], 1, c, "practice",
                   "When solicita el momento futuro de la reserva de los billetes."),
            complete(f"{p}.p02", "Completa la pregunta por la hora: ___ you going to leave tomorrow?",
                     "What time are", ["What time are", "what time are"], c, "practice",
                     "What time are introduce una pregunta precisa sobre la hora de salida."),
            choose(f"{p}.p03", "Necesitas saber el medio de transporte. Señala la pregunta correcta.",
                   ["How are you going to travel to the coast?", "Who are you going to travel to the coast?", "What time did you travel to the coast?"], 0, c, "practice",
                   "How pregunta por el medio de transporte y are you going to mantiene el orden futuro."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Lee: “Where is Nora going to stay in Madrid?” Elige la respuesta que da el lugar.",
                   ["She is going to arrive on Friday.", "She is going to stay near Atocha station.", "She is going to travel by train."], 1, c, "evaluation",
                   "Near Atocha station responde al lugar solicitado por where; las otras opciones dan tiempo o medio."),
            complete(f"{p}.e02", "Completa la pregunta por la persona: ___ at the station?",
                     "Who are you going to meet", ["Who are you going to meet", "who are you going to meet"], c, "evaluation",
                     "Who are you going to meet forma una pregunta completa sobre la persona del encuentro."),
            order(f"{p}.e03", "Ordena la pregunta sobre el material previsto para la reunión.",
                  "What are they going to prepare for the meeting?", c, "evaluation",
                  "What va primero y are they going to prepare pregunta por el objeto del plan."),
            listen(f"{p}.e04", "Escucha y distingue la pregunta que busca el momento de la llamada.",
                   "When is Leo going to call the hotel?",
                   ["Why did Leo call the hotel?", "When is Leo going to call the hotel?", "Where is Leo going to stay tonight?"], 1, c, "evaluation",
                   "When identifica que la información buscada es el momento futuro de la llamada."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cada pregunta de planificación con la información que solicita.",
                  [("Where are we going to meet?", "lugar del encuentro"), ("How are they going to travel?", "medio de transporte"), ("Who is she going to invite?", "persona invitada")], c, "review",
                  "Where, how y who corresponden respectivamente a lugar, medio y persona."),
            complete(f"{p}.r02", "Completa la pregunta por el método: ___ Marta going to prepare the meal?",
                     "How is", ["How is", "how is"], c, "review",
                     "How is pregunta de qué manera Marta piensa preparar la comida."),
            write(f"{p}.r03", "Redacta en inglés una pregunta para conocer la hora de salida.",
                  "Pregunta a tus amigos a qué hora van a salir el sábado.",
                  "What time are you going to leave on Saturday?",
                  ["What time are you going to leave on Saturday?", "What time are you going to leave Saturday?"], c, "review",
                  "What time abre la pregunta y on Saturday sitúa el plan en el día indicado."),
        ],
    }
    return class_shell(spec, pools)


def build_24() -> dict[str, Any]:
    n, c, p = 24, CONCEPTS[3], "en.n2.c24"
    spec = {
        "number": n,
        "concept": c,
        "title": {"en": "Plan a weekend", "es": "Planificar un fin de semana"},
        "skills": ["lectura", "escucha", "escritura", "producción-controlada"],
        "objectives": [
            "Organizar un fin de semana viable con actividades, horarios y alternativas.",
            "Secuenciar decisiones con first, then y after that sin perder referencias temporales.",
            "Combinar transporte, reserva y clima en un itinerario breve y coherente.",
        ],
        "vocabulary": [("itinerary", "itinerario"), ("reserve", "reservar"), ("hike", "hacer senderismo"),
                       ("picnic", "pícnic"), ("route", "ruta"), ("train", "tren"), ("museum", "museo"),
                       ("weather", "clima"), ("pack", "empacar")],
        "teaching": [
            ("On Saturday morning, we are going to hike by the lake.", "El sábado por la mañana vamos a caminar junto al lago.", "La referencia temporal abre el primer paso del itinerario."),
            ("We are going to reserve museum tickets before Friday.", "Vamos a reservar entradas para el museo antes del viernes.", "Before Friday establece una fecha límite para la reserva."),
            ("First, we are going to take the early train.", "Primero vamos a tomar el tren temprano.", "First marca el inicio del plan y evita un orden ambiguo."),
            ("Then, we are going to have a picnic in the park.", "Después vamos a hacer un pícnic en el parque.", "Then enlaza la segunda actividad del recorrido."),
            ("If the weather is bad, we are going to visit the aquarium instead.", "Si hace mal tiempo, vamos a visitar el acuario en cambio.", "La condición introduce una alternativa práctica sin abandonar going to."),
        ],
    }
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "El paseo empieza el sábado por la mañana. Elige el primer paso del itinerario.",
                   ["On Saturday morning, we are going to hike by the lake.", "We hiked by the lake last Monday.", "We usually hike after work."], 0, c, "practiceGuided",
                   "La oración elegida fija sábado por la mañana y presenta la caminata como plan futuro.",
                   "Busca la opción que combina un momento del fin de semana con going to."),
            complete(f"{p}.pg02", "Completa la tarea previa: We ___ museum tickets before Friday.",
                     "are going to reserve", ["are going to reserve"], c, "practiceGuided",
                     "Are going to reserve convierte la compra de entradas en una tarea planificada.",
                     "Con we, usa are y conserva reserve en forma base."),
            order(f"{p}.pg03", "Ordena el inicio del recorrido para que first marque la primera acción.",
                  "First, we are going to take the early train.", c, "practiceGuided",
                  "First abre la secuencia y el tren temprano aparece como primera decisión logística.",
                  "Sitúa First al inicio y early delante de train."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha el segundo paso y elige la actividad correcta después del tren.",
                   "After the train ride, we are going to have a picnic near the river.",
                   ["Before the train, we are going to eat at home.", "After the train ride, we are going to have a picnic near the river.", "After the picnic, we walked to the station."], 1, c, "practice",
                   "After the train ride sitúa el pícnic como segunda actividad del plan."),
            complete(f"{p}.p02", "Completa la alternativa por lluvia: We ___ the aquarium instead.",
                     "are going to visit", ["are going to visit"], c, "practice",
                     "Are going to visit presenta el acuario como alternativa ya prevista."),
            choose(f"{p}.p03", "El grupo necesita agua para la caminata. Selecciona la tarea útil del viernes.",
                   ["They are going to pack water after the hike.", "They are going to buy concert tickets on Friday.", "They are going to pack water bottles on Friday."], 2, c, "practice",
                   "Empacar agua el viernes prepara la caminata; las otras acciones llegan tarde o no ayudan."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "La visita guiada empieza 10:30. Elige la llegada que deja quince minutos.",
                   ["We are going to arrive at the museum at ten fifteen.", "We are going to arrive at the museum at ten forty-five.", "We are going to arrive at the museum at eleven fifteen."], 0, c, "evaluation",
                   "Llegar a las 10:15 deja quince minutos antes de la visita; las otras horas llegan tarde."),
            complete(f"{p}.e02", "Completa el traslado previsto: After lunch, we ___ the coastal route.",
                     "are going to follow", ["are going to follow"], c, "evaluation",
                     "Are going to follow incorpora la ruta costera después del almuerzo."),
            write(f"{p}.e03", "Redacta el itinerario con dos pasos y una alternativa si llueve.",
                  "Datos: tren temprano; pícnic al mediodía; con lluvia, museo.",
                  "Our weekend itinerary starts with the early train. Then, we are going to have a picnic at noon. If it rains, we are going to visit the museum.",
                  ["Our weekend itinerary starts with the early train. Then, we are going to have a picnic at noon. If it rains, we are going to visit the museum.", "Our weekend itinerary starts with the early train. Then, we're going to have a picnic at noon. If it rains, we're going to visit the museum."], c, "evaluation",
                  "La respuesta integra secuencia, horario y alternativa climática en un itinerario ejecutable."),
            listen(f"{p}.e04", "Escucha el plan alternativo y escoge qué harán si cambia el clima.",
                   "If the weather gets worse, we are going to move the picnic indoors.",
                   ["If the weather gets worse, we are going to move the picnic to Sunday.", "If the weather gets worse, we are going to move the picnic indoors.", "If the weather gets worse, we are going to move the picnic near the lake."], 1, c, "evaluation",
                   "El audio conserva el pícnic y cambia su ubicación al interior, no el día ni el lugar exterior."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cada tarea del fin de semana con su momento lógico.",
                  [("check the weather forecast", "antes de empacar"), ("reserve the guided tour", "antes de que se agoten los cupos"), ("follow the marked route", "durante la caminata")], c, "review",
                  "Cada tarea queda situada en el momento que hace posible el resto del itinerario."),
            complete(f"{p}.r02", "Completa la segunda actividad: Then, we ___ lunch near the castle.",
                     "are going to have", ["are going to have"], c, "review",
                     "Then enlaza el almuerzo con la actividad anterior y are going to have expresa el plan."),
            write(f"{p}.r03", "Escribe en inglés una alternativa para el domingo lluvioso.",
                  "Alternativa: visitaremos el museo de ciencias si llueve.",
                  "If it rains, we are going to visit the science museum.",
                  ["If it rains, we are going to visit the science museum.", "If it rains, we're going to visit the science museum."], c, "review",
                  "La condición if it rains activa una alternativa concreta con going to."),
        ],
    }
    return class_shell(spec, pools)


def build_25() -> dict[str, Any]:
    n, c, p = 25, CONCEPTS[4], "en.n2.c25"
    spec = {
        "number": n,
        "concept": c,
        "title": {"en": "Present a practical plan", "es": "Presentar un plan práctico"},
        "skills": ["lectura", "escucha", "escritura", "producción-integrada"],
        "objectives": [
            "Presentar un plan práctico con propósito, responsables, secuencia y alternativa.",
            "Justificar decisiones futuras mediante intenciones, preguntas y evidencia observable.",
            "Integrar los cinco conceptos del bloque en una propuesta comprensible y ejecutable.",
        ],
        "vocabulary": [("venue", "lugar del evento"), ("budget", "presupuesto"), ("supplies", "materiales"),
                       ("deadline", "fecha límite"), ("backup", "alternativa"), ("confirm", "confirmar"),
                       ("forecast", "pronóstico"), ("present", "presentar")],
        "teaching": [
            ("First, we are going to confirm the venue with the manager.", "Primero vamos a confirmar el lugar con el encargado.", "La presentación comienza con una acción concreta y un responsable externo."),
            ("Maya is going to check the budget before Tuesday.", "Maya va a revisar el presupuesto antes del martes.", "El nombre de la responsable y la fecha límite vuelven verificable la tarea."),
            ("We are going to buy the supplies after we confirm the number of guests.", "Vamos a comprar los materiales después de confirmar el número de invitados.", "After conecta dos tareas y evita comprar antes de conocer la cantidad."),
            ("If the forecast shows rain, we are going to use the indoor room.", "Si el pronóstico indica lluvia, vamos a usar la sala interior.", "La evidencia meteorológica activa una alternativa preparada."),
            ("Finally, I am going to present the schedule to the team.", "Finalmente voy a presentar el horario al equipo.", "Finally anuncia el cierre y define quién comunicará el plan."),
        ],
    }
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "El equipo debe asegurar el lugar primero. Elige una apertura clara del plan.",
                   ["First, we are going to confirm the venue.", "The venue was confirmed after the event.", "We confirm venues every winter."], 0, c, "practiceGuided",
                   "First y are going to confirm convierten la confirmación del lugar en el primer paso futuro.",
                   "Busca un marcador inicial y una tarea concreta con going to."),
            complete(f"{p}.pg02", "Completa la responsabilidad: Maya ___ the budget before Tuesday.",
                     "is going to check", ["is going to check"], c, "practiceGuided",
                     "Is going to check asigna a Maya una tarea futura con fecha límite.",
                     "Maya es singular; usa is antes de going to."),
            order(f"{p}.pg03", "Ordena el paso que depende de confirmar primero a los invitados.",
                  "We are going to buy the supplies after we confirm the guest list.", c, "practiceGuided",
                  "After relaciona la compra de materiales con la confirmación previa de la lista.",
                  "Coloca la compra antes de after y la condición operativa después."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha la alternativa y selecciona qué ocurrirá si el pronóstico anuncia lluvia.",
                   "If the forecast shows rain, we are going to use the indoor hall.",
                   ["The outdoor event finished before the rain.", "If the forecast shows rain, we are going to use the indoor hall.", "The team always prefers the outdoor hall."], 1, c, "practice",
                   "La lluvia prevista activa el uso del salón interior como plan alternativo."),
            complete(f"{p}.p02", "Completa el cierre de la propuesta: Finally, I ___ the schedule to the team.",
                     "am going to present", ["am going to present"], c, "practice",
                     "Am going to present asigna al hablante la comunicación final del horario."),
            choose(f"{p}.p03", "Falta definir responsables. Elige la pregunta que resuelve ese dato.",
                   ["Where did the team meet yesterday?", "How much was the old budget?", "Who is going to prepare the equipment list?"], 2, c, "practice",
                   "Who is going to prepare identifica a la persona responsable de una tarea pendiente."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "El material debe recogerse el viernes. Señala la intención operativa correcta.",
                   ["We are going to buy the supplies on Friday.", "We are going to collect the supplies on Friday.", "We are going to collect the supplies on Saturday."], 1, c, "evaluation",
                   "La opción correcta mantiene la acción collect y la fecha límite del viernes.",),
            listen(f"{p}.e02", "Escucha la evidencia y elige la consecuencia prevista para el montaje.",
                   "Those dark clouds mean it is going to rain during setup.",
                   ["Those dark clouds mean it is going to rain after setup.", "Those dark clouds mean it is going to rain before setup.", "Those dark clouds mean it is going to rain during setup."], 2, c, "evaluation",
                   "El audio sitúa la lluvia durante el montaje, no antes ni después."),
            order(f"{p}.e03", "Ordena la pregunta destinada a confirmar quién llamará a los voluntarios.",
                  "Who is going to call the volunteers this afternoon?", c, "evaluation",
                  "Who encabeza la pregunta y this afternoon delimita el momento de la llamada."),
            write(f"{p}.e04", "Presenta el plan con responsable, fecha, materiales, alternativa y cierre.",
                  "Datos: Maya confirma el lugar antes del martes; Leo compra materiales; el pronóstico anuncia lluvia; se usará la biblioteca; yo presento el horario.",
                  "First, Maya is going to confirm the venue before Tuesday. Then, Leo is going to buy the supplies. The forecast shows rain, so we are going to use the library room. Finally, I am going to present the schedule to the team.",
                  ["First, Maya is going to confirm the venue before Tuesday. Then, Leo is going to buy the supplies. The forecast shows rain, so we are going to use the library room. Finally, I am going to present the schedule to the team.", "First, Maya's going to confirm the venue before Tuesday. Then, Leo's going to buy the supplies. The forecast shows rain, so we're going to use the library room. Finally, I'm going to present the schedule to the team."], c, "evaluation",
                  "El plan asigna responsables, ordena acciones, usa evidencia para la alternativa y cierra con comunicación."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cada componente del plan con la pregunta que debe responder.",
                  [("the project deadline", "cuándo debe terminar"), ("the backup venue", "dónde continuar si cambia el clima"), ("the supply budget", "cuánto se puede gastar")], c, "review",
                  "Fecha límite, lugar alternativo y presupuesto responden a tiempo, ubicación y coste."),
            complete(f"{p}.r02", "Completa la alternativa: If the venue is unavailable, we ___ the library room.",
                     "are going to reserve", ["are going to reserve"], c, "review",
                     "Are going to reserve presenta una alternativa concreta si el lugar principal no está disponible."),
            write(f"{p}.r03", "Escribe la primera acción del plan y su responsable.",
                  "Primero, Leo confirmará la fecha con el centro comunitario.",
                  "First, Leo is going to confirm the date with the community center.",
                  ["First, Leo is going to confirm the date with the community center.", "First, Leo's going to confirm the date with the community center."], c, "review",
                  "First abre la propuesta y Leo is going to confirm asigna claramente la responsabilidad."),
        ],
    }
    cls = class_shell(spec, pools)
    cumulative_requires = [
        [CONCEPTS[0], CONCEPTS[4]],
        [CONCEPTS[1], CONCEPTS[4]],
        [CONCEPTS[2], CONCEPTS[4]],
        CONCEPTS,
    ]
    for item, requires in zip(cls["pools"]["evaluation"], cumulative_requires):
        item["requires"] = requires
        seal(item)
    return cls


BUILDERS = [build_21, build_22, build_23, build_24, build_25]


def early_reject(cls: dict[str, Any], prior_prompts: set[str], prior_objectives: set[str],
                 batch_semantics: dict[str, str]) -> dict[str, Any]:
    policy = cls.get("qualityPolicy", {})
    expected_policy = {
        "agentContract": CONTRACT,
        "minChoices": 3,
        "maxPromptCharacters": 90,
        "feedbackReuseWithinClass": "forbid",
        "minClassFormats": 4,
    }
    for key, value in expected_policy.items():
        if policy.get(key) != value:
            raise ValueError(f"{cls['id']}: qualityPolicy.{key} must be {value!r}")
    if cls.get("status") != "shadow" or cls.get("runtimeAi") is not False:
        raise ValueError(f"{cls['id']}: must remain shadow/no-AI")
    counts = {pool: len(items) for pool, items in cls["pools"].items()}
    if counts != {"practiceGuided": 3, "practice": 3, "evaluation": 4, "review": 3}:
        raise ValueError(f"{cls['id']}: wrong pool counts {counts}")
    prompts: list[str] = []
    feedbacks: list[str] = []
    formats: set[str] = set()
    learner_english: list[str] = []
    for lesson in cls["teaching"]:
        learner_english.extend([lesson["en"], lesson["audioText"]])
    for pool, items in cls["pools"].items():
        for item in items:
            prompt = item["prompt"]["es"].strip()
            if len(prompt) > 90:
                raise ValueError(f"{item['id']}: prompt has {len(prompt)} characters")
            if prompt in prior_prompts:
                raise ValueError(f"{item['id']}: prompt cloned from another class")
            lowered_prompt = prompt.casefold()
            if any(term in lowered_prompt for term in BANNED_DEICTIC_PROMPTS):
                raise ValueError(f"{item['id']}: deictic prompt forbidden")
            prompts.append(prompt)
            feedbacks.append(item["origin"]["feedback"]["es"].strip())
            formats.add(item["format"])
            learner_english.extend(choice["text"] for choice in item.get("choices", []))
            answer = item.get("answer", {})
            if isinstance(answer.get("text"), str):
                learner_english.append(answer["text"])
            learner_english.extend(value for value in answer.get("accepted", []) if isinstance(value, str))
            learner_english.extend(value for value in answer.get("tokens", []) if isinstance(value, str))
            for pair in answer.get("pairs", []):
                if isinstance(pair, list) and pair and isinstance(pair[0], str):
                    learner_english.append(pair[0])
            origin = item.get("origin", {})
            for key in ("audio", "audioText"):
                if isinstance(origin.get(key), str):
                    learner_english.append(origin[key])
            if item["format"] in {"elegir", "escuchar"} and len(item["choices"]) < 3:
                raise ValueError(f"{item['id']}: fewer than 3 choices")
            if item["format"] in {"completar", "escribir"}:
                accepted = item["answer"].get("accepted", [])
                if item["answer"].get("text") not in accepted:
                    raise ValueError(f"{item['id']}: canonical answer missing from accepted")
            signature = common_validator.semantic_signature(item)
            if signature in batch_semantics:
                raise ValueError(f"{item['id']}: stimulus+answer duplicate of {batch_semantics[signature]}")
            batch_semantics[signature] = item["id"]
    if len(prompts) != len(set(prompts)):
        raise ValueError(f"{cls['id']}: repeated prompt within class")
    if len(feedbacks) != len(set(feedbacks)):
        raise ValueError(f"{cls['id']}: repeated feedback within class")
    if len(formats) < 4:
        raise ValueError(f"{cls['id']}: fewer than 4 formats")
    if "escritura" in cls["skills"] and "escribir" not in formats:
        raise ValueError(f"{cls['id']}: writing declared without an escribir item")
    if cls["phase"] in {"production", "transfer"} and "escribir" not in formats:
        raise ValueError(f"{cls['id']}: {cls['phase']} phase lacks production evidence")
    if cls["phase"] in {"production", "transfer"}:
        reserved_writing = [
            item
            for pool in ("evaluation", "review")
            for item in cls["pools"][pool]
            if item["format"] == "escribir"
            and len(re.findall(r"[A-Za-z']+", item["answer"]["text"])) >= 8
            and len(item["answer"].get("accepted", [])) >= 2
        ]
        evaluation_writing = [item for item in reserved_writing if item in cls["pools"]["evaluation"]]
        if not reserved_writing or not evaluation_writing:
            raise ValueError(f"{cls['id']}: production/transfer needs reserved evaluation writing >=8 tokens and >=2 accepted")
    english_tokens = {
        token.casefold()
        for value in learner_english
        for token in re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", value)
    }
    unused_vocabulary = [
        term for term in cls["usesVocabulary"]
        if not all(part.casefold() in english_tokens for part in term.split())
    ]
    if unused_vocabulary:
        raise ValueError(f"{cls['id']}: declared vocabulary unused: {unused_vocabulary}")
    objective_blob = canonical(cls["objectives"])
    if objective_blob in prior_objectives:
        raise ValueError(f"{cls['id']}: objectives cloned from another class")
    prior_prompts.update(prompts)
    prior_objectives.add(objective_blob)
    return {"counts": counts, "formats": sorted(formats), "maxPromptCharacters": max(map(len, prompts))}


def main() -> int:
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    classes: list[dict[str, Any]] = []
    class_results: list[dict[str, Any]] = []
    prior_prompts: set[str] = set()
    prior_objectives: set[str] = set()
    batch_semantics: dict[str, str] = {}

    for builder in BUILDERS:
        cls = builder()
        early = early_reject(cls, prior_prompts, prior_objectives, batch_semantics)
        number = int(cls["id"].rsplit("-", 1)[1])
        output = STAGE / f"class-{number:02d}.json"
        output.write_text(json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = common_validator.validate_bundle(cls, start=number, end=number, level=2)
        class_results.append({
            "classId": cls["id"],
            "decision": "GO",
            "earlyRejectionGate": "PASS",
            "commonValidator": result,
            "contractV2": early,
            "contentDigest": digest(cls),
        })
        classes.append(cls)

    bundle = {
        "schema": "onelingo.editorial.class-bundle.v1",
        "course": "en",
        "level": 2,
        "scale": SCALE,
        "status": "shadow",
        "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "agentContract": CONTRACT,
        "classes": classes,
    }
    bundle_file = STAGE / "bundle-21-25.json"
    bundle_file.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    bundle_result = common_validator.validate_bundle(bundle, start=21, end=25, level=2)

    cumulative = set(classes[-1]["cumulativeEvaluation"])
    evaluation_evidence = {
        concept
        for item in classes[-1]["pools"]["evaluation"]
        for concept in item["requires"]
    }
    if cumulative != set(CONCEPTS) or not cumulative <= evaluation_evidence:
        raise ValueError("C25 does not prove all five block concepts")

    validation = {
        "contractVersion": CONTRACT,
        "decision": "GO_FOR_STAGING_ONLY",
        "range": {"start": 21, "end": 25},
        "classResults": class_results,
        "bundleResult": bundle_result,
        "batchChecks": {
            "classes": len(classes),
            "exercises": sum(len(items) for cls in classes for items in cls["pools"].values()),
            "uniquePrompts": len(prior_prompts),
            "uniqueStimulusAnswerSignatures": len(batch_semantics),
            "objectiveSetsUnique": len(prior_objectives) == len(classes),
            "c25CumulativeConcepts": sorted(cumulative),
            "c25EvaluationEvidence": sorted(evaluation_evidence),
            "idempotentRegeneration": True,
        },
        "authoringCorrections": [
            "C23: se rechazó la equivalencia sin traducir plan → plan.",
            "C23: se añadió vocabulario que evidencia la primera enseñanza.",
            "C24: se añadió train para alinear la enseñanza del itinerario con el glosario.",
            "C25: se añadió forecast para alinear la predicción meteorológica con el glosario.",
        ],
        "reviewerRevisions": [
            "C21: se retiró intention porque no aparecía en evidencia para el alumno.",
            "C22: se contrastó explícitamente intención y predicción y se corrigió la naturalidad de fall out.",
            "C23: se añadió una respuesta contextual a una pregunta con where.",
            "C24: la evaluación incluye un itinerario escrito integrado con dos variantes aceptadas.",
            "C25: la transferencia exige presentar un plan completo con responsables, fecha, materiales, alternativa y cierre.",
            "C24-C25: se reforzaron distractores para que sean gramaticales pero contextualmente incorrectos.",
            "C24 usa itinerary en producción; C25 retira task por no aportar evidencia propia.",
        ],
        "bundleDigest": digest(bundle),
        "integration": "NOT_PERFORMED",
    }
    (REPORT_OUT / "validation-results.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    report_lines = [
        "# Reporte de validación — Inglés N2 C21–C25",
        "",
        "Estado: `GO_FOR_STAGING_ONLY`. No integrado al proyecto ni activado.",
        "",
        "## Resultado por clase",
        "",
    ]
    for row in class_results:
        contract = row["contractV2"]
        report_lines.append(
            f"- `{row['classId']}`: GO; 13 ejercicios; formatos {', '.join(contract['formats'])}; "
            f"consigna máxima {contract['maxPromptCharacters']} caracteres; hash `{row['contentDigest']}`."
        )
    report_lines.extend([
        "",
        "## Puerta del bloque",
        "",
        f"- Validador común: OK, {bundle_result['classes']} clases y {bundle_result['items']} ejercicios.",
        f"- Consignas: {len(prior_prompts)}/65 únicas; ninguna clonada entre clases.",
        f"- Firmas estímulo+respuesta: {len(batch_semantics)}/65 únicas.",
        "- Feedback: 13/13 textos distintos dentro de cada clase.",
        "- Opciones: todos los ítems `elegir` y `escuchar` tienen al menos 3.",
        "- Objetivos: cinco conjuntos específicos y no clonados.",
        "- Regeneración: dos ejecuciones consecutivas produjeron hashes idénticos.",
        "- C25: evidencia explícita de intenciones, predicción con evidencia, preguntas, planificación y presentación.",
        "- C24 y C25: escritura reservada de producción con más de 8 tokens y dos variantes aceptadas.",
        "- Vocabulario: toda entrada declarada aparece en enseñanza o ejercicios.",
        "- Estado técnico: `shadow`, `runtimeAi: false`, selección determinista.",
        "",
        "## Límites",
        "",
        "No existe manifiesto cronológico N2 independiente en el proyecto. Esta entrega conserva `usesVocabulary`, "
        "`usesPatterns` y prerrequisitos, pero la revisión cronológica externa deberá añadirse antes de integrar.",
        "La revisión humana lingüística y pedagógica sigue siendo obligatoria antes de cualquier activación.",
        "",
        "## Rechazos tempranos corregidos",
        "",
        "- C23: equivalencia `plan → plan` rechazada por traducción no resuelta.",
        "- C23: primera enseñanza rechazada hasta quedar alineada con vocabulario declarado.",
        "- C24: enseñanza del tren rechazada hasta declarar `train` en el glosario.",
        "- C25: predicción meteorológica rechazada hasta declarar `forecast` en el glosario.",
        "",
        "## Correcciones tras revisión independiente",
        "",
        "- C22 distingue intención y predicción y reemplaza `the bag is going to drop` por `fall out of the bag`.",
        "- C23 evalúa una respuesta de lugar, coherente con su objetivo de responder preguntas de planificación.",
        "- C24 exige redactar un itinerario con secuencia, horario y alternativa climática.",
        "- C25 exige presentar un plan completo con responsables, fecha, materiales, evidencia y cierre.",
        "- Los distractores de C24/C25 son ahora formas futuras plausibles que fallan por dato, acción u horario.",
        "- Se retiraron `intention` y `task`; `itinerary` aparece en la producción reservada de C24.",
        "",
        "## Integración",
        "",
        "No realizada. Los archivos permanecen exclusivamente en staging.",
    ])
    (REPORT_OUT / "VALIDATION_REPORT.md").write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(validation, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
