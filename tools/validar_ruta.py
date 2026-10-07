#!/usr/bin/env python3
"""Valida las rutas de aprendizaje (assets/contenido/<idioma>/ruta/).

Uso: python3 tools/validar_ruta.py [idioma ...]   (sin argumentos: todos)
     python3 tools/validar_ruta.py fr --borrador b01.json [b02.json …]
       valida además módulos en borrador (aún no están en curso.json), como si
       se publicaran: sirve para revisar un bloque antes de integrarlo.
Sale con código 1 si hay errores. Reglas en docs/claude-educacion/ESQUEMA_CONTENIDO.md.
"""
import json
import re
import sys
from pathlib import Path

# La detección de ciclos recorre la cadena de prerrequisitos (~1000 unidades en inglés).
sys.setrecursionlimit(20000)

RAIZ = Path(__file__).resolve().parent.parent / "assets" / "contenido"
ENSENAR = {"explicacion", "ejemplos", "vocabulario", "patron", "tabla"}
ORDEN_TIPOS = ["ensenar", "practica_guiada", "practica_independiente", "situacion", "evaluacion"]
FORMATOS = {"elegir", "escuchar", "ordenar", "completar", "escribir", "relacionar"}
PUNTUACION = re.compile(r"[.,!?¡¿;:。、！？「」『』・（）…\"“”„()«»‹›—–，：；]")
CAMPOS_HUELLA = {
    "formato", "consigna", "pregunta", "preguntaApoyo", "opciones", "respuesta",
    "aceptadas", "tokens", "texto", "audio", "pares",
}


def palabras(texto):
    texto = texto.replace("’", "'").replace("‘", "'").replace("‚", "'").replace("___", " ")
    # Comillas simples de cita ('once', shopkeepers', alemán ‚so‘) no forman parte de la palabra.
    res = [p.strip("'") for p in PUNTUACION.sub(" ", texto.lower()).split()]
    return [p for p in res if p and p != "-"]


def bases(w):
    """Formas base posibles de una flexión regular inglesa (plural, 's,
    -ed, -ing, -er/-est). Evita exigir que cada flexión se declare aparte."""
    res = set()
    if w.endswith("'s"):
        res.add(w[:-2])
    for suf, reemplazos in (("ies", ("y",)), ("ied", ("y",)), ("iest", ("y",)), ("ier", ("y",)),
                            ("es", ("", "e")), ("s", ("",)), ("ed", ("", "e")), ("d", ("",)),
                            ("ing", ("", "e")), ("est", ("", "e")), ("er", ("", "e"))):
        if w.endswith(suf) and len(w) - len(suf) >= 2:
            raiz = w[: -len(suf)]
            for r in reemplazos:
                res.add(raiz + r)
            if len(raiz) >= 3 and raiz[-1] == raiz[-2]:
                res.add(raiz[:-1])  # running → run, bigger → big
    return res


def conocida(w, conocidas):
    # Tokens con cifras (cantidades, precios «£45», horas) cuentan como números.
    return w in conocidas or any(c.isdigit() for c in w) or bool(bases(w) & conocidas)


_FORMAS = {}


def formas_verbales(idioma):
    """Forma conjugada → infinitivos, según assets/contenido/<idioma>/verbos.json
    (celdas de las tablas y formas sueltas; el auxiliar del alemán no cuenta)."""
    if idioma not in _FORMAS:
        indice = _FORMAS[idioma] = {}
        ruta = RAIZ / idioma / "verbos.json"
        if ruta.exists():
            for v in json.loads(ruta.read_text(encoding="utf-8")).get("verbos", []):
                inf = v["infinitivo"].lower()
                formas = [f for t in v.get("tablas", {}).values() for f in t]
                formas += [f for k, f in v.get("formas", {}).items() if k != "auxiliar" and isinstance(f, str)]
                for f in formas:
                    for w in palabras(f):
                        indice.setdefault(w, set()).add(inf)
    return _FORMAS[idioma]


def formas_pt():
    return formas_verbales("pt")


def bases_pt(w):
    """Formas base posibles de una flexión nominal portuguesa (número y género)."""
    res = set()
    for suf, reemplazos in (("ões", ("ão",)), ("ães", ("ão",)), ("ãos", ("ão",)), ("ais", ("al",)),
                            ("éis", ("el",)), ("eis", ("el", "il")), ("óis", ("ol",)), ("uis", ("ul",)),
                            ("is", ("il",)), ("ns", ("m",)), ("es", ("",)), ("s", ("",))):
        if w.endswith(suf) and len(w) - len(suf) >= 2:
            res |= {w[: -len(suf)] + r for r in reemplazos}
    for f in [w] + sorted(res):
        if f.endswith("a") and len(f) >= 3:
            res |= {f[:-1] + "o", f[:-1] + "e"} | ({f[:-1]} if f.endswith("ora") else set())
    return res


# Terminaciones de los verbos regulares (presente, pretérito, imperfecto, futuro,
# condicional, subjuntivos, participio y gerundio) → vocal temática posible.
_DESINENCIAS_PT = {
    "a": ("o", "a", "as", "amos", "am", "ei", "ou", "aram", "ava", "avas", "ávamos", "avam",
          "e", "es", "emos", "em", "ado", "ada", "ados", "adas", "ando", "asse", "assem", "ássemos",
          "armos", "arem", "arei", "ará", "aremos", "arão", "aria", "ariam", "aríamos"),
    "e": ("o", "e", "es", "emos", "em", "i", "eu", "eram", "ia", "ias", "íamos", "iam",
          "a", "as", "amos", "am", "ido", "ida", "idos", "idas", "endo", "esse", "essem",
          "ermos", "erem", "erei", "erá", "eremos", "erão", "eria", "eriam", "eríamos"),
    "i": ("o", "e", "es", "imos", "em", "i", "iu", "iram", "ia", "ias", "íamos", "iam",
          "a", "as", "amos", "am", "ido", "ida", "idos", "idas", "indo", "isse", "issem",
          "irmos", "irem", "irei", "irá", "iremos", "irão", "iria", "iriam", "iríamos"),
}
# Cambios ortográficos ante e: liguei/ligue (ligar), fiquei (ficar), comecei (começar).
_ORTOGRAFIA_PT = (("gu", "g"), ("qu", "c"), ("c", "ç"))


def infinitivos_pt(w):
    res = set()
    for vocal, desinencias in _DESINENCIAS_PT.items():
        for d in desinencias:
            if w.endswith(d) and len(w) - len(d) >= 2:
                raiz = w[: -len(d)]
                res.add(raiz + vocal + "r")
                for antes, despues in _ORTOGRAFIA_PT:
                    if raiz.endswith(antes):
                        res.add(raiz[: -len(antes)] + despues + vocal + "r")
    # Gerundio de verbos cortos: indo (ir), sendo (ser), tendo (ter), pondo (pôr).
    if w.endswith(("ando", "endo", "indo")):
        res.add(w[:-3] + "r")
    if w == "pondo":
        res.add("pôr")
    return res


def conocida_pt(w, conocidas):
    """Como `conocida`, aceptando además plurales/femeninos de palabras enseñadas
    y formas conjugadas de verbos cuyo infinitivo ya se enseñó."""
    if conocida(w, conocidas) or bases_pt(w) & conocidas:
        return True
    if (formas_pt().get(w, set()) | infinitivos_pt(w)) & conocidas:
        return True
    # Ênclise: «registra-se», «deixá-la», «fazê-lo»; el clítico cuenta si se
    # enseñó su forma base («-la» tras «deixá» = «a»).
    verbo, _, clitico = w.partition("-")
    if not clitico or "-" in clitico or not _CLITICOS_PT.get(clitico, set()) & conocidas:
        return False
    candidatos = {verbo}
    if verbo[-1:] in _INFINITIVO_PT:
        candidatos.add(verbo[:-1] + _INFINITIVO_PT[verbo[-1]])
    return any(conocida_pt(v, conocidas) for v in candidatos)


_CLITICOS_PT = {
    "se": {"se"}, "me": {"me"}, "te": {"te"}, "lhe": {"lhe"}, "lhes": {"lhe", "lhes"},
    "o": {"o"}, "a": {"a"}, "os": {"os", "o"}, "as": {"as", "a"},
    "lo": {"o"}, "la": {"a"}, "los": {"os", "o"}, "las": {"as", "a"},
    "no": {"o"}, "na": {"a"}, "nos": {"nos", "os", "o"}, "nas": {"as", "a"},
}
# «deixá-la» ← deixar, «fazê-lo» ← fazer, «pô-lo» ← pôr; «parti-lo» queda en «parti» → partir.
_INFINITIVO_PT = {"á": "ar", "ê": "er", "ô": "or", "i": "ir"}


# ── Alemán ────────────────────────────────────────────────────────────────
# Heurística como la del portugués: una forma cuenta si su base ya se enseñó.
# Mismas reglas en lib/core/aprendizaje/integridad.dart (palabraConocidaDe).

_ALT_GRAFIA_DE = {"ss": "ß", "ae": "ä", "oe": "ö", "ue": "ü"}


def grafias_de(w):
    """La palabra con ß/ss, ä/ae, ö/oe y ü/ue intercambiadas (máx. 64 grafías)."""
    plano = w.replace("ß", "ss").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    res = [""]
    i = 0
    while i < len(plano):
        par = plano[i:i + 2]
        if par in _ALT_GRAFIA_DE and len(res) < 64:
            res = [r + x for r in res for x in (par, _ALT_GRAFIA_DE[par])]
            i += 2
        else:
            res = [r + plano[i] for r in res]
            i += 1
    return set(res)


def sin_umlaut_de(w):
    """Quita la última diéresis: Äpfel → apfel, Häuser → hauser, läuft → lauft."""
    res = set()
    for a, b in (("äu", "au"), ("ä", "a"), ("ö", "o"), ("ü", "u")):
        i = w.rfind(a)
        if i >= 0:
            res.add(w[:i] + b + w[i + len(a):])
    return res


def _quitar_de(w, sufijos, minimo=2):
    return {w[: -len(s)] for s in sufijos if w.endswith(s) and len(w) - len(s) >= minimo}


# Plural, caso y terminación de adjetivo; luego grado (comparativo/superlativo).
_SUF_NOMINAL_DE = ("ern", "nen", "sen", "ens", "en", "em", "er", "es", "se", "e", "n", "s")
_SUF_GRADO_DE = ("est", "st", "er")
_GRADO_IRREG_DE = {
    "besser": "gut", "best": "gut", "mehr": "viel", "meist": "viel", "lieber": "gern",
    "liebst": "gern", "höher": "hoch", "höchst": "hoch", "nächst": "nah", "größt": "groß",
}
# Palabras que parecen flexión de otra y no lo son (aber ≠ ab+er, dass ≠ das+s…).
_NO_DERIVAR_DE = {"aber", "unser", "euer", "denen", "deren", "wenn", "denn", "das", "dass",
                  "neun", "ihnen", "etwas", "ins", "eins"}


def bases_de(w):
    """Bases posibles de una flexión nominal/adjetival alemana: plural (-e, -er,
    -n, -en, -s, -nen, -se, con diéresis), -n/-s/-es de caso, terminaciones de
    adjetivo y grado (-er, -(e)st, diéresis, besser/best…)."""
    if w in _NO_DERIVAR_DE:
        return set()
    n1 = _quitar_de(w, _SUF_NOMINAL_DE)
    res = set(n1)
    for x in {w} | n1:
        if x in _NO_DERIVAR_DE:
            continue
        if x in _GRADO_IRREG_DE:
            res.add(_GRADO_IRREG_DE[x])
        res |= _quitar_de(x, _SUF_GRADO_DE)
    for x in res | {w}:
        res = res | sin_umlaut_de(x)
    for x in set(res):
        # e caída del tema: dunkle → dunkel, teure → teuer, Regeln → regel ya sale.
        if len(x) >= 3 and x[-1] in "lr" and x[-2] != "e":
            res.add(x[:-1] + "e" + x[-1])
    res.discard(w)
    return res


def _forma_a_inf_de(tabla):
    return {f: set(infs.split("|")) for infs, formas in tabla.items() for f in formas.split()}


# Formas sueltas (presente irregular, Präteritum y Konjunktiv II de sein/haben/werden).
_FORMAS_IRREG_DE = _forma_a_inf_de({
    "sein": "bin bist ist sind seid sei seien seist war warst waren wart wäre wärst wären wärt wäret wärest",
    "haben": "hast hat hatte hattest hatten hattet hätte hättest hätten hättet",
    "werden": "wirst wird wurde wurdest wurden wurdet würde würdest würden würdet",
    "wissen": "weiß weißt",
    "können": "kann kannst",
    "müssen": "muss musst",
    "wollen": "will willst",
    "dürfen": "darf darfst",
    "sollen": "soll sollst",
    "mögen": "mag magst",
    "tun": "tu tue tust tut tun",
    "nehmen": "nimm nimmst nimmt",
    "treten": "tritt trittst",
    "halten": "hält hältst",
    "gelten": "gilt",
    "raten": "rät rätst",
    "laden": "lädt",
})
# Bases de Präteritum fuerte/mixto y de Konjunktiv II; admiten -st/-t/-en/-n detrás
# (gingen, kamst, könntest, wüssten).
_BASES_IRREG_DE = _forma_a_inf_de({
    "gehen": "ging ginge", "kommen": "kam käme", "sehen": "sah sähe", "geben": "gab gäbe",
    "finden": "fand fände", "lesen": "las", "essen": "aß", "trinken": "trank",
    "sprechen": "sprach", "nehmen": "nahm", "fahren": "fuhr", "laufen": "lief",
    "bleiben": "blieb", "schreiben": "schrieb", "stehen": "stand", "sitzen": "saß",
    "liegen": "lag", "rufen": "rief", "denken": "dachte", "bringen": "brachte",
    "kennen": "kannte", "nennen": "nannte", "rennen": "rannte", "wissen": "wusste wüsste",
    "tun": "tat täte", "heißen": "hieß", "schlafen": "schlief", "treffen": "traf",
    "fliegen": "flog", "helfen": "half", "beginnen": "begann", "ziehen": "zog",
    "tragen": "trug", "fallen": "fiel", "halten": "hielt", "lassen": "ließ",
    "waschen": "wusch", "singen": "sang", "schwimmen": "schwamm", "gewinnen": "gewann",
    "sterben": "starb", "steigen": "stieg", "schneiden": "schnitt", "verlieren": "verlor",
    "vergessen": "vergaß", "empfehlen": "empfahl", "bitten": "bat", "schließen": "schloss",
    "bieten": "bot", "greifen": "griff", "scheinen": "schien", "fangen": "fing",
    "können": "konnte könnte", "müssen": "musste müsste", "dürfen": "durfte dürfte",
    "mögen": "mochte möchte", "wollen": "wollte", "sollen": "sollte",
})
# Partizip II fuerte/mixto sin ge- (gegangen, verstanden ← ver+standen, begonnen).
_PARTIZIP_DE = _forma_a_inf_de({
    "gehen": "gangen", "sein": "wesen", "werden": "worden", "trinken": "trunken",
    "finden": "funden", "schreiben": "schrieben", "sprechen": "sprochen", "nehmen": "nommen",
    "bleiben": "blieben", "essen": "gessen", "treffen": "troffen", "stehen": "standen",
    "helfen": "holfen", "wissen": "wusst", "denken": "dacht", "bringen": "bracht",
    "kennen": "kannt", "nennen": "nannt", "rennen": "rannt", "fliegen": "flogen",
    "ziehen": "zogen", "sitzen": "sessen", "liegen": "legen", "sterben": "storben",
    "schwimmen": "schwommen", "singen": "sungen", "gewinnen": "wonnen", "ginnen": "gonnen",
    "steigen": "stiegen", "schneiden": "schnitten", "tun": "tan", "mögen": "mocht",
    "können": "konnt", "müssen": "musst", "dürfen": "durft", "lieren": "loren",
    "gebären": "boren", "bitten": "beten", "schließen": "schlossen", "bieten": "boten",
    "greifen": "griffen", "scheinen": "schienen", "leihen": "liehen", "schweigen": "schwiegen",
})
_SEPARABLES_DE = ("zusammen", "zurück", "vorbei", "weiter", "wieder", "kennen", "fern", "fest",
                  "nach", "teil", "auf", "aus", "ein", "mit", "vor", "weg", "los", "bei",
                  "her", "hin", "ab", "an", "um", "zu")
_INSEPARABLES_DE = ("miss", "emp", "ent", "zer", "ver", "be", "er")


def _regular_de(raiz):
    res = {raiz + "en"}
    if raiz.endswith(("el", "er")):
        res.add(raiz + "n")  # wandert → wandern
    if len(raiz) >= 3 and raiz[-1] in "lr" and raiz[-2] != "e":
        res.add(raiz[:-1] + "e" + raiz[-1] + "n")  # sammle → sammeln
    return res


def _cambio_vocal_de(raiz):
    """Raíz de presente con cambio vocálico → raíz del infinitivo (liest, gibt, fährt)."""
    res = sin_umlaut_de(raiz)
    i = raiz.rfind("ie")
    if i >= 0:
        res.add(raiz[:i] + "e" + raiz[i + 2:])
    i = raiz.rfind("i")
    if i >= 0:
        res.add(raiz[:i] + "e" + raiz[i + 1:])
    return res


def infinitivos_de(w, prefijos=True, sin_ge=False):
    """Infinitivos posibles de una forma verbal alemana."""
    res = set()
    for e in ("", "st", "t", "n", "en", "est", "et"):
        if w.endswith(e) and len(w) - len(e) >= 2:
            base = w[: len(w) - len(e)] if e else w
            res |= _BASES_IRREG_DE.get(base, set())
    res |= _FORMAS_IRREG_DE.get(w, set())
    # Presente (e de unión: arbeitest, wartet; wir/sie = infinitivo) e imperativo (komm, geh).
    for e in ("est", "et", "st", "en", "t", "e", "n", ""):
        if w.endswith(e) and len(w) - len(e) >= 2:
            raiz = w[: len(w) - len(e)] if e else w
            res |= _regular_de(raiz)
            if e in ("est", "st", "t", ""):
                for r in _cambio_vocal_de(raiz):
                    res |= _regular_de(r)
    # Präteritum regular: machte, arbeiteten.
    for e in ("etest", "etet", "eten", "ete", "test", "tet", "ten", "te"):
        if w.endswith(e) and len(w) - len(e) >= 2:
            res |= _regular_de(w[: -len(e)])
    # Partizip II: ge-…-(e)t regular, ge-…-en fuerte, más la tabla de irregulares.
    nucleos = [w] if sin_ge else []
    if w.startswith("ge") and len(w) >= 5:
        nucleos.append(w[2:])
    for n in nucleos:
        res |= _PARTIZIP_DE.get(n, set())
        for e in ("et", "t", "en"):
            if n.endswith(e) and len(n) - len(e) >= 2:
                res |= _regular_de(n[: -len(e)])
    if prefijos:
        for p in _INSEPARABLES_DE:
            if w.startswith(p) and len(w) - len(p) >= 3:
                res |= {p + i for i in infinitivos_de(w[len(p):], False, True)}
        for p in _SEPARABLES_DE:
            if w.startswith(p) and len(w) - len(p) >= 3:
                resto = w[len(p):]
                # anzurufen → anrufen; angerufen → an + gerufen.
                for r in {resto} | ({resto[2:]} if resto.startswith("zu") and len(resto) >= 5 else set()):
                    res |= {p + i for i in infinitivos_de(r, False)}
    return res


def conocida_de(w, conocidas):
    """Como `conocida` (sin la morfología inglesa), aceptando además flexiones
    alemanas de palabras enseñadas: plurales, caso, adjetivos y grado, formas
    verbales (presente, Präteritum, Konjunktiv II, Partizip II, separables) y
    grafías ß/ss, ä/ae, ö/oe, ü/ue. Las mayúsculas ya las quita `palabras`."""
    if w in conocidas or any(c.isdigit() for c in w):
        return True
    formas = formas_verbales("de")
    for g in grafias_de(w):
        candidatos = {g} | bases_de(g) | formas.get(g, set())
        infs = infinitivos_de(g)
        # Participio declinado como adjetivo: gekochte, geschlossenen.
        for x in _quitar_de(g, ("e", "en", "em", "er", "es"), 4):
            if x.endswith(("t", "en")):
                infs |= infinitivos_de(x)
        # Verbo separable con el prefijo aparte en la frase: «ich rufe … an».
        infs |= {p + i for i in infs for p in _SEPARABLES_DE}
        candidatos |= infs
        if any(v in conocidas for c in candidatos for v in grafias_de(c)):
            return True
    # El prefijo separado («an», «auf») cuenta si se enseñó un verbo con él.
    return w in _SEPARABLES_DE and any(
        c.startswith(w) and len(c) >= len(w) + 4 and c.endswith("n") and c not in _SEPARABLES_DE
        for c in conocidas)


# ── Italiano ──────────────────────────────────────────────────────────────
# Heurística como la del alemán: una forma cuenta si su base ya se enseñó.
# Elisión (l'amico, dell'acqua, c'è, quest'anno), truncamiento (po', buon,
# signor), plurales/femeninos, -issimo/-mente, verbos regulares (-are, -ere,
# -ire, -isc-), irregulares frecuentes y pronombres enclíticos (chiamarsi,
# dimmi). Mismas reglas en lib/core/aprendizaje/integridad.dart (palabraConocidaIt).

_VOCALES_IT = "aeio"
# Elididas sin vocal fácil de reponer: l' = il/lo/la, dell' = del/della…
_ELISION_IT = {"l": {"il", "lo", "la"}, "gl": {"gli"}, "dell": {"del", "della", "dello"},
               "nell": {"nel", "nella", "nello"}, "all": {"al", "alla", "allo"},
               "sull": {"sul", "sulla", "sullo"}, "dall": {"dal", "dalla", "dallo"},
               "coll": {"col", "colla", "collo"}, "un": {"una", "uno"}}
# Preposición articulada elidida = preposición + artículo l' enseñados por separado.
_PREP_ART_IT = {"dell": "di", "nell": "in", "all": "a", "sull": "su", "dall": "da", "coll": "con"}
_ARTICULO_L_IT = {"l", "il", "lo", "la"}
# Truncamientos (apócope) sin apóstrofo o con él ya quitado por `palabras` (po' → po).
_APOCOPE_IT = {"po": "poco", "be": "bene", "buon": "buono", "bel": "bello", "quel": "quello",
               "gran": "grande", "san": "santo", "nessun": "nessuno", "ciascun": "ciascuno",
               "alcun": "alcuno", "qual": "quale", "tal": "tale", "signor": "signore",
               "dottor": "dottore", "professor": "professore", "ingegner": "ingegnere",
               "suor": "suora", "mal": "male", "ben": "bene", "fin": "fino"}
_PLURAL_IRREG_IT = {"uomini": "uomo", "uova": "uovo", "dita": "dito", "braccia": "braccio",
                    "labbra": "labbro", "ossa": "osso", "paia": "paio", "migliaia": "migliaio",
                    "centinaia": "centinaio", "ginocchia": "ginocchio", "mogli": "moglie",
                    "buoi": "bue", "templi": "tempio"}
_SUF_NOMINAL_IT = (("chi", ("co",)), ("ghi", ("go",)), ("che", ("ca",)), ("ghe", ("ga",)),
                   ("ci", ("co", "ce", "cio", "cia")), ("gi", ("go", "ge", "gio", "gia")),
                   ("ce", ("cia",)), ("ge", ("gia",)), ("trice", ("tore",)), ("trici", ("tore", "trice")),
                   ("essa", ("e", "o")), ("esse", ("e", "o", "essa")),
                   ("i", ("o", "e", "a", "io")), ("e", ("a",)), ("a", ("o",)))
# Palabras que parecen flexión de otra y no lo son (anche ≠ anca, dei ≠ dea…).
_NO_DERIVAR_IT = {"anche", "come", "che", "dei", "nei", "sei", "lei", "mai", "poi", "oggi",
                  "bene", "male", "gli", "le", "la", "lo", "ci", "si", "mi", "ti", "vi", "ne",
                  "se", "e", "a", "i", "o", "da", "di", "fa", "va", "qui", "qua", "ma", "tra", "fra"}


def bases_it(w):
    """Bases posibles de una flexión nominal/adjetival italiana: plural (-i, -e,
    -chi/-ghi, -ci/-gi, -ce/-ge, irregulares), femenino → masculino,
    -trice/-essa, superlativo -issimo y adverbio en -mente."""
    if w in _NO_DERIVAR_IT:
        return set()
    res = set()
    if w in _PLURAL_IRREG_IT:
        res.add(_PLURAL_IRREG_IT[w])
    # -issimo/-issima/-issimi/-issime → bello, grande
    m = re.fullmatch(r"(.{2,})issim[oaie]", w)
    if m:
        res |= {m.group(1) + "o", m.group(1) + "e", m.group(1) + "a"}
    # -mente → lenta/lento, facile, veloce
    m = re.fullmatch(r"(.{2,})mente", w)
    if m:
        r = m.group(1)
        res |= {r, r + "e"} | ({r[:-1] + "o"} if r.endswith("a") else set())
    for x in [w] + sorted(res):
        for suf, reemplazos in _SUF_NOMINAL_IT:
            if x.endswith(suf) and len(x) - len(suf) >= 2:
                res |= {x[: -len(suf)] + r for r in reemplazos}
    # femenino → masculino también sobre lo ya obtenido (italiane → italiana → italiano).
    for x in sorted(res):
        if x.endswith("a") and len(x) >= 3:
            res.add(x[:-1] + "o")
    res.discard(w)
    return res


def _forma_a_inf_it(tabla):
    res = {}
    for inf, formas in tabla.items():
        for f in formas.split():
            res.setdefault(f, set()).add(inf)
    return res


# Formas irregulares frecuentes (presente, pasado remoto, futuro/condicional
# con raíz contraída, subjuntivo, imperativo y participio).
_FORMAS_IRREG_IT = _forma_a_inf_it({
    "essere": "sono sei è siamo siete ero eri era eravamo eravate erano fui fu fummo foste furono "
              "sarò sarai sarà saremo sarete saranno sarei saresti sarebbe saremmo sareste sarebbero "
              "sia siano siate fossi fosse fossimo fossero stato stata stati state",
    "avere": "ho hai ha abbiamo avete hanno ebbi ebbe ebbero avrò avrai avrà avremo avrete avranno "
             "avrei avresti avrebbe avremmo avreste avrebbero abbia abbiano abbiate",
    "andare": "vado vai va vanno andrò andrai andrà andremo andrete andranno andrei andresti "
              "andrebbe andremmo andreste andrebbero vada vadano",
    "fare": "faccio fai fa facciamo fate fanno facevo facevi faceva facevamo facevate facevano "
            "feci fece facemmo faceste fecero faccia facciano facendo fatto",
    "stare": "sto stai sta stiamo stanno stetti stette stettero stia stiano",
    "dare": "do dai dà diamo danno diedi diede diedero dettero dia diano",
    "dire": "dico dici dice diciamo dite dicono dicevo dicevi diceva dicevamo dicevate dicevano "
            "dirò dirai dirà diremo direte diranno direi diresti direbbe dissi disse dissero dica "
            "dicano dicendo detto",
    "potere": "posso puoi può possiamo potete possono potrò potrai potrà potremo potrete potranno "
              "potrei potresti potrebbe potremmo potreste potrebbero possa possano",
    "volere": "voglio vuoi vuole vogliamo volete vogliono vorrò vorrai vorrà vorremo vorrete "
              "vorranno vorrei vorresti vorrebbe vorremmo vorreste vorrebbero volli volle vollero "
              "voglia vogliano",
    "dovere": "devo debbo devi deve dobbiamo dovete devono debbono dovrò dovrai dovrà dovremo "
              "dovrete dovranno dovrei dovresti dovrebbe dovremmo dovreste dovrebbero debba debbano",
    "sapere": "so sai sa sappiamo sanno saprò saprai saprà sapremo saprete sapranno saprei "
              "sapresti saprebbe sapremmo sapreste saprebbero seppi seppe seppero sappia sappiano",
    "venire": "vengo vieni viene vengono verrò verrai verrà verremo verrete verranno verrei "
              "verresti verrebbe verremmo verreste verrebbero venni venne vennero venga vengano",
    "uscire": "esco esci esce escono esca escano",
    "bere": "bevo bevi beve beviamo bevete bevono bevevo bevevi beveva bevevamo bevevate bevevano "
            "berrò berrai berrà berremo berrete berranno berrei berresti berrebbe bevvi bevve "
            "bevvero beva bevano bevendo bevuto",
    "tenere": "tengo tieni tiene tengono terrò terrai terrà terremo terrete terranno terrei "
              "terresti terrebbe tenni tenne tennero tenga tengano",
    "rimanere": "rimango rimangono rimarrò rimarrai rimarrà rimarrei rimasi rimase rimasero "
                "rimasto rimanga",
    "piacere": "piaccio piacciono piacque piacquero piaccia piacciano",
    "morire": "muoio muori muore muoiono morto muoia",
    "salire": "salgo salgono salga",
    "scegliere": "scelgo scelgono scelsi scelse scelsero scelto scelga",
    "togliere": "tolgo tolgono tolsi tolse tolto tolga",
    "sedere": "siedo siedi siede siedono sieda",
    "nascere": "nacqui nacque nacquero nato",
    "vivere": "vissi visse vissero vissuto vivrò vivrai vivrà vivremo vivrete vivranno vivrei",
    "vedere": "vidi vide videro visto vedrò vedrai vedrà vedremo vedrete vedranno vedrei "
              "vedresti vedrebbe",
    "prendere": "presi prese presero preso",
    "mettere": "misi mise misero messo",
    "leggere": "lessi lesse lessero letto",
    "scrivere": "scrissi scrisse scrissero scritto",
    "aprire": "aperto", "offrire": "offerto", "soffrire": "sofferto", "coprire": "coperto",
    "chiudere": "chiusi chiuse chiusero chiuso",
    "rispondere": "risposi rispose risposero risposto",
    "chiedere": "chiesi chiese chiesero chiesto",
    "correre": "corsi corse corsero corso",
    "perdere": "persi perse persero perso",
    "decidere": "decisi decise decisero deciso",
    "scendere": "scesi scese scesero sceso",
    "spendere": "spesi spese spesero speso",
    "accendere": "accesi accese acceso",
    "rompere": "ruppi ruppe ruppero rotto",
    "muovere": "mossi mosse mosso",
    "succedere": "successe successo",
    "conoscere": "conobbi conobbe conobbero",
    "crescere": "crebbi crebbe",
    "vincere": "vinsi vinse vinto",
    "spegnere": "spensi spense spento",
    "piangere": "piansi pianse pianto",
    "ridere": "risi rise riso",
    "dividere": "divisi divise diviso",
    "porre": "pongo poni pone poniamo ponete pongono posi pose posto",
})
# Prefijos de compuestos de irregulares (rifare, ottenere, permettere, comporre).
_PREFIJOS_IT = ("sotto", "ri", "pre", "com", "con", "dis", "man", "ot", "per", "pro", "tra",
                "sor", "av", "ap", "sup", "im", "in")
_CLITICOS_IT = {"lo": {"lo"}, "la": {"la"}, "li": {"li"}, "le": {"le"}, "ne": {"ne"},
                "mi": {"mi"}, "ti": {"ti"}, "si": {"si"}, "ci": {"ci"}, "vi": {"vi"},
                "gli": {"gli"}}
# Primer clítico de un grupo (me lo → melo, glielo).
_CLITICOS_COMB_IT = {"me": "mi", "te": "ti", "se": "si", "ce": "ci", "ve": "vi", "glie": "gli"}
# Imperativos monosilábicos que doblan la consonante del clítico (dimmi, fallo, dammi).
_IMPERATIVO_CORTO_IT = {"di": "dire", "fa": "fare", "da": "dare", "va": "andare", "sta": "stare"}

_DESINENCIAS_IT = {
    "are": ("o", "i", "a", "iamo", "ate", "ano", "avo", "avi", "ava", "avamo", "avate", "avano",
            "erò", "erai", "erà", "eremo", "erete", "eranno", "erei", "eresti", "erebbe",
            "eremmo", "ereste", "erebbero", "arò", "arai", "arà", "aremo", "arete", "aranno",
            "arei", "aresti", "arebbe", "aremmo", "areste", "arebbero", "ai", "asti", "ò",
            "ammo", "aste", "arono", "ino", "iate", "ato", "ata", "ati", "ate", "ando", "are",
            "assi", "asse", "assimo", "assero"),
    "ere": ("o", "i", "e", "iamo", "ete", "ono", "evo", "evi", "eva", "evamo", "evate", "evano",
            "erò", "erai", "erà", "eremo", "erete", "eranno", "erei", "eresti", "erebbe",
            "eremmo", "ereste", "erebbero", "ei", "etti", "é", "ette", "emmo", "este", "erono",
            "ettero", "a", "ano", "iate", "uto", "uta", "uti", "ute", "iuto", "iuta", "iuti",
            "iute", "endo", "ere", "essi", "esse", "essimo", "essero"),
    "ire": ("o", "i", "e", "iamo", "ite", "ono", "ivo", "ivi", "iva", "ivamo", "ivate", "ivano",
            "irò", "irai", "irà", "iremo", "irete", "iranno", "irei", "iresti", "irebbe",
            "iremmo", "ireste", "irebbero", "ii", "isti", "ì", "immo", "iste", "irono", "a",
            "ano", "iate", "ito", "ita", "iti", "ite", "endo", "ire", "isco", "isci", "isce",
            "iscono", "isca", "iscano", "issi", "isse", "issimo", "issero"),
}


def _irregulares_it(w):
    res = set(_FORMAS_IRREG_IT.get(w, set()))
    # Participio irregular con género y número: fatta, scritti, aperte.
    if not res and w[-1:] in "aie" and len(w) >= 4:
        res |= {i for i in _FORMAS_IRREG_IT.get(w[:-1] + "o", set())
                if (w[:-1] + "o").endswith(("to", "so"))}
    return res


def infinitivos_it(w, prefijos=True):
    """Infinitivos posibles de una forma verbal italiana."""
    res = _irregulares_it(w)
    for tema, desinencias in _DESINENCIAS_IT.items():
        for d in desinencias:
            if w.endswith(d) and len(w) - len(d) >= 2:
                raiz = w[: -len(d)]
                res.add(raiz + tema)
                if raiz.endswith(("ch", "gh")):  # cerchi → cercare, paghiamo → pagare
                    res.add(raiz[:-1] + tema)
                if tema == "are" and d[0] in "ie":  # studi → studiare, mangerò → mangiare
                    res.add(raiz + "iare")
                if tema == "ere" and raiz.endswith("uc"):  # traduco → tradurre
                    res.add(raiz[:-1] + "rre")
    # Infinitivo reflexivo enseñado como tal: chiamo → chiamarsi.
    res |= {i[:-1] + "si" for i in list(res) if i.endswith("re")}
    if prefijos:
        for p in _PREFIJOS_IT:
            if w.startswith(p) and len(w) - len(p) >= 3:
                res |= {p + i for i in _irregulares_it(w[len(p):])}
    return res


def _enclitico_it(w, conocidas):
    """Forma verbal + pronombres enclíticos: chiamarsi, vederlo, dimmi, dandoglielo."""
    for c, bases in _CLITICOS_IT.items():
        if not w.endswith(c) or len(w) - len(c) < 2 or not bases & conocidas:
            continue
        resto = w[: -len(c)]
        restos = {resto}
        for comb, base in _CLITICOS_COMB_IT.items():
            if resto.endswith(comb) and len(resto) - len(comb) >= 2 and base in conocidas:
                restos.add(resto[: -len(comb)])
        for r in set(restos):
            # Consonante doblada tras imperativo corto: dimmi, fallo, dammelo.
            if len(r) >= 3 and r[-1] == c[0] and r[:-1] in _IMPERATIVO_CORTO_IT:
                if _IMPERATIVO_CORTO_IT[r[:-1]] in conocidas:
                    return True
            candidatos = {r + "e"} if r.endswith("r") else set()  # chiamar(si) → chiamare
            candidatos |= infinitivos_it(r)
            if candidatos & conocidas:
                return True
    return False


def _elision_it(prefijo, conocidas):
    """La parte elidida delante del apóstrofo (l', dell', un', c', quest', anch')."""
    if prefijo in conocidas or any(prefijo + v in conocidas for v in _VOCALES_IT):
        return True
    if _ELISION_IT.get(prefijo, set()) & conocidas:
        return True
    prep = _PREP_ART_IT.get(prefijo)
    if prep and prep in conocidas and _ARTICULO_L_IT & conocidas:
        return True
    # Ya enseñada en otra palabra elidida: «l'amico» enseña «l'» para «l'acqua».
    return any(c.startswith(prefijo + "'") for c in conocidas if "'" in c)


def _grafias_it(w):
    """é/è finales intercambiables (perché/perchè, caffè/caffé)."""
    res = {w}
    if w.endswith("é"):
        res.add(w[:-1] + "è")
    elif w.endswith("è"):
        res.add(w[:-1] + "é")
    return res


def conocida_it(w, conocidas):
    """Como `conocida` (sin la morfología inglesa), aceptando además la elisión
    (l'amico, dell'acqua, c'è, un'amica), truncamientos (po', buon), flexiones
    italianas de palabras enseñadas (plural, femenino, -issimo, -mente), formas
    verbales (regulares, irregulares frecuentes, verbos.json si existe) y
    enclíticos. Las mayúsculas y comillas ya las quita `palabras`."""
    if w in conocidas or any(c.isdigit() for c in w):
        return True
    if "'" in w:
        prefijo, _, resto = w.partition("'")
        return bool(prefijo) and _elision_it(prefijo, conocidas) and conocida_it(resto, conocidas)
    formas = formas_verbales("it")
    for g in _grafias_it(w):
        if g in conocidas:
            return True
        candidatos = {g} | bases_it(g) | formas.get(g, set()) | infinitivos_it(g)
        if g in _APOCOPE_IT:
            candidatos.add(_APOCOPE_IT[g])
        if candidatos & conocidas:
            return True
    if _enclitico_it(w, conocidas):
        return True
    # Vista ya tras un apóstrofo en lo enseñado: «dov'è» enseña «è».
    return any(c.endswith("'" + w) for c in conocidas if "'" in c)


# ── Ruso, coreano, japonés y chino ────────────────────────────────────────
# Sin morfología inventada: una forma cuenta solo si se enseñó tal cual (el
# vocablo «читать (читаю)» o «자다 (자요)» enseña las dos formas, porque
# `palabras` parte por los paréntesis). Los campos `rom` nunca se validan.
# Mismas reglas en lib/core/aprendizaje/integridad.dart.

def normalizar_ru(w):
    """Sin acento gráfico (U+0301) y con ё ≡ е, para comparar."""
    return w.replace("́", "").replace("ё", "е")


def conocida_ru(w, conocidas):
    """Forma exacta enseñada, ignorando el acento U+0301 y la diferencia ё/е."""
    if w in conocidas or any(c.isdigit() for c in w):
        return True
    n = normalizar_ru(w)
    return n in conocidas or any(normalizar_ru(c) == n for c in conocidas)


def conocida_cjk(w, conocidas):
    """Japonés y chino: el curso escribe con espacios entre palabras y
    `palabras` quita la puntuación de ancho completo. Sin segmentar: cada
    token, partículas sueltas incluidas (は, の, 的, 吗), debe estar enseñado."""
    return w in conocidas or any(c.isdigit() for c in w)


# Partículas que pueden ir pegadas a un sustantivo en el eojeol (ficha ko.md).
PARTICULAS_KO = ("은", "는", "이", "가", "을", "를", "에", "에서", "도", "의", "와", "과",
                 "하고", "으로", "로", "이에요", "예요", "에게", "한테", "부터", "까지",
                 "만", "보다", "처럼", "이랑", "랑")
# Partícula de tema/adición tras otra de caso: 서울에서는, 주말에는, 저한테도.
_PARTICULAS_KO_FINAL = ("은", "는", "도", "만")
_PARTICULAS_KO_INTERIOR = ("에", "에서", "에게", "한테", "하고", "와", "과", "으로", "로",
                           "부터", "까지", "보다", "처럼", "이랑", "랑")


def _quitar_particula_ko(w, conocidas, particulas):
    """Raíces de `w` tras quitar una partícula final enseñada (sin tocar jamo)."""
    return {w[: -len(p)] for p in particulas
            if len(w) > len(p) and w.endswith(p) and p in conocidas}


_DIGITOS_SINO_KO = "일이삼사오육칠팔구"
_GRUPO_SINO_KO = (rf"(?:[{_DIGITOS_SINO_KO}]?천)?(?:[{_DIGITOS_SINO_KO}]?백)?"
                  rf"(?:[{_DIGITOS_SINO_KO}]?십)?[{_DIGITOS_SINO_KO}]?")
_NUMERO_SINO_KO = re.compile(rf"(?:{_GRUPO_SINO_KO}만)?{_GRUPO_SINO_KO}")


def _numero_sino_ko(w, conocidas):
    """Número sinocoreano compuesto cuyos dígitos y multiplicadores están
    enseñados: 이십, 십일, 삼백오십, 오천 (con 십/백/천/만) o una serie de 3+
    dígitos (공일공, un teléfono). Una pareja de dígitos como 오이 no cuenta."""
    if len(w) < 2 or not all(c in conocidas for c in w):
        return False
    if _NUMERO_SINO_KO.fullmatch(w) and any(m in w for m in "십백천만"):
        return True
    return len(w) >= 3 and all(c in _DIGITOS_SINO_KO + "공영" for c in w)


def conocida_ko(w, conocidas):
    """Eojeol enseñado tal cual, o sustantivo enseñado + partícula pegada que
    también se enseñó (저는, 서울에서, 학생이에요); como mucho dos partículas
    si la última es 은/는/도/만 (서울에서는); o un número sinocoreano compuesto
    de dígitos enseñados (이천, 공일공). Los verbos conjugados solo
    cuentan si se enseñó esa forma exacta."""
    if w in conocidas or any(c.isdigit() for c in w) or _numero_sino_ko(w, conocidas):
        return True
    if _quitar_particula_ko(w, conocidas, PARTICULAS_KO) & conocidas:
        return True
    return any(_quitar_particula_ko(r, conocidas, _PARTICULAS_KO_INTERIOR) & conocidas
               for r in _quitar_particula_ko(w, conocidas, _PARTICULAS_KO_FINAL))


def conocida_para(idioma):
    """Prueba de «palabra conocida» que corresponde al idioma de la ruta."""
    return {"pt": conocida_pt, "de": conocida_de, "it": conocida_it, "ru": conocida_ru,
            "ko": conocida_ko, "ja": conocida_cjk, "zh": conocida_cjk}.get(idioma, conocida)


def huella_item(item):
    """Contenido puntuable, sin id, pista, consigna ni feedback editorial."""
    datos = {k: item[k] for k in CAMPOS_HUELLA if k in item}
    return json.dumps(datos, ensure_ascii=False, sort_keys=True)


class Validador:
    def __init__(self, idioma, borradores=()):
        self.idioma = idioma
        self.borradores = list(borradores)
        self.errores = []
        self.advertencias = []

    def error(self, donde, msg):
        self.errores.append(f"[{self.idioma}] {donde}: {msg}")

    def advertencia(self, donde, msg):
        self.advertencias.append(f"[{self.idioma}] {donde}: {msg}")

    def apoyo(self, valor, donde):
        if not isinstance(valor, dict):
            self.error(donde, "se esperaba TextoApoyo {idioma: texto}")
            return
        for l in self.apoyos:
            if not str(valor.get(l, "")).strip():
                self.error(donde, f"falta texto de apoyo '{l}'")

    def validar(self):
        base = RAIZ / self.idioma / "ruta"
        try:
            curso = json.loads((base / "curso.json").read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            self.error("curso.json", f"no se puede leer: {e}")
            return self.errores
        if curso.get("idioma") != self.idioma:
            self.error("curso.json", "campo idioma no coincide con la carpeta")
        self.apoyos = curso.get("idiomasApoyo") or []
        if not self.apoyos or curso.get("apoyoPredeterminado") not in self.apoyos:
            self.error("curso.json", "idiomasApoyo/apoyoPredeterminado inválidos")
        if curso.get("revision") not in ("inicial", "revisada"):
            self.error("curso.json", "revision debe ser 'inicial' o 'revisada'")
        libres = {w for p in curso.get("palabrasLibres", []) for w in palabras(p)}
        # vocabularioEstricto: solo cuenta como enseñado el vocabulario que se
        # muestra (refs de un paso `vocabulario`) o aparece en ejemplos,
        # patrones y tablas; un vocablo declarado pero oculto no basta.
        self.estricto = bool(curso.get("vocabularioEstricto"))
        # reglasAutoria: reglas mecánicas que en el francés causaron ~30 % de
        # las correcciones de revisión (tablas «Para leer», opciones de
        # comprensión, extensión de la situación, apellidos del reparto).
        self.autoria = bool(curso.get("reglasAutoria"))
        self.libres = libres
        self.reparto = self._reparto() if self.autoria else {}
        niveles = {n["id"]: n for n in curso.get("niveles", [])}
        for n in niveles.values():
            self.apoyo(n.get("titulo"), f"nivel {n['id']}.titulo")
            if n.get("estado") == "planificado" and n.get("nivelInterno") is not None:
                self.error(f"nivel {n['id']}", "un nivel planificado no lleva nivelInterno")
        unidades = {}
        for m in curso.get("modulos", []):
            self.apoyo(m.get("titulo"), f"modulo {m.get('id')}.titulo")
            if m.get("nivel") not in niveles:
                self.error(f"modulo {m.get('id')}", "nivel inexistente")
            try:
                datos = json.loads((base / m["archivo"]).read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                self.error(m.get("archivo", "?"), f"no se puede leer: {e}")
                continue
            if datos.get("modulo") != m["id"]:
                self.error(m["archivo"], "campo modulo no coincide con curso.json")
            if not datos.get("unidades"):
                self.error(m["archivo"], "módulo sin unidades")
            for u in datos.get("unidades", []):
                if u.get("id") in unidades:
                    self.error(u.get("id"), "id de unidad duplicado")
                unidades[u.get("id")] = u
        for archivo in self.borradores:
            try:
                datos = json.loads(Path(archivo).read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                self.error(str(archivo), f"no se puede leer: {e}")
                continue
            if not datos.get("unidades"):
                self.error(str(archivo), "módulo sin unidades")
            for u in datos.get("unidades", []):
                if u.get("id") in unidades:
                    self.error(u.get("id"), "id de unidad duplicado")
                unidades[u.get("id")] = u
        # Curso «en preparación» (it, ja, ko, ru, zh): módulos vacíos a propósito.
        if not unidades and (curso.get("modulos") or self.borradores):
            self.error("curso", "sin unidades")
        self.grafo(unidades)
        for u in unidades.values():
            self.unidad(u, unidades, libres)
            # Solo las clases del plan (DEC-034: <idioma>.nX.cNN), no Fundamentos ni el contenido anterior.
            if self.autoria and re.search(r"\.n\d+\.c\d+$", str(u.get("id", ""))):
                self.reglas_autoria(u)
        return self.errores

    def _reparto(self):
        """{apellido: {nombre: género}} del reparto (curriculo/<idioma>/n1.json)."""
        p = RAIZ.parents[1] / "curriculo" / self.idioma / "n1.json"
        res = {}
        if p.exists():
            for per in json.loads(p.read_text(encoding="utf-8")).get("personajes", []):
                partes = str(per.get("nombre", "")).split()
                if len(partes) == 2 and partes[0].lower() not in self.TITULOS:
                    res.setdefault(partes[1], {})[partes[0]] = per.get("genero")
        return res

    TITULOS = {"señor": "m", "don": "m", "doctor": "m", "dr": "m", "sr": "m",
               "señora": "f", "doña": "f", "doctora": "f", "dra": "f", "sra": "f", "señorita": "f",
               "monsieur": "m", "madame": "f", "mademoiselle": "f"}
    LECTURA = {1: (3, 6, "líneas"), 2: (60, 160, "palabras"), 3: (130, 300, "palabras"), 4: (130, 300, "palabras"),
               5: (270, 560, "palabras"), 6: (270, 560, "palabras"), 7: (270, 560, "palabras"),
               8: (360, 770, "palabras"), 9: (360, 770, "palabras"), 10: (360, 770, "palabras")}

    def apellidos(self, texto, donde):
        """Un apellido del reparto solo va con su nombre o con un tratamiento de su género."""
        for m in re.finditer(r"(?=\b([A-Za-zÁÉÍÓÚÑáéíóúñ]+)\.? ([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+))", texto or ""):
            previo, apellido = m.group(1), m.group(2)
            if apellido not in self.reparto or previo[0].islower() and previo.lower() not in self.TITULOS:
                continue
            familia = self.reparto[apellido]
            genero = self.TITULOS.get(previo.lower())
            if genero is None and previo not in familia and previo[0].isupper():
                self.error(donde, f"«{previo} {apellido}»: {apellido} es del reparto ({', '.join(familia)})")
            elif genero and genero not in familia.values():
                self.error(donde, f"«{previo} {apellido}»: nadie del reparto con ese apellido es {'hombre' if genero == 'm' else 'mujer'}")

    def reglas_autoria(self, u):
        uid = u.get("id", "?")
        nivel = u.get("nivelInterno")
        for v in u.get("vocabulario", []):
            if not isinstance(v.get("id"), str) or not v["id"]:
                self.error(f"{uid}.vocabulario", f"«{v.get('texto')}» sin id")
        for p in u.get("pasos", []):
            donde = f"{uid}.{p.get('id')}"
            # La app lee el id de cada paso como String: sin él el módulo entero no carga.
            if not isinstance(p.get("id"), str) or not p["id"]:
                self.error(donde, f"paso «{p.get('tipo')}» sin id")
            if p.get("tipo") == "tabla":
                titulo = " ".join(str(v) for v in (p.get("titulo") or {}).values()).lower()
                if re.search(r"para le?er|to read", titulo):
                    if len(p.get("filas", [])) > 15:
                        self.error(donde, f"tabla «Para leer» con {len(p['filas'])} filas (máx. 15): reescribe la situación con palabras ya enseñadas")
                    for i, fila in enumerate(p.get("filas", [])):
                        c0 = fila[0] if fila and isinstance(fila[0], dict) else {}
                        t = str(c0.get("texto", "")).strip()
                        # Con minúscula inicial no es nombre propio (alemán «lange» frente al apellido Lange).
                        if t and not t[:1].islower() and all(w in self.libres for w in palabras(t)):
                            self.error(donde, f"fila {i} «{t}»: los nombres propios no llevan fila")
                        if re.search(r"(^[-–])|([-–]$)", t):
                            self.error(donde, f"fila {i} «{t}»: celda suelta; la fila es palabra + sentido + frase")
            if p.get("tipo") == "situacion":
                for i, d in enumerate(p.get("dialogo", [])):
                    self.apellidos(d.get("hablante", ""), f"{donde}.dialogo[{i}].hablante")
                    self.apellidos(d.get("texto", ""), f"{donde}.dialogo[{i}]")
                if isinstance(nivel, int) and nivel in self.LECTURA:
                    mn, mx, unidad = self.LECTURA[nivel]
                    dialogo = p.get("dialogo", [])
                    n = len(dialogo) if unidad == "líneas" else len(palabras(" ".join(d.get("texto", "") for d in dialogo)))
                    if not mn <= n <= mx:
                        self.error(donde, f"la lectura tiene {n} {unidad}; en el nivel {nivel}: {mn}–{mx}")
                if isinstance(nivel, int) and nivel >= 3:
                    for it in p.get("items", []):
                        if it.get("formato") in ("elegir", "escuchar") and any(isinstance(o, dict) for o in it.get("opciones", [])):
                            self.error(f"{donde}.{it.get('id')}", "desde el nivel 3 las opciones de comprensión van en el idioma meta: enseña la palabra o reformula")

    def grafo(self, unidades):
        for uid, u in unidades.items():
            if not str(uid).startswith(f"{self.idioma}."):
                self.error(uid, "el id debe empezar por el código de idioma")
            for p in u.get("prerequisitos", []):
                if p not in unidades:
                    self.error(uid, f"prerrequisito inexistente {p}")
                elif unidades[p].get("orden", 0) >= u.get("orden", 0):
                    self.error(uid, f"orden no posterior a su prerrequisito {p}")
        estado = {}

        def visitar(uid, pila):
            if estado.get(uid) == 1:
                self.error(uid, "ciclo de prerrequisitos: " + " → ".join(pila + [uid]))
                return
            if estado.get(uid) == 2 or uid not in unidades:
                return
            estado[uid] = 1
            for p in unidades[uid].get("prerequisitos", []):
                visitar(p, pila + [uid])
            estado[uid] = 2

        for uid in unidades:
            visitar(uid, [])

    @staticmethod
    def _cadena(u, unidades):
        """La unidad y todos sus prerrequisitos (iterativo: la ruta de inglés
        encadena ~1000 unidades y la recursión superaría el límite de Python)."""
        vistos, pila = set(), [u]
        while pila:
            x = pila.pop()
            if x["id"] in vistos:
                continue
            vistos.add(x["id"])
            yield x
            pila.extend(unidades[p] for p in x.get("prerequisitos", []) if p in unidades)

    def conocidas(self, u, unidades, vistos=None):
        res = set()
        for x in self._cadena(u, unidades):
            if getattr(self, "estricto", False):
                mostrados = {r for p in x.get("pasos", []) if p.get("tipo") == "vocabulario" for r in p.get("refs", [])}
                res |= {w for v in x.get("vocabulario", []) if v.get("id") in mostrados
                        for w in palabras(v.get("texto", ""))}
                res |= {w for p in x.get("pasos", []) if p.get("tipo") in ("ejemplos", "patron")
                        for e in p.get("items", p.get("ejemplos", [])) for w in palabras(e.get("texto", ""))}
            else:
                res |= {w for v in x.get("vocabulario", []) for w in palabras(v.get("texto", ""))}
            # Las celdas de las tablas (escrituras, conjugaciones) también enseñan.
            res |= {w for p in x.get("pasos", []) if p.get("tipo") == "tabla"
                    for fila in p.get("filas", []) for c in fila if isinstance(c, dict) and "texto" in c
                    for w in palabras(c["texto"])}
        return res

    def de_errores(self, u, unidades, vistos=None):
        """Palabras de las frases incorrectas enseñadas (unidad y prerrequisitos)."""
        return {w for x in self._cadena(u, unidades) for e in x.get("erroresFrecuentes", [])
                for w in palabras(re.sub(r"\([^)]*\)", " ", e.get("incorrecto", "")))}

    def unidad(self, u, unidades, libres):
        uid = u.get("id", "?")
        for campo in ("orden", "titulo", "objetivo", "cefr", "concepto", "prerequisitos",
                      "habilidades", "vocabulario", "erroresFrecuentes", "pasos", "criterioDominio"):
            if campo not in u:
                self.error(uid, f"falta campo {campo}")
        if "nivelInterno" not in u:
            self.error(uid, "falta campo nivelInterno")
        self.apoyo(u.get("titulo"), f"{uid}.titulo")
        self.apoyo(u.get("objetivo"), f"{uid}.objetivo")
        vocab_ids = set()
        for v in u.get("vocabulario", []):
            if v.get("id") in vocab_ids:
                self.error(uid, f"vocablo duplicado {v.get('id')}")
            vocab_ids.add(v.get("id"))
            if not v.get("texto"):
                self.error(uid, f"vocablo sin texto {v.get('id')}")
            self.apoyo(v.get("traduccion"), f"{uid}.vocabulario.{v.get('id')}")
            if "nota" in v:
                self.apoyo(v["nota"], f"{uid}.vocabulario.{v.get('id')}.nota")
        if not u.get("vocabulario"):
            self.error(uid, "unidad sin vocabulario")
        if not u.get("erroresFrecuentes"):
            self.error(uid, "sin erroresFrecuentes")
        for i, e in enumerate(u.get("erroresFrecuentes", [])):
            self.apoyo(e.get("explicacion"), f"{uid}.erroresFrecuentes[{i}]")
        umbral = (u.get("criterioDominio") or {}).get("umbral")
        if not isinstance(umbral, (int, float)) or not 0.5 <= umbral <= 1:
            self.error(uid, "criterioDominio.umbral debe estar entre 0.5 y 1")
        conocidas = set(libres)
        declaradas = {
            palabra
            for vocablo in u.get("vocabulario", [])
            for palabra in palabras(vocablo.get("texto", ""))
        }
        for p in u.get("prerequisitos", []):
            if p in unidades:
                conocidas |= self.conocidas(unidades[p], unidades)
        # Las formas incorrectas enseñadas como error solo valen como distractor.
        errores_distractor = self.de_errores(u, unidades)
        self.distractores = conocidas | errores_distractor
        pasos = u.get("pasos", [])
        if not pasos or pasos[0].get("tipo") not in ENSENAR:
            self.error(uid, "la unidad debe empezar enseñando (explicacion/ejemplos/vocabulario/patron)")
        rango_prev = -1
        tipos = set()
        paso_ids = set()
        item_ids = set()
        evidencia = set()
        huellas = {}
        for p in pasos:
            pid, tipo = p.get("id"), p.get("tipo")
            donde = f"{uid}.{pid}"
            if pid in paso_ids:
                self.error(donde, "id de paso duplicado")
            paso_ids.add(pid)
            clase = "ensenar" if tipo in ENSENAR else tipo
            if clase not in ORDEN_TIPOS:
                self.error(donde, f"tipo desconocido {tipo}")
                continue
            rango = ORDEN_TIPOS.index(clase)
            if rango < rango_prev:
                self.error(donde, f"'{tipo}' fuera de orden (enseñar → guiada → independiente → situación → evaluación)")
            rango_prev = max(rango_prev, rango)
            tipos.add(clase)
            if tipo == "explicacion":
                self.apoyo(p.get("texto"), f"{donde}.texto")
                evidencia.add("gramatica")
            if tipo in ("ejemplos", "patron"):
                for i, e in enumerate(p.get("items", p.get("ejemplos", []))):
                    texto = e.get("texto", "")
                    # Ejemplos y patrones son pasos de enseñanza: pueden
                    # introducir vocablos declarados, pero no palabras ajenas
                    # al vocabulario/prerrequisitos de la unidad.
                    self.meta(texto, conocidas | declaradas, f"{donde}.ejemplo[{i}]")
                    conocidas |= set(palabras(texto))
                    self.apoyo(e.get("traduccion"), f"{donde}.ejemplo[{i}].traduccion")
            if tipo == "patron":
                evidencia.add("gramatica")
                for i, f in enumerate(p.get("formula", [])):
                    # La fórmula puede contener etiquetas metalingüísticas
                    # (subject, noun, raíz, +, →); no constituye por sí sola
                    # exposición de vocabulario meta.
                    if "nota" in f:
                        self.apoyo(f["nota"], f"{donde}.formula[{i}].nota")
                if "texto" in p:
                    self.apoyo(p["texto"], f"{donde}.texto")
            if tipo == "tabla":
                evidencia.add("gramatica")
                evidencia.add("escritura")
                if not p.get("filas"):
                    self.error(donde, "tabla sin filas")
                for k in ("titulo", "texto"):
                    if k in p:
                        self.apoyo(p[k], f"{donde}.{k}")
                for i, col in enumerate(p.get("columnas", [])):
                    self.apoyo(col, f"{donde}.columnas[{i}]")
                ancho = len(p.get("columnas", [])) or None
                for i, fila in enumerate(p.get("filas", [])):
                    if ancho and len(fila) != ancho:
                        self.error(donde, f"fila {i} con {len(fila)} celdas; columnas: {ancho}")
                    for j, c in enumerate(fila):
                        if not isinstance(c, dict) or not ("texto" in c or "apoyo" in c):
                            self.error(donde, f"celda [{i}][{j}] debe ser {{texto, rom?}} o {{apoyo}}")
                        elif "apoyo" in c:
                            self.apoyo(c["apoyo"], f"{donde}.celda[{i}][{j}]")
                        elif "texto" in c:
                            texto = c.get("texto", "")
                            # Una tabla es material explícito de enseñanza
                            # (alfabetos, silabarios y conjugaciones). Sus
                            # celdas meta introducen el contenido que muestran.
                            conocidas |= set(palabras(texto))
            if tipo == "vocabulario":
                evidencia.add("vocabulario")
                for r in p.get("refs", []):
                    if r not in vocab_ids:
                        self.error(donde, f"ref de vocabulario inexistente {r}")
                # `vocabulario` es el lexicón declarado de la unidad; `refs`
                # decide qué tarjetas se muestran al alumno. El compilador
                # puede declarar formas de transferencia, nombres propios o
                # flexiones necesarias para validar ejercicios sin convertir
                # cada distractor y cada frase completa en una tarjeta visible.
                if self.estricto:
                    por_id = {v.get("id"): v for v in u.get("vocabulario", [])}
                    conocidas |= {w for r in p.get("refs", []) if r in por_id
                                  for w in palabras(por_id[r].get("texto", ""))}
                else:
                    conocidas |= declaradas
            if tipo in ENSENAR:
                # Una vez mostrado por un paso de enseñanza, el vocabulario
                # también puede utilizarse como distractor legítimo.
                self.distractores = conocidas | errores_distractor
            if tipo == "situacion":
                evidencia.add("lectura")
                self.apoyo(p.get("contexto"), f"{donde}.contexto")
                if not p.get("dialogo"):
                    self.error(donde, "situación sin diálogo modelo")
                for i, d in enumerate(p.get("dialogo", [])):
                    self.meta(d.get("texto", ""), conocidas, f"{donde}.dialogo[{i}]")
                    self.apoyo(d.get("traduccion"), f"{donde}.dialogo[{i}].traduccion")
            if "items" in p and tipo not in ("ejemplos",):
                if not p["items"]:
                    self.error(donde, "paso sin ítems")
                formatos = set()
                for it in p["items"]:
                    iid = it.get("id")
                    if iid in item_ids:
                        self.error(donde, f"id de ítem duplicado {iid}")
                    item_ids.add(iid)
                    formatos.add(it.get("formato"))
                    self.item(it, tipo, conocidas, f"{donde}.{iid}")
                if tipo in ("practica_guiada", "practica_independiente", "evaluacion"):
                    huella = {huella_item(it) for it in p["items"]}
                    if huella:
                        huellas.setdefault(tipo, []).append((donde, huella))
                if any(it.get("formato") in ("escribir", "ordenar", "completar") for it in p["items"]):
                    evidencia.add("escritura")
                if tipo == "evaluacion" and (len(p["items"]) < 4 or len(formatos) < 2):
                    self.error(donde, "la evaluación necesita ≥ 4 ítems y ≥ 2 formatos")
        for requerido in ("practica_guiada", "situacion", "evaluacion"):
            if requerido not in tipos:
                self.error(uid, f"falta un paso '{requerido}'")
        if pasos and pasos[-1].get("tipo") != "evaluacion":
            self.error(uid, "la evaluación debe ser el último paso")
        for habilidad in set(u.get("habilidades", [])) & {"gramatica", "vocabulario", "lectura", "escritura"}:
            if habilidad not in evidencia:
                self.error(uid, f"habilidad declarada sin evidencia determinista: {habilidad}")
        for a in ("practica_guiada", "practica_independiente"):
            for da, ha in huellas.get(a, []):
                for db, hb in huellas.get("evaluacion", []):
                    if ha & hb:
                        self.advertencia(uid, f"contaminación: ítems exactos reutilizados entre {da} y {db}")

    def meta(self, texto, conocidas, donde):
        prueba = conocida_para(self.idioma)
        faltan = [w for w in palabras(texto) if not prueba(w, conocidas)]
        if faltan:
            self.error(donde, f"usa palabras no enseñadas: {', '.join(sorted(set(faltan)))}")

    def item(self, it, tipo, conocidas, donde):
        f = it.get("formato")
        if f not in FORMATOS:
            self.error(donde, f"formato desconocido {f}")
            return
        self.apoyo(it.get("consigna"), f"{donde}.consigna")
        self.apoyo(it.get("feedback"), f"{donde}.feedback")
        if tipo == "practica_guiada":
            self.apoyo(it.get("pista"), f"{donde}.pista")
        elif "pista" in it:
            self.error(donde, "solo la práctica guiada lleva pista")
        if f in ("elegir", "escuchar"):
            ops = it.get("opciones") or []
            if len(ops) < 2:
                self.error(donde, "necesita ≥ 2 opciones")
            r = it.get("respuesta")
            if not isinstance(r, int) or not 0 <= r < len(ops):
                self.error(donde, "respuesta debe ser un índice válido")
            for i, o in enumerate(ops):
                if isinstance(o, dict):
                    self.apoyo(o, f"{donde}.opciones[{i}]")
                else:
                    permitidas = conocidas if i == r else self.distractores
                    self.meta(str(o), permitidas, f"{donde}.opciones[{i}]")
            if "pregunta" in it:
                self.meta(it["pregunta"], conocidas, f"{donde}.pregunta")
            if "preguntaApoyo" in it:
                self.apoyo(it["preguntaApoyo"], f"{donde}.preguntaApoyo")
            if f == "escuchar":
                if not it.get("audio"):
                    self.error(donde, "escuchar necesita audio")
                self.meta(it.get("audio", ""), conocidas, f"{donde}.audio")
        elif f == "ordenar":
            tokens = it.get("tokens") or []
            resp = it.get("respuesta", "")
            if sorted(palabras(" ".join(tokens))) != sorted(palabras(resp)):
                self.error(donde, "tokens no coinciden con la respuesta")
            self.meta(resp, conocidas, f"{donde}.respuesta")
        elif f in ("completar", "escribir"):
            if not it.get("respuesta"):
                self.error(donde, "falta respuesta")
            if f == "completar" and "___" not in it.get("texto", ""):
                self.error(donde, "completar necesita '___' en texto")
            # La app escribe la respuesta en todos los huecos: uno solo por ítem.
            if f == "completar" and it.get("texto", "").count("___") > 1:
                self.error(donde, "completar con más de un '___' (la app admite un solo hueco)")
            # La app acepta el modelo de una producción abierta solo si llega al mínimo.
            if it.get("abierta") and it.get("minimoPalabras"):
                n = len(re.sub(r"[^\w'’\-]+", " ", it.get("respuesta", "")).split())
                if n < it["minimoPalabras"]:
                    self.error(donde, f"el modelo tiene {n} palabras, menos que minimoPalabras ({it['minimoPalabras']})")
            self.meta(it.get("texto", ""), conocidas, f"{donde}.texto")
            self.meta(it.get("respuesta", ""), conocidas, f"{donde}.respuesta")
            for o in it.get("opciones", []):
                permitidas = conocidas if palabras(str(o)) == palabras(it.get("respuesta", "")) else self.distractores
                self.meta(str(o), permitidas, f"{donde}.opciones")
            if it.get("audio"):
                self.meta(it["audio"], conocidas, f"{donde}.audio")
        elif f == "relacionar":
            pares = it.get("pares") or []
            if not 3 <= len(pares) <= 5:
                self.error(donde, "relacionar necesita 3–5 pares")
            for i, (meta, ap) in enumerate(pares):
                self.meta(meta, conocidas, f"{donde}.pares[{i}]")
                self.apoyo(ap, f"{donde}.pares[{i}]")


def main():
    args = sys.argv[1:]
    borradores = []
    if "--borrador" in args:
        i = args.index("--borrador")
        args, borradores = args[:i], args[i + 1:]
    idiomas = args or sorted(p.name for p in RAIZ.iterdir() if (p / "ruta").is_dir())
    errores = []
    advertencias = []
    for idioma in idiomas:
        validador = Validador(idioma, borradores if len(idiomas) == 1 else ())
        errores += validador.validar()
        advertencias += validador.advertencias
    for e in errores:
        print(e)
    for e in advertencias:
        print("WARN " + e)
    print(f"{len(idiomas)} idioma(s) · {len(errores)} error(es)")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
