#!/usr/bin/env python3
"""Estructura el mapa editorial N1 aprobado sin convertirlo en contenido."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "assets" / "contenido" / "en" / "plan-editorial"
SOURCE = ROOT / "docs" / "claude-educacion" / "PLAN_NIVEL1_INGLES_100.md"


def main() -> int:
    scale = json.loads((PLAN / "escala-cliente.json").read_text(encoding="utf-8"))
    level = next(entry for entry in scale["levels"] if entry["level"] == 1)
    classes = []
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^(\d+)\.\s+(.+?)\s+—\s+([CDRN])(.*)$", line)
        if not match:
            continue
        number = int(match.group(1))
        detail = match.group(4).strip().rstrip(".")
        classes.append(
            {
                "id": f"en.n1.l{number:03d}",
                "nivel": 1,
                "banda_mcer": level["cefrBand"],
                "etiqueta_nivel": level["label"],
                "bloque": (number - 1) // 5 + 1,
                "clase_en_bloque": (number - 1) % 5 + 1,
                "titulo_editorial": match.group(2).replace("`", ""),
                "estrategia_origen": match.group(3),
                "referencias_legacy": re.findall(r"`([^`]+)`", detail),
                "nota_editorial": re.sub(r"[`()]+", "", detail).strip(" ,;"),
                "prerrequisitos": [
                    "en.f0.presentarse"
                    if number == 1
                    else f"en.n1.l{number - 1:03d}"
                ],
                "requiere_redaccion": True,
                "estado": "planificado",
            }
        )
    if [entry["id"] for entry in classes] != [
        f"en.n1.l{number:03d}" for number in range(1, 101)
    ]:
        raise SystemExit("ERROR: el mapa N1 no contiene exactamente las clases 1-100")
    output = {
        "schema": "onelingo.editorial-plan.v1",
        "idioma": "en",
        "curriculumScale": scale["id"],
        "nivel": 1,
        "banda_mcer": level["cefrBand"],
        "etiqueta_nivel": level["label"],
        "total_clases": 100,
        "total_bloques": 20,
        "estado": "planificado",
        "nota": "Mapa editorial aprobado; no constituye contenido publicable ni activa la ruta.",
        "clases": classes,
    }
    (PLAN / "mapa-n1.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    higher = json.loads(
        (PLAN / "mapa-ingles-n2-n10.json").read_text(encoding="utf-8")
    )
    aggregate = {
        "schema": "onelingo.editorial-plan.v1",
        "idioma": "en",
        "niveles": "N1-N10",
        "curriculumScale": scale["id"],
        "total_clases": 1000,
        "total_bloques": 200,
        "estado": "planificado",
        "nota": "Índice completo de planificación; no equivale a clases redactadas o publicables.",
        "clases": classes + higher["clases"],
    }
    (PLAN / "mapa-ingles-n1-n10.json").write_text(
        json.dumps(aggregate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("OK: N1, 100 clases; agregado inglés, 1.000 clases planificadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
