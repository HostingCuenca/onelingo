import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/lexico/imagenes.dart';
import 'package:onelingo/core/lexico/lexico.dart';
import 'package:onelingo/features/lexico/repaso_palabras_screen.dart';

const idiomas = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko'];

Map<String, String> mapa(String idioma) => Map<String, String>.from(
  jsonDecode(File('assets/contenido/$idioma/imagenes.json').readAsStringSync())
      as Map,
);

void main() {
  test('cada palabra con imagen apunta a una ilustración que existe', () {
    for (final idioma in idiomas) {
      final m = mapa(idioma);
      expect(m.length, greaterThan(300), reason: idioma);
      for (final a in m.values.toSet()) {
        expect(File(rutaImagenVocab(a)).existsSync(), isTrue, reason: a);
      }
    }
  });

  test('los mapas están al día con la ruta y las situaciones', () {
    final r = Process.runSync('python3', [
      'tools/imagenes/mapear.py',
      '--comprobar',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
  });

  test('la imagen se busca con la clave del léxico', () {
    const i = ImagenesVocab({'acheter': 'action-buy'});
    expect(i.de('  Acheter. '), 'assets/img/vocab/action-buy.webp');
    expect(i.de('vendre'), isNull);
  });

  test('distractores de otras familias, que no se confunden a la vista', () {
    final banco = mapa('fr').values.toSet();
    for (final a in ['food-rice', 'transport-bus', 'adjective-big']) {
      final d = distractoresImagen(a, banco, Random(4));
      expect(d.length, 3);
      final familias = {familiaImagen(a), ...d.map(familiaImagen)};
      expect(familias.length, 4, reason: '$a: $d');
    }
    expect(familiaImagen('kitchen-chopsticks'), familiaImagen('food-rice'));
    expect(familiaImagen('place-bus-stop'), familiaImagen('transport-bus'));
  });

  test('escucha y elige la imagen: cuatro distintas y una correcta', () {
    final imagenes = ImagenesVocab(mapa('fr'));
    final con = EntradaLexico(
      clave: claveLexico('acheter'),
      texto: 'acheter',
      traduccion: 'comprar',
      nivel: 1,
    );
    final q = preguntaImagen(con, imagenes, Random(2))!;
    expect(q.forma, FormaPregunta.imagen);
    expect(q.escucha, isTrue);
    expect(q.opciones.toSet().length, 4);
    expect(q.opciones[q.correcta], 'assets/img/vocab/action-buy.webp');

    final sin = EntradaLexico(
      clave: 'zzz',
      texto: 'zzz',
      traduccion: 'nada',
      nivel: 1,
    );
    expect(preguntaImagen(sin, imagenes, Random(2)), isNull);
  });
}
