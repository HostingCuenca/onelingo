#!/usr/bin/env python3
"""Integra los bloques de N1 francés aprobados en la ruta (ENCARGO_N1_FR.md).

- Solo entra un bloque con `revision-bXX.md` en GO, en orden y sin huecos (B1, B2…).
- Encadena prerrequisitos: c01 → fr.f0.se-presenter y cada clase → la anterior,
  y numera el orden global a continuación de Fundamentos
  (los autores usan prerrequisitos provisionales para trabajar en paralelo).
- Copia cada bloque a assets/contenido/fr/ruta/n1-bXX.json y registra en
  curso.json el nivel `n1` (A1, nivelInterno 1) con sus módulos. El módulo
  antiguo `fr.a1-1` (Primeras frases, reutilizado en B1–B3) sale del curso;
  su archivo se conserva por trazabilidad.
- Termina con `validar_ruta.py fr`.

Uso: python3 tools/contenido/ruta-fr/integrar.py
"""
import json
import pathlib
import re
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
RUTA = RAIZ / 'assets/contenido/fr/ruta'
# Títulos de los bloques (PLAN_PRODUCCION.md §2).
BLOQUES = {
    1: ('Saludar y presentarse', 'Greetings and introductions'),
    2: ('Hablar de mí', 'Talking about myself'),
    3: ('Personas y cosas', 'People and things'),
    4: ('Preguntar y negar', 'Asking and saying no'),
    5: ('Café y compras', 'Café and shopping'),
    6: ('Gustos y rutina', 'Likes and routine'),
    7: ('Describir y ubicarse', 'Describing and finding your way'),
    8: ('Verbos frecuentes y comida', 'Common verbs and food'),
    9: ('Moverse y planes', 'Getting around and making plans'),
    10: ('Mi fin de semana y cierre', 'My weekend and review'),
}


def main():
    bloques = []
    for n in range(1, 11):
        fuente = AQUI / f'n1-b{n:02d}.json'
        revision = AQUI / f'revision-b{n:02d}.md'
        if not fuente.exists() or not revision.exists() or not re.search(r'\bGO\b', revision.read_text()):
            break
        bloques.append((n, json.loads(fuente.read_text(encoding='utf-8'))))
    if not bloques:
        sys.exit('No hay bloques con revisión GO.')
    anterior = 'fr.f0.se-presenter'
    # El orden global es consecutivo: N1 sigue a Fundamentos.
    orden = 1 + max(u['orden'] for u in json.loads((RUTA / 'f0.json').read_text(encoding='utf-8'))['unidades'])
    for n, datos in bloques:
        for u in datos['unidades']:
            u['prerequisitos'] = [anterior]
            u['orden'] = orden
            anterior = u['id']
            orden += 1
        datos['modulo'] = f'fr.n1-b{n:02d}'
        (RUTA / f'n1-b{n:02d}.json').write_text(
            json.dumps(datos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    curso_p = RUTA / 'curso.json'
    curso = json.loads(curso_p.read_text(encoding='utf-8'))
    curso['niveles'] = [nv for nv in curso['niveles'] if nv['id'] != 'a1-1']
    if not any(nv['id'] == 'n1' for nv in curso['niveles']):
        i = next(k for k, nv in enumerate(curso['niveles']) if nv['id'] == 'f0') + 1
        curso['niveles'].insert(i, {
            'id': 'n1', 'cefr': 'A1', 'nivelInterno': 1, 'estado': 'publicado',
            'titulo': {'es': 'Nivel 1 · A1', 'en': 'Level 1 · A1'},
        })
    curso['modulos'] = [m for m in curso['modulos'] if not m['id'].startswith(('fr.a1-1', 'fr.n1-b'))]
    for n, _ in bloques:
        curso['modulos'].append({
            'id': f'fr.n1-b{n:02d}', 'nivel': 'n1', 'archivo': f'n1-b{n:02d}.json',
            'titulo': {'es': BLOQUES[n][0], 'en': BLOQUES[n][1]},
        })
    curso_p.write_text(json.dumps(curso, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'N1: {len(bloques)} bloque(s), {sum(len(d["unidades"]) for _, d in bloques)} clases integradas')
    sys.exit(subprocess.run([sys.executable, str(RAIZ / 'tools/validar_ruta.py'), 'fr']).returncode)


if __name__ == '__main__':
    main()
