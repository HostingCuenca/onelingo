#!/usr/bin/env python3
"""Genera el Nivel 0 «Leer y pronunciar italiano» (misma estructura que el del alemán).

Escribe assets/contenido/it/nivel0/sonidos.json y nivel0.json desde los datos
de este archivo y termina con `validar_nivel0.py it --bilingue`.
Apoyo bilingüe {es, en}: español latino neutro con «tú», inglés americano.
Italiano estándar; sin historia continua; nombres solo de tools/ia/idiomas/it.md.
Lumo solo en la bienvenida (u01l01), nunca en la evaluación (u10).
Reglas fonéticas: solo las guías de tools/ia/idiomas/it.md (c/g suaves y duras,
ch/gh, gn, gli, sc/sch, z, qu, h muda, r/rr, dobles, vocales plenas, acento),
más avisos mínimos (e/o abiertas y cerradas, s entre vocales, b frente a v) que
se oyen pero no se evalúan.
Imágenes: solo emoji Noto ya presentes en assets/img/emoji/.

16 claves (curriculo/it/f0.json · previos) → unidades:
  sound-text u01 · alphabet u02 · full-vowels, open-closed-vowels u03 ·
  c-g-soft-hard u04 · ch-gh-hard, qu-sound u05 · gn-gli, sc-sound u06 ·
  z-sound, s-voicing, h-silent u07 · r-tap-trill, b-v-distinction,
  double-consonants u08 · stress-accents u09 · prueba de salida u10.

Uso: python3 tools/contenido/nivel0-it/generar.py
"""
import json
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
DESTINO = RAIZ / 'assets/contenido/it/nivel0'
GRUPO = re.compile(r'\(([^():]+):([^()]+)\)')


def b(es, en):
    return {'es': es, 'en': en}


def plano(m):
    return GRUPO.sub(lambda g: g.group(1), m)


# ── Mapa de sonidos ──────────────────────────────────────────────────────────
# (id, grupo, color, colorNombre es, en, ancla, emoji, nombre es, en, grafías, ejemplos, unidad)
SONIDOS = [
    ('a', 'vocal', '#E24B4A', 'rojo', 'red', 'ape', '1f41d', 'la a de ape', 'the a in ape', ['a'], ['ape', 'casa', 'mare'], 1),
    ('i', 'vocal', '#E0559B', 'rosa', 'pink', 'libro', '1f4d6', 'la i de libro', 'the i in libro', ['i'], ['libro', 'vino', 'riso'], 1),
    ('u', 'vocal', '#1E88E5', 'azul', 'blue', 'uva', '1f347', 'la u de uva', 'the u in uva', ['u'], ['uva', 'luna', 'lupo'], 1),
    ('e', 'vocal', '#E8B923', 'amarillo', 'yellow', 'elefante', '1f418', 'la e de elefante', 'the e in elefante', ['e'], ['elefante', 'sera', 'mele'], 3),
    ('o', 'vocal', '#2E8B57', 'verde', 'green', 'orso', '1f43b', 'la o de orso', 'the o in orso', ['o'], ['orso', 'moto', 'sole'], 3),
    ('ch', 'suave', '#FF7043', 'coral', 'coral', 'ciao', '1f44b', 'c + e, i suena «ch», como en ciao', 'c + e, i sounds like “ch,” as in ciao', ['ce', 'ci'], ['ciao', 'cena', 'cinema'], 4),
    ('j', 'suave', '#F08A24', 'naranja', 'orange', 'gelato', '1f366', 'g + e, i suena como la j inglesa de gelato', 'g + e, i sounds like English “j,” as in gelato', ['ge', 'gi'], ['gelato', 'giorno', 'gente'], 4),
    ('sh', 'suave', '#C2185B', 'frambuesa', 'raspberry', 'pesce', '1f41f', 'sc + e, i suena «sh», como en pesce', 'sc + e, i sounds like “sh,” as in pesce', ['sce', 'sci'], ['pesce', 'scimmia', 'uscita'], 6),
    ('k', 'duro', '#455A64', 'pizarra', 'slate', 'casa', '1f3e0', 'c duro («k»): casa, chiesa', 'hard c (“k”): casa, chiesa', ['c + a, o, u', 'ch + e, i'], ['casa', 'chiesa', 'chitarra'], 4),
    ('g', 'duro', '#5D4037', 'café', 'coffee', 'gatto', '1f431', 'g dura: gatto, spaghetti', 'hard g: gatto, spaghetti', ['g + a, o, u', 'gh + e, i'], ['gatto', 'gola', 'funghi'], 4),
    ('sk', 'duro', '#795548', 'chocolate', 'chocolate', 'maschera', '1f3ad', 'sch + e, i suena «sk», como en maschera', 'sch + e, i sounds like “sk,” as in maschera', ['sche', 'schi'], ['maschera', 'schiena', 'scherzo'], 6),
    ('qu', 'unido', '#00A6A6', 'turquesa', 'teal', 'quadro', '1f3a8', 'qu suena «cu»: quadro', 'qu sounds like “kw”: quadro', ['qu'], ['quadro', 'quando', 'questo'], 5),
    ('gn', 'unido', '#6B8E23', 'oliva', 'olive', 'bagno', '1f6c1', 'gn suena «ñ»: bagno', 'gn sounds like “ny”: bagno', ['gn'], ['bagno', 'gnocchi', 'montagna'], 6),
    ('gli', 'unido', '#9C6ADE', 'lila', 'lilac', 'figlio', '1f466', 'gli: una «l» pegada al paladar, como en figlio', 'gli: a “l” pressed to the palate, as in figlio', ['gli'], ['figlio', 'famiglia', 'moglie'], 6),
    ('z', 'sibilante', '#C0CA33', 'pistacho', 'pistachio', 'stazione', '1f686', 'z suena «ts» o «ds»: pizza, zero', 'z sounds like “ts” or “ds”: pizza, zero', ['z', 'zz'], ['pizza', 'zero', 'stazione'], 7),
    ('s', 'sibilante', '#3949AB', 'índigo', 'indigo', 'sole', '2600', 'la s fuerte de sole', 'the strong s in sole', ['s', 'ss'], ['sole', 'sera', 'sala'], 7),
    ('sv', 'sibilante', '#26A69A', 'verde agua', 'aqua', 'rosa', '1f339', 'la s suave entre vocales, como en rosa', 'the soft s between vowels, as in rosa', ['s entre vocales'], ['rosa', 'casa', 'museo'], 7),
    ('r', 'vibrante', '#AD1457', 'granate', 'maroon', 'pera', '1f350', 'la r simple: un golpe de lengua, como en pera', 'the single r: one tap of the tongue, as in pera', ['r'], ['pera', 'caro', 'sera'], 8),
    ('rr', 'vibrante', '#8D6E63', 'café con leche', 'latte', 'terra', '1f30d', 'la rr: vibrante múltiple, como en terra', 'the rr: rolled, as in terra', ['rr'], ['terra', 'carro', 'arrivederci'], 8),
    ('b', 'labial', '#D4A017', 'dorado', 'gold', 'barca', '26f5', 'b: labios juntos, como en barca', 'b: lips together, as in barca', ['b'], ['barca', 'bacio', 'bene'], 8),
    ('v', 'labial', '#D84315', 'teja', 'brick', 'vino', '1f377', 'v: dientes sobre el labio, como en vino', 'v: teeth on the lip, as in vino', ['v'], ['vino', 'vacca', 'vene'], 8),
    ('doble', 'doble', '#7CB342', 'lima', 'lime', 'palla', '26bd', 'la consonante doble, más larga: palla', 'the double consonant, held longer: palla', ['bb, cc, dd, ll, mm, nn, pp, rr, ss, tt, zz'], ['palla', 'nonno', 'cappello'], 8),
]

GRUPOS = {
    'vocal': b('Vocales plenas', 'Full vowels'),
    'suave': b('c, g, sc suaves', 'Soft c, g, sc'),
    'duro': b('c, g, sch duras', 'Hard c, g, sch'),
    'unido': b('Sonidos unidos: qu, gn, gli', 'Joined sounds: qu, gn, gli'),
    'sibilante': b('z y s', 'z and s'),
    'vibrante': b('r simple y rr', 'Single r and rr'),
    'labial': b('b y v', 'b and v'),
    'doble': b('Consonantes dobles', 'Double consonants'),
}


def sonidos_json():
    return {
        'esquema': 'onelingo.sonidos.v1',
        'idioma': 'it',
        'nota': 'Mapa de sonidos del italiano estándar. El color acompaña siempre al nombre y a la imagen; es una pista de escucha, no una transcripción fonética.',
        'marcas': {'_': 'letra que no suena (h)', '=': 'varias letras, un sonido'},
        'acento': b('Modelo: italiano estándar. Las diferencias regionales (por ejemplo en la s o en la e y la o abiertas y cerradas) se reconocen más adelante.',
                    'Model: standard Italian. Regional differences (for example in s, or in open and closed e and o) come later.'),
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
CUAL_INVENTADA = ('¿Cuál es la palabra inventada?', 'Which word is made up?')
PSEUDO = ('Pseudopalabra: no significa nada; léela con las reglas vistas.', 'Pseudoword: it means nothing; read it with the rules you know.')


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


def sig(m, pes, pen):
    """Atajo para «¿Qué significa?» con dos opciones (la primera es la correcta)."""
    return significado(m, '¿Qué significa?', 'What does it mean?', [pes, pen])


LETRA = ('nombre de la letra', 'letter name')

UNIDADES = [
    {
        'id': 'u01', 'titulo': b('I1 · Ciao! Del sonido a la letra', 'I1 · Ciao! From sound to letter'),
        'objetivo': b('Comprobar que en italiano lo escrito y lo que suena van muy unidos y leer las primeras palabras con a, i, u.',
                      'See that in Italian spelling and sound are closely linked, and read your first words with a, i, u.'),
        'lecciones': [
            L('u01l01', 'Ciao!', 'Ciao!',
              [W('ci(a:a)o', 'hola; chao', 'hi; bye', '1f44b'), W('c(a:a)sa', 'casa', 'house', '1f3e0'), W('m(a:a)re', 'mar', 'sea', '1f30a')],
              ('ci(a:a)o', 'Escucha «ciao» entera: suena «chao». En italiano lo escrito y lo que suena van muy unidos: si aprendes las reglas, puedes leer palabras que nunca has visto.',
               'Hear the whole word “ciao”: it sounds like “chow.” In Italian, spelling and sound are closely linked: once you know the rules, you can read words you have never seen.'),
              foco='a', par=('c(a:a)sa', 'sole'), oye=('casa', 'sole'),
              extras=[
                  {'tipo': 'lumo', 'pose': 'anima', 'texto': b('Bienvenido al italiano. Primero escucharás, después leerás. ¡Los colores te ayudan a recordar cada sonido!',
                                                              'Welcome to Italian. First you listen, then you read. The colors help you remember each sound!')},
                  sig('ciao', ('hola; chao', 'hi; bye'), ('gracias', 'thank you')),
              ],
              construye=('casa', 'o')),
            L('u01l02', 'La i: siempre «i»', 'The i: always “ee”',
              [W('v(i:i)no', 'vino', 'wine', '1f377'), W('l(i:i)bro', 'libro', 'book', '1f4d6'), W('r(i:i)so', 'arroz', 'rice', '1f35a')],
              ('l(i:i)bro', 'La i suena siempre igual: una «i» clara, como la de «vino» en español. No cambia según la palabra.',
               'The i always sounds the same: a clear “ee,” like the i in “machine.” It does not change from word to word.'),
              foco='i', par=('l(i:i)bro', 'sole'), oye=('vino', 'vano'),
              extras=[mezcla('riso', 'arroz', 'rice')],
              construye=('vino', 'e')),
            L('u01l03', 'La u: siempre «u»', 'The u: always “oo”',
              [W('(u:u)va', 'uva', 'grape', '1f347'), W('l(u:u)na', 'luna', 'moon', '1f319'), W('l(u:u)po', 'lobo', 'wolf', '1f43a')],
              ('l(u:u)na', 'La u es una «u» redonda y clara, como en «luna» en español. Nunca suena «iu» como en inglés.',
               'The u is a round, clear “oo,” as in “moon.” It never sounds like “yoo.”'),
              foco='u', par=('l(u:u)na', 'sole'), oye=('luna', 'lana'),
              extras=[sig('luna', ('luna', 'moon'), ('lobo', 'wolf'))],
              construye=('uva', 'a')),
            L('u01l04', 'Palabras que ya conoces', 'Words you already know',
              [W('r(a:a)dio', 'radio', 'radio', '1f4fb'), W('pi(a:a)no', 'piano', 'piano', '1f3b9'), W('m(o:o)to', 'moto', 'motorcycle', '1f3cd')],
              ('r(a:a)dio', 'Muchas palabras italianas se parecen a las españolas: radio, piano, moto. Si conoces la regla de cada letra, las lees sin ayuda.',
               'Many Italian words look like English ones: radio, piano, moto. If you know the rule for each letter, you can read them without help.'),
              foco='a', par=('r(a:a)dio', 'video'), oye=('piano', 'pianto'),
              extras=[lee('Ciao, Marco!', '¡Hola, Marco!', 'Hi, Marco!', '¿Cuál palabra es el nombre de una persona?', 'Which word is a person’s name?', ['Marco', 'Ciao'])],
              construye=('radio', 'a')),
        ],
    },
    {
        'id': 'u02', 'titulo': b('I2 · El alfabeto', 'I2 · The alphabet'),
        'objetivo': b('Reconocer los nombres de las letras italianas y de las cinco extranjeras (J, K, W, X, Y), y deletrear nombres.',
                      'Recognize the names of the Italian letters and of the five foreign ones (J, K, W, X, Y), and spell names.'),
        'lecciones': [
            L('u02l01', 'A, B, C, D: los nombres', 'A, B, C, D: the names',
              [W('A, B, C', *LETRA), W('D, E, F', *LETRA), W('G, H, I', *LETRA)],
              ('A, B, C', 'El alfabeto italiano tiene veintiuna letras. B se llama «bi», C se llama «ci» (suena «chi»), D se llama «di» y F se llama «effe».',
               'The Italian alphabet has twenty-one letters. B is called “bee,” C is called “chee,” D is called “dee” and F is called “eff-eh.”'),
              oye=('Anna', 'Sara'),
              extras=[letra('B', ['B', 'D', 'C']), deletreo('Anna', 'Escucha y ordena las letras de Anna.', 'Listen and put the letters of Anna in order.')],
              construye=('Sara', 'o')),
            L('u02l02', 'G, H, L, M, N: cuidado', 'G, H, L, M, N: careful',
              [W('G', 'se dice «gi»', 'said “jee”'), W('H', 'se dice «acca»', 'said “ahk-ka”'), W('L, M, N', 'elle, emme, enne', 'ell-eh, em-meh, en-neh')],
              ('G, H', 'Cuidado: la G no se llama «ge» como en español, sino «gi». La H se llama «acca» y nunca suena en las palabras.',
               'Careful: G is called “jee” and H is called “ahk-ka.” In words, H never sounds.'),
              oye=('Elena', 'Chiara'),
              extras=[letra('G', ['G', 'C', 'Q']), letra('H', ['H', 'A', 'E']), deletreo('Elena', 'Escucha y ordena las letras de Elena.', 'Listen and put the letters of Elena in order.')],
              construye=('Elena', 'i')),
            L('u02l03', 'P, Q, R, S, T, U, V, Z', 'P, Q, R, S, T, U, V, Z',
              [W('P, Q, R', 'pi, qu, erre', 'pee, koo, er-reh'), W('S, T, U', 'esse, ti, u', 'es-seh, tee, oo'), W('V, Z', 'vu, zeta', 'voo, dzeh-ta')],
              ('Q, V, Z', 'Q se llama «qu» («cu»), V se llama «vu» y Z se llama «zeta». La R se llama «erre».',
               'Q is called “koo,” V is called “voo” and Z is called “zeta.” R is called “er-reh.”'),
              oye=('Paolo', 'Davide'),
              extras=[letra('Q', ['Q', 'P', 'C']), letra('V', ['V', 'U', 'B']), deletreo('Paolo', 'Escucha y ordena las letras de Paolo.', 'Listen and put the letters of Paolo in order.')],
              construye=('Paolo', 'e')),
            L('u02l04', 'J, K, W, X, Y y deletrear', 'J, K, W, X, Y and spelling',
              [W('J, K', 'i lunga, cappa', 'ee loon-ga, kap-pa'), W('W, X', 'doppia vu, ics', 'dop-pya voo, eeks'), W('Y', 'ipsilon', 'eep-see-lon')],
              ('J, K, W, X, Y', 'Estas cinco letras no son del italiano: aparecen en palabras extranjeras como jeans, kiwi, taxi o yogurt. J = «i lunga», K = «cappa», W = «doppia vu».',
               'These five letters are not native to Italian: they show up in foreign words like jeans, kiwi, taxi or yogurt. J = “ee loon-ga,” K = “kap-pa,” W = “dop-pya voo.”'),
              oye=('Giulia', 'Giorgio'),
              extras=[letra('K', ['K', 'Q', 'C']), letra('W', ['W', 'V', 'U']), deletreo('Luca', 'Escucha y ordena las letras de Luca.', 'Listen and put the letters of Luca in order.')],
              construye=('Luca', 'e')),
        ],
    },
    {
        'id': 'u03', 'titulo': b('I3 · Vocales plenas', 'I3 · Full vowels'),
        'objetivo': b('Pronunciar las cinco vocales siempre plenas, también sin acento, y saber que la e y la o pueden sonar más abiertas o cerradas.',
                      'Pronounce the five vowels always full, even when unstressed, and know that e and o can sound more open or more closed.'),
        'lecciones': [
            L('u03l01', 'Cinco vocales, cinco sonidos', 'Five vowels, five sounds',
              [W('(a:a)pe', 'abeja', 'bee', '1f41d'), W('(e:e)lefante', 'elefante', 'elephant', '1f418'), W('(o:o)rso', 'oso', 'bear', '1f43b')],
              ('(e:e)lefante', 'Italiano tiene cinco vocales: a, e, i, o, u. Cada una suena siempre igual de clara, venga donde venga en la palabra.',
               'Italian has five vowels: a, e, i, o, u. Each one sounds equally clear wherever it comes in the word.'),
              foco='e', par=('(e:e)lefante', 'uva'), oye=('ora', 'uva'),
              extras=[sig('orso', ('oso', 'bear'), ('uva', 'grape'))],
              construye=('orso', 'u')),
            L('u03l02', 'No se reducen', 'Never reduced',
              [W('sol(e:e)', 'sol', 'sun', '2600'), W('mel(a:a)', 'manzana', 'apple', '1f34e'), W('past(a:a)', 'pasta', 'pasta')],
              ('sol(e:e)', 'Las vocales sin acento no se apagan: la e final de sole y la a final de pasta se pronuncian completas. No las conviertas en una «e» débil.',
               'Unstressed vowels do not fade: the final e of sole and the final a of pasta are pronounced in full. Never reduce them to “uh.”'),
              foco='e', par=('sol(e:e)', 'pasta'), oye=('sole', 'sola'), inv=True,
              extras=[mezcla('mela', 'manzana', 'apple')],
              construye=('sole', 'a')),
            L('u03l03', 'e y o: abiertas y cerradas', 'e and o: open and closed',
              [W('bello', 'bonito', 'beautiful'), W('sera', 'tarde; noche', 'evening'), W('sole', 'sol', 'sun', '2600')],
              ('bello', 'La e y la o pueden sonar un poco más abiertas o más cerradas, según la palabra y la región. Por ahora basta con saber que existen: tu oído las irá afinando.',
               'The e and the o can sound a little more open or more closed, depending on the word and the region. For now it is enough to know they exist: your ear will fine-tune them.'),
              oye=('bello', 'pollo'),
              extras=[sig('bello', ('bonito', 'beautiful'), ('feo', 'ugly')), lee('sera', 'tarde; noche', 'evening', '¿Cuál palabra significa «sol»?', 'Which word means “sun”?', ['sole', 'sera'])],
              construye=('bello', 'a')),
            L('u03l04', 'Si cambia la vocal, cambia la palabra', 'Change the vowel, change the word',
              [W('c(a:a)sa', 'casa', 'house', '1f3e0'), W('c(o:o)sa', 'cosa', 'thing'), W('p(a:a)ne', 'pan', 'bread', '1f35e')],
              ('c(o:o)sa', 'Cada vocal cuenta: casa (hogar) y cosa (objeto) solo se distinguen por la vocal. Escucha la diferencia.',
               'Every vowel counts: casa (house) and cosa (thing) differ only in the vowel. Listen to the difference.'),
              foco='o', par=('c(o:o)sa', 'casa'), oye=('cosa', 'casa'),
              extras=[cambia('casa', 'cosa', ['o', 'a', 'e']), sig('pane', ('pan', 'bread'), ('mar', 'sea'))],
              construye=('cosa', 'u')),
        ],
    },
    {
        'id': 'u04', 'titulo': b('I4 · c y g: suaves y duras', 'I4 · c and g: soft and hard'),
        'objetivo': b('Leer c y g suaves ante e, i (ciao, gelato) y duras ante a, o, u (casa, gatto).',
                      'Read soft c and g before e, i (ciao, gelato) and hard c and g before a, o, u (casa, gatto).'),
        'lecciones': [
            L('u04l01', 'ce, ci: suena «ch»', 'ce, ci: sounds like “ch”',
              [W('(c:ch)iao', 'hola; chao', 'hi; bye', '1f44b'), W('(c:ch)ena', 'cena', 'dinner', '1f37d'), W('(c:ch)inema', 'cine', 'cinema', '1f3a6')],
              ('(c:ch)iao', 'La c antes de e o i suena «ch»: ciao ≈ «chao», cena ≈ «chena». En ciao, la i casi no se oye: solo acompaña a la c.',
               'C before e or i sounds like “ch” in “church”: ciao ≈ “chow,” cena ≈ “chay-na.” In ciao the i is barely heard: it only goes with the c.'),
              foco='ch', par=('(c:ch)ena', 'casa'), oye=('cena', 'cane'),
              extras=[sig('cena', ('cena', 'dinner'), ('perro', 'dog'))],
              construye=('cena', 'a')),
            L('u04l02', 'ca, co, cu: suena «k»', 'ca, co, cu: sounds like “k”',
              [W('(c:k)asa', 'casa', 'house', '1f3e0'), W('(c:k)ane', 'perro', 'dog', '1f436'), W('(c:k)uoco', 'cocinero', 'cook', '1f9d1_200d_1f373')],
              ('(c:k)asa', 'Antes de a, o, u, la c suena «k», como la c de «casa» en español. Solo cambia a «ch» antes de e o i.',
               'Before a, o, u, c sounds like “k,” as in “cat.” It only changes to “ch” before e or i.'),
              foco='k', par=('(c:k)asa', 'cena'), oye=('cane', 'cena'), inv=True,
              extras=[toca('ch', '(c:ch)inema', 'cane')],
              construye=('cane', 'o')),
            L('u04l03', 'ge, gi: como la j inglesa', 'ge, gi: like English “j”',
              [W('(g:j)elato', 'helado', 'ice cream', '1f366'), W('(g:j)iorno', 'día', 'day'), W('(g:j)ente', 'gente', 'people')],
              ('(g:j)elato', 'La g antes de e o i suena como la «j» inglesa de «jeans»: gelato, giorno, gente. En giorno, la i casi no se oye.',
               'G before e or i sounds like “j” in “jeans”: gelato, giorno, gente. In giorno the i is barely heard.'),
              foco='j', par=('(g:j)elato', 'gatto'), oye=('gelato', 'gatto'),
              extras=[sig('gelato', ('helado', 'ice cream'), ('gato', 'cat')), mezcla('giorno', 'día', 'day')],
              construye=('gelato', 'i')),
            L('u04l04', 'ga, go, gu: «g» dura', 'ga, go, gu: hard “g”',
              [W('(g:g)atto', 'gato', 'cat', '1f431'), W('(g:g)ola', 'garganta', 'throat'), W('(g:g)usto', 'sabor', 'taste')],
              ('(g:g)atto', 'Antes de a, o, u, la g es dura, como la g de «gato» en español. Antes de e o i es suave: gatto, pero gelato.',
               'Before a, o, u, g is hard, as in “go.” Before e or i it is soft: gatto, but gelato.'),
              foco='g', par=('(g:g)atto', 'gelato'), oye=('gola', 'cola'),
              extras=[cambia('gola', 'cola', ['c', 'g', 'p']), toca('j', '(g:j)ente', 'gatto')],
              construye=('gatto', 'o')),
        ],
    },
    {
        'id': 'u05', 'titulo': b('I5 · ch, gh y qu', 'I5 · ch, gh and qu'),
        'objetivo': b('Leer ch y gh ante e, i como «k» y «g» duras (chiesa, spaghetti) y qu como «cu» (quando).',
                      'Read ch and gh before e, i as hard “k” and “g” (chiesa, spaghetti) and qu as “kw” (quando).'),
        'lecciones': [
            L('u05l01', 'che, chi: suena «k»', 'che, chi: sounds like “k”',
              [W('(ch:k)iesa', 'iglesia', 'church', '26ea'), W('(ch:k)itarra', 'guitarra', 'guitar', '1f3b8'), W('(ch:k)i', 'quién', 'who')],
              ('(ch:k)iesa', 'La h convierte la c en dura: chiesa ≈ «kiesa», chi ≈ «ki». No suena «ch» como en español.',
               'The h makes the c hard: chiesa ≈ “kyeh-za,” chi ≈ “kee.” It does not sound like “ch” in “church.”'),
              foco='k', par=('(ch:k)iesa', 'città'), oye=('chi', 'ci'),
              extras=[sig('chitarra', ('guitarra', 'guitar'), ('iglesia', 'church'))],
              construye=('chiesa', 'e')),
            L('u05l02', 'ghe, ghi: «g» dura', 'ghe, ghi: hard “g”',
              [W('spa(gh:g)etti', 'espagueti', 'spaghetti'), W('fun(gh:g)i', 'hongos', 'mushrooms', '1f344'), W('(gh:g)iaccio', 'hielo', 'ice', '1f9ca')],
              ('spa(gh:g)etti', 'Antes de e o i, gh suena como la g de «guerra»: spaghetti, funghi. La h evita que la g se vuelva suave.',
               'Before e or i, gh sounds like “g” in “go”: spaghetti, funghi. The h keeps the g from turning soft.'),
              foco='g', par=('spa(gh:g)etti', 'gelato'), oye=('ghiaccio', 'giorno'),
              extras=[sig('funghi', ('hongos', 'mushrooms'), ('lagos', 'lakes'))],
              construye=('funghi', 'a')),
            L('u05l03', 'amici y amiche', 'amici and amiche',
              [W('ami(c:ch)i', 'amigos', 'friends'), W('ami(ch:k)e', 'amigas', 'female friends'), W('ba(c:ch)i', 'besos', 'kisses', '1f48b')],
              ('ami(ch:k)e', 'La h cambia el sonido: amici (amigos) suena «amíchi»; amiche (amigas) suena «amíke». Una sola letra distingue las dos palabras.',
               'The h changes the sound: amici (friends) sounds like “ah-MEE-chee”; amiche (female friends) sounds like “ah-MEE-keh.” One letter tells the words apart.'),
              foco='k', par=('ami(ch:k)e', 'ami(c:ch)i'), oye=('amiche', 'amici'),
              extras=[sig('amiche', ('amigas', 'female friends'), ('amigos', 'friends'))],
              construye=('amiche', 'o')),
            L('u05l04', 'qu suena «cu»', 'qu sounds like “kw”',
              [W('(qu:qu)ando', 'cuándo', 'when'), W('(qu:qu)adro', 'cuadro', 'painting', '1f3a8'), W('(qu:qu)esto', 'este', 'this')],
              ('(qu:qu)ando', 'qu se lee «cu»: quando ≈ «cuando». La u sí se oye, a diferencia del español «que».',
               'qu is read like “kw”: quando ≈ “KWAHN-do.” The u is heard, unlike Spanish “que.”'),
              foco='qu', par=('(qu:qu)ando', 'cane'), oye=('questo', 'cesto'),
              extras=[sig('quando', ('cuándo', 'when'), ('dónde', 'where')), mezcla('quadro', 'cuadro', 'painting')],
              construye=('quando', 'e')),
        ],
    },
    {
        'id': 'u06', 'titulo': b('I6 · gn, gli, sc', 'I6 · gn, gli, sc'),
        'objetivo': b('Leer gn como «ñ», gli como una «l» unida al paladar, sc ante e, i como «sh» y sch ante e, i como «sk».',
                      'Read gn as “ny,” gli as a “l” pressed to the palate, sc before e, i as “sh” and sch before e, i as “sk.”'),
        'lecciones': [
            L('u06l01', 'gn suena «ñ»', 'gn sounds like “ny”',
              [W('ba(gn:gn)o', 'baño', 'bathroom', '1f6c1'), W('monta(gn:gn)a', 'montaña', 'mountain', '26f0'), W('(gn:gn)occhi', 'ñoquis', 'gnocchi')],
              ('ba(gn:gn)o', 'gn suena «ñ»: bagno, gnocchi. Son dos letras para un solo sonido.',
               'gn sounds like “ny” in “canyon”: bagno, gnocchi. Two letters for one sound.'),
              foco='gn', par=('ba(gn:gn)o', 'banco'), oye=('bagno', 'banco'),
              extras=[sig('bagno', ('baño', 'bathroom'), ('banco', 'bank'))],
              construye=('bagno', 'm')),
            L('u06l02', 'gli: la «l» unida', 'gli: the joined “l”',
              [W('fi(gli:gli)o', 'hijo', 'son', '1f466'), W('fami(gli:gli)a', 'familia', 'family', '1f46a'), W('mo(gli:gli)e', 'esposa', 'wife')],
              ('fi(gli:gli)o', 'gli suena como «li» muy unido, con la lengua pegada al paladar: figlio ≈ «fí-lio» en un solo golpe. No se separa en «g-l-i».',
               'gli sounds like the “lli” in “million,” with the tongue pressed to the palate: figlio ≈ “FEE-lyo” in a single stroke. It is not split into g-l-i.'),
              foco='gli', par=('fi(gli:gli)o', 'filo'), oye=('figlio', 'filo'),
              extras=[sig('famiglia', ('familia', 'family'), ('amigos', 'friends'))],
              construye=('figlio', 'a')),
            L('u06l03', 'sce, sci: suena «sh»', 'sce, sci: sounds like “sh”',
              [W('pe(sc:sh)e', 'pescado', 'fish', '1f41f'), W('(sc:sh)immia', 'mono', 'monkey', '1f412'), W('u(sc:sh)ita', 'salida', 'exit')],
              ('pe(sc:sh)e', 'sc antes de e o i suena «sh»: pesce ≈ «peshe». Son dos letras para un solo sonido.',
               'sc before e or i sounds like “sh”: pesce ≈ “PEH-sheh.” Two letters for one sound.'),
              foco='sh', par=('pe(sc:sh)e', 'pesto'), oye=('pesce', 'pesto'),
              extras=[sig('uscita', ('salida', 'exit'), ('entrada', 'entrance')), mezcla('scimmia', 'mono', 'monkey')],
              construye=('pesce', 'i')),
            L('u06l04', 'sche, schi: suena «sk»', 'sche, schi: sounds like “sk”',
              [W('ma(sch:sk)era', 'máscara', 'mask', '1f3ad'), W('(sch:sk)iena', 'espalda', 'back'), W('(sch:sk)erzo', 'broma', 'joke')],
              ('ma(sch:sk)era', 'Con una h, sch antes de e o i suena «sk»: schiena ≈ «skiena», maschera ≈ «maskera». Es el mismo truco que ch: la h endurece el sonido.',
               'With the h, sch before e or i sounds like “sk”: schiena ≈ “SKYEH-na,” maschera ≈ “MAS-keh-ra.” It is the same trick as ch: the h makes the sound hard.'),
              foco='sk', par=('ma(sch:sk)era', 'pesce'), oye=('pesche', 'pesce'),
              extras=[toca('sh', 'pe(sc:sh)e', 'schiena'), sig('scherzo', ('broma', 'joke'), ('pescado', 'fish'))],
              construye=('schiena', 'a')),
        ],
    },
    {
        'id': 'u07', 'titulo': b('I7 · z, s y h', 'I7 · z, s and h'),
        'objetivo': b('Leer z como «ts» o «ds», oír la s fuerte y la s suave entre vocales, y saber que la h nunca suena.',
                      'Read z as “ts” or “ds,” hear the strong s and the soft s between vowels, and know that h never sounds.'),
        'lecciones': [
            L('u07l01', 'z: «ts» o «ds»', 'z: “ts” or “ds”',
              [W('pi(zz:z)a', 'pizza', 'pizza'), W('gra(z:z)ie', 'gracias', 'thank you'), W('(z:z)ero', 'cero', 'zero')],
              ('pi(zz:z)a', 'La z suena «ts» (pizza ≈ «pitsa») o «ds» (zero ≈ «dsero»). No cambia el significado: tu oído aprende cuál lleva cada palabra.',
               'The z sounds like “ts” (pizza ≈ “PEET-sa”) or “ds” (zero ≈ “DZEH-ro”). The meaning does not change: your ear learns which one each word takes.'),
              foco='z', par=('pi(zz:z)a', 'pasta'), oye=('pizza', 'pista'),
              extras=[sig('grazie', ('gracias', 'thank you'), ('por favor', 'please'))],
              construye=('pizza', 'e')),
            L('u07l02', 'z en más palabras', 'z in more words',
              [W('sta(z:z)ione', 'estación', 'station', '1f686'), W('(z:z)io', 'tío', 'uncle'), W('(z:z)ucchero', 'azúcar', 'sugar')],
              ('sta(z:z)ione', 'Lee estas palabras con la misma z: stazione, zio, zucchero. En el italiano de todos los días, se oye «ts» o «ds» según la palabra.',
               'Read these words with the same z: stazione, zio, zucchero. In everyday Italian, you hear “ts” or “ds” depending on the word.'),
              foco='z', par=('sta(z:z)ione', 'sera'), oye=('zio', 'dio'),
              extras=[sig('stazione', ('estación', 'station'), ('farmacia', 'pharmacy')), mezcla('zucchero', 'azúcar', 'sugar')],
              construye=('zio', 'a')),
            L('u07l03', 's: fuerte o suave', 's: strong or soft',
              [W('(s:s)ole', 'sol', 'sun', '2600'), W('ro(s:sv)a', 'rosa', 'rose', '1f339'), W('ca(s:sv)a', 'casa', 'house', '1f3e0')],
              ('ro(s:sv)a', 'Al inicio de una palabra, la s es fuerte: sole. Entre dos vocales suele sonar suave y con vibración en la garganta: rosa, casa. Según la región cambia; por ahora se escucha, no se evalúa.',
               'At the start of a word, s is strong: sole. Between two vowels it usually sounds soft and buzzing in the throat, like a “z”: rosa, casa. It varies by region; for now you listen, you are not tested.'),
              foco='sv', par=('ro(s:sv)a', 'sole'), oye=('rosa', 'sola'),
              extras=[toca('s', '(s:s)ole', 'ro(s:sv)a'), sig('rosa', ('rosa (flor)', 'rose (flower)'), ('sol', 'sun'))],
              construye=('rosa', 'u')),
            L('u07l04', 'La h nunca suena', 'The h never sounds',
              [W('(h:_)o', 'tengo', 'I have'), W('(h:_)ai', 'tienes', 'you have'), W('(h:_)anno', 'tienen', 'they have')],
              ('(h:_)o', 'La h nunca suena: ho ≈ «o», hai ≈ «ai», hanno ≈ «anno». Se escribe para distinguir ho (tengo) de o (o).',
               'The h never sounds: ho ≈ “oh,” hai ≈ “eye,” hanno ≈ “AHN-no.” It is written to tell ho (I have) from o (or).'),
              oye=('hai', 'mai'),
              extras=[sig('hai', ('tienes', 'you have'), ('tengo', 'I have')), cambia('ho', 'so', ['s', 'h', 'n']), mezcla('hotel', 'hotel', 'hotel')],
              construye=('hanno', 'm')),
        ],
    },
    {
        'id': 'u08', 'titulo': b('I8 · r, b, v y dobles', 'I8 · r, b, v and doubles'),
        'objetivo': b('Distinguir la r simple y la rr, la b y la v, y mantener más tiempo las consonantes dobles, que cambian el significado.',
                      'Tell single r and rr apart, b and v apart, and hold double consonants longer, because they change the meaning.'),
        'lecciones': [
            L('u08l01', 'r simple y rr', 'Single r and rr',
              [W('p(e:e)ra', 'pera', 'pear', '1f350'), W('ca(r:r)o', 'querido; caro', 'dear; expensive'), W('ca(rr:rr)o', 'carro', 'cart')],
              ('ca(rr:rr)o', 'La r simple es un solo golpe de la lengua: caro. La rr es vibrante, con varias vibraciones: carro. Se parecen a la r de «pero» y a la rr de «perro».',
               'A single r is one tap of the tongue: caro. The rr is rolled, with several vibrations: carro. Hold it longer, and the word changes.'),
              foco='rr', par=('ca(rr:rr)o', 'caro'), oye=('carro', 'caro'), inv=True,
              extras=[sig('caro', ('querido; caro', 'dear; expensive'), ('barato', 'cheap'))],
              construye=('caro', 'u')),
            L('u08l02', 'b y v: no son iguales', 'b and v are not the same',
              [W('(b:b)acio', 'beso', 'kiss', '1f48b'), W('(v:v)ino', 'vino', 'wine', '1f377'), W('(v:v)acca', 'vaca', 'cow', '1f404')],
              ('(v:v)ino', 'En italiano b y v son dos sonidos. Para la b, junta los labios (bacio). Para la v, apoya los dientes de arriba sobre el labio de abajo, como la v inglesa (vino).',
               'In Italian b and v are two sounds. For b, bring your lips together (bacio). For v, put your upper teeth on your lower lip, as in English “v” (vino).'),
              foco='v', par=('(v:v)ino', 'bacio'), oye=('vene', 'bene'),
              extras=[toca('b', '(b:b)acio', 'vino'), cambia('bene', 'vene', ['v', 'b', 'p']), sig('vacca', ('vaca', 'cow'), ('baya', 'berry'))],
              construye=('vino', 'b')),
            L('u08l03', 'Consonantes dobles', 'Double consonants',
              [W('pa(ll:doble)a', 'pelota', 'ball', '26bd'), W('no(nn:doble)o', 'abuelo', 'grandfather', '1f474'), W('ca(pp:doble)ello', 'sombrero', 'hat', '1f9e2')],
              ('pa(ll:doble)a', 'Las consonantes dobles se mantienen más tiempo y cambian el significado: pala (pala) y palla (pelota). Hazlas largas y claras.',
               'Double consonants are held longer and change the meaning: pala (shovel) and palla (ball). Make them long and clear.'),
              foco='doble', par=('pa(ll:doble)a', 'pala'), oye=('palla', 'pala'), inv=True,
              extras=[sig('nonno', ('abuelo', 'grandfather'), ('noveno', 'ninth')), sig('cappello', ('sombrero', 'hat'), ('pelo', 'hair'))],
              construye=('palla', 'e')),
            L('u08l04', 'Pares con dobles', 'Pairs with doubles',
              [W('pe(nn:doble)a', 'bolígrafo', 'pen'), W('se(tt:doble)e', 'siete', 'seven'), W('ca(ss:doble)a', 'caja', 'cash register')],
              ('se(tt:doble)e', 'Mantén más tiempo la doble: sette (siete) frente a sete (sed); penna (bolígrafo) frente a pena (tristeza); cassa (caja) frente a casa (casa).',
               'Hold the double longer: sette (seven) versus sete (thirst); penna (pen) versus pena (sorrow); cassa (cash register) versus casa (house).'),
              foco='doble', par=('se(tt:doble)e', 'sete'), oye=('sette', 'sete'), inv=True,
              extras=[oye('penna', 'pena', inv=True), oye('cassa', 'casa', inv=True), sig('sette', ('siete', 'seven'), ('sed', 'thirst'))],
              construye=('sette', 'a')),
        ],
    },
    {
        'id': 'u09', 'titulo': b('I9 · Acento y acento escrito', 'I9 · Stress and written accent'),
        'objetivo': b('Poner la fuerza en la penúltima sílaba en las palabras llanas y leer el acento escrito, que solo va en la última sílaba (città, perché).',
                      'Stress the next-to-last syllable in most words and read the written accent, which only goes on the last syllable (città, perché).'),
        'lecciones': [
            L('u09l01', 'La fuerza va en la penúltima', 'Stress goes on the next-to-last syllable',
              [W('casa', 'casa', 'house', '1f3e0'), W('amico', 'amigo', 'friend', '1f465'), W('chitarra', 'guitarra', 'guitar', '1f3b8')],
              ('amico', 'La mayoría de las palabras italianas son llanas: la fuerza va en la penúltima sílaba. CA-sa, a-MI-co, chi-TAR-ra.',
               'Most Italian words are stressed on the next-to-last syllable: CA-sa, a-MI-co, chi-TAR-ra.'),
              oye=('casa', 'cosa'),
              extras=[lee('amico', 'amigo', 'friend', '¿Dónde va la fuerza?', 'Where is the stress?', ['a-MI-co', 'A-mi-co']),
                      lee('chitarra', 'guitarra', 'guitar', '¿Dónde va la fuerza?', 'Where is the stress?', ['chi-TAR-ra', 'CHI-tar-ra'])],
              construye=('amico', 'e')),
            L('u09l02', 'Acento escrito: città, caffè', 'Written accent: città, caffè',
              [W('città', 'ciudad', 'city'), W('caffè', 'café', 'coffee', '2615'), W('perché', 'por qué; porque', 'why; because')],
              ('città', 'Cuando una palabra lleva acento escrito, siempre va en la última sílaba, y ahí cae la fuerza: cit-TÀ, caf-FÈ, per-CHÉ, più.',
               'When a word has a written accent, it always sits on the last syllable, and that is where the stress falls: cit-TÀ, caf-FÈ, per-CHÉ, più.'),
              oye=('caffè', 'caffettiera'),
              extras=[lee('caffè', 'café', 'coffee', '¿Dónde va la fuerza?', 'Where is the stress?', ['caf-FÈ', 'CAF-fè']),
                      lee('perché', 'por qué; porque', 'why; because', '¿Dónde va la fuerza?', 'Where is the stress?', ['per-CHÉ', 'PER-ché']),
                      sig('città', ('ciudad', 'city'), ('café', 'coffee'))],
              construye=('città', 'u')),
            L('u09l03', 'è con acento, e sin acento', 'è with accent, e without',
              [W('è', 'es; está', 'is'), W('e', 'y', 'and'), W("c'è", 'hay', 'there is')],
              ('è', 'El acento cambia la palabra: è (con acento) es el verbo «es» o «está»; e (sin acento) es la conjunción «y». Se pronuncian parecido, pero no se escriben igual.',
               'The accent changes the word: è (with accent) is the verb “is”; e (without) is the conjunction “and.” They sound similar, but they are not written the same.'),
              oye=('Giulia', 'Chiara'),
              extras=[sig('è', ('es; está', 'is'), ('y', 'and')), sig('e', ('y', 'and'), ('es; está', 'is')),
                      lee('Marco e Sara', 'Marco y Sara', 'Marco and Sara', '¿Cuál palabra significa «y»?', 'Which word means “and”?', ['e', 'è'])],
              construye=("c'è", 'a')),
            L('u09l04', 'Lee con calma', 'Read calmly',
              [W('lunedì', 'lunes', 'Monday'), W('università', 'universidad', 'university', '1f3eb'), W('più', 'más', 'more')],
              ('lunedì', 'Lee despacio: vocales plenas y la fuerza en su sílaba. lu-ne-DÌ, u-ni-ver-si-TÀ. Los días de la semana van en minúscula.',
               'Read slowly: full vowels and the stress on its syllable. lu-ne-DÌ, u-ni-ver-si-TÀ. Days of the week are written in lowercase.'),
              oye=('università', 'universo'),
              extras=[lee('università', 'universidad', 'university', '¿Dónde va la fuerza?', 'Where is the stress?', ['u-ni-ver-si-TÀ', 'u-ni-VER-si-tà']),
                      mezcla('lunedì', 'lunes', 'Monday')],
              construye=('lunedì', 'e')),
        ],
    },
    {
        'id': 'u10', 'titulo': b('I10 · Ya puedes empezar', 'I10 · You can start now'),
        'objetivo': b('Comprobar que lees y oyes los sonidos del italiano: carteles, contrastes, palabras nuevas y una primera frase.',
                      'Check that you can read and hear Italian sounds: signs, contrasts, new words and a first sentence.'),
        'lecciones': [
            L('u10l01', 'Lee carteles', 'Read signs',
              [W('entrata', 'entrada', 'entrance', '1f6aa'), W('uscita', 'salida', 'exit'), W('aperto', 'abierto', 'open'), W('chiuso', 'cerrado', 'closed')],
              ('ENTRATA · USCITA', 'Los carteles suelen ir en mayúsculas. El sonido no cambia: lee primero la palabra clave.',
               'Signs are often in capitals. The sound does not change: read the key word first.'),
              oye=('uscita', 'entrata'),
              extras=[lee('USCITA · ENTRATA', 'SALIDA · ENTRADA', 'EXIT · ENTRANCE', '¿Qué palabra indica por dónde salir?', 'Which word tells you where to exit?', ['USCITA', 'ENTRATA']),
                      lee('APERTO', 'abierto', 'open', '¿El lugar está abierto o cerrado?', 'Is the place open or closed?', ['aperto', 'chiuso']),
                      lee('Cegnoli', *PSEUDO, *CUAL_INVENTADA, ['pesce', 'Cegnoli'], 1)],
              construye=('aperto', 'e')),
            L('u10l02', 'Contrastes', 'Contrasts',
              [W('ami(ch:k)e', 'amigas', 'female friends'), W('pe(sc:sh)e', 'pescado', 'fish', '1f41f'), W('pa(ll:doble)a', 'pelota', 'ball', '26bd')],
              ('ami(ch:k)e', 'Repaso: c y ch (amici, amiche), sc y sch (pesce, pesche), simples y dobles (pala, palla, caro, carro).',
               'Review: c and ch (amici, amiche), sc and sch (pesce, pesche), single and double (pala, palla, caro, carro).'),
              foco='doble', par=('pa(ll:doble)a', 'pala'), oye=('amiche', 'amici'),
              extras=[oye('pesche', 'pesce'), oye('carro', 'caro', inv=True), oye('bene', 'vene'),
                      toca('sk', 'ma(sch:sk)era', 'pesce'), toca('gn', 'ba(gn:gn)o', 'banco')],
              construye=('pesce', 'a')),
            L('u10l03', 'Palabras nuevas', 'New words',
              [W('(qu:qu)aderno', 'cuaderno', 'notebook'), W('(g:j)iardino', 'jardín', 'garden', '1f331'), W('(gn:gn)occhi', 'ñoquis', 'gnocchi')],
              ('(qu:qu)aderno', 'Estas palabras son nuevas, pero ya conoces sus reglas: qu = «cu», gi = «ji» inglesa, gn = «ñ», cchi = «k» larga.',
               'These words are new, but you know their rules: qu = “kw,” gi = English “j,” gn = “ny,” cchi = a long “k.”'),
              foco='qu', par=('(qu:qu)aderno', 'giardino'), oye=('giardino', 'giallo'),
              extras=[lee('Quegnile', *PSEUDO, *CUAL_INVENTADA, ['Quegnile', 'quaderno']),
                      sig('giardino', ('jardín', 'garden'), ('cuaderno', 'notebook'))],
              construye=('giardino', 'e')),
            L('u10l04', 'Tu primera frase', 'Your first sentence',
              [W('Ciao!', 'hola; chao', 'hi; bye', '1f44b'), W('Mi chiamo Chiara.', 'me llamo Chiara', 'my name is Chiara'), W('Arrivederci!', 'hasta luego', 'goodbye')],
              ('Ciao! Mi chiamo Chiara.', 'Junta todo: ci = «chi», chi = «ki», la rr de Arrivederci. ¡Ya puedes empezar Fundamentos!',
               'Put it all together: ci = “chee,” chi = “kee,” the rr in Arrivederci. You are ready for Foundations!'),
              oye=('ciao', 'chiaro'),
              extras=[lee('Arrivederci!', 'hasta luego', 'goodbye', '¿Es un saludo o una despedida?', 'Is it a greeting or a goodbye?', ['Buongiorno', 'Arrivederci'], 1),
                      deletreo('Chiara', 'Escucha y ordena las letras de Chiara.', 'Listen and put the letters of Chiara in order.')],
              construye=('ciao', 'e')),
        ],
    },
]


def nivel0_json():
    return {
        'esquema': 'onelingo.nivel0.v1',
        'idioma': 'it',
        'titulo': b('Nivel 0 · Leer y pronunciar italiano', 'Level 0 · Read and pronounce Italian'),
        'subtitulo': b('Para quien empieza desde cero: cómo suenan las letras italianas y cómo leerlas.',
                       'For complete beginners: how Italian letters sound and how to read them.'),
        'voz': 'narradora',
        'nota': 'Marcado: (letras:sonido) pinta las letras con el color del sonido (ver sonidos.json); _ = letra que no suena (h). Fuente: tools/contenido/nivel0-it/generar.py. Apoyo es + en.',
        'textos': {
            'tarjeta': b('¿Empiezas de cero? Cómo suenan las letras italianas y cómo leerlas.', 'Starting from zero? How Italian letters sound and how to read them.'),
            'muestra': '(c:ch)iao · (gn:gn)occhi · pa(ll:doble)a',
            'emoji': '1f3e0',
            'junta': b('Escucha despacio y después rápido: así se lee el italiano.', 'Listen slowly, then fast: that is how you read Italian.'),
            'mapaIntro': b('El italiano se lee de forma muy regular y las vocales son siempre claras. Lo nuevo son c y g ante e, i, los grupos ch, gh, gn, gli, sc, la z, la h muda y las consonantes dobles. Cada sonido tiene una imagen y un color que verás en las palabras. Toca una tarjeta para oírla.',
                           'Italian is read very regularly and the vowels are always clear. What is new: c and g before e, i, the groups ch, gh, gn, gli, sc, the z, the silent h and double consonants. Each sound has a picture and a color you will see in the words. Tap a card to hear it.'),
            'grupos': GRUPOS,
        },
        'revision': 'inicial',
        'refuerzo': {'alfabeto': 'u02', 'vocales': 'u03', 'suaves': 'u04', 'duras': 'u05',
                     'unidos': 'u06', 'consonantes': 'u07', 'dobles': 'u08', 'acento': 'u09'},
        'evaluacion': {'lecciones': ['u10l01', 'u10l02', 'u10l03', 'u10l04'], 'pseudopalabras': ['Cegnoli', 'Quegnile'], 'umbral': 0.8},
        'unidades': UNIDADES,
    }


def escribir(nombre, datos):
    (DESTINO / nombre).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    DESTINO.mkdir(parents=True, exist_ok=True)
    escribir('sonidos.json', sonidos_json())
    escribir('nivel0.json', nivel0_json())
    r = subprocess.run([sys.executable, str(RAIZ / 'tools/contenido/validar_nivel0.py'), 'it',
                        str(DESTINO / 'nivel0.json'), '--bilingue'])
    sys.exit(r.returncode)
