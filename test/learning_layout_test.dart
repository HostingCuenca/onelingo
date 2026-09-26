import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
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
    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();
    Efectos.animaciones.value = false;
    final container = ProviderContainer(
      overrides: [prefsProvider.overrideWithValue(prefs)],
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
      final evidence = <String, dynamic>{};
      Future<void> render() => tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: SingleChildScrollView(
              child: LearningPath(
                nivel: 1,
                recommended: 'gramatica',
                practices: Map.of(evidence),
              ),
            ),
          ),
        ),
      );
      await render();
      expect(find.text('Empieza desde cero'), findsOneWidget);
      expect(find.text('0 de 6 pasos practicados con apoyo'), findsOneWidget);
      final first = foundationUnits.first;
      evidence[foundationKey(first, 0)] = {
        'correcta': true,
        'resueltaConApoyo': true,
      };
      await render();
      expect(find.text('0 de 6 pasos practicados con apoyo'), findsOneWidget);
      for (var i = 0; i < first.checks.length; i++) {
        evidence[foundationKey(first, i)] = {'resueltaConApoyo': true};
      }
      await render();
      expect(find.text('Continuar: Digo mi nombre'), findsOneWidget);
      expect(find.text('1 de 6 pasos practicados con apoyo'), findsOneWidget);
      for (final unit in foundationUnits) {
        for (var i = 0; i < unit.checks.length; i++) {
          evidence[foundationKey(unit, i)] = {'resueltaConApoyo': true};
        }
      }
      await render();
      expect(find.text('Repasa tus primeros pasos'), findsOneWidget);
      expect(find.text('6 de 6 pasos practicados con apoyo'), findsOneWidget);
      expect(find.text('Gramática'), findsOneWidget);
      expect(find.byType(InkWell), findsNWidgets(6));
      expect(tester.takeException(), isNull);
    },
  );
}
