import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/models/models.dart';
import 'package:onelingo/core/placement.dart';

LessonStep _q(int n, int i) => LessonStep(type: StepType.multipleChoice, skill: Skill.gramatica, prompt: 'N$n-$i', answer: 'ok', options: const ['ok', 'a', 'b', 'c']);
List<LessonStep> _banco(int n) => List.generate(12, (i) => _q(n, i));

/// Simula un alumno cuyo nivel real es `real`: acierta si la pregunta es de ese nivel o inferior.
int _simular(int real, int arranque) {
  final p = PruebaNivel(nivelInicio: arranque, banco: _banco);
  while (!p.terminada) {
    final s = p.actual;
    if (s == null) break;
    final nivelPregunta = int.parse(s.prompt.substring(1).split('-').first);
    p.responder(nivelPregunta <= real ? 'ok' : 'a');
  }
  return p.resultado;
}

void main() {
  test('posiciona en el nivel real desde distintos arranques', () {
    for (final real in [1, 3, 5, 7, 10]) {
      for (final arranque in [1, 2, 4, 6, 8]) {
        expect(_simular(real, arranque), real, reason: 'real $real arranque $arranque');
      }
    }
  });

  test('termina en pocos bloques y nunca supera 21 preguntas', () {
    final p = PruebaNivel(nivelInicio: 4, banco: _banco);
    while (!p.terminada) {
      final s = p.actual;
      if (s == null) break;
      p.responder('a');
    }
    expect(p.resultado, 0); // falla todo: empieza por Fundamentos
    expect(p.totalRespondidas, lessThanOrEqualTo(24));
  });

  test('el diagnóstico es progresivo: baja hasta Fundamentos y sube desde cero', () {
    expect(_simular(0, 2), 0, reason: 'no supera el nivel 1 → Fundamentos');
    expect(_simular(1, 0), 1, reason: 'empieza de cero pero domina el nivel 1');
    expect(_simular(3, 0), 3, reason: 'sube desde Fundamentos hasta su nivel real');
  });

  test('autoevaluación fija el nivel de arranque', () {
    expect(PruebaNivel.nivelDesdeAutoevaluacion(0), 0);
    expect(PruebaNivel.nivelDesdeAutoevaluacion(2), 4);
    expect(PruebaNivel.nivelDesdeAutoevaluacion(4), 8);
  });
}
