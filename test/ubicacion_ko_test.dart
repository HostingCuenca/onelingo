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
/// `assets/contenido/ko/diagnostico-v2.json`, N1–N4, apoyo {es, en} y
/// romanización RR (`textoRom`, `opcionesRom`) en cada texto y opción en hangul
/// (con espacios entre palabras, sin hanja, sin cifras ni símbolos).
/// Nunca ubica por encima de N4 (último nivel con clases publicadas).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final json =
      jsonDecode(File('assets/contenido/ko/diagnostico-v2.json').readAsStringSync())
          as Map<String, dynamic>;
  final banco = ItemUbicacion.bancoLocalizado(json, 'es');
  final hangul = RegExp(r'[가-힣]');

  test('El banco cubre N1–N4 en las cinco habilidades y nada más', () {
    expect(json['idioma'], 'ko');
    expect(banco, hasLength(72));
    for (var n = 1; n <= 4; n++) {
      for (final h in [...habilidadesUbicacion, 'escritura']) {
        final k = banco.where((i) => i.nivel == n && i.habilidad == h).length;
        expect(k, h == 'escritura' ? 2 : 4, reason: 'N$n $h');
      }
    }
    expect(banco.where((i) => i.nivel > 4), isEmpty);
    expect(nivelMaximoUbicacion(banco), 4);
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
    expect(banco.where((u) => u.item.tieneRom), hasLength(64));
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
    // N3: qué pasó (-게 되다), qué cambió (-아/어지다) y cómo está.
    final n3 = banco.firstWhere((u) => u.item.id == 'dx.ko.n3.escritura.1').item;
    expect(
      corregir(n3, '작년에 회사를 옮기게 됐어요. 일이 많아졌어요. 그래도 아주 뿌듯해요.', 'ko'),
      isTrue,
    );
    expect(
      corregir(n3, '작년에 회사를 옮기게 됐어요 일이 많아졌어요 그래도 아주 뿌듯해요', 'ko'),
      isTrue,
    );
    // Sin el cambio (-아/어지다) no cumple aunque sea largo.
    expect(
      corregir(n3, '작년에 서울에서 일하게 됐어요. 회사 일이 정말 재미있어요. 친구도 많아요.', 'ko'),
      isFalse,
    );
    expect(corregir(n3, '서울에서 일하게 됐어요.', 'ko'), isFalse);
    // N3: un recado sin lo que pidió (-아/어 달라고) no cumple.
    final n3b = banco.firstWhere((u) => u.item.id == 'dx.ko.n3.escritura.2').item;
    expect(
      corregir(n3b, '민준 씨가 전화했어요. 오늘 늦는다고 했어요. 그리고 확인해 달라고 했어요.', 'ko'),
      isTrue,
    );
    expect(
      corregir(n3b, '민준 씨가 전화했어요. 오늘 늦는다고 했어요. 내일 다시 올 거예요.', 'ko'),
      isFalse,
    );
    // N4: dónde vivía (-았/었었어요), qué solía hacer (-곤 했다) y qué cambió (-에 비해).
    final n4 = banco.firstWhere((u) => u.item.id == 'dx.ko.n4.escritura.1').item;
    expect(
      corregir(n4, '어렸을 때 대구에 살았었어요. 주말마다 친구들하고 축구를 하곤 했어요. 그때에 비해 지금은 많이 달라졌어요.', 'ko'),
      isTrue,
    );
    // Sin lo habitual (-곤 했다) no cumple.
    expect(
      corregir(n4, '어렸을 때 대구에 살았었어요. 주말마다 축구를 했어요. 그때에 비해 지금은 많이 달라졌어요.', 'ko'),
      isFalse,
    );
    // N4: una opinión sin la razón (-기 때문이다) no cumple.
    final n4b = banco.firstWhere((u) => u.item.id == 'dx.ko.n4.escritura.2').item;
    expect(
      corregir(n4b, '저는 자전거가 더 좋다고 생각해요. 왜냐하면 버스가 느리기 때문이에요. 그래서 도로를 개선해야 해요.', 'ko'),
      isTrue,
    );
    expect(
      corregir(n4b, '저는 자전거가 더 좋다고 생각해요. 버스는 느려요. 그래서 도로를 개선해야 해요.', 'ko'),
      isFalse,
    );
  });

  test('El tope es N4: lo publicado en la ruta y en el banco', () async {
    expect(idiomasConRuta, contains('ko'));
    final ruta = (await CargadorRuta().cargar('ko'))!;
    expect(nivelesPublicados(ruta), {1, 2, 3, 4});
    expect(nivelMaximoUbicacion(banco, publicados: nivelesPublicados(ruta)), 4);
  });

  testWidgets('Aprender: N1–N4 publicados y N5–N10 «Próximamente»', (tester) async {
    tester.view.physicalSize = const Size(390, 2600);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final ruta = (await tester.runAsync(() => CargadorRuta().cargar('ko')))!;
    // Un alumno ubicado por el diagnóstico antiguo en N8 estudia N4, el último publicado.
    const s = ProgressState(
      onboardingDone: true,
      nombre: 'Ana',
      idiomaMeta: 'ko',
      nivelInicial: 8,
    );
    expect(nivelAlumnoEnRuta(ruta, s), 4);
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
    // N3 y N4 son ambos B1 en el marco.
    expect(find.text('Nivel 3 · B1'), findsOneWidget);
    expect(find.text('Nivel 4 · B1'), findsOneWidget);
    // N5–N10 no existen en el curso: la app los muestra bloqueados.
    expect(find.text('Próximamente'), findsNWidgets(6));
  });

  test('Alumnos simulados: nunca por encima de N4 y bien ubicados hasta N4', () {
    final rnd = Random(7);
    var ok = 0;
    const n = 300;
    for (var k = 0; k < n; k++) {
      final t = rnd.nextInt(11); // nivel real 0–10
      final u = Ubicacion(
        banco: banco,
        declarado: Autodeclaracion.desdeNivel(max(1, t)),
        nivelMaximo: 4,
        random: rnd,
      );
      expect(u.nivelMaximo, 4);
      var guardia = 0;
      for (var i = u.siguiente(); i != null; i = u.siguiente()) {
        expect(i.nivel, lessThanOrEqualTo(4));
        final p = i.nivel <= t ? .92 : (i.nivel == t + 1 ? .45 : 1 / 3);
        u.responder(rnd.nextDouble() < p);
        expect(++guardia, lessThan(30));
      }
      if (u.escritura() != null) u.responder(true);
      expect(u.terminado, isTrue);
      final r = u.resultado();
      expect(r.nivel, lessThanOrEqualTo(4), reason: 'nivel real $t');
      for (final v in r.habilidades.values) {
        expect(v, lessThanOrEqualTo(4));
      }
      if ((r.nivel - min(t, 4)).abs() <= 1) ok++;
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
      final u = Ubicacion(banco: banco, declarado: d, nivelMaximo: 4, random: rnd);
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
