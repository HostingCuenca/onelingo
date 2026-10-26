#!/usr/bin/env python3
"""Une las partes de un lote (partes/sNN.json, una situación por archivo) en lote-N.json.

Uso: python3 tools/contenido/situaciones/unir_partes.py <idioma> <N>
Cada parte es una lista con una situación o la situación sola. Valida el lote al final.
"""
import json
import pathlib
import subprocess
import sys

DIR = pathlib.Path(__file__).resolve().parent
idioma, n = sys.argv[1], int(sys.argv[2])
lote = []
for sid in range((n - 1) * 10 + 1, n * 10 + 1):
    p = DIR / idioma / 'partes' / f's{sid:02d}.json'
    if not p.exists():
        sys.exit(f'falta {p.relative_to(DIR.parents[2])}')
    d = json.loads(p.read_text(encoding='utf-8'))
    s = d[0] if isinstance(d, list) else d
    assert s['id'] == sid, f'{p.name}: id {s["id"]}'
    lote.append({'id': s['id'], 'tramos': s['tramos']})
destino = DIR / idioma / f'lote-{n}.json'
destino.write_text(json.dumps(lote, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('Escrito', destino.relative_to(DIR.parents[2]))
sys.exit(subprocess.run([sys.executable, str(DIR.parent / 'validar_situaciones.py'), str(destino)]).returncode)
