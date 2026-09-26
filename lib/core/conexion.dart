import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import 'api/sync.dart';

/// Comprueba nuestro servidor, sin inferir que todo Internet está caído.
enum EstadoConexion {
  comprobando,
  disponible,
  sinConexion,
  servicioNoDisponible,
}

class Conexion {
  static final estado = ValueNotifier(EstadoConexion.comprobando);
  static bool _comprobando = false;
  static Future<void> comprobar() async {
    if (_comprobando) return;
    _comprobando = true;
    try {
      final r = await http
          .get(Uri.parse('${Sync.baseUrl}/salud'))
          .timeout(const Duration(seconds: 5));
      estado.value = r.statusCode == 200
          ? EstadoConexion.disponible
          : EstadoConexion.servicioNoDisponible;
    } catch (_) {
      estado.value = EstadoConexion.sinConexion;
    } finally {
      _comprobando = false;
    }
  }
}
