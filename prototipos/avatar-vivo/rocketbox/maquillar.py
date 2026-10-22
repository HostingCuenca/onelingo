# Maquillaje sobre la textura de la cara de un Rocketbox: labial, delineado y
# sombra en el párpado superior, rubor y cejas un poco más definidas. Las zonas
# salen de los blendshapes del propio modelo (scripts/zonas.py), así caen
# exactamente sobre labios, párpados y mejillas de esa cara.
#   python3 maquillar.py zonas.npz head_color.tga salida.png [labial=#b8455c]
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from mascaras import rasterizar
from PIL import Image, ImageFilter
zonas, tex, salida = sys.argv[1:4]
labial = sys.argv[4] if len(sys.argv) > 4 else '#a8475a'
d = np.load(zonas); im = Image.open(tex).convert('RGB'); L = im.size[0]
img = np.asarray(im).astype(np.float32) / 255
n = lambda a: a / (a.max() + 1e-9)
def mascara(w, desenfoque):
    M = Image.fromarray((rasterizar(d['tris'], d['tuv'], w, L) * 255).astype(np.uint8))
    return np.asarray(M.filter(ImageFilter.GaussianBlur(desenfoque * L / 1024))).astype(np.float32) / 255
def mezclar(img, color, M, alfa, modo='multiplicar'):
    c = np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
    capa = img * c if modo == 'multiplicar' else np.broadcast_to(c, img.shape)
    a = (M * alfa)[..., None]
    return img * (1 - a) + capa * a
# Labios: el labio superior se reconoce por el color (más rojo que la piel de
# alrededor); el inferior tiene brillo y se confunde con la piel, así que sale
# de la geometría (lo que más se mueve al meter los labios).
def suavizar(M, *filtros):
    I = Image.fromarray((M * 255).astype(np.uint8))
    for f in filtros: I = I.filter(f)
    return np.asarray(I).astype(np.float32) / 255
wr = n(d['MouthRollLower'] + d['MouthRollUpper'])
Z = suavizar(rasterizar(d['tris'], d['tuv'], n(wr + n(d['MouthPucker'])), L), ImageFilter.MaxFilter(9), ImageFilter.GaussianBlur(4 * L / 1024))
r, g, b = img[..., 0], img[..., 1], img[..., 2]
f = (r - g) / (r + g + b + 1e-3)
piel, tope = np.median(f[(Z > .1) & (Z < .35)]), np.percentile(f[Z > .15], 97)
color = np.clip((f - piel - .25 * (tope - piel)) / .015, 0, 1) * (Z > .3) * (suavizar(rasterizar(d['tris'], d['tuv'], wr, L), ImageFilter.MaxFilter(15)) > .25)
color = suavizar(color, ImageFilter.MedianFilter(7), ImageFilter.MaxFilter(3), ImageFilter.GaussianBlur(1.2 * L / 1024))
geo = suavizar(rasterizar(d['tris'], d['tuv'], np.clip((wr - .6) / .2, 0, 1), L), ImageFilter.GaussianBlur(1.5 * L / 1024))
labio = np.maximum(color, geo)
lc = np.array([int(labial[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
lum = (img @ np.array([.3, .59, .11], np.float32))[..., None]
pintado = np.clip(lc * np.clip(lum / np.percentile(lum[labio > .5], 75), 0, 1.15), 0, 1)  # el tono del labial con el relieve del labio
img = img * (1 - labio[..., None] * .7) + pintado * labio[..., None] * .7
# Párpado superior: sombra suave cálida y delineado oscuro en el borde (lo que más baja al parpadear).
zp = n(d['EyeBlinkLeft'] + d['EyeBlinkRight'])
img = mezclar(img, '#a87a72', mascara(zp ** 1.2, 7), .55)
# Delineado: franja justo encima del hueco del ojo (en la textura es la zona
# oscura dentro del párpado), más gruesa hacia afuera, y pestaña inferior suave.
hueco = (mascara(zp, 3) > .25) & ((img @ np.array([.3, .59, .11], np.float32)) < .33)
arriba = np.zeros_like(hueco); abajo = np.zeros_like(hueco)
for k in range(1, int(7 * L / 2048) + 1): arriba |= np.roll(hueco, -k, axis=0)
for k in range(1, int(3 * L / 2048) + 1): abajo |= np.roll(hueco, k, axis=0)
lin = Image.fromarray(((arriba & ~hueco) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5 * L / 2048))
inf = Image.fromarray(((abajo & ~hueco) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5 * L / 2048))
img = mezclar(img, '#1e1412', np.asarray(lin).astype(np.float32) / 255, .8, 'color')
img = mezclar(img, '#3a2622', np.asarray(inf).astype(np.float32) / 255, .35, 'color')
# Rubor: pómulos (zona de la mejilla al entrecerrar los ojos), bajada y difusa.
zm = n(d['CheekSquintLeft'] + d['CheekSquintRight']) * (1 - n(d['EyeBlinkLeft'] + d['EyeBlinkRight']))
M = mascara(zm, 18); M = np.roll(M, int(22 * L / 1024), axis=0)
img = mezclar(img, '#f2a3a0', M, .35)
Image.fromarray((img.clip(0, 1) * 255).astype(np.uint8)).save(salida)
print('LISTO', salida, L)
