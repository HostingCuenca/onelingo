#!/usr/bin/env python3
"""Valida el manifiesto cronológico N1 y declaraciones uses* de clases.

El control es declarativo: no intenta adivinar vocabulario o gramática desde
texto libre. Una clase o bundle que declare ``usesVocabulary`` y
``usesPatterns`` se comprueba contra su entrada cronológica.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "assets/contenido/en/plan-editorial/cronologia-n1-01-20.json"
CLASS_ID_RE = re.compile(r"en\.n1\.class-(\d{2,3})")


class ChronologyError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ChronologyError(message)


def string_list(value: Any, where: str) -> list[str]:
    require(isinstance(value, list), f"{where}: must be a list")
    require(all(isinstance(part, str) and part.strip() for part in value), f"{where}: invalid entry")
    normalized = [part.strip().casefold() for part in value]
    require(len(normalized) == len(set(normalized)), f"{where}: duplicates")
    return normalized


def validate_manifest(data: Any) -> dict[str, dict[str, set[str]]]:
    require(isinstance(data, dict), "manifest root must be an object")
    require(data.get("schema") == "onelingo.editorial.chronology.v1", "wrong chronology schema")
    require(data.get("course") == "en" and data.get("level") == 1, "wrong chronology course/level")
    classes = data.get("classes")
    require(isinstance(classes, list) and len(classes) >= 20, "chronology must contain contiguous classes starting at 1 (minimum 20)")
    declared_range = data.get("range")
    require(
        isinstance(declared_range, dict)
        and declared_range.get("start") == 1
        and declared_range.get("end") == len(classes),
        f"chronology range must be 1-{len(classes)}",
    )
    reserved_future = set(string_list(data.get("reservedFutureVocabulary", []), "reservedFutureVocabulary"))
    vocabulary_seen: set[str] = set()
    patterns_seen: set[str] = set()
    index: dict[str, dict[str, set[str]]] = {}
    for number, entry in enumerate(classes, 1):
        where = f"chronology class {number}"
        require(isinstance(entry, dict), f"{where}: must be an object")
        class_id = f"en.n1.class-{number:02d}"
        require(entry.get("id") == class_id, f"{where}: malformed/out-of-order id")
        introduced = set(string_list(entry.get("introducedVocabulary"), f"{class_id}.introducedVocabulary"))
        carryover = set(string_list(entry.get("allowedCarryover"), f"{class_id}.allowedCarryover"))
        new_patterns = set(string_list(entry.get("newPatterns"), f"{class_id}.newPatterns"))
        required_patterns = set(string_list(entry.get("requiresPatterns"), f"{class_id}.requiresPatterns"))
        require(not introduced & vocabulary_seen, f"{class_id}: vocabulary reintroduced: {sorted(introduced & vocabulary_seen)}")
        require(carryover <= vocabulary_seen, f"{class_id}: carryover before introduction: {sorted(carryover - vocabulary_seen)}")
        require(not new_patterns & patterns_seen, f"{class_id}: pattern reintroduced: {sorted(new_patterns & patterns_seen)}")
        require(required_patterns <= patterns_seen, f"{class_id}: pattern required before introduction: {sorted(required_patterns - patterns_seen)}")
        index[class_id] = {
            "vocabulary": introduced | carryover,
            "patterns": new_patterns | required_patterns,
            "introducedVocabulary": introduced,
            "newPatterns": new_patterns,
            "reservedFutureVocabulary": reserved_future,
        }
        vocabulary_seen.update(introduced)
        patterns_seen.update(new_patterns)
    require(reserved_future <= vocabulary_seen, f"reserved future vocabulary is never introduced: {sorted(reserved_future - vocabulary_seen)}")
    return index


def normalize_classes(data: Any) -> list[dict[str, Any]]:
    require(isinstance(data, dict), "class document root must be an object")
    schema = data.get("schema")
    if schema == "onelingo.editorial.class-bundle.v1":
        classes = data.get("classes")
        require(isinstance(classes, list), "bundle classes must be a list")
        return classes
    if schema == "onelingo.editorial.class.v1":
        return [data]
    raise ChronologyError(f"unsupported class schema: {schema!r}")


def structured_english_strings(cls: dict[str, Any]) -> list[str]:
    """Recoge solo campos estructurados que contienen inglés para el alumno."""

    result: list[str] = []

    def add(value: Any) -> None:
        if isinstance(value, str) and value.strip():
            result.append(value)

    title = cls.get("title", {})
    if isinstance(title, dict):
        add(title.get("en"))
    for entry in cls.get("vocabulary", []):
        if isinstance(entry, dict):
            add(entry.get("en"))
    for lesson in cls.get("teaching", []):
        if not isinstance(lesson, dict):
            continue
        add(lesson.get("en"))
        add(lesson.get("audioText"))
        for segment in lesson.get("segments", []):
            if isinstance(segment, dict):
                add(segment.get("en"))
            else:
                add(segment)
    pools = cls.get("pools", {})
    if isinstance(pools, dict):
        for items in pools.values():
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict):
                    continue
                answer = item.get("answer", {})
                if isinstance(answer, dict):
                    add(answer.get("text"))
                    for key in ("accepted", "tokens"):
                        for value in answer.get(key, []):
                            add(value)
                    for pair in answer.get("pairs", []):
                        if isinstance(pair, list) and pair:
                            add(pair[0])
                for choice in item.get("choices", []):
                    if isinstance(choice, dict):
                        add(choice.get("text"))
                origin = item.get("origin", {})
                if isinstance(origin, dict):
                    add(origin.get("audio"))
                    add(origin.get("audioText"))
    return result


def learner_english_strings(cls: dict[str, Any]) -> list[str]:
    """Recoge el inglés que el alumno ve u oye, sin título ni glosario.

    Esta vista permite comprobar de forma opt-in que ``usesVocabulary`` sea
    exhaustivo. No se usa para documentos legacy porque estos no fueron
    escritos con ese contrato.
    """

    result: list[str] = []

    def add(value: Any) -> None:
        if isinstance(value, str) and value.strip():
            result.append(value)

    for lesson in cls.get("teaching", []):
        if not isinstance(lesson, dict):
            continue
        add(lesson.get("en"))
        add(lesson.get("audioText"))
        for segment in lesson.get("segments", []):
            if isinstance(segment, dict):
                add(segment.get("en"))
            else:
                add(segment)
    pools = cls.get("pools", {})
    if isinstance(pools, dict):
        for items in pools.values():
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict):
                    continue
                answer = item.get("answer", {})
                if isinstance(answer, dict):
                    add(answer.get("text"))
                    for key in ("accepted", "tokens"):
                        for value in answer.get(key, []):
                            add(value)
                    for pair in answer.get("pairs", []):
                        if isinstance(pair, list) and pair:
                            add(pair[0])
                for choice in item.get("choices", []):
                    if isinstance(choice, dict):
                        add(choice.get("text"))
                origin = item.get("origin", {})
                if isinstance(origin, dict):
                    add(origin.get("audio"))
                    add(origin.get("audioText"))
    return result


def vocabulary_tokens(strings: list[str]) -> set[str]:
    """Tokeniza vocabulario inglés y normaliza el posesivo nominal ``'s``."""

    tokens: set[str] = set()
    for value in strings:
        for token in re.findall(r"[a-z]+(?:['’][a-z]+)?", value.casefold()):
            if token.endswith(("'s", "’s")):
                token = token[:-2]
            tokens.add(token)
    return tokens


def vocabulary_evidence(strings: list[str], declarations: set[str]) -> tuple[set[str], set[str], set[str]]:
    """Devuelve tokens reales, declaraciones evidenciadas y tokens cubiertos.

    Las declaraciones pueden ser frases como ``have got``. En ese caso la
    frase debe aparecer contigua y cubre sus componentes, para no obligar a
    declarar ``got`` como palabra independiente.
    """

    sequences: list[list[str]] = []
    for value in strings:
        sequence: list[str] = []
        for token in re.findall(r"[a-z]+(?:['’][a-z]+)?", value.casefold()):
            if token.endswith(("'s", "’s")):
                token = token[:-2]
            sequence.append(token)
        if sequence:
            sequences.append(sequence)
    actual = {token for sequence in sequences for token in sequence}
    matched: set[str] = set()
    covered: set[str] = set()
    for declaration in declarations:
        parts = declaration.split()
        if any(
            sequence[index : index + len(parts)] == parts
            for sequence in sequences
            for index in range(len(sequence) - len(parts) + 1)
        ):
            matched.add(declaration)
            covered.update(parts)
    return actual, matched, covered


def contains_reserved_term(text: str, term: str) -> bool:
    phrase = r"\s+".join(re.escape(part) for part in term.casefold().split())
    return re.search(rf"(?<!\w){phrase}(?!\w)", text.casefold()) is not None


def validate_declarations(
    data: Any,
    chronology: dict[str, dict[str, set[str]]],
    start: int | None = None,
    end: int | None = None,
) -> dict[str, int]:
    checked_vocabulary = 0
    checked_patterns = 0
    classes = normalize_classes(data)
    for cls in classes:
        require(isinstance(cls, dict), "class entry must be an object")
        class_id = cls.get("id")
        require(isinstance(class_id, str) and CLASS_ID_RE.fullmatch(class_id), f"invalid class id: {class_id!r}")
        require(class_id in chronology, f"{class_id}: outside chronology manifest")
        class_number = int(CLASS_ID_RE.fullmatch(class_id).group(1))
        if start is not None:
            require(class_number >= start, f"{class_id}: outside requested range {start}-{end or len(chronology)}")
        if end is not None:
            require(class_number <= end, f"{class_id}: outside requested range {start or 1}-{end}")
        scope = chronology[class_id]
        quality_policy = cls.get("qualityPolicy", {})
        require(isinstance(quality_policy, dict), f"{class_id}: qualityPolicy must be an object")
        chronology_policy = quality_policy.get("chronologyTokens")
        if chronology_policy is not None:
            require(chronology_policy == "enforce", f"{class_id}: unsupported chronologyTokens policy")
        if "usesVocabulary" in cls:
            used = set(string_list(cls["usesVocabulary"], f"{class_id}.usesVocabulary"))
            early = used - scope["vocabulary"]
            require(not early, f"{class_id}: vocabulary used before introduction/not allowed: {sorted(early)}")
            checked_vocabulary += len(used)
            if quality_policy.get("vocabularyDeclarations") is not None:
                require(
                    quality_policy["vocabularyDeclarations"] == "exhaustive",
                    f"{class_id}: unsupported vocabularyDeclarations policy",
                )
                actual, matched, covered = vocabulary_evidence(learner_english_strings(cls), used)
                require(not actual - covered, f"{class_id}: learner vocabulary not declared: {sorted(actual - covered)}")
                require(not used - matched, f"{class_id}: declared vocabulary not used: {sorted(used - matched)}")
        used_patterns: set[str] | None = None
        if "usesPatterns" in cls:
            used = set(string_list(cls["usesPatterns"], f"{class_id}.usesPatterns"))
            early = used - scope["patterns"]
            require(not early, f"{class_id}: pattern used before introduction/not allowed: {sorted(early)}")
            checked_patterns += len(used)
            used_patterns = used
        if "cumulativeEvaluation" in cls:
            cumulative = set(string_list(cls["cumulativeEvaluation"], f"{class_id}.cumulativeEvaluation"))
            require(cumulative <= scope["patterns"], f"{class_id}: cumulative pattern not allowed by chronology: {sorted(cumulative - scope['patterns'])}")
            require(
                used_patterns is not None and cumulative <= used_patterns,
                f"{class_id}: cumulative patterns missing from usesPatterns: {sorted(cumulative - (used_patterns or set()))}",
            )
        if chronology_policy == "enforce":
            future_terms: dict[str, str] = {}
            for future_id, future_scope in chronology.items():
                future_number = int(CLASS_ID_RE.fullmatch(future_id).group(1))
                if future_number > class_number:
                    for term in future_scope["introducedVocabulary"] & scope["reservedFutureVocabulary"]:
                        future_terms.setdefault(term, future_id)
            for english in structured_english_strings(cls):
                for term, introduced_in in future_terms.items():
                    require(
                        not contains_reserved_term(english, term),
                        f"{class_id}: reserved future vocabulary {term!r} appears before {introduced_in}",
                    )
    return {"classes": len(classes), "vocabulary": checked_vocabulary, "patterns": checked_patterns}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=pathlib.Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--file", type=pathlib.Path, help="Optional class or bundle declaring usesVocabulary/usesPatterns")
    parser.add_argument("--start", type=int, help="First class allowed in --file (manifest is still validated in full)")
    parser.add_argument("--end", type=int, help="Last class allowed in --file (manifest is still validated in full)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        require(args.start is None or args.start >= 1, "--start must be at least 1")
        require(args.end is None or args.end >= 1, "--end must be at least 1")
        require(args.start is None or args.end is None or args.start <= args.end, "--start cannot exceed --end")
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        chronology = validate_manifest(manifest)
        if args.file is None:
            require(args.start is None and args.end is None, "--start/--end require --file")
            print(f"OK: chronology classes 1-{len(chronology)}; {len(chronology)} entries")
            return 0
        data = json.loads(args.file.read_text(encoding="utf-8"))
        result = validate_declarations(data, chronology, start=args.start, end=args.end)
    except (OSError, json.JSONDecodeError, ChronologyError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(
        f"OK: {result['classes']} classes; "
        f"{result['vocabulary']} declared vocabulary uses; "
        f"{result['patterns']} declared pattern uses"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
