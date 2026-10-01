import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../models/models.dart';

// Las 50 situaciones viven en catalogo_situaciones.g.dart (generado).
export 'catalogo_situaciones.g.dart';

const tutores = [
  Tutor(
    id: 'mia',
    nombre: 'Mia',
    personalidad: Personalidad.amigable,
    descripcion: 'Amable y paciente, perfecta para principiantes.',
    color: OL.morado,
  ),
  Tutor(
    id: 'leo',
    nombre: 'Leo',
    personalidad: Personalidad.motivador,
    descripcion: 'Te anima a hablar más y celebra cada avance.',
    color: OL.naranja,
  ),
  Tutor(
    id: 'sofia',
    nombre: 'Sofía',
    personalidad: Personalidad.profesional,
    descripcion: 'Formal y precisa, ideal para el trabajo y entrevistas.',
    color: OL.azul,
  ),
  Tutor(
    id: 'max',
    nombre: 'Max',
    personalidad: Personalidad.directo,
    descripcion: 'Correcciones rápidas y sin rodeos.',
    color: OL.rojo,
  ),
];

Tutor tutor(String id) => tutores.firstWhere((t) => t.id == id, orElse: () => tutores.first);

String nombrePersonalidad(Personalidad p) => switch (p) {
      Personalidad.amigable => 'Amigable',
      Personalidad.motivador => 'Motivador',
      Personalidad.profesional => 'Profesional',
      Personalidad.directo => 'Directo',
    };

/// Un perfil por nivel: es lo que hace que "Restaurante" sea distinto en N1 y N10.
const perfilesNivel = [
  LevelProfile(nivel: 1, vocabularioMax: 300, tiempos: 'presente simple', longitudFrase: '3-6 palabras', velocidad: 0.7, correccion: 'solo errores graves, explicados en el idioma nativo'),
  LevelProfile(nivel: 2, vocabularioMax: 600, tiempos: 'presente, pasado y futuro básicos', longitudFrase: '5-8 palabras', velocidad: 0.75, correccion: 'errores frecuentes, explicados en el idioma nativo'),
  LevelProfile(nivel: 3, vocabularioMax: 1000, tiempos: 'presente continuo, pasado, futuro', longitudFrase: '6-10 palabras', velocidad: 0.8, correccion: 'errores de gramática y vocabulario, explicación breve'),
  LevelProfile(nivel: 4, vocabularioMax: 1500, tiempos: 'todos los tiempos comunes', longitudFrase: '8-12 palabras', velocidad: 0.85, correccion: 'todos los errores, explicación en ambos idiomas'),
  LevelProfile(nivel: 5, vocabularioMax: 2200, tiempos: 'todos + condicionales', longitudFrase: '10-15 palabras', velocidad: 0.9, correccion: 'todos los errores, explicación en el idioma meta con apoyo'),
  LevelProfile(nivel: 6, vocabularioMax: 3000, tiempos: 'todos + phrasal verbs', longitudFrase: 'párrafos cortos', velocidad: 0.95, correccion: 'todos los errores, exige reformular'),
  LevelProfile(nivel: 7, vocabularioMax: 4000, tiempos: 'sin restricción', longitudFrase: 'párrafos', velocidad: 1.0, correccion: 'incluye estilo y registro'),
  LevelProfile(nivel: 8, vocabularioMax: 5000, tiempos: 'sin restricción', longitudFrase: 'sin límite', velocidad: 1.0, correccion: 'incluye matices, expresiones idiomáticas'),
  LevelProfile(nivel: 9, vocabularioMax: 0, tiempos: 'sin restricción', longitudFrase: 'sin límite', velocidad: 1.05, correccion: 'nivel académico y profesional'),
  LevelProfile(nivel: 10, vocabularioMax: 0, tiempos: 'sin restricción', longitudFrase: 'sin límite', velocidad: 1.1, correccion: 'como un hablante nativo exigente'),
];

LevelProfile perfilNivel(int n) => perfilesNivel[n.clamp(1, 10) - 1];

const planes = [
  Plan(id: 'p1', nombre: 'Un idioma', idiomas: 1, precio: 20, incluye: [
    '1 idioma a elegir', '10 niveles · 1 000 lecciones', '50 situaciones de práctica',
    'Conversación libre con IA', 'Corrección de errores y progreso',
  ]),
  Plan(id: 'p2', nombre: 'Dos idiomas', idiomas: 2, precio: 30, incluye: [
    '2 idiomas a elegir', 'Todo lo del plan de 1 idioma', 'Cambia de idioma cuando quieras',
    'Progreso independiente por idioma',
  ]),
  Plan(id: 'p3', nombre: 'Tres idiomas', idiomas: 3, precio: 40, incluye: [
    '3 idiomas a elegir', 'Todo lo del plan de 2 idiomas', 'Tutores con todas las personalidades',
    'Certificado al completar cada nivel',
  ]),
];

/// Actividades diarias (REQUERIMIENTOS §9).
final actividadesDiarias = <(String, String, IconData, Color)>[
  ('Desayunar', 'To have breakfast', Icons.free_breakfast_outlined, OL.naranja),
  ('Caminar', 'To walk', Icons.directions_walk_outlined, OL.verde),
  ('Ir al trabajo', 'To go to work', Icons.work_outline, OL.azul),
  ('Hacer ejercicio', 'To exercise', Icons.fitness_center_outlined, OL.morado),
  ('Estudiar', 'To study', Icons.menu_book_outlined, OL.azul),
  ('Dormir', 'To sleep', Icons.bedtime_outlined, OL.rojo),
];

const segundosPruebaGratis = 60 * 60;
