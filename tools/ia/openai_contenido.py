#!/usr/bin/env python3
"""Producción masiva de contenido de cursos con la API de OpenAI (ver tools/ia/LEEME.md).

    python3 tools/ia/openai_contenido.py mapa    it 3            # claves gramaticales del nivel
    python3 tools/ia/openai_contenido.py outline it 3 [--bloques 1-10]
    python3 tools/ia/openai_contenido.py fichas  it 3 [--bloques 1-10]
    python3 tools/ia/openai_contenido.py plan    it 3            # versión esencial: plan = esqueleto, sin fichas
    python3 tools/ia/openai_contenido.py clases  it 3 2 [--clases 6-10] [--ligera]
    python3 tools/ia/openai_contenido.py revisar it 3 2
    python3 tools/ia/openai_contenido.py costos

Modo manual (`--manual` o IA_MANUAL=1): sin API. Cada llamada deja el encargo completo en
tools/ia/registro/manual/pendientes/<clave>.md y termina con código 3; el agente escribe el
JSON en registro/manual/respuestas/<clave>.json y repite el comando. El montaje, la validación
y el bucle de reparación son los mismos.

Reparto: el modelo escribe el contenido lingüístico; el programa pone ids, orden, claves,
repasos espaciados y prerrequisitos, valida con los validadores del repo y, si hay
errores, devuelve la lista al modelo (bucle de reparación, `--intentos`).
La clave de OpenAI se toma de OPENAI_API_KEY o de backend/.env y nunca se imprime.
"""
import argparse, json, os, re, subprocess, sys, time, urllib.error, urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import esquemas  # noqa: E402

R = Path(__file__).resolve().parents[2]
IA = R / 'tools' / 'ia'
REGISTRO = IA / 'registro' / 'costos.jsonl'
NOMBRES = {'it': 'italiano', 'ru': 'ruso', 'ko': 'coreano', 'ja': 'japonés', 'zh': 'chino mandarín'}
EXAMEN = {'it': 'CILS / CELI / PLIDA {cefr}', 'ru': 'TORFL (ТРКИ) {cefr}', 'ko': 'TOPIK {cefr}',
          'ja': 'JLPT {cefr}', 'zh': 'HSK 3.0 {cefr}'}
LIGERA = os.environ.get('IA_LIGERA') == '1'  # versión esencial: prompt clase_autor_ligera (ver PLAN_SEMANA_IDIOMAS.md)
NIVELES = {  # duración y extensión de la situación (como en los encargos de de/pt)
    1: 'N1 · A1 · 10–12 min · sonido del día · diálogo de 3–6 líneas',
    2: 'N2 · A2 · 12–15 min · diálogo o texto de 60–160 palabras',
    3: 'N3 · B1 · 15 min · 140–300 palabras', 4: 'N4 · B1 · 15 min · 140–300 palabras',
    5: 'N5 · B2 · 15–20 min · 290–560 palabras', 6: 'N6 · B2 · 15–20 min · 290–560 palabras',
    7: 'N7 · B2 · 15–20 min · 290–560 palabras',
    8: 'N8 · C1 · 20 min · 390–770 palabras', 9: 'N9 · C1 · 20 min · 390–770 palabras',
    10: 'N10 · C1 · 20 min · 390–770 palabras',
}
# USD por millón de tokens (entrada, entrada en caché, salida), tarifa estándar (Batch = la mitad).
PRECIOS = {
    'gpt-6-sol': (2.0, 0.2, 10.0), 'gpt-6-luna': (0.1, 0.01, 0.5), 'gpt-6-astra': (10.0, 1.0, 50.0),
    'gpt-5.6-sol': (4.0, 0.4, 20.0), 'gpt-5.6-terra': (2.0, 0.2, 12.0), 'gpt-5.6-luna': (0.2, 0.02, 1.2),
    'gpt-5.5': (5.0, 0.5, 30.0), 'gpt-5.4': (2.5, 0.25, 15.0), 'gpt-5.4-mini': (0.75, 0.075, 4.5),
    'gpt-5.4-nano': (0.2, 0.02, 1.25), 'gpt-5': (1.25, 0.125, 10.0), 'gpt-5-mini': (0.25, 0.025, 2.0),
    'gpt-4.1': (2.0, 0.5, 8.0), 'gpt-4.1-mini': (0.4, 0.1, 1.6),
}
AUTOR = os.environ.get('IA_MODELO_AUTOR', 'gpt-5.4-mini')
REVISOR = os.environ.get('IA_MODELO_REVISOR', 'gpt-6-sol')
PLANIFICADOR = os.environ.get('IA_MODELO_PLAN', 'gpt-6-sol')


def L(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def G(p, datos):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


# ---------------------------------------------------------------- OpenAI

def _clave():
    if os.environ.get('OPENAI_API_KEY'):
        return os.environ['OPENAI_API_KEY']
    for linea in (R / 'backend' / '.env').read_text(encoding='utf-8').splitlines():
        if linea.startswith('OPENAI_API_KEY='):
            return linea.split('=', 1)[1].strip().strip('"\'')
    sys.exit('Falta OPENAI_API_KEY')


ROM_ITEMS = re.compile(r'<!-- rom-items.*?<!-- /rom-items -->\n', re.S)
ROM_MARCAS = re.compile(r'<!-- /?rom-items[^>]*-->\n')


def prompt(nombre, idi):
    t = (IA / 'prompts' / f'{nombre}.md').read_text(encoding='utf-8')
    # Bloque <!-- rom-items --> (romanización de los ítems): solo para ru, ko, ja y zh; en los
    # idiomas de escritura latina se quita entero y el prompt queda como antes.
    t = ROM_MARCAS.sub('', t) if idi in esquemas.NO_LATINOS else ROM_ITEMS.sub('', t)
    return (t.replace('{FICHA_IDIOMA}', (IA / 'idiomas' / f'{idi}.md').read_text(encoding='utf-8'))
             .replace('{IDIOMA_NOMBRE}', NOMBRES[idi]))


ESFUERZO = {'mapa': 'high', 'outline': 'medium', 'fichas': 'low', 'clase': 'low', 'reparacion': 'low', 'revision': 'medium'}
ESFUERZO_FORZADO = None


MANUAL = os.environ.get('IA_MANUAL') == '1'
MANUAL_DIR = IA / 'registro' / 'manual'


class Pendiente(Exception):
    """Modo manual: el encargo quedó escrito y falta la respuesta del agente que hace de modelo."""


def errores_esquema(x, e, ruta='$'):
    """Validación del subconjunto de JSON Schema que usa esquemas.py (lo que en la API garantiza `strict`)."""
    if 'anyOf' in e:
        intentos = [errores_esquema(x, rama, ruta) for rama in e['anyOf']]
        return [] if any(not r for r in intentos) else min(intentos, key=len)
    tipo = e.get('type')
    ok = {'object': isinstance(x, dict), 'array': isinstance(x, list), 'string': isinstance(x, str), 'null': x is None,
          'integer': isinstance(x, int) and not isinstance(x, bool), 'boolean': isinstance(x, bool)}.get(tipo, True)
    if not ok:
        return [f'{ruta}: se esperaba {tipo}']
    if 'enum' in e and x not in e['enum']:
        return [f'{ruta}: valor {x!r} fuera de {e["enum"]}']
    out = []
    if tipo == 'object':
        out += [f'{ruta}: falta «{k}»' for k in e.get('required', []) if k not in x]
        out += [f'{ruta}: sobra «{k}»' for k in x if k not in e.get('properties', {})]
        for k, sub in e.get('properties', {}).items():
            if k in x: out += errores_esquema(x[k], sub, f'{ruta}.{k}')
    if tipo == 'array':
        for i, v in enumerate(x): out += errores_esquema(v, e['items'], f'{ruta}[{i}]')
    return out


def llamar_manual(instrucciones, entrada, esquema, etapa, objetivo):
    """El encargo se escribe en registro/manual/pendientes/<clave>.md; la respuesta se lee de respuestas/<clave>.json."""
    import hashlib
    clave = f'{objetivo}.{etapa}.' + hashlib.sha1((instrucciones + entrada).encode()).hexdigest()[:8]
    pend, resp = MANUAL_DIR / 'pendientes' / f'{clave}.md', MANUAL_DIR / 'respuestas' / f'{clave}.json'
    problemas = []
    if resp.exists():
        try:
            datos = json.loads(resp.read_text(encoding='utf-8'))
            problemas = errores_esquema(datos, esquema)
        except json.JSONDecodeError as ex:
            problemas = [f'JSON inválido: {ex}']
        if not problemas:
            pend.unlink(missing_ok=True)
            return datos
    for viejo in (MANUAL_DIR / 'pendientes').glob(f'{objetivo}.{etapa}.*.md'):
        viejo.unlink()  # encargos anteriores del mismo objetivo que ya no aplican
    pend.parent.mkdir(parents=True, exist_ok=True)
    resp.parent.mkdir(parents=True, exist_ok=True)
    pend.write_text(
        f'# ENCARGO {clave}\n\nEscribe tu respuesta (SOLO el objeto JSON, sin texto alrededor) en:\n'
        f'`{resp.relative_to(R)}`\n\nDespués vuelve a ejecutar el mismo comando.\n'
        + ('\n## TU RESPUESTA NO CUMPLE EL ESQUEMA (corrígela)\n- ' + '\n- '.join(problemas[:30]) + '\n' if problemas else '')
        + f'\n---\n\n# INSTRUCCIONES\n\n{instrucciones}\n\n---\n\n# ENTRADA\n\n{entrada}\n\n---\n\n'
        f'# ESQUEMA DE SALIDA (obligatorio: todos los campos; lo opcional va como null)\n\n```json\n{json.dumps(esquema, ensure_ascii=False)}\n```\n',
        encoding='utf-8')
    raise Pendiente(str(pend.relative_to(R)))


def llamar(modelo, instrucciones, entrada, esquema, nombre, etapa, objetivo, esfuerzo=None):
    """Una llamada a /v1/responses con salida JSON estricta. Devuelve el objeto ya parseado."""
    if MANUAL:
        return llamar_manual(instrucciones, entrada, esquema, etapa, objetivo)
    cuerpo = {'model': modelo, 'instructions': instrucciones, 'input': entrada, 'max_output_tokens': 64000,
              'text': {'format': {'type': 'json_schema', 'name': nombre, 'schema': esquema, 'strict': True}}}
    if re.match(r'(gpt-5|gpt-6|o\d)', modelo):
        cuerpo['reasoning'] = {'effort': ESFUERZO_FORZADO or esfuerzo or ESFUERZO.get(etapa, 'low')}
    peticion = urllib.request.Request('https://api.openai.com/v1/responses', data=json.dumps(cuerpo).encode(),
                                      headers={'Authorization': f'Bearer {_clave()}', 'Content-Type': 'application/json'})
    for intento in range(6):
        try:
            with urllib.request.urlopen(peticion, timeout=900) as r:
                resp = json.load(r)
            break
        except urllib.error.HTTPError as e:
            detalle = e.read().decode(errors='replace')[:400]
            if e.code in (429, 500, 502, 503, 504) and intento < 5:
                time.sleep(15 * (intento + 1)); continue
            sys.exit(f'OpenAI {e.code}: {detalle}')
        except (urllib.error.URLError, TimeoutError):
            if intento < 5:
                time.sleep(15 * (intento + 1)); continue
            raise
    u = resp.get('usage') or {}
    ent, cache = u.get('input_tokens', 0), (u.get('input_tokens_details') or {}).get('cached_tokens', 0)
    sal = u.get('output_tokens', 0)
    p = PRECIOS.get(modelo, (0, 0, 0))
    usd = ((ent - cache) * p[0] + cache * p[1] + sal * p[2]) / 1e6
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRO.open('a', encoding='utf-8') as f:
        f.write(json.dumps({'fecha': datetime.now().isoformat(timespec='seconds'), 'etapa': etapa, 'objetivo': objetivo,
                            'modelo': resp.get('model', modelo), 'entrada': ent, 'cache': cache, 'salida': sal,
                            'razonamiento': (u.get('output_tokens_details') or {}).get('reasoning_tokens', 0),
                            'usd': round(usd, 5)}) + '\n')
    if resp.get('status') != 'completed':
        raise RuntimeError(f'respuesta {resp.get("status")}: {resp.get("incomplete_details")}')
    texto = ''.join(c.get('text', '') for o in resp.get('output', []) if o.get('type') == 'message'
                    for c in o.get('content', []) if c.get('type') == 'output_text')
    return json.loads(texto)


def sin_nulos(x):
    if isinstance(x, dict):
        return {k: sin_nulos(v) for k, v in x.items() if v is not None}
    if isinstance(x, list):
        return [sin_nulos(v) for v in x]
    return x


# ---------------------------------------------------------------- planificación

def rango(txt, total):
    if not txt:
        return list(range(1, total + 1))
    a, _, b = txt.partition('-')
    return list(range(int(a), int(b or a) + 1))


def claves_previas(idi, n):
    """Claves disponibles al cerrar N{n-1}: previos del nivel anterior + lo que introduce."""
    if n == 1:  # Nivel 0 + Fundamentos (lo mismo que exige validar_outline_n1.py)
        f0 = L(R / 'curriculo' / idi / 'f0.json')
        return f0.get('previos', []) + f0.get('clavesSalida', [])
    # Desde los mapas aprobados (completos desde el principio): así los niveles se planifican en paralelo.
    claves = claves_previas(idi, 1)
    for m in range(1, n):
        mapa = R / 'tools' / 'curriculo' / idi / f'mapa-n{m}.json'
        if mapa.exists():
            claves += [k['clave'] for k in L(mapa)['claves'] if k['clave'] not in claves]
        else:
            p = R / 'curriculo' / idi / f'n{m}.json'
            prev = L(p if p.exists() else R / 'tools' / 'curriculo' / idi / f'n{m}-outline.json')
            claves += [k for c in prev['clases'] for k in c.get('introduce', []) if k not in claves]
    return claves


def cmd_mapa(a):
    idi, n = a.idioma, a.nivel
    marco = next(x for x in L(R / 'curriculo' / 'marco.json')['niveles'] if x['nivel'] == n)
    fr = L(R / 'curriculo' / 'fr' / f'n{n}.json')
    ref = [{'clase': c['id'].split('.')[-1], 'introduce': c.get('introduce'), 'gramatica': c.get('gramatica', [])[:3]}
           for c in fr['clases']]
    cubierto = claves_previas(idi, 1) + [k for m in range(1, n) for k in (x['clave'] for x in L(R / 'tools' / 'curriculo' / idi / f'mapa-n{m}.json')['claves'])]
    total = 49 if n == 1 else 48
    entrada = (f'NIVEL: N{n} ({marco["cefr"]}). Escribe exactamente {total} claves (c01–c{total:02d}).\n\n'
               f'MARCO:\n{json.dumps(marco, ensure_ascii=False)}\n\nREFERENCIA (francés N{n}):\n'
               f'{json.dumps(ref, ensure_ascii=False)}\n\nYA CUBIERTO ({len(cubierto)}):\n{", ".join(cubierto)}\n(Las primeras {len(claves_previas(idi, 1))} son Nivel 0 y Fundamentos: el alumno ya las domina; N1 parte de ahí.)')
    salida = R / 'tools' / 'curriculo' / idi / f'mapa-n{n}.json'
    for intento in range(a.intentos + 1):
        datos = llamar(a.modelo or PLANIFICADOR, prompt('mapa_claves', idi), entrada, esquemas.MAPA, 'mapa', 'mapa', f'{idi}.n{n}')
        cl = datos['claves']
        errores = []
        if len(cl) != total: errores.append(f'hay {len(cl)} claves, se piden {total}')
        dup = {k['clave'] for k in cl if [x['clave'] for x in cl].count(k['clave']) > 1} | {k['clave'] for k in cl if k['clave'] in cubierto}
        if dup: errores.append(f'claves repetidas o ya cubiertas: {", ".join(sorted(dup))}')
        malas = [k['clave'] for k in cl if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', k['clave'])]
        if malas: errores.append(f'formato de clave inválido: {", ".join(malas)}')
        if not errores: break
        entrada += '\n\nERRORES de tu versión anterior (corrígelos todos):\n- ' + '\n- '.join(errores)
    G(salida, datos)
    print(f'{salida.relative_to(R)}: {len(cl)} claves' + (f' · SIN RESOLVER: {errores}' if errores else ' · 0 errores'))


def recicla_de(i, intro, previas_nivel):
    """Repaso espaciado mecánico: +1, +2, +7 y una clave del nivel anterior (lo que exige validar_outline_nivel)."""
    r = [intro[j] for j in (i - 1, i - 2, i - 7) if j in intro]
    if previas_nivel:
        r.append(previas_nivel[(i * 7) % len(previas_nivel)])
    if i == 50:  # la prueba repasa el nivel
        r += [intro[j] for j in range(1, 49, 6) if j in intro and intro[j] not in r]
    return list(dict.fromkeys(r))


def cmd_outline(a):
    idi, n = a.idioma, a.nivel
    marco = next(x for x in L(R / 'curriculo' / 'marco.json')['niveles'] if x['nivel'] == n)
    mapa = {int(k['clase'][1:]): k for k in L(R / 'tools' / 'curriculo' / idi / f'mapa-n{n}.json')['claves']}
    intro = {i: k['clave'] for i, k in mapa.items()}
    previos = claves_previas(idi, n)
    del_anterior = previos[-48:]
    destino = R / 'tools' / 'curriculo' / idi / f'n{n}-outline.json'
    datos = L(destino) if destino.exists() else {
        'idioma': idi, 'nivel': n, 'cefr': marco['cefr'],
        'nota': {'es': f'Esqueleto N{n} ({marco["cefr"]}). Método ligero: cada clase es una situación autónoma con nombres genéricos; 48 claves nuevas, c49 proyecto y c50 prueba. Repaso a +1, +2 y +7.',
                 'en': f'N{n} skeleton ({marco["cefr"]}). Light method: each class is a self-contained situation with generic names; 48 new keys, c49 project and c50 test. Review at +1, +2 and +7.'},
        'previos': previos, 'clases': []}
    por_id = {c['id']: c for c in datos['clases']}
    cat = {x['id']: x['nombre'] for x in L(R / 'assets' / 'contenido' / 'situaciones' / 'catalogo.json')['situaciones']}
    for b in rango(a.bloques, 10):
        bm = next(x for x in marco['bloques'] if x['bloque'] == b)
        ids = range((b - 1) * 5 + 1, b * 5 + 1)
        if not a.rehacer and all(f'{idi}.n{n}.c{i:02d}' in por_id for i in ids):
            continue  # bloque ya planificado: no se rehace (--rehacer para forzarlo)
        claves = [mapa.get(i, {'clase': f'c{i:02d}', 'clave': '(proyecto del nivel)' if i == 49 else '(prueba del nivel: repaso, sin clave nueva)'}) for i in ids]
        usados = [c['titulo']['es'] for c in por_id.values()]
        vocab = sorted({w for c in por_id.values() for w in c['vocabulario']['palabras']})
        entrada = (f'NIVEL: {NIVELES[n]}\nBLOQUE {b}: {json.dumps(bm, ensure_ascii=False)}\n'
                   f'SITUACIONES PERMITIDAS (id: descripción): {json.dumps({i: cat.get(i, "?") for i in bm["situaciones"]}, ensure_ascii=False)}\n\nCLAVES DEL BLOQUE:\n{json.dumps(claves, ensure_ascii=False)}\n\n'
                   f'TÍTULOS YA USADOS: {usados}\n\nVOCABULARIO YA PLANIFICADO: {", ".join(vocab)}')
        for intento in range(a.intentos + 1):
            out = llamar(a.modelo or PLANIFICADOR, prompt('outline_nivel', idi), entrada, esquemas.OUTLINE, 'outline', 'outline', f'{idi}.n{n}.b{b}')
            errores = []
            if [c['clase'] for c in out['clases']] != [f'c{i:02d}' for i in ids]:
                errores.append(f'las clases deben ser exactamente {[f"c{i:02d}" for i in ids]}')
            for c in out['clases']:
                if c['situacion'] not in bm['situaciones']:
                    errores.append(f'{c["clase"]}: situación {c["situacion"]} fuera de {bm["situaciones"]}')
                if not 6 <= len(c['vocabulario']['palabras']) <= 12:
                    errores.append(f'{c["clase"]}: vocabulario con {len(c["vocabulario"]["palabras"])} palabras (6–12)')
            if not errores: break
            entrada += '\n\nERRORES de tu versión anterior (corrígelos todos):\n- ' + '\n- '.join(errores)
        for i, c in zip(ids, out['clases']):
            cid = f'{idi}.n{n}.c{i:02d}'
            por_id[cid] = {'id': cid, 'bloque': b, 'titulo': c['titulo'], 'objetivo': c['objetivo'], 'gramatica': c['gramatica'],
                           'introduce': [intro[i]] if i in intro else [], 'recicla': recicla_de(i, intro, del_anterior),
                           'vocabulario': c['vocabulario'], 'sonido': c['sonido'], 'situacion': c['situacion'],
                           'tarea': c['tarea'], 'estado': 'esqueleto'}
        datos['clases'] = [por_id[k] for k in sorted(por_id)]
        G(destino, datos)
        print(f'{destino.relative_to(R)}: bloque {b}' + (f' · SIN RESOLVER: {errores}' if errores else ''))
    if len(datos['clases']) == 50:
        subprocess.run(['python3', 'tools/curriculo/validar_outline_n1.py' if n == 1 else 'tools/curriculo/validar_outline_nivel.py', idi]
                       + ([] if n == 1 else [str(n)]), cwd=R)


def validar_plan(idi, n):
    r = subprocess.run(['python3', 'tools/curriculo/validar_plan_detallado.py', idi, f'curriculo/{idi}/n{n}.json', '--parcial'],
                       cwd=R, capture_output=True, text=True)
    return [l for l in (r.stdout + r.stderr).splitlines() if 'ERROR' in l or 'error' in l.lower() and idi + '.n' in l]


# Mensajes del validador → instrucción concreta para el modelo (sin esto repite el mismo fallo).
EXPLICA = {
    'no coincide con ninguna opción': 'tras «→» va el TEXTO EXACTO de una de las opciones, no la letra',
    'inventa elementos': 'en relacionar, la solución usa exactamente los mismos elementos que el estímulo; solo cambian las parejas',
    'ya entrega la respuesta': 'el estímulo de escribir no puede contener la respuesta: descríbela en español',
    'repite estímulo/respuesta': 'cada ítem de la clase usa una frase distinta: cambia estímulo y respuesta',
    'sin dos opciones reales': 'da al menos dos opciones distintas, una sola correcta',
    'repetidos': 'hay ejemplos repetidos en el nivel: cambia la frase de los ítems repetidos',
    'demasiado vaga': 'la situación necesita un diálogo o datos concretos (nombres, lugar, horas, cifras), no una descripción general',
    'clave no disponible': 'la clave del ítem debe estar en introduce o recicla de ESA clase; cambia la clave o el ítem',
}


def explicar(linea):
    return linea + ''.join(f' ⇒ {v}' for k, v in EXPLICA.items() if k in linea)


def mezclar_ordenar(ej):
    """Los tokens de ordenar salen de la solución (palabras sin puntuación, en orden rotado)."""
    for e in ([*ej['guiada'], *ej['independiente'], *ej['evaluacion'], *ej['situacion']['preguntas']]):
        if e['formato'] != 'ordenar' or '→' not in e['ejemplo']:
            continue
        sol = e['ejemplo'].split('→', 1)[1].strip()
        w = re.sub(r'[.,!?¿¡;:«»"]', ' ', sol).split()
        if len(w) >= 3:
            mezcla = w[len(w) // 2:][::-1] + w[:len(w) // 2]
            e['ejemplo'] = '[' + ' / '.join(mezcla) + '] → ' + sol


def mezclar_relacionar(ej):
    """El modelo da los pares correctos; el estímulo mezclado lo construye el código (lado derecho rotado)."""
    for e in ([*ej['guiada'], *ej['independiente'], *ej['evaluacion'], *ej['situacion']['preguntas']]):
        if e['formato'] != 'relacionar' or '→' not in e['ejemplo']:
            continue
        sol = e['ejemplo'].split('→', 1)[1].strip().rstrip(';')
        pares = [p.split('↔', 1) for p in sol.split(';') if '↔' in p]
        if len(pares) < 3:
            continue
        izq, der = [x.strip() for x, _ in pares], [y.strip() for _, y in pares]
        mezcla = der[1:] + der[:1]
        e['ejemplo'] = '; '.join(f'{x}↔{y}' for x, y in zip(izq, mezcla)) + ' → ' + '; '.join(f'{x}↔{y}' for x, y in zip(izq, der))


def repetidos(datos, fichas):
    """Localiza los ejemplos repetidos del nivel en las clases del bloque (el validador solo da el total)."""
    vistos, out = {}, []
    for c in datos['clases']:
        ej = c.get('ejercicios') or {}
        items = [(f'{s}[{i}]', e) for s in ('guiada', 'independiente', 'evaluacion') for i, e in enumerate(ej.get(s, []), 1)]
        items += [(f'situacion[{i}]', e) for i, e in enumerate((ej.get('situacion') or {}).get('preguntas', []), 1)]
        for donde, e in items:
            k = re.sub(r'\W+', ' ', e['ejemplo'].lower()).strip()
            if k in vistos and c in fichas:
                out.append(f'{c["id"]}.{donde}: ejemplo repetido (ya está en {vistos[k]}) ⇒ escribe otra frase distinta')
            vistos.setdefault(k, f'{c["id"]}.{donde}')
    return out


def cmd_fichas(a):
    idi, n = a.idioma, a.nivel
    out_p = R / 'tools' / 'curriculo' / idi / f'n{n}-outline.json'
    destino = R / 'curriculo' / idi / f'n{n}.json'
    outline = L(out_p)
    marco = next(x for x in L(R / 'curriculo' / 'marco.json')['niveles'] if x['nivel'] == n)
    datos = L(destino) if destino.exists() else {
        'idioma': idi, 'nivel': n, 'cefr': outline['cefr'], 'examen': EXAMEN[idi].format(cefr=marco['cefr']),
        'nota': outline['nota'], 'previos': outline['previos'], 'clases': []}
    # Las clases del esqueleto que aún no están en el plan se incorporan (el plan crece bloque a bloque).
    ya = {c['id'] for c in datos['clases']}
    datos['clases'] = sorted(datos['clases'] + [dict(c) for c in outline['clases'] if c['id'] not in ya], key=lambda c: c['id'])
    for b in rango(a.bloques, 10):
        if not any(c['bloque'] == b for c in datos['clases']):
            print(f'bloque {b}: sin esqueleto (ejecuta antes «outline {idi} {n} --bloques {b}»)'); continue
        fichas = [c for c in datos['clases'] if c['bloque'] == b]
        usados = [e['ejemplo'] for c in datos['clases'] if c.get('ejercicios') and c['bloque'] != b
                  for s in ('guiada', 'independiente', 'evaluacion') for e in c['ejercicios'][s]]
        base = [{k: v for k, v in c.items() if k not in ('ejercicios', 'estado')} for c in fichas]
        entrada = f'NIVEL: {NIVELES[n]}\n\nFICHAS ESQUELETO:\n{json.dumps(base, ensure_ascii=False)}\n\nEJEMPLOS YA USADOS: {json.dumps(usados[-400:], ensure_ascii=False)}'
        con_error = None
        if all(c.get('ejercicios') for c in fichas) and not a.rehacer:
            errores = [explicar(l) for l in validar_plan(idi, n) if any(c['id'] in l for c in fichas)] + repetidos(datos, fichas)
            con_error = {c['id'] for c in fichas if any(c['id'] + '.' in l or c['id'] + ':' in l for l in errores)}
            if not errores:
                print(f'{destino.relative_to(R)}: bloque {b} ya planificado · 0 errores'); continue
            entrada += (f'\n\nVERSIÓN ACTUAL (planificada): {json.dumps([{"id": c["id"], "ejercicios": c["ejercicios"]} for c in fichas], ensure_ascii=False)}'
                        '\n\nERRORES (corrígelos todos; devuelve las 5 fichas):\n- ' + '\n- '.join(errores))
        for intento in range(a.intentos + 1):
            if intento == 0 and con_error is not None:
                intento = 1  # ya hay versión: se entra directamente en modo reparación
            out = llamar(a.modelo or AUTOR, prompt('fichas', idi), entrada, esquemas.FICHAS, 'fichas', 'fichas', f'{idi}.n{n}.b{b}')
            por = {f['id']: f['ejercicios'] for f in out['fichas']}
            for c in fichas:
                # En las reparaciones solo se sustituyen las clases que tenían errores.
                if c['id'] in por and (intento == 0 or c['id'] in con_error):
                    mezclar_relacionar(por[c['id']]); mezclar_ordenar(por[c['id']])
                    c['ejercicios'], c['estado'] = por[c['id']], 'planificado'
            G(destino, datos)
            errores = [explicar(l) for l in validar_plan(idi, n) if any(c['id'] in l for c in fichas)]
            errores += repetidos(datos, fichas) if any('repetid' in l for l in validar_plan(idi, n)) else []
            con_error = {c['id'] for c in fichas if any(c['id'] + '.' in l or c['id'] + ':' in l for l in errores)}
            if errores and not con_error:  # errores de raíz sin clase concreta: se rehace el bloque
                con_error = {c['id'] for c in fichas}
            if not errores: break
            entrada += '\n\nERRORES del validador en tu versión anterior (corrígelos todos):\n- ' + '\n- '.join(errores)
        print(f'{destino.relative_to(R)}: bloque {b} · {len(errores)} error(es)' + ('\n  ' + '\n  '.join(errores[:10]) if errores else ''))


def cmd_plan(a):
    """Versión esencial: el plan del nivel es el esqueleto tal cual, sin plan de ejercicios (sin modelo)."""
    idi, n = a.idioma, a.nivel
    outline = L(R / 'tools' / 'curriculo' / idi / f'n{n}-outline.json')
    destino = R / 'curriculo' / idi / f'n{n}.json'
    marco = next(x for x in L(R / 'curriculo' / 'marco.json')['niveles'] if x['nivel'] == n)
    datos = L(destino) if destino.exists() else {
        'idioma': idi, 'nivel': n, 'cefr': outline['cefr'], 'examen': EXAMEN[idi].format(cefr=marco['cefr']),
        'nota': outline['nota'], 'previos': outline['previos'], 'clases': []}
    # Las clases sin plan de ejercicios se copian del esqueleto (también si este se corrigió después).
    con_fichas = {c['id']: c for c in datos['clases'] if c.get('ejercicios')}
    datos['clases'] = sorted(list(con_fichas.values()) + [dict(c) for c in outline['clases'] if c['id'] not in con_fichas],
                             key=lambda c: c['id'])
    G(destino, datos)
    print(f'{destino.relative_to(R)}: {len(datos["clases"])} clases en el plan')


# ---------------------------------------------------------------- clases

def ya_ensenado(idi, n, hasta_cid):
    """Palabras que el alumno ya vio: Fundamentos, vocabulario de las fichas anteriores y
    pasos de enseñanza de los borradores anteriores, en orden de aparición."""
    vistos = {}
    f0 = f0_de(idi)
    fuentes = []
    if f0.exists():
        fuentes += L(f0).get('unidades', [])
    # Igual que validar_bloque.py: de una clase ya escrita cuenta lo que enseña de verdad; de una clase
    # aún sin escribir, el vocabulario de su ficha (su esbozo).
    escritas = set()
    for k in range(1, n + 1):
        for j in range(1, 11):
            p = R / 'tools' / 'contenido' / f'ruta-{idi}' / f'n{k}-b{j:02d}.json'
            # Como validar_bloque.py: un bloque ajeno a medio escribir cuenta como esbozo (su ficha), no
            # por lo que ya tenga escrito; el bloque propio cuenta con sus clases anteriores reales.
            propio = k == n and any(c['id'] == hasta_cid for c in L(R / 'curriculo' / idi / f'n{k}.json')['clases'] if c['bloque'] == j)
            if p.exists() and (propio or len(L(p)['unidades']) == 5):
                us = [u for u in L(p)['unidades'] if (k, u['id']) < (n, hasta_cid)]
                fuentes += us
                escritas |= {u['id'] for u in us}
    for k in range(1, n + 1):
        cur = R / 'curriculo' / idi / f'n{k}.json'
        if not cur.exists(): continue
        for c in L(cur)['clases']:
            if c['id'] >= hasta_cid and k == n: break
            if c['id'] in escritas: continue
            for w in c.get('vocabulario', {}).get('palabras', []): vistos.setdefault(w, 1)
    for u in fuentes:
        for v in u.get('vocabulario', []): vistos.setdefault(v.get('texto', ''), 1)
        for p in u.get('pasos', []):
            if p.get('tipo') == 'ejemplos':
                for e in p.get('items', []): vistos.setdefault(e.get('texto', ''), 1)
            if p.get('tipo') == 'tabla':
                for fila in p.get('filas', []):
                    for celda in fila:
                        if isinstance(celda, dict) and celda.get('texto'): vistos.setdefault(celda['texto'], 1)
    palabras = {}
    for t in vistos:
        for w in re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)?|[^\W\d_]+'", t):
            palabras.setdefault(w.lower(), 1)
    return ' '.join(palabras)


def montar(idi, n, cid, ficha, crudo, cefr, prerequisito):
    """Clase del modelo → unidad de la app (ids, orden, claves y enlaces los pone el programa)."""
    c = sin_nulos(crudo)
    vocab = [dict(v, id=f'v{i}') for i, v in enumerate(c['vocabulario'], 1)]
    pref = {'practica_guiada': 'g', 'practica_independiente': 'i', 'situacion': 's', 'evaluacion': 'e'}
    # Orden que exige la app: enseñar → guiada → independiente → situación → evaluación.
    rango_paso = {'explicacion': 0, 'vocabulario': 1, 'ejemplos': 2, 'tabla': 3, 'practica_guiada': 4,
                  'practica_independiente': 5, 'situacion': 6, 'evaluacion': 7}
    c['pasos'] = sorted(c['pasos'], key=lambda p: rango_paso.get(p['tipo'], 3))
    pasos = []
    for i, p in enumerate(c['pasos'], 1):
        p = dict(p)
        if p['tipo'] == 'vocabulario':
            p['refs'] = [v['id'] for v in vocab]
        if p['tipo'] in pref:
            items = []
            for j, it in enumerate(p['items'], 1):
                it = dict(it, id=f'{pref[p["tipo"]]}{j}')
                if p['tipo'] != 'practica_guiada':
                    it.pop('pista', None)  # la app solo admite pista en la práctica guiada
                if it['formato'] == 'relacionar':
                    it['pares'] = [[x['izquierda'], x['derecha']] for x in it['pares']]
                if it['formato'] == 'escribir' and not it.get('abierta'):
                    for k in ('abierta', 'minimoPalabras', 'maximoPalabras'): it.pop(k, None)
                for k in ('textoRom', 'opcionesRom', 'tokensRom', 'paresRom'):  # romanización (ru, ko, ja, zh)
                    if k in it and not (any(it[k]) if isinstance(it[k], list) else it[k]):
                        it.pop(k)  # se conserva salvo si va vacía
                items.append(it)
            p['items'] = items
        p['id'] = f'p{i}'
        pasos.append(p)
    i = int(cid.split('.c')[1])
    clave = ficha.get('introduce') or []
    return {
        'id': cid, 'orden': 100 * n + i, 'titulo': ficha['titulo'], 'objetivo': ficha['objetivo'],
        'cefr': cefr, 'nivelInterno': n, 'concepto': clave[0] if clave else f'review-n{n}',
        'prerequisitos': [prerequisito],
        'habilidades': habilidades_de(pasos, n),
        'gramatica': [f'{idi}-g-{k}' for k in clave], 'vocabulario': vocab,
        'erroresFrecuentes': c['erroresFrecuentes'], 'pasos': pasos, 'criterioDominio': {'umbral': 0.8},
    }


def habilidades_de(pasos, n):
    """Solo las habilidades con evidencia en la clase (validar_ruta.py exige evidencia de gramática,
    vocabulario, lectura y escritura; la versión esencial puede no tener todas)."""
    tipos = {p['tipo'] for p in pasos}
    formatos = {it.get('formato') for p in pasos for it in p.get('items', []) if isinstance(it, dict)}
    h = ['vocabulario'] if 'vocabulario' in tipos else []
    if tipos & {'explicacion', 'tabla'}: h.append('gramatica')
    if 'situacion' in tipos: h.append('lectura')
    if 'escuchar' in formatos: h.append('escucha')
    if 'tabla' in tipos or formatos & {'escribir', 'ordenar', 'completar'}: h.append('escritura')
    return h + ['conversacion'] + (['pronunciacion'] if n == 1 else [])


def prerequisito_de(idi, n, i):
    if i > 1:
        return f'{idi}.n{n}.c{i - 1:02d}'
    if n > 1:
        return f'{idi}.n{n - 1}.c50'
    return L(f0_de(idi))['unidades'][-1]['id']


def f0_de(idi):
    """Fundamentos: el borrador nuevo si existe (aún sin integrar), si no el publicado."""
    b = R / 'tools' / 'contenido' / f'ruta-{idi}' / 'borrador-f0.json'
    return b if b.exists() else R / 'assets' / 'contenido' / idi / 'ruta' / 'f0.json'


def guardar_unidad(idi, n, b, unidad):
    p = R / 'tools' / 'contenido' / f'ruta-{idi}' / f'n{n}-b{b:02d}.json'
    datos = L(p) if p.exists() else {'modulo': f'{idi}.n{n}-b{b:02d}', 'unidades': []}
    datos['unidades'] = sorted([u for u in datos['unidades'] if u['id'] != unidad['id']] + [unidad], key=lambda u: u['orden'])
    G(p, datos)
    return p


def errores_de(idi, n, b, cid):
    r = subprocess.run(['python3', 'tools/curriculo/validar_bloque.py', idi, str(n), str(b)], cwd=R, capture_output=True, text=True)
    lineas = [l for l in (r.stdout + r.stderr).splitlines() if cid in l or 'falló' in l or 'Traceback' in l]
    p = R / 'tools' / 'contenido' / f'ruta-{idi}' / f'n{n}-b{b:02d}.json'
    q = subprocess.run(['python3', 'tools/ia/chequeos.py', str(p), '--clase', cid], cwd=R, capture_output=True, text=True)
    return lineas + [l for l in q.stdout.splitlines() if l.startswith('ERROR')]


def contexto_clase(idi, n, ficha, cid, formatos):
    return (f'NIVEL: {NIVELES[n]}\n\nFICHA:\n{json.dumps(ficha, ensure_ascii=False)}\n\n'
            f'FORMATOS YA USADOS EN EL BLOQUE: {", ".join(formatos) or "(ninguno: es la primera clase)"}\n\n'
            f'YA ENSEÑADO:\n{ya_ensenado(idi, n, cid)}')


def escribir_clase(a, idi, n, b, ficha, cefr, formatos, crudo=None, errores=None):
    cid = ficha['id']
    guardado = IA / 'registro' / 'crudo' / idi / f'{cid}.json'
    if crudo is None and guardado.exists() and not a.rehacer:  # reanudar: se remonta y solo se repara
        crudo = L(guardado)
        guardar_unidad(idi, n, b, montar(idi, n, cid, ficha, crudo, cefr, prerequisito_de(idi, n, int(cid.split('.c')[1]))))
        errores = errores_de(idi, n, b, cid)
    base = contexto_clase(idi, n, ficha, cid, formatos)
    entrada = base
    for intento in range(a.intentos + 1):
        if crudo is not None and errores:
            entrada = (base + f'\n\nTU VERSIÓN ANTERIOR:\n{json.dumps(crudo, ensure_ascii=False)}\n\n'
                       'ERRORES (corrígelos todos sin crear otros; devuelve la clase completa):\n- ' + '\n- '.join(errores[:40]))
        elif crudo is not None and not errores:
            break
        crudo = llamar(a.modelo or AUTOR, prompt('clase_autor_ligera' if LIGERA else 'clase_autor', idi), entrada, esquemas.clase(idi), 'clase',
                       'clase' if intento == 0 and not errores else 'reparacion', cid)
        guardar_unidad(idi, n, b, montar(idi, n, cid, ficha, crudo, cefr, prerequisito_de(idi, n, int(cid.split('.c')[1]))))
        errores = errores_de(idi, n, b, cid)
        if not errores: break
    crudos = IA / 'registro' / 'crudo' / idi
    G(crudos / f'{cid}.json', crudo)
    return crudo, errores


def cmd_clases(a):
    idi, n, b = a.idioma, a.nivel, a.bloque
    cur = L(R / 'curriculo' / idi / f'n{n}.json')
    fichas = [c for c in cur['clases'] if c['bloque'] == b]
    formatos = []
    for ficha in fichas:
        i = int(ficha['id'].split('.c')[1])
        if a.clases and i not in rango(a.clases, 50): continue
        _, errores = escribir_clase(a, idi, n, b, ficha, cur['cefr'], formatos)
        u = next(x for x in L(R / 'tools' / 'contenido' / f'ruta-{idi}' / f'n{n}-b{b:02d}.json')['unidades'] if x['id'] == ficha['id'])
        formatos += sorted({it['formato'] for p in u['pasos'] for it in p.get('items', []) if 'formato' in it})
        print(f'{ficha["id"]}: {"0 errores" if not errores else f"{len(errores)} SIN RESOLVER"}')
        for e in errores[:8]: print('   ', e)


def cmd_revisar(a):
    idi, n, b = a.idioma, a.nivel, a.bloque
    cur = L(R / 'curriculo' / idi / f'n{n}.json')
    p = R / 'tools' / 'contenido' / f'ruta-{idi}' / f'n{n}-b{b:02d}.json'
    lineas, veredictos = [], []
    for ficha in [c for c in cur['clases'] if c['bloque'] == b]:
        cid = ficha['id']
        crudo = IA / 'registro' / 'crudo' / idi / f'{cid}.json'
        # El revisor recibe el mismo formato que devuelve (el del autor), no la unidad montada para la app.
        clase = L(crudo) if crudo.exists() else next(u for u in L(p)['unidades'] if u['id'] == cid)
        entrada = contexto_clase(idi, n, ficha, cid, []) + f'\n\nCLASE:\n{json.dumps(clase, ensure_ascii=False)}'
        rev = llamar(a.modelo or REVISOR, prompt('clase_revisor', idi), entrada, esquemas.revision(idi), 'revision', 'revision', cid)
        guardar_unidad(idi, n, b, montar(idi, n, cid, ficha, rev['clase'], cur['cefr'], prerequisito_de(idi, n, int(cid.split('.c')[1]))))
        G(crudo, rev['clase'])
        errores = errores_de(idi, n, b, cid)
        if errores:  # el revisor rompió algo: el autor repara sobre la versión revisada
            _, errores = escribir_clase(a, idi, n, b, ficha, cur['cefr'], [], rev['clase'], errores)
        # El revisor a veces anota cambios que no aplica: se comprueba que cada «después» corto está en la clase.
        texto_final = json.dumps(rev['clase'], ensure_ascii=False)
        no_aplicados = [x for x in rev['problemas'] if 3 < len(x['despues']) < 80 and '«' not in x['despues'] and x['despues'] not in texto_final]
        veredictos.append('GO' if rev['veredicto'] == 'GO' and not errores and not no_aplicados else 'REVISE')
        lineas.append(f'\n## {cid} · {rev["veredicto"]} · {len(rev["problemas"])} cambio(s)')
        lineas += [f'- [{x["gravedad"]}] {x["donde"]}: «{x["antes"]}» → «{x["despues"]}» ({x["motivo"]})' for x in rev['problemas']]
        if errores or no_aplicados:
            lineas.append('### Sin resolver\n' + '\n'.join([f'- {e}' for e in errores] + [f'- cambio anotado pero no aplicado: {x["donde"]} → «{x["despues"]}»' for x in no_aplicados]))
        print(f'{cid}: {rev["veredicto"]} · {len(rev["problemas"])} cambio(s) · {len(errores)} error(es) tras validar')
    total = 'GO' if all(v == 'GO' for v in veredictos) else 'REVISE'
    (p.parent / f'revision-n{n}-b{b:02d}.md').write_text(
        f'{total}\n\n# Revisión automática N{n} B{b} ({a.modelo or REVISOR})\n' + '\n'.join(lineas) + '\n\n## Sin resolver\n', encoding='utf-8')


def cmd_costos(a):
    if not REGISTRO.exists():
        return print('sin registro')
    filas = [json.loads(l) for l in REGISTRO.read_text(encoding='utf-8').splitlines() if l.strip()]
    por = {}
    for f in filas:
        k = (f['etapa'], f['modelo'])
        x = por.setdefault(k, [0, 0, 0, 0.0])
        x[0] += 1; x[1] += f['entrada']; x[2] += f['salida']; x[3] += f['usd']
    for (etapa, modelo), (llam, ent, sal, usd) in sorted(por.items()):
        print(f'{etapa:12} {modelo:22} {llam:5} llamadas · {ent / 1e6:7.2f} M entrada · {sal / 1e6:6.2f} M salida · ${usd:8.2f}')
    print(f'TOTAL ${sum(f["usd"] for f in filas):.2f}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('orden', choices=['mapa', 'outline', 'fichas', 'plan', 'clases', 'revisar', 'costos'])
    ap.add_argument('idioma', nargs='?')
    ap.add_argument('nivel', nargs='?', type=int)
    ap.add_argument('bloque', nargs='?', type=int)
    ap.add_argument('--bloques'), ap.add_argument('--clases'), ap.add_argument('--modelo')
    ap.add_argument('--intentos', type=int, default=2, help='rondas de reparación tras la primera versión')
    ap.add_argument('--rehacer', action='store_true', help='regenera aunque ya exista una versión')
    ap.add_argument('--esfuerzo', choices=['minimal', 'low', 'medium', 'high'], help='razonamiento (por defecto, según la etapa)')
    ap.add_argument('--manual', action='store_true',
                    help='sin API: deja el encargo en tools/ia/registro/manual/pendientes/ y lee la respuesta del agente')
    ap.add_argument('--ligera', action='store_true', help='versión esencial de la clase (prompt clase_autor_ligera)')
    a = ap.parse_args()
    global ESFUERZO_FORZADO, MANUAL, LIGERA
    LIGERA = LIGERA or a.ligera
    ESFUERZO_FORZADO = a.esfuerzo
    MANUAL = MANUAL or a.manual
    try:
        {'mapa': cmd_mapa, 'outline': cmd_outline, 'fichas': cmd_fichas, 'plan': cmd_plan, 'clases': cmd_clases,
         'revisar': cmd_revisar, 'costos': cmd_costos}[a.orden](a)
    except Pendiente as p:
        print(f'PENDIENTE: lee {p} , escribe la respuesta donde indica y vuelve a ejecutar este mismo comando.')
        sys.exit(3)


if __name__ == '__main__':
    main()
