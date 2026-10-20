import '../api/sync.dart';
import '../content/catalog.dart' show planes, segundosPruebaGratis;
import '../i18n/i18n.dart';

/// Planes y suscripciones (contrato de pagos, fase 1). El servidor es la
/// autoridad del plan; la app solo lo muestra. Los usuarios DEMO (correo
/// `@onelingo.demo`) y quien no tiene sesión de servidor siguen eligiendo su
/// plan en el dispositivo, como antes.

/// Usuario DEMO de la app: sus datos viven solo en el dispositivo.
bool esCorreoDemo(String email) =>
    email.trim().toLowerCase().endsWith('@onelingo.demo');

/// El plan y la prueba de este usuario los decide el servidor.
bool usaServidorPagos(String email) =>
    Sync.instancia.conectado && !esCorreoDemo(email);

/// Texto de un mapa `{es, en}` en [idioma], con el español de respaldo.
String textoEnIdioma(Map<String, String> m, String idioma) {
  final t = m[idioma];
  if (t != null && t.trim().isNotEmpty) return t;
  final es = m['es'];
  if (es != null && es.trim().isNotEmpty) return es;
  for (final v in m.values) {
    if (v.trim().isNotEmpty) return v;
  }
  return '';
}

Map<String, String> _mapaTextos(Object? j) => j is Map
    ? {
        for (final e in j.entries)
          if (e.value is String) '${e.key}': e.value as String,
      }
    : j is String
    ? {'es': j}
    : const {};

Map<String, List<String>> _mapaListas(Object? j) => j is Map
    ? {
        for (final e in j.entries)
          if (e.value is List)
            '${e.key}': (e.value as List).whereType<String>().toList(),
      }
    : j is List
    ? {'es': j.whereType<String>().toList()}
    : const {};

class PlanServidor {
  const PlanServidor({
    required this.id,
    required this.nombre,
    this.descripcion = const {},
    this.incluye = const {},
    this.idiomas = 1,
    this.precio = 0,
    this.moneda = 'usd',
    this.intervalo = 'mes',
    this.destacado = false,
    this.orden = 0,
  });

  final String id;
  final Map<String, String> nombre;
  final Map<String, String> descripcion;
  final Map<String, List<String>> incluye;
  final int idiomas;
  final double precio;
  final String moneda;

  /// `mes` o `anio`.
  final String intervalo;
  final bool destacado;
  final int orden;

  String nombreEn(String idioma) => textoEnIdioma(nombre, idioma);
  String descripcionEn(String idioma) => textoEnIdioma(descripcion, idioma);

  List<String> incluyeEn(String idioma) {
    final l = incluye[idioma];
    if (l != null && l.isNotEmpty) return l;
    return incluye['es'] ?? incluye.values.firstOrNull ?? const [];
  }

  /// «$20», «$19.99», «€15»…
  String get precioTexto => formatoPrecio(precio, moneda);

  /// «/ mes» o «/ año» en el idioma de la interfaz.
  String get intervaloTexto => intervalo == 'anio' ? tr('/ año') : tr('/ mes');

  static PlanServidor fromJson(Map<String, dynamic> j, {String moneda = 'usd'}) =>
      PlanServidor(
        id: '${j['id']}',
        nombre: _mapaTextos(j['nombre']),
        descripcion: _mapaTextos(j['descripcion']),
        incluye: _mapaListas(j['incluye']),
        idiomas: (j['idiomas'] as num?)?.round() ?? 1,
        precio: (j['precio'] as num?)?.toDouble() ?? 0,
        moneda: (j['moneda'] as String?)?.toLowerCase() ?? moneda,
        intervalo: j['intervalo'] == 'anio' ? 'anio' : 'mes',
        destacado: j['destacado'] == true,
        orden: (j['orden'] as num?)?.round() ?? 0,
      );
}

/// Símbolo y cifra sin decimales cuando el precio es entero.
String formatoPrecio(double precio, String moneda) {
  const simbolos = {'usd': r'$', 'eur': '€', 'gbp': '£'};
  final cifra = precio == precio.roundToDouble()
      ? precio.round().toString()
      : precio.toStringAsFixed(2);
  final simbolo = simbolos[moneda.toLowerCase()];
  return simbolo == null ? '${moneda.toUpperCase()} $cifra' : '$simbolo$cifra';
}

/// Planes fijos de la app: respaldo si nunca se pudo bajar `GET /planes`.
/// Se construyen al leerlos para que salgan en el idioma actual.
List<PlanServidor> planesRespaldo() => [
  for (final (i, p) in planes.indexed)
    PlanServidor(
      id: p.id,
      nombre: {'es': p.nombre},
      incluye: {'es': p.incluye},
      idiomas: p.idiomas,
      precio: p.precio.toDouble(),
      destacado: p.idiomas == 2,
      orden: i + 1,
    ),
];

enum OrigenCatalogo { servidor, cache, respaldo }

/// Respuesta de `GET /planes` (o su copia guardada, o el respaldo fijo).
class CatalogoPlanes {
  const CatalogoPlanes({
    this.moneda = 'usd',
    this.pruebaMinutos = segundosPruebaGratis ~/ 60,
    this.pagosDisponible = false,
    this.pagosModo,
    this.listaPlanes,
    this.origen = OrigenCatalogo.respaldo,
  });

  final String moneda;
  final int pruebaMinutos;
  final bool pagosDisponible;

  /// `test` o `live` (null si no hay pagos).
  final String? pagosModo;
  /// Planes del servidor; null = respaldo fijo.
  final List<PlanServidor>? listaPlanes;
  final OrigenCatalogo origen;

  List<PlanServidor> get planes => listaPlanes ?? planesRespaldo();
  int get pruebaSegundos => pruebaMinutos * 60;
  bool get modoPrueba => pagosDisponible && pagosModo == 'test';

  PlanServidor? plan(String id) =>
      id.isEmpty ? null : planes.where((p) => p.id == id).firstOrNull;

  static CatalogoPlanes fromJson(
    Map<String, dynamic> j, {
    OrigenCatalogo origen = OrigenCatalogo.servidor,
  }) {
    final moneda = (j['moneda'] as String?)?.toLowerCase() ?? 'usd';
    final pagos = j['pagos'] is Map ? j['pagos'] as Map : const {};
    final lista = [
      for (final p in (j['planes'] as List? ?? const []))
        if (p is Map) PlanServidor.fromJson(p.cast<String, dynamic>(), moneda: moneda),
    ]..sort((a, b) => a.orden.compareTo(b.orden));
    return CatalogoPlanes(
      moneda: moneda,
      pruebaMinutos:
          (j['pruebaMinutos'] as num?)?.round() ?? segundosPruebaGratis ~/ 60,
      pagosDisponible: pagos['disponible'] == true,
      pagosModo: pagos['modo'] as String?,
      listaPlanes: lista,
      origen: origen,
    );
  }
}

/// `prueba` de `GET /usuarios/me/suscripcion`.
class PruebaServidor {
  const PruebaServidor({
    this.minutos = segundosPruebaGratis ~/ 60,
    this.segundosUsados = 0,
    this.restanteSegundos = segundosPruebaGratis,
    this.agotada = false,
  });
  final int minutos;
  final int segundosUsados;
  final int restanteSegundos;
  final bool agotada;

  static PruebaServidor fromJson(Object? j) {
    if (j is! Map) return const PruebaServidor();
    final minutos = (j['minutos'] as num?)?.round() ?? segundosPruebaGratis ~/ 60;
    final usados = (j['segundosUsados'] as num?)?.round() ?? 0;
    return PruebaServidor(
      minutos: minutos,
      segundosUsados: usados,
      restanteSegundos:
          (j['restanteSegundos'] as num?)?.round() ??
          (minutos * 60 - usados).clamp(0, minutos * 60),
      agotada: j['agotada'] == true,
    );
  }
}

/// Respuesta de `GET /usuarios/me/suscripcion` y `POST /pagos/confirmar`.
class Suscripcion {
  const Suscripcion({
    this.planId = '',
    this.estado = 'sin_plan',
    this.origen,
    this.acceso = false,
    this.periodoFin,
    this.cancelaAlFinal = false,
    this.modo,
    this.puedeGestionar = false,
    this.prueba = const PruebaServidor(),
  });

  final String planId;

  /// activa | prueba_stripe | impago | cancelada | vencida | sin_plan
  final String estado;

  /// stripe | cortesia | null
  final String? origen;
  final bool acceso;
  final DateTime? periodoFin;
  final bool cancelaAlFinal;
  final String? modo;
  final bool puedeGestionar;
  final PruebaServidor prueba;

  bool get esStripe => origen == 'stripe';
  bool get esCortesia => origen == 'cortesia' && acceso;

  /// Plan efectivo: solo cuenta si da acceso.
  String get planEfectivo => acceso ? planId : '';

  /// Suscripción de Stripe que el alumno puede ver y gestionar (incluido un
  /// impago, para que actualice su tarjeta).
  bool get stripeVigente =>
      esStripe && estado != 'vencida' && (acceso || estado == 'impago');

  String get estadoTexto => switch (estado) {
    'activa' => tr('Activa'),
    'prueba_stripe' => tr('En periodo de prueba'),
    'impago' => tr('Pago pendiente'),
    'cancelada' => tr('Cancelada'),
    'vencida' => tr('Vencida'),
    _ => esCortesia ? tr('Cortesía') : tr('Sin plan'),
  };

  static Suscripcion fromJson(Map<String, dynamic> j) => Suscripcion(
    planId: j['planId'] as String? ?? '',
    estado: j['estado'] as String? ?? 'sin_plan',
    origen: j['origen'] as String?,
    acceso: j['acceso'] == true,
    periodoFin: j['periodoFin'] is String
        ? DateTime.tryParse(j['periodoFin'] as String)
        : null,
    cancelaAlFinal: j['cancelaAlFinal'] == true,
    modo: j['modo'] as String?,
    puedeGestionar: j['puedeGestionar'] == true,
    prueba: PruebaServidor.fromJson(j['prueba']),
  );
}

/// Plan y prueba que ve el alumno: del servidor cuando hay respuesta suya; si
/// no (DEMO, sin sesión o sin haberla bajado nunca), los del dispositivo.
class EstadoPlan {
  const EstadoPlan({
    required this.planId,
    required this.pruebaTotal,
    required this.trialRestante,
    required this.trialAgotado,
    this.suscripcion,
    this.servidor = false,
  });

  final String planId;

  /// Duración total de la prueba gratuita, en segundos.
  final int pruebaTotal;
  final int trialRestante;
  final bool trialAgotado;

  /// Respuesta del servidor (null si el estado es local).
  final Suscripcion? suscripcion;

  /// El usuario tiene sesión de servidor (no es DEMO): paga con Stripe.
  final bool servidor;

  bool get tienePlan => planId.isNotEmpty;
}

/// «20/11/2026» en hora local (igual en los dos idiomas de la interfaz).
String fechaCorta(DateTime fecha) {
  final d = fecha.toLocal();
  return '${d.day.toString().padLeft(2, '0')}/${d.month.toString().padLeft(2, '0')}/${d.year}';
}
