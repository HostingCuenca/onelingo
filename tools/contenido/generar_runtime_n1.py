#!/usr/bin/env python3
"""Compila el corte editorial inglés aprobado a ruta + exercise-library/1.

El nombre histórico del archivo se conserva para no romper comandos y reportes
anteriores. El corte publicado se declara en ``LEVELS``: nunca descubre clases
por glob ni activa borradores accidentalmente.
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path

import validar_enriquecimiento


ROOT = Path(__file__).resolve().parents[2]
EDITORIAL = ROOT / "assets/contenido/en/editorial"
ROUTE_DIR = ROOT / "assets/contenido/en/ruta"
LIBRARY_OUT = ROOT / "assets/contenido/en/exercise-library.json"
ACTIVATION_OUT = ROOT / "assets/contenido/en/exercise-activation.json"
COURSE_OUT = ROUTE_DIR / "curso.json"
VERSION = "2026.09.30-en-pulido.1"
# Corte publicado: clases aprobadas (GO) por nivel, siempre contiguas desde C1.
# Ampliarlo es una decisión explícita tras la revisión independiente.
CUT = {"n1": 100, "n2": 100, "n3": 100, "n4": 100, "n5": 100}
CEFR = {"n1": "A1", "n2": "A2", "n3": "B1", "n4": "B1", "n5": "B2", "n6": "B2",
        "n7": "B2", "n8": "C1", "n9": "C1", "n10": "C1"}
LEVELS = tuple(
    {"id": level, "count": count, "cefr": CEFR[level], "internal": int(level[1:]),
     "first_order": 7 + 100 * (int(level[1:]) - 1)}
    for level, count in CUT.items()
    if count > 0
)


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(value: dict) -> str:
    payload = {key: item for key, item in value.items() if key not in {"id", "contentHash"}}
    return "sha256:" + hashlib.sha256(canonical(payload).encode()).hexdigest()


def classes(level: str, count: int) -> list[dict]:
    directory = EDITORIAL / level
    if level == "n1":
        pilot = json.loads((directory / "pilot-classes-01-05.json").read_text(encoding="utf-8"))
        result = list(pilot["classes"])
        start = 6
    else:
        result = []
        start = 1
    result.extend(
        json.loads((directory / f"class-{number:02d}.json").read_text(encoding="utf-8"))
        for number in range(start, count + 1)
    )
    return result


def enrichments(level: str, units: dict[str, dict]) -> dict[str, dict]:
    """Capa de enriquecimiento (CONTRATO_ENRIQUECIMIENTO.md) aprobada.

    Solo se fusionan archivos con revisión independiente ``GO``; un borrador
    no cambia el runtime aunque esté en la carpeta.
    """
    result: dict[str, dict] = {}
    for path in sorted((EDITORIAL / level).glob("enriquecimiento-*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if document.get("review", {}).get("status") != "GO":
            continue
        if not set(document["classes"]) & set(units):
            continue  # bloque aún fuera del corte publicado (LEVELS)
        errors, _ = validar_enriquecimiento.validar(path, units)
        if errors:
            raise ValueError(f"{path.name} tiene GO pero no pasa la validación automática: {errors[:5]}")
        for class_id, entry in document["classes"].items():
            if class_id in result:
                raise ValueError(f"{class_id}: enriquecimiento duplicado ({path.name})")
            result[class_id] = entry
    return result


def unenriched_units() -> list[dict]:
    """Todas las clases del corte, sin enriquecer y encadenadas como en el runtime."""
    result = []
    previous = "en.f0.presentarse"
    for spec in LEVELS:
        for document in classes(spec["id"], spec["count"]):
            result.append(
                route_unit(
                    document,
                    level=spec["id"],
                    cefr=spec["cefr"],
                    internal=spec["internal"],
                    first_order=spec["first_order"],
                    previous=previous,
                )
            )
            previous = document["id"]
    return result


def es(text: str) -> dict:
    return {"es": text}


def number_of(document: dict) -> int:
    return int(document["id"].rsplit("-", 1)[1])


def family_id(exercise_id: str) -> str:
    return "ex.onelingo." + exercise_id.replace("en.", "", 1)


FILL_CUES: dict[str, dict] = {}


def load_fill_cues() -> dict[str, dict]:
    """Pistas de «completar» aprobadas (correcciones-completar.json con GO).

    Cada entrada da la frase con hueco, su traducción completa como pista y
    las respuestas aceptadas con esa pista.
    """
    cues: dict[str, dict] = {}
    for spec in LEVELS:
        path = EDITORIAL / spec["id"] / "correcciones-completar.json"
        if not path.exists():
            continue
        document = json.loads(path.read_text(encoding="utf-8"))
        if document.get("review", {}).get("status") != "GO":
            continue
        for exercise_id, entry in document["items"].items():
            if entry["frase"].count("___") != 1:
                raise ValueError(f"{exercise_id}: la frase debe tener un solo hueco")
            if not entry.get("pista", "").strip():
                raise ValueError(f"{exercise_id}: falta la pista")
            cues[exercise_id] = entry
    return cues


def apply_fill_cue(source: dict) -> None:
    cue = FILL_CUES.get(source.get("id", ""))
    if cue is None or source.get("format") != "completar":
        return
    answer = source.setdefault("answer", {})
    original = str(answer.get("text", ""))
    accepted = list(dict.fromkeys([original, *answer.get("accepted", []), *cue.get("aceptadas", [])]))
    answer["accepted"] = accepted
    origin = source.setdefault("origin", {})
    passage = str(origin.get("text") or "").strip()
    if passage and passage != "___" and "___" not in passage:
        # «Lee y completa»: se conserva el texto de lectura encima de la frase.
        origin["text"] = f"{passage}\n\n{cue['frase']}"
        source["prompt"] = {"es": f"Lee y completa la frase: «{cue['pista']}»"}
    else:
        origin["text"] = cue["frase"]
        source["prompt"] = {"es": f"Completa la frase: «{cue['pista']}»"}


ITEM_FIXES: dict[str, dict] = {}


def load_item_fixes() -> dict[str, dict]:
    """Correcciones de ejercicios aprobadas (correcciones-items.json con GO)."""
    fixes: dict[str, dict] = {}
    for spec in LEVELS:
        path = EDITORIAL / spec["id"] / "correcciones-items.json"
        if not path.exists():
            continue
        document = json.loads(path.read_text(encoding="utf-8"))
        if document.get("review", {}).get("status") != "GO":
            continue
        fixes.update(document["items"])
    return fixes


def apply_item_fix(source: dict) -> None:
    fix = ITEM_FIXES.get(source.get("id", ""))
    if fix is None:
        return
    exercise_id = source["id"]
    answer = source.setdefault("answer", {})
    origin = source.setdefault("origin", {})
    if "prompt" in fix:
        source["prompt"] = {"es": fix["prompt"]}
    if "choices" in fix:
        source["choices"] = [{"text": text} for text in fix["choices"]]
    if "answerIndex" in fix:
        answer["index"] = fix["answerIndex"]
    if "answerText" in fix:
        answer["text"] = fix["answerText"]
    if "accepted" in fix:
        answer["accepted"] = list(dict.fromkeys([answer.get("text", ""), *fix["accepted"]]))
    if "tokens" in fix:
        answer["tokens"] = fix["tokens"]
    for key, target in (("feedback", "feedback"), ("hint", "hint")):
        if key in fix:
            origin[target] = {"es": fix[key]}
    for key in ("text", "audio"):
        if key in fix:
            origin[key] = fix[key]
    if "pairs" in fix:
        pairs = [[left, {"es": right}] for left, right in fix["pairs"]]
        origin["pairs"] = pairs
        answer["pairs"] = pairs
    if source.get("format") in {"elegir", "escuchar"}:
        choices = source.get("choices", [])
        if len(choices) < 3 or not 0 <= int(answer.get("index", -1)) < len(choices):
            raise ValueError(f"{exercise_id}: corrección con opciones o índice inválidos")
    if source.get("format") == "ordenar" and answer.get("tokens"):
        if " ".join(answer["tokens"]) != answer.get("text", "").strip():
            raise ValueError(f"{exercise_id}: las fichas no forman la respuesta")


def normalized_exercise(document: dict, class_document: dict) -> dict:
    source = deepcopy(document)
    apply_fill_cue(source)
    apply_item_fix(source)
    origin = source.setdefault("origin", {})
    if (
        source.get("format") == "completar"
        and not origin.get("sentences")
        and not origin.get("text")
    ):
        # La consigna de apoyo ya contiene el contexto completo. La vista de
        # completar necesita además una plantilla con hueco, sin interpretar
        # el español de apoyo como vocabulario de la lengua meta.
        origin["text"] = "___"
    if source.get("format") == "relacionar":
        # La interacción está diseñada para 3–5 pares por pantalla. Los cierres
        # editoriales que reúnen más evidencia se recortan de forma estable.
        pairs = list(origin.get("pairs") or source.get("answer", {}).get("pairs") or [])[:5]
        used_left = {str(pair[0]).casefold() for pair in pairs}
        used_right = {
            str((pair[1] or {}).get("es", "")).casefold()
            for pair in pairs
            if isinstance(pair, list) and len(pair) == 2 and isinstance(pair[1], dict)
        }
        if len(pairs) < 3:
            for entry in class_document.get("vocabulary", []):
                left, right = str(entry.get("en", "")), str(entry.get("es", ""))
                if left and right and left.casefold() not in used_left and right.casefold() not in used_right:
                    pairs.append([left, {"es": right}])
                    used_left.add(left.casefold())
                    used_right.add(right.casefold())
                    if len(pairs) >= 3:
                        break
        origin["pairs"] = pairs
        source.setdefault("answer", {})["pairs"] = pairs
    open_production(source)
    return source


OPEN_WORDS = 12
WORD_RANGE = re.compile(r"(\d+)\s*[–-]\s*(\d+)\s*palabras")


def open_production(source: dict) -> None:
    """Escritura larga sin rúbrica: producción abierta, no puntuable.

    Un texto de más de ``OPEN_WORDS`` palabras tiene muchas formas correctas;
    compararlo con una o dos soluciones exactas rechaza respuestas válidas.
    Sin IA en runtime, el alumno escribe dentro de un rango de extensión y
    después compara su texto con el modelo. Los ítems con ``evidenceGroups``
    conservan su rúbrica determinista y siguen puntuando.
    """
    if source.get("format") != "escribir":
        return
    origin = source.setdefault("origin", {})
    scoring = origin.setdefault("scoring", {})
    if scoring.get("evidenceGroups"):
        return
    words = len(str(source.get("answer", {}).get("text", "")).split())
    if words <= OPEN_WORDS:
        if not scoring:
            origin.pop("scoring")
        return
    scoring["openProduction"] = True
    if not scoring.get("wordRange"):
        prompt = str((source.get("prompt") or {}).get("es", ""))
        match = WORD_RANGE.search(prompt)
        scoring["wordRange"] = (
            [int(match.group(1)), int(match.group(2))]
            if match
            else [max(4, round(words * 0.6)), round(words * 1.8) + 5]
        )


def variant(document: dict, pool: str, class_document: dict) -> tuple[dict, dict]:
    source = normalized_exercise(document, class_document)
    origin = dict(source.get("origin", {}))
    origin["editorialId"] = source["id"]
    source["origin"] = origin
    family = family_id(source["id"])
    source["id"] = f"{family}:v1:{pool}"
    source["contentHash"] = content_hash(source)
    family_document = {
        "id": family,
        "revision": 1,
        "concepts": list(dict.fromkeys([*source.get("teaches", []), *source.get("requires", [])])),
        "skills": [],
        "variants": [source],
    }
    return source, family_document


def support(value: object, fallback: str = "") -> dict:
    if isinstance(value, dict):
        text = str(value.get("es") or next(iter(value.values()), fallback))
    else:
        text = str(value or fallback)
    return {"es": text}


def accepted_parts(answer: dict) -> list[list[str]]:
    result = []
    for part in answer.get("parts", []):
        if isinstance(part, dict):
            result.append(
                list(
                    dict.fromkeys(
                        [str(part.get("text", "")), *map(str, part.get("accepted", []))]
                    )
                )
            )
        else:
            result.append([str(part)])
    return result


def route_item(source: dict, pool: str, class_document: dict) -> dict:
    source = normalized_exercise(source, class_document)
    converted, _ = variant(source, pool, class_document)
    answer = source.get("answer", {})
    origin = source.get("origin", {})
    item = {
        "id": converted["id"],
        "formato": source["format"],
        "consigna": support(source.get("prompt"), "Resuelve el ejercicio."),
        "feedback": support(origin.get("feedback"), "Revisa el modelo y vuelve a intentarlo."),
    }
    if origin.get("hint") is not None:
        item["pista"] = support(origin["hint"])
    choices = [choice.get("text") for choice in source.get("choices", [])]
    if choices:
        item["opciones"] = choices
    if source["format"] in {"elegir", "escuchar"}:
        item["respuesta"] = int(answer["index"])
    elif source["format"] == "relacionar":
        item["pares"] = origin.get("pairs") or answer.get("pairs") or []
        item["respuesta"] = True
    else:
        item["respuesta"] = answer.get("text") or answer.get("value") or ""
        if answer.get("accepted"):
            item["aceptadas"] = answer["accepted"]
        if answer.get("tokens"):
            item["tokens"] = answer["tokens"]
    if origin.get("text") is not None:
        item["texto"] = origin["text"]
    if source["format"] == "completar" and "___" not in str(item.get("texto", "")):
        # El ítem embebido es solo fallback; el runtime activo usa la variante
        # completa de la biblioteca (incluido su texto/fuente). El contrato de
        # ruta legado exige una plantilla con hueco incluso para multipartes.
        item["texto"] = "___"
    if origin.get("sentences"):
        item["textosPartes"] = origin["sentences"]
    if answer.get("parts"):
        item["respuestasPartes"] = accepted_parts(answer)
    scoring = origin.get("scoring") or {}
    if scoring.get("parts", scoring.get("total")) is not None:
        item["partesPuntuables"] = scoring.get("parts", scoring.get("total"))
    if scoring.get("minimumCorrect") is not None:
        item["minimoCorrectas"] = scoring["minimumCorrect"]
    if scoring.get("requiredParts"):
        item["partesObligatorias"] = scoring["requiredParts"]
    if scoring.get("wordRange"):
        item["minimoPalabras"], item["maximoPalabras"] = scoring["wordRange"]
    if scoring.get("evidenceGroups"):
        item["evidenciasEscritura"] = scoring["evidenceGroups"]
    if scoring.get("openProduction"):
        item["abierta"] = True
    if origin.get("audio") is not None:
        item["audio"] = origin["audio"]
    if origin.get("imageAsset") is not None:
        item["imagen"] = origin["imageAsset"]
        item["imagenAlt"] = origin.get("imageAlt", "Apoyo visual del ejercicio.")
    return item


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "expresion"


def vocabulary(document: dict, level: str, number: int) -> list[dict]:
    translated = {
        str(entry.get("en", "")).casefold(): str(entry.get("es", "expresión del curso"))
        for entry in document.get("vocabulary", [])
    }
    values = list(document.get("usesVocabulary", []))
    values.extend(entry.get("en", "") for entry in document.get("vocabulary", []))
    values.extend(item.get("en", "") for item in document.get("teaching", []))
    for exercises in document.get("pools", {}).values():
        for raw_exercise in exercises:
            # El contenido efectivo, con pistas y correcciones aplicadas.
            exercise = normalized_exercise(raw_exercise, document)
            values.extend(
                choice.get("text", "")
                for choice in exercise.get("choices", [])
                if isinstance(choice.get("text"), str)
            )
            answer = exercise.get("answer", {})
            values.append(answer.get("text", ""))
            values.extend(answer.get("tokens", []))
            for part in accepted_parts(answer):
                values.extend(part)
            origin = exercise.get("origin", {})
            values.append(origin.get("audio", ""))
            values.append(origin.get("text", ""))
            values.extend(origin.get("sentences", []))
            for pair in origin.get("pairs") or answer.get("pairs") or []:
                if isinstance(pair, list) and pair:
                    values.append(pair[0])
    result = []
    seen = set()
    for index, text in enumerate(values, 1):
        text = str(text).strip()
        if not text or text.casefold() in seen:
            continue
        seen.add(text.casefold())
        result.append(
            {
                "id": f"v-{level}-{number:03d}-{index:03d}-{slug(text)[:28]}",
                "texto": text,
                "traduccion": {"es": translated.get(text.casefold(), "expresión del curso")},
            }
        )
    return result


def route_unit(
    document: dict,
    *,
    level: str,
    cefr: str,
    internal: int,
    first_order: int,
    previous: str,
    enrichment: dict | None = None,
) -> dict:
    number = number_of(document)
    title = document.get("title", {})
    objective = (document.get("objectives", {}).get("es") or ["Completar la clase con autonomía."])[0]
    teaching = document.get("teaching", [])
    first_sentence = teaching[0].get("en", "English") if teaching else "English"
    first_translation = teaching[0].get("es", "Inglés") if teaching else "Inglés"
    words = vocabulary(document, level, number)
    # El inventario completo declara también tokens usados por los ejercicios
    # para que el validador cronológico pueda comprobarlos. La pantalla de
    # vocabulario, en cambio, debe enseñar solo la selección editorial explícita
    # de la clase y no exponer distractores, frases completas ni tokens internos.
    explicit_vocabulary = {
        str(entry.get("en", "")).strip().casefold()
        for entry in document.get("vocabulary", [])
        if str(entry.get("en", "")).strip()
    }
    visible_vocabulary_refs = [
        entry["id"]
        for entry in words
        if str(entry.get("texto", "")).strip().casefold() in explicit_vocabulary
    ]
    guided = [
        route_item(item, "practiceGuided", document)
        for item in document["pools"]["practiceGuided"]
    ]
    practice = [
        route_item(item, "practice", document)
        for item in document["pools"]["practice"]
    ]
    evaluation = [
        route_item(item, "evaluation", document)
        for item in document["pools"]["evaluation"]
    ]
    formats = {
        exercise.get("format")
        for pool in ("practiceGuided", "practice", "evaluation")
        for exercises in [document.get("pools", {}).get(pool, [])]
        for exercise in exercises
    }
    skills = list(dict.fromkeys(document.get("skills", ["gramatica"])))
    if "escritura" in skills and not formats.intersection({"escribir", "ordenar", "completar"}):
        skills.remove("escritura")
    situation_item = deepcopy(practice[0])
    situation_item["id"] = f"ex.onelingo.{level}.c{number:02d}.situation-check:v1:application"
    prefix = f"en.{level}.class-{number:02d}"
    teaching_items = [
        {
            "texto": item.get("en", ""),
            "traduccion": {"es": item.get("es", "")},
            "nota": {"es": item.get("explanationEs", "Observa el modelo.")},
        }
        for item in teaching
    ]
    situation = {
        "id": f"{prefix}.situation",
        "tipo": "situacion",
        "contexto": {"es": "Usa el modelo de la clase en una situación breve."},
        "dialogo": [
            {"hablante": "Modelo", "texto": first_sentence, "traduccion": {"es": first_translation}}
        ],
        "items": [situation_item],
    }
    frequent_errors = [
        {
            "incorrecto": first_sentence.rstrip(".") + " ?",
            "correcto": first_sentence,
            "explicacion": {"es": "Conserva el orden y la forma del modelo enseñado."},
        }
    ]
    explanation_steps = [
        {
            "id": f"{prefix}.explanation",
            "tipo": "explicacion",
            "titulo": {"es": "Objetivo de la clase"},
            "texto": {"es": objective},
        }
    ]
    if enrichment:
        explanation = enrichment["explicacion"]
        explanation_steps = [
            {
                "id": f"{prefix}.explanation",
                "tipo": "explicacion",
                "titulo": es(explanation["titulo"]),
                "texto": es(explanation["texto"]),
            }
        ]
        pattern = enrichment.get("patron")
        if pattern:
            explanation_steps.append(
                {
                    "id": f"{prefix}.pattern",
                    "tipo": "patron",
                    "texto": es(pattern["texto"]),
                    "formula": [
                        {"texto": segment["texto"], "nota": es(segment["nota"])}
                        for segment in pattern["formula"]
                    ],
                }
            )
        table = enrichment.get("tabla")
        if table:
            explanation_steps.append(
                {
                    "id": f"{prefix}.table",
                    "tipo": "tabla",
                    "columnas": [es(column) for column in table["columnas"]],
                    "filas": [
                        [
                            {
                                key: (es(value) if key == "apoyo" else value)
                                for key, value in cell.items()
                            }
                            for cell in row
                        ]
                        for row in table["filas"]
                    ],
                }
            )
        for replacement in enrichment.get("ejemplos", []):
            teaching_items[replacement["indice"]] = {
                "texto": replacement["en"],
                "traduccion": es(replacement["es"]),
                "nota": es(replacement["nota"]),
            }
        frequent_errors = [
            {
                "incorrecto": error["incorrecto"],
                "correcto": error["correcto"],
                "explicacion": es(error["explicacion"]),
            }
            for error in enrichment["erroresFrecuentes"]
        ]
        authored = enrichment["situacion"]
        item = authored["item"]
        situation_item = {
            "id": f"ex.onelingo.{level}.c{number:02d}.situation:v2:application",
            "formato": item["formato"],
            "consigna": es(item["consigna"]),
            "feedback": es(item["feedback"]),
            "opciones": list(item["opciones"]),
            "respuesta": item["respuesta"],
        }
        if item.get("audio"):
            situation_item["audio"] = item["audio"]
        situation = {
            "id": f"{prefix}.situation",
            "tipo": "situacion",
            "contexto": es(authored["contexto"]),
            "dialogo": [
                {"hablante": line["hablante"], "texto": line["texto"], "traduccion": es(line["traduccion"])}
                for line in authored["dialogo"]
            ],
            "items": [situation_item],
        }
    steps = [
        *explanation_steps,
        {
            "id": f"en.{level}.class-{number:02d}.vocabulary",
            "tipo": "vocabulario",
            "refs": visible_vocabulary_refs,
        },
        {
            "id": f"en.{level}.class-{number:02d}.teaching",
            "tipo": "ejemplos",
            "titulo": {"es": "Aprende y observa"},
            "items": teaching_items,
        },
        {
            "id": f"en.{level}.class-{number:02d}.guided",
            "tipo": "practica_guiada",
            "items": guided,
        },
        {
            "id": f"en.{level}.class-{number:02d}.practice",
            "tipo": "practica_independiente",
            "items": practice,
        },
        situation,
        {
            "id": f"en.{level}.class-{number:02d}.evaluation",
            "tipo": "evaluacion",
            "items": evaluation,
        },
    ]
    return {
        "id": document["id"],
        "orden": first_order + number - 1,
        "titulo": {"es": str(title.get("es") or title.get("en") or f"Clase {number}")},
        "objetivo": {"es": objective},
        "cefr": cefr,
        "nivelInterno": internal,
        "concepto": document.get("concepts", [f"{level}-class-{number:03d}"])[0],
        "prerequisitos": [previous],
        "habilidades": skills,
        "gramatica": list(document.get("usesPatterns", [])),
        "vocabulario": words,
        "erroresFrecuentes": frequent_errors,
        "pasos": steps,
        "criterioDominio": {"umbral": 0.8},
        "repaso": {"intervalosDias": [1, 3, 7, 16, 35, 90]},
        "tutor": {"opcional": True, "runtimeAiRequired": False},
    }


def compile_runtime() -> tuple[dict[str, dict], dict, dict, dict]:
    FILL_CUES.clear()
    FILL_CUES.update(load_fill_cues())
    ITEM_FIXES.clear()
    ITEM_FIXES.update(load_item_fixes())
    library = {
        "schema": "exercise-library/1",
        "libraryId": "onelingo-en-editorial",
        "version": VERSION,
        "course": "en",
        "units": {},
        "families": [],
    }
    previous = "en.f0.presentarse"
    # La validación del enriquecimiento compara con las clases sin enriquecer.
    base_units = {unit["id"]: unit for unit in unenriched_units()}
    routes = {}
    active_ids = []
    for spec in LEVELS:
        level = spec["id"]
        documents = classes(level, spec["count"])
        enriched = enrichments(level, base_units)
        unknown = set(enriched) - {document["id"] for document in documents}
        if unknown:
            raise ValueError(f"enriquecimiento de clases fuera del corte: {sorted(unknown)}")
        if len(documents) != spec["count"]:
            raise ValueError(f"expected {spec['count']} {level} classes, got {len(documents)}")
        route_units = []
        for document in documents:
            number = number_of(document)
            unit_pools = {}
            for pool in ["practiceGuided", "practice", "evaluation", "review"]:
                references = []
                for exercise in document["pools"][pool]:
                    converted, family = variant(exercise, pool, document)
                    family["concepts"] = list(document.get("concepts", []))
                    family["skills"] = list(document.get("skills", []))
                    library["families"].append(family)
                    references.append(converted["id"])
                unit_pools[pool] = references
            unit_pools["teaching"] = []
            library["units"][document["id"]] = {
                "concepts": list(document.get("concepts", [])),
                "skills": list(document.get("skills", [])),
                "prerequisites": [previous],
                "pools": unit_pools,
            }
            route_units.append(
                route_unit(
                    document,
                    level=level,
                    cefr=spec["cefr"],
                    internal=spec["internal"],
                    first_order=spec["first_order"],
                    previous=previous,
                    enrichment=enriched.get(document["id"]),
                )
            )
            active_ids.append(document["id"])
            previous = document["id"]
        routes[level] = {"modulo": f"en.{level}.editorial", "unidades": route_units}
    activation = {
        "schema": "exercise-activation/1",
        "course": "en",
        "version": VERSION,
        "units": {unit_id: "active" for unit_id in active_ids},
    }
    course = json.loads(COURSE_OUT.read_text(encoding="utf-8"))
    published = {spec["id"]: spec for spec in LEVELS}
    for level in course["niveles"]:
        if level["id"] in published:
            level["estado"] = "publicado"
            level["nivelInterno"] = published[level["id"]]["internal"]
    course["modulos"] = [
        module for module in course["modulos"] if module["nivel"] not in published
    ] + [
        {
            "id": f"en.{spec['id']}.editorial",
            "nivel": spec["id"],
            "archivo": f"{spec['id']}-editorial.json",
            "titulo": {"es": f"Inglés {spec['id'].upper()} · {spec['cefr']}"},
        }
        for spec in LEVELS
    ]
    return routes, library, activation, course


def compact(value: object) -> str:
    # Artefactos que descarga la app: sin sangría (≈40 % menos de bytes). La
    # fuente legible es el JSON editorial de assets/contenido/en/editorial/.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n"


def main() -> int:
    routes, library, activation, course = compile_runtime()
    for level, route in routes.items():
        (ROUTE_DIR / f"{level}-editorial.json").write_text(compact(route), encoding="utf-8")
    LIBRARY_OUT.write_text(compact(library), encoding="utf-8")
    ACTIVATION_OUT.write_text(json.dumps(activation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    COURSE_OUT.write_text(json.dumps(course, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"OK: {sum(len(route['unidades']) for route in routes.values())} route units; "
        f"{len(library['families'])} variants; {len(activation['units'])} active"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
