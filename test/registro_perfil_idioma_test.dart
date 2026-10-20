import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/api/sync.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/providers.dart';
import 'package:onelingo/core/content/curriculum.dart';
import 'package:onelingo/core/i18n/i18n.dart';
import 'package:onelingo/core/i18n/nombres_idioma.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/onboarding/onboarding_screen.dart';
import 'package:onelingo/features/onboarding/welcome_screen.dart';
import 'package:onelingo/features/progress/progress_screen.dart';

/// Registro, perfil y bienvenida sin suponer que el idioma meta es inglés
/// (errores vistos en Android con un hispanohablante que aprende japonés).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final cargador = CargadorRuta();
  tearDown(() => I18n.idioma.value = 'es');

  /// Monta [pantalla] con la ruta de [idiomas] ya cargada y [prefs].
  Future<void> montar(
    WidgetTester tester,
    Widget pantalla, {
    required List<String> idiomas,
    Map<String, Object> prefs = const {},
  }) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    SharedPreferences.setMockInitialValues(prefs);
    final p = await SharedPreferences.getInstance();
    Sync.instancia.inicializar(p);
    // La ruta se lee de assets fuera del reloj simulado de la prueba.
    await tester.runAsync(
      () => Future.wait([for (final i in idiomas) cargador.cargar(i)]),
    );
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          prefsProvider.overrideWithValue(p),
          cargadorRutaProvider.overrideWithValue(cargador),
        ],
        child: MaterialApp(theme: buildTheme(), home: pantalla),
      ),
    );
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 200)),
    );
    await tester.pumpAndSettle();
  }

  Map<String, Object> borrador(String meta, int paso) => {
    'onelingo.api.token': 'test',
    'onelingo.api.email': 'test@example.com',
    'onelingo.onboarding.draft.v2': jsonEncode({
      'correo': 'test@example.com',
      'nombre': 'Test',
      'nativo': 'es',
      'meta': meta,
      'sectores': ['estudiante'],
      'objetivos': ['estudiar'],
      'nivel': 1,
      'paso': paso,
    }),
  };

  test('el idioma dentro de una frase: minúscula en español, «Japanese» en inglés', () {
    expect(nombreIdiomaEnFrase('ja'), 'japonés');
    expect(nombreIdiomaEnFrase('zh'), 'chino');
    final en = Map<String, String>.from(
      jsonDecode(File('assets/i18n/en.json').readAsStringSync()) as Map,
    );
    I18n.usar('en', en);
    I18n.idioma.value = 'en';
    expect(nombreIdiomaEnFrase('ja'), 'Japanese');
    expect(
      tr('¿Qué quieres lograr con el {idioma}?', {
        'idioma': nombreIdiomaEnFrase('ja'),
      }),
      'What do you want to achieve with Japanese?',
    );
  });

  testWidgets('paso 5: los objetivos nombran el idioma elegido', (tester) async {
    await montar(
      tester,
      const OnboardingScreen(),
      idiomas: const ['ja'],
      prefs: borrador('ja', 4),
    );
    expect(find.text('Paso 5 de 7'), findsOneWidget);
    expect(find.text('¿Qué quieres lograr con el japonés?'), findsOneWidget);
    expect(find.textContaining('inglés'), findsNothing);
    await Sync.instancia.cerrarSesion();
  });

  test('paso 6: las descripciones de nivel no son gramática del inglés', () {
    for (final n in niveles) {
      for (final ingles in ['presente simple', 'phrasal', 'irregulares', 'continuo']) {
        expect(n.descripcion.toLowerCase(), isNot(contains(ingles)), reason: 'N${n.numero}');
      }
    }
  });

  test('las cifras del curso salen de la ruta de cada idioma', () async {
    final ja = (await cargador.cargar('ja'))!;
    final en = (await cargador.cargar('en'))!;
    expect(clasesPorNivel(ja), 50);
    expect(clasesPorNivel(en), 100);
    // La prueba de nivel pide 27 de 30: el 90 %, no el 65 % del examen antiguo.
    expect(porcentajePruebaNivel, 90);
  });

  testWidgets('paso 7: clases reales por nivel y prueba al 90 %', (tester) async {
    await montar(
      tester,
      const OnboardingScreen(),
      idiomas: const ['ja'],
      prefs: borrador('ja', 6),
    );
    expect(find.text('Paso 7 de 7'), findsOneWidget);
    expect(find.textContaining('50 clases por nivel'), findsOneWidget);
    expect(find.textContaining('(90 %)'), findsOneWidget);
    expect(find.textContaining('100 lecciones'), findsNothing);
    expect(find.textContaining('65 %'), findsNothing);
    await Sync.instancia.cerrarSesion();
  });

  test('posición en la ruta: Fundamentos o el nivel de la ubicación', () async {
    final ja = (await cargador.cargar('ja'))!;
    final desdeCero = posicionEnRuta(
      ja,
      const ProgressState(idiomaMeta: 'ja', nivelInicial: 0, fundamentos: true),
    );
    expect(desdeCero.nivel, 'f0');
    expect(desdeCero.clase, 1);
    expect(desdeCero.total, ja.delNivel('f0').length);
    expect(desdeCero.aprobadas, 0);
    final fr = (await cargador.cargar('fr'))!;
    final ubicado = posicionEnRuta(
      fr,
      const ProgressState(idiomaMeta: 'fr', nivelInicial: 3),
    );
    expect(ubicado.nivel, 'n3');
    expect(ubicado.clase, 1);
    expect(ubicado.total, 50);
  });

  testWidgets('perfil: nivel y clase actuales de la ruta, no del modelo de 100', (
    tester,
  ) async {
    await montar(
      tester,
      const ProgressScreen(),
      idiomas: const ['fr'],
      prefs: {
        'onelingo.progress.v1': jsonEncode(
          const ProgressState(
            onboardingDone: true,
            idiomaMeta: 'fr',
            nivelInicial: 3,
          ).toJson(),
        ),
      },
    );
    expect(find.text('Nivel 3 · B1'), findsWidgets);
    expect(find.text('1/50'), findsOneWidget);
    expect(find.text('Clase actual'), findsOneWidget);
    expect(find.textContaining('Lección 100'), findsNothing);
    expect(find.textContaining('/100'), findsNothing);
  });

  testWidgets('fuera de la web no se ofrece descargar el APK', (tester) async {
    await montar(tester, const WelcomeScreen(), idiomas: const []);
    expect(find.text('Descarga la app para Android'), findsNothing);
  });
}
