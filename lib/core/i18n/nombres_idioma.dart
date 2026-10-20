import 'i18n.dart';

/// Nombre del idioma dentro de una frase, en el idioma de la interfaz:
/// en minúscula en español («¿Qué quieres lograr con el japonés?») y con
/// mayúscula en inglés («… with Japanese?»). Fuente única para frases que
/// nombran el idioma que se estudia (registro, prueba de nivel, tutores).
String nombreIdiomaEnFrase(String code) => switch (code) {
  'en' => tr('inglés'),
  'es' => tr('español'),
  'fr' => tr('francés'),
  'de' => tr('alemán'),
  'pt' => tr('portugués'),
  'it' => tr('italiano'),
  'zh' => tr('chino'),
  'ja' => tr('japonés'),
  'ko' => tr('coreano'),
  'ru' => tr('ruso'),
  _ => code,
};
