import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/content/curriculum.dart';
import 'package:onelingo/core/models/models.dart';
import 'package:onelingo/core/state/providers.dart';

void main() {
  test('cada nivel tiene 100 lecciones y 20 unidades', () {
    for (var n = 1; n <= 10; n++) {
      expect(unidadesDe(n).length, 20);
      expect(leccionesDe(n).length, Level.totalLecciones);
      expect(leccionesDe(n).every((l) => l.steps.isNotEmpty), isTrue);
    }
  });

  test('desbloqueo progresivo: solo la lección 1 empieza desbloqueada', () {
    const s = ProgressState(onboardingDone: true);
    final lecciones = leccionesDe(1);
    expect(s.estadoLeccion(lecciones[0]), LessonState.actual);
    expect(s.estadoLeccion(lecciones[1]), LessonState.bloqueada);
    expect(s.nivelDesbloqueado(2), isFalse);
    expect(s.examenDesbloqueado(1), isFalse);
  });

  test('examen: 65 % aprueba y desbloquea el siguiente nivel', () {
    final todas = leccionesDe(1).map((l) => l.id).toSet();
    final s = ProgressState(onboardingDone: true, completadas: todas, examenes: const {1: 65});
    expect(s.examenDesbloqueado(1), isTrue);
    expect(s.examenAprobado(1), isTrue);
    expect(s.nivelDesbloqueado(2), isTrue);
    expect(s.nivelActual, 2);
    final reprobado = s.copyWith(examenes: const {1: 64});
    expect(reprobado.nivelDesbloqueado(2), isFalse);
  });
}
