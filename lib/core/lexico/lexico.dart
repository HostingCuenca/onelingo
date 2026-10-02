import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../aprendizaje/dominio.dart';
import '../aprendizaje/modelos.dart';
import '../aprendizaje/providers.dart';
import '../content/situaciones.dart';
import '../nivel0/nivel0.dart';
import '../state/providers.dart';

/// Léxico único (fase D, docs/ARQUITECTURA_VIGENTE.md): índice de cada palabra
/// que enseña la app, con su nivel y dónde aparece. No es otra fuente: se
/// calcula desde la ruta (pasos de vocabulario), las situaciones y el Nivel 0,
/// así una palabra nunca vive en dos sitios.

/// Clave de una palabra: minúsculas, sin espacios ni puntuación final.
String claveLexico(String texto) => texto
    .trim()
    .toLowerCase()
    .replaceAll(RegExp(r'\s+'), ' ')
    .replaceAll(RegExp(r'[.!?¿¡,;:]+$'), '');

/// Dónde aparece una palabra.
class OrigenPalabra {
  const OrigenPalabra.clase(this.unidad) : situacion = null, tramo = null;
  const OrigenPalabra.situacion(int this.situacion, Tramo this.tramo)
    : unidad = null;
  final String? unidad;
  final int? situacion;
  final Tramo? tramo;
}

class EntradaLexico {
  EntradaLexico({
    required this.clave,
    required this.texto,
    required this.traduccion,
    required this.nivel,
    this.ejemplo,
  });
  final String clave, texto, traduccion;

  /// Nivel en que se enseña por primera vez (0 = Nivel 0 o Fundamentos).
  int nivel;
  String? ejemplo;
  final origenes = <OrigenPalabra>[];

  Iterable<int> get situaciones => {
    for (final o in origenes)
      if (o.situacion != null) o.situacion!,
  };
}

class LexicoIndice {
  LexicoIndice(this.idioma);
  final String idioma;
  final entradas = <String, EntradaLexico>{};

  EntradaLexico _poner(
    String texto,
    String traduccion,
    int nivel,
    OrigenPalabra origen, {
    String? ejemplo,
  }) {
    final clave = claveLexico(texto);
    final e = entradas.putIfAbsent(
      clave,
      () => EntradaLexico(
        clave: clave,
        texto: texto.trim(),
        traduccion: traduccion.trim(),
        nivel: nivel,
        ejemplo: ejemplo,
      ),
    );
    if (nivel < e.nivel) e.nivel = nivel;
    e.ejemplo ??= ejemplo;
    e.origenes.add(origen);
    return e;
  }

  /// Palabras enseñadas en una unidad de la ruta (las de sus pasos de
  /// vocabulario; el glosario de la unidad no cuenta).
  static Iterable<Vocablo> palabrasDeUnidad(UnidadRuta u) sync* {
    for (final p in u.pasos) {
      if (p.tipo != TipoPaso.vocabulario) continue;
      for (final id in p.refs) {
        final v = u.vocablo(id);
        if (v != null && v.texto.trim().isNotEmpty) yield v;
      }
    }
  }

  static LexicoIndice construir({
    required String idioma,
    required List<String> cadena,
    RutaCargada? ruta,
    Map<int, ContenidoSituacion>? situaciones,
    Nivel0? nivel0,
  }) {
    final l = LexicoIndice(idioma);
    for (final l0 in nivel0?.lecciones ?? const <LeccionN0>[]) {
      for (final paso in l0.pasos) {
        for (final p in [...paso.palabras, ...paso.opciones]) {
          if (p.traduccion == null || p.texto.trim().isEmpty) continue;
          l._poner(p.texto, p.traduccion!, 0, OrigenPalabra.clase(l0.id));
        }
      }
    }
    for (final u in ruta?.unidades ?? const <UnidadRuta>[]) {
      for (final v in palabrasDeUnidad(u)) {
        final es = v.traduccion.en(cadena);
        if (es.trim().isEmpty) continue;
        l._poner(v.texto, es, u.nivelInterno ?? 0, OrigenPalabra.clase(u.id));
      }
    }
    for (final s in situaciones?.values ?? const <ContenidoSituacion>[]) {
      for (final t in Tramo.values) {
        for (final p in s.tramo(t).vocabulario) {
          l._poner(
            p.en,
            p.es,
            t.nivelMinimo,
            OrigenPalabra.situacion(s.id, t),
            ejemplo: p.ejemplo,
          );
        }
      }
    }
    return l;
  }

  /// Palabras que el alumno ya vio: clases practicadas, tramos de situación
  /// empezados y lecciones del Nivel 0 completas. Se calcula, no se guarda.
  List<EntradaLexico> delAlumno({
    required Map<String, dynamic> practicas,
    required Set<String> unidadesVistas,
    Map<int, ContenidoSituacion>? situaciones,
  }) {
    final tramos = <(int, Tramo)>{};
    for (final s in situaciones?.values ?? const <ContenidoSituacion>[]) {
      for (final t in Tramo.values) {
        if (estadoTramo(practicas, idioma, s, t).empezado) tramos.add((s.id, t));
      }
    }
    bool vista(OrigenPalabra o) => o.unidad != null
        ? unidadesVistas.contains(o.unidad) ||
              leccionN0Completa(practicas, idioma, o.unidad!)
        : tramos.contains((o.situacion!, o.tramo!));
    return [
      for (final e in entradas.values)
        if (e.origenes.any(vista)) e,
    ]..sort((a, b) {
      final n = a.nivel.compareTo(b.nivel);
      return n != 0 ? n : a.texto.toLowerCase().compareTo(b.texto.toLowerCase());
    });
  }
}

/// Índice del idioma del alumno (espera a la ruta, las situaciones y el
/// Nivel 0, que ya se cargan en otras pantallas).
final lexicoProvider = FutureProvider<LexicoIndice>((ref) async {
  final s = ref.watch(progressProvider.select((s) => (s.idiomaMeta, s.idiomaNativo)));
  final idioma = s.$1;
  final ruta = await ref.watch(rutaProvider(idioma).future);
  final situaciones = await ref.watch(situacionesProvider(idioma).future);
  final nivel0 = await ref.watch(nivel0Provider.future);
  return LexicoIndice.construir(
    idioma: idioma,
    cadena: ruta == null
        ? const ['es']
        : cadenaApoyo(s.$2, ruta.curso.apoyoPredeterminado),
    ruta: ruta,
    situaciones: situaciones,
    nivel0: nivel0,
  );
});

/// Palabras del alumno («Mis palabras»).
final misPalabrasProvider = Provider<AsyncValue<List<EntradaLexico>>>((ref) {
  final s = ref.watch(progressProvider);
  return ref.watch(lexicoProvider).whenData((l) {
    final ruta = ref.watch(rutaProvider(s.idiomaMeta)).valueOrNull;
    final vistas = <String>{};
    if (ruta != null) {
      final e = estadosAlumno(ruta, s);
      for (final u in ruta.unidades) {
        // Omitir un nivel por la ubicación no enseña sus palabras.
        if (e[u.id]!.estado.alMenos(EstadoUnidad.practicada)) vistas.add(u.id);
      }
    }
    return l.delAlumno(
      practicas: s.practicas,
      unidadesVistas: vistas,
      situaciones: ref
          .watch(situacionesProvider(s.idiomaMeta))
          .valueOrNull,
    );
  });
});

// --- Repaso espaciado por palabra -------------------------------------------

/// Clave en `practicas` con el estado de repaso de todas las palabras de un
/// idioma: `{palabras: {clave: [caja, 'aaaa-mm-dd']}}`.
String claveRepasoLexico(String idioma) => 'lexico:$idioma';

const intervalosLexico = UnidadRuta.intervalosPorDefecto;

class RepasoPalabra {
  const RepasoPalabra(this.caja, this.proximo);

  /// 0 = recién fallada o nueva; sube con cada acierto.
  final int caja;
  final DateTime proximo;

  bool vencida(DateTime hoy) => !proximo.isAfter(_dia(hoy));

  /// Aprendida de verdad: superó varios repasos espaciados.
  bool get dominada => caja >= 3;

  List<Object> toJson() => [caja, _fecha(proximo)];
}

DateTime _dia(DateTime d) => DateTime(d.year, d.month, d.day);
String _fecha(DateTime d) =>
    '${d.year}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';

Map<String, RepasoPalabra> repasoLexico(
  Map<String, dynamic> practicas,
  String idioma,
) {
  final raw =
      (practicas[claveRepasoLexico(idioma)] as Map?)?['palabras'] as Map? ??
      const {};
  return {
    for (final e in raw.entries)
      if (e.value is List && (e.value as List).length == 2)
        '${e.key}': RepasoPalabra(
          ((e.value as List)[0] as num).toInt(),
          DateTime.tryParse('${(e.value as List)[1]}') ?? DateTime(2000),
        ),
  };
}

/// Resultado de una respuesta: acierto sube de caja y espacia el repaso;
/// fallo vuelve a la caja 0 y se repasa mañana.
RepasoPalabra responderPalabra(
  RepasoPalabra? anterior,
  bool correcta,
  DateTime hoy,
) {
  final caja = correcta
      ? ((anterior?.caja ?? 0) + 1).clamp(1, intervalosLexico.length)
      : 0;
  final dias = correcta ? intervalosLexico[caja - 1] : 1;
  return RepasoPalabra(caja, _dia(hoy).add(Duration(days: dias)));
}

/// Palabras para una sesión: primero las vencidas (las más atrasadas
/// primero), luego nuevas del nivel más bajo. Como mucho [n].
List<EntradaLexico> seleccionarRepaso(
  List<EntradaLexico> mias,
  Map<String, RepasoPalabra> estado,
  DateTime hoy, {
  int n = 10,
}) {
  final vencidas =
      [
        for (final e in mias)
          if (estado[e.clave]?.vencida(hoy) ?? false) e,
      ]..sort(
        (a, b) => estado[a.clave]!.proximo.compareTo(estado[b.clave]!.proximo),
      );
  final nuevas = [
    for (final e in mias)
      if (!estado.containsKey(e.clave)) e,
  ];
  return [...vencidas, ...nuevas].take(n).toList();
}

int vencidasHoy(
  List<EntradaLexico> mias,
  Map<String, RepasoPalabra> estado,
  DateTime hoy,
) => mias.where((e) => estado[e.clave]?.vencida(hoy) ?? false).length;
