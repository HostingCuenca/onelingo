#!/usr/bin/env python3
"""Valida unidades del Nivel 0 (mismas reglas que test/nivel0_test.dart).

Uso:
  python3 tools/contenido/validar_nivel0.py <idioma> [archivo.json]

Sin archivo valida assets/contenido/<idioma>/nivel0/nivel0.json. El archivo
puede ser un nivel0.json completo o un borrador {"unidades": [...]}.
Los emoji que falten se listan aparte (se descargan de Noto, no se generan).
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
GRUPO = re.compile(r'\(([^():]+):([^()]+)\)')
ESPECIALES = {'_', '=', '*'}


def segmentos(m):
    res, i = [], 0
    for g in GRUPO.finditer(m):
        if g.start() > i:
            res.append((m[i:g.start()], None))
        res.append((g.group(1), g.group(2)))
        i = g.end()
    if i < len(m):
        res.append((m[i:], None))
    return res


def plano(m):
    return ''.join(t for t, _ in segmentos(m)).replace('‿', ' ')


def opciones(p):
    return [o if isinstance(o, dict) else {'m': o} for o in p.get('opciones', [])]


def validar(idioma, datos):
    sonidos = json.loads(
        (RAIZ / f'assets/contenido/{idioma}/nivel0/sonidos.json').read_text()
    )
    ids_sonido = {v['id'] for v in sonidos['vocales']}
    problemas, faltan = [], set()

    def marcado(donde, m):
        for _, clave in segmentos(m or ''):
            if clave and clave not in ESPECIALES and clave not in ids_sonido:
                problemas.append(f'{donde}: sonido desconocido «{clave}» en {m}')

    def emoji(e):
        if e and not (RAIZ / f'assets/img/emoji/{e}.webp').exists():
            faltan.add(e)

    for v in sonidos['vocales']:
        emoji(v.get('emoji'))
    vistos = set()
    for u in datos['unidades']:
        for l in u['lecciones']:
            if l['id'] in vistos:
                problemas.append(f'id repetido {l["id"]}')
            vistos.add(l['id'])
            if not l.get('pasos'):
                problemas.append(f'{l["id"]}: sin pasos')
            for i, p in enumerate(l.get('pasos', [])):
                donde = f'{l["id"]}#{i} {p["tipo"]}'
                marcado(donde, p.get('m'))
                ops = opciones(p)
                for w in p.get('palabras', []) + ops:
                    marcado(donde, w.get('m'))
                    emoji(w.get('e'))
                t = p['tipo']
                if t == 'escucha_elige':
                    if plano(ops[p['correcta']]['m']).lower() != p['audio'].lower():
                        problemas.append(f'{donde}: el audio «{p["audio"]}» no es la opción correcta')
                elif t == 'toca_sonido':
                    for k, o in enumerate(ops):
                        tiene = any(c == p['sonido'] for _, c in segmentos(o['m']))
                        if k == p['correcta'] and not tiene:
                            problemas.append(f'{donde}: la correcta no tiene el sonido {p["sonido"]}')
                        if k != p['correcta'] and tiene:
                            problemas.append(f'{donde}: la opción {k} también tiene el sonido')
                elif t == 'construye':
                    fichas = list(p['fichas'])
                    for c in plano(p['m']):
                        if c in fichas:
                            fichas.remove(c)
                        else:
                            problemas.append(f'{donde}: faltan fichas para «{plano(p["m"])}»')
                            break
                elif t == 'cambia':
                    de, a = plano(p['de']), plano(p['a'])
                    difs = [k for k in range(min(len(de), len(a))) if de[k] != a[k]]
                    if len(de) != len(a) or len(difs) != 1:
                        problemas.append(f'{donde}: «{de}»→«{a}» debe cambiar una letra')
                    elif a[difs[0]] not in p.get('opciones', []):
                        problemas.append(f'{donde}: falta la letra correcta')
                elif t == 'escucha_letra':
                    if p['letra'] not in p.get('opciones', []):
                        problemas.append(f'{donde}: la letra no está en las opciones')
                elif t in ('deletreo', 'elige_significado', 'lee'):
                    n = len(ops) if t == 'lee' else len(p.get('opciones', []))
                    if p.get('correcta', 0) >= n:
                        problemas.append(f'{donde}: índice correcto inválido')
    return problemas, sorted(faltan)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    idioma = sys.argv[1]
    ruta = (
        pathlib.Path(sys.argv[2])
        if len(sys.argv) > 2
        else RAIZ / f'assets/contenido/{idioma}/nivel0/nivel0.json'
    )
    datos = json.loads(ruta.read_text(encoding='utf-8'))
    problemas, faltan = validar(idioma, datos)
    for p in problemas:
        print('ERROR', p)
    if faltan:
        print('EMOJI QUE FALTAN (descargar de Noto):', ' '.join(faltan))
    lecciones = sum(len(u['lecciones']) for u in datos['unidades'])
    print(f'{len(datos["unidades"])} unidades, {lecciones} lecciones, {len(problemas)} errores')
    sys.exit(1 if problemas else 0)


if __name__ == '__main__':
    main()
