// Exporta los bancos escritos a mano al formato del pipeline para probar el cargador.
//   EXPORTAR=1 flutter test test/exportar_semilla_test.dart
import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/content/curriculum.dart';

void main() {
  test('exporta assets/contenido/<idioma>/nivel-1.json desde los bancos', () {
    for (final l in idiomas) {
      idiomaContenido = l.code;
      final unidades = unidadesDe(1);
      final rom = RegExp(r'^(.*?)\s*\(([^)]*)\)\s*$');
      List<Map<String, String>> partir(String s) {
        final m = rom.firstMatch(s);
        return [{'texto': m == null ? s : m.group(1)!.trim(), 'rom': m == null ? '' : m.group(2)!}];
      }
      final salida = {
        'idioma': l.code,
        'nivel': 1,
        'generado': DateTime.now().toIso8601String(),
        'origen': 'semilla manual (idiomas.dart)',
        'unidades': [
          for (final u in unidades)
            {
              'numero': u.numero,
              'tema': u.titulo,
              'titulo': u.titulo,
              'objetivo': '',
              'gramatica': '',
              'vocab': [
                for (final (p, t) in u.vocab)
                  {'palabra': partir(p).first['texto'], 'romanizacion': partir(p).first['rom'], 'traduccion': t, 'ejemplo': ''}
              ],
              'frases': [
                for (final (f, t) in u.frases)
                  {'texto': f, 'romanizacion': partir(t).first['rom'], 'traduccion': partir(t).first['texto']}
              ],
              'dialogo': <Map<String, String>>[],
              'errores_tipicos': <Map<String, String>>[],
              'examen': <Map<String, Object>>[],
            }
        ],
      };
      final f = File('assets/contenido/${l.code}/nivel-1.json');
      f.writeAsStringSync(jsonEncode(salida));
      expect(unidades.length, 20);
    }
    idiomaContenido = 'en';
  }, skip: Platform.environment['EXPORTAR'] != '1' ? 'solo con EXPORTAR=1' : false);
}
