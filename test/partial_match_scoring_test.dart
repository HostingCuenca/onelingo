import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/features/ruta/item_view.dart';

void main() {
  testWidgets('relacionar muestra la fuente editorial antes de emparejar', (
    tester,
  ) async {
    const source =
        'Meeting note: Iris prepares the room by Wednesday; Jon uploads notes by Friday.';
    const item = Item(
      id: 'en.n3.c63.e04',
      formato: FormatoItem.relacionar,
      consigna: TextoApoyo({'es': 'Relaciona tarea, responsable y plazo.'}),
      feedback: TextoApoyo({'es': 'Las asociaciones salen de la nota.'}),
      texto: source,
      pares: [
        ('prepare the room', TextoApoyo({'es': 'Iris — Wednesday'})),
        ('upload notes', TextoApoyo({'es': 'Jon — Friday'})),
      ],
    );

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: ItemView(
            item: item,
            idioma: 'en',
            cadena: ['es'],
            guiada: false,
            permitirReintento: false,
            onComprobado: _noopResult,
            onContinuar: _noop,
          ),
        ),
      ),
    );

    expect(find.text(source), findsOneWidget);
    expect(find.text('prepare the room'), findsOneWidget);
  });

  testWidgets('relacionar aplica el umbral editorial de aciertos', (
    tester,
  ) async {
    bool? result;
    const item = Item(
      id: 'en.n3.c32.e04',
      formato: FormatoItem.relacionar,
      consigna: TextoApoyo({'es': 'Relaciona las decisiones.'}),
      feedback: TextoApoyo({'es': 'Cinco de seis decisiones son suficientes.'}),
      pares: [
        ('want', TextoApoyo({'es': 'to save'})),
        ('need', TextoApoyo({'es': 'to call'})),
      ],
      partesPuntuables: 2,
      minimoCorrectas: 1,
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: ItemView(
            item: item,
            idioma: 'en',
            cadena: const ['es'],
            guiada: false,
            permitirReintento: false,
            onComprobado: (ok, _) => result = ok,
            onContinuar: () {},
          ),
        ),
      ),
    );

    await tester.tap(find.text('want'));
    await tester.tap(find.text('to call'));
    await tester.pump();
    await tester.tap(find.text('want'));
    await tester.tap(find.text('to save'));
    await tester.pump();
    await tester.tap(find.text('need'));
    await tester.tap(find.text('to call'));
    await tester.pumpAndSettle();

    expect(result, isTrue);
    expect(find.text('¡Correcto!'), findsOneWidget);
  });
}

void _noopResult(bool _, String answer) {}

void _noop() {}
