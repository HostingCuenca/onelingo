#!/usr/bin/env python3
"""Valida Fundamentos de japonés (ja-JP) en staging, como ruta-it/validar.py.

Construye un curso temporal para reutilizar el validador real de esquema 2 y
contrasta el borrador ejecutable (`borrador-f0.json`) con `curriculo/ja/f0.json`.
Añade comprobaciones propias del japonés (tools/ia/idiomas/ja.md): sin kanji
en Fundamentos, puntuación de ancho completo, partículas separadas y tokens
de longitud razonable. Romanización de los ítems (`textoRom`, `preguntaRom`,
`opcionesRom`, `tokensRom`, `paresRom`) según docs/claude-educacion/ROMANIZACION.md
(tools/contenido/rom_items.py). No escribe en `assets/` ni modifica el runtime.
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rom_items  # noqa: E402


RAIZ = Path(__file__).resolve().parents[3]
BORRADOR = Path(__file__).with_name('borrador-f0.json')
PLAN = RAIZ / 'curriculo' / 'ja' / 'f0.json'
VALIDADOR = RAIZ / 'tools' / 'validar_ruta.py'
# Si el curso ya existe en assets, sus palabras libres se suman a las de la ficha.
CURSO = RAIZ / 'assets' / 'contenido' / 'ja' / 'ruta' / 'curso.json'

# Listas cerradas de tools/ia/idiomas/ja.md (en kana; los nombres de pila van siempre en hiragana).
NOMBRES = [
    'さくら', 'ゆき', 'あおい', 'めぐみ', 'ようこ', 'みさき', 'あやか', 'ななこ',
    'けんた', 'たくや', 'ゆうた', 'だいすけ', 'りょう', 'しょうた', 'ひろし',
]
APELLIDOS = [
    'たなか', 'すずき', 'わたなべ', 'たかはし', 'いとう',
    'やまもと', 'なかむら', 'こばやし', 'かとう', 'よしだ',
]
CIUDADES = [
    'とうきょう', 'おおさか', 'きょうと', 'なごや', 'ふくおか',
    'さっぽろ', 'よこはま', 'こうべ', 'ひろしま', 'せんだい',
]
PAISES = [
    'メキシコ', 'コロンビア', 'アルゼンチン', 'チリ', 'ペルー',
    'スペイン', 'アメリカ', 'にほん', 'イタリア', 'スイス',
]
# Nombre de persona + さん (tratamiento pegado) cuenta como palabra libre.
NOMBRES_LIBRES = list(dict.fromkeys(
    NOMBRES + APELLIDOS + CIUDADES + PAISES
    + [n + 'さん' for n in NOMBRES + APELLIDOS]
    + [p + 'じん' for p in PAISES]
))

PROHIBIDAS = re.compile(r'\b(?:ecuador\w*|ecuatorian\w*|quito|guayaquil|cuenca)\b', re.IGNORECASE)
PLANTILLA = re.compile(r'\b(?:placeholder|lorem ipsum|todo)\b', re.IGNORECASE)

KANA = re.compile(r'[ぁ-ゖァ-ヺー]')
# Ideogramas CJK. Fundamentos va en kana: ni un solo kanji (la «～» y «ー» no cuentan).
KANJI = re.compile(r'[一-鿿㐀-䶿]')
KANJI_PERMITIDOS: set[str] = set()  # Fundamentos: ninguno
ASCII_PUNT_JA = re.compile(r'[ぁ-ヿ一-鿿][.,!?;]')
ESPACIO_ANCHO = '　'
CIFRA_EN_JA = re.compile(r'[0-9][ぁ-ヿ]|[ぁ-ヿ][0-9]')
RECORTE = '。、？！「」『』«»“”"\'()（）…・ '
PARTICULAS_FINAL_PROHIBIDAS = ('を',)
# Palabras japonesas que terminan en は y son legítimas como una sola palabra.
TERMINAN_EN_WA = {'こんにちは', 'こんばんは'}
LIMITE_MORAS = 10


def recorrer(valor):
    yield valor
    if isinstance(valor, dict):
        for item in valor.values():
            yield from recorrer(item)
    elif isinstance(valor, list):
        for item in valor:
            yield from recorrer(item)


def tokens_japoneses(texto: str):
    """Tokens (separados por espacios) que contienen kana, sin puntuación en los extremos."""
    for tok in re.split(r'[\s/・]+', texto):
        limpio = tok.strip(RECORTE)
        if limpio and KANA.search(limpio):
            yield limpio


def es_mayormente_japones(texto: str) -> bool:
    """Texto japonés puro, sin letras latinas (los textos de apoyo mezclan idiomas y llevan comas ASCII)."""
    ja = len(KANA.findall(texto)) + len(KANJI.findall(texto))
    latinas = len(re.findall(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]', texto))
    return ja > 0 and latinas == 0


def revisar_japones(textos: list[str], errores: list[str], avisos: list[str]) -> None:
    for texto in textos:
        tiene_kana = bool(KANA.search(texto))
        if ESPACIO_ANCHO in texto:
            errores.append(f'japonés: espacio de ancho completo (U+3000) en «{texto}»')
        if not tiene_kana and not KANJI.search(texto):
            continue
        for k in KANJI.findall(texto):
            if k not in KANJI_PERMITIDOS:
                errores.append(f'japonés: kanji «{k}» no permitido en Fundamentos («{texto}»)')
                break
        if ASCII_PUNT_JA.search(texto) and es_mayormente_japones(texto):
            errores.append(f'japonés: puntuación ASCII junto a texto japonés en «{texto}»')
        if CIFRA_EN_JA.search(texto) and es_mayormente_japones(texto):
            avisos.append(f'japonés: cifra arábiga pegada a texto japonés en «{texto}»')
        if re.search(r'\s[。、？！]', texto):
            errores.append(f'japonés: espacio antes de puntuación japonesa en «{texto}»')
        if re.search(r'[。、？！]\S', texto) and not re.search(r'[。、？！][」』]', texto):
            # Tras 。 、 ？ ！ va un espacio (salvo al cerrar comillas o al final del texto).
            if re.search(r'[。、？！][^\s」』）)»“”"\']', texto):
                errores.append(f'japonés: falta espacio tras la puntuación en «{texto}»')
        for tok in tokens_japoneses(texto):
            if tok.endswith(PARTICULAS_FINAL_PROHIBIDAS) and len(tok) > 1:
                errores.append(f'japonés: partícula pegada «{tok}» (を va aparte) en «{texto}»')
            elif len(tok) > 1 and tok.endswith('は') and tok not in TERMINAN_EN_WA:
                avisos.append(f'japonés: ¿partícula は pegada en «{tok}»? en «{texto}»')
            if len(tok) > LIMITE_MORAS and tok not in NOMBRES_LIBRES:
                avisos.append(f'japonés: token muy largo «{tok}», ¿falta separar palabras? en «{texto}»')


def main() -> None:
    if not BORRADOR.exists():
        print(
            f'ERROR: no existe el borrador {BORRADOR.relative_to(RAIZ)}. '
            'Lo escribe el autor de Fundamentos; hasta entonces no hay nada que validar.',
            file=sys.stderr,
        )
        raise SystemExit(2)
    if not PLAN.exists():
        print(f'ERROR: no existe el plan {PLAN.relative_to(RAIZ)}.', file=sys.stderr)
        raise SystemExit(2)
    if not VALIDADOR.exists():
        print(f'ERROR: no existe {VALIDADOR.relative_to(RAIZ)}.', file=sys.stderr)
        raise SystemExit(2)

    plan = json.loads(PLAN.read_text(encoding='utf-8'))
    ruta = json.loads(BORRADOR.read_text(encoding='utf-8'))
    errores: list[str] = []
    avisos: list[str] = []

    libres = list(NOMBRES_LIBRES)
    if CURSO.exists():
        libres = list(dict.fromkeys(json.loads(CURSO.read_text(encoding='utf-8')).get('palabrasLibres', []) + libres))
    libres = [p for p in libres if not PROHIBIDAS.search(p)]

    if ruta.get('modulo') != 'ja.f0':
        errores.append('raíz: modulo debe ser ja.f0')
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
        # rom obligatorio en cada vocablo (ficha: rom Hepburn modificado en N1–N4 y Fundamentos).
        for v in unidad.get('vocabulario', []):
            if not str(v.get('rom', '')).strip():
                errores.append(f'{uid}: vocablo «{v.get("texto")}» sin rom')
        errores.extend(rom_items.errores(
            {'unidades': [unidad]},
            lambda t: isinstance(t, str) and bool(KANA.search(t) or KANJI.search(t)),
            lambda _t, rom: 'rom con kana o kanji' if (KANA.search(rom) or KANJI.search(rom)) else None))

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

    # Sin Ecuador (tools/ia/idiomas/ja.md): ni en el japonés ni en el apoyo.
    if any(PROHIBIDAS.search(x) for x in textos):
        errores.append('raíz: menciona Ecuador o una ciudad ecuatoriana')

    # Reglas propias del japonés: kana sin kanji, puntuación y separación de palabras.
    revisar_japones(textos, errores, avisos)

    with tempfile.TemporaryDirectory(prefix='onelingo-ja-f0-') as temporal:
        base = Path(temporal)
        carpeta = base / 'ja' / 'ruta'
        carpeta.mkdir(parents=True)
        shutil.copy2(BORRADOR, carpeta / 'f0.json')
        curso = {
            'esquema': 2,
            'idioma': 'ja',
            'version': 'staging',
            'revision': 'inicial',
            'idiomasApoyo': ['es', 'en'],
            'apoyoPredeterminado': 'es',
            'palabrasLibres': libres,
            'vocabularioEstricto': True,
            'niveles': [{
                'id': 'f0', 'cefr': 'Pre-A1', 'nivelInterno': 0,
                'estado': 'publicado',
                'titulo': {'es': 'Fundamentos', 'en': 'Foundations'},
            }],
            'modulos': [{
                'id': 'ja.f0', 'nivel': 'f0', 'archivo': 'f0.json',
                'titulo': {'es': 'Fundamentos', 'en': 'Foundations'},
            }],
        }
        (carpeta / 'curso.json').write_text(
            json.dumps(curso, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
        )
        spec = importlib.util.spec_from_file_location('validar_ruta_ja_staging', VALIDADOR)
        modulo = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(modulo)
        modulo.RAIZ = base
        validador = modulo.Validador('ja')
        errores.extend(validador.validar())
        for aviso in validador.advertencias:
            print('ADVERTENCIA:', aviso)

    for aviso in dict.fromkeys(avisos):
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
