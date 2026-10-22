# Aplica una hoja de 3 texturas editada fuera (cabeza | cuerpo | mechones, en
# fila y con el mismo encuadre UV): toma sus colores y les devuelve el detalle
# fino de la textura original de 2048 px, para que no se vea borrosa.
#   python3 usar_hoja.py hoja.png carpeta_texturas prefijo salida/
import sys, os, shutil, numpy as np
from PIL import Image, ImageFilter
hoja, tex, pre, sal = sys.argv[1:5]
os.makedirs(sal, exist_ok=True)
for f in os.listdir(tex): shutil.copy(os.path.join(tex, f), sal)
u = Image.open(hoja).convert('RGB'); W, H = u.size; p = W / 3
LUM = np.array([.3, .59, .11], np.float32)
arr = lambda im: np.asarray(im).astype(np.float32) / 255
for i, n in enumerate(['head_color', 'body_color', 'opacity_color']):
    o = Image.open(os.path.join(tex, f'{pre}_{n}.tga')); L = o.size[0]
    rgb = o.convert('RGB'); alfa = o.split()[3] if o.mode == 'RGBA' else None
    nuevo = arr(u.crop((round(i * p), 0, round((i + 1) * p), H)).resize((L, L), Image.LANCZOS))
    org = arr(rgb); detalle = org - arr(rgb.filter(ImageFilter.GaussianBlur(3)))
    base = arr(Image.fromarray((nuevo * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)))
    # Donde la edición aclaró mucho (pelo negro → plateado) el detalle original
    # es tenue: se amplifica en la misma proporción.
    ganancia = np.clip((base @ LUM) / np.maximum(arr(rgb.filter(ImageFilter.GaussianBlur(3))) @ LUM, .05), 1, 3)[..., None]
    out = np.clip(base + detalle * ganancia, 0, 1)
    im = Image.fromarray((out * 255).astype(np.uint8))
    if alfa is not None: im.putalpha(alfa)  # la forma de cada mechón sale del original
    im.save(os.path.join(sal, f'{pre}_{n}.tga'))
print('LISTO', sal)
