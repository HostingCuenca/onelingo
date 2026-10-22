#!/usr/bin/env python3
"""Volcado compacto de las variantes aplicadas de un nivel para revisarlas rápido.

Uso: python3 tools/contenido/refuerzo/volcado.py fr 2
"""
import sys

from construir import Constructor, frases, variantes_de


def main():
    idioma, nv = sys.argv[1], int(sys.argv[2])
    variantes = variantes_de(idioma, nv)
    for b in range(1, 11):
        c = Constructor(idioma, nv, b).preparar()
        c.frases_originales = {f for u in c.clases for f, _ in frases(u)} | {
            it.get('respuesta') for u in c.clases for p in u['pasos'] for it in (p.get('items') or [])}
        extra = {r['id']: x for r, x in c.refuerzos}
        for clave, cand in c.candidatas.items():
            v = variantes.get(clave)
            if v and not c.aceptar(cand['frase'], v, cand['mantener'], extra[clave.rsplit('.', 1)[0]]):
                print(f"{clave.split('.', 2)[2]} | {cand['frase']} → {v['variante']} | {v['es']}")


if __name__ == '__main__':
    main()
