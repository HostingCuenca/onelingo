#!/usr/bin/env python3
"""Validador editorial genérico para bundles de Inglés N1-N10.

No modifica el bundle. La validación cubre contrato estructural, cronología de
conceptos, semántica mínima de formatos, hashes, separación de pools y cierres
acumulativos. Uso:

    python3 validate_bundle.py --file bundle.json --start 1 --end 5
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from typing import Any, Iterable


ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_BUNDLE = "onelingo.editorial.class-bundle.v1"
SCHEMA_CLASS = "onelingo.editorial.class.v1"
SCALE = "client-10-levels-v1"
POOLS = ("practiceGuided", "practice", "evaluation", "review")
POOL_PREFIX = {"practiceGuided": "pg", "practice": "p", "evaluation": "e", "review": "r"}
MINIMUMS = {"practiceGuided": 3, "practice": 3, "evaluation": 4, "review": 3}
FORMATS = {"elegir", "escuchar", "ordenar", "completar", "escribir", "relacionar"}
WORD_RE = re.compile(r"[a-záéíóúüñ0-9]+(?:'[a-záéíóúüñ0-9]+)?", re.I)
AI_RE = re.compile(r"\b(?:ai|ia|llm|openai|chatgpt|inteligencia artificial|tutor ia)\b", re.I)
AGENT_CONTRACT_V2 = "editorial-agent.v2"
DEICTIC_PROMPT_RE = re.compile(
    r"\b(?:idea trabajada|modelo (?:correcto|de la clase)|tercer modelo|"
    r"contexto nuevo|frase indicada|oraci[oó]n indicada|informaci[oó]n indicada)\b",
    re.I,
)
GENERIC_PROMPTS = {
    "elige",
    "elige la opcion",
    "elige la opcion correcta",
    "elige la opción",
    "elige la opción correcta",
    "selecciona la respuesta",
    "selecciona la respuesta correcta",
    "responde",
    "completa",
    "escribe",
    "ordena",
    "relaciona",
    "escucha y elige",
    "practica",
}
FEEDBACK_ORDINAL_PATTERNS = {
    0: re.compile(
        r"\b(?:the first|la primera|el primero)\s+"
        r"(?:option|answer|response|statement|choice|opci[oó]n|respuesta|frase|afirmaci[oó]n)\b"
        r"[^.;]{0,45}\b(?:is correct|is the only|preserves?|keeps?|shows?|uses?|relies|promises only|"
        r"es correcta|es la [uú]nica|conserva|mantiene|muestra|usa|se apoya)\b",
        re.I,
    ),
    1: re.compile(
        r"\b(?:the second|la segunda|el segundo)\s+"
        r"(?:option|answer|response|statement|choice|opci[oó]n|respuesta|frase|afirmaci[oó]n)\b"
        r"[^.;]{0,45}\b(?:is correct|is the only|preserves?|keeps?|shows?|uses?|relies|promises only|"
        r"es correcta|es la [uú]nica|conserva|mantiene|muestra|usa|se apoya)\b",
        re.I,
    ),
    2: re.compile(
        r"\b(?:the third|la tercera|el tercero)\s+"
        r"(?:option|answer|response|statement|choice|opci[oó]n|respuesta|frase|afirmaci[oó]n)\b"
        r"[^.;]{0,45}\b(?:is correct|is the only|preserves?|keeps?|shows?|uses?|relies|promises only|"
        r"es correcta|es la [uú]nica|conserva|mantiene|muestra|usa|se apoya)\b",
        re.I,
    ),
}


class ValidationError(AssertionError):
    """Error editorial con ubicación legible."""


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_without_identity(item: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in item.items() if key not in {"id", "contentHash"}}


def expected_hash(item: dict[str, Any]) -> str:
    payload = canonical(content_without_identity(item)).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def words(value: str) -> list[str]:
    return [part.casefold() for part in WORD_RE.findall(value)]


def normalized(value: Any) -> str:
    if not isinstance(value, str):
        value = canonical(value)
    return " ".join(words(value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def require_string(value: Any, message: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), message)
    return value


def require_string_list(value: Any, message: str, *, allow_empty: bool = False) -> list[str]:
    require(isinstance(value, list), message)
    require(allow_empty or bool(value), message)
    require(all(isinstance(part, str) and part.strip() for part in value), message)
    require(len(value) == len(set(value)), f"{message}: duplicates")
    return value


def walk_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, part in value.items():
            yield str(key)
            yield from walk_strings(part)
    elif isinstance(value, list):
        for part in value:
            yield from walk_strings(part)


def validate_no_ai(data: Any) -> None:
    for text in walk_strings(data):
        require(AI_RE.search(text) is None, f"runtime AI reference forbidden: {text!r}")


def normalize_document(data: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Normaliza un lote o una clase incremental al mismo recorrido interno."""

    require(isinstance(data, dict), "document root must be an object")
    schema = data.get("schema")
    if schema == SCHEMA_BUNDLE:
        classes = data.get("classes")
        require(isinstance(classes, list), "bundle classes must be a list")
        return data, classes
    if schema == SCHEMA_CLASS:
        # En el flujo incremental la raíz contiene a la vez metadatos y clase.
        return data, [data]
    raise ValidationError(f"wrong schema: {schema!r}")


def answer_semantics(item: dict[str, Any]) -> Any:
    fmt = item["format"]
    answer = item["answer"]
    if fmt in {"elegir", "escuchar"}:
        index = answer["index"]
        return item["choices"][index]["text"]
    if fmt == "completar" and isinstance(answer.get("parts"), list):
        return [part.get("text") if isinstance(part, dict) else part for part in answer["parts"]]
    if fmt in {"ordenar", "completar", "escribir"}:
        return answer["text"]
    if fmt == "relacionar":
        return sorted(
            (
                normalized(pair[0]),
                normalized(pair[1].get("es") if isinstance(pair[1], dict) else pair[1]),
            )
            for pair in answer["pairs"]
        )
    raise ValidationError(f"unsupported semantic format: {fmt}")


def reusable_answer_signature(item: dict[str, Any]) -> str | None:
    """Reserva respuestas con evidencia suficiente para detectar reutilización."""

    semantics = answer_semantics(item)
    if item.get("format") == "relacionar":
        return normalized(semantics)
    return normalized(semantics) if len(words(str(semantics))) >= 2 else None


def answer_evidence_signatures(item: dict[str, Any]) -> set[str]:
    """Extrae respuestas inglesas multitérmino sin depender del formato."""

    if item.get("format") == "relacionar":
        candidates = [pair[0] for pair in item["answer"]["pairs"]]
    else:
        candidates = [answer_semantics(item)]
    return {
        normalized(candidate)
        for candidate in candidates
        if isinstance(candidate, str) and len(words(candidate)) >= 2
    }


def register_answer_evidence(
    item: dict[str, Any],
    pool: str,
    early: dict[str, str],
    reserved: dict[str, str],
) -> None:
    """Aplica la frontera estricta de evidencia entre pools de una clase."""

    signatures = answer_evidence_signatures(item)
    if pool in {"practiceGuided", "practice"}:
        for signature in signatures:
            require(signature not in early, f"{item['id']}: answer evidence duplicate inside practice pools {early.get(signature)}")
            require(signature not in reserved, f"{item['id']}: answer evidence duplicate of reserved {reserved.get(signature)}")
            early.setdefault(signature, item["id"])
    else:
        for signature in signatures:
            require(signature not in early, f"{item['id']}: answer evidence duplicate of practice {early.get(signature)}")
            require(signature not in reserved, f"{item['id']}: answer evidence duplicate inside reserved pools {reserved.get(signature)}")
            reserved.setdefault(signature, item["id"])


def stimulus_semantics(item: dict[str, Any]) -> Any:
    origin = item["origin"]
    fmt = item["format"]
    if fmt == "escuchar":
        stimulus = origin.get("audio")
    elif fmt == "relacionar":
        stimulus = origin.get("pairs")
    else:
        stimulus = origin.get("text") or origin.get("sentences") or item["prompt"].get("es")
    return stimulus


def semantic_signature(item: dict[str, Any]) -> str:
    """Ignora IDs, pool, distractores y orden de opciones.

    Así, reordenar opciones o mover el mismo estímulo/respuesta a un pool
    reservado no crea una variante pedagógica nueva.
    """

    return normalized({"stimulus": stimulus_semantics(item), "answer": answer_semantics(item)})


def atomic_pair_signatures(item: dict[str, Any]) -> set[str]:
    """Treat every matching association as exposed evidence."""

    if item.get("format") != "relacionar":
        return set()
    return {
        normalized(
            {
                "left": pair[0],
                "right": pair[1].get("es")
                if isinstance(pair[1], dict)
                else pair[1],
            }
        )
        for pair in item["answer"]["pairs"]
    }


def validate_prompt(item: dict[str, Any], where: str) -> None:
    prompt = item.get("prompt")
    require(isinstance(prompt, dict), f"{where}: prompt must be an object")
    text = require_string(prompt.get("es"), f"{where}: prompt.es missing")
    require(len(text.strip()) >= 8, f"{where}: prompt.es too short")
    generic = normalized(text) in GENERIC_PROMPTS
    external_stimulus = item.get("origin", {}).get("audio") or item.get("origin", {}).get("text") or item.get("origin", {}).get("pairs") or item.get("origin", {}).get("sentences")
    require(not generic or bool(external_stimulus), f"{where}: generic/unresolvable prompt")
    if item.get("format") == "completar":
        require(
            "___" in text
            or isinstance(item.get("origin", {}).get("text"), str)
            or isinstance(item.get("origin", {}).get("sentences"), list),
            f"{where}: completar needs a visible blank or stimulus",
        )
        if "___" in text and not isinstance(item.get("origin", {}).get("text"), str):
            visible = text.split(":", 1)[-1].replace("___", " ")
            lexical_tokens = re.findall(r"[^\W_]+", visible, flags=re.UNICODE)
            require(len(lexical_tokens) >= 2, f"{where}: completar prompt is underspecified")


def validate_choices(item: dict[str, Any], where: str) -> None:
    choices = item.get("choices")
    require(isinstance(choices, list) and len(choices) >= 2, f"{where}: choices required")
    texts: list[str] = []
    for number, choice in enumerate(choices, 1):
        require(isinstance(choice, dict), f"{where}: choice {number} must be an object")
        texts.append(require_string(choice.get("text"), f"{where}: choice {number} missing text").casefold())
    require(len(texts) == len(set(texts)), f"{where}: duplicate choices")
    index = item["answer"].get("index")
    require(isinstance(index, int) and not isinstance(index, bool), f"{where}: answer.index must be int")
    require(0 <= index < len(choices), f"{where}: answer.index out of range")


def validate_feedback_ordinal(item: dict[str, Any], where: str) -> None:
    """Reject explicit ordinal feedback that contradicts the answer key.

    The check is deliberately narrow: it only interprets an ordinal when it
    directly qualifies option/answer/response/statement/choice and makes a
    positive correctness claim. This avoids treating explanations of a wrong
    distractor ("the first option rejects without politeness") as answer keys.
    """

    if item.get("format") not in {"elegir", "escuchar"}:
        return
    feedback = item["origin"]["feedback"]["es"]
    mentioned = [index for index, pattern in FEEDBACK_ORDINAL_PATTERNS.items() if pattern.search(feedback)]
    require(len(mentioned) <= 1, f"{where}: feedback contains conflicting answer ordinals")
    if mentioned:
        require(
            mentioned[0] == item["answer"]["index"],
            f"{where}: feedback ordinal contradicts answer.index",
        )


def validate_pairs(item: dict[str, Any], where: str) -> None:
    pairs = item["origin"].get("pairs")
    answer_pairs = item["answer"].get("pairs")
    require(isinstance(pairs, list) and len(pairs) >= 2, f"{where}: pairs required")
    require(answer_pairs == pairs, f"{where}: answer.pairs must match origin.pairs")
    lefts: set[str] = set()
    rights: set[str] = set()
    for number, pair in enumerate(pairs, 1):
        require(isinstance(pair, list) and len(pair) == 2, f"{where}: invalid pair {number}")
        left = require_string(pair[0], f"{where}: pair {number} left missing").casefold()
        right_value = pair[1].get("es") if isinstance(pair[1], dict) else pair[1]
        right = require_string(right_value, f"{where}: pair {number} right missing").casefold()
        require(left not in lefts and right not in rights, f"{where}: duplicate pair side")
        lefts.add(left)
        rights.add(right)


def validate_format(item: dict[str, Any], where: str) -> None:
    fmt = item["format"]
    answer = item["answer"]
    scoring = item["origin"].get("scoring")
    if scoring is not None:
        require(isinstance(scoring, dict), f"{where}: scoring must be an object")
        parts = scoring.get("parts", scoring.get("total"))
        minimum = scoring.get("minimumCorrect")
        if parts is not None or minimum is not None:
            require(
                isinstance(parts, int) and not isinstance(parts, bool) and parts > 0,
                f"{where}: scoring parts/total must be a positive integer",
            )
            require(
                isinstance(minimum, int)
                and not isinstance(minimum, bool)
                and 1 <= minimum <= parts,
                f"{where}: scoring minimumCorrect must satisfy 1 <= minimum <= parts",
            )
            multipart_completion = fmt == "completar" and isinstance(answer.get("parts"), list)
            if fmt != "relacionar" and not multipart_completion:
                require(
                    minimum == parts,
                    f"{where}: partial thresholds are only executable for relacionar or multipart completar",
                )
            required_parts = scoring.get("requiredParts")
            if required_parts is not None:
                require(multipart_completion, f"{where}: requiredParts needs multipart completar")
                require(
                    isinstance(required_parts, list)
                    and bool(required_parts)
                    and all(isinstance(index, int) and not isinstance(index, bool) for index in required_parts)
                    and len(required_parts) == len(set(required_parts))
                    and all(0 <= index < parts for index in required_parts),
                    f"{where}: requiredParts contains invalid indexes",
                )
                require(
                    len(required_parts) <= minimum,
                    f"{where}: requiredParts makes minimumCorrect stricter than declared",
                )
    if fmt in {"elegir", "escuchar"}:
        validate_choices(item, where)
        if fmt == "escuchar":
            require_string(item["origin"].get("audio"), f"{where}: listening needs origin.audio")
            require(item["origin"].get("audioMode") == "tts", f"{where}: listening audioMode must be tts")
            require(item["origin"].get("languageCode") == "en", f"{where}: listening languageCode must be en")
            require(item["origin"].get("speedOptions") == [0.75, 1.0], f"{where}: listening speed options missing")
            require(item["origin"].get("maxReplays") == 3, f"{where}: listening replay policy missing")
            require(item["origin"].get("revealTranscriptAfterAttempt") is True, f"{where}: listening transcript policy missing")
            # Si un productor incluye también aliases de un contrato anterior,
            # no pueden contradecir los campos canónicos que consumirá la app.
            if "audioSource" in item["origin"]:
                require(item["origin"]["audioSource"] == item["origin"]["audioMode"], f"{where}: conflicting audio source metadata")
            if "audioText" in item["origin"]:
                require(item["origin"]["audioText"] == item["origin"]["audio"], f"{where}: conflicting audio text metadata")
            controls = item["origin"].get("audioControls")
            if controls is not None:
                require(isinstance(controls, dict), f"{where}: audioControls must be an object")
                if "replayLimit" in controls:
                    require(controls["replayLimit"] == item["origin"]["maxReplays"], f"{where}: conflicting replay policies")
                if "showTranscript" in controls:
                    require(controls["showTranscript"] is False, f"{where}: transcript must stay hidden before attempt")
        else:
            require("audio" not in item["origin"], f"{where}: elegir must not masquerade as listening")
    elif fmt == "ordenar":
        text = require_string(answer.get("text"), f"{where}: ordenar needs answer.text")
        tokens = answer.get("tokens")
        require(isinstance(tokens, list) and len(tokens) >= 2 and all(isinstance(x, str) and x for x in tokens), f"{where}: ordenar needs tokens")
        require(sorted(words(" ".join(tokens))) == sorted(words(text)), f"{where}: tokens do not form answer.text")
    elif fmt in {"completar", "escribir"}:
        text = require_string(answer.get("text"), f"{where}: {fmt} needs answer.text")
        accepted = answer.get("accepted")
        require(isinstance(accepted, list) and text in accepted and all(isinstance(x, str) and x for x in accepted), f"{where}: accepted answers missing")
        if fmt == "completar":
            sentences = item["origin"].get("sentences")
            parts = answer.get("parts")
            if sentences is not None or parts is not None:
                require(isinstance(sentences, list) and len(sentences) >= 2, f"{where}: multipart completar needs origin.sentences")
                require(all(isinstance(sentence, str) and sentence.strip() and "___" in sentence for sentence in sentences), f"{where}: multipart sentences need visible blanks")
                require(isinstance(parts, list) and len(parts) == len(sentences), f"{where}: multipart answer.parts count mismatch")
                for number, part in enumerate(parts, 1):
                    require(isinstance(part, dict), f"{where}: multipart part {number} must be an object")
                    part_text = require_string(part.get("text"), f"{where}: multipart part {number} text missing")
                    part_accepted = part.get("accepted")
                    require(isinstance(part_accepted, list) and part_text in part_accepted and all(isinstance(value, str) and value for value in part_accepted), f"{where}: multipart part {number} accepted answers missing")
                    if "|" in part_text:
                        require(
                            any("|" not in value for value in part_accepted),
                            f"{where}: multipart part {number} requires an unprompted pipe separator",
                        )
                require(isinstance(scoring, dict), f"{where}: multipart completar needs scoring")
                scored_parts = scoring.get("parts", scoring.get("total"))
                require(scored_parts == len(parts), f"{where}: scoring parts/total must match multipart count")
            else:
                visible = item["origin"].get("text") or item["prompt"].get("es") or ""
                require(
                    visible.count("___") <= 1,
                    f"{where}: completar UI supports at most one visible blank",
                )
        if fmt == "escribir":
            require_string(item["origin"].get("text"), f"{where}: escribir needs origin.text stimulus")
            evidence_groups = scoring.get("evidenceGroups") if isinstance(scoring, dict) else None
            if evidence_groups is not None:
                word_range = scoring.get("wordRange")
                require(
                    isinstance(word_range, list)
                    and len(word_range) == 2
                    and all(isinstance(value, int) and not isinstance(value, bool) for value in word_range)
                    and 1 <= word_range[0] <= word_range[1],
                    f"{where}: evidenceGroups needs a valid wordRange",
                )
                require(
                    isinstance(evidence_groups, list)
                    and len(evidence_groups) >= 3
                    and all(
                        isinstance(group, list)
                        and bool(group)
                        and all(isinstance(value, str) and value.strip() for value in group)
                        for group in evidence_groups
                    ),
                    f"{where}: evidenceGroups must contain at least three non-empty phrase groups",
                )
                models = [text, *accepted]
                for number, group in enumerate(evidence_groups, 1):
                    require(
                        any(
                            normalized(phrase) in normalized(model)
                            for phrase in group
                            for model in models
                        ),
                        f"{where}: evidence group {number} is absent from every model answer",
                    )
    elif fmt == "relacionar":
        require("audio" not in item["origin"], f"{where}: relacionar cannot render origin.audio")
        validate_pairs(item, where)
        if scoring is not None and ("parts" in scoring or "total" in scoring):
            parts = scoring.get("parts", scoring.get("total"))
            require(
                parts == len(item["answer"]["pairs"]),
                f"{where}: scoring parts/total must match pair count",
            )


def validate_item(
    item: Any,
    *,
    class_number: int,
    level: int,
    pool: str,
    number: int,
    class_concepts: set[str],
    concepts_before: set[str],
    concepts_available: set[str],
    seen_ids: set[str],
) -> None:
    where = f"en.n{level}.class-{class_number:02d}.{pool}[{number}]"
    require(isinstance(item, dict), f"{where}: item must be an object")
    item_id = require_string(item.get("id"), f"{where}: id missing")
    expected = rf"en\.n{level}\.c{class_number:02d}\.{POOL_PREFIX[pool]}\d{{2}}"
    require(re.fullmatch(expected, item_id) is not None, f"{where}: malformed id {item_id}")
    require(item_id not in seen_ids, f"duplicate item id: {item_id}")
    seen_ids.add(item_id)
    fmt = require_string(item.get("format"), f"{where}: format missing")
    require(fmt in FORMATS, f"{where}: unsupported format {fmt}")
    require(isinstance(item.get("answer"), dict), f"{where}: answer must be an object")
    require(isinstance(item.get("choices"), list), f"{where}: choices must be a list")
    teaches = set(require_string_list(item.get("teaches"), f"{where}: invalid teaches", allow_empty=True))
    requires = set(require_string_list(item.get("requires"), f"{where}: invalid requires", allow_empty=True))
    origin = item.get("origin")
    require(isinstance(origin, dict) and origin.get("kind") == "editorial", f"{where}: editorial origin missing")
    feedback = origin.get("feedback")
    require(isinstance(feedback, dict), f"{where}: feedback missing")
    require_string(feedback.get("es"), f"{where}: feedback.es missing")
    image_asset = origin.get("imageAsset")
    image_alt = origin.get("imageAlt")
    if image_asset is not None or image_alt is not None:
        image_asset = require_string(image_asset, f"{where}: imageAsset missing")
        require_string(image_alt, f"{where}: imageAlt missing")
        require(
            re.fullmatch(r"assets/img/[a-zA-Z0-9_./-]+\.(?:png|webp|jpe?g)", image_asset) is not None
            and ".." not in pathlib.PurePosixPath(image_asset).parts,
            f"{where}: invalid imageAsset path",
        )
        require((ROOT / image_asset).is_file(), f"{where}: imageAsset does not exist: {image_asset}")
    if pool == "practiceGuided":
        require(teaches and teaches <= class_concepts, f"{where}: guided teaches must introduce class concepts")
        require(requires <= concepts_before, f"{where}: guided requires concept not previously taught")
        hint = origin.get("hint")
        require(isinstance(hint, dict), f"{where}: guided hint missing")
        require_string(hint.get("es"), f"{where}: guided hint.es missing")
    else:
        require(not teaches, f"{where}: teaches forbidden outside guided practice")
        require(requires and requires <= concepts_available, f"{where}: requires undeclared/not-yet-taught concept")
        require("hint" not in origin, f"{where}: hints forbidden outside guided practice")
    validate_prompt(item, where)
    validate_format(item, where)
    validate_feedback_ordinal(item, where)
    require(item.get("contentHash") == expected_hash(item), f"{where}: bad contentHash")


def validate_agent_contract_v2(
    cls: dict[str, Any],
    quality_policy: dict[str, Any],
) -> None:
    """Puertas editoriales adicionales para clases producidas con agentes v2.

    El contrato es opt-in para no invalidar retrospectivamente contenido ya
    aprobado. Todo contenido nuevo debe declarar el contrato y sus límites de
    forma explícita para que el validador no dependa del prompt del agente.
    """

    class_id = cls["id"]
    require(quality_policy.get("minChoices") == 3, f"{class_id}: v2 minChoices must be 3")
    require(
        quality_policy.get("maxPromptCharacters") == 90,
        f"{class_id}: v2 maxPromptCharacters must be 90",
    )
    require(
        quality_policy.get("feedbackReuseWithinClass") == "forbid",
        f"{class_id}: v2 feedback reuse policy missing",
    )
    require(
        quality_policy.get("minClassFormats") == 4,
        f"{class_id}: v2 minClassFormats must be 4",
    )

    accessibility = cls.get("accessibility")
    require(isinstance(accessibility, dict), f"{class_id}: v2 accessibility missing")
    for key in ("highContrast", "largeText", "screenReader", "audioReplay"):
        require(accessibility.get(key) is True, f"{class_id}: v2 accessibility.{key} must be true")

    recovery = cls.get("recovery")
    require(isinstance(recovery, dict), f"{class_id}: v2 recovery missing")
    require(recovery.get("retryPool") == "review", f"{class_id}: v2 recovery must use review")
    require(recovery.get("maxAttempts") == 2, f"{class_id}: v2 recovery maxAttempts must be 2")
    require(recovery.get("allowAudioReplay") is True, f"{class_id}: v2 recovery audio replay missing")
    require(recovery.get("preserveProgress") is True, f"{class_id}: v2 recovery must preserve progress")

    pools = cls["pools"]
    formats: set[str] = set()
    reserved_formats: set[str] = set()
    feedback_seen: dict[str, str] = {}
    answer_indexes: list[int] = []
    for pool, items in pools.items():
        for item in items:
            item_id = item["id"]
            formats.add(item["format"])
            if pool in {"evaluation", "review"}:
                reserved_formats.add(item["format"])
            require(
                len(item["prompt"]["es"]) <= 90,
                f"{item_id}: v2 prompt exceeds 90 characters",
            )
            require(
                DEICTIC_PROMPT_RE.search(item["prompt"]["es"]) is None,
                f"{item_id}: v2 prompt uses an unresolved deictic reference",
            )
            if item["format"] in {"elegir", "escuchar"}:
                require(len(item["choices"]) >= 3, f"{item_id}: v2 selection needs >=3 choices")
                answer_indexes.append(item["answer"]["index"])
            feedback = normalized(item["origin"]["feedback"]["es"])
            require(
                feedback not in feedback_seen,
                f"{item_id}: v2 feedback duplicates {feedback_seen.get(feedback)}",
            )
            feedback_seen[feedback] = item_id
    require(len(formats) >= 4, f"{class_id}: v2 class needs >=4 formats")
    if answer_indexes:
        counts = {index: answer_indexes.count(index) for index in set(answer_indexes)}
        require(len(counts) >= 2, f"{class_id}: v2 correct-choice position is constant")
        require(
            max(counts.values()) / len(answer_indexes) <= 0.60,
            f"{class_id}: v2 correct-choice position exceeds 60%",
        )

    phase = require_string(cls.get("phase"), f"{class_id}: v2 phase missing")
    require(
        phase in {"input", "form", "comprehension", "production", "transfer"},
        f"{class_id}: v2 invalid phase",
    )
    skills = set(cls["skills"])
    if "escucha" in skills:
        require("escuchar" in reserved_formats, f"{class_id}: v2 escucha skill lacks reserved evidence")
    if "escritura" in skills:
        require("escribir" in formats, f"{class_id}: v2 escritura skill lacks writing evidence")
    if phase in {"production", "transfer"}:
        reserved_writing = [
            item
            for pool in ("evaluation", "review")
            for item in pools[pool]
            if item["format"] == "escribir"
        ]
        require(reserved_writing, f"{class_id}: v2 {phase} lacks reserved writing evidence")
        require(
            any(
                len(words(item["answer"]["text"])) >= 8
                and len(item["answer"].get("accepted", [])) >= 2
                and len({normalized(value) for value in item["answer"]["accepted"]}) >= 2
                for item in reserved_writing
            ),
            f"{class_id}: v2 {phase} lacks extended writing with accepted variation",
        )

    uses_vocabulary = {
        value.casefold()
        for value in require_string_list(
            cls.get("usesVocabulary"),
            f"{class_id}: v2 usesVocabulary missing",
        )
    }
    declared_vocabulary = {entry["en"].casefold() for entry in cls["vocabulary"]}
    require(
        declared_vocabulary <= uses_vocabulary,
        f"{class_id}: v2 usesVocabulary does not cover declared vocabulary",
    )
    observable_content = normalized(
        {
            "teaching": cls["teaching"],
            "pools": cls["pools"],
        }
    )
    for entry in cls["vocabulary"]:
        require(
            normalized(entry["en"]) in observable_content,
            f"{class_id}: v2 vocabulary lacks observable use {entry['en']}",
        )
    uses_patterns = set(
        require_string_list(cls.get("usesPatterns"), f"{class_id}: v2 usesPatterns missing")
    )
    require(
        set(cls["concepts"]) <= uses_patterns,
        f"{class_id}: v2 usesPatterns does not cover class concepts",
    )
    teaching_patterns = {
        lesson["patternId"]
        for lesson in cls["teaching"]
        if isinstance(lesson.get("patternId"), str)
    }
    guided_teaches = {
        concept
        for item in pools["practiceGuided"]
        for concept in item["teaches"]
    }
    evaluation_requires = {
        concept
        for item in pools["evaluation"]
        for concept in item["requires"]
    }
    for concept in cls["concepts"]:
        require(concept in teaching_patterns, f"{class_id}: v2 concept lacks teaching pattern {concept}")
        require(concept in guided_teaches, f"{class_id}: v2 concept lacks guided teaching {concept}")
        require(concept in evaluation_requires, f"{class_id}: v2 concept lacks evaluation evidence {concept}")


def validate_teaching(cls: dict[str, Any], class_number: int, level: int, vocab_en: set[str]) -> set[str]:
    teaching = cls.get("teaching")
    require(isinstance(teaching, list) and 4 <= len(teaching) <= 6, f"{cls['id']}: teaching must contain 4-6 entries")
    ids: set[str] = set()
    patterns: set[str] = set()
    for number, lesson in enumerate(teaching, 1):
        where = f"{cls['id']}.teaching[{number}]"
        require(isinstance(lesson, dict), f"{where}: must be an object")
        lesson_id = require_string(lesson.get("id"), f"{where}: id missing")
        require(re.fullmatch(rf"en\.n{level}\.class-{class_number:02d}\.t\d{{2}}", lesson_id) is not None, f"{where}: malformed id")
        require(lesson_id not in ids, f"{where}: duplicate teaching id")
        ids.add(lesson_id)
        english = require_string(lesson.get("en"), f"{where}: en missing")
        require_string(lesson.get("es"), f"{where}: es missing")
        require_string(lesson.get("explanationEs"), f"{where}: explanationEs missing")
        segments = lesson.get("segments")
        require(isinstance(segments, list) and len(segments) >= 2, f"{where}: segments missing")
        segment_texts: list[str] = []
        for segment in segments:
            if isinstance(segment, str):
                segment_texts.append(require_string(segment, f"{where}: empty segment"))
            else:
                require(isinstance(segment, dict), f"{where}: segment must be text or bilingual object")
                segment_texts.append(require_string(segment.get("en"), f"{where}: segment.en missing"))
                require_string(segment.get("es"), f"{where}: segment.es missing")
        require(
            set(words(english)) <= set(words(" ".join(segment_texts))),
            f"{where}: segments do not cover en",
        )
        require(lesson.get("audioText") == english, f"{where}: audioText must equal en")
        require(lesson.get("audioMode") == "tts" and lesson.get("languageCode") == "en", f"{where}: English TTS metadata missing")
        require(any(token in words(english) for token in vocab_en), f"{where}: not aligned to vocabulary")
        if "patternId" in lesson:
            patterns.add(require_string(lesson["patternId"], f"{where}: invalid patternId"))
    return patterns


def validate_bundle(data: Any, *, start: int, end: int, level: int = 1) -> dict[str, int]:
    require(1 <= start <= end <= 100, "range must satisfy 1 <= start <= end <= 100")
    require(1 <= level <= 10, "level must satisfy 1 <= level <= 10")
    metadata, classes = normalize_document(data)
    single_document = metadata.get("schema") == SCHEMA_CLASS
    require(metadata.get("course") == "en" and metadata.get("level") == level, "wrong course/level")
    require(metadata.get("scale") == SCALE, "wrong client scale")
    require(metadata.get("status") == "shadow", "document must remain shadow")
    require(metadata.get("runtimeAi") is False, "runtimeAi must be false")
    require(metadata.get("selectionPolicy", {}).get("deterministic") is True, "deterministic selection policy missing")
    require(metadata.get("evidencePolicy", {}).get("attemptRecords") == ["variantId", "libraryVersion", "selectionId"], "attempt evidence policy missing")
    validate_no_ai(data)

    require(isinstance(classes, list) and len(classes) == end - start + 1, f"expected {end - start + 1} classes")
    seen_ids: set[str] = set()
    concepts_before: set[str] = set()
    concepts_by_number: dict[int, set[str]] = {}
    objective_signatures: dict[str, str] = {}
    v2_semantics: dict[str, str] = {}
    v2_prompts: dict[str, str] = {}
    v2_feedback: dict[str, str] = {}
    item_count = 0

    for offset, cls in enumerate(classes):
        # La frontera antifuga es por clase. Entre clases sí debe permitirse
        # reciclar vocabulario y patrones ya enseñados para práctica espaciada.
        early_semantics: dict[str, str] = {}
        reserved_semantics: dict[str, str] = {}
        early_pairs: dict[str, str] = {}
        reserved_pairs: dict[str, str] = {}
        class_number = start + offset
        class_id = f"en.n{level}.class-{class_number:02d}"
        require(isinstance(cls, dict), f"class {class_number}: must be an object")
        require(cls.get("id") == class_id, f"class {class_number}: malformed/out-of-order id")
        expected_prereq = (
            ([] if level == 1 else [f"en.n{level - 1}.class-100"])
            if class_number == 1
            else [f"en.n{level}.class-{class_number - 1:02d}"]
        )
        require(cls.get("prerequisites") == expected_prereq, f"{class_id}: prerequisites mismatch")
        title = cls.get("title")
        require(isinstance(title, dict), f"{class_id}: title missing")
        require_string(title.get("en"), f"{class_id}: title.en missing")
        require_string(title.get("es"), f"{class_id}: title.es missing")
        objectives = cls.get("objectives")
        require(isinstance(objectives, dict), f"{class_id}: objectives missing")
        require_string_list(objectives.get("es"), f"{class_id}: objectives.es missing")
        class_concepts = set(require_string_list(cls.get("concepts"), f"{class_id}: concepts missing"))
        concepts_by_number[class_number] = class_concepts
        require_string_list(cls.get("skills"), f"{class_id}: skills missing")

        vocabulary = cls.get("vocabulary")
        require(isinstance(vocabulary, list) and 6 <= len(vocabulary) <= 12, f"{class_id}: vocabulary must contain 6-12 entries")
        vocab_en: set[str] = set()
        for number, entry in enumerate(vocabulary, 1):
            require(isinstance(entry, dict), f"{class_id}: vocabulary {number} must be an object")
            en = require_string(entry.get("en"), f"{class_id}: vocabulary {number}.en missing")
            es = require_string(entry.get("es"), f"{class_id}: vocabulary {number}.es missing")
            require(en.casefold() not in vocab_en, f"{class_id}: duplicate vocabulary {en}")
            require(en.casefold() != es.casefold(), f"{class_id}: untranslated vocabulary {en}")
            vocab_en.add(en.casefold())
        validate_teaching(cls, class_number, level, vocab_en)
        declared_external: set[str] = set()
        if single_document and class_number % 5 == 0:
            # La clase incremental no trae las cuatro clases anteriores. Los
            # conceptos externos del cierre deben declararse y demostrarse en
            # su propia evaluación acumulativa.
            declared_external = set(
                require_string_list(
                    cls.get("cumulativeEvaluation"),
                    f"{class_id}: cumulativeEvaluation required at block close",
                )
            )
            # Un ítem acumulativo puede combinar el concepto declarado con
            # otro concepto anterior (p. ej. pronombre + forma de be). El
            # bundle longitudinal prueba su origen; en la clase aislada solo
            # podemos exigir que esté declarado como requisito de evaluación.
            evaluation_items = cls.get("pools", {}).get("evaluation", [])
            if isinstance(evaluation_items, list):
                declared_external.update(
                    concept
                    for item in evaluation_items
                    if isinstance(item, dict) and isinstance(item.get("requires"), list)
                    for concept in item["requires"]
                    if isinstance(concept, str) and concept
                )
        effective_before = concepts_before | declared_external
        concepts_available = effective_before | class_concepts

        pools = cls.get("pools")
        require(isinstance(pools, dict) and set(pools) == set(POOLS), f"{class_id}: pools mismatch")
        quality_policy = cls.get("qualityPolicy", {})
        require(isinstance(quality_policy, dict), f"{class_id}: qualityPolicy must be an object")
        agent_contract = quality_policy.get("agentContract")
        if agent_contract is not None:
            require(agent_contract == AGENT_CONTRACT_V2, f"{class_id}: unsupported agent contract")
        forbid_answer_reuse = quality_policy.get("answerReuseAcrossEarlyReserved") == "forbid"
        if "answerReuseAcrossEarlyReserved" in quality_policy:
            require(forbid_answer_reuse, f"{class_id}: unsupported answerReuseAcrossEarlyReserved policy")
        class_early_answers: dict[str, str] = {}
        class_reserved_answers: dict[str, str] = {}
        forbid_atomic_answer_evidence = quality_policy.get("answerEvidenceReuseAcrossPools") == "forbid"
        if "answerEvidenceReuseAcrossPools" in quality_policy:
            require(forbid_atomic_answer_evidence, f"{class_id}: unsupported answerEvidenceReuseAcrossPools policy")
        class_early_evidence: dict[str, str] = {}
        class_reserved_evidence: dict[str, str] = {}
        for pool in POOLS:
            items = pools[pool]
            require(isinstance(items, list) and len(items) >= MINIMUMS[pool], f"{class_id}: {pool} needs >= {MINIMUMS[pool]} items")
            for number, item in enumerate(items, 1):
                validate_item(
                    item,
                    class_number=class_number,
                    level=level,
                    pool=pool,
                    number=number,
                    class_concepts=class_concepts,
                    concepts_before=effective_before,
                    concepts_available=concepts_available,
                    seen_ids=seen_ids,
                )
                item_count += 1
                signature = semantic_signature(item)
                if agent_contract == AGENT_CONTRACT_V2:
                    require(
                        signature not in v2_semantics,
                        f"{item['id']}: v2 semantic duplicate of {v2_semantics.get(signature)}",
                    )
                    v2_semantics[signature] = item["id"]
                    prompt_signature = normalized(item["prompt"]["es"])
                    require(
                        prompt_signature not in v2_prompts,
                        f"{item['id']}: v2 prompt duplicates {v2_prompts.get(prompt_signature)}",
                    )
                    v2_prompts[prompt_signature] = item["id"]
                    feedback_signature = normalized(item["origin"]["feedback"]["es"])
                    require(
                        feedback_signature not in v2_feedback,
                        f"{item['id']}: v2 feedback duplicates bundle item {v2_feedback.get(feedback_signature)}",
                    )
                    v2_feedback[feedback_signature] = item["id"]
                answer_signature = reusable_answer_signature(item)
                pair_signatures = atomic_pair_signatures(item)
                if forbid_atomic_answer_evidence:
                    register_answer_evidence(item, pool, class_early_evidence, class_reserved_evidence)
                if pool in {"practiceGuided", "practice"}:
                    require(signature not in reserved_semantics, f"{item['id']}: semantic duplicate of reserved {reserved_semantics.get(signature)}")
                    for pair_signature in pair_signatures:
                        require(pair_signature not in reserved_pairs, f"{item['id']}: atomic pair duplicate of reserved {reserved_pairs.get(pair_signature)}")
                        early_pairs.setdefault(pair_signature, item["id"])
                    early_semantics.setdefault(signature, item["id"])
                    if forbid_answer_reuse and answer_signature is not None:
                        require(
                            answer_signature not in class_reserved_answers,
                            f"{item['id']}: answer semantic duplicate of reserved {class_reserved_answers.get(answer_signature)}",
                        )
                        class_early_answers.setdefault(answer_signature, item["id"])
                else:
                    require(signature not in early_semantics, f"{item['id']}: semantic duplicate of practice {early_semantics.get(signature)}")
                    for pair_signature in pair_signatures:
                        require(pair_signature not in early_pairs, f"{item['id']}: atomic pair duplicate of practice {early_pairs.get(pair_signature)}")
                        reserved_pairs.setdefault(pair_signature, item["id"])
                    if forbid_answer_reuse and answer_signature is not None:
                        require(
                            answer_signature not in class_early_answers,
                            f"{item['id']}: answer semantic duplicate of practice {class_early_answers.get(answer_signature)}",
                        )
                        class_reserved_answers.setdefault(answer_signature, item["id"])
                    # Evaluation and review form the same reserved side of the
                    # anti-leak boundary. Cumulative evaluation may reuse an
                    # earlier reserved stimulus; neither may reuse guided or
                    # independent practice.
                    reserved_semantics.setdefault(signature, item["id"])

        evaluation = pools["evaluation"]
        require(len({item["format"] for item in evaluation}) >= 2, f"{class_id}: evaluation needs >=2 formats")
        remediation = cls.get("remediationMap")
        require(isinstance(remediation, dict), f"{class_id}: remediationMap missing")
        require(set(remediation) == {item["id"] for item in evaluation}, f"{class_id}: remediationMap coverage mismatch")
        teaching_ids = {lesson["id"] for lesson in cls["teaching"]}
        review_ids = {item["id"] for item in pools["review"]}
        for evaluation_id, target in remediation.items():
            require(isinstance(target, dict), f"{evaluation_id}: remediation target must be an object")
            require(target.get("reteach") in teaching_ids, f"{evaluation_id}: invalid reteach target")
            require(target.get("review") in review_ids, f"{evaluation_id}: invalid review target")

        cumulative = cls.get("cumulativeEvaluation")
        if class_number % 5 == 0:
            cumulative_set = set(require_string_list(cumulative, f"{class_id}: cumulativeEvaluation required at block close"))
            evaluation_requires = {concept for item in evaluation for concept in item["requires"]}
            require(cumulative_set <= evaluation_requires, f"{class_id}: cumulativeEvaluation lacks real evaluation evidence")
            if single_document:
                require(len(cumulative_set) >= 4, f"{class_id}: standalone block close needs >=4 cumulative concepts")
            else:
                require(
                    cumulative_set <= concepts_before | class_concepts,
                    f"{class_id}: cumulativeEvaluation must reference taught/current concepts",
                )
                block_start = class_number - 4
                for prior in range(block_start, class_number):
                    if prior in concepts_by_number:
                        require(bool(cumulative_set & concepts_by_number[prior]), f"{class_id}: cumulativeEvaluation misses class {prior}")
                if quality_policy:
                    require(bool(cumulative_set & class_concepts), f"{class_id}: cumulativeEvaluation misses current class")
        else:
            require(cumulative in (None, []), f"{class_id}: cumulativeEvaluation only belongs on multiples of 5")
        if agent_contract == AGENT_CONTRACT_V2:
            validate_agent_contract_v2(cls, quality_policy)
            objective_signature = normalized(objectives["es"])
            require(
                objective_signature not in objective_signatures,
                f"{class_id}: v2 objectives duplicate {objective_signatures.get(objective_signature)}",
            )
            objective_signatures[objective_signature] = class_id
        concepts_before.update(class_concepts)

    return {"classes": len(classes), "items": item_count, "start": start, "end": end, "level": level}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=pathlib.Path, required=True, help="Bundle JSON to validate")
    parser.add_argument("--start", type=int, required=True, help="First class number in the file")
    parser.add_argument("--end", type=int, required=True, help="Last class number in the file")
    parser.add_argument("--level", type=int, default=1, help="Client curriculum level (1-10)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        data = json.loads(args.file.read_text(encoding="utf-8"))
        result = validate_bundle(data, start=args.start, end=args.end, level=args.level)
    except (OSError, json.JSONDecodeError, ValidationError, KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(
        f"OK: N{result['level']} classes {result['start']}-{result['end']}; "
        f"{result['classes']} classes; {result['items']} exercises; shadow/no-AI"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
