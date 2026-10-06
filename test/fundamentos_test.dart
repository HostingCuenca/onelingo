import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/integridad.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/aprendizaje/providers.dart' show idiomasConRuta;
import 'package:onelingo/core/content/contenido_json.dart';
import 'package:onelingo/core/content/curriculum.dart';
import 'package:onelingo/core/content/fundamentos.dart';
import 'package:onelingo/core/models/models.dart';
import 'package:onelingo/core/placement.dart';
import 'package:onelingo/core/state/providers.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('el nivel 0 (Fundamentos) existe en los idiomas con contenido antiguo y genera lecciones cortas', () async {
    // El portugués se reinició desde cero (DEC-035): su Fundamentos es solo la ruta f0.
    for (final idm in ['en', 'es', 'fr', 'de', 'it', 'zh', 'ja', 'ko', 'ru']) {
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

  test('el portugués (en reconstrucción) tiene Fundamentos solo en la ruta f0: 8 unidades', () async {
    expect(idiomasSoloRutaF0, contains('pt'));
    await ContenidoJson.precargar('pt');
    expect(Fundamentos.disponible('pt'), isFalse); // sin nivel-0.json antiguo
    final ruta = await CargadorRuta().cargar('pt');
    expect(ruta, isNotNull);
    final f0 = ruta!.delNivel('f0');
    expect(f0, hasLength(8));
    expect(f0.first.id, 'pt.f0.primeiro-contato');
    expect(f0.last.id, 'pt.f0.apresentar-se');
    expect(problemasDeContenido(ruta), isEmpty);
    // Solo Fundamentos: aún sin niveles N publicados ni ruta por niveles.
    expect(ruta.curso.niveles.where((n) => n.estado == EstadoNivel.publicado).map((n) => n.id), ['f0']);
    expect(idiomasConRuta, isNot(contains('pt')));
    const s = ProgressState(idiomaMeta: 'pt', fundamentos: true);
    expect(s.fundamentosPendientes, isTrue);
    expect(s.nivel0Pendiente, isTrue);
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
