#!/usr/bin/env python3
"""Valida Fundamentos pt-BR en staging sin activar portugués.

Construye un curso temporal para reutilizar el validador real de esquema 2 y
contrasta el borrador ejecutable con `curriculo/pt/f0.json`. No escribe en
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
PLAN = RAIZ / 'curriculo' / 'pt' / 'f0.json'
VALIDADOR = RAIZ / 'tools' / 'validar_ruta.py'
NOMBRES_LIBRES = [
    'Ana', 'Beatriz', 'Bia', 'Beto', 'Caio', 'Costa', 'Eva', 'Ivo', 'Lara',
    'Leo', 'Lia', 'Lima', 'Luis', 'Marta', 'Paula', 'Paulo', 'Pedro',
    'Roberto', 'Rui', 'Silva',
]
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

    if ruta.get('modulo') != 'pt.f0':
        errores.append('raíz: modulo debe ser pt.f0')
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

    # F6.e2 era un contraste auditivo A→B («Você é Ana.» / «Você é Ana?») que el TTS
    # no garantiza; se sustituyó por un ítem textual. No debe quedar audio pendiente.
    producciones = [
        x['produccionAudio'] for x in recorrer(ruta)
        if isinstance(x, dict) and isinstance(x.get('produccionAudio'), dict)
    ]
    if producciones:
        errores.append(f'raíz: quedan {len(producciones)} metadato(s) produccionAudio pendientes')
    tipos_f6 = {
        it.get('id'): it.get('formato')
        for u in ruta_u if u.get('id') == 'pt.f0.perguntar-reparar'
        for p in u.get('pasos', []) if p.get('tipo') == 'evaluacion'
        for it in p.get('items', [])
    }
    if tipos_f6.get('e2') != 'elegir':
        errores.append('F6: e2 debe ser un ítem textual (elegir), no un contraste auditivo')

    with tempfile.TemporaryDirectory(prefix='onelingo-pt-f0-') as temporal:
        base = Path(temporal)
        carpeta = base / 'pt' / 'ruta'
        carpeta.mkdir(parents=True)
        shutil.copy2(BORRADOR, carpeta / 'f0.json')
        curso = {
            'esquema': 2,
            'idioma': 'pt',
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
                'id': 'pt.f0', 'nivel': 'f0', 'archivo': 'f0.json',
                'titulo': {'es': 'Fundamentos', 'en': 'Foundations'},
            }],
        }
        (carpeta / 'curso.json').write_text(
            json.dumps(curso, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
        )
        spec = importlib.util.spec_from_file_location('validar_ruta_pt_staging', VALIDADOR)
        modulo = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(modulo)
        modulo.RAIZ = base
        validador = modulo.Validador('pt')
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
