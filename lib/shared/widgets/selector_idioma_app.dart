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
            _Ficha(
              texto: e.value,
              elegida: actual == e.key,
              sobreColor: sobreColor,
              alElegir: () => ref
                  .read(progressProvider.notifier)
                  .elegirIdiomaInterfaz(e.key),
            ),
        ],
      ),
    );
  }
}

/// Ficha de idioma con colores fijos por estado. No usa ChoiceChip: en Android
/// el tema M3 pintaba la no elegida blanca opaca con el texto blanco encima.
class _Ficha extends StatelessWidget {
  const _Ficha({
    required this.texto,
    required this.elegida,
    required this.sobreColor,
    required this.alElegir,
  });

  final String texto;
  final bool elegida, sobreColor;
  final VoidCallback alElegir;

  @override
  Widget build(BuildContext context) {
    final (fondo, letra, borde) = switch ((sobreColor, elegida)) {
      (true, true) => (OL.blanco, OL.morado, OL.blanco),
      (true, false) => (
        Colors.transparent,
        OL.blanco,
        OL.blanco.withValues(alpha: .55),
      ),
      (false, true) => (OL.moradoClaro, OL.morado, OL.morado),
      (false, false) => (OL.blanco, OL.morado, OL.grisClaro),
    };
    return Semantics(
      button: true,
      selected: elegida,
      child: Material(
        color: fondo,
        shape: StadiumBorder(side: BorderSide(color: borde, width: 1.5)),
        clipBehavior: Clip.antiAlias,
        child: InkWell(
          onTap: elegida ? null : alElegir,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 9),
            child: Text(
              texto,
              style: TextStyle(fontWeight: FontWeight.w800, color: letra),
            ),
          ),
        ),
      ),
    );
  }
}
