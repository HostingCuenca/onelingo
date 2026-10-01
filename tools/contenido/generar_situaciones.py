#!/usr/bin/env python3
"""Genera las copias de las situaciones desde su fuente única.

Fuente (docs/claude-educacion/SITUACIONES_V2.md):
  assets/contenido/situaciones/catalogo.json       las 50 (nombre, categoría, icono, color)
  assets/contenido/<idioma>/situaciones.json       contenido por tramo

Genera (no editar a mano):
  lib/core/content/catalogo_situaciones.g.dart     lista de la app
  web/avatar/topics.json                           temas de la videollamada
  backend/src/content/situaciones-<idioma>.json    contenido para el tutor IA

Uso: python3 tools/contenido/generar_situaciones.py [--comprobar]
Con --comprobar no escribe: sale con 1 si algún generado está desactualizado.
"""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
CATALOGO = RAIZ / 'assets/contenido/situaciones/catalogo.json'


def cargar(p):
    return json.loads(p.read_text(encoding='utf-8'))


def dart(catalogo):
    lineas = [
        '// GENERADO por tools/contenido/generar_situaciones.py desde',
        '// assets/contenido/situaciones/catalogo.json. No editar a mano.',
        '',
        "import 'package:flutter/material.dart';",
        '',
        "import '../../app/theme.dart';",
        "import '../models/models.dart';",
        '',
        '/// Las 50 situaciones de práctica (contenido por tramo en',
        '/// `assets/contenido/<idioma>/situaciones.json`).',
        'const situaciones = <Situation>[',
    ]
    for s in catalogo['situaciones']:
        nombre = s['nombre'].replace("'", "\\'")
        lineas.append(
            f"  Situation(id: {s['id']}, nombre: '{nombre}', "
            f"categoria: '{s['categoria']}', icono: Icons.{s['icono']}, "
            f"color: OL.{s['color']}),"
        )
    lineas += [
        '];',
        '',
        'Situation situacion(int id) => situaciones[id - 1];',
        '',
    ]
    return '\n'.join(lineas)


def temas(catalogo):
    return json.dumps(
        [{'id': s['id'], 'nombre': s['nombre']} for s in catalogo['situaciones']],
        ensure_ascii=False,
    ) + '\n'


def backend(catalogo, contenido):
    nombres = {s['id']: s['nombre'] for s in catalogo['situaciones']}
    return json.dumps(
        {
            'version': contenido['version'],
            'idioma': contenido['idioma'],
            'situaciones': [
                {'id': s['id'], 'nombre': nombres[s['id']], 'tramos': s['tramos']}
                for s in contenido['situaciones']
            ],
        },
        ensure_ascii=False,
        indent=1,
    ) + '\n'


def salidas():
    catalogo = cargar(CATALOGO)
    ids = [s['id'] for s in catalogo['situaciones']]
    assert ids == list(range(1, len(ids) + 1)), 'ids del catálogo: 1..N en orden'
    res = {
        RAIZ / 'lib/core/content/catalogo_situaciones.g.dart': dart(catalogo),
        RAIZ / 'web/avatar/topics.json': temas(catalogo),
    }
    for p in sorted(RAIZ.glob('assets/contenido/*/situaciones.json')):
        contenido = cargar(p)
        if not isinstance(contenido, dict):
            continue  # formato anterior a v2 (en migración)
        faltan = set(ids) - {s['id'] for s in contenido['situaciones']}
        assert not faltan, f'{p}: faltan situaciones {sorted(faltan)}'
        idioma = contenido['idioma']
        res[RAIZ / f'backend/src/content/situaciones-{idioma}.json'] = backend(
            catalogo, contenido
        )
    return res


def main():
    comprobar = '--comprobar' in sys.argv
    viejos = []
    for ruta, texto in salidas().items():
        actual = ruta.read_text(encoding='utf-8') if ruta.exists() else None
        if actual != texto:
            viejos.append(ruta.relative_to(RAIZ))
            if not comprobar:
                ruta.write_text(texto, encoding='utf-8')
    if comprobar and viejos:
        print('Desactualizados (ejecuta generar_situaciones.py):')
        for v in viejos:
            print(' ', v)
        sys.exit(1)
    print('Actualizados:' if viejos else 'Todo al día.', *viejos)


if __name__ == '__main__':
    main()
