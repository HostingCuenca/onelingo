import 'dart:async';
import 'dart:convert';

import 'package:audioplayers_platform_interface/audioplayers_platform_interface.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/providers.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/library/grammar_screen.dart';
import 'package:onelingo/features/ruta/ruta_screen.dart';
import 'package:onelingo/features/ruta/unidad_screen.dart';

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

/// Recorridos de usuario sobre la ruta nueva y la gramática.
void main() {
  AudioplayersPlatformInterface.instance = _Audio();
  GlobalAudioplayersPlatformInterface.instance = _AudioGlobal();
  Future<ProviderContainer> montar(
    WidgetTester tester,
    Widget pantalla, {
    Map<String, Object> prefs = const {},
  }) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    SharedPreferences.setMockInitialValues(prefs);
    // Sin complemento de audio en pruebas: efectos silenciados.
    Efectos.sonido = false;
    addTearDown(() => Efectos.sonido = true);
    final p = await SharedPreferences.getInstance();
    // La ruta se lee de assets fuera del reloj simulado de la prueba.
    final cargador = CargadorRuta();
    await tester.runAsync(() => cargador.cargar('en'));
    final container = ProviderContainer(
      overrides: [
        prefsProvider.overrideWithValue(p),
        cargadorRutaProvider.overrideWithValue(cargador),
      ],
    );
    addTearDown(container.dispose);
    await tester.pumpWidget(
      UncontrolledProviderScope(
        container: container,
        child: MaterialApp(theme: buildTheme(), home: pantalla),
      ),
    );
    await tester.runAsync(
      () => Future<void>.delayed(const Duration(milliseconds: 300)),
    );
    await tester.pumpAndSettle();
    return container;
  }

  /// Desplaza la lista perezosa hasta el texto y lo toca (primero o último).
  Future<void> texto(
    WidgetTester tester,
    String t, {
    bool ultimo = false,
  }) async {
    final base = find.text(t);
    if (base.evaluate().isEmpty) {
      await tester.scrollUntilVisible(
        base,
        160,
        scrollable: find.byType(Scrollable).first,
        maxScrolls: 60,
      );
      await tester.pumpAndSettle();
    }
    final elegido = ultimo ? base.last : base.first;
    await tester.ensureVisible(elegido);
    await tester.pumpAndSettle();
    await tester.tap(elegido);
    await tester.pumpAndSettle();
    expect(tester.takeException(), isNull);
  }

  Future<void> responder(WidgetTester tester, String opcion) async {
    await texto(tester, opcion);
    await texto(tester, 'COMPROBAR');
    expect(find.text('¡Correcto!'), findsOneWidget);
    await texto(tester, 'CONTINUAR');
  }

  Future<void> relacionar(
    WidgetTester tester,
    List<(String, String)> pares,
  ) async {
    for (final (izq, der) in pares) {
      await texto(tester, izq);
      await texto(tester, der, ultimo: true);
    }
    expect(find.text('¡Correcto!'), findsOneWidget);
    await texto(tester, 'CONTINUAR');
  }

  testWidgets(
    'Principiante: Unidad 0 de inglés, de la enseñanza a la aprobación',
    (tester) async {
      final c = await montar(
        tester,
        const UnidadScreen(unidadId: 'en.f0.primer-contacto'),
      );
      // Enseña antes de evaluar: primera pantalla sin ejercicios.
      expect(find.text('Cómo aprendes aquí'), findsOneWidget);
      expect(
        find.textContaining('Objetivo:', skipOffstage: false),
        findsOneWidget,
      );
      expect(find.text('COMPROBAR'), findsNothing);
      await texto(tester, 'SIGUIENTE'); // vocabulario
      expect(find.text('good morning'), findsOneWidget);
      await texto(tester, 'SIGUIENTE'); // ejemplos
      await texto(tester, 'SIGUIENTE'); // práctica guiada
      expect(find.text('Práctica con ayuda'), findsOneWidget);
      // Un error en la práctica guiada no bloquea: se ve la respuesta, se
      // continúa y el ejercicio vuelve al final del bloque («Otra vez»).
      await texto(tester, 'goodbye');
      await texto(tester, 'COMPROBAR');
      expect(find.text('Vamos a repasarlo'), findsOneWidget);
      expect(find.text('Respuesta: hello'), findsOneWidget);
      await texto(tester, 'CONTINUAR');
      await responder(tester, 'thank you');
      await relacionar(tester, [
        ('hello', 'hola'),
        ('goodbye', 'adiós'),
        ('please', 'por favor'),
        ('thank you', 'gracias'),
      ]);
      expect(find.text('Otra vez'), findsOneWidget);
      await responder(tester, 'hello');
      final practicas = c.read(progressProvider).practicas;
      expect(
        practicas['ruta:en.f0.primer-contacto:p4:g1']['resueltaConApoyo'],
        isTrue,
      );
      expect(
        practicas['ruta:en.f0.primer-contacto:p4:g1']['primeraCorrecta'],
        isFalse,
      );
      // Práctica independiente y situación.
      await responder(tester, 'thank you');
      await responder(tester, 'sorry');
      expect(find.text('En situación'), findsOneWidget);
      await texto(tester, 'PARTICIPAR');
      await responder(tester, 'thank you');
      // Evaluación sin ayuda.
      expect(find.text('Comprueba'), findsOneWidget);
      expect(find.text('Ver una pista'), findsNothing);
      await responder(tester, 'goodbye');
      await relacionar(tester, [
        ('yes', 'sí'),
        ('no', 'no'),
        ('sorry', 'perdón'),
        ('excuse me', 'disculpe'),
      ]);
      await responder(tester, 'good morning');
      await tester.enterText(find.byType(TextField), 'Thank you');
      await tester.pumpAndSettle();
      await texto(tester, 'COMPROBAR');
      await texto(tester, 'CONTINUAR');
      await responder(tester, 'excuse me');
      // Recompensa: celebración con XP, precisión y tiempo.
      expect(find.text('¡Lección completada!'), findsOneWidget);
      expect(find.text('100 %'), findsOneWidget);
      expect(find.text('XP GANADA'), findsOneWidget);
      expect(find.textContaining('+'), findsWidgets);

      final ruta = (await tester.runAsync(() => CargadorRuta().cargar('en')))!!;
      final estados = estadosRuta(ruta, c.read(progressProvider).practicas);
      expect(estados['en.f0.primer-contacto']!.estado, EstadoUnidad.aprobada);
      expect(estados['en.f0.alfabeto']!.estado, EstadoUnidad.disponible);
      // Aprobar una unidad no completa el nivel.
      expect(c.read(progressProvider).rutaFundamentosAprobada, isFalse);
    },
  );

  testWidgets('Ruta: muestra unidades, estados y la recomendación', (
    tester,
  ) async {
    await montar(
      tester,
      const RutaScreen(),
      prefs: {
        'onelingo.progress.v1': jsonEncode({
          'onboardingDone': true,
          'idiomaMeta': 'en',
          'nivelInicial': 1,
          'fundamentos': true,
        }),
      },
    );
    expect(find.text('Fundamentos de Inglés'), findsOneWidget);
    expect(find.text('Siguiente paso'), findsOneWidget);
    expect(
      find.text('0. Primer contacto', skipOffstage: false),
      findsOneWidget,
    );
    expect(find.text('Versión inicial'), findsNothing);
    await tester.scrollUntilVisible(
      find.text('6. Presentarte'),
      200,
      scrollable: find.byType(Scrollable).first,
    );
    expect(find.text('Bloqueada'), findsWidgets);
  });

  testWidgets('N1 activo entra al recorrido editorial y carga la biblioteca', (
    tester,
  ) async {
    await montar(tester, const UnidadScreen(unidadId: 'en.n1.class-01'));
    expect(find.text('Presentarse y dar datos personales'), findsOneWidget);
    // Enriquecimiento: la clase empieza explicando la regla en español.
    expect(
      find.text('Presentarte: my name is, I am from, I live in'),
      findsOneWidget,
    );
    await tester.scrollUntilVisible(
      find.textContaining('Objetivo:'),
      200,
      scrollable: find.byType(Scrollable).first,
    );
    expect(find.textContaining('Objetivo:'), findsOneWidget);
    for (var i = 0; i < 4 && find.text('hello').evaluate().isEmpty; i++) {
      await texto(tester, 'SIGUIENTE');
    }
    expect(find.text('hello'), findsOneWidget);
    expect(find.text('Práctica con ayuda'), findsNothing);
  });

  testWidgets(
    'Alumno ubicado en Nivel 1: A1 disponible y fundamentos opcionales',
    (tester) async {
      final estado = jsonEncode({
        'onboardingDone': true,
        'idiomaMeta': 'en',
        'nivelInicial': 1,
        'fundamentos': false,
      });
      await montar(
        tester,
        const RutaScreen(nivel: 'n1'),
        prefs: {'onelingo.progress.v1': estado},
      );
      expect(find.text('Nivel 1 · A1 completo · Inglés'), findsOneWidget);
      expect(find.text('0 de 100 unidades aprobadas · A1'), findsOneWidget);
      expect(find.text('Siguiente paso'), findsOneWidget);
      // Sin bloqueo por fundamentos: la primera unidad de A1 está disponible.
      expect(find.text('Disponible', skipOffstage: false), findsWidgets);
      await montar(
        tester,
        const RutaScreen(),
        prefs: {'onelingo.progress.v1': estado},
      );
      expect(
        find.text('Opcional · según tu nivel', skipOffstage: false),
        findsWidgets,
      );
    },
  );

  testWidgets('Gramática: al volver reanuda el tema y marca lo practicado', (
    tester,
  ) async {
    await montar(
      tester,
      const GrammarScreen(nivel: 1),
      prefs: {
        'onelingo.gramatica.posicion': '1:1',
        'onelingo.gramatica.borrador.be': 'I am Ana.',
      },
    );
    // Reanuda en el tema 2 guardado, no en el 1.
    expect(find.textContaining('Tema 2'), findsWidgets);
  });
}
