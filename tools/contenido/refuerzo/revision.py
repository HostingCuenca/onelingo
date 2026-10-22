#!/usr/bin/env python3
"""Tabla HTML para revisar a ojo las variantes de un nivel: original → variante,
palabras cambiadas resaltadas, traducciones y si pasó el control automático.

Uso: python3 tools/contenido/refuerzo/revision.py fr 1 salida.html
"""
import difflib
import html
import sys

from construir import Constructor, frases, palabras, variantes_de


def resaltar(original, variante):
    a, b = variante.split(), original.split()
    sm = difflib.SequenceMatcher(a=[tuple(palabras(w)) for w in b], b=[tuple(palabras(w)) for w in a])
    res = []
    for op, _, _, j1, j2 in sm.get_opcodes():
        trozo = html.escape(' '.join(a[j1:j2]))
        res.append(trozo if op == 'equal' else f'<mark>{trozo}</mark>')
    return ' '.join(t for t in res if t)


def main():
    idioma, nv, salida = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    variantes = variantes_de(idioma, nv)
    filas, cuenta = [], {'aplicada': 0, 'rechazada': 0, 'sin variante': 0}
    for b in range(1, 11):
        c = Constructor(idioma, nv, b).preparar()
        c.frases_originales = {f for u in c.clases for f, _ in frases(u)} | {
            it.get('respuesta') for u in c.clases for p in u['pasos'] for it in (p.get('items') or [])}
        extra = {r['id']: x for r, x in c.refuerzos}
        for clave, cand in c.candidatas.items():
            v = variantes.get(clave)
            rid = clave.rsplit('.', 1)[0]
            motivo = c.aceptar(cand['frase'], v, cand['mantener'], extra[rid]) if v else None
            estado = 'sin variante' if not v else ('rechazada' if motivo else 'aplicada')
            cuenta[estado] += 1
            filas.append(
                f'<tr class="{estado.replace(" ", "-")}"><td>{html.escape(clave.split(".", 2)[2])}</td>'
                f'<td lang="{idioma}">{html.escape(cand["frase"])}</td>'
                f'<td lang="{idioma}">{resaltar(cand["frase"], v["variante"]) if v else "—"}</td>'
                f'<td>{html.escape(v["es"]) if v else ""}</td><td>{html.escape(v["en"]) if v else ""}</td>'
                f'<td>{estado}{": " + html.escape(motivo) if motivo else ""}</td></tr>')
    total = sum(cuenta.values())
    with open(salida, 'w', encoding='utf-8') as f:
        f.write(f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Variantes {idioma} N{nv}</title>
<style>
:root {{ --fondo:#fff; --texto:#1d1b26; --suave:#6b6880; --linea:#e6e3ef; --marca:#ffe58a; --mal:#fde2e1; --nada:#f4f3f8; }}
@media (prefers-color-scheme: dark) {{ :root {{ --fondo:#16151c; --texto:#ece9f5; --suave:#a29fb5; --linea:#2c2a36; --marca:#7a6200; --mal:#4a1f1f; --nada:#1f1e27; }} }}
body {{ margin:0; padding:16px; font:14px/1.45 system-ui, sans-serif; background:var(--fondo); color:var(--texto); }}
h1 {{ font-size:20px; margin:0 0 4px; }} p {{ color:var(--suave); margin:0 0 12px; }}
.tabla {{ overflow-x:auto; }} table {{ border-collapse:collapse; width:100%; min-width:760px; }}
th, td {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--linea); vertical-align:top; }}
th {{ position:sticky; top:0; background:var(--fondo); font-size:12px; color:var(--suave); }}
td:first-child {{ font-family:ui-monospace, monospace; font-size:12px; color:var(--suave); white-space:nowrap; }}
mark {{ background:var(--marca); color:inherit; padding:0 2px; border-radius:3px; }}
tr.rechazada {{ background:var(--mal); }} tr.sin-variante {{ background:var(--nada); color:var(--suave); }}
</style></head><body>
<h1>Variantes de refuerzo · {idioma} N{nv}</h1>
<p>{total} frases: {cuenta["aplicada"]} aplicadas, {cuenta["rechazada"]} rechazadas por el control automático y {cuenta["sin variante"]} sin variante (quedan como el original). Amarillo = palabras cambiadas.</p>
<div class="tabla"><table><thead><tr><th>Ejercicio</th><th>Original</th><th>Variante</th><th>Español</th><th>Inglés</th><th>Estado</th></tr></thead>
<tbody>{"".join(filas)}</tbody></table></div></body></html>''')
    print(f'{salida}: {cuenta}')


if __name__ == '__main__':
    main()
