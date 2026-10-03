#!/usr/bin/env python3
"""Valida el plan de clases (docs/claude-educacion/PLAN_CLASES.md).

- curriculo/marco.json: marco común a todos los idiomas, 10 niveles × 10 bloques.
- curriculo/<idioma>/nX.json: las 50 clases de cada nivel de un idioma.

Uso: python3 tools/curriculo/validar_plan.py [idioma ...]
     (sin idiomas valida solo el marco; con idiomas, el marco y sus niveles)
Sale con código 1 si hay errores.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CURRICULO = RAIZ / 'curriculo'
CEFR = {1: 'A1', 2: 'A2', 3: 'B1', 4: 'B1', 5: 'B2', 6: 'B2', 7: 'B2', 8: 'C1', 9: 'C1', 10: 'C1'}
BLOQUES, CLASES_POR_BLOQUE = 10, 5
ESTADOS = ('planificado', 'escrito', 'revisado', 'publicado')
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

errores, avisos = [], []


def bilingue(v, donde):
    if not (isinstance(v, dict) and all(isinstance(v.get(k), str) and v[k].strip() for k in ('es', 'en'))):
        errores.append(f'{donde}: falta el texto {{es, en}}')


def slugs(v, donde, minimo=0):
    if not isinstance(v, list) or len(v) < minimo:
        errores.append(f'{donde}: se esperan al menos {minimo} claves')
        return []
    for s in v:
        if not isinstance(s, str) or not SLUG.match(s):
            errores.append(f'{donde}: clave no válida {s!r} (minúsculas-con-guiones)')
    return v


def validar_marco():
    p = CURRICULO / 'marco.json'
    if not p.exists():
        errores.append('falta curriculo/marco.json')
        return {}
    m = json.loads(p.read_text(encoding='utf-8'))
    niveles = m.get('niveles', [])
    if [n.get('nivel') for n in niveles] != list(range(1, 11)):
        errores.append('marco: se esperan los niveles 1…10 en orden')
    usadas = set()
    res = {}
    for n in niveles:
        nv = n.get('nivel')
        d = f'marco n{nv}'
        if n.get('cefr') != CEFR.get(nv):
            errores.append(f'{d}: cefr {n.get("cefr")!r}, se espera {CEFR.get(nv)!r}')
        bilingue(n.get('titulo'), f'{d} titulo')
        bilingue(n.get('objetivo'), f'{d} objetivo')
        bloques = n.get('bloques', [])
        if [b.get('bloque') for b in bloques] != list(range(1, BLOQUES + 1)):
            errores.append(f'{d}: se esperan los bloques 1…{BLOQUES} en orden')
        for b in bloques:
            db = f'{d} b{b.get("bloque")}'
            bilingue(b.get('tema'), f'{db} tema')
            bilingue(b.get('objetivo'), f'{db} objetivo')
            slugs(b.get('funciones'), f'{db} funciones', 2)
            slugs(b.get('lexico'), f'{db} lexico', 1)
            sit = b.get('situaciones')
            if not isinstance(sit, list) or not sit or not all(isinstance(s, int) and 1 <= s <= 50 for s in sit):
                errores.append(f'{db}: situaciones debe ser una lista de ids 1…50')
            else:
                usadas.update(sit)
            if b.get('tipo') not in ('tema', 'integracion'):
                errores.append(f'{db}: tipo debe ser tema o integracion')
        if bloques and bloques[-1].get('tipo') != 'integracion':
            errores.append(f'{d}: el bloque {BLOQUES} es de integración (repaso y prueba del nivel)')
        res[nv] = {b.get('bloque'): b for b in bloques}
    faltan = sorted(set(range(1, 51)) - usadas)
    if faltan:
        avisos.append(f'marco: situaciones sin bloque: {faltan}')
    return res


def unidades_existentes(idioma):
    """ids de unidades escritas: publicadas (ruta) o en borrador (tools/contenido/ruta-<idioma>)."""
    pub, bor = {}, {}
    for carpeta, destino in ((RAIZ / f'assets/contenido/{idioma}/ruta', pub),
                             (RAIZ / f'tools/contenido/ruta-{idioma}', bor)):
        for f in sorted(carpeta.glob('*.json')) if carpeta.exists() else []:
            try:
                datos = json.loads(f.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                continue
            for u in datos.get('unidades', []) if isinstance(datos, dict) else []:
                if isinstance(u, dict) and 'id' in u:
                    destino[u['id']] = u
    return pub, bor


FORMATOS = {'elegir', 'escuchar', 'ordenar', 'completar', 'escribir', 'relacionar'}
CUANTOS = {'guiada': (3, 5), 'independiente': (3, 4), 'evaluacion': (4, 8)}


def validar_item(it, d, claves):
    if not isinstance(it, dict):
        errores.append(f'{d}: ejercicio no válido')
        return
    if it.get('formato') not in FORMATOS:
        errores.append(f'{d}: formato {it.get("formato")!r} no válido')
    for campo in ('consigna', 'ejemplo'):
        if not (isinstance(it.get(campo), str) and it[campo].strip()):
            errores.append(f'{d}: falta «{campo}»')
    if it.get('clave') not in claves:
        errores.append(f'{d}: clave {it.get("clave")!r} no está en introduce ni en recicla de la ficha')


def validar_ejercicios(c, d, intro, recicla):
    """Plan de ejercicios de la ficha (PLAN_CLASES.md §2): lo exigen las
    clases planificadas, para que el autor sepa exactamente qué escribir."""
    ej = c.get('ejercicios')
    if not isinstance(ej, dict):
        errores.append(f'{d}: falta el plan de ejercicios')
        return
    claves = set(intro) | set(recicla)
    for paso, (mn, mx) in CUANTOS.items():
        items = ej.get(paso) or []
        if not mn <= len(items) <= mx:
            errores.append(f'{d}: {paso} debe tener {mn}–{mx} ejercicios ({len(items)})')
        for i, it in enumerate(items, 1):
            validar_item(it, f'{d} {paso}[{i}]', claves)
    s = ej.get('situacion') or {}
    if not (isinstance(s.get('texto'), str) and s['texto'].strip()):
        errores.append(f'{d}: falta situacion.texto (qué pasa y quién habla)')
    preg = s.get('preguntas') or []
    if not 1 <= len(preg) <= 2:
        errores.append(f'{d}: la situación lleva 1–2 preguntas de comprensión')
    for i, it in enumerate(preg, 1):
        validar_item(it, f'{d} situacion[{i}]', claves)
    ev = ej.get('evaluacion') or []
    if len({it.get('formato') for it in ev if isinstance(it, dict)}) < 3:
        errores.append(f'{d}: la evaluación usa al menos 3 formatos')
    sin = [k for k in intro if k not in {it.get('clave') for it in ev if isinstance(it, dict)}]
    if sin:
        errores.append(f'{d}: la evaluación no evalúa {", ".join(sin)}')


def leer_mapa(idioma):
    """{nivel: {bloque: [claves]}} de curriculo/<idioma>/MAPA.md, si el idioma
    tiene mapa: fija qué introduce cada bloque (el francés no lo tiene)."""
    p = CURRICULO / idioma / 'MAPA.md'
    mapa, nv, b = {}, None, None
    for linea in p.read_text(encoding='utf-8').splitlines() if p.exists() else []:
        if m := re.match(r'## N(\d+)\b', linea):
            nv = int(m.group(1))
            mapa[nv] = {}
        elif nv and (m := re.match(r'- \*\*B(\d+)\b', linea)):
            b = int(m.group(1))
            mapa[nv][b] = []
        elif nv and b and (m := re.match(r'\s+- `([a-z0-9-]+)`', linea)):
            mapa[nv][b].append(m.group(1))
    return mapa


def validar_idioma(idioma, marco):
    carpeta = CURRICULO / idioma
    if not carpeta.exists():
        errores.append(f'{idioma}: falta curriculo/{idioma}/')
        return
    pub, bor = unidades_existentes(idioma)
    mapa = leer_mapa(idioma)
    introducidas = {}
    palabras = {}
    resumen = []
    for nv in range(1, 11):
        p = carpeta / f'n{nv}.json'
        if not p.exists():
            resumen.append(f'n{nv}: sin plan')
            continue
        datos = json.loads(p.read_text(encoding='utf-8'))
        d0 = f'{idioma} n{nv}'
        if datos.get('idioma') != idioma or datos.get('nivel') != nv or datos.get('cefr') != CEFR[nv]:
            errores.append(f'{d0}: idioma, nivel o cefr no coinciden')
        for k in slugs(datos.get('previos', []), f'{d0} previos'):
            introducidas.setdefault(k, 'previo')
        clases = datos.get('clases', [])
        if len(clases) != BLOQUES * CLASES_POR_BLOQUE:
            errores.append(f'{d0}: {len(clases)} clases, se esperan {BLOQUES * CLASES_POR_BLOQUE}')
        estados = {e: 0 for e in ESTADOS}
        for i, c in enumerate(clases, 1):
            cid = f'{idioma}.n{nv}.c{i:02d}'
            d = f'{d0} {c.get("id")}'
            if c.get('id') != cid:
                errores.append(f'{d}: se espera el id {cid}')
            bloque = (i - 1) // CLASES_POR_BLOQUE + 1
            if c.get('bloque') != bloque:
                errores.append(f'{d}: bloque {c.get("bloque")}, se espera {bloque}')
            mb = marco.get(nv, {}).get(bloque, {})
            for campo in ('titulo', 'objetivo', 'tarea'):
                bilingue(c.get(campo), f'{d} {campo}')
            g = c.get('gramatica')
            if not isinstance(g, list) or not g or not all(isinstance(x, str) and x.strip() for x in g):
                errores.append(f'{d}: gramatica debe ser una lista de puntos')
            intro = slugs(c.get('introduce'), f'{d} introduce')
            if not intro and mb.get('tipo') == 'tema':
                errores.append(f'{d}: una clase de bloque temático introduce al menos un punto nuevo')
            for k in intro:
                if k in introducidas:
                    errores.append(f'{d}: «{k}» ya se introdujo en {introducidas[k]}')
            for k in slugs(c.get('recicla'), f'{d} recicla'):
                if k not in introducidas:
                    errores.append(f'{d}: recicla «{k}», que no se introdujo antes')
            if not c.get('recicla') and cid != f'{idioma}.n1.c01':
                avisos.append(f'{d}: no recicla nada')
            for k in intro:
                introducidas[k] = cid
                if mapa and k not in mapa.get(nv, {}).get(bloque, []):
                    errores.append(f'{d}: introduce «{k}», que MAPA.md no da al bloque {bloque}')
            voc = c.get('vocabulario') or {}
            bilingue(voc.get('campo'), f'{d} vocabulario.campo')
            pals = voc.get('palabras')
            if not isinstance(pals, list) or not 6 <= len(pals) <= 12:
                errores.append(f'{d}: vocabulario.palabras debe tener 6–12 palabras')
            else:
                for w in pals:
                    if w in palabras:
                        avisos.append(f'{d}: «{w}» ya es vocabulario de {palabras[w]}')
                    palabras.setdefault(w, cid)
            if nv == 1 and not (isinstance(c.get('sonido'), str) and c['sonido'].strip()):
                errores.append(f'{d}: en N1 cada clase abre con un sonido del Nivel 0')
            s = c.get('situacion')
            if not isinstance(s, int) or not 1 <= s <= 50:
                errores.append(f'{d}: situacion debe ser un id 1…50')
            elif mb and s not in mb.get('situaciones', []):
                avisos.append(f'{d}: la situación {s} no está en el bloque {bloque} del marco')
            e = c.get('estado')
            if e == 'planificado' or c.get('ejercicios'):
                validar_ejercicios(c, d, intro, c.get('recicla') or [])
            if e not in ESTADOS:
                errores.append(f'{d}: estado {e!r} no válido')
                continue
            estados[e] += 1
            if e == 'publicado' and cid not in pub:
                errores.append(f'{d}: marcada publicada pero no está en assets/contenido/{idioma}/ruta')
            if e in ('escrito', 'revisado') and cid not in pub and cid not in bor:
                errores.append(f'{d}: marcada {e} pero no hay unidad con ese id')
            u = pub.get(cid) or bor.get(cid)
            if u and isinstance(u.get('titulo'), dict) and u['titulo'] != c.get('titulo'):
                avisos.append(f'{d}: el título de la unidad difiere del plan')
        if mapa and len(clases) == BLOQUES * CLASES_POR_BLOQUE:
            for b, ks in mapa.get(nv, {}).items():
                falta = [k for k in ks if introducidas.get(k, '').split('.')[1:2] != [f'n{nv}']]
                if falta:
                    errores.append(f'{d0} b{b}: MAPA.md pide introducir {", ".join(falta)}')
        resumen.append(f'n{nv}: ' + ', '.join(f'{v} {k}' for k, v in estados.items() if v))
    print(f'{idioma}: ' + ' · '.join(resumen))


def main():
    idiomas = sys.argv[1:]
    marco = validar_marco()
    for idioma in idiomas:
        validar_idioma(idioma, marco)
    for a in avisos:
        print('aviso:', a)
    for e in errores:
        print('ERROR:', e)
    print(f'{len(errores)} errores, {len(avisos)} avisos')
    sys.exit(1 if errores else 0)


if __name__ == '__main__':
    main()
