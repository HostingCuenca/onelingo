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
PUNTUACION = re.compile(r"[.,!?¡¿;:/。、！？「」…\"“”()«»—–，：；]")
CAMPOS_HUELLA = {
    "formato", "consigna", "pregunta", "preguntaApoyo", "opciones", "respuesta",
    "aceptadas", "tokens", "texto", "audio", "pares",
}


def palabras(texto):
    texto = texto.replace("’", "'").replace("___", " ")
    # Comillas simples de cita ('once', shopkeepers') no forman parte de la palabra.
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
        if not unidades:
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
        for p in u.get("pasos", []):
            donde = f"{uid}.{p.get('id')}"
            if p.get("tipo") == "tabla":
                titulo = " ".join(str(v) for v in (p.get("titulo") or {}).values()).lower()
                if re.search(r"para leer|to read", titulo):
                    if len(p.get("filas", [])) > 15:
                        self.error(donde, f"tabla «Para leer» con {len(p['filas'])} filas (máx. 15): reescribe la situación con palabras ya enseñadas")
                    for i, fila in enumerate(p.get("filas", [])):
                        c0 = fila[0] if fila and isinstance(fila[0], dict) else {}
                        t = str(c0.get("texto", "")).strip()
                        if t and all(w in self.libres for w in palabras(t)):
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
        faltan = [w for w in palabras(texto) if not conocida(w, conocidas)]
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
