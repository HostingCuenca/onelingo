#!/usr/bin/env python3
"""Valida Fundamentos de chino mandarín (zh-CN) en staging, como ruta-it/validar.py.

Contrasta `borrador-f0.json` con el plan `curriculo/zh/f0.json`, aplica las
reglas propias de `tools/ia/idiomas/zh.md` (palabras separadas por espacios,
`rom` en pinyin con marcas y sandhi escrito, puntuación china, solo caracteres
simplificados, sin Ecuador; en los ítems, `textoRom`, `preguntaRom`, `opcionesRom`,
`tokensRom` y `paresRom` según docs/claude-educacion/ROMANIZACION.md) y delega el esquema 2 en el validador real
(`tools/validar_ruta.py`) sobre un curso temporal. No escribe en `assets/` ni
modifica el runtime.

Uso: python3 tools/contenido/ruta-zh/validar.py
Salida: 0 sin errores; 1 con errores; 2 si falta el borrador o el plan.
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
BORRADOR = Path(__file__).with_name('borrador-f0.json')
PLAN = RAIZ / 'curriculo' / 'zh' / 'f0.json'
VALIDADOR = RAIZ / 'tools' / 'validar_ruta.py'
CURSO = RAIZ / 'assets' / 'contenido' / 'zh' / 'ruta' / 'curso.json'
INTEGRAR = Path(__file__).with_name('integrar.py')

# Listas cerradas de tools/ia/idiomas/zh.md (hanzi y pinyin): palabras libres.
APELLIDOS = [('王', 'Wáng'), ('李', 'Lǐ'), ('张', 'Zhāng'), ('刘', 'Liú'), ('陈', 'Chén'),
             ('杨', 'Yáng'), ('黄', 'Huáng'), ('赵', 'Zhào'), ('吴', 'Wú'), ('周', 'Zhōu')]
NOMBRES = [('芳', 'Fāng'), ('梅', 'Méi'), ('丽', 'Lì'), ('敏', 'Mǐn'), ('静', 'Jìng'),
           ('雪', 'Xuě'), ('婷', 'Tíng'), ('英', 'Yīng'), ('伟', 'Wěi'), ('强', 'Qiáng'),
           ('磊', 'Lěi'), ('涛', 'Tāo'), ('浩', 'Hào'), ('军', 'Jūn'), ('亮', 'Liàng')]
CIUDADES = [('北京', 'Běijīng'), ('上海', 'Shànghǎi'), ('广州', 'Guǎngzhōu'), ('深圳', 'Shēnzhèn'),
            ('成都', 'Chéngdū'), ('杭州', 'Hángzhōu'), ('西安', "Xī'ān"), ('南京', 'Nánjīng'),
            ('武汉', 'Wǔhàn'), ('重庆', 'Chóngqìng')]
NOMBRES_LIBRES = [p for par in APELLIDOS + NOMBRES + CIUDADES for p in par]

PROHIBIDAS = re.compile(
    r'\b(?:ecuador\w*|ecuatorian\w*|quito|guayaquil|cuenca)\b|厄瓜多[尔爾]|基多|瓜亚基尔|昆卡',
    re.IGNORECASE)
PLANTILLA = re.compile(r'\b(?:placeholder|lorem ipsum|todo)\b', re.IGNORECASE)

HANZI = re.compile(r'[一-鿿]')
CORRIDA_HANZI = re.compile(r'[一-鿿]+')
PUNT_ZH = '。，？！、；：…'
PUNT_ASCII_TEXTO = re.compile(r'[,.?!;:]')
PAUSA_ROM = set(',.?!;:…—')
# Palabras de 5 caracteres permitidas sin espacios (el resto de corridas >= 5 avisa).
LARGAS_OK = {'哥伦比亚人'}
# Caracteres que solo existen en tradicional (el curso es en simplificado).
TRADICIONALES = set(
    '們說話語這個學車書國會還開認識謝對麼嗎見問號愛買賣錢請歡爾來時間點為沒關係'
    '馬點電腦飯館師親兒媽學習漢區現與兩幾歲貴價鐘')
ROM_PERMITIDOS = set("abcdefghijklmnopqrstuwxyzü '.,?!…-—:;()")  # sin «v»
TONOS = {'̄': 1, '́': 2, '̌': 3, '̀': 4}


def recorrer(valor, clave=None):
    """Genera (clave, valor) para cada nodo; las listas heredan la clave del padre."""
    yield clave, valor
    if isinstance(valor, dict):
        for k, item in valor.items():
            yield from recorrer(item, k)
    elif isinstance(valor, list):
        for item in valor:
            yield from recorrer(item, clave)


def dicts(valor):
    for _, v in recorrer(valor):
        if isinstance(v, dict):
            yield v


def parse_rom(texto: str):
    """Devuelve (plano, tonos): plano en minúsculas sin marcas, tonos[idx] = 1..4."""
    plano: list[str] = []
    tonos: dict[int, int] = {}
    for ch in unicodedata.normalize('NFD', texto):
        if ch in TONOS:
            if plano:
                tonos[len(plano) - 1] = TONOS[ch]
        elif ch == '̈':
            if plano and plano[-1].lower() == 'u':
                plano[-1] = 'ü'
            else:
                plano.append(ch)
        else:
            plano.append(ch.lower())
    return ''.join(plano), tonos


def primer_tono(grupo: str):
    """Tono de la primera sílaba de un grupo de pinyin; 0 si es neutra o no se sabe."""
    plano, tonos = parse_rom(grupo)
    if not tonos:
        return 0
    p = min(tonos)
    if re.fullmatch(r"[^aeiouü]*[iuü]?", plano[:p]):
        return tonos[p]
    return 0


def errores_rom(rom: str, donde: str) -> tuple[list[str], list[str]]:
    errores: list[str] = []
    avisos: list[str] = []
    plano, tonos = parse_rom(rom)
    malos = sorted({c for c in plano if c not in ROM_PERMITIDOS})
    if malos:
        errores.append(f'{donde}: rom con caracteres no válidos {malos} (sin números de tono, sin «v», sin hanzi)')
        return errores, avisos
    if re.search(r'[a-zü][1-5](?![a-zü0-9])', plano):
        errores.append(f'{donde}: rom con números de tono; usa marcas (nǐ, no ni3)')

    # Sandhi 3.º + 3.º: dos 3.º consecutivos sin pausa ni sílaba neutra intermedia.
    marcadas = sorted(tonos)
    for a, b in zip(marcadas, marcadas[1:]):
        if tonos[a] != 3 or tonos[b] != 3:
            continue
        entre = plano[a + 1:b]
        if any(c in PAUSA_ROM for c in entre):
            continue
        resto = entre[len(re.match(r'[aeiouü]{0,2}', entre).group(0)):]
        m = re.search(r"[^aeiouü]*[iuü]?$", resto)
        if m and re.search(r'[aeiouü]', resto[:m.start()]):
            continue  # hay una sílaba neutra en medio
        errores.append(f'{donde}: sandhi 3.º+3.º sin aplicar en «{rom}» (el primero se escribe con 2.º)')
        break

    # 不 / 一 como grupo suelto, según el tono de la palabra siguiente.
    grupos = rom.split()
    for i, g in enumerate(grupos[:-1]):
        limpio = g.strip('.,?!;:…')
        if limpio != g.rstrip() or any(c in PAUSA_ROM for c in g):
            continue
        t = primer_tono(grupos[i + 1])
        if not t:
            continue
        if limpio.lower() == 'bù' and t == 4:
            errores.append(f'{donde}: «bù» ante 4.º tono debe escribirse «bú» en «{rom}»')
        elif limpio.lower() == 'bú' and t != 4:
            errores.append(f'{donde}: «bú» solo ante 4.º tono en «{rom}»')
        elif limpio.lower() == 'yí' and t != 4:
            avisos.append(f'{donde}: «yí» solo ante 4.º tono en «{rom}»')
        elif limpio.lower() == 'yì' and t == 4:
            avisos.append(f'{donde}: «yì» no va ante 4.º tono (¿yí?) en «{rom}»')
    return errores, avisos


def sin_etiqueta(s: str) -> str:
    """Quita «Hablante:» al inicio de una línea de diálogo."""
    return re.sub(r'^[^一-鿿:：\n]{1,30}[:：]\s*', '', s)


def mayormente_chino(s: str) -> bool:
    s = sin_etiqueta(s)
    h = len(HANZI.findall(s))
    letras = len(re.findall(r'[A-Za-zÀ-ɏ]', s))
    return h >= 2 and h > letras


def errores_texto_chino(s: str, donde: str) -> tuple[list[str], list[str]]:
    errores: list[str] = []
    avisos: list[str] = []
    t = sin_etiqueta(s)
    for corrida in CORRIDA_HANZI.findall(t):
        if len(corrida) > 5 or (len(corrida) == 5 and corrida not in LARGAS_OK):
            errores.append(f'{donde}: «{corrida}» ({len(corrida)} caracteres sin espacios); '
                           'separa las palabras: «我 是 学生。»')
    if PUNT_ASCII_TEXTO.search(t):
        errores.append(f'{donde}: puntuación latina en texto chino «{s}»; usa 。，？！、')
    if re.search(rf'\s[{PUNT_ZH}]', t):
        errores.append(f'{donde}: espacio antes de la puntuación china en «{s}»')
    if re.search(rf'[{PUNT_ZH}]\s+\S', t):
        errores.append(f'{donde}: espacio tras la puntuación china en «{s}» (la puntuación va pegada)')
    if '  ' in t:
        errores.append(f'{donde}: doble espacio en «{s}»')
    if re.search(r'\d', t):
        errores.append(f'{donde}: cifras en texto chino «{s}»; escribe los números en caracteres')
    trad = sorted({c for c in t if c in TRADICIONALES})
    if trad:
        errores.append(f'{donde}: caracteres tradicionales {trad}; usa simplificados')
    return errores, avisos


def grupos_hanzi(texto: str) -> int:
    n = 0
    for tok in sin_etiqueta(texto).split():
        tok = tok.strip(PUNT_ZH + '“”"\'()（）')
        if tok and HANZI.search(tok):
            n += 1
    return n


def grupos_rom(rom: str) -> int:
    return len([g for g in (x.strip('.,?!;:…—-"\'()') for x in rom.split()) if g])


def cargar_libres() -> list[str]:
    libres = list(NOMBRES_LIBRES)
    if CURSO.exists():
        libres += json.loads(CURSO.read_text(encoding='utf-8')).get('palabrasLibres', [])
    prohibidas_integrar: list[str] = []
    if INTEGRAR.exists():
        spec = importlib.util.spec_from_file_location('integrar_zh', INTEGRAR)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        libres += list(getattr(modulo, 'NOMBRES_LIBRES', []))
        prohibidas_integrar = list(getattr(modulo, 'PROHIBIDAS', []))
    return [p for p in dict.fromkeys(libres) if p not in prohibidas_integrar]


def main() -> None:
    if not PLAN.exists():
        print(f'ERROR: falta el plan {PLAN.relative_to(RAIZ)}', file=sys.stderr)
        raise SystemExit(2)
    if not BORRADOR.exists():
        print(
            f'ERROR: no existe {BORRADOR.relative_to(RAIZ)}.\n'
            'El borrador de Fundamentos de chino lo escribe un autor a partir de '
            'curriculo/zh/f0.json y tools/ia/idiomas/zh.md; aún no está creado.',
            file=sys.stderr,
        )
        raise SystemExit(2)

    plan = json.loads(PLAN.read_text(encoding='utf-8'))
    ruta = json.loads(BORRADOR.read_text(encoding='utf-8'))
    errores: list[str] = []
    avisos: list[str] = []

    if ruta.get('modulo') != 'zh.f0':
        errores.append('raíz: modulo debe ser zh.f0')
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

        vocab_plan = {v.get('texto'): v for v in ficha.get('vocabulario', [])}
        vocab_ruta = {v.get('texto'): v for v in unidad.get('vocabulario', [])}
        if set(vocab_plan) != set(vocab_ruta):
            errores.append(
                f'{uid}: vocabulario diverge; falta={sorted(set(vocab_plan) - set(vocab_ruta))}, '
                f'sobra={sorted(set(vocab_ruta) - set(vocab_plan))}'
            )
        for texto, v in vocab_ruta.items():
            if not v.get('rom'):
                errores.append(f'{uid}: vocablo «{texto}» sin rom (obligatoria en el vocabulario)')
            elif texto in vocab_plan and v.get('rom') != vocab_plan[texto].get('rom'):
                errores.append(f'{uid}: rom de «{texto}» diverge del plan '
                               f'({v.get("rom")!r} frente a {vocab_plan[texto].get("rom")!r})')
            if texto in vocab_plan and v.get('clasificador') != vocab_plan[texto].get('clasificador'):
                avisos.append(f'{uid}: clasificador de «{texto}» diverge del plan')

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

    # Reglas propias del chino sobre todo el borrador.
    vistos: set[str] = set()
    for clave, valor in recorrer(ruta):
        if not isinstance(valor, str):
            continue
        if clave == 'rom' or (clave or '').endswith('Rom'):
            if not valor:
                continue  # posición sin hanzi en una lista paralela
            e, a = errores_rom(valor.replace('___', ''), f'{clave} «{valor}»')
            errores.extend(e)
            avisos.extend(a)
        elif mayormente_chino(valor) and valor not in vistos:
            vistos.add(valor)
            e, a = errores_texto_chino(valor, f'{clave or "texto"}')
            errores.extend(e)
            avisos.extend(a)
    for d in dicts(ruta):
        rom = d.get('rom')
        if not isinstance(rom, str):
            continue
        for campo in ('texto', 'zh', 'hanzi'):
            zh = d.get(campo)
            if isinstance(zh, str) and HANZI.search(zh):
                if grupos_hanzi(zh) != grupos_rom(rom):
                    errores.append(
                        f'{campo} «{zh}» tiene {grupos_hanzi(zh)} palabras y rom «{rom}» tiene '
                        f'{grupos_rom(rom)} grupos; deben coincidir uno a uno')
                break

    def comprobar_item(zh: str, rom: str):
        if grupos_hanzi(zh) != grupos_rom(rom.replace('___', '')):
            return (f'«{zh}» tiene {grupos_hanzi(zh)} palabras y «{rom}» tiene '
                    f'{grupos_rom(rom.replace("___", ""))} grupos; deben coincidir uno a uno')
        return None

    errores.extend(rom_items.errores(ruta, lambda t: isinstance(t, str) and bool(HANZI.search(t)), comprobar_item))

    textos = [x for _, x in recorrer(ruta) if isinstance(x, str)]
    if any(PLANTILLA.search(x) for x in textos):
        errores.append('raíz: contiene texto plantilla')

    # Sin Ecuador (tools/ia/idiomas/zh.md): ni en el chino ni en el apoyo.
    if any(PROHIBIDAS.search(x) for x in textos):
        errores.append('raíz: menciona Ecuador o una ciudad ecuatoriana')

    with tempfile.TemporaryDirectory(prefix='onelingo-zh-f0-') as temporal:
        base = Path(temporal)
        carpeta = base / 'zh' / 'ruta'
        carpeta.mkdir(parents=True)
        shutil.copy2(BORRADOR, carpeta / 'f0.json')
        curso = {
            'esquema': 2,
            'idioma': 'zh',
            'version': 'staging',
            'revision': 'inicial',
            'idiomasApoyo': ['es', 'en'],
            'apoyoPredeterminado': 'es',
            'palabrasLibres': cargar_libres(),
            'vocabularioEstricto': True,
            'niveles': [{
                'id': 'f0', 'cefr': 'Pre-A1', 'nivelInterno': 0,
                'estado': 'publicado',
                'titulo': {'es': 'Fundamentos', 'en': 'Foundations'},
            }],
            'modulos': [{
                'id': 'zh.f0', 'nivel': 'f0', 'archivo': 'f0.json',
                'titulo': {'es': 'Fundamentos', 'en': 'Foundations'},
            }],
        }
        (carpeta / 'curso.json').write_text(
            json.dumps(curso, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
        )
        try:
            spec = importlib.util.spec_from_file_location('validar_ruta_zh_staging', VALIDADOR)
            modulo = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(modulo)
            modulo.RAIZ = base
            validador = modulo.Validador('zh')
            errores.extend(validador.validar())
            avisos.extend(validador.advertencias)
        except Exception as exc:  # el validador real puede no soportar aún «zh»
            errores.append(
                f'validar_ruta.py no pudo validar zh ({type(exc).__name__}: {exc}); '
                'revisa si soporta idioma «zh» (tokenización por espacios, palabrasLibres)'
            )

    for aviso in avisos:
        print('ADVERTENCIA:', aviso)
    for error in errores:
        print('ERROR:', error)
    ruta_vocab = sum(len(u.get('vocabulario', [])) for u in ruta_u)
    ejercicios = sum(
        len(next((p for p in u.get('pasos', []) if p.get('tipo') == tipo), {}).get('items', []))
        for u in ruta_u
        for tipo in ('practica_guiada', 'practica_independiente', 'situacion', 'evaluacion')
    )
    print(
        f'{len(errores)} errores · {len(ruta_u)} unidades · '
        f'{ruta_vocab} vocablos · {ejercicios} ejercicios'
    )
    raise SystemExit(1 if errores else 0)


if __name__ == '__main__':
    main()
