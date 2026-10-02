import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:audioplayers_platform_interface/audioplayers_platform_interface.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/aprendizaje/correccion.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/aprendizaje/ubicacion.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/onboarding/ubicacion_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Doble de audio: en pruebas no hay complemento nativo de audioplayers.
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

/// Banco real de la prueba de nivel v2 (assets/contenido/en/diagnostico-v2.json).
void main() {
  AudioplayersPlatformInterface.instance = _Audio();
  GlobalAudioplayersPlatformInterface.instance = _AudioGlobal();
  final banco = ItemUbicacion.banco(
    jsonDecode(
      File('assets/contenido/en/diagnostico-v2.json').readAsStringSync(),
    ) as Map<String, dynamic>,
  );

  test('El banco cubre N1–N10 en las cinco habilidades', () {
    for (var n = 1; n <= 10; n++) {
      for (final h in [...habilidadesUbicacion, 'escritura']) {
        final k = banco.where((i) => i.nivel == n && i.habilidad == h).length;
        expect(k, h == 'escritura' ? 2 : 4, reason: 'N$n $h');
      }
    }
    for (final i in banco.where((i) => i.habilidad != 'escritura')) {
      expect(i.item.opciones.length, inInclusiveRange(3, 4), reason: i.item.id);
      expect(
        i.item.indiceRespuesta != null || i.item.respuesta != null,
        isTrue,
        reason: i.item.id,
      );
    }
  });

  test(
    'Cada ítem se corrige como correcto con su respuesta y como error con otra',
    () {
      for (final u in banco.where((i) => i.habilidad != 'escritura')) {
        final it = u.item;
        if (it.formato == FormatoItem.completar) {
          final otra = it.opciones
              .map((o) => o.meta ?? '')
              .firstWhere((o) => o != it.respuesta);
          expect(corregir(it, it.respuesta!, 'en'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'en'), isFalse, reason: it.id);
        } else {
          final otra = (it.indiceRespuesta! + 1) % it.opciones.length;
          expect(corregir(it, it.indiceRespuesta, 'en'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'en'), isFalse, reason: it.id);
        }
      }
    },
  );

  test(
    'Con el banco real la prueba termina y ubica bien a alumnos simulados',
    () {
      final rnd = Random(5);
      var ok = 0;
      const n = 200;
      for (var k = 0; k < n; k++) {
        final t = rnd.nextInt(11);
        final u = Ubicacion(
          banco: banco,
          declarado: Autodeclaracion.desdeNivel(max(1, t)),
          random: rnd,
        );
        var guardia = 0;
        for (var i = u.siguiente(); i != null; i = u.siguiente()) {
          final p = i.nivel <= t ? .92 : (i.nivel == t + 1 ? .45 : 1 / 3);
          u.responder(rnd.nextDouble() < p);
          expect(++guardia, lessThan(30));
        }
        if (u.escritura() != null) u.responder(true);
        expect(u.terminado, isTrue);
        if ((u.resultado().nivel - t).abs() <= 1) ok++;
      }
      expect(ok / n, greaterThan(.88));
    },
  );

  testWidgets(
    'Pantalla: «Nada» propone empezar desde cero; «Un poco» abre la prueba',
    (tester) async {
      tester.view.physicalSize = const Size(390, 844);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      SharedPreferences.setMockInitialValues({});
      Efectos.sonido = false;
      addTearDown(() => Efectos.sonido = true);
      final p = await SharedPreferences.getInstance();
      Future<void> montar() async {
        await tester.pumpWidget(
          ProviderScope(
            overrides: [prefsProvider.overrideWithValue(p)],
            child: MaterialApp(
              theme: buildTheme(),
              home: const UbicacionScreen(),
            ),
          ),
        );
        // El banco se limita a los niveles publicados: espera también a la ruta.
        for (var k = 0; k < 100; k++) {
          await tester.runAsync(
            () => Future<void>.delayed(const Duration(milliseconds: 100)),
          );
          await tester.pump();
          if (find.byType(CircularProgressIndicator).evaluate().isEmpty) break;
        }
        await tester.pumpAndSettle();
      }

      await montar();
      expect(find.text('¿Cuánto inglés sabes?'), findsOneWidget);
      await tester.tap(find.text('Nada, empiezo de cero'));
      await tester.pumpAndSettle();
      expect(find.text('Empiezas desde cero'), findsOneWidget);

      await tester.pumpWidget(const SizedBox());
      await montar();
      await tester.tap(find.text('Un poco'));
      await tester.pumpAndSettle();
      // Primera pregunta: una habilidad del nivel 1.
      expect(
        find.byWidgetPredicate(
          (w) =>
              w is Chip &&
              w.label is Text &&
              nombresHabilidad.values.contains((w.label as Text).data),
        ),
        findsOneWidget,
      );
    },
  );
}
