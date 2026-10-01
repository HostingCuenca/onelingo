import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/features/ruta/item_view.dart';
import 'package:onelingo/features/ruta/unidad_screen.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test(
    'Clases editoriales: unir y escribir se añaden y los formatos se alternan',
    () async {
      final ruta = (await CargadorRuta().cargar('en'))!;
      final clases = ruta.unidades
          .where((u) => RegExp(r'\.n\d+\.class-').hasMatch(u.id))
          .toList();
      expect(clases.length, greaterThan(100));
      var conUnir = 0, conEscribir = 0, repetidos = 0, pares = 0;
      for (final u in clases) {
        final f = formatosDeClase(u);
        if (f.contains(FormatoItem.relacionar)) conUnir++;
        if (f.contains(FormatoItem.escribir)) conEscribir++;
        for (var i = 1; i < f.length; i++) {
          pares++;
          if (f[i] == f[i - 1]) repetidos++;
        }
      }
      // Prácticamente todas las clases tienen ya «unir» y «escribir».
      expect(conUnir / clases.length, greaterThan(.95));
      expect(conEscribir / clases.length, greaterThan(.95));
      // Pocos ejercicios seguidos del mismo tipo.
      expect(repetidos / pares, lessThan(.2));
      // Fundamentos conserva su secuencia diseñada a mano.
      final f0 = ruta.unidad('en.f0.primer-contacto')!;
      expect(
        formatosDeClase(f0).where((f) => f == FormatoItem.escribir).length,
        lessThanOrEqualTo(1),
      );
    },
  );

  testWidgets(
    'Escribir: la IA acepta otra forma correcta y muestra el modelo',
    (tester) async {
      const item = Item(
        id: 'prueba.escribir',
        formato: FormatoItem.escribir,
        consigna: TextoApoyo({'es': 'Escribe esta frase en inglés'}),
        feedback: TextoApoyo({'es': 'Bien.'}),
        texto: 'Normalmente empiezo a las ocho.',
        respuesta: 'I usually start at eight.',
        aceptadas: ['I usually start at eight.'],
      );
      String? revisada;
      var comprobado = false;
      await tester.pumpWidget(
        MaterialApp(
          theme: buildTheme(),
          home: Scaffold(
            body: ItemView(
              item: item,
              idioma: 'en',
              cadena: const ['es'],
              guiada: false,
              permitirReintento: true,
              lumo: false,
              botonFijo: true,
              onComprobado: (ok, _) => comprobado = ok,
              onContinuar: () {},
              revisarConIa: (i, respuesta) async {
                revisada = respuesta;
                return {
                  'correcta': true,
                  'correccion': respuesta,
                  'explicacion': 'Correcta: usually va antes del verbo.',
                  'errores': [],
                };
              },
            ),
          ),
        ),
      );
      await tester.enterText(find.byType(TextField), 'I usually begin at 8.');
      await tester.pump();
      await tester.tap(find.text('COMPROBAR'));
      await tester.pumpAndSettle();
      expect(revisada, 'I usually begin at 8.');
      expect(comprobado, isTrue);
      expect(find.text('¡Correcto!'), findsOneWidget);
      expect(
        find.text('Correcta: usually va antes del verbo.'),
        findsOneWidget,
      );
      expect(
        find.text('Otra forma: I usually start at eight.'),
        findsOneWidget,
      );
    },
  );

  testWidgets('Escribir: si coincide exactamente no se consulta a la IA', (
    tester,
  ) async {
    const item = Item(
      id: 'prueba.exacta',
      formato: FormatoItem.escribir,
      consigna: TextoApoyo({'es': 'Escribe'}),
      feedback: TextoApoyo({'es': 'Bien.'}),
      respuesta: 'Thank you.',
      aceptadas: ['Thank you.'],
    );
    var llamadas = 0;
    await tester.pumpWidget(
      MaterialApp(
        theme: buildTheme(),
        home: Scaffold(
          body: ItemView(
            item: item,
            idioma: 'en',
            cadena: const ['es'],
            guiada: false,
            permitirReintento: true,
            lumo: false,
            onComprobado: (_, _) {},
            onContinuar: () {},
            revisarConIa: (_, _) async {
              llamadas++;
              return null;
            },
          ),
        ),
      ),
    );
    await tester.enterText(find.byType(TextField), 'thank you');
    await tester.pump();
    await tester.tap(find.text('COMPROBAR'));
    await tester.pumpAndSettle();
    expect(llamadas, 0);
    expect(find.text('¡Correcto!'), findsOneWidget);
  });
}
