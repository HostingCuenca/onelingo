import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/features/ruta/item_view.dart';

void main() {
  const visibleStimulus =
      'Caso: recoge el paquete en Desk Four y completa el formulario K28.';

  Item writingItem({String? audio}) => Item(
    id: 'en.n3.c54.e04',
    formato: FormatoItem.escribir,
    consigna: const TextoApoyo({'es': 'Redacta una respuesta breve.'}),
    feedback: const TextoApoyo({'es': 'Incluye todos los datos del caso.'}),
    respuesta: 'Respuesta modelo',
    aceptadas: const ['Respuesta modelo'],
    texto: visibleStimulus,
    audio: audio,
  );

  Widget app(Item item) => MaterialApp(
    home: Scaffold(
      body: SingleChildScrollView(
        child: ItemView(
          item: item,
          idioma: 'en',
          cadena: const ['es'],
          guiada: false,
          permitirReintento: false,
          onComprobado: (_, _) {},
          onContinuar: () {},
        ),
      ),
    ),
  );

  testWidgets('escribir muestra el estimulo textual cuando no hay audio', (
    tester,
  ) async {
    await tester.pumpWidget(app(writingItem()));

    expect(find.text(visibleStimulus), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget);
  });

  testWidgets(
    'escribir con audio no revela el texto alternativo antes del intento',
    (tester) async {
      await tester.pumpWidget(
        app(writingItem(audio: 'Audio visible para el alumno.')),
      );

      expect(find.text(visibleStimulus), findsNothing);
      expect(find.text('Escuchar y escribir'), findsOneWidget);
    },
  );

  testWidgets('elegir muestra la fuente editorial que resuelve la pregunta', (
    tester,
  ) async {
    const source =
        'Source card: the café will open at 08:00 next week.';
    const item = Item(
      id: 'en.n3.c74.e01',
      formato: FormatoItem.elegir,
      consigna: TextoApoyo({'es': '¿Qué dato sí está en la ficha?'}),
      feedback: TextoApoyo({'es': 'La hora aparece en la fuente.'}),
      texto: source,
      opciones: [
        Opcion.meta('the café opens at 08:00 next week'),
        Opcion.meta('the café is popular'),
      ],
      indiceRespuesta: 0,
    );

    await tester.pumpWidget(app(item));

    expect(find.text(source), findsOneWidget);
    expect(find.text('the café opens at 08:00 next week'), findsOneWidget);
  });
}
