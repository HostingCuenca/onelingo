import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/content/learning_units.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/library/learning_unit_screen.dart';
import 'package:onelingo/shared/widgets/widgets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  Future<ProviderContainer> montar(
    WidgetTester tester,
    Widget pantalla, {
    double escala = 1,
    Map<String, Object> prefs = const {},
  }) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    SharedPreferences.setMockInitialValues(prefs);
    final sp = await SharedPreferences.getInstance();
    Efectos.sonido = false;
    Efectos.vibraciones.value = false;
    final container = ProviderContainer(
      overrides: [prefsProvider.overrideWithValue(sp)],
    );
    addTearDown(container.dispose);
    // Carga real de los JSON: fuera del reloj falso del test.
    for (final skill in ['reading', 'listening']) {
      await tester.runAsync(
        () => container.read(learningUnitsProvider(skill).future),
      );
    }
    await tester.pumpWidget(
      UncontrolledProviderScope(
        container: container,
        child: MaterialApp(
          theme: buildTheme(),
          builder: (context, child) => MediaQuery(
            data: MediaQuery.of(context).copyWith(
              textScaler: TextScaler.linear(escala),
              disableAnimations: true,
            ),
            child: child!,
          ),
          home: pantalla,
        ),
      ),
    );
    await tester.pumpAndSettle();
    return container;
  }

  Future<void> tocar(WidgetTester tester, Finder f) async {
    await tester.ensureVisible(f);
    await tester.pumpAndSettle();
    await tester.tap(f);
    await tester.pumpAndSettle();
  }

  VoidCallback? accion(WidgetTester tester, String texto) => tester
      .widget<BotonPrincipal>(find.widgetWithText(BotonPrincipal, texto))
      .onPressed;

  for (final escala in [1.0, 2.0]) {
    testWidgets('Lectura: palabras, texto y una pregunta por pantalla x$escala', (
      tester,
    ) async {
      final c = await montar(
        tester,
        const LearningUnitScreen(skill: 'reading'),
        escala: escala,
      );
      expect(find.text('Lectura'), findsOneWidget);
      expect(find.byType(DropdownButtonFormField<int>), findsNothing);
      expect(find.textContaining('Nivel interno'), findsNothing);
      await tocar(tester, find.text('Una nueva clase'));

      expect(find.text('Antes de empezar'), findsOneWidget);
      expect(find.text('Palabras clave'), findsOneWidget);
      await tocar(tester, find.text('EMPEZAR A LEER'));
      await tocar(tester, find.text('RESPONDER'));

      // Una pregunta: COMPROBAR espera a que se elija una opción.
      expect(find.text('1 de 3'), findsOneWidget);
      expect(accion(tester, 'COMPROBAR'), isNull);
      await tocar(tester, find.text('Eva'));
      expect(accion(tester, 'COMPROBAR'), isNotNull);
      await tocar(tester, find.text('COMPROBAR'));
      expect(find.text('Casi'), findsOneWidget);
      final p = c
          .read(progressProvider)
          .practicas['learn-reading-en-reading-n01-new-class-en-reading-n01-new-class-q1'];
      expect(p['correcta'], false);
      expect(p['idioma'], 'en');
      expect(p['skill'], 'reading');

      await tocar(tester, find.text('CONTINUAR'));
      expect(find.text('2 de 3'), findsOneWidget);
      await tocar(tester, find.text('In room six'));
      await tocar(tester, find.text('COMPROBAR'));
      expect(find.text('¡Bien!'), findsOneWidget);
      await tocar(tester, find.text('CONTINUAR'));
      await tocar(tester, find.text('Eva and her English class'));
      await tocar(tester, find.text('COMPROBAR'));
      await tocar(tester, find.text('CONTINUAR'));

      expect(find.text('2 de 3 correctas'), findsOneWidget);
      for (final jerga in [
        'Comprobación guiada',
        'Evidencia',
        'Bien razonado',
        'retención',
      ]) {
        expect(find.textContaining(jerga), findsNothing);
      }
      await tocar(tester, find.text('OTRA LECTURA'));
      expect(find.text('Antes de empezar'), findsOneWidget);
      expect(find.text('Un pedido sencillo'), findsOneWidget);
      expect(tester.takeException(), isNull);
    });
  }

  testWidgets('Escucha: transcripción oculta y COMPROBAR exige el audio', (
    tester,
  ) async {
    await montar(tester, const LearningUnitScreen(skill: 'listening'));
    expect(find.text('Escucha'), findsOneWidget);
    await tocar(tester, find.text('La primera clase'));
    await tocar(tester, find.widgetWithText(BotonPrincipal, 'ESCUCHAR'));
    expect(find.text('Ver transcripción'), findsOneWidget);
    expect(find.byType(SelectableText), findsNothing);
    await tocar(tester, find.text('Ver transcripción'));
    expect(find.byType(SelectableText), findsOneWidget);
    await tocar(tester, find.text('RESPONDER'));
    await tocar(tester, find.text('In an English class'));
    // Sin haber escuchado el audio no se puede comprobar.
    expect(accion(tester, 'COMPROBAR'), isNull);
    expect(find.text('Escucha el audio primero.'), findsOneWidget);
  });

  testWidgets('Vocabulario ya no existe: se abre como lectura', (tester) async {
    await montar(tester, const LearningUnitScreen(skill: 'vocabulario'));
    expect(find.text('Lectura'), findsOneWidget);
    expect(find.text('Una nueva clase'), findsOneWidget);
  });

  testWidgets('Usa el nivel del alumno, no un selector', (tester) async {
    await montar(
      tester,
      const LearningUnitScreen(skill: 'reading'),
      prefs: {
        'onelingo.progress.v1': jsonEncode({
          'onboardingDone': true,
          'idiomaMeta': 'en',
          'nivelInicial': 3,
          'fundamentos': false,
        }),
      },
    );
    expect(find.text('Nivel 3'), findsOneWidget);
    expect(find.text('Cambio de planes'), findsOneWidget);
    expect(find.text('Una nueva clase'), findsNothing);
  });
}
