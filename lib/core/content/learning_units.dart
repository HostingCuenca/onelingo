import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class LearningWord {
  const LearningWord(this.word, this.translation, this.example);
  final String word, translation, example;
}

class LearningQuestion {
  const LearningQuestion(
    this.id,
    this.prompt,
    this.options,
    this.answerIndex,
    this.explanation,
    this.evidence,
  );
  final String id, prompt, explanation, evidence;
  final List<String> options;
  final int answerIndex;
}

class LearningUnit {
  const LearningUnit(
    this.id,
    this.level,
    this.title,
    this.objective,
    this.strategy,
    this.passage,
    this.words,
    this.questions,
  );
  final String id, title, objective, strategy, passage;
  final int level;
  final List<LearningWord> words;
  final List<LearningQuestion> questions;
  factory LearningUnit.fromJson(Map<String, dynamic> j) => LearningUnit(
    j['id'] as String,
    j['nivel'] as int,
    j['title'] as String,
    j['objective'] as String,
    j['strategy'] as String,
    j['passage'] as String,
    [
      for (final w in j['vocabulary'] as List)
        LearningWord(w['word'], w['translation'], w['example']),
    ],
    [
      for (final q in j['questions'] as List)
        LearningQuestion(
          q['id'],
          q['prompt'],
          List<String>.from(q['options']),
          q['answerIndex'],
          q['explanation'],
          q['evidence'],
        ),
    ],
  );
}

final learningUnitsProvider = FutureProvider.family<List<LearningUnit>, String>(
  (ref, skill) async {
    final file = skill == 'listening' ? 'listening_units' : 'reading_units';
    final data = jsonDecode(
      await rootBundle.loadString('assets/contenido/en/$file.json'),
    ) as Map<String, dynamic>;
    return [
      for (final j in data['units'] as List)
        LearningUnit.fromJson(Map<String, dynamic>.from(j)),
    ];
  },
);
