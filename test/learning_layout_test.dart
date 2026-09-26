import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/providers.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/content/foundations.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/shared/widgets/streak_card.dart';
import 'package:onelingo/shared/widgets/learning_path.dart';

void main() {
  testWidgets('Racha y todas las áreas siguen legibles con texto grande', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(320, 740);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    // Principiante que empieza de cero (onboarding: fundamentos = true).
    SharedPreferences.setMockInitialValues({
      'onelingo.progress.v1': jsonEncode({
        'onboardingDone': true,
        'idiomaMeta': 'en',
        'nivelInicial': 1,
        'fundamentos': true,
      }),
    });
    final prefs = await SharedPreferences.getInstance();
    Efectos.animaciones.value = false;
    final cargador = CargadorRuta();
    await tester.runAsync(() => cargador.cargar('en'));
    final container = ProviderContainer(
      overrides: [
        prefsProvider.overrideWithValue(prefs),
        cargadorRutaProvider.overrideWithValue(cargador),
      ],
    );
    addTearDown(container.dispose);
    Future<void> render(String recommendation) => tester.pumpWidget(
      UncontrolledProviderScope(
        container: container,
        child: MaterialApp(
          builder: (context, child) => MediaQuery(
            data: MediaQuery.of(context)
                .copyWith(textScaler: const TextScaler.linear(3)),
            child: child!,
          ),
          home: Scaffold(
            body: SingleChildScrollView(
              child: Column(
                children: [
                  const StreakCard(),
                  LearningPath(
                    nivel: 1,
                    recommended: recommendation,
                    practices: const {},
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
    await render('gramatica');
    await tester.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 50)));
    await tester.pumpAndSettle();
    expect(tester.takeException(), isNull);
    expect(find.text('Gramática'), findsOneWidget);
    await render('listening');
    await tester.pumpAndSettle();
    expect(find.text('Gramática'), findsOneWidget);
    expect(find.byType(InkWell), findsNWidgets(6));
    expect(find.textContaining('Empieza desde cero'), findsOneWidget);
    expect(tester.takeException(), isNull);
    await tester.pumpWidget(const SizedBox());
  });
  testWidgets(
    'Fundamentos muestra el próximo paso sin confundir práctica con dominio',
    (tester) async {
      SharedPreferences.setMockInitialValues({
        'onelingo.progress.v1': jsonEncode({
          'onboardingDone': true,
          'idiomaMeta': 'en',
          'nivelInicial': 1,
          'fundamentos': true,
        }),
      });
      final prefs = await SharedPreferences.getInstance();
      final cargador = CargadorRuta();
      final ruta = (await tester.runAsync(() => cargador.cargar('en')))!!;
      final container = ProviderContainer(
        overrides: [
          prefsProvider.overrideWithValue(prefs),
          cargadorRutaProvider.overrideWithValue(cargador),
        ],
      );
      addTearDown(container.dispose);
      final notifier = container.read(progressProvider.notifier);
      Future<void> render() async {
        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: SingleChildScrollView(
                  child: LearningPath(
                    nivel: 1,
                    recommended: 'gramatica',
                    practices: {},
                  ),
                ),
              ),
            ),
          ),
        );
        await tester.runAsync(
          () => Future<void>.delayed(const Duration(milliseconds: 50)),
        );
        await tester.pumpAndSettle();
      }

      await render();
      expect(find.text('Empieza desde cero'), findsOneWidget);
      expect(find.text('0 de 7 unidades aprobadas'), findsOneWidget);
      // La evidencia antigua de foundations-v1 es práctica con apoyo: no aprueba.
      for (final unit in foundationUnits) {
        for (var i = 0; i < unit.checks.length; i++) {
          notifier.registrarPractica(foundationKey(unit, i), {
            'correcta': true,
            'resueltaConApoyo': true,
            'conApoyo': true,
          });
        }
      }
      await render();
      expect(find.text('0 de 7 unidades aprobadas'), findsOneWidget);
      // Aprobar la evaluación de la primera unidad sí avanza la ruta.
      final primera = ruta.unidades.first;
      notifier.registrarPractica(
        ClaveRuta.evaluacion(primera.id),
        resumenEvaluacion(primera, 5, 5, null, DateTime.now()),
      );
      await render();
      expect(find.text('Continuar: El alfabeto'), findsOneWidget);
      expect(find.text('1 de 7 unidades aprobadas'), findsOneWidget);
      expect(find.text('Gramática'), findsOneWidget);
      expect(tester.takeException(), isNull);
    },
    timeout: const Timeout(Duration(seconds: 45)),
  );
}
