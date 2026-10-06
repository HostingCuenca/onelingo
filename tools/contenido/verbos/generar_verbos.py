#!/usr/bin/env python3
"""Expande la fuente de verbos a las tablas de conjugación de la app.

Fuente:   tools/contenido/verbos/verbos-<idioma>.json (revisada, ver LEEME.md)
Generado: assets/contenido/<idioma>/verbos.json (no editar a mano)

Esquema generado (igual para todos los idiomas; textos de apoyo {es, en}):
  personas: [{meta, traduccion}], tiempos: [{id, nombre, uso}],
  etiquetaResumen, verbos: [{id, infinitivo, traduccion, tipo, nivel, enRuta,
  resumen: [formas clave], formas, tablas: {tiempo: [6 formas]}, ejemplo: {meta, traduccion}}]

El nivel de cada verbo es el primero en que la ruta lo enseña (pasos de
vocabulario); si no, el de la fuente (o 1), con `enRuta: false`.

Uso: python3 tools/contenido/verbos/generar_verbos.py [--comprobar]
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]

IDIOMAS = {
    'en': {
        'personas': [
            ('I', 'yo', 'I'), ('you', 'tú', 'you'), ('he / she / it', 'él / ella', 'he / she / it'),
            ('we', 'nosotros', 'we'), ('you', 'ustedes', 'you (plural)'), ('they', 'ellos', 'they'),
        ],
        'tiempos': [
            ('presente', 'Presente simple', 'Present simple', 'Hábitos y cosas que siempre son así.', 'Habits and things that are always true.'),
            ('pasado', 'Pasado simple', 'Past simple', 'Algo terminado en el pasado (yesterday, last week).', 'Finished actions in the past.'),
            ('futuro', 'Futuro con will', 'Future with will', 'Decisiones del momento, promesas y predicciones.', 'Quick decisions, promises and predictions.'),
            ('perfecto', 'Presente perfecto', 'Present perfect', 'Experiencias y cosas que siguen hasta hoy.', 'Experiences and things that continue until now.'),
            ('continuo', 'Presente continuo', 'Present continuous', 'Lo que está pasando ahora.', 'What is happening right now.'),
        ],
        'etiqueta': ('infinitivo · pasado · participio', 'infinitive · past · past participle'),
    },
    'fr': {
        'personas': [
            ('je', 'yo', 'I'), ('tu', 'tú', 'you'), ('il / elle / on', 'él / ella', 'he / she / one'),
            ('nous', 'nosotros', 'we'), ('vous', 'ustedes / usted', 'you (plural / formal)'), ('ils / elles', 'ellos / ellas', 'they'),
        ],
        'tiempos': [
            ('presente', 'Presente (présent)', 'Present (présent)', 'Lo que haces normalmente o ahora.', 'What you do usually or right now.'),
            ('passe_compose', 'Pasado compuesto (passé composé)', 'Compound past (passé composé)', 'Algo que pasó y terminó.', 'Something that happened and is finished.'),
            ('imperfecto', 'Imperfecto (imparfait)', 'Imperfect (imparfait)', 'Cómo eran las cosas o lo que hacías habitualmente.', 'How things were or what you used to do.'),
            ('futur_proche', 'Futuro próximo (futur proche)', 'Near future (futur proche)', 'Lo que vas a hacer pronto.', 'What you are going to do soon.'),
            ('futuro', 'Futuro (futur simple)', 'Future (futur simple)', 'Lo que harás más adelante.', 'What you will do later.'),
        ],
        'etiqueta': ('infinitivo · presente (je) · participio', 'infinitive · present (je) · past participle'),
    },
    # Portugués de Brasil para hispanohablantes: sin tu/vós (você y ele/ela comparten forma).
    'pt': {
        'personas': [
            ('eu', 'yo', 'I'), ('você', 'tú / usted', 'you'), ('ele / ela', 'él / ella', 'he / she'),
            ('nós', 'nosotros', 'we'), ('vocês', 'ustedes', 'you (plural)'), ('eles / elas', 'ellos / ellas', 'they'),
        ],
        'tiempos': [
            ('presente', 'Presente (presente)', 'Present (presente)', 'Lo que haces normalmente o ahora.', 'What you do usually or right now.'),
            ('preterito', 'Pretérito perfecto (pretérito perfeito)', 'Simple past (pretérito perfeito)', 'Algo que pasó y terminó; también el pasado reciente.', 'Something that happened and is finished.'),
            ('imperfecto', 'Imperfecto (pretérito imperfeito)', 'Imperfect (pretérito imperfeito)', 'Cómo eran las cosas o lo que hacías habitualmente.', 'How things were or what you used to do.'),
            ('futuro', 'Futuro (futuro do presente)', 'Future (futuro do presente)', 'Lo que harás más adelante (en el habla se usa más «vou + infinitivo»).', 'What you will do later (speech often uses «vou + infinitive»).'),
            ('condicional', 'Condicional (futuro do pretérito)', 'Conditional (futuro do pretérito)', 'Lo que harías; pedidos corteses.', 'What you would do; polite requests.'),
            ('subjuntivo', 'Subjuntivo presente (presente do subjuntivo)', 'Present subjunctive (presente do subjuntivo)', 'Después de deseos y dudas: quero que você venha.', 'After wishes and doubts: quero que você venha.'),
            ('futuro_subjuntivo', 'Futuro del subjuntivo (futuro do subjuntivo)', 'Future subjunctive (futuro do subjuntivo)', 'Después de se y quando para algo futuro: se eu puder, quando você chegar.', 'After se and quando for future events: se eu puder, quando você chegar.'),
        ],
        'etiqueta': ('infinitivo · presente (eu) · participio', 'infinitive · present (eu) · past participle'),
    },
    # Español para anglohablantes: el apoyo es solo inglés (como su ruta), así
    # que las traducciones de personas y tiempos van en la columna «en».
    'es': {
        'soloEn': True,
        'personas': [
            ('yo', None, 'I'), ('tú', None, 'you'), ('él / ella / usted', None, 'he / she / you (formal)'),
            ('nosotros / nosotras', None, 'we'), ('ustedes', None, 'you (plural)'), ('ellos / ellas', None, 'they'),
        ],
        'tiempos': [
            ('presente', None, 'Present', None, 'What you do usually or right now.'),
            ('preterito', None, 'Preterite (pretérito)', None, 'A finished action at a specific time (ayer, el lunes).'),
            ('imperfecto', None, 'Imperfect (imperfecto)', None, 'How things were or what you used to do.'),
            ('futuro', None, 'Future (futuro)', None, 'What will happen; also a guess about now.'),
            ('condicional', None, 'Conditional (condicional)', None, 'What would happen; polite requests.'),
            ('perfecto', None, 'Present perfect (pretérito perfecto)', None, 'Haber + participle: what you have done (in Latin America, mostly for experiences).'),
            ('subjuntivo', None, 'Present subjunctive', None, 'After wishes, doubts and «que» in many sentences: quiero que vengas.'),
        ],
        'etiqueta': (None, 'infinitive · present (yo) · past participle'),
    },
    # Alemán (PLAN_ALEMAN.md §7.4). Fuente verbos-de.json, por verbo:
    #   infinitivo, traduccion {es,en}, tipo (regular|fuerte|mixto|modal|irregular), nivel,
    #   auxiliar ('haben'|'sein'), trennbar (prefijo separable o null), partizip2,
    #   praeteritum3sg, imperativo {du, ihr, Sie} (opcional), tablas (6 formas por tiempo,
    #   separables partidos: «stehe auf»; perfekt con auxiliar: «bin aufgestanden»), ejemplo.
    'de': {
        'personas': [
            ('ich', 'yo', 'I'), ('du', 'tú', 'you'), ('er / sie / es', 'él / ella', 'he / she / it'),
            ('wir', 'nosotros', 'we'), ('ihr', 'ustedes (informal)', 'you (plural, informal)'),
            ('sie / Sie', 'ellos / ellas / usted(es)', 'they / you (formal)'),
        ],
        'tiempos': [
            ('praesens', 'Presente (Präsens)', 'Present (Präsens)', 'Lo que haces normalmente, ahora o pronto.', 'What you do usually, now or soon.'),
            ('praeteritum', 'Pasado simple (Präteritum)', 'Simple past (Präteritum)', 'Pasado de textos escritos; en el habla, con sein, haben y los modales.', 'Past in written texts; in speech, with sein, haben and modals.'),
            ('perfekt', 'Pasado compuesto (Perfekt)', 'Present perfect (Perfekt)', 'El pasado del habla: haben o sein + participio al final.', 'The spoken past: haben or sein + participle at the end.'),
            ('futur1', 'Futuro (Futur I)', 'Future (Futur I)', 'werden + infinitivo: planes, promesas y suposiciones.', 'werden + infinitive: plans, promises and guesses.'),
            ('konjunktiv2', 'Condicional (Konjunktiv II)', 'Conditional (Konjunktiv II)', 'Lo que harías y pedidos corteses: ich würde, ich hätte, ich könnte.', 'What you would do and polite requests: ich würde, ich hätte, ich könnte.'),
        ],
        'etiqueta': ('infinitivo · Präteritum (er) · Perfekt (er)', 'infinitive · Präteritum (er) · Perfekt (er)'),
    },
}
AUX_DE = {'haben': 'hat', 'sein': 'ist'}
SOLO_EN = {i for i, c in IDIOMAS.items() if c.get('soloEn')}
BE = {
    'presente': ['am', 'are', 'is', 'are', 'are', 'are'],
    'pasado': ['was', 'were', 'was', 'were', 'were', 'were'],
}
AUX_CONTINUO = ['am', 'are', 'is', 'are', 'are', 'are']


def tablas_en(v):
    inf = v['infinitivo']
    return {
        'presente': BE['presente'] if inf == 'be' else [inf, inf, v['tercera'], inf, inf, inf],
        'pasado': BE['pasado'] if inf == 'be' else [v['pasado']] * 6,
        'futuro': [f'will {inf}'] * 6,
        'perfecto': [('has ' if i == 2 else 'have ') + v['participio'] for i in range(6)],
        'continuo': [f'{a} {v["gerundio"]}' for a in AUX_CONTINUO],
    }


def niveles_en_ruta(idioma):
    """Primer nivel interno en que la ruta enseña cada palabra."""
    base = RAIZ / f'assets/contenido/{idioma}/ruta'
    if not (base / 'curso.json').exists():
        return {}
    curso = json.loads((base / 'curso.json').read_text(encoding='utf-8'))
    publicados = {n['id']: n.get('nivelInterno') for n in curso['niveles'] if n.get('estado') == 'publicado'}
    res = {}
    for m in curso['modulos']:
        if publicados.get(m['nivel']) is None:
            continue
        datos = json.loads((base / m['archivo']).read_text(encoding='utf-8'))
        for u in datos['unidades']:
            nivel = u.get('nivelInterno', publicados[m['nivel']])
            vocab = {v['id']: v['texto'] for v in u.get('vocabulario', [])}
            for p in u.get('pasos', []):
                if p.get('tipo') != 'vocabulario':
                    continue
                for ref in p.get('refs', []):
                    texto = re.sub(r'^(to|se|s’|s\') ', '', vocab.get(ref, '').strip().lower())
                    if texto and (texto not in res or nivel < res[texto]):
                        res[texto] = nivel
    return res


def validar(idioma, verbos):
    errores, vistos = [], set()
    tiempos = [t[0] for t in IDIOMAS[idioma]['tiempos']]
    for v in verbos:
        inf = v.get('infinitivo', '')
        if inf in vistos:
            errores.append(f'{inf}: repetido')
        vistos.add(inf)
        if idioma == 'en':
            for k in ('es', 'tipo', 'tercera', 'pasado', 'participio', 'gerundio'):
                if not str(v.get(k, '')).strip():
                    errores.append(f'{inf}: falta {k}')
            if v.get('tipo') == 'regular' and not (v.get('pasado') == v.get('participio') and str(v.get('pasado')).endswith('ed')):
                errores.append(f'{inf}: regular con formas irregulares')
            ej = v.get('ejemplo') or {}
            if not ej.get('en') or not ej.get('es'):
                errores.append(f'{inf}: sin ejemplo')
        else:
            tr = v.get('traduccion') or {}
            if idioma in SOLO_EN:
                if set(tr) != {'en'} or not tr.get('en'):
                    errores.append(f'{inf}: traducción solo en inglés {{en}}')
                if not str(v.get('participio', '')).strip():
                    errores.append(f'{inf}: falta participio')
            elif not tr.get('es') or not tr.get('en'):
                errores.append(f'{inf}: traducción sin español e inglés')
            tablas = v.get('tablas') or {}
            for t in tiempos:
                fila = tablas.get(t) or []
                if len(fila) != 6 or not all(str(x).strip() for x in fila):
                    errores.append(f'{inf}: tabla «{t}» incompleta')
            if idioma == 'de':
                errores += validar_de(v)
            ej = v.get('ejemplo') or {}
            tej = ej.get('traduccion') or {}
            if not ej.get('meta') or not tej.get('en') or (idioma not in SOLO_EN and not tej.get('es')):
                errores.append(f'{inf}: ejemplo incompleto')
    return errores


def validar_de(v):
    """Campos propios del alemán: auxiliar, separable, Stammformen e imperativo."""
    inf, errores = v.get('infinitivo', ''), []
    for k in ('partizip2', 'praeteritum3sg'):
        if not str(v.get(k, '')).strip():
            errores.append(f'{inf}: falta {k}')
    if v.get('auxiliar') not in AUX_DE:
        errores.append(f'{inf}: auxiliar debe ser haben o sein')
    pref = v.get('trennbar')
    if pref is not None and not (isinstance(pref, str) and inf.startswith(pref) and len(pref) < len(inf)):
        errores.append(f'{inf}: trennbar debe ser el prefijo separable del infinitivo o null')
    tablas = v.get('tablas') or {}
    pres = tablas.get('praesens') or []
    if pref and pres and not all(str(f).endswith(' ' + pref) for f in pres):
        errores.append(f'{inf}: el presente de un separable lleva la partícula al final («stehe {pref}»)')
    perf = tablas.get('perfekt') or []
    if perf and v.get('partizip2') and not all(str(f).endswith(' ' + v['partizip2']) for f in perf):
        errores.append(f'{inf}: el Perfekt debe terminar en el partizip2')
    if len(perf) == 6 and v.get('auxiliar') in AUX_DE and perf[2].split()[0] != AUX_DE[v['auxiliar']]:
        errores.append(f'{inf}: el Perfekt (er) no usa el auxiliar {v["auxiliar"]}')
    imp = v.get('imperativo')
    if imp is not None and (not isinstance(imp, dict) or set(imp) != {'du', 'ihr', 'Sie'}):
        errores.append(f'{inf}: imperativo debe ser {{du, ihr, Sie}}')
    return errores


def apoyo(es, en=None):
    if es is None:  # idioma con apoyo solo en inglés
        return {'en': en}
    return {'es': es, **({'en': en} if en else {})}


def generar(idioma):
    fuente = RAIZ / f'tools/contenido/verbos/verbos-{idioma}.json'
    verbos = json.loads(fuente.read_text(encoding='utf-8'))
    errores = validar(idioma, verbos)
    if errores:
        sys.exit('\n'.join(f'ERROR {e}' for e in errores))
    conf = IDIOMAS[idioma]
    niveles = niveles_en_ruta(idioma)
    salida = []
    for v in sorted(verbos, key=lambda x: x['infinitivo']):
        inf = v['infinitivo']
        if idioma == 'en':
            formas = {k: v[k] for k in ('tercera', 'pasado', 'participio', 'gerundio')}
            tablas = tablas_en(v)
            resumen = [inf, v['pasado'], v['participio']]
            traduccion = apoyo(v['es'])
            ejemplo = {'meta': v['ejemplo']['en'], 'traduccion': apoyo(v['ejemplo']['es'])}
        elif idioma == 'de':
            tablas = v['tablas']
            participio = v['partizip2']
            formas = {'participio': participio, 'praeteritum3sg': v['praeteritum3sg'],
                      'auxiliar': v['auxiliar']}
            if v.get('trennbar'):
                formas['trennbar'] = v['trennbar']
            for p, f in (v.get('imperativo') or {}).items():
                formas[f'imperativo_{p}'] = f.rstrip('!')  # sin «!»: la ruta las usa como formas conocidas
            resumen = [inf, v['praeteritum3sg'], f'{AUX_DE[v["auxiliar"]]} {participio}']
            traduccion = v['traduccion']
            ejemplo = v['ejemplo']
        else:
            tablas = v['tablas']
            if 'participio' in v:
                participio = v['participio']
            else:
                # Participio: última palabra de «je» en passé composé (allé(e) → allé).
                participio = tablas['passe_compose'][0].split()[-1].replace('(e)', '')
            formas = {'participio': participio}
            resumen = [inf, tablas['presente'][0], participio]
            traduccion = v['traduccion']
            ejemplo = v['ejemplo']
        clave = re.sub(r'^(se |s’|s\')', '', inf)
        if idioma == 'es':
            clave = inf  # la ruta enseña el infinitivo tal cual (levantarse)
        salida.append({
            'id': re.sub(r'[^a-z0-9]+', '-', inf.lower().replace('’', '-')).strip('-'),
            'infinitivo': inf,
            'traduccion': traduccion,
            'tipo': v['tipo'],
            'nivel': niveles.get(clave, v.get('nivel', 1)),
            'enRuta': clave in niveles,
            'resumen': resumen,
            'formas': formas,
            'tablas': tablas,
            'ejemplo': ejemplo,
        })
    return json.dumps({
        'version': '2026.10.01',
        'idioma': idioma,
        'personas': [{'meta': m, 'traduccion': apoyo(es, en)} for m, es, en in conf['personas']],
        'tiempos': [{'id': i, 'nombre': apoyo(nes, nen), 'uso': apoyo(ues, uen)} for i, nes, nen, ues, uen in conf['tiempos']],
        'etiquetaResumen': apoyo(*conf['etiqueta']),
        'verbos': salida,
    }, ensure_ascii=False, indent=1) + '\n'


def main():
    idiomas = [i for i in IDIOMAS if (RAIZ / f'tools/contenido/verbos/verbos-{i}.json').exists()]
    viejos = []
    for idioma in idiomas:
        destino = RAIZ / f'assets/contenido/{idioma}/verbos.json'
        texto = generar(idioma)
        actual = destino.read_text(encoding='utf-8') if destino.exists() else ''
        if actual != texto:
            viejos.append(idioma)
            if '--comprobar' not in sys.argv:
                destino.write_text(texto, encoding='utf-8')
                n = len(json.loads(texto)['verbos'])
                print(f'{idioma}: {n} verbos → {destino.relative_to(RAIZ)}')
    if '--comprobar' in sys.argv and viejos:
        sys.exit(f'verbos.json desactualizado ({", ".join(viejos)}): ejecuta generar_verbos.py')
    if not viejos:
        print('Todo al día.')


if __name__ == '__main__':
    main()
