import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';

/// Romanización bajo el texto en el idioma meta (ru, ko, ja, zh).
/// Convención y regla didáctica: docs/claude-educacion/ROMANIZACION.md.

/// N1–N2 (y Fundamentos) muestran la romanización; desde N3 se oculta y el
/// alumno la abre con un toque ([BotonRomanizacion]).
bool romVisiblePorDefecto(int? nivelInterno) =>
    nivelInterno == null || nivelInterno <= 2;

/// Línea pequeña y gris con la romanización (nada si [rom] es null).
class TextoRom extends StatelessWidget {
  const TextoRom(
    this.rom, {
    super.key,
    this.tamano = 14,
    this.alineacion,
    this.color,
  });
  final String? rom;
  final double tamano;
  final TextAlign? alineacion;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    final r = rom;
    if (r == null || r.trim().isEmpty) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.only(top: 2),
      child: Text(
        r,
        textAlign: alineacion,
        style: TextStyle(
          color: color ?? OL.gris,
          fontSize: tamano,
          fontWeight: FontWeight.w500,
          height: 1.25,
        ),
      ),
    );
  }
}

/// Muestra u oculta la romanización (desde N3, donde va oculta por defecto).
class BotonRomanizacion extends StatelessWidget {
  const BotonRomanizacion({
    super.key,
    required this.visible,
    required this.onPressed,
  });
  final bool visible;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) => Align(
    alignment: Alignment.centerLeft,
    child: TextButton.icon(
      onPressed: onPressed,
      icon: Icon(
        visible ? Icons.visibility_off_outlined : Icons.translate_rounded,
        size: 18,
      ),
      label: Text(
        visible ? tr('Ocultar romanización') : tr('Ver romanización'),
      ),
    ),
  );
}
