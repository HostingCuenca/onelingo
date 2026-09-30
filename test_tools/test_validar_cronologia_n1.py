from __future__ import annotations

import copy
import json
import pathlib
import unittest

from tools.contenido import validar_cronologia_n1 as chronology


HERE = pathlib.Path(__file__).resolve().parent
MANIFEST = HERE.parent / "assets/contenido/en/plan-editorial/cronologia-n1-01-20.json"


class ChronologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.index = chronology.validate_manifest(cls.manifest)
        cls.base_manifest = copy.deepcopy(cls.manifest)
        cls.base_manifest["classes"] = cls.base_manifest["classes"][:20]
        cls.base_manifest["range"]["end"] = 20

    @staticmethod
    def class_document(number, vocabulary, patterns):
        return {
            "schema": "onelingo.editorial.class.v1",
            "id": f"en.n1.class-{number:02d}",
            "usesVocabulary": vocabulary,
            "usesPatterns": patterns,
        }

    def test_manifest_is_chronological(self):
        self.assertEqual(len(self.index), self.manifest["range"]["end"])

    def test_manifest_accepts_contiguous_class_21(self):
        extended = copy.deepcopy(self.base_manifest)
        extended["range"]["end"] = 21
        extended["classes"].append({
            "id": "en.n1.class-21",
            "title": "Habitaciones y muebles",
            "introducedVocabulary": ["bedroom"],
            "allowedCarryover": ["room"],
            "newPatterns": ["rooms-and-furniture"],
            "requiresPatterns": ["room-inventory-description"],
        })
        self.assertEqual(len(chronology.validate_manifest(extended)), 21)

    def test_manifest_accepts_class_100_id(self):
        extended = copy.deepcopy(self.manifest)
        extended["range"]["end"] = 100
        for number in range(len(extended["classes"]) + 1, 101):
            extended["classes"].append({
                "id": f"en.n1.class-{number:02d}",
                "title": f"Class {number}",
                "introducedVocabulary": [],
                "allowedCarryover": [],
                "newPatterns": [f"pattern-{number}"],
                "requiresPatterns": [],
            })
        self.assertIn("en.n1.class-100", chronology.validate_manifest(extended))

    def test_manifest_rejects_gap_after_class_20(self):
        extended = copy.deepcopy(self.base_manifest)
        extended["range"]["end"] = 21
        extended["classes"].append({
            "id": "en.n1.class-22",
            "title": "Gap",
            "introducedVocabulary": [],
            "allowedCarryover": [],
            "newPatterns": [],
            "requiresPatterns": [],
        })
        with self.assertRaisesRegex(chronology.ChronologyError, "malformed/out-of-order id"):
            chronology.validate_manifest(extended)

    def test_manifest_rejects_reintroduction_after_class_20(self):
        extended = copy.deepcopy(self.manifest)
        next_number = len(extended["classes"]) + 1
        extended["range"]["end"] = next_number
        extended["classes"].append({
            "id": f"en.n1.class-{next_number:02d}",
            "title": "Repeated vocabulary",
            "introducedVocabulary": ["room"],
            "allowedCarryover": [],
            "newPatterns": [],
            "requiresPatterns": [],
        })
        with self.assertRaisesRegex(chronology.ChronologyError, "vocabulary reintroduced"):
            chronology.validate_manifest(extended)

    def test_manifest_rejects_segment_without_base_context(self):
        segment = copy.deepcopy(self.manifest)
        segment["classes"] = [{
            "id": "en.n1.class-21",
            "title": "Segment",
            "introducedVocabulary": ["bedroom"],
            "allowedCarryover": [],
            "newPatterns": [],
            "requiresPatterns": [],
        }]
        with self.assertRaisesRegex(chronology.ChronologyError, "minimum 20"):
            chronology.validate_manifest(segment)

    def test_partial_range_uses_full_prior_context(self):
        index = chronology.validate_manifest(self.manifest)
        data = self.class_document(22, ["there", "room"], ["there-is-are-affirmative", "rooms-furniture"])
        chronology.validate_declarations(data, index, start=22, end=22)

    def test_partial_range_rejects_class_outside_requested_window(self):
        data = self.class_document(20, ["eyes"], ["family-possession-integration"])
        with self.assertRaisesRegex(chronology.ChronologyError, "outside requested range"):
            chronology.validate_declarations(data, self.index, start=21, end=40)

    def test_reserved_term_is_blocked_across_block_boundary(self):
        extended = copy.deepcopy(self.manifest)
        first = len(extended["classes"]) + 1
        second = first + 1
        extended["range"]["end"] = second
        extended["reservedFutureVocabulary"].append("garden")
        extended["classes"].append({
            "id": f"en.n1.class-{first:02d}",
            "title": "Existence",
            "introducedVocabulary": [],
            "allowedCarryover": ["room"],
            "newPatterns": ["existence-review"],
            "requiresPatterns": ["there-is-are-affirmative"],
        })
        extended["classes"].append({
            "id": f"en.n1.class-{second:02d}",
            "title": "Garden",
            "introducedVocabulary": ["garden"],
            "allowedCarryover": ["room"],
            "newPatterns": ["garden-naming"],
            "requiresPatterns": ["existence-review"],
        })
        index = chronology.validate_manifest(extended)
        data = self.class_document(first, ["room"], ["existence-review"])
        data["qualityPolicy"] = {"chronologyTokens": "enforce"}
        data["teaching"] = [{"en": "This garden is small."}]
        with self.assertRaisesRegex(chronology.ChronologyError, "reserved future vocabulary 'garden'"):
            chronology.validate_declarations(data, index, start=first, end=first)

    def test_manifest_rejects_stale_declared_range(self):
        bad = copy.deepcopy(self.manifest)
        bad["range"]["end"] = 20
        with self.assertRaisesRegex(chronology.ChronologyError, rf"chronology range must be 1-{len(self.manifest['classes'])}"):
            chronology.validate_manifest(bad)

    def test_class_08_can_use_its_irregular_plural_scope(self):
        data = self.class_document(8, ["man", "men", "child", "children"], ["regular-plurals", "irregular-plurals"])
        result = chronology.validate_declarations(data, self.index)
        self.assertEqual(result["vocabulary"], 4)

    def test_class_08_cannot_advance_colors_from_class_11(self):
        data = self.class_document(8, ["red"], ["irregular-plurals"])
        with self.assertRaisesRegex(chronology.ChronologyError, "vocabulary used before introduction"):
            chronology.validate_declarations(data, self.index)

    def test_class_11_can_introduce_colors(self):
        data = self.class_document(11, ["red", "blue", "small"], ["adjective-description"])
        chronology.validate_declarations(data, self.index)

    def test_class_08_cannot_advance_adjective_pattern(self):
        data = self.class_document(8, ["men"], ["adjective-description"])
        with self.assertRaisesRegex(chronology.ChronologyError, "pattern used before introduction"):
            chronology.validate_declarations(data, self.index)

    def test_manifest_rejects_early_carryover(self):
        bad = copy.deepcopy(self.manifest)
        bad["classes"][7]["allowedCarryover"].append("red")
        with self.assertRaisesRegex(chronology.ChronologyError, "carryover before introduction"):
            chronology.validate_manifest(bad)

    def test_opt_in_reserved_future_token_finds_new_in_structured_choice(self):
        data = self.class_document(9, ["the", "book"], ["articles-the-contrast"])
        data["qualityPolicy"] = {"chronologyTokens": "enforce"}
        data["pools"] = {"evaluation": [{"choices": [{"text": "The book is new."}, {"text": "The book is here."}]}]}
        with self.assertRaisesRegex(chronology.ChronologyError, "reserved future vocabulary 'new'"):
            chronology.validate_declarations(data, self.index)

    def test_reserved_future_scan_is_opt_in_for_legacy_documents(self):
        data = self.class_document(9, ["the", "book"], ["articles-the-contrast"])
        data["teaching"] = [{"en": "The book is new."}]
        chronology.validate_declarations(data, self.index)

    def test_class_10_cumulative_patterns_must_be_declared(self):
        data = self.class_document(10, ["room", "table"], ["articles-a-an", "articles-the-contrast", "regular-plurals", "room-inventory-description"])
        data["cumulativeEvaluation"] = ["regular-plurals", "irregular-plurals"]
        with self.assertRaisesRegex(chronology.ChronologyError, "cumulative patterns missing from usesPatterns"):
            chronology.validate_declarations(data, self.index)

    def test_class_10_cannot_use_reserved_has_before_class_19(self):
        data = self.class_document(10, ["room", "table"], ["articles-a-an", "articles-the-contrast", "regular-plurals", "irregular-plurals", "room-inventory-description"])
        data["qualityPolicy"] = {"chronologyTokens": "enforce"}
        data["teaching"] = [{"en": "The room has a table."}]
        with self.assertRaisesRegex(chronology.ChronologyError, "reserved future vocabulary 'has'"):
            chronology.validate_declarations(data, self.index)

    def test_exhaustive_vocabulary_rejects_undeclared_learner_token(self):
        data = self.class_document(17, ["our", "home"], ["possessive-adjectives-plural"])
        data["qualityPolicy"] = {"vocabularyDeclarations": "exhaustive"}
        data["teaching"] = [{"en": "our home their"}]
        with self.assertRaisesRegex(chronology.ChronologyError, r"learner vocabulary not declared: \['their'\]"):
            chronology.validate_declarations(data, self.index)

    def test_exhaustive_vocabulary_rejects_declared_but_unused_token(self):
        data = self.class_document(17, ["our", "home", "parents"], ["possessive-adjectives-plural"])
        data["qualityPolicy"] = {"vocabularyDeclarations": "exhaustive"}
        data["teaching"] = [{"en": "our home"}]
        with self.assertRaisesRegex(chronology.ChronologyError, r"declared vocabulary not used: \['parents'\]"):
            chronology.validate_declarations(data, self.index)

    def test_exhaustive_vocabulary_normalizes_possessive_s(self):
        data = self.class_document(18, ["mother", "photo"], ["possessive-s"])
        data["qualityPolicy"] = {"vocabularyDeclarations": "exhaustive"}
        data["teaching"] = [{"en": "mother's photo"}]
        chronology.validate_declarations(data, self.index)

    def test_exhaustive_vocabulary_accepts_declared_multiword_phrase(self):
        data = self.class_document(19, ["i", "have", "have got", "book"], ["have-got-possession"])
        data["qualityPolicy"] = {"vocabularyDeclarations": "exhaustive"}
        data["teaching"] = [{"en": "I have got book"}]
        chronology.validate_declarations(data, self.index)

    def test_exhaustive_vocabulary_rejects_unused_multiword_phrase(self):
        data = self.class_document(19, ["i", "have", "have got", "book", "has got"], ["have-got-possession"])
        data["qualityPolicy"] = {"vocabularyDeclarations": "exhaustive"}
        data["teaching"] = [{"en": "I have got book"}]
        with self.assertRaisesRegex(chronology.ChronologyError, r"declared vocabulary not used: \['has got'\]"):
            chronology.validate_declarations(data, self.index)


if __name__ == "__main__":
    unittest.main()
