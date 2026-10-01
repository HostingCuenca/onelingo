import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

/// Reglas de arquitectura de docs/ARQUITECTURA_VIGENTE.md que se pueden
/// comprobar leyendo el código. Si una falla, corrige el código, no la regla:
/// cambiar una regla es una decisión del cliente (DECISIONES.md).
void main() {
  final dart = [
    for (final f in Directory('lib').listSync(recursive: true))
      if (f is File && f.path.endsWith('.dart')) f,
  ];
  String sinComentarios(String s) => s
      .split('\n')
      .where((l) => !l.trimLeft().startsWith('//'))
      .join('\n');

  test('la jerga interna no llega a la pantalla', () {
    // Textos que describen el sistema por dentro y confunden al alumno.
    const prohibidos = [
      'Nivel interno',
      'orientativ',
      'Banco piloto',
      'Evidencia:',
      'no certifica',
      'no equivale a dominar',
      'Comprobación guiada',
      'dominio aún no evaluado',
      'introducción sugerida',
    ];
    final fallos = <String>[];
    for (final f in dart) {
      final texto = sinComentarios(f.readAsStringSync());
      for (final p in prohibidos) {
        // Solo cuenta dentro de textos (entre comillas), no en claves de
        // datos como `'orientativo': true`.
        final enTexto = RegExp(
          "['\"][^'\"\\n]*${RegExp.escape(p)}[^'\"\\n]*['\"](?!\\s*:)",
        );
        if (enTexto.hasMatch(texto)) fallos.add('${f.path}: «$p»');
      }
    }
    expect(fallos, isEmpty, reason: fallos.join('\n'));
  });

  test('el alumno nunca elige su nivel con un desplegable', () {
    // El nivel sale de la prueba de ubicación o de superar niveles.
    final fallos = [
      for (final f in dart)
        if (f.path.startsWith('lib/features') &&
            RegExp(r'DropdownButtonFormField<int>').hasMatch(
              f.readAsStringSync(),
            ))
          f.path,
    ];
    expect(fallos, isEmpty, reason: fallos.join('\n'));
  });

  test('las pantallas retiradas no vuelven', () {
    const retiradas = [
      'lib/features/library/library_screen.dart',
      'lib/features/foundations/foundations_screen.dart',
      'lib/shared/widgets/learning_path.dart',
      'lib/shared/widgets/learning_primer.dart',
      'lib/core/content/foundations.dart',
      // Fase C: las situaciones tienen una sola fuente (SITUACIONES_V2.md).
      'lib/core/content/situation_units.dart',
      'assets/contenido/en/situational_vocabulary.json',
      'backend/src/content/situational-vocabulary-en.json',
    ];
    for (final r in retiradas) {
      expect(File(r).existsSync(), isFalse, reason: '$r se retiró');
    }
  });

  test('las opciones de respuesta usan OpcionRespuesta', () {
    // Las pantallas de ejercicios no dibujan opciones propias.
    final fallos = [
      for (final f in dart)
        if (f.path.startsWith('lib/features') &&
            RegExp(r'class _Opcion\b').hasMatch(f.readAsStringSync()))
          f.path,
    ];
    expect(fallos, isEmpty, reason: fallos.join('\n'));
  });
}
