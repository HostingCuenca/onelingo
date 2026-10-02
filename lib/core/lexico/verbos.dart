import 'dart:convert';
import 'dart:math';

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../i18n/i18n.dart';
import '../state/providers.dart';

/// «Mis verbos» (fase D): tablas de conjugación por idioma, generadas desde
/// `tools/contenido/verbos/verbos-<idioma>.json`. El esquema es el mismo para
/// todos los idiomas (personas, tiempos y una tabla por tiempo).

class Persona {
  const Persona(this.meta, this.es);

  /// Pronombre en el idioma meta (je, I…) y su traducción ya resuelta al
  /// idioma de la interfaz (el campo se llama `es` por historia).
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
    required this.resumen,
    required this.formas,
    required this.tablas,
    required this.ejemploMeta,
    required this.ejemploEs,
  });

  /// [es] y [ejemploEs]: traducciones en el idioma de la interfaz.
  final String id, infinitivo, es, ejemploMeta, ejemploEs;
  final bool irregular;
  final int nivel;

  /// Formas clave para recordar (go · went · gone; aller · vais · allé).
  final List<String> resumen;

  /// Formas sueltas por nombre (inglés: tercera, pasado, participio, gerundio).
  final Map<String, String> formas;
  final Map<String, List<String>> tablas;
}

class Verbos {
  const Verbos(
    this.idioma,
    this.personas,
    this.tiempos,
    this.verbos, {
    this.etiquetaResumen = '',
  });
  final String idioma;
  final List<Persona> personas;
  final List<Tiempo> tiempos;
  final List<Verbo> verbos;
  final String etiquetaResumen;

  Verbo? porId(String id) {
    for (final v in verbos) {
      if (v.id == id) return v;
    }
    return null;
  }

  /// Pronombre + forma. En francés «je» se apostrofa ante vocal o h muda.
  String conPronombre(int persona, String forma) {
    final p = personas[persona].meta.split(' /').first;
    if (idioma == 'fr' &&
        p == 'je' &&
        RegExp(r'^[aeiouyàâéèêëîïôûh]', caseSensitive: false).hasMatch(forma)) {
      return 'j’$forma';
    }
    return '$p $forma';
  }

  /// [j] ya pasó por `localizarApoyo` (textos de apoyo resueltos).
  factory Verbos.fromJson(Map<String, dynamic> j) => Verbos(
    j['idioma'] as String,
    [
      for (final p in j['personas'] as List)
        Persona(p['meta'] as String, p['traduccion'] as String),
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
          es: v['traduccion'] as String,
          irregular: v['tipo'] == 'irregular',
          nivel: (v['nivel'] as num).toInt(),
          resumen: List<String>.from(v['resumen'] as List),
          formas: Map<String, String>.from(v['formas'] as Map),
          tablas: {
            for (final e in (v['tablas'] as Map).entries)
              '${e.key}': List<String>.from(e.value as List),
          },
          ejemploMeta: v['ejemplo']['meta'] as String,
          ejemploEs: v['ejemplo']['traduccion'] as String,
        ),
    ],
    etiquetaResumen: (j['etiquetaResumen'] as String?) ?? '',
  );
}

/// Verbos del idioma, con los textos de apoyo en el idioma de la interfaz;
/// null si el idioma aún no tiene.
final verbosProvider = FutureProvider.family<Verbos?, String>((
  ref,
  idioma,
) async {
  final interfaz = ref.watch(progressProvider.select((s) => s.interfaz));
  final String raw;
  try {
    raw = await rootBundle.loadString('assets/contenido/$idioma/verbos.json');
  } catch (_) {
    return null;
  }
  return Verbos.fromJson(
    localizarApoyo(jsonDecode(raw), interfaz) as Map<String, dynamic>,
  );
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

/// Pregunta con la tabla (idiomas con conjugación rica, como el francés):
/// «parler · présent · nous ___» y como distractores las formas de otras
/// personas y otros tiempos del mismo verbo.
PreguntaVerbo? preguntaTabla(Verbos vs, Verbo v, Random rnd) {
  final tiempos = [
    for (final t in vs.tiempos)
      if ((v.tablas[t.id] ?? const []).length == vs.personas.length) t,
  ];
  if (tiempos.isEmpty) return null;
  final t = tiempos[rnd.nextInt(tiempos.length)];
  final persona = rnd.nextInt(vs.personas.length);
  final correcta = v.tablas[t.id]![persona];
  final otras = {
    for (final x in v.tablas[t.id]!) x,
    for (final tt in tiempos) v.tablas[tt.id]![persona],
  }.where((x) => x != correcta).toList()..shuffle(rnd);
  if (otras.length < 2) return null;
  final opciones = [correcta, ...otras.take(3)]..shuffle(rnd);
  return PreguntaVerbo(
    v,
    tr('«{verbo}» ({significado}) · {tiempo}: {persona} ___', {
      'verbo': v.infinitivo,
      'significado': v.es,
      'tiempo': t.nombre,
      'persona': vs.personas[persona].meta,
    }),
    opciones,
    opciones.indexOf(correcta),
    vs.conPronombre(persona, correcta),
  );
}

PreguntaVerbo? preguntaVerbo(Verbo v, int tipo, Random rnd) {
  final f = v.formas;
  final (enunciado, correcta, explicacion) = switch (tipo % 3) {
    0 => (
      tr('Pasado de «{verbo}» ({significado})', {
        'verbo': v.infinitivo,
        'significado': v.es,
      }),
      f['pasado']!,
      '${tr('{verbo} → {forma} (pasado).', {'verbo': v.infinitivo, 'forma': f['pasado']})} '
          '${v.irregular ? tr('Es irregular: hay que aprenderlo.') : tr('Es regular: termina en -ed.')}',
    ),
    1 => (
      tr('Participio de «{verbo}»: I have ___', {'verbo': v.infinitivo}),
      f['participio']!,
      tr('I have {forma}. El participio va con have/has.', {
        'forma': f['participio'],
      }),
    ),
    _ => (
      'He ___ (${v.infinitivo}) every day.',
      f['tercera']!,
      tr('Con he, she o it el presente lleva -s: {forma}.', {
        'forma': f['tercera'],
      }),
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
  Verbos vs,
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
      // Inglés: pasado, participio y -s; el resto, con la tabla.
      ?(orden[i].formas.containsKey('pasado')
          ? preguntaVerbo(orden[i], i, rnd)
          : preguntaTabla(vs, orden[i], rnd)),
  ];
}
