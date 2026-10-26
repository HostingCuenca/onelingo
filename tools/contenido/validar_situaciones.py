#!/usr/bin/env python3
"""Valida contenido de situaciones v2 (docs/claude-educacion/SITUACIONES_V2.md).

Uso:
  python3 tools/contenido/validar_situaciones.py assets/contenido/en/situaciones.json
  python3 tools/contenido/validar_situaciones.py tools/contenido/situaciones/borrador/lote-1.json

Acepta el archivo final ({"situaciones": [...]}) o un lote (lista de situaciones).
Sale con código 1 si hay errores.
"""
import importlib.util
import json
import pathlib
import re
import sys
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parents[2]

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


# Nunca se menciona Ecuador (la app es para EE. UU. y Latinoamérica); el curso de
# español es la excepción: se ambienta en Quito.
ECUADOR = re.compile(
    r'\b(?:ecuador\w*|ecuatorian\w*|quito|guayaquil|cuenca)\b|эквадор|厄瓜多|에콰도르|エクアドル', re.I)

# Romanización en los idiomas sin alfabeto latino (docs/claude-educacion/ROMANIZACION.md,
# reglas de cada tools/ia/idiomas/<idioma>.md). Como en el curso (rom en ejercicios hasta
# N4, después solo en vocabulario): el básico la lleva en todo (`fraseRom`, `metaRom`,
# `ejemploRom`); intermedio y avanzado, solo `metaRom` del vocabulario. En japonés, una
# palabra con kanji lleva además `lectura` en kana (la voz lee esa, no el kanji).
ROM_IDIOMAS = {'ru', 'ja', 'ko', 'zh'}
_MODULOS = {}


def _modulo(nombre, ruta):
    if nombre not in _MODULOS:
        sys.path.insert(0, str(RAIZ / 'tools/contenido'))
        spec = importlib.util.spec_from_file_location(nombre, RAIZ / ruta)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _MODULOS[nombre] = m
    return _MODULOS[nombre]


ESCRITURA = {
    'ru': re.compile(r'[А-Яа-яЁё]'),
    'ko': re.compile(r'[가-힯]'),
    'ja': re.compile(r'[ぁ-ゖァ-ヺ一-鿿]'),
    'zh': re.compile(r'[一-鿿]'),
}
KANJI = re.compile(r'[一-鿿]')
KANA = re.compile(r'[ぁ-ゖァ-ヺー]')
# Básico (N1–N3) del japonés: solo kana y los kanji que el curso enseña en N1–N2.
KANJI_BASICO_JA = set('日本人私先生学円水駅何今')


def _error_rom(idioma, texto, rom):
    """Mensaje si `rom` no es la romanización de `texto` según la ficha (o None)."""
    if not isinstance(rom, str) or not rom.strip():
        return 'sin romanización'
    if ESCRITURA[idioma].search(rom):
        return 'la romanización lleva la escritura del idioma'
    if idioma == 'ru':
        errores = []
        _modulo('ruta_ru', 'tools/contenido/ruta-ru/validar.py').comprobar_par('', '', texto, rom, errores)
        return errores[0].lstrip(': ') if errores else None
    if idioma == 'ko':
        e = _modulo('ruta_ko', 'tools/contenido/ruta-ko/validar.py').error_rom(rom)
        if e:
            return e
        # RR con los cambios fonéticos de la ficha, eojeol por eojeol (nombre completo = 2).
        e = _modulo('rr_ko', 'tools/contenido/rr_ko.py').errores_rom(texto, rom)
        return e[0] if e else None
    if idioma == 'zh':
        m = _modulo('ruta_zh', 'tools/contenido/ruta-zh/validar.py')
        e, _ = m.errores_rom(rom, '')
        if '不' not in texto:
            # «bù» de 部 o 步 no cambia de tono ante un 4.º: solo 不 hace sandhi.
            e = [x for x in e if '«bù»' not in x]
        if e:
            return e[0].lstrip(': ')
        if re.search(r'[,.?!;:][^\s,.?!;:…"”)]', rom):
            return f'«{rom}»: en el pinyin va un espacio tras la puntuación («Hǎo, shūbāo»)'
        # Como en el curso: «好，书包 我…» (puntuación pegada) ↔ «Hǎo, shūbāo wǒ…».
        palabras = [t for t in re.split(r'[\s。，？！、；：…]+', texto) if m.HANZI.search(t)]
        grupos = [g for g in re.split(r'[\s,.?!;:…]+', rom) if re.search(r'[a-zü]', g, re.I)]
        if len(palabras) != len(grupos):
            return f'«{texto}» tiene {len(palabras)} palabras y «{rom}» {len(grupos)} grupos (tras la coma, espacio en el pinyin)'
        return None
    # ja: Hepburn de la ficha cuando el texto va en kana; con kanji, al menos un grupo por palabra.
    hep = _modulo('hepburn_ja', 'tools/contenido/hepburn_ja.py')
    e = hep.errores_rom(texto, rom)
    if e:
        return e[0]
    if len(texto.split()) != len(rom.split()):
        return f'«{texto}» tiene {len(texto.split())} palabras y «{rom}» {len(rom.split())} grupos'
    return None


def _error_texto(idioma, texto, tramo):
    """Forma del texto en la escritura del idioma (o None)."""
    if idioma == 'zh':
        e, _ = _modulo('ruta_zh', 'tools/contenido/ruta-zh/validar.py').errores_texto_chino(texto, '')
        return e[0].lstrip(': ') if e else None
    if idioma == 'ja':
        if '\u3000' in texto:
            return 'espacio de ancho completo'
        if re.search(r'[ぁ-ヿ一-鿿][.,!?;]', texto):
            return f'puntuación ASCII en «{texto}» (usa 。、？！)'
        if re.search(r'\s[。、？！]', texto):
            return f'espacio antes de la puntuación en «{texto}»'
        if re.search(r'(?<!\s)\S{9,}', re.sub(r'[。、？！「」]', ' ', texto)) and KANA.search(texto):
            return f'¿faltan espacios entre palabras? «{texto}»'
        if tramo == 'basico':
            fuera = sorted({k for k in KANJI.findall(texto) if k not in KANJI_BASICO_JA})
            if fuera:
                return f'kanji {fuera} en el básico (va en kana; solo {"".join(sorted(KANJI_BASICO_JA))})'
    if idioma == 'ru' and '\u0301' in unicodedata.normalize('NFD', texto).replace('й', '').replace('Й', ''):
        return f'marca de acento en el cirílico «{texto}» (el acento va solo en el rom)'
    return None


def validar_rom(situaciones, idioma):
    errores = []
    for s in situaciones:
        for tramo, t in (s.get('tramos') or {}).items():
            donde = f's{s.get("id")} {tramo}'
            basico = tramo == 'basico'
            campos = []  # (id, campo, texto, rom, obligatorio)
            for o in t.get('objetivos', []):
                campos.append((o.get('id'), 'frase', o.get('frase', ''), o.get('fraseRom'), basico))
            for v in t.get('vocabulario', []):
                campos.append((v.get('id'), 'meta', v.get('meta', ''), v.get('metaRom'), True))
                campos.append((v.get('id'), 'ejemplo', v.get('ejemplo', ''), v.get('ejemploRom'), basico))
                if idioma == 'ja':
                    lectura = v.get('lectura')
                    if KANJI.search(v.get('meta', '')) and not (lectura and KANA.search(lectura) and not KANJI.search(lectura)):
                        errores.append(f'{donde}: {v.get("id")} «{v.get("meta")}» lleva kanji y le falta `lectura` en kana')
                    elif lectura and not KANJI.search(v.get('meta', '')):
                        errores.append(f'{donde}: {v.get("id")} lleva `lectura` sin kanji en «{v.get("meta")}»')
                elif 'lectura' in v:
                    errores.append(f'{donde}: {v.get("id")} lleva `lectura` (solo japonés)')
                # El ejemplo contiene la palabra: su primer carácter (o los 3 primeros en ruso,
                # que declina y conjuga) aparece en el ejemplo.
                meta = re.sub(r'\s+', '', v.get('meta', ''))
                if idioma == 'ru':
                    raiz = (re.findall(r'[А-Яа-яЁё]+', v.get('meta', '').lower()) or [''])[0][:3]
                    ok = raiz in v.get('ejemplo', '').lower()
                else:
                    ok = meta[:1] in v.get('ejemplo', '')
                if meta and not ok:
                    errores.append(f'{donde}: el ejemplo de «{v.get("meta")}» no la contiene')
            for f in t.get('frases', []):
                campos.append((f.get('id'), 'meta', f.get('meta', ''), f.get('metaRom'), basico))
            for cid, campo, texto, rom, obligatorio in campos:
                if e := _error_texto(idioma, texto, tramo):
                    errores.append(f'{donde}: {cid} {campo}: {e}')
                if obligatorio:
                    if e := _error_rom(idioma, texto, rom):
                        errores.append(f'{donde}: {cid} {campo}Rom: {e}')
                elif rom is not None:
                    errores.append(f'{donde}: {cid} lleva {campo}Rom (en {tramo} solo el vocabulario la lleva)')
    return errores


def validar(situaciones, idioma=None):
    global SOLO_EN
    SOLO_EN = idioma in APOYO_SOLO_EN
    errores = []
    situaciones = json.loads(json.dumps(situaciones))  # sin tocar el original
    for x in ([] if idioma == 'es' else re.findall(r'"(?:[^"\\]|\\.)*"', json.dumps(situaciones, ensure_ascii=False))):
        if ECUADOR.search(x):
            errores.append(f'mención a Ecuador: {x[:80]}')
            break
    if '⚠' in json.dumps(situaciones, ensure_ascii=False):
        errores.append('símbolo «⚠» en el contenido (la traducción correcta basta)')
    if idioma in ROM_IDIOMAS:
        errores += validar_rom(situaciones, idioma)
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
                                                           'el', 'los', 'las', 'una', 'unos', 'unas',
                                                           'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
                                                           'der', 'die', 'das', 'ein', 'eine', 'sich',
                                                           'il', 'lo', 'gli', 'i', 'uno'):
                    # el artículo (o el «sich» del reflexivo alemán, que en el ejemplo
                    # va conjugado: «Ich melde mich») no tiene que repetirse en el ejemplo
                    raiz = raiz[1:]
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
    # Idioma: el del archivo integrado o la carpeta del lote (situaciones/<idioma>/[partes/]).
    carpeta = pathlib.Path(sys.argv[1]).resolve().parent
    if carpeta.name == 'partes':  # situaciones/<idioma>/partes/sNN.json
        carpeta = carpeta.parent
    idioma = datos.get('idioma') if isinstance(datos, dict) else carpeta.name
    errores = validar(situaciones, idioma)
    for e in errores:
        print('ERROR', e)
    print(f'{len(situaciones)} situaciones, {len(errores)} errores')
    sys.exit(1 if errores else 0)


if __name__ == '__main__':
    main()
