# Extiende el color de los mechones hacia sus bordes transparentes. Las
# texturas de pelo traen fondo claro detrás del alfa y, al filtrar la textura,
# ese color se cuela como líneas claras en el borde de cada mechón.
#   python3 sangrar.py textura_opacity.tga
import sys, numpy as np
from PIL import Image, ImageFilter
p = sys.argv[1]; im = Image.open(p).convert('RGBA'); a = np.asarray(im.split()[3]).astype(np.float32) / 255
rgb = np.asarray(im.convert('RGB')).astype(np.float32); lleno = a > .5
acc, peso = rgb * lleno[..., None], lleno.astype(np.float32)
for r in (2, 4, 8, 16, 32, 64):  # promedios cada vez más amplios de lo opaco
    A = np.asarray(Image.fromarray(np.clip(acc, 0, 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(r))).astype(np.float32)
    P = np.asarray(Image.fromarray((peso * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(r))).astype(np.float32) / 255
    color = A / np.maximum(P, 1e-3)[..., None]; nuevo = (~lleno) & (P > .02) & (peso == 0)
    acc[nuevo] = color[nuevo]; peso[nuevo] = 1
out = np.where(lleno[..., None], rgb, acc).clip(0, 255).astype(np.uint8)
o = Image.fromarray(out); o.putalpha(im.split()[3]); o.save(p); print('LISTO', p)
