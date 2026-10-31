import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:record/record.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:wakelock_plus/wakelock_plus.dart';
import 'package:webview_flutter_android/webview_flutter_android.dart';

import '../../core/api/sync.dart';
import '../../core/i18n/i18n.dart';
import '../../core/state/providers.dart';
import 'tutores_3d.dart';
import 'visor_datos.dart';

/// Visor de la videollamada en Android/iOS: la misma página que en la web
/// (web/avatar), dentro de un WebView. La sesión se entrega por mensaje
/// (canal `OneLingo`), nunca en la URL.
///
/// URL del visor: `--dart-define=AVATAR_URL=...`; si no, la del servidor de
/// la API (`https://onelingo.org/api` → `https://onelingo.org/avatar/…`).
Uri urlVisor(String tutorId) {
  const definida = String.fromEnvironment('AVATAR_URL');
  final api = Uri.parse(Sync.baseUrl);
  final base = definida.isNotEmpty
      ? Uri.parse(definida)
      : api.path.endsWith('/api')
      ? api.replace(path: '/avatar/index.html')
      : Uri.parse('https://onelingo.org/avatar/index.html');
  return base.replace(
    queryParameters: {'v': 'avatar31', 'embebido': '1', 'tutor': tutorId},
  );
}

class AvatarScreen extends ConsumerStatefulWidget {
  const AvatarScreen({
    super.key,
    required this.tutorId,
    this.tema,
    this.objetivoId,
  });
  final String tutorId;
  final int? tema;
  final String? objetivoId;

  @override
  ConsumerState<AvatarScreen> createState() => _AvatarScreenState();
}

class _AvatarScreenState extends ConsumerState<AvatarScreen>
    with WidgetsBindingObserver {
  WebViewController? _web;
  String? _error;
  bool _abriendo = false;
  // Si la página no avisa que está lista (falló un script, un 502 de nginx),
  // se muestra «Reintentar» en vez de una pantalla en blanco para siempre.
  Timer? _vigiaCarga;
  // La pantalla sigue montada en otra pestaña (IndexedStack) o con la app en
  // segundo plano: la llamada se pausa y no se mantiene la pantalla encendida.
  bool _visible = true, _enPrimerPlano = true, _pausada = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    if (Sync.instancia.token != null) _abrir();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final visible = TickerMode.valuesOf(context).enabled;
    if (visible != _visible) {
      _visible = visible;
      _actualizarPausa();
    }
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState estado) {
    // «inactive» (cortina de notificaciones, diálogo del sistema) no pausa.
    final primerPlano = estado == AppLifecycleState.resumed
        ? true
        : estado == AppLifecycleState.inactive
        ? _enPrimerPlano
        : false;
    if (primerPlano != _enPrimerPlano) {
      _enPrimerPlano = primerPlano;
      _actualizarPausa();
    }
  }

  void _actualizarPausa() {
    final pausar = !(_visible && _enPrimerPlano);
    // En vivo se habla sin tocar la pantalla: si se apagaba, se cortaba la llamada.
    WakelockPlus.toggle(enable: !pausar).catchError((_) {});
    if (pausar == _pausada) return;
    _pausada = pausar;
    _web
        ?.runJavaScript(
          pausar ? 'window.onelingoPausa?.()' : 'window.onelingoReanudar?.()',
        )
        .catchError((_) {});
  }

  Future<void> _abrir() async {
    if (_abriendo) return;
    _abriendo = true;
    try {
      await _crearVisor();
    } catch (e) {
      if (mounted) setState(() => _error = '$e');
    } finally {
      _abriendo = false;
    }
  }

  Future<void> _crearVisor() async {
    // El WebView solo puede dar el micrófono si la app ya tiene el permiso.
    final grabadora = AudioRecorder();
    try {
      await grabadora.hasPermission();
    } catch (_) {
      // Sin micrófono la llamada sigue: se puede escribir.
    } finally {
      await grabadora.dispose();
    }
    final c = WebViewController(
      onPermissionRequest: (p) =>
          p.types.contains(WebViewPermissionResourceType.microphone)
          ? p.grant()
          : p.deny(),
    );
    await c.setJavaScriptMode(JavaScriptMode.unrestricted);
    await c.setBackgroundColor(Colors.white);
    await c.addJavaScriptChannel('OneLingo', onMessageReceived: _mensaje);
    await c.setNavigationDelegate(
      NavigationDelegate(
        // Solo el visor: otra página que cargara aquí recibiría la sesión.
        onNavigationRequest: (r) {
          final u = Uri.tryParse(r.url);
          final visor = urlVisor(widget.tutorId);
          return u != null &&
                  (r.url == 'about:blank' || u.origin == visor.origin)
              ? NavigationDecision.navigate
              : NavigationDecision.prevent;
        },
        onWebResourceError: (e) {
          if (e.isForMainFrame == true && mounted) {
            setState(() => _error = e.description);
          }
        },
        onHttpError: (e) {
          final url = e.request?.uri;
          if (url != null &&
              url.path == urlVisor(widget.tutorId).path &&
              mounted) {
            setState(() => _error = 'HTTP ${e.response?.statusCode}');
          }
        },
      ),
    );
    final android = c.platform;
    if (android is AndroidWebViewController) {
      // El tutor empieza a hablar solo, como una llamada real.
      await android.setMediaPlaybackRequiresUserGesture(false);
    }
    await c.loadRequest(urlVisor(widget.tutorId));
    _vigiaCarga?.cancel();
    // Con 3G lento la página (three.js incluido) puede tardar: 30 s de margen.
    _vigiaCarga = Timer(const Duration(seconds: 30), () {
      if (mounted && _error == null) {
        setState(() => _error = 'La página no respondió');
      }
    });
    if (mounted) setState(() => _web = c);
    _actualizarPausa();
  }

  /// El visor no pudo abrir el micrófono: se pide el permiso de Android (si ya
  /// se negó para siempre no sale el diálogo y el visor indica Ajustes).
  Future<void> _pedirMicrofono() async {
    final grabadora = AudioRecorder();
    var ok = false;
    try {
      ok = await grabadora.hasPermission();
    } catch (_) {
      ok = false;
    } finally {
      await grabadora.dispose();
    }
    await _web?.runJavaScript('window.onelingoMicrofono?.($ok)');
  }

  void _mensaje(JavaScriptMessage m) {
    final c = _web;
    if (m.message == 'onelingo-avatar-salir') {
      if (mounted) context.canPop() ? context.pop() : context.go('/tutores');
      return;
    }
    if (m.message == 'onelingo-avatar-permiso-microfono') {
      _pedirMicrofono();
      return;
    }
    if (m.message != 'onelingo-avatar-ready' || c == null) return;
    _vigiaCarga?.cancel();
    final datos = datosVisor(
      ref.read(progressProvider),
      tema: widget.tema,
      objetivoId: widget.objetivoId,
    );
    // jsonEncode de un String ya es un literal JS seguro.
    c.runJavaScript(
      'window.postMessage(${jsonEncode(datos)}, location.origin);',
    );
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _vigiaCarga?.cancel();
    WakelockPlus.disable().catchError((_) {});
    _web?.loadRequest(Uri.parse('about:blank'));
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final nombre = tutor3d(widget.tutorId)?.nombre ?? tr('Tutor');
    if (Sync.instancia.token == null || _error != null) {
      return Scaffold(
        appBar: AppBar(
          title: Text(tr('{tutor} · videollamada', {'tutor': nombre})),
        ),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  _error == null
                      ? tr('Inicia sesión para hablar con {nombre}', {
                          'nombre': nombre,
                        })
                      : tr(
                          'No se pudo abrir la videollamada. Revisa tu conexión.',
                        ),
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 16),
                FilledButton(
                  onPressed: () {
                    if (_error == null) {
                      context.push('/login');
                      return;
                    }
                    setState(() {
                      _error = null;
                      _web = null;
                      _pausada = false;
                    });
                    _abrir();
                  },
                  child: Text(
                    _error == null ? tr('Iniciar sesión') : tr('Reintentar'),
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    }
    final c = _web;
    // Inició sesión después de abrir esta pantalla: la llamada se abre ahora.
    if (c == null && !_abriendo) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted && _web == null) _abrir();
      });
    }
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        bottom: false,
        child: c == null
            ? const Center(child: CircularProgressIndicator())
            : WebViewWidget(controller: c),
      ),
    );
  }
}
