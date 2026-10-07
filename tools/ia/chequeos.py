#!/usr/bin/env python3
"""Chequeos de los fallos que los revisores humanos encontraron una y otra vez (pt, de)
y que validar_ruta.py no mira. Se pasan tras cada clase generada por IA.

    python3 tools/ia/chequeos.py tools/contenido/ruta-it/n1-b01.json [--clase it.n1.c03]

ERROR = la clase se repara · AVISO = se informa al revisor.
"""
import json, re, sys

ESPANA = re.compile(r'\b(vosotr[oa]s|vuestr[oa]s?|habéis|tenéis|sois|móvil(es)?|coche(s)?|ordenador(es)?|zumo|patatas?|'
                    r'aparcar|coger|cogí|melocot[oó]n|ordenata|gafetes?|m[oó]dulo de inscripci[oó]n|'
                    r'compa[ñn]er[oa]s? de piso|entrantes?|camarer[oa]s?|crua?s[aá]n(es)?|hectos?|piso compartido|'
                    r'billetes? de (tren|avi[oó]n|autob[uú]s)|bocadillos?|zapatillas de deporte)\b|(^|[¡.!?]\s*)vale\b[,.!]', re.I)
ESPANOL = re.compile(r'\b(el|los|las|del|y|es|está|están|por|para|su|sus|un|unos|pero|también|muy|hay)\b', re.I)
INGLES = re.compile(r'\b(the|a|an|and|is|are|of|to|in|at|with|for|his|her)\b', re.I)
# Palabras que delatan el idioma meta dentro de un texto de apoyo.
META = {
    'it': re.compile(r'\b(il|gli|della|dello|degli|nel|nella|alla|sono|è|non|anche|questo|questa|ho|hai|perché|molto|grazie)\b', re.I),
    'de': re.compile(r'\b(der|die|das|und|ist|nicht|ich|mit|ein|eine|auf|zu|wir|bitte)\b', re.I),
}
TRANSFORMA = re.compile(r'^(une|transforma|pasa|reformula|convierte|cambia|combina|reescribe|reemplaza|sustituye)\b', re.I)
ECUADOR = re.compile(r'[Ee]cuador|ECUADOR|\bQuito\b|[Gg]uayaquil|\bCuenca\b|[Ee]cuatorian')  # «quito» (verbo) no cuenta
CITAS = re.compile(r'«[^»]*»|“[^”]*”|"[^"]*"')


PUNTUACION = re.compile(r'[.,!?¡¿;:/。、！？「」…"“”«»()—–，：；]')


def normalizar(t):
    return re.sub(r'\s+', ' ', PUNTUACION.sub(' ', t.lower().replace('’', "'").replace('‘', "'"))).strip()


def sin_citas(t):
    return CITAS.sub(' ', t or '')


def textos(x, ruta=''):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from textos(v, f'{ruta}.{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from textos(v, f'{ruta}[{i}]')
    elif isinstance(x, str):
        yield ruta, x


def revisar(u):
    e, a = [], []
    uid = u['id']
    for ruta, t in textos(u):
        if ECUADOR.search(t):
            e.append(f'{uid}{ruta}: menciona Ecuador o una ciudad ecuatoriana')
        if ruta.endswith('.es') and ESPANA.search(sin_citas(t)):
            e.append(f'{uid}{ruta}: español de España «{ESPANA.search(sin_citas(t)).group(0)}» (usa español latino neutro)')
        if ruta.endswith(('.es', '.en')) and len(t.strip()) <= 1 and ('.titulo' in ruta or '.columnas' in ruta):
            e.append(f'{uid}{ruta}: texto de un solo carácter')
        if ruta.endswith('.en') and re.search(r'[¿¡ñ]', sin_citas(t)):
            e.append(f'{uid}{ruta}: el campo «en» contiene español')
    for p in u.get('pasos', []):
        donde = f'{uid}.{p.get("id")}'
        if p.get('tipo') == 'situacion':
            ctx = p.get('contexto', {})
            meta = META.get(uid.split('.')[0])
            for lengua, marcas in (('es', ESPANOL), ('en', INGLES)):
                t = sin_citas(ctx.get(lengua, ''))
                ajenas = len(meta.findall(t)) if meta else 0
                if ajenas >= 3 and ajenas > len(marcas.findall(t)):
                    e.append(f'{donde}.contexto.{lengua}: está escrito en el idioma meta, no en {"español" if lengua == "es" else "inglés"}')
            hablantes = [l.get('hablante') for l in p.get('dialogo', [])]
            if any(re.fullmatch(r'[A-Z]\.?', h or '') for h in hablantes):
                e.append(f'{donde}: hablantes «A/B»: usa nombres de la ficha del idioma o el papel en el idioma meta')
            for i in range(1, len(hablantes)):
                if hablantes[i] == hablantes[i - 1]:
                    (e if u.get('nivelInterno', 1) <= 4 else a).append(f'{donde}.dialogo[{i}]: dos líneas seguidas de {hablantes[i]}')
            if any('lumo' in (h or '').lower() for h in hablantes) and len(set(hablantes)) > 1:
                e.append(f'{donde}: Lumo comparte escena con otro personaje')
        for it in p.get('items', []) or []:
            if 'formato' not in it:
                continue
            d = f'{donde}.{it.get("id")}'
            c = it.get('consigna', {}).get('es', '')
            f = it['formato']
            if f == 'escribir' and TRANSFORMA.search(c.strip()) and not CITAS.search(c):
                e.append(f'{d}: consigna de transformación sin la frase de partida entre «…»')
            if f == 'completar' and it.get('texto', '').count('___') != 1:
                e.append(f'{d}: completar debe tener exactamente un «___»')
            if f in ('elegir', 'escuchar'):
                ops = [json.dumps(o, ensure_ascii=False) for o in it.get('opciones', [])]
                if len(set(ops)) != len(ops):
                    e.append(f'{d}: opciones repetidas')
                if not (isinstance(it.get('respuesta'), int) and 0 <= it['respuesta'] < len(ops)):
                    e.append(f'{d}: respuesta fuera de las opciones')
            if f == 'ordenar':
                # Igual que normalizar() de lib/core/aprendizaje/correccion.dart: la app quita la puntuación.
                if sorted(normalizar(' '.join(it.get('tokens', []))).split()) != sorted(normalizar(it.get('respuesta', '')).split()):
                    e.append(f'{d}: los tokens no son exactamente las palabras de la respuesta')
            if f == 'relacionar':
                izq = [x[0] for x in it.get('pares', [])]
                der = [json.dumps(x[1], ensure_ascii=False) for x in it.get('pares', [])]
                if len(set(izq)) != len(izq) or len(set(der)) != len(der):
                    e.append(f'{d}: pares repetidos (cada lado debe tener una sola pareja)')
            if f == 'escribir' and it.get('abierta') and len(it.get('respuesta', '').split()) < it.get('minimoPalabras', 0):
                e.append(f'{d}: la respuesta modelo tiene menos de minimoPalabras')
    nuevo = u['id'].split('.')[0] not in ('de', 'pt', 'fr', 'es', 'en')  # reglas nuevas: solo idiomas producidos con tools/ia
    if nuevo:
        if len(u.get('vocabulario', [])) > 12:
            e.append(f'{uid}: {len(u["vocabulario"])} entradas de vocabulario (máximo 12)')
        n_ej = sum(len(p.get('items', [])) for p in u.get('pasos', []) if p.get('tipo') == 'ejemplos')
        if n_ej > 8:
            e.append(f'{uid}: {n_ej} ejemplos (máximo 8)')
        formatos = [it.get('formato') for p in u.get('pasos', []) for it in p.get('items', []) or []]
        if 'escuchar' not in formatos:
            e.append(f'{uid}: ningún ítem escuchar (pon al menos uno)')
        tipos = [p.get('tipo') for p in u.get('pasos', [])]
        for t in ('vocabulario', 'ejemplos', 'practica_guiada', 'practica_independiente', 'situacion', 'evaluacion'):
            if tipos.count(t) > 1:
                e.append(f'{uid}: paso {t} repetido')
        for p in u.get('pasos', []):
            for it in p.get('items', []) or []:
                d = f'{uid}.{p.get("id")}.{it.get("id")}'
                c = it.get('consigna', {}).get('es', '')
                if it.get('formato') == 'ordenar':
                    toks = it.get('tokens', [])
                    if len(toks) < 3:
                        e.append(f'{d}: ordenar con menos de 3 tokens')
                    if any(PUNTUACION.search(t) for t in toks):
                        e.append(f'{d}: tokens con signos de puntuación (van sin ellos)')
                    base = sorted(normalizar(' '.join(toks)).split())
                    for alt in it.get('aceptadas', []) or []:
                        if sorted(normalizar(alt).split()) != base:
                            e.append(f'{d}: la aceptada «{alt}» no usa exactamente las palabras de los tokens')

                if it.get('formato') in ('escribir', 'completar') and not it.get('abierta') and p.get('tipo') != 'situacion':
                    resp = str(it.get('respuesta', ''))
                    # Nombres propios = mayúscula que no abre frase (en la situación los datos salen del diálogo).
                    nombres = [m.group(1) for m in re.finditer(r"(?<![.!?¿¡]\s)(?<!^)\b([A-ZÁÉÍÓÚ][a-zàèéìòù]+)\b", resp)
                               if m.start() > 0 and m.group(1) not in ('Lei', 'Loro')]
                    faltan = [w for w in nombres if w not in c + it.get('texto', '')]
                    if faltan:
                        e.append(f'{d}: la respuesta usa {", ".join(faltan)}, que la consigna no da')
                if re.search(r'\bustedes\b', c) and re.search(r'\b(noi|ci chiamiamo|siamo|abbiamo)\b', str(it.get('respuesta', '')), re.I):
                    e.append(f'{d}: «ustedes» pide voi, pero la respuesta es de noi')
            if p.get('tipo') == 'explicacion' and p.get('icono') == 'sonido' and re.search(r'\b(church|jeans|canyon|million|loch|English)\b', sin_citas(p.get('texto', {}).get('es', ''))):
                e.append(f'{uid}.{p.get("id")}: guía de sonido en español con referencia inglesa (va solo en «en»)')
    ejemplos = [p for p in u.get('pasos', []) if p.get('tipo') == 'ejemplos']
    if ejemplos and len(ejemplos[0].get('items', [])) > 10:
        a.append(f'{uid}: {len(ejemplos[0]["items"])} ejemplos (lo normal es 5–8)')
    if not u.get('erroresFrecuentes'):
        e.append(f'{uid}: faltan erroresFrecuentes')
    ev = next((p for p in u.get('pasos', []) if p.get('tipo') == 'evaluacion'), None)
    if ev:
        puntuables = [it for it in ev.get('items', []) if not it.get('abierta')]
        if len(puntuables) < 4 or len({it['formato'] for it in puntuables}) < 2:
            e.append(f'{uid}: la evaluación necesita ≥ 4 ítems puntuables y ≥ 2 formatos')
    for x in re.finditer(r'⚠', json.dumps(u, ensure_ascii=False)):
        a.append(f'{uid}: usa ⚠ (comprueba que es un falso amigo real)')
        break
    return e, a


def main():
    ruta = sys.argv[1]
    solo = sys.argv[sys.argv.index('--clase') + 1] if '--clase' in sys.argv else None
    total = 0
    for u in json.load(open(ruta, encoding='utf-8'))['unidades']:
        if solo and u['id'] != solo:
            continue
        e, a = revisar(u)
        total += len(e)
        for x in e: print('ERROR', x)
        for x in a: print('AVISO', x)
    print(f'== {total} error(es)')
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
