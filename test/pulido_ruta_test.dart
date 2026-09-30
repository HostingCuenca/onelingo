import 'dart:convert';
import 'dart:io';

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

  group('Producción abierta', () {
    final item = Item.fromJson({
      'id': 'abierta',
      'formato': 'escribir',
      'consigna': {'es': 'Escribe'},
      'respuesta': 'The request was received on Monday and the repair is being done now.',
      'abierta': true,
      'minimoPalabras': 8,
      'maximoPalabras': 20,
    });

    test('se completa al llegar al mínimo de palabras, sin texto exacto', () {
      expect(item.abierta, isTrue);
      expect(corregir(item, 'My laptop was repaired.', 'en'), isFalse);
      expect(
        corregir(
          item,
          'My laptop was checked yesterday and it is ready now.',
          'en',
        ),
        isTrue,
      );
    });
  });

  test('Todas las clases editoriales enseñan antes de practicar', () {
    final niveles = [
      for (final n in [
        'n1',
        'n2',
        'n3',
        'n4',
        'n5',
        'n6',
        'n7',
        'n8',
        'n9',
        'n10',
      ])
        if (File('assets/contenido/en/ruta/$n-editorial.json').existsSync()) n,
    ];
    for (final nivel in niveles) {
      final unidades =
          (jsonDecode(
                File('assets/contenido/en/ruta/$nivel-editorial.json')
                    .readAsStringSync(),
              ) as Map)['unidades']
              as List;
      for (final u in unidades.cast<Map<String, dynamic>>()) {
        final pasos = (u['pasos'] as List).cast<Map<String, dynamic>>();
        final tipos = pasos.map((p) => p['tipo']).toList();
        final id = u['id'];
        expect(tipos.first, 'explicacion', reason: '$id');
        expect(tipos, contains('patron'), reason: '$id sin patrón');
        expect(
          (pasos.first['titulo'] as Map)['es'],
          isNot('Objetivo de la clase'),
          reason: '$id sin explicación real',
        );
        final situacion = pasos.firstWhere((p) => p['tipo'] == 'situacion');
        expect(
          (situacion['dialogo'] as List).length,
          greaterThanOrEqualTo(3),
          reason: '$id situación sin diálogo',
        );
        expect(
          (situacion['items'] as List).every(
            (i) => !(i['id'] as String).contains('situation-check'),
          ),
          isTrue,
          reason: '$id situación copiada de la práctica',
        );
        final errores = (u['erroresFrecuentes'] as List)
            .cast<Map<String, dynamic>>();
        expect(errores.length, 2, reason: '$id');
        expect(
          errores.every((e) => !(e['incorrecto'] as String).endsWith(' ?')),
          isTrue,
          reason: '$id con errores de relleno',
        );
      }
      expect(unidades, isNotEmpty);
    }
  });
}
