import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/features/ruta/item_view.dart';

void main() {
  testWidgets('completar multiparte aplica umbral y conserva la fuente', (
    tester,
  ) async {
    bool? result;
    const item = Item(
      id: 'en.n3.c07.e04',
      formato: FormatoItem.completar,
      consigna: TextoApoyo({'es': 'Completa las dos decisiones.'}),
      feedback: TextoApoyo({'es': 'Se evalúa cada decisión por separado.'}),
      texto: 'Informe breve del incidente.',
      respuesta: 'was walking / started | were waiting / arrived',
      aceptadas: ['was walking / started | were waiting / arrived'],
      textosPartes: [
        'I ___ home when the rain ___.',
        'They ___ outside when the bus ___.',
      ],
      respuestasPartes: [
        ['was walking / started'],
        ['were waiting / arrived'],
      ],
      partesPuntuables: 2,
      minimoCorrectas: 1,
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SingleChildScrollView(
            child: ItemView(
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
      ),
    );

    expect(find.text('Informe breve del incidente.'), findsOneWidget);
    expect(find.byType(TextField), findsNWidgets(2));
    await tester.enterText(
      find.byType(TextField).at(0),
      'WAS WALKING / STARTED',
    );
    await tester.enterText(
      find.byType(TextField).at(1),
      'respuesta incorrecta',
    );
    await tester.pump();
    final comprobar = find.text('COMPROBAR');
    await tester.ensureVisible(comprobar);
    await tester.tap(comprobar);
    await tester.pumpAndSettle();

    expect(result, isTrue);
    expect(find.text('¡Correcto!'), findsOneWidget);
  });

  testWidgets(
    'una parte obligatoria no puede omitirse aunque alcance el umbral',
    (tester) async {
      bool? result;
      const item = Item(
        id: 'en.n3.c43.e04',
        formato: FormatoItem.completar,
        consigna: TextoApoyo({'es': 'Extrae tres datos.'}),
        feedback: TextoApoyo({'es': 'El estado actual es obligatorio.'}),
        respuesta: 'received | reviewed | repair',
        aceptadas: ['received | reviewed | repair'],
        textosPartes: ['Stage 1: ___', 'Stage 2: ___', 'Current: ___'],
        respuestasPartes: [
          ['received'],
          ['reviewed'],
          ['repair'],
        ],
        partesPuntuables: 3,
        minimoCorrectas: 2,
        partesObligatorias: [2],
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: SingleChildScrollView(
              child: ItemView(
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
        ),
      );

      await tester.enterText(find.byType(TextField).at(0), 'received');
      await tester.enterText(find.byType(TextField).at(1), 'reviewed');
      await tester.enterText(find.byType(TextField).at(2), 'wrong');
      await tester.pump();
      final comprobar = find.text('COMPROBAR');
      await tester.ensureVisible(comprobar);
      await tester.tap(comprobar);
      await tester.pumpAndSettle();

      expect(result, isFalse);
      expect(find.text('Vamos a repasarlo'), findsOneWidget);
    },
  );
}
