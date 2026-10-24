import 'dart:convert';
import 'dart:math';

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'lexico.dart';

/// Biblioteca de imágenes de vocabulario: una ilustración por concepto, la
/// misma en los 10 idiomas (`assets/img/vocab/<archivo>.webp`). El mapa
/// palabra → imagen de cada idioma lo genera `tools/imagenes/mapear.py` en
/// `assets/contenido/<idioma>/imagenes.json`, con la clave de `claveLexico`.
class ImagenesVocab {
  const ImagenesVocab(this.porClave);
  final Map<String, String> porClave;

  static const vacio = ImagenesVocab({});

  /// Ruta del asset de la palabra, o null si no tiene imagen.
  String? de(String texto) {
    final a = porClave[claveLexico(texto)];
    return a == null ? null : rutaImagenVocab(a);
  }

  /// Todas las imágenes del idioma (para los distractores).
  Iterable<String> get archivos => porClave.values.toSet();
}

String rutaImagenVocab(String archivo) => 'assets/img/vocab/$archivo.webp';

/// Familias que se parecen a la vista (el arroz y los palillos, la parada y el
/// autobús): un distractor nunca es de la familia de la respuesta.
String familiaImagen(String archivo) {
  final c = archivo.startsWith('fruit-veg')
      ? 'fruit-veg'
      : archivo.split('-').first;
  return switch (c) {
    'food' || 'fruit-veg' || 'drink' || 'kitchen' => 'comida',
    'home' || 'furniture' => 'casa',
    'action' || 'emotion' || 'person' || 'family' || 'job' => 'gente',
    'health' || 'body' => 'cuerpo',
    'place' || 'transport' || 'travel' => 'lugares',
    'nature' || 'weather' || 'time' || 'plant' => 'naturaleza',
    'object' || 'tech' || 'school' || 'shopping' || 'work' => 'objetos',
    'leisure' || 'sport' => 'ocio',
    'adjective' || 'color' => 'cualidades',
    _ => c,
  };
}

/// Tres imágenes que no se confunden con `archivo` ni entre sí: cada una de
/// otra familia.
List<String> distractoresImagen(
  String archivo,
  Iterable<String> banco,
  Random rnd,
) {
  final usadas = {familiaImagen(archivo)};
  final elegidas = <String>[];
  for (final a in banco.toList()..shuffle(rnd)) {
    if (elegidas.length == 3) break;
    if (usadas.add(familiaImagen(a))) elegidas.add(a);
  }
  return elegidas;
}

/// Imágenes de vocabulario del idioma; vacío si el idioma aún no tiene.
final imagenesVocabProvider = FutureProvider.family<ImagenesVocab, String>((
  ref,
  idioma,
) async {
  try {
    final raw = await rootBundle.loadString(
      'assets/contenido/$idioma/imagenes.json',
    );
    return ImagenesVocab(Map<String, String>.from(jsonDecode(raw) as Map));
  } catch (_) {
    return ImagenesVocab.vacio;
  }
});
