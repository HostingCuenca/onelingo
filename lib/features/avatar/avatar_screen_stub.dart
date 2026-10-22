import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:record/record.dart';
import 'package:webview_flutter/webview_flutter.dart';
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

class _AvatarScreenState extends ConsumerState<AvatarScreen> {
  WebViewController? _web;
  String? _error;

  @override
  void initState() {
    super.initState();
    if (Sync.instancia.token != null) _abrir();
  }

  Future<void> _abrir() async {
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
        onWebResourceError: (e) {
          if (e.isForMainFrame == true && mounted) {
            setState(() => _error = e.description);
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
    if (mounted) setState(() => _web = c);
  }

  void _mensaje(JavaScriptMessage m) {
    final c = _web;
    if (m.message == 'onelingo-avatar-salir') {
      if (mounted) context.canPop() ? context.pop() : context.go('/tutores');
      return;
    }
    if (m.message != 'onelingo-avatar-ready' || c == null) return;
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
