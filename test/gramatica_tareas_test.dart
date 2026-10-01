import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/content/grammar_guides.dart';
import 'package:onelingo/core/content/grammar_production_tasks.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'Cada tema enseñado tiene una tarea de producción sin clave prefijada',
    () {
      expect(grammarGuides.length, 43);
      expect(
        grammarProductionTasks.keys.toSet(),
        grammarGuides.map((g) => g.id).toSet(),
      );
      expect(grammarGuides.expand((g) => g.checks).length, 86);
      final passive = grammarGuides.indexWhere((g) => g.id == 'passive-basic');
      // La regla básica se enseña antes del resultado perfecto, no por rareza.
      expect(passive, greaterThanOrEqualTo(0));
      expect(
        passive,
        lessThan(grammarGuides.indexWhere((g) => g.id == 'passive')),
      );
    },
  );
}
