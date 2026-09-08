import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/services.dart';

/// Sonidos cortos + vibración, al estilo Duolingo: respuesta inmediata y agradable.
class Efectos {
  Efectos._();
  static final _player = AudioPlayer()..setPlayerMode(PlayerMode.lowLatency);
  static bool sonido = true;

  static Future<void> _tocar(String nombre) async {
    if (!sonido) return;
    try {
      await _player.stop();
      await _player.play(AssetSource('sfx/$nombre.wav'), volume: 0.9);
    } catch (_) {}
  }

  static void correcto() {
    HapticFeedback.lightImpact();
    _tocar('correcto');
  }

  static void incorrecto() {
    HapticFeedback.heavyImpact();
    _tocar('incorrecto');
  }

  static void completado() {
    HapticFeedback.mediumImpact();
    _tocar('completado');
  }

  static void toque() => HapticFeedback.selectionClick();
}
