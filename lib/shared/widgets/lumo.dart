import 'package:flutter/material.dart';

import '../../core/efectos.dart';

/// Poses de Lumo (assets/img/mascotas): imagen fija (360 px, ~25 KB) y
/// animación en bucle (216 px, 8 fps, 0,3–0,6 MB). Fuentes en alta
/// resolución: output/imagegen/mascotas/fuente/.
enum PoseLumo {
  reposo('lumo-reposo-alpha.png', 'lumo-idle-alpha.webp'),
  celebra('lumo-celebra-alpha.webp', 'lumo-celebra-anim-alpha.webp'),
  anima('lumo-anima-alpha.webp', 'lumo-anima-anim-alpha.webp'),
  errorAmable(
    'lumo-error-amable-alpha.webp',
    'lumo-error-amable-anim-alpha.webp',
  ),
  pensando('lumo-pensando-alpha.webp', 'lumo-pensando-anim-alpha.webp'),
  escucha('lumo-escucha-alpha.webp', 'lumo-escucha-anim-alpha.webp'),
  sorprendido(
    'lumo-sorprendido-alpha.webp',
    'lumo-sorprendido-anim-alpha.webp',
  );

  const PoseLumo(this.archivo, this.archivoAnimado);
  final String archivo, archivoAnimado;
  String get asset => 'assets/img/mascotas/$archivo';
  String get assetAnimado => 'assets/img/mascotas/$archivoAnimado';

  static int _aciertos = 0;

  /// Alterna celebrar y pulgar arriba para que el acierto no sea repetitivo.
  static PoseLumo acierto() =>
      (_aciertos++).isEven ? PoseLumo.celebra : PoseLumo.anima;
}

/// Lumo reaccionando. Nunca debe haber dos personajes a la vez en pantalla.
/// Siempre se ve: la imagen fija (precargada al abrir la
/// app) aparece al instante y se sustituye por la animación cuando esta ya
/// está decodificada. Sin animaciones (ajuste del alumno o movimiento
/// reducido del sistema) queda la imagen fija.
class LumoReaccion extends StatelessWidget {
  const LumoReaccion({super.key, required this.pose, this.size = 96});
  final PoseLumo pose;
  final double size;

  Widget _fija() => Image.asset(
    pose.asset,
    width: size,
    height: size,
    fit: BoxFit.contain,
    excludeFromSemantics: true,
    gaplessPlayback: true,
    errorBuilder: (_, _, _) => Image.asset(
      PoseLumo.reposo.asset,
      width: size,
      height: size,
      excludeFromSemantics: true,
    ),
  );

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<bool>(
      valueListenable: Efectos.animaciones,
      builder: (context, enabled, _) {
        final fija = _fija();
        if (!enabled || MediaQuery.disableAnimationsOf(context)) return fija;
        final animada = Image.asset(
          pose.assetAnimado,
          width: size,
          height: size,
          fit: BoxFit.contain,
          excludeFromSemantics: true,
          gaplessPlayback: true,
          // Hasta tener el primer cuadro, la imagen fija (nunca un hueco).
          frameBuilder: (_, child, frame, sincrono) =>
              frame == null && !sincrono ? fija : child,
          errorBuilder: (_, _, _) => fija,
        );
        // Sin rebote de entrada: la animación propia de la pose basta.
        return animada;
      },
    );
  }
}

/// Precarga a Lumo al abrir la app: las imágenes fijas enseguida (son
/// ligeras y deben estar listas antes del primer «Comprobar») y las
/// animaciones unos segundos después, en segundo plano.
class PrecargaLumo extends StatefulWidget {
  const PrecargaLumo({super.key, required this.child});
  final Widget child;

  @override
  State<PrecargaLumo> createState() => _PrecargaLumoState();
}

class _PrecargaLumoState extends State<PrecargaLumo> {
  bool _hecho = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_hecho) return;
    _hecho = true;
    for (final p in PoseLumo.values) {
      precacheImage(AssetImage(p.asset), context, onError: (_, _) {});
    }
    Future<void>.delayed(const Duration(seconds: 4), () {
      if (!mounted) return;
      for (final p in [
        PoseLumo.celebra,
        PoseLumo.anima,
        PoseLumo.errorAmable,
        PoseLumo.pensando,
        PoseLumo.escucha,
      ]) {
        precacheImage(AssetImage(p.assetAnimado), context, onError: (_, _) {});
      }
    });
  }

  @override
  Widget build(BuildContext context) => widget.child;
}
