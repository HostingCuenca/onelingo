import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

/// Elenco de voces de los diálogos: `assets/contenido/<idioma>/elenco.json`
/// (`{hablante: rol}`), generado por `tools/voz/elenco.py`. Los roles son los
/// del servidor (`backend/src/lib/voz.ts`, `NATIVAS`): narradora, narrador,
/// mujer_b, hombre_b y lumo; cada idioma tiene una voz nativa para cada uno.
class Elenco {
  Elenco._();
  static final Map<String, Future<Map<String, String>>> _cache = {};

  /// Elenco del idioma (vacío si no existe: se usa el respaldo por orden).
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

  /// Rol de voz de `hablante` dentro de un diálogo (`dialogo`: el hablante de
  /// cada línea, en orden). Null sin hablante: la voz por defecto.
  static Future<String?> voz(
    String idioma,
    List<String?> dialogo,
    String? hablante,
  ) async {
    if (hablante == null || hablante.isEmpty) return null;
    return vocesDelDialogo(dialogo, await de(idioma))[hablante];
  }
}

const _otraDelGenero = {
  'narradora': 'mujer_b',
  'mujer_b': 'narradora',
  'narrador': 'hombre_b',
  'hombre_b': 'narrador',
};

/// Voz de cada hablante de un diálogo:
/// 1. la del elenco;
/// 2. si no está en el elenco (contenido nuevo), por orden de aparición:
///    alterna narradora / narrador;
/// 3. si dos hablantes distintos quedarían con la misma voz, el que aparece
///    después pasa a la otra voz de su género (narradora ↔ mujer_b,
///    narrador ↔ hombre_b) cuando está libre. Así dos mujeres de un mismo
///    diálogo suenan distintas.
Map<String, String> vocesDelDialogo(
  Iterable<String?> hablantes,
  Map<String, String> elenco,
) {
  final orden = <String>[];
  for (final h in hablantes) {
    if (h != null && h.isNotEmpty && !orden.contains(h)) orden.add(h);
  }
  final usadas = <String>{};
  final voces = <String, String>{};
  for (var i = 0; i < orden.length; i++) {
    final h = orden[i];
    var rol = elenco[h] ?? (i.isEven ? 'narradora' : 'narrador');
    final otra = _otraDelGenero[rol];
    if (usadas.contains(rol) && otra != null && !usadas.contains(otra)) {
      rol = otra;
    }
    voces[h] = rol;
    usadas.add(rol);
  }
  return voces;
}
