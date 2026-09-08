import 'dart:async';
import 'dart:convert' show utf8;
import 'dart:io' show File;

import 'package:audioplayers/audioplayers.dart';
import 'package:crypto/crypto.dart';
import 'package:flutter/foundation.dart' show debugPrint, kIsWeb;
import 'package:flutter_tts/flutter_tts.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:record/record.dart';
import 'package:speech_to_text/speech_to_text.dart';

import 'api/sync.dart';
import 'content/idiomas.dart';

/// Voz de la app. Primero intenta la voz natural del servidor (ElevenLabs, con
/// caché en el servidor y en el dispositivo); si no hay sesión o falla, usa el
/// motor del sistema (flutter_tts). Un solo objeto para toda la app.
class Voz {
  Voz._();
  static final Voz instancia = Voz._();
  final FlutterTts _tts = FlutterTts();
  String? _localeActual;

  /// Voz natural (ElevenLabs a través del backend). Se puede apagar desde ajustes.
  static bool natural = true;

  Future<void> _preparar(String idioma) async {
    final loc = localeVoz[idioma] ?? 'en-US';
    if (_localeActual == loc) return;
    _localeActual = loc;
    try {
      await _tts.setLanguage(loc);
      await _tts.setSpeechRate(0.45); // algo más lento: nivel principiante
      await _tts.setPitch(1.0);
      await _tts.awaitSpeakCompletion(false);
    } catch (_) {}
  }

  /// Habla `texto` en el idioma dado; quita la romanización entre paréntesis.
  /// `voz` es el rol de voz del servidor: id del tutor (mia, leo, sofia, max),
  /// `narradora` (lecciones, por defecto) o `narrador` (diálogos).
  /// `velocidad` ≤ 0.4 reproduce despacio (modo Listening lento).
  Future<void> hablar(String texto, String idioma, {double? velocidad, String? voz}) async {
    final limpio = soloNativo(texto);
    if (limpio.isEmpty) return;
    if (natural && Sync.instancia.conectado) {
      await _tts.stop().catchError((_) {});
      final ok = await VozNube.instancia.reproducir(limpio, idioma, voz: voz ?? 'narradora', lento: (velocidad ?? 1) <= 0.4);
      if (ok) return;
    }
    try {
      await _preparar(idioma);
      if (velocidad != null) await _tts.setSpeechRate(velocidad);
      await _tts.stop();
      await _tts.speak(limpio);
    } catch (_) {
      // Sin motor de voz disponible (p. ej. simulador sin voces): se ignora.
    }
  }

  Future<void> parar() async {
    await VozNube.instancia.parar();
    try {
      await _tts.stop();
    } catch (_) {}
  }
}

/// Voz natural servida por el backend (`GET /voz`). Cada frase se pide una sola
/// vez: el servidor la genera con ElevenLabs y la guarda; el dispositivo la
/// conserva en su carpeta temporal para no volver a descargarla.
class VozNube {
  VozNube._();
  static final VozNube instancia = VozNube._();
  final AudioPlayer _player = AudioPlayer()..setReleaseMode(ReleaseMode.stop);
  final Map<String, Future<String?>> _enCurso = {};
  String? _dir;
  String ultimoError = '';
  int _turno = 0;

  String _clave(String texto, String idioma, String voz) => sha1.convert(utf8.encode('$voz|$idioma|$texto')).toString();

  Uri _url(String texto, String idioma, String voz, {bool conToken = false}) => Uri.parse('${Sync.baseUrl}/voz').replace(queryParameters: {
        'texto': texto, 'idioma': idioma, 'voz': voz, if (conToken) 'token': Sync.instancia.token ?? '',
      });

  /// Descarga (o recupera de la caché local) el MP3 y devuelve su ruta; null si falla.
  Future<String?> _archivo(String texto, String idioma, String voz) {
    final k = _clave(texto, idioma, voz);
    return _enCurso.putIfAbsent(k, () async {
      try {
        _dir ??= '${(await getTemporaryDirectory()).path}/onelingo_voz';
        final f = File('$_dir/$k.mp3');
        if (await f.exists() && await f.length() > 0) return f.path;
        final r = await http.get(_url(texto, idioma, voz), headers: {'authorization': 'Bearer ${Sync.instancia.token}'}).timeout(const Duration(seconds: 15));
        if (r.statusCode != 200 || r.bodyBytes.isEmpty) {
          ultimoError = 'voz ${r.statusCode}';
          return null;
        }
        await f.parent.create(recursive: true);
        await f.writeAsBytes(r.bodyBytes, flush: true);
        return f.path;
      } catch (e) {
        ultimoError = '$e';
        return null;
      } finally {
        _enCurso.remove(k);
      }
    });
  }

  /// Reproduce la frase; devuelve false si no se pudo (la app usa entonces la voz del sistema).
  Future<bool> reproducir(String texto, String idioma, {String voz = 'narradora', bool lento = false}) async {
    final mio = ++_turno;
    try {
      await _player.stop();
      await _player.setPlaybackRate(lento ? 0.8 : 1.0);
      if (kIsWeb) {
        await _player.play(UrlSource(_url(texto, idioma, voz, conToken: true).toString()));
        return true;
      }
      final ruta = await _archivo(texto, idioma, voz);
      if (ruta == null || mio != _turno) return ruta != null; // otra frase pidió la voz mientras tanto
      await _player.play(DeviceFileSource(ruta));
      return true;
    } catch (e) {
      ultimoError = '$e';
      return false;
    }
  }

  /// Descarga en segundo plano las frases de una lección para que suenen al instante.
  void precargar(Iterable<String> textos, String idioma, {String voz = 'narradora'}) {
    if (kIsWeb || !Sync.instancia.conectado || !Voz.natural) return;
    Future(() async {
      for (final t in textos) {
        final limpio = soloNativo(t);
        if (limpio.isEmpty) continue;
        await _archivo(limpio, idioma, voz);
      }
    });
  }

  Future<void> parar() async {
    _turno++;
    try {
      await _player.stop();
    } catch (_) {}
  }
}

/// Reconocimiento de voz (micrófono). Con sesión en el servidor graba el audio
/// y lo transcribe con la IA (OpenAI, mejor en chino/japonés/coreano); sin
/// servidor, o en web, usa el motor del sistema. Devuelve el texto reconocido en
/// el idioma pedido; en plataformas sin soporte, `disponible` es false.
class Oido {
  Oido._();
  static final Oido instancia = Oido._();
  final SpeechToText _stt = SpeechToText();
  final AudioRecorder _grabadora = AudioRecorder();
  bool _inicializado = false;
  bool disponible = false;
  void Function()? _onFin;
  String ultimoError = '';

  /// Transcripción con la IA del servidor (se puede apagar desde ajustes).
  static bool nube = true;

  /// Estado de la grabación en la nube.
  bool _grabando = false;
  Timer? _limite;
  void Function(String texto, bool finalizado)? _onTexto;
  String _idiomaGrabacion = 'en';
  /// Último modo usado: 'nube' o 'sistema' (para mostrarlo en la interfaz).
  String modo = 'sistema';

  Future<bool> preparar() async {
    if (_inicializado) return disponible;
    _inicializado = true;
    try {
      disponible = await _stt.initialize(
        onError: (e) {
          ultimoError = e.errorMsg;
          _onFin?.call();
        },
        onStatus: (st) {
          if (st == 'notListening' || st == 'done') _onFin?.call();
        },
      );
    } catch (_) {
      disponible = false;
    }
    return disponible;
  }

  bool get escuchando => _grabando || _stt.isListening;

  Future<bool> _puedeGrabar() async {
    if (kIsWeb || !nube || !Sync.instancia.conectado) return false;
    try {
      final ok = await _grabadora.hasPermission();
      if (!ok) debugPrint('Oido: sin permiso de micrófono para grabar');
      return ok;
    } catch (e) {
      debugPrint('Oido: grabadora no disponible ($e)');
      return false;
    }
  }

  /// Escucha hasta `segundos` y llama a `onTexto` con resultados parciales y el final.
  /// En modo nube no hay parciales: el texto llega de una vez al terminar (o al llamar a `parar`).
  Future<bool> escuchar(String idioma, void Function(String texto, bool finalizado) onTexto,
      {int segundos = 6, void Function()? onFin}) async {
    ultimoError = '';
    await Voz.instancia.parar();
    if (await _puedeGrabar()) {
      try {
        final dir = await getTemporaryDirectory();
        final ruta = '${dir.path}/onelingo_grabacion.m4a';
        await _grabadora.start(const RecordConfig(encoder: AudioEncoder.aacLc, sampleRate: 16000, numChannels: 1, bitRate: 64000), path: ruta);
        modo = 'nube';
        _grabando = true;
        _onFin = onFin;
        _onTexto = onTexto;
        _idiomaGrabacion = idioma;
        _limite?.cancel();
        _limite = Timer(Duration(seconds: segundos + 2), parar);
        return true;
      } catch (e) {
        ultimoError = '$e';
        debugPrint('Oido: no se pudo grabar ($e); se usa el motor del sistema');
      }
    }
    if (!await preparar()) return false;
    modo = 'sistema';
    _onFin = onFin;
    try {
      await _stt.listen(
        listenOptions: SpeechListenOptions(
          localeId: localeVoz[idioma] ?? 'en-US',
          partialResults: true,
          cancelOnError: true,
          listenFor: Duration(seconds: segundos),
          pauseFor: const Duration(seconds: 2),
        ),
        onResult: (r) => onTexto(r.recognizedWords, r.finalResult),
      );
      return true;
    } catch (_) {
      return false;
    }
  }

  Future<void> parar() async {
    if (_grabando) {
      _grabando = false;
      _limite?.cancel();
      final onTexto = _onTexto;
      final onFin = _onFin;
      _onTexto = null;
      _onFin = null;
      String? texto;
      try {
        final ruta = await _grabadora.stop();
        if (ruta != null) {
          final bytes = await File(ruta).readAsBytes();
          if (bytes.length > 1500) {
            texto = await Sync.instancia.transcribir(bytes, _idiomaGrabacion);
            if (texto == null) ultimoError = Sync.instancia.ultimoError;
          } else {
            ultimoError = 'audio vacío: no se captó sonido del micrófono';
          }
        }
      } catch (e) {
        ultimoError = '$e';
      }
      if (texto != null && texto.isNotEmpty) onTexto?.call(texto, true);
      onFin?.call();
      return;
    }
    try {
      await _stt.stop();
    } catch (_) {}
    _onFin?.call();
    _onFin = null;
  }
}

/// Similitud 0..1 entre lo dicho y lo esperado (palabras coincidentes / esperadas).
double similitud(String dicho, String esperado) {
  String norm(String t) => soloNativo(t).toLowerCase().replaceAll(RegExp(r"[^\p{L}\p{N}\s']", unicode: true), '').trim();
  final a = norm(dicho), b = norm(esperado);
  if (a.isEmpty || b.isEmpty) return 0;
  if (!b.contains(' ')) {
    // Sin espacios (chino/japonés real): comparar caracteres.
    final setB = b.replaceAll(' ', '').split('').toSet();
    final setA = a.replaceAll(' ', '').split('').toSet();
    return setA.intersection(setB).length / setB.length;
  }
  final pb = b.split(RegExp(r'\s+'));
  final pa = a.split(RegExp(r'\s+')).toSet();
  final ok = pb.where(pa.contains).length;
  return ok / pb.length;
}
