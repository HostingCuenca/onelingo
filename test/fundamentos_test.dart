import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/integridad.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart' show nivelPublicadoMaximo;
import 'package:onelingo/core/aprendizaje/providers.dart' show idiomasConRuta, nivelAlumnoEnRuta;
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
    for (final idm in ['en', 'es', 'fr', 'de']) {
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

  test('el portugués: Fundamentos solo en la ruta f0 (8 unidades) y N1–N10 encadenados tras ella', () async {
    expect(idiomasSoloRutaF0, contains('pt'));
    await ContenidoJson.precargar('pt');
    expect(Fundamentos.disponible('pt'), isFalse); // sin nivel-0.json antiguo
    final cargador = CargadorRuta();
    final ruta = await cargador.cargar('pt');
    expect(ruta, isNotNull);
    expect(cargador.modulosConError, isEmpty);
    final f0 = ruta!.delNivel('f0');
    expect(f0, hasLength(8));
    expect(f0.first.id, 'pt.f0.primeiro-contato');
    expect(f0.last.id, 'pt.f0.apresentar-se');
    expect(problemasDeContenido(ruta, formasVerbales: await cargador.formasVerbales('pt')), isEmpty);
    // Publicados solo los niveles que integró tools/contenido/ruta-pt/integrar.py:
    // f0 y luego N1, N2… consecutivos, cada uno con clases y encadenado al anterior.
    final publicados = [
      for (final n in ruta.curso.niveles)
        if (n.estado == EstadoNivel.publicado) n.id,
    ];
    expect(publicados.first, 'f0');
    expect(publicados.skip(1), [for (var i = 1; i < publicados.length; i++) 'n$i']);
    expect(publicados, contains('n1'));
    var previa = f0.last.id;
    for (final nivel in publicados.skip(1)) {
      final clases = ruta.delNivel(nivel);
      expect(clases.length, greaterThanOrEqualTo(5), reason: nivel);
      for (final u in clases) {
        expect(u.id, startsWith('pt.$nivel.c'), reason: u.id);
        expect(u.prerequisitos, [previa], reason: u.id);
        previa = u.id;
      }
    }
    // Curso completo publicado: f0 y N1–N10, con la ruta por niveles activa.
    expect(publicados, ['f0', for (var i = 1; i <= 10; i++) 'n$i']);
    expect(idiomasConRuta, contains('pt'));
    const s = ProgressState(idiomaMeta: 'pt', fundamentos: true);
    expect(s.fundamentosPendientes, isTrue);
    expect(s.nivel0Pendiente, isTrue);
  });

  test('el alemán: ruta f0 (8 unidades) y N1–N10 encadenados tras ella, sin el a1-1 heredado', () async {
    final cargador = CargadorRuta();
    final ruta = await cargador.cargar('de');
    expect(ruta, isNotNull);
    expect(cargador.modulosConError, isEmpty);
    final f0 = ruta!.delNivel('f0');
    expect(f0, hasLength(8));
    expect(f0.first.id, 'de.f0.laute-gruesse');
    expect(f0.last.id, 'de.f0.vorstellen');
    expect(ruta.delNivel('a1-1'), isEmpty);
    expect(problemasDeContenido(ruta, formasVerbales: await cargador.formasVerbales('de')), isEmpty);
    final publicados = [
      for (final n in ruta.curso.niveles)
        if (n.estado == EstadoNivel.publicado) n.id,
    ];
    // Curso completo publicado (método ligero: 50 clases por nivel).
    expect(publicados, ['f0', for (var i = 1; i <= 10; i++) 'n$i']);
    var previa = f0.last.id;
    for (final nivel in publicados.skip(1)) {
      final clases = ruta.delNivel(nivel);
      expect(clases, hasLength(50), reason: nivel);
      for (final u in clases) {
        expect(u.id, startsWith('de.$nivel.c'), reason: u.id);
        expect(u.prerequisitos, [previa], reason: u.id);
        previa = u.id;
      }
    }
    expect(idiomasConRuta, contains('de'));
  });

  test('el italiano (versión esencial): ruta f0 (8 unidades) y solo N1–N6 publicados', () async {
    expect(idiomasSoloRutaF0, contains('it'));
    await ContenidoJson.precargar('it');
    expect(Fundamentos.disponible('it'), isFalse); // sin nivel-0.json antiguo
    final cargador = CargadorRuta();
    final ruta = await cargador.cargar('it');
    expect(ruta, isNotNull);
    expect(cargador.modulosConError, isEmpty);
    final f0 = ruta!.delNivel('f0');
    expect(f0, hasLength(8));
    expect(f0.first.id, 'it.f0.primo-contatto');
    expect(f0.last.id, 'it.f0.presentarsi');
    expect(ruta.delNivel('a1-1'), isEmpty);
    expect(ruta.curso.idiomasApoyo, ['es', 'en']);
    expect(problemasDeContenido(ruta, formasVerbales: await cargador.formasVerbales('it')), isEmpty);
    final publicados = [
      for (final n in ruta.curso.niveles)
        if (n.estado == EstadoNivel.publicado) n.id,
    ];
    // Versión esencial: N1–N6 (50 clases por nivel); N7–N10 aún no existen
    // en el curso, así que la app los muestra «Próximamente» y no se juegan.
    expect(publicados, ['f0', for (var i = 1; i <= 6; i++) 'n$i']);
    for (var i = 7; i <= 10; i++) {
      expect(ruta.delNivel('n$i'), isEmpty, reason: 'n$i');
    }
    expect(nivelPublicadoMaximo(ruta), 6);
    var previa = f0.last.id;
    for (final nivel in publicados.skip(1)) {
      final clases = ruta.delNivel(nivel);
      expect(clases, hasLength(50), reason: nivel);
      for (final u in clases) {
        expect(u.id, startsWith('it.$nivel.c'), reason: u.id);
        expect(u.prerequisitos, [previa], reason: u.id);
        previa = u.id;
      }
    }
    expect(idiomasConRuta, contains('it'));
    const s = ProgressState(idiomaMeta: 'it', fundamentos: true);
    expect(s.fundamentosPendientes, isTrue);
    expect(s.nivel0Pendiente, isTrue);
    // Un alumno ubicado más arriba (diagnóstico antiguo) se queda en N6.
    const alto = ProgressState(idiomaMeta: 'it', nivelInicial: 8);
    expect(nivelAlumnoEnRuta(ruta, alto), 6);
  });

  test('el chino (versión esencial): ruta f0 (8 unidades) y solo N1–N4 publicados', () async {
    expect(idiomasSoloRutaF0, contains('zh'));
    await ContenidoJson.precargar('zh');
    expect(Fundamentos.disponible('zh'), isFalse); // nunca tuvo nivel-0.json
    final cargador = CargadorRuta();
    final ruta = await cargador.cargar('zh');
    expect(ruta, isNotNull);
    expect(cargador.modulosConError, isEmpty);
    final f0 = ruta!.delNivel('f0');
    expect(f0, hasLength(8));
    expect(f0.first.id, 'zh.f0.nihao');
    expect(f0.last.id, 'zh.f0.zi-wo-jieshao');
    expect(ruta.delNivel('a1-1'), isEmpty);
    expect(ruta.curso.idiomasApoyo, ['es', 'en']);
    expect(problemasDeContenido(ruta, formasVerbales: await cargador.formasVerbales('zh')), isEmpty);
    final publicados = [
      for (final n in ruta.curso.niveles)
        if (n.estado == EstadoNivel.publicado) n.id,
    ];
    // Versión esencial: N1–N4 (50 clases por nivel); N5–N10 aún no existen
    // en el curso, así que la app los muestra «Próximamente» y no se juegan.
    expect(publicados, ['f0', 'n1', 'n2', 'n3', 'n4']);
    for (var i = 5; i <= 10; i++) {
      expect(ruta.delNivel('n$i'), isEmpty, reason: 'n$i');
    }
    expect(nivelPublicadoMaximo(ruta), 4);
    var previa = f0.last.id;
    for (final nivel in publicados.skip(1)) {
      final clases = ruta.delNivel(nivel);
      expect(clases, hasLength(50), reason: nivel);
      for (final u in clases) {
        expect(u.id, startsWith('zh.$nivel.c'), reason: u.id);
        expect(u.prerequisitos, [previa], reason: u.id);
        previa = u.id;
      }
    }
    // La romanización llega intacta a las clases (N1–N4: visible).
    final items = [
      for (final u in ruta.unidades)
        for (final p in u.pasos) ...p.items,
    ];
    expect(items.where((i) => i.tieneRom).length, greaterThan(500));
    expect(idiomasConRuta, contains('zh'));
    const s = ProgressState(idiomaMeta: 'zh', fundamentos: true);
    expect(s.fundamentosPendientes, isTrue);
    expect(s.nivel0Pendiente, isTrue);
    // Un alumno ubicado más arriba (diagnóstico antiguo) se queda en N4.
    const alto = ProgressState(idiomaMeta: 'zh', nivelInicial: 8);
    expect(nivelAlumnoEnRuta(ruta, alto), 4);
  });

  test('el japonés (versión esencial): ruta f0 (8 unidades) y solo N1–N4 publicados', () async {
    expect(idiomasSoloRutaF0, contains('ja'));
    await ContenidoJson.precargar('ja');
    expect(Fundamentos.disponible('ja'), isFalse); // nunca tuvo nivel-0.json (su Nivel 0 es el nuevo)
    final cargador = CargadorRuta();
    final ruta = await cargador.cargar('ja');
    expect(ruta, isNotNull);
    expect(cargador.modulosConError, isEmpty);
    final f0 = ruta!.delNivel('f0');
    expect(f0, hasLength(8));
    expect(f0.first.id, 'ja.f0.aisatsu');
    expect(f0.last.id, 'ja.f0.jikoshoukai');
    expect(ruta.delNivel('a1-1'), isEmpty);
    expect(ruta.curso.idiomasApoyo, ['es', 'en']);
    expect(problemasDeContenido(ruta, formasVerbales: await cargador.formasVerbales('ja')), isEmpty);
    final publicados = [
      for (final n in ruta.curso.niveles)
        if (n.estado == EstadoNivel.publicado) n.id,
    ];
    // Versión esencial: N1–N4 (50 clases por nivel); N5–N10 aún no existen
    // en el curso, así que la app los muestra «Próximamente» y no se juegan.
    expect(publicados, ['f0', 'n1', 'n2', 'n3', 'n4']);
    for (var i = 5; i <= 10; i++) {
      expect(ruta.delNivel('n$i'), isEmpty, reason: 'n$i');
    }
    expect(nivelPublicadoMaximo(ruta), 4);
    var previa = f0.last.id;
    for (final nivel in publicados.skip(1)) {
      final clases = ruta.delNivel(nivel);
      expect(clases, hasLength(50), reason: nivel);
      for (final u in clases) {
        expect(u.id, startsWith('ja.$nivel.c'), reason: u.id);
        expect(u.prerequisitos, [previa], reason: u.id);
        previa = u.id;
      }
    }
    // La romanización llega intacta a las clases (N1–N4: visible).
    final items = [
      for (final u in ruta.unidades)
        for (final p in u.pasos) ...p.items,
    ];
    expect(items.where((i) => i.tieneRom).length, greaterThan(500));
    expect(idiomasConRuta, contains('ja'));
    const s = ProgressState(idiomaMeta: 'ja', fundamentos: true);
    expect(s.fundamentosPendientes, isTrue);
    expect(s.nivel0Pendiente, isTrue);
    // Un alumno ubicado más arriba (diagnóstico antiguo) se queda en N4.
    const alto = ProgressState(idiomaMeta: 'ja', nivelInicial: 8);
    expect(nivelAlumnoEnRuta(ruta, alto), 4);
  });

  test('el ruso (versión esencial): ruta f0 (8 unidades) y solo N1–N4 publicados', () async {
    expect(idiomasSoloRutaF0, contains('ru'));
    await ContenidoJson.precargar('ru');
    expect(Fundamentos.disponible('ru'), isFalse); // no tiene nivel-0.json (su Nivel 0 es el nuevo, en nivel0/)
    final cargador = CargadorRuta();
    final ruta = await cargador.cargar('ru');
    expect(ruta, isNotNull);
    expect(cargador.modulosConError, isEmpty);
    final f0 = ruta!.delNivel('f0');
    expect(f0, hasLength(8));
    expect(f0.first.id, 'ru.f0.privetstviya');
    expect(f0.last.id, 'ru.f0.predstavlenie');
    expect(ruta.delNivel('a1-1'), isEmpty);
    expect(ruta.curso.idiomasApoyo, ['es', 'en']);
    expect(problemasDeContenido(ruta, formasVerbales: await cargador.formasVerbales('ru')), isEmpty);
    final publicados = [
      for (final n in ruta.curso.niveles)
        if (n.estado == EstadoNivel.publicado) n.id,
    ];
    // Versión esencial: N1–N4 (50 clases por nivel); N5–N10 aún no existen
    // en el curso, así que la app los muestra «Próximamente» y no se juegan.
    expect(publicados, ['f0', 'n1', 'n2', 'n3', 'n4']);
    for (var i = 5; i <= 10; i++) {
      expect(ruta.delNivel('n$i'), isEmpty, reason: 'n$i');
    }
    expect(nivelPublicadoMaximo(ruta), 4);
    var previa = f0.last.id;
    for (final nivel in publicados.skip(1)) {
      final clases = ruta.delNivel(nivel);
      expect(clases, hasLength(50), reason: nivel);
      for (final u in clases) {
        expect(u.id, startsWith('ru.$nivel.c'), reason: u.id);
        expect(u.prerequisitos, [previa], reason: u.id);
        previa = u.id;
      }
    }
    // La romanización llega intacta a las clases (N1–N4: visible).
    final items = [
      for (final u in ruta.unidades)
        for (final p in u.pasos) ...p.items,
    ];
    expect(items.where((i) => i.tieneRom).length, greaterThan(500));
    expect(idiomasConRuta, contains('ru'));
    const s = ProgressState(idiomaMeta: 'ru', fundamentos: true);
    expect(s.fundamentosPendientes, isTrue);
    expect(s.nivel0Pendiente, isTrue);
    // Un alumno ubicado más arriba (diagnóstico antiguo) se queda en N4.
    const alto = ProgressState(idiomaMeta: 'ru', nivelInicial: 8);
    expect(nivelAlumnoEnRuta(ruta, alto), 4);
  });

  test('el coreano (versión esencial): ruta f0 (9 unidades) y solo N1–N4 publicados', () async {
    expect(idiomasSoloRutaF0, contains('ko'));
    await ContenidoJson.precargar('ko');
    expect(Fundamentos.disponible('ko'), isFalse); // no tiene nivel-0.json (su Nivel 0 es el nuevo, en nivel0/)
    final cargador = CargadorRuta();
    final ruta = await cargador.cargar('ko');
    expect(ruta, isNotNull);
    expect(cargador.modulosConError, isEmpty);
    final f0 = ruta!.delNivel('f0');
    expect(f0, hasLength(9));
    expect(f0.first.id, 'ko.f0.insa');
    expect(f0.last.id, 'ko.f0.sogae');
    expect(ruta.delNivel('a1-1'), isEmpty);
    expect(ruta.curso.idiomasApoyo, ['es', 'en']);
    expect(problemasDeContenido(ruta, formasVerbales: await cargador.formasVerbales('ko')), isEmpty);
    final publicados = [
      for (final n in ruta.curso.niveles)
        if (n.estado == EstadoNivel.publicado) n.id,
    ];
    // Versión esencial: N1–N4 (50 clases por nivel); N5–N10 aún no existen
    // en el curso, así que la app los muestra «Próximamente» y no se juegan.
    expect(publicados, ['f0', 'n1', 'n2', 'n3', 'n4']);
    for (var i = 5; i <= 10; i++) {
      expect(ruta.delNivel('n$i'), isEmpty, reason: 'n$i');
    }
    expect(nivelPublicadoMaximo(ruta), 4);
    var previa = f0.last.id;
    for (final nivel in publicados.skip(1)) {
      final clases = ruta.delNivel(nivel);
      expect(clases, hasLength(50), reason: nivel);
      for (final u in clases) {
        expect(u.id, startsWith('ko.$nivel.c'), reason: u.id);
        expect(u.prerequisitos, [previa], reason: u.id);
        previa = u.id;
      }
    }
    // La romanización llega intacta a las clases (N1–N4: visible).
    final items = [
      for (final u in ruta.unidades)
        for (final p in u.pasos) ...p.items,
    ];
    expect(items.where((i) => i.tieneRom).length, greaterThan(500));
    expect(idiomasConRuta, contains('ko'));
    const s = ProgressState(idiomaMeta: 'ko', fundamentos: true);
    expect(s.fundamentosPendientes, isTrue);
    expect(s.nivel0Pendiente, isTrue);
    // Un alumno ubicado más arriba (diagnóstico antiguo) se queda en N4.
    const alto = ProgressState(idiomaMeta: 'ko', nivelInicial: 8);
    expect(nivelAlumnoEnRuta(ruta, alto), 4);
  });

}
