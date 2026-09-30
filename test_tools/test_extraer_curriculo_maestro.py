import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "curriculo"))

from extraer_curriculo_maestro import parse_curriculum, validate_curriculum  # noqa: E402


class CurriculumMasterTest(unittest.TestCase):
    def test_extracts_fields_and_removes_runtime_ai_instruction(self):
        lessons = []
        for number in range(1, 101):
            lessons.append(
                f"""LECCIÓN {number} — Lesson {number}
Temas: Topic {number} | words | structure
Contenido: Teach the words.
Gramática/estructuras: Teach the structure.
Práctica con IA: role-play the situation. The AI must generate feedback.
Aplicación real: Apply it.
Resultado: Complete the task.
"""
            )
        text = "\n".join(
            f"NIVEL {level} — Level {level}\n" + "\n".join(lessons)
            for level in range(1, 11)
        )
        result = parse_curriculum(text)
        self.assertEqual([], validate_curriculum(result))
        self.assertFalse(result["runtimeAiRequired"])
        first = result["levels"][0]["lecciones"][0]
        self.assertEqual("role-play the situation", first["practicaEditorial"])
        self.assertNotRegex(str(result), r"\bAI\b")

    def test_validation_rejects_incomplete_source(self):
        result = parse_curriculum(
            """NIVEL 1 — Level
LECCIÓN 1 — Title
Temas: Topic | words | structure
Contenido: Content
Gramática/estructuras: Structure
Práctica con IA: Practice
Aplicación real: Apply
Resultado: Result
"""
        )
        self.assertTrue(validate_curriculum(result))


if __name__ == "__main__":
    unittest.main()
