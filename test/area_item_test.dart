import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';

void main() {
  test('el área sale del formato, no de la primera habilidad de la unidad', () {
    final j =
        jsonDecode(File('assets/contenido/es/ruta/n3-b01.json').readAsStringSync())
            as Map<String, dynamic>;
    final u = UnidadRuta.fromJson(
      (j['unidades'] as List)
          .cast<Map<String, dynamic>>()
          .firstWhere((u) => u['id'] == 'es.n3.c01'),
      idioma: 'es',
      nivel: 'n3',
    );
    expect(u.habilidades.first, 'vocabulario');
    final items = [for (final p in u.pasos) ...p.items];
    Item de(FormatoItem f) => items.firstWhere((i) => i.formato == f);
    // «¿Le ___ que ya soy coordinadora?» es gramática, no vocabulario.
    expect(areaDeItem(u, items.firstWhere((i) => i.id == 'g3')), 'gramatica');
    expect(areaDeItem(u, de(FormatoItem.escuchar)), 'listening');
    expect(areaDeItem(u, de(FormatoItem.escribir)), 'escritura');
    expect(areaDeItem(u, de(FormatoItem.relacionar)), 'vocabulario');
  });
}
