#!/usr/bin/env python3
"""Versión nítida del símbolo de OneLingo para los íconos, redibujada por OpenAI
a partir del logo oficial (el original está comprimido y se pixela).

    python3 tools/imagenes/icono_openai.py <carpeta de salida> [n]

Guarda `icono-N.png` (1024×1024, fondo blanco; `iconos_app.py` lo vuelve
transparente donde hace falta). Se elige uno a ojo y se
pasa a `iconos_app.py --maestro <png>`. La clave se toma como en
tools/ia/openai_contenido.py y nunca se imprime.
"""
import base64
import io
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ia'))
from openai_contenido import _clave  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from iconos_app import simbolo_del_logo  # noqa: E402

MODELO = 'gpt-image-2'
PROMPT = (
    'Redraw this exact logo symbol as a crisp, clean, flat vector-style app icon. '
    'Keep the same composition and colors: the white number 1 inside a speech bubble with a '
    'blue-to-purple gradient, the globe with a rainbow grid of colored tiles, the orange arc '
    'around it and the small red dot. Smooth edges, no noise, no blur, no compression artifacts, '
    'no text, no extra elements. Centered with a small margin on a plain pure white background.'
)


def multipart(campos: dict, archivos: dict) -> tuple[bytes, str]:
    limite = 'onelingo-icono'
    cuerpo = io.BytesIO()
    for k, v in campos.items():
        cuerpo.write(f'--{limite}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for k, (nombre, datos) in archivos.items():
        cuerpo.write(f'--{limite}\r\nContent-Disposition: form-data; name="{k}"; filename="{nombre}"\r\n'
                     'Content-Type: image/png\r\n\r\n'.encode())
        cuerpo.write(datos + b'\r\n')
    cuerpo.write(f'--{limite}--\r\n'.encode())
    return cuerpo.getvalue(), f'multipart/form-data; boundary={limite}'


def main():
    salida = Path(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    salida.mkdir(parents=True, exist_ok=True)
    s = simbolo_del_logo()
    lado = max(s.size) + 80
    from PIL import Image
    base = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
    base.alpha_composite(s, ((lado - s.width) // 2, (lado - s.height) // 2))
    png = io.BytesIO()
    base.resize((1024, 1024), Image.LANCZOS).save(png, 'PNG')
    cuerpo, tipo = multipart(
        {'model': MODELO, 'prompt': PROMPT, 'n': n, 'size': '1024x1024',
         'quality': 'high', 'output_format': 'png'},
        {'image[]': ('simbolo.png', png.getvalue())},
    )
    req = urllib.request.Request('https://api.openai.com/v1/images/edits', data=cuerpo, method='POST',
                                 headers={'Authorization': f'Bearer {_clave()}', 'Content-Type': tipo})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            datos = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'OpenAI respondió {e.code}: {e.read().decode()[:400]}')
    for i, d in enumerate(datos['data'], 1):
        (salida / f'icono-{i}.png').write_bytes(base64.b64decode(d['b64_json']))
        print(salida / f'icono-{i}.png')
    print('uso:', json.dumps(datos.get('usage', {})))


if __name__ == '__main__':
    main()
