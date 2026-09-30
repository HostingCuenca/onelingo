from __future__ import annotations

import json
import pathlib
import re
import unittest

from tools.contenido import validar_bundle_editorial as validator


ROOT = pathlib.Path(__file__).resolve().parents[1]
N2 = ROOT / "assets/contenido/en/editorial/n2"
MAP = ROOT / "assets/contenido/en/plan-editorial/mapa-n2-editorial-v2.json"


class N2EditorialSimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.classes = [
            json.loads((N2 / f"class-{number:02d}.json").read_text(encoding="utf-8"))
            for number in range(1, 101)
        ]
        cls.map = json.loads(MAP.read_text(encoding="utf-8"))

    def test_beginner_can_follow_every_prerequisite_from_n1(self):
        completed = {"en.n1.class-100"}
        for lesson in self.classes:
            self.assertTrue(set(lesson["prerequisites"]) <= completed)
            completed.add(lesson["id"])

    def test_total_failure_always_has_deterministic_remediation(self):
        for lesson in self.classes:
            teaching = {item["id"] for item in lesson["teaching"]}
            review = {item["id"] for item in lesson["pools"]["review"]}
            evaluation = {item["id"] for item in lesson["pools"]["evaluation"]}
            self.assertEqual(set(lesson["remediationMap"]), evaluation)
            for target in lesson["remediationMap"].values():
                self.assertIn(target["reteach"], teaching)
                self.assertIn(target["review"], review)

    def test_perfect_student_receives_real_block_evidence(self):
        for end in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100):
            lesson = self.classes[end - 1]
            block_concepts = {item["concepts"][0] for item in self.classes[end - 5:end]}
            evidence = {concept for item in lesson["pools"]["evaluation"] for concept in item["requires"]}
            self.assertEqual(set(lesson["cumulativeEvaluation"]), block_concepts)
            self.assertTrue(block_concepts <= evidence)

    def test_reentry_keeps_stable_ids_and_attempt_metadata(self):
        ids = []
        for lesson in self.classes:
            self.assertTrue(lesson["selectionPolicy"]["deterministic"])
            self.assertEqual(lesson["evidencePolicy"]["attemptRecords"], ["variantId", "libraryVersion", "selectionId"])
            for pool in lesson["pools"].values():
                ids.extend(item["id"] for item in pool)
        self.assertEqual(len(ids), len(self.classes) * 13)
        self.assertEqual(len(ids), len(set(ids)))

    def test_accessibility_profile_has_short_prompts_and_audio_controls(self):
        for lesson in self.classes:
            self.assertTrue(lesson["accessibility"]["screenReader"])
            for pool in lesson["pools"].values():
                for item in pool:
                    self.assertLessEqual(len(item["prompt"]["es"]), 90)
                    if item["format"] == "escuchar":
                        self.assertEqual(item["origin"]["speedOptions"], [0.75, 1.0])
                        self.assertEqual(item["origin"]["maxReplays"], 3)

    def test_full_map_has_twenty_complete_five_phase_blocks(self):
        classes = self.map["classes"]
        self.assertEqual(len(classes), 100)
        self.assertEqual(len({item["id"] for item in classes}), 100)
        phases = ["input", "form", "comprehension", "production", "transfer"]
        for offset in range(0, 100, 5):
            self.assertEqual([item["phase"] for item in classes[offset:offset + 5]], phases)

    def test_authored_classes_follow_the_frozen_map(self):
        map_by_id = {item["id"]: item for item in self.map["classes"]}
        for lesson in self.classes:
            planned = map_by_id[lesson["id"]]
            self.assertEqual(lesson["title"], planned["title"])
            self.assertEqual(lesson["prerequisites"], planned["prerequisites"])
            if int(lesson["id"].rsplit("-", 1)[1]) >= 16:
                self.assertEqual(lesson["phase"], planned["phase"])

    def test_agent_v2_blocks_have_diverse_prompts_feedback_and_positions(self):
        for start in (16, 21, 26, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76, 81, 86, 91, 96):
            block = self.classes[start - 1:start + 4]
            prompts = []
            feedback = []
            positions = []
            for lesson in block:
                self.assertEqual(
                    lesson["qualityPolicy"]["agentContract"],
                    validator.AGENT_CONTRACT_V2,
                )
                for items in lesson["pools"].values():
                    for item in items:
                        prompts.append(validator.normalized(item["prompt"]["es"]))
                        feedback.append(
                            validator.normalized(item["origin"]["feedback"]["es"])
                        )
                        if item["format"] in {"elegir", "escuchar"}:
                            positions.append(item["answer"]["index"])
                            self.assertGreaterEqual(len(item["choices"]), 3)
            self.assertEqual(len(prompts), len(set(prompts)))
            self.assertEqual(len(feedback), len(set(feedback)))
            counts = {index: positions.count(index) for index in set(positions)}
            self.assertGreaterEqual(len(counts), 2)
            self.assertLessEqual(max(counts.values()) / len(positions), 0.60)

    def test_agent_v2_production_and_transfer_are_extended(self):
        for number in (19, 20, 24, 25, 29, 30, 34, 35, 39, 40, 44, 45, 49, 50, 54, 55, 59, 60, 64, 65, 69, 70, 74, 75, 79, 80, 84, 85, 89, 90, 94, 95, 99, 100):
            lesson = self.classes[number - 1]
            writings = [
                item
                for pool in ("evaluation", "review")
                for item in lesson["pools"][pool]
                if item["format"] == "escribir"
            ]
            self.assertTrue(
                any(
                    len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", item["answer"]["text"])) >= 8
                    and len(item["answer"]["accepted"]) >= 2
                    and len({validator.normalized(value) for value in item["answer"]["accepted"]}) >= 2
                    for item in writings
                ),
                lesson["id"],
            )


if __name__ == "__main__":
    unittest.main()
