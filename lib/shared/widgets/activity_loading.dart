import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/efectos.dart';

/// Reserva el espacio del ejercicio mientras llega el contenido real.
class ActivityLoading extends StatefulWidget {
  const ActivityLoading({
    super.key,
    this.label = 'Preparando tu actividad…',
    this.detail,
    this.compact = false,
  });
  final String label;
  final String? detail;
  final bool compact;
  @override
  State<ActivityLoading> createState() => _ActivityLoadingState();
}

class _ActivityLoadingState extends State<ActivityLoading>
    with SingleTickerProviderStateMixin {
  late final AnimationController motion = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 2400),
  );
  @override
  void dispose() {
    motion.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => ValueListenableBuilder<bool>(
    valueListenable: Efectos.animaciones,
    builder: (context, enabled, _) {
      final animate =
          enabled &&
          !MediaQuery.disableAnimationsOf(context) &&
          TickerMode.valuesOf(context).enabled;
      if (animate && !motion.isAnimating) motion.repeat();
      if (!animate && motion.isAnimating) motion.stop();
      return Semantics(
        label: '${widget.label} ${widget.detail ?? ''}',
        liveRegion: true,
        child: ExcludeSemantics(
          child: AnimatedBuilder(
            animation: motion,
            builder: (context, _) {
              final t = animate ? motion.value : 0.0;
              final orbit = SizedBox(
                width: 176,
                height: 176,
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    Transform.rotate(
                      angle: animate ? .12 * math.sin(t * math.pi * 4) : 0,
                      child: Transform.scale(
                        scale: animate
                            ? 1 + .12 * math.sin(t * math.pi * 4)
                            : 1,
                        child: Container(
                          width: 74,
                          height: 74,
                          decoration: const BoxDecoration(
                            color: OL.moradoSuave,
                            shape: BoxShape.circle,
                          ),
                          child: CustomPaint(
                            painter: _BookBuddy(animate ? t : .2),
                          ),
                        ),
                      ),
                    ),
                    for (var i = 0; i < 4; i++)
                      Transform.translate(
                        key: ValueKey('activity-orbit-$i'),
                        offset:
                            Offset(
                              math.cos(t * math.pi * 2 + i * math.pi / 2),
                              math.sin(t * math.pi * 2 + i * math.pi / 2),
                            ) *
                            (62 +
                                (animate
                                    ? 7 * math.sin(t * math.pi * 4 + i)
                                    : 0)),
                        child: Transform.rotate(
                          angle: animate
                              ? .22 * math.sin(t * math.pi * 4 + i)
                              : 0,
                          child: Transform.scale(
                            scale: animate
                                ? 1 + .12 * math.sin(t * math.pi * 4 + i)
                                : 1,
                            child: Container(
                              width: 40,
                              height: 40,
                              decoration: BoxDecoration(
                                color: [
                                  OL.moradoSuave,
                                  OL.verdeSuave,
                                  OL.naranjaSuave,
                                  const Color(0xFFE5F2FF),
                                ][i],
                                borderRadius: BorderRadius.circular(12),
                                border: Border.all(
                                  color: OL.morado.withValues(alpha: .15),
                                ),
                              ),
                              child: Icon(
                                [
                                  Icons.menu_book_rounded,
                                  Icons.headphones_rounded,
                                  Icons.chat_bubble_outline_rounded,
                                  Icons.edit_rounded,
                                ][i],
                                color: OL.morado,
                                size: 21,
                              ),
                            ),
                          ),
                        ),
                      ),
                  ],
                ),
              );
              return Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  orbit,
                  const SizedBox(height: 12),
                  Text(
                    widget.label,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontWeight: FontWeight.w700,
                      color: OL.morado,
                    ),
                  ),
                  if (widget.detail != null)
                    Padding(
                      padding: const EdgeInsets.only(top: 8),
                      child: Text(widget.detail!, textAlign: TextAlign.center),
                    ),
                  if (!widget.compact) ...[
                    const SizedBox(height: 24),
                    Opacity(
                      opacity: animate
                          ? .65 + .25 * math.sin(t * math.pi * 4)
                          : .8,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _block(16),
                          const SizedBox(height: 10),
                          FractionallySizedBox(
                            widthFactor: .7,
                            child: _block(16),
                          ),
                          const SizedBox(height: 20),
                          for (var i = 0; i < 3; i++)
                            Padding(
                              padding: const EdgeInsets.only(bottom: 10),
                              child: _block(44),
                            ),
                        ],
                      ),
                    ),
                  ],
                ],
              );
            },
          ),
        ),
      );
    },
  );
  Widget _block(double height) => Container(
    width: double.infinity,
    height: height,
    decoration: BoxDecoration(
      color: OL.moradoSuave,
      borderRadius: BorderRadius.circular(12),
    ),
  );
}

/// Libro-personaje propio: páginas, mirada y sonrisa acompañan la espera.
class _BookBuddy extends CustomPainter {
  _BookBuddy(this.t);
  final double t;
  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width, h = size.height;
    final cover = RRect.fromRectAndRadius(
      Rect.fromLTWH(w * .16, h * .17, w * .68, h * .68),
      const Radius.circular(12),
    );
    canvas.drawRRect(cover, Paint()..color = OL.morado);
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(w * .25, h * .12, w * .58, h * .59),
        const Radius.circular(8),
      ),
      Paint()..color = Colors.white,
    );
    canvas.drawLine(
      Offset(w * .30, h * .23),
      Offset(w * .73, h * .23),
      Paint()
        ..color = OL.moradoSuave
        ..strokeWidth = 3,
    );
    final blink = t > .82 && t < .90;
    for (final x in [.40, .66]) {
      if (blink) {
        canvas.drawLine(
          Offset(w * (x - .04), h * .41),
          Offset(w * (x + .04), h * .41),
          Paint()
            ..color = OL.morado
            ..strokeWidth = 3
            ..strokeCap = StrokeCap.round,
        );
      } else {
        canvas.drawOval(
          Rect.fromCenter(
            center: Offset(w * x, h * .40),
            width: w * .07,
            height: h * .10,
          ),
          Paint()..color = OL.morado,
        );
      }
    }
    canvas.drawArc(
      Rect.fromCenter(
        center: Offset(w * .53, h * .49),
        width: w * .19,
        height: h * .14,
      ),
      0,
      math.pi,
      false,
      Paint()
        ..color = OL.morado
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2.5
        ..strokeCap = StrokeCap.round,
    );
    canvas.drawLine(
      Offset(w * .32, h * .77),
      Offset(w * .74, h * .77),
      Paint()
        ..color = Colors.white.withValues(alpha: .8)
        ..strokeWidth = 2,
    );
  }

  @override
  bool shouldRepaint(_BookBuddy old) => old.t != t;
}
