import 'dart:convert';

import 'package:flutter/services.dart';

import 'biblioteca_modelos.dart';
import 'biblioteca_selector.dart';
import 'modelos.dart';

enum EstadoBiblioteca { legacy, shadow, active }

enum EstadoCargaBiblioteca { disponible, ausente, invalida }

class ActivacionBiblioteca {
  const ActivacionBiblioteca({this.porUnidad = const {}});

  final Map<String, EstadoBiblioteca> porUnidad;

  EstadoBiblioteca estado(String unidad) =>
      porUnidad[unidad] ?? EstadoBiblioteca.legacy;

  factory ActivacionBiblioteca.fromJson(Map<String, dynamic> json) {
    if (json['schema'] != 'exercise-activation/1') {
      throw const FormatException('exercise activation schema');
    }
    final units = json['units'];
    if (units is! Map) throw const FormatException('activation units');
    return ActivacionBiblioteca(
      porUnidad: units.map(
        (key, value) => MapEntry(
          key.toString(),
          EstadoBiblioteca.values.byName(value.toString()),
        ),
      ),
    );
  }
}

class ResultadoCargaBiblioteca {
  const ResultadoCargaBiblioteca._(this.estado, {this.library, this.error});

  const ResultadoCargaBiblioteca.disponible(ExerciseLibrary library)
    : this._(EstadoCargaBiblioteca.disponible, library: library);

  const ResultadoCargaBiblioteca.ausente([String? error])
    : this._(EstadoCargaBiblioteca.ausente, error: error);

  const ResultadoCargaBiblioteca.invalida(String error)
    : this._(EstadoCargaBiblioteca.invalida, error: error);

  final EstadoCargaBiblioteca estado;
  final ExerciseLibrary? library;
  final String? error;
}

class DiagnosticoBiblioteca {
  const DiagnosticoBiblioteca({
    required this.activacion,
    required this.carga,
    this.errores = const [],
  });

  final EstadoBiblioteca activacion;
  final EstadoCargaBiblioteca carga;
  final List<String> errores;

  /// Solo `active` sustituye ejercicios visibles. `shadow` valida y compara.
  bool get aplicaAlAlumno =>
      activacion == EstadoBiblioteca.active &&
      carga == EstadoCargaBiblioteca.disponible &&
      errores.isEmpty;

  bool get validaEnSombra =>
      activacion == EstadoBiblioteca.shadow &&
      carga == EstadoCargaBiblioteca.disponible &&
      errores.isEmpty;
}

/// Selecciones congeladas que una unidad activa consume en el recorrido real.
/// En `legacy` y `shadow` queda vacío y la pantalla conserva sus pasos
/// embebidos. En `active` cada pool procede exclusivamente de la biblioteca.
class BibliotecaUnidadRuntime {
  const BibliotecaUnidadRuntime({
    required this.diagnostico,
    this.libraryVersion,
    this.selecciones = const {},
  });

  final DiagnosticoBiblioteca diagnostico;
  final String? libraryVersion;
  final Map<String, ExerciseSelection> selecciones;

  bool get activa => diagnostico.aplicaAlAlumno;
  ExerciseSelection? pool(String name) => selecciones[name];
}

class CargadorBiblioteca {
  CargadorBiblioteca({AssetBundle? bundle}) : _bundle = bundle ?? rootBundle;

  final AssetBundle _bundle;
  final _cache = <String, Future<ResultadoCargaBiblioteca>>{};
  final _activaciones = <String, Future<ActivacionBiblioteca>>{};

  static String asset(String idioma) =>
      'assets/contenido/$idioma/exercise-library.json';

  static String assetActivacion(String idioma) =>
      'assets/contenido/$idioma/exercise-activation.json';

  Future<ResultadoCargaBiblioteca> cargar(String idioma) =>
      _cache.putIfAbsent(idioma, () => _leer(idioma));

  Future<ActivacionBiblioteca> cargarActivacion(String idioma) =>
      _activaciones.putIfAbsent(idioma, () => _leerActivacion(idioma));

  Future<ResultadoCargaBiblioteca> _leer(String idioma) async {
    final String raw;
    try {
      raw = await _bundle.loadString(asset(idioma), cache: false);
    } catch (error) {
      return ResultadoCargaBiblioteca.ausente('$error');
    }
    try {
      final library = ExerciseLibrary.fromJson(
        jsonDecode(raw) as Map<String, dynamic>,
      );
      final errors = validateExerciseLibrary(library);
      if (errors.isNotEmpty) {
        return ResultadoCargaBiblioteca.invalida(errors.join('\n'));
      }
      return ResultadoCargaBiblioteca.disponible(library);
    } catch (error) {
      return ResultadoCargaBiblioteca.invalida('$error');
    }
  }

  Future<ActivacionBiblioteca> _leerActivacion(String idioma) async {
    try {
      final raw = await _bundle.loadString(
        assetActivacion(idioma),
        cache: false,
      );
      return ActivacionBiblioteca.fromJson(
        jsonDecode(raw) as Map<String, dynamic>,
      );
    } catch (_) {
      // Ausencia o manifiesto inválido nunca activa contenido por accidente.
      return const ActivacionBiblioteca();
    }
  }

  Future<DiagnosticoBiblioteca> diagnostico(
    String idioma,
    String unidad,
    ActivacionBiblioteca activacion,
  ) async {
    final estado = activacion.estado(unidad);
    if (estado == EstadoBiblioteca.legacy) {
      return const DiagnosticoBiblioteca(
        activacion: EstadoBiblioteca.legacy,
        carga: EstadoCargaBiblioteca.ausente,
      );
    }
    final resultado = await cargar(idioma);
    final errors = <String>[];
    final library = resultado.library;
    final unit = library?.units[unidad];
    if (resultado.error != null) errors.add(resultado.error!);
    if (library != null && unit == null) {
      errors.add('unit absent from exercise library: $unidad');
    }
    if (estado == EstadoBiblioteca.active &&
        unit != null &&
        (unit.pools['review'] ?? const <String>[]).isEmpty) {
      errors.add('active unit without editorial review pool: $unidad');
    }
    return DiagnosticoBiblioteca(
      activacion: estado,
      carga: resultado.estado,
      errores: errors,
    );
  }

  /// Resuelve de forma determinista todos los pools visibles de una unidad.
  /// La semilla es estable por intento; el `selectionId` resultante se guarda
  /// junto con cada respuesta para permitir reanudación y auditoría.
  Future<BibliotecaUnidadRuntime> resolverUnidad(
    String idioma,
    String unidad, {
    int seed = 1,
  }) async {
    final activacion = await cargarActivacion(idioma);
    final diagnosis = await diagnostico(idioma, unidad, activacion);
    if (!diagnosis.aplicaAlAlumno) {
      return BibliotecaUnidadRuntime(diagnostico: diagnosis);
    }
    final result = await cargar(idioma);
    final library = result.library!;
    final unit = library.units[unidad]!;
    final selections = <String, ExerciseSelection>{};
    for (final pool in const [
      'practiceGuided',
      'practice',
      'evaluation',
      'review',
    ]) {
      final count = unit.pools[pool]?.length ?? 0;
      selections[pool] = selectExercises(
        library,
        unitId: unidad,
        pool: pool,
        seed: seed,
        limit: count,
      );
    }
    return BibliotecaUnidadRuntime(
      diagnostico: diagnosis,
      libraryVersion: library.version,
      selecciones: selections,
    );
  }
}

Item itemDesdeVariante(ExerciseVariant variant) {
  final answer = variant.answer;
  final prompt = TextoApoyo(variant.prompt);
  final scoring = variant.origin['scoring'];
  final scoringMap = scoring is Map ? scoring : const <Object?, Object?>{};
  final parts = scoringMap['parts'] ?? scoringMap['total'];
  final minimumCorrect = scoringMap['minimumCorrect'];
  final wordRange = scoringMap['wordRange'];
  final rawParts = answer['parts'];
  return Item(
    id: variant.id,
    formato: _formato(variant.format),
    consigna: prompt,
    feedback: TextoApoyo.fromJson(variant.origin['feedback']),
    pista: variant.origin['hint'] == null
        ? null
        : TextoApoyo.fromJson(variant.origin['hint']),
    pregunta: variant.origin['question'] as String? ?? variant.prompt['meta'],
    preguntaApoyo: prompt,
    opciones: [
      for (final choice in variant.choices)
        choice['text'] is String
            ? Opcion.meta(choice['text'] as String)
            : Opcion.apoyo(TextoApoyo.fromJson(choice['text'])),
    ],
    indiceRespuesta: answer['index'] is num
        ? (answer['index'] as num).toInt()
        : null,
    respuesta: (answer['text'] ?? answer['value']) is String
        ? (answer['text'] ?? answer['value']) as String
        : null,
    aceptadas: [
      for (final value in answer['accepted'] as List? ?? const [])
        if (value is String) value,
    ],
    tokens: [
      for (final value in answer['tokens'] as List? ?? const [])
        if (value is String) value,
    ],
    texto: variant.origin['text'] as String?,
    textosPartes: [
      for (final sentence in variant.origin['sentences'] as List? ?? const [])
        if (sentence is String) sentence,
    ],
    respuestasPartes: [
      for (final part in rawParts as List? ?? const [])
        if (part is String)
          [part]
        else if (part is Map && (part['text'] is String))
          <String>{
            part['text'] as String,
            for (final accepted in part['accepted'] as List? ?? const [])
              if (accepted is String) accepted,
          }.toList(),
    ],
    audio: variant.origin['audio'] as String?,
    imagen: variant.origin['imageAsset'] as String?,
    imagenAlt: variant.origin['imageAlt'] as String?,
    partesPuntuables: parts is num ? parts.toInt() : null,
    minimoCorrectas: minimumCorrect is num ? minimumCorrect.toInt() : null,
    partesObligatorias: [
      for (final index in scoringMap['requiredParts'] as List? ?? const [])
        if (index is num) index.toInt(),
    ],
    minimoPalabras:
        wordRange is List && wordRange.length == 2 && wordRange.first is num
        ? (wordRange.first as num).toInt()
        : null,
    maximoPalabras:
        wordRange is List && wordRange.length == 2 && wordRange.last is num
        ? (wordRange.last as num).toInt()
        : null,
    evidenciasEscritura: [
      for (final grupo in scoringMap['evidenceGroups'] as List? ?? const [])
        if (grupo is List)
          [
            for (final frase in grupo)
              if (frase is String) frase,
          ],
    ],
    pares: [
      for (final pair in variant.origin['pairs'] as List? ?? const [])
        if (pair is List && pair.length == 2 && pair.first is String)
          (pair.first as String, TextoApoyo.fromJson(pair[1])),
    ],
  );
}

FormatoItem _formato(String value) => switch (value) {
  'elegir' || 'choice' || 'multipleChoice' => FormatoItem.elegir,
  'escuchar' || 'listen' => FormatoItem.escuchar,
  'ordenar' || 'order' => FormatoItem.ordenar,
  'completar' || 'fill' => FormatoItem.completar,
  'escribir' || 'write' => FormatoItem.escribir,
  'relacionar' || 'match' => FormatoItem.relacionar,
  _ => throw FormatException('unknown exercise format: $value'),
};
