import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/barajar.dart';

void main() {
  test('barajarDistinto nunca devuelve el orden original', () {
    const frase = ['I', 'have', 'been', 'waiting', 'for', 'you'];
    for (var semilla = 0; semilla < 500; semilla++) {
      final r = barajarDistinto(frase, Random(semilla));
      expect(r, isNot(orderedEquals(frase)));
      expect(r.toSet(), frase.toSet());
    }
    expect(barajarDistinto(['a', 'b'], Random(1)), ['b', 'a']);
    expect(barajarDistinto(['x']), ['x']);
  });
}
