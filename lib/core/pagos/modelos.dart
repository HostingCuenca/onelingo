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

/// Una opción de duración del plan: cobro cada [meses] meses.
class DuracionPlan {
  const DuracionPlan(this.meses, this.precio);
  final int meses;
  final double precio;

  /// Precio equivalente por mes.
  double get porMes => precio / meses;
}

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
    this.usuarios = 1,
    this.listaDuraciones = const [],
    this.googleProducto,
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

  /// Personas que cubre (Familiar: 4, el titular incluido).
  final int usuarios;

  /// Duraciones del servidor (incluida la de 1 mes); vacía en servidores
  /// anteriores a las duraciones.
  final List<DuracionPlan> listaDuraciones;

  /// Producto de Google Play (`plan_p1`); null en servidores anteriores.
  final String? googleProducto;

  bool get familiar => usuarios > 1;

  /// Opciones de duración: las del servidor o, si no manda, solo el cobro
  /// del plan (1 mes, o 12 si es anual).
  List<DuracionPlan> get duraciones => listaDuraciones.isNotEmpty
      ? listaDuraciones
      : [DuracionPlan(intervalo == 'anio' ? 12 : 1, precio)];

  /// Ahorro (0–100) de [d] frente a pagar mes a mes. 0 sin precio mensual.
  int ahorro(DuracionPlan d) {
    final mensual = duraciones.where((x) => x.meses == 1).firstOrNull;
    if (mensual == null || d.meses == 1 || mensual.precio <= 0) return 0;
    return ((1 - d.precio / (mensual.precio * d.meses)) * 100).round().clamp(0, 99);
  }

  String nombreEn(String idioma) => textoEnIdioma(nombre, idioma);
  String descripcionEn(String idioma) => textoEnIdioma(descripcion, idioma);

  List<String> incluyeEn(String idioma) {
    final l = incluye[idioma];
    if (l != null && l.isNotEmpty) return l;
    return incluye['es'] ?? incluye.values.firstOrNull ?? const [];
  }

  /// `idiomas == 0`: el plan incluye todos los idiomas.
  bool get todosLosIdiomas => idiomas == 0;

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
        idiomas: (j['idiomas'] as num?)?.round().clamp(0, 10) ?? 1,
        precio: (j['precio'] as num?)?.toDouble() ?? 0,
        moneda: (j['moneda'] as String?)?.toLowerCase() ?? moneda,
        intervalo: j['intervalo'] == 'anio' ? 'anio' : 'mes',
        destacado: j['destacado'] == true,
        orden: (j['orden'] as num?)?.round() ?? 0,
        usuarios: (j['usuarios'] as num?)?.round().clamp(1, 10) ?? 1,
        listaDuraciones: [
          for (final d in (j['duraciones'] as List? ?? const []))
            if (d is Map && d['meses'] is num && d['precio'] is num)
              DuracionPlan((d['meses'] as num).round(), (d['precio'] as num).toDouble()),
        ]..sort((a, b) => a.meses.compareTo(b.meses)),
        googleProducto: j['google'] is Map && j['google']['producto'] is String
            ? j['google']['producto'] as String
            : null,
      );
}

/// Plan base de Google Play de una duración: `mes-1`, `mes-3`…
String planBaseDeMeses(int meses) => 'mes-$meses';

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
    this.demoActivo = true,
    this.googleDisponible = false,
    this.googlePaquete = 'com.torisoftt.onelingo',
  });

  final String moneda;
  final int pruebaMinutos;
  final bool pagosDisponible;

  /// `test` o `live` (null si no hay pagos).
  final String? pagosModo;
  /// Planes del servidor; null = respaldo fijo.
  final List<PlanServidor>? listaPlanes;
  final OrigenCatalogo origen;

  /// Usuarios demo (@onelingo.demo) habilitados en el servidor (Panel → Pagos).
  final bool demoActivo;

  /// El servidor verifica compras de Google Play (cobro dentro de la app Android).
  final bool googleDisponible;
  final String googlePaquete;

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
    final google = j['google'] is Map ? j['google'] as Map : const {};
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
      demoActivo: j['demoActivo'] != false,
      googleDisponible: google['disponible'] == true,
      googlePaquete: google['paquete'] is String ? google['paquete'] as String : 'com.torisoftt.onelingo',
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

/// Los 10 idiomas que se pueden pagar (anexo de idiomas por suscripción).
const idiomasDePago = ['en', 'es', 'fr', 'de', 'pt', 'it', 'zh', 'ja', 'ko', 'ru'];

/// `cambioIdiomas` de la suscripción: si el alumno puede cambiar un idioma.
class CambioIdiomas {
  const CambioIdiomas({
    this.regla = 'uno_por_periodo',
    this.permitido = false,
    this.proximoCambio,
  });

  /// libre | uno_por_periodo | solo_admin
  final String regla;
  final bool permitido;
  final DateTime? proximoCambio;

  static CambioIdiomas fromJson(Object? j) {
    if (j is! Map) return const CambioIdiomas();
    return CambioIdiomas(
      regla: j['regla'] as String? ?? 'uno_por_periodo',
      permitido: j['permitido'] == true,
      proximoCambio: j['proximoCambio'] is String
          ? DateTime.tryParse(j['proximoCambio'] as String)
          : null,
    );
  }

  /// «Próximo cambio: …» o «Pide el cambio al soporte» si no está permitido.
  String? get motivo => permitido
      ? null
      : proximoCambio != null && regla != 'solo_admin'
      ? tr('Próximo cambio: {fecha}', {'fecha': fechaCorta(proximoCambio!)})
      : tr('Pide el cambio al soporte');
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
    this.idiomas = const [],
    this.todosLosIdiomas = false,
    this.idiomasPorElegir = 0,
    this.cambioIdiomas = const CambioIdiomas(),
    this.accesoPorIdioma = const {},
    this.accesoPlan,
    this.meses,
    this.usuariosPlan,
    this.familiar = false,
    this.googleProducto,
    this.googlePlanBase,
  });

  final String planId;

  /// activa | prueba_stripe | impago | cancelada | vencida | sin_plan
  final String estado;

  /// stripe | google | cortesia | familia | null
  final String? origen;

  /// Acceso de pago en el idioma meta que el servidor tiene guardado.
  final bool acceso;
  final DateTime? periodoFin;
  final bool cancelaAlFinal;
  final String? modo;
  final bool puedeGestionar;
  final PruebaServidor prueba;

  /// Idiomas pagados (códigos) y si el plan o la cortesía son «todos».
  final List<String> idiomas;
  final bool todosLosIdiomas;

  /// Idiomas del plan aún sin elegir (p. ej. tras subir de 2 a 3).
  final int idiomasPorElegir;
  final CambioIdiomas cambioIdiomas;

  /// Acceso de pago en cada uno de los 10 idiomas.
  final Map<String, bool> accesoPorIdioma;

  /// Acceso de pago en algún idioma (null si el servidor no lo manda).
  final bool? accesoPlan;

  /// Meses del periodo que paga en Stripe (1, 3, 6, 12).
  final int? meses;

  /// Personas que cubre su plan (Familiar: 4).
  final int? usuariosPlan;

  /// Miembro de un plan familiar: lo paga otra persona.
  final bool familiar;

  /// Compra de Google Play: producto (`plan_p2`) y plan base (`mes-3`).
  final String? googleProducto;
  final String? googlePlanBase;

  /// Titular de un plan familiar con acceso: puede añadir personas.
  bool get titularFamiliar => !familiar && vigente && (usuariosPlan ?? 1) > 1;

  /// Idiomas que incluye el plan (elegidos + por elegir); 0 = todos.
  int get idiomasDelPlan =>
      todosLosIdiomas ? 0 : idiomas.length + idiomasPorElegir;

  /// La suscripción da acceso de pago en algún idioma («tiene plan»).
  bool get vigente =>
      accesoPlan ?? (acceso || accesoPorIdioma.containsValue(true));

  /// Suscripción en curso aunque aún no dé acceso (p. ej. idiomas por elegir).
  bool get enCurso =>
      vigente ||
      (estado != 'vencida' &&
          estado != 'sin_plan' &&
          (estado != 'cancelada' ||
              (periodoFin?.isAfter(DateTime.now()) ?? false)));

  /// Acceso de pago en [idioma]. Sin `accesoPorIdioma` (servidor anterior al
  /// anexo), el booleano general.
  bool accesoEn(String idioma) => accesoPorIdioma.isNotEmpty
      ? accesoPorIdioma[idioma] == true
      : acceso;

  /// Plan efectivo en [idioma]: vacío si ahí sigue la prueba gratuita.
  String planEfectivoEn(String idioma) => accesoEn(idioma) ? planId : '';

  bool get esStripe => origen == 'stripe';
  bool get esGoogle => origen == 'google';
  bool get esCortesia => origen == 'cortesia' && enCurso;

  /// Suscripción de Stripe que el alumno puede ver y gestionar (incluido un
  /// impago, para que actualice su tarjeta).
  bool get stripeVigente =>
      esStripe && enCurso;

  /// Suscripción de Google Play en curso: se gestiona y se cambia en Play.
  bool get googleVigente => esGoogle && enCurso;

  /// Suscripción que se paga sola (Stripe o Google Play) en curso.
  bool get pagoVigente => stripeVigente || googleVigente;

  String get estadoTexto => switch (estado) {
    'activa' => tr('Activa'),
    'prueba_stripe' => tr('En periodo de prueba'),
    'impago' => tr('Pago pendiente'),
    'cancelada' => tr('Cancelada'),
    'vencida' => tr('Vencida'),
    _ => esCortesia ? tr('Cortesía') : tr('Sin plan'),
  };

  /// «Cada 3 meses», «Mensual»… del periodo de Stripe (null si no se sabe).
  String? get periodoTexto => meses == null ? null : textoDuracion(meses!);

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
    idiomas: (j['idiomas'] as List? ?? const []).whereType<String>().toList(),
    todosLosIdiomas: j['todosLosIdiomas'] == true,
    idiomasPorElegir: (j['idiomasPorElegir'] as num?)?.round() ?? 0,
    cambioIdiomas: CambioIdiomas.fromJson(j['cambioIdiomas']),
    accesoPorIdioma: j['accesoPorIdioma'] is Map
        ? {
            for (final e in (j['accesoPorIdioma'] as Map).entries)
              '${e.key}': e.value == true,
          }
        : const {},
    accesoPlan: j['accesoPlan'] is bool ? j['accesoPlan'] as bool : null,
    meses: (j['meses'] as num?)?.round(),
    usuariosPlan: (j['usuariosPlan'] as num?)?.round(),
    familiar: j['familiar'] == true,
    googleProducto: j['google'] is Map ? j['google']['producto'] as String? : null,
    googlePlanBase: j['google'] is Map ? j['google']['planBase'] as String? : null,
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

/// «1 mes», «3 meses», «12 meses».
String textoDuracion(int meses) =>
    meses == 1 ? tr('1 mes') : tr('{n} meses', {'n': meses});

/// Miembro o invitación de un plan familiar (`GET /usuarios/me/familia`).
class MiembroFamilia {
  const MiembroFamilia(this.email, this.nombre, {this.activo = false});
  final String email, nombre;

  /// Ya tiene cuenta con ese correo (si no, la invitación está pendiente).
  final bool activo;
}

class Familia {
  const Familia({this.rol, this.plazas = 0, this.miembros = const [], this.titular});

  /// titular | miembro | null
  final String? rol;

  /// Personas que puede añadir el titular, además de él.
  final int plazas;
  final List<MiembroFamilia> miembros;

  /// Nombre o correo de quien paga (para un miembro).
  final String? titular;

  bool get esTitular => rol == 'titular';
  bool get esMiembro => rol == 'miembro';
  bool get completa => miembros.length >= plazas;

  static Familia fromJson(Map<String, dynamic> j) {
    final t = j['titular'];
    return Familia(
      rol: j['rol'] as String?,
      plazas: (j['plazas'] as num?)?.round() ?? 0,
      miembros: [
        for (final m in (j['miembros'] as List? ?? const []))
          if (m is Map)
            MiembroFamilia(
              '${m['email'] ?? ''}',
              '${m['nombre'] ?? ''}',
              activo: m['estado'] == 'activo',
            ),
      ],
      titular: t is Map
          ? ('${t['nombre'] ?? ''}'.trim().isNotEmpty ? '${t['nombre']}' : '${t['email'] ?? ''}')
          : null,
    );
  }
}

/// «20/11/2026» en hora local (igual en los dos idiomas de la interfaz).
String fechaCorta(DateTime fecha) {
  final d = fecha.toLocal();
  return '${d.day.toString().padLeft(2, '0')}/${d.month.toString().padLeft(2, '0')}/${d.year}';
}
