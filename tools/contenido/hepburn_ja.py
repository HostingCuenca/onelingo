"""Rōmaji Hepburn modificado del japonés (tools/ia/idiomas/ja.md, sección `rom`).

Convierte kana a rōmaji palabra a palabra, con las reglas de la ficha:
- vocales largas con macrón (おう/おお → ō, ええ → ē, うう → ū, ああ → ā; いい → ii,
  えい → ei) y ー del katakana alarga la vocal anterior;
- し shi, ち chi, つ tsu, ふ fu, じ ji; っ dobla la consonante (kitte, zasshi, matcha → tch);
- ん siempre n, con apóstrofo recto ante vocal o y (kin'en, hon'ya);
- は wa, へ e, を o cuando son partículas (palabras sueltas del texto);
- minúscula salvo inicio de frase y nombres propios (personas, ciudades, países de la
  lista cerrada); «-san» pegado al nombre propio lleva guion (Tanaka-san).

El texto japonés va con un espacio entre palabras y la rom lleva una palabra por cada
una (mismo número de grupos). Lo usan `validar_diagnostico.py` (japonés) y el autor del
banco de ubicación; no se usa en tiempo de ejecución.

    rom_frase('わたし は たなかさん です。')  ->  'Watashi wa Tanaka-san desu.'
    errores_rom('わたし は がくせい です。', 'Watashi wa gakusei desu.')  ->  []
"""
from __future__ import annotations

import re

_BASE = {}
for _ks, _rs in [
    ('あいうえお', 'a i u e o'), ('かきくけこ', 'ka ki ku ke ko'), ('さしすせそ', 'sa shi su se so'),
    ('たちつてと', 'ta chi tsu te to'), ('なにぬねの', 'na ni nu ne no'), ('はひふへほ', 'ha hi fu he ho'),
    ('まみむめも', 'ma mi mu me mo'), ('やゆよ', 'ya yu yo'), ('らりるれろ', 'ra ri ru re ro'),
    ('わゐゑを', 'wa i e o'), ('がぎぐげご', 'ga gi gu ge go'), ('ざじずぜぞ', 'za ji zu ze zo'),
    ('だぢづでど', 'da ji zu de do'), ('ばびぶべぼ', 'ba bi bu be bo'), ('ぱぴぷぺぽ', 'pa pi pu pe po'),
    ('ゔ', 'vu'),
]:
    for _k, _r in zip(_ks, _rs.split()):
        _BASE[_k] = _r

_MACRON = {'a': 'ā', 'i': 'ī', 'u': 'ū', 'e': 'ē', 'o': 'ō'}
_PARTICULAS = {'は': 'wa', 'へ': 'e', 'を': 'o'}
_FIJAS = {'こんにちは': 'konnichiwa', 'こんばんは': 'konbanwa'}
_PUNT = {'。': '.', '、': ',', '？': '?', '！': '!'}
_PUNT_FINAL = re.compile(r'[。、？！]+$')

PERSONAS = ('さくら ゆき あおい めぐみ ようこ みさき あやか ななこ けんた たくや ゆうた だいすけ りょう '
            'しょうた ひろし たなか すずき わたなべ たかはし いとう やまもと なかむら こばやし かとう '
            'よしだ').split()
LUGARES = ('とうきょう おおさか きょうと なごや ふくおか さっぽろ よこはま こうべ ひろしま せんだい '
           'メキシコ コロンビア アルゼンチン チリ ペルー スペイン アメリカ にほん イタリア スイス').split()


def _hira(c: str) -> str:
    return chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c


def palabra(tok: str) -> str | None:
    """Rōmaji de una palabra en kana (sin partículas ni puntuación); None si lleva otra escritura."""
    s = [_hira(c) for c in tok]
    kata = [('ァ' <= c <= 'ヶ') for c in tok]
    out: list[str] = []
    i, doble = 0, False
    while i < len(s):
        c = s[i]
        if c == 'っ':
            doble = True
            i += 1
            continue
        if c == 'ー':
            if not out:
                return None
            out[-1] = out[-1][:-1] + _MACRON[out[-1][-1]]
            i += 1
            continue
        if c == 'ん':
            sig = s[i + 1] if i + 1 < len(s) else ''
            out.append("n'" if sig and sig in 'あいうえおやゆよ' else 'n')
            i += 1
            continue
        if c in 'ぁぃぅぇぉ':  # katakana extendido: ファ fa, ティ ti, ウィ wi, チェ che
            if not out:
                return None
            ant = out.pop()
            v = {'ぁ': 'a', 'ぃ': 'i', 'ぅ': 'u', 'ぇ': 'e', 'ぉ': 'o'}[c]
            if ant == 'fu':
                r = 'f' + v
            elif ant == 'tsu':
                r = 'ts' + v
            elif ant in ('chi', 'shi', 'ji'):
                r = ('ch' if ant == 'chi' else 'sh' if ant == 'shi' else 'j') + v
            elif ant == 'te':
                r = 'ti' if v == 'i' else 'te'
            elif ant == 'de':
                r = 'di'
            elif ant == 'u':
                r = 'w' + v
            else:
                r = ant[:-1] + v
            out.append(r)
            i += 1
            continue
        r = _BASE.get(c)
        if r is None:
            return None
        if i + 1 < len(s) and s[i + 1] in 'ゃゅょ':
            v = {'ゃ': 'a', 'ゅ': 'u', 'ょ': 'o'}[s[i + 1]]
            r = (r[:-1] + v) if r in ('shi', 'chi', 'ji') else r[:-1] + 'y' + v
            i += 1
        if doble:
            r = ('t' + r) if r[:2] in ('ch', 'ts') else r[0] + r
            doble = False
        # Vocal larga escrita en hiragana: おう/おお → ō, ええ → ē, うう → ū, ああ → ā (いい y えい no).
        if out and not kata[i] and c in 'あいうえお' and r in ('a', 'i', 'u', 'e', 'o'):
            prev = out[-1]
            v = prev[-1]
            if (c, v) in (('あ', 'a'), ('う', 'u'), ('え', 'e'), ('お', 'o'), ('う', 'o')):
                out[-1] = prev[:-1] + _MACRON[v]
                i += 1
                continue
        out.append(r)
        i += 1
    return ''.join(out)


def _nombre_propio(nucleo: str) -> str | None:
    """Nombre de la lista cerrada (solo o con «さん» pegado, o seguido del hueco ___)."""
    for n in sorted(PERSONAS + LUGARES, key=len, reverse=True):
        if nucleo == n or (n in PERSONAS and nucleo == n + 'さん') or nucleo.startswith(n + '_'):
            return n
    return None


def _esperado(token: str, ini: bool) -> str | None:
    """Rōmaji esperado de un token japonés (con su puntuación); None si no se puede calcular."""
    m = _PUNT_FINAL.search(token)
    nucleo = token[:m.start()] if m else token
    punt = ''.join(_PUNT[p] for p in (m.group() if m else ''))
    if nucleo in ('—', '～'):
        return nucleo
    if nucleo.endswith('___') or nucleo == '___':
        pre = nucleo[:-3]
        r = palabra(pre) if pre else ''
        if r is None:
            return None
        r += '___'
    elif nucleo in _PARTICULAS:
        r = _PARTICULAS[nucleo]
    elif nucleo in _FIJAS:
        r = _FIJAS[nucleo]
    else:
        nom = _nombre_propio(nucleo)
        if nom and nucleo == nom + 'さん' and nom in PERSONAS:
            base = palabra(nom)
            r = None if base is None else base + '-san'
        else:
            r = palabra(nucleo)
        if r is None:
            return None
        if nom:
            r = r[0].upper() + r[1:]
    if ini and r[0].isalpha():
        r = r[0].upper() + r[1:]
    return r + punt


def rom_frase(texto: str) -> str | None:
    """Rōmaji de un texto japonés con espacios entre palabras; None si lleva kanji u otra escritura."""
    frase = bool(re.search(r'[。？！]', texto))
    out, ini = [], frase
    for tok in texto.split():
        e = _esperado(tok, ini)
        if e is None:
            return None
        out.append(e)
        # Tras un enunciado completo (o tras el guion de diálogo) empieza otro.
        ini = frase and (bool(re.search(r'[。？！]$', tok)) or tok == '—')
    return ' '.join(out)


def errores_rom(texto: str, rom: str) -> list[str]:
    """Discrepancias entre `texto` (japonés con espacios) y su `rom`; vacío = correcto.

    Exige un grupo de rōmaji por palabra y la ortografía Hepburn de la ficha, con la
    capitalización de la ficha (inicio de frase y nombres propios)."""
    esperado = rom_frase(texto)
    if esperado is None:
        return []  # lleva kanji u otra escritura: no se puede calcular
    jt, rt, et = texto.split(), rom.split(), esperado.split()
    if len(jt) != len(rt):
        return [f'«{texto}» tiene {len(jt)} palabras y su rom «{rom}» tiene {len(rt)} grupos; deben coincidir uno a uno']
    return [f'«{j}» debería ser «{e}», no «{r}»' for j, r, e in zip(jt, rt, et) if r != e]
