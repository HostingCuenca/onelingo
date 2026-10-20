import 'package:url_launcher/url_launcher.dart';

/// Android/iOS: Stripe Checkout y el portal se abren en el navegador externo.
/// Al volver a la app se refresca la suscripción (ver `main.dart`).
Future<bool> abrirUrlPago(String url) async {
  try {
    return await launchUrl(
      Uri.parse(url),
      mode: LaunchMode.externalApplication,
    );
  } catch (_) {
    return false;
  }
}
