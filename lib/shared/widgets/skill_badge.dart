import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/diagnostico.dart';

/// Iconos propios, vectoriales: libro, onda sonora, estructura, palabra y pluma.
class InsigniaHabilidad extends StatelessWidget {
  const InsigniaHabilidad(this.skill, {super.key, this.size = 48});
  final String skill;
  final double size;
  @override
  Widget build(BuildContext context) => Semantics(
    label: skillsDiag[skill],
    child: CustomPaint(
      size: Size.square(size),
      painter: _InsigniaPainter(skill),
    ),
  );
}

class _InsigniaPainter extends CustomPainter {
  _InsigniaPainter(this.skill);
  final String skill;
  @override
  void paint(Canvas canvas, Size size) {
    canvas.save();
    canvas.scale(size.width / 48);
    final color = switch (skill) {
      'comprension' => OL.azul,
      'listening' => OL.naranja,
      'gramatica' => OL.morado,
      'vocabulario' => OL.verde,
      _ => OL.rojo,
    };
    final p = Paint()..color = color.withValues(alpha: .12);
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        const Rect.fromLTWH(0, 0, 48, 48),
        const Radius.circular(16),
      ),
      p,
    );
    p
      ..color = color
      ..strokeWidth = 2.5
      ..strokeCap = StrokeCap.round
      ..style = PaintingStyle.stroke;
    if (skill == 'listening') {
      for (var i = 0; i < 5; i++) {
        final h = [5.0, 10.0, 15.0, 10.0, 5.0][i];
        canvas.drawLine(
          Offset(12 + i * 6, 24 - h / 2),
          Offset(12 + i * 6, 24 + h / 2),
          p,
        );
      }
    } else if (skill == 'comprension') {
      canvas.drawPath(
        Path()
          ..moveTo(24, 15)
          ..quadraticBezierTo(16, 10, 10, 14)
          ..lineTo(10, 33)
          ..quadraticBezierTo(18, 29, 24, 35)
          ..quadraticBezierTo(30, 29, 38, 33)
          ..lineTo(38, 14)
          ..quadraticBezierTo(32, 10, 24, 15)
          ..lineTo(24, 35),
        p,
      );
    } else if (skill == 'gramatica') {
      for (var i = 0; i < 3; i++) {
        canvas.drawRRect(
          RRect.fromRectAndRadius(
            Rect.fromLTWH(10 + i * 4, 12 + i * 9, 23 - i * 4, 5),
            const Radius.circular(2),
          ),
          p,
        );
      }
    } else if (skill == 'escritura') {
      canvas.drawPath(
        Path()
          ..moveTo(13, 35)
          ..lineTo(16, 26)
          ..lineTo(31, 11)
          ..lineTo(37, 17)
          ..lineTo(22, 32)
          ..close(),
        p,
      );
      canvas.drawLine(const Offset(12, 39), const Offset(36, 39), p);
    } else {
      canvas.drawRRect(
        RRect.fromRectAndRadius(
          const Rect.fromLTWH(10, 12, 28, 22),
          const Radius.circular(7),
        ),
        p,
      );
      canvas.drawPath(
        Path()
          ..moveTo(16, 34)
          ..lineTo(16, 39)
          ..lineTo(23, 34),
        p,
      );
      for (var i = 0; i < 3; i++) {
        canvas.drawCircle(Offset(17 + i * 7, 23), 1, p);
      }
    }
    canvas.restore();
  }

  @override
  bool shouldRepaint(_InsigniaPainter old) => old.skill != skill;
}
