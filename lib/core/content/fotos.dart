/// Fotos con licencia libre (CC0 / CC BY, ver assets/img/fotos/CREDITOS.md)
/// asociadas a situaciones, unidades, tutores y actividades diarias.
library;

import 'package:flutter/painting.dart';

const _base = 'assets/img/fotos/';

/// Tarjeta de cada situación: su propia ilustración (escena 1). Antes eran 31
/// fotos genéricas para 50 situaciones y se repetían (taxi ×4, aeropuerto ×3…).
String? fotoSituacion(int id) => id >= 1 && id <= 50
    ? 'assets/img/situaciones/situacion-${id.toString().padLeft(2, '0')}-1.webp'
    : null;

String? fotoUnidad(int nivel, int numero) {
  if (nivel != 1) return null;
  const m = <int, String>{
    1: 'saludo', 2: 'escuela', 4: 'banco', 6: 'estudiar', 7: 'familia', 8: 'apartamento',
    9: 'estudiar', 10: 'desayuno', 11: 'tienda-ropa', 12: 'gimnasio', 13: 'ciudad',
    16: 'ejercicio', 17: 'oficina', 18: 'telefono', 20: 'restaurante',
  };
  final n = m[numero];
  return n == null ? null : '$_base$n.jpg';
}

String fotoTutor(String id) => '${_base}tutor-$id.jpg';

/// Focal points measured from the existing photos; avoid cropping faces.
Alignment encuadreTutor(String id) => switch (id) {
  'sofia' => Alignment.centerLeft,
  'mia' => const Alignment(-.7, 0),
  'leo' => const Alignment(.55, 0),
  'max' => const Alignment(.35, 0),
  _ => Alignment.center,
};

String fotoActividad(String nombre) {
  const m = <String, String>{
    'Desayunar': 'desayuno', 'Caminar': 'caminar', 'Ir al trabajo': 'oficina',
    'Hacer ejercicio': 'ejercicio', 'Estudiar': 'estudiar', 'Dormir': 'dormir',
  };
  return '$_base${m[nombre] ?? 'ciudad'}.jpg';
}

/// Cuatro fotos para el ejercicio "elige la imagen" según la palabra objetivo.
List<(String, String)> opcionesImagen(String palabraCorrecta) {
  const banco = <String, String>{
    'Breakfast': 'desayuno', 'Family': 'familia', 'City': 'ciudad', 'Beach': 'playa',
    'Kitchen': 'cocina', 'School': 'escuela', 'Office': 'oficina', 'Restaurant': 'restaurante',
    'Hospital': 'medico', 'Airport': 'aeropuerto', 'Train': 'tren', 'Bus': 'autobus',
    'Coffee': 'cafeteria', 'Party': 'fiesta', 'Gym': 'gimnasio', 'Hotel': 'hotel',
  };
  final resto = banco.keys.where((k) => k != palabraCorrecta).toList()..shuffle();
  final elegidas = [palabraCorrecta, ...resto.take(3)]..shuffle();
  return [for (final k in elegidas) (k, '$_base${banco[k] ?? 'ciudad'}.jpg')];
}
