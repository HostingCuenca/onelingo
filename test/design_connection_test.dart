import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:onelingo/core/conexion.dart';
import 'package:onelingo/shared/widgets/daily_activities.dart';
import 'package:onelingo/shared/widgets/connection_banner.dart';
import 'package:onelingo/shared/widgets/app_navigation_icon.dart';

void main() {
  testWidgets('seis actividades llenan tres columnas y dos filas en móvil', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Padding(padding: EdgeInsets.all(20), child: DailyActivities()),
        ),
      ),
    );
    final cards = find.byType(InkWell);
    expect(cards, findsNWidgets(6));
    final rects = [for (var i = 0; i < 6; i++) tester.getRect(cards.at(i))];
    expect(rects.first.width, closeTo((350 - 16) / 3, .1));
    expect(rects.take(3).map((r) => r.top).toSet().length, 1);
    expect(rects.skip(3).map((r) => r.top).toSet().length, 1);
    expect(rects[3].top, greaterThan(rects[0].bottom));
    expect(tester.takeException(), isNull);
  });
  test(
    'distingue falta de conexión y servidor con error, y se recupera',
    () async {
      await http.runWithClient(
        Conexion.comprobar,
        () => MockClient((_) async => throw const SocketException('offline')),
      );
      expect(Conexion.estado.value, EstadoConexion.sinConexion);
      await http.runWithClient(
        Conexion.comprobar,
        () => MockClient((_) async => http.Response('{}', 503)),
      );
      expect(Conexion.estado.value, EstadoConexion.servicioNoDisponible);
      await http.runWithClient(
        Conexion.comprobar,
        () => MockClient((_) async => http.Response('{"ok":true}', 200)),
      );
      expect(Conexion.estado.value, EstadoConexion.disponible);
    },
  );
  testWidgets(
    'el aviso aparece sin quitar la pantalla y se oculta al recuperar conexión',
    (tester) async {
      Conexion.estado.value = EstadoConexion.sinConexion;
      await tester.pumpWidget(
        const MaterialApp(home: ConnectionBanner(child: Text('Tu actividad'))),
      );
      expect(
        find.text('Sin conexión con OneLingo. Comprueba tu conexión.'),
        findsOneWidget,
      );
      expect(find.text('Tu actividad'), findsOneWidget);
      Conexion.estado.value = EstadoConexion.disponible;
      await tester.pump();
      expect(find.text('Reintentar'), findsNothing);
      expect(find.text('Tu actividad'), findsOneWidget);
    },
  );
  testWidgets(
    'la navegación conserva un tamaño coherente al aparecer el aviso',
    (tester) async {
      final semantics = tester.ensureSemantics();
      Conexion.estado.value = EstadoConexion.disponible;
      await tester.pumpWidget(
        MaterialApp(
          builder: (context, child) => ConnectionBanner(child: child!),
          home: Scaffold(
            bottomNavigationBar: NavigationBar(
              destinations: const [
                NavigationDestination(icon: Icon(Icons.home), label: 'Inicio'),
                NavigationDestination(
                  icon: Icon(Icons.book),
                  label: 'Aprender',
                ),
              ],
            ),
          ),
        ),
      );
      final tooltip = tester.state<TooltipState>(find.byType(Tooltip).first);
      tooltip.ensureTooltipVisible();
      await tester.pumpAndSettle();
      Conexion.estado.value = EstadoConexion.sinConexion;
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      expect(find.text('Reintentar'), findsOneWidget);
      expect(find.bySemanticsLabel('Reintentar'), findsOneWidget);
      Conexion.estado.value = EstadoConexion.disponible;
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      semantics.dispose();
    },
  );
  testWidgets('los cuatro iconos propios se dibujan en ambos estados', (
    tester,
  ) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Row(
          children: [
            for (var i = 0; i < 4; i++) ...[
              AppNavigationIcon(i),
              AppNavigationIcon(i, selected: true),
            ],
          ],
        ),
      ),
    );
    expect(tester.takeException(), isNull);
  });
}
