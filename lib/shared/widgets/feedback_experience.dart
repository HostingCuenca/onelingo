import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/efectos.dart';

class SoundToggle extends StatelessWidget {
  const SoundToggle({super.key});
  @override
  Widget build(BuildContext context) => ValueListenableBuilder<bool>(
    valueListenable: Efectos.sonidos,
    builder: (_, enabled, _) => IconButton(
      tooltip: enabled ? 'Silenciar efectos' : 'Activar efectos',
      onPressed: () => Efectos.cambiarSonido(!enabled),
      icon: Icon(enabled ? Icons.volume_up_rounded : Icons.volume_off_rounded),
    ),
  );
}

/// Entrada corta, sin bucles; respeta el ajuste local y movimiento reducido del sistema.
class FeedbackMotion extends StatelessWidget {
  const FeedbackMotion({super.key, required this.child});
  final Widget child;
  @override
  Widget build(BuildContext context) => ValueListenableBuilder<bool>(
    valueListenable: Efectos.animaciones,
    builder: (context, enabled, _) {
      if (!enabled || MediaQuery.disableAnimationsOf(context)) return child;
      return TweenAnimationBuilder<double>(
        tween: Tween(begin: 0, end: 1),
        duration: const Duration(milliseconds: 420),
        curve: Curves.easeOutCubic,
        builder: (_, value, child) => Opacity(
          opacity: value,
          child: Transform.translate(
            offset: Offset(0, 14 * (1 - value)),
            child: child,
          ),
        ),
        child: child,
      );
    },
  );
}

/// Sello dibujado: trazo de acierto, flecha para revisar o estrella de finalización.
class FeedbackBadge extends StatelessWidget {
  const FeedbackBadge({
    super.key,
    this.correct = true,
    this.completed = false,
    this.size = 64,
  });
  final bool correct, completed;
  final double size;
  @override
  Widget build(BuildContext context) => ValueListenableBuilder<bool>(
    valueListenable: Efectos.animaciones,
    builder: (context, enabled, _) {
      final reduce = !enabled || MediaQuery.disableAnimationsOf(context);
      return TweenAnimationBuilder<double>(
        tween: Tween(begin: reduce ? 1 : 0, end: 1),
        duration: reduce ? Duration.zero : const Duration(milliseconds: 550),
        builder: (_, t, _) => CustomPaint(
          size: Size.square(size),
          painter: _BadgePainter(t, correct, completed),
        ),
      );
    },
  );
}

class _BadgePainter extends CustomPainter {
  _BadgePainter(this.t, this.correct, this.completed);
  final double t;
  final bool correct, completed;
  @override
  void paint(Canvas canvas, Size size) {
    final c = size.center(Offset.zero), r = size.width * .34;
    final color = completed
        ? OL.morado
        : correct
        ? const Color(0xFF197D58)
        : OL.morado;
    canvas.drawCircle(c, r, Paint()..color = color.withValues(alpha: .10));
    final ring = Paint()
      ..color = color.withValues(alpha: .25)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.5;
    canvas.drawArc(
      Rect.fromCircle(center: c, radius: r),
      -math.pi / 2,
      2 * math.pi * t,
      false,
      ring,
    );
    if (correct || completed) {
      for (var i = 0; i < 8; i++) {
        final a = i * math.pi / 4;
        final p =
            c + Offset(math.cos(a), math.sin(a)) * size.width * (.34 + .1 * t);
        final radius = size.width * .07 * math.sin(math.pi * t);
        final star = Path();
        for (var point = 0; point < 8; point++) {
          final angle = a + point * math.pi / 4;
          final d = radius * (point.isEven ? 1 : .3);
          final x = p.dx + math.cos(angle) * d;
          final y = p.dy + math.sin(angle) * d;
          if (point == 0) {
            star.moveTo(x, y);
          } else {
            star.lineTo(x, y);
          }
        }
        star.close();
        canvas.drawPath(
          star,
          Paint()
            ..color = (completed ? OL.morado : const Color(0xFF23B875))
                .withValues(alpha: 1 - t),
        );
      }
    }
    final path = Path();
    if (completed) {
      for (var i = 0; i < 10; i++) {
        final a = -math.pi / 2 + i * math.pi / 5;
        final p =
            c + Offset(math.cos(a), math.sin(a)) * r * (i.isEven ? .62 : .29);
        if (i == 0) {
          path.moveTo(p.dx, p.dy);
        } else {
          path.lineTo(p.dx, p.dy);
        }
      }
      path.close();
    } else if (correct) {
      path.moveTo(c.dx - r * .5, c.dy);
      path.lineTo(c.dx - r * .12, c.dy + r * .35);
      path.lineTo(c.dx + r * .53, c.dy - r * .36);
    } else {
      path.addArc(
        Rect.fromCircle(center: c, radius: r * .48),
        -.5,
        math.pi * 1.6,
      );
      path.moveTo(c.dx - r * .49, c.dy - r * .44);
      path.lineTo(c.dx - r * .49, c.dy);
      path.lineTo(c.dx - r * .05, c.dy);
    }
    final stroke = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = size.width * .05
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;
    for (final metric in path.computeMetrics()) {
      canvas.drawPath(
        metric.extractPath(0, metric.length * (t * 1.6).clamp(0, 1)),
        stroke,
      );
    }
  }

  @override
  bool shouldRepaint(_BadgePainter old) =>
      old.t != t || old.correct != correct || old.completed != completed;
}

class AnswerFeedback extends StatelessWidget {
  const AnswerFeedback({
    super.key,
    required this.correct,
    required this.title,
    required this.child,
  });
  final bool correct;
  final String title;
  final Widget child;
  @override
  Widget build(BuildContext context) => FeedbackMotion(
    child: Semantics(
      liveRegion: true,
      child: Container(
        width: double.infinity,
        margin: const EdgeInsets.only(top: 14),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: correct ? OL.verdeSuave : OL.moradoSuave,
          borderRadius: BorderRadius.circular(22),
          border: Border.all(
            color: (correct ? OL.verde : OL.morado).withValues(alpha: .28),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                FeedbackBadge(correct: correct, size: 52),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    title,
                    style: const TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            child,
          ],
        ),
      ),
    ),
  );
}

class EffectsSettings extends StatelessWidget {
  const EffectsSettings({super.key});
  @override
  Widget build(BuildContext context) => Column(
    children: [
      _switch(
        Efectos.sonidos,
        'Sonidos de práctica',
        'Aciertos, errores y actividades completadas',
        Efectos.cambiarSonido,
      ),
      _switch(
        Efectos.animaciones,
        'Animaciones de práctica',
        'Celebraciones y transiciones breves',
        Efectos.cambiarAnimaciones,
      ),
      _switch(
        Efectos.vibraciones,
        'Vibración suave',
        'En dispositivos compatibles',
        Efectos.cambiarVibracion,
      ),
    ],
  );
  Widget _switch(
    ValueNotifier<bool> notifier,
    String title,
    String subtitle,
    Future<void> Function(bool) change,
  ) => ValueListenableBuilder<bool>(
    valueListenable: notifier,
    builder: (_, v, _) => SwitchListTile(
      value: v,
      onChanged: change,
      title: Text(title),
      subtitle: Text(subtitle),
    ),
  );
}

/// Panel visible encima de Continuar; las explicaciones largas tienen scroll propio.
class FeedbackDock extends StatelessWidget {
  const FeedbackDock({super.key, required this.child});
  final Widget child;
  @override
  Widget build(BuildContext context) => ConstrainedBox(
    constraints: BoxConstraints(
      maxHeight:
          (MediaQuery.sizeOf(context).height -
              MediaQuery.viewInsetsOf(context).bottom) *
          .38,
    ),
    child: Scrollbar(
      child: SingleChildScrollView(primary: false, child: child),
    ),
  );
}
