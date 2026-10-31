import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';

/// Páginas públicas de la web (`web/privacidad`, `web/terminos`,
/// `web/eliminar-cuenta`): se leen sin iniciar sesión.
const urlPrivacidad = 'https://onelingo.org/privacidad/';
const urlTerminos = 'https://onelingo.org/terminos/';
const urlEliminarCuenta = 'https://onelingo.org/eliminar-cuenta/';

/// Abre una página legal en el navegador (pestaña nueva en la web). Con la
/// interfaz en otro idioma va directo a la versión en inglés (`#en`).
Future<bool> abrirPaginaLegal(String url) async {
  final destino = I18n.idioma.value == 'es' ? url : '$url#en';
  try {
    return await launchUrl(
      Uri.parse(destino),
      mode: LaunchMode.externalApplication,
    );
  } catch (_) {
    return false;
  }
}

/// «Términos» y «Política de privacidad». En el registro, con el aviso de que
/// crear la cuenta los acepta.
class EnlacesLegales extends StatelessWidget {
  const EnlacesLegales({super.key, this.registro = false});
  final bool registro;

  @override
  Widget build(BuildContext context) {
    const estilo = TextStyle(
      color: OL.morado,
      fontSize: 13,
      fontWeight: FontWeight.w700,
      decoration: TextDecoration.underline,
      decorationColor: OL.morado,
    );
    final denso = TextButton.styleFrom(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      minimumSize: const Size(0, 36),
      tapTargetSize: MaterialTapTargetSize.shrinkWrap,
    );
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (registro)
          Text(
            tr(
              'Al crear tu cuenta aceptas los Términos y la Política de privacidad.',
            ),
            textAlign: TextAlign.center,
            style: const TextStyle(color: OL.gris, fontSize: 12),
          ),
        Wrap(
          alignment: WrapAlignment.center,
          children: [
            TextButton(
              style: denso,
              onPressed: () => abrirPaginaLegal(urlTerminos),
              child: Text(tr('Términos'), style: estilo),
            ),
            TextButton(
              style: denso,
              onPressed: () => abrirPaginaLegal(urlPrivacidad),
              child: Text(tr('Política de privacidad'), style: estilo),
            ),
          ],
        ),
      ],
    );
  }
}
