#!/usr/bin/env python3
"""Mide la preparación real del currículo inglés sin confundir diseño y publicación."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EN = ROOT / "assets" / "contenido" / "en"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    master = read_json(EN / "curriculo-master.json")
    course = read_json(EN / "ruta" / "curso.json")
    activation = read_json(EN / "exercise-activation.json")
    source_lessons = [
        lesson
        for level in master.get("levels", [])
        for lesson in level.get("lecciones", [])
    ]
    editorial_states = Counter(
        lesson.get("estadoEditorial", "sin_estado") for lesson in source_lessons
    )
    route_units = []
    for module in course.get("modulos", []):
        data = read_json(EN / "ruta" / module["archivo"])
        route_units.extend(data.get("unidades", []))
    route_by_level = Counter(unit.get("nivelInterno") for unit in route_units)

    library_path = EN / "exercise-library.json"
    library = read_json(library_path) if library_path.exists() else {"units": {}}
    library_units = library.get("units", {})
    pool_coverage = Counter()
    for unit in library_units.values():
        for pool, references in unit.get("pools", {}).items():
            if references:
                pool_coverage[pool] += 1
    active_states = Counter(activation.get("units", {}).values())

    print("Inglés — estado editorial verificable")
    print(f"Especificaciones fuente: {len(source_lessons)}/1000")
    print("Estados fuente:", dict(sorted(editorial_states.items())))
    print(f"Unidades de ruta actuales: {len(route_units)}")
    print("Ruta por nivel interno:", dict(sorted(route_by_level.items())))
    print(f"Unidades en biblioteca: {len(library_units)}")
    print("Cobertura por pool:", dict(sorted(pool_coverage.items())))
    print("Activación:", dict(sorted(active_states.items())))

    errors = []
    if len(master.get("levels", [])) != 10 or len(source_lessons) != 1000:
        errors.append("el manifiesto maestro no contiene 10 × 100")
    if master.get("runtimeAiRequired") is not False:
        errors.append("la ruta base no debe requerir IA")
    if master.get("curriculumScale") != "client-10-levels-v1":
        errors.append("el manifiesto maestro no declara la escala cliente")
    if re.search(r"\bAI\b|OpenAI|tutor", json.dumps(master), re.IGNORECASE):
        errors.append("el manifiesto maestro todavía contiene una dependencia de IA")
    if any(value not in {"legacy", "shadow", "active"} for value in active_states):
        errors.append("estado de activación desconocido")
    for unit_id, state in activation.get("units", {}).items():
        if state in {"shadow", "active"} and unit_id not in library_units:
            errors.append(f"{unit_id}: activada sin existir en biblioteca")
        if state == "active" and not library_units[unit_id]["pools"].get("review"):
            errors.append(f"{unit_id}: activa sin pool review")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Errores estructurales: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
