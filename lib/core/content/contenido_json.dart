import 'dart:convert';

import 'package:flutter/material.dart' show Color, IconData;
import 'package:flutter/services.dart' show rootBundle;

import '../models/models.dart';
import 'curriculum.dart' show invalidarCacheContenido;
import 'fundamentos.dart';
import '../diagnostico.dart' show BancoDiag;

/// Contenido generado por el pipeline (`tools/contenido`) y empaquetado en
/// `assets/contenido/<idioma>/nivel-N.json`. Si el fichero existe, sustituye a
/// los bancos escritos a mano de `curriculum.dart` / `idiomas.dart`.
class UnidadJson {
  UnidadJson({required this.numero, required this.tema, required this.titulo, required this.objetivo, required this.gramatica,
      required this.vocab, required this.frases, required this.dialogo, required this.erroresTipicos, required this.examen});
  final int numero;
  final String tema;
  final String titulo;
  final String objetivo;
  final String gramatica;
  final List<({String palabra, String romanizacion, String traduccion, String ejemplo})> vocab;
  final List<({String texto, String romanizacion, String traduccion})> frases;
  final List<({String quien, String texto, String romanizacion, String traduccion})> dialogo;
  final List<({String incorrecto, String correcto, String explicacion})> erroresTipicos;
  final List<({String pregunta, List<String> opciones, int correcta, String explicacion})> examen;

  static UnidadJson fromJson(Map<String, dynamic> j) => UnidadJson(
        numero: j['numero'] as int,
        tema: j['tema'] as String? ?? '',
        titulo: j['titulo'] as String? ?? '',
        objetivo: j['objetivo'] as String? ?? '',
        gramatica: j['gramatica'] as String? ?? '',
        vocab: [
          for (final v in (j['vocab'] as List))
            (palabra: v['palabra'] as String, romanizacion: v['romanizacion'] as String? ?? '', traduccion: v['traduccion'] as String, ejemplo: v['ejemplo'] as String? ?? '')
        ],
        frases: [
          for (final f in (j['frases'] as List))
            (texto: f['texto'] as String, romanizacion: f['romanizacion'] as String? ?? '', traduccion: f['traduccion'] as String)
        ],
        dialogo: [
          for (final d in (j['dialogo'] as List? ?? []))
            (quien: d['quien'] as String? ?? '', texto: d['texto'] as String, romanizacion: d['romanizacion'] as String? ?? '', traduccion: d['traduccion'] as String? ?? '')
        ],
        erroresTipicos: [
          for (final e in (j['errores_tipicos'] as List? ?? []))
            (incorrecto: e['incorrecto'] as String, correcto: e['correcto'] as String, explicacion: e['explicacion'] as String? ?? '')
        ],
        examen: [
          for (final q in (j['examen'] as List? ?? []))
            (pregunta: q['pregunta'] as String, opciones: (q['opciones'] as List).cast<String>(), correcta: q['correcta'] as int, explicacion: q['explicacion'] as String? ?? '')
        ],
      );

  /// Palabra tal como la muestra la app: texto nativo + romanización entre paréntesis.
  static String conRomanizacion(String texto, String rom) => rom.isEmpty ? texto : '$texto ($rom)';
}

class ContenidoJson {
  ContenidoJson._();
  static final Map<String, Map<int, List<UnidadJson>>> _cache = {}; // idioma → nivel → unidades
  static final Set<String> _intentado = {};

  static List<UnidadJson>? unidades(String idioma, int nivel) => _cache[idioma]?[nivel];

  /// Carga los 10 niveles de un idioma (los que existan) y refresca el currículo.
  static Future<void> precargar(String idioma) async {
    if (_intentado.contains(idioma)) return;
    _intentado.add(idioma);
    await Fundamentos.precargar(idioma);
    await BancoDiag.precargar(idioma);
    var alguno = false;
    for (var n = 1; n <= 10; n++) {
      try {
        final raw = await rootBundle.loadString('assets/contenido/$idioma/nivel-$n.json');
        final j = jsonDecode(raw) as Map<String, dynamic>;
        final lista = [for (final u in (j['unidades'] as List)) UnidadJson.fromJson(u as Map<String, dynamic>)];
        if (lista.length == 20) {
          (_cache[idioma] ??= {})[n] = lista;
          alguno = true;
        }
      } catch (_) {
        // No existe el fichero para ese nivel: se usa el banco escrito a mano.
      }
    }
    if (alguno) invalidarCacheContenido(idioma);
  }

  /// Convierte una unidad JSON al modelo `Unit` que usa el generador de lecciones.
  static Unit aUnit(UnidadJson u, int nivel, IconData icono, Color color) => Unit(
        nivel: nivel,
        numero: u.numero,
        titulo: u.titulo.isEmpty ? u.tema : u.titulo,
        icono: icono,
        color: color,
        vocab: [for (final v in u.vocab) (UnidadJson.conRomanizacion(v.palabra, v.romanizacion), v.traduccion)],
        frases: [
          for (final f in u.frases)
            (f.texto, f.romanizacion.isEmpty ? f.traduccion : '${f.traduccion} (${f.romanizacion})')
        ],
        gramatica: u.gramatica,
        dialogo: [for (final d in u.dialogo) (d.quien, UnidadJson.conRomanizacion(d.texto, d.romanizacion), d.traduccion)],
        erroresTipicos: [for (final e in u.erroresTipicos) (e.incorrecto, e.correcto, e.explicacion)],
        examen: [for (final q in u.examen) (q.pregunta, q.opciones, q.correcta, q.explicacion)],
      );
}
