import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/content/grammar_guides.dart';

void main() {
  test('Los diez niveles conservan enseñanza y evaluación independientes', () {
    expect(grammarGuides.map((g) => g.id).toSet().length, grammarGuides.length);
    for (var level = 1; level <= 10; level++) {
      final guides = grammarForLevel(level);
      expect(guides.length, greaterThanOrEqualTo(2));
      for (final guide in guides) {
        expect(guide.rule, isNotEmpty);
        expect(guide.goal, isNotEmpty);
        expect(guide.commonError, isNotEmpty);
        expect(guide.examples, isNotEmpty);
        expect(guide.checks.length, greaterThanOrEqualTo(2));
        for (final q in guide.checks) {
          expect(q.answer, inInclusiveRange(0, q.options.length - 1));
          expect(q.options.toSet().length, q.options.length);
          expect(q.feedback, isNotEmpty);
          expect(q.prompt, isNotEmpty);
        }
      }
    }
    expect(grammarForLevel(0), isEmpty);
    expect(grammarForLevel(11), isEmpty);
  });
}
