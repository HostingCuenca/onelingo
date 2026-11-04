import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/aprendizaje/providers.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/progress/certificado_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late RutaCargada ruta;
  setUpAll(() async {
    ruta = (await CargadorRuta().cargar('en'))!;
  });

  test('solo los niveles 1 a 10 llevan certificado; fecha legible', () {
    expect(['n1', 'n7', 'n10'].every(conCertificado), isTrue);
    expect(['f0', 'n0', 'n11', 'c2'].any(conCertificado), isFalse);
    expect(
      fechaCertificado(DateTime(2026, 10, 22), 'es'),
      '22 de octubre de 2026',
    );
    expect(fechaCertificado(DateTime(2026, 10, 22), 'en'), 'October 22, 2026');
  });

  Future<void> abrir(WidgetTester tester, ProgressState s, String nivel) async {
    SharedPreferences.setMockInitialValues({
      'onelingo.progress.v1': jsonEncode(s.toJson()),
    });
    final prefs = await SharedPreferences.getInstance();
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          prefsProvider.overrideWithValue(prefs),
          rutaProvider.overrideWith((ref, idioma) async => ruta),
        ],
        child: MaterialApp(
          theme: buildTheme(),
          home: CertificadoScreen(nivel: nivel),
        ),
      ),
    );
    await tester.pump();
    await tester.pump();
  }

  testWidgets('con el nivel superado se ve su certificado con el nombre', (
    tester,
  ) async {
    final s = ProgressState(
      onboardingDone: true,
      nombre: 'Ana Pérez',
      idiomaMeta: 'en',
      practicas: {
        ClaveRuta.pruebaNivel('en', 'n3'): {
          'aprobada': true,
          'aprobadaEn': '2026-10-22T15:00:00',
        },
      },
    );
    await abrir(tester, s, 'n3');
    expect(find.text('Ana Pérez'), findsOneWidget);
    expect(find.text('N3'), findsOneWidget);
    expect(
      find.text(
        'por aprobar la prueba del Nivel 3 del curso de inglés de OneLingo.',
      ),
      findsOneWidget,
    );
    expect(find.text('22 de octubre de 2026'), findsOneWidget);
    // Sin sesión no hay enlace ni PDF, pero sí el aviso para conseguirlos.
    expect(find.text('DESCARGAR PDF'), findsNothing);
    expect(
      find.text(
        'Inicia sesión para obtener el enlace y el PDF de tu certificado.',
      ),
      findsOneWidget,
    );
  });

  testWidgets('sin superar el nivel no hay certificado', (tester) async {
    await abrir(
      tester,
      const ProgressState(onboardingDone: true, idiomaMeta: 'en'),
      'n4',
    );
    expect(
      find.text('Supera este nivel para recibir su certificado.'),
      findsOneWidget,
    );
    expect(find.text('N4'), findsNothing);
  });
}
