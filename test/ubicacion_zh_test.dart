import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/correccion.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/aprendizaje/providers.dart' show idiomasConRuta;
import 'package:onelingo/core/aprendizaje/ubicacion.dart';

/// Prueba de ubicación v2 del chino mandarín (versión esencial): banco real
/// `assets/contenido/zh/diagnostico-v2.json`, N1–N2, apoyo {es, en} y pinyin
/// (`textoRom`, `opcionesRom`) en cada texto y opción en chino.
/// Nunca ubica por encima de N2 (último nivel con clases publicadas).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final json =
      jsonDecode(File('assets/contenido/zh/diagnostico-v2.json').readAsStringSync())
          as Map<String, dynamic>;
  final banco = ItemUbicacion.bancoLocalizado(json, 'es');
  final hanzi = RegExp(r'[一-鿿]');

  test('El banco cubre N1–N2 en las cinco habilidades y nada más', () {
    expect(json['idioma'], 'zh');
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
    expect(banco.where((u) => u.item.tieneRom), hasLength(32));
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
  });

  test('El tope es N2: lo publicado en la ruta y en el banco', () async {
    expect(idiomasConRuta, contains('zh'));
    final ruta = (await CargadorRuta().cargar('zh'))!;
    expect(nivelesPublicados(ruta), {1, 2});
    expect(nivelMaximoUbicacion(banco, publicados: nivelesPublicados(ruta)), 2);
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
