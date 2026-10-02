import 'dart:convert';
import 'dart:math';

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// «Mis verbos» (fase D): tablas de conjugación por idioma, generadas desde
/// `tools/contenido/verbos/verbos-<idioma>.json`. El esquema es el mismo para
/// todos los idiomas (personas, tiempos y una tabla por tiempo).

class Persona {
  const Persona(this.meta, this.es);
  final String meta, es;
}

class Tiempo {
  const Tiempo(this.id, this.nombre, this.uso);
  final String id, nombre, uso;
}

class Verbo {
  const Verbo({
    required this.id,
    required this.infinitivo,
    required this.es,
    required this.irregular,
    required this.nivel,
    required this.formas,
    required this.tablas,
    required this.ejemploMeta,
    required this.ejemploEs,
  });
  final String id, infinitivo, es, ejemploMeta, ejemploEs;
  final bool irregular;
  final int nivel;

  /// tercera, pasado, participio, gerundio (según el idioma).
  final Map<String, String> formas;
  final Map<String, List<String>> tablas;
}

class Verbos {
  const Verbos(this.idioma, this.personas, this.tiempos, this.verbos);
  final String idioma;
  final List<Persona> personas;
  final List<Tiempo> tiempos;
  final List<Verbo> verbos;

  Verbo? porId(String id) {
    for (final v in verbos) {
      if (v.id == id) return v;
    }
    return null;
  }

  factory Verbos.fromJson(Map<String, dynamic> j) {
    final meta = j['idioma'] as String;
    return Verbos(
      meta,
      [
        for (final p in j['personas'] as List)
          Persona(p[meta] as String, p['es'] as String),
      ],
      [
        for (final t in j['tiempos'] as List)
          Tiempo(t['id'] as String, t['nombre'] as String, t['uso'] as String),
      ],
      [
        for (final v in j['verbos'] as List)
          Verbo(
            id: v['id'] as String,
            infinitivo: v['infinitivo'] as String,
            es: v['es'] as String,
            irregular: v['tipo'] == 'irregular',
            nivel: (v['nivel'] as num).toInt(),
            formas: Map<String, String>.from(v['formas'] as Map),
            tablas: {
              for (final e in (v['tablas'] as Map).entries)
                '${e.key}': List<String>.from(e.value as List),
            },
            ejemploMeta: v['ejemplo'][meta] as String,
            ejemploEs: v['ejemplo']['es'] as String,
          ),
      ],
    );
  }
}

/// Verbos del idioma; null si aún no tiene.
final verbosProvider = FutureProvider.family<Verbos?, String>((
  ref,
  idioma,
) async {
  final String raw;
  try {
    raw = await rootBundle.loadString('assets/contenido/$idioma/verbos.json');
  } catch (_) {
    return null;
  }
  return Verbos.fromJson(jsonDecode(raw) as Map<String, dynamic>);
});

// --- Práctica ---------------------------------------------------------------

class PreguntaVerbo {
  const PreguntaVerbo(this.verbo, this.enunciado, this.opciones, this.correcta,
      this.explicacion);
  final Verbo verbo;
  final String enunciado, explicacion;
  final List<String> opciones;
  final int correcta;
}

/// Formas equivocadas típicas: regularizar un irregular (goed), confundir
/// pasado y participio, olvidar la -s.
List<String> _distractores(Verbo v, String correcta) {
  final f = v.formas;
  final inf = v.infinitivo;
  final regular = inf.endsWith('e') ? '${inf}d' : '${inf}ed';
  return {
    regular,
    f['pasado']!,
    f['participio']!,
    f['tercera']!,
    inf,
    f['gerundio']!,
  }.where((x) => x != correcta).toList();
}

PreguntaVerbo? preguntaVerbo(Verbo v, int tipo, Random rnd) {
  final f = v.formas;
  final (enunciado, correcta, explicacion) = switch (tipo % 3) {
    0 => (
      'Pasado de «${v.infinitivo}» (${v.es})',
      f['pasado']!,
      '${v.infinitivo} → ${f['pasado']} (pasado). ${v.irregular ? 'Es irregular: hay que aprenderlo.' : 'Es regular: termina en -ed.'}',
    ),
    1 => (
      'Participio de «${v.infinitivo}»: I have ___',
      f['participio']!,
      'I have ${f['participio']}. El participio va con have/has.',
    ),
    _ => (
      'He ___ (${v.infinitivo}) every day.',
      f['tercera']!,
      'Con he, she o it el presente lleva -s: ${f['tercera']}.',
    ),
  };
  final otras = _distractores(v, correcta)..shuffle(rnd);
  if (otras.length < 2) return null;
  final opciones = [correcta, ...otras.take(3)]..shuffle(rnd);
  return PreguntaVerbo(
    v,
    enunciado,
    opciones,
    opciones.indexOf(correcta),
    explicacion,
  );
}

/// 10 preguntas de verbos del nivel del alumno (los irregulares pesan más:
/// son los que hay que memorizar).
List<PreguntaVerbo> preguntasVerbos(
  List<Verbo> disponibles,
  Random rnd, {
  int n = 10,
}) {
  final irregulares = [
    for (final v in disponibles)
      if (v.irregular) v,
  ]..shuffle(rnd);
  final regulares = [
    for (final v in disponibles)
      if (!v.irregular) v,
  ]..shuffle(rnd);
  final orden = [...irregulares.take(7), ...regulares.take(3)];
  if (orden.length < n) {
    orden.addAll(
      [...irregulares.skip(7), ...regulares.skip(3)].take(n - orden.length),
    );
  }
  orden.shuffle(rnd);
  return [
    for (var i = 0; i < orden.length; i++)
      ?preguntaVerbo(orden[i], i, rnd),
  ];
}
