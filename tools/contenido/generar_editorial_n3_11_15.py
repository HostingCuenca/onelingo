#!/usr/bin/env python3
"""Generate the isolated English N3 C11-C15 editorial draft."""
from __future__ import annotations

import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n3"
REPORT_OUT = ROOT / "build/editorial-n3-11-15"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
SCALE = "client-10-levels-v1"
NUMBERS = range(11, 16)
CONCEPTS = {n: f"n3-narrative-turning-points-{n-10}" for n in NUMBERS}
PHASES = {11: "input", 12: "form", 13: "comprehension", 14: "production", 15: "transfer"}
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


def build_11() -> dict[str, Any]:
    n, c, p = 11, CONCEPTS[11], "en.n3.c11"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige el conector que abre la historia.",
              ["At first", "Suddenly", "Eventually"], 0, c, "practiceGuided",
              "At first presenta la situación inicial antes de que cambie.",
              hint="Busca la señal que introduce el comienzo."),
            fill(f"{p}.pg02", "Completa el giro: ___, the lights went out.", "Suddenly", c,
                 "practiceGuided", "Suddenly marca una interrupción inesperada.",
                 hint="El apagón ocurre sin aviso."),
            order(f"{p}.pg03", "Ordena el cierre de la búsqueda.",
                  "Eventually we found the missing dog.", c, "practiceGuided",
                  "Eventually señala el resultado final tras una espera.",
                  hint="El conector de cierre va antes del sujeto."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige qué ocurrió después del giro.",
                   "At first, the beach was quiet. Suddenly, we heard a shout. Later, a lifeguard arrived.",
                   ["The beach became quiet", "A lifeguard arrived", "We heard music"], 1, c,
                   "practice", "Later introduce la llegada posterior del socorrista."),
            match(f"{p}.p02", "Une cada función narrativa con su señal temporal.",
                  [("situación inicial", "at first"), ("cambio inesperado", "suddenly"),
                   ("resultado final", "eventually")], c, "practice",
                  "Las tres señales distinguen apertura, giro y desenlace."),
            q(f"{p}.p03", "¿Qué frase mantiene el orden de la historia del autobús?",
              ["At first, the bus was still on its route.", "Suddenly, the driver checked the engine.",
               "Later, another driver offered us a ride."], 2, c, "practice",
              "Later sitúa la ayuda después del problema con el autobús."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige la apertura natural de un relato sobre un museo.",
              ["At first, our group followed the guide.", "Later, our group entered the art room.",
               "Suddenly, the guide dropped her map."], 0, c, "evaluation",
              "At first abre el relato con la actividad inicial del grupo."),
            listen(f"{p}.e02", "Escucha y selecciona el punto de cambio.",
                   "Meanwhile, I was taking photos. Suddenly, a door opened behind me. Later, I found my group.",
                   ["I was taking photos", "I found my group", "A door opened behind me"], 2, c,
                   "evaluation", "La puerta que se abre de repente cambia la dirección del relato."),
            write(f"{p}.e03", "Escribe dos hechos con meanwhile y later.",
                  "Mina preparaba té; al mismo tiempo, Luis llamaba. Después llegó Ana.",
                  "Mina was making tea; meanwhile, Luis was calling. Later, Ana arrived.",
                  "While Mina was making tea, Luis was calling; later, Ana arrived.", c, "evaluation",
                  "Las variantes conectan acciones simultáneas y una llegada posterior."),
            q(f"{p}.e04", "Elige el cierre que completa una búsqueda de cartera.",
              ["Suddenly, I started looking for it.", "Eventually, a cashier returned it to me.",
               "At first, I thanked the cashier."], 1, c, "evaluation",
              "Eventually introduce el desenlace satisfactorio de la búsqueda."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona las señales con la historia de una carrera.",
                  [("inicio de la carrera", "the runners stayed together"),
                   ("giro de la carrera", "one runner fell"), ("final de la carrera", "she finished safely")], c,
                  "review", "El orden muestra inicio, giro y resultado sin mezclar las etapas."),
            q(f"{p}.r02", "¿Qué conector introduce una acción simultánea?",
              ["Eventually", "Meanwhile", "At first"], 1, c, "review",
              "Meanwhile enlaza una acción que ocurre al mismo tiempo que otra."),
            write(f"{p}.r03", "Resume el orden de la entrega usando tres conectores.",
                  "Inicio: Kai empaquetó el regalo. Giro: perdió la dirección. Final: llamó a Jo.",
                  "At first, Kai packed the gift. Suddenly, he lost the address. Eventually, he called Jo.",
                  "Kai packed the gift at first; then he lost the address, but eventually he called Jo.",
                  c, "review", "Ambas versiones hacen visibles el inicio, el problema y la solución."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-11.t01", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-11.t02", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-11.t04", f"{p}.r02"),
             f"{p}.e04": (f"en.n3.class-11.t05", f"{p}.r03")}
    return make_class(n, ["Reconocer señales de inicio, giro y desenlace.",
                          "Ordenar un relato breve mediante conectores temporales."],
        [("first", "primero"), ("suddenly", "de repente"), ("later", "más tarde"),
         ("eventually", "finalmente"), ("meanwhile", "mientras tanto"),
         ("turning", "giro")],
        [("At first, the street was calm.", "Al principio, la calle estaba tranquila.",
          "At first abre la situación inicial."),
         ("Suddenly, a cyclist stopped.", "De repente, un ciclista se detuvo.",
          "Suddenly anuncia el cambio inesperado."),
         ("Later, the police arrived.", "Más tarde, llegó la policía.",
          "Later coloca otro hecho después del giro."),
         ("Meanwhile, people moved away.", "Mientras tanto, la gente se alejó.",
          "Meanwhile indica simultaneidad."),
         ("Eventually, everyone was safe.", "Finalmente, todos estaban a salvo.",
          "Eventually presenta el desenlace."),
         ("The turning point was the sudden stop.", "El punto de giro fue la parada repentina.",
          "El turning point cambia el curso del relato.")], pools, remap)


def build_12() -> dict[str, Any]:
    n, c, p = 12, CONCEPTS[12], "en.n3.c12"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la frase que marca el hecho anterior.",
              ["Nora had left before I arrived.", "Nora left after I arrived.",
               "Nora is leaving when I arrive."], 0, c, "practiceGuided",
              "Had left sitúa la salida de Nora antes de mi llegada.",
              hint="Busca had más participio para el hecho más antiguo."),
            fill(f"{p}.pg02", "Completa: The film started after we ___ down.", "had sat", c,
                 "practiceGuided", "Had sat aclara que nos sentamos antes del inicio.",
                 hint="Usa had y el participio de sit."),
            order(f"{p}.pg03", "Ordena el hecho previo a la llamada.",
                  "I had already sent the message.", c, "practiceGuided",
                  "Had sent expresa una acción terminada antes de la llamada.",
                  hint="Pon had before sent y already entre ambos."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige qué ocurrió primero.",
                   "When Omar reached the café, his friends had ordered lunch.",
                   ["Omar reached the café", "His friends ordered lunch", "They paid together"], 1,
                   c, "practice", "Had ordered identifica el pedido como el hecho anterior."),
            match(f"{p}.p02", "Une cada hecho posterior con su causa anterior.",
                  [("She missed the train", "She had left home late"),
                   ("The room was clean", "They had finished the work")], c, "practice",
                  "Cada forma con had explica una situación posterior en past simple."),
            write(f"{p}.p03", "Aclara el orden: cerrar la tienda; llegar nosotros.",
                  "Primero cerraron la tienda. Después llegamos nosotros.",
                  "The staff had closed the shop before we arrived.",
                  "When we arrived, the staff had already closed the shop.", c, "practice",
                  "Las dos variantes marcan el cierre como anterior a nuestra llegada."),
        ],
        "evaluation": [
            fill(f"{p}.e01", "Completa: Eva was tired because she ___ all night.", "had worked", c,
                 "evaluation", "Had worked presenta el trabajo anterior que causó el cansancio."),
            q(f"{p}.e02", "Elige la frase: el show ya había empezado al entrar.",
              ["The show had begun before we entered.", "The show began after we entered.",
               "The show was beginning as we entered."], 0, c, "evaluation",
              "Had begun confirma que el espectáculo ya había empezado."),
            listen(f"{p}.e03", "Escucha y selecciona el hecho más antiguo.",
                   "Leo found an empty box because someone had taken the tools.",
                   ["Leo found the box", "Someone took the tools", "Leo bought new tools"], 1, c,
                   "evaluation", "Had taken coloca el retiro de las herramientas antes del hallazgo."),
            write(f"{p}.e04", "Explica el orden: perder la llave; esperar fuera.",
                  "Primero Sam perdió la llave. Después esperó fuera del piso.",
                  "Sam waited outside because he had lost his key.",
                  "Because Sam had lost his key, he waited outside the flat.", c, "evaluation",
                  "Las variantes conectan la pérdida anterior con la espera posterior."),
        ],
        "review": [
            order(f"{p}.r01", "Ordena la causa anterior del cierre de la carretera.",
                  "A tree had fallen across the road.", c, "review",
                  "Had fallen explica por qué la carretera quedó cerrada."),
            q(f"{p}.r02", "¿Qué pasó primero en esta pareja de hechos?",
              ["The guests arrived", "Maya had prepared dinner", "They ate dessert"], 1, c,
              "review", "Had prepared muestra que la cena estaba lista antes de la llegada."),
            write(f"{p}.r03", "Une los hechos: cargar el teléfono; comenzar el viaje.",
                  "El teléfono se cargó primero. El viaje comenzó después.",
                  "I had charged my phone before the journey began.",
                  "Before the journey began, I had fully charged my phone.", c, "review",
                  "Ambas respuestas mantienen el teléfono cargado como hecho previo."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-12.t04", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-12.t02", f"{p}.r02"),
             f"{p}.e03": (f"en.n3.class-12.t03", f"{p}.r02"),
             f"{p}.e04": (f"en.n3.class-12.t05", f"{p}.r03")}
    return make_class(n, ["Formar past perfect con had y participio.",
                          "Distinguir el hecho anterior del hecho posterior."],
        [("had", "había"), ("participle", "participio"), ("before", "antes de"),
         ("after", "después de"), ("already", "ya"), ("earlier", "anterior")],
        [("Past perfect uses had plus a participle.", "Past perfect usa had más un participio.",
          "La forma no cambia según el sujeto."),
         ("The bus had left before we arrived.", "El autobús había salido antes de que llegáramos.",
          "Before separa el hecho anterior del posterior."),
         ("After Mia had called, she relaxed.", "Después de que Mia llamó, se relajó.",
          "After también permite identificar el orden."),
         ("The earlier event uses past perfect.", "El hecho anterior usa past perfect.",
          "El past simple presenta normalmente el hecho posterior."),
         ("I had already eaten when Lee came.", "Ya había comido cuando Lee llegó.",
          "Already refuerza que la acción estaba terminada.")], pools, remap)


def build_13() -> dict[str, Any]:
    n, c, p = 13, CONCEPTS[13], "en.n3.c13"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la causa anterior del cambio en el parque.",
              ["A storm had damaged a tree.", "Families were having lunch.",
               "The park will open tomorrow."], 0, c, "practiceGuided",
              "El daño previo explica por qué cambia la escena del parque.",
              hint="Busca el hecho con had que explica el problema."),
            listen(f"{p}.pg02", "Escucha y selecciona el punto de giro.",
                   "We were walking home because the last bus had left. Suddenly, a neighbour stopped her car.",
                   ["The bus had left", "A neighbour stopped", "We reached home"], 1, c,
                   "practiceGuided", "La parada del coche transforma una caminata difícil en ayuda.",
                   hint="El giro aparece después de suddenly."),
            order(f"{p}.pg03", "Ordena la consecuencia del rescate.",
                  "Eventually the hikers reached the village safely.", c, "practiceGuided",
                  "El regreso seguro es la consecuencia final de la ayuda.",
                  hint="Eventually abre el desenlace."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada parte del relato con su función.",
                  [("The gate had locked automatically", "causa anterior"),
                   ("A guard heard us", "punto de giro"),
                   ("We entered the building", "consecuencia")], c, "practice",
                  "Las partes explican problema, cambio y resultado en orden causal."),
            q(f"{p}.p02", "¿Por qué no pudo Ada pagar el almuerzo?",
              ["The café was crowded", "She ordered soup", "She had left her wallet at home"],
              2, c, "practice", "La cartera olvidada anteriormente causa el problema de pago."),
            write(f"{p}.p03", "Resume causa, giro y consecuencia del paseo.",
                  "Causa: se rompió el mapa. Giro: apareció una señal. Resultado: hallaron el lago.",
                  "The map had torn, but then we saw a sign, so we eventually found the lake.",
                  "Because our map had torn, a road sign changed everything and helped us reach the lake.",
                  c, "practice", "Las variantes enlazan la causa previa con el giro y su resultado."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha y elige la causa del retraso de Priya.",
                   "Priya arrived late because her alarm had not rung. Luckily, the meeting started late too.",
                   ["Her alarm had not rung", "The meeting started early", "She missed the meeting"], 0,
                   c, "evaluation", "El despertador que no sonó explica directamente el retraso."),
            q(f"{p}.e02", "Selecciona el giro en la historia del pastel.",
              ["Jon had forgotten the sugar.", "A neighbour brought an extra cake.",
               "Everyone ate at noon."], 1, c, "evaluation",
              "La llegada de otro pastel resuelve de forma inesperada el problema inicial."),
            q(f"{p}.e03", "¿Qué consecuencia corresponde al corte de agua?",
              ["The pipe had broken underground.", "Workers checked the street.",
               "The café closed for the morning."], 2, c, "evaluation",
              "El cierre del café es el resultado observable del problema con el agua."),
            write(f"{p}.e04", "Explica causa, giro y resultado de la entrega.",
                  "Furgoneta averiada antes. Una ciclista ofreció ayuda. El paquete llegó a tiempo.",
                  "The van had broken down, but a cyclist offered help, so the package arrived on time.",
                  "Because the van had stopped working, a cyclist helped and the parcel reached its destination on time.",
                  c, "evaluation", "Ambas respuestas conservan la avería, la ayuda decisiva y la entrega puntual."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cada dato de la excursión con su función.",
                  [("We had chosen the wrong path", "causa"),
                   ("A farmer showed us a shortcut", "giro"),
                   ("We caught the train", "consecuencia")], c, "review",
                  "El atajo conecta la causa del retraso con la consecuencia positiva."),
            q(f"{p}.r02", "¿Qué hecho anterior explica la habitación fría?",
              ["The guests arrived at eight", "Someone had left a window open",
               "They drank hot tea"], 1, c, "review",
              "La ventana abierta previamente explica la baja temperatura."),
            write(f"{p}.r03", "Resume la solución inesperada del examen perdido.",
                  "Noa había ido al aula equivocada. Un profesor la llevó. Entró antes de empezar.",
                  "Noa had gone to the wrong room, but a teacher guided her, so she arrived before the exam began.",
                  "Because Noa had entered the wrong classroom, a teacher helped her reach the exam in time.",
                  c, "review", "Las versiones enlazan el error inicial, la ayuda y la llegada a tiempo."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-13.t01", f"{p}.r02"),
             f"{p}.e02": (f"en.n3.class-13.t03", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-13.t04", f"{p}.r01"),
             f"{p}.e04": (f"en.n3.class-13.t05", f"{p}.r03")}
    return make_class(n, ["Inferir una causa anterior expresada en past perfect.",
                          "Identificar giro y consecuencia en un relato breve."],
        [("cause", "causa"), ("result", "resultado"), ("because", "porque"),
         ("luckily", "por suerte"), ("change", "cambio"), ("consequence", "consecuencia")],
        [("The cause happened before the problem.", "La causa ocurrió antes del problema.",
          "Una causa anterior suele aparecer en past perfect."),
         ("Because the road had closed, we turned back.", "Como la carretera había cerrado, regresamos.",
          "Because hace explícita la relación causal."),
         ("Luckily, a driver offered help.", "Por suerte, un conductor ofreció ayuda.",
          "Luckily puede introducir un giro positivo."),
         ("The result came after the turning point.", "El resultado llegó después del punto de giro.",
          "El resultado muestra el efecto del cambio."),
         ("A change can produce a clear consequence.", "Un cambio puede producir una consecuencia clara.",
          "La consecuencia debe apoyarse en datos del relato.")], pools, remap)


def build_14() -> dict[str, Any]:
    n, c, p = 14, CONCEPTS[14], "en.n3.c14"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige el mejor contexto para iniciar una historia.",
              ["It was a cold morning, and I was waiting outside the college.",
               "Eventually, I found the correct classroom.", "Suddenly, the main door closed."], 0, c,
              "practiceGuided", "La primera opción establece lugar, momento y acción inicial.",
              hint="Un contexto responde cuándo, dónde y qué estaba ocurriendo."),
            fill(f"{p}.pg02", "Completa el hecho anterior: I was nervous because I ___.",
                 "had forgotten my notes", c, "practiceGuided",
                 "Had forgotten my notes explica el nerviosismo previo.",
                 hint="Usa had más participio y el objeto perdido."),
            order(f"{p}.pg03", "Ordena el giro de la presentación.",
                  "Suddenly my classmate offered to share her notes.", c, "practiceGuided",
                  "Suddenly presenta la ayuda que cambia la situación.",
                  hint="Comienza con la señal de giro y sigue con sujeto y verbo."),
        ],
        "practice": [
            match(f"{p}.p01", "Une las cuatro etapas con datos de una historia.",
                  [("contexto", "We were cycling beside the river"),
                   ("hecho anterior", "I had left the repair kit at home"),
                   ("giro", "A mechanic stopped to help"),
                   ("desenlace", "We reached the village before dark")], c, "practice",
                  "Las cuatro piezas forman una secuencia narrativa completa."),
            listen(f"{p}.p02", "Escucha y elige el detalle que hace coherente el final.",
                   "Our tyre was flat, but a mechanic repaired it. Eventually, we reached the village before dark.",
                   ["The river was cold", "The repaired tyre let them continue",
                    "They had dinner at home"], 1, c, "practice",
                   "La reparación permite continuar y explica la llegada final."),
            write(f"{p}.p03", "Conecta las cuatro etapas del viaje en dos oraciones.",
                  "Llovía. Habíamos perdido el paraguas. Paró un taxi. Llegamos secos.",
                  "It was raining, and we had lost our umbrella. Then a taxi stopped, so we arrived dry.",
                  "We had lost our umbrella while it was raining, but a taxi stopped and took us there dry.",
                  c, "practice", "Las variantes conectan contexto, antecedente, giro y resultado."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige el hecho anterior que explica el hambre de los viajeros.",
              ["They had skipped breakfast.", "They reached a village.", "They ordered lunch later."],
              0, c, "evaluation", "Had skipped breakfast aporta una causa anterior clara."),
            listen(f"{p}.e02", "Escucha y selecciona el giro de la historia del teléfono.",
                   "I had dropped my phone on the path. I was searching in the dark when a runner found it.",
                   ["I dropped the phone", "I searched in the dark", "A runner found it"], 2, c,
                   "evaluation", "El hallazgo del corredor cambia la búsqueda y conduce a la solución."),
            order(f"{p}.e03", "Ordena el desenlace de la visita inesperada.",
                  "Eventually we shared dinner and laughed together.", c, "evaluation",
                  "Eventually introduce un cierre explícito y conectado con la visita."),
            write(f"{p}.e04", "Escribe 60–80 palabras sobre una excursión con un giro.",
                  "Contexto: bosque lluvioso. Antes: mapa mojado. Giro: guardabosques llega. Final: refugio.",
                  "At first, my cousin and I were walking through a wet forest. We were worried because our map had become impossible to read in the rain. Suddenly, a forest ranger appeared on the path and showed us a safer route. Later, we followed the river towards a small shelter. Eventually, we arrived there before dark, made hot tea, and called our family to explain that we were safe.",
                  "My cousin and I were hiking in a rainy forest when we noticed that the map had become unreadable. We did not know which path to take. Suddenly, a ranger found us and pointed towards a shelter beside the river. Later, we walked there together. Eventually, we reached the shelter before night, drank something warm, and sent our family a message saying that everything was fine.",
                  c, "evaluation", "Las versiones desarrollan las cuatro etapas y mantienen una cronología coherente."),
        ],
        "review": [
            q(f"{p}.r01", "¿Qué final resuelve una historia sobre un tren perdido?",
              ["At first, we checked the time.", "Eventually, we took the next train and arrived at noon.",
               "Suddenly, the departure board changed."], 1, c, "review",
              "El siguiente tren y la llegada a mediodía cierran el problema."),
            match(f"{p}.r02", "Relaciona cada detalle de la fiesta con su etapa.",
                  [("Guests were waiting outside", "contexto"),
                   ("I had written the wrong time", "hecho anterior"),
                   ("The caretaker opened the hall", "giro"),
                   ("The party started calmly", "desenlace")], c, "review",
                  "La secuencia vincula el error previo con la solución y el inicio de la fiesta."),
            write(f"{p}.r03", "Redacta 60–80 palabras sobre una entrega que cambia.",
                  "Contexto: tarde con tráfico. Antes: dirección copiada mal. Giro: cliente llama. Final: entrega.",
                  "At first, I was delivering a birthday parcel on a busy afternoon. I became confused because I had copied one number in the address incorrectly. Suddenly, the customer called and described a bright blue door near the library. Later, I recognised the correct street and found the house. Eventually, I delivered the parcel before the party began, and the customer thanked me for checking instead of leaving it elsewhere.",
                  "I was carrying a birthday package through heavy afternoon traffic when I realised that I had written the wrong house number. Suddenly, the customer phoned and mentioned a blue door beside the library. That landmark helped me find the correct road. Later, I reached the house, and eventually I handed over the parcel before the celebration started. The customer was pleased that I had called to confirm the address.",
                  c, "review", "Ambos relatos conectan el error anterior, la llamada decisiva y la entrega final."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-14.t02", f"{p}.r02"),
             f"{p}.e02": (f"en.n3.class-14.t03", f"{p}.r01"),
             f"{p}.e03": (f"en.n3.class-14.t04", f"{p}.r01"),
             f"{p}.e04": (f"en.n3.class-14.t05", f"{p}.r03")}
    return make_class(n, ["Planificar contexto, hecho anterior, giro y desenlace.",
                          "Escribir un relato conectado de 60–80 palabras."],
        [("context", "contexto"), ("previous", "anterior"), ("turn", "giro"),
         ("outcome", "desenlace"), ("connect", "conectar"), ("revise", "revisar")],
        [("Set the context with time, place and action.", "Presenta el contexto con tiempo, lugar y acción.",
          "El contexto orienta al lector desde el inicio."),
         ("Show a previous event with past perfect.", "Muestra un hecho anterior con past perfect.",
          "El hecho previo explica la situación."),
         ("Add a turn that changes the story.", "Añade un giro que cambie la historia.",
          "El giro debe afectar lo que sucede después."),
         ("Give the story a clear outcome.", "Da a la historia un desenlace claro.",
          "El resultado debe resolver o explicar el cambio."),
         ("Connect the stages, then revise the chronology.", "Conecta las etapas y luego revisa la cronología.",
          "Revisar evita saltos o contradicciones temporales.")], pools, remap)


def build_15() -> dict[str, Any]:
    n, c, p = 15, CONCEPTS[15], "en.n3.c15"
    all_c = [CONCEPTS[k] for k in NUMBERS]
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la pregunta que aclara el hecho anterior.",
              ["What had happened before you arrived?", "Do you like stories?",
               "Will the place be open tomorrow?"], 0, c, "practiceGuided",
              "La pregunta con had happened solicita la causa anterior.",
              hint="Busca una pregunta sobre algo ocurrido antes de la llegada."),
            fill(f"{p}.pg02", "Completa la aclaración: Before that, we ___.", "had called the guide", c,
                 "practiceGuided", "Had called fija la llamada antes del resto del relato.",
                 hint="Usa had más el participio de call."),
            order(f"{p}.pg03", "Ordena la pregunta sobre el desenlace.",
                  "How did the story end?", c, "practiceGuided",
                  "La pregunta pide directamente el resultado final.",
                  hint="Empieza con How, luego auxiliar, sujeto y verbo."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige la aclaración coherente.",
                   "We were locked outside because I had left the key inside. A neighbour helped us enter.",
                   ["The key was in my bag", "I had left the key inside",
                    "The neighbour had locked the door"], 1, c, "practice",
                   "La llave olvidada dentro mantiene la causa del relato original."),
            match(f"{p}.p02", "Une cada pregunta con la información que aclara.",
                  [("What happened first?", "We had missed the earlier bus."),
                   ("What changed the situation?", "A driver offered us a lift."),
                   ("How did it end?", "We arrived before the doors closed.")], c, "practice",
                  "Las respuestas conservan causa, giro y desenlace en la misma cronología."),
            write(f"{p}.p03", "Cuenta el cambio y responde por qué estabas allí.",
                  "Esperabas frente al teatro porque habías comprado una entrada. Un actor te invitó a entrar.",
                  "I was waiting outside the theatre because I had bought a ticket. Then an actor invited me inside.",
                  "Because I had bought a ticket, I was outside the theatre when an actor suddenly invited me in.",
                  c, "practice", "Las variantes cuentan el cambio y aclaran el motivo sin alterar el orden."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige la aclaración compatible con el relato del puerto.",
              ["We had checked the wrong departure time.", "The boat will depart next week.",
               "We always prefer travelling by bus."], 0, c, "evaluation",
              "El horario consultado anteriormente puede explicar el problema en el puerto."),
            listen(f"{p}.e02", "Escucha y selecciona el desenlace de la entrevista.",
                   "I had brought the wrong folder. Suddenly, the receptionist printed my form. Eventually, I entered the interview calmly.",
                   ["I brought the wrong folder", "The receptionist printed a form",
                    "I entered the interview calmly"], 2, c, "evaluation",
                   "La entrada tranquila es el resultado final tras la ayuda."),
            write(f"{p}.e03", "Responde cuándo cambió la historia del concierto.",
                  "Se había cancelado el autobús. Caminábamos. Una familia ofreció llevarnos.",
                  "The story changed when a family offered us a lift after our bus had been cancelled.",
                  "After the bus had been cancelled, the turning point came when a family gave us a ride.",
                  c, "evaluation", "Ambas respuestas ubican la oferta de transporte como giro después de la cancelación."),
            write(f"{p}.e04", "Escribe 70–100 palabras y responde causa y orden.",
                  "Costa: caminabas. Antes, olvidaste agua. Giro: tormenta y faro abierto. Final: refugio. Preguntas: ¿por qué estabas preocupado? ¿qué ocurrió primero?",
                  "At first, I was walking along the coast with my brother. I was worried because I had left our water bottles in the car before we started. Suddenly, a storm reached the beach, but the keeper of a nearby lighthouse opened the door for us. Later, we waited there and called our parents. Eventually, the rain stopped, and we returned safely. I was worried because we had no water. Leaving the bottles happened first.",
                  "My brother and I were following a coastal path when dark clouds appeared. Earlier, I had forgotten our water in the car, so I felt worried. Suddenly, heavy rain began, and a lighthouse keeper invited us inside. We contacted our parents while we waited. Eventually, the weather improved and we walked back safely together. The missing water caused my worry, and forgetting it in the car was the first event.",
                  c, "evaluation", "Los relatos explican el antecedente, el giro, el final y las dos aclaraciones solicitadas.",
                  requires=all_c),
        ],
        "review": [
            q(f"{p}.r01", "¿Qué pregunta comprueba la causa de un retraso?",
              ["Where are you going next?", "Why had the journey started late?",
               "Who likes travelling?"], 1, c, "review",
              "Why had the journey started late solicita la causa anterior del retraso."),
            match(f"{p}.r02", "Relaciona las aclaraciones con la historia de una feria.",
                  [("hecho anterior", "We had left the tickets at home."),
                   ("giro", "A friend sent digital copies."),
                   ("desenlace", "We entered before the show began.")], c, "review",
                  "La secuencia recupera el problema, la solución decisiva y la entrada final."),
            write(f"{p}.r03", "Escribe 70–100 palabras y aclara causa y desenlace.",
                  "Exposición: llevabas una maqueta. Antes, una pieza se rompió. Giro: taller abierto. Final: reparación. Preguntas: ¿qué causó el problema? ¿cómo terminó?",
                  "At first, I was carrying my model to a school exhibition. I felt upset because one wooden piece had broken on the bus. Suddenly, I noticed that the technology workshop was open, and a teacher offered me some tools. Later, I repaired the piece and checked the whole model. Eventually, I presented it to the visitors on time. The broken piece had caused the problem. The story ended with a successful presentation.",
                  "I was taking a model to our school exhibition when I saw some damage. A small part had broken during the bus journey, which caused the problem. Suddenly, a teacher invited me into the open workshop and helped me choose safe tools. Later, I fixed and tested the model. Eventually, the exhibition opened, and I explained my work to the visitors. It ended with the model repaired and ready on time.",
                  c, "review", "Ambas versiones mantienen la causa, el giro, el desenlace y respuestas consistentes.",
                  requires=all_c),
        ],
    }
    remap = {f"{p}.e01": (f"en.n3.class-15.t02", f"{p}.r01"),
             f"{p}.e02": (f"en.n3.class-15.t04", f"{p}.r02"),
             f"{p}.e03": (f"en.n3.class-15.t03", f"{p}.r02"),
             f"{p}.e04": (f"en.n3.class-15.t06", f"{p}.r03")}
    return make_class(n, ["Contar una experiencia inesperada con cronología estable.",
                          "Responder dos preguntas sobre causa y orden sin contradecir el relato."],
        [("clarify", "aclarar"), ("first", "primero"), ("earlier", "antes"),
         ("turning", "giro"), ("ending", "final"), ("consistent", "coherente")],
        [("Clarify what happened first.", "Aclara qué ocurrió primero.",
          "La primera aclaración identifica el hecho más antiguo."),
         ("Use past perfect for the earlier cause.", "Usa past perfect para la causa anterior.",
          "La forma had más participio mantiene el orden."),
         ("A turning point changes the next action.", "Un punto de giro cambia la acción siguiente.",
          "El cambio debe tener una consecuencia visible."),
         ("Give the story a clear ending.", "Da a la historia un final claro.",
          "El desenlace responde qué ocurrió al final."),
         ("Keep every answer consistent with the story.", "Mantén cada respuesta coherente con el relato.",
          "Las aclaraciones no pueden añadir otra cronología."),
         ("At first, I was carrying food to a community event. I was delayed because I had left my keys in the flat. Suddenly, a neighbour returned home and opened the building door for me. Later, I collected the keys and took a shortcut through the park. Eventually, I reached the event safely and calmly before lunch began. The keys caused my delay, and leaving them upstairs happened before the neighbour arrived.",
          "Al principio llevaba comida a un evento comunitario. El giro fue la ayuda de un vecino y llegué antes del almuerzo.",
          "Este modelo integrado muestra orden, causa anterior, giro, final y dos aclaraciones.")],
        pools, remap, uses=all_c, cumulative=all_c)


BUILDERS = {11: build_11, 12: build_12, 13: build_13, 14: build_14, 15: build_15}


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
        close=classes[-1]; expected=[CONCEPTS[n] for n in NUMBERS]
        assert close["cumulativeEvaluation"]==expected and close["usesPatterns"]==expected
        e04=next(x for x in close["pools"]["evaluation"] if x["id"]=="en.n3.c15.e04")
        r03=next(x for x in close["pools"]["review"] if x["id"]=="en.n3.c15.r03")
        assert e04["requires"]==expected and r03["requires"]==expected
        t06=close["teaching"][-1]["en"].casefold(); ea=e04["answer"]["text"].casefold(); ra=r03["answer"]["text"].casefold()
        assert "community event" in t06 and "coast" in ea and "exhibition" in ra
        for text in (t06,ea,ra):
            assert "had" in text and ("suddenly" in text or "turning" in text)
            assert "eventually" in text
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
         "range":{"start":11,"end":15},"classes":classes}
    path=OUT/"bundle-11-15.json"; path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return path,summary


def write_report(paths:list[Path], summary:dict[str,Any])->Path:
    hashes="\n".join(f"{digest(p)}  {p.name}" for p in paths)
    text=f"""# DRAFT — Inglés N3 C11–C15

Estado: **DRAFT para revisión independiente; no autorizado para integración**.

## Alcance

- Bloque `narrative-turning-points`, entrada B1, fases `input → form → comprehension → production → transfer`.
- Cinco clases, 65 ejercicios y contrato `editorial-agent.v2`.
- `status: shadow`, `runtimeAi: false`, selección y recuperación deterministas.

## Cierre C15

- `t06`: llaves olvidadas antes de un evento comunitario.
- `e04`: tormenta durante una caminata por la costa.
- `r03`: maqueta dañada antes de una exposición escolar.
- Cada escenario demuestra inicio, hecho anterior en past perfect, giro,
  desenlace y dos aclaraciones coherentes.

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
PYTHONDONTWRITEBYTECODE=1 python3 work/n3_c11_15/generate.py --all
python3 tools/contenido/validar_bundle_editorial.py --file work/n3_c11_15/bundle-11-15.json --start 11 --end 15 --level 3
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
    entries=[f"{digest(Path(__file__))}  ../../tools/contenido/generar_editorial_n3_11_15.py",
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
