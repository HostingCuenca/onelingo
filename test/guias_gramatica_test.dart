import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/library/grammar_screen.dart';
import 'package:onelingo/features/ruta/opcion_respuesta.dart';
import 'package:onelingo/shared/widgets/widgets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Guías: acción fija abajo, opciones con pedestal y chips de nivel', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();
    Efectos.sonido = false;
    Efectos.vibraciones.value = false;
    final container = ProviderContainer(
      overrides: [prefsProvider.overrideWithValue(prefs)],
    );
    addTearDown(container.dispose);
    await tester.pumpWidget(
      UncontrolledProviderScope(
        container: container,
        child: MaterialApp(
          theme: buildTheme(),
          builder: (context, child) => MediaQuery(
            data: MediaQuery.of(context).copyWith(disableAnimations: true),
            child: child!,
          ),
          home: const GrammarScreen(nivel: 1),
        ),
      ),
    );
    await tester.pumpAndSettle();

    // La acción principal no está dentro de la lista desplazable.
    final principal = find.widgetWithText(BotonPrincipal, 'AHORA ME TOCA A MÍ');
    expect(principal, findsOneWidget);
    expect(
      find.ancestor(of: principal, matching: find.byType(ListView)),
      findsNothing,
    );
    await tester.tap(principal);
    await tester.pumpAndSettle();
    await tester.tap(find.text('COMPROBAR CON EJEMPLOS'));
    await tester.pumpAndSettle();

    expect(find.byType(OpcionRespuesta), findsWidgets);
    expect(find.byType(FilledButton), findsNothing);
    final comprobar = find.widgetWithText(BotonPrincipal, 'COMPROBAR');
    expect(tester.widget<BotonPrincipal>(comprobar).onPressed, isNull);
    await tester.tap(find.text('is'));
    await tester.pumpAndSettle();
    expect(tester.widget<BotonPrincipal>(comprobar).onPressed, isNotNull);
    await tester.tap(comprobar);
    await tester.pumpAndSettle();
    final registro =
        container.read(progressProvider).practicas['grammar-guide-be-0'];
    expect(registro['correcta'], true);
    expect(registro['idioma'], 'en');
    expect(find.text('SIGUIENTE PREGUNTA'), findsOneWidget);

    // Temario sin desplegable ni «nivel interno».
    await tester.ensureVisible(find.text('Temario'));
    await tester.tap(find.text('Temario'));
    await tester.pumpAndSettle();
    expect(find.byType(DropdownButtonFormField<int>), findsNothing);
    expect(find.textContaining('nivel interno'), findsNothing);
    expect(find.textContaining('Explorar nivel'), findsNothing);
    expect(find.byType(ChoiceChip), findsNWidgets(10));
    for (final jerga in ['evidencia', 'orientativo', 'no certifica']) {
      expect(find.textContaining(jerga), findsNothing);
    }
    expect(tester.takeException(), isNull);
  });
}
