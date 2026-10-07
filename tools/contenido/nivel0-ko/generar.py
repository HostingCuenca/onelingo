#!/usr/bin/env python3
"""Genera el Nivel 0 «Leer y pronunciar coreano» (hangul), misma estructura que it/de.

Escribe assets/contenido/ko/nivel0/sonidos.json y nivel0.json desde los datos de
este archivo y termina con `validar_nivel0.py ko --bilingue`.
Apoyo bilingüe {es, en}: español latino neutro con «tú», inglés americano.
Coreano estándar de Seúl; sin historia continua; nombres solo de tools/ia/idiomas/ko.md.
Lumo solo en la bienvenida (u01l01), nunca en la evaluación (u10).
Reglas de pronunciación: solo las guías de tools/ia/idiomas/ko.md (tres series,
ㅓ/ㅗ, ㅡ/ㅜ, ㅐ/ㅔ, ㅇ, 받침, enlace, asimilación básica, ㄹ, ritmo y entonación).
`rom` (Romanización Revisada) lo calcula romanizar.py (probado con los casos de la ficha)
y se añade a cada texto, opción, ficha y letra en hangul.
Marcado: (bloque:sonido) pinta el bloque con el color del sonido (sonidos.json).
En las unidades de vocales el color es el de la vocal; en las de consonantes, el de la
consonante o serie; en 받침, enlace y asimilación, el del cambio que se enseña.
Imágenes: solo emoji Noto ya presentes en assets/img/emoji/.

16 claves (curriculo/ko/f0.json · previos) → unidades:
  hangul-logic, ieung-silent-ng, basic-vowels (ㅏㅣㅗㅜ) u01 · basic-vowels (ㅓㅡㅔㅐ) u02 ·
  basic-consonants, rieul-r-l, lax-voicing u03 · y-vowels, compound-vowels u04 ·
  aspirated-consonants, tense-consonants, three-way-contrast u05 ·
  batchim-seven-sounds (y ㅇ final «ng») u06 · liaison-yeoneum u07 · nasalization u08 ·
  intonation-basic, romanization-rr, lectura de palabras y carteles u09 · prueba de salida u10.

Uso: python3 tools/contenido/nivel0-ko/generar.py
"""
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from romanizar import HANGUL, LI, VO, FI, PROPIOS, rom_texto  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[3]
DESTINO = RAIZ / 'assets/contenido/ko/nivel0'
GRUPO = re.compile(r'\(([^():]+):([^()]+)\)')


def b(es, en):
    return {'es': es, 'en': en}


def plano(m):
    return GRUPO.sub(lambda g: g.group(1), m)


def mk(w, spec):
    """Marca bloque a bloque: mk('나무', 'a u') → (나:a)(무:u); '-' deja el bloque sin marca."""
    toks, i, out = spec.split(), 0, []
    for ch in w:
        if ch == ' ':
            out.append(' ')
            continue
        s = toks[i]
        i += 1
        out.append(ch if s == '-' else f'({ch}:{s})')
    assert i == len(toks), (w, spec)
    return ''.join(out)


def jamos(m):
    """Descompone en letras (jamo) para el ejercicio de ordenar letras."""
    res = []
    for ch in m:
        c = ord(ch) - 0xAC00
        res += [LI[c // 588], VO[(c % 588) // 28]] + ([FI[c % 28]] if c % 28 else [])
    return res


# ── Mapa de sonidos ──────────────────────────────────────────────────────────
# (id, grupo, color, colorNombre es, en, ancla, emoji, nombre es, en, grafías, ejemplos, unidad)
SONIDOS = [
    ('a', 'vocal', '#E24B4A', 'rojo', 'red', '아기', '1f476', 'ㅏ: una «a» clara, como en «casa»', 'ㅏ: a clear “ah,” as in “father”', ['ㅏ'], ['아기', '가구', '나무'], 1),
    ('i', 'vocal', '#E0559B', 'rosa', 'pink', '이', '1f9b7', 'ㅣ: una «i» clara, como en «sí»', 'ㅣ: a clear “ee,” as in “see”', ['ㅣ'], ['이마', '아기', '나이'], 1),
    ('o', 'vocal', '#2E8B57', 'verde', 'green', '고기', '1f357', 'ㅗ: tu «o» española, con los labios redondeados', 'ㅗ: “o” as in “go,” lips rounded', ['ㅗ'], ['고기', '모기', '오이'], 1),
    ('u', 'vocal', '#1E88E5', 'azul', 'blue', '우유', '1f95b', 'ㅜ: tu «u» española, con los labios redondeados', 'ㅜ: “oo” as in “boot,” lips rounded', ['ㅜ'], ['우유', '누구', '구두'], 1),
    ('eu', 'vocal', '#7B1FA2', 'púrpura', 'purple', '구름', '2601', 'ㅡ: una «u» con los labios estirados, sin redondear', 'ㅡ: like “oo” in “good” with the lips spread flat', ['ㅡ'], ['그네', '구름', '그'], 2),
    ('eo', 'vocal', '#E8B923', 'amarillo', 'yellow', '어머니', '1f469', 'ㅓ: una «o» abierta, boca bien abierta y labios sin redondear', 'ㅓ: like “u” in “cup,” mouth wide open, lips unrounded', ['ㅓ'], ['어머니', '거미', '거기'], 2),
    ('e', 'vocal', '#F08A24', 'naranja', 'orange', '개', '1f436', 'ㅔ y ㅐ: una «e» española (solo la escritura los distingue)', 'ㅔ and ㅐ: one “e” as in “bed” (only spelling tells them apart)', ['ㅔ', 'ㅐ'], ['개', '게', '네'], 2),
    ('lisa', 'consonante', '#455A64', 'pizarra', 'slate', '바다', '1f30a', 'ㄱ ㄷ ㅂ ㅈ: consonantes lisas, con poco aire; entre vocales suenan sonoras', 'ㄱ ㄷ ㅂ ㅈ: plain consonants, low air; voiced between vowels', ['ㄱ', 'ㄷ', 'ㅂ', 'ㅈ'], ['바다', '구두', '지도'], 3),
    ('nasal', 'consonante', '#8D6E63', 'café', 'brown', '나무', '1f333', 'ㄴ y ㅁ: «n» y «m», como en español (también al final)', 'ㄴ and ㅁ: “n” and “m,” as in English (also at the end)', ['ㄴ', 'ㅁ'], ['나무', '어머니', '모기'], 1),
    ('ele', 'consonante', '#7CB342', 'lima', 'lime', '라디오', '1f4fb', 'ㄹ: una «r» simple entre vocales, como en «pero»; «l» al final', 'ㄹ: a single tap “r” between vowels; “l” at the end', ['ㄹ'], ['오리', '라디오', '머리'], 3),
    ('ese', 'consonante', '#C0CA33', 'pistacho', 'pistachio', '소', '1f404', 'ㅅ: «s»; ante ㅣ suena entre «s» y «sh»', 'ㅅ: “s”; before ㅣ it sounds between “s” and “sh”', ['ㅅ'], ['소', '사자', '시'], 3),
    ('hache', 'consonante', '#5C6BC0', 'azul lavanda', 'periwinkle', '해', '2600', 'ㅎ: una «h» suave que sí se oye', 'ㅎ: a soft “h” that you do hear', ['ㅎ'], ['해', '하나', '호수'], 3),
    ('mudo', 'consonante', '#9E9E9E', 'gris', 'gray', '아이', '1f9d2', 'ㅇ al inicio de un bloque: no suena', 'ㅇ at the start of a block: silent', ['ㅇ'], ['아이', '오이', '우유'], 1),
    ('ya', 'vocal-y', '#C2185B', 'frambuesa', 'raspberry', '야채', '1f96c', 'ㅑ: «ya»', 'ㅑ: “yah”', ['ㅑ'], ['야구', '야채'], 4),
    ('yeo', 'vocal-y', '#FF7043', 'coral', 'coral', '여우', '1f98a', 'ㅕ: la ㅓ con una «y» delante', 'ㅕ: ㅓ with a “y” in front', ['ㅕ'], ['여기', '여우', '여자'], 4),
    ('yo', 'vocal-y', '#6B8E23', 'oliva', 'olive', '요리', '1f373', 'ㅛ: «yo»', 'ㅛ: “yo”', ['ㅛ'], ['요리', '요가', '교수'], 4),
    ('yu', 'vocal-y', '#00A6A6', 'turquesa', 'teal', '우유', '1f95b', 'ㅠ: «yu»', 'ㅠ: “yoo”', ['ㅠ'], ['우유', '유리', '휴지'], 4),
    ('ye', 'vocal-y', '#795548', 'chocolate', 'chocolate', '시계', '231a', 'ㅖ y ㅒ: «ye»', 'ㅖ and ㅒ: “yeh”', ['ㅖ', 'ㅒ'], ['시계', '예', '얘'], 4),
    ('wa', 'compuesta', '#9C6ADE', 'lila', 'lilac', '사과', '1f34e', 'ㅘ: «wa» (ㅗ + ㅏ)', 'ㅘ: “wah” (ㅗ + ㅏ)', ['ㅘ'], ['사과', '과자', '와'], 4),
    ('we', 'compuesta', '#26A69A', 'verde agua', 'aqua', '돼지', '1f437', 'ㅙ, ㅚ y ㅞ: «we» (solo la escritura los distingue)', 'ㅙ, ㅚ and ㅞ: “weh” (only spelling tells them apart)', ['ㅙ', 'ㅚ', 'ㅞ'], ['돼지', '회사', '왜'], 4),
    ('wo', 'compuesta', '#D4A017', 'dorado', 'gold', '뭐', '2753', 'ㅝ: «wo» (ㅜ + ㅓ)', 'ㅝ: “wuh” (ㅜ + ㅓ)', ['ㅝ'], ['뭐', '샤워'], 4),
    ('wi', 'compuesta', '#D84315', 'teja', 'brick', '귀', '1f442', 'ㅟ: «wi» (ㅜ + ㅣ)', 'ㅟ: “wee” (ㅜ + ㅣ)', ['ㅟ'], ['귀', '쥐', '위'], 4),
    ('ui', 'compuesta', '#3949AB', 'índigo', 'indigo', '의자', '1fa91', 'ㅢ: «ui» (ㅡ + ㅣ)', 'ㅢ: “ui” (ㅡ + ㅣ)', ['ㅢ'], ['의자', '의사', '의미'], 4),
    ('aspirada', 'serie', '#FFB300', 'ámbar', 'amber', '커피', '2615', 'ㅋ ㅌ ㅍ ㅊ: aspiradas, con un soplo fuerte de aire', 'ㅋ ㅌ ㅍ ㅊ: aspirated, with a strong puff of air', ['ㅋ', 'ㅌ', 'ㅍ', 'ㅊ'], ['커피', '코', '포도'], 5),
    ('tensa', 'serie', '#AD1457', 'granate', 'maroon', '토끼', '1f430', 'ㄲ ㄸ ㅃ ㅆ ㅉ: tensas, garganta apretada y sin aire', 'ㄲ ㄸ ㅃ ㅆ ㅉ: tense, tight throat and no air', ['ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ'], ['토끼', '아빠', '꼬리'], 5),
    ('fk', 'final', '#E65100', 'naranja oscuro', 'deep orange', '책', '1f4d6', '받침 ㄱ ㅋ ㄲ: «k» sin soltar el aire', 'Final ㄱ ㅋ ㄲ: “k,” unreleased', ['ㄱ', 'ㅋ', 'ㄲ'], ['책', '밖', '부엌'], 6),
    ('ft', 'final', '#1B5E20', 'verde oscuro', 'dark green', '옷', '1f455', '받침 ㄷ ㅅ ㅆ ㅈ ㅊ ㅌ ㅎ: «t» sin soltar el aire', 'Final ㄷ ㅅ ㅆ ㅈ ㅊ ㅌ ㅎ: “t,” unreleased', ['ㄷ', 'ㅅ', 'ㅆ', 'ㅈ', 'ㅊ', 'ㅌ', 'ㅎ'], ['옷', '꽃', '끝'], 6),
    ('fp', 'final', '#0D47A1', 'azul marino', 'navy', '집', '1f3e0', '받침 ㅂ ㅍ: «p» sin soltar el aire', 'Final ㅂ ㅍ: “p,” unreleased', ['ㅂ', 'ㅍ'], ['집', '앞', '밥'], 6),
    ('fl', 'final', '#00838F', 'cian oscuro', 'dark cyan', '물', '1f4a7', '받침 ㄹ: «l»', 'Final ㄹ: “l”', ['ㄹ'], ['물', '불', '달'], 6),
    ('ng', 'final', '#4E342E', 'café oscuro', 'dark brown', '공', '26bd', '받침 ㅇ: «ng», como en «tango»', 'Final ㅇ: “ng,” as in “sing”', ['ㅇ'], ['공', '강', '방'], 6),
    ('enlace', 'cambio', '#00ACC1', 'cian', 'cyan', '음악', '1f3b5', 'Enlace: la 받침 pasa a la ㅇ vacía siguiente (음악 → eumak)', 'Linking: the final consonant moves to the next empty ㅇ (음악 → eumak)', ['받침 + ㅇ'], ['음악', '한국어', '월요일'], 7),
    ('asim', 'cambio', '#7E57C2', 'violeta', 'violet', '감사합니다', '1f64f', 'Asimilación: la 받침 cambia por el sonido que sigue (합니다 → hamnida)', 'Assimilation: the final changes because of the next sound (합니다 → hamnida)', ['ㅂ + ㄴ → mn', 'ㄱ + ㅁ → ngm', 'ㄴ/ㄹ + ㄹ → ll'], ['감사합니다', '국물', '칠레'], 8),
]

GRUPOS = {
    'vocal': b('Vocales básicas', 'Basic vowels'),
    'consonante': b('Consonantes básicas', 'Basic consonants'),
    'vocal-y': b('Vocales con y', 'Vowels with y'),
    'compuesta': b('Vocales compuestas', 'Compound vowels'),
    'serie': b('Aspiradas y tensas', 'Aspirated and tense'),
    'final': b('Consonantes finales (받침)', 'Final consonants (받침)'),
    'cambio': b('Enlace y asimilación', 'Linking and assimilation'),
}


def sonidos_json():
    return {
        'esquema': 'onelingo.sonidos.v1',
        'idioma': 'ko',
        'nota': 'Mapa de sonidos del coreano estándar de Seúl. El color acompaña siempre al nombre y a la imagen; es una pista de escucha, no una transcripción fonética. Cada ancla y cada ejemplo llevan su romanización (RR) en anclaRom y ejemplosRom.',
        'marcas': {'_': 'letra que no suena', '=': 'varias letras, un sonido'},
        'acento': b('Modelo: coreano estándar de Seúl. El coreano no tiene sílaba fuerte: cada sílaba dura casi lo mismo.',
                    'Model: standard Seoul Korean. Korean has no stressed syllable: every syllable lasts about the same.'),
        'vocales': [
            {'id': i, 'grupo': g, 'color': c, 'colorNombre': b(ces, cen), 'ancla': a, 'anclaRom': rom_texto(a),
             'emoji': e, 'nombre': b(nes, nen), 'grafias': gr, 'ejemplos': ej,
             'ejemplosRom': [rom_texto(x) for x in ej], 'unidad': u}
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
TOCA = b('Escucha y toca la palabra que lleva la marca de color indicada.',
         'Listen and tap the word that carries the marked color.')
CUAL_INVENTADA = ('¿Cuál es la palabra inventada?', 'Which word is made up?')
PSEUDO = ('Pseudopalabra: no significa nada; léela con las reglas vistas.', 'Pseudoword: it means nothing; read it with the rules you know.')


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


def deletreo(m, es, en):
    return {'tipo': 'deletreo', 'm': m, 'pregunta': b(es, en), 'opciones': jamos(m), 'correcta': 0}


def mezcla(m, es, en):
    return {'tipo': 'mezcla', 'm': m, 't': b(es, en)}


def oye(correcta, otra, inv=False):
    return {'tipo': 'escucha_elige', 'audio': plano(correcta), 'pregunta': ESCUCHA_ELIGE,
            'opciones': [{'m': correcta}, {'m': otra}] if not inv else [{'m': otra}, {'m': correcta}],
            'correcta': 1 if inv else 0}


def toca(foco, si, no, inv=False):
    ops = [{'m': si}, {'m': no}]
    if inv:
        ops.reverse()
    return {'tipo': 'toca_sonido', 'sonido': foco, 'pregunta': TOCA, 'opciones': ops, 'correcta': 1 if inv else 0}


def sig(m, pes, pen):
    """Atajo para «¿Qué significa?» con dos opciones (la primera es la correcta)."""
    return significado(m, '¿Qué significa?', 'What does it mean?', [pes, pen])


def rr(m, tes, ten, ops):
    """¿Cuál es la romanización? (la primera opción es la correcta)."""
    return lee(m, tes, ten, '¿Cuál es su romanización?', 'Which is its romanization?', ops)


UNIDADES = [
    # ─────────────────────────────────────────────────────────────────────────
    {
        'id': 'u01', 'titulo': b('K1 · 안녕 (annyeong): las sílabas son bloques', 'K1 · 안녕 (annyeong): syllables are blocks'),
        'objetivo': b('Entender que el hangul se escribe en bloques de sílaba y leer las primeras palabras con ㅇ, ㄱ, ㄴ, ㅁ y las vocales ㅏ, ㅣ, ㅗ, ㅜ.',
                      'See that hangul is written in syllable blocks and read your first words with ㅇ, ㄱ, ㄴ, ㅁ and the vowels ㅏ, ㅣ, ㅗ, ㅜ.'),
        'lecciones': [
            L('u01l01', 'Un alfabeto de bloques', 'An alphabet of blocks',
              [W(mk('아이', 'a i'), 'niño; niña', 'child', '1f9d2'), W(mk('오이', 'o i'), 'pepino', 'cucumber'), W(mk('나무', 'a u'), 'árbol', 'tree', '1f333')],
              (mk('아이', 'a i'), 'El hangul se escribe en bloques: cada bloque es una sílaba y junta una consonante y una vocal. En 아 (a), la ㅇ del inicio no suena y la vocal ㅏ suena «a». Se lee de izquierda a derecha y de arriba abajo: 아이 (ai) = «a-i». Si aprendes pocas piezas, podrás leer muchísimas palabras.',
               'Hangul is written in blocks: each block is one syllable and joins a consonant and a vowel. In 아 (a), the ㅇ at the start is silent and the vowel ㅏ sounds “ah.” Read left to right and top to bottom: 아이 (ai) = “ah-ee.” Learn a few pieces and you can read a huge number of words.'),
              foco='a', par=(mk('아이', 'a i'), mk('오이', 'o i')), oye=('아이', '오이'),
              extras=[
                  {'tipo': 'lumo', 'pose': 'anima', 'texto': b('Bienvenido al coreano. Primero escucharás, después leerás. ¡Cada sonido tiene un color que te ayuda a recordarlo!',
                                                              'Welcome to Korean. First you listen, then you read. Each sound has a color that helps you remember it!')},
                  sig('아이', ('niño; niña', 'child'), ('árbol', 'tree')),
              ],
              construye=('아이', '오')),
            L('u01l02', 'La ㅇ vacía, ㅏ y ㅣ', 'The empty ㅇ, ㅏ and ㅣ',
              [W(mk('아기', 'mudo -'), 'bebé', 'baby', '1f476'), W(mk('이마', 'mudo -'), 'frente', 'forehead'), W(mk('아니', 'mudo -'), 'no', 'no')],
              (mk('이마', 'mudo -'), 'La ㅇ al inicio de un bloque no suena: solo ocupa el lugar de la consonante para que la vocal tenga su bloque. 이마 (ima) = «i-ma». ㅏ (a) y ㅣ (i) son vocales verticales: van a la derecha de la consonante. ㄴ (n) es «n» y ㅁ (m) es «m». ㄱ (g) es suave, entre «g» y «k»; entre vocales suena «g»: 아기 (agi).',
               'The ㅇ at the start of a block is silent: it only holds the place of the consonant so the vowel gets its own block. 이마 (ima) = “ee-mah.” ㅏ (a) and ㅣ (i) are vertical vowels: they go to the right of the consonant. ㄴ (n) is “n” and ㅁ (m) is “m.” ㄱ (g) is soft, between “g” and “k”; between vowels it sounds “g”: 아기 (agi).'),
              foco='mudo', par=(mk('아기', 'mudo -'), '가구'), oye=('아기', '아니'), inv=True,
              extras=[mezcla('아기', 'bebé', 'baby'), sig('이마', ('frente', 'forehead'), ('mano', 'hand'))],
              construye=('아기', '마')),
            L('u01l03', 'ㅗ y ㅜ: las vocales de abajo', 'ㅗ and ㅜ: the vowels below',
              [W(mk('고기', 'o i'), 'carne', 'meat', '1f357'), W(mk('누구', 'u u'), 'quién', 'who'), W(mk('이모', 'i o'), 'tía (hermana de la mamá)', 'aunt (mother’s sister)')],
              (mk('고기', 'o i'), 'ㅗ (o) y ㅜ (u) son vocales horizontales: van debajo de la consonante. ㅗ es tu «o» española y ㅜ es tu «u» española, con los labios redondeados. 고기 (gogi) = «go-gi»; 누구 (nugu) = «nu-gu».',
               'ㅗ (o) and ㅜ (u) are horizontal vowels: they go below the consonant. ㅗ is “o” as in “go” and ㅜ is “oo” as in “boot,” with rounded lips. 고기 (gogi) = “go-gee”; 누구 (nugu) = “noo-goo.”'),
              foco='o', par=(mk('고기', 'o i'), mk('누구', 'u u')), oye=('고기', '누구'),
              extras=[toca('u', mk('누구', 'u u'), mk('고기', 'o i')), sig('고기', ('carne', 'meat'), ('árbol', 'tree'))],
              construye=('누구', '모')),
            L('u01l04', 'Primeras palabras', 'First words',
              [W(mk('가구', 'a u'), 'mueble', 'furniture'), W(mk('고구마', 'o u a'), 'camote; batata', 'sweet potato'), W(mk('나이', 'a i'), 'edad', 'age')],
              (mk('고구마', 'o u a'), 'Ya lees palabras reales: 가구 (gagu), 고구마 (goguma), 나이 (nai). Cada vocal suena siempre igual y todas las sílabas duran casi lo mismo: en coreano no hay una sílaba «fuerte».',
               'You can already read real words: 가구 (gagu), 고구마 (goguma), 나이 (nai). Each vowel always sounds the same and every syllable lasts about the same: Korean has no “stressed” syllable.'),
              foco='a', par=(mk('나이', 'a i'), mk('고기', 'o i')), oye=('나이', '나무'), inv=True,
              extras=[lee('가구 · 나이 · 고구마', 'mueble · edad · camote', 'furniture · age · sweet potato', '¿Cuál palabra significa «edad»?', 'Which word means “age”?', ['나이', '가구']),
                      deletreo('나무', 'Escucha y ordena las letras de 나무 (namu).', 'Listen and put the letters of 나무 (namu) in order.'),
                      sig('고구마', ('camote; batata', 'sweet potato'), ('mueble', 'furniture'))],
              construye=('고구마', '기')),
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    {
        'id': 'u02', 'titulo': b('K2 · Más vocales: ㅓ, ㅡ, ㅔ y ㅐ', 'K2 · More vowels: ㅓ, ㅡ, ㅔ and ㅐ'),
        'objetivo': b('Distinguir ㅓ de ㅗ y ㅡ de ㅜ, y leer ㅔ y ㅐ como una «e» (solo la escritura los separa).',
                      'Tell ㅓ from ㅗ and ㅡ from ㅜ, and read ㅔ and ㅐ as one “e” (only spelling tells them apart).'),
        'lecciones': [
            L('u02l01', 'ㅓ (eo) no es ㅗ (o)', 'ㅓ (eo) is not ㅗ (o)',
              [W(mk('거기', 'eo i'), 'allí', 'there'), W(mk('거미', 'eo i'), 'araña', 'spider', '1f577'), W(mk('어머니', 'eo eo i'), 'madre', 'mother', '1f469')],
              (mk('거기', 'eo i'), 'ㅓ (eo) es una «o» abierta: boca bien abierta y labios sin redondear (≈ la «o» de «hot» en inglés). ㅗ (o) es tu «o» española, con los labios redondeados. 거기 (geogi, «allí») ≠ 고기 (gogi, «carne»): solo cambia la vocal.',
               'ㅓ (eo) is like the “u” in “cup,” with the mouth wide open and the lips unrounded. ㅗ (o) is like “o” in “go,” with rounded lips. 거기 (geogi, “there”) ≠ 고기 (gogi, “meat”): only the vowel changes.'),
              foco='eo', par=(mk('거기', 'eo i'), mk('고기', 'o i')), oye=('거기', '고기'),
              extras=[toca('o', mk('고기', 'o i'), mk('거기', 'eo i')), cambia('거기', '고기', ['고', '거', '구']),
                      sig('거미', ('araña', 'spider'), ('mosquito', 'mosquito'))],
              construye=('거미', '모')),
            L('u02l02', 'ㅡ (eu) no es ㅜ (u)', 'ㅡ (eu) is not ㅜ (u)',
              [W(mk('그네', 'eu e'), 'columpio', 'swing'), W(mk('구', 'u'), 'nueve', 'nine'), W(mk('그', 'eu'), 'ese; aquel', 'that')],
              (mk('그', 'eu'), 'ㅡ (eu): labios estirados y planos, sin redondear; no es «i» ni «u». ㅜ (u) lleva los labios redondeados. 구 (gu, «nueve») ≠ 그 (geu, «ese»).',
               'ㅡ (eu): the lips are spread flat, like the “oo” in “good” without rounding them. ㅜ (u) has rounded lips, like “oo” in “boot.” 구 (gu, “nine”) ≠ 그 (geu, “that”).'),
              foco='eu', par=(mk('그네', 'eu e'), mk('고기', 'o i')), oye=('구', '그'), inv=True,
              extras=[toca('u', mk('구', 'u'), mk('그', 'eu')), cambia('구', '그', ['그', '구', '고']),
                      sig('그네', ('columpio', 'swing'), ('árbol', 'tree'))],
              construye=('그네', '구')),
            L('u02l03', 'ㅔ y ㅐ: dos letras, una «e»', 'ㅔ and ㅐ: two letters, one “e”',
              [W(mk('네', 'e'), 'sí', 'yes'), W(mk('개', 'e'), 'perro', 'dog', '1f436'), W(mk('게', 'e'), 'cangrejo', 'crab')],
              (mk('개', 'e'), 'ㅐ (ae) y ㅔ (e) hoy suenan casi igual: una «e» española. Solo la escritura los distingue: 개 (gae, «perro») y 게 (ge, «cangrejo»). Es un dato de escritura: no se oye, así que no hay que adivinarlo de oído.',
               'ㅐ (ae) and ㅔ (e) sound almost the same today: one “e” as in “bed.” Only spelling tells them apart: 개 (gae, “dog”) and 게 (ge, “crab”). It is a spelling fact: you cannot hear it, so there is nothing to guess by ear.'),
              foco='e', par=(mk('개', 'e'), mk('고', 'o')), oye=('개', '고'),
              extras=[sig('개', ('perro', 'dog'), ('cangrejo', 'crab')), sig('게', ('cangrejo', 'crab'), ('perro', 'dog')),
                      mezcla('네', 'sí', 'yes')],
              construye=('그네', '개')),
            L('u02l04', 'Seis vocales y una «e»', 'Six vowels and one “e”',
              [W(mk('어머니', 'eo eo i'), 'madre', 'mother', '1f469'), W(mk('모기', 'o i'), 'mosquito', 'mosquito'), W(mk('가게', 'a e'), 'tienda', 'shop')],
              (mk('어머니', 'eo eo i'), 'Ya conoces las vocales básicas: ㅏ (a), ㅓ (eo), ㅗ (o), ㅜ (u), ㅡ (eu), ㅣ (i) y la «e» de ㅔ/ㅐ. Lee con calma: 어머니 (eomeoni) = «eo-meo-ni».',
               'You already know the basic vowels: ㅏ (a), ㅓ (eo), ㅗ (o), ㅜ (u), ㅡ (eu), ㅣ (i) and the “e” of ㅔ/ㅐ. Read calmly: 어머니 (eomeoni) = “uh-muh-nee.”'),
              foco='eo', par=(mk('어머니', 'eo eo i'), mk('모기', 'o i')), oye=('모기', '무기'), inv=True,
              extras=[lee('어머니 · 모기 · 가게', 'mamá · mosquito · tienda', 'mom · mosquito · shop', '¿Cuál palabra significa «tienda»?', 'Which word means “shop”?', ['가게', '모기']),
                      cambia('모기', '무기', ['무', '모', '마']), sig('모기', ('mosquito', 'mosquito'), ('tienda', 'shop'))],
              construye=('가게', '이')),
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    {
        'id': 'u03', 'titulo': b('K3 · Consonantes básicas y la ㄹ', 'K3 · Basic consonants and ㄹ'),
        'objetivo': b('Leer ㄷ, ㅂ, ㅅ, ㅈ, ㅎ y ㄹ; saber que ㄱ, ㄷ, ㅂ y ㅈ suenan sonoras entre vocales y que la ㄹ es una «r» simple.',
                      'Read ㄷ, ㅂ, ㅅ, ㅈ, ㅎ and ㄹ; know that ㄱ, ㄷ, ㅂ and ㅈ sound voiced between vowels and that ㄹ is a single-tap “r.”'),
        'lecciones': [
            L('u03l01', 'ㄱ ㄷ ㅂ ㅈ: las lisas', 'ㄱ ㄷ ㅂ ㅈ: the plain ones',
              [W(mk('바다', 'lisa lisa'), 'mar', 'sea', '1f30a'), W(mk('구두', 'lisa lisa'), 'zapatos', 'shoes', '1f45e'), W(mk('지도', 'lisa lisa'), 'mapa', 'map', '1f5fa')],
              (mk('바다', 'lisa lisa'), 'ㄱ (g), ㄷ (d), ㅂ (b) y ㅈ (j) son consonantes lisas: suaves, con poco aire. Al inicio suenan entre «k/g», «t/d», «p/b» y «ch/y»; entre vocales suenan sonoras: 바다 (bada) ≈ «bada», 아기 (agi) ≈ «agui». Por eso la romanización las escribe g, d, b, j.',
               'ㄱ (g), ㄷ (d), ㅂ (b) and ㅈ (j) are plain consonants: soft, with little air. At the start they sound between “k/g,” “t/d,” “p/b” and “ch/j”; between vowels they sound voiced: 바다 (bada) ≈ “bah-dah,” 아기 (agi) ≈ “ah-gee.” That is why romanization writes them g, d, b, j.'),
              foco='lisa', par=(mk('바다', 'lisa lisa'), mk('어머니', 'eo eo i')), oye=('구두', '고기'), inv=True,
              extras=[sig('바다', ('mar', 'sea'), ('árbol', 'tree')), sig('구두', ('zapatos', 'shoes'), ('mueble', 'furniture'))],
              construye=('지도', '구')),
            L('u03l02', 'ㅅ y ㅎ', 'ㅅ and ㅎ',
              [W(mk('소', 'ese'), 'vaca', 'cow', '1f404'), W(mk('사자', 'ese lisa'), 'león', 'lion'), W(mk('해', 'hache'), 'sol', 'sun', '2600')],
              (mk('시', 'ese'), 'ㅅ (s) suena «s». Antes de ㅣ suena entre «s» y «sh»: 시 (si) ≈ «shi», pero se escribe «si» y no cambia el significado. ㅎ (h) es una «h» suave que sí se oye; no es la «h» muda del español.',
               'ㅅ (s) sounds like “s.” Before ㅣ it sounds between “s” and “sh”: 시 (si) ≈ “shee,” but it is written “si” and the meaning does not change. ㅎ (h) is a soft “h” that you do hear, like the “h” in “hat.”'),
              foco='ese', par=(mk('소', 'ese'), mk('해', 'hache')), oye=('소', '해'),
              extras=[toca('hache', mk('해', 'hache'), mk('소', 'ese')), sig('사자', ('león', 'lion'), ('pato', 'duck'))],
              construye=('사자', '소')),
            L('u03l03', 'ㄹ: una «r» simple', 'ㄹ: a single-tap “r”',
              [W(mk('오리', '- ele'), 'pato', 'duck', '1f986'), W(mk('나라', 'nasal ele'), 'país', 'country'), W(mk('라디오', 'ele lisa -'), 'radio', 'radio', '1f4fb'), W(mk('머리', 'nasal ele'), 'cabeza', 'head')],
              (mk('오리', '- ele'), 'ㄹ (r) entre vocales es una «r» simple, un solo toque de lengua, como en «pero»: 오리 (ori) = «o-ri». Al inicio de una palabra suena entre «r» y «l» (라디오, radio). Nunca es la «rr» vibrante del español. Al final de una sílaba suena «l»; lo verás pronto.',
               'ㄹ (r) between vowels is a single tap of the tongue, like the middle of “butter”: 오리 (ori) = “oh-ree.” At the start of a word it sounds between “r” and “l” (라디오, radio). It is never the rolled “rr” of Spanish. At the end of a syllable it sounds like “l”; you will see that soon.'),
              foco='ele', par=(mk('오리', '- ele'), mk('소', 'ese')), oye=('오리', '오이'), inv=True,
              extras=[sig('나라', ('país', 'country'), ('mar', 'sea')), mezcla('머리', 'cabeza', 'head')],
              construye=('오리', '라')),
            L('u03l04', 'Palabras con todas las consonantes', 'Words with all the consonants',
              [W(mk('아버지', '- lisa lisa'), 'papá', 'father'), W(mk('모자', 'nasal lisa'), 'gorra; sombrero', 'cap; hat', '1f9e2'), W(mk('바나나', 'lisa nasal nasal'), 'banana', 'banana', '1f34c'), W(mk('지구', 'lisa lisa'), 'Tierra (el planeta)', 'Earth', '1f30d')],
              (mk('아버지', '- lisa lisa'), 'Ya conoces las consonantes ㄱ, ㄴ, ㄷ, ㄹ, ㅁ, ㅂ, ㅅ, ㅈ y ㅎ, más la ㅇ muda. Lee con calma: 아버지 (abeoji) = «a-beo-ji». Todas las sílabas duran casi lo mismo.',
               'You already know the consonants ㄱ (g), ㄴ (n), ㄷ (d), ㄹ (r), ㅁ (m), ㅂ (b), ㅅ (s), ㅈ (j) and ㅎ (h), plus the silent ㅇ. Read calmly: 아버지 (abeoji) = “ah-buh-jee.” Every syllable lasts about the same.'),
              foco='lisa', par=(mk('아버지', '- lisa lisa'), mk('나라', 'nasal ele')), oye=('바나나', '바다'),
              extras=[lee('아버지 · 모자 · 지구', 'papá · gorra · Tierra', 'dad · cap · Earth', '¿Cuál palabra significa «Tierra»?', 'Which word means “Earth”?', ['지구', '모자']),
                      sig('바나나', ('banana', 'banana'), ('manzana', 'apple'))],
              construye=('아버지', '모')),
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    {
        'id': 'u04', 'titulo': b('K4 · Vocales con y y vocales compuestas', 'K4 · Vowels with y and compound vowels'),
        'objetivo': b('Leer ㅑ, ㅕ, ㅛ, ㅠ, ㅖ y las vocales compuestas ㅘ, ㅝ, ㅟ, ㅢ, ㅙ, ㅚ y ㅞ.',
                      'Read ㅑ, ㅕ, ㅛ, ㅠ, ㅖ and the compound vowels ㅘ, ㅝ, ㅟ, ㅢ, ㅙ, ㅚ and ㅞ.'),
        'lecciones': [
            L('u04l01', 'ㅑ (ya) y ㅕ (yeo)', 'ㅑ (ya) and ㅕ (yeo)',
              [W(mk('야구', 'ya u'), 'béisbol', 'baseball'), W(mk('여기', 'yeo i'), 'aquí', 'here'), W(mk('여우', 'yeo u'), 'zorro', 'fox', '1f98a')],
              (mk('여기', 'yeo i'), 'La «y» se añade con una raya más: ㅏ (a) → ㅑ (ya) y ㅓ (eo) → ㅕ (yeo). ㅑ suena «ya»; ㅕ es la ㅓ con una «y» delante. 여기 (yeogi) = «yeo-gi»; 야구 (yagu) = «ya-gu».',
               'The “y” is added with one extra stroke: ㅏ (a) → ㅑ (ya) and ㅓ (eo) → ㅕ (yeo). ㅑ sounds “yah”; ㅕ is ㅓ with a “y” in front. 여기 (yeogi) = “yuh-gee”; 야구 (yagu) = “yah-goo.”'),
              foco='yeo', par=(mk('여기', 'yeo i'), mk('야구', 'ya u')), oye=('여기', '거기'),
              extras=[toca('ya', mk('야구', 'ya u'), mk('여기', 'yeo i')), sig('여우', ('zorro', 'fox'), ('perro', 'dog'))],
              construye=('여기', '야')),
            L('u04l02', 'ㅛ (yo) y ㅠ (yu)', 'ㅛ (yo) and ㅠ (yu)',
              [W(mk('요리', 'yo ele'), 'cocina (el arte de cocinar)', 'cooking', '1f373'), W(mk('우유', 'u yu'), 'leche', 'milk', '1f95b'), W(mk('유리', 'yu ele'), 'vidrio', 'glass')],
              (mk('우유', 'u yu'), 'ㅗ (o) → ㅛ (yo) y ㅜ (u) → ㅠ (yu): también con una raya más. ㅛ suena «yo» y ㅠ suena «yu». 우유 (uyu) = «u-yu»; 요리 (yori) = «yo-ri».',
               'ㅗ (o) → ㅛ (yo) and ㅜ (u) → ㅠ (yu): also with one extra stroke. ㅛ sounds “yo” and ㅠ sounds “yoo.” 우유 (uyu) = “oo-yoo”; 요리 (yori) = “yo-ree.”'),
              foco='yu', par=(mk('우유', 'u yu'), mk('요리', 'yo ele')), oye=('우유', '우리'), inv=True,
              extras=[toca('yo', mk('요리', 'yo ele'), mk('우유', 'u yu')), cambia('우유', '우리', ['리', '유', '우']),
                      sig('우유', ('leche', 'milk'), ('vidrio', 'glass'))],
              construye=('우유', '요')),
            L('u04l03', 'ㅘ ㅝ ㅟ ㅢ', 'ㅘ ㅝ ㅟ ㅢ',
              [W(mk('사과', 'ese wa'), 'manzana', 'apple', '1f34e'), W(mk('뭐', 'wo'), 'qué', 'what', '2753'), W(mk('귀', 'wi'), 'oreja', 'ear', '1f442'), W(mk('의자', 'ui lisa'), 'silla', 'chair', '1fa91')],
              (mk('사과', 'ese wa'), 'Las vocales compuestas deslizan una vocal en la otra: ㅗ + ㅏ = ㅘ (wa); ㅜ + ㅓ = ㅝ (wo); ㅜ + ㅣ = ㅟ (wi); ㅡ + ㅣ = ㅢ (ui). 사과 (sagwa) = «sa-gwa»; 귀 (gwi) = «gwi».',
               'Compound vowels slide one vowel into the other: ㅗ + ㅏ = ㅘ (wa); ㅜ + ㅓ = ㅝ (wo); ㅜ + ㅣ = ㅟ (wi); ㅡ + ㅣ = ㅢ (ui). 사과 (sagwa) = “sah-gwah”; 귀 (gwi) = “gwee.”'),
              foco='wa', par=(mk('사과', 'ese wa'), mk('귀', 'wi')), oye=('귀', '구'),
              extras=[toca('wi', mk('귀', 'wi'), mk('사과', 'ese wa')), sig('사과', ('manzana', 'apple'), ('oreja', 'ear')),
                      sig('의자', ('silla', 'chair'), ('mesa', 'table'))],
              construye=('사과', '귀')),
            L('u04l04', 'ㅖ y ㅙ ㅚ ㅞ: dato de escritura', 'ㅖ and ㅙ ㅚ ㅞ: a spelling fact',
              [W(mk('시계', 'ese ye'), 'reloj', 'clock; watch', '231a'), W(mk('돼지', 'we lisa'), 'cerdo', 'pig', '1f437'), W(mk('왜', 'we'), 'por qué', 'why'), W(mk('회사', 'we ese'), 'empresa', 'company')],
              (mk('돼지', 'we lisa'), 'ㅙ (wae), ㅚ (oe) y ㅞ (we) se leen casi igual: una «we». Solo la escritura los distingue: 돼지 (dwaeji), 회사 (hoesa), 스웨터 (seuweteo, «suéter»). Es un dato de escritura, como ㅐ y ㅔ. ㅖ (ye) suena «ye»: 시계 (sigye).',
               'ㅙ (wae), ㅚ (oe) and ㅞ (we) are read almost the same: one “we.” Only spelling tells them apart: 돼지 (dwaeji), 회사 (hoesa), 스웨터 (seuweteo, “sweater”). It is a spelling fact, like ㅐ and ㅔ. ㅖ (ye) sounds “ye”: 시계 (sigye).'),
              foco='we', par=(mk('돼지', 'we lisa'), mk('시계', 'ese ye')), oye=('돼지', '대지'), inv=True,
              extras=[toca('ye', mk('시계', 'ese ye'), mk('돼지', 'we lisa')), sig('돼지', ('cerdo', 'pig'), ('gato', 'cat')),
                      sig('시계', ('reloj', 'clock; watch'), ('silla', 'chair'))],
              construye=('시계', '돼')),
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    {
        'id': 'u05', 'titulo': b('K5 · Tres series: lisas, aspiradas y tensas', 'K5 · Three series: plain, aspirated and tense'),
        'objetivo': b('Oír y pronunciar la diferencia entre ㄱ/ㅋ/ㄲ, ㄷ/ㅌ/ㄸ, ㅂ/ㅍ/ㅃ y ㅈ/ㅊ/ㅉ, que cambia el significado.',
                      'Hear and say the difference between ㄱ/ㅋ/ㄲ, ㄷ/ㅌ/ㄸ, ㅂ/ㅍ/ㅃ and ㅈ/ㅊ/ㅉ, which changes the meaning.'),
        'lecciones': [
            L('u05l01', 'Aspiradas: ㅋ ㅌ ㅍ ㅊ', 'Aspirated: ㅋ ㅌ ㅍ ㅊ',
              [W(mk('커피', 'aspirada aspirada'), 'café', 'coffee', '2615'), W(mk('코', 'aspirada'), 'nariz', 'nose', '1f443'), W(mk('포도', 'aspirada lisa'), 'uva', 'grape', '1f347'), W(mk('토마토', 'aspirada nasal aspirada'), 'tomate', 'tomato', '1f345')],
              (mk('커피', 'aspirada aspirada'), 'ㅋ (k), ㅌ (t), ㅍ (p) y ㅊ (ch) llevan un soplo fuerte de aire, como la «k», «t», «p» y «ch» del inglés al inicio de una palabra (kite, top). Pon la mano frente a la boca: debe sentirse el aire. 커피 (keopi) = «keo-pi».',
               'ㅋ (k), ㅌ (t), ㅍ (p) and ㅊ (ch) carry a strong puff of air, like English “k,” “t,” “p” and “ch” at the start of a word (kite, top). Put your hand in front of your mouth: you should feel the air. 커피 (keopi) = “kuh-pee.”'),
              foco='aspirada', par=(mk('커피', 'aspirada aspirada'), mk('바다', 'lisa lisa')), oye=('포도', '보도'),
              extras=[sig('포도', ('uva', 'grape'), ('banana', 'banana')), sig('커피', ('café', 'coffee'), ('leche', 'milk'))],
              construye=('토마토', '포')),
            L('u05l02', 'Tensas: ㄲ ㄸ ㅃ ㅆ ㅉ', 'Tense: ㄲ ㄸ ㅃ ㅆ ㅉ',
              [W(mk('토끼', 'aspirada tensa'), 'conejo', 'rabbit', '1f430'), W(mk('아빠', '- tensa'), 'papá (informal)', 'dad (informal)', '1f468'), W(mk('아저씨', '- lisa tensa'), 'señor (un hombre adulto)', 'mister (an adult man)'), W(mk('꼬리', 'tensa ele'), 'cola', 'tail')],
              (mk('아빠', '- tensa'), 'ㄲ (kk), ㄸ (tt), ㅃ (pp), ㅆ (ss) y ㅉ (jj) se dicen con la garganta apretada, sin aire, más cortas e intensas. No existen en español: se parecen a la «k», «t» y «p» españolas muy secas. 빠 (ppa) ≈ «ppa» seco; 아빠 (appa) = «a-ppa».',
               'ㄲ (kk), ㄸ (tt), ㅃ (pp), ㅆ (ss) and ㅉ (jj) are said with a tight throat and no air, shorter and sharper. They do not exist in English: they are like “k,” “t” and “p” made very dry. 빠 (ppa) ≈ a dry “ppa”; 아빠 (appa) = “ah-ppa.”'),
              foco='tensa', par=(mk('아빠', '- tensa'), mk('코', 'aspirada')), oye=('아빠', '아파'), inv=True,
              extras=[toca('aspirada', mk('코', 'aspirada'), mk('아빠', '- tensa')), sig('토끼', ('conejo', 'rabbit'), ('zorro', 'fox')),
                      mezcla('꼬리', 'cola', 'tail')],
              construye=('아빠', '꼬')),
            L('u05l03', 'Tres sonidos, tres palabras', 'Three sounds, three words',
              [W('자다 (자요)', 'dormir', 'to sleep', '1f634'), W('차다 (차요)', 'estar frío', 'to be cold'), W('짜다 (짜요)', 'ser salado', 'to be salty')],
              (mk('자다', 'lisa lisa'), 'Los tres sonidos cambian el significado: ㅈ (j) es lisa, con poco aire; ㅊ (ch) es aspirada, con un soplo de aire; ㅉ (jj) es tensa, con la garganta apretada. 자다 (jada, «dormir») ≠ 차다 (chada, «estar frío») ≠ 짜다 (jjada, «ser salado»).',
               'The three sounds change the meaning: ㅈ (j) is plain, with little air; ㅊ (ch) is aspirated, with a puff of air; ㅉ (jj) is tense, with a tight throat. 자다 (jada, “to sleep”) ≠ 차다 (chada, “to be cold”) ≠ 짜다 (jjada, “to be salty”).'),
              foco='tensa', par=(mk('짜다', 'tensa lisa'), mk('차다', 'aspirada lisa')), oye=('자다', '짜다'),
              extras=[oye('차다', '짜다'), toca('aspirada', mk('차다', 'aspirada lisa'), mk('자다', 'lisa lisa')),
                      sig('짜다', ('ser salado', 'to be salty'), ('dormir', 'to sleep'))],
              construye=('자다', '짜')),
            L('u05l04', 'Más pares que cambian el significado', 'More pairs that change the meaning',
              [W(mk('비', 'lisa'), 'lluvia', 'rain', '1f327'), W(mk('피', 'aspirada'), 'sangre', 'blood'), W('사다 (사요)', 'comprar', 'to buy'), W('싸다 (싸요)', 'ser barato', 'to be cheap')],
              (mk('비', 'lisa'), 'Más pares: 비 (bi, «lluvia») con ㅂ lisa y 피 (pi, «sangre») con ㅍ aspirada. 사다 (sada, «comprar») con ㅅ y 싸다 (ssada, «ser barato») con ㅆ tensa. Pon la mano frente a la boca: con ㅍ debe salir aire; con ㅂ, casi nada.',
               'More pairs: 비 (bi, “rain”) with plain ㅂ and 피 (pi, “blood”) with aspirated ㅍ. 사다 (sada, “to buy”) with ㅅ and 싸다 (ssada, “to be cheap”) with tense ㅆ. Put your hand in front of your mouth: with ㅍ air should come out; with ㅂ, almost none.'),
              foco='aspirada', par=(mk('피', 'aspirada'), mk('비', 'lisa')), oye=('비', '피'), inv=True,
              extras=[oye('사다', '싸다'), toca('tensa', mk('싸다', 'tensa lisa'), mk('사다', 'ese lisa')),
                      sig('비', ('lluvia', 'rain'), ('sangre', 'blood')), sig('싸다', ('ser barato', 'to be cheap'), ('comprar', 'to buy'))],
              construye=('사다', '싸')),
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    {
        'id': 'u06', 'titulo': b('K6 · 받침: la consonante de abajo', 'K6 · 받침: the consonant below'),
        'objetivo': b('Leer bloques con consonante final y saber que en esa posición solo existen siete sonidos, siempre sin soltar el aire.',
                      'Read blocks with a final consonant and know that in that position there are only seven sounds, always unreleased.'),
        'lecciones': [
            L('u06l01', '받침 con ㄴ, ㅁ y ㅇ', '받침 with ㄴ, ㅁ and ㅇ',
              [W(mk('산', 'nasal'), 'montaña', 'mountain', '26f0'), W(mk('곰', 'nasal'), 'oso', 'bear', '1f43b'), W(mk('강', 'ng'), 'río', 'river', '1f3de'), W(mk('방', 'ng'), 'cuarto; habitación', 'room', '1f6cf')],
              (mk('강', 'ng'), 'Un bloque puede llevar una consonante abajo: la 받침 (batchim). Se «traba» sin vocal extra: 산 (san) = «san», no «sanu». ㄴ (n) suena «n», ㅁ (m) suena «m» y ㅇ (ng) suena «ng», como en «tango»: 강 (gang). La ㅇ al inicio no suena; la ㅇ al final, sí.',
               'A block can carry a consonant below: the 받침 (batchim). It “locks” the syllable with no extra vowel: 산 (san) = “san,” not “sanu.” ㄴ (n) sounds “n,” ㅁ (m) sounds “m” and ㅇ (ng) sounds “ng,” as in “sing”: 강 (gang). ㅇ at the start is silent; ㅇ at the end is heard.'),
              foco='ng', par=(mk('강', 'ng'), mk('곰', 'nasal')), oye=('강', '간'),
              extras=[toca('nasal', mk('곰', 'nasal'), mk('강', 'ng')), sig('곰', ('oso', 'bear'), ('mar', 'sea')),
                      sig('강', ('río', 'river'), ('montaña', 'mountain')), sig('사람', ('persona', 'person'), ('perro', 'dog'))],
              construye=('사람', '산')),
            L('u06l02', 'Siete sonidos finales', 'Seven final sounds',
              [W(mk('책', 'fk'), 'libro', 'book', '1f4d6'), W(mk('옷', 'ft'), 'ropa', 'clothes', '1f455'), W(mk('집', 'fp'), 'casa; hogar', 'house; home', '1f3e0')],
              (mk('책', 'fk'), 'En posición final solo hay siete sonidos, y siempre sin soltar el aire: «k», «n», «t», «l», «m», «p» y «ng». ㄱ (g) final suena «k»: 책 (chaek). ㅂ (b) final suena «p»: 집 (jip). ㅅ (s) final suena «t»: 옷 (ot). La consonante final se traba, sin vocal extra: 학 (hak), no «haku».',
               'In final position there are only seven sounds, and always unreleased: “k,” “n,” “t,” “l,” “m,” “p” and “ng.” Final ㄱ (g) sounds “k”: 책 (chaek). Final ㅂ (b) sounds “p”: 집 (jip). Final ㅅ (s) sounds “t”: 옷 (ot). The final consonant locks the syllable with no extra vowel: 학 (hak), not “haku.”'),
              foco='fk', par=(mk('책', 'fk'), mk('옷', 'ft')), oye=('집', '짐'), inv=True,
              extras=[toca('fp', mk('집', 'fp'), mk('책', 'fk')), toca('ft', mk('옷', 'ft'), mk('집', 'fp')),
                      sig('책', ('libro', 'book'), ('ropa', 'clothes'))],
              construye=('가방', '집')),
            L('u06l03', 'Varias letras, un solo sonido', 'Several letters, one sound',
              [W(mk('밖', 'fk'), 'afuera', 'outside'), W(mk('부엌', '- fk'), 'cocina (la habitación)', 'kitchen'), W(mk('꽃', 'ft'), 'flor', 'flower', '1f337'), W(mk('앞', 'fp'), 'frente; adelante', 'front')],
              (mk('꽃', 'ft'), 'Aunque se escriban distinto, estas 받침 suenan igual: ㄱ, ㅋ y ㄲ suenan «k» (밖 → «bak», 부엌 → «bueok»); ㄷ, ㅅ, ㅆ, ㅈ, ㅊ, ㅌ y ㅎ suenan «t» (옷 → «ot», 꽃 → «kkot»); ㅂ y ㅍ suenan «p» (앞 → «ap»).',
               'Although they are written differently, these 받침 sound the same: ㄱ, ㅋ and ㄲ sound “k” (밖 → “bak,” 부엌 → “bueok”); ㄷ, ㅅ, ㅆ, ㅈ, ㅊ, ㅌ and ㅎ sound “t” (옷 → “ot,” 꽃 → “kkot”); ㅂ and ㅍ sound “p” (앞 → “ap”).'),
              foco='ft', par=(mk('꽃', 'ft'), mk('앞', 'fp')), oye=('꽃', '꼬리'),
              extras=[sig('꽃', ('flor', 'flower'), ('hoja', 'leaf')), sig('부엌', ('cocina (la habitación)', 'kitchen'), ('puerta', 'door')),
                      lee('밖 · 앞', 'afuera · frente', 'outside · front', '¿Cuál palabra significa «afuera»?', 'Which word means “outside”?', ['밖', '앞'])],
              construye=('부엌', '밖')),
            L('u06l04', 'ㄹ final y los tres pares', 'Final ㄹ and the three pairs',
              [W(mk('달', 'lisa'), 'luna', 'moon', '1f319'), W(mk('탈', 'aspirada'), 'máscara', 'mask', '1f3ad'), W(mk('딸', 'tensa'), 'hija', 'daughter', '1f467')],
              (mk('달', 'lisa'), 'ㄹ (l) al final suena «l», con la punta de la lengua detrás de los dientes de arriba: 달 (dal), 물 (mul), 불 (bul). Aquí vuelven las tres series: 달 (dal, «luna»), 탈 (tal, «máscara») y 딸 (ttal, «hija»). También 불 (bul, «fuego»), 풀 (pul, «hierba») y 뿔 (ppul, «cuerno»).',
               'ㄹ (l) at the end sounds “l,” with the tip of the tongue behind the upper teeth: 달 (dal), 물 (mul), 불 (bul). The three series return here: 달 (dal, “moon”), 탈 (tal, “mask”) and 딸 (ttal, “daughter”). Also 불 (bul, “fire”), 풀 (pul, “grass”) and 뿔 (ppul, “horn”).'),
              foco='tensa', par=(mk('딸', 'tensa'), mk('탈', 'aspirada')), oye=('딸', '탈'), inv=True,
              extras=[oye('불', '풀'), toca('fl', mk('물', 'fl'), mk('달', 'lisa')), toca('aspirada', mk('풀', 'aspirada'), mk('불', 'lisa')),
                      sig('불', ('fuego', 'fire'), ('hierba', 'grass')), sig('사랑', ('amor', 'love'), ('hija', 'daughter'))],
              construye=('사랑', '딸')),
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    {
        'id': 'u07', 'titulo': b('K7 · Enlace: la 받침 se muda', 'K7 · Linking: the 받침 moves'),
        'objetivo': b('Leer el enlace (연음, yeoneum): una 받침 seguida de ㅇ pasa a la sílaba siguiente (음악 → eumak), salvo la ㅇ final.',
                      'Read linking (연음, yeoneum): a 받침 followed by ㅇ moves to the next syllable (음악 → eumak), except final ㅇ.'),
        'lecciones': [
            L('u07l01', 'La ㅇ vacía recibe la consonante', 'The empty ㅇ receives the consonant',
              [W(mk('음악', '- enlace'), 'música', 'music', '1f3b5'), W(mk('한국어', '- - enlace'), 'idioma coreano', 'Korean language'), W('있어요', 'hay; está; tiene', 'there is; to have')],
              (mk('음악', '- enlace'), 'Cuando una 받침 (batchim) va seguida de un bloque que empieza con ㅇ, la consonante pasa a ese bloque: 음악 (eumak) se lee «eu-mak», no «eum-ak»; 한국어 (hangugeo) se lee «han-gu-geo»; 있어요 (isseoyo) se lee «i-sseo-yo». Es el enlace (연음, yeoneum): la ㅇ vacía «recibe» la consonante.',
               'When a 받침 (batchim) is followed by a block that starts with ㅇ, the consonant moves to that block: 음악 (eumak) is read “eu-mak,” not “eum-ak”; 한국어 (hangugeo) is read “han-gu-geo”; 있어요 (isseoyo) is read “i-sseo-yo.” This is linking (연음, yeoneum): the empty ㅇ “receives” the consonant.'),
              foco='enlace', par=(mk('음악', '- enlace'), mk('산', 'nasal')), oye=('한국어', '한국'),
              extras=[sig('음악', ('música', 'music'), ('árbol', 'tree')), sig('한국어', ('idioma coreano', 'Korean language'), ('idioma japonés', 'Japanese language'))],
              construye=('음악', '한')),
            L('u07l02', 'Enlace con cualquier 받침', 'Linking with any 받침',
              [W(mk('일요일', '- enlace -'), 'domingo', 'Sunday'), W(mk('금요일', '- enlace -'), 'viernes', 'Friday'), W(mk('한국인', '- - enlace'), 'coreano; coreana (persona)', 'Korean (person)')],
              (mk('월요일', '- enlace -'), 'Pasa con cualquier 받침: 월요일 (woryoil, «lunes») = «wo-ryo-il», 금요일 (geumyoil) = «geu-myo-il», 한국인 (hangugin) = «han-gu-gin». Al pasar, la consonante suena como inicial: ㄹ → «r», ㅁ → «m», ㄱ → «g». La romanización se escribe ya enlazada. Ojo: ㄹ al final suena «l», pero ante una vocal suena «r».',
               'It happens with any 받침: 월요일 (woryoil, “Monday”) = “wo-ryo-il,” 금요일 (geumyoil) = “geu-myo-il,” 한국인 (hangugin) = “han-gu-gin.” When it moves, the consonant sounds like an initial: ㄹ → “r,” ㅁ → “m,” ㄱ → “g.” Romanization is written already linked. Note: ㄹ at the end sounds “l,” but before a vowel it sounds “r.”'),
              foco='enlace', par=(mk('월요일', '- enlace -'), mk('곰', 'nasal')), oye=('일요일', '월요일'), inv=True,
              extras=[sig('월요일', ('lunes', 'Monday'), ('viernes', 'Friday')), sig('금요일', ('viernes', 'Friday'), ('domingo', 'Sunday')),
                      mezcla('일요일', 'domingo', 'Sunday')],
              construye=('월요일', '금')),
            L('u07l03', 'Enlace con ㄲ, ㅋ, ㅊ, ㅍ y ㅅ', 'Linking with ㄲ, ㅋ, ㅊ, ㅍ and ㅅ',
              [W(mk('꽃이', '- enlace'), 'la flor (como sujeto)', 'the flower (as subject)'), W(mk('밖에', '- enlace'), 'afuera; fuera', 'outside'), W(mk('앞에', '- enlace'), 'delante; enfrente', 'in front'), W(mk('부엌에', '- - enlace'), 'en la cocina', 'in the kitchen')],
              (mk('꽃이', '- enlace'), 'Las 받침 de sonido doble también se «sueltan»: 꽃이 (kkochi) = «kko-chi» (ㅊ suena «ch» ante ㅣ), 밖에 (bakke) = «ba-kke», 앞에 (ape) = «a-pe», 부엌에 (bueoke) = «bu-eo-ke». Las partículas pequeñas 이 y 에 las verás en Fundamentos; aquí solo escucha cómo se enlazan.',
               'Final consonants with a double sound also “let go”: 꽃이 (kkochi) = “kko-chi” (ㅊ sounds “ch” before ㅣ), 밖에 (bakke) = “ba-kke,” 앞에 (ape) = “a-pe,” 부엌에 (bueoke) = “bu-eo-ke.” You will see the small particles 이 and 에 in Foundations; here just listen to how they link.'),
              foco='enlace', par=(mk('밖에', '- enlace'), mk('강', 'ng')), oye=('꽃이', '꽃'),
              extras=[oye('밖에', '밖'), sig('앞에', ('delante; enfrente', 'in front'), ('afuera', 'outside')),
                      sig('부엌에', ('en la cocina', 'in the kitchen'), ('en la casa', 'at home'))],
              construye=('부엌에', '밖')),
            L('u07l04', 'La ㅇ final no se muda', 'Final ㅇ does not move',
              [W(mk('강아지', 'ng - -'), 'cachorro', 'puppy', '1f436'), W(mk('고양이', '- ng -'), 'gato', 'cat', '1f431'), W(mk('영어', 'ng -'), 'inglés (idioma)', 'English (language)'), W(mk('공원', 'ng -'), 'parque', 'park')],
              (mk('강아지', 'ng - -'), 'La ㅇ final («ng») es la excepción: no pasa a la sílaba siguiente. 강아지 (gangaji) = «gang-a-ji», 고양이 (goyangi) = «go-yang-i», 영어 (yeongeo) = «yeong-eo». Compara: 음악 (eumak) se enlaza, pero 강아지 (gangaji) no.',
               'Final ㅇ (“ng”) is the exception: it does not move to the next syllable. 강아지 (gangaji) = “gang-a-ji,” 고양이 (goyangi) = “go-yang-i,” 영어 (yeongeo) = “yeong-eo.” Compare: 음악 (eumak) links, but 강아지 (gangaji) does not.'),
              foco='ng', par=(mk('강아지', 'ng - -'), mk('음악', '- enlace')), oye=('고양이', '고구마'),
              extras=[sig('고양이', ('gato', 'cat'), ('perro', 'dog')), sig('영어', ('inglés (idioma)', 'English (language)'), ('coreano (idioma)', 'Korean (language)')),
                      lee('강아지 · 음악', 'cachorro · música', 'puppy · music', '¿Cuál palabra significa «música»?', 'Which word means “music”?', ['음악', '강아지'])],
              construye=('고양이', '강')),
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    {
        'id': 'u08', 'titulo': b('K8 · Asimilación: se escribe de una manera, se dice de otra', 'K8 · Assimilation: written one way, said another'),
        'objetivo': b('Leer la nasalización (ㅂ/ㄱ + ㄴ/ㅁ) y ㄴ/ㄹ + ㄹ → «ll», y saber que la romanización escribe lo que se oye.',
                      'Read nasalization (ㅂ/ㄱ + ㄴ/ㅁ) and ㄴ/ㄹ + ㄹ → “ll,” and know that romanization writes what you hear.'),
        'lecciones': [
            L('u08l01', 'ㅂ + ㄴ o ㅁ → «mn», «mm»', 'ㅂ + ㄴ or ㅁ → “mn,” “mm”',
              [W(mk('감사합니다', '- - asim - -'), 'gracias', 'thank you', '1f64f'), W(mk('앞문', 'asim -'), 'puerta delantera', 'front door', '1f6aa'), W(mk('입니다', 'asim - -'), 'es (formal)', 'is (formal)')],
              (mk('감사합니다', '- - asim - -'), 'Asimilación: se escribe de una manera y se dice de otra. Cuando ㅂ va seguida de ㄴ o ㅁ, la ㅂ suena «m»: 합니다 (hamnida) se lee «ham-ni-da»; por eso 감사합니다 (gamsahamnida) se dice «gam-sa-ham-ni-da». La romanización escribe lo que se oye.',
               'Assimilation: it is written one way and said another. When ㅂ is followed by ㄴ or ㅁ, the ㅂ sounds “m”: 합니다 (hamnida) is read “ham-ni-da,” so 감사합니다 (gamsahamnida) is said “gam-sa-ham-ni-da.” Romanization writes what you hear.'),
              foco='asim', par=(mk('감사합니다', '- - asim - -'), mk('곰', 'nasal')), oye=('감사합니다', '감사합시다'),
              extras=[rr('감사합니다', 'gracias', 'thank you', ['gamsahamnida', 'gamsahabnida']),
                      sig('감사합니다', ('gracias', 'thank you'), ('perdón', 'sorry')), sig('앞문', ('puerta delantera', 'front door'), ('puerta trasera', 'back door'))],
              construye=('감사합니다', '안')),
            L('u08l02', 'ㄱ + ㄴ o ㅁ → «ng»', 'ㄱ + ㄴ or ㅁ → “ng”',
              [W(mk('한국말', '- asim -'), 'idioma coreano (hablado)', 'Korean language (spoken)'), W(mk('국물', 'asim -'), 'caldo', 'broth', '1f372'), W(mk('박물관', 'asim - -'), 'museo', 'museum')],
              (mk('국물', 'asim -'), 'ㄱ + ㄴ/ㅁ: la ㄱ suena «ng». 국물 (gungmul) = «gung-mul»; 한국말 (hangungmal) = «han-gung-mal»; 박물관 (bangmulgwan) = «bang-mul-gwan». Compara: 한국어 (hangugeo) se enlaza y 한국말 (hangungmal) se asimila.',
               'ㄱ + ㄴ/ㅁ: the ㄱ sounds “ng.” 국물 (gungmul) = “gung-mool”; 한국말 (hangungmal) = “han-gung-mal”; 박물관 (bangmulgwan) = “bang-mool-gwan.” Compare: 한국어 (hangugeo) links and 한국말 (hangungmal) assimilates.'),
              foco='asim', par=(mk('국물', 'asim -'), mk('책', 'fk')), oye=('한국말', '한국어'), inv=True,
              extras=[cambia('한국말', '한국어', ['어', '말', '국']), sig('국물', ('caldo', 'broth'), ('arroz', 'rice')),
                      sig('박물관', ('museo', 'museum'), ('biblioteca', 'library'))],
              construye=('박물관', '국')),
            L('u08l03', 'ㄹ + ㄹ y ㄴ + ㄹ → «ll»', 'ㄹ + ㄹ and ㄴ + ㄹ → “ll”',
              [W(mk('칠레', '- asim'), 'Chile', 'Chile'), W(mk('실례', '- asim'), 'disculpe; con permiso', 'excuse me'), W(mk('연락', '- asim'), 'contacto', 'contact')],
              (mk('칠레', '- asim'), 'ㄹ + ㄹ y ㄴ + ㄹ suenan «ll» larga: 칠레 (chille) = «chil-le»; 실례 (sillye) = «sil-lye»; 연락 (yeollak) = «yeol-lak» (la ㄴ se vuelve «l»). Mantén la «l» un poco más, sin vibrar.',
               'ㄹ + ㄹ and ㄴ + ㄹ sound like a long “ll”: 칠레 (chille) = “chil-leh”; 실례 (sillye) = “sil-lyeh”; 연락 (yeollak) = “yuhl-lak” (the ㄴ turns into “l”). Hold the “l” a little longer, without rolling.'),
              foco='asim', par=(mk('칠레', '- asim'), mk('산', 'nasal')), oye=('칠레', '칠'),
              extras=[rr('칠레', 'Chile', 'Chile', ['chille', 'chilre']), sig('칠레', ('Chile', 'Chile'), ('Perú', 'Peru')),
                      sig('실례', ('disculpe; con permiso', 'excuse me'), ('gracias', 'thank you')), sig('연락', ('contacto', 'contact'), ('música', 'music'))],
              construye=('칠레', '실')),
            L('u08l04', 'Se oye así, pero se lee igual', 'It sounds like this, but you read it the same',
              [W('학교', 'escuela', 'school', '1f3eb'), W('식당', 'restaurante', 'restaurant'), W('학생', 'estudiante', 'student')],
              ('학교', 'Tras ㄱ, ㄷ o ㅂ el sonido siguiente se oye un poco más tenso: 학교 (hakgyo) suena casi «hak-kkyo». No te preocupes: se lee igual, y la romanización lo escribe sin tensión: hakgyo, sikdang, haksaeng. Esto se oye, pero no se evalúa.',
               'After ㄱ, ㄷ or ㅂ the next sound is heard a little tenser: 학교 (hakgyo) sounds almost like “hak-kkyo.” Do not worry: you read it the same, and romanization writes it without the tension: hakgyo, sikdang, haksaeng. You listen to this, but it is not tested.'),
              oye=('학교', '학생'),
              extras=[lee('학교 · 식당 · 학생', 'escuela · restaurante · estudiante', 'school · restaurant · student', '¿Cuál palabra significa «estudiante»?', 'Which word means “student”?', ['학생', '식당']),
                      rr('학교', 'escuela', 'school', ['hakgyo', 'hakkyo']), sig('식당', ('restaurante', 'restaurant'), ('escuela', 'school'))],
              construye=('학교', '생')),
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    {
        'id': 'u09', 'titulo': b('K9 · Palabras reales, carteles y entonación', 'K9 · Real words, signs and intonation'),
        'objetivo': b('Leer carteles, países, ciudades y saludos con todo lo aprendido, comprobar la romanización RR y oír la entonación de preguntas y afirmaciones.',
                      'Read signs, countries, cities and greetings with everything you have learned, check the RR romanization and hear question and statement intonation.'),
        'lecciones': [
            L('u09l01', 'Lee carteles', 'Read signs',
              [W('출구', 'salida', 'exit'), W('입구', 'entrada', 'entrance', '1f6aa'), W('화장실', 'baño; sanitario', 'restroom'), W('약국', 'farmacia', 'pharmacy')],
              ('출구 · 입구', 'Los carteles coreanos usan hangul, sin mayúsculas. Lee bloque a bloque: 출구 (chulgu) = «chul-gu», 입구 (ipgu) = «ip-gu»; la 받침 ㅂ suena «p» y la ㄹ final suena «l». 화장실 (hwajangsil) y 약국 (yakguk) también se leen con lo que ya sabes.',
               'Korean signs use hangul, with no capital letters. Read block by block: 출구 (chulgu) = “chul-gu,” 입구 (ipgu) = “ip-gu”; the 받침 ㅂ sounds “p” and final ㄹ sounds “l.” 화장실 (hwajangsil) and 약국 (yakguk) are also read with what you already know.'),
              oye=('출구', '입구'),
              extras=[lee('출구 · 입구', 'salida · entrada', 'exit · entrance', '¿Qué cartel indica por dónde salir?', 'Which sign shows where to exit?', ['출구', '입구']),
                      lee('약국', 'farmacia', 'pharmacy', '¿Es una farmacia o un banco?', 'Is it a pharmacy or a bank?', ['약국', '은행']),
                      sig('화장실', ('baño; sanitario', 'restroom'), ('salida', 'exit'))],
              construye=('화장실', '약')),
            L('u09l02', 'Países', 'Countries',
              [W('멕시코', 'México', 'Mexico'), W('콜롬비아', 'Colombia', 'Colombia'), W('아르헨티나', 'Argentina', 'Argentina'), W('스페인', 'España', 'Spain')],
              ('콜롬비아', 'Muchos nombres de países se escriben con los sonidos del hangul: 멕시코 (meksiko), 콜롬비아 (kollombia), 아르헨티나 (areuhentina), 스페인 (seupein). Fíjate en la «ll» de 콜 (kol) + 롬 (rom): kollombia. La ㅡ (eu) aparece en 르 (reu) y 스 (seu).',
               'Many country names are written with hangul sounds: 멕시코 (meksiko), 콜롬비아 (kollombia), 아르헨티나 (areuhentina), 스페인 (seupein). Notice the “ll” of 콜 (kol) + 롬 (rom): kollombia. The vowel ㅡ (eu) shows up in 르 (reu) and 스 (seu).'),
              oye=('멕시코', '스페인'),
              extras=[lee('미국 · 일본 · 한국', 'Estados Unidos · Japón · Corea', 'United States · Japan · Korea', '¿Cuál es Japón?', 'Which one is Japan?', ['일본', '미국']),
                      rr('콜롬비아', 'Colombia', 'Colombia', ['kollombia', 'kolombia']), sig('스페인', ('España', 'Spain'), ('Chile', 'Chile'))],
              construye=('멕시코', '스')),
            L('u09l03', 'Ciudades, nombres y romanización', 'Cities, names and romanization',
              [W('서울', 'Seúl (capital)', 'Seoul (capital)'), W('부산', 'Busan (ciudad portuaria)', 'Busan (port city)'), W('제주', 'Jeju (isla)', 'Jeju (island)'), W('김지은', 'nombre de persona: Gim Ji-eun', 'person’s name: Gim Ji-eun')],
              ('서울', 'En mapas y nombres propios verás la romanización RR: Seoul, Busan, Jeju. Los nombres coreanos llevan el apellido primero: 김지은 (Gim Ji-eun) = apellido 김 (Gim) + nombre 지은 (Ji-eun). RR no usa tildes ni signos raros: ㅓ = eo, ㅡ = eu, ㅅ = s, ㅈ = j, ㅊ = ch, ㅋ = k.',
               'On maps and in proper names you will see RR romanization: Seoul, Busan, Jeju. Korean names put the family name first: 김지은 (Gim Ji-eun) = family name 김 (Gim) + given name 지은 (Ji-eun). RR uses no accents or odd signs: ㅓ = eo, ㅡ = eu, ㅅ = s, ㅈ = j, ㅊ = ch, ㅋ = k.'),
              oye=('서울', '부산'),
              extras=[rr('한국어', 'idioma coreano', 'Korean language', ['hangugeo', 'hangukeo']),
                      lee('김지은', 'Gim Ji-eun', 'Gim Ji-eun', '¿Cuál es la romanización de este nombre?', 'Which is the romanization of this name?', ['Gim Ji-eun', 'Gim Ji-un']),
                      sig('서울', ('Seúl (capital)', 'Seoul (capital)'), ('Busan (ciudad portuaria)', 'Busan (port city)'))],
              construye=('서울', '부')),
            L('u09l04', 'Saludos y entonación', 'Greetings and intonation',
              [W('안녕하세요', 'hola', 'hello'), W('감사합니다', 'gracias', 'thank you', '1f64f'), W('죄송합니다', 'lo siento; perdón', 'I am sorry'), W('안녕히 가세요', 'adiós (a quien se va)', 'goodbye (to someone leaving)')],
              ('안녕하세요', 'Son fórmulas fijas: 안녕하세요 (annyeonghaseyo) = «an-nyeong-ha-se-yo», 감사합니다 (gamsahamnida), 죄송합니다 (joesonghamnida). Cada sílaba dura casi lo mismo y no hay sílaba «fuerte».',
               'These are fixed phrases: 안녕하세요 (annyeonghaseyo) = “an-nyeong-ha-se-yo,” 감사합니다 (gamsahamnida), 죄송합니다 (joesonghamnida). Every syllable lasts about the same and there is no “stressed” syllable.'),
              oye=('감사합니다', '죄송합니다'),
              nota=('La entonación: en las preguntas con -요 la voz sube al final (학생이에요? haksaengieyo?); en las afirmaciones baja (학생이에요. haksaengieyo.).',
                    'Intonation: in questions ending in -요 the voice rises at the end (학생이에요? haksaengieyo?); in statements it falls (학생이에요. haksaengieyo.).'),
              extras=[significado('학생이에요?', '¿Cómo termina la voz en esta frase?', 'How does the voice end in this sentence?',
                                  [('Sube: es una pregunta', 'It rises: it is a question'), ('Baja: es una afirmación', 'It falls: it is a statement')]),
                      significado('학생이에요.', '¿Cómo termina la voz en esta frase?', 'How does the voice end in this sentence?',
                                  [('Baja: es una afirmación', 'It falls: it is a statement'), ('Sube: es una pregunta', 'It rises: it is a question')]),
                      sig('죄송합니다', ('lo siento; perdón', 'I am sorry'), ('gracias', 'thank you'))],
              construye=('안녕히', '하')),
        ],
    },
    # ─────────────────────────────────────────────────────────────────────────
    {
        'id': 'u10', 'titulo': b('K10 · Ya puedes empezar', 'K10 · You can start now'),
        'objetivo': b('Comprobar que lees y oyes los sonidos del coreano: carteles, contrastes, palabras nuevas y una primera frase.',
                      'Check that you can read and hear Korean sounds: signs, contrasts, new words and a first sentence.'),
        'lecciones': [
            L('u10l01', 'Lee carteles', 'Read signs',
              [W('입구', 'entrada', 'entrance', '1f6aa'), W('출구', 'salida', 'exit'), W('영업중', 'abierto', 'open'), W('휴무', 'cerrado (día de descanso)', 'closed (day off)')],
              ('입구 · 출구', 'Los carteles no cambian el sonido: lee primero la palabra clave, bloque a bloque.',
               'Signs do not change the sound: read the key word first, block by block.'),
              oye=('출구', '입구'),
              extras=[lee('출구 · 입구', 'salida · entrada', 'exit · entrance', '¿Qué palabra indica por dónde salir?', 'Which word tells you where to exit?', ['출구', '입구']),
                      lee('영업중', 'abierto', 'open', '¿El lugar está abierto o cerrado?', 'Is the place open or closed?', ['영업중', '휴무']),
                      lee('퍼쏘', *PSEUDO, *CUAL_INVENTADA, ['고기', '퍼쏘'], 1)],
              construye=('영업중', '휴')),
            L('u10l02', 'Contrastes', 'Contrasts',
              [W(mk('딸', 'tensa'), 'hija', 'daughter', '1f467'), W(mk('꽃이', '- enlace'), 'la flor (como sujeto)', 'the flower (as subject)'), W(mk('한국말', '- asim -'), 'idioma coreano (hablado)', 'Korean language (spoken)')],
              (mk('딸', 'tensa'), 'Repaso: lisa, aspirada y tensa (달 dal, 탈 tal, 딸 ttal), 받침 (집 jip, 꽃 kkot), enlace (꽃이 kkochi, 음악 eumak) y asimilación (한국말 hangungmal, 감사합니다 gamsahamnida).',
               'Review: plain, aspirated and tense (달 dal, 탈 tal, 딸 ttal), 받침 (집 jip, 꽃 kkot), linking (꽃이 kkochi, 음악 eumak) and assimilation (한국말 hangungmal, 감사합니다 gamsahamnida).'),
              foco='tensa', par=(mk('딸', 'tensa'), mk('탈', 'aspirada')), oye=('탈', '달'),
              extras=[oye('불', '풀'), oye('한국말', '한국어', inv=True), oye('꽃이', '꽃'),
                      toca('enlace', mk('음악', '- enlace'), mk('산', 'nasal')), toca('asim', mk('국물', 'asim -'), mk('곰', 'nasal'))],
              construye=('음악', '한')),
            L('u10l03', 'Palabras nuevas', 'New words',
              [W('도서관', 'biblioteca', 'library'), W('병원', 'hospital', 'hospital'), W('지하철', 'metro', 'subway'), W('대학교', 'universidad', 'university', '1f3eb')],
              ('도서관', 'Estas palabras son nuevas, pero ya conoces sus reglas: 도서관 (doseogwan) con ㄱ entre vocales = «g», 병원 (byeongwon) con ㅇ final = «ng», 지하철 (jihacheol) con ㄹ final = «l», 대학교 (daehakgyo) con 받침 ㄱ = «k».',
               'These words are new, but you know their rules: 도서관 (doseogwan) with ㄱ between vowels = “g,” 병원 (byeongwon) with final ㅇ = “ng,” 지하철 (jihacheol) with final ㄹ = “l,” 대학교 (daehakgyo) with 받침 ㄱ = “k.”'),
              oye=('병원', '도서관'),
              extras=[lee('뚜캄', *PSEUDO, *CUAL_INVENTADA, ['도서관', '뚜캄'], 1),
                      sig('병원', ('hospital', 'hospital'), ('escuela', 'school')), sig('지하철', ('metro', 'subway'), ('autobús', 'bus'))],
              construye=('도서관', '병')),
            L('u10l04', 'Tu primera frase', 'Your first sentence',
              [W('안녕하세요!', 'hola', 'hello'), W('감사합니다!', 'gracias', 'thank you', '1f64f'), W('안녕히 가세요!', 'adiós (a quien se va)', 'goodbye (to someone leaving)')],
              ('안녕하세요! 감사합니다!', 'Junta todo: 안녕하세요 (annyeonghaseyo), 감사합니다 (gamsahamnida, con ㅂ + ㄴ → «mn») y 안녕히 가세요 (annyeonghi gaseyo). ¡Ya puedes empezar Fundamentos!',
               'Put it all together: 안녕하세요 (annyeonghaseyo), 감사합니다 (gamsahamnida, with ㅂ + ㄴ → “mn”) and 안녕히 가세요 (annyeonghi gaseyo). You are ready for Foundations!'),
              oye=('안녕하세요', '안녕히'),
              extras=[lee('안녕히 가세요!', 'adiós', 'goodbye', '¿Es un saludo o una despedida?', 'Is it a greeting or a goodbye?', ['안녕하세요', '안녕히 가세요'], 1),
                      deletreo('안녕', 'Escucha y ordena las letras de 안녕 (annyeong).', 'Listen and put the letters of 안녕 (annyeong) in order.')],
              construye=('안녕', '하')),
        ],
    },
]


def nivel0_json():
    return {
        'esquema': 'onelingo.nivel0.v1',
        'idioma': 'ko',
        'titulo': b('Nivel 0 · Leer y pronunciar coreano', 'Level 0 · Read and pronounce Korean'),
        'subtitulo': b('Para quien empieza desde cero: cómo se leen y suenan las letras del hangul.',
                       'For complete beginners: how hangul letters are read and how they sound.'),
        'voz': 'narradora',
        'nota': 'Marcado: (bloque:sonido) pinta el bloque con el color del sonido (ver sonidos.json). Cada texto, opción, ficha y letra en hangul lleva `rom` (Romanización Revisada) generado por romanizar.py. Fuente: tools/contenido/nivel0-ko/generar.py. Apoyo es + en.',
        'textos': {
            'tarjeta': b('¿Empiezas de cero? Aprende a leer y pronunciar el hangul.', 'Starting from zero? Learn to read and pronounce hangul.'),
            'muestra': '(가:lisa)(카:aspirada)(까:tensa) · 음(악:enlace)',
            'emoji': '1f4d6',
            'junta': b('Escucha despacio y después rápido: así se lee el coreano.', 'Listen slowly, then fast: that is how you read Korean.'),
            'mapaIntro': b('El hangul se escribe en bloques de sílaba y se lee tal como suena, con unas pocas reglas. Lo nuevo: las vocales ㅓ y ㅡ, las tres series de consonantes (lisas, aspiradas y tensas), la 받침 de abajo, el enlace y la asimilación. Cada sonido tiene una imagen y un color que verás en las palabras. Toca una tarjeta para oírla.',
                           'Hangul is written in syllable blocks and read as it sounds, with a few rules. What is new: the vowels ㅓ and ㅡ, the three series of consonants (plain, aspirated and tense), the 받침 below, linking and assimilation. Each sound has a picture and a color you will see in the words. Tap a card to hear it.'),
            'grupos': GRUPOS,
        },
        'revision': 'inicial',
        'refuerzo': {'bloques': 'u01', 'vocales': 'u02', 'consonantes': 'u03', 'vocalesY': 'u04',
                     'series': 'u05', 'finales': 'u06', 'enlace': 'u07', 'asimilacion': 'u08'},
        'evaluacion': {'lecciones': ['u10l01', 'u10l02', 'u10l03', 'u10l04'], 'pseudopalabras': ['퍼쏘', '뚜캄'], 'umbral': 0.8},
        'unidades': UNIDADES,
    }


# ── rom: se añade a todo texto, opción, ficha y letra en hangul ──────────────
CAMPOS_TEXTO = ('texto', 'pregunta', 't', 'nota', 'titulo', 'objetivo')


def con_rom(nodo):
    if isinstance(nodo, list):
        for x in nodo:
            con_rom(x)
    elif isinstance(nodo, dict):
        m = nodo.get('m')
        if isinstance(m, str) and HANGUL.search(m) and 'rom' not in nodo:
            nodo['rom'] = rom_texto(plano(m))
        if nodo.get('tipo') == 'cambia':
            nodo['deRom'], nodo['aRom'] = rom_texto(nodo['de']), rom_texto(nodo['a'])
        for clave in ('opciones', 'fichas'):
            v = nodo.get(clave)
            if isinstance(v, list) and v and all(isinstance(x, str) for x in v) and any(HANGUL.search(x) for x in v):
                nodo[clave + 'Rom'] = [rom_texto(x) for x in v]  # opcionesRom, fichasRom (docs/claude-educacion/ROMANIZACION.md)
        for k, v in nodo.items():
            if isinstance(v, (list, dict)):
                con_rom(v)


def textos(nodo, acc=None):
    """Todos los textos de apoyo (es/en) de un nodo."""
    acc = [] if acc is None else acc
    if isinstance(nodo, dict):
        for k, v in nodo.items():
            if k in CAMPOS_TEXTO and isinstance(v, dict) and 'es' in v:
                acc += [v['es'], v['en']]
            elif k == 'texto' and isinstance(v, str):
                acc.append(v)
            else:
                textos(v, acc)
    elif isinstance(nodo, list):
        for x in nodo:
            textos(x, acc)
    return acc


def comprobar(datos):
    """Avisos de calidad: cifras, Ecuador, hangul en el apoyo sin su rom, nombres fuera de la ficha."""
    avisos = []
    s = json.dumps(datos, ensure_ascii=False)
    for t in re.findall(r'"(?:m|audio)": "([^"]*)"', s):
        if re.search(r'\d', t):
            avisos.append(f'cifra en texto que se oye: {t}')
    for t in textos(datos):
        if re.search(r'\d', t) and not re.match(r'(K\d+ ·|Nivel 0|Level 0)', t):
            avisos.append(f'cifra en apoyo: {t}')
        if re.search(r'ecuador|\bquito\b|guayaquil|\bcuenca\b|ecuatorian|에콰도르', t, re.I):
            avisos.append(f'Ecuador: {t}')
        letras = re.sub(r'[^a-z]', '', t.lower())
        for run in re.findall(r'[가-힣]+', t):
            if run == '받침':  # término técnico: se define con su rom (batchim) en u06
                continue
            r = re.sub(r'[^a-z]', '', rom_texto(run).lower())
            if r not in letras:
                avisos.append(f'hangul sin rom en el apoyo: {run} ({r}) en «{t[:60]}»')
    if re.search(r'ecuador|\bquito\b|guayaquil|\bcuenca\b|ecuatorian|에콰도르', s, re.I):
        avisos.append('Ecuador en el archivo')
    return avisos


def escribir(nombre, datos):
    (DESTINO / nombre).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


if __name__ == '__main__':
    DESTINO.mkdir(parents=True, exist_ok=True)
    nivel0 = nivel0_json()
    con_rom(nivel0)
    avisos = comprobar(nivel0)
    for a in avisos:
        print('AVISO', a)
    escribir('sonidos.json', sonidos_json())
    escribir('nivel0.json', nivel0)
    r = subprocess.run([sys.executable, str(RAIZ / 'tools/contenido/validar_nivel0.py'), 'ko',
                        str(DESTINO / 'nivel0.json'), '--bilingue'])
    sys.exit(r.returncode or (1 if avisos else 0))
