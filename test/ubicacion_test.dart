import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/ubicacion.dart';

/// Banco sintético con la forma del real: 4 ítems por nivel y habilidad
/// (3 opciones) y 2 de escritura por nivel.
List<ItemUbicacion> bancoSintetico() => [
  for (var nivel = 1; nivel <= 10; nivel++) ...[
    for (final h in habilidadesUbicacion)
      for (var k = 1; k <= 4; k++)
        ItemUbicacion.fromJson({
          'id': 'dx.en.n$nivel.$h.$k',
          'nivel': nivel,
          'habilidad': h,
          'formato': 'elegir',
          'consigna': {'es': 'x'},
          'feedback': {'es': 'x'},
          'opciones': ['a', 'b', 'c'],
          'respuesta': 0,
        }),
    for (var k = 1; k <= 2; k++)
      ItemUbicacion.fromJson({
        'id': 'dx.en.n$nivel.escritura.$k',
        'nivel': nivel,
        'habilidad': 'escritura',
        'formato': 'escribir',
        'consigna': {'es': 'x'},
        'feedback': {'es': 'x'},
        'respuesta': 'x',
      }),
  ],
];

/// Alumno simulado: acierta el 92 % de lo que domina, el 45 % un nivel por
/// encima y adivina (1/3) más arriba.
class Alumno {
  Alumno(this.niveles, this.rnd);
  final Map<String, int> niveles;
  final Random rnd;
  bool responde(ItemUbicacion i) {
    final t = i.habilidad == 'escritura'
        ? niveles.values.reduce(min)
        : niveles[i.habilidad]!;
    final p = i.nivel <= t
        ? .92
        : i.nivel == t + 1
        ? .45
        : 1 / 3;
    return rnd.nextDouble() < p;
  }
}

({ResultadoUbicacion r, int maxNivelVisto}) correr(
  Alumno a,
  Autodeclaracion d,
  Random rnd,
) {
  final u = Ubicacion(banco: bancoSintetico(), declarado: d, random: rnd);
  var maxVisto = 0;
  while (true) {
    final i = u.siguiente();
    if (i == null) break;
    maxVisto = max(maxVisto, i.nivel);
    u.responder(a.responde(i));
  }
  final w = u.escritura();
  if (w != null) u.responder(a.responde(w));
  expect(u.terminado, isTrue);
  return (r: u.resultado(), maxNivelVisto: maxVisto);
}

int inicioReal(Map<String, int> t) {
  final v = t.values.toList();
  return min((v.reduce((a, b) => a + b) / v.length).floor(), v.reduce(min) + 2);
}

void main() {
  test('«Nada»: empieza desde cero sin preguntas', () {
    final u = Ubicacion(
      banco: bancoSintetico(),
      declarado: Autodeclaracion.nada,
    );
    expect(u.siguiente(), isNull);
    expect(u.terminado, isTrue);
    expect(u.resultado().nivel, 0);
    expect(u.resultado().desdeCero, isTrue);
  });

  test(
    'Sin conocimientos: termina en pocas preguntas y propone empezar de 0',
    () {
      final rnd = Random(11);
      var total = 0, ceros = 0;
      for (var k = 0; k < 200; k++) {
        final a = Alumno({for (final h in habilidadesUbicacion) h: 0}, rnd);
        final x = correr(a, Autodeclaracion.poco, rnd);
        total += x.r.preguntas;
        if (x.r.nivel == 0) ceros++;
      }
      expect(total / 200, lessThan(9));
      expect(ceros / 200, greaterThan(.9));
    },
  );

  test('Precisión: habilidades e inicio a ±1 nivel en alumnos simulados', () {
    final rnd = Random(7);
    var ok = 0, tot = 0, okInicio = 0, sobre = 0, preguntas = 0;
    const n = 400;
    for (var k = 0; k < n; k++) {
      final base = rnd.nextInt(11);
      final t = {
        for (final h in habilidadesUbicacion)
          h: (base + [-1, 0, 0, 1][rnd.nextInt(4)]).clamp(0, 10),
      };
      final d = Autodeclaracion.desdeNivel(
        (base + [-1, 0, 1][rnd.nextInt(3)]).clamp(1, 10),
      );
      final x = correr(Alumno(t, rnd), d, rnd);
      preguntas += x.r.preguntas;
      expect(x.r.preguntas, lessThanOrEqualTo(23));
      for (final h in habilidadesUbicacion) {
        tot++;
        if ((x.r.habilidades[h]! - t[h]!).abs() <= 1) ok++;
        if (x.r.habilidades[h]! > t[h]! + 1) sobre++;
      }
      if ((x.r.nivel - inicioReal(t)).abs() <= 1) okInicio++;
    }
    expect(ok / tot, greaterThan(.88), reason: 'habilidades ±1');
    expect(okInicio / n, greaterThan(.9), reason: 'inicio ±1');
    expect(sobre / tot, lessThan(.05), reason: 'sobreubicación');
    expect(preguntas / n, lessThan(21));
  });

  test('Un alumno A1 no recibe preguntas de B2 en adelante', () {
    final rnd = Random(3);
    var altas = 0;
    for (var k = 0; k < 200; k++) {
      final a = Alumno({for (final h in habilidadesUbicacion) h: 1}, rnd);
      final x = correr(a, Autodeclaracion.poco, rnd);
      if (x.maxNivelVisto >= 5) altas++;
    }
    expect(altas / 200, lessThan(.05));
  });
}
