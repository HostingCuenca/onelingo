import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/content/situaciones.dart';
import 'package:onelingo/core/i18n/i18n.dart';
import 'package:onelingo/core/lexico/lexico.dart';
import 'package:onelingo/core/lexico/verbos.dart';
import 'package:onelingo/core/nivel0/nivel0.dart';
import 'package:onelingo/features/lexico/repaso_palabras_screen.dart';

Map<String, dynamic> _json(String p) =>
    jsonDecode(File(p).readAsStringSync()) as Map<String, dynamic>;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late RutaCargada ruta;
  late Map<int, ContenidoSituacion> situaciones;
  late LexicoIndice lexico;
  setUpAll(() async {
    ruta = (await CargadorRuta().cargar('en'))!;
    situaciones = situacionesDesdeJson(
      _json('assets/contenido/en/situaciones.json'),
    )!;
    lexico = LexicoIndice.construir(
      idioma: 'en',
      cadena: const ['es'],
      ruta: ruta,
      situaciones: situaciones,
      nivel0: Nivel0.desdeJson(
        _json('assets/contenido/en/nivel0/nivel0.json'),
        _json('assets/contenido/en/nivel0/sonidos.json'),
      ),
    );
  });

  test('un solo índice para clases, situaciones y Nivel 0', () {
    expect(claveLexico('  Hello! '), 'hello');
    expect(lexico.entradas.length, greaterThan(4000));
    final hello = lexico.entradas['hello']!;
    expect(hello.traduccion, isNotEmpty);
    // Una palabra de situación conoce su situación y su tramo.
    final palabra = situaciones[1]!.tramo(Tramo.intermedio).vocabulario.first;
    final e = lexico.entradas[claveLexico(palabra.en)]!;
    expect(e.situaciones, contains(1));
    expect(e.ejemplo, isNotNull);
    // Ninguna clave repetida: cada palabra vive una vez.
    expect(lexico.entradas.keys.toSet().length, lexico.entradas.length);
  });

  test('Mis palabras: solo lo que el alumno ya vio', () {
    expect(
      lexico.delAlumno(practicas: const {}, unidadesVistas: const {}),
      isEmpty,
    );
    final primera = ruta.delNivel('n1').first;
    final mias = lexico.delAlumno(
      practicas: const {},
      unidadesVistas: {primera.id},
    );
    final ensenadas = {
      for (final v in LexicoIndice.palabrasDeUnidad(primera))
        claveLexico(v.texto),
    };
    expect(mias.map((e) => e.clave).toSet(), ensenadas);
    // Empezar un tramo de situación añade sus palabras.
    final conSituacion = lexico.delAlumno(
      practicas: {
        clavePruebaSituacion('en', 7, Tramo.basico): {
          'aprobada': false,
          'aciertos': 5,
          'total': 10,
        },
      },
      unidadesVistas: const {},
      situaciones: situaciones,
    );
    expect(conSituacion.length, 10);
  });

  test('repaso espaciado por palabra', () {
    final hoy = DateTime(2026, 10, 1);
    var r = responderPalabra(null, true, hoy);
    expect((r.caja, r.proximo), (1, DateTime(2026, 10, 2)));
    r = responderPalabra(r, true, hoy);
    expect((r.caja, r.proximo), (2, DateTime(2026, 10, 4)));
    r = responderPalabra(r, false, hoy);
    expect((r.caja, r.proximo), (0, DateTime(2026, 10, 2)));
    // Guardado y leído desde practicas.
    final practicas = {
      claveRepasoLexico('en'): {
        'palabras': {'hello': r.toJson()},
      },
    };
    expect(repasoLexico(practicas, 'en')['hello']!.caja, 0);

    final mias = lexico.delAlumno(
      practicas: const {},
      unidadesVistas: {ruta.delNivel('n1').first.id},
    );
    final estado = {
      mias[0].clave: RepasoPalabra(2, DateTime(2026, 9, 30)), // vencida
      mias[1].clave: RepasoPalabra(3, DateTime(2026, 10, 9)), // al día
    };
    final sesion = seleccionarRepaso(mias, estado, hoy, n: 5);
    expect(sesion.first.clave, mias[0].clave);
    expect(sesion.map((e) => e.clave), isNot(contains(mias[1].clave)));
    expect(vencidasHoy(mias, estado, hoy), 1);
  });

  test('preguntas de palabras con opciones distintas y una correcta', () {
    final banco = lexico.entradas.values.take(200).toList();
    for (final forma in FormaPregunta.values) {
      final q = preguntaPalabra(banco[3], forma, banco, Random(1));
      expect(q.opciones.length, 4);
      expect(q.opciones.toSet().length, 4);
      expect(
        q.opciones[q.correcta],
        forma == FormaPregunta.inversa ? banco[3].texto : banco[3].traduccion,
      );
    }
  });

  test('Mis verbos: tablas generadas al día y práctica válida', () {
    final r = Process.runSync('python3', [
      'tools/contenido/verbos/generar_verbos.py',
      '--comprobar',
    ]);
    expect(r.exitCode, 0, reason: '${r.stdout}${r.stderr}');
    final v = Verbos.fromJson(
      localizarApoyo(_json('assets/contenido/en/verbos.json'), 'es')
          as Map<String, dynamic>,
    );
    expect(v.verbos.length, greaterThan(150));
    final go = v.porId('go')!;
    expect(go.irregular, isTrue);
    expect(go.tablas['presente']![2], 'goes');
    expect(go.tablas['perfecto']![2], 'has gone');
    expect(v.porId('be')!.tablas['pasado'], [
      'was',
      'were',
      'was',
      'were',
      'were',
      'were',
    ]);
    for (final x in v.verbos) {
      expect(x.tablas.keys.toSet(), {for (final t in v.tiempos) t.id});
      for (final t in x.tablas.values) {
        expect(t.length, v.personas.length);
      }
    }
    final p = preguntasVerbos(
      v,
      [
        for (final x in v.verbos)
          if (x.nivel <= 2) x,
      ],
      Random(4),
    );
    expect(p.length, 10);
    for (final q in p) {
      expect(q.opciones.toSet().length, q.opciones.length);
      expect(q.correcta, inInclusiveRange(0, q.opciones.length - 1));
    }
  });

  test('Mis verbos en francés: tablas completas, j’ ante vocal y práctica', () {
    final v = Verbos.fromJson(
      localizarApoyo(_json('assets/contenido/fr/verbos.json'), 'en')
          as Map<String, dynamic>,
    );
    expect(v.verbos.length, greaterThanOrEqualTo(100));
    final aller = v.porId('aller')!;
    expect(aller.irregular, isTrue);
    expect(aller.tablas['futuro']![0], 'irai');
    expect(aller.es, 'to go');
    expect(v.conPronombre(0, aller.tablas['futuro']![0]), 'j’irai');
    expect(v.conPronombre(1, 'vas'), 'tu vas');
    final p = preguntasVerbos(v, v.verbos, Random(5));
    expect(p.length, 10);
    for (final q in p) {
      expect(q.opciones.toSet().length, q.opciones.length);
    }
  });

  test('Mis verbos en español: tablas completas, apoyo en inglés y práctica', () {
    for (final interfaz in ['en', 'es']) {
      final v = Verbos.fromJson(
        localizarApoyo(_json('assets/contenido/es/verbos.json'), interfaz)
            as Map<String, dynamic>,
      );
      expect(v.verbos.length, greaterThanOrEqualTo(100));
      final ir = v.porId('ir')!;
      expect(ir.irregular, isTrue);
      expect(ir.tablas['preterito']![0], 'fui');
      expect(ir.tablas['subjuntivo']![0], 'vaya');
      expect(ir.es, 'to go');
      expect(v.conPronombre(1, 'vas'), 'tú vas');
      final p = preguntasVerbos(v, v.verbos, Random(5));
      expect(p.length, 10);
      for (final q in p) {
        expect(q.opciones.toSet().length, q.opciones.length);
      }
    }
  });
}
