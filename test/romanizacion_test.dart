import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/i18n/i18n.dart';
import 'package:onelingo/core/nivel0/nivel0.dart';
import 'package:onelingo/features/ruta/item_view.dart';
import 'package:onelingo/shared/widgets/romanizacion.dart';

/// Romanización de ru, ko, ja y zh (docs/claude-educacion/ROMANIZACION.md).
/// Los cuatro idiomas aún no están publicados: los JSON se leen directamente
/// (borradores de Fundamentos y Nivel 0), sin pasar por `idiomasConNivel0`.
const _noLatinos = ['ru', 'ko', 'ja', 'zh'];

final _escritura = {
  'ru': RegExp(r'[А-Яа-яЁё]'),
  'ko': RegExp(r'[가-힣ㄱ-ㅣ]'),
  'ja': RegExp(r'[ぁ-ゖァ-ヺー一-鿿]'),
  'zh': RegExp(r'[一-鿿]'),
};

List<UnidadRuta> _borrador(String idioma) {
  final j = jsonDecode(
    File('tools/contenido/ruta-$idioma/borrador-f0.json').readAsStringSync(),
  ) as Map<String, dynamic>;
  return [
    for (final u in j['unidades'] as List)
      UnidadRuta.fromJson(
        u as Map<String, dynamic>,
        idioma: idioma,
        nivel: 'f0',
      ),
  ];
}

Nivel0 _nivel0(String idioma) {
  Map<String, dynamic> leer(String archivo) => localizarApoyo(
    jsonDecode(
      File('assets/contenido/$idioma/nivel0/$archivo').readAsStringSync(),
    ),
    'es',
  ) as Map<String, dynamic>;
  return Nivel0.desdeJson(leer('nivel0.json'), leer('sonidos.json'));
}

void main() {
  group('Item.fromJson lee la romanización de los ítems', () {
    test('campos con sufijo Rom; "" y null = sin romanización', () {
      final item = Item.fromJson({
        'id': 'g1',
        'formato': 'completar',
        'consigna': {'es': 'Completa'},
        'feedback': {'es': 'Bien'},
        'texto': 'Спасибо! — ___!',
        'textoRom': 'Spasíbo! — ___!',
        'respuesta': 'Пожалуйста',
        'opciones': ['Пожалуйста', 'Пока'],
        'opcionesRom': ['Pozháluysta', ''],
      });
      expect(item.textoRom, 'Spasíbo! — ___!');
      expect(item.romOpcion(0), 'Pozháluysta');
      expect(item.romOpcion(1), isNull);
      expect(item.romOpcion(7), isNull);
      expect(item.tieneRom, isTrue);

      final orden = Item.fromJson({
        'id': 'e4',
        'formato': 'ordenar',
        'consigna': {'es': 'Ordena'},
        'feedback': {'es': 'Bien'},
        'tokens': ['明天', '见'],
        'tokensRom': ['míngtiān', 'jiàn'],
        'respuesta': '明天 见',
      });
      expect(orden.romToken(1), 'jiàn');

      final pares = Item.fromJson({
        'id': 'g3',
        'formato': 'relacionar',
        'consigna': {'es': 'Une'},
        'feedback': {'es': 'Bien'},
        'pares': [
          [
            '안녕',
            {'es': 'hola'},
          ],
        ],
        'paresRom': ['annyeong'],
      });
      expect(pares.romPar(0), 'annyeong');

      final latino = Item.fromJson({
        'id': 'x',
        'formato': 'elegir',
        'consigna': {'es': 'Elige'},
        'feedback': {'es': 'Bien'},
        'opciones': ['ciao', 'grazie'],
        'respuesta': 0,
      });
      expect(latino.tieneRom, isFalse);
      expect(latino.opcionesRom, isEmpty);
    });

    test('hablanteRom en las líneas de diálogo', () {
      final f = Frase.fromJson({
        'hablante': 'Продавец',
        'hablanteRom': 'Prodavéts',
        'texto': 'Добрый вечер!',
        'rom': 'Dóbryy vécher!',
        'traduccion': {'es': '¡Buenas tardes!'},
      });
      expect(f.rom, 'Dóbryy vécher!');
      expect(f.hablanteRom, 'Prodavéts');
    });
  });

  for (final idioma in _noLatinos) {
    test('Fundamentos ($idioma): cada texto, opción, ficha y par en el '
        'idioma tiene su romanización', () {
      final hay = _escritura[idioma]!;
      var conRom = 0;
      for (final u in _borrador(idioma)) {
        for (final p in u.pasos) {
          for (final it in p.items) {
            final donde = '${u.id}/${it.id}';
            if (hay.hasMatch(it.texto ?? '')) {
              expect(it.textoRom, isNotNull, reason: '$donde texto');
            }
            if (hay.hasMatch(it.pregunta ?? '')) {
              expect(it.preguntaRom, isNotNull, reason: '$donde pregunta');
            }
            for (var i = 0; i < it.opciones.length; i++) {
              if (hay.hasMatch(it.opciones[i].meta ?? '')) {
                expect(it.romOpcion(i), isNotNull, reason: '$donde opción $i');
              }
            }
            for (var i = 0; i < it.tokens.length; i++) {
              if (hay.hasMatch(it.tokens[i])) {
                expect(it.romToken(i), isNotNull, reason: '$donde token $i');
              }
            }
            for (var i = 0; i < it.pares.length; i++) {
              if (hay.hasMatch(it.pares[i].$1)) {
                expect(it.romPar(i), isNotNull, reason: '$donde par $i');
              }
            }
            if (it.tieneRom) conRom++;
          }
        }
      }
      expect(conRom, greaterThan(20));
    });
  }

  test('ru: las líneas de diálogo traen hablanteRom', () {
    final lineas = [
      for (final u in _borrador('ru'))
        for (final p in u.pasos)
          if (p.tipo == TipoPaso.situacion) ...p.frases,
    ];
    expect(lineas, isNotEmpty);
    expect(lineas.every((f) => f.hablanteRom != null), isTrue);
  });

  group('Nivel 0 de ru, ko, ja y zh', () {
    test('aún no se publican (no están en idiomasConNivel0)', () {
      for (final idioma in _noLatinos) {
        expect(idiomasConNivel0.contains(idioma), isFalse);
      }
    });

    for (final idioma in _noLatinos) {
      test('Nivel 0 ($idioma): idioma del curso y rom en palabras y pasos', () {
        final n = _nivel0(idioma);
        // La voz (y el TTS de las letras sueltas de escucha_letra) usa n.idioma.
        expect(n.idioma, idioma);
        final pasos = [for (final l in n.lecciones) ...l.pasos];
        // Palabras con `m` (tarjetas y opciones-palabra; las letras sueltas
        // de escucha_letra/deletreo van como texto plano).
        final palabras = [
          for (final p in pasos) ...p.palabras,
          for (final p in pasos)
            for (final o in p.j['opciones'] as List? ?? const [])
              if (o is Map) Palabra.fromJson(o as Map<String, dynamic>),
        ].where((w) => _escritura[idioma]!.hasMatch(w.texto)).toList();
        expect(palabras, isNotEmpty);
        if (idioma != 'ja') {
          // ja no pone rom en las opciones de escucha (las delataría).
          expect(palabras.every((w) => w.rom != null), isTrue);
        }
        for (final p in pasos) {
          if (const {'mira', 'repite', 'mezcla'}.contains(p.tipo)) {
            expect(p.rom, isNotNull, reason: '${p.tipo} ${p.marcado}');
          }
        }
        // Ninguna clave antigua (romOpciones, romFichas, romDe, romA).
        for (final p in pasos) {
          for (final k in p.j.keys) {
            expect(k.startsWith('rom') && k != 'rom', isFalse, reason: k);
          }
        }
      });
    }

    test('ko: opcionesRom, fichasRom, deRom y aRom', () {
      final pasos = [for (final l in _nivel0('ko').lecciones) ...l.pasos];
      final cambia = pasos.firstWhere((p) => p.tipo == 'cambia');
      expect(cambia.deRom, isNotNull);
      expect(cambia.aRom, isNotNull);
      expect(cambia.opcionesRom.length, cambia.textos.length);
      final construye = pasos.firstWhere((p) => p.fichasRom.isNotEmpty);
      expect(construye.romFicha(0), isNotNull);
      expect(_nivel0('ko').sonidos.first.anclaRom, isNotNull);
    });

    test('ja: escucha_letra lleva letraRom', () {
      final letras = [
        for (final l in _nivel0('ja').lecciones)
          ...l.pasos.where((p) => p.tipo == 'escucha_letra'),
      ];
      expect(letras, isNotEmpty);
      expect(letras.every((p) => p.letraRom != null), isTrue);
    });

    test('zh: anclaRom y ejemplosRom en el mapa de sonidos', () {
      final s = _nivel0('zh').sonidos.first;
      expect(s.anclaRom, isNotNull);
      expect(s.ejemplosRom.length, s.ejemplos.length);
    });

    test('sin «idioma» en el JSON se usa el del curso, no el inglés', () {
      final n = Nivel0.desdeJson(
        {'titulo': 't', 'subtitulo': 's', 'unidades': const []},
        {'vocales': const []},
        idioma: 'ko',
      );
      expect(n.idioma, 'ko');
    });
  });

  group('ItemView muestra la romanización', () {
    Widget app(Item item, {bool mostrar = true, VoidCallback? alternar}) =>
        MaterialApp(
          home: Scaffold(
            body: SingleChildScrollView(
              child: ItemView(
                item: item,
                idioma: 'ru',
                cadena: const ['es'],
                guiada: false,
                permitirReintento: false,
                onComprobado: (_, _) {},
                onContinuar: () {},
                mostrarRom: mostrar,
                onAlternarRom: alternar,
              ),
            ),
          ),
        );

    const elegir = Item(
      id: 'g1',
      formato: FormatoItem.elegir,
      consigna: TextoApoyo({'es': 'Elige el saludo'}),
      feedback: TextoApoyo({'es': 'Bien'}),
      opciones: [Opcion.meta('Привет'), Opcion.meta('Пока')],
      opcionesRom: ['Privét', 'Poká'],
      indiceRespuesta: 0,
    );

    testWidgets('bajo cada opción (N1–N2)', (tester) async {
      await tester.pumpWidget(app(elegir));
      expect(find.text('Privét'), findsOneWidget);
      expect(find.text('Poká'), findsOneWidget);
      expect(find.byType(BotonRomanizacion), findsNothing);
    });

    testWidgets('desde N3, oculta tras «Ver romanización»', (tester) async {
      var alternado = false;
      await tester.pumpWidget(
        app(elegir, mostrar: false, alternar: () => alternado = true),
      );
      expect(find.text('Privét'), findsNothing);
      await tester.tap(find.text('Ver romanización'));
      expect(alternado, isTrue);
    });

    testWidgets('texto, fichas y pares', (tester) async {
      await tester.pumpWidget(
        app(
          const Item(
            id: 'e4',
            formato: FormatoItem.ordenar,
            consigna: TextoApoyo({'es': 'Ordena'}),
            feedback: TextoApoyo({'es': 'Bien'}),
            tokens: ['Пока,', 'Анна!'],
            tokensRom: ['Poká,', 'Ánna!'],
            respuesta: 'Пока, Анна!',
          ),
        ),
      );
      expect(find.text('Ánna!'), findsOneWidget);

      await tester.pumpWidget(
        app(
          const Item(
            id: 'g2',
            formato: FormatoItem.completar,
            consigna: TextoApoyo({'es': 'Completa'}),
            feedback: TextoApoyo({'es': 'Bien'}),
            texto: 'Спасибо! — ___!',
            textoRom: 'Spasíbo! — ___!',
            respuesta: 'Пожалуйста',
          ),
        ),
      );
      expect(find.text('Spasíbo! — ___!'), findsOneWidget);

      await tester.pumpWidget(
        app(
          const Item(
            id: 'g3',
            formato: FormatoItem.relacionar,
            consigna: TextoApoyo({'es': 'Une'}),
            feedback: TextoApoyo({'es': 'Bien'}),
            pares: [
              ('привет', TextoApoyo({'es': 'hola'})),
              ('пока', TextoApoyo({'es': 'chao'})),
            ],
            paresRom: ['privét', 'poká'],
          ),
        ),
      );
      expect(find.text('privét'), findsOneWidget);
    });

    testWidgets(
      'en «escuchar» las opciones no la muestran antes de responder',
      (tester) async {
        await tester.pumpWidget(
          app(
            const Item(
              id: 'i2',
              formato: FormatoItem.escuchar,
              consigna: TextoApoyo({'es': 'Escucha y elige'}),
              feedback: TextoApoyo({'es': 'Bien'}),
              audio: 'пожалуйста',
              opciones: [Opcion.meta('пожалуйста'), Opcion.meta('спасибо')],
              opcionesRom: ['pozháluysta', 'spasíbo'],
              indiceRespuesta: 0,
            ),
          ),
        );
        expect(find.text('пожалуйста'), findsOneWidget);
        expect(find.text('pozháluysta'), findsNothing);
      },
    );
  });

  test('regla didáctica: visible hasta N2, oculta desde N3', () {
    expect(romVisiblePorDefecto(null), isTrue);
    expect(romVisiblePorDefecto(0), isTrue);
    expect(romVisiblePorDefecto(2), isTrue);
    expect(romVisiblePorDefecto(3), isFalse);
  });
}
