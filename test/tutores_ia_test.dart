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
    expect(tutor3d('lumo')?.nombre, 'Lumo');
    expect(lumoTutor.retrato, 'assets/img/tutores/lumo.webp');
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
    // Los tutores 3D de MakeHuman están ocultos por ahora.
    // (Sofía y otros nombres también son tutores del chat: se miran los únicos.)
    for (final n in ['Amara', 'Owen', 'Malik', 'Kenji', 'Mei']) {
      expect(find.text(n), findsNothing, reason: n);
    }
    expect(find.text('Recomendado'), findsNothing);
    // Lumo que habla, destacado.
    expect(find.text('Habla con Lumo'), findsOneWidget);
    expect(find.bySemanticsLabel('Videollamada con Lumo'), findsOneWidget);
    // Tutores en vivo: 6 × 2, ellas arriba y ellos abajo, antes de Lumo.
    expect(tutorasVivo.map((t) => t.id), [
      'ana',
      'elena',
      'julia',
      'chloe',
      'nora',
      'hana',
    ]);
    expect(tutoresVivoHombres.map((t) => t.id), [
      'lucas',
      'tomas',
      'frank',
      'diego',
      'erik',
      'andre',
    ]);
    final y = [
      for (final t in tutoresVivo)
        tester
            .getTopLeft(find.bySemanticsLabel(RegExp('^${t.nombre}')).first)
            .dy,
    ];
    expect(y.take(6).toSet().length, 1);
    expect(y.skip(6).toSet().length, 1);
    expect(y[0], lessThan(y[6]));
    expect(y[6], lessThan(tester.getTopLeft(find.text('Habla con Lumo')).dy));
    for (final t in tutoresVivo) {
      expect(t.rasgo, isNotEmpty, reason: t.id);
      expect(t.especialidad, isNotEmpty, reason: t.id);
    }
    // El especialista del idioma que se estudia (inglés: Frank) viene elegido
    // y marcado; al tocar otra cara se ve su ficha y el botón para llamarla.
    expect(find.text('Especialista en inglés'), findsOneWidget);
    expect(find.text('Videollamada con Frank'), findsOneWidget);
    for (final l in [
      'en',
      'es',
      'fr',
      'de',
      'pt',
      'it',
      'ru',
      'ko',
      'ja',
      'zh',
    ]) {
      expect(
        tutoresVivo.where((t) => t.idiomaEspecial == l),
        isNotEmpty,
        reason: l,
      );
    }
    await tester.tap(find.bySemanticsLabel(RegExp('^Erik')).first);
    await tester.pumpAndSettle();
    expect(find.text('Relajado y curioso'), findsOneWidget);
    expect(find.text('Conoce de primera mano el japonés.'), findsOneWidget);
    expect(find.text('Videollamada con Erik'), findsOneWidget);
    expect(find.text('Habla con Lumo'), findsOneWidget);
    expect(find.text('Más tutores'), findsOneWidget);
    // Los tutores 3D de MakeHuman están ocultos por ahora.
    expect(find.text(tutores3dPara('en').first.nombre), findsNothing);
    expect(find.text('Hablar con mi tutor'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
