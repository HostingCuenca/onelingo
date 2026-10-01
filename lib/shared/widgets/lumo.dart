import 'package:flutter/material.dart';

import '../../core/efectos.dart';

/// Poses de Lumo (assets/img/mascotas, 360 px con transparencia).
/// Fuentes en alta resolución: output/imagegen/mascotas/fuente/.
enum PoseLumo {
  reposo('lumo-reposo-alpha.png'),
  celebra('lumo-celebra-alpha.webp'),
  anima('lumo-anima-alpha.webp'),
  errorAmable('lumo-error-amable-alpha.webp'),
  pensando('lumo-pensando-alpha.webp'),
  escucha('lumo-escucha-alpha.webp'),
  sorprendido('lumo-sorprendido-alpha.webp');

  const PoseLumo(this.archivo);
  final String archivo;
  String get asset => 'assets/img/mascotas/$archivo';

  static int _aciertos = 0;

  /// Alterna celebrar y pulgar arriba para que el acierto no sea repetitivo.
  static PoseLumo acierto() =>
      (_aciertos++).isEven ? PoseLumo.celebra : PoseLumo.anima;
}

/// Lumo reaccionando: entra con un pequeño salto (o quieto si el alumno
/// desactivó las animaciones o el sistema pide movimiento reducido).
class LumoReaccion extends StatelessWidget {
  const LumoReaccion({super.key, required this.pose, this.size = 96});
  final PoseLumo pose;
  final double size;

  @override
  Widget build(BuildContext context) {
    final imagen = Image.asset(
      pose.asset,
      width: size,
      height: size,
      fit: BoxFit.contain,
      excludeFromSemantics: true,
      errorBuilder: (_, _, _) => Image.asset(
        PoseLumo.reposo.asset,
        width: size,
        height: size,
        excludeFromSemantics: true,
      ),
    );
    return ValueListenableBuilder<bool>(
      valueListenable: Efectos.animaciones,
      builder: (context, enabled, _) {
        if (!enabled || MediaQuery.disableAnimationsOf(context)) return imagen;
        final alegre = pose != PoseLumo.errorAmable;
        return TweenAnimationBuilder<double>(
          key: ValueKey(pose),
          tween: Tween(begin: 0, end: 1),
          duration: Duration(milliseconds: alegre ? 650 : 500),
          curve: alegre ? Curves.elasticOut : Curves.easeOutBack,
          builder: (_, t, child) => Transform.translate(
            // Alegre: salta desde abajo; triste: se hunde un poco al entrar.
            offset: Offset(0, (alegre ? 18 : -8) * (1 - t)),
            child: Transform.scale(scale: .7 + .3 * t, child: child),
          ),
          child: imagen,
        );
      },
    );
  }
}
