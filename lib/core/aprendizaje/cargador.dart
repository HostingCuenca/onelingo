import 'dart:convert';

import 'package:flutter/services.dart';

import 'integridad.dart' show indiceFormasVerbales;
import 'modelos.dart';

/// Carga las rutas desde assets (rootBundle: válido en web y móvil).
class CargadorRuta {
  CargadorRuta({AssetBundle? bundle}) : _bundle = bundle ?? rootBundle;
  final AssetBundle _bundle;
  final _cache = <String, Future<RutaCargada?>>{};
  final _formas = <String, Future<Map<String, Set<String>>>>{};

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
    // Los módulos se descargan a la vez (en la web son peticiones HTTP).
    final porModulo = await Future.wait([
      for (final m in curso.modulos) _modulo(idioma, m),
    ]);
    final unidades = [for (final u in porModulo) ...u];
    unidades.sort((a, b) => a.orden.compareTo(b.orden));
    return RutaCargada(curso, unidades);
  }

  /// Forma conjugada → infinitivos según `assets/contenido/<idioma>/verbos.json`
  /// (la misma fuente que «Mis verbos»), para `problemasDeContenido`; vacío si
  /// el idioma no tiene tabla de verbos.
  Future<Map<String, Set<String>>> formasVerbales(String idioma) =>
      _formas.putIfAbsent(idioma, () async {
        final String raw;
        try {
          raw = await _bundle.loadString(
            'assets/contenido/$idioma/verbos.json',
            cache: false,
          );
        } catch (_) {
          return const {};
        }
        return indiceFormasVerbales(jsonDecode(raw) as Map<String, dynamic>);
      });

  Future<List<UnidadRuta>> _modulo(String idioma, ModuloIndice m) async {
    // Un módulo ausente o dañado no debe tumbar el curso entero; las
    // pruebas de integridad lo detectan antes de publicar.
    try {
      final datos = jsonDecode(
        await _bundle.loadString('${base(idioma)}/${m.archivo}', cache: false),
      ) as Map<String, dynamic>;
      return [
        for (final u in datos['unidades'] as List)
          UnidadRuta.fromJson(
            u as Map<String, dynamic>,
            idioma: idioma,
            nivel: m.nivel,
            modulo: m.id,
          ),
      ];
    } catch (e) {
      modulosConError.add('${m.id}: $e');
      return const [];
    }
  }
}
