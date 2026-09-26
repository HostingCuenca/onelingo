/// Fotos con licencia libre (CC0 / CC BY, ver assets/img/fotos/CREDITOS.md)
/// asociadas a situaciones, unidades, tutores y actividades diarias.
library;

import 'package:flutter/painting.dart';

const _base = 'assets/img/fotos/';

String? fotoSituacion(int id) {
  const m = <int, String>{
    1: 'restaurante', 2: 'cafeteria', 3: 'supermercado', 4: 'tienda-ropa', 5: 'tienda-ropa',
    6: 'tienda-ropa', 7: 'aeropuerto', 8: 'aeropuerto', 9: 'aeropuerto', 10: 'hotel',
    11: 'taxi', 12: 'taxi', 13: 'taxi', 14: 'taxi', 15: 'medico', 16: 'farmacia', 17: 'medico',
    18: 'banco', 19: 'supermercado', 20: 'entrevista', 21: 'oficina', 22: 'entrevista',
    23: 'oficina', 24: 'telefono', 25: 'telefono', 26: 'apartamento', 27: 'apartamento',
    28: 'apartamento', 29: 'policia', 30: 'ciudad', 31: 'autobus', 32: 'tren', 33: 'direcciones',
    34: 'escuela', 35: 'escuela', 36: 'ejercicio', 37: 'gimnasio', 38: 'playa', 39: 'playa',
    40: 'cine', 41: 'fiesta', 42: 'cine', 43: 'familia', 44: 'saludo', 45: 'saludo', 46: 'fiesta',
    47: 'fiesta', 48: 'cocina', 49: 'cocina', 50: 'ciudad',
  };
  final n = m[id];
  return n == null ? null : '$_base$n.jpg';
}

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
