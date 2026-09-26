import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/biblioteca.dart';
import 'package:onelingo/core/diagnostico.dart';
import 'package:onelingo/core/state/providers.dart';

void main() {
  final raw = jsonDecode(
    File('assets/contenido/en/biblioteca.json').readAsStringSync(),
  ) as Map;
  final bank = (raw['preguntas'] as List)
      .map((q) => PreguntaDiag.fromJson(Map<String, dynamic>.from(q)))
      .toList();
  test('biblioteca íntegra: IDs, respuestas, imágenes y pares de lectura', () {
    expect(bank.length, 116);
    expect(bank.map((q) => q.id).toSet().length, bank.length);
    for (final q in bank) {
      expect(q.nivel, inInclusiveRange(1, 10));
      expect(q.explicacion, isNotEmpty);
      if (q.conOpciones) {
        expect(q.opciones.toSet().length, q.opciones.length);
        expect(q.correcta, inInclusiveRange(0, q.opciones.length - 1));
      } else if (!q.esEscritura) {
        expect(q.aceptadas, isNotEmpty);
      }
      if (q.imagen.isNotEmpty) expect(File(q.imagen).existsSync(), isTrue);
    }
    for (var n = 1; n <= 10; n++) {
      expect(
        bank.where((q) => q.nivel == n).map((q) => q.skill).toSet(),
        containsAll(RutaBiblioteca.habilidades),
      );
    }
  });
  test(
    'el audio no revela textos de lectura ni vocabulario y cubre los extremos',
    () async {
      final other = bank
          .where((q) => q.skill != 'listening')
          .map((q) => q.texto)
          .toSet();
      final audio = bank.where((q) => q.skill == 'listening').toList();
      expect(audio.map((q) => q.texto).toSet().length, audio.length);
      expect(audio.any((q) => other.contains(q.texto)), isFalse);
      for (final level in [1, 10]) {
        for (var seed = 0; seed < 100; seed++) {
          final d = Diagnostico(
            declarado: level,
            banco: bank,
            personalizado: true,
            random: Random(seed),
            generador: (_) => throw StateError('Biblioteca agotada'),
          );
          for (var i = 0; i < 10; i++) {
            final q = (await d.siguienteAsync())!;
            if (q.esEscritura) {
              d.registrarEscritura(
                'Sample',
                EvaluacionEscritura(puntuacion: level.toDouble()),
              );
            } else {
              d.responder(
                seed % 3 == 0 || (seed % 3 == 1 && i.isEven)
                    ? q.respuestaCorrecta
                    : 'incorrect answer',
              );
            }
          }
        }
      }
    },
  );
  for (var level = 1; level <= 10; level++) {
    test(
      'diagnóstico nivel $level usa biblioteca sin generar preguntas',
      () async {
        final d = Diagnostico(
          declarado: level,
          banco: bank,
          personalizado: true,
          generador: (_) =>
              throw StateError('No debe consumir IA para generar'),
        );
        for (var i = 0; i < 10; i++) {
          final q = (await d.siguienteAsync())!;
          expect(d.origenActual, 'banco');
          if (q.esEscritura) {
            d.registrarEscritura(
              'Sample',
              EvaluacionEscritura(puntuacion: level.toDouble()),
            );
          } else {
            d.responder(i.isEven ? q.respuestaCorrecta : 'incorrect answer');
          }
        }
        expect(await d.siguienteAsync(), isNull);
      },
    );
  }
  test(
    'mismo nivel con debilidades distintas produce prioridades distintas',
    () {
      expect(
        RutaBiblioteca.prioridades({
          'skills': {
            'listening': 3,
            'gramatica': 7,
            'comprension': 6,
            'vocabulario': 6,
            'escritura': 6,
          },
        }, {}).first,
        'listening',
      );
      expect(
        RutaBiblioteca.prioridades({
          'skills': {
            'listening': 7,
            'gramatica': 3,
            'comprension': 6,
            'vocabulario': 6,
            'escritura': 6,
          },
        }, {}).first,
        'gramatica',
      );
    },
  );
  test(
    'perfil elige lectura contextual y mantiene preguntas del mismo texto',
    () {
      final qs = RutaBiblioteca.seleccionar(
        banco: bank,
        nivel: 5,
        skill: 'comprension',
        sectores: ['salud'],
      );
      expect(qs.length, 2);
      expect(qs.every((q) => q.sectores.contains('salud')), isTrue);
      expect(qs.map((q) => q.pasajeId).toSet().length, 1);
    },
  );
  test('prioriza nuevos ejemplos frente a respuestas ya acertadas', () {
    final first = RutaBiblioteca.seleccionar(
      banco: bank,
      nivel: 5,
      skill: 'listening',
    ).first;
    final next = RutaBiblioteca.seleccionar(
      banco: bank,
      nivel: 5,
      skill: 'listening',
      practicas: {
        first.id: {'correcta': true},
      },
    ).first;
    expect(next.id, isNot(first.id));
  });
  test('práctica persiste sin sustituir diagnóstico', () {
    final s = ProgressState(
      diagnostico: const {'nivel': 5},
      practicas: const {
        'a': {'skill': 'listening', 'correcta': false},
      },
    );
    final restored = ProgressState.fromJson(s.toJson());
    expect(restored.practicas, s.practicas);
    expect(restored.diagnostico, s.diagnostico);
  });
  test('listening no modifica la dificultad de gramática', () {
    final d = Diagnostico(declarado: 6, banco: bank);
    d.actual = bank.firstWhere((q) => q.skill == 'listening' && q.nivel == 6);
    d.responder('wrong');
    d.responder('wrong');
    expect(d.nivelParaSkill('gramatica'), 6);
    expect(d.nivelParaSkill('listening'), 5);
  });
  test('equivalencias curriculares coherentes, sin C2 inferido', () {
    for (var n = 1; n <= 10; n++) {
      expect(
        cefrDe(n.toDouble()),
        ['A1', 'A2', 'B1', 'B2', 'C1'][(n - 1) ~/ 2],
      );
    }
  });
}
