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

/// Prueba de ubicación v2 del chino mandarín (versión esencial): banco real
/// `assets/contenido/zh/diagnostico-v2.json`, N1–N4, apoyo {es, en} y pinyin
/// (`textoRom`, `opcionesRom`) en cada texto y opción en chino.
/// Nunca ubica por encima de N4 (último nivel con clases publicadas).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final json =
      jsonDecode(File('assets/contenido/zh/diagnostico-v2.json').readAsStringSync())
          as Map<String, dynamic>;
  final banco = ItemUbicacion.bancoLocalizado(json, 'es');
  final hanzi = RegExp(r'[一-鿿]');

  test('El banco cubre N1–N4 en las cinco habilidades y nada más', () {
    expect(json['idioma'], 'zh');
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

  test('Pinyin bajo cada texto y opción en chino; el audio no lo lleva', () {
    for (final u in banco) {
      final it = u.item;
      if (hanzi.hasMatch(it.texto ?? '')) {
        expect(it.textoRom, isNotNull, reason: it.id);
      }
      for (var i = 0; i < it.opciones.length; i++) {
        if (hanzi.hasMatch(it.opciones[i].meta ?? '')) {
          expect(it.romOpcion(i), isNotNull, reason: '${it.id} opción $i');
        }
      }
      if (it.formato == FormatoItem.escuchar) {
        expect(it.audio, isNotNull, reason: it.id);
        expect(it.texto, isNull, reason: it.id);
      }
    }
    expect(banco.where((u) => u.item.tieneRom), hasLength(64));
    // Sin cifras ni letras latinas en el chino (los números van en hanzi).
    for (final u in banco) {
      final it = u.item;
      final textos = [
        it.texto, it.audio, ...it.opciones.map((o) => o.meta), //
        if (it.formato == FormatoItem.escribir) ...[it.respuesta, ...it.aceptadas],
      ];
      for (final t in textos.whereType<String>()) {
        if (!hanzi.hasMatch(t)) continue;
        expect(RegExp('[0-9A-Za-z]').hasMatch(t), isFalse, reason: '${it.id}: $t');
      }
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
          expect(corregir(it, it.respuesta!, 'zh'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'zh'), isFalse, reason: it.id);
        case FormatoItem.escribir:
          for (final t in [it.respuesta!, ...it.aceptadas]) {
            expect(corregir(it, t, 'zh'), isTrue, reason: '${it.id}: $t');
            // El alumno escribe sin espacios (teclado chino): también vale.
            final junto = t.replaceAll(' ', '');
            expect(corregir(it, junto, 'zh'), isTrue, reason: '${it.id}: $junto');
          }
          expect(corregir(it, '你好。', 'zh'), isFalse, reason: it.id);
        default:
          final otra = (it.indiceRespuesta! + 1) % it.opciones.length;
          expect(corregir(it, it.indiceRespuesta, 'zh'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'zh'), isFalse, reason: it.id);
      }
    }
  });

  test('Escritura en chino: extensión en caracteres y evidencias sin espacios', () {
    final it = banco
        .firstWhere((u) => u.item.id == 'dx.zh.n1.escritura.1')
        .item;
    expect(corregir(it, '我住在北京。我在学校学习。我很喜欢音乐。', 'zh'), isTrue);
    // Falta qué le gusta: no cumple la rúbrica aunque sea largo.
    expect(corregir(it, '我住在北京。我在学校学习汉语。', 'zh'), isFalse);
    // Demasiado corto (menos de ocho caracteres).
    expect(corregir(it, '住在家', 'zh'), isFalse);
    // N3: qué pasó (被 / 把), qué hacía (…的 时候) y qué hizo.
    final n3 = banco.firstWhere((u) => u.item.id == 'dx.zh.n3.escritura.1').item;
    expect(
      corregir(n3, '我 在 公园 跑步 的 时候，我 的 手机 被 人 偷 走 了。我 马上 去 派出所 报警 了。', 'zh'),
      isTrue,
    );
    expect(corregir(n3, '我在公园跑步的时候，我的手机被人偷走了。我马上去派出所报警了。', 'zh'), isTrue);
    // Sin «…的 时候» no cumple aunque sea largo.
    expect(
      corregir(n3, '昨天 我 的 手机 被 人 偷 走 了。我 马上 去 派出所 报警 了。', 'zh'),
      isFalse,
    );
    // N3: un plan con «只要…就…» sin qué pasa si no (不然 / 万一) no cumple.
    final n3b = banco.firstWhere((u) => u.item.id == 'dx.zh.n3.escritura.2').item;
    expect(
      corregir(n3b, '只要 周末 天气 好，我们 就 去 爬山。万一 下雨，我们 就 在 家 看 电影。', 'zh'),
      isTrue,
    );
    expect(
      corregir(n3b, '只要 周末 天气 好，我们 就 去 爬山。我们 早上 七 点 出发。', 'zh'),
      isFalse,
    );
    // N4: algo que ya no hace (不 再) comparado con antes (跟 以前 相比).
    final n4 = banco.firstWhere((u) => u.item.id == 'dx.zh.n4.escritura.1').item;
    expect(
      corregir(n4, '以前 我 每天 都 坐 公共汽车 上班，现在 不 再 坐 了。跟 以前 相比，现在 方便 多 了。', 'zh'),
      isTrue,
    );
    // Sin la comparación no cumple.
    expect(
      corregir(n4, '以前 我 每天 都 坐 公共汽车 上班，现在 不 再 坐 了。我 现在 开车 上班。', 'zh'),
      isFalse,
    );
    // N4: un deseo (要是 … 就 好 了) sin el lamento (早 知道 …) no cumple.
    final n4b = banco.firstWhere((u) => u.item.id == 'dx.zh.n4.escritura.2').item;
    expect(
      corregir(n4b, '要是 我 有 时间 就 好 了。早 知道 这么 忙，我 就 不 去 了。', 'zh'),
      isTrue,
    );
    expect(
      corregir(n4b, '要是 我 有 时间 就 好 了。我 想 去 北京 旅行。', 'zh'),
      isFalse,
    );
  });

  test('El tope es N4: lo publicado en la ruta y en el banco', () async {
    expect(idiomasConRuta, contains('zh'));
    final ruta = (await CargadorRuta().cargar('zh'))!;
    expect(nivelesPublicados(ruta), {1, 2, 3, 4});
    expect(nivelMaximoUbicacion(banco, publicados: nivelesPublicados(ruta)), 4);
  });

  testWidgets('Aprender: N1–N4 publicados y N5–N10 «Próximamente»', (tester) async {
    tester.view.physicalSize = const Size(390, 2600);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final ruta = (await tester.runAsync(() => CargadorRuta().cargar('zh')))!;
    // Un alumno ubicado por el diagnóstico antiguo en N8 estudia N4, el último publicado.
    const s = ProgressState(
      onboardingDone: true,
      nombre: 'Ana',
      idiomaMeta: 'zh',
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
    var ceros = 0, altos = 0;
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
      // Con cuatro niveles, un acertante con mucha suerte pasa rara vez de N1
      // (como en ja, ru y ko).
      expect(r.nivel, lessThanOrEqualTo(2), reason: 'azar, $d');
      if (r.nivel > 1) altos++;
      if (r.desdeCero) ceros++;
    }
    expect(altos, lessThanOrEqualTo(1), reason: '$altos de $n por encima de N1');
    expect(ceros / n, greaterThan(.9), reason: '$ceros de $n desde cero');
  });
}
