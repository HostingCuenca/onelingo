#!/usr/bin/env python3
"""Une la cabecera y los borradores revisados en assets/contenido/fr/nivel0/nivel0.json."""
import json
import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
datos = json.loads((AQUI / 'cabecera.json').read_text(encoding='utf-8'))
datos['unidades'] = []
for borrador in sorted((AQUI / 'borrador').glob('u*.json')):
    datos['unidades'] += json.loads(borrador.read_text(encoding='utf-8'))['unidades']
destino = RAIZ / 'assets/contenido/fr/nivel0/nivel0.json'
destino.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
r = subprocess.run([sys.executable, str(RAIZ / 'tools/contenido/validar_nivel0.py'), 'fr'])
sys.exit(r.returncode)
