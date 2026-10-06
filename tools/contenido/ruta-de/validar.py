#!/usr/bin/env python3
"""Valida Fundamentos de alemán (de-DE) en staging, como ruta-pt/validar.py.

Construye un curso temporal para reutilizar el validador real de esquema 2 y
contrasta el borrador ejecutable con `curriculo/de/f0.json`. No escribe en
`assets/` ni modifica el runtime.
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import tempfile
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[3]
BORRADOR = Path(__file__).with_name('borrador-f0.json')
PLAN = RAIZ / 'curriculo' / 'de' / 'f0.json'
VALIDADOR = RAIZ / 'tools' / 'validar_ruta.py'
# Mismos nombres libres que el curso publicado (integrar.py los fija al integrar N1).
CURSO = RAIZ / 'assets' / 'contenido' / 'de' / 'ruta' / 'curso.json'
NOMBRES_LIBRES = json.loads(CURSO.read_text(encoding='utf-8')).get('palabrasLibres', [])
PROHIBIDAS = re.compile(r'\b(?:Ecuador|Quito|Guayaquil|Cuenca)\b')
PLANTILLA = re.compile(r'\b(?:placeholder|lorem ipsum|todo)\b', re.IGNORECASE)


def recorrer(valor):
    yield valor
    if isinstance(valor, dict):
        for item in valor.values():
            yield from recorrer(item)
    elif isinstance(valor, list):
        for item in valor:
            yield from recorrer(item)


def main() -> None:
    plan = json.loads(PLAN.read_text(encoding='utf-8'))
    ruta = json.loads(BORRADOR.read_text(encoding='utf-8'))
    errores: list[str] = []

    if ruta.get('modulo') != 'de.f0':
        errores.append('raíz: modulo debe ser de.f0')
    plan_u = plan.get('unidades', [])
    ruta_u = ruta.get('unidades', [])
    if len(ruta_u) != 8:
        errores.append(f'raíz: se esperan 8 unidades, hay {len(ruta_u)}')

    for indice, (ficha, unidad) in enumerate(zip(plan_u, ruta_u)):
        uid = str(unidad.get('id', f'F{indice + 1}'))
        if unidad.get('id') != ficha.get('id'):
            errores.append(f'{uid}: id distinto de la ficha')
        if unidad.get('orden') != indice:
            errores.append(f'{uid}: orden debe ser {indice}')
        esperado = [] if indice == 0 else [ruta_u[indice - 1].get('id')]
        if unidad.get('prerequisitos') != esperado:
            errores.append(f'{uid}: cadena de prerrequisitos incorrecta')
        if not set(ficha.get('introduce', [])) <= set(unidad.get('gramatica', [])):
            errores.append(f'{uid}: faltan claves introducidas en gramatica')
        if 'introduce' in unidad:
            errores.append(f'{uid}: introduce es editorial y no pertenece a la ruta')
        if 'tutor' in unidad:
            errores.append(f'{uid}: la ruta base no debe depender de tutor')

        vocab_plan = {v.get('texto') for v in ficha.get('vocabulario', [])}
        vocab_ruta = {v.get('texto') for v in unidad.get('vocabulario', [])}
        if vocab_plan != vocab_ruta:
            errores.append(
                f'{uid}: vocabulario diverge; falta={sorted(vocab_plan - vocab_ruta)}, '
                f'sobra={sorted(vocab_ruta - vocab_plan)}'
            )

        pasos = {p.get('tipo'): p for p in unidad.get('pasos', [])}
        for tipo, cantidad in (
            ('practica_guiada', 3),
            ('practica_independiente', 3),
            ('situacion', 2),
            ('evaluacion', 5),
        ):
            actual = len(pasos.get(tipo, {}).get('items', []))
            if actual != cantidad:
                errores.append(f'{uid}: {tipo} tiene {actual} ítems; se esperan {cantidad}')
        formatos = {x.get('formato') for x in pasos.get('evaluacion', {}).get('items', [])}
        if len(formatos) < 3:
            errores.append(f'{uid}: evaluación con menos de 3 formatos')
        if not unidad.get('pasos') or unidad['pasos'][-1].get('tipo') != 'evaluacion':
            errores.append(f'{uid}: evaluación no es el último paso')

    textos = [x for x in recorrer(ruta) if isinstance(x, str)]
    if any(PLANTILLA.search(x) for x in textos):
        errores.append('raíz: contiene texto plantilla')

    # Sin Ecuador (PLAN_ALEMAN §2): ni en el alemán ni en el apoyo.
    if any(PROHIBIDAS.search(x) for x in textos):
        errores.append('raíz: menciona Ecuador o una ciudad ecuatoriana')

    with tempfile.TemporaryDirectory(prefix='onelingo-de-f0-') as temporal:
        base = Path(temporal)
        carpeta = base / 'de' / 'ruta'
        carpeta.mkdir(parents=True)
        shutil.copy2(BORRADOR, carpeta / 'f0.json')
        curso = {
            'esquema': 2,
            'idioma': 'de',
            'version': 'staging',
            'revision': 'inicial',
            'idiomasApoyo': ['es', 'en'],
            'apoyoPredeterminado': 'es',
            'palabrasLibres': NOMBRES_LIBRES,
            'vocabularioEstricto': True,
            'niveles': [{
                'id': 'f0', 'cefr': 'Pre-A1', 'nivelInterno': 0,
                'estado': 'publicado',
                'titulo': {'es': 'Fundamentos', 'en': 'Foundations'},
            }],
            'modulos': [{
                'id': 'de.f0', 'nivel': 'f0', 'archivo': 'f0.json',
                'titulo': {'es': 'Fundamentos', 'en': 'Foundations'},
            }],
        }
        (carpeta / 'curso.json').write_text(
            json.dumps(curso, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
        )
        spec = importlib.util.spec_from_file_location('validar_ruta_de_staging', VALIDADOR)
        modulo = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(modulo)
        modulo.RAIZ = base
        validador = modulo.Validador('de')
        errores.extend(validador.validar())
        for aviso in validador.advertencias:
            print('ADVERTENCIA:', aviso)

    for error in errores:
        print('ERROR:', error)
    vocablos = sum(len(u.get('vocabulario', [])) for u in ruta_u)
    ejercicios = sum(
        len(next((p for p in u.get('pasos', []) if p.get('tipo') == tipo), {}).get('items', []))
        for u in ruta_u
        for tipo in ('practica_guiada', 'practica_independiente', 'situacion', 'evaluacion')
    )
    print(
        f'{len(errores)} errores · {len(ruta_u)} unidades · '
        f'{vocablos} vocablos · {ejercicios} ejercicios'
    )
    raise SystemExit(1 if errores else 0)


if __name__ == '__main__':
    main()
