import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../i18n/i18n.dart';
import '../state/providers.dart';

/// Nivel 0 · Leer y pronunciar (desde cero, por idioma). Contenido en
/// `assets/contenido/<idioma>/nivel0/`: el mapa de sonidos (sonidos.json) y las
/// unidades (nivel0.json). Es una pista propia, antes de Fundamentos: no
/// altera la ruta ni sus reglas de léxico (aquí se leen palabras como «sat»).

/// Un trozo de palabra marcada: `(a:ae)` pinta la «a» con el color del sonido
/// «ae»; `_` = muda, `=` = dos letras con un sonido, `*` = e mágica.
class Segmento {
  const Segmento(this.texto, [this.clave]);
  final String texto;
  final String? clave;

  bool get muda => clave == '_';
  bool get digrafo => clave == '=';
  bool get magica => clave == '*';
  String? get sonido =>
      (clave == null || muda || digrafo || magica) ? null : clave;
}

/// Unión entre palabras (liaison/enlace): se ve en la palabra, no se lee.
const enlace = '‿';

final _grupo = RegExp(r'\(([^():]+):([^()]+)\)');

/// Divide un marcado en segmentos de texto plano y letras marcadas.
List<Segmento> segmentos(String marcado) {
  final res = <Segmento>[];
  var i = 0;
  for (final m in _grupo.allMatches(marcado)) {
    if (m.start > i) res.add(Segmento(marcado.substring(i, m.start)));
    res.add(Segmento(m.group(1)!, m.group(2)));
    i = m.end;
  }
  if (i < marcado.length) res.add(Segmento(marcado.substring(i)));
  return res;
}

/// Texto sin marcas (lo que se escucha y se escribe).
String textoPlano(String marcado) =>
    segmentos(marcado).map((s) => s.texto).join().replaceAll(enlace, ' ');

class SonidoVocal {
  const SonidoVocal({
    required this.id,
    required this.grupo,
    required this.color,
    required this.colorNombre,
    required this.ancla,
    required this.emoji,
    required this.nombre,
    required this.grafias,
    required this.ejemplos,
    required this.unidad,
  });
  final String id, grupo, colorNombre, ancla, emoji, nombre;
  final Color color;
  final List<String> grafias, ejemplos;
  final int unidad;

  factory SonidoVocal.fromJson(Map<String, dynamic> j) => SonidoVocal(
    id: j['id'] as String,
    grupo: j['grupo'] as String,
    color: Color(
      int.parse('FF${(j['color'] as String).substring(1)}', radix: 16),
    ),
    colorNombre: j['colorNombre'] as String,
    ancla: j['ancla'] as String,
    emoji: j['emoji'] as String,
    nombre: j['nombre'] as String,
    grafias: [for (final g in j['grafias'] as List) '$g'],
    ejemplos: [for (final g in j['ejemplos'] as List) '$g'],
    unidad: j['unidad'] as int,
  );
}

/// Palabra con marcado, imagen (emoji) y traducción.
class Palabra {
  const Palabra(this.marcado, {this.emoji, this.traduccion});
  final String marcado;
  final String? emoji, traduccion;
  String get texto => textoPlano(marcado);

  factory Palabra.fromJson(Map<String, dynamic> j) => Palabra(
    (j['m'] as String?) ?? '',
    emoji: j['e'] as String?,
    traduccion: j['t'] as String?,
  );
}

String rutaEmoji(String codigo) => 'assets/img/emoji/$codigo.webp';

/// Un paso de lección. Se guarda el JSON y se exponen lectores por tipo.
class PasoN0 {
  const PasoN0(this.tipo, this.j);
  final String tipo;
  final Map<String, dynamic> j;

  String get texto => (j['texto'] as String?) ?? '';
  String get pregunta => (j['pregunta'] as String?) ?? '';
  String get marcado => (j['m'] as String?) ?? '';
  String? get traduccion => j['t'] as String?;
  String? get pose => j['pose'] as String?;
  String? get sonido => j['sonido'] as String?;
  int get correcta => (j['correcta'] as int?) ?? 0;
  List<Palabra> get palabras => [
    for (final p in (j['palabras'] as List? ?? const []))
      Palabra.fromJson(p as Map<String, dynamic>),
  ];
  List<Palabra> get opciones => [
    for (final o in (j['opciones'] as List? ?? const []))
      o is String ? Palabra(o) : Palabra.fromJson(o as Map<String, dynamic>),
  ];
  List<String> get textos => [
    for (final o in (j['opciones'] as List? ?? const [])) '$o',
  ];
  List<String> get fichas => [
    for (final f in (j['fichas'] as List? ?? const [])) '$f',
  ];
  List<String> get letras => [
    for (final f in (j['letras'] as List? ?? const [])) '$f',
  ];

  /// Pasos que el alumno responde (cuentan para la nota de la lección).
  bool get evaluable => const {
    'escucha_elige',
    'toca_sonido',
    'construye',
    'cambia',
    'lee',
    'elige_significado',
    'escucha_letra',
    'deletreo',
  }.contains(tipo);
}

class LeccionN0 {
  const LeccionN0(this.id, this.titulo, this.pasos);
  final String id, titulo;
  final List<PasoN0> pasos;
}

class UnidadN0 {
  const UnidadN0(this.id, this.titulo, this.objetivo, this.lecciones);
  final String id, titulo, objetivo;
  final List<LeccionN0> lecciones;
}

/// Idiomas con Nivel 0 (contenido en `assets/contenido/<idioma>/nivel0/`).
/// Mantener igual que `ProgressState.nivel0Pendiente`.
const idiomasConNivel0 = {'en', 'fr', 'es', 'pt', 'de'};

class Nivel0 {
  Nivel0({
    this.idioma = 'en',
    this.textos = const {},
    required this.titulo,
    required this.subtitulo,
    required this.voz,
    required this.unidades,
    required this.sonidos,
  });
  final String idioma, titulo, subtitulo, voz;

  /// Textos de interfaz propios del idioma (tarjeta, mapa, grupos…).
  final Map<String, dynamic> textos;
  String texto(String clave) => (textos[clave] as String?) ?? '';
  Map<String, String> get grupos => {
    for (final e in (textos['grupos'] as Map? ?? const {}).entries)
      '${e.key}': '${e.value}',
  };
  final List<UnidadN0> unidades;
  final List<SonidoVocal> sonidos;

  late final Map<String, SonidoVocal> porId = {
    for (final s in sonidos) s.id: s,
  };
  late final List<LeccionN0> lecciones = [
    for (final u in unidades) ...u.lecciones,
  ];

  LeccionN0? leccion(String id) {
    for (final l in lecciones) {
      if (l.id == id) return l;
    }
    return null;
  }

  static Nivel0 desdeJson(Map<String, dynamic> n, Map<String, dynamic> s) =>
      Nivel0(
        idioma: (n['idioma'] as String?) ?? 'en',
        textos: Map<String, dynamic>.from(n['textos'] as Map? ?? const {}),
        titulo: n['titulo'] as String,
        subtitulo: n['subtitulo'] as String,
        voz: (n['voz'] as String?) ?? 'sofia',
        sonidos: [
          for (final v in s['vocales'] as List)
            SonidoVocal.fromJson(v as Map<String, dynamic>),
        ],
        unidades: [
          for (final u in n['unidades'] as List)
            UnidadN0(
              u['id'] as String,
              u['titulo'] as String,
              u['objetivo'] as String,
              [
                for (final l in u['lecciones'] as List)
                  LeccionN0(l['id'] as String, l['titulo'] as String, [
                    for (final p in l['pasos'] as List)
                      PasoN0(p['tipo'] as String, p as Map<String, dynamic>),
                  ]),
              ],
            ),
        ],
      );
}

/// Nivel 0 del idioma que estudia el alumno (null si ese idioma no tiene).
final nivel0Provider = FutureProvider<Nivel0?>((ref) async {
  final idioma = ref.watch(progressProvider.select((s) => s.idiomaMeta));
  // Explicaciones en el idioma de la interfaz (textos {es, en} del JSON).
  final interfaz = ref.watch(progressProvider.select((s) => s.interfaz));
  if (!idiomasConNivel0.contains(idioma)) return null;
  final base = 'assets/contenido/$idioma/nivel0';
  final n = localizarApoyo(
    jsonDecode(await rootBundle.loadString('$base/nivel0.json')),
    interfaz,
  );
  final s = localizarApoyo(
    jsonDecode(await rootBundle.loadString('$base/sonidos.json')),
    interfaz,
  );
  return Nivel0.desdeJson(n as Map<String, dynamic>, s as Map<String, dynamic>);
});

/// Clave de progreso de una lección del Nivel 0.
String claveN0(String idioma, String leccionId) => 'nivel0:$idioma:$leccionId';

/// Marca de Nivel 0 terminado (deja de recomendarse al empezar).
String claveN0Completo(String idioma) => 'nivel0:$idioma:completo';

bool leccionN0Completa(
  Map<String, dynamic> practicas,
  String idioma,
  String leccionId,
) => (practicas[claveN0(idioma, leccionId)] as Map?)?['completa'] == true;

/// Una lección se abre cuando la anterior está completa (la primera, siempre).
bool leccionN0Abierta(
  Nivel0 n,
  Map<String, dynamic> practicas,
  String leccionId,
) {
  final i = n.lecciones.indexWhere((l) => l.id == leccionId);
  return i <= 0 ||
      leccionN0Completa(practicas, n.idioma, n.lecciones[i - 1].id);
}

/// Siguiente lección por hacer (null si todas están completas).
LeccionN0? siguienteN0(Nivel0 n, Map<String, dynamic> practicas) {
  for (final l in n.lecciones) {
    if (!leccionN0Completa(practicas, n.idioma, l.id)) return l;
  }
  return null;
}
