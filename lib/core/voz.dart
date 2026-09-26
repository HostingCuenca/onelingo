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
import 'silencio.dart';
import 'blob_cleanup_stub.dart'
    if (dart.library.js_interop) 'blob_cleanup_web.dart';
import 'efectos.dart';
import 'content/idiomas.dart';

/// Voz de la app. Primero intenta la voz natural del servidor (ElevenLabs, con
/// caché en el servidor y en el dispositivo); si no hay sesión o falla, usa el
/// motor del sistema (flutter_tts). Un solo objeto para toda la app.
class Voz {
  Voz._();
  static final Voz instancia = Voz._();
  final FlutterTts _tts = FlutterTts();
  String? _localeActual;
  bool _ttsUsado = false;
  int _solicitud = 0;

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
  Future<void> hablar(
    String texto,
    String idioma, {
    double? velocidad,
    String? voz,
    bool progresivo = true,
  }) async {
    final solicitud = ++_solicitud;
    await Efectos.detener();
    if (solicitud != _solicitud) return;
    final limpio = soloNativo(texto);
    if (limpio.isEmpty) return;
    if (natural && Sync.instancia.conectado) {
      await _tts.stop().catchError((_) {});
      if (solicitud != _solicitud) return;
      final ok = await VozNube.instancia.reproducir(
        limpio,
        idioma,
        voz: voz ?? 'narradora',
        progresivo: progresivo,
        lento: (velocidad ?? 1) <= 0.4,
      );
      if (ok || solicitud != _solicitud) return;
    }
    try {
      await _preparar(idioma);
      if (solicitud != _solicitud) return;
      if (velocidad != null) await _tts.setSpeechRate(velocidad);
      await _tts.stop();
      _ttsUsado = true;
      await _tts.speak(limpio);
    } catch (_) {
      // Sin motor de voz disponible (p. ej. simulador sin voces): se ignora.
    }
  }

  Future<void> parar() async {
    _solicitud++;
    await VozNube.instancia.parar();
    if (!_ttsUsado) return;
    try {
      await _tts.stop();
      _ttsUsado = false;
    } catch (_) {}
  }
}

/// Voz natural servida por el backend (`GET /voz`). Cada frase se pide una sola
/// vez: el servidor transmite con ElevenLabs y la guarda al completarla.
/// En nativo se aprovechan también los archivos ya descargados.
class VozNube {
  VozNube._();
  static final VozNube instancia = VozNube._();
  final AudioPlayer _player = AudioPlayer()..setReleaseMode(ReleaseMode.stop);
  final Map<String, Future<String?>> _enCurso = {};
  String? _dir;
  String ultimoError = '';
  int _turno = 0;

  String _clave(String texto, String idioma, String voz) =>
      sha1.convert(utf8.encode('$voz|$idioma|$texto')).toString();

  Uri _url(String texto, String idioma, String voz, {bool conToken = false}) =>
      Uri.parse('${Sync.baseUrl}/voz').replace(
        queryParameters: {
          'texto': texto,
          'idioma': idioma,
          'voz': voz,
          if (conToken) 'token': Sync.instancia.token ?? '',
        },
      );

  Future<String?> _archivoLocal(String texto, String idioma, String voz) async {
    if (kIsWeb) return null;
    try {
      _dir ??= '${(await getTemporaryDirectory()).path}/onelingo_voz';
      final f = File('$_dir/${_clave(texto, idioma, voz)}.mp3');
      return await f.exists() && await f.length() > 0 ? f.path : null;
    } catch (_) {
      return null;
    }
  }

  /// Descarga (o recupera de la caché local) el MP3 y devuelve su ruta; null si falla.
  Future<String?> _archivo(String texto, String idioma, String voz) {
    final k = _clave(texto, idioma, voz);
    return _enCurso.putIfAbsent(k, () async {
      try {
        _dir ??= '${(await getTemporaryDirectory()).path}/onelingo_voz';
        final f = File('$_dir/$k.mp3');
        if (await f.exists() && await f.length() > 0) return f.path;
        final r = await http
            .get(
              _url(texto, idioma, voz),
              headers: {'authorization': 'Bearer ${Sync.instancia.token}'},
            )
            .timeout(const Duration(seconds: 15));
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
  Future<bool> reproducir(
    String texto,
    String idioma, {
    String voz = 'narradora',
    bool lento = false,
    bool progresivo = true,
  }) async {
    final mio = ++_turno;
    ultimoError = '';
    await Efectos.detener();
    if (mio != _turno) return false;
    try {
      await _player.stop();
      await _player.setPlaybackRate(lento ? 0.8 : 1.0);
      if (mio != _turno) return false;
      final local = await _archivoLocal(texto, idioma, voz);
      if (mio != _turno) return false;
      if (local != null) {
        await _player.play(DeviceFileSource(local));
        return mio == _turno;
      }
      if (kIsWeb || progresivo) {
        final url = _url(texto, idioma, voz, conToken: true);
        await _player.play(
          UrlSource(
            (progresivo ? url.replace(path: '${url.path}/stream') : url)
                .toString(),
          ),
        );
        return mio == _turno;
      }
      final ruta = await _archivo(texto, idioma, voz);
      if (ruta == null || mio != _turno) {
        return false; // Cancelar no equivale a haber escuchado.
      }
      await _player.play(DeviceFileSource(ruta));
      return mio == _turno;
    } catch (e) {
      ultimoError = '$e';
      return false;
    }
  }

  /// Descarga en segundo plano las frases de una lección para que suenen al instante.
  void precargar(
    Iterable<String> textos,
    String idioma, {
    String voz = 'narradora',
  }) {
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
/// y lo transcribe con la IA. El chat web graba para controlar el silencio;
/// otras actividades web pueden usar el motor del sistema. Devuelve el texto reconocido en
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
  int _sesion = 0;
  StreamSubscription<Amplitude>? _amplitud;
  void Function()? _onProcesando;

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

  Future<bool> _puedeGrabar({bool permitirWeb = false}) async {
    if ((kIsWeb && !permitirWeb) || !nube || !Sync.instancia.conectado) {
      return false;
    }
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
  Future<bool> escuchar(
    String idioma,
    void Function(String texto, bool finalizado) onTexto, {
    int segundos = 6,
    Duration? silencio,
    void Function()? onProcesando,
    void Function()? onFin,
  }) async {
    final sesion = ++_sesion;
    ultimoError = '';
    await Efectos.detener();
    await Voz.instancia.parar();
    if (sesion != _sesion) return false;
    final puedeGrabar = await _puedeGrabar(permitirWeb: silencio != null);
    if (sesion != _sesion) return false;
    if (puedeGrabar) {
      try {
        final dir = kIsWeb ? null : await getTemporaryDirectory();
        if (sesion != _sesion) return false;
        final ruta = kIsWeb ? '' : '${dir!.path}/onelingo_grabacion.m4a';
        await _grabadora.start(
          const RecordConfig(
            encoder: kIsWeb ? AudioEncoder.wav : AudioEncoder.aacLc,
            echoCancel: true,
            noiseSuppress: true,
            autoGain: true,
            sampleRate: 16000,
            numChannels: 1,
            bitRate: 64000,
          ),
          path: ruta,
        );
        if (sesion != _sesion) {
          await _grabadora.cancel();
          return false;
        }
        if (!await _grabadora.isRecording()) {
          throw StateError('No se inició el micrófono');
        }
        if (sesion != _sesion) {
          await _grabadora.cancel();
          return false;
        }
        modo = 'nube';
        _grabando = true;
        _onProcesando = onProcesando;
        _onFin = onFin;
        _onTexto = (texto, fin) {
          if (sesion == _sesion) onTexto(texto, fin);
        };
        _idiomaGrabacion = idioma;
        _limite?.cancel();
        _limite = Timer(
          Duration(seconds: silencio == null ? segundos + 2 : segundos),
          parar,
        );
        await _amplitud?.cancel();
        if (sesion != _sesion) return false;
        if (silencio != null) {
          final detector = FinPorSilencio(pausa: silencio);
          final reloj = Stopwatch()..start();
          _amplitud = _grabadora
              .onAmplitudeChanged(const Duration(milliseconds: 200))
              .listen(
                (a) {
                  if (sesion == _sesion &&
                      _grabando &&
                      detector.actualizar(a.current, reloj.elapsed)) {
                    parar();
                  }
                },
                onError: (Object _) {
                  /* Manual stop remains available. */
                },
              );
        }
        return true;
      } catch (e) {
        ultimoError = '$e';
        _grabando = false;
        _limite?.cancel();
        await _grabadora.cancel().catchError((_) {});
        if (kIsWeb && silencio != null) return false;
        debugPrint('Oido: no se pudo grabar ($e); se usa el motor del sistema');
      }
    }
    if (kIsWeb && silencio != null) {
      ultimoError = 'Revisa el permiso del micrófono y tu sesión.';
      return false;
    }
    if (!await preparar() || sesion != _sesion) return false;
    modo = 'sistema';
    _onFin = onFin;
    try {
      await _stt.listen(
        listenOptions: SpeechListenOptions(
          localeId: localeVoz[idioma] ?? 'en-US',
          partialResults: true,
          cancelOnError: true,
          listenFor: Duration(seconds: segundos),
          pauseFor: silencio ?? const Duration(seconds: 3),
        ),
        onResult: (r) {
          if (sesion == _sesion) onTexto(r.recognizedWords, r.finalResult);
        },
      );
      return true;
    } catch (_) {
      return false;
    }
  }

  /// Abandona el ejercicio sin enviar una grabación a transcribir.
  Future<void> cancelar() async {
    _sesion++;
    _limite?.cancel();
    final amplitud = _amplitud;
    _amplitud = null;
    _onProcesando = null;
    _onTexto = null;
    _onFin = null;
    _grabando = false;
    await amplitud?.cancel();
    try {
      await _grabadora.cancel();
    } catch (_) {}
    try {
      await _stt.cancel();
    } catch (_) {}
  }

  Future<void> parar() async {
    if (_grabando) {
      final sesion = _sesion;
      _grabando = false;
      _limite?.cancel();
      final onTexto = _onTexto;
      final onFin = _onFin;
      _onProcesando?.call();
      _onProcesando = null;
      final amplitud = _amplitud;
      _amplitud = null;
      _onTexto = null;
      _onFin = null;
      await amplitud?.cancel();
      if (sesion != _sesion) return;
      String? texto;
      try {
        final ruta = await _grabadora.stop();
        if (ruta != null) {
          final bytes = kIsWeb
              ? await (() async {
                  try {
                    return (await http.get(Uri.parse(ruta))).bodyBytes;
                  } finally {
                    liberarBlob(ruta);
                  }
                })()
              : await File(ruta).readAsBytes();
          if (sesion != _sesion) return;
          if (bytes.length > 1500) {
            texto = await Sync.instancia.transcribir(
              bytes,
              _idiomaGrabacion,
              nombre: kIsWeb ? 'voz.wav' : 'voz.m4a',
              tipo: kIsWeb ? 'audio/wav' : 'audio/m4a',
            );
            if (texto == null) ultimoError = Sync.instancia.ultimoError;
          } else {
            ultimoError = 'audio vacío: no se captó sonido del micrófono';
          }
        }
      } catch (e) {
        ultimoError = '$e';
      }
      if (sesion != _sesion) return;
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

/// Coincidencia textual 0..1 para repetición; no mide pronunciación ni fluidez.
double similitud(String dicho, String esperado) {
  String norm(String t) {
    var value = soloNativo(t).toLowerCase().replaceAll(RegExp('[’‘]'), "'");
    // Solo equivalencias inglesas no ambiguas. 's y 'd no se expanden:
    // pueden representar verbos distintos o un posesivo.
    const contractions = {
      "i'm": 'i am',
      "you're": 'you are',
      "we're": 'we are',
      "they're": 'they are',
      "isn't": 'is not',
      "aren't": 'are not',
      "wasn't": 'was not',
      "weren't": 'were not',
      "don't": 'do not',
      "doesn't": 'does not',
      "didn't": 'did not',
      "haven't": 'have not',
      "hasn't": 'has not',
      "hadn't": 'had not',
      "can't": 'can not',
      'cannot': 'can not',
      "won't": 'will not',
      "wouldn't": 'would not',
      "couldn't": 'could not',
      "shouldn't": 'should not',
      "mustn't": 'must not',
      "needn't": 'need not',
      "let's": 'let us',
      "i've": 'i have',
      "you've": 'you have',
      "we've": 'we have',
      "they've": 'they have',
      "i'll": 'i will',
      "you'll": 'you will',
      "he'll": 'he will',
      "she'll": 'she will',
      "it'll": 'it will',
      "we'll": 'we will',
      "they'll": 'they will',
    };
    value = value.replaceAllMapped(
      RegExp(r"\b[a-z]+(?:'[a-z]+)?\b"),
      (m) => contractions[m[0]] ?? m[0]!,
    );
    return value
        .replaceAll(RegExp(r"[^\p{L}\p{N}\s']", unicode: true), ' ')
        .replaceAll(RegExp(r'\s+'), ' ')
        .trim();
  }

  final a = norm(dicho), b = norm(esperado);
  if (a.isEmpty || b.isEmpty) return 0;
  if (a == b) return 1;
  final wordsA = a.split(' '), wordsB = b.split(' ');
  // Impedir que una negación añadida/omitida pase por alta coincidencia.
  // Es una protección textual inglesa (y "no"), no análisis semántico universal.
  const negatives = {
    'not',
    'no',
    'never',
    'nothing',
    'nobody',
    'nowhere',
    'neither',
    'nor',
  };
  final negationChanged =
      wordsA.where(negatives.contains).join(' ') !=
      wordsB.where(negatives.contains).join(' ');
  // Comparar secuencias conserva el orden y las repeticiones. Para palabras
  // aisladas y escrituras sin espacios, usar puntos de código, no conjuntos.
  final useCharacters = !a.contains(' ') && !b.contains(' ');
  final tokensA = useCharacters
      ? a.runes.map(String.fromCharCode).toList()
      : wordsA;
  final tokensB = useCharacters
      ? b.runes.map(String.fromCharCode).toList()
      : wordsB;
  var previous = List<int>.generate(tokensB.length + 1, (i) => i);
  for (var i = 1; i <= tokensA.length; i++) {
    final row = List<int>.filled(tokensB.length + 1, 0)..[0] = i;
    for (var j = 1; j <= tokensB.length; j++) {
      final deletion = previous[j] + 1;
      final insertion = row[j - 1] + 1;
      final replacement =
          previous[j - 1] + (tokensA[i - 1] == tokensB[j - 1] ? 0 : 1);
      final best = deletion < insertion ? deletion : insertion;
      row[j] = best < replacement ? best : replacement;
    }
    previous = row;
  }
  final length = tokensA.length > tokensB.length
      ? tokensA.length
      : tokensB.length;
  final score = 1 - previous.last / length;
  final sortedA = [...tokensA]..sort();
  final sortedB = [...tokensB]..sort();
  final sameTokensReordered =
      sortedA.length == sortedB.length &&
      List.generate(
        sortedA.length,
        (i) => sortedA[i] == sortedB[i],
      ).every((same) => same);
  // La UI usa 0.6: un cambio de polaridad o un reordenamiento completo
  // no debe aprobar por compartir casi todas las palabras.
  return (negationChanged || sameTokensReordered) && score >= .5 ? .49 : score;
}
