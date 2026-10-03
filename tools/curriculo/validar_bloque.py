#!/usr/bin/env python3
"""Valida un bloque en borrador aunque falten bloques anteriores sin escribir.

Pasa a validar_ruta.py todos los borradores aún no integrados hasta el bloque
pedido; los bloques que todavía no existen se sustituyen por esbozos mínimos
(id, orden, prerrequisitos) para que la cadena no se rompa. Imprime solo los
errores del bloque, así los agentes no persiguen errores ajenos.

Los esbozos enseñan el vocabulario de sus fichas.

Uso: python3 tools/curriculo/validar_bloque.py fr 10 5
"""
import json, os, re, subprocess, sys, tempfile

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
idi, n, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
curso = json.load(open(f'{R}/assets/contenido/{idi}/ruta/curso.json'))
integrados = {int(m[1]) for nv in curso.get('niveles', []) if (m := re.fullmatch(r'n(\d+)', str(nv.get('id'))))}
if n in integrados:
    sys.exit(f'N{n} ya está integrado en curso.json: valida con python3 tools/validar_ruta.py {idi}')
desde = max([k for k in integrados if k < n], default=0) + 1
tmp = tempfile.mkdtemp(prefix='esbozos-')
fs, esbozos = [], []
for k in range(desde, n + 1):
    for j in range(1, 11):
        if (k, j) > (n, b): break
        p = f'{R}/tools/contenido/ruta-{idi}/n{k}-b{j:02d}.json'
        completo = False
        if os.path.exists(p):
            try: completo = len(json.load(open(p))['unidades']) == 5
            except Exception: pass
        if completo or (k, j) == (n, b): fs.append(p); continue
        cur = json.load(open(f'{R}/curriculo/{idi}/n{k}.json'))
        us = []
        for c in cur['clases']:
            if c['bloque'] != j: continue
            i = int(c['id'].split('.c')[1])
            prev = f'{idi}.n{k}.c{i - 1:02d}' if i > 1 else f'{idi}.n{k - 1}.c50'
            # El esbozo enseña el vocabulario de la ficha: los bloques se pueden escribir en
            # paralelo contando solo con lo que las fichas anteriores prometen enseñar.
            voc = [{'id': f'v-{c["id"]}-{x}', 'texto': w, 'traduccion': {'en': w}}
                   for x, w in enumerate(c.get('vocabulario', {}).get('palabras', []))]
            us.append({'id': c['id'], 'orden': k * 100 + i, 'titulo': c['titulo'], 'objetivo': c['objetivo'],
                       'cefr': cur['cefr'], 'nivelInterno': k, 'prerequisitos': [prev], 'vocabulario': voc,
                       'pasos': [{'id': 'p1', 'tipo': 'vocabulario', 'refs': [v['id'] for v in voc]}] if voc else []})
        sp = f'{tmp}/n{k}-b{j:02d}.json'
        json.dump({'modulo': {'id': f'{idi}.n{k}-b{j:02d}'}, 'unidades': us}, open(sp, 'w'), ensure_ascii=False)
        fs.append(sp); esbozos.append(f'n{k}-b{j:02d}')
res = subprocess.run(['python3', 'tools/validar_ruta.py', idi, '--borrador', *fs], cwd=R, capture_output=True, text=True)
out = res.stdout
if 'Traceback' in res.stderr:
    # Un fallo del validador (p. ej. un campo de texto null) no puede pasar por «0 errores».
    print(res.stderr.strip().splitlines()[-1])
    sys.exit(f'== N{n} B{b}: validar_ruta.py falló; revisa campos nulos o mal formados en los borradores')
clases = '|'.join(f'{(b - 1) * 5 + i:02d}' for i in range(1, 6))
mios = [l for l in out.splitlines() if re.search(rf'{idi}\.n{n}\.c({clases})\b', l) or f'n{n}-b{b:02d}' in l]
print('\n'.join(mios[:60]) + (f'\n... (+{len(mios) - 60} más)' if len(mios) > 60 else ''))
print(f'== N{n} B{b}: {len(mios)} error(es) del bloque' + (f' · esbozos: {", ".join(esbozos)}' if esbozos else ''))
