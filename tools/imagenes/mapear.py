#!/usr/bin/env python3
"""Asigna a cada palabra de la ruta y de las situaciones su imagen de la biblioteca
(tools/imagenes/biblioteca.json).

Genera assets/contenido/<idioma>/imagenes.json: {clave léxica: archivo}; la imagen
es assets/img/vocab/<archivo>.webp. La clave es la de `claveLexico` (lib/core/lexico/lexico.dart): el texto de la palabra
en minúsculas, sin espacios repetidos ni puntuación final.

La palabra se reconoce por su glosa inglesa (el propio texto en el curso de inglés,
la traducción `en` en los demás) y se confirma con la española, para no confundir
homógrafos: «the cold» = el resfriado no es el frío; «to park» no es el parque.

Uso:
  python3 tools/imagenes/mapear.py               # escribe los mapas y resume
  python3 tools/imagenes/mapear.py --comprobar   # falla si el mapa no está al día
  python3 tools/imagenes/mapear.py --dudas       # aceptadas solo por la glosa inglesa
"""
import json
import pathlib
import re
import sys
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parents[2]
CONTENIDO = RAIZ / 'assets/contenido'
IDIOMAS = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko']
BIBLIO = json.loads((RAIZ / 'tools/imagenes/biblioteca.json').read_text())['imagenes']
SIN_TRADUCCION = {'expresión del curso', 'expresión en inglés'}  # marcadores, no traducciones

# Categorías que puede ilustrar un verbo («to rain» → weather-rain, «to cough» → health-cough).
CATEGORIAS_VERBO = {'action', 'sport', 'weather', 'health', 'emotion'}

# Glosas inglesas simples cuya primera acepción en el curso no es la de la imagen.
EXCLUIDAS = {
    ('key', 'clave'), ('key', 'tecla'), ('table', 'tabla'), ('tablet', 'tableta'),
    ('lift', 'ascensor'), ('cold', 'resfriado'), ('heel', 'talon'), ('bank', 'orilla'),
    ('station', 'emisora'), ('work', 'obra'), ('stretch', 'tramo'), ('fall', 'otono'),
    ('draw', 'empate'), ('close', 'cerca'), ('short', 'bajo'), ('actor', 'persona responsable'),
    ('chair', 'moderador'), ('chair', 'presidente de la mesa'), ('chair', 'presidente de la reunion'),
    ('cabinet', 'gabinete'), ('glasses', 'vasos'), ('hike', 'subida'), ('orange', 'anaranjado'),
    ('outlet', 'medio de comunicacion'), ('print', 'imprimir'), ('print', 'estampado'),
    ('square', 'casilla'), ('store', 'guardar'), ('stressed', 'acentuada'), ('stressed', 'acentuado'),
    ('stressed', 'subrayo'), ('tag', 'coletilla'), ('tag', 'coletilla interrogativa'),
    ('tap', 'acercar la tarjeta'), ('board', 'directiva'), ('board', 'junta directiva'),
    ('breakdown', 'desglose'), ('checkout', 'salida del hotel'), ('curtain', 'telon'),
    ('drill', 'simulacro'), ('bag', 'funda'), ('match', 'combinar'), ('match', 'emparejar'),
    ('pill', 'hacer bolitas'), ('stretch', 'ensanchar'), ('work', 'funcionar'), ('worn out', 'gastado'),
}

# Sin glosa española no hay cómo saber la acepción de estas: sin imagen.
HOMOGRAFOS_EN = {
    'back', 'fall', 'draw', 'lift', 'light', 'land', 'board', 'match', 'tag', 'store', 'square',
    'scale', 'trunk', 'spring', 'heel', 'tablet', 'cold', 'short', 'close', 'iron', 'wave', 'shade',
    'field', 'novel', 'stretch', 'slip', 'freeze', 'catch', 'tap', 'fan', 'coach', 'band', 'fire',
    'bank', 'key', 'table', 'orange', 'park', 'train', 'cross', 'fix', 'rest', 'cut', 'hang', 'plug',
    'pipe', 'lock', 'box', 'shop', 'wash', 'work', 'pet', 'police', 'reception', 'picture',
}


def clave_lexico(t):
    t = re.sub(r'\s+', ' ', t.strip().lower())
    return re.sub(r'[.!?¿¡,;:]+$', '', t)


def sin_tildes(t):
    return ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')


def limpiar(t, articulos):
    t = re.sub(r'[.!?¡¿…«»"]+', '', t).strip().lower()
    return re.sub(rf'^(?:{articulos})\s+', '', t).strip()


def glosa_en(t):
    """(glosa de la primera acepción, es verbo, tiene matices) de «the bus (city)»."""
    t = (t or '').strip()
    primera = re.split(r'[(;,/]', t)[0]
    verbo = bool(re.match(r'\s*to\s', primera, re.I))
    return limpiar(primera, 'a|an|the|to'), verbo, primera.strip() != t


def glosas_es(t):
    """Todas las acepciones españolas, sin artículo ni tildes: «la carta, el menú» → {carta, menu}."""
    t = re.sub(r'\([^)]*\)', '', t or '')
    return {g for g in (sin_tildes(limpiar(p, 'el|la|los|las|un|una|unos|unas|mi|tu|su'))
                        for p in re.split(r'[;,/]| o ', t)) if g}


def emparenta(a, b):
    """Misma palabra o misma familia: llave/llaves, espera/esperar, reparación/reparar."""
    return a == b or (len(a) >= 5 and len(b) >= 5 and a[:5] == b[:5])


POR_CONCEPTO = {}
for img in BIBLIO:
    for c in img['conceptos']:
        POR_CONCEPTO.setdefault(c, []).append(img)


def elegir(en, es):
    """(archivo, dudosa) para una palabra con glosa inglesa `en` y española `es`."""
    g, verbo, matices = glosa_en(en)
    candidatos = [i for i in POR_CONCEPTO.get(g, [])
                  if not verbo or i['categoria'] in CATEGORIAS_VERBO]
    if not candidatos:
        return None, False
    if es and es not in SIN_TRADUCCION:
        ges = glosas_es(es)
        for img in candidatos:
            if any(emparenta(sin_tildes(img['es']), x) for x in ges):
                return img['archivo'], False
        # Sinónimo español (mamá / madre, zumo / jugo): vale si la glosa inglesa no
        # tiene matices y la imagen no es de otra clase de palabra.
        if matices or len(candidatos) > 1 or any((g, x) in EXCLUIDAS for x in ges):
            return None, False
        if not verbo and candidatos[0]['categoria'] in ('action', 'adjective'):
            return None, False
        return candidatos[0]['archivo'], True
    if len(candidatos) > 1 or matices or g in HOMOGRAFOS_EN:
        return None, False
    return candidatos[0]['archivo'], False


def palabras(idioma):
    """(texto en el idioma meta, glosa inglesa, glosa española) de la ruta y las situaciones."""
    for f in sorted((CONTENIDO / idioma / 'ruta').glob('*.json')):
        if f.name == 'curso.json':
            continue
        for u in json.loads(f.read_text()).get('unidades', []):
            for v in u.get('vocabulario', []):
                tr = v.get('traduccion') or {}
                yield (v['texto'], v['texto'] if idioma == 'en' else tr.get('en'),
                       v['texto'] if idioma == 'es' else tr.get('es'))
    sit = CONTENIDO / idioma / 'situaciones.json'
    if sit.exists():
        for s in json.loads(sit.read_text())['situaciones']:
            for t in s['tramos'].values():
                for v in t.get('vocabulario', []):
                    tr = v.get('traduccion') or {}
                    meta = v.get('meta') or v.get('en', '')
                    yield (meta, meta if idioma == 'en' else tr.get('en'),
                           meta if idioma == 'es' else tr.get('es'))


def mapa():
    salida, dudas = {}, []
    for idioma in IDIOMAS:
        votos = {}
        for texto, en, es in palabras(idioma):
            if not texto.strip():
                continue
            archivo, dudosa = elegir(en, es)
            if archivo:
                votos.setdefault(clave_lexico(texto), set()).add(archivo)
                if dudosa:
                    dudas.append((idioma, texto, en, es, archivo))
        # Una palabra que en el curso ilustra dos conceptos (fr «la glace») se queda sin imagen.
        salida[idioma] = {k: a.pop() for k, a in sorted(votos.items()) if len(a) == 1}
    return salida, dudas


def texto(m):
    return json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True) + '\n'


if __name__ == '__main__':
    m, dudas = mapa()
    if '--comprobar' in sys.argv:
        viejos = [i for i in IDIOMAS if not (CONTENIDO / i / 'imagenes.json').exists()
                  or (CONTENIDO / i / 'imagenes.json').read_text() != texto(m[i])]
        if viejos:
            sys.exit(f'imagenes.json no está al día en {", ".join(viejos)}: ejecuta tools/imagenes/mapear.py')
        print('imagenes.json al día en los 10 idiomas')
    elif '--dudas' in sys.argv:
        for d in sorted(set(dudas)):
            print(*d, sep='\t')
    else:
        for idioma in IDIOMAS:
            (CONTENIDO / idioma / 'imagenes.json').write_text(texto(m[idioma]))
        usadas = {a for i in m.values() for a in i.values()}
        for idioma, i in m.items():
            print(f'{idioma}: {len(i)} palabras con imagen')
        print(f'imágenes usadas: {len(usadas)}/{len(BIBLIO)} · aceptadas por sinónimo: {len(set(dudas))}')
