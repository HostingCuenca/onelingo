#!/usr/bin/env python3
"""Integra en la ruta el ruso aprobado (versión esencial, como el japonés y el chino).

Ruso estándar contemporáneo (cirílico sin marcas de acento; romanización neutra
letra a letra con tilde aguda de acento solo en el `rom`) para hispanohablantes
y anglohablantes; apoyo bilingüe {es, en}. Copia adaptada de ruta-ja/integrar.py:
sin reparto ni canon, nombres genéricos (NOMBRES_LIBRES, las listas cerradas de
tools/ia/idiomas/ru.md) y nada de Ecuador (mercado EE. UU. + LatAm).

Los campos de romanización (`rom`, `textoRom`, `preguntaRom`, `opcionesRom`,
`tokensRom`, `paresRom`; docs/claude-educacion/ROMANIZACION.md) se copian tal
cual: este script solo reescribe `orden`, `prerequisitos` y `modulo`.

- Fundamentos: si existen `borrador-f0.json` y `revision-f0.md` con GO en la
  línea «Estado:» (o, con --esencial, si pasa `validar.py`), se copia a
  assets/contenido/ru/ruta/f0.json. Si no, se conserva el f0 publicado.
- Niveles: borradores `nX-bYY.json` con `revision-nX-bYY.md` en GO (primera
  línea). Por nivel entran solo bloques en orden y sin huecos; un nivel entra
  solo si el anterior está completo (10 bloques). Encadena prerrequisitos
  (n1 → ru.f0.predstavlenie; cada clase → la anterior) y numera el orden global
  a continuación de lo ya publicado, con títulos del marco (curriculo/marco.json).
  Ids de clase `ru.nX.cYY`; módulo `ru.nX-bYY`.
- curso.json: se conservan sus metadatos y se rehacen los niveles nX y sus
  módulos. Al integrar N1 se fijan idiomasApoyo [es, en], vocabularioEstricto,
  reglasAutoria y palabrasLibres (unión con NOMBRES_LIBRES, sin Ecuador). Con
  N1 completo (10 bloques) se retira el nivel heredado a1-1 (estructura vieja
  f0, a1-1…c2 sin módulos).
- Sin bloques aprobados no escribe nada. Termina con `validar_ruta.py ru`.
- Versión esencial (`--esencial`, PLAN_SEMANA_IDIOMAS.md): la aprobación de
  cada bloque es pasar `tools/curriculo/validar_bloque.py ru N B` y
  `tools/ia/chequeos.py` con 0 errores (se comprueba antes de integrar), y la
  del f0, pasar `validar.py`; no se exigen archivos revision-*.md. Un nivel
  ya integrado no pasa otra vez por validar_bloque.py (lo rechaza): lo cubre
  el `validar_ruta.py ru` final. Los niveles que aún no existen no se
  declaran en curso.json: la app los muestra bloqueados («Próximamente»)
  y la prueba de ubicación nunca ubica por encima del último publicado.
  Desde el 13-10-2026 están integrados N1–N10: el ruso está completo (rom en
  todo texto ruso en N1–N4; desde N5, solo en el vocabulario).
- Ruso sin morfología inventada: `vocabularioEstricto` solo da por conocida una
  forma enseñada tal cual (con ё ≡ е y sin acento gráfico); las formas
  flexionadas van entre paréntesis en el vocablo («читать (читаю)»). No lleva
  `verbos.json`.

Uso: python3 tools/contenido/ruta-ru/integrar.py [--hasta N] [--seco] [--esencial]
     --hasta N:   integra solo hasta el nivel N
     --seco:      muestra qué integraría, sin escribir ni validar
     --esencial:  aprobación por validadores (ver arriba)
"""
import json
import pathlib
import re
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
IDIOMA = 'ru'
RUTA = RAIZ / f'assets/contenido/{IDIOMA}/ruta'
BLOQUES = 10
ULTIMA_F0 = 'ru.f0.predstavlenie'
HEREDADOS = ['ru.a1-1']  # nivel heredado (sin módulos) que se retira con N1 completo
# Además de lo prohibido, se retiran las palabras libres heredadas del curso.json viejo
# que no están en la lista cerrada de la ficha (nombres genéricos antiguos y el patronímico:
# no hay patronímicos antes de N5).
PROHIBIDAS = {'Quito', 'Ecuador', 'Guayaquil', 'Cuenca', 'Карлос', 'Лаура', 'Ивановна'}
# Listas cerradas de tools/ia/idiomas/ru.md (las mismas de validar.py): nombres de pila,
# apellidos masculinos y femeninos y ciudades. Sin Ecuador.
NOMBRES = ['Анна', 'Мария', 'Елена', 'Ольга', 'Наталья', 'Татьяна', 'Ирина', 'Светлана',
           'Иван', 'Александр', 'Дмитрий', 'Сергей', 'Андрей', 'Михаил', 'Максим']
APELLIDOS = ['Иванов', 'Иванова', 'Петров', 'Петрова', 'Смирнов', 'Смирнова', 'Кузнецов', 'Кузнецова',
             'Макаров', 'Макарова', 'Васильев', 'Васильева', 'Новиков', 'Новикова', 'Фёдоров', 'Фёдорова',
             'Михайлов', 'Михайлова', 'Павлов', 'Павлова']
CIUDADES = ['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск', 'Екатеринбург', 'Самара',
            'Краснодар', 'Сочи', 'Воронеж', 'Владивосток']
NOMBRES_LIBRES = list(dict.fromkeys(NOMBRES + APELLIDOS + CIUDADES))


def escribir(p, datos):
    p.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def f0_aprobado():
    r = AQUI / 'revision-f0.md'
    estado = next((l for l in r.read_text(encoding='utf-8').splitlines() if l.startswith('Estado:')), '') \
        if r.exists() else ''
    return re.search(r'\bGO\b', estado) is not None and 'NO-GO' not in estado


ESENCIAL = '--esencial' in sys.argv


def integrados():
    curso_p = RUTA / 'curso.json'
    curso = json.loads(curso_p.read_text(encoding='utf-8')) if curso_p.exists() else {}
    return {int(m[1]) for n in curso.get('niveles', []) if (m := re.fullmatch(r'n(\d+)', str(n.get('id'))))}


def validadores_ok(nv, b):
    """Versión esencial: el bloque pasa validar_bloque.py y chequeos.py sin errores."""
    cmds = [[sys.executable, str(RAIZ / 'tools/ia/chequeos.py'), str(AQUI / f'n{nv}-b{b:02d}.json')]]
    if nv not in integrados():
        cmds.insert(0, [sys.executable, str(RAIZ / 'tools/curriculo/validar_bloque.py'), IDIOMA, str(nv), str(b)])
    for cmd in cmds:
        r = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True)
        if r.returncode:
            print(f'N{nv} B{b}: {pathlib.Path(cmd[1]).name} falla\n{(r.stdout + r.stderr)[-1500:]}')
            return False
    return True


def aprobado(nv, b):
    if ESENCIAL:
        return validadores_ok(nv, b)
    r = AQUI / f'revision-n{nv}-b{b:02d}.md'
    return r.exists() and re.search(r'\bGO\b', r.read_text(encoding='utf-8').split('\n', 1)[0]) is not None


def curso_base():
    return {
        'esquema': 2, 'idioma': IDIOMA, 'version': '2026.10.0', 'revision': 'inicial',
        'idiomasApoyo': ['es', 'en'], 'apoyoPredeterminado': 'es',
        'vocabularioEstricto': True, 'reglasAutoria': True,
        'palabrasLibres': NOMBRES_LIBRES,
        'niveles': [
            {'id': 'f0', 'cefr': 'Pre-A1', 'nivelInterno': 0, 'estado': 'publicado',
             'titulo': {'es': 'Fundamentos', 'en': 'Foundations'}},
            {'id': 'c2', 'cefr': 'C2', 'nivelInterno': None, 'estado': 'planificado',
             'titulo': {'es': 'C2 · Maestría', 'en': 'C2 · Mastery'}},
        ],
        'modulos': [
            {'id': f'{IDIOMA}.f0', 'nivel': 'f0', 'archivo': 'f0.json',
             'titulo': {'es': 'Fundamentos: tus primeras frases en ruso',
                        'en': 'Foundations: your first sentences in Russian'}},
        ],
    }


def main():
    seco = '--seco' in sys.argv
    hasta = int(sys.argv[sys.argv.index('--hasta') + 1]) if '--hasta' in sys.argv else 10

    f0_nuevo = (AQUI / 'borrador-f0.json').exists() and (ESENCIAL or f0_aprobado())
    if f0_nuevo and (AQUI / 'validar.py').exists() and not seco:
        if subprocess.run([sys.executable, str(AQUI / 'validar.py')]).returncode:
            sys.exit('validar.py falla: no se integra.')
    f0_p = AQUI / 'borrador-f0.json' if f0_nuevo else RUTA / 'f0.json'
    f0 = json.loads(f0_p.read_text(encoding='utf-8'))

    marco = {n['nivel']: n for n in json.loads((RAIZ / 'curriculo/marco.json').read_text(encoding='utf-8'))['niveles']}
    niveles = []  # (nivel, [(bloque, datos)])
    for nv in range(1, hasta + 1):
        bloques = []
        for b in range(1, BLOQUES + 1):
            fuente = AQUI / f'n{nv}-b{b:02d}.json'
            if not fuente.exists() or not aprobado(nv, b):
                break
            bloques.append((b, json.loads(fuente.read_text(encoding='utf-8'))))
        if not bloques:
            break
        niveles.append((nv, bloques))
        if len(bloques) < BLOQUES:
            break

    print(f'F0: {"borrador aprobado" if f0_nuevo else "se conserva el publicado"} ({len(f0["unidades"])} unidades)')
    for nv, bloques in niveles:
        print(f'N{nv}: {len(bloques)} bloque(s), {sum(len(d["unidades"]) for _, d in bloques)} clases aprobadas')
    if not niveles and not f0_nuevo:
        print('Sin bloques aprobados (nX-bYY.json + revision-nX-bYY.md en GO): nada que integrar.')
        return
    n1_completo = any(nv == 1 and len(bl) == BLOQUES for nv, bl in niveles)
    if seco:
        print('[seco] no se escribe nada.' + (f' Se retirarían: {", ".join(HEREDADOS)}.' if n1_completo else ''))
        return

    RUTA.mkdir(parents=True, exist_ok=True)
    if f0_nuevo:
        escribir(RUTA / 'f0.json', f0)

    curso_p = RUTA / 'curso.json'
    curso = json.loads(curso_p.read_text(encoding='utf-8')) if curso_p.exists() else curso_base()
    if n1_completo:
        retirar = set(HEREDADOS)
        niveles_retirados = {m['nivel'] for m in curso['modulos'] if m['id'] in retirar}
        # El curso.json heredado declaraba el nivel a1-1 sin módulos: también se retira.
        niveles_retirados |= {h.split('.', 1)[1] for h in HEREDADOS}
        curso['modulos'] = [m for m in curso['modulos'] if m['id'] not in retirar]
        curso['niveles'] = [n for n in curso['niveles'] if n['id'] not in niveles_retirados]
    if f0_nuevo or niveles:
        # El curso.json heredado tenía f0 y c2 «planificados» con título solo {es}
        # y ningún módulo: se toman los de curso_base() (f0 publicado, apoyo {es, en}).
        base = curso_base()
        fijos = {n['id']: n for n in base['niveles']}
        curso['niveles'] = [fijos.get(n['id'], n) for n in curso['niveles']]
        if not any(m['id'] == f'{IDIOMA}.f0' for m in curso['modulos']):
            curso['modulos'].insert(0, base['modulos'][0])
    # El orden global sigue a todo lo publicado que no es nX (f0 y, mientras exista, el legado).
    orden = 1 + max(u['orden'] for u in f0['unidades'])
    for m in curso['modulos']:
        if m['id'] != f'{IDIOMA}.f0' and not re.match(rf'{IDIOMA}\.n\d+-b', m['id']) and (RUTA / m['archivo']).exists():
            orden = max(orden, 1 + max(u['orden'] for u in json.loads((RUTA / m['archivo']).read_text(encoding='utf-8'))['unidades']))

    anterior = ULTIMA_F0
    for nv, bloques in niveles:
        for b, datos in bloques:
            for u in datos['unidades']:
                u['prerequisitos'] = [anterior]
                u['orden'] = orden
                anterior = u['id']
                orden += 1
            datos['modulo'] = f'{IDIOMA}.n{nv}-b{b:02d}'
            escribir(RUTA / f'n{nv}-b{b:02d}.json', datos)

    if niveles:
        curso['idiomasApoyo'] = ['es', 'en']
        curso['vocabularioEstricto'] = True
        curso['reglasAutoria'] = True
        libres = [p for p in curso.get('palabrasLibres', []) if p not in PROHIBIDAS]
        curso['palabrasLibres'] = libres + [p for p in NOMBRES_LIBRES if p not in libres]
    curso['niveles'] = [n for n in curso['niveles'] if not re.fullmatch(r'n\d+', n['id'])]
    curso['modulos'] = [m for m in curso['modulos'] if not re.match(rf'{IDIOMA}\.n\d+-b', m['id'])]
    for nv, bloques in niveles:
        previo = 'f0' if nv == 1 else f'n{nv - 1}'
        i = next(k for k, n in enumerate(curso['niveles']) if n['id'] == previo) + 1
        curso['niveles'].insert(i, {
            'id': f'n{nv}', 'cefr': marco[nv]['cefr'], 'nivelInterno': nv, 'estado': 'publicado',
            'titulo': {'es': f'Nivel {nv} · {marco[nv]["cefr"]}', 'en': f'Level {nv} · {marco[nv]["cefr"]}'},
        })
        temas = {bl['bloque']: bl['tema'] for bl in marco[nv]['bloques']}
        for b, _ in bloques:
            curso['modulos'].append({
                'id': f'{IDIOMA}.n{nv}-b{b:02d}', 'nivel': f'n{nv}', 'archivo': f'n{nv}-b{b:02d}.json',
                'titulo': temas[b],
            })
    escribir(curso_p, curso)
    for nv, bloques in niveles:
        print(f'N{nv}: {len(bloques)} bloque(s) integrados')
    if n1_completo:
        print(f'Retirados de curso.json: {", ".join(HEREDADOS)}')
    sys.exit(subprocess.run([sys.executable, str(RAIZ / 'tools/validar_ruta.py'), IDIOMA]).returncode)


if __name__ == '__main__':
    main()
