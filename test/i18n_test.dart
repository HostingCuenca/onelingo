import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/i18n/i18n.dart';
import 'package:onelingo/core/state/providers.dart';

/// Interfaz multilingüe (docs/claude-educacion/I18N.md).
void main() {
  tearDown(() => I18n.idioma.value = 'es');

  test('tr: traduce, sustituye marcas y nunca se rompe', () {
    I18n.usar('en', {
      'Nivel {n}': 'Level {n}',
      'Mis palabras': 'My words',
    });
    expect(tr('Mis palabras'), 'Mis palabras');
    I18n.idioma.value = 'en';
    expect(tr('Mis palabras'), 'My words');
    expect(tr('Nivel {n}', {'n': 3}), 'Level 3');
    // Sin traducción: el español, nunca un hueco.
    expect(tr('Texto nuevo sin traducir'), 'Texto nuevo sin traducir');
  });

  test('idioma de la interfaz: el elegido o, si no, según el nativo', () {
    expect(const ProgressState(idiomaNativo: 'es').interfaz, 'es');
    expect(const ProgressState(idiomaNativo: 'en').interfaz, 'en');
    // Sin interfaz propia todavía: inglés.
    expect(const ProgressState(idiomaNativo: 'pt').interfaz, 'en');
    expect(
      const ProgressState(idiomaNativo: 'es', idiomaInterfaz: 'en').interfaz,
      'en',
    );
    final vuelta = ProgressState.fromJson(
      const ProgressState(idiomaInterfaz: 'en').toJson(),
    );
    expect(vuelta.idiomaInterfaz, 'en');
  });

  test('todos los textos de la interfaz tienen traducción al inglés', () {
    final r = Process.runSync('python3', [
      'tools/i18n/extraer.py',
      '--comprobar',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
  });
}
