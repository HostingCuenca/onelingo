import 'diagnostico.dart';
import 'i18n/i18n.dart';

/// Selección reproducible basada en evidencias; la IA interpreta, no inventa IDs.
class RutaBiblioteca {
  static const habilidades = [
    'comprension',
    'listening',
    'gramatica',
    'vocabulario',
    'escritura',
  ];

  static int nivelSugerido(
    String skill,
    int inicial,
    Map<String, dynamic>? diagnostico,
    Map<String, dynamic> practicas,
  ) {
    final valor = (diagnostico?['skills'] as Map?)?[skill];
    var n = valor is num
        ? valor.round().clamp(
            (inicial - 1).clamp(1, 10),
            (inicial + 1).clamp(1, 10),
          )
        : inicial;
    final nuevas =
        practicas.values
            .whereType<Map>()
            .where(
              (r) =>
                  r['skill'] == skill &&
                  r['tipo'] != 'practica_guiada' &&
                  r['tipo'] != 'comprobacion_guiada' &&
                  r['conApoyo'] != true &&
                  (r['idioma'] == null || r['idioma'] == 'en') &&
                  (r['primeraCorrecta'] != null || r['intentos'] == 1),
            )
            .toList()
          ..sort(
            (a, b) => '${b['primeraFecha'] ?? b['fecha']}'.compareTo(
              '${a['primeraFecha'] ?? a['fecha']}',
            ),
          );
    final muestra = nuevas.take(4).toList();
    if (muestra.length >= 3) {
      final aciertos = muestra
          .where((r) => (r['primeraCorrecta'] ?? r['correcta']) == true)
          .length;
      if (aciertos == muestra.length) n++;
      if (aciertos <= 1) n--;
    }
    return n.clamp(1, 10);
  }

  static List<String> prioridades(
    Map<String, dynamic>? diagnostico,
    Map<String, dynamic> practicas,
  ) {
    final skills = diagnostico?['skills'] as Map? ?? {};
    double necesidad(String skill) {
      final recientes =
          practicas.values
              .whereType<Map>()
              .where(
                (r) =>
                    r['skill'] == skill &&
                    (r['idioma'] == null || r['idioma'] == 'en'),
              )
              .toList()
            ..sort((a, b) => '${b['fecha']}'.compareTo('${a['fecha']}'));
      final muestra = recientes.take(6).toList();
      if (muestra.length >= 2) {
        return muestra.where((r) => r['correcta'] != true).length /
            muestra.length;
      }
      final valor = skills[skill];
      return valor is num ? (10 - valor.toDouble()) / 10 : .55;
    }

    return [...habilidades]..sort((a, b) {
      final c = necesidad(b).compareTo(necesidad(a));
      return c == 0
          ? habilidades.indexOf(a).compareTo(habilidades.indexOf(b))
          : c;
    });
  }

  static List<PreguntaDiag> seleccionar({
    required List<PreguntaDiag> banco,
    required int nivel,
    required String skill,
    Map<String, dynamic> practicas = const {},
    List<String> sectores = const [],
    List<String> objetivos = const [],
    int limite = 4,
    bool nivelFijo = false,
  }) {
    final candidates = banco
        .where(
          (q) =>
              q.skill == skill &&
              (nivelFijo ? q.nivel == nivel : (q.nivel - nivel).abs() <= 1),
        )
        .toList();
    double score(PreguntaDiag q) {
      final previa = practicas[q.id] as Map?;
      // Prioriza contenido nuevo, conserva repaso de errores; no sube de nivel por repetición.
      return (q.nivel - nivel).abs() * 10 +
          (previa == null
              ? 0
              : previa['correcta'] == true
              ? 30
              : 15) -
          (q.sectores.any(sectores.contains) ? 2 : 0) -
          (q.objetivos.any(objetivos.contains) ? 1 : 0);
    }

    candidates.sort((a, b) {
      final c = score(a).compareTo(score(b));
      return c == 0 ? a.id.compareTo(b.id) : c;
    });
    if (candidates.isEmpty) return [];
    if (skill == 'comprension') {
      final first = candidates.first;
      return banco
          .where(
            (q) =>
                q.skill == skill &&
                q.pasajeId == first.pasajeId &&
                (!nivelFijo || q.nivel == nivel),
          )
          .toList();
    }
    return candidates.take(limite).toList();
  }

  static String motivo(
    String skill,
    Map<String, dynamic>? diagnostico,
    Map<String, dynamic> practicas,
  ) {
    final rs = practicas.values
        .whereType<Map>()
        .where(
          (r) =>
              r['skill'] == skill &&
              (r['idioma'] == null || r['idioma'] == 'en'),
        )
        .toList();
    final errores = rs.where((r) => r['correcta'] == false).length;
    if (errores > 0) {
      return tr(
        '{n} actividades con errores por reforzar. Practica y comprueba con ejemplos nuevos.',
        {'n': errores},
      );
    }
    if (rs.isNotEmpty) {
      return tr('Continúa con ejemplos nuevos y repasa lo que ya has trabajado.');
    }
    if ((diagnostico?['skills'] as Map?)?.containsKey(skill) ?? false) {
      return tr(
        'Seleccionado a partir de tu diagnóstico inicial. Afinaremos el perfil con tus respuestas.',
      );
    }
    return tr(
      'Aún necesitamos observar esta habilidad. Empieza con una práctica breve.',
    );
  }
}
