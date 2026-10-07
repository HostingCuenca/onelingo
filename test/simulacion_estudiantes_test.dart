import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';

/// Recorridos mínimos de estudiantes: no modifica ni genera contenido.
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late final Map<String, RutaCargada> rutas;

  setUpAll(() async {
    final cargador = CargadorRuta();
    rutas = {
      for (final idioma in ['en'])
        idioma: (await cargador.cargar(idioma))!,
    };
  });

  test('principiante: empieza disponible y no salta prerrequisitos', () {
    final ruta = rutas['en']!;
    final estados = estadosRuta(ruta, {});
    expect(
      estados.values.where((e) => e.estado == EstadoUnidad.disponible),
      hasLength(1),
    );
    expect(unidadRecomendada(ruta, estados), isNotNull);
  });

  test('diagnóstico a nivel sin contenido: niveles anteriores omitibles', () {
    final ruta = rutas['en']!;
    final base = nivelBaseDisponible(ruta, 8);
    final estados = estadosRuta(ruta, {}, nivelBase: base);
    final anteriores = ruta.unidades.where(
      (u) => (u.nivelInterno ?? 99) < base,
    );
    expect(anteriores, isNotEmpty);
    expect(anteriores.every((u) => estados[u.id]!.omitible), isTrue);
    final siguiente = unidadRecomendada(ruta, estados);
    expect(siguiente, isNotNull);
    expect(siguiente!.nivelInterno, base);
  });

  test('prerrequisito omitible no bloquea la primera unidad del nivel', () {
    final ruta = rutas['en']!;
    final estados = estadosRuta(ruta, {}, nivelBase: 1);
    final primera = ruta.unidades.firstWhere((u) => u.nivelInterno == 1);
    expect(estados[primera.id]!.estado, isNot(EstadoUnidad.bloqueada));
  });

  test('estudiante que vuelve encuentra primero el repaso vencido', () {
    final ruta = rutas['en']!;
    final unidad = ruta.unidades.first;
    final estados = estadosRuta(ruta, {
      ClaveRuta.evaluacion(unidad.id): {
        'aprobada': true,
        'fechaAprobada': '2026-09-20T10:00:00.000',
      },
      ClaveRuta.repaso(unidad.id): {
        'proximo': '2026-09-21T10:00:00.000',
        'retencion': false,
      },
    }, ahora: DateTime(2026, 9, 27));
    expect(estados[unidad.id]!.repasoPendiente, isTrue);
    expect(unidadRecomendada(ruta, estados)?.id, unidad.id);
  });

  test('fallar un repaso crea refuerzo sin borrar el dominio histórico', () {
    final unidad = rutas['en']!.unidades.first;
    final aprobado = resumenEvaluacion(
      unidad,
      5,
      5,
      null,
      DateTime(2026, 9, 20),
    );
    final retenido = siguienteRepaso(
      unidad,
      aprobado,
      null,
      5,
      5,
      DateTime(2026, 9, 22),
    );
    final fallo = siguienteRepaso(
      unidad,
      aprobado,
      retenido,
      1,
      5,
      DateTime(2026, 9, 27),
    );
    expect(fallo['retencion'], isTrue);
    expect(fallo['necesitaRefuerzo'], isTrue);
  });
}
