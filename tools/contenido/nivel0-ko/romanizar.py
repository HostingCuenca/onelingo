"""Romanización Revisada (RR) del coreano para el Nivel 0 (solo lo que se enseña).

Es la única fuente de `rom`: decompone el hangul y aplica enlace (연음),
nasalización básica (ㄱ/ㅂ/ㄷ + ㄴ/ㅁ) y ㄴ+ㄹ / ㄹ+ㄹ → ll. Lo que no soporta
(grupos finales, palatalización ㄷ/ㅌ+ㅣ, ㄹ tras otras consonantes) lanza error.
Reglas: tools/ia/idiomas/ko.md (tabla RR completa y notas).
"""
import re

LI = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
VO = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
FI = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ',
      'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
RI = dict(zip(LI, ['g', 'kk', 'n', 'd', 'tt', 'r', 'm', 'b', 'pp', 's', 'ss', '', 'j', 'jj',
                   'ch', 'k', 't', 'p', 'h']))
RV = dict(zip(VO, ['a', 'ae', 'ya', 'yae', 'eo', 'e', 'yeo', 'ye', 'o', 'wa', 'wae', 'oe', 'yo',
                   'u', 'wo', 'we', 'wi', 'yu', 'eu', 'ui', 'i']))
CLASE = {'ㄱ': 'k', 'ㄲ': 'k', 'ㅋ': 'k', 'ㄴ': 'n', 'ㄷ': 't', 'ㅅ': 't', 'ㅆ': 't', 'ㅈ': 't',
         'ㅊ': 't', 'ㅌ': 't', 'ㅎ': 't', 'ㄹ': 'l', 'ㅁ': 'm', 'ㅂ': 'p', 'ㅍ': 'p', 'ㅇ': 'ng'}
NASAL = {'k': 'ng', 't': 'n', 'p': 'm', 'n': 'n', 'm': 'm', 'ng': 'ng'}

# Nombres propios de la ficha (apellido + nombre con guion) y ciudades.
PROPIOS = {
    '김지은': 'Gim Ji-eun', '박서연': 'Bak Seo-yeon', '최민지': 'Choe Min-ji',
    '정수빈': 'Jeong Su-bin', '강하윤': 'Gang Ha-yun', '조예린': 'Jo Ye-rin',
    '윤소희': 'Yun So-hui', '장유진': 'Jang Yu-jin', '김민준': 'Gim Min-jun',
    '박도윤': 'Bak Do-yun', '최지훈': 'Choe Ji-hun', '정현우': 'Jeong Hyeon-u',
    '강준호': 'Gang Jun-ho', '홍성민': 'Hong Seong-min', '송동현': 'Song Dong-hyeon',
    '서울': 'Seoul', '부산': 'Busan', '인천': 'Incheon', '대구': 'Daegu', '대전': 'Daejeon',
    '광주': 'Gwangju', '수원': 'Suwon', '울산': 'Ulsan', '전주': 'Jeonju', '제주': 'Jeju',
}
JAMO = {**RI, **RV, 'ㅇ': 'ng'}
TROZOS = re.compile(r'[가-힣]+|[ㄱ-ㅣ]|[^가-힣ㄱ-ㅣ]+')
HANGUL = re.compile(r'[가-힣ㄱ-ㅣ]')


def _palabra(w):
    sil = []
    for ch in w:
        c = ord(ch) - 0xAC00
        sil.append((LI[c // 588], VO[(c % 588) // 28], FI[c % 28]))
    n = len(sil)
    ini = [RI[s[0]] for s in sil]
    fin = [''] * n
    for i, (_, _, t) in enumerate(sil):
        if not t:
            continue
        if t not in CLASE:
            raise ValueError(f'grupo final no soportado en {w}')
        nxt = sil[i + 1] if i + 1 < n else None
        if nxt and nxt[0] == 'ㅇ' and t != 'ㅇ':
            if t in 'ㄷㅌ' and nxt[1] == 'ㅣ':
                raise ValueError(f'palatalización no soportada en {w}')
            ini[i + 1] = '' if t == 'ㅎ' else RI[t]
        elif nxt and nxt[0] in 'ㄴㅁ':
            if t == 'ㄹ':
                raise ValueError(f'ㄹ+ㄴ/ㅁ no soportado en {w}')
            fin[i] = NASAL[CLASE[t]]
        elif nxt and nxt[0] == 'ㄹ':
            if t not in 'ㄴㄹ':
                raise ValueError(f'asimilación con ㄹ no soportada en {w}')
            fin[i], ini[i + 1] = 'l', 'l'
        else:
            fin[i] = CLASE[t]
    for i in range(1, n):
        if sil[i][0] == 'ㄹ' and ini[i] == 'r' and sil[i - 1][2]:
            raise ValueError(f'ㄹ inicial tras consonante no soportada en {w}')
    return ''.join(ini[i] + RV[sil[i][1]] + fin[i] for i in range(n))


def rom_palabra(w):
    """Romaniza una palabra (un eojeol); nombres propios con su forma de la ficha."""
    r = _palabra(w)
    if w in PROPIOS:
        assert re.sub(r'[- ]', '', PROPIOS[w]).lower() == r, (w, PROPIOS[w], r)
        return PROPIOS[w]
    return r


def rom_texto(s):
    """Romaniza un texto: cada tramo de hangul por separado; el resto pasa igual."""
    out = []
    for t in TROZOS.findall(s):
        if re.match(r'[가-힣]', t):
            out.append(rom_palabra(t))
        elif re.match(r'[ㄱ-ㅣ]', t):
            out.append(JAMO[t])
        else:
            out.append(t)
    return ''.join(out)


# Casos de la ficha (ko.md): si alguno falla, el romanizador está mal.
PRUEBAS = {
    '감사합니다': 'gamsahamnida', '실례': 'sillye', '아기': 'agi', '고기': 'gogi', '바다': 'bada',
    '한국': 'hanguk', '사랑': 'sarang', '달': 'dal', '일본': 'ilbon', '칠레': 'chille',
    '한국어': 'hangugeo', '있어요': 'isseoyo', '입니다': 'imnida', '한국말': 'hangungmal',
    '학교': 'hakgyo', '시': 'si', '선생님': 'seonsaengnim', '저는': 'jeoneun',
    '학생이에요': 'haksaengieyo', '민준이에요': 'minjunieyo', '밖': 'bak', '옷': 'ot',
    '꽃': 'kkot', '앞': 'ap', '부엌': 'bueok', '학': 'hak', '음악': 'eumak', '국물': 'gungmul',
    '강': 'gang', '서울': 'Seoul', '부산': 'Busan', '김지은': 'Gim Ji-eun',
}
for _h, _r in PRUEBAS.items():
    assert rom_palabra(_h) == _r, (_h, rom_palabra(_h), _r)
