from __future__ import annotations

import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
N3 = ROOT / "assets/contenido/en/editorial/n3"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n3-editorial-v2.json"


class N3EditorialSimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class_files = sorted(N3.glob("class-[0-9][0-9].json"))
        numbers = [int(path.stem.split("-")[1]) for path in class_files]
        if numbers != list(range(1, len(numbers) + 1)):
            raise AssertionError(f"N3 authored classes are not contiguous: {numbers}")
        cls.classes = [json.loads(path.read_text(encoding="utf-8")) for path in class_files]
        cls.map = json.loads(MAP.read_text(encoding="utf-8"))

    def test_n3_starts_after_completed_n2_and_keeps_prerequisites_contiguous(self):
        completed = {"en.n2.class-100"}
        for lesson in self.classes:
            self.assertTrue(set(lesson["prerequisites"]) <= completed)
            completed.add(lesson["id"])

    def test_authored_classes_follow_the_frozen_map(self):
        map_by_id = {item["id"]: item for item in self.map["classes"]}
        for lesson in self.classes:
            planned = map_by_id[lesson["id"]]
            self.assertEqual(lesson["title"], planned["title"])
            self.assertEqual(lesson["phase"], planned["phase"])
            self.assertEqual(lesson["prerequisites"], planned["prerequisites"])

    def test_every_evaluation_has_deterministic_remediation(self):
        for lesson in self.classes:
            teaching = {item["id"] for item in lesson["teaching"]}
            review = {item["id"] for item in lesson["pools"]["review"]}
            evaluation = {item["id"] for item in lesson["pools"]["evaluation"]}
            self.assertEqual(set(lesson["remediationMap"]), evaluation)
            for target in lesson["remediationMap"].values():
                self.assertIn(target["reteach"], teaching)
                self.assertIn(target["review"], review)

    def test_each_transfer_class_demonstrates_its_five_block_concepts(self):
        for index, transfer in enumerate(self.classes):
            if transfer["phase"] != "transfer":
                continue
            block = self.classes[index - 4 : index + 1]
            self.assertEqual(len(block), 5)
            expected = {item["concepts"][0] for item in block}
            evidence = {
                concept
                for item in transfer["pools"]["evaluation"]
                for concept in item["requires"]
            }
            self.assertEqual(set(transfer["cumulativeEvaluation"]), expected)
            self.assertTrue(expected <= evidence)

    def test_ids_are_unique_and_attempt_metadata_is_stable(self):
        ids = []
        for lesson in self.classes:
            self.assertTrue(lesson["selectionPolicy"]["deterministic"])
            self.assertEqual(
                lesson["evidencePolicy"]["attemptRecords"],
                ["variantId", "libraryVersion", "selectionId"],
            )
            for pool in lesson["pools"].values():
                ids.extend(item["id"] for item in pool)
        self.assertEqual(len(ids), len(self.classes) * 13)
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
