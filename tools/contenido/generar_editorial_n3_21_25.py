#!/usr/bin/env python3
"""Generate isolated English N3 C21-C25 editorial candidates."""
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
REPORT_OUT = ROOT / "build/editorial-n3-21-25"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
NUMBERS = range(21, 26)
SCALE = "client-10-levels-v1"
CONCEPTS = {n: f"n3-real-consequences-{n - 20}" for n in NUMBERS}
PHASES = {21: "input", 22: "form", 23: "comprehension", 24: "production", 25: "transfer"}
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


def base(i: str, fmt: str, prompt: str, c: str, pool: str, feedback: str,
         *, requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": hint or "Ubica primero la condición y después su consecuencia."}
    return {
        "id": i, "format": fmt, "prompt": {"es": prompt}, "answer": {}, "choices": [],
        "teaches": [c] if pool == "practiceGuided" else [],
        "requires": [] if pool == "practiceGuided" else list(requires or [c]),
        "origin": origin,
        "accessibility": {"screenReader": True, "highContrast": True, "largeText": True},
    }


def choose(i: str, prompt: str, options: list[str], index: int, c: str, pool: str,
           feedback: str, *, requires: list[str] | None = None,
           hint: str | None = None) -> dict[str, Any]:
    x = base(i, "elegir", prompt, c, pool, feedback, requires=requires, hint=hint)
    x["choices"] = [{"text": value} for value in options]
    x["answer"] = {"index": index}
    return hashed(x)


def listen(i: str, prompt: str, audio: str, options: list[str], index: int, c: str,
           pool: str, feedback: str, *, requires: list[str] | None = None) -> dict[str, Any]:
    x = base(i, "escuchar", prompt, c, pool, feedback, requires=requires)
    x["choices"] = [{"text": value} for value in options]
    x["answer"] = {"index": index}
    x["origin"].update({"audio": audio, "audioMode": "tts", "languageCode": "en",
                        "speedOptions": [0.75, 1.0], "maxReplays": 3,
                        "revealTranscriptAfterAttempt": True})
    return hashed(x)


def fill(i: str, prompt: str, answer: str, accepted: list[str], c: str, pool: str,
         feedback: str, *, requires: list[str] | None = None,
         hint: str | None = None) -> dict[str, Any]:
    x = base(i, "completar", prompt, c, pool, feedback, requires=requires, hint=hint)
    x["answer"] = {"text": answer, "accepted": accepted}
    return hashed(x)


def multi_fill(i: str, prompt: str, sentences: list[str], answers: list[str],
               c: str, pool: str, feedback: str, *, minimum_correct: int,
               requires: list[str] | None = None) -> dict[str, Any]:
    x = base(i, "completar", prompt, c, pool, feedback, requires=requires)
    x["origin"]["sentences"] = sentences
    x["origin"]["scoring"] = {"parts": len(sentences), "minimumCorrect": minimum_correct,
                                "independentAttempt": True}
    joined = " | ".join(answers)
    x["answer"] = {"text": joined, "accepted": [joined],
                   "parts": [{"text": value, "accepted": [value]} for value in answers]}
    return hashed(x)


def order(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str,
          *, requires: list[str] | None = None,
          hint: str | None = None) -> dict[str, Any]:
    x = base(i, "ordenar", prompt, c, pool, feedback, requires=requires, hint=hint)
    x["answer"] = {"text": answer, "tokens": answer.split()}
    return hashed(x)


def write(i: str, prompt: str, stimulus: str, answer: str, alternative: str, c: str,
          pool: str, feedback: str, *, requires: list[str] | None = None,
          scoring: dict[str, Any] | None = None) -> dict[str, Any]:
    x = base(i, "escribir", prompt, c, pool, feedback, requires=requires)
    x["origin"]["text"] = stimulus
    if scoring is not None:
        x["origin"]["scoring"] = scoring
    x["answer"] = {"text": answer, "accepted": [answer, alternative]}
    return hashed(x)


def match(i: str, prompt: str, pairs: list[tuple[str, str]], c: str, pool: str,
          feedback: str, *, requires: list[str] | None = None,
          hint: str | None = None,
          scoring: dict[str, Any] | None = None) -> dict[str, Any]:
    x = base(i, "relacionar", prompt, c, pool, feedback, requires=requires, hint=hint)
    values = [[left, {"es": right}] for left, right in pairs]
    x["answer"] = {"pairs": values}
    x["origin"]["pairs"] = values
    if scoring is not None:
        x["origin"]["scoring"] = scoring
    return hashed(x)


def teaching(n: int, rows: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    out = []
    for idx, (en, es, explanation) in enumerate(rows, 1):
        ew, sw = en.split(), es.split()
        em, sm = max(1, len(ew) // 2), max(1, len(sw) // 2)
        out.append({
            "id": f"en.n3.class-{n:02d}.t{idx:02d}", "en": en, "es": es,
            "explanationEs": explanation,
            "segments": [{"en": " ".join(ew[:em]), "es": " ".join(sw[:sm])},
                         {"en": " ".join(ew[em:]), "es": " ".join(sw[sm:])}],
            "audioText": en, "audioMode": "tts", "languageCode": "en",
            "patternId": CONCEPTS[n],
        })
    return out


def make_class(n: int, objectives: list[str], vocab: list[tuple[str, str]],
               rows: list[tuple[str, str, str]], pools: dict[str, list[dict[str, Any]]],
               remap: dict[str, tuple[str, str]], *, uses: list[str] | None = None,
               cumulative: list[str] | None = None) -> dict[str, Any]:
    spec = json.loads(MAP.read_text(encoding="utf-8"))["classes"][n - 1]
    doc: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 3,
        "cefr": "B1", "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "phase": spec["phase"], "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY), "id": spec["id"], "title": spec["title"],
        "objectives": {"es": objectives}, "concepts": spec["concepts"],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": spec["prerequisites"],
        "usesVocabulary": [en for en, _ in vocab], "usesPatterns": uses or spec["concepts"],
        "vocabulary": [{"en": en, "es": es} for en, es in vocab],
        "teaching": teaching(n, rows), "pools": pools,
        "remediationMap": {k: {"reteach": a, "review": b} for k, (a, b) in remap.items()},
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True,
                          "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2,
                     "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if cumulative is not None:
        doc["cumulativeEvaluation"] = cumulative
    return doc


def build_21() -> dict[str, Any]:
    n, c, p = 21, CONCEPTS[21], "en.n3.c21"
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Elige la condición real con una consecuencia futura.",
                   ["If the bus is late, we will call the hotel.",
                    "The bus was late, so we called the hotel.",
                    "If the bus is late, we usually wait at the stop."], 0, c,
                   "practiceGuided", "If más presente introduce una posibilidad real; will expresa el resultado.",
                   hint="Busca if, presente simple y una consecuencia con will."),
            order(f"{p}.pg02", "Ordena el resultado si la oficina cierra temprano.",
                  "If the office closes early, we will return tomorrow.", c, "practiceGuided",
                  "Closes mantiene presente después de if y will return expresa el resultado.",
                  hint="Después de if no uses will en la condición."),
            match(f"{p}.pg03", "Relaciona cada condición con su resultado lógico.",
                  [("If it rains", "llevaremos paraguas"),
                   ("If the train arrives on time", "llegaremos antes de las ocho")], c,
                  "practiceGuided", "Cada consecuencia responde directamente a una condición probable.",
                  hint="Comprueba que el resultado sea posible y útil."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige qué harán si no encuentran taxi.",
                   "If we cannot find a taxi, we will take the airport bus.",
                   ["They will wait at the taxi rank", "They will take the airport bus",
                    "They will call their accommodation"], 1, c, "practice",
                   "El autobús del aeropuerto es la alternativa explícita si no aparece un taxi."),
            write(f"{p}.p02", "Escribe la consecuencia probable del cierre del museo.",
                  "Condición: el museo cierra a las cinco. Resultado: visitar la plaza.",
                  "If the museum closes at five, we will visit the square.",
                  "We will visit the square if the museum closes at five.", c, "practice",
                  "Las dos variantes conservan la condición real y la visita futura."),
            match(f"{p}.p03", "Une cada problema cotidiano con una respuesta viable.",
                  [("If the card does not work", "pagaremos en efectivo"),
                   ("If the room is ready", "dejaremos las maletas")], c, "practice",
                  "Pagar en efectivo y dejar las maletas son consecuencias prácticas y coherentes."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "El vuelo puede retrasarse. Elige el plan condicional correcto.",
                   ["If the flight is delayed, we will inform the host.",
                    "The flight was delayed, so we informed the host.",
                    "If the flight is delayed, we usually wait for news."], 0, c, "evaluation",
                   "Is delayed presenta la condición y will inform la respuesta futura."),
            listen(f"{p}.e02", "Escucha y selecciona la consecuencia de perder el último tren.",
                   "If we miss the last train, we will stay near the station.",
                   ["They will wait for a later taxi", "They will call the station hotel",
                    "They will stay near the station"], 2, c, "evaluation",
                   "Alojarse cerca de la estación es la consecuencia declarada en el audio."),
            write(f"{p}.e03", "Redacta condición y resultado para una reserva sin confirmar.",
                  "Si la reserva no llega hoy, llamaremos al alojamiento mañana.",
                  "If the booking does not arrive today, we will call the accommodation tomorrow.",
                  "We will call the accommodation tomorrow if the booking does not arrive today.",
                  c, "evaluation", "La reserva pendiente activa una llamada futura con momento explícito."),
            match(f"{p}.e04", "Relaciona cinco condiciones y resultados. Meta: 4 de 5.",
                  [("If the pharmacy closes early", "iremos a la farmacia de la estación"),
                   ("If the lift is out of service", "usaremos las escaleras"),
                   ("If the meeting ends late", "tomaremos el autobús de las nueve"),
                   ("If the café has no tables", "pediremos comida para llevar"),
                   ("If the printer stops", "enviaremos el formulario por correo")], c,
                  "evaluation", "Las cinco consecuencias responden a su condición explícita; cuatro aciertos cumplen la meta.",
                  scoring={"parts": 5, "minimumCorrect": 4, "independentAttempt": True}),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona nuevas condiciones con consecuencias directas.",
                  [("If the ferry is full", "reservaremos el siguiente"),
                   ("If reception is open", "pediremos la llave"),
                   ("If the card reader fails", "pagaremos en efectivo"),
                   ("If the rain gets heavier", "esperaremos bajo techo"),
                   ("If the office confirms today", "imprimiremos el billete")], c, "review",
                  "Las cinco respuestas recuperan la relación entre condición presente y resultado futuro."),
            order(f"{p}.r02", "Ordena el plan si el equipaje llega tarde.",
                  "If the luggage arrives late, we will report it at the desk.", c, "review",
                  "La condición usa presente y el reporte futuro responde al retraso del equipaje."),
            write(f"{p}.r03", "Escribe otra condición real y su solución de transporte.",
                  "Si el metro está cerrado, tomaremos el autobús número 12.",
                  "If the metro is closed, we will take bus number twelve.",
                  "We will take the number twelve bus if the metro is closed.", c, "review",
                  "La recuperación conserva cierre probable y alternativa específica."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-{n:02d}.t01", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-{n:02d}.t01", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-{n:02d}.t05", f"{p}.r03"),
             f"{p}.e04": (f"en.n3.class-{n:02d}.t01", f"{p}.r01")}
    return make_class(n,
        ["Reconocer if más presente como condición real.",
         "Identificar una consecuencia futura con will.",
         "Relacionar problemas cotidianos con respuestas lógicas."],
        [("condition", "condición"), ("result", "resultado"), ("likely", "probable"),
         ("booking", "reserva"), ("delayed", "retrasado"), ("accommodation", "alojamiento"),
         ("report", "informar"), ("alternative", "alternativa")],
        [("A likely condition is: if the train is delayed, we will call the accommodation.",
          "Si el tren se retrasa, llamaremos al alojamiento.",
          "If introduce una condición probable y will presenta el resultado futuro."),
         ("If the booking is confirmed, we will receive an email.",
          "Si se confirma la reserva, recibiremos un correo.",
          "La confirmación probable produce un resultado verificable."),
         ("If the road is busy, we will use an alternative route.",
          "Si la carretera está ocupada, usaremos una ruta alternativa.",
          "Alternative nombra la respuesta práctica a una condición real."),
         ("The flight was delayed yesterday.", "El vuelo se retrasó ayer.",
          "Yesterday convierte delayed en un hecho pasado, no en una condición."),
         ("If the luggage is late, we will report it at the desk.",
          "Si el equipaje llega tarde, lo informaremos en el mostrador.",
          "Report expresa la acción que sigue a la condición del equipaje.")], pools, remap)


def build_22() -> dict[str, Any]:
    n, c, p = 22, CONCEPTS[22], "en.n3.c22"
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Elige el aviso que usa unless como excepción.",
                   ["Unless you confirm today, we will release the room.",
                    "When you confirm today, we released the room.",
                    "If you confirmed yesterday, we kept the room."], 0, c,
                   "practiceGuided", "Unless significa si no y presenta la excepción que evita liberar la habitación.",
                   hint="Sustituye unless por if not para comprobar el sentido."),
            order(f"{p}.pg02", "Ordena el aviso sobre el momento seguro de llegada.",
                  "When the train arrives, we will call the hotel.", c, "practiceGuided",
                  "When presenta un momento futuro esperado, no una duda.",
                  hint="Usa presente después de when y will en la consecuencia."),
            match(f"{p}.pg03", "Relaciona cada conector con su función.",
                  [("if", "condición posible"), ("unless", "condición equivalente a if not"),
                   ("when", "momento futuro esperado")], c, "practiceGuided",
                  "If, unless y when distinguen posibilidad, condición con if not y momento seguro.",
                  hint="Pregunta si el hecho es posible, negativo o esperado."),
        ],
        "practice": [
            write(f"{p}.p01", "Escribe el aviso si el autobús deja de operar.",
                  "Condición posible: el autobús no funciona. Resultado: tomar taxi.",
                  "If the bus is not running, we will take a taxi.",
                  "We will take a taxi if the bus is not running.", c, "practice",
                  "If introduce el problema posible sin cambiar el resultado."),
            listen(f"{p}.p02", "Escucha y elige qué ocurrirá si no pagan antes del viernes.",
                   "Unless you pay by Friday, the booking will be cancelled.",
                   ["The room will remain available", "The hotel will request payment later",
                    "The booking will be cancelled"], 2, c, "practice",
                   "Unless you pay equivale a if you do not pay; la reserva se cancelará."),
            match(f"{p}.p03", "Une cada aviso de viaje con el conector adecuado.",
                  [("___ the gate opens, passengers will board.", "when"),
                   ("___ the weather improves, the boat may leave.", "if"),
                   ("___ you show ID, entry will be refused.", "unless")], c, "practice",
                  "Cada conector conserva la certeza o excepción expresada por el aviso."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "La apertura de recepción es segura a las ocho. Elige el conector.",
                   ["If reception opened at eight", "When reception opens at eight",
                    "Unless reception opens at eight"], 1, c, "evaluation",
                   "When encaja con un horario esperado y mantiene presente en opens."),
            choose(f"{p}.e02", "Sin pasaporte no podrán embarcar. Elige el aviso equivalente.",
                   ["When the gate opens, you will wait without boarding.",
                    "If you bring another document, you will board without a passport.",
                    "Unless you bring your passport, you will not board."], 2, c, "evaluation",
                   "Unless you bring equivale a if you do not bring y conserva la prohibición."),
            listen(f"{p}.e03", "Escucha y decide si la salida es posible o segura.",
                   "If the fog clears, the ferry will leave at noon.",
                   ["Es una posibilidad condicionada", "Es un horario seguro sin condición",
                    "Es una condición equivalente a if not"], 0, c, "evaluation",
                   "If señala que la salida depende de que la niebla desaparezca."),
            multi_fill(f"{p}.e04", "Completa seis avisos con if, unless o when.",
                  ["Una carretera quizá esté helada: ___ the road is icy, we will delay the tour.",
                   "Sin registro se pierde la plaza: ___ you register by Tuesday, you will lose your place.",
                   "La llegada del guía es esperada: ___ the guide arrives, we will start the walk.",
                   "El ascensor podría detenerse: ___ the lift stops, we will use the stairs.",
                   "Sin salir a tiempo habrá cargo: ___ you leave by eleven, the hotel will charge an extra fee.",
                   "La oficina confirmará el traslado: ___ the office confirms it, we will send the pickup time."],
                  ["If", "Unless", "When", "If", "Unless", "When"],
                  c, "evaluation",
                  "Cada respuesta distingue posibilidad, condición con if not o momento esperado.",
                  minimum_correct=5),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona tres avisos nuevos con if, unless o when.",
                  [("___ the office confirms, we will print the ticket.", "when"),
                   ("___ traffic gets worse, we will use the metro.", "if"),
                   ("___ you register, you cannot join the tour.", "unless")], c, "review",
                  "La recuperación separa confirmación segura, condición posible y excepción."),
            order(f"{p}.r02", "Ordena el aviso cuando abra la puerta de embarque.",
                  "When the boarding gate opens, we will join the queue.", c, "review",
                  "When y opens expresan el momento previsto antes de la acción futura."),
            multi_fill(f"{p}.r03", "Recupera seis avisos con if, unless o when.",
                  ["La clínica podría cerrar: ___ the clinic closes, we will use the station pharmacy.",
                   "Sin etiqueta rechazarán la maleta: ___ the bag has a label, the airline will reject it.",
                   "El correo llegará como se espera: ___ the email arrives, we will print the ticket.",
                   "La niebla podría empeorar: ___ the fog gets worse, the boat will be cancelled.",
                   "Sin llamar perderemos la habitación: ___ we call by nine, the hotel will release the room.",
                   "La puerta abrirá según el horario: ___ the gate opens, we will join the queue."],
                  ["If", "Unless", "When", "If", "Unless", "When"],
                  c, "review",
                  "La recuperación aplica dos veces cada conector según el significado.",
                  minimum_correct=5),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-{n:02d}.t03", f"{p}.r02"),
             f"{p}.e02": (f"en.n3.class-{n:02d}.t02", f"{p}.r03"),
             f"{p}.e03": (f"en.n3.class-{n:02d}.t01", f"{p}.r01"),
             f"{p}.e04": (f"en.n3.class-{n:02d}.t06", f"{p}.r03")}
    return make_class(n,
        ["Distinguir if, unless y when por su significado.",
         "Mantener presente simple en la cláusula condicional.",
         "Redactar avisos de viaje con consecuencias claras."],
        [("if", "si"), ("unless", "a menos que"), ("when", "cuando"),
         ("exception", "excepción"), ("confirm", "confirmar"), ("release", "liberar"),
         ("boarding", "embarque"), ("register", "registrarse")],
        [("If the weather changes, we will use the indoor route.",
          "Si cambia el clima, usaremos la ruta interior.",
          "If presenta una condición posible y no una certeza."),
         ("Unless you confirm, the hotel will release the room.",
          "A menos que confirmes, el hotel liberará la habitación.",
          "Unless expresa una condición equivalente a if you do not confirm."),
         ("When boarding starts, we will join the queue.",
          "Cuando empiece el embarque, nos uniremos a la fila.",
          "When presenta un momento futuro esperado."),
         ("If you register today, the office will confirm by email.",
          "Si te registras hoy, la oficina confirmará por correo.",
          "Register y confirm forman una condición y su resultado."),
         ("Unless we call, reception will release our late booking.",
          "Si no llamamos, recepción liberará nuestra reserva tardía.",
          "La excepción conserva presente tras unless y will en el resultado."),
         ("Check all six notices: use if for a possibility, unless for an exception, and when for an expected event.",
          "Revisa los seis avisos: usa if para una posibilidad, unless para una excepción y when para un hecho esperado.",
          "La revisión de seis avisos permite comprobar al menos cinco formas y significados correctos.")], pools, remap)


def build_23() -> dict[str, Any]:
    n, c, p = 23, CONCEPTS[23], "en.n3.c23"
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "La tarifa es reembolsable hasta las 18:00. Elige la decisión segura.",
                   ["Cancel after 18:00 and expect the full refund.",
                    "Keep the booking and request a refund after the stay.",
                    "Cancel before 18:00 to receive a full refund."], 2, c,
                   "practiceGuided", "La decisión usa la hora explícita y no añade condiciones inexistentes.",
                   hint="Localiza primero la hora límite y la consecuencia."),
            match(f"{p}.pg02", "Relaciona cada regla con su consecuencia escrita.",
                  [("If you arrive after 22:00", "debes avisar al hotel"),
                   ("Unless breakfast is pre-booked", "se paga por separado")], c,
                  "practiceGuided", "Las consecuencias proceden directamente de las dos reglas visibles.",
                  hint="No infieras descuentos ni servicios que no aparecen."),
            order(f"{p}.pg03", "Ordena la decisión si la maleta supera veinte kilos.",
                  "If the bag weighs over twenty kilos, we will pay the extra fee.", c,
                  "practiceGuided", "La respuesta conserva el límite y la tarifa adicional.",
                  hint="Coloca la condición de peso antes de la consecuencia."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige qué ocurre si no presentan identificación.",
                   "Unless every guest shows identification, the host will not provide the keys.",
                   ["The host will keep the keys", "The host will provide keys before checking ID",
                    "One guest will collect every key without ID"], 0, c, "practice",
                   "Sin identificación de todos, el anfitrión conserva las llaves."),
            match(f"{p}.p02", "Une cada condición de reserva con la acción permitida.",
                  [("Change requested 48 hours before arrival", "cambiar la fecha sin tarifa"),
                   ("Two guests named on the booking", "mostrar dos identificaciones")], c, "practice",
                  "El cambio y las identificaciones dependen de datos expresos, no de suposiciones."),
            write(f"{p}.p03", "Explica qué harás ante una llegada posterior a medianoche.",
                  "Regla: después de medianoche, llamar al número nocturno para conservar la reserva.",
                  "If we arrive after midnight, we will call the night number to keep the booking.",
                  "We will call the night number to keep the booking if we arrive after midnight.",
                  c, "practice", "Las variantes mantienen hora, llamada y conservación de la reserva."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "El desayuno no está reservado. Según la regla, elige la consecuencia.",
                   ["Breakfast will be included for free at check-in.",
                    "We will pay for breakfast separately.",
                    "The hotel will remove the breakfast fee."], 1, c, "evaluation",
                   "La regla indica pago separado cuando el desayuno no se reserva antes."),
            listen(f"{p}.e02", "Escucha y elige la decisión sobre una maleta de veintitrés kilos.",
                   "Bags up to twenty kilos are free. If a bag is heavier, the traveller will pay fifteen euros.",
                   ["Pay no fee because the difference is small", "Pay five euros for the extra weight",
                    "Pay fifteen euros"], 2, c,
                   "evaluation", "Veintitrés supera el límite de veinte y activa la tarifa de quince euros."),
            write(f"{p}.e03", "Redacta la acción exacta para un check-in a las 23:15.",
                  "Regla visible: si llegas después de 22:00, avisa por mensaje para conservar la habitación.",
                  "Because we will arrive at 23:15, we will message the hotel to keep the room.",
                  "We will message the hotel to keep the room because our arrival is at 23:15.",
                  c, "evaluation", "La decisión conserva la hora, el mensaje y la habitación sin inventar servicios."),
            match(f"{p}.e04", "Lee las cinco condiciones y relaciona cada caso con su decisión.",
                  [("Parking requests sent 24 hours early are accepted; sent 2 days early", "mantener la reserva de estacionamiento"),
                   ("Pool entry ends at 20:00; family wants to enter at 20:30", "usar la piscina otro día"),
                   ("A cot is free for children under two; child is 18 months", "pedir la cuna gratuita"),
                   ("Bike room holds two bikes; group brings three", "buscar espacio para una bicicleta"),
                   ("Shuttle leaves 08:30 without waiting; checkout is 09:00", "no reservar ese traslado")], c, "evaluation",
                  "Cada decisión se deduce de un dato nuevo explícito sin añadir servicios ni documentos."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cinco reglas nuevas con sus decisiones exactas.",
                  [("Cancel by noon", "evitar la penalización"),
                   ("Arrival after 21:00", "llamar a recepción"),
                   ("Dinner not included", "pagar la cena"),
                   ("Bag over 18 kg", "comprar peso adicional"),
                   ("Deposit received", "guardar la confirmación")], c, "review",
                  "La recuperación vuelve a localizar cinco condiciones y cinco consecuencias explícitas."),
            order(f"{p}.r02", "Ordena la acción para una llegada posterior a las 21:30.",
                  "If we arrive after 21:30, we will call reception to keep the room.", c, "review",
                  "La recuperación conserva la hora límite, la llamada y la habitación."),
            write(f"{p}.r03", "Escribe una decisión basada en la política de mascotas.",
                  "Política: sin aviso previo, no se aceptan mascotas. Viaje con perro; aún no avisaste.",
                  "Unless I notify the hotel first, it will not accept my dog, so I will call now.",
                  "I will call the hotel now because it will not accept my dog unless I notify it first.",
                  c, "review", "La decisión combina la excepción escrita con una llamada inmediata."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-{n:02d}.t02", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-{n:02d}.t03", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-{n:02d}.t01", f"{p}.r02"),
             f"{p}.e04": (f"en.n3.class-{n:02d}.t06", f"{p}.r01")}
    return make_class(n,
        ["Localizar condiciones explícitas en una reserva.",
         "Elegir consecuencias sin añadir inferencias.",
         "Resolver cinco decisiones mediante datos visibles."],
        [("refund", "reembolso"), ("deadline", "fecha límite"), ("arrival", "llegada"),
         ("breakfast", "desayuno"), ("deposit", "depósito"), ("receipt", "recibo"),
         ("fee", "tarifa"), ("identification", "identificación")],
        [("If your arrival is after 22:00, message the hotel or it will release the room.",
          "Si tu llegada es después de las 22:00, avisa al hotel o liberará la habitación.",
          "Arrival y la hora límite determinan la acción exacta."),
         ("Unless breakfast is pre-booked, you will pay for it separately.",
          "Si el desayuno no se reserva antes, se paga por separado.",
          "La ausencia de breakfast reservado activa un pago separado."),
         ("Bags up to twenty kilos are free; heavier bags have a fee.",
          "Las maletas de hasta veinte kilos son gratis; las más pesadas tienen tarifa.",
          "Fee depende del peso escrito y no de una estimación."),
         ("When the deposit arrives, the office will email the receipt.",
          "Cuando llegue el depósito, la oficina enviará el recibo.",
          "Deposit confirmado produce un receipt verificable."),
         ("Every guest must show identification before receiving a key.",
          "Cada huésped debe mostrar identificación antes de recibir una llave.",
          "Identification es un requisito explícito y no opcional."),
         ("Read each condition, locate its deadline or limit, and choose only the stated consequence.",
          "Lee cada condición, localiza su fecha límite o límite y elige solo la consecuencia escrita.",
          "Este procedimiento evita inferencias en las cinco decisiones.")], pools, remap)


def build_24() -> dict[str, Any]:
    n, c, p = 24, CONCEPTS[24], "en.n3.c24"
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Elige un plan A/B con dos problemas y dos respuestas.",
                   ["If it rains, we will visit the museum; if buses stop, we will take the metro.",
                    "If it rains, we will visit the museum; the buses may also stop.",
                    "We will check the weather and the buses before deciding."], 0, c,
                   "practiceGuided", "El plan contiene dos condiciones reales y una respuesta viable para cada una.",
                   hint="Cuenta dos problemas y dos acciones diferentes."),
            order(f"{p}.pg02", "Ordena la primera contingencia por mal tiempo.",
                  "If the beach closes, we will use the indoor pool.", c, "practiceGuided",
                  "El cierre activa una alternativa interior concreta.",
                  hint="Mantén presente tras if y will en la acción."),
            match(f"{p}.pg03", "Relaciona cada riesgo con su alternativa.",
                  [("Heavy rain", "visitar el museo"),
                   ("Train cancellation", "tomar el autobús directo")], c,
                  "practiceGuided", "Cada alternativa responde al riesgo sin depender de datos nuevos.",
                  hint="Elige acciones que todavía permitan realizar la salida."),
        ],
        "practice": [
            write(f"{p}.p01", "Escribe dos contingencias para una excursión al lago.",
                  "Problema 1: lluvia; alternativa: centro natural. Problema 2: tren cancelado; alternativa: bus 8:10.",
                  "If it rains, we will visit the nature centre. If the train is cancelled, we will take the 8:10 bus.",
                  "We will visit the nature centre if it rains, and we will take the 8:10 bus if the train is cancelled.",
                  c, "practice", "Las variantes conservan los dos riesgos y sus dos soluciones."),
            listen(f"{p}.p02", "Escucha y elige el plan si el sendero está cerrado.",
                   "If the forest path is closed, we will follow the marked river route.",
                   ["Wait beside the closed path", "Use an unmarked forest route",
                    "Follow the marked river route"], 2, c, "practice",
                   "La ruta marcada mantiene la salida sin usar el sendero cerrado."),
            match(f"{p}.p03", "Une cada fase del plan con su función.",
                  [("Check the forecast", "verificar el riesgo"),
                   ("Book the backup bus", "preparar la alternativa"),
                   ("Message the group", "comunicar la decisión")], c, "practice",
                  "Verificación, alternativa y comunicación forman una secuencia completa."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "La carretera puede inundarse. Elige la alternativa viable.",
                   ["If the road floods, we will park near the closed road.",
                    "If the road floods, we will use the hill route.",
                    "The hill route was unavailable yesterday."], 1, c, "evaluation",
                   "La ruta alta evita la carretera inundada y conserva el viaje."),
            listen(f"{p}.e02", "Escucha y selecciona la segunda contingencia del grupo.",
                   "If the rain becomes heavy, we will move indoors. If the last bus is cancelled, we will share two taxis.",
                   ["Move indoors", "Share two taxis", "Wait for a bus tomorrow"], 1, c,
                   "evaluation", "La segunda condición es la cancelación del último bus y la respuesta son dos taxis."),
            write(f"{p}.e03", "Redacta dos respuestas para lluvia y cierre del funicular.",
                  "Lluvia: galería cubierta. Funicular cerrado: autobús de montaña 9:30.",
                  "If it rains, we will use the covered gallery. If the funicular closes, we will take the 9:30 mountain bus.",
                  "We will use the covered gallery if it rains, and take the 9:30 mountain bus if the funicular closes.",
                  c, "evaluation", "La respuesta conserva dos condiciones, dos alternativas y la hora del bus."),
            write(f"{p}.e04", "Escribe 60–80 palabras para el plan A/B de la salida costera.",
                  "Salida sábado. Riesgo 1: lluvia fuerte; alternativa: acuario 10:00. Riesgo 2: tren cancelado; alternativa: bus 9:15. Revisar clima 7:00, confirmar transporte 7:30, avisar grupo 7:45. Llevar comida salvo que café confirme apertura.",
                  "Our coastal trip is on Saturday. If the rain is heavy, we will visit the aquarium at ten. If the train is cancelled, we will take the 9:15 bus. We will check the forecast at seven and confirm transport at 7:30. At 7:45, we will message the group. Unless the café confirms that it is open, everyone will bring lunch.",
                  "On Saturday, we will check the coastal forecast at seven. If heavy rain starts, the group will meet at the aquarium at ten. If our train is cancelled, we will use the 9:15 bus instead. We will confirm the service at 7:30 and update everyone fifteen minutes later. Everyone will pack lunch unless the café confirms that it will open.",
                  c, "evaluation", "El plan integra dos riesgos, respuestas viables, horas y comunicación ordenada."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona riesgos de una visita rural con alternativas.",
                  [("Bridge closed", "usar la carretera norte"),
                   ("Storm warning", "trasladar la actividad al centro comunitario")], c, "review",
                  "Las alternativas permiten continuar sin cruzar el puente ni permanecer fuera."),
            order(f"{p}.r02", "Ordena la comunicación después de comprobar el transporte.",
                  "When we confirm the minibus, we will send the final meeting point.", c, "review",
                  "La confirmación ocurre antes de comunicar el punto de encuentro."),
            write(f"{p}.r03", "Escribe 60–80 palabras para el plan de una visita al valle.",
                  "Visita domingo. Riesgo 1: niebla; alternativa: museo local 11:00. Riesgo 2: autobús lleno; alternativa: dos taxis 10:20. Revisar visibilidad 8:00, llamar bus 8:15, informar grupo 8:30. Llevar agua salvo que centro la venda.",
                  "Our valley visit is on Sunday. If the fog is thick, we will meet at the local museum at eleven. If the bus is full, we will book two taxis for 10:20. We will check visibility at eight and call the bus company at 8:15. At 8:30, we will update the group. Everyone will carry water unless the visitor centre confirms that it sells drinks.",
                  "On Sunday, we will check the valley visibility at eight. If fog covers the road, the group will visit the local museum at eleven. If there are no bus seats, two taxis will collect us at 10:20. We will call the company at 8:15 and message everyone at 8:30. We will bring water unless the visitor centre confirms that drinks are available.",
                  c, "review", "La recuperación mantiene riesgos nuevos, secuencia horaria y dos soluciones completas."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-{n:02d}.t02", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-{n:02d}.t06", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-{n:02d}.t06", f"{p}.r03"),
             f"{p}.e04": (f"en.n3.class-{n:02d}.t06", f"{p}.r03")}
    return make_class(n,
        ["Proponer respuestas para dos problemas probables.",
         "Ordenar verificación, decisión y comunicación.",
         "Redactar un plan A/B de 60–80 palabras."],
        [("contingency", "contingencia"), ("forecast", "pronóstico"),
         ("backup", "alternativa"), ("flood", "inundarse"), ("cancelled", "cancelado"),
         ("confirm", "confirmar"), ("update", "avisar"), ("route", "ruta")],
        [("A contingency gives a practical response to a likely problem.",
          "Una contingencia da una respuesta práctica a un problema probable.",
          "Contingency conecta riesgo real y acción viable."),
         ("If the road floods, our backup will be the hill route.",
          "Si se inunda la carretera, la alternativa será la ruta alta.",
          "Flood activa un backup que todavía permite viajar."),
         ("Check the forecast before choosing the outdoor route.",
          "Revisa el pronóstico antes de elegir la ruta exterior.",
          "Forecast aporta datos antes de tomar la decisión."),
         ("When transport is confirmed, update the group.",
          "Cuando se confirme el transporte, avisa al grupo.",
          "Confirm precede a update en la secuencia del plan."),
         ("If the train is cancelled, use the bus route instead.",
          "Si se cancela el tren, usa la ruta de autobús.",
          "Cancelled activa una route alternativa concreta."),
         ("Plan A: continue if conditions are safe. Plan B: use the backup if they change.",
          "Plan A: continúa si es seguro. Plan B: usa la alternativa si cambia.",
          "El modelo integra dos condiciones, respuestas y orden de comunicación.")], pools, remap)


def build_25() -> dict[str, Any]:
    n, c, p = 25, CONCEPTS[25], "en.n3.c25"
    all_c = [CONCEPTS[x] for x in NUMBERS]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Elige una decisión que usa condición, dato y alternativa.",
                   ["The ferry company may offer another service.",
                    "If the 16:00 ferry is cancelled, we will take the 17:30 service.",
                    "We will wait without checking the next departure."], 1, c,
                   "practiceGuided", "La respuesta comprueba un servicio concreto y propone una alternativa fechada.",
                   hint="Busca condición real, consecuencia y dato verificable."),
            order(f"{p}.pg02", "Ordena el mensaje cuando se confirme la conexión.",
                  "When the connection is confirmed, I will send you the new arrival time.", c,
                  "practiceGuided", "When marca la confirmación esperada antes del mensaje futuro.",
                  hint="Primero va la condición segura; después, la comunicación."),
            match(f"{p}.pg03", "Relaciona cada problema del viaje con una acción práctica.",
                  [("Connection under thirty minutes", "pedir cambio de tren"),
                   ("Hotel arrival after 23:00", "avisar para conservar habitación")], c,
                  "practiceGuided", "Cada acción responde a un límite explícito de conexión o llegada.",
                  hint="No elijas una acción que ignore la hora límite."),
        ],
        "practice": [
            write(f"{p}.p01", "Escribe la decisión y el mensaje tras un retraso del ferry.",
                  "Ferry 15:00 retrasado; conexión 16:10. Si llega después de 15:50, tomar ferry 17:00. Avisa a Eva.",
                  "If the ferry arrives after 15:50, we will take the 17:00 service. Eva, I will confirm the new arrival time.",
                  "We will take the 17:00 ferry if this service arrives after 15:50, and I will update Eva.",
                  c, "practice", "Las variantes conservan límite, alternativa y aviso al acompañante."),
            listen(f"{p}.p02", "Escucha y elige cómo conservarán la habitación.",
                   "Unless we message the hotel before eleven, it will release our room.",
                   ["Message the hotel at 11:30", "Arrive before eleven without sending a message",
                    "Message the hotel before eleven"], 2, c, "practice",
                   "El mensaje antes de las once evita que el hotel libere la habitación."),
            match(f"{p}.p03", "Une cada dato comprobado con la decisión correspondiente.",
                  [("Train 40 minutes late", "usar la conexión de las 18:20"),
                   ("Room held until 22:30", "avisar si la llegada será posterior")], c, "practice",
                  "Las decisiones se apoyan en el retraso y en la hora límite de la habitación."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "La conexión exige 35 minutos y solo hay 20. Elige la decisión.",
                   ["Try the short connection without changing the booking.",
                    "Ask to move to the later connection.",
                    "Change the hotel booking instead of the train."], 1, c, "evaluation",
                   "Veinte minutos no cumplen el mínimo de treinta y cinco; cambiar conexión es viable."),
            listen(f"{p}.e02", "Escucha y selecciona la regla de alojamiento aplicable.",
                   "If guests arrive after midnight, they must call the night desk to keep the room.",
                   ["Message reception only before an early arrival",
                    "Wait until morning without contacting the hotel",
                    "Call the night desk after a midnight arrival"], 2, c, "evaluation",
                   "La llegada posterior a medianoche activa la llamada al mostrador nocturno."),
            write(f"{p}.e03", "Redacta una decisión breve con unless y avisa al acompañante.",
                  "Sin confirmación del tren antes de las 17:00, tomar bus 17:20. Avisa a Noor.",
                  "Unless the train is confirmed before five, we will take the 5:20 bus. Noor, I will update you at five.",
                  "We will take the 5:20 bus unless the train is confirmed before five, and I will message Noor then.",
                  c, "evaluation", "La excepción, alternativa y comunicación conservan las horas dadas."),
            write(f"{p}.e04", "Escribe 70–100 palabras para resolver el viaje de tren y hotel.",
                  "Tren llega 18:25; conexión sale 18:40 y exige 25 min. Alternativa 19:10. Hotel conserva habitación hasta 21:00 salvo aviso; nueva llegada 21:35. Billete permite un cambio gratis. Decide, justifica y escribe a Maya.",
                  "If our train arrives at 18:25, the 18:40 connection is impossible because we need twenty-five minutes. We will take the 19:10 train, using the free change on our ticket. Unless we contact the hotel before 21:00, it will release our room. Our new arrival is 21:35, so I will message the hotel now. Maya, I have changed our connection and protected the room. I will send the confirmed platform when it appears.",
                  "If our train reaches the station at 18:25, we cannot catch the 18:40 service because the connection needs twenty-five minutes. We will use our free change for the 19:10 train. The hotel keeps the room until 21:00 unless we warn them, and we now arrive at 21:35. I will call the hotel immediately. Maya, the later train and room are arranged. When the platform is confirmed, I will send it to you.",
                  c, "evaluation", "La solución usa tiempos, regla, alternativa justificada y mensaje final completo.",
                  requires=all_c),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona datos de un viaje aéreo con decisiones justificadas.",
                  [("Connection needs 50 minutes; only 30 available", "pedir el vuelo siguiente"),
                   ("Hostel holds beds until 20:00", "avisar antes si la llegada cambia"),
                   ("Ticket includes one free change", "cambiar sin pagar tarifa")], c, "review",
                  "Las tres decisiones citan límites y derechos visibles en los datos."),
            order(f"{p}.r02", "Ordena el mensaje después de confirmar la alternativa.",
                  "When the airline confirms the flight, I will send you the gate and arrival time.",
                  c, "review", "El mensaje espera una confirmación y comunica dos datos verificables."),
            write(f"{p}.r03", "Escribe 70–100 palabras para resolver el viaje en bus y ferry.",
                  "Bus llega 13:50; ferry 14:00 exige embarcar 20 min antes. Alternativa 15:30. Hostal guarda cama hasta 17:00 salvo llamada; nueva llegada 17:20. Billete ferry admite cambio. Decide, justifica y escribe a Luis.",
                  "If our bus reaches the port at 13:50, we will miss the 14:00 ferry because boarding closes twenty minutes earlier. We will change our ticket to the 15:30 ferry. Unless we call the hostel before 17:00, it will release the bed. The later ferry arrives at 17:20, so I will call now. Luis, I have changed the ferry and kept our bed. When the operator confirms the gate, I will send it.",
                  "If our bus arrives at 13:50, we cannot use the 14:00 ferry because boarding closes twenty minutes before departure. We will move the ticket to 15:30. Our hostel holds the bed until 17:00 unless we phone, but the new arrival is 17:20, so I will contact it now. Luis, the later ferry and hostel are arranged. I will share the gate when the operator confirms it.",
                  c, "review", "La recuperación cambia transporte, horarios y alojamiento sin repetir la evidencia evaluada.",
                  requires=all_c),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-{n:02d}.t01", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-{n:02d}.t04", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-{n:02d}.t06", f"{p}.r03"),
             f"{p}.e04": (f"en.n3.class-{n:02d}.t06", f"{p}.r03")}
    return make_class(n,
        ["Comprobar retraso, conexión y alojamiento.",
         "Elegir una alternativa mediante condiciones reales.",
         "Justificar y comunicar una solución de 70–100 palabras."],
        [("connection", "conexión"), ("delay", "retraso"), ("minimum", "mínimo"),
         ("platform", "andén"), ("release", "liberar"), ("change", "cambio"),
         ("companion", "acompañante"), ("confirmed", "confirmado")],
        [("Check the delay and the minimum connection time before choosing.",
          "Comprueba el retraso y el tiempo mínimo de conexión antes de elegir.",
          "Delay y minimum permiten justificar la conexión posible."),
         ("If the connection is too short, use the next confirmed service.",
          "Si la conexión es demasiado corta, usa el siguiente servicio confirmado.",
          "If conecta el dato con una alternativa confirmed."),
         ("Use the free change if the ticket allows one.",
          "Usa el cambio gratuito si el billete lo permite.",
          "Change debe apoyarse en una condición escrita del billete."),
         ("Unless you call before the deadline, the hotel may release the room.",
          "Si no llamas antes del límite, el hotel puede liberar la habitación.",
          "Unless y release expresan la regla de alojamiento."),
         ("Tell your companion the decision, reason and next confirmed detail.",
          "Comunica al acompañante la decisión, razón y siguiente dato confirmado.",
          "Companion recibe una solución y un dato verificable."),
         ("Ferry case: If the 16:00 ferry is cancelled, we will use the 17:30 ferry. Unless we call the island hotel before six, it will release our room. I will use the free ticket change, call the hotel, and send my companion the confirmed pier.",
          "Caso del ferry: si se cancela el de las 16:00, usaremos el de las 17:30. Si no llamamos al hotel isleño antes de las seis, liberará la habitación. Usaré el cambio gratuito, llamaré y enviaré al acompañante el muelle confirmado.",
          "El modelo integra condición, regla, dos contingencias y comunicación final.")],
        pools, remap, uses=all_c, cumulative=all_c)


BUILDERS = {21: build_21, 22: build_22, 23: build_23, 24: build_24, 25: build_25}


def words(text: str) -> int:
    return len(re.findall(r"\b[\w’-]+\b", text))


def audit(classes: list[dict[str, Any]], full: bool) -> dict[str, Any]:
    totals: Counter[str] = Counter()
    formats: Counter[str] = Counter()
    indices: Counter[int] = Counter()
    prompts: dict[str, str] = {}
    signatures: dict[str, str] = {}
    map_classes = json.loads(MAP.read_text(encoding="utf-8"))["classes"]
    for cls in classes:
        n = int(cls["id"].rsplit("-", 1)[1])
        spec = map_classes[n - 1]
        assert cls["id"] == spec["id"] and cls["phase"] == spec["phase"]
        assert cls["title"] == spec["title"] and cls["concepts"] == spec["concepts"]
        assert cls["prerequisites"] == spec["prerequisites"]
        assert cls["status"] == "shadow" and cls["runtimeAi"] is False
        assert cls["qualityPolicy"] == QUALITY and 6 <= len(cls["vocabulary"]) <= 12
        assert 4 <= len(cls["teaching"]) <= 6
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
                local_formats.add(item["format"])
                formats[item["format"]] += 1
                key = norm(item["prompt"]["es"])
                assert key not in prompts, (item["id"], prompts.get(key))
                prompts[key] = item["id"]
                feedbacks.append(item["origin"]["feedback"]["es"])
                if pool != "practiceGuided":
                    assert "hint" not in item["origin"]
                if item["format"] in {"elegir", "escuchar"}:
                    assert len(item["choices"]) >= 3
                    idx = item["answer"]["index"]
                    local_indices[idx] += 1
                    indices[idx] += 1
                if item["format"] == "completar":
                    assert "___" in item["prompt"]["es"] or item["origin"].get("sentences")
                if item["format"] == "escribir":
                    accepted = item["answer"]["accepted"]
                    assert len(accepted) >= 2 and len({norm(x) for x in accepted}) >= 2
                stimulus = (item["origin"].get("audio") or item["origin"].get("text")
                            or item["origin"].get("sentences")
                            or item["origin"].get("pairs") or item["prompt"]["es"])
                sig = canonical({"stimulus": stimulus, "answer": item["answer"]}).casefold()
                assert sig not in signatures, (item["id"], signatures.get(sig))
                signatures[sig] = item["id"]
        assert len(local_formats) >= 4
        assert len(feedbacks) == len(set(feedbacks))
        assert len(local_indices) >= 2 and max(local_indices.values()) / sum(local_indices.values()) <= .60
        visible = canonical({"teaching": cls["teaching"], "pools": cls["pools"]}).casefold()
        for entry in cls["vocabulary"]:
            assert entry["en"].casefold() in visible, (cls["id"], entry["en"])
        eval_ids = {x["id"] for x in cls["pools"]["evaluation"]}
        assert set(cls["remediationMap"]) == eval_ids
        teach_ids = {x["id"] for x in cls["teaching"]}
        review_ids = {x["id"] for x in cls["pools"]["review"]}
        for route in cls["remediationMap"].values():
            assert route["reteach"] in teach_ids and route["review"] in review_ids
    if full:
        assert len(classes) == 5 and sum(totals.values()) == 65
        c21, c22, c23, c24, c25 = classes
        c21_e04 = c21["pools"]["evaluation"][-1]
        assert c21_e04["id"] == "en.n3.c21.e04"
        assert c21_e04["format"] == "relacionar" and len(c21_e04["answer"]["pairs"]) == 5
        assert "4 de 5" in c21_e04["prompt"]["es"]
        assert c21_e04["origin"]["scoring"] == {"parts": 5, "minimumCorrect": 4, "independentAttempt": True}
        assert c21["remediationMap"]["en.n3.c21.e02"] == {
            "reteach": "en.n3.class-21.t01", "review": "en.n3.c21.r01"}
        assert c21["remediationMap"]["en.n3.c21.e04"] == {
            "reteach": "en.n3.class-21.t01", "review": "en.n3.c21.r01"}
        c22_e04 = c22["pools"]["evaluation"][-1]
        assert c22_e04["id"] == "en.n3.c22.e04"
        assert c22_e04["format"] == "completar" and len(c22_e04["answer"]["parts"]) == 6
        assert c22_e04["origin"]["scoring"] == {"parts": 6, "minimumCorrect": 5, "independentAttempt": True}
        connectors = Counter(part["text"].casefold() for part in c22_e04["answer"]["parts"])
        assert connectors == Counter({"if": 2, "unless": 2, "when": 2}), connectors
        c23_e04 = c23["pools"]["evaluation"][-1]
        assert c23_e04["id"] == "en.n3.c23.e04"
        assert c23_e04["format"] == "relacionar" and len(c23_e04["answer"]["pairs"]) == 5
        c23_evidence = canonical(c23_e04).casefold()
        assert all(token in c23_evidence for token in ("parking", "pool", "cot", "bike", "shuttle"))
        assert all(token not in c23_evidence for token in (
            "receipt", "refund", "late arrival", "arrival", "breakfast",
            "twenty kilos", "20 kg", "23 kg"))
        assert c23["remediationMap"]["en.n3.c23.e03"] == {
            "reteach": "en.n3.class-23.t01", "review": "en.n3.c23.r02"}
        c23_r02 = c23["pools"]["review"][1]
        c23_r02_text = canonical(c23_r02).casefold()
        assert c23_r02["id"] == "en.n3.c23.r02"
        assert all(token in c23_r02_text for token in ("21:30", "call reception", "keep the room"))
        c23_choice_text = canonical({
            "pg01": c23["pools"]["practiceGuided"][0],
            "p01": c23["pools"]["practice"][0],
            "e01": c23["pools"]["evaluation"][0],
            "e02": c23["pools"]["evaluation"][1],
        }).casefold()
        assert all(token not in c23_choice_text for token in (
            "two refunds", "every fare is flexible", "two keys", "identification becomes optional",
            "automatically free", "cancel the room", "remove the luggage label", "standard room fee"))
        for item_id in ("en.n3.c24.e04", "en.n3.c24.r03"):
            item = next(x for pool in ("evaluation", "review") for x in c24["pools"][pool]
                        if x["id"] == item_id)
            assert all(60 <= words(x) <= 80 for x in item["answer"]["accepted"])
        expected = [CONCEPTS[x] for x in NUMBERS]
        assert c25["usesPatterns"] == expected and c25["cumulativeEvaluation"] == expected
        assert c25["remediationMap"]["en.n3.c25.e01"] == {
            "reteach": "en.n3.class-25.t01", "review": "en.n3.c25.r01"}
        c25_t01 = c25["teaching"][0]["en"].casefold()
        c25_r01 = canonical(c25["pools"]["review"][0]).casefold()
        assert "minimum connection" in c25_t01 and "connection needs" in c25_r01
        assert c25["remediationMap"]["en.n3.c25.e03"] == {
            "reteach": "en.n3.class-25.t06", "review": "en.n3.c25.r03"}
        assert "unless" in c25["pools"]["review"][2]["answer"]["text"].casefold()
        full_text = canonical(classes).casefold()
        assert "excepción negativa" not in full_text and "exception negativa" not in full_text
        for item_id in ("en.n3.c25.e04", "en.n3.c25.r03"):
            item = next(x for pool in ("evaluation", "review") for x in c25["pools"][pool]
                        if x["id"] == item_id)
            assert item["requires"] == expected
            assert all(70 <= words(x) <= 100 for x in item["answer"]["accepted"])
        t06 = c25["teaching"][-1]["en"].casefold()
        e04 = c25["pools"]["evaluation"][-1]["answer"]["text"].casefold()
        r03 = c25["pools"]["review"][-1]["answer"]["text"].casefold()
        assert "ferry case" in t06 and "18:25" in e04 and "13:50" in r03
        for text in (t06, e04, r03):
            assert "if" in text and "unless" in text and "will" in text
    return {"classes": len(classes), "items": sum(totals.values()),
            "pools": dict(totals), "formats": dict(sorted(formats.items())),
            "correctIndices": dict(sorted(indices.items())),
            "prompts": len(prompts), "fingerprints": len(signatures)}


def write_class(n: int) -> Path:
    doc = BUILDERS[n]()
    audit([doc], False)
    path = OUT / f"class-{n:02d}.json"
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_bundle() -> tuple[Path, dict[str, Any]]:
    classes = [json.loads((OUT / f"class-{n:02d}.json").read_text(encoding="utf-8"))
               for n in NUMBERS]
    summary = audit(classes, True)
    doc = {"schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 3,
           "scale": SCALE, "status": "shadow", "runtimeAi": False,
           "selectionPolicy": {"deterministic": True},
           "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
           "range": {"start": 21, "end": 25}, "classes": classes}
    path = OUT / "bundle-21-25.json"
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path, summary


def write_report(paths: list[Path], summary: dict[str, Any]) -> Path:
    file_hashes = "\n".join(f"{digest(path)}  {path.name}" for path in paths)
    text = f"""# DRAFT — Inglés N3 C21–C25

Estado: **DRAFT para revisión independiente; no autorizado para integración**.

## Alcance

- Bloque `real-consequences`, entrada B1, fases `input → form → comprehension → production → transfer`.
- Cinco clases, 65 ejercicios, `status: shadow`, `runtimeAi: false` y contrato `editorial-agent.v2`.
- C23 materializa cinco decisiones basadas en condiciones visibles de reserva.
- C24 reserva producciones de 60–80 palabras; C25, de 70–100 palabras.

## Cierre C25

- `t06`: cancelación de ferry y hotel isleño.
- `e04`: conexión ferroviaria tardía y hotel urbano.
- `r03`: conexión bus–ferry y hostal.
- Los tres escenarios muestran condición real, `if/unless/when`, lectura de reglas,
  contingencias justificadas y mensaje final al acompañante.

## Auditoría

```json
{json.dumps(summary, ensure_ascii=False, indent=2)}
```

## Validación

- Cinco validaciones individuales level 3: OK.
- Bundle C21–C25 level 3: OK.
- Regeneración doble con hashes idénticos.
- Manifiesto incluye el generador y el mapa de entrada.

## Hashes

```text
{file_hashes}
{digest(Path(__file__))}  generate.py
{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json
```

El autor entrega `DRAFT`, nunca `GO`.
"""
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    path = REPORT_OUT / "REPORT.md"
    path.write_text(text, encoding="utf-8")
    return path


def write_all() -> list[Path]:
    classes = [write_class(n) for n in NUMBERS]
    bundle, summary = write_bundle()
    report = write_report(classes + [bundle], summary)
    files = classes + [bundle, report]
    manifest = REPORT_OUT / "MANIFEST.sha256"
    entries = [f"{digest(Path(__file__))}  ../../tools/contenido/generar_editorial_n3_21_25.py",
               f"{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"]
    entries.extend(f"{digest(path)}  {path.name if path.parent == REPORT_OUT else '../../' + str(path.relative_to(ROOT))}" for path in files)
    manifest.write_text("\n".join(entries) + "\n", encoding="utf-8")
    return classes + [bundle, report, manifest]


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
        docs = [json.loads((OUT / f"class-{n:02d}.json").read_text(encoding="utf-8"))
                for n in NUMBERS]
        print(json.dumps(audit(docs, True), ensure_ascii=False, sort_keys=True))
    elif args.all:
        for path in write_all():
            print(path)
    else:
        parser.error("choose --class-number, --bundle, --audit or --all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
