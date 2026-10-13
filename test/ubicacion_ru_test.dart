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

/// Prueba de ubicación v2 del ruso (versión esencial, curso completo): banco
/// real `assets/contenido/ru/diagnostico-v2.json`, N1–N10, apoyo {es, en} y
/// romanización (`textoRom`, `opcionesRom`) en cada texto y opción en ruso
/// (cirílico sin marcas de acento; el acento va solo en el rom).
/// Nunca ubica por encima de N10 (último nivel del curso, todo publicado).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final json =
      jsonDecode(File('assets/contenido/ru/diagnostico-v2.json').readAsStringSync())
          as Map<String, dynamic>;
  final banco = ItemUbicacion.bancoLocalizado(json, 'es');
  final cirilico = RegExp(r'[А-Яа-яЁё]');

  test('El banco cubre N1–N10 en las cinco habilidades y nada más', () {
    expect(json['idioma'], 'ru');
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

  test('Rom bajo cada texto y opción en ruso; el audio no lo lleva', () {
    for (final u in banco) {
      final it = u.item;
      if (cirilico.hasMatch(it.texto ?? '')) {
        expect(it.textoRom, isNotNull, reason: it.id);
      }
      for (var i = 0; i < it.opciones.length; i++) {
        if (cirilico.hasMatch(it.opciones[i].meta ?? '')) {
          expect(it.romOpcion(i), isNotNull, reason: '${it.id} opción $i');
        }
      }
      if (it.formato == FormatoItem.escuchar) {
        expect(it.audio, isNotNull, reason: it.id);
        expect(it.texto, isNull, reason: it.id);
      }
    }
    expect(banco.where((u) => u.item.tieneRom), hasLength(160));
    // El cirílico nunca lleva marca de acento (U+0301): el acento va solo en
    // el rom. Ninguna cifra ni símbolo en lo que se lee o se oye, y sin Lumo.
    final prohibido = RegExp('[\u0301₽%0-9]');
    for (final u in banco) {
      final it = u.item;
      for (final t in [it.texto, it.audio, ...it.opciones.map((o) => o.meta)]) {
        expect(prohibido.hasMatch(t ?? ''), isFalse, reason: '${it.id}: $t');
      }
      expect(it.id, startsWith('dx.ru.n'));
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
          expect(corregir(it, it.respuesta!, 'ru'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'ru'), isFalse, reason: it.id);
        case FormatoItem.escribir:
          for (final t in [it.respuesta!, ...it.aceptadas]) {
            expect(corregir(it, t, 'ru'), isTrue, reason: '${it.id}: $t');
            // Sin mayúsculas ni puntuación y con «е» por «ё»: también vale.
            final llana = t
                .toLowerCase()
                .replaceAll(RegExp(r'[.,!?]'), '')
                .replaceAll('ё', 'е');
            expect(corregir(it, llana, 'ru'), isTrue, reason: '${it.id}: $llana');
          }
          expect(corregir(it, 'Здравствуйте!', 'ru'), isFalse, reason: it.id);
        default:
          final otra = (it.indiceRespuesta! + 1) % it.opciones.length;
          expect(corregir(it, it.indiceRespuesta, 'ru'), isTrue, reason: it.id);
          expect(corregir(it, otra, 'ru'), isFalse, reason: it.id);
      }
    }
  });

  test('Escritura en ruso: extensión en palabras y evidencias con ё ≡ е', () {
    final n1 = banco.firstWhere((u) => u.item.id == 'dx.ru.n1.escritura.1').item;
    expect(
      corregir(n1, 'Меня зовут Анна. Я живу в Москве. Я люблю кофе.', 'ru'),
      isTrue,
    );
    // Sin mayúsculas ni puntuación y con otros datos.
    expect(
      corregir(n1, 'меня зовут иван я работаю в школе я люблю футбол', 'ru'),
      isTrue,
    );
    // Falta qué le gusta: no cumple la rúbrica aunque sea largo.
    expect(
      corregir(n1, 'Меня зовут Анна. Я живу в Москве. Я работаю в школе.', 'ru'),
      isFalse,
    );
    // Demasiado corto (menos de siete palabras).
    expect(corregir(n1, 'Меня зовут Анна.', 'ru'), isFalse);
    // «ё» y «е» son lo mismo para quien escribe sin ё (teclado, hábito).
    final n2 = banco.firstWhere((u) => u.item.id == 'dx.ru.n2.escritura.1').item;
    expect(
      corregir(n2, 'Утром я был дома. Днем я купил подарок. Вечером я читал.', 'ru'),
      isTrue,
    );
    expect(
      corregir(n2, 'Утром я был дома. Днём я купил подарок. Вечером я читал.', 'ru'),
      isTrue,
    );
    // Sin verbo en pasado no cumple.
    expect(
      corregir(n2, 'Утром я дома. Днём я в офисе. Потом я в парке.', 'ru'),
      isFalse,
    );
    // N3: lo ya logrado (уже) y lo pendiente (ещё не), con ё ≡ е.
    final n3 = banco.firstWhere((u) => u.item.id == 'dx.ru.n3.escritura.1').item;
    expect(
      corregir(n3, 'Я уже нашла работу и наконец сдала экзамен. Но квартиру я ещё не нашла.', 'ru'),
      isTrue,
    );
    expect(
      corregir(n3, 'я уже нашел работу и наконец сдал экзамен но я еще не нашел квартиру', 'ru'),
      isTrue,
    );
    // Sin nada pendiente no cumple.
    expect(
      corregir(n3, 'Я уже нашёл работу и наконец сдал экзамен. Я живу у сестры.', 'ru'),
      isFalse,
    );
    expect(corregir(n3, 'Я уже нашёл работу.', 'ru'), isFalse);
    // N3: una propuesta sin finalidad (чтобы) no cumple.
    final n3b = banco.firstWhere((u) => u.item.id == 'dx.ru.n3.escritura.2').item;
    expect(
      corregir(n3b, 'Я предлагаю поставить скамейки во дворе. Если бы у нас был бюджет, мы бы посадили цветы.', 'ru'),
      isFalse,
    );
    // N4: el pasado habitual (бывало / раньше) frente al presente (теперь).
    final n4 = banco.firstWhere((u) => u.item.id == 'dx.ru.n4.escritura.1').item;
    expect(
      corregir(n4, 'Раньше мы жили в посёлке и часто играли во дворе. А теперь мы живём в Москве. Я скучаю по родному городу.', 'ru'),
      isTrue,
    );
    expect(
      corregir(n4, 'раньше мы жили в поселке и часто играли во дворе а теперь мы живем в москве я скучаю по родному городу', 'ru'),
      isTrue,
    );
    // Sin el contraste con el presente no cumple.
    expect(
      corregir(n4, 'Раньше мы жили в посёлке. Мы часто играли во дворе. Я скучаю по родному городу.', 'ru'),
      isFalse,
    );
    // N4: correo formal sin petición (прошу / просьба) no cumple.
    final n4b = banco.firstWhere((u) => u.item.id == 'dx.ru.n4.escritura.2').item;
    expect(
      corregir(n4b, 'Здравствуйте! Пишу вам по поводу перевода: деньги ещё не пришли. С уважением, Андрей.', 'ru'),
      isFalse,
    );
    expect(
      corregir(n4b, 'Здравствуйте! Пишу вам по поводу перевода: деньги ещё не пришли. Прошу вас проверить перевод. С уважением, Андрей.', 'ru'),
      isTrue,
    );
    // N5: relato de adaptación con gerundio, lo que sigue (всё ещё / больше не)
    // y la adaptación (привык к); sin la adaptación no cumple.
    final n5 = banco.firstWhere((u) => u.item.id == 'dx.ru.n5.escritura.1').item;
    expect(
      corregir(n5, 'переехав в москву я сразу нашел жилье живя в новом районе я привык к городу я все еще скучаю по дому но больше не чувствую себя чужим', 'ru'),
      isTrue,
    );
    expect(
      corregir(n5, 'Переехав в Москву, я сразу нашёл жильё. Я всё ещё скучаю по дому, но больше не чувствую себя чужим.', 'ru'),
      isFalse,
    );
    // N8: carta de reclamación sin la consecuencia (в противном случае) no cumple.
    final n8 = banco.firstWhere((u) => u.item.id == 'dx.ru.n8.escritura.1').item;
    expect(
      corregir(n8, 'Обращаюсь к вам по поводу двойной комиссии за мою карту. Согласно акту проверки, банк допустил ошибку. Прошу перечислить деньги на мой счёт в течение десяти рабочих дней.', 'ru'),
      isFalse,
    );
    // N10: solicitud de crédito; demasiado corta no cumple aunque tenga las claves.
    final n10 = banco.firstWhere((u) => u.item.id == 'dx.ru.n10.escritura.1').item;
    expect(
      corregir(n10, 'Кредит в размере ста тысяч, двенадцать процентов годовых, срок погашения пять лет.', 'ru'),
      isFalse,
    );
  });

  test('El tope es N10: lo publicado en la ruta y en el banco', () async {
    expect(idiomasConRuta, contains('ru'));
    final ruta = (await CargadorRuta().cargar('ru'))!;
    expect(nivelesPublicados(ruta), {for (var n = 1; n <= 10; n++) n});
    expect(nivelMaximoUbicacion(banco, publicados: nivelesPublicados(ruta)), 10);
  });

  testWidgets('Aprender: N1–N10 publicados y ninguno «Próximamente» ni «En preparación»', (tester) async {
    tester.view.physicalSize = const Size(390, 2600);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    final ruta = (await tester.runAsync(() => CargadorRuta().cargar('ru')))!;
    // Un alumno ubicado en N10 estudia N10: ya está publicado.
    const s = ProgressState(
      onboardingDone: true,
      nombre: 'Ana',
      idiomaMeta: 'ru',
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
      // avanzado pasa rara vez de N1 (como en it, zh y ja).
      expect(r.nivel, lessThanOrEqualTo(2), reason: 'azar, $d');
      if (r.nivel > 1) altos++;
      if (r.desdeCero) ceros++;
    }
    expect(altos, lessThanOrEqualTo(1), reason: '$altos de $n por encima de N1');
    expect(ceros / n, greaterThan(.9), reason: '$ceros de $n desde cero');
  });
}
