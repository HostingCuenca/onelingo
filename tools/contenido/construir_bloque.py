#!/usr/bin/env python3
"""Construye un bloque editorial de Inglés desde el formato compacto de autoría.

Los agentes escriben solo contenido pedagógico en
``assets/contenido/en/editorial/<nivel>/autor/bloque-<ini>-<fin>.json``
(contrato: docs/claude-educacion/CONTRATO_AUTORIA_COMPACTA.md). Este script:

1. comprueba el léxico: toda palabra inglesa de ejercicios y situación debe
   estar enseñada o practicada antes, o enseñarse en la propia clase;
2. genera las clases con el esquema editorial v1 + contrato editorial-agent.v2
   (ids, hashes, metadatos de audio, remediación, evaluación acumulativa y
   posiciones de respuesta equilibradas);
3. valida el bundle con ``validar_bundle_editorial.py`` y la capa de
   enriquecimiento con ``validar_enriquecimiento.validar_clase``;
4. solo si todo pasa, escribe ``class-NN.json``, ``bundle-ini-fin.json`` y
   ``enriquecimiento-ini-fin.json`` (sin revisión: la añade el revisor).

Uso: python3 tools/contenido/construir_bloque.py assets/contenido/en/editorial/n3/autor/bloque-91-95.json [--solo-validar]
"""

from __future__ import annotations

import glob
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validar_bundle_editorial as vb  # noqa: E402
import validar_enriquecimiento as ve  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
EDITORIAL = ROOT / "assets/contenido/en/editorial"
PLAN = ROOT / "assets/contenido/en/plan-editorial"
POOLS = {"guiada": "practiceGuided", "practica": "practice", "evaluacion": "evaluation", "repaso": "review"}
PREFIX = {"practiceGuided": "pg", "practice": "p", "evaluation": "e", "review": "r"}
MINIMOS = {"practiceGuided": 3, "practice": 3, "evaluation": 4, "review": 3}
PALABRA = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
CAPITAL = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]+")


class ErrorAutoria(Exception):
    pass


# ---------------------------------------------------------------- léxico --

def palabras(texto: str) -> set[str]:
    return {w.lower() for w in PALABRA.findall(str(texto or ""))}


def raices(w: str) -> set[str]:
    res = {w}
    if w.endswith("'s"):
        res.add(w[:-2])
    for suf, reps in (("ies", ("y",)), ("ied", ("y",)), ("iest", ("y",)), ("ier", ("y",)),
                      ("es", ("", "e")), ("s", ("",)), ("ed", ("", "e")), ("d", ("",)),
                      ("ing", ("", "e")), ("est", ("", "e")), ("er", ("", "e")), ("ly", ("",)),
                      ("n't", ("",))):
        if w.endswith(suf) and len(w) - len(suf) >= 2:
            raiz = w[: -len(suf)]
            for r in reps:
                res.add(raiz + r)
            if len(raiz) >= 3 and raiz[-1] == raiz[-2]:
                res.add(raiz[:-1])
    return res


ORTOGRAFIA = (("our", "or"), ("ise", "ize"), ("yse", "yze"), ("tre", "ter"), ("ogue", "og"),
              ("lled", "led"), ("lling", "ling"), ("ence", "ense"))


def variantes_ortograficas(w: str) -> set[str]:
    """Variantes británica/estadounidense (neighbour/neighbor, organise/organize)."""
    res = {w}
    for uk, us in ORTOGRAFIA:
        for a, b in ((uk, us), (us, uk)):
            if a in w:
                res.add(w.replace(a, b))
    return res


def conocida(w: str, lexico: set[str]) -> bool:
    return any(raices(v) & lexico for v in variantes_ortograficas(w))


def nombres_propios(texto: str) -> set[str]:
    """Palabras con mayúscula que no abren frase (nombres, lugares)."""
    res = set()
    for frase in re.split(r"(?<=[.!?:])\s+|\n", str(texto or "")):
        tokens = PALABRA.findall(frase)
        for t in tokens[1:]:
            if t[0].isupper():
                res.add(t.lower())
    return res


def clases_editoriales(nivel: str) -> list[dict]:
    carpeta = EDITORIAL / nivel
    docs = []
    if nivel == "n1" and (carpeta / "pilot-classes-01-05.json").exists():
        docs += json.loads((carpeta / "pilot-classes-01-05.json").read_text(encoding="utf-8"))["classes"]
    for f in sorted(carpeta.glob("class-*.json")):
        docs.append(json.loads(f.read_text(encoding="utf-8")))
    return docs


def numero(cid: str) -> int:
    return int(cid.rsplit("-", 1)[1])


def lexico_previo(nivel_num: int, antes_de: int) -> set[str]:
    """Palabras enseñadas o practicadas antes de la clase ``antes_de`` del nivel."""
    lex: set[str] = set()
    curso = json.loads((ROOT / "assets/contenido/en/ruta/curso.json").read_text(encoding="utf-8"))
    for p in curso.get("palabrasLibres", []):
        lex |= palabras(p)
    for u in json.loads((ROOT / "assets/contenido/en/ruta/f0.json").read_text(encoding="utf-8"))["unidades"]:
        for v in u.get("vocabulario", []):
            lex |= palabras(v["texto"])
        for p in u.get("pasos", []):
            for it in p.get("items", []) + p.get("ejemplos", []) + p.get("dialogo", []):
                lex |= palabras(it.get("texto", "")) if "formato" not in it else set()
    for n in range(1, nivel_num + 1):
        nivel = f"n{n}"
        for d in clases_editoriales(nivel):
            if n == nivel_num and numero(d["id"]) >= antes_de:
                continue
            for v in d.get("vocabulary", []):
                lex |= palabras(v["en"])
            for t in d.get("teaching", []):
                lex |= palabras(t["en"])
            for items in d.get("pools", {}).values():
                for it in items:
                    a = it.get("answer", {})
                    o = it.get("origin", {})
                    lex |= palabras(a.get("text", "")) | palabras(" ".join(a.get("accepted", [])))
                    lex |= palabras(" ".join(c.get("text", "") for c in it.get("choices", [])))
                    lex |= palabras(o.get("text", "")) | palabras(o.get("audio", ""))
                    for par in o.get("pairs") or []:
                        lex |= palabras(par[0])
        for f in (EDITORIAL / nivel).glob("enriquecimiento-*.json"):
            for cid, e in json.loads(f.read_text(encoding="utf-8"))["classes"].items():
                if n == nivel_num and numero(cid) >= antes_de:
                    continue
                lex |= textos_ensenanza_enriquecimiento(e)
    return lex


def textos_ensenanza_enriquecimiento(e: dict) -> set[str]:
    res: set[str] = set()
    for s in (e.get("patron") or {}).get("formula", []):
        res |= palabras(s.get("texto", ""))
    for fila in (e.get("tabla") or {}).get("filas", []):
        for c in fila:
            res |= palabras(c.get("texto", ""))
    for x in e.get("erroresFrecuentes", []):
        res |= palabras(x.get("correcto", ""))
    for l in (e.get("situacion") or {}).get("dialogo", []):
        res |= palabras(l.get("texto", ""))
    for x in e.get("ejemplos", []):
        res |= palabras(x.get("en", ""))
    return res


def textos_ingleses_item(it: dict) -> list[str]:
    textos = []
    if it["formato"] in ("elegir", "escuchar"):
        textos += [o for o in it.get("opciones", []) if isinstance(o, str)]
    if isinstance(it.get("respuesta"), str):
        textos.append(it["respuesta"])
    # Las «aceptadas» no se muestran: solo corrigen lo que escribe el alumno,
    # que puede usar sinónimos correctos no enseñados (cozy, ocean…).
    for campo in ("audio", "texto"):
        if it.get(campo) and it.get("textoIdioma", "en") == "en":
            textos.append(it[campo])
    textos += [p[0] for p in it.get("pares", [])]
    textos += it.get("frases", [])
    for parte in it.get("partes", []):
        textos.append(parte.get("respuesta", ""))
    return textos


# ------------------------------------------------------------ utilidades --

def hash_estable(texto: str) -> int:
    return int(hashlib.sha256(texto.encode()).hexdigest()[:8], 16)


def segmentos(en: str) -> list[str]:
    tokens = en.split()
    if len(tokens) < 2:
        raise ErrorAutoria(f"ejemplo demasiado corto para segmentar: {en!r}")
    mitad = (len(tokens) + 1) // 2
    return [" ".join(tokens[:mitad]), " ".join(tokens[mitad:])]


def es(texto: str) -> dict:
    return {"es": texto}


# ------------------------------------------------------------ construcción --

ORDINAL = re.compile(
    # Ordinal que designa una opción: «Solo la primera usa…», «la segunda
    # opción», «la tercera es…». No «el tercer condicional», «la primera frase
    # era…» ni «el segundo punto» (orden del estímulo, que no cambia).
    r"\b(?:la|el)\s+(?:primer[oa]?|segund[oa]|tercer[oa]?|cuart[oa]|últim[oa])\s+"
    r"(?:opci[oó]n|respuesta|alternativa|usa|es|son|lleva|tiene|dice|expresa|marca|muestra|mantiene|"
    r"combina|retrocede|suena|funciona|encaja|sirve|conserva|incluye|respeta)\b"
    r"|\bopci[oó]n\s+(?:[abcd1-4])\b|\b(?:first|second|third|last)\s+(?:option|answer|choice)\b",
    re.IGNORECASE,
)


def construir_item(it: dict, *, cid_corto: str, pool: str, k: int, concepto: str,
                   requiere: list[str], turno: int = 0) -> dict:
    fmt = it["formato"]
    iid = f"{cid_corto}.{PREFIX[pool]}{k:02d}"
    if fmt in ("elegir", "escuchar") and ORDINAL.search(it.get("feedback", "") + " " + it.get("pista", "")):
        raise ErrorAutoria(f"{iid}: el feedback o la pista citan la posición de una opción; el orden cambia al construir: cita el contenido")
    origin: dict = {"kind": "editorial", "variantSeed": "0", "variantId": f"{iid}.seed-0",
                    "feedback": es(it["feedback"])}
    if pool == "practiceGuided":
        if not it.get("pista"):
            raise ErrorAutoria(f"{iid}: la práctica guiada necesita pista")
        origin["hint"] = es(it["pista"])
    elif it.get("pista"):
        raise ErrorAutoria(f"{iid}: solo la práctica guiada lleva pista")
    answer: dict = {}
    choices: list[dict] = []
    if fmt in ("elegir", "escuchar"):
        opciones = list(it["opciones"])
        correcta = int(it["respuesta"])
        if len(opciones) < 3 or not 0 <= correcta < len(opciones):
            raise ErrorAutoria(f"{iid}: se piden ≥3 opciones y respuesta válida")
        # Posición de la correcta repartida por turnos dentro de la clase: la
        # misma posición nunca supera el 60 % sin añadir opciones de relleno.
        destino = turno % len(opciones)
        texto_ok = opciones.pop(correcta)
        opciones.insert(destino, texto_ok)
        choices = [{"text": o} for o in opciones]
        answer = {"index": destino}
        if fmt == "escuchar":
            origin.update({"audio": it["audio"], "audioMode": "tts", "languageCode": "en",
                           "speedOptions": [0.75, 1.0], "maxReplays": 3,
                           "revealTranscriptAfterAttempt": True})
        if it.get("texto"):
            origin["text"] = it["texto"]
    elif fmt == "ordenar":
        answer = {"text": it["respuesta"], "tokens": it["respuesta"].split()}
        if it.get("aceptadas"):
            # Otros órdenes igual de correctos (p. ej. un adverbio movible).
            answer["accepted"] = list(dict.fromkeys([it["respuesta"], *it["aceptadas"]]))
    elif fmt == "completar":
        if it.get("frases"):
            origin["sentences"] = it["frases"]
            partes = [{"text": p["respuesta"], "accepted": list(dict.fromkeys([p["respuesta"], *p.get("aceptadas", [])]))}
                      for p in it["partes"]]
            answer = {"text": " | ".join(p["text"] for p in partes),
                      "accepted": [" | ".join(p["text"] for p in partes)], "parts": partes}
            minimo = it.get("minimo", len(partes))
            origin["scoring"] = {"parts": len(partes), "minimumCorrect": minimo}
            if it.get("texto"):
                origin["text"] = it["texto"]
        else:
            if str(it.get("texto", "")).count("___") != 1:
                raise ErrorAutoria(f"{iid}: «completar» necesita texto con un solo ___")
            origin["text"] = it["texto"]
            answer = {"text": it["respuesta"],
                      "accepted": list(dict.fromkeys([it["respuesta"], *it.get("aceptadas", [])]))}
        if it.get("audio"):
            origin["audio"] = it["audio"]
    elif fmt == "escribir":
        if not it.get("texto"):
            raise ErrorAutoria(f"{iid}: «escribir» necesita texto de estímulo")
        origin["text"] = it["texto"]
        answer = {"text": it["respuesta"],
                  "accepted": list(dict.fromkeys([it["respuesta"], *it.get("aceptadas", [])]))}
        rub = it.get("rubrica")
        if rub:
            origin["scoring"] = {"wordRange": list(rub["palabras"]), "evidenceGroups": rub["evidencias"]}
        if it.get("audio"):
            origin["audio"] = it["audio"]
    elif fmt == "relacionar":
        pares = [[a, {"es": b}] for a, b in it["pares"]]
        origin["pairs"] = pares
        answer = {"pairs": pares}
        if it.get("minimo"):
            origin["scoring"] = {"parts": len(pares), "minimumCorrect": it["minimo"]}
    else:
        raise ErrorAutoria(f"{iid}: formato desconocido {fmt}")
    item = {
        "id": iid,
        "format": fmt,
        "prompt": es(it["consigna"]),
        "answer": answer,
        "choices": choices,
        "teaches": [concepto] if pool == "practiceGuided" else [],
        "requires": [] if pool == "practiceGuided" else requiere,
        "origin": origin,
        "accessibility": {"screenReader": True, "highContrast": True, "largeText": True},
    }
    item["contentHash"] = vb.expected_hash(item)
    return item


def construir_clase(c: dict, *, nivel_num: int, mapa: dict, previos_bloque: list[str]) -> dict:
    n = c["n"]
    nivel = f"n{nivel_num}"
    cid = f"en.{nivel}.class-{n:02d}"
    cid_corto = f"en.{nivel}.c{n:02d}"
    m = mapa[cid]
    concepto = m["concepts"][0]
    previo = f"en.n{nivel_num - 1}.class-100" if n == 1 else f"en.{nivel}.class-{n - 1:02d}"
    ensenanza = []
    for k, t in enumerate(c["ensenanza"], 1):
        ensenanza.append({
            "id": f"{cid}.t{k:02d}", "en": t["en"], "es": t["es"], "explanationEs": t["nota"],
            "segments": segmentos(t["en"]), "audioText": t["en"], "audioMode": "tts",
            "languageCode": "en", "patternId": concepto,
        })
    pools: dict[str, list] = {}
    cierre = n % 5 == 0
    turno = n  # desplazamiento por clase para no empezar siempre en la misma posición
    for clave, pool in POOLS.items():
        items = c["ejercicios"][clave]
        if len(items) < MINIMOS[pool]:
            raise ErrorAutoria(f"{cid}: {clave} necesita ≥{MINIMOS[pool]} ítems")
        construidos = []
        for k, it in enumerate(items, 1):
            requiere = [concepto]
            if cierre and pool == "evaluation" and previos_bloque:
                requiere = [concepto, previos_bloque[(k - 1) % len(previos_bloque)]]
            construidos.append(construir_item(it, cid_corto=cid_corto, pool=pool, k=k,
                                              concepto=concepto, requiere=requiere, turno=turno))
            if it["formato"] in ("elegir", "escuchar"):
                turno += 1
        pools[pool] = construidos
    evaluacion, repaso = pools["evaluation"], pools["review"]
    remediacion = {
        e["id"]: {"reteach": ensenanza[i % len(ensenanza)]["id"], "review": repaso[i % len(repaso)]["id"]}
        for i, e in enumerate(evaluacion)
    }
    doc = {
        "schema": vb.SCHEMA_CLASS, "course": "en", "level": nivel_num, "cefr": m["cefr"],
        "scale": vb.SCALE, "status": "shadow", "runtimeAi": False, "phase": m["phase"],
        "variantSeed": "0", "selectionPolicy": {"deterministic": True},
        "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
        "qualityPolicy": {"chronologyTokens": "enforce", "answerReuseAcrossEarlyReserved": "forbid",
                          "answerEvidenceReuseAcrossPools": "forbid", "agentContract": vb.AGENT_CONTRACT_V2,
                          "minChoices": 3, "maxPromptCharacters": 90, "feedbackReuseWithinClass": "forbid",
                          "minClassFormats": 4},
        "id": cid,
        "title": c.get("titulo") or m["title"],
        "objectives": {"es": [c["objetivo"]]},
        "concepts": [concepto],
        "skills": c.get("habilidades", ["gramática", "lectura", "escucha", "escritura"]),
        "prerequisites": [previo],
        "usesVocabulary": [v["en"] for v in c["vocabulario"]],
        "usesPatterns": [concepto],
        "vocabulary": [{"en": v["en"], "es": v["es"]} for v in c["vocabulario"]],
        "teaching": ensenanza,
        "pools": pools,
        "remediationMap": remediacion,
        "accessibility": {"highContrast": True, "largeText": True, "screenReader": True, "audioReplay": True},
        "recovery": {"retryPool": "review", "maxAttempts": 2, "allowAudioReplay": True, "preserveProgress": True},
        "remediationPolicy": {"source": "editorial", "deterministic": True},
    }
    if cierre:
        doc["cumulativeEvaluation"] = sorted({x for e in evaluacion for x in e["requires"]})
    return doc


def enriquecimiento(c: dict) -> dict:
    e = {k: c[k] for k in ("explicacion", "patron", "erroresFrecuentes", "situacion") if k in c}
    if c.get("tabla"):
        e["tabla"] = c["tabla"]
    return e


_FIJAS = {"can't": "can not", "cannot": "can not", "won't": "will not", "shan't": "shall not",
          "i'm": "i am", "let's": "let us"}
_CON_S = {"he", "she", "it", "that", "what", "there", "where", "who", "here", "how"}


def _expandir(palabra: str) -> str:
    """Igual que expandirContracciones en correccion.dart."""
    if palabra in _FIJAS:
        return _FIJAS[palabra]
    if palabra.endswith("n't") and len(palabra) > 3:
        return palabra[:-3] + " not"
    m = re.fullmatch(r"([a-z]+)'(re|ve|ll|d|s)", palabra)
    if not m:
        return palabra
    base, suf = m.groups()
    return {"re": f"{base} are", "ve": f"{base} have", "ll": f"{base} will", "d": f"{base} would"}.get(
        suf, f"{base} is" if base in _CON_S else palabra)


def _norm_rubrica(t: str) -> str:
    t = t.lower().replace("’", "'").replace("‘", "'")
    t = re.sub(r"[.,!?¡¿;:/\"“”«»()—–…]", " ", t)
    t = " ".join(_expandir(w) for w in t.split())
    return " " + re.sub(r"\s+", " ", t).strip() + " "


def cumple_rubrica(texto: str, rub: dict) -> bool:
    """Réplica de la corrección de la app (correccion.dart) para autocomprobar."""
    n = len(_norm_rubrica(texto).split())
    lo, hi = rub["palabras"]
    if not lo <= n <= hi:
        return False
    dada = _norm_rubrica(texto)
    for grupo in rub["evidencias"]:
        ok = False
        for frase in grupo:
            ev = _norm_rubrica(frase).strip()
            if ev and (f" {ev} " in dada or re.search(rf" {re.escape(ev)}(?:s|es|d|ed|ing) ", dada)):
                ok = True
                break
        if not ok:
            return False
    return True


def comprobar_rubricas(c: dict, cid: str) -> list[str]:
    errores = []
    for clave in POOLS:
        for k, it in enumerate(c["ejercicios"][clave], 1):
            rub = it.get("rubrica")
            if it["formato"] != "escribir" or not rub:
                continue
            for texto in [it["respuesta"], *it.get("aceptadas", [])]:
                if not cumple_rubrica(texto, rub):
                    errores.append(f"{cid} {clave}[{k}]: el modelo o una respuesta aceptada no supera su propia rúbrica: {texto[:60]!r}")
    return errores


def comprobar_lexico(c: dict, cid: str, previo: set[str]) -> list[str]:
    clase = set(previo)
    for v in c["vocabulario"]:
        clase |= palabras(v["en"])
    for t in c["ensenanza"]:
        clase |= palabras(t["en"])
    enr = enriquecimiento(c)
    # El diálogo y el patrón deben usar lo ya enseñado + lo de esta clase.
    errores = []
    textos_ens = [s.get("texto", "") for s in (enr.get("patron") or {}).get("formula", [])]
    textos_ens += [x.get("correcto", "") for x in enr.get("erroresFrecuentes", [])]
    textos_ens += [l.get("texto", "") for l in (enr.get("situacion") or {}).get("dialogo", [])]
    item_sit = (enr.get("situacion") or {}).get("item", {})
    textos_ens += [o for o in item_sit.get("opciones", []) if isinstance(o, str)]
    textos_ens.append(item_sit.get("audio", ""))
    for fila in (enr.get("tabla") or {}).get("filas", []):
        for celda in fila:
            clase |= palabras(celda.get("texto", ""))

    def revisar(textos: list[str], donde: str) -> None:
        faltan = set()
        for t in textos:
            propios = nombres_propios(t)
            faltan |= {w for w in palabras(t) if w not in propios and not conocida(w, clase)}
        if faltan:
            errores.append(f"{cid} {donde}: palabras no enseñadas antes ni en la clase: {', '.join(sorted(faltan))}")

    revisar(textos_ens, "situación/patrón/errores")
    for clave in POOLS:
        for k, it in enumerate(c["ejercicios"][clave], 1):
            revisar(textos_ingleses_item(it), f"{clave}[{k}]")
    return errores


def cargar_mapa(nivel_num: int) -> dict:
    ruta = PLAN / f"mapa-n{nivel_num}-editorial-v2.json"
    m = json.loads(ruta.read_text(encoding="utf-8"))
    return {c["id"]: c for c in m["classes"]}


def construir(ruta: Path, solo_validar: bool = False) -> int:
    doc = json.loads(ruta.read_text(encoding="utf-8"))
    nivel = doc["level"]
    nivel_num = int(nivel[1:])
    ini, fin = doc["range"]["start"], doc["range"]["end"]
    compactas = sorted(doc["classes"], key=lambda c: c["n"])
    if [c["n"] for c in compactas] != list(range(ini, fin + 1)):
        print(f"ERROR: el bloque debe tener las clases {ini}–{fin}")
        return 1
    mapa = cargar_mapa(nivel_num)
    errores: list[str] = []
    clases: list[dict] = []
    previos_bloque: list[str] = []
    lex = lexico_previo(nivel_num, ini)
    for c in compactas:
        cid = f"en.{nivel}.class-{c['n']:02d}"
        errores += comprobar_lexico(c, cid, lex)
        errores += comprobar_rubricas(c, cid)
        try:
            clase = construir_clase(c, nivel_num=nivel_num, mapa=mapa, previos_bloque=list(previos_bloque))
        except (ErrorAutoria, KeyError, ValueError, TypeError) as exc:
            errores.append(f"{cid}: {exc}")
            continue
        clases.append(clase)
        previos_bloque.append(clase["concepts"][0])
        # Lo enseñado y practicado en esta clase cuenta para las siguientes.
        for v in c["vocabulario"]:
            lex |= palabras(v["en"])
        for t in c["ensenanza"]:
            lex |= palabras(t["en"])
        lex |= textos_ensenanza_enriquecimiento(enriquecimiento(c))
        for clave in POOLS:
            for it in c["ejercicios"][clave]:
                for t in textos_ingleses_item(it):
                    lex |= palabras(t)
        # Enriquecimiento con la validación común (unidad sintética).
        unidad = {"pasos": [{"tipo": "ejemplos", "items": [{"texto": t["en"]} for t in c["ensenanza"]]}]}
        err, _ = ve.validar_clase(cid, enriquecimiento(c), unidad)
        errores += err
    bundle = None
    if not errores:
        bundle = {
            "schema": vb.SCHEMA_BUNDLE, "course": "en", "level": nivel_num, "scale": vb.SCALE,
            "status": "shadow", "runtimeAi": False, "selectionPolicy": {"deterministic": True},
            "evidencePolicy": {"attemptRecords": ["variantId", "libraryVersion", "selectionId"]},
            "range": {"start": ini, "end": fin}, "classes": clases,
        }
        try:
            vb.validate_bundle(bundle, start=ini, end=fin, level=nivel_num)
        except (vb.ValidationError, KeyError, IndexError, TypeError, ValueError) as exc:
            errores.append(f"validar_bundle_editorial: {exc}")
    if errores:
        print(f"{ruta.name}: {len(errores)} error(es)")
        for e in errores:
            print("  ERROR", e)
        return 1
    print(f"{ruta.name}: OK · {len(clases)} clases · {sum(len(p) for c in clases for p in c['pools'].values())} ejercicios")
    if solo_validar:
        return 0
    carpeta = EDITORIAL / nivel
    for c in clases:
        (carpeta / f"class-{numero(c['id']):02d}.json").write_text(
            json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (carpeta / f"bundle-{ini:02d}-{fin:02d}.json").write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    enr_path = carpeta / f"enriquecimiento-{ini:02d}-{fin:02d}.json"
    enr = {"schema": ve.SCHEMA, "level": nivel, "range": {"start": ini, "end": fin},
           "classes": {f"en.{nivel}.class-{c['n']:02d}": enriquecimiento(c) for c in compactas}}
    revision = doc.get("review")
    if revision:
        enr["review"] = revision
    enr_path.write_text(json.dumps(enr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"escrito: {len(clases)} clases, bundle y {enr_path.name}")
    return 0


def main(argv: list[str]) -> int:
    solo = "--solo-validar" in argv
    rutas = [Path(a) for a in argv if not a.startswith("--")]
    return max((construir(r, solo) for r in rutas), default=0)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
