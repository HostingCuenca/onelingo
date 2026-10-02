#!/usr/bin/env python3
"""Recoge los «Hechos del reparto confirmados» de las revisiones de un nivel
y los escribe en `hechosDelReparto` de su plan (PLAN_CLASES.md).

Cada revisión (`tools/contenido/ruta-<idioma>/revision-nX-bYY.md`) lista los
hechos en una sección «Hechos del reparto confirmados» con líneas
`- texto en español / text in English`. Así los autores del bloque siguiente
los leen en el plan y no contradicen la historia.

Uso: python3 tools/curriculo/reparto.py fr 2
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def hechos(texto):
    m = re.search(r'[Hh]echos del reparto[^\n]*\n(.*?)(?=\n#{1,3} |\Z)', texto, re.S)
    for linea in (m.group(1).splitlines() if m else []):
        linea = linea.strip()
        if linea.startswith('- ') and ' / ' in linea:
            es, en = linea[2:].rsplit(' / ', 1)
            yield es.strip(), en.strip()


def main():
    idioma, nivel = sys.argv[1], int(sys.argv[2])
    plan = RAIZ / f'curriculo/{idioma}/n{nivel}.json'
    datos = json.loads(plan.read_text(encoding='utf-8'))
    lista = []
    for b in range(1, 11):
        rev = RAIZ / f'tools/contenido/ruta-{idioma}/revision-n{nivel}-b{b:02d}.md'
        if rev.exists():
            lista += [{'es': es, 'en': en, 'bloque': b} for es, en in hechos(rev.read_text(encoding='utf-8'))]
    datos['hechosDelReparto'] = lista
    plan.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{plan.relative_to(RAIZ)}: {len(lista)} hechos del reparto')


if __name__ == '__main__':
    main()
