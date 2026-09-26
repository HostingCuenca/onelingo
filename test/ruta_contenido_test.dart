import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/integridad.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/content/curriculum.dart';

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

  test('Solo inglés está revisado; el resto se marca «versión inicial»', () async {
    for (final l in idiomas) {
      final ruta = (await CargadorRuta().cargar(l.code))!;
      expect(ruta.curso.revisionInicial, l.code != 'en', reason: l.code);
    }
  });

  test('TextoApoyo: nativo → predeterminado → español', () {
    const t = TextoApoyo({'es': 'hola', 'en': 'hello'});
    expect(t.en(cadenaApoyo('en', 'es')), 'hello');
    expect(t.en(cadenaApoyo('fr', 'es')), 'hola');
    expect(t.en(cadenaApoyo('fr', 'en')), 'hello');
    expect(TextoApoyo.fromJson('solo').en(['en']), 'solo');
  });
}
