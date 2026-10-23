#!/usr/bin/env python3
"""Revisa la biblioteca de imágenes de vocabulario contra tools/imagenes/biblioteca.json.

Uso:
  python3 tools/imagenes/revisar.py                  # avance por lote, faltantes y nombres desconocidos
  python3 tools/imagenes/revisar.py --renombrar 3    # ChatGPT web: work/imagenes-vocab/lote-003/*.png
                                                     #   → originales/<archivo>.png por orden de descarga
"""
import json
import pathlib
import sys

from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[2]
BASE = RAIZ / 'work/imagenes-vocab'
ORIG = BASE / 'originales'
BIBLIO = json.loads((RAIZ / 'tools/imagenes/biblioteca.json').read_text())['imagenes']


def renombrar(lote):
    carpeta = BASE / f'lote-{lote:03d}'
    esperadas = [i for i in BIBLIO if i['lote'] == lote]
    hechas = {p.stem for p in ORIG.glob('*.png')}
    pendientes = [i for i in esperadas if i['archivo'] not in hechas]
    fotos = sorted((p for p in carpeta.iterdir() if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp')), key=lambda p: p.stat().st_mtime)
    if len(fotos) != len(pendientes):
        sys.exit(f'{carpeta}: hay {len(fotos)} imágenes y faltan {len(pendientes)} del lote; no renombro nada.')
    for foto, item in zip(fotos, pendientes):
        Image.open(foto).convert('RGB').save(ORIG / f"{item['archivo']}.png")
        print(f"{foto.name} → {item['archivo']}.png ({item['es']})")


def revisar():
    archivos = {p.stem: p for p in ORIG.glob('*.png')}
    conocidas = {i['archivo'] for i in BIBLIO}
    por_lote = {}
    for i in BIBLIO:
        por_lote.setdefault(i['lote'], []).append(i)
    total = 0
    for lote, items in sorted(por_lote.items()):
        hechas = [i for i in items if i['archivo'] in archivos]
        total += len(hechas)
        if hechas:
            faltan = ', '.join(i['archivo'] for i in items if i['archivo'] not in archivos)
            print(f"lote {lote:03d}: {len(hechas)}/{len(items)}" + (f" · faltan: {faltan}" if faltan else ''))
    for nombre, p in sorted(archivos.items()):
        if nombre not in conocidas:
            print(f'nombre desconocido: {p.name}')
            continue
        ancho, alto = Image.open(p).size
        if ancho != alto or ancho < 512:
            print(f'{p.name}: {ancho}×{alto} (se espera cuadrada y de al menos 512 px)')
    print(f'total: {total}/{len(BIBLIO)}')


if __name__ == '__main__':
    ORIG.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:2] == ['--renombrar']:
        renombrar(int(sys.argv[2]))
    else:
        revisar()
