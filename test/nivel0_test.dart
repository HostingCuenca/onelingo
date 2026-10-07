import 'dart:convert';
import 'dart:io';

import 'dart:async';

import 'package:audioplayers_platform_interface/audioplayers_platform_interface.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/i18n/i18n.dart';
import 'package:onelingo/core/nivel0/nivel0.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/nivel0/leccion_n0_screen.dart';
import 'package:onelingo/features/nivel0/nivel0_screen.dart';
import 'package:onelingo/features/nivel0/palabra_color.dart';
import 'package:shared_preferences/shared_preferences.dart';

class _Audio extends AudioplayersPlatformInterface {
  final _eventos = StreamController<AudioEvent>.broadcast();
  @override
  Stream<AudioEvent> getEventStream(String id) => _eventos.stream;
  @override
  dynamic noSuchMethod(Invocation invocation) => Future<void>.value();
}

class _AudioGlobal extends GlobalAudioplayersPlatformInterface {
  @override
  Stream<GlobalAudioEvent> getGlobalEventStream() => const Stream.empty();
  @override
  dynamic noSuchMethod(Invocation invocation) => Future<void>.value();
}

Nivel0 cargar([String idioma = 'en', String interfaz = 'es']) {
  // Igual que la app: los textos {es, en} se resuelven al idioma de la interfaz.
  Map<String, dynamic> leer(String archivo) =>
      localizarApoyo(
            jsonDecode(
              File('assets/contenido/$idioma/nivel0/$archivo').readAsStringSync(),
            ),
            interfaz,
          )
          as Map<String, dynamic>;
  return Nivel0.desdeJson(leer('nivel0.json'), leer('sonidos.json'));
}

void main() {
  AudioplayersPlatformInterface.instance = _Audio();
  GlobalAudioplayersPlatformInterface.instance = _AudioGlobal();

  Future<ProviderContainer> montar(
    WidgetTester tester,
    Widget pantalla, {
    String idioma = 'en',
  }) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    SharedPreferences.setMockInitialValues({});
    Efectos.sonido = false;
    addTearDown(() => Efectos.sonido = true);
    final prefs = await SharedPreferences.getInstance();
    final n = cargar(idioma);
    final c = ProviderContainer(
      overrides: [
        prefsProvider.overrideWithValue(prefs),
        nivel0Provider.overrideWith((ref) async => n),
      ],
    );
    addTearDown(c.dispose);
    await tester.pumpWidget(
      UncontrolledProviderScope(
        container: c,
        child: MaterialApp(theme: buildTheme(), home: pantalla),
      ),
    );
    await tester.pumpAndSettle();
    return c;
  }

  Future<void> toca(
    WidgetTester tester,
    String t, {
    bool ultimo = false,
  }) async {
    final f = ultimo ? find.text(t).last : find.text(t).first;
    await tester.ensureVisible(f);
    await tester.pumpAndSettle();
    await tester.tap(f);
    await tester.pumpAndSettle();
  }

  test('Marcado: segmentos, marcas y texto plano', () {
    final s = segmentos('c(a:ey)k(e:*)');
    expect(s.map((x) => x.texto).join(), 'cake');
    expect(s[1].sonido, 'ey');
    expect(s[3].magica, isTrue);
    expect(textoPlano('(sh:=)(i:ih)p'), 'ship');
    expect(segmentos('(k:_)n(ow:ow)')[0].muda, isTrue);
    expect(textoPlano('Hello!'), 'Hello!');
  });

  test('El Nivel 0 español trae cada explicación en inglés', () {
    // El español se explica solo en inglés (como su ruta).
    final r = Process.runSync('python3', [
      'tools/contenido/validar_nivel0.py',
      'es',
      '--bilingue',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
  });

  test('El Nivel 0 francés trae cada explicación en español e inglés', () {
    // Sirve a hispanohablantes y anglohablantes (I18N.md, fase I2).
    final r = Process.runSync('python3', [
      'tools/contenido/validar_nivel0.py',
      'fr',
      '--bilingue',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
  });

  test('El Nivel 0 portugués (pt-BR) trae cada explicación en español e inglés', () {
    // Reinicio desde cero (DEC-035): apoyo bilingüe como el francés.
    final r = Process.runSync('python3', [
      'tools/contenido/validar_nivel0.py',
      'pt',
      '--bilingue',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
    expect('${r.stdout}', isNot(contains('EMOJI QUE FALTAN')));
    final n = cargar('pt');
    expect(n.unidades, hasLength(10));
    expect(n.lecciones, hasLength(40));
    expect(n.sonidos, hasLength(12)); // vocales orales y nasales congeladas
  });

  test('El Nivel 0 alemán trae cada explicación en español e inglés', () {
    // Método ligero (PLAN_ALEMAN.md §3): 16 claves de lectura en 10 unidades.
    final r = Process.runSync('python3', [
      'tools/contenido/validar_nivel0.py',
      'de',
      '--bilingue',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
    expect('${r.stdout}', isNot(contains('EMOJI QUE FALTAN')));
    final n = cargar('de');
    expect(n.unidades, hasLength(10));
    expect(n.lecciones, hasLength(40));
    expect(n.sonidos, hasLength(27)); // vocales, Umlaut, diptongos y consonantes
    // Lumo solo da la bienvenida: nunca en la prueba de salida (u10).
    expect(
      [for (final l in n.unidades.last.lecciones) ...l.pasos.map((p) => p.tipo)],
      isNot(contains('lumo')),
    );
  });

  test('El Nivel 0 italiano trae cada explicación en español e inglés', () {
    final r = Process.runSync('python3', [
      'tools/contenido/validar_nivel0.py',
      'it',
      '--bilingue',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
    expect('${r.stdout}', isNot(contains('EMOJI QUE FALTAN')));
    expect(idiomasConNivel0, contains('it'));
    final n = cargar('it');
    expect(n.idioma, 'it');
    expect(n.unidades, hasLength(10));
    expect(n.lecciones, hasLength(40));
    expect(n.sonidos.length, greaterThanOrEqualTo(15));
    // Lumo solo da la bienvenida: nunca en la prueba de salida (u10).
    expect(
      [for (final l in n.unidades.last.lecciones) ...l.pasos.map((p) => p.tipo)],
      isNot(contains('lumo')),
    );
  });

  test('El Nivel 0 chino trae cada explicación en español e inglés', () {
    final r = Process.runSync('python3', [
      'tools/contenido/validar_nivel0.py',
      'zh',
      '--bilingue',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
    expect('${r.stdout}', isNot(contains('EMOJI QUE FALTAN')));
    expect(idiomasConNivel0, contains('zh'));
    final n = cargar('zh');
    expect(n.idioma, 'zh');
    expect(n.unidades, hasLength(10));
    expect(n.lecciones, hasLength(44));
    expect(n.sonidos.length, greaterThanOrEqualTo(15));
    // Lumo solo da la bienvenida: nunca en la prueba de salida (u10).
    expect(
      [for (final l in n.unidades.last.lecciones) ...l.pasos.map((p) => p.tipo)],
      isNot(contains('lumo')),
    );
  });

  test('Nivel 0 chino: lo que se oye está en chino y coincide con la respuesta', () {
    final n = cargar('zh');
    final hanzi = RegExp(r'[\u4e00-\u9fff]');
    final problemas = <String>[];
    for (final l in n.lecciones) {
      for (final (i, p) in l.pasos.indexed) {
        final id = '${l.id}#$i ${p.tipo}';
        switch (p.tipo) {
          case 'escucha_elige':
            // Se oye `audio` (no `m`) y es la opción correcta, con su pinyin.
            final audio = (p.j['audio'] as String?) ?? '';
            if (!hanzi.hasMatch(audio)) problemas.add('$id: audio «$audio»');
            if (p.opciones[p.correcta].texto != audio) {
              problemas.add('$id: el audio no es la opción correcta');
            }
            if (p.opciones[p.correcta].rom == null) problemas.add('$id: sin rom');
          case 'toca_sonido' || 'escucha':
            final ws = p.tipo == 'escucha' ? p.palabras : p.opciones;
            for (final w in ws) {
              if (!hanzi.hasMatch(w.texto) || w.rom == null) {
                problemas.add('$id: «${w.texto}» sin chino o sin rom');
              }
            }
          case 'mira' || 'repite' || 'construye' || 'elige_significado':
            if (!hanzi.hasMatch(textoPlano(p.marcado)) || p.rom == null) {
              problemas.add('$id: «${p.marcado}» sin chino o sin rom');
            }
          case 'deletreo':
            // Lo que suena es `palabra`; con solo `m` saldría mudo.
            if (((p.j['palabra'] as String?) ?? '').isEmpty) {
              problemas.add('$id: deletreo sin «palabra»');
            }
        }
      }
    }
    expect(problemas, isEmpty, reason: problemas.join('\n'));
  });

  test('El Nivel 0 japonés trae cada explicación en español e inglés', () {
    final r = Process.runSync('python3', [
      'tools/contenido/validar_nivel0.py',
      'ja',
      '--bilingue',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
    expect('${r.stdout}', isNot(contains('EMOJI QUE FALTAN')));
    expect(idiomasConNivel0, contains('ja'));
    final n = cargar('ja');
    expect(n.idioma, 'ja');
    expect(n.unidades, hasLength(10));
    expect(n.lecciones, hasLength(43));
    expect(n.sonidos.length, greaterThanOrEqualTo(15));
    // Lumo solo da la bienvenida: nunca en la prueba de salida (u10).
    expect(
      [for (final l in n.unidades.last.lecciones) ...l.pasos.map((p) => p.tipo)],
      isNot(contains('lumo')),
    );
  });

  test('Nivel 0 japonés: lo que se oye está en kana y coincide con la respuesta', () {
    final n = cargar('ja');
    final kana = RegExp(r'[ぁ-ゖァ-ヺー]');
    final kanji = RegExp(r'[一-鿿]');
    final problemas = <String>[];
    for (final l in n.lecciones) {
      for (final (i, p) in l.pasos.indexed) {
        final id = '${l.id}#$i ${p.tipo}';
        switch (p.tipo) {
          case 'escucha_elige':
            // Se oye `audio` (no `m`) y es la opción correcta; las opciones
            // no llevan rōmaji (la delatarían).
            final audio = (p.j['audio'] as String?) ?? '';
            if (!kana.hasMatch(audio)) problemas.add('$id: audio «$audio»');
            if (p.opciones[p.correcta].texto != audio) {
              problemas.add('$id: el audio no es la opción correcta');
            }
          case 'toca_sonido':
            for (final w in p.opciones) {
              if (!kana.hasMatch(w.texto)) problemas.add('$id: «${w.texto}» sin kana');
            }
          case 'escucha':
            for (final w in p.palabras) {
              if (!kana.hasMatch(w.texto) || w.rom == null) {
                problemas.add('$id: «${w.texto}» sin kana o sin rom');
              }
            }
          case 'mira' || 'repite' || 'mezcla' || 'construye' || 'elige_significado':
            if (!kana.hasMatch(textoPlano(p.marcado)) || p.rom == null) {
              problemas.add('$id: «${p.marcado}» sin kana o sin rom');
            }
          case 'lee':
            if (!kana.hasMatch(textoPlano(p.marcado)) || p.rom == null) {
              problemas.add('$id: «${p.marcado}» sin kana o sin rom');
            }
            for (final w in p.opciones) {
              if (!kana.hasMatch(w.texto)) problemas.add('$id: «${w.texto}» sin kana');
            }
          case 'escucha_letra':
            // Suena `letra` (kana suelto) y está entre las opciones.
            final letra = (p.j['letra'] as String?) ?? '';
            if (!kana.hasMatch(letra) || !p.textos.contains(letra)) {
              problemas.add('$id: la letra «$letra» no está en las opciones');
            }
            if (p.letraRom == null) problemas.add('$id: sin letraRom');
        }
        // Ningún kanji en el japonés del Nivel 0 (solo kana); las explicaciones
        // en es/en pueden citarlos.
        final soloJa = [
          p.marcado, p.j['audio'], p.j['letra'], p.j['de'], p.j['a'],
          ...p.palabras.map((w) => w.marcado), ...p.textos, ...p.fichas,
        ].whereType<String>().join();
        if (kanji.hasMatch(soloJa)) problemas.add('$id: kanji en el japonés');
      }
    }
    expect(problemas, isEmpty, reason: problemas.join('\n'));
  });

  for (final idioma in idiomasConNivel0)
  test('Contenido del Nivel 0 ($idioma) coherente (sonidos, imágenes y respuestas)', () {
    final n = cargar(idioma);
    expect(n.idioma, idioma);
    expect(n.unidades, isNotEmpty);
    // El portugués de Brasil congela 12 IDs vocálicos (7 orales + 5 nasales).
    expect(n.sonidos.length, greaterThanOrEqualTo(idioma == 'pt' ? 12 : 15));
    final problemas = <String>[];
    void marcado(String id, String m) {
      for (final s in segmentos(m)) {
        if (s.clave != null &&
            !s.muda &&
            !s.digrafo &&
            !s.magica &&
            n.porId[s.clave] == null) {
          problemas.add('$id: sonido desconocido «${s.clave}» en $m');
        }
      }
    }

    void emoji(String id, String? e) {
      if (e != null && !File('assets/img/emoji/$e.webp').existsSync())
        problemas.add('$id: falta imagen $e');
    }

    for (final s in n.sonidos) {
      emoji(s.id, s.emoji);
    }
    final ids = <String>{};
    for (final l in n.lecciones) {
      if (!ids.add(l.id)) problemas.add('id repetido ${l.id}');
      expect(l.pasos, isNotEmpty, reason: l.id);
      for (final (i, p) in l.pasos.indexed) {
        final id = '${l.id}#$i ${p.tipo}';
        // Solo tipos que LeccionN0Screen sabe mostrar (si no, sale Lumo).
        if (!const {
          'lumo', 'escucha', 'mira', 'mezcla', 'repite', 'letras',
          'escucha_elige', 'toca_sonido', 'elige_significado',
          'escucha_letra', 'deletreo', 'lee', 'construye', 'cambia',
        }.contains(p.tipo)) {
          problemas.add('$id: tipo desconocido');
        }
        marcado(id, p.marcado);
        for (final w in [...p.palabras, ...p.opciones]) {
          marcado(id, w.marcado);
          emoji(id, w.emoji);
        }
        switch (p.tipo) {
          case 'escucha_elige':
            final audio = p.j['audio'] as String;
            if (p.opciones[p.correcta].texto.toLowerCase() !=
                audio.toLowerCase()) {
              problemas.add('$id: el audio «$audio» no es la opción correcta');
            }
          case 'toca_sonido':
            final buena = segmentos(p.opciones[p.correcta].marcado)
                .any((s) => s.sonido == p.sonido);
            if (!buena)
              problemas.add(
                '$id: la opción correcta no tiene el sonido ${p.sonido}',
              );
            for (final (k, o) in p.opciones.indexed) {
              if (k != p.correcta &&
                  segmentos(o.marcado).any((s) => s.sonido == p.sonido)) {
                problemas.add('$id: la opción $k también tiene el sonido');
              }
            }
          case 'construye':
            final objetivo = textoPlano(p.marcado);
            final fichas = [...p.fichas];
            for (final c in objetivo.split('')) {
              if (!fichas.remove(c))
                problemas.add('$id: faltan fichas para «$objetivo»');
            }
          case 'cambia':
            final de = textoPlano(p.j['de'] as String),
                a = textoPlano(p.j['a'] as String);
            final difs = [
              for (var k = 0; k < de.length; k++)
                if (k < a.length && de[k] != a[k]) k,
            ];
            if (de.length != a.length || difs.length != 1)
              problemas.add('$id: «$de»→«$a» debe cambiar una letra');
            if (difs.isNotEmpty && !p.textos.contains(a[difs.first]))
              problemas.add('$id: falta la letra correcta');
          case 'escucha_letra':
            if (!p.textos.contains(p.j['letra']))
              problemas.add('$id: la letra no está en las opciones');
          case 'deletreo' || 'elige_significado' || 'lee':
            if (p.correcta >=
                (p.tipo == 'lee' ? p.opciones.length : p.textos.length))
              problemas.add('$id: índice correcto inválido');
        }
      }
    }
    expect(problemas, isEmpty, reason: problemas.join('\n'));
  });

  testWidgets('PalabraColor pinta cada vocal con el color de su sonido', (
    tester,
  ) async {
    final n = cargar();
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(body: PalabraColor('c(a:ey)k(e:*)', nivel: n)),
      ),
    );
    final rich = tester.widget<Text>(find.byType(Text)).textSpan! as TextSpan;
    final spans = rich.children!.cast<TextSpan>();
    expect(spans.map((s) => s.text).join(), 'cake');
    expect(spans[1].style!.color, n.porId['ey']!.color);
    expect(spans[3].style!.color!.a, lessThan(.6)); // e mágica tenue
  });

  testWidgets(
    'Nivel 0: la primera lección está abierta y las demás bloqueadas',
    (tester) async {
      await montar(tester, const Nivel0Screen());
      expect(find.text('EMPEZAR'), findsOneWidget);
      expect(find.text('Mapa de sonidos'), findsOneWidget);
      expect(find.byIcon(Icons.play_circle_fill_rounded), findsOneWidget);
      expect(find.byIcon(Icons.lock_rounded), findsWidgets);
    },
  );

  testWidgets('Nivel 0 chino: la lección muestra caracteres con su pinyin', (
    tester,
  ) async {
    await montar(
      tester,
      const LeccionN0Screen(leccionId: 'u01l02'),
      idioma: 'zh',
    );
    expect(tester.takeException(), isNull);
    // Primer paso (escucha): palabras en chino con su pinyin.
    final escucha = cargar('zh').leccion('u01l02')!.pasos.first;
    expect(escucha.tipo, 'escucha');
    final w = escucha.palabras.first;
    expect(find.textContaining(w.rom!), findsWidgets);
  });

  testWidgets('Nivel 0 japonés: la lección muestra kana con su rōmaji', (
    tester,
  ) async {
    await montar(
      tester,
      const LeccionN0Screen(leccionId: 'u01l02'),
      idioma: 'ja',
    );
    expect(tester.takeException(), isNull);
    // Primer paso (escucha): palabras en kana con su rōmaji.
    final escucha = cargar('ja').leccion('u01l02')!.pasos.first;
    expect(escucha.tipo, 'escucha');
    final w = escucha.palabras.first;
    expect(find.textContaining(w.rom!), findsWidgets);
  });

  testWidgets('Lección completa: escuchar, elegir y registrar el progreso', (
    tester,
  ) async {
    final c = await montar(tester, const LeccionN0Screen(leccionId: 'u01.l02'));
    await toca(tester, 'SIGUIENTE'); // escucha (la primera ya sonó)
    await toca(tester, 'SALTAR'); // repite sin micrófono
    await toca(tester, 'please');
    await toca(tester, 'COMPROBAR');
    expect(find.text('¡Muy bien!'), findsOneWidget);
    await toca(tester, 'SIGUIENTE', ultimo: true);
    await toca(tester, 'yes');
    await toca(tester, 'COMPROBAR');
    await toca(tester, 'SIGUIENTE', ultimo: true);
    await toca(tester, 'SALTAR');
    await toca(tester, 'gracias');
    await toca(tester, 'COMPROBAR');
    await toca(tester, 'SIGUIENTE', ultimo: true);
    expect(find.text('¡Lección completada!'), findsOneWidget);
    expect(find.text('3 de 3 respuestas bien'), findsOneWidget);
    expect(
      leccionN0Completa(c.read(progressProvider).practicas, 'en', 'u01.l02'),
      isTrue,
    );
  });
}
