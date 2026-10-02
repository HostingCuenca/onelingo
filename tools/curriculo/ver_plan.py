#!/usr/bin/env python3
"""Genera la vista legible del plan de clases (no se edita a mano).

Uso: python3 tools/curriculo/ver_plan.py fr
     → docs/claude-educacion/plan/marco.md y docs/claude-educacion/plan/fr.md
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CURRICULO = RAIZ / 'curriculo'
SALIDA = RAIZ / 'docs/claude-educacion/plan'
AVISO = '<!-- Generado con tools/curriculo/ver_plan.py desde curriculo/. No editar a mano. -->\n\n'
ICONO = {'planificado': '·', 'escrito': '✎', 'revisado': '✓', 'publicado': '●'}


def situaciones():
    c = json.loads((RAIZ / 'assets/contenido/situaciones/catalogo.json').read_text(encoding='utf-8'))
    return {s['id']: s['nombre'] for s in c['situaciones']}


def marco_md(marco, sit):
    out = [AVISO, '# Marco común: 10 niveles × 10 bloques\n']
    for n in marco['niveles']:
        out.append(f"\n## N{n['nivel']} · {n['cefr']} · {n['titulo']['es']}\n\n{n['objetivo']['es']}\n")
        out.append('\n| Bloque | Tema | Objetivo | Situaciones |\n|---|---|---|---|\n')
        for b in n['bloques']:
            s = ', '.join(f"{i} {sit.get(i, '?')}" for i in b['situaciones'])
            out.append(f"| {b['bloque']} | {b['tema']['es']} | {b['objetivo']['es']} | {s} |\n")
    return ''.join(out)


def idioma_md(idioma, marco, sit):
    out = [AVISO, f'# Plan de clases · {idioma}\n\n',
           'Estado: · planificado · ✎ escrito · ✓ revisado · ● publicado. Fuente: `curriculo/', idioma, '/nX.json`.\n']
    temas = {(n['nivel'], b['bloque']): b['tema']['es'] for n in marco['niveles'] for b in n['bloques']}
    for nv in range(1, 11):
        p = CURRICULO / idioma / f'n{nv}.json'
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding='utf-8'))
        out.append(f"\n## N{nv} · {d['cefr']}" + (f" · {d['examen']}" if d.get('examen') else '') + '\n')
        bloque = None
        for c in d['clases']:
            if c['bloque'] != bloque:
                bloque = c['bloque']
                out.append(f"\n### Bloque {bloque} · {temas.get((nv, bloque), '')}\n\n"
                           '| | Clase | Objetivo | Gramática | Situación |\n|---|---|---|---|---|\n')
            num = c['id'].rsplit('.c', 1)[1]
            g = '; '.join(c['gramatica'])
            out.append(f"| {ICONO.get(c['estado'], '?')} | {num} {c['titulo']['es']} | {c['objetivo']['es']} | {g} | "
                       f"{sit.get(c['situacion'], '?')} |\n")
    return ''.join(out)


def main():
    marco = json.loads((CURRICULO / 'marco.json').read_text(encoding='utf-8'))
    sit = situaciones()
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / 'marco.md').write_text(marco_md(marco, sit), encoding='utf-8')
    for idioma in sys.argv[1:]:
        (SALIDA / f'{idioma}.md').write_text(idioma_md(idioma, marco, sit), encoding='utf-8')
    print('plan →', SALIDA.relative_to(RAIZ))


if __name__ == '__main__':
    main()
