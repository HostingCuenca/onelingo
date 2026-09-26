#!/usr/bin/env python3
"""Regenera docs/claude-educacion/MAPA_CURRICULAR.md desde las rutas (esquema 2).

Uso: python3 tools/generar_mapa_curricular.py
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
IDIOMAS = [("en", "Inglés"), ("es", "Español"), ("fr", "Francés"), ("de", "Alemán"),
           ("pt", "Portugués (BR)"), ("it", "Italiano"), ("zh", "Chino mandarín"),
           ("ja", "Japonés"), ("ko", "Coreano"), ("ru", "Ruso")]
ENSENAR = {"explicacion", "ejemplos", "vocabulario", "patron"}
PRACTICA = {"practica_guiada", "practica_independiente", "situacion"}


def texto(t, apoyo):
    return t.get(apoyo) or next(iter(t.values()), "")


def main():
    out = [
        "# Mapa curricular — índice maestro de unidades", "",
        "Generado con `python3 tools/generar_mapa_curricular.py` desde `assets/contenido/<idioma>/ruta/`. "
        "PROBADO = pasa `tools/validar_ruta.py` y `test/ruta_contenido_test.dart`; «inicial» = sin revisión nativa.",
        "Enseña / Practica / Evalúa = pasos de enseñanza / ítems de práctica (guiada + independiente + situación) / ítems de evaluación.",
        "",
        "Escala interna (DEC-002): 0 = Fundamentos (Pre-A1) · 1–2 A1 · 3–4 A2 · 5–6 B1 · 7–8 B2 · 9–10 C1 · C2 planificado. "
        "Plan de A1 de inglés: [PLAN_A1_INGLES.md](PLAN_A1_INGLES.md).", "",
    ]
    total = 0
    for code, nombre in IDIOMAS:
        base = RAIZ / "assets" / "contenido" / code / "ruta"
        curso = json.loads((base / "curso.json").read_text(encoding="utf-8"))
        apoyo, rev = curso["apoyoPredeterminado"], curso["revision"]
        estado = "PROBADO" if rev == "revisada" else "PROBADO (inicial)"
        out += [f"## {nombre} (`{code}`) · apoyo `{apoyo}` · revisión {rev}", ""]
        for m in curso["modulos"]:
            archivo = base / m["archivo"]
            if not archivo.exists():
                out += [f"### {texto(m['titulo'], apoyo)} — `{m['archivo']}` AUSENTE", ""]
                continue
            datos = json.loads(archivo.read_text(encoding="utf-8"))
            out += [f"### {texto(m['titulo'], apoyo)} · nivel `{m['nivel']}` · "
                    f"[{m['archivo']}](../../assets/contenido/{code}/ruta/{m['archivo']})", "",
                    "| ID | Nivel | CEFR | Tema | Prerrequisitos | Estado | Enseña | Practica | Evalúa |",
                    "|---|---:|---|---|---|---|---:|---:|---:|"]
            for u in datos["unidades"]:
                pasos = u["pasos"]
                ens = sum(1 for p in pasos if p["tipo"] in ENSENAR)
                pra = sum(len(p.get("items", [])) for p in pasos if p["tipo"] in PRACTICA)
                eva = sum(len(p.get("items", [])) for p in pasos if p["tipo"] == "evaluacion")
                pre = ", ".join(p.split(".")[-1] for p in u["prerequisitos"]) or "—"
                out.append(f"| `{u['id']}` | {u['nivelInterno']} | {u['cefr']} | "
                           f"{texto(u['titulo'], apoyo)} | {pre} | {estado} | {ens} | {pra} | {eva} |")
                total += 1
            out.append("")
    out += [f"Total: {total} unidades implementadas.", "",
            "## Diseñado, no implementado", "",
            "Grafo gramatical inglés pre-A1→C2 (111 nodos `en-g-*`) y mapas A2–C2 de los otros 9 idiomas: "
            "[auditoria/A-curriculo-gramatica.md](auditoria/A-curriculo-gramatica.md). "
            "Las 50 situaciones: [auditoria/B-vocabulario-situaciones.md](auditoria/B-vocabulario-situaciones.md)."]
    (RAIZ / "docs" / "claude-educacion" / "MAPA_CURRICULAR.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{total} unidades")


if __name__ == "__main__":
    main()
