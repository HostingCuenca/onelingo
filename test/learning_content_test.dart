import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/biblioteca.dart';
import 'package:onelingo/core/content/learning_units.dart';
import 'package:onelingo/core/diagnostico.dart';

PreguntaDiag item(
  String id,
  int level, {
  String skill = 'gramatica',
  String passage = '',
}) => PreguntaDiag(
  id: id,
  nivel: level,
  skill: skill,
  tipo: TipoDiag.eleccion,
  tema: 'fixture',
  instruccion: 'Choose.',
  texto: 'A short passage.',
  opciones: const ['Yes', 'No'],
  correcta: 0,
  pasajeId: passage,
);

Map<String, dynamic> evidence(String type, int i, {bool supported = false}) => {
  'skill': 'comprension',
  'idioma': 'en',
  'tipo': type,
  'correcta': true,
  'primeraCorrecta': true,
  'intentos': 1,
  'fecha': '2026-09-${10 + i}',
  'primeraFecha': '2026-09-${10 + i}',
  'conApoyo': supported,
};

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('assets reales se cargan por el provider y conservan evidencia utilizable en 40 unidades', () async {
    final container = ProviderContainer();
    addTearDown(container.dispose);
    final allIds = <String>{};
    final passagesBySkill = <String, Set<String>>{};
    for (final skill in ['comprension', 'listening']) {
      final file = skill == 'listening' ? 'listening_units' : 'reading_units';
      final raw = jsonDecode(
        await rootBundle.loadString('assets/contenido/en/$file.json'),
      ) as Map;
      expect(raw['version'], 1);
      final units = await container.read(learningUnitsProvider(skill).future);
      expect(
        units,
        hasLength(20),
        reason: 'Debe cargarse el banco completo de $skill.',
      );
      passagesBySkill[skill] = units.map((u) => u.passage).toSet();
      expect(passagesBySkill[skill], hasLength(20));
      for (var level = 1; level <= 10; level++) {
        expect(
          units.where((u) => u.level == level),
          hasLength(2),
          reason: '$skill nivel $level',
        );
      }
      for (final unit in units) {
        expect(allIds.add(unit.id), isTrue, reason: 'ID duplicado ${unit.id}');
        expect(unit.objective.trim(), isNotEmpty);
        expect(unit.strategy.trim(), isNotEmpty);
        expect(unit.words, hasLength(4));
        for (final word in unit.words) {
          expect(
            unit.passage.toLowerCase(),
            contains(word.word.toLowerCase()),
            reason: '${unit.id}: vocabulario previo no contextualizado',
          );
          expect(word.translation.trim(), isNotEmpty);
          expect(word.example.trim(), isNotEmpty);
        }
        expect(unit.questions, hasLength(3));
        for (final question in unit.questions) {
          expect(
            allIds.add(question.id),
            isTrue,
            reason: 'ID duplicado ${question.id}',
          );
          expect(question.options, hasLength(4));
          expect(question.options.toSet(), hasLength(4));
          expect(question.answerIndex, inInclusiveRange(0, 3));
          expect(question.options[question.answerIndex].trim(), isNotEmpty);
          expect(question.explanation.trim(), isNotEmpty);
          expect(question.evidence.trim(), isNotEmpty);
          expect(
            unit.passage,
            contains(question.evidence),
            reason:
                '${question.id}: la devolución no debe citar evidencia ajena al texto',
          );
        }
      }
    }
    expect(
      passagesBySkill['comprension']!.intersection(
        passagesBySkill['listening']!,
      ),
      isEmpty,
      reason: 'No reutilizar una lectura ya vista como supuesta escucha independiente.',
    );
  });

  test('nivel manual no salta al vecino aunque todos sus ítems estén practicados', () {
    final bank = [item('low', 4), item('a', 5), item('b', 5), item('high', 6)];
    final practiced = {
      'a': {'correcta': true},
      'b': {'correcta': true},
    };
    final selected = RutaBiblioteca.seleccionar(
      banco: bank,
      nivel: 5,
      skill: 'gramatica',
      practicas: practiced,
      nivelFijo: true,
    );
    expect(selected.map((q) => q.id).toSet(), {'a', 'b'});
    expect(
      RutaBiblioteca.seleccionar(
        banco: bank,
        nivel: 8,
        skill: 'gramatica',
        nivelFijo: true,
      ),
      isEmpty,
      reason:
          'Un banco vacío no debe sustituir silenciosamente el nivel elegido.',
    );
  });

  test(
    'agrupar lectura por pasaje no reintroduce preguntas de otro nivel manual',
    () {
      final bank = [
        item('read-five-a', 5, skill: 'comprension', passage: 'shared-text'),
        item('read-five-b', 5, skill: 'comprension', passage: 'shared-text'),
        item('read-six', 6, skill: 'comprension', passage: 'shared-text'),
      ];
      final selected = RutaBiblioteca.seleccionar(
        banco: bank,
        nivel: 5,
        skill: 'comprension',
        nivelFijo: true,
      );
      expect(selected.map((q) => q.id).toSet(), {'read-five-a', 'read-five-b'});
    },
  );

  test('éxitos guiados y con apoyo no se convierten en ascenso automático', () {
    for (final type in ['practica_guiada', 'comprobacion_guiada']) {
      final attempts = {
        for (var i = 0; i < 4; i++) 'guided-$i': evidence(type, i),
      };
      expect(
        RutaBiblioteca.nivelSugerido('comprension', 5, null, attempts),
        5,
        reason: type,
      );
    }
    final withSupport = {
      for (var i = 0; i < 4; i++)
        'supported-$i': evidence('prueba', i, supported: true),
    };
    expect(
      RutaBiblioteca.nivelSugerido('comprension', 5, null, withSupport),
      5,
    );
    final independent = {
      for (var i = 0; i < 4; i++) 'fresh-$i': evidence('prueba', i),
    };
    expect(
      RutaBiblioteca.nivelSugerido('comprension', 5, null, independent),
      6,
      reason: 'La exclusión no debe desactivar toda adaptación.',
    );
  });

  test('aciertos guiados recientes no tapan primera evidencia independiente con errores', () {
    final attempts = <String, dynamic>{
      for (var i = 0; i < 3; i++)
        'independent-$i': {
          ...evidence('prueba', i),
          'correcta': true,
          'primeraCorrecta': false,
          'intentos': 2,
        },
      for (var i = 0; i < 4; i++)
        'guided-$i': evidence('comprobacion_guiada', i + 4),
    };
    expect(
      RutaBiblioteca.nivelSugerido('comprension', 5, null, attempts),
      4,
      reason: 'Repetir y memorizar no borra las dificultades independientes.',
    );
  });
}
