import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/providers.dart' show idiomasConRuta;
import 'package:onelingo/core/content/curriculum.dart';

void main() {
  test('los idiomas con ruta tienen 100 lecciones de Nivel 1 con pasos', () {
    for (final l in idiomas.where((l) => idiomasConRuta.contains(l.code))) {
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

  test('idiomas sin ruta nueva (ja, ko, ru): sin lecciones antiguas', () {
    for (final code in const ['ja', 'ko', 'ru']) {
      idiomaContenido = code;
      expect(idiomasConRuta, isNot(contains(code)), reason: code);
      for (final n in [0, 1, 2]) {
        expect(unidadesDe(n), isEmpty, reason: '$code N$n');
        expect(leccionesDe(n), isEmpty, reason: '$code N$n');
      }
    }
    idiomaContenido = 'en';
  });
}
