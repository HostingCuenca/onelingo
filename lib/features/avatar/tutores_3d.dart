/// Tutores 3D de videollamada (web/avatar/roster.json). Los retratos están
/// también en assets/img/tutores para mostrarlos en la app (web y Android).
class Tutor3d {
  const Tutor3d(this.id, this.nombre, this.estilo);
  final String id, nombre, estilo;
  String get retrato => 'assets/img/tutores/$id.webp';
}

/// Lumo que habla (2D con bocas sincronizadas con la voz): el tutor más
/// ligero (~80 KB frente a 1,1–1,4 MB de un tutor 3D). Va destacado primero.
const lumoTutor = Tutor3d(
  'lumo',
  'Lumo',
  'Tu compañero de OneLingo: habla contigo, te corrige y carga al instante.',
);

const tutores3d = [
  Tutor3d('amara', 'Amara', 'Conversacional · acento estadounidense'),
  Tutor3d('sofia', 'Sofía', 'Educativa · acento estadounidense'),
  Tutor3d('clara', 'Clara', 'Educativa · acento británico'),
  Tutor3d('owen', 'Owen', 'Cálido · acento británico'),
  Tutor3d('daniel', 'Daniel', 'Tranquilo · acento estadounidense'),
  Tutor3d('malik', 'Malik', 'Educativo · acento estadounidense'),
  Tutor3d('lucia', 'Lucía', 'Cercana · acento mexicano suave'),
  Tutor3d('mateo', 'Mateo', 'Animado · acento puertorriqueño'),
  Tutor3d('mei', 'Mei', 'Serena · acento de Hong Kong'),
  Tutor3d('kenji', 'Kenji', 'Amable · acento japonés'),
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
