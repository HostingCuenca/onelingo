"""Valida el piloto editorial inglés N1 sin tocar la ruta legacy.

El piloto es editorial y permanece en ``shadow``. Este validador comprueba
estructura, semántica mínima de cada formato, anti-duplicación y hashes de
contenido independientes de los identificadores estables.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys
from typing import Any


FILE = pathlib.Path(__file__).parents[2] / "assets/contenido/en/editorial/n1/pilot-classes-01-05.json"
SCALE_FILE = pathlib.Path(__file__).parents[2] / "assets/contenido/en/plan-editorial/escala-cliente.json"
POOLS = ("practiceGuided", "practice", "evaluation", "review")
FORMATS = {"elegir", "escuchar", "ordenar", "completar", "escribir", "relacionar"}
POOL_PREFIX = {"practiceGuided": "pg", "practice": "p", "evaluation": "e", "review": "r"}
MINIMUMS = {"practiceGuided": 3, "practice": 3, "evaluation": 4, "review": 3}
WORD_RE = re.compile(r"[a-záéíóúüñ0-9]+(?:'[a-záéíóúüñ0-9]+)?", re.I)


class ValidationError(AssertionError):
    pass


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_without_identity(item: dict[str, Any]) -> dict[str, Any]:
    """The hash covers content, never the mutable identity or its own hash."""
    return {key: value for key, value in item.items() if key not in {"id", "contentHash"}}


def semantic_content(item: dict[str, Any]) -> dict[str, Any]:
    """Content used for duplicate detection, independent of pool metadata."""
    value = {
        key: part
        for key, part in item.items()
        if key not in {"id", "contentHash", "teaches", "requires"}
    }
    if isinstance(value.get("origin"), dict):
        value["origin"] = {
            key: part for key, part in value["origin"].items() if key != "kind"
        }
    return value


def words(value: str) -> list[str]:
    return [part.lower() for part in WORD_RE.findall(value)]


def normalized(value: Any) -> str:
    return " ".join(words(canonical(value)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def require_string(value: Any, message: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), message)
    return value


def contains_bare_yes(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() == "yes"
    if isinstance(value, dict):
        return any(contains_bare_yes(v) for v in value.values())
    if isinstance(value, list):
        return any(contains_bare_yes(v) for v in value)
    return False


def validate_prompt(item: dict[str, Any], where: str) -> None:
    prompt = item.get("prompt")
    require(isinstance(prompt, dict), f"{where}: prompt must be an object")
    require_string(prompt.get("es"), f"{where}: prompt.es missing")
    require(len(prompt["es"].strip()) >= 12, f"{where}: prompt.es too short")


def validate_choices(item: dict[str, Any], where: str, index: int) -> None:
    choices = item.get("choices")
    require(isinstance(choices, list) and len(choices) >= 2, f"{where}: choices required")
    texts = []
    for choice_number, choice in enumerate(choices, 1):
        require(isinstance(choice, dict), f"{where}: choice {choice_number} must be an object")
        text = require_string(choice.get("text"), f"{where}: choice {choice_number} missing text")
        texts.append(text.casefold())
    require(len(set(texts)) == len(texts), f"{where}: duplicate choices")
    require(isinstance(index, int) and not isinstance(index, bool), f"{where}: answer.index must be int")
    require(0 <= index < len(choices), f"{where}: answer.index out of range")


def validate_pairs(item: dict[str, Any], where: str) -> None:
    origin = item["origin"]
    pairs = origin.get("pairs")
    answer_pairs = item["answer"].get("pairs")
    require(isinstance(pairs, list) and len(pairs) >= 2, f"{where}: pairs required")
    require(answer_pairs == pairs, f"{where}: answer.pairs must match origin.pairs")
    lefts = set()
    rights = set()
    for number, pair in enumerate(pairs, 1):
        require(isinstance(pair, list) and len(pair) == 2, f"{where}: invalid pair {number}")
        left = require_string(pair[0], f"{where}: pair {number} left missing").casefold()
        right = pair[1]
        if isinstance(right, dict):
            right = right.get("es")
        right = require_string(right, f"{where}: pair {number} right missing").casefold()
        require(left not in lefts and right not in rights, f"{where}: duplicate pair side")
        lefts.add(left)
        rights.add(right)


def validate_item(item: dict[str, Any], cls: dict[str, Any], pool: str, number: int, seen_ids: set[str], seen_content: dict[str, str]) -> None:
    class_number = int(cls["id"].rsplit("-", 1)[1])
    where = f"{cls['id']}.{pool}[{number}]"
    require(isinstance(item, dict), f"{where}: item must be an object")
    item_id = require_string(item.get("id"), f"{where}: id missing")
    expected_id = rf"en\.n1\.c{class_number:02d}\.{POOL_PREFIX[pool]}\d{{2}}"
    require(re.fullmatch(expected_id, item_id) is not None, f"{where}: unstable/malformed id {item_id}")
    require(item_id not in seen_ids, f"duplicate item id: {item_id}")
    seen_ids.add(item_id)
    fmt = require_string(item.get("format"), f"{where}: format missing")
    require(fmt in FORMATS, f"{where}: unsupported format {fmt}")
    validate_prompt(item, where)
    require(isinstance(item.get("answer"), dict), f"{where}: answer must be an object")
    require(isinstance(item.get("choices"), list), f"{where}: choices must be a list")
    require(isinstance(item.get("teaches"), list) and all(isinstance(x, str) and x for x in item["teaches"]), f"{where}: invalid teaches")
    require(isinstance(item.get("requires"), list) and all(isinstance(x, str) and x for x in item["requires"]), f"{where}: invalid requires")
    require(isinstance(item.get("origin"), dict) and item["origin"].get("kind") == "editorial", f"{where}: editorial origin missing")
    feedback = item["origin"].get("feedback")
    require(isinstance(feedback, dict), f"{where}: feedback missing")
    require_string(feedback.get("es"), f"{where}: feedback.es missing")
    if pool == "practiceGuided":
        hint = item["origin"].get("hint")
        require(isinstance(hint, dict), f"{where}: guided hint missing")
        require_string(hint.get("es"), f"{where}: guided hint.es missing")
    else:
        require("hint" not in item["origin"], f"{where}: hints forbidden outside guided practice")
    require(not contains_bare_yes(item), f"{where}: bare answer yes is not a valid exercise response")

    answer = item["answer"]
    if fmt in {"elegir", "escuchar"}:
        validate_choices(item, where, answer.get("index"))
        if fmt == "escuchar":
            require_string(item["origin"].get("audio"), f"{where}: listening item needs origin.audio")
            require(item["origin"].get("audioMode") == "tts", f"{where}: listening audioMode must be tts")
            require(item["origin"].get("languageCode") == "en", f"{where}: listening languageCode must be en")
            require(item["origin"].get("speedOptions") == [0.75, 1.0], f"{where}: listening speed options missing")
            require(item["origin"].get("maxReplays") == 3, f"{where}: listening replay policy missing")
            require(item["origin"].get("revealTranscriptAfterAttempt") is True, f"{where}: listening transcript policy missing")
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
        require(isinstance(accepted, list) and text in accepted and all(isinstance(x, str) and x for x in accepted), f"{where}: accessible accepted answers missing")
        if fmt == "escribir":
            require(isinstance(item["origin"].get("text"), str), f"{where}: escribir needs origin.text stimulus")
    elif fmt == "relacionar":
        validate_pairs(item, where)

    fingerprint = canonical(content_without_identity(item))
    require(item.get("contentHash") == "sha256:" + hashlib.sha256(fingerprint.encode()).hexdigest(), f"{where}: bad contentHash")
    loose = normalized(semantic_content(item))
    require(loose not in seen_content, f"near/exact duplicate with {seen_content.get(loose)}: {item_id}")
    seen_content[loose] = item_id


def main() -> None:
    data = json.loads(FILE.read_text(encoding="utf-8"))
    scale = json.loads(SCALE_FILE.read_text(encoding="utf-8"))
    require(data.get("schema") == "onelingo.editorial.class-bundle.v1", "wrong schema")
    require(data.get("course") == "en" and data.get("level") == 1, "wrong course/level")
    require(data.get("scale") == scale.get("id") and data.get("status") == "shadow", "pilot must use the client scale and remain shadow")
    require(data.get("runtimeAi") is False, "runtimeAi must be false")
    require(data.get("selectionPolicy", {}).get("deterministic") is True, "deterministic selection policy missing")
    require(data.get("evidencePolicy", {}).get("attemptRecords") == ["variantId", "libraryVersion", "selectionId"], "attempt evidence policy missing")
    classes = data.get("classes")
    require(isinstance(classes, list) and len(classes) == 5, "exactly 5 classes required")
    ids = set()
    seen_content: dict[str, str] = {}
    known_concepts: set[str] = set()
    for class_number, cls in enumerate(classes, 1):
        require(isinstance(cls, dict), f"class {class_number} must be an object")
        require(cls.get("id") == f"en.n1.class-{class_number:02d}", f"class {class_number}: unstable id/order")
        expected_prerequisites = [] if class_number == 1 else [f"en.n1.class-{class_number - 1:02d}"]
        require(cls.get("prerequisites") == expected_prerequisites, f"{cls.get('id')}: class prerequisites mismatch")
        require(isinstance(cls.get("concepts"), list) and cls["concepts"], f"{cls.get('id')}: concepts missing")
        known_concepts.update(cls["concepts"])
        require(cls.get("skills") == ["lectura", "escucha", "escritura-controlada"], f"{cls.get('id')}: skills mismatch")
        accessibility = cls.get("accessibility", {})
        require(accessibility.get("audioSpeedOptions") == [0.75, 1.0], f"{cls.get('id')}: accessibility audio speeds missing")
        require(accessibility.get("acceptCaseAndTerminalPunctuationVariants") is True, f"{cls.get('id')}: answer accessibility missing")
        require(accessibility.get("lowLoadMode") == "one_item_at_a_time", f"{cls.get('id')}: low-load mode missing")
        require(accessibility.get("orderAndWriteSegmentation") is True, f"{cls.get('id')}: segmentation support missing")
        require(cls.get("recovery", {}).get("afterTwoErrors") == "reteach_then_guided_variant", f"{cls.get('id')}: recovery policy missing")
        require_string(cls.get("title", {}).get("en") if isinstance(cls.get("title"), dict) else None, f"{cls.get('id')}: title.en missing")
        require_string(cls.get("title", {}).get("es") if isinstance(cls.get("title"), dict) else None, f"{cls.get('id')}: title.es missing")
        vocabulary = cls.get("vocabulary")
        require(isinstance(vocabulary, list) and 6 <= len(vocabulary) <= 12, f"{cls['id']}: vocabulary must contain 6-12 words")
        vocab_en = set()
        for entry in vocabulary:
            require(isinstance(entry, dict), f"{cls['id']}: vocabulary entry must be object")
            en = require_string(entry.get("en"), f"{cls['id']}: vocabulary.en missing")
            es = require_string(entry.get("es"), f"{cls['id']}: vocabulary.es missing")
            require(en.casefold() not in vocab_en, f"{cls['id']}: duplicate vocabulary {en}")
            require(en.casefold() != es.casefold(), f"{cls['id']}: vocabulary must be translated")
            vocab_en.add(en.casefold())
        teaching = cls.get("teaching")
        require(isinstance(teaching, list) and 4 <= len(teaching) <= 6, f"{cls['id']}: teaching must contain 4-6 lessons")
        teaching_ids = set()
        for lesson_number, lesson in enumerate(teaching, 1):
            require(isinstance(lesson, dict), f"{cls['id']}: teaching entry must be object")
            lesson_id = require_string(lesson.get("id"), f"{cls['id']}: teaching id missing")
            require(re.fullmatch(rf"en\.n1\.class-{class_number:02d}\.t\d{{2}}", lesson_id) is not None, f"{cls['id']}: unstable teaching id")
            require(lesson_id not in teaching_ids, f"{cls['id']}: duplicate teaching id")
            teaching_ids.add(lesson_id)
            english = require_string(lesson.get("en"), f"{cls['id']}: teaching.en missing")
            require_string(lesson.get("es"), f"{cls['id']}: teaching.es missing")
            require_string(lesson.get("explanationEs"), f"{cls['id']}: teaching explanation missing")
            require(isinstance(lesson.get("segments"), list) and len(lesson["segments"]) >= 2, f"{cls['id']}: teaching segments missing")
            require(lesson.get("audioText") == english and lesson.get("audioMode") == "tts", f"{cls['id']}: teaching audio support missing")
            require(any(word in words(english) for word in vocab_en if len(words(word)) == 1), f"{cls['id']}: teaching {lesson_number} is not aligned to vocabulary")
        pools = cls.get("pools")
        require(isinstance(pools, dict) and set(pools) == set(POOLS), f"{cls['id']}: pools mismatch")
        class_eval = []
        class_review = []
        for pool in POOLS:
            require(isinstance(pools[pool], list) and len(pools[pool]) >= MINIMUMS[pool], f"{cls['id']}: {pool} needs >= {MINIMUMS[pool]} items")
            for number, exercise in enumerate(pools[pool], 1):
                validate_item(exercise, cls, pool, number, ids, seen_content)
                if pool == "evaluation":
                    class_eval.append(exercise)
                elif pool == "review":
                    class_review.append(exercise)
                require(set(exercise["requires"]).issubset(known_concepts), f"{exercise['id']}: requires undeclared concept")
        require(len({x["format"] for x in class_eval}) >= 2, f"{cls['id']}: evaluation needs >=2 formats")
        eval_signatures = {(x["format"], normalized({"prompt": x["prompt"], "answer": x["answer"], "origin": x["origin"]})) for x in class_eval}
        review_signatures = {(x["format"], normalized({"prompt": x["prompt"], "answer": x["answer"], "origin": x["origin"]})) for x in class_review}
        require(not eval_signatures & review_signatures, f"{cls['id']}: review repeats evaluation stimulus/response")
        remediation = cls.get("remediationMap")
        require(isinstance(remediation, dict), f"{cls['id']}: remediation map missing")
        require(set(remediation) == {item["id"] for item in pools["evaluation"]}, f"{cls['id']}: remediation coverage mismatch")
        teaching_ids_all = {lesson["id"] for lesson in teaching}
        review_ids = {item["id"] for item in pools["review"]}
        for evaluation_id, target in remediation.items():
            require(target.get("reteach") in teaching_ids_all, f"{evaluation_id}: invalid reteach target")
            require(target.get("review") in review_ids, f"{evaluation_id}: invalid review target")
        taught_sentences = {lesson["en"].casefold().rstrip(".") for lesson in teaching}
        for exercise in pools["practice"]:
            if exercise["format"] == "escribir":
                require(exercise["answer"]["text"].casefold().rstrip(".") in taught_sentences, f"{exercise['id']}: independent writing was not taught")
        if class_number == 5:
            require(set(cls.get("cumulativeEvaluation", [])) == {"identity-be", "pronouns-be", "classroom-objects", "family-vocabulary"}, "class 5 cumulative coverage missing")
    print(f"OK: {len(classes)} clases, {len(ids)} ejercicios, pools y formatos funcionales; shadow sin activación")


if __name__ == "__main__":
    try:
        main()
    except (ValidationError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
