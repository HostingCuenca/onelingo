import 'dart:async';
import 'dart:convert';
import 'dart:io' show Platform;

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart' show MediaType;
import 'package:shared_preferences/shared_preferences.dart';

/// Cliente mínimo del backend (onelingo-backend). Offline-first: el estado vive
/// en el dispositivo y se sube en segundo plano; si el servidor no responde, no
/// afecta a la app.
class Sync {
  Sync._();
  static final Sync instancia = Sync._();

  static const _kToken = 'onelingo.api.token';
  static const _kUsuario = 'onelingo.api.usuarioId';
  static const _kEmail = 'onelingo.api.email';

  SharedPreferences? _prefs;
  Timer? _debounce;
  Map<String, dynamic>? _pendiente;
  bool _enviando = false;
  String? _usuarioPendiente;

  /// URL del backend: `--dart-define=API_URL=...`; por defecto localhost:8091
  /// (simulador iOS y web) o 10.0.2.2 en el emulador Android.
  static String get baseUrl {
    const definida = String.fromEnvironment('API_URL');
    if (definida.isNotEmpty) return definida;
    if (!kIsWeb && Platform.isAndroid) return 'http://10.0.2.2:8091';
    return 'http://localhost:8091';
  }

  void inicializar(SharedPreferences p) {
    _prefs = p;
    _recuperarPendiente();
  }

  void _recuperarPendiente() {
    if (usuarioId == null) return;
    final raw = _prefs?.getString('onelingo.pending.$usuarioId');
    if (raw != null) {
      try {
        subir(jsonDecode(raw) as Map<String, dynamic>);
      } catch (_) {
        /* formato antiguo */
      }
    }
  }

  String? get token => _prefs?.getString(_kToken);
  String? get usuarioId => _prefs?.getString(_kUsuario);
  String? get email => _prefs?.getString(_kEmail);
  bool get conectado => token != null;

  String get _plataforma => kIsWeb ? 'web' : Platform.operatingSystem;

  Future<Map<String, dynamic>?> _post(
    String ruta,
    Map<String, dynamic> cuerpo, {
    bool auth = false,
  }) async {
    try {
      final r = await http
          .post(
            Uri.parse('$baseUrl$ruta'),
            headers: {
              'content-type': 'application/json',
              if (auth && token != null) 'authorization': 'Bearer $token',
            },
            body: jsonEncode(cuerpo),
          )
          .timeout(const Duration(seconds: 8));
      if (r.statusCode >= 200 && r.statusCode < 300)
        return jsonDecode(r.body) as Map<String, dynamic>;
    } catch (_) {}
    return null;
  }

  /// Resultado de una autenticación: sesión guardada y, si el servidor lo tenía, el progreso.
  Map<String, dynamic>? ultimoEstadoServidor;
  String ultimoError = '';

  Future<Map<String, dynamic>?> _postConError(
    String ruta,
    Map<String, dynamic> cuerpo,
  ) async {
    ultimoError = '';
    try {
      final r = await http
          .post(
            Uri.parse('$baseUrl$ruta'),
            headers: {'content-type': 'application/json'},
            body: jsonEncode(cuerpo),
          )
          .timeout(const Duration(seconds: 10));
      final j = r.body.isEmpty
          ? <String, dynamic>{}
          : jsonDecode(r.body) as Map<String, dynamic>;
      if (r.statusCode >= 200 && r.statusCode < 300) return j;
      ultimoError = (j['error'] ?? 'Error ${r.statusCode}').toString();
    } catch (_) {
      ultimoError = 'No se pudo conectar con el servidor';
    }
    return null;
  }

  /// Registro real con contraseña. Devuelve null y deja `ultimoError` si falla.
  Future<bool> registrarConPassword({
    required String email,
    required String password,
    required String nombre,
    required String idiomaNativo,
    required String idiomaMeta,
    required int nivelInicial,
  }) async {
    final r = await _postConError('/auth/registro', {
      'email': email,
      'password': password,
      'nombre': nombre,
      'idiomaNativo': idiomaNativo,
      'idiomaMeta': idiomaMeta,
      'nivelInicial': nivelInicial,
      'plataforma': _plataforma,
    });
    if (r == null) return false;
    await _guardarSesion(r, email);
    return true;
  }

  /// Inicio de sesión real. Si el servidor tiene progreso, queda en `ultimoEstadoServidor`.
  Future<bool> loginConPassword(String email, String password) async {
    final r = await _postConError('/auth/login', {
      'email': email,
      'password': password,
    });
    if (r == null) return false;
    await _guardarSesion(r, email);
    ultimoEstadoServidor = r['estado'] as Map<String, dynamic>?;
    return true;
  }

  /// Inicio de sesión con Google (idToken obtenido en el dispositivo).
  Future<Map<String, dynamic>?> loginConGoogle(
    String idToken, {
    required String idiomaNativo,
    required String idiomaMeta,
    required int nivelInicial,
  }) async {
    final r = await _postConError('/auth/google', {
      'idToken': idToken,
      'idiomaNativo': idiomaNativo,
      'idiomaMeta': idiomaMeta,
      'nivelInicial': nivelInicial,
      'plataforma': _plataforma,
    });
    if (r == null) return null;
    await _guardarSesion(r, r['email'] as String? ?? '');
    ultimoEstadoServidor = r['estado'] as Map<String, dynamic>?;
    return r;
  }

  Future<String?> recuperarPassword(String email) async {
    final r = await _postConError('/auth/recuperar', {'email': email});
    return r?['mensaje'] as String?;
  }

  /// Respuesta del tutor con IA real; null si el servidor no tiene IA o falla (la app usa el simulador).
  Future<Map<String, dynamic>?> chat({
    required String idiomaMeta,
    required String idiomaNativo,
    required int nivel,
    required String tutorId,
    int? situacionId,
    String? situacion,
    String? objetivo,
    String? objetivoId,
    String modo = 'practica',
    required List<Map<String, String>> historial,
    void Function(String)? onReply,
    http.Client? client,
  }) async {
    if (!conectado) return null;
    final transport = client ?? http.Client();
    final deadline = Timer(const Duration(seconds: 40), transport.close);
    try {
      final req = http.Request('POST', Uri.parse('$baseUrl/chat'))
        ..headers.addAll({
          'content-type': 'application/json',
          'authorization': 'Bearer $token',
          if (onReply != null) 'accept': 'text/event-stream',
        })
        ..body = jsonEncode({
          'idiomaMeta': idiomaMeta,
          'idiomaNativo': idiomaNativo,
          'nivel': nivel,
          'tutorId': tutorId,
          'situacionId': ?situacionId,
          'situacion': ?situacion,
          'objetivo': ?objetivo,
          'objetivoId': ?objetivoId,
          'modo': modo,
          'historial': historial
              .skip(historial.length > 30 ? historial.length - 30 : 0)
              .toList(),
        });
      final response = await transport
          .send(req)
          .timeout(const Duration(seconds: 40));
      if (response.statusCode != 200) return null;
      if (!(response.headers['content-type'] ?? '').contains(
        'text/event-stream',
      )) {
        return jsonDecode(await response.stream.bytesToString())
            as Map<String, dynamic>;
      }
      await for (final line
          in response.stream
              .transform(utf8.decoder)
              .transform(const LineSplitter())) {
        if (!line.startsWith('data:')) continue;
        final event =
            jsonDecode(line.substring(5).trim()) as Map<String, dynamic>;
        if (event['tipo'] == 'reply') onReply?.call(event['data'] as String);
        if (event['tipo'] == 'final')
          return event['data'] as Map<String, dynamic>;
        if (event['tipo'] == 'error') return null;
      }
    } catch (_) {
      /* La interfaz conserva el mensaje y permite reintentar. */
    } finally {
      deadline.cancel();
      transport.close();
    }
    return null;
  }

  /// Pregunta de diagnóstico redactada por la IA para el nivel, competencia y tipo pedidos. null si falla.
  Future<Map<String, dynamic>?> generarPreguntaDiag(
    Map<String, dynamic> peticion,
  ) async {
    if (!conectado) return null;
    try {
      final r = await http
          .post(
            Uri.parse('$baseUrl/diagnostico/pregunta'),
            headers: {
              'content-type': 'application/json',
              'authorization': 'Bearer $token',
            },
            body: jsonEncode(peticion),
          )
          .timeout(const Duration(seconds: 75));
      if (r.statusCode == 200)
        return jsonDecode(r.body) as Map<String, dynamic>;
    } catch (_) {}
    return null;
  }

  /// Resumen narrativo y plan del diagnóstico redactados por la IA. null si falla.
  Future<Map<String, dynamic>?> perfilDiag({
    required String idiomaMeta,
    required String idiomaNativo,
    required Map<String, dynamic> resultado,
  }) async {
    if (!conectado) return null;
    try {
      final r = await http
          .post(
            Uri.parse('$baseUrl/diagnostico/perfil'),
            headers: {
              'content-type': 'application/json',
              'authorization': 'Bearer $token',
            },
            body: jsonEncode({
              'idiomaMeta': idiomaMeta,
              'idiomaNativo': idiomaNativo,
              'resultado': resultado,
            }),
          )
          .timeout(const Duration(seconds: 40));
      if (r.statusCode == 200)
        return jsonDecode(r.body) as Map<String, dynamic>;
    } catch (_) {}
    return null;
  }

  /// Evaluación de la producción escrita del diagnóstico (IA del servidor). null si falla.
  Future<Map<String, dynamic>?> evaluarEscritura({
    required String idiomaMeta,
    required String idiomaNativo,
    required double nivelEstimado,
    required String consigna,
    required String texto,
  }) async {
    if (!conectado) return null;
    try {
      final r = await http
          .post(
            Uri.parse('$baseUrl/diagnostico/escritura'),
            headers: {
              'content-type': 'application/json',
              'authorization': 'Bearer $token',
            },
            body: jsonEncode({
              'idiomaMeta': idiomaMeta,
              'idiomaNativo': idiomaNativo,
              'nivelEstimado': nivelEstimado,
              'consigna': consigna,
              'texto': texto,
            }),
          )
          .timeout(const Duration(seconds: 45));
      if (r.statusCode == 200)
        return jsonDecode(r.body) as Map<String, dynamic>;
    } catch (_) {}
    return null;
  }

  /// Voz del alumno → texto con la IA del servidor (OpenAI). null si falla.
  Future<String?> transcribir(
    List<int> audio,
    String idioma, {
    String nombre = 'voz.m4a',
    String tipo = 'audio/m4a',
  }) async {
    if (!conectado) return null;
    try {
      final req =
          http.MultipartRequest('POST', Uri.parse('$baseUrl/transcribir'))
            ..headers['authorization'] = 'Bearer $token'
            ..fields['idioma'] = idioma
            ..files.add(
              http.MultipartFile.fromBytes(
                'audio',
                audio,
                filename: nombre,
                contentType: MediaType.parse(tipo),
              ),
            );
      final r = await http.Response.fromStream(
        await req.send().timeout(const Duration(seconds: 30)),
      );
      if (r.statusCode == 200)
        return (jsonDecode(r.body) as Map<String, dynamic>)['texto'] as String?;
      ultimoError = 'transcripcion ${r.statusCode}';
    } catch (e) {
      ultimoError = '$e';
    }
    return null;
  }

  Future<void> _guardarSesion(Map<String, dynamic> r, String email) async {
    _debounce?.cancel();
    _pendiente = null;
    await _prefs?.setString(_kToken, r['token'] as String);
    await _prefs?.setString(_kUsuario, r['id'] as String);
    await _prefs?.setString(_kEmail, email);
    _recuperarPendiente();
  }

  /// Registro (o reactivación) de la cuenta en el servidor.
  Future<bool> registrar({
    required String email,
    required String nombre,
    required String idiomaNativo,
    required String idiomaMeta,
    required int nivelInicial,
  }) async {
    final r = await _post('/usuarios/registro', {
      'email': email,
      'nombre': nombre,
      'idiomaNativo': idiomaNativo,
      'idiomaMeta': idiomaMeta,
      'nivelInicial': nivelInicial,
      'plataforma': _plataforma,
    });
    if (r == null) return false;
    await _guardarSesion(r, email);
    return true;
  }

  /// Inicio de sesión por correo (demo). Si el usuario no existe en el servidor lo crea.
  Future<bool> login({
    required String email,
    required String nombre,
    required String idiomaNativo,
    required String idiomaMeta,
    required int nivelInicial,
  }) async {
    final r = await _post('/usuarios/login', {'email': email});
    if (r != null) {
      await _guardarSesion(r, email);
      return true;
    }
    return registrar(
      email: email,
      nombre: nombre,
      idiomaNativo: idiomaNativo,
      idiomaMeta: idiomaMeta,
      nivelInicial: nivelInicial,
    );
  }

  /// Conserva el último estado hasta que el servidor confirma el guardado.
  /// La cola persistente pertenece al usuario, nunca a una sesión distinta.
  void subir(Map<String, dynamic> estado) {
    if (!conectado || usuarioId == null) return;
    _pendiente = estado;
    _usuarioPendiente = usuarioId;
    _prefs?.setString('onelingo.pending.$usuarioId', jsonEncode(estado));
    _debounce?.cancel();
    _debounce = Timer(const Duration(seconds: 2), _enviarPendiente);
  }

  Future<void> _enviarPendiente() async {
    if (_enviando ||
        _pendiente == null ||
        !conectado ||
        usuarioId != _usuarioPendiente)
      return;
    final e = _pendiente!;
    final id = usuarioId;
    final sesion = token;
    var reintentar = true;
    _enviando = true;
    try {
      final r = await http
          .put(
            Uri.parse('$baseUrl/usuarios/me/progreso'),
            headers: {
              'content-type': 'application/json',
              'authorization': 'Bearer $sesion',
            },
            body: jsonEncode(e),
          )
          .timeout(const Duration(seconds: 10));
      if (r.statusCode >= 200 &&
          r.statusCode < 300 &&
          id == usuarioId &&
          identical(e, _pendiente)) {
        _pendiente = null;
        await _prefs?.remove('onelingo.pending.$id');
      }
      if (r.statusCode == 401 || r.statusCode == 403) reintentar = false;
    } catch (_) {
      /* Se conserva para reintentar o recuperar al abrir la app. */
    } finally {
      _enviando = false;
      if (reintentar && _pendiente != null && conectado) {
        _debounce?.cancel();
        _debounce = Timer(const Duration(seconds: 5), _enviarPendiente);
      }
    }
  }

  Future<void> evento(
    String tipo, [
    Map<String, dynamic> datos = const {},
  ]) async {
    if (!conectado) return;
    await _post('/usuarios/me/eventos', {
      'tipo': tipo,
      'datos': datos,
    }, auth: true);
  }

  Future<void> cerrarSesion() async {
    _debounce?.cancel();
    _pendiente = null;
    _usuarioPendiente = null;
    await _prefs?.remove(_kToken);
    await _prefs?.remove(_kUsuario);
    await _prefs?.remove(_kEmail);
  }
}
