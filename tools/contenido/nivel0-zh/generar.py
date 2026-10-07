#!/usr/bin/env python3
"""Genera el Nivel 0 «Pinyin, tonos y caracteres» del chino mandarín (misma estructura que el del italiano).

Escribe assets/contenido/zh/nivel0/sonidos.json y nivel0.json desde los datos
de este archivo y termina con `validar_nivel0.py zh --bilingue`.
Apoyo bilingüe {es, en}: español latino neutro con «tú», inglés americano.
Mandarín estándar, caracteres simplificados; sin historia continua; nombres solo de
tools/ia/idiomas/zh.md. Lumo solo en la bienvenida (u01l01), nunca en la evaluación (u10).
Guías de pronunciación: solo las de tools/ia/idiomas/zh.md (tonos, sandhi, aspiradas,
retroflejas, j/q/x, ü, -n/-ng, er, reglas de ortografía del pinyin).
Imágenes: solo emoji Noto ya presentes en assets/img/emoji/.

Convenciones de este nivel:
- Todo texto chino va con espacios entre palabras (la app los quita al leer en voz alta).
- Cada texto chino lleva `rom` (pinyin con tono, sandhi escrito como suena).
- Marcado: (carácter:sonido) pinta ese carácter con el color del sonido (ver sonidos.json):
  tonos t1 t2 t3 t4 tn, iniciales, finales. Un carácter es una sílaba entera; el
  color señala el rasgo que se está aprendiendo (p. ej. (你:t2) = «ní» por sandhi).
- Sin cifras arábigas en ningún texto: números en caracteres chinos o en palabras.

18 claves (curriculo/zh/f0.json · previos) → unidades:
  four-tones u01 · neutral-tone, tone-sandhi-third, yi-bu-sandhi u02 ·
  initials-labial-dental, aspirated-vs-unaspirated u03 · initials-g-k-h, initials-z-c-s u04 ·
  initials-j-q-x, initials-zh-ch-sh-r u05 · finals-simple-compound, er-erhua-awareness u06 ·
  nasal-finals-n-ng, umlaut-u, pinyin-spelling-rules u07 · what-is-a-character,
  radicals-and-strokes u08 · stroke-order-basic (+ primeras palabras reales) u09 · prueba u10.

Uso: python3 tools/contenido/nivel0-zh/generar.py
"""
import json
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
DESTINO = RAIZ / 'assets/contenido/zh/nivel0'
GRUPO = re.compile(r'\(([^():]+):([^()]+)\)')


def b(es, en):
    return {'es': es, 'en': en}


def plano(m):
    return GRUPO.sub(lambda g: g.group(1), m)


# ── Mapa de sonidos ──────────────────────────────────────────────────────────
# (id, grupo, color, (color es, en), (ancla, rom), emoji, nombre es, en, grafías, ejemplos [(m, rom)], unidad)
SONIDOS = [
    ('t1', 'tono', '#E24B4A', ('rojo', 'red'), ('书', 'shū'), '1f4d6',
     'primer tono: alto y plano, como sostener una nota: mā', 'first tone: high and level, like holding a note: mā',
     ['ā ē ī ō ū'], [('妈', 'mā'), ('咖啡', 'kāfēi')], 1),
    ('t2', 'tono', '#F08A24', ('naranja', 'orange'), ('茶', 'chá'), '1f375',
     'segundo tono: sube, como el «¿qué?» de sorpresa: má', 'second tone: rising, like a surprised “what?”: má',
     ['á é í ó ú'], [('麻', 'má'), ('学习', 'xuéxí')], 1),
    ('t3', 'tono', '#2E8B57', ('verde', 'green'), ('马', 'mǎ'), '1f434',
     'tercer tono: baja y sube; al hablar rápido solo baja: mǎ', 'third tone: dips and rises; in fast speech it just goes low: mǎ',
     ['ǎ ě ǐ ǒ ǔ'], [('水', 'shuǐ'), ('手', 'shǒu')], 1),
    ('t4', 'tono', '#1E88E5', ('azul', 'blue'), ('大', 'dà'), '1f418',
     'cuarto tono: cae de golpe, como un «¡ya!»: mà', 'fourth tone: falls sharply, like a command: mà',
     ['à è ì ò ù'], [('骂', 'mà'), ('去', 'qù')], 1),
    ('tn', 'tono', '#8E8E93', ('gris', 'gray'), ('爸爸', 'bàba'), '1f468',
     'tono neutro: sílaba breve y ligera, sin marca: bàba', 'neutral tone: short and light, no mark: bàba',
     ['sin marca'], [('妈妈', 'māma'), ('谢谢', 'xièxie')], 2),
    ('b', 'labial', '#D4A017', ('dorado', 'gold'), ('包', 'bāo'), '1f45c',
     'b: como la «p» española de «paso», sin soplo', 'b: like the p in “spin,” no puff of air',
     ['b'], [('爸爸', 'bàba'), ('北京', 'Běijīng')], 3),
    ('p', 'labial', '#D84315', ('teja', 'brick'), ('苹果', 'píngguǒ'), '1f34e',
     'p: con un soplo fuerte de aire', 'p: with a strong puff of air, as in “pin”',
     ['p'], [('朋友', 'péngyou'), ('拼音', 'pīnyīn')], 3),
    ('m', 'labial', '#E0559B', ('rosa', 'pink'), ('米饭', 'mǐfàn'), '1f35a',
     'm: como en español', 'm: as in English',
     ['m'], [('妈妈', 'māma'), ('米饭', 'mǐfàn')], 3),
    ('f', 'labial', '#7CB342', ('lima', 'lime'), ('饭', 'fàn'), '1f372',
     'f: como en español', 'f: as in English',
     ['f'], [('饭', 'fàn'), ('飞机', 'fēijī')], 3),
    ('d', 'dental', '#00A6A6', ('turquesa', 'teal'), ('弟弟', 'dìdi'), '1f466',
     'd: como la «t» española de «tela», sin soplo', 'd: like the t in “sty,” no puff of air',
     ['d'], [('大', 'dà'), ('电话', 'diànhuà')], 3),
    ('t', 'dental', '#26A69A', ('verde agua', 'aqua'), ('太阳', 'tàiyang'), '2600',
     't: con un soplo fuerte de aire', 't: with a strong puff of air, as in “tie”',
     ['t'], [('他', 'tā'), ('太阳', 'tàiyang')], 3),
    ('n', 'dental', '#455A64', ('pizarra', 'slate'), ('鸟', 'niǎo'), '1f426',
     'n: como en español', 'n: as in English',
     ['n'], [('牛奶', 'niúnǎi'), ('你', 'nǐ')], 3),
    ('l', 'dental', '#6B8E23', ('oliva', 'olive'), ('梨', 'lí'), '1f350',
     'l: como en español', 'l: as in English',
     ['l'], [('老师', 'lǎoshī'), ('六', 'liù')], 3),
    ('g', 'velar', '#5D4037', ('café', 'coffee'), ('狗', 'gǒu'), '1f436',
     'g: como la «c» de «casa», sin soplo (no es la g sonora española)', 'g: like the k in “sky,” no puff (not English voiced g)',
     ['g'], [('哥哥', 'gēge'), ('个', 'gè')], 4),
    ('k', 'velar', '#795548', ('chocolate', 'chocolate'), ('可乐', 'kělè'), '1f964',
     'k: con un soplo fuerte de aire', 'k: with a strong puff of air, as in “kite”',
     ['k'], [('课', 'kè'), ('看', 'kàn')], 4),
    ('h', 'velar', '#8D6E63', ('café con leche', 'latte'), ('花', 'huā'), '1f338',
     'h: como la «j» española suave, más ligera', 'h: a light, raspy “h” (closer to Spanish j or German ch in Bach)',
     ['h'], [('好', 'hǎo'), ('喝', 'hē')], 4),
    ('z', 'sibilante', '#C0CA33', ('pistacho', 'pistachio'), ('嘴', 'zuǐ'), '1f444',
     'z: una «ts» sin soplo (casi «ds»)', 'z: like “ds” in “kids,” unvoiced, no puff',
     ['z'], [('做', 'zuò'), ('字', 'zì')], 4),
    ('c', 'sibilante', '#FF7043', ('coral', 'coral'), ('菜', 'cài'), '1f957',
     'c: una «ts» con soplo fuerte', 'c: like “ts” in “cats” with a strong puff',
     ['c'], [('菜', 'cài'), ('错', 'cuò')], 4),
    ('s', 'sibilante', '#3949AB', ('índigo', 'indigo'), ('松树', 'sōngshù'), '1f332',
     's: la «s» española', 's: like the s in “see”',
     ['s'], [('三', 'sān'), ('四', 'sì')], 4),
    ('j', 'palatal', '#9C6ADE', ('lila', 'lilac'), ('鸡', 'jī'), '1f414',
     'j: una «ch» suave y sin soplo (no es la «j» española)', 'j: like “j” in “jeep,” but unvoiced and tenser',
     ['j + i, ü'], [('鸡', 'jī'), ('九', 'jiǔ')], 5),
    ('q', 'palatal', '#7E57C2', ('morado', 'purple'), ('球', 'qiú'), '26bd',
     'q: como j pero con soplo, más suave que la «ch» española', 'q: like “ch” in “cheese,” with a puff',
     ['q + i, ü'], [('七', 'qī'), ('请', 'qǐng')], 5),
    ('x', 'palatal', '#C2185B', ('frambuesa', 'raspberry'), ('香蕉', 'xiāngjiāo'), '1f34c',
     'x: una «s» suave que roza «sh» (no es la «x» española)', 'x: like “sh” in “she,” but tongue flat and lips spread',
     ['x + i, ü'], [('小', 'xiǎo'), ('谢谢', 'xièxie')], 5),
    ('zh', 'retroflejo', '#AD1457', ('granate', 'maroon'), ('猪', 'zhū'), '1f437',
     'zh: como «ch» sin soplo, con la lengua curvada hacia atrás', 'zh: like “j” in “jam,” unvoiced, tongue curled back',
     ['zh'], [('这', 'zhè'), ('中国', 'Zhōngguó')], 5),
    ('ch', 'retroflejo', '#E8B923', ('amarillo', 'yellow'), ('吃', 'chī'), '1f37d',
     'ch: lo mismo que zh, pero con soplo', 'ch: like “ch” in “church,” tongue back, with a puff',
     ['ch'], [('车', 'chē'), ('吃饭', 'chīfàn')], 5),
    ('sh', 'retroflejo', '#00897B', ('esmeralda', 'emerald'), ('山', 'shān'), '26f0',
     'sh: la «sh» de «she», con la lengua atrás', 'sh: like “sh” in “she,” tongue back',
     ['sh'], [('书', 'shū'), ('老师', 'lǎoshī')], 5),
    ('r', 'retroflejo', '#FF8F00', ('ámbar', 'amber'), ('肉', 'ròu'), '1f357',
     'r: como la «r» inglesa de «red», con zumbido; nunca la «r» española', 'r: like English “r” in “red,” with a buzz',
     ['r'], [('人', 'rén'), ('热', 'rè')], 5),
    ('ih', 'especial', '#9E9E9E', ('plateado', 'silver'), ('四', 'sì'), '1f522',
     'la «i» de zi, ci, si, zhi, chi, shi, ri: no es «i», es un zumbido de la consonante', 'the “i” in zi, ci, si, zhi, chi, shi, ri: not “ee,” a buzz of the consonant',
     ['i tras z c s zh ch sh r'], [('字', 'zì'), ('词', 'cí')], 4),
    ('a', 'vocal', '#FF5252', ('rojo claro', 'light red'), ('妈', 'mā'), '1f469',
     'a: como en español', 'a: like “ah”',
     ['a'], [('大', 'dà'), ('爸爸', 'bàba')], 6),
    ('e', 'vocal', '#FDD835', ('amarillo limón', 'lemon'), ('车', 'chē'), '1f697',
     'e ≈ «o» con los labios estirados', 'e: unrounded “uh” from the back of the mouth',
     ['e'], [('喝', 'hē'), ('可乐', 'kělè')], 6),
    ('i', 'vocal', '#EC407A', ('rosa fuerte', 'hot pink'), ('一', 'yī'), '0031_20e3',
     'i: como la «i» española', 'i: like “ee”',
     ['i'], [('米', 'mǐ'), ('鸡', 'jī')], 6),
    ('u', 'vocal', '#42A5F5', ('azul cielo', 'sky blue'), ('乌龟', 'wūguī'), '1f422',
     'u: como la «u» española', 'u: like “oo”',
     ['u'], [('五', 'wǔ'), ('书', 'shū')], 6),
    ('yu', 'vocal', '#AB47BC', ('violeta', 'violet'), ('鱼', 'yú'), '1f41f',
     'ü: di «i» con los labios en posición de «u» (como la «u» del francés)', 'ü: say “ee” with rounded lips (like French u)',
     ['ü', 'u tras j q x y'], [('女', 'nǚ'), ('绿', 'lǜ')], 7),
    ('er', 'vocal', '#26C6DA', ('celeste', 'cyan'), ('耳朵', 'ěrduo'), '1f442',
     'er: vocal con la lengua curvada hacia atrás, como la «er» de «her»', 'er: like “er” in American “her”',
     ['er'], [('二', 'èr'), ('儿子', 'érzi')], 6),
    ('ai', 'compuesta', '#66BB6A', ('verde hoja', 'leaf green'), ('爱', 'ài'), '2764',
     'ai: dos vocales que se deslizan: ài', 'ai: two vowels gliding together: ài',
     ['ai'], [('爱', 'ài'), ('菜', 'cài')], 6),
    ('ei', 'compuesta', '#9CCC65', ('verde claro', 'light green'), ('飞机', 'fēijī'), '2708',
     'ei: dos vocales que se deslizan: fēi', 'ei: two vowels gliding together: fēi',
     ['ei'], [('飞机', 'fēijī'), ('美国', 'Měiguó')], 6),
    ('ao', 'compuesta', '#FFA726', ('mandarina', 'tangerine'), ('猫', 'māo'), '1f431',
     'ao: dos vocales que se deslizan: māo', 'ao: two vowels gliding together: māo',
     ['ao'], [('猫', 'māo'), ('好', 'hǎo')], 6),
    ('ou', 'compuesta', '#BCAAA4', ('arena', 'sand'), ('手', 'shǒu'), '270b',
     'ou: dos vocales que se deslizan: shǒu', 'ou: two vowels gliding together: shǒu',
     ['ou'], [('手', 'shǒu'), ('狗', 'gǒu')], 6),
    ('iu', 'compuesta', '#D4E157', ('lima suave', 'soft lime'), ('牛', 'niú'), '1f404',
     'iu = «iou»: jiǔ ≈ «jiou»', 'iu = “iou”: jiǔ ≈ “jyoh”',
     ['iu'], [('九', 'jiǔ'), ('六', 'liù')], 6),
    ('ui', 'compuesta', '#4DB6AC', ('turquesa suave', 'soft teal'), ('水', 'shuǐ'), '1f4a7',
     'ui = «uei»: guì ≈ «guei»', 'ui = “uei”: guì ≈ “gway”',
     ['ui'], [('贵', 'guì'), ('水', 'shuǐ')], 6),
    ('ian', 'compuesta', '#29B6F6', ('azul claro', 'light blue'), ('天', 'tiān'), '2601',
     'ian ≈ «ien»: tiān ≈ «tien»', 'ian ≈ “yen”: tiān ≈ “tyen”',
     ['ian'], [('天', 'tiān'), ('电话', 'diànhuà')], 6),
    ('ie', 'compuesta', '#FF8A65', ('salmón', 'salmon'), ('鞋', 'xié'), '1f45e',
     'ie ≈ «ié»: xiè', 'ie ≈ “ye”: xiè',
     ['ie'], [('谢谢', 'xièxie'), ('鞋', 'xié')], 6),
    ('n', 'nasal', '#5C6BC0', ('azul violáceo', 'periwinkle'), ('门', 'mén'), '1f6aa',
     'final -n: la lengua en las encías, como la «n» de «pan»', 'final -n: tongue on the gum ridge, like “n” in “pan”',
     ['an en in un ün'], [('新', 'xīn'), ('饭', 'fàn')], 7),
    ('ng', 'nasal', '#283593', ('azul noche', 'navy'), ('星', 'xīng'), '2b50',
     'final -ng: la «n» de «banco» o «tengo», sin g aparte', 'final -ng: like “ng” in “sing,” no separate g',
     ['ang eng ing ong'], [('中国', 'Zhōngguó'), ('放', 'fàng')], 7),
]

GRUPOS = {
    'tono': b('Cuatro tonos y tono neutro', 'Four tones and the neutral tone'),
    'labial': b('Iniciales b, p, m, f', 'Initials b, p, m, f'),
    'dental': b('Iniciales d, t, n, l', 'Initials d, t, n, l'),
    'velar': b('Iniciales g, k, h', 'Initials g, k, h'),
    'sibilante': b('Iniciales z, c, s', 'Initials z, c, s'),
    'palatal': b('Iniciales j, q, x', 'Initials j, q, x'),
    'retroflejo': b('Retroflejas zh, ch, sh, r', 'Retroflexes zh, ch, sh, r'),
    'especial': b('La «i» zumbada', 'The buzzed “i”'),
    'vocal': b('Finales simples, ü y er', 'Simple finals, ü and er'),
    'compuesta': b('Finales compuestas', 'Compound finals'),
    'nasal': b('Finales -n y -ng', 'Finals -n and -ng'),
}


def sonidos_json():
    return {
        'esquema': 'onelingo.sonidos.v1',
        'idioma': 'zh',
        'nota': 'Mapa de sonidos del mandarín estándar (pinyin). El color acompaña siempre al nombre y a la imagen; es una pista de escucha, no una transcripción fonética. Los tonos (t1–t4, tn) se pintan sobre el carácter entero; el resto de sonidos señalan la inicial o la final que se estudia en esa sílaba. «anclaRom» y «ejemplosRom» llevan el pinyin con tono de cada ejemplo.',
        'marcas': {'_': 'letra que no suena', '=': 'varias letras, un sonido'},
        'acento': b('Modelo: mandarín estándar (普通话), caracteres simplificados. La erhua y los regionalismos solo se reconocen, mucho más adelante.',
                    'Model: standard Mandarin (普通话), simplified characters. Erhua and regionalisms are only recognized, much later.'),
        'vocales': [
            {'id': i, 'grupo': g, 'color': c, 'colorNombre': b(*cn), 'ancla': a[0], 'anclaRom': a[1], 'emoji': e,
             'nombre': b(nes, nen), 'grafias': gr, 'ejemplos': [x[0] for x in ej], 'ejemplosRom': [x[1] for x in ej],
             'unidad': u}
            for i, g, c, cn, a, e, nes, nen, gr, ej, u in SONIDOS
        ],
    }


# ── Lecciones ────────────────────────────────────────────────────────────────
def O(o):
    """Opción: cadena (pinyin u otro texto) o tupla (m, rom)."""
    if isinstance(o, str):
        return {'m': o}
    d = {'m': o[0]}
    if len(o) > 1 and o[1]:
        d['rom'] = o[1]
    return d


def W(m, rom, es, en, e=None):
    w = {'m': m, 'rom': rom, 't': b(es, en)}
    if e:
        w['e'] = e
    return w


ESCUCHA_ELIGE = b('¿Qué palabra oyes?', 'Which word do you hear?')
TOCA = b('Escucha y toca la palabra con el sonido marcado.', 'Listen and tap the word with the marked sound.')
CUAL_INVENTADA = ('¿Cuál sílaba no existe en pinyin?', 'Which syllable does not exist in pinyin?')
PSEUDO = ('Sílaba inventada: no existe en pinyin.', 'Made-up syllable: it does not exist in pinyin.')


def L(lid, tes, ten, palabras, mira, foco=None, par=None, oye=None, extras=(), construye=None, inv=False, nota=None):
    """Plantilla: escucha → mira → repite → [toca_sonido] → [escucha_elige] → extras → construye.
    mira = (m, rom, es, en); par = (con el sonido foco, sin él), cada uno (m, rom);
    oye = (correcta, distractor), cada uno (m, rom); construye = (m, rom, ficha extra)."""
    pasos = [{'tipo': 'escucha', 'palabras': palabras}]
    m0, r0, mes, men = mira
    paso = {'tipo': 'mira', 'm': m0, 'rom': r0, 'texto': b(mes, men)}
    if foco:
        paso['sonido'] = foco
    if nota:
        paso['nota'] = b(*nota)
    pasos.append(paso)
    pasos.append({'tipo': 'repite', 'm': palabras[0]['m'], 'rom': palabras[0]['rom'], 't': palabras[0]['t']})
    if foco and par:
        ops = [O(par[0]), O(par[1])]
        if inv:
            ops.reverse()
        pasos.append({'tipo': 'toca_sonido', 'sonido': foco, 'pregunta': TOCA, 'opciones': ops, 'correcta': 1 if inv else 0})
    if oye:
        ops = [O(oye[0]), O(oye[1])]
        if not inv:
            ops.reverse()
        pasos.append({'tipo': 'escucha_elige', 'audio': plano(oye[0][0]), 'pregunta': ESCUCHA_ELIGE,
                      'opciones': ops, 'correcta': 0 if inv else 1})
    pasos += list(extras)
    if construye:
        m, rom, extra = construye
        pasos.append({'tipo': 'construye', 'm': m, 'rom': rom, 'fichas': list(plano(m)) + [extra]})
    return {'id': lid, 'titulo': b(tes, ten), 'pasos': pasos}


def lee(m, rom, tes, ten, pes, pen, ops, correcta=0):
    p = {'tipo': 'lee', 'm': m, 't': b(tes, ten), 'pregunta': b(pes, pen),
         'opciones': [O(o) for o in ops], 'correcta': correcta}
    if rom:
        p['rom'] = rom
    return p


def significado(m, rom, pes, pen, ops, correcta=0):
    p = {'tipo': 'elige_significado', 'm': m, 'pregunta': b(pes, pen),
         'opciones': [b(*o) for o in ops], 'correcta': correcta}
    if rom:
        p['rom'] = rom
    return p


def sig(m, rom, pes, pen):
    """«¿Qué significa?» con dos opciones (la primera es la correcta)."""
    return significado(m, rom, '¿Qué significa?', 'What does it mean?', [pes, pen])


def oye(correcta, otra, inv=False):
    return {'tipo': 'escucha_elige', 'audio': plano(correcta[0]), 'pregunta': ESCUCHA_ELIGE,
            'opciones': [O(correcta), O(otra)] if not inv else [O(otra), O(correcta)],
            'correcta': 1 if inv else 0}


def toca(foco, si, no, inv=False):
    ops = [O(si), O(no)]
    if inv:
        ops.reverse()
    return {'tipo': 'toca_sonido', 'sonido': foco, 'pregunta': TOCA, 'opciones': ops, 'correcta': 1 if inv else 0}


def tono(m, rom, correcto):
    """«¿Qué tono tiene?»: correcto = 1, 2, 3, 4 o 0 (neutro)."""
    ops = [
        ('Primero: alto y plano', 'First: high and level'),
        ('Segundo: sube', 'Second: rising'),
        ('Tercero: baja y sube', 'Third: dips and rises'),
        ('Cuarto: cae de golpe', 'Fourth: falls sharply'),
        ('Neutro: breve y ligero', 'Neutral: short and light'),
    ]
    idx = {1: 0, 2: 1, 3: 2, 4: 3, 0: 4}[correcto]
    otros = [o for k, o in enumerate(ops) if k != idx][:2]
    return significado(m, rom, '¿Qué tono tiene esta sílaba?', 'Which tone does this syllable have?', [ops[idx]] + otros)


UNIDADES = [
    # ── u01 ──────────────────────────────────────────────────────────────────
    {
        'id': 'u01', 'titulo': b('Z1 · Los cuatro tonos', 'Z1 · The four tones'),
        'objetivo': b('Oír y distinguir los cuatro tonos del mandarín en la sílaba ma y en palabras reales: mā, má, mǎ, mà.',
                      'Hear and tell apart the four Mandarin tones on the syllable ma and in real words: mā, má, mǎ, mà.'),
        'lecciones': [
            L('u01l01', 'Hola, chino: el primer tono', 'Hello, Chinese: the first tone',
              [W('(妈:t1)', 'mā', 'mamá', 'mom', '1f469'), W('(书:t1)', 'shū', 'libro', 'book', '1f4d6'), W('(咖啡:t1)', 'kāfēi', 'café', 'coffee', '2615')],
              ('(妈:t1)', 'mā',
               'El chino se escribe con caracteres, y el pinyin es el alfabeto que usamos para leer cómo suenan. Cada sílaba lleva un tono: la melodía forma parte de la palabra, como una letra. El primer tono es alto y plano, como sostener una nota; en el pinyin se marca con una raya sobre la vocal: mā.',
               'Chinese is written with characters, and pinyin is the alphabet we use to read how they sound. Every syllable has a tone: the melody is part of the word, like a letter. The first tone is high and level, like holding a note; in pinyin it is marked with a bar over the vowel: mā.'),
              foco='t1', par=(('(妈:t1)', 'mā'), ('马', 'mǎ')), oye=(('妈', 'mā'), ('马', 'mǎ')),
              extras=[
                  {'tipo': 'lumo', 'pose': 'anima', 'texto': b('Bienvenido al chino. Primero escucharás, después leerás. Cada sílaba tiene su melodía: ¡los colores te ayudan a recordar cada tono!',
                                                              'Welcome to Chinese. First you listen, then you read. Every syllable has its own melody: the colors help you remember each tone!')},
                  sig('妈', 'mā', ('mamá', 'mom'), ('caballo', 'horse')),
              ],
              construye=('咖啡', 'kāfēi', '书')),
            L('u01l02', 'El segundo tono: sube', 'The second tone: rising',
              [W('(茶:t2)', 'chá', 'té', 'tea', '1f375'), W('(人:t2)', 'rén', 'persona', 'person', '1f465'), W('(学习:t2)', 'xuéxí', 'estudiar', 'to study')],
              ('(茶:t2)', 'chá',
               'El segundo tono sube, como el «¿qué?» de sorpresa: má, chá. Cuidado: ese «¿qué?» es solo para imaginar el movimiento. En chino una pregunta no sube el tono de la última sílaba; el tono pertenece a la palabra.',
               'The second tone rises, like a surprised “what?”: má, chá. That “what?” is only to picture the movement. In Chinese a question does not raise the tone of the last syllable; the tone belongs to the word.'),
              foco='t2', par=(('(茶:t2)', 'chá'), ('书', 'shū')), oye=(('麻', 'má'), ('妈', 'mā')),
              extras=[sig('茶', 'chá', ('té', 'tea'), ('café', 'coffee')), tono('人', 'rén', 2)],
              construye=('学习', 'xuéxí', '书')),
            L('u01l03', 'El tercer tono: baja y sube', 'The third tone: dips and rises',
              [W('(马:t3)', 'mǎ', 'caballo', 'horse', '1f434'), W('(手:t3)', 'shǒu', 'mano', 'hand', '270b'), W('(火:t3)车', 'huǒchē', 'tren', 'train', '1f686')],
              ('(马:t3)', 'mǎ',
               'El tercer tono baja y vuelve a subir: mǎ. Al hablar rápido, en el medio de una frase, casi solo baja («medio tercero»). No lo confundas con el segundo, que solo sube.',
               'The third tone dips and then rises again: mǎ. In fast speech it mostly just goes low (a “half third”). Do not confuse it with the second tone, which only rises.'),
              foco='t3', par=(('(马:t3)', 'mǎ'), ('妈', 'mā')), oye=(('马', 'mǎ'), ('麻', 'má')), inv=True,
              extras=[sig('马', 'mǎ', ('caballo', 'horse'), ('mamá', 'mom')), tono('手', 'shǒu', 3)],
              construye=('火车', 'huǒchē', '手')),
            L('u01l04', 'El cuarto tono: cae', 'The fourth tone: falling',
              [W('(大:t4)', 'dà', 'grande', 'big', '1f418'), W('(去:t4)', 'qù', 'ir', 'to go'), W('(再见:t4)', 'zàijiàn', 'adiós', 'goodbye', '1f44b')],
              ('(大:t4)', 'dà',
               'El cuarto tono cae de golpe, como un «¡ya!» o una orden: mà, dà. Ahora tienes los cuatro: mā (alto y plano), má (sube), mǎ (baja y sube), mà (cae). Escucha la misma sílaba con cada uno.',
               'The fourth tone falls sharply, like a command: mà, dà. Now you have all four: mā (high and level), má (rising), mǎ (dips and rises), mà (falling). Listen to the same syllable with each one.'),
              foco='t4', par=(('(大:t4)', 'dà'), ('马', 'mǎ')), oye=(('骂', 'mà'), ('妈', 'mā')),
              extras=[tono('大', 'dà', 4), tono('妈', 'mā', 1), tono('马', 'mǎ', 3)],
              construye=('再见', 'zàijiàn', '去')),
            L('u01l05', 'Pares que cambian el sentido', 'Pairs that change the meaning',
              [W('买', 'mǎi', 'comprar', 'to buy'), W('(卖:t4)', 'mài', 'vender', 'to sell'), W('(四:t4)', 'sì', 'cuatro', 'four'), W('死', 'sǐ', 'morir', 'to die')],
              ('(卖:t4)', 'mài',
               'Un solo tono cambia la palabra: mǎi 买 (comprar) y mài 卖 (vender); wèn 问 (preguntar) y wén 文 (escritura); sì 四 (cuatro) y sǐ 死 (morir); mā 妈 (mamá) y mǎ 马 (caballo). El tono es parte de la palabra.',
               'A single tone changes the word: mǎi 买 (to buy) and mài 卖 (to sell); wèn 问 (to ask) and wén 文 (writing); sì 四 (four) and sǐ 死 (to die); mā 妈 (mom) and mǎ 马 (horse). The tone is part of the word.'),
              foco='t4', par=(('(卖:t4)', 'mài'), ('买', 'mǎi')), oye=(('卖', 'mài'), ('买', 'mǎi')), inv=True,
              nota=('⚠ 四 sì (cuatro) no es «sí»; y 死 sǐ significa «morir», por eso algunas personas evitan el número cuatro en la cultura china.',
                    'Sì (four) is not the Spanish word sí; and 死 sǐ means “to die,” which is why some people avoid the number four in Chinese culture.'),
              extras=[sig('买', 'mǎi', ('comprar', 'to buy'), ('vender', 'to sell')),
                      oye(('问', 'wèn'), ('文', 'wén')),
                      sig('文', 'wén', ('escritura; lengua escrita', 'writing; written language'), ('preguntar', 'to ask')),
                      oye(('死', 'sǐ'), ('四', 'sì'), inv=True)]),
        ],
    },
    # ── u02 ──────────────────────────────────────────────────────────────────
    {
        'id': 'u02', 'titulo': b('Z2 · Tono neutro y cambios de tono', 'Z2 · Neutral tone and tone changes'),
        'objetivo': b('Decir el tono neutro y aplicar los cambios de tono: dos terceros seguidos (ní hǎo), 不 (bù, bú) y 一 (yī, yí, yì).',
                      'Say the neutral tone and apply the tone changes: two third tones in a row (ní hǎo), 不 (bù, bú) and 一 (yī, yí, yì).'),
        'lecciones': [
            L('u02l01', 'Tono neutro: sílaba breve', 'Neutral tone: a short syllable',
              [W('妈(妈:tn)', 'māma', 'mamá', 'mom', '1f469'), W('爸(爸:tn)', 'bàba', 'papá', 'dad', '1f468'), W('谢(谢:tn)', 'xièxie', 'gracias', 'thank you', '1f64f')],
              ('妈(妈:tn)', 'māma',
               'La segunda sílaba de 妈妈 es de tono neutro: breve, ligera y sin marca. Se escribe māma, no «mā-mā». La sílaba sin marca se dice rápido y suave, y se apoya en el tono de la sílaba anterior.',
               'The second syllable of 妈妈 has the neutral tone: short, light and unmarked. It is written māma, not “mā-mā.” The unmarked syllable is said quickly and softly, leaning on the tone of the syllable before it.'),
              foco='tn', par=(('爸(爸:tn)', 'bàba'), ('火车', 'huǒchē')), oye=(('妈妈', 'māma'), ('妈', 'mā')),
              extras=[sig('谢谢', 'xièxie', ('gracias', 'thank you'), ('adiós', 'goodbye')), tono('爸', 'bà', 4)],
              construye=('爸爸', 'bàba', '妈')),
            L('u02l02', 'Tono neutro en palabras comunes', 'Neutral tone in common words',
              [W('名(字:tn)', 'míngzi', 'nombre', 'name'), W('学(生:tn)', 'xuésheng', 'estudiante', 'student'), W('你(们:tn)', 'nǐmen', 'ustedes', 'you (plural)')],
              ('你(们:tn)', 'nǐmen',
               'El tono neutro también aparece en partículas como 吗 ma y en palabras como míngzi (名字), xuésheng (学生) y nǐmen (你们). En una pregunta con 吗, la última sílaba no sube: no uses la entonación española de pregunta.',
               'The neutral tone also appears in particles like 吗 ma and in words like míngzi (名字), xuésheng (学生) and nǐmen (你们). In a question with 吗 the last syllable does not rise: do not use English question intonation.'),
              foco='tn', par=(('学(生:tn)', 'xuésheng'), ('茶', 'chá')), oye=(('名字', 'míngzi'), ('明天', 'míngtiān')),
              extras=[significado('你 好 吗？', 'Ní hǎo ma?', '¿Cómo suena 吗 al final?', 'How does 吗 sound at the end?',
                                  [('Breve y ligera (tono neutro); no sube como una pregunta en español', 'Short and light (neutral tone); it does not rise like an English question'),
                                   ('Sube mucho, como una pregunta', 'Rises a lot, like a question')]),
                      sig('学生', 'xuésheng', ('estudiante', 'student'), ('profesor', 'teacher'))],
              construye=('学生', 'xuésheng', '名')),
            L('u02l03', 'Dos terceros tonos seguidos', 'Two third tones in a row',
              [W('(你:t2) 好', 'ní hǎo', 'hola', 'hello', '1f44b'), W('(水:t2)果', 'shuíguǒ', 'fruta', 'fruit', '1f34e'), W('(我:t2) (很:t2) 好', 'wó hén hǎo', 'estoy muy bien', 'I am very well')],
              ('(你:t2) 好', 'ní hǎo',
               'Cuando dos sílabas de tercer tono van juntas, la primera sube y se dice como segundo tono: nǐ hǎo se dice «ní hǎo». En una cadena de terceros, todos menos el último suben: wó hén hǎo. Lo mismo dentro de una palabra: shuíguǒ. Una coma o un punto corta la cadena. En este curso el pinyin se escribe como suena.',
               'When two third-tone syllables come together, the first one rises and is said as a second tone: nǐ hǎo is said “ní hǎo.” In a chain of third tones, all but the last one rise: wó hén hǎo. The same happens inside a word: shuíguǒ. A comma or a period breaks the chain. In this course, pinyin is written as it sounds.'),
              foco='t2', par=(('(你:t2) 好', 'ní hǎo'), ('老师', 'lǎoshī')),
              extras=[lee('我 很 好', None, 'estoy muy bien', 'I am very well', '¿Cómo se dice en voz alta?', 'How is it said aloud?', ['wó hén hǎo', 'wǒ hěn hǎo']),
                      lee('老师', None, 'profesor; profesora', 'teacher', 'Tercero + primero: ¿cambia algún tono?', 'Third + first: does any tone change?', ['lǎoshī', 'láoshī']),
                      sig('哪里', 'nálǐ', ('dónde', 'where'), ('qué', 'what'))],
              construye=('水果', 'shuíguǒ', '手')),
            L('u02l04', 'El cambio de 不: bù y bú', 'The change in 不: bù and bú',
              [W('(不:t2) 是', 'bú shì', 'no es', 'is not'), W('不 好', 'bù hǎo', 'no es bueno; no está bien', 'not good'), W('(不:t2) 客气', 'bú kèqi', 'de nada', 'you’re welcome')],
              ('(不:t2) 是', 'bú shì',
               'Solo, 不 es bù (cuarto tono). Ante otro cuarto tono pasa a bú: 不 是 bú shì, 不 客气 bú kèqi. Ante primero, segundo o tercer tono se queda bù: bù hē, bù lái, bù hǎo.',
               'By itself, 不 is bù (fourth tone). Before another fourth tone it becomes bú: 不 是 bú shì, 不 客气 bú kèqi. Before a first, second or third tone it stays bù: bù hē, bù lái, bù hǎo.'),
              foco='t2', par=(('(不:t2) 是', 'bú shì'), ('不 好', 'bù hǎo')), oye=(('不 是', 'bú shì'), ('不 好', 'bù hǎo')),
              extras=[lee('不 是', None, 'no es', 'is not', '¿Cómo se lee?', 'How is it read?', ['bú shì', 'bù shì']),
                      lee('不 来', None, 'no viene', 'does not come', '¿Cómo se lee?', 'How is it read?', ['bù lái', 'bú lái']),
                      sig('不 客气', 'bú kèqi', ('de nada', 'you’re welcome'), ('perdón', 'sorry'))]),
            L('u02l05', 'El cambio de 一: yī, yí y yì', 'The change in 一: yī, yí and yì',
              [W('(一:t2) 个', 'yí gè', 'uno; un', 'one; a'), W('(一:t4) 杯', 'yì bēi', 'una taza; un vaso', 'a cup; a glass', '2615'), W('(一:t4) 本', 'yì běn', 'un (libro)', 'one (book)', '1f4d8')],
              ('(一:t4) 杯', 'yì bēi',
               'Solo, contando o en números y fechas, 一 es yī: yī, èr, sān, y 十一 shíyī. Ante un cuarto tono pasa a yí: 一 个 yí gè. Ante primero, segundo o tercer tono pasa a yì: 一 杯 yì bēi, 一 年 yì nián, 一 本 yì běn. El clasificador 个 siempre es gè.',
               'On its own, counting, or in numbers and dates, 一 is yī: yī, èr, sān, and 十一 shíyī. Before a fourth tone it becomes yí: 一 个 yí gè. Before a first, second or third tone it becomes yì: 一 杯 yì bēi, 一 年 yì nián, 一 本 yì běn. The classifier 个 is always gè.'),
              foco='t4', par=(('(一:t4) 杯', 'yì bēi'), ('(一:t2) 个', 'yí gè')), oye=(('一 本', 'yì běn'), ('一 个', 'yí gè'), ),
              extras=[lee('一 杯', None, 'una taza', 'a cup', '¿Cómo se lee?', 'How is it read?', ['yì bēi', 'yí bēi']),
                      lee('一 个', None, 'uno', 'one', '¿Cómo se lee?', 'How is it read?', ['yí gè', 'yì gè']),
                      sig('十一', 'shíyī', ('once', 'eleven'), ('uno', 'one'))]),
        ],
    },
    # ── u03 ──────────────────────────────────────────────────────────────────
    {
        'id': 'u03', 'titulo': b('Z3 · Iniciales b, p, m, f, d, t, n, l', 'Z3 · Initials b, p, m, f, d, t, n, l'),
        'objetivo': b('Leer las iniciales labiales y dentales y distinguir las no aspiradas (b, d) de las aspiradas (p, t).',
                      'Read the labial and dental initials and tell the unaspirated (b, d) from the aspirated (p, t).'),
        'lecciones': [
            L('u03l01', 'm, f, n, l: casi como en español', 'm, f, n, l: close to English',
              [W('(妈:m)妈', 'māma', 'mamá', 'mom', '1f469'), W('米(饭:f)', 'mǐfàn', 'arroz (cocido)', 'cooked rice', '1f35a'), W('(牛:n)奶', 'niúnǎi', 'leche', 'milk', '1f95b'), W('(老:l)师', 'lǎoshī', 'profesor; profesora', 'teacher')],
              ('米(饭:f)', 'mǐfàn',
               'm, f, n y l suenan casi como en español: māma, fàn, niúnǎi, lǎoshī. Lo nuevo es que cada sílaba lleva también su tono.',
               'm, f, n and l sound close to English: māma, fàn, niúnǎi, lǎoshī. What is new is that every syllable also carries its tone.'),
              foco='f', par=(('米(饭:f)', 'mǐfàn'), ('老师', 'lǎoshī')), oye=(('牛奶', 'niúnǎi'), ('老师', 'lǎoshī')),
              nota=('⚠ 米 mǐ significa «arroz» (también «metro»); no es la sílaba «mi». En 米饭 mǐfàn, 饭 fàn es el arroz cocido o la comida.',
                    'The word 米 mǐ means “rice” (also “meter”); here 饭 fàn is cooked rice or a meal.'),
              extras=[sig('米饭', 'mǐfàn', ('arroz (cocido)', 'cooked rice'), ('leche', 'milk')), toca('n', ('(牛:n)奶', 'niúnǎi'), ('妈妈', 'māma'))],
              construye=('牛奶', 'niúnǎi', '饭')),
            L('u03l02', 'b y p: sin soplo y con soplo', 'b and p: no puff and puff',
              [W('(爸:b)爸', 'bàba', 'papá', 'dad', '1f468'), W('(朋:p)友', 'péngyou', 'amigo; amiga', 'friend', '1f91d'), W('(苹:p)果', 'píngguǒ', 'manzana', 'apple', '1f34e')],
              ('(苹:p)果', 'píngguǒ',
               'b, d y g no son sonoras como en español: b suena como la «p» de «paso», sin soplo. p, en cambio, lleva un soplo fuerte de aire. Acerca una hoja de papel a la boca: se mueve con p y no con b.',
               'b, d, g are not voiced like English b, d, g: b sounds like the p in “spin,” with no puff. p carries a strong puff of air. Hold a sheet of paper close to your mouth: it moves with p, not with b.'),
              foco='p', par=(('(苹:p)果', 'píngguǒ'), ('(爸:b)爸', 'bàba')), oye=(('怕', 'pà'), ('爸', 'bà')),
              extras=[sig('怕', 'pà', ('tener miedo', 'to be afraid'), ('papá', 'dad')), toca('b', ('(爸:b)爸', 'bàba'), ('朋友', 'péngyou'))],
              construye=('朋友', 'péngyou', '爸')),
            L('u03l03', 'd y t: sin soplo y con soplo', 'd and t: no puff and puff',
              [W('(大:d)', 'dà', 'grande', 'big', '1f418'), W('(弟:d)弟', 'dìdi', 'hermano menor', 'younger brother', '1f466'), W('(太:t)阳', 'tàiyang', 'sol', 'sun', '2600')],
              ('(太:t)阳', 'tàiyang',
               'd suena como la «t» española de «tela», sin soplo; t lleva un soplo fuerte de aire. Es el mismo contraste que b y p: dà (sin soplo) frente a tā (con soplo).',
               'd sounds like the t in “sty,” with no puff; t carries a strong puff of air. It is the same contrast as b and p: dà (no puff) versus tā (puff).'),
              foco='t', par=(('(太:t)阳', 'tàiyang'), ('(弟:d)弟', 'dìdi')), oye=(('对', 'duì'), ('退', 'tuì')), inv=True,
              extras=[sig('对', 'duì', ('correcto', 'correct'), ('retroceder', 'to retreat')), toca('d', ('(大:d)', 'dà'), ('太阳', 'tàiyang'))],
              construye=('太阳', 'tàiyang', '弟')),
            L('u03l04', 'Palabras con b, p, d, t', 'Words with b, p, d, t',
              [W('(北:b)京', 'Běijīng', 'Beijing (ciudad)', 'Beijing (city)'), W('(电:d)话', 'diànhuà', 'teléfono', 'telephone', '260e'), W('(拼:p)音', 'pīnyīn', 'pinyin', 'pinyin')],
              ('(拼:p)音', 'pīnyīn',
               '拼音 es el nombre de este sistema de escritura del sonido: pīnyīn. Repasa: b y d sin soplo, p y t con soplo. Pon cada sílaba con su tono.',
               '拼音 is the name of this sound-writing system: pīnyīn. Review: b and d with no puff, p and t with a puff. Give each syllable its tone.'),
              foco='d', par=(('(电:d)话', 'diànhuà'), ('拼音', 'pīnyīn')), oye=(('电话', 'diànhuà'), ('电视', 'diànshì')),
              extras=[sig('电视', 'diànshì', ('televisión', 'television'), ('teléfono', 'telephone')), toca('p', ('(拼:p)音', 'pīnyīn'), ('北京', 'Běijīng'))],
              construye=('北京', 'Běijīng', '拼')),
        ],
    },
    # ── u04 ──────────────────────────────────────────────────────────────────
    {
        'id': 'u04', 'titulo': b('Z4 · Iniciales g, k, h, z, c, s', 'Z4 · Initials g, k, h, z, c, s'),
        'objetivo': b('Leer g, k, h, z, c, s: g y z sin soplo, k y c con soplo, h suave, y saber que la «i» de zi, ci, si no es una «i».',
                      'Read g, k, h, z, c, s: g and z with no puff, k and c with a puff, a light h, and know that the “i” in zi, ci, si is not an “ee.”'),
        'lecciones': [
            L('u04l01', 'g y k: sin soplo y con soplo', 'g and k: no puff and puff',
              [W('(狗:g)', 'gǒu', 'perro', 'dog', '1f436'), W('(哥:g)哥', 'gēge', 'hermano mayor', 'older brother', '1f468'), W('(可:k)乐', 'kělè', 'cola (refresco)', 'cola', '1f964')],
              ('(可:k)乐', 'kělè',
               'g suena como la «c» de «casa», sin soplo, y no como la «g» sonora española: gǒu, gēge. k es lo mismo con un soplo fuerte de aire: kělè. Es el mismo contraste que b/p y d/t.',
               'g sounds like the k in “sky,” with no puff, not like the voiced English g: gǒu, gēge. k is the same sound with a strong puff of air: kělè. It is the same contrast as b/p and d/t.'),
              foco='k', par=(('(可:k)乐', 'kělè'), ('(狗:g)', 'gǒu')), oye=(('课', 'kè'), ('个', 'gè')), inv=True,
              extras=[sig('课', 'kè', ('clase; lección', 'class; lesson'), ('perro', 'dog')),
                      sig('个', 'gè', ('clasificador comodín (como en 一 个)', 'all-purpose classifier (as in 一 个)'), ('clase', 'class')),
                      toca('g', ('(哥:g)哥', 'gēge'), ('可乐', 'kělè'))],
              construye=('哥哥', 'gēge', '可')),
            L('u04l02', 'h: una «j» suave', 'h: a soft “j”',
              [W('(好:h)', 'hǎo', 'bueno; bien', 'good; well', '1f44d'), W('(喝:h)', 'hē', 'beber', 'to drink'), W('(花:h)', 'huā', 'flor', 'flower', '1f338')],
              ('(好:h)', 'hǎo',
               'h suena como la «j» española suave, más ligera: hǎo, huā. A diferencia del español, la h del pinyin sí suena. En 喝 hē, la e se dice como una «o» con los labios estirados.',
               'h sounds like a light, raspy “h,” closer to Spanish j or German ch in “Bach”: hǎo, huā. Unlike Spanish, the h of pinyin is pronounced. In 喝 hē, the e is said like “uh” from the back of the mouth.'),
              foco='h', par=(('(好:h)', 'hǎo'), ('(狗:g)', 'gǒu')), oye=(('喝', 'hē'), ('哥', 'gē')), inv=True,
              extras=[sig('好', 'hǎo', ('bueno; bien', 'good; well'), ('malo', 'bad')),
                      sig('好喝', 'hǎohē', ('rico (de beber)', 'tasty (to drink)'), ('muy caliente', 'very hot'))],
              construye=('好喝', 'hǎohē', '花')),
            L('u04l03', 'z, c, s', 'z, c, s',
              [W('(做:z)', 'zuò', 'hacer', 'to do; to make'), W('(菜:c)', 'cài', 'comida; plato; verdura', 'dish; vegetable', '1f957'), W('(三:s)', 'sān', 'tres', 'three')],
              ('(菜:c)', 'cài',
               'z es una «ts» sin soplo (casi «ds»): zuò. c es una «ts» con soplo fuerte: cài. s es la «s» española: sān. La pareja z/c funciona como b/p: sin soplo frente a con soplo.',
               'z is like “ds” in “kids,” with no puff: zuò. c is like “ts” in “cats,” with a strong puff: cài. s is the s in “see”: sān. The z/c pair works like b/p: no puff versus puff.'),
              foco='c', par=(('(菜:c)', 'cài'), ('(做:z)', 'zuò')), oye=(('错', 'cuò'), ('做', 'zuò')), inv=True,
              extras=[sig('错', 'cuò', ('equivocado; mal', 'wrong'), ('hacer', 'to do')), toca('z', ('(做:z)', 'zuò'), ('三', 'sān')), toca('s', ('(三:s)', 'sān'), ('菜', 'cài'))]),
            L('u04l04', 'La «i» de zi, ci, si', 'The “i” in zi, ci, si',
              [W('(字:ih)', 'zì', 'carácter (escrito)', 'character (written)'), W('(词:ih)', 'cí', 'palabra', 'word'), W('(四:ih)', 'sì', 'cuatro', 'four')],
              ('(字:ih)', 'zì',
               'En zi, ci y si la «i» no es una «i»: es un zumbido de la misma consonante. Alarga la z: «zzz». Lo mismo ocurre con zhi, chi, shi y ri.',
               'In zi, ci and si the “i” is not “ee”: it is a buzz of the same consonant. Stretch the z: “zzz.” The same happens in zhi, chi, shi and ri.'),
              foco='ih', par=(('(字:ih)', 'zì'), ('三', 'sān')), oye=(('四', 'sì'), ('三', 'sān')),
              extras=[sig('词', 'cí', ('palabra', 'word'), ('carácter', 'character')),
                      sig('汉字', 'hànzì', ('caracteres chinos', 'Chinese characters'), ('palabra', 'word')),
                      toca('ih', ('(词:ih)', 'cí'), ('三', 'sān'))],
              construye=('汉字', 'hànzì', '词')),
        ],
    },
    # ── u05 ──────────────────────────────────────────────────────────────────
    {
        'id': 'u05', 'titulo': b('Z5 · Iniciales j, q, x y zh, ch, sh, r', 'Z5 · Initials j, q, x and zh, ch, sh, r'),
        'objetivo': b('Leer j, q, x (lengua plana, solo ante i y ü) y las retroflejas zh, ch, sh, r (lengua curvada hacia atrás).',
                      'Read j, q, x (flat tongue, only before i and ü) and the retroflexes zh, ch, sh, r (tongue curled back).'),
        'lecciones': [
            L('u05l01', 'j, q, x: lengua plana', 'j, q, x: flat tongue',
              [W('(鸡:j)', 'jī', 'pollo; gallina', 'chicken', '1f414'), W('(球:q)', 'qiú', 'pelota; balón', 'ball', '26bd'), W('(小:x)', 'xiǎo', 'pequeño', 'small')],
              ('(鸡:j)', 'jī',
               'j, q y x van solo ante i y ü. La lengua queda plana detrás de los dientes de abajo y los labios en sonrisa. j suena como una «ch» suave y sin soplo (no es la «j» española); q es lo mismo con soplo, más suave que la «ch» española; x es una «s» suave que roza «sh» (no es la «x» española).',
               'j, q and x only go before i and ü. The tongue is flat behind the lower teeth and the lips are spread. j is like “j” in “jeep,” but unvoiced and tenser; q is like “ch” in “cheese” with a puff; x is like “sh” in “she,” but with the tongue flat and the lips spread.'),
              foco='q', par=(('(球:q)', 'qiú'), ('(鸡:j)', 'jī')), oye=(('七', 'qī'), ('鸡', 'jī')),
              extras=[sig('七', 'qī', ('siete', 'seven'), ('pollo', 'chicken')), toca('x', ('(小:x)', 'xiǎo'), ('鸡', 'jī')),
                      sig('小鸡', 'xiǎojī', ('pollito', 'chick'), ('gallo', 'rooster'))],
              construye=('小鸡', 'xiǎojī', '球')),
            L('u05l02', 'j, q, x en palabras de uso diario', 'j, q, x in everyday words',
              [W('(请:q)', 'qǐng', 'por favor; invitar', 'please; to invite'), W('(谢:x)谢', 'xièxie', 'gracias', 'thank you', '1f64f'), W('再(见:j)', 'zàijiàn', 'adiós', 'goodbye', '1f44b')],
              ('(谢:x)谢', 'xièxie',
               'Ya puedes leer palabras muy usadas: 请 qǐng, 谢谢 xièxie, 再见 zàijiàn. Si dices la x como la «x» española (como «ks»), suena mal: sonríe y deja la lengua plana, con un roce suave.',
               'You can now read very common words: 请 qǐng, 谢谢 xièxie, 再见 zàijiàn. If you say x like the English “x” (as “ks”), it sounds wrong: smile and keep the tongue flat, with a soft friction.'),
              foco='x', par=(('(谢:x)谢', 'xièxie'), ('再见', 'zàijiàn')), oye=(('西', 'xī'), ('七', 'qī')),
              extras=[sig('西', 'xī', ('oeste', 'west'), ('siete', 'seven')), toca('q', ('(请:q)', 'qǐng'), ('谢谢', 'xièxie'))],
              construye=('谢谢', 'xièxie', '请')),
            L('u05l03', 'zh, ch, sh: lengua hacia atrás', 'zh, ch, sh: tongue back',
              [W('(猪:zh)', 'zhū', 'cerdo', 'pig', '1f437'), W('(吃:ch)', 'chī', 'comer', 'to eat', '1f37d'), W('(山:sh)', 'shān', 'montaña', 'mountain', '26f0')],
              ('(山:sh)', 'shān',
               'En zh, ch, sh y r (las retroflejas) la punta de la lengua se curva hacia atrás, hacia el paladar. zh es como una «ch» sin soplo, con la lengua atrás; ch es lo mismo con soplo; sh es la «sh» de «she» con la lengua atrás. Contrasta: sān 三 (tres) y shān 山 (montaña).',
               'In zh, ch, sh and r (the retroflexes) the tongue tip curls back toward the palate. zh is like “j” in “jam,” unvoiced, with the tongue back; ch is like “ch” in “church,” with a puff; sh is like “sh” in “she,” tongue back. Contrast: sān 三 (three) and shān 山 (mountain).'),
              foco='sh', par=(('(山:sh)', 'shān'), ('(猪:zh)', 'zhū')), oye=(('山', 'shān'), ('三', 'sān')),
              extras=[sig('三', 'sān', ('tres', 'three'), ('montaña', 'mountain')), toca('ch', ('(吃:ch)', 'chī'), ('三', 'sān')),
                      oye(('吃', 'chī'), ('七', 'qī'), inv=True)],
              construye=('吃饭', 'chīfàn', '山')),
            L('u05l04', 'r y repaso de las tres familias', 'r and a review of the three families',
              [W('(人:r)', 'rén', 'persona', 'person', '1f465'), W('(热:r)', 'rè', 'caliente; calor', 'hot'), W('(肉:r)', 'ròu', 'carne', 'meat', '1f357')],
              ('(人:r)', 'rén',
               'r es como la «r» inglesa de «red», con un zumbido: está entre una «sh» sonora y una «r». Nunca es la «r» española de «pero» ni la «rr». Repasa las tres familias: z/c/s (lengua adelante), j/q/x (lengua plana) y zh/ch/sh/r (lengua atrás).',
               'r is like English “r” in “red,” with a buzz: it sits between a voiced “sh” and an “r.” It is never a tapped or rolled r. Review the three families: z/c/s (tongue forward), j/q/x (tongue flat) and zh/ch/sh/r (tongue back).'),
              foco='r', par=(('(人:r)', 'rén'), ('(山:sh)', 'shān')), oye=(('人', 'rén'), ('十', 'shí')),
              extras=[sig('十', 'shí', ('diez', 'ten'), ('cuatro', 'four')), oye(('十', 'shí'), ('四', 'sì'), inv=True),
                      toca('zh', ('(猪:zh)', 'zhū'), ('(字:ih)', 'zì')), sig('热', 'rè', ('caliente; calor', 'hot'), ('frío', 'cold'))]),
        ],
    },
    # ── u06 ──────────────────────────────────────────────────────────────────
    {
        'id': 'u06', 'titulo': b('Z6 · Finales simples y compuestas, y er', 'Z6 · Simple and compound finals, and er'),
        'objetivo': b('Leer las finales simples (a, e, i, u), las compuestas (ai, ei, ao, ou, iu, ui, ian, ie) y la vocal er.',
                      'Read the simple finals (a, e, i, u), the compound ones (ai, ei, ao, ou, iu, ui, ian, ie) and the vowel er.'),
        'lecciones': [
            L('u06l01', 'Finales simples: a, e, i, u', 'Simple finals: a, e, i, u',
              [W('(大:a)', 'dà', 'grande', 'big', '1f418'), W('(喝:e)', 'hē', 'beber', 'to drink'), W('(米:i)', 'mǐ', 'arroz; metro', 'rice; meter'), W('(五:u)', 'wǔ', 'cinco', 'five')],
              ('(喝:e)', 'hē',
               'Las finales simples son a, o, e, i, u y ü. a, i y u se parecen al español. La e suena como una «o» con los labios estirados: hē, de. La o aparece sobre todo tras b, p, m, f (bō, pō) y dentro de uo (wǒ, duō). La ü la verás en la unidad siguiente.',
               'The simple finals are a, o, e, i, u and ü. a, i and u are close to English “ah,” “ee” and “oo.” The e is an unrounded “uh” from the back of the mouth: hē, de. The o shows up mostly after b, p, m, f (bō, pō) and inside uo (wǒ, duō). You will meet ü in the next unit.'),
              foco='e', par=(('(喝:e)', 'hē'), ('(大:a)', 'dà')), oye=(('喝', 'hē'), ('大', 'dà')), inv=True,
              extras=[toca('i', ('(米:i)', 'mǐ'), ('五', 'wǔ')), sig('五', 'wǔ', ('cinco', 'five'), ('seis', 'six')),
                      sig('我', 'wǒ', ('yo', 'I; me'), ('tú', 'you'))]),
            L('u06l02', 'ai, ei, ao, ou', 'ai, ei, ao, ou',
              [W('(爱:ai)', 'ài', 'amar; amor', 'to love; love', '2764'), W('(飞:ei)机', 'fēijī', 'avión', 'airplane', '2708'), W('(猫:ao)', 'māo', 'gato', 'cat', '1f431'), W('(手:ou)', 'shǒu', 'mano', 'hand', '270b')],
              ('(猫:ao)', 'māo',
               'ai, ei, ao y ou son finales compuestas: dos vocales seguidas que se deslizan de una a otra dentro de una sola sílaba: ài, fēi, māo, shǒu. La primera vocal es la más fuerte.',
               'ai, ei, ao and ou are compound finals: two vowels in a row that glide from one to the other within a single syllable: ài, fēi, māo, shǒu. The first vowel is the strongest.'),
              foco='ao', par=(('(猫:ao)', 'māo'), ('(手:ou)', 'shǒu')), oye=(('猫', 'māo'), ('手', 'shǒu')),
              extras=[toca('ai', ('(爱:ai)', 'ài'), ('飞机', 'fēijī')), sig('猫', 'māo', ('gato', 'cat'), ('perro', 'dog')),
                      sig('飞机', 'fēijī', ('avión', 'airplane'), ('tren', 'train'))],
              construye=('飞机', 'fēijī', '猫')),
            L('u06l03', 'iu, ui, ian, ie', 'iu, ui, ian, ie',
              [W('(九:iu)', 'jiǔ', 'nueve', 'nine'), W('(贵:ui)', 'guì', 'caro; costoso', 'expensive'), W('(天:ian)', 'tiān', 'cielo; día', 'sky; day', '2601'), W('(谢:ie)谢', 'xièxie', 'gracias', 'thank you', '1f64f')],
              ('(天:ian)', 'tiān',
               'Algunas finales no suenan como se escriben: ian ≈ «ien» (tiān ≈ «tien»); iu = «iou» (jiǔ ≈ «jiou»); ui = «uei» (guì ≈ «guei»); ie ≈ «ié» (xiè). La marca de tono va sobre la última vocal en iu y ui.',
               'Some finals do not sound the way they are written: ian ≈ “yen” (tiān ≈ “tyen”); iu = “iou” (jiǔ ≈ “jyoh”); ui = “uei” (guì ≈ “gway”); ie ≈ “ye” (xiè). In iu and ui the tone mark goes on the last vowel.'),
              foco='ui', par=(('(贵:ui)', 'guì'), ('(九:iu)', 'jiǔ')), oye=(('九', 'jiǔ'), ('贵', 'guì')),
              extras=[toca('ian', ('(天:ian)', 'tiān'), ('九', 'jiǔ')), sig('贵', 'guì', ('caro', 'expensive'), ('barato', 'cheap')),
                      sig('九', 'jiǔ', ('nueve', 'nine'), ('seis', 'six'))]),
            L('u06l04', 'La vocal er', 'The vowel er',
              [W('(二:er)', 'èr', 'dos', 'two'), W('(儿:er)子', 'érzi', 'hijo', 'son', '1f466'), W('(耳:er)朵', 'ěrduo', 'oreja', 'ear', '1f442')],
              ('(二:er)', 'èr',
               'er es una vocal con la lengua curvada hacia atrás, como la «er» de «her» en inglés americano: èr, érzi, ěrduo. En el habla del norte a veces se añade una «r» a otras palabras (erhua): 花儿 huār. Solo hay que reconocerla; este curso escribe 花.',
               'er is a vowel with the tongue curled back, like the “er” in American “her”: èr, érzi, ěrduo. In northern speech an “r” is sometimes added to other words (erhua): 花儿 huār. You only need to recognize it; this course writes 花.'),
              foco='er', par=(('(二:er)', 'èr'), ('四', 'sì')), oye=(('二', 'èr'), ('三', 'sān')),
              extras=[significado('花儿', 'huār', '¿Qué hace 儿 aquí?', 'What does 儿 do here?',
                                  [('Añade una «r» al final de la sílaba; solo hace falta reconocerla', 'It adds an “r” sound at the end of the syllable; you only need to recognize it'),
                                   ('Es una sílaba más, con tono propio', 'It is an extra syllable with its own tone')]),
                      sig('二', 'èr', ('dos', 'two'), ('tres', 'three')), toca('er', ('(耳:er)朵', 'ěrduo'), ('猫', 'māo'))],
              construye=('儿子', 'érzi', '二')),
        ],
    },
    # ── u07 ──────────────────────────────────────────────────────────────────
    {
        'id': 'u07', 'titulo': b('Z7 · -n y -ng, ü y reglas del pinyin', 'Z7 · -n and -ng, ü and pinyin spelling rules'),
        'objetivo': b('Distinguir -n de -ng, decir la ü (nǚ, lǜ) y aplicar las reglas de escritura del pinyin: u por ü tras j, q, x, y; y/w; apóstrofo; marca de tono.',
                      'Tell -n from -ng, say ü (nǚ, lǜ) and apply the pinyin spelling rules: u for ü after j, q, x, y; y/w; the apostrophe; tone-mark placement.'),
        'lecciones': [
            L('u07l01', 'Final -n', 'Final -n',
              [W('(门:n)', 'mén', 'puerta', 'door', '1f6aa'), W('(新:n)', 'xīn', 'nuevo', 'new'), W('吃(饭:n)', 'chīfàn', 'comer; comida', 'to eat; meal', '1f37d')],
              ('(门:n)', 'mén',
               'En -n la lengua toca las encías, como la «n» de «pan»: mén, xīn, fàn. Las finales con -n son an, en, in, un y ün.',
               'In -n the tongue touches the gum ridge, like the “n” in “pan”: mén, xīn, fàn. The finals with -n are an, en, in, un and ün.'),
              foco='n', par=(('(新:n)', 'xīn'), ('西', 'xī')), oye=(('新', 'xīn'), ('西', 'xī')),
              extras=[sig('新', 'xīn', ('nuevo', 'new'), ('viejo', 'old')), toca('n', ('(门:n)', 'mén'), ('猫', 'māo'))],
              construye=('吃饭', 'chīfàn', '门')),
            L('u07l02', 'Final -ng', 'Final -ng',
              [W('(星:ng)', 'xīng', 'estrella', 'star', '2b50'), W('(中:ng)国', 'Zhōngguó', 'China', 'China', '1f30d'), W('(放:ng)', 'fàng', 'poner; colocar', 'to put; to place')],
              ('(星:ng)', 'xīng',
               '-ng suena como la «n» de «banco» o «tengo», sin una g aparte: xīng, zhōng, fàng. No digas «xin-g»: el sonido termina en la nariz. Pares para oír: xīn 新 / xīng 星 y fàn 饭 / fàng 放. ong ≈ «ung» (dōng ≈ «dung»).',
               '-ng sounds like the “ng” in “sing,” with no separate g: xīng, zhōng, fàng. Do not say “xin-g”: the sound ends in the nose. Pairs to hear: xīn 新 / xīng 星 and fàn 饭 / fàng 放. ong ≈ “ung” (dōng ≈ “dung”).'),
              foco='ng', par=(('(星:ng)', 'xīng'), ('新', 'xīn')), oye=(('星', 'xīng'), ('新', 'xīn')), inv=True,
              extras=[oye(('放', 'fàng'), ('饭', 'fàn')), sig('星', 'xīng', ('estrella', 'star'), ('nuevo', 'new')),
                      sig('红', 'hóng', ('rojo', 'red'), ('verde', 'green')), toca('ng', ('(放:ng)', 'fàng'), ('饭', 'fàn'))],
              construye=('中国', 'Zhōngguó', '星')),
            L('u07l03', 'La ü', 'The ü',
              [W('(女:yu)', 'nǚ', 'mujer', 'woman', '1f469'), W('(绿:yu)', 'lǜ', 'verde', 'green', '1f96c'), W('(鱼:yu)', 'yú', 'pez; pescado', 'fish', '1f41f')],
              ('(女:yu)', 'nǚ',
               'ü se dice «i» con los labios en posición de «u», como la «u» del francés: nǚ, lǜ. Tras n y l se escribe «ü», con los puntos, para no confundirla con u: lǜ 绿 (verde) y lù 路 (camino) son palabras distintas.',
               'ü is said “ee” with rounded lips, like the French u: nǚ, lǜ. After n and l it is written “ü,” with the dots, so it is not confused with u: lǜ 绿 (green) and lù 路 (road) are different words.'),
              foco='yu', par=(('(绿:yu)', 'lǜ'), ('路', 'lù')), oye=(('绿', 'lǜ'), ('路', 'lù')),
              extras=[sig('路', 'lù', ('camino; calle', 'road; street'), ('verde', 'green')), toca('yu', ('(女:yu)', 'nǚ'), ('牛', 'niú')),
                      sig('女', 'nǚ', ('mujer', 'woman'), ('hombre', 'man'))]),
            L('u07l04', 'u que suena ü: qù, xué, yuè', 'u that sounds like ü: qù, xué, yuè',
              [W('(去:yu)', 'qù', 'ir', 'to go'), W('(学:yu)', 'xué', 'estudiar; aprender', 'to study; to learn'), W('(月:yu)', 'yuè', 'luna; mes', 'moon; month', '1f319')],
              ('(去:yu)', 'qù',
               'Tras j, q, x e y el pinyin escribe «u», pero suena ü: qù, xué, yuè. j, q y x solo van con i y ü, así que no hace falta poner los puntos. Nunca se escribe «v» por la ü.',
               'After j, q, x and y, pinyin writes “u” but it sounds ü: qù, xué, yuè. j, q and x only go with i and ü, so the dots are not needed. A “v” is never written for ü.'),
              foco='yu', par=(('(月:yu)', 'yuè'), ('(球:q)', 'qiú')), oye=(('去', 'qù'), ('七', 'qī')),
              extras=[sig('去', 'qù', ('ir', 'to go'), ('venir', 'to come')),
                      lee('学', None, 'estudiar; aprender', 'to study; to learn', '¿Cómo se escribe en pinyin?', 'How is it written in pinyin?', ['xué', 'xüé']),
                      lee('女', None, 'mujer', 'woman', '¿Cómo se escribe en pinyin?', 'How is it written in pinyin?', ['nǚ', 'nǔ']),
                      toca('yu', ('(学:yu)', 'xué'), ('小', 'xiǎo'))],
              construye=('学生', 'xuésheng', '月')),
            L('u07l05', 'y, w, apóstrofo y marca de tono', 'y, w, the apostrophe and tone marks',
              [W('西安', "Xī'ān", 'Xi’an (ciudad)', 'Xi’an (city)'), W('十二', "shí'èr", 'doce', 'twelve'), W('女儿', "nǚ'ér", 'hija', 'daughter', '1f467')],
              ('西安', "Xī'ān",
               'Sin consonante inicial, i → yi, u → wu y ü → yu: yī 一, wǔ 五, yú 鱼. Si una sílaba empieza con vocal y va tras otra, un apóstrofo las separa: Xī’ān, shí’èr, nǚ’ér. La marca de tono va sobre la «a» si la hay; si no, sobre la «e» o la «o»; en iu y ui, sobre la última vocal: liù, guì.',
               'With no initial consonant, i → yi, u → wu and ü → yu: yī 一, wǔ 五, yú 鱼. If a syllable starts with a vowel and follows another one, an apostrophe separates them: Xī’ān, shí’èr, nǚ’ér. The tone mark goes on the a if there is one; otherwise on the e or the o; in iu and ui, on the last vowel: liù, guì.'),
              oye=(('十二', "shí'èr"), ('十', 'shí')),
              extras=[lee('六', None, 'seis', 'six', '¿Dónde va la marca en liu?', 'Where does the mark go in liu?', ['liù', 'lìu']),
                      lee('贵', None, 'caro', 'expensive', '¿Dónde va la marca en gui?', 'Where does the mark go in gui?', ['guì', 'gùi']),
                      lee('好', None, 'bueno; bien', 'good; well', '¿Dónde va la marca en hao?', 'Where does the mark go in hao?', ['hǎo', 'haǒ']),
                      lee('五', None, 'cinco', 'five', '¿Cómo se escribe u sin consonante inicial?', 'How is u written with no initial consonant?', ['wǔ', 'ǔ']),
                      lee('十二', None, 'doce', 'twelve', '¿Cómo se escribe?', 'How is it written?', ["shí'èr", 'shíèr'])],
              construye=('十二', "shí'èr", '五')),
        ],
    },
    # ── u08 ──────────────────────────────────────────────────────────────────
    {
        'id': 'u08', 'titulo': b('Z8 · Qué es un carácter: radicales y trazos', 'Z8 · What a character is: radicals and strokes'),
        'objetivo': b('Entender que cada carácter escribe una sílaba con significado, reconocer radicales frecuentes y contar los trazos básicos.',
                      'Understand that each character writes a meaningful syllable, recognize common radicals and count the basic strokes.'),
        'lecciones': [
            L('u08l01', 'Un carácter, una sílaba', 'One character, one syllable',
              [W('日', 'rì', 'sol; día', 'sun; day', '2600'), W('月', 'yuè', 'luna; mes', 'moon; month', '1f319'), W('山', 'shān', 'montaña', 'mountain', '26f0'), W('水', 'shuǐ', 'agua', 'water', '1f4a7')],
              ('日', 'rì',
               'Un carácter (字 zì) escribe una sílaba y casi siempre tiene un significado propio. Muchos nacieron como dibujos: 日 era un sol, 月 una luna, 山 una montaña, 水 una corriente de agua. Una palabra puede tener uno o más caracteres: 山 tiene uno; 中国 tiene dos (中, «centro», y 国, «país»). Este curso usa caracteres simplificados (简体字).',
               'A character (字 zì) writes one syllable and almost always has a meaning of its own. Many began as pictures: 日 was a sun, 月 a moon, 山 a mountain, 水 a stream of water. A word can have one or more characters: 山 has one; 中国 has two (中, “center,” and 国, “country”). This course uses simplified characters (简体字).'),
              oye=(('山', 'shān'), ('水', 'shuǐ')),
              extras=[sig('山', 'shān', ('montaña', 'mountain'), ('agua', 'water')),
                      significado('中国', 'Zhōngguó', '¿Cuántos caracteres y cuántas sílabas tiene?', 'How many characters and syllables does it have?',
                                  [('Dos caracteres y dos sílabas', 'Two characters and two syllables'), ('Un carácter y dos sílabas', 'One character and two syllables')]),
                      sig('月', 'yuè', ('luna; mes', 'moon; month'), ('sol; día', 'sun; day'))],
              construye=('中国', 'Zhōngguó', '日')),
            L('u08l02', 'Radical y pista de sonido', 'Radical and sound clue',
              [W('妈', 'mā', 'mamá', 'mom', '1f469'), W('吗', 'ma', 'partícula de pregunta', 'question particle'), W('马', 'mǎ', 'caballo', 'horse', '1f434'), W('骂', 'mà', 'regañar; insultar', 'to scold')],
              ('妈', 'mā',
               'Muchos caracteres tienen dos partes: una pista de significado (el radical) y una pista de sonido. En 妈, 女 (mujer) da la idea y 马 (mǎ) da el sonido: mā. En 吗, 口 (boca) indica algo hablado y 马 vuelve a dar el sonido. La pista de sonido es aproximada: el tono puede cambiar.',
               'Many characters have two parts: a meaning clue (the radical) and a sound clue. In 妈, 女 (woman) gives the idea and 马 (mǎ) gives the sound: mā. In 吗, 口 (mouth) points to something spoken and 马 again gives the sound. The sound clue is approximate: the tone may change.'),
              oye=(('骂', 'mà'), ('妈', 'mā')),
              extras=[significado('女', 'nǚ', '¿Qué idea aporta 女 a 妈?', 'What idea does 女 add to 妈?', [('Mujer', 'Woman'), ('Agua', 'Water'), ('Fuego', 'Fire')]),
                      significado('口', 'kǒu', '¿Qué idea aporta 口 a 吗?', 'What idea does 口 add to 吗?', [('Boca', 'Mouth'), ('Mano', 'Hand')]),
                      sig('骂', 'mà', ('regañar; insultar', 'to scold'), ('comprar', 'to buy'))],
              construye=('妈妈', 'māma', '马')),
            L('u08l03', 'Radicales frecuentes', 'Common radicals',
              [W('河', 'hé', 'río', 'river', '1f30a'), W('说', 'shuō', 'decir; hablar', 'to say; to speak', '1f5e3'), W('吃', 'chī', 'comer', 'to eat', '1f37d'), W('你', 'nǐ', 'tú', 'you')],
              ('河', 'hé',
               'Algunos radicales muy útiles: 氵 (agua) en 河 hé (río) y 海 hǎi (mar); 讠 (palabra) en 说 shuō (decir) y 请 qǐng (por favor); 口 (boca) en 吃 chī (comer) y 喝 hē (beber); 亻 (persona) en 你 nǐ (tú) y 他 tā (él). Fíjate en el radical: te da una pista del significado.',
               'Some very useful radicals: 氵 (water) in 河 hé (river) and 海 hǎi (sea); 讠 (speech) in 说 shuō (to say) and 请 qǐng (please); 口 (mouth) in 吃 chī (to eat) and 喝 hē (to drink); 亻 (person) in 你 nǐ (you) and 他 tā (he). Look at the radical: it hints at the meaning.'),
              oye=(('说', 'shuō'), ('河', 'hé')),
              extras=[significado('河', 'hé', '¿Qué radical comparten 河 y 海 (mar)?', 'Which radical do 河 and 海 (sea) share?',
                                  [('El de agua (氵)', 'The water radical (氵)'), ('El de fuego', 'The fire radical'), ('El de boca (口)', 'The mouth radical (口)')]),
                      significado('说', 'shuō', '¿Qué radical comparten 说 y 请?', 'Which radical do 说 and 请 share?',
                                  [('El de palabra (讠)', 'The speech radical (讠)'), ('El de agua', 'The water radical')]),
                      sig('吃', 'chī', ('comer', 'to eat'), ('beber', 'to drink'))]),
            L('u08l04', 'Los trazos', 'The strokes',
              [W('一', 'yī', 'uno', 'one'), W('十', 'shí', 'diez', 'ten'), W('人', 'rén', 'persona', 'person', '1f465'), W('大', 'dà', 'grande', 'big', '1f418')],
              ('十', 'shí',
               'Los trazos son las líneas que forman un carácter. Los básicos: 横 héng (horizontal), 竖 shù (vertical), 撇 piě (diagonal hacia la izquierda), 捺 nà (diagonal hacia la derecha) y 点 diǎn (punto). También hay 提 tí, 折 zhé y 钩 gōu. 一 tiene un trazo; 十 tiene dos (横, 竖); 人 tiene dos (撇, 捺); 大 tiene tres (横, 撇, 捺).',
               'Strokes are the lines that make up a character. The basic ones: 横 héng (horizontal), 竖 shù (vertical), 撇 piě (falling left), 捺 nà (falling right) and 点 diǎn (dot). There are also 提 tí, 折 zhé and 钩 gōu. 一 has one stroke; 十 has two (横, 竖); 人 has two (撇, 捺); 大 has three (横, 撇, 捺).'),
              extras=[lee('大', 'dà', 'grande', 'big', '¿Cuántos trazos tiene?', 'How many strokes does it have?', [('三', 'sān'), ('二', 'èr')]),
                      lee('人', 'rén', 'persona', 'person', '¿Cuántos trazos tiene?', 'How many strokes does it have?', [('二', 'èr'), ('三', 'sān')]),
                      lee('十', 'shí', 'diez', 'ten', '¿Cuántos trazos tiene?', 'How many strokes does it have?', [('三', 'sān'), ('二', 'èr')], 1),
                      lee('一', 'yī', 'uno', 'one', '¿Qué trazo forma 一?', 'Which stroke makes up 一?', [('横', 'héng'), ('竖', 'shù')])]),
        ],
    },
    # ── u09 ──────────────────────────────────────────────────────────────────
    {
        'id': 'u09', 'titulo': b('Z9 · Orden de los trazos y primeras palabras', 'Z9 · Stroke order and first words'),
        'objetivo': b('Escribir con el orden básico (arriba a abajo, izquierda a derecha, horizontal antes de vertical, cierre al final) y leer las primeras palabras reales.',
                      'Write with the basic order (top to bottom, left to right, horizontal before vertical, closing last) and read your first real words.'),
        'lecciones': [
            L('u09l01', 'De arriba abajo', 'Top to bottom',
              [W('二', 'èr', 'dos', 'two'), W('三', 'sān', 'tres', 'three'), W('工', 'gōng', 'trabajo; obra', 'work')],
              ('三', 'sān',
               'Regla general: los trazos se escriben de arriba abajo y de izquierda a derecha. En 三 se escribe primero la raya de arriba, luego la del medio y al final la de abajo. En 二, primero la de arriba y luego la de abajo. En 工 (tres trazos): raya de arriba, trazo vertical y raya de abajo.',
               'General rule: strokes are written from top to bottom and from left to right. In 三 you write the top line first, then the middle one, and the bottom one last. In 二, the top line and then the bottom one. In 工 (three strokes): top line, vertical stroke and bottom line.'),
              oye=(('二', 'èr'), ('三', 'sān')),
              extras=[significado('三', 'sān', '¿Qué raya de 三 se escribe primero?', 'Which line of 三 is written first?',
                                  [('La de arriba', 'The top one'), ('La de abajo', 'The bottom one')]),
                      lee('工', 'gōng', 'trabajo; obra', 'work', '¿Cuántos trazos tiene?', 'How many strokes does it have?', [('三', 'sān'), ('四', 'sì')]),
                      sig('工', 'gōng', ('trabajo; obra', 'work'), ('tierra', 'earth'))]),
            L('u09l02', 'De izquierda a derecha', 'Left to right',
              [W('林', 'lín', 'bosque', 'forest', '1f332'), W('明', 'míng', 'claro; brillante', 'bright'), W('好', 'hǎo', 'bueno; bien', 'good; well', '1f44d')],
              ('林', 'lín',
               'Se escribe de izquierda a derecha: en 林 se escribe primero el 木 de la izquierda y luego el de la derecha. En 明, primero 日 y luego 月. En 好, primero 女 y luego 子.',
               'Strokes go from left to right: in 林 you write the 木 on the left first, then the one on the right. In 明, first 日 and then 月. In 好, first 女 and then 子.'),
              oye=(('林', 'lín'), ('明', 'míng')), inv=True,
              extras=[significado('明', 'míng', '¿Qué parte de 明 se escribe primero?', 'Which part of 明 is written first?',
                                  [('日, la de la izquierda', '日, the one on the left'), ('月, la de la derecha', '月, the one on the right')]),
                      sig('林', 'lín', ('bosque', 'forest'), ('río', 'river')),
                      significado('好', 'hǎo', '¿Qué parte de 好 se escribe primero?', 'Which part of 好 is written first?',
                                  [('女, la de la izquierda', '女, the one on the left'), ('子, la de la derecha', '子, the one on the right')])]),
            L('u09l03', 'Horizontal antes que vertical', 'Horizontal before vertical',
              [W('十', 'shí', 'diez', 'ten'), W('土', 'tǔ', 'tierra', 'earth; soil'), W('木', 'mù', 'madera; árbol', 'wood; tree', '1f333')],
              ('十', 'shí',
               'Cuando dos trazos se cruzan, la horizontal va antes que la vertical: en 十 se escribe primero 横 y después 竖. En 土: horizontal, vertical y la horizontal de abajo. En 木: 横, 竖 y después 撇 y 捺, de izquierda a derecha.',
               'When two strokes cross, the horizontal goes before the vertical: in 十 you write 横 first and then 竖. In 土: horizontal, vertical and the bottom horizontal. In 木: 横, 竖 and then 撇 and 捺, left to right.'),
              oye=(('土', 'tǔ'), ('木', 'mù')),
              extras=[lee('十', 'shí', 'diez', 'ten', '¿Qué trazo va primero?', 'Which stroke comes first?', [('横', 'héng'), ('竖', 'shù')]),
                      lee('木', 'mù', 'madera; árbol', 'wood; tree', '¿Cuántos trazos tiene?', 'How many strokes does it have?', [('四', 'sì'), ('三', 'sān')]),
                      lee('土', 'tǔ', 'tierra', 'earth; soil', '¿Cuántos trazos tiene?', 'How many strokes does it have?', [('三', 'sān'), ('二', 'èr')])]),
            L('u09l04', 'El cuadro se cierra al final', 'The box closes last',
              [W('口', 'kǒu', 'boca; entrada', 'mouth; opening', '1f444'), W('日', 'rì', 'sol; día', 'sun; day', '2600'), W('国', 'guó', 'país', 'country', '1f30d')],
              ('口', 'kǒu',
               'En los cuadrados se escribe primero el lado izquierdo y el de arriba; después, lo de dentro; el cierre de abajo va al final. 口 se cierra con la raya de abajo; en 日, la raya del medio va antes de ese cierre; en 国, primero el marco, luego lo de dentro y por último se cierra el cuadro.',
               'In boxes you write the left side and the top first; then what is inside; the bottom closing stroke comes last. 口 closes with the bottom line; in 日, the middle line comes before that closing; in 国, first the frame, then what is inside, and finally the box is closed.'),
              oye=(('国', 'guó'), ('口', 'kǒu')),
              extras=[significado('日', 'rì', '¿Qué raya de 日 se escribe al final?', 'Which line of 日 is written last?',
                                  [('La de abajo, que cierra el cuadro', 'The bottom one, which closes the box'), ('La del medio', 'The middle one')]),
                      lee('口', 'kǒu', 'boca; entrada', 'mouth; opening', '¿Cuántos trazos tiene?', 'How many strokes does it have?', [('三', 'sān'), ('四', 'sì')]),
                      lee('日', 'rì', 'sol; día', 'sun; day', '¿Cuántos trazos tiene?', 'How many strokes does it have?', [('四', 'sì'), ('三', 'sān')]),
                      lee('国', 'guó', 'país', 'country', '¿Cuántos trazos tiene?', 'How many strokes does it have?', [('八', 'bā'), ('六', 'liù')])]),
            L('u09l05', 'Tus primeras palabras reales', 'Your first real words',
              [W('你 好', 'ní hǎo', 'hola', 'hello', '1f44b'), W('谢谢', 'xièxie', 'gracias', 'thank you', '1f64f'), W('再见', 'zàijiàn', 'adiós', 'goodbye'), W('对不起', 'duìbuqǐ', 'perdón; lo siento', 'sorry')],
              ('你 好', 'ní hǎo',
               'Ya puedes leer palabras muy usadas: cada carácter lleva su pinyin, su tono y su significado. 你 好 se escribe con dos palabras y el pinyin refleja el cambio de tono: ní hǎo. 谢谢, 再见 y 对不起 son una sola palabra cada una.',
               'You can now read very common words: each character comes with its pinyin, its tone and its meaning. 你 好 is written as two words and the pinyin shows the tone change: ní hǎo. 谢谢, 再见 and 对不起 are one word each.'),
              oye=(('谢谢', 'xièxie'), ('再见', 'zàijiàn')),
              extras=[sig('对不起', 'duìbuqǐ', ('perdón; lo siento', 'sorry'), ('de nada', 'you’re welcome')),
                      sig('再见', 'zàijiàn', ('adiós', 'goodbye'), ('hola', 'hello')),
                      lee('你 好', None, 'hola', 'hello', '¿Cómo se dice en voz alta?', 'How is it said aloud?', ['ní hǎo', 'nǐ hǎo'])],
              construye=('对不起', 'duìbuqǐ', '谢')),
        ],
    },
    # ── u10 · evaluación (sin Lumo) ──────────────────────────────────────────
    {
        'id': 'u10', 'titulo': b('Z10 · Ya puedes empezar', 'Z10 · You can start now'),
        'objetivo': b('Comprobar que oyes y lees el pinyin: tonos, cambios de tono, iniciales, finales, caracteres y primeras palabras.',
                      'Check that you can hear and read pinyin: tones, tone changes, initials, finals, characters and first words.'),
        'lecciones': [
            L('u10l01', 'Tonos y cambios de tono', 'Tones and tone changes',
              [W('妈', 'mā', 'mamá', 'mom'), W('马', 'mǎ', 'caballo', 'horse'), W('买', 'mǎi', 'comprar', 'to buy'), W('卖', 'mài', 'vender', 'to sell')],
              ('买', 'mǎi',
               'Repaso de tonos: mā, má, mǎ, mà; mǎi y mài; sì y sǐ. Y de los cambios: ní hǎo, bú shì, yì bēi.',
               'Tone review: mā, má, mǎ, mà; mǎi and mài; sì and sǐ. And the changes: ní hǎo, bú shì, yì bēi.'),
              oye=(('买', 'mǎi'), ('卖', 'mài')),
              extras=[oye(('马', 'mǎ'), ('妈', 'mā'), inv=True), oye(('四', 'sì'), ('死', 'sǐ')), oye(('问', 'wèn'), ('文', 'wén'), inv=True),
                      tono('马', 'mǎ', 3), tono('卖', 'mài', 4),
                      lee('不 是', None, 'no es', 'is not', '¿Cómo se lee?', 'How is it read?', ['bú shì', 'bù shì']),
                      lee('一 杯', None, 'una taza', 'a cup', '¿Cómo se lee?', 'How is it read?', ['yì bēi', 'yí bēi']),
                      lee('你 好', None, 'hola', 'hello', '¿Cómo se dice en voz alta?', 'How is it said aloud?', ['ní hǎo', 'nǐ hǎo'])],
              construye=('火车', 'huǒchē', '妈')),
            L('u10l02', 'Iniciales', 'Initials',
              [W('山', 'shān', 'montaña', 'mountain'), W('三', 'sān', 'tres', 'three'), W('球', 'qiú', 'pelota; balón', 'ball'), W('鸡', 'jī', 'pollo; gallina', 'chicken')],
              ('山', 'shān',
               'Repaso: sin soplo y con soplo (b/p, d/t, g/k, z/c, j/q, zh/ch) y las tres familias (s, sh, x). Escucha cada inicial antes de decidir.',
               'Review: no puff and puff (b/p, d/t, g/k, z/c, j/q, zh/ch) and the three families (s, sh, x). Listen to each initial before you decide.'),
              foco='sh', par=(('(山:sh)', 'shān'), ('三', 'sān')), oye=(('山', 'shān'), ('三', 'sān')),
              extras=[oye(('怕', 'pà'), ('爸', 'bà')), oye(('课', 'kè'), ('个', 'gè'), inv=True), oye(('七', 'qī'), ('鸡', 'jī')),
                      oye(('吃', 'chī'), ('七', 'qī'), inv=True), oye(('错', 'cuò'), ('做', 'zuò')),
                      toca('c', ('(菜:c)', 'cài'), ('三', 'sān')), toca('zh', ('(猪:zh)', 'zhū'), ('字', 'zì'))],
              construye=('吃饭', 'chīfàn', '七')),
            L('u10l03', 'Finales, ü y ortografía', 'Finals, ü and spelling',
              [W('星', 'xīng', 'estrella', 'star'), W('新', 'xīn', 'nuevo', 'new'), W('绿', 'lǜ', 'verde', 'green'), W('路', 'lù', 'camino; calle', 'road; street')],
              ('星', 'xīng',
               'Repaso: -n frente a -ng, ü frente a u, y las reglas de escritura (qù, xué, liù, guì, shí’èr). Ojo con las sílabas inventadas.',
               'Review: -n versus -ng, ü versus u, and the spelling rules (qù, xué, liù, guì, shí’èr). Watch for made-up syllables.'),
              foco='ng', par=(('(星:ng)', 'xīng'), ('新', 'xīn')), oye=(('饭', 'fàn'), ('放', 'fàng')),
              extras=[oye(('绿', 'lǜ'), ('路', 'lù')), toca('yu', ('(鱼:yu)', 'yú'), ('牛', 'niú')),
                      toca('ui', ('(贵:ui)', 'guì'), ('九', 'jiǔ')),
                      lee('贵', None, 'caro', 'expensive', '¿Dónde va la marca en gui?', 'Where does the mark go in gui?', ['guì', 'gùi']),
                      lee('qü', None, *PSEUDO, *CUAL_INVENTADA, ['qù', 'qü'], 1),
                      lee('fiu', None, *PSEUDO, *CUAL_INVENTADA, ['liù', 'fiu'], 1)],
              construye=('中国', 'Zhōngguó', '星')),
            L('u10l04', 'Caracteres y palabras', 'Characters and words',
              [W('王 老师', 'Wáng lǎoshī', 'profesor Wang; profesora Wang', 'Teacher Wang'), W('张 先生', 'Zhāng xiānsheng', 'señor Zhang', 'Mr. Zhang'), W('刘 女士', 'Liú nǚshì', 'señora Liu', 'Ms. Liu'), W('谢谢', 'xièxie', 'gracias', 'thank you')],
              ('王 老师', 'Wáng lǎoshī',
               'Repaso final: en chino el apellido va primero y el título después: 王 老师 es «profesor Wang» (o «profesora Wang»). Cada carácter tiene su pinyin, su tono y su significado; los trazos y los radicales te ayudan a recordarlo.',
               'Final review: in Chinese the family name comes first and the title after it: 王 老师 is “Teacher Wang.” Every character has its pinyin, its tone and its meaning; strokes and radicals help you remember it.'),
              oye=(('谢谢', 'xièxie'), ('再见', 'zàijiàn')),
              extras=[lee('王 芳', 'Wáng Fāng', 'Wang Fang (nombre de persona)', 'Wang Fang (a person’s name)', '¿Cuál es el apellido?', 'Which one is the family name?', [('王', 'Wáng'), ('芳', 'Fāng')]),
                      lee('十', 'shí', 'diez', 'ten', '¿Cuántos trazos tiene?', 'How many strokes does it have?', [('三', 'sān'), ('二', 'èr')], 1),
                      significado('日', 'rì', '¿Qué raya de 日 se escribe al final?', 'Which line of 日 is written last?',
                                  [('La de abajo, que cierra el cuadro', 'The bottom one, which closes the box'), ('La del medio', 'The middle one')]),
                      significado('妈', 'mā', '¿Qué idea aporta 女 a 妈?', 'What idea does 女 add to 妈?', [('Mujer', 'Woman'), ('Agua', 'Water')]),
                      significado('河', 'hé', '¿Qué radical tiene 河?', 'Which radical does 河 have?', [('El de agua (氵)', 'The water radical (氵)'), ('El de boca (口)', 'The mouth radical (口)')]),
                      sig('对不起', 'duìbuqǐ', ('perdón; lo siento', 'sorry'), ('de nada', 'you’re welcome'))],
              construye=('老师', 'lǎoshī', '王')),
        ],
    },
]


def nivel0_json():
    return {
        'esquema': 'onelingo.nivel0.v1',
        'idioma': 'zh',
        'titulo': b('Nivel 0 · Pinyin, tonos y caracteres', 'Level 0 · Pinyin, tones and characters'),
        'subtitulo': b('Para quien empieza desde cero: cómo suena el chino, cómo se lee el pinyin y qué es un carácter.',
                       'For complete beginners: how Chinese sounds, how to read pinyin and what a character is.'),
        'voz': 'narradora',
        'nota': 'Marcado: (carácter:sonido) pinta ese carácter con el color del sonido (ver sonidos.json); tonos t1–t4 y tn. Cada texto chino lleva `rom` (pinyin con tono, sandhi escrito como suena) y espacios entre palabras. Fuente: tools/contenido/nivel0-zh/generar.py. Apoyo es + en.',
        'textos': {
            'tarjeta': b('¿Empiezas de cero? Los cuatro tonos, el pinyin y qué es un carácter.', 'Starting from zero? The four tones, pinyin and what a character is.'),
            'muestra': '(妈:t1) · (麻:t2) · (马:t3) · (骂:t4)',
            'emoji': '1f469',
            'junta': b('Escucha despacio y después rápido: así se oye el chino.', 'Listen slowly, then fast: that is how Chinese sounds.'),
            'mapaIntro': b('En chino cada sílaba lleva un tono, y el pinyin te dice cómo suena cada carácter. Lo nuevo son los cuatro tonos y el neutro, el soplo de p, t, k, c, q y ch, las retroflejas zh, ch, sh, r, la ü y las finales con -n y -ng. Cada sonido tiene una imagen y un color que verás en las palabras. Toca una tarjeta para oírla.',
                           'In Chinese every syllable has a tone, and pinyin tells you how each character sounds. What is new: the four tones and the neutral one, the puff of p, t, k, c, q and ch, the retroflexes zh, ch, sh, r, the ü and the finals with -n and -ng. Each sound has a picture and a color you will see in the words. Tap a card to hear it.'),
            'grupos': GRUPOS,
        },
        'revision': 'inicial',
        'refuerzo': {'tonos': 'u01', 'sandhi': 'u02', 'labiales': 'u03', 'velares': 'u04',
                     'palatales': 'u05', 'finales': 'u06', 'nasales': 'u07', 'caracteres': 'u08', 'trazos': 'u09'},
        'evaluacion': {'lecciones': ['u10l01', 'u10l02', 'u10l03', 'u10l04'], 'pseudopalabras': ['qü', 'fiu'], 'umbral': 0.8},
        'unidades': UNIDADES,
    }


def escribir(nombre, datos):
    (DESTINO / nombre).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    DESTINO.mkdir(parents=True, exist_ok=True)
    escribir('sonidos.json', sonidos_json())
    escribir('nivel0.json', nivel0_json())
    r = subprocess.run([sys.executable, str(RAIZ / 'tools/contenido/validar_nivel0.py'), 'zh',
                        str(DESTINO / 'nivel0.json'), '--bilingue'])
    sys.exit(r.returncode)
