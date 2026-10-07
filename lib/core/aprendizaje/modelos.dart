/// Modelos de las rutas de aprendizaje (esquema 2).
///
/// Contrato completo en docs/claude-educacion/ESQUEMA_CONTENIDO.md. Solo usa
/// tipos puros de Dart para funcionar igual en web y móvil.
library;

/// Texto dirigido al alumno en uno o varios idiomas de apoyo (DEC-004).
class TextoApoyo {
  const TextoApoyo(this.porIdioma);
  final Map<String, String> porIdioma;

  static const vacio = TextoApoyo({});

  factory TextoApoyo.fromJson(Object? j) {
    if (j == null) return vacio;
    if (j is String) return TextoApoyo({'es': j});
    return TextoApoyo({
      for (final e in (j as Map).entries) e.key as String: '${e.value}',
    });
  }

  bool get isEmpty => porIdioma.values.every((t) => t.trim().isEmpty);

  /// Primer texto disponible según la cadena de idiomas de apoyo.
  String en(List<String> cadena) {
    for (final l in cadena) {
      final t = porIdioma[l];
      if (t != null && t.trim().isNotEmpty) return t;
    }
    for (final t in porIdioma.values) {
      if (t.trim().isNotEmpty) return t;
    }
    return '';
  }
}

/// Romanización opcional (docs/claude-educacion/ROMANIZACION.md): null si
/// falta o va vacía.
String? romDe(Object? v) =>
    v is String && v.trim().isNotEmpty ? v.trim() : null;

/// Lista paralela de romanizaciones (`opcionesRom`, `tokensRom`, `paresRom`…).
/// Cada posición vacía o ausente es null.
List<String?> romsDe(Object? v) => [
  for (final r in v is List ? v : const []) romDe(r),
];

/// Posición [i] de una lista paralela de romanizaciones (null si no hay).
String? romEn(List<String?> roms, int i) =>
    i >= 0 && i < roms.length ? roms[i] : null;

/// Cadena de resolución: nativo → predeterminado del curso → español.
List<String> cadenaApoyo(String nativo, String predeterminado) => [
  nativo,
  predeterminado,
  'es',
];

enum EstadoNivel { publicado, planificado }

class NivelCurso {
  const NivelCurso({
    required this.id,
    required this.cefr,
    required this.nivelInterno,
    required this.estado,
    required this.titulo,
  });
  final String id, cefr;
  final int? nivelInterno;
  final EstadoNivel estado;
  final TextoApoyo titulo;

  factory NivelCurso.fromJson(Map<String, dynamic> j) => NivelCurso(
    id: j['id'] as String,
    cefr: j['cefr'] as String,
    nivelInterno: j['nivelInterno'] as int?,
    estado: j['estado'] == 'planificado'
        ? EstadoNivel.planificado
        : EstadoNivel.publicado,
    titulo: TextoApoyo.fromJson(j['titulo']),
  );
}

class ModuloIndice {
  const ModuloIndice({
    required this.id,
    required this.nivel,
    required this.archivo,
    required this.titulo,
  });
  final String id, nivel, archivo;
  final TextoApoyo titulo;

  factory ModuloIndice.fromJson(Map<String, dynamic> j) => ModuloIndice(
    id: j['id'] as String,
    nivel: j['nivel'] as String,
    archivo: j['archivo'] as String,
    titulo: TextoApoyo.fromJson(j['titulo']),
  );
}

class Curso {
  const Curso({
    required this.idioma,
    required this.version,
    required this.curriculumScale,
    required this.revisionInicial,
    required this.idiomasApoyo,
    required this.apoyoPredeterminado,
    required this.palabrasLibres,
    required this.niveles,
    required this.modulos,
  });
  final String idioma, version, curriculumScale, apoyoPredeterminado;

  bool get usaEscalaCliente => curriculumScale == 'client-10-levels-v1';

  /// Contenido sin revisión nativa: se muestra la etiqueta «Versión inicial».
  final bool revisionInicial;
  final List<String> idiomasApoyo, palabrasLibres;
  final List<NivelCurso> niveles;
  final List<ModuloIndice> modulos;

  factory Curso.fromJson(Map<String, dynamic> j) => Curso(
    idioma: j['idioma'] as String,
    version: j['version'] as String? ?? '',
    curriculumScale: j['curriculumScale'] as String? ?? 'internal-0-10-v1',
    revisionInicial: j['revision'] != 'revisada',
    idiomasApoyo: List<String>.from(j['idiomasApoyo'] as List? ?? const ['es']),
    apoyoPredeterminado: j['apoyoPredeterminado'] as String? ?? 'es',
    palabrasLibres: List<String>.from(j['palabrasLibres'] as List? ?? const []),
    niveles: [
      for (final n in j['niveles'] as List? ?? const [])
        NivelCurso.fromJson(n as Map<String, dynamic>),
    ],
    modulos: [
      for (final m in j['modulos'] as List? ?? const [])
        ModuloIndice.fromJson(m as Map<String, dynamic>),
    ],
  );
}

class Vocablo {
  const Vocablo({
    required this.id,
    required this.texto,
    this.rom,
    required this.traduccion,
    this.nota,
  });
  final String id, texto;
  final String? rom;
  final TextoApoyo traduccion;
  final TextoApoyo? nota;

  factory Vocablo.fromJson(Map<String, dynamic> j) => Vocablo(
    id: j['id'] as String,
    texto: j['texto'] as String,
    rom: romDe(j['rom']),
    traduccion: TextoApoyo.fromJson(j['traduccion']),
    nota: j['nota'] == null ? null : TextoApoyo.fromJson(j['nota']),
  );
}

/// Frase en el idioma meta con su traducción (ejemplos y diálogos).
class Frase {
  const Frase({
    required this.texto,
    this.rom,
    required this.traduccion,
    this.nota,
    this.hablante,
    this.hablanteRom,
  });
  final String texto;
  final String? rom, hablante, hablanteRom;
  final TextoApoyo traduccion;
  final TextoApoyo? nota;

  factory Frase.fromJson(Map<String, dynamic> j) => Frase(
    texto: j['texto'] as String,
    rom: romDe(j['rom']),
    traduccion: TextoApoyo.fromJson(j['traduccion']),
    nota: j['nota'] == null ? null : TextoApoyo.fromJson(j['nota']),
    hablante: j['hablante'] as String?,
    hablanteRom: romDe(j['hablanteRom']),
  );
}

class ErrorFrecuente {
  const ErrorFrecuente(this.incorrecto, this.correcto, this.explicacion);
  final String incorrecto, correcto;
  final TextoApoyo explicacion;

  factory ErrorFrecuente.fromJson(Map<String, dynamic> j) => ErrorFrecuente(
    j['incorrecto'] as String,
    j['correcto'] as String,
    TextoApoyo.fromJson(j['explicacion']),
  );
}

enum FormatoItem { elegir, escuchar, ordenar, completar, escribir, relacionar }

/// Opción de respuesta: texto en el idioma meta o texto de apoyo.
class Opcion {
  const Opcion.meta(String this.meta) : apoyo = null;
  const Opcion.apoyo(TextoApoyo this.apoyo) : meta = null;
  final String? meta;
  final TextoApoyo? apoyo;

  factory Opcion.fromJson(Object j) =>
      j is String ? Opcion.meta(j) : Opcion.apoyo(TextoApoyo.fromJson(j));
}

class Item {
  const Item({
    required this.id,
    required this.formato,
    required this.consigna,
    required this.feedback,
    this.pista,
    this.pregunta,
    this.preguntaApoyo,
    this.opciones = const [],
    this.indiceRespuesta,
    this.respuesta,
    this.aceptadas = const [],
    this.tokens = const [],
    this.texto,
    this.audio,
    this.imagen,
    this.imagenAlt,
    this.pares = const [],
    this.textosPartes = const [],
    this.respuestasPartes = const [],
    this.partesPuntuables,
    this.minimoCorrectas,
    this.partesObligatorias = const [],
    this.minimoPalabras,
    this.maximoPalabras,
    this.evidenciasEscritura = const [],
    this.abierta = false,
    this.textoRom,
    this.preguntaRom,
    this.opcionesRom = const [],
    this.tokensRom = const [],
    this.paresRom = const [],
  });
  final String id;
  final FormatoItem formato;

  /// Romanización (ru, ko, ja, zh): `textoRom`/`preguntaRom` bajo el texto y
  /// listas paralelas a [opciones], [tokens] y a la izquierda de [pares].
  /// `audio` y `respuesta` nunca llevan (docs/claude-educacion/ROMANIZACION.md).
  final String? textoRom, preguntaRom;
  final List<String?> opcionesRom, tokensRom, paresRom;

  String? romOpcion(int i) => romEn(opcionesRom, i);
  String? romToken(int i) => romEn(tokensRom, i);
  String? romPar(int i) => romEn(paresRom, i);

  bool get tieneRom =>
      textoRom != null ||
      preguntaRom != null ||
      [...opcionesRom, ...tokensRom, ...paresRom].any((r) => r != null);

  /// Producción abierta (escritura larga sin rúbrica): el alumno escribe
  /// dentro del rango de palabras y compara su texto con el modelo. No puntúa.
  final bool abierta;
  final TextoApoyo consigna, feedback;
  final TextoApoyo? pista, preguntaApoyo;
  final String? pregunta, respuesta, texto, audio, imagen, imagenAlt;
  final List<Opcion> opciones;
  final int? indiceRespuesta;
  final int? partesPuntuables, minimoCorrectas;
  final int? minimoPalabras, maximoPalabras;
  final List<int> partesObligatorias;
  final List<List<String>> evidenciasEscritura;
  final List<String> aceptadas, tokens;
  final List<(String, TextoApoyo)> pares;

  /// Estímulos y respuestas válidas de una actividad de completar multiparte.
  /// Cada posición de [respuestasPartes] corresponde a [textosPartes].
  final List<String> textosPartes;
  final List<List<String>> respuestasPartes;

  factory Item.fromJson(Map<String, dynamic> j) {
    final formato = FormatoItem.values.byName(j['formato'] as String);
    final r = j['respuesta'];
    return Item(
      id: j['id'] as String,
      formato: formato,
      consigna: TextoApoyo.fromJson(j['consigna']),
      feedback: TextoApoyo.fromJson(j['feedback']),
      pista: j['pista'] == null ? null : TextoApoyo.fromJson(j['pista']),
      pregunta: j['pregunta'] as String?,
      preguntaApoyo: j['preguntaApoyo'] == null
          ? null
          : TextoApoyo.fromJson(j['preguntaApoyo']),
      opciones: [
        for (final o in j['opciones'] as List? ?? const []) Opcion.fromJson(o),
      ],
      indiceRespuesta: r is int ? r : null,
      respuesta: r is String ? r : null,
      aceptadas: List<String>.from(j['aceptadas'] as List? ?? const []),
      tokens: List<String>.from(j['tokens'] as List? ?? const []),
      texto: j['texto'] as String?,
      audio: j['audio'] as String?,
      imagen: j['imagen'] as String?,
      imagenAlt: j['imagenAlt'] as String?,
      partesPuntuables: j['partesPuntuables'] as int?,
      minimoCorrectas: j['minimoCorrectas'] as int?,
      partesObligatorias: List<int>.from(
        j['partesObligatorias'] as List? ?? const [],
      ),
      abierta: j['abierta'] == true,
      minimoPalabras: j['minimoPalabras'] as int?,
      maximoPalabras: j['maximoPalabras'] as int?,
      evidenciasEscritura: [
        for (final grupo in j['evidenciasEscritura'] as List? ?? const [])
          List<String>.from(grupo as List),
      ],
      textosPartes: List<String>.from(j['textosPartes'] as List? ?? const []),
      respuestasPartes: [
        for (final respuestas in j['respuestasPartes'] as List? ?? const [])
          List<String>.from(respuestas as List),
      ],
      pares: [
        for (final p in j['pares'] as List? ?? const [])
          ((p as List)[0] as String, TextoApoyo.fromJson(p[1])),
      ],
      textoRom: romDe(j['textoRom']),
      preguntaRom: romDe(j['preguntaRom']),
      opcionesRom: romsDe(j['opcionesRom']),
      tokensRom: romsDe(j['tokensRom']),
      paresRom: romsDe(j['paresRom']),
    );
  }

  /// Formas escritas válidas (respuesta + aceptadas), para comparar normalizadas.
  List<String> get respuestasValidas => [?respuesta, ...aceptadas];
}

enum TipoPaso {
  explicacion,
  ejemplos,
  vocabulario,
  patron,
  tabla,
  practicaGuiada,
  practicaIndependiente,
  situacion,
  evaluacion;

  static TipoPaso desdeJson(String s) => switch (s) {
    'practica_guiada' => practicaGuiada,
    'practica_independiente' => practicaIndependiente,
    _ => TipoPaso.values.byName(s),
  };

  /// Pasos que enseñan (sin ítems que puntúen).
  bool get ensena => index <= tabla.index;
}

/// Celda de una tabla: texto en el idioma meta (con romanización opcional)
/// o texto de apoyo (encabezados de fila, traducciones).
class Celda {
  const Celda({this.texto, this.rom, this.apoyo});
  final String? texto, rom;
  final TextoApoyo? apoyo;

  factory Celda.fromJson(Map<String, dynamic> j) => Celda(
    texto: j['texto'] as String?,
    rom: romDe(j['rom']),
    apoyo: j['apoyo'] == null ? null : TextoApoyo.fromJson(j['apoyo']),
  );
}

class Paso {
  const Paso({
    required this.id,
    required this.tipo,
    this.titulo,
    this.texto,
    this.icono,
    this.frases = const [],
    this.refs = const [],
    this.formula = const [],
    this.contexto,
    this.items = const [],
    this.columnas = const [],
    this.filas = const [],
  });
  final String id;
  final TipoPaso tipo;
  final TextoApoyo? titulo, texto, contexto;
  final String? icono;

  /// Ejemplos, ejemplos de un patrón o líneas de diálogo.
  final List<Frase> frases;
  final List<String> refs;
  final List<({String texto, TextoApoyo? nota})> formula;
  final List<Item> items;

  /// Tabla (escrituras, conjugaciones): encabezados y filas de celdas.
  final List<TextoApoyo> columnas;
  final List<List<Celda>> filas;

  factory Paso.fromJson(Map<String, dynamic> j) {
    final tipo = TipoPaso.desdeJson(j['tipo'] as String);
    final frases = switch (tipo) {
      TipoPaso.ejemplos => j['items'],
      TipoPaso.patron => j['ejemplos'],
      TipoPaso.situacion => j['dialogo'],
      _ => null,
    };
    return Paso(
      id: j['id'] as String,
      tipo: tipo,
      titulo: j['titulo'] == null ? null : TextoApoyo.fromJson(j['titulo']),
      texto: j['texto'] == null ? null : TextoApoyo.fromJson(j['texto']),
      icono: j['icono'] as String?,
      contexto: j['contexto'] == null
          ? null
          : TextoApoyo.fromJson(j['contexto']),
      frases: [
        for (final f in frases as List? ?? const [])
          Frase.fromJson(f as Map<String, dynamic>),
      ],
      refs: List<String>.from(j['refs'] as List? ?? const []),
      formula: [
        for (final f in j['formula'] as List? ?? const [])
          (
            texto: (f as Map)['texto'] as String,
            nota: f['nota'] == null ? null : TextoApoyo.fromJson(f['nota']),
          ),
      ],
      columnas: [
        for (final c in j['columnas'] as List? ?? const [])
          TextoApoyo.fromJson(c),
      ],
      filas: [
        for (final f in j['filas'] as List? ?? const [])
          [
            for (final c in f as List)
              Celda.fromJson(c as Map<String, dynamic>),
          ],
      ],
      items: tipo == TipoPaso.ejemplos
          ? const []
          : [
              for (final i in j['items'] as List? ?? const [])
                Item.fromJson(i as Map<String, dynamic>),
            ],
    );
  }
}

class UnidadRuta {
  const UnidadRuta({
    required this.id,
    required this.idioma,
    required this.nivel,
    this.modulo = '',
    required this.orden,
    required this.titulo,
    required this.objetivo,
    required this.cefr,
    required this.nivelInterno,
    required this.concepto,
    required this.prerequisitos,
    required this.habilidades,
    required this.gramatica,
    required this.vocabulario,
    required this.erroresFrecuentes,
    required this.pasos,
    required this.umbral,
    required this.intervalosRepaso,
    required this.tutor,
    this.guias = const [],
  });
  final String id, idioma, nivel, cefr, concepto;

  /// Módulo al que pertenece (sección dentro del nivel).
  final String modulo;
  final int orden;
  final int? nivelInterno;
  final TextoApoyo titulo, objetivo;
  final List<String> prerequisitos, habilidades, gramatica;
  final List<Vocablo> vocabulario;
  final List<ErrorFrecuente> erroresFrecuentes;
  final List<Paso> pasos;
  final double umbral;
  final List<int> intervalosRepaso;

  /// Metadatos para el tutor IA (integración futura, sin interfaz).
  final Map<String, dynamic> tutor;

  /// Guías de gramática existentes relacionadas (ids de grammar_guides.dart).
  final List<String> guias;

  static const intervalosPorDefecto = [1, 3, 7, 16, 35, 90];

  factory UnidadRuta.fromJson(
    Map<String, dynamic> j, {
    required String idioma,
    required String nivel,
    String modulo = '',
  }) => UnidadRuta(
    id: j['id'] as String,
    idioma: idioma,
    nivel: nivel,
    modulo: modulo,
    orden: j['orden'] as int,
    titulo: TextoApoyo.fromJson(j['titulo']),
    objetivo: TextoApoyo.fromJson(j['objetivo']),
    cefr: j['cefr'] as String,
    nivelInterno: j['nivelInterno'] as int?,
    concepto: j['concepto'] as String,
    prerequisitos: List<String>.from(j['prerequisitos'] as List),
    habilidades: List<String>.from(j['habilidades'] as List),
    gramatica: List<String>.from(j['gramatica'] as List? ?? const []),
    vocabulario: [
      for (final v in j['vocabulario'] as List)
        Vocablo.fromJson(v as Map<String, dynamic>),
    ],
    erroresFrecuentes: [
      for (final e in j['erroresFrecuentes'] as List)
        ErrorFrecuente.fromJson(e as Map<String, dynamic>),
    ],
    pasos: [
      for (final p in j['pasos'] as List)
        Paso.fromJson(p as Map<String, dynamic>),
    ],
    umbral: ((j['criterioDominio'] as Map)['umbral'] as num).toDouble(),
    intervalosRepaso: List<int>.from(
      (j['repaso'] as Map?)?['intervalosDias'] as List? ?? intervalosPorDefecto,
    ),
    tutor: Map<String, dynamic>.from(j['tutor'] as Map? ?? const {}),
    guias: List<String>.from(j['guias'] as List? ?? const []),
  );

  Vocablo? vocablo(String id) {
    for (final v in vocabulario) {
      if (v.id == id) return v;
    }
    return null;
  }

  Iterable<(Paso, Item)> itemsDe(TipoPaso tipo) sync* {
    for (final p in pasos) {
      if (p.tipo != tipo) continue;
      for (final i in p.items) {
        yield (p, i);
      }
    }
  }
}

/// Curso con sus unidades cargadas (orden de presentación).
class RutaCargada {
  const RutaCargada(this.curso, this.unidades);
  final Curso curso;
  final List<UnidadRuta> unidades;

  UnidadRuta? unidad(String id) {
    for (final u in unidades) {
      if (u.id == id) return u;
    }
    return null;
  }

  List<UnidadRuta> delNivel(String nivel) => [
    for (final u in unidades)
      if (u.nivel == nivel) u,
  ];
}
