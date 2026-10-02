import 'dart:async';
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../app/theme.dart';
import '../../core/state/providers.dart';
import '../../core/efectos.dart';
import 'widgets.dart';
import '../../core/i18n/i18n.dart';

class StreakCard extends ConsumerStatefulWidget {
  const StreakCard({super.key});
  @override
  ConsumerState<StreakCard> createState() => _StreakCardState();
}

class _StreakCardState extends ConsumerState<StreakCard>
    with SingleTickerProviderStateMixin {
  late final AnimationController pulse = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 1100),
  );
  Timer? midnight;
  String? celebrated;
  String dayKey(DateTime d) =>
      '${d.year}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';
  @override
  void initState() {
    super.initState();
    Efectos.animaciones.addListener(effectsChanged);
    scheduleMidnight();
  }

  void effectsChanged() {
    if (mounted) setState(() {});
  }

  void scheduleMidnight() {
    final now = DateTime.now();
    midnight = Timer(
      DateTime(now.year, now.month, now.day + 1).difference(now),
      () {
        if (mounted) {
          setState(() {});
          scheduleMidnight();
        }
      },
    );
  }

  @override
  void dispose() {
    Efectos.animaciones.removeListener(effectsChanged);
    midnight?.cancel();
    pulse.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final now = DateTime.now();
    final today = dayKey(now);
    final active = s.diasActividad.contains(today);
    final reduced =
        MediaQuery.disableAnimationsOf(context) || !Efectos.animaciones.value;
    if (active && celebrated != today) {
      celebrated = today;
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted && !reduced) pulse.forward(from: 0);
      });
    }
    final monday = DateTime(now.year, now.month, now.day - (now.weekday - 1));
    return Semantics(
      label: tr('Racha de {n} días. {estado}', {
        'n': s.rachaVigente,
        'estado': active
            ? tr('Actividad de hoy completada')
            : tr('Aún sin actividad hoy'),
      }),
      child: Tarjeta(
        color: OL.naranjaSuave,
        borde: OL.naranja.withValues(alpha: .4),
        sombra: false,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                AnimatedBuilder(
                  animation: pulse,
                  builder: (_, _) => Transform.scale(
                    scale: reduced
                        ? 1
                        : 1 + math.sin(pulse.value * math.pi) * .13,
                    child: CustomPaint(
                      size: const Size(52, 60),
                      painter: _Flame(
                        active: active,
                        progress: reduced ? 0 : pulse.value,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        s.rachaVigente == 1
                            ? tr('{n} día de constancia', {'n': s.rachaVigente})
                            : tr('{n} días de constancia', {
                                'n': s.rachaVigente,
                              }),
                        style: const TextStyle(
                          fontSize: 19,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        active
                            ? tr('¡Hoy ya diste un paso!')
                            : tr('Una práctica hoy mantiene tu hábito.'),
                        style: const TextStyle(fontSize: 13, height: 1.35),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                for (var i = 0; i < 7; i++)
                  Expanded(
                    child: Builder(
                      builder: (context) {
                        final date = monday.add(Duration(days: i));
                        final key = dayKey(date);
                        final done = s.diasActividad.contains(key);
                        final isToday = key == today;
                        return Semantics(
                          label:
                              '${date.day}/${date.month}: ${done ? tr('actividad registrada') : tr('sin actividad registrada')}',
                          child: Column(
                            children: [
                              Text(
                                // Iniciales de lunes a domingo.
                                tr('L M X J V S D').split(' ')[i],
                                style: const TextStyle(
                                  fontWeight: FontWeight.w800,
                                  fontSize: 11,
                                ),
                              ),
                              const SizedBox(height: 6),
                              AnimatedContainer(
                                duration: reduced
                                    ? Duration.zero
                                    : const Duration(milliseconds: 240),
                                width: 30,
                                height: 30,
                                decoration: BoxDecoration(
                                  color: done ? OL.naranja : OL.blanco,
                                  shape: BoxShape.circle,
                                  border: Border.all(
                                    color: isToday
                                        ? OL.morado
                                        : OL.naranja.withValues(alpha: .25),
                                    width: isToday ? 2 : 1,
                                  ),
                                ),
                                child: done
                                    ? const Icon(
                                        Icons.check_rounded,
                                        size: 20,
                                        color: OL.texto,
                                      )
                                    : Center(
                                        child: FittedBox(
                                          fit: BoxFit.scaleDown,
                                          child: Text(
                                            '${date.day}',
                                            style: const TextStyle(
                                              fontWeight: FontWeight.w700,
                                              fontSize: 11,
                                            ),
                                          ),
                                        ),
                                      ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 10),
            Text(
              tr('Cada intento cuenta, incluso si te equivocas.'),
              style: const TextStyle(fontSize: 11, color: OL.texto),
            ),
          ],
        ),
      ),
    );
  }
}

class _Flame extends CustomPainter {
  const _Flame({required this.active, required this.progress});
  final bool active;
  final double progress;
  @override
  void paint(Canvas c, Size size) {
    c.save();
    c.scale(size.width / 52, size.height / 60);
    final flame = Path()
      ..moveTo(27, 3)
      ..cubicTo(39, 16, 31, 18, 41, 28)
      ..cubicTo(55, 46, 39, 58, 25, 58)
      ..cubicTo(5, 58, -1, 41, 10, 27)
      ..cubicTo(12, 35, 17, 33, 17, 27)
      ..cubicTo(16, 17, 24, 16, 27, 3)
      ..close();
    c.drawPath(flame, Paint()..color = active ? OL.naranja : OL.grisClaro);
    c.drawPath(
      flame,
      Paint()
        ..color = active ? OL.naranja : OL.gris
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2,
    );
    c.drawPath(
      Path()
        ..moveTo(27, 31)
        ..cubicTo(39, 43, 32, 53, 25, 53)
        ..cubicTo(13, 53, 17, 41, 27, 31),
      Paint()..color = active ? OL.amarillo : OL.blanco,
    );
    if (active && progress > 0 && progress < 1) {
      final paint = Paint()..color = OL.naranja.withValues(alpha: 1 - progress);
      for (var i = 0; i < 5; i++) {
        final angle = i * math.pi * .4;
        c.drawCircle(
          Offset(
            26 + math.cos(angle) * (20 + progress * 9),
            25 - math.sin(angle) * (20 + progress * 9),
          ),
          2.5 * (1 - progress),
          paint,
        );
      }
    }
    c.restore();
  }

  @override
  bool shouldRepaint(_Flame old) =>
      old.active != active || old.progress != progress;
}
