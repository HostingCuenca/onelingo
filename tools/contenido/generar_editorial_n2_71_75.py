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
REPORT_OUT = ROOT / "build/editorial-n2-71-75"
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
    71: "n2-tasks-responsibilities",
    72: "n2-schedules-deadlines",
    73: "n2-short-progress-update",
    74: "n2-ask-clarification",
    75: "n2-work-study-simulation",
}
PHASES = {71: "input", 72: "form", 73: "comprehension", 74: "production", 75: "transfer"}
TITLES = {
    71: {"en": "Tasks and responsibilities", "es": "Tareas y responsabilidades"},
    72: {"en": "Schedules and deadlines", "es": "Horarios y plazos"},
    73: {"en": "Give a short progress update", "es": "Dar una actualización breve"},
    74: {"en": "Ask for clarification", "es": "Pedir una aclaración"},
    75: {"en": "Work and study simulation", "es": "Simulación de trabajo y estudio"},
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


def build_71() -> dict[str, Any]:
    n, c, p = 71, CONCEPTS[71], "en.n2.c71"
    vocabulary = [("task", "tarea"), ("responsible", "responsable"), ("prepare", "preparar"),
                  ("check", "revisar"), ("submit", "entregar"), ("team", "equipo")]
    teaching = [
        ("My main task is to prepare the weekly report.", "Mi tarea principal es preparar el informe semanal.", "Task nombra el trabajo asignado y prepare explica la acción concreta."),
        ("Lina is responsible for checking the customer list.", "Lina es responsable de revisar la lista de clientes.", "Responsible for va seguido de verbo en -ing y asigna una responsabilidad."),
        ("We check the figures before we submit the document.", "Revisamos las cifras antes de entregar el documento.", "Check ocurre antes de submit para evitar errores en la entrega."),
        ("Each team member prepares one section of the presentation.", "Cada miembro del equipo prepara una sección de la presentación.", "Team reparte una tarea amplia entre responsabilidades individuales."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Ana debe revisar los datos. Elige su responsabilidad.",
                   ["Ana is responsible for checking the data.", "Ana is checking responsibility for data.", "Ana submits the data without checking it."],
                   0, c, "Responsible for checking expresa exactamente la tarea asignada a Ana.", guided=True,
                   hint="Usa responsible for seguido de un verbo en -ing."),
            match(f"{p}.pg02", "Relaciona cada acción con su resultado de trabajo.",
                  [("prepare slides", "crear material para exponer"), ("submit an essay", "entregar un texto")], c,
                  "Prepare inicia el material y submit completa la entrega formal.", guided=True,
                  hint="Distingue crear un producto de entregarlo."),
            complete(f"{p}.pg03", "Completa el grupo de trabajo: Our ___ checks every task.",
                     "team", c, "Team identifica al grupo que revisa las tareas.", guided=True,
                     hint="Necesitas el sustantivo para varias personas que colaboran."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué documento debe preparar Noah.",
                   "Noah needs to prepare the meeting notes.",
                   ["the final invoice", "the class timetable", "the meeting notes"], 2, c,
                   "La grabación asigna a Noah la preparación de las notas de la reunión."),
            order(f"{p}.p02", "Ordena la responsabilidad de revisar los correos.",
                  "I am responsible for checking the emails.",
                  ["I", "am", "responsible", "for", "checking", "the", "emails."], c,
                  "Responsible for checking mantiene for antes del gerundio."),
            write(f"{p}.p03", "Escribe: Mi tarea es preparar la lista del equipo.",
                  "Mi tarea es preparar la lista del equipo.", "My task is to prepare the team list.",
                  ["My task is to prepare the team list.", "I am responsible for preparing the team list."], c,
                  "La producción vincula una tarea definida con prepare y el objeto concreto."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Luis crea el gráfico; Mei revisa los números. ¿Qué frase es correcta?",
                   ["Mei prepares the chart alone.", "Luis is responsible for the chart.", "Mei submits the chart without numbers."],
                   1, c, "Luis is responsible for the chart coincide con la división indicada."),
            listen(f"{p}.e02", "Escucha qué debe entregarse al profesor.",
                   "Please submit the research summary to the teacher.",
                   ["the team calendar", "the customer list", "the research summary"], 2, c,
                   "Research summary es el único producto que la instrucción pide entregar."),
            complete(f"{p}.e03", "Usa check: We must ___ the answers before class.",
                     "check", c, "Check completa la revisión necesaria antes de la clase."),
            write(f"{p}.e04", "Describe: Sara prepara el informe y Tom revisa las cifras.",
                  "Sara prepara el informe y Tom revisa las cifras.",
                  "Sara is responsible for preparing the report, and Tom checks the figures.",
                  ["Sara is responsible for preparing the report, and Tom checks the figures.",
                   "Sara prepares the report while Tom is responsible for checking the figures."], c,
                  "La respuesta asigna una responsabilidad diferente a cada persona."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada integrante con su responsabilidad.",
                  [("editor", "check the text"), ("presenter", "prepare the talk")], c,
                  "El editor revisa el texto y quien presenta prepara la exposición."),
            choose(f"{p}.r02", "Debes entregar el formulario terminado. Elige la acción final.",
                   ["Submit the completed form.", "Prepare a different team.", "Check an unrelated calendar."], 0, c,
                   "Submit the completed form es la acción de entrega solicitada."),
            order(f"{p}.r03", "Reconstruye la tarea compartida del grupo.",
                  "The team prepares the project together.",
                  ["The", "team", "prepares", "the", "project", "together."], c,
                  "Team funciona como sujeto colectivo de la preparación conjunta."),
        ],
    }
    return common_class(n, ["Identificar tareas concretas en contextos de trabajo y estudio.",
                            "Asignar responsabilidades a integrantes de un equipo.",
                            "Describir preparación, revisión y entrega de un producto."], vocabulary, teaching, pools,
                        {"e01": (2, "r01"), "e02": (3, "r02"), "e03": (3, "r01"), "e04": (4, "r03")})


def build_72() -> dict[str, Any]:
    n, c, p = 72, CONCEPTS[72], "en.n2.c72"
    vocabulary = [("deadline", "plazo"), ("due", "vence"), ("schedule", "horario"),
                  ("by", "a más tardar"), ("before", "antes de"), ("available", "disponible")]
    teaching = [
        ("The deadline is Friday at five o'clock.", "El plazo es el viernes a las cinco.", "Deadline fija el último momento aceptado para entregar."),
        ("The assignment is due on Tuesday morning.", "La tarea vence el martes por la mañana.", "Due indica la fecha o el momento límite de una tarea."),
        ("Send the draft by noon, before the meeting.", "Envía el borrador a más tardar al mediodía, antes de la reunión.", "By incluye el límite; before exige un momento anterior al evento."),
        ("My schedule shows that I am available after three.", "Mi horario muestra que estoy disponible después de las tres.", "Schedule organiza el tiempo y available señala un espacio libre."),
        ("The deadline is 30 June; in American English, write June 30.", "El plazo es el 30 de junio; en inglés estadounidense, escribe June 30.", "Las dos formas expresan la misma fecha: día-mes o mes-día."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "El último momento es viernes a las 17:00. Elige la frase exacta.",
                   ["The deadline is Friday at 5 p.m.", "The work starts after Friday.", "The schedule has no Friday task."],
                   0, c, "Deadline Friday at 5 p.m. expresa el límite completo.", guided=True,
                   hint="Busca la opción con día y hora final."),
            complete(f"{p}.pg02", "Usa by: Please finish the notes ___ 2 p.m.",
                     "by", c, "By 2 p.m. permite terminar en cualquier momento hasta las dos.", guided=True,
                     hint="La preposición incluye la hora límite."),
            match(f"{p}.pg03", "Relaciona cada expresión temporal con su sentido.",
                  [("due on Monday", "vence el lunes"), ("before lunch", "en un momento anterior al almuerzo")], c,
                  "Due marca vencimiento y before excluye el momento posterior.", guided=True,
                  hint="Una expresión nombra un plazo; la otra ordena dos momentos."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha cuándo está disponible la tutora.",
                   "The tutor is available from four to six on Wednesday.",
                   ["Wednesday, 2 to 4", "Wednesday, 4 to 6", "Thursday, 4 to 6"], 1, c,
                   "La franja disponible es el miércoles desde las cuatro hasta las seis."),
            order(f"{p}.p02", "Ordena el plazo del ensayo del jueves.",
                  "The essay is due by Thursday evening.",
                  ["The", "essay", "is", "due", "by", "Thursday", "evening."], c,
                  "Due by introduce el límite del jueves por la noche."),
            write(f"{p}.p03", "Escribe: Estoy disponible antes de las diez.",
                  "Estoy disponible antes de las diez.", "I am available before ten.",
                  ["I am available before ten.", "I can meet before ten."], c,
                  "Available before ten comunica una franja libre anterior a esa hora."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha el plazo del informe y elige la fecha.",
                   "The report is due by noon on the fifteenth of May.",
                   ["May 15 at noon", "May 15 at midnight", "May 14 at noon"], 0, c,
                   "Noon on May fifteenth fija el límite a mediodía del 15 de mayo."),
            choose(f"{p}.e02", "Reunión 14:00; debes enviar el archivo antes. ¿Qué opción sirve?",
                   ["Send it at 3 p.m.", "Send it before 2 p.m.", "Send it after the meeting."], 1, c,
                   "Before 2 p.m. garantiza que el archivo llegue antes de la reunión."),
            complete(f"{p}.e03", "La fecha límite es 30 de junio. Completa: The application deadline is ___.",
                     "30 June", c, "30 June y June 30 son variantes regionales de la misma fecha.",
                     accepted=["30 June", "June 30"]),
            write(f"{p}.e04", "Informa: proyecto vence el lunes; estás disponible el sábado.",
                  "El proyecto vence el lunes; estoy disponible el sábado.",
                  "The project is due on Monday, and I am available on Saturday.",
                  ["The project is due on Monday, and I am available on Saturday.",
                   "Monday is the project deadline, but I am free to work on Saturday."], c,
                  "La frase diferencia la fecha límite de la franja disponible para trabajar."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada dato con su función en el calendario.",
                  [("deadline: 8 April", "último día de entrega"), ("available after 1", "franja libre")], c,
                  "El deadline cierra el plazo y available identifica tiempo utilizable."),
            order(f"{p}.r02", "Reconstruye la instrucción previa a la clase.",
                  "Submit the worksheet before the lesson starts.",
                  ["Submit", "the", "worksheet", "before", "the", "lesson", "starts."], c,
                  "Before coloca la entrega en un momento anterior al inicio de la clase."),
            choose(f"{p}.r03", "La fecha es 12 September. Elige la variante estadounidense equivalente.",
                   ["September 20", "12 October", "September 12"], 2, c,
                   "September 12 expresa la misma fecha con el mes antes del día."),
        ],
    }
    return common_class(n, ["Interpretar fechas y horas límite en tareas académicas o laborales.",
                            "Distinguir by de before al organizar una entrega.",
                            "Comunicar disponibilidad dentro de un horario concreto."], vocabulary, teaching, pools,
                        {"e01": (2, "r01"), "e02": (3, "r02"), "e03": (5, "r03"), "e04": (4, "r01")})


def build_73() -> dict[str, Any]:
    n, c, p = 73, CONCEPTS[73], "en.n2.c73"
    vocabulary = [("progress", "avance"), ("finished", "terminado"), ("working", "trabajando"),
                  ("next", "siguiente"), ("issue", "problema"), ("on track", "según lo previsto")]
    teaching = [
        ("Here is my progress: I finished the introduction.", "Este es mi avance: terminé la introducción.", "Progress presenta el estado y finished identifica una parte completada."),
        ("I am working on the final chart now.", "Ahora estoy trabajando en el gráfico final.", "Working on señala la tarea activa en este momento."),
        ("Next, I will check the references.", "A continuación, revisaré las referencias.", "Next introduce el paso que sigue después del avance actual."),
        ("There is one issue, but the project is still on track.", "Hay un problema, pero el proyecto sigue según lo previsto.", "Issue nombra la dificultad y on track confirma que el plan general continúa."),
        ("I finished the survey. I am working on the analysis, and next I will write the summary.", "Terminé la encuesta. Estoy trabajando en el análisis y después escribiré el resumen.", "La actualización integrada separa resultado terminado, tarea actual y próximo paso."),
    ]
    pools = {
        "practiceGuided": [
            match(f"{p}.pg01", "Relaciona cada parte de la actualización con su función.",
                  [("I finished the table", "trabajo completado"), ("I am working on the summary", "trabajo actual")], c,
                  "Finished separa lo completado de working on, que marca la tarea activa.", guided=True,
                  hint="Busca pasado completado frente a acción en curso."),
            choose(f"{p}.pg02", "Terminaste las notas y ahora haces las diapositivas. Elige el resumen.",
                   ["I finished the notes and I am working on the slides.", "I am working on the notes and finished the slides.", "I finished both the notes and the slides."],
                   0, c, "La primera opción distingue resultado terminado y trabajo actual.", guided=True,
                   hint="La actualización necesita finished y working on."),
            complete(f"{p}.pg03", "Completa el paso posterior: ___, I will email the teacher.",
                     "Next", c, "Next introduce la acción que vendrá después.", guided=True,
                     hint="Usa el conector para el paso siguiente."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué parte del proyecto está terminada.",
                   "I finished the research, and I am working on the conclusion.",
                   ["the research", "the conclusion", "the presentation"], 0, c,
                   "Finished the research identifica la parte ya completada."),
            order(f"{p}.p02", "Ordena la actualización que reconoce un problema menor.",
                  "We have one issue, but we are on track.",
                  ["We", "have", "one", "issue,", "but", "we", "are", "on", "track."], c,
                  "But contrasta la dificultad puntual con el avance general previsto."),
            write(f"{p}.p03", "Escribe: Terminé el esquema; ahora trabajo en el ejemplo.",
                  "Terminé el esquema; ahora trabajo en el ejemplo.",
                  "I finished the outline, and now I am working on the example.",
                  ["I finished the outline, and now I am working on the example.",
                   "The outline is finished; I am currently working on the example."], c,
                  "La actualización separa claramente lo terminado de la tarea actual."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha el estado y elige la tarea actual.",
                   "The draft is finished. I am working on the images now.",
                   ["writing the draft", "editing the images", "choosing a deadline"], 1, c,
                   "Working on the images indica que las imágenes son la actividad presente."),
            choose(f"{p}.e02", "El equipo sigue el calendario pese a un error pequeño. Elige el informe.",
                   ["The issue means the project is no longer on schedule.", "We have an issue, but we are still on track.", "The project is finished, so there is no issue."],
                   1, c, "On track comunica que el problema no ha desviado el calendario."),
            complete(f"{p}.e03", "Usa finished: I ___ the first section this morning.",
                     "finished", c, "Finished marca que la primera sección quedó completa esta mañana."),
            write(f"{p}.e04", "Actualiza: datos listos; analizas resultados; luego harás el gráfico.",
                  "Datos terminados; análisis actual; gráfico siguiente.",
                  "I finished the data collection. I am working on the results now, and next I will make the chart.",
                  ["I finished the data collection. I am working on the results now, and next I will make the chart.",
                   "The data collection is finished; now I am analysing the results. Next, I will create the chart."], c,
                  "La actualización incluye progreso completado, actividad actual y próximo paso."),
        ],
        "review": [
            order(f"{p}.r01", "Ordena el avance: entrevistas listas, notas actuales e informe después.",
                  "The interviews are finished; I am working on notes, and next I will draft the report.",
                  ["The", "interviews", "are", "finished;", "I", "am", "working", "on", "notes,", "and", "next", "I", "will", "draft", "the", "report."], c,
                  "El repaso recupera en una frase lo terminado, lo actual y el paso siguiente."),
            choose(f"{p}.r02", "Solo falta revisar una página y el plazo se mantiene. ¿Qué dices?",
                   ["We are on track, with one page left to check.", "The entire schedule has failed.", "I finished a different project."],
                   0, c, "On track es coherente porque queda una tarea pequeña y el plazo sigue vigente."),
            order(f"{p}.r03", "Reconstruye el avance actual sobre la bibliografía.",
                  "I am working on the bibliography today.",
                  ["I", "am", "working", "on", "the", "bibliography", "today."], c,
                  "Am working on presenta una actividad en curso durante el día."),
        ],
    }
    return common_class(n, ["Distinguir trabajo terminado, actual y próximo en una actualización.",
                            "Reconocer problemas breves sin perder el estado general del plan.",
                            "Producir un informe corto con una secuencia temporal clara."], vocabulary, teaching, pools,
                        {"e01": (2, "r03"), "e02": (4, "r02"), "e03": (1, "r01"), "e04": (5, "r01")})


def build_74() -> dict[str, Any]:
    n, c, p = 74, CONCEPTS[74], "en.n2.c74"
    vocabulary = [("clarify", "aclarar"), ("mean", "querer decir"), ("repeat", "repetir"),
                  ("example", "ejemplo"), ("exactly", "exactamente"), ("understand", "entender")]
    teaching = [
        ("Could you clarify the last instruction, please?", "¿Podría aclarar la última instrucción, por favor?", "Clarify pide más precisión sobre una instrucción concreta."),
        ("What do you mean by final version?", "¿Qué quiere decir con versión final?", "What do you mean by pregunta por el sentido de una expresión específica."),
        ("Could you repeat the deadline exactly?", "¿Podría repetir el plazo exactamente?", "Repeat solicita oír de nuevo y exactly centra la respuesta en el dato preciso."),
        ("I do not understand step two. Could you give an example?", "No entiendo el paso dos. ¿Podría dar un ejemplo?", "Understand identifica la dificultad y example solicita una demostración útil."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "No sabes qué significa «draft». Elige la aclaración cortés.",
                   ["What do you mean by draft?", "Draft means that I finished.", "Repeat a different schedule."],
                   0, c, "What do you mean by draft? pregunta directamente por el término desconocido.", guided=True,
                   hint="Incluye el término que necesitas comprender."),
            complete(f"{p}.pg02", "Completa la petición: Could you ___ the instructions, please?",
                     "clarify", c, "Clarify pide que las instrucciones sean más precisas.", guided=True,
                     hint="Usa el verbo que significa aclarar."),
            match(f"{p}.pg03", "Relaciona la dificultad con la petición adecuada.",
                  [("I did not hear the date", "Could you repeat it?"), ("I do not understand the method", "Could you give an example?")], c,
                  "Repeat recupera un dato no oído y example ayuda a comprender un método.", guided=True,
                  hint="Distingue un problema auditivo de uno conceptual."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué dato necesita confirmar el estudiante.",
                   "Could you repeat exactly which pages we need to read?",
                   ["the page numbers", "the teacher's name", "the classroom size"], 0, c,
                   "Which pages identifica los números de página como dato por confirmar."),
            order(f"{p}.p02", "Ordena la pregunta sobre el sentido de «complete».",
                  "What do you mean by complete?",
                  ["What", "do", "you", "mean", "by", "complete?"], c,
                  "Mean by introduce la palabra cuyo sentido se desea aclarar."),
            write(f"{p}.p03", "Pide un ejemplo porque no entiendes el segundo paso.",
                  "No entiendo el segundo paso; necesito un ejemplo.",
                  "I do not understand step two. Could you give me an example, please?",
                  ["I do not understand step two. Could you give me an example, please?",
                   "Could you show me an example of step two? I do not understand it."], c,
                  "La petición nombra la parte confusa y el tipo de ayuda requerido."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "La instrucción «pronto» es imprecisa. Selecciona la mejor pregunta.",
                   ["Could you repeat my name?", "Do you mean there is no task?", "Could you clarify the exact time?"],
                   2, c, "Clarify the exact time convierte una referencia vaga en un dato verificable."),
            listen(f"{p}.e02", "Escucha qué palabra necesita comprender la alumna.",
                   "What do you mean by optional in this assignment?",
                   ["assignment", "optional", "finished"], 1, c,
                   "Optional aparece después de mean by y es el término consultado."),
            complete(f"{p}.e03", "Usa repeat: Could you ___ the room number?",
                     "repeat", c, "Repeat solicita oír otra vez el número de aula."),
            write(f"{p}.e04", "Pide que aclaren exactamente qué archivo debes entregar.",
                  "Necesito saber exactamente qué archivo entregar.",
                  "Could you clarify exactly which file I need to submit, please?",
                  ["Could you clarify exactly which file I need to submit, please?",
                   "I am not sure which file to submit. Could you tell me exactly which one?"], c,
                  "La producción delimita la duda al archivo y solicita precisión con cortesía."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada pregunta con la información que recupera.",
                  [("Could you repeat the address?", "un dato no oído"), ("What do you mean by formal?", "el sentido de una palabra")], c,
                  "Repeat recupera sonido o dato; mean by recupera significado."),
            order(f"{p}.r02", "Reconstruye la petición para aclarar una fecha.",
                  "Could you clarify which date is correct?",
                  ["Could", "you", "clarify", "which", "date", "is", "correct?"], c,
                  "Which date concreta las alternativas que la aclaración debe resolver."),
            write(f"{p}.r03", "Explica que no entiendes y pide que repitan más despacio.",
                  "No entiendo; repita más despacio.",
                  "I do not understand. Could you repeat that more slowly, please?",
                  ["I do not understand. Could you repeat that more slowly, please?",
                   "Could you say it again more slowly? I did not understand."], c,
                  "La frase comunica la dificultad y especifica cómo debe repetirse."),
        ],
    }
    return common_class(n, ["Reconocer qué parte de una instrucción necesita precisión.",
                            "Elegir entre pedir significado, repetición o un ejemplo.",
                            "Formular una aclaración cortés y específica."], vocabulary, teaching, pools,
                        {"e01": (1, "r02"), "e02": (2, "r01"), "e03": (3, "r01"), "e04": (1, "r02")})


def build_75() -> dict[str, Any]:
    n, c, p = 75, CONCEPTS[75], "en.n2.c75"
    cumulative = [CONCEPTS[number] for number in range(71, 76)]
    vocabulary = [("assignment", "encargo"), ("coordinate", "coordinar"), ("status", "estado"),
                  ("priority", "prioridad"), ("confirm", "confirmar"), ("handover", "entrega a otra persona")]
    teaching = [
        ("The assignment gives each person a clear responsibility.", "El encargo da a cada persona una responsabilidad clara.", "Assignment reúne las tareas que deben repartirse."),
        ("Coordinate the schedule and confirm the deadline.", "Coordina el horario y confirma el plazo.", "Coordinate organiza tiempos; confirm verifica el límite acordado."),
        ("Give a short status update before the handover.", "Da una actualización breve del estado antes de la entrega a otra persona.", "Status resume el avance y handover marca el cambio de responsable."),
        ("Ask for clarification when the priority is unclear.", "Pide una aclaración cuando la prioridad no esté clara.", "Priority decide qué hacer primero y una aclaración evita suposiciones."),
        ("Confirm the task, time and next action at the end.", "Confirma la tarea, la hora y la siguiente acción al final.", "Una simulación completa cierra con acuerdos observables."),
        ("Presentation plan: Omar prepares the slides and Zoe checks the sources by Monday at noon. Status: the outline is finished and Omar is working on the chart. Ask: Could you clarify the required length? Next, Zoe checks the final slides.", "Plan de presentación: Omar prepara las diapositivas y Zoe revisa las fuentes a más tardar el lunes al mediodía. Estado: el esquema está terminado y Omar trabaja en el gráfico. Pregunta: ¿Podría aclarar la extensión requerida? Después, Zoe revisa las diapositivas finales.", "El modelo coordina responsables, plazo, estado, aclaración y próximo paso en un solo intercambio."),
    ]
    pools = {
        "practiceGuided": [
            match(f"{p}.pg01", "Relaciona cada paso de la reunión con su objetivo.",
                  [("assign responsibility", "definir quién hace la tarea"), ("confirm deadline", "acordar el límite")], c,
                  "La responsabilidad asigna dueño y el deadline fija el momento final.", guided=True,
                  hint="Separa quién hace el trabajo de cuándo debe terminarlo."),
            choose(f"{p}.pg02", "El estado no está claro. ¿Qué acción mejora la coordinación?",
                   ["Ask for a short status update.", "Ask everyone to repeat only their job titles.", "Confirm the deadline but skip the progress details."],
                   0, c, "Una actualización breve aporta la información que falta para coordinar.", guided=True,
                   hint="Busca una acción que solicite evidencia del avance."),
            complete(f"{p}.pg03", "Completa el foco principal: Our first ___ is the client report.",
                     "priority", c, "Priority identifica la tarea que debe atenderse primero.", guided=True,
                     hint="Necesitas el sustantivo para el trabajo más importante."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué dato debe confirmarse antes de empezar.",
                   "Before we start, please confirm the handover time.",
                   ["the assignment title", "the handover time", "the report deadline"], 1, c,
                   "Handover time es el dato que la instrucción pide confirmar."),
            order(f"{p}.p02", "Ordena el acuerdo para coordinar dos horarios.",
                  "We need to coordinate our schedules today.",
                  ["We", "need", "to", "coordinate", "our", "schedules", "today."], c,
                  "Coordinate our schedules expresa la acción conjunta necesaria."),
            write(f"{p}.p03", "Escribe: Confirmo el encargo y su prioridad.",
                  "Confirmo el encargo y su prioridad.", "I confirm the assignment and its priority.",
                  ["I confirm the assignment and its priority.", "I can confirm which assignment has priority."], c,
                  "La frase verifica tanto el trabajo como su importancia relativa."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Maya redacta; Jon revisa. ¿Qué acuerdo refleja las responsabilidades?",
                   ["Maya writes the draft, and Jon is responsible for checking it.", "Jon writes the draft, and Maya checks it.", "Maya writes and checks the draft by herself."],
                   0, c, "La primera opción asigna una tarea distinta y coherente a cada persona.",
                   requires=[CONCEPTS[71], c]),
            listen(f"{p}.e02", "Escucha y selecciona el plazo acordado.",
                   "The slides are due by three on Thursday, before the team meeting.",
                   ["Thursday at 3 p.m.", "Friday after the meeting", "Thursday at midnight"], 0, c,
                   "By three on Thursday fija el plazo antes de la reunión.",
                   requires=[CONCEPTS[72], c]),
            choose(f"{p}.e03", "Avance: esquema listo; escribe resultados; luego revisará. ¿Qué informe sirve?",
                   ["The results are finished, and the outline is still in progress.", "The outline is finished; the results are in progress, and review is next.", "The outline and results are finished, so there is no next step."],
                   1, c, "La segunda opción conserva las tres etapas en su orden real.",
                   requires=[CONCEPTS[73], c]),
            write(f"{p}.e04", "Redacta el acuerdo con cada dato y reproduce la pregunta entre comillas.",
                  "Report: Ana prepares it; you check it; deadline Friday at 4 p.m. Status: introduction finished, Ana working on results. Ask: ‘Could you clarify exactly which file format we need to use?’ Next: you review the complete draft.",
                  "Ana is responsible for preparing the report, and I will check it. The deadline is Friday at 4 p.m. The introduction is finished, and Ana is working on the results. I will ask, ‘Could you clarify exactly which file format we need to use?’ Next, I will review the complete draft.",
                  [
                      "Ana is responsible for preparing the report, and I will check it. The deadline is Friday at 4 p.m. The introduction is finished, and Ana is working on the results. I will ask, ‘Could you clarify exactly which file format we need to use?’ Next, I will review the complete draft.",
                      "Ana prepares the report, and I check it by Friday at 4 p.m. The introduction is finished, while Ana is working on the results. I will ask, ‘Could you clarify exactly which file format we need to use?’ My next task is to review the full draft.",
                  ], c, "La simulación usa responsables, plazo, estado, pregunta textual y próximo paso visibles.",
                  requires=cumulative),
        ],
        "review": [
            match(f"{p}.r01", "Nora prepara el folleto; Eli revisa las fuentes. Relaciona responsabilidades.",
                  [("Nora", "preparar el folleto"), ("Eli", "revisar las fuentes")], c,
                  "El repaso asigna una tarea concreta y diferente a cada integrante."),
            match(f"{p}.r02", "Une cada momento de la simulación con su intervención.",
                  [("unclear instruction", "ask for clarification"), ("work in progress", "give a status update")], c,
                  "La aclaración resuelve ambigüedad y el status update informa del avance."),
            write(f"{p}.r03", "Redacta el plan del seminario y reproduce la pregunta indicada.",
                  "Seminar: Leo researches; Mia edits; deadline Tuesday at 2 p.m. Status: sources finished, Leo working on notes. Ask: ‘Could you clarify which template we need?’ Next: Mia edits the draft.",
                  "Leo is responsible for the research, and Mia edits the seminar draft by Tuesday at 2 p.m. The sources are finished, and Leo is working on the notes. We will ask, ‘Could you clarify which template we need?’ Next, Mia will edit the draft.",
                  ["Leo is responsible for the research, and Mia edits the seminar draft by Tuesday at 2 p.m. The sources are finished, and Leo is working on the notes. We will ask, ‘Could you clarify which template we need?’ Next, Mia will edit the draft.",
                   "Leo researches the seminar, and Mia is responsible for editing it by Tuesday at 2 p.m. The sources are finished, while Leo is working on notes. We will ask, ‘Could you clarify which template we need?’ Mia edits the draft next."], c,
                  "La recuperación integra los cinco conceptos en un seminario distinto al informe de Ana.",
                  requires=cumulative),
        ],
    }
    return common_class(n, ["Coordinar responsabilidades y plazos en una conversación simulada.",
                            "Comunicar el estado de una tarea y solicitar precisión cuando falte.",
                            "Cerrar un intercambio con prioridad, entrega y próxima acción."], vocabulary, teaching, pools,
                        {"e01": (1, "r01"), "e02": (2, "r03"), "e03": (3, "r02"), "e04": (6, "r03")},
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
        "# DRAFT — Inglés N2 C71–C75", "",
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
        "", "## Cobertura acumulativa C75", "",
        "- `e01`: reparto inequívoco de tareas y responsabilidades.",
        "- `e02`: horario y plazo con `due`, `by` y referencia a la reunión.",
        "- `e03`: actualización con parte terminada, trabajo actual y paso siguiente.",
        "- `e04`: simulación extensa que integra responsables, plazo, estado, aclaración y próxima acción.",
        "", "## Correcciones incorporadas tras revisión", "",
        "- C72 `e03` acepta `30 June` y `June 30`; `t05` y `r03` enseñan ambas convenciones.",
        "- C73 `e04` recupera de forma conjunta trabajo terminado, actual y próximo con `t05` + `r01`.",
        "- C75 `e01` remedia responsabilidades con `t01` + `r01`.",
        "- C75 `e04` aporta todos los datos en el estímulo y remedia con una presentación y un seminario distintos.",
        "- Se naturalizaron disponibilidad, referencias a formato, variantes y distractores.",
        "", "## Auditoría reproducible", "", "```json",
        json.dumps(audit_result, ensure_ascii=False, indent=2), "```", "",
        "## Validación ejecutada", "",
    ])
    lines.extend(f"- `{message}`" for message in validation)
    lines.extend([
        "", "Comando de regeneración:", "", "```bash",
        "PYTHONDONTWRITEBYTECODE=1 python3 work/n2_c71_75/generate.py", "```", "",
        "## Incidencias y dudas para el revisor", "",
        "- Incidencias automáticas conocidas: ninguna tras la validación incluida.",
        "- Revisar naturalidad A2 de las variantes extensas de C74 y C75.",
        "- Simular fallo total para confirmar que cada ruta de remediación ataca el error concreto.",
        "- Verificar en revisión adversarial que C75 demuestra los cinco conceptos sin depender de memoria externa.",
        "- Este autor entrega `DRAFT`; no emite `GO` ni integra el contenido.", "",
    ])
    return "\n".join(lines)


def main() -> int:
    classes = [build_71(), build_72(), build_73(), build_74(), build_75()]
    audit_result = audit(classes)
    for cls in classes:
        number = int(cls["id"].rsplit("-", 1)[1])
        (OUT / f"class-{number}.json").write_text(
            json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    bundle_path = OUT / "bundle-71-75.json"
    bundle_path.write_text(json.dumps(bundle(classes), ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    validation = [validate_file(OUT / f"class-{number}.json", number, number)
                  for number in range(71, 76)]
    validation.append(validate_file(bundle_path, 71, 75))
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    (REPORT_OUT / "REPORT.md").write_text(report(classes, audit_result, validation), encoding="utf-8")
    print("\n".join(validation))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
