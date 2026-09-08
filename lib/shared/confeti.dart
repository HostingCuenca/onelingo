import 'dart:math';

import 'package:flutter/material.dart';

import '../app/theme.dart';
import '../core/efectos.dart';

/// Lluvia de confeti con la paleta del logo (2,5 s). Suena la melodía de logro al aparecer.
class Confeti extends StatefulWidget {
  const Confeti({super.key, this.particulas = 90, this.conSonido = true});
  final int particulas;
  final bool conSonido;

  @override
  State<Confeti> createState() => _ConfetiState();
}

class _ConfetiState extends State<Confeti> with SingleTickerProviderStateMixin {
  late final AnimationController _c = AnimationController(vsync: this, duration: const Duration(milliseconds: 2600))..forward();
  late final List<_Particula> _p;
  static const _colores = [OL.morado, OL.naranja, OL.verde, OL.azul, OL.rojo, Color(0xFFFFD23F)];

  @override
  void initState() {
    super.initState();
    final r = Random();
    _p = List.generate(widget.particulas, (i) => _Particula(
          x: r.nextDouble(), vy: 0.55 + r.nextDouble() * 0.9, vx: (r.nextDouble() - 0.5) * 0.5,
          rot: r.nextDouble() * pi * 2, vr: (r.nextDouble() - 0.5) * 8, tam: 6 + r.nextDouble() * 7,
          color: _colores[i % _colores.length], retraso: r.nextDouble() * 0.35,
        ));
    if (widget.conSonido) Efectos.completado();
  }

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => IgnorePointer(
        child: AnimatedBuilder(
          animation: _c,
          builder: (_, _) => CustomPaint(painter: _Pintor(_p, _c.value), size: Size.infinite),
        ),
      );
}

class _Particula {
  _Particula({required this.x, required this.vy, required this.vx, required this.rot, required this.vr, required this.tam, required this.color, required this.retraso});
  final double x, vy, vx, rot, vr, tam, retraso;
  final Color color;
}

class _Pintor extends CustomPainter {
  _Pintor(this.p, this.t);
  final List<_Particula> p;
  final double t;

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint();
    for (final q in p) {
      final tt = ((t - q.retraso) / (1 - q.retraso)).clamp(0.0, 1.0);
      if (tt <= 0) continue;
      final y = -20 + tt * tt * size.height * q.vy * 1.4 + tt * size.height * 0.25;
      final x = q.x * size.width + sin(tt * 6 + q.rot) * 18 + q.vx * tt * size.width;
      final alpha = (1 - tt).clamp(0.0, 1.0);
      paint.color = q.color.withValues(alpha: alpha);
      canvas.save();
      canvas.translate(x, y);
      canvas.rotate(q.rot + q.vr * tt);
      canvas.drawRRect(RRect.fromRectAndRadius(Rect.fromCenter(center: Offset.zero, width: q.tam, height: q.tam * 0.55), const Radius.circular(1.5)), paint);
      canvas.restore();
    }
  }

  @override
  bool shouldRepaint(_Pintor old) => old.t != t;
}
