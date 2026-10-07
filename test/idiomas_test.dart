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

  test('ningún idioma queda sin ruta nueva (ko ya la tiene)', () {
    // Con ko (versión esencial N1–N2) los 10 idiomas habilitados tienen ruta:
    // la tarjeta «En preparación» ya no se muestra para ninguno.
    expect(idiomasConRuta, contains('ko'));
    for (final l in idiomas) {
      expect(idiomasConRuta, contains(l.code), reason: l.code);
    }
  });
}
