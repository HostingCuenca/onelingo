#!/usr/bin/env python3
"""Lecturas de palabras japonesas cortas para la voz: backend/src/lib/lecturas_ja.json.

Un kanji suelto («星», «生», «今日») es ambiguo para la voz: sin contexto elige una
lectura cualquiera (星 salió «ほしい»; cortos ja 19-10-2026). El vocabulario de la
ruta trae la lectura que se enseña: «星 (ほし)». Este script junta, de los vocablos
de assets/contenido/ja/ruta, los kanji sueltos (y las lecturas especiales de
JUKUJIKUN: 今日, 明日…) con UNA sola lectura en todo el curso; `textoParaVoz` (backend/src/lib/voz.ts) manda a la
voz esa lectura en kana cuando el texto entero es una de esas palabras.

  python3 tools/voz/lecturas_ja.py            # escribe el JSON
  python3 tools/voz/lecturas_ja.py --informe  # solo cuenta
"""
import argparse
import collections
import glob
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = os.path.join(RAIZ, 'backend', 'src', 'lib', 'lecturas_ja.json')
KANJI = re.compile(r'[㐀-鿿々]')
KANA = re.compile(r'^[ぁ-ゟ゠-ヿー]+$')
# Palabras de dos kanji cuya lectura no sale de sus partes (jukujikun) o es ambigua.
JUKUJIKUN = {'今日', '明日', '昨日', '今年', '今朝', '一人', '二人', '大人', '上手', '下手',
             '一日', '二日', '果物', '眼鏡', '部屋', '時計', '景色', '土産', '迷子', '真似'}
VOCABLO = re.compile(r'^\s*([^\s()（）]+)\s*\(([^)]*)\)')


def vocablos(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'vocabulario' and isinstance(v, list):
                for e in v:
                    if isinstance(e, dict) and isinstance(e.get('texto'), str):
                        yield e['texto']
            yield from vocablos(v)
    elif isinstance(o, list):
        for v in o:
            yield from vocablos(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--informe', action='store_true')
    a = ap.parse_args()
    lecturas = collections.defaultdict(set)
    for f in sorted(glob.glob(os.path.join(RAIZ, 'assets/contenido/ja/ruta/*.json'))):
        for t in vocablos(json.load(open(f, encoding='utf8'))):
            m = VOCABLO.match(t)
            if not m:
                continue
            base, lect = m.group(1), re.split(r'[,、;；]', m.group(2))[0].strip()
            if (len(base) == 1 or base in JUKUJIKUN) and KANJI.search(base) and KANA.match(lect):
                lecturas[base].add(lect)
    unicas = {k: next(iter(v)) for k, v in sorted(lecturas.items()) if len(v) == 1}
    dudosas = {k: sorted(v) for k, v in lecturas.items() if len(v) > 1}
    print(f'{len(unicas)} palabras con lectura única; {len(dudosas)} con varias (no entran): {dict(list(dudosas.items())[:12])}')
    if not a.informe:
        with open(SALIDA, 'w', encoding='utf8') as f:
            json.dump(unicas, f, ensure_ascii=False, indent=0, sort_keys=True)
            f.write('\n')


if __name__ == '__main__':
    main()
