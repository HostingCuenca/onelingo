import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../api/sync.dart';
import '../content/catalog.dart';
import '../content/contenido_json.dart';
import '../content/curriculum.dart';
import '../models/models.dart';

/// Se inyecta en `main` con `overrideWithValue`.
final prefsProvider = Provider<SharedPreferences>((_) => throw UnimplementedError());

/// Todo el estado del estudiante. En fase 2 vive en el servidor; aquí se
/// persiste en el dispositivo para que la demo funcione sin backend.
/// Si el nombre es un correo (el alumno escribió el correo en el campo del nombre), se muestra la parte anterior a la @.
String nombreLimpio(String nombre, {String? email}) {
  var n = nombre.trim();
  if (n.contains('@')) n = n.split('@').first;
  if (n.isEmpty && email != null && email.contains('@')) n = email.split('@').first;
  if (n.isEmpty) return 'Alumno';
  return n[0].toUpperCase() + n.substring(1);
}

/// `--dart-define=DESBLOQUEAR_TODO=true`: compilación de prueba con todos los
/// niveles y lecciones abiertos (para revisar contenido sin recorrer el camino).
const desbloquearTodo = bool.fromEnvironment('DESBLOQUEAR_TODO');

class ProgressState {
  const ProgressState({
    this.onboardingDone = false,
    this.nombre = 'Bryan',
    this.email = '',
    this.idiomaNativo = 'es',
    this.idiomaMeta = 'en',
    this.nivelInicial = 1,
    this.fundamentos = false,
    this.diagnostico,
    this.completadas = const {},
    this.puntuaciones = const {},
    this.examenes = const {},
    this.errores = const [],
    this.xp = 0,
    this.racha = 0,
    this.ultimoDia = '',
    this.segundosEstudio = 0,
    this.trialInicio,
    this.trialSegundos = 0,
    this.tutorId = 'mia',
    this.planId = '',
  });

  final bool onboardingDone;
  final String nombre;
  final String email;
  final String idiomaNativo;
  final String idiomaMeta;
  final int nivelInicial;
  /// Recomendado por la prueba de nivel: empezar por el Nivel 0 (Fundamentos).
  final bool fundamentos;
  /// Resultado del diagnóstico adaptativo (nivel, competencias, refuerzo, plan).
  final Map<String, dynamic>? diagnostico;
  final Set<String> completadas; // ids de lección
  final Map<String, int> puntuaciones; // id → % aciertos
  final Map<int, int> examenes; // nivel → % (último intento)
  final List<Mistake> errores;
  final int xp;
  final int racha;
  final String ultimoDia; // yyyy-mm-dd
  final int segundosEstudio;
  final DateTime? trialInicio;
  final int trialSegundos;
  final String tutorId;
  final String planId;

  // ---- Reglas de desbloqueo (ARQUITECTURA §3) ----

  bool nivelDesbloqueado(int k) {
    if (desbloquearTodo) return true;
    if (k <= nivelInicial) return true;
    for (var i = nivelInicial; i < k; i++) {
      if ((examenes[i] ?? 0) < Level.minimoAprobacion) return false;
    }
    return true;
  }

  /// Fundamentos pendientes: recomendados y sin terminar.
  bool get fundamentosPendientes => fundamentos && leccionesDe(0).isNotEmpty && completadasEnNivel(0) < totalLeccionesDe(0);

  int get nivelActual {
    if (fundamentosPendientes) return 0;
    var n = nivelInicial;
    while (n < 10 && nivelDesbloqueado(n + 1)) {
      n++;
    }
    return n;
  }

  int completadasEnNivel(int n) =>
      completadas.where((id) => id.startsWith('L$n-')).length;

  bool examenDesbloqueado(int n) =>
      nivelDesbloqueado(n) && completadasEnNivel(n) >= totalLeccionesDe(n);

  bool examenAprobado(int n) => (examenes[n] ?? 0) >= Level.minimoAprobacion;

  bool get programaCompletado => examenAprobado(10);

  LessonState estadoLeccion(Lesson l) {
    if (completadas.contains(l.id)) return LessonState.completada;
    if (!nivelDesbloqueado(l.nivel)) return LessonState.bloqueada;
    if (desbloquearTodo) return LessonState.actual;
    if (l.numero == 1) return LessonState.actual;
    final anterior = 'L${l.nivel}-${(l.numero - 1).toString().padLeft(3, '0')}';
    return completadas.contains(anterior) ? LessonState.actual : LessonState.bloqueada;
  }

  Lesson? leccionActual(int n) {
    for (final l in leccionesDe(n)) {
      if (estadoLeccion(l) == LessonState.actual) return l;
    }
    return null;
  }

  double progresoNivel(int n) => completadasEnNivel(n) / totalLeccionesDe(n);

  int get trialRestante {
    if (planId.isNotEmpty) return segundosPruebaGratis;
    return (segundosPruebaGratis - trialSegundos).clamp(0, segundosPruebaGratis);
  }

  bool get trialAgotado => planId.isEmpty && trialInicio != null && trialRestante == 0;

  Map<Skill, int> get porHabilidad {
    final m = <Skill, int>{for (final s in Skill.values) s: 0};
    for (final id in completadas) {
      final l = leccionPorId(id);
      if (l == null) continue;
      for (final s in l.steps) {
        m[s.skill] = (m[s.skill] ?? 0) + 1;
      }
    }
    return m;
  }

  int get vocabularioAprendido {
    var n = 0;
    for (final id in completadas) {
      final l = leccionPorId(id);
      if (l == null) continue;
      n += l.steps.where((s) => s.type == StepType.flashcard).length;
      n += l.steps.where((s) => s.type == StepType.matchPairs).fold(0, (a, s) => a + s.pairs.length);
    }
    return n;
  }

  ProgressState copyWith({
    bool? onboardingDone,
    String? nombre,
    String? email,
    String? idiomaNativo,
    String? idiomaMeta,
    int? nivelInicial,
    bool? fundamentos,
    Map<String, dynamic>? diagnostico,
    Set<String>? completadas,
    Map<String, int>? puntuaciones,
    Map<int, int>? examenes,
    List<Mistake>? errores,
    int? xp,
    int? racha,
    String? ultimoDia,
    int? segundosEstudio,
    DateTime? trialInicio,
    int? trialSegundos,
    String? tutorId,
    String? planId,
  }) =>
      ProgressState(
        onboardingDone: onboardingDone ?? this.onboardingDone,
        nombre: nombre ?? this.nombre,
        email: email ?? this.email,
        idiomaNativo: idiomaNativo ?? this.idiomaNativo,
        idiomaMeta: idiomaMeta ?? this.idiomaMeta,
        nivelInicial: nivelInicial ?? this.nivelInicial,
        fundamentos: fundamentos ?? this.fundamentos,
        diagnostico: diagnostico ?? this.diagnostico,
        completadas: completadas ?? this.completadas,
        puntuaciones: puntuaciones ?? this.puntuaciones,
        examenes: examenes ?? this.examenes,
        errores: errores ?? this.errores,
        xp: xp ?? this.xp,
        racha: racha ?? this.racha,
        ultimoDia: ultimoDia ?? this.ultimoDia,
        segundosEstudio: segundosEstudio ?? this.segundosEstudio,
        trialInicio: trialInicio ?? this.trialInicio,
        trialSegundos: trialSegundos ?? this.trialSegundos,
        tutorId: tutorId ?? this.tutorId,
        planId: planId ?? this.planId,
      );

  Map<String, dynamic> toJson() => {
        'onboardingDone': onboardingDone,
        'nombre': nombre,
        'email': email,
        'idiomaNativo': idiomaNativo,
        'idiomaMeta': idiomaMeta,
        'nivelInicial': nivelInicial,
        'fundamentos': fundamentos,
        if (diagnostico != null) 'diagnostico': diagnostico,
        'completadas': completadas.toList(),
        'puntuaciones': puntuaciones,
        'examenes': examenes.map((k, v) => MapEntry(k.toString(), v)),
        'errores': errores.map((e) => e.toJson()).toList(),
        'xp': xp,
        'racha': racha,
        'ultimoDia': ultimoDia,
        'segundosEstudio': segundosEstudio,
        'trialInicio': trialInicio?.toIso8601String(),
        'trialSegundos': trialSegundos,
        'tutorId': tutorId,
        'planId': planId,
      };

  static ProgressState fromJson(Map<String, dynamic> j) => ProgressState(
        onboardingDone: j['onboardingDone'] as bool? ?? false,
        nombre: j['nombre'] as String? ?? 'Bryan',
        email: j['email'] as String? ?? '',
        idiomaNativo: j['idiomaNativo'] as String? ?? 'es',
        idiomaMeta: j['idiomaMeta'] as String? ?? 'en',
        nivelInicial: j['nivelInicial'] as int? ?? 1,
        fundamentos: j['fundamentos'] as bool? ?? false,
        diagnostico: (j['diagnostico'] as Map?)?.cast<String, dynamic>(),
        completadas: ((j['completadas'] as List?) ?? []).cast<String>().toSet(),
        puntuaciones: ((j['puntuaciones'] as Map?) ?? {}).cast<String, int>(),
        examenes: ((j['examenes'] as Map?) ?? {})
            .map((k, v) => MapEntry(int.parse(k as String), v as int)),
        errores: ((j['errores'] as List?) ?? [])
            .map((e) => Mistake.fromJson((e as Map).cast<String, dynamic>()))
            .toList(),
        xp: j['xp'] as int? ?? 0,
        racha: j['racha'] as int? ?? 0,
        ultimoDia: j['ultimoDia'] as String? ?? '',
        segundosEstudio: j['segundosEstudio'] as int? ?? 0,
        trialInicio: j['trialInicio'] == null ? null : DateTime.parse(j['trialInicio'] as String),
        trialSegundos: j['trialSegundos'] as int? ?? 0,
        tutorId: j['tutorId'] as String? ?? 'mia',
        planId: j['planId'] as String? ?? '',
      );
}

class ProgressNotifier extends StateNotifier<ProgressState> {
  ProgressNotifier(this._prefs) : super(_load(_prefs));

  static const _key = 'onelingo.progress.v1';
  final SharedPreferences _prefs;

  static ProgressState _load(SharedPreferences p) {
    final raw = p.getString(_key);
    if (raw == null) return const ProgressState();
    try {
      final st = ProgressState.fromJson(jsonDecode(raw) as Map<String, dynamic>);
      idiomaContenido = st.idiomaMeta;
      ContenidoJson.precargar(st.idiomaMeta);
      return st;
    } catch (_) {
      return const ProgressState();
    }
  }

  void _save(ProgressState s) {
    idiomaContenido = s.idiomaMeta;
    ContenidoJson.precargar(s.idiomaMeta);
    if (s.onboardingDone) Sync.instancia.subir(s.toJson());
    state = s;
    _prefs.setString(_key, jsonEncode(s.toJson()));
  }

  static String _hoy() {
    final d = DateTime.now();
    return '${d.year}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';
  }

  void terminarOnboarding({
    required String nombre,
    required String idiomaNativo,
    required String idiomaMeta,
    required int nivelInicial,
    bool fundamentos = false,
    Map<String, dynamic>? diagnostico,
    String email = '',
    String password = '',
  }) {
    final correo = email.trim().isEmpty ? '${nombre.trim().toLowerCase().replaceAll(RegExp(r'[^a-z0-9]+'), '.')}@onelingo.demo' : email.trim().toLowerCase();
    final nuevo = state.copyWith(
      onboardingDone: true,
      nombre: nombreLimpio(nombre, email: correo),
      email: correo,
      idiomaNativo: idiomaNativo,
      idiomaMeta: idiomaMeta,
      nivelInicial: nivelInicial,
      fundamentos: fundamentos,
      diagnostico: diagnostico,
      trialInicio: state.trialInicio ?? DateTime.now(),
    );
    final registro = password.trim().length >= 6 && email.trim().isNotEmpty
        ? Sync.instancia.registrarConPassword(email: correo, password: password, nombre: nombre, idiomaNativo: idiomaNativo, idiomaMeta: idiomaMeta, nivelInicial: nivelInicial)
        : Sync.instancia.registrar(email: correo, nombre: nombre, idiomaNativo: idiomaNativo, idiomaMeta: idiomaMeta, nivelInicial: nivelInicial);
    registro.then((_) => Sync.instancia.subir(nuevo.toJson()));
    _save(nuevo);
  }

  /// Tras iniciar sesión real: usa el progreso del servidor si existe; si no, crea el estado inicial.
  void iniciarSesionReal({required String email, required String nombre, Map<String, dynamic>? estadoServidor, String idiomaNativo = 'es', String idiomaMeta = 'en', int nivelInicial = 1}) {
    if (estadoServidor != null && (estadoServidor['onboardingDone'] as bool? ?? false)) {
      _save(ProgressState.fromJson(estadoServidor).copyWith(email: email));
      return;
    }
    _save(ProgressState(onboardingDone: true, nombre: nombreLimpio(nombre, email: email), email: email, idiomaNativo: idiomaNativo, idiomaMeta: idiomaMeta, nivelInicial: nivelInicial, trialInicio: DateTime.now()));
  }

  /// Carga un estado completo (usuarios de prueba / sesión del servidor en fase 2).
  void cargar(ProgressState s, {String? email}) {
    final correo = email ?? s.email;
    final st = s.copyWith(email: correo);
    if (correo.isNotEmpty) {
      Sync.instancia
          .login(email: correo, nombre: st.nombre, idiomaNativo: st.idiomaNativo, idiomaMeta: st.idiomaMeta, nivelInicial: st.nivelInicial)
          .then((_) => Sync.instancia.subir(st.toJson()));
    }
    _save(st);
  }

  void elegirTutor(String id) => _save(state.copyWith(tutorId: id));

  void elegirPlan(String id) => _save(state.copyWith(planId: id));

  /// Suma XP y actualiza la racha (un día nuevo con actividad = +1).
  ProgressState _conActividad(ProgressState s, int xpGanado) {
    final hoy = _hoy();
    var racha = s.racha;
    if (s.ultimoDia != hoy) {
      final ayer = DateTime.now().subtract(const Duration(days: 1));
      final ayerStr =
          '${ayer.year}-${ayer.month.toString().padLeft(2, '0')}-${ayer.day.toString().padLeft(2, '0')}';
      racha = (s.ultimoDia == ayerStr) ? racha + 1 : 1;
    }
    return s.copyWith(xp: s.xp + xpGanado, racha: racha, ultimoDia: hoy);
  }

  void completarLeccion(Lesson l, {required int aciertos, required int total}) {
    Sync.instancia.evento('leccion_completada', {'leccion': l.id, 'aciertos': aciertos, 'total': total});
    final pct = total == 0 ? 100 : (aciertos * 100 / total).round();
    final s = _conActividad(state, l.xp + (pct == 100 ? 5 : 0));
    _save(s.copyWith(
      completadas: {...s.completadas, l.id},
      puntuaciones: {...s.puntuaciones, l.id: pct},
    ));
  }

  void registrarExamen(int nivel, int pct) {
    Sync.instancia.evento('examen', {'nivel': nivel, 'pct': pct});
    final s = _conActividad(state, pct >= Level.minimoAprobacion ? 200 : 20);
    _save(s.copyWith(examenes: {...s.examenes, nivel: pct}));
  }

  void agregarError({
    required Skill skill,
    required String original,
    required String correccion,
    required String explicacion,
    String origen = '',
  }) {
    final m = Mistake(
      id: DateTime.now().microsecondsSinceEpoch.toString(),
      skill: skill,
      original: original,
      correccion: correccion,
      explicacion: explicacion,
      fecha: DateTime.now(),
      origen: origen,
    );
    _save(state.copyWith(errores: [m, ...state.errores].take(200).toList()));
  }

  void marcarErrorPracticado(String id) {
    _save(state.copyWith(
      errores: [for (final e in state.errores) e.id == id ? e.copyWith(practicado: true) : e],
    ));
  }

  /// Latido de uso: la app lo llama cada 30 s en primer plano.
  void sumarSegundos(int seg) {
    _save(state.copyWith(
      segundosEstudio: state.segundosEstudio + seg,
      trialSegundos: state.planId.isEmpty ? state.trialSegundos + seg : state.trialSegundos,
    ));
  }

  void reiniciar() {
    Sync.instancia.cerrarSesion();
    _save(const ProgressState());
  }
}

final progressProvider = StateNotifierProvider<ProgressNotifier, ProgressState>(
  (ref) => ProgressNotifier(ref.watch(prefsProvider)),
);
