#!/usr/bin/env python3
"""Consolida lotes editoriales aprobados en el plan canónico N1.

Uso:
  python3 tools/curriculo/consolidar_n1.py pt archivo1.json ... archivoN.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[2]


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit('uso: consolidar_n1.py IDIOMA LOTE1 LOTE2 [...]')

    idioma = sys.argv[1]
    archivos = [Path(x) for x in sys.argv[2:]]
    outline_p = RAIZ / 'tools' / 'curriculo' / idioma / 'n1-outline.json'
    salida = RAIZ / 'curriculo' / idioma / 'n1.json'
    outline = json.loads(outline_p.read_text(encoding='utf-8'))
    bases = {clase['id']: clase for clase in outline['clases']}
    clases: list[dict] = []

    for archivo in archivos:
        datos = json.loads(archivo.read_text(encoding='utf-8'))
        clases.extend(datos.get('clases', []))

    por_id = {clase.get('id'): clase for clase in clases}
    esperados = [f'{idioma}.n1.c{n:02d}' for n in range(1, 51)]
    if len(clases) != 50 or len(por_id) != 50:
        raise SystemExit(f'se requieren 50 clases únicas; recibidas {len(clases)} / {len(por_id)} únicas')
    if set(por_id) != set(esperados):
        faltan = sorted(set(esperados) - set(por_id))
        sobran = sorted(set(por_id) - set(esperados))
        raise SystemExit(f'IDs incorrectos; faltan={faltan}, sobran={sobran}')

    campos_congelados = (
        'id', 'bloque', 'titulo', 'objetivo', 'gramatica', 'introduce', 'recicla',
        'vocabulario', 'sonido', 'situacion', 'tarea', 'estado',
    )
    for cid in esperados:
        clase = por_id[cid]
        base = bases[cid]
        distintos = []
        for campo in campos_congelados:
            esperado = 'planificado' if campo == 'estado' else base.get(campo)
            if clase.get(campo) != esperado:
                distintos.append(campo)
        if distintos:
            raise SystemExit(f'{cid}: metadatos distintos del outline: {distintos}')

    consolidado = {clave: valor for clave, valor in outline.items() if clave != 'clases'}
    consolidado['clases'] = [por_id[cid] for cid in esperados]
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(consolidado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{salida}: 50 clases consolidadas')


if __name__ == '__main__':
    main()
