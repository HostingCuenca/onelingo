#!/usr/bin/env python3
"""Textos de interfaz (I1, docs/claude-educacion/I18N.md).

Busca las llamadas `tr('texto en español', …)` en lib/ y las compara con
assets/i18n/<idioma>.json.

Uso:
  python3 tools/i18n/extraer.py --comprobar        # sale con 1 si falta algo
  python3 tools/i18n/extraer.py --pendientes en    # escribe tools/i18n/pendientes-en.json
  python3 tools/i18n/extraer.py --limpiar en       # quita traducciones que ya no se usan
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
IDIOMAS = ['en']
LLAMADA = re.compile(r'(?<![A-Za-z0-9_.])tr\(\s*')
MARCA = re.compile(r'\{([A-Za-z_][A-Za-z0-9_]*)\}')


def _literal(texto, i):
    """Lee una cadena Dart en texto[i:] ('…', "…", '''…'''). Devuelve (valor, fin)."""
    crudo = texto[i] == 'r'
    if crudo:
        i += 1
    for q in ("'''", '"""', "'", '"'):
        if texto.startswith(q, i):
            break
    else:
        return None, i
    j, valor = i + len(q), []
    while j < len(texto):
        if texto.startswith(q, j):
            return ''.join(valor), j + len(q)
        c = texto[j]
        if c == '\\' and not crudo:
            sig = texto[j + 1]
            valor.append({'n': '\n', 't': '\t', "'": "'", '"': '"', '\\': '\\', '$': '$'}.get(sig, '\\' + sig))
            j += 2
            continue
        valor.append(c)
        j += 1
    return None, j


def claves():
    """{clave: [archivo:línea, …]} de todas las llamadas tr()."""
    res, errores = {}, []
    for f in sorted(RAIZ.glob('lib/**/*.dart')):
        if f.name.endswith('.g.dart') or f.name == 'i18n.dart':
            continue
        texto = f.read_text(encoding='utf-8')
        for m in LLAMADA.finditer(texto):
            i, partes = m.end(), []
            while True:
                while i < len(texto) and texto[i] in ' \n\t':
                    i += 1
                valor, fin = _literal(texto, i)
                if valor is None:
                    break
                partes.append(valor)
                i = fin
            linea = texto.count('\n', 0, m.start()) + 1
            donde = f'{f.relative_to(RAIZ)}:{linea}'
            if not partes:
                errores.append(f'{donde}: tr() sin cadena literal')
                continue
            clave = ''.join(partes)
            if '$' in clave:
                errores.append(f'{donde}: la clave lleva $ (usa {{nombre}}): {clave[:60]}')
            res.setdefault(clave, []).append(donde)
    return res, errores


def datos():
    """Claves de textos que llegan como dato y se muestran con trDato()."""
    res = {}
    cat = json.loads((RAIZ / 'assets/contenido/situaciones/catalogo.json').read_text(encoding='utf-8'))
    for s in cat['situaciones']:
        res.setdefault(s['nombre'], []).append('catalogo.json')
        res.setdefault(s['categoria'], []).append('catalogo.json')
    return res


def diccionario(idioma):
    p = RAIZ / f'assets/i18n/{idioma}.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def main():
    usadas, errores = claves()
    for k, v in datos().items():
        usadas.setdefault(k, []).extend(v)
    modo = sys.argv[1] if len(sys.argv) > 1 else '--comprobar'
    if modo == '--pendientes':
        idioma = sys.argv[2]
        d = diccionario(idioma)
        faltan = {k: '' for k in sorted(usadas) if not d.get(k)}
        destino = RAIZ / f'tools/i18n/pendientes-{idioma}.json'
        destino.write_text(json.dumps(faltan, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(f'{len(faltan)} pendientes de {len(usadas)} → {destino.relative_to(RAIZ)}')
        return
    if modo == '--limpiar':
        idioma = sys.argv[2]
        d = diccionario(idioma)
        limpio = {k: v for k, v in sorted(d.items()) if k in usadas}
        (RAIZ / f'assets/i18n/{idioma}.json').write_text(
            json.dumps(limpio, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(f'{len(d) - len(limpio)} traducciones sin uso eliminadas')
        return
    for idioma in IDIOMAS:
        d = diccionario(idioma)
        for k, donde in sorted(usadas.items()):
            t = d.get(k)
            if not t:
                errores.append(f'{idioma}: falta traducir «{k[:70]}» ({donde[0]})')
            elif set(MARCA.findall(k)) != set(MARCA.findall(t)):
                errores.append(f'{idioma}: marcas distintas en «{k[:60]}» → «{t[:60]}»')
    for e in errores[:60]:
        print('ERROR', e)
    print(f'{len(usadas)} textos de interfaz, {len(errores)} errores')
    sys.exit(1 if errores else 0)


if __name__ == '__main__':
    main()
