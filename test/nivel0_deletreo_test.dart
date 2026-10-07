import 'dart:async';
import 'dart:convert';
import 'dart:io';

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

Nivel0 cargar(String idioma) {
  Map<String, dynamic> leer(String archivo) => localizarApoyo(
    jsonDecode(
      File('assets/contenido/$idioma/nivel0/$archivo').readAsStringSync(),
    ),
    'es',
  ) as Map<String, dynamic>;
  return Nivel0.desdeJson(
    leer('nivel0.json'),
    leer('sonidos.json'),
    idioma: idioma,
  );
}

/// El paso `deletreo` real de [idioma] cuya palabra (`m` o `palabra`) es [w],
/// metido solo en una lección de prueba.
Nivel0 conPaso(String idioma, String w) {
  final base = cargar(idioma);
  final paso = [for (final l in base.lecciones) ...l.pasos].firstWhere(
    (p) => p.tipo == 'deletreo' && (p.j['palabra'] ?? p.j['m']) == w,
  );
  return Nivel0(
    idioma: base.idioma,
    titulo: base.titulo,
    subtitulo: base.subtitulo,
    voz: base.voz,
    sonidos: base.sonidos,
    unidades: [
      UnidadN0('u', 'u', 'o', [
        LeccionN0('x', 'x', [paso]),
      ]),
    ],
  );
}

void main() {
  AudioplayersPlatformInterface.instance = _Audio();
  GlobalAudioplayersPlatformInterface.instance = _AudioGlobal();

  Future<void> montar(WidgetTester tester, Nivel0 n) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    SharedPreferences.setMockInitialValues({});
    Efectos.sonido = false;
    addTearDown(() => Efectos.sonido = true);
    final prefs = await SharedPreferences.getInstance();
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
        child: MaterialApp(
          theme: buildTheme(),
          home: const LeccionN0Screen(leccionId: 'x'),
        ),
      ),
    );
    await tester.pumpAndSettle();
  }

  /// Letras de las fichas, en el orden en que están en pantalla.
  List<String> fichas(WidgetTester tester) {
    final r = <String>[];
    for (
      var i = 0;
      find.byKey(ValueKey('ficha$i')).evaluate().isNotEmpty;
      i++
    ) {
      r.add(
        tester
            .widget<Text>(
              find.descendant(
                of: find.byKey(ValueKey('ficha$i')),
                matching: find.byType(Text),
              ),
            )
            .data!,
      );
    }
    return r;
  }

  /// Toca las fichas de [secuencia] en ese orden. Con letras repetidas usa la
  /// primera ficha libre (o la última si [ultima]).
  Future<void> ordena(
    WidgetTester tester,
    List<String> secuencia, {
    bool ultima = false,
  }) async {
    final f = fichas(tester);
    final usadas = <int>{};
    for (final l in secuencia) {
      final libres = [
        for (var i = 0; i < f.length; i++)
          if (f[i] == l && !usadas.contains(i)) i,
      ];
      final i = ultima ? libres.last : libres.first;
      usadas.add(i);
      final w = find.byKey(ValueKey('ficha$i'));
      await tester.ensureVisible(w);
      await tester.tap(w);
      await tester.pumpAndSettle();
    }
  }

  Future<void> comprueba(WidgetTester tester) async {
    final b = find.text('COMPROBAR');
    await tester.ensureVisible(b);
    await tester.tap(b);
    await tester.pumpAndSettle();
  }

  for (final ultima in [false, true]) {
    testWidgets(
      'Formato B latino (it «Anna»): cualquier N vale (ultima=$ultima)',
      (tester) async {
        await montar(tester, conPaso('it', 'Anna'));
        expect(tester.takeException(), isNull);
        expect(find.textContaining('Anna'), findsWidgets); // título
        expect(find.byKey(const ValueKey('hueco3')), findsOneWidget);
        expect(find.byKey(const ValueKey('hueco4')), findsNothing);
        expect(fichas(tester), unorderedEquals(['A', 'A', 'N', 'N']));
        await ordena(tester, ['A', 'N', 'N', 'A'], ultima: ultima);
        await comprueba(tester);
        expect(find.text('¡Muy bien!'), findsOneWidget);
      },
    );
  }

  testWidgets(
    'Formato B latino: mal ordenado se corrige y nunca sale resuelto',
    (tester) async {
      await montar(tester, conPaso('it', 'Luca'));
      expect(fichas(tester), isNot(['L', 'U', 'C', 'A']));
      await ordena(tester, ['A', 'C', 'U', 'L']);
      await comprueba(tester);
      expect(find.text('Casi, mira cómo es'), findsOneWidget);
      expect(find.text('Luca'), findsOneWidget); // palabra en el panel
    },
  );

  testWidgets('Formato B con 6 fichas cabe en pantalla (it «Chiara»)', (
    tester,
  ) async {
    await montar(tester, conPaso('it', 'Chiara'));
    expect(tester.takeException(), isNull);
    expect(fichas(tester), isNot(['C', 'H', 'I', 'A', 'R', 'A']));
    await ordena(tester, ['C', 'H', 'I', 'A', 'R', 'A']);
    await comprueba(tester);
    expect(find.text('¡Muy bien!'), findsOneWidget);
  });

  testWidgets('Formato B coreano (jamo): ordena 나무', (tester) async {
    await montar(tester, conPaso('ko', '나무'));
    expect(tester.takeException(), isNull);
    expect(fichas(tester), unorderedEquals(['ㄴ', 'ㅏ', 'ㅁ', 'ㅜ']));
    await ordena(tester, ['ㄴ', 'ㅏ', 'ㅁ', 'ㅜ']);
    await comprueba(tester);
    expect(find.text('¡Muy bien!'), findsOneWidget);
    expect(find.text('나무'), findsOneWidget);
  });

  testWidgets('Formato B coreano: 안녕 (6 jamo, dos ㄴ y dos ㅇ)', (tester) async {
    await montar(tester, conPaso('ko', '안녕'));
    expect(tester.takeException(), isNull);
    await ordena(tester, ['ㅇ', 'ㅏ', 'ㄴ', 'ㄴ', 'ㅕ', 'ㅇ'], ultima: true);
    await comprueba(tester);
    expect(find.text('¡Muy bien!'), findsOneWidget);
  });

  testWidgets('Formato A (en): sigue siendo elegir entre palabras', (
    tester,
  ) async {
    await montar(tester, conPaso('en', 'ANA'));
    expect(tester.takeException(), isNull);
    expect(find.byKey(const ValueKey('hueco0')), findsNothing);
    for (final o in ['ANA', 'ANN', 'AMA']) {
      expect(find.text(o), findsOneWidget);
    }
    await tester.tap(find.text('ANN'));
    await tester.pumpAndSettle();
    await comprueba(tester);
    expect(find.text('Casi, mira cómo es'), findsOneWidget);
  });

  test(
    'Formato B con opciones largas (pt, correos) sigue siendo de elegir',
    () {
      final pt = cargar('pt');
      final pasos = [
        for (final l in pt.lecciones)
          for (final p in l.pasos)
            if (p.tipo == 'deletreo') p,
      ];
      expect(pasos.where(esDeletreoOrdena), isNotEmpty);
      expect(
        pasos.where((p) => p.marcado.contains('@')).any(esDeletreoOrdena),
        isFalse,
      );
    },
  );

  test(
    'Todos los pasos deletreo de todos los idiomas tienen datos válidos',
    () {
      var total = 0, ordena = 0;
      final problemas = <String>[];
      void recorre(String f, Object? o) {
        if (o is Map) {
          if (o['tipo'] == 'deletreo') {
            total++;
            final op = o['opciones'];
            final tieneOpciones = op is List && op.isNotEmpty;
            final a =
                o['palabra'] is String &&
                (o['palabra'] as String).isNotEmpty &&
                tieneOpciones;
            final b =
                o['m'] is String &&
                (o['m'] as String).isNotEmpty &&
                tieneOpciones;
            if (!a && !b) problemas.add('$f: ${jsonEncode(o)}');
            if (b && !a) {
              final p = PasoN0('deletreo', Map<String, dynamic>.from(o));
              if (esDeletreoOrdena(p)) ordena++;
            }
          }
          for (final v in o.values) {
            recorre(f, v);
          }
        } else if (o is List) {
          for (final v in o) {
            recorre(f, v);
          }
        }
      }

      final archivos = Directory('assets/contenido')
          .listSync()
          .whereType<Directory>()
          .map((d) => Directory('${d.path}/nivel0'))
          .where((d) => d.existsSync())
          .expand((d) => d.listSync().whereType<File>())
          .where((f) => f.path.endsWith('.json'));
      for (final f in archivos) {
        recorre(f.path, jsonDecode(f.readAsStringSync()));
      }
      expect(problemas, isEmpty);
      expect(total, greaterThanOrEqualTo(20));
      expect(ordena, greaterThanOrEqualTo(17));
    },
  );
}
