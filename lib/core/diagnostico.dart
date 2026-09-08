import 'dart:convert';
import 'dart:math';

import 'package:flutter/services.dart' show rootBundle;

import 'content/curriculum.dart';
import 'content/idiomas.dart' show soloNativo;
import 'voz.dart' show similitud;
import 'models/models.dart';
import 'placement.dart';

/// Diagnóstico adaptativo de nivel (1-10 con medios puntos) por competencias.
///
/// No es un cuestionario fijo: parte del nivel que declara el alumno, mide
/// una competencia distinta en cada pregunta, sube o baja la dificultad según
/// las respuestas (nunca más de un nivel por respuesta), incluye al final una
/// producción escrita que evalúa la IA y termina con un perfil: nivel estimado,
/// equivalencia MCER, puntuación por competencia, fortalezas, debilidades,
/// temas a reforzar y un plan inicial.
///
/// Banco de preguntas: `assets/contenido/<idioma>/diagnostico.json`
/// (semilla `tools/contenido/semilla/<idioma>-diagnostico.txt`).

/// Tipos de pregunta: elegir, la más natural, significado de una expresión,
/// comprensión de un texto corto, situación cotidiana, detectar el error,
/// completar (escribir la palabra), respuesta corta, escuchar y elegir,
/// escuchar y escribir (dictado) y producción escrita.
enum TipoDiag { eleccion, natural, significado, contexto, situacion, error, completar, corta, escucha, dictado, escritura }

const tiposDiagNombre = {
  TipoDiag.eleccion: 'Elige', TipoDiag.natural: 'La más natural', TipoDiag.significado: 'Significado', TipoDiag.contexto: 'Comprensión',
  TipoDiag.situacion: 'Situación', TipoDiag.error: 'Detecta el error', TipoDiag.completar: 'Completa', TipoDiag.corta: 'Respuesta corta',
  TipoDiag.escucha: 'Escucha', TipoDiag.dictado: 'Dictado', TipoDiag.escritura: 'Escribe',
};

const skillsDiag = {
  'comprension': 'Comprensión',
  'vocabulario': 'Vocabulario',
  'gramatica': 'Gramática',
  'tiempos': 'Tiempos verbales',
  'expresiones': 'Expresiones naturales',
  'contexto': 'Comprensión contextual',
  'cotidiano': 'Comunicación cotidiana',
  'escritura': 'Escritura',
};

class PreguntaDiag {
  const PreguntaDiag({
    required this.nivel,
    required this.skill,
    required this.tipo,
    required this.tema,
    required this.instruccion,
    required this.texto,
    this.opciones = const [],
    this.correcta = -1,
    this.aceptadas = const [],
    this.explicacion = '',
  });
  final int nivel; // 0..10
  final String skill;
  final TipoDiag tipo;
  final String tema; // p. ej. "third conditional": alimenta el plan de refuerzo
  final String instruccion;
  final String texto;
  final List<String> opciones; // con la correcta en `correcta` (índice)
  final int correcta;
  final List<String> aceptadas; // completar / respuesta corta
  final String explicacion;

  bool get conOpciones => opciones.isNotEmpty;
  bool get esEscritura => tipo == TipoDiag.escritura;
  /// El texto se escucha y no se muestra hasta responder.
  bool get esAuditiva => tipo == TipoDiag.escucha || tipo == TipoDiag.dictado;
  String get respuestaCorrecta => conOpciones ? opciones[correcta] : (aceptadas.isEmpty ? '' : aceptadas.first);
  String get clave => '$nivel|$skill|$texto';

  static PreguntaDiag fromJson(Map<String, dynamic> j) => PreguntaDiag(
        nivel: j['nivel'] as int,
        skill: j['skill'] as String,
        tipo: TipoDiag.values.firstWhere((t) => t.name == j['tipo'], orElse: () => TipoDiag.eleccion),
        tema: j['tema'] as String? ?? '',
        instruccion: j['instruccion'] as String? ?? '',
        texto: j['texto'] as String,
        opciones: ((j['opciones'] as List?) ?? []).cast<String>(),
        correcta: j['correcta'] as int? ?? -1,
        aceptadas: ((j['aceptadas'] as List?) ?? []).cast<String>(),
        explicacion: j['explicacion'] as String? ?? '',
      );

  /// Copia con las opciones barajadas (la correcta se sigue de `correcta`).
  PreguntaDiag barajada(Random rnd) {
    if (!conOpciones) return this;
    final correctaTexto = opciones[correcta];
    final ops = [...opciones]..shuffle(rnd);
    return PreguntaDiag(nivel: nivel, skill: skill, tipo: tipo, tema: tema, instruccion: instruccion, texto: texto, opciones: ops, correcta: ops.indexOf(correctaTexto), aceptadas: aceptadas, explicacion: explicacion);
  }

  /// Pregunta de opción múltiple a partir de un paso de lección (banco de respaldo).
  static PreguntaDiag desdePaso(LessonStep s, int nivel) => PreguntaDiag(
        nivel: nivel,
        skill: switch (s.skill) { Skill.vocabulario => 'vocabulario', Skill.frases => 'expresiones', Skill.gramatica => 'gramatica', _ => 'comprension' },
        tipo: TipoDiag.eleccion,
        tema: s.hint.isEmpty ? 'repaso del nivel $nivel' : s.hint,
        instruccion: 'Elige la opción correcta.',
        texto: s.prompt,
        opciones: s.options,
        correcta: s.options.indexOf(s.answer).clamp(0, s.options.length - 1),
      );
}

/// Banco de preguntas por idioma.
class BancoDiag {
  BancoDiag._();
  static final Map<String, List<PreguntaDiag>> _cache = {};
  static final Set<String> _intentado = {};

  static Future<void> precargar(String idioma) async {
    if (_intentado.contains(idioma)) return;
    _intentado.add(idioma);
    try {
      final raw = await rootBundle.loadString('assets/contenido/$idioma/diagnostico.json');
      final j = jsonDecode(raw) as Map<String, dynamic>;
      _cache[idioma] = [for (final q in (j['preguntas'] as List)) PreguntaDiag.fromJson(q as Map<String, dynamic>)];
    } catch (_) {}
  }

  static bool disponible(String idioma) => (_cache[idioma]?.isNotEmpty) ?? false;

  /// Preguntas sembradas del idioma; si no hay, se construyen desde las lecciones.
  static List<PreguntaDiag> de(String idioma) {
    final s = _cache[idioma];
    if (s != null && s.isNotEmpty) return s;
    return [
      for (var n = 0; n <= 10; n++)
        for (final p in PruebaNivel.bancoNivel(n).take(12)) PreguntaDiag.desdePaso(p, n)
    ];
  }
}

class RespuestaDiag {
  RespuestaDiag({required this.pregunta, required this.respuesta, required this.correcta, this.puntuacion});
  final PreguntaDiag pregunta;
  final String respuesta;
  final bool correcta;
  final double? puntuacion; // escritura: 1-10 dado por la IA
}

/// Evaluación de la producción escrita (IA o heurística local).
class EvaluacionEscritura {
  const EvaluacionEscritura({required this.puntuacion, this.correccion = '', this.comentario = '', this.errores = const [], this.porIa = true});
  final double puntuacion; // 1-10
  final String correccion;
  final String comentario;
  final List<String> errores; // temas detectados, p. ej. "ortografía", "puntuación"
  final bool porIa;
}

class ResultadoDiag {
  const ResultadoDiag({
    required this.declarado,
    required this.nivel,
    required this.cefr,
    required this.confianza,
    required this.preguntas,
    required this.aciertos,
    required this.skills,
    required this.fortalezas,
    required this.debilidades,
    required this.recurrentes,
    required this.refuerzo,
    required this.recomendado,
    required this.plan,
    this.escritura,
  });
  final int declarado;
  final double nivel; // con medios puntos, 0 = Fundamentos
  final String cefr;
  final double confianza;
  final int preguntas;
  final int aciertos;
  final Map<String, double> skills; // 1-10
  final List<String> fortalezas;
  final List<String> debilidades;
  final List<String> recurrentes;
  final List<String> refuerzo;
  final int recomendado; // 0 = Fundamentos, 1-10
  final List<String> plan;
  final EvaluacionEscritura? escritura;

  double get precision => preguntas == 0 ? 0 : aciertos / preguntas;

  Map<String, dynamic> toJson() => {
        'declarado': declarado,
        'nivel': nivel,
        'cefr': cefr,
        'confianza': confianza,
        'preguntas': preguntas,
        'aciertos': aciertos,
        'skills': skills,
        'fortalezas': fortalezas,
        'debilidades': debilidades,
        'recurrentes': recurrentes,
        'refuerzo': refuerzo,
        'recomendado': recomendado,
        'plan': plan,
        if (escritura != null) 'escritura': {'puntuacion': escritura!.puntuacion, 'correccion': escritura!.correccion, 'comentario': escritura!.comentario, 'porIa': escritura!.porIa},
        'fecha': DateTime.now().toIso8601String(),
      };
}

String cefrDe(double n) {
  if (n < 1) return 'Pre-A1 · desde cero';
  if (n < 1.5) return 'Pre-A1';
  if (n < 2.5) return 'A1';
  if (n < 3.5) return 'A2';
  if (n < 4.5) return 'A2+';
  if (n < 5.5) return 'B1';
  if (n < 6.5) return 'B1+';
  if (n < 7) return 'B1+ · acercándose a B2';
  if (n < 7.5) return 'B2';
  if (n < 8.5) return 'B2+ / C1';
  if (n < 9.5) return 'C1';
  return 'C2';
}

/// Petición al generador de preguntas (IA): el motor decide qué medir, la IA redacta.
class PeticionDiag {
  const PeticionDiag({required this.nivel, required this.skill, required this.tipo, required this.evitar, required this.declarado, required this.estimacion, required this.aciertos, required this.fallos, required this.debilidades});
  final int nivel;
  final String skill;
  final TipoDiag tipo;
  final List<String> evitar;
  final int declarado;
  final double estimacion;
  final int aciertos;
  final int fallos;
  final List<String> debilidades;

  Map<String, dynamic> toJson() => {
        'nivel': nivel, 'skill': skill, 'tipo': tipo.name, 'evitar': evitar, 'declarado': declarado,
        'estimacion': estimacion, 'aciertos': aciertos, 'fallos': fallos, 'debilidades': debilidades,
      };
}

/// Tipos de pregunta que usa cada competencia (rotan para variar el formato).
const tiposPorSkill = <String, List<TipoDiag>>{
  'comprension': [TipoDiag.escucha, TipoDiag.contexto, TipoDiag.dictado],
  'vocabulario': [TipoDiag.significado, TipoDiag.eleccion, TipoDiag.escucha],
  'gramatica': [TipoDiag.eleccion, TipoDiag.completar, TipoDiag.error],
  'tiempos': [TipoDiag.completar, TipoDiag.eleccion, TipoDiag.dictado],
  'expresiones': [TipoDiag.natural, TipoDiag.significado],
  'contexto': [TipoDiag.contexto, TipoDiag.escucha],
  'cotidiano': [TipoDiag.situacion, TipoDiag.corta, TipoDiag.natural],
  'escritura': [TipoDiag.escritura],
};

class Diagnostico {
  Diagnostico({
    required this.declarado,
    required List<PreguntaDiag> banco,
    this.minPreguntas = 10,
    this.maxPreguntas = 25,
    this.generador,
    Random? random,
  })  : _banco = List.of(banco),
        estimacion = declarado.toDouble().clamp(0, 10),
        _rnd = random ?? Random();

  /// Generador con IA (opcional). Si falla o no existe, se usa el banco sembrado.
  final Future<PreguntaDiag?> Function(PeticionDiag peticion)? generador;
  /// Origen de la última pregunta: 'ia' o 'banco'.
  String origenActual = 'banco';

  final int declarado;
  final List<PreguntaDiag> _banco;
  final int minPreguntas;
  final int maxPreguntas;
  final Random _rnd;

  double estimacion;
  final respuestas = <RespuestaDiag>[];
  final _usadas = <String>{};
  final _historial = <double>[];
  PreguntaDiag? actual;
  bool terminado = false;
  bool escrituraHecha = false;

  int get n => respuestas.length;
  int get aciertos => respuestas.where((r) => r.correcta).length;
  int get nivelActual => estimacion.round().clamp(0, 10);

  Map<String, int> get _porSkill {
    final m = <String, int>{};
    for (final r in respuestas) {
      m[r.pregunta.skill] = (m[r.pregunta.skill] ?? 0) + 1;
    }
    return m;
  }

  bool get _tocaEscritura => !escrituraHecha && estimacion >= 1.5 && (n >= 8 || _estable()) && _banco.any((q) => q.esEscritura);

  Map<String, int> get _porTipo {
    final m = <String, int>{};
    for (final r in respuestas) {
      m[r.pregunta.tipo.name] = (m[r.pregunta.tipo.name] ?? 0) + 1;
    }
    return m;
  }

  bool get _terminaria => n >= maxPreguntas || (n >= minPreguntas && _estable() && (escrituraHecha || estimacion < 1.5));

  /// Competencia menos medida (sin contar la escritura) para la siguiente pregunta.
  String _siguienteSkill() {
    final conteo = _porSkill;
    final skills = skillsDiag.keys.where((k) => k != 'escritura').toList()..shuffle(_rnd);
    skills.sort((a, b) => (conteo[a] ?? 0) - (conteo[b] ?? 0));
    return skills.first;
  }

  /// Tipo menos usado de los que admite la competencia (variedad de formatos).
  TipoDiag _siguienteTipo(String skill, int nivel) {
    final conteo = _porTipo;
    var tipos = [...(tiposPorSkill[skill] ?? [TipoDiag.eleccion])]..shuffle(_rnd);
    // En Fundamentos no se dicta: reconocer letras y palabras sueltas.
    if (nivel == 0) tipos = tipos.where((t) => t != TipoDiag.dictado && t != TipoDiag.completar && t != TipoDiag.corta).toList();
    if (tipos.isEmpty) return TipoDiag.eleccion;
    tipos.sort((a, b) => (conteo[a.name] ?? 0) - (conteo[b.name] ?? 0));
    return tipos.first;
  }

  List<String> get _debilidadesActuales {
    final out = <String>[];
    for (final s in skillsDiag.keys) {
      final rs = respuestas.where((r) => r.pregunta.skill == s).toList();
      if (rs.length >= 2 && rs.where((r) => !r.correcta).length * 2 > rs.length) out.add(skillsDiag[s]!);
    }
    return out;
  }

  /// Siguiente pregunta pidiéndola a la IA (con el banco sembrado como respaldo). null si terminó.
  Future<PreguntaDiag?> siguienteAsync() async {
    if (terminado || generador == null) return siguiente();
    if (_terminaria) {
      terminado = true;
      return null;
    }
    final String skill;
    final TipoDiag tipo;
    if (_tocaEscritura || (!escrituraHecha && estimacion >= 1.5 && n >= 8)) {
      skill = 'escritura';
      tipo = TipoDiag.escritura;
    } else {
      skill = _siguienteSkill();
      tipo = _siguienteTipo(skill, nivelActual);
    }
    final peticion = PeticionDiag(
      nivel: nivelActual, skill: skill, tipo: tipo,
      evitar: [for (final r in respuestas) r.pregunta.texto],
      declarado: declarado, estimacion: estimacion, aciertos: aciertos, fallos: n - aciertos, debilidades: _debilidadesActuales,
    );
    PreguntaDiag? q;
    try {
      q = await generador!(peticion);
    } catch (_) {
      q = null;
    }
    if (q != null && q.texto.isNotEmpty && !_usadas.contains(q.clave)) {
      _usadas.add(q.clave);
      origenActual = 'ia';
      actual = q.barajada(_rnd);
      if (q.esEscritura) escrituraHecha = false; // se marca al registrar
      return actual;
    }
    origenActual = 'banco';
    return siguiente();
  }

  /// Siguiente pregunta del banco sembrado (null si terminó).
  PreguntaDiag? siguiente() {
    if (terminado) return null;
    if (n >= maxPreguntas) {
      terminado = true;
      return null;
    }
    if (n >= minPreguntas && _estable() && (escrituraHecha || estimacion < 1.5 || !_banco.any((q) => q.esEscritura))) {
      terminado = true;
      return null;
    }
    PreguntaDiag? q;
    if (_tocaEscritura) {
      q = _mejor(_banco.where((x) => x.esEscritura && !_usadas.contains(x.clave)).toList(), nivelActual);
    }
    q ??= _elegirObjetiva();
    if (q == null) {
      terminado = true;
      return null;
    }
    _usadas.add(q.clave);
    actual = q.barajada(_rnd);
    return actual;
  }

  PreguntaDiag? _elegirObjetiva() {
    final objetivo = nivelActual;
    final conteo = _porSkill;
    for (final distancia in [0, 1, 2, 3, 10]) {
      final candidatas = _banco.where((x) => !x.esEscritura && !_usadas.contains(x.clave) && (x.nivel - objetivo).abs() <= distancia).toList();
      if (candidatas.isEmpty) continue;
      // Competencia menos medida hasta ahora; entre iguales, la más cercana al objetivo; luego azar.
      candidatas.sort((a, b) {
        final ca = conteo[a.skill] ?? 0, cb = conteo[b.skill] ?? 0;
        if (ca != cb) return ca - cb;
        final da = (a.nivel - objetivo).abs(), db = (b.nivel - objetivo).abs();
        if (da != db) return da - db;
        return 0;
      });
      final menor = conteo[candidatas.first.skill] ?? 0;
      final menorDist = (candidatas.first.nivel - objetivo).abs();
      final empate = candidatas.where((x) => (conteo[x.skill] ?? 0) == menor && (x.nivel - objetivo).abs() == menorDist).toList();
      return empate[_rnd.nextInt(empate.length)];
    }
    return null;
  }

  PreguntaDiag? _mejor(List<PreguntaDiag> lista, int objetivo) {
    if (lista.isEmpty) return null;
    lista.sort((a, b) => (a.nivel - objetivo).abs() - (b.nivel - objetivo).abs());
    return lista.first;
  }

  /// La estimación se ha movido poco en las últimas cuatro respuestas.
  bool _estable() {
    if (_historial.length < 4) return false;
    final ult = _historial.sublist(_historial.length - 4);
    return ult.reduce(max) - ult.reduce(min) <= 0.5;
  }

  static String _norm(String t) => soloNativo(t).toLowerCase().replaceAll(RegExp(r"[^\p{L}\p{N}\s']", unicode: true), '').replaceAll(RegExp(r'\s+'), ' ').trim();

  /// Comprueba una respuesta objetiva y actualiza la estimación.
  bool responder(String respuesta) {
    final q = actual;
    if (q == null || q.esEscritura) return false;
    final bool ok;
    if (q.conOpciones) {
      ok = respuesta == q.opciones[q.correcta];
    } else if (q.tipo == TipoDiag.dictado) {
      // Dictado: se admite un pequeño margen (una palabra de cada cinco).
      final esperado = q.aceptadas.isEmpty ? q.texto : q.aceptadas.first;
      ok = similitud(respuesta, esperado) >= 0.8 || q.aceptadas.any((a) => _norm(a) == _norm(respuesta));
    } else {
      final r = _norm(respuesta);
      ok = q.aceptadas.any((a) => _norm(a) == r);
    }
    respuestas.add(RespuestaDiag(pregunta: q, respuesta: respuesta, correcta: ok));
    _ajustar(q, ok);
    return ok;
  }

  void _ajustar(PreguntaDiag q, bool ok) {
    double delta;
    if (ok) {
      delta = q.nivel > estimacion + 0.5 ? 0.75 : 0.5;
    } else {
      delta = q.nivel < estimacion - 0.5 ? -0.75 : -0.5;
      // Fallos concentrados en una sola competencia con buen rendimiento general:
      // se anota la debilidad, pero no baja el nivel global tanto.
      final fallosSkill = respuestas.where((r) => !r.correcta && r.pregunta.skill == q.skill).length;
      final precision = respuestas.isEmpty ? 0.0 : aciertos / respuestas.length;
      if (fallosSkill >= 2 && precision >= 0.6) delta = -0.25;
    }
    estimacion = (estimacion + delta.clamp(-1.0, 1.0)).clamp(0.0, 10.0);
    _historial.add(estimacion);
  }

  /// Registra la evaluación de la producción escrita (IA o local).
  void registrarEscritura(String texto, EvaluacionEscritura e) {
    final q = actual;
    if (q == null) return;
    escrituraHecha = true;
    _escritura = e;
    respuestas.add(RespuestaDiag(pregunta: q, respuesta: texto, correcta: e.puntuacion >= estimacion - 0.5, puntuacion: e.puntuacion));
    // La producción libre pesa más que una pregunta de opción: media ponderada.
    final nueva = (estimacion * 2 + e.puntuacion) / 3;
    estimacion = (estimacion + (nueva - estimacion).clamp(-1.0, 1.0)).clamp(0.0, 10.0);
    _historial.add(estimacion);
  }

  EvaluacionEscritura? _escritura;

  /// Evaluación local de respaldo cuando la IA no está disponible.
  static EvaluacionEscritura evaluarLocal(String texto, double estimacion) {
    final palabras = texto.trim().split(RegExp(r'\s+')).where((w) => w.isNotEmpty).toList();
    final frases = texto.split(RegExp(r'[.!?。！？]+')).where((f) => f.trim().isNotEmpty).length;
    final largas = palabras.where((w) => w.length >= 7).length;
    var p = estimacion;
    if (palabras.length < 8) p -= 1.5;
    if (palabras.length >= 40) p += 0.5;
    if (frases >= 3) p += 0.25;
    if (largas >= 4) p += 0.25;
    return EvaluacionEscritura(
      puntuacion: p.clamp(1, 10),
      comentario: palabras.length < 8 ? 'Texto muy corto: escribe al menos 3 frases para medir mejor tu escritura.' : 'Evaluación aproximada sin IA: cuenta de frases y vocabulario.',
      porIa: false,
    );
  }

  /// Nivel final: la producción escrita pesa un 35 % cuando existe, porque
  /// reconocer una respuesta entre cuatro no demuestra lo mismo que producir el idioma.
  double get nivelFinal {
    final e = _escritura;
    final v = e == null ? estimacion : estimacion * 0.65 + e.puntuacion * 0.35;
    return (v.clamp(0.0, 10.0) * 2).round() / 2;
  }

  ResultadoDiag resultado() {
    final nivel = nivelFinal;
    // Puntuación por competencia: nivel estimado ajustado por la precisión en esa competencia.
    final skills = <String, double>{};
    for (final s in skillsDiag.keys) {
      final rs = respuestas.where((r) => r.pregunta.skill == s).toList();
      if (rs.isEmpty) continue;
      if (s == 'escritura') {
        skills[s] = ((rs.first.puntuacion ?? estimacion) * 2).round() / 2;
        continue;
      }
      final prec = rs.where((r) => r.correcta).length / rs.length;
      final nivelMedio = rs.map((r) => r.pregunta.nivel).reduce((a, b) => a + b) / rs.length;
      final v = (nivelMedio + (prec - 0.5) * 3).clamp(1.0, 10.0);
      skills[s] = (v * 2).round() / 2;
    }
    final fortalezas = [for (final e in skills.entries) if (e.value >= nivel + 0.5) skillsDiag[e.key]!];
    final debilidades = [for (final e in skills.entries) if (e.value <= nivel - 0.5) skillsDiag[e.key]!];
    final temasFallados = <String, int>{};
    for (final r in respuestas.where((r) => !r.correcta && !r.pregunta.esEscritura)) {
      temasFallados[r.pregunta.tema] = (temasFallados[r.pregunta.tema] ?? 0) + 1;
    }
    final recurrentes = [for (final e in temasFallados.entries) if (e.value >= 2) e.key];
    final refuerzo = <String>{...temasFallados.keys, ...?_escritura?.errores}.toList();
    final recomendado = nivel < 1 ? 0 : nivel.round().clamp(1, 10);
    final confianza = (0.4 + n * 0.03 + (escrituraHecha ? 0.15 : 0) - (_estable() ? 0 : 0.1)).clamp(0.3, 0.95);
    return ResultadoDiag(
      declarado: declarado,
      nivel: nivel,
      cefr: cefrDe(nivel),
      confianza: (confianza * 100).round() / 100,
      preguntas: n,
      aciertos: aciertos,
      skills: skills,
      fortalezas: fortalezas,
      debilidades: debilidades,
      recurrentes: recurrentes,
      refuerzo: refuerzo,
      recomendado: recomendado,
      plan: planDe(recomendado, refuerzo),
      escritura: _escritura,
    );
  }

  /// Plan inicial: unidades del nivel recomendado (y del anterior) que tratan los temas a reforzar.
  static List<String> planDe(int recomendado, List<String> refuerzo) {
    final plan = <String>[];
    if (recomendado == 0) {
      plan.add('Fundamentos: letras y sonidos, números, colores y palabras básicas');
      plan.add('Después, Nivel 1 desde la unidad 1');
      return plan;
    }
    final niveles = {recomendado, if (recomendado > 1) recomendado - 1};
    for (final tema in refuerzo) {
      final claves = tema.toLowerCase().split(RegExp(r'[\s/,]+')).where((w) => w.length > 3).toList();
      String? hallado;
      for (final nv in niveles) {
        for (final u in unidadesDe(nv)) {
          final titulo = u.titulo.toLowerCase();
          if (claves.any((c) => titulo.contains(c))) {
            hallado = 'Nivel $nv · Unidad ${u.numero}: ${u.titulo} (refuerza: $tema)';
            break;
          }
        }
        if (hallado != null) break;
      }
      plan.add(hallado ?? 'Refuerzo con la IA: $tema');
      if (plan.length >= 6) break;
    }
    if (plan.isEmpty) plan.add('Empieza el Nivel $recomendado desde la unidad 1: no se detectaron debilidades claras');
    return plan;
  }
}
