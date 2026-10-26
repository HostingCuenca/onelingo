import 'modelos.dart';

/// Respuestas escritas en letras latinas en ru, ja, ko y zh, para quien no
/// tiene el teclado del idioma («privet» por «привет», «gakusei» por «学生»).
///
/// La romanización esperada sale del propio curso: cada palabra con su `rom`
/// (vocabulario, fichas de ordenar, opciones, pares y frases con el mismo
/// número de palabras). Lo que no está en el curso se translitera si se
/// puede (cirílico, hangul y kana). Si una parte de la respuesta no se puede
/// romanizar, la forma latina no se acepta y sigue la corrección normal.
///
/// Se compara sin tildes, tonos ni macrones, sin espacios ni signos, y con
/// las variantes habituales de cada sistema (ru «j/y», «h/kh»; ko g/k, d/t,
/// b/p, r/l; ja vocales largas «ou», «oo»; zh «v» por «ü»).
class LexicoRom {
  LexicoRom._(this.idioma);
  final String idioma;

  /// Palabra en la escritura del idioma (sin signos ni espacios) → sus
  /// romanizaciones ya normalizadas con [_canon].
  final _palabras = <String, Set<String>>{};
  int _largoMax = 1;

  static const idiomas = {'ru', 'ja', 'ko', 'zh'};
  static final _rutas = <String, RutaCargada>{};
  static final _lexicos = <String, LexicoRom>{};

  /// La ruta de [idioma] alimenta su léxico (se construye al primer uso).
  static void registrar(String idioma, RutaCargada ruta) {
    if (!idiomas.contains(idioma)) return;
    _rutas[idioma] = ruta;
    _lexicos.remove(idioma);
  }

  static LexicoRom? de(String idioma) {
    if (!idiomas.contains(idioma)) return null;
    return _lexicos[idioma] ??= _construir(idioma, _rutas[idioma]);
  }

  static LexicoRom _construir(String idioma, RutaCargada? ruta) {
    final l = LexicoRom._(idioma);
    for (final u in ruta?.unidades ?? const <UnidadRuta>[]) {
      for (final v in u.vocabulario) {
        if (v.rom == null) continue;
        l._par(v.texto.replaceAll(RegExp(r'\s*[(（][^)）]*[)）]'), ''), v.rom!);
        // «検疫 (けんえき)»: la lectura en kana también vale.
        final lectura = RegExp(r'[(（]([^)）]*)[)）]').firstMatch(v.texto);
        if (lectura != null) l._par(lectura.group(1)!, v.rom!);
      }
      for (final p in u.pasos) {
        for (final f in p.frases) {
          if (f.rom != null) l._frase(f.texto, f.rom!);
        }
        for (final fila in p.filas) {
          for (final c in fila) {
            if (c.texto != null && c.rom != null) l._frase(c.texto!, c.rom!);
          }
        }
        for (final it in p.items) {
          for (var i = 0; i < it.tokens.length; i++) {
            final r = romEn(it.tokensRom, i);
            if (r != null) l._par(it.tokens[i], r);
          }
          for (var i = 0; i < it.opciones.length; i++) {
            final o = it.opciones[i].meta, r = romEn(it.opcionesRom, i);
            if (o != null && r != null) l._frase(o, r);
          }
          for (var i = 0; i < it.pares.length; i++) {
            final r = romEn(it.paresRom, i);
            if (r != null) l._frase(it.pares[i].$1, r);
          }
          for (final (t, r) in [
            (it.texto, it.textoRom),
            (it.pregunta, it.preguntaRom),
          ]) {
            if (t != null && r != null && !t.contains('___')) l._frase(t, r);
          }
        }
      }
    }
    return l;
  }

  static final _signos = RegExp(
    '[\\s.,!?¡¿;:"“”«»()（）「」『』。、！？，：；…—–\\-~～・]',
  );
  static String _clave(String s) => s.toLowerCase().replaceAll(_signos, '');

  void _par(String texto, String rom) {
    final k = _clave(texto);
    if (k.isEmpty || !_escritura(idioma).hasMatch(k)) return;
    final c = _canon(rom, idioma);
    if (c.isEmpty) return;
    (_palabras[k] ??= {}).add(c);
    if (k.length > _largoMax) _largoMax = k.length;
  }

  /// Texto y rom con el mismo número de palabras: un par por palabra (y el
  /// texto entero, que sirve para respuestas de una sola pieza).
  void _frase(String texto, String rom) {
    final t = texto.trim().split(RegExp(r'\s+'));
    final r = rom.trim().split(RegExp(r'\s+'));
    if (t.length != r.length) return;
    for (var i = 0; i < t.length; i++) {
      _par(t[i], r[i]);
    }
  }

  /// Formas latinas aceptadas de [nativo] (ya normalizadas); vacío si alguna
  /// parte no se puede romanizar.
  Set<String> formas(String nativo) {
    var res = <String>{''};
    for (final palabra in nativo.trim().split(RegExp(r'\s+'))) {
      final k = _clave(palabra);
      if (k.isEmpty) continue;
      final f = _formasPalabra(k);
      if (f.isEmpty) return const {};
      res = {
        for (final a in res)
          for (final b in f) a + b,
      };
      if (res.length > 64) res = res.take(64).toSet();
    }
    return res.length == 1 && res.first.isEmpty ? const {} : res;
  }

  Set<String> _formasPalabra(String k) {
    final res = <String>{...?_palabras[k]};
    if (idioma == 'ru' && _cirilico.hasMatch(k)) {
      res.add(_canon(_ru(k), 'ru'));
      return res;
    }
    if (idioma == 'ko' && _hangul.hasMatch(k)) {
      for (final r in _ko(k)) {
        res.add(_canon(r, 'ko'));
      }
      return res;
    }
    // Partículas sueltas: は se lee wa y へ, e.
    if (idioma == 'ja' && (k == 'は' || k == 'へ')) res.add(k == 'は' ? 'wa' : 'e');
    if (res.isNotEmpty) return res;
    if (!_escritura(idioma).hasMatch(k)) return {_canon(k, idioma)};
    return _segmentar(k);
  }

  /// ja y zh sin espacios: palabras del léxico y, en japonés, kana suelta.
  Set<String> _segmentar(String k) {
    final en = List<Set<String>>.generate(k.length + 1, (_) => {});
    en[0].add('');
    for (var i = 0; i < k.length; i++) {
      if (en[i].isEmpty) continue;
      void llegar(int fin, Set<String> trozos) {
        for (final a in en[i]) {
          for (final b in trozos) {
            if (en[fin].length < 16) en[fin].add(a + b);
          }
        }
      }

      for (var n = 1; n <= _largoMax && i + n <= k.length; n++) {
        final f = _palabras[k.substring(i, i + n)];
        if (f != null) llegar(i + n, f);
      }
      if (idioma == 'ja') {
        final (fin, rom) = _mora(k, i);
        if (rom != null) llegar(fin, {_canon(rom, 'ja')});
      }
    }
    return en[k.length];
  }
}

final _cirilico = RegExp('[а-яё]');
final _hangul = RegExp('[가-힣]');
RegExp _escritura(String idioma) => switch (idioma) {
  'ru' => _cirilico,
  'ko' => _hangul,
  'ja' => RegExp('[ぁ-ゖァ-ヺー一-鿿]'),
  _ => RegExp('[一-鿿]'),
};

/// ¿Hay algo en la escritura del idioma?
bool tieneEscritura(String s, String idioma) =>
    LexicoRom.idiomas.contains(idioma) &&
    _escritura(idioma).hasMatch(s.toLowerCase());

/// La respuesta latina [dada] corresponde a alguna de [validas] (en la
/// escritura del idioma).
bool aceptaRomanizada(String idioma, Iterable<String> validas, String dada) {
  if (tieneEscritura(dada, idioma) || !RegExp('[a-zA-Z]').hasMatch(dada)) {
    return false;
  }
  final lexico = LexicoRom.de(idioma);
  if (lexico == null) return false;
  final c = _canon(dada, idioma);
  if (c.isEmpty) return false;
  return validas.any(
    (v) => tieneEscritura(v, idioma) && lexico.formas(v).contains(c),
  );
}

const _sinMarca = {
  'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a', 'ā': 'a', 'ǎ': 'a',
  'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'ē': 'e', 'ě': 'e',
  'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i', 'ī': 'i', 'ǐ': 'i',
  'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o', 'ō': 'o', 'ǒ': 'o', 'ŏ': 'o',
  'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u', 'ū': 'u', 'ǔ': 'u', 'ŭ': 'u',
  'ǖ': 'u', 'ǘ': 'u', 'ǚ': 'u', 'ǜ': 'u', 'ý': 'y', 'ÿ': 'y',
};

/// Forma de comparación: minúsculas, sin marcas ni signos y con las
/// variantes de cada sistema unificadas.
String _canon(String s, String idioma) {
  var t = s
      .toLowerCase()
      .split('')
      .map((c) => _sinMarca[c] ?? c)
      .join()
      .replaceAll(RegExp('[^a-z]'), '');
  switch (idioma) {
    case 'ru':
      t = t
          .replaceAll(RegExp('shch|sch|shh'), 'Ŝ')
          .replaceAll('kh', 'h')
          .replaceAll('x', 'h')
          .replaceAll('ts', 'c')
          .replaceAll('j', 'y')
          .replaceAll('Ŝ', 'shch')
          .replaceAll(RegExp('iy\$|yy\$'), 'i')
          .replaceAll(RegExp('(?<=^|[aeiou])ye'), 'e');
    case 'ko':
      t = t
          .replaceAllMapped(RegExp('(kk|tt|pp|ss|jj)'), (m) => m[0]![0])
          .replaceAll('g', 'k')
          .replaceAll('d', 't')
          .replaceAll('b', 'p')
          .replaceAll('r', 'l');
    case 'ja':
      t = t
          .replaceAll('ou', 'o')
          .replaceAllMapped(RegExp('([aeiou])\\1+'), (m) => m[1]!)
          .replaceAll('nn', 'n');
    case 'zh':
      t = t.replaceAll('v', 'u');
  }
  return t;
}

// --- Ruso: transliteración de tools/ia/idiomas/ru.md (sin acento) ---------

const _ruMapa = {
  'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ж': 'zh', 'з': 'z',
  'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
  'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh',
  'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
  'э': 'e', 'ю': 'yu', 'я': 'ya', 'ё': 'yo',
};

String _ru(String palabra) {
  final b = StringBuffer();
  for (var i = 0; i < palabra.length; i++) {
    final c = palabra[i];
    final previa = i == 0 ? '' : palabra[i - 1];
    if (c == 'е') {
      b.write(i == 0 || 'аеёиоуыэюяьъ'.contains(previa) ? 'ye' : 'e');
    } else {
      b.write(_ruMapa[c] ?? c);
    }
  }
  return b.toString();
}

// --- Coreano: Romanización Revisada con enlace y asimilaciones comunes ----

const _koInicial = [
  'g', 'kk', 'n', 'd', 'tt', 'r', 'm', 'b', 'pp', 's', 'ss', '', 'j', 'jj',
  'ch', 'k', 't', 'p', 'h',
];
const _koVocal = [
  'a', 'ae', 'ya', 'yae', 'eo', 'e', 'yeo', 'ye', 'o', 'wa', 'wae', 'oe',
  'yo', 'u', 'wo', 'we', 'wi', 'yu', 'eu', 'ui', 'i',
];

/// Final de sílaba (índice 0–27): cómo suena al cerrar y qué pasa a la
/// sílaba siguiente si esta empieza por vocal (enlace).
const _koFinal = [
  ('', ''), ('k', 'g'), ('k', 'kk'), ('k', 'gs'), ('n', 'n'), ('n', 'nj'),
  ('n', 'n'), ('t', 'd'), ('l', 'r'), ('k', 'lg'), ('m', 'lm'), ('l', 'lb'),
  ('l', 'ls'), ('l', 'lt'), ('p', 'lp'), ('l', 'r'), ('m', 'm'), ('p', 'b'),
  ('p', 'bs'), ('t', 's'), ('t', 'ss'), ('ng', 'ng'), ('t', 'j'), ('t', 'ch'),
  ('k', 'k'), ('t', 't'), ('p', 'p'), ('t', ''),
];

/// Romanizaciones de una palabra en hangul: con los cambios fonéticos (como
/// el curso: 감사합니다 → gamsahamnida) y sílaba a sílaba.
Set<String> _ko(String palabra) {
  final silabas = <(int, int, int)>[];
  final otros = <int, String>{};
  for (final r in palabra.runes) {
    if (r >= 0xAC00 && r <= 0xD7A3) {
      final c = r - 0xAC00;
      silabas.add((c ~/ 588, (c % 588) ~/ 28, c % 28));
    } else {
      otros[silabas.length] = (otros[silabas.length] ?? '') +
          String.fromCharCode(r);
    }
  }
  final suelta = StringBuffer(), fonetica = StringBuffer();
  for (var i = 0; i < silabas.length; i++) {
    final (ini, voc, fin) = silabas[i];
    final previa = i == 0 ? null : silabas[i - 1];
    suelta
      ..write(otros[i] ?? '')
      ..write(_koInicial[ini])
      ..write(_koVocal[voc])
      ..write(_koFinal[fin].$1);
    // Inicial según el final anterior.
    var inicial = _koInicial[ini];
    if (previa != null && previa.$3 != 0) {
      final cierre = _koFinal[previa.$3].$1;
      if (ini == 11 && previa.$3 != 21) {
        final paso = _koFinal[previa.$3].$2;
        inicial = paso.length > 1 && paso.startsWith('l') ? paso.substring(1) : paso;
        if (paso == 'gs' || paso == 'bs') inicial = 's';
      } else if (ini == 5) {
        inicial = cierre == 'l' || cierre == 'n' ? 'l' : 'n';
      } else if (ini == 2 && cierre == 'l') {
        inicial = 'l';
      }
    }
    fonetica.write(otros[i] ?? '');
    fonetica
      ..write(inicial)
      ..write(_koVocal[voc]);
    // Final según la inicial siguiente.
    if (fin != 0) {
      final siguiente = i + 1 < silabas.length ? silabas[i + 1].$1 : null;
      var cierre = _koFinal[fin].$1;
      if (siguiente == 11 && fin != 21) {
        final paso = _koFinal[fin].$2;
        cierre = paso.length > 1 && paso.startsWith('l') ? 'l' : '';
        if (paso == 'gs') cierre = 'k';
        if (paso == 'bs') cierre = 'p';
      } else if (siguiente == 2 || siguiente == 6 || siguiente == 5) {
        // Nasalización: k → ng, t → n, p → m ante n, m (y ante r, que pasa a n).
        cierre = switch (cierre) {
          'k' => 'ng',
          't' => 'n',
          'p' => 'm',
          'n' when siguiente == 5 => 'l',
          _ => cierre,
        };
      }
      fonetica.write(cierre);
    }
  }
  suelta.write(otros[silabas.length] ?? '');
  fonetica.write(otros[silabas.length] ?? '');
  return {suelta.toString(), fonetica.toString()};
}

// --- Japonés: kana → rōmaji Hepburn, una mora por paso -------------------

const _kanaRom = {
  'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
  'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
  'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
  'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
  'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
  'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
  'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
  'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
  'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
  'わ': 'wa', 'ゐ': 'i', 'ゑ': 'e', 'を': 'o', 'ん': 'n',
  'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
  'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
  'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
  'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
  'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po', 'ゔ': 'vu',
  'ぁ': 'a', 'ぃ': 'i', 'ぅ': 'u', 'ぇ': 'e', 'ぉ': 'o',
};
const _pequenas = {'ゃ': 'ya', 'ゅ': 'yu', 'ょ': 'yo'};
const _vocalPequena = {'ぁ': 'a', 'ぃ': 'i', 'ぅ': 'u', 'ぇ': 'e', 'ぉ': 'o'};

/// Katakana → hiragana (la ー se queda).
String _hira(String c) {
  final r = c.codeUnitAt(0);
  return r >= 0x30A1 && r <= 0x30F6 ? String.fromCharCode(r - 0x60) : c;
}

/// Una mora desde [i] (con su ゃ/ぁ pequeña, la っ anterior y la ー
/// siguiente): (posición final, rōmaji) o (i, null) si no es kana.
(int, String?) _mora(String k, int i) {
  var j = i;
  var doble = false;
  if (_hira(k[j]) == 'っ') {
    doble = true;
    j++;
    if (j >= k.length) return (i, null);
  }
  final c = _hira(k[j]);
  var rom = _kanaRom[c];
  if (rom == null) return (i, null);
  j++;
  if (j < k.length) {
    final p = _hira(k[j]);
    final y = _pequenas[p], v = _vocalPequena[p];
    if (y != null && rom.endsWith('i') && rom.length > 1) {
      final base = rom.substring(0, rom.length - 1);
      rom = base.endsWith('h') || base == 'j' ? base + y.substring(1) : base + y;
      j++;
    } else if (v != null) {
      final base = rom == 'u' ? 'w' : rom.substring(0, rom.length - 1);
      rom = base + v;
      j++;
    }
  }
  while (j < k.length && k[j] == 'ー') {
    j++;
  }
  if (doble) rom = (rom.startsWith('ch') ? 't' : rom[0]) + rom;
  return (j, rom);
}
