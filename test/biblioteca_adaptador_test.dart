import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/biblioteca_adaptador.dart';
import 'package:onelingo/core/aprendizaje/biblioteca_modelos.dart';
import 'package:onelingo/core/aprendizaje/correccion.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';

void main() {
  ExerciseVariant variant(String format, Map<String, dynamic> answer) =>
      ExerciseVariant(
        id: 'ex.u:v1:practice',
        format: format,
        prompt: const {'es': 'Elige'},
        answer: answer,
        choices: const [
          {'text': 'hello'},
        ],
        teaches: const [],
        requires: const [],
        origin: const {},
        contentHash: 'sha256:x',
      );

  test('adapta formatos y respuesta sin cambiar el id estable', () {
    final item = itemDesdeVariante(variant('choice', {'index': 0}));
    expect(item.id, 'ex.u:v1:practice');
    expect(item.formato.name, 'elegir');
    expect(item.indiceRespuesta, 0);
  });

  test('conserva imagen editorial opcional y texto alternativo', () {
    final base = variant('choice', {'index': 0});
    final visual = ExerciseVariant(
      id: base.id,
      format: base.format,
      prompt: base.prompt,
      answer: base.answer,
      choices: base.choices,
      teaches: base.teaches,
      requires: base.requires,
      origin: const {
        'imageAsset': 'assets/img/educacion/en/location-under.webp',
        'imageAlt': 'Una pelota debajo de una mesa.',
      },
      contentHash: base.contentHash,
    );

    final item = itemDesdeVariante(visual);
    expect(item.imagen, 'assets/img/educacion/en/location-under.webp');
    expect(item.imagenAlt, 'Una pelota debajo de una mesa.');
  });

  test('adapta el umbral parcial de un ejercicio de relacionar', () {
    final base = variant('match', {
      'pairs': [
        [
          'want',
          {'es': 'to save'},
        ],
        [
          'need',
          {'es': 'to call'},
        ],
      ],
    });
    final matching = ExerciseVariant(
      id: base.id,
      format: base.format,
      prompt: base.prompt,
      answer: base.answer,
      choices: base.choices,
      teaches: base.teaches,
      requires: base.requires,
      origin: const {
        'pairs': [
          [
            'want',
            {'es': 'to save'},
          ],
          [
            'need',
            {'es': 'to call'},
          ],
        ],
        'scoring': {'total': 6, 'minimumCorrect': 5},
      },
      contentHash: base.contentHash,
    );

    final item = itemDesdeVariante(matching);
    expect(item.partesPuntuables, 6);
    expect(item.minimoCorrectas, 5);
  });

  test('adapta completar multiparte con variantes aceptadas', () {
    final base = variant('fill', {
      'text': 'was walking / started | were waiting / arrived',
      'accepted': ['was walking / started | were waiting / arrived'],
      'parts': [
        {
          'text': 'was walking / started',
          'accepted': ['was walking / started', 'was walking; started'],
        },
        {
          'text': 'were waiting / arrived',
          'accepted': ['were waiting / arrived'],
        },
      ],
    });
    final multipart = ExerciseVariant(
      id: base.id,
      format: base.format,
      prompt: base.prompt,
      answer: base.answer,
      choices: base.choices,
      teaches: base.teaches,
      requires: base.requires,
      origin: const {
        'sentences': [
          'I ___ home when the rain ___.',
          'They ___ outside when the bus ___.',
        ],
        'scoring': {
          'parts': 2,
          'minimumCorrect': 1,
          'requiredParts': [1],
        },
      },
      contentHash: base.contentHash,
    );

    final item = itemDesdeVariante(multipart);
    expect(item.textosPartes, hasLength(2));
    expect(item.respuestasPartes[0], [
      'was walking / started',
      'was walking; started',
    ]);
    expect(item.partesPuntuables, 2);
    expect(item.minimoCorrectas, 1);
    expect(item.partesObligatorias, [1]);
  });

  test('adapta y aplica rúbrica determinista de escritura extensa', () {
    final base = variant('write', {
      'text': 'A complete model answer.',
      'accepted': ['A complete model answer.'],
    });
    final writing = ExerciseVariant(
      id: base.id,
      format: base.format,
      prompt: base.prompt,
      answer: base.answer,
      choices: base.choices,
      teaches: base.teaches,
      requires: base.requires,
      origin: const {
        'text': 'Write a short study plan.',
        'scoring': {
          'wordRange': [8, 14],
          'evidenceGroups': [
            ['my goal is', 'my aim is'],
            ['two weeks', 'fourteen days'],
            ['dated answer sheets', 'dated records'],
          ],
        },
      },
      contentHash: base.contentHash,
    );

    final item = itemDesdeVariante(writing);
    expect(item.minimoPalabras, 8);
    expect(item.maximoPalabras, 14);
    expect(item.evidenciasEscritura, hasLength(3));
    expect(
      corregir(
        item,
        'My aim is progress in fourteen days with dated records.',
        'en',
      ),
      isTrue,
    );
    expect(
      corregir(item, 'My aim is progress in fourteen days.', 'en'),
      isFalse,
    );
  });

  test('Item.fromJson conserva el contrato multiparte legado', () {
    final item = Item.fromJson({
      'id': 'legacy.multipart',
      'formato': 'completar',
      'consigna': {'es': 'Completa ambas.'},
      'feedback': {'es': 'Revisa las decisiones.'},
      'textosPartes': ['Primera: ___', 'Segunda: ___'],
      'respuestasPartes': [
        ['one'],
        ['two', 'second'],
      ],
      'partesPuntuables': 2,
      'minimoCorrectas': 1,
      'partesObligatorias': [1],
    });

    expect(item.textosPartes, ['Primera: ___', 'Segunda: ___']);
    expect(item.respuestasPartes[1], ['two', 'second']);
    expect(item.partesObligatorias, [1]);
  });

  test('normaliza barras con o sin espacios de la misma forma', () {
    expect(
      normalizar('was walking/started'),
      normalizar('was walking / started'),
    );
  });

  test('legacy es seguro por defecto y shadow conserva diagnóstico', () async {
    const activation = ActivacionBiblioteca();
    final result = await CargadorBiblioteca().diagnostico(
      'en',
      'u',
      activation,
    );
    expect(result.activacion, EstadoBiblioteca.legacy);
    expect(result.aplicaAlAlumno, isFalse);
  });

  test('distingue biblioteca ausente de inválida', () async {
    final bundle = TestAssetBundle({
      CargadorBiblioteca.asset('bad'): '{not json',
    });
    final loader = CargadorBiblioteca(bundle: bundle);
    expect(
      (await loader.cargar('missing')).estado,
      EstadoCargaBiblioteca.ausente,
    );
    expect((await loader.cargar('bad')).estado, EstadoCargaBiblioteca.invalida);
  });

  test('active exige review y shadow nunca sustituye la ruta', () async {
    final bundle = TestAssetBundle({
      CargadorBiblioteca.asset('en'): '''
        {"schema":"exercise-library/1","libraryId":"x","version":"1","course":"en",
         "units":{"u":{"concepts":[],"skills":[],"prerequisites":[],"pools":{}}},
         "families":[]}
      ''',
    });
    final loader = CargadorBiblioteca(bundle: bundle);
    final shadow = await loader.diagnostico(
      'en',
      'u',
      const ActivacionBiblioteca(porUnidad: {'u': EstadoBiblioteca.shadow}),
    );
    expect(shadow.validaEnSombra, isTrue);
    expect(shadow.aplicaAlAlumno, isFalse);
    final active = await loader.diagnostico(
      'en',
      'u',
      const ActivacionBiblioteca(porUnidad: {'u': EstadoBiblioteca.active}),
    );
    expect(active.aplicaAlAlumno, isFalse);
    expect(active.errores.single, contains('without editorial review'));
  });
}

class TestAssetBundle extends CachingAssetBundle {
  TestAssetBundle(this.assets);
  final Map<String, String> assets;

  @override
  Future<ByteData> load(String key) async {
    final value = assets[key];
    if (value == null) throw StateError('missing $key');
    final bytes = Uint8List.fromList(utf8.encode(value));
    return ByteData.sublistView(bytes);
  }
}
