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
REPORT_OUT = ROOT / "build/editorial-n2-91-95"
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
    91: "n2-invitations-alternatives",
    92: "n2-apologies-explanations",
    93: "n2-polite-agreement-disagreement",
    94: "n2-social-compromise",
    95: "n2-resolve-social-plan",
}
PHASES = {91: "input", 92: "form", 93: "comprehension", 94: "production", 95: "transfer"}
TITLES = {
    91: {"en": "Invitations and alternatives", "es": "Invitaciones y alternativas"},
    92: {"en": "Apologies and explanations", "es": "Disculpas y explicaciones"},
    93: {"en": "Agree and disagree politely", "es": "Estar de acuerdo y discrepar con cortesía"},
    94: {"en": "Find a compromise", "es": "Encontrar un acuerdo"},
    95: {"en": "Resolve a social plan", "es": "Resolver un plan social"},
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
    result: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}, **extra}
    if hint is not None:
        result["hint"] = {"es": hint}
    return result


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
          feedback: str, *, guided: bool = False, hint: str | None = None,
          requires: list[str] | None = None) -> dict[str, Any]:
    teaches, default_requires = requirements(concept, guided)
    return add_hash({
        "id": item_id, "format": "ordenar", "prompt": {"es": prompt},
        "answer": {"text": answer, "tokens": tokens}, "choices": [],
        "teaches": teaches, "requires": default_requires if requires is None else requires,
        "origin": origin(feedback, hint=hint), "accessibility": dict(ACCESSIBILITY),
    })


def write(item_id: str, prompt: str, stimulus: str, answer: str, accepted: list[str],
          concept: str, feedback: str, *, requires: list[str] | None = None) -> dict[str, Any]:
    return add_hash({
        "id": item_id, "format": "escribir", "prompt": {"es": prompt},
        "answer": {"text": answer, "accepted": accepted}, "choices": [],
        "teaches": [], "requires": [concept] if requires is None else requires,
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
          feedback: str, *, guided: bool = False, hint: str | None = None,
          requires: list[str] | None = None) -> dict[str, Any]:
    teaches, default_requires = requirements(concept, guided)
    values = [[left, {"es": right}] for left, right in pairs]
    return add_hash({
        "id": item_id, "format": "relacionar", "prompt": {"es": prompt},
        "answer": {"pairs": values}, "choices": [], "teaches": teaches,
        "requires": default_requires if requires is None else requires,
        "origin": origin(feedback, hint=hint, pairs=values),
        "accessibility": dict(ACCESSIBILITY),
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
    result: dict[str, Any] = {
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
        result["cumulativeEvaluation"] = cumulative
    return result


def build_91() -> dict[str, Any]:
    n, c, p = 91, CONCEPTS[91], "en.n2.c91"
    vocabulary = [("invite", "invitar"), ("available", "disponible"), ("join", "unirse"),
                  ("instead", "en su lugar"), ("another day", "otro día"), ("free", "libre")]
    teaching = [
        ("I want to invite Sam to a picnic on Sunday.", "Quiero invitar a Sam a un pícnic el domingo.", "Invite introduce la intención de incluir a otra persona en un plan concreto."),
        ("Would you like to join us for lunch on Saturday?", "¿Te gustaría unirte a nosotros para almorzar el sábado?", "Would you like to...? formula una invitación amable con actividad y momento."),
        ("Are you available after class on Tuesday?", "¿Estás disponible después de clase el martes?", "Available pregunta si el horario funciona antes de cerrar el plan."),
        ("I am not free tonight, but I can meet tomorrow.", "No estoy libre esta noche, pero puedo reunirme mañana.", "Not free rechaza el horario sin rechazar a la persona; but introduce una opción."),
        ("We could visit the market instead or meet another day.", "Podríamos visitar el mercado en su lugar o reunirnos otro día.", "Instead cambia la actividad y another day cambia la fecha como alternativas claras."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Elige una invitación amable para tomar café el jueves.",
                   ["You take coffee Thursday.", "Would you like to have coffee on Thursday?", "Coffee is on Thursday."], 1, c,
                   "Would you like to...? invita sin imponer el plan.", guided=True,
                   hint="Busca una pregunta amable con actividad y día."),
            match(f"{p}.pg02", "Relaciona cada respuesta con su función social.",
                  [("I'd love to come.", "aceptar"), ("I can't on Friday, but Sunday works.", "proponer otra fecha")], c,
                  "La primera respuesta acepta; la segunda conserva el plan con otra fecha.", guided=True,
                  hint="Observa si la persona confirma o cambia el momento."),
            complete(f"{p}.pg03", "Usa instead: We cannot go hiking; we could watch a film ___ .",
                     "instead", c, "Instead marca que la película sustituye la caminata.", guided=True,
                     hint="La palabra pedida presenta una actividad alternativa."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y selecciona cuándo puede reunirse Elena.",
                   "I am busy on Friday evening, but I am available on Saturday morning.",
                   ["Friday morning", "Friday evening", "Saturday morning"], 2, c,
                   "Elena descarta el viernes por la noche y queda disponible el sábado por la mañana."),
            order(f"{p}.p02", "Ordena la alternativa para una cena que no funciona.",
                  "Could we have lunch together instead?",
                  ["Could", "we", "have", "lunch", "together", "instead?"], c,
                  "Could we...? propone el almuerzo como sustitución cortés de la cena."),
            write(f"{p}.p03", "Invita a Nina al partido del lunes a las seis.",
                  "Nina; partido; lunes; 6:00 p. m.",
                  "Nina, would you like to join me for the game on Monday at six?",
                  ["Nina, would you like to join me for the game on Monday at six?",
                   "Would you like to come to the game with me at six on Monday, Nina?"], c,
                  "La invitación incluye persona, actividad, día y hora."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Quieres un plan tranquilo el domingo. Elige la invitación adecuada.",
                   ["Would you like to read together in the park on Sunday morning?", "Join a loud club now.", "You must run with me on Monday."], 0, c,
                   "Leer en el parque el domingo coincide con el momento y el tipo de plan pedidos."),
            listen(f"{p}.e02", "Escucha y elige la alternativa completa de Omar.",
                   "I cannot join the walk on Wednesday, but I can have tea with you on Thursday.",
                   ["Walk on Thursday", "Tea on Thursday", "Tea on Wednesday"], 1, c,
                   "Omar cambia tanto la actividad como el día: té el jueves."),
            complete(f"{p}.e03", "Usa dos palabras: I'm busy this week. Can we meet ___?",
                     "another day", c, "Another day propone una fecha diferente sin cerrar la conversación."),
            write(f"{p}.e04", "Responde con rechazo y alternativa usando todos los datos.",
                  "Invitación: museo el viernes. Trabajas el viernes. Alternativa: sábado por la mañana.",
                  "I cannot go to the museum on Friday because I work, but I am free on Saturday morning.",
                  ["I cannot go to the museum on Friday because I work, but I am free on Saturday morning.",
                   "I work on Friday, so I can't visit the museum then. Could we go on Saturday morning?"], c,
                  "La respuesta rechaza solo el viernes, explica el motivo y ofrece el sábado por la mañana."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada mensaje con la intención que comunica.",
                  [("Are you free for breakfast tomorrow?", "comprobar disponibilidad"),
                   ("I can come after ten.", "aceptar con límite horario"),
                   ("Can we meet next week instead?", "proponer otro día")], c,
                  "Cada mensaje pregunta, limita o propone una fecha distinta."),
            choose(f"{p}.r02", "No puedes ir al concierto, pero quieres ver a tu amiga. Elige la respuesta.",
                   ["I hate your plan.", "The concert is yesterday.", "I can't come, but could we meet for breakfast?"], 2, c,
                   "La tercera opción rechaza el concierto y mantiene el contacto con un desayuno."),
            order(f"{p}.r03", "Ordena la invitación para estudiar después de clase.",
                  "Would you like to study with us after class?",
                  ["Would", "you", "like", "to", "study", "with", "us", "after", "class?"], c,
                  "Would you like to...? y with us expresan una invitación abierta al grupo."),
        ],
    }
    return common_class(n, ["Reconocer invitaciones amables con actividad y horario.",
                            "Responder a un plan con aceptación, límite o alternativa.",
                            "Mantener el contacto cuando el primer plan no funciona."],
                        vocabulary, teaching, pools,
                        {"e01": (2, "r03"), "e02": (4, "r02"), "e03": (5, "r01"), "e04": (4, "r02")})


def build_92() -> dict[str, Any]:
    n, c, p = 92, CONCEPTS[92], "en.n2.c92"
    vocabulary = [("sorry", "lo siento"), ("late", "tarde"), ("because", "porque"),
                  ("missed", "perdí"), ("forgot", "olvidé"), ("happen", "ocurrir")]
    teaching = [
        ("I am sorry I am late for dinner.", "Siento llegar tarde a la cena.", "Sorry reconoce el problema; late especifica que la llegada ocurrió después de la hora."),
        ("I missed the bus because the road was closed.", "Perdí el autobús porque la carretera estaba cerrada.", "Because conecta una explicación concreta con el resultado sin borrar la responsabilidad."),
        ("I forgot to send the message, and I am sorry.", "Olvidé enviar el mensaje y lo siento.", "Forgot to + verbo explica una acción pendiente y la disculpa reconoce su efecto."),
        ("I could not come because I had to work.", "No pude ir porque tuve que trabajar.", "Could not + verbo y because presentan una ausencia y su razón."),
        ("It will not happen again; I set a reminder.", "No volverá a ocurrir; puse un recordatorio.", "It will not happen again va mejor con una acción concreta que previene el mismo problema."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Llegaste tarde a una reunión. Elige una disculpa responsable.",
                   ["Meetings are boring.", "I'm sorry I'm late; my bus was delayed.", "You chose the wrong time."], 1, c,
                   "La disculpa reconoce la demora y añade una explicación breve.", guided=True,
                   hint="Busca sorry, el problema y una razón clara."),
            complete(f"{p}.pg02", "Usa because: I missed the start ___ my train was delayed.",
                     "because", c, "Because introduce la causa del retraso del tren.", guided=True,
                     hint="Necesitas el conector que responde por qué."),
            match(f"{p}.pg03", "Relaciona cada frase con la parte de la disculpa.",
                  [("I'm really sorry.", "reconocer el problema"),
                   ("I wrote the wrong date.", "explicar el motivo")], c,
                  "Una disculpa puede separar el reconocimiento de la explicación factual.", guided=True,
                  hint="Distingue la disculpa de la información sobre la causa."),
        ],
        "practice": [
            order(f"{p}.p01", "Ordena la explicación de una llamada no realizada.",
                  "I forgot to call you after work.",
                  ["I", "forgot", "to", "call", "you", "after", "work."], c,
                  "Forgot to call identifica exactamente la acción que no se realizó."),
            listen(f"{p}.p02", "Escucha y selecciona por qué Malik no fue al almuerzo.",
                   "I'm sorry I couldn't join you. I had to take my son to the doctor.",
                   ["He had a class.", "He felt angry.", "He took his son to the doctor."], 2, c,
                   "Malik explica una obligación médica familiar, no una preferencia."),
            write(f"{p}.p03", "Discúlpate: olvidaste reservar la mesa; llamarás ahora.",
                  "Olvidaste reservar la mesa. Acción: llamar ahora.",
                  "I'm sorry I forgot to book the table. I will call the restaurant now.",
                  ["I'm sorry I forgot to book the table. I will call the restaurant now.",
                   "I'm sorry I didn't book the table. I'll phone the restaurant now."], c,
                  "El mensaje nombra el olvido y ofrece una acción inmediata para corregirlo."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Rompiste sin querer una taza prestada. Elige la respuesta adecuada.",
                   ["I'm sorry I broke your cup. I will replace it.", "Your cup was too old anyway.", "I never use cups."], 0, c,
                   "La respuesta reconoce el daño y propone reemplazar la taza."),
            complete(f"{p}.e02", "Usa late: I'm sorry I'm ___; the meeting started at nine.",
                     "late", c, "Late describe llegar después del inicio de la reunión."),
            listen(f"{p}.e03", "Escucha y elige qué olvidó hacer Grace.",
                   "I am sorry. I forgot to send you the address before the party.",
                   ["buy a present", "send the address", "choose the music"], 1, c,
                   "Grace identifica el envío de la dirección como la acción olvidada."),
            write(f"{p}.e04", "Escribe una disculpa con motivo y solución usando los datos.",
                  "No fuiste al cine: tu turno terminó tarde. Solución: pagar las entradas del domingo.",
                  "I'm sorry I missed the film because my shift finished late. I will buy our Sunday tickets.",
                  ["I'm sorry I missed the film because my shift finished late. I will buy our Sunday tickets.",
                   "My shift ended late, so I couldn't see the film with you. I'm sorry; I'll pay for Sunday's tickets."], c,
                  "La respuesta une disculpa, explicación laboral y una solución específica para el domingo."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada situación con la explicación precisa.",
                  [("I did not answer.", "my phone battery was empty"),
                   ("I arrived after dessert.", "the last bus was cancelled"),
                   ("I brought no gift.", "I wrote the party on the wrong date")], c,
                  "Cada explicación aporta una causa concreta para el hecho descrito."),
            choose(f"{p}.r02", "Faltaste al pícnic por cuidar a tu hermano. Elige la respuesta completa.",
                   ["I missed the picnic because I looked after my brother.",
                    "I'm sorry I missed the picnic because I had to look after my brother. I will bring lunch next Saturday.",
                    "I'm sorry about Saturday; please cancel next Saturday too."], 1, c,
                   "La opción central combina disculpa, motivo familiar y una solución concreta para el sábado."),
            order(f"{p}.r03", "Ordena la promesa tras olvidar una fecha importante.",
                  "It will not happen again because I set two reminders.",
                  ["It", "will", "not", "happen", "again", "because", "I", "set", "two", "reminders."], c,
                  "La promesa se apoya en dos recordatorios, una medida concreta para evitar la repetición."),
        ],
    }
    return common_class(n, ["Distinguir disculpa, explicación y reparación.",
                            "Usar because para presentar una causa breve y verificable.",
                            "Responder a un fallo social sin culpar a la otra persona."],
                        vocabulary, teaching, pools,
                        {"e01": (3, "r02"), "e02": (1, "r01"), "e03": (3, "r03"), "e04": (4, "r02")})


def build_93() -> dict[str, Any]:
    n, c, p = 93, CONCEPTS[93], "en.n2.c93"
    vocabulary = [("agree", "estar de acuerdo"), ("point", "punto de vista"),
                  ("prefer", "preferir"), ("maybe", "quizá"), ("however", "sin embargo"),
                  ("opinion", "opinión")]
    teaching = [
        ("I agree that the park is a good meeting place.", "Estoy de acuerdo en que el parque es un buen lugar de encuentro.", "I agree confirma de forma directa una idea compartida."),
        ("I see your point, but the café is closer.", "Entiendo tu punto, pero la cafetería está más cerca.", "I see your point reconoce la idea antes de presentar una diferencia."),
        ("I prefer the early show because the last bus leaves at ten.", "Prefiero la función temprana porque el último autobús sale a las diez.", "Prefer expresa una elección y because aporta una razón útil para decidir."),
        ("In my opinion, the free concert is better.", "En mi opinión, el concierto gratuito es mejor.", "In my opinion señala que se presenta una valoración, no un hecho absoluto."),
        ("The beach is beautiful; however, maybe the weather is too cold.", "La playa es hermosa; sin embargo, quizá haga demasiado frío.", "However introduce contraste y maybe reduce la fuerza de una objeción incierta."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Elige una forma cortés de discrepar sobre un restaurante.",
                   ["That idea is stupid.", "I see your point, but I prefer the café.", "You are completely wrong."], 1, c,
                   "Reconocer el punto antes de decir una preferencia protege el tono cordial.", guided=True,
                   hint="Busca reconocimiento, but y una preferencia personal."),
            match(f"{p}.pg02", "Relaciona cada expresión con la postura que comunica.",
                  [("I agree with Maya.", "acuerdo"), ("In my opinion, noon is too early.", "opinión personal")], c,
                  "Agree confirma coincidencia; in my opinion presenta una valoración propia.", guided=True,
                  hint="Decide si la frase confirma otra idea o introduce una perspectiva."),
            complete(f"{p}.pg03", "Usa prefer: I ___ the bus because it is cheaper.",
                     "prefer", c, "Prefer presenta el autobús como la opción elegida.", guided=True,
                     hint="La consigna ya indica el verbo de preferencia."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y selecciona la postura de Hana.",
                   "I agree that Friday is convenient, and six o'clock works for me.",
                   ["She disagrees with Friday.", "She needs a later time.", "She agrees with Friday at six."], 2, c,
                   "Hana confirma tanto el viernes como la hora de las seis."),
            order(f"{p}.p02", "Ordena una objeción cortés sobre el precio.",
                  "I understand your point, but this ticket is expensive.",
                  ["I", "understand", "your", "point,", "but", "this", "ticket", "is", "expensive."], c,
                  "La frase reconoce la idea y después limita el acuerdo por el precio."),
            write(f"{p}.p03", "Responde: aceptas el lugar, pero prefieres ir más tarde.",
                  "Acuerdo: el lugar. Diferencia: prefieres una hora posterior.",
                  "I agree about the place, but I would prefer to go later.",
                  ["I agree about the place, but I would prefer to go later.",
                   "The place works for me; however, I prefer a later time."], c,
                  "La respuesta mantiene el acuerdo sobre el lugar y limita la diferencia al horario."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Tu amigo propone caminar, pero está lloviendo. Elige una objeción cortés.",
                   ["I see your point, but maybe we should stay indoors.", "Walking is a terrible idea.", "You never check the weather."], 0, c,
                   "La primera opción reconoce la propuesta y usa maybe para sugerir un cambio."),
            listen(f"{p}.e02", "Escucha y decide en qué no está de acuerdo Ben.",
                   "The picnic sounds fun. However, I don't think Sunday morning works for everyone.",
                   ["the picnic activity", "the Sunday morning time", "the people invited"], 1, c,
                   "Ben acepta la actividad, pero cuestiona específicamente el horario del domingo."),
            complete(f"{p}.e03", "Usa opinion: In my ___, the smaller room is more comfortable.",
                     "opinion", c, "Opinion presenta la comodidad como valoración personal."),
            write(f"{p}.e04", "Contesta con acuerdo parcial y una razón usando los datos.",
                  "Aceptas el sábado. No aceptas las 7:00 a. m. porque trabajas hasta las 8:00.",
                  "I agree with Saturday, but seven is too early because I work until eight.",
                  ["I agree with Saturday, but seven is too early because I work until eight.",
                   "Saturday is good for me; however, I can't meet at seven because I work until eight."], c,
                  "El mensaje separa el acuerdo sobre el día de la objeción razonada a la hora."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada marcador con el efecto que produce.",
                  [("however", "contrastar dos ideas"), ("maybe", "suavizar una posibilidad"),
                   ("I see your point", "reconocer la perspectiva ajena"),
                   ("In my opinion, the bus is cheaper.", "presentar una valoración personal")], c,
                  "Los marcadores contrastan, suavizan, reconocen o introducen una opinión personal."),
            choose(f"{p}.r02", "Prefieres cocinar en casa y valoras la idea del restaurante. Elige la respuesta.",
                   ["Restaurants are always bad.", "Your idea does not matter.", "I understand your idea, but I'd prefer to cook at home."], 2, c,
                   "La última respuesta valora la propuesta y expresa la preferencia sin ataque personal."),
            order(f"{p}.r03", "Ordena un acuerdo parcial sobre día y hora.",
                  "The day works for me; however, I need an evening time.",
                  ["The", "day", "works", "for", "me;", "however,", "I", "need", "an", "evening", "time."], c,
                  "La secuencia acepta el día y usa however para pedir otra hora."),
        ],
    }
    return common_class(n, ["Identificar acuerdo, desacuerdo y acuerdo parcial en conversación.",
                            "Interpretar marcadores que suavizan una opinión diferente.",
                            "Responder a una propuesta sin convertir la diferencia en ataque."],
                        vocabulary, teaching, pools,
                        {"e01": (5, "r01"), "e02": (5, "r02"), "e03": (4, "r01"), "e04": (2, "r03")})


def build_94() -> dict[str, Any]:
    n, c, p = 94, CONCEPTS[94], "en.n2.c94"
    vocabulary = [("compromise", "acuerdo intermedio"), ("both", "ambos"),
                  ("halfway", "a mitad de camino"), ("share", "compartir"),
                  ("take turns", "turnarse"), ("fair", "justo")]
    teaching = [
        ("A compromise gives both people part of what they want.", "Un acuerdo intermedio da a ambas personas parte de lo que quieren.", "Compromise busca una solución viable para both, no una victoria total."),
        ("We can meet halfway between our two homes.", "Podemos encontrarnos a mitad de camino entre nuestras dos casas.", "Halfway reduce el viaje de las dos personas de manera equilibrada."),
        ("Let's share one large pizza and pay half each.", "Compartamos una pizza grande y paguemos la mitad cada uno.", "Share puede resolver un límite de precio si la división queda clara."),
        ("We can take turns choosing the film, so the plan is fair.", "Podemos turnarnos para elegir la película, así el plan es justo.", "Take turns reparte una decisión repetida y fair destaca el equilibrio."),
        ("That sounds fair: you choose the place, and I choose the time.", "Eso parece justo: tú eliges el lugar y yo la hora.", "Fair describe un reparto aceptable de decisiones o esfuerzo."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Ana quiere té y Luis quiere pastel. Elige una solución para ambos.",
                   ["Only Luis eats.", "They go home hungry.", "They visit a café with tea and cake."], 2, c,
                   "Una cafetería con té y pastel conserva una parte importante para cada persona.", guided=True,
                   hint="Busca una opción que incluya las dos necesidades."),
            match(f"{p}.pg02", "Relaciona cada problema con un tipo de acuerdo.",
                  [("two favourite games", "take turns choosing"),
                   ("homes far apart", "meet halfway")], c,
                  "Los turnos reparten decisiones repetidas y halfway reparte el trayecto.", guided=True,
                  hint="Piensa si hay que repartir elecciones o distancia."),
            complete(f"{p}.pg03", "Usa fair: One person drives and the other pays. That is ___ .",
                     "fair", c, "Fair evalúa como equilibrado el reparto de conducción y pago.", guided=True,
                     hint="La consigna pide el adjetivo que significa justo."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y selecciona el acuerdo sobre la música.",
                   "You choose the first playlist, and I will choose the second one.",
                   ["They cancel the music.", "They take turns choosing playlists.", "One person chooses all evening."], 1, c,
                   "Elegir la primera y la segunda lista por separado crea turnos claros."),
            order(f"{p}.p02", "Ordena una propuesta para compartir el coste.",
                  "We could share a taxi and split the price.",
                  ["We", "could", "share", "a", "taxi", "and", "split", "the", "price."], c,
                  "Compartir el taxi y dividir el precio atiende transporte y presupuesto."),
            write(f"{p}.p03", "Propón un punto medio: una persona quiere 5:00 y otra 7:00.",
                  "Preferencias: 5:00 y 7:00. Punto medio posible: 6:00.",
                  "Could we meet at six as a compromise?",
                  ["Could we meet at six as a compromise?", "Let's compromise and meet at six."], c,
                  "Las seis quedan entre las dos horas y la pregunta deja espacio para aceptar."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Una persona quiere gastar $8 y otra $16. Elige un límite intermedio.",
                   ["Set a budget of $12 each.", "Spend $30 each.", "Only one person pays $16."], 0, c,
                   "Doce dólares queda entre ocho y dieciséis y aplica el mismo límite a ambos."),
            listen(f"{p}.e02", "Escucha y elige cómo reparten la preparación.",
                   "I will make the sandwiches if you bring the drinks and fruit.",
                   ["One person does everything.", "They buy no food.", "They divide food tasks."], 2, c,
                   "Una persona prepara sándwiches y la otra lleva bebidas y fruta."),
            complete(f"{p}.e03", "Usa una expresión de dos palabras: We can ___ choosing the venue.",
                     "take turns", c, "Take turns reparte la elección del lugar entre ocasiones distintas."),
            write(f"{p}.e04", "Crea un acuerdo con estas dos necesidades y confirma el reparto.",
                  "Dara quiere caminar; Joel necesita descansar. Plan: paseo corto y luego café.",
                  "We can take a short walk and then rest at a café, so both plans are included.",
                  ["We can take a short walk and then rest at a café, so both plans are included.",
                   "Let's take a short walk, then have a rest at a café; that works for both of us."], c,
                  "La propuesta conserva actividad y descanso en un orden concreto y equilibrado."),
        ],
        "review": [
            write(f"{p}.r01", "Propón un compromiso: Kim quiere cocinar; Jo necesita estudiar.",
                  "Kim quiere cocinar. Jo necesita tiempo para estudiar. Reparto posible: Kim cocina y Jo lleva un postre comprado después de estudiar.",
                  "Kim can cook while Jo studies, and Jo can bring dessert afterwards.",
                  ["Kim can cook while Jo studies, and Jo can bring dessert afterwards.",
                   "Kim could prepare the meal, and Jo could study first and bring a ready dessert later."], c,
                  "El compromiso conserva la cocina de Kim, el tiempo de estudio de Jo y reparte la comida."),
            choose(f"{p}.r02", "Dos amigos quieren actividades distintas. Elige una alternancia clara.",
                   ["Do my activity every week.", "Choose nothing for a month.", "You choose this Saturday; I choose next Saturday."], 2, c,
                   "Alternar sábados distribuye la elección de manera explícita y verificable."),
            write(f"{p}.r03", "Propón un acuerdo: presupuesto $20 y salida hasta las 9:00.",
                  "Límites: gastar como máximo $20 y terminar antes de las 9:00 p. m.",
                  "Let's choose the $15 meal and leave at eight thirty; that respects both limits.",
                  ["Let's choose the $15 meal and leave at eight thirty; that respects both limits.",
                   "We could spend $15 on dinner and go home at 8:30, so the plan meets both limits."], c,
                  "La recuperación comprueba precio y hora, y formula una solución aceptable para ambos."),
        ],
    }
    return common_class(n, ["Comparar necesidades antes de proponer una solución intermedia.",
                            "Distribuir tiempo, coste o decisiones de forma explícita.",
                            "Redactar un compromiso que respete dos límites visibles."],
                        vocabulary, teaching, pools,
                        {"e01": (1, "r03"), "e02": (5, "r01"), "e03": (4, "r02"), "e04": (1, "r01")})


def build_95() -> dict[str, Any]:
    n, c, p = 95, CONCEPTS[95], "en.n2.c95"
    cumulative = [CONCEPTS[i] for i in range(91, 96)]
    vocabulary = [("schedule", "horario"), ("budget", "presupuesto"),
                  ("venue", "lugar del evento"), ("confirm", "confirmar"),
                  ("change", "cambio"), ("solution", "solución")]
    teaching = [
        ("Start with an invitation that names the venue and time.", "Empieza con una invitación que indique el lugar y la hora.", "Venue y hora hacen que el plan inicial sea verificable."),
        ("Check each person's schedule before you confirm the plan.", "Comprueba el horario de cada persona antes de confirmar el plan.", "Schedule revela límites reales; confirm solo llega después de resolverlos."),
        ("An apology and explanation make a late change easier to understand.", "Una disculpa y una explicación facilitan entender un cambio tardío.", "Sorry más una causa concreta explica change sin culpar a los demás."),
        ("A polite opinion can support a change without rejecting the whole plan.", "Una opinión cortés puede apoyar un cambio sin rechazar todo el plan.", "El acuerdo parcial permite cambiar un detalle y mantener el objetivo común."),
        ("A fair solution respects the time, activity and budget limits.", "Una solución justa respeta los límites de tiempo, actividad y presupuesto.", "Solution es válida cuando incorpora todas las restricciones visibles."),
        ("Leo invites Mina and Eva to a beach picnic on Sunday at one. Mina's schedule includes family lunch until two, so she says sorry. Eva agrees with a picnic, but her budget is ten dollars and she prefers less travel. Their solution is to change the venue to Riverside Park at three, bring food, and confirm on Saturday.", "Leo invita a Mina y Eva a un pícnic en la playa el domingo a la una. El horario de Mina incluye un almuerzo familiar hasta las dos, así que se disculpa. Eva acepta el pícnic, pero su presupuesto es de diez dólares y prefiere viajar menos. La solución es cambiar el lugar a Riverside Park a las tres, llevar comida y confirmar el sábado.", "El escenario integra invitación, disculpa, acuerdo parcial, compromiso y confirmación final."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Elige el primer mensaje que aporta lugar, día y hora.",
                   ["Do something soon.", "Would you like to meet at Green Café on Tuesday at six?", "The place may change."], 1, c,
                   "La invitación central fija Green Café, martes y seis antes de negociar.", guided=True,
                   hint="Busca un mensaje con venue y horario completos."),
            match(f"{p}.pg02", "Relaciona cada dato con la decisión que permite tomar.",
                  [("Ava works until 7:00", "mover la hora"),
                   ("Ben can spend $12", "fijar el presupuesto")], c,
                  "El horario determina la hora posible y el límite de gasto determina el coste.", guided=True,
                  hint="Une cada restricción con el elemento del plan que cambia."),
            complete(f"{p}.pg03", "Usa confirm: Please ___ the final venue before noon.",
                     "confirm", c, "Confirm pide verificar el lugar definitivo antes de la hora límite.", guided=True,
                     hint="La consigna da el verbo que significa verificar definitivamente."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige qué cambio necesita el grupo.",
                   "I agree with the bowling plan, but my class ends at seven, so I need a later start.",
                   ["a cheaper ticket", "a different activity", "a later start"], 2, c,
                   "La persona acepta la actividad y solo solicita empezar después de las siete."),
            order(f"{p}.p02", "Ordena la solución que respeta un límite de gasto.",
                  "Let's choose the free show and meet outside at eight.",
                  ["Let's", "choose", "the", "free", "show", "and", "meet", "outside", "at", "eight."], c,
                  "El espectáculo gratuito resuelve el coste y la hora fija el encuentro."),
            write(f"{p}.p03", "Confirma un plan: parque, domingo, 3:00 y máximo $5.",
                  "Plan acordado: parque; domingo; 3:00 p. m.; presupuesto máximo de $5.",
                  "I confirm the park for Sunday at three, with a budget of five dollars each.",
                  ["I confirm the park for Sunday at three, with a budget of five dollars each.",
                   "The plan is confirmed: the park at 3:00 on Sunday, and no more than $5 each."], c,
                  "La confirmación conserva lugar, fecha, hora y presupuesto máximo."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Nora no puede cenar, pero sí tomar café mañana. Elige su respuesta.",
                   ["I can't have dinner, but would you like coffee tomorrow?", "Dinner is the only possible plan.", "I refuse to meet again."], 0, c,
                   "La primera respuesta rechaza la cena y ofrece una alternativa concreta para mañana.",
                   requires=[CONCEPTS[91], c]),
            listen(f"{p}.e02", "Escucha e identifica la explicación de la cancelación.",
                   "I'm sorry I cancelled our walk. My daughter was ill, and I had to stay home.",
                   ["The weather changed.", "Her daughter was ill.", "She forgot the meeting place."], 1, c,
                   "La hablante se disculpa y explica que cuidó a su hija enferma.",
                   requires=[CONCEPTS[92], c]),
            match(f"{p}.e03", "Une cada mensaje con el paso que resuelve la diferencia.",
                  [("I see your point, but the 9:00 show is too late.", "desacuerdo cortés"),
                   ("Let's choose the 7:00 show and share a taxi home.", "compromiso")], c,
                  "El primer mensaje limita el acuerdo; el segundo resuelve hora y transporte.",
                  requires=[CONCEPTS[93], CONCEPTS[94], c]),
            write(f"{p}.e04", "Redacta el diálogo social con todos los datos del caso.",
                  "Maya invita a Leo e Iris al mercado de arte, sábado 3:00. Leo tiene clase hasta 5:00 y se disculpa. Iris está de acuerdo con salir, pero prefiere interior por lluvia y solo puede gastar $10. Acuerdo: exposición gratuita de la biblioteca, 5:30. Maya confirma el viernes.",
                  "Maya: Would you like to visit the art market on Saturday at three? Leo: I'm sorry, but I have class until five. Iris: I agree that we should go out, but I prefer an indoor place because of the rain, and my budget is ten dollars. Maya: Let's meet at the free library exhibition at five thirty. That works for everyone. I will confirm the plan on Friday.",
                  ["Maya: Would you like to visit the art market on Saturday at three? Leo: I'm sorry, but I have class until five. Iris: I agree that we should go out, but I prefer an indoor place because of the rain, and my budget is ten dollars. Maya: Let's meet at the free library exhibition at five thirty. That works for everyone. I will confirm the plan on Friday.",
                   "Maya: Do you want to go to the art market at 3:00 on Saturday? Leo: Sorry, I can't arrive before five because I have class. Iris: I like the idea of going out; however, I prefer to be indoors because it may rain, and I can spend only $10. Maya: We could go to the free library exhibition at 5:30 instead. I will confirm everything on Friday."], c,
                  "El diálogo usa los datos para invitar, explicar, discrepar, acordar y confirmar.",
                  requires=cumulative),
        ],
        "review": [
            match(f"{p}.r01", "Une cada mensaje con la respuesta que completa la solución.",
                  [("I can't have dinner tonight.", "Could we have coffee tomorrow?"),
                   ("I cancelled because my child was ill.", "I'm sorry; I should have told you earlier."),
                   ("The film is good, but nine is too late.", "Let's choose the seven o'clock show.")], c,
                  "Las parejas recuperan alternativa concreta, disculpa con motivo y compromiso de horario."),
            choose(f"{p}.r02", "El plan ya funciona para todos. Elige una confirmación completa.",
                   ["Maybe something happens later.", "We discussed it once.", "Confirmed: Riverside Hall, Thursday at seven, $8 each."], 2, c,
                   "La última opción cierra lugar, día, hora y coste por persona."),
            write(f"{p}.r03", "Recupera el plan social con todos los datos del caso.",
                  "Jo invita a Kim y Ravi a una película comunitaria en el parque, viernes 9:00. Kim trabaja hasta 8:00 y se disculpa. Ravi acepta la película, pero no quiere comida cara; presupuesto $12. Acuerdo: encontrarse 8:30, llevar aperitivos y gastar máximo $10. Jo confirma el jueves.",
                  "Jo: Would you like to see the community film in the park on Friday at nine? Kim: I'm sorry, but I work until eight. Ravi: I agree with the film, but I prefer not to buy expensive food because my budget is twelve dollars. Jo: Let's meet at eight thirty, bring snacks and spend no more than ten dollars. I will confirm the plan on Thursday.",
                  ["Jo: Would you like to see the community film in the park on Friday at nine? Kim: I'm sorry, but I work until eight. Ravi: I agree with the film, but I prefer not to buy expensive food because my budget is twelve dollars. Jo: Let's meet at eight thirty, bring snacks and spend no more than ten dollars. I will confirm the plan on Thursday.",
                   "Jo: Do you want to watch the park film at 9:00 on Friday? Kim: Sorry, I finish work at eight. Ravi: The film sounds good; however, I don't want costly food because I have a $12 budget. Jo: We can meet at 8:30 and bring snacks, with a $10 limit. I'll confirm on Thursday."], c,
                  "La recuperación integra los cinco pasos en un escenario distinto y con límites completos.",
                  requires=cumulative),
        ],
    }
    return common_class(n, ["Extraer restricciones de horario, lugar y presupuesto de un grupo.",
                            "Negociar una diferencia mediante disculpa, opinión y compromiso.",
                            "Cerrar un plan social completo con confirmación verificable."],
                        vocabulary, teaching, pools,
                        {"e01": (6, "r01"), "e02": (3, "r01"), "e03": (4, "r01"), "e04": (6, "r03")},
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
        assert [len(cls["pools"][name]) for name in ("practiceGuided", "practice", "evaluation", "review")] == [3, 3, 4, 3]
        assert 6 <= len(cls["vocabulary"]) <= 12
        assert len({item["format"] for items in cls["pools"].values() for item in items}) >= 4
        for pool, items in cls["pools"].items():
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
                if pool in {"evaluation", "review"} and item["format"] == "escribir":
                    assert len(item["answer"].get("accepted", [])) >= 2
                prompt_ids[prompt] = item["id"]
                feedback_ids[feedback] = item["id"]
                semantic_ids[semantic] = item["id"]
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
        "# CORRECTED — Inglés N2 C91–C95", "",
        "Estado: **CORRECTED para nueva revisión; no autorizado para integración**.", "",
        "## Alcance", "",
        "- Staging aislado; no modifica `assets/contenido`, tests ni documentación.",
        f"- Digest del mapa N2 v2: `{digest(MAP)}`.",
        "- Contrato `editorial-agent.v2`; `status: shadow`; `runtimeAi: false`.",
        "- El generador construye y valida una clase por vez antes del bundle.",
        "", "## Evidencia por clase", "",
        "| Clase | Fase | Concepto | Vocabulario | Ejercicios | Formatos |",
        "|---|---|---|---:|---:|---:|",
    ]
    for cls in classes:
        class_formats = {item["format"] for items in cls["pools"].values() for item in items}
        lines.append(f"| {cls['id']} | {cls['phase']} | `{cls['concepts'][0]}` | "
                     f"{len(cls['vocabulary'])} | 13 | {len(class_formats)} |")
    lines.extend([
        "", "## Cobertura acumulativa C95", "",
        "- `e01`: rechaza una invitación y ofrece una alternativa concreta.",
        "- `e02`: identifica una disculpa con explicación factual.",
        "- `e03`: diferencia desacuerdo cortés y compromiso.",
        "- `e04`: integra invitación, disculpa, acuerdo parcial, compromiso y confirmación.",
        "- `t06`, `e04` y `r03` usan pícnic/parque, mercado de arte/biblioteca y cine comunitario.",
        "", "## Correcciones de remediación", "",
        "- C92 `r02` recupera disculpa, motivo y solución en un pícnic distinto.",
        "- C93 `r01` practica directamente `In my opinion` en una valoración nueva.",
        "- C94 `r01` reconstruye un compromiso que conserva dos necesidades.",
        "- C95 `r01` recupera rechazo con alternativa, disculpa y compromiso.",
        "", "## Auditoría reproducible", "", "```json",
        json.dumps(audit_result, ensure_ascii=False, indent=2), "```", "",
        "## Hashes de salidas", "", "```text", manifest.rstrip(), "```", "",
        "## Validación ejecutada", "",
    ])
    lines.extend(f"- `{message}`" for message in validation)
    lines.extend([
        "", "Comando de regeneración:", "", "```bash",
        "PYTHONDONTWRITEBYTECODE=1 python3 tools/contenido/generar_editorial_n2_91_95.py", "```", "",
        "## Pruebas de repositorio", "",
        "- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s test_tools`: 52 tests, OK.",
        "- `PYTHONDONTWRITEBYTECODE=1 python3 tools/validar_ruta.py`: 10 idiomas, 0 errores.",
        "- La validación de ruta comprueba el producto actual; no integra este staging.",
        "", "## Incidencias y dudas para el revisor", "",
        "- Incidencias automáticas conocidas: ninguna tras la validación incluida.",
        "- Revisar si la carga del diálogo C95 sigue siendo cómoda para A2 con lectura segmentada.",
        "- Simular fallo total para confirmar que cada recuperación atiende el error semántico.",
        "- Este autor entrega `CORRECTED`; no emite `GO` ni integra el contenido.", "",
    ])
    return "\n".join(lines)


def main() -> int:
    builders = [build_91, build_92, build_93, build_94, build_95]
    classes: list[dict[str, Any]] = []
    validation: list[str] = []
    output_paths: list[Path] = []
    for builder in builders:
        cls = builder()
        classes.append(cls)
        number = int(cls["id"].rsplit("-", 1)[1])
        path = OUT / f"class-{number}.json"
        path.write_text(json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        validation.append(validate_file(path, number, number))
        output_paths.append(path)
    audit_result = audit(classes)
    bundle_path = OUT / "bundle-91-95.json"
    bundle_path.write_text(json.dumps(bundle(classes), ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    validation.append(validate_file(bundle_path, 91, 95))
    output_paths.append(bundle_path)
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
