import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/shared/widgets/widgets.dart';

void main() {
  testWidgets('toda la tarjeta de audio responde y se hunde al presionarla', (
    tester,
  ) async {
    var reproducciones = 0;

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Center(
            child: SizedBox(
              width: 280,
              child: Tarjeta(
                key: const Key('audio-card'),
                etiquetaSemantica: 'Escuchar hello',
                onTap: () => reproducciones++,
                child: const Row(
                  children: [
                    Expanded(child: Text('hello')),
                    Icon(Icons.volume_up_outlined),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );

    final card = find.byKey(const Key('audio-card'));
    final gesture = await tester.startGesture(tester.getCenter(card));
    await tester.pump();

    final scale = tester.widget<AnimatedScale>(
      find.descendant(of: card, matching: find.byType(AnimatedScale)),
    );
    expect(scale.scale, 0.98);

    await gesture.up();
    await tester.pumpAndSettle();
    expect(reproducciones, 1);

    await tester.tap(find.text('hello'));
    await tester.pumpAndSettle();
    expect(reproducciones, 2);

    final semantics = tester.getSemantics(card);
    expect(semantics.label, contains('Escuchar hello'));
    expect(semantics.flagsCollection.isButton, isTrue);
  });
}
