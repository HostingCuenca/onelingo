import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/avatar/tutores_3d.dart';
import 'package:onelingo/features/plans/tutors_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  test('Recomendados primero según el idioma', () {
    expect(tutores3dPara('en').take(3).map((t) => t.id), [
      'amara',
      'sofia',
      'clara',
    ]);
    expect(tutores3dPara('ja').first.id, 'kenji');
    expect(tutores3d.length, 10);
  });

  testWidgets('Tutores con IA: videollamada 3D y chat en una sola pantalla', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(390, 2400);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();
    await tester.pumpWidget(
      ProviderScope(
        overrides: [prefsProvider.overrideWithValue(prefs)],
        child: MaterialApp(theme: buildTheme(), home: const TutorsScreen()),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('Tutores con IA'), findsOneWidget);
    expect(find.text('Videollamada con un tutor'), findsOneWidget);
    expect(find.text('Chat de voz y texto'), findsOneWidget);
    for (final t in tutores3d) {
      expect(find.text(t.nombre), findsWidgets, reason: t.id);
    }
    expect(find.text('Recomendado'), findsNWidgets(3));
    expect(find.text('Hablar con mi tutor'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
