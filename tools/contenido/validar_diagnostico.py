#!/usr/bin/env python3
"""Valida (y compila) el banco del diagnóstico de ubicación v2 de inglés.

Uso:
  python3 tools/contenido/validar_diagnostico.py assets/contenido/en/plan-editorial/diagnostico/n4.json
  python3 tools/contenido/validar_diagnostico.py --compilar   # valida los 10 niveles y escribe el banco

Reglas en docs/claude-educacion/DIAGNOSTICO_V2.md.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import construir_bloque as cb  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FUENTES = ROOT / "assets/contenido/en/plan-editorial/diagnostico"
SALIDA = ROOT / "assets/contenido/en/diagnostico-v2.json"

HABILIDADES = {"escucha": ("escuchar",), "lectura": ("elegir",), "gramatica": ("elegir", "completar"),
               "vocabulario": ("elegir", "completar"), "escritura": ("escribir",)}
POR_HABILIDAD = {"escucha": 4, "lectura": 4, "gramatica": 4, "vocabulario": 4, "escritura": 2}
LECTURA = {1: (15, 35), 2: (25, 45), 3: (35, 60), 4: (45, 70), 5: (55, 85), 6: (65, 95),
           7: (75, 110), 8: (85, 120), 9: (95, 130), 10: (105, 150)}
ESCUCHA = {1: (5, 15), 2: (8, 20), 3: (12, 25), 4: (15, 30), 5: (20, 40), 6: (25, 45),
           7: (30, 55), 8: (35, 60), 9: (40, 70), 10: (45, 80)}
MAX_CORRECTA_MAS_LARGA = 0.35
POSICION = re.compile(r"\b(primer[ao]?|segund[ao]|tercer[ao]?|cuart[ao]|últim[ao])\s+(opci[oó]n|respuesta)", re.I)


def n_palabras(t: str) -> int:
    return len(cb.PALABRA.findall(str(t or "")))


def es_texto(v) -> str:
    return v.get("es", "") if isinstance(v, dict) else ""


def validar(path: Path) -> tuple[list[str], list[dict]]:
    errores: list[str] = []
    doc = json.loads(path.read_text(encoding="utf-8"))
    nivel = doc.get("nivel")
    if nivel not in LECTURA:
        return [f"{path.name}: «nivel» debe ser 1–10"], []
    items = doc.get("items") or []
    lex = cb.lexico_previo(nivel, 101)
    ids, consignas = set(), set()
    cuenta = {h: 0 for h in HABILIDADES}
    con_opciones = delata = 0
    for k, it in enumerate(items, 1):
        iid = it.get("id") or f"#{k}"
        e = lambda m: errores.append(f"{iid}: {m}")  # noqa: E731
        h, f = it.get("habilidad"), it.get("formato")
        if h not in HABILIDADES:
            e("habilidad inválida"); continue
        cuenta[h] += 1
        if it.get("nivel") != nivel:
            e(f"nivel debe ser {nivel}")
        if f not in HABILIDADES[h]:
            e(f"formato {f} no válido para {h}")
        esperado = f"dx.en.n{nivel}.{h}.{cuenta[h]}"
        if it.get("id") != esperado:
            e(f"id esperado {esperado}")
        if iid in ids:
            e("id duplicado")
        ids.add(iid)
        consigna, feedback = es_texto(it.get("consigna")), es_texto(it.get("feedback"))
        if not consigna or len(consigna) > 90:
            e("consigna.es obligatoria y ≤ 90 caracteres")
        if consigna.casefold() in consignas:
            e("consigna repetida")
        consignas.add(consigna.casefold())
        if not feedback:
            e("falta feedback.es")
        if POSICION.search(feedback):
            e("el feedback no puede citar la posición de una opción")
        textos_en: list[str] = []
        if h == "lectura":
            lo, hi = LECTURA[nivel]
            n = n_palabras(it.get("texto", ""))
            if not lo <= n <= hi:
                e(f"el pasaje tiene {n} palabras (N{nivel}: {lo}–{hi})")
            textos_en.append(it.get("texto", ""))
        if h == "escucha":
            lo, hi = ESCUCHA[nivel]
            n = n_palabras(it.get("audio", ""))
            if not lo <= n <= hi:
                e(f"el audio tiene {n} palabras (N{nivel}: {lo}–{hi})")
            if it.get("texto"):
                e("escucha: sin `texto` (se respondería leyendo)")
            textos_en.append(it.get("audio", ""))
        if h in ("gramatica", "vocabulario") and it.get("texto"):
            textos_en.append(it["texto"])
        op = it.get("opciones")
        if f in ("elegir", "escuchar") or (f == "completar"):
            if not isinstance(op, list) or not 3 <= len(op) <= 4 or not all(isinstance(o, str) and o.strip() for o in op):
                e("3–4 opciones (texto inglés)")
                op = []
            elif len({o.strip().casefold() for o in op}) != len(op):
                e("opciones repetidas")
            r = it.get("respuesta")
            if not isinstance(r, int) or not 0 <= r < max(len(op), 1):
                e("respuesta debe ser el índice de la opción correcta")
            elif op:
                con_opciones += 1
                largos = [n_palabras(o) for o in op]
                delata += largos[r] == max(largos) and largos.count(max(largos)) == 1
            textos_en += op or []
            if f == "completar" and it.get("texto", "").count("___") != 1:
                e("completar: `texto` con exactamente un ___")
        if f == "escribir":
            modelo = it.get("respuesta") or ""
            acept = it.get("aceptadas") or []
            ev = it.get("evidenciasEscritura") or []
            lo, hi = it.get("minimoPalabras"), it.get("maximoPalabras")
            if not modelo or not acept:
                e("escribir: respuesta modelo y ≥1 aceptada")
            if len(ev) < 3 or any(not g or any(len(x.split()) < 2 for x in g) for g in ev):
                e("escribir: ≥3 grupos de evidencias, cada evidencia de 2+ palabras")
            if not (isinstance(lo, int) and isinstance(hi, int) and 0 < lo < hi):
                e("escribir: minimoPalabras y maximoPalabras")
            else:
                rub = {"palabras": [lo, hi], "evidencias": ev}
                for t in [modelo, *acept]:
                    if not cb.cumple_rubrica(t, rub):
                        e(f"escribir: el texto no supera su rúbrica: «{t[:60]}…»")
            textos_en.append(modelo)
            if it.get("texto") and it.get("textoIdioma", "en") == "en":
                textos_en.append(it["texto"])
        faltan = {w for t in textos_en for w in cb.palabras(t) if not cb.conocida(w, lex)}
        if faltan:
            e(f"palabras no enseñadas hasta el final de N{nivel}: {', '.join(sorted(faltan))}")
    for h, n in POR_HABILIDAD.items():
        if cuenta[h] != n:
            errores.append(f"{path.name}: {h} tiene {cuenta[h]} ítems (se esperan {n})")
    if con_opciones and delata / con_opciones > MAX_CORRECTA_MAS_LARGA:
        errores.append(f"{path.name}: la correcta es la única opción más larga en {delata}/{con_opciones} ítems "
                       f"(máx. {100 * MAX_CORRECTA_MAS_LARGA:.0f} %)")
    return errores, items


def main(argv: list[str]) -> int:
    compilar = "--compilar" in argv
    rutas = [Path(a) for a in argv if not a.startswith("--")]
    if compilar or not rutas:
        rutas = [FUENTES / f"n{n}.json" for n in range(1, 11)]
    total_err, banco = 0, []
    for p in rutas:
        if not p.exists():
            print(f"{p.name}: no existe"); total_err += 1; continue
        err, items = validar(p)
        if compilar and (json.loads(p.read_text(encoding="utf-8")).get("review") or {}).get("status") != "GO":
            err.append(f"{p.name}: sin revisión independiente GO")
        total_err += len(err)
        print(f"{p.name}: {'OK' if not err else f'{len(err)} error(es)'} · {len(items)} ítems")
        for x in err[:40]:
            print("  ERROR", x)
        for it in items:
            # La vista de ítems corrige «completar» por texto: se exporta la
            # opción correcta como respuesta (la fuente guarda el índice).
            if it.get("formato") == "completar" and isinstance(it.get("respuesta"), int):
                it = {**it, "respuesta": it["opciones"][it["respuesta"]],
                      "aceptadas": [it["opciones"][it["respuesta"]]]}
            banco.append(it)
    if compilar:
        if total_err:
            print("No se compila: hay errores.")
            return 1
        SALIDA.write_text(json.dumps({"schema": "onelingo.diagnostico.v2", "idioma": "en", "items": banco},
                                     ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"escrito {SALIDA.relative_to(ROOT)} · {len(banco)} ítems")
    return 1 if total_err else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
