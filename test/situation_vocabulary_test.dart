import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/content/situation_units.dart';
import 'package:onelingo/core/content/grammar_guides.dart';
import 'package:onelingo/core/content/grammar_production_tasks.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'Situaciones cargan enseñanza contextual y conservan palabras originales',
    () async {
      final container = ProviderContainer();
      addTearDown(container.dispose);
      final units = await container.read(situationUnitsProvider.future);
      expect(units.length, 50);
      expect(units.expand((u) => u.words).length, 550);
      for (final unit in units) {
        expect(unit.words.length, 11);
        expect(unit.words.map((w) => w.$1.toLowerCase()).toSet().length, 11);
        expect(unit.vocabulary.length, 8);
        expect(unit.patterns, isNotEmpty);
        for (final word in unit.vocabulary) {
          expect(word.example, isNotEmpty);
          expect(word.level, inInclusiveRange(1, 10));
        }
        for (final pattern in unit.patterns) {
          expect(pattern.examples.length, greaterThanOrEqualTo(2));
          expect(
            pattern.examples.map((e) => e.$1).toSet().length,
            pattern.examples.length,
          );
          expect(pattern.template, contains('{'));
        }
      }
      final restaurant = units.firstWhere((u) => u.id == 1);
      expect(restaurant.words.any((w) => w.$1 == 'menu'), isTrue);
      expect(restaurant.vocabulary.any((w) => w.en == 'without nuts'), isTrue);
      expect(
        restaurant.patterns.first.examples.first.$1,
        contains('without cream'),
      );
    },
  );
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
