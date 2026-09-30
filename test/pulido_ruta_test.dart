import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/correccion.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';

Item _escribir(String respuesta) => Item.fromJson({
  'id': 'x',
  'formato': 'completar',
  'consigna': {'es': 'Escribe'},
  'respuesta': respuesta,
});

void main() {
  group('Contracciones en inglés', () {
    test('se aceptan en ambos sentidos', () {
      expect(
        respuestaEscritaCorrecta(
          _escribir('I am a student.'),
          "I'm a student",
          'en',
        ),
        isTrue,
      );
      expect(
        respuestaEscritaCorrecta(
          _escribir("She doesn't work."),
          'She does not work',
          'en',
        ),
        isTrue,
      );
      expect(
        respuestaEscritaCorrecta(
          _escribir('I cannot swim.'),
          "I can't swim",
          'en',
        ),
        isTrue,
      );
      expect(
        respuestaEscritaCorrecta(
          _escribir('They will not come.'),
          "They won't come",
          'en',
        ),
        isTrue,
      );
      expect(
        respuestaEscritaCorrecta(
          _escribir("It is Tom's book."),
          "It's Tom's book",
          'en',
        ),
        isTrue,
      );
    });

    test('el genitivo sajón no se convierte en «is»', () {
      expect(expandirContracciones("my brother's pen"), "my brother's pen");
      expect(
        respuestaEscritaCorrecta(
          _escribir("My brother's pen is new."),
          'My brother is pen is new',
          'en',
        ),
        isFalse,
      );
    });

    test('otros idiomas no expanden', () {
      expect(
        respuestaEscritaCorrecta(_escribir("c'est"), 'ce est', 'fr'),
        isFalse,
      );
    });

    test('multiparte usa las mismas reglas', () {
      expect(mismaRespuesta("don't", 'do not', 'en'), isTrue);
      expect(mismaRespuesta('esta', 'está', 'es'), isTrue);
      expect(mismaRespuesta('', '', 'en'), isFalse);
    });
  });

  group('Umbral de aprobación', () {
    test('las pruebas cortas no exigen el 100 %', () {
      expect(aciertosNecesarios(4, 0.8), 3);
      expect(aciertosNecesarios(3, 0.8), 2);
      expect(aciertosNecesarios(5, 0.8), 4);
      expect(aciertosNecesarios(10, 0.8), 8);
      expect(aciertosNecesarios(2, 0.8), 2);
      expect(aciertosNecesarios(1, 0.8), 1);
      expect(superaUmbral(3, 4, 0.8), isTrue);
      expect(superaUmbral(2, 4, 0.8), isFalse);
      expect(superaUmbral(0, 0, 0.8), isFalse);
    });
  });
}
