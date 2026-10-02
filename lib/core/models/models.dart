import 'package:flutter/material.dart';

import '../i18n/i18n.dart';

/// Habilidad que mide un paso de lección. Alimenta las barras del perfil y la
/// clasificación de errores (REQUERIMIENTOS §8 y §13).
enum Skill {
  vocabulario('Vocabulario'),
  gramatica('Gramática'),
  conjugacion('Conjugación'),
  listening('Listening'),
  pronunciacion('Pronunciación'),
  frases('Formación de frases'),
  lectura('Lectura'),
  escritura('Escritura'),
  conversacion('Conversación');

  const Skill(this.nombreEs);

  /// Nombre en español (dato estable; no se muestra tal cual).
  final String nombreEs;

  /// Nombre visible en el idioma de la interfaz.
  String get nombre => switch (this) {
    vocabulario => tr('Vocabulario'),
    gramatica => tr('Gramática'),
    conjugacion => tr('Conjugación'),
    listening => tr('Listening'),
    pronunciacion => tr('Pronunciación'),
    frases => tr('Formación de frases'),
    lectura => tr('Lectura'),
    escritura => tr('Escritura'),
    conversacion => tr('Conversación'),
  };
}

/// Los ~10 tipos de ejercicio del reproductor de lección (ARQUITECTURA §1).
enum StepType {
  flashcard,
  multipleChoice,
  fillBlank,
  orderWords,
  listenWrite,
  matchPairs,
  imageChoice,
  speak,
  roleplay,
  readText,
}

class Language {
  const Language({
    required this.code,
    required String nombre,
    required this.nombreNativo,
    this.disponible = true,
  }) : nombreEs = nombre;
  final String code;
  final String nombreEs; // en español (clave de traducción)
  final String nombreNativo; // en el propio idioma

  /// Nombre en el idioma de la interfaz.
  String get nombre => trDato(nombreEs);
  final bool disponible;
}

class Level {
  const Level({
    required this.numero,
    required String nombre,
    required this.descripcion,
    required this.temario,
  }) : nombreEs = nombre;
  final int numero;
  final String nombreEs;

  /// Nombre en el idioma de la interfaz (la descripción y el temario son
  /// contenido antiguo, solo en español).
  String get nombre => trDato(nombreEs);
  final String descripcion;
  final List<String> temario;

  static const totalLecciones = 100;
  static const minimoAprobacion = 65;
}

class Unit {
  const Unit({
    required this.nivel,
    required this.numero,
    required this.titulo,
    required this.icono,
    required this.color,
    this.vocab = const [],
    this.frases = const [],
    this.gramatica = '',
    this.dialogo = const [],
    this.erroresTipicos = const [],
    this.examen = const [],
  });
  final int nivel;
  final int numero; // 1..20 dentro del nivel
  final String titulo;
  final IconData icono;
  final Color color;

  /// Explicación gramatical de la unidad (del contenido generado).
  final String gramatica;

  /// Diálogo de situación real: (quién, texto en idioma meta, traducción).
  final List<(String, String, String)> dialogo;

  /// Errores típicos de hispanohablantes: (incorrecto, correcto, explicación).
  final List<(String, String, String)> erroresTipicos;

  /// Preguntas para el examen del nivel: (pregunta, opciones, índice correcta, explicación).
  final List<(String, List<String>, int, String)> examen;

  /// Pares (idioma meta, idioma nativo) que usan las lecciones de la unidad.
  final List<(String, String)> vocab;

  /// Frases (idioma meta, idioma nativo).
  final List<(String, String)> frases;

  static const leccionesPorUnidad = 5;
}

class LessonStep {
  const LessonStep({
    required this.type,
    required this.skill,
    required this.prompt,
    this.answer = '',
    this.options = const [],
    this.pairs = const [],
    this.translation = '',
    this.hint = '',
  });
  final StepType type;
  final Skill skill;

  /// Enunciado o frase principal (según el tipo).
  final String prompt;
  final String answer;
  final List<String> options;
  final List<(String, String)> pairs;
  final String translation;
  final String hint;
}

class Lesson {
  const Lesson({
    required this.id,
    required this.nivel,
    required this.numero,
    required this.unidad,
    required this.titulo,
    required this.subtitulo,
    required this.steps,
    this.xp = 20,
  });
  final String id; // "L1-023"
  final int nivel;
  final int numero; // 1..100
  final int unidad;
  final String titulo;
  final String subtitulo;
  final List<LessonStep> steps;
  final int xp;

  Set<Skill> get skills => steps.map((s) => s.skill).toSet();
}

enum LessonState { bloqueada, actual, completada }

class Situation {
  const Situation({
    required this.id,
    required this.nombre,
    required this.categoria,
    required this.icono,
    required this.color,
  });
  final int id;
  final String nombre;
  final String categoria;
  final IconData icono;
  final Color color;
}

enum Personalidad { amigable, motivador, profesional, directo }

class Tutor {
  const Tutor({
    required this.id,
    required this.nombre,
    required this.personalidad,
    required this.descripcion,
    required this.color,
  });
  final String id;
  final String nombre;
  final Personalidad personalidad;
  final String descripcion;
  final Color color;
}

/// Perfil que se inyecta en el prompt de la IA según el nivel (ARQUITECTURA §5).
class LevelProfile {
  const LevelProfile({
    required this.nivel,
    required this.vocabularioMax,
    required this.tiempos,
    required this.longitudFrase,
    required this.velocidad,
    required this.correccion,
  });
  final int nivel;
  final int vocabularioMax; // 0 = sin límite
  final String tiempos;
  final String longitudFrase;
  final double velocidad; // 0.7 .. 1.0
  final String correccion;
}

class Mistake {
  const Mistake({
    required this.id,
    required this.skill,
    required this.original,
    required this.correccion,
    required this.explicacion,
    required this.fecha,
    this.origen = '',
    this.practicado = false,
  });
  final String id;
  final Skill skill;
  final String original;
  final String correccion;
  final String explicacion;
  final DateTime fecha;
  final String origen;
  final bool practicado;

  Mistake copyWith({bool? practicado}) => Mistake(
        id: id,
        skill: skill,
        original: original,
        correccion: correccion,
        explicacion: explicacion,
        fecha: fecha,
        origen: origen,
        practicado: practicado ?? this.practicado,
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'skill': skill.name,
        'original': original,
        'correccion': correccion,
        'explicacion': explicacion,
        'fecha': fecha.toIso8601String(),
        'origen': origen,
        'practicado': practicado,
      };

  static Mistake fromJson(Map<String, dynamic> j) => Mistake(
        id: j['id'] as String,
        skill: Skill.values.byName(j['skill'] as String),
        original: j['original'] as String,
        correccion: j['correccion'] as String,
        explicacion: j['explicacion'] as String,
        fecha: DateTime.parse(j['fecha'] as String),
        origen: (j['origen'] as String?) ?? '',
        practicado: (j['practicado'] as bool?) ?? false,
      );
}

class Plan {
  const Plan({
    required this.id,
    required this.nombre,
    required this.idiomas,
    required this.precio,
    required this.incluye,
  });
  final String id;
  final String nombre;
  final int idiomas;
  final int precio; // USD / mes
  final List<String> incluye;
}
