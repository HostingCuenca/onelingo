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

/// Prueba de ubicación v2 del japonés (versión esencial): banco real
/// `assets/contenido/ja/diagnostico-v2.json`, N1–N4, apoyo {es, en} y rōmaji
/// (`textoRom`, `opcionesRom`) en cada texto y opción en japonés (kana, con
/// espacios entre palabras; desde N3, solo los kanji que enseña la ruta).
/// Nunca ubica por encima de N4 (último nivel con clases publicadas).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final json =
      jsonDecode(File('assets/contenido/ja/diagnostico-v2.json').readAsStringSync())
          as Map<String, dynamic>;
  final banco = ItemUbicacion.bancoLocalizado(json, 'es');
  final kana = RegExp(r'[ぁ-ゖァ-ヺー]');
  final kanji = RegExp(r'[一-鿿㐀-䶿]');

  /// Kanji enseñados hasta el final de cada nivel: los del vocabulario y las
  /// tablas de la ruta publicada (como `kanji_ensenados_ja` de
  /// tools/contenido/validar_diagnostico.py).
  Set<String> kanjiHasta(int nivel) {
    const base = 'assets/contenido/ja/ruta';
    final curso =
        jsonDecode(File('$base/curso.json').readAsStringSync())
            as Map<String, dynamic>;
    final res = <String>{};
    for (final m in curso['modulos'] as List) {
      final datos =
          jsonDecode(File('$base/${m['archivo']}').readAsStringSync())
              as Map<String, dynamic>;
      for (final u in datos['unidades'] as List) {
        final interno = u['nivelInterno'] as int?;
        if (interno == null || interno > nivel) continue;
        final textos = [
          for (final v in u['vocabulario'] as List? ?? const []) v['texto'],
          for (final p in u['pasos'] as List? ?? const [])
            if (p['tipo'] == 'tabla')
              for (final fila in p['filas'] as List? ?? const [])
                for (final c in fila as List)
                  if (c is Map) c['texto'],
        ];
        for (final t in textos.whereType<String>()) {
          res.addAll(kanji.allMatches(t).map((m) => m[0]!));
        }
      }
    }
    return res;
  }

  test('El banco cubre N1–N4 en las cinco habilidades y nada más', () {
    expect(json['idioma'], 'ja');
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

  test('Rōmaji bajo cada texto y opción en japonés; el audio no lo lleva', () {
    for (final u in banco) {
      final it = u.item;
      if (kana.hasMatch(it.texto ?? '')) {
        expect(it.textoRom, isNotNull, reason: it.id);
      }
      for (var i = 0; i < it.opciones.length; i++) {
        if (kana.hasMatch(it.opciones[i].meta ?? '')) {
          expect(it.romOpcion(i), isNotNull, reason: '${it.id} opción $i');
        }
      }
      if (it.formato == FormatoItem.escuchar) {
        expect(it.audio, isNotNull, reason: it.id);
        expect(it.texto, isNull, reason: it.id);
      }
    }
    expect(banco.where((u) => u.item.tieneRom), hasLength(64));
    // Sin cifras ni letras latinas en el japonés; N1–N2 van solo en kana y,
    // desde N3, cada kanji es uno enseñado hasta el nivel del ítem.
    final ensenados = {for (var n = 1; n <= 4; n++) n: kanjiHasta(n)};
    expect(ensenados[2], isEmpty);
    expect(ensenados[3], containsAll(['男', '言', '東', '大']));
    expect(ensenados[4], containsAll(['生', '気', '水']));
    for (final u in banco) {
      final it = u.item;
      final textos = [
        it.texto, it.audio, ...it.opciones.map((o) => o.meta), //
        if (it.formato == FormatoItem.escribir) ...[it.respuesta, ...it.aceptadas],
      ];
      for (final t in textos.whereType<String>()) {
        if (!kana.hasMatch(t) && !kanji.hasMatch(t)) continue;
        expect(RegExp('[0-9A-Za-z]').hasMatch(t), isFalse, reason: '${it.id}: $t');
        for (final k in kanji.allMatches(t).map((m) => m[0]!)) {
          expect(ensenados[u.nivel], contains(k), reason: '${it.id}: $k en $t');
        }
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
          expect(corregir(it, it.respuesta!, 'ja'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'ja'), isFalse, reason: it.id);
        case FormatoItem.escribir:
          for (final t in [it.respuesta!, ...it.aceptadas]) {
            expect(corregir(it, t, 'ja'), isTrue, reason: '${it.id}: $t');
            // El alumno escribe sin espacios (teclado japonés): también vale.
            final junto = t.replaceAll(' ', '');
            expect(corregir(it, junto, 'ja'), isTrue, reason: '${it.id}: $junto');
          }
          expect(corregir(it, 'こんにちは。', 'ja'), isFalse, reason: it.id);
        default:
          final otra = (it.indiceRespuesta! + 1) % it.opciones.length;
          expect(corregir(it, it.indiceRespuesta, 'ja'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'ja'), isFalse, reason: it.id);
      }
    }
  });

  test('Escritura en japonés: extensión en caracteres y evidencias sin espacios', () {
    final it = banco
        .firstWhere((u) => u.item.id == 'dx.ja.n1.escritura.1')
        .item;
    expect(
      corregir(it, 'わたしはゆきです。とうきょうのかいしゃではたらきます。コーヒーがすきです。', 'ja'),
      isTrue,
    );
    // Con y sin espacios entre palabras, y con la puntuación que sea.
    expect(
      corregir(it, 'わたし は ゆき です、 とうきょう に すんで います、 おんがく が すき です', 'ja'),
      isTrue,
    );
    // Falta qué le gusta: no cumple la rúbrica aunque sea largo.
    expect(
      corregir(it, 'わたし は ゆき です。 とうきょう の かいしゃ で はたらきます。', 'ja'),
      isFalse,
    );
    // Demasiado corto (menos de doce caracteres).
    expect(corregir(it, 'ゆき です', 'ja'), isFalse);
    // N3: lo que ahora puede hacer (～ように なりました) y un hábito (～ように して います).
    final n3 = banco.firstWhere((u) => u.item.id == 'dx.ja.n3.escritura.1').item;
    expect(
      corregir(n3, 'まえ は ピアノ が にがて でした。 いま は ひける ように なりました。 まいにち れんしゅう する ように して います。', 'ja'),
      isTrue,
    );
    expect(
      corregir(n3, 'まえはピアノがにがてでした。いまはひけるようになりました。まいにちれんしゅうするようにしています。', 'ja'),
      isTrue,
    );
    // Sin el hábito no cumple aunque sea largo.
    expect(
      corregir(n3, 'まえ は ピアノ が にがて でした。 いま は ひける ように なりました。 とても うれしい です。', 'ja'),
      isFalse,
    );
    // N3: una invitación sin qué pasa si llueve (～たら / なら) no cumple.
    final n3b = banco.firstWhere((u) => u.item.id == 'dx.ja.n3.escritura.2').item;
    expect(
      corregir(n3b, 'どようび に うみ へ いきません か。 大雨 だったら、 えいが を みましょう。', 'ja'),
      isTrue,
    );
    expect(
      corregir(n3b, 'どようび に うみ へ いきません か。 そのあと、 えいが を みましょう。', 'ja'),
      isFalse,
    );
    // N4: un plan (～よう と おもって います) y algo que lamenta (～ば よかった).
    final n4 = banco.firstWhere((u) => u.item.id == 'dx.ja.n4.escritura.1').item;
    expect(
      corregir(n4, 'らいねん は にほん に りゅうがく しよう と おもって います。 もっと はやく べんきょう すれば よかった です。', 'ja'),
      isTrue,
    );
    // Sin lo que lamenta no cumple.
    expect(
      corregir(n4, 'らいねん は にほん に りゅうがく しよう と おもって います。 まいにち べんきょう して います。', 'ja'),
      isFalse,
    );
    // N4: la avería sin la petición cortés (～て いただけません か) no cumple.
    final n4b = banco.firstWhere((u) => u.item.id == 'dx.ja.n4.escritura.2').item;
    expect(
      corregir(n4b, 'すみません。 水道 が こわれて います ので、 みて いただけません か？', 'ja'),
      isTrue,
    );
    expect(
      corregir(n4b, 'すみません。 水道 が こわれて います。 とても こまって います。', 'ja'),
      isFalse,
    );
  });

  test('El tope es N4: lo publicado en la ruta y en el banco', () async {
    expect(idiomasConRuta, contains('ja'));
    final ruta = (await CargadorRuta().cargar('ja'))!;
    expect(nivelesPublicados(ruta), {1, 2, 3, 4});
    expect(nivelMaximoUbicacion(banco, publicados: nivelesPublicados(ruta)), 4);
  });

  testWidgets('Aprender: N1–N4 publicados y N5–N10 «Próximamente»', (tester) async {
    tester.view.physicalSize = const Size(390, 2600);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final ruta = (await tester.runAsync(() => CargadorRuta().cargar('ja')))!;
    // Un alumno ubicado por el diagnóstico antiguo en N8 estudia N4, el último publicado.
    const s = ProgressState(
      onboardingDone: true,
      nombre: 'Ana',
      idiomaMeta: 'ja',
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
      // (≈ 0,03 % de los alumnos en 200 semillas, como en ru y ko).
      expect(r.nivel, lessThanOrEqualTo(2), reason: 'azar, $d');
      if (r.nivel > 1) altos++;
      if (r.desdeCero) ceros++;
    }
    expect(altos, lessThanOrEqualTo(1), reason: '$altos de $n por encima de N1');
    expect(ceros / n, greaterThan(.9), reason: '$ceros de $n desde cero');
  });
}
