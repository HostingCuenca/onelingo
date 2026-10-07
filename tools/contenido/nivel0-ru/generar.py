#!/usr/bin/env python3
"""Genera el Nivel 0 «Leer y pronunciar ruso» (alfabeto cirílico).

Escribe assets/contenido/ru/nivel0/sonidos.json y nivel0.json desde los datos
de este archivo y termina con `validar_nivel0.py ru --bilingue`.
Apoyo bilingüe {es, en}: español latino neutro con «tú», inglés americano.
Ruso estándar; sin historia continua; nombres solo de tools/ia/idiomas/ru.md.
Lumo solo en la bienvenida (u01l01), nunca en la evaluación (u10).
Imágenes: solo emoji Noto ya presentes en assets/img/emoji/.

Romanización (`rom`): transliteración neutra letra a letra (decisión fija):
  а a · б b · в v · г g · д d · е e (ye al inicio, tras vocal o tras ь/ъ) · ё yo ·
  ж zh · з z · и i · й y · к k · л l · м m · н n · о o · п p · р r · с s · т t ·
  у u · ф f · х kh · ц ts · ч ch · ш sh · щ shch · ъ " · ы y · ь ' · э e ·
  ю yu · я ya. La vocal tónica lleva tilde aguda en el `rom` de las palabras
  de dos o más sílabas. NUNCA se usa U+0301 en el texto cirílico: el acento
  vive solo en `rom`, calculado desde el léxico LEX_SRC (^ tras la vocal tónica).

17 claves (curriculo/ru/f0.json · previos) → unidades:
  cyrillic-sound-text, letters-like-spanish u01 · letters-false-friends u02 ·
  letters-new-vowels, letter-yo u03 · letters-new-consonants u04 ·
  hard-soft-vowels, vowel-y u05 · vowel-reduction, stress-mobile u06 ·
  hard-soft-consonants, soft-sign, hard-sign u07 · hissing-consonants u08 ·
  final-devoicing, voicing-assimilation, question-intonation u09 · prueba u10.

Orden de letras (cada palabra solo usa letras ya enseñadas):
  u01 а к м о т · u02 в н р с у х · u03 э и е я ю ё · u04 б г д з л п ф й ж ш щ ч ц ·
  u05 ы · u07 ь ъ.

Uso: python3 tools/contenido/nivel0-ru/generar.py
"""
import json
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
DESTINO = RAIZ / 'assets/contenido/ru/nivel0'
GRUPO = re.compile(r'\(([^():]+):([^()]+)\)')
CIRILICO = re.compile(r'[а-яёА-ЯЁ]')


def b(es, en):
    return {'es': es, 'en': en}


def plano(m):
    return GRUPO.sub(lambda g: g.group(1), m)


# ── Romanización y léxico con acento ─────────────────────────────────────────
MAP = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
       'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
       'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '"',
       'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ё': 'yo'}
VOC = 'аеёиоуыэюя'
TILDE = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú', 'y': 'ý'}

# Cada palabra con ^ tras su vocal tónica (los monosílabos y la «ё» no la llevan).
LEX_SRC = """
ма^ма кот там как так кто акт а^том такт то том мак
вот нос рот сок у^хо су^мка рука^ тут сон мост хор ва^нна
э^то э^хо экра^н э^ра э^ти такси^ мир рис кит кино^ вино^ метро^ нет те^ма река^ сестра^
ве^тер мя^со моя^ твоя^ я ю^мор меню^ всё моё твоё её нёс ему^
бана^н бар банк балко^н авто^бус гора^ год го^лос гита^ра го^род нога^ газ дом да друг
де^рево вода^ до^ктор доро^га зе^бра зо^на ва^за ро^за звезда^ зима^ луна^ ла^мпа лиса^ лук
ле^то слон стол стул па^па парк порт пти^ца по^чта фо^то флаг ко^фе футбо^л телефо^н чай май
трамва^й музе^й мой твой жира^ф жук жар у^жин жена^ журна^л нож этаж^ шокола^д шар шум шко^ла
ша^пка маши^на борщ щи щу^ка о^вощи ещё чат час челове^к ру^чка врач чек цирк цвето^к цена^
центр конце^рт у^лица оте^ц
рад ряд люк ты мы вы сыр сын ры^ба мы^ло ми^ло был бил
молоко^ хорошо^ соба^ка язы^к ру^ки во^ды города^ окно^ о^кна
брат брать быль у^гол у^голь мать день конь соль семья^ письмо^ пла^тье о^льга друзья^
объём подъе^зд объе^кт объявле^ние съел сел подва^л
жить шить жизнь ча^шка шов цех а^нна заво^д
хлеб хле^ба дру^га глаз сад са^да ло^жка вокза^л за^втра сдать
здра^вствуйте спаси^бо приве^т до свида^ния извини^те пожа^луйста зову^т меня^ дела^ пока^
вход вы^ход апте^ка магази^н туале^т откры^то закры^то аэропо^рт гости^ница университе^т рестора^н
макси^м мари^я ро^лфа зи^фка
"""
LEX = {}
for _t in LEX_SRC.split():
    LEX[_t.replace('^', '')] = _t


FALTAN = set()


def rom_palabra(tok):
    todo_mayus = len(tok) > 1 and tok.isupper()
    t = tok.lower()
    chars = list(t)
    nvoc = sum(c in VOC for c in chars)
    forma = LEX.get(t)
    ac = None
    if forma and '^' in forma:
        ac = forma.index('^') - 1
    elif nvoc >= 2 and 'ё' not in chars:
        FALTAN.add(t)
        ac = 0
    out = ''
    for i, c in enumerate(chars):
        if c == 'е':
            prev = chars[i - 1] if i else ''
            r = 'ye' if (i == 0 or prev in VOC or prev in 'ьъ') else 'e'
        else:
            r = MAP.get(c, c)
        if nvoc >= 2 and c in VOC and (i == ac or c == 'ё'):
            r = r[:-1] + TILDE[r[-1]]
        out += r
    if todo_mayus or tok[0] != tok[0].lower():
        out = out[0].upper() + out[1:]
    return out


TOK = re.compile(r'[а-яёА-ЯЁ]+(?:-[а-яёА-ЯЁ]+)*|[^а-яёА-ЯЁ]+')


def rom(texto):
    return ''.join(rom_palabra(t) if CIRILICO.match(t) else t for t in TOK.findall(texto))


def forma_acentuada(w):
    return LEX[w]


# ── Marcado de color ─────────────────────────────────────────────────────────
ID = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
      'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
      'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh',
      'щ': 'shch', 'ъ': 'tz', 'ы': 'y', 'ь': 'mz', 'э': 'e', 'ю': 'yu', 'я': 'ya'}


def K(w, letras):
    """Marca con el color de su sonido las letras de `letras` que aparecen en la palabra."""
    return ''.join(f'({c}:{ID[c.lower()]})' if c.lower() in letras else c for c in w)


def R(w):
    """Marca como «red» las vocales átonas о, а, е, я (reducción vocálica)."""
    f = LEX[w]
    ac = f.index('^') - 1
    return ''.join(f'({c}:red)' if (c in 'оаея' and i != ac) else c for i, c in enumerate(w))


def SB(w):
    """Marca ь (mz) y la consonante que ablanda (bl)."""
    return re.sub(r'(.)ь', lambda g: f'({g.group(1)}:bl)(ь:mz)', w)


# ── Mapa de sonidos ──────────────────────────────────────────────────────────
PALETA = [
    ('#E24B4A', 'rojo', 'red'), ('#2E8B57', 'verde', 'green'), ('#1E88E5', 'azul', 'blue'),
    ('#E8B923', 'amarillo', 'yellow'), ('#7E57C2', 'violeta', 'violet'), ('#E0559B', 'rosa', 'pink'),
    ('#F08A24', 'naranja', 'orange'), ('#00A6A6', 'turquesa', 'teal'), ('#FF7043', 'coral', 'coral'),
    ('#9C6ADE', 'lila', 'lilac'), ('#C0CA33', 'pistacho', 'pistachio'), ('#3949AB', 'índigo', 'indigo'),
    ('#AD1457', 'granate', 'maroon'), ('#5D4037', 'café', 'coffee'), ('#D4A017', 'dorado', 'gold'),
    ('#D84315', 'teja', 'brick'), ('#7CB342', 'lima', 'lime'), ('#455A64', 'pizarra', 'slate'),
    ('#6B8E23', 'oliva', 'olive'), ('#26A69A', 'verde agua', 'aqua'), ('#C2185B', 'frambuesa', 'raspberry'),
    ('#795548', 'chocolate', 'chocolate'), ('#8D6E63', 'café con leche', 'latte'), ('#4FC3F7', 'celeste', 'sky blue'),
    ('#C68E17', 'ocre', 'ochre'), ('#AB47BC', 'orquídea', 'orchid'), ('#80CBC4', 'menta', 'mint'),
    ('#EF9A9A', 'salmón', 'salmon'), ('#1A237E', 'marino', 'navy'), ('#616161', 'gris', 'gray'),
    ('#6A1B9A', 'ciruela', 'plum'), ('#BF6B3A', 'cobre', 'copper'), ('#558B2F', 'musgo', 'moss'),
    ('#00695C', 'petróleo', 'petrol'), ('#D7B98E', 'arena', 'sand'), ('#880E4F', 'vino', 'wine'),
    ('#00B8D4', 'cian', 'cyan'),
]

# (id, grupo, ancla, emoji, nombre es, nombre en, grafías, ejemplos, unidad)
SONIDOS = [
    ('a', 'igual', 'автобус', '1f68c', 'А = «a», como en español: автобус', 'А = “a” as in “father”: автобус', ['а'], ['автобус', 'мама', 'такси'], 1),
    ('o', 'igual', 'облако', '2601', 'О = «o», como en español, con acento: облако', 'О = “o” as in “more,” when stressed: облако', ['о'], ['облако', 'кот', 'метро'], 1),
    ('k', 'igual', 'кот', '1f431', 'К = «k», sin soplo: кот', 'К = “k,” with no puff of air: кот', ['к'], ['кот', 'как', 'мак'], 1),
    ('m', 'igual', 'молоко', '1f95b', 'М = «m»: молоко', 'М = “m”: молоко', ['м'], ['молоко', 'мама', 'мир'], 1),
    ('t', 'igual', 'торт', '1f370', 'Т = «t», sin soplo: торт', 'Т = “t,” with no puff of air: торт', ['т'], ['торт', 'там', 'кто'], 1),
    ('v', 'falsa', 'волк', '1f43a', 'В = «v» (no «b»): волк', 'В = “v” (not “b”): волк', ['в'], ['волк', 'вода', 'вот'], 2),
    ('n', 'falsa', 'нос', '1f443', 'Н = «n» (no «h»): нос', 'Н = “n” (not “h”): нос', ['н'], ['нос', 'нет', 'сон'], 2),
    ('r', 'falsa', 'рот', '1f444', 'Р = «r» vibrante (no «p»): рот', 'Р = rolled “r” (not “p”): рот', ['р'], ['рот', 'рука', 'мир'], 2),
    ('s', 'falsa', 'слон', '1f418', 'С = «s» (no «k»): слон', 'С = “s” (not “k”): слон', ['с'], ['слон', 'сок', 'нос'], 2),
    ('u', 'falsa', 'утка', '1f986', 'У = «u» (no «y»): утка', 'У = “oo” (not “y”): утка', ['у'], ['утка', 'ухо', 'рука'], 2),
    ('kh', 'falsa', 'хлеб', '1f35e', 'Х = «j» de «jamón» (no «x»): хлеб', 'Х = “kh” as in “loch” (not “x”): хлеб', ['х'], ['хлеб', 'хор', 'ухо'], 2),
    ('e', 'vocal', 'экран', '1f4fa', 'Э = «e» de «mesa»: экран', 'Э = “e” as in “bed”: экран', ['э'], ['экран', 'это', 'эхо'], 3),
    ('i', 'blanda', 'игра', '1f3ae', 'И = «i» de «sí»: игра', 'И = “ee” as in “see”: игра', ['и'], ['игра', 'такси', 'мир'], 3),
    ('ya', 'blanda', 'яблоко', '1f34e', 'Я = «ya», como en «playa»: яблоко', 'Я = “ya” as in “yard”: яблоко', ['я'], ['яблоко', 'моя', 'мясо'], 3),
    ('yu', 'blanda', 'юбка', '1f457', 'Ю = «yu», como en «yuca»: юбка', 'Ю = “yoo” as in “you”: юбка', ['ю'], ['юбка', 'меню', 'юмор'], 3),
    ('ye', 'blanda', 'еда', '1f37d', 'Е = «ye» (o «e» tras consonante): еда', 'Е = “ye” (or “e” after a consonant): еда', ['е'], ['еда', 'нет', 'метро'], 3),
    ('yo', 'blanda', 'ёлка', '1f332', 'Ё = «yo», siempre tónica: ёлка', 'Ё = “yo,” always stressed: ёлка', ['ё'], ['ёлка', 'всё', 'моё'], 3),
    ('y', 'vocal', 'сыр', '1f9c0', 'Ы = vocal central, entre «i» y «u»: сыр', 'Ы = central vowel, between “ee” and “oo”: сыр', ['ы', 'и tras ж, ш, ц'], ['сыр', 'мы', 'жить'], 5),
    ('b', 'nueva', 'банан', '1f34c', 'Б = «b»: банан', 'Б = “b”: банан', ['б'], ['банан', 'бар', 'банк'], 4),
    ('g', 'nueva', 'гитара', '1f3b8', 'Г = «g» de «gato», siempre: гитара', 'Г = “g” as in “go,” always: гитара', ['г'], ['гитара', 'гора', 'год'], 4),
    ('d', 'nueva', 'дом', '1f3e0', 'Д = «d»: дом', 'Д = “d”: дом', ['д'], ['дом', 'да', 'вода'], 4),
    ('z', 'nueva', 'зебра', '1f993', 'З = «s» con zumbido, como la «z» inglesa de «zoo»: зебра', 'З = “z” as in “zoo”: зебра', ['з'], ['зебра', 'зима', 'зона'], 4),
    ('l', 'nueva', 'луна', '1f319', 'Л = «l» firme, con la lengua atrás: луна', 'Л = “l” with the tongue back, as in “ball”: луна', ['л'], ['луна', 'лиса', 'лук'], 4),
    ('p', 'nueva', 'птица', '1f426', 'П = «p», sin soplo: птица', 'П = “p,” with no puff of air: птица', ['п'], ['птица', 'папа', 'парк'], 4),
    ('f', 'nueva', 'фото', '1f4f7', 'Ф = «f»: фото', 'Ф = “f”: фото', ['ф'], ['фото', 'флаг', 'кофе'], 4),
    ('j', 'nueva', 'чай', '1f375', 'Й = una «i» muy breve, como en «hoy»: чай', 'Й = a very short “ee,” as in “boy”: чай', ['й'], ['чай', 'май', 'музей'], 4),
    ('zh', 'sibil', 'жираф', '1f992', 'Ж = como la «j» del francés «jour» (o la «y» rioplatense): жираф', 'Ж = like the “s” in “measure”: жираф', ['ж'], ['жираф', 'жена', 'нож'], 4),
    ('sh', 'sibil', 'шоколад', '1f36b', 'Ш = «sh» con la lengua curvada hacia atrás: шоколад', 'Ш = “sh” with the tongue curled back: шоколад', ['ш'], ['шоколад', 'шар', 'школа'], 4),
    ('shch', 'sibil', 'щи', '1f372', 'Щ = «sh» larga y blanda: щи', 'Щ = a long, soft “sh”: щи', ['щ'], ['щи', 'борщ', 'ещё'], 4),
    ('ch', 'sibil', 'чемодан', '1f9f3', 'Ч = «ch» suave, sin explosión: чемодан', 'Ч = a soft “ch,” without a burst: чемодан', ['ч'], ['чемодан', 'чай', 'час'], 4),
    ('ts', 'sibil', 'цветок', '1f337', 'Ц = «ts», como en «pizza»: цветок', 'Ц = “ts” as in “cats”: цветок', ['ц'], ['цветок', 'цена', 'конец'], 4),
    ('mz', 'signo', 'конь', '1f434', 'Ь no suena: ablanda la consonante anterior: конь', 'Ь is silent: it softens the consonant before it: конь', ['ь'], ['конь', 'день', 'семья'], 7),
    ('tz', 'signo', 'подъезд', '1f6aa', 'Ъ no suena: separa con una pausa breve: подъезд', 'Ъ is silent: it separates with a tiny pause: подъезд', ['ъ'], ['подъезд', 'объём', 'съел'], 7),
    ('red', 'regla', 'молоко', '1f95b', 'Vocal átona reducida: о y а suenan «a» corta, е y я suenan «i»: молоко', 'Reduced unstressed vowel: о and а sound like a short “uh,” е and я like a short “i”: молоко', ['о, а, е, я sin acento'], ['молоко', 'вода', 'река'], 6),
    ('bl', 'regla', 'мяч', '26bd', 'Consonante blanda: la lengua sube hacia el paladar, como al decir «i»: мяч', 'Soft consonant: the tongue rises toward the palate, as when saying “ee”: мяч', ['consonante + ь, я, е, ё, ю, и'], ['мяч', 'люк', 'день'], 7),
    ('ens', 'regla', 'друг', '1f91d', 'Sonora que se ensordece: друг suena «druk», хлеб suena «jlep»', 'Voiced sound that becomes voiceless: друг sounds like “druk,” хлеб like “khlep”', ['б, в, г, д, ж, з al final o ante sorda'], ['друг', 'хлеб', 'ложка'], 9),
    ('son', 'regla', 'вокзал', '1f686', 'Sorda que se sonoriza ante sonora: вокзал suena «vagzál»', 'Voiceless sound that becomes voiced: вокзал sounds like “vagzál”', ['к, с, т, п… ante sonora'], ['вокзал', 'сдать', 'футбол'], 9),
]

GRUPOS = {
    'igual': b('Letras que suenan como en español', 'Letters that sound as expected'),
    'falsa': b('Letras engañosas: parecen latinas, suenan distinto', 'Tricky letters: they look Latin but sound different'),
    'vocal': b('Vocales duras: э y ы', 'Hard vowels: э and ы'),
    'blanda': b('Vocales blandas: я, ю, е, ё, и', 'Soft vowels: я, ю, е, ё, и'),
    'nueva': b('Consonantes nuevas', 'New consonants'),
    'sibil': b('Ж, ш, щ, ч, ц', 'Ж, ш, щ, ч, ц'),
    'signo': b('Signos: ь y ъ', 'Signs: ь and ъ'),
    'regla': b('Reglas de pronunciación', 'Pronunciation rules'),
}


def sonidos_json():
    assert len(PALETA) >= len(SONIDOS)
    return {
        'esquema': 'onelingo.sonidos.v1',
        'idioma': 'ru',
        'nota': 'Mapa de sonidos del ruso estándar (norma de Moscú). El color acompaña siempre al nombre y a la imagen; es una pista de escucha, no una transcripción fonética. Los marcadores red, bl, ens y son señalan reglas (reducción, consonante blanda, ensordecimiento, sonorización).',
        'marcas': {'_': 'letra que no suena', '=': 'varias letras, un sonido'},
        'acento': b('Modelo: ruso estándar de Moscú. El acento no se escribe en el cirílico: se marca con ´ en la romanización.',
                    'Model: standard Moscow Russian. Stress is not written in Cyrillic: it is marked with ´ in the romanization.'),
        'vocales': [
            {'id': i, 'grupo': g, 'color': PALETA[n][0], 'colorNombre': b(PALETA[n][1], PALETA[n][2]),
             'ancla': a, 'emoji': e, 'nombre': b(nes, nen), 'grafias': gr, 'ejemplos': ej, 'unidad': u}
            for n, (i, g, a, e, nes, nen, gr, ej, u) in enumerate(SONIDOS)
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
FUERZA = ('¿Dónde va la fuerza?', 'Where is the stress?')


def L(lid, tes, ten, palabras, mira, foco=None, par=None, oye=None, extras=(), construye=None, inv=False, nota=None):
    """Plantilla: escucha → mira → repite → [toca_sonido] → [escucha_elige] → extras → construye."""
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


def fuerza(m, tes, ten, ops, correcta=0):
    return lee(m, tes, ten, *FUERZA, ops, correcta)


A = 'акмот'
PRIMERAS = 'акмотвнрсух'
VOCNUEVAS = 'эиеяюё'

UNIDADES = [
    {
        'id': 'u01', 'titulo': b('R1 · Del sonido a la letra', 'R1 · From sound to letter'),
        'objetivo': b('Comprobar que el cirílico se lee como suena y leer las primeras palabras con А, К, М, О, Т, cinco letras que suenan como en español.',
                      'See that Cyrillic is read as it sounds and read your first words with А, К, М, О, Т, five letters that sound just as you would expect.'),
        'lecciones': [
            L('u01l01', 'El cirílico se lee como suena', 'Cyrillic is read as it sounds',
              [W(K('мама', A), 'mamá', 'mom', '1f469'), W(K('кот', A), 'gato', 'cat', '1f431'), W(K('там', A), 'allí', 'there')],
              (K('кот', A), 'Esto es cirílico, el alfabeto del ruso. Casi cada letra tiene un solo sonido, así que se lee como suena. Cinco letras te sonarán conocidas: А, К, М, О y Т suenan como en español. Los colores te ayudan a recordar cada sonido.',
               'This is Cyrillic, the Russian alphabet. Almost every letter has a single sound, so you read it as it sounds. Five letters will feel familiar: А, К, М, О and Т sound just as you would expect. The colors help you remember each sound.'),
              foco='k', par=(K('кот', A), K('мама', A)), oye=('кот', 'там'),
              extras=[
                  {'tipo': 'lumo', 'pose': 'anima', 'texto': b('Bienvenido al ruso. Primero escucharás, después leerás letra por letra. ¡Los colores te ayudan a recordar cada sonido!',
                                                              'Welcome to Russian. First you listen, then you read letter by letter. The colors help you remember each sound!')},
                  sig('кот', ('gato', 'cat'), ('casa', 'house')),
              ],
              construye=('кот', 'а')),
            L('u01l02', 'А y О: vocales claras', 'А and О: clear vowels',
              [W(K('так', A), 'así', 'so'), W(K('как', A), 'cómo', 'how'), W(K('акт', A), 'acto', 'act')],
              (K('как', A), 'А suena «a» y О suena «o»: abre la boca y di la vocal clara, como en «mamá» y «foto». Por ahora, léelas siempre así.',
               'А sounds like “a” and О like “o”: open your mouth and say the vowel clearly, as in “father” and “more.” For now, always read them this way.'),
              foco='a', par=(K('так', A), K('кот', A)), oye=('как', 'так'),
              extras=[sig('как', ('cómo', 'how'), ('quién', 'who')), cambia('как', 'так', ['т', 'к', 'м'])],
              construye=('так', 'о')),
            L('u01l03', 'К, М, Т: tres consonantes amigas', 'К, М, Т: three friendly consonants',
              [W(K('кто', A), 'quién', 'who'), W(K('мак', A), 'amapola', 'poppy'), W(K('том', A), 'tomo (de un libro)', 'volume (of a book)')],
              (K('кто', A), 'К, М y Т suenan «k», «m» y «t»: la К y la Т son secas, sin soplo de aire. Así, кто se lee «kto»: tres sonidos seguidos.',
               'К, М and Т sound like “k,” “m” and “t”: К and Т are crisp, without a puff of air. So кто is read “kto”: three sounds in a row.'),
              foco='m', par=(K('мак', A), K('кот', A)), oye=('кто', 'кот'),
              extras=[sig('кто', ('quién', 'who'), ('allí', 'there')), mezcla('том', 'tomo (de un libro)', 'volume (of a book)')],
              construye=('кто', 'а')),
            L('u01l04', 'Palabras que ya conoces', 'Words you already know',
              [W(K('атом', A), 'átomo', 'atom'), W(K('акт', A), 'acto', 'act'), W(K('такт', A), 'tacto; compás', 'tact; beat')],
              (K('атом', A), 'Muchas palabras rusas se parecen a las nuestras: атом, акт, такт. Si conoces las letras, las lees sin ayuda.',
               'Many Russian words look like English ones: атом, акт, такт. If you know the letters, you can read them without help.'),
              foco='o', par=(K('атом', A), K('такт', A)), oye=('атом', 'акт'),
              extras=[lee('Кто там?', '¿Quién está ahí?', 'Who is there?', '¿Cuál palabra significa «allí»?', 'Which word means “there”?', ['там', 'кто'])],
              construye=('атом', 'к')),
        ],
    },
    {
        'id': 'u02', 'titulo': b('R2 · Letras engañosas', 'R2 · Tricky letters'),
        'objetivo': b('Leer В, Н, Р, С, У y Х, que parecen letras latinas pero suenan distinto («v», «n», «r», «s», «u», «j»).',
                      'Read В, Н, Р, С, У and Х, which look like Latin letters but sound different (“v,” “n,” “r,” “s,” “oo,” “kh”).'),
        'lecciones': [
            L('u02l01', 'В y Н: no son «b» ni «h»', 'В and Н: not “b” or “h”',
              [W(K('вот', 'вн'), 'aquí está', 'here is', None), W(K('нос', 'вн'), 'nariz', 'nose', '1f443'), W(K('ванна', 'вн'), 'bañera', 'bathtub', '1f6c1')],
              (K('вот', 'вн'), 'Cuidado: В no es «b» y Н no es «h». В suena «v», con los dientes de arriba sobre el labio de abajo. Н suena «n».',
               'Careful: В is not “b” and Н is not “h.” В sounds like “v,” with your upper teeth on your lower lip. Н sounds like “n.”'),
              foco='v', par=(K('вот', 'вн'), K('нос', 'н')), oye=('вот', 'нос'),
              extras=[letra('В', ['В', 'Н', 'Р']), letra('Н', ['Н', 'В', 'С']), sig('нос', ('nariz', 'nose'), ('boca', 'mouth'))],
              construye=('нос', 'а')),
            L('u02l02', 'Р y С: no son «p» ni «k»', 'Р and С: not “p” or “k”',
              [W(K('рот', 'рс'), 'boca', 'mouth', '1f444'), W(K('сок', 'рс'), 'jugo', 'juice', '1f9c3'), W(K('мост', 'рс'), 'puente', 'bridge', '1f309')],
              (K('рот', 'рс'), 'Cuidado: Р no es «p»: es una «r» vibrante, como la «rr» de «perro». С no es «k»: suena «s», como en «sol».',
               'Careful: Р is not “p”: it is a rolled “r,” like Spanish “rr.” С is not “k”: it sounds like “s,” as in “sun.”'),
              foco='r', par=(K('рот', 'рс'), K('сок', 'с')), oye=('рот', 'сок'),
              extras=[toca('s', K('сок', 'рс'), 'кот'), letra('Р', ['Р', 'Н', 'В']), letra('С', ['С', 'К', 'Р']), sig('рот', ('boca', 'mouth'), ('nariz', 'nose'))],
              construye=('сок', 'р')),
            L('u02l03', 'У y Х: no son «y» ni «x»', 'У and Х: not “y” or “x”',
              [W(K('ухо', 'ух'), 'oreja', 'ear', '1f442'), W(K('рука', 'ух'), 'mano; brazo', 'hand; arm', '270b'), W(K('хор', 'ух'), 'coro', 'choir')],
              (K('ухо', 'ух'), 'Cuidado: У no es «y»: suena «u», como en «luna». Х no es «x»: suena como la «j» de «jamón»: хор se lee «jor».',
               'Careful: У is not “y”: it sounds like “oo,” as in “moon.” Х is not “x”: it sounds like “kh,” the throaty sound in “loch”: хор is read “khor.”'),
              foco='kh', par=(K('хор', 'ух'), K('рука', 'у')), oye=('ухо', 'хор'),
              extras=[letra('У', ['У', 'Х', 'В']), letra('Х', ['Х', 'Н', 'Р']), sig('ухо', ('oreja', 'ear'), ('nariz', 'nose'))],
              construye=('рука', 'о')),
            L('u02l04', 'Las seis juntas', 'All six together',
              [W(K('сумка', PRIMERAS), 'bolso', 'bag', '1f45c'), W(K('тут', PRIMERAS), 'aquí', 'here'), W(K('сон', PRIMERAS), 'sueño', 'sleep; dream')],
              (K('сумка', PRIMERAS), 'Repaso: В = «v», Н = «n», Р = «r», С = «s», У = «u», Х = «j». No las leas como letras latinas: lee el sonido que tienen.',
               'Review: В = “v,” Н = “n,” Р = rolled “r,” С = “s,” У = “oo,” Х = “kh.” Do not read them as Latin letters: read the sound they have.'),
              foco='u', par=(K('тут', PRIMERAS), K('сок', 'с')), oye=('сон', 'сок'),
              extras=[cambia('рот', 'вот', ['в', 'р', 'н']), cambia('сок', 'сон', ['н', 'к', 'м']),
                      deletreo('Анна', 'Escucha y ordena las letras de Анна.', 'Listen and put the letters of Анна in order.'),
                      sig('сумка', ('bolso', 'bag'), ('mano', 'hand'))],
              construye=('сумка', 'о')),
        ],
    },
    {
        'id': 'u03', 'titulo': b('R3 · Vocales nuevas: э, и, я, ю, е, ё', 'R3 · New vowels: э, и, я, ю, е, ё'),
        'objetivo': b('Leer las vocales э, и, я, ю, е y ё, y saber que la ё siempre lleva el acento.',
                      'Read the vowels э, и, я, ю, е and ё, and know that ё is always stressed.'),
        'lecciones': [
            L('u03l01', 'Э e И', 'Э and И',
              [W(K('это', 'эи'), 'esto; esto es', 'this; this is'), W(K('эхо', 'эи'), 'eco', 'echo'), W(K('такси', 'эи'), 'taxi', 'taxi'), W(K('мир', 'эи'), 'paz; mundo', 'peace; world')],
              (K('это', 'эи'), 'Э suena «e», como la e de «mesa». И suena «i», como la i de «sí». No te confundas: la Э parece una E latina al revés.',
               'Э sounds like “e,” as in “bed.” И sounds like “ee,” as in “see.” Do not be fooled: Э looks like a backwards E.'),
              foco='e', par=(K('это', 'эи'), K('такси', 'и')), oye=('эхо', 'мир'),
              extras=[letra('Э', ['Э', 'Е', 'И']), letra('И', ['И', 'Н', 'Э']), sig('мир', ('paz; mundo', 'peace; world'), ('nariz', 'nose'))],
              construye=('мир', 'а')),
            L('u03l02', 'Я y Ю: «ya» y «yu»', 'Я and Ю: “ya” and “yu”',
              [W(K('я', 'яю'), 'yo', 'I'), W(K('моя', 'яю'), 'mi; mía', 'my; mine (feminine)'), W(K('меню', 'яю'), 'menú', 'menu'), W(K('юмор', 'яю'), 'humor', 'humor')],
              (K('моя', 'яю'), 'Я suena «ya», como en «playa», y es también la palabra «yo». Ю suena «yu», como en «yuca». Son vocales «blandas»: más adelante verás cómo ablandan la consonante anterior.',
               'Я sounds like “ya,” as in “yard,” and it is also the word “I.” Ю sounds like “yoo,” as in “you.” They are “soft” vowels: later you will see how they soften the consonant before them.'),
              foco='ya', par=(K('моя', 'яю'), K('меню', 'ю')), oye=('меню', 'мир'),
              extras=[toca('yu', K('юмор', 'яю'), 'мир'), letra('Я', ['Я', 'А', 'Ю']), letra('Ю', ['Ю', 'У', 'Я']), sig('меню', ('menú', 'menu'), ('mundo', 'world'))],
              construye=('меню', 'а')),
            L('u03l03', 'Е: «ye» o «e»', 'Е: “ye” or “e”',
              [W(K('нет', 'е'), 'no', 'no'), W(K('метро', 'е'), 'metro', 'subway'), W(K('ветер', 'е'), 'viento', 'wind', '1f32c'), W(K('ему', 'е'), 'a él; le', 'to him')],
              (K('нет', 'е'), 'Е suena «ye» al inicio de palabra o después de vocal (ему ≈ «yemú»). Después de una consonante suena una «e» que ablanda esa consonante: нет ≈ «ñet», метро ≈ «metró» con la «m» suave.',
               'Е sounds like “ye” at the start of a word or after a vowel (ему ≈ “yeh-MOO”). After a consonant it is an “e” that softens that consonant: нет ≈ “nyet,” метро ≈ “myeh-TRO.”'),
              foco='ye', par=(K('нет', 'е'), K('такси', 'и')), oye=('метро', 'мир'),
              extras=[letra('Е', ['Е', 'Э', 'Ё']), sig('нет', ('no', 'no'), ('sí', 'yes')), mezcla('ветер', 'viento', 'wind')],
              construye=('нет', 'а')),
            L('u03l04', 'Ё: siempre con acento', 'Ё: always stressed',
              [W(K('всё', 'ё'), 'todo', 'everything'), W(K('моё', 'ё'), 'mío (neutro)', 'mine (neuter)'), W(K('твоё', 'ё'), 'tuyo (neutro)', 'yours (neuter)'), W(K('её', 'ё'), 'su; de ella', 'her; hers')],
              (K('всё', 'ё'), 'Ё suena «yo» y es siempre tónica: lleva el acento sin necesidad de otra marca. En este curso se escribe siempre con sus dos puntos: всё, моё. Es una letra distinta de Е.',
               'Ё sounds like “yo” and is always stressed: it carries the stress with no other mark. In this course it is always written with its two dots: всё, моё. It is a different letter from Е.'),
              foco='yo', par=(K('всё', 'ё'), K('метро', 'е')), oye=('всё', 'вот'),
              extras=[cambia('нос', 'нёс', ['ё', 'о', 'е']), sig('всё', ('todo', 'everything'), ('nada', 'nothing')), letra('Ё', ['Ё', 'Е', 'О'])],
              construye=('моё', 'а')),
        ],
    },
    {
        'id': 'u04', 'titulo': b('R4 · Consonantes nuevas', 'R4 · New consonants'),
        'objetivo': b('Leer las consonantes que no tienes en español o que no suenan igual: б, г, д, з, л, п, ф, й, ж, ш, щ, ч, ц.',
                      'Read the consonants you do not have, or that do not sound the same: б, г, д, з, л, п, ф, й, ж, ш, щ, ч, ц.'),
        'lecciones': [
            L('u04l01', 'Б, Г, Д, З', 'Б, Г, Д, З',
              [W(K('банан', 'бгдз'), 'plátano', 'banana', '1f34c'), W(K('гора', 'бгдз'), 'montaña', 'mountain', '26f0'), W(K('дом', 'бгдз'), 'casa; edificio', 'house; building', '1f3e0'), W(K('зебра', 'бгдз'), 'cebra', 'zebra', '1f993')],
              (K('гора', 'бгдз'), 'Б = «b», Г = «g» de «gato» (siempre, nunca «j»), Д = «d». З es una «s» con zumbido en la garganta, como la «z» inglesa de «zoo»: no suena como la «z» española.',
               'Б = “b,” Г = “g” as in “go” (always, never “j”), Д = “d.” З is a buzzing “s,” like the “z” in “zoo.”'),
              foco='g', par=(K('гора', 'бгдз'), 'мир'), oye=('гора', 'дом'),
              extras=[letra('Д', ['Д', 'Б', 'Г']), letra('З', ['З', 'С', 'Д']), sig('дом', ('casa; edificio', 'house; building'), ('ciudad', 'city'))],
              construye=('дом', 'а')),
            L('u04l02', 'Л, П, Ф, Й', 'Л, П, Ф, Й',
              [W(K('луна', 'лпфй'), 'luna', 'moon', '1f319'), W(K('парк', 'лпфй'), 'parque', 'park', '1f333'), W(K('фото', 'лпфй'), 'foto', 'photo', '1f4f7'), W(K('музей', 'лпфй'), 'museo', 'museum')],
              (K('музей', 'лпфй'), 'Л suena «l» firme, con la lengua atrás, como en el inglés «ball». П = «p» sin soplo y Ф = «f». Й es una «i» muy breve al final de sílaba: музей ≈ «muzéi».',
               'Л sounds like a firm “l,” with the tongue back, as in “ball.” П = “p” with no puff of air, Ф = “f.” Й is a very short “ee” at the end of a syllable: музей ≈ “moo-ZEY.”'),
              foco='j', par=(K('музей', 'лпфй'), 'мир'), oye=('луна', 'лук'),
              extras=[toca('l', K('луна', 'лпфй'), 'парк'), sig('парк', ('parque', 'park'), ('museo', 'museum')), letra('Л', ['Л', 'П', 'Ф'])],
              construye=('парк', 'о')),
            L('u04l03', 'Ж, Ш, Щ', 'Ж, Ш, Щ',
              [W(K('жираф', 'жшщ'), 'jirafa', 'giraffe', '1f992'), W(K('шоколад', 'жшщ'), 'chocolate', 'chocolate', '1f36b'), W(K('борщ', 'жшщ'), 'borsch (sopa)', 'borscht (soup)', '1f372')],
              (K('шоколад', 'жшщ'), 'Ж suena como la «j» del francés «jour» (o como la «y» rioplatense de «yo»). Ш = «sh» con la lengua curvada hacia atrás. Щ = una «sh» larga y blanda: no son «sh» y «ch» separadas.',
               'Ж sounds like the “s” in “measure.” Ш = “sh” with the tongue curled back. Щ = a long, soft “sh”: not “sh” and “ch” separately.'),
              foco='sh', par=(K('шоколад', 'жшщ'), K('жираф', 'жшщ')), oye=('жираф', 'шоколад'),
              extras=[toca('shch', K('борщ', 'жшщ'), 'жираф'), sig('жираф', ('jirafa', 'giraffe'), ('cebra', 'zebra')), letra('Ж', ['Ж', 'З', 'Ш'])],
              construye=('борщ', 'а')),
            L('u04l04', 'Ч y Ц', 'Ч and Ц',
              [W(K('чай', 'чц'), 'té', 'tea', '1f375'), W(K('цветок', 'чц'), 'flor', 'flower', '1f337'), W(K('концерт', 'чц'), 'concierto', 'concert'), W(K('врач', 'чц'), 'médico', 'doctor')],
              (K('цветок', 'чц'), 'Ч suena como la «ch» de «chico», pero más suave y sin explosión. Ц suena «ts», como en «pizza»: цветок ≈ «tsvetók».',
               'Ч sounds like “ch,” but softer and without a burst. Ц sounds like “ts” in “cats”: цветок ≈ “tsvyeh-TOK.”'),
              foco='ts', par=(K('цветок', 'чц'), K('чай', 'чц')), oye=('чай', 'цена'),
              extras=[deletreo('Мария', 'Escucha y ordena las letras de Мария.', 'Listen and put the letters of Мария in order.'),
                      sig('цветок', ('flor', 'flower'), ('árbol', 'tree')), letra('Ч', ['Ч', 'Ц', 'Щ'])],
              construye=('чай', 'о')),
        ],
    },
    {
        'id': 'u05', 'titulo': b('R5 · Vocales duras y blandas, y la ы', 'R5 · Hard and soft vowels, and ы'),
        'objetivo': b('Distinguir los cinco pares de vocales (а–я, о–ё, у–ю, э–е, ы–и) y pronunciar la ы, la vocal central del ruso.',
                      'Tell the five vowel pairs apart (а–я, о–ё, у–ю, э–е, ы–и) and pronounce ы, the central vowel of Russian.'),
        'lecciones': [
            L('u05l01', 'Pares: а–я y о–ё', 'Pairs: а–я and о–ё',
              [W(K('рад', 'аяоё'), 'contento', 'glad'), W(K('ряд', 'аяоё'), 'fila', 'row'), W(K('нос', 'аяоё'), 'nariz', 'nose'), W(K('нёс', 'аяоё'), 'él llevó', 'he carried')],
              (K('ряд', 'аяоё'), 'En ruso hay cinco vocales «duras» (а, о, у, э, ы) y cinco «blandas» (я, ё, ю, е, и). La blanda ablanda la consonante anterior: рад (р dura) ≠ ряд (р blanda, «ria»). Cambia la vocal y cambia la palabra.',
               'Russian has five “hard” vowels (а, о, у, э, ы) and five “soft” ones (я, ё, ю, е, и). The soft one softens the consonant before it: рад (hard р) ≠ ряд (soft р, “rya”). Change the vowel and you change the word.'),
              foco='ya', par=(K('ряд', 'аяоё'), K('рад', 'аяоё')), oye=('ряд', 'рад'),
              extras=[cambia('рад', 'ряд', ['я', 'а', 'о']), sig('ряд', ('fila', 'row'), ('contento', 'glad'))],
              construye=('ряд', 'а')),
            L('u05l02', 'Pares: у–ю y э–е', 'Pairs: у–ю and э–е',
              [W(K('лук', 'уюэе'), 'cebolla', 'onion'), W(K('люк', 'уюэе'), 'escotilla', 'hatch'), W(K('мэр', 'уюэе'), 'alcalde', 'mayor'), W(K('нет', 'уюэе'), 'no', 'no')],
              (K('люк', 'уюэе'), 'Lo mismo ocurre con у–ю y э–е: лук (л dura) ≠ люк (л blanda, «liuk»). Después de ме-, не-, ле-… la consonante se hace blanda. La Э en cambio es dura y aparece casi solo en palabras tomadas de otras lenguas: мэр.',
               'The same goes for у–ю and э–е: лук (hard л) ≠ люк (soft л, “lyook”). After ме-, не-, ле-… the consonant becomes soft. Э, on the other hand, is hard and appears almost only in borrowed words: мэр.'),
              foco='yu', par=(K('люк', 'уюэе'), K('лук', 'уюэе')), oye=('люк', 'лук'),
              extras=[cambia('лук', 'люк', ['ю', 'у', 'а']), sig('люк', ('escotilla', 'hatch'), ('cebolla', 'onion')), toca('e', K('мэр', 'уюэе'), 'нет')],
              construye=('лук', 'ю')),
            L('u05l03', 'Ы: la vocal central', 'Ы: the central vowel',
              [W(K('ты', 'ы'), 'tú', 'you (informal)'), W(K('мы', 'ы'), 'nosotros', 'we'), W(K('сыр', 'ы'), 'queso', 'cheese', '1f9c0'), W(K('сын', 'ы'), 'hijo', 'son', '1f466')],
              (K('сыр', 'ы'), 'Ы es una vocal que no existe en español: di «i» con los labios sin redondear y la lengua llevada hacia atrás, entre «i» y «u». Nunca va al inicio de una palabra: ты ≠ ти.',
               'Ы is a vowel that does not exist in English: say “ee” with your lips unrounded and your tongue pulled back, between “ee” and “oo.” It never starts a word.'),
              foco='y', par=(K('сыр', 'ы'), 'мир'), oye=('сыр', 'сын'),
              extras=[sig('мы', ('nosotros', 'we'), ('ustedes', 'you (plural)')), sig('сыр', ('queso', 'cheese'), ('jugo', 'juice'))],
              construye=('сыр', 'и')),
            L('u05l04', 'Ы frente a И', 'Ы versus И',
              [W(K('мыло', 'ыи'), 'jabón', 'soap', '1f9fc'), W(K('мило', 'ыи'), 'lindo; agradable', 'nice; cute'), W(K('был', 'ыи'), 'fue; estuvo', 'was'), W(K('бил', 'ыи'), 'golpeó', 'hit')],
              (K('мыло', 'ыи'), 'Escucha el contraste: мыло (м dura + ы) y мило (м blanda + и). Un solo cambio de vocal cambia la palabra: был (era) y бил (golpeó).',
               'Listen to the contrast: мыло (hard м + ы) and мило (soft м + и). One vowel change makes a different word: был (was) and бил (hit).'),
              foco='y', par=(K('был', 'ыи'), K('бил', 'и')), oye=('мыло', 'мило'),
              extras=[cambia('был', 'бил', ['и', 'ы', 'е']), sig('мыло', ('jabón', 'soap'), ('lindo', 'nice')), oye('был', 'бил')],
              construye=('мыло', 'и')),
        ],
    },
    {
        'id': 'u06', 'titulo': b('R6 · Acento y reducción vocálica', 'R6 · Stress and vowel reduction'),
        'objetivo': b('Oír dónde cae el acento, saber que О y А sin acento suenan «a» corta, que Е y Я suenan «i», y que el acento cambia de sílaba según la forma.',
                      'Hear where the stress falls, know that unstressed О and А sound like a short “uh,” that Е and Я sound like “i,” and that stress moves between syllables.'),
        'lecciones': [
            L('u06l01', 'Una sílaba más fuerte', 'One stronger syllable',
              [W('мама', 'mamá', 'mom', '1f469'), W('метро', 'metro', 'subway'), W('молоко', 'leche', 'milk', '1f95b')],
              ('молоко', 'En cada palabra de dos o más sílabas hay una vocal tónica: más larga y clara. En el romanizado la marcamos con ´: máma, metró, molokó. En ruso el acento no se escribe y no sigue una regla fija: se aprende con cada palabra.',
               'In every word of two or more syllables, one vowel is stressed: longer and clearer. In the romanization we mark it with ´: máma, metró, molokó. Russian does not write the stress and it follows no fixed rule: you learn it with each word.'),
              oye=('метро', 'мир'),
              extras=[fuerza('мама', 'mamá', 'mom', ['MA-ma', 'ma-MA']), fuerza('молоко', 'leche', 'milk', ['mo-lo-KO', 'MO-lo-ko']),
                      fuerza('метро', 'metro', 'subway', ['met-RO', 'MET-ro'])],
              construye=('метро', 'а')),
            L('u06l02', 'О sin acento suena «a»', 'Unstressed О sounds like “a”',
              [W(R('молоко'), 'leche', 'milk', '1f95b'), W(R('вода'), 'agua', 'water', '1f4a7'), W(R('хорошо'), 'bien', 'good; well'), W(R('собака'), 'perro', 'dog', '1f436')],
              (R('молоко'), 'Sin acento, О suena como una «a» corta: молоко ≈ «malakó», вода ≈ «vadá», хорошо ≈ «jarashó». La vocal tónica se alarga y se oye clara; las demás se acortan. En el romanizado se escribe «o», pero se oye «a».',
               'Without stress, О sounds like a short “uh”: молоко ≈ “muh-luh-KOH,” вода ≈ “vuh-DAH,” хорошо ≈ “khuh-ruh-SHOH.” The stressed vowel is longer and clear; the others get short. The romanization writes “o,” but you hear “uh.”'),
              foco='red', par=(R('молоко'), 'мир'), oye=('вода', 'вот'),
              extras=[sig('хорошо', ('bien', 'good; well'), ('mal', 'bad')), toca('red', R('собака'), 'сок'), mezcla('вода', 'agua', 'water')],
              construye=('вода', 'и')),
            L('u06l03', 'Е y Я sin acento suenan «i»', 'Unstressed Е and Я sound like “i”',
              [W(R('язык'), 'idioma; lengua', 'language; tongue'), W(R('река'), 'río', 'river'), W(R('сестра'), 'hermana', 'sister', '1f467'), W(R('телефон'), 'teléfono', 'phone', '260e')],
              (R('язык'), 'Sin acento, Е y Я suenan como una «i» breve: язык ≈ «yizík», река ≈ «riká», телефон ≈ «tilifón». Pero no escribas «i»: sigue escribiendo е y я.',
               'Without stress, Е and Я sound like a short “i”: язык ≈ “yih-ZIK,” река ≈ “rih-KAH,” телефон ≈ “tih-lih-FON.” But do not write “i”: keep writing е and я.'),
              foco='red', par=(R('река'), 'мир'), oye=('река', 'рука'),
              extras=[sig('сестра', ('hermana', 'sister'), ('hermano', 'brother')), sig('язык', ('idioma; lengua', 'language; tongue'), ('río', 'river'))],
              construye=('река', 'о')),
            L('u06l04', 'El acento se mueve', 'Stress moves',
              [W('рука', 'mano', 'hand', '270b'), W('руки', 'manos', 'hands'), W('вода', 'agua', 'water', '1f4a7'), W('воды', 'aguas', 'waters')],
              ('рука', 'En ruso el acento cambia de sílaba según la forma: рука (ruká, mano) pero руки (rúki, manos), вода (vodá, agua) pero воды (vódy, aguas). No hay una regla sencilla: por eso lo marcamos siempre en el romanizado.',
               'In Russian, stress moves between syllables depending on the form: рука (ruká, hand) but руки (rúki, hands), вода (vodá, water) but воды (vódy, waters). There is no simple rule: that is why we always mark it in the romanization.'),
              oye=('рука', 'руки'),
              extras=[fuerza('руки', 'manos', 'hands', ['RU-ki', 'ru-KI']), fuerza('воды', 'aguas', 'waters', ['VO-dy', 'vo-DY']),
                      fuerza('город', 'ciudad', 'city', ['GO-rod', 'go-ROD']), fuerza('города', 'ciudades', 'cities', ['go-ro-DA', 'GO-ro-da'])],
              construye=('руки', 'о')),
        ],
    },
    {
        'id': 'u07', 'titulo': b('R7 · Consonantes blandas, ь y ъ', 'R7 · Soft consonants, ь and ъ'),
        'objetivo': b('Oír la diferencia entre consonante dura y blanda, leer el signo blando ь (también ante vocal: семья) y el signo duro ъ (объём).',
                      'Hear the difference between hard and soft consonants, read the soft sign ь (also before a vowel: семья) and the hard sign ъ (объём).'),
        'lecciones': [
            L('u07l01', 'Duras y blandas', 'Hard and soft',
              [W('лук', 'cebolla', 'onion'), W('(л:bl)юк', 'escotilla', 'hatch'), W('нос', 'nariz', 'nose', '1f443'), W('(н:bl)ёс', 'él llevó', 'he carried')],
              ('(л:bl)юк', 'Casi todas las consonantes rusas tienen dos versiones: dura y blanda. Para ablandar, la parte media de la lengua sube hacia el paladar, como al decir «i». Se ablanda con ь o con я, е, ё, ю, и después de la consonante. Cambia el significado.',
               'Almost every Russian consonant comes in two versions: hard and soft. To soften, the middle of the tongue rises toward the palate, as when saying “ee.” You soften with ь or with я, е, ё, ю, и after the consonant. It changes the meaning.'),
              foco='bl', par=('(л:bl)юк', 'лук'), oye=('люк', 'лук'),
              extras=[cambia('лук', 'люк', ['ю', 'у', 'а']), toca('bl', '(н:bl)ёс', 'нос'), sig('люк', ('escotilla', 'hatch'), ('cebolla', 'onion'))],
              construye=('люк', 'а')),
            L('u07l02', 'El signo blando ь', 'The soft sign ь',
              [W(SB('брат'), 'hermano', 'brother'), W(SB('брать'), 'tomar', 'to take'), W(SB('мать'), 'madre', 'mother', '1f469'), W(SB('день'), 'día', 'day', '2600')],
              (SB('брать'), 'La ь no suena: solo ablanda la consonante anterior. брат (hermano, т dura) ≠ брать (tomar, т blanda); мать (madre), день (día). En el romanizado se escribe con un apóstrofo: brat\' ≠ brat.',
               'The ь does not sound: it only softens the consonant before it. брат (brother, hard т) ≠ брать (to take, soft т); мать (mother), день (day). In the romanization it is written with an apostrophe: brat\' ≠ brat.'),
              foco='mz', par=(SB('брать'), 'брат'), oye=('брать', 'брат'),
              extras=[sig('мать', ('madre', 'mother'), ('hermano', 'brother')), toca('mz', SB('день'), 'дом'), oye('брат', 'брать')],
              construye=('день', 'а')),
            L('u07l03', 'ь antes de vocal', 'ь before a vowel',
              [W(SB('семья'), 'familia', 'family', '1f46a'), W(SB('письмо'), 'carta', 'letter', '1f4e7'), W(SB('платье'), 'vestido', 'dress', '1f457'), W(SB('друзья'), 'amigos', 'friends')],
              (SB('семья'), 'Antes de una vocal, ь suena como una «y» corta que ablanda: семья ≈ «simyá», платье ≈ «plátye». Fíjate: no separa los sonidos, los une en un solo golpe.',
               'Before a vowel, ь sounds like a short “y” that softens: семья ≈ “syem-YAH,” платье ≈ “PLAT-ye.” Notice it does not split the sounds: it joins them in one stroke.'),
              foco='mz', par=(SB('семья'), 'мама'), oye=('семья', 'мама'),
              extras=[sig('семья', ('familia', 'family'), ('amigos', 'friends')), sig('письмо', ('carta', 'letter'), ('libro', 'book')),
                      lee('Ольга', 'Ольга', 'Olga', '¿Cuál es un nombre de persona?', 'Which one is a person’s name?', ['Ольга', 'семья'])],
              construye=('семья', 'о')),
            L('u07l04', 'El signo duro ъ', 'The hard sign ъ',
              [W(K('объём', 'ъ'), 'volumen', 'volume'), W(K('подъезд', 'ъ'), 'entrada (de un edificio)', 'building entrance', '1f6aa'), W(K('объявление', 'ъ'), 'anuncio', 'announcement')],
              (K('подъезд', 'ъ'), 'La ъ es el signo duro, y es muy poco frecuente. No suena: marca una pausa breve entre la consonante y я, е, ё, ю: объём ≈ «abyóm», подъезд ≈ «padyézd». En el romanizado se escribe con una comilla recta: ob"yóm.',
               'The ъ is the hard sign, and it is rare. It does not sound: it marks a tiny pause between the consonant and я, е, ё, ю: объём ≈ “ab-YOM,” подъезд ≈ “pad-YEZD.” In the romanization it is written with a straight quote: ob"yóm.'),
              foco='tz', par=(K('подъезд', 'ъ'), 'подвал'), oye=('съел', 'сел'),
              extras=[sig('съел', ('él comió', 'he ate'), ('él se sentó', 'he sat down')), sig('объём', ('volumen', 'volume'), ('anuncio', 'announcement'))],
              construye=('подъезд', 'о')),
        ],
    },
    {
        'id': 'u08', 'titulo': b('R8 · Ж, ш, щ, ч, ц', 'R8 · Ж, ш, щ, ч, ц'),
        'objetivo': b('Pronunciar las sibilantes: ж, ш y ц son siempre duras; ч y щ son siempre blandas; tras ж, ш y ц la letra и suena como ы.',
                      'Pronounce the hushing sounds: ж, ш and ц are always hard; ч and щ are always soft; after ж, ш and ц the letter и sounds like ы.'),
        'lecciones': [
            L('u08l01', 'Ж, ш, ц: siempre duras', 'Ж, ш, ц: always hard',
              [W('ж(и:y)ть', 'vivir', 'to live'), W('ц(и:y)рк', 'circo', 'circus'), W('маш(и:y)на', 'carro; máquina', 'car; machine', '1f697'), W('ш(и:y)ть', 'coser', 'to sew')],
              ('ж(и:y)ть', 'Ж, Ш y Ц son siempre duras. Por eso, después de ellas, la letra и suena casi como «ы»: жить ≈ «zhyt\'», цирк ≈ «tsyrk», машина ≈ «mashýna». Se escribe «и», pero se oye «ы».',
               'Ж, Ш and Ц are always hard. So after them the letter и sounds almost like ы: жить ≈ “zhyt’,” цирк ≈ “tsyrk,” машина ≈ “mah-SHY-nah.” You write и, but you hear ы.'),
              foco='y', par=('ж(и:y)ть', 'мир'), oye=('цирк', 'мир'),
              extras=[sig('жить', ('vivir', 'to live'), ('coser', 'to sew')), toca('y', 'ц(и:y)рк', 'такси')],
              construye=('жить', 'а')),
            L('u08l02', 'Ч y щ: siempre blandas', 'Ч and щ: always soft',
              [W(K('чай', 'чщ'), 'té', 'tea', '1f375'), W(K('чашка', 'чщ'), 'taza', 'cup'), W(K('щука', 'чщ'), 'lucio', 'pike (fish)', '1f41f'), W(K('ещё', 'чщ'), 'todavía; más', 'still; more')],
              (K('щука', 'чщ'), 'Ч y Щ son siempre blandas: ч es una «ch» suave sin explosión; щ es una «sh» larga y blanda, no «sh» y «ch» separadas. Después de ellas se escribe а o у, no я ni ю: чашка, щука.',
               'Ч and Щ are always soft: ч is a soft “ch” with no burst; щ is a long, soft “sh,” not “sh” and “ch” separately. After them you write а or у, not я or ю: чашка, щука.'),
              foco='shch', par=(K('щука', 'чщ'), K('чай', 'ч')), oye=('щука', 'чашка'),
              extras=[toca('ch', K('чашка', 'чщ'), 'мир'), sig('ещё', ('todavía; más', 'still; more'), ('nunca', 'never'))],
              construye=('чай', 'щ')),
            L('u08l03', 'Contrastes', 'Contrasts',
              [W(K('шар', 'жшчц'), 'globo; esfera', 'balloon; ball', '1f388'), W(K('жар', 'жшчц'), 'calor; fiebre', 'heat; fever'), W(K('чек', 'жшчц'), 'recibo; cheque', 'receipt; check'), W(K('цех', 'жшчц'), 'taller', 'workshop')],
              (K('жар', 'жшчц'), 'Cada una es un sonido propio: ш ≠ ж (шар, жар), ч ≠ ц (чек, цех). Escucha la diferencia: ж es sonora, ш es sorda; ч es suave, ц es dura.',
               'Each one is its own sound: ш ≠ ж (шар, жар), ч ≠ ц (чек, цех). Listen to the difference: ж is voiced, ш is voiceless; ч is soft, ц is hard.'),
              foco='zh', par=(K('жар', 'жшчц'), K('шар', 'шчц')), oye=('шар', 'жар'),
              extras=[oye('жить', 'шить'), oye('чек', 'цех'), cambia('шар', 'жар', ['ж', 'ш', 'щ']), sig('жар', ('calor; fiebre', 'heat; fever'), ('globo', 'balloon'))],
              construye=('шар', 'ж')),
            L('u08l04', 'Palabras de todos los días', 'Everyday words',
              [W(K('хорошо', 'жшщчц'), 'bien', 'good; well'), W(K('пожалуйста', 'жшщчц'), 'por favor; de nada', 'please; you are welcome'), W(K('школа', 'жшщчц'), 'escuela', 'school', '1f3eb'), W(K('шапка', 'жшщчц'), 'gorro', 'hat', '1f9e2')],
              (K('пожалуйста', 'жшщчц'), 'Ahora lee palabras muy usadas con lo que ya sabes: ж = «zh», ш = «sh», х = «j», о sin acento ≈ «a». пожалуйста ≈ «pazháluista».',
               'Now read very common words with what you know: ж = “zh,” ш = “sh,” х = “kh,” unstressed о ≈ “uh.” пожалуйста ≈ “pah-ZHAH-lstah.”'),
              foco='zh', par=(K('пожалуйста', 'жшщчц'), 'мир'), oye=('шапка', 'шар'),
              extras=[sig('школа', ('escuela', 'school'), ('tienda', 'store')), sig('хорошо', ('bien', 'good; well'), ('mal', 'bad'))],
              construye=('школа', 'а')),
        ],
    },
    {
        'id': 'u09', 'titulo': b('R9 · Ensordecimiento y entonación', 'R9 · Devoicing and intonation'),
        'objetivo': b('Oír cómo b, d, g, v, z, zh suenan p, t, k, f, s, sh al final de palabra y ante consonante sorda, y cómo sube la voz en una pregunta de sí o no.',
                      'Hear how b, d, g, v, z, zh sound like p, t, k, f, s, sh at the end of a word and before a voiceless consonant, and how the voice rises in a yes/no question.'),
        'lecciones': [
            L('u09l01', 'Al final de palabra', 'At the end of a word',
              [W('хле(б:ens)', 'pan', 'bread', '1f35e'), W('дру(г:ens)', 'amigo', 'friend', '1f91d'), W('гла(з:ens)', 'ojo', 'eye', '1f441'), W('но(ж:ens)', 'cuchillo', 'knife')],
              ('дру(г:ens)', 'Al final de palabra, las consonantes sonoras se vuelven sordas: б suena «p», д «t», г «k», з «s», ж «sh». Se escribe хлеб, pero suena «jlep»; друг suena «druk»; нож suena «nosh».',
               'At the end of a word, voiced consonants become voiceless: б sounds like “p,” д like “t,” г like “k,” з like “s,” ж like “sh.” You write хлеб but it sounds like “khlep”; друг sounds like “druk”; нож like “nosh.”'),
              foco='ens', par=('дру(г:ens)', 'друга'), oye=('друг', 'друга'),
              extras=[toca('ens', 'хле(б:ens)', 'хлеба'), sig('хлеб', ('pan', 'bread'), ('leche', 'milk')), sig('друг', ('amigo', 'friend'), ('casa', 'house'))],
              construye=('друг', 'а')),
            L('u09l02', 'Ante otra consonante', 'Before another consonant',
              [W('ло(ж:ens)ка', 'cuchara', 'spoon', '1f944'), W('за(в:ens)тра', 'mañana', 'tomorrow'), W('а(в:ens)тобус', 'autobús', 'bus', '1f68c'), W('во(к:son)зал', 'estación de tren', 'train station', '1f686')],
              ('ло(ж:ens)ка', 'El mismo efecto ocurre dentro de la palabra: una sonora ante una sorda se ensordece (ложка ≈ «lóshka», завтра ≈ «záftra», автобус ≈ «aftóbus»). Y al revés, una sorda ante una sonora se sonoriza: вокзал ≈ «vagzál».',
               'The same effect happens inside a word: a voiced sound before a voiceless one becomes voiceless (ложка ≈ “LOSH-ka,” завтра ≈ “ZAF-tra,” автобус ≈ “af-TO-bus”). And the other way around, a voiceless sound before a voiced one becomes voiced: вокзал ≈ “vag-ZAL.”'),
              foco='son', par=('во(к:son)зал', 'мир'), oye=('завтра', 'завод'),
              extras=[toca('ens', 'за(в:ens)тра', 'мир'), sig('завтра', ('mañana', 'tomorrow'), ('ayer', 'yesterday')), sig('вокзал', ('estación de tren', 'train station'), ('aeropuerto', 'airport'))],
              construye=('завтра', 'о')),
            L('u09l03', '¿Es una pregunta?', 'Is it a question?',
              [W('Это стол.', 'esto es una mesa', 'this is a table'), W('Это стол?', '¿es una mesa?', 'is it a table?'), W('Это стул?', '¿es una silla?', 'is it a chair?', '1fa91')],
              ('Это стол?', 'En una pregunta de sí o no, la voz sube sobre la palabra por la que preguntas y luego baja. No sube al final, como en español. En «Это стол?» la voz sube sobre «стол» y cae después. Escucha la diferencia con la afirmación.',
               'In a yes/no question, the voice rises on the word you are asking about and then falls. It does not rise at the end, as in English. In “Это стол?” the voice rises on “стол” and falls afterward. Listen to the difference from the statement.'),
              oye=('Это стол?', 'Это стол.'),
              extras=[lee('Это кот?', '¿Es un gato?', 'Is it a cat?', '¿Sobre qué palabra sube la voz?', 'On which word does the voice rise?', ['кот', 'это']),
                      lee('Это Анна?', '¿Es Anna?', 'Is it Anna?', '¿Sobre qué palabra sube la voz?', 'On which word does the voice rise?', ['Анна', 'это']),
                      lee('Это кофе?', '¿Es café?', 'Is it coffee?', '¿Sobre qué palabra sube la voz?', 'On which word does the voice rise?', ['кофе', 'это'])],
              construye=('стол', 'а')),
            L('u09l04', 'Cortesía de todos los días', 'Everyday politeness',
              [W('Здравствуйте!', 'hola (formal)', 'hello (formal)'), W('Спасибо!', 'gracias', 'thank you'), W('Привет!', 'hola (informal)', 'hi (informal)', '1f44b'), W('До свидания!', 'adiós', 'goodbye')],
              ('Здравствуйте!', 'Algunas letras no suenan: en здравствуйте la «в» no se pronuncia («zdrástvuite»). Y fíjate otra vez en el acento: zdrávstvuyte, spasíbo, privét.',
               'Some letters are silent: in здравствуйте the “в” is not pronounced (“ZDRAH-stvooy-tyeh”). And look at the stress again: zdrávstvuyte, spasíbo, privét.'),
              oye=('спасибо', 'пожалуйста'),
              extras=[lee('Спасибо, Анна!', '¡Gracias, Anna!', 'Thank you, Anna!', '¿Cuál palabra es el nombre de una persona?', 'Which word is a person’s name?', ['Анна', 'Спасибо']),
                      sig('привет', ('hola (informal)', 'hi (informal)'), ('adiós', 'goodbye'))],
              construye=('привет', 'а')),
        ],
    },
    {
        'id': 'u10', 'titulo': b('R10 · Ya puedes empezar', 'R10 · You can start now'),
        'objetivo': b('Comprobar que lees y oyes los sonidos del ruso: carteles, contrastes, palabras nuevas y una primera frase.',
                      'Check that you can read and hear Russian sounds: signs, contrasts, new words and a first sentence.'),
        'lecciones': [
            L('u10l01', 'Lee carteles', 'Read signs',
              [W('ВХОД', 'entrada', 'entrance', '1f6aa'), W('ВЫХОД', 'salida', 'exit'), W('ОТКРЫТО', 'abierto', 'open'), W('ЗАКРЫТО', 'cerrado', 'closed')],
              ('ВХОД · ВЫХОД', 'Los carteles suelen ir en mayúsculas. El sonido no cambia: lee primero la palabra clave, letra por letra.',
               'Signs are often in capitals. The sound does not change: read the key word first, letter by letter.'),
              oye=('выход', 'вход'),
              extras=[lee('ВЫХОД · ВХОД', 'SALIDA · ENTRADA', 'EXIT · ENTRANCE', '¿Qué palabra indica por dónde salir?', 'Which word tells you where to exit?', ['ВЫХОД', 'ВХОД']),
                      lee('ОТКРЫТО', 'abierto', 'open', '¿El lugar está abierto o cerrado?', 'Is the place open or closed?', ['открыто', 'закрыто']),
                      lee('Ролфа', *PSEUDO, *CUAL_INVENTADA, ['школа', 'Ролфа'], 1)],
              construye=('вход', 'а')),
            L('u10l02', 'Carteles de la ciudad', 'City signs',
              [W('МЕТРО', 'metro', 'subway'), W('АПТЕКА', 'farmacia', 'pharmacy'), W('МАГАЗИН', 'tienda', 'store'), W('ТАКСИ', 'taxi', 'taxi')],
              ('МЕТРО · АПТЕКА', 'Estas palabras están en toda ciudad de habla rusa. Lee cada letra con lo que ya sabes: М-Е-Т-Р-О, А-П-Т-Е-К-А.',
               'These words are in every Russian-speaking city. Read each letter with what you know: М-Е-Т-Р-О, А-П-Т-Е-К-А.'),
              oye=('аптека', 'магазин'),
              extras=[lee('АПТЕКА', 'farmacia', 'pharmacy', '¿Dónde compras medicinas?', 'Where do you buy medicine?', ['аптека', 'магазин']),
                      lee('МЕТРО · ТАКСИ', 'METRO · TAXI', 'SUBWAY · TAXI', '¿Qué palabra es un transporte bajo tierra?', 'Which word is underground transport?', ['метро', 'такси']),
                      sig('магазин', ('tienda', 'store'), ('farmacia', 'pharmacy'))],
              nota=('⚠ Falso amigo: магазин significa «tienda», no «revista».', '⚠ False friend: магазин means “store,” not “magazine.”'),
              construye=('аптека', 'о')),
            L('u10l03', 'Contrastes', 'Contrasts',
              [W(K('был', 'ы'), 'fue; estuvo', 'was'), W('бил', 'golpeó', 'hit'), W(SB('брать'), 'tomar', 'to take'), W('брат', 'hermano', 'brother')],
              (K('был', 'ы'), 'Repaso: ы frente a и (был, бил), duras y blandas (брат, брать), ж frente a ш (жар, шар), sonora al final (друг, друга).',
               'Review: ы versus и (был, бил), hard and soft (брат, брать), ж versus ш (жар, шар), voiced at the end (друг, друга).'),
              foco='y', par=(K('был', 'ы'), 'бил'), oye=('был', 'бил'),
              extras=[oye('брать', 'брат'), oye('шар', 'жар'), oye('жить', 'шить'), toca('mz', SB('брать'), 'брат'), toca('ens', 'дру(г:ens)', 'друга')],
              construye=('брат', 'ь')),
            L('u10l04', 'Palabras nuevas', 'New words',
              [W(R('гостиница'), 'hotel', 'hotel', '1f3e8'), W('аэропорт', 'aeropuerto', 'airport', '2708'), W('университет', 'universidad', 'university', '1f3eb'), W('ресторан', 'restaurante', 'restaurant')],
              (R('гостиница'), 'Estas palabras son nuevas, pero ya conoces sus reglas: о y е sin acento se acortan, щ y ж son un solo sonido, ь no suena. Léelas despacio y marca la sílaba fuerte.',
               'These words are new, but you know their rules: unstressed о and е get short, щ and ж are single sounds, ь is silent. Read them slowly and mark the strong syllable.'),
              foco='red', par=(R('гостиница'), 'мир'), oye=('аэропорт', 'автобус'),
              extras=[lee('Зифка', *PSEUDO, *CUAL_INVENTADA, ['Зифка', 'школа']),
                      sig('аэропорт', ('aeropuerto', 'airport'), ('estación de tren', 'train station')),
                      fuerza('ресторан', 'restaurante', 'restaurant', ['res-to-RAN', 'RES-to-ran'])],
              construye=('гостиница', 'о')),
            L('u10l05', 'Tu primera frase', 'Your first sentence',
              [W('Привет!', 'hola', 'hi', '1f44b'), W('Меня зовут Анна.', 'me llamo Anna', 'my name is Anna'), W('Как дела?', '¿cómo estás?', 'how are you?'), W('Хорошо, спасибо!', 'bien, gracias', 'good, thank you!')],
              ('Привет! Меня зовут Анна.', 'Junta todo: lee despacio, con las letras que ya conoces y la fuerza en su sílaba. ¡Ya puedes empezar Fundamentos de ruso!',
               'Put it all together: read slowly, with the letters you know and the stress on its syllable. You are ready for Foundations of Russian!'),
              oye=('привет', 'пока'),
              extras=[lee('До свидания!', '¡Adiós!', 'Goodbye!', '¿Cuál palabra es una despedida?', 'Which word is a goodbye?', ['Здравствуйте', 'До свидания'], 1),
                      deletreo('Максим', 'Escucha y ordena las letras de Максим.', 'Listen and put the letters of Максим in order.')],
              construye=('привет', 'а')),
        ],
    },
]


def nivel0_json():
    return {
        'esquema': 'onelingo.nivel0.v1',
        'idioma': 'ru',
        'titulo': b('Nivel 0 · Leer y pronunciar ruso', 'Level 0 · Read and pronounce Russian'),
        'subtitulo': b('Para quien nunca leyó cirílico: cómo suenan las letras rusas y cómo leerlas.',
                       'For anyone who has never read Cyrillic: how Russian letters sound and how to read them.'),
        'voz': 'narradora',
        'nota': 'Marcado: (letras:sonido) pinta las letras con el color del sonido (ver sonidos.json); _ = letra que no suena. El cirílico no lleva nunca acento combinado: el acento va solo en `rom` (transliteración neutra letra a letra, tilde aguda en la vocal tónica de las palabras de dos o más sílabas). Fuente: tools/contenido/nivel0-ru/generar.py. Apoyo es + en.',
        'textos': {
            'tarjeta': b('¿Nunca leíste cirílico? Cómo suenan las letras rusas y cómo leerlas.', 'Never read Cyrillic? How Russian letters sound and how to read them.'),
            'muestra': '(м:m)(а:a)(м:m)(а:a) · с(ы:y)р · (ж:zh)(и:y)ть',
            'emoji': '1f4d6',
            'junta': b('Escucha despacio y después rápido: así se lee el ruso.', 'Listen slowly, then fast: that is how you read Russian.'),
            'mapaIntro': b('El cirílico se lee casi como suena. Cinco letras son como en español, seis parecen latinas pero suenan distinto (В, Н, Р, С, У, Х), y el resto son nuevas. Lo importante: cada vocal dura tiene una pareja blanda, la ы es una vocal propia, el acento cambia de sílaba y las vocales sin acento se acortan, las consonantes pueden ser blandas y, al final de palabra, se ensordecen. Cada sonido tiene una imagen y un color que verás en las palabras. Toca una tarjeta para oírla.',
                           'Cyrillic is read almost as it sounds. Five letters are as expected, six look Latin but sound different (В, Н, Р, С, У, Х), and the rest are new. What matters: every hard vowel has a soft partner, ы is a vowel of its own, stress moves between syllables and unstressed vowels get short, consonants can be soft and, at the end of a word, they lose their voice. Each sound has a picture and a color you will see in the words. Tap a card to hear it.'),
            'grupos': GRUPOS,
        },
        'revision': 'inicial',
        'refuerzo': {'igual': 'u01', 'falsas': 'u02', 'vocales': 'u03', 'consonantes': 'u04', 'blandas': 'u05',
                     'acento': 'u06', 'signos': 'u07', 'sibilantes': 'u08', 'ensordecimiento': 'u09'},
        'evaluacion': {'lecciones': ['u10l01', 'u10l02', 'u10l03', 'u10l04', 'u10l05'], 'pseudopalabras': ['Ролфа', 'Зифка'], 'umbral': 0.8},
        'unidades': UNIDADES,
    }


def agregar_rom(o):
    """Añade `rom` a todo objeto con texto cirílico en `m` (palabras, opciones y pasos)."""
    if isinstance(o, dict):
        m = o.get('m')
        if isinstance(m, str) and CIRILICO.search(m) and 'rom' not in o:
            o['rom'] = rom(plano(m))
        for v in list(o.values()):
            agregar_rom(v)
    elif isinstance(o, list):
        for v in o:
            agregar_rom(v)


def verificar(texto_json):
    assert '\u0301' not in texto_json, 'U+0301 no permitido'
    assert not re.search(r'\d', ''.join(re.findall(r'"(?:m|audio)": "([^"]*)"', texto_json))), 'cifras en texto que se oye'
    for palabra in re.findall(r'[A-Za-zа-яёА-ЯЁ]+', texto_json):
        if CIRILICO.search(palabra) and re.search(r'[A-Za-z]', palabra):
            raise AssertionError(f'letras latinas y cirílicas mezcladas: {palabra}')


def escribir(nombre, datos):
    texto = json.dumps(datos, ensure_ascii=False, indent=1) + '\n'
    verificar(texto)
    (DESTINO / nombre).write_text(texto, encoding='utf-8')


if __name__ == '__main__':
    DESTINO.mkdir(parents=True, exist_ok=True)
    datos = nivel0_json()
    agregar_rom(datos)
    if FALTAN:
        sys.exit('Faltan en LEX_SRC (añadir con ^ tras la vocal tónica): ' + ' '.join(sorted(FALTAN)))
    escribir('sonidos.json', sonidos_json())
    escribir('nivel0.json', datos)
    r = subprocess.run([sys.executable, str(RAIZ / 'tools/contenido/validar_nivel0.py'), 'ru',
                        str(DESTINO / 'nivel0.json'), '--bilingue'])
    sys.exit(r.returncode)
