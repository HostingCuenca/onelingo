#!/usr/bin/env python3
"""Generate the isolated English N3 C36-C40 editorial draft."""
from __future__ import annotations

import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contenido/en/editorial/n3"
REPORT_OUT = ROOT / "build/editorial-n3-36-40"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"
SCALE = "client-10-levels-v1"
NUMBERS = range(36, 41)
CONCEPTS = {n: f"n3-defining-information-{n-35}" for n in NUMBERS}
PHASES = {36: "input", 37: "form", 38: "comprehension", 39: "production", 40: "transfer"}
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
    x["origin"]["scoring"] = {"parts": len(sentences), "minimumCorrect": minimum_correct,
                                "independentAttempt": True}
    joined = " | ".join(answers)
    x["answer"] = {"text": joined, "accepted": [joined],
                   "parts": [
                       {"text": value,
                        "accepted": [value, *(["which", "that"] if value in {"which", "that"} else [])]}
                       for value in answers
                   ]}
    return hashed(x)


def order(i: str, prompt: str, answer: str, c: str, pool: str, feedback: str,
          **kw: Any) -> dict[str, Any]:
    x = base(i, "ordenar", prompt, c, pool, feedback, **kw)
    x["answer"] = {"text": answer, "tokens": answer.split()}
    return hashed(x)


def write(i: str, prompt: str, stimulus: str, answer: str, alternative: str, c: str,
          pool: str, feedback: str, **kw: Any) -> dict[str, Any]:
    scoring = kw.pop("scoring", None)
    x = base(i, "escribir", prompt, c, pool, feedback, **kw)
    x["origin"]["text"] = stimulus
    if scoring is not None: x["origin"]["scoring"] = scoring
    x["answer"] = {"text": answer, "accepted": [answer, alternative]}
    return hashed(x)


def match(i: str, prompt: str, pairs: list[tuple[str, str]], c: str, pool: str,
          feedback: str, **kw: Any) -> dict[str, Any]:
    scoring = kw.pop("scoring", None)
    x = base(i, "relacionar", prompt, c, pool, feedback, **kw)
    values = [[a, {"es": b}] for a, b in pairs]
    x["answer"], x["origin"]["pairs"] = {"pairs": values}, values
    if scoring is not None: x["origin"]["scoring"] = scoring
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




def build_36() -> dict[str, Any]:
    n, c, p = 36, CONCEPTS[36], "en.n3.c36"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la definición de una persona que ayuda en una biblioteca.",
              ["A librarian is a place where books are kept.",
               "A librarian is an object that records loans.",
               "A librarian is a person who helps readers find books."], 2, c, "practiceGuided",
              "Who enlaza librarian, una persona, con su función de ayudar a lectores.",
              hint="Para una persona, busca who o that."),
            fill(f"{p}.pg02", "Completa con who: A nurse is someone ___ cares for patients.",
                 "who", c, "practiceGuided", "Who introduce la función de la enfermera.",
                 hint="El antecedente someone se refiere a una persona."),
            order(f"{p}.pg03", "Ordena la definición de un técnico.",
                  "A technician is a person that repairs equipment.", c, "practiceGuided",
                  "That también puede introducir una definición esencial de persona.",
                  hint="Coloca that después de person."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha y elige el profesional descrito.",
                   "This is someone who checks your eyes and recommends glasses.",
                   ["An optician", "A mechanic", "A pharmacist"], 0, c, "practice",
                   "An optician es quien revisa la vista y recomienda gafas."),
            match(f"{p}.p02", "Relaciona tres profesionales con sus funciones.",
                  [("A plumber", "is someone who repairs water pipes"),
                   ("A translator", "is a person who changes text into another language"),
                   ("A paramedic", "is someone that gives emergency care")], c, "practice",
                  "Cada definición usa una función concreta para identificar a la persona."),
            write(f"{p}.p03", "Define a una recepcionista con who o that.",
                  "Función: recibir visitantes y responder llamadas.",
                  "A receptionist is a person who welcomes visitors and answers calls.",
                  "A receptionist is someone that greets visitors and answers the phone.", c,
                  "practice", "Las variantes identifican a la persona mediante dos tareas visibles."),
        ],
        "evaluation": [
            q(f"{p}.e01", "¿Qué definición identifica a un electricista?",
              ["A person who designs gardens", "A person who delivers medicine",
               "A person who repairs electrical systems"], 2, c, "evaluation",
              "Reparar sistemas eléctricos distingue al electricista de los otros profesionales."),
            listen(f"{p}.e02", "Escucha y selecciona a la persona descrita.",
                   "I need someone who can prepare legal documents and explain my rights.",
                   ["A chef", "A lawyer", "A driver"], 1, c, "evaluation",
                   "A lawyer prepara documentos legales y explica derechos."),
            write(f"{p}.e03", "Define a un orientador laboral mediante una función.",
                  "Profesional: career adviser. Función: ayudar a elegir formación y empleo.",
                  "A career adviser is a person who helps people choose training and jobs.",
                  "A career adviser is someone that helps clients select courses and work.", c,
                  "evaluation", "Las dos definiciones hacen inequívoco el rol del orientador laboral."),
            match(f"{p}.e04", "Relaciona cinco profesionales y definiciones. Meta: 4 de 5.",
                  [("A locksmith", "is a person who repairs locks"),
                   ("A dietitian", "is someone who advises people about food"),
                   ("A surveyor", "is a professional that measures land and buildings"),
                   ("A counsellor", "is someone who helps people discuss problems"),
                   ("A courier", "is a person that delivers documents and parcels")], c,
                  "evaluation", "Las cinco relaciones usan funciones distintas y referentes personales claros.",
                  scoring={"parts": 5, "minimumCorrect": 4, "independentAttempt": True}),
        ],
        "review": [
            q(f"{p}.r01", "Elige la definición correcta de un intérprete.",
              ["A person who translates spoken language", "A person who repairs roofs",
               "A person who checks tickets"], 0, c, "review",
              "Traducir lenguaje hablado es la función específica del intérprete."),
            match(f"{p}.r02", "Recupera cinco profesiones mediante sus funciones.",
                  [("A roofer", "is someone who repairs roofs"),
                   ("A vet", "is a person who treats animals"),
                   ("A cashier", "is someone that takes payments"),
                   ("A guide", "is a person who shows visitors around"),
                   ("A tailor", "is someone who makes or changes clothes")], c, "review",
                  "La recuperación practica cinco personas nuevas con who o that."),
            write(f"{p}.r03", "Define a un trabajador social con una función precisa.",
                  "Función: apoyar a familias que necesitan servicios públicos.",
                  "A social worker is a person who supports families that need public services.",
                  "A social worker is someone that helps families access public support.", c,
                  "review", "Ambas variantes identifican el rol sin añadir tareas no indicadas."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-36.t02", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-36.t04", f"{p}.r01"),
             f"{p}.e03": ("en.n3.class-36.t05", f"{p}.r03"),
             f"{p}.e04": ("en.n3.class-36.t06", f"{p}.r02")}
    return make_class(n, ["Reconocer who o that tras un antecedente de persona.",
                          "Relacionar cinco profesionales con funciones inequívocas."],
        [("professional", "profesional"), ("person", "persona"), ("who", "que"),
         ("that", "que relativo"), ("role", "función"), ("help", "ayudar")],
        [("A professional can be defined by a specific function.",
          "Un profesional puede definirse mediante una función específica.", "La tarea concreta distingue una profesión de otra."),
         ("Use who after a person.", "Usa who después de una persona.",
          "Who introduce información esencial sobre alguien."),
         ("That can also define a person in an essential clause.",
          "That también puede definir a una persona en una cláusula esencial.", "No lleva coma en estas definiciones."),
         ("The role must identify the worker clearly.",
          "La función debe identificar al trabajador con claridad.", "Evita tareas tan generales que sirvan para varios profesionales."),
         ("A clear definition tells how the worker can help.",
          "Una definición clara dice cómo puede ayudar el trabajador.", "La ayuda debe ser observable en la frase."),
         ("Match each professional to the person who performs its exact function.",
          "Relaciona cada profesional con la persona que realiza su función exacta.", "Cinco relaciones permiten comprobar una meta de cuatro aciertos.")],
        pools, remap)


def build_37() -> dict[str, Any]:
    n, c, p = 37, CONCEPTS[37], "en.n3.c37"
    pools = {
        "practiceGuided": [
            fill(f"{p}.pg01", "Completa con which: A kettle is a thing ___ heats water.",
                 "which", c, "practiceGuided", "Which introduce la función de un objeto.",
                 hint="El antecedente kettle es una cosa."),
            q(f"{p}.pg02", "Elige where para definir un lugar.",
              ["A clinic is a place which people receive medical care.",
               "A clinic is a person who gives care.",
               "A clinic is a place where people receive medical care."], 2, c, "practiceGuided",
              "Where enlaza clinic con la actividad que ocurre allí.",
              hint="Para un lugar seguido de sujeto y verbo, usa where."),
            order(f"{p}.pg03", "Ordena la definición de un cargador.",
                  "A charger is a device that gives power to a battery.", c, "practiceGuided",
                  "That introduce la función esencial del dispositivo.",
                  hint="Coloca that después del antecedente device."),
        ],
        "practice": [
            match(f"{p}.p01", "Relaciona antecedentes con which, that o where.",
                  [("a tool ___ cuts wire", "that"), ("a hall ___ events happen", "where"),
                   ("a card ___ stores travel credit", "which")], c, "practice",
                  "Thing acepta which/that; el lugar con actividad usa where."),
            listen(f"{p}.p02", "Escucha y elige el objeto descrito.",
                   "It is a device which measures the temperature in a room.",
                   ["A thermometer", "A suitcase", "A ladder"], 0, c, "practice",
                   "A thermometer es el objeto que mide temperatura."),
            write(f"{p}.p03", "Define una lavandería y una linterna.",
                  "Lavandería: lavar ropa allí. Linterna: producir luz portátil.",
                  "A laundrette is a place where people wash clothes. A torch is an object which produces portable light.",
                  "A laundrette is somewhere where customers wash clothes. A torch is a device that gives portable light.",
                  c, "practice", "Las variantes distinguen el lugar con where y el objeto con which/that."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige el relativo para un sitio donde se recicla vidrio.",
              ["who", "where", "which"], 1, c, "evaluation",
              "Where introduce lo que ocurre en el centro de reciclaje."),
            listen(f"{p}.e02", "Escucha la pista y selecciona la herramienta definida.",
                   "This is a tool that opens bottles without damaging the cap.",
                   ["A bottle opener", "A paintbrush", "A key ring"], 0, c, "evaluation",
                   "A bottle opener cumple exactamente la función indicada."),
            write(f"{p}.e03", "Define un punto de información con where.",
                  "Lugar: viajeros piden mapas y direcciones allí.",
                  "An information point is a place where travellers ask for maps and directions.",
                  "An information desk is somewhere where visitors request maps and directions.", c,
                  "evaluation", "Ambas definiciones usan where para ubicar la actividad del servicio."),
            multi_fill(f"{p}.e04", "Completa seis definiciones con that, which o where.",
                  ["An alarm is a device ___ warns people.",
                   "A studio is a place ___ artists work.",
                   "A filter is an object ___ removes dirt.",
                   "A depot is a place ___ buses wait.",
                   "A scanner is a device ___ copies an image.",
                   "A shelter is a place ___ people stay safe."],
                  ["that", "where", "which", "where", "that", "where"],
                  c, "evaluation", "Cada respuesta distingue objetos de lugares por la estructura de la definición.",
                  minimum_correct=5),
        ],
        "review": [
            q(f"{p}.r01", "¿Qué definición usa correctamente where?",
              ["A pantry is a person who stores food.", "A pantry is an object where stores food.",
               "A pantry is a place where food is stored."], 2, c, "review",
              "Where conecta el lugar pantry con la acción pasiva que sucede allí."),
            order(f"{p}.r02", "Ordena la definición de una tarjeta de acceso.",
                  "An access card is an object that opens a secure door.", c, "review",
                  "That enlaza el objeto con su función de abrir una puerta."),
            multi_fill(f"{p}.r03", "Recupera seis definiciones con that, which o where.",
                  ["A timer is a device ___ counts time.",
                   "A bakery is a place ___ bread is made.",
                   "An adapter is an object ___ connects plugs.",
                   "An archive is a place ___ records are kept.",
                   "A helmet is something ___ protects the head.",
                   "A terminal is a place ___ passengers arrive."],
                  ["that", "where", "which", "where", "that", "where"],
                  c, "review", "La recuperación exige elegir el relativo por la función sintáctica.",
                  minimum_correct=5),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-37.t04", f"{p}.r01"),
             f"{p}.e02": ("en.n3.class-37.t02", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-37.t04", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-37.t06", f"{p}.r03")}
    return make_class(n, ["Usar which o that para objetos y where para lugares.",
                          "Completar seis definiciones con al menos cinco formas correctas."],
        [("thing", "cosa"), ("which", "que relativo"), ("that", "que esencial"),
         ("place", "lugar"), ("where", "donde"), ("object", "objeto")],
        [("A thing can use which in an essential definition.",
          "Una cosa puede usar which en una definición esencial.", "Which introduce la función del objeto."),
         ("An object can also use that.", "Un objeto también puede usar that.",
          "That y which son posibles con cosas en este contexto."),
         ("Use that without a comma in these definitions.",
          "Usa that sin coma en estas definiciones.", "La información es necesaria para identificar el antecedente."),
         ("A place uses where before an activity.",
          "Un lugar usa where antes de una actividad.", "Where equivale a in/at which en estas definiciones."),
         ("Which or that must agree with a thing, not a person.",
          "Which o that deben referirse a una cosa, no a una persona.", "Primero identifica el tipo de antecedente."),
         ("For six items, label each antecedent as object or place before completing.",
          "En seis ítems, etiqueta cada antecedente como objeto o lugar antes de completar.", "La etiqueta hace inequívoca la selección del relativo.")],
        pools, remap)


def build_38() -> dict[str, Any]:
    n, c, p = 38, CONCEPTS[38], "en.n3.c38"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "El anuncio dice someone who repairs watches. ¿Quién es?",
              ["The waiting customer", "The shop owner next door", "The watch repairer"], 2,
              c, "practiceGuided", "Who repairs watches define al reparador, no a las personas mencionadas cerca.",
              hint="Busca el referente que realiza la acción definitoria."),
            listen(f"{p}.pg02", "Escucha y elige el lugar descrito.",
                   "Visit the centre where residents can borrow tools for home repairs.",
                   ["The tool library", "The sports hall", "The post office"], 0, c,
                   "practiceGuided", "The tool library es el lugar donde los residentes toman herramientas prestadas.",
                   hint="La acción después de where identifica el servicio."),
            order(f"{p}.pg03", "Ordena el detalle que define un servicio de reparto.",
                  "It is a service that delivers medicine on the same day.", c, "practiceGuided",
                  "That delivers medicine distingue el servicio por su función.",
                  hint="Coloca la cláusula relativa después de service."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada anuncio con su referente exacto.",
                  [("a person who fits new locks", "locksmith"),
                   ("a device which prints labels", "label printer"),
                   ("a place where bikes are stored", "cycle store")], c, "practice",
                  "Persona, objeto y lugar se identifican mediante el detalle definitorio."),
            listen(f"{p}.p02", "Escucha y selecciona el objeto, no la información extra.",
                   "Our office opens at eight. Use the card which records each visitor's arrival.",
                   ["The opening time", "The visitor card", "The office manager"], 1, c,
                   "practice", "Which records arrivals define la tarjeta; la hora es información adicional."),
            write(f"{p}.p03", "Identifica persona, objeto y lugar en tres anuncios.",
                  "who repairs shoes; which copies keys; where customers collect parcels.",
                  "Person: the shoe repairer. Object: the key machine. Place: the parcel collection point.",
                  "The cobbler is the person; the key cutter is the object; the collection desk is the place.", c,
                  "practice", "Las respuestas recuperan los tres referentes a partir del detalle relativo."),
        ],
        "evaluation": [
            q(f"{p}.e01", "¿Quién ofrece el apoyo definido en el anuncio?",
              ["The adviser who checks benefit forms", "The receptionist who opens the door",
               "The visitor who waits outside"], 0, c, "evaluation",
              "Checking benefit forms es el detalle que identifica al adviser solicitado."),
            listen(f"{p}.e02", "Escucha y selecciona el servicio descrito.",
                   "We recommend the service that collects large furniture from your home.",
                   ["Furniture sales", "Room decoration", "Home furniture collection"], 2, c,
                   "evaluation", "Collects large furniture from home define el servicio de recogida."),
            q(f"{p}.e03", "Elige el lugar definido por where you can report lost property.",
              ["A lost-property office", "A waiting room", "A ticket machine"], 0, c,
              "evaluation", "La oficina de objetos perdidos es el lugar donde se reportan pertenencias."),
            write(f"{p}.e04", "Lee tres anuncios e identifica persona, objeto y lugar.",
                  "A: Ask for Nara, who translates housing letters; she works mornings. B: Use the tablet which displays queue numbers; it is beside reception. C: Go to the room where tenants meet advisers; it closes at six.",
                  "Person: Nara, the translator. Object: the queue-number tablet. Place: the adviser meeting room.",
                  "Nara is the person; the tablet displaying queue numbers is the object; the room for tenant-adviser meetings is the place.",
                  c, "evaluation", "La respuesta usa solo los detalles definitorios y descarta horarios y ubicación extra."),
        ],
        "review": [
            q(f"{p}.r01", "¿Qué objeto describe which checks air quality?",
              ["A window cleaner", "A health adviser", "An air-quality sensor"], 2, c, "review",
              "El sensor es el objeto que mide la calidad del aire."),
            listen(f"{p}.r02", "Escucha y elige el referente principal.",
                   "The centre is busy on Fridays. Ask for the volunteer who helps people complete online forms.",
                   ["Friday", "The volunteer", "The online form"], 1, c, "review",
                   "Who helps people complete forms define al voluntario."),
            write(f"{p}.r03", "Recupera tres referentes de anuncios nuevos.",
                  "who tests hearing; which stores digital tickets; where residents leave batteries.",
                  "Person: the hearing specialist. Object: the digital ticket wallet. Place: the battery collection point.",
                  "The hearing tester is the person; the ticket wallet is the object; the battery point is the place.",
                  c, "review", "Los tres referentes se apoyan en acciones distintas y explícitas."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-38.t02", f"{p}.r02"),
             f"{p}.e02": ("en.n3.class-38.t03", f"{p}.r01"),
             f"{p}.e03": ("en.n3.class-38.t04", f"{p}.r03"),
             f"{p}.e04": ("en.n3.class-38.t06", f"{p}.r03")}
    return make_class(n, ["Localizar el referente definido en un anuncio de servicio.",
                          "Ignorar horarios o detalles extra que no cambian el referente."],
        [("advert", "anuncio"), ("referent", "referente"), ("detail", "detalle"),
         ("person", "persona"), ("service", "servicio"), ("location", "ubicación")],
        [("Read the whole advert before choosing.", "Lee todo el anuncio antes de elegir.",
          "La información definitoria puede aparecer después del nombre."),
         ("The referent is the person, thing or place being defined.",
          "El referente es la persona, cosa o lugar definido.", "Who, which/that y where ayudan a localizarlo."),
         ("The relative detail identifies the service exactly.",
          "El detalle relativo identifica el servicio con precisión.", "La función es más importante que información secundaria."),
         ("Where points to a location in which an activity happens.",
          "Where señala una ubicación en la que ocurre una actividad.", "No confundas el lugar con un objeto cercano."),
         ("A person may be mentioned beside extra opening times.",
          "Una persona puede aparecer junto a horarios adicionales.", "El horario no cambia quién realiza la función."),
         ("For an integrated advert set, extract one person, one object and one place.",
          "En un conjunto integrado, extrae una persona, un objeto y un lugar.", "Cada respuesta debe citar el detalle que la define.")],
        pools, remap)


def build_39() -> dict[str, Any]:
    n, c, p = 39, CONCEPTS[39], "en.n3.c39"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige el acertijo que define una persona sin nombrarla.",
              ["This is someone who checks a building's safety.",
               "This is a building where inspections happen.",
               "This is a device which records heat."], 0, c, "practiceGuided",
              "Someone who checks safety deja identificar a la persona por su función.",
              hint="Busca un antecedente personal y who."),
            fill(f"{p}.pg02", "Completa el objeto: It is a device ___ detects smoke.",
                 "that", c, "practiceGuided", "That introduce la pista funcional del detector.",
                 hint="El antecedente device es un objeto."),
            order(f"{p}.pg03", "Ordena el acertijo de un lugar.",
                  "It is a place where passengers wait for trains.", c, "practiceGuided",
                  "Where presenta la actividad que permite identificar la estación.",
                  hint="Coloca where después de place."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada pista con el tipo de referente.",
                  [("someone who repairs instruments", "person"),
                   ("a tool which measures distance", "object"),
                   ("a room where recordings are made", "place")], c, "practice",
                  "Las pistas distinguen persona, objeto y lugar por antecedente y relativo."),
            listen(f"{p}.p02", "Escucha y elige la solución del acertijo.",
                   "I am a place where people take damaged computers for repair.",
                   ["A keyboard", "A computer repair shop", "A web designer"], 1, c,
                   "practice", "La tienda de reparación es el lugar donde se llevan los equipos dañados."),
            write(f"{p}.p03", "Escribe tres pistas breves sin nombrar las respuestas.",
                  "Persona: corta pelo. Objeto: seca ropa. Lugar: se toman autobuses.",
                  "Someone who cuts hair works here. It is a machine that dries clothes. It is a place where people catch buses.",
                  "This person is someone who cuts hair. This is a device which dries clothes. This is somewhere where passengers board buses.",
                  c, "practice", "Las variantes usan tres antecedentes y mantienen identificables los referentes."),
        ],
        "evaluation": [
            q(f"{p}.e01", "¿Qué solución corresponde a someone who designs buildings?",
              ["An architect", "A survey tool", "A construction site"], 0, c, "evaluation",
              "An architect es la persona que diseña edificios."),
            listen(f"{p}.e02", "Escucha y selecciona el objeto definido.",
                   "It is a tool which shows whether a surface is level.",
                   ["A workshop", "A builder", "A spirit level"], 2, c, "evaluation",
                   "A spirit level es la herramienta que comprueba si una superficie está nivelada."),
            q(f"{p}.e03", "Elige el lugar where legal documents are officially recorded.",
              ["A registry office", "A filing cabinet", "A legal adviser"], 0, c,
              "evaluation", "A registry office es el lugar donde se registran documentos oficiales."),
            write(f"{p}.e04", "Escribe 70–90 palabras con tres acertijos funcionales.",
                  "Persona: revisa audición de adultos y niños/explica resultados. Objeto: amplifica sonido/se lleva dentro o detrás de la oreja. Lugar: pruebas auditivas/salas silenciosas con equipo. No nombres respuestas; usa who, which/that y where.",
                  "The first is someone who tests how well people can hear and explains the results clearly. This person works with adults and children. The second is a small device which makes sounds louder and fits behind or inside an ear. The third is a quiet place where people complete hearing tests and discuss suitable support. Its rooms have special equipment. Identify the professional, the object and the place from these clues.",
                  "One is a professional who measures hearing and discusses each result clearly with the client. The next is an object that increases sound and can be worn in or behind the ear. The last is a place where hearing is tested in quiet rooms with specialist equipment. Each riddle gives a function and one extra clue. Can you identify the person, the device and the service location without their names?",
                  c, "evaluation", "Los tres acertijos usan who, which/that y where con referentes recuperables."),
        ],
        "review": [
            q(f"{p}.r01", "¿Qué tipo de referente introduce a place where...?",
              ["A person", "A location", "An object"], 1, c, "review",
              "A place where introduce necesariamente un lugar."),
            match(f"{p}.r02", "Relaciona pistas nuevas con sus soluciones.",
                  [("someone who restores old paintings", "art restorer"),
                   ("a device that controls room temperature", "thermostat"),
                   ("a place where local records are studied", "archive")], c, "review",
                  "Cada solución se apoya en una función única dentro de su categoría."),
            write(f"{p}.r03", "Escribe 70–90 palabras con otros tres acertijos.",
                  "Persona: repara frenos, cambios y ruedas/comprueba seguridad. Objeto: infla neumáticos/tiene medidor. Lugar: guardar bicicletas/tiene soportes y entrada cerrada. Sin nombres.",
                  "The first is someone who repairs brakes, gears and damaged wheels for cyclists. This person also checks whether a bike is safe. The second is a tool that pushes air into tyres and usually has a pressure gauge. The third is a secure place where residents leave bicycles during the day. It has racks and a locked entrance. Use the clues to identify the worker, the object and the location.",
                  "One is a person who fixes bicycle parts and checks bikes before a journey. Another is an object which fills tyres with air and shows their pressure. The final one is a place where people keep bicycles securely while they work or shop. It contains racks and requires a key. Identify all three references from their functions and supporting details, without using the missing names or guessing any missing information.",
                  c, "review", "La recuperación mantiene tres tipos de antecedente y dos pistas observables por cada uno."),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-39.t02", f"{p}.r02"),
             f"{p}.e02": ("en.n3.class-39.t03", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-39.t04", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-39.t06", f"{p}.r03")}
    return make_class(n, ["Crear tres acertijos para persona, objeto y lugar.",
                          "Mantener los tres referentes identificables en 70–90 palabras."],
        [("riddle", "acertijo"), ("identify", "identificar"), ("clue", "pista"),
         ("function", "función"), ("object", "objeto"), ("location", "lugar")],
        [("A riddle defines a referent without naming it.",
          "Un acertijo define un referente sin nombrarlo.", "La función sustituye el nombre ausente."),
         ("Use who for the person someone must identify.",
          "Usa who para la persona que se debe identificar.", "La pista explica qué hace esa persona."),
         ("Use which or that for the object.",
          "Usa which o that para el objeto.", "La función debe distinguirlo de herramientas similares."),
         ("Use where for the location.", "Usa where para el lugar.",
          "La actividad situada allí permite reconocerlo."),
         ("Give one function and one supporting clue for each referent.",
          "Da una función y una pista adicional para cada referente.", "Dos datos hacen la solución inequívoca."),
         ("Write three linked riddles: one person who performs a task, one object that has a function, and one place where an activity happens. Add a second clue to each riddle, but do not use any answer as a name. Finish by asking the listener to identify all three. This structure keeps the person, object and location distinct and recoverable. Make every clue specific enough that a partner can solve it confidently.",
          "Escribe tres acertijos enlazados: persona, objeto y lugar, con dos pistas cada uno.",
          "El modelo integrado cubre los tres antecedentes sin revelar las soluciones.")],
        pools, remap)


def build_40() -> dict[str, Any]:
    n, c, p = 40, CONCEPTS[40], "en.n3.c40"
    all_c = [CONCEPTS[k] for k in NUMBERS]
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la frase que define a la persona que ayuda.",
              ["Ask for Mina, who repairs hiking boots.", "Use the service which cleans boots.",
               "Visit the shop where boots are sold."], 0, c, "practiceGuided",
              "Who repairs hiking boots define a Mina por su función.",
              hint="Busca un nombre de persona seguido de who."),
            listen(f"{p}.pg02", "Escucha y elige el servicio descrito.",
                   "Green Fix offers a service which collects broken lamps from your home.",
                   ["Home painting", "Lamp collection", "Garden design"], 1, c,
                   "practiceGuided", "Which collects broken lamps identifica el servicio de recogida."),
            order(f"{p}.pg03", "Ordena la definición del lugar recomendado.",
                  "It is a workshop where customers can watch the repair.", c, "practiceGuided",
                  "Where enlaza el taller con la actividad disponible allí.",
                  hint="Coloca where después de workshop."),
        ],
        "practice": [
            match(f"{p}.p01", "Une cada dato con persona, servicio o lugar.",
                  [("Ravi, who fits locks", "person"),
                   ("a plan which includes a home visit", "service"),
                   ("a centre where evening appointments happen", "place")], c, "practice",
                  "Los relativos permiten distinguir los tres referentes antes de recomendar."),
            q(f"{p}.p02", "¿Qué razón justifica elegir el taller cercano?",
              ["It is where same-day repairs are completed.", "Its sign is green.",
               "A different shop opens next month."], 0, c, "practice",
              "La reparación en el mismo día es un beneficio funcional del lugar."),
            write(f"{p}.p03", "Recomienda un servicio con who, which y where.",
                  "Nora repara cremalleras; servicio incluye recogida; taller junto a estación.",
                  "I recommend Nora, who repairs zips. Choose the service which includes collection from the workshop where she works beside the station.",
                  "Nora is the specialist who repairs zips. She offers a collection service which operates from the workshop where she works beside the station.",
                  c, "practice", "Las variantes identifican persona, servicio y lugar antes de recomendar."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Elige al profesional que cumple la necesidad indicada.",
              ["Ivo, who repairs electric bikes", "Lena, who rents ordinary bikes",
               "Sam, who sells cycling maps"], 0, c, "evaluation",
              "Ivo es la única persona definida por reparar bicicletas eléctricas."),
            listen(f"{p}.e02", "Escucha y selecciona el servicio con recogida.",
                   "Quick Wheel offers a repair plan which includes collection; Cycle Corner requires delivery to its shop.",
                   ["Cycle Corner shop service", "Neither service", "Quick Wheel repair plan"], 2,
                   c, "evaluation", "Which includes collection identifica el plan de Quick Wheel."),
            write(f"{p}.e03", "Describe persona, servicio y lugar antes de recomendar.",
                  "Tariq ajusta frenos; revisión incluye luces; taller junto al mercado.",
                  "Tariq is the mechanic who adjusts brakes. The check which includes the lights is available at the workshop where customers wait beside the market. I recommend it.",
                  "I recommend Tariq, who adjusts brakes, and the check that includes the lights at the workshop where clients wait next to the market.",
                  c, "evaluation", "Las respuestas definen los tres referentes y cierran una recomendación explícita."),
            write(f"{p}.e04", "Escribe 80–110 palabras y recomienda un taller de bicicletas.",
                  "Necesidad: e-bike y recogida. Quick Wheel: Ivo repara e-bikes; plan Home Collect recoge y devuelve; taller Riverside junto al puente. Cycle Corner: Lena repara bicis normales; Standard Check sin recogida; taller Market Yard junto al mercado. Compara y recomienda.",
                  "Quick Wheel is the better option for this request. Ivo is the mechanic who repairs electric bikes, while Lena at Cycle Corner repairs ordinary bikes. Home Collect is the plan which collects and returns the bicycle; Standard Check requires the customer to deliver it. Riverside is the workshop where Quick Wheel completes the repair beside the bridge. Market Yard is where Cycle Corner works beside the market. I recommend Quick Wheel because its specialist, service and location match the electric-bike and collection needs exactly.",
                  "I would choose Quick Wheel rather than Cycle Corner. Ivo, who repairs electric bikes, matches the required person; Lena only repairs ordinary models. Home Collect is a service that collects and returns the bike, but Standard Check has no collection. Riverside is the place where Ivo carries out repairs near the bridge, whereas Market Yard is beside the market. Quick Wheel is my final recommendation because the defined mechanic and collection plan meet both needs, and the workshop is clearly identified.",
                  c, "evaluation", "Ambas versiones comparan dos talleres y basan la recomendación en tres referentes definidos.",
                  requires=all_c),
        ],
        "review": [
            q(f"{p}.r01", "¿Qué opción define persona, servicio y lugar?",
              ["Jo teaches, and the centre is nice.",
               "Jo, who tutors adults, offers a plan which includes feedback at a centre where evening lessons happen.",
               "Lessons are useful in many places."], 1,
              c, "review", "La segunda opción contiene los tres relativos y tres referentes claros."),
            match(f"{p}.r02", "Relaciona los referentes de dos servicios de estudio.",
                  [("Mei, who teaches exam writing", "person"),
                   ("Review Plus, which includes weekly feedback", "service"),
                   ("North Hub, where evening sessions happen", "place")], c, "review",
                  "Cada relativo aporta la función necesaria para identificar el referente."),
            write(f"{p}.r03", "Escribe 80–110 palabras y recomienda apoyo informático.",
                  "Necesidad: recuperar archivos y visita a domicilio. Data Help: Noor recupera archivos; Home Visit incluye desplazamiento; taller East Lab junto a biblioteca. Byte Shop: Eli instala programas; Counter Repair exige llevar equipo; tienda West Arcade. Compara y recomienda.",
                  "Data Help fits the request better than Byte Shop. Noor is the specialist who recovers lost files, whereas Eli installs software. Home Visit is the service which sends Noor to the customer's home; Counter Repair requires the computer to be taken to the shop. East Lab is the workshop where Data Help is based beside the library. West Arcade is where Byte Shop receives equipment. I recommend Data Help because the defined person and home service meet both needs, and its location is also clear.",
                  "I recommend Data Help rather than Byte Shop. Noor, who recovers lost files, provides the required expertise; Eli only installs programs. Home Visit is a plan that includes travel to the customer's address, while Counter Repair needs shop delivery. East Lab is the place where Data Help works near the library. Byte Shop works at West Arcade. Data Help is the stronger choice because its specialist, service and clearly described workshop support both file recovery and a home appointment.",
                  c, "review", "Las variantes comparan dos servicios y justifican la elección con persona, plan y lugar.",
                  requires=all_c),
        ],
    }
    remap = {f"{p}.e01": ("en.n3.class-40.t02", f"{p}.r02"),
             f"{p}.e02": ("en.n3.class-40.t03", f"{p}.r02"),
             f"{p}.e03": ("en.n3.class-40.t05", f"{p}.r01"),
             f"{p}.e04": ("en.n3.class-40.t06", f"{p}.r03")}
    return make_class(n, ["Comparar dos servicios mediante persona, oferta y lugar definidos.",
                          "Recomendar una opción en 80–110 palabras usando who, which/that y where."],
        [("recommend", "recomendar"), ("compare", "comparar"), ("assistant", "especialista"),
         ("service", "servicio"), ("workshop", "taller"), ("reason", "razón")],
        [("Recommend only after checking the stated need.",
          "Recomienda solo después de comprobar la necesidad indicada.", "La elección debe basarse en los datos visibles."),
         ("Define the assistant with who or that.",
          "Define al especialista con who o that.", "La función profesional identifica a la persona."),
         ("Define the service with which or that.",
          "Define el servicio con which o that.", "La oferta descrita debe responder a la necesidad."),
         ("Define the workshop with where.",
          "Define el taller con where.", "La actividad o ubicación distingue el lugar."),
         ("Compare both options before giving a reason.",
          "Compara ambas opciones antes de dar una razón.", "La recomendación final debe derivarse de las tres definiciones."),
         ("For local pet care, compare two services. Alma is the vet who treats birds; Bruno treats only cats and dogs. Bird Home Care is a service which includes a home visit; Pet Desk requires an office visit. River Clinic is the place where Alma examines birds near the park; Central Pets is where Bruno works by the station. I recommend Alma and Bird Home Care because the person, service and place meet the bird and home-visit needs, unlike the second option.",
          "El modelo compara dos servicios veterinarios y recomienda mediante persona, servicio y lugar definidos.",
          "El escenario integra who, which, where, tres referentes claros y una recomendación basada en ellos.")],
        pools, remap, uses=all_c, cumulative=all_c)


BUILDERS = {36: build_36, 37: build_37, 38: build_38, 39: build_39, 40: build_40}


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
        e04=next(x for x in close["pools"]["evaluation"] if x["id"]=="en.n3.c40.e04")
        r03=next(x for x in close["pools"]["review"] if x["id"]=="en.n3.c40.r03")
        assert e04["requires"]==expected and r03["requires"]==expected
        t06=close["teaching"][-1]["en"].casefold(); ea=e04["answer"]["text"].casefold(); ra=r03["answer"]["text"].casefold()
        assert "pet care" in t06 and "quick wheel" in ea and "data help" in ra
        for text in (t06,ea,ra):
            assert " who " in f" {text} " and (" which " in f" {text} " or " that " in f" {text} ")
            assert " where " in f" {text} " and ("recommend" in text or "choose" in text)
            count = len(re.findall(r"\b[\w’-]+\b", text))
            assert 80 <= count <= 110, count
        c36 = classes[0]
        c36e04 = next(x for x in c36["pools"]["evaluation"] if x["id"] == "en.n3.c36.e04")
        c36r02 = next(x for x in c36["pools"]["review"] if x["id"] == "en.n3.c36.r02")
        assert len(c36e04["answer"]["pairs"]) == 5 and len(c36r02["answer"]["pairs"]) == 5
        assert "4 de 5" in c36e04["prompt"]["es"]
        assert c36e04["origin"]["scoring"] == {"parts": 5, "minimumCorrect": 4, "independentAttempt": True}
        for pair in c36e04["answer"]["pairs"]:
            definition = pair[1]["es"].casefold()
            assert " who " in f" {definition} " or " that " in f" {definition} "
        c37 = classes[1]
        for item_id, pool in (("en.n3.c37.e04", "evaluation"), ("en.n3.c37.r03", "review")):
            item = next(x for x in c37["pools"][pool] if x["id"] == item_id)
            assert item["format"] == "completar" and len(item["answer"]["parts"]) == 6
            answers = [part["text"].casefold() for part in item["answer"]["parts"]]
            assert answers.count("where") == 3
            assert sum(answer in {"which", "that"} for answer in answers) == 3
        c37e04 = next(x for x in c37["pools"]["evaluation"] if x["id"] == "en.n3.c37.e04")
        assert c37e04["origin"]["scoring"] == {"parts": 6, "minimumCorrect": 5, "independentAttempt": True}
        c38 = classes[2]
        c38e04 = next(x for x in c38["pools"]["evaluation"] if x["id"] == "en.n3.c38.e04")
        advert = c38e04["origin"]["text"].casefold()
        assert all(token in advert for token in (" who ", " which ", " where "))
        assert all(label in c38e04["answer"]["text"].casefold() for label in ("person:", "object:", "place:"))
        c39 = classes[3]
        c39e04 = next(x for x in c39["pools"]["evaluation"] if x["id"] == "en.n3.c39.e04")
        c39r03 = next(x for x in c39["pools"]["review"] if x["id"] == "en.n3.c39.r03")
        for text in (c39["teaching"][-1]["en"], *c39e04["answer"]["accepted"], *c39r03["answer"]["accepted"]):
            lowered = text.casefold()
            count = len(re.findall(r"\b[\w’-]+\b", text))
            assert 70 <= count <= 90, count
            assert " who " in f" {lowered} " and (" which " in f" {lowered} " or " that " in f" {lowered} ")
            assert " where " in f" {lowered} "
    return {"classes":len(classes),"items":sum(totals.values()),"pools":dict(totals),
            "formats":dict(sorted(formats.items())),"correctIndices":dict(sorted(indices.items())),
            "prompts":len(prompts),"fingerprints":len(signatures)}


def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_in_memory() -> dict[str, Any]:
    first = [BUILDERS[n]() for n in NUMBERS]
    second = [BUILDERS[n]() for n in NUMBERS]
    assert canonical(first) == canonical(second), "non-deterministic in-memory generation"
    return audit(first, True)


def write_class(n: int) -> Path:
    doc=BUILDERS[n](); audit([doc],False); path=OUT/f"class-{n:02d}.json"
    path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); return path


def write_bundle() -> tuple[Path,dict[str,Any]]:
    classes=[json.loads((OUT/f"class-{n:02d}.json").read_text()) for n in NUMBERS]; summary=audit(classes,True)
    doc={"schema":"onelingo.editorial.class-bundle.v1","course":"en","level":3,"scale":SCALE,
         "status":"shadow","runtimeAi":False,"selectionPolicy":{"deterministic":True},
         "evidencePolicy":{"attemptRecords":["variantId","libraryVersion","selectionId"]},
         "range":{"start":36,"end":40},"classes":classes}
    path=OUT/"bundle-36-40.json"; path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return path,summary


def write_report(paths:list[Path], summary:dict[str,Any])->Path:
    hashes="\n".join(f"{digest(p)}  {p.name}" for p in paths)
    text=f"""# GO — Inglés N3 C36–C40

Estado: **GO independiente; integrado en shadow, no autorizado para activación**.

## Alcance

- Bloque `defining-information`, entrada B1, fases `input → form → comprehension → production → transfer`.
- Cinco clases, 65 ejercicios y contrato `editorial-agent.v2`.
- `status: shadow`, `runtimeAi: false`, selección y recuperación deterministas.

## Cierre C40

- `t06`: comparación de dos servicios veterinarios locales.
- `e04`: comparación de dos talleres de bicicletas.
- `r03`: comparación de dos servicios de apoyo informático.
- Cada escenario define persona con who/that, servicio con which/that y lugar con where,
  mantiene tres referentes inequívocos y basa la recomendación en esas definiciones.

## Auditoría

```json
{json.dumps(summary,ensure_ascii=False,indent=2)}
```

## Validación reproducible

- El generador construye el bloque dos veces en memoria, compara su forma canónica y ejecuta
  las aserciones editoriales antes de escribir archivos.
- La entrega del autor fue verificada en una copia temporal: cinco clases individuales y el
  bundle level 3 devolvieron `OK`; dos ejecuciones consecutivas conservaron todos los hashes.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/contenido/generar_editorial_n3_36_40.py --all
for n in 36 37 38 39 40; do python3 tools/contenido/validar_bundle_editorial.py --file assets/contenido/en/editorial/n3/class-$n.json --start $n --end $n --level 3; done
python3 tools/contenido/validar_bundle_editorial.py --file assets/contenido/en/editorial/n3/bundle-36-40.json --start 36 --end 40 --level 3
```

## Hashes

```text
{hashes}
```

Revisión independiente: `GO`; integración únicamente en `shadow`.
"""
    path=REPORT_OUT/"REPORT.md"; path.write_text(text,encoding="utf-8"); return path


def write_all()->list[Path]:
    memory_summary=verify_in_memory()
    REPORT_OUT.mkdir(parents=True,exist_ok=True)
    classes=[write_class(n) for n in NUMBERS]; bundle,summary=write_bundle()
    assert summary == memory_summary
    report=write_report(classes+[bundle],summary)
    files=classes+[bundle,report]; manifest=REPORT_OUT/"MANIFEST.sha256"
    entries=[f"{digest(Path(__file__))}  ../../tools/contenido/generar_editorial_n3_36_40.py",
             f"{digest(MAP)}  ../../assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"]
    entries.extend(f"{digest(p)}  {p.name if p.parent == REPORT_OUT else '../../' + str(p.relative_to(ROOT))}" for p in files)
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
