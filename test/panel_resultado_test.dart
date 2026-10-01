import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/shared/widgets/feedback_experience.dart';
import 'package:onelingo/shared/widgets/lumo.dart';

void main() {
  Future<String?> abrir(
    WidgetTester tester,
    bool correcto, {
    bool conLumo = true,
  }) async {
    Efectos.sonido = false;
    addTearDown(() => Efectos.sonido = true);
    String? resultado;
    await tester.pumpWidget(
      MaterialApp(
        home: Builder(
          builder: (context) => Scaffold(
            body: Center(
              child: TextButton(
                onPressed: () async => resultado = await mostrarPanelResultado(
                  context,
                  correcto: correcto,
                  titulo: correcto ? '¡Correcto!' : 'Vamos a repasarlo',
                  cuerpo: const Text('Explicación'),
                  reintentar: !correcto,
                  lumo: conLumo,
                ),
                child: const Text('abrir'),
              ),
            ),
          ),
        ),
      ),
    );
    await tester.tap(find.text('abrir'));
    await tester.pumpAndSettle();
    return resultado;
  }

  Finder lumo(PoseLumo pose) =>
      find.byWidgetPredicate((w) => w is LumoReaccion && w.pose == pose);

  testWidgets('Acierto: Lumo feliz y SIGUIENTE continúa', (tester) async {
    await abrir(tester, true);
    expect(find.text('¡Correcto!'), findsOneWidget);
    expect(
      lumo(PoseLumo.celebra).evaluate().length +
          lumo(PoseLumo.anima).evaluate().length,
      1,
    );
    expect(find.text('Intentar otra vez ahora'), findsNothing);
    await tester.tap(find.text('SIGUIENTE'));
    await tester.pumpAndSettle();
    expect(find.text('¡Correcto!'), findsNothing);
  });

  testWidgets('Error: Lumo triste, explicación y reintento', (tester) async {
    await abrir(tester, false);
    expect(find.text('Vamos a repasarlo'), findsOneWidget);
    expect(lumo(PoseLumo.errorAmable), findsOneWidget);
    expect(find.text('Explicación'), findsOneWidget);
    expect(find.text('Intentar otra vez ahora'), findsOneWidget);
  });

  testWidgets('Prueba de nivel: panel sin Lumo', (tester) async {
    await abrir(tester, true, conLumo: false);
    expect(find.text('¡Correcto!'), findsOneWidget);
    expect(find.byType(LumoReaccion), findsNothing);
  });

  test('Las poses alternan al acertar', () {
    final a = PoseLumo.acierto(), b = PoseLumo.acierto();
    expect({a, b}, {PoseLumo.celebra, PoseLumo.anima});
  });
}
