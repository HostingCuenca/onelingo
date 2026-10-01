import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/core/content/catalog.dart';
import 'package:onelingo/core/content/situaciones.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/situations/prueba_situacion_screen.dart';
import 'package:onelingo/features/situations/situation_screen.dart';

/// Situaciones v2 (docs/claude-educacion/SITUACIONES_V2.md).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final contenido = situacionesDesdeJson(
    jsonDecode(File('assets/contenido/en/situaciones.json').readAsStringSync())
        as Map<String, dynamic>,
  )!;

  test('las copias generadas coinciden con la fuente única', () {
    final r = Process.runSync('python3', [
      'tools/contenido/generar_situaciones.py',
      '--comprobar',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
    final v = Process.runSync('python3', [
      'tools/contenido/validar_situaciones.py',
      'assets/contenido/en/situaciones.json',
    ]);
    expect(v.exitCode, 0, reason: '${v.stdout}');
  });

  test('50 situaciones con tres tramos completos y objetivos únicos', () {
    expect(contenido.keys.toList()..sort(), [
      for (var i = 1; i <= 50; i++) i,
    ]);
    expect(situaciones, hasLength(50));
    final ids = <String>{};
    for (final c in contenido.values) {
      for (final t in Tramo.values) {
        final x = c.tramo(t);
        expect(x.objetivos, hasLength(3));
        expect(x.vocabulario, hasLength(10));
        expect(x.frases, hasLength(4));
        for (final o in x.objetivos) {
          expect(ids.add(o.id), isTrue, reason: o.id);
          expect(c.tramoDeObjetivo(o.id), t);
        }
      }
    }
    // El básico conserva los objetivos de siempre (progreso y servidor).
    expect(contenido[1]!.tramo(Tramo.basico).objetivos.first.id, 's1-o1');
  });

  test('el tramo sale del nivel y los superiores se abren al llegar', () {
    expect(Tramo.deNivel(1), Tramo.basico);
    expect(Tramo.deNivel(3), Tramo.basico);
    expect(Tramo.deNivel(4), Tramo.intermedio);
    expect(Tramo.deNivel(7), Tramo.avanzado);
    expect(Tramo.avanzado.abiertoPara(5), isFalse);
    expect(Tramo.basico.abiertoPara(1), isTrue);
  });

  test('la prueba del tramo: 10 preguntas con una respuesta correcta', () {
    final t = contenido[1]!.tramo(Tramo.intermedio);
    final p = preguntasPruebaSituacion(t, Random(3));
    expect(p, hasLength(10));
    expect(p.where((q) => q.audio != null), hasLength(2));
    for (final q in p) {
      expect(q.correcta, inInclusiveRange(0, q.opciones.length - 1));
      expect(q.opciones.toSet(), hasLength(q.opciones.length));
    }
    expect(aciertosPruebaSituacion(10), 8);
  });

  test('completado: prueba aprobada y un objetivo practicado', () {
    final c = contenido[1]!;
    var e = estadoTramo({}, 'en', c, Tramo.basico);
    expect(e.completado, isFalse);
    expect(e.progreso, 0);
    final practicas = <String, dynamic>{
      clavePruebaSituacion('en', 1, Tramo.basico): {
        'aprobada': true,
        'aciertos': 9,
        'total': 10,
        'mejor': 9,
      },
    };
    e = estadoTramo(practicas, 'en', c, Tramo.basico);
    expect(e.completado, isFalse);
    practicas[claveObjetivoSituacion('en', 1, 's1-o1')] = {'idioma': 'en'};
    e = estadoTramo(practicas, 'en', c, Tramo.basico);
    expect(e.completado, isTrue);
    expect(e.mejorNota, (9, 10));
  });

  test('situación sugerida: retoma la última y si no, según las metas', () {
    expect(situacionSugerida({}, 'en', ['entrevistas']), 20);
    expect(
      situacionSugerida(
        {
          'a': {'idioma': 'en', 'situacionId': 1, 'fecha': '2026-01'},
          'b': {'idioma': 'en', 'situacionId': 7, 'fecha': '2026-08'},
        },
        'en',
        ['entrevistas'],
      ),
      7,
    );
    expect(
      situacionSugerida(
        {
          'a': {'idioma': 'fr', 'situacionId': 1},
        },
        'en',
        ['estudiar'],
      ),
      35,
    );
  });

  for (final size in [const Size(390, 700), const Size(430, 900)]) {
    testWidgets('la situación muestra su tramo y cabe en ${size.width}', (
      tester,
    ) async {
      tester.view.physicalSize = size;
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      SharedPreferences.setMockInitialValues({
        'onelingo.progress.v1': jsonEncode({
          'onboardingDone': true,
          'idiomaMeta': 'en',
          'nivelInicial': 5,
          'nivelEscala': 'client-10-levels-v1',
          'nivelClienteInicial': 5,
        }),
      });
      final prefs = await SharedPreferences.getInstance();
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            prefsProvider.overrideWithValue(prefs),
            situacionesProvider.overrideWith((ref, _) async => contenido),
          ],
          child: const MaterialApp(home: SituationScreen(id: 1)),
        ),
      );
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      // Nivel 5 → tramo intermedio; avanzado bloqueado.
      expect(find.text('Tu nivel'), findsOneWidget);
      final intermedio = contenido[1]!.tramo(Tramo.intermedio);
      await tester.scrollUntilVisible(
        find.text(intermedio.objetivos.first.titulo),
        200,
        scrollable: find.byType(Scrollable).first,
      );
      expect(find.text(intermedio.objetivos.first.titulo), findsOneWidget);
      expect(find.text('HACER LA PRUEBA'), findsOneWidget);
    });
  }
}
