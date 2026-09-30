#!/usr/bin/env python3
"""Convierte el PDF maestro de inglés en un manifiesto editorial verificable.

El documento del cliente describe una actividad como ``Práctica con IA``. La
ruta base de OneLingo no ejecuta esa instrucción: el importador conserva solo
el escenario anterior a la frase normativa y lo publica como
``practicaEditorial`` para que un editor redacte ejercicios estáticos.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path


LEVEL_RE = re.compile(r"NIVEL (\d+) — ([^\n]+)")
LESSON_RE = re.compile(r"LECCIÓN (\d+) — ([^\n]+)")
FIELDS = (
    ("temas", "Temas:"),
    ("contenido", "Contenido:"),
    ("estructuras", "Gramática/estructuras:"),
    ("practicaFuente", "Práctica con IA:"),
    ("aplicacionReal", "Aplicación real:"),
    ("resultado", "Resultado:"),
)


def _plain(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\f", " ")).strip()


def _without_runtime_ai(text: str) -> str:
    text = re.sub(
        r"\s*The AI should recycle the level's core language instead of "
        r"introducing a large new grammar load\.",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\bAI feedback\b", "editorial feedback", text, flags=re.I)
    text = re.sub(
        r"\bsustained AI conversation\b",
        "sustained structured conversation",
        text,
        flags=re.I,
    )
    return text.strip()


def _extract_text(source: Path) -> str:
    if source.suffix.lower() == ".txt":
        return source.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="onelingo-curriculum-") as tmp:
        target = Path(tmp) / "curriculum.txt"
        subprocess.run(
            ["pdftotext", "-layout", str(source), str(target)],
            check=True,
            capture_output=True,
            text=True,
        )
        return target.read_text(encoding="utf-8")


def _field(segment: str, label: str, next_labels: list[str]) -> str:
    end = "|".join(re.escape(value) for value in next_labels)
    pattern = rf"{re.escape(label)}\s*(.*?)(?=\n\s*(?:{end})|\Z)"
    match = re.search(pattern, segment, flags=re.DOTALL)
    return _plain(match.group(1)) if match else ""


def _editorial_practice(source: str) -> str:
    practice = re.split(
        r"\bThe AI (?:must|should)\b", source, maxsplit=1, flags=re.IGNORECASE
    )[0].strip().rstrip(".")
    replacements = {
        "AI interview": "structured interview",
        "AI free conversation": "free conversation with editorial prompts",
        "AI correction": "guided error-correction activity",
        "AI assessment simulation": "editorial assessment simulation",
        "AI-guided project": "editorially guided project",
    }
    for old, new in replacements.items():
        practice = re.sub(re.escape(old), new, practice, flags=re.IGNORECASE)
    return _without_runtime_ai(practice)


def parse_curriculum(text: str) -> dict:
    level_matches = list(LEVEL_RE.finditer(text))
    levels = []
    for level_index, level_match in enumerate(level_matches):
        end = (
            level_matches[level_index + 1].start()
            if level_index + 1 < len(level_matches)
            else len(text)
        )
        level_segment = text[level_match.end() : end]
        lesson_matches = list(LESSON_RE.finditer(level_segment))
        lessons = []
        for lesson_index, lesson_match in enumerate(lesson_matches):
            lesson_end = (
                lesson_matches[lesson_index + 1].start()
                if lesson_index + 1 < len(lesson_matches)
                else len(level_segment)
            )
            segment = level_segment[lesson_match.end() : lesson_end]
            values = {}
            for field_index, (key, label) in enumerate(FIELDS):
                following = [item[1] for item in FIELDS[field_index + 1 :]]
                values[key] = _field(segment, label, following) if following else _plain(
                    segment.split(label, 1)[1] if label in segment else ""
                )

            raw_topics = [part.strip() for part in values.pop("temas").split("|")]
            practice_source = values.pop("practicaFuente")
            practice_editorial = _editorial_practice(practice_source)
            number = int(lesson_match.group(1))
            level = int(level_match.group(1))
            lessons.append(
                {
                    "id": f"en.n{level}.l{number:03d}",
                    "numero": number,
                    "titulo": _without_runtime_ai(_plain(lesson_match.group(2))),
                    "tema": _without_runtime_ai(raw_topics[0]) if raw_topics else "",
                    "vocabularioObjetivo": _without_runtime_ai(raw_topics[1]) if len(raw_topics) > 1 else "",
                    "estructuraObjetivo": _without_runtime_ai(raw_topics[2]) if len(raw_topics) > 2 else "",
                    "contenido": _without_runtime_ai(values["contenido"]),
                    "estructuras": _without_runtime_ai(values["estructuras"]),
                    "practicaEditorial": practice_editorial,
                    "aplicacionReal": _without_runtime_ai(values["aplicacionReal"]),
                    "resultado": _without_runtime_ai(values["resultado"]),
                    "estadoEditorial": "especificacion_fuente",
                }
            )
        levels.append(
            {
                "nivel": int(level_match.group(1)),
                "titulo": _plain(level_match.group(2)),
                "lecciones": lessons,
            }
        )
    return {
        "schema": "curriculum-master/1",
        "course": "en",
        "curriculumScale": "client-10-levels-v1",
        "source": "OneLingo_Master_Curriculum_1000_Lessons.pdf",
        "runtimeAiRequired": False,
        "levels": levels,
    }


def validate_curriculum(curriculum: dict) -> list[str]:
    errors = []
    levels = curriculum.get("levels", [])
    if len(levels) != 10:
        errors.append(f"se esperaban 10 niveles; hay {len(levels)}")
    ids = set()
    for expected_level, level in enumerate(levels, 1):
        if level.get("nivel") != expected_level:
            errors.append(f"nivel fuera de orden: {level.get('nivel')}")
        lessons = level.get("lecciones", [])
        if len(lessons) != 100:
            errors.append(
                f"nivel {expected_level}: se esperaban 100 lecciones; hay {len(lessons)}"
            )
        for expected_lesson, lesson in enumerate(lessons, 1):
            if lesson.get("numero") != expected_lesson:
                errors.append(
                    f"nivel {expected_level}: lección fuera de orden {lesson.get('numero')}"
                )
            lesson_id = lesson.get("id")
            if lesson_id in ids:
                errors.append(f"ID duplicado: {lesson_id}")
            ids.add(lesson_id)
            for field in (
                "titulo",
                "tema",
                "contenido",
                "estructuras",
                "practicaEditorial",
                "aplicacionReal",
                "resultado",
            ):
                if not str(lesson.get(field, "")).strip():
                    errors.append(f"{lesson_id}: campo vacío {field}")
            canonical_lesson = json.dumps(lesson, ensure_ascii=False, sort_keys=True)
            if re.search(r"\bAI\b", canonical_lesson, re.I):
                errors.append(f"{lesson_id}: todavía depende de IA: {canonical_lesson}")
    if len(ids) != 1000:
        errors.append(f"se esperaban 1.000 IDs únicos; hay {len(ids)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    curriculum = parse_curriculum(_extract_text(args.source))
    errors = validate_curriculum(curriculum)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(curriculum, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("OK: 10 niveles, 1.000 lecciones, 0 errores")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
