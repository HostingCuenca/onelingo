import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/elenco.dart';

const _roles = {'narradora', 'narrador', 'mujer_b', 'hombre_b', 'lumo'};
const _idiomas = ['en', 'es', 'fr', 'de', 'pt', 'it', 'ru', 'ko', 'ja', 'zh'];

/// Apellidos japoneses de la lista cerrada (tools/ia/idiomas/ja.md), en kana y
/// en kanji: no dicen el género, así que tools/voz/elenco.py no los asigna
/// (regla 4) y la app usa el respaldo por orden de aparición.
const _apellidosJa = {
  'たなか', 'すずき', 'わたなべ', 'たかはし', 'いとう', //
  'やまもと', 'なかむら', 'こばやし', 'かとう', 'よしだ',
  '田中', '鈴木', '渡辺', '高橋', '伊藤', '山本', '中村', '小林', '加藤', '吉田',
};

/// Hablante sin género inferible por diseño: apellido japonés, solo o con
/// さん / せんせい / ぶちょう (como la raíz de tools/voz/elenco.py).
bool _sinGeneroPorDiseno(String idioma, String h) =>
    idioma == 'ja' &&
    _apellidosJa.contains(h.replaceFirst(RegExp(r'(さん|ちゃん|くん|せんせい|ぶちょう)$'), ''));

void main() {
  test('dos mujeres (o dos hombres) de un diálogo suenan distintas', () {
    final v = vocesDelDialogo(
      ['Ana', 'Mia', 'Ana', 'Tom', 'Leo'],
      {'Ana': 'narradora', 'Mia': 'narradora', 'Tom': 'hombre_b', 'Leo': 'hombre_b'},
    );
    expect(v, {'Ana': 'narradora', 'Mia': 'mujer_b', 'Tom': 'hombre_b', 'Leo': 'narrador'});
  });

  test('sin elenco: respaldo por orden de aparición (narradora / narrador)', () {
    expect(vocesDelDialogo(['やまもと', 'わたなべ', 'やまもと'], {}), {
      'やまもと': 'narradora',
      'わたなべ': 'narrador',
    });
    // Mezcla: el conocido conserva su voz y el desconocido no la repite.
    expect(vocesDelDialogo(['すずき', 'あやか'], {'あやか': 'narradora'}), {
      'すずき': 'narradora',
      'あやか': 'mujer_b',
    });
    expect(vocesDelDialogo([null, 'Lumo'], {'Lumo': 'lumo'}), {'Lumo': 'lumo'});
  });

  test('hay elenco para los 10 idiomas, con roles válidos y casi todos los hablantes', () {
    for (final idioma in _idiomas) {
      final f = File('assets/contenido/$idioma/elenco.json');
      expect(f.existsSync(), isTrue, reason: idioma);
      final elenco = Map<String, dynamic>.from(jsonDecode(f.readAsStringSync()) as Map);
      expect(elenco, isNotEmpty, reason: idioma);
      for (final e in elenco.entries) {
        expect(_roles, contains(e.value), reason: '$idioma ${e.key}');
      }
      // Los hablantes de la ruta publicada que faltan usan el respaldo por
      // orden; son pocos (oficios sin género claro). Los apellidos japoneses
      // no cuentan: no tienen género y su ausencia es intencionada.
      final hablantes = <String>{};
      for (final ruta in Directory('assets/contenido/$idioma/ruta').listSync()) {
        if (ruta is! File || !ruta.path.endsWith('.json')) continue;
        void recorrer(Object? x) {
          if (x is Map) {
            final h = x['hablante'];
            if (h is String && x.containsKey('texto')) hablantes.add(h);
            x.values.forEach(recorrer);
          } else if (x is List) {
            x.forEach(recorrer);
          }
        }
        recorrer(jsonDecode(ruta.readAsStringSync()));
      }
      final faltan = hablantes
          .where((h) => !elenco.containsKey(h) && !_sinGeneroPorDiseno(idioma, h))
          .length;
      expect(faltan, lessThanOrEqualTo(hablantes.length * 0.6), reason: idioma);
    }
  });
}
