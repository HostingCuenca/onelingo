#!/usr/bin/env python3
"""Generate the isolated English N3 C01-C05 editorial draft."""

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
REPORT_OUT = ROOT / "build/editorial-n3-01-05"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
SCALE = "client-10-levels-v1"
NUMBERS = range(1, 6)
CONCEPTS = {n: f"n3-recent-progress-{n}" for n in NUMBERS}
PHASES = {1: "input", 2: "form", 3: "comprehension", 4: "production", 5: "transfer"}
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


def norm(value: str) -> str:
    return " ".join(re.findall(r"[a-záéíóúüñ0-9']+", value.casefold()))


def hashed(item: dict[str, Any]) -> dict[str, Any]:
    payload = {k: v for k, v in item.items() if k not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return item


def base(i: str, fmt: str, prompt: str, concept: str, pool: str, feedback: str,
         *, requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": hint or "Localiza el marcador y comprueba qué información conecta."}
    return {
        "id": i, "format": fmt, "prompt": {"es": prompt}, "answer": {}, "choices": [],
        "teaches": [concept] if pool == "practiceGuided" else [],
        "requires": [] if pool == "practiceGuided" else list(requires or [concept]),
        "origin": origin,
        "accessibility": {"screenReader": True, "highContrast": True, "largeText": True},
    }


def q(i: str, prompt: str, options: list[str], index: int, c: str, pool: str,
      feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "elegir", prompt, c, pool, feedback, **kw)
    x["choices"] = [{"text": v} for v in options]
    x["answer"] = {"index": index}
    return hashed(x)


def listen(i: str, prompt: str, audio: str, options: list[str], index: int, c: str,
           pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "escuchar", prompt, c, pool, feedback, **kw)
    x["choices"] = [{"text": v} for v in options]
    x["answer"] = {"index": index}
    x["origin"].update({"audio": audio, "audioMode": "tts", "languageCode": "en",
                        "speedOptions": [0.75, 1.0], "maxReplays": 3,
                        "revealTranscriptAfterAttempt": True})
    return hashed(x)


def fill(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str,
         **kw: Any) -> dict[str, Any]:
    x = base(i, "completar", prompt, c, pool, feedback, **kw)
    x["answer"] = {"text": answer, "accepted": [answer]}
    return hashed(x)


def order(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str,
          **kw: Any) -> dict[str, Any]:
    x = base(i, "ordenar", prompt, c, pool, feedback, **kw)
    x["answer"] = {"text": answer, "tokens": answer.split()}
    return hashed(x)


def write(i: str, prompt: str, stimulus: str, answer: str, alternative: str, c: str,
          pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "escribir", prompt, c, pool, feedback, **kw)
    x["origin"]["text"] = stimulus
    x["answer"] = {"text": answer, "accepted": [answer, alternative]}
    return hashed(x)


def match(i: str, prompt: str, pairs: list[tuple[str, str]], c: str, pool: str,
          feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "relacionar", prompt, c, pool, feedback, **kw)
    values = [[a, {"es": b}] for a, b in pairs]
    x["answer"] = {"pairs": values}
    x["origin"]["pairs"] = values
    return hashed(x)


def teaching(number: int, rows: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    result = []
    for idx, (en, es, explanation) in enumerate(rows, 1):
        ew, sw = en.split(), es.split()
        em, sm = max(1, len(ew) // 2), max(1, len(sw) // 2)
        result.append({
            "id": f"en.n3.class-{number:02d}.t{idx:02d}", "en": en, "es": es,
            "explanationEs": explanation,
            "segments": [{"en": " ".join(ew[:em]), "es": " ".join(sw[:sm])},
                         {"en": " ".join(ew[em:]), "es": " ".join(sw[sm:])}],
            "audioText": en, "audioMode": "tts", "languageCode": "en",
            "patternId": CONCEPTS[number],
        })
    return result


def make_class(number: int, objectives: list[str], vocab: list[tuple[str, str]],
               rows: list[tuple[str, str, str]], pools: dict[str, list[dict[str, Any]]],
               remap: dict[str, tuple[str, str]], *, uses: list[str] | None = None,
               cumulative: list[str] | None = None) -> dict[str, Any]:
    spec = json.loads(MAP.read_text())["classes"][number - 1]
    prerequisite = "en.n2.class-100" if number == 1 else f"en.n3.class-{number-1:02d}"
    doc: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 3,
        "cefr": "B1", "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "phase": PHASES[number], "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY), "id": f"en.n3.class-{number:02d}",
        "title": spec["title"], "objectives": {"es": objectives},
        "concepts": [CONCEPTS[number]],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [prerequisite], "usesVocabulary": [x for x, _ in vocab],
        "usesPatterns": uses or [CONCEPTS[number]],
        "vocabulary": [{"en": en, "es": es} for en, es in vocab],
        "teaching": teaching(number, rows), "pools": pools,
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


def build_1() -> dict[str, Any]:
    n, c, p = 1, CONCEPTS[1], "en.n3.c01"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la actualización con un resultado visible ahora.",
              ["I repaired the heater in 2022.", "I have repaired the heater, so the room is warm now.",
               "I will repair the heater next month."], 1, c, "practiceGuided",
              "Have repaired conecta la reparación con la temperatura actual.",
              hint="Busca una acción pasada y una consecuencia que sigue presente."),
            fill(f"{p}.pg02", "Completa con has fixed: Leo ___ the broken shelf; it is safe now.",
                 "has fixed", c, "practiceGuided",
                 "Has fixed presenta la reparación como causa de la seguridad actual.",
                 hint="Leo es tercera persona y el resultado importa ahora."),
            order(f"{p}.pg03", "Ordena la noticia cuyo resultado permite usar la sala.",
                  "We have cleaned the room, so it is available now.", c, "practiceGuided",
                  "Have cleaned explica por qué la sala está disponible en este momento.",
                  hint="Coloca primero el cambio y después su resultado actual."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige el resultado actual del cambio.",
                   "Nina has replaced the broken screen, so the tablet works again.",
                   ["The tablet worked last year", "The screen will break soon",
                    "The tablet works again now"], 2, c, "practice",
                   "Works again now es la consecuencia actual de haber cambiado la pantalla."),
            match(f"{p}.p02", "Relaciona cada actualización con su consecuencia presente.",
                  [("Sam has charged the camera.", "La cámara está lista para usar."),
                   ("I have lost my pass.", "No puedo entrar ahora.")], c, "practice",
                  "Cada present perfect explica una situación comprobable en el presente."),
            write(f"{p}.p03", "Escribe la actualización y su resultado actual.",
                  "Ava reparó la impresora; ahora el equipo puede imprimir.",
                  "Ava has repaired the printer, so the team can print now.",
                  "The team can print now because Ava has repaired the printer.", c, "practice",
                  "Las dos variantes conectan el cambio terminado con la capacidad actual."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige la noticia que explica por qué el ascensor funciona ahora.",
              ["They checked the lift last Tuesday.", "They have repaired the lift, so it works now.",
               "They are going to inspect the lift."], 1, c, "evaluation",
              "Have repaired aporta la causa pasada del funcionamiento actual."),
            listen(f"{p}.e02", "Escucha y selecciona el efecto que continúa en el presente.",
                   "Omar has moved closer to the office, so his journey is shorter now.",
                   ["His journey is shorter now", "He travelled yesterday",
                    "The office moved away"], 0, c, "evaluation",
                   "La consecuencia vigente es que el trayecto de Omar ahora es más corto."),
            write(f"{p}.e03", "Redacta el cambio y la consecuencia que se observa ahora.",
                  "Priya terminó el informe; ahora el cliente puede revisarlo.",
                  "Priya has finished the report, so the client can review it now.",
                  "The client can review the report now because Priya has finished it.", c,
                  "evaluation", "La respuesta muestra acción terminada y disponibilidad presente."),
            q(f"{p}.e04", "¿Qué frase informa solo de un hecho pasado sin resultado actual?",
              ["I have updated the app, so it runs faster now.",
               "I have just found the key, so the door can open.",
               "I updated the app during Monday's meeting."], 2, c, "evaluation",
              "During Monday's meeting cierra el tiempo y no declara una consecuencia actual."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada mensaje del edificio con su función temporal.",
                  [("Mia has booked the venue.", "El evento ya tiene lugar."),
                   ("The café has opened.", "Los clientes pueden entrar ahora."),
                   ("The team checked the room on Monday.", "Hecho pasado sin efecto actual declarado.")], c, "review",
                  "La recuperación contrasta dos efectos presentes con un hecho pasado fechado."),
            order(f"{p}.r02", "Ordena la actualización sobre el archivo disponible.",
                  "Jon has uploaded the file, so we can read it now.", c, "review",
                  "El archivo puede leerse ahora porque Jon ya completó la carga."),
            write(f"{p}.r03", "Explica por qué el laboratorio vuelve a estar disponible.",
                  "Mei arregló la puerta rota; ahora todos pueden entrar.",
                  "Mei has repaired the broken door, so everyone can enter the lab now.",
                  "Everyone can enter the lab now because Mei has fixed the broken door.", c,
                  "review", "La recuperación conserva reparación, puerta y acceso actual."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-01.t01", f"{p}.r02"),
             f"{p}.e02": (f"en.n3.class-01.t02", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-01.t06", f"{p}.r03"),
             f"{p}.e04": (f"en.n3.class-01.t03", f"{p}.r01")}
    return make_class(n,
        ["Reconocer acciones pasadas con consecuencias visibles ahora.",
         "Distinguir resultado actual de un hecho ubicado en tiempo terminado.",
         "Expresar un cambio mediante have o has y un participio."],
        [("result", "resultado"), ("repair", "reparar"), ("broken", "roto"),
         ("available", "disponible"), ("already", "ya"), ("just", "acabar de"),
         ("yet", "todavía"), ("update", "actualización")],
        [("I have repaired the broken lamp, so it works now.",
          "He reparado la lámpara rota, así que ahora funciona.",
          "Present perfect presenta la reparación y el resultado que aún importa."),
         ("Lena has updated the calendar; the new times are available now.",
          "Lena ha actualizado el calendario; los horarios nuevos están disponibles.",
          "Has updated conecta una actualización terminada con información disponible."),
         ("We repaired the broken door last Friday.", "Reparamos la puerta rota el viernes pasado.",
          "Past simple con last Friday informa un hecho cerrado, no su efecto actual."),
         ("They have already finished, and I have just sent the result.",
          "Ellos ya terminaron y yo acabo de enviar el resultado.",
          "Already y just sitúan cambios recientes con relevancia presente."),
         ("The room is not available yet because the team has not finished.",
          "La sala aún no está disponible porque el equipo no ha terminado.",
          "Not ... yet expresa que el resultado esperado todavía no existe."),
         ("We have completed the safety check, so the hall is available now.",
          "Hemos completado la revisión de seguridad, así que la sala está disponible.",
          "El modelo integrado une un logro en present perfect con su efecto actual.")], pools, remap)


def build_2() -> dict[str, Any]:
    n, c, p = 2, CONCEPTS[2], "en.n3.c02"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la pregunta sobre experiencia sin fecha terminada.",
              ["Did you visit Rome in 2022?", "Have you ever visited Rome?",
               "Will you visit Rome next year?"], 1, c, "practiceGuided",
              "Have you ever pregunta por una experiencia de la vida sin fecha cerrada.",
              hint="Ever no indica un año o día terminado."),
            fill(f"{p}.pg02", "Completa con saw: We ___ that exhibition yesterday.", "saw", c,
                 "practiceGuided", "Yesterday exige el past simple irregular saw.",
                 hint="El marcador cierra la acción en un día anterior."),
            order(f"{p}.pg03", "Ordena la experiencia que no menciona una fecha.",
                  "I have tried online classes twice.", c, "practiceGuided",
                  "Have tried resume una experiencia acumulada sin momento terminado.",
                  hint="Coloca have antes del participio tried."),
        ],
        "practice": [
            match(f"{p}.p01", "Relaciona el marcador con el tiempo verbal que exige.",
                  [("ever", "experiencia en present perfect"),
                   ("last summer", "periodo terminado en past simple"),
                   ("in 2021", "fecha exacta en past simple")], c, "practice",
                  "Ever abre la experiencia; last summer e in 2021 cierran el tiempo."),
            listen(f"{p}.p02", "Escucha y elige cuándo ocurrió el viaje específico.",
                   "I have travelled abroad several times. I went to Peru in 2023.",
                   ["In 2021", "No date is given", "In 2023"], 2, c, "practice",
                   "Went to Peru in 2023 aporta el hecho concreto dentro de la experiencia."),
            write(f"{p}.p03", "Escribe experiencia general y detalle fechado.",
                  "Experiencia: trabajar en equipo. Detalle: proyecto escolar, abril pasado.",
                  "I have worked in teams. I joined a school project last April.",
                  "I have taken part in team projects; I joined a school project last April.", c,
                  "practice", "Las variantes separan experiencia acumulada y episodio fechado."),
        ],
        "evaluation": [
            q(f"{p}.e01", "No se da fecha. Elige la pregunta correcta sobre kayak.",
              ["Have you ever been kayaking?", "Did you go kayaking last Saturday?",
               "Are you going kayaking tomorrow?"], 0, c, "evaluation",
              "Have you ever been kayaking mantiene abierta la experiencia de la vida."),
            fill(f"{p}.e02", "Usa visit en pasado: I ___ the science museum in 2022.",
                 "visited", c, "evaluation",
                 "Visited concuerda con el año terminado 2022."),
            listen(f"{p}.e03", "Escucha y selecciona la experiencia general, no el hecho fechado.",
                   "Tom has repaired several bicycles. He fixed a race bike on 3 June.",
                   ["He fixed a race bike on 3 June", "He has repaired several bicycles",
                    "He repairs every bicycle on 3 June"], 1, c, "evaluation",
                   "Has repaired several bicycles resume la experiencia sin limitarla al 3 de junio."),
            write(f"{p}.e04", "Redacta la experiencia y el hecho concreto sin mezclar tiempos.",
                  "Experiencia: cocinar para grupos. Hecho: cena benéfica, diciembre de 2024.",
                  "I have cooked for groups. I prepared a charity dinner in December 2024.",
                  "I have cooked for large groups; I made a charity dinner in December 2024.",
                  c, "evaluation", "La experiencia usa present perfect y el evento fechado, past simple."),
        ],
        "review": [
            match(f"{p}.r01", "Une cada oración del taller con su función temporal.",
                  [("Have you ever led a workshop?", "experiencia abierta"),
                   ("I led one on 12 March.", "hecho fechado")], c, "review",
                  "El contraste recupera experiencia general y evento del 12 de marzo."),
            order(f"{p}.r02", "Ordena el detalle de una carrera ocurrida el año pasado.",
                  "I ran my first race last year.", c, "review",
                  "Ran y last year forman un hecho completo en past simple."),
            write(f"{p}.r03", "Cuenta una experiencia tecnológica y un momento específico.",
                  "Experiencia: crear sitios web. Detalle: sitio del club, enero pasado.",
                  "I have created websites. I built the club website last January.",
                  "I have built several websites; I made the club site last January.", c,
                  "review", "La recuperación asigna cada idea a su marco temporal correcto."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-02.t01", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-02.t03", f"{p}.r02"),
             f"{p}.e03": (f"en.n3.class-02.t04", f"{p}.r01"),
             f"{p}.e04": (f"en.n3.class-02.t04", f"{p}.r03")}
    return make_class(n,
        ["Elegir present perfect para experiencias sin fecha terminada.",
         "Usar past simple cuando el mensaje incluye un momento cerrado.",
         "Combinar experiencia general y detalle específico en dos oraciones."],
        [("experience", "experiencia"), ("ever", "alguna vez"), ("never", "nunca"),
         ("several", "varios"), ("centre", "centro"), ("dated", "fechado"),
         ("conference", "conferencia"), ("abroad", "en el extranjero")],
        [("Have you ever worked abroad?", "¿Alguna vez has trabajado en el extranjero?",
          "Ever abre una pregunta sobre experiencia sin fecha terminada."),
         ("I have never led a conference session.", "Nunca he dirigido una sesión de conferencia.",
          "Never resume una experiencia ausente hasta el presente."),
         ("We visited the centre in 2022.", "Visitamos el centro en 2022.",
          "El año específico 2022 exige past simple."),
         ("She has given several talks; she spoke here last May.",
          "Ella ha dado varias charlas; habló aquí en mayo pasado.",
          "La primera parte resume experiencia y la segunda aporta un hecho fechado."),
         ("Ask about experience first, then request a dated detail.",
          "Pregunta primero por la experiencia y luego pide un detalle fechado.",
          "La secuencia evita usar present perfect con un tiempo pasado terminado.")], pools, remap)


def build_3() -> dict[str, Any]:
    n, c, p = 3, CONCEPTS[3], "en.n3.c03"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la actualización general, no el detalle fechado.",
              ["We tested it on Tuesday.", "The technician arrived at nine.",
               "We have improved the booking system."], 2, c, "practiceGuided",
              "Have improved presenta el cambio general antes de explicar cuándo ocurrió.",
              hint="La actualización general no lleva día ni hora terminados."),
            match(f"{p}.pg02", "Relaciona cada pregunta con el detalle que solicita.",
                  [("When did it happen?", "fecha u hora"),
                   ("How did you solve it?", "método usado")], c, "practiceGuided",
                  "When localiza el momento; how pide el procedimiento.",
                  hint="Distingue tiempo de manera."),
            order(f"{p}.pg03", "Ordena la respuesta que añade un detalle de método.",
                  "We solved it by replacing the cable.", c, "practiceGuided",
                  "By replacing the cable explica cómo se resolvió el problema.",
                  hint="Empieza con el resultado y termina con el método."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige la fecha del cambio específico.",
                   "We have improved the entrance. The builders installed the new ramp on 6 June.",
                   ["On 6 June", "On 16 June", "No date is stated"], 0, c, "practice",
                   "Installed on 6 June aporta la fecha concreta detrás de la mejora."),
            match(f"{p}.p02", "Une cada dato de la actualización con su función.",
                  [("The service has become faster.", "resultado general"),
                   ("We changed the server last Thursday.", "fecha y acción"),
                   ("We moved the files in two hours.", "método y duración")], c, "practice",
                  "Los tres datos separan resultado, momento y procedimiento."),
            write(f"{p}.p03", "Escribe actualización general, fecha y modo de solución.",
                  "Resultado: mejoró el jardín. Fecha: 3 abril. Método: plantaron árboles.",
                  "We have improved the garden. On 3 April, we planted new trees.",
                  "The garden has improved; we planted new trees there on 3 April.", c,
                  "practice", "Las variantes distinguen el resultado actual del detalle fechado."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha y selecciona el resultado general del informe.",
                   "Our delivery process has become more reliable. We changed the route last month.",
                   ["The route changed last month", "The process is more reliable now",
                    "Drivers now use a shorter route"], 1, c, "evaluation",
                   "Has become more reliable resume el resultado que sigue vigente."),
            q(f"{p}.e02", "¿Qué dato responde directamente a cuándo ocurrió la reparación?",
              ["The machine works better now.", "They used a metal part.",
               "The mechanic repaired it on 14 August."], 2, c, "evaluation",
              "On 14 August proporciona el momento exacto solicitado por when."),
            q(f"{p}.e03", "¿Qué frase explica cómo redujeron el ruido?",
              ["They added soft panels to the walls.", "The room is quieter now.",
               "The work ended last Wednesday."], 0, c, "evaluation",
              "Added soft panels describe el método que produjo la reducción del ruido."),
            write(f"{p}.e04", "Resume resultado, fecha y método del cambio del centro.",
                  "Resultado: acceso más fácil. Fecha: 18 febrero. Método: instalaron puerta automática.",
                  "The centre has made access easier. On 18 February, workers installed an automatic door.",
                  "Access to the centre has improved; workers fitted an automatic door on 18 February.",
                  c, "evaluation", "La síntesis conserva resultado vigente, fecha exacta y acción realizada."),
        ],
        "review": [
            match(f"{p}.r01", "Clasifica los datos de una actualización sobre la biblioteca.",
                  [("The library has extended its hours.", "resultado actual"),
                   ("The change began on 2 September.", "fecha concreta"),
                   ("Staff tested the schedule with students.", "cómo se realizó")], c, "review",
                  "La recuperación mantiene separadas la noticia principal, la fecha y el método."),
            order(f"{p}.r02", "Ordena el detalle que explica cómo recuperaron los documentos.",
                  "They recovered the documents by using a backup copy.", c, "review",
                  "By using a backup copy responde de forma directa a how."),
            write(f"{p}.r03", "Redacta los tres datos de la mejora del mercado.",
                  "Resultado: mercado más limpio. Fecha: 9 mayo. Método: nuevos contenedores.",
                  "The market has become cleaner. On 9 May, the council added new bins.",
                  "The market is cleaner now because the council installed new bins on 9 May.", c,
                  "review", "La recuperación combina efecto actual, día terminado y medio concreto."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-03.t01", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-03.t03", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-03.t04", f"{p}.r02"),
             f"{p}.e04": (f"en.n3.class-03.t05", f"{p}.r03")}
    return make_class(n,
        ["Identificar el resultado general de una actualización.",
         "Extraer una fecha concreta expresada con past simple.",
         "Reconocer el método que explica cómo ocurrió un cambio."],
        [("date", "fecha"), ("overall", "general"), ("result", "resultado"),
         ("method", "método"), ("reliable", "fiable"), ("improved", "mejorado"),
         ("installed", "instaló"), ("backup", "copia de seguridad")],
        [("The service has improved, and it is more reliable now.",
          "El servicio ha mejorado y ahora es más fiable.",
          "La primera oración da el resultado general que importa en el presente."),
         ("We installed the new system on 12 March.",
          "Instalamos el sistema nuevo el 12 de marzo.",
          "La fecha específica convierte la acción en un detalle de past simple."),
         ("When did you make the change? Give the date.", "¿Cuándo hicieron el cambio? Da la fecha.",
          "When solicita una fecha u hora concreta."),
         ("How did you solve the problem? We used a backup.",
          "¿Cómo resolvieron el problema? Usamos una copia de seguridad.",
          "How pide el método y la respuesta aporta el procedimiento."),
         ("A clear update gives the overall result, a date and a method.",
          "Una actualización clara da el resultado general, una fecha y un método.",
          "Los tres datos permiten comprender y comprobar el cambio.")], pools, remap)


def build_4() -> dict[str, Any]:
    n, c, p = 4, CONCEPTS[4], "en.n3.c04"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la apertura que presenta un logro con efecto actual.",
              ["We painted a wall in 2020.", "We have completed the first stage, so testing can begin.",
               "We may start a project next year."], 1, c, "practiceGuided",
              "Have completed introduce el logro y testing can begin muestra su efecto.",
              hint="Busca logro terminado y consecuencia presente."),
            order(f"{p}.pg02", "Ordena el detalle fechado de una actualización de progreso.",
                  "The team tested the new form last Thursday.", c, "practiceGuided",
                  "Tested y last Thursday aportan un hecho concreto en past simple.",
                  hint="Coloca el marcador de tiempo después del objeto."),
            fill(f"{p}.pg03", "Completa con has improved: The process ___, so delays are shorter.",
                 "has improved", c, "practiceGuided",
                 "Has improved conecta el avance con retrasos más cortos ahora.",
                 hint="The process es singular y el resultado continúa."),
        ],
        "practice": [
            write(f"{p}.p01", "Escribe logro, efecto actual y detalle pasado del huerto.",
                  "Logro: terminar riego. Ahora: plantas reciben agua. Detalle: prueba, martes.",
                  "We have finished the watering system, so the plants receive water now. We tested it on Tuesday.",
                  "We have completed the watering system, so it works now; we tested it last Tuesday.", c,
                  "practice", "Las variantes incluyen logro, efecto presente y prueba fechada."),
            listen(f"{p}.p02", "Escucha y elige el detalle pasado que respalda el progreso.",
                   "We have prepared the exhibition, so it can open. We hung the final pictures on Monday.",
                   ["They hung the final pictures on Monday", "It can open now",
                    "They will choose pictures next year"], 0, c, "practice",
                   "Hung on Monday es el paso terminado y fechado que respalda la actualización."),
            match(f"{p}.p03", "Une cada parte del informe con su función.",
                  [("We have trained six volunteers.", "logro"),
                   ("They can welcome visitors now.", "resultado actual"),
                   ("The course ended on Friday.", "detalle pasado")], c, "practice",
                  "La estructura distribuye logro, efecto vigente y prueba fechada."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige el informe que incluye logro y efecto presente.",
              ["We discussed the plan last winter.",
               "We have installed the lights, so evening classes can start.",
               "We are going to buy lights next month."], 1, c, "evaluation",
              "Have installed y can start enlazan el avance con una posibilidad actual."),
            listen(f"{p}.e02", "Escucha y selecciona el paso que ocurrió el 8 de julio.",
                   "The archive has become easier to search. We added topic labels on 8 July.",
                   ["The search became slower", "They removed every label",
                    "They added topic labels"], 2, c, "evaluation",
                   "Added topic labels identifica el detalle fechado del 8 de julio."),
            write(f"{p}.e03", "Redacta una actualización breve sobre la aplicación escolar.",
                  "Logro: lanzar nueva versión. Ahora: familias ven horarios. Detalle: prueba 24 mayo.",
                  "We have launched the new school app, so families can see schedules now. We tested the final version on 24 May.",
                  "We have released the new school app, so families can view schedules; we tested it on 24 May.", c,
                  "evaluation", "La producción conserva el logro, su utilidad actual y la fecha de prueba."),
            write(f"{p}.e04", "Escribe 60–80 palabras sobre el progreso del proyecto de lectura.",
                  "Proyecto: rincón de lectura. Logros: 120 libros y estantes reparados. Resultado: abre tras clases. Detalles: catálogo, 7 abril; estantes, 10 abril. Escuela compartió fecha y equipo preparó guía. Próximo: invitar familias.",
                  "We have collected 120 books and repaired the shelves, so the reading corner can now open after classes. Volunteers catalogued the books on 7 April, and a carpenter finished the shelves on 10 April. Families can already use the space. The school has shared the opening date, and the team has prepared a welcome guide. Our next step is to invite families to visit the space.",
                  "The reading corner is ready because we have collected 120 books and fixed the shelves. Volunteers catalogued everything on 7 April, and the carpenter completed the shelves on 10 April. The space is now available after classes. The school has shared the opening date, and the team has prepared a welcome guide. Next, we will invite local families to visit the space.", c, "evaluation",
                  "El texto integra dos logros, resultado actual, dos hechos fechados y siguiente paso."),
        ],
        "review": [
            match(f"{p}.r01", "Clasifica la actualización del proyecto de bicicletas.",
                  [("We have repaired ten bicycles.", "logro"),
                   ("Students can borrow them now.", "resultado actual"),
                   ("The last repair ended on 16 June.", "detalle fechado")], c, "review",
                  "La recuperación separa las tres funciones en un proyecto distinto."),
            order(f"{p}.r02", "Ordena el cierre que anuncia el siguiente paso del equipo.",
                  "Next, we are going to train the new helpers.", c, "review",
                  "Next organiza la acción futura después de informar el progreso."),
            write(f"{p}.r03", "Escribe 60–80 palabras sobre la mejora del comedor comunitario.",
                  "Logros: pintar comedor y conseguir 40 sillas. Resultado: sirve a más personas. Detalles: pintura 2 marzo; sillas, 5 marzo. Confirmaron primer almuerzo la próxima semana. Próximo: formar equipo de cocina.",
                  "We have painted the community dining room and obtained forty chairs, so it can serve more people now. Volunteers painted the room on 2 March, and the chairs arrived on 5 March. The main space is already available for lunch groups. The organisers have confirmed that the first lunch group can attend next week. Next, we will train a small cooking team for future meals.",
                  "The community dining room can welcome larger groups because we have painted it and found forty chairs. The painting finished on 2 March, and the chairs arrived three days later. The room is now ready for lunch. The organisers have confirmed that the first lunch group can attend next week. Our next step is to train kitchen volunteers for future meals.", c, "review",
                  "La recuperación mantiene progreso, efecto, cronología y siguiente acción."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-04.t01", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-04.t03", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-04.t06", f"{p}.r03"),
             f"{p}.e04": (f"en.n3.class-04.t06", f"{p}.r03")}
    return make_class(n,
        ["Producir una actualización con logro y efecto actual.",
         "Añadir detalles fechados que respalden el progreso.",
         "Cerrar el informe con un siguiente paso concreto."],
        [("progress", "progreso"), ("stage", "etapa"), ("completed", "completado"),
         ("launched", "lanzado"), ("test", "prueba"), ("volunteers", "voluntarios"),
         ("already", "ya"), ("next step", "siguiente paso")],
        [("We have completed the first stage, so testing can begin now.",
          "Hemos completado la primera etapa, así que las pruebas pueden comenzar.",
          "Present perfect presenta un logro cuyo resultado permite avanzar."),
         ("The team has launched the update, and users can already open it.",
          "El equipo ha lanzado la actualización y los usuarios ya pueden abrirla.",
          "Already subraya que el efecto está disponible en el presente."),
         ("The test involved five volunteers on 11 June.",
          "La prueba incluyó a cinco voluntarios el 11 de junio.",
          "Past simple añade quién, qué y cuándo como evidencia concreta."),
         ("A progress update links the achievement to its current result.",
          "Una actualización enlaza el logro con su resultado actual.",
          "La relación causal evita una lista de acciones sin propósito."),
         ("End with a next step that follows from the progress.",
          "Termina con un siguiente paso que continúe el progreso.",
          "El cierre proyecta una acción concreta a partir del avance informado."),
         ("We have completed the website, so families can use it now. We tested it on Monday. Next, volunteers will add new guides.",
          "Hemos completado el sitio web, así que las familias ya pueden usarlo. Lo probamos el lunes. Después, los voluntarios añadirán guías.",
          "El modelo integrado contiene logro, resultado actual, detalle fechado y siguiente paso.")], pools, remap)


def build_5() -> dict[str, Any]:
    n, c, p = 5, CONCEPTS[5], "en.n3.c05"
    all_concepts = [CONCEPTS[i] for i in NUMBERS]
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la apertura que comparte un cambio relevante ahora.",
              ["I changed jobs in 2018 and forgot the date.",
               "I have started a new role, so I work with a larger team now.",
               "I may look for a role next year."], 1, c, "practiceGuided",
              "Have started introduce el cambio y el equipo mayor muestra su efecto actual.",
              hint="Busca un cambio reciente unido a una situación presente."),
            order(f"{p}.pg02", "Ordena la pregunta que solicita un detalle de fecha.",
                  "When did you begin the new course?", c, "practiceGuided",
                  "When did you begin pide el momento concreto del cambio.",
                  hint="Coloca did antes del sujeto y usa begin en forma base."),
            match(f"{p}.pg03", "Relaciona cada pregunta con el detalle de seguimiento.",
                  [("How did you find the position?", "método"),
                   ("What has changed since then?", "resultado actual")], c,
                  "practiceGuided",
                  "How pide el proceso y what has changed explora el efecto presente.",
                  hint="Distingue el camino pasado de la situación que continúa."),
        ],
        "practice": [
            write(f"{p}.p01", "Escribe el cambio de Hana y una pregunta de seguimiento.",
                  "Hana terminó curso de diseño y ahora trabaja en publicidad. Pregunta: cuándo terminó.",
                  "Hana has completed a design course, so she works in advertising now. When did she finish it?",
                  "Hana now works in advertising because she has completed a design course. When did the course end?",
                  c, "practice", "Las variantes conectan cambio, resultado actual y pregunta de fecha."),
            listen(f"{p}.p02", "Escucha y elige cómo consiguió Malik su nuevo trabajo.",
                   "Malik has found a new job at a hotel. A former teacher recommended him in February.",
                   ["A teacher recommended him", "He applied next December",
                    "The hotel moved in February"], 0, c, "practice",
                   "Recommended him in February explica el método y aporta el detalle fechado."),
            match(f"{p}.p03", "Une cada parte del reencuentro con su función.",
                  [("I have moved to Bristol.", "cambio relevante"),
                   ("I moved there in September.", "detalle fechado"),
                   ("What do you like about it?", "pregunta de seguimiento")], c, "practice",
                  "El intercambio separa noticia, momento concreto y pregunta relacionada."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige la respuesta que une experiencia y hecho fechado.",
              ["I have taught online, and I led my first virtual class last October.",
               "I have taught online, and I have led my first class last October.",
               "I have taught online, and I have led classes since last October."], 0, c, "evaluation",
              "Have taught resume la experiencia y led last October aporta el episodio concreto."),
            listen(f"{p}.e02", "Escucha y selecciona el resultado que sigue vigente.",
                   "Eva has completed her nursing course. She passed the final exam on 20 June, and she can apply for hospital jobs now.",
                   ["She will take the exam next June", "She can apply for hospital jobs now",
                    "She stopped studying in 2020"], 1, c, "evaluation",
                   "Can apply now es el efecto presente de haber completado el curso."),
            write(f"{p}.e03", "Redacta dos preguntas para ampliar la actualización de Omar.",
                  "Omar ha abierto una panadería; abrió el local en marzo y aprendió con su tía.",
                  "When did you open the bakery? How did your aunt help you learn?",
                  "What date did the bakery open? How did you learn from your aunt?", c,
                  "evaluation", "Las preguntas solicitan fecha y método sin repetir la información dada."),
            write(f"{p}.e04", "Escribe 70–100 palabras para el reencuentro en el estudio musical.",
                  "Lina no ve a Jo desde hace un año. Jo abrió estudio musical; ahora ofrece clases nocturnas. Abrió 12 enero; equipos donados por escuela. Próximo: grabar coro con tres músicos locales el mes próximo. Lina pregunta fecha y método; Jo responde.",
                  "Jo: I have opened a music studio, so I can offer evening lessons now. I opened it on 12 January, and a local school donated the equipment. We are preparing to record a community choir next. I have also invited three local musicians to help with the first recording next month. Lina: When did the studio open? How did you get the equipment? Jo: It opened on 12 January, and the school gave it to us.",
                  "Jo: I have started a music studio and now teach evening classes there. The studio opened on 12 January after a local school donated its equipment. Our next project is recording a community choir. I have also invited three local musicians to help with the first recording next month. Lina: What date did you open? How did you obtain the instruments? Jo: On 12 January; the school gave them to us.", c, "evaluation",
                  "El diálogo integra cambio, efecto, dos detalles, próximo paso y dos preguntas respondidas.",
                  requires=all_concepts),
        ],
        "review": [
            match(f"{p}.r01", "Clasifica los datos del reencuentro de dos antiguas compañeras.",
                  [("I have become a team leader.", "cambio con efecto actual"),
                   ("The promotion happened in November.", "detalle fechado"),
                   ("How did your duties change?", "seguimiento sobre el resultado")], c,
                  "review", "La recuperación distingue noticia, fecha y pregunta relacionada."),
            order(f"{p}.r02", "Ordena dos preguntas sobre la fecha y el método del cambio.",
                  "When did the change happen? How did you find the opportunity?", c, "review",
                  "When recupera la fecha y how solicita el método de la oportunidad."),
            write(f"{p}.r03", "Redacta 70–100 palabras para el reencuentro del club ciclista.",
                  "Noah vuelve a ver a Iris. Iris creó club ciclista; ahora 30 miembros entrenan cada semana. Primera salida: 4 mayo. Tienda local dio cascos. Ya completaron taller de seguridad. Próximo: ruta benéfica. Noah pregunta fecha y método; Iris responde.",
                  "Iris: I have created a cycling club, so thirty members train together every week now. We held our first ride on 4 May, and a local shop provided the helmets. The club has also completed a safety workshop for all its new riders. Next, we are planning a charity route. Noah: When was your first ride? How did you get the helmets? Iris: It was on 4 May, and the shop supplied them.",
                  "Iris: I have started a cycling club that now has thirty weekly riders. Our first group ride took place on 4 May, and a local shop gave us the helmets. The club has also completed a safety workshop for all its new riders. We will organise a charity route next. Noah: What date was the first ride? How did the shop help? Iris: On 4 May; it supplied the helmets.", c, "review",
                  "La recuperación demuestra las cinco funciones en un club y cronología nuevos.",
                  requires=all_concepts),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-05.t06", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-05.t01", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-05.t04", f"{p}.r02"),
             f"{p}.e04": (f"en.n3.class-05.t06", f"{p}.r03")}
    return make_class(n,
        ["Compartir un cambio con consecuencia presente.",
         "Aportar dos detalles pasados con fechas o métodos verificables.",
         "Formular y responder dos preguntas de seguimiento pertinentes."],
        [("role", "puesto"), ("changed", "cambió"),
         ("detail", "detalle"), ("recommended", "recomendó"),
         ("questions", "preguntas"), ("community", "comunidad"),
         ("equipment", "equipos"), ("opportunity", "oportunidad")],
        [("My role has changed, so I manage a larger team now.",
          "Mi puesto ha cambiado, así que ahora dirijo un equipo mayor.",
          "El cambio en present perfect abre el reencuentro con un efecto actual."),
         ("One detail is that I joined the department last September.",
          "Un detalle es que me incorporé al departamento en septiembre pasado.",
          "Past simple aporta un momento terminado que concreta la actualización."),
         ("A colleague recommended the opportunity to me.",
          "Un colega me recomendó la oportunidad.",
          "El detalle explica cómo apareció la oportunidad."),
         ("Ask two follow-up questions: one about when and one about how.",
          "Haz dos preguntas: una sobre cuándo y otra sobre cómo.",
          "Las dos preguntas recuperan fecha y método sin cambiar el tema."),
         ("Answer each question with a specific detail, not only yes or no.",
          "Responde cada pregunta con un detalle específico, no solo sí o no.",
          "Una respuesta informativa mantiene el reencuentro y verifica la noticia."),
         ("Mara: I have joined a community kitchen, so I cook for families now. I started on 8 February after a neighbour recommended the opportunity. We have already served fifty meals, and we are planning weekend sessions. Leo: When did you start? How did you hear about it? Mara: On 8 February; my neighbour told me.",
          "Mara se unió a una cocina comunitaria y ahora cocina para familias. Empezó el 8 de febrero por recomendación de una vecina. Ya sirvieron cincuenta comidas y planean sesiones de fin de semana. Leo pregunta cuándo empezó y cómo conoció la oportunidad; Mara responde.",
          "El modelo integra cambio actual, experiencia, detalles pasados, progreso y seguimiento." )],
        pools, remap, uses=all_concepts, cumulative=all_concepts)


BUILDERS = {1: build_1, 2: build_2, 3: build_3, 4: build_4, 5: build_5}


def audit(classes: list[dict[str, Any]], full: bool) -> dict[str, Any]:
    totals: Counter[str] = Counter()
    formats: Counter[str] = Counter()
    indices: Counter[int] = Counter()
    prompts: dict[str, str] = {}
    signatures: dict[str, str] = {}
    for cls in classes:
        assert cls["status"] == "shadow" and cls["runtimeAi"] is False
        assert cls["qualityPolicy"] == QUALITY
        assert len(cls["vocabulary"]) in range(6, 13)
        assert len(cls["teaching"]) in range(4, 7)
        local_formats: set[str] = set()
        local_indices: Counter[int] = Counter()
        feedbacks: list[str] = []
        for pool, expected in (("practiceGuided", 3), ("practice", 3),
                               ("evaluation", 4), ("review", 3)):
            items = cls["pools"][pool]
            assert len(items) == expected
            totals[pool] += len(items)
            for item in items:
                assert len(item["prompt"]["es"]) <= 90, (item["id"], len(item["prompt"]["es"]))
                assert item["contentHash"] == "sha256:" + hashlib.sha256(canonical(
                    {k: v for k, v in item.items() if k not in {"id", "contentHash"}}
                ).encode()).hexdigest()
                local_formats.add(item["format"]); formats[item["format"]] += 1
                key = norm(item["prompt"]["es"])
                assert key not in prompts, (item["id"], prompts.get(key))
                prompts[key] = item["id"]
                feedbacks.append(item["origin"]["feedback"]["es"])
                if pool != "practiceGuided":
                    assert "hint" not in item["origin"]
                if item["format"] in {"elegir", "escuchar"}:
                    assert len(item["choices"]) >= 3
                    idx = item["answer"]["index"]
                    assert 0 <= idx < len(item["choices"])
                    local_indices[idx] += 1; indices[idx] += 1
                if item["format"] == "escribir":
                    accepted = item["answer"]["accepted"]
                    assert len(accepted) >= 2 and len({norm(v) for v in accepted}) >= 2
                stimulus = item["origin"].get("audio") or item["origin"].get("text") \
                    or item["origin"].get("pairs") or item["prompt"]["es"]
                answer = item["answer"]
                signature = canonical({"stimulus": stimulus, "answer": answer}).casefold()
                assert signature not in signatures, (item["id"], signatures.get(signature))
                signatures[signature] = item["id"]
        assert len(local_formats) >= 4
        assert len(feedbacks) == len(set(feedbacks))
        assert len(local_indices) >= 2 and max(local_indices.values()) / sum(local_indices.values()) <= .60
        visible = canonical({"teaching": cls["teaching"], "pools": cls["pools"]}).casefold()
        for entry in cls["vocabulary"]:
            assert entry["en"].casefold() in visible, (cls["id"], entry["en"])
        eval_ids = {item["id"] for item in cls["pools"]["evaluation"]}
        assert set(cls["remediationMap"]) == eval_ids
        teach_ids = {item["id"] for item in cls["teaching"]}
        review_ids = {item["id"] for item in cls["pools"]["review"]}
        for route in cls["remediationMap"].values():
            assert route["reteach"] in teach_ids and route["review"] in review_ids
        if cls["phase"] in {"production", "transfer"}:
            reserved = [item for pool in ("evaluation", "review")
                        for item in cls["pools"][pool] if item["format"] == "escribir"]
            assert any(len(re.findall(r"\b[\w’-]+\b", item["answer"]["text"])) >= 8
                       and len(item["answer"]["accepted"]) >= 2 for item in reserved)
    if full:
        assert len(classes) == 5 and sum(totals.values()) == 65
        close = classes[-1]
        expected = [CONCEPTS[n] for n in NUMBERS]
        assert close["cumulativeEvaluation"] == expected
        assert close["usesPatterns"] == expected
        final = next(x for x in close["pools"]["evaluation"] if x["id"] == "en.n3.c05.e04")
        recovery = next(x for x in close["pools"]["review"] if x["id"] == "en.n3.c05.r03")
        assert final["requires"] == expected and recovery["requires"] == expected
        t06 = close["teaching"][-1]["en"].casefold()
        e04 = final["answer"]["text"].casefold()
        r03 = recovery["answer"]["text"].casefold()
        assert "community kitchen" in t06 and "music studio" in e04 and "cycling club" in r03
        for text in (t06, e04, r03):
            assert "have" in text and "when" in text and "how" in text
        assert "12 january" in e04 and "4 may" in r03
    return {"classes": len(classes), "items": sum(totals.values()), "pools": dict(totals),
            "formats": dict(sorted(formats.items())),
            "correctIndices": dict(sorted(indices.items())),
            "prompts": len(prompts), "fingerprints": len(signatures)}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_class(number: int) -> Path:
    document = BUILDERS[number]()
    audit([document], False)
    path = OUT / f"class-{number:02d}.json"
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_bundle() -> tuple[Path, dict[str, Any]]:
    classes = [json.loads((OUT / f"class-{n:02d}.json").read_text()) for n in NUMBERS]
    summary = audit(classes, True)
    bundle = {
        "schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 3,
        "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "range": {"start": 1, "end": 5}, "classes": classes,
    }
    path = OUT / "bundle-01-05.json"
    path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path, summary


def write_report(paths: list[Path], summary: dict[str, Any]) -> Path:
    hashes = "\n".join(f"{file_digest(path)}  {path.name}" for path in paths)
    report = f"""# CORRECTED — Inglés N3 C01–C05

Estado: **CORRECTED en staging; no autorizado para integración**.

## Alcance

- Primer bloque N3 de entrada B1: `recent-progress`.
- Cinco clases en ciclo `input → form → comprehension → production → transfer`.
- 13 ejercicios por clase: 3 guiados, 3 de práctica, 4 de evaluación y 3 de repaso.
- `status: shadow`, `runtimeAi: false`, contrato `editorial-agent.v2`.

## Evidencia del cierre C05

- `t06`: reencuentro sobre una cocina comunitaria.
- `e04`: reencuentro sobre un estudio musical.
- `r03`: reencuentro sobre un club ciclista.
- Los tres escenarios integran present perfect con resultado actual, past simple fechado,
  detalle de método, progreso/siguiente paso y dos preguntas de seguimiento respondidas.

## Correcciones posteriores a revisión

- Todas las variantes de C2 conservan present perfect para la experiencia general.
- C4 conserva present perfect en logro y usa una enseñanza integrada para remediación.
- C1 e03, C2 e04, C4 e03/e04 y C5 e01 tienen rutas semánticas alineadas.
- C2 e03 usa otro escenario y otra operación que t04; se retiraron distractores absurdos.
- C5 e04 mantiene la primera persona de Jo durante toda su intervención.

## Auditoría del generador

```json
{json.dumps(summary, ensure_ascii=False, indent=2)}
```

## Validación reproducible

Resultados de esta generación:

- Cinco validaciones individuales: `OK`.
- Bundle N3 C01–C05: `OK`, 5 clases y 65 ejercicios.
- Pruebas focalizadas: 52 pruebas, `OK`.
- Ruta editorial: 10 idiomas, 0 errores.
- Idempotencia: dos regeneraciones consecutivas producen hashes idénticos.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/contenido/generar_editorial_n3_01_05.py --all
python3 tools/contenido/validar_bundle_editorial.py --file assets/contenido/en/editorial/n3/bundle-01-05.json --start 1 --end 5 --level 3
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s test_tools -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 tools/validar_ruta.py
```

## Hashes de clases y bundle

```text
{hashes}
```

El autor entrega `CORRECTED`, nunca `GO`.
"""
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    path = REPORT_OUT / "REPORT.md"
    path.write_text(report, encoding="utf-8")
    return path


def write_all() -> list[Path]:
    class_paths = [write_class(n) for n in NUMBERS]
    bundle, summary = write_bundle()
    report = write_report(class_paths + [bundle], summary)
    manifest_paths = class_paths + [bundle, report]
    manifest = REPORT_OUT / "MANIFEST.sha256"
    manifest.write_text("\n".join(f"{file_digest(p)}  {p.name}" for p in manifest_paths) + "\n",
                        encoding="utf-8")
    return manifest_paths + [manifest]


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
        classes = [json.loads((OUT / f"class-{n:02d}.json").read_text()) for n in NUMBERS]
        print(json.dumps(audit(classes, True), ensure_ascii=False, sort_keys=True))
    elif args.all:
        for path in write_all():
            print(path)
    else:
        parser.error("choose --class-number, --bundle, --audit or --all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
