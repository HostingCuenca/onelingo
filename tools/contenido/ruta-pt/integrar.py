#!/usr/bin/env python3
"""Integra en la ruta el portugués aprobado (PLAN_PORTUGUES.md, DEC-035).

Portugués de Brasil (pt-BR) para hispanohablantes; apoyo bilingüe {es, en}
como el francés.

- Fundamentos: `borrador-f0.json` entra si `revision-f0.md` declara GO en la
  línea de estado y `validar.py` (contraste con curriculo/pt/f0.json) pasa.
  Se copia a assets/contenido/pt/ruta/f0.json.
- curso.json: si no existe se crea con Fundamentos y C2 planificado; si existe
  se conservan sus metadatos y se rehacen los niveles nX y sus módulos.
- Niveles (cuando existan): borradores `nX-bYY.json` con `revision-nX-bYY.md`
  en GO (primera línea). Por nivel entran solo bloques en orden y sin huecos;
  un nivel entra solo si el anterior está completo (10 bloques). Encadena
  prerrequisitos (n1 → pt.f0.apresentar-se; cada clase → la anterior) y
  numera el orden global a continuación de Fundamentos, con títulos del marco
  (curriculo/marco.json).
- Termina con `validar_ruta.py pt`.

Uso: python3 tools/contenido/ruta-pt/integrar.py [--hasta N]
     (--hasta N: integra solo hasta el nivel N; --hasta 0 deja solo Fundamentos)
"""
import json
import pathlib
import re
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
RUTA = RAIZ / 'assets/contenido/pt/ruta'
BLOQUES = 10
ULTIMA_F0 = 'pt.f0.apresentar-se'
NOMBRES_LIBRES = [
    'Ana',
    'Beatriz',
    'Bia',
    'Beto',
    'Caio',
    'Costa',
    'Eva',
    'Ivo',
    'Lara',
    'Leo',
    'Lia',
    'Lima',
    'Luis',
    'Marta',
    'Paula',
    'Paulo',
    'Pedro',
    'Roberto',
    'Rui',
    'Silva',
    'Camila',
    'Ortega',
    'Marina',
    'Lins',
    'Lucas',
    'Beltrão',
    'Bruno',
    'Cavalcanti',
    'Santos',
    'Barros',
    'Gomes',
    'Renata',
    'Souza',
    'Frevo',
    'Alberto',
    'Helena',
    'Iara',
    'Menezes',
    'Diego',
    'Yasmin',
    'Tomás',
    'Larissa',
    'Davi',
    'Gloria',
    'Jaime',
    'Valeria',
    'Neide',
    'Maré',
    'Digital',
    'Travessia',
    'Recife',
    'Boa',
    'Viagem',
    'Graças',
    'Olinda',
    'Miami',
    'Medellín',
    'Pernambuco',
    'Capibaribe',
    'Noronha',
    'Caruaru',
    'Lisboa',
    'Rafael',
    'Luana',
    'Carolina',
    'Marco',
    'João',
    'Luiz',
    'Júlia',
    'Joana',
    'Valentina',
    'Lúcia',
    'Otávio',
    'Fernando',
    'Clarice',
    'Farias',
    'Duarte',
    'Nogueira',
    'Carla',
    'José',
    'Henrique',
    'Bandeira',
    'Lispector',
    'Rita',
    'Rocha',
    'Moura',
    'Prado',
    'Lopes',
    'Rodrigo',
    'Clara',
    'Michele',
    'Maurício',
    'Cecília',
    'Felipe',
    'Dias',
    'Manuel',
    'Severino',
    'Almeida',
    'Marcos',
    'Patrícia',
    'Cabral',
    'Letícia',
    'Aguirre',
    'Pereira',
    'Elisa',
    'Nina',
    'Tavares',
    'Salazar',
    'Kendall',
    'Sofia',
    'Nara',
    'Igor',
    'Mia',
    'Marie',
    'Rosa',
    'Bogotá',
    'Galinhas',
    'Salvador',
    'Nassau',
    'Porto',
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
        'esquema': 2, 'idioma': 'pt', 'version': '2026.10.0', 'revision': 'inicial',
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
            {'id': 'pt.f0', 'nivel': 'f0', 'archivo': 'f0.json',
             'titulo': {'es': 'Fundamentos: tus primeras frases en portugués',
                        'en': 'Foundations: your first sentences in Portuguese'}},
        ],
    }


def main():
    if not f0_aprobado():
        sys.exit('revision-f0.md no está en GO.')
    if subprocess.run([sys.executable, str(AQUI / 'validar.py')]).returncode:
        sys.exit('validar.py falla: no se integra.')
    RUTA.mkdir(parents=True, exist_ok=True)
    f0 = json.loads((AQUI / 'borrador-f0.json').read_text(encoding='utf-8'))
    escribir(RUTA / 'f0.json', f0)

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

    anterior = ULTIMA_F0
    orden = 1 + max(u['orden'] for u in f0['unidades'])
    for nv, bloques in niveles:
        for b, datos in bloques:
            for u in datos['unidades']:
                u['prerequisitos'] = [anterior]
                u['orden'] = orden
                anterior = u['id']
                orden += 1
            datos['modulo'] = f'pt.n{nv}-b{b:02d}'
            escribir(RUTA / f'n{nv}-b{b:02d}.json', datos)

    curso_p = RUTA / 'curso.json'
    curso = json.loads(curso_p.read_text(encoding='utf-8')) if curso_p.exists() else curso_base()
    curso['niveles'] = [n for n in curso['niveles'] if not re.fullmatch(r'n\d+', n['id'])]
    curso['modulos'] = [m for m in curso['modulos'] if not re.match(r'pt\.n\d+-b', m['id'])]
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
                'id': f'pt.n{nv}-b{b:02d}', 'nivel': f'n{nv}', 'archivo': f'n{nv}-b{b:02d}.json',
                'titulo': temas[b],
            })
    escribir(curso_p, curso)
    print(f'F0: {len(f0["unidades"])} unidades integradas')
    for nv, bloques in niveles:
        print(f'N{nv}: {len(bloques)} bloque(s), {sum(len(d["unidades"]) for _, d in bloques)} clases integradas')
    sys.exit(subprocess.run([sys.executable, str(RAIZ / 'tools/validar_ruta.py'), 'pt']).returncode)


if __name__ == '__main__':
    main()
