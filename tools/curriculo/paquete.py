#!/usr/bin/env python3
"""Paquete de contexto de un bloque: un solo archivo con todo lo que necesita
el autor o el revisor (brief, esquema, plan, nota del nivel, índice, las 5
fichas, el reparto, los hechos recientes y una clase modelo publicada).

Los agentes leen solo este archivo en vez de explorar el repositorio: así su
contexto no crece en cada turno (ver PLAN_PRODUCCION.md, «Agentes»).

Uso: python3 tools/curriculo/paquete.py fr 10 5 [--salida DIR] [--modelo fr.n8.c01]
"""
import argparse, glob, json, os, re

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
a = argparse.ArgumentParser()
a.add_argument('idioma'); a.add_argument('nivel', type=int); a.add_argument('bloque', type=int)
a.add_argument('--salida', default='/tmp/onelingo-paquetes')
a.add_argument('--modelo', help='id de una clase publicada que sirve de modelo (por defecto la primera del nivel anterior)')
x = a.parse_args(); idi, n, b = x.idioma, x.nivel, x.bloque
L = lambda p: json.load(open(os.path.join(R, p)))
cur = L(f'curriculo/{idi}/n{n}.json'); n1 = L(f'curriculo/{idi}/n1.json')
cards = [c for c in cur['clases'] if c['bloque'] == b]
out = [f'# Paquete de contexto · {idi} N{n} bloque B{b} ({cards[0]["id"]}–{cards[-1]["id"]})\n']
w = out.append
for doc in [f'ENCARGO_RUTA_{idi.upper()}.md', 'ESQUEMA_CONTENIDO.md', 'PLAN_CLASES.md']:
    p = f'{R}/docs/claude-educacion/{doc}'
    if os.path.exists(p): w(f'\n\n########## docs/claude-educacion/{doc}\n' + open(p).read())
w(f'\n\n########## Nivel N{n}: nota y examen\n' + json.dumps({'cefr': cur['cefr'], 'nota': cur['nota'], 'examen': cur.get('examen')}, ensure_ascii=False, indent=1))
w(f'\n\n########## Índice de las 50 clases de N{n}\n')
for c in cur['clases']: w(f"- {c['id']} B{c['bloque']}: {c['titulo']['es']} · introduce={c.get('introduce')}\n")
w('\n\n########## LAS 5 FICHAS DEL BLOQUE (fuente de verdad)\n' + json.dumps(cards, ensure_ascii=False, indent=1))
w('\n\n########## Reparto: personajes (n1.json)\n' + json.dumps(n1['personajes'], ensure_ascii=False, indent=1))
txt = json.dumps(cards, ensure_ascii=False)
libres = L(f'assets/contenido/{idi}/ruta/curso.json').get('palabrasLibres', [])
names = [p for p in libres if p != 'Ana' and len(p) > 2 and re.search(r'\b' + re.escape(p) + r'\b', txt)]
w(f'\n\n########## Hechos del reparto sobre: {", ".join(names) or "(nadie nombrado)"} (últimos 3 niveles; los anteriores están en curriculo/{idi}/nK.json)\n')
for k in range(max(1, n - 3), n):
    for h in L(f'curriculo/{idi}/n{k}.json').get('hechosDelReparto', []):
        if any(re.search(r'\b' + re.escape(p) + r'\b', h['es']) for p in names): w(f"- N{k}: {h['es']}\n")
w('\n\n########## Hechos confirmados en revisiones de borradores aún sin recoger\n')
for f in sorted(glob.glob(f'{R}/tools/contenido/ruta-{idi}/revision-n{n}-b*.md')):
    kb = int(re.search(r'-b(\d+)', f)[1])
    if kb >= b: continue
    s = re.search(r'## Hechos del reparto confirmados\n(.*?)(\n## |\Z)', open(f).read(), re.S)
    if s: w(f'\n### N{n} B{kb}\n' + '\n'.join(l.split(' / ')[0] for l in s[1].strip().splitlines()) + '\n')
mid = x.modelo or f'{idi}.n{max(1, n - 1)}.c01'
mn, mc = re.match(rf'{idi}\.n(\d+)\.c(\d+)', mid).groups()
mod = L(f'assets/contenido/{idi}/ruta/n{mn}-b{(int(mc) - 1) // 5 + 1:02d}.json')
u = [u for u in mod['unidades'] if u['id'] == mid]
w(f'\n\n########## MODELO de clase publicada ({mid}; solo estilo y forma)\n' + json.dumps({'modulo': mod['modulo'], 'unidades': u}, ensure_ascii=False, indent=1))
os.makedirs(x.salida, exist_ok=True)
p = f'{x.salida}/{idi}-n{n}-b{b:02d}.md'
open(p, 'w').write(''.join(out)); print(p, len(''.join(out)) // 1000, 'kB')
