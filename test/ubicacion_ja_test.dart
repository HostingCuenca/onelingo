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

/// Prueba de ubicación v2 del japonés (versión esencial, curso completo):
/// banco real `assets/contenido/ja/diagnostico-v2.json`, N1–N10, apoyo
/// {es, en} y rōmaji (`textoRom`, `opcionesRom`) en cada texto y opción en
/// japonés de los ítems cerrados (kana, con espacios entre palabras; desde
/// N3, solo los kanji que enseña la ruta; la escritura no lleva rom).
/// Nunca ubica por encima de N10 (último nivel del curso, todo publicado).
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

  test('El banco cubre N1–N10 en las cinco habilidades y nada más', () {
    expect(json['idioma'], 'ja');
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
    expect(banco.where((u) => u.item.tieneRom), hasLength(160));
    // Sin cifras ni letras latinas en el japonés; N1–N2 van solo en kana y,
    // desde N3, cada kanji es uno enseñado hasta el nivel del ítem.
    final ensenados = {for (var n = 1; n <= 10; n++) n: kanjiHasta(n)};
    expect(ensenados[2], isEmpty);
    expect(ensenados[3], containsAll(['男', '言', '東', '大']));
    expect(ensenados[4], containsAll(['生', '気', '水']));
    expect(ensenados[5], containsAll(['遅', '急', '出', '発']));
    expect(ensenados[8], containsAll(['俳', '優', '撮', '影']));
    expect(ensenados[10], containsAll(['費', '融', '資', '貯']));
    // Cada nivel suma kanji al anterior (objetivo acumulado de la ficha).
    for (var n = 5; n <= 10; n++) {
      expect(ensenados[n]!.length, greaterThan(ensenados[n - 1]!.length), reason: 'N$n');
    }
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
    // N5: la causa (～ せいで) y lo que habría pasado (～たら ～た だろう).
    final n5 = banco.firstWhere((u) => u.item.id == 'dx.ja.n5.escritura.1').item;
    expect(
      corregir(n5, 'バス が こなかった せいで、 かいぎ に 遅れました。 もう すこし 急いで 出発 したら、 間に合った だろう。', 'ja'),
      isTrue,
    );
    expect(
      corregir(n5, 'バスがこなかったせいで、かいぎに遅れました。もうすこし急いで出発したら、間に合っただろう。', 'ja'),
      isTrue,
    );
    // Sin la suposición (～た だろう) no cumple aunque sea largo.
    expect(
      corregir(n5, 'バス が こなかった せいで、 かいぎ に 遅れました。 とても はずかしかった です。', 'ja'),
      isFalse,
    );
    // N6: contraste (～ いっぽう で) sin «～ に たいして» no cumple.
    final n6 = banco.firstWhere((u) => u.item.id == 'dx.ja.n6.escritura.1').item;
    expect(
      corregir(n6, '若者 は かくかぞく が いい と 思う いっぽう で、 老人 は だいかぞく が いい と 思います。 家族 は 大切 です。', 'ja'),
      isFalse,
    );
    // N7: sin «～ を のぞいて» no cumple.
    final n7 = banco.firstWhere((u) => u.item.id == 'dx.ja.n7.escritura.1').item;
    expect(
      corregir(n7, 'ご 意見 を ふまえて、 プラン を へんこう しました。 よさん に おうじて、 ホテル を えらべます。', 'ja'),
      isFalse,
    );
    // N8: informe formal con «～ むね»; sin «を もちまして» no cumple.
    final n8 = banco.firstWhere((u) => u.item.id == 'dx.ja.n8.escritura.2').item;
    expect(
      corregir(n8, '本日、 管理会社 に 電話 した むね を 報告 します。 対応 いただけない ようで あれば、 弁護士 に 相談 します。', 'ja'),
      isFalse,
    );
    // N9: con y sin espacios cumple; sin «と ばかり は いえ…» no.
    final n9 = banco.firstWhere((u) => u.item.id == 'dx.ja.n9.escritura.2').item;
    expect(
      corregir(n9, '知る限りでは、この会社は黒字です。全部は返済できないまでも、毎月少し返しています。理由は為替とばかりはいえません。', 'ja'),
      isTrue,
    );
    expect(
      corregir(n9, '知る 限り で は、 この 会社 は 黒字 です。 全部 は 返済 できない までも、 毎月 少し 返して います。', 'ja'),
      isFalse,
    );
    // N10: registro coloquial (って さ / ん だって); sin «ん だって» no cumple.
    final n10 = banco.firstWhere((u) => u.item.id == 'dx.ja.n10.escritura.1').item;
    expect(
      corregir(n10, 'たなかさん が ね、 あした は 暇 って さ。 けんたさん も 来る ん だって。 で、 どう なった の？', 'ja'),
      isTrue,
    );
    expect(
      corregir(n10, 'たなかさん が ね、 あした は 暇 って さ。 けんたさん も 来ます。 で、 どう なった の？', 'ja'),
      isFalse,
    );
  });

  test('El tope es N10: lo publicado en la ruta y en el banco', () async {
    expect(idiomasConRuta, contains('ja'));
    final ruta = (await CargadorRuta().cargar('ja'))!;
    expect(nivelesPublicados(ruta), {for (var n = 1; n <= 10; n++) n});
    expect(nivelMaximoUbicacion(banco, publicados: nivelesPublicados(ruta)), 10);
    // Cada nivel nuevo (N5–N10) trae sus 100 clases (50 + 50 de refuerzo).
    for (var n = 5; n <= 10; n++) {
      expect(ruta.delNivel('n$n'), hasLength(100), reason: 'N$n');
    }
  });

  testWidgets('Aprender: N1–N10 publicados y ninguno «Próximamente» ni «En preparación»', (tester) async {
    tester.view.physicalSize = const Size(390, 2600);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final ruta = (await tester.runAsync(() => CargadorRuta().cargar('ja')))!;
    // Un alumno ubicado en N8 estudia N8 (ya publicado); uno en N10, N10.
    const s8 = ProgressState(
      onboardingDone: true,
      nombre: 'Ana',
      idiomaMeta: 'ja',
      nivelInicial: 8,
    );
    expect(nivelAlumnoEnRuta(ruta, s8), 8);
    const s = ProgressState(
      onboardingDone: true,
      nombre: 'Ana',
      idiomaMeta: 'ja',
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
    var ok = 0;
    const n = 300;
    for (var k = 0; k < n; k++) {
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
      if ((r.nivel - t).abs() <= 1) ok++;
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
      final u = Ubicacion(banco: banco, declarado: d, nivelMaximo: 10, random: rnd);
      for (var i = u.siguiente(); i != null; i = u.siguiente()) {
        u.responder(rnd.nextInt(i.item.opciones.length) == i.item.indiceRespuesta);
      }
      if (u.escritura() != null) u.responder(false);
      final r = u.resultado();
      // Con diez niveles, un acertante con mucha suerte que se declara
      // avanzado pasa rara vez de N1 (como en ru, it, ko y zh).
      expect(r.nivel, lessThanOrEqualTo(2), reason: 'azar, $d');
      if (r.nivel > 1) altos++;
      if (r.desdeCero) ceros++;
    }
    expect(altos, lessThanOrEqualTo(1), reason: '$altos de $n por encima de N1');
    expect(ceros / n, greaterThan(.9), reason: '$ceros de $n desde cero');
  });
}
