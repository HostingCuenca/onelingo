#!/usr/bin/env python3
"""Romanización Revisada (RR) del coreano para comprobar la `rom` de los ítems.

Lo usa tools/contenido/validar_diagnostico.py (como hepburn_ja.py para el japonés):
calcula la RR de cada eojeol con las reglas de tools/ia/idiomas/ko.md y la
compara con el rom escrito. Reglas:
- enlace (연음): la 받침 pasa a la ㅇ siguiente (한국어 hangugeo, 있어요 isseoyo);
- grupos finales: 읽어요 ilgeoyo, 읽다 ikda, 많아요 manayo, 싫어해요 sireohaeyo;
- nasalización: ㄱ/ㄷ/ㅂ + ㄴ/ㅁ (입니다 imnida), ㅁ/ㅇ + ㄹ (심리 simni), ㄴ+ㄹ y ㄹ+ㄴ = ll;
- ㅎ: con ㄱ/ㄷ/ㅂ/ㅈ/ㅅ se transcribe la aspirada sin h (가족하고 gajokago, 못해요 motaeyo,
  놓쳐요 nochyeoyo); con ㄴ/ㄹ/ㅁ/ㅇ se escribe con h (안녕하세요 annyeonghaseyo,
  금요일하고 geumyoilhago); ㅎ ante vocal no suena (좋아요 joayo);
- palatalización: 같이 gachi, 닫혀요 dachyeoyo;
- la tensión de ㄱㄷㅂ tras 받침 no se transcribe (학교 hakgyo); ㅅ ante ㅣ es s; 의 = ui.
`EXCEPCIONES` recoge lo léxico que ninguna regla da (십육 simnyuk, 못 mot, 알약 allyak…).
"""
import re

LI = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
VO = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
FI = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ',
      'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
INI = dict(zip(LI, ['g', 'kk', 'n', 'd', 'tt', 'r', 'm', 'b', 'pp', 's', 'ss', '', 'j', 'jj',
                    'ch', 'k', 't', 'p', 'h']))
VOW = dict(zip(VO, ['a', 'ae', 'ya', 'yae', 'eo', 'e', 'yeo', 'ye', 'o', 'wa', 'wae', 'oe', 'yo',
                    'u', 'wo', 'we', 'wi', 'yu', 'eu', 'ui', 'i']))
FIN = {'ㄱ': 'k', 'ㄲ': 'k', 'ㅋ': 'k', 'ㄴ': 'n', 'ㄷ': 't', 'ㅅ': 't', 'ㅆ': 't', 'ㅈ': 't',
       'ㅊ': 't', 'ㅌ': 't', 'ㅎ': 't', 'ㄹ': 'l', 'ㅁ': 'm', 'ㅂ': 'p', 'ㅍ': 'p', 'ㅇ': 'ng'}
GRUPO = {'ㄳ': ('ㄱ', 'ㅅ'), 'ㄵ': ('ㄴ', 'ㅈ'), 'ㄶ': ('ㄴ', 'ㅎ'), 'ㄺ': ('ㄹ', 'ㄱ'), 'ㄻ': ('ㄹ', 'ㅁ'),
         'ㄼ': ('ㄹ', 'ㅂ'), 'ㄽ': ('ㄹ', 'ㅅ'), 'ㄾ': ('ㄹ', 'ㅌ'), 'ㄿ': ('ㄹ', 'ㅍ'), 'ㅀ': ('ㄹ', 'ㅎ'),
         'ㅄ': ('ㅂ', 'ㅅ')}
# Qué sonido deja el grupo ante consonante (se pronuncia una sola letra).
GRUPO_ANTE_CONSONANTE = {'ㄳ': 'ㄱ', 'ㄵ': 'ㄴ', 'ㄶ': 'ㄴ', 'ㄺ': 'ㄱ', 'ㄻ': 'ㅁ', 'ㄼ': 'ㄹ', 'ㄽ': 'ㄹ',
                         'ㄾ': 'ㄹ', 'ㄿ': 'ㅂ', 'ㅀ': 'ㄹ', 'ㅄ': 'ㅂ'}
ASPIRADA = {'ㄱ': 'ㅋ', 'ㄷ': 'ㅌ', 'ㅂ': 'ㅍ', 'ㅈ': 'ㅊ', 'ㅅ': 'ㅌ'}
NASAL = {'k': 'ㅇ', 't': 'ㄴ', 'p': 'ㅁ'}

# Léxico: lo que ninguna regla da (inserción de ㄴ, palabras compuestas, lecturas fijas).
EXCEPCIONES = {
    '십육': 'simnyuk', '못': 'mot', '알약': 'allyak', '집안일': 'jibannil', '신혼여행': 'sinhonnyeohaeng',
    '붙여요': 'buchyeoyo', '붙여': 'buchyeo',
}


def _silabas(w):
    out = []
    for ch in w:
        c = ord(ch) - 0xAC00
        out.append([LI[c // 588], VO[(c % 588) // 28], FI[c % 28]])
    return out


def romanizar_eojeol(w):
    """RR (en minúsculas) de un eojeol en hangul; `None` si hay letras que no son sílabas."""
    if not w or not all('가' <= c <= '힣' for c in w):
        return None
    if w in EXCEPCIONES:
        return EXCEPCIONES[w]
    s = _silabas(w)
    n = len(s)
    for i in range(n - 1):
        ini, vo, fi = s[i]
        if not fi:
            continue
        sig = s[i + 1]
        ni = sig[0]
        a, b = GRUPO.get(fi, (fi, None))
        # palatalización: ㄷ/ㅌ + 이 (같이 gachi) y ㄷ+히 (닫히다 dachida)
        if ni == 'ㅇ' and fi in 'ㄷㅌ' and sig[1] == 'ㅣ':
            s[i][2], s[i + 1][0] = '', {'ㄷ': 'ㅈ', 'ㅌ': 'ㅊ'}[fi]
            continue
        if ni == 'ㅎ' and fi == 'ㄷ' and sig[1] in 'ㅣㅕ':
            s[i][2], s[i + 1][0] = '', 'ㅊ'
            continue
        # enlace ante ㅇ vacía
        if ni == 'ㅇ':
            if fi == 'ㅇ':
                continue
            if b is not None:
                s[i][2] = a
                if b != 'ㅎ':
                    s[i + 1][0] = b
                else:  # ㅎ muda: ㄶ→n, ㅀ→r (싫어요 sireoyo)
                    if a == 'ㄹ':
                        s[i][2], s[i + 1][0] = '', 'ㄹ'
            elif fi == 'ㅎ':
                s[i][2] = ''
            else:
                s[i][2], s[i + 1][0] = '', fi
            continue
        # ㅎ tras 받침 simple o grupo con ㅎ
        if ni == 'ㅎ' and b is None and fi in ASPIRADA:
            s[i][2], s[i + 1][0] = '', ASPIRADA[fi]
            continue
        if (fi == 'ㅎ' or b == 'ㅎ') and ni == 'ㅊ':  # 놓쳐요 nochyeoyo
            s[i][2] = a if b == 'ㅎ' else ''
            continue
        if (fi == 'ㅎ' or b == 'ㅎ') and ni in 'ㄱㄷㅂㅈ':
            s[i][2] = a if b == 'ㅎ' else ''
            s[i + 1][0] = {'ㄱ': 'ㅋ', 'ㄷ': 'ㅌ', 'ㅂ': 'ㅍ', 'ㅈ': 'ㅊ'}[ni]
            continue
        if b is not None:  # grupo ante consonante: una sola letra
            fi = GRUPO_ANTE_CONSONANTE[fi]
            if fi == 'ㄱ' and a == 'ㄹ' and ni == 'ㄱ':
                fi = 'ㄹ'  # 읽고 ilgo
        s[i][2] = fi
        cl = FIN[fi]
        if ni in 'ㄴㅁ' and cl in NASAL:
            s[i][2] = NASAL[cl]
        elif ni == 'ㄹ':
            if cl in ('l', 'n'):
                s[i][2], s[i + 1][0] = 'ㄹ', 'ㄹ'
            elif cl in ('m', 'ng'):
                s[i + 1][0] = 'ㄴ'
            elif cl in NASAL:
                s[i + 1][0], s[i][2] = 'ㄴ', NASAL[cl]
        elif ni == 'ㄴ' and cl == 'l':
            s[i][2], s[i + 1][0] = 'ㄹ', 'ㄹ'
    out = ''
    for i, (ini, vo, fi) in enumerate(s):
        c = INI['ㅇ' if ini == 'ㅇ' else ini]
        if ini == 'ㄹ':
            c = 'l' if (i > 0 and s[i - 1][2] == 'ㄹ') else 'r'
        f = ''
        if fi:
            f = FIN[GRUPO_ANTE_CONSONANTE.get(fi, fi)]
        out += c + VOW[vo] + f
    return out


# Nombres de la ficha (tools/ia/idiomas/ko.md): apellido + nombre = dos palabras de rom.
APELLIDOS = ['김', '박', '최', '정', '강', '조', '윤', '장', '홍', '송']
NOMBRES_PILA = ['지은', '서연', '민지', '수빈', '하윤', '예린', '소희', '유진',
                '민준', '도윤', '지훈', '현우', '준호', '성민', '동현']
CIUDADES = ['서울', '부산', '인천', '대구', '대전', '광주', '수원', '울산', '전주', '제주']
HANGUL = re.compile(r'[가-힣]+')


def _es_nombre_completo(w):
    return any(w.startswith(a + n) for a in APELLIDOS for n in NOMBRES_PILA)


def tokens_hangul(texto):
    """Eojeol (con hangul) del texto, sin puntuación ni huecos."""
    return [m.group(0) for t in texto.replace('___', ' ').split() for m in [HANGUL.search(t)] if m]


def errores_rom(texto, rom, lexico=None):
    """Errores de la `rom` de un texto coreano. `lexico`: eojeol → roms de las clases
    (si el eojeol está allí, vale cualquiera de las suyas, sin distinguir mayúsculas)."""
    errores = []
    eojeol = tokens_hangul(texto)
    esperados = sum(2 if _es_nombre_completo(w) else 1 for w in eojeol)
    partes = [p for p in rom.replace('___', ' ').split() if re.search(r'[A-Za-z]', p)]
    if len(partes) != esperados:
        return [f'«{texto}» tiene {len(eojeol)} eojeol ({esperados} palabras de rom) y «{rom}» tiene '
                f'{len(partes)}; deben coincidir uno a uno (nombre completo = 2 palabras)']
    k = 0
    for w in eojeol:
        if _es_nombre_completo(w):
            k += 2  # el nombre propio se comprueba como lista cerrada (validar.py)
            continue
        r = re.sub(r'[^A-Za-z\-]', '', partes[k])
        k += 1
        propio = any(w.startswith(c) for c in CIUDADES) or any(w.startswith(n) for n in NOMBRES_PILA)
        if r[:1].isupper() != any(w.startswith(c) for c in CIUDADES) and not propio:
            errores.append(f'«{w}»: mayúscula en «{r}» (solo en nombres propios)')
        if propio and r[:1].islower() and any(w.startswith(c) for c in CIUDADES):
            errores.append(f'«{w}»: «{r}» debe llevar mayúscula (ciudad)')
        if lexico and w in lexico and r.lower() in {x.lower() for x in lexico[w]}:
            continue
        calc = romanizar_eojeol(w)
        if calc is not None and r.lower().replace('-', '') != calc:
            errores.append(f'«{w}»: la RR es «{calc}», no «{r}»')
    return errores
