# Piel más clara (porcelana) y pelo platino sobre las texturas de un Rocketbox.
#   python3 recolorear.py carpeta_texturas prefijo pestanas.json salida/
# Piel: píxeles de tono piel se llevan a un tono claro conservando el detalle.
# Pelo: lo oscuro y poco saturado fuera de la cara (cabeza) y toda la textura
# de mechones (menos las pestañas) pasa a platino, con el relieve de cada mechón.
import sys, os, json, shutil, numpy as np
from PIL import Image, ImageFilter
tex, pre, pest, sal = sys.argv[1:5]
os.makedirs(sal, exist_ok=True)
for f in os.listdir(tex): shutil.copy(os.path.join(tex, f), sal)
LUM = np.array([.3, .59, .11], np.float32)
PIEL = np.array([.94, .80, .72], np.float32)   # porcelana cálida
PLATINO = np.array([.93, .94, .97], np.float32)

def cargar(n, modo='RGB'): return np.asarray(Image.open(os.path.join(tex, f'{pre}_{n}.tga')).convert(modo)).astype(np.float32) / 255
def guardar(a, n, modo='RGB'): Image.fromarray((a.clip(0, 1) * 255).astype(np.uint8), modo).save(os.path.join(sal, f'{pre}_{n}.tga'))
def blur(m, r): return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255
def mascara_piel(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]; mx, mn = c.max(-1), c.min(-1); sat = (mx - mn) / (mx + 1e-3)
    return ((r > g) & (g > b) & (r - b > .08) & (sat > .12) & (sat < .62) & (c @ LUM > .22) & (c @ LUM < .92)).astype(np.float32)
def aclarar(c, M):
    media = c[M > .5].mean(0)
    nuevo = c / media * PIEL
    return c * (1 - M[..., None]) + nuevo * M[..., None]
def platino(c, M, ref):
    l = c @ LUM; lo, hi = np.percentile(l[ref], 5), np.percentile(l[ref], 97)
    t = np.clip((l - lo) / (hi - lo + 1e-3), 0, 1)
    nuevo = PLATINO * (.68 + .32 * t)[..., None]
    return c * (1 - M[..., None]) + nuevo * M[..., None]

# Cabeza
c = cargar('head_color'); L = c.shape[0]
piel = blur(mascara_piel(c), 2)
cara = np.asarray(Image.fromarray((piel > .5).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.MinFilter(31))) > 0  # piel con cejas y ojos dentro
mx, mn = c.max(-1), c.min(-1); sat = (mx - mn) / (mx + 1e-3)
y = np.arange(L)[:, None] / L; x = np.arange(L)[None, :] / L
atlas_ojos = ((x < .2) & (y > .6)) | ((x > .19) & (x < .33) & (y > .83))  # boca por dentro y globo ocular
pelo = (c @ LUM < .32) & ((sat < .55) | (c @ LUM < .15)) & ~cara & ~atlas_ojos
pelo = blur(pelo.astype(np.float32), 1.5)
c = aclarar(c, piel * (1 - pelo))
c = platino(c, pelo, pelo > .5)
guardar(c, 'head_color')
# Cuerpo: solo la piel (la ropa queda); se borra el tatuaje del brazo.
c = cargar('body_color')
piel = blur(mascara_piel(c), 2)
suave = np.asarray(Image.fromarray((c * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(21))).astype(np.float32) / 255
tinta = (piel > .3) & (c @ LUM < suave @ LUM - .035)
tinta = blur(np.asarray(Image.fromarray(tinta.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(15))).astype(np.float32) / 255, 4)
c = c * (1 - tinta[..., None]) + suave * tinta[..., None]
if len(sys.argv) > 5:  # recuadro del tatuaje x0,y0,x1,y1 (0–1): se rellena con la piel de alrededor
    x0, y0, x1, y1 = (int(float(v) * c.shape[0]) for v in sys.argv[5].split(','))
    zona = Image.fromarray((c[y0:y1, x0:x1] * 255).astype(np.uint8))
    fondo = np.asarray(zona.filter(ImageFilter.MedianFilter(61))).astype(np.float32) / 255
    sub = c[y0:y1, x0:x1]; t = blur((sub @ LUM < fondo @ LUM - .015).astype(np.float32), 3)
    h, w = sub.shape[:2]; yy, xx = np.mgrid[0:h, 0:w]
    elipse = blur((((yy - h / 2) / (h / 2)) ** 2 + ((xx - w / 2) / (w / 2)) ** 2 < .8).astype(np.float32), 8)
    fondo = np.asarray(Image.fromarray((fondo * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
    t = np.maximum(np.clip(t * 2.5, 0, 1), elipse); c[y0:y1, x0:x1] = sub * (1 - t[..., None]) + fondo * t[..., None]
c = aclarar(c, blur(mascara_piel(c), 2))  # máscara de nuevo: donde estaba el tatuaje ya es piel
guardar(c, 'body_color')
# Mechones (con alfa), menos las pestañas.
o = cargar('opacity_color', 'RGBA'); rgb, a = o[..., :3], o[..., 3]; L = a.shape[0]
quitar = np.zeros_like(a, bool)
for x0, y0, x1, y1 in json.load(open(pest)):
    quitar[int((1 - y1) * L) - 4:int((1 - y0) * L) + 4, int(x0 * L) - 4:int(x1 * L) + 4] = True
M = ((a > .02) & ~quitar).astype(np.float32)
rgb = platino(rgb, M, (a > .5) & ~quitar)
guardar(np.dstack([rgb, a]), 'opacity_color', 'RGBA')
print('LISTO', sal)
