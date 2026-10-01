import 'dart:async';

import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/efectos.dart';
import 'widgets.dart';

/// Bundled, silent gesture. Never generates media or waits on a remote API.
class MascotCoach extends StatefulWidget {
  const MascotCoach({
    super.key,
    required this.message,
    this.listening = false,
    this.idle = false,
  });
  final String message;
  final bool listening;
  final bool idle;
  @override
  State<MascotCoach> createState() => _MascotCoachState();
}

class _MascotCoachState extends State<MascotCoach> {
  Timer? _rest;
  bool _ended = false;
  bool _started = false;
  void _firstFrame() {
    if (_started || widget.idle) return;
    _started = true;
    // Bound playback even if a platform interprets WebP repetition differently.
    _rest = Timer(const Duration(seconds: 5), () {
      if (mounted) setState(() => _ended = true);
    });
  }

  @override
  void dispose() {
    _rest?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final name = widget.listening ? 'Nara' : 'Lumo';
    final stem = widget.listening ? 'nara' : 'lumo';
    final still = 'assets/img/mascotas/$stem-reposo-alpha.png';
    final motion = widget.idle && !widget.listening
        ? 'assets/img/mascotas/lumo-idle-alpha.webp'
        : 'assets/img/mascotas/$stem-${widget.listening ? 'escucha' : 'saludo'}-alpha.webp';
    Widget fallback() => Image.asset(
      still,
      width: 112,
      height: 112,
      excludeFromSemantics: true,
      errorBuilder: (_, _, _) => const SizedBox(
        width: 112,
        height: 112,
        child: Icon(Icons.auto_awesome, color: OL.morado, size: 40),
      ),
    );
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Tarjeta(
        padding: const EdgeInsets.all(12),
        color: OL.moradoSuave,
        borde: OL.moradoClaro,
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(18),
              child: ValueListenableBuilder<bool>(
                valueListenable: Efectos.animaciones,
                builder: (context, enabled, _) {
                  final animate =
                      enabled &&
                      (!_ended || widget.idle) &&
                      !MediaQuery.disableAnimationsOf(context) &&
                      TickerMode.valuesOf(context).enabled;
                  if (!animate) return fallback();
                  return Image.asset(
                    motion,
                    width: 112,
                    height: 112,
                    excludeFromSemantics: true,
                    frameBuilder: (_, child, frame, _) {
                      if (frame == null) return fallback();
                      _firstFrame();
                      return child;
                    },
                    errorBuilder: (_, _, _) => fallback(),
                  );
                },
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    name,
                    style: const TextStyle(
                      color: OL.morado,
                      fontWeight: FontWeight.w900,
                      fontSize: 18,
                    ),
                  ),
                  const SizedBox(height: 5),
                  Text(widget.message, style: const TextStyle(height: 1.35)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
