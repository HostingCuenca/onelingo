import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/voz.dart';
import 'package:onelingo/shared/widgets/onda_voz.dart';

void main() {
  tearDown(() {
    Oido.instancia.nivel.value = 0;
    Oido.instancia.procesando.value = false;
  });

  testWidgets('las barras siguen el nivel y luego avisa que transcribe', (
    t,
  ) async {
    await t.pumpWidget(const MaterialApp(home: Scaffold(body: OndaVoz())));
    double alto() => t
        .widgetList<AnimatedContainer>(find.byType(AnimatedContainer))
        .map((c) => c.constraints!.maxHeight)
        .reduce((a, b) => a > b ? a : b);
    final quieto = alto();
    Oido.instancia.nivel.value = 1;
    await t.pumpAndSettle();
    expect(alto(), greaterThan(quieto * 3));

    Oido.instancia.procesando.value = true;
    await t.pump();
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
    expect(find.text('Transcribiendo tu respuesta…'), findsOneWidget);
  });
}
