import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/nivel0/nivel0.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import 'palabra_color.dart';

/// Acceso al Nivel 0 · Leer y pronunciar en Aprender (inglés). Sin personaje:
/// la pantalla ya tiene su mascota y nunca debe haber dos a la vez.
class TarjetaNivel0 extends ConsumerWidget {
  const TarjetaNivel0({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final nivel = ref.watch(nivel0Provider).valueOrNull;
    final practicas = ref.watch(progressProvider).practicas;
    if (nivel == null) return const SizedBox.shrink();
    final hechas = nivel.lecciones
        .where((l) => leccionN0Completa(practicas, nivel.idioma, l.id))
        .length;
    final total = nivel.lecciones.length;
    return Semantics(
      button: true,
      label: 'Nivel 0, leer y pronunciar',
      child: Tarjeta(
        onTap: () => context.push('/nivel0'),
        borde: OL.moradoClaro,
        child: Row(
          children: [
            ImagenPalabra(nivel.texto('emoji'), tamano: 54),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Nivel 0 · Leer y pronunciar',
                    style: TextStyle(fontSize: 17, fontWeight: FontWeight.w900),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    hechas == 0
                        ? nivel.texto('tarjeta')
                        : '$hechas de $total lecciones',
                    style: const TextStyle(
                      color: OL.gris,
                      fontSize: 13,
                      height: 1.3,
                    ),
                  ),
                  const SizedBox(height: 6),
                  PalabraColor(
                    nivel.texto('muestra'),
                    nivel: nivel,
                    tamano: 18,
                    centrar: false,
                  ),
                ],
              ),
            ),
            const Icon(Icons.chevron_right_rounded, color: OL.gris),
          ],
        ),
      ),
    );
  }
}
