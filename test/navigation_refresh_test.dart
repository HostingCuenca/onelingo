import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/app/router.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/providers.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/i18n/i18n.dart';
import 'package:onelingo/core/state/providers.dart';

void main() {
  for (final level in [1, 5, 9]) {
    testWidgets(
      'Nivel $level conserva tabs en gramática, fundamentos y situaciones',
      (tester) async {
        tester.view.physicalSize = const Size(390, 844);
        tester.view.devicePixelRatio = 1;
        addTearDown(tester.view.resetPhysicalSize);
        addTearDown(tester.view.resetDevicePixelRatio);
        Efectos.animaciones.value = false;
        Efectos.sonido = false;
        SharedPreferences.setMockInitialValues({
          'onelingo.progress.v1': jsonEncode({
            'onboardingDone': true,
            'nombre': 'Demo',
            'nivelInicial': level,
            'idiomaMeta': 'en',
          }),
        });
        final prefs = await SharedPreferences.getInstance();
        // La ruta de fundamentos se lee de assets fuera del reloj simulado.
        final cargador = CargadorRuta();
        await tester.runAsync(() => cargador.cargar('en'));
        final container = ProviderContainer(
          overrides: [
            prefsProvider.overrideWithValue(prefs),
            cargadorRutaProvider.overrideWithValue(cargador),
          ],
        );
        addTearDown(container.dispose);
        final router = container.read(routerProvider);
        router.go('/gramatica?nivel=$level');
        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: MaterialApp.router(
              theme: buildTheme(),
              builder: (context, child) => MediaQuery(
                data: MediaQuery.of(
                  context,
                ).copyWith(textScaler: TextScaler.linear(level == 9 ? 2 : 1)),
                child: child!,
              ),
              routerConfig: router,
            ),
          ),
        );
        await tester.pumpAndSettle();
        expect(find.byType(NavigationBar), findsOneWidget);
        expect(
          tester
              .widget<NavigationBar>(find.byType(NavigationBar))
              .selectedIndex,
          1,
        );
        expect(tester.takeException(), isNull);
        router.go('/fundamentos');
        await tester.pump();
        await tester.runAsync(
          () => Future<void>.delayed(const Duration(milliseconds: 50)),
        );
        await tester.pumpAndSettle();
        expect(find.byType(NavigationBar), findsOneWidget);
        router.go('/practicar');
        await tester.pumpAndSettle();
        expect(find.byType(NavigationBar), findsOneWidget);
        expect(
          tester
              .widget<NavigationBar>(find.byType(NavigationBar))
              .selectedIndex,
          2,
        );
        expect(tester.takeException(), isNull);
        await tester.pumpWidget(const SizedBox());
        await tester.pumpAndSettle();
      },
    );
  }

  testWidgets(
    'al cambiar el idioma de la app, el menú y la portada se traducen al momento',
    (tester) async {
      tester.view.physicalSize = const Size(390, 844);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      addTearDown(() => I18n.idioma.value = 'es');
      Efectos.animaciones.value = false;
      Efectos.sonido = false;
      I18n.usar('en', {
        'Inicio': 'Home',
        'Aprender': 'Learn',
        'Practicar': 'Practice',
        'Perfil': 'Profile',
        'OneLingo. Un mundo, más oportunidades.':
            'OneLingo. One world, more opportunities.',
      });
      SharedPreferences.setMockInitialValues({
        'onelingo.progress.v1': jsonEncode({
          'onboardingDone': true,
          'nombre': 'Demo',
          'idiomaMeta': 'en',
          'idiomaInterfaz': 'es',
        }),
      });
      final prefs = await SharedPreferences.getInstance();
      final container = ProviderContainer(
        overrides: [prefsProvider.overrideWithValue(prefs)],
      );
      addTearDown(container.dispose);
      final router = container.read(routerProvider);
      Finder etiquetaSemantica(String texto) => find.byWidgetPredicate(
        (w) => w is Semantics && w.properties.label == texto,
      );
      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          // Como OneLingoApp: el idioma de `tr()` sale del progreso.
          child: Consumer(
            builder: (context, ref, _) {
              I18n.idioma.value = ref.watch(
                progressProvider.select((s) => s.interfaz),
              );
              return MaterialApp.router(
                theme: buildTheme(),
                // La fuente de las pruebas es más ancha: sin desbordes ajenos.
                builder: (context, child) => MediaQuery(
                  data: MediaQuery.of(context)
                      .copyWith(textScaler: const TextScaler.linear(.7)),
                  child: child!,
                ),
                routerConfig: router,
              );
            },
          ),
        ),
      );
      await tester.pumpAndSettle();
      expect(find.text('Inicio'), findsOneWidget);
      expect(
        etiquetaSemantica('OneLingo. Un mundo, más oportunidades.'),
        findsOneWidget,
      );
      container.read(progressProvider.notifier).elegirIdiomaInterfaz('en');
      await tester.pumpAndSettle();
      for (final etiqueta in ['Home', 'Learn', 'Practice', 'Profile']) {
        expect(find.text(etiqueta), findsOneWidget);
      }
      expect(find.text('Inicio'), findsNothing);
      expect(
        etiquetaSemantica('OneLingo. One world, more opportunities.'),
        findsOneWidget,
      );
      expect(tester.takeException(), isNull);
      await tester.pumpWidget(const SizedBox());
      await tester.pumpAndSettle();
    },
  );
}
