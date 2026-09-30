import 'grafo.dart';
import 'migracion.dart';
import 'modelos.dart';

/// Estado pedagógico de una unidad, calculado siempre desde `practicas`
/// (DEC-006). El orden importa: cada estado incluye a los anteriores.
enum EstadoUnidad {
  bloqueada,
  disponible,
  enCurso,
  practicada,
  aprobada,
  dominada;

  bool alMenos(EstadoUnidad otro) => index >= otro.index;
}

/// Claves de evidencia en `ProgressState.practicas`.
abstract final class ClaveRuta {
  static String item(String unidad, String paso, String item) =>
      'ruta:$unidad:$paso:$item';
  static String visto(String unidad) => 'ruta:$unidad:visto';
  static String evaluacion(String unidad) => 'ruta:$unidad:evaluacion';
  static String repaso(String unidad) => 'ruta:$unidad:repaso';
  static String nivelCompleto(String idioma, String nivel) =>
      'ruta:$idioma.$nivel:completa';
}

/// Evidencia de una clave, con los alias históricos de foundations-v1.
Map? evidenciaDe(Map<String, dynamic> practicas, String clave) {
  final directa = practicas[clave];
  if (directa is Map) return directa;
  for (final antigua in aliasHistoricos(clave)) {
    final e = practicas[antigua];
    if (e is Map) return e;
  }
  return null;
}

bool _resueltaGuiada(Map? e) =>
    e != null && (e['resueltaConApoyo'] == true || e['correcta'] == true);

DateTime? _fecha(Object? v) => v is String ? DateTime.tryParse(v) : null;

class InfoUnidad {
  const InfoUnidad(
    this.estado, {
    this.repasoPendiente = false,
    this.necesitaRefuerzo = false,
    this.proximoRepaso,
    this.omitible = false,
  });
  final EstadoUnidad estado;
  final bool repasoPendiente;
  final bool necesitaRefuerzo;
  final DateTime? proximoRepaso;

  /// De un nivel inferior al del diagnóstico: cuenta como prerrequisito
  /// cumplido y no se recomienda, pero se puede estudiar.
  final bool omitible;

  InfoUnidad comoOmitible() => InfoUnidad(
    estado == EstadoUnidad.bloqueada ? EstadoUnidad.disponible : estado,
    repasoPendiente: repasoPendiente,
    necesitaRefuerzo: necesitaRefuerzo,
    proximoRepaso: proximoRepaso,
    omitible: true,
  );
}

/// Nivel interno desde el que empieza la ruta de un alumno: los niveles
/// inferiores al del diagnóstico se pueden omitir (salvo quien empieza de cero).
int nivelBaseDe({required bool desdeCero, required int nivelInicial}) =>
    desdeCero ? 0 : nivelInicial;

/// Convierte la ubicación histórica (0=Fundamentos, 1–2=A1, …) a la escala
/// comercial adoptada (Nivel 1=A1 completo). Se usa solo para recomendación;
/// las claves de progreso y el diagnóstico original permanecen intactos.
int nivelClienteDesdeNivelHistorico(int nivel) {
  if (nivel <= 0) return 0;
  if (nivel <= 2) return 1;
  if (nivel <= 4) return 2;
  if (nivel <= 6) return 3;
  if (nivel <= 8) return 5;
  return 8;
}

int nivelBaseClienteDe({required bool desdeCero, required int nivelInicial}) =>
    desdeCero ? 0 : nivelClienteDesdeNivelHistorico(nivelInicial);

/// Evita una ruta sin siguiente paso cuando el diagnóstico apunta a un nivel
/// que todavía no tiene contenido editorial publicado.
int nivelBaseDisponible(RutaCargada ruta, int solicitado) {
  final publicados = ruta.unidades.map((u) => u.nivelInterno).whereType<int>();
  if (publicados.isEmpty) return 0;
  final maximo = publicados.reduce((a, b) => a > b ? a : b);
  return solicitado.clamp(0, maximo).toInt();
}

/// En escrituras no latinas, demostrar un nivel oral/global no prueba que el
/// alumno sepa leer. Estas unidades no se omiten sin evidencia específica.
bool alfabetizacionObligatoria(UnidadRuta u) =>
    const {'zh', 'ja', 'ko', 'ru'}.contains(u.idioma) &&
    u.nivelInterno == 0 &&
    u.habilidades.contains('escritura');

/// Calcula el estado de todas las unidades de una ruta.
Map<String, InfoUnidad> estadosRuta(
  RutaCargada ruta,
  Map<String, dynamic> practicas, {
  DateTime? ahora,
  int nivelBase = 0,
}) {
  final hoy = ahora ?? DateTime.now();
  final res = <String, InfoUnidad>{};
  // Las unidades vienen ordenadas y los prerrequisitos siempre son anteriores.
  for (final u in ruta.unidades) {
    final prereqOk = u.prerequisitos.every(
      (p) =>
          (res[p]?.omitible ?? false) ||
          (res[p]?.estado.alMenos(EstadoUnidad.practicada) ?? false),
    );
    final info = _estadoUnidad(u, practicas, prereqOk, hoy);
    final omitible =
        (u.nivelInterno ?? 99) < nivelBase &&
        !alfabetizacionObligatoria(u) &&
        !info.estado.alMenos(EstadoUnidad.aprobada);
    res[u.id] = omitible ? info.comoOmitible() : info;
  }
  return res;
}

InfoUnidad _estadoUnidad(
  UnidadRuta u,
  Map<String, dynamic> practicas,
  bool prereqOk,
  DateTime hoy,
) {
  final evaluacion = practicas[ClaveRuta.evaluacion(u.id)];
  final repaso = practicas[ClaveRuta.repaso(u.id)];
  final aprobada = evaluacion is Map && evaluacion['aprobada'] == true;
  if (aprobada) {
    final proximo = repaso is Map
        ? _fecha(repaso['proximo'])
        : _fecha(evaluacion['fechaAprobada'])
              ?.add(Duration(days: u.intervalosRepaso.first));
    final dominada = repaso is Map && repaso['retencion'] == true;
    final necesitaRefuerzo =
        repaso is Map && repaso['necesitaRefuerzo'] == true;
    return InfoUnidad(
      dominada ? EstadoUnidad.dominada : EstadoUnidad.aprobada,
      repasoPendiente:
          necesitaRefuerzo || (proximo != null && !proximo.isAfter(hoy)),
      necesitaRefuerzo: necesitaRefuerzo,
      proximoRepaso: proximo,
    );
  }
  final guiados = u.itemsDe(TipoPaso.practicaGuiada).toList();
  final practicada =
      guiados.isNotEmpty &&
      guiados.every(
        (pi) => _resueltaGuiada(
          evidenciaDe(practicas, ClaveRuta.item(u.id, pi.$1.id, pi.$2.id)),
        ),
      );
  // Sin prerrequisitos practicados la unidad sigue visible pero no se recomienda.
  if (!prereqOk && !practicada) return const InfoUnidad(EstadoUnidad.bloqueada);
  if (practicada) return const InfoUnidad(EstadoUnidad.practicada);
  final empezada =
      practicas.containsKey(ClaveRuta.visto(u.id)) ||
      u.pasos.any(
        (p) => p.items.any(
          (i) =>
              evidenciaDe(practicas, ClaveRuta.item(u.id, p.id, i.id)) != null,
        ),
      );
  return InfoUnidad(empezada ? EstadoUnidad.enCurso : EstadoUnidad.disponible);
}

/// Resultado de un intento de evaluación de unidad.
Map<String, dynamic> resumenEvaluacion(
  UnidadRuta u,
  int aciertos,
  int total,
  Map? anterior,
  DateTime ahora,
) {
  final aprobadaAhora = total > 0 && aciertos / total >= u.umbral;
  final yaAprobada = anterior?['aprobada'] == true;
  return {
    'idioma': u.idioma,
    'skill': 'evaluacion',
    'tipo': 'evaluacion_unidad',
    'unidad': u.id,
    'aciertos': aciertos,
    'total': total,
    'correcta': aprobadaAhora,
    // Una aprobación no se revoca por un intento posterior peor.
    'aprobada': yaAprobada || aprobadaAhora,
    'fechaAprobada': yaAprobada
        ? anterior!['fechaAprobada']
        : aprobadaAhora
        ? ahora.toIso8601String()
        : null,
  };
}

/// Nuevo registro de repaso espaciado (cajas tipo Leitner).
Map<String, dynamic> siguienteRepaso(
  UnidadRuta u,
  Map? evaluacion,
  Map? anterior,
  int aciertos,
  int total,
  DateTime ahora,
) {
  final acierto = total > 0 && aciertos / total >= u.umbral;
  final cajaPrevia = anterior?['caja'] as int? ?? 0;
  final caja = acierto ? cajaPrevia + 1 : (cajaPrevia - 2).clamp(0, 99);
  final intervalos = u.intervalosRepaso;
  final dias = acierto
      ? intervalos[(caja - 1).clamp(0, intervalos.length - 1)]
      : 1;
  final aprobadaEn = _fecha(evaluacion?['fechaAprobada']);
  // Retención: acierto en un repaso hecho al menos un día después de aprobar.
  final retencion =
      anterior?['retencion'] == true ||
      (acierto &&
          aprobadaEn != null &&
          ahora.difference(aprobadaEn) >= const Duration(days: 1));
  return {
    'idioma': u.idioma,
    'skill': 'repaso',
    'tipo': 'repaso_unidad',
    'unidad': u.id,
    'aciertos': aciertos,
    'total': total,
    'correcta': acierto,
    'caja': caja,
    'retencion': retencion,
    'necesitaRefuerzo': !acierto,
    'ultimo': ahora.toIso8601String(),
    'proximo': ahora.add(Duration(days: dias)).toIso8601String(),
  };
}

/// Unidad recomendada: primero retención/refuerzo vencido; después contenido
/// nuevo no aprobado. Así el repaso espaciado no queda enterrado por la ruta.
UnidadRuta? unidadRecomendada(RutaCargada ruta, Map<String, InfoUnidad> e) {
  for (final u in ruta.unidades) {
    final info = e[u.id]!;
    if (info.necesitaRefuerzo || info.repasoPendiente) return u;
  }
  for (final u in ruta.unidades) {
    final info = e[u.id]!;
    if (!info.omitible &&
        !info.estado.alMenos(EstadoUnidad.aprobada) &&
        info.estado != EstadoUnidad.bloqueada) {
      return u;
    }
  }
  return null;
}

/// Nivel completo: todas sus unidades al menos aprobadas.
bool nivelAprobado(RutaCargada ruta, Map<String, InfoUnidad> e, String nivel) {
  final unidades = ruta.delNivel(nivel);
  return unidades.isNotEmpty &&
      unidades.every((u) => e[u.id]!.estado.alMenos(EstadoUnidad.aprobada));
}

/// Palabras del idioma meta enseñadas hasta una unidad (incluida).
Set<String> vocabularioConocido(RutaCargada ruta, String unidadId) => {
  for (final id in {unidadId, ...prerequisitosTransitivos(ruta, unidadId)})
    for (final v in ruta.unidad(id)?.vocabulario ?? const <Vocablo>[]) v.texto,
};
