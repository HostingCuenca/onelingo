import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/nivel0/nivel0.dart';
import '../../core/voz.dart';

/// Palabra con cada vocal pintada del color de su sonido (Mapa de Sonidos):
/// las letras mudas y la e mágica se ven tenues, las dos letras con un solo
/// sonido van subrayadas juntas y la vocal fantasma lleva un punteado gris.
class PalabraColor extends StatelessWidget {
  const PalabraColor(
    this.marcado, {
    super.key,
    required this.nivel,
    this.tamano = 34,
    this.centrar = true,
  });
  final String marcado;
  final Nivel0 nivel;
  final double tamano;
  final bool centrar;

  @override
  Widget build(BuildContext context) {
    final base = TextStyle(
      fontSize: tamano,
      fontWeight: FontWeight.w800,
      color: OL.texto,
      height: 1.25,
      letterSpacing: tamano > 30 ? 1.5 : 0.5,
    );
    return Text.rich(
      TextSpan(
        children: [
          for (final s in segmentos(marcado))
            TextSpan(text: s.texto, style: estiloSegmento(s, base, nivel)),
        ],
      ),
      textAlign: centrar ? TextAlign.center : TextAlign.start,
    );
  }
}

TextStyle estiloSegmento(Segmento s, TextStyle base, Nivel0 nivel) {
  if (s.muda || s.magica) {
    return base.copyWith(color: OL.gris.withValues(alpha: .45));
  }
  if (s.digrafo) {
    return base.copyWith(
      decoration: TextDecoration.underline,
      decorationThickness: 3,
      decorationColor: OL.texto,
    );
  }
  final sonido = s.sonido == null ? null : nivel.porId[s.sonido];
  if (sonido == null) return base;
  if (sonido.grupo == 'fantasma') {
    return base.copyWith(
      color: OL.gris,
      decoration: TextDecoration.underline,
      decorationStyle: TextDecorationStyle.dashed,
      decorationColor: OL.gris,
      decorationThickness: 2,
    );
  }
  return base.copyWith(
    color: sonido.color,
    fontWeight: FontWeight.w900,
    // Vocales con R: subrayado del mismo color (la «r» se pronuncia).
    decoration: sonido.grupo == 'r' ? TextDecoration.underline : null,
    decorationColor: sonido.color,
    decorationThickness: 2.5,
  );
}

/// Imagen de la palabra (emoji Noto) o un hueco si no tiene.
class ImagenPalabra extends StatelessWidget {
  const ImagenPalabra(this.emoji, {super.key, this.tamano = 64});
  final String? emoji;
  final double tamano;

  @override
  Widget build(BuildContext context) => emoji == null
      ? SizedBox(width: tamano, height: tamano)
      : Image.asset(
          rutaEmoji(emoji!),
          width: tamano,
          height: tamano,
          excludeFromSemantics: true,
          errorBuilder: (_, _, _) => SizedBox(width: tamano, height: tamano),
        );
}

/// Pronuncia en la voz del Nivel 0 de su idioma. `lento` = versión
/// tortuga. Las letras sueltas van con la voz del sistema (la voz en la nube
/// las lee como sonido, no como nombre).
Future<void> decir(
  Nivel0 n,
  String texto, {
  bool lento = false,
  bool letra = false,
}) => Voz.instancia.hablar(
  texto.replaceAll(enlace, ' '),
  n.idioma,
  voz: n.voz,
  velocidad: lento ? 0.4 : null,
  sistema: letra,
);
