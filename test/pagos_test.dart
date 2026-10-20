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
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/i18n/i18n.dart';
import 'package:onelingo/core/pagos/providers.dart';
import 'package:onelingo/core/state/providers.dart';
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

ProviderContainer _contenedor(
  SharedPreferences prefs,
  _Servidor servidor, {
  List<String>? abiertas,
}) {
  final c = ProviderContainer(
    overrides: [
      prefsProvider.overrideWithValue(prefs),
      pagosApiProvider.overrideWithValue(PagosApi(cliente: servidor.cliente)),
      abrirUrlProvider.overrideWithValue((url) async {
        abiertas?.add(url);
        return true;
      }),
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
      expect(find.text('Choose 2 languages'), findsOneWidget);
      expect(find.text('/ year'), findsOneWidget);
      expect(find.text('Test mode: use card 4242 4242 4242 4242'), findsOneWidget);
      expect(find.text('Subscribe'), findsNWidgets(2));
      await tester.tap(find.text('Subscribe').last);
      await tester.pumpAndSettle();
      final checkout = servidor.peticiones.last;
      expect('${checkout.method} ${checkout.url.path}', 'POST /pagos/checkout');
      expect(jsonDecode(checkout.body), {'planId': 'p2'});
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
      expect(find.text('Pagos próximamente'), findsNWidgets(2));
      expect(_boton(tester, 'Pagos próximamente').onPressed, isNull);
      expect(find.text('Suscribirme'), findsNothing);
      expect(find.textContaining('4242'), findsNothing);
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
      expect(find.text('Suscribirme'), findsNWidgets(2));
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
      expect(find.text('PLAN ACTUAL'), findsOneWidget);
      expect(find.text('TU PLAN'), findsOneWidget);
      expect(find.text('Cambiar de plan'), findsOneWidget);
      // Con suscripción activa no hay banner de prueba.
      expect(find.text('Prueba gratuita en curso'), findsNothing);
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
      await tester.tap(find.text('Suscribirme').first);
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
      expect(find.text('Suscribirme'), findsNothing);
      expect(find.textContaining('4242'), findsNothing);
      await tester.tap(find.text('ELEGIR DOS IDIOMAS'));
      await tester.pumpAndSettle();
      expect(c.read(progressProvider).planId, 'p2');
      expect(servidor.rutasPedidas, isNot(contains('POST /pagos/checkout')));
      expect(find.text('PLAN ACTUAL'), findsOneWidget);
      await _fin();
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
}
