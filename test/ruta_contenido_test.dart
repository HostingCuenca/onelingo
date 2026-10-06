import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/biblioteca_adaptador.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/integridad.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/content/curriculum.dart';
import 'package:onelingo/core/content/fundamentos.dart' show idiomasSoloRutaF0;

/// Integridad de las rutas de los 10 idiomas habilitados.
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  for (final l in idiomas) {
    test('Ruta ${l.code}: existe, grafo válido y nada sin enseñar', () async {
      final ruta = await CargadorRuta().cargar(l.code);
      expect(ruta, isNotNull, reason: 'falta assets/contenido/${l.code}/ruta');
      final unidades = ruta!.delNivel('f0');
      expect(unidades.length, greaterThanOrEqualTo(5));
      expect(problemasDeContenido(ruta), isEmpty);
      // Cadena lineal: la primera sin prerrequisitos, las demás con alguno.
      expect(unidades.first.prerequisitos, isEmpty);
      for (final u in unidades.skip(1)) {
        expect(u.prerequisitos, isNotEmpty, reason: u.id);
      }
      // Todas las unidades de fundamentos: Pre-A1, nivel interno 0.
      for (final u in unidades) {
        expect(u.id.startsWith('${l.code}.f0.'), isTrue, reason: u.id);
        expect(u.nivelInterno, 0);
        expect(u.cefr, 'Pre-A1');
      }
      // C2 planificado sin nivel interno (DEC-002).
      final c2 = ruta.curso.niveles.where((n) => n.cefr == 'C2');
      expect(c2.single.estado, EstadoNivel.planificado);
      expect(c2.single.nivelInterno, isNull);
    });
  }

  test(
    'Inglés N1: 100 clases editoriales activas y sin módulos rotos',
    () async {
      final cargador = CargadorRuta();
      final ruta = (await cargador.cargar('en'))!;
      expect(cargador.modulosConError, isEmpty);
      final n1 = ruta.delNivel('n1');
      expect(n1.length, 100);
      for (final u in n1) {
        expect(u.cefr, 'A1', reason: u.id);
        expect(u.nivelInterno, 1, reason: u.id);
        expect(u.id.startsWith('en.n1.class-'), isTrue, reason: u.id);
      }
      expect(n1.first.prerequisitos, ['en.f0.presentarse']);
      expect(n1.last.id, 'en.n1.class-100');
      final vocabularioVisible = n1.first.pasos.firstWhere(
        (paso) => paso.tipo == TipoPaso.vocabulario,
      );
      expect(vocabularioVisible.refs, hasLength(8));
      expect(
        vocabularioVisible.refs,
        everyElement(isNot(contains('good-night'))),
      );
      expect(ruta.unidades.map((u) => u.orden).toList(), [
        for (var i = 0; i < ruta.unidades.length; i++) i,
      ]);
    },
  );

  test('Inglés N1–N3 consumen los cuatro pools editoriales activos', () async {
    final loader = CargadorBiblioteca();
    final samples = [
      await loader.resolverUnidad('en', 'en.n1.class-01'),
      await loader.resolverUnidad('en', 'en.n1.class-100'),
      await loader.resolverUnidad('en', 'en.n2.class-01'),
      await loader.resolverUnidad('en', 'en.n2.class-100'),
      await loader.resolverUnidad('en', 'en.n3.class-01'),
      await loader.resolverUnidad('en', 'en.n3.class-90'),
    ];
    for (final runtime in samples) {
      expect(runtime.activa, isTrue);
      expect(runtime.libraryVersion, '2026.09.30-en-pulido.1');
      expect(runtime.pool('practiceGuided')!.variants, hasLength(3));
      expect(runtime.pool('practice')!.variants, hasLength(3));
      expect(runtime.pool('evaluation')!.variants, hasLength(4));
      expect(runtime.pool('review')!.variants, hasLength(3));
    }
    expect(
      samples.first.pool('evaluation')!.selectionId,
      (await loader.resolverUnidad(
        'en',
        'en.n1.class-01',
      )).pool('evaluation')!.selectionId,
    );
  });

  test(
    'Inglés publica un corte continuo: cada nivel encadena sus clases',
    () async {
      final ruta = (await CargadorRuta().cargar('en'))!;
      var previa = 'en.f0.presentarse';
      for (final nivel in ruta.curso.niveles.where(
        (n) => n.id.startsWith('n') && ruta.delNivel(n.id).isNotEmpty,
      )) {
        final clases = ruta.delNivel(nivel.id);
        for (var i = 0; i < clases.length; i++) {
          final u = clases[i];
          expect(
            u.id,
            'en.${nivel.id}.class-${(i + 1).toString().padLeft(2, '0')}',
          );
          expect(u.prerequisitos, [previa], reason: u.id);
          expect(u.cefr, nivel.cefr, reason: u.id);
          expect(u.nivelInterno, nivel.nivelInterno, reason: u.id);
          previa = u.id;
        }
      }
      expect(ruta.delNivel('n1'), hasLength(100));
      expect(ruta.delNivel('n2'), hasLength(100));
    },
  );

  test(
    'Los 10 idiomas tienen escritura/sonidos y un A1 inicial con tablas',
    () async {
      for (final l in idiomas) {
        final ruta = (await CargadorRuta().cargar(l.code))!;
        bool conTabla(List<UnidadRuta> us) =>
            us.any((u) => u.pasos.any((p) => p.tipo == TipoPaso.tabla));
        // En reconstrucción (portugués, DEC-035): solo Fundamentos, sin A1 aún.
        if (idiomasSoloRutaF0.contains(l.code)) {
          expect(ruta.delNivel('n1'), isEmpty, reason: l.code);
          expect(ruta.delNivel('a1-1'), isEmpty, reason: l.code);
          expect(conTabla(ruta.delNivel('f0')), isTrue, reason: l.code);
          expect(ruta.unidades.map((u) => u.orden).toList(), [
            for (var i = 0; i < ruta.unidades.length; i++) i,
          ], reason: l.code);
          continue;
        }
        // Con N1 publicado (inglés, francés) el A1 es n1; si no, a1-1.
        final a1 = ruta.delNivel(
          ruta.delNivel('n1').isNotEmpty ? 'n1' : 'a1-1',
        );
        expect(a1.length, greaterThanOrEqualTo(7), reason: l.code);
        // El A1 empieza donde terminan los fundamentos.
        expect(a1.first.prerequisitos, [
          ruta.delNivel('f0').last.id,
        ], reason: l.code);
        // Hay tablas (escritura o conjugación) en fundamentos y en A1.
        expect(conTabla(ruta.delNivel('f0')), isTrue, reason: l.code);
        if (l.code != 'en') expect(conTabla(a1), isTrue, reason: l.code);
        // Orden global consecutivo.
        expect(ruta.unidades.map((u) => u.orden).toList(), [
          for (var i = 0; i < ruta.unidades.length; i++) i,
        ], reason: l.code);
      }
    },
  );

  test('Ningún idioma tiene módulos que no cargan', () async {
    for (final l in idiomas) {
      final cargador = CargadorRuta();
      await cargador.cargar(l.code);
      expect(cargador.modulosConError, isEmpty, reason: l.code);
    }
  });

  test('Idiomas de apoyo (DEC-004): español explicado en inglés', () async {
    final es = (await CargadorRuta().cargar('es'))!;
    expect(es.curso.apoyoPredeterminado, 'en');
    final explicacion = es.unidades.first.pasos
        .firstWhere((p) => p.tipo == TipoPaso.explicacion)
        .texto!;
    // Un angloparlante recibe inglés y un francófono también (respaldo del curso).
    final enIngles = explicacion.en(cadenaApoyo('en', 'en'));
    expect(enIngles, isNotEmpty);
    expect(explicacion.en(cadenaApoyo('fr', 'en')), enIngles);
    final en = (await CargadorRuta().cargar('en'))!;
    expect(en.curso.idiomasApoyo, ['es']);
    expect(en.curso.revisionInicial, isFalse);
  });

  test(
    'Solo inglés está revisado; el resto se marca «versión inicial»',
    () async {
      for (final l in idiomas) {
        final ruta = (await CargadorRuta().cargar(l.code))!;
        expect(ruta.curso.revisionInicial, l.code != 'en', reason: l.code);
      }
    },
  );

  test('TextoApoyo: nativo → predeterminado → español', () {
    const t = TextoApoyo({'es': 'hola', 'en': 'hello'});
    expect(t.en(cadenaApoyo('en', 'es')), 'hello');
    expect(t.en(cadenaApoyo('fr', 'es')), 'hola');
    expect(t.en(cadenaApoyo('fr', 'en')), 'hello');
    expect(TextoApoyo.fromJson('solo').en(['en']), 'solo');
  });
}
