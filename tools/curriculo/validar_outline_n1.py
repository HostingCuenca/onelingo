#!/usr/bin/env python3
"""Valida el outline N1 previo a las fichas con ejercicios.

Uso: python3 tools/curriculo/validar_outline_n1.py pt
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[2]


def main() -> None:
    idioma = sys.argv[1] if len(sys.argv) > 1 else 'pt'
    ruta = RAIZ / 'tools' / 'curriculo' / idioma / 'n1-outline.json'
    f0 = RAIZ / 'curriculo' / idioma / 'f0.json'
    marco = json.loads((RAIZ / 'curriculo' / 'marco.json').read_text(encoding='utf-8'))
    datos = json.loads(ruta.read_text(encoding='utf-8'))
    base = json.loads(f0.read_text(encoding='utf-8'))
    errores: list[str] = []

    def bilingue(valor, donde):
        if not (
            isinstance(valor, dict)
            and all(isinstance(valor.get(k), str) and valor[k].strip() for k in ('es', 'en'))
        ):
            errores.append(f'{donde}: falta texto ES/EN')

    if (datos.get('idioma'), datos.get('nivel'), datos.get('cefr')) != (idioma, 1, 'A1'):
        errores.append('raíz: idioma/nivel/cefr incorrectos')
    bilingue(datos.get('nota'), 'raíz.nota')
    esperados = base.get('previos', []) + base.get('clavesSalida', [])
    if datos.get('previos') != esperados:
        errores.append('raíz.previos: no son las 16 claves Nivel 0 + 24 de Fundamentos')

    nivel1 = next(n for n in marco['niveles'] if n['nivel'] == 1)
    situaciones = {b['bloque']: set(b['situaciones']) for b in nivel1['bloques']}
    clases = datos.get('clases', [])
    if len(clases) != 50:
        errores.append(f'raíz.clases: se esperan 50, hay {len(clases)}')
    if Counter(c.get('bloque') for c in clases) != Counter({i: 5 for i in range(1, 11)}):
        errores.append('raíz.clases: deben ser 5 por bloque')

    conocidas = set(esperados)
    introduccion: dict[str, int] = {}
    for i, clase in enumerate(clases, 1):
        cid = str(clase.get('id', f'C{i:02d}'))
        if clase.get('id') != f'{idioma}.n1.c{i:02d}':
            errores.append(f'{cid}: id fuera de secuencia')
        bloque = (i - 1) // 5 + 1
        if clase.get('bloque') != bloque:
            errores.append(f'{cid}: bloque incorrecto')
        for campo in ('titulo', 'objetivo', 'tarea'):
            bilingue(clase.get(campo), f'{cid}.{campo}')
        if clase.get('estado') != 'esqueleto':
            errores.append(f'{cid}: el outline debe mantener estado esqueleto')
        if not isinstance(clase.get('sonido'), str) or not clase['sonido'].strip():
            errores.append(f'{cid}: falta sonido concreto')
        if not (
            isinstance(clase.get('gramatica'), list)
            and clase['gramatica']
            and all(isinstance(x, str) and x.strip() for x in clase['gramatica'])
        ):
            errores.append(f'{cid}: gramática vacía')

        nuevas = clase.get('introduce')
        if not isinstance(nuevas, list):
            errores.append(f'{cid}: introduce debe ser lista')
            nuevas = []
        if bloque < 10 and not nuevas:
            errores.append(f'{cid}: clase temática sin clave nueva')
        if cid == f'{idioma}.n1.c50' and nuevas:
            errores.append(f'{cid}: el cierre no introduce gramática')
        for clave in nuevas:
            if clave in conocidas:
                errores.append(f'{cid}: clave repetida {clave}')
            conocidas.add(clave)
            introduccion[clave] = i - 1
        for clave in clase.get('recicla', []):
            if clave not in conocidas - set(nuevas):
                errores.append(f'{cid}: recicla clave futura/desconocida {clave}')

        vocabulario = clase.get('vocabulario', {})
        bilingue(vocabulario.get('campo'), f'{cid}.vocabulario.campo')
        palabras = vocabulario.get('palabras')
        if not (
            isinstance(palabras, list)
            and 6 <= len(palabras) <= 12
            and all(isinstance(x, str) and x.strip() for x in palabras)
        ):
            errores.append(f'{cid}: se esperan 6–12 vocablos')
        if clase.get('situacion') not in situaciones[bloque]:
            errores.append(f'{cid}: situación fuera del bloque del marco')

        texto_obj = ' '.join((clase.get('objetivo') or {}).values()).lower()
        texto_tar = ' '.join((clase.get('tarea') or {}).values()).lower()
        if 'situación cotidiana de nivel' in texto_obj or 'realiza esta tarea' in texto_tar:
            errores.append(f'{cid}: conserva texto genérico')

    if len(introduccion) != 49:
        errores.append(f'raíz: se esperan 49 claves nuevas, hay {len(introduccion)}')

    # Para las claves con espacio suficiente: repaso inmediato, a +2/+3 y a +6…+8.
    for clave, origen in introduccion.items():
        apariciones = [
            i - origen for i, clase in enumerate(clases[origen + 1:], origen + 1)
            if clave in clase.get('recicla', [])
        ]
        if origen <= 42:
            if 1 not in apariciones:
                errores.append(f'{clave}: falta repaso inmediato')
            if not any(x in apariciones for x in (2, 3)):
                errores.append(f'{clave}: falta repaso +2/+3')
            if not any(6 <= x <= 8 for x in apariciones):
                errores.append(f'{clave}: falta repaso aproximado +7')
        elif origen < 49 and not apariciones:
            errores.append(f'{clave}: falta cierre antes de terminar N1')

    for error in errores:
        print('ERROR:', error)
    print(
        f'{len(errores)} errores · {len(clases)} clases · '
        f'{len(introduccion)} claves nuevas · {len(esperados)} previos'
    )
    raise SystemExit(1 if errores else 0)


if __name__ == '__main__':
    main()
