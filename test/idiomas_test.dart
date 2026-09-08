import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/content/curriculum.dart';
import 'package:onelingo/core/content/idiomas.dart';

void main() {
  test('los 10 idiomas tienen 100 lecciones de Nivel 1 con pasos', () {
    for (final l in idiomas) {
      idiomaContenido = l.code;
      final lecciones = leccionesDe(1);
      expect(lecciones.length, 100, reason: l.code);
      for (final lec in lecciones) {
        expect(lec.steps, isNotEmpty, reason: '${l.code} ${lec.id}');
        for (final s in lec.steps) {
          expect(s.prompt.isNotEmpty || s.pairs.isNotEmpty, isTrue, reason: '${l.code} ${lec.id}');
        }
      }
    }
    idiomaContenido = 'en';
  });

  test('idiomas no latinos muestran romanización entre paréntesis', () {
    for (final code in idiomasNoLatinos) {
      idiomaContenido = code;
      final u1 = unidadesDe(1).first;
      for (final (palabra, _) in u1.vocab) {
        expect(palabra, matches(RegExp(r'\([^)]+\)')), reason: '$code: $palabra');
      }
      expect(soloNativo(u1.vocab.first.$1), isNot(contains('(')));
    }
    idiomaContenido = 'en';
  });
}
