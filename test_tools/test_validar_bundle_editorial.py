from __future__ import annotations

import copy
import json
import pathlib
import unittest

from tools.contenido import validar_bundle_editorial as validator


HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
PILOT = ROOT / "assets/contenido/en/editorial/n1/pilot-classes-01-05.json"
N2_FIRST_BLOCK = ROOT / "assets/contenido/en/editorial/n2/bundle-01-05.json"
N2_PRODUCTION_CLASS = ROOT / "assets/contenido/en/editorial/n2/class-19.json"
CASES = HERE / "fixtures/editorial_bad_cases.json"


def at(root, path):
    value = root
    for part in path:
        value = value[part]
    return value


def parent_at(root, path):
    return at(root, path[:-1]), path[-1]


def refresh_hashes(data):
    for cls in data["classes"]:
        for items in cls["pools"].values():
            for item in items:
                item["contentHash"] = validator.expected_hash(item)


def mutate(base, case):
    data = copy.deepcopy(base)
    operation = case["operation"]
    if operation == "set":
        parent, key = parent_at(data, case["path"])
        parent[key] = copy.deepcopy(case["value"])
    elif operation == "delete":
        parent, key = parent_at(data, case["path"])
        del parent[key]
    elif operation == "copy_semantic":
        source = at(data, case["source"])
        target = at(data, case["path"])
        target_id = target["id"]
        target_requires = target["requires"]
        copied = copy.deepcopy(source)
        copied["id"] = target_id
        copied["requires"] = target_requires
        copied["teaches"] = []
        copied["origin"].pop("hint", None)
        parent, key = parent_at(data, case["path"])
        parent[key] = copied
    elif operation == "copy_pair":
        source = at(data, case["source"])
        target = at(data, case["path"])
        pair = copy.deepcopy(source["answer"]["pairs"][case["sourceIndex"]])
        target["answer"]["pairs"][case["targetIndex"]] = copy.deepcopy(pair)
        target["origin"]["pairs"][case["targetIndex"]] = copy.deepcopy(pair)
    elif operation == "underspecify_completion":
        target = at(data, case["path"])
        target["prompt"]["es"] = "Completa: Three ___."
        target["origin"].pop("text", None)
    else:
        raise AssertionError(f"unknown fixture operation: {operation}")
    if case.get("rehash"):
        refresh_hashes(data)
    return data


class ValidateBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot = json.loads(PILOT.read_text(encoding="utf-8"))
        cls.n2_first = json.loads(N2_FIRST_BLOCK.read_text(encoding="utf-8"))
        cls.n2_production = json.loads(N2_PRODUCTION_CLASS.read_text(encoding="utf-8"))
        cls.cases = json.loads(CASES.read_text(encoding="utf-8"))

    def v2_single_class(self):
        single = copy.deepcopy(self.n2_first["classes"][0])
        for key in ("course", "level", "scale", "status", "runtimeAi", "selectionPolicy", "evidencePolicy"):
            single[key] = copy.deepcopy(self.n2_first[key])
        single["schema"] = validator.SCHEMA_CLASS
        single["phase"] = "input"
        single["qualityPolicy"].update(
            {
                "agentContract": validator.AGENT_CONTRACT_V2,
                "minChoices": 3,
                "maxPromptCharacters": 90,
                "feedbackReuseWithinClass": "forbid",
                "minClassFormats": 4,
            }
        )
        selection_number = 0
        for items in single["pools"].values():
            for item in items:
                item["prompt"]["es"] = (
                    f"Completa el horario ___ en {item['id']}."
                    if item["format"] == "completar"
                    else f"Aplica el patrón de horarios en {item['id']}."
                )
                item["origin"]["feedback"]["es"] += f" Referencia {item['id']}."
                if item["format"] in {"elegir", "escuchar"}:
                    item["choices"].append({"text": "This alternative does not fit here."})
                    current = item["answer"]["index"]
                    correct = item["choices"].pop(current)
                    target = selection_number % 3
                    item["choices"].insert(target, correct)
                    item["answer"]["index"] = target
                    selection_number += 1
                item["contentHash"] = validator.expected_hash(item)
        writing = single["pools"]["practiceGuided"][1]
        writing["format"] = "escribir"
        writing["prompt"]["es"] = "Escribe la palabra que expresa la frecuencia de la rutina."
        writing["origin"]["text"] = "I usually start my shift at eight."
        writing["contentHash"] = validator.expected_hash(writing)
        return single

    def test_approved_pilot_passes(self):
        result = validator.validate_bundle(self.pilot, start=1, end=5)
        self.assertEqual(result["classes"], 5)
        self.assertEqual(result["items"], 65)

    def test_n2_bundle_uses_cross_level_prerequisite_without_relaxing_contract(self):
        bundle = self.n2_first
        result = validator.validate_bundle(bundle, start=1, end=5, level=2)
        self.assertEqual(result["level"], 2)
        self.assertEqual(result["classes"], 5)
        self.assertEqual(result["items"], 65)
        self.assertEqual(bundle["classes"][0]["prerequisites"], ["en.n1.class-100"])

        wrong_level = copy.deepcopy(bundle)
        with self.assertRaisesRegex(validator.ValidationError, "wrong course/level"):
            validator.validate_bundle(wrong_level, start=1, end=5, level=1)

    def test_agent_v2_contract_enforces_measurable_quality_gates(self):
        single = self.v2_single_class()
        result = validator.validate_bundle(single, start=1, end=1, level=2)
        self.assertEqual(result["items"], 13)

        two_choices = copy.deepcopy(single)
        item = two_choices["pools"]["practiceGuided"][0]
        item["choices"].pop()
        item["contentHash"] = validator.expected_hash(item)
        with self.assertRaisesRegex(validator.ValidationError, "v2 selection needs >=3 choices"):
            validator.validate_bundle(two_choices, start=1, end=1, level=2)

        duplicate_feedback = copy.deepcopy(single)
        first = duplicate_feedback["pools"]["practiceGuided"][0]
        second = duplicate_feedback["pools"]["practiceGuided"][1]
        second["origin"]["feedback"] = copy.deepcopy(first["origin"]["feedback"])
        second["contentHash"] = validator.expected_hash(second)
        with self.assertRaisesRegex(validator.ValidationError, "v2 feedback duplicates"):
            validator.validate_bundle(duplicate_feedback, start=1, end=1, level=2)

        contradictory_ordinal = copy.deepcopy(single)
        item = contradictory_ordinal["pools"]["practiceGuided"][0]
        item["origin"]["feedback"]["es"] = "La segunda opción conserva el dato correcto."
        item["answer"]["index"] = 0
        item["contentHash"] = validator.expected_hash(item)
        with self.assertRaisesRegex(validator.ValidationError, "feedback ordinal contradicts"):
            validator.validate_bundle(contradictory_ordinal, start=1, end=1, level=2)

        unrelated_ordinal = copy.deepcopy(single)
        item = unrelated_ordinal["pools"]["practiceGuided"][0]
        item["origin"]["feedback"]["es"] = "The first step is to identify the stated time."
        item["contentHash"] = validator.expected_hash(item)
        validator.validate_bundle(unrelated_ordinal, start=1, end=1, level=2)

        long_prompt = copy.deepcopy(single)
        item = long_prompt["pools"]["practiceGuided"][0]
        item["prompt"]["es"] = (
            "Escucha con atención y selecciona la alternativa que expresa "
            "exactamente la información presentada en este ejercicio."
        )
        item["contentHash"] = validator.expected_hash(item)
        with self.assertRaisesRegex(validator.ValidationError, "v2 prompt exceeds"):
            validator.validate_bundle(long_prompt, start=1, end=1, level=2)

        deictic_prompt = copy.deepcopy(single)
        item = deictic_prompt["pools"]["practiceGuided"][0]
        item["prompt"]["es"] = "Elige el modelo correcto para la idea trabajada."
        item["contentHash"] = validator.expected_hash(item)
        with self.assertRaisesRegex(validator.ValidationError, "unresolved deictic"):
            validator.validate_bundle(deictic_prompt, start=1, end=1, level=2)

        fixed_position = copy.deepcopy(single)
        for items in fixed_position["pools"].values():
            for item in items:
                if item["format"] in {"elegir", "escuchar"}:
                    current = item["answer"]["index"]
                    correct = item["choices"].pop(current)
                    item["choices"].insert(0, correct)
                    item["answer"]["index"] = 0
                    item["contentHash"] = validator.expected_hash(item)
        with self.assertRaisesRegex(validator.ValidationError, "correct-choice position is constant"):
            validator.validate_bundle(fixed_position, start=1, end=1, level=2)

        no_writing = copy.deepcopy(single)
        item = no_writing["pools"]["practiceGuided"][1]
        item["format"] = "completar"
        item["prompt"]["es"] = "Completa la frecuencia ___ para la rutina diaria."
        item["contentHash"] = validator.expected_hash(item)
        with self.assertRaisesRegex(validator.ValidationError, "escritura skill lacks"):
            validator.validate_bundle(no_writing, start=1, end=1, level=2)

        shallow_production = copy.deepcopy(single)
        shallow_production["phase"] = "production"
        with self.assertRaisesRegex(validator.ValidationError, "production lacks reserved writing"):
            validator.validate_bundle(shallow_production, start=1, end=1, level=2)

        unused_vocabulary = copy.deepcopy(single)
        unused_vocabulary["vocabulary"].append(
            {"en": "unobservable-term", "es": "término no observable"}
        )
        unused_vocabulary["usesVocabulary"].append("unobservable-term")
        with self.assertRaisesRegex(validator.ValidationError, "vocabulary lacks observable use"):
            validator.validate_bundle(unused_vocabulary, start=1, end=1, level=2)

    def test_agent_v2_rejects_punctuation_only_writing_variants(self):
        single = copy.deepcopy(self.n2_production)
        # Aísla esta prueba del legado multiparte de N2 C19; ese contrato tiene
        # una prueba propia y no debe ocultar la variante de escritura inválida.
        for items in single["pools"].values():
            for item in items:
                if item["format"] == "completar":
                    item["origin"]["text"] = "Completa una forma: ___."
                    item["contentHash"] = validator.expected_hash(item)
        writing = next(
            item
            for pool in ("evaluation", "review")
            for item in single["pools"][pool]
            if item["format"] == "escribir" and len(validator.words(item["answer"]["text"])) >= 8
        )
        answer = writing["answer"]["text"]
        writing["answer"]["accepted"] = [answer, answer.rstrip(".")]
        writing["contentHash"] = validator.expected_hash(writing)
        with self.assertRaisesRegex(validator.ValidationError, "production lacks extended writing"):
            validator.validate_bundle(single, start=19, end=19, level=2)

    def test_runtime_contract_rejects_unrenderable_multi_blank_completion(self):
        single = self.v2_single_class()
        item = next(
            item
            for items in single["pools"].values()
            for item in items
            if item["format"] == "completar"
        )
        item["origin"]["text"] = "When ___ arrives, we will ___ the room."
        item["contentHash"] = validator.expected_hash(item)

        with self.assertRaisesRegex(validator.ValidationError, "at most one visible blank"):
            validator.validate_bundle(single, start=1, end=1, level=2)

    def test_runtime_contract_accepts_valid_multipart_completion(self):
        single = self.v2_single_class()
        item = next(
            item
            for items in single["pools"].values()
            for item in items
            if item["format"] == "completar"
        )
        item["origin"].pop("text", None)
        item["origin"]["sentences"] = [
            "I ___ home when the rain ___.",
            "They ___ outside when the bus ___.",
        ]
        item["origin"]["scoring"] = {
            "parts": 2,
            "minimumCorrect": 1,
            "requiredParts": [1],
        }
        item["answer"] = {
            "text": "was walking / started | were waiting / arrived",
            "accepted": ["was walking / started | were waiting / arrived"],
            "parts": [
                {
                    "text": "was walking / started",
                    "accepted": ["was walking / started", "was walking; started"],
                },
                {
                    "text": "were waiting / arrived",
                    "accepted": ["were waiting / arrived"],
                },
            ],
        }
        item["contentHash"] = validator.expected_hash(item)

        result = validator.validate_bundle(single, start=1, end=1, level=2)
        self.assertEqual(result["items"], 13)

        broken = copy.deepcopy(single)
        target = next(
            candidate
            for items in broken["pools"].values()
            for candidate in items
            if candidate["id"] == item["id"]
        )
        target["answer"]["parts"].pop()
        target["contentHash"] = validator.expected_hash(target)
        with self.assertRaisesRegex(validator.ValidationError, "count mismatch"):
            validator.validate_bundle(broken, start=1, end=1, level=2)

        invalid_required = copy.deepcopy(single)
        target = next(
            candidate
            for items in invalid_required["pools"].values()
            for candidate in items
            if candidate["id"] == item["id"]
        )
        target["origin"]["scoring"]["requiredParts"] = [2]
        target["contentHash"] = validator.expected_hash(target)
        with self.assertRaisesRegex(validator.ValidationError, "invalid indexes"):
            validator.validate_bundle(invalid_required, start=1, end=1, level=2)

        stricter_than_declared = copy.deepcopy(single)
        target = next(
            candidate
            for items in stricter_than_declared["pools"].values()
            for candidate in items
            if candidate["id"] == item["id"]
        )
        target["origin"]["scoring"]["requiredParts"] = [0, 1]
        target["contentHash"] = validator.expected_hash(target)
        with self.assertRaisesRegex(validator.ValidationError, "stricter than declared"):
            validator.validate_bundle(stricter_than_declared, start=1, end=1, level=2)

        unprompted_pipe = copy.deepcopy(single)
        target = next(
            candidate
            for items in unprompted_pipe["pools"].values()
            for candidate in items
            if candidate["id"] == item["id"]
        )
        target["answer"]["parts"][0] = {
            "text": "was walking | started",
            "accepted": ["was walking | started"],
        }
        target["contentHash"] = validator.expected_hash(target)
        with self.assertRaisesRegex(validator.ValidationError, "unprompted pipe separator"):
            validator.validate_bundle(unprompted_pipe, start=1, end=1, level=2)

    def test_writing_rubric_requires_range_groups_and_model_evidence(self):
        single = self.v2_single_class()
        item = single["pools"]["practiceGuided"][1]
        model = "My goal is eight dates in two weeks with dated answer sheets."
        item["answer"] = {
            "text": model,
            "accepted": [
                model,
                "My aim is eight dates in fourteen days with dated records.",
            ],
        }
        item["origin"]["scoring"] = {
            "wordRange": [8, 14],
            "evidenceGroups": [
                ["my goal is", "my aim is"],
                ["two weeks", "fourteen days"],
                ["dated answer sheets", "dated records"],
            ],
        }
        item["contentHash"] = validator.expected_hash(item)
        validator.validate_bundle(single, start=1, end=1, level=2)

        absent = copy.deepcopy(single)
        target = absent["pools"]["practiceGuided"][1]
        target["origin"]["scoring"]["evidenceGroups"][2] = ["weekly recordings"]
        target["contentHash"] = validator.expected_hash(target)
        with self.assertRaisesRegex(validator.ValidationError, "absent from every model"):
            validator.validate_bundle(absent, start=1, end=1, level=2)

    def test_partial_threshold_requires_a_runtime_multipart_format(self):
        single = self.v2_single_class()
        item = next(
            item
            for items in single["pools"].values()
            for item in items
            if item["format"] == "elegir"
        )
        item["origin"]["scoring"] = {"parts": 6, "minimumCorrect": 5}
        item["contentHash"] = validator.expected_hash(item)

        with self.assertRaisesRegex(validator.ValidationError, "only executable for relacionar"):
            validator.validate_bundle(single, start=1, end=1, level=2)

    def test_single_class_schema_is_normalized_without_relaxing_rules(self):
        single = copy.deepcopy(self.pilot["classes"][0])
        for key in ("course", "level", "scale", "status", "runtimeAi", "selectionPolicy", "evidencePolicy"):
            single[key] = copy.deepcopy(self.pilot[key])
        single["schema"] = validator.SCHEMA_CLASS
        result = validator.validate_bundle(single, start=1, end=1)
        self.assertEqual(result["classes"], 1)
        self.assertEqual(result["items"], 13)

    def test_standalone_block_close_proves_all_cumulative_concepts(self):
        single = copy.deepcopy(self.pilot["classes"][4])
        for key in ("course", "level", "scale", "status", "runtimeAi", "selectionPolicy", "evidencePolicy"):
            single[key] = copy.deepcopy(self.pilot[key])
        single["schema"] = validator.SCHEMA_CLASS
        result = validator.validate_bundle(single, start=5, end=5)
        self.assertEqual(result["classes"], 1)

    def test_declared_bad_fixtures_fail_for_expected_reason(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                bad = mutate(self.pilot, case)
                with self.assertRaisesRegex(validator.ValidationError, case["expected"]):
                    validator.validate_bundle(bad, start=1, end=5)

    def test_range_and_class_ids_are_generic(self):
        shifted = copy.deepcopy(self.pilot)
        # A mismatched declared range must fail before accepting the pilot by accident.
        with self.assertRaisesRegex(validator.ValidationError, "expected 6 classes"):
            validator.validate_bundle(shifted, start=1, end=6)

    def test_optional_editorial_image_requires_existing_asset_and_alt_text(self):
        visual = copy.deepcopy(self.pilot)
        item = visual["classes"][0]["pools"]["practiceGuided"][0]
        item["origin"]["imageAsset"] = "assets/img/logo.png"
        item["origin"]["imageAlt"] = "Logo de OneLingo usado como fixture visual."
        item["contentHash"] = validator.expected_hash(item)
        self.assertEqual(validator.validate_bundle(visual, start=1, end=5)["classes"], 5)

        missing_alt = copy.deepcopy(visual)
        broken = missing_alt["classes"][0]["pools"]["practiceGuided"][0]
        del broken["origin"]["imageAlt"]
        broken["contentHash"] = validator.expected_hash(broken)
        with self.assertRaisesRegex(validator.ValidationError, "imageAlt missing"):
            validator.validate_bundle(missing_alt, start=1, end=5)

        missing_asset = copy.deepcopy(visual)
        broken = missing_asset["classes"][0]["pools"]["practiceGuided"][0]
        broken["origin"]["imageAsset"] = "assets/img/does-not-exist.webp"
        broken["contentHash"] = validator.expected_hash(broken)
        with self.assertRaisesRegex(validator.ValidationError, "imageAsset does not exist"):
            validator.validate_bundle(missing_asset, start=1, end=5)

    def test_strict_answer_policy_allows_single_token_reuse(self):
        single = copy.deepcopy(self.pilot["classes"][1])
        for key in ("course", "level", "scale", "status", "runtimeAi", "selectionPolicy", "evidencePolicy"):
            single[key] = copy.deepcopy(self.pilot[key])
        single["schema"] = validator.SCHEMA_CLASS
        single["qualityPolicy"] = {"answerReuseAcrossEarlyReserved": "forbid"}

        guided = single["pools"]["practiceGuided"][2]
        review_completion = single["pools"]["review"][1]
        for item, prompt, context in (
            (guided, "Completa: This is ___ apple.", "This is an apple."),
            (review_completion, "Completa: I see ___ orange.", "I see an orange."),
        ):
            item["prompt"]["es"] = prompt
            item["answer"] = {"text": "an", "accepted": ["an"]}
            item["origin"]["text"] = context
            item["contentHash"] = validator.expected_hash(item)

        listening = single["pools"]["review"][0]
        listening["choices"][listening["answer"]["index"]]["text"] = "We are students."
        listening["origin"]["audio"] = "We are students."
        listening["origin"]["audioText"] = "We are students."
        listening["contentHash"] = validator.expected_hash(listening)

        result = validator.validate_bundle(single, start=2, end=2)
        self.assertEqual(result["classes"], 1)
        self.assertIsNone(validator.reusable_answer_signature({"format": "completar", "answer": {"text": "an"}}))

        strict_duplicate = copy.deepcopy(single)
        for item in (
            strict_duplicate["pools"]["practiceGuided"][0],
            strict_duplicate["pools"]["evaluation"][0],
        ):
            item["choices"][item["answer"]["index"]]["text"] = "The chair is here."
            item["contentHash"] = validator.expected_hash(item)
        with self.assertRaisesRegex(validator.ValidationError, "answer semantic duplicate of practice"):
            validator.validate_bundle(strict_duplicate, start=2, end=2)

    def test_atomic_answer_evidence_crosses_formats(self):
        early, reserved = {}, {}
        writing = {"id": "early-writing", "format": "escribir", "answer": {"text": "The chair is here."}}
        matching = {"id": "evaluation-matching", "format": "relacionar", "answer": {"pairs": [["The chair is here.", {"es": "La silla está aquí."}]]}}
        validator.register_answer_evidence(writing, "practice", early, reserved)
        with self.assertRaisesRegex(validator.ValidationError, "answer evidence duplicate of practice"):
            validator.register_answer_evidence(matching, "evaluation", early, reserved)

    def test_atomic_answer_evidence_rejects_evaluation_review_reuse(self):
        early, reserved = {}, {}
        evaluation = {"id": "evaluation-ordering", "format": "ordenar", "answer": {"text": "A green table."}}
        review = {"id": "review-matching", "format": "relacionar", "answer": {"pairs": [["a green table", {"es": "una mesa verde"}]]}}
        validator.register_answer_evidence(evaluation, "evaluation", early, reserved)
        with self.assertRaisesRegex(validator.ValidationError, "inside reserved pools"):
            validator.register_answer_evidence(review, "review", early, reserved)

    def test_atomic_answer_evidence_rejects_guided_practice_reuse(self):
        early, reserved = {}, {}
        guided = {"id": "guided-writing", "format": "escribir", "answer": {"text": "She is my sister."}}
        practice = {"id": "practice-choice", "format": "elegir", "choices": [{"text": "She is my sister."}, {"text": "He is my brother."}], "answer": {"index": 0}}
        validator.register_answer_evidence(guided, "practiceGuided", early, reserved)
        with self.assertRaisesRegex(validator.ValidationError, "inside practice pools"):
            validator.register_answer_evidence(practice, "practice", early, reserved)

    def test_atomic_answer_evidence_ignores_single_tokens(self):
        early, reserved = {}, {}
        for pool, item_id in (("practice", "practice-an"), ("evaluation", "evaluation-an")):
            validator.register_answer_evidence({"id": item_id, "format": "completar", "answer": {"text": "an"}}, pool, early, reserved)
        self.assertEqual(early, {})
        self.assertEqual(reserved, {})

    def test_antileak_scope_allows_recycling_in_later_class(self):
        two_classes = copy.deepcopy(self.pilot)
        two_classes["classes"] = two_classes["classes"][:2]
        prior_pair = copy.deepcopy(two_classes["classes"][0]["pools"]["evaluation"][3]["answer"]["pairs"][2])
        later = two_classes["classes"][1]["pools"]["practice"][2]
        later["answer"]["pairs"][0] = copy.deepcopy(prior_pair)
        later["origin"]["pairs"][0] = copy.deepcopy(prior_pair)
        later["contentHash"] = validator.expected_hash(later)
        result = validator.validate_bundle(two_classes, start=1, end=2)
        self.assertEqual(result["classes"], 2)


if __name__ == "__main__":
    unittest.main()
