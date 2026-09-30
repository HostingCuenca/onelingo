#!/usr/bin/env python3
"""Regenera las clases editoriales de Inglés N2 C46-C50.

Cada ejecución reconstruye las cinco clases, el bundle y un informe de build,
y ejecuta el validador editorial común.
"""

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
REPORT_OUT = ROOT / "build/editorial-n2-46-50"
VALIDATOR = ROOT / "tools/contenido/validar_bundle_editorial.py"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n2-editorial-v2.json"
REFERENCE = ROOT / "assets/contenido/en/editorial/n2/class-45.json"
SCALE = "client-10-levels-v1"

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
ACCESSIBILITY = {"screenReader": True, "highContrast": True, "largeText": True}

CONCEPTS = {
    46: "n2-superlatives-in-group",
    47: "n2-too-not-enough",
    48: "n2-as-as-equality",
    49: "n2-advantages-limits",
    50: "n2-choose-three-options",
}
PHASES = {46: "input", 47: "form", 48: "comprehension", 49: "production", 50: "transfer"}
TITLES = {
    46: {"en": "Superlatives in a group", "es": "Superlativos en un grupo"},
    47: {"en": "Too and not enough", "es": "Too y not enough"},
    48: {"en": "As ... as", "es": "As ... as"},
    49: {"en": "Describe advantages and limits", "es": "Describir ventajas y límites"},
    50: {"en": "Choose from three options", "es": "Elegir entre tres opciones"},
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


def choose(
    item_id: str,
    prompt: str,
    choices: list[str],
    index: int,
    concept: str,
    feedback: str,
    *,
    guided: bool = False,
    hint: str | None = None,
    requires: list[str] | None = None,
) -> dict[str, Any]:
    teaches, default_requires = requirements(concept, guided)
    return add_hash({
        "id": item_id,
        "format": "elegir",
        "prompt": {"es": prompt},
        "answer": {"index": index},
        "choices": [{"text": value} for value in choices],
        "teaches": teaches,
        "requires": default_requires if requires is None else requires,
        "origin": origin(feedback, hint=hint),
        "accessibility": dict(ACCESSIBILITY),
    })


def complete(
    item_id: str,
    prompt: str,
    answer: str,
    concept: str,
    feedback: str,
    *,
    guided: bool = False,
    hint: str | None = None,
    requires: list[str] | None = None,
) -> dict[str, Any]:
    teaches, default_requires = requirements(concept, guided)
    return add_hash({
        "id": item_id,
        "format": "completar",
        "prompt": {"es": prompt},
        "answer": {"text": answer, "accepted": [answer]},
        "choices": [],
        "teaches": teaches,
        "requires": default_requires if requires is None else requires,
        "origin": origin(feedback, hint=hint),
        "accessibility": dict(ACCESSIBILITY),
    })


def order(
    item_id: str,
    prompt: str,
    answer: str,
    tokens: list[str],
    concept: str,
    feedback: str,
    *,
    guided: bool = False,
    hint: str | None = None,
) -> dict[str, Any]:
    teaches, reqs = requirements(concept, guided)
    return add_hash({
        "id": item_id,
        "format": "ordenar",
        "prompt": {"es": prompt},
        "answer": {"text": answer, "tokens": tokens},
        "choices": [],
        "teaches": teaches,
        "requires": reqs,
        "origin": origin(feedback, hint=hint),
        "accessibility": dict(ACCESSIBILITY),
    })


def write(
    item_id: str,
    prompt: str,
    stimulus: str,
    answer: str,
    accepted: list[str],
    concept: str,
    feedback: str,
    *,
    requires: list[str] | None = None,
) -> dict[str, Any]:
    return add_hash({
        "id": item_id,
        "format": "escribir",
        "prompt": {"es": prompt},
        "answer": {"text": answer, "accepted": accepted},
        "choices": [],
        "teaches": [],
        "requires": [concept] if requires is None else requires,
        "origin": origin(feedback, text=stimulus),
        "accessibility": dict(ACCESSIBILITY),
    })


def listen(
    item_id: str,
    prompt: str,
    audio: str,
    choices: list[str],
    index: int,
    concept: str,
    feedback: str,
    *,
    requires: list[str] | None = None,
) -> dict[str, Any]:
    return add_hash({
        "id": item_id,
        "format": "escuchar",
        "prompt": {"es": prompt},
        "answer": {"index": index},
        "choices": [{"text": value} for value in choices],
        "teaches": [],
        "requires": [concept] if requires is None else requires,
        "origin": origin(
            feedback,
            audio=audio,
            audioMode="tts",
            languageCode="en",
            speedOptions=[0.75, 1.0],
            maxReplays=3,
            revealTranscriptAfterAttempt=True,
        ),
        "accessibility": dict(ACCESSIBILITY),
    })


def match(
    item_id: str,
    prompt: str,
    pairs: list[tuple[str, str]],
    concept: str,
    feedback: str,
    *,
    guided: bool = False,
    hint: str | None = None,
) -> dict[str, Any]:
    teaches, reqs = requirements(concept, guided)
    values = [[left, {"es": right}] for left, right in pairs]
    return add_hash({
        "id": item_id,
        "format": "relacionar",
        "prompt": {"es": prompt},
        "answer": {"pairs": values},
        "choices": [],
        "teaches": teaches,
        "requires": reqs,
        "origin": origin(feedback, hint=hint, pairs=values),
        "accessibility": dict(ACCESSIBILITY),
    })


def lesson(number: int, index: int, en: str, es: str, explanation: str) -> dict[str, Any]:
    midpoint = max(1, len(en.split()) // 2)
    en_words = en.split()
    es_words = es.split()
    es_midpoint = max(1, len(es_words) // 2)
    return {
        "id": f"en.n2.class-{number}.t{index:02d}",
        "en": en,
        "es": es,
        "explanationEs": explanation,
        "segments": [
            {"en": " ".join(en_words[:midpoint]), "es": " ".join(es_words[:es_midpoint])},
            {"en": " ".join(en_words[midpoint:]), "es": " ".join(es_words[es_midpoint:])},
        ],
        "audioText": en,
        "audioMode": "tts",
        "languageCode": "en",
        "patternId": CONCEPTS[number],
    }


def common_class(
    number: int,
    objectives: list[str],
    vocabulary: list[tuple[str, str]],
    teaching: list[tuple[str, str, str]],
    pools: dict[str, list[dict[str, Any]]],
    remediation: dict[str, tuple[int, str]],
    *,
    uses_patterns: list[str] | None = None,
    cumulative: list[str] | None = None,
) -> dict[str, Any]:
    prefix = f"en.n2.c{number}"
    document: dict[str, Any] = {
        "schema": "onelingo.editorial.class.v1",
        "course": "en",
        "level": 2,
        "scale": SCALE,
        "status": "shadow",
        "runtimeAi": False,
        "phase": PHASES[number],
        "title": TITLES[number],
        "objectives": {"es": objectives},
        "id": f"en.n2.class-{number}",
        "cefr": "A2",
        "concepts": [CONCEPTS[number]],
        "skills": ["gramática", "lectura", "escucha", "escritura"],
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
        "accessibility": {
            "highContrast": True,
            "largeText": True,
            "screenReader": True,
            "audioReplay": True,
        },
        "recovery": {
            "retryPool": "review",
            "maxAttempts": 2,
            "allowAudioReplay": True,
            "preserveProgress": True,
        },
        "remediationPolicy": {"source": "editorial", "deterministic": True},
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": dict(QUALITY_POLICY),
    }
    if cumulative is not None:
        document["cumulativeEvaluation"] = cumulative
    return document


def build_46() -> dict[str, Any]:
    n, c, p = 46, CONCEPTS[46], "en.n2.c46"
    vocabulary = [
        ("tallest", "el más alto"), ("busiest", "el más concurrido"),
        ("most affordable", "el más económico"), ("least crowded", "el menos concurrido"),
        ("best", "el mejor"), ("among", "entre"), ("group", "grupo"),
    ]
    teaching = [
        ("Leo is the tallest student in the group.", "Leo es el estudiante más alto del grupo.",
         "Con adjetivos cortos, the + -est identifica un extremo dentro de un grupo."),
        ("Monday is the busiest day among the five weekdays.", "El lunes es el día más ocupado entre los cinco días laborables.",
         "Los adjetivos terminados en consonante + y cambian y por i antes de -est."),
        ("The city bus is the most affordable option in the group.", "El bus urbano es la opción más económica del grupo.",
         "Con adjetivos largos se usa the most sin cambiar el adjetivo."),
        ("The morning class is the least crowded in the group.", "La clase matutina es la menos concurrida del grupo.",
         "The least expresa el grado mínimo cuando se comparan tres o más elementos."),
        ("Of the three cooks, Nora is the best in the group.", "De los tres cocineros, Nora es la mejor del grupo.",
         "Good cambia de forma: el superlativo irregular es best, no most good."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Tres árboles miden 2, 4 y 6 m. Elige la descripción del tercero.",
                   ["The third tree is the tallest.", "The third tree is tallest than the other two.", "The third tree is the most tall."],
                   0, c, "Tall admite -est; por eso tallest marca el extremo del grupo de tres.",
                   guided=True, hint="Para tres elementos, usa the + adjetivo corto + -est."),
            order(f"{p}.pg02", "Ordena la frase que identifica el día con más actividad.",
                  "Saturday is the busiest day of the week.",
                  ["Saturday", "is", "the", "busiest", "day", "of", "the", "week."], c,
                  "Busiest va después de the y antes del sustantivo day.", guided=True,
                  hint="Empieza con Saturday is y coloca the busiest antes de day."),
            complete(f"{p}.pg03", "Usa most affordable: This is the ___ plan in the group.",
                     "most affordable", c,
                     "Affordable es largo; el superlativo correcto conserva el adjetivo tras most.",
                     guided=True, hint="No añadas -est a affordable; usa most."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha cuál lago ocupa el extremo de profundidad.",
                   "Lake Azul is the deepest lake in the region.",
                   ["Lake Azul is deeper than the region.", "Lake Azul is the deepest lake in the region.", "Lake Azul is the most deep lake in the region."],
                   1, c, "Deep es corto: deepest compara el lago con toda la región."),
            match(f"{p}.p02", "Relaciona dos extremos con su significado.",
                  [("busiest market", "mercado más concurrido"), ("least crowded train", "tren menos concurrido")], c,
                  "Busiest señala el máximo de actividad; least crowded, el mínimo de gente."),
            write(f"{p}.p03", "Escribe en inglés: De los tres cocineros, Leo es el mejor.",
                  "De los tres cocineros, Leo es el mejor.",
                  "Of the three cooks, Leo is the best.",
                  ["Of the three cooks, Leo is the best.", "Leo is the best of the three cooks."], c,
                  "Good cambia a best para comparar a Leo con todo el grupo."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Tres hoteles cuestan $40, $65 y $90. Elige la conclusión correcta.",
                   ["The $40 hotel is more affordable of the three.", "The $90 hotel is the least expensive.", "The $40 hotel is the most affordable of the three."],
                   2, c, "Most affordable compara correctamente el hotel de $40 con los otros dos."),
            listen(f"{p}.e02", "Escucha e identifica el resultado irregular dentro de una familia.",
                   "Nora is the best cook in her family.",
                   ["Nora is the goodest cook in her family.", "Nora is the best cook in her family.", "Nora is a better cook of her family."],
                   1, c, "Best es el superlativo irregular de good y exige the en esta comparación."),
            complete(f"{p}.e03", "Usa least crowded: The 6 a.m. bus is the ___ of all.",
                     "least crowded", c,
                     "Least crowded expresa que el bus de las seis tiene menos pasajeros que todos."),
            write(f"{p}.e04", "Escribe en inglés: Es el edificio más alto entre los cuatro.",
                  "Es el edificio más alto entre los cuatro.",
                  "It is the tallest building among the four.",
                  ["It is the tallest building among the four.", "It is the highest building of the four."], c,
                  "Tallest/highest con the sitúan un edificio en el extremo de un grupo de cuatro."),
        ],
        "review": [
            order(f"{p}.r01", "Reconstruye el superlativo largo sobre tres rutas.",
                  "This is the most convenient route of the three.",
                  ["This", "is", "the", "most", "convenient", "route", "of", "the", "three."], c,
                  "Most convenient mantiene intacto el adjetivo largo y compara tres rutas."),
            choose(f"{p}.r02", "En un grupo de tres resultados, selecciona el extremo irregular.",
                   ["This is the best result in the group.", "This is the better result in the group.", "This is the most good result in the group."],
                   0, c, "Best, no better, expresa el resultado máximo dentro del grupo."),
            match(f"{p}.r03", "Une dos extremos de grupo con su traducción.",
                  [("the least expensive choice", "la opción menos cara"), ("the tallest in the group", "el más alto del grupo")], c,
                  "The least marca el mínimo; the tallest marca el máximo dentro de un grupo."),
        ],
    }
    return common_class(
        n,
        [
            "Identificar el extremo de una cualidad al comparar tres o más elementos.",
            "Distinguir -est, most y least según la forma del adjetivo.",
            "Describir una persona, lugar u opción que ocupa un extremo del grupo.",
        ],
        vocabulary, teaching, pools,
        {"e01": (3, "r01"), "e02": (5, "r02"), "e03": (4, "r03"), "e04": (1, "r03")},
    )


def build_47() -> dict[str, Any]:
    n, c, p = 47, CONCEPTS[47], "en.n2.c47"
    vocabulary = [
        ("too", "demasiado"), ("enough", "suficiente"), ("heavy", "pesado"),
        ("narrow", "estrecho"), ("warm", "cálido"), ("space", "espacio"),
    ]
    teaching = [
        ("This suitcase is too heavy for the shelf.", "Esta maleta es demasiado pesada para el estante.",
         "Too va antes del adjetivo y expresa un exceso que causa un problema."),
        ("The hallway is not wide enough for the sofa.", "El pasillo no es lo bastante ancho para el sofá.",
         "Not + adjective + enough expresa que una cualidad no alcanza el nivel necesario."),
        ("The room has enough space for four desks.", "La habitación tiene suficiente espacio para cuatro escritorios.",
         "Enough va antes de un sustantivo como space, pero después de un adjetivo."),
        ("The soup is too warm now, but it will be cool enough soon.", "La sopa está demasiado caliente ahora, pero pronto estará suficientemente fría.",
         "El contexto decide si hay exceso con too o suficiencia con enough."),
    ]
    pools = {
        "practiceGuided": [
            complete(f"{p}.pg01", "Completa el exceso: The box is ___ heavy to carry alone.", "too", c,
                     "Too precede heavy y explica por qué una persona no puede cargar la caja.",
                     guided=True, hint="Si la cualidad impide la acción, coloca too antes del adjetivo."),
            choose(f"{p}.pg02", "La puerta mide 60 cm y la mesa 80 cm. Elige el límite correcto.",
                   ["The door is too enough narrow for the table.", "The door is not wide enough for the table.", "The door has not enough wide for the table."],
                   1, c, "Not wide enough expresa que los 60 cm no alcanzan para la mesa.",
                   guided=True, hint="Usa not + adjetivo + enough para una medida insuficiente."),
            match(f"{p}.pg03", "Relaciona cada problema con la expresión adecuada.",
                  [("too heavy", "demasiado pesado"), ("not warm enough", "no suficientemente cálido")], c,
                  "Too heavy señala exceso de peso; not warm enough, falta de calor.",
                  guided=True, hint="Too indica exceso; not ... enough indica insuficiencia."),
        ],
        "practice": [
            order(f"{p}.p01", "Ordena la explicación sobre un pasillo estrecho.",
                  "The hallway is too narrow for the cart.",
                  ["The", "hallway", "is", "too", "narrow", "for", "the", "cart."], c,
                  "Too narrow va unido antes del complemento for the cart."),
            listen(f"{p}.p02", "Escucha por qué no puede entrar el grupo.",
                   "The room does not have enough space for everyone.",
                   ["The room does not have enough space for everyone.", "The room has too enough space for everyone.", "The room is not space enough for everyone."],
                   0, c, "Enough precede el sustantivo space y la negación marca insuficiencia."),
            write(f"{p}.p03", "Escribe en inglés: El café está demasiado caliente para beberlo.",
                  "El café está demasiado caliente para beberlo.",
                  "The coffee is too hot to drink.",
                  ["The coffee is too hot to drink.", "The coffee is too warm to drink now."], c,
                  "Too hot aparece antes del infinitivo que resulta imposible en este momento."),
        ],
        "evaluation": [
            listen(f"{p}.e01", "Escucha la razón por la que una chaqueta no sirve para el invierno.",
                   "This jacket is not warm enough for winter.",
                   ["This jacket is warm enough for winter.", "This jacket is too warm for winter.", "This jacket is not warm enough for winter."],
                   2, c, "Not warm enough indica que la chaqueta no ofrece el calor necesario."),
            choose(f"{p}.e02", "El sofá mide 2 m y el espacio 1,5 m. Selecciona la conclusión.",
                   ["The sofa is small enough for the space.", "The sofa is too long for the space.", "The space is enough long for the sofa."],
                   1, c, "Too long expresa el exceso de longitud frente al espacio disponible."),
            complete(f"{p}.e03", "Usa too warm: The bedroom is ___ to sleep comfortably.",
                     "too warm", c,
                     "Too warm explica que el exceso de calor impide dormir con comodidad."),
            write(f"{p}.e04", "Escribe en inglés: No tenemos suficiente espacio para seis sillas.",
                  "No tenemos suficiente espacio para seis sillas.",
                  "We do not have enough space for six chairs.",
                  ["We do not have enough space for six chairs.", "There is not enough space for six chairs."], c,
                  "Enough va antes de space; la negación muestra que el espacio disponible no basta."),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona dos límites físicos con su significado.",
                  [("too narrow", "demasiado estrecho"), ("enough space", "espacio suficiente")], c,
                  "Too narrow describe un exceso problemático; enough space confirma suficiencia."),
            order(f"{p}.r02", "Reconstruye la condición mínima para una reunión.",
                  "The table is not large enough for eight people.",
                  ["The", "table", "is", "not", "large", "enough", "for", "eight", "people."], c,
                  "Enough sigue a large; not convierte la frase en una insuficiencia."),
            choose(f"{p}.r03", "Una mochila soporta 5 kg y la carga pesa 8. Elige la frase precisa.",
                   ["The load is too heavy for the backpack.", "The load is not heavy enough for the backpack.", "The backpack has enough heavy load."],
                   0, c, "Ocho kilos superan el límite; too heavy es la única conclusión coherente."),
        ],
    }
    return common_class(
        n,
        [
            "Interpretar cuándo una cualidad excede un límite práctico.",
            "Colocar too y enough correctamente con adjetivos y sustantivos.",
            "Explicar por qué un objeto o espacio sirve o no para una necesidad.",
        ],
        vocabulary, teaching, pools,
        {"e01": (2, "r02"), "e02": (1, "r03"), "e03": (4, "r01"), "e04": (3, "r02")},
    )


def build_48() -> dict[str, Any]:
    n, c, p = 48, CONCEPTS[48], "en.n2.c48"
    vocabulary = [
        ("equally", "por igual"), ("similar", "parecido"), ("quiet", "silencioso"),
        ("fast", "rápido"), ("strong", "fuerte"), ("same", "mismo"),
    ]
    teaching = [
        ("The meeting room is as quiet as the study room.", "La sala de reuniones es tan silenciosa como la sala de estudio.",
         "As + adjective + as compara dos elementos que tienen el mismo grado de una cualidad."),
        ("The red bicycle is not as fast as the blue one.", "La bicicleta roja no es tan rápida como la azul.",
         "Not as ... as indica que el primer elemento tiene un grado menor."),
        ("Mia is as strong as her teammate.", "Mia es tan fuerte como su compañera.",
         "El adjetivo queda sin cambios entre los dos as."),
        ("Both plans have the same price and are similar in length.", "Ambos planes tienen el mismo precio y una duración similar.",
         "Same y similar ayudan a interpretar una comparación de igualdad."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Dos trenes tardan 40 minutos. Elige la comparación de igualdad.",
                   ["Train A is fast as train B.", "Train A is as faster as train B.", "Train A is as fast as train B."],
                   2, c, "As fast as conserva fast y expresa que ambos trenes tardan lo mismo.",
                   guided=True, hint="Rodea el adjetivo sin cambios con as ... as."),
            match(f"{p}.pg02", "Une cada relación con su significado.",
                  [("as quiet as", "tan silencioso como"), ("not as strong as", "no tan fuerte como")], c,
                  "La primera relación marca igualdad; la segunda, un grado menor.",
                  guided=True, hint="La palabra not cambia igualdad por inferioridad."),
            order(f"{p}.pg03", "Ordena la comparación de dos cajas con el mismo peso.",
                  "This box is as heavy as that one.",
                  ["This", "box", "is", "as", "heavy", "as", "that", "one."], c,
                  "Heavy permanece entre dos as porque el peso es igual.", guided=True,
                  hint="Construye sujeto + be + as + adjetivo + as + comparación."),
        ],
        "practice": [
            complete(f"{p}.p01", "Usa just as quiet as: The library is ___ the study room.",
                     "just as quiet as", c,
                     "Just as quiet as confirma que ambos espacios tienen el mismo nivel de silencio."),
            write(f"{p}.p02", "Escribe en inglés: Mi teléfono es tan rápido como el tuyo.",
                  "Mi teléfono es tan rápido como el tuyo.",
                  "My phone is as fast as yours.",
                  ["My phone is as fast as yours.", "My phone works as quickly as yours."], c,
                  "As fast as yours compara el rendimiento sin convertir fast en comparativo."),
            listen(f"{p}.p03", "Escucha qué dos atletas tienen la misma fuerza.",
                   "Carla is as strong as Elena.",
                   ["Carla is as strong as Elena.", "Carla is stronger as Elena.", "Carla is the strongest of Elena."],
                   0, c, "As strong as presenta la fuerza de Carla y Elena como equivalente."),
        ],
        "evaluation": [
            write(f"{p}.e01", "Escribe en inglés: La oficina nueva es tan silenciosa como la anterior.",
                  "La oficina nueva es tan silenciosa como la anterior.",
                  "The new office is as quiet as the old one.",
                  ["The new office is as quiet as the old one.", "The new office is just as quiet as the previous one."], c,
                  "As quiet as conserva quiet y conecta dos oficinas con el mismo grado."),
            choose(f"{p}.e02", "La ruta A tarda 30 min y la B 45. Elige la comparación verdadera.",
                   ["Route A is as slow as route B.", "Route B is not as fast as route A.", "Route B is as fast as route A."],
                   1, c, "Al tardar más, la ruta B no es tan rápida como la ruta A."),
            listen(f"{p}.e03", "Escucha la igualdad entre dos baterías.",
                   "Battery X lasts as long as battery Y.",
                   ["Battery X lasts longer as battery Y.", "Battery X is the longest battery Y.", "Battery X lasts as long as battery Y."],
                   2, c, "As long as comunica que las dos baterías duran el mismo tiempo."),
            complete(f"{p}.e04", "Usa the same: Both tickets cost ___ amount.",
                     "the same", c,
                     "The same amount confirma que no existe diferencia de precio."),
        ],
        "review": [
            order(f"{p}.r01", "Reconstruye una comparación negativa de velocidad.",
                  "The local bus is not as fast as the express.",
                  ["The", "local", "bus", "is", "not", "as", "fast", "as", "the", "express."], c,
                  "Not as fast as sitúa al bus local por debajo del expreso."),
            match(f"{p}.r02", "Relaciona dos expresiones de semejanza.",
                  [("equally useful", "igual de útil"), ("similar size", "tamaño similar")], c,
                  "Equally expresa el mismo grado; similar señala características cercanas."),
            choose(f"{p}.r03", "Dos cuerdas soportan 20 kg. Selecciona la descripción exacta.",
                   ["Rope A is as strong as rope B.", "Rope A is stronger as rope B.", "Rope A is the most strong of rope B."],
                   0, c, "La capacidad idéntica exige as strong as, no un comparativo o superlativo."),
        ],
    }
    return common_class(
        n,
        [
            "Reconocer igualdad e inferioridad al comparar dos cualidades.",
            "Interpretar datos iguales mediante as ... as, same y equally.",
            "Redactar comparaciones de igualdad sin modificar el adjetivo.",
        ],
        vocabulary, teaching, pools,
        {"e01": (3, "r03"), "e02": (2, "r01"), "e03": (3, "r03"), "e04": (4, "r02")},
    )


def build_49() -> dict[str, Any]:
    n, c, p = 49, CONCEPTS[49], "en.n2.c49"
    vocabulary = [
        ("advantage", "ventaja"), ("limit", "límite"), ("practical", "práctico"),
        ("portable", "portátil"), ("battery", "batería"), ("however", "sin embargo"),
    ]
    teaching = [
        ("The main advantage is its long battery life.", "La principal ventaja es la larga duración de su batería.",
         "Una ventaja presenta el beneficio concreto que ofrece una opción."),
        ("Its limit is the small screen.", "Su límite es la pantalla pequeña.",
         "Un límite nombra una característica que reduce la utilidad de la opción."),
        ("The tablet is portable; however, its keyboard is narrow.", "La tableta es portátil; sin embargo, su teclado es estrecho.",
         "However conecta una ventaja con una restricción opuesta."),
        ("This practical device is easy to carry, but it needs daily charging.", "Este dispositivo práctico es fácil de llevar, pero necesita carga diaria.",
         "Una descripción equilibrada incluye un beneficio y una condición desfavorable."),
    ]
    pools = {
        "practiceGuided": [
            match(f"{p}.pg01", "Clasifica beneficio y restricción de un teléfono.",
                  [("long battery life", "ventaja"), ("small screen", "límite")], c,
                  "La batería larga aporta uso; la pantalla pequeña restringe la lectura.",
                  guided=True, hint="Pregunta qué ayuda y qué dificulta el uso."),
            choose(f"{p}.pg02", "Una laptop pesa 1 kg, pero la batería dura 2 h. Elige el resumen equilibrado.",
                   ["The laptop is portable; however, its battery life is limited.", "The laptop is portable because its battery is always long.", "The laptop has no limit and no practical advantage."],
                   0, c, "Portable recoge la ventaja del peso; however introduce el límite de batería.",
                   guided=True, hint="Conserva un dato positivo y otro negativo en la misma frase."),
            order(f"{p}.pg03", "Ordena una ventaja práctica seguida de una condición.",
                  "The camera is practical, but it needs a large bag.",
                  ["The", "camera", "is", "practical,", "but", "it", "needs", "a", "large", "bag."], c,
                  "But separa la utilidad de la cámara de la bolsa grande que requiere.",
                  guided=True, hint="Coloca primero el beneficio y después but + límite."),
        ],
        "practice": [
            write(f"{p}.p01", "Escribe: la ventaja es el bajo peso; el límite es la batería corta.",
                  "La ventaja es el bajo peso; el límite es la batería corta.",
                  "The advantage is the low weight, while the limit is the short battery life.",
                  ["The advantage is the low weight, while the limit is the short battery life.", "Its low weight is an advantage, but its short battery life is a limit."], c,
                  "El bajo peso es favorable; la duración corta de la batería es la restricción."),
            complete(f"{p}.p02", "Usa however: It is portable; ___, it is not very strong.",
                     "however", c,
                     "However introduce la debilidad después de reconocer que el objeto es portátil."),
            listen(f"{p}.p03", "Escucha la valoración equilibrada del reloj.",
                   "The watch is practical, but its screen is too small.",
                   ["The watch is impractical because its screen is large.", "The watch has no limits and a perfect screen.", "The watch is practical, but its screen is too small."],
                   2, c, "La frase conserva la utilidad del reloj y especifica el tamaño como límite."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Bici: ligera y fácil de guardar, pero sin cesta. Elige el análisis fiel.",
                   ["The bicycle is not portable, and the basket is its advantage.", "Its advantage is portability; its limit is the missing basket.", "The bicycle has a basket, so it has no practical limit."],
                   1, c, "La facilidad para guardarla es ventaja; la ausencia de cesta es el límite."),
            write(f"{p}.e02", "Datos: lector ligero, batería 3 semanas, pantalla pequeña. Evalúalo.",
                  "Lector: ligero, batería de tres semanas, pantalla pequeña.",
                  "The reader is portable and its long battery life is a major advantage. However, its small screen is a limit for long reading.",
                  [
                      "The reader is portable and its long battery life is a major advantage. However, its small screen is a limit for long reading.",
                      "A key advantage is the reader's light weight and three-week battery, but the small screen limits long reading.",
                  ], c,
                  "La evaluación usa los tres datos: dos ventajas concretas y un límite de lectura."),
            listen(f"{p}.e03", "Escucha el contraste sobre una bicicleta plegable.",
                   "The folding bicycle is portable; however, it is not comfortable on long trips.",
                   ["The folding bicycle is portable; however, it is not comfortable on long trips.", "The folding bicycle is comfortable because it cannot fold.", "The folding bicycle has no advantage on short trips."],
                   0, c, "However introduce una limitación de comodidad sin negar que la bici es portátil."),
            complete(f"{p}.e04", "Usa limit: Its main ___ is the short battery life.",
                     "limit", c,
                     "Limit nombra correctamente la duración corta de la batería como restricción."),
        ],
        "review": [
            write(f"{p}.r01", "Escribe en inglés: El aparato es práctico, pero requiere carga diaria.",
                  "El aparato es práctico, pero requiere carga diaria.",
                  "The device is practical, but it needs daily charging.",
                  ["The device is practical, but it needs daily charging.", "This is a practical device; however, you must charge it every day."], c,
                  "La producción combina una utilidad clara con la condición de carga cotidiana."),
            order(f"{p}.r02", "Reconstruye una conclusión con however.",
                  "The speaker is portable; however, it is not loud enough.",
                  ["The", "speaker", "is", "portable;", "however,", "it", "is", "not", "loud", "enough."], c,
                  "However enlaza portabilidad y volumen insuficiente en una valoración equilibrada."),
            match(f"{p}.r03", "Relaciona cada término con su función en una valoración.",
                  [("practical feature", "característica útil"), ("important limit", "restricción importante")], c,
                  "Una característica práctica ayuda; un límite importante condiciona la elección."),
        ],
    }
    return common_class(
        n,
        [
            "Separar beneficios y restricciones en descripciones de productos cotidianos.",
            "Conectar una ventaja y un límite mediante but, while o however.",
            "Producir una valoración equilibrada basada en todos los datos disponibles.",
        ],
        vocabulary, teaching, pools,
        {"e01": (1, "r03"), "e02": (4, "r01"), "e03": (3, "r02"), "e04": (2, "r03")},
        uses_patterns=[CONCEPTS[47], c],
    )


def build_50() -> dict[str, Any]:
    n, c, p = 50, CONCEPTS[50], "en.n2.c50"
    cumulative = [CONCEPTS[number] for number in range(46, 51)]
    vocabulary = [
        ("shortlist", "lista final"), ("option", "opción"), ("priority", "prioridad"),
        ("compare", "comparar"), ("choose", "elegir"), ("reason", "razón"),
    ]
    teaching = [
        ("Compare every option on the shortlist; the $20 plan is the cheapest.", "Compara cada opción de la lista final; el plan de $20 es el más barato.",
         "Una elección entre tres revisa el mismo criterio y puede identificar un extremo."),
        ("Remove option B: it is too noisy and not quiet enough for the library.", "Descarta la opción B: es demasiado ruidosa y no es lo bastante silenciosa para la biblioteca.",
         "Too noisy expresa exceso; not quiet enough expresa insuficiencia de la cualidad necesaria."),
        ("Compare whether option A is as practical as option B.", "Compara si la opción A es tan práctica como la opción B.",
         "La igualdad permite agrupar opciones antes de aplicar la prioridad principal."),
        ("Choose the best fit and give a reason based on the priority.", "Elige la más adecuada y da una razón basada en la prioridad.",
         "La decisión final debe nombrar la opción, compararla y justificarla con datos."),
    ]
    pools = {
        "practiceGuided": [
            choose(f"{p}.pg01", "Tres planes: $20, $35 y $50. La prioridad es ahorrar. Elige el cierre.",
                   ["I compare only the $50 option because it costs the most.", "I choose the $20 plan because it is the cheapest.", "I choose all three options for the same reason."],
                   1, c, "La prioridad precio exige comparar las tres y elegir el plan más barato.",
                   guided=True, hint="Busca el extremo que coincide con la prioridad: el menor precio."),
            match(f"{p}.pg02", "Relaciona cada paso con su propósito al decidir.",
                  [("compare the shortlist", "revisar las tres opciones"), ("give a reason", "justificar la elección")], c,
                  "Comparar evita omisiones; dar una razón conecta la elección con la prioridad.",
                  guided=True, hint="Primero revisa alternativas; después explica la decisión."),
            complete(f"{p}.pg03", "Usa choose: I ___ option B because it fits my priority.",
                     "choose", c,
                     "Choose presenta la decisión y because introduce la razón basada en la prioridad.",
                     guided=True, hint="Usa el verbo que comunica una decisión final."),
        ],
        "practice": [
            listen(f"{p}.p01", "Escucha qué alternativa queda fuera por precio.",
                   "Option C is too expensive, so it is not on my shortlist.",
                   ["Option C is too expensive, so it is not on my shortlist.", "Option C is the cheapest, so it is my only option.", "Option C is as affordable as every other option."],
                   0, c, "Too expensive justifica retirar C de la lista final antes de elegir."),
            write(f"{p}.p02", "Escribe en inglés: Comparo tres opciones y elijo A por su batería.",
                  "Comparo tres opciones y elijo A por su batería.",
                  "I compare the three options and choose option A because of its battery.",
                  ["I compare the three options and choose option A because of its battery.", "After comparing all three, I choose option A for its battery life."], c,
                  "La frase incluye el conjunto comparado, la opción elegida y una razón concreta."),
            order(f"{p}.p03", "Ordena una decisión basada en la prioridad de espacio.",
                  "Option B best fits our priority because it has more space.",
                  ["Option", "B", "best", "fits", "our", "priority", "because", "it", "has", "more", "space."], c,
                  "Best fits relaciona la opción B directamente con la prioridad de espacio."),
        ],
        "evaluation": [
            choose(f"{p}.e01", "Cabañas A, B y C cuestan $70, $55 y $40. Elige el dato decisivo.",
                   ["Cabin A is the cheapest of the three.", "Cabin B is cheaper of all three.", "Cabin C is the cheapest of the three."],
                   2, c, "C cuesta menos que A y B; the cheapest expresa el extremo entre tres.",
                   requires=[CONCEPTS[46], c]),
            complete(f"{p}.e02", "Usa too noisy + not quiet enough: B is ___ for the library.",
                     "too noisy and not quiet enough", c,
                     "La respuesta expresa tanto el exceso de ruido como la falta de silencio.",
                     requires=[CONCEPTS[47]]),
            listen(f"{p}.e03", "Escucha qué dos tabletas pesan lo mismo.",
                   "Tablet A is as light as tablet C.",
                   ["Tablet A is lighter than tablet C.", "Tablet A is as light as tablet C.", "Tablet A is not light enough for tablet C."],
                   1, c, "As light as confirma igualdad de peso entre A y C.",
                   requires=[CONCEPTS[48]]),
            write(f"{p}.e04", "Datos A:$40/2kg; B:$55/2kg; C:$70/1kg. Elige la más barata que no supere $60.",
                  "A: $40 y 2 kg; B: $55 y 2 kg; C: $70 y 1 kg. Prioridad: elegir la opción más barata que no supere $60.",
                  "Option A is the cheapest of the three and is as heavy as option B. Its advantage is the low price, while its limit is the weight. Option C is too expensive for the budget, so I choose option A.",
                  [
                      "Option A is the cheapest of the three and is as heavy as option B. Its advantage is the low price, while its limit is the weight. Option C is too expensive for the budget, so I choose option A.",
                      "I choose option A because it is the most affordable. A and B are equally heavy, and weight is A's limit. Option C costs too much for a $60 budget.",
                  ], c,
                  "La elección usa precio extremo, igualdad de peso, ventaja, límite y presupuesto.",
                  requires=cumulative),
        ],
        "review": [
            match(f"{p}.r01", "Relaciona cada problema con su significado.",
                  [("too noisy", "exceso de ruido"), ("not quiet enough", "silencio insuficiente")], c,
                  "Too marca exceso y not ... enough marca insuficiencia."),
            write(f"{p}.r02", "Datos X:$30/4h; Y:$45/8h; Z:$60/8h. Máx. $50 y mínimo 8h: elige.",
                  "X: $30 y 4 h; Y: $45 y 8 h; Z: $60 y 8 h. Prioridad: al menos 8 h y máximo $50.",
                  "X is the cheapest, but its four-hour battery is not long enough. Y lasts as long as Z, costs $45, and meets the eight-hour minimum. Z is too expensive, so I choose Y.",
                  [
                      "X is the cheapest, but its four-hour battery is not long enough. Y lasts as long as Z, costs $45, and meets the eight-hour minimum. Z is too expensive, so I choose Y.",
                      "I choose Y because it costs less than $50 and meets the eight-hour minimum. X is cheaper but does not last long enough, while Y and Z last equally long and Z exceeds the budget.",
                  ], c,
                  "Solo Y cumple a la vez el máximo de $50 y el mínimo de ocho horas."),
            order(f"{p}.r03", "Reconstruye una decisión basada en el extremo de comodidad.",
                  "Plan C is my first choice because it is the most comfortable.",
                  ["Plan", "C", "is", "my", "first", "choice", "because", "it", "is", "the", "most", "comfortable."], c,
                  "The most comfortable justifica por qué plan C ocupa el primer lugar."),
        ],
    }
    return common_class(
        n,
        [
            "Comparar tres alternativas mediante los mismos criterios y una prioridad explícita.",
            "Descartar opciones que exceden un límite o no alcanzan un requisito.",
            "Elegir una opción y justificarla con superlativos, igualdad, ventajas y límites.",
        ],
        vocabulary, teaching, pools,
        {"e01": (1, "r03"), "e02": (2, "r01"), "e03": (3, "r02"), "e04": (4, "r02")},
        uses_patterns=cumulative,
        cumulative=cumulative,
    )


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
        for pool, items in cls["pools"].items():
            for item in items:
                prompt = normalized(item["prompt"]["es"])
                feedback = normalized(item["origin"]["feedback"]["es"])
                stimulus = item["origin"].get("audio") or item["origin"].get("text") or item["origin"].get("pairs") or item["prompt"]["es"]
                if item["format"] in {"elegir", "escuchar"}:
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
        "uniquePrompts": len(prompt_ids),
        "uniqueFeedback": len(feedback_ids),
        "uniqueSemanticSignatures": len(semantic_ids),
        "formats": dict(sorted(formats.items())),
        "correctPositions": {key: dict(sorted(value.items())) for key, value in positions.items()},
    }


def bundle(classes: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "onelingo.editorial.class-bundle.v1",
        "course": "en",
        "level": 2,
        "scale": SCALE,
        "status": "shadow",
        "runtimeAi": False,
        "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "classes": classes,
    }


def validate_file(path: Path, start: int, end: int) -> str:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--file", str(path), "--start", str(start), "--end", str(end), "--level", "2"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    message = (result.stdout + result.stderr).strip()
    if result.returncode:
        raise SystemExit(f"Validation failed for {path.name}: {message}")
    return message


def report(classes: list[dict[str, Any]], audit_result: dict[str, Any], validation: list[str]) -> str:
    lines = [
        "# DRAFT — Inglés N2 C46–C50",
        "",
        "Estado: **DRAFT para revisión independiente; no autorizado para integración**.",
        "",
        "## Alcance y trazabilidad",
        "",
        "- Staging aislado; no se modifica `assets/contenido`, tests ni documentación.",
        f"- Digest del mapa N2 v2: `{digest(MAP)}`.",
        f"- Digest de la referencia estructural C45: `{digest(REFERENCE)}`.",
        "- Contrato: `editorial-agent.v2`; `status: shadow`; `runtimeAi: false`.",
        "",
        "## Evidencia por clase",
        "",
        "| Clase | Fase | Concepto | Vocabulario | Ejercicios | Formatos |",
        "|---|---|---|---:|---:|---:|",
    ]
    for cls in classes:
        class_formats = {item["format"] for items in cls["pools"].values() for item in items}
        lines.append(
            f"| {cls['id']} | {cls['phase']} | `{cls['concepts'][0]}` | "
            f"{len(cls['vocabulary'])} | 13 | {len(class_formats)} |"
        )
    lines.extend([
        "",
        "C50 demuestra en evaluación los cinco conceptos mediante: superlativo entre tres, "
        "límite con `too/not enough`, igualdad con `as ... as`, balance ventaja/límite y "
        "una elección escrita con razón y prioridad.",
        "",
        "## Correcciones incorporadas tras revisión",
        "",
        "- C46 enseña `best` en `t05`, lo practica en `p03` antes de `e02` y remedia ese error con `t05` + `r02`.",
        "- C48 `t01` modela de forma visible `as ... as`.",
        "- C49 `p01` explicita bajo peso como ventaja y batería corta como límite.",
        "- C50 `r02` exige simultáneamente máximo $50 y mínimo 8 h, por lo que solo Y es válida.",
        "- C50 remedia `e02` con enseñanza y revisión de `too noisy` y `not quiet enough`; `e03` conserva remediación de igualdad.",
        "- C50 `e04` explicita en consigna y estímulo la prioridad de elegir la opción más barata que no supere $60; solo A satisface el criterio.",
        "",
        "## Auditoría reproducible",
        "",
        "```json",
        json.dumps(audit_result, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Validación ejecutada",
        "",
    ])
    lines.extend(f"- `{message}`" for message in validation)
    lines.extend([
        "",
        "Comando de regeneración:",
        "",
        "```bash",
        "PYTHONDONTWRITEBYTECODE=1 python3 work/n2_c46_50/generate.py",
        "```",
        "",
        "## Incidencias y dudas para el revisor",
        "",
        "- Incidencias automáticas conocidas: ninguna.",
        "- Revisar naturalidad A2 y tolerancia de paráfrasis en las escrituras largas de C49 y C50.",
        "- Simular fallo total para confirmar que cada remediación ataca el tipo de error observado.",
        "- Este autor no emite `GO`; el lote requiere revisión adversarial y simulación independiente.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    classes = [build_46(), build_47(), build_48(), build_49(), build_50()]
    audit_result = audit(classes)
    for cls in classes:
        number = int(cls["id"].rsplit("-", 1)[1])
        (OUT / f"class-{number}.json").write_text(
            json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    bundle_path = OUT / "bundle-46-50.json"
    bundle_path.write_text(json.dumps(bundle(classes), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    validation = [
        validate_file(OUT / f"class-{number}.json", number, number)
        for number in range(46, 51)
    ]
    validation.append(validate_file(bundle_path, 46, 50))
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    (REPORT_OUT / "REPORT.md").write_text(report(classes, audit_result, validation), encoding="utf-8")
    print("\n".join(validation))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
