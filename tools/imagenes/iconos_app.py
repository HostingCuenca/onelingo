#!/usr/bin/env python3
"""Íconos de la app (Android y web) a partir del logo oficial.

Usa solo el símbolo (la burbuja con el globo), sin el texto «OneLingo», que a
tamaño de ícono no se lee. Se vuelve a correr si cambia el logo:

    python3 tools/imagenes/iconos_app.py [--maestro <png redibujado>]

Con `--maestro` (una versión nítida de icono_openai.py) el símbolo se guarda en
tools/imagenes/icono-simbolo.png y sale de ahí; sin ese archivo, del logo.

Genera:
- Android: mipmap-*/ic_launcher.png (íconos clásicos) y el ícono adaptativo
  (mipmap-*/ic_launcher_foreground.png + mipmap-anydpi-v26/ic_launcher.xml,
  fondo blanco en values/ic_launcher_background.xml).
- Web: web/iconos/ (192, 512, maskable y apple-touch) y web/favicon.png. La
  carpeta no se llama «icons» porque Apache reserva /icons/ con un alias.
- Página de descarga: web/descargar/icono.png.
"""
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
LOGO = RAIZ / 'assets/img/logo-oficial-transparente.png'
# Símbolo nítido redibujado a partir del logo (icono_openai.py → --maestro).
SIMBOLO = RAIZ / 'tools/imagenes/icono-simbolo.png'
RES = RAIZ / 'android/app/src/main/res'
WEB = RAIZ / 'web'
BLANCO = (255, 255, 255, 255)


def simbolo_del_logo() -> Image.Image:
    """El símbolo del logo oficial: lo que hay por encima de la primera franja vacía."""
    im = Image.open(LOGO).convert('RGBA')
    alfa = im.split()[3]
    ancho, alto = im.size
    corte = next(y for y in range(alto // 2, alto)
                 if all(alfa.getpixel((x, y)) <= 40 for x in range(ancho)))
    parte = im.crop((0, 0, ancho, corte))
    return parte.crop(parte.getbbox())


def simbolo() -> Image.Image:
    """El símbolo nítido (icono-simbolo.png) si existe; si no, el del logo."""
    return Image.open(SIMBOLO).convert('RGBA') if SIMBOLO.exists() else simbolo_del_logo()


def importar_maestro(ruta: Path):
    """Guarda como icono-simbolo.png una versión redibujada sobre blanco
    (icono_openai.py): el blanco que toca los bordes pasa a transparente."""
    im = Image.open(ruta).convert('RGBA')
    fondo = Image.new('L', im.size, 0)
    blanco = Image.eval(im.convert('L'), lambda v: 255 if v >= 245 else 0)
    from PIL import ImageDraw
    relleno = blanco.copy()
    for esquina in ((0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)):
        ImageDraw.floodfill(relleno, esquina, 128)
    fondo = Image.eval(relleno, lambda v: 0 if v == 128 else 255)
    im.putalpha(fondo)
    im = im.crop(im.getbbox())
    im.save(SIMBOLO, optimize=True)
    print(SIMBOLO.relative_to(RAIZ), im.size)


def lienzo(lado: int, fraccion: float, fondo=BLANCO) -> Image.Image:
    """El símbolo centrado ocupando `fraccion` del lado, sobre `fondo`."""
    s = simbolo()
    escala = lado * fraccion / max(s.size)
    s = s.resize((round(s.width * escala), round(s.height * escala)), Image.LANCZOS)
    base = Image.new('RGBA', (lado, lado), fondo)
    base.alpha_composite(s, ((lado - s.width) // 2, (lado - s.height) // 2))
    return base


def guardar(im: Image.Image, ruta: Path, rgb=False):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    (im.convert('RGB') if rgb else im).save(ruta, optimize=True)
    print(ruta.relative_to(RAIZ), im.size)


def main():
    if '--maestro' in sys.argv:
        importar_maestro(Path(sys.argv[sys.argv.index('--maestro') + 1]))
    # Android: dp 48 (clásico) y 108 (adaptativo) por densidad.
    for carpeta, factor in {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}.items():
        guardar(lienzo(round(48 * factor), .82), RES / f'mipmap-{carpeta}/ic_launcher.png', rgb=True)
        # Zona segura del adaptativo: 66 de 108 dp; el símbolo ocupa ~54 dp.
        guardar(lienzo(round(108 * factor), .5, (0, 0, 0, 0)), RES / f'mipmap-{carpeta}/ic_launcher_foreground.png')
    xml = RES / 'mipmap-anydpi-v26/ic_launcher.xml'
    xml.parent.mkdir(parents=True, exist_ok=True)
    xml.write_text('<?xml version="1.0" encoding="utf-8"?>\n'
                   '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
                   '    <background android:drawable="@color/ic_launcher_background"/>\n'
                   '    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n'
                   '</adaptive-icon>\n')
    (RES / 'values/ic_launcher_background.xml').write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        '    <color name="ic_launcher_background">#FFFFFF</color>\n</resources>\n')

    # Web: íconos normales con margen y «maskable» con la zona segura (80 %).
    for lado in (192, 512):
        guardar(lienzo(lado, .84), WEB / f'iconos/Icon-{lado}.png', rgb=True)
        guardar(lienzo(lado, .62), WEB / f'iconos/Icon-maskable-{lado}.png', rgb=True)
    guardar(lienzo(180, .84), WEB / 'iconos/apple-touch-icon.png', rgb=True)
    guardar(lienzo(64, .96, (0, 0, 0, 0)), WEB / 'favicon.png')
    guardar(lienzo(192, .84), WEB / 'descargar/icono.png', rgb=True)


if __name__ == '__main__':
    main()
