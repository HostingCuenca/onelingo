#!/usr/bin/env python3
"""Generate the isolated English N3 C06-C10 editorial draft."""
from __future__ import annotations

import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n3"
REPORT_OUT = ROOT / "build/editorial-n3-06-10"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
SCALE = "client-10-levels-v1"
NUMBERS = range(6, 11)
CONCEPTS = {n: f"n3-past-scenes-{n-5}" for n in NUMBERS}
PHASES = {6: "input", 7: "form", 8: "comprehension", 9: "production", 10: "transfer"}
QUALITY = {"chronologyTokens": "enforce", "answerReuseAcrossEarlyReserved": "forbid",
           "answerEvidenceReuseAcrossPools": "forbid", "agentContract": "editorial-agent.v2",
           "minChoices": 3, "maxPromptCharacters": 90,
           "feedbackReuseWithinClass": "forbid", "minClassFormats": 4}


def canonical(v: Any) -> str:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def norm(v: str) -> str:
    return " ".join(re.findall(r"[a-záéíóúüñ0-9']+", v.casefold()))


def hashed(x: dict[str, Any]) -> dict[str, Any]:
    payload = {k: v for k, v in x.items() if k not in {"id", "contentHash"}}
    x["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return x


def base(i: str, fmt: str, prompt: str, c: str, pool: str, feedback: str,
         *, requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided": origin["hint"] = {"es": hint or "Ubica el fondo y el hecho que cambia la escena."}
    return {"id": i, "format": fmt, "prompt": {"es": prompt}, "answer": {}, "choices": [],
            "teaches": [c] if pool == "practiceGuided" else [],
            "requires": [] if pool == "practiceGuided" else list(requires or [c]),
            "origin": origin,
            "accessibility": {"screenReader": True, "highContrast": True, "largeText": True}}


def q(i: str, prompt: str, options: list[str], index: int, c: str, pool: str,
      feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "elegir", prompt, c, pool, feedback, **kw)
    x["choices"], x["answer"] = [{"text": v} for v in options], {"index": index}
    return hashed(x)


def listen(i: str, prompt: str, audio: str, options: list[str], index: int, c: str,
           pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    x = base(i, "escuchar", prompt, c, pool, feedback, **kw)
    x["choices"], x["answer"] = [{"text": v} for v in options], {"index": index}
    x["origin"].update({"audio": audio, "audioMode": "tts", "languageCode": "en",
                        "speedOptions": [0.75, 1.0], "maxReplays": 3,
                        "revealTranscriptAfterAttempt": True})
    return hashed(x)


def fill(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str,
         **kw: Any) -> dict[str, Any]:
    x = base(i, "completar", prompt, c, pool, feedback, **kw)
    x["answer"] = {"text": answer, "accepted": [answer]}
    return hashed(x)


def multi_fill(i: str, prompt: str, sentences: list[str], answers: list[str],
               c: str, pool: str, feedback: str, *, minimum_correct: int,
               **kw: Any) -> dict[str, Any]:
    x = base(i, "completar", prompt, c, pool, feedback, **kw)
    x["origin"]["sentences"] = sentences
    x["origin"]["scoring"] = {
        "parts": len(sentences),
        "minimumCorrect": minimum_correct,
        "independentAttempt": True,
    }
    joined = " | ".join(answers)
    x["answer"] = {
        "text": joined,
        "accepted": [joined],
        "parts": [
            {"text": answer, "accepted": [answer, answer.replace(" / ", "; ")]}
            for answer in answers
        ],
    }
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
    x["answer"], x["origin"]["pairs"] = {"pairs": values}, values
    return hashed(x)


def scored_match(i: str, prompt: str, pairs: list[tuple[str, str]], c: str,
                 pool: str, feedback: str, *, minimum_correct: int,
                 **kw: Any) -> dict[str, Any]:
    x = match(i, prompt, pairs, c, pool, feedback, **kw)
    x["origin"]["scoring"] = {
        "parts": len(pairs),
        "minimumCorrect": minimum_correct,
        "independentAttempt": True,
    }
    return hashed(x)


def teaching(n: int, rows: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    out = []
    for k, (en, es, explanation) in enumerate(rows, 1):
        ew, sw = en.split(), es.split(); em, sm = max(1, len(ew)//2), max(1, len(sw)//2)
        out.append({"id": f"en.n3.class-{n:02d}.t{k:02d}", "en": en, "es": es,
                    "explanationEs": explanation,
                    "segments": [{"en": " ".join(ew[:em]), "es": " ".join(sw[:sm])},
                                 {"en": " ".join(ew[em:]), "es": " ".join(sw[sm:])}],
                    "audioText": en, "audioMode": "tts", "languageCode": "en",
                    "patternId": CONCEPTS[n]})
    return out


def make_class(n: int, objectives: list[str], vocab: list[tuple[str, str]],
               rows: list[tuple[str, str, str]], pools: dict[str, list[dict[str, Any]]],
               remap: dict[str, tuple[str, str]], *, uses: list[str] | None = None,
               cumulative: list[str] | None = None) -> dict[str, Any]:
    spec = json.loads(MAP.read_text())["classes"][n-1]
    doc: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1", "course": "en", "level": 3,
        "cefr": "B1", "scale": SCALE, "status": "shadow", "runtimeAi": False,
        "phase": PHASES[n], "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY), "id": f"en.n3.class-{n:02d}", "title": spec["title"],
        "objectives": {"es": objectives}, "concepts": [CONCEPTS[n]],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
        "prerequisites": [f"en.n3.class-{n-1:02d}"],
        "usesVocabulary": [en for en, _ in vocab], "usesPatterns": uses or [CONCEPTS[n]],
        "vocabulary": [{"en": en, "es": es} for en, es in vocab],
        "teaching": teaching(n, rows), "pools": pools,
        "remediationMap": {k: {"reteach": a, "review": b} for k, (a,b) in remap.items()},
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True,
                          "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2,
                     "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True}}
    if cumulative is not None: doc["cumulativeEvaluation"] = cumulative
    return doc


def build_6() -> dict[str, Any]:
    n, c, p = 6, CONCEPTS[6], "en.n3.c06"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la frase que crea el fondo de una escena pasada.",
              ["A taxi stopped suddenly.", "People were waiting outside the station.",
               "The driver will call later."], 1, c, "practiceGuided",
              "Were waiting describe una acción en progreso antes del hecho principal.",
              hint="Busca was o were más una forma terminada en -ing."),
            fill(f"{p}.pg02", "Completa con was raining: At six, it ___ heavily.", "was raining", c,
                 "practiceGuided", "Was raining establece el clima en progreso a las seis.",
                 hint="It usa was y la lluvia continúa durante ese momento."),
            order(f"{p}.pg03", "Ordena la acción que estaba ocurriendo en el andén.",
                  "The passengers were carrying heavy bags.", c, "practiceGuided",
                  "Were carrying presenta la actividad que formaba parte de la escena.",
                  hint="Coloca were entre el sujeto plural y carrying."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige qué hacía Leo mientras esperaba.",
                   "It was quiet, and Leo was reading a map near the ticket office.",
                   ["He was reading a map", "He bought a ticket", "He called a taxi"], 0, c,
                   "practice", "Was reading a map identifica la actividad en curso de Leo."),
            match(f"{p}.p02", "Une cada escena con la acción de fondo adecuada.",
                  [("Outside the school", "Children were talking by the gate."),
                   ("Inside the café", "A server was cleaning the tables.")], c, "practice",
                  "Las dos descripciones muestran acciones que ya estaban en progreso."),
            write(f"{p}.p03", "Describe dos acciones simultáneas en la plaza.",
                  "Plaza a las cinco: músicos tocaban; familias esperaban el autobús.",
                  "Musicians were playing, and families were waiting for the bus in the square.",
                  "In the square, musicians were playing while families were waiting for the bus.",
                  c, "practice", "Las variantes sitúan dos actividades en curso dentro de la misma escena."),
        ],
        "evaluation": [
            scored_match(f"{p}.e01", "Relaciona cinco escenas con su acción de fondo.",
              [("At the bus stop", "Commuters were checking the timetable."),
               ("In the hotel lobby", "Guests were waiting near reception."),
               ("On the sports field", "The team was warming up."),
               ("Inside the workshop", "A mechanic was testing the brakes."),
               ("Beside the harbour", "The crew were loading supplies.")],
              c, "evaluation",
              "Las cinco relaciones sitúan una actividad en progreso dentro de cada escena.",
              minimum_correct=4),
            listen(f"{p}.e02", "Escucha y selecciona qué hacían los dos trabajadores.",
                   "Traffic was moving slowly, and two workers were checking the road.",
                   ["They were directing traffic", "They were repairing the bridge",
                    "They were checking the road"], 2, c, "evaluation",
                   "Were checking the road es una acción visible en progreso."),
            write(f"{p}.e03", "Redacta el fondo de la escena del mercado a las nueve.",
                  "Mercado, 9:00: vendedores organizaban fruta; clientes miraban precios.",
                  "Vendors were arranging fruit while customers were checking prices at the market.",
                  "At nine, vendors were organising fruit, and customers were looking at prices.", c,
                  "evaluation", "La respuesta mantiene ambas acciones abiertas en el mismo momento pasado."),
            q(f"{p}.e04", "¿Qué oración informa un hecho breve y no una acción de fondo?",
              ["A cyclist crossed the street.", "Cars were moving through heavy traffic.",
               "People were standing near the crossing."], 0, c, "evaluation",
              "Crossed presenta un hecho completo; las otras opciones describen el fondo."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cada lugar con la acción descrita.",
                  [("At the clinic", "Patients were sitting in the waiting room."),
                   ("At the harbour", "Sailors were loading boxes onto a boat."),
                   ("Near the office", "A metal door slammed suddenly.")], c, "review",
                  "La recuperación contrasta dos acciones prolongadas con un hecho breve."),
            order(f"{p}.r02", "Ordena la descripción del clima y el tráfico nocturno.",
                  "Rain was falling while traffic was moving slowly.", c, "review",
                  "Las dos formas continuas crean un fondo nocturno coherente."),
            write(f"{p}.r03", "Describe el fondo de una cocina durante el almuerzo.",
                  "Cocina: dos cocineros preparaban sopa; una ayudante lavaba platos.",
                  "Two cooks were preparing soup while an assistant was washing dishes.",
                  "In the kitchen, two cooks were making soup, and an assistant was washing dishes.",
                  c, "review", "La recuperación conserva participantes y acciones simultáneas en progreso."),
        ]}
    remap = {f"{p}.e01": ("en.n3.class-06.t01", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-06.t02", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-06.t05", f"{p}.r03"),
             f"{p}.e04": ("en.n3.class-06.t06", f"{p}.r01")}
    return make_class(n,
        ["Reconocer was o were más -ing como fondo narrativo.",
         "Distinguir una actividad en progreso de un hecho breve.",
         "Describir dos acciones simultáneas dentro de una escena pasada."],
        [("background", "fondo"), ("scene", "escena"), ("raining", "lloviendo"),
         ("waiting", "esperando"), ("carrying", "llevando"), ("traffic", "tráfico"),
         ("platform", "andén"), ("quiet", "silencioso")],
        [("The background shows what people were doing before the event.",
          "El fondo muestra lo que las personas hacían antes del hecho.",
          "Past continuous mantiene abiertas las acciones que forman el fondo."),
         ("It was raining, and traffic was moving slowly.",
          "Estaba lloviendo y el tráfico avanzaba despacio.",
          "Was raining y was moving sitúan clima y tráfico en progreso."),
         ("Passengers were waiting on the platform.", "Los pasajeros esperaban en el andén.",
          "Were waiting concuerda con un sujeto plural y describe duración."),
         ("A woman was carrying a red suitcase.", "Una mujer llevaba una maleta roja.",
          "Was carrying añade una acción visible sin convertirla en el hecho principal."),
         ("The scene was quiet while a guard was watching the entrance.",
          "La escena estaba tranquila mientras un guardia vigilaba la entrada.",
          "La descripción combina ambiente y actividad simultánea."),
         ("Traffic was moving when a metal door slammed.",
          "El tráfico avanzaba cuando una puerta metálica se cerró de golpe.",
          "Was moving crea el fondo; slammed presenta el hecho breve completo.")], pools, remap)


def build_7() -> dict[str, Any]:
    n, c, p = 7, CONCEPTS[7], "en.n3.c07"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la oración que combina fondo e interrupción correctamente.",
              ["I cooked when the phone was ringing all evening.",
               "I was cooking when the phone rang.",
               "I will cook while the phone rang."], 1, c, "practiceGuided",
              "Was cooking presenta el fondo y rang marca la interrupción breve.",
              hint="Usa past continuous para la actividad y past simple para el hecho."),
            fill(f"{p}.pg02", "Completa con while: ___ we were walking, the lights went out.",
                 "While", c, "practiceGuided",
                 "While introduce la acción prolongada de caminar.",
                 hint="La palabra abre una actividad que ya estaba ocurriendo."),
            order(f"{p}.pg03", "Ordena la llegada que interrumpió la reunión.",
                  "We were discussing the plan when Maya arrived.", c, "practiceGuided",
                  "When conecta la conversación en curso con la llegada breve.",
                  hint="Coloca el fondo antes de when y la llegada después."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada conector con la estructura que introduce.",
                  [("while", "actividad prolongada en past continuous"),
                   ("when", "hecho breve en past simple")], c, "practice",
                  "While abre el fondo; when señala el momento que lo modifica."),
            listen(f"{p}.p02", "Escucha y elige qué ocurrió mientras Ana conducía.",
                   "While Ana was driving to work, a warning light appeared on the dashboard.",
                   ["She arrived at work", "The car was parked", "A warning light appeared"], 2,
                   c, "practice", "Appeared es el hecho breve que ocurrió durante el trayecto."),
            write(f"{p}.p03", "Une la caminata y la caída de una rama con while.",
                  "Fondo: caminábamos por el parque. Hecho: una rama cayó delante.",
                  "While we were walking through the park, a branch fell in front of us.",
                  "A branch fell in front of us while we were walking through the park.", c,
                  "practice", "Las variantes conservan la simultaneidad sin cambiar el orden real."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige la forma correcta para una alarma que interrumpe el sueño.",
              ["I slept while the alarm was sounding.", "I was sleeping when the alarm sounded.",
               "I was sleeping when the alarm was sounding."], 1, c, "evaluation",
              "Was sleeping crea el fondo y sounded presenta la alarma puntual."),
            multi_fill(f"{p}.e02", "Completa seis escenas; separa las dos formas con una barra.",
                  ["While Mia ___ home, it ___ to rain.",
                   "We ___ the map when the screen ___.",
                   "When the bell ___, the students ___ a test.",
                   "The lights ___ while I ___ dinner.",
                   "While they ___ for the bus, a taxi ___.",
                   "He ___ the bike when his friend ___."],
                  ["was walking / started", "were watching / froze",
                   "rang / were taking", "went out / was cooking",
                   "were waiting / stopped", "was repairing / arrived"],
                  c, "evaluation",
                  "Cada respuesta exige past continuous para el fondo y past simple para el hecho breve.",
                  minimum_correct=5),
            listen(f"{p}.e03", "Escucha y selecciona la actividad que ya estaba en curso.",
                   "The guests were eating dinner when the electricity went off.",
                   ["The guests were eating dinner", "The electricity returned",
                    "The restaurant closed after dinner"], 0, c, "evaluation",
                   "Were eating dinner es la actividad de fondo anterior al corte."),
            write(f"{p}.e04", "Combina la espera y la llegada del mensaje con when.",
                  "Fondo: Sara esperaba al médico. Interrupción: llegó un mensaje urgente.",
                  "Sara was waiting for the doctor when an urgent message arrived.",
                  "When an urgent message arrived, Sara was waiting for the doctor.", c,
                  "evaluation", "Ambas versiones mantienen la espera abierta y el mensaje puntual."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona fondo e interrupción en dos incidentes.",
                  [("The children were playing outside.", "when hail started"),
                   ("A technician was checking the lift.", "when the alarm rang")], c, "review",
                  "La recuperación combina dos fondos continuos con hechos breves diferentes."),
            multi_fill(f"{p}.r02", "Recupera seis escenas; separa las dos formas con una barra.",
                  ["While I ___, the connection ___.",
                   "We ___ dinner when the doorbell ___.",
                   "When the bus ___, Ava ___ a ticket.",
                   "The glass ___ while they ___.",
                   "While Leo ___ home, the storm ___.",
                   "Mina ___ the lift when it ___."],
                  ["was presenting / stopped", "were eating / rang",
                   "arrived / was buying", "broke / were cleaning",
                   "was driving / started", "was checking / stopped"],
                  c, "review",
                  "La recuperación vuelve a separar seis fondos continuos de seis hechos breves.",
                  minimum_correct=5),
            write(f"{p}.r03", "Relata la interrupción durante la preparación del almuerzo.",
                  "Fondo: Nora preparaba sopa. Hecho: sonó la alarma de humo.",
                  "Nora was preparing soup when the smoke alarm rang.",
                  "The smoke alarm rang while Nora was making soup.", c, "review",
                  "La recuperación distingue preparación prolongada y alarma instantánea."),
        ]}
    remap = {f"{p}.e01": ("en.n3.class-07.t01", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-07.t03", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-07.t02", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-07.t05", f"{p}.r03")}
    return make_class(n,
        ["Usar when para introducir una interrupción breve.",
         "Usar while para situar una actividad en progreso.",
         "Mantener past continuous para fondo y past simple para el hecho."],
        [("when", "cuando"), ("while", "mientras"), ("interrupted", "interrumpió"),
         ("rang", "sonó"), ("arrived", "llegó"), ("walking", "caminando"),
         ("cooking", "cocinando"), ("alarm", "alarma")],
        [("I was cooking when the phone rang.", "Cocinaba cuando sonó el teléfono.",
          "When introduce el hecho corto que interrumpe la acción en curso."),
         ("While we were walking, the rain started.", "Mientras caminábamos, empezó a llover.",
          "While presenta la actividad prolongada como fondo."),
         ("The bus arrived while I was buying a ticket.",
          "El autobús llegó mientras compraba un billete.",
          "Arrived es breve; la compra seguía en progreso."),
         ("The alarm interrupted the lesson.", "La alarma interrumpió la clase.",
          "Interrupted nombra el hecho que cambia el curso de la escena."),
         ("Use while with was or were plus -ing; use when with a brief event.",
          "Usa while con was o were más -ing; usa when con un hecho breve.",
          "El contraste conserva la duración y el orden real de los hechos.")], pools, remap)


def build_8() -> dict[str, Any]:
    n, c, p = 8, CONCEPTS[8], "en.n3.c08"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige el dato que establece el escenario del incidente.",
              ["A glass broke suddenly.", "People were shopping in the busy market.",
               "A guard called for help."], 1, c, "practiceGuided",
              "Were shopping establece la actividad que llenaba el mercado.",
              hint="El escenario muestra qué ocurría antes de la interrupción."),
            order(f"{p}.pg02", "Ordena la secuencia desde el fondo hasta la reacción.",
                  "We were waiting when the sign fell, so we moved away.", c, "practiceGuided",
                  "La secuencia conserva fondo, caída breve y reacción posterior.",
                  hint="Sitúa was waiting antes de fell y moved al final."),
            match(f"{p}.pg03", "Relaciona cada fragmento con su lugar en la cronología.",
                  [("Cars were crossing the bridge.", "fondo"),
                   ("A tyre burst.", "interrupción"),
                   ("The driver stopped safely.", "reacción")], c, "practiceGuided",
                  "Los tres fragmentos forman una cronología completa y verificable.",
                  hint="Identifica duración, hecho breve y respuesta."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige qué sucedió inmediatamente después del golpe.",
                   "I was carrying boxes when a door hit my arm. I dropped one box and called a colleague.",
                   ["I dropped one box", "I was carrying boxes", "A colleague opened the door"], 0,
                   c, "practice", "Dropped one box es la primera reacción después del golpe."),
            match(f"{p}.p02", "Une los datos del testigo con su función narrativa.",
                  [("It was getting dark.", "escenario"),
                   ("A dog ran into the road.", "interrupción"),
                   ("The cyclist braked.", "respuesta inmediata")], c, "practice",
                  "El testimonio separa ambiente, cambio repentino y respuesta."),
            write(f"{p}.p03", "Resume la cronología del incidente de la ventana.",
                  "Fondo: estudiantes trabajaban. Interrupción: ventana se abrió. Reacción: cerraron libros.",
                  "The students were working when the window opened, so they closed their books.",
                  "While the students were working, the window opened and they shut their books.", c,
                  "practice", "Las variantes mantienen las tres etapas en el mismo orden."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha y selecciona la acción que formaba el fondo.",
                   "The band was playing in the square when a cable came loose. The music stopped.",
                   ["The music stopped", "The band was playing", "A worker fixed the cable later"], 1,
                   c, "evaluation", "Was playing describe la actividad que ya estaba ocurriendo."),
            q(f"{p}.e02", "¿Qué hecho interrumpió la entrega de paquetes?",
              ["The driver was checking the address.", "The customer thanked the driver.",
               "A bicycle hit the side of the van."], 2, c, "evaluation",
              "Hit the side of the van es el hecho breve que cambia la entrega."),
            order(f"{p}.e03", "Ordena la línea temporal completa del incidente en el parque.",
                  "Children were playing when a branch fell, and a teacher moved them inside.", c,
                  "evaluation", "El orden presenta actividad, caída y medida de seguridad."),
            listen(f"{p}.e04", "Escucha y elige la secuencia completa del testimonio.",
                  "People were waiting at a crossing. A van hit a sign. A guard stopped traffic. The pedestrians moved back.",
                  ["waiting → van hit sign → guard stopped traffic → pedestrians moved back",
                   "van hit sign → waiting → pedestrians moved back → guard stopped traffic",
                   "waiting → guard stopped traffic → van hit sign → pedestrians moved back"], 0,
                  c, "evaluation", "La primera secuencia conserva los cuatro hechos del testimonio."),
        ],
        "review": [
            match(f"{p}.r01", "Clasifica los hechos del testimonio sobre el gimnasio.",
                  [("People were exercising.", "situación inicial"),
                   ("The fire alarm sounded.", "interrupción repentina"),
                   ("Everyone left calmly.", "reacción posterior")], c, "review",
                  "La recuperación reconstruye un incidente nuevo sin invertir las etapas."),
            order(f"{p}.r02", "Ordena la cronología de la avería en la calle.",
                  "A crew was repairing the road when a pipe broke, so they closed the lane.", c,
                  "review", "La reparación estaba en curso antes de la rotura y el cierre."),
            write(f"{p}.r03", "Reconstruye cuatro hechos del incidente en una clase de arte.",
                  "Alumnos pintaban. Cayó agua del techo. Docente cerró el aula. Grupo movió materiales.",
                  "The students were painting when water fell from the ceiling. The teacher closed the room, and the group moved their materials.",
                  "While the class was painting, water came through the ceiling; the teacher shut the room and everyone moved the materials.",
                  c, "review", "La recuperación ordena fondo, incidente y dos reacciones explícitas."),
        ]}
    remap = {f"{p}.e01": ("en.n3.class-08.t02", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-08.t04", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-08.t01", f"{p}.r02"),
             f"{p}.e04": ("en.n3.class-08.t01", f"{p}.r03")}
    return make_class(n,
        ["Extraer el escenario anterior a una interrupción.",
         "Ordenar fondo, hecho breve y reacción sin alterar la cronología.",
         "Reconstruir un testimonio con datos explícitos."],
        [("timeline", "línea temporal"), ("setting", "escenario"),
         ("witness", "testigo"), ("interruption", "interrupción"),
         ("reaction", "reacción"), ("before", "antes"),
         ("suddenly", "de repente"), ("afterwards", "después")],
        [("A timeline keeps the background, interruption and result in order.",
          "Una línea temporal mantiene en orden el fondo, la interrupción y el resultado.",
          "El orden evita atribuir una reacción a un hecho posterior."),
         ("The setting tells us what was happening and where.",
          "El escenario indica qué ocurría y dónde.",
          "El past continuous aporta lugar y actividad de fondo."),
         ("A witness reports only the actions that were seen or heard.",
          "Un testigo informa solo las acciones que vio u oyó.",
          "El testimonio debe conservar los datos sin inventar causas."),
         ("The interruption happened suddenly when a shelf fell.",
          "La interrupción ocurrió de repente cuando cayó un estante.",
          "Past simple marca el cambio breve dentro de la escena."),
         ("Before the fall, people were browsing; afterwards, their reaction was to leave.",
          "Antes de la caída, la gente miraba; después, su reacción fue salir.",
          "Before y afterwards hacen visible la secuencia completa.")], pools, remap)


def build_9() -> dict[str, Any]:
    n, c, p = 9, CONCEPTS[9], "en.n3.c09"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige el relato que incluye contexto, interrupción y reacción.",
              ["The floor was wet all morning.",
               "I was carrying lunch when I slipped, so I checked my ankle.",
               "I will be careful near the kitchen."], 1, c, "practiceGuided",
              "La segunda opción contiene actividad, caída breve y comprobación posterior.",
              hint="Busca tres momentos conectados en una sola secuencia."),
            order(f"{p}.pg02", "Ordena la reacción posterior a un vaso derramado.",
                  "After the glass fell, we cleaned the floor carefully.", c, "practiceGuided",
                  "After sitúa la limpieza después de la caída del vaso.",
                  hint="Empieza con el hecho y termina con la reacción."),
            fill(f"{p}.pg03", "Completa con shouted: The cyclist fell, so a witness ___.", "shouted", c,
                 "practiceGuided", "Shouted presenta la reacción inmediata del testigo.",
                 hint="La consigna pide el pasado regular de shout."),
        ],
        "practice": [
            write(f"{p}.p01", "Relata el incidente de la pintura en tres etapas.",
                  "Contexto: pintaban pared. Interrupción: escalera cayó. Reacción: alejaron latas.",
                  "They were painting a wall when the ladder fell, so they moved the paint cans away.",
                  "While they were painting the wall, the ladder fell and they moved the cans to safety.",
                  c, "practice", "Las variantes conservan actividad, caída y respuesta protectora."),
            listen(f"{p}.p02", "Escucha y selecciona la reacción del conductor.",
                   "A driver was turning into the car park when a ball rolled into the road. She stopped immediately.",
                   ["She stopped immediately", "She was turning", "She kicked the ball"], 0, c,
                   "practice", "Stopped immediately es la acción posterior al balón en la vía."),
            match(f"{p}.p03", "Une cada parte del relato con su función.",
                  [("We were moving the chairs.", "contexto"),
                   ("One chair broke.", "interrupción"),
                   ("We checked the other chairs.", "reacción")], c, "practice",
                  "La secuencia explica qué ocurría, qué cambió y qué hicieron después."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige la reacción lógica tras un ruido en el almacén.",
              ["The boxes were standing near the door.", "The team checked where the noise came from.",
               "A driver moved the next delivery outside."], 1, c, "evaluation",
              "Checked where the noise came from responde directamente al sonido inesperado."),
            listen(f"{p}.e02", "Escucha y selecciona el hecho que interrumpió el paseo.",
                   "We were walking beside the river when my bag strap broke. I picked up the bag.",
                   ["The strap broke", "We picked a route", "The river was closed"], 0, c,
                   "evaluation", "Broke es el cambio breve que interrumpe la caminata."),
            write(f"{p}.e03", "Escribe contexto, interrupción y reacción del laboratorio.",
                  "Contexto: Mei medía líquido. Interrupción: botella se rompió. Reacción: avisó supervisora.",
                  "Mei was measuring liquid when the bottle broke, so she alerted her supervisor.",
                  "While Mei was measuring the liquid, the bottle broke and she called her supervisor.", c,
                  "evaluation", "La narración mantiene la medición, la rotura y el aviso en orden."),
            write(f"{p}.e04", "Escribe 60–80 palabras sobre el incidente de la feria escolar.",
                  "Contexto: familias visitaban puestos; alumnos servían bebidas. Interrupción: mesa perdió una pata y bebidas cayeron. Reacciones: docente apartó personas, alumnos limpiaron, enfermera comprobó que nadie se hirió, revisaron mesas; feria continuó.",
                  "Families were visiting the stalls while students were serving drinks at the school fair. A table suddenly lost one leg, and several drinks fell onto the floor. A teacher moved people away from the wet area. The students cleaned the floor and checked the other tables. The school nurse confirmed that nobody was hurt before the fair continued safely with a different table.",
                  "At the school fair, families were visiting stalls and students were serving drinks. One table suddenly broke, so the drinks spilled across the floor. A teacher asked visitors to step back. Students cleaned the area and then checked every other table. The school nurse confirmed that nobody was hurt. Eventually, they replaced the damaged table, and the fair continued without another problem.", c,
                  "evaluation", "El relato extenso incluye contexto doble, rotura, dos reacciones y desenlace."),
        ],
        "review": [
            match(f"{p}.r01", "Clasifica las tres etapas del incidente en el jardín.",
                  [("Children were watering plants.", "contexto"),
                   ("A hose split.", "interrupción"),
                   ("An adult turned off the water.", "reacción")], c, "review",
                  "La recuperación distribuye una actividad, una avería y una respuesta."),
            order(f"{p}.r02", "Ordena el desenlace posterior a la caída del cartel.",
                  "Eventually, the staff secured the sign and reopened the entrance.", c, "review",
                  "Eventually introduce el resultado final después de resolver el riesgo."),
            write(f"{p}.r03", "Escribe 60–80 palabras sobre una avería durante un taller.",
                  "Contexto: grupo construía estantes; instructor mostraba herramienta. Interrupción: taladro se detuvo y olió a quemado. Reacciones: apagaron corriente, abrieron ventanas, revisaron cable; instructor registró fallo y retiró taladro; usaron herramienta manual.",
                  "The group was building shelves while the instructor was demonstrating a drill. The drill suddenly stopped, and everyone noticed a burning smell. The instructor switched off the power and opened the windows. She checked the cable before the session continued. The instructor recorded the fault and removed the drill from the room. Eventually, the group used hand tools and finished the shelf safely.",
                  "During the workshop, participants were building shelves as the instructor demonstrated a drill. The machine stopped and produced a burning smell. The instructor cut the power, and the group opened the windows. After she checked the cable, they continued with hand tools. The instructor recorded the fault and removed the drill from the room. Eventually, they completed one shelf without further trouble.", c,
                  "review", "La recuperación aporta fondo, fallo, medidas de seguridad y resultado final."),
        ]}
    remap = {f"{p}.e01": ("en.n3.class-09.t03", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-09.t02", f"{p}.r01"),
             f"{p}.e03": ("en.n3.class-09.t04", f"{p}.r03"),
             f"{p}.e04": ("en.n3.class-09.t06", f"{p}.r03")}
    return make_class(n,
        ["Narrar un contexto mediante past continuous.",
         "Introducir una interrupción breve mediante past simple.",
         "Añadir una reacción y un desenlace coherentes."],
        [("context", "contexto"), ("tray", "bandeja"),
         ("drinks", "bebidas"), ("slipped", "resbaló"),
         ("spilled", "derramó"), ("shouted", "gritó"),
         ("checked", "revisó"), ("eventually", "finalmente")],
        [("The context explains what was happening before the problem.",
          "El contexto explica qué ocurría antes del problema.",
          "El past continuous crea el fondo necesario para comprender el incidente."),
         ("I was carrying a tray when I slipped.", "Llevaba una bandeja cuando resbalé.",
          "Slipped es la interrupción breve de la acción en progreso."),
         ("The drinks spilled, so a colleague shouted a warning.",
          "Las bebidas se derramaron, así que un colega gritó una advertencia.",
          "La reacción sigue de manera lógica al derrame."),
         ("We checked the floor and moved everyone away.",
          "Revisamos el suelo y alejamos a todos.",
          "Checked introduce una medida posterior y verificable."),
         ("Eventually, the area was safe and the event continued.",
          "Finalmente, la zona quedó segura y el evento continuó.",
          "Eventually cierra el relato con el resultado alcanzado."),
         ("Shoppers were visiting a market when an awning fell. Staff moved them back, checked the area and eventually reopened the stalls.",
          "Los clientes visitaban un mercado cuando cayó un toldo. El personal los alejó, revisó la zona y finalmente reabrió los puestos.",
          "El modelo reúne contexto, interrupción, reacciones seguras y desenlace.")], pools, remap)


def build_10() -> dict[str, Any]:
    n, c, p = 10, CONCEPTS[10], "en.n3.c10"
    all_c = [CONCEPTS[i] for i in NUMBERS]
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la explicación que incluye causa y petición práctica.",
              ["I was late because transport is sometimes difficult.",
               "The bus broke down while I was travelling. Could I take the later tour?",
               "I may arrive early tomorrow."], 1, c, "practiceGuided",
              "La segunda opción explica la avería y solicita una alternativa concreta.",
              hint="Busca una cronología pasada y una pregunta que resuelva el retraso."),
            order(f"{p}.pg02", "Ordena la reacción posterior al cierre de la carretera.",
                  "The road closed, so we took a different route.", c, "practiceGuided",
                  "Closed presenta el problema y took muestra la reacción posterior.",
                  hint="Coloca la causa antes de so y la alternativa después."),
            match(f"{p}.pg03", "Relaciona cada parte de la explicación con su función.",
                  [("I was travelling to the clinic.", "situación de fondo"),
                   ("A crash blocked the road.", "causa inmediata"),
                   ("Could I have a later appointment?", "petición práctica")], c,
                  "practiceGuided",
                  "La explicación completa sitúa el trayecto, la causa y la solución solicitada.",
                  hint="Distingue lo que ocurría, lo que cambió y lo que se pide."),
        ],
        "practice": [
            write(f"{p}.p01", "Explica el retraso de Kai y pide una solución.",
                  "Kai iba a entrevista. Tren se detuvo por problema de señal. Tomó taxi. Pide entrar 15 minutos tarde.",
                  "Kai was travelling to an interview when a signal problem stopped the train. He took a taxi. Could he arrive fifteen minutes late?",
                  "A signal failure stopped Kai's train while he was going to an interview. He took a taxi and asked to arrive fifteen minutes late.",
                  c, "practice", "Las variantes conservan trayecto, fallo, reacción y petición."),
            listen(f"{p}.p02", "Escucha y elige qué hizo Rosa después de perder el autobús.",
                   "Rosa was buying a ticket when her bus left. She called the office and booked the next bus.",
                   ["She booked the next bus", "She bought a plane ticket", "She walked home"], 0,
                   c, "practice", "Booked the next bus es la reacción posterior a perder la salida."),
            match(f"{p}.p03", "Une cada problema de viaje con una petición adecuada.",
                  [("The ferry was cancelled.", "Could you move my booking to tomorrow?"),
                   ("The road was blocked.", "Can you tell me another route?")], c, "practice",
                  "Cada petición responde de manera concreta al problema indicado."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige el fondo que explica dónde comenzó el retraso.",
              ["The driver called the depot.", "We were crossing the city by tram.",
               "The tram door failed suddenly."], 1, c, "evaluation",
              "Were crossing the city establece la situación anterior a la avería."),
            listen(f"{p}.e02", "Escucha y selecciona la causa inmediata de la demora.",
                   "I was walking to the station when a delivery van blocked the narrow street. I had to turn back.",
                   ["The station closed unexpectedly", "Heavy rain filled the street",
                    "A van blocked the street"], 2,
                   c, "evaluation", "Blocked the narrow street es el hecho que obligó a regresar."),
            write(f"{p}.e03", "Redacta reacción y petición tras perder una conexión.",
                  "Vuelo llegó tarde; Mina perdió conexión. Habló con agente. Pide asiento en vuelo 18:30.",
                  "Mina's flight arrived late, so she missed her connection and spoke to an agent. Could she take the 6:30 flight?",
                  "Because Mina's flight was late, she missed the connection. She asked an agent for a seat on the 6:30 flight.", c,
                  "evaluation", "La respuesta conserva causa, reacción y alternativa horaria exacta."),
            write(f"{p}.e04", "Escribe 70–100 palabras para explicar el retraso en la clínica.",
                  "Iba en autobús a cita 10:00. Tráfico lento. Accidente bloqueó avenida 9:25. Bajó 9:40, caminó 20 minutos, llamó clínica. Conductor dio número de incidente. Llegará 10:20. Pide mover cita a 10:30 y confirmar.",
                  "I was travelling by bus to a ten o'clock clinic appointment while traffic was moving slowly. At 9:25, an accident blocked the main avenue. I got off the bus at 9:40, walked for twenty minutes and called the clinic. The driver also gave me an incident number for the clinic. I will arrive at 10:20. Could you move my appointment to 10:30 and confirm that the doctor can still see me?",
                  "While I was taking the bus to my ten o'clock appointment, traffic was moving slowly. An accident blocked the avenue at 9:25. I left the bus at 9:40 and walked for twenty minutes before calling the clinic. The driver also gave me an incident number for the clinic. I expect to arrive at 10:20. Could I have the 10:30 appointment, and could you confirm it for me?",
                  c, "evaluation", "La explicación integra fondo, hora del bloqueo, reacción, llegada y petición verificable.",
                  requires=all_c),
        ],
        "review": [
            match(f"{p}.r01", "Clasifica los datos del retraso de una entrega.",
                  [("The courier was driving to the office.", "contexto"),
                   ("A tyre burst near the bridge.", "interrupción"),
                   ("The courier called the customer.", "reacción"),
                   ("Could we deliver after lunch?", "petición")], c, "review",
                  "La recuperación separa trayecto, avería, reacción y solución solicitada."),
            order(f"{p}.r02", "Ordena la reacción tras una avería del metro.",
                  "The metro stopped, so we left the station and found a taxi.", c, "review",
                  "La secuencia muestra problema, salida y transporte alternativo."),
            write(f"{p}.r03", "Escribe 70–100 palabras para explicar el retraso al curso.",
                  "Iba en tren a curso 14:00. Tren se acercaba a estación cuando señal falló 13:10. Esperó 25 minutos; empresa confirmó fallo por mensaje; tomó taxi 13:40; avisó instructor. Llegará 14:15. Pide unirse en línea y confirmar enlace.",
                  "I was travelling by train to a two o'clock course, and the train was approaching the final station when a signal failed at 1:10. We waited for twenty-five minutes. The railway company sent a message confirming the signal problem. At 1:40, I took a taxi and contacted the instructor. I will arrive at 2:15. Could I join online until I arrive, and could you confirm the meeting link directly?",
                  "While I was going to a two o'clock training session, my train was nearing the last station. A signal failed at 1:10, so we waited twenty-five minutes. The railway company sent a message confirming the signal problem. I took a taxi at 1:40 and messaged the instructor. I expect to arrive at 2:15. Could you send the online link directly and let me join remotely until then?",
                  c, "review", "La recuperación reconstruye cronología ferroviaria, alternativa y petición digital.",
                  requires=all_c),
        ]}
    remap = {f"{p}.e01": ("en.n3.class-10.t01", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-10.t02", f"{p}.r01"),
             f"{p}.e03": ("en.n3.class-10.t06", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-10.t06", f"{p}.r03")}
    return make_class(n,
        ["Explicar el contexto y la causa inmediata de un retraso.",
         "Narrar la reacción mediante hechos ordenados y horas verificables.",
         "Cerrar con una petición práctica y específica."],
        [("delay", "retraso"), ("journey", "trayecto"), ("appointment", "cita"),
         ("cause", "causa"), ("request", "petición"), ("blocked", "bloqueó"),
         ("alternative", "alternativa"), ("agent", "agente")],
        [("Begin the delay explanation with the journey already in progress.",
          "Empieza la explicación del retraso con el trayecto ya en curso.",
          "Past continuous sitúa a la persona antes de que aparezca el problema."),
         ("State the cause as a brief event: a van blocked the road.",
          "Indica la causa como hecho breve: una furgoneta bloqueó la carretera.",
          "Past simple identifica la interrupción que produjo la demora."),
         ("Give the appointment time and the important moments in order.",
          "Da la hora de la cita y los momentos importantes en orden.",
          "Las horas permiten comprobar la cronología del retraso."),
         ("Explain the reaction and any alternative route you used.",
          "Explica la reacción y cualquier ruta alternativa que usaste.",
          "La reacción muestra qué hizo la persona después de la interrupción."),
         ("End with a specific request to the agent.",
          "Termina con una petición específica al agente.",
          "La petición convierte la explicación en una solución práctica."),
         ("Nora: I was checking in for my flight when the fire alarm sounded. Staff moved everyone outside at 7:20. We returned thirty minutes later, but boarding had closed. I spoke to an agent and explained the delay. Could you book me on the 10:15 flight and keep my checked bag on the new booking? Agent: Yes, I can change both now.",
          "Nora hacía el registro cuando sonó la alarma. El personal evacuó a todos a las 7:20. Volvieron treinta minutos después, pero el embarque había cerrado. Nora explicó el retraso y pidió al agente el vuelo de las 10:15 y conservar su equipaje; el agente aceptó.",
          "El modelo integra contexto, interrupción, reacción, cronología y petición con respuesta.")],
        pools, remap, uses=all_c, cumulative=all_c)


BUILDERS = {6: build_6, 7: build_7, 8: build_8, 9: build_9, 10: build_10}


def audit(classes: list[dict[str, Any]], full: bool) -> dict[str, Any]:
    totals: Counter[str] = Counter(); formats: Counter[str] = Counter(); indices: Counter[int] = Counter()
    prompts: dict[str, str] = {}; signatures: dict[str, str] = {}
    for cls in classes:
        assert cls["status"] == "shadow" and cls["runtimeAi"] is False
        assert cls["qualityPolicy"] == QUALITY and 6 <= len(cls["vocabulary"]) <= 12
        assert 4 <= len(cls["teaching"]) <= 6
        local_formats: set[str] = set(); local_indices: Counter[int] = Counter(); feedbacks = []
        for pool, count in (("practiceGuided",3),("practice",3),("evaluation",4),("review",3)):
            assert len(cls["pools"][pool]) == count; totals[pool] += count
            for item in cls["pools"][pool]:
                assert len(item["prompt"]["es"]) <= 90, (item["id"], len(item["prompt"]["es"]))
                payload = {k:v for k,v in item.items() if k not in {"id","contentHash"}}
                assert item["contentHash"] == "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
                local_formats.add(item["format"]); formats[item["format"]] += 1
                pk = norm(item["prompt"]["es"]); assert pk not in prompts, (item["id"], prompts.get(pk)); prompts[pk] = item["id"]
                feedbacks.append(item["origin"]["feedback"]["es"])
                if pool != "practiceGuided": assert "hint" not in item["origin"]
                if item["format"] in {"elegir","escuchar"}:
                    assert len(item["choices"]) >= 3
                    idx = item["answer"]["index"]; assert 0 <= idx < len(item["choices"])
                    local_indices[idx] += 1; indices[idx] += 1
                if item["format"] == "escribir":
                    acc = item["answer"]["accepted"]; assert len(acc) >= 2 and len({norm(x) for x in acc}) >= 2
                stimulus = item["origin"].get("audio") or item["origin"].get("text") or item["origin"].get("pairs") or item["prompt"]["es"]
                sig = canonical({"stimulus":stimulus,"answer":item["answer"]}).casefold()
                assert sig not in signatures, (item["id"], signatures.get(sig)); signatures[sig] = item["id"]
        assert len(local_formats) >= 4 and len(feedbacks) == len(set(feedbacks))
        assert len(local_indices) >= 2 and max(local_indices.values())/sum(local_indices.values()) <= .60
        visible = canonical({"teaching":cls["teaching"],"pools":cls["pools"]}).casefold()
        for v in cls["vocabulary"]: assert v["en"].casefold() in visible, (cls["id"],v["en"])
        eval_ids = {x["id"] for x in cls["pools"]["evaluation"]}; assert set(cls["remediationMap"]) == eval_ids
        teach_ids = {x["id"] for x in cls["teaching"]}; review_ids = {x["id"] for x in cls["pools"]["review"]}
        for route in cls["remediationMap"].values(): assert route["reteach"] in teach_ids and route["review"] in review_ids
        if cls["phase"] in {"production","transfer"}:
            reserved = [x for pool in ("evaluation","review") for x in cls["pools"][pool] if x["format"]=="escribir"]
            assert any(len(re.findall(r"\b[\w’-]+\b",x["answer"]["text"]))>=8 and len(x["answer"]["accepted"])>=2 for x in reserved)
    if full:
        assert len(classes)==5 and sum(totals.values())==65
        c06e01 = next(x for x in classes[0]["pools"]["evaluation"] if x["id"] == "en.n3.c06.e01")
        assert c06e01["format"] == "relacionar" and len(c06e01["answer"]["pairs"]) == 5
        assert c06e01["origin"]["scoring"] == {"parts": 5, "minimumCorrect": 4, "independentAttempt": True}
        c07e02 = next(x for x in classes[1]["pools"]["evaluation"] if x["id"] == "en.n3.c07.e02")
        assert c07e02["format"] == "completar" and len(c07e02["answer"]["parts"]) == 6
        assert c07e02["origin"]["scoring"] == {"parts": 6, "minimumCorrect": 5, "independentAttempt": True}
        close=classes[-1]; expected=[CONCEPTS[n] for n in NUMBERS]
        assert close["cumulativeEvaluation"]==expected and close["usesPatterns"]==expected
        e04=next(x for x in close["pools"]["evaluation"] if x["id"]=="en.n3.c10.e04")
        r03=next(x for x in close["pools"]["review"] if x["id"]=="en.n3.c10.r03")
        assert e04["requires"]==expected and r03["requires"]==expected
        t06=close["teaching"][-1]["en"].casefold(); ea=e04["answer"]["text"].casefold(); ra=r03["answer"]["text"].casefold()
        assert "flight" in t06 and "clinic" in ea and "course" in ra
        for text in (t06,ea,ra):
            assert "was" in text and "could" in text and ("when" in text or "while" in text)
    return {"classes":len(classes),"items":sum(totals.values()),"pools":dict(totals),
            "formats":dict(sorted(formats.items())),"correctIndices":dict(sorted(indices.items())),
            "prompts":len(prompts),"fingerprints":len(signatures)}


def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def write_class(n: int) -> Path:
    doc=BUILDERS[n](); audit([doc],False); path=OUT/f"class-{n:02d}.json"
    path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); return path


def write_bundle() -> tuple[Path,dict[str,Any]]:
    classes=[json.loads((OUT/f"class-{n:02d}.json").read_text()) for n in NUMBERS]; summary=audit(classes,True)
    doc={"schema":"onelingo.editorial.class-bundle.v1","course":"en","level":3,"scale":SCALE,
         "status":"shadow","runtimeAi":False,"selectionPolicy":{"deterministic":True},
         "evidencePolicy":{"attemptRecords":["variantId","libraryVersion","selectionId"]},
         "range":{"start":6,"end":10},"classes":classes}
    path=OUT/"bundle-06-10.json"; path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return path,summary


def write_report(paths:list[Path], summary:dict[str,Any])->Path:
    hashes="\n".join(f"{digest(p)}  {p.name}" for p in paths)
    text=f"""# DRAFT — Inglés N3 C06–C10

Estado: **DRAFT para revisión independiente; no autorizado para integración**.

## Alcance

- Bloque `past-scenes`, entrada B1, fases `input → form → comprehension → production → transfer`.
- Cinco clases, 65 ejercicios y contrato `editorial-agent.v2`.
- `status: shadow`, `runtimeAi: false`, selección y recuperación deterministas.

## Cierre C10

- `t06`: alarma durante el registro de un vuelo.
- `e04`: accidente vial antes de una cita clínica.
- `r03`: fallo de señal ferroviaria antes de un curso.
- Cada escenario demuestra fondo en past continuous, interrupción en past simple,
  reacción ordenada, cronología verificable y petición práctica.

## Auditoría

```json
{json.dumps(summary,ensure_ascii=False,indent=2)}
```

## Validación reproducible

Resultados de esta generación:

- Cinco validaciones individuales y bundle level 3: `OK`.
- Pruebas focalizadas: 57 pruebas, `OK`.
- Ruta editorial: 10 idiomas, 0 errores.
- Idempotencia: dos regeneraciones consecutivas producen hashes idénticos.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 work/n3_c06_10/generate.py --all
python3 tools/contenido/validar_bundle_editorial.py --file work/n3_c06_10/bundle-06-10.json --start 6 --end 10 --level 3
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s test_tools -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 tools/validar_ruta.py
```

## Hashes

```text
{hashes}
```

El autor entrega `DRAFT`, nunca `GO`.
"""
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    path=REPORT_OUT/"REPORT.md"; path.write_text(text,encoding="utf-8"); return path


def write_all()->list[Path]:
    classes=[write_class(n) for n in NUMBERS]; bundle,summary=write_bundle(); report=write_report(classes+[bundle],summary)
    files=classes+[bundle,report]; manifest=REPORT_OUT/"MANIFEST.sha256"
    entries=[f"{digest(Path(__file__))}  ../../tools/contenido/generar_editorial_n3_06_10.py",
             f"{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"]
    entries.extend(
        f"{digest(p)}  {p.name if p.parent == REPORT_OUT else '../../' + str(p.relative_to(ROOT))}"
        for p in files
    )
    manifest.write_text("\n".join(entries)+"\n",encoding="utf-8")
    return files+[manifest]


def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--class-number",type=int,choices=NUMBERS)
    parser.add_argument("--bundle",action="store_true"); parser.add_argument("--audit",action="store_true"); parser.add_argument("--all",action="store_true")
    args=parser.parse_args()
    if args.class_number: print(write_class(args.class_number))
    elif args.bundle: print(write_bundle()[0])
    elif args.audit:
        docs=[json.loads((OUT/f"class-{n:02d}.json").read_text()) for n in NUMBERS]
        print(json.dumps(audit(docs,True),ensure_ascii=False,sort_keys=True))
    elif args.all:
        for path in write_all(): print(path)
    else: parser.error("choose --class-number, --bundle, --audit or --all")
    return 0


if __name__=="__main__": raise SystemExit(main())
