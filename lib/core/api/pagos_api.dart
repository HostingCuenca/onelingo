import 'dart:convert';

import 'package:http/http.dart' as http;

import '../i18n/i18n.dart';
import 'sync.dart';

/// Respuesta de una llamada de pagos: código HTTP (0 sin conexión) y cuerpo.
class RespuestaPago {
  const RespuestaPago(this.codigo, [this.cuerpo = const {}]);
  final int codigo;
  final Map<String, dynamic> cuerpo;

  bool get ok => codigo >= 200 && codigo < 300;
  String? get url => cuerpo['url'] as String?;

  /// Mensaje para el alumno cuando falla.
  String get error {
    if (codigo == 0) return tr('No se pudo conectar con el servidor');
    if (codigo == 409) {
      return tr('Ya tienes una suscripción activa. Cámbiala o cancélala en «Gestionar suscripción».');
    }
    if (codigo == 503) return tr('Los pagos no están disponibles por ahora.');
    final e = cuerpo['error'];
    return e is String && e.isNotEmpty
        ? e
        : tr('Error {codigo}', {'codigo': codigo});
  }
}

/// Cliente de las rutas de planes y pagos del backend (contrato de pagos).
/// Usa la URL y la sesión de [Sync]; el cliente HTTP se inyecta en pruebas.
class PagosApi {
  PagosApi({this.cliente});

  /// null: un cliente por llamada (y el de `http.runWithClient` si lo hay).
  final http.Client? cliente;

  Future<RespuestaPago> _pedir(
    String metodo,
    String ruta, {
    Map<String, dynamic>? cuerpo,
    bool auth = true,
  }) async {
    final c = cliente ?? http.Client();
    try {
      final req = http.Request(metodo, Uri.parse('${Sync.baseUrl}$ruta'));
      req.headers['accept'] = 'application/json';
      final token = Sync.instancia.token;
      if (auth && token != null) req.headers['authorization'] = 'Bearer $token';
      if (cuerpo != null) {
        req.headers['content-type'] = 'application/json';
        req.body = jsonEncode(cuerpo);
      }
      final r = await http.Response.fromStream(
        await c.send(req).timeout(const Duration(seconds: 12)),
      );
      Map<String, dynamic> j = const {};
      try {
        final d = r.body.isEmpty ? null : jsonDecode(r.body);
        if (d is Map<String, dynamic>) j = d;
      } catch (_) {}
      return RespuestaPago(r.statusCode, j);
    } catch (_) {
      return const RespuestaPago(0);
    } finally {
      if (cliente == null) c.close();
    }
  }

  /// `GET /planes` (pública). null si falla.
  Future<Map<String, dynamic>?> planes() async {
    final r = await _pedir('GET', '/planes', auth: false);
    return r.ok && r.cuerpo['planes'] is List ? r.cuerpo : null;
  }

  /// `GET /usuarios/me/suscripcion`. null sin sesión o si falla.
  Future<Map<String, dynamic>?> suscripcion() async {
    if (!Sync.instancia.conectado) return null;
    final r = await _pedir('GET', '/usuarios/me/suscripcion');
    return r.ok && r.cuerpo.containsKey('estado') ? r.cuerpo : null;
  }

  /// `POST /pagos/checkout` → `{url}` de Stripe Checkout.
  Future<RespuestaPago> checkout(String planId) =>
      _pedir('POST', '/pagos/checkout', cuerpo: {'planId': planId});

  /// `POST /pagos/confirmar` → mismo cuerpo que la suscripción.
  Future<RespuestaPago> confirmar(String sessionId) =>
      _pedir('POST', '/pagos/confirmar', cuerpo: {'sessionId': sessionId});

  /// `POST /pagos/portal` → `{url}` del Customer Portal.
  Future<RespuestaPago> portal() =>
      _pedir('POST', '/pagos/portal', cuerpo: const {});
}
