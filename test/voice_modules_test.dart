import 'dart:async';
import 'package:flutter_test/flutter_test.dart';
// Interface used only to replace the installed audio plugin in tests.
// ignore: depend_on_referenced_packages
import 'package:audioplayers_platform_interface/audioplayers_platform_interface.dart';
import 'package:onelingo/core/voz.dart';

class AudioPlatform extends AudioplayersPlatformInterface {
  final events = StreamController<AudioEvent>.broadcast();
  final sources = <String>[];
  bool prepare = true;
  Completer<void>? requested;
  int resumes = 0;
  @override Future<void> create(String id) async {}
  @override Stream<AudioEvent> getEventStream(String id) => events.stream;
  @override Future<void> setSourceUrl(String id, String url, {bool? isLocal, String? mimeType}) async {
    sources.add(url); requested?.complete();
    if (prepare) ready();
  }
  void ready() => events.add(const AudioEvent(eventType: AudioEventType.prepared, isPrepared: true));
  @override Future<void> resume(String id) async { resumes++; }
  @override Future<int?> getCurrentPosition(String id) async => 0;
  @override Future<int?> getDuration(String id) async => 1000;
  @override dynamic noSuchMethod(Invocation invocation) => Future<void>.value();
}
class GlobalPlatform extends GlobalAudioplayersPlatformInterface {
  @override Stream<GlobalAudioEvent> getGlobalEventStream() => const Stream.empty();
  @override dynamic noSuchMethod(Invocation invocation) => Future<void>.value();
}
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final platform = AudioPlatform();
  AudioplayersPlatformInterface.instance = platform;
  GlobalAudioplayersPlatformInterface.instance = GlobalPlatform();
  test('diagnóstico, biblioteca y lecciones usan streaming por defecto', () async {
    expect(await VozNube.instancia.reproducir('Hello', 'en', lento: true), true);
    expect(Uri.parse(platform.sources.last).path, endsWith('/voz/stream'));
    expect(platform.resumes, 1);
    await VozNube.instancia.parar();
  });
  test('cancelar mientras se prepara audio no cuenta como escuchado ni reanuda', () async {
    platform.prepare = false; platform.requested = Completer<void>();
    final previous = platform.resumes;
    final pending = VozNube.instancia.reproducir('Wait', 'en');
    await platform.requested!.future;
    await VozNube.instancia.parar();
    platform.ready();
    expect(await pending, false);
    expect(platform.resumes, previous);
  });
  test('el modo letra viaja al servidor', () async {
    platform.prepare = true; platform.requested = null;
    expect(await VozNube.instancia.reproducir('H', 'es', modo: 'letra'), true);
    expect(Uri.parse(platform.sources.last).queryParameters['modo'], 'letra');
    await VozNube.instancia.parar();
  });
  test('la voz del dispositivo (respaldo) recibe letras sueltas en minúscula', () {
    // Con «A» dice «A mayúscula»; con «a», el nombre de la letra.
    expect(paraVozDelSistema('A'), 'a');
    expect(paraVozDelSistema('Я.'), 'я');
    expect(paraVozDelSistema('Hola'), 'Hola');
    expect(paraVozDelSistema('あ'), 'あ');
  });
}
