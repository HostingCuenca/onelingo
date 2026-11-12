import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/content/fotos.dart';
import 'package:onelingo/shared/widgets/situation_illustrations.dart';

void main() {
  test(
    'cada una de las 50 situaciones tiene su propia ilustración en la tarjeta',
    () {
      final rutas = [for (var id = 1; id <= 50; id++) fotoSituacion(id)!];
      expect(rutas.toSet().length, 50);
      for (final r in rutas) {
        expect(File(r).existsSync(), isTrue, reason: r);
      }
    },
  );

  testWidgets(
    'la situación 22 muestra la escena 2 nueva cuando está en la app',
    (tester) async {
      await tester.pumpWidget(
        const MaterialApp(home: Scaffold(body: SituationIllustrations(22))),
      );
      await tester.runAsync(
        () => Future<void>.delayed(const Duration(milliseconds: 200)),
      );
      await tester.pump();
      expect(find.textContaining('de 2'), findsOneWidget);
      await tester.drag(find.byType(PageView), const Offset(-500, 0));
      await tester.pumpAndSettle();
      final img = tester.widget<Image>(find.byType(Image).last);
      expect(
        (img.image as AssetImage).assetName,
        endsWith('situacion-22-2b.webp'),
      );
    },
  );
}
