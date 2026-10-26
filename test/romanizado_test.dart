import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/correccion.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/aprendizaje/romanizado.dart';

/// Respuestas escritas en letras latinas en ru, ja, ko y zh.
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final rutas = <String, RutaCargada>{};

  setUpAll(() async {
    final cargador = CargadorRuta();
    for (final idioma in LexicoRom.idiomas) {
      rutas[idioma] = (await cargador.cargar(idioma))!;
    }
  });

  bool acepta(String idioma, String valida, String dada) =>
      aceptaRomanizada(idioma, [valida], dada);

  test('ruso: transliteración con variantes habituales', () {
    expect(acepta('ru', 'Привет!', 'privet'), isTrue);
    expect(acepta('ru', 'Здравствуйте.', 'Zdravstvuyte'), isTrue);
    expect(acepta('ru', 'Здравствуйте.', 'zdravstvujte'), isTrue);
    expect(acepta('ru', 'Спасибо', 'spasíbo'), isTrue);
    expect(acepta('ru', 'хорошо', 'horosho'), isTrue);
    expect(acepta('ru', 'Привет!', 'poka'), isFalse);
  });

  test('coreano: Romanización Revisada con los cambios fonéticos', () {
    expect(acepta('ko', '감사합니다', 'gamsahamnida'), isTrue);
    expect(acepta('ko', '안녕하세요', 'annyeonghaseyo'), isTrue);
    expect(acepta('ko', '한국어', 'hangugeo'), isTrue);
    expect(acepta('ko', '저는 학생이에요.', 'jeoneun haksaengieyo'), isTrue);
    expect(acepta('ko', '감사합니다', 'saranghaeyo'), isFalse);
  });

  test('japonés: kana y palabras del curso', () {
    expect(acepta('ja', 'わたし は がくせい です。', 'watashi wa gakusei desu'), isTrue);
    expect(acepta('ja', 'わたしはがくせいです', 'Watashi wa gakusei desu.'), isTrue);
    expect(acepta('ja', 'ありがとう', 'arigatou'), isTrue);
    expect(acepta('ja', 'ありがとう', 'arigatō'), isTrue);
    expect(acepta('ja', 'コーヒー', 'koohii'), isTrue);
    expect(acepta('ja', '学生', 'gakusei'), isTrue);
    expect(acepta('ja', 'わたし は がくせい です。', 'watashi wa sensei desu'), isFalse);
  });

  test('chino: pinyin con o sin tonos', () {
    expect(acepta('zh', '我 是 学生。', 'wo shi xuesheng'), isTrue);
    expect(acepta('zh', '我是学生', 'wǒ shì xuésheng'), isTrue);
    expect(acepta('zh', '你 好！', 'ni hao'), isTrue);
    expect(acepta('zh', '我 是 学生。', 'wo shi laoshi'), isFalse);
  });

  test('en la escritura del idioma sigue la corrección de siempre', () {
    expect(acepta('ru', 'Привет!', 'Привет'), isFalse);
    expect(acepta('fr', 'Bonjour', 'bonjour'), isFalse);
    expect(mismaRespuesta('privet', 'привет', 'ru'), isTrue);
  });

  test('casi todas las respuestas escritas tienen forma latina', () {
    for (final idioma in LexicoRom.idiomas) {
      var total = 0, con = 0;
      final lexico = LexicoRom.de(idioma)!;
      for (final u in rutas[idioma]!.unidades) {
        // Hasta N4 el curso da la romanización de los ejercicios.
        if ((u.nivelInterno ?? 0) > 4) continue;
        for (final p in u.pasos) {
          for (final it in p.items) {
            final r = it.respuesta;
            final escrita = it.formato == FormatoItem.escribir ||
                (it.formato == FormatoItem.completar && it.opciones.isEmpty);
            if (!escrita || r == null || !tieneEscritura(r, idioma)) continue;
            total++;
            if (lexico.formas(r).isNotEmpty) con++;
          }
        }
      }
      final cobertura = con / total;
      // ignore: avoid_print
      print('$idioma: $con/$total respuestas con forma latina');
      expect(cobertura, greaterThan(0.9), reason: idioma);
    }
  });
}
