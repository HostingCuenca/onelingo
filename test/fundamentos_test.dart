import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/content/contenido_json.dart';
import 'package:onelingo/core/content/curriculum.dart';
import 'package:onelingo/core/content/fundamentos.dart';
import 'package:onelingo/core/models/models.dart';
import 'package:onelingo/core/placement.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('el nivel 0 (Fundamentos) existe en los 10 idiomas y genera lecciones cortas', () async {
    for (final idm in ['en', 'es', 'fr', 'de', 'pt', 'it', 'zh', 'ja', 'ko', 'ru']) {
      await ContenidoJson.precargar(idm);
      idiomaContenido = idm;
      expect(Fundamentos.unidades(idm).length, 8, reason: idm);
      final lecciones = leccionesDe(0);
      expect(lecciones.length, greaterThanOrEqualTo(24), reason: idm);
      expect(totalLeccionesDe(0), lecciones.length);
      for (final l in lecciones) {
        expect(l.steps.length, inInclusiveRange(4, 14), reason: '${l.id} ${l.titulo}');
        for (final s in l.steps) {
          if (s.type == StepType.multipleChoice) {
            expect(s.options.length, greaterThanOrEqualTo(3), reason: '${l.id}: ${s.prompt}');
            expect(s.options, contains(s.answer));
          }
        }
      }
      expect(unidadesDe(0).first.examen.length, greaterThanOrEqualTo(2));
      expect(PruebaNivel.bancoNivel(0).length, greaterThanOrEqualTo(20), reason: idm);
    }
    idiomaContenido = 'en';
  });

  test('el japonés empieza por hiragana y el coreano por hangul', () async {
    await ContenidoJson.precargar('ja');
    await ContenidoJson.precargar('ko');
    expect(Fundamentos.unidades('ja').first.items.first.simbolo, 'あ');
    expect(Fundamentos.unidades('ko').first.items.first.simbolo, 'ㄱ');
    expect(Fundamentos.unidades('ko').first.esEscritura, isTrue);
    idiomaContenido = 'ja';
    expect(leccionesDe(0).first.titulo, startsWith('Descubre'));
    idiomaContenido = 'en';
  });
}
