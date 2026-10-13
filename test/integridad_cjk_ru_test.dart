import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/integridad.dart';

/// «Palabra conocida» en ruso, coreano, japonés y chino: espejo de
/// `conocida_ru`, `conocida_ko` y `conocida_cjk` en tools/validar_ruta.py
/// (pruebas Python: tools/test_conocida_cjk.py).
void main() {
  /// Lo que enseñan unos vocablos (`texto`), como lo arma la integridad.
  Set<String> saber(List<String> textos) => {
    for (final t in textos) ...palabrasMeta(t),
  };

  /// Palabras de [texto] que no cuentan como enseñadas en [idioma].
  List<String> faltan(String idioma, String texto, Set<String> conocidas) {
    final prueba = palabraConocidaPara(idioma);
    return palabrasMeta(texto).where((w) => !prueba(w, conocidas)).toList();
  }

  group('japonés', () {
    test('conocida', () {
      final s = saber(['わたし', 'は', 'がくせい', 'です']);
      expect(faltan('ja', 'わたし は がくせい です。', s), isEmpty);
    });
    test('una partícula suelta también debe enseñarse', () {
      final s = saber(['わたし', 'がくせい', 'です']);
      expect(faltan('ja', 'わたし は がくせい です。', s), ['は']);
    });
    test('sin espacios no se inventa segmentación', () {
      final s = saber(['わたし', 'は', 'がくせい', 'です']);
      expect(faltan('ja', 'わたしはがくせいです。', s), ['わたしはがくせいです']);
    });
    test('puntuación de ancho completo', () {
      expect(palabrasMeta('「すみません」、『にほん』・マリア（メキシコ）です か？！'), [
        'すみません', 'にほん', 'マリア', 'メキシコ', 'です', 'か', //
      ]);
    });
    test('vocablo con lectura entre paréntesis', () {
      final s = saber(['日本 (にほん)', '何 (なに, なん)']);
      expect(s.containsAll({'日本', 'にほん', '何', 'なに', 'なん'}), isTrue);
      expect(faltan('ja', 'にほん', s), isEmpty);
    });
  });

  group('chino', () {
    test('conocida', () {
      expect(faltan('zh', '我 是 学生。', saber(['我', '是', '学生'])), isEmpty);
    });
    test('no conocida', () {
      expect(faltan('zh', '我 是 老师。', saber(['我', '是'])), ['老师']);
    });
    test('partícula suelta', () {
      expect(faltan('zh', '你 好 吗？', saber(['你', '好'])), ['吗']);
    });
    test('puntuación', () {
      expect(palabrasMeta('书、茶，“水”：（好）；对！'), ['书', '茶', '水', '好', '对']);
      expect(faltan('zh', '书、茶。', saber(['书', '茶'])), isEmpty);
    });
  });

  group('coreano', () {
    final s = saber([
      '저', '학생', '은', '는', '이에요', '서울', '에', '에서', '자다 (자요)', //
    ]);
    test('eojeol tal cual y forma entre paréntesis', () {
      expect(faltan('ko', '자요.', s), isEmpty);
      expect(faltan('ko', '자다', s), isEmpty);
    });
    test('partícula pegada enseñada', () {
      expect(faltan('ko', '저는 학생이에요.', s), isEmpty);
      expect(faltan('ko', '서울에서 자요?', s), isEmpty);
      expect(faltan('ko', '서울에는', s), isEmpty);
    });
    test('partícula no enseñada', () {
      expect(faltan('ko', '학생을 서울에도', s), ['학생을', '서울에도']);
    });
    test('raíz o conjugación no enseñadas', () {
      expect(faltan('ko', '의사는 먹어요.', s), ['의사는', '먹어요']);
      expect(faltan('ko', '잤어요', s), ['잤어요']);
    });
    test('dos partículas de caso seguidas no cuentan', () {
      expect(faltan('ko', '학생이가', {...s, '이', '가'}), ['학생이가']);
    });
    test('puntuación', () {
      expect(palabrasMeta('«저는 학생이에요?»'), ['저는', '학생이에요']);
    });
    test('números sinocoreanos compuestos de dígitos enseñados', () {
      final n = saber(['일', '이', '삼', '오', '공', '십', '천', '만']);
      for (final w in ['이십', '십일', '삼천', '십만', '삼십오만', '공일공']) {
        expect(faltan('ko', w, n), isEmpty, reason: w);
      }
      // Dos dígitos seguidos sin multiplicador (오삼) no son un número; a 이백 le falta 백.
      expect(faltan('ko', '오삼', n), ['오삼']);
      expect(faltan('ko', '이백', n), ['이백']);
    });
  });

  group('ruso', () {
    test('conocida', () {
      final s = saber(['я', 'читать — прочитать', 'книга']);
      expect(faltan('ru', 'Я читать книга.', s), isEmpty);
    });
    test('la flexión solo cuenta si se enseñó', () {
      expect(
        faltan('ru', 'читаю книгу', saber(['читать — прочитать', 'книга'])),
        ['читаю', 'книгу'],
      );
      expect(
        faltan('ru', 'читаю книгу', saber(['читать (читаю)', 'книга (книгу)'])),
        isEmpty,
      );
    });
    test('ё ≡ е y sin acento U+0301', () {
      expect(faltan('ru', 'Еще все.', saber(['ещё', 'всё'])), isEmpty);
      expect(faltan('ru', 'Ещё ещ́е', saber(['еще'])), isEmpty);
    });
    test('puntuación y guiones', () {
      final s = saber(['по-русски', 'анна', 'врач']);
      expect(faltan('ru', 'Анна — врач! «По-русски»?', s), isEmpty);
      expect(faltan('ru', 'Анна — доктор.', s), ['доктор']);
    });
    test('N3: varias formas entre paréntesis y preposición con guion', () {
      final s = saber([
        'я', 'повесить (повесил)', 'куртка (куртку)', //
        'вешалка (на вешалку, на вешалке)', 'из-за', 'дождь (из-за дождя)',
      ]);
      expect(faltan('ru', 'Я повесил куртку на вешалку.', s), isEmpty);
      expect(faltan('ru', 'Куртка на вешалке? Из-за дождя!', s), isEmpty);
      // Un caso no enseñado no se deduce de los otros.
      expect(faltan('ru', 'под вешалкой', s), ['под', 'вешалкой']);
    });
    test('N4: paréntesis con «;» y «:» (régimen y formas del verbo)', () {
      final s = saber([
        'я', 'и', //
        'коллектив (коллектива; руководить коллективом: руковожу, руководите)',
        'заведовать (заведую, заведовал, заведовала; склад: склада, складом)',
        'вничью (закончился вничью)', 'матч',
      ]);
      expect(faltan('ru', 'Я руковожу коллективом и заведую складом.', s), isEmpty);
      expect(faltan('ru', 'Матч закончился вничью!', s), isEmpty);
      // Ni la forma no enseñada ni el caso que falta se deducen.
      expect(faltan('ru', 'Он руководит складом.', s), ['он', 'руководит']);
    });
  });

  test('sin morfología inglesa fuera del inglés', () {
    expect(palabraConocidaPara('ru')('книгаs', {'книга'}), isFalse);
    expect(palabraConocidaPara('zh')('学生s', {'学生'}), isFalse);
    expect(palabraConocidaPara('en')('books', {'book'}), isTrue);
  });
}
