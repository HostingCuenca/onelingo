import 'dart:math';

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

  /// Prueba para saltar un nivel (aprobada → el nivel cuenta como superado).
  static String pruebaNivel(String idioma, String nivel) =>
      'ruta:$idioma.$nivel:prueba';
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

/// Niveles N1–N10 (nivel interno) que ya tienen unidades publicadas.
Set<int> nivelesPublicados(RutaCargada ruta) => {
  for (final nv in ruta.curso.niveles)
    if ((nv.nivelInterno ?? 0) >= 1 && ruta.delNivel(nv.id).isNotEmpty)
      nv.nivelInterno!,
};

/// Nivel más alto con unidades publicadas (0 si solo hay Fundamentos).
int nivelPublicadoMaximo(RutaCargada ruta) =>
    nivelesPublicados(ruta).fold(0, max);

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
      // Tras un repaso fallido el siguiente vence al día siguiente: repetirlo
      // en el acto solo produce un bucle con las mismas preguntas.
      repasoPendiente: proximo != null && !proximo.isAfter(hoy),
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
  final aprobadaAhora = superaUmbral(aciertos, total, u.umbral);
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

/// Aciertos mínimos para superar [umbral] en una prueba de [total] ítems.
/// Se redondea hacia abajo para que las pruebas cortas no exijan el 100 %:
/// con 0,8, 3 de 4 y 2 de 3 aprueban; con 1 o 2 ítems se piden todos.
int aciertosNecesarios(int total, double umbral) =>
    total <= 2 ? total : (total * umbral + 1e-9).floor().clamp(1, total);

bool superaUmbral(int aciertos, int total, double umbral) =>
    total > 0 && aciertos >= aciertosNecesarios(total, umbral);

/// Nuevo registro de repaso espaciado (cajas tipo Leitner).
Map<String, dynamic> siguienteRepaso(
  UnidadRuta u,
  Map? evaluacion,
  Map? anterior,
  int aciertos,
  int total,
  DateTime ahora,
) {
  final acierto = superaUmbral(aciertos, total, u.umbral);
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
    if (info.repasoPendiente) return u;
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

/// Preguntas de la prueba de un nivel y aciertos para aprobarla.
const preguntasPruebaNivel = 20;
const aciertosPruebaNivel = 16;

/// Formatos que se corrigen solos (la producción libre queda fuera).
const _formatosPrueba = {
  FormatoItem.elegir,
  FormatoItem.escuchar,
  FormatoItem.completar,
  FormatoItem.ordenar,
  FormatoItem.relacionar,
};

/// Prueba de un nivel: una pregunta de evaluación de cada tramo del nivel
/// (20 tramos de clases seguidas), al azar en cada intento, para que cubra
/// todo el nivel y no se pueda memorizar.
List<Item> itemsPruebaNivel(RutaCargada ruta, String nivel, Random rnd) {
  final unidades = ruta.delNivel(nivel);
  if (unidades.isEmpty) return const [];
  final tramos = min(preguntasPruebaNivel, unidades.length);
  final res = <Item>[];
  for (var t = 0; t < tramos; t++) {
    final desde = t * unidades.length ~/ tramos;
    final hasta = (t + 1) * unidades.length ~/ tramos;
    final candidatos = [
      for (final u in unidades.sublist(desde, hasta))
        for (final (_, i) in u.itemsDe(TipoPaso.evaluacion))
          if (_formatosPrueba.contains(i.formato)) i,
    ];
    if (candidatos.isNotEmpty) {
      res.add(candidatos[rnd.nextInt(candidatos.length)]);
    }
  }
  return res;
}

bool pruebaNivelAprobada(
  Map<String, dynamic> practicas,
  String idioma,
  String nivel,
) =>
    (practicas[ClaveRuta.pruebaNivel(idioma, nivel)] as Map?)?['aprobada'] ==
    true;

/// Nivel completo por cualquiera de los dos caminos: todas sus unidades
/// aprobadas o su prueba aprobada.
bool nivelSuperado(
  RutaCargada ruta,
  Map<String, InfoUnidad> e,
  Map<String, dynamic> practicas,
  String nivel,
) =>
    pruebaNivelAprobada(practicas, ruta.curso.idioma, nivel) ||
    nivelAprobado(ruta, e, nivel);

/// Nivel interno más alto superado con su prueba (0 si ninguno).
int nivelPorPruebas(RutaCargada ruta, Map<String, dynamic> practicas) {
  var m = 0;
  for (final n in ruta.curso.niveles) {
    final interno = n.nivelInterno;
    if (interno != null &&
        interno > m &&
        pruebaNivelAprobada(practicas, ruta.curso.idioma, n.id)) {
      m = interno;
    }
  }
  return m;
}
