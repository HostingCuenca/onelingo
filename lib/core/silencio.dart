/// Audio-activity gate, not linguistic VAD. Short pauses stay in one turn.
///
/// The bar for "activity" follows the voice: once the student has spoken, a
/// sample counts as activity only if it is within [caidaDb] of the loudest
/// voice heard. Phones with auto gain keep room noise above a fixed -50 dBFS,
/// so a fixed bar never saw the silence after a short "hello" and the
/// recording stayed open until its time limit.
class FinPorSilencio {
  FinPorSilencio({
    this.pausa = const Duration(seconds: 3),
    this.umbralDb = -50,
    this.caidaDb = 20,
  });
  final Duration pausa;
  final double umbralDb;
  final double caidaDb;
  Duration? _ultimaActividad;
  int _muestras = 0;
  double? _pico;
  bool huboVoz = false;

  double get _umbral {
    final pico = _pico;
    if (pico == null) return umbralDb;
    final relativo = pico - caidaDb;
    return relativo > umbralDb ? relativo : umbralDb;
  }

  bool actualizar(double db, Duration tiempo) {
    // PCM silence can be -infinity dBFS (log(0)); it is valid silence.
    if (db.isNaN || db == double.infinity) return false;
    if (db > _umbral) {
      _muestras++;
      if (_muestras >= 2) {
        huboVoz = true;
        // One click is not voice: the peak only counts sustained sound.
        if (_pico == null || db > _pico!) _pico = db;
      }
      _ultimaActividad = tiempo;
      return false;
    }
    _muestras = 0;
    return huboVoz &&
        _ultimaActividad != null &&
        tiempo - _ultimaActividad! >= pausa;
  }
}

/// Mic level 0..1 for the voice meter (dBFS from -60 to -10).
double nivelDeDb(double db) {
  if (db.isNaN || db == double.infinity) return 0;
  return ((db + 60) / 50).clamp(0.0, 1.0);
}
