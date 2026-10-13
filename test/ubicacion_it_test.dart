import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/correccion.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/aprendizaje/providers.dart';
import 'package:onelingo/core/aprendizaje/ubicacion.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/course/levels_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Prueba de ubicación v2 del italiano (versión esencial, curso completo):
/// banco real `assets/contenido/it/diagnostico-v2.json`, N1–N10, apoyo {es, en}.
/// Nunca ubica por encima de N10 (último nivel del curso, todo publicado).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final json =
      jsonDecode(File('assets/contenido/it/diagnostico-v2.json').readAsStringSync())
          as Map<String, dynamic>;
  final banco = ItemUbicacion.bancoLocalizado(json, 'es');

  test('El banco cubre N1–N10 en las cinco habilidades y nada más', () {
    expect(json['idioma'], 'it');
    expect(banco, hasLength(180));
    for (var n = 1; n <= 10; n++) {
      for (final h in [...habilidadesUbicacion, 'escritura']) {
        final k = banco.where((i) => i.nivel == n && i.habilidad == h).length;
        expect(k, h == 'escritura' ? 2 : 4, reason: 'N$n $h');
      }
    }
    expect(banco.where((i) => i.nivel > 10), isEmpty);
    expect(nivelMaximoUbicacion(banco), 10);
  });

  test('Apoyo en español latino y en inglés según la interfaz', () {
    final en = ItemUbicacion.bancoLocalizado(json, 'en');
    for (var k = 0; k < banco.length; k++) {
      final es = banco[k].item.consigna.en(const []);
      final ing = en[k].item.consigna.en(const []);
      expect(es, isNotEmpty, reason: banco[k].item.id);
      expect(ing, isNotEmpty, reason: banco[k].item.id);
      expect(es, isNot(ing), reason: banco[k].item.id);
    }
  });

  test('Cada ítem se corrige con su respuesta y falla con otra; la escritura con su rúbrica', () {
    for (final u in banco) {
      final it = u.item;
      switch (it.formato) {
        case FormatoItem.completar:
          final otra = it.opciones
              .map((o) => o.meta ?? '')
              .firstWhere((o) => o != it.respuesta);
          expect(corregir(it, it.respuesta!, 'it'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'it'), isFalse, reason: it.id);
        case FormatoItem.escribir:
          for (final t in [it.respuesta!, ...it.aceptadas]) {
            expect(corregir(it, t, 'it'), isTrue, reason: '${it.id}: $t');
          }
          expect(corregir(it, 'Ciao.', 'it'), isFalse, reason: it.id);
        default:
          final otra = (it.indiceRespuesta! + 1) % it.opciones.length;
          expect(corregir(it, it.indiceRespuesta, 'it'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'it'), isFalse, reason: it.id);
      }
    }
  });

  test('El tope es N10: lo publicado en la ruta y en el banco', () async {
    expect(idiomasConRuta, contains('it'));
    final ruta = (await CargadorRuta().cargar('it'))!;
    expect(nivelesPublicados(ruta), {for (var n = 1; n <= 10; n++) n});
    expect(nivelMaximoUbicacion(banco, publicados: nivelesPublicados(ruta)), 10);
  });

  testWidgets('Aprender: N1–N10 publicados y ninguno «Próximamente» ni «En preparación»', (tester) async {
    tester.view.physicalSize = const Size(390, 2600);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final ruta = (await tester.runAsync(() => CargadorRuta().cargar('it')))!;
    // Un alumno ubicado en N10 estudia N10: ya está publicado.
    const s = ProgressState(
      onboardingDone: true,
      nombre: 'Ana',
      idiomaMeta: 'it',
      nivelInicial: 10,
    );
    expect(nivelAlumnoEnRuta(ruta, s), 10);
    SharedPreferences.setMockInitialValues({
      'onelingo.progress.v1': jsonEncode(s.toJson()),
    });
    final prefs = await SharedPreferences.getInstance();
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          prefsProvider.overrideWithValue(prefs),
          rutaProvider.overrideWith((ref, idioma) async => ruta),
        ],
        child: MaterialApp(theme: buildTheme(), home: const LevelsScreen()),
      ),
    );
    await tester.pump();
    await tester.pump();
    expect(find.text('En preparación'), findsNothing);
    for (final t in [
      'Nivel 1 · A1', 'Nivel 2 · A2', 'Nivel 3 · B1', 'Nivel 4 · B1', 'Nivel 5 · B2', //
      'Nivel 6 · B2', 'Nivel 7 · B2', 'Nivel 8 · C1', 'Nivel 9 · C1', 'Nivel 10 · C1',
    ]) {
      expect(find.text(t), findsOneWidget, reason: t);
    }
    // Curso completo: ningún nivel queda bloqueado por falta de clases.
    expect(find.text('Próximamente'), findsNothing);
  });

  test('Alumnos simulados: nunca por encima de N10 y bien ubicados hasta N10', () {
    final rnd = Random(7);
    var ok = 0, total = 0;
    for (var k = 0; k < 300; k++) {
      final t = rnd.nextInt(11); // nivel real 0–10
      final u = Ubicacion(
        banco: banco,
        declarado: Autodeclaracion.desdeNivel(max(1, t)),
        nivelMaximo: 10,
        random: rnd,
      );
      expect(u.nivelMaximo, 10);
      var guardia = 0;
      for (var i = u.siguiente(); i != null; i = u.siguiente()) {
        expect(i.nivel, lessThanOrEqualTo(10));
        final p = i.nivel <= t ? .92 : (i.nivel == t + 1 ? .45 : 1 / 3);
        u.responder(rnd.nextDouble() < p);
        expect(++guardia, lessThan(30));
      }
      if (u.escritura() != null) u.responder(true);
      expect(u.terminado, isTrue);
      final r = u.resultado();
      expect(r.nivel, lessThanOrEqualTo(10), reason: 'nivel real $t');
      for (final v in r.habilidades.values) {
        expect(v, lessThanOrEqualTo(10));
      }
      final esperado = t;
      total++;
      if ((r.nivel - esperado).abs() <= 1) ok++;
    }
    expect(ok / total, greaterThan(.85));
  });

  test('Al azar casi siempre empieza desde cero', () {
    final rnd = Random(21);
    var ceros = 0, altos = 0;
    const n = 400;
    for (var k = 0; k < n; k++) {
      final d = [
        Autodeclaracion.poco,
        Autodeclaracion.poco,
        Autodeclaracion.defiendo,
        Autodeclaracion.avanzado,
      ][k % 4];
      final u = Ubicacion(banco: banco, declarado: d, nivelMaximo: 10, random: rnd);
      for (var i = u.siguiente(); i != null; i = u.siguiente()) {
        u.responder(rnd.nextInt(i.item.opciones.length) == i.item.indiceRespuesta);
      }
      if (u.escritura() != null) u.responder(false);
      final r = u.resultado();
      // Con diez niveles, un acertante con mucha suerte que se declara
      // avanzado pasa rara vez de N1 (como en zh y ja).
      expect(r.nivel, lessThanOrEqualTo(2), reason: 'azar, $d');
      if (r.nivel > 1) altos++;
      if (r.desdeCero) ceros++;
    }
    expect(altos, lessThanOrEqualTo(1), reason: '$altos de $n por encima de N1');
    expect(ceros / n, greaterThan(.9), reason: '$ceros de $n desde cero');
  });
}
