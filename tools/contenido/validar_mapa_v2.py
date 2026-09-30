#!/usr/bin/env python3
"""Valida un mapa editorial v2 de Inglés (100 clases, 20 bloques de 5 fases).

Uso: python3 tools/contenido/validar_mapa_v2.py assets/contenido/en/plan-editorial/mapa-n4-editorial-v2.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FASES = ["input", "form", "comprehension", "production", "transfer"]
CEFR = {3: "B1", 4: "B1", 5: "B2", 6: "B2", 7: "B2", 8: "C1", 9: "C1", 10: "C1"}


def validar(path: Path) -> list[str]:
    errores: list[str] = []
    m = json.loads(path.read_text(encoding="utf-8"))
    nivel = m.get("level")

    def err(msg: str) -> None:
        errores.append(msg)

    if m.get("schema") != "onelingo.editorial.map.v2":
        err("schema debe ser onelingo.editorial.map.v2")
    if m.get("course") != "en" or nivel not in CEFR:
        err("course/level inválidos")
        return errores
    if m.get("cefr") != CEFR[nivel]:
        err(f"cefr debe ser {CEFR[nivel]}")
    if m.get("runtimeAi") is not False or m.get("phaseCycle") != FASES:
        err("runtimeAi false y phaseCycle requeridos")
    clases = m.get("classes") or []
    bloques = m.get("blocks") or []
    if len(clases) != 100 or len(bloques) != 20:
        err(f"se esperan 100 clases y 20 bloques ({len(clases)}/{len(bloques)})")
    conceptos: set[str] = set()
    titulos: set[str] = set()
    for i, c in enumerate(clases, 1):
        cid = f"en.n{nivel}.class-{i:02d}"
        donde = c.get("id", f"#{i}")
        if c.get("id") != cid:
            err(f"{donde}: id esperado {cid}")
        previo = f"en.n{nivel - 1}.class-100" if i == 1 else f"en.n{nivel}.class-{i - 1:02d}"
        if c.get("prerequisites") != [previo]:
            err(f"{cid}: prerequisites debe ser [{previo}]")
        if c.get("block") != (i - 1) // 5 + 1 or c.get("position") != (i - 1) % 5 + 1:
            err(f"{cid}: block/position incorrectos")
        if c.get("phase") != FASES[(i - 1) % 5]:
            err(f"{cid}: phase debe ser {FASES[(i - 1) % 5]}")
        t = c.get("title") or {}
        if not (t.get("en") and t.get("es")):
            err(f"{cid}: title en/es")
        elif t["es"].casefold() in titulos:
            err(f"{cid}: título repetido «{t['es']}»")
        else:
            titulos.add(t["es"].casefold())
        cs = c.get("concepts") or []
        if len(cs) != 1 or not re.fullmatch(rf"n{nivel}-[a-z0-9-]+-\d", cs[0] or ""):
            err(f"{cid}: concepts debe ser [\"n{nivel}-<tema>-<k>\"]")
        elif cs[0] in conceptos:
            err(f"{cid}: concepto repetido {cs[0]}")
        else:
            conceptos.add(cs[0])
        for campo in ("theme", "themeEs"):
            if not c.get(campo):
                err(f"{cid}: falta {campo}")
        if not c.get("languageFocus"):
            err(f"{cid}: falta languageFocus")
        if not (c.get("canDo") or {}).get("es"):
            err(f"{cid}: falta canDo.es")
        if not (c.get("assessment") or {}).get("taskEs"):
            err(f"{cid}: falta assessment.taskEs")
        if c.get("cefr") != CEFR[nivel] or c.get("level") != nivel:
            err(f"{cid}: cefr/level")
    for j, b in enumerate(bloques, 1):
        esperado = [f"en.n{nivel}.class-{k:02d}" for k in range(5 * j - 4, 5 * j + 1)]
        if b.get("number") != j or b.get("classIds") != esperado:
            err(f"bloque {j}: number/classIds")
        if not (b.get("theme") and b.get("themeEs") and b.get("outcomeEs")):
            err(f"bloque {j}: theme/themeEs/outcomeEs")
    return errores


def main(argv: list[str]) -> int:
    fallos = 0
    for a in argv:
        e = validar(Path(a))
        fallos += len(e)
        print(f"{a}: {len(e)} error(es)")
        for x in e[:40]:
            print("  ", x)
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
