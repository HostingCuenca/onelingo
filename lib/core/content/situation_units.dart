import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

final situationUnitsProvider = FutureProvider<List<SituationUnit>>((ref) async {
  final sources = await Future.wait([
    rootBundle.loadString('assets/contenido/en/situaciones.json'),
    rootBundle.loadString('assets/contenido/en/situational_vocabulary.json'),
  ]);
  final base = jsonDecode(sources[0]) as List;
  final expanded = (jsonDecode(sources[1]) as Map)['situations'] as List;
  return base.map((j) {
    final matching = expanded.where((e) => e['situacionId'] == j['id']);
    final extra = matching.isEmpty ? null : matching.single as Map;
    return SituationUnit.fromJson(Map<String, dynamic>.from(j), extra: extra);
  }).toList();
});

class SituationObjective {
  const SituationObjective(this.id, this.title, this.phrase, this.translation);
  final String id, title, phrase, translation;
}

class SituationUnit {
  const SituationUnit(
    this.id,
    this.name,
    this.words,
    this.objectives, {
    this.vocabulary = const [],
    this.patterns = const [],
  });
  final List<SituationWord> vocabulary;
  final List<SituationPattern> patterns;
  final int id;
  final String name;
  final List<(String, String)> words;
  final List<SituationObjective> objectives;
  factory SituationUnit.fromJson(Map<String, dynamic> j, {Map? extra}) =>
      SituationUnit(
        j['id'] as int,
        j['nombre'] as String,
        [
          for (final w in j['vocabulario'] as List)
            (w['en'] as String, w['es'] as String),
          for (final w in extra?['vocabulary'] as List? ?? [])
            (w['en'] as String, w['es'] as String),
        ],
        [
          for (final o in j['objetivos'] as List)
            SituationObjective(
              o['id'],
              o['titulo'],
              o['frase'],
              o['traduccion'],
            ),
        ],
        vocabulary: [
          for (final w in extra?['vocabulary'] as List? ?? [])
            SituationWord.fromJson(w),
        ],
        patterns: [
          for (final p in extra?['patterns'] as List? ?? [])
            SituationPattern.fromJson(p),
        ],
      );
}

class SituationWord {
  const SituationWord(
    this.en,
    this.es,
    this.example,
    this.category,
    this.level,
  );
  final String en, es, example, category;
  final int level;
  factory SituationWord.fromJson(Map j) => SituationWord(
    j['en'],
    j['es'],
    j['example'],
    j['category'],
    j['nivelInicial'],
  );
}

class SituationPattern {
  const SituationPattern(
    this.template,
    this.translation,
    this.examples, {
    this.note = '',
  });
  final String note;
  final String template, translation;
  final List<(String, String)> examples;
  factory SituationPattern.fromJson(Map j) =>
      SituationPattern(j['template'], j['translation'], [
        for (final e in j['examples'] as List)
          (e['en'] as String, e['es'] as String),
      ], note: j['note'] as String? ?? '');
}

/// A conversation is evidence of practice, never an automatic pass.
List<Map> situationEvidence(Map<String, dynamic> practices, int id) =>
    practices.values
        .whereType<Map>()
        .where((e) => e['situacionId'] == id && e['idioma'] == 'en')
        .toList()
      ..sort((a, b) => '${b['fecha']}'.compareTo('${a['fecha']}'));

/// Continue recent evidence first; otherwise use explicit personal goals.
int suggestedSituation(Map<String, dynamic> practices, List<String> goals) {
  final recent =
      practices.values
          .whereType<Map>()
          .where(
            (e) =>
                e['idioma'] == 'en' &&
                e['situacionId'] is int &&
                e['situacionId'] >= 1 &&
                e['situacionId'] <= 50,
          )
          .toList()
        ..sort((a, b) => '${b['fecha']}'.compareTo('${a['fecha']}'));
  if (recent.isNotEmpty) return recent.first['situacionId'] as int;
  for (final goal in goals) {
    final id = {
      'entrevistas': 20,
      'trabajar': 23,
      'viajar': 7,
      'estudiar': 35,
      'clientes': 25,
      'conversar': 44,
    }[goal];
    if (id != null) return id;
  }
  return 1;
}
