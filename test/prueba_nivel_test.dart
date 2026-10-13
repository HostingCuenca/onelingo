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

  test('la prueba es exigente: 90 %, todo el nivel, escuchar y escribir', () {
    expect(
      aciertosPruebaNivel / preguntasPruebaNivel,
      greaterThanOrEqualTo(0.9),
    );
    for (final nivel in ['n1', 'n5', 'n10']) {
      final items = itemsPruebaNivel(ruta, nivel, Random(1));
      expect(items, hasLength(preguntasPruebaNivel), reason: nivel);
      expect(items.map((i) => i.id).toSet(), hasLength(items.length));
      final formatos = items.map((i) => i.formato).toList();
      // Se oye y se produce: elegir y relacionar (que se aciertan por
      // descarte) solo entran si un tramo no tiene otra cosa.
      int n(FormatoItem f) => formatos.where((x) => x == f).length;
      expect(n(FormatoItem.escuchar), greaterThanOrEqualTo(5), reason: nivel);
      expect(n(FormatoItem.escribir), greaterThanOrEqualTo(3), reason: nivel);
      expect(
        n(FormatoItem.elegir) + n(FormatoItem.relacionar),
        lessThanOrEqualTo(2),
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

  test('francés: la prueba del nivel sale de su propia ruta', () async {
    final fr = (await CargadorRuta().cargar('fr'))!;
    final n1 = fr.curso.niveles.firstWhere((n) => n.nivelInterno == 1);
    final items = itemsPruebaNivel(fr, n1.id, Random(3));
    expect(items, hasLength(preguntasPruebaNivel));
    expect(items.where((i) => i.formato == FormatoItem.escribir), isNotEmpty);
  });

  test('tras suspender hay que esperar para repetirla', () {
    final clave = ClaveRuta.pruebaNivel('en', 'n1');
    final intento = DateTime(2026, 10, 13, 9);
    Map<String, dynamic> con(bool aprobada) => {
      clave: {'aprobada': aprobada, 'fecha': intento.toIso8601String()},
    };
    expect(pruebaNivelDisponibleDesde(const {}, 'en', 'n1'), isNull);
    expect(
      pruebaNivelDisponibleDesde(
        con(false),
        'en',
        'n1',
        ahora: intento.add(const Duration(hours: 1)),
      ),
      intento.add(esperaPruebaNivel),
    );
    expect(
      pruebaNivelDisponibleDesde(
        con(false),
        'en',
        'n1',
        ahora: intento.add(esperaPruebaNivel),
      ),
      isNull,
    );
    expect(
      pruebaNivelDisponibleDesde(con(true), 'en', 'n1', ahora: intento),
      isNull,
    );
  });
}
