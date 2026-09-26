import 'dart:convert';

import 'package:flutter/services.dart';

import 'modelos.dart';

/// Carga las rutas desde assets (rootBundle: válido en web y móvil).
class CargadorRuta {
  CargadorRuta({AssetBundle? bundle}) : _bundle = bundle ?? rootBundle;
  final AssetBundle _bundle;
  final _cache = <String, Future<RutaCargada?>>{};

  static String base(String idioma) => 'assets/contenido/$idioma/ruta';

  /// Ruta de un idioma, o null si el idioma aún no tiene ruta.
  Future<RutaCargada?> cargar(String idioma) =>
      _cache.putIfAbsent(idioma, () => _leer(idioma));

  Future<RutaCargada?> _leer(String idioma) async {
    final String indice;
    try {
      // Sin la caché del bundle: CargadorRuta ya cachea la ruta completa.
      indice = await _bundle.loadString(
        '${base(idioma)}/curso.json',
        cache: false,
      );
    } catch (_) {
      return null;
    }
    final curso = Curso.fromJson(jsonDecode(indice) as Map<String, dynamic>);
    final unidades = <UnidadRuta>[];
    for (final m in curso.modulos) {
      final datos =
          jsonDecode(
                await _bundle.loadString(
                  '${base(idioma)}/${m.archivo}',
                  cache: false,
                ),
              )
              as Map<String, dynamic>;
      for (final u in datos['unidades'] as List) {
        unidades.add(
          UnidadRuta.fromJson(
            u as Map<String, dynamic>,
            idioma: idioma,
            nivel: m.nivel,
          ),
        );
      }
    }
    unidades.sort((a, b) => a.orden.compareTo(b.orden));
    return RutaCargada(curso, unidades);
  }
}
