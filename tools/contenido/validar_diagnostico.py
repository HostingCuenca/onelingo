#!/usr/bin/env python3
"""Valida (y compila) el banco de la prueba de ubicación v2 de un idioma.

Uso:
  python3 tools/contenido/validar_diagnostico.py assets/contenido/en/plan-editorial/diagnostico/n4.json
  python3 tools/contenido/validar_diagnostico.py --compilar   # inglés: valida los 10 niveles y escribe el banco
  python3 tools/contenido/validar_diagnostico.py --idioma fr  # valida los niveles presentes del francés
  python3 tools/contenido/validar_diagnostico.py --idioma fr --compilar
      # compila solo los niveles con revisión GO (consecutivos desde N1)

Fuentes: assets/contenido/<idioma>/plan-editorial/diagnostico/nN.json.
Salida: assets/contenido/<idioma>/diagnostico-v2.json.
Reglas en docs/claude-educacion/DIAGNOSTICO_V2.md (sección «Otros idiomas»).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import construir_bloque as cb  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validar_ruta as vr  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def fuentes(idioma: str) -> Path:
    return ROOT / f"assets/contenido/{idioma}/plan-editorial/diagnostico"


def salida(idioma: str) -> Path:
    return ROOT / f"assets/contenido/{idioma}/diagnostico-v2.json"


FUENTES = fuentes("en")
SALIDA = salida("en")

HABILIDADES = {"escucha": ("escuchar",), "lectura": ("elegir",), "gramatica": ("elegir", "completar"),
               "vocabulario": ("elegir", "completar"), "escritura": ("escribir",)}
POR_HABILIDAD = {"escucha": 4, "lectura": 4, "gramatica": 4, "vocabulario": 4, "escritura": 2}
LECTURA = {1: (15, 35), 2: (25, 45), 3: (35, 60), 4: (45, 70), 5: (55, 85), 6: (65, 95),
           7: (75, 110), 8: (85, 120), 9: (95, 130), 10: (105, 150)}
ESCUCHA = {1: (5, 15), 2: (8, 20), 3: (12, 25), 4: (15, 30), 5: (20, 40), 6: (25, 45),
           7: (30, 55), 8: (35, 60), 9: (40, 70), 10: (45, 80)}
MAX_CORRECTA_MAS_LARGA = 0.35
POSICION = re.compile(r"\b(primer[ao]?|segund[ao]|tercer[ao]?|cuart[ao]|últim[ao])\s+(opci[oó]n|respuesta)", re.I)
POSICION_EN = re.compile(r"\b(first|second|third|fourth|last)\s+(option|answer|choice)", re.I)
# Textos de apoyo del ítem (TextoApoyo en la app).
APOYOS = ("consigna", "feedback", "pista", "preguntaApoyo")
# Palabras con letras de cualquier alfabeto (école, aujourd'hui); el inglés
# sigue con cb.PALABRA para no cambiar sus recuentos.
PALABRA_UNICODE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")


def n_palabras(t: str, idioma: str = "en") -> int:
    patron = cb.PALABRA if idioma == "en" else PALABRA_UNICODE
    return len(patron.findall(str(t or "")))


# --- Otros idiomas: léxico de la ruta publicada y rúbrica como la app ---

def lexico_ruta(idioma: str, nivel: int) -> tuple[set[str], set[str]]:
    """(conocidas, distractores) hasta el final del nivel en la ruta publicada.

    Mismo criterio que tools/validar_ruta.py: vocabulario y tablas de las
    unidades (f0 y N1…N); las formas incorrectas enseñadas solo valen como
    distractor."""
    base = ROOT / f"assets/contenido/{idioma}/ruta"
    curso = json.loads((base / "curso.json").read_text(encoding="utf-8"))
    conocidas = {w for p in curso.get("palabrasLibres", []) for w in vr.palabras(p)}
    errores: set[str] = set()
    for m in curso.get("modulos", []):
        try:
            datos = json.loads((base / m["archivo"]).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for u in datos.get("unidades", []):
            interno = u.get("nivelInterno")
            if interno is None or interno > nivel:
                continue
            conocidas |= _ensenadas(u)
            errores |= {w for e in u.get("erroresFrecuentes", [])
                        for w in vr.palabras(re.sub(r"\([^)]*\)", " ", e.get("incorrecto", "")))}
    return conocidas, conocidas | errores


def no_ensenadas(texto: str, lexico: set[str], idioma: str = "") -> set[str]:
    """Palabras del texto que la ruta no enseña (símbolos y cifras no cuentan).

    En portugués y alemán acepta, como la ruta, flexiones y conjugaciones de lo enseñado."""
    conocida = vr.conocida_para(idioma)
    return {w for w in vr.palabras(str(texto or "").replace("___", " "))
            if any(c.isalpha() for c in w) and not conocida(w, lexico)}


def _ensenadas(u: dict) -> set[str]:
    res = {w for v in u.get("vocabulario", []) for w in vr.palabras(v.get("texto", ""))}
    res |= {w for p in u.get("pasos", []) if p.get("tipo") == "tabla"
            for fila in p.get("filas", []) for c in fila if isinstance(c, dict) and "texto" in c
            for w in vr.palabras(c["texto"])}
    return res


_PUNTUACION_APP = re.compile(r"[.,!?¡¿;:/。、！？「」…\"“”«»()—–，：；]")
_TILDES = str.maketrans({"á": "a", "à": "a", "â": "a", "ä": "a", "ã": "a", "å": "a",
                         "é": "e", "è": "e", "ê": "e", "ë": "e", "í": "i", "ì": "i", "î": "i", "ï": "i",
                         "ó": "o", "ò": "o", "ô": "o", "ö": "o", "õ": "o", "ú": "u", "ù": "u", "û": "u",
                         "ü": "u", "ç": "c", "ñ": "n", "œ": "oe", "æ": "ae", "ё": "е"})


def _normalizar_app(t: str) -> str:
    """Igual que normalizar + sinTildes de correccion.dart (idiomas sin
    contracciones inglesas). \\s incluye U+202F y U+00A0, como en Dart."""
    t = t.lower().replace("’", "'").replace("‘", "'")
    t = re.sub(r"\s+", " ", _PUNTUACION_APP.sub(" ", t)).strip()
    return t.translate(_TILDES)


# El ruso se normaliza con ё ≡ е (_TILDES, como sinTildes de correccion.dart).
# zh y ja se escriben sin espacios: como en correccion.dart (_sinEspacios),
# la extensión se mide en caracteres y las evidencias se buscan sin espacios.
SIN_ESPACIOS = {"zh", "ja"}
_CARACTER_CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


def cumple_rubrica(texto: str, rub: dict, idioma: str) -> bool:
    if idioma == "en":
        return cb.cumple_rubrica(texto, rub)
    dada = _normalizar_app(texto)
    lo, hi = rub["palabras"]
    if idioma in SIN_ESPACIOS:
        n = len(_CARACTER_CJK.findall(dada)) + len(_CARACTER_CJK.sub(" ", dada).split())
        if not lo <= n <= hi:
            return False
        dada = dada.replace(" ", "")
        return all(any((ev := _normalizar_app(f).replace(" ", "")) and ev in dada for f in grupo)
                   for grupo in rub["evidencias"])
    if not lo <= len(dada.split()) <= hi:
        return False
    dada = f" {dada} "
    return all(any((ev := _normalizar_app(f)) and f" {ev} " in dada for f in grupo)
               for grupo in rub["evidencias"])


# Cursos cuyo apoyo es solo inglés (el español se explica en inglés).
APOYO_SOLO_EN = {"es"}


def es_texto(v, clave: str = "es") -> str:
    return v.get(clave, "") if isinstance(v, dict) else ""


def _modulo_zh():
    """Reglas del chino de tools/contenido/ruta-zh/validar.py (sandhi, espacios,
    puntuación de ancho completo, solo simplificado)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "validar_zh", ROOT / "tools/contenido/ruta-zh/validar.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


_PAUSAS_ZH = re.compile(r"[\s。，？！、；：…“”（）]+")
_PAUSAS_ROM = re.compile(r"[\s,.?!;:…\"()]+")


def errores_chino(it: dict) -> list[str]:
    """Romanización y tipografía de un ítem en chino (docs/claude-educacion/ROMANIZACION.md):
    `textoRom`/`opcionesRom` paralelos al chino, palabra a palabra; pinyin con el
    sandhi escrito; palabras separadas por espacios y puntuación de ancho
    completo pegada. `audio`, `respuesta` y `aceptadas` no llevan rom."""
    import rom_items  # noqa: E402  (tools/contenido)
    zh = _modulo_zh()
    hay = lambda t: isinstance(t, str) and bool(zh.HANZI.search(t))  # noqa: E731

    def comprobar(texto: str, rom: str):
        a = [t for t in _PAUSAS_ZH.split(texto) if zh.HANZI.search(t)]
        b = [g for g in _PAUSAS_ROM.split(rom.replace("___", " ")) if g.strip("-—'")]
        if len(a) != len(b):
            return f"«{texto}» tiene {len(a)} palabras y «{rom}» tiene {len(b)} grupos; deben coincidir uno a uno"
        return None

    errores = rom_items.errores({"unidades": [{"id": it.get("id", "?"), "pasos": [{"items": [it]}]}]},
                                hay, comprobar)
    for k, v in it.items():
        if k.endswith("Rom"):
            for r in (v if isinstance(v, list) else [v]):
                if isinstance(r, str) and r:
                    # El hueco corta la cadena de sandhi (no se sabe qué va en él).
                    e, a = zh.errores_rom(r.replace("___", ","), f"{k} «{r}»")
                    errores += e + a
    textos = [it.get("texto"), it.get("audio"), *(it.get("opciones") or [])]
    if it.get("formato") == "escribir":
        textos += [it.get("respuesta"), *(it.get("aceptadas") or [])]
    for t in textos:
        if hay(t):
            e, a = zh.errores_texto_chino(t, "texto")
            errores += e + a
    iid = str(it.get("id", "?"))
    return [x.replace(f"{iid}/{iid}", iid, 1) if x.startswith(iid) else f"{iid}: {x}" for x in errores]


def _modulo_ja():
    """Reglas del japonés de tools/contenido/ruta-ja/validar.py (kana sin kanji,
    puntuación de ancho completo, partículas aparte, tokens razonables)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "validar_ja", ROOT / "tools/contenido/ruta-ja/validar.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


_KANJI_JA: dict[int, set[str]] = {}


def kanji_ensenados_ja(nivel: int) -> set[str]:
    """Kanji enseñados hasta el final del nivel en la ruta publicada del japonés:
    los que aparecen en el vocabulario o en las tablas de las unidades (mismo
    criterio que `_ensenadas`). N1–N2 no enseñan ninguno: todo va en kana."""
    if nivel not in _KANJI_JA:
        kanji = re.compile(r"[一-鿿㐀-䶿]")
        base = ROOT / "assets/contenido/ja/ruta"
        curso = json.loads((base / "curso.json").read_text(encoding="utf-8"))
        res: set[str] = set()
        for m in curso.get("modulos", []):
            try:
                datos = json.loads((base / m["archivo"]).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            for u in datos.get("unidades", []):
                interno = u.get("nivelInterno")
                if interno is not None and interno <= nivel:
                    res |= {k for w in _ensenadas(u) for k in kanji.findall(w)}
        _KANJI_JA[nivel] = res
    return _KANJI_JA[nivel]


def errores_japones(it: dict) -> list[str]:
    """Romanización y tipografía de un ítem en japonés (docs/claude-educacion/ROMANIZACION.md):
    `textoRom`/`opcionesRom` paralelos al japonés, una palabra de rōmaji por cada palabra
    (Hepburn modificado de tools/ia/idiomas/ja.md, con macrones, n', wa/e/o y mayúscula solo
    al inicio de frase y en nombres propios: tools/contenido/hepburn_ja.py); palabras
    separadas por espacios y puntuación de ancho completo pegada; kanji solo los enseñados
    hasta el nivel del ítem (ninguno en N1–N2: kanji_ensenados_ja). `audio`,
    `respuesta` y `aceptadas` no llevan rom."""
    import hepburn_ja  # noqa: E402  (tools/contenido)
    import rom_items  # noqa: E402
    ja = _modulo_ja()
    nivel = it.get("nivel")
    ja.KANJI_PERMITIDOS = kanji_ensenados_ja(nivel) if isinstance(nivel, int) else set()
    hay = lambda t: isinstance(t, str) and bool(ja.KANA.search(t) or ja.KANJI.search(t))  # noqa: E731

    def comprobar(texto: str, rom: str):
        if ja.KANA.search(rom) or ja.KANJI.search(rom):
            return "rom con kana o kanji"
        e = hepburn_ja.errores_rom(texto, rom)
        return "; ".join(e) if e else None

    errores = rom_items.errores({"unidades": [{"id": it.get("id", "?"), "pasos": [{"items": [it]}]}]},
                                hay, comprobar)
    textos = [it.get("texto"), it.get("audio"), *(it.get("opciones") or [])]
    if it.get("formato") == "escribir":
        textos += [it.get("respuesta"), *(it.get("aceptadas") or [])]
        textos += [e for g in it.get("evidenciasEscritura") or [] for e in g]
    textos = [t for t in textos if isinstance(t, str)]
    avisos: list[str] = []
    ja.revisar_japones(textos, errores, avisos)
    # «はは» (madre) no es una partícula は pegada.
    avisos = [x for x in avisos if "pegada en «はは»" not in x]
    # Los números van en kana: ninguna cifra arábiga en el japonés (ficha, escritura por nivel).
    errores += [f"cifra arábiga en «{t}»" for t in textos if hay(t) and re.search(r"[0-9]", t)]
    iid = str(it.get("id", "?"))
    return [x.replace(f"{iid}/{iid}", iid, 1) if x.startswith(iid) else f"{iid}: {x}" for x in errores + avisos]


def _modulo_ru():
    """Reglas del ruso de tools/contenido/ruta-ru/validar.py (rom letra a letra con
    la tilde de acento solo en el rom, cirílico sin U+0301, sin alfabetos mezclados)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "validar_ru", ROOT / "tools/contenido/ruta-ru/validar.py")
    modulo = importlib.util.module_from_spec(spec)
    argv, sys.argv = sys.argv, sys.argv[:1]  # validar.py lee sys.argv[1] al importarse
    try:
        spec.loader.exec_module(modulo)
    finally:
        sys.argv = argv
    return modulo


_ECUADOR_RU = re.compile(r"ecuador|ecuatorian|quito|guayaquil|cuenca|эквадор", re.I)


def errores_ruso(it: dict) -> list[str]:
    """Romanización y tipografía de un ítem en ruso (docs/claude-educacion/ROMANIZACION.md,
    tools/ia/idiomas/ru.md): `textoRom`/`opcionesRom` paralelos al ruso, una palabra de
    rom por cada palabra rusa, letra a letra (ё = yo, е = ye al inicio o tras vocal o ь/ъ,
    ь = ', una tilde aguda por palabra de 2+ sílabas y ninguna en los monosílabos); el
    cirílico nunca lleva marca de acento ni letras latinas mezcladas. `audio`,
    `respuesta` y `aceptadas` no llevan rom. Nunca Ecuador."""
    import rom_items  # noqa: E402  (tools/contenido)
    ru = _modulo_ru()
    hay = lambda t: isinstance(t, str) and bool(ru.CIRILICO.search(t))  # noqa: E731

    def comprobar(texto: str, rom: str):
        propios: list[str] = []
        ru.comprobar_par("", "", texto, rom, propios)
        return "; ".join(e.split(": ", 1)[-1].strip() for e in propios) or None

    errores = rom_items.errores({"unidades": [{"id": it.get("id", "?"), "pasos": [{"items": [it]}]}]},
                                hay, comprobar)

    def textos(x):
        if isinstance(x, str):
            yield x
        elif isinstance(x, dict):
            for v in x.values():
                yield from textos(v)
        elif isinstance(x, list):
            for v in x:
                yield from textos(v)

    for t in textos(it):
        if ru.ACENTO in t:
            errores.append(f"marca de acento U+0301 en «{t[:40]}»: el acento va solo en el rom")
        for palabra in re.findall(r"[A-Za-zА-Яа-яЁё]+", t):
            if ru.CIRILICO.search(palabra) and re.search(r"[A-Za-z]", palabra):
                errores.append(f"letras latinas y cirílicas mezcladas en «{palabra}»")
        if _ECUADOR_RU.search(t):
            errores.append(f"menciona Ecuador: «{t[:40]}»")
    # En el texto que se oye o se lee no van cifras ni símbolos (se escriben en palabras).
    for t in [it.get("audio"), it.get("texto"), *(it.get("opciones") or [])]:
        if hay(t) and re.search(r"[0-9₽%/→]", t):
            errores.append(f"cifra o símbolo en «{t[:40]}»: se escribe en palabras")
    iid = str(it.get("id", "?"))
    return [x.replace(f"{iid}/{iid}", iid, 1) if x.startswith(iid) else f"{iid}: {x}" for x in errores]


def _modulo_ko():
    """Reglas del coreano de tools/contenido/ruta-ko/validar.py (rom sin hangul ni diacríticos,
    mayúscula solo en nombres propios, sin Ecuador)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "validar_ko", ROOT / "tools/contenido/ruta-ko/validar.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


_LEXICO_ROM_KO: dict[str, set[str]] | None = None


def _lexico_rom_ko() -> dict[str, set[str]]:
    """eojeol → roms que le dan las clases publicadas (texto/rom, textoRom, opcionesRom…):
    un eojeol de las clases debe llevar en el diagnóstico la misma rom que allí."""
    global _LEXICO_ROM_KO
    if _LEXICO_ROM_KO is not None:
        return _LEXICO_ROM_KO
    import rr_ko  # noqa: E402  (tools/contenido)
    lex: dict[str, set[str]] = {}

    def par(c, r):
        if isinstance(c, str) and isinstance(r, str):
            a, b = rr_ko.tokens_hangul(c), [x for x in re.split(r"\s+", r.replace("___", " ")) if re.search("[A-Za-z]", x)]
            if len(a) == len(b):
                for x, y in zip(a, b):
                    lex.setdefault(x, set()).add(re.sub(r"[^A-Za-z\-]", "", y))

    def recorrer(x):
        if isinstance(x, dict):
            if "texto" in x and "rom" in x:
                par(x["texto"], x["rom"])
            for k in ("texto", "pregunta"):
                if k in x and k + "Rom" in x:
                    par(x[k], x[k + "Rom"])
            for k in ("opciones", "tokens"):
                if isinstance(x.get(k), list) and isinstance(x.get(k + "Rom"), list) \
                        and len(x[k]) == len(x[k + "Rom"]):
                    for c, r in zip(x[k], x[k + "Rom"]):
                        par(c, r)
            for v in x.values():
                recorrer(v)
        elif isinstance(x, list):
            for v in x:
                recorrer(v)

    for f in sorted((ROOT / "assets/contenido/ko/ruta").glob("*.json")):
        if f.name != "curso.json":
            recorrer(json.loads(f.read_text(encoding="utf-8")))
    _LEXICO_ROM_KO = lex
    return lex


_ECUADOR_KO = re.compile(r"ecuador|ecuatorian|quito|guayaquil|cuenca|에콰도르|키토|과야킬|쿠엥카", re.I)


def errores_coreano(it: dict) -> list[str]:
    """Romanización y tipografía de un ítem en coreano (docs/claude-educacion/ROMANIZACION.md,
    tools/ia/idiomas/ko.md): `textoRom`/`opcionesRom` paralelos al coreano, una palabra de
    rom por eojeol (RR oficial, comprobada con tools/contenido/rr_ko.py y con la rom de
    las clases; nombre completo = 2 palabras); hangul con espacios entre eojeol, sin hanja
    ni kana, sin 당신 ni Ecuador, sin cifras ni símbolos en lo que se oye o se lee.
    `audio`, `respuesta` y `aceptadas` no llevan rom."""
    import rom_items  # noqa: E402  (tools/contenido)
    import rr_ko  # noqa: E402
    ko = _modulo_ko()
    hay = lambda t: isinstance(t, str) and bool(ko.HANGUL.search(t))  # noqa: E731
    lexico = _lexico_rom_ko()

    def comprobar(texto: str, rom: str):
        e = ko.error_rom(rom.replace("___", "").strip() or "-")
        e = None if e == "rom vacío" else e
        if e is None or e.startswith("rom con mayúscula fuera"):
            e = "; ".join(rr_ko.errores_rom(texto, rom, lexico)) or None
        return e

    errores = rom_items.errores({"unidades": [{"id": it.get("id", "?"), "pasos": [{"items": [it]}]}]},
                                hay, comprobar)

    def textos(x):
        if isinstance(x, str):
            yield x
        elif isinstance(x, dict):
            for v in x.values():
                yield from textos(v)
        elif isinstance(x, list):
            for v in x:
                yield from textos(v)

    for t in textos(it):
        if _ECUADOR_KO.search(t):
            errores.append(f"menciona Ecuador: «{t[:40]}»")
        if re.search(r"[\u3040-\u30ff\u3400-\u9fff]", t):
            errores.append(f"hanja o kana en «{t[:40]}»")
    for t in [it.get("audio"), it.get("texto"), *(it.get("opciones") or [])]:
        if hay(t) and re.search(r"[0-9₩%/→_]", str(t).replace("___", "")):
            errores.append(f"cifra o símbolo en «{str(t)[:40]}»: se escribe en palabras")
        if hay(t) and re.search(r"(?<![가-힣])당신", str(t)):
            errores.append(f"usa 당신 en «{str(t)[:40]}»")
    for t in [it.get("audio"), it.get("texto"), *(it.get("opciones") or []), it.get("respuesta")]:
        if hay(t) and re.search(r"[가-힣][,.?!]?\S*[가-힣]", str(t)) and "  " in str(t):
            errores.append(f"doble espacio en «{str(t)[:40]}»")
    iid = str(it.get("id", "?"))
    return [x.replace(f"{iid}/{iid}", iid, 1) if x.startswith(iid) else f"{iid}: {x}" for x in errores]


def validar(path: Path, idioma: str = "en") -> tuple[list[str], list[dict]]:
    errores: list[str] = []
    doc = json.loads(path.read_text(encoding="utf-8"))
    nivel = doc.get("nivel")
    if nivel not in LECTURA:
        return [f"{path.name}: «nivel» debe ser 1–10"], []
    if idioma != "en" and doc.get("idioma", idioma) != idioma:
        errores.append(f"{path.name}: «idioma» debe ser {idioma}")
    items = doc.get("items") or []
    if idioma == "en":
        lex = cb.lexico_previo(nivel, 101)
    else:
        lex_ruta, lex_distractores = lexico_ruta(idioma, nivel)
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
        esperado = f"dx.{idioma}.n{nivel}.{h}.{cuenta[h]}"
        if it.get("id") != esperado:
            e(f"id esperado {esperado}")
        if iid in ids:
            e("id duplicado")
        ids.add(iid)
        solo_en = idioma in APOYO_SOLO_EN
        clave = "en" if solo_en else "es"
        consigna, feedback = es_texto(it.get("consigna"), clave), es_texto(it.get("feedback"), clave)
        if not consigna or len(consigna) > (110 if solo_en else 90):
            e(f"consigna.{clave} obligatoria y ≤ {110 if solo_en else 90} caracteres")
        if consigna.casefold() in consignas:
            e("consigna repetida")
        consignas.add(consigna.casefold())
        if not feedback:
            e(f"falta feedback.{clave}")
        if POSICION.search(feedback):
            e("el feedback no puede citar la posición de una opción")
        if solo_en:
            # Apoyo solo en inglés, como la ruta del idioma (idiomasApoyo: ["en"]).
            for campo in APOYOS:
                if campo not in it:
                    continue
                v = it[campo]
                if not isinstance(v, dict) or set(v) != {"en"} or \
                        not all(isinstance(x, str) and x.strip() for x in v.values()):
                    e(f"{campo}: texto de apoyo {{en}} sin vacíos")
            if POSICION_EN.search(feedback):
                e("el feedback (en) no puede citar la posición de una opción")
        elif idioma != "en":
            # Apoyo bilingüe para hispanohablantes y anglohablantes (I18N.md).
            for campo in APOYOS:
                if campo not in it:
                    continue
                v = it[campo]
                if not isinstance(v, dict) or set(v) != {"es", "en"} or \
                        not all(isinstance(x, str) and x.strip() for x in v.values()):
                    e(f"{campo}: texto de apoyo bilingüe {{es, en}} sin vacíos")
            consigna_en = (it.get("consigna") or {}).get("en", "") if isinstance(it.get("consigna"), dict) else ""
            if len(consigna_en) > 110:
                e("consigna.en ≤ 110 caracteres")
            feedback_en = it.get("feedback").get("en", "") if isinstance(it.get("feedback"), dict) else ""
            if POSICION_EN.search(feedback_en):
                e("el feedback (en) no puede citar la posición de una opción")
        textos_en: list[str] = []
        if h == "lectura":
            lo, hi = LECTURA[nivel]
            n = n_palabras(it.get("texto", ""), idioma)
            if not lo <= n <= hi:
                e(f"el pasaje tiene {n} palabras (N{nivel}: {lo}–{hi})")
            textos_en.append(it.get("texto", ""))
        if h == "escucha":
            lo, hi = ESCUCHA[nivel]
            n = n_palabras(it.get("audio", ""), idioma)
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
                e("3–4 opciones (texto inglés)" if idioma == "en" else f"3–4 opciones (texto en {idioma})")
                op = []
            elif len({o.strip().casefold() for o in op}) != len(op):
                e("opciones repetidas")
            r = it.get("respuesta")
            if not isinstance(r, int) or not 0 <= r < max(len(op), 1):
                e("respuesta debe ser el índice de la opción correcta")
            elif op:
                con_opciones += 1
                largos = [n_palabras(o, idioma) for o in op]
                delata += largos[r] == max(largos) and largos.count(max(largos)) == 1
            if idioma == "en":
                textos_en += op or []
            else:
                # Como en la ruta: los distractores pueden usar formas
                # incorrectas enseñadas como error frecuente.
                r_ok = it.get("respuesta") if isinstance(it.get("respuesta"), int) else -1
                for i_op, o in enumerate(op or []):
                    lexico = lex_ruta if i_op == r_ok else lex_distractores
                    faltan_op = no_ensenadas(o, lexico, idioma)
                    if faltan_op:
                        e(f"opción {i_op}: palabras no enseñadas hasta el final de N{nivel}: "
                          f"{', '.join(sorted(faltan_op))}")
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
                    if not cumple_rubrica(t, rub, idioma):
                        e(f"escribir: el texto no supera su rúbrica: «{t[:60]}…»")
            textos_en.append(modelo)
            if it.get("texto") and it.get("textoIdioma", idioma) == idioma:
                textos_en.append(it["texto"])
        if idioma == "zh":
            for x in errores_chino(it):
                errores.append(x)
        if idioma == "ja":
            for x in errores_japones(it):
                errores.append(x)
        if idioma == "ru":
            for x in errores_ruso(it):
                errores.append(x)
        if idioma == "ko":
            for x in errores_coreano(it):
                errores.append(x)
        if idioma == "en":
            faltan = {w for t in textos_en for w in cb.palabras(t) if not cb.conocida(w, lex)}
        else:
            # Sin la regla de ortografía británica/estadounidense; la tipografía
            # francesa (U+202F antes de ? ! : ;) es un espacio más.
            faltan = {w for t in textos_en for w in no_ensenadas(t, lex_ruta, idioma)}
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
    idioma = "en"
    if "--idioma" in argv:
        k = argv.index("--idioma")
        if k + 1 >= len(argv) or not re.fullmatch(r"[a-z]{2}", argv[k + 1]):
            print("--idioma necesita un código de idioma (en, fr…)")
            return 2
        idioma = argv[k + 1]
        argv = argv[:k] + argv[k + 2:]
    rutas = [Path(a) for a in argv if not a.startswith("--")]
    todos = compilar or not rutas
    if todos:
        rutas = [fuentes(idioma) / f"n{n}.json" for n in range(1, 11)]
        if idioma != "en":
            # Otros idiomas: solo los niveles que ya existen (N1, luego N2…).
            rutas = [p for p in rutas if p.exists()]
            if not rutas:
                print(f"{fuentes(idioma).relative_to(ROOT)}: no hay niveles"); return 1
    total_err, banco, compilados = 0, [], []
    for p in rutas:
        if not p.exists():
            print(f"{p.name}: no existe"); total_err += 1; continue
        err, items = validar(p, idioma)
        sin_go = (json.loads(p.read_text(encoding="utf-8")).get("review") or {}).get("status") != "GO"
        if compilar and sin_go and idioma != "en":
            # Un nivel sin GO no se compila, pero no impide compilar los demás.
            print(f"{p.name}: sin revisión independiente GO · no se compila"
                  f"{'' if not err else f' ({len(err)} error(es))'}")
            for x in err[:40]:
                print("  ERROR", x)
            continue
        if compilar and sin_go:
            err.append(f"{p.name}: sin revisión independiente GO")
        total_err += len(err)
        print(f"{p.name}: {'OK' if not err else f'{len(err)} error(es)'} · {len(items)} ítems")
        for x in err[:40]:
            print("  ERROR", x)
        compilados.append(json.loads(p.read_text(encoding="utf-8")).get("nivel"))
        for it in items:
            # La vista de ítems corrige «completar» por texto: se exporta la
            # opción correcta como respuesta (la fuente guarda el índice).
            if it.get("formato") == "completar" and isinstance(it.get("respuesta"), int):
                it = {**it, "respuesta": it["opciones"][it["respuesta"]],
                      "aceptadas": [it["opciones"][it["respuesta"]]]}
            banco.append(it)
    if compilar:
        if idioma != "en" and (not compilados or compilados != list(range(1, len(compilados) + 1))):
            print(f"Los niveles con GO deben ser consecutivos desde N1 (hay {compilados or 'ninguno'}).")
            total_err += 1
        if total_err:
            print("No se compila: hay errores.")
            return 1
        destino = salida(idioma)
        destino.write_text(json.dumps({"schema": "onelingo.diagnostico.v2", "idioma": idioma, "items": banco},
                                      ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"escrito {destino.relative_to(ROOT) if destino.is_relative_to(ROOT) else destino} · {len(banco)} ítems"
              + ("" if idioma == "en" else f" · niveles {', '.join(f'N{n}' for n in compilados)}"))
    return 1 if total_err else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
