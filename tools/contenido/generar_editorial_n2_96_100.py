#!/usr/bin/env python3
"""Generate the isolated English N2 C96-C100 editorial draft."""

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
    96: "n2-review-time-tense",
    97: "n2-review-quantity-comparison",
    98: "n2-review-modals-interaction",
    99: "n2-integrated-a2-project",
    100: "n2-final-a2-performance",
}
PHASES = {96: "input", 97: "form", 98: "comprehension", 99: "production", 100: "transfer"}
TITLES = {
    96: ("Review: time and tense", "Repaso: tiempo y tiempos verbales"),
    97: ("Review: quantity and comparison", "Repaso: cantidad y comparación"),
    98: ("Review: modals and interaction", "Repaso: modales e interacción"),
    99: ("Integrated A2 project", "Proyecto integrado A2"),
    100: ("Final A2 performance", "Desempeño final A2"),
}
QUALITY_POLICY = {
    "chronologyTokens": "enforce", "answerReuseAcrossEarlyReserved": "forbid",
    "answerEvidenceReuseAcrossPools": "forbid", "agentContract": "editorial-agent.v2",
    "minChoices": 3, "maxPromptCharacters": 90,
    "feedbackReuseWithinClass": "forbid", "minClassFormats": 4,
}
EXPECTED_INDICES = Counter({0: 7, 1: 11, 2: 7})


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def hashed(item: dict[str, Any]) -> dict[str, Any]:
    payload = {key: value for key, value in item.items() if key not in {"id", "contentHash"}}
    item["contentHash"] = "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()
    return item


def base(item_id: str, fmt: str, prompt: str, concept: str, pool: str, feedback: str,
         requires: list[str] | None = None, hint: str | None = None) -> dict[str, Any]:
    origin: dict[str, Any] = {"kind": "editorial", "feedback": {"es": feedback}}
    if pool == "practiceGuided":
        origin["hint"] = {"es": hint or "Identifica la función y los datos antes de responder."}
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
    x["choices"], x["answer"] = [{"text": value} for value in options], {"index": index}
    return hashed(x)


def l(i: str, prompt: str, audio: str, options: list[str], index: int, c: str, pool: str,
      feedback: str, *, requires: list[str] | None = None) -> dict[str, Any]:
    x = base(i, "escuchar", prompt, c, pool, feedback, requires)
    x["choices"], x["answer"] = [{"text": value} for value in options], {"index": index}
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
    x["answer"], x["origin"]["pairs"] = {"pairs": values}, values
    return hashed(x)


def lessons(number: int, rows: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    result = []
    for index, (en, es, explanation) in enumerate(rows, 1):
        ew, sw = en.split(), es.split()
        em, sm = max(1, len(ew) // 2), max(1, len(sw) // 2)
        result.append({"id": f"en.n2.class-{number}.t{index:02d}", "en": en, "es": es,
                       "explanationEs": explanation,
                       "segments": [{"en": " ".join(ew[:em]), "es": " ".join(sw[:sm])},
                                    {"en": " ".join(ew[em:]), "es": " ".join(sw[sm:])}],
                       "audioText": en, "audioMode": "tts", "languageCode": "en",
                       "patternId": CONCEPTS[number]})
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
        "teaching": lessons(number, lesson_rows), "pools": pools,
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


def build_96() -> dict[str, Any]:
    n, c, p = 96, CONCEPTS[96], "en.n2.c96"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la frase que describe una rutina de cada lunes.",
              ["I check the schedule every Monday.", "I checked the schedule yesterday.",
               "I am checking the schedule now."], 0, c, "practiceGuided",
              "Every Monday exige presente simple para una rutina repetida.",
              hint="Relaciona el marcador semanal con una acción habitual."),
            f(f"{p}.pg02", "Usa el pasado de call: Yesterday, I ___ the clinic.", "called", c,
              "practiceGuided", "Called sitúa la llamada en el pasado terminado de yesterday.",
              hint="El marcador yesterday necesita la forma pasada regular."),
            o(f"{p}.pg03", "Ordena la actividad que ocurre en este momento.",
              "I am preparing the report now.", c, "practiceGuided",
              "Am preparing combina presente continuo con now.",
              hint="Coloca am antes del verbo terminado en -ing."),
        ],
        "practice": [
            w(f"{p}.p01", "Escribe el plan de Leo para mañana por la tarde.",
              "Leo: visitar a su abuela mañana por la tarde.",
              "Leo is going to visit his grandmother tomorrow afternoon.",
              "Tomorrow afternoon, Leo is going to visit his grandmother.", c, "practice",
              "Ambas variantes conservan la intención, la visita y el momento futuro."),
            l(f"{p}.p02", "Escucha y selecciona desde cuándo trabaja Mia allí.",
              "Mia has worked at the library since March.",
              ["Since Monday", "For three months", "Since March"], 2, c, "practice",
              "Since March identifica el punto inicial exacto del trabajo de Mia."),
            m(f"{p}.p03", "Relaciona cada marcador con el tiempo que activa.",
              [("usually", "rutina presente"), ("yesterday", "pasado terminado")], c,
              "practice", "Usually señala hábito y yesterday sitúa una acción acabada."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Omar revisa el inventario de lunes a viernes. Elige su frase.",
              ["Omar checks the inventory on weekdays.",
               "Omar checked the inventory last night.",
               "Omar is checking the inventory tomorrow."], 0, c, "evaluation",
              "Checks on weekdays expresa una rutina que ocurre durante la semana."),
            q(f"{p}.e02", "Ben llegó en 2024 y todavía vive aquí. Elige el informe correcto.",
              ["Ben lived here until 2024.", "Ben will live here after 2024.",
               "Ben has lived here since 2024."], 2, c, "evaluation",
              "Has lived y since conectan la llegada en 2024 con la situación actual."),
            w(f"{p}.e03", "Redacta tres oraciones con ayer, ahora y mañana.",
              "Ayer: terminé el presupuesto. Ahora: reviso precios. Mañana: compraré materiales.",
              "Yesterday, I finished the budget. Now I am checking prices. Tomorrow, I am going to buy materials.",
              "I finished the budget yesterday. I am checking prices now, and I am going to buy materials tomorrow.",
              c, "evaluation", "La respuesta separa un hecho pasado, una acción actual y un plan futuro."),
            l(f"{p}.e04", "Escucha y elige la tarea que Kim acaba de completar.",
              "Kim has just paid the invoice, but she has not posted the receipt yet.",
              ["Posting the receipt", "Paying the invoice", "Calling the supplier"], 1, c,
              "evaluation", "Has just paid señala que el pago acaba de terminar."),
        ],
        "review": [
            m(f"{p}.r01", "Une cada expresión temporal con la forma verbal adecuada.",
              [("on school days", "walks"), ("since last June", "has studied"),
               ("has just finished", "resultado reciente")], c, "review",
              "La frecuencia usa presente; since conecta con ahora y just marca un resultado reciente."),
            o(f"{p}.r02", "Ordena el plan confirmado para mañana a las ocho.",
              "We are meeting at eight tomorrow.", c, "review",
              "El presente continuo y tomorrow expresan un arreglo futuro concreto."),
            w(f"{p}.r03", "Escribe otra actualización con tres momentos.",
              "Ayer: llamé a Ana. Ahora: preparo notas. Mañana: tendremos reunión.",
              "Yesterday, I called Ana. Now I am preparing notes. Tomorrow, we are going to have a meeting.",
              "I called Ana yesterday. I am preparing notes now, and we are going to meet tomorrow.",
              c, "review", "La recuperación vuelve a distinguir pasado, presente en curso y futuro."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n2.class-{n}.t01", f"{p}.r01"),
             f"{p}.e02": (f"en.n2.class-{n}.t05", f"{p}.r01"),
             f"{p}.e03": (f"en.n2.class-{n}.t06", f"{p}.r03"),
             f"{p}.e04": (f"en.n2.class-{n}.t05", f"{p}.r01")}
    return make_class(n,
        ["Elegir una forma verbal mediante marcadores temporales claros.",
         "Distinguir rutina, pasado terminado, acción actual y plan futuro.",
         "Producir una actualización breve con tres momentos."],
        [("yesterday", "ayer"), ("usually", "normalmente"), ("now", "ahora"),
         ("tomorrow", "mañana"), ("since", "desde"), ("already", "ya"),
         ("schedule", "horario"), ("plan", "planificación")],
        [("I usually check the schedule every Monday.",
          "Normalmente reviso el horario cada lunes.",
          "Usually y every Monday activan presente simple para una rutina."),
         ("I am preparing the plan now.", "Estoy preparando el plan ahora.",
          "Now combina con presente continuo para una acción en curso."),
         ("Yesterday, I finished the report.", "Ayer terminé el informe.",
          "Yesterday sitúa una acción completa en pasado simple."),
         ("Tomorrow, I am going to call the clinic.", "Mañana voy a llamar a la clínica.",
          "Be going to presenta una intención futura con momento explícito."),
         ("I have worked here since March and already know the schedule.",
          "Trabajo aquí desde marzo y ya conozco el horario.",
          "Since introduce el punto inicial y already señala progreso hasta ahora."),
         ("Yesterday I called; now I am writing, and tomorrow I will visit.",
          "Ayer llamé; ahora escribo y mañana haré una visita.",
          "Una actualización integrada asigna una forma distinta a ayer, ahora y mañana.")], pools, remap)


def build_97() -> dict[str, Any]:
    n, c, p = 97, CONCEPTS[97], "en.n2.c97"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Hay ocho personas y diez tazas. Elige la conclusión exacta.",
              ["There are too few cups.", "There are enough cups.", "There is too much coffee."],
              1, c, "practiceGuided", "Diez tazas para ocho personas forman una cantidad suficiente.",
              hint="Compara primero las personas con los objetos disponibles."),
            f(f"{p}.pg02", "Usa fewer con chairs: We need ___ chairs than last year.", "fewer", c,
              "practiceGuided", "Fewer acompaña al sustantivo contable plural chairs.",
              hint="La consigna pide el comparador para objetos contables."),
            o(f"{p}.pg03", "Ordena la comparación de igualdad entre dos salas.",
              "Room A is as large as Room B.", c, "practiceGuided",
              "As large as indica que las dos salas tienen el mismo tamaño.",
              hint="Coloca as a ambos lados del adjetivo large."),
        ],
        "practice": [
            w(f"{p}.p01", "Escribe la cantidad suficiente para el grupo.",
              "Seis estudiantes; ocho cuadernos disponibles.",
              "Eight notebooks are enough for six students.",
              "For six students, eight notebooks are enough.", c, "practice",
              "Las variantes conservan seis estudiantes, ocho cuadernos y suficiencia."),
            l(f"{p}.p02", "Escucha y selecciona la opción más económica.",
              "The blue room costs thirty dollars. The green room costs twenty-five.",
              ["The green room", "Both rooms cost thirty dollars", "The blue room"], 0, c,
              "practice", "Veinticinco es menos que treinta, por eso la sala verde es más barata."),
            m(f"{p}.p03", "Relaciona cada comparador con el sustantivo adecuado.",
              [("fewer", "chairs"), ("less", "water"),
               ("as large as", "the same size")], c, "practice",
              "Fewer y less distinguen cantidad; as large as expresa igualdad de tamaño."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Tres habitaciones cuestan $40, $55 y $70. Elige la más barata.",
              ["The $70 room is the cheapest.", "The $40 room is the cheapest.",
               "The $55 room is the cheapest."], 1, c, "evaluation",
              "Cuarenta dólares es el precio menor, por eso esa habitación es the cheapest."),
            q(f"{p}.e02", "El plan A cuesta $18 y el B, $25. Elige la comparación correcta.",
              ["Plan A is cheaper than Plan B.", "Plan B is cheaper than Plan A.",
               "Plan A is as expensive as Plan B."], 0, c, "evaluation",
              "Dieciocho es menor que veinticinco, así que el plan A es cheaper."),
            w(f"{p}.e03", "Compara las opciones e indica cuál alcanza.",
              "Grupo: 12. Caja A: 10 vasos, $8. Caja B: 15 vasos, $10.",
              "Box B is more expensive than Box A, but it has enough cups for twelve people.",
              "Box A is cheaper, but only Box B has enough cups for the group of twelve.",
              c, "evaluation", "Ambas variantes comparan precio y explican qué caja tiene cantidad suficiente."),
            l(f"{p}.e04", "Escucha y elige la descripción exacta de la situación.",
              "There are fewer buses today, but we have enough time to wait.",
              ["More buses and too little time", "Fewer buses but enough time",
               "The same number of buses and more time"], 1, c, "evaluation",
              "Fewer describe menos autobuses y enough confirma que el tiempo alcanza."),
        ],
        "review": [
            m(f"{p}.r01", "Une cada situación con su descripción cuantitativa.",
              [("fewer lamps", "cantidad contable menor"),
               ("less paint", "cantidad no contable menor"),
               ("enough rice", "cantidad suficiente")], c, "review",
              "Fewer se usa con objetos, less con sustancias y enough confirma suficiencia."),
            o(f"{p}.r02", "Ordena la igualdad de precio entre los dos menús.",
              "Menu X is as expensive as Menu Y.", c, "review",
              "As expensive as recupera una comparación donde los dos precios son iguales."),
            w(f"{p}.r03", "Escribe otra decisión con cantidad y precio.",
              "Equipo: 9. X: 12 lápices/$7. Y: 8/$6. Z: 10/$5.",
              "Package Z is the cheapest and has enough pencils for the team of nine.",
              "For nine people, Package Z is the best choice because ten pencils are enough and five dollars is the lowest price.",
              c, "review", "La recuperación compara tres precios y verifica la cantidad necesaria."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n2.class-{n}.t05", f"{p}.r03"),
             f"{p}.e02": (f"en.n2.class-{n}.t04", f"{p}.r03"),
             f"{p}.e03": (f"en.n2.class-{n}.t03", f"{p}.r03"),
             f"{p}.e04": (f"en.n2.class-{n}.t02", f"{p}.r01")}
    return make_class(n,
        ["Elegir fewer, less y enough según el tipo y la cantidad.",
         "Comparar dos opciones y reconocer la mejor entre tres.",
         "Justificar una decisión breve con precio y suficiencia."],
        [("enough", "suficiente"), ("fewer", "menos contables"), ("less", "menos no contable"),
         ("more", "más"), ("cheaper", "más barato"), ("best", "mejor"),
         ("than", "que"), ("large", "grande")],
        [("We have enough chairs for every guest.", "Tenemos suficientes sillas para cada invitado.",
          "Enough confirma que la cantidad cubre la necesidad."),
         ("We need fewer plates and less water.", "Necesitamos menos platos y menos agua.",
          "Fewer modifica contables; less modifica cantidades no contables."),
         ("Plan A has more tickets, but Plan B has enough.",
          "El plan A tiene más entradas, pero el plan B tiene suficientes.",
          "More compara cantidad y enough verifica el mínimo requerido."),
         ("The bus is cheaper than the train.", "El autobús es más barato que el tren.",
          "Cheaper than compara una cualidad entre dos opciones."),
         ("Of the three routes, the fastest route is the best for us.",
          "De las tres rutas, la más rápida es la mejor para nosotros.",
          "Best selecciona una opción dentro de un grupo de tres o más."),
         ("Room A is as large as Room B.", "La sala A es tan grande como la sala B.",
          "As large as expresa igualdad en una comparación.")], pools, remap)


def build_98() -> dict[str, Any]:
    n, c, p = 98, CONCEPTS[98], "en.n2.c98"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige la petición cortés para recibir ayuda con una caja.",
              ["You must carry my box.", "May I carry your box?",
               "Could you help me carry this box, please?"], 2, c, "practiceGuided",
              "Could you help me...? pide una acción concreta con cortesía.",
              hint="Busca una pregunta dirigida a la otra persona con please."),
            f(f"{p}.pg02", "Usa mustn't para la prohibición: Visitors ___ enter this room.",
              "mustn't", c, "practiceGuided",
              "Mustn't enter comunica una prohibición, no ausencia de necesidad.",
              hint="La consigna pide la forma contraída de una regla negativa."),
            o(f"{p}.pg03", "Ordena la respuesta cortés que acepta una petición.",
              "Yes, of course; I can help you.", c, "practiceGuided",
              "Of course y can help aceptan la petición de manera clara.",
              hint="Empieza con la aceptación y termina con la ayuda ofrecida."),
        ],
        "practice": [
            w(f"{p}.p01", "Escribe una petición para cerrar la ventana.",
              "Pedir a Alex que cierre la ventana, por favor.",
              "Alex, could you close the window, please?",
              "Could you please close the window, Alex?", c, "practice",
              "Las dos variantes mantienen destinatario, acción y cortesía."),
            l(f"{p}.p02", "Escucha y elige lo que solicita permiso para hacer Sara.",
              "May I use the meeting room after lunch?",
              ["Use the room before lunch", "Use the room after lunch", "Book lunch for the room"],
              1, c, "practice", "May I use solicita permiso para usar la sala después del almuerzo."),
            m(f"{p}.p03", "Relaciona cada modal con su función comunicativa.",
              [("should", "consejo"), ("have to", "requisito externo"),
               ("mustn't", "prohibición")], c, "practice",
              "Should aconseja, have to marca un requisito y mustn't prohíbe una acción."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Lina está cansada. Elige un consejo, no una orden.",
              ["Lina, you should take a short break.", "Lina, you must finish now.",
               "Lina, could you finish the report now?"], 0, c, "evaluation",
              "Should take a short break mantiene la fuerza de un consejo."),
            q(f"{p}.e02", "La empresa exige identificación al personal. Elige la regla.",
              ["Staff may wear an ID badge at work.",
               "Staff have to wear an ID badge at work.",
               "Staff should ask for an ID badge someday."], 1, c, "evaluation",
              "Have to wear expresa el requisito externo establecido por la empresa."),
            w(f"{p}.e03", "Redacta la petición y una respuesta positiva.",
              "Nora pide a Luis enviar el horario; Luis acepta.",
              "Nora: Could you send me the schedule, please? Luis: Yes, of course. I can send it now.",
              "Nora: Could you please send the schedule? Luis: Certainly. I can send it now.",
              c, "evaluation", "El intercambio conserva petición, objeto solicitado y aceptación inmediata."),
            l(f"{p}.e04", "Escucha y selecciona la regla que comunica el aviso.",
              "Staff mustn't share the entrance code with visitors.",
              ["Visitors must receive the code.", "Sharing the code is recommended.",
               "Staff are prohibited from sharing the code."], 2, c, "evaluation",
              "Mustn't share comunica que divulgar el código está prohibido."),
        ],
        "review": [
            m(f"{p}.r01", "Une cada inicio con la interacción correspondiente.",
              [("Could you open the door?", "petición"), ("May I sit here?", "permiso")], c,
              "review", "Could you pide acción a otra persona; May I pide autorización propia."),
            o(f"{p}.r02", "Ordena el consejo sobre confirmar la información.",
              "You should ask if the instructions are unclear.", c, "review",
              "Should ask aconseja pedir aclaración cuando falta certeza."),
            w(f"{p}.r03", "Escribe una regla, una petición y una respuesta.",
              "Regla: llevar identificación; prohibido entrar sin ella. Pide mostrarla; acepta.",
              "You have to carry ID and mustn't enter without it. Could you show it, please? Yes, of course.",
              "ID is required, and you must not enter without it. Could you please show it? Certainly.",
              c, "review",
              "La recuperación distingue requisito, prohibición, petición y respuesta cooperativa."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n2.class-{n}.t03", f"{p}.r02"),
             f"{p}.e02": (f"en.n2.class-{n}.t04", f"{p}.r03"),
             f"{p}.e03": (f"en.n2.class-{n}.t01", f"{p}.r03"),
             f"{p}.e04": (f"en.n2.class-{n}.t05", f"{p}.r03")}
    return make_class(n,
        ["Distinguir petición, permiso, consejo, requisito y prohibición.",
         "Responder de forma breve y cortés a otra persona.",
         "Construir un intercambio A2 con un modal adecuado."],
        [("could", "podría"), ("may", "puede"), ("should", "debería"),
         ("mustn't", "no debe"), ("requirement", "requisito"),
         ("permission", "permiso"), ("request", "petición"), ("respond", "responder")],
        [("Could you help me with this request, please?",
          "¿Podrías ayudarme con esta petición, por favor?",
          "Could you...? introduce una request dirigida a otra persona."),
         ("May I use this chair? Yes, you may.", "¿Puedo usar esta silla? Sí, puedes.",
          "May I pide permission y la respuesta repite el modal con claridad."),
         ("You should rest before the meeting.", "Deberías descansar antes de la reunión.",
          "Should comunica consejo y deja la decisión a la persona."),
         ("This requirement means visitors have to show identification.",
          "Este requisito significa que los visitantes tienen que mostrar identificación.",
          "Have to expresa un requisito externo del lugar."),
         ("You mustn't block the emergency exit.",
          "No debes bloquear la salida de emergencia.",
          "Mustn't expresa una prohibición firme por seguridad."),
         ("Please respond politely: Yes, of course, or Sorry, I cannot.",
          "Responde con cortesía: Sí, claro, o Lo siento, no puedo.",
          "Respond completa la interacción aceptando o rechazando sin brusquedad.")], pools, remap)


def build_99() -> dict[str, Any]:
    n, c, p = 99, CONCEPTS[99], "en.n2.c99"
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Elige el objetivo concreto de un proyecto de lectura.",
              ["Create a reading afternoon for ten children on Saturday.",
               "Books are sometimes interesting.", "Maybe do something later."], 0, c,
              "practiceGuided",
              "El objetivo define actividad, grupo y día, por lo que puede comprobarse.",
              hint="Busca una meta con acción, destinatarios y fecha."),
            f(f"{p}.pg02", "Usa deadline: Friday is the ___ for the final list.", "deadline", c,
              "practiceGuided", "Deadline identifica el último día para completar la lista.",
              hint="La consigna pide la palabra que marca el plazo final."),
            o(f"{p}.pg03", "Ordena los pasos básicos antes de enviar una actualización.",
              "First check the materials, then update the project plan.", c, "practiceGuided",
              "First y then organizan revisión y actualización en secuencia.",
              hint="Coloca primero la comprobación y después la actualización."),
        ],
        "practice": [
            w(f"{p}.p01", "Escribe la actualización temporal del proyecto.",
              "Ayer: reservamos sala. Ahora: hacemos carteles. Mañana: invitaremos familias.",
              "Yesterday, we booked the room. Now we are making posters. Tomorrow, we are going to invite families.",
              "We booked the room yesterday. We are making posters now, and we will invite families tomorrow.",
              c, "practice", "La actualización conserva el paso terminado, el actual y el siguiente."),
            l(f"{p}.p02", "Escucha y selecciona la compra suficiente y más barata.",
              "Pack A has twelve markers for nine dollars. Pack B has eight for seven dollars. We need ten.",
              ["Pack B, because it is cheaper", "Both packs have enough markers",
               "Pack A, because it has enough markers"], 2, c, "practice",
              "Solo el paquete A alcanza la necesidad de diez marcadores."),
            m(f"{p}.p03", "Relaciona cada frase del proyecto con su función.",
              [("Could you bring the forms?", "petición"),
               ("We have to finish by Friday.", "requisito y plazo")], c, "practice",
              "La primera coordina ayuda; la segunda fija una obligación con fecha límite."),
        ],
        "evaluation": [
            q(f"{p}.e01", "El equipo terminó el presupuesto ayer. Elige la actualización fiel.",
              ["We are finishing the budget tomorrow.", "We finished the budget yesterday.",
               "We usually finish it next week."], 1, c, "evaluation",
              "Finished y yesterday informan un paso completo del proyecto."),
            q(f"{p}.e02", "Hay 18 entradas para 15 invitados. Elige la conclusión exacta.",
              ["There are not enough tickets.", "There are enough tickets.",
               "There are exactly fifteen tickets."], 1, c, "evaluation",
              "Dieciocho entradas cubren a quince personas, por eso hay enough tickets."),
            w(f"{p}.e03", "Redacta el proyecto breve con todos los datos indicados.",
              "Reunión comunitaria. Ayer: sala pequeña reservada. Ahora: necesitan 15 sillas. "
              "Sala pequeña $30; sala grande $45. Luis debe confirmar acceso a más tardar el jueves. "
              "Pídele a Luis enviar la actualización.",
              "Our project is a community meeting. We booked the small hall yesterday. Now we need fifteen chairs. At thirty dollars, it is cheaper than the forty-five-dollar hall. Luis has to confirm access by Thursday. Luis, could you send the update?",
              "We are planning a community meeting. Yesterday, we reserved the small hall. We now need fifteen chairs. The small hall costs thirty dollars; the large hall costs forty-five, so the small one costs less. Luis must confirm access by Thursday. Could you send the update, Luis?",
              c, "evaluation",
              "El proyecto conserva meta, tiempo, cantidad, comparación, responsable, plazo y petición."),
            l(f"{p}.e04", "Escucha y elige el resumen completo del proyecto.",
              "We reserved the garden yesterday. Now we need twelve gloves. Pack A costs nine dollars and Pack B costs twelve. Ana has to confirm the order by Friday.",
              ["Garden today; ten gloves; no deadline",
               "Garden yesterday; twelve gloves; Pack B; Ana confirms today",
               "Garden yesterday; twelve gloves; Pack A; Ana confirms by Friday"], 2, c,
              "evaluation", "El resumen conserva lugar, tiempo, cantidad, opción barata, responsable y plazo."),
        ],
        "review": [
            m(f"{p}.r01", "Une cada dato con la parte del proyecto que completa.",
              [("reserved the gym on Monday", "lugar y paso terminado"),
               ("fourteen notebooks for eleven learners", "cantidad suficiente"),
               ("Pack C costs $8; Pack D costs $11", "opción C más barata"),
               ("Rita checks the order by Tuesday", "responsable y plazo")], c, "review",
              "La recuperación clasifica lugar, tiempo, cantidad, comparación, responsable y plazo."),
            o(f"{p}.r02", "Ordena el paso que cierra la comparación del presupuesto.",
              "Choose the cheaper option and confirm the budget.", c, "review",
              "La secuencia convierte la comparación en una decisión confirmada."),
            w(f"{p}.r03", "Redacta el plan del taller con todos los datos.",
              "Taller: 8 jóvenes, domingo 11:00. Ayer sala; ahora 10 lápices. X $6, Y $9. Ana confirma sala y recibe petición de actualizar.",
              "Our project is a drawing workshop for eight young people on Sunday at eleven. We booked the room yesterday. Now we need ten pencils. Pack X costs six dollars, so it is cheaper than Pack Y at nine. Ana has to confirm the room. Ana, could you send the update?",
              "We are planning a drawing workshop for eight young people at eleven on Sunday. Yesterday, we reserved the room. We now need ten pencils. Pack Y is nine dollars, but Pack X is only six. Ana must confirm the room. Could you send the update, Ana?",
              c, "review", "La recuperación integra meta, tiempo, cantidad, comparación, obligación y petición."),
        ],
    }
    remap = {f"{p}.e01": (f"en.n2.class-{n}.t02", f"{p}.r01"),
             f"{p}.e02": (f"en.n2.class-{n}.t03", f"{p}.r01"),
             f"{p}.e03": (f"en.n2.class-{n}.t06", f"{p}.r03"),
             f"{p}.e04": (f"en.n2.class-{n}.t06", f"{p}.r01")}
    return make_class(n,
        ["Definir un proyecto A2 con meta, materiales y plazo.",
         "Integrar tiempo, cantidad, comparación y modales en decisiones breves.",
         "Comunicar una actualización con responsables y siguiente paso."],
        [("project", "proyecto"), ("goal", "objetivo"), ("steps", "pasos"),
         ("materials", "materiales"), ("budget", "presupuesto"),
         ("deadline", "plazo"), ("update", "actualización"), ("choice", "elección")],
        [("Our project goal is a reading afternoon for ten children.",
          "El objetivo del proyecto es una tarde de lectura para diez niños.",
          "Project y goal expresan un resultado concreto y comprobable."),
         ("Yesterday we booked the room; now we are checking the steps.",
          "Ayer reservamos la sala; ahora revisamos los pasos.",
          "Los marcadores temporales convierten acciones en una update clara."),
         ("The materials cost less than the old budget, and we have enough.",
          "Los materiales cuestan menos que el presupuesto anterior y tenemos suficientes.",
          "Less than compara costo y enough comprueba la cantidad."),
         ("We have to finish before the deadline. Could you confirm the list?",
          "Tenemos que terminar antes del plazo. ¿Podrías confirmar la lista?",
          "Have to fija obligación y Could you coordina una acción con otra persona."),
         ("Choose the cheaper option, record the choice and send the update before the deadline.",
          "Elige la opción más barata, registra la elección y envía la actualización antes del plazo.",
          "El modelo conecta comparación, choice, update y deadline en pasos simples."),
         ("Project check: place and time, quantity and price, person and deadline.",
          "Control del proyecto: lugar y hora, cantidad y precio, persona y plazo.",
          "Seis datos agrupados permiten redactar o reconocer un resumen completo sin adivinar.")], pools, remap,
        uses=[CONCEPTS[96], CONCEPTS[97], CONCEPTS[98], c])


def build_100() -> dict[str, Any]:
    n, c, p = 100, CONCEPTS[100], "en.n2.c100"
    all_c = [CONCEPTS[x] for x in range(96, 101)]
    pools = {
        "practiceGuided": [
            q(f"{p}.pg01", "Ayer reservaron, ahora preparan y mañana se reúnen. Elige el informe.",
              ["We will book yesterday, prepared now and meet tomorrow.",
               "We booked yesterday, are preparing now and will meet tomorrow.",
               "We booked tomorrow, prepare yesterday and met now."], 1, c, "practiceGuided",
              "Booked, are preparing y will meet corresponden a los tres momentos dados.",
              hint="Comprueba el verbo que acompaña a cada momento."),
            f(f"{p}.pg02", "Usa enough: Nine chairs are ___ for seven people.", "enough", c,
              "practiceGuided", "Enough confirma que nueve sillas cubren a siete personas.",
              hint="La cantidad disponible supera la cantidad necesaria."),
            o(f"{p}.pg03", "Ordena la petición y la respuesta de confirmación.",
              "Could you confirm the time? Yes, I can.", c, "practiceGuided",
              "La interacción incluye una petición con could y una respuesta directa.",
              hint="Coloca la pregunta antes de la confirmación."),
        ],
        "practice": [
            w(f"{p}.p01", "Escribe una actualización con paso anterior y siguiente.",
              "Ayer: elegimos sala. Ahora: revisamos lista. Mañana: enviaremos plan.",
              "Yesterday, we chose the room. Now we are checking the list. Tomorrow, we will send the plan.",
              "We chose the room yesterday, are checking the list now and will send the plan tomorrow.",
              c, "practice", "Ambas variantes conservan los tres pasos y sus momentos."),
            l(f"{p}.p02", "Escucha y selecciona la comparación y cantidad correctas.",
              "Room B is cheaper than Room A, and twelve seats are enough for ten people.",
              ["Room A is cheaper; ten seats", "Room B is cheaper; twelve seats are enough",
               "Both rooms cost the same; twelve seats"], 1, c, "practice",
              "El audio identifica la sala B y confirma suficiencia para diez personas."),
            m(f"{p}.p03", "Une cada frase del desempeño con su función.",
              [("We have to arrive early.", "requisito"),
               ("Could you bring the list?", "petición"),
               ("Yes, I can.", "respuesta")], c, "practice",
              "Las tres frases distribuyen obligación, coordinación y respuesta."),
        ],
        "evaluation": [
            q(f"{p}.e01", "Ravi terminó carteles anoche y los coloca ahora. Elige el informe.",
              ["Ravi made the posters last night and is putting them up now.",
               "Ravi makes the posters now and put them up last night.",
               "Ravi will make the posters last night and puts them up tomorrow."], 0, c,
              "evaluation", "Made sitúa el trabajo anoche e is putting describe la acción actual.",
              requires=[CONCEPTS[96], c]),
            q(f"{p}.e02", "Se necesitan 12 plazas. Este: $30/14; Oeste: $24/10. Elige.",
              ["The West room is cheaper and has enough seats.",
               "The East room costs more, but it has enough seats.",
               "Both rooms cost the same and have enough seats."], 1, c, "evaluation",
              "La sala Este cuesta más, pero sus catorce plazas cubren la necesidad de doce.",
              requires=[CONCEPTS[97], c]),
            l(f"{p}.e03", "Escucha y elige la interacción con petición y aceptación.",
              "Could you bring the forms at ten? Yes, of course. I can bring them.",
              ["A prohibition followed by refusal", "Advice without a response",
               "A polite request followed by acceptance"], 2, c, "evaluation",
              "Could you formula la petición y Yes, of course expresa aceptación.",
              requires=[CONCEPTS[98], c]),
            w(f"{p}.e04", "Redacta el desempeño final con todos los datos indicados.",
              "Ficha: cocina para 8. Ayer reservaron. Ahora compran; sábado 10:00. 10 platos. Sala pequeña $35, salón $50. Lavarse manos. Maya confirma.",
              "COOKING CLASS UPDATE. Done: We booked the community kitchen yesterday. Now: We are buying supplies for eight people for Saturday at ten. Numbers: Ten plates are enough; the small room at thirty-five dollars is cheaper than the hall at fifty. Rule: We have to wash our hands. Maya: Could you confirm the time? Yes, Saturday at ten.",
              "COOKING CLASS FORM. Past: We reserved the community kitchen yesterday. Present and plan: We are buying supplies now for eight people and will meet Saturday at ten. Quantity and price: Ten plates are enough. The small room costs thirty-five dollars, less than the fifty-dollar hall. Rule: We must wash our hands. Request: Maya, could you confirm the time? Reply: Yes, Saturday at ten.",
              c, "evaluation",
              "El desempeño conserva proyecto, tres tiempos, cantidad, comparación, regla y diálogo.",
              requires=all_c),
        ],
        "review": [
            m(f"{p}.r01", "Une cada situación nueva con la conclusión que permite recuperar.",
              [("The flyers went out last night; the team is packing now.",
                "pasado terminado y acción actual"),
               ("Hall C: $28 and 12 seats; Hall D: $35 and 10; we need 11.",
                "C es más barata y suficiente"),
               ("Could you bring the keys? Certainly; I can bring them.",
                "petición aceptada")], c, "review",
              "Cada situación contiene datos suficientes para recuperar tiempo, comparación o interacción."),
            o(f"{p}.r02", "Ordena el cierre que confirma resultado y paso siguiente.",
              "The plan is confirmed, and tomorrow we will send the update.", c, "review",
              "La oración confirma el resultado y sitúa la actualización futura."),
            w(f"{p}.r03", "Redacta la recuperación final con todos los datos.",
              "Mensaje: pícnic para 6, domingo 12:00. Invitaciones ayer; preparar ahora. 8 bocadillos. Parque a 1 km, playa a 5 km. Agua obligatoria. Sam confirma.",
              "Neighbours: our picnic for six is Sunday at noon. We sent invitations yesterday and are packing now. Eight sandwiches are enough. The park is one kilometre away; the beach is five, so the park is closer. Everyone has to bring water. Sam, could you confirm noon? Yes.",
              "PICNIC MESSAGE: Six neighbours will meet Sunday at noon. Yesterday we sent invitations; now we are preparing. We have eight sandwiches, so there are enough. The park is one kilometre away and nearer than the beach at five. Everyone must bring water. Could you confirm noon, Sam? Yes, I can.",
              c, "review", "La recuperación demuestra los cinco conceptos en un pícnic nuevo.",
              requires=all_c),
        ],
    }
    remap = {f"{p}.e01": (f"en.n2.class-{n}.t01", f"{p}.r01"),
             f"{p}.e02": (f"en.n2.class-{n}.t02", f"{p}.r01"),
             f"{p}.e03": (f"en.n2.class-{n}.t03", f"{p}.r01"),
             f"{p}.e04": (f"en.n2.class-{n}.t06", f"{p}.r03")}
    return make_class(n,
        ["Demostrar recursos A2 en una actuación breve y autocontenida.",
         "Integrar proyecto, tiempos, cantidad, comparación, modales e interacción.",
         "Confirmar un resultado y el siguiente paso sin complejidad B1."],
        [("plan", "planificación"), ("update", "actualización"), ("compare", "comparar"),
         ("request", "petición"), ("respond", "responder"),
         ("confirm", "confirmar"), ("result", "resultado"), ("step", "paso")],
        [("Yesterday we finished the plan; now we are preparing the update.",
          "Ayer terminamos el plan; ahora preparamos la actualización.",
          "Los marcadores separan un resultado pasado de una acción actual."),
         ("Compare the prices and choose an option with enough seats.",
          "Compara los precios y elige una opción con suficientes asientos.",
          "Compare y enough conectan una diferencia con una necesidad real."),
         ("Use a polite request: Could you bring the materials, please?",
          "Usa una petición cortés: ¿Podrías traer los materiales, por favor?",
          "Request con could coordina una acción sin imponerla."),
         ("Respond clearly and confirm the time and place.",
          "Responde con claridad y confirma la hora y el lugar.",
          "Respond y confirm cierran la interacción con datos verificables."),
         ("State the result and the next step in short sentences.",
          "Indica el resultado y el siguiente paso en oraciones cortas.",
          "Result resume lo logrado y next step mantiene el proyecto en marcha."),
         ("Ava: We booked Room A yesterday. Now our plan is for Friday at four with six students. Eight chairs are enough, and A is quieter than B. We have to arrive early. Leo, could you bring the worksheets? Leo: Yes, I can.",
          "Ava: Ayer reservamos la sala A. Ahora nuestro plan es para el viernes a las cuatro con seis estudiantes. Ocho sillas alcanzan y A es más silenciosa que B. Tenemos que llegar antes. Leo, ¿podrías traer las hojas? Leo: Sí.",
          "El diálogo modela tiempo, cantidad, comparación, requisito, petición y respuesta por turnos.")],
        pools, remap, uses=all_c, cumulative=all_c)


BUILDERS = {96: build_96, 97: build_97, 98: build_98, 99: build_99, 100: build_100}


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.casefold()).strip()


def audit(classes: list[dict[str, Any]], full: bool) -> dict[str, Any]:
    banned_prompt = re.compile(
        r"\b(?:esta frase|esta oración|lo anterior|el modelo|frase indicada|idea trabajada)\b", re.I)
    signatures: dict[str, str] = {}
    prompts: set[str] = set()
    indices: Counter[int] = Counter()
    totals: Counter[str] = Counter()
    formats: Counter[str] = Counter()
    for cls in classes:
        number = int(cls["id"].rsplit("-", 1)[1])
        concept = CONCEPTS[number]
        assert cls["phase"] == PHASES[number]
        assert cls["status"] == "shadow" and cls["runtimeAi"] is False
        assert cls["qualityPolicy"] == QUALITY_POLICY
        assert cls["prerequisites"] == [f"en.n2.class-{number - 1}"]
        assert 4 <= len(cls["teaching"]) <= 6 and 6 <= len(cls["vocabulary"]) <= 12
        assert {key: len(value) for key, value in cls["pools"].items()} == {
            "practiceGuided": 3, "practice": 3, "evaluation": 4, "review": 3}
        items = [(pool, item) for pool, values in cls["pools"].items() for item in values]
        assert len(items) == 13 and len({item["format"] for _, item in items}) >= 4
        assert any(item["format"] == "escribir" for _, item in items)
        assert any(item["format"] == "escuchar" for _, item in items)
        feedbacks: list[str] = []
        local_indices: Counter[int] = Counter()
        for pool, item in items:
            totals[pool] += 1
            formats[item["format"]] += 1
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
        expected = [CONCEPTS[number] for number in range(96, 101)]
        assert close["cumulativeEvaluation"] == expected and close["usesPatterns"] == expected
        final_write = next(item for item in close["pools"]["evaluation"]
                           if item["id"] == "en.n2.c100.e04")
        assert final_write["requires"] == expected
        answer = final_write["answer"]["text"].casefold()
        for marker in ("cooking class update", "yesterday", "now", "saturday at ten", "eight people",
                       "ten plates are enough", "cheaper", "have to",
                       "could you confirm", "yes, saturday at ten"):
            assert marker in answer, marker
        teaching_final = close["teaching"][-1]["en"].casefold()
        review_final = next(item for item in close["pools"]["review"]
                            if item["id"] == "en.n2.c100.r03")["answer"]["text"].casefold()
        assert "room a" in teaching_final and "ava:" in teaching_final
        assert "cooking class" in answer
        assert "picnic" in review_final
    return {"classes": len(classes), "items": sum(totals.values()), "pools": dict(totals),
            "formats": dict(sorted(formats.items())),
            "correctIndices": dict(sorted(indices.items())), "fingerprints": len(signatures),
            "prompts": len(prompts)}


def write_class(number: int) -> Path:
    document = BUILDERS[number]()
    audit([document], False)
    path = OUT / f"class-{number}.json"
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_bundle() -> Path:
    classes = [json.loads((OUT / f"class-{number}.json").read_text(encoding="utf-8"))
               for number in range(96, 101)]
    audit(classes, True)
    bundle = {"schema": "onelingo.editorial.class-bundle.v1", "course": "en", "level": 2,
              "scale": SCALE, "status": "shadow", "runtimeAi": False,
              "selectionPolicy": {"deterministic": True},
              "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
              "range": {"start": 96, "end": 100}, "classes": classes}
    path = OUT / "bundle-96-100.json"
    path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-number", type=int, choices=range(96, 101))
    parser.add_argument("--bundle", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    if args.class_number is not None:
        print(write_class(args.class_number))
    elif args.bundle:
        print(write_bundle())
    elif args.audit:
        classes = [json.loads((OUT / f"class-{number}.json").read_text(encoding="utf-8"))
                   for number in range(96, 101)]
        print(json.dumps(audit(classes, True), ensure_ascii=False, sort_keys=True))
    else:
        parser.error("choose --class-number, --bundle, or --audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
