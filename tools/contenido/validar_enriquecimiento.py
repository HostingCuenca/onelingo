#!/usr/bin/env python3
"""Puerta automática de la capa de enriquecimiento (CONTRATO_ENRIQUECIMIENTO.md).

Comprueba estructura, coherencia con la clase compilada y heurísticas de
calidad que no dependen de juicio humano. Un archivo con errores no se
integra aunque tenga revisión ``GO`` (el compilador llama a ``validar``).

Uso: python3 tools/contenido/validar_enriquecimiento.py [archivo …]
Sin argumentos valida todos los ``enriquecimiento-*.json`` de N1–N3.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDITORIAL = ROOT / "assets/contenido/en/editorial"
SCHEMA = "onelingo.editorial.enrichment.v1"
PALABRA = re.compile(r"[A-Za-z]+(?:'[a-z]+)?")
# Metalenguaje gramatical en inglés presentado como ejemplo («Present passive
# uses…», «Although introduces contrast…»). Las órdenes sueltas («Read the
# message.») pueden ser ejemplos legítimos del imperativo: solo avisan.
METALENGUAJE = re.compile(
    r"\b(present|past|future) (simple|continuous|perfect|passive)\b"
    r"|\b(clause|participle|infinitive|gerund|auxiliary|modal verb|base form)s?\b"
    r"|\b(introduces|expresses|marks|signals) (a |an |the )?(contrast|result|reason|action|condition|sequence|past|present|future)\b",
    re.IGNORECASE,
)
INSTRUCCION = re.compile(r"^(use|place|put|compare|start from|keep|name the|make sure)\b", re.IGNORECASE)
RELLENO = ("expresión del curso", "observa el modelo", "usa el modelo de la clase")


def _palabras(texto: str) -> set[str]:
    return {w.lower() for w in PALABRA.findall(texto)}


def _raiz(palabra: str) -> str:
    for sufijo in ("ing", "ed", "es", "s"):
        if palabra.endswith(sufijo) and len(palabra) - len(sufijo) >= 3:
            return palabra[: -len(sufijo)]
    return palabra


def _texto(valor, donde: str, errores: list[str], minimo: int = 1) -> str:
    if not isinstance(valor, str) or len(valor.strip()) < minimo:
        errores.append(f"{donde}: texto vacío o demasiado corto")
        return ""
    if any(r in valor.lower() for r in RELLENO):
        errores.append(f"{donde}: texto de relleno")
    return valor


def validar_clase(cid: str, e: dict, clase: dict | None) -> tuple[list[str], list[str]]:
    errores: list[str] = []
    avisos: list[str] = []
    if clase is None:
        return [f"{cid}: la clase no existe en el runtime"], avisos

    exp = e.get("explicacion") or {}
    _texto(exp.get("titulo"), f"{cid}.explicacion.titulo", errores, 3)
    texto = _texto(exp.get("texto"), f"{cid}.explicacion.texto", errores, 80)
    if texto and len(texto) > 650:
        avisos.append(f"{cid}.explicacion.texto: {len(texto)} caracteres (largo para móvil; ideal ≤ 550)")

    patron = e.get("patron")
    if patron is not None:
        _texto(patron.get("texto"), f"{cid}.patron.texto", errores)
        segmentos = patron.get("formula") or []
        if not 2 <= len(segmentos) <= 6:
            errores.append(f"{cid}.patron: {len(segmentos)} segmentos (2–6)")
        for i, s in enumerate(segmentos):
            _texto(s.get("texto"), f"{cid}.patron.formula[{i}].texto", errores)
            _texto(s.get("nota"), f"{cid}.patron.formula[{i}].nota", errores)
    else:
        avisos.append(f"{cid}: sin patrón")

    tabla = e.get("tabla")
    if tabla is not None:
        columnas = tabla.get("columnas") or []
        if any(not str(c).strip() for c in columnas):
            errores.append(f"{cid}.tabla: encabezado de columna vacío")
        for i, fila in enumerate(tabla.get("filas") or []):
            if len(fila) != len(columnas):
                errores.append(f"{cid}.tabla.filas[{i}]: {len(fila)} celdas para {len(columnas)} columnas")
            for c in fila:
                if not (c.get("texto") or c.get("apoyo")):
                    errores.append(f"{cid}.tabla.filas[{i}]: celda vacía")

    errs = e.get("erroresFrecuentes") or []
    if len(errs) != 2:
        errores.append(f"{cid}: {len(errs)} errores frecuentes (se piden 2)")
    for i, x in enumerate(errs):
        inc = _texto(x.get("incorrecto"), f"{cid}.errores[{i}].incorrecto", errores)
        cor = _texto(x.get("correcto"), f"{cid}.errores[{i}].correcto", errores)
        _texto(x.get("explicacion"), f"{cid}.errores[{i}].explicacion", errores, 15)
        if inc and cor and inc.strip(" .?!").lower() == cor.strip(" .?!").lower():
            errores.append(f"{cid}.errores[{i}]: incorrecto y correcto solo difieren en puntuación")

    sit = e.get("situacion") or {}
    _texto(sit.get("contexto"), f"{cid}.situacion.contexto", errores, 15)
    dialogo = sit.get("dialogo") or []
    if not 3 <= len(dialogo) <= 6:
        errores.append(f"{cid}.situacion: {len(dialogo)} líneas de diálogo (3–6)")
    hablantes = {l.get("hablante") for l in dialogo}
    if len(hablantes) < 2 or "Modelo" in hablantes:
        errores.append(f"{cid}.situacion: hacen falta al menos dos personajes con nombre")
    palabras_dialogo: set[str] = set()
    for i, l in enumerate(dialogo):
        palabras_dialogo |= _palabras(_texto(l.get("texto"), f"{cid}.dialogo[{i}].texto", errores))
        _texto(l.get("traduccion"), f"{cid}.dialogo[{i}].traduccion", errores)

    item = sit.get("item") or {}
    if item.get("formato") not in ("elegir", "escuchar"):
        errores.append(f"{cid}.situacion.item: formato {item.get('formato')!r}")
    if item.get("formato") == "escuchar" and not item.get("audio"):
        errores.append(f"{cid}.situacion.item: escuchar sin audio")
    # Opciones en inglés (texto) o en el idioma de apoyo ({"es": …}).
    opciones = [o.get("es", "") if isinstance(o, dict) else o for o in item.get("opciones") or []]
    if len(opciones) != 3 or len({o.strip().lower() for o in opciones}) != 3:
        errores.append(f"{cid}.situacion.item: se piden 3 opciones distintas")
    r = item.get("respuesta")
    if not isinstance(r, int) or not 0 <= r < len(opciones):
        errores.append(f"{cid}.situacion.item: respuesta fuera de rango")
    else:
        consigna = _texto(item.get("consigna"), f"{cid}.situacion.item.consigna", errores)
        _texto(item.get("feedback"), f"{cid}.situacion.item.feedback", errores)
        correcta = opciones[r]
        if correcta.lower().strip(" .") in consigna.lower():
            errores.append(f"{cid}.situacion.item: la respuesta aparece en la consigna")
        # Se responde leyendo el diálogo: la opción correcta debe apoyarse en él.
        base = {_raiz(w) for w in palabras_dialogo}
        propias = {_raiz(w) for w in _palabras(correcta)} - {"a", "the", "is", "he", "she", "it", "i"}
        if propias and len(propias & base) / len(propias) < 0.5:
            avisos.append(f"{cid}.situacion.item: la opción correcta apenas aparece en el diálogo")

    ensenanza = [p for p in clase["pasos"] if p["tipo"] == "ejemplos"]
    total = len(ensenanza[0].get("items", [])) if ensenanza else 0
    reemplazados = set()
    for i, x in enumerate(e.get("ejemplos") or []):
        k = x.get("indice")
        if not isinstance(k, int) or not 0 <= k < total:
            errores.append(f"{cid}.ejemplos[{i}]: índice {k} fuera de 0–{total - 1}")
            continue
        reemplazados.add(k)
        en = _texto(x.get("en"), f"{cid}.ejemplos[{i}].en", errores)
        _texto(x.get("es"), f"{cid}.ejemplos[{i}].es", errores)
        _texto(x.get("nota"), f"{cid}.ejemplos[{i}].nota", errores)
        if en and (METALENGUAJE.search(en) or INSTRUCCION.search(en)):
            errores.append(f"{cid}.ejemplos[{i}]: el reemplazo sigue siendo metalenguaje: {en!r}")
    # Ejemplos originales que siguen pareciendo instrucciones y no se sustituyen.
    for k, it in enumerate(ensenanza[0].get("items", []) if ensenanza else []):
        original = it.get("texto", "")
        if k in reemplazados:
            continue
        if METALENGUAJE.search(original):
            errores.append(f"{cid}: el ejemplo {k} es metalenguaje y no se sustituye: {original!r}")
        elif INSTRUCCION.search(original):
            avisos.append(f"{cid}: el ejemplo {k} parece una instrucción: {original!r}")
    return errores, avisos


def _conocidas_por_clase(unidades: dict[str, dict], ids: list[str]) -> dict[str, set[str]]:
    """Palabras que el validador de rutas da por enseñadas en cada clase
    (misma regla que tools/validar_ruta.py, sobre la cadena de clases)."""
    sys.path.insert(0, str(ROOT / "tools"))
    import validar_ruta

    curso = json.loads((ROOT / "assets/contenido/en/ruta/curso.json").read_text(encoding="utf-8"))
    libres = {w for p in curso.get("palabrasLibres", []) for w in validar_ruta.palabras(p)}
    todas = dict(unidades)
    for archivo in ("f0.json",):
        for u in json.loads((ROOT / f"assets/contenido/en/ruta/{archivo}").read_text(encoding="utf-8"))["unidades"]:
            todas[u["id"]] = u
    v = validar_ruta.Validador("en")
    return {cid: v.conocidas(todas[cid], todas) | libres for cid in ids}


def palabras_no_ensenadas(cid: str, e: dict, conocidas: set[str]) -> list[str]:
    import validar_ruta

    textos = [s.get("texto", "") for s in (e.get("patron") or {}).get("formula", [])]
    textos += [x.get("correcto", "") for x in e.get("erroresFrecuentes", [])]
    sit = e.get("situacion") or {}
    textos += [l.get("texto", "") for l in sit.get("dialogo", [])]
    item = sit.get("item") or {}
    textos += [o for o in item.get("opciones", []) if isinstance(o, str)]
    textos.append(item.get("audio") or "")
    textos += [x.get("en", "") for x in e.get("ejemplos", [])]
    faltan = set()
    for t in textos:
        faltan |= {w for w in validar_ruta.palabras(t) if not validar_ruta.conocida(w, conocidas)}
    return sorted(faltan)


def unidades_runtime() -> dict[str, dict]:
    """Clases tal como quedan sin enriquecer (los índices de `ejemplos`
    se refieren a la enseñanza original, no a una versión ya sustituida)."""
    import generar_runtime_n1 as compilador

    return {u["id"]: u for u in compilador.unenriched_units()}


def validar(path: Path, unidades: dict[str, dict] | None = None) -> tuple[list[str], list[str]]:
    unidades = unidades if unidades is not None else unidades_runtime()
    doc = json.loads(path.read_text(encoding="utf-8"))
    errores: list[str] = []
    avisos: list[str] = []
    if doc.get("schema") != SCHEMA:
        errores.append(f"{path.name}: schema {doc.get('schema')!r}")
    rango = doc.get("range") or {}
    esperadas = {
        f"en.{doc.get('level')}.class-{n:02d}"
        for n in range(rango.get("start", 0), rango.get("end", -1) + 1)
    }
    clases = doc.get("classes") or {}
    conocidas = _conocidas_por_clase(unidades, [cid for cid in clases if cid in unidades])
    if set(clases) != esperadas:
        errores.append(f"{path.name}: clases {sorted(clases)} no coinciden con el rango {sorted(esperadas)}")
    for cid, e in clases.items():
        err, av = validar_clase(cid, e, unidades.get(cid))
        if cid in conocidas:
            faltan = palabras_no_ensenadas(cid, e, conocidas[cid])
            if faltan:
                err.append(f"{cid}: palabras inglesas no enseñadas antes: {', '.join(faltan)}")
        errores += err
        avisos += av
    return errores, avisos


def main(argv: list[str]) -> int:
    rutas = [Path(a) for a in argv] or sorted(EDITORIAL.glob("n*/enriquecimiento-*.json"))
    unidades = unidades_runtime()
    fallos = 0
    for p in rutas:
        errores, avisos = validar(p, unidades)
        fallos += len(errores)
        print(f"{p.relative_to(ROOT) if p.is_absolute() else p}: {len(errores)} error(es), {len(avisos)} aviso(s)")
        for x in errores:
            print("  ERROR", x)
        for x in avisos:
            print("  aviso", x)
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
