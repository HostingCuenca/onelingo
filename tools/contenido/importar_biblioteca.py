#!/usr/bin/env python3
"""Importa ejercicios del esquema 2 a exercise-library/1.

El modo predeterminado es dry-run: escribe únicamente informes. ``--apply``
requiere el mismo manifiesto previamente revisado y nunca activa unidades.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import tempfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POOL_BY_STEP = {
    "practica_guiada": "practiceGuided",
    "practica_independiente": "practice",
    "situacion": "practice",
    "evaluacion": "evaluation",
}


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def slug(value: str) -> str:
    clean = value.lower().replace("_", "-")
    clean = re.sub(r"[^a-z0-9.-]+", "-", clean)
    return re.sub(r"-+", "-", clean).strip("-") or "item"


def load_units(course: str) -> tuple[dict, list[tuple[str, dict]]]:
    base = ROOT / "assets" / "contenido" / course / "ruta"
    index = json.loads((base / "curso.json").read_text(encoding="utf-8"))
    units = []
    for module in index.get("modulos", []):
        path = base / module["archivo"]
        data = json.loads(path.read_text(encoding="utf-8"))
        for unit in data.get("unidades", []):
            units.append((str(path.relative_to(ROOT)), unit))
    units.sort(key=lambda entry: (entry[1].get("orden", 0), entry[1]["id"]))
    return index, units


def answer_from(item: dict) -> dict:
    raw = item.get("respuesta")
    answer = {"index": raw} if isinstance(raw, int) else {"text": raw or ""}
    if item.get("aceptadas"):
        answer["accepted"] = item["aceptadas"]
    if item.get("tokens"):
        answer["tokens"] = item["tokens"]
    return answer


def choices_from(item: dict) -> list[dict]:
    return [{"text": choice} for choice in item.get("opciones", [])]


def build_library(course: str) -> tuple[dict, list[dict], list[dict], list[str]]:
    index, source_units = load_units(course)
    units = {}
    families = []
    rows = []
    migration = []
    errors = []
    variant_ids = set()
    fingerprints = defaultdict(list)

    for source_file, unit in source_units:
        unit_id = unit["id"]
        pools = {name: [] for name in ("teaching", "practiceGuided", "practice", "evaluation", "review")}
        for step in unit.get("pasos", []):
            pool = POOL_BY_STEP.get(step.get("tipo"))
            if pool is None:
                continue
            for position, item in enumerate(step.get("items", [])):
                family_id = ".".join(
                    (
                        "ex",
                        "onelingo",
                        course,
                        slug(unit_id.removeprefix(f"{course}.")),
                        slug(step.get("id", "step")),
                        slug(item.get("id", f"item-{position + 1}")),
                    )
                )
                variant_id = f"{family_id}:v1:{pool}"
                if variant_id in variant_ids:
                    errors.append(f"duplicate variant id: {variant_id}")
                    continue
                variant_ids.add(variant_id)
                concept = str(unit.get("concepto", unit_id))
                semantic = {
                    "format": item.get("formato", ""),
                    "prompt": item.get("consigna", {}),
                    "answer": answer_from(item),
                    "choices": choices_from(item),
                    "teaches": [concept] if pool == "practiceGuided" else [],
                    "requires": [] if pool == "practiceGuided" else [concept],
                    "question": item.get("pregunta"),
                    "audio": item.get("audio"),
                    "text": item.get("texto"),
                    "pairs": item.get("pares", []),
                }
                content_hash = sha256(semantic)
                origin = {
                    "kind": "schema2-import",
                    "sourceFile": source_file,
                    "sourceUnitId": unit_id,
                    "sourceStepId": step.get("id"),
                    "sourceItemIndex": position,
                    "legacyKey": f"{unit_id}:{step.get('id')}:{item.get('id')}",
                    "feedback": item.get("feedback", {}),
                    **({"hint": item["pista"]} if "pista" in item else {}),
                    **({"question": item["pregunta"]} if "pregunta" in item else {}),
                    **({"audio": item["audio"]} if "audio" in item else {}),
                    **({"text": item["texto"]} if "texto" in item else {}),
                    **({"pairs": item["pares"]} if "pares" in item else {}),
                }
                variant = {
                    "id": variant_id,
                    "format": semantic["format"],
                    "prompt": semantic["prompt"],
                    "answer": semantic["answer"],
                    "choices": semantic["choices"],
                    "teaches": semantic["teaches"],
                    "requires": semantic["requires"],
                    "origin": origin,
                    "contentHash": content_hash,
                }
                families.append(
                    {
                        "id": family_id,
                        "revision": 1,
                        "concepts": [concept],
                        "skills": unit.get("habilidades", []),
                        "variants": [variant],
                    }
                )
                pools[pool].append(variant_id)
                fingerprints[content_hash].append(
                    {"unit": unit_id, "pool": pool, "variantId": variant_id}
                )
                legacy_key = origin["legacyKey"]
                migration.append(
                    {
                        "legacyKey": legacy_key,
                        "variantId": variant_id,
                        "confidence": "exact",
                    }
                )
                rows.append(
                    {
                        "sourceFile": source_file,
                        "unitId": unit_id,
                        "stepId": step.get("id"),
                        "itemId": item.get("id"),
                        "pool": pool,
                        "familyId": family_id,
                        "variantId": variant_id,
                        "contentHash": content_hash,
                        "status": "imported",
                    }
                )
        units[unit_id] = {
            "concepts": [str(unit.get("concepto", unit_id))],
            "skills": unit.get("habilidades", []),
            "prerequisites": unit.get("prerequisitos", []),
            "pools": pools,
        }

    families.sort(key=lambda family: family["id"])
    duplicates = [entries for entries in fingerprints.values() if len(entries) > 1]
    for entries in duplicates:
        incompatible = {entry["pool"] for entry in entries}
        if len(incompatible) > 1:
            errors.append(
                "same content in incompatible pools: "
                + ", ".join(entry["variantId"] for entry in entries)
            )
    library = {
        "schema": "exercise-library/1",
        "libraryId": "onelingo",
        "version": index.get("version", "0"),
        "course": course,
        "units": dict(sorted(units.items())),
        "families": families,
    }
    return library, rows, migration, errors


def write_reports(output: Path, library: dict, rows: list[dict], migration: list[dict], errors: list[str]) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    duplicate_groups = defaultdict(list)
    for family in library["families"]:
        variant = family["variants"][0]
        duplicate_groups[variant["contentHash"]].append(variant["id"])
    duplicates = [values for values in duplicate_groups.values() if len(values) > 1]
    manifest = {
        "schema": "exercise-import-manifest/1",
        "course": library["course"],
        "libraryVersion": library["version"],
        "libraryHash": sha256(library),
        "units": len(library["units"]),
        "families": len(library["families"]),
        "variants": len(rows),
        "errors": len(errors),
    }
    payloads = {
        "manifest.json": manifest,
        "duplicates.json": {"groups": duplicates},
        "integrity.json": {"errors": errors, "warnings": []},
        "migration-map.json": {"aliases": migration},
        "progress-impact.json": {
            "deletesProgress": False,
            "changesApproval": False,
            "changesRetention": False,
            "aliases": len(migration),
        },
        "exercise-library.json": library,
    }
    for name, payload in payloads.items():
        (output / name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    with (output / "classification.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else ["status"])
        writer.writeheader()
        writer.writerows(rows)
    return manifest


def apply_library(report_dir: Path, approved_manifest: Path, course: str) -> None:
    reported = json.loads((report_dir / "manifest.json").read_text(encoding="utf-8"))
    approved = json.loads(approved_manifest.read_text(encoding="utf-8"))
    if canonical(reported) != canonical(approved):
        raise SystemExit("ERROR: el manifiesto aprobado no coincide con el dry-run")
    if reported.get("errors"):
        raise SystemExit("ERROR: no se puede aplicar un manifiesto con errores")
    source = report_dir / "exercise-library.json"
    target = ROOT / "assets" / "contenido" / course / "exercise-library.json"
    with tempfile.NamedTemporaryFile("w", dir=target.parent, delete=False, encoding="utf-8") as stream:
        stream.write(source.read_text(encoding="utf-8"))
        temporary = Path(stream.name)
    temporary.replace(target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", default="en")
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--approved-manifest", type=Path)
    args = parser.parse_args()
    library, rows, migration, errors = build_library(args.course)
    manifest = write_reports(args.report, library, rows, migration, errors)
    print(canonical(manifest))
    if args.apply:
        if args.approved_manifest is None:
            raise SystemExit("ERROR: --apply requiere --approved-manifest")
        apply_library(args.report, args.approved_manifest, args.course)
        print("APPLIED: library written; activation unchanged")
    else:
        print("DRY-RUN: no product assets changed")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
