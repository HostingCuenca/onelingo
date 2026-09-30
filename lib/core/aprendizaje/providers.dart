import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../state/providers.dart';
import 'biblioteca_adaptador.dart';
import 'cargador.dart';
import 'dominio.dart';
import 'modelos.dart';

final cargadorRutaProvider = Provider<CargadorRuta>((_) => CargadorRuta());
final cargadorBibliotecaProvider = Provider<CargadorBiblioteca>(
  (_) => CargadorBiblioteca(),
);

final activacionBibliotecaProvider =
    FutureProvider.family<ActivacionBiblioteca, String>(
      (ref, idioma) =>
          ref.watch(cargadorBibliotecaProvider).cargarActivacion(idioma),
    );

final diagnosticoBibliotecaProvider =
    FutureProvider.family<
      DiagnosticoBiblioteca,
      ({String idioma, String unidad})
    >((ref, key) async {
      final activacion = await ref.watch(
        activacionBibliotecaProvider(key.idioma).future,
      );
      return ref
          .watch(cargadorBibliotecaProvider)
          .diagnostico(key.idioma, key.unidad, activacion);
    });

final bibliotecaUnidadRuntimeProvider =
    FutureProvider.family<
      BibliotecaUnidadRuntime,
      ({String idioma, String unidad})
    >((ref, key) {
      return ref
          .watch(cargadorBibliotecaProvider)
          .resolverUnidad(key.idioma, key.unidad);
    });

/// Ruta de un idioma (null si aún no tiene).
final rutaProvider = FutureProvider.family<RutaCargada?, String>(
  (ref, idioma) => ref.watch(cargadorRutaProvider).cargar(idioma),
);

/// Nivel desde el que empieza la ruta del alumno (omite lo ya superado).
int nivelBaseAlumno(ProgressState s) =>
    nivelBaseDe(desdeCero: s.fundamentos, nivelInicial: s.nivelInicial);

/// Base de la ruta 10 × 100. La ruta legacy conserva `nivelBaseAlumno` hasta
/// que cada unidad pase por `shadow` y se active explícitamente.
int nivelBaseAlumnoCliente(ProgressState s) =>
    nivelBaseDe(desdeCero: s.fundamentos, nivelInicial: s.nivelCliente);

/// Estados de la ruta de un alumno.
Map<String, InfoUnidad> estadosAlumno(RutaCargada ruta, ProgressState s) =>
    estadosRuta(
      ruta,
      s.practicas,
      nivelBase: nivelBaseDisponible(
        ruta,
        ruta.curso.usaEscalaCliente
            ? nivelBaseAlumnoCliente(s)
            : nivelBaseAlumno(s),
      ),
    );

/// Cadena de idiomas de apoyo para mostrar textos al alumno (DEC-004).
List<String> cadenaDelAlumno(ProgressState s, Curso curso) =>
    cadenaApoyo(s.idiomaNativo, curso.apoyoPredeterminado);

/// Registro de evidencia de la ruta sobre `registrarPractica`, que conserva
/// primera respuesta, intentos y fechas, y concede XP una sola vez por clave.
class RegistroRuta {
  RegistroRuta(this._ref);
  final Ref _ref;

  ProgressNotifier get _notifier => _ref.read(progressProvider.notifier);
  Map<String, dynamic> get _practicas => _ref.read(progressProvider).practicas;

  void visto(UnidadRuta u) {
    final clave = ClaveRuta.visto(u.id);
    if (_practicas.containsKey(clave)) return;
    _notifier.registrarPractica(clave, {
      'idioma': u.idioma,
      'skill': 'exposicion',
      'tipo': 'exposicion',
      'unidad': u.id,
      'correcta': true,
    });
  }

  void item(
    UnidadRuta u,
    Paso p,
    Item i, {
    required bool correcta,
    required String respuesta,
    String? variantId,
    String? libraryVersion,
    String? selectionId,
  }) {
    final clave = ClaveRuta.item(u.id, p.id, i.id);
    final anterior = _practicas[clave];
    final guiada = p.tipo == TipoPaso.practicaGuiada;
    _notifier.registrarPractica(clave, {
      'idioma': u.idioma,
      'skill': u.habilidades.first,
      'nivel': u.nivelInterno,
      'ruta': 'ruta-v2',
      'unidad': u.id,
      'tipo': switch (p.tipo) {
        TipoPaso.practicaGuiada => 'practica_guiada',
        TipoPaso.practicaIndependiente => 'practica_independiente',
        TipoPaso.situacion => 'situacion',
        _ => 'evaluacion',
      },
      'formato': i.formato.name,
      'conApoyo': guiada,
      'correcta': correcta,
      if (guiada)
        'resueltaConApoyo':
            correcta ||
            (anterior is Map && anterior['resueltaConApoyo'] == true),
      'respuesta': respuesta,
      'variantId': ?variantId,
      'libraryVersion': ?libraryVersion,
      'selectionId': ?selectionId,
    });
  }

  /// Guarda el intento de evaluación; devuelve si la unidad quedó aprobada.
  bool evaluacion(UnidadRuta u, int aciertos, int total) {
    final clave = ClaveRuta.evaluacion(u.id);
    final anterior = _practicas[clave];
    final resumen = resumenEvaluacion(
      u,
      aciertos,
      total,
      anterior is Map ? anterior : null,
      DateTime.now(),
    );
    _notifier.registrarPractica(clave, resumen);
    return resumen['aprobada'] == true;
  }

  void repaso(UnidadRuta u, int aciertos, int total) {
    final evaluacion = _practicas[ClaveRuta.evaluacion(u.id)];
    final anterior = _practicas[ClaveRuta.repaso(u.id)];
    _notifier.registrarPractica(
      ClaveRuta.repaso(u.id),
      siguienteRepaso(
        u,
        evaluacion is Map ? evaluacion : null,
        anterior is Map ? anterior : null,
        aciertos,
        total,
        DateTime.now(),
      ),
    );
  }

  /// Marca el nivel como completo (una vez) si todas sus unidades están
  /// aprobadas. Devuelve true si se acaba de completar.
  bool comprobarNivel(RutaCargada ruta, String nivel) {
    final clave = ClaveRuta.nivelCompleto(ruta.curso.idioma, nivel);
    if (_practicas.containsKey(clave)) return false;
    if (!nivelAprobado(ruta, estadosRuta(ruta, _practicas), nivel)) {
      return false;
    }
    _notifier.registrarPractica(clave, {
      'idioma': ruta.curso.idioma,
      'skill': 'evaluacion',
      'tipo': 'nivel_completo',
      'nivel': nivel,
      'correcta': true,
    });
    return true;
  }
}

final registroRutaProvider = Provider<RegistroRuta>(RegistroRuta.new);
