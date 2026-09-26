import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/core/content/curriculum.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  Future<ProgressNotifier> load([
    ProgressState state = const ProgressState(),
  ]) async {
    SharedPreferences.setMockInitialValues({
      'onelingo.progress.v1': jsonEncode(state.toJson()),
    });
    return ProgressNotifier(await SharedPreferences.getInstance());
  }

  test(
    'racha usa días civiles, caduca sin actividad y no modifica historial',
    () {
      const s = ProgressState(racha: 5, ultimoDia: '2026-09-19');
      expect(s.rachaEn(DateTime(2026, 9, 19)), 5);
      expect(s.rachaEn(DateTime(2026, 9, 20, 23)), 5);
      expect(s.rachaEn(DateTime(2026, 9, 21)), 0);
      expect(s.rachaEn(DateTime(2026, 9, 18)), 0);
      expect(s.racha, 5);
    },
  );

  test('migración sólo conoce último día, no inventa semana', () {
    final s = ProgressState.fromJson({'racha': 30, 'ultimoDia': '2026-09-19'});
    expect(s.diasActividad, {'2026-09-19'});
    expect(ProgressState.fromJson(s.toJson()).diasActividad, s.diasActividad);
  });

  test('repasos no revocan examen aprobado ni multiplican XP', () async {
    final p = await load();
    p.registrarExamen(1, 30);
    expect(p.state.xp, 20);
    p.registrarExamen(1, 40);
    expect(p.state.xp, 20);
    p.registrarExamen(1, 80);
    expect(p.state.xp, 220);
    p.registrarExamen(1, 10);
    expect(p.state.examenes[1], 80);
    expect(p.state.nivelDesbloqueado(2), isTrue);
    p.registrarExamen(1, 100);
    expect(p.state.examenes[1], 100);
    expect(p.state.xp, 220);
    expect(p.state.diasActividad.length, 1);
    expect(p.state.rachaVigente, 1);
    p.dispose();
  });

  test(
    'repetir lección conserva mejor puntuación y XP de primera actividad',
    () async {
      final p = await load();
      final lesson = leccionesDe(1).first;
      p.completarLeccion(lesson, aciertos: 4, total: 5);
      final xp = p.state.xp;
      p.completarLeccion(lesson, aciertos: 1, total: 5);
      expect(p.state.puntuaciones[lesson.id], 80);
      expect(p.state.xp, xp);
      p.completarLeccion(lesson, aciertos: 5, total: 5);
      expect(p.state.puntuaciones[lesson.id], 100);
      expect(p.state.xp, xp);
      expect(p.state.completadas, {lesson.id});
      p.dispose();
    },
  );

  test(
    'primera respuesta sobrevive repeticiones, recarga y alias habilidad',
    () async {
      final p = await load();
      p.registrarPractica('q1', {'habilidad': 'gramatica', 'correcta': false});
      final firstDate = (p.state.practicas['q1'] as Map)['primeraFecha'];
      p.registrarPractica('q1', {'skill': 'gramatica', 'correcta': true});
      final restored = ProgressState.fromJson(p.state.toJson());
      final q = restored.practicas['q1'] as Map;
      expect(q['skill'], 'gramatica');
      expect(q['primeraCorrecta'], false);
      expect(q['primeraFecha'], firstDate);
      expect(q['correcta'], true);
      expect(q['intentos'], 2);
      expect(restored.xp, 5);
      p.dispose();
    },
  );

  test(
    'no inventa primera respuesta en registros antiguos ya repetidos',
    () async {
      final p = await load(
        const ProgressState(
          practicas: {
            'q': {'correcta': true, 'intentos': 3, 'fecha': '2026-09-01'},
          },
        ),
      );
      p.registrarPractica('q', {'skill': 'gramatica', 'correcta': false});
      expect(
        (p.state.practicas['q'] as Map).containsKey('primeraCorrecta'),
        false,
      );
      expect(p.state.xp, 0);
      p.dispose();
    },
  );
}
