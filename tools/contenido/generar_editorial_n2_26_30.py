#!/usr/bin/env python3
"""Regenera las clases editoriales de Inglés N2 C26-C30."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n2"
SCALE = "client-10-levels-v1"
CONCEPTS = {
    26: "n2-future-arrangements-present-continuous",
    27: "n2-will-instant-decisions",
    28: "n2-will-neutral-predictions",
    29: "n2-future-form-choice",
    30: "n2-group-plan-coordination",
}
PHASES = {26: "input", 27: "form", 28: "comprehension", 29: "production", 30: "transfer"}
TITLES = {
    26: ("Present continuous for arrangements", "Presente continuo para arreglos"),
    27: ("Will for instant decisions", "Will para decisiones instantáneas"),
    28: ("Will for neutral predictions", "Will para predicciones neutrales"),
    29: ("Choose the appropriate future", "Elegir el futuro apropiado"),
    30: ("Coordinate a group plan", "Coordinar un plan grupal"),
}
EXPECTED_INDEX_COUNTS = {0: 7, 1: 7, 2: 6}


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def add_hash(item: dict) -> dict:
    payload = {key: value for key, value in item.items() if key not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return item


def access() -> dict:
    return {"screenReader": True, "highContrast": True, "largeText": True}


def base_item(item_id: str, fmt: str, prompt: str, concept: str, pool: str,
              feedback: str, requires: list[str] | None = None, hint: str | None = None) -> dict:
    origin = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": hint or "Revisa el patrón presentado antes de responder."}
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


def choice(item_id: str, prompt: str, options: list[str], index: int, concept: str,
           pool: str, feedback: str, requires: list[str] | None = None,
           hint: str | None = None) -> dict:
    item = base_item(item_id, "elegir", prompt, concept, pool, feedback, requires, hint)
    item["choices"] = [{"text": value} for value in options]
    item["answer"] = {"index": index}
    return add_hash(item)


def listen(item_id: str, prompt: str, audio: str, options: list[str], index: int,
           concept: str, pool: str, feedback: str, requires: list[str] | None = None,
           hint: str | None = None) -> dict:
    item = base_item(item_id, "escuchar", prompt, concept, pool, feedback, requires, hint)
    item["choices"] = [{"text": value} for value in options]
    item["answer"] = {"index": index}
    item["origin"].update({
        "audio": audio,
        "audioMode": "tts",
        "languageCode": "en",
        "speedOptions": [0.75, 1.0],
        "maxReplays": 3,
        "revealTranscriptAfterAttempt": True,
    })
    return add_hash(item)


def complete(item_id: str, prompt: str, answer: str, concept: str, pool: str,
             feedback: str, requires: list[str] | None = None,
             hint: str | None = None) -> dict:
    item = base_item(item_id, "completar", prompt, concept, pool, feedback, requires, hint)
    item["answer"] = {"text": answer, "accepted": [answer]}
    return add_hash(item)


def order(item_id: str, prompt: str, answer: str, concept: str, pool: str,
          feedback: str, requires: list[str] | None = None,
          hint: str | None = None) -> dict:
    item = base_item(item_id, "ordenar", prompt, concept, pool, feedback, requires, hint)
    item["answer"] = {"text": answer, "tokens": answer.split()}
    return add_hash(item)


def write(item_id: str, prompt: str, stimulus: str, answer: str, concept: str,
          pool: str, feedback: str, requires: list[str] | None = None,
          hint: str | None = None) -> dict:
    item = base_item(item_id, "escribir", prompt, concept, pool, feedback, requires, hint)
    item["answer"] = {"text": answer, "accepted": [answer, answer.rstrip(".")]}
    item["origin"]["text"] = stimulus
    return add_hash(item)


def match(item_id: str, prompt: str, pairs: list[tuple[str, str]], concept: str,
          pool: str, feedback: str, requires: list[str] | None = None,
          hint: str | None = None) -> dict:
    item = base_item(item_id, "relacionar", prompt, concept, pool, feedback, requires, hint)
    values = [[left, {"es": right}] for left, right in pairs]
    item["answer"] = {"pairs": values}
    item["origin"]["pairs"] = values
    return add_hash(item)


def teaching(class_number: int, entries: list[tuple[str, str, str]]) -> list[dict]:
    concept = CONCEPTS[class_number]
    result = []
    for number, (english, spanish, explanation) in enumerate(entries, 1):
        en_words, es_words = english.split(), spanish.split()
        en_mid, es_mid = max(1, len(en_words) // 2), max(1, len(es_words) // 2)
        result.append({
            "id": f"en.n2.class-{class_number:02d}.t{number:02d}",
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


def common_class(number: int, objectives: list[str], vocabulary: list[tuple[str, str]],
                 lessons: list[tuple[str, str, str]], pools: dict,
                 cumulative: list[str] | None = None) -> dict:
    concept = CONCEPTS[number]
    prefix = f"en.n2.c{number:02d}"
    result = {
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
        "qualityPolicy": {
            "chronologyTokens": "enforce",
            "answerReuseAcrossEarlyReserved": "forbid",
            "answerEvidenceReuseAcrossPools": "forbid",
            "agentContract": "editorial-agent.v2",
            "minChoices": 3,
            "maxPromptCharacters": 90,
            "feedbackReuseWithinClass": "forbid",
            "minClassFormats": 4,
        },
        "id": f"en.n2.class-{number:02d}",
        "title": {"en": TITLES[number][0], "es": TITLES[number][1]},
        "objectives": {"es": objectives},
        "concepts": [concept],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n2.class-{number - 1:02d}"],
        "usesVocabulary": [en for en, _ in vocabulary],
        "usesPatterns": [concept],
        "vocabulary": [{"en": en, "es": es} for en, es in vocabulary],
        "teaching": teaching(number, lessons),
        "pools": pools,
        "remediationMap": {
            f"{prefix}.e01": {"reteach": f"en.n2.class-{number:02d}.t01", "review": f"{prefix}.r01"},
            f"{prefix}.e02": {"reteach": f"en.n2.class-{number:02d}.t02", "review": f"{prefix}.r02"},
            f"{prefix}.e03": {"reteach": f"en.n2.class-{number:02d}.t03", "review": f"{prefix}.r03"},
            f"{prefix}.e04": {"reteach": f"en.n2.class-{number:02d}.t04", "review": f"{prefix}.r03"},
        },
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True, "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2, "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if cumulative is not None:
        result["cumulativeEvaluation"] = cumulative
    return result


def build_26() -> dict:
    n, c, p = 26, CONCEPTS[26], "en.n2.c26"
    pools = {
        "practiceGuided": [
            choice(f"{p}.pg01", "Ana tiene una cita acordada. Elige la oración en inglés.",
                   ["Ana is seeing the dentist on Friday.", "Ana will see the dentist right now.", "Ana sees the dentist every Friday."], 0, c, "practiceGuided",
                   "El presente continuo expresa aquí una cita fijada para el viernes.", hint="Busca be + verbo en -ing y una referencia futura concreta."),
            complete(f"{p}.pg02", "Completa el arreglo: We ___ Leo at seven tonight.", "are meeting", c, "practiceGuided",
                     "Are meeting combina sujeto plural, be y -ing para un encuentro acordado.", hint="Con we, la forma de be necesaria es are."),
            order(f"{p}.pg03", "Ordena el vuelo ya reservado para el lunes.", "Maya is flying to Cuenca on Monday.", c, "practiceGuided",
                  "El arreglo conserva Maya + is flying + destino + día.", hint="Coloca is antes de flying y deja on Monday al final."),
        ],
        "practice": [
            write(f"{p}.p01", "Escribe en inglés el encuentro acordado.", "Quedamos con Sara mañana a las ocho.", "We are meeting Sara at eight tomorrow.", c, "practice",
                  "La respuesta usa are meeting porque la hora y la persona ya están acordadas."),
            listen(f"{p}.p02", "Escucha y selecciona el almuerzo ya organizado.", "Tom is having lunch with us on Sunday.",
                   ["Tom has lunch with us every Sunday.", "Tom is having lunch with us on Sunday.", "Tom will have lunch alone now."], 1, c, "practice",
                   "Is having y on Sunday identifican un arreglo futuro concreto."),
            match(f"{p}.p03", "Relaciona cada horario acordado con su significado.",
                  [("tomorrow morning", "mañana por la mañana"), ("on Friday evening", "el viernes por la tarde")], c, "practice",
                  "Las expresiones sitúan arreglos en momentos futuros específicos."),
        ],
        "evaluation": [
            choice(f"{p}.e01", "Los billetes están comprados. Elige el viaje ya fijado.",
                   ["They take the bus at nine every day.", "They'll choose a bus now.", "They are taking the bus at nine tomorrow."], 2, c, "evaluation",
                   "Are taking comunica el plan con billetes y hora ya definidos."),
            complete(f"{p}.e02", "Completa la cita confirmada: Julie ___ a client tomorrow.", "is meeting", c, "evaluation",
                     "Is meeting concuerda con Julie y presenta una cita confirmada."),
            write(f"{p}.e03", "Redacta en inglés la cita del jueves.", "Tengo cita con el dentista el jueves a las diez.", "I am seeing the dentist at ten on Thursday.", c, "evaluation",
                  "Am seeing expresa una cita personal fijada con hora y día."),
            listen(f"{p}.e04", "Escucha y elige la invitación vinculada al plan de esta noche.", "Are you coming to the concert tonight?",
                   ["Are you coming to the concert tonight?", "Do you come to concerts every night?", "Will you decide about the concert now?"], 0, c, "evaluation",
                   "Are you coming pregunta por participación en un arreglo de esta noche."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona dos referencias futuras con su traducción.",
                  [("next Saturday", "el próximo sábado"), ("after work", "después del trabajo")], c, "review",
                  "Las referencias temporales aclaran cuándo ocurre cada arreglo."),
            order(f"{p}.r02", "Ordena el partido de tenis pactado para mañana.", "We are playing tennis with Eva tomorrow.", c, "review",
                  "Are playing presenta una actividad futura acordada con Eva."),
            write(f"{p}.r03", "Escribe en inglés el plan de la cena.", "Ellos cenan con nosotros esta noche.", "They are having dinner with us tonight.", c, "review",
                  "Are having y tonight convierten la cena en un arreglo específico."),
        ],
    }
    return common_class(n,
        ["Reconocer el presente continuo cuando expresa un arreglo futuro confirmado.", "Indicar persona, actividad y momento en planes ya acordados.", "Redactar un arreglo propio con be + verbo en -ing."],
        [("meeting", "encuentro"), ("tonight", "esta noche"), ("tomorrow", "mañana"), ("joining", "uniéndose"), ("Saturday", "sábado"), ("dentist", "dentista")],
        [("I'm meeting Sara at six tomorrow.", "Me encuentro con Sara mañana a las seis.", "El presente continuo puede expresar un arreglo personal ya fijado."),
         ("We're having dinner with Leo tonight.", "Cenamos con Leo esta noche.", "Are having señala una cena organizada, no una decisión del momento."),
         ("She is seeing the dentist on Friday.", "Ella tiene cita con el dentista el viernes.", "Is seeing se interpreta como cita gracias a on Friday."),
         ("They are taking the train on Saturday morning.", "Toman el tren el sábado por la mañana.", "Are taking describe un viaje ya coordinado."),
         ("Are you joining us after work?", "¿Te unes a nosotros después del trabajo?", "La pregunta confirma participación en un plan existente.")], pools)


def build_27() -> dict:
    n, c, p = 27, CONCEPTS[27], "en.n2.c27"
    pools = {
        "practiceGuided": [
            choice(f"{p}.pg01", "Suena el teléfono. Elige la decisión tomada ahora.",
                   ["I answer the phone every morning.", "I'll answer the phone.", "I'm answering a scheduled call tomorrow."], 1, c, "practiceGuided",
                   "I'll answer responde de inmediato a la situación del teléfono.", hint="Busca will cuando la decisión nace en este momento."),
            complete(f"{p}.pg02", "Completa la oferta espontánea: I ___ those bags for you.", "will carry", c, "practiceGuided",
                     "Will carry ofrece ayuda decidida al ver las bolsas.", hint="Después de will se usa carry sin to ni terminación."),
            order(f"{p}.pg03", "Ordena la respuesta inmediata al frío.", "I will close the window now.", c, "practiceGuided",
                  "Will precede al verbo base close en una decisión inmediata.", hint="Empieza con I will y coloca now al final."),
        ],
        "practice": [
            write(f"{p}.p01", "Responde en inglés con una decisión inmediata.", "No hay leche. Iré a comprar un poco.", "There is no milk. I will get some.", c, "practice",
                  "Will get muestra la decisión que surge al notar que falta leche."),
            listen(f"{p}.p02", "Escucha y elige la ayuda ofrecida en ese momento.", "That box is heavy. I'll help you with it.",
                   ["That box was heavy yesterday.", "That box is heavy. I'll help you with it.", "I help with boxes every week."], 1, c, "practice",
                   "I'll help es una oferta espontánea motivada por la caja pesada."),
            match(f"{p}.p03", "Relaciona cada reacción inmediata con su motivo.",
                  [("I'll pay for lunch.", "La cuenta acaba de llegar."), ("I'll open the door.", "Alguien acaba de llamar.")], c, "practice",
                  "Cada uso de will responde a una necesidad presente distinta."),
        ],
        "evaluation": [
            choice(f"{p}.e01", "El vaso se cae. Elige la reacción decidida al instante.",
                   ["I'll catch it!", "I catch falling glasses at work.", "I'm catching it in tomorrow's rehearsal."], 0, c, "evaluation",
                   "I'll catch it expresa una reacción inmediata ante el vaso que cae."),
            complete(f"{p}.e02", "Completa la decisión al oír el timbre: I ___ the door.", "will open", c, "evaluation",
                     "Will open comunica la decisión tomada al escuchar el timbre."),
            write(f"{p}.e03", "Escribe una oferta espontánea en inglés.", "Estas cajas pesan. Te ayudaré con ellas.", "These boxes are heavy. I will help you with them.", c, "evaluation",
                  "I will help funciona como oferta inmediata y them retoma boxes."),
            listen(f"{p}.e04", "Escucha y selecciona la solución decidida ahora.", "We missed the bus. I'll call a taxi.",
                   ["We call a taxi every Friday.", "We're calling our booked taxi tomorrow.", "We missed the bus. I'll call a taxi."], 2, c, "evaluation",
                   "I'll call a taxi es la solución improvisada después de perder el autobús."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona las ofertas inmediatas con la acción.",
                  [("I'll carry it.", "lo llevaré"), ("I'll answer it.", "lo contestaré")], c, "review",
                  "Las contracciones I'll mantienen will y un verbo base."),
            order(f"{p}.r02", "Ordena la decisión de pagar la cuenta ahora.", "I will pay the bill now.", c, "review",
                  "La secuencia correcta es sujeto + will + pay + complemento."),
            write(f"{p}.r03", "Contesta en inglés ante una habitación oscura.", "Está oscuro. Encenderé la luz.", "It is dark. I will turn on the light.", c, "review",
                  "Will turn on expresa una respuesta inmediata a la oscuridad."),
        ],
    }
    return common_class(n,
        ["Distinguir una decisión inmediata de un hábito o un arreglo previo.", "Formar respuestas espontáneas con will + verbo base.", "Ofrecer ayuda por escrito ante una necesidad presente."],
        [("carry", "llevar"), ("answer", "contestar"), ("pay", "pagar"), ("help", "ayudar"), ("open", "abrir"), ("close", "cerrar"), ("get", "conseguir"), ("call", "llamar")],
        [("Those bags look heavy. I'll carry them.", "Esas bolsas parecen pesadas. Yo las llevaré.", "I'll carry expresa una oferta decidida al ver las bolsas."),
         ("The phone is ringing. I'll answer it.", "El teléfono está sonando. Yo contestaré.", "Will presenta la reacción inmediata al sonido."),
         ("We don't have any milk. I'll get some.", "No tenemos leche. Iré a comprar un poco.", "I'll get surge de una carencia detectada ahora."),
         ("It's cold in here. I'll close the window.", "Hace frío aquí. Cerraré la ventana.", "I'll close comunica una solución espontánea."),
         ("I forgot to book a table. I'll call the restaurant now.", "Olvidé reservar mesa. Llamaré al restaurante ahora.", "Now refuerza que la decisión no era un plan previo.")], pools)


def build_28() -> dict:
    n, c, p = 28, CONCEPTS[28], "en.n2.c28"
    pools = {
        "practiceGuided": [
            choice(f"{p}.pg01", "El pronóstico es neutral. Elige la predicción para mañana.",
                   ["It rains at this time every year.", "It is raining outside now.", "It will rain tomorrow afternoon."], 2, c, "practiceGuided",
                   "Will rain presenta un hecho futuro esperado, no un plan personal.", hint="Busca will + verbo base con una referencia futura."),
            complete(f"{p}.pg02", "Completa la predicción: Prices ___ next year.", "will increase", c, "practiceGuided",
                     "Will increase formula una previsión neutral sobre los precios.", hint="Después de will usa increase en forma base."),
            order(f"{p}.pg03", "Ordena la previsión sobre ciudades más cálidas.", "Cities will probably become warmer.", c, "practiceGuided",
                  "Probably se coloca después de will y antes del verbo principal.", hint="Une will probably con become antes de warmer."),
        ],
        "practice": [
            write(f"{p}.p01", "Escribe en inglés una predicción tecnológica.", "Los robots harán más trabajos rutinarios.", "Robots will do more routine jobs.", c, "practice",
                  "Will do expresa una predicción general sobre el trabajo futuro."),
            listen(f"{p}.p02", "Escucha y elige la previsión sobre la población.", "The city population will grow in the next decade.",
                   ["The city population grew last decade.", "The city population grows every spring.", "The city population will grow in the next decade."], 2, c, "practice",
                   "Will grow y next decade sitúan el cambio en el futuro."),
            match(f"{p}.p03", "Relaciona cada marcador con su valor predictivo.",
                  [("probably", "probablemente"), ("in the next decade", "en la próxima década")], c, "practice",
                  "Los marcadores expresan probabilidad y horizonte temporal."),
        ],
        "evaluation": [
            choice(f"{p}.e01", "No es una decisión humana. Elige la predicción climática.",
                   ["Winters will become shorter in this region.", "Winters became shorter here last year.", "Winters are becoming shorter during the current cycle."], 0, c, "evaluation",
                   "Will become presenta una proyección neutral sobre los inviernos."),
            complete(f"{p}.e02", "Completa la previsión: Technology ___ daily life.", "will change", c, "evaluation",
                     "Will change proyecta un cambio futuro sin expresar intención."),
            write(f"{p}.e03", "Redacta en inglés la predicción sobre energía.", "La energía solar será más común.", "Solar energy will become more common.", c, "evaluation",
                  "Will become describe una tendencia futura neutral de la energía solar."),
            listen(f"{p}.e04", "Escucha y selecciona la previsión sobre el transporte.", "Electric buses will reduce city pollution.",
                   ["Electric buses reduced city pollution last year.", "Electric buses will reduce city pollution.", "Electric buses are reducing pollution during today's test."], 1, c, "evaluation",
                   "Will reduce comunica el efecto futuro previsto de los autobuses eléctricos."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona dos expresiones de predicción con su significado.",
                  [("will probably rise", "probablemente subirá"), ("will remain stable", "permanecerá estable")], c, "review",
                  "Ambas expresiones combinan will con una previsión, no con un arreglo."),
            order(f"{p}.r02", "Ordena la predicción sobre el trabajo remoto.", "Remote work will remain common in the future.", c, "review",
                  "Will remain conecta el tema con un estado futuro previsto."),
            write(f"{p}.r03", "Escribe en inglés una previsión demográfica.", "La población aumentará lentamente.", "The population will increase slowly.", c, "review",
                  "Will increase slowly expresa una previsión con modo de cambio."),
        ],
    }
    return common_class(n,
        ["Interpretar will como predicción neutral cuando no existe decisión ni arreglo.", "Usar marcadores de probabilidad y tiempo con previsiones A2.", "Producir por escrito una predicción breve sustentada por un contexto."],
        [("forecast", "pronóstico"), ("probably", "probablemente"), ("population", "población"), ("technology", "tecnología"), ("warmer", "más cálido"), ("increase", "aumentar"), ("future", "futuro"), ("change", "cambiar"), ("robots", "máquinas automatizadas")],
        [("The forecast says it will rain tomorrow.", "El pronóstico dice que lloverá mañana.", "Will rain expresa una previsión meteorológica neutral."),
         ("I think prices will increase next year.", "Creo que los precios aumentarán el próximo año.", "I think introduce una predicción personal sin convertirla en plan."),
         ("Cities will probably become warmer.", "Las ciudades probablemente serán más cálidas.", "Probably matiza el grado de seguridad de la predicción."),
         ("Robots will do more routine jobs.", "Los robots harán más trabajos rutinarios.", "Will do proyecta un cambio tecnológico general."),
         ("Life will change in the next twenty years.", "La vida cambiará en los próximos veinte años.", "El marco temporal amplio favorece la lectura predictiva.")], pools)


def build_29() -> dict:
    n, c, p = 29, CONCEPTS[29], "en.n2.c29"
    pools = {
        "practiceGuided": [
            choice(f"{p}.pg01", "La cita está en el calendario. Elige la forma futura adecuada.",
                   ["I'm meeting Nora at four.", "I'll call Nora now.", "I meet Nora at four every Tuesday."], 0, c, "practiceGuided",
                   "Present continuous es adecuado porque la cita ya figura en el calendario.", hint="Decide primero si existe un arreglo previo o una reacción actual."),
            complete(f"{p}.pg02", "Completa la reacción: The doorbell is ringing. I ___ it.", "will answer", c, "practiceGuided",
                     "Will answer corresponde a una decisión tomada al oír el timbre.", hint="La segunda oración necesita will + verbo base."),
            order(f"{p}.pg03", "Ordena la predicción neutral sobre el partido.", "I think our team will win tonight.", c, "practiceGuided",
                  "I think introduce la predicción y will win expresa el resultado esperado.", hint="Coloca will inmediatamente antes de win."),
        ],
        "practice": [
            write(f"{p}.p01", "Escribe en inglés el viaje ya reservado.", "Tomamos el tren de las ocho y cuarto mañana.", "We are taking the 8:15 train tomorrow.", c, "practice",
                  "Are taking señala un horario reservado, no una decisión espontánea."),
            listen(f"{p}.p02", "Escucha y distingue la oferta inmediata.", "You don't have a pen. I'll lend you mine.",
                   ["You don't have a pen. I'll lend you mine.", "I'm lending Mia my spare pen on Friday.", "I lend you a pen every morning."], 0, c, "practice",
                   "I'll lend responde en el momento a la falta de un bolígrafo."),
            match(f"{p}.p03", "Relaciona cada contexto con la función futura.",
                  [("a fixed schedule", "un arreglo confirmado"), ("a sudden problem", "una decisión inmediata")], c, "practice",
                  "El contexto determina si corresponde presente continuo o will."),
        ],
        "evaluation": [
            choice(f"{p}.e01", "El hotel confirmó la reserva. Elige el futuro apropiado.",
                   ["We stay at that hotel every summer.", "We'll choose a hotel now.", "We're staying at the hotel on Friday."], 2, c, "evaluation",
                   "Are staying expresa la reserva confirmada para el viernes."),
            complete(f"{p}.e02", "Completa la decisión inmediata: I ___ the broken chair.", "will replace", c, "evaluation",
                     "Will replace comunica una solución decidida al descubrir el problema."),
            write(f"{p}.e03", "Redacta en inglés una predicción neutral.", "Creo que el viaje será tranquilo y cómodo.", "I think the journey will be calm and comfortable.", c, "evaluation",
                  "Will be funciona como predicción y une dos cualidades futuras con and."),
            listen(f"{p}.e04", "Escucha y elige la oración que describe un arreglo.", "Mia is presenting the report at ten tomorrow.",
                   ["Mia presents reports every month.", "Mia is presenting the report at ten tomorrow.", "Mia will present it because we just asked."], 1, c, "evaluation",
                   "Is presenting y la hora de mañana identifican un arreglo fijado."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cada forma con su función principal.",
                  [("is visiting on Monday", "arreglo futuro"), ("will probably arrive", "predicción neutral")], c, "review",
                  "La forma verbal y el contexto separan arreglo de predicción."),
            order(f"{p}.r02", "Ordena la solución espontánea al problema de luz.", "I will bring another lamp now.", c, "review",
                  "Will bring sigue al sujeto y expresa una solución inmediata."),
            write(f"{p}.r03", "Escribe el arreglo futuro en inglés.", "Nos reunimos con el guía el sábado.", "We are meeting the guide on Saturday.", c, "review",
                  "Are meeting y on Saturday presentan un encuentro acordado."),
        ],
    }
    pools["evaluation"][2]["answer"]["accepted"] = [
        "I think the journey will be calm and comfortable.",
        "In my opinion, the journey will be comfortable and peaceful.",
    ]
    add_hash(pools["evaluation"][2])
    return common_class(n,
        ["Elegir entre presente continuo de arreglo y will según el contexto.", "Identificar la evidencia contextual que determina cada forma futura.", "Redactar arreglos, decisiones y predicciones sin mezclar sus funciones."],
        [("schedule", "horario"), ("fixed", "fijado"), ("calendar", "calendario"), ("doorbell", "timbre"), ("team", "equipo"), ("lend", "prestar"), ("train", "tren")],
        [("I'm meeting Nora at four; it's in my calendar.", "Me reúno con Nora a las cuatro; está en mi calendario.", "El calendario confirma el arreglo y favorece el presente continuo."),
         ("The doorbell is ringing. I'll open the door.", "Suena el timbre. Abriré la puerta.", "Will expresa la respuesta decidida al oír el timbre."),
         ("I think our team will win.", "Creo que nuestro equipo ganará.", "I think y will presentan una predicción neutral."),
         ("We're taking the 8:15 train tomorrow.", "Tomamos el tren de las ocho y cuarto mañana.", "El horario específico indica un viaje ya organizado."),
         ("No one has a pen. I'll lend you mine.", "Nadie tiene bolígrafo. Te prestaré el mío.", "La oferta nace del problema actual, por eso usa will.")], pools)


def build_30() -> dict:
    n, c, p = 30, CONCEPTS[30], "en.n2.c30"
    c26, c27, c28, c29 = (CONCEPTS[i] for i in range(26, 30))
    pools = {
        "practiceGuided": [
            choice(f"{p}.pg01", "La sala está reservada. Elige el mensaje que confirma el plan.",
                   ["We meet in Room B at ten every Saturday.", "We're meeting in Room B at ten on Saturday.", "We'll reserve Room B for a future event."], 1, c, "practiceGuided",
                   "Present continuous confirma el lugar y la hora ya acordados por el grupo.", hint="Busca una actividad con lugar y horario concretos."),
            complete(f"{p}.pg02", "Completa la oferta: We need drinks. I ___ some.", "will bring", c, "practiceGuided",
                     "Will bring registra una oferta inmediata dentro de la coordinación.", hint="La necesidad aparece ahora; usa will + verbo base."),
            order(f"{p}.pg03", "Ordena la predicción sobre la llegada del grupo.", "I think everyone will arrive before ten.", c, "practiceGuided",
                  "La predicción conserva I think + will arrive + límite temporal.", hint="Coloca will antes de arrive y before ten al final."),
        ],
        "practice": [
            write(f"{p}.p01", "Redacta en inglés el mensaje del plan grupal.", "Nos reunimos en la biblioteca a las diez el sábado.", "We are meeting at the library at ten on Saturday.", c, "practice",
                  "Are meeting comunica a todo el grupo un arreglo con lugar y hora."),
            listen(f"{p}.p02", "Escucha y elige quién se ofrece a llevar sillas.", "We need more chairs. I'll bring two from home.",
                   ["I bring two chairs from home for every meeting.", "I'm bringing two chairs to next month's meeting.", "We need more chairs. I'll bring two from home."], 2, c, "practice",
                   "I'll bring identifica al hablante que se ofrece al detectar la necesidad."),
            match(f"{p}.p03", "Relaciona cada tarea del grupo con su responsable.",
                  [("Maya is booking the room.", "Maya reserva la sala."), ("Leo will send the message.", "Leo enviará el mensaje.")], c, "practice",
                  "Las responsabilidades quedan asociadas con una persona concreta."),
        ],
        "evaluation": [
            choice(f"{p}.e01", "El local está confirmado. Elige el arreglo que coordina al grupo.",
                   ["We're meeting at the community center at six on Friday.", "The center is free, so I'll book it now for Friday.", "We meet at the community center at six every Friday."], 0, c, "evaluation",
                   "Are meeting demuestra el arreglo confirmado y aporta lugar, hora y día.", requires=[c26, c]),
            complete(f"{p}.e02", "Faltan vasos. Completa la decisión: I ___ some now.", "will buy", c, "evaluation",
                     "Will buy demuestra una decisión inmediata ante una necesidad del grupo.", requires=[c27, c]),
            write(f"{p}.e03", "Redacta el mensaje con reunión, tareas, previsión y alternativa.",
                  "La reunión está confirmada en la biblioteca el sábado a las diez. Faltan mapas y Maya se ofrece a llevarlos. Leo enviará el mensaje de confirmación esta noche. Crees que todos llegarán a tiempo. Si llueve, usarán la sala B como local alternativo.",
                  "We're meeting at the library at ten on Saturday. We need maps, so Maya says, 'I'll bring them.' Leo is sending the confirmation message tonight. I think everyone will arrive on time. If it rains, we'll use Room B as our backup venue.", c, "evaluation",
                  "El mensaje combina arreglo, oferta inmediata, predicción, responsables y alternativa.",
                  requires=[c26, c27, c28, c29, c]),
            listen(f"{p}.e04", "Escucha y elige la forma adecuada para el plan ya reservado.", "The room is reserved. We're meeting there at six.",
                   ["The room is available, so I'll reserve it now.", "The room is reserved. We're meeting there at six.", "The room will probably be available at six."], 1, c, "evaluation",
                   "El contexto de reserva exige presente continuo, no decisión ni predicción.", requires=[c29, c]),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cada elemento del plan con su función.",
                  [("backup venue", "local alternativo"), ("confirmation message", "mensaje de confirmación")], c, "review",
                  "Un plan coordinado incluye alternativa y confirmación para el grupo."),
            order(f"{p}.r02", "Ordena la confirmación final enviada al equipo.", "Everyone is meeting outside the station at nine.", c, "review",
                  "Is meeting integra participantes, punto de encuentro y hora confirmada."),
            write(f"{p}.r03", "Redacta una oferta inmediata para el grupo.", "Necesitamos un mapa. Yo traeré uno.", "We need a map. I will bring one.", c, "review",
                  "Will bring responde de inmediato a una necesidad compartida."),
        ],
    }
    pools["evaluation"][2]["answer"]["accepted"] = [
        pools["evaluation"][2]["answer"]["text"],
        "Our group is meeting at the library at ten on Saturday. Maya will bring the maps, and Leo is sending the confirmation tonight. Everyone will probably arrive on time. If it rains, Room B will be our backup venue.",
    ]
    pools["review"][2]["answer"]["accepted"] = [
        "We need a map. I will bring one.",
        "We do not have a map, so I will bring one.",
    ]
    add_hash(pools["evaluation"][2])
    add_hash(pools["review"][2])
    result = common_class(n,
        ["Coordinar un plan grupal con lugar, horario y responsabilidades explícitas.", "Combinar arreglos, decisiones inmediatas y predicciones sin confundir sus funciones.", "Redactar un mensaje de coordinación comprensible para todos los participantes."],
        [("venue", "local"), ("confirm", "confirmar"), ("bring", "traer"), ("message", "mensaje"), ("everyone", "todos"), ("backup", "alternativa"), ("library", "biblioteca")],
        [("We're meeting at the library at ten on Saturday.", "Nos reunimos en la biblioteca a las diez el sábado.", "El presente continuo fija el encuentro principal del grupo."),
         ("We need drinks. I'll bring some.", "Necesitamos bebidas. Yo llevaré algunas.", "Will permite aceptar una responsabilidad en el momento."),
         ("I think everyone will arrive before ten.", "Creo que todos llegarán antes de las diez.", "La predicción ayuda a anticipar la llegada del grupo."),
         ("Maya is sending the confirmation message tonight.", "Maya envía el mensaje de confirmación esta noche.", "Is sending presenta una tarea ya asignada y programada."),
         ("If the park is busy, we'll use the backup venue.", "Si el parque está lleno, usaremos el local alternativo.", "Will presenta la respuesta prevista para una condición posible.")], pools,
        cumulative=[CONCEPTS[i] for i in range(26, 31)])
    result["usesPatterns"] = [CONCEPTS[i] for i in range(26, 31)]
    return result


BUILDERS = {26: build_26, 27: build_27, 28: build_28, 29: build_29, 30: build_30}


def audit(classes: list[dict], *, require_full_block: bool) -> dict:
    deictic = re.compile(r"\b(?:modelo|idea trabajada|frase indicada|contexto nuevo)\b", re.I)
    indices = Counter()
    fingerprints: dict[str, str] = {}
    totals = Counter()
    for cls in classes:
        number = int(cls["id"].rsplit("-", 1)[1])
        assert cls["phase"] == PHASES[number]
        assert any(item["format"] == "escribir" for items in cls["pools"].values() for item in items)
        assert sum(len(items) for items in cls["pools"].values()) == 13
        assert len({item["format"] for items in cls["pools"].values() for item in items}) >= 4
        feedback = []
        for pool, items in cls["pools"].items():
            totals[pool] += len(items)
            for item in items:
                prompt = item["prompt"]["es"]
                assert len(prompt) <= 90 and not deictic.search(prompt), (item["id"], prompt)
                feedback.append(item["origin"]["feedback"]["es"].casefold())
                if item["format"] in {"elegir", "escuchar"}:
                    assert len(item["choices"]) >= 3
                    indices[item["answer"]["index"]] += 1
                payload = {"prompt": item["prompt"], "answer": item["answer"],
                           "stimulus": item["origin"].get("audio") or item["origin"].get("text") or item["origin"].get("pairs")}
                signature = canonical(payload).casefold()
                assert signature not in fingerprints, (item["id"], fingerprints.get(signature))
                fingerprints[signature] = item["id"]
        assert len(feedback) == len(set(feedback)), cls["id"]
    if require_full_block:
        assert indices == Counter(EXPECTED_INDEX_COUNTS), indices
        close = classes[-1]
        expected = {CONCEPTS[i] for i in range(26, 31)}
        assert set(close["cumulativeEvaluation"]) == expected
        assert set(close["usesPatterns"]) == expected
        evidence = {concept for item in close["pools"]["evaluation"] for concept in item["requires"]}
        assert expected <= evidence
        reserved = next(item for item in close["pools"]["evaluation"] if item["format"] == "escribir")
        assert expected <= set(reserved["requires"])
        reserved_text = reserved["answer"]["text"].casefold()
        for marker in ("library", "ten", "maya", "leo", "confirmation", "if it rains", "backup venue"):
            assert marker in reserved_text, (reserved["id"], marker)
    return {"classes": len(classes), "items": sum(totals.values()), "pools": dict(totals),
            "correctIndices": dict(sorted(indices.items())), "fingerprints": len(fingerprints)}


def write_class(number: int) -> Path:
    document = BUILDERS[number]()
    audit([document], require_full_block=False)
    path = OUT / f"class-{number:02d}.json"
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_bundle() -> Path:
    classes = [json.loads((OUT / f"class-{number:02d}.json").read_text(encoding="utf-8")) for number in range(26, 31)]
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
        "range": {"start": 26, "end": 30},
        "classes": classes,
    }
    path = OUT / "bundle-26-30.json"
    path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-number", type=int, choices=range(26, 31))
    parser.add_argument("--bundle", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    if args.class_number is not None:
        print(write_class(args.class_number))
    elif args.bundle:
        print(write_bundle())
    elif args.audit:
        classes = [json.loads((OUT / f"class-{number:02d}.json").read_text(encoding="utf-8")) for number in range(26, 31)]
        print(json.dumps(audit(classes, require_full_block=True), ensure_ascii=False, sort_keys=True))
    else:
        parser.error("choose --class-number, --bundle, or --audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
