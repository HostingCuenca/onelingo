#!/usr/bin/env python3
"""Valida los mapas ingleses N1-N10 contra escala y fuentes independientes."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "assets" / "contenido" / "en" / "plan-editorial"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    scale = load(PLAN / "escala-cliente.json")
    master = load(ROOT / "assets" / "contenido" / "en" / "curriculo-master.json")
    by_level = {entry["level"]: entry for entry in scale["levels"]}
    errors = []
    ids = set()
    total = 0
    n1 = load(PLAN / "mapa-n1.json")
    if len(n1.get("clases", [])) != 100:
        errors.append("N1 no contiene 100 clases")
    for number, lesson in enumerate(n1.get("clases", []), 1):
        expected_id = f"en.n1.l{number:03d}"
        if lesson.get("id") != expected_id:
            errors.append(f"N1.{number}: ID incorrecto")
        if lesson.get("estado") != "planificado":
            errors.append(f"{expected_id}: estado no planificado")
        ids.add(expected_id)
        total += 1
    for level in range(2, 11):
        plan = load(PLAN / f"mapa-n{level}.json")
        source = master["levels"][level - 1]["lecciones"]
        classes = plan.get("clases", [])
        if len(classes) != 100:
            errors.append(f"N{level}: {len(classes)} clases")
        expected_scale = by_level[level]
        if plan.get("curriculumScale") != scale["id"]:
            errors.append(f"N{level}: escala incorrecta")
        if plan.get("banda_mcer") != expected_scale["cefrBand"]:
            errors.append(f"N{level}: banda MCER incorrecta")
        if plan.get("etiqueta_nivel") != expected_scale["label"]:
            errors.append(f"N{level}: etiqueta incorrecta")
        for number, (lesson, original) in enumerate(zip(classes, source), 1):
            total += 1
            expected_id = f"en.n{level}.l{number:03d}"
            if lesson.get("id") != expected_id:
                errors.append(f"N{level}.{number}: ID {lesson.get('id')}")
            if expected_id in ids:
                errors.append(f"ID duplicado: {expected_id}")
            ids.add(expected_id)
            if lesson.get("titulo_fuente") != original["titulo"]:
                errors.append(f"{expected_id}: título no trazable")
            if lesson.get("tema_fuente") != original["tema"]:
                errors.append(f"{expected_id}: tema no trazable")
            if lesson.get("resultado_fuente") != original["resultado"]:
                errors.append(f"{expected_id}: resultado no trazable")
            previous = (
                f"en.n{level}.l{number - 1:03d}"
                if number > 1
                else f"en.n{level - 1}.l100"
            )
            if lesson.get("prerrequisitos") != [previous]:
                errors.append(f"{expected_id}: prerrequisito incorrecto")
            if lesson.get("estado") != "planificado":
                errors.append(f"{expected_id}: estado no planificado")
            if re.search(r"\bAI\b|OpenAI|tutor", json.dumps(lesson), re.I):
                errors.append(f"{expected_id}: dependencia de IA")
            has_claim = bool(
                re.search(r"native-like|bilingual|\bC2\b", json.dumps(original), re.I)
            )
            if lesson.get("requiere_reescritura_claims") is not has_claim:
                errors.append(f"{expected_id}: flag de claim incorrecto")
    if total != 1000 or len(ids) != 1000:
        errors.append(f"cobertura incorrecta: {total} clases, {len(ids)} IDs")
    aggregate = load(PLAN / "mapa-ingles-n1-n10.json")
    aggregate_ids = [entry.get("id") for entry in aggregate.get("clases", [])]
    if len(aggregate_ids) != 1000 or len(set(aggregate_ids)) != 1000:
        errors.append("agregado inglés no contiene 1.000 IDs únicos")
    if any(entry["cefrBand"] == "C2" for entry in scale["levels"]):
        errors.append("la escala promete C2")
    if scale["claims"] != {
        "officialCertification": False,
        "level10IsC2": False,
        "level10GuaranteesBilingualism": False,
    }:
        errors.append("claims de escala alterados")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("OK: N1-N10, 1.000 clases planificadas, escala/IDs/trazabilidad válidos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
