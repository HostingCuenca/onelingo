import 'i18n/i18n.dart';

/// Sectores (id → nombre visible en el idioma de la interfaz).
Map<String, String> get sectoresAprendizaje => {
  'estudiante': tr('Estudiante'),
  'tecnologia': tr('Tecnología e ingeniería'),
  'salud': tr('Salud y bienestar'),
  'negocios': tr('Negocios y administración'),
  'ventas': tr('Ventas y atención al cliente'),
  'educacion': tr('Educación e investigación'),
  'turismo': tr('Turismo y hostelería'),
  'general': tr('Otros sectores / vida cotidiana'),
};
/// Objetivos (id → nombre visible en el idioma de la interfaz).
Map<String, String> get objetivosAprendizaje => {
  'conversar': tr('Conversar con confianza'),
  'trabajar': tr('Reuniones y trabajo en equipo'),
  'entrevistas': tr('Entrevistas y oportunidades'),
  'viajar': tr('Viajar y vivir en otro país'),
  'estudiar': tr('Estudiar y entender contenidos'),
  'clientes': tr('Atender y comunicarme con clientes'),
  'escribir': tr('Escribir mensajes y correos'),
  'escuchar': tr('Entender conversaciones y videos'),
};
