#!/usr/bin/env python3
"""Valida unidades del Nivel 0 (mismas reglas que test/nivel0_test.dart).

Uso:
  python3 tools/contenido/validar_nivel0.py <idioma> [archivo.json] [--bilingue]

Con --bilingue exige que cada texto de apoyo sea {"es": …, "en": …}
(fase I2: el contenido sirve a hispanohablantes y a anglohablantes).

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


CAMPOS_APOYO = ('texto', 'pregunta', 't', 'nota', 'titulo', 'objetivo')


def faltan_idiomas(datos):
    """Textos de apoyo que no tienen español e inglés."""
    res = []

    def bilingue(v):
        return isinstance(v, dict) and v.get('es') and v.get('en')

    for u in datos['unidades']:
        for campo in ('titulo', 'objetivo'):
            if u.get(campo) and not bilingue(u[campo]):
                res.append(f'{u["id"]}.{campo}')
        for l in u['lecciones']:
            if not bilingue(l.get('titulo')):
                res.append(f'{l["id"]}.titulo')
            for i, p in enumerate(l.get('pasos', [])):
                for campo in CAMPOS_APOYO:
                    if campo in p and not bilingue(p[campo]):
                        res.append(f'{l["id"]}#{i}.{campo}')
                for w in p.get('palabras', []) + [o for o in p.get('opciones', []) if isinstance(o, dict)]:
                    if 't' in w and not bilingue(w['t']):
                        res.append(f'{l["id"]}#{i}.palabra.t')
                if p['tipo'] == 'elige_significado':
                    if not all(bilingue(o) for o in p.get('opciones', [])):
                        res.append(f'{l["id"]}#{i}.opciones')
    for k, v in (datos.get('textos') or {}).items():
        if k == 'grupos':
            res += [f'textos.grupos.{g}' for g, t in v.items() if not bilingue(t)]
        elif k not in ('muestra', 'emoji') and not bilingue(v):
            res.append(f'textos.{k}')
    return res


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
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    idioma = args[0]
    ruta = (
        pathlib.Path(args[1])
        if len(args) > 1
        else RAIZ / f'assets/contenido/{idioma}/nivel0/nivel0.json'
    )
    datos = json.loads(ruta.read_text(encoding='utf-8'))
    problemas, faltan = validar(idioma, datos)
    if '--bilingue' in sys.argv:
        sin = faltan_idiomas(datos)
        problemas += [f'sin español e inglés: {x}' for x in sin[:40]]
        if len(sin) > 40:
            problemas.append(f'… y {len(sin) - 40} más')
    for p in problemas:
        print('ERROR', p)
    if faltan:
        print('EMOJI QUE FALTAN (descargar de Noto):', ' '.join(faltan))
    lecciones = sum(len(u['lecciones']) for u in datos['unidades'])
    print(f'{len(datos["unidades"])} unidades, {lecciones} lecciones, {len(problemas)} errores')
    sys.exit(1 if problemas else 0)


if __name__ == '__main__':
    main()
