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

/// Prueba de ubicación v2 del coreano (versión esencial): banco real
/// `assets/contenido/ko/diagnostico-v2.json`, N1–N2, apoyo {es, en} y
/// romanización RR (`textoRom`, `opcionesRom`) en cada texto y opción en hangul
/// (con espacios entre palabras, sin hanja, sin cifras ni símbolos).
/// Nunca ubica por encima de N2 (último nivel con clases publicadas).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final json =
      jsonDecode(File('assets/contenido/ko/diagnostico-v2.json').readAsStringSync())
          as Map<String, dynamic>;
  final banco = ItemUbicacion.bancoLocalizado(json, 'es');
  final hangul = RegExp(r'[가-힣]');

  test('El banco cubre N1–N2 en las cinco habilidades y nada más', () {
    expect(json['idioma'], 'ko');
    expect(banco, hasLength(36));
    for (var n = 1; n <= 2; n++) {
      for (final h in [...habilidadesUbicacion, 'escritura']) {
        final k = banco.where((i) => i.nivel == n && i.habilidad == h).length;
        expect(k, h == 'escritura' ? 2 : 4, reason: 'N$n $h');
      }
    }
    expect(banco.where((i) => i.nivel > 2), isEmpty);
    expect(nivelMaximoUbicacion(banco), 2);
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

  test('Rom bajo cada texto y opción en hangul; el audio no lo lleva', () {
    for (final u in banco) {
      final it = u.item;
      if (hangul.hasMatch(it.texto ?? '')) {
        expect(it.textoRom, isNotNull, reason: it.id);
      }
      for (var i = 0; i < it.opciones.length; i++) {
        if (hangul.hasMatch(it.opciones[i].meta ?? '')) {
          expect(it.romOpcion(i), isNotNull, reason: '${it.id} opción $i');
        }
      }
      if (it.formato == FormatoItem.escuchar) {
        expect(it.audio, isNotNull, reason: it.id);
        expect(it.texto, isNull, reason: it.id);
      }
    }
    expect(banco.where((u) => u.item.tieneRom), hasLength(32));
    // El hangul va con espacios entre palabras y sin hanja ni kana; ninguna
    // cifra ni símbolo en lo que se lee o se oye, y sin Lumo.
    final prohibido = RegExp('[0-9%₩\\u4E00-\\u9FFF\\u3040-\\u30FF]');
    for (final u in banco) {
      final it = u.item;
      for (final t in [it.texto, it.audio, ...it.opciones.map((o) => o.meta)]) {
        expect(prohibido.hasMatch(t ?? ''), isFalse, reason: '${it.id}: $t');
      }
      expect(it.id, startsWith('dx.ko.n'));
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
          expect(corregir(it, it.respuesta!, 'ko'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'ko'), isFalse, reason: it.id);
        case FormatoItem.escribir:
          for (final t in [it.respuesta!, ...it.aceptadas]) {
            expect(corregir(it, t, 'ko'), isTrue, reason: '${it.id}: $t');
            // Sin puntuación también vale.
            final llana = t.replaceAll(RegExp(r'[.,!?]'), '');
            expect(corregir(it, llana, 'ko'), isTrue, reason: '${it.id}: $llana');
          }
          expect(corregir(it, '안녕하세요!', 'ko'), isFalse, reason: it.id);
        default:
          final otra = (it.indiceRespuesta! + 1) % it.opciones.length;
          expect(corregir(it, it.indiceRespuesta, 'ko'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'ko'), isFalse, reason: it.id);
      }
    }
  });

  test('Escritura en coreano: extensión en palabras y evidencias de frase', () {
    final n1 = banco.firstWhere((u) => u.item.id == 'dx.ko.n1.escritura.1').item;
    expect(
      corregir(n1, '저는 학생이에요. 서울에 살아요. 영화를 좋아해요.', 'ko'),
      isTrue,
    );
    // Sin puntuación y con otros datos.
    expect(
      corregir(n1, '저는 회사원이에요 부산에 살아요 음악을 좋아해요', 'ko'),
      isTrue,
    );
    // Falta qué le gusta: no cumple la rúbrica aunque sea largo.
    expect(
      corregir(n1, '저는 학생이에요. 서울에 살아요. 책을 읽어요.', 'ko'),
      isFalse,
    );
    // Demasiado corto.
    expect(corregir(n1, '저는 학생이에요.', 'ko'), isFalse);
    final n2 = banco.firstWhere((u) => u.item.id == 'dx.ko.n2.escritura.1').item;
    expect(
      corregir(n2, '지난주에 부산에 갔어요. 사진을 찍었어요. 정말 좋았어요.', 'ko'),
      isTrue,
    );
    // Sin pasado no cumple.
    expect(
      corregir(n2, '지금 부산에 가요. 사진을 찍어요. 정말 좋아요.', 'ko'),
      isFalse,
    );
  });

  test('El tope es N2: lo publicado en la ruta y en el banco', () async {
    expect(idiomasConRuta, contains('ko'));
    final ruta = (await CargadorRuta().cargar('ko'))!;
    expect(nivelesPublicados(ruta), {1, 2});
    expect(nivelMaximoUbicacion(banco, publicados: nivelesPublicados(ruta)), 2);
  });

  testWidgets('Aprender: N1–N2 publicados y N3–N10 «Próximamente»', (tester) async {
    tester.view.physicalSize = const Size(390, 2600);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final ruta = (await tester.runAsync(() => CargadorRuta().cargar('ko')))!;
    // Un alumno ubicado por el diagnóstico antiguo en N8 estudia N2, el último publicado.
    const s = ProgressState(
      onboardingDone: true,
      nombre: 'Ana',
      idiomaMeta: 'ko',
      nivelInicial: 8,
    );
    expect(nivelAlumnoEnRuta(ruta, s), 2);
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
    expect(find.text('Nivel 1 · A1'), findsOneWidget);
    expect(find.text('Nivel 2 · A2'), findsOneWidget);
    // N3–N10 no existen en el curso: la app los muestra bloqueados.
    expect(find.text('Próximamente'), findsNWidgets(8));
  });

  test('Alumnos simulados: nunca por encima de N2 y bien ubicados hasta N2', () {
    final rnd = Random(7);
    var ok = 0;
    const n = 300;
    for (var k = 0; k < n; k++) {
      final t = rnd.nextInt(11); // nivel real 0–10
      final u = Ubicacion(
        banco: banco,
        declarado: Autodeclaracion.desdeNivel(max(1, t)),
        nivelMaximo: 2,
        random: rnd,
      );
      expect(u.nivelMaximo, 2);
      var guardia = 0;
      for (var i = u.siguiente(); i != null; i = u.siguiente()) {
        expect(i.nivel, lessThanOrEqualTo(2));
        final p = i.nivel <= t ? .92 : (i.nivel == t + 1 ? .45 : 1 / 3);
        u.responder(rnd.nextDouble() < p);
        expect(++guardia, lessThan(30));
      }
      if (u.escritura() != null) u.responder(true);
      expect(u.terminado, isTrue);
      final r = u.resultado();
      expect(r.nivel, lessThanOrEqualTo(2), reason: 'nivel real $t');
      for (final v in r.habilidades.values) {
        expect(v, lessThanOrEqualTo(2));
      }
      if ((r.nivel - min(t, 2)).abs() <= 1) ok++;
    }
    expect(ok / n, greaterThan(.85));
  });

  test('Al azar casi siempre empieza desde cero', () {
    final rnd = Random(21);
    var ceros = 0;
    const n = 400;
    for (var k = 0; k < n; k++) {
      final d = [
        Autodeclaracion.poco,
        Autodeclaracion.poco,
        Autodeclaracion.defiendo,
        Autodeclaracion.avanzado,
      ][k % 4];
      final u = Ubicacion(banco: banco, declarado: d, nivelMaximo: 2, random: rnd);
      for (var i = u.siguiente(); i != null; i = u.siguiente()) {
        u.responder(rnd.nextInt(i.item.opciones.length) == i.item.indiceRespuesta);
      }
      if (u.escritura() != null) u.responder(false);
      final r = u.resultado();
      expect(r.nivel, lessThanOrEqualTo(1), reason: 'azar, $d');
      if (r.desdeCero) ceros++;
    }
    expect(ceros / n, greaterThan(.9), reason: '$ceros de $n desde cero');
  });
}
