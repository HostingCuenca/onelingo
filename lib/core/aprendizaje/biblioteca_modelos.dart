/// Modelos aislados para el contrato `exercise-library/1`.
class ExerciseLibrary {
  const ExerciseLibrary({
    required this.libraryId,
    required this.version,
    required this.course,
    required this.units,
    required this.families,
  });
  final String libraryId, version, course;
  final Map<String, ExerciseUnit> units;
  final List<ExerciseFamily> families;
  factory ExerciseLibrary.fromJson(Map<String, dynamic> json) {
    if (json['schema'] != 'exercise-library/1') throw FormatException('schema');
    final rawUnits = json['units'];
    final rawFamilies = json['families'];
    if (rawUnits is! Map || rawFamilies is! List) {
      throw const FormatException('units/families');
    }
    return ExerciseLibrary(
      libraryId: _required(json, 'libraryId'),
      version: _required(json, 'version'),
      course: _required(json, 'course'),
      units: rawUnits.map(
        (k, v) => MapEntry(
          k.toString(),
          ExerciseUnit.fromJson(Map<String, dynamic>.from(v as Map)),
        ),
      ),
      families: rawFamilies
          .map(
            (v) => ExerciseFamily.fromJson(Map<String, dynamic>.from(v as Map)),
          )
          .toList(growable: false),
    );
  }
}

class ExerciseUnit {
  const ExerciseUnit({
    required this.concepts,
    required this.skills,
    required this.prerequisites,
    required this.pools,
  });
  final List<String> concepts, skills, prerequisites;
  final Map<String, List<String>> pools;
  factory ExerciseUnit.fromJson(Map<String, dynamic> j) => ExerciseUnit(
    concepts: _strings(j['concepts']),
    skills: _strings(j['skills']),
    prerequisites: _strings(j['prerequisites']),
    pools: (j['pools'] as Map? ?? {}).map(
      (k, v) => MapEntry(k.toString(), _strings(v)),
    ),
  );
}

class ExerciseFamily {
  const ExerciseFamily({
    required this.id,
    required this.revision,
    required this.concepts,
    required this.skills,
    required this.variants,
  });
  final String id;
  final int revision;
  final List<String> concepts, skills;
  final List<ExerciseVariant> variants;
  factory ExerciseFamily.fromJson(Map<String, dynamic> j) => ExerciseFamily(
    id: _required(j, 'id'),
    revision: (j['revision'] as num?)?.toInt() ?? 0,
    concepts: _strings(j['concepts']),
    skills: _strings(j['skills']),
    variants: ((j['variants'] as List?) ?? [])
        .map(
          (v) => ExerciseVariant.fromJson(Map<String, dynamic>.from(v as Map)),
        )
        .toList(growable: false),
  );
}

class ExerciseVariant {
  const ExerciseVariant({
    required this.id,
    required this.format,
    required this.prompt,
    required this.answer,
    required this.choices,
    required this.teaches,
    required this.requires,
    required this.origin,
    required this.contentHash,
  });
  final String id, format, contentHash;
  final Map<String, String> prompt;
  final Map<String, dynamic> answer;
  final List<Map<String, dynamic>> choices;
  final List<String> teaches, requires;
  final Map<String, dynamic> origin;
  factory ExerciseVariant.fromJson(Map<String, dynamic> j) => ExerciseVariant(
    id: _required(j, 'id'),
    format: _required(j, 'format'),
    prompt: (j['prompt'] as Map? ?? {}).map(
      (k, v) => MapEntry(k.toString(), v.toString()),
    ),
    answer: Map<String, dynamic>.from((j['answer'] as Map?) ?? {}),
    choices: ((j['choices'] as List?) ?? [])
        .map((v) => Map<String, dynamic>.from(v as Map))
        .toList(growable: false),
    teaches: _strings(j['teaches']),
    requires: _strings(j['requires']),
    origin: Map<String, dynamic>.from((j['origin'] as Map?) ?? {}),
    contentHash: _required(j, 'contentHash'),
  );
}

String _required(Map<String, dynamic> j, String key) {
  final v = j[key];
  if (v is! String || v.isEmpty) throw FormatException('missing $key');
  return v;
}

List<String> _strings(Object? value) => value is List
    ? value.whereType<String>().toList(growable: false)
    : const [];
