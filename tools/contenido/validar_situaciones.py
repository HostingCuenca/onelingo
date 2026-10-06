#!/usr/bin/env python3
"""Valida contenido de situaciones v2 (docs/claude-educacion/SITUACIONES_V2.md).

Uso:
  python3 tools/contenido/validar_situaciones.py assets/contenido/en/situaciones.json
  python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/borrador/lote-1.json

Acepta el archivo final ({"situaciones": [...]}) o un lote (lista de situaciones).
Sale con código 1 si hay errores.
"""
import json
import pathlib
import re
import sys

TRAMOS = {'basico': 'b', 'intermedio': 'i', 'avanzado': 'a'}
OBJ_PREFIJO = {'basico': 'o', 'intermedio': 'i', 'avanzado': 'a'}
MAX_PALABRAS_FRASE = {'basico': 12, 'intermedio': 20, 'avanzado': 30}
# Palabras de España que no usamos (español neutro de América).
PENINSULAR = re.compile(
    r'\b(coche|móvil|ordenador|vale(?! la pena)|vosotros|billete|piso|zumo|gafas|conducir)\b',
    re.I,
)


# Inglés general americano (como el Nivel 0): ortografía y léxico de EE. UU.
BRITANICO = re.compile(
    r"\b(favourite|colour|neighbour|behaviour|flavour|honour|humour|labour|"
    r"centre|theatre|metre|litre|(?:organi|reali|apologi|recogni)s(?:e|es|ed|ing|ation|er)|"
    r"cheque|programme|travelling|travelled|cancelled|cancelling|petrol|pavement|"
    r"trousers|trainers|queue|rubbish|motorway|chemist|timetable|mobile phone|"
    r"chilli|crisps|biscuit|lorry|postcode|car park|fortnight|maths)\b",
    re.I,
)


def palabras(t):
    # Letras de cualquier idioma (très, déjà); el apóstrofo une (l’ami = 1).
    return len(re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)*", t))


# Idiomas meta cuyo apoyo es solo inglés (el español se explica en inglés):
# títulos y traducciones van como {"en": …}.
APOYO_SOLO_EN = {'es'}
SOLO_EN = False  # lo fija validar() según el idioma del contenido


def _bilingue(x):
    if SOLO_EN:
        return isinstance(x, dict) and set(x) == {'en'} and str(x['en']).strip()
    return isinstance(x, dict) and str(x.get('es', '')).strip() and str(x.get('en', '')).strip()


def _apoyo(x):
    """Texto de apoyo que el validador mide: el español o, si es solo inglés, el inglés."""
    if not isinstance(x, dict):
        return x or ''
    return x.get('es') or x.get('en', '')


def _normalizar(situaciones, errores):
    """Esquema genérico (meta + traduccion {es, en}) → claves del validador.

    Devuelve True si el contenido es de un idioma nuevo (no inglés).
    """
    generico = False
    for s in situaciones:
        for tramo, t in (s.get('tramos') or {}).items():
            donde = f's{s.get("id")} {tramo}'
            for o in t.get('objetivos', []):
                if isinstance(o.get('titulo'), dict) or isinstance(o.get('traduccion'), dict):
                    generico = True
                    if not _bilingue(o.get('titulo')) or not _bilingue(o.get('traduccion')):
                        errores.append(f'{donde}: objetivo {o.get("id")} sin español e inglés')
                    o['titulo'] = _apoyo(o.get('titulo'))
                    o['traduccion'] = _apoyo(o.get('traduccion'))
            for v in t.get('vocabulario', []) + t.get('frases', []):
                if 'meta' in v:
                    generico = True
                    if not _bilingue(v.get('traduccion')):
                        errores.append(f'{donde}: {v.get("id")} sin traducción en español e inglés')
                    v['en'] = v.get('meta', '')
                    v['es'] = _apoyo(v.get('traduccion')) if isinstance(v.get('traduccion'), dict) else ''
    return generico


def validar(situaciones, idioma=None):
    global SOLO_EN
    SOLO_EN = idioma in APOYO_SOLO_EN
    errores = []
    situaciones = json.loads(json.dumps(situaciones))  # sin tocar el original
    generico = _normalizar(situaciones, errores)
    for s in situaciones:
        sid = s.get('id')
        tramos = s.get('tramos') or {}
        vistas = {}
        for tramo, letra in TRAMOS.items():
            t = tramos.get(tramo)
            donde = f's{sid} {tramo}'
            if not isinstance(t, dict):
                errores.append(f'{donde}: falta el tramo')
                continue
            objs, voc, fr = t.get('objetivos', []), t.get('vocabulario', []), t.get('frases', [])
            if len(objs) != 3:
                errores.append(f'{donde}: {len(objs)} objetivos (deben ser 3)')
            if len(voc) != 10:
                errores.append(f'{donde}: {len(voc)} palabras (deben ser 10)')
            if len(fr) != 4:
                errores.append(f'{donde}: {len(fr)} frases (deben ser 4)')
            for n, o in enumerate(objs, 1):
                esperado = f's{sid}-{OBJ_PREFIJO[tramo]}{n}'
                if o.get('id') != esperado:
                    errores.append(f'{donde}: objetivo {n} id {o.get("id")} (debe ser {esperado})')
                for k in ('titulo', 'frase', 'traduccion'):
                    if not str(o.get(k, '')).strip():
                        errores.append(f'{donde}: objetivo {n} sin {k}')
                if len(o.get('titulo', '')) > 60:
                    errores.append(f'{donde}: título largo «{o.get("titulo")}»')
                if palabras(o.get('frase', '')) > MAX_PALABRAS_FRASE[tramo]:
                    errores.append(f'{donde}: frase modelo larga «{o.get("frase")}»')
            for n, v in enumerate(voc, 1):
                esperado = f's{sid}-{letra}-v{n}'
                if v.get('id') != esperado:
                    errores.append(f'{donde}: vocabulario {n} id {v.get("id")} (debe ser {esperado})')
                en = str(v.get('en', '')).strip()
                if not en or not str(v.get('es', '')).strip() or not str(v.get('ejemplo', '')).strip():
                    errores.append(f'{donde}: vocabulario {n} incompleto')
                    continue
                if palabras(en) > 5:
                    errores.append(f'{donde}: «{en}» tiene más de 5 palabras')
                raiz = re.sub(r'[^a-zà-ÿœ]+', ' ', en.lower()).split()
                ejemplo = re.sub(r'[^a-zà-ÿœ]+', ' ', v['ejemplo'].lower())
                if generico and len(raiz) > 1 and raiz[0] in ('le', 'la', 'les', 'un', 'une', 'des', 'l', 'du', 'de',
                                                           'el', 'los', 'las', 'una', 'unos', 'unas'):
                    raiz = raiz[1:]  # el artículo no tiene que repetirse en el ejemplo
                if raiz and raiz[0][:4] not in ejemplo:
                    errores.append(f'{donde}: el ejemplo de «{en}» no la contiene')
                clave = en.lower()
                if clave in vistas:
                    errores.append(f'{donde}: «{en}» repetida (ya en {vistas[clave]})')
                vistas[clave] = tramo
            for n, f in enumerate(fr, 1):
                esperado = f's{sid}-{letra}-f{n}'
                if f.get('id') != esperado:
                    errores.append(f'{donde}: frase {n} id {f.get("id")} (debe ser {esperado})')
                if not str(f.get('en', '')).strip() or not str(f.get('es', '')).strip():
                    errores.append(f'{donde}: frase {n} incompleta')
            textos_es = [o.get('traduccion', '') for o in objs] + [v.get('es', '') for v in voc] + [f.get('es', '') for f in fr]
            textos_en = [o.get('frase', '') for o in objs] + [v.get('en', '') + ' ' + v.get('ejemplo', '') for v in voc] + [f.get('en', '') for f in fr]
            for x in ([] if generico else textos_en):
                m = BRITANICO.search(x)
                if m:
                    errores.append(f'{donde}: «{m.group(0)}» es inglés británico (usamos el americano)')
            # En el curso de español el español es la lengua meta (frase, meta, ejemplo).
            for x in (textos_en if SOLO_EN else textos_es):
                m = PENINSULAR.search(x)
                if m:
                    errores.append(f'{donde}: «{m.group(0)}» no es español neutro de América')
    return errores


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    datos = json.load(open(sys.argv[1], encoding='utf-8'))
    situaciones = datos['situaciones'] if isinstance(datos, dict) else datos
    # Idioma: el del archivo integrado o la carpeta del lote (situaciones/<idioma>/).
    idioma = datos.get('idioma') if isinstance(datos, dict) else pathlib.Path(sys.argv[1]).resolve().parent.name
    errores = validar(situaciones, idioma)
    for e in errores:
        print('ERROR', e)
    print(f'{len(situaciones)} situaciones, {len(errores)} errores')
    sys.exit(1 if errores else 0)


if __name__ == '__main__':
    main()
