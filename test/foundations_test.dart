import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/content/foundations.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/foundations/foundations_screen.dart';

void main() {
  for (final scale in [1.0, 2.0]) {
    testWidgets(
      'Desde cero: enseñanza, error, ayuda, secuencia y persistencia x$scale',
      (tester) async {
        tester.view.physicalSize = const Size(390, 844);
        tester.view.devicePixelRatio = 1;
        addTearDown(tester.view.resetPhysicalSize);
        addTearDown(tester.view.resetDevicePixelRatio);
        SharedPreferences.setMockInitialValues({});
        final prefs = await SharedPreferences.getInstance();
        final container = ProviderContainer(
          overrides: [prefsProvider.overrideWithValue(prefs)],
        );
        addTearDown(container.dispose);
        final initialLevel = container.read(progressProvider).nivelInicial;
        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: MaterialApp(
              theme: buildTheme(),
              builder: (context, child) => MediaQuery(
                data: MediaQuery.of(context)
                    .copyWith(textScaler: TextScaler.linear(scale)),
                child: child!,
              ),
              home: const FoundationsScreen(),
            ),
          ),
        );
        await tester.pumpAndSettle();
        Future<void> tap(String text) async {
          final finder = find.text(text);
          await tester.scrollUntilVisible(
            finder,
            180,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 60,
          );
          await tester.pumpAndSettle();
          await tester.ensureVisible(finder);
          await tester.pumpAndSettle();
          await tester.tap(finder);
          await tester.pumpAndSettle();
          expect(tester.takeException(), isNull);
        }

        expect(
          foundationAvailable(
            foundationUnits[1],
            container.read(progressProvider).practicas,
          ),
          isFalse,
        );
        await tap('1. Yo y tú');
        await tester.scrollUntilVisible(
          find.text('I'),
          180,
          scrollable: find.byType(Scrollable).first,
        );
        await tester.pumpAndSettle();
        expect(find.text('I'), findsOneWidget);
        expect(find.text('yo'), findsOneWidget);
        expect(find.text('COMPROBAR'), findsNothing);
        expect(container.read(progressProvider).practicas, isEmpty);
        for (var index = 0; index < foundationUnits.length; index++) {
          final unit = foundationUnits[index];
          for (var c = 1; c < unit.cards.length; c++) {
            await tap('SIGUIENTE EJEMPLO');
          }
          await tap('PRACTICAR CON AYUDA');
          for (var q = 0; q < unit.checks.length; q++) {
            final check = unit.checks[q];
            if (index == 0 && q == 0) {
              await tap('you');
              await tap('COMPROBAR');
              expect(find.text('Vamos a repasarlo:'), findsOneWidget);
              expect(
                container.read(progressProvider).practicas[foundationKey(
                  unit,
                  q,
                )]['primeraCorrecta'],
                isFalse,
              );
              await tap('INTENTAR CON ESTA AYUDA');
            }
            if (check.order) {
              for (final token in check.answer.split(' ')) {
                await tap(token);
              }
            } else {
              await tap(check.answer);
            }
            await tap('COMPROBAR');
            expect(find.text('¡Bien! Mira por qué:'), findsOneWidget);
            await tap('CONTINUAR');
          }
          expect(
            foundationPracticed(
              unit,
              container.read(progressProvider).practicas,
            ),
            isTrue,
          );
          if (index < foundationUnits.length - 1) {
            await tap('SIGUIENTE PASO');
          }
        }
        expect(container.read(progressProvider).nivelInicial, initialLevel);
        expect(container.read(progressProvider).practicas.length, 12);
        final xp = container.read(progressProvider).xp;
        await tap('VER MI RECORRIDO');
        await tap('1. Yo y tú');
        await tap('SIGUIENTE EJEMPLO');
        await tap('PRACTICAR CON AYUDA');
        await tap('you');
        await tap('COMPROBAR');
        expect(container.read(progressProvider).xp, xp);
        expect(
          foundationPracticed(
            foundationUnits.first,
            container.read(progressProvider).practicas,
          ),
          isTrue,
        );
        expect(
          container.read(progressProvider).practicas[foundationKey(
            foundationUnits.first,
            0,
          )]['primeraCorrecta'],
          isFalse,
        );
        await tester.pumpWidget(const SizedBox());
        await tester.pumpAndSettle();
        final restored = ProviderContainer(
          overrides: [prefsProvider.overrideWithValue(prefs)],
        );
        addTearDown(restored.dispose);
        expect(
          foundationPracticed(
            foundationUnits.last,
            restored.read(progressProvider).practicas,
          ),
          isTrue,
        );
      },
    );
  }
}
