#!/usr/bin/env python3
"""Valida el plan detallado de Fundamentos previo a N1.

Uso:
  python3 tools/curriculo/validar_fundamentos.py pt
  python3 tools/curriculo/validar_fundamentos.py ruta/al/f0.json

La fuente canónica esperada es curriculo/<idioma>/f0.json. Este validador no
publica contenido: comprueba que las ocho fichas sean ejecutables antes de que
un autor escriba la ruta f0.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[2]
FORMATOS = {'elegir', 'escuchar', 'ordenar', 'completar', 'escribir', 'relacionar'}
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
PLANTILLAS = re.compile(
    r'^(situación breve y determinista\.?|short deterministic situation\.?|'
    r'respuesta indicada|expresión indicada|responde el ítem\.?|answer the item\.?|'
    r'opción → correcta|___ → respuesta|audio → opción|modelo → respuesta|respuesta\.)$',
    re.IGNORECASE,
)


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else 'pt'
    ruta = Path(arg) if arg.endswith('.json') else RAIZ / 'curriculo' / arg / 'f0.json'
    if not ruta.exists():
        raise SystemExit(f'ERROR falta {ruta}')

    datos = json.loads(ruta.read_text(encoding='utf-8'))
    errores: list[str] = []
    avisos: list[str] = []

    def error(msg: str) -> None:
        errores.append(msg)

    def bilingue(valor: object, donde: str) -> None:
        if not (
            isinstance(valor, dict)
            and all(isinstance(valor.get(k), str) and valor[k].strip() for k in ('es', 'en'))
        ):
            error(f'{donde}: falta texto {{es, en}}')

    def vacio(valor: object) -> bool:
        return valor is None or valor == '' or valor == [] or valor == {}

    def claves(valor: object, donde: str) -> list[str]:
        if not isinstance(valor, list):
            error(f'{donde}: debe ser una lista de claves')
            return []
        for clave in valor:
            if not isinstance(clave, str) or not SLUG.fullmatch(clave):
                error(f'{donde}: clave inválida {clave!r}')
        return valor

    def buscar_plantillas(valor: object, donde: str) -> None:
        if isinstance(valor, str) and PLANTILLAS.fullmatch(valor.strip()):
            error(f'{donde}: texto plantilla {valor!r}')
        elif isinstance(valor, list):
            for i, item in enumerate(valor):
                buscar_plantillas(item, f'{donde}[{i}]')
        elif isinstance(valor, dict):
            for k, item in valor.items():
                buscar_plantillas(item, f'{donde}.{k}')

    idioma = datos.get('idioma')
    if not isinstance(idioma, str) or not SLUG.fullmatch(idioma):
        error('raíz: idioma inválido')
        idioma = 'xx'
    if datos.get('esquema') != 'onelingo.plan-fundamentos.v1':
        error('raíz: esquema inesperado')
    if datos.get('cefr') != 'Pre-A1':
        error('raíz: cefr debe ser Pre-A1')
    if datos.get('estado') != 'planificado':
        error('raíz: estado debe ser planificado')

    previos = claves(datos.get('previos'), 'raíz.previos')
    salida_declarada = claves(datos.get('clavesSalida'), 'raíz.clavesSalida')
    conocidas = set(previos)
    introducidas: set[str] = set()
    vocab_ids: set[str] = set()
    unidades = datos.get('unidades')
    if not isinstance(unidades, list):
        error('raíz: unidades debe ser una lista')
        unidades = []
    if len(unidades) != 8:
        error(f'raíz: se esperan 8 unidades, hay {len(unidades)}')

    for orden, unidad in enumerate(unidades, 1):
        if not isinstance(unidad, dict):
            error(f'F{orden}: unidad inválida')
            continue
        uid = unidad.get('id')
        donde = str(uid or f'F{orden}')
        if not isinstance(uid, str) or not uid.startswith(f'{idioma}.f0.'):
            error(f'{donde}: id fuera de {idioma}.f0.*')
        if unidad.get('orden') != orden:
            error(f'{donde}: orden {unidad.get("orden")!r}, se espera {orden}')
        if unidad.get('cefr') != 'Pre-A1':
            error(f'{donde}: cefr debe ser Pre-A1')
        for campo in ('titulo', 'objetivo', 'tarea'):
            bilingue(unidad.get(campo), f'{donde}.{campo}')
        for campo in ('gramatica', 'habilidades'):
            valor = unidad.get(campo)
            if not isinstance(valor, list) or not valor or not all(
                isinstance(x, str) and x.strip() for x in valor
            ):
                error(f'{donde}.{campo}: lista vacía o inválida')
        if not isinstance(unidad.get('sonido'), str) or not unidad['sonido'].strip():
            error(f'{donde}.sonido: falta la pista de sonido')

        prerequisitos = claves(unidad.get('prerequisitos'), f'{donde}.prerequisitos')
        recicla = claves(unidad.get('recicla'), f'{donde}.recicla')
        introduce = claves(unidad.get('introduce'), f'{donde}.introduce')
        for clave in prerequisitos:
            if clave not in conocidas:
                error(f'{donde}: prerequisito futuro o desconocido {clave!r}')
        for clave in recicla:
            if clave not in conocidas:
                error(f'{donde}: recicla clave futura o desconocida {clave!r}')
        for clave in introduce:
            if clave in conocidas or clave in introducidas:
                error(f'{donde}: introduce clave duplicada {clave!r}')
            introducidas.add(clave)

        vocabulario = unidad.get('vocabulario')
        if not isinstance(vocabulario, list) or not 12 <= len(vocabulario) <= 16:
            error(f'{donde}.vocabulario: se esperan 12–16 entradas')
            vocabulario = vocabulario if isinstance(vocabulario, list) else []
        for i, entrada in enumerate(vocabulario, 1):
            ev = f'{donde}.vocabulario[{i}]'
            if not isinstance(entrada, dict):
                error(f'{ev}: entrada inválida')
                continue
            vid = entrada.get('id')
            if not isinstance(vid, str) or not SLUG.fullmatch(vid):
                error(f'{ev}: id inválido {vid!r}')
            elif vid in vocab_ids:
                error(f'{ev}: id duplicado {vid!r}')
            else:
                vocab_ids.add(vid)
            if not isinstance(entrada.get('texto'), str) or not entrada['texto'].strip():
                error(f'{ev}: falta texto meta')
            bilingue(entrada.get('traduccion'), f'{ev}.traduccion')
            if entrada.get('nota') is not None:
                bilingue(entrada['nota'], f'{ev}.nota')

        frecuentes = unidad.get('erroresFrecuentes')
        if not isinstance(frecuentes, list) or len(frecuentes) < 2:
            error(f'{donde}.erroresFrecuentes: se esperan al menos 2')
            frecuentes = frecuentes if isinstance(frecuentes, list) else []
        for i, frecuente in enumerate(frecuentes, 1):
            ef = f'{donde}.erroresFrecuentes[{i}]'
            if not isinstance(frecuente, dict) or not all(
                isinstance(frecuente.get(k), str) and frecuente[k].strip()
                for k in ('incorrecto', 'correcto')
            ):
                error(f'{ef}: falta incorrecto/correcto')
                continue
            bilingue(frecuente.get('explicacion'), f'{ef}.explicacion')

        ejercicios = unidad.get('ejercicios')
        if not isinstance(ejercicios, dict):
            error(f'{donde}.ejercicios: falta el plan')
            ejercicios = {}
        situacion = ejercicios.get('situacion')
        if not isinstance(situacion, dict):
            error(f'{donde}.situacion: falta')
            situacion = {}
        bilingue(situacion.get('contexto'), f'{donde}.situacion.contexto')
        dialogo = situacion.get('dialogo')
        if not (
            isinstance(dialogo, list)
            and 3 <= len(dialogo) <= 5
            and all(isinstance(x, str) and x.strip() for x in dialogo)
        ):
            error(f'{donde}.situacion.dialogo: se esperan 3–5 líneas portuguesas')

        grupos = (
            ('guiada', ejercicios.get('guiada'), 3),
            ('independiente', ejercicios.get('independiente'), 3),
            ('situacion', situacion.get('preguntas'), 2),
            ('evaluacion', ejercicios.get('evaluacion'), 5),
        )
        huellas: set[str] = set()
        evaluacion: list[dict] = []
        claves_locales = set(introduce) | set(recicla)
        for grupo, items, esperado in grupos:
            if not isinstance(items, list) or len(items) != esperado:
                cuantos = len(items) if isinstance(items, list) else 0
                error(f'{donde}.{grupo}: se esperan {esperado} ítems, hay {cuantos}')
                items = items if isinstance(items, list) else []
            if grupo == 'evaluacion':
                evaluacion = [x for x in items if isinstance(x, dict)]
            for i, item in enumerate(items, 1):
                di = f'{donde}.{grupo}[{i}]'
                if not isinstance(item, dict):
                    error(f'{di}: ítem inválido')
                    continue
                if item.get('formato') not in FORMATOS:
                    error(f'{di}: formato inválido {item.get("formato")!r}')
                if item.get('clave') not in claves_locales:
                    error(f'{di}: clave no introducida ni reciclada {item.get("clave")!r}')
                bilingue(item.get('consigna'), f'{di}.consigna')
                for campo in ('estimulo', 'respuesta', 'ejemplo'):
                    if vacio(item.get(campo)):
                        error(f'{di}: falta {campo}')
                if item.get('formato') in ('elegir', 'escuchar'):
                    opciones = item.get('opciones')
                    if not isinstance(opciones, list) or len(opciones) < 2:
                        error(f'{di}: se esperan al menos 2 opciones')
                huella = json.dumps(
                    [item.get('estimulo'), item.get('respuesta')],
                    ensure_ascii=False,
                    sort_keys=True,
                )
                if huella in huellas:
                    error(f'{di}: repite estímulo y respuesta dentro de la unidad')
                huellas.add(huella)
        if len({x.get('formato') for x in evaluacion}) < 3:
            error(f'{donde}.evaluacion: debe usar al menos 3 formatos')
        cubiertas = {x.get('clave') for x in evaluacion}
        faltan = set(introduce) - cubiertas
        if faltan:
            error(f'{donde}.evaluacion: no cubre {sorted(faltan)}')

        conocidas.update(introduce)

    if set(salida_declarada) != introducidas:
        error('raíz.clavesSalida: no coincide exactamente con las claves introducidas')
    if unidades and datos.get('salida') != unidades[-1].get('id'):
        error('raíz.salida: debe ser el id de la última unidad')
    buscar_plantillas(datos, 'raíz')

    for aviso in avisos:
        print('aviso:', aviso)
    for item in errores:
        print('ERROR:', item)
    print(
        f'{len(errores)} errores, {len(avisos)} avisos · '
        f'{len(unidades)} unidades · {len(introducidas)} claves · {len(vocab_ids)} vocablos'
    )
    raise SystemExit(1 if errores else 0)


if __name__ == '__main__':
    main()
