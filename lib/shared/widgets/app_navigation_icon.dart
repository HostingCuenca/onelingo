import 'package:flutter/material.dart';

import '../../app/theme.dart';

/// Familia propia: casa con estrella, libro con brote, diálogos y retrato.
class AppNavigationIcon extends StatelessWidget {
  const AppNavigationIcon(this.index, {super.key, this.selected = false});
  final int index;
  final bool selected;
  @override
  Widget build(BuildContext context) => AnimatedScale(
    scale: selected ? 1.08 : 1,
    duration: MediaQuery.disableAnimationsOf(context)
        ? Duration.zero
        : const Duration(milliseconds: 180),
    curve: Curves.easeOutCubic,
    child: SizedBox(
      width: 32,
      height: 32,
      child: CustomPaint(painter: _NavigationPainter(index, selected)),
    ),
  );
}

class _NavigationPainter extends CustomPainter {
  _NavigationPainter(this.index, this.selected);
  final int index;
  final bool selected;
  @override
  void paint(Canvas c, Size size) {
    final p = Paint()
      ..color = selected
          ? [OL.morado, OL.azul, OL.naranja, OL.morado][index]
          : OL.gris
      ..strokeWidth = 2.4
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round
      ..style = PaintingStyle.stroke;
    final fill = Paint()
      ..color = selected
          ? [
              OL.moradoClaro,
              OL.azulSuave,
              OL.naranjaSuave,
              OL.moradoClaro,
            ][index]
          : OL.blanco;
    if (index == 0) {
      final house = Path()
        ..moveTo(4, 15)
        ..lineTo(16, 4)
        ..lineTo(28, 15)
        ..lineTo(26, 15)
        ..lineTo(26, 28)
        ..lineTo(7, 28)
        ..lineTo(7, 15)
        ..close();
      c.drawPath(house, fill);
      c.drawPath(house, p);
      c.drawRRect(
        RRect.fromRectAndRadius(
          const Rect.fromLTWH(13, 20, 6, 8),
          const Radius.circular(2),
        ),
        p,
      );
      c.drawCircle(const Offset(16, 13), 2.5, p);
    } else if (index == 1) {
      final book = Path()
        ..moveTo(16, 13)
        ..quadraticBezierTo(9, 9, 3, 12)
        ..lineTo(3, 27)
        ..quadraticBezierTo(10, 24, 16, 29)
        ..quadraticBezierTo(22, 24, 29, 27)
        ..lineTo(29, 12)
        ..quadraticBezierTo(23, 9, 16, 13)
        ..close();
      c.drawPath(book, fill);
      c.drawPath(book, p);
      c.drawLine(const Offset(16, 13), const Offset(16, 29), p);
      c.drawPath(
        Path()
          ..moveTo(16, 9)
          ..quadraticBezierTo(8, 10, 10, 3)
          ..quadraticBezierTo(16, 3, 16, 9)
          ..quadraticBezierTo(24, 9, 23, 2)
          ..quadraticBezierTo(16, 2, 16, 9),
        p,
      );
    } else if (index == 2) {
      final back = RRect.fromRectAndRadius(
        const Rect.fromLTWH(10, 11, 19, 16),
        const Radius.circular(6),
      );
      c.drawRRect(back, fill);
      c.drawRRect(back, p);
      final front = RRect.fromRectAndRadius(
        const Rect.fromLTWH(2, 3, 23, 18),
        const Radius.circular(7),
      );
      c.drawRRect(front, Paint()..color = OL.blanco);
      c.drawRRect(front, p);
      c.drawPath(
        Path()
          ..moveTo(7, 21)
          ..lineTo(7, 26)
          ..lineTo(13, 21),
        p,
      );
      for (var i = 0; i < 3; i++) {
        c.drawCircle(Offset(8 + i * 5, 12), .9, p);
      }
    } else {
      c.drawCircle(const Offset(16, 16), 14, fill);
      c.drawCircle(const Offset(16, 16), 14, p);
      c.drawCircle(const Offset(16, 12), 4, p);
      c.drawPath(
        Path()
          ..moveTo(7, 26)
          ..quadraticBezierTo(8, 19, 16, 19)
          ..quadraticBezierTo(24, 19, 25, 26),
        p,
      );
      c.drawPath(
        Path()
          ..moveTo(24, 4)
          ..lineTo(27, 1)
          ..moveTo(28, 7)
          ..lineTo(31, 6),
        p,
      );
    }
  }

  @override
  bool shouldRepaint(_NavigationPainter old) =>
      old.index != index || old.selected != selected;
}
