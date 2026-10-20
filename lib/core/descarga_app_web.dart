import 'dart:convert';
import 'dart:js_interop';

import 'package:web/web.dart' as web;

/// Descarga de la app Android desde la web. Rutas relativas al dominio: sirve
/// igual en cualquier dominio donde se publique la web.
const descargaAppDisponible = true;
const _apk = '/descargas/onelingo.apk';
const _version = '/descargas/version.json';

/// Abre el APK en una pestaña nueva.
void abrirDescargaApp() => web.window.open(_apk, '_blank', 'noopener');

/// `{"version": "0.2.0", "tamano_mb": 110}` o null si no se puede leer.
Future<Map<String, dynamic>?> leerVersionApp() async {
  try {
    final r = await web.window
        .fetch(_version.toJS, web.RequestInit(cache: 'no-cache'))
        .toDart;
    if (!r.ok) return null;
    final j = jsonDecode((await r.text().toDart).toDart);
    return j is Map<String, dynamic> ? j : null;
  } catch (_) {
    return null;
  }
}
