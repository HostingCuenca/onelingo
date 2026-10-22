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

  /// Carácter de un tutor en vivo, en pocas palabras (ficha en backend/src/lib/personajes.ts).
  String get rasgo => switch (id) {
    'ana' => tr('Alegre y cercana'),
    'elena' => tr('Elegante y serena'),
    'julia' => tr('Entusiasta y creativa'),
    'chloe' => tr('Espontánea y risueña'),
    'nora' => tr('Dulce y muy paciente'),
    'lucas' => tr('Amable y práctico'),
    'tomas' => tr('Cálido y pausado'),
    'frank' => tr('Tranquilo y experimentado'),
    'diego' => tr('Cercano y bromista'),
    'erik' => tr('Relajado y curioso'),
    'hana' => tr('Curiosa y detallista'),
    'andre' => tr('Seguro y motivador'),
    _ => '',
  };

  /// En qué se apoya cada tutor en vivo para enseñar.
  String get especialidad => switch (id) {
    'ana' => tr('Viajes y conversación libre: habla de lo que quieras.'),
    'elena' => tr('Describir lugares, personas y cosas con la palabra justa.'),
    'julia' => tr(
      'Juegos de rol y escenas para practicar como en la vida real.',
    ),
    'chloe' => tr('Cómo se habla de verdad: expresiones de todos los días.'),
    'nora' => tr('Ideal para empezar: va despacio y te da confianza.'),
    'lucas' => tr(
      'Situaciones prácticas paso a paso: compras, transporte y citas.',
    ),
    'tomas' => tr('Pronunciación, ritmo y entonación para sonar natural.'),
    'frank' => tr('Trabajo, trámites e imprevistos de viaje, con calma.'),
    'diego' => tr('Vocabulario con humor: comida, juegos y retos rápidos.'),
    'erik' => tr('Charla casual y reuniones de trabajo a distancia.'),
    'hana' => tr('Contar historias: lo que te pasó, en orden y en pasado.'),
    'andre' => tr('Entender lo que oyes a velocidad real.'),
    _ => '',
  };
}

/// Lumo que habla (2D con bocas sincronizadas con la voz): el tutor más
/// ligero (~80 KB frente a 1,1–1,4 MB de un tutor 3D). Va destacado primero.
const lumoTutor = Tutor3d('lumo', 'Lumo');

/// Ana: tutora realista de la llamada en vivo (Avaturn), la primera de la
/// cuadrícula.
const anaTutor = Tutor3d('ana', 'Ana');

/// Tutores realistas de la llamada en vivo (Microsoft Rocketbox, licencia
/// MIT, y Ana), en una cuadrícula de 6 × 2: ellas arriba y ellos abajo.
const tutorasVivo = [
  anaTutor,
  Tutor3d('elena', 'Elena'),
  Tutor3d('julia', 'Julia'),
  Tutor3d('chloe', 'Chloe'),
  Tutor3d('nora', 'Nora'),
  Tutor3d('hana', 'Hana'),
];
const tutoresVivoHombres = [
  Tutor3d('lucas', 'Lucas'),
  Tutor3d('tomas', 'Tomás'),
  Tutor3d('frank', 'Frank'),
  Tutor3d('diego', 'Diego'),
  Tutor3d('erik', 'Erik'),
  Tutor3d('andre', 'Andre'),
];
const tutoresVivo = [...tutorasVivo, ...tutoresVivoHombres];

/// Tutores 3D anteriores (MakeHuman), que se retirarán más adelante.
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
  for (final t in [...tutoresVivo, lumoTutor, ...tutores3d]) {
    if (t.id == id) return t;
  }
  return null;
}
