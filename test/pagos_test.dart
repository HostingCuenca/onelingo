import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/api/pagos_api.dart';
import 'package:onelingo/core/api/sync.dart';
import 'package:onelingo/core/diagnostico.dart' show escalaDiagnosticoCliente;
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/i18n/i18n.dart';
import 'package:onelingo/core/pagos/google_play.dart';
import 'package:onelingo/core/pagos/providers.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/plans/idiomas_plan.dart';
import 'package:onelingo/features/plans/pago_screen.dart';
import 'package:onelingo/features/plans/plans_screen.dart';

/// Planes y pagos en la app (contrato de pagos, fase 1), con HTTP simulado.

Map<String, dynamic> _planesJson({bool disponible = true, String modo = 'test'}) => {
  'moneda': 'usd',
  'pruebaMinutos': 30,
  'pagos': {'disponible': disponible, 'modo': modo},
  'planes': [
    {
      'id': 'p2',
      'nombre': {'es': 'Dos idiomas', 'en': 'Two languages'},
      'descripcion': {'es': 'El favorito', 'en': ''},
      'incluye': {
        'es': ['2 idiomas a elegir'],
        'en': ['Choose 2 languages'],
      },
      'idiomas': 2,
      'precio': 30.0,
      'moneda': 'usd',
      'intervalo': 'mes',
      'destacado': true,
      'orden': 2,
    },
    {
      'id': 'p1',
      'nombre': {'es': 'Un idioma', 'en': 'One language'},
      'descripcion': {'es': '', 'en': ''},
      'incluye': {'es': ['1 idioma a elegir'], 'en': []},
      'idiomas': 1,
      'precio': 199.5,
      'moneda': 'usd',
      'intervalo': 'anio',
      'destacado': false,
      'orden': 1,
    },
  ],
};

Map<String, dynamic> _suscripcionJson({
  String planId = '',
  String estado = 'sin_plan',
  String? origen,
  bool acceso = false,
  String? periodoFin,
  bool cancelaAlFinal = false,
  bool puedeGestionar = false,
  int usados = 0,
  bool agotada = false,
  List<String>? idiomas,
  bool todos = false,
  int porElegir = 0,
  Map<String, Object?>? cambio,
  Map<String, bool>? accesoPorIdioma,
}) => {
  'planId': planId,
  'estado': estado,
  'origen': origen,
  'acceso': acceso,
  'periodoFin': periodoFin,
  'cancelaAlFinal': cancelaAlFinal,
  'modo': origen == 'stripe' ? 'test' : null,
  'puedeGestionar': puedeGestionar,
  'prueba': {
    'minutos': 60,
    'segundosUsados': usados,
    'restanteSegundos': (3600 - usados).clamp(0, 3600),
    'agotada': agotada,
  },
  'idiomas': ?idiomas,
  'todosLosIdiomas': todos,
  'idiomasPorElegir': porElegir,
  'cambioIdiomas': ?cambio,
  'accesoPorIdioma': ?accesoPorIdioma,
};

/// Simula el backend: rutas → (código, cuerpo). Guarda las peticiones.
class _Servidor {
  _Servidor(this.rutas);
  final Map<String, (int, Object)> rutas;
  final peticiones = <http.Request>[];

  MockClient get cliente => MockClient((req) async {
    peticiones.add(req);
    final r = rutas['${req.method} ${req.url.path}'];
    if (r == null) return http.Response('{"error":"no existe"}', 404);
    return http.Response(jsonEncode(r.$2), r.$1, headers: {'content-type': 'application/json; charset=utf-8'});
  });

  Iterable<String> get rutasPedidas => peticiones.map((r) => '${r.method} ${r.url.path}');
}

Future<SharedPreferences> _prefs({
  String email = 'alumna@correo.com',
  bool sesion = true,
  String planId = '',
  int trialSegundos = 0,
  String interfaz = 'es',
  Map<String, Object> extra = const {},
}) async {
  SharedPreferences.setMockInitialValues({
    if (sesion) 'onelingo.api.token': 'tok',
    if (sesion) 'onelingo.api.usuarioId': 'u1',
    'onelingo.progress.v1': jsonEncode({
      'onboardingDone': true,
      'nombre': 'Alumna',
      'email': email,
      'idiomaInterfaz': interfaz,
      'trialInicio': DateTime.now().toIso8601String(),
      'trialSegundos': trialSegundos,
      'planId': planId,
    }),
    ...extra,
  });
  final prefs = await SharedPreferences.getInstance();
  Sync.instancia.inicializar(prefs);
  return prefs;
}

/// Google Play simulado: registra las compras abiertas y completadas; las
/// compras llegan con [entregar], como las manda el plugin.
class _TiendaFalsa implements TiendaPlay {
  _TiendaFalsa({this.preciosFalsos = const {}, this.pendientes = const []});
  final Map<String, PrecioPlay> preciosFalsos;
  final List<CompraPlay> pendientes;
  final _flujo = StreamController<List<CompraPlay>>.broadcast();
  final abiertas = <String>[];
  final completadas = <String>[];
  String? anterior;

  void entregar(CompraPlay c) => _flujo.add([c]);

  @override
  Stream<List<CompraPlay>> get compras => _flujo.stream;
  @override
  Future<bool> disponible() async => true;
  @override
  Future<Map<String, PrecioPlay>> precios(Set<String> productos) async => preciosFalsos;
  @override
  Future<bool> comprar({required String producto, required String planBase, required String cuenta, String? productoAnterior}) async {
    abiertas.add('$producto|$planBase|$cuenta');
    anterior = productoAnterior;
    return true;
  }

  @override
  Future<List<CompraPlay>> sinCompletar() async => pendientes;
  @override
  Future<void> completar(CompraPlay c) async => completadas.add(c.token);
}

/// [enApp]: Android con Google Play (por defecto, la web con Stripe).
ProviderContainer _contenedor(
  SharedPreferences prefs,
  _Servidor servidor, {
  List<String>? abiertas,
  bool enApp = false,
  TiendaPlay? tienda,
}) {
  final c = ProviderContainer(
    overrides: [
      prefsProvider.overrideWithValue(prefs),
      pagosApiProvider.overrideWithValue(PagosApi(cliente: servidor.cliente)),
      abrirUrlProvider.overrideWithValue((url) async {
        abiertas?.add(url);
        return true;
      }),
      pagoEnAppProvider.overrideWithValue(enApp),
      tiendaPlayProvider.overrideWithValue(tienda ?? _TiendaFalsa()),
    ],
  );
  addTearDown(c.dispose);
  return c;
}

Future<void> _pantallaPlanes(WidgetTester tester, ProviderContainer c) async {
  tester.view.physicalSize = const Size(430, 2600);
  tester.view.devicePixelRatio = 1;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
  await tester.pumpWidget(
    UncontrolledProviderScope(
      container: c,
      child: MaterialApp(theme: buildTheme(), home: const PlansScreen()),
    ),
  );
  await tester.pumpAndSettle();
}

/// Abre el detalle de un plan desde la lista.
Future<void> _abrirPlan(WidgetTester tester, String id) async {
  await tester.tap(find.byKey(ValueKey('plan-$id')));
  await tester.pumpAndSettle();
}

/// Vuelve del detalle a la lista.
Future<void> _volver(WidgetTester tester) async {
  await tester.pageBack();
  await tester.pumpAndSettle();
}

/// La subida del progreso deja un temporizador (Sync): se cancela al terminar.
Future<void> _fin() => Sync.instancia.cerrarSesion();

ElevatedButton _boton(WidgetTester tester, String texto) => tester.widget<ElevatedButton>(
  find.ancestor(of: find.text(texto), matching: find.byType(ElevatedButton)).first,
);

void main() {
  setUp(() {
    Efectos.animaciones.value = false;
    Efectos.sonido = false;
    I18n.idioma.value = 'es';
  });
  tearDown(() async {
    I18n.idioma.value = 'es';
    await Sync.instancia.cerrarSesion();
  });

  group('catálogo de planes', () {
    test('baja GET /planes, lo ordena y lo guarda', () async {
      final prefs = await _prefs();
      final servidor = _Servidor({'GET /planes': (200, _planesJson())});
      final c = _contenedor(prefs, servidor);
      expect(c.read(catalogoPlanesProvider).origen, OrigenCatalogo.respaldo);
      await c.read(catalogoPlanesProvider.notifier).refrescar();
      final cat = c.read(catalogoPlanesProvider);
      expect(cat.origen, OrigenCatalogo.servidor);
      expect(cat.planes.map((p) => p.id), ['p1', 'p2']);
      expect(cat.pruebaMinutos, 30);
      expect(cat.pruebaSegundos, 1800);
      expect(cat.modoPrueba, isTrue);
      expect(cat.plan('p1')!.precioTexto, r'$199.50');
      expect(cat.plan('p2')!.precioTexto, r'$30');
      expect(prefs.getString(CatalogoPlanesNotifier.clave), isNotNull);
      expect(servidor.peticiones.single.headers['authorization'], isNull);
    });

    test('sin red usa la copia guardada', () async {
      final prefs = await _prefs(extra: {CatalogoPlanesNotifier.clave: jsonEncode(_planesJson(disponible: false))});
      final servidor = _Servidor({});
      final c = _contenedor(prefs, servidor);
      await c.read(catalogoPlanesProvider.notifier).refrescar();
      final cat = c.read(catalogoPlanesProvider);
      expect(cat.origen, OrigenCatalogo.cache);
      expect(cat.planes.map((p) => p.id), ['p1', 'p2']);
      expect(cat.pagosDisponible, isFalse);
    });

    test('si nunca bajó nada, los planes fijos y 60 min de prueba', () async {
      final prefs = await _prefs();
      final c = _contenedor(prefs, _Servidor({'GET /planes': (500, {'error': 'x'})}));
      await c.read(catalogoPlanesProvider.notifier).refrescar();
      final cat = c.read(catalogoPlanesProvider);
      expect(cat.origen, OrigenCatalogo.respaldo);
      expect(cat.planes.map((p) => p.id), ['p1', 'p2', 'p3']);
      expect(cat.planes.map((p) => p.precio), [20, 30, 40]);
      expect(cat.pruebaSegundos, 3600);
      expect(cat.pagosDisponible, isFalse);
    });

    test('nombre, descripción y ventajas en el idioma, con español de respaldo', () {
      final cat = CatalogoPlanes.fromJson(_planesJson());
      final p1 = cat.plan('p1')!, p2 = cat.plan('p2')!;
      expect(p2.nombreEn('en'), 'Two languages');
      expect(p2.nombreEn('es'), 'Dos idiomas');
      expect(p2.nombreEn('fr'), 'Dos idiomas');
      expect(p2.descripcionEn('en'), 'El favorito');
      expect(p2.incluyeEn('en'), ['Choose 2 languages']);
      expect(p1.incluyeEn('en'), ['1 idioma a elegir']);
      expect(p1.intervaloTexto, '/ año');
      I18n.usar('en', {'/ año': '/ year', '/ mes': '/ month'});
      I18n.idioma.value = 'en';
      expect(p1.intervaloTexto, '/ year');
      expect(p2.intervaloTexto, '/ month');
    });
  });

  group('suscripción del servidor', () {
    test('la prueba agotada la decide el servidor', () async {
      final prefs = await _prefs(trialSegundos: 0);
      final servidor = _Servidor({
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson(usados: 3600, agotada: true)),
      });
      final c = _contenedor(prefs, servidor);
      expect(c.read(estadoPlanProvider).trialAgotado, isFalse);
      await c.read(suscripcionProvider.notifier).refrescar();
      final ep = c.read(estadoPlanProvider);
      expect(ep.servidor, isTrue);
      expect(ep.trialAgotado, isTrue);
      expect(ep.trialRestante, 0);
      expect(servidor.peticiones.single.headers['authorization'], 'Bearer tok');
      // Se guarda para verla sin red.
      expect(prefs.getString('onelingo.suscripcion.u1'), isNotNull);
    });

    test('el plan visible sale del servidor y pasa al progreso local', () async {
      final prefs = await _prefs(planId: 'p1');
      final c = _contenedor(prefs, _Servidor({
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson(planId: 'p3', estado: 'activa', origen: 'stripe', acceso: true)),
      }));
      await c.read(suscripcionProvider.notifier).refrescar();
      expect(c.read(estadoPlanProvider).planId, 'p3');
      expect(c.read(progressProvider).planId, 'p3');
      // Con servidor, el alumno ya no se asigna planes a sí mismo.
      expect(c.read(progressProvider.notifier).elegirPlan('p1'), isFalse);
      expect(c.read(progressProvider).planId, 'p3');
    });

    test('sin acceso, el plan local se borra y la prueba sigue contando', () async {
      final prefs = await _prefs(planId: 'p2', trialSegundos: 600);
      final c = _contenedor(prefs, _Servidor({
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson(planId: 'p2', estado: 'vencida', origen: 'stripe', usados: 300)),
      }));
      await c.read(suscripcionProvider.notifier).refrescar();
      final ep = c.read(estadoPlanProvider);
      expect(ep.planId, '');
      expect(c.read(progressProvider).planId, '');
      // Manda el mayor entre el servidor y el latido local.
      expect(ep.trialRestante, 3000);
    });

    test('planId vacío = prueba gratuita aunque el servidor diga acceso', () async {
      final prefs = await _prefs(trialSegundos: 1200);
      final c = _contenedor(prefs, _Servidor({
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson(acceso: true, usados: 600)),
      }));
      await c.read(suscripcionProvider.notifier).refrescar();
      final ep = c.read(estadoPlanProvider);
      expect(ep.tienePlan, isFalse);
      expect(ep.trialRestante, 2400);
      expect(ep.trialAgotado, isFalse);
    });

    test('POST /pagos/portal envía {} como JSON (Fastify rechaza JSON vacío)', () async {
      final prefs = await _prefs();
      final servidor = _Servidor({'POST /pagos/portal': (200, {'url': 'https://billing.stripe.com/x'})});
      final r = await PagosApi(cliente: servidor.cliente).portal();
      expect(r.url, 'https://billing.stripe.com/x');
      final req = servidor.peticiones.single;
      expect(req.body, '{}');
      expect(req.headers['content-type'], startsWith('application/json'));
      expect(prefs, isNotNull);
    });

    test('DEMO: sin cambios, plan en local aunque haya sesión', () async {
      final prefs = await _prefs(email: 'diego@onelingo.demo', trialSegundos: 3600);
      final servidor = _Servidor({});
      final c = _contenedor(prefs, servidor);
      await c.read(suscripcionProvider.notifier).refrescar();
      expect(servidor.peticiones, isEmpty);
      var ep = c.read(estadoPlanProvider);
      expect(ep.servidor, isFalse);
      expect(ep.trialAgotado, isTrue);
      expect(c.read(progressProvider.notifier).elegirPlan('p2'), isTrue);
      ep = c.read(estadoPlanProvider);
      expect(ep.planId, 'p2');
      expect(ep.trialAgotado, isFalse);
    });

    test('sin sesión de servidor: comportamiento local', () async {
      final prefs = await _prefs(sesion: false);
      final c = _contenedor(prefs, _Servidor({}));
      expect(c.read(estadoPlanProvider).servidor, isFalse);
      expect(c.read(progressProvider.notifier).elegirPlan('p1'), isTrue);
      expect(c.read(estadoPlanProvider).planId, 'p1');
    });
  });

  group('pantalla de planes', () {
    testWidgets('planes del servidor en inglés, aviso de modo test y Suscribirme abre Checkout', (tester) async {
      final en = jsonDecode(File('assets/i18n/en.json').readAsStringSync()) as Map<String, dynamic>;
      I18n.usar('en', en.cast<String, String>());
      I18n.idioma.value = 'en';
      final prefs = await _prefs(interfaz: 'en');
      final abiertas = <String>[];
      final servidor = _Servidor({
        'GET /planes': (200, _planesJson()),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson()),
        'POST /pagos/checkout': (200, {'url': 'https://checkout.stripe.com/c/pay/cs_test_1'}),
      });
      final c = _contenedor(prefs, servidor, abiertas: abiertas);
      await _pantallaPlanes(tester, c);
      expect(find.text('Two languages'), findsOneWidget);
      expect(find.text('One language'), findsOneWidget);
      expect(find.text('2 languages'), findsOneWidget);
      expect(find.text('/ year'), findsOneWidget);
      expect(find.text('Test mode: use card 4242 4242 4242 4242'), findsOneWidget);
      expect(find.text('Business'), findsOneWidget);
      // Detalle: lo que incluye y el botón para seguir.
      await _abrirPlan(tester, 'p2');
      expect(find.text('Choose 2 languages'), findsOneWidget);
      await tester.tap(find.byKey(const ValueKey('suscribirme')));
      await tester.pumpAndSettle();
      // Plan de 2 idiomas: selector con el idioma meta (inglés) ya marcado.
      expect(find.text("Choose your plan's 2 languages"), findsOneWidget);
      await tester.tap(find.byKey(const ValueKey('idioma-plan-fr')));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Continue').last);
      await tester.pumpAndSettle();
      final checkout = servidor.peticiones.last;
      expect('${checkout.method} ${checkout.url.path}', 'POST /pagos/checkout');
      expect(jsonDecode(checkout.body), {'planId': 'p2', 'idiomas': ['en', 'fr']});
      expect(checkout.headers['authorization'], 'Bearer tok');
      expect(abiertas, ['https://checkout.stripe.com/c/pay/cs_test_1']);
      await _fin();
    });

    testWidgets('sin pagos: botón deshabilitado «Pagos próximamente» y sin aviso de test', (tester) async {
      final prefs = await _prefs();
      final c = _contenedor(prefs, _Servidor({
        'GET /planes': (200, _planesJson(disponible: false)),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson()),
      }));
      await _pantallaPlanes(tester, c);
      expect(find.textContaining('4242'), findsNothing);
      await _abrirPlan(tester, 'p2');
      expect(_boton(tester, 'Pagos próximamente').onPressed, isNull);
      expect(find.byKey(const ValueKey('suscribirme')), findsNothing);
      await _fin();
    });

    testWidgets('modo real: sin aviso de tarjeta de prueba', (tester) async {
      final prefs = await _prefs();
      final c = _contenedor(prefs, _Servidor({
        'GET /planes': (200, _planesJson(modo: 'live')),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson()),
      }));
      await _pantallaPlanes(tester, c);
      expect(find.textContaining('4242'), findsNothing);
      await _abrirPlan(tester, 'p1');
      expect(find.byKey(const ValueKey('suscribirme')), findsOneWidget);
      await _fin();
    });

    testWidgets('suscripción activa de Stripe: plan, estado, fecha y «Gestionar»', (tester) async {
      final prefs = await _prefs();
      final abiertas = <String>[];
      final servidor = _Servidor({
        'GET /planes': (200, _planesJson()),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson(
          planId: 'p2', estado: 'activa', origen: 'stripe', acceso: true,
          periodoFin: '2026-11-20T12:00:00Z', cancelaAlFinal: true, puedeGestionar: true,
        )),
        'POST /pagos/portal': (200, {'url': 'https://billing.stripe.com/p/session/test_1'}),
      });
      final c = _contenedor(prefs, servidor, abiertas: abiertas);
      await _pantallaPlanes(tester, c);
      expect(find.text('Tu suscripción'), findsOneWidget);
      expect(find.text('Activa'), findsOneWidget);
      expect(find.text('Se cancela el 20/11/2026'), findsOneWidget);
      expect(find.text('TU PLAN'), findsOneWidget);
      // Con suscripción activa no hay banner de prueba.
      expect(find.text('Prueba gratuita en curso'), findsNothing);
      await _abrirPlan(tester, 'p2');
      expect(find.text('PLAN ACTUAL'), findsOneWidget);
      await _volver(tester);
      await _abrirPlan(tester, 'p1');
      expect(find.text('Cambiar de plan'), findsOneWidget);
      await _volver(tester);
      await tester.tap(find.text('Gestionar suscripción'));
      await tester.pumpAndSettle();
      expect(servidor.rutasPedidas.last, 'POST /pagos/portal');
      expect(abiertas, ['https://billing.stripe.com/p/session/test_1']);
      await _fin();
    });

    testWidgets('cortesía: «Acceso otorgado por el administrador» hasta la fecha', (tester) async {
      final prefs = await _prefs();
      final c = _contenedor(prefs, _Servidor({
        'GET /planes': (200, _planesJson()),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson(
          planId: 'p1', estado: 'activa', origen: 'cortesia', acceso: true, periodoFin: '2026-12-31T12:00:00Z',
        )),
      }));
      await _pantallaPlanes(tester, c);
      expect(find.text('Acceso otorgado por el administrador hasta el 31/12/2026'), findsOneWidget);
      expect(find.text('Gestionar suscripción'), findsNothing);
      await _abrirPlan(tester, 'p1');
      expect(find.text('PLAN ACTUAL'), findsOneWidget);
      await _fin();
    });

    testWidgets('checkout con 409: avisa que use «Gestionar suscripción»', (tester) async {
      final prefs = await _prefs();
      final abiertas = <String>[];
      final c = _contenedor(prefs, _Servidor({
        'GET /planes': (200, _planesJson()),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson()),
        'POST /pagos/checkout': (409, {'error': 'ya suscrito'}),
      }), abiertas: abiertas);
      await _pantallaPlanes(tester, c);
      await _abrirPlan(tester, 'p1');
      await tester.tap(find.byKey(const ValueKey('suscribirme')));
      await tester.pumpAndSettle();
      // Plan de 1 idioma: el idioma meta ya basta.
      expect(find.text('Elige el idioma de tu plan'), findsOneWidget);
      await tester.tap(find.text('Continuar').last);
      await tester.pumpAndSettle();
      expect(abiertas, isEmpty);
      expect(find.textContaining('Ya tienes una suscripción activa'), findsOneWidget);
      await _fin();
    });

    testWidgets('DEMO: elige el plan en el dispositivo, sin pagar', (tester) async {
      final prefs = await _prefs(email: 'ana@onelingo.demo');
      final servidor = _Servidor({'GET /planes': (200, _planesJson())});
      final c = _contenedor(prefs, servidor);
      await _pantallaPlanes(tester, c);
      expect(find.textContaining('4242'), findsNothing);
      await _abrirPlan(tester, 'p2');
      expect(find.byKey(const ValueKey('suscribirme')), findsNothing);
      await tester.tap(find.text('ELEGIR DOS IDIOMAS'));
      await tester.pumpAndSettle();
      expect(c.read(progressProvider).planId, 'p2');
      expect(servidor.rutasPedidas, isNot(contains('POST /pagos/checkout')));
      expect(find.text('PLAN ACTUAL'), findsOneWidget);
      await _fin();
    });
  });

  group('idiomas por suscripción', () {
    Map<String, dynamic> conIdiomas({
      List<String> idiomas = const ['en', 'fr'],
      Map<String, Object?> cambio = const {'regla': 'uno_por_periodo', 'permitido': true, 'proximoCambio': null},
      int porElegir = 0,
      String origen = 'stripe',
    }) => _suscripcionJson(
      planId: 'p2', estado: 'activa', origen: origen, acceso: true, puedeGestionar: origen == 'stripe',
      periodoFin: '2026-11-20T12:00:00Z', idiomas: idiomas, porElegir: porElegir, cambio: cambio,
      accesoPorIdioma: {for (final c in idiomasDePago) c: idiomas.contains(c)},
    )..['accesoPlan'] = idiomas.isNotEmpty;

    testWidgets('selector: idioma meta marcado, exige exactamente N y bloquea el resto', (tester) async {
      final prefs = await _prefs();
      final servidor = _Servidor({
        'GET /planes': (200, _planesJson()),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson()),
        'POST /pagos/checkout': (200, {'url': 'https://checkout.stripe.com/x'}),
      });
      final c = _contenedor(prefs, servidor, abiertas: []);
      await _pantallaPlanes(tester, c);
      await _abrirPlan(tester, 'p2');
      await tester.tap(find.byKey(const ValueKey('suscribirme')));
      await tester.pumpAndSettle();
      expect(find.text('Elige los 2 idiomas de tu plan'), findsOneWidget);
      expect(find.text('1 de 2 elegidos'), findsOneWidget);
      CheckboxListTile casilla(String c) => tester.widget(find.byKey(ValueKey('idioma-plan-$c')));
      expect(casilla('en').value, isTrue);
      ElevatedButton continuar() => tester.widget<ElevatedButton>(
        find.ancestor(of: find.text('Continuar').last, matching: find.byType(ElevatedButton)).first,
      );
      expect(continuar().onPressed, isNull);
      await tester.tap(find.byKey(const ValueKey('idioma-plan-de')));
      await tester.pumpAndSettle();
      expect(find.text('2 de 2 elegidos'), findsOneWidget);
      // Completo: los demás no se pueden marcar; desmarcar sí.
      expect(casilla('fr').onChanged, isNull);
      expect(casilla('en').onChanged, isNotNull);
      await tester.tap(find.text('Continuar').last);
      await tester.pumpAndSettle();
      expect(jsonDecode(servidor.peticiones.last.body), {'planId': 'p2', 'idiomas': ['en', 'de']});
      await _fin();
    });

    testWidgets('plan «todos»: sin selector, checkout con idiomas vacíos', (tester) async {
      final planes = _planesJson();
      (planes['planes'] as List).add({
        'id': 'p9', 'nombre': {'es': 'Ilimitado', 'en': 'Unlimited'}, 'incluye': {'es': [], 'en': []},
        'idiomas': 0, 'precio': 60, 'moneda': 'usd', 'intervalo': 'mes', 'destacado': false, 'orden': 9,
      });
      final prefs = await _prefs();
      final servidor = _Servidor({
        'GET /planes': (200, planes),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson()),
        'POST /pagos/checkout': (200, {'url': 'https://checkout.stripe.com/y'}),
      });
      final abiertas = <String>[];
      final c = _contenedor(prefs, servidor, abiertas: abiertas);
      await _pantallaPlanes(tester, c);
      expect(find.text('Todos los idiomas'), findsOneWidget);
      await _abrirPlan(tester, 'p9');
      await tester.tap(find.byKey(const ValueKey('suscribirme')));
      await tester.pumpAndSettle();
      expect(find.textContaining('idiomas de tu plan'), findsNothing);
      expect(jsonDecode(servidor.peticiones.last.body), {'planId': 'p9', 'idiomas': []});
      expect(abiertas, ['https://checkout.stripe.com/y']);
      await _fin();
    });

    testWidgets('chips y «Cambiar idiomas» permitido: PUT con los nuevos idiomas', (tester) async {
      final prefs = await _prefs();
      final servidor = _Servidor({
        'GET /planes': (200, _planesJson()),
        'GET /usuarios/me/suscripcion': (200, conIdiomas()),
        'PUT /usuarios/me/suscripcion/idiomas': (200, conIdiomas(idiomas: ['en', 'de'])),
      });
      final c = _contenedor(prefs, servidor);
      await _pantallaPlanes(tester, c);
      expect(find.byKey(const ValueKey('chip-idioma-en')), findsOneWidget);
      expect(find.byKey(const ValueKey('chip-idioma-fr')), findsOneWidget);
      await tester.tap(find.text('Cambiar idiomas'));
      await tester.pumpAndSettle();
      expect(find.text('2 de 2 elegidos'), findsOneWidget);
      await tester.tap(find.byKey(const ValueKey('idioma-plan-fr')));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const ValueKey('idioma-plan-de')));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Continuar'));
      await tester.pumpAndSettle();
      final put = servidor.peticiones.last;
      expect('${put.method} ${put.url.path}', 'PUT /usuarios/me/suscripcion/idiomas');
      expect(jsonDecode(put.body), {'idiomas': ['en', 'de']});
      expect(find.byKey(const ValueKey('chip-idioma-de')), findsOneWidget);
      expect(find.byKey(const ValueKey('chip-idioma-fr')), findsNothing);
      expect(c.read(suscripcionProvider)!.idiomas, ['en', 'de']);
      await _fin();
    });

    testWidgets('cambio no permitido: «Próximo cambio» o «Pide el cambio al soporte»', (tester) async {
      final prefs = await _prefs();
      final c = _contenedor(prefs, _Servidor({
        'GET /planes': (200, _planesJson()),
        'GET /usuarios/me/suscripcion': (200, conIdiomas(cambio: {'regla': 'uno_por_periodo', 'permitido': false, 'proximoCambio': '2026-12-01T12:00:00Z'})),
      }));
      await _pantallaPlanes(tester, c);
      expect(find.text('Cambiar idiomas'), findsNothing);
      expect(find.text('Próximo cambio: 01/12/2026'), findsOneWidget);
      c.read(suscripcionProvider.notifier).aplicar(conIdiomas(origen: 'cortesia', cambio: {'regla': 'solo_admin', 'permitido': false, 'proximoCambio': null}));
      await tester.pumpAndSettle();
      expect(find.text('Pide el cambio al soporte'), findsOneWidget);
      expect(find.text('Acceso otorgado por el administrador hasta el 20/11/2026'), findsOneWidget);
      await _fin();
    });

    testWidgets('idiomas por elegir: aviso que abre el selector con los que ya tiene', (tester) async {
      final prefs = await _prefs();
      final servidor = _Servidor({
        'GET /planes': (200, _planesJson()),
        'GET /usuarios/me/suscripcion': (200, conIdiomas(porElegir: 1)),
      });
      final c = _contenedor(prefs, servidor);
      await _pantallaPlanes(tester, c);
      expect(find.text('Te falta elegir 1 idioma de tu plan'), findsOneWidget);
      await tester.tap(find.text('Te falta elegir 1 idioma de tu plan'));
      await tester.pumpAndSettle();
      expect(find.text('Elige los 3 idiomas de tu plan'), findsOneWidget);
      expect(find.text('2 de 3 elegidos'), findsOneWidget);
      await tester.tapAt(const Offset(10, 10));
      await tester.pumpAndSettle();
      await _fin();
    });

    testWidgets('Stripe sin idiomas: sin acceso hasta elegirlos; el aviso los pide con el meta marcado', (tester) async {
      final prefs = await _prefs();
      final sinElegir = conIdiomas(idiomas: [], porElegir: 2)..['acceso'] = false;
      final servidor = _Servidor({
        'GET /planes': (200, _planesJson()),
        'GET /usuarios/me/suscripcion': (200, sinElegir),
        'PUT /usuarios/me/suscripcion/idiomas': (200, conIdiomas(idiomas: ['en', 'ja'])),
      });
      final c = _contenedor(prefs, servidor);
      await _pantallaPlanes(tester, c);
      expect(c.read(estadoPlanProvider).tienePlan, isFalse);
      // Sigue siendo su plan y puede gestionarlo.
      expect(find.text('TU PLAN'), findsOneWidget);
      expect(find.text('Gestionar suscripción'), findsOneWidget);
      await tester.tap(find.text('Te faltan 2 idiomas de tu plan por elegir'));
      await tester.pumpAndSettle();
      expect(find.text('1 de 2 elegidos'), findsOneWidget);
      await tester.tap(find.byKey(const ValueKey('idioma-plan-ja')));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Continuar'));
      await tester.pumpAndSettle();
      expect(jsonDecode(servidor.peticiones.last.body), {'idiomas': ['en', 'ja']});
      expect(c.read(estadoPlanProvider).tienePlan, isTrue);
      expect(find.textContaining('por elegir'), findsNothing);
      await _fin();
    });

    Future<void> perfil(WidgetTester tester, ProviderContainer c, String codigo) async {
      final router = GoRouter(initialLocation: '/perfil', routes: [
        GoRoute(
          path: '/perfil',
          builder: (_, _) => Scaffold(
            body: Consumer(
              builder: (context, ref, _) => TextButton(
                onPressed: () => cambiarIdiomaMetaConAviso(context, ref, codigo),
                child: const Text('CAMBIAR'),
              ),
            ),
          ),
        ),
        GoRoute(path: '/planes', builder: (_, _) => const Text('PLANES')),
      ]);
      await tester.pumpWidget(UncontrolledProviderScope(
        container: c,
        child: MaterialApp.router(theme: buildTheme(), routerConfig: router),
      ));
      await tester.tap(find.text('CAMBIAR'));
      await tester.pumpAndSettle();
    }

    testWidgets('idioma no pagado: aviso con «Añadirlo a mi plan» y «Cambiar un idioma»', (tester) async {
      final prefs = await _prefs();
      final servidor = _Servidor({'GET /usuarios/me/suscripcion': (200, conIdiomas())});
      final c = _contenedor(prefs, servidor);
      await c.read(suscripcionProvider.notifier).refrescar();
      expect(c.read(estadoPlanProvider).planId, 'p2');
      await perfil(tester, c, 'de');
      expect(c.read(progressProvider).idiomaMeta, 'de');
      expect(find.text('Este idioma no está en tu plan: estás en la prueba gratuita'), findsOneWidget);
      expect(find.text('Cambiar un idioma de mi plan'), findsOneWidget);
      await tester.tap(find.text('Cambiar un idioma de mi plan'));
      await tester.pumpAndSettle();
      // Plan lleno (2 de 2): el alumno quita uno para poner el nuevo.
      expect(find.text('2 de 2 elegidos'), findsOneWidget);
      await tester.tapAt(const Offset(10, 10));
      await tester.pumpAndSettle();
      await tester.tap(find.text('CAMBIAR'));
      await tester.pumpAndSettle();
      expect(find.text('Este idioma no está en tu plan: estás en la prueba gratuita'), findsNothing,
          reason: 'ya está en alemán: no hay cambio');
      await _fin();
    });

    testWidgets('idioma no pagado sin cambio permitido: solo «Añadirlo», que abre los planes', (tester) async {
      final prefs = await _prefs();
      final c = _contenedor(prefs, _Servidor({
        'GET /usuarios/me/suscripcion': (200, conIdiomas(cambio: {'regla': 'solo_admin', 'permitido': false})),
      }));
      await c.read(suscripcionProvider.notifier).refrescar();
      await perfil(tester, c, 'it');
      expect(find.text('Cambiar un idioma de mi plan'), findsNothing);
      await tester.tap(find.text('Añadirlo a mi plan'));
      await tester.pumpAndSettle();
      expect(find.text('PLANES'), findsOneWidget);
      await _fin();
    });

    testWidgets('idioma pagado o DEMO: sin aviso', (tester) async {
      final prefs = await _prefs(email: 'carla@onelingo.demo', planId: 'p2');
      final servidor = _Servidor({});
      final c = _contenedor(prefs, servidor);
      await perfil(tester, c, 'fr');
      expect(c.read(progressProvider).idiomaMeta, 'fr');
      expect(find.byType(AlertDialog), findsNothing);
      expect(c.read(estadoPlanProvider).planId, 'p2');
      expect(servidor.peticiones, isEmpty);
      await _fin();
    });

    test('bloqueo por idioma con accesoPorIdioma', () async {
      final prefs = await _prefs();
      final c = _contenedor(prefs, _Servidor({
        'GET /usuarios/me/suscripcion': (200, {
          ...conIdiomas(idiomas: ['en']),
          'prueba': {'minutos': 60, 'segundosUsados': 3600, 'restanteSegundos': 0, 'agotada': true},
        }),
      }));
      await c.read(suscripcionProvider.notifier).refrescar();
      var ep = c.read(estadoPlanProvider);
      expect(ep.tienePlan, isTrue);
      expect(ep.trialAgotado, isFalse);
      expect(c.read(progressProvider).planId, 'p2');
      c.read(progressProvider.notifier).cambiarIdiomaMeta('fr');
      ep = c.read(estadoPlanProvider);
      expect(ep.tienePlan, isFalse);
      expect(ep.trialAgotado, isTrue);
      // El plan local sigue al idioma: en francés cuenta la prueba.
      expect(c.read(progressProvider).planId, '');
      c.read(progressProvider.notifier).cambiarIdiomaMeta('en');
      expect(c.read(estadoPlanProvider).trialAgotado, isFalse);
      expect(c.read(progressProvider).planId, 'p2');
    });

    test('cambiar de idioma conserva la ubicación de cada idioma', () async {
      final prefs = await _prefs(sesion: false);
      final c = _contenedor(prefs, _Servidor({}));
      final n = c.read(progressProvider.notifier);
      n.guardarDiagnostico({'idioma': 'en', 'escala': escalaDiagnosticoCliente}, 6);
      final enIngles = c.read(progressProvider);
      n.cambiarIdiomaMeta('fr');
      expect(c.read(progressProvider).idiomaMeta, 'fr');
      expect(c.read(progressProvider).nivelInicial, 1);
      expect(c.read(progressProvider).diagnostico, isNull);
      n.cambiarIdiomaMeta('en');
      final vuelta = c.read(progressProvider);
      expect(vuelta.nivelCliente, enIngles.nivelCliente);
      expect(vuelta.nivelEscala, enIngles.nivelEscala);
      expect(vuelta.diagnostico, enIngles.diagnostico);
    });
  });

  group('vuelta de Checkout', () {
    Future<GoRouter> pantallaPago(WidgetTester tester, ProviderContainer c, String ruta) async {
      final router = GoRouter(
        initialLocation: ruta,
        routes: [
          GoRoute(
            path: '/pago',
            builder: (_, s) => PagoScreen(
              estado: s.uri.queryParameters['estado'] ?? '',
              sessionId: s.uri.queryParameters['session_id'],
            ),
          ),
          GoRoute(path: '/inicio', builder: (_, _) => const Text('INICIO')),
          GoRoute(path: '/planes', builder: (_, _) => const Text('PLANES')),
        ],
      );
      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: c,
          child: MaterialApp.router(theme: buildTheme(), routerConfig: router),
        ),
      );
      await tester.pumpAndSettle();
      return router;
    }

    testWidgets('estado=ok confirma, muestra el plan y vuelve al inicio', (tester) async {
      final prefs = await _prefs();
      final servidor = _Servidor({
        'POST /pagos/confirmar': (200, _suscripcionJson(planId: 'p2', estado: 'activa', origen: 'stripe', acceso: true, puedeGestionar: true)),
      });
      final c = _contenedor(prefs, servidor);
      c.read(catalogoPlanesProvider.notifier).state = CatalogoPlanes.fromJson(_planesJson());
      await pantallaPago(tester, c, '/pago?estado=ok&session_id=cs_test_9');
      expect(jsonDecode(servidor.peticiones.single.body), {'sessionId': 'cs_test_9'});
      expect(find.text('¡Listo! Tu plan Dos idiomas está activo'), findsOneWidget);
      expect(c.read(estadoPlanProvider).planId, 'p2');
      expect(c.read(progressProvider).planId, 'p2');
      await tester.pump(const Duration(seconds: 5));
      await tester.pumpAndSettle();
      expect(find.text('INICIO'), findsOneWidget);
      await _fin();
    });

    testWidgets('estado=ok con error del servidor lo muestra', (tester) async {
      final prefs = await _prefs();
      final c = _contenedor(prefs, _Servidor({
        'POST /pagos/confirmar': (400, {'error': 'Sesión de pago no válida'}),
      }));
      await pantallaPago(tester, c, '/pago?estado=ok&session_id=cs_x');
      expect(find.text('Sesión de pago no válida'), findsOneWidget);
      await tester.tap(find.text('Volver al inicio'));
      await tester.pumpAndSettle();
      expect(find.text('INICIO'), findsOneWidget);
      await _fin();
    });

    testWidgets('estado=cancelado: «Pago cancelado»', (tester) async {
      final prefs = await _prefs();
      final servidor = _Servidor({});
      final c = _contenedor(prefs, servidor);
      await pantallaPago(tester, c, '/pago?estado=cancelado');
      expect(find.text('Pago cancelado'), findsOneWidget);
      expect(servidor.peticiones, isEmpty);
      await _fin();
    });

    testWidgets('estado=portal: refresca la suscripción y abre los planes', (tester) async {
      final prefs = await _prefs();
      final servidor = _Servidor({
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson(planId: 'p3', estado: 'activa', origen: 'stripe', acceso: true)),
      });
      final c = _contenedor(prefs, servidor);
      await pantallaPago(tester, c, '/pago?estado=portal');
      expect(servidor.rutasPedidas, ['GET /usuarios/me/suscripcion']);
      expect(find.text('PLANES'), findsOneWidget);
      expect(c.read(estadoPlanProvider).planId, 'p3');
      await _fin();
    });
  });

  group('duraciones, familia y empresas', () {
    Map<String, dynamic> conDuraciones() {
      final j = _planesJson();
      j['planes'] = <Object>[...j['planes'] as List, 
        {
          'id': 'p1m', 'nombre': {'es': 'Básico', 'en': 'Basic'}, 'incluye': {'es': ['1 idioma'], 'en': []},
          'idiomas': 1, 'precio': 20, 'moneda': 'usd', 'intervalo': 'mes', 'orden': 3, 'usuarios': 1,
          'duraciones': [
            {'meses': 1, 'precio': 20}, {'meses': 3, 'precio': 55}, {'meses': 6, 'precio': 110}, {'meses': 12, 'precio': 220},
          ],
        },
        {
          'id': 'familiar', 'nombre': {'es': 'Familiar', 'en': 'Family'}, 'incluye': {'es': [], 'en': []},
          'idiomas': 1, 'precio': 60, 'moneda': 'usd', 'intervalo': 'mes', 'orden': 4, 'usuarios': 4,
          'duraciones': [{'meses': 1, 'precio': 60}, {'meses': 12, 'precio': 600}],
        },
      ];
      return j;
    }

    test('ahorro frente a pagar mes a mes y respaldo sin duraciones', () {
      final p = CatalogoPlanes.fromJson(conDuraciones());
      final b = p.plan('p1m')!;
      expect(b.duraciones.map((d) => d.meses), [1, 3, 6, 12]);
      expect([for (final d in b.duraciones) b.ahorro(d)], [0, 8, 8, 8]);
      expect(p.plan('familiar')!.familiar, isTrue);
      // Servidor anterior a las duraciones: una sola opción, la del cobro del plan.
      expect(p.plan('p1')!.duraciones.map((d) => d.meses), [12]);
      expect(p.plan('p2')!.duraciones.map((d) => d.meses), [1]);
    });

    testWidgets('detalle: elegir 3 meses manda meses al checkout; «4 usuarios» en el Familiar', (tester) async {
      final prefs = await _prefs();
      final servidor = _Servidor({
        'GET /planes': (200, conDuraciones()),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson()),
        'POST /pagos/checkout': (200, {'url': 'https://checkout.stripe.com/z'}),
      });
      final c = _contenedor(prefs, servidor, abiertas: []);
      await _pantallaPlanes(tester, c);
      expect(find.text('4 usuarios'), findsOneWidget);
      await _abrirPlan(tester, 'p1m');
      expect(find.text('Elige la duración de tu suscripción'), findsOneWidget);
      expect(find.text('Sin descuento'), findsOneWidget);
      expect(find.text('Ahorra 8 %'), findsNWidgets(3));
      expect(find.text(r'$18.33 al mes'), findsNWidgets(3));
      await tester.tap(find.byKey(const ValueKey('duracion-3')));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const ValueKey('suscribirme')));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Continuar').last);
      await tester.pumpAndSettle();
      expect(jsonDecode(servidor.peticiones.last.body), {'planId': 'p1m', 'idiomas': ['en'], 'meses': 3});
      await _fin();
    });

    testWidgets('titular: ve su familia, añade por correo y quita', (tester) async {
      final prefs = await _prefs();
      final familia = {
        'rol': 'titular', 'plazas': 3,
        'miembros': [{'email': 'hijo@correo.com', 'nombre': 'Hijo', 'estado': 'activo'}],
        'titular': null,
      };
      final servidor = _Servidor({
        'GET /planes': (200, conDuraciones()),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson(planId: 'familiar', estado: 'activa', origen: 'cortesia', acceso: true)..['usuariosPlan'] = 4),
        'GET /usuarios/me/familia': (200, familia),
        'POST /usuarios/me/familia': (200, {
          ...familia,
          'miembros': [...familia['miembros'] as List, {'email': 'tia@correo.com', 'nombre': '', 'estado': 'pendiente'}],
        }),
      });
      final c = _contenedor(prefs, servidor);
      await _pantallaPlanes(tester, c);
      await tester.tap(find.byKey(const ValueKey('tarjeta-familia')));
      await tester.pumpAndSettle();
      expect(find.text('Personas en tu plan'), findsOneWidget);
      expect(find.text('Hijo'), findsOneWidget);
      expect(find.text('1 de 3 personas'), findsOneWidget);
      await tester.enterText(find.byKey(const ValueKey('correo-familiar')), 'Tia@Correo.com');
      await tester.tap(find.text('Añadir a mi plan'));
      await tester.pumpAndSettle();
      final p = servidor.peticiones.lastWhere((r) => r.method == 'POST');
      expect(jsonDecode(p.body), {'email': 'tia@correo.com'});
      expect(find.text('Pendiente'), findsOneWidget);
      expect(find.text('2 de 3 personas'), findsOneWidget);
      await _fin();
    });

    testWidgets('empresa: valida y envía la cotización', (tester) async {
      final prefs = await _prefs();
      final servidor = _Servidor({
        'GET /planes': (200, conDuraciones()),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson()),
        'POST /cotizaciones': (201, {'id': 1}),
      });
      final c = _contenedor(prefs, servidor);
      await _pantallaPlanes(tester, c);
      await tester.tap(find.byKey(const ValueKey('plan-empresa')));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const ValueKey('cot-enviar')));
      await tester.pumpAndSettle();
      expect(find.text('Campo obligatorio'), findsOneWidget);
      expect(find.text('Elige al menos un idioma'), findsOneWidget);
      expect(servidor.rutasPedidas, isNot(contains('POST /cotizaciones')));
      await tester.enterText(find.byKey(const ValueKey('cot-empresa')), 'Acme');
      await tester.enterText(find.byKey(const ValueKey('cot-empleados')), '50');
      await tester.tap(find.byKey(const ValueKey('cot-idioma-fr')));
      await tester.tap(find.byKey(const ValueKey('cot-idioma-en')));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const ValueKey('cot-enviar')));
      await tester.pumpAndSettle();
      final p = servidor.peticiones.last;
      expect('${p.method} ${p.url.path}', 'POST /cotizaciones');
      final cuerpo = jsonDecode(p.body) as Map;
      expect([cuerpo['empresa'], cuerpo['empleados'], cuerpo['idiomas'], cuerpo['email']], ['Acme', 50, ['en', 'fr'], 'alumna@correo.com']);
      expect(find.byKey(const ValueKey('cotizacion-enviada')), findsOneWidget);
      await _fin();
    });
  });

  group('Google Play (Android)', () {
    Map<String, dynamic> conGoogle({bool disponible = true}) {
      final j = _planesJson(disponible: false);
      j['google'] = {'disponible': disponible, 'paquete': 'com.torisoftt.onelingo'};
      j['planes'] = <Object>[
        for (final p in j['planes'] as List) {...p as Map<String, dynamic>, 'google': {'producto': 'plan_${p['id']}'}},
        {
          'id': 'p1m', 'nombre': {'es': 'Básico', 'en': 'Basic'}, 'incluye': {'es': ['1 idioma'], 'en': []},
          'idiomas': 1, 'precio': 20, 'moneda': 'usd', 'intervalo': 'mes', 'orden': 3, 'usuarios': 1,
          'duraciones': [{'meses': 1, 'precio': 20}, {'meses': 3, 'precio': 55}],
          'google': {'producto': 'plan_p1m', 'planesBase': ['mes-1', 'mes-3']},
        },
      ];
      return j;
    }

    Map<String, dynamic> deGoogle({String planId = 'p1m', String planBase = 'mes-3', String estado = 'activa'}) => {
      ..._suscripcionJson(planId: planId, estado: estado, origen: 'google', acceso: true, periodoFin: '2027-01-15T00:00:00Z', idiomas: ['en']),
      'accesoPlan': true,
      'meses': 3,
      'google': {'producto': 'plan_$planId', 'planBase': planBase},
    };

    test('catálogo: Google Play disponible y producto de cada plan; suscripción de Play', () {
      final cat = CatalogoPlanes.fromJson(conGoogle());
      expect(cat.googleDisponible, isTrue);
      expect(cat.googlePaquete, 'com.torisoftt.onelingo');
      expect(cat.plan('p1m')!.googleProducto, 'plan_p1m');
      expect(CatalogoPlanes.fromJson(_planesJson()).googleDisponible, isFalse);
      final s = Suscripcion.fromJson(deGoogle());
      expect(s.esGoogle && s.googleVigente && s.pagoVigente, isTrue);
      expect(s.stripeVigente, isFalse);
      expect(s.googlePlanBase, 'mes-3');
    });

    testWidgets('comprar: precios de Play, idiomas, compra en Play, verifica en el servidor y la completa', (tester) async {
      final prefs = await _prefs();
      final tienda = _TiendaFalsa(preciosFalsos: {
        'plan_p1m|mes-1': const PrecioPlay(texto: r'US$20.00', valor: 20, moneda: 'USD'),
        'plan_p1m|mes-3': const PrecioPlay(texto: r'US$55.00', valor: 55, moneda: 'USD'),
      });
      final servidor = _Servidor({
        'GET /planes': (200, conGoogle()),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson()),
        'POST /pagos/google/verificar': (200, deGoogle()),
      });
      final c = _contenedor(prefs, servidor, enApp: true, tienda: tienda);
      c.read(comprasPlayProvider);
      await _pantallaPlanes(tester, c);
      expect(find.text('Pago seguro con Google Play. Cancela cuando quieras desde Google Play.'), findsOneWidget);
      await _abrirPlan(tester, 'p1m');
      expect(find.text(r'US$55.00'), findsOneWidget, reason: 'precio de Google en la moneda del alumno');
      expect(find.text(r'$18.33 al mes'), findsOneWidget);
      await tester.tap(find.byKey(const ValueKey('duracion-3')));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const ValueKey('suscribirme')));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Continuar').last);
      // Google abre su hoja de pago: mientras, el botón espera (no se asienta).
      await tester.pump();
      await tester.pump();
      expect(tienda.abiertas, ['plan_p1m|mes-3|u1']);
      expect(servidor.rutasPedidas, isNot(contains('POST /pagos/checkout')));
      tienda.entregar(const CompraPlay(estado: EstadoCompraPlay.comprada, token: 'tok-play-1', producto: 'plan_p1m'));
      await tester.pumpAndSettle();
      final v = servidor.peticiones.lastWhere((r) => r.url.path == '/pagos/google/verificar');
      expect(jsonDecode(v.body), {'token': 'tok-play-1', 'idiomas': ['en']});
      expect(tienda.completadas, ['tok-play-1']);
      expect(c.read(suscripcionProvider)!.esGoogle, isTrue);
      expect(find.text('¡Listo! Tu plan ya está activo.'), findsOneWidget);
      expect(find.byKey(const ValueKey('plan-p1m')), findsOneWidget, reason: 'vuelve a la lista');
      await _fin();
    });

    testWidgets('verificación fallida: no completa la compra y avisa', (tester) async {
      final prefs = await _prefs();
      final tienda = _TiendaFalsa();
      final servidor = _Servidor({
        'GET /planes': (200, conGoogle()),
        'GET /usuarios/me/suscripcion': (200, _suscripcionJson()),
        'POST /pagos/google/verificar': (502, {'error': 'Google Play: caído'}),
      });
      final c = _contenedor(prefs, servidor, enApp: true, tienda: tienda);
      c.read(comprasPlayProvider);
      await _pantallaPlanes(tester, c);
      await _abrirPlan(tester, 'p2');
      tienda.entregar(const CompraPlay(estado: EstadoCompraPlay.comprada, token: 'tok-play-2', producto: 'plan_p2'));
      await tester.pumpAndSettle();
      expect(tienda.completadas, isEmpty);
      expect(find.text('Recibimos tu pago, pero aún no pudimos confirmarlo. Lo intentaremos de nuevo al abrir la app.'), findsOneWidget);
      await _fin();
    });

    testWidgets('al arrancar: verifica en silencio las compras cobradas sin completar', (tester) async {
      final prefs = await _prefs();
      final tienda = _TiendaFalsa(pendientes: const [CompraPlay(estado: EstadoCompraPlay.comprada, token: 'tok-viejo', producto: 'plan_p1m')]);
      final servidor = _Servidor({'POST /pagos/google/verificar': (200, deGoogle())});
      final c = _contenedor(prefs, servidor, enApp: true, tienda: tienda);
      c.read(catalogoPlanesProvider.notifier).state = CatalogoPlanes.fromJson(conGoogle());
      await c.read(comprasPlayProvider.notifier).reintentarPendientes();
      expect(tienda.completadas, ['tok-viejo']);
      expect(c.read(suscripcionProvider)!.planId, 'p1m');
      await _fin();
    });

    testWidgets('suscrito en Play: «Gestionar en Google Play», cambiar duración o plan reemplaza la compra', (tester) async {
      final prefs = await _prefs();
      final abiertas = <String>[];
      final tienda = _TiendaFalsa();
      final servidor = _Servidor({'GET /planes': (200, conGoogle()), 'GET /usuarios/me/suscripcion': (200, deGoogle())});
      final c = _contenedor(prefs, servidor, enApp: true, tienda: tienda, abiertas: abiertas);
      await _pantallaPlanes(tester, c);
      expect(find.text('Pago cada 3 meses'), findsOneWidget);
      await tester.tap(find.text('Gestionar en Google Play'));
      await tester.pumpAndSettle();
      expect(abiertas, ['https://play.google.com/store/account/subscriptions?sku=plan_p1m&package=com.torisoftt.onelingo']);
      // Mismo plan y duración: PLAN ACTUAL; otra duración: cambiarla en Play, sin volver a elegir idiomas.
      await _abrirPlan(tester, 'p1m');
      await tester.tap(find.byKey(const ValueKey('duracion-3')));
      await tester.pumpAndSettle();
      expect(_boton(tester, 'PLAN ACTUAL').onPressed, isNull);
      await tester.tap(find.byKey(const ValueKey('duracion-1')));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Cambiar la duración'));
      await tester.pump();
      await tester.pump();
      expect(tienda.abiertas, ['plan_p1m|mes-1|u1']);
      expect(tienda.anterior, 'plan_p1m');
      // El alumno cierra la hoja de Google sin pagar: el botón vuelve.
      tienda.entregar(const CompraPlay(estado: EstadoCompraPlay.cancelada, producto: 'plan_p1m'));
      await tester.pumpAndSettle();
      await _volver(tester);
      await _abrirPlan(tester, 'p2');
      await tester.tap(find.text('Cambiar a este plan'));
      await tester.pump();
      await tester.pump();
      expect(tienda.abiertas.last, 'plan_p2|mes-1|u1');
      tienda.entregar(const CompraPlay(estado: EstadoCompraPlay.cancelada, producto: 'plan_p2'));
      await tester.pumpAndSettle();
      await _fin();
    });

    testWidgets('Android sin Google Play en el servidor: «Pagos próximamente»; pagada en la web: sin Stripe', (tester) async {
      final prefs = await _prefs();
      var servidor = _Servidor({'GET /planes': (200, conGoogle(disponible: false)), 'GET /usuarios/me/suscripcion': (200, _suscripcionJson())});
      var c = _contenedor(prefs, servidor, enApp: true);
      await _pantallaPlanes(tester, c);
      await _abrirPlan(tester, 'p2');
      expect(_boton(tester, 'Pagos próximamente').onPressed, isNull);
      await _fin();
      final web = _suscripcionJson(planId: 'p1', estado: 'activa', origen: 'stripe', acceso: true, puedeGestionar: true, periodoFin: '2027-01-01T00:00:00Z');
      servidor = _Servidor({'GET /planes': (200, conGoogle()), 'GET /usuarios/me/suscripcion': (200, web)});
      c = _contenedor(await _prefs(), servidor, enApp: true);
      await tester.pumpWidget(const SizedBox()); // pantalla nueva: vuelve a pedir la suscripción
      await _pantallaPlanes(tester, c);
      expect(find.text('Pagada en la web: se gestiona desde onelingo.org.'), findsOneWidget);
      expect(find.text('Gestionar suscripción'), findsNothing);
      expect(find.text('Modo de prueba: usa la tarjeta 4242 4242 4242 4242'), findsNothing);
      await _abrirPlan(tester, 'p2');
      expect(find.text('Tu suscripción se gestiona en la web'), findsOneWidget);
      expect(servidor.rutasPedidas, isNot(contains('POST /pagos/portal')));
      await _fin();
    });
  });
}
