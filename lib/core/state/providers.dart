import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../api/sync.dart';
import '../content/catalog.dart';
import '../content/contenido_json.dart';
import '../i18n/i18n.dart';
import '../content/curriculum.dart';
import '../content/fundamentos.dart' show idiomasSoloRutaF0;
import '../diagnostico.dart'
    show
        escalaDiagnosticoCliente,
        escalaDiagnosticoLegacy,
        nivelClienteDesdeLegacy;
import '../models/models.dart';

/// Se inyecta en `main` con `overrideWithValue`.
final prefsProvider = Provider<SharedPreferences>(
  (_) => throw UnimplementedError(),
);

/// Todo el estado del estudiante. En fase 2 vive en el servidor; aquí se
/// persiste en el dispositivo para que la demo funcione sin backend.
/// Si el nombre es un correo (el alumno escribió el correo en el campo del nombre), se muestra la parte anterior a la @.
String nombreLimpio(String nombre, {String? email}) {
  var n = nombre.trim();
  if (n.contains('@')) n = n.split('@').first;
  if (n.isEmpty && email != null && email.contains('@')) {
    n = email.split('@').first;
  }
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
    this.idiomaInterfaz,
    this.idiomaMeta = 'en',
    this.nivelInicial = 1,
    this.nivelEscala = escalaDiagnosticoLegacy,
    this.nivelClienteInicial,
    this.fundamentos = false,
    this.diagnostico,
    this.practicas = const {},
    this.sectores = const [],
    this.objetivos = const [],
    this.completadas = const {},
    this.puntuaciones = const {},
    this.examenes = const {},
    this.errores = const [],
    this.xp = 0,
    this.racha = 0,
    this.ultimoDia = '',
    this.diasActividad = const {},
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

  /// Idioma de la interfaz elegido en Perfil (null = según el nativo).
  final String? idiomaInterfaz;

  /// Idioma en que se ve la app y los textos de apoyo del contenido.
  String get interfaz => idiomaInterfaz ?? idiomaInterfazPara(idiomaNativo);
  final String idiomaMeta;

  /// Ubicación histórica usada por la ruta anterior. Nunca se sobrescribe
  /// con un valor de una escala distinta.
  final int nivelInicial;
  final String nivelEscala;
  final int? nivelClienteInicial;

  int get nivelCliente =>
      nivelClienteInicial ??
      (nivelEscala == escalaDiagnosticoCliente
          ? nivelInicial.clamp(0, 10)
          : nivelClienteDesdeLegacy(nivelInicial));

  /// Recomendado por la prueba de nivel: empezar por el Nivel 0 (Fundamentos).
  final bool fundamentos;

  /// Resultado del diagnóstico adaptativo (nivel, competencias, refuerzo, plan).
  final Map<String, dynamic>? diagnostico;
  final Map<String, dynamic> practicas;
  final List<String> sectores, objetivos;
  final Set<String> completadas; // ids de lección
  final Map<String, int> puntuaciones; // id → % aciertos
  final Map<int, int> examenes; // nivel → mejor resultado; conserva logros
  final List<Mistake> errores;
  final int xp;
  final int racha;
  final String ultimoDia; // yyyy-mm-dd
  final Set<String> diasActividad; // días reales observados, yyyy-mm-dd
  final int segundosEstudio;
  final DateTime? trialInicio;
  final int trialSegundos;
  final String tutorId;
  final String planId;

  /// Ayer sigue vigente: todavía se puede estudiar hoy. No inventa historial.
  int get rachaVigente => rachaEn(DateTime.now());

  int rachaEn(DateTime fecha) {
    final ultima = DateTime.tryParse(ultimoDia);
    if (ultima == null || racha < 1) return 0;
    final hoy = DateTime.utc(fecha.year, fecha.month, fecha.day);
    final dia = DateTime.utc(ultima.year, ultima.month, ultima.day);
    final diferencia = hoy.difference(dia).inDays;
    return diferencia == 0 || diferencia == 1 ? racha : 0;
  }

  // ---- Reglas de desbloqueo (ARQUITECTURA §3) ----

  bool nivelDesbloqueado(int k) {
    if (desbloquearTodo) return true;
    if (k <= nivelInicial) return true;
    for (var i = nivelInicial; i < k; i++) {
      if ((examenes[i] ?? 0) < Level.minimoAprobacion) return false;
    }
    return true;
  }

  /// Fundamentos pendientes: recomendados y sin terminar. Se terminan al
  /// aprobar la ruta de fundamentos del idioma (DEC-007) o, como antes,
  /// completando todas las lecciones antiguas del nivel 0. Los idiomas en
  /// reconstrucción ([idiomasSoloRutaF0]) no tienen lecciones antiguas: solo
  /// cuenta la ruta.
  bool get fundamentosPendientes =>
      fundamentos &&
      !rutaFundamentosAprobada &&
      (idiomasSoloRutaF0.contains(idiomaMeta) ||
          leccionesDe(0).isNotEmpty &&
              completadasEnNivel(0) < totalLeccionesDe(0));

  /// Nivel 0 · Leer y pronunciar: recomendado a quien empieza de cero, antes
  /// de Fundamentos, hasta completar sus lecciones (idiomas que lo tienen).
  bool get nivel0Pendiente =>
      const {'en', 'fr', 'es', 'pt', 'de', 'it', 'zh', 'ja', 'ru', 'ko'}.contains(idiomaMeta) &&
      fundamentos &&
      !practicas.containsKey('nivel0:$idiomaMeta:completo');

  /// Marca que escribe la ruta nueva al aprobar todas las unidades de f0.
  bool get rutaFundamentosAprobada =>
      practicas.containsKey('ruta:$idiomaMeta.f0:completa');

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
    return completadas.contains(anterior)
        ? LessonState.actual
        : LessonState.bloqueada;
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
    return (segundosPruebaGratis - trialSegundos).clamp(
      0,
      segundosPruebaGratis,
    );
  }

  bool get trialAgotado =>
      planId.isEmpty && trialInicio != null && trialRestante == 0;

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
      n += l.steps
          .where((s) => s.type == StepType.matchPairs)
          .fold(0, (a, s) => a + s.pairs.length);
    }
    return n;
  }

  ProgressState copyWith({
    bool? onboardingDone,
    String? nombre,
    String? email,
    String? idiomaNativo,
    String? idiomaInterfaz,
    String? idiomaMeta,
    int? nivelInicial,
    String? nivelEscala,
    int? nivelClienteInicial,
    bool? fundamentos,
    Map<String, dynamic>? diagnostico,
    Map<String, dynamic>? practicas,
    List<String>? sectores,
    List<String>? objetivos,
    Set<String>? completadas,
    Map<String, int>? puntuaciones,
    Map<int, int>? examenes,
    List<Mistake>? errores,
    int? xp,
    int? racha,
    String? ultimoDia,
    Set<String>? diasActividad,
    int? segundosEstudio,
    DateTime? trialInicio,
    int? trialSegundos,
    String? tutorId,
    String? planId,
  }) => ProgressState(
    onboardingDone: onboardingDone ?? this.onboardingDone,
    nombre: nombre ?? this.nombre,
    email: email ?? this.email,
    idiomaNativo: idiomaNativo ?? this.idiomaNativo,
    idiomaInterfaz: idiomaInterfaz ?? this.idiomaInterfaz,
    idiomaMeta: idiomaMeta ?? this.idiomaMeta,
    nivelInicial: nivelInicial ?? this.nivelInicial,
    nivelEscala: nivelEscala ?? this.nivelEscala,
    nivelClienteInicial: nivelClienteInicial ?? this.nivelClienteInicial,
    fundamentos: fundamentos ?? this.fundamentos,
    diagnostico: diagnostico ?? this.diagnostico,
    practicas: practicas ?? this.practicas,
    sectores: sectores ?? this.sectores,
    objetivos: objetivos ?? this.objetivos,
    completadas: completadas ?? this.completadas,
    puntuaciones: puntuaciones ?? this.puntuaciones,
    examenes: examenes ?? this.examenes,
    errores: errores ?? this.errores,
    xp: xp ?? this.xp,
    racha: racha ?? this.racha,
    ultimoDia: ultimoDia ?? this.ultimoDia,
    diasActividad: diasActividad ?? this.diasActividad,
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
    'idiomaInterfaz': ?idiomaInterfaz,
    'idiomaMeta': idiomaMeta,
    'nivelInicial': nivelInicial,
    'nivelEscala': nivelEscala,
    'nivelClienteInicial': ?nivelClienteInicial,
    'fundamentos': fundamentos,
    'practicas': practicas,
    'sectores': sectores,
    'objetivos': objetivos,
    if (diagnostico != null) 'diagnostico': diagnostico,
    'completadas': completadas.toList(),
    'puntuaciones': puntuaciones,
    'examenes': examenes.map((k, v) => MapEntry(k.toString(), v)),
    'errores': errores.map((e) => e.toJson()).toList(),
    'xp': xp,
    'racha': racha,
    'ultimoDia': ultimoDia,
    'diasActividad': diasActividad.toList()..sort(),
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
    idiomaInterfaz: j['idiomaInterfaz'] as String?,
    idiomaMeta: j['idiomaMeta'] as String? ?? 'en',
    nivelInicial: j['nivelInicial'] as int? ?? 1,
    nivelEscala: j['nivelEscala'] as String? ?? escalaDiagnosticoLegacy,
    nivelClienteInicial: (j['nivelClienteInicial'] as num?)?.round(),
    fundamentos: j['fundamentos'] as bool? ?? false,
    diagnostico: (j['diagnostico'] as Map?)?.cast<String, dynamic>(),
    practicas: (j['practicas'] as Map?)?.cast<String, dynamic>() ?? {},
    sectores: ((j['sectores'] as List?) ?? []).whereType<String>().toList(),
    objetivos: ((j['objetivos'] as List?) ?? []).whereType<String>().toList(),
    completadas: ((j['completadas'] as List?) ?? []).cast<String>().toSet(),
    puntuaciones: ((j['puntuaciones'] as Map?) ?? {}).cast<String, int>(),
    examenes: ((j['examenes'] as Map?) ?? {}).map(
      (k, v) => MapEntry(int.parse(k as String), v as int),
    ),
    errores: ((j['errores'] as List?) ?? [])
        .map((e) => Mistake.fromJson((e as Map).cast<String, dynamic>()))
        .toList(),
    xp: j['xp'] as int? ?? 0,
    racha: j['racha'] as int? ?? 0,
    ultimoDia: j['ultimoDia'] as String? ?? '',
    diasActividad: j['diasActividad'] is List
        ? (j['diasActividad'] as List).whereType<String>().toSet()
        : {
            if ((j['ultimoDia'] as String? ?? '').isNotEmpty)
              j['ultimoDia'] as String,
          },
    segundosEstudio: j['segundosEstudio'] as int? ?? 0,
    trialInicio: j['trialInicio'] == null
        ? null
        : DateTime.parse(j['trialInicio'] as String),
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
      final st = ProgressState.fromJson(
        jsonDecode(raw) as Map<String, dynamic>,
      );
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
    List<String> sectores = const [],
    List<String> objetivos = const [],
    bool sesionPreparada = false,
  }) {
    final correo = email.trim().isEmpty
        ? '${nombre.trim().toLowerCase().replaceAll(RegExp(r'[^a-z0-9]+'), '.')}@onelingo.demo'
        : email.trim().toLowerCase();
    final nuevo = state.copyWith(
      onboardingDone: true,
      nombre: nombreLimpio(nombre, email: correo),
      email: correo,
      idiomaNativo: idiomaNativo,
      idiomaMeta: idiomaMeta,
      nivelInicial: nivelInicial,
      fundamentos: fundamentos,
      diagnostico: diagnostico,
      // La prueba de nivel v2 ubica directamente en la escala del curso.
      nivelEscala: diagnostico?['escala'] == escalaDiagnosticoCliente
          ? escalaDiagnosticoCliente
          : null,
      nivelClienteInicial: diagnostico?['escala'] == escalaDiagnosticoCliente
          ? (diagnostico!['nivelCliente'] as num).round().clamp(0, 10)
          : null,
      sectores: sectores,
      objetivos: objetivos,
      trialInicio: state.trialInicio ?? DateTime.now(),
    );
    final registro = sesionPreparada
        ? Future.value(true)
        : password.trim().length >= 6 && email.trim().isNotEmpty
        ? Sync.instancia.registrarConPassword(
            email: correo,
            password: password,
            nombre: nombre,
            idiomaNativo: idiomaNativo,
            idiomaMeta: idiomaMeta,
            nivelInicial: nivelInicial,
          )
        : Sync.instancia.registrar(
            email: correo,
            nombre: nombre,
            idiomaNativo: idiomaNativo,
            idiomaMeta: idiomaMeta,
            nivelInicial: nivelInicial,
          );
    registro.then((_) => Sync.instancia.subir(nuevo.toJson()));
    _save(nuevo);
  }

  /// Tras iniciar sesión real: usa el progreso del servidor si existe; si no, crea el estado inicial.
  void iniciarSesionReal({
    required String email,
    required String nombre,
    Map<String, dynamic>? estadoServidor,
    String idiomaNativo = 'es',
    String idiomaMeta = 'en',
    int nivelInicial = 1,
  }) {
    if (estadoServidor != null &&
        (estadoServidor['onboardingDone'] as bool? ?? false)) {
      _save(ProgressState.fromJson(estadoServidor).copyWith(email: email));
      return;
    }
    _save(
      ProgressState(
        onboardingDone: true,
        nombre: nombreLimpio(nombre, email: email),
        email: email,
        idiomaNativo: idiomaNativo,
        idiomaMeta: idiomaMeta,
        nivelInicial: nivelInicial,
        trialInicio: DateTime.now(),
      ),
    );
  }

  /// Carga un estado completo (usuarios de prueba / sesión del servidor en fase 2).
  void cargar(ProgressState s, {String? email}) {
    final correo = email ?? s.email;
    final st = s.copyWith(email: correo);
    if (correo.isNotEmpty) {
      Sync.instancia
          .login(
            email: correo,
            nombre: st.nombre,
            idiomaNativo: st.idiomaNativo,
            idiomaMeta: st.idiomaMeta,
            nivelInicial: st.nivelInicial,
          )
          .then((_) => Sync.instancia.subir(st.toJson()));
    }
    _save(st);
  }

  void guardarPerfil(List<String> sectores, List<String> objetivos) =>
      _save(state.copyWith(sectores: sectores, objetivos: objetivos));

  void guardarDiagnostico(Map<String, dynamic> resultado, int nivel) => _save(
    state.copyWith(
      diagnostico: resultado,
      // `nivelInicial` conserva el valor de la escala histórica. Un
      // diagnóstico cliente nuevo se guarda en su propio campo versionado.
      nivelInicial:
          resultado['idioma'] == state.idiomaMeta &&
              resultado['escala'] != escalaDiagnosticoCliente
          ? nivel.clamp(1, 10)
          : state.nivelInicial,
      nivelEscala: resultado['idioma'] == state.idiomaMeta
          ? (resultado['escala'] as String? ?? escalaDiagnosticoLegacy)
          : state.nivelEscala,
      // Manda el nivel que eligió el alumno, no el recomendado por la prueba.
      nivelClienteInicial: resultado['idioma'] == state.idiomaMeta
          ? (resultado['escala'] == escalaDiagnosticoCliente
                ? nivel.clamp(0, 10)
                : nivelClienteDesdeLegacy(nivel))
          : state.nivelCliente,
      fundamentos: resultado['idioma'] == state.idiomaMeta
          ? nivel == 0
          : state.fundamentos,
    ),
  );

  void registrarPractica(String id, Map<String, dynamic> evidencia) {
    final anterior = state.practicas[id] as Map?;
    final intentos = (anterior?['intentos'] as int? ?? 0) + 1;
    final fecha = DateTime.now().toIso8601String();
    final skill = evidencia['skill'] ?? evidencia['habilidad'];
    // Si el registro antiguo ya se repitió, su primera respuesta es desconocida.
    final primeraCorrecta = anterior == null
        ? evidencia['correcta']
        : anterior['primeraCorrecta'] ??
              (anterior['intentos'] == 1 ? anterior['correcta'] : null);
    final primeraFecha = anterior == null
        ? fecha
        : anterior['primeraFecha'] ??
              (anterior['intentos'] == 1 ? anterior['fecha'] : null);
    _save(
      _conActividad(
        state.copyWith(
          practicas: {
            ...state.practicas,
            id: {
              ...evidencia,
              'skill': ?skill,
              'primeraCorrecta': ?primeraCorrecta,
              'primeraFecha': ?primeraFecha,
              if (evidencia['situacionId'] != null)
                'historial': [
                  ...((anterior?['historial'] as List?) ?? []).skip(
                    ((anterior?['historial'] as List?)?.length ?? 0) > 4
                        ? ((anterior?['historial'] as List).length - 4)
                        : 0,
                  ),
                  if (anterior != null)
                    {
                      'fecha': anterior['fecha'],
                      'correcta': anterior['correcta'],
                    },
                ],
              'intentos': intentos,
              'fecha': fecha,
            },
          },
        ),
        anterior == null ? 5 : 0,
      ),
    );
  }

  /// Repaso de «Mis palabras» (fase D): guarda caja y próxima fecha de cada
  /// palabra respondida en `lexico:<idioma>` y suma 1 XP por acierto.
  void guardarRepasoPalabras(
    String idioma,
    Map<String, List<Object>> cambios,
    int aciertos,
  ) {
    final clave = 'lexico:$idioma';
    final anterior =
        (state.practicas[clave] as Map?)?['palabras'] as Map? ?? const {};
    _save(
      _conActividad(
        state.copyWith(
          practicas: {
            ...state.practicas,
            clave: {
              'palabras': {...anterior, ...cambios},
              'fecha': DateTime.now().toIso8601String(),
            },
          },
        ),
        aciertos,
      ),
    );
  }

  /// Last turn and bounded correction evidence; does not award mastery or XP.
  void guardarTurnoSituacion(
    int id,
    String objetivo,
    Map<String, dynamic> evidencia,
  ) {
    final key = 'situacion-${state.idiomaMeta}-$id-$objetivo';
    final anterior = state.practicas[key] as Map?;
    final historial = [
      ...?anterior?['historial'] as List?,
      if (anterior != null)
        {'fecha': anterior['fecha'], 'feedback': anterior['feedback']},
    ];
    _save(
      state.copyWith(
        practicas: {
          ...state.practicas,
          key: {
            ...evidencia,
            'idioma': state.idiomaMeta,
            'situacionId': id,
            'objetivoId': objetivo,
            'tipo': 'conversacion',
            'fecha': DateTime.now().toIso8601String(),
            'historial': historial
                .skip(historial.length > 5 ? historial.length - 5 : 0)
                .toList(),
          },
        },
      ),
    );
  }

  void elegirTutor(String id) => _save(state.copyWith(tutorId: id));

  void elegirIdiomaInterfaz(String codigo) =>
      _save(state.copyWith(idiomaInterfaz: codigo));

  void elegirPlan(String id) => _save(state.copyWith(planId: id));

  /// Suma XP y actualiza la racha (un día nuevo con actividad = +1).
  ProgressState _conActividad(ProgressState s, int xpGanado) {
    final hoy = _hoy();
    var racha = s.racha;
    if (s.ultimoDia != hoy) {
      racha = s.rachaVigente + 1;
    }
    return s.copyWith(
      xp: s.xp + xpGanado,
      racha: racha,
      ultimoDia: hoy,
      diasActividad: {
        ...s.diasActividad,
        if (s.ultimoDia.isNotEmpty) s.ultimoDia,
        hoy,
      },
    );
  }

  void completarLeccion(Lesson l, {required int aciertos, required int total}) {
    Sync.instancia.evento('leccion_completada', {
      'leccion': l.id,
      'aciertos': aciertos,
      'total': total,
    });
    final pct = total == 0 ? 100 : (aciertos * 100 / total).round();
    // Completar conserva su significado de participación; no demuestra dominio.
    final s = _conActividad(
      state,
      state.completadas.contains(l.id) ? 0 : l.xp + (pct == 100 ? 5 : 0),
    );
    _save(
      s.copyWith(
        completadas: {...s.completadas, l.id},
        puntuaciones: {
          ...s.puntuaciones,
          l.id: pct > (s.puntuaciones[l.id] ?? 0)
              ? pct
              : (s.puntuaciones[l.id] ?? 0),
        },
      ),
    );
  }

  void registrarExamen(int nivel, int pct) {
    Sync.instancia.evento('examen', {'nivel': nivel, 'pct': pct});
    final anterior = state.examenes[nivel];
    final primeraAprobacion =
        pct >= Level.minimoAprobacion &&
        (anterior == null || anterior < Level.minimoAprobacion);
    final s = _conActividad(
      state,
      primeraAprobacion
          ? 200
          : anterior == null
          ? 20
          : 0,
    );
    _save(
      s.copyWith(
        examenes: {
          ...s.examenes,
          nivel: anterior == null || pct > anterior ? pct : anterior,
        },
      ),
    );
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
    _save(
      state.copyWith(
        errores: [
          for (final e in state.errores)
            e.id == id ? e.copyWith(practicado: true) : e,
        ],
      ),
    );
  }

  /// Latido de uso: la app lo llama cada 30 s en primer plano.
  void sumarSegundos(int seg) {
    _save(
      state.copyWith(
        segundosEstudio: state.segundosEstudio + seg,
        trialSegundos: state.planId.isEmpty
            ? state.trialSegundos + seg
            : state.trialSegundos,
      ),
    );
  }

  void reiniciar() {
    Sync.instancia.cerrarSesion();
    _save(const ProgressState());
  }
}

final progressProvider = StateNotifierProvider<ProgressNotifier, ProgressState>(
  (ref) => ProgressNotifier(ref.watch(prefsProvider)),
);
