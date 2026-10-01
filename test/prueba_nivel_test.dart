import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/aprendizaje/providers.dart';
import 'package:onelingo/core/diagnostico.dart';
import 'package:onelingo/core/state/providers.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late RutaCargada ruta;
  setUpAll(() async {
    ruta = (await CargadorRuta().cargar('en'))!;
  });

  test('la prueba cubre todo el nivel con formatos que se corrigen solos', () {
    for (final nivel in ['n1', 'n5', 'n10']) {
      final items = itemsPruebaNivel(ruta, nivel, Random(1));
      expect(items, hasLength(preguntasPruebaNivel), reason: nivel);
      expect(items.map((i) => i.id).toSet(), hasLength(items.length));
      expect(
        items.where((i) => i.formato == FormatoItem.escribir),
        isEmpty,
        reason: nivel,
      );
      // Cada intento sale distinto: no se puede memorizar.
      final otra = itemsPruebaNivel(ruta, nivel, Random(2));
      expect(
        otra.map((i) => i.id).toList(),
        isNot(items.map((i) => i.id).toList()),
      );
    }
  });

  test('aprobar la prueba supera el nivel y abre el siguiente', () {
    const base = ProgressState(
      onboardingDone: true,
      idiomaMeta: 'en',
      nivelInicial: 1,
      nivelEscala: escalaDiagnosticoCliente,
      nivelClienteInicial: 1,
    );
    var e = estadosAlumno(ruta, base);
    final n2 = ruta.delNivel('n2').first.id;
    expect(e[n2]!.estado, EstadoUnidad.bloqueada);
    expect(nivelSuperado(ruta, e, base.practicas, 'n1'), isFalse);

    // Una prueba suspendida no cambia nada.
    final suspendida = base.copyWith(
      practicas: {
        ClaveRuta.pruebaNivel('en', 'n1'): {'aprobada': false},
      },
    );
    e = estadosAlumno(ruta, suspendida);
    expect(e[n2]!.estado, EstadoUnidad.bloqueada);

    final aprobada = base.copyWith(
      practicas: {
        ClaveRuta.pruebaNivel('en', 'n1'): {'aprobada': true},
      },
    );
    e = estadosAlumno(ruta, aprobada);
    expect(nivelSuperado(ruta, e, aprobada.practicas, 'n1'), isTrue);
    expect(e[n2]!.estado, isNot(EstadoUnidad.bloqueada));
    // Las clases del nivel superado quedan abiertas para repasar.
    for (final u in ruta.delNivel('n1')) {
      expect(e[u.id]!.omitible, isTrue, reason: u.id);
    }
    // El nivel 3 sigue cerrado hasta superar el 2.
    expect(e[ruta.delNivel('n3').first.id]!.estado, EstadoUnidad.bloqueada);
  });
}
