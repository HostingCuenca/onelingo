import 'package:flutter/material.dart';

import '../../app/theme.dart';

/// Ilustración cuadrada de una palabra (biblioteca de `core/lexico/imagenes.dart`).
/// Decorativa: la palabra ya está escrita al lado, así que el lector de
/// pantalla no la repite.
class ImagenVocab extends StatelessWidget {
  const ImagenVocab(this.ruta, {super.key, this.lado = 72, this.radio = 14});
  final String ruta;
  final double lado, radio;

  @override
  Widget build(BuildContext context) => ClipRRect(
    borderRadius: BorderRadius.circular(radio),
    child: Image.asset(
      ruta,
      width: lado,
      height: lado,
      fit: BoxFit.cover,
      cacheWidth: (lado * MediaQuery.devicePixelRatioOf(context)).round(),
      excludeFromSemantics: true,
      errorBuilder: (_, _, _) => SizedBox(
        width: lado,
        height: lado,
        child: const ColoredBox(color: OL.moradoSuave),
      ),
    ),
  );
}
