#!/usr/bin/env python3
"""Descarga emoji de Noto (Google, Apache 2.0) y los guarda como WebP.

No se generan imágenes: se usan emoji con licencia de uso comercial
(créditos en assets/img/emoji/CREDITOS.md).

Uso:
  python3 tools/contenido/descargar_emoji.py 1f431 1f6cf ...
  python3 tools/contenido/descargar_emoji.py --faltan fr   # los que pide el Nivel 0 de un idioma
"""
import io
import pathlib
import subprocess
import sys
import urllib.request

from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[2]
DESTINO = RAIZ / 'assets/img/emoji'
FUENTE = 'https://raw.githubusercontent.com/googlefonts/noto-emoji/main/2D/png/128/emoji_u{}.png'


def descargar(codigo):
    salida = DESTINO / f'{codigo}.webp'
    if salida.exists():
        return 'ya estaba'
    with urllib.request.urlopen(FUENTE.format(codigo), timeout=30) as r:
        imagen = Image.open(io.BytesIO(r.read())).convert('RGBA')
    imagen.save(salida, 'WEBP', quality=90)
    return f'{salida.stat().st_size} bytes'


def main():
    args = sys.argv[1:]
    if args[:1] == ['--faltan']:
        r = subprocess.run(
            [sys.executable, str(RAIZ / 'tools/contenido/validar_nivel0.py'), args[1]],
            capture_output=True, text=True,
        )
        linea = next((l for l in r.stdout.splitlines() if l.startswith('EMOJI QUE FALTAN')), '')
        args = linea.split(':', 1)[1].split() if linea else []
    for c in args:
        try:
            print(c, descargar(c.lower()))
        except Exception as e:  # noqa: BLE001
            print(c, 'ERROR', e)


if __name__ == '__main__':
    main()
