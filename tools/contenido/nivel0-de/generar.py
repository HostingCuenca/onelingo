#!/usr/bin/env python3
"""Genera el Nivel 0 «Leer y pronunciar» del alemán (PLAN_ALEMAN.md §3, fase 1).

Escribe assets/contenido/de/nivel0/sonidos.json y nivel0.json desde los datos
de este archivo y termina con `validar_nivel0.py de --bilingue`.
Apoyo bilingüe {es, en}; alemán estándar de Alemania; sin historia continua;
Lumo solo en la bienvenida (u01l01), nunca en la evaluación (u10).
Imágenes: solo emoji Noto ya presentes en assets/img/emoji/.

16 claves (curriculo/de/f0.json · previos) → unidades:
  sound-text u01 · alphabet u02 · umlauts, eszett u03 · vowel-length, h-length u04 ·
  ie-ei-diphthongs u05 · ch-sounds u06 · sch-sp-st, z-w-v u07 ·
  final-devoicing, r-sounds, schwa-endings u08 · word-stress, capital-nouns,
  glottal-stop u09 · prueba de salida u10.

Uso: python3 tools/contenido/nivel0-de/generar.py
"""
import json
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
DESTINO = RAIZ / 'assets/contenido/de/nivel0'
GRUPO = re.compile(r'\(([^():]+):([^()]+)\)')


def b(es, en):
    return {'es': es, 'en': en}


def plano(m):
    return GRUPO.sub(lambda g: g.group(1), m)


# ── Mapa de sonidos ──────────────────────────────────────────────────────────
# (id, grupo, color, colorNombre es/en, ancla, emoji, nombre es/en, grafías, ejemplos, unidad)
SONIDOS = [
    ('a-kurz', 'breve', '#E24B4A', 'rojo', 'red', 'Apfel', '1f34e', 'la a breve de Apfel', 'the short a in Apfel', ['a', 'a + doble consonante'], ['Apfel', 'Hallo', 'Stadt'], 1),
    ('a-lang', 'larga', '#F08A24', 'naranja', 'orange', 'Hase', '1f430', 'la a larga de Hase', 'the long a in Hase', ['a', 'aa', 'ah'], ['Hase', 'Staat', 'Zahn'], 1),
    ('e-lang', 'larga', '#E8B923', 'amarillo', 'yellow', 'Tee', '1f375', 'la e larga de Tee', 'the long e in Tee', ['e', 'ee', 'eh'], ['Tee', 'Meer', 'Schnee'], 1),
    ('o-lang', 'larga', '#2E8B57', 'verde', 'green', 'Boot', '26f5', 'la o larga de Boot', 'the long o in Boot', ['o', 'oo', 'oh'], ['Boot', 'Brot', 'Sohn'], 1),
    ('e-kurz', 'breve', '#C2185B', 'frambuesa', 'raspberry', 'Bett', '1f6cf', 'la e breve de Bett', 'the short e in Bett', ['e', 'ä'], ['Bett', 'essen', 'Äpfel'], 4),
    ('i-lang', 'larga', '#E0559B', 'rosa', 'pink', 'Biene', '1f41d', 'la i larga de Biene', 'the long i in Biene', ['ie', 'i', 'ih'], ['Biene', 'Tier', 'vier'], 4),
    ('i-kurz', 'breve', '#9C6ADE', 'lila', 'lilac', 'Fisch', '1f41f', 'la i breve de Fisch', 'the short i in Fisch', ['i'], ['Fisch', 'bitte', 'Milch'], 4),
    ('o-kurz', 'breve', '#6B8E23', 'oliva', 'olive', 'Sonne', '2600', 'la o breve de Sonne', 'the short o in Sonne', ['o'], ['Sonne', 'kommen', 'Wolf'], 4),
    ('u-lang', 'larga', '#1E88E5', 'azul', 'blue', 'Blume', '1f337', 'la u larga de Blume', 'the long u in Blume', ['u', 'uh'], ['Blume', 'Kuh', 'Fuß'], 3),
    ('u-kurz', 'breve', '#0D47A1', 'azul marino', 'navy blue', 'Hund', '1f436', 'la u breve de Hund', 'the short u in Hund', ['u'], ['Hund', 'Butter', 'Fluss'], 4),
    ('ae-lang', 'umlaut', '#B5651D', 'marrón', 'brown', 'Käse', '1f9c0', 'la ä larga de Käse', 'the long ä in Käse', ['ä', 'äh'], ['Käse', 'Bär', 'spät'], 3),
    ('ue-lang', 'umlaut', '#00A6A6', 'turquesa', 'teal', 'Tür', '1f6aa', 'la ü larga de Tür', 'the long ü in Tür', ['ü', 'üh'], ['Tür', 'grün', 'müde'], 3),
    ('ue-kurz', 'umlaut', '#4DD0E1', 'celeste', 'sky blue', 'Brücke', '1f309', 'la ü breve de Brücke', 'the short ü in Brücke', ['ü'], ['Brücke', 'Glück', 'fünf'], 3),
    ('oe-lang', 'umlaut', '#D4A017', 'dorado', 'gold', 'König', '1f451', 'la ö larga de König', 'the long ö in König', ['ö', 'öh'], ['König', 'schön', 'Öl'], 3),
    ('oe-kurz', 'umlaut', '#8D6E63', 'café con leche', 'latte', 'Löffel', '1f944', 'la ö breve de Löffel', 'the short ö in Löffel', ['ö'], ['Löffel', 'zwölf', 'können'], 3),
    ('ei', 'diptongo', '#FF7043', 'coral', 'coral', 'Eis', '1f366', 'ei suena «ai», como en Eis', 'ei sounds like “eye,” as in Eis', ['ei', 'ai'], ['Eis', 'drei', 'Wein'], 5),
    ('au', 'diptongo', '#795548', 'chocolate', 'chocolate', 'Haus', '1f3e0', 'au de Haus', 'au as in Haus', ['au'], ['Haus', 'Baum', 'Frau'], 5),
    ('eu', 'diptongo', '#D84315', 'teja', 'brick', 'Feuer', '1f525', 'eu y äu suenan «oi», como en Feuer', 'eu and äu sound like “oy,” as in Feuer', ['eu', 'äu'], ['Feuer', 'Eule', 'Häuser'], 5),
    ('ich', 'consonante', '#7CB342', 'lima', 'lime', 'Milch', '1f95b', 'la ch suave de ich y Milch', 'the soft ch in ich and Milch', ['ch tras i, e, ä, ö, ü, ei, eu, l, r, n', '-ig final'], ['ich', 'Milch', 'König'], 6),
    ('ach', 'consonante', '#5D4037', 'café', 'coffee', 'Buch', '1f4d6', 'la ch áspera de Buch', 'the rough ch in Buch', ['ch tras a, o, u, au'], ['Buch', 'Nacht', 'Kuchen'], 6),
    ('sch', 'consonante', '#455A64', 'pizarra', 'slate', 'Schaf', '1f411', 'sch, y la s de sp/st al inicio', 'sch, and the s of initial sp/st', ['sch', 's en sp-, st- iniciales'], ['Schaf', 'Stern', 'Spinne'], 7),
    ('ts', 'consonante', '#C0CA33', 'pistacho', 'pistachio', 'Zitrone', '1f34b', 'z suena «ts», como en Zitrone', 'z sounds like “ts,” as in Zitrone', ['z', 'tz'], ['Zitrone', 'Zahn', 'Katze'], 7),
    ('w', 'consonante', '#3949AB', 'índigo', 'indigo', 'Wolf', '1f43a', 'w suena como la v inglesa (dientes sobre el labio): Wolf', 'w sounds like English v: Wolf', ['w'], ['Wolf', 'Wasser', 'Wein'], 7),
    ('f', 'consonante', '#26A69A', 'verde agua', 'aqua', 'Vogel', '1f426', 'f, y la v de Vogel', 'f, and the v in Vogel', ['f', 'v', 'ph'], ['Vogel', 'vier', 'Fisch'], 7),
    ('r', 'consonante', '#AD1457', 'granate', 'maroon', 'Rose', '1f339', 'la r de garganta de Rose', 'the throat r in Rose', ['r al inicio de sílaba', 'rr'], ['Rose', 'rot', 'Brot'], 8),
    ('er', 'atona', '#90A4AE', 'gris', 'gray', 'Wasser', '1f4a7', '-er final suena «a» breve: Wasser', 'final -er sounds like a short “uh”: Wasser', ['-er final', 'r tras vocal larga'], ['Wasser', 'Butter', 'Vater'], 8),
    ('schwa', 'atona', '#BDBDBD', 'gris claro', 'light gray', 'Tasche', '1f45c', 'la e débil final de Tasche', 'the weak final e in Tasche', ['-e final', '-en', '-el'], ['Tasche', 'bitte', 'haben'], 8),
]

GRUPOS = {
    'larga': b('Vocales largas', 'Long vowels'),
    'breve': b('Vocales breves', 'Short vowels'),
    'umlaut': b('Umlaut: ä, ö, ü', 'Umlauts: ä, ö, ü'),
    'diptongo': b('Diptongos', 'Diphthongs'),
    'consonante': b('Consonantes que cambian', 'Consonants that change'),
    'atona': b('Finales débiles', 'Weak endings'),
}


def sonidos_json():
    return {
        'esquema': 'onelingo.sonidos.v1',
        'idioma': 'de',
        'nota': 'Mapa de sonidos del alemán estándar de Alemania. El color acompaña siempre al nombre y a la imagen; es una pista de escucha, no una transcripción fonética.',
        'marcas': {'_': 'letra que no suena (h de longitud)', '=': 'varias letras, un sonido'},
        'acento': b('Modelo: alemán estándar de Alemania (Standarddeutsch). Austria y Suiza suenan distinto en algunos sonidos; se reconocen más adelante.',
                    'Model: standard German from Germany (Standarddeutsch). Austria and Switzerland sound different in some sounds; you will meet them later.'),
        'vocales': [
            {'id': i, 'grupo': g, 'color': c, 'colorNombre': b(ces, cen), 'ancla': a, 'emoji': e,
             'nombre': b(nes, nen), 'grafias': gr, 'ejemplos': ej, 'unidad': u}
            for i, g, c, ces, cen, a, e, nes, nen, gr, ej, u in SONIDOS
        ],
    }


# ── Lecciones ────────────────────────────────────────────────────────────────
def W(m, es, en, e=None):
    w = {'m': m, 't': b(es, en)}
    if e:
        w['e'] = e
    return w


ESCUCHA_ELIGE = b('¿Qué palabra oyes?', 'Which word do you hear?')
TOCA = b('Escucha y toca la palabra con el sonido marcado.', 'Listen and tap the word with the marked sound.')


def L(lid, tes, ten, palabras, mira, foco=None, par=None, oye=None, extras=(), construye=None, inv=False, nota=None):
    """Plantilla: escucha → mira → repite → [toca_sonido] → [escucha_elige] → extras → construye.
    par = (con el sonido foco, sin él); oye = (correcta, distractor) para escucha_elige."""
    pasos = [{'tipo': 'escucha', 'palabras': palabras}]
    m0, mes, men = mira
    paso = {'tipo': 'mira', 'm': m0, 'texto': b(mes, men)}
    if foco:
        paso['sonido'] = foco
    if nota:
        paso['nota'] = b(*nota)
    pasos.append(paso)
    pasos.append({'tipo': 'repite', 'm': palabras[0]['m'], 't': palabras[0]['t']})
    if foco and par:
        ops = [{'m': par[0]}, {'m': par[1]}]
        if inv:
            ops.reverse()
        pasos.append({'tipo': 'toca_sonido', 'sonido': foco, 'pregunta': TOCA, 'opciones': ops, 'correcta': 1 if inv else 0})
    if oye:
        ops = [{'m': oye[0]}, {'m': oye[1]}]
        if not inv:
            ops.reverse()
        pasos.append({'tipo': 'escucha_elige', 'audio': plano(oye[0]), 'pregunta': ESCUCHA_ELIGE,
                      'opciones': ops, 'correcta': 0 if inv else 1})
    pasos += list(extras)
    if construye:
        m, extra = construye
        pasos.append({'tipo': 'construye', 'm': m, 'fichas': list(plano(m)) + [extra]})
    return {'id': lid, 'titulo': b(tes, ten), 'pasos': pasos}


def lee(m, tes, ten, pes, pen, ops, correcta=0):
    return {'tipo': 'lee', 'm': m, 't': b(tes, ten), 'pregunta': b(pes, pen),
            'opciones': [{'m': o} for o in ops], 'correcta': correcta}


def significado(m, pes, pen, ops, correcta=0):
    return {'tipo': 'elige_significado', 'm': m, 'pregunta': b(pes, pen),
            'opciones': [b(*o) for o in ops], 'correcta': correcta}


def cambia(de, a, ops):
    return {'tipo': 'cambia', 'de': de, 'a': a, 'opciones': ops}


def letra(l, ops, es='Toca la letra cuyo nombre oyes.', en='Tap the letter whose name you hear.'):
    return {'tipo': 'escucha_letra', 'letra': l, 'pregunta': b(es, en), 'opciones': ops}


def deletreo(m, es, en):
    return {'tipo': 'deletreo', 'm': m, 'pregunta': b(es, en), 'opciones': list(m.upper()), 'correcta': 0}


def mezcla(m, es, en):
    return {'tipo': 'mezcla', 'm': m, 't': b(es, en)}


def oye(correcta, otra, **k):
    return {'tipo': 'escucha_elige', 'audio': plano(correcta), 'pregunta': ESCUCHA_ELIGE,
            'opciones': [{'m': correcta}, {'m': otra}] if not k.get('inv') else [{'m': otra}, {'m': correcta}],
            'correcta': 1 if k.get('inv') else 0}


def toca(foco, si, no, inv=False):
    ops = [{'m': si}, {'m': no}]
    if inv:
        ops.reverse()
    return {'tipo': 'toca_sonido', 'sonido': foco, 'pregunta': TOCA, 'opciones': ops, 'correcta': 1 if inv else 0}


LETRA = ('nombre de la letra', 'letter name')

UNIDADES = [
    {
        'id': 'u01', 'titulo': b('D1 · Hallo! Del sonido a la letra', 'D1 · Hallo! From sound to letter'),
        'objetivo': b('Comprobar que en alemán casi cada letra suena siempre igual y leer las primeras palabras cortas.',
                      'See that in German almost every letter always sounds the same, and read your first short words.'),
        'lecciones': [
            L('u01l01', 'Hallo!', 'Hallo!',
              [W('H(a:a-kurz)llo', 'hola', 'hi', '1f44b'), W('(A:a-kurz)pfel', 'manzana', 'apple', '1f34e'), W('H(a:a-lang)se', 'conejo', 'rabbit', '1f430')],
              ('H(a:a-kurz)llo', 'Escucha «Hallo» entera. En alemán lo escrito y lo que suena van muy unidos: si aprendes las reglas, puedes leer palabras que nunca has visto.',
               'Hear the whole word “Hallo.” In German, spelling and sound are closely linked: once you know the rules, you can read words you have never seen.'),
              foco='a-kurz', par=('(A:a-kurz)pfel', 'Tee'), oye=('Hallo', 'Hase'),
              extras=[
                  {'tipo': 'lumo', 'pose': 'anima', 'texto': b('Bienvenido al alemán de Alemania. Primero escucharás, después leerás. ¡Los colores te ayudan a recordar cada sonido!',
                                                              'Welcome to German as spoken in Germany. First you listen, then you read. The colors help you remember each sound!')},
                  significado('Hallo', '¿Qué significa?', 'What does it mean?', [('hola', 'hi'), ('adiós', 'goodbye')]),
              ],
              construye=('Hallo', 'e')),
            L('u01l02', 'La a: breve o larga', 'The a: short or long',
              [W('N(a:a-lang)se', 'nariz', 'nose', '1f443'), W('H(a:a-lang)se', 'conejo', 'rabbit', '1f430'), W('Name', 'nombre', 'name')],
              ('N(a:a-lang)se', 'La a de Nase es larga y abierta, como una a española estirada. La a de Hallo es igual de abierta, pero corta.',
               'The a in Nase is long and open, like a stretched Spanish a. The a in Hallo is just as open, but short.'),
              foco='a-lang', par=('N(a:a-lang)se', 'Tee'), oye=('Name', 'Nase'), inv=True,
              extras=[lee('Hallo, Anna!', '¡Hola, Anna!', 'Hi, Anna!', '¿Es un saludo o una despedida?', 'Is it a greeting or a goodbye?', ['Hallo', 'Tschüss'])],
              construye=('Nase', 'o')),
            L('u01l03', 'La e larga: Tee', 'The long e: Tee',
              [W('T(ee:e-lang)', 'té', 'tea', '1f375'), W('M(ee:e-lang)r', 'mar', 'sea', '1f30a'), W('Schn(ee:e-lang)', 'nieve', 'snow', '2744')],
              ('T(ee:e-lang)', 'ee se lee como una sola e larga y pura, como la e española pero más larga. No digas «te-e».',
               'ee is read as one long, pure vowel, without the glide of English “say” (more like Spanish e). Don’t say “te-e.”'),
              foco='e-lang', par=('M(ee:e-lang)r', 'Tor'), oye=('Tee', 'Tor'),
              extras=[mezcla('Schnee', 'nieve', 'snow')],
              construye=('Tee', 'a')),
            L('u01l04', 'La o larga: Boot y Brot', 'The long o: Boot and Brot',
              [W('B(oo:o-lang)t', 'barco', 'boat', '26f5'), W('Br(o:o-lang)t', 'pan', 'bread', '1f35e'), W('Rose', 'rosa', 'rose', '1f339')],
              ('B(oo:o-lang)t', 'oo es una o larga y redonda. En Brot la o también es larga aunque se escriba una sola vez.',
               'oo is a long, rounded o. In Brot the o is also long even though it is written once.'),
              foco='o-lang', par=('Br(o:o-lang)t', 'Bett'), oye=('Brot', 'Bett'), inv=True,
              extras=[mezcla('Brot', 'pan', 'bread')],
              construye=('Brot', 'a')),
        ],
    },
    {
        'id': 'u02', 'titulo': b('D2 · El alfabeto', 'D2 · The alphabet'),
        'objetivo': b('Reconocer los nombres de las letras, sobre todo las que engañan (E, I, J, V, W, Y, Z), y deletrear nombres.',
                      'Recognize the letter names, especially the tricky ones (E, I, J, V, W, Y, Z), and spell names.'),
        'lecciones': [
            L('u02l01', 'A, B, C: los nombres', 'A, B, C: the names',
              [W('A, B, C', *LETRA), W('D, E, F', *LETRA), W('G, H, I', *LETRA)],
              ('A, B, C', 'Las letras se llaman casi siempre con su sonido + e: B = «be», D = «de». La H se llama «ha».',
               'Letter names are mostly their sound + e: B = “bay,” D = “day.” H is called “hah.”'),
              oye=('Oma', 'Opa'),
              extras=[letra('H', ['H', 'A', 'E']), deletreo('Oma', 'Escucha y ordena las letras de Oma.', 'Listen and put the letters of Oma in order.')],
              construye=('Opa', 'e')),
            L('u02l02', 'E, I, J: cuidado', 'E, I, J: careful',
              [W('E', 'se dice «e»', 'said “ay”'), W('I', 'se dice «i»', 'said “ee”'), W('J', 'se dice «yot»', 'said “yot”')],
              ('E, I, J', 'E se dice «e» e I se dice «i», como en español. Cuidado con la J: se llama «yot» (no «jota») y suena como la y de «ayer»: ja.',
               'A trap for English speakers: E is said “ay” and I is said “ee.” J is called “yot” and sounds like the y in “yes”: ja.'),
              oye=('ja', 'nein'),
              extras=[letra('J', ['J', 'G', 'I']), deletreo('Jan', 'Deletrea Jan: escucha cada letra.', 'Spell Jan: listen to each letter.'),
                      significado('ja', '¿Qué significa?', 'What does it mean?', [('sí', 'yes'), ('no', 'no')])],
              construye=('ja', 'y')),
            L('u02l03', 'V, W, Y, Z', 'V, W, Y, Z',
              [W('V', 'se dice «fau»', 'said “fow”'), W('W', 'se dice «ve»', 'said “vay”'), W('Y', 'se dice «üpsilon»', 'said “üpsilon”'), W('Z', 'se dice «tset»', 'said “tset”')],
              ('V, W, Z', 'V se llama «fau», W se llama «ve» (con los dientes sobre el labio inferior) y Z se llama «tset».',
               'V is called “fow,” W is called “vay,” and Z is called “tset.”'),
              oye=('Zug', 'Bus'),
              extras=[letra('W', ['W', 'V', 'Z']), letra('Z', ['S', 'Z', 'C']), deletreo('Zug', 'Deletrea Zug.', 'Spell Zug.')],
              construye=('Zug', 's')),
            L('u02l04', 'Ä, Ö, Ü, ß y deletrear', 'Ä, Ö, Ü, ß and spelling',
              [W('Ä, Ö, Ü', 'a-Umlaut, o-Umlaut, u-Umlaut', 'a-umlaut, o-umlaut, u-umlaut'), W('ß', 'Eszett (s doble)', 'Eszett (double s)'), W('L-E-N-A', 'Lena', 'Lena')],
              ('ß', 'ß no es una B: se llama «Eszett» y suena como ss. Cuando deletreas un nombre, ä se dice «a-Umlaut».',
               'ß is not a B: it is called “Eszett” and sounds like ss. When spelling a name, ä is said “a-Umlaut.”'),
              oye=('Lena', 'Lina'),
              extras=[letra('ß', ['ß', 'B', 'S']), deletreo('Lena', 'Escucha y ordena las letras de Lena.', 'Listen and put the letters of Lena in order.')],
              construye=('Lena', 'i')),
        ],
    },
    {
        'id': 'u03', 'titulo': b('D3 · Umlaut y ß', 'D3 · Umlauts and ß'),
        'objetivo': b('Pronunciar ä, ö, ü y leer ß como una s fuerte después de vocal larga o diptongo.',
                      'Pronounce ä, ö, ü and read ß as a strong s after a long vowel or diphthong.'),
        'lecciones': [
            L('u03l01', 'ä suena como e', 'ä sounds like e',
              [W('K(ä:ae-lang)se', 'queso', 'cheese', '1f9c0'), W('B(ä:ae-lang)r', 'oso', 'bear', '1f43b'), W('Mädchen', 'chica', 'girl', '1f467')],
              ('K(ä:ae-lang)se', 'ä se pronuncia como una e abierta (la de «perro»). En Käse es larga; en Mädchen, breve.',
               'ä is pronounced like an open e (the e in “bed”). In Käse it is long; in Mädchen, short.'),
              foco='ae-lang', par=('K(ä:ae-lang)se', 'Kasse'), oye=('Käse', 'Kasse'),
              extras=[cambia('Bar', 'Bär', ['ä', 'a', 'e'])],
              construye=('Käse', 'a')),
            L('u03l02', 'ü: i con labios de u', 'ü: ee with lips for oo',
              [W('T(ü:ue-lang)r', 'puerta', 'door', '1f6aa'), W('gr(ü:ue-lang)n', 'verde', 'green'), W('Br(ü:ue-kurz)cke', 'puente', 'bridge', '1f309')],
              ('T(ü:ue-lang)r', 'Di «i» y, sin mover la lengua, redondea los labios como para «u»: eso es ü. En Brücke la ü es breve.',
               'Say “ee” and, without moving your tongue, round your lips as for “oo”: that is ü. In Brücke the ü is short.'),
              foco='ue-lang', par=('T(ü:ue-lang)r', 'Tier'), oye=('Tier', 'Tür'), inv=True,
              extras=[significado('Tür', '¿Qué significa?', 'What does it mean?', [('puerta', 'door'), ('animal', 'animal')])],
              construye=('Tür', 'u')),
            L('u03l03', 'ö: e con labios de o', 'ö: ay with lips for oh',
              [W('K(ö:oe-lang)nig', 'rey', 'king', '1f451'), W('sch(ö:oe-lang)n', 'bonito', 'beautiful'), W('L(ö:oe-kurz)ffel', 'cuchara', 'spoon', '1f944')],
              ('K(ö:oe-lang)nig', 'Di «e» y redondea los labios como para «o»: eso es ö. schon (ya) y schön (bonito) son palabras distintas.',
               'Say “ay” and round your lips as for “oh”: that is ö. schon (already) and schön (beautiful) are different words.'),
              foco='oe-lang', par=('sch(ö:oe-lang)n', 'schon'), oye=('schön', 'schon'),
              extras=[cambia('schon', 'schön', ['ö', 'o', 'ü'])],
              construye=('schön', 'o')),
            L('u03l04', 'ß: Eszett', 'ß: Eszett',
              [W('F(u:u-lang)ß', 'pie', 'foot', '1f9b6'), W('Straße', 'calle', 'street', '1f6e3'), W('groß', 'grande', 'big')],
              ('F(u:u-lang)ß', 'ß suena como ss. Aparece después de vocal larga (Fuß) o de diptongo (heißen). Tras vocal breve se escribe ss: Fluss.',
               'ß sounds like ss. It comes after a long vowel (Fuß) or a diphthong (heißen). After a short vowel, write ss: Fluss.'),
              foco='u-lang', par=('F(u:u-lang)ß', 'Fluss'), oye=('Fluss', 'Fuß'), inv=True,
              extras=[lee('Straße', 'calle', 'street', '¿Cómo suena ß?', 'How does ß sound?', ['ss', 'b'])],
              construye=('groß', 'b')),
        ],
    },
    {
        'id': 'u04', 'titulo': b('D4 · Vocal larga, vocal breve', 'D4 · Long vowel, short vowel'),
        'objetivo': b('Distinguir vocales largas y breves, y saber que la h después de vocal no suena: alarga la vocal.',
                      'Tell long and short vowels apart, and know that h after a vowel is silent: it makes the vowel long.'),
        'lecciones': [
            L('u04l01', 'Staat o Stadt', 'Staat or Stadt',
              [W('St(aa:a-lang)t', 'Estado', 'state'), W('St(a:a-kurz)dt', 'ciudad', 'city'), W('T(a:a-lang)g', 'día', 'day')],
              ('St(aa:a-lang)t', 'La longitud cambia el significado: Staat (a larga) es «Estado»; Stadt (a breve) es «ciudad». Escucha cuánto dura la vocal.',
               'Length changes meaning: Staat (long a) is “state”; Stadt (short a) is “city.” Listen to how long the vowel lasts.'),
              foco='a-lang', par=('St(aa:a-lang)t', 'Stadt'), oye=('Stadt', 'Staat'),
              extras=[significado('Stadt', '¿Qué significa?', 'What does it mean?', [('ciudad', 'city'), ('Estado', 'state')])],
              construye=('Stadt', 'a')),
            L('u04l02', 'Doble consonante: vocal breve', 'Double consonant: short vowel',
              [W('S(o:o-kurz)nne', 'sol', 'sun', '2600'), W('B(e:e-kurz)tt', 'cama', 'bed', '1f6cf'), W('B(i:i-kurz)tte', 'por favor', 'please')],
              ('S(o:o-kurz)nne', 'Si después de la vocal vienen dos consonantes (nn, tt, ss), la vocal es breve: Sonne, Bett, bitte.',
               'If two consonants follow the vowel (nn, tt, ss), the vowel is short: Sonne, Bett, bitte.'),
              foco='o-kurz', par=('S(o:o-kurz)nne', 'Sohn'), oye=('Sohn', 'Sonne'), inv=True,
              extras=[cambia('Bett', 'Beet', ['e', 't', 'a'])],
              construye=('Bett', 'e')),
            L('u04l03', 'La h que alarga', 'The h that lengthens',
              [W('K(u:u-lang)(h:_)', 'vaca', 'cow', '1f404'), W('Sch(u:u-lang)(h:_)', 'zapato', 'shoe', '1f45e'), W('Z(a:a-lang)(h:_)n', 'diente', 'tooth', '1f9b7')],
              ('K(u:u-lang)(h:_)', 'Después de vocal, la h no suena: solo indica que la vocal es larga. Kuh se dice «kuu». Al inicio de palabra sí suena: Hallo.',
               'After a vowel, h is silent: it only shows the vowel is long. Kuh is said “koo.” At the start of a word it is heard: Hallo.'),
              foco='u-lang', par=('K(u:u-lang)(h:_)', 'Kuss'), oye=('Uhr', 'Ohr'),
              extras=[mezcla('Zahn', 'diente', 'tooth')],
              construye=('Kuh', 'a')),
            L('u04l04', 'ie es una i larga', 'ie is a long i',
              [W('B(ie:i-lang)ne', 'abeja', 'bee', '1f41d'), W('T(ie:i-lang)r', 'animal', 'animal'), W('F(i:i-kurz)sch', 'pez', 'fish', '1f41f')],
              ('B(ie:i-lang)ne', 'ie no es «i-e»: es una sola i larga. La i de Fisch es breve y más relajada.',
               'ie is not “ee-ay”: it is one long ee. The i in Fisch is short and more relaxed.'),
              foco='i-lang', par=('b(ie:i-lang)ten', 'bitten'), oye=('bitten', 'bieten'),
              extras=[significado('Tier', '¿Qué significa?', 'What does it mean?', [('animal', 'animal'), ('puerta', 'door')])],
              construye=('Biene', 'i')),
        ],
    },
    {
        'id': 'u05', 'titulo': b('D5 · ie, ei, eu, au', 'D5 · ie, ei, eu, au'),
        'objetivo': b('Leer sin confundir ie (i larga) con ei («ai»), y pronunciar eu/äu («oi») y au.',
                      'Read ie (long ee) and ei (“eye”) without mixing them up, and pronounce eu/äu (“oy”) and au.'),
        'lecciones': [
            L('u05l01', 'ei suena «ai»', 'ei sounds like “eye”',
              [W('(Ei:ei)s', 'helado', 'ice cream', '1f366'), W('(Ei:ei)', 'huevo', 'egg', '1f95a'), W('dr(ei:ei)', 'tres', 'three')],
              ('(Ei:ei)s', 'ei se pronuncia «ai», como en «aire». Truco: se lee la segunda letra en inglés (ei → «I»).',
               'ei is pronounced like “eye.” Trick: read the second letter the English way (ei → “I”).'),
              foco='ei', par=('W(ei:ei)n', 'Wien'), oye=('Wein', 'Wien'),
              extras=[significado('Wein', '¿Qué significa?', 'What does it mean?', [('vino', 'wine'), ('Viena', 'Vienna')])],
              construye=('Eis', 'a')),
            L('u05l02', 'ie frente a ei', 'ie versus ei',
              [W('W(ie:i-lang)n', 'Viena', 'Vienna'), W('v(ie:i-lang)r', 'cuatro', 'four'), W('L(ie:i-lang)be', 'amor', 'love', '2764')],
              ('W(ie:i-lang)n', 'Truco para las dos: lee la segunda letra. ie → «i» (Wien); ei → «ai» (Wein).',
               'Trick for both: read the second letter. ie → “ee” (Wien); ei → “eye” (Wein).'),
              foco='i-lang', par=('v(ie:i-lang)r', 'drei'), oye=('Wien', 'Wein'), inv=True,
              extras=[lee('Wien', 'Viena', 'Vienna', '¿Es una ciudad o una bebida?', 'Is it a city or a drink?', ['Stadt', 'Wein'])],
              construye=('vier', 'e')),
            L('u05l03', 'eu y äu suenan «oi»', 'eu and äu sound like “oy”',
              [W('F(eu:eu)er', 'fuego', 'fire', '1f525'), W('(Eu:eu)le', 'búho', 'owl', '1f989'), W('H(äu:eu)ser', 'casas', 'houses')],
              ('F(eu:eu)er', 'eu y äu suenan igual: «oi», como en «hoy». Häuser es el plural de Haus.',
               'eu and äu sound the same: “oy,” as in “boy.” Häuser is the plural of Haus.'),
              foco='eu', par=('h(eu:eu)te', 'Hütte'), oye=('heute', 'Hütte'),
              extras=[mezcla('Eule', 'búho', 'owl')],
              construye=('neu', 'a')),
            L('u05l04', 'au como en «auto»', 'au as in “ow”',
              [W('H(au:au)s', 'casa', 'house', '1f3e0'), W('B(au:au)m', 'árbol', 'tree', '1f333'), W('Fr(au:au)', 'mujer; señora', 'woman; Mrs.', '1f469')],
              ('H(au:au)s', 'au suena como en «auto» en español: Haus, Baum, Frau.',
               'au sounds like “ow” in “now”: Haus, Baum, Frau.'),
              foco='au', par=('H(au:au)s', 'Hose'), oye=('Hose', 'Haus'), inv=True,
              extras=[cambia('Haus', 'Maus', ['M', 'H', 'R'])],
              construye=('Baum', 'o')),
        ],
    },
    {
        'id': 'u06', 'titulo': b('D6 · ch: ich y ach', 'D6 · ch: ich and ach'),
        'objetivo': b('Pronunciar las dos ch: suave tras i, e, ü, ö, ä (ich) y áspera tras a, o, u, au (ach); leer -ig final como «ich».',
                      'Pronounce both ch sounds: soft after i, e, ü, ö, ä (ich) and rough after a, o, u, au (ach); read final -ig like “ich.”'),
        'lecciones': [
            L('u06l01', 'La ch suave: ich', 'The soft ch: ich',
              [W('i(ch:ich)', 'yo', 'I'), W('Mil(ch:ich)', 'leche', 'milk', '1f95b'), W('Kir(ch:ich)e', 'iglesia', 'church', '26ea')],
              ('i(ch:ich)', 'Para ich, di «i» y sopla aire con la lengua alta, como un gato que bufa suave. No es «ik» ni «ish».',
               'For ich, say “ee” and push air out with your tongue high, like a gentle cat hiss. It is not “ick” or “ish.”'),
              foco='ich', par=('Mil(ch:ich)', 'Buch'), oye=('ich', 'ach'),
              extras=[mezcla('Milch', 'leche', 'milk')],
              construye=('ich', 'k')),
            L('u06l02', 'La ch áspera: ach', 'The rough ch: ach',
              [W('Bu(ch:ach)', 'libro', 'book', '1f4d6'), W('Ku(ch:ach)en', 'pastel', 'cake', '1f370'), W('Na(ch:ach)t', 'noche', 'night', '1f319')],
              ('Bu(ch:ach)', 'Después de a, o, u y au, la ch se pronuncia al fondo, como la j española de «jota»: Buch, Nacht.',
               'After a, o, u and au, ch is pronounced at the back of the throat, like the ch in Scottish “loch”: Buch, Nacht.'),
              foco='ach', par=('Na(ch:ach)t', 'nicht'), oye=('Nacht', 'nicht'),
              extras=[significado('Buch', '¿Qué significa?', 'What does it mean?', [('libro', 'book'), ('leche', 'milk')])],
              construye=('Buch', 'k')),
            L('u06l03', 'Buch, Bücher', 'Buch, Bücher',
              [W('Bu(ch:ach)', 'libro', 'book', '1f4d6'), W('Bü(ch:ich)er', 'libros', 'books', '1f4da'), W('Mäd(ch:ich)en', 'chica', 'girl', '1f467')],
              ('Bü(ch:ich)er', 'La vocal de antes decide: Buch (u) lleva ach; Bücher (ü) lleva ich. -chen siempre suena ich.',
               'The vowel before decides: Buch (u) takes ach; Bücher (ü) takes ich. -chen always sounds ich.'),
              foco='ich', par=('Bü(ch:ich)er', 'Buch'), oye=('Bücher', 'Buch'), inv=True,
              extras=[toca('ach', 'Bu(ch:ach)', 'Bücher')],
              construye=('Bücher', 'u')),
            L('u06l04', '-ig al final: «ich»', 'Final -ig: “ich”',
              [W('Köni(g:ich)', 'rey', 'king', '1f451'), W('zwanzi(g:ich)', 'veinte', 'twenty'), W('ri(ch:ich)ti(g:ich)', 'correcto', 'correct', '2705')],
              ('Köni(g:ich)', 'En el alemán estándar de Alemania, -ig al final se dice como ich: König, zwanzig, richtig.',
               'In standard German from Germany, final -ig is said like ich: König, zwanzig, richtig.'),
              foco='ich', par=('Köni(g:ich)', 'Tag'), oye=('König', 'Könige'),
              extras=[mezcla('richtig', 'correcto', 'correct')],
              construye=('König', 'k')),
        ],
    },
    {
        'id': 'u07', 'titulo': b('D7 · sch, sp, st, z, w, v', 'D7 · sch, sp, st, z, w, v'),
        'objetivo': b('Leer sch como «sh», sp/st al inicio como «shp/sht», z como «ts», w como v y v como f.',
                      'Read sch as “sh,” initial sp/st as “shp/sht,” z as “ts,” w as v and v as f.'),
        'lecciones': [
            L('u07l01', 'sch suena «sh»', 'sch sounds like “sh”',
              [W('(Sch:sch)af', 'oveja', 'sheep', '1f411'), W('Fi(sch:sch)', 'pez', 'fish', '1f41f'), W('Ta(sch:sch)e', 'bolso', 'bag', '1f45c')],
              ('(Sch:sch)af', 'Tres letras, un sonido: sch se pronuncia como «sh» (como para pedir silencio).',
               'Three letters, one sound: sch is pronounced like English “sh.”'),
              foco='sch', par=('Ta(sch:sch)e', 'Tasse'), oye=('Tasse', 'Tasche'), inv=True,
              extras=[mezcla('Schule', 'escuela', 'school')],
              construye=('Fisch', 's')),
            L('u07l02', 'sp y st al inicio', 'sp and st at the start',
              [W('(S:sch)tern', 'estrella', 'star', '2b50'), W('(S:sch)pinne', 'araña', 'spider', '1f577'), W('(S:sch)tuhl', 'silla', 'chair', '1fa91')],
              ('(S:sch)tern', 'Al inicio de palabra, st- y sp- suenan «sht-» y «shp-». En medio de la palabra la s es normal: Fenster.',
               'At the start of a word, st- and sp- sound like “sht-” and “shp-.” Inside a word the s is normal: Fenster.'),
              foco='sch', par=('(S:sch)tern', 'Fenster'), oye=('Stern', 'Fenster'),
              extras=[lee('Straße', 'calle', 'street', '¿Cómo empieza?', 'How does it start?', ['Schtraße', 'Sstraße'])],
              construye=('Stern', 'h')),
            L('u07l03', 'z suena «ts»', 'z sounds like “ts”',
              [W('(Z:ts)itrone', 'limón', 'lemon', '1f34b'), W('(Z:ts)ahn', 'diente', 'tooth', '1f9b7'), W('Her(z:ts)', 'corazón', 'heart', '2764')],
              ('(Z:ts)itrone', 'La z alemana siempre suena «ts», como al final de «pizza». tz también: Katze.',
               'German z always sounds like “ts,” as in “pizza.” So does tz: Katze.'),
              foco='ts', par=('(Z:ts)ahn', 'Sahne'), oye=('Zahn', 'Sahne'), inv=True,
              extras=[mezcla('Katze', 'gato', 'cat')],
              construye=('Herz', 's')),
            L('u07l04', 'w suena v; v suena f', 'w sounds like v; v sounds like f',
              [W('(W:w)olf', 'lobo', 'wolf', '1f43a'), W('(W:w)asser', 'agua', 'water', '1f4a7'), W('(V:f)ogel', 'pájaro', 'bird', '1f426')],
              ('(W:w)olf', 'w se pronuncia con los dientes sobre el labio, como la v inglesa: Wolf. Y la v suele sonar f: Vogel, vier.',
               'w is pronounced with your teeth on your lip, like English v: Wolf. And v usually sounds like f: Vogel, vier.'),
              foco='w', par=('(W:w)olf', 'Vogel'), oye=('Wein', 'fein'),
              extras=[cambia('Wein', 'fein', ['f', 'w', 'v']), toca('f', '(V:f)ogel', 'Wolf', inv=True)],
              construye=('Wolf', 'v')),
        ],
    },
    {
        'id': 'u08', 'titulo': b('D8 · Finales: -d, -er, -e', 'D8 · Endings: -d, -er, -e'),
        'objetivo': b('Ensordecer b, d, g al final, decir -er como una «a» breve, la r de garganta al inicio y la e débil final.',
                      'Devoice final b, d, g, say -er like a short “uh,” the throat r at the start, and the weak final e.'),
        'lecciones': [
            L('u08l01', 'Hund suena «hunt»', 'Hund sounds like “hunt”',
              [W('Hund', 'perro', 'dog', '1f436'), W('Kind', 'niño', 'child', '1f9d2'), W('Tag', 'día', 'day')],
              ('Hund', 'Al final de la palabra, b suena p, d suena t y g suena k: Hund («hunt»), Tag («tak»). Si sigue una vocal, vuelven: Hunde.',
               'At the end of a word, b sounds like p, d like t and g like k: Hund (“hunt”), Tag (“tahk”). If a vowel follows, they come back: Hunde.'),
              oye=('Kinder', 'Kind'),
              extras=[lee('Hund · Hunde', 'perro · perros', 'dog · dogs', '¿En cuál suena una d de verdad?', 'In which one do you hear a real d?', ['Hunde', 'Hund']),
                      mezcla('Tag', 'día', 'day')],
              construye=('Hund', 't')),
            L('u08l02', '-er suena «a»', '-er sounds like “uh”',
              [W('Wass(er:er)', 'agua', 'water', '1f4a7'), W('Butt(er:er)', 'mantequilla', 'butter', '1f9c8'), W('Vat(er:er)', 'padre', 'father', '1f468')],
              ('Wass(er:er)', 'La -er final no se dice «er»: suena como una «a» breve y suave. Wasser ≈ «vasa».',
               'Final -er is not said “er”: it sounds like a short, soft “uh.” Wasser ≈ “vassuh.”'),
              foco='er', par=('bitt(er:er)', 'bitte'), oye=('bitte', 'bitter'), inv=True,
              extras=[mezcla('Mutter', 'madre', 'mother')],
              construye=('Vater', 'a')),
            L('u08l03', 'La r de garganta', 'The throat r',
              [W('(R:r)ose', 'rosa', 'rose', '1f339'), W('(R:r)ad', 'bicicleta; rueda', 'bike; wheel', '1f6b2'), W('B(r:r)ot', 'pan', 'bread', '1f35e')],
              ('(R:r)ose', 'Al inicio de sílaba, la r se hace al fondo de la boca, como un gargarismo suave. No es la rr española.',
               'At the start of a syllable, r is made at the back of the mouth, like a soft gargle. It is not a rolled r.'),
              foco='r', par=('(R:r)ose', 'Hose'), oye=('Hose', 'Rose'),
              extras=[cambia('Hose', 'Rose', ['R', 'H', 'L'])],
              construye=('Rose', 'h')),
            L('u08l04', 'La e débil final', 'The weak final e',
              [W('Tasch(e:schwa)', 'bolso', 'bag', '1f45c'), W('Nas(e:schwa)', 'nariz', 'nose', '1f443'), W('hab(e:schwa)n', 'tener', 'to have')],
              ('Tasch(e:schwa)', 'La e final sin acento es débil y corta, nunca muda: Tasche, bitte. En -en casi desaparece: haben.',
               'An unstressed final e is weak and short, never silent: Tasche, bitte. In -en it almost disappears: haben.'),
              foco='schwa', par=('Hund(e:schwa)', 'Hund'), oye=('Hunde', 'Hund'),
              extras=[significado('Nase', '¿Qué significa?', 'What does it mean?', [('nariz', 'nose'), ('bolso', 'bag')])],
              construye=('Tasche', 'a')),
        ],
    },
    {
        'id': 'u09', 'titulo': b('D9 · Acento, mayúscula y arranque', 'D9 · Stress, capitals and onset'),
        'objetivo': b('Poner la fuerza en la primera sílaba (salvo palabras extranjeras), reconocer sustantivos por la mayúscula y arrancar cada vocal limpia.',
                      'Stress the first syllable (except in foreign words), spot nouns by their capital letter and start each vowel cleanly.'),
        'lecciones': [
            L('u09l01', 'La fuerza va al inicio', 'Stress goes first',
              [W('Vater', 'padre', 'father', '1f468'), W('Mutter', 'madre', 'mother', '1f469'), W('lernen', 'aprender', 'to learn', '1f4da')],
              ('Vater', 'En las palabras alemanas, la fuerza va casi siempre en la primera sílaba: VA-ter, MUT-ter, LER-nen.',
               'In native German words, stress almost always goes on the first syllable: VA-ter, MUT-ter, LER-nen.'),
              oye=('Mutter', 'Butter'),
              extras=[lee('Vater', 'padre', 'father', '¿Dónde va la fuerza?', 'Where is the stress?', ['VA-ter', 'va-TER'])],
              construye=('Vater', 'e')),
            L('u09l02', 'Palabras extranjeras', 'Foreign words',
              [W('Hotel', 'hotel', 'hotel', '1f3e8'), W('Musik', 'música', 'music', '1f3b5'), W('Telefon', 'teléfono', 'telephone', '260e')],
              ('Hotel', 'Muchas palabras de otros idiomas llevan la fuerza al final: ho-TEL, mu-SIK, te-le-FON.',
               'Many words from other languages are stressed at the end: ho-TEL, mu-SIK, te-le-FON.'),
              oye=('Musik', 'Mosaik'),
              extras=[lee('Telefon', 'teléfono', 'telephone', '¿Dónde va la fuerza?', 'Where is the stress?', ['te-le-FON', 'TE-le-fon']),
                      lee('Elefant', 'elefante', 'elephant', '¿Dónde va la fuerza?', 'Where is the stress?', ['E-le-fant', 'e-le-FANT'], 1)],
              construye=('Hotel', 'a')),
            L('u09l03', 'Sustantivos con mayúscula', 'Nouns with a capital',
              [W('der Hund', 'el perro', 'the dog', '1f436'), W('die Katze', 'el gato', 'the cat', '1f431'), W('das Haus', 'la casa', 'the house', '1f3e0')],
              ('das Haus', 'En alemán todos los sustantivos empiezan con mayúscula, en cualquier lugar de la frase: das Haus, der Hund.',
               'In German every noun starts with a capital letter, anywhere in the sentence: das Haus, der Hund.'),
              oye=('Hund', 'und'),
              extras=[lee('Ich sehe den Hund.', 'Veo al perro.', 'I see the dog.', '¿Qué palabra es un sustantivo?', 'Which word is a noun?', ['Hund', 'sehe']),
                      significado('das Haus', '¿Qué significa?', 'What does it mean?', [('la casa', 'the house'), ('el perro', 'the dog')])],
              construye=('Haus', 'h')),
            L('u09l04', 'Cada vocal arranca limpia', 'Each vowel starts clean',
              [W('Abend', 'tarde; noche', 'evening', '1f319'), W('Eis', 'helado', 'ice cream', '1f366'), W('am Abend', 'por la noche', 'in the evening')],
              ('am Abend', 'En alemán no se unen las palabras como en español («a‿la»): antes de una vocal inicial hay un pequeño corte. am | Abend.',
               'German does not link words before a vowel: there is a tiny catch before a vowel at the start of a word. am | Abend.'),
              oye=('Eis', 'Reis'),
              extras=[mezcla('Guten Abend', 'buenas noches (al llegar)', 'good evening')],
              construye=('Abend', 'a')),
        ],
    },
    {
        'id': 'u10', 'titulo': b('D10 · Ya puedes empezar', 'D10 · You can start now'),
        'objetivo': b('Comprobar que lees y oyes los sonidos del alemán: carteles, contrastes, palabras nuevas y una primera frase.',
                      'Check that you can read and hear German sounds: signs, contrasts, new words and a first sentence.'),
        'lecciones': [
            L('u10l01', 'Lee carteles', 'Read signs',
              [W('Eingang', 'entrada', 'entrance', '1f6aa'), W('Ausgang', 'salida', 'exit'), W('offen', 'abierto', 'open'), W('geschlossen', 'cerrado', 'closed')],
              ('EINGANG · AUSGANG', 'Los carteles suelen ir en mayúsculas. El sonido no cambia: lee primero la palabra clave.',
               'Signs are often in capitals. The sound does not change: read the key word first.'),
              oye=('Ausgang', 'Eingang'),
              extras=[lee('EINGANG · AUSGANG', 'ENTRADA · SALIDA', 'ENTRANCE · EXIT', '¿Qué palabra indica por dónde salir?', 'Which word tells you where to exit?', ['AUSGANG', 'EINGANG']),
                      lee('OFFEN 9–18 Uhr', 'ABIERTO 9–18 h', 'OPEN 9am–6pm', '¿El lugar está abierto o cerrado?', 'Is the place open or closed?', ['offen', 'geschlossen']),
                      lee('Schlaupe', 'Pseudopalabra: no significa nada; léela con las reglas vistas.', 'Pseudoword: it means nothing; read it with the rules you know.',
                          '¿Cuál es la palabra inventada?', 'Which word is made up?', ['Straße', 'Schlaupe'], 1)],
              construye=('offen', 'e')),
            L('u10l02', 'Contrastes', 'Contrasts',
              [W('St(aa:a-lang)t', 'Estado', 'state'), W('T(ü:ue-lang)r', 'puerta', 'door', '1f6aa'), W('W(ei:ei)n', 'vino', 'wine')],
              ('St(aa:a-lang)t', 'Repaso: longitud (Staat/Stadt), Umlaut (Tür/Tier) y diptongos (Wein/Wien).',
               'Review: length (Staat/Stadt), umlauts (Tür/Tier) and diphthongs (Wein/Wien).'),
              foco='ue-lang', par=('T(ü:ue-lang)r', 'Tier'), oye=('Stadt', 'Staat'),
              extras=[oye('Wien', 'Wein', inv=True), oye('schön', 'schon'), oye('ich', 'ach', inv=True), toca('ach', 'Na(ch:ach)t', 'nicht', inv=True)],
              construye=('Stadt', 'e')),
            L('u10l03', 'Palabras nuevas', 'New words',
              [W('Fr(eu:eu)nd', 'amigo', 'friend', '1f91d'), W('Spiel', 'juego', 'game', '1f3b2'), W('Zeit', 'tiempo', 'time', '23f0')],
              ('Fr(eu:eu)nd', 'Estas palabras son nuevas, pero ya conoces sus reglas: eu = «oi», sp- = «shp», z = «ts», ei = «ai», d final = t.',
               'These words are new, but you know their rules: eu = “oy,” sp- = “shp,” z = “ts,” ei = “eye,” final d = t.'),
              foco='eu', par=('Fr(eu:eu)nd', 'Spiel'), oye=('Zeit', 'Seite'),
              extras=[lee('Zeuchen', 'Pseudopalabra: no significa nada; léela con las reglas vistas.', 'Pseudoword: it means nothing; read it with the rules you know.',
                          '¿Cuál es la palabra inventada?', 'Which word is made up?', ['Zeuchen', 'Freund']),
                      mezcla('Spiel', 'juego', 'game')],
              construye=('Zeit', 's')),
            L('u10l04', 'Tu primera frase', 'Your first sentence',
              [W('Hallo!', 'hola', 'hi', '1f44b'), W('Ich heiße Anna.', 'me llamo Anna', 'my name is Anna'), W('Tschüss!', 'chao', 'bye')],
              ('Hallo! Ich heiße Anna.', 'Juntas todo: H que suena, ei = «ai», ß = ss, ü con labios redondos. ¡Ya puedes empezar Fundamentos!',
               'Put it all together: a heard h, ei = “eye,” ß = ss, ü with rounded lips. You are ready for Foundations!'),
              oye=('Tschüss', 'Tisch'),
              extras=[lee('Tschüss!', 'chao', 'bye', '¿Es un saludo o una despedida?', 'Is it a greeting or a goodbye?', ['Hallo', 'Tschüss'], 1),
                      deletreo('Anna', 'Escucha y ordena las letras de Anna.', 'Listen and put the letters of Anna in order.')],
              construye=('Hallo', 'e')),
        ],
    },
]


def nivel0_json():
    return {
        'esquema': 'onelingo.nivel0.v1',
        'idioma': 'de',
        'titulo': b('Nivel 0 · Leer y pronunciar alemán', 'Level 0 · Read and pronounce German'),
        'subtitulo': b('Para quien empieza desde cero: cómo suenan las letras alemanas y cómo leerlas.',
                       'For complete beginners: how German letters sound and how to read them.'),
        'voz': 'narradora',
        'nota': 'Marcado: (letras:sonido) pinta las letras con el color del sonido (ver sonidos.json); _ = letra que no suena (h de longitud). Fuente: tools/contenido/nivel0-de/generar.py. Apoyo es + en.',
        'textos': {
            'tarjeta': b('¿Empiezas de cero? Cómo suenan las letras alemanas y cómo leerlas.', 'Starting from zero? How German letters sound and how to read them.'),
            'muestra': 'H(a:a-kurz)llo · T(ü:ue-lang)r · (Ei:ei)s',
            'emoji': '1f3e0',
            'junta': b('Escucha despacio y después rápido: así se lee el alemán.', 'Listen slowly, then fast: that is how you read German.'),
            'mapaIntro': b('El alemán se lee de forma muy regular. Lo nuevo son las vocales largas y breves, la ä, ö, ü y algunas consonantes (ch, sch, z, w, v). Cada sonido tiene una imagen y un color que verás en las palabras. Toca una tarjeta para oírla.',
                           'German is read very regularly. What is new: long and short vowels, ä, ö, ü and a few consonants (ch, sch, z, w, v). Each sound has a picture and a color you will see in the words. Tap a card to hear it.'),
            'grupos': GRUPOS,
        },
        'revision': 'inicial',
        'refuerzo': {'alfabeto': 'u02', 'umlaut': 'u03', 'longitud': 'u04', 'diptongos': 'u05', 'ch': 'u06',
                     'consonantes': 'u07', 'finales': 'u08', 'acento': 'u09'},
        'evaluacion': {'lecciones': ['u10l01', 'u10l02', 'u10l03', 'u10l04'], 'pseudopalabras': ['Schlaupe', 'Zeuchen'], 'umbral': 0.8},
        'unidades': UNIDADES,
    }


def escribir(nombre, datos):
    (DESTINO / nombre).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    DESTINO.mkdir(parents=True, exist_ok=True)
    escribir('sonidos.json', sonidos_json())
    escribir('nivel0.json', nivel0_json())
    r = subprocess.run([sys.executable, str(RAIZ / 'tools/contenido/validar_nivel0.py'), 'de', '--bilingue'])
    sys.exit(r.returncode)
