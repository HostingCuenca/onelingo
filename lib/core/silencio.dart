/// Audio-activity gate, not linguistic VAD. Short pauses stay in one turn.
class FinPorSilencio {
  FinPorSilencio({
    this.pausa = const Duration(seconds: 3),
    this.umbralDb = -50,
  });
  final Duration pausa;
  final double umbralDb;
  Duration? _ultimaActividad;
  int _muestras = 0;
  bool huboVoz = false;
  bool actualizar(double db, Duration tiempo) {
    // PCM silence can be -infinity dBFS (log(0)); it is valid silence.
    if (db.isNaN || db == double.infinity) return false;
    if (db > umbralDb) {
      _muestras++;
      if (_muestras >= 2) huboVoz = true;
      _ultimaActividad = tiempo;
      return false;
    }
    _muestras = 0;
    return huboVoz &&
        _ultimaActividad != null &&
        tiempo - _ultimaActividad! >= pausa;
  }
}
