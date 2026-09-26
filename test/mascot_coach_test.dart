import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/shared/widgets/mascot_coach.dart';

void main() {
  testWidgets(
    'Movimiento reducido y preferencia local conservan imagen y mensaje',
    (tester) async {
      Efectos.animaciones.value = true;
      addTearDown(() => Efectos.animaciones.value = true);
      Future<void> render(bool reduced) => tester.pumpWidget(
        MaterialApp(
          home: MediaQuery(
            data: MediaQueryData(disableAnimations: reduced),
            child: const Scaffold(body: MascotCoach(message: 'Vamos juntos')),
          ),
        ),
      );
      await render(true);
      await tester.pumpAndSettle();
      expect(find.text('Vamos juntos'), findsOneWidget);
      expect(
        tester
            .widgetList<Image>(find.byType(Image))
            .map((i) => (i.image as AssetImage).assetName),
        everyElement(endsWith('-reposo-alpha.png')),
      );
      Efectos.animaciones.value = false;
      await render(false);
      await tester.pumpAndSettle();
      expect(
        tester
            .widgetList<Image>(find.byType(Image))
            .map((i) => (i.image as AssetImage).assetName),
        everyElement(endsWith('-reposo-alpha.png')),
      );
      expect(tester.takeException(), isNull);
    },
  );
}
