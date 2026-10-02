import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../i18n/i18n.dart';
import '../state/providers.dart';

/// Situaciones v2 (docs/claude-educacion/SITUACIONES_V2.md): las 50 de
/// `catalogo_situaciones.g.dart`, cada una con tres tramos que crecen con el
/// alumno. Contenido en `assets/contenido/<idioma>/situaciones.json`.

enum Tramo {
  basico('Básico', 'Niveles 1–3', 1),
  intermedio('Intermedio', 'Niveles 4–6', 4),
  avanzado('Avanzado', 'Niveles 7–10', 7);

  const Tramo(this.nombreEs, this.nivelesEs, this.nivelMinimo);

  /// Textos en español (dato estable; se muestran con [nombre] y [niveles]).
  final String nombreEs, nivelesEs;

  /// Nombre visible en el idioma de la interfaz.
  String get nombre => switch (this) {
    basico => tr('Básico'),
    intermedio => tr('Intermedio'),
    avanzado => tr('Avanzado'),
  };

  /// Rango de niveles visible en el idioma de la interfaz.
  String get niveles => switch (this) {
    basico => tr('Niveles {desde}–{hasta}', {'desde': 1, 'hasta': 3}),
    intermedio => tr('Niveles {desde}–{hasta}', {'desde': 4, 'hasta': 6}),
    avanzado => tr('Niveles {desde}–{hasta}', {'desde': 7, 'hasta': 10}),
  };

  /// Nivel del curso desde el que se abre.
  final int nivelMinimo;

  /// Tramo que corresponde al nivel del alumno (0–10).
  static Tramo deNivel(int nivel) => nivel >= avanzado.nivelMinimo
      ? avanzado
      : nivel >= intermedio.nivelMinimo
      ? intermedio
      : basico;

  bool abiertoPara(int nivel) =>
      this == basico || nivel >= nivelMinimo;
}

class ObjetivoSituacion {
  const ObjetivoSituacion(this.id, this.titulo, this.frase, this.traduccion);
  final String id, titulo, frase, traduccion;
}

class PalabraSituacion {
  const PalabraSituacion(this.id, this.en, this.es, this.ejemplo);
  final String id, en, es, ejemplo;
}

class FraseSituacion {
  const FraseSituacion(this.id, this.en, this.es);
  final String id, en, es;
}

class TramoSituacion {
  const TramoSituacion(this.objetivos, this.vocabulario, this.frases);
  final List<ObjetivoSituacion> objetivos;
  final List<PalabraSituacion> vocabulario;
  final List<FraseSituacion> frases;

  factory TramoSituacion.fromJson(Map<String, dynamic> j) => TramoSituacion(
    [
      for (final o in j['objetivos'] as List)
        ObjetivoSituacion(o['id'], o['titulo'], o['frase'], o['traduccion']),
    ],
    [
      // Inglés usa en/es; los idiomas nuevos, meta/traduccion (ya resuelta al
      // idioma de la interfaz por localizarApoyo).
      for (final v in j['vocabulario'] as List)
        PalabraSituacion(
          v['id'],
          v['meta'] ?? v['en'],
          v['traduccion'] ?? v['es'],
          v['ejemplo'],
        ),
    ],
    [
      for (final f in j['frases'] as List)
        FraseSituacion(f['id'], f['meta'] ?? f['en'], f['traduccion'] ?? f['es']),
    ],
  );
}

class ContenidoSituacion {
  const ContenidoSituacion(this.id, this.tramos);
  final int id;
  final Map<Tramo, TramoSituacion> tramos;

  TramoSituacion tramo(Tramo t) => tramos[t]!;

  /// Tramo al que pertenece un objetivo (null si no es de esta situación).
  Tramo? tramoDeObjetivo(String objetivoId) {
    for (final e in tramos.entries) {
      if (e.value.objetivos.any((o) => o.id == objetivoId)) return e.key;
    }
    return null;
  }

  ObjetivoSituacion? objetivo(String id) {
    for (final t in tramos.values) {
      for (final o in t.objetivos) {
        if (o.id == id) return o;
      }
    }
    return null;
  }
}

/// Contenido por id del idioma; null si el idioma aún no tiene situaciones.
Map<int, ContenidoSituacion>? situacionesDesdeJson(Map<String, dynamic> j) => {
  for (final s in j['situaciones'] as List)
    s['id'] as int: ContenidoSituacion(s['id'] as int, {
      for (final t in Tramo.values)
        t: TramoSituacion.fromJson(
          Map<String, dynamic>.from(s['tramos'][t.name] as Map),
        ),
    }),
};

final situacionesProvider =
    FutureProvider.family<Map<int, ContenidoSituacion>?, String>((
      ref,
      idioma,
    ) async {
      final String raw;
      try {
        raw = await rootBundle.loadString(
          'assets/contenido/$idioma/situaciones.json',
        );
      } catch (_) {
        return null;
      }
      // Textos de apoyo {es, en} en el idioma de la interfaz.
      final interfaz = ref.watch(progressProvider.select((s) => s.interfaz));
      return situacionesDesdeJson(
        localizarApoyo(jsonDecode(raw), interfaz) as Map<String, dynamic>,
      );
    });

// --- Progreso ---------------------------------------------------------------

/// Clave de la prueba de un tramo.
String clavePruebaSituacion(String idioma, int id, Tramo t) =>
    'situacion:$idioma:$id:${t.name}:prueba';

/// Clave de los turnos de práctica de un objetivo (la escribe el chat).
String claveObjetivoSituacion(String idioma, int id, String objetivoId) =>
    'situacion-$idioma-$id-$objetivoId';

/// Aciertos necesarios en la prueba de un tramo (80 %).
int aciertosPruebaSituacion(int total) => (total * .8).ceil();

class EstadoTramo {
  const EstadoTramo({
    required this.objetivosPracticados,
    required this.totalObjetivos,
    required this.pruebaAprobada,
    this.mejorNota,
  });
  final int objetivosPracticados, totalObjetivos;
  final bool pruebaAprobada;

  /// Mejor resultado de la prueba (aciertos, total), si se hizo.
  final (int, int)? mejorNota;

  /// Completado: prueba aprobada y al menos un objetivo practicado con IA.
  bool get completado => pruebaAprobada && objetivosPracticados > 0;

  /// Avance 0–1: cada objetivo practicado y la prueba cuentan lo mismo.
  double get progreso =>
      (objetivosPracticados + (pruebaAprobada ? 1 : 0)) / (totalObjetivos + 1);

  bool get empezado => objetivosPracticados > 0 || mejorNota != null;
}

EstadoTramo estadoTramo(
  Map<String, dynamic> practicas,
  String idioma,
  ContenidoSituacion s,
  Tramo t,
) {
  final objetivos = s.tramo(t).objetivos;
  final prueba = practicas[clavePruebaSituacion(idioma, s.id, t)] as Map?;
  return EstadoTramo(
    objetivosPracticados: objetivos
        .where(
          (o) => practicas.containsKey(
            claveObjetivoSituacion(idioma, s.id, o.id),
          ),
        )
        .length,
    totalObjetivos: objetivos.length,
    pruebaAprobada: prueba?['aprobada'] == true,
    mejorNota: prueba == null
        ? null
        : ((prueba['mejor'] as num? ?? prueba['aciertos'] as num).toInt(),
              (prueba['total'] as num).toInt()),
  );
}

/// Conversaciones recientes de una situación (la más nueva primero).
List<Map> evidenciaSituacion(
  Map<String, dynamic> practicas,
  String idioma,
  int id,
) =>
    practicas.values
        .whereType<Map>()
        .where((e) => e['situacionId'] == id && e['idioma'] == idioma)
        .toList()
      ..sort((a, b) => '${b['fecha']}'.compareTo('${a['fecha']}'));

/// Situación sugerida: la última practicada; si no hay, según los objetivos
/// personales del alumno.
int situacionSugerida(
  Map<String, dynamic> practicas,
  String idioma,
  List<String> metas,
) {
  final recientes =
      practicas.values
          .whereType<Map>()
          .where(
            (e) =>
                e['idioma'] == idioma &&
                e['situacionId'] is int &&
                e['situacionId'] >= 1 &&
                e['situacionId'] <= 50,
          )
          .toList()
        ..sort((a, b) => '${b['fecha']}'.compareTo('${a['fecha']}'));
  if (recientes.isNotEmpty) return recientes.first['situacionId'] as int;
  for (final meta in metas) {
    final id = const {
      'entrevistas': 20,
      'trabajar': 23,
      'viajar': 7,
      'estudiar': 35,
      'clientes': 25,
      'conversar': 44,
    }[meta];
    if (id != null) return id;
  }
  return 1;
}
