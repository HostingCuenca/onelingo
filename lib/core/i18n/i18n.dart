import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

/// Interfaz multilingüe (I1, docs/claude-educacion/I18N.md).
///
/// El texto en español es la clave: `tr('Mis palabras')` devuelve «My words»
/// si la interfaz está en inglés y el texto tal cual si está en español o si
/// falta la traducción (nunca se rompe). Las traducciones viven en
/// `assets/i18n/<idioma>.json` ({"texto en español": "traducción"}); las
/// claves se extraen con `python3 tools/i18n/extraer.py`.
abstract final class I18n {
  /// Idiomas de interfaz disponibles (código → nombre en ese idioma).
  static const disponibles = {'es': 'Español', 'en': 'English'};

  /// Idioma actual de la interfaz.
  static final idioma = ValueNotifier<String>('es');

  static final _diccionarios = <String, Map<String, String>>{};

  /// Carga los diccionarios (una vez, al arrancar).
  static Future<void> cargar() async {
    for (final codigo in disponibles.keys) {
      if (codigo == 'es') continue;
      try {
        final raw = await rootBundle.loadString('assets/i18n/$codigo.json');
        _diccionarios[codigo] = Map<String, String>.from(
          jsonDecode(raw) as Map,
        );
      } catch (_) {
        // Sin diccionario: la interfaz se ve en español.
      }
    }
  }

  @visibleForTesting
  static void usar(String codigo, Map<String, String> diccionario) =>
      _diccionarios[codigo] = diccionario;

  static String traducir(String es, Map<String, Object?> datos) {
    var t = idioma.value == 'es'
        ? es
        : (_diccionarios[idioma.value]?[es] ?? es);
    for (final e in datos.entries) {
      t = t.replaceAll('{${e.key}}', '${e.value}');
    }
    return t;
  }
}

/// Texto de interfaz en el idioma del alumno. [es] es una cadena literal en
/// español (sin `$`): los valores van como `{nombre}` en [datos].
String tr(String es, [Map<String, Object?> datos = const {}]) =>
    I18n.traducir(es, datos);

/// Texto fijo que llega como dato (nombre o categoría de una situación…).
/// Sus claves se declaran en `tools/i18n/extraer.py` (DATOS).
String trDato(String es) => I18n.traducir(es, const {});

/// Idioma de interfaz por defecto según el idioma nativo: el propio si está
/// disponible; si no, inglés.
String idiomaInterfazPara(String nativo) =>
    I18n.disponibles.containsKey(nativo) ? nativo : 'en';

/// Idiomas que puede tener un texto de apoyo del contenido.
const _apoyos = {'es', 'en', 'fr', 'pt', 'de', 'it'};

/// Resuelve los textos de apoyo de un JSON de contenido: cada mapa
/// `{"es": …, "en": …}` (solo cadenas) se cambia por el texto en [idioma],
/// o en español si falta. Lo demás queda igual. Así un contenido puede pasar
/// de un texto simple (solo español) a bilingüe sin tocar el modelo.
Object? localizarApoyo(Object? j, String idioma) {
  if (j is List) return [for (final x in j) localizarApoyo(x, idioma)];
  if (j is Map) {
    if (j.isNotEmpty &&
        j.containsKey('es') &&
        j.keys.every(_apoyos.contains) &&
        j.values.every((v) => v is String)) {
      return (j[idioma] as String?) ?? j['es'] as String;
    }
    return {
      for (final e in j.entries) '${e.key}': localizarApoyo(e.value, idioma),
    };
  }
  return j;
}
