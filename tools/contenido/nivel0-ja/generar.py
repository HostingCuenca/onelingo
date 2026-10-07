#!/usr/bin/env python3
"""Genera el Nivel 0 «Leer y pronunciar japonés» (hiragana y katakana).

Escribe assets/contenido/ja/nivel0/sonidos.json y nivel0.json desde los datos
de este archivo y termina con `validar_nivel0.py ja --bilingue`.
Misma estructura que el Nivel 0 del italiano (tools/contenido/nivel0-it).
Apoyo bilingüe {es, en}: español latino neutro con «tú», inglés americano.
Japonés estándar, registro cortés; sin historia continua; nombres solo de
tools/ia/idiomas/ja.md; sin kanji; sin cifras en ningún texto.
Lumo solo en la bienvenida (u01l01), nunca en la evaluación (u10).
Reglas: solo las guías de pronunciación y el rōmaji Hepburn modificado de
tools/ia/idiomas/ja.md. El texto japonés lleva un espacio entre palabras y las
partículas aparte.
Imágenes: solo emoji Noto ya presentes en assets/img/emoji/.

El marcado (kana:sonido) y el `rom` de cada palabra se calculan solos desde
el kana (funciones mk y R); el generador comprueba además que cada lección
solo usa kana y sonidos ya enseñados.

20 claves (curriculo/ja/f0.json · previos) → unidades:
  hiragana-vowels u01 · hiragana-k, hiragana-s u02 · hiragana-t, hiragana-n u03 ·
  hiragana-h, hiragana-m, hiragana-y u04 ·
  hiragana-r, hiragana-w, hiragana-n-final, particle-readings u05 ·
  dakuten-handakuten u06 · youon-combos, sokuon-small-tsu u07 ·
  long-vowels, devoiced-vowels, pitch-accent u08 ·
  katakana-basic, katakana-loanwords u09 · prueba de salida u10.

Uso: python3 tools/contenido/nivel0-ja/generar.py
"""
import json
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
DESTINO = RAIZ / 'assets/contenido/ja/nivel0'
GRUPO = re.compile(r'\(([^():]+):([^()]+)\)')


def b(es, en):
    return {'es': es, 'en': en}


def plano(m):
    return GRUPO.sub(lambda g: g.group(1), m)


# ── Kana: sonido, rōmaji y marcado automáticos ───────────────────────────────
SND, ROMH = {}, {}


def _fila(sid, chars, roms):
    for c, r in zip(chars, roms.split()):
        SND[c] = sid if sid else r
        ROMH[c] = r


_fila(None, 'あいうえお', 'a i u e o')
_fila('k', 'かきくけこ', 'ka ki ku ke ko')
_fila('s', 'さしすせそ', 'sa shi su se so')
_fila('t', 'たちつてと', 'ta chi tsu te to')
_fila('n', 'なにぬねの', 'na ni nu ne no')
_fila('h', 'はひふへほ', 'ha hi fu he ho')
_fila('m', 'まみむめも', 'ma mi mu me mo')
_fila('y', 'やゆよ', 'ya yu yo')
_fila('r', 'らりるれろ', 'ra ri ru re ro')
_fila('w', 'わを', 'wa o')
_fila('nn', 'ん', 'n')
_fila('g', 'がぎぐげご', 'ga gi gu ge go')
_fila('z', 'ざじずぜぞ', 'za ji zu ze zo')
_fila('d', 'だぢづでど', 'da ji zu de do')
_fila('b', 'ばびぶべぼ', 'ba bi bu be bo')
_fila('p', 'ぱぴぷぺぽ', 'pa pi pu pe po')
PUNT = {'。': '.', '、': ',', '！': '!', '？': '?'}
PART = {'は': 'wa', 'へ': 'e', 'を': 'o'}
NOMBRES = {'メキシコ', 'アメリカ', 'スペイン', 'イタリア', 'チリ', 'ペルー', 'コロンビア', 'アルゼンチン', 'スイス',
           'にほん', 'とうきょう', 'おおさか', 'きょうと', 'さくら'}  # nombres propios de la ficha: rom con mayúscula
FIJAS = {'こんにちは': 'konnichiwa', 'こんばんは': 'konbanwa'}
MAC = {'a': 'ā', 'i': 'ī', 'u': 'ū', 'e': 'ē', 'o': 'ō'}
LARGAS = {('あ', 'a'), ('い', 'i'), ('う', 'u'), ('え', 'e'), ('お', 'o'), ('う', 'o')}


def hira(c):
    return chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c


def _alargar(p, c):
    r = p['r']
    p['r'] = r + 'i' if (c == 'い' and r[-1] == 'i') else r[:-1] + MAC[r[-1]]


def analizar(tok):
    """Moras de una palabra: {k: kana, r: rōmaji, s: sonido, v: vocal final}."""
    out, h, i = [], [hira(c) for c in tok], 0
    while i < len(tok):
        c = h[i]
        if c == 'っ':
            out.append({'k': tok[i], 'r': '', 's': 'sokuon', 'sok': True})
        elif c == 'ー':
            _alargar(out[-1], 'ー')
            out.append({'k': tok[i], 'r': '', 's': 'largo'})
        elif c == 'ん':
            sig = h[i + 1] if i + 1 < len(tok) else ''
            out.append({'k': tok[i], 'r': "n'" if sig and sig in 'あいうえおやゆよ' else 'n', 's': 'nn'})
        else:
            base, k, s = ROMH[c], tok[i], SND[c]
            if i + 1 < len(tok) and h[i + 1] in 'ゃゅょ':
                v = {'ゃ': 'a', 'ゅ': 'u', 'ょ': 'o'}[h[i + 1]]
                r = base[:-1] + v if base in ('shi', 'chi', 'ji') else base[:-1] + 'y' + v
                out.append({'k': k + tok[i + 1], 'r': r, 's': 'yoon', 'v': v})
                i += 2
                continue
            prev = out[-1] if out else None
            if c in 'あいうえお' and prev and prev.get('v') and (c, prev['v']) in LARGAS:
                _alargar(prev, c)
                out.append({'k': k, 'r': '', 's': 'largo'})
            elif c == 'い' and prev and prev.get('v') == 'e':
                out.append({'k': k, 'r': 'i', 's': 'largo', 'v': 'i'})
            else:
                out.append({'k': k, 'r': base, 's': s, 'v': base[-1] if base[-1] in 'aiueo' else None})
        i += 1
    return out


def _tokens(m):
    for tok in m.split(' '):
        core = tok.rstrip('。、！？')
        yield core, tok[len(core):]


def _part(core, m):
    """は, へ, を sueltos son partículas, salvo en una tabla de kana sueltos (は ひ ふ へ ほ)."""
    if core not in PART:
        return False
    toks = [t.rstrip('。、！？') for t in m.split(' ')]
    return m == 'は へ を' or any(len(t) > 1 for t in toks)


def R(m, nombre=False):
    """Rōmaji Hepburn modificado de una palabra o frase."""
    partes = []
    for core, punt in _tokens(m):
        if _part(core, m):
            r = PART[core]
        elif core in FIJAS:
            r = FIJAS[core]
        else:
            r, pend = '', False
            for x in analizar(core):
                if x.get('sok'):
                    pend = True
                    continue
                t = x['r']
                if pend:
                    t = ('t' + t) if t[:2] in ('ch', 'ts') else ('s' + t) if t[:2] == 'sh' else t[0] + t
                    pend = False
                r += t
        if core in NOMBRES:
            r = r[0].upper() + r[1:]
        partes.append(r + ''.join(PUNT[p] for p in punt))
    s = ' '.join(partes)
    if re.search('[。！？]', m):
        s = re.sub(r'(^|[.!?] )(\S)', lambda g: g.group(1) + g.group(2).upper(), s)
    return s


def mk(m):
    """Marcado (kana:sonido): cada mora lleva el color de su fila."""
    partes = []
    for core, punt in _tokens(m):
        if _part(core, m):
            t = f'({core}:part)'
        else:
            ms = analizar(core)
            if core in FIJAS:
                ms[-1]['s'] = 'part'
            t = ''.join(f"({x['k']}:{x['s']})" for x in ms)
        partes.append(t + punt)
    return ' '.join(partes)


# ── Mapa de sonidos ──────────────────────────────────────────────────────────
# (id, grupo, color, colorNombre es, en, ancla, emoji, nombre es, en, grafías, ejemplos, unidad)
def _g(*filas):
    return [c for f in filas for c in f]


SONIDOS = [
    ('a', 'vocal', '#E24B4A', 'rojo', 'red', 'あり', '1f41c', 'あ: la a de «casa»', 'あ: the a in “father”', ['あ', 'ア'], ['あい', 'あお', 'あさ'], 1),
    ('i', 'vocal', '#E0559B', 'rosa', 'pink', 'いぬ', '1f436', 'い: la i de «ir»', 'い: the ee in “see,” a bit shorter', ['い', 'イ'], ['いぬ', 'いえ', 'いす'], 1),
    ('u', 'vocal', '#1E88E5', 'azul', 'blue', 'うま', '1f434', 'う: una u con los labios sin redondear', 'う: an oo with unrounded lips', ['う', 'ウ'], ['うま', 'うえ', 'くつ'], 1),
    ('e', 'vocal', '#E8B923', 'amarillo', 'yellow', 'えき', '1f686', 'え: la e de «mesa»', 'え: the e in “bed”', ['え', 'エ'], ['えき', 'いえ', 'え'], 1),
    ('o', 'vocal', '#2E8B57', 'verde', 'green', 'おかし', '1f36c', 'お: la o de «foto»', 'お: the o in “more,” without the glide', ['お', 'オ'], ['おかし', 'あお', 'こえ'], 1),
    ('k', 'fila', '#455A64', 'pizarra', 'slate', 'かめ', '1f422', 'か行: k + vocal', 'か row: k + vowel', ['か', 'き', 'く', 'け', 'こ'], ['かめ', 'かお', 'ここ'], 2),
    ('s', 'fila', '#C2185B', 'frambuesa', 'raspberry', 'さる', '1f412', 'さ行: s + vocal; し suena «shi»', 'さ row: s + vowel; し is “shi”', ['さ', 'し', 'す', 'せ', 'そ'], ['さる', 'すし', 'しお'], 2),
    ('t', 'fila', '#FF7043', 'coral', 'coral', 'とり', '1f426', 'た行: t + vocal; ち «chi», つ «tsu»', 'た row: t + vowel; ち “chee,” つ “tsu”', ['た', 'ち', 'つ', 'て', 'と'], ['とり', 'つき', 'くつ'], 3),
    ('n', 'fila', '#6B8E23', 'oliva', 'olive', 'ねこ', '1f431', 'な行: n + vocal', 'な row: n + vowel', ['な', 'に', 'ぬ', 'ね', 'の'], ['ねこ', 'いぬ', 'なつ'], 3),
    ('h', 'fila', '#D4A017', 'dorado', 'gold', 'ひまわり', '1f33b', 'は行: h + vocal; ふ se sopla entre los labios', 'は row: h + vowel; ふ is blown between the lips', ['は', 'ひ', 'ふ', 'へ', 'ほ'], ['ひまわり', 'ふね', 'ほし'], 4),
    ('m', 'fila', '#F08A24', 'naranja', 'orange', 'みかん', '1f34a', 'ま行: m + vocal', 'ま row: m + vowel', ['ま', 'み', 'む', 'め', 'も'], ['みかん', 'うま', 'いま'], 4),
    ('y', 'fila', '#00A6A6', 'turquesa', 'teal', 'やま', '26f0', 'や行: ya, yu, yo', 'や row: ya, yu, yo', ['や', 'ゆ', 'よ'], ['やま', 'ゆき', 'やさい'], 4),
    ('r', 'fila', '#AD1457', 'granate', 'maroon', 'りんご', '1f34e', 'ら行: una r simple y rápida, la de «pero»', 'ら row: one quick tap, like the tt in “butter”', ['ら', 'り', 'る', 'れ', 'ろ'], ['りんご', 'そら', 'くるま'], 5),
    ('w', 'fila', '#9C6ADE', 'lila', 'lilac', 'わに', '1f40a', 'わ, を: wa y o', 'わ, を: wa and o', ['わ', 'を'], ['わに', 'わたし', 'かわ'], 5),
    ('nn', 'especial', '#8D6E63', 'café con leche', 'latte', 'ほん', '1f4d6', 'ん: un golpe propio, nasal', 'ん: its own beat, nasal', ['ん', 'ン'], ['ほん', 'みかん', 'にほん'], 5),
    ('part', 'especial', '#3949AB', 'índigo', 'indigo', 'は', '1f449', 'Partículas: は se lee «wa», へ «e», を «o»', 'Particles: は is read “wa,” へ “e,” を “o”', ['は', 'へ', 'を'], ['わたし は', 'にほん へ', 'ほん を'], 5),
    ('g', 'sonoro', '#5D4037', 'café', 'coffee', 'ごはん', '1f35a', 'が行: g dura + vocal', 'が row: hard g + vowel', ['が', 'ぎ', 'ぐ', 'げ', 'ご'], ['ごはん', 'かぎ', 'げんき'], 6),
    ('z', 'sonoro', '#26A69A', 'verde agua', 'aqua', 'かぜ', '1f32c', 'ざ行: z + vocal; じ «yi» fuerte, ず «dsu»', 'ざ row: z + vowel; じ “jee,” ず “dzu”', ['ざ', 'じ', 'ず', 'ぜ', 'ぞ'], ['かぜ', 'みず', 'じかん'], 6),
    ('d', 'sonoro', '#C0CA33', 'pistacho', 'pistachio', 'でんわ', '260e', 'だ行: d + vocal', 'だ row: d + vowel', ['だ', 'ぢ', 'づ', 'で', 'ど'], ['でんわ', 'ともだち', 'どこ'], 6),
    ('b', 'sonoro', '#D84315', 'teja', 'brick', 'ばら', '1f339', 'ば行: b + vocal', 'ば row: b + vowel', ['ば', 'び', 'ぶ', 'べ', 'ぼ'], ['ばら', 'かばん', 'ぶた'], 6),
    ('p', 'sonoro', '#7CB342', 'lima', 'lime', 'ぺんぎん', '1f427', 'ぱ行: p + vocal', 'ぱ row: p + vowel', ['ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ'], ['ぺんぎん', 'さんぽ', 'えんぴつ'], 6),
    ('yoon', 'especial', '#1565C0', 'azul cobalto', 'cobalt', 'おちゃ', '1f375', 'きゃ, しゅ, ちょ…: una i + ゃ ゅ ょ pequeña, un solo golpe', 'きゃ, しゅ, ちょ…: an i-kana + small ゃ ゅ ょ, one single beat', ['きゃ', 'しゅ', 'ちょ', 'じゃ', 'りょ'], ['おちゃ', 'しゃしん', 'しゅみ'], 7),
    ('sokuon', 'especial', '#E0559B', 'rosa fuerte', 'hot pink', 'サッカー', '26bd', 'っ: pausa de un golpe antes de la consonante', 'っ: a one-beat pause before the consonant', ['っ', 'ッ'], ['きって', 'ざっし', 'サッカー'], 7),
    ('largo', 'especial', '#7E57C2', 'violeta', 'violet', 'おかあさん', '1f469', 'Vocal larga: dos golpes; ー en katakana', 'Long vowel: two beats; ー in katakana', ['ああ', 'いい', 'うう', 'えい', 'おう', 'ー'], ['おかあさん', 'せんせい', 'コーヒー'], 8),
]

GRUPOS = {
    'vocal': b('Las cinco vocales', 'The five vowels'),
    'fila': b('Filas del kana', 'Kana rows'),
    'sonoro': b('Dakuten y handakuten', 'Dakuten and handakuten'),
    'especial': b('ん, partículas, combinaciones, っ y vocales largas', 'ん, particles, combinations, っ and long vowels'),
}
UNIDAD_DE = {s[0]: s[11] for s in SONIDOS}


def sonidos_json():
    return {
        'esquema': 'onelingo.sonidos.v1',
        'idioma': 'ja',
        'nota': 'Mapa de sonidos del japonés estándar (Tokio). Cada fila de kana tiene su color, igual en hiragana y en katakana; el color acompaña siempre al nombre y a la imagen. Es una pista de escucha, no una transcripción fonética.',
        'marcas': {'=': 'varios kana, un solo golpe (por ejemplo きゃ)'},
        'acento': b('Modelo: japonés estándar. El tono alto y bajo de cada palabra se oye, pero no se marca ni se evalúa.',
                    'Model: standard Japanese. The high and low pitch of each word is heard, but it is not marked or tested.'),
        'vocales': [
            {'id': i, 'grupo': g, 'color': c, 'colorNombre': b(ces, cen), 'ancla': a, 'emoji': e,
             'nombre': b(nes, nen), 'grafias': gr, 'ejemplos': ej, 'unidad': u}
            for i, g, c, ces, cen, a, e, nes, nen, gr, ej, u in SONIDOS
        ],
    }


# ── Lecciones ────────────────────────────────────────────────────────────────
LECCION_NUEVOS = {}  # id de lección → kana que se enseñan por primera vez en ella


def W(m, es, en, e=None, nombre=False):
    w = {'m': mk(m), 'rom': R(m, nombre), 't': b(es, en)}
    if e:
        w['e'] = e
    return w


ESCUCHA_ELIGE = b('¿Qué palabra oyes?', 'Which word do you hear?')
TOCA = b('Escucha y toca la palabra con el sonido marcado.', 'Listen and tap the word with the marked sound.')
CUAL_INVENTADA = ('¿Cuál es la palabra inventada?', 'Which word is made up?')
PSEUDO = ('Pseudopalabra: no significa nada; léela con las reglas que conoces.', 'Pseudoword: it means nothing; read it with the rules you know.')


def mira(m, es, en, foco=None, nota=None):
    paso = {'tipo': 'mira', 'm': mk(m), 'rom': R(m), 'texto': b(es, en)}
    if foco:
        paso['sonido'] = foco
    if nota:
        paso['nota'] = b(*nota)
    return paso


def toca(foco, si, no, inv=False):
    ops = [{'m': mk(si)}, {'m': mk(no)}]
    if inv:
        ops.reverse()
    return {'tipo': 'toca_sonido', 'sonido': foco, 'pregunta': TOCA, 'opciones': ops, 'correcta': 1 if inv else 0}


def oye(correcta, otra, inv=False):
    ops = [{'m': correcta}, {'m': otra}]
    if inv:
        ops.reverse()
    return {'tipo': 'escucha_elige', 'audio': plano(correcta), 'pregunta': ESCUCHA_ELIGE,
            'opciones': ops, 'correcta': 1 if inv else 0}


def L(lid, tes, ten, nuevos, palabras, m0, foco=None, par=None, o=None, extras=(), construye=None, inv=False):
    """Plantilla: escucha → mira → repite → [toca_sonido] → [escucha_elige] → extras → construye.
    m0 = (kana, es, en[, (nota es, nota en)]); par = (con el sonido foco, sin él); o = (correcta, distractor)."""
    LECCION_NUEVOS[lid] = nuevos
    pasos = [{'tipo': 'escucha', 'palabras': palabras}, mira(m0[0], m0[1], m0[2], foco, m0[3] if len(m0) > 3 else None)]
    p0 = palabras[0]
    pasos.append({'tipo': 'repite', 'm': p0['m'], 'rom': p0['rom'], 't': p0['t']})
    if foco and par:
        pasos.append(toca(foco, par[0], par[1], inv))
    if o:
        pasos.append(oye(o[0], o[1], not inv))
    pasos += list(extras)
    if construye:
        m, extra = construye
        pasos.append({'tipo': 'construye', 'm': m, 'rom': R(m), 'fichas': list(m) + [extra]})
    return {'id': lid, 'titulo': b(tes, ten), 'pasos': pasos}


def lee(m, tes, ten, pes, pen, ops, correcta=0):
    return {'tipo': 'lee', 'm': m, 'rom': R(m), 't': b(tes, ten), 'pregunta': b(pes, pen),
            'opciones': [{'m': o, 'rom': R(o)} for o in ops], 'correcta': correcta}


def sig(m, pes, pen, ops=None):
    """«¿Qué significa?» con dos opciones (la primera es la correcta)."""
    return {'tipo': 'elige_significado', 'm': m, 'rom': R(m), 'pregunta': b('¿Qué significa?', 'What does it mean?'),
            'opciones': [b(*pes), b(*pen)], 'correcta': 0}


def cambia(de, a, ops):
    return {'tipo': 'cambia', 'de': de, 'a': a, 'opciones': ops}


def letra(l, ops):
    return {'tipo': 'escucha_letra', 'letra': l, 'letraRom': R(l),
            'pregunta': b('Toca el kana que oyes.', 'Tap the kana you hear.'), 'opciones': ops}


def deletreo(m, es, en):
    return {'tipo': 'deletreo', 'm': m, 'rom': R(m), 'pregunta': b(es, en), 'opciones': list(m), 'correcta': 0}


def mezcla(m, es, en):
    return {'tipo': 'mezcla', 'm': m, 'rom': R(m), 't': b(es, en)}


UNIDADES = [
    {
        'id': 'u01', 'titulo': b('J1 · Las vocales', 'J1 · The vowels'),
        'objetivo': b('Entender cómo se escribe el japonés, contar golpes y leer las cinco vocales あ い う え お.',
                      'Understand how Japanese is written, count beats and read the five vowels あ い う え お.'),
        'lecciones': [
            L('u01l01', 'Hola, hiragana', 'Hello, hiragana', 'あいうえお',
              [W('あい', 'amor', 'love', '2764'), W('いえ', 'casa', 'house', '1f3e0'), W('うえ', 'arriba', 'up; above', '1f446')],
              ('あ い う え お',
               'El japonés se escribe con tres sistemas: hiragana, katakana y kanji. Empiezas por el hiragana. Cada signo, o kana, es un golpe de igual duración y no hay una sílaba fuerte como en español. Estas son las cinco vocales: a, i, u, e, o.',
               'Japanese is written with three systems: hiragana, katakana and kanji. You start with hiragana. Each sign, or kana, is one beat of equal length, and there is no heavy stressed syllable. These are the five vowels: a, i, u, e, o.',
               ('Las vocales son siempre puras: no se reducen ni se diptongan.', 'The vowels are always pure: never reduced, never a glide.')),
              foco='a', par=('あい', 'いえ'), o=('あい', 'いえ'),
              extras=[
                  {'tipo': 'lumo', 'pose': 'anima', 'texto': b('Bienvenido al japonés. Primero escucharás, después leerás. ¡Cada fila de kana tiene su color para ayudarte a recordarla!',
                                                              'Welcome to Japanese. First you listen, then you read. Each row of kana has its own color to help you remember it!')},
                  sig('あい', ('amor', 'love'), ('casa', 'house')),
                  letra('あ', ['あ', 'い', 'う']),
              ],
              construye=('あい', 'う')),
            L('u01l02', 'う: sin redondear los labios', 'う: with unrounded lips', '',
              [W('うえ', 'arriba', 'up; above', '1f446'), W('あう', 'encontrarse', 'to meet'), W('いう', 'decir', 'to say')],
              ('う', 'う no es la «u» española: no redondees ni proyectes los labios. Suena entre «u» e «i», con los labios relajados.',
               'う is not a rounded “oo”: keep your lips relaxed, not rounded or pushed forward. It sounds between “oo” and “ee.”'),
              foco='u', par=('うえ', 'いえ'), o=('うえ', 'いえ'),
              extras=[cambia('いえ', 'うえ', ['う', 'あ', 'お']), sig('いう', ('decir', 'to say'), ('comer', 'to eat'))],
              construye=('うえ', 'お')),
            L('u01l03', 'え y お', 'え and お', '',
              [W('え', 'dibujo', 'picture', '1f3a8'), W('あお', 'azul', 'blue', '1f535'), W('あおい', 'azul (adjetivo)', 'blue (adjective)')],
              ('え お', 'え suena como la «e» de «mesa» y お como la «o» de «foto». Las dos son cortas y puras: nunca suenan «ei» ni «ou».',
               'え sounds like the e in “bed” and お like the o in “more.” Both are short and pure: never “ay” or “oh-oo.”'),
              foco='o', par=('あお', 'あい'), o=('あお', 'あい'),
              extras=[cambia('あお', 'あい', ['い', 'お', 'う']), sig('え', ('dibujo', 'picture'), ('mano', 'hand')), letra('お', ['お', 'う', 'え'])],
              construye=('あお', 'い')),
            L('u01l04', 'Lee y escucha', 'Read and listen', '',
              [W('あい', 'amor', 'love', '2764'), W('いえ', 'casa', 'house', '1f3e0'), W('あお', 'azul', 'blue', '1f535')],
              ('あい いえ うえ あお', 'Ya lees cuatro palabras: あい «amor», いえ «casa», うえ «arriba» y あお «azul». Cada kana es un golpe: あ-い, い-え, う-え, あ-お.',
               'You can already read four words: あい “love,” いえ “house,” うえ “up” and あお “blue.” Each kana is one beat: あ-い, い-え, う-え, あ-お.'),
              foco='e', par=('いえ', 'あお'), o=('いえ', 'うえ'),
              extras=[lee('あおい', 'azul (adjetivo)', 'blue (adjective)', '¿Cuál palabra significa «arriba»?', 'Which word means “up”?', ['うえ', 'あおい']),
                      sig('うえ', ('arriba', 'up'), ('casa', 'house')), mezcla('うえ', 'arriba', 'up')],
              construye=('いえ', 'う')),
        ],
    },
    {
        'id': 'u02', 'titulo': b('J2 · Las filas か y さ', 'J2 · The か and さ rows'),
        'objetivo': b('Leer las filas か (k) y さ (s), con す sin redondear y し «shi», y tus primeras palabras con consonante.',
                      'Read the か (k) and さ (s) rows, with す unrounded and し “shi,” and your first words with consonants.'),
        'lecciones': [
            L('u02l01', 'か き く け こ', 'か き く け こ', 'かきくけこ',
              [W('かお', 'rostro', 'face'), W('いく', 'ir', 'to go'), W('ここ', 'aquí', 'here')],
              ('か き く け こ', 'La fila か es k + vocal: か ka, き ki, く ku, け ke, こ ko. La k es la de «casa». Cada kana sigue siendo un solo golpe.',
               'The か row is k + vowel: か ka, き ki, く ku, け ke, こ ko. The k is like the k in “sky.” Each kana is still one single beat.'),
              foco='k', par=('かお', 'あお'), o=('かお', 'あお'),
              extras=[letra('か', ['か', 'き', 'こ']), cambia('かお', 'かう', ['う', 'お', 'き']), sig('かお', ('rostro', 'face'), ('casa', 'house'))],
              construye=('いく', 'こ')),
            L('u02l02', 'Palabras con か行', 'Words with the か row', '',
              [W('あき', 'otoño', 'autumn'), W('こえ', 'voz', 'voice'), W('かく', 'escribir', 'to write')],
              ('あき いけ きく こえ', 'Cuenta los golpes: あき son dos, いけ son dos, きく son dos y こえ son dos. Cada kana dura lo mismo.',
               'Count the beats: あき is two, いけ is two, きく is two and こえ is two. Every kana lasts the same.'),
              foco='k', par=('きく', 'いえ'), o=('あき', 'あい'),
              extras=[sig('きく', ('escuchar', 'to listen'), ('escribir', 'to write')), mezcla('こえ', 'voz', 'voice'), letra('く', ['く', 'け', 'き'])],
              construye=('あき', 'く')),
            L('u02l03', 'さ し す せ そ', 'さ し す せ そ', 'さしすせそ',
              [W('あさ', 'mañana (la hora del día)', 'morning'), W('いす', 'silla', 'chair', '1fa91'), W('しお', 'sal', 'salt')],
              ('さ し す せ そ', 'La fila さ es s + vocal: さ sa, し shi, す su, せ se, そ so. Cuidado con し: suena «shi» (la «sh» inglesa), no «si». す se dice con los labios relajados, como う.',
               'The さ row is s + vowel: さ sa, し shi, す su, せ se, そ so. Careful with し: it is “shee,” not “see.” す is said with relaxed lips, like う.',
               ('し: «shi», no «si».', 'し: “shi,” not “si.”')),
              foco='s', par=('あさ', 'あき'), o=('あさ', 'あき'),
              extras=[letra('し', ['し', 'す', 'せ']), cambia('あさ', 'あき', ['き', 'さ', 'く']), sig('しお', ('sal', 'salt'), ('azúcar', 'sugar'))],
              construye=('いす', 'し')),
            L('u02l04', 'Palabras con k y s', 'Words with k and s', '',
              [W('すし', 'sushi', 'sushi'), W('すこし', 'un poco', 'a little'), W('せかい', 'mundo', 'world', '1f30d')],
              ('すき おかし せかい すこし', 'Junta las dos filas: すき «me gusta», おかし «dulces», せかい «mundo» y すこし «un poco». Lee cada kana con la misma duración.',
               'Put the two rows together: すき “I like,” おかし “sweets,” せかい “world” and すこし “a little.” Read every kana with the same length.'),
              foco='s', par=('すこし', 'かお'), o=('すし', 'すき'),
              extras=[sig('せかい', ('mundo', 'world'), ('país', 'country')),
                      lee('すき', 'me gusta', 'I like', '¿Cuál palabra significa «un poco»?', 'Which word means “a little”?', ['すこし', 'すき']),
                      mezcla('おかし', 'dulces', 'sweets')],
              construye=('すこし', 'き')),
        ],
    },
    {
        'id': 'u03', 'titulo': b('J3 · Las filas た y な', 'J3 · The た and な rows'),
        'objetivo': b('Leer las filas た (t) y な (n), con ち «chi» y つ «tsu», y ya más de veinte palabras.',
                      'Read the た (t) and な (n) rows, with ち “chi” and つ “tsu,” and more than twenty words already.'),
        'lecciones': [
            L('u03l01', 'た ち つ て と', 'た ち つ て と', 'たちつてと',
              [W('たこ', 'pulpo', 'octopus'), W('つき', 'luna', 'moon', '1f319'), W('くつ', 'zapatos', 'shoes', '1f45e')],
              ('た ち つ て と', 'La fila た es t + vocal, con dos excepciones: ち se lee «chi» (como «chico») y つ se lee «tsu», en una sola sílaba, como el inicio de «tsunami». Nunca «tu» ni «chu».',
               'The た row is t + vowel, with two exceptions: ち is “chee” and つ is “tsu,” one syllable, like the end of “cats” plus “oo.” Never “too” or “choo.”',
               ('つ: «tsu», nunca «tu».', 'つ: “tsu,” never “too.”')),
              foco='t', par=('たこ', 'かお'), o=('たこ', 'かこ'),
              extras=[letra('つ', ['つ', 'す', 'ち']), sig('くつ', ('zapatos', 'shoes'), ('sombrero', 'hat')), cambia('たこ', 'かこ', ['か', 'た', 'さ'])],
              construye=('つき', 'た')),
            L('u03l02', 'Palabras con た行', 'Words with the た row', '',
              [W('くち', 'boca', 'mouth', '1f444'), W('て', 'mano', 'hand', '270b'), W('あした', 'mañana (el día siguiente)', 'tomorrow')],
              ('くち て あした たかい', 'Lee despacio y cuenta los golpes: て es un solo golpe, くち son dos, あした son tres y たかい son tres. たかい significa «alto» o «caro».',
               'Read slowly and count the beats: て is one beat, くち is two, あした is three and たかい is three. たかい means “tall” or “expensive.”'),
              foco='t', par=('あした', 'あさ'), o=('あした', 'あさ'),
              extras=[sig('たかい', ('alto; caro', 'tall; expensive'), ('bajo', 'short')), mezcla('くち', 'boca', 'mouth'), cambia('くち', 'くつ', ['つ', 'ち', 'き'])],
              construye=('あした', 'き')),
            L('u03l03', 'な に ぬ ね の', 'な に ぬ ね の', 'なにぬねの',
              [W('ねこ', 'gato', 'cat', '1f431'), W('いぬ', 'perro', 'dog', '1f436'), W('さかな', 'pescado', 'fish', '1f41f')],
              ('な に ぬ ね の', 'La fila な es n + vocal: な na, に ni, ぬ nu, ね ne, の no. Es la «n» de «nada», con la punta de la lengua en los dientes de arriba. ぬ se dice con los labios relajados.',
               'The な row is n + vowel: な na, に ni, ぬ nu, ね ne, の no. The tip of your tongue touches your upper teeth. ぬ is said with relaxed lips.'),
              foco='n', par=('ねこ', 'かお'), o=('ねこ', 'たこ'),
              extras=[letra('ぬ', ['ぬ', 'ね', 'の']), cambia('たこ', 'ねこ', ['ね', 'た', 'か']), sig('いぬ', ('perro', 'dog'), ('gato', 'cat'))],
              construye=('いぬ', 'な')),
            L('u03l04', 'Palabras con t y n', 'Words with t and n', '',
              [W('なつ', 'verano', 'summer'), W('おとこ', 'hombre', 'man'), W('ことし', 'este año', 'this year')],
              ('なつ なに おとこ いなか', 'Ya lees tres filas de consonantes. なに es «qué» e いなか es «campo». Recuerda: つ es «tsu» y ち es «chi».',
               'You now read three consonant rows. なに is “what” and いなか is “countryside.” Remember: つ is “tsu” and ち is “chi.”'),
              foco='n', par=('なつ', 'くつ'), o=('なつ', 'たつ'),
              extras=[sig('おとこ', ('hombre', 'man'), ('mujer', 'woman')),
                      lee('ことし', 'este año', 'this year', '¿Cuál palabra significa «qué»?', 'Which word means “what”?', ['なに', 'ことし']),
                      mezcla('いなか', 'campo', 'countryside')],
              construye=('ことし', 'な')),
        ],
    },
    {
        'id': 'u04', 'titulo': b('J4 · Las filas は, ま y や', 'J4 · The は, ま and や rows'),
        'objetivo': b('Leer las filas は (h), ま (m) y や (y), con ふ soplado entre los labios, y despedirte con おやすみなさい.',
                      'Read the は (h), ま (m) and や (y) rows, with ふ blown between the lips, and say goodnight with おやすみなさい.'),
        'lecciones': [
            L('u04l01', 'は ひ ふ へ ほ', 'は ひ ふ へ ほ', 'はひふへほ',
              [W('ひと', 'persona', 'person'), W('ふね', 'barco', 'ship', '1f6a2'), W('ほし', 'estrella', 'star', '2b50')],
              ('は ひ ふ へ ほ', 'La fila は es h + vocal: は ha, ひ hi, ふ fu, へ he, ほ ho. Cuidado con ふ: no es «fu» con los dientes sobre el labio; sopla el aire entre los dos labios, como al apagar una vela.',
               'The は row is h + vowel: は ha, ひ hi, ふ fu, へ he, ほ ho. Careful with ふ: it is not “foo” with teeth on the lip; blow air between both lips, as if blowing out a candle.',
               ('は se lee «ha» aquí; como partícula se lee «wa» (lo verás pronto).', 'は is read “ha” here; as a particle it is read “wa” (you will see it soon).')),
              foco='h', par=('ひと', 'いす'), o=('ひと', 'いと'),
              extras=[letra('ふ', ['ふ', 'ひ', 'ほ']), sig('ほし', ('estrella', 'star'), ('luna', 'moon')), cambia('ふね', 'ふく', ['く', 'ね', 'し'])],
              construye=('ふね', 'ひ')),
            L('u04l02', 'ま み む め も', 'ま み む め も', 'まみむめも',
              [W('みみ', 'oreja', 'ear', '1f442'), W('め', 'ojo', 'eye', '1f441'), W('うま', 'caballo', 'horse', '1f434')],
              ('ま み む め も', 'La fila ま es m + vocal: ま ma, み mi, む mu, め me, も mo. Es la «m» de «mamá». む, como う y す, se dice con los labios relajados.',
               'The ま row is m + vowel: ま ma, み mi, む mu, め me, も mo. It is the m of “mama.” む, like う and す, is said with relaxed lips.'),
              foco='m', par=('みみ', 'ひと'), o=('うま', 'うた'),
              extras=[letra('む', ['む', 'ぬ', 'ふ']), sig('め', ('ojo', 'eye'), ('mano', 'hand')), cambia('うま', 'うみ', ['み', 'ま', 'め'])],
              construye=('うま', 'め')),
            L('u04l03', 'や ゆ よ', 'や ゆ よ', 'やゆよ',
              [W('やま', 'montaña', 'mountain', '26f0'), W('ゆき', 'nieve', 'snow', '2744'), W('やさい', 'verduras', 'vegetables', '1f96c')],
              ('や ゆ よ', 'La fila や solo tiene tres kana: や ya, ゆ yu, よ yo. La y es la de «yo». No existen «yi» ni «ye» en esta fila. ゆ se dice con los labios relajados.',
               'The や row has only three kana: や ya, ゆ yu, よ yo. There is no “yi” or “ye” in this row. ゆ is said with relaxed lips.'),
              foco='y', par=('やま', 'うま'), o=('やま', 'うま'),
              extras=[letra('ゆ', ['ゆ', 'よ', 'や']), sig('ゆき', ('nieve', 'snow'), ('lluvia', 'rain')), cambia('やま', 'うま', ['う', 'や', 'ゆ'])],
              construye=('やま', 'ゆ')),
            L('u04l04', 'Palabras y buenas noches', 'Words and goodnight', '',
              [W('なまえ', 'nombre', 'name'), W('やすい', 'barato', 'cheap'), W('おやすみなさい', 'buenas noches (al irse a dormir)', 'good night (before bed)')],
              ('なまえ やすい よこ ゆめ', 'Con ocho filas ya lees muchas palabras: なまえ «nombre», やすい «barato», よこ «lado» y ゆめ «sueño». おやすみなさい se dice al despedirse de noche: «que descanses».',
               'With eight rows you can read many words: なまえ “name,” やすい “cheap,” よこ “side” and ゆめ “dream.” おやすみなさい is said at night when you say goodbye: “rest well.”'),
              foco='m', par=('なまえ', 'やすい'), o=('やすい', 'やさい'),
              extras=[sig('やすい', ('barato', 'cheap'), ('caro', 'expensive')),
                      lee('ゆめ', 'sueño', 'dream', '¿Cuál palabra significa «nombre»?', 'Which word means “name”?', ['なまえ', 'ゆめ']),
                      mezcla('よこ', 'lado', 'side')],
              construye=('ゆめ', 'み')),
        ],
    },
    {
        'id': 'u05', 'titulo': b('J5 · ら, わ, ん y las partículas', 'J5 · ら, わ, ん and the particles'),
        'objetivo': b('Leer la fila ら con una r simple, わ, を y ん, y saber que は, へ y を se leen «wa», «e» y «o» como partículas.',
                      'Read the ら row with a single tap r, わ, を and ん, and know that は, へ and を are read “wa,” “e” and “o” as particles.'),
        'lecciones': [
            L('u05l01', 'ら り る れ ろ', 'ら り る れ ろ', 'らりるれろ',
              [W('そら', 'cielo', 'sky', '2601'), W('とり', 'pájaro', 'bird', '1f426'), W('くるま', 'carro', 'car', '1f697')],
              ('ら り る れ ろ', 'La fila ら es una «r» simple y rápida: la de «pero» o «aro». Nunca la «rr» vibrante de «perro», ni una «l». ら ra, り ri, る ru, れ re, ろ ro.',
               'The ら row is one quick tap of the tongue, like the tt in American “butter” or “ladder.” Not an English r, not a trilled rr, not an l. ら ra, り ri, る ru, れ re, ろ ro.',
               ('Un solo golpe de lengua, sin vibrar.', 'One single tap of the tongue, no rolling.')),
              foco='r', par=('とり', 'たこ'), o=('そら', 'そこ'),
              extras=[letra('る', ['る', 'ろ', 'れ']), sig('くるま', ('carro', 'car'), ('barco', 'ship')), cambia('そら', 'そこ', ['こ', 'ら', 'り'])],
              construye=('とり', 'る')),
            L('u05l02', 'わ を ん', 'わ を ん', 'わをん',
              [W('わたし', 'yo', 'I'), W('わに', 'cocodrilo', 'crocodile', '1f40a'), W('ほん', 'libro', 'book', '1f4d6')],
              ('わ を ん', 'わ es «wa». を se pronuncia «o» y casi solo se usa como partícula. ん es un golpe propio y nasal: ほん termina con un golpe nasal, no con «ne» ni «no».',
               'わ is “wa.” を is pronounced “o” and is used almost only as a particle. ん is a beat of its own, nasal: ほん ends in a nasal beat, not “nuh.”',
               ('ん cuenta como un golpe.', 'ん counts as one beat.')),
              foco='nn', par=('ほん', 'ほし'), o=('ほん', 'ほし'),
              extras=[letra('ん', ['ん', 'の', 'ぬ']), sig('わたし', ('yo', 'I'), ('tú', 'you')), cambia('わに', 'かに', ['か', 'わ', 'た'])],
              construye=('ほん', 'わ')),
            L('u05l03', 'ん en las palabras', 'ん in words', '',
              [W('にほん', 'Japón', 'Japan', nombre=True), W('みかん', 'mandarina', 'mandarin orange', '1f34a'), W('ほんや', 'librería', 'bookstore')],
              ('にほん みかん ほんや てんき', 'ん suena distinto según lo que sigue: antes de p, b y m suena «m»; antes de k y g suena «ng» de «banco»; en los demás casos suena «n». Lo importante es que dura un golpe. En ほんや el rōmaji pone un apóstrofo: hon\'ya.',
               'ん sounds different depending on what follows: before p, b and m it sounds like “m”; before k and g like the “ng” of “sing”; elsewhere like “n.” What matters is that it lasts one beat. In ほんや the rōmaji adds an apostrophe: hon\'ya.'),
              foco='nn', par=('にほん', 'にし'), o=('てんき', 'てき'),
              extras=[sig('にほん', ('Japón', 'Japan'), ('México', 'Mexico')), mezcla('ほんや', 'librería', 'bookstore'), sig('てんき', ('tiempo; clima', 'weather'), ('ciudad', 'city'))],
              construye=('にほん', 'み')),
            L('u05l04', 'は, へ y を como partículas', 'は, へ and を as particles', '',
              [W('こんにちは', 'hola; buenas tardes', 'hello; good afternoon', '1f44b'),
               W('わたし は ほん を よみます。', 'Leo un libro.', 'I read a book.'),
               W('にほん へ いきます。', 'Voy a Japón.', 'I go to Japan.')],
              ('は へ を', 'Tres kana cambian de sonido cuando son partículas, es decir, palabras cortas que unen la frase: は se lee «wa», へ se lee «e» y を se lee «o». Se escriben igual, pero se leen así. Por eso こんにちは suena «konnichiwa».',
               'Three kana change sound when they are particles, short words that link the sentence: は is read “wa,” へ is read “e” and を is read “o.” They are written as usual but read this way. That is why こんにちは sounds like “konnichiwa.”',
               ('En este curso el japonés se escribe con un espacio entre palabras y las partículas van aparte.', 'In this course Japanese is written with a space between words, and particles stand alone.')),
              foco='part', par=('ほん を よみます。', 'ほんや'), o=('ほん を よみます。', 'ほん を みます。'),
              extras=[sig('にほん へ いきます。', ('Voy a Japón.', 'I go to Japan.'), ('Vengo de Japón.', 'I come from Japan.')),
                      sig('わたし は ほん を よみます。', ('Leo un libro.', 'I read a book.'), ('Compro un libro.', 'I buy a book.'))],
              construye=('こんにちは', 'ほ')),
        ],
    },
]
UNIDADES += [
    {
        'id': 'u06', 'titulo': b('J6 · Dakuten y handakuten', 'J6 · Dakuten and handakuten'),
        'objetivo': b('Leer los kana con dos rayitas ゛ (g, z, d, b) y con un circulito ゜ (p), y la ん ante p, b y m.',
                      'Read kana with two small strokes ゛ (g, z, d, b) and with a small circle ゜ (p), and ん before p, b and m.'),
        'lecciones': [
            L('u06l01', 'が行 y ざ行', 'The が and ざ rows', 'がぎぐげござじずぜぞ',
              [W('かぎ', 'llave', 'key', '1f511'), W('ごはん', 'arroz; comida', 'cooked rice; meal', '1f35a'), W('かぜ', 'viento; resfriado', 'wind; a cold', '1f32c')],
              ('が ぎ ぐ げ ご', 'Dakuten: dos rayitas ゛ sobre un kana vuelven sonoro su sonido: か ka → が ga, き ki → ぎ gi. La g es siempre dura, como en «gato». Pon la mano en la garganta: con g vibra; con k no.',
               'Dakuten: two small strokes ゛ on a kana make its sound voiced: か ka → が ga, き ki → ぎ gi. The g is always hard, as in “go.” Touch your throat: it buzzes with g, not with k.'),
              foco='g', par=('かぎ', 'かき'), o=('かぎ', 'かき'),
              extras=[mira('ざ じ ず ぜ ぞ', 'La fila ざ es さ con dakuten: ざ za, じ ji, ず zu, ぜ ze, ぞ zo. Cuidado: じ suena como una «yi» fuerte (como la «y» de «yeso», muy tensa) y ず suena «dsu».',
                           'The ざ row is さ with dakuten: ざ za, じ ji, ず zu, ぜ ze, ぞ zo. Careful: じ is “jee” and ず is “dzu.”', 'z'),
                      letra('が', ['が', 'か', 'ぎ']), toca('z', 'かぜ', 'かき'), cambia('かき', 'かぎ', ['ぎ', 'き', 'ぐ']),
                      sig('かぜ', ('viento; resfriado', 'wind; a cold'), ('lluvia', 'rain'))],
              construye=('かぎ', 'が')),
            L('u06l02', 'だ行 y ば行', 'The だ and ば rows', 'だぢづでどばびぶべぼ',
              [W('ともだち', 'amigo', 'friend'), W('でんわ', 'teléfono', 'telephone', '260e'), W('ばら', 'rosa', 'rose', '1f339')],
              ('だ ぢ づ で ど', 'La fila だ es た con dakuten: だ da, で de, ど do. ぢ y づ suenan igual que じ y ず y casi no se usan: solo los verás en pocas palabras, como はなぢ y つづく.',
               'The だ row is た with dakuten: だ da, で de, ど do. ぢ and づ sound the same as じ and ず and are almost never used: you will only see them in a few words, like はなぢ and つづく.'),
              foco='b', par=('ばら', 'はら'), o=('ばら', 'はら'),
              extras=[mira('ば び ぶ べ ぼ', 'La fila ば es は con dakuten: ば ba, び bi, ぶ bu, べ be, ぼ bo. La b es la de «boca».',
                           'The ば row is は with dakuten: ば ba, び bi, ぶ bu, べ be, ぼ bo. The b is the b of “boat.”', 'b'),
                      toca('d', 'ともだち', 'かばん'), cambia('はら', 'ばら', ['ば', 'か', 'ま']), letra('で', ['で', 'て', 'べ']),
                      sig('でんわ', ('teléfono', 'telephone'), ('televisión', 'television'))],
              construye=('ばら', 'は')),
            L('u06l03', 'ぱ行 y la ん', 'The ぱ row and ん', 'ぱぴぷぺぽ',
              [W('さんぽ', 'paseo', 'walk'), W('てんぷら', 'tempura', 'tempura'), W('えんぴつ', 'lápiz', 'pencil', '270f')],
              ('ぱ ぴ ぷ ぺ ぽ', 'Handakuten: un circulito ゜ sobre は ひ ふ へ ほ los vuelve pa, pi, pu, pe, po. La p es la de «papá». Ojo con ん: antes de p, b y m suena «m», así que さんぽ suena «sampo». En el rōmaji se escribe siempre n: sanpo.',
               'Handakuten: a small circle ゜ on は ひ ふ へ ほ turns them into pa, pi, pu, pe, po. The p is the p of “spot.” Careful with ん: before p, b and m it sounds like “m,” so さんぽ sounds like “sampo.” In rōmaji it is always written n: sanpo.'),
              foco='p', par=('えんぴつ', 'かばん'), o=('さんぽ', 'さんご'),
              extras=[letra('ぷ', ['ぷ', 'ぶ', 'ふ']), toca('b', 'かばん', 'さんぽ'), sig('えんぴつ', ('lápiz', 'pencil'), ('cuaderno', 'notebook')),
                      mezcla('しんぶん', 'periódico', 'newspaper')],
              construye=('さんぽ', 'ぼ')),
            L('u06l04', 'Palabras con dakuten', 'Words with dakuten', '',
              [W('ただいま', 'ya llegué', 'I am home'), W('げんき', 'bien; con energía', 'well; energetic'), W('どこ', 'dónde', 'where')],
              ('ただいま げんき こんばんは しんぶん', 'Lee con las marcas: ただいま «ya llegué» (al entrar a casa), げんき «con energía», しんぶん «periódico» y こんばんは «buenas noches» como saludo (aquí は se lee «wa»).',
               'Read with the marks: ただいま “I am home” (said when you come in), げんき “energetic,” しんぶん “newspaper” and こんばんは “good evening” (here は is read “wa”).'),
              foco='d', par=('どこ', 'ここ'), o=('どこ', 'ここ'),
              extras=[sig('げんき', ('bien; con energía', 'well; energetic'), ('cansado', 'tired')), mezcla('ただいま', 'ya llegué', 'I am home'),
                      sig('ごはん を たべます。', ('Como arroz.', 'I eat rice.'), ('Compro arroz.', 'I buy rice.'))],
              construye=('どこ', 'ご')),
        ],
    },
    {
        'id': 'u07', 'titulo': b('J7 · Combinaciones y っ', 'J7 · Combinations and っ'),
        'objetivo': b('Leer los kana con ゃ ゅ ょ pequeñas como un solo golpe y la っ pequeña como una pausa que alarga la consonante.',
                      'Read kana with small ゃ ゅ ょ as one single beat and the small っ as a pause that lengthens the consonant.'),
        'lecciones': [
            L('u07l01', 'きゃ しゅ ちょ', 'きゃ しゅ ちょ', 'ゃゅょ',
              [W('おちゃ', 'té', 'tea', '1f375'), W('しゃしん', 'foto', 'photo', '1f4f7'), W('かいしゃ', 'empresa', 'company')],
              ('きゃ きゅ きょ しゃ しゅ しょ ちゃ ちゅ ちょ', 'Un kana de la columna い (き し ち に ひ み り) con ゃ ゅ ょ pequeñas se lee como un solo golpe: きゃ kya, きゅ kyu, きょ kyo. きゃ es un golpe; き-や serían dos. Con し, ち y じ: しゃ sha, ちゃ cha, じゃ ja.',
               'An い-column kana (き し ち に ひ み り) with a small ゃ ゅ ょ is read as one single beat: きゃ kya, きゅ kyu, きょ kyo. きゃ is one beat; き-や would be two. With し, ち and じ: しゃ sha, ちゃ cha, じゃ ja.',
               ('Las ゃ ゅ ょ pequeñas siempre se escriben pequeñas.', 'The small ゃ ゅ ょ are always written small.')),
              foco='yoon', par=('おちゃ', 'おかし'), o=('しゅみ', 'しみ'),
              extras=[sig('しゃしん', ('foto', 'photo'), ('película', 'film')), mezcla('かいしゃ', 'empresa', 'company'), oye('いしゃ', 'いしや', True)],
              construye=('おちゃ', 'ゅ')),
            L('u07l02', 'Más combinaciones', 'More combinations', '',
              [W('ひゃく', 'cien', 'one hundred'), W('りょかん', 'posada japonesa', 'Japanese inn'), W('しょくじ', 'comida', 'meal')],
              ('にゃ ひゃ みゃ りゃ ぎゃ じゃ びゃ ぴゃ', 'Todas las filas con i hacen lo mismo: にゃ nya, ひゃ hya, みゃ mya, りゃ rya, ぎゃ gya, じゃ ja, びゃ bya, ぴゃ pya, y lo mismo con ゅ y ょ. Cuenta los golpes: りょかん son tres (りょ-か-ん), しょくじ son tres (しょ-く-じ).',
               'All the rows with i do the same: にゃ nya, ひゃ hya, みゃ mya, りゃ rya, ぎゃ gya, じゃ ja, びゃ bya, ぴゃ pya, and the same with ゅ and ょ. Count the beats: りょかん is three (りょ-か-ん), しょくじ is three (しょ-く-じ).'),
              foco='yoon', par=('じしょ', 'じしん'), o=('じしょ', 'じしん'),
              extras=[sig('じしょ', ('diccionario', 'dictionary'), ('terremoto', 'earthquake')), sig('ひゃく', ('cien', 'one hundred'), ('mil', 'one thousand')),
                      mezcla('しょくじ', 'comida', 'meal')],
              construye=('じしょ', 'ゃ')),
            L('u07l03', 'La っ pequeña', 'The small っ', 'っ',
              [W('きっぷ', 'boleto', 'ticket'), W('ざっし', 'revista', 'magazine'), W('きって', 'sello postal', 'postage stamp')],
              ('きっぷ ざっし きって さっか', 'La っ pequeña no tiene sonido propio: es una pausa de un golpe, con la boca cerrada, antes de k, s, t o p. Compara: きて «ven» y きって «sello»; さか «cuesta» y さっか «escritor». El español no tiene este sonido: la duración lo cambia todo. En rōmaji se duplica la consonante: kitte, zasshi.',
               'The small っ has no sound of its own: it is a one-beat pause, mouth closed, before k, s, t or p. Compare: きて “come” and きって “stamp”; さか “slope” and さっか “writer.” English has a similar hold in “hot-tub,” but here it lasts longer. In rōmaji the consonant is doubled: kitte, zasshi.',
               ('っ dura un golpe completo.', 'っ lasts one full beat.')),
              foco='sokuon', par=('きって', 'きて'), o=('さっか', 'さか'),
              extras=[oye('きって', 'きて', True), sig('さっか', ('escritor', 'writer'), ('cuesta', 'slope')), sig('きって', ('sello postal', 'postage stamp'), ('ven', 'come'))],
              construye=('ざっし', 'き')),
            L('u07l04', 'Palabras con っ', 'Words with っ', '',
              [W('ちょっと', 'un poco', 'a bit'), W('いっぱい', 'lleno; mucho', 'full; a lot'), W('まっちゃ', 'matcha', 'matcha', '1f375')],
              ('いっしょ みっつ にっき ずっと', 'Más palabras con っ: いっしょ «juntos», みっつ «tres cosas», にっき «diario» y ずっと «siempre». En rōmaji, っ duplica la consonante: issho, mittsu, nikki, zutto; ante ch se escribe tch: matcha.',
               'More words with っ: いっしょ “together,” みっつ “three things,” にっき “diary” and ずっと “always.” In rōmaji, っ doubles the consonant: issho, mittsu, nikki, zutto; before ch it becomes tch: matcha.'),
              foco='sokuon', par=('いっしょ', 'いしゃ'), o=('おっと', 'おと'),
              extras=[sig('みっつ', ('tres cosas', 'three things'), ('dos cosas', 'two things')),
                      sig('ずっと', ('siempre; todo el tiempo', 'always; all along'), ('nunca', 'never')), mezcla('にっき', 'diario', 'diary')],
              construye=('みっつ', 'ち')),
        ],
    },
    {
        'id': 'u08', 'titulo': b('J8 · Vocales largas, vocales mudas y tono', 'J8 · Long vowels, silent vowels and pitch'),
        'objetivo': b('Alargar las vocales dos golpes, oír las vocales que casi no suenan (です, ます) y saber que el japonés usa tono alto y bajo.',
                      'Hold long vowels for two beats, hear the vowels that almost disappear (です, ます) and know that Japanese uses high and low pitch.'),
        'lecciones': [
            L('u08l01', 'Vocales largas: ああ いい うう ええ', 'Long vowels: ああ いい うう ええ', '',
              [W('おかあさん', 'madre', 'mother', '1f469'), W('おにいさん', 'hermano mayor', 'older brother'), W('おじいさん', 'abuelo', 'grandfather', '1f474')],
              ('おかあさん おにいさん おじいさん おねえさん', 'Una vocal larga dura dos golpes y cambia la palabra. En hiragana se escribe repitiendo la vocal: ああ, いい, うう, ええ. Compara: おばさん «tía» y おばあさん «abuela»; おじさん «tío» y おじいさん «abuelo». En rōmaji lleva macrón: ā, ū, ē, ō; いい se escribe ii.',
               'A long vowel lasts two beats and changes the word. In hiragana it is written by repeating the vowel: ああ, いい, うう, ええ. Compare: おばさん “aunt” and おばあさん “grandmother”; おじさん “uncle” and おじいさん “grandfather.” In rōmaji it takes a macron: ā, ū, ē, ō; いい is written ii.',
               ('Mantén la vocal el doble de tiempo.', 'Hold the vowel twice as long.')),
              foco='largo', par=('おじいさん', 'おじさん'), o=('おばあさん', 'おばさん'),
              extras=[oye('おじいさん', 'おじさん'), oye('ゆうき', 'ゆき', True), sig('おばあさん', ('abuela', 'grandmother'), ('tía', 'aunt')),
                      sig('おばさん', ('tía', 'aunt'), ('abuela', 'grandmother'))],
              construye=('おかあさん', 'お')),
            L('u08l02', 'Vocales largas: おう, おお y えい', 'Long vowels: おう, おお and えい', '',
              [W('ありがとう', 'gracias', 'thank you'), W('おはよう', 'buenos días', 'good morning'), W('せんせい', 'profesor; maestro', 'teacher')],
              ('おう おお えい', 'La o larga se escribe casi siempre おう (ありがとう, おはよう) y a veces おお (おおさか). La e larga se escribe ええ o, muy a menudo, えい: せんせい suena con la e larga. En rōmaji: おう y おお → ō; えい → ei (sensei).',
               'The long o is almost always written おう (ありがとう, おはよう) and sometimes おお (おおさか). The long e is written ええ or, very often, えい: せんせい is said with a long e. In rōmaji: おう and おお → ō; えい → ei (sensei).'),
              foco='largo', par=('ありがとう', 'あかい'), o=('ゆうき', 'ゆき'),
              extras=[sig('せんせい', ('profesor; maestro', 'teacher'), ('estudiante', 'student')), mezcla('おはよう', 'buenos días', 'good morning'),
                      oye('こうこう', 'ここ', True), sig('ありがとう', ('gracias', 'thank you'), ('perdón', 'sorry'))],
              construye=('ありがとう', 'こ')),
            L('u08l03', 'Ciudades y lugares', 'Cities and places', '',
              [W('とうきょう', 'Tokio', 'Tokyo', nombre=True), W('おおさか', 'Osaka', 'Osaka', nombre=True), W('きょうと', 'Kioto', 'Kyoto', nombre=True)],
              ('とうきょう おおさか きょうと', 'Los nombres de las ciudades japonesas están llenos de vocales largas: とうきょう es «Tōkyō», おおさか es «Ōsaka» y きょうと es «Kyōto». Cuenta: と-う-きょ-う son cuatro golpes.',
               'Japanese city names are full of long vowels: とうきょう is “Tōkyō,” おおさか is “Ōsaka” and きょうと is “Kyōto.” Count: と-う-きょ-う is four beats.'),
              foco='largo', par=('とうきょう', 'ひと'), o=('こうこう', 'ここ'),
              extras=[sig('がっこう', ('escuela', 'school'), ('hospital', 'hospital')), sig('びょういん', ('hospital', 'hospital'), ('escuela', 'school')),
                      mezcla('ゆうびんきょく', 'correos', 'post office')],
              construye=('きょうと', 'お')),
            L('u08l04', 'Vocales que casi no suenan', 'Vowels that almost disappear', '',
              [W('です', 'es', 'is; am; are'), W('すき', 'me gusta', 'I like'), W('ひとつ', 'una cosa', 'one thing')],
              ('です ます すき ひとつ', 'A veces la i y la u casi no suenan: entre dos consonantes sordas, o al final después de una consonante sorda. です suena «des», ます suena «mas», すき suena «ski» y ひとつ suena «htotsu». No cambia lo que escribes, solo lo que oyes. Por ahora solo escúchalo: no se evalúa.',
               'The i and the u sometimes almost disappear: between two voiceless consonants, or at the end after a voiceless consonant. です sounds like “des,” ます like “mas,” すき like “ski” and ひとつ like “htotsu.” It does not change what you write, only what you hear. For now just listen: it is not tested.'),
              extras=[sig('すき', ('me gusta', 'I like'), ('no me gusta', 'I do not like')), mezcla('ひとつ', 'una cosa', 'one thing')],
              construye=('です', 'す')),
            L('u08l05', 'El tono: alto y bajo', 'Pitch: high and low', '',
              [W('はし', 'palillos', 'chopsticks'), W('はし', 'puente', 'bridge', '1f309'), W('あめ', 'lluvia', 'rain', '1f327'), W('あめ', 'caramelo', 'candy', '1f36c')],
              ('はし あめ', 'El japonés no tiene una sílaba fuerte como el español: usa tonos altos y bajos. はし dicho alto-bajo es «palillos»; dicho bajo-alto es «puente». あめ puede ser «lluvia» o «caramelo». Por ahora solo escucha: el tono no se marca al escribir ni se evalúa.',
               'Japanese has no heavy stressed syllable: it uses high and low pitch. はし said high-low is “chopsticks”; said low-high it is “bridge.” あめ can be “rain” or “candy.” For now just listen: the pitch is not written and it is not tested.'),
              extras=[mezcla('あめ', 'lluvia; caramelo', 'rain; candy')],
              construye=('はし', 'あ')),
        ],
    },
    {
        'id': 'u09', 'titulo': b('J9 · Katakana y préstamos', 'J9 · Katakana and loanwords'),
        'objetivo': b('Leer el katakana básico, la raya ー y las palabras de otros idiomas, con carteles y países.',
                      'Read basic katakana, the ー stroke and words from other languages, with signs and countries.'),
        'lecciones': [
            L('u09l01', 'ア行, カ行 y サ行', 'The ア, カ and サ rows', 'アイウエオカキクケコサシスセソ',
              [W('アイス', 'helado', 'ice cream', '1f366'), W('スイカ', 'sandía', 'watermelon'), W('ココア', 'cacao; chocolate caliente', 'cocoa')],
              ('ア イ ウ エ オ', 'El katakana suena igual que el hiragana, pero se escribe con trazos rectos y angulosos. Se usa para palabras de otros idiomas, nombres y países extranjeros, y algunos animales y plantas. ア a, イ i, ウ u, エ e, オ o.',
               'Katakana sounds the same as hiragana but is written with straight, angular strokes. It is used for words from other languages, foreign names and countries, and some animals and plants. ア a, イ i, ウ u, エ e, オ o.'),
              foco='k', par=('スイカ', 'アイス'), o=('アイス', 'スイス'),
              extras=[mira('カ キ ク ケ コ', 'カ ka, キ ki, ク ku, ケ ke, コ ko: la misma fila か, con otra forma.', 'カ ka, キ ki, ク ku, ケ ke, コ ko: the same か row, in a different shape.', 'k'),
                      mira('サ シ ス セ ソ', 'サ sa, シ shi, ス su, セ se, ソ so. Fíjate en la dirección de los trazos de シ y ソ.', 'サ sa, シ shi, ス su, セ se, ソ so. Look at the direction of the strokes in シ and ソ.', 's'),
                      letra('ク', ['ク', 'ケ', 'コ']), letra('シ', ['シ', 'ス', 'セ']), sig('アイス', ('helado', 'ice cream'), ('hielo', 'ice'))],
              construye=('アイス', 'ク')),
            L('u09l02', 'タ行, ナ行 y ハ行', 'The タ, ナ and ハ rows', 'タチツテトナニヌネノハヒフヘホ',
              [W('テスト', 'examen', 'test'), W('ネクタイ', 'corbata', 'necktie'), W('ツナ', 'atún', 'tuna')],
              ('タ チ ツ テ ト', 'タ ta, チ chi, ツ tsu, テ te, ト to: igual que た ち つ て と, así que ツ es «tsu» y チ es «chi».',
               'タ ta, チ chi, ツ tsu, テ te, ト to: the same as た ち つ て と, so ツ is “tsu” and チ is “chi.”'),
              foco='t', par=('テスト', 'アイス'),
              extras=[mira('ナ ニ ヌ ネ ノ', 'ナ na, ニ ni, ヌ nu, ネ ne, ノ no.', 'ナ na, ニ ni, ヌ nu, ネ ne, ノ no.', 'n'),
                      mira('ハ ヒ フ ヘ ホ', 'ハ ha, ヒ hi, フ fu, ヘ he, ホ ho. フ se sopla entre los labios, como ふ.', 'ハ ha, ヒ hi, フ fu, ヘ he, ホ ho. フ is blown between the lips, like ふ.', 'h'),
                      letra('チ', ['チ', 'テ', 'ツ']), letra('ヌ', ['ヌ', 'ネ', 'ノ']), sig('ネクタイ', ('corbata', 'necktie'), ('camisa', 'shirt')),
                      sig('ツナ', ('atún', 'tuna'), ('pulpo', 'octopus'))],
              construye=('ツナ', 'ネ')),
            L('u09l03', 'マ行, ヤ行 y ラ行', 'The マ, ヤ and ラ rows', 'マミムメモヤユヨラリルレロ',
              [W('ホテル', 'hotel', 'hotel', '1f3e8'), W('カメラ', 'cámara', 'camera', '1f4f7'), W('トマト', 'tomate', 'tomato', '1f345')],
              ('マ ミ ム メ モ', 'マ ma, ミ mi, ム mu, メ me, モ mo.', 'マ ma, ミ mi, ム mu, メ me, モ mo.'),
              foco='r', par=('カメラ', 'テスト'),
              extras=[mira('ヤ ユ ヨ ラ リ ル レ ロ', 'ヤ ya, ユ yu, ヨ yo; ラ ra, リ ri, ル ru, レ re, ロ ro. La ラ行 sigue siendo una r simple y rápida.',
                           'ヤ ya, ユ yu, ヨ yo; ラ ra, リ ri, ル ru, レ re, ロ ro. The ラ row is still one quick tap r.', 'r'),
                      letra('ミ', ['ミ', 'メ', 'ム']), letra('リ', ['リ', 'ル', 'レ']), sig('ホテル', ('hotel', 'hotel'), ('hospital', 'hospital')),
                      mezcla('ミルク', 'leche', 'milk')],
              construye=('カメラ', 'ル')),
            L('u09l04', 'ワ, ヲ, ン y la raya ー', 'ワ, ヲ, ン and the ー stroke', 'ワヲンー',
              [W('ワイン', 'vino', 'wine', '1f377'), W('コーヒー', 'café', 'coffee', '2615'), W('ケーキ', 'pastel', 'cake', '1f370')],
              ('ワ ヲ ン', 'ワ wa, ヲ o y ン n, igual que わ, を y ん. ヲ casi no se usa.', 'ワ wa, ヲ o and ン n, like わ, を and ん. ヲ is almost never used.'),
              foco='nn', par=('レモン', 'テスト'),
              extras=[mira('コーヒー ケーキ', 'En katakana la vocal larga se escribe con una raya ー, nunca repitiendo la vocal. La raya alarga un golpe más la vocal anterior: コーヒー es «kōhī» y ケーキ es «kēki».',
                           'In katakana a long vowel is written with a stroke ー, never by repeating the vowel. The stroke holds the previous vowel one more beat: コーヒー is “kōhī” and ケーキ is “kēki.”', 'largo'),
                      mira('シ ツ ソ ン', 'Cuidado con los parecidos: シ y ツ (shi y tsu) y ソ y ン (so y n) se distinguen por la dirección de los trazos. Léelos despacio.',
                           'Careful with look-alikes: シ and ツ (shi and tsu), and ソ and ン (so and n), differ in the direction of their strokes. Read them slowly.'),
                      mira('ノート', 'ノート se lee «nōto» y viene del inglés «note», pero significa «cuaderno», no «nota». ⚠ Falso amigo.',
                           'ノート is read “nōto” and comes from “note,” but it means “notebook,” not “note.” ⚠ False friend.', None,
                           ('⚠ ノート = cuaderno, no «nota».', '⚠ ノート = notebook, not “note.”')),
                      letra('ン', ['ン', 'ソ', 'シ']), letra('ソ', ['ソ', 'ン', 'ツ']), sig('ノート', ('cuaderno', 'notebook'), ('nota', 'note')),
                      sig('レモン', ('limón', 'lemon'), ('melón', 'melon')), sig('メロン', ('melón', 'melon'), ('limón', 'lemon'))],
              construye=('ワイン', 'ン')),
            L('u09l05', 'Dakuten, handakuten, ッ y ャュョ', 'Dakuten, handakuten, ッ and ャュョ', 'ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポッャュョ',
              [W('バス', 'autobús', 'bus', '1f68c'), W('テレビ', 'televisión', 'TV', '1f4fa'), W('ピアノ', 'piano', 'piano', '1f3b9')],
              ('ガ ギ グ ゲ ゴ', 'El katakana usa las mismas marcas: ゛ y ゜. カ ka → ガ ga; ハ ha → バ ba → パ pa. Lo mismo pasa con ザ ダ y con ジ ズ. Los kana pequeños funcionan igual que en hiragana: ッ marca una pausa de un golpe y ャ ュ ョ forman un solo golpe con el kana anterior.',
               'Katakana uses the same marks: ゛ and ゜. カ ka → ガ ga; ハ ha → バ ba → パ pa. The same goes for ザ ダ and ジ ズ. The small kana work as in hiragana: ッ marks a one-beat pause and ャ ュ ョ form one single beat with the kana before them.'),
              foco='b', par=('バス', 'アイス'), o=('ビール', 'ビル'),
              extras=[mira('シャツ ジュース サッカー ベッド', 'Lee con ッ y ャュョ: シャツ «shatsu» (camisa), ジュース «jūsu» (jugo), サッカー «sakkā» (fútbol) y ベッド «beddo» (cama).',
                           'Read with ッ and ャュョ: シャツ “shatsu” (shirt), ジュース “jūsu” (juice), サッカー “sakkā” (soccer) and ベッド “beddo” (bed).', 'sokuon'),
                      sig('ビール', ('cerveza', 'beer'), ('edificio', 'building')), sig('ビル', ('edificio', 'building'), ('cerveza', 'beer')),
                      sig('サッカー', ('fútbol', 'soccer'), ('tenis', 'tennis')), sig('シャツ', ('camisa', 'shirt'), ('zapatos', 'shoes'))],
              construye=('バス', 'ビ')),
            L('u09l06', 'Carteles y países', 'Signs and countries', '',
              [W('コンビニ', 'tienda de conveniencia', 'convenience store', '1f3ea'), W('トイレ', 'baño', 'restroom'), W('メキシコ', 'México', 'Mexico', nombre=True)],
              ('コンビニ トイレ タクシー レストラン', 'Mira lo que ya sabes leer: コンビニ «tienda de conveniencia», トイレ «baño», タクシー «taxi» y レストラン «restaurante». Muchas palabras vienen del inglés, pero se pronuncian con los sonidos japoneses.',
               'Look what you can already read: コンビニ “convenience store,” トイレ “restroom,” タクシー “taxi” and レストラン “restaurant.” Many words come from English, but they are pronounced with Japanese sounds.'),
              foco='nn', par=('コンビニ', 'トイレ'), o=('スイス', 'アイス'),
              extras=[mira('メキシコ アメリカ スペイン イタリア', 'Los países también van en katakana: メキシコ «México», アメリカ «Estados Unidos», スペイン «España» e イタリア «Italia».',
                           'Countries are also written in katakana: メキシコ “Mexico,” アメリカ “the United States,” スペイン “Spain” and イタリア “Italy.”'),
                      mira('チリ ペルー コロンビア アルゼンチン スイス', 'Más países: チリ, ペルー, コロンビア, アルゼンチン y スイス. La ー alarga la vocal: ペルー es «perū».',
                           'More countries: チリ, ペルー, コロンビア, アルゼンチン and スイス. The ー holds the vowel: ペルー is “perū.”'),
                      mira('マンション', 'マンション se lee «manshon» y significa «departamento» en un edificio de concreto, no «mansión». ⚠ Falso amigo.',
                           'マンション is read “manshon” and means an apartment in a concrete building, not a “mansion.” ⚠ False friend.', None,
                           ('⚠ マンション = departamento, no «mansión».', '⚠ マンション = apartment, not “mansion.”')),
                      sig('マンション', ('departamento en un edificio', 'apartment in a building'), ('casa grande y lujosa', 'big luxury house')),
                      lee('コンビニ', 'tienda de conveniencia', 'convenience store', '¿Cuál palabra significa «baño»?', 'Which word means “restroom”?', ['トイレ', 'コンビニ']),
                      lee('アメリカ', 'Estados Unidos', 'the United States', '¿Cuál palabra es un país?', 'Which word is a country?', ['スペイン', 'タクシー'])],
              construye=('メキシコ', 'ン')),
        ],
    },
    {
        'id': 'u10', 'titulo': b('J10 · Ya puedes empezar', 'J10 · You can start now'),
        'objetivo': b('Comprobar que lees y oyes el japonés: carteles, contrastes, palabras nuevas y una primera presentación.',
                      'Check that you can read and hear Japanese: signs, contrasts, new words and a first introduction.'),
        'lecciones': [
            L('u10l01', 'Lee carteles', 'Read signs', '',
              [W('でぐち', 'salida', 'exit'), W('いりぐち', 'entrada', 'entrance'), W('えき', 'estación', 'station', '1f686'), W('トイレ', 'baño', 'restroom')],
              ('でぐち いりぐち', 'Los carteles suelen llevar solo la palabra clave. Lee primero la palabra y piensa en su significado.',
               'Signs usually carry only the key word. Read the word first and think about its meaning.'),
              o=('でぐち', 'いりぐち'),
              extras=[lee('でぐち いりぐち', 'salida entrada', 'exit entrance', '¿Qué palabra indica por dónde salir?', 'Which word tells you where to exit?', ['でぐち', 'いりぐち']),
                      sig('ぎんこう', ('banco', 'bank'), ('escuela', 'school')), sig('ゆうびんきょく', ('correos', 'post office'), ('hospital', 'hospital')),
                      sig('コンビニ', ('tienda de conveniencia', 'convenience store'), ('restaurante', 'restaurant')),
                      lee('ぬろせ', *PSEUDO, *CUAL_INVENTADA, ['やま', 'ぬろせ'], 1)],
              construye=('でぐち', 'い')),
            L('u10l02', 'Contrastes', 'Contrasts', '',
              [W('きって', 'sello postal', 'postage stamp'), W('おばあさん', 'abuela', 'grandmother'), W('ビール', 'cerveza', 'beer', '1f377')],
              ('きて きって', 'Repaso: っ y sin っ (きて, きって), vocal corta y larga (おばさん, おばあさん), con dakuten y sin él (かき, かぎ; はら, ばら) y con ー o sin ー (ビル, ビール).',
               'Review: with and without っ (きて, きって), short and long vowel (おばさん, おばあさん), with and without dakuten (かき, かぎ; はら, ばら) and with or without ー (ビル, ビール).'),
              foco='sokuon', par=('きって', 'きて'), o=('きって', 'きて'),
              extras=[oye('おばあさん', 'おばさん', True), oye('ゆうき', 'ゆき'), oye('かぎ', 'かき', True), oye('ばら', 'はら'), oye('ビール', 'ビル', True),
                      toca('yoon', 'しゃしん', 'かお'), toca('largo', 'おかあさん', 'かお', True)],
              construye=('きって', 'と')),
            L('u10l03', 'Palabras nuevas', 'New words', '',
              [W('ひこうき', 'avión', 'airplane', '2708'), W('ぎゅうにゅう', 'leche', 'milk', '1f95b'), W('ハンバーガー', 'hamburguesa', 'hamburger')],
              ('ひこうき ぎゅうにゅう ハンバーガー', 'Estas palabras son nuevas, pero ya conoces todas sus reglas: vocales largas, combinaciones, dakuten y la raya ー. Léelas sin ayuda y luego escúchalas.',
               'These words are new, but you know all their rules: long vowels, combinations, dakuten and the ー stroke. Read them without help, then listen.'),
              foco='yoon', par=('ぎゅうにゅう', 'ひこうき'), o=('ハンバーガー', 'ハンバーグ'),
              extras=[lee('ヘミヌ', *PSEUDO, *CUAL_INVENTADA, ['ヘミヌ', 'ハンバーガー']),
                      sig('ひこうき', ('avión', 'airplane'), ('barco', 'ship')), sig('ぎゅうにゅう', ('leche', 'milk'), ('jugo', 'juice'))],
              construye=('ひこうき', 'り')),
            L('u10l04', 'Tu primera presentación', 'Your first introduction', '',
              [W('こんにちは。', 'Hola; buenas tardes.', 'Hello; good afternoon.'), W('はじめまして。 さくら です。', 'Mucho gusto. Soy Sakura.', 'Nice to meet you. I am Sakura.'),
               W('ありがとう ございます。', 'Muchas gracias.', 'Thank you very much.')],
              ('はじめまして。 さくら です。', 'Junta todo: はじめまして se dice al conocer a alguien y さくら です quiere decir «soy Sakura». Al presentarte a ti mismo, tu nombre nunca lleva さん. ¡Ya puedes empezar Fundamentos!',
               'Put it all together: はじめまして is said when you meet someone and さくら です means “I am Sakura.” When you introduce yourself, your name never takes さん. You are ready for Foundations!'),
              o=('こんにちは。', 'こんばんは。'),
              extras=[lee('ありがとう ございます。', 'Muchas gracias.', 'Thank you very much.', '¿Es un saludo o una forma de dar las gracias?', 'Is it a greeting or a way to say thanks?',
                          ['ありがとう ございます。', 'こんにちは。']),
                      deletreo('さくら', 'Escucha y ordena los kana de «さくら».', 'Listen and put the kana of “さくら” in order.')],
              construye=('です', 'ま')),
        ],
    },
]


# ── Comprobaciones: solo kana y sonidos ya enseñados; sin cifras ────────────
KANA = re.compile('[ぁ-ゖァ-ヺー]')
CLAVES = {'m', 'de', 'a', 'audio', 'letra', 'fichas', 'opciones'}
TEXTO = {'m', 'rom', 'letraRom', 't', 'texto', 'pregunta', 'nota', 'titulo', 'objetivo', 'es', 'en', 'audio'}


def _cadenas(o, clave=None):
    if isinstance(o, str):
        if clave in CLAVES:
            yield o
    elif isinstance(o, list):
        for x in o:
            yield from _cadenas(x, clave)
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from _cadenas(v, k if isinstance(v, str) else clave if isinstance(v, list) else k)


def _todas(o, clave=None):
    if isinstance(o, str):
        if clave in TEXTO:
            yield o
    elif isinstance(o, list):
        for x in o:
            yield from _todas(x, clave)
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from _todas(v, k)


def comprobar():
    errores, vistos = [], set()
    for u in UNIDADES:
        n = int(u['id'][1:])
        for l in u['lecciones']:
            vistos |= set(LECCION_NUEVOS[l['id']])
            for s in _cadenas(l['pasos']):
                for c in set(KANA.findall(plano(s))) - vistos:
                    errores.append(f'{l["id"]}: kana no enseñado «{c}» en {plano(s)}')
                for sid in GRUPO.findall(s):
                    if UNIDAD_DE[sid[1]] > n:
                        errores.append(f'{l["id"]}: sonido «{sid[1]}» (unidad {UNIDAD_DE[sid[1]]}) aún no enseñado')
            for s in _todas(l['pasos']):
                if re.search(r'[0-9]', s):
                    errores.append(f'{l["id"]}: cifra en «{s}»')
    return errores


# ── Archivo nivel0.json ──────────────────────────────────────────────────────
def nivel0_json():
    return {
        'esquema': 'onelingo.nivel0.v1',
        'idioma': 'ja',
        'titulo': b('Nivel 0 · Leer y pronunciar japonés', 'Level 0 · Read and pronounce Japanese'),
        'subtitulo': b('Para quien empieza desde cero: hiragana, katakana y cómo suenan.',
                       'For complete beginners: hiragana, katakana and how they sound.'),
        'voz': 'narradora',
        'nota': 'Marcado: (kana:sonido) pinta el kana con el color de su fila (ver sonidos.json). Cada palabra lleva rom (rōmaji Hepburn modificado). Fuente: tools/contenido/nivel0-ja/generar.py. Apoyo es + en.',
        'textos': {
            'tarjeta': b('¿Empiezas de cero? Aprende hiragana y katakana y cómo se pronuncian.', 'Starting from zero? Learn hiragana and katakana and how they sound.'),
            'muestra': mk('ひらがな') + ' · ' + mk('カタカナ'),
            'emoji': '1f338',
            'junta': b('Escucha despacio y después rápido: así se lee el japonés.', 'Listen slowly, then fast: that is how you read Japanese.'),
            'mapaIntro': b('El japonés se escribe con kana: cada signo es un golpe de igual duración y suena siempre igual. Lo nuevo es el ritmo: las vocales largas, la っ pequeña, la ん y las combinaciones. Cada fila de kana tiene un color y una imagen, iguales en hiragana y en katakana. Toca una tarjeta para oírla.',
                           'Japanese is written with kana: each sign is one beat of equal length and always sounds the same. What is new is the rhythm: long vowels, the small っ, ん and the combinations. Each kana row has a color and a picture, the same in hiragana and katakana. Tap a card to hear it.'),
            'grupos': GRUPOS,
        },
        'revision': 'inicial',
        'refuerzo': {'vocales': 'u01', 'ka-sa': 'u02', 'ta-na': 'u03', 'ha-ma-ya': 'u04', 'ra-wa-n': 'u05',
                     'dakuten': 'u06', 'combinaciones': 'u07', 'largas-y-tono': 'u08', 'katakana': 'u09'},
        'evaluacion': {'lecciones': ['u10l01', 'u10l02', 'u10l03', 'u10l04'], 'pseudopalabras': ['ぬろせ', 'ヘミヌ'], 'umbral': 0.8},
        'unidades': UNIDADES,
    }


def escribir(nombre, datos):
    (DESTINO / nombre).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    errores = comprobar()
    for e in errores:
        print('ERROR', e)
    if errores:
        sys.exit(1)
    DESTINO.mkdir(parents=True, exist_ok=True)
    escribir('sonidos.json', sonidos_json())
    escribir('nivel0.json', nivel0_json())
    r = subprocess.run([sys.executable, str(RAIZ / 'tools/contenido/validar_nivel0.py'), 'ja',
                        str(DESTINO / 'nivel0.json'), '--bilingue'])
    sys.exit(r.returncode)
