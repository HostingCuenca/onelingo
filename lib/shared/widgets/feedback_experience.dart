import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../app/theme.dart';
import 'lumo.dart';
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

/// Sello dibujado: ✓ de acierto, ✗ de error o estrella de finalización.
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
        : OL.rojo;
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
      // Error: una X clara (antes era una flecha curva que parecía «repetir»).
      path.moveTo(c.dx - r * .38, c.dy - r * .38);
      path.lineTo(c.dx + r * .38, c.dy + r * .38);
      path.moveTo(c.dx + r * .38, c.dy - r * .38);
      path.lineTo(c.dx - r * .38, c.dy + r * .38);
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
    this.lumo = false,
  });
  final bool correct;
  final String title;
  final Widget child;

  /// Lumo reacciona (feliz al acertar, triste pero amable al fallar). Por
  /// defecto no: estas pantallas ya muestran un personaje y nunca debe haber
  /// dos a la vez. El panel inferior es quien lleva a Lumo.
  final bool lumo;
  @override
  Widget build(BuildContext context) => FeedbackMotion(
    child: Semantics(
      liveRegion: true,
      child: Container(
        width: double.infinity,
        margin: const EdgeInsets.only(top: 14),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: correct ? OL.verdeSuave : OL.rojoSuave,
          borderRadius: BorderRadius.circular(22),
          border: Border.all(
            color: (correct ? OL.verde : OL.rojo).withValues(alpha: .28),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                if (lumo) ...[
                  LumoReaccion(
                    pose: correct ? PoseLumo.acierto() : PoseLumo.errorAmable,
                    size: 64,
                  ),
                  const SizedBox(width: 6),
                ],
                FeedbackBadge(correct: correct, size: 40),
                const SizedBox(width: 8),
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

/// Panel de resultado al estilo de las apps de idiomas: sube desde abajo con
/// Lumo, el título, la explicación (con scroll propio) y SIGUIENTE siempre
/// visible. Devuelve 'siguiente' o 'reintentar'.
Future<String?> mostrarPanelResultado(
  BuildContext context, {
  required bool correcto,
  required String titulo,
  required Widget cuerpo,
  bool reintentar = false,
  String boton = 'SIGUIENTE',
  bool lumo = true,
}) {
  final pose = correcto ? PoseLumo.acierto() : PoseLumo.errorAmable;
  final color = correcto ? const Color(0xFF197D58) : OL.rojo;
  return showModalBottomSheet<String>(
    context: context,
    // Por encima de la barra de navegación, ocupando el borde inferior.
    useRootNavigator: true,
    isDismissible: false,
    enableDrag: false,
    isScrollControlled: true,
    barrierColor: Colors.black.withValues(alpha: .12),
    backgroundColor: correcto ? OL.verdeSuave : OL.rojoSuave,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(26)),
    ),
    builder: (context) => PopScope(
      canPop: false,
      child: SafeArea(
        top: false,
        child: ConstrainedBox(
          constraints: BoxConstraints(
            maxHeight: MediaQuery.sizeOf(context).height * .62,
          ),
          child: Semantics(
            liveRegion: true,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(20, 16, 20, 16),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      if (lumo) ...[
                        LumoReaccion(pose: pose, size: 92),
                        const SizedBox(width: 10),
                      ],
                      Expanded(
                        child: Padding(
                          padding: const EdgeInsets.only(bottom: 12),
                          child: Row(
                            children: [
                              FeedbackBadge(correct: correcto, size: 40),
                              const SizedBox(width: 6),
                              Expanded(
                                child: Text(
                                  titulo,
                                  style: TextStyle(
                                    fontSize: 22,
                                    fontWeight: FontWeight.w900,
                                    color: color,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Flexible(
                    child: SingleChildScrollView(
                      child: DefaultTextStyle.merge(
                        style: const TextStyle(color: OL.texto),
                        child: cuerpo,
                      ),
                    ),
                  ),
                  const SizedBox(height: 14),
                  FilledButton(
                    style: FilledButton.styleFrom(
                      backgroundColor: color,
                      minimumSize: const Size.fromHeight(54),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                    ),
                    onPressed: () => Navigator.of(context).pop('siguiente'),
                    child: Text(
                      boton,
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w900,
                        letterSpacing: .5,
                      ),
                    ),
                  ),
                  if (reintentar)
                    TextButton.icon(
                      onPressed: () => Navigator.of(context).pop('reintentar'),
                      icon: const Icon(Icons.replay_rounded),
                      label: const Text('Intentar otra vez ahora'),
                    ),
                ],
              ),
            ),
          ),
        ),
      ),
    ),
  );
}
