import '../../core/i18n/i18n.dart';

/// Tutores 3D de videollamada (web/avatar/roster.json). Los retratos están
/// también en assets/img/tutores para mostrarlos en la app (web y Android).
class Tutor3d {
  const Tutor3d(this.id, this.nombre);
  final String id, nombre;
  String get retrato => 'assets/img/tutores/$id.webp';

  /// Descripción en el idioma de la interfaz (se resuelve al mostrarla).
  String get estilo => switch (id) {
    'lumo' => tr(
      'Tu compañero de OneLingo: habla contigo, te corrige y carga al instante.',
    ),
    'amara' => tr('Conversacional · acento estadounidense'),
    'sofia' => tr('Educativa · acento estadounidense'),
    'clara' => tr('Educativa · acento británico'),
    'owen' => tr('Cálido · acento británico'),
    'daniel' => tr('Tranquilo · acento estadounidense'),
    'malik' => tr('Educativo · acento estadounidense'),
    'lucia' => tr('Cercana · acento mexicano suave'),
    'mateo' => tr('Animado · acento puertorriqueño'),
    'mei' => tr('Serena · acento de Hong Kong'),
    'kenji' => tr('Amable · acento japonés'),
    _ => '',
  };
}

/// Lumo que habla (2D con bocas sincronizadas con la voz): el tutor más
/// ligero (~80 KB frente a 1,1–1,4 MB de un tutor 3D). Va destacado primero.
const lumoTutor = Tutor3d('lumo', 'Lumo');

const tutores3d = [
  Tutor3d('amara', 'Amara'),
  Tutor3d('sofia', 'Sofía'),
  Tutor3d('clara', 'Clara'),
  Tutor3d('owen', 'Owen'),
  Tutor3d('daniel', 'Daniel'),
  Tutor3d('malik', 'Malik'),
  Tutor3d('lucia', 'Lucía'),
  Tutor3d('mateo', 'Mateo'),
  Tutor3d('mei', 'Mei'),
  Tutor3d('kenji', 'Kenji'),
];

/// Recomendados por idioma (mismo criterio que el visor web).
const _recomendados = {
  'en': ['amara', 'sofia', 'clara'],
  'es': ['lucia', 'mateo'],
  'fr': ['clara', 'sofia'],
  'de': ['daniel', 'owen'],
  'pt': ['amara', 'mateo'],
  'it': ['sofia', 'mateo'],
  'zh': ['mei', 'kenji'],
  'ja': ['kenji', 'mei'],
  'ko': ['mei', 'kenji'],
  'ru': ['owen', 'clara'],
};

List<String> recomendados3d(String idioma) =>
    _recomendados[idioma] ?? _recomendados['en']!;

/// Tutores ordenados con los recomendados para el idioma primero.
List<Tutor3d> tutores3dPara(String idioma) {
  final r = recomendados3d(idioma);
  int orden(Tutor3d t) => r.contains(t.id) ? r.indexOf(t.id) : 99;
  return [...tutores3d]..sort((a, b) => orden(a).compareTo(orden(b)));
}

Tutor3d? tutor3d(String id) {
  for (final t in [lumoTutor, ...tutores3d]) {
    if (t.id == id) return t;
  }
  return null;
}
