import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';
import 'widgets.dart';

/// Idiomas que aún no tienen ruta nueva (ja, ko, ru, zh): en lugar de las
/// lecciones antiguas, el curso aparece «En preparación». El tutor IA, las
/// situaciones y la práctica siguen disponibles.
class TarjetaEnPreparacion extends StatelessWidget {
  const TarjetaEnPreparacion({super.key, required this.idioma});

  /// Nombre del idioma que estudia el alumno.
  final String idioma;

  @override
  Widget build(BuildContext context) {
    return Tarjeta(
      color: OL.moradoSuave,
      sombra: false,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const IconoCuadro(Icons.construction_rounded),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  tr('En preparación'),
                  style: const TextStyle(
                    color: OL.morado,
                    fontSize: 18,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  tr(
                    'Estamos preparando tu curso de {idioma}. Mientras tanto, practica conversación con tu tutor y las situaciones.',
                    {'idioma': idioma},
                  ),
                  style: const TextStyle(color: OL.gris, height: 1.35),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
