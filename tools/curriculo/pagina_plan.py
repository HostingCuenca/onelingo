#!/usr/bin/env python3
"""Genera la página de revisión del plan de un idioma (marco + fichas + lo
publicado) para revisarla y aprobarla nivel a nivel.

Uso: python3 tools/curriculo/pagina_plan.py fr salida.html
Los datos van embebidos; las aprobaciones y notas viven en la base del
artifact (colección «revision»), no en el archivo.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ES = lambda v: (v.get('es') if isinstance(v, dict) else v) or ''  # noqa: E731


def celda(c):
    if isinstance(c, dict):
        return c.get('texto') or ES(c.get('apoyo')) or ES(c)
    return str(c)


ETAPA = {'practica_guiada': 'guiada', 'practica_independiente': 'independiente', 'situacion': 'situacion',
         'evaluacion': 'evaluacion'}


def item_real(i):
    """Un ejercicio publicado como lo ve el alumno: consigna, enunciado y respuesta."""
    ops = i.get('opciones') or []
    resp = i.get('respuesta')
    if isinstance(resp, int) and 0 <= resp < len(ops):
        resp = ops[resp]
    if i.get('pares'):
        resp = ' · '.join(f'{a} = {celda(b)}' for a, b in (p for p in i['pares'] if isinstance(p, list) and len(p) == 2))
    enunciado = i.get('texto') or i.get('audio') or ES(i.get('preguntaApoyo')) or ES(i.get('pregunta')) or ''
    if i.get('tokens') and not enunciado:
        enunciado = ' / '.join(i['tokens'])
    return {'formato': i.get('formato', ''), 'consigna': ES(i.get('consigna')), 'enunciado': enunciado,
            'opciones': [celda(o) for o in ops], 'respuesta': celda(resp) if resp is not None else '',
            'abierta': bool(i.get('abierta'))}


def resumen_unidad(u):
    """Lo que el revisor necesita ver de una clase publicada (en español)."""
    r = {'explicaciones': [], 'tablas': [], 'ejemplos': [], 'vocabulario': [], 'situacion': None,
         'practica': 0, 'evaluacion': 0, 'formatos': [], 'ejercicios': {}}
    formatos = set()
    for v in u.get('vocabulario', []):
        r['vocabulario'].append([v.get('texto', ''), ES(v.get('traduccion'))])
    for p in u.get('pasos', []):
        t = p.get('tipo')
        if t == 'explicacion':
            r['explicaciones'].append([ES(p.get('titulo')), ES(p.get('texto'))])
        elif t in ('tabla', 'patron'):
            filas = [[celda(c) for c in (f if isinstance(f, list) else f.get('celdas', []))] for f in p.get('filas', [])]
            r['tablas'].append({'titulo': ES(p.get('titulo')), 'columnas': [celda(c) for c in p.get('columnas', [])],
                                'filas': filas})
        elif t == 'ejemplos':
            r['ejemplos'] += [[i.get('texto', ''), ES(i.get('traduccion'))] for i in p.get('items', [])]
        elif t == 'situacion':
            r['situacion'] = {'contexto': ES(p.get('contexto')),
                              'dialogo': [[l.get('hablante', ''), l.get('texto', ''), ES(l.get('traduccion'))]
                                          for l in p.get('dialogo', [])]}
        if t in ETAPA and isinstance(p.get('items'), list):
            r['ejercicios'].setdefault(ETAPA[t], []).extend(item_real(i) for i in p['items'] if isinstance(i, dict))
        if t in ('practica_guiada', 'practica_independiente'):
            r['practica'] += len(p.get('items', []))
        if t == 'evaluacion':
            r['evaluacion'] = len(p.get('items', []))
        for i in p.get('items', []) if isinstance(p.get('items'), list) else []:
            if isinstance(i, dict) and i.get('formato'):
                formatos.add(i['formato'])
    r['formatos'] = sorted(formatos)
    r['errores'] = [[e.get('incorrecto', ''), e.get('correcto', ''), ES(e.get('explicacion'))]
                    for e in u.get('erroresFrecuentes', [])]
    return r


def main():
    idioma, salida = sys.argv[1], Path(sys.argv[2])
    marco = json.loads((RAIZ / 'curriculo/marco.json').read_text(encoding='utf-8'))
    sit = {s['id']: s['nombre'] for s in json.loads(
        (RAIZ / 'assets/contenido/situaciones/catalogo.json').read_text(encoding='utf-8'))['situaciones']}
    ruta = RAIZ / f'assets/contenido/{idioma}/ruta'
    unidades = {}
    for f in ruta.glob('*.json'):
        d = json.loads(f.read_text(encoding='utf-8'))
        for u in d.get('unidades', []) if isinstance(d, dict) else []:
            unidades[u['id']] = u
    niveles = []
    for n in marco['niveles']:
        p = RAIZ / f'curriculo/{idioma}/n{n["nivel"]}.json'
        plan = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        clases = []
        for c in plan.get('clases', []):
            u = unidades.get(c['id'])
            clases.append({
                'id': c['id'], 'bloque': c['bloque'], 'titulo': ES(c['titulo']), 'objetivo': ES(c['objetivo']),
                'gramatica': c.get('gramatica', []), 'introduce': c.get('introduce', []),
                'recicla': c.get('recicla', []), 'campo': ES(c.get('vocabulario', {}).get('campo')),
                'palabras': c.get('vocabulario', {}).get('palabras', []), 'sonido': c.get('sonido', ''),
                'situacion': sit.get(c.get('situacion'), ''), 'tarea': ES(c.get('tarea')), 'estado': c.get('estado'),
                'ejercicios': c.get('ejercicios'),
                'contenido': resumen_unidad(u) if u else None,
            })
        niveles.append({
            'nivel': n['nivel'], 'cefr': n['cefr'], 'titulo': ES(n['titulo']), 'objetivo': ES(n['objetivo']),
            'examen': plan.get('examen', ''), 'nota': ES(plan.get('nota')),
            'bloques': [{'bloque': b['bloque'], 'tema': ES(b['tema']), 'objetivo': ES(b['objetivo']),
                         'tipo': b['tipo'], 'situaciones': [sit.get(s, '') for s in b['situaciones']]}
                        for b in n['bloques']],
            'clases': clases,
            'hechos': [ES(h) for h in plan.get('hechosDelReparto', [])],
        })
    n1 = json.loads((RAIZ / f'curriculo/{idioma}/n1.json').read_text(encoding='utf-8'))
    personajes = [{'nombre': p.get('nombre', '') + (f" {p['apellido']}" if p.get('apellido') and p['apellido'] not in p.get('nombre', '') else ''),
                   'edad': p.get('edad'), 'nacionalidad': p.get('nacionalidad', ''), 'ciudad': p.get('ciudad', ''),
                   'ocupacion': ES(p.get('ocupacion')), 'familia': ES(p.get('familia'))}
                  for p in n1.get('personajes', [])]
    antes = {}
    n0 = RAIZ / f'assets/contenido/{idioma}/nivel0/nivel0.json'
    if n0.exists():
        d = json.loads(n0.read_text(encoding='utf-8'))
        antes['nivel0'] = [[ES(u.get('titulo')), [ES(l.get('titulo')) for l in u.get('lecciones', [])]]
                           for u in d.get('unidades', [])]
    f0 = ruta / 'f0.json'
    if f0.exists():
        antes['f0'] = [ES(u.get('titulo')) for u in json.loads(f0.read_text(encoding='utf-8'))['unidades']]
    extra = {}
    for nombre, archivo in (('situaciones', 'situaciones.json'), ('verbos', 'verbos.json')):
        p = RAIZ / f'assets/contenido/{idioma}/{archivo}'
        if p.exists():
            d = json.loads(p.read_text(encoding='utf-8'))
            extra[nombre] = len(d.get('situaciones', d.get('verbos', d)) if isinstance(d, dict) else d)
    datos = {'idioma': idioma, 'niveles': niveles, 'personajes': personajes, 'hechosN1': [ES(h) for h in n1.get('hechosDelReparto', [])],
             'antes': antes, 'extra': extra}
    plantilla = (Path(__file__).parent / 'pagina_plan.html').read_text(encoding='utf-8')
    salida.write_text(plantilla.replace('/*DATOS*/null', json.dumps(datos, ensure_ascii=False).replace('</', '<\\/')),
                      encoding='utf-8')
    print(f'{salida}: {salida.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
