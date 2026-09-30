import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/biblioteca_modelos.dart';
import 'package:onelingo/core/aprendizaje/biblioteca_selector.dart';

void main() {
  Map<String, dynamic> fixture() => {
    'schema': 'exercise-library/1',
    'libraryId': 'onelingo',
    'version': '1',
    'course': 'en',
    'units': {
      'u': {
        'concepts': ['c'],
        'skills': ['vocabulario'],
        'prerequisites': [],
        'pools': {
          'practice': ['ex.onelingo.en.c.a:v1:practice'],
          'review': ['ex.onelingo.en.c.r:v1:review'],
        },
      },
    },
    'families': [
      {
        'id': 'ex.onelingo.en.c.a',
        'revision': 1,
        'concepts': ['c'],
        'skills': ['vocabulario'],
        'variants': [
          {
            'id': 'ex.onelingo.en.c.a:v1:practice',
            'format': 'elegir',
            'prompt': {'es': 'x'},
            'answer': {'index': 0},
            'choices': [
              {'text': 'x'},
            ],
            'teaches': [],
            'requires': [],
            'origin': {'kind': 'editorial'},
            'contentHash': 'sha256:a',
          },
        ],
      },
      {
        'id': 'ex.onelingo.en.c.r',
        'revision': 1,
        'concepts': ['c'],
        'skills': ['vocabulario'],
        'variants': [
          {
            'id': 'ex.onelingo.en.c.r:v1:review',
            'format': 'elegir',
            'prompt': {'es': 'y'},
            'answer': {'index': 0},
            'choices': [
              {'text': 'y'},
            ],
            'teaches': [],
            'requires': [],
            'origin': {'kind': 'editorial'},
            'contentHash': 'sha256:b',
          },
        ],
      },
    ],
  };
  test('parsea y valida', () {
    final l = ExerciseLibrary.fromJson(fixture());
    expect(validateExerciseLibrary(l), isEmpty);
  });
  test('selección estable y exclusión', () {
    final l = ExerciseLibrary.fromJson(fixture());
    final a = selectExercises(l, unitId: 'u', pool: 'practice', seed: 4);
    final b = selectExercises(l, unitId: 'u', pool: 'practice', seed: 4);
    expect(a.selectionId, b.selectionId);
    expect(
      selectExercises(
        l,
        unitId: 'u',
        pool: 'practice',
        seed: 4,
        excludedFamilies: {'ex.onelingo.en.c.a'},
      ).variants,
      isEmpty,
    );
  });

  test('rechaza referencias y revisiones inconsistentes', () {
    final data = fixture();
    final units = data['units'] as Map<String, dynamic>;
    final unit = units['u'] as Map<String, dynamic>;
    final pools = unit['pools'] as Map<String, dynamic>;
    pools['evaluation'] = ['ex.onelingo.en.c.unknown:v1:assessment'];
    final families = data['families'] as List<dynamic>;
    final family = families.first as Map<String, dynamic>;
    family['revision'] = 2;

    final errors = validateExerciseLibrary(ExerciseLibrary.fromJson(data));
    expect(errors, anyElement(contains('unknown variant')));
    expect(errors, anyElement(contains('variant revision mismatch')));
  });
}
