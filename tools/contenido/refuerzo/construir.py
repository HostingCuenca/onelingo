#!/usr/bin/env python3
"""Clases de refuerzo: una por cada clase del plan (cNN → rNN), armadas con el
material ya revisado del bloque. No se escriben clases nuevas.

Cómo se arma rNN (va después de las 5 clases del bloque, así todo el bloque ya
está enseñado):
- Repaso: explicación breve, los ejemplos y el vocabulario de cNN y su primera tabla.
- Ejercicios de cNN endurecidos: elegir → escribir, escuchar → dictado,
  completar sin opciones, ordenar → escribir a partir de la traducción.
- Mezcla espaciada: dos ejercicios de otras clases del bloque, una frase
  combinada para ordenar y un relacionar mezclado.
- Situación invertida: el alumno hace la parte de un personaje del diálogo.
- Sin pistas fuera de la práctica guiada y umbral 0,9.

Variación ligera (opcional): `--paquete` escribe las frases de producción para
que una IA cambie un solo elemento de cada una. Al construir, cada variante pasa
un control automático (palabras ya enseñadas, 1–3 palabras cambiadas, se
conserva la palabra del hueco, traducciones presentes). Si falla, queda la
frase original: no hay reintentos ni revisión por clase.

Uso:
  python3 tools/contenido/refuerzo/construir.py fr 1 todo --paquete   (o un bloque: fr 1 1)
  python3 tools/contenido/refuerzo/construir.py fr 1 todo
Archivos: tools/contenido/refuerzo/<idioma>/nX[-bYY].paquete.json y .variantes.json
(al construir se juntan todas las variantes guardadas del nivel)
Al construir reencadena prerrequisitos y orden del curso y corre validar_ruta.py.
Ojo: ruta-<idioma>/integrar.py reescribe los bloques sin refuerzos; tras integrar,
vuelve a construir (es determinista y reaplica las variantes guardadas).
"""
import copy
import difflib
import importlib.util
import json
import pathlib
import random
import re
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
_spec = importlib.util.spec_from_file_location('validar_ruta', RAIZ / 'tools/validar_ruta.py')
vr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vr)
palabras = vr.palabras

NOMBRE = {
    'fr': ('francés', 'French'), 'de': ('alemán', 'German'), 'pt': ('portugués', 'Portuguese'),
    'it': ('italiano', 'Italian'), 'es': ('español', 'Spanish'), 'ru': ('ruso', 'Russian'),
    'zh': ('chino', 'Chinese'), 'ja': ('japonés', 'Japanese'), 'ko': ('coreano', 'Korean'),
}
# Romanización bajo el texto: textoRom en completar y tokensRom en ordenar (listas paralelas).
ROMANIZADOS = {'ru', 'zh', 'ja', 'ko'}
# Escritura propia de cada curso romanizado. En N1–N4 todo texto con ella lleva romanización;
# desde N5, solo el vocabulario (test/romanizacion_test.dart).
ESCRITURA = {'ru': re.compile(r'[\u0400-\u04FF]'), 'zh': re.compile(r'[\u4e00-\u9fff]'),
             'ja': re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]'), 'ko': re.compile(r'[\uac00-\ud7af]')}
NIVEL_MAX_ROM = 4
UMBRAL = 0.9
# La app no menciona Ecuador (mercado EE. UU. + Latinoamérica): ninguna variante lo introduce.
PROHIBIDAS = {'ecuador', 'équateur', 'equador', 'ekuador', 'quito', 'cuenca', 'guayaquil', 'équatorien', 'équatorienne',
              'эквадор', 'кито', '厄瓜多尔', '基多', 'エクアドル', 'キト', '에콰도르', '키토'}
PRODUCCION = {'escribir', 'ordenar', 'completar'}


def apoyo(es, en):
    return {'es': es, 'en': en}


def solo_en(x, rellenar):
    """Cursos con apoyo solo en inglés (español): el constructor trabaja con 'es' copiado
    de 'en' (rellenar=True) y al escribir se quita 'es' (rellenar=False)."""
    if isinstance(x, dict):
        if 'en' in x and isinstance(x['en'], (str, list)):
            if rellenar:
                x.setdefault('es', x['en'])
            else:
                x.pop('es', None)
        for v in x.values():
            solo_en(v, rellenar)
    elif isinstance(x, list):
        for v in x:
            solo_en(v, rellenar)


def leer(p):
    return json.loads(p.read_text(encoding='utf-8'))


def escribir_json(p, datos):
    p.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def es_clase(u):
    return re.search(r'\.n\d+\.c\d+$', u['id'])


def fichas(texto):
    """Fichas de «ordenar»: las palabras con su mayúscula, sin puntuación."""
    return [t for t in vr.PUNTUACION.sub(' ', texto).split() if t != '-']


def barajar(tokens, semilla, roms=None):
    """Fichas barajadas; con `roms` devuelve también la romanización en el mismo orden."""
    idx = list(range(len(tokens)))
    rnd = random.Random(semilla)
    for _ in range(10):
        rnd.shuffle(idx)
        if [tokens[i] for i in idx] != list(tokens) or len(set(tokens)) < 2:
            break
    res = [tokens[i] for i in idx]
    return (res, [roms[i] for i in idx]) if roms is not None else res


def con_rom(it, texto, rom):
    """Fichas de «ordenar» para `texto`, con tokensRom si la romanización tiene las mismas palabras."""
    tokens = fichas(texto)
    roms = fichas(rom) if rom else None
    if roms and len(roms) == len(tokens):
        it['tokens'], it['tokensRom'] = barajar(tokens, texto, roms)
    else:
        it['tokens'] = barajar(tokens, texto)
        it.pop('tokensRom', None)
    return it


def rom_ordenado(it):
    """Romanización de la respuesta de un «ordenar» a partir de sus fichas, o None."""
    pares = list(zip(it.get('tokens') or [], it.get('tokensRom') or []))
    res = []
    for f in fichas(it['respuesta']):
        par = next((x for x in pares if x[0] == f), None)
        if not par:
            return None
        pares.remove(par)
        res.append(par[1])
    return ' '.join(res)


def entre_comillas(t):
    m = re.search(r'[«“](.+)[»”]', t or '')
    return m.group(1).strip() if m else None


def frases(u):
    """Frases con traducción de la clase: ejemplos y diálogo de la situación."""
    res = []
    for p in u['pasos']:
        if p['tipo'] == 'ejemplos':
            res += [(e['texto'], e['traduccion']) for e in p['items']]
        if p['tipo'] == 'situacion':
            res += [(d['texto'], d['traduccion']) for d in p['dialogo']]
    # Fuera deletreos («H, U, G, O.»): al menos dos palabras de dos letras.
    return [(t, tr) for t, tr in res if sum(len(w) >= 2 for w in palabras(t)) >= 2]


def elidida(w):
    return w[-1:] in "’'"


def palabra_re(w):
    """La palabra entera: no cuenta dentro de «vingt-quatre» ni de «m’appelle».
    Una forma elidida («qu’», «d’») va pegada a la siguiente."""
    fin = '' if elidida(w) else r"(?![\w’'-])"
    return re.compile(rf"(?<![\w’'-]){re.escape(w)}{fin}")


def unir(texto, w, idioma=None):
    """«Je n’ai ___ un jour» + «qu’» da «qu’un», no «qu’ un». En francés el
    apóstrofo nunca va seguido de espacio y una letra."""
    if w and elidida(w):
        texto = texto.replace(f'{w} ', w)
    return re.sub(r"(?<=\w’) (?=\w)", '', texto) if idioma == 'fr' else texto


def huella(it):
    return vr.huella_item(it)


class Constructor:
    def __init__(self, idioma, nv, b):
        if idioma not in NOMBRE:
            sys.exit(f'{idioma}: falta adaptar el constructor (romanización o nombre del idioma).')
        self.idioma, self.nv, self.b = idioma, nv, b
        self.ruta = RAIZ / 'assets/contenido' / idioma / 'ruta'
        self.curso = leer(self.ruta / 'curso.json')
        self.apoyos = self.curso['idiomasApoyo']
        if set(self.apoyos) - {'es', 'en'}:
            sys.exit(f'{idioma}: las consignas solo están en es/en; faltan {set(self.apoyos) - {"es", "en"}}')
        self.lengua = NOMBRE[idioma]
        self.archivo = self.ruta / f'n{nv}-b{b:02d}.json'
        self.datos = leer(self.archivo)
        if 'es' not in self.apoyos:
            solo_en(self.datos, True)
        self.clases = [u for u in self.datos['unidades'] if es_clase(u)]
        self.romaniza = idioma in ROMANIZADOS
        self.rom_obligatoria = self.romaniza and nv <= NIVEL_MAX_ROM
        self.rom_de = {x['texto']: x['rom'] for u in self.clases for p in u['pasos']
                       for x in (p['items'] if p['tipo'] == 'ejemplos' else p.get('dialogo') or [])
                       if x.get('rom')}
        self.dir = AQUI / idioma
        self.dir.mkdir(exist_ok=True)
        self.conocida = vr.conocida_para(idioma)
        self.conocidas = self._conocidas()
        self.huellas_originales = {huella(it) for u in self.clases for p in u['pasos']
                                   for it in (p.get('items') or []) if p['tipo'] != 'ejemplos'}
        self.candidatas = {}   # clave → {frase, mantener, tipo}
        self.informe = {'variadas': 0, 'rechazadas': {}, 'identicos_quitados': 0}

    def _conocidas(self):
        """Palabras enseñadas al terminar el bloque, como las calcula el validador."""
        unidades = {}
        for m in self.curso['modulos']:
            for u in leer(self.ruta / m['archivo'])['unidades']:
                unidades[u['id']] = u
        v = vr.Validador(self.idioma)
        v.estricto = bool(self.curso.get('vocabularioEstricto'))
        libres = {w for p in self.curso.get('palabrasLibres', []) for w in palabras(p)}
        return libres | v.conocidas(unidades[self.clases[-1]['id']], unidades)

    def conoce(self, texto, extra=()):
        todas = self.conocidas | set(extra)
        return all(self.conocida(w, todas) for w in palabras(texto))

    # ---- endurecer un ejercicio de la clase original ----
    def endurecer(self, it):
        """Versión más exigente de un ejercicio o None. Marca '_candidata' si su
        frase puede variarse con IA: (frase completa, palabra que se conserva)."""
        f = it['formato']
        base = {k: it[k] for k in ('feedback',) if k in it}
        if f == 'completar':
            n = {**base, 'formato': 'completar', 'consigna': it['consigna'], 'texto': it['texto'],
                 'respuesta': it['respuesta']}
            if it.get('textoRom'):
                n['textoRom'] = it['textoRom']
            n['_candidata'] = (unir(it['texto'].replace('___', it['respuesta']), it['respuesta']), it['respuesta'])
            return n
        if f == 'escuchar' and it.get('audio'):
            ops = it.get('opciones') or []
            if ops and isinstance(ops[0], str):
                return {**base, 'formato': 'escribir', 'audio': it['audio'], 'respuesta': ops[it['respuesta']],
                        'consigna': apoyo('Escucha y escribe lo que oyes.', 'Listen and write what you hear.')}
            if sum(len(w) >= 2 for w in palabras(it['audio'])) >= 1:
                return {**base, 'formato': 'escribir', 'audio': it['audio'], 'respuesta': it['audio'],
                        'consigna': apoyo('Escucha y escribe la frase completa.', 'Listen and write the whole sentence.')}
            return None
        if f == 'elegir':
            ops = it.get('opciones') or []
            if ops and isinstance(ops[0], str) and it.get('preguntaApoyo'):
                pa = it['preguntaApoyo']
                return {**base, 'formato': 'escribir', 'respuesta': ops[it['respuesta']],
                        'consigna': apoyo(f"{pa['es']} Escríbelo en {self.lengua[0]}, sin opciones.",
                                          f"{pa['en']} Write it in {self.lengua[1]}, with no options.")}
            return None
        if f == 'ordenar':
            es, en = entre_comillas(it['consigna'].get('es')), entre_comillas(it['consigna'].get('en'))
            if es and en:
                n = {**base, 'formato': 'escribir', 'respuesta': it['respuesta'],
                     'consigna': apoyo(f'Escribe en {self.lengua[0]}: «{es}»', f'Write in {self.lengua[1]}: “{en}”')}
                if it.get('aceptadas'):
                    n['aceptadas'] = it['aceptadas']
            else:
                n = {**base, 'formato': 'ordenar', 'consigna': it['consigna'], 'respuesta': it['respuesta'],
                     'tokens': barajar(it['tokens'], it['respuesta'])}
                if it.get('tokensRom') and len(it['tokensRom']) == len(it['tokens']):
                    n['tokens'], n['tokensRom'] = barajar(it['tokens'], it['respuesta'], it['tokensRom'])
            n['_candidata'] = (it['respuesta'], None)
            return n
        if f == 'escribir' and not it.get('audio'):
            n = {**base, 'formato': 'escribir', 'consigna': it['consigna'], 'respuesta': it['respuesta']}
            if it.get('aceptadas'):
                n['aceptadas'] = it['aceptadas']
            n['_candidata'] = (it['respuesta'], None)
            return n
        return None

    def endurecidos(self, u, tipo):
        return [n for p in u['pasos'] if p['tipo'] == tipo for it in p['items']
                if (n := self.endurecer(it)) is not None]

    def ordenar_de(self, texto, tr, consigna=None, rom=None):
        return con_rom({'formato': 'ordenar', 'respuesta': texto,
                        'consigna': consigna or apoyo(f"Ordena: «{tr['es']}»", f"Put in order: “{tr['en']}”"),
                        'feedback': apoyo(texto, texto)}, texto, rom or self.rom_de.get(texto))

    # ---- una clase de refuerzo ----
    def refuerzo(self, k):
        u = self.clases[k]
        n = len(self.clases)
        num = re.search(r'c(\d+)$', u['id']).group(1)
        rid = f'{self.idioma}.n{self.nv}.r{num}'
        err = u['erroresFrecuentes'][0]['explicacion']
        t = u['titulo']
        ensenar = [{
            'id': 'p1', 'tipo': 'explicacion', 'icono': 'gramatica',
            'titulo': apoyo(f"Refuerzo: {t['es']}", f"Reinforcement: {t['en']}"),
            'texto': apoyo(
                f"Repasas «{t['es']}» con ejercicios más exigentes: escribes más, eliges menos y la práctica libre "
                f"no tiene pistas. También vuelven frases de las otras clases del bloque. Ojo con el error típico: {err['es']}",
                f"You review “{t['en']}” with harder exercises: more writing, less choosing, and no hints in free "
                f"practice. Sentences from the other lessons in the unit come back too. Watch out for the typical "
                f"mistake: {err['en']}"),
        }]
        for p in u['pasos']:
            if p['tipo'] == 'ejemplos':
                ensenar.append({**copy.deepcopy(p), 'id': f'p{len(ensenar) + 1}'})
                break
        refs = [r for p in u['pasos'] if p['tipo'] == 'vocabulario' for r in p['refs']]
        if refs:
            ensenar.append({'id': f'p{len(ensenar) + 1}', 'tipo': 'vocabulario', 'refs': refs})
        for p in u['pasos']:
            if p['tipo'] == 'tabla':
                ensenar.append({**copy.deepcopy(p), 'id': f'p{len(ensenar) + 1}'})
                break
        extra = {w for e in (x for p in u['pasos'] if p['tipo'] == 'ejemplos' for x in p['items'])
                 for w in palabras(e['texto'])}

        pista_err = apoyo(err['es'], err['en'])
        guiada = []
        for p in u['pasos']:
            if p['tipo'] != 'practica_guiada':
                continue
            for it in p['items']:
                e = self.endurecer(it)
                if e:
                    e['pista'] = it.get('pista') or pista_err
                    guiada.append(e)
        guiada = guiada[:4]

        situacion = self.situacion(u)
        pool = frases(u)
        usadas = {it.get('respuesta') for p in u['pasos'] + [situacion] for it in (p.get('items') or [])}
        independiente = self.endurecidos(u, 'practica_independiente')[:3]
        largas = sorted((f for f in pool if f[0] not in usadas and len(palabras(f[0])) >= 4),
                        key=lambda f: -len(palabras(f[0])))
        for f in largas:  # en N1–N4 romanizado, la primera cuya romanización cuadra palabra por palabra
            o = self.ordenar_de(*f)
            if not self.falta_rom(o):
                independiente.append(o)
                break
        if not guiada:  # la práctica guiada es obligatoria
            guiada = [{**independiente.pop(0), 'pista': pista_err}] if independiente else []

        evaluacion = self.endurecidos(u, 'evaluacion')[:3]
        for j in ((k - 1) % n, (k - 2) % n):
            otros = [e for e in self.endurecidos(self.clases[j], 'evaluacion')
                     if e.get('respuesta') not in {x.get('respuesta') for x in evaluacion}
                     and len(palabras(e.get('respuesta') or '')) >= 2]
            if otros:  # rota para no repetir el mismo ejercicio en todos los refuerzos
                evaluacion.append(otros[k % len(otros)])
        cortas = lambda c: sorted((f for f in frases(c) if 3 <= len(palabras(f[0])) <= 6),  # noqa: E731
                                  key=lambda f: len(palabras(f[0])))
        a, b = cortas(u), cortas(self.clases[(k + 1) % n])
        if a and b:
            texto = f'{a[0][0]} {b[0][0]}'
            tr = {l: f"{a[0][1][l]} {b[0][1][l]}" for l in ('es', 'en')}
            ra, rb = self.rom_de.get(a[0][0]), self.rom_de.get(b[0][0])
            evaluacion.append(self.ordenar_de(texto, tr, apoyo(f'Ordena las dos frases: «{tr["es"]}»',
                                                                 f'Put both sentences in order: “{tr["en"]}”'),
                                              f'{ra} {rb}' if ra and rb else None))
        rel = self.relacionar(u, self.clases[(k + 2) % n])
        if rel:
            evaluacion.append(rel)
        if len({e['formato'] for e in evaluacion}) < 2:  # sin frases cortas: ordenar la más corta de la clase
            todas = sorted((f for f in frases(u) if len(palabras(f[0])) >= 3), key=lambda f: len(palabras(f[0])))
            if todas:
                evaluacion.append(self.ordenar_de(todas[0][0], todas[0][1]))

        pasos = ensenar + [
            {'id': 'pg', 'tipo': 'practica_guiada', 'items': guiada},
            {'id': 'pi', 'tipo': 'practica_independiente', 'items': independiente},
            situacion,
            {'id': 'pe', 'tipo': 'evaluacion', 'items': evaluacion},
        ]
        pasos = [p for p in pasos if p.get('items', True) != []]
        for p in pasos:
            pref = {'practica_guiada': 'g', 'practica_independiente': 'i', 'situacion': 's', 'evaluacion': 'e'}.get(p['tipo'])
            if not pref:
                continue
            for i, it in enumerate(p['items'], 1):
                it['id'] = f'{pref}{i}'
                cand = it.pop('_candidata', None)
                if cand and self.conoce(cand[0], extra):
                    self.candidatas[f"{rid}.{it['id']}"] = {'frase': cand[0], 'mantener': cand[1],
                                                           'formato': it['formato']}
                    rom = it.get('textoRom') if it['formato'] == 'completar' else (
                        rom_ordenado(it) if it['formato'] == 'ordenar' else None)
                    if self.romaniza and rom:
                        self.candidatas[f"{rid}.{it['id']}"]['rom'] = rom
        r = {k2: copy.deepcopy(v) for k2, v in u.items()
             if k2 not in ('id', 'titulo', 'objetivo', 'concepto', 'pasos', 'criterioDominio', 'prerequisitos', 'orden')}
        obj = u['objetivo']
        r.update({
            'id': rid, 'orden': 0, 'prerequisitos': [],
            'titulo': apoyo(f"Refuerzo · {t['es']}", f"Reinforcement · {t['en']}"),
            'objetivo': apoyo(f"Practicar con más exigencia: {obj['es'][0].lower()}{obj['es'][1:]}",
                              f"Harder practice: {obj['en'][0].lower()}{obj['en'][1:]}"),
            'concepto': f"{u['concepto']}-refuerzo",
            'pasos': pasos,
            'criterioDominio': {'umbral': UMBRAL},
            'refuerzoDe': u['id'],
        })
        return r, extra

    def situacion(self, u):
        p = next(x for x in u['pasos'] if x['tipo'] == 'situacion')
        dialogo = p['dialogo']
        conteo = {}
        for d in dialogo:
            conteo[d['hablante']] = conteo.get(d['hablante'], 0) + 1
        quien = max(conteo, key=lambda h: (conteo[h], -[d['hablante'] for d in dialogo].index(h)))
        lineas = [d for d in dialogo if d['hablante'] == quien]
        items = []
        larga = max(lineas, key=lambda d: len(palabras(d['texto'])))
        items.append(self.ordenar_de(larga['texto'], larga['traduccion'], apoyo(
            f"Eres {quien}. Ordena lo que dices: «{larga['traduccion']['es']}»",
            f"You are {quien}. Put what you say in order: “{larga['traduccion']['en']}”")))
        vocab = sorted({v['texto'] for v in u['vocabulario']}, key=len, reverse=True)
        rom_vocab = {v['texto']: v['rom'] for v in u['vocabulario'] if v.get('rom')}
        for d in lineas:
            if d is larga:
                continue
            hueco = next((v for v in vocab if palabra_re(v).search(d['texto'])), None)
            if hueco:
                items.append({'formato': 'completar', 'texto': palabra_re(hueco).sub('___', d['texto'], 1), 'respuesta': hueco,
                              'consigna': apoyo(f"Eres {quien}. Completa tu frase: «{d['traduccion']['es']}»",
                                                f"You are {quien}. Complete your line: “{d['traduccion']['en']}”"),
                              'feedback': apoyo(d['texto'], d['texto'])})
                rh = rom_vocab.get(hueco)
                if d.get('rom') and rh:
                    m = re.compile(rf"(?<!\w){re.escape(rh)}(?!\w)", re.I)
                    if len(m.findall(d['rom'])) == 1:
                        items[-1]['textoRom'] = m.sub('___', d['rom'], 1)
                break
        else:
            otra = next((d for d in lineas if d is not larga), None)
            if otra:
                items.append({'formato': 'escribir', 'respuesta': otra['texto'],
                              'consigna': apoyo(f"Eres {quien}. Escribe: «{otra['traduccion']['es']}»",
                                                f"You are {quien}. Write: “{otra['traduccion']['en']}”"),
                              'feedback': apoyo(otra['texto'], otra['texto'])})
        c = p['contexto']
        return {'id': 'ps', 'tipo': 'situacion',
                'contexto': apoyo(f"{c['es']} Ahora tú eres {quien}: reconstruye lo que dice.",
                                  f"{c['en']} Now you are {quien}: rebuild what they say."),
                'dialogo': copy.deepcopy(dialogo), 'items': items}

    def relacionar(self, u, otra):
        def pares(c):  # (par, romanización o None)
            return [(par, (it.get('paresRom') or [])[i] if i < len(it.get('paresRom') or []) else None)
                    for p in c['pasos'] if p['tipo'] in ('practica_guiada', 'evaluacion')
                    for it in p['items'] if it['formato'] == 'relacionar' for i, par in enumerate(it['pares'])]
        a, b = pares(u), pares(otra)
        if len(a) < 2 or len(b) < 2:
            return None
        mezcla = [a[-1], b[0], a[0], b[-1]]
        if len({m[0][0] for m in mezcla}) < 4:
            return None
        n = {'formato': 'relacionar', 'pares': copy.deepcopy([m[0] for m in mezcla]),
             'consigna': apoyo('Relaciona: mezcla de esta clase y otra del bloque.',
                               'Match: a mix from this lesson and another in the unit.'),
             'feedback': apoyo('Repasa las dos clases si fallaste alguna.', 'Review both lessons if you missed one.')}
        if any(m[1] for m in mezcla):
            n['paresRom'] = [m[1] for m in mezcla]
        return n

    # ---- variación con IA ----
    def aceptar(self, original, var, mantener, extra, cand=None):
        texto = unir((var or {}).get('variante', '').strip(), mantener, self.idioma)
        if not texto or texto == original:
            return 'sin cambio'
        if cand and (cand.get('rom') or (self.rom_obligatoria and cand['formato'] in ('completar', 'ordenar'))):
            # la original lleva (o debe llevar) romanización: la variante también
            rom = (var.get('rom') or '').strip()
            if cand['formato'] == 'completar' and rom.count('___') != 1:
                return 'sin romanización'
            if cand['formato'] == 'ordenar' and len(fichas(rom)) != len(fichas(texto)):
                return 'sin romanización'
        if not all((var.get(l) or '').strip() for l in self.apoyos):
            return 'sin traducción'
        if (set(palabras(texto)) - set(palabras(original))) & PROHIBIDAS:
            return 'menciona Ecuador'
        if not self.conoce(texto, extra):
            return 'palabra no enseñada'
        a, b = palabras(original), palabras(texto)
        iguales = sum(m.size for m in difflib.SequenceMatcher(a=a, b=b).get_matching_blocks())
        cambiadas = max(len(a), len(b)) - iguales
        if not 1 <= cambiadas <= 3 or abs(len(a) - len(b)) > 2:
            return 'cambia demasiado'
        if mantener and len(palabra_re(mantener).findall(texto)) != 1:
            return 'perdió la palabra del hueco'
        if texto in self.frases_originales:
            return 'repite otra frase del bloque'
        return None

    def falta_rom(self, it):
        """En N1–N4 de un curso romanizado: ¿algún texto del ejercicio quedó sin su romanización?"""
        if not self.rom_obligatoria:
            return False
        hay = ESCRITURA[self.idioma].search
        if hay(it.get('texto') or '') and not it.get('textoRom'):
            return True
        if hay(it.get('pregunta') or '') and not it.get('preguntaRom'):
            return True
        toks = it.get('tokens') or []
        if any(hay(t) for t in toks) and len(it.get('tokensRom') or []) != len(toks):
            return True
        ops, oro = it.get('opciones') or [], it.get('opcionesRom') or []
        if any(hay(o.get('meta') or '' if isinstance(o, dict) else o) and not (i < len(oro) and oro[i])
               for i, o in enumerate(ops)):
            return True
        pares = it.get('pares') or []
        return bool(pares) and any(hay(json.dumps(x, ensure_ascii=False)) for x in pares) \
            and len(it.get('paresRom') or []) != len(pares)

    def aplicar(self, rid, it, var):
        texto = unir(var['variante'].strip(), None, self.idioma)
        es, en = var['es'].strip(), var['en'].strip()
        it.pop('aceptadas', None)
        it['feedback'] = apoyo(texto, texto)
        if it['formato'] == 'completar':
            texto = unir(texto, it['respuesta'])
            it['feedback'] = apoyo(texto, texto)
            hueco = '___ ' if elidida(it['respuesta']) else '___'
            it['texto'] = palabra_re(it['respuesta']).sub(hueco, texto, 1)
            it['consigna'] = apoyo(f'Completa: «{es}»', f'Complete: “{en}”')
            rom = (var.get('rom') or '').strip()
            if rom.count('___') == 1:
                it['textoRom'] = rom
            else:
                it.pop('textoRom', None)
        elif it['formato'] == 'ordenar':
            it['respuesta'] = texto
            con_rom(it, texto, (var.get('rom') or '').strip())
            it['consigna'] = apoyo(f'Ordena: «{es}»', f'Put in order: “{en}”')
        else:
            it['respuesta'] = texto
            it['consigna'] = apoyo(f'Escribe en {self.lengua[0]}: «{es}»', f'Write in {self.lengua[1]}: “{en}”')

    # ---- conjunto ----
    def preparar(self):
        self.refuerzos = [self.refuerzo(k) for k in range(len(self.clases))]
        self.permitidas = self.conocidas | {w for _, x in self.refuerzos for w in x}
        return self

    def escribir(self, variantes):
        """Aplica las variantes que pasan el control y escribe el bloque (sin reencadenar)."""
        self.frases_originales = {f for u in self.clases for f, _ in frases(u)} | {
            it.get('respuesta') for u in self.clases for p in u['pasos'] for it in (p.get('items') or [])}
        for r, extra in self.refuerzos:
            for p in r['pasos']:
                if 'items' not in p or p['tipo'] == 'ejemplos':
                    continue
                for it in p['items']:
                    clave = f"{r['id']}.{it['id']}"
                    if clave not in self.candidatas:
                        continue
                    c = self.candidatas[clave]
                    motivo = self.aceptar(c['frase'], variantes.get(clave), c['mantener'], extra, c)
                    if motivo:
                        if clave in variantes:
                            self.informe['rechazadas'][motivo] = self.informe['rechazadas'].get(motivo, 0) + 1
                            self.informe.setdefault('detalle', []).append((clave, motivo))
                    else:
                        self.aplicar(r['id'], it, variantes[clave])
                        self.informe['variadas'] += 1
                # Fuera los ejercicios que quedaron idénticos a uno de las clases, si sobra material.
                minimo = {'practica_guiada': 1, 'practica_independiente': 2, 'situacion': 1, 'evaluacion': 4}[p['tipo']]
                # N1–N4 romanizado: fuera los que quedaron sin romanización (si sobra material).
                for it in list(p['items']):
                    if not self.falta_rom(it):
                        continue
                    resto = [x for x in p['items'] if x is not it]
                    if len(resto) >= minimo and (p['tipo'] != 'evaluacion' or len({x['formato'] for x in resto}) >= 2):
                        p['items'].remove(it)
                        self.informe['sin_rom_quitados'] = self.informe.get('sin_rom_quitados', 0) + 1
                    else:
                        sys.exit(f"{r['id']}/{it['id']}: sin romanización y no sobra material para quitarlo")
                for it in list(p['items']):
                    sin_id = {k: v for k, v in it.items() if k != 'id'}
                    if p['tipo'] == 'evaluacion' and len({x['formato'] for x in p['items'] if x is not it}) < 2:
                        continue  # la evaluación necesita al menos dos formatos
                    if huella(sin_id) in self.huellas_originales and len(p['items']) > minimo:
                        p['items'].remove(it)
                        self.informe['identicos_quitados'] += 1
                if p['tipo'] == 'evaluacion' and len({it['formato'] for it in p['items']}) < 2:
                    sys.exit(f"{r['id']}: la evaluación quedó con un solo formato")
            # Fuera de la práctica los ejercicios que repite la evaluación (contaminación), si sobra material.
            en_evaluacion = {huella({k: v for k, v in it.items() if k != 'id'})
                             for p in r['pasos'] if p['tipo'] == 'evaluacion' for it in p['items']}
            for p in r['pasos']:
                if p['tipo'] not in ('practica_guiada', 'practica_independiente'):
                    continue
                minimo = {'practica_guiada': 1, 'practica_independiente': 2}[p['tipo']]
                for it in list(p['items']):
                    h = huella({k: v for k, v in it.items() if k != 'id'})
                    if h not in en_evaluacion:
                        continue
                    if len(p['items']) > minimo:
                        p['items'].remove(it)
                        self.informe['identicos_quitados'] += 1
                        continue
                    # Práctica al mínimo: sale de la evaluación, si le sobran ítems y formatos.
                    ev = next(q for q in r['pasos'] if q['tipo'] == 'evaluacion')
                    for x in list(ev['items']):
                        if (huella({k: v for k, v in x.items() if k != 'id'}) == h and len(ev['items']) > 4
                                and len({y['formato'] for y in ev['items'] if y is not x}) >= 2):
                            ev['items'].remove(x)
                            self.informe['identicos_quitados'] += 1
        # Encadenados ya detrás de la última clase: si la cadena se corta, el bloque
        # siguiente de esta misma corrida no ve el vocabulario anterior.
        anterior = self.clases[-1]
        for r, _ in self.refuerzos:
            r['prerequisitos'], r['orden'] = [anterior['id']], anterior['orden'] + 1
            anterior = r
        self.datos['unidades'] = self.clases + [r for r, _ in self.refuerzos]
        if 'es' not in self.apoyos:
            solo_en(self.datos, False)
        escribir_json(self.archivo, self.datos)
        self.resumen([r for r, _ in self.refuerzos])

    def resumen(self, refuerzos):
        for r in refuerzos:
            items = [it for p in r['pasos'] if p['tipo'] in ('practica_guiada', 'practica_independiente', 'situacion', 'evaluacion')
                     for it in p['items']]
            prod = sum(it['formato'] in PRODUCCION for it in items)
            largo = sum(len(palabras(it.get('respuesta') or '')) for it in items if it['formato'] in PRODUCCION)
            print(f"{r['id']}: {len(items)} ejercicios, {prod / len(items):.0%} producción, "
                  f"{largo / max(prod, 1):.1f} palabras por respuesta")
        i = self.informe
        total = len(self.candidatas)
        print(f"Variación IA: {i['variadas']}/{total} frases variadas; rechazadas: {i['rechazadas'] or 'ninguna'}; "
              f"ejercicios idénticos quitados: {i['identicos_quitados']}")


def reencadenar(idioma):
    """Cadena lineal del curso como en ruta-<idioma>/integrar.py, con los refuerzos
    detrás de las clases de su bloque."""
    ruta = RAIZ / 'assets/contenido' / idioma / 'ruta'
    curso = leer(ruta / 'curso.json')
    modulos = [m for m in curso['modulos'] if re.match(rf'{idioma}\.n\d+-b\d+$', m['id'])]
    # El ancla (última clase de Fundamentos) y el primer orden los dejó el integrador.
    primera = leer(ruta / modulos[0]['archivo'])['unidades'][0]
    anterior, orden = primera['prerequisitos'][0], primera['orden']
    for m in modulos:
        datos = leer(ruta / m['archivo'])
        for u in datos['unidades']:
            u['prerequisitos'] = [anterior]
            u['orden'] = orden
            anterior = u['id']
            orden += 1
        escribir_json(ruta / m['archivo'], datos)


def variantes_de(idioma, nv):
    """Variantes guardadas del nivel: por bloque (nX-bYY) y del nivel entero (nX)."""
    # Las del bloque van después: sus correcciones a mano mandan sobre las del nivel.
    res = {}
    nivel = AQUI / idioma / f'n{nv}.variantes.json'
    if nivel.exists():
        res.update(leer(nivel))
    for p in sorted((AQUI / idioma).glob(f'n{nv}-b*.variantes.json')):
        res.update(leer(p))
    return res


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 3:
        sys.exit(__doc__)
    idioma, nv = args[0], int(args[1])
    bloques = range(1, 11) if args[2] == 'todo' else [int(args[2])]
    variantes = variantes_de(idioma, nv)
    if '--paquete' in sys.argv:
        # Un paquete por encargo: las palabras de cada bloque se dan como novedad
        # respecto al anterior, y se omiten las frases que ya tienen variante.
        frases_p, nuevas, previas = [], {}, set()
        for b in bloques:
            c = Constructor(idioma, nv, b).preparar()
            nuevas[f'b{b:02d}'] = sorted(c.permitidas - previas)
            previas |= c.permitidas
            frases_p += [{'clave': k, 'bloque': f'b{b:02d}', 'frase': v['frase'],
                          **({'conservar': v['mantener']} if v['mantener'] else {}),
                          **({'rom': v['rom']} if v.get('rom') else {})}
                         for k, v in c.candidatas.items() if k not in variantes]
        nombre = f'n{nv}' if len(bloques) > 1 else f'n{nv}-b{bloques[0]:02d}'
        destino = AQUI / idioma / f'{nombre}.paquete.json'
        escribir_json(destino, {'idioma': idioma, 'nivel': nv,
                                'instrucciones': 'Ver tools/contenido/refuerzo/ENCARGO_VARIACION.md',
                                'palabrasPorBloque': nuevas, 'frases': frases_p})
        print(f'{destino.relative_to(RAIZ)}: {len(frases_p)} frases para variar')
        sys.exit(0)
    for b in bloques:
        Constructor(idioma, nv, b).preparar().escribir(variantes)
    reencadenar(idioma)
    sys.exit(subprocess.run([sys.executable, str(RAIZ / 'tools/validar_ruta.py'), idioma]).returncode)


if __name__ == '__main__':
    main()
