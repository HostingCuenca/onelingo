import 'dart:convert';

import 'package:onelingo/app/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/core/api/sync.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/onboarding/onboarding_screen.dart';

void main() {
  testWidgets(
    'borrador de registro reanuda y muestra los diez idiomas en pantalla móvil',
    (tester) async {
      tester.view.physicalSize = const Size(390, 740);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      SharedPreferences.setMockInitialValues({
        'onelingo.api.token': 'test',
        'onelingo.api.email': 'test@example.com',
        'onelingo.onboarding.draft.v2': jsonEncode({
          'correo': 'test@example.com',
          'nombre': 'Test',
          'nativo': 'es',
          'meta': 'en',
          'sectores': ['estudiante'],
          'objetivos': ['estudiar'],
          'nivel': 6,
          'paso': 1,
        }),
      });
      final prefs = await SharedPreferences.getInstance();
      Sync.instancia.inicializar(prefs);
      await tester.pumpWidget(
        ProviderScope(
          overrides: [prefsProvider.overrideWithValue(prefs)],
          child: MaterialApp(
            theme: buildTheme(),
            home: const OnboardingScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();
      expect(find.text('Paso 2 de 7'), findsOneWidget);
      for (final idioma in [
        'Inglés',
        'Español',
        'Francés',
        'Alemán',
        'Portugués',
        'Italiano',
        'Chino mandarín',
        'Japonés',
        'Coreano',
        'Ruso',
      ]) {
        // .first: «Español» también está en el selector de idioma de la app.
        final rect = tester.getRect(find.text(idioma).first);
        expect(rect.top, greaterThan(0));
        expect(
          rect.bottom,
          lessThan(670),
          reason: '$idioma debe verse sin scroll',
        );
      }
      expect(tester.takeException(), isNull);
      await Sync.instancia.cerrarSesion();
    },
  );
}
