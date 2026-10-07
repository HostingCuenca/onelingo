#!/usr/bin/env python3
"""Valida Fundamentos de coreano (ko-KR) en staging, como ruta-it/validar.py.

Contrasta `borrador-f0.json` (que escribe otro agente) con el plan
`curriculo/ko/f0.json` y, en un curso temporal, con el validador real de esquema
2 (`tools/validar_ruta.py`). No escribe en `assets/` ni modifica el runtime.

Reglas propias del coreano (tools/ia/idiomas/ko.md):
- `rom` (Romanización Revisada) en todo vocablo, ejemplo, celda y línea de
  diálogo; sin hangul, sin McCune-Reischauer ni diacríticos.
- Ítems de ejercicio: `textoRom`, `preguntaRom`, `opcionesRom`, `tokensRom` y
  `paresRom` según docs/claude-educacion/ROMANIZACION.md (tools/contenido/rom_items.py).
- Partículas pegadas: «conocida» descompone eojeol = raíz enseñada + partículas
  enseñadas (저는, 서울에서, 학생이에요, 오천 → números compuestos).
- `ordenar`: los tokens son eojeol completos (sin espacios, sin partículas
  sueltas).
- Sin Ecuador, Quito, Guayaquil ni Cuenca (ni en hangul); sin 당신 en el texto.
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
PLAN = RAIZ / 'curriculo' / 'ko' / 'f0.json'
VALIDADOR = RAIZ / 'tools' / 'validar_ruta.py'
MODULO = 'ko.f0'

# Listas cerradas de tools/ia/idiomas/ko.md (nombres propios = palabras libres).
APELLIDOS = ['김', '박', '최', '정', '강', '조', '윤', '장', '홍', '송']
NOMBRES_COMPLETOS = [
    '김지은', '박서연', '최민지', '정수빈', '강하윤', '조예린', '윤소희', '장유진',
    '김민준', '박도윤', '최지훈', '정현우', '강준호', '홍성민', '송동현',
]
NOMBRES_PILA = [
    '지은', '서연', '민지', '수빈', '하윤', '예린', '소희', '유진',
    '민준', '도윤', '지훈', '현우', '준호', '성민', '동현',
]
CIUDADES = ['서울', '부산', '인천', '대구', '대전', '광주', '수원', '울산', '전주', '제주']
NOMBRES_LIBRES = APELLIDOS + NOMBRES_COMPLETOS + NOMBRES_PILA + CIUDADES
ROM_PROPIOS = [
    'Gim', 'Bak', 'Choe', 'Jeong', 'Gang', 'Jo', 'Yun', 'Jang', 'Hong', 'Song',
    'Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon', 'Gwangju', 'Suwon', 'Ulsan', 'Jeonju', 'Jeju',
    # nombres de pila (se escriben Ji-eun, Min-jun…)
    'Ji-eun', 'Seo-yeon', 'Min-ji', 'Su-bin', 'Ha-yun', 'Ye-rin', 'So-hui', 'Yu-jin',
    'Min-jun', 'Do-yun', 'Ji-hun', 'Hyeon-u', 'Jun-ho', 'Seong-min', 'Dong-hyeon',
]

PROHIBIDAS = re.compile(
    r'\b(?:ecuador\w*|ecuatorian\w*|quito|guayaquil|cuenca)\b|에콰도르|키토|과야킬|쿠엥카',
    re.IGNORECASE,
)
PLANTILLA = re.compile(r'\b(?:placeholder|lorem ipsum|todo)\b', re.IGNORECASE)
HANGUL = re.compile(r'[ᄀ-ᇿ㄰-㆏가-힯]')
# RR: solo minúsculas ASCII, guion (nombres de pila), apóstrofo no se usa.
ROM_MALA = re.compile(r"[^A-Za-z0-9 \-.,?!()…:;]")

# Partículas y terminaciones que se pegan a la palabra. Solo cuentan si están
# enseñadas (en `conocidas`), salvo los números compuestos.
PARTICULAS = ['은', '는', '이', '가', '도', '에', '에서', '을', '를', '의', '와', '과', '만', '부터', '까지', '로', '으로']
COPULA = ['이에요', '예요', '이', '아니에요']
# Partículas que jamás deben ir como token suelto en `ordenar`.
SUELTAS = {'은', '는', '가', '도', '에', '에서', '을', '를', '의', '와', '과', '이에요', '예요'}
SINO = set('영공일이삼사오육칠팔구십백천만')


def recorrer(valor):
    yield valor
    if isinstance(valor, dict):
        for item in valor.values():
            yield from recorrer(item)
    elif isinstance(valor, list):
        for item in valor:
            yield from recorrer(item)


def conocida_ko(w: str, conocidas) -> bool:
    """Palabra conocida: eojeol = raíz enseñada + partículas/terminaciones enseñadas.

    También acepta números sinocoreanos compuestos cuyos dígitos están enseñados
    (이십, 십일, 삼백오십, 오천).
    """
    if w in conocidas or any(c.isdigit() for c in w):
        return True
    if len(w) > 1 and all(c in SINO for c in w) and all(c in conocidas for c in w):
        return True
    for i in range(1, len(w)):
        cabeza, cola = w[:i], w[i:]
        if cola in conocidas and (cola in PARTICULAS or cola in COPULA) and conocida_ko(cabeza, conocidas):
            return True
    return False


def error_rom(rom: str):
    if not isinstance(rom, str) or not rom.strip():
        return 'rom vacío'
    if HANGUL.search(rom):
        return 'rom contiene hangul'
    if ROM_MALA.search(rom):
        return f'rom con caracteres no RR: {sorted(set(ROM_MALA.findall(rom)))}'
    # Mayúscula solo en nombres propios de la ficha (apellidos, nombres de pila, ciudades).
    for pal in re.findall(r'[A-Za-z]+(?:-[A-Za-z]+)*', rom):
        if pal[0].isupper() and pal not in ROM_PROPIOS and pal.split('-')[0] not in ROM_PROPIOS:
            return f'rom con mayúscula fuera de nombres propios: {pal}'
    return None


def validar_rom(ruta, errores):
    """`rom` obligatorio en vocabulario, ejemplos, tablas y diálogos."""
    for u in ruta.get('unidades', []):
        uid = u.get('id', '?')
        for v in u.get('vocabulario', []):
            if HANGUL.search(str(v.get('texto', ''))):
                e = error_rom(v.get('rom'))
                if e:
                    errores.append(f'{uid}.vocabulario «{v.get("texto")}»: {e}')
        for p in u.get('pasos', []):
            donde = f'{uid}.{p.get("id", p.get("tipo"))}'
            if p.get('tipo') in ('ejemplos', 'patron'):
                for x in p.get('items', []) or []:
                    if isinstance(x, dict) and HANGUL.search(str(x.get('texto', ''))):
                        e = error_rom(x.get('rom'))
                        if e:
                            errores.append(f'{donde} «{x.get("texto")}»: {e}')
            for i, d in enumerate(p.get('dialogo', []) or []):
                if HANGUL.search(str(d.get('texto', ''))):
                    e = error_rom(d.get('rom'))
                    if e:
                        errores.append(f'{donde}.dialogo[{i}]: {e}')
            if p.get('tipo') == 'tabla':
                for fila in p.get('filas', []):
                    for celda in fila:
                        if isinstance(celda, dict) and 'texto' in celda and HANGUL.search(str(celda['texto'])):
                            e = error_rom(celda.get('rom'))
                            if e:
                                errores.append(f'{donde} celda «{celda["texto"]}»: {e}')
    errores.extend(rom_items.errores(ruta, lambda t: isinstance(t, str) and bool(HANGUL.search(t)),
                                     lambda _t, rom: error_rom(rom.replace('___', '')) if rom.replace('___', '').strip() else None))


def validar_ordenar(ruta, errores):
    """Tokens = eojeol completos; las partículas van pegadas."""
    for u in ruta.get('unidades', []):
        for p in u.get('pasos', []):
            for it in p.get('items', []) or []:
                if it.get('formato') != 'ordenar':
                    continue
                donde = f'{u.get("id")}.{p.get("id")}.{it.get("id")}'
                tokens = it.get('tokens') or []
                limpios = [re.sub(r'[.,!?]+$', '', t) for t in tokens]
                for t in tokens:
                    if re.search(r'\s', t) or not t:
                        errores.append(f'{donde}: token «{t}» con espacio o vacío (un token = un eojeol)')
                if [t for t in limpios if t in SUELTAS]:
                    errores.append(
                        f'{donde}: partícula suelta en tokens {[t for t in limpios if t in SUELTAS]}; '
                        'va pegada a su palabra (저는, 학생이에요)'
                    )
                resp = re.sub(r'[.,!?]+', '', it.get('respuesta', ''))
                if len(tokens) != len(resp.split()):
                    errores.append(f'{donde}: {len(tokens)} tokens para {len(resp.split())} eojeol en la respuesta')


def validar_registro(ruta, errores, avisos):
    """Sin 당신; 너 solo como advertencia en diálogos."""
    for u in ruta.get('unidades', []):
        for p in u.get('pasos', []):
            for i, d in enumerate(p.get('dialogo', []) or []):
                t = str(d.get('texto', ''))
                if '당신' in t:
                    errores.append(f'{u.get("id")}.{p.get("id")}.dialogo[{i}]: usa 당신 (se evita)')
                if re.search(r'(?<![가-힣])너(?:는|도|가|를|의)?(?![가-힣])', t):
                    avisos.append(f'{u.get("id")}.{p.get("id")}.dialogo[{i}]: usa 너 (solo 반말)')
            for it in p.get('items', []) or []:
                if '당신' in str(it.get('respuesta', '')):
                    errores.append(f'{u.get("id")}.{p.get("id")}.{it.get("id")}: respuesta con 당신')


def main() -> None:
    if not PLAN.exists():
        print(f'ERROR: falta el plan {PLAN}')
        raise SystemExit(2)
    if not BORRADOR.exists():
        print(
            f'ERROR: no existe el borrador {BORRADOR}.\n'
            '       Lo escribe otro agente a partir de curriculo/ko/f0.json; '
            'ejecuta este validador cuando exista.'
        )
        raise SystemExit(2)
    try:
        plan = json.loads(PLAN.read_text(encoding='utf-8'))
        ruta = json.loads(BORRADOR.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        print(f'ERROR: JSON inválido: {exc}')
        raise SystemExit(2)
    errores: list[str] = []
    avisos: list[str] = []

    if ruta.get('modulo') != MODULO:
        errores.append(f'raíz: modulo debe ser {MODULO}')
    plan_u = plan.get('unidades', [])
    ruta_u = ruta.get('unidades', [])
    if len(plan_u) != 9:
        errores.append(f'plan: se esperan 9 unidades, hay {len(plan_u)}')
    if len(ruta_u) != len(plan_u):
        errores.append(f'raíz: se esperan {len(plan_u)} unidades, hay {len(ruta_u)}')

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
        rom_plan = {v.get('texto'): v.get('rom') for v in ficha.get('vocabulario', [])}
        for v in unidad.get('vocabulario', []):
            if v.get('texto') in rom_plan and v.get('rom') != rom_plan[v.get('texto')]:
                errores.append(f'{uid}: rom de «{v.get("texto")}» distinto del plan ({rom_plan[v.get("texto")]})')

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

    # Sin Ecuador (tools/ia/idiomas/ko.md): ni en el coreano ni en el apoyo.
    if any(PROHIBIDAS.search(x) for x in textos):
        errores.append('raíz: menciona Ecuador o una ciudad ecuatoriana')

    validar_rom(ruta, errores)
    validar_ordenar(ruta, errores)
    validar_registro(ruta, errores, avisos)

    with tempfile.TemporaryDirectory(prefix='onelingo-ko-f0-') as temporal:
        base = Path(temporal)
        carpeta = base / 'ko' / 'ruta'
        carpeta.mkdir(parents=True)
        shutil.copy2(BORRADOR, carpeta / 'f0.json')
        curso = {
            'esquema': 2,
            'idioma': 'ko',
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
                'id': MODULO, 'nivel': 'f0', 'archivo': 'f0.json',
                'titulo': {'es': 'Fundamentos', 'en': 'Foundations'},
            }],
        }
        (carpeta / 'curso.json').write_text(
            json.dumps(curso, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
        )
        spec = importlib.util.spec_from_file_location('validar_ruta_ko_staging', VALIDADOR)
        modulo = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(modulo)
        modulo.RAIZ = base
        # validar_ruta.py no trae prueba de «palabra conocida» para el coreano
        # (usa la inglesa por defecto): aquí se sustituye por la que entiende
        # partículas pegadas y números compuestos.
        modulo.conocida_para = lambda idioma: conocida_ko
        validador = modulo.Validador('ko')
        errores.extend(validador.validar())
        avisos.extend(validador.advertencias)

    for aviso in avisos:
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
