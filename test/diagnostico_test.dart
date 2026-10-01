import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/diagnostico.dart';

/// Banco sintético: 6 preguntas objetivas por nivel (0-10) de distintas
/// competencias y una de escritura cada dos niveles.
List<PreguntaDiag> _banco() {
  final out = <PreguntaDiag>[];
  const skills = ['gramatica', 'vocabulario', 'comprension', 'tiempos', 'expresiones', 'cotidiano'];
  for (var n = 0; n <= 10; n++) {
    for (var i = 0; i < skills.length; i++) {
      out.add(PreguntaDiag(nivel: n, skill: skills[i], tipo: i.isEven ? TipoDiag.eleccion : TipoDiag.completar, tema: 'tema-$n-${skills[i]}', instruccion: '', texto: 'N$n-$i', opciones: i.isEven ? const ['ok', 'a', 'b', 'c'] : const [], correcta: i.isEven ? 0 : -1, aceptadas: i.isEven ? const [] : const ['ok']));
    }
    if (n.isEven && n > 0) out.add(PreguntaDiag(nivel: n, skill: 'escritura', tipo: TipoDiag.escritura, tema: 'escritura', instruccion: '', texto: 'W$n'));
  }
  return out;
}

/// Alumno cuyo nivel real es `real`: acierta las preguntas de nivel ≤ real
/// (y, para hacerlo realista, falla las de gramática por encima de real-1).
ResultadoDiag _simular(double real, int declarado, {bool debilGramatica = false}) {
  final d = Diagnostico(declarado: declarado, banco: _banco(), random: Random(1));
  while (true) {
    final q = d.siguiente();
    if (q == null) break;
    if (q.esEscritura) {
      d.registrarEscritura('some text with several words in it here', EvaluacionEscritura(puntuacion: real));
      continue;
    }
    var sabe = q.nivel <= real;
    if (debilGramatica && q.skill == 'gramatica' && q.nivel > real - 2) sabe = false;
    d.responder(sabe ? 'ok' : 'a');
  }
  return d.resultado();
}

void main() {
  test('converge al nivel real desde distintos niveles declarados', () {
    for (final real in [1.0, 3.0, 5.0, 7.0, 9.0]) {
      for (final declarado in [1, 4, 7, 10]) {
        final r = _simular(real, declarado);
        expect((r.nivel - real).abs(), lessThanOrEqualTo(1.0), reason: 'real $real declarado $declarado → ${r.nivel} (${r.preguntas} preguntas)');
        expect(r.preguntas, inInclusiveRange(10, 25));
      }
    }
  });

  test('responder al azar no deja a nadie en un nivel alto', () {
    for (final declarado in [4, 7, 10]) {
      for (var semilla = 0; semilla < 40; semilla++) {
        final azar = Random(semilla);
        final d = Diagnostico(
          declarado: declarado,
          banco: _banco(),
          random: Random(semilla),
        );
        while (true) {
          final q = d.siguiente();
          if (q == null) break;
          if (q.esEscritura) {
            // Sin IA, la escritura de respaldo parte de la estimación actual.
            d.registrarEscritura(
              'asdf qwer zxcv',
              Diagnostico.evaluarLocal('asdf qwer zxcv', d.estimacion),
            );
            continue;
          }
          // Elige una opción cualquiera o escribe algo sin sentido.
          d.responder(
            q.conOpciones
                ? q.opciones[azar.nextInt(q.opciones.length)]
                : 'xyz',
          );
        }
        expect(
          d.resultado().nivel,
          lessThanOrEqualTo(2),
          reason: 'declarado $declarado, semilla $semilla',
        );
      }
    }
  });

  test('parte del nivel declarado y nunca salta más de un nivel por respuesta', () {
    final d = Diagnostico(declarado: 7, banco: _banco(), random: Random(2));
    final q = d.siguiente()!;
    expect(q.nivel, 7);
    var anterior = d.estimacion;
    d.responder('a');
    expect((d.estimacion - anterior).abs(), lessThanOrEqualTo(1.0));
    anterior = d.estimacion;
    d.siguiente();
    d.responder('ok');
    expect((d.estimacion - anterior).abs(), lessThanOrEqualTo(1.0));
  });

  test('incluye producción escrita antes de terminar y la pesa más', () {
    final r = _simular(6.0, 6);
    expect(r.escritura, isNotNull);
    expect(r.skills.containsKey('escritura'), isTrue);
  });

  test('una debilidad concentrada no hunde el nivel global y aparece en el plan', () {
    final r = _simular(7.0, 7, debilGramatica: true);
    expect(r.nivel, greaterThanOrEqualTo(6.0));
    // La gramática queda como la competencia más baja.
    final otras = [
      for (final e in r.skills.entries)
        if (e.key != 'gramatica' && e.key != 'escritura') e.value,
    ];
    expect(r.skills['gramatica']!, lessThan(otras.reduce(min)));
    expect(r.refuerzo.any((t) => t.contains('gramatica')), isTrue);
  });

  test('quien no supera el nivel 1 va a Fundamentos', () {
    final r = _simular(0.0, 2);
    expect(r.recomendado, 0);
    expect(r.cefr, startsWith('Pre-A1'));
  });

  test('las opciones se barajan y la correcta sigue siendo la misma', () {
    final banco = [for (var i = 0; i < 30; i++) PreguntaDiag(nivel: 5, skill: 'gramatica', tipo: TipoDiag.eleccion, tema: 't', instruccion: '', texto: 'q$i', opciones: const ['ok', 'a', 'b', 'c'], correcta: 0)];
    var primeras = 0;
    for (var s = 0; s < 30; s++) {
      final d = Diagnostico(declarado: 5, banco: banco, random: Random(s));
      final q = d.siguiente()!;
      expect(q.opciones[q.correcta], 'ok');
      if (q.opciones.first == 'ok') primeras++;
      expect(d.responder('ok'), isTrue);
    }
    expect(primeras, lessThan(20));
  });

  test('la escritura pesa un 35 % en el nivel final', () {
    final d = Diagnostico(declarado: 9, banco: _banco(), random: Random(3));
    for (var i = 0; i < 9; i++) {
      final q = d.siguiente()!;
      if (q.esEscritura) { d.registrarEscritura('texto de prueba con varias palabras', const EvaluacionEscritura(puntuacion: 4.5)); continue; }
      d.responder('ok');
    }
    while (!d.terminado) {
      final q = d.siguiente();
      if (q == null) break;
      if (q.esEscritura) { d.registrarEscritura('texto de prueba con varias palabras', const EvaluacionEscritura(puntuacion: 4.5)); continue; }
      d.responder('ok');
    }
    final r = d.resultado();
    expect(r.nivel, lessThanOrEqualTo(8.5), reason: 'objetivo alto pero escritura 4.5 → ${r.nivel}');
    expect(r.nivel, greaterThanOrEqualTo(6.5));
  });

  test('con generador de IA el motor pide nivel, competencia y tipo variados y cae al banco si falla', () async {
    final pedidas = <PeticionDiag>[];
    final d = Diagnostico(declarado: 5, banco: _banco(), random: Random(4), generador: (p) async {
      pedidas.add(p);
      if (pedidas.length % 3 == 0) return null; // la IA falla a veces
      return PreguntaDiag(nivel: p.nivel, skill: p.skill, tipo: p.tipo, tema: 't', instruccion: '', texto: 'IA-${pedidas.length}', opciones: p.tipo == TipoDiag.escritura || p.tipo == TipoDiag.completar || p.tipo == TipoDiag.corta || p.tipo == TipoDiag.dictado ? const [] : const ['ok', 'a', 'b', 'c'], correcta: p.tipo == TipoDiag.escritura || p.tipo == TipoDiag.completar || p.tipo == TipoDiag.corta || p.tipo == TipoDiag.dictado ? -1 : 0, aceptadas: p.tipo == TipoDiag.escritura ? const [] : const ['ok', 'IA'] );
    });
    var origenes = <String>{};
    while (true) {
      final q = await d.siguienteAsync();
      if (q == null) break;
      origenes.add(d.origenActual);
      if (q.esEscritura) { d.registrarEscritura('texto de prueba con varias palabras', const EvaluacionEscritura(puntuacion: 5)); continue; }
      d.responder(q.conOpciones ? 'ok' : (q.tipo == TipoDiag.dictado ? q.texto : 'ok'));
    }
    expect(pedidas.first.nivel, 5);
    expect(pedidas.map((p) => p.skill).toSet().length, greaterThanOrEqualTo(5), reason: 'competencias variadas');
    expect(pedidas.map((p) => p.tipo).toSet().length, greaterThanOrEqualTo(4), reason: 'tipos variados');
    expect(origenes, containsAll(['ia', 'banco']));
    expect(d.resultado().preguntas, inInclusiveRange(10, 25));
  });

  test('equivalencia MCER', () {
    expect(cefrDe(6.5), 'B1');
    expect(cefrDe(7), 'B2');
    expect(cefrDe(2), 'A1');
  });
}
