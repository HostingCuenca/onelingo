#!/usr/bin/env python3
"""Integra en la ruta el alemán aprobado (PLAN_ALEMAN.md §7.5, método ligero).

Alemán estándar de Alemania para hispanohablantes; apoyo bilingüe {es, en}.
Copia adaptada de ruta-pt/integrar.py SIN reparto ni canon: los nombres de las
clases son genéricos y no se arrastran de una clase a otra.

- Fundamentos: si existen `borrador-f0.json` y `revision-f0.md` con GO en la
  línea «Estado:», se copia a assets/contenido/de/ruta/f0.json (y antes pasa
  `validar.py` de esta carpeta, si existe). Si no, se conserva el f0 publicado.
- Niveles: borradores `nX-bYY.json` con `revision-nX-bYY.md` en GO (primera
  línea). Por nivel entran solo bloques en orden y sin huecos; un nivel entra
  solo si el anterior está completo (10 bloques). Encadena prerrequisitos
  (n1 → de.f0.vorstellen; cada clase → la anterior) y numera el orden global a
  continuación de lo ya publicado, con títulos del marco (curriculo/marco.json).
- curso.json: se conservan sus metadatos y se rehacen los niveles nX y sus
  módulos. Al integrar N1 se fijan idiomasApoyo [es, en], vocabularioEstricto,
  reglasAutoria y palabrasLibres (unión con NOMBRES_LIBRES, sin Ecuador). Con
  N1 completo (10 bloques) se retira el módulo heredado de.a1-1 (el archivo
  queda en disco; no hay progreso que mapear: el alemán no tenía ruta activa
  en la app hasta publicarse N1–N10).
- Sin bloques aprobados no escribe nada. Termina con `validar_ruta.py de`.

Uso: python3 tools/contenido/ruta-de/integrar.py [--hasta N] [--seco]
     --hasta N: integra solo hasta el nivel N
     --seco:    muestra qué integraría, sin escribir ni validar
"""
import json
import pathlib
import re
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
IDIOMA = 'de'
RUTA = RAIZ / f'assets/contenido/{IDIOMA}/ruta'
BLOQUES = 10
ULTIMA_F0 = 'de.f0.vorstellen'
HEREDADOS = ['de.a1-1']  # módulos legados que se retiran con N1 completo
PROHIBIDAS = {'Quito', 'Ecuador', 'Guayaquil', 'Cuenca'}
# Banco de nombres genéricos (sin reparto) y ciudades grandes sin datos verificables.
# Se evitan apellidos que son palabras alemanas corrientes (Klein, Lang, Koch…).
NOMBRES_LIBRES = [
    # nombres de pila
    'Anna', 'Jonas', 'Lena', 'Paul', 'Mia', 'Felix', 'Sophie', 'Lukas', 'Lea', 'Tim',
    'Lisa', 'Tom', 'Sara', 'Ben', 'Laura', 'Max', 'Julia', 'David', 'Nina', 'Jan',
    'Emma', 'Leon', 'Clara', 'Niklas', 'Hannah', 'Moritz', 'Ana', 'Leo', 'Carlos',
    'Lucía', 'Diego', 'Carmen', 'Paula', 'Sofía', 'Carla', 'Andrés', 'Valentina',
    # apellidos
    'Becker', 'Berger', 'Wolf', 'Müller', 'Schmidt', 'Schulz', 'Weber', 'Meyer',
    'Wagner', 'Fischer', 'Hoffmann', 'Neumann', 'Keller', 'Krüger', 'Hartmann',
    'Ruiz', 'García', 'López',
    # ciudades
    'Berlin', 'Hamburg', 'München', 'Köln', 'Leipzig', 'Frankfurt', 'Dresden',
    'Stuttgart', 'Wien', 'Zürich',
    # ampliación 06-10 (nombres, apellidos y ciudades frecuentes en los bloques)
    'Peter', 'Eva', 'Kai', 'Lara', 'Jakob', 'Marie', 'Elias', 'Tobias', 'Katrin', 'Simon', 'Johanna', 'Philipp', 'Greta', 'Martin', 'Sabine', 'Thomas', 'Andrea', 'Stefan', 'Ines', 'Oliver', 'Bauer', 'Richter', 'Klein', 'Schröder', 'Lange', 'Vogel', 'Braun', 'Zimmermann', 'Krause', 'Lehmann', 'Schneider', 'Koch', 'Sommer', 'Roth', 'Frank', 'Seidel', 'Lang', 'Kurz', 'Brandt', 'Fuchs', 'Nürnberg', 'Bremen', 'Hannover', 'Düsseldorf', 'Bonn', 'Graz', 'Salzburg', 'Innsbruck', 'Bern', 'Basel', 'Heidelberg', 'Freiburg', 'Mainz', 'Kiel', 'Rostock', 'Potsdam', 'Deutschland', 'Österreich', 'Schweiz',
    # ampliación 06-10 (2): apellidos ya usados en bloques aprobados
    'Albers', 'Albrecht', 'Behr', 'Berg', 'Dietz', 'Engel', 'Ernst', 'Haas', 'Hahn', 'Hanna', 'Kern', 'Kraft', 'Krämer', 'Kunz', 'Lenz', 'Lindner', 'Lorenz', 'Lutz', 'Maier', 'Maurer', 'Mayer', 'Moll', 'Möller', 'Peters', 'Pohl', 'Rau', 'Sander', 'Schmitt', 'Scholz', 'Voigt', 'Voss', 'Weiß', 'Winter', 'Yilmaz',
    # interjección heredada
    'Oh',
]


def escribir(p, datos):
    p.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def f0_aprobado():
    r = AQUI / 'revision-f0.md'
    estado = next((l for l in r.read_text(encoding='utf-8').splitlines() if l.startswith('Estado:')), '') \
        if r.exists() else ''
    return re.search(r'\bGO\b', estado) is not None and 'NO-GO' not in estado


def aprobado(nv, b):
    r = AQUI / f'revision-n{nv}-b{b:02d}.md'
    return r.exists() and re.search(r'\bGO\b', r.read_text(encoding='utf-8').split('\n', 1)[0]) is not None


def curso_base():
    return {
        'esquema': 2, 'idioma': IDIOMA, 'version': '2026.10.0', 'revision': 'inicial',
        'idiomasApoyo': ['es', 'en'], 'apoyoPredeterminado': 'es',
        'vocabularioEstricto': True, 'reglasAutoria': True,
        'palabrasLibres': NOMBRES_LIBRES,
        'niveles': [
            {'id': 'f0', 'cefr': 'Pre-A1', 'nivelInterno': 0, 'estado': 'publicado',
             'titulo': {'es': 'Fundamentos', 'en': 'Foundations'}},
            {'id': 'c2', 'cefr': 'C2', 'nivelInterno': None, 'estado': 'planificado',
             'titulo': {'es': 'C2 · Maestría', 'en': 'C2 · Mastery'}},
        ],
        'modulos': [
            {'id': 'de.f0', 'nivel': 'f0', 'archivo': 'f0.json',
             'titulo': {'es': 'Fundamentos: tus primeras frases en alemán',
                        'en': 'Foundations: your first sentences in German'}},
        ],
    }


def main():
    seco = '--seco' in sys.argv
    hasta = int(sys.argv[sys.argv.index('--hasta') + 1]) if '--hasta' in sys.argv else 10

    f0_nuevo = (AQUI / 'borrador-f0.json').exists() and f0_aprobado()
    if f0_nuevo and (AQUI / 'validar.py').exists() and not seco:
        if subprocess.run([sys.executable, str(AQUI / 'validar.py')]).returncode:
            sys.exit('validar.py falla: no se integra.')
    f0_p = AQUI / 'borrador-f0.json' if f0_nuevo else RUTA / 'f0.json'
    f0 = json.loads(f0_p.read_text(encoding='utf-8'))

    marco = {n['nivel']: n for n in json.loads((RAIZ / 'curriculo/marco.json').read_text(encoding='utf-8'))['niveles']}
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

    print(f'F0: {"borrador aprobado" if f0_nuevo else "se conserva el publicado"} ({len(f0["unidades"])} unidades)')
    for nv, bloques in niveles:
        print(f'N{nv}: {len(bloques)} bloque(s), {sum(len(d["unidades"]) for _, d in bloques)} clases aprobadas')
    if not niveles and not f0_nuevo:
        print('Sin bloques aprobados (nX-bYY.json + revision-nX-bYY.md en GO): nada que integrar.')
        return
    n1_completo = any(nv == 1 and len(bl) == BLOQUES for nv, bl in niveles)
    if seco:
        print('[seco] no se escribe nada.' + (f' Se retirarían: {", ".join(HEREDADOS)}.' if n1_completo else ''))
        return

    RUTA.mkdir(parents=True, exist_ok=True)
    if f0_nuevo:
        escribir(RUTA / 'f0.json', f0)

    curso_p = RUTA / 'curso.json'
    curso = json.loads(curso_p.read_text(encoding='utf-8')) if curso_p.exists() else curso_base()
    if n1_completo:
        retirar = set(HEREDADOS)
        niveles_retirados = {m['nivel'] for m in curso['modulos'] if m['id'] in retirar}
        curso['modulos'] = [m for m in curso['modulos'] if m['id'] not in retirar]
        curso['niveles'] = [n for n in curso['niveles'] if n['id'] not in niveles_retirados]
    # El orden global sigue a todo lo publicado que no es nX (f0 y, mientras exista, el legado).
    orden = 1 + max(u['orden'] for u in f0['unidades'])
    for m in curso['modulos']:
        if m['id'] != 'de.f0' and not re.match(rf'{IDIOMA}\.n\d+-b', m['id']) and (RUTA / m['archivo']).exists():
            orden = max(orden, 1 + max(u['orden'] for u in json.loads((RUTA / m['archivo']).read_text(encoding='utf-8'))['unidades']))

    anterior = ULTIMA_F0
    for nv, bloques in niveles:
        for b, datos in bloques:
            for u in datos['unidades']:
                u['prerequisitos'] = [anterior]
                u['orden'] = orden
                anterior = u['id']
                orden += 1
            datos['modulo'] = f'{IDIOMA}.n{nv}-b{b:02d}'
            escribir(RUTA / f'n{nv}-b{b:02d}.json', datos)

    if niveles:
        curso['idiomasApoyo'] = ['es', 'en']
        curso['vocabularioEstricto'] = True
        curso['reglasAutoria'] = True
        libres = [p for p in curso.get('palabrasLibres', []) if p not in PROHIBIDAS]
        curso['palabrasLibres'] = libres + [p for p in NOMBRES_LIBRES if p not in libres]
    curso['niveles'] = [n for n in curso['niveles'] if not re.fullmatch(r'n\d+', n['id'])]
    curso['modulos'] = [m for m in curso['modulos'] if not re.match(rf'{IDIOMA}\.n\d+-b', m['id'])]
    for nv, bloques in niveles:
        previo = 'f0' if nv == 1 else f'n{nv - 1}'
        i = next(k for k, n in enumerate(curso['niveles']) if n['id'] == previo) + 1
        curso['niveles'].insert(i, {
            'id': f'n{nv}', 'cefr': marco[nv]['cefr'], 'nivelInterno': nv, 'estado': 'publicado',
            'titulo': {'es': f'Nivel {nv} · {marco[nv]["cefr"]}', 'en': f'Level {nv} · {marco[nv]["cefr"]}'},
        })
        temas = {bl['bloque']: bl['tema'] for bl in marco[nv]['bloques']}
        for b, _ in bloques:
            curso['modulos'].append({
                'id': f'{IDIOMA}.n{nv}-b{b:02d}', 'nivel': f'n{nv}', 'archivo': f'n{nv}-b{b:02d}.json',
                'titulo': temas[b],
            })
    escribir(curso_p, curso)
    for nv, bloques in niveles:
        print(f'N{nv}: {len(bloques)} bloque(s) integrados')
    if n1_completo:
        print(f'Retirados de curso.json: {", ".join(HEREDADOS)}')
    sys.exit(subprocess.run([sys.executable, str(RAIZ / 'tools/validar_ruta.py'), IDIOMA]).returncode)


if __name__ == '__main__':
    main()
