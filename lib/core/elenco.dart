import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

/// Elenco de voces de los diálogos. Los roles son los del servidor
/// (`backend/src/lib/voz.ts`, `NATIVAS`): narradora, narrador, mujer_b,
/// hombre_b y lumo; cada idioma tiene una voz nativa para cada uno.
///
/// - `assets/contenido/<idioma>/elenco.json` (`{hablante: rol}`), generado por
///   `tools/voz/elenco.py`: la voz global de cada personaje.
/// - `assets/contenido/<idioma>/elenco_clases.json`
///   (`{idClase: {hablante: rol}}`), generado por `tools/voz/elenco_clases.py`:
///   la voz de los hablantes sin género fijo (apellidos japoneses, oficios
///   como «Policía» o «Recepcionista») en cada clase concreta.
class Elenco {
  Elenco._();
  static final Map<String, Future<Map<String, String>>> _cache = {};
  static final Map<String, Future<Map<String, Map<String, String>>>>
  _cacheClases = {};

  /// Elenco global del idioma (vacío si no existe: se usa el respaldo).
  static Future<Map<String, String>> de(String idioma) =>
      _cache.putIfAbsent(idioma, () async {
        try {
          final raw = await rootBundle.loadString(
            'assets/contenido/$idioma/elenco.json',
          );
          return Map<String, String>.from(jsonDecode(raw) as Map);
        } catch (_) {
          return const {};
        }
      });

  /// Elencos por clase del idioma (vacío si no existe).
  static Future<Map<String, Map<String, String>>> clasesDe(String idioma) =>
      _cacheClases.putIfAbsent(idioma, () async {
        try {
          final raw = await rootBundle.loadString(
            'assets/contenido/$idioma/elenco_clases.json',
          );
          return {
            for (final e in (jsonDecode(raw) as Map).entries)
              e.key as String: Map<String, String>.from(e.value as Map),
          };
        } catch (_) {
          return const {};
        }
      });

  /// Rol de voz de `hablante` dentro de un diálogo (`dialogo`: el hablante de
  /// cada línea, en orden) de la clase `clase` (id de la unidad). Null sin
  /// hablante: la voz por defecto.
  static Future<String?> voz(
    String idioma,
    List<String?> dialogo,
    String? hablante, {
    String? clase,
  }) async {
    if (hablante == null || hablante.isEmpty) return null;
    final elenco = await de(idioma);
    final porClase = clase == null
        ? const <String, String>{}
        : (await clasesDe(idioma))[clase] ?? const <String, String>{};
    return vocesDelDialogo(dialogo, elenco, clase: porClase)[hablante];
  }
}

const _otraDelGenero = {
  'narradora': 'mujer_b',
  'mujer_b': 'narradora',
  'narrador': 'hombre_b',
  'hombre_b': 'narrador',
};

/// Voz de cada hablante de un diálogo:
/// 1. la del elenco de la clase (`clase`), si la tiene;
/// 2. si no, la del elenco global;
/// 3. si no está en ninguno (contenido nuevo o sin género inferible), por
///    orden de aparición: alterna narradora / narrador;
/// 4. si dos hablantes distintos quedarían con la misma voz, el que aparece
///    después pasa a la otra voz de su género (narradora ↔ mujer_b,
///    narrador ↔ hombre_b) cuando está libre. Así dos mujeres de un mismo
///    diálogo suenan distintas.
Map<String, String> vocesDelDialogo(
  Iterable<String?> hablantes,
  Map<String, String> elenco, {
  Map<String, String> clase = const {},
}) {
  final orden = <String>[];
  for (final h in hablantes) {
    if (h != null && h.isNotEmpty && !orden.contains(h)) orden.add(h);
  }
  final usadas = <String>{};
  final voces = <String, String>{};
  for (var i = 0; i < orden.length; i++) {
    final h = orden[i];
    var rol = clase[h] ?? elenco[h] ?? (i.isEven ? 'narradora' : 'narrador');
    final otra = _otraDelGenero[rol];
    if (usadas.contains(rol) && otra != null && !usadas.contains(otra)) {
      rol = otra;
    }
    voces[h] = rol;
    usadas.add(rol);
  }
  return voces;
}
