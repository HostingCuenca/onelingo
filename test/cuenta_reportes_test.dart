import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/core/api/sync.dart';
import 'package:onelingo/shared/widgets/enlaces_legales.dart';
import 'package:onelingo/shared/widgets/reportar_ia.dart';

/// Requisitos de Google Play en la app: eliminar la cuenta
/// (`DELETE /usuarios/me`) y reportar respuestas de la IA (`/reportes-ia`).
void main() {
  Future<SharedPreferences> sesion() async {
    SharedPreferences.setMockInitialValues({
      'onelingo.api.token': 'tok-1',
      'onelingo.api.usuarioId': 'u-1',
      'onelingo.api.email': 'lucia@correo.test',
      'onelingo.pending.u-1': '{"xp":3}',
    });
    final prefs = await SharedPreferences.getInstance();
    Sync.instancia.inicializar(prefs);
    return prefs;
  }

  test('eliminar cuenta: DELETE sin cuerpo; al terminar cierra la sesión y descarta lo pendiente', () async {
    final prefs = await sesion();
    late http.Request pedida;
    final r = await http.runWithClient(
      () => Sync.instancia.eliminarCuenta(),
      () => MockClient((req) async {
        pedida = req;
        return http.Response(
          jsonEncode({
            'ok': true,
            'stripeCancelada': false,
            'googlePlay': {'debeCancelar': true, 'producto': 'plan_p1'},
          }),
          200,
        );
      }),
    );
    expect(pedida.method, 'DELETE');
    expect(pedida.url.path, endsWith('/usuarios/me'));
    expect(pedida.headers['authorization'], 'Bearer tok-1');
    expect(pedida.headers.containsKey('content-type'), isFalse);
    expect(r?['googlePlay']['debeCancelar'], isTrue);
    expect(Sync.instancia.conectado, isFalse);
    expect(prefs.containsKey('onelingo.pending.u-1'), isFalse);
  });

  test('eliminar cuenta: una cuenta demo (403) conserva la sesión y deja el código', () async {
    final prefs = await sesion();
    final r = await http.runWithClient(
      () => Sync.instancia.eliminarCuenta(),
      () => MockClient(
        (_) async => http.Response(
          jsonEncode({
            'error': 'Las cuentas de demostración no se pueden eliminar.',
            'codigo': 'cuenta_demo',
          }),
          403,
        ),
      ),
    );
    expect(r, isNull);
    expect(Sync.instancia.ultimoCodigo, 'cuenta_demo');
    expect(Sync.instancia.conectado, isTrue);
    expect(prefs.containsKey('onelingo.pending.u-1'), isTrue);
    await Sync.instancia.cerrarSesion();
  });

  test(
    'reportar IA: manda origen, motivo, texto recortado y contexto sin nulos',
    () async {
      await sesion();
      late Map<String, dynamic> cuerpo;
      final ok = await http.runWithClient(
        () => Sync.instancia.reportarIA(
          origen: 'chat',
          texto: '  ${'a' * 2100}  ',
          motivo: 'ofensivo',
          comentario: ' feo ',
          contexto: {'idioma': 'fr', 'tutorId': 'mia', 'situacion': null},
        ),
        () => MockClient((req) async {
          expect(req.url.path, endsWith('/reportes-ia'));
          expect(req.headers['authorization'], 'Bearer tok-1');
          cuerpo = jsonDecode(req.body) as Map<String, dynamic>;
          return http.Response('{"ok":true,"id":1}', 201);
        }),
      );
      expect(ok, isTrue);
      expect(cuerpo['origen'], 'chat');
      expect(cuerpo['motivo'], 'ofensivo');
      expect((cuerpo['texto'] as String).length, 2000);
      expect(cuerpo['comentario'], 'feo');
      expect(cuerpo['contexto'], {'idioma': 'fr', 'tutorId': 'mia'});
      await Sync.instancia.cerrarSesion();
    },
  );

  testWidgets(
    'hoja de reporte: elegir motivo, enviar y «Gracias, lo revisaremos»',
    (tester) async {
      await tester.runAsync(sesion);
      Map<String, dynamic>? cuerpo;
      await http.runWithClient(
        () async {
          await tester.pumpWidget(
            MaterialApp(
              home: Scaffold(
                body: Builder(
                  builder: (context) => TextButton(
                    onPressed: () => reportarRespuestaIA(
                      context,
                      origen: 'chat',
                      texto: 'Respuesta del tutor',
                    ),
                    child: const Text('abrir'),
                  ),
                ),
              ),
            ),
          );
          await tester.tap(find.text('abrir'));
          await tester.pumpAndSettle();
          expect(find.text('Reportar respuesta'), findsOneWidget);
          // Sin motivo no se puede enviar.
          final enviar = find.widgetWithText(FilledButton, 'Enviar reporte');
          expect(tester.widget<FilledButton>(enviar).onPressed, isNull);
          await tester.tap(find.text('Incorrecta'));
          await tester.pump();
          await tester.tap(enviar);
          await tester.runAsync(
            () => Future<void>.delayed(const Duration(milliseconds: 50)),
          );
          await tester.pumpAndSettle();
        },
        () => MockClient((req) async {
          cuerpo = jsonDecode(req.body) as Map<String, dynamic>;
          return http.Response('{"ok":true,"id":7}', 201);
        }),
      );
      expect(cuerpo?['motivo'], 'incorrecto');
      expect(find.text('Gracias, lo revisaremos.'), findsOneWidget);
      expect(find.text('Reportar respuesta'), findsNothing);
      await tester.runAsync(Sync.instancia.cerrarSesion);
    },
  );

  testWidgets(
    'enlaces legales del registro: aviso, Términos y Política de privacidad',
    (tester) async {
      await tester.pumpWidget(
        const MaterialApp(home: Scaffold(body: EnlacesLegales(registro: true))),
      );
      expect(find.textContaining('aceptas los Términos'), findsOneWidget);
      expect(find.text('Términos'), findsOneWidget);
      expect(find.text('Política de privacidad'), findsOneWidget);
      expect(urlPrivacidad, 'https://onelingo.org/privacidad/');
      expect(urlTerminos, 'https://onelingo.org/terminos/');
    },
  );
}
