import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/version.dart';

void main() {
  test('la versión de Perfil coincide con pubspec.yaml', () {
    final linea = File('pubspec.yaml')
        .readAsLinesSync()
        .firstWhere((l) => l.startsWith('version:'));
    expect(linea.trim(), 'version: $versionApp+$compilacionApp');
  });
}
