#!/usr/bin/env python3
"""Valida un outline de 50 clases para N2–N10 antes de poblar ejercicios.

Uso:
  python3 tools/curriculo/validar_outline_nivel.py pt 2 /tmp/n2-outline.json
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[2]
GENERICO = re.compile(r'\bparte\s+\d+\b|repaso integrado de n\d+|realiza esta tarea', re.I)


def main() -> None:
    idioma = sys.argv[1] if len(sys.argv) > 1 else 'pt'
    nivel = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    ruta = Path(sys.argv[3]) if len(sys.argv) > 3 else (
        RAIZ / 'tools' / 'curriculo' / idioma / f'n{nivel}-outline.json'
    )
    if nivel < 2:
        raise SystemExit('para N1 usa validar_outline_n1.py')

    marco = json.loads((RAIZ / 'curriculo' / 'marco.json').read_text(encoding='utf-8'))
    previo_p = RAIZ / 'curriculo' / idioma / f'n{nivel - 1}.json'
    if not previo_p.exists():  # nivel anterior aún en esqueleto
        previo_p = RAIZ / 'tools' / 'curriculo' / idioma / f'n{nivel - 1}-outline.json'
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from validar_plan import leer_mapa  # noqa: E402
    mapa = leer_mapa(idioma).get(nivel, {})
    claves_mapa = [k for b in sorted(mapa) for k in mapa[b]]
    datos = json.loads(ruta.read_text(encoding='utf-8'))
    previo = json.loads(previo_p.read_text(encoding='utf-8'))
    errores: list[str] = []

    def bilingue(valor, donde):
        if not (
            isinstance(valor, dict)
            and all(isinstance(valor.get(k), str) and valor[k].strip() for k in ('es', 'en'))
        ):
            errores.append(f'{donde}: falta texto ES/EN')

    nivel_marco = next(n for n in marco['niveles'] if n['nivel'] == nivel)
    if (datos.get('idioma'), datos.get('nivel'), datos.get('cefr')) != (
        idioma, nivel, nivel_marco['cefr']
    ):
        errores.append('raíz: idioma/nivel/cefr incorrectos')
    bilingue(datos.get('nota'), 'raíz.nota')

    esperados = list(previo.get('previos', []))
    for clase in previo.get('clases', []):
        for clave in clase.get('introduce', []):
            if clave not in esperados:
                esperados.append(clave)
    if datos.get('previos') != esperados:
        errores.append(f'raíz.previos: deben ser las {len(esperados)} claves disponibles al cerrar N{nivel - 1}')

    situaciones = {b['bloque']: set(b['situaciones']) for b in nivel_marco['bloques']}
    clases = datos.get('clases', [])
    if len(clases) != 50:
        errores.append(f'raíz.clases: se esperan 50, hay {len(clases)}')
    if Counter(c.get('bloque') for c in clases) != Counter({i: 5 for i in range(1, 11)}):
        errores.append('raíz.clases: deben ser 5 por bloque')

    conocidas = set(esperados)
    introduccion: dict[str, int] = {}
    titulos: Counter[str] = Counter()
    objetivos: Counter[str] = Counter()
    tareas: Counter[str] = Counter()
    for i, clase in enumerate(clases, 1):
        cid = str(clase.get('id', f'C{i:02d}'))
        if clase.get('id') != f'{idioma}.n{nivel}.c{i:02d}':
            errores.append(f'{cid}: id fuera de secuencia')
        bloque = (i - 1) // 5 + 1
        if clase.get('bloque') != bloque:
            errores.append(f'{cid}: bloque incorrecto')
        for campo in ('titulo', 'objetivo', 'tarea'):
            bilingue(clase.get(campo), f'{cid}.{campo}')
        titulos[str((clase.get('titulo') or {}).get('es', '')).strip()] += 1
        objetivos[str((clase.get('objetivo') or {}).get('es', '')).strip()] += 1
        tareas[str((clase.get('tarea') or {}).get('es', '')).strip()] += 1
        textos = ' '.join(
            str((clase.get(campo) or {}).get('es', ''))
            for campo in ('titulo', 'objetivo', 'tarea')
        )
        if GENERICO.search(textos):
            errores.append(f'{cid}: conserva título/objetivo/tarea genérico')
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
        if claves_mapa:
            # Con MAPA.md manda el mapa: cada bloque introduce sus claves (0–2 por clase).
            fuera = [k for k in nuevas if k not in mapa.get(bloque, [])]
            if fuera:
                errores.append(f'{cid}: introduce {", ".join(fuera)}, que MAPA.md no da al bloque {bloque}')
            if len(nuevas) > 2 or (i >= 49 and nuevas):
                errores.append(f'{cid}: demasiadas claves nuevas ({len(nuevas)})')
        else:
            esperadas_nuevas = 0 if i >= 49 else 1
            if len(nuevas) != esperadas_nuevas:
                errores.append(f'{cid}: se esperan {esperadas_nuevas} claves nuevas, hay {len(nuevas)}')
        for clave in nuevas:
            if clave in conocidas:
                errores.append(f'{cid}: clave repetida {clave}')
            conocidas.add(clave)
            introduccion[clave] = i - 1
        recicla = clase.get('recicla', [])
        if not isinstance(recicla, list) or not recicla:
            errores.append(f'{cid}: debe declarar reciclaje explícito')
            recicla = []
        if not any(clave in set(esperados) for clave in recicla):
            errores.append(f'{cid}: falta al menos un prerrequisito heredado de N{nivel - 1}')
        for clave in recicla:
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
        if clase.get('situacion') not in situaciones.get(bloque, set()):
            errores.append(f'{cid}: situación fuera del bloque del marco')

    if claves_mapa:
        if sorted(introduccion) != sorted(claves_mapa):
            errores.append(f'raíz: las claves nuevas ({len(introduccion)}) no coinciden con MAPA.md ({len(claves_mapa)})')
    elif len(introduccion) != 48:
        errores.append(f'raíz: se esperan 48 claves nuevas, hay {len(introduccion)}')
    for etiqueta, contador in (
        ('títulos', titulos), ('objetivos', objetivos), ('tareas', tareas)
    ):
        repetidos = [texto for texto, cantidad in contador.items() if texto and cantidad > 1]
        if repetidos:
            errores.append(f'raíz: {len(repetidos)} {etiqueta} repetidos exactamente')

    for clave, origen in introduccion.items():
        if 'transfer' in clave or clave.startswith('integrated-') or clave.startswith('integration-'):
            continue  # claves de integración (5.ª clase del bloque): no se reciclan como gramática
        apariciones = [
            i - origen for i, clase in enumerate(clases[origen + 1:], origen + 1)
            if clave in clase.get('recicla', [])
        ]
        if origen <= 41:
            if 1 not in apariciones:
                errores.append(f'{clave}: falta repaso inmediato')
            if not any(x in apariciones for x in (2, 3)):
                errores.append(f'{clave}: falta repaso +2/+3')
            if not any(6 <= x <= 8 for x in apariciones):
                errores.append(f'{clave}: falta repaso aproximado +7')
        elif origen < 48 and not apariciones:
            errores.append(f'{clave}: falta reciclaje antes del cierre N{nivel}')

    for error in errores:
        print('ERROR:', error)
    print(
        f'{len(errores)} errores · {len(clases)} clases · '
        f'{len(introduccion)} claves nuevas · {len(esperados)} previos'
    )
    raise SystemExit(1 if errores else 0)


if __name__ == '__main__':
    main()
