import 'content/curriculum.dart';
import 'content/fundamentos.dart';
import 'models/models.dart';

/// Prueba de nivel adaptativa (posicionamiento), inspirada en el Cambridge
/// Placement Test y el Oxford Online Placement Test:
///  1. autoevaluación → nivel de arranque;
///  2. bloques de 3 preguntas del nivel actual: ≥2 aciertos sube, ≤1 baja;
///  3. termina cuando el nivel queda acotado (aprobó N y falló N+1), al tocar
///     los extremos dos veces, o tras `maxBloques`.
/// El resultado es el nivel más alto aprobado (mínimo 1).
class PruebaNivel {
  PruebaNivel({required this.nivelInicio, this.preguntasPorBloque = 3, this.maxBloques = 8, List<LessonStep> Function(int nivel)? banco})
      : nivel = nivelInicio,
        _banco = banco ?? bancoNivel;

  final int nivelInicio;
  final int preguntasPorBloque;
  final int maxBloques;
  final List<LessonStep> Function(int nivel) _banco;

  int nivel;
  int maxAprobado = -1;
  int minReprobado = 11;
  int bloques = 0;
  final respuestas = <({int nivel, bool correcta})>[];
  final _usadas = <String>{};
  List<LessonStep> _bloque = [];
  int _idx = 0;
  int _aciertosBloque = 0;
  bool terminada = false;

  /// Autoevaluación → nivel de arranque.
  static int nivelDesdeAutoevaluacion(int opcion) => switch (opcion) {
        0 => 0, // Nunca lo he estudiado → empieza por Fundamentos (letras, sonidos, números)
        1 => 2, // Sé lo básico
        2 => 4, // Me defiendo en situaciones sencillas
        3 => 6, // Converso con soltura
        _ => 8, // Nivel avanzado
      };

  /// Banco de preguntas de un nivel: primero las del examen generado, luego los
  /// ejercicios de opción de las lecciones.
  static List<LessonStep> bancoNivel(int n) {
    if (n == 0) {
      final b = Fundamentos.banco(idiomaContenido);
      // Sin fundamentos para este idioma: se usa el nivel 1 como suelo.
      return b.isEmpty ? bancoNivel(1) : b;
    }
    final out = <LessonStep>[];
    for (final u in unidadesDe(n)) {
      for (final q in u.examen) {
        if (q.$2.length >= 2 && q.$3 >= 0 && q.$3 < q.$2.length) {
          out.add(LessonStep(type: StepType.multipleChoice, skill: Skill.gramatica, prompt: q.$1, answer: q.$2[q.$3], options: [...q.$2]..shuffle(), hint: 'N$n'));
        }
      }
    }
    for (final l in leccionesDe(n)) {
      for (final s in l.steps) {
        if ((s.type == StepType.multipleChoice || s.type == StepType.fillBlank) && s.options.length >= 3) {
          // Las opciones de las lecciones llevan la correcta en primer lugar: se barajan.
          out.add(LessonStep(type: s.type, skill: s.skill, prompt: s.prompt, answer: s.answer, options: [...s.options]..shuffle(), translation: s.translation, hint: s.hint));
        }
      }
    }
    return out..shuffle();
  }

  int get totalRespondidas => respuestas.length;
  int get preguntasEstimadas => preguntasPorBloque * maxBloques;

  LessonStep? get actual {
    if (terminada) return null;
    if (_idx >= _bloque.length) _nuevoBloque();
    return _bloque.isEmpty ? null : _bloque[_idx];
  }

  void _nuevoBloque() {
    final candidatas = _banco(nivel).where((s) => !_usadas.contains('${s.prompt}|${s.answer}')).take(preguntasPorBloque).toList();
    _bloque = candidatas;
    _idx = 0;
    _aciertosBloque = 0;
    for (final s in candidatas) {
      _usadas.add('${s.prompt}|${s.answer}');
    }
    if (candidatas.isEmpty) {
      terminada = true;
    }
  }

  /// Registra la respuesta a la pregunta actual y avanza. Devuelve si fue correcta.
  bool responder(String opcion) {
    final s = actual;
    if (s == null) return false;
    final ok = opcion == s.answer;
    respuestas.add((nivel: nivel, correcta: ok));
    if (ok) _aciertosBloque++;
    _idx++;
    if (_idx >= _bloque.length) _cerrarBloque();
    return ok;
  }

  void _cerrarBloque() {
    bloques++;
    final aprobado = _aciertosBloque * 2 >= _bloque.length; // ≥ 2 de 3
    if (aprobado) {
      if (nivel > maxAprobado) maxAprobado = nivel;
    } else {
      if (nivel < minReprobado) minReprobado = nivel;
    }
    // Acotado: aprobó N y falló N+1 (o falló el 1, o aprobó el 10).
    if (minReprobado == maxAprobado + 1 || (maxAprobado == 10) || (minReprobado == 0) || bloques >= maxBloques) {
      terminada = true;
      return;
    }
    // Siguiente nivel: sube si aprobó, baja si falló; mientras no haya cota en ese
    // sentido salta de dos en dos (como una búsqueda binaria) para acabar antes.
    final salto = aprobado ? (minReprobado == 11 ? 2 : 1) : (maxAprobado == -1 ? 2 : 1);
    var siguiente = aprobado ? nivel + salto : nivel - salto;
    if (siguiente >= minReprobado) siguiente = minReprobado - 1;
    if (siguiente <= maxAprobado) siguiente = maxAprobado + 1;
    nivel = siguiente.clamp(0, 10);
    if (nivel <= maxAprobado || nivel >= minReprobado) terminada = true;
  }

  /// Nivel recomendado: el más alto aprobado. 0 = empezar por Fundamentos
  /// (letras, sonidos, números); si no aprobó ninguno, también 0.
  int get resultado => maxAprobado.clamp(0, 10);

  double get precision => respuestas.isEmpty ? 0 : respuestas.where((r) => r.correcta).length / respuestas.length;
}
