// GENERADO por tools/contenido/generar_situaciones.py desde
// assets/contenido/situaciones/catalogo.json. No editar a mano.

import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../models/models.dart';

/// Las 50 situaciones de práctica (contenido por tramo en
/// `assets/contenido/<idioma>/situaciones.json`).
const situaciones = <Situation>[
  Situation(id: 1, nombre: 'En un restaurante', categoria: 'Comida', icono: Icons.restaurant_outlined, color: OL.morado),
  Situation(id: 2, nombre: 'En una cafetería', categoria: 'Comida', icono: Icons.coffee_outlined, color: OL.morado),
  Situation(id: 3, nombre: 'En el supermercado', categoria: 'Compras', icono: Icons.shopping_cart_outlined, color: OL.naranja),
  Situation(id: 4, nombre: 'De compras en una tienda', categoria: 'Compras', icono: Icons.storefront_outlined, color: OL.naranja),
  Situation(id: 5, nombre: 'Comprando ropa', categoria: 'Compras', icono: Icons.checkroom_outlined, color: OL.naranja),
  Situation(id: 6, nombre: 'Comprando zapatos', categoria: 'Compras', icono: Icons.ice_skating_outlined, color: OL.naranja),
  Situation(id: 7, nombre: 'En el aeropuerto', categoria: 'Viajes', icono: Icons.flight_takeoff_outlined, color: OL.azul),
  Situation(id: 8, nombre: 'En el avión', categoria: 'Viajes', icono: Icons.airplanemode_active_outlined, color: OL.azul),
  Situation(id: 9, nombre: 'En inmigración o aduana', categoria: 'Viajes', icono: Icons.badge_outlined, color: OL.azul),
  Situation(id: 10, nombre: 'En un hotel', categoria: 'Viajes', icono: Icons.hotel_outlined, color: OL.azul),
  Situation(id: 11, nombre: 'Tomando un taxi o Uber', categoria: 'Transporte', icono: Icons.local_taxi_outlined, color: OL.azul),
  Situation(id: 12, nombre: 'Alquilando un automóvil', categoria: 'Transporte', icono: Icons.car_rental_outlined, color: OL.azul),
  Situation(id: 13, nombre: 'En una gasolinera', categoria: 'Transporte', icono: Icons.local_gas_station_outlined, color: OL.azul),
  Situation(id: 14, nombre: 'En un taller mecánico', categoria: 'Transporte', icono: Icons.build_outlined, color: OL.azul),
  Situation(id: 15, nombre: 'En el médico', categoria: 'Salud', icono: Icons.medical_services_outlined, color: OL.rojo),
  Situation(id: 16, nombre: 'En la farmacia', categoria: 'Salud', icono: Icons.local_pharmacy_outlined, color: OL.rojo),
  Situation(id: 17, nombre: 'En el dentista', categoria: 'Salud', icono: Icons.mood_outlined, color: OL.rojo),
  Situation(id: 18, nombre: 'En el banco', categoria: 'Dinero', icono: Icons.account_balance_outlined, color: OL.verde),
  Situation(id: 19, nombre: 'Pagando en una tienda o caja', categoria: 'Dinero', icono: Icons.point_of_sale_outlined, color: OL.verde),
  Situation(id: 20, nombre: 'En una entrevista de trabajo', categoria: 'Trabajo', icono: Icons.work_outline, color: OL.morado),
  Situation(id: 21, nombre: 'En el trabajo', categoria: 'Trabajo', icono: Icons.business_center_outlined, color: OL.morado),
  Situation(id: 22, nombre: 'Hablando con un jefe', categoria: 'Trabajo', icono: Icons.supervisor_account_outlined, color: OL.morado),
  Situation(id: 23, nombre: 'En una reunión de trabajo', categoria: 'Trabajo', icono: Icons.groups_outlined, color: OL.morado),
  Situation(id: 24, nombre: 'En una llamada telefónica', categoria: 'Comunicación', icono: Icons.phone_outlined, color: OL.verde),
  Situation(id: 25, nombre: 'Llamada de servicio al cliente', categoria: 'Comunicación', icono: Icons.support_agent_outlined, color: OL.verde),
  Situation(id: 26, nombre: 'Alquilando una casa o apartamento', categoria: 'Hogar', icono: Icons.home_work_outlined, color: OL.naranja),
  Situation(id: 27, nombre: 'Resolviendo un problema en el apartamento', categoria: 'Hogar', icono: Icons.plumbing_outlined, color: OL.naranja),
  Situation(id: 28, nombre: 'Hablando con un técnico o reparador', categoria: 'Hogar', icono: Icons.handyman_outlined, color: OL.naranja),
  Situation(id: 29, nombre: 'Hablando con la policía', categoria: 'Emergencias', icono: Icons.local_police_outlined, color: OL.rojo),
  Situation(id: 30, nombre: 'En una situación de tráfico', categoria: 'Transporte', icono: Icons.traffic_outlined, color: OL.rojo),
  Situation(id: 31, nombre: 'En un autobús', categoria: 'Transporte', icono: Icons.directions_bus_outlined, color: OL.azul),
  Situation(id: 32, nombre: 'En una estación de tren', categoria: 'Transporte', icono: Icons.train_outlined, color: OL.azul),
  Situation(id: 33, nombre: 'Preguntando cómo llegar a un lugar', categoria: 'Ciudad', icono: Icons.signpost_outlined, color: OL.azul),
  Situation(id: 34, nombre: 'En una escuela', categoria: 'Educación', icono: Icons.school_outlined, color: OL.verde),
  Situation(id: 35, nombre: 'Hablando con un profesor', categoria: 'Educación', icono: Icons.co_present_outlined, color: OL.verde),
  Situation(id: 36, nombre: 'Hablando de deportes', categoria: 'Ocio', icono: Icons.sports_soccer_outlined, color: OL.verde),
  Situation(id: 37, nombre: 'En el gimnasio', categoria: 'Ocio', icono: Icons.fitness_center_outlined, color: OL.verde),
  Situation(id: 38, nombre: 'En la playa', categoria: 'Ocio', icono: Icons.beach_access_outlined, color: OL.naranja),
  Situation(id: 39, nombre: 'De vacaciones', categoria: 'Viajes', icono: Icons.luggage_outlined, color: OL.naranja),
  Situation(id: 40, nombre: 'En el cine', categoria: 'Ocio', icono: Icons.movie_outlined, color: OL.morado),
  Situation(id: 41, nombre: 'Hablando de música', categoria: 'Ocio', icono: Icons.music_note_outlined, color: OL.morado),
  Situation(id: 42, nombre: 'Hablando de películas y series', categoria: 'Ocio', icono: Icons.live_tv_outlined, color: OL.morado),
  Situation(id: 43, nombre: 'Hablando sobre la familia', categoria: 'Social', icono: Icons.family_restroom_outlined, color: OL.rojo),
  Situation(id: 44, nombre: 'Conociendo a una persona nueva', categoria: 'Social', icono: Icons.waving_hand_outlined, color: OL.rojo),
  Situation(id: 45, nombre: 'Conversaciones sociales y relaciones', categoria: 'Social', icono: Icons.favorite_outline, color: OL.rojo),
  Situation(id: 46, nombre: 'En una fiesta o celebración', categoria: 'Social', icono: Icons.celebration_outlined, color: OL.naranja),
  Situation(id: 47, nombre: 'En un cumpleaños o evento', categoria: 'Social', icono: Icons.cake_outlined, color: OL.naranja),
  Situation(id: 48, nombre: 'Cocinando y hablando de comida', categoria: 'Comida', icono: Icons.soup_kitchen_outlined, color: OL.morado),
  Situation(id: 49, nombre: 'Tareas de la casa y vida cotidiana', categoria: 'Hogar', icono: Icons.cleaning_services_outlined, color: OL.verde),
  Situation(id: 50, nombre: 'Conversación libre sobre cualquier tema', categoria: 'Libre', icono: Icons.forum_outlined, color: OL.morado),
];

Situation situacion(int id) => situaciones[id - 1];
