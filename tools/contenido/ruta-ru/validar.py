#!/usr/bin/env python3
"""Valida Fundamentos de ruso (ru-RU) en staging, como ruta-it/validar.py.

Valida `borrador-f0.json` (junto a este script) o la ruta que se pase como
primer argumento. Construye un curso temporal para reutilizar el validador real
de esquema 2 y contrasta el borrador con `curriculo/ru/f0.json`. No escribe en
`assets/` ni modifica el runtime.

Comprobaciones propias del ruso (tools/ia/idiomas/ru.md):
- el texto cirílico nunca lleva marca de acento: U+0301 en cualquier campo es
  un error (el acento va solo en `rom`, con tilde aguda);
- todo texto ruso (vocablos, ejemplos, diálogos, tablas, huecos, preguntas y
  opciones) lleva `rom`, y cada par coincide con la transliteración neutra de la
  ficha (se compara ignorando la tilde de acento);
- el acento del `rom`: una tilde por palabra de 2 o más sílabas, ninguna en los
  monosílabos, y siempre en la «ё» de las palabras de 2 o más sílabas;
- ninguna palabra mezcla alfabeto latino y cirílico;
- sin Ecuador (en español, inglés ni ruso).
Limitación conocida: `tools/validar_ruta.py` solo tiene morfología inglesa en
`conocida` (no rusa), así que cada forma flexionada (брата, Москве, Мексики)
debe aparecer enseñada tal cual o estar en NOMBRES_LIBRES; si hace falta
relajarlo, VOCABULARIO_ESTRICTO = False.
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
import tempfile
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rom_items  # noqa: E402


RAIZ = Path(__file__).resolve().parents[3]
BORRADOR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).with_name('borrador-f0.json')
PLAN = RAIZ / 'curriculo' / 'ru' / 'f0.json'
VALIDADOR = RAIZ / 'tools' / 'validar_ruta.py'
VOCABULARIO_ESTRICTO = True
ACENTO = '\u0301'

# Nombres libres del curso (lista cerrada de tools/ia/idiomas/ru.md): nombres de
# pila, apellidos masculinos y femeninos y ciudades. Sin Ecuador.
NOMBRES_LIBRES = [
    # nombres femeninos
    'Анна', 'Мария', 'Елена', 'Ольга', 'Наталья', 'Татьяна', 'Ирина', 'Светлана',
    # nombres masculinos
    'Иван', 'Александр', 'Дмитрий', 'Сергей', 'Андрей', 'Михаил', 'Максим',
    # apellidos (masculino y femenino)
    'Иванов', 'Иванова', 'Петров', 'Петрова', 'Смирнов', 'Смирнова', 'Кузнецов', 'Кузнецова',
    'Макаров', 'Макарова', 'Васильев', 'Васильева', 'Новиков', 'Новикова', 'Фёдоров', 'Фёдорова',
    'Михайлов', 'Михайлова', 'Павлов', 'Павлова',
    # ciudades
    'Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск', 'Екатеринбург', 'Самара',
    'Краснодар', 'Сочи', 'Воронеж', 'Владивосток',
]
PROHIBIDAS = re.compile(
    r'\b(?:ecuador\w*|ecuatorian\w*|quito|guayaquil|cuenca|эквадор\w*)\b', re.IGNORECASE)
PLANTILLA = re.compile(r'\b(?:placeholder|lorem ipsum|todo)\b', re.IGNORECASE)
PALABRA = re.compile(r'[A-Za-zА-Яа-яЁё' + ACENTO + r']+')

# --- Romanización neutra (tools/ia/idiomas/ru.md) -----------------------------------
_V = 'аеёиоуыэюя'
_MAP = dict(zip('абвгдежзийклмнопрстуфхцчшщъыьэюя', [
    'a', 'b', 'v', 'g', 'd', 'e', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
    'f', 'kh', 'ts', 'ch', 'sh', 'shch', '"', 'y', "'", 'e', 'yu', 'ya']))
_MAP['ё'] = 'yo'
CIRILICO = re.compile(r'[А-Яа-яЁё]+')


def _rom_palabra(w: str) -> str:
    """Transliteración letra a letra, sin tilde de acento."""
    out = ''
    for k, c in enumerate(w):
        lo = c.lower()
        prev = w[k - 1].lower() if k else ''
        if lo == 'е':
            r = 'ye' if k == 0 or prev in _V + 'ьъ' else 'e'
        else:
            r = _MAP.get(lo, c)
        out += r[0].upper() + r[1:] if c != lo else r
    return out


def romanizar(texto: str) -> str:
    """Romanización esperada de un texto cirílico (sin tilde de acento)."""
    return CIRILICO.sub(lambda m: _rom_palabra(m.group(0)), texto)


def sin_tilde(rom: str) -> str:
    """Quita la tilde aguda del `rom` (á é í ó ú ý -> a e i o u y)."""
    return unicodedata.normalize('NFC', unicodedata.normalize('NFD', rom).replace(ACENTO, ''))


def recorrer(valor, ruta=''):
    """Recorre el JSON devolviendo (ruta, valor) para cada nodo."""
    yield ruta, valor
    if isinstance(valor, dict):
        for k, item in valor.items():
            yield from recorrer(item, f'{ruta}.{k}' if ruta else k)
    elif isinstance(valor, list):
        for i, item in enumerate(valor):
            yield from recorrer(item, f'{ruta}[{i}]')


def _silabas(palabra: str) -> int:
    return sum(1 for c in palabra.lower() if c in _V)


def comprobar_acentos(ruta_json: dict, errores: list[str]) -> None:
    """El cirílico no lleva marca de acento U+0301 en ningún campo."""
    for u in ruta_json.get('unidades', []):
        uid = u.get('id', '?')
        for ruta, valor in recorrer(u):
            if isinstance(valor, str) and ACENTO in valor:
                errores.append(f'{uid}: marca de acento U+0301 en {ruta}: el acento va solo en rom')


def comprobar_par(uid: str, ruta: str, texto: str, rom: str, errores: list[str]) -> None:
    """Un `rom` debe ser la transliteración de su `texto` con el acento bien marcado."""
    esperado = romanizar(texto)
    if sin_tilde(rom) != esperado:
        errores.append(f'{uid}: {ruta} rom «{rom}» debería ser «{esperado}» (salvo tildes)')
        return
    t_pal, r_pal = texto.split(), rom.split()
    if len(t_pal) != len(r_pal):
        errores.append(f'{uid}: {ruta} rom con distinto número de palabras que el texto')
        return
    for tp, rp in zip(t_pal, r_pal):
        esperadas = 0
        for run in CIRILICO.findall(tp):
            if _silabas(run) >= 2:
                esperadas += 1
                if 'ё' in run.lower() and 'yó' not in rp.lower() and 'ó' not in rp.lower():
                    errores.append(f'{uid}: {ruta} la «ё» de «{tp}» debe llevar acento en el rom «{rp}»')
        reales = sum(1 for c in unicodedata.normalize('NFD', rp) if c == ACENTO)
        if reales != esperadas:
            errores.append(f'{uid}: {ruta} rom «{rp}» lleva {reales} tildes y «{tp}» pide {esperadas}')


def comprobar_rom(ruta_json: dict, errores: list[str]) -> None:
    """Todo texto ruso lleva `rom` y coincide con la transliteración de la ficha.

    Convención (docs/claude-educacion/ROMANIZACION.md): `rom` junto a `texto` en
    vocablos, ejemplos, líneas de diálogo y celdas; en los ítems de ejercicio,
    `textoRom`/`preguntaRom` y las listas paralelas `opcionesRom`, `tokensRom` y
    `paresRom` (izquierda de cada par), comprobadas con tools/contenido/rom_items.py;
    `hablanteRom`, `incorrectoRom` y `correctoRom` junto a su campo. `respuesta`,
    `aceptadas` y `audio` nunca llevan rom.
    """
    def hay(s) -> bool:
        return isinstance(s, str) and bool(CIRILICO.search(s))

    for u in ruta_json.get('unidades', []):
        uid = u.get('id', '?')
        for v in u.get('vocabulario', []):
            if not v.get('rom'):
                errores.append(f'{uid}/{v.get("id")}: vocablo sin rom')
        for e_i, e in enumerate(u.get('erroresFrecuentes', [])):
            for campo in ('incorrecto', 'correcto'):
                if hay(e.get(campo)):
                    if not isinstance(e.get(campo + 'Rom'), str):
                        errores.append(f'{uid}: erroresFrecuentes[{e_i}].{campo} sin {campo}Rom')
                    else:
                        comprobar_par(uid, f'erroresFrecuentes[{e_i}].{campo}Rom', e[campo], e[campo + 'Rom'], errores)
        for ruta, nodo in recorrer(u):
            if not isinstance(nodo, dict) or 'formato' in nodo:
                continue  # los ítems se comprueban con rom_items
            for campo in ('texto', 'pregunta'):
                valor = nodo.get(campo)
                if not hay(valor):
                    continue
                if not isinstance(nodo.get('rom'), str):
                    errores.append(f'{uid}: {ruta}.{campo} tiene cirílico y no tiene rom')
                else:
                    comprobar_par(uid, f'{ruta}.rom', valor, nodo['rom'], errores)
            if hay(nodo.get('hablante')):
                if not isinstance(nodo.get('hablanteRom'), str):
                    errores.append(f'{uid}: {ruta}.hablante sin hablanteRom')
                else:
                    comprobar_par(uid, f'{ruta}.hablanteRom', nodo['hablante'], nodo['hablanteRom'], errores)

    def comprobar(texto: str, rom: str):
        propios: list[str] = []
        comprobar_par('', '', texto, rom, propios)
        return '; '.join(e.split(': ', 1)[-1].strip() for e in propios) or None

    errores.extend(rom_items.errores(ruta_json, hay, comprobar))

def main() -> None:
    if not BORRADOR.exists():
        raise SystemExit(
            f'ERROR: no existe el borrador {BORRADOR}.\n'
            'Aún no se ha escrito: debe generarlo el agente autor a partir de '
            f'{PLAN.relative_to(RAIZ)} (módulo ru.f0, 8 unidades) antes de validar.')
    if not PLAN.exists():
        raise SystemExit(f'ERROR: no existe el plan {PLAN}.')
    plan = json.loads(PLAN.read_text(encoding='utf-8'))
    try:
        original = json.loads(BORRADOR.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        raise SystemExit(f'ERROR: {BORRADOR.name} no es JSON válido: {e}')
    errores: list[str] = []

    comprobar_acentos(original, errores)
    comprobar_rom(original, errores)
    ruta = original

    if ruta.get('modulo') != 'ru.f0':
        errores.append('raíz: modulo debe ser ru.f0')
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

    textos = [x for _, x in recorrer(ruta) if isinstance(x, str)]
    if any(PLANTILLA.search(x) for x in textos):
        errores.append('raíz: contiene texto plantilla')

    # Sin Ecuador (tools/ia/idiomas/ru.md): ni en el ruso ni en el apoyo.
    if any(PROHIBIDAS.search(x) for x in textos):
        errores.append('raíz: menciona Ecuador o una ciudad ecuatoriana')

    # Ninguna palabra mezcla alfabeto latino y cirílico (letras «gemelas» pegadas).
    for texto in textos:
        for w in PALABRA.findall(texto):
            alfabetos = {unicodedata.name(c, '?').split()[0] for c in w if c.isalpha()}
            if {'LATIN', 'CYRILLIC'} <= alfabetos:
                errores.append(f'raíz: palabra con letras latinas y cirílicas mezcladas: «{w}»')

    with tempfile.TemporaryDirectory(prefix='onelingo-ru-f0-') as temporal:
        base = Path(temporal)
        carpeta = base / 'ru' / 'ruta'
        carpeta.mkdir(parents=True)
        (carpeta / 'f0.json').write_text(
            json.dumps(ruta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        curso = {
            'esquema': 2,
            'idioma': 'ru',
            'version': 'staging',
            'revision': 'inicial',
            'idiomasApoyo': ['es', 'en'],
            'apoyoPredeterminado': 'es',
            'palabrasLibres': NOMBRES_LIBRES,
            'vocabularioEstricto': VOCABULARIO_ESTRICTO,
            'niveles': [{
                'id': 'f0', 'cefr': 'Pre-A1', 'nivelInterno': 0,
                'estado': 'publicado',
                'titulo': {'es': 'Fundamentos', 'en': 'Foundations'},
            }],
            'modulos': [{
                'id': 'ru.f0', 'nivel': 'f0', 'archivo': 'f0.json',
                'titulo': {'es': 'Fundamentos', 'en': 'Foundations'},
            }],
        }
        (carpeta / 'curso.json').write_text(
            json.dumps(curso, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
        )
        spec = importlib.util.spec_from_file_location('validar_ruta_ru_staging', VALIDADOR)
        modulo = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(modulo)
        modulo.RAIZ = base
        validador = modulo.Validador('ru')
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
