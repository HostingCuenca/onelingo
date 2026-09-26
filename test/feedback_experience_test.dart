import 'package:onelingo/shared/widgets/activity_loading.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/shared/widgets/feedback_experience.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUp(() async {
    SharedPreferences.setMockInitialValues({});
    Efectos.inicializar(await SharedPreferences.getInstance());
    Efectos.antesDeSonar = null;
  });
  testWidgets('carga animada se detiene al reducir movimiento y al desmontar', (
    tester,
  ) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(body: SingleChildScrollView(child: ActivityLoading())),
      ),
    );
    final before = tester
        .widget<Transform>(find.byKey(const ValueKey('activity-orbit-0')))
        .transform
        .clone();
    await tester.pump(const Duration(milliseconds: 250));
    expect(
      tester
          .widget<Transform>(find.byKey(const ValueKey('activity-orbit-0')))
          .transform,
      isNot(before),
    );
    expect(tester.binding.transientCallbackCount, greaterThan(0));
    await Efectos.cambiarAnimaciones(false);
    await tester.pumpAndSettle();
    expect(tester.binding.transientCallbackCount, 0);
    expect(find.text('Preparando tu actividad…'), findsOneWidget);
    expect(tester.takeException(), isNull);
    await tester.pumpWidget(const SizedBox());
    expect(tester.takeException(), isNull);
  });
  testWidgets('corrección larga visible junto al botón en pantalla pequeña', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(390, 640);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Column(
            children: [
              const Expanded(child: Text('Actividad')),
              FeedbackDock(
                child: AnswerFeedback(
                  correct: true,
                  title: '¡Correcto!',
                  child: Column(
                    children: [
                      Text(
                        List.filled(
                          50,
                          'Explicación que conserva todos los detalles.',
                        ).join(' '),
                      ),
                      const Text('Fin de la corrección'),
                    ],
                  ),
                ),
              ),
              ElevatedButton(onPressed: () {}, child: const Text('CONTINUAR')),
            ],
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    expect(tester.takeException(), isNull);
    expect(
      tester.getRect(find.text('¡Correcto!')).bottom,
      lessThan(tester.getRect(find.text('CONTINUAR')).top),
    );
    await tester.drag(
      find.byType(SingleChildScrollView),
      const Offset(0, -3000),
    );
    await tester.pumpAndSettle();
    expect(tester.takeException(), isNull);
    expect(
      tester.getRect(find.text('Fin de la corrección')).bottom,
      lessThan(tester.getRect(find.text('CONTINUAR')).top),
    );
  });
  test('silencio y preferencias sobreviven a la inicialización', () async {
    await Efectos.cambiarSonido(false);
    await Efectos.cambiarAnimaciones(false);
    await Efectos.cambiarVibracion(false);
    Efectos.inicializar(await SharedPreferences.getInstance());
    expect(Efectos.sonido, isFalse);
    expect(Efectos.animaciones.value, isFalse);
    expect(Efectos.vibraciones.value, isFalse);
    var calls = 0;
    Efectos.antesDeSonar = () async {
      calls++;
    };
    Efectos.correcto();
    await Future<void>.delayed(Duration.zero);
    expect(calls, 0);
  });
  testWidgets('silenciar desde la práctica se refleja en ajustes', (
    tester,
  ) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Column(children: [SoundToggle(), EffectsSettings()]),
        ),
      ),
    );
    await tester.tap(find.byTooltip('Silenciar efectos'));
    await tester.pumpAndSettle();
    expect(find.byTooltip('Activar efectos'), findsOneWidget);
    expect(
      tester.widget<SwitchListTile>(find.byType(SwitchListTile).first).value,
      isFalse,
    );
  });
  testWidgets('feedback se adapta a texto grande y movimiento reducido', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(
      MaterialApp(
        home: MediaQuery(
          data: const MediaQueryData(
            size: Size(390, 844),
            disableAnimations: true,
            textScaler: TextScaler.linear(1.5),
          ),
          child: const Scaffold(
            body: SingleChildScrollView(
              child: AnswerFeedback(
                correct: false,
                title: 'Vamos a repasarlo',
                child: Text(
                  'La explicación sigue disponible sin depender de sonido, movimiento ni color.',
                ),
              ),
            ),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('Vamos a repasarlo'), findsOneWidget);
    expect(tester.takeException(), isNull);
    expect(tester.binding.transientCallbackCount, 0);
  });
}
