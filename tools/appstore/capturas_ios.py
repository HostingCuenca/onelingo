"""Recompone las capturas de Google Play (1080x1920) al tamaño que pide
App Store Connect para iPhone (1206x2622): mismo fondo, título en Nunito
y la pantalla del teléfono recortada de la captura de Play.

Uso: python3 tools/appstore/capturas_ios.py
Salida: docs/appstore/capturas/<idioma>-NN-*.png
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parents[2]
ORIGEN = RAIZ / "docs/play/graficos"
DESTINO = RAIZ / "docs/appstore/capturas"
FUENTE = RAIZ / "assets/fonts/Nunito.ttf"

W, H = 1206, 2622
ARRIBA, ABAJO = (68, 24, 186), (46, 15, 134)
MARCO = (155, 284, 926, 1911)  # teléfono dentro de la captura de Play
RADIO = 64

CAPTURAS = {
    "es": [
        ("es-01-videollamada", "Habla en videollamada\ncon tu tutor de IA"),
        ("es-02-tutores", "12 tutores con voz\ny personalidad propias"),
        ("es-03-gramatica", "Gramática clara,\nexplicada en tu idioma"),
        ("es-04-vocabulario", "Vocabulario con\nilustraciones y audio"),
        ("es-05-practica", "Practica situaciones\nde la vida real"),
        ("es-06-inicio", "10 idiomas,\na tu ritmo"),
    ],
    "en": [
        ("en-01-tutors", None),
        ("en-02-practice", None),
        ("en-03-vocabulary", None),
        ("en-04-home", None),
    ],
}


def fondo():
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(ARRIBA, ABAJO)))
    # la onda clara de abajo a la izquierda, como en Play
    capa = Image.new("L", (W, H), 0)
    ImageDraw.Draw(capa).ellipse((-900, 1450, 700, 3400), fill=255)
    im.paste(Image.new("RGB", (W, H), (83, 40, 200)), (0, 0), capa)
    return im


def fuente(tam):
    f = ImageFont.truetype(str(FUENTE), tam)
    try:
        f.set_variation_by_axes([800])
    except Exception:
        pass
    return f


def telefono(origen):
    tel = Image.open(origen).convert("RGB").crop(MARCO)
    mascara = Image.new("L", tel.size, 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0, tel.width - 1, tel.height - 1), RADIO, fill=255)
    tel.putalpha(mascara)
    ancho = 960
    return tel.resize((ancho, round(tel.height * ancho / tel.width)), Image.LANCZOS)


def titulo_play(origen):
    """Para las capturas en inglés reutiliza el título de Play tal cual."""
    im = Image.open(origen).convert("RGB")
    return im.crop((0, 60, 1080, 270))


def componer(nombre, titulo):
    im = fondo()
    d = ImageDraw.Draw(im)
    y_tel = 520
    if titulo:
        f = fuente(86)
        d.multiline_text((W // 2, 150), titulo, font=f, fill="white", anchor="ma", align="center", spacing=22)
    else:
        banda = titulo_play(ORIGEN / f"{nombre}.png")
        banda = banda.resize((W, round(banda.height * W / banda.width)), Image.LANCZOS)
        # se funde con el degradado: solo se copian los píxeles claros (el texto)
        gris = banda.convert("L").point(lambda v: 255 if v > 150 else 0)
        im.paste(banda, (0, 110), gris)
    tel = telefono(ORIGEN / f"{nombre}.png")
    im.paste(tel, ((W - tel.width) // 2, y_tel), tel)
    DESTINO.mkdir(parents=True, exist_ok=True)
    salida = DESTINO / f"{nombre}.png"
    im.save(salida, optimize=True)
    return salida, tel.height + y_tel


if __name__ == "__main__":
    for idioma, lista in CAPTURAS.items():
        for nombre, titulo in lista:
            salida, fin = componer(nombre, titulo)
            print(salida.relative_to(RAIZ), Image.open(salida).size, "fin del teléfono:", fin)
