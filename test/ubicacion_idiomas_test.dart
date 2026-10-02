import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/app/theme.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/aprendizaje/providers.dart';
import 'package:onelingo/core/aprendizaje/ubicacion.dart';
import 'package:onelingo/core/diagnostico.dart'
    show escalaDiagnosticoCliente, escalaDiagnosticoLegacy;
import 'package:onelingo/core/efectos.dart';
import 'package:onelingo/core/state/providers.dart';
import 'package:onelingo/features/course/levels_screen.dart';
import 'package:onelingo/features/onboarding/diagnostico_screen.dart';
import 'package:onelingo/features/onboarding/ubicacion_screen.dart';
import 'package:onelingo/features/ruta/item_view.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Prueba de ubicación v2 en idiomas distintos del inglés (FR-6).
///
/// Banco de muestra con la forma del francés: 4 ítems por habilidad
/// (3 opciones) y 2 de escritura en cada nivel de [niveles], con apoyo
/// bilingüe {es, en}.
Map<String, dynamic> bancoFrances({List<int> niveles = const [1]}) => {
  'schema': 'onelingo.diagnostico.v2',
  'idioma': 'fr',
  'items': [
    for (final n in niveles) ...[
      for (final h in habilidadesUbicacion)
        for (var k = 1; k <= 4; k++)
          {
            'id': 'dx.fr.n$n.$h.$k',
            'nivel': n,
            'habilidad': h,
            'formato': h == 'escucha' ? 'escuchar' : 'elegir',
            'consigna': {'es': 'Consigna $h $k N$n', 'en': 'Prompt $h $k N$n'},
            'feedback': {'es': 'Explicación', 'en': 'Explanation'},
            if (h == 'escucha') 'audio': 'Bonjour, je m’appelle Léa.',
            if (h == 'lectura') 'texto': 'Léa habite à Lyon. Elle a un chat.',
            'opciones': ['un', 'deux', 'trois'],
            'respuesta': 0,
          },
      for (var k = 1; k <= 2; k++)
        {
          'id': 'dx.fr.n$n.escritura.$k',
          'nivel': n,
          'habilidad': 'escritura',
          'formato': 'escribir',
          'consigna': {'es': 'Escribe N$n', 'en': 'Write N$n'},
          'feedback': {'es': 'x', 'en': 'x'},
          'respuesta': 'Je m’appelle Léa.',
        },
    ],
  ],
};

/// Responde al azar: elige una opción cualquiera y escribe algo sin sentido.
ResultadoUbicacion alAzar(
  List<ItemUbicacion> banco,
  Autodeclaracion d,
  Random rnd, {
  int? nivelMaximo,
}) {
  final u = Ubicacion(
    banco: banco,
    declarado: d,
    nivelMaximo: nivelMaximo,
    random: rnd,
  );
  var guardia = 0;
  for (var i = u.siguiente(); i != null; i = u.siguiente()) {
    final n = i.item.opciones.length;
    u.responder(rnd.nextInt(n) == i.item.indiceRespuesta);
    expect(++guardia, lessThan(30));
  }
  if (u.escritura() != null) u.responder(false);
  expect(u.terminado, isTrue);
  return u.resultado();
}

/// Simulación de respuestas al azar sobre un banco de francés.
void comprobarAzar(List<ItemUbicacion> banco, {int? nivelMaximo}) {
  final rnd = Random(21);
  const n = 400;
  var ceros = 0;
  for (var k = 0; k < n; k++) {
    // También declaraciones altas: la pantalla no las ofrece si el curso
    // solo llega a N1, pero el motor tampoco debe dejarse engañar.
    final d = [
      Autodeclaracion.poco,
      Autodeclaracion.poco,
      Autodeclaracion.defiendo,
      Autodeclaracion.avanzado,
    ][k % 4];
    final r = alAzar(banco, d, rnd, nivelMaximo: nivelMaximo);
    expect(r.nivel, lessThanOrEqualTo(1), reason: 'azar, $d');
    for (final v in r.habilidades.values) {
      expect(v, lessThanOrEqualTo(1));
    }
    if (r.desdeCero) ceros++;
  }
  expect(ceros / n, greaterThan(.9), reason: '$ceros de $n desde cero');
}

ProgressState frances({
  int nivelInicial = 1,
  int? nivelCliente,
  bool fundamentos = false,
  Map<String, dynamic>? diagnostico,
  String interfaz = 'es',
}) => ProgressState(
  onboardingDone: true,
  nombre: 'Ana',
  idiomaMeta: 'fr',
  idiomaInterfaz: interfaz,
  nivelInicial: nivelInicial,
  nivelEscala: nivelCliente == null
      ? escalaDiagnosticoLegacy
      : escalaDiagnosticoCliente,
  nivelClienteInicial: nivelCliente,
  fundamentos: fundamentos,
  diagnostico: diagnostico,
);

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('Motor por idioma', () {
    test('al azar en francés (solo N1): casi siempre desde cero, nunca > 1', () {
      comprobarAzar(ItemUbicacion.banco(bancoFrances()));
    });

    test(
      'al azar con el banco real del francés (si ya está compilado)',
      () {
        final f = File('assets/contenido/fr/diagnostico-v2.json');
        final banco = ItemUbicacion.banco(
          jsonDecode(f.readAsStringSync()) as Map<String, dynamic>,
        );
        comprobarAzar(banco, nivelMaximo: 1);
      },
      skip: File('assets/contenido/fr/diagnostico-v2.json').existsSync()
          ? false
          : 'el banco francés aún no está compilado',
    );

    test('quien domina N1 sale en N1 y nunca por encima del banco', () {
      final banco = ItemUbicacion.banco(bancoFrances());
      final rnd = Random(4);
      var unos = 0;
      for (var k = 0; k < 200; k++) {
        final u = Ubicacion(
          banco: banco,
          declarado: Autodeclaracion.poco,
          random: rnd,
        );
        expect(u.nivelMaximo, 1);
        for (var i = u.siguiente(); i != null; i = u.siguiente()) {
          expect(i.nivel, 1);
          u.responder(rnd.nextDouble() < .92);
        }
        if (u.escritura() != null) u.responder(true);
        final r = u.resultado();
        expect(r.nivel, lessThanOrEqualTo(1));
        if (r.nivel == 1) unos++;
      }
      expect(unos / 200, greaterThan(.85));
    });

    test('el tope corta el banco: N2 sin clases publicadas no se pregunta', () {
      final banco = ItemUbicacion.banco(bancoFrances(niveles: [1, 2]));
      expect(nivelMaximoUbicacion(banco), 2);
      expect(nivelMaximoUbicacion(banco, publicados: {1}), 1);
      final u = Ubicacion(
        banco: banco,
        declarado: Autodeclaracion.avanzado,
        nivelMaximo: 1,
        random: Random(1),
      );
      for (var i = u.siguiente(); i != null; i = u.siguiente()) {
        expect(i.nivel, 1);
        u.responder(true);
      }
      expect(u.resultado().nivel, 1);
      // Sin banco (o sin niveles publicados): desde cero, sin preguntas.
      final vacio = Ubicacion(
        banco: banco,
        declarado: Autodeclaracion.poco,
        nivelMaximo: 0,
      );
      expect(vacio.siguiente(), isNull);
      expect(vacio.escritura(), isNull);
      expect(vacio.terminado, isTrue);
      expect(vacio.resultado().nivel, 0);
    });

    test('solo se ofrecen puntos de partida con contenido', () {
      expect(Autodeclaracion.hasta(1), [
        Autodeclaracion.nada,
        Autodeclaracion.poco,
      ]);
      expect(Autodeclaracion.hasta(3), hasLength(3));
      expect(Autodeclaracion.hasta(10), Autodeclaracion.values);
      expect(Autodeclaracion.hasta(0), [Autodeclaracion.nada]);
    });

    test('los textos de apoyo salen en el idioma de la interfaz', () {
      final en = ItemUbicacion.bancoLocalizado(bancoFrances(), 'en');
      final es = ItemUbicacion.bancoLocalizado(bancoFrances(), 'es');
      expect(en.first.item.consigna.en(const []), 'Prompt escucha 1 N1');
      expect(es.first.item.consigna.en(const []), 'Consigna escucha 1 N1');
      // El idioma meta no se toca.
      expect(en.first.item.opciones.first.meta, 'un');
    });
  });

  group('Tope a lo publicado (francés)', () {
    late RutaCargada fr, en;
    setUpAll(() async {
      fr = (await CargadorRuta().cargar('fr'))!;
      en = (await CargadorRuta().cargar('en'))!;
    });

    test('niveles publicados', () {
      expect(nivelesPublicados(en), {for (var n = 1; n <= 10; n++) n});
      expect(nivelPublicadoMaximo(fr), greaterThanOrEqualTo(1));
    });

    test(
      'el diagnóstico antiguo en N4 no deja N1 superado ni al alumno en N4',
      () {
        final maximo = nivelPublicadoMaximo(fr);
        final diag = {
          'idioma': 'fr',
          'escala': escalaDiagnosticoLegacy,
          'nivel': 8,
          'recomendado': 8,
        };
        for (final (s, nivel) in [
          // Diagnóstico antiguo (escala histórica).
          (frances(nivelInicial: 4, diagnostico: diag), 4),
          (frances(nivelInicial: 8, diagnostico: diag), 8),
          // Prueba v2 guardada antes de limitarse (escala del curso).
          (frances(nivelCliente: 4, diagnostico: {'idioma': 'fr'}), 4),
        ]) {
          // Se queda en su nivel si está publicado; si no, en el más alto.
          final esperado = min(nivel, maximo);
          final e = estadosAlumno(fr, s);
          expect(nivelUbicacionRuta(fr, s), esperado);
          expect(nivelAlumnoEnRuta(fr, s), esperado);
          // Su nivel está abierto, no superado ni omitido.
          final id = 'n$esperado';
          final primera = e[fr.delNivel(id).first.id]!;
          expect(nivelSuperado(fr, e, s.practicas, id), isFalse);
          expect(primera.omitible, isFalse);
          expect(primera.estado, isNot(EstadoUnidad.bloqueada));
          // El diagnóstico guardado se conserva.
          expect(s.diagnostico, isNotNull);
        }
        // La ubicación v2 «desde cero» empieza por Fundamentos.
        final cero = frances(nivelCliente: 0, fundamentos: true);
        expect(nivelUbicacionRuta(fr, cero), 0);
        expect(
          estadosAlumno(fr, cero)[fr.delNivel('f0').first.id]!.omitible,
          isFalse,
        );
        // El inglés no cambia: sus diez niveles están publicados.
        final ingles = ProgressState(
          idiomaMeta: 'en',
          nivelEscala: escalaDiagnosticoCliente,
          nivelClienteInicial: 6,
        );
        expect(nivelAlumnoEnRuta(en, ingles), 6);
        expect(nivelUbicacionRuta(en, ingles), 6);
      },
    );

    testWidgets('Aprender: el nivel publicado más alto en curso con diagnóstico N4', (
      tester,
    ) async {
      tester.view.physicalSize = const Size(390, 2400);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      final s = frances(
        nivelInicial: 4,
        diagnostico: {'idioma': 'fr', 'escala': escalaDiagnosticoLegacy},
      );
      SharedPreferences.setMockInitialValues({
        'onelingo.progress.v1': jsonEncode(s.toJson()),
      });
      final p = await SharedPreferences.getInstance();
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            prefsProvider.overrideWithValue(p),
            rutaProvider.overrideWith((ref, idioma) async => fr),
          ],
          child: MaterialApp(theme: buildTheme(), home: const LevelsScreen()),
        ),
      );
      await tester.pump();
      await tester.pump();
      // Con el tope, el alumno estudia N4 o, si aún no está publicado, el
      // nivel publicado más alto; nunca un nivel sin clases.
      final tope = min(4, nivelPublicadoMaximo(fr));
      final cefr = fr.curso.niveles.firstWhere((n) => n.id == 'n$tope').cefr;
      final n1 = find.ancestor(
        of: find.text('Nivel $tope · $cefr'),
        matching: find.byType(Row),
      );
      expect(n1, findsWidgets);
      expect(
        find.descendant(of: n1.first, matching: find.text('Superado')),
        findsNothing,
      );
      expect(
        find.descendant(
          of: n1.first,
          matching: find.textContaining(
            'de ${fr.delNivel('n$tope').length} clases',
          ),
        ),
        findsOneWidget,
      );
    });
  });

  group('Pantalla por idioma', () {
    Future<void> montar(
      WidgetTester tester, {
      required BancoUbicacion? banco,
      String interfaz = 'es',
    }) async {
      tester.view.physicalSize = const Size(390, 844);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      Efectos.sonido = false;
      addTearDown(() => Efectos.sonido = true);
      SharedPreferences.setMockInitialValues({
        'onelingo.progress.v1': jsonEncode(
          frances(interfaz: interfaz).toJson(),
        ),
      });
      final p = await SharedPreferences.getInstance();
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            prefsProvider.overrideWithValue(p),
            bancoUbicacionProvider.overrideWith((ref, idioma) async => banco),
          ],
          child: MaterialApp(
            theme: buildTheme(),
            home: const PruebaNivelScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();
    }

    testWidgets('francés con banco: prueba v2 solo con N1 y voz francesa', (
      tester,
    ) async {
      await montar(tester, banco: BancoUbicacion(bancoFrances(), 1));
      expect(find.byType(UbicacionScreen), findsOneWidget);
      expect(find.text('¿Cuánto francés sabes?'), findsOneWidget);
      expect(find.text('Nada, empiezo de cero'), findsOneWidget);
      expect(find.text('Un poco'), findsOneWidget);
      // Sin contenido por encima de N1: no se ofrecen esos puntos de partida.
      expect(find.text('Me defiendo'), findsNothing);
      expect(find.text('Avanzado'), findsNothing);
      await tester.tap(find.text('Un poco'));
      await tester.pumpAndSettle();
      final vista = tester.widget<ItemView>(find.byType(ItemView));
      expect(vista.idioma, 'fr');
      expect(vista.item.id, startsWith('dx.fr.n1.'));
      expect(find.textContaining('Consigna'), findsWidgets);
    });

    testWidgets('consignas en inglés si la interfaz está en inglés', (
      tester,
    ) async {
      await montar(
        tester,
        banco: BancoUbicacion(bancoFrances(), 1),
        interfaz: 'en',
      );
      await tester.tap(find.text('Un poco'));
      await tester.pumpAndSettle();
      expect(find.textContaining('Prompt'), findsWidgets);
      expect(find.textContaining('Consigna'), findsNothing);
    });

    testWidgets('francés sin banco v2: sigue el diagnóstico anterior', (
      tester,
    ) async {
      await montar(tester, banco: null);
      expect(find.byType(DiagnosticoScreen), findsOneWidget);
      expect(find.byType(UbicacionScreen), findsNothing);
    });
  });
}
