#!/usr/bin/env python3
"""Expande la fuente de verbos a las tablas de conjugación de la app.

Fuente:   tools/contenido/verbos/verbos-<idioma>.json (revisada, ver LEEME.md)
Generado: assets/contenido/<idioma>/verbos.json (no editar a mano)

El nivel de cada verbo es el primero en que la ruta lo enseña (pasos de
vocabulario); si la ruta no lo enseña, el nivel en que suele aparecer
(regulares 1, irregulares frecuentes 1–2), marcado con `enRuta: false`.

Uso: python3 tools/contenido/verbos/generar_verbos.py [--comprobar]
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]

PERSONAS_EN = [
    {'en': 'I', 'es': 'yo'},
    {'en': 'you', 'es': 'tú'},
    {'en': 'he / she / it', 'es': 'él / ella'},
    {'en': 'we', 'es': 'nosotros'},
    {'en': 'you', 'es': 'ustedes'},
    {'en': 'they', 'es': 'ellos'},
]
TIEMPOS_EN = [
    {'id': 'presente', 'nombre': 'Presente simple', 'uso': 'Hábitos y cosas que siempre son así.'},
    {'id': 'pasado', 'nombre': 'Pasado simple', 'uso': 'Algo terminado en el pasado (yesterday, last week).'},
    {'id': 'futuro', 'nombre': 'Futuro con will', 'uso': 'Decisiones del momento, promesas y predicciones.'},
    {'id': 'perfecto', 'nombre': 'Presente perfecto', 'uso': 'Experiencias y cosas que siguen hasta hoy.'},
    {'id': 'continuo', 'nombre': 'Presente continuo', 'uso': 'Lo que está pasando ahora.'},
]
BE = {
    'presente': ['am', 'are', 'is', 'are', 'are', 'are'],
    'pasado': ['was', 'were', 'was', 'were', 'were', 'were'],
}
AUX_CONTINUO = ['am', 'are', 'is', 'are', 'are', 'are']


def tablas_en(v):
    inf = v['infinitivo']
    t = {
        'presente': BE['presente'] if inf == 'be'
        else [inf, inf, v['tercera'], inf, inf, inf],
        'pasado': BE['pasado'] if inf == 'be' else [v['pasado']] * 6,
        'futuro': [f'will {inf}'] * 6,
        'perfecto': [
            ('has ' if i == 2 else 'have ') + v['participio'] for i in range(6)
        ],
        'continuo': [f'{a} {v["gerundio"]}' for a in AUX_CONTINUO],
    }
    return t


def niveles_en_ruta(idioma):
    """Primer nivel interno en que la ruta enseña cada palabra."""
    base = RAIZ / f'assets/contenido/{idioma}/ruta'
    curso = json.loads((base / 'curso.json').read_text(encoding='utf-8'))
    publicados = {
        n['id']: n.get('nivelInterno')
        for n in curso['niveles']
        if n.get('estado') == 'publicado'
    }
    res = {}
    for m in curso['modulos']:
        if m['nivel'] not in publicados or publicados[m['nivel']] is None:
            continue
        datos = json.loads((base / m['archivo']).read_text(encoding='utf-8'))
        for u in datos['unidades']:
            nivel = u.get('nivelInterno', publicados[m['nivel']])
            vocab = {v['id']: v['texto'] for v in u.get('vocabulario', [])}
            for p in u.get('pasos', []):
                if p.get('tipo') != 'vocabulario':
                    continue
                for ref in p.get('refs', []):
                    texto = re.sub(r'^to ', '', vocab.get(ref, '').strip().lower())
                    if texto and (texto not in res or nivel < res[texto]):
                        res[texto] = nivel
    return res


def validar(verbos):
    errores = []
    vistos = set()
    for v in verbos:
        inf = v.get('infinitivo', '')
        if inf in vistos:
            errores.append(f'{inf}: repetido')
        vistos.add(inf)
        for k in ('es', 'tipo', 'tercera', 'pasado', 'participio', 'gerundio'):
            if not str(v.get(k, '')).strip():
                errores.append(f'{inf}: falta {k}')
        if v.get('tipo') == 'regular' and not (
            v.get('pasado') == v.get('participio') and str(v.get('pasado')).endswith('ed')
        ):
            errores.append(f'{inf}: regular con formas irregulares')
        ej = v.get('ejemplo') or {}
        if not ej.get('en') or not ej.get('es'):
            errores.append(f'{inf}: sin ejemplo')
    return errores


def generar(idioma):
    fuente = RAIZ / f'tools/contenido/verbos/verbos-{idioma}.json'
    verbos = json.loads(fuente.read_text(encoding='utf-8'))
    errores = validar(verbos)
    if errores:
        sys.exit('\n'.join(f'ERROR {e}' for e in errores))
    niveles = niveles_en_ruta(idioma)
    salida = []
    for v in sorted(verbos, key=lambda x: x['infinitivo']):
        inf = v['infinitivo']
        en_ruta = inf in niveles
        salida.append({
            'id': inf,
            'infinitivo': inf,
            'es': v['es'],
            'tipo': v['tipo'],
            'nivel': niveles.get(inf, 1),
            'enRuta': en_ruta,
            'formas': {k: v[k] for k in ('tercera', 'pasado', 'participio', 'gerundio')},
            'tablas': tablas_en(v),
            'ejemplo': v['ejemplo'],
        })
    return json.dumps({
        'version': '2026.10.01',
        'idioma': idioma,
        'personas': PERSONAS_EN,
        'tiempos': TIEMPOS_EN,
        'verbos': salida,
    }, ensure_ascii=False, indent=1) + '\n'


def main():
    destino = RAIZ / 'assets/contenido/en/verbos.json'
    texto = generar('en')
    if '--comprobar' in sys.argv:
        actual = destino.read_text(encoding='utf-8') if destino.exists() else ''
        if actual != texto:
            sys.exit('verbos.json desactualizado: ejecuta generar_verbos.py')
        print('Todo al día.')
        return
    destino.write_text(texto, encoding='utf-8')
    datos = json.loads(texto)
    en_ruta = sum(1 for v in datos['verbos'] if v['enRuta'])
    print(f"{len(datos['verbos'])} verbos ({en_ruta} enseñados en la ruta) → {destino.relative_to(RAIZ)}")


if __name__ == '__main__':
    main()
