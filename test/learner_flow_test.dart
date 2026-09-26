import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/library/grammar_screen.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  for (final scale in [1.0, 2.0]) {
    testWidgets(
      'Alumno falla, revisa regla y conserva respuesta, texto x$scale',
      (tester) async {
        tester.view.physicalSize = const Size(390, 844);
        tester.view.devicePixelRatio = 1;
        addTearDown(tester.view.resetPhysicalSize);
        addTearDown(tester.view.resetDevicePixelRatio);
        SharedPreferences.setMockInitialValues({});
        final prefs = await SharedPreferences.getInstance();
        Efectos.sonido = false;
        Efectos.vibraciones.value = false;
        final container = ProviderContainer(
          overrides: [prefsProvider.overrideWithValue(prefs)],
        );
        addTearDown(container.dispose);
        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: MaterialApp(
              theme: buildTheme(),
              builder: (context, child) => MediaQuery(
                data: MediaQuery.of(context).copyWith(
                  textScaler: TextScaler.linear(scale),
                  disableAnimations: true,
                ),
                child: child!,
              ),
              home: const GrammarScreen(nivel: 1),
            ),
          ),
        );
        await tester.pumpAndSettle();
        // All content is in one ListView. Scroll until the target is built.
        Future<void> reveal(Finder finder, {double delta = 180}) async {
          tester
              .state<ScrollableState>(find.byType(Scrollable).first)
              .position
              .jumpTo(0);
          await tester.pumpAndSettle();
          await tester.scrollUntilVisible(
            finder,
            delta.abs(),
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 80,
          );
          await tester.pumpAndSettle();
        }

        await reveal(find.text('La idea clave'));
        expect(find.textContaining('Usa I am;'), findsOneWidget);
        await reveal(find.text('AHORA ME TOCA A MÍ'));
        await tester.tap(find.text('AHORA ME TOCA A MÍ'));
        await tester.pumpAndSettle();
        await reveal(find.byKey(const ValueKey('production-be')));
        await tester.enterText(
          find.byKey(const ValueKey('production-be')),
          'I am Ana. I am happy.',
        );
        expect(container.read(progressProvider).xp, 0);
        await reveal(find.text('COMPROBAR CON EJEMPLOS'));
        await tester.tap(find.text('COMPROBAR CON EJEMPLOS'));
        await tester.pumpAndSettle();
        await reveal(find.text('am'));
        await tester.tap(
          find.text('am'),
        ); // My name am Leo is deliberately wrong.
        await tester.pump();
        await reveal(find.text('COMPROBAR'));
        await tester.tap(find.text('COMPROBAR'));
        await tester.pumpAndSettle();
        await reveal(find.text('Vamos a entenderlo'));
        expect(find.text('Respuesta: is'), findsOneWidget);
        expect(
          container
              .read(progressProvider)
              .practicas['grammar-guide-be-0']['correcta'],
          false,
        );
        expect(find.text('Are you tired?'), findsNothing);
        await reveal(find.text('SIGUIENTE PREGUNTA'));
        await tester.tap(find.text('SIGUIENTE PREGUNTA'));
        await tester.pumpAndSettle();
        await reveal(find.text('Pregunta 2 de 2'));
        expect(find.text('Pregunta 2 de 2'), findsOneWidget);
        expect(find.text('Respuesta: is'), findsNothing);
        await reveal(find.text('Revisar pregunta anterior'));
        await tester.tap(find.text('Revisar pregunta anterior'));
        await tester.pumpAndSettle();
        final xp = container.read(progressProvider).xp;
        await reveal(find.text('VOLVER A LA EXPLICACIÓN'));
        await tester.tap(find.text('VOLVER A LA EXPLICACIÓN'));
        await tester.pumpAndSettle();
        await reveal(find.text('La idea clave'), delta: -180);
        expect(find.textContaining('Usa I am;'), findsOneWidget);
        await reveal(find.text('AHORA ME TOCA A MÍ'));
        await tester.tap(find.text('AHORA ME TOCA A MÍ'));
        await tester.pumpAndSettle();
        await reveal(find.byKey(const ValueKey('production-be')));
        expect(find.text('I am Ana. I am happy.'), findsOneWidget);
        await reveal(find.text('COMPROBAR CON EJEMPLOS'));
        await tester.tap(find.text('COMPROBAR CON EJEMPLOS'));
        await tester.pumpAndSettle();
        await reveal(find.text('Vamos a entenderlo'), delta: -180);
        expect(find.text('Respuesta: is'), findsOneWidget);
        expect(container.read(progressProvider).xp, xp);
        expect(
          container
              .read(progressProvider)
              .practicas['grammar-guide-be-0']['intentos'],
          1,
        );
        // A supported retry preserves the first mistake and grants no extra XP.
        await reveal(find.text('INTENTAR OTRA VEZ'));
        await tester.tap(find.text('INTENTAR OTRA VEZ'));
        await tester.pumpAndSettle();
        await reveal(find.text('is'), delta: -180);
        await tester.tap(find.text('is'));
        await reveal(find.text('COMPROBAR'));
        await tester.tap(find.text('COMPROBAR'));
        await tester.pumpAndSettle();
        final retry = container
            .read(progressProvider)
            .practicas['grammar-guide-be-0'];
        expect(retry['correcta'], true);
        expect(retry['primeraCorrecta'], false);
        expect(retry['intentos'], 2);
        expect(container.read(progressProvider).xp, xp);
        await reveal(find.text('Temario'), delta: -180);
        await tester.tap(find.text('Temario'));
        await tester.pumpAndSettle();
        expect(find.text('Elige tu próximo tema'), findsOneWidget);
        expect(find.text('Nivel 10'), findsNothing);
        final selector = find.byType(DropdownButtonFormField<int>);
        await tester.tap(selector);
        await tester.pumpAndSettle();
        await tester.tap(find.text('Nivel 2').last);
        await tester.pumpAndSettle();
        await tester.tap(find.text('Pronombres: a quién y de quién'));
        await tester.pumpAndSettle();
        expect(find.text('Nivel 2 · Tema 1 de 6'), findsOneWidget);
        expect(find.text('Pronombres: a quién y de quién'), findsOneWidget);
        expect(find.text('Pregunta 1 de 2'), findsNothing);
        expect(tester.takeException(), isNull);
        await tester.pumpWidget(const SizedBox.shrink());
        await tester.pumpAndSettle();
      },
    );
  }
}
