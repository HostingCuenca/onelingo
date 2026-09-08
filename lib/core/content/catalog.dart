import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../models/models.dart';

/// Las 50 situaciones de práctica libre (REQUERIMIENTOS §6).
final situaciones = <Situation>[
  _s(1, 'En un restaurante', 'Comida', Icons.restaurant_outlined, OL.morado),
  _s(2, 'En una cafetería', 'Comida', Icons.coffee_outlined, OL.morado),
  _s(3, 'En el supermercado', 'Compras', Icons.shopping_cart_outlined, OL.naranja),
  _s(4, 'De compras en una tienda', 'Compras', Icons.storefront_outlined, OL.naranja),
  _s(5, 'Comprando ropa', 'Compras', Icons.checkroom_outlined, OL.naranja),
  _s(6, 'Comprando zapatos', 'Compras', Icons.ice_skating_outlined, OL.naranja),
  _s(7, 'En el aeropuerto', 'Viajes', Icons.flight_takeoff_outlined, OL.azul),
  _s(8, 'En el avión', 'Viajes', Icons.airplanemode_active_outlined, OL.azul),
  _s(9, 'En inmigración o aduana', 'Viajes', Icons.badge_outlined, OL.azul),
  _s(10, 'En un hotel', 'Viajes', Icons.hotel_outlined, OL.azul),
  _s(11, 'Tomando un taxi o Uber', 'Transporte', Icons.local_taxi_outlined, OL.azul),
  _s(12, 'Alquilando un automóvil', 'Transporte', Icons.car_rental_outlined, OL.azul),
  _s(13, 'En una gasolinera', 'Transporte', Icons.local_gas_station_outlined, OL.azul),
  _s(14, 'En un taller mecánico', 'Transporte', Icons.build_outlined, OL.azul),
  _s(15, 'En el médico', 'Salud', Icons.medical_services_outlined, OL.rojo),
  _s(16, 'En la farmacia', 'Salud', Icons.local_pharmacy_outlined, OL.rojo),
  _s(17, 'En el dentista', 'Salud', Icons.mood_outlined, OL.rojo),
  _s(18, 'En el banco', 'Dinero', Icons.account_balance_outlined, OL.verde),
  _s(19, 'Pagando en una tienda o caja', 'Dinero', Icons.point_of_sale_outlined, OL.verde),
  _s(20, 'En una entrevista de trabajo', 'Trabajo', Icons.work_outline, OL.morado),
  _s(21, 'En el trabajo', 'Trabajo', Icons.business_center_outlined, OL.morado),
  _s(22, 'Hablando con un jefe', 'Trabajo', Icons.supervisor_account_outlined, OL.morado),
  _s(23, 'En una reunión de trabajo', 'Trabajo', Icons.groups_outlined, OL.morado),
  _s(24, 'En una llamada telefónica', 'Comunicación', Icons.phone_outlined, OL.verde),
  _s(25, 'Llamada de servicio al cliente', 'Comunicación', Icons.support_agent_outlined, OL.verde),
  _s(26, 'Alquilando una casa o apartamento', 'Hogar', Icons.home_work_outlined, OL.naranja),
  _s(27, 'Resolviendo un problema en el apartamento', 'Hogar', Icons.plumbing_outlined, OL.naranja),
  _s(28, 'Hablando con un técnico o reparador', 'Hogar', Icons.handyman_outlined, OL.naranja),
  _s(29, 'Hablando con la policía', 'Emergencias', Icons.local_police_outlined, OL.rojo),
  _s(30, 'En una situación de tráfico', 'Transporte', Icons.traffic_outlined, OL.rojo),
  _s(31, 'En un autobús', 'Transporte', Icons.directions_bus_outlined, OL.azul),
  _s(32, 'En una estación de tren', 'Transporte', Icons.train_outlined, OL.azul),
  _s(33, 'Preguntando cómo llegar a un lugar', 'Ciudad', Icons.signpost_outlined, OL.azul),
  _s(34, 'En una escuela', 'Educación', Icons.school_outlined, OL.verde),
  _s(35, 'Hablando con un profesor', 'Educación', Icons.co_present_outlined, OL.verde),
  _s(36, 'Hablando de deportes', 'Ocio', Icons.sports_soccer_outlined, OL.verde),
  _s(37, 'En el gimnasio', 'Ocio', Icons.fitness_center_outlined, OL.verde),
  _s(38, 'En la playa', 'Ocio', Icons.beach_access_outlined, OL.naranja),
  _s(39, 'De vacaciones', 'Viajes', Icons.luggage_outlined, OL.naranja),
  _s(40, 'En el cine', 'Ocio', Icons.movie_outlined, OL.morado),
  _s(41, 'Hablando de música', 'Ocio', Icons.music_note_outlined, OL.morado),
  _s(42, 'Hablando de películas y series', 'Ocio', Icons.live_tv_outlined, OL.morado),
  _s(43, 'Hablando sobre la familia', 'Social', Icons.family_restroom_outlined, OL.rojo),
  _s(44, 'Conociendo a una persona nueva', 'Social', Icons.waving_hand_outlined, OL.rojo),
  _s(45, 'Conversaciones sociales y relaciones', 'Social', Icons.favorite_outline, OL.rojo),
  _s(46, 'En una fiesta o celebración', 'Social', Icons.celebration_outlined, OL.naranja),
  _s(47, 'En un cumpleaños o evento', 'Social', Icons.cake_outlined, OL.naranja),
  _s(48, 'Cocinando y hablando de comida', 'Comida', Icons.soup_kitchen_outlined, OL.morado),
  _s(49, 'Tareas de la casa y vida cotidiana', 'Hogar', Icons.cleaning_services_outlined, OL.verde),
  _s(50, 'Conversación libre sobre cualquier tema', 'Libre', Icons.forum_outlined, OL.morado),
];

Situation _s(int id, String n, String c, IconData i, Color col) =>
    Situation(id: id, nombre: n, categoria: c, icono: i, color: col);

Situation situacion(int id) => situaciones[id - 1];

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

LevelProfile perfilNivel(int n) => perfilesNivel[n - 1];

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
