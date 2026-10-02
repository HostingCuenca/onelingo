#!/usr/bin/env python3
"""Integra en la ruta los bloques de francés aprobados (PLAN_CLASES.md).

- Borradores: `nX-bYY.json` (nivel X, bloque YY) con su revisión en GO:
  `revision-nX-bYY.md` (N1 usa el nombre antiguo `revision-bYY.md`).
- Por nivel entran solo bloques en orden y sin huecos (b01, b02…); un nivel
  entra solo si el anterior está completo (10 bloques).
- Encadena prerrequisitos (n1.c01 → fr.f0.se-presenter; cada clase → la
  anterior; nX.c01 → la última clase del nivel anterior) y numera el orden
  global a continuación de Fundamentos. Los autores usan valores provisionales.
- Copia cada bloque a assets/contenido/fr/ruta/ y registra en curso.json el
  nivel `nX` y sus módulos, con títulos del marco (curriculo/marco.json).
  El módulo antiguo `fr.a1-1` sale del curso; su archivo se conserva.
- Termina con `validar_ruta.py fr`.

Uso: python3 tools/contenido/ruta-fr/integrar.py [--hasta N]
     (--hasta N: integra solo hasta el nivel N, aunque haya bloques GO de niveles siguientes)
"""
import json
import pathlib
import re
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
RUTA = RAIZ / 'assets/contenido/fr/ruta'
BLOQUES = 10


def aprobado(nv, b):
    revisiones = [AQUI / f'revision-n{nv}-b{b:02d}.md'] + ([AQUI / f'revision-b{b:02d}.md'] if nv == 1 else [])
    return any(r.exists() and re.search(r'\bGO\b', r.read_text()) for r in revisiones)


def main():
    marco = {n['nivel']: n for n in json.loads((RAIZ / 'curriculo/marco.json').read_text(encoding='utf-8'))['niveles']}
    hasta = int(sys.argv[sys.argv.index('--hasta') + 1]) if '--hasta' in sys.argv else 10
    niveles = []  # (nivel, [(bloque, datos)])
    for nv in range(1, hasta + 1):
        bloques = []
        for b in range(1, BLOQUES + 1):
            fuente = AQUI / f'n{nv}-b{b:02d}.json'
            if not fuente.exists() or not aprobado(nv, b):
                break
            bloques.append((b, json.loads(fuente.read_text(encoding='utf-8'))))
        if not bloques:
            break
        niveles.append((nv, bloques))
        if len(bloques) < BLOQUES:
            break
    if not niveles:
        sys.exit('No hay bloques con revisión GO.')

    anterior = 'fr.f0.se-presenter'
    orden = 1 + max(u['orden'] for u in json.loads((RUTA / 'f0.json').read_text(encoding='utf-8'))['unidades'])
    for nv, bloques in niveles:
        for b, datos in bloques:
            for u in datos['unidades']:
                u['prerequisitos'] = [anterior]
                u['orden'] = orden
                anterior = u['id']
                orden += 1
            datos['modulo'] = f'fr.n{nv}-b{b:02d}'
            (RUTA / f'n{nv}-b{b:02d}.json').write_text(
                json.dumps(datos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    curso_p = RUTA / 'curso.json'
    curso = json.loads(curso_p.read_text(encoding='utf-8'))
    curso['niveles'] = [n for n in curso['niveles'] if n['id'] != 'a1-1']
    curso['modulos'] = [m for m in curso['modulos'] if not re.match(r'fr\.(a1-1|n\d+-b)', m['id'])]
    for nv, bloques in niveles:
        if not any(n['id'] == f'n{nv}' for n in curso['niveles']):
            previo = 'f0' if nv == 1 else f'n{nv - 1}'
            i = next(k for k, n in enumerate(curso['niveles']) if n['id'] == previo) + 1
            curso['niveles'].insert(i, {
                'id': f'n{nv}', 'cefr': marco[nv]['cefr'], 'nivelInterno': nv, 'estado': 'publicado',
                'titulo': {'es': f'Nivel {nv} · {marco[nv]["cefr"]}', 'en': f'Level {nv} · {marco[nv]["cefr"]}'},
            })
        temas = {bl['bloque']: bl['tema'] for bl in marco[nv]['bloques']}
        for b, _ in bloques:
            curso['modulos'].append({
                'id': f'fr.n{nv}-b{b:02d}', 'nivel': f'n{nv}', 'archivo': f'n{nv}-b{b:02d}.json',
                'titulo': temas[b],
            })
    curso_p.write_text(json.dumps(curso, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for nv, bloques in niveles:
        print(f'N{nv}: {len(bloques)} bloque(s), {sum(len(d["unidades"]) for _, d in bloques)} clases integradas')
    sys.exit(subprocess.run([sys.executable, str(RAIZ / 'tools/validar_ruta.py'), 'fr']).returncode)


if __name__ == '__main__':
    main()
