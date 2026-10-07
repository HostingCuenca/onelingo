import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../models/models.dart';
import 'contenido_json.dart' show UnidadJson;
import 'curriculum.dart' show invalidarCacheContenido, iconoUnidad, colorUnidad;
import 'idiomas.dart' show soloNativo;

/// Nivel 0 · Fundamentos: para quien empieza de cero. Antes de formar frases
/// aprende, como un niño, las letras y sus sonidos, los números, los colores y
/// las palabras sueltas más básicas. No cuenta dentro de los 10 niveles del
/// contrato: es un tramo previo, recomendado por la prueba de nivel cuando el
/// alumno no supera las preguntas más elementales.
///
/// Contenido: `assets/contenido/<idioma>/nivel-0.json` (semilla `tools/contenido/semilla/<idioma>-nivel-0.txt`).
/// Idiomas en reconstrucción cuyo Fundamentos es solo la ruta f0
/// (`assets/contenido/<idioma>/ruta/f0.json`): su `nivel-0.json` antiguo se
/// retiró al reiniciarlos desde cero (portugués, DEC-035; italiano, versión
/// esencial de 10-2026) y no se resucita. El chino y el japonés (versión
/// esencial de 10-2026) nunca tuvieron `nivel-0.json`: también son solo la
/// ruta f0.
const idiomasSoloRutaF0 = {'pt', 'it', 'zh', 'ja'};

const nivelFundamentos = Level(
  numero: 0,
  nombre: 'Fundamentos',
  descripcion: 'Empieza desde cero: letras y sonidos, números, colores y palabras básicas. Sin frases todavía.',
  temario: ['Letras y escritura', 'Sonidos', 'Números', 'Colores', 'Palabras básicas', 'Vocabulario esencial', 'Verbos esenciales'],
);

class ItemFund {
  const ItemFund({required this.simbolo, required this.romanizacion, required this.significado, required this.ejemplo});
  final String simbolo; // letra, sílaba o palabra en escritura nativa
  final String romanizacion; // cómo suena / romanización (vacío en alfabeto latino cuando es una palabra)
  final String significado; // explicación o traducción en español
  final String ejemplo; // palabra o sílaba de ejemplo

  /// Texto que se muestra y se lee en voz alta: símbolo + (romanización).
  String get mostrado => UnidadJson.conRomanizacion(simbolo, romanizacion);

  /// Lo que hay que reconocer: el sonido (letras) o la traducción (palabras).
  String get clave => romanizacion.isNotEmpty ? romanizacion : significado;
}

class UnidadFund {
  const UnidadFund({required this.numero, required this.tipo, required this.titulo, required this.descripcion, required this.items, required this.examen});
  final int numero;
  final String tipo; // 'escritura' | 'vocabulario'
  final String titulo;
  final String descripcion;
  final List<ItemFund> items;
  final List<(String, List<String>, int, String)> examen;

  bool get esEscritura => tipo == 'escritura';

  static UnidadFund fromJson(Map<String, dynamic> j) => UnidadFund(
        numero: j['numero'] as int,
        tipo: j['tipo'] as String? ?? 'vocabulario',
        titulo: j['titulo'] as String? ?? '',
        descripcion: j['descripcion'] as String? ?? '',
        items: [
          for (final it in (j['items'] as List))
            ItemFund(simbolo: it['simbolo'] as String, romanizacion: it['romanizacion'] as String? ?? '', significado: it['significado'] as String? ?? '', ejemplo: it['ejemplo'] as String? ?? '')
        ],
        examen: [
          for (final q in (j['examen'] as List? ?? []))
            (q['pregunta'] as String, (q['opciones'] as List).cast<String>(), q['correcta'] as int, q['explicacion'] as String? ?? '')
        ],
      );
}

class Fundamentos {
  Fundamentos._();
  static final Map<String, List<UnidadFund>> _cache = {};
  static final Set<String> _intentado = {};

  static List<UnidadFund> unidades(String idioma) => _cache[idioma] ?? const [];
  static bool disponible(String idioma) => (_cache[idioma]?.isNotEmpty) ?? false;

  static Future<void> precargar(String idioma) async {
    if (_intentado.contains(idioma)) return;
    _intentado.add(idioma);
    try {
      final raw = await rootBundle.loadString('assets/contenido/$idioma/nivel-0.json');
      final j = jsonDecode(raw) as Map<String, dynamic>;
      _cache[idioma] = [for (final u in (j['unidades'] as List)) UnidadFund.fromJson(u as Map<String, dynamic>)];
      invalidarCacheContenido(idioma);
    } catch (_) {
      // Sin fundamentos para este idioma: el nivel 0 queda vacío y no se muestra.
    }
  }

  /// Unidades del nivel 0 como `Unit` (para el examen y las pantallas de nivel).
  static List<Unit> comoUnits(String idioma) => [
        for (final u in unidades(idioma))
          Unit(
            nivel: 0,
            numero: u.numero,
            titulo: u.titulo,
            icono: iconoUnidad(u.numero),
            color: colorUnidad(u.numero),
            vocab: [for (final it in u.items) (it.mostrado, it.significado)],
            gramatica: u.descripcion,
            examen: u.examen,
          )
      ];

  static const _porLeccion = 6; // ítems por lección: cortas, para no frustrar

  /// Lecciones del nivel 0: por cada bloque de ítems una lección "Descubre" y
  /// una "Practica"; al final de cada unidad, un "Repaso".
  static List<Lesson> lecciones(String idioma) {
    final out = <Lesson>[];
    var numero = 0;
    Lesson nueva(UnidadFund u, String titulo, String sub, List<LessonStep> pasos) {
      numero++;
      return Lesson(id: 'L0-${numero.toString().padLeft(3, '0')}', nivel: 0, numero: numero, unidad: u.numero, titulo: titulo, subtitulo: sub, steps: pasos, xp: 15);
    }

    for (final u in unidades(idioma)) {
      final bloques = <List<ItemFund>>[];
      for (var i = 0; i < u.items.length; i += _porLeccion) {
        bloques.add(u.items.sublist(i, (i + _porLeccion).clamp(0, u.items.length)));
      }
      // Un bloque final demasiado corto se une al anterior.
      if (bloques.length > 1 && bloques.last.length < 3) {
        final ultimo = bloques.removeLast();
        bloques.last.addAll(ultimo);
      }
      for (var b = 0; b < bloques.length; b++) {
        final parte = bloques.length > 1 ? ' (${b + 1}/${bloques.length})' : '';
        out.add(nueva(u, 'Descubre: ${u.titulo}$parte', u.esEscritura ? 'Mira, escucha y repite' : 'Palabras nuevas', _descubre(u, bloques[b])));
        out.add(nueva(u, 'Practica: ${u.titulo}$parte', 'Reconoce y pronuncia', _practica(u, bloques[b])));
      }
      out.add(nueva(u, 'Repaso: ${u.titulo}', 'Todo junto', _repaso(u)));
    }
    return out;
  }

  /// Opciones con la correcta en primer lugar (el reproductor la lee de `answer`)
  /// y el resto barajado; el orden mostrado se baraja al construir el paso.
  static List<String> _opciones(List<ItemFund> todos, ItemFund correcto, String Function(ItemFund) f) {
    final otros = <String>{for (final o in todos) if (o != correcto && f(o) != f(correcto)) f(o)}.toList()..shuffle();
    return [f(correcto), ...otros.take(3)]..shuffle();
  }

  /// Parejas sin claves ni símbolos repetidos (si dos letras suenan igual, se usa solo una).
  static List<(String, String)> _parejasUnicas(UnidadFund u, List<ItemFund> its) {
    final vistosA = <String>{}, vistosB = <String>{};
    final out = <(String, String)>[];
    for (final it in its) {
      final a = u.esEscritura ? it.simbolo : it.mostrado;
      final b = it.clave;
      if (vistosA.add(a) && vistosB.add(b)) out.add((a, b));
      if (out.length == 4) break;
    }
    return out;
  }

  static LessonStep _flash(UnidadFund u, ItemFund it) => LessonStep(
        type: StepType.flashcard,
        skill: u.esEscritura ? Skill.escritura : Skill.vocabulario,
        prompt: it.mostrado,
        translation: it.significado,
        hint: it.ejemplo,
      );

  /// "¿Cómo suena か?" (escritura) o "¿Qué significa 水?" (vocabulario).
  static LessonStep _eligeClave(UnidadFund u, ItemFund it, List<ItemFund> todos) => LessonStep(
        type: StepType.multipleChoice,
        skill: u.esEscritura ? Skill.pronunciacion : Skill.vocabulario,
        prompt: u.esEscritura ? '¿Cómo suena "${it.simbolo}"?' : '¿Qué significa "${it.simbolo}"?',
        answer: it.clave,
        options: _opciones(todos, it, (o) => o.clave),
        translation: it.ejemplo,
      );

  /// "¿Qué letra suena 'ka'?" o "¿Cómo se dice 'agua'?".
  static LessonStep _eligeSimbolo(UnidadFund u, ItemFund it, List<ItemFund> todos) => LessonStep(
        type: StepType.multipleChoice,
        skill: u.esEscritura ? Skill.escritura : Skill.vocabulario,
        prompt: u.esEscritura ? '¿Qué letra o sílaba suena "${it.clave}"?' : '¿Cómo se dice "${it.significado}"?',
        answer: u.esEscritura ? it.simbolo : it.mostrado,
        options: _opciones(todos, it, (o) => u.esEscritura ? o.simbolo : o.mostrado),
        hint: u.esEscritura ? 'Sonidos' : 'Vocabulario',
      );

  static LessonStep _pares(UnidadFund u, List<ItemFund> its) => LessonStep(
        type: StepType.matchPairs,
        skill: u.esEscritura ? Skill.escritura : Skill.vocabulario,
        prompt: u.esEscritura ? 'Une cada letra con su sonido' : 'Une cada palabra con su significado',
        pairs: _parejasUnicas(u, its),
      );

  static LessonStep _habla(UnidadFund u, ItemFund it) => LessonStep(
        type: StepType.speak,
        skill: Skill.pronunciacion,
        prompt: u.esEscritura && it.ejemplo.isNotEmpty ? it.ejemplo : it.mostrado,
        translation: u.esEscritura ? 'Suena "${it.clave}"' : it.significado,
      );

  static List<LessonStep> _descubre(UnidadFund u, List<ItemFund> b) => [
        for (final it in b) _flash(u, it),
        for (final it in b.take(3)) _eligeClave(u, it, b.length >= 4 ? b : u.items),
        _pares(u, [...b]..shuffle()),
      ];

  static List<LessonStep> _practica(UnidadFund u, List<ItemFund> b) {
    final barajados = [...b]..shuffle();
    return [
      for (final it in barajados.take(3)) _eligeSimbolo(u, it, b.length >= 4 ? b : u.items),
      for (final it in barajados.skip(3).take(2)) _eligeClave(u, it, b.length >= 4 ? b : u.items),
      for (final it in barajados.take(2)) _habla(u, it),
      _pares(u, barajados.reversed.toList()),
    ];
  }

  static List<LessonStep> _repaso(UnidadFund u) {
    final todos = [...u.items]..shuffle();
    return [
      for (final it in todos.take(3)) _eligeClave(u, it, u.items),
      for (final it in todos.skip(3).take(3)) _eligeSimbolo(u, it, u.items),
      _pares(u, todos.take(4).toList()),
      for (final it in todos.skip(6).take(2)) _habla(u, it),
      if (todos.length > 4) _pares(u, todos.skip(4).take(4).toList()),
    ];
  }

  /// Banco para la prueba de nivel (nivel 0): reconocer letras, sonidos y
  /// palabras básicas. Si el alumno no supera este bloque, empieza por Fundamentos.
  static List<LessonStep> banco(String idioma) {
    final out = <LessonStep>[];
    for (final u in unidades(idioma)) {
      for (final q in u.examen) {
        if (q.$2.length >= 2 && q.$3 >= 0 && q.$3 < q.$2.length) {
          out.add(LessonStep(type: StepType.multipleChoice, skill: Skill.vocabulario, prompt: q.$1, answer: q.$2[q.$3], options: [...q.$2]..shuffle(), hint: 'Fundamentos'));
        }
      }
      final its = [...u.items]..shuffle();
      for (final it in its.take(3)) {
        final s = _eligeClave(u, it, u.items);
        out.add(LessonStep(type: s.type, skill: s.skill, prompt: s.prompt, answer: s.answer, options: [...s.options], hint: 'Fundamentos'));
      }
    }
    return out..shuffle();
  }

  /// Para pruebas: texto nativo sin romanización de un ítem.
  static String nativo(ItemFund it) => soloNativo(it.mostrado);
}
