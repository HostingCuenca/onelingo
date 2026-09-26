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
}
