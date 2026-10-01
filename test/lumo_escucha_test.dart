import 'dart:async';

import 'package:audioplayers_platform_interface/audioplayers_platform_interface.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/features/ruta/item_view.dart';
import 'package:onelingo/shared/widgets/lumo.dart';

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

void main() {
  AudioplayersPlatformInterface.instance = _Audio();
  GlobalAudioplayersPlatformInterface.instance = _AudioGlobal();

  final item = Item.fromJson({
    'id': 'prueba.escucha',
    'formato': 'escuchar',
    'consigna': {'es': 'Escucha y elige'},
    'feedback': {'es': 'Explicación'},
    'audio': 'I go to school by bus.',
    'opciones': ['By bus', 'On foot', 'By car'],
    'respuesta': 0,
  });

  Finder lumo(PoseLumo p) =>
      find.byWidgetPredicate((w) => w is LumoReaccion && w.pose == p);

  Future<void> montar(WidgetTester tester, {bool conLumo = true}) async {
    Efectos.sonido = false;
    addTearDown(() => Efectos.sonido = true);
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SingleChildScrollView(
            child: ItemView(
              item: item,
              idioma: 'en',
              cadena: const [],
              guiada: false,
              permitirReintento: false,
              lumo: conLumo,
              onComprobado: (_, _) {},
              onContinuar: () {},
            ),
          ),
        ),
      ),
    );
    await tester.pump();
  }

  testWidgets(
    'Escucha: Lumo escucha antes de responder y un solo Lumo después',
    (tester) async {
      await montar(tester);
      expect(lumo(PoseLumo.escucha), findsOneWidget);
      await tester.tap(find.text('By bus'));
      await tester.pump();
      await tester.tap(find.text('COMPROBAR'));
      await tester.pumpAndSettle();
      // Panel abierto: Lumo de acierto y ya no el de escucha (nunca dos).
      expect(lumo(PoseLumo.escucha), findsNothing);
      expect(find.byType(LumoReaccion), findsOneWidget);
    },
  );

  testWidgets('Prueba de nivel (lumo: false): sin Lumo', (tester) async {
    await montar(tester, conLumo: false);
    expect(find.byType(LumoReaccion), findsNothing);
  });
}
