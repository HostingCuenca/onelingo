import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/content/contenido_json.dart';
import 'package:onelingo/core/content/curriculum.dart';
import 'package:onelingo/core/models/models.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('un idioma sin ruta nueva (ko) ya no carga lecciones antiguas', () async {
    await ContenidoJson.precargar('ko');
    expect(ContenidoJson.unidades('ko', 1), isNull);
    idiomaContenido = 'ko';
    expect(unidadesDe(1), isEmpty);
    expect(leccionesDe(1), isEmpty);
    idiomaContenido = 'en';
  });

  test('el examen del nivel usa las preguntas generadas y la lección lleva diálogo y errores', () async {
    await ContenidoJson.precargar('en');
    idiomaContenido = 'en';
    final u1 = unidadesDe(1).first;
    expect(u1.examen.length, inInclusiveRange(3, 4));
    expect(u1.dialogo.length, inInclusiveRange(4, 8));
    expect(u1.erroresTipicos.length, inInclusiveRange(2, 4));
    final lecciones = leccionesDe(1);
    expect(lecciones[1].steps.first.type, StepType.readText); // Frases: "Antes de empezar"
    expect(lecciones[4].steps.first.type, StepType.roleplay); // Repaso: diálogo
    idiomaContenido = 'en';
  });

  test('sin fichero JSON se mantiene el banco manual', () async {
    await ContenidoJson.precargar('fr');
    idiomaContenido = 'fr';
    expect(unidadesDe(2).length, 20); // nivel 2 no tiene JSON: banco genérico
    idiomaContenido = 'en';
  });
}
