import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';
import '../../core/state/providers.dart';

/// Idioma de la app (I18N.md): en la bienvenida, el registro y Perfil. Cada
/// idioma aparece con su propio nombre para que cualquiera encuentre el suyo.
class SelectorIdiomaApp extends ConsumerWidget {
  const SelectorIdiomaApp({super.key, this.sobreColor = false});

  /// Sobre un fondo de color (bienvenida): fichas claras.
  final bool sobreColor;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final actual = ref.watch(progressProvider.select((s) => s.interfaz));
    return Semantics(
      label: tr('Idioma de la app'),
      child: Wrap(
        spacing: 8,
        runSpacing: 8,
        crossAxisAlignment: WrapCrossAlignment.center,
        children: [
          Icon(
            Icons.language_rounded,
            size: 20,
            color: sobreColor ? OL.moradoClaro : OL.gris,
          ),
          for (final e in I18n.disponibles.entries)
            ChoiceChip(
              label: Text(e.value),
              selected: actual == e.key,
              showCheckmark: false,
              selectedColor: sobreColor ? OL.blanco : OL.moradoClaro,
              backgroundColor: sobreColor
                  ? OL.blanco.withValues(alpha: .15)
                  : OL.blanco,
              labelStyle: TextStyle(
                fontWeight: FontWeight.w800,
                color: sobreColor && actual != e.key ? OL.blanco : OL.morado,
              ),
              side: BorderSide(
                color: sobreColor ? OL.blanco.withValues(alpha: .4) : OL.grisClaro,
              ),
              onSelected: (_) => ref
                  .read(progressProvider.notifier)
                  .elegirIdiomaInterfaz(e.key),
            ),
        ],
      ),
    );
  }
}
