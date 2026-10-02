#!/usr/bin/env python3
"""Integra los lotes revisados en la fuente única de situaciones.

Solo entra un lote cuyo `revision-N.md` dice GO y que pasa el validador.
Escribe assets/contenido/en/situaciones.json y regenera las copias.

Uso: python3 tools/contenido/situaciones/integrar_lotes.py [idioma]
     (en: lotes en borrador/; otros idiomas: lotes en <idioma>/)
"""
import json
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
IDIOMA = sys.argv[1] if len(sys.argv) > 1 else 'en'
BORRADOR = RAIZ / 'tools/contenido/situaciones' / ('borrador' if IDIOMA == 'en' else IDIOMA)
DESTINO = RAIZ / f'assets/contenido/{IDIOMA}/situaciones.json'
sys.path.insert(0, str(RAIZ / 'tools/contenido'))
from validar_situaciones import validar  # noqa: E402


def main():
    situaciones = []
    for n in range(1, 6):
        lote = BORRADOR / f'lote-{n}.json'
        revision = BORRADOR / f'revision-{n}.md'
        if not revision.exists() or not re.search(r'\bGO\b', revision.read_text()):
            sys.exit(f'lote-{n}: sin revisión GO')
        datos = json.loads(lote.read_text(encoding='utf-8'))
        errores = validar(datos)
        if errores:
            sys.exit(f'lote-{n}: {len(errores)} errores ({errores[0]})')
        situaciones += datos
    situaciones.sort(key=lambda s: s['id'])
    assert [s['id'] for s in situaciones] == list(range(1, 51))
    DESTINO.write_text(
        json.dumps(
            {
                'version': '2026.10.01',
                'idioma': IDIOMA,
                'situaciones': [
                    {'id': s['id'], 'tramos': s['tramos']} for s in situaciones
                ],
            },
            ensure_ascii=False,
            indent=1,
        )
        + '\n',
        encoding='utf-8',
    )
    print('Escrito', DESTINO.relative_to(RAIZ))
    subprocess.run(
        [sys.executable, str(RAIZ / 'tools/contenido/generar_situaciones.py')],
        check=True,
    )


if __name__ == '__main__':
    main()
