import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/descarga_app_stub.dart'
    if (dart.library.js_interop) '../../core/descarga_app_web.dart';
import '../../core/i18n/i18n.dart';

/// Enlace discreto «Descarga la app para Android» (solo en la web): abre
/// `/descargas/onelingo.apk` en una pestaña nueva y, si se puede leer
/// `/descargas/version.json`, muestra debajo la versión y el tamaño.
class DescargaAndroid extends StatefulWidget {
  const DescargaAndroid({super.key, this.sobreColor = false});

  /// Sobre el fondo morado de la bienvenida (texto claro).
  final bool sobreColor;

  @override
  State<DescargaAndroid> createState() => _DescargaAndroidState();
}

class _DescargaAndroidState extends State<DescargaAndroid> {
  Map<String, dynamic>? info;

  @override
  void initState() {
    super.initState();
    if (!descargaAppDisponible) return;
    leerVersionApp().then((j) {
      if (mounted && j != null) setState(() => info = j);
    });
  }

  String? get _detalle {
    final version = info?['version'];
    if (version is! String || version.isEmpty) return null;
    final mb = info?['tamano_mb'];
    return mb is num
        ? tr('Versión {version} · {mb} MB', {'version': version, 'mb': mb.round()})
        : tr('Versión {version}', {'version': version});
  }

  @override
  Widget build(BuildContext context) {
    if (!descargaAppDisponible) return const SizedBox.shrink();
    final color = widget.sobreColor ? OL.blanco : OL.morado;
    final detalle = _detalle;
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        TextButton.icon(
          onPressed: abrirDescargaApp,
          style: TextButton.styleFrom(foregroundColor: color),
          icon: const Icon(Icons.android_rounded, size: 20),
          label: Text(
            tr('Descarga la app para Android'),
            style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 13),
          ),
        ),
        if (detalle != null)
          Text(
            detalle,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: widget.sobreColor ? OL.moradoClaro : OL.gris,
              fontSize: 11,
            ),
          ),
      ],
    );
  }
}
