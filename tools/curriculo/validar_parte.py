#!/usr/bin/env python3
"""Valida un trozo de fichas de un nivel contra el mapa del idioma, antes de
unirlo al plan (`curriculo/<idioma>/nX.json`).

Uso: python3 tools/curriculo/validar_parte.py <idioma> <nivel> <parte.json>
     (parte.json: lista de fichas, o {"clases": [...]}, de bloques completos)

Comprueba, además de las reglas de validar_plan.py:
- que `introduce` use solo las claves que `curriculo/<idioma>/MAPA.md` da a ese
  bloque y que el bloque las introduzca todas;
- que `recicla` solo use claves de Fundamentos, de bloques anteriores o de
  clases anteriores del mismo bloque;
- en idiomas con apoyo solo en inglés (es), que las consignas estén en inglés.
Sale con código 1 si hay errores.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validar_plan as vp  # noqa: E402

CONSIGNA_ES = re.compile(r'^(Elige|Completa|Escucha|Ordena|Escribe|Relaciona|Traduce|Responde)\b|^¿')


def main():
    idioma, nivel, archivo = sys.argv[1], int(sys.argv[2]), Path(sys.argv[3])
    marco = vp.validar_marco()
    mapa = vp.leer_mapa(idioma)
    n1 = json.loads((vp.CURRICULO / idioma / 'n1.json').read_text(encoding='utf-8'))
    datos = json.loads(archivo.read_text(encoding='utf-8'))
    clases = datos['clases'] if isinstance(datos, dict) else datos
    bloques = sorted({c.get('bloque') for c in clases})
    vistas = set(n1.get('previos', []))
    for nv in range(1, nivel):
        for ks in mapa.get(nv, {}).values():
            vistas.update(ks)
    for b in range(1, bloques[0]):
        vistas.update(mapa[nivel].get(b, []))
    solo_en = idioma == 'es'
    hechas = {b: [] for b in bloques}
    for c in clases:
        b = c.get('bloque')
        i = int(str(c.get('id', '')).rsplit('c', 1)[-1] or 0)
        d = f'{idioma} n{nivel} {c.get("id")}'
        if c.get('id') != f'{idioma}.n{nivel}.c{i:02d}' or (i - 1) // vp.CLASES_POR_BLOQUE + 1 != b:
            vp.errores.append(f'{d}: id o bloque incoherentes')
        mb = marco.get(nivel, {}).get(b, {})
        for campo in ('titulo', 'objetivo', 'tarea'):
            vp.bilingue(c.get(campo), f'{d} {campo}')
        g = c.get('gramatica')
        if not isinstance(g, list) or not g:
            vp.errores.append(f'{d}: gramatica debe ser una lista de puntos')
        intro = vp.slugs(c.get('introduce'), f'{d} introduce')
        if not intro and mb.get('tipo') == 'tema':
            vp.errores.append(f'{d}: una clase de bloque temático introduce al menos un punto nuevo')
        for k in intro:
            if k not in mapa[nivel].get(b, []):
                vp.errores.append(f'{d}: introduce «{k}», que el mapa no da al bloque {b}')
            if k in vistas:
                vp.errores.append(f'{d}: «{k}» ya se introdujo antes')
        rec = vp.slugs(c.get('recicla'), f'{d} recicla')
        for k in rec:
            if k not in vistas:
                vp.errores.append(f'{d}: recicla «{k}», que no se introdujo antes')
        vistas.update(intro)
        hechas[b].extend(intro)
        voc = c.get('vocabulario') or {}
        vp.bilingue(voc.get('campo'), f'{d} vocabulario.campo')
        if not isinstance(voc.get('palabras'), list) or not 6 <= len(voc['palabras']) <= 12:
            vp.errores.append(f'{d}: vocabulario.palabras debe tener 6–12 palabras')
        if nivel == 1 and not (isinstance(c.get('sonido'), str) and c['sonido'].strip()):
            vp.errores.append(f'{d}: en N1 cada clase abre con un sonido')
        s = c.get('situacion')
        if not isinstance(s, int) or not 1 <= s <= 50:
            vp.errores.append(f'{d}: situacion debe ser un id 1…50')
        if c.get('estado') != 'planificado':
            vp.errores.append(f'{d}: estado debe ser «planificado»')
        vp.validar_ejercicios(c, d, intro, rec)
        ej = c.get('ejercicios') or {}
        items = [*ej.get('guiada', []), *ej.get('independiente', []), *ej.get('evaluacion', []),
                 *(ej.get('situacion') or {}).get('preguntas', [])]
        for it in items:
            if not isinstance(it, dict):
                continue
            if '→' not in str(it.get('ejemplo', '')):
                vp.errores.append(f'{d}: ejemplo sin «→ respuesta»: {str(it.get("ejemplo"))[:50]}')
            if solo_en and CONSIGNA_ES.search(str(it.get('consigna', ''))):
                vp.errores.append(f'{d}: consigna en español (va en inglés): {str(it.get("consigna"))[:50]}')
    for b in bloques:
        falta = [k for k in mapa[nivel].get(b, []) if k not in hechas[b]]
        if falta:
            vp.errores.append(f'{idioma} n{nivel} b{b}: el mapa pide introducir {", ".join(falta)}')
    for a in vp.avisos:
        print('aviso:', a)
    for e in vp.errores:
        print('ERROR:', e)
    print(f'== {archivo.name}: {len(clases)} fichas, {len(vp.errores)} error(es)')
    sys.exit(1 if vp.errores else 0)


if __name__ == '__main__':
    main()
