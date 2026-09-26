import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/voz.dart';

void main() {
  group('Coincidencia de transcripción, no pronunciación', () {
    test('normaliza puntuación, mayúsculas y espacios', () {
      expect(similitud('  HELLO,   Mia! ', 'Hello Mia'), 1);
    });
    test('normaliza contracciones no ambiguas y apóstrofo tipográfico', () {
      expect(similitud('I’m ready and I’ll help.', 'I am ready and I will help'), 1);
      expect(similitud("We haven't finished", 'We have not finished'), 1);
      expect(similitud("I can't go", 'I cannot go'), 1);
      expect(similitud("They won't leave", 'They will not leave'), 1);
    });
    test('negación añadida no aprueba aunque casi todo coincida', () {
      expect(similitud('I do not like coffee', 'I like coffee'), lessThan(.6));
      expect(similitud('I will not send the finished report before lunch today',
          'I will send the finished report before lunch today'), lessThan(.6));
    });
    test('negación omitida o contraída no aprueba', () {
      expect(similitud('I can join the meeting tomorrow',
          "I can't join the meeting tomorrow"), lessThan(.6));
      expect(similitud('I have visited London before',
          'I have never visited London before'), lessThan(.6));
    });
    test('mismas palabras reordenadas no equivalen a la frase', () {
      expect(similitud('The dog chased the cat', 'The cat chased the dog'), lessThan(.6));
      expect(similitud('You can help me with the report after lunch',
          'Can you help me with the report after lunch'), lessThan(.6));
    });
    test('cuenta palabras extra y repeticiones, no solo pertenencia', () {
      expect(similitud('Go go', 'Go'), lessThan(1));
      expect(similitud('Please bring the blue book and the red bag',
          'Please bring the blue book'), lessThan(1));
    });
    test('preserva orden en escritura sin espacios', () {
      expect(similitud('我爱你', '你爱我'), lessThan(.6));
      expect(similitud('你好', '你好'), 1);
    });
    test('no inventa expansión de contracción ambigua', () {
      expect(similitud("He'd finished", 'He had finished'), lessThan(1));
    });
    test('vacíos y texto diferente no producen acierto', () {
      expect(similitud('', 'Hello'), 0);
      expect(similitud('...', 'Hello'), 0);
      expect(similitud('Good night', 'Blue car'), 0);
    });
  });
}
