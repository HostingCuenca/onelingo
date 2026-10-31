import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/features/avatar/puerta_microfono.dart';

void main() {
  Future<void> montar(WidgetTester tester, List<bool> respuestas) async {
    var pedidas = 0;
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          permisoMicrofonoProvider.overrideWithValue(
            ({pedir = true}) async =>
                respuestas[(pedidas++).clamp(0, respuestas.length - 1)],
          ),
        ],
        child: MaterialApp(
          theme: buildTheme(),
          home: const PuertaMicrofono(child: Text('Tutor abierto')),
        ),
      ),
    );
    await tester.pumpAndSettle();
  }

  testWidgets('Con permiso del micrófono se entra al tutor', (tester) async {
    await montar(tester, [true]);
    expect(find.text('Tutor abierto'), findsOneWidget);
    expect(find.text('Necesitamos tu micrófono'), findsNothing);
  });

  testWidgets(
    'Sin permiso no se entra; «Permitir micrófono» lo pide otra vez',
    (tester) async {
      await montar(tester, [false, true]);
      expect(find.text('Tutor abierto'), findsNothing);
      expect(find.text('Necesitamos tu micrófono'), findsOneWidget);
      await tester.tap(find.text('Permitir micrófono'));
      await tester.pumpAndSettle();
      expect(find.text('Tutor abierto'), findsOneWidget);
    },
  );

  testWidgets('Al volver de Ajustes se comprueba de nuevo', (tester) async {
    await montar(tester, [false, true]);
    expect(find.text('Tutor abierto'), findsNothing);
    tester.binding.handleAppLifecycleStateChanged(AppLifecycleState.paused);
    tester.binding.handleAppLifecycleStateChanged(AppLifecycleState.resumed);
    await tester.pumpAndSettle();
    expect(find.text('Tutor abierto'), findsOneWidget);
  });
}
