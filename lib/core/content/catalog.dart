import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../i18n/i18n.dart';
import '../models/models.dart';

// Las 50 situaciones viven en catalogo_situaciones.g.dart (generado).
export 'catalogo_situaciones.g.dart';

/// Tutores (getter: las descripciones salen en el idioma de la interfaz).
List<Tutor> get tutores => [
  Tutor(
    id: 'mia',
    nombre: 'Mia',
    personalidad: Personalidad.amigable,
    descripcion: tr('Amable y paciente, perfecta para principiantes.'),
    color: OL.morado,
  ),
  Tutor(
    id: 'leo',
    nombre: 'Leo',
    personalidad: Personalidad.motivador,
    descripcion: tr('Te anima a hablar más y celebra cada avance.'),
    color: OL.naranja,
  ),
  Tutor(
    id: 'sofia',
    nombre: 'Sofía',
    personalidad: Personalidad.profesional,
    descripcion: tr('Formal y precisa, ideal para el trabajo y entrevistas.'),
    color: OL.azul,
  ),
  Tutor(
    id: 'max',
    nombre: 'Max',
    personalidad: Personalidad.directo,
    descripcion: tr('Correcciones rápidas y sin rodeos.'),
    color: OL.rojo,
  ),
];

Tutor tutor(String id) => tutores.firstWhere((t) => t.id == id, orElse: () => tutores.first);

String nombrePersonalidad(Personalidad p) => switch (p) {
      Personalidad.amigable => tr('Amigable'),
      Personalidad.motivador => tr('Motivador'),
      Personalidad.profesional => tr('Profesional'),
      Personalidad.directo => tr('Directo'),
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

/// Planes (getter: nombres y ventajas en el idioma de la interfaz).
List<Plan> get planes => [
  Plan(id: 'p1', nombre: tr('Un idioma'), idiomas: 1, precio: 20, incluye: [
    tr('1 idioma a elegir'), tr('10 niveles · 1 000 lecciones'), tr('50 situaciones de práctica'),
    tr('Conversación libre con IA'), tr('Corrección de errores y progreso'),
  ]),
  Plan(id: 'p2', nombre: tr('Dos idiomas'), idiomas: 2, precio: 30, incluye: [
    tr('2 idiomas a elegir'), tr('Todo lo del plan de 1 idioma'), tr('Cambia de idioma cuando quieras'),
    tr('Progreso independiente por idioma'),
  ]),
  Plan(id: 'p3', nombre: tr('Tres idiomas'), idiomas: 3, precio: 40, incluye: [
    tr('3 idiomas a elegir'), tr('Todo lo del plan de 2 idiomas'), tr('Tutores con todas las personalidades'),
    tr('Certificado al completar cada nivel'),
  ]),
];

/// Actividades diarias (REQUERIMIENTOS §9).
/// El primer campo es el nombre visible (idioma de la interfaz); el segundo,
/// la frase en el idioma que se aprende.
List<(String, String, IconData, Color)> get actividadesDiarias => [
  (tr('Desayunar'), 'To have breakfast', Icons.free_breakfast_outlined, OL.naranja),
  (tr('Caminar'), 'To walk', Icons.directions_walk_outlined, OL.verde),
  (tr('Ir al trabajo'), 'To go to work', Icons.work_outline, OL.azul),
  (tr('Hacer ejercicio'), 'To exercise', Icons.fitness_center_outlined, OL.morado),
  (tr('Estudiar'), 'To study', Icons.menu_book_outlined, OL.azul),
  (tr('Dormir'), 'To sleep', Icons.bedtime_outlined, OL.rojo),
];

const segundosPruebaGratis = 60 * 60;
