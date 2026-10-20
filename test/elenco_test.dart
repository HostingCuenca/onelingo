import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/elenco.dart';

const _roles = {'narradora', 'narrador', 'mujer_b', 'hombre_b', 'lumo'};
const _idiomas = ['en', 'es', 'fr', 'de', 'pt', 'it', 'ru', 'ko', 'ja', 'zh'];

/// Tope de líneas de diálogo sin voz asignada (ni en el elenco de su clase ni
/// en el global), que usan el respaldo por orden de aparición. Lo que queda son
/// hablantes sin ninguna pista de género en su clase (tools/voz/elenco_clases.py,
/// «sin_asignar»): sobre todo apellidos japoneses en entrevistas y oficios del
/// curso de español. Antes del elenco por clase: ja 23,8 %, es 5,2 %, pt 2,8 %.
const _topeSinVoz = {'ja': 0.06, 'es': 0.04, 'pt': 0.01};
const _topePorDefecto = 0.005;

Map<String, dynamic> _json(String ruta) =>
    Map<String, dynamic>.from(jsonDecode(File(ruta).readAsStringSync()) as Map);

/// Diálogos de la ruta publicada: id de la unidad → hablante de cada línea.
Map<String, List<List<String>>> _dialogos(String idioma) {
  final res = <String, List<List<String>>>{};
  for (final f in Directory('assets/contenido/$idioma/ruta').listSync()) {
    if (f is! File || !f.path.endsWith('.json')) continue;
    final datos = jsonDecode(f.readAsStringSync());
    if (datos is! Map || datos['unidades'] is! List) continue;
    for (final u in datos['unidades'] as List) {
      for (final p in (u['pasos'] as List? ?? const [])) {
        final dialogo = [
          for (final l in (p['dialogo'] as List? ?? const []))
            if (l is Map && l['hablante'] is String && l.containsKey('texto'))
              l['hablante'] as String,
        ];
        if (dialogo.isNotEmpty) {
          res.putIfAbsent(u['id'] as String, () => []).add(dialogo);
        }
      }
    }
  }
  return res;
}

void main() {
  test('dos mujeres (o dos hombres) de un diálogo suenan distintas', () {
    final v = vocesDelDialogo(
      ['Ana', 'Mia', 'Ana', 'Tom', 'Leo'],
      {
        'Ana': 'narradora',
        'Mia': 'narradora',
        'Tom': 'hombre_b',
        'Leo': 'hombre_b',
      },
    );
    expect(v, {
      'Ana': 'narradora',
      'Mia': 'mujer_b',
      'Tom': 'hombre_b',
      'Leo': 'narrador',
    });
  });

  test(
    'sin elenco: respaldo por orden de aparición (narradora / narrador)',
    () {
      expect(vocesDelDialogo(['やまもと', 'わたなべ', 'やまもと'], {}), {
        'やまもと': 'narradora',
        'わたなべ': 'narrador',
      });
      // Mezcla: el conocido conserva su voz y el desconocido no la repite.
      expect(vocesDelDialogo(['すずき', 'あやか'], {'あやか': 'narradora'}), {
        'すずき': 'narradora',
        'あやか': 'mujer_b',
      });
      expect(vocesDelDialogo([null, 'Lumo'], {'Lumo': 'lumo'}), {
        'Lumo': 'lumo',
      });
    },
  );

  test('precedencia: elenco de la clase > elenco global > respaldo', () {
    const global = {'あやか': 'narradora', 'たなか': 'narradora'};
    // Sin elenco de clase manda el global (たなか tendría voz de mujer).
    expect(vocesDelDialogo(['たなか', 'すずき'], global), {
      'たなか': 'narradora',
      'すずき': 'narrador',
    });
    // La clase lo corrige; el que no está en ningún elenco usa el respaldo.
    expect(
      vocesDelDialogo(
        ['すずき', 'たなか', 'あやか'],
        global,
        clase: {'たなか': 'narrador'},
      ),
      {'すずき': 'narradora', 'たなか': 'narrador', 'あやか': 'mujer_b'},
    );
    // Dos hombres por clase: el segundo pasa a la otra voz si choca.
    expect(
      vocesDelDialogo(
        ['なかむら', 'りょう', 'なかむら'],
        {'りょう': 'narrador'},
        clase: {'なかむら': 'narrador'},
      ),
      {'なかむら': 'narrador', 'りょう': 'hombre_b'},
    );
  });

  test(
    'hay elenco global y por clase para los 10 idiomas, con roles válidos',
    () {
      for (final idioma in _idiomas) {
        final f = File('assets/contenido/$idioma/elenco.json');
        expect(f.existsSync(), isTrue, reason: idioma);
        final elenco = _json(f.path);
        expect(elenco, isNotEmpty, reason: idioma);
        for (final e in elenco.entries) {
          expect(_roles, contains(e.value), reason: '$idioma ${e.key}');
        }
        final clases = _json('assets/contenido/$idioma/elenco_clases.json');
        final dialogos = _dialogos(idioma);
        for (final c in clases.entries) {
          // Cada entrada apunta a una clase y a un hablante que existen.
          expect(dialogos, contains(c.key), reason: '$idioma ${c.key}');
          final hablantes = {for (final d in dialogos[c.key]!) ...d};
          for (final e in Map<String, dynamic>.from(c.value as Map).entries) {
            expect(
              hablantes,
              contains(e.key),
              reason: '$idioma ${c.key} ${e.key}',
            );
            expect(
              _roles,
              contains(e.value),
              reason: '$idioma ${c.key} ${e.key}',
            );
          }
        }
      }
    },
  );

  test(
    'con el elenco por clase, dos personas del mismo género no comparten voz '
    'si hay una libre',
    () {
      const genero = {
        'narradora': 'f',
        'mujer_b': 'f',
        'narrador': 'm',
        'hombre_b': 'm',
      };
      for (final idioma in _idiomas) {
        final global = Map<String, String>.from(
          _json('assets/contenido/$idioma/elenco.json'),
        );
        final clases = _json('assets/contenido/$idioma/elenco_clases.json');
        final dialogos = _dialogos(idioma);
        for (final c in clases.entries) {
          final clase = Map<String, String>.from(c.value as Map);
          for (final d in dialogos[c.key]!) {
            final voces = vocesDelDialogo(d, global, clase: clase);
            for (final h in clase.keys.where(voces.containsKey)) {
              final g = genero[voces[h]];
              // Tres personas del mismo género y solo dos voces: inevitable.
              if (voces.values.where((r) => genero[r] == g).length > 2)
                continue;
              final iguales = voces.entries.where(
                (e) => e.key != h && e.value == voces[h],
              );
              expect(iguales, isEmpty, reason: '$idioma ${c.key} $h');
            }
          }
        }
      }
    },
  );

  test('pocas líneas de diálogo sin voz asignada (respaldo por orden)', () {
    for (final idioma in _idiomas) {
      final global = _json('assets/contenido/$idioma/elenco.json');
      final clases = _json('assets/contenido/$idioma/elenco_clases.json');
      var total = 0;
      var sinVoz = 0;
      for (final u in _dialogos(idioma).entries) {
        final clase = Map<String, dynamic>.from(
          clases[u.key] as Map? ?? const {},
        );
        for (final d in u.value) {
          total += d.length;
          sinVoz += d
              .where((h) => !clase.containsKey(h) && !global.containsKey(h))
              .length;
        }
      }
      expect(total, greaterThan(0), reason: idioma);
      final tope = _topeSinVoz[idioma] ?? _topePorDefecto;
      expect(
        sinVoz / total,
        lessThanOrEqualTo(tope),
        reason: '$idioma: $sinVoz de $total líneas sin voz asignada',
      );
    }
  });
}
