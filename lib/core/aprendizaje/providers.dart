import 'dart:convert';
import 'dart:math';

import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../diagnostico.dart' show escalaDiagnosticoCliente;
import '../state/providers.dart';
import 'biblioteca_adaptador.dart';
import 'cargador.dart';
import 'dominio.dart';
import 'modelos.dart';
import 'ubicacion.dart';

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

/// Idiomas cuya pantalla Aprender usa los niveles de la ruta (esquema 2,
/// con estado y prueba de cada nivel). El resto sigue con las lecciones
/// antiguas hasta tener su N1 (PLAN_PRODUCCION.md, FR-5b).
const idiomasConRuta = {'en', 'fr'};

/// Ruta de un idioma (null si aún no tiene).
final rutaProvider = FutureProvider.family<RutaCargada?, String>(
  (ref, idioma) => ref.watch(cargadorRutaProvider).cargar(idioma),
);

/// Banco de la prueba de ubicación v2 de un idioma con ruta, ya limitado a
/// lo publicado (FR-6). Null si el idioma no tiene ruta, banco o niveles
/// publicados: entonces sigue con el diagnóstico anterior.
class BancoUbicacion {
  const BancoUbicacion(this.json, this.nivelMaximo);

  /// `assets/contenido/<idioma>/diagnostico-v2.json` tal cual (textos de
  /// apoyo sin resolver: se resuelven con el idioma de la interfaz).
  final Map<String, dynamic> json;

  /// Nivel más alto con preguntas en el banco y clases publicadas.
  final int nivelMaximo;

  List<ItemUbicacion> banco(String interfaz) =>
      ItemUbicacion.bancoLocalizado(json, interfaz);
}

String rutaBancoUbicacion(String idioma) =>
    'assets/contenido/$idioma/diagnostico-v2.json';

final bancoUbicacionProvider = FutureProvider.family<BancoUbicacion?, String>((
  ref,
  idioma,
) async {
  if (!idiomasConRuta.contains(idioma)) return null;
  final Map<String, dynamic> json;
  try {
    json =
        jsonDecode(await rootBundle.loadString(rutaBancoUbicacion(idioma)))
            as Map<String, dynamic>;
  } catch (_) {
    return null;
  }
  final ruta = await ref.watch(rutaProvider(idioma).future);
  if (ruta == null) return null;
  final tope = nivelMaximoUbicacion(
    ItemUbicacion.banco(json),
    publicados: nivelesPublicados(ruta),
  );
  return tope < 1 ? null : BancoUbicacion(json, tope);
});

/// La ubicación guardada está en la escala del curso (N1 = A1 completo):
/// la del curso si la declara o la de una prueba de nivel v2.
bool ubicacionEnEscalaCliente(RutaCargada ruta, ProgressState s) =>
    ruta.curso.usaEscalaCliente || s.nivelEscala == escalaDiagnosticoCliente;

/// Nivel de ubicación efectivo en la ruta: el de la prueba de nivel, pero
/// nunca por encima del nivel publicado más alto (un francés ubicado en N4
/// por el diagnóstico anterior empieza en N1 mientras solo haya N1). El
/// diagnóstico guardado no se toca: al publicarse más niveles, se aplica.
int nivelUbicacionRuta(RutaCargada ruta, ProgressState s) =>
    nivelBaseDisponible(
      ruta,
      ubicacionEnEscalaCliente(ruta, s)
          ? nivelBaseAlumnoCliente(s)
          : nivelBaseAlumno(s),
    );

/// Nivel desde el que empieza la ruta del alumno (omite lo ya superado).
int nivelBaseAlumno(ProgressState s) =>
    nivelBaseDe(desdeCero: s.fundamentos, nivelInicial: s.nivelInicial);

/// Base de la ruta 10 × 100. La ruta legacy conserva `nivelBaseAlumno` hasta
/// que cada unidad pase por `shadow` y se active explícitamente.
int nivelBaseAlumnoCliente(ProgressState s) =>
    nivelBaseDe(desdeCero: s.fundamentos, nivelInicial: s.nivelCliente);

/// Estados de la ruta de un alumno.
/// Los niveles superados con su prueba se omiten como los que la prueba de
/// ubicación deja por debajo.
Map<String, InfoUnidad> estadosAlumno(RutaCargada ruta, ProgressState s) {
  final ubicacion = nivelUbicacionRuta(ruta, s);
  final porPruebas = nivelPorPruebas(ruta, s.practicas);
  return estadosRuta(
    ruta,
    s.practicas,
    nivelBase: nivelBaseDisponible(
      ruta,
      porPruebas > 0 ? max(ubicacion, porPruebas + 1) : ubicacion,
    ),
  );
}

/// Cadena de idiomas de apoyo para mostrar textos al alumno (DEC-004).
List<String> cadenaDelAlumno(ProgressState s, Curso curso) =>
    cadenaApoyo(s.interfaz, curso.apoyoPredeterminado);

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

/// Nivel del curso en que está el alumno (1–10): el de su ubicación o el
/// siguiente al último nivel superado (clases o prueba), lo que sea mayor.
/// Es el que usan situaciones y biblioteca; nunca lo elige el alumno.
/// Con la ruta cargada, nunca supera el nivel publicado más alto.
final nivelAlumnoProvider = Provider<int>((ref) {
  final s = ref.watch(progressProvider);
  final ruta = ref.watch(rutaProvider(s.idiomaMeta)).valueOrNull;
  if (ruta == null) return s.nivelActual.clamp(1, 10);
  return nivelAlumnoEnRuta(ruta, s);
});

/// [nivelAlumnoProvider] con la ruta ya cargada.
int nivelAlumnoEnRuta(RutaCargada ruta, ProgressState s) {
  // Los idiomas que aún estudian con las lecciones antiguas no se limitan
  // por su ruta piloto.
  final tope = idiomasConRuta.contains(ruta.curso.idioma)
      ? max(1, nivelPublicadoMaximo(ruta))
      : 10;
  var n = min(
    ubicacionEnEscalaCliente(ruta, s) ? s.nivelCliente : s.nivelActual,
    tope,
  );
  final e = estadosAlumno(ruta, s);
  for (final nv in ruta.curso.niveles) {
    final interno = nv.nivelInterno;
    if (interno != null &&
        interno >= 1 &&
        interno + 1 > n &&
        ruta.delNivel(nv.id).isNotEmpty &&
        nivelSuperado(ruta, e, s.practicas, nv.id)) {
      n = interno + 1;
    }
  }
  return n.clamp(1, tope);
}
