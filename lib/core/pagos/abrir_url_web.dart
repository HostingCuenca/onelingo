import 'package:web/web.dart' as web;

/// Web: Stripe Checkout y el portal se abren en la misma pestaña; Stripe
/// vuelve a `<urlApp>/#/pago?estado=…` (ruta `/pago`).
Future<bool> abrirUrlPago(String url) async {
  web.window.location.href = url;
  return true;
}
