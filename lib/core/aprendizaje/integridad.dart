import 'correccion.dart';
import 'grafo.dart';
import 'modelos.dart';

final _puntuacion = RegExp(r'[.,!?¡¿;:。、！？「」…"“”()«»—–，：；]');

/// Palabras de un texto en el idioma meta (misma regla que tools/validar_ruta.py).
List<String> palabrasMeta(String texto) => texto
    .replaceAll('’', "'")
    .replaceAll('___', ' ')
    .toLowerCase()
    .replaceAll(_puntuacion, ' ')
    .split(RegExp(r'\s+'))
    // Comillas simples de cita ('once', shopkeepers') no son parte de la palabra.
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
/// `formas_pt` en tools/validar_ruta.py): cuentan las celdas de todas las
/// tablas y las formas sueltas.
Map<String, Set<String>> indiceFormasVerbales(Map<String, dynamic> verbos) {
  final res = <String, Set<String>>{};
  for (final v in verbos['verbos'] as List? ?? const []) {
    final infinitivo = (v['infinitivo'] as String).toLowerCase();
    final formas = [
      for (final t in (v['tablas'] as Map? ?? const {}).values)
        ...List<String>.from(t as List),
      ...(v['formas'] as Map? ?? const {}).values.cast<String>(),
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

/// Problemas pedagógicos y de datos de una ruta. Vacío = íntegra.
///
/// En portugués valen además las flexiones de lo enseñado
/// ([palabraConocidaPt]); [formasVerbales] (ver
/// `CargadorRuta.formasVerbales`) añade las formas irregulares de su
/// `verbos.json`. Sin él la comprobación solo es más estricta, nunca más laxa.
List<String> problemasDeContenido(
  RutaCargada ruta, {
  Map<String, Set<String>> formasVerbales = const {},
}) {
  final errores = [...validarGrafo(ruta.unidades)];
  final bool Function(String, Set<String>) conocida = ruta.curso.idioma == 'pt'
      ? (w, saber) => palabraConocidaPt(w, saber, formasVerbales)
      : palabraConocida;
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
