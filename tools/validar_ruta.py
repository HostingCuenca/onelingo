#!/usr/bin/env python3
"""Valida las rutas de aprendizaje (assets/contenido/<idioma>/ruta/).

Uso: python3 tools/validar_ruta.py [idioma ...]   (sin argumentos: todos)
Sale con código 1 si hay errores. Reglas en docs/claude-educacion/ESQUEMA_CONTENIDO.md.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "assets" / "contenido"
ENSENAR = {"explicacion", "ejemplos", "vocabulario", "patron", "tabla"}
ORDEN_TIPOS = ["ensenar", "practica_guiada", "practica_independiente", "situacion", "evaluacion"]
FORMATOS = {"elegir", "escuchar", "ordenar", "completar", "escribir", "relacionar"}
PUNTUACION = re.compile(r"[.,!?¡¿;:。、！？「」…\"“”()«»—–，：；]")


def palabras(texto):
    texto = texto.replace("’", "'").replace("___", " ")
    return [p for p in PUNTUACION.sub(" ", texto.lower()).split() if p and p != "-"]


class Validador:
    def __init__(self, idioma):
        self.idioma = idioma
        self.errores = []

    def error(self, donde, msg):
        self.errores.append(f"[{self.idioma}] {donde}: {msg}")

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
        if not unidades:
            self.error("curso", "sin unidades")
        self.grafo(unidades)
        for u in unidades.values():
            self.unidad(u, unidades, libres)
        return self.errores

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

    def conocidas(self, u, unidades, vistos=None):
        vistos = vistos if vistos is not None else set()
        if u["id"] in vistos:
            return set()
        vistos.add(u["id"])
        res = {w for v in u.get("vocabulario", []) for w in palabras(v.get("texto", ""))}
        # Las celdas de las tablas (escrituras, conjugaciones) también enseñan.
        res |= {w for p in u.get("pasos", []) if p.get("tipo") == "tabla"
                for fila in p.get("filas", []) for c in fila if isinstance(c, dict) and "texto" in c
                for w in palabras(c["texto"])}
        for p in u.get("prerequisitos", []):
            if p in unidades:
                res |= self.conocidas(unidades[p], unidades, vistos)
        return res

    def de_errores(self, u, unidades, vistos=None):
        """Palabras de las frases incorrectas enseñadas (unidad y prerrequisitos)."""
        vistos = vistos if vistos is not None else set()
        if u["id"] in vistos:
            return set()
        vistos.add(u["id"])
        res = {w for e in u.get("erroresFrecuentes", [])
               for w in palabras(re.sub(r"\([^)]*\)", " ", e.get("incorrecto", "")))}
        for p in u.get("prerequisitos", []):
            if p in unidades:
                res |= self.de_errores(unidades[p], unidades, vistos)
        return res

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
        conocidas = self.conocidas(u, unidades) | libres
        # Las formas incorrectas enseñadas como error solo valen como distractor.
        self.distractores = conocidas | self.de_errores(u, unidades)
        pasos = u.get("pasos", [])
        if not pasos or pasos[0].get("tipo") not in ENSENAR:
            self.error(uid, "la unidad debe empezar enseñando (explicacion/ejemplos/vocabulario/patron)")
        rango_prev = -1
        tipos = set()
        paso_ids = set()
        item_ids = set()
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
            if tipo in ("ejemplos", "patron"):
                for i, e in enumerate(p.get("items", p.get("ejemplos", []))):
                    self.meta(e.get("texto", ""), conocidas, f"{donde}.ejemplo[{i}]")
                    self.apoyo(e.get("traduccion"), f"{donde}.ejemplo[{i}].traduccion")
            if tipo == "patron":
                for i, f in enumerate(p.get("formula", [])):
                    if "nota" in f:
                        self.apoyo(f["nota"], f"{donde}.formula[{i}].nota")
                if "texto" in p:
                    self.apoyo(p["texto"], f"{donde}.texto")
            if tipo == "tabla":
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
            if tipo == "vocabulario":
                for r in p.get("refs", []):
                    if r not in vocab_ids:
                        self.error(donde, f"ref de vocabulario inexistente {r}")
            if tipo == "situacion":
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
                if tipo == "evaluacion" and (len(p["items"]) < 4 or len(formatos) < 2):
                    self.error(donde, "la evaluación necesita ≥ 4 ítems y ≥ 2 formatos")
        for requerido in ("practica_guiada", "situacion", "evaluacion"):
            if requerido not in tipos:
                self.error(uid, f"falta un paso '{requerido}'")
        if pasos and pasos[-1].get("tipo") != "evaluacion":
            self.error(uid, "la evaluación debe ser el último paso")

    def meta(self, texto, conocidas, donde):
        faltan = [w for w in palabras(texto) if w not in conocidas]
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
    idiomas = sys.argv[1:] or sorted(p.name for p in RAIZ.iterdir() if (p / "ruta").is_dir())
    errores = []
    for idioma in idiomas:
        errores += Validador(idioma).validar()
    for e in errores:
        print(e)
    print(f"{len(idiomas)} idioma(s) · {len(errores)} error(es)")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
