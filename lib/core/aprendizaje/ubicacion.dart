import 'dart:math';

import 'modelos.dart';

/// Diagnóstico de ubicación v2 (DEC-025, docs/claude-educacion/DIAGNOSTICO_V2.md).
///
/// Estimación bayesiana por habilidad sobre los niveles 0–10: cada respuesta
/// actualiza la probabilidad de cada nivel y la siguiente pregunta de esa
/// habilidad se pide en el nivel mediano. Las demás habilidades informan
/// con menos peso (están correlacionadas). Una habilidad se cierra cuando la
/// estimación es segura (±1 nivel con 85 %) o tras 6 preguntas; si todo
/// apunta a cero conocimientos, se termina enseguida. Así un alumno A1 no
/// ve preguntas de B2 y el diagnóstico dura unos 8 minutos.
/// Simulación de referencia (tools, 3000 alumnos sintéticos): 92 % de las
/// habilidades a ±1 nivel, inicio a ±1 en el 95 %, ~18 preguntas.

const habilidadesUbicacion = ['escucha', 'lectura', 'gramatica', 'vocabulario'];

const nombresHabilidad = {
  'escucha': 'Escucha',
  'lectura': 'Lectura',
  'gramatica': 'Gramática',
  'vocabulario': 'Vocabulario',
  'escritura': 'Escritura',
};

/// Respuesta a «¿Cuánto inglés sabes?»: centra la estimación inicial.
enum Autodeclaracion {
  nada(0),
  poco(1),
  defiendo(3),
  bastante(5),
  avanzado(7);

  const Autodeclaracion(this.inicio);
  final int inicio;

  /// Desde el nivel que el alumno eligió en el registro (0–10).
  static Autodeclaracion desdeNivel(int nivel) => nivel <= 0
      ? nada
      : nivel <= 2
      ? poco
      : nivel <= 4
      ? defiendo
      : nivel <= 6
      ? bastante
      : avanzado;
}

class ItemUbicacion {
  const ItemUbicacion({
    required this.nivel,
    required this.habilidad,
    required this.item,
  });

  final int nivel;
  final String habilidad;
  final Item item;

  factory ItemUbicacion.fromJson(Map<String, dynamic> j) => ItemUbicacion(
    nivel: (j['nivel'] as num).toInt(),
    habilidad: j['habilidad'] as String,
    item: Item.fromJson(j),
  );

  static List<ItemUbicacion> banco(Map<String, dynamic> json) => [
    for (final i in json['items'] as List)
      ItemUbicacion.fromJson(i as Map<String, dynamic>),
  ];
}

class RespuestaUbicacion {
  const RespuestaUbicacion(this.item, this.correcta);
  final ItemUbicacion item;
  final bool correcta;
}

class ResultadoUbicacion {
  const ResultadoUbicacion({
    required this.nivel,
    required this.habilidades,
    required this.preguntas,
    required this.aciertos,
    this.escritura,
  });

  /// Nivel de inicio (0 = empezar desde cero, 1–10 = N1–N10).
  final int nivel;

  /// Nivel por habilidad objetiva (0–10).
  final Map<String, int> habilidades;

  /// Nivel de escritura, o null si se omitió.
  final int? escritura;
  final int preguntas, aciertos;

  bool get desdeCero => nivel == 0;

  /// Habilidades por debajo del nivel de inicio (para reforzar).
  List<String> get reforzar => [
    for (final e in habilidades.entries)
      if (e.value < nivel) e.key,
    if (escritura != null && escritura! < nivel) 'escritura',
  ];

  Map<String, dynamic> toJson() => {
    'nivel': nivel,
    'habilidades': habilidades,
    'escritura': ?escritura,
    'preguntas': preguntas,
    'aciertos': aciertos,
    'reforzar': reforzar,
  };
}

class Ubicacion {
  Ubicacion({
    required List<ItemUbicacion> banco,
    required this.declarado,
    this.maxPreguntas = 22,
    Random? random,
  }) : _banco = List.of(banco),
       _rnd = random ?? Random() {
    final w = [
      for (var t = 0; t <= 10; t++)
        exp(-pow(t - declarado.inicio, 2) / (2 * _sd * _sd)),
    ];
    final s = w.reduce((a, b) => a + b);
    _prior = [for (final x in w) x / s];
  }

  static const _sd = 3.0;
  static const _pesoOtras = 0.4;
  static const _minPorHabilidad = 3, _maxPorHabilidad = 6;
  static const _umbral = 0.85;

  final Autodeclaracion declarado;
  final int maxPreguntas;
  final List<ItemUbicacion> _banco;
  final Random _rnd;
  late final List<double> _prior;
  final _usados = <String>{};
  final respuestas = <RespuestaUbicacion>[];
  final _cerradas = <String>{};
  int _turno = 0;
  bool _sinBase = false;

  ItemUbicacion? actual;
  bool escrituraHecha = false;
  bool escrituraOmitida = false;
  int? nivelEscritura;

  int get n => respuestas.length;
  bool get objetivasTerminadas =>
      declarado == Autodeclaracion.nada ||
      _sinBase ||
      _cerradas.length == habilidadesUbicacion.length;
  bool get terminado =>
      objetivasTerminadas &&
      (declarado == Autodeclaracion.nada ||
          _sinBase ||
          escrituraHecha ||
          escrituraOmitida);

  /// Progreso aproximado (0–1) para la barra.
  double get progreso {
    if (terminado) return 1;
    final porHabilidad = [
      for (final h in habilidadesUbicacion)
        _cerradas.contains(h)
            ? 1.0
            : min(_objetivas(h).length, _maxPorHabilidad) /
                  (_maxPorHabilidad + 1),
    ];
    return (porHabilidad.reduce((a, b) => a + b) /
            (habilidadesUbicacion.length + 1))
        .clamp(0, .95);
  }

  List<RespuestaUbicacion> _objetivas(String h) => [
    for (final r in respuestas)
      if (r.item.habilidad == h) r,
  ];

  /// Probabilidad de acertar un ítem de nivel [nivel] con nivel real [t].
  static double _pAcierto(int nivel, int t, double azar) => nivel <= t
      ? .92
      : nivel == t + 1
      ? .45
      : azar;

  static double _azar(ItemUbicacion i) =>
      i.item.opciones.length >= 2 ? 1 / i.item.opciones.length : .05;

  /// Distribución del nivel de una habilidad (o conjunta si [h] es null).
  List<double> _posterior(String? h) {
    final p = List.of(_prior);
    for (final r in respuestas) {
      if (r.item.habilidad == 'escritura') continue;
      final peso = h == null || r.item.habilidad == h ? 1.0 : _pesoOtras;
      final azar = _azar(r.item);
      for (var t = 0; t <= 10; t++) {
        final q = _pAcierto(r.item.nivel, t, azar);
        p[t] *= pow(r.correcta ? q : 1 - q, peso);
      }
    }
    final s = p.reduce((a, b) => a + b);
    return [for (final x in p) x / s];
  }

  static int _mediana(List<double> p) {
    var a = 0.0;
    for (var t = 0; t <= 10; t++) {
      a += p[t];
      if (a >= .5) return t;
    }
    return 10;
  }

  static int _moda(List<double> p) {
    var m = 0;
    for (var t = 1; t <= 10; t++) {
      if (p[t] > p[m]) m = t;
    }
    return m;
  }

  static double _seguridad(List<double> p) {
    final m = _moda(p);
    var s = 0.0;
    for (var t = max(0, m - 1); t <= min(10, m + 1); t++) {
      s += p[t];
    }
    return s;
  }

  /// Nivel estimado de una habilidad (0–10).
  int nivelDe(String h) => _sinBase ? 0 : _moda(_posterior(h));

  /// Siguiente pregunta objetiva; null cuando toca la escritura o terminó.
  ItemUbicacion? siguiente() {
    if (declarado == Autodeclaracion.nada) return actual = null;
    if (n >= 3 && _posterior(null)[0] >= _umbral) _sinBase = true;
    if (_sinBase || n >= maxPreguntas) {
      _cerradas.addAll(habilidadesUbicacion);
    }
    final abiertas = [
      for (final h in habilidadesUbicacion)
        if (!_cerradas.contains(h)) h,
    ];
    if (abiertas.isEmpty) return actual = null;
    final h = abiertas[_turno++ % abiertas.length];
    final objetivo = _mediana(_posterior(h)).clamp(1, 10);
    final item = _elegir(h, objetivo);
    if (item == null) {
      _cerradas.add(h);
      return siguiente();
    }
    return actual = item;
  }

  /// Ítem sin usar de la habilidad en el nivel pedido o el más cercano.
  ItemUbicacion? _elegir(String habilidad, int nivel) {
    for (final d in [0, -1, 1, -2, 2]) {
      final candidatos = [
        for (final i in _banco)
          if (i.habilidad == habilidad &&
              i.nivel == nivel + d &&
              !_usados.contains(i.item.id))
            i,
      ];
      if (candidatos.isNotEmpty) {
        final i = candidatos[_rnd.nextInt(candidatos.length)];
        _usados.add(i.item.id);
        return i;
      }
    }
    return null;
  }

  void responder(bool correcta) {
    final a = actual;
    if (a == null) return;
    respuestas.add(RespuestaUbicacion(a, correcta));
    actual = null;
    if (a.habilidad == 'escritura') {
      escrituraHecha = true;
      nivelEscritura = correcta ? a.nivel : max(0, a.nivel - 1);
      return;
    }
    final h = a.habilidad;
    final hechas = _objetivas(h).length;
    if ((hechas >= _minPorHabilidad && _seguridad(_posterior(h)) >= _umbral) ||
        hechas >= _maxPorHabilidad) {
      _cerradas.add(h);
    }
  }

  /// Nivel de inicio: media de las habilidades objetivas redondeada hacia
  /// abajo, sin superar en más de 2 a la más débil.
  int get nivelInicio {
    if (declarado == Autodeclaracion.nada || _sinBase) return 0;
    final v = [for (final h in habilidadesUbicacion) nivelDe(h)];
    final media = v.reduce((a, b) => a + b) / v.length;
    return min(media.floor(), v.reduce(min) + 2).clamp(0, 10);
  }

  /// Tarea de escritura en el nivel estimado (null si no hay o empieza de cero).
  ItemUbicacion? escritura() {
    final nivel = nivelInicio;
    if (nivel == 0) {
      escrituraOmitida = true;
      return actual = null;
    }
    final item = _elegir('escritura', nivel);
    if (item == null) escrituraOmitida = true;
    return actual = item;
  }

  void omitirEscritura() {
    escrituraOmitida = true;
    actual = null;
  }

  ResultadoUbicacion resultado() => ResultadoUbicacion(
    nivel: nivelInicio,
    habilidades: {for (final h in habilidadesUbicacion) h: nivelDe(h)},
    escritura: nivelEscritura,
    preguntas: n,
    aciertos: respuestas.where((r) => r.correcta).length,
  );
}
