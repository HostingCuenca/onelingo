import 'dart:convert';

import 'package:flutter/services.dart';

import 'modelos.dart';

/// Carga las rutas desde assets (rootBundle: válido en web y móvil).
class CargadorRuta {
  CargadorRuta({AssetBundle? bundle}) : _bundle = bundle ?? rootBundle;
  final AssetBundle _bundle;
  final _cache = <String, Future<RutaCargada?>>{};

  /// Módulos que no se pudieron cargar (para pruebas y diagnóstico).
  final modulosConError = <String>[];

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
      // Un módulo ausente o dañado no debe tumbar el curso entero; las
      // pruebas de integridad lo detectan antes de publicar.
      try {
        final datos =
            jsonDecode(
                  await _bundle.loadString(
                    '${base(idioma)}/${m.archivo}',
                    cache: false,
                  ),
                )
                as Map<String, dynamic>;
        final delModulo = [
          for (final u in datos['unidades'] as List)
            UnidadRuta.fromJson(
              u as Map<String, dynamic>,
              idioma: idioma,
              nivel: m.nivel,
              modulo: m.id,
            ),
        ];
        unidades.addAll(delModulo);
      } catch (e) {
        modulosConError.add('${m.id}: $e');
      }
    }
    unidades.sort((a, b) => a.orden.compareTo(b.orden));
    return RutaCargada(curso, unidades);
  }
}
