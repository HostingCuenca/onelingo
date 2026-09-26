import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/core/content/situation_units.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/situations/situation_screen.dart';
import 'package:onelingo/features/plans/tutors_screen.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final units = (jsonDecode(
    File('assets/contenido/en/situaciones.json').readAsStringSync(),
  ) as List).map((e) => SituationUnit.fromJson(e)).toList();
  test('recommendation resumes evidence and respects goals', () {
    expect(suggestedSituation({}, ['entrevistas']), 20);
    expect(
      suggestedSituation(
        {
          'a': {'idioma': 'en', 'situacionId': 1, 'fecha': '2026-01'},
          'b': {'idioma': 'en', 'situacionId': 7, 'fecha': '2026-08'},
        },
        ['entrevistas'],
      ),
      7,
    );
    expect(
      suggestedSituation(
        {
          'a': {'idioma': 'fr', 'situacionId': 1},
        },
        ['estudiar'],
      ),
      35,
    );
  });
  test(
    'conversation memory survives reload without granting XP or completion',
    () async {
      SharedPreferences.setMockInitialValues({});
      final prefs = await SharedPreferences.getInstance();
      final progress = ProgressNotifier(prefs);
      for (var i = 0; i < 10; i++) {
        progress.guardarTurnoSituacion(1, 's1-o2', {
          'feedback': 'Correction $i',
          'asistida': true,
        });
      }
      final restored = ProgressNotifier(prefs).state;
      final evidence = restored.practicas['situacion-en-1-s1-o2'] as Map;
      expect(evidence['feedback'], 'Correction 9');
      expect((evidence['historial'] as List).length, 5);
      expect(restored.xp, 0);
      expect(restored.completadas, isEmpty);
      progress.dispose();
    },
  );
  for (final size in [const Size(390, 640), const Size(430, 900)]) {
    testWidgets('four sections and tutor portraits fit ${size.width}', (
      tester,
    ) async {
      tester.view.physicalSize = size;
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      SharedPreferences.setMockInitialValues({});
      final prefs = await SharedPreferences.getInstance();
      await tester.pumpWidget(
        ProviderScope(
          key: UniqueKey(),
          overrides: [
            prefsProvider.overrideWithValue(prefs),
            situationUnitsProvider.overrideWith((ref) async => units),
          ],
          child: const MaterialApp(home: SituationScreen(id: 1)),
        ),
      );
      await tester.pumpAndSettle();
      await tester.scrollUntilVisible(
        find.text('Vocabulario'),
        200,
        scrollable: find.byType(Scrollable).first,
      );
      for (final title in ['Vocabulario', 'Aprender', 'Practicar', 'Pruebas'])
        expect(find.text(title), findsOneWidget);
      expect(tester.takeException(), isNull);
      await tester.pumpWidget(
        ProviderScope(
          key: UniqueKey(),
          overrides: [prefsProvider.overrideWithValue(prefs)],
          child: const MaterialApp(home: TutorsScreen()),
        ),
      );
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      expect(find.text('Mia'), findsOneWidget);
    });
  }
}
