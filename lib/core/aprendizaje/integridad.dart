import 'correccion.dart';
import 'grafo.dart';
import 'modelos.dart';

final _puntuacion = RegExp(r'[.,!?¡¿;:。、！？「」…"“”„()«»‹›—–，：；]');

/// Palabras de un texto en el idioma meta (misma regla que tools/validar_ruta.py).
List<String> palabrasMeta(String texto) => texto
    .replaceAll('’', "'")
    .replaceAll('‘', "'")
    .replaceAll('‚', "'")
    .replaceAll('___', ' ')
    .toLowerCase()
    .replaceAll(_puntuacion, ' ')
    .split(RegExp(r'\s+'))
    // Comillas simples de cita ('once', shopkeepers', alemán ‚so‘) no son
    // parte de la palabra.
    .map((p) => p.replaceAll(RegExp(r"^'+|'+$"), ''))
    .where((p) => p.isNotEmpty && p != '-')
    .toList();

/// Formas base posibles de una flexión regular inglesa (misma regla que
/// `bases` en tools/validar_ruta.py).
Set<String> basesFlexion(String w) {
  final res = <String>{};
  if (w.endsWith("'s")) res.add(w.substring(0, w.length - 2));
  const sufijos = [
    ('ies', ['y']),
    ('ied', ['y']),
    ('iest', ['y']),
    ('ier', ['y']),
    ('es', ['', 'e']),
    ('s', ['']),
    ('ed', ['', 'e']),
    ('d', ['']),
    ('ing', ['', 'e']),
    ('est', ['', 'e']),
    ('er', ['', 'e']),
  ];
  for (final (suf, reemplazos) in sufijos) {
    if (w.endsWith(suf) && w.length - suf.length >= 2) {
      final raiz = w.substring(0, w.length - suf.length);
      for (final r in reemplazos) {
        res.add(raiz + r);
      }
      if (raiz.length >= 3 && raiz[raiz.length - 1] == raiz[raiz.length - 2]) {
        res.add(raiz.substring(0, raiz.length - 1));
      }
    }
  }
  return res;
}

bool palabraConocida(String w, Set<String> conocidas) =>
    conocidas.contains(w) ||
    RegExp(r'\d').hasMatch(w) ||
    basesFlexion(w).any(conocidas.contains);

/// Forma conjugada → infinitivos, a partir de `verbos.json` (misma regla que
/// `formas_verbales` en tools/validar_ruta.py): cuentan las celdas de todas las
/// tablas y las formas sueltas.
Map<String, Set<String>> indiceFormasVerbales(Map<String, dynamic> verbos) {
  final res = <String, Set<String>>{};
  for (final v in verbos['verbos'] as List? ?? const []) {
    final infinitivo = (v['infinitivo'] as String).toLowerCase();
    final formas = [
      for (final t in (v['tablas'] as Map? ?? const {}).values)
        ...List<String>.from(t as List),
      // El auxiliar del alemán (haben/sein) no es una forma del verbo.
      for (final MapEntry(:key, :value)
          in (v['formas'] as Map? ?? const {}).entries)
        if (key != 'auxiliar' && value is String) value,
    ];
    for (final f in formas) {
      for (final w in palabrasMeta(f)) {
        res.putIfAbsent(w, () => {}).add(infinitivo);
      }
    }
  }
  return res;
}

/// Formas base posibles de una flexión nominal portuguesa, número y género
/// (misma regla que `bases_pt` en tools/validar_ruta.py).
Set<String> basesFlexionPt(String w) {
  final res = <String>{};
  const sufijos = [
    ('ões', ['ão']),
    ('ães', ['ão']),
    ('ãos', ['ão']),
    ('ais', ['al']),
    ('éis', ['el']),
    ('eis', ['el', 'il']),
    ('óis', ['ol']),
    ('uis', ['ul']),
    ('is', ['il']),
    ('ns', ['m']),
    ('es', ['']),
    ('s', ['']),
  ];
  for (final (suf, reemplazos) in sufijos) {
    if (w.endsWith(suf) && w.length - suf.length >= 2) {
      final raiz = w.substring(0, w.length - suf.length);
      for (final r in reemplazos) {
        res.add(raiz + r);
      }
    }
  }
  // Femenino → masculino (aberta → aberto), también sobre los singulares ya
  // obtenidos (brasileiras → brasileira → brasileiro).
  for (final f in [w, ...res]) {
    if (f.endsWith('a') && f.length >= 3) {
      final raiz = f.substring(0, f.length - 1);
      res.addAll(['${raiz}o', '${raiz}e']);
      if (f.endsWith('ora')) res.add(raiz); // professora → professor
    }
  }
  return res;
}

/// Terminaciones de los verbos regulares (presente, pretérito, imperfecto,
/// futuro, condicional, subjuntivos, participio y gerundio) por vocal temática.
const _desinenciasPt = {
  'a': [
    'o', 'a', 'as', 'amos', 'am', 'ei', 'ou', 'aram', 'ava', 'avas', //
    'ávamos', 'avam', 'e', 'es', 'emos', 'em', 'ado', 'ada', 'ados', 'adas',
    'ando', 'asse', 'assem', 'ássemos', 'armos', 'arem', 'arei', 'ará',
    'aremos', 'arão', 'aria', 'ariam', 'aríamos',
  ],
  'e': [
    'o', 'e', 'es', 'emos', 'em', 'i', 'eu', 'eram', 'ia', 'ias', 'íamos', //
    'iam', 'a', 'as', 'amos', 'am', 'ido', 'ida', 'idos', 'idas', 'endo',
    'esse', 'essem', 'ermos', 'erem', 'erei', 'erá', 'eremos', 'erão', 'eria',
    'eriam', 'eríamos',
  ],
  'i': [
    'o', 'e', 'es', 'imos', 'em', 'i', 'iu', 'iram', 'ia', 'ias', 'íamos', //
    'iam', 'a', 'as', 'amos', 'am', 'ido', 'ida', 'idos', 'idas', 'indo',
    'isse', 'issem', 'irmos', 'irem', 'irei', 'irá', 'iremos', 'irão', 'iria',
    'iriam', 'iríamos',
  ],
};

/// Cambios ortográficos ante e: liguei/ligue (ligar), fiquei (ficar),
/// comecei (começar).
const _ortografiaPt = [('gu', 'g'), ('qu', 'c'), ('c', 'ç')];

/// Infinitivos posibles de una forma de verbo regular portugués (misma regla
/// que `infinitivos_pt` en tools/validar_ruta.py).
Set<String> infinitivosPt(String w) {
  final res = <String>{};
  for (final MapEntry(key: vocal, value: desinencias)
      in _desinenciasPt.entries) {
    for (final d in desinencias) {
      if (w.endsWith(d) && w.length - d.length >= 2) {
        final raiz = w.substring(0, w.length - d.length);
        res.add('$raiz${vocal}r');
        for (final (antes, despues) in _ortografiaPt) {
          if (raiz.endsWith(antes)) {
            final sinCambio = raiz.substring(0, raiz.length - antes.length);
            res.add('$sinCambio$despues${vocal}r');
          }
        }
      }
    }
  }
  // Gerundio de verbos cortos: indo (ir), sendo (ser), tendo (ter), pondo (pôr).
  if (['ando', 'endo', 'indo'].any(w.endsWith)) {
    res.add('${w.substring(0, w.length - 3)}r');
  }
  if (w == 'pondo') res.add('pôr');
  return res;
}

/// Clítico tras guion → formas base que deben estar enseñadas («-la» = «a»).
const _cliticosPt = {
  'se': {'se'},
  'me': {'me'},
  'te': {'te'},
  'lhe': {'lhe'},
  'lhes': {'lhe', 'lhes'},
  'o': {'o'},
  'a': {'a'},
  'os': {'os', 'o'},
  'as': {'as', 'a'},
  'lo': {'o'},
  'la': {'a'},
  'los': {'os', 'o'},
  'las': {'as', 'a'},
  'no': {'o'},
  'na': {'a'},
  'nos': {'nos', 'os', 'o'},
  'nas': {'as', 'a'},
};

/// «deixá-la» ← deixar, «fazê-lo» ← fazer, «pô-lo» ← pôr; «parti-lo» queda en
/// «parti» → partir.
const _infinitivoPt = {'á': 'ar', 'ê': 'er', 'ô': 'or', 'i': 'ir'};

/// Como [palabraConocida], aceptando además plurales/femeninos de palabras
/// enseñadas y formas conjugadas de verbos cuyo infinitivo ya se enseñó
/// (misma regla que `conocida_pt` en tools/validar_ruta.py). [formasVerbales]
/// es el índice de [indiceFormasVerbales] sobre `assets/contenido/pt/verbos.json`.
bool palabraConocidaPt(
  String w,
  Set<String> conocidas, [
  Map<String, Set<String>> formasVerbales = const {},
]) {
  if (palabraConocida(w, conocidas) ||
      basesFlexionPt(w).any(conocidas.contains)) {
    return true;
  }
  if ((formasVerbales[w] ?? const <String>{}).any(conocidas.contains) ||
      infinitivosPt(w).any(conocidas.contains)) {
    return true;
  }
  // Ênclise: «registra-se», «deixá-la», «fazê-lo»; el clítico cuenta si se
  // enseñó su forma base («-la» tras «deixá» = «a»).
  final guion = w.indexOf('-');
  if (guion < 0) return false;
  final verbo = w.substring(0, guion);
  final clitico = w.substring(guion + 1);
  if (clitico.contains('-') ||
      !(_cliticosPt[clitico] ?? const <String>{}).any(conocidas.contains)) {
    return false;
  }
  final ultima = verbo.isEmpty ? '' : verbo[verbo.length - 1];
  final sinAcento = _infinitivoPt[ultima];
  return {
    verbo,
    if (sinAcento != null) verbo.substring(0, verbo.length - 1) + sinAcento,
  }.any((v) => palabraConocidaPt(v, conocidas, formasVerbales));
}

// ── Alemán ──────────────────────────────────────────────────────────────────
// Heurística como la del portugués: una forma cuenta si su base ya se enseñó.
// Misma regla que `conocida_de` en tools/validar_ruta.py.

const _altGrafiaDe = {'ss': 'ß', 'ae': 'ä', 'oe': 'ö', 'ue': 'ü'};

/// La palabra con ß/ss, ä/ae, ö/oe y ü/ue intercambiadas (máx. 64 grafías;
/// misma regla que `grafias_de` en tools/validar_ruta.py).
Set<String> grafiasDe(String w) {
  final plano = w
      .replaceAll('ß', 'ss')
      .replaceAll('ä', 'ae')
      .replaceAll('ö', 'oe')
      .replaceAll('ü', 'ue');
  var res = [''];
  var i = 0;
  while (i < plano.length) {
    final par = i + 2 <= plano.length ? plano.substring(i, i + 2) : '';
    final alt = _altGrafiaDe[par];
    if (alt != null && res.length < 64) {
      res = [
        for (final r in res) ...['$r$par', '$r$alt'],
      ];
      i += 2;
    } else {
      final c = plano[i];
      res = [for (final r in res) '$r$c'];
      i += 1;
    }
  }
  return res.toSet();
}

/// Quita la última diéresis: äpfel → apfel, häuser → hauser, läuft → lauft.
Set<String> _sinUmlautDe(String w) {
  final res = <String>{};
  for (final (a, b) in const [
    ('äu', 'au'),
    ('ä', 'a'),
    ('ö', 'o'),
    ('ü', 'u'),
  ]) {
    final i = w.lastIndexOf(a);
    if (i >= 0) res.add(w.substring(0, i) + b + w.substring(i + a.length));
  }
  return res;
}

Set<String> _quitarDe(String w, List<String> sufijos, [int minimo = 2]) => {
  for (final s in sufijos)
    if (w.endsWith(s) && w.length - s.length >= minimo)
      w.substring(0, w.length - s.length),
};

/// Plural, caso y terminación de adjetivo; luego grado.
const _sufNominalDe = [
  'ern', 'nen', 'sen', 'ens', 'en', 'em', 'er', 'es', 'se', 'e', 'n', 's', //
];
const _sufGradoDe = ['est', 'st', 'er'];
const _gradoIrregDe = {
  'besser': 'gut',
  'best': 'gut',
  'mehr': 'viel',
  'meist': 'viel',
  'lieber': 'gern',
  'liebst': 'gern',
  'höher': 'hoch',
  'höchst': 'hoch',
  'nächst': 'nah',
  'größt': 'groß',
};

/// Palabras que parecen flexión de otra y no lo son (aber ≠ ab+er, dass ≠ das+s…).
const _noDerivarDe = {
  'aber', 'unser', 'euer', 'denen', 'deren', 'wenn', 'denn', 'das', 'dass', //
  'neun', 'ihnen', 'etwas', 'ins', 'eins',
};

/// Bases posibles de una flexión nominal/adjetival alemana: plural (-e, -er,
/// -n, -en, -s, -nen, -se, con diéresis), -n/-s/-es de caso, terminaciones de
/// adjetivo y grado (misma regla que `bases_de` en tools/validar_ruta.py).
Set<String> basesFlexionDe(String w) {
  if (_noDerivarDe.contains(w)) return {};
  final n1 = _quitarDe(w, _sufNominalDe);
  final res = {...n1};
  for (final x in {w, ...n1}) {
    if (_noDerivarDe.contains(x)) continue;
    final irreg = _gradoIrregDe[x];
    if (irreg != null) res.add(irreg);
    res.addAll(_quitarDe(x, _sufGradoDe));
  }
  for (final x in {...res, w}) {
    res.addAll(_sinUmlautDe(x));
  }
  for (final x in {...res}) {
    // e caída del tema: dunkle → dunkel, teure → teuer.
    if (x.length >= 3 &&
        'lr'.contains(x[x.length - 1]) &&
        x[x.length - 2] != 'e') {
      res.add('${x.substring(0, x.length - 1)}e${x[x.length - 1]}');
    }
  }
  res.remove(w);
  return res;
}

Map<String, Set<String>> _formaAInfDe(Map<String, String> tabla) {
  final res = <String, Set<String>>{};
  for (final MapEntry(key: inf, value: formas) in tabla.entries) {
    for (final f in formas.split(' ')) {
      res.putIfAbsent(f, () => {}).add(inf);
    }
  }
  return res;
}

/// Formas sueltas (presente irregular, Präteritum y Konjunktiv II de
/// sein/haben/werden).
final _formasIrregDe = _formaAInfDe(const {
  'sein':
      'bin bist ist sind seid sei seien seist war warst waren wart wäre wärst '
      'wären wärt wäret wärest',
  'haben': 'hast hat hatte hattest hatten hattet hätte hättest hätten hättet',
  'werden':
      'wirst wird wurde wurdest wurden wurdet würde würdest würden würdet',
  'wissen': 'weiß weißt',
  'können': 'kann kannst',
  'müssen': 'muss musst',
  'wollen': 'will willst',
  'dürfen': 'darf darfst',
  'sollen': 'soll sollst',
  'mögen': 'mag magst',
  'tun': 'tu tue tust tut tun',
  'nehmen': 'nimm nimmst nimmt',
  'treten': 'tritt trittst',
  'halten': 'hält hältst',
  'gelten': 'gilt',
  'raten': 'rät rätst',
  'laden': 'lädt',
});

/// Bases de Präteritum fuerte/mixto y de Konjunktiv II; admiten -st/-t/-en/-n
/// detrás (gingen, kamst, könntest, wüssten).
final _basesIrregDe = _formaAInfDe(const {
  'gehen': 'ging ginge', 'kommen': 'kam käme', 'sehen': 'sah sähe', //
  'geben': 'gab gäbe', 'finden': 'fand fände', 'lesen': 'las', 'essen': 'aß',
  'trinken': 'trank', 'sprechen': 'sprach', 'nehmen': 'nahm', 'fahren': 'fuhr',
  'laufen': 'lief', 'bleiben': 'blieb', 'schreiben': 'schrieb',
  'stehen': 'stand', 'sitzen': 'saß', 'liegen': 'lag', 'rufen': 'rief',
  'denken': 'dachte', 'bringen': 'brachte', 'kennen': 'kannte',
  'nennen': 'nannte', 'rennen': 'rannte', 'wissen': 'wusste wüsste',
  'tun': 'tat täte', 'heißen': 'hieß', 'schlafen': 'schlief',
  'treffen': 'traf', 'fliegen': 'flog', 'helfen': 'half',
  'beginnen': 'begann', 'ziehen': 'zog', 'tragen': 'trug', 'fallen': 'fiel',
  'halten': 'hielt', 'lassen': 'ließ', 'waschen': 'wusch', 'singen': 'sang',
  'schwimmen': 'schwamm', 'gewinnen': 'gewann', 'sterben': 'starb',
  'steigen': 'stieg', 'schneiden': 'schnitt', 'verlieren': 'verlor',
  'vergessen': 'vergaß', 'empfehlen': 'empfahl', 'bitten': 'bat',
  'schließen': 'schloss', 'bieten': 'bot', 'greifen': 'griff',
  'scheinen': 'schien', 'fangen': 'fing', 'können': 'konnte könnte',
  'müssen': 'musste müsste', 'dürfen': 'durfte dürfte',
  'mögen': 'mochte möchte', 'wollen': 'wollte', 'sollen': 'sollte',
});

/// Partizip II fuerte/mixto sin ge- (gegangen, verstanden ← ver+standen).
final _partizipDe = _formaAInfDe(const {
  'gehen': 'gangen', 'sein': 'wesen', 'werden': 'worden', //
  'trinken': 'trunken', 'finden': 'funden', 'schreiben': 'schrieben',
  'sprechen': 'sprochen', 'nehmen': 'nommen', 'bleiben': 'blieben',
  'essen': 'gessen', 'treffen': 'troffen', 'stehen': 'standen',
  'helfen': 'holfen', 'wissen': 'wusst', 'denken': 'dacht',
  'bringen': 'bracht', 'kennen': 'kannt', 'nennen': 'nannt',
  'rennen': 'rannt', 'fliegen': 'flogen', 'ziehen': 'zogen',
  'sitzen': 'sessen', 'liegen': 'legen', 'sterben': 'storben',
  'schwimmen': 'schwommen', 'singen': 'sungen', 'gewinnen': 'wonnen',
  'ginnen': 'gonnen', 'steigen': 'stiegen', 'schneiden': 'schnitten',
  'tun': 'tan', 'mögen': 'mocht', 'können': 'konnt', 'müssen': 'musst',
  'dürfen': 'durft', 'lieren': 'loren', 'gebären': 'boren',
  'bitten': 'beten', 'schließen': 'schlossen', 'bieten': 'boten',
  'greifen': 'griffen', 'scheinen': 'schienen', 'leihen': 'liehen',
  'schweigen': 'schwiegen',
});

const _separablesDe = [
  'zusammen', 'zurück', 'vorbei', 'weiter', 'wieder', 'kennen', 'fern', //
  'fest', 'nach', 'teil', 'auf', 'aus', 'ein', 'mit', 'vor', 'weg', 'los',
  'bei', 'her', 'hin', 'ab', 'an', 'um', 'zu',
];
const _inseparablesDe = ['miss', 'emp', 'ent', 'zer', 'ver', 'be', 'er'];

Set<String> _regularDe(String raiz) {
  final res = {'${raiz}en'};
  if (raiz.endsWith('el') || raiz.endsWith('er')) res.add('${raiz}n');
  if (raiz.length >= 3 &&
      'lr'.contains(raiz[raiz.length - 1]) &&
      raiz[raiz.length - 2] != 'e') {
    // sammle → sammeln
    res.add('${raiz.substring(0, raiz.length - 1)}e${raiz[raiz.length - 1]}n');
  }
  return res;
}

/// Raíz de presente con cambio vocálico → raíz del infinitivo (liest, gibt, fährt).
Set<String> _cambioVocalDe(String raiz) {
  final res = _sinUmlautDe(raiz);
  var i = raiz.lastIndexOf('ie');
  if (i >= 0) res.add('${raiz.substring(0, i)}e${raiz.substring(i + 2)}');
  i = raiz.lastIndexOf('i');
  if (i >= 0) res.add('${raiz.substring(0, i)}e${raiz.substring(i + 1)}');
  return res;
}

String _sinFinal(String w, String e) => w.substring(0, w.length - e.length);

/// Infinitivos posibles de una forma verbal alemana (misma regla que
/// `infinitivos_de` en tools/validar_ruta.py).
Set<String> infinitivosDe(
  String w, {
  bool prefijos = true,
  bool sinGe = false,
}) {
  final res = <String>{};
  for (final e in const ['', 'st', 't', 'n', 'en', 'est', 'et']) {
    if (w.endsWith(e) && w.length - e.length >= 2) {
      res.addAll(_basesIrregDe[_sinFinal(w, e)] ?? const {});
    }
  }
  res.addAll(_formasIrregDe[w] ?? const {});
  // Presente (e de unión: arbeitest, wartet; wir/sie = infinitivo) e
  // imperativo (komm, geh).
  for (final e in const ['est', 'et', 'st', 'en', 't', 'e', 'n', '']) {
    if (w.endsWith(e) && w.length - e.length >= 2) {
      final raiz = _sinFinal(w, e);
      res.addAll(_regularDe(raiz));
      if (const ['est', 'st', 't', ''].contains(e)) {
        for (final r in _cambioVocalDe(raiz)) {
          res.addAll(_regularDe(r));
        }
      }
    }
  }
  // Präteritum regular: machte, arbeiteten.
  for (final e in const [
    'etest', 'etet', 'eten', 'ete', 'test', 'tet', 'ten', 'te', //
  ]) {
    if (w.endsWith(e) && w.length - e.length >= 2) {
      res.addAll(_regularDe(_sinFinal(w, e)));
    }
  }
  // Partizip II: ge-…-(e)t regular, ge-…-en fuerte y la tabla de irregulares.
  final nucleos = [
    if (sinGe) w,
    if (w.startsWith('ge') && w.length >= 5) w.substring(2),
  ];
  for (final n in nucleos) {
    res.addAll(_partizipDe[n] ?? const {});
    for (final e in const ['et', 't', 'en']) {
      if (n.endsWith(e) && n.length - e.length >= 2) {
        res.addAll(_regularDe(_sinFinal(n, e)));
      }
    }
  }
  if (prefijos) {
    for (final p in _inseparablesDe) {
      if (w.startsWith(p) && w.length - p.length >= 3) {
        res.addAll({
          for (final i in infinitivosDe(
            w.substring(p.length),
            prefijos: false,
            sinGe: true,
          ))
            '$p$i',
        });
      }
    }
    for (final p in _separablesDe) {
      if (w.startsWith(p) && w.length - p.length >= 3) {
        final resto = w.substring(p.length);
        // anzurufen → anrufen; angerufen → an + gerufen.
        for (final r in {
          resto,
          if (resto.startsWith('zu') && resto.length >= 5) resto.substring(2),
        }) {
          res.addAll({
            for (final i in infinitivosDe(r, prefijos: false)) '$p$i',
          });
        }
      }
    }
  }
  return res;
}

/// Como [palabraConocida] (sin la morfología inglesa), aceptando además
/// flexiones alemanas de palabras enseñadas: plurales, caso, adjetivos y
/// grado, formas verbales (presente, Präteritum, Konjunktiv II, Partizip II,
/// separables) y grafías ß/ss, ä/ae, ö/oe, ü/ue. Las mayúsculas ya las quita
/// [palabrasMeta]. Misma regla que `conocida_de` en tools/validar_ruta.py;
/// [formasVerbales] es el índice de [indiceFormasVerbales] sobre
/// `assets/contenido/de/verbos.json` (si existe).
bool palabraConocidaDe(
  String w,
  Set<String> conocidas, [
  Map<String, Set<String>> formasVerbales = const {},
]) {
  if (conocidas.contains(w) || RegExp(r'\d').hasMatch(w)) return true;
  for (final g in grafiasDe(w)) {
    final infs = infinitivosDe(g);
    // Participio declinado como adjetivo: gekochte, geschlossenen.
    for (final x in _quitarDe(g, const ['e', 'en', 'em', 'er', 'es'], 4)) {
      if (x.endsWith('t') || x.endsWith('en')) infs.addAll(infinitivosDe(x));
    }
    // Verbo separable con el prefijo aparte en la frase: «ich rufe … an».
    infs.addAll({
      for (final i in [...infs])
        for (final p in _separablesDe) '$p$i',
    });
    final candidatos = {
      g,
      ...basesFlexionDe(g),
      ...?formasVerbales[g],
      ...infs,
    };
    if (candidatos.any((c) => grafiasDe(c).any(conocidas.contains))) {
      return true;
    }
  }
  // El prefijo separado («an», «auf») cuenta si se enseñó un verbo con él.
  return _separablesDe.contains(w) &&
      conocidas.any(
        (c) =>
            c.startsWith(w) &&
            c.length >= w.length + 4 &&
            c.endsWith('n') &&
            !_separablesDe.contains(c),
      );
}

/// Problemas pedagógicos y de datos de una ruta. Vacío = íntegra.
///
/// En portugués y alemán valen además las flexiones de lo enseñado
/// ([palabraConocidaPt], [palabraConocidaDe]); [formasVerbales] (ver
/// `CargadorRuta.formasVerbales`) añade las formas irregulares de su
/// `verbos.json`. Sin él la comprobación solo es más estricta, nunca más laxa.
List<String> problemasDeContenido(
  RutaCargada ruta, {
  Map<String, Set<String>> formasVerbales = const {},
}) {
  final errores = [...validarGrafo(ruta.unidades)];
  final bool Function(String, Set<String>) conocida =
      switch (ruta.curso.idioma) {
        'pt' => (w, saber) => palabraConocidaPt(w, saber, formasVerbales),
        'de' => (w, saber) => palabraConocidaDe(w, saber, formasVerbales),
        _ => palabraConocida,
      };
  final apoyos = ruta.curso.idiomasApoyo;
  final libres = {
    for (final p in ruta.curso.palabrasLibres) ...palabrasMeta(p),
  };

  void apoyo(TextoApoyo? t, String donde) {
    for (final l in apoyos) {
      if ((t?.porIdioma[l] ?? '').trim().isEmpty) {
        errores.add('$donde: falta texto de apoyo "$l"');
      }
    }
  }

  Iterable<UnidadRuta> cadena(UnidadRuta u) => [
    for (final id in {u.id, ...prerequisitosTransitivos(ruta, u.id)})
      ruta.unidad(id)!,
  ];
  Set<String> conocidas(UnidadRuta u) => {
    ...libres,
    for (final x in cadena(u)) ...[
      for (final v in x.vocabulario) ...palabrasMeta(v.texto),
      // Las celdas de las tablas (escrituras, conjugaciones) también enseñan.
      for (final p in x.pasos)
        for (final fila in p.filas)
          for (final c in fila) ...palabrasMeta(c.texto ?? ''),
    ],
  };
  // Las formas incorrectas enseñadas como error solo valen como distractor.
  Set<String> distractores(UnidadRuta u) => {
    ...conocidas(u),
    for (final x in cadena(u))
      for (final e in x.erroresFrecuentes)
        ...palabrasMeta(e.incorrecto.replaceAll(RegExp(r'\([^)]*\)'), ' ')),
  };

  for (final u in ruta.unidades) {
    final saber = conocidas(u);
    final saberDistractor = distractores(u);
    void meta(String? texto, String donde, {bool distractor = false}) {
      if (texto == null) return;
      final validas = distractor ? saberDistractor : saber;
      final faltan = palabrasMeta(texto)
          .where((w) => !conocida(w, validas))
          .toSet();
      if (faltan.isNotEmpty) {
        errores.add('$donde: palabras no enseñadas ${faltan.join(', ')}');
      }
    }

    apoyo(u.titulo, '${u.id}.titulo');
    apoyo(u.objetivo, '${u.id}.objetivo');
    for (final v in u.vocabulario) {
      apoyo(v.traduccion, '${u.id}.${v.id}');
    }
    if (u.pasos.isEmpty || !u.pasos.first.tipo.ensena) {
      errores.add('${u.id}: no empieza enseñando');
    }
    if (u.pasos.isNotEmpty && u.pasos.last.tipo != TipoPaso.evaluacion) {
      errores.add('${u.id}: la evaluación no es el último paso');
    }
    // Enseñar → guiada → independiente → situación → evaluación.
    var rango = -1;
    for (final p in u.pasos) {
      final r = switch (p.tipo) {
        _ when p.tipo.ensena => 0,
        TipoPaso.practicaGuiada => 1,
        TipoPaso.practicaIndependiente => 2,
        TipoPaso.situacion => 3,
        _ => 4,
      };
      if (r < rango) errores.add('${u.id}.${p.id}: paso fuera de orden');
      if (r > rango) rango = r;
      if (p.texto != null || p.tipo == TipoPaso.explicacion) {
        apoyo(p.texto, '${u.id}.${p.id}.texto');
      }
      if (p.tipo == TipoPaso.situacion) {
        apoyo(p.contexto, '${u.id}.${p.id}.contexto');
      }
      if (p.tipo == TipoPaso.tabla) {
        if (p.filas.isEmpty) errores.add('${u.id}.${p.id}: tabla sin filas');
        for (final c in p.columnas) {
          apoyo(c, '${u.id}.${p.id}.columnas');
        }
        for (final fila in p.filas) {
          if (p.columnas.isNotEmpty && fila.length != p.columnas.length) {
            errores.add('${u.id}.${p.id}: fila con ${fila.length} celdas');
          }
          for (final c in fila) {
            if (c.apoyo != null) apoyo(c.apoyo, '${u.id}.${p.id}.celda');
          }
        }
      }
      for (final f in p.frases) {
        meta(f.texto, '${u.id}.${p.id}');
        apoyo(f.traduccion, '${u.id}.${p.id}.traduccion');
      }
    }
    for (final tipo in [
      TipoPaso.practicaGuiada,
      TipoPaso.situacion,
      TipoPaso.evaluacion,
    ]) {
      if (!u.pasos.any((p) => p.tipo == tipo)) {
        errores.add('${u.id}: falta ${tipo.name}');
      }
    }
    final evaluacion = u.itemsDe(TipoPaso.evaluacion).map((e) => e.$2).toList();
    if (evaluacion.length < 4 ||
        evaluacion.map((i) => i.formato).toSet().length < 2) {
      errores.add('${u.id}: evaluación con < 4 ítems o < 2 formatos');
    }
    for (final p in u.pasos) {
      for (final i in p.items) {
        final donde = '${u.id}.${p.id}.${i.id}';
        apoyo(i.consigna, '$donde.consigna');
        apoyo(i.feedback, '$donde.feedback');
        meta(i.respuesta, donde);
        meta(i.texto, donde);
        meta(i.audio, donde);
        meta(i.pregunta, donde);
        for (var k = 0; k < i.opciones.length; k++) {
          final o = i.opciones[k];
          final esRespuesta = i.indiceRespuesta != null
              ? k == i.indiceRespuesta
              : palabrasMeta(o.meta ?? '').join(' ') ==
                    palabrasMeta(i.respuesta ?? '').join(' ');
          o.meta != null
              ? meta(o.meta, donde, distractor: !esRespuesta)
              : apoyo(o.apoyo, donde);
        }
        for (final par in i.pares) {
          meta(par.$1, donde);
          apoyo(par.$2, donde);
        }
        // La clave del propio contenido debe corregirse como correcta.
        final clave = switch (i.formato) {
          FormatoItem.elegir || FormatoItem.escuchar => i.indiceRespuesta,
          FormatoItem.relacionar => true,
          _ => i.respuesta,
        };
        if (!corregir(i, clave, u.idioma)) {
          errores.add('$donde: la respuesta del contenido no se acepta');
        }
        if (i.formato == FormatoItem.ordenar &&
            !respuestaEscritaCorrecta(i, i.tokens.join(' '), u.idioma) &&
            !_mismosTokens(i)) {
          errores.add('$donde: las fichas no forman la respuesta');
        }
        if ((i.formato == FormatoItem.elegir ||
                i.formato == FormatoItem.escuchar) &&
            (i.indiceRespuesta == null ||
                i.indiceRespuesta! >= i.opciones.length)) {
          errores.add('$donde: índice de respuesta inválido');
        }
      }
    }
  }
  return errores;
}

bool _mismosTokens(Item i) {
  final a = palabrasMeta(i.tokens.join(' '))..sort();
  final b = palabrasMeta(i.respuesta ?? '')..sort();
  return a.join('|') == b.join('|');
}
