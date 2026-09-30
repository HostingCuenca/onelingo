import 'biblioteca_modelos.dart';

const exercisePools = [
  'teaching',
  'practiceGuided',
  'practice',
  'evaluation',
  'review',
];

class ExerciseSelection {
  const ExerciseSelection(this.selectionId, this.variants);
  final String selectionId;
  final List<ExerciseVariant> variants;
}

List<String> validateExerciseLibrary(ExerciseLibrary lib) {
  final errors = <String>[];
  final families = <String, ExerciseFamily>{};
  final variants = <String, String>{};
  for (final f in lib.families) {
    if (families.containsKey(f.id)) {
      errors.add('duplicate family ${f.id}');
    }
    if (f.revision < 1) {
      errors.add('invalid revision ${f.id}');
    }
    if (f.variants.isEmpty) {
      errors.add('family without variants ${f.id}');
    }
    families[f.id] = f;
    for (final v in f.variants) {
      if (variants.containsKey(v.id)) {
        errors.add('duplicate variant ${v.id}');
      }
      if (!v.id.startsWith('${f.id}:v${f.revision}:')) {
        errors.add('variant revision mismatch ${v.id}');
      }
      variants[v.id] = f.id;
    }
  }
  for (final e in lib.units.entries) {
    for (final p in e.value.pools.keys) {
      if (!exercisePools.contains(p)) {
        errors.add('unknown pool $p');
      }
    }
    final seen = <String, String>{};
    final seenVariants = <String>{};
    for (final p in exercisePools) {
      for (final id in e.value.pools[p] ?? const <String>[]) {
        final fid = id.split(':').first;
        if (!variants.containsKey(id)) {
          errors.add('unknown variant $id');
        } else if (variants[id] != fid) {
          errors.add('variant family mismatch $id');
        }
        if (!seenVariants.add(id)) {
          errors.add('duplicate pool reference $id');
        }
        if (seen.containsKey(fid) && seen[fid] != p) {
          errors.add('family exposed in ${seen[fid]} and $p');
        }
        seen[fid] = p;
      }
    }
  }
  return errors;
}

ExerciseSelection selectExercises(
  ExerciseLibrary lib, {
  required String unitId,
  required String pool,
  required int seed,
  int limit = 1,
  Set<String> excludedFamilies = const {},
}) {
  final unit = lib.units[unitId];
  if (unit == null) throw ArgumentError('unknown unit $unitId');
  if (!exercisePools.contains(pool)) throw ArgumentError('unknown pool');
  final allowed = (unit.pools[pool] ?? const <String>[])
      .where((id) => !excludedFamilies.contains(id.split(':').first))
      .toList();
  final byId = <String, ExerciseVariant>{
    for (final family in lib.families)
      for (final variant in family.variants) variant.id: variant,
  };
  final candidates = <ExerciseVariant>[];
  for (final id in allowed) {
    final variant = byId[id];
    if (variant != null) candidates.add(variant);
  }
  candidates.sort(
    (a, b) => _score(
      lib.version,
      unitId,
      pool,
      seed,
      a.id,
    ).compareTo(_score(lib.version, unitId, pool, seed, b.id)),
  );
  final selected = candidates
      .take(limit < 0 ? 0 : limit)
      .toList(growable: false);
  return ExerciseSelection(
    _hash(
      '${lib.version}|$unitId|$pool|$seed|${selected.map((v) => v.id).join(',')}',
    ).toRadixString(16).padLeft(8, '0'),
    selected,
  );
}

int _score(String v, String u, String p, int s, String id) =>
    _hash('$v|$u|$p|$s|$id');
int _hash(String input) {
  var h = 2166136261;
  for (final c in input.codeUnits) {
    h ^= c;
    // (h × primo) mod 2^31 por mitades: en la web los enteros son dobles y el
    // producto completo (> 2^53) perdería precisión y cambiaría la selección.
    final bajo = (h & 0xffff) * 16777619;
    final alto = (((h >> 16) * 16777619) & 0x7fff) << 16;
    h = (bajo + alto) & 0x7fffffff;
  }
  return h;
}
