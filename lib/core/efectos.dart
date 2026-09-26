import 'dart:async';

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Feedback local: nunca llama a proveedores de IA o de voz.
class Efectos {
  Efectos._();
  static AudioPlayer? _player;
  static final _players = <String, AudioPlayer>{};
  static Future<void>? _preparacion;

  static Future<void> precargar() => _preparacion ??= _preparar();
  static Future<void> _preparar() async {
    for (final nombre in ['correcto', 'incorrecto', 'completado', 'toque', 'nivel']) {
      final player = AudioPlayer();
      try {
        await player.setReleaseMode(ReleaseMode.stop);
        // El toque de selección es mucho más discreto que el feedback.
        await player.setVolume(nombre == 'toque' ? .2 : .35);
        await player.setSource(AssetSource('sfx/$nombre.wav'));
        _players[nombre] = player;
      } catch (_) {
        await player.dispose();
      }
    }
  }

  static SharedPreferences? _prefs;
  static final sonidos = ValueNotifier(true);
  static final animaciones = ValueNotifier(true);
  static final vibraciones = ValueNotifier(true);
  static int _turno = 0;
  static Future<void> Function()? antesDeSonar;
  static bool get sonido => sonidos.value;
  static set sonido(bool value) => sonidos.value = value;

  static void inicializar(SharedPreferences prefs) {
    _prefs = prefs;
    sonidos.value = prefs.getBool('onelingo.efectos.sonido') ?? true;
    animaciones.value = prefs.getBool('onelingo.efectos.animaciones') ?? true;
    vibraciones.value = prefs.getBool('onelingo.efectos.vibracion') ?? true;
  }

  static Future<void> cambiarSonido(bool v) async {
    sonidos.value = v;
    if (!v) await detener();
    await _prefs?.setBool('onelingo.efectos.sonido', v);
  }

  static Future<void> cambiarAnimaciones(bool v) async {
    animaciones.value = v;
    await _prefs?.setBool('onelingo.efectos.animaciones', v);
  }

  static Future<void> cambiarVibracion(bool v) async {
    vibraciones.value = v;
    await _prefs?.setBool('onelingo.efectos.vibracion', v);
  }

  static Future<void> detener() async {
    _turno++;
    try {
      await _player?.stop();
    } catch (_) {}
  }

  static Future<void> _tocar(String nombre) async {
    final turno = ++_turno;
    if (!sonido) return;
    try {
      await precargar();
      await antesDeSonar?.call();
      if (!sonido || turno != _turno) return;
      final anterior = _player;
      if (anterior?.state == PlayerState.playing) await anterior!.stop();
      final player = _players[nombre] ?? AudioPlayer();
      _player = player;
      if (!sonido || turno != _turno) return;
      if (_players.containsKey(nombre)) {
        await player.resume();
      } else {
        _players[nombre] = player;
        await player.setReleaseMode(ReleaseMode.stop);
        await player.play(AssetSource('sfx/$nombre.wav'), volume: .35);
      }
    } catch (_) {
      /* Un fallo de audio nunca bloquea una respuesta. */
    }
  }

  static void _vibrar() {
    if (vibraciones.value) {
      unawaited(HapticFeedback.lightImpact().catchError((_) {}));
    }
  }

  static void correcto() {
    _vibrar();
    unawaited(_tocar('correcto'));
  }

  static void incorrecto() {
    _vibrar();
    unawaited(_tocar('incorrecto'));
  }

  static void completado() {
    _vibrar();
    unawaited(_tocar('completado'));
  }

  /// Nivel completado: fanfarria más larga que la de una unidad.
  static void nivel() {
    if (vibraciones.value) {
      unawaited(HapticFeedback.heavyImpact().catchError((_) {}));
    }
    unawaited(_tocar('nivel'));
  }

  /// Selección de una opción: clic breve y vibración ligera.
  static void toque() {
    if (vibraciones.value) {
      unawaited(HapticFeedback.selectionClick().catchError((_) {}));
    }
    unawaited(_tocar('toque'));
  }
}
