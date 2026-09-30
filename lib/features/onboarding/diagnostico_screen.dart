import '../../shared/widgets/activity_loading.dart';
import '../../shared/widgets/feedback_experience.dart';

import 'dart:math';
import 'dart:convert';

import 'package:flutter/material.dart';

import '../../core/perfil_aprendizaje.dart';
import '../../core/biblioteca.dart';
import '../../shared/widgets/perfil_seleccion.dart';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/content/contenido_json.dart';
import '../../core/content/curriculum.dart';
import '../../core/diagnostico.dart';
import '../../core/efectos.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/widgets.dart';

/// Diagnóstico adaptativo de nivel: parte del nivel declarado, mide una
/// competencia distinta en cada pregunta (elegir, completar, escuchar, dictado,
/// detectar el error, producción escrita…), sube o baja la dificultad según las
/// respuestas y termina con un perfil por competencias y un plan de refuerzo.
class DiagnosticoScreen extends ConsumerStatefulWidget {
  const DiagnosticoScreen({
    super.key,
    this.idioma,
    this.configuracion = const {},
  });
  final Map<String, dynamic> configuracion;
  final String? idioma;

  /// Resultado + resumen y plan de la IA (si los hubo), listo para guardar en el alumno.
  static Map<String, dynamic> diagnosticoJson(
    ResultadoDiag r,
    Map<String, dynamic>? perfil,
  ) {
    final j = r.toJson();
    if (perfil != null) {
      j['resumenIa'] = perfil['resumen'];
      j['recomendacionesIa'] = perfil['recomendaciones'];
      j['interpretacionIa'] = perfil['plan'];
    }
    return j;
  }

  @override
  ConsumerState<DiagnosticoScreen> createState() => _DiagnosticoScreenState();
}

class _DiagnosticoScreenState extends ConsumerState<DiagnosticoScreen> {
  static const _auto = [
    (
      'Nunca lo he estudiado',
      'Empiezo desde cero: letras, sonidos y palabras',
      0,
    ),
    ('Sé lo básico', 'Saludos, números, frases sueltas', 2),
    (
      'Me defiendo',
      'Situaciones sencillas: comprar, preguntar, presentarme',
      4,
    ),
    (
      'Converso con soltura',
      'Hablo de mi vida y mi trabajo sin mucho esfuerzo',
      6,
    ),
    ('Nivel avanzado', 'Debato, leo textos largos, entiendo acentos', 8),
  ];

  int? autoevaluacion;
  int declarado = 4;
  Diagnostico? diag;
  PreguntaDiag? q;
  ResultadoDiag? resultado;
  String seleccion = '';
  bool? correcto;
  EvaluacionEscritura? evaluacion;
  bool evaluando = false;
  bool reproduciendo = false;
  bool mostrarTexto = false;
  final texto = TextEditingController();
  String? idiomaAnterior;
  bool bancoListo = false;
  bool cargando = false;
  String? errorCarga;
  String? errorEscritura;
  bool audioListo = false;
  int reproducciones = 0;
  List<String> fichas = [];
  final orden = <int>[];
  final evidencias = <Map<String, dynamic>>[];
  late String nativo;
  late List<String> sectores, objetivos;
  String get _draftKey =>
      'onelingo.diagnostico.v2.${Sync.instancia.usuarioId}.$idiomaContenido';
  String get _perfilKey => jsonEncode([declarado, nativo, sectores, objetivos]);

  bool get esOnboarding => widget.configuracion['onboarding'] == true;
  bool get personalizado => idiomaContenido == 'en';
  Map<String, dynamic>? perfilIa;
  bool perfilCargando = false;

  @override
  void initState() {
    super.initState();
    final st = ref.read(progressProvider);
    nativo = widget.configuracion['nativo'] as String? ?? st.idiomaNativo;
    sectores = List<String>.from(
      widget.configuracion['sectores'] as List? ?? st.sectores,
    );
    objetivos = List<String>.from(
      widget.configuracion['objetivos'] as List? ?? st.objetivos,
    );
    declarado = (widget.configuracion['nivel'] as int? ?? st.nivelInicial)
        .clamp(0, 10);
    autoevaluacion = declarado == 0
        ? 0
        : declarado <= 2
        ? 1
        : declarado <= 4
        ? 2
        : declarado <= 6
        ? 3
        : 4;
    final meta =
        widget.configuracion['idioma'] as String? ??
        widget.idioma ??
        st.idiomaMeta;
    if (meta != idiomaContenido) {
      idiomaAnterior = idiomaContenido;
      idiomaContenido = meta;
    }
    // El banco sembrado se carga aquí: desde el registro aún no se ha precargado el idioma.
    ContenidoJson.precargar(idiomaContenido).then((_) {
      if (mounted) setState(() => bancoListo = true);
    });
  }

  /// La IA redacta la pregunta que pide el motor (nivel, competencia, tipo); null si no hay servidor.
  Future<PreguntaDiag?> _generar(PeticionDiag peticion) async {
    final r = await Sync.instancia.generarPreguntaDiag({
      ...peticion.toJson(),
      'idiomaMeta': idiomaContenido,
      'idiomaNativo': nativo,
      'sectores': sectores,
      'objetivos': objetivos,
      'personalizar': [3, 4, 7, 9].contains(diag!.n),
    });
    if (r == null) return null;
    try {
      return PreguntaDiag.fromJson(r);
    } catch (_) {
      return null;
    }
  }

  @override
  void dispose() {
    Voz.instancia.parar();
    texto.dispose();
    if (idiomaAnterior != null) idiomaContenido = idiomaAnterior!;
    super.dispose();
  }

  void _empezar() {
    diag = Diagnostico(
      declarado: declarado,
      banco: BancoDiag.de(idiomaContenido),
      generador: Sync.instancia.conectado ? _generar : null,
      personalizado: personalizado,
      sectores: sectores,
      objetivos: objetivos,
    );
    final raw = ref.read(prefsProvider).getString(_draftKey);
    if (raw != null && personalizado) {
      try {
        final draft = jsonDecode(raw) as Map<String, dynamic>;
        if (draft['perfil'] == _perfilKey) {
          for (final data in (draft['evidencias'] as List)) {
            final e = Map<String, dynamic>.from(data as Map);
            final p = PreguntaDiag.fromJson(
              Map<String, dynamic>.from(
                e['pregunta'] as Map? ??
                    {
                      ...e,
                      'correcta': -1,
                      'opciones': <String>[],
                      'aceptadas': [
                        if ((e['esperada'] as String? ?? '').isNotEmpty)
                          e['esperada'],
                      ],
                    },
              ),
            );
            diag!.actual = p;
            if (p.esEscritura) {
              final w = e['escritura'] as Map;
              diag!.registrarEscritura(
                e['respuesta'] as String,
                EvaluacionEscritura(
                  puntuacion: (w['puntuacion'] as num).toDouble(),
                  comentario: w['comentario'] as String,
                  correccion: w['correccion'] as String,
                  errores: List<String>.from(w['errores'] as List),
                ),
              );
            } else {
              diag!.responder(e['respuesta'] as String);
            }
            evidencias.add(e);
          }
        }
      } catch (_) {
        evidencias.clear();
        diag = Diagnostico(
          declarado: declarado,
          banco: BancoDiag.de(idiomaContenido),
          generador: _generar,
          personalizado: personalizado,
          sectores: sectores,
          objetivos: objetivos,
        );
      }
    }
    setState(() {});
    _siguiente();
  }

  Future<void> _siguiente() async {
    final d = diag!;
    await Voz.instancia.parar();
    if (!mounted) return;
    setState(() {
      cargando = true;
      seleccion = '';
      correcto = null;
      evaluacion = null;
      mostrarTexto = false;
      texto.clear();
      errorCarga = null;
      errorEscritura = null;
      audioListo = false;
      reproducciones = 0;
      orden.clear();
    });
    PreguntaDiag? p;
    ResultadoDiag? finalizado;
    try {
      p = await d.siguienteAsync();
      if (p == null) finalizado = d.resultado();
    } catch (_) {
      if (mounted) {
        setState(() {
          cargando = false;
          errorCarga = 'No pudimos generar la pregunta. Comprueba tu conexión y reintenta; tus respuestas se conservan.';
        });
      }
      return;
    }
    if (!mounted) return;
    setState(() {
      cargando = false;
      q = p;
      fichas = p?.tipo == TipoDiag.ordenar
          ? (p!.aceptadas.first.split(RegExp(r'\s+'))..shuffle(Random()))
          : [];
      resultado = finalizado;
    });
    if (p == null) {
      Efectos.completado();
      _pedirPerfil();
    }
  }

  /// Resumen y plan redactados por la IA a partir del resultado numérico.
  Future<void> _pedirPerfil() async {
    final r = resultado;
    if (r == null || !Sync.instancia.conectado) return;
    setState(() => perfilCargando = true);
    final p = await Sync.instancia.perfilDiag(
      idiomaMeta: idiomaContenido,
      idiomaNativo: nativo,
      resultado: {
        ...r.toJson(),
        'sectores': sectores,
        'objetivos': objetivos,
        'evidencias': evidencias,
        'actividadesDisponibles': [
          for (final skill in RutaBiblioteca.habilidades)
            ...RutaBiblioteca.seleccionar(
              banco: BancoDiag.de('en'),
              nivel: r.recomendado.clamp(1, 10),
              skill: skill,
              sectores: sectores,
              objetivos: objetivos,
              limite: 2,
            ).map(
              (q) => {
                'id': q.id,
                'skill': q.skill,
                'nivel': q.nivel,
                'tema': q.tema,
              },
            ),
        ],
        'orientativo': true,
        'feedbackInmediato': true,
        'noEvaluado': ['expresión oral'],
      },
    );
    if (!mounted) return;
    setState(() {
      perfilCargando = false;
      perfilIa = p;
    });
  }

  Future<void> _escuchar() async {
    final p = q;
    if (p == null || reproduciendo) return;
    setState(() => reproduciendo = true);
    final ok = await VozNube.instancia.reproducir(
      p.texto,
      idiomaContenido,
      lento: p.nivel <= 3,
    );
    if (!mounted || q != p) return;
    setState(() {
      reproduciendo = false;
      if (ok) {
        audioListo = true;
        reproducciones++;
      }
    });
    if (!ok && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'No se pudo reproducir el audio. Toca para reintentar; no afecta a tu puntuación.',
          ),
        ),
      );
    }
  }

  void _registrarEvidencia(
    PreguntaDiag p,
    String respuesta, {
    bool? correcta,
    EvaluacionEscritura? escritura,
  }) {
    evidencias.add({
      'pregunta': p.toJson(),
      'numero': evidencias.length + 1,
      'nivel': p.nivel,
      'skill': p.skill,
      'tipo': p.tipo.name,
      'tema': p.tema,
      'instruccion': p.instruccion,
      'texto': p.texto,
      'respuesta': respuesta,
      'correcta': correcta,
      'esperada': p.respuestaCorrecta,
      'explicacion': p.explicacion,
      'reproducciones': reproducciones,
      if (escritura != null)
        'escritura': {
          'puntuacion': escritura.puntuacion,
          'comentario': escritura.comentario,
          'correccion': escritura.correccion,
          'errores': escritura.errores,
        },
    });
    ref
        .read(prefsProvider)
        .setString(
          _draftKey,
          jsonEncode({'perfil': _perfilKey, 'evidencias': evidencias}),
        );
  }

  void _comprobar() {
    final p = q!;
    if (correcto != null || (p.esAuditiva && !audioListo)) return;
    final respuesta = p.tipo == TipoDiag.ordenar
        ? orden.map((i) => fichas[i]).join(' ')
        : p.conOpciones
        ? seleccion
        : texto.text.trim();
    if (respuesta.isEmpty) return;
    final ok = diag!.responder(respuesta);
    _registrarEvidencia(p, respuesta, correcta: ok);
    ok ? Efectos.correcto() : Efectos.incorrecto();
    setState(() {
      correcto = ok;
      mostrarTexto = true;
    });
  }

  Future<void> _enviarEscritura() async {
    final p = q!;
    final t = texto.text.trim();
    if (t.isEmpty || (p.nivel > 2 && t.split(RegExp(r'\s+')).length < 3)) {
      return;
    }
    if (evaluando || evaluacion != null) return;
    setState(() {
      evaluando = true;
      errorEscritura = null;
    });
    final r = await Sync.instancia.evaluarEscritura(
      idiomaMeta: idiomaContenido,
      idiomaNativo: nativo,
      nivelEstimado: diag!.estimacion,
      consigna: p.texto,
      texto: t,
    );
    if (!mounted) return;
    if (r == null) {
      setState(() {
        evaluando = false;
        errorEscritura = 'No pudimos evaluar tu texto. Puedes reenviarlo sin perderlo; no se asignó una nota.';
      });
      return;
    }
    final e = EvaluacionEscritura(
      puntuacion: (r['puntuacion'] as num).toDouble(),
      correccion: r['correccion'] as String? ?? '',
      comentario: r['comentario'] as String? ?? '',
      errores: ((r['errores'] as List?) ?? []).cast<String>(),
    );
    diag!.registrarEscritura(t, e);
    _registrarEvidencia(p, t, escritura: e);
    if (!mounted) return;
    final ok = e.puntuacion >= diag!.estimacion - 0.5;
    ok ? Efectos.correcto() : Efectos.incorrecto();
    setState(() {
      evaluando = false;
      evaluacion = e;
      correcto = e.puntuacion >= diag!.estimacion - 0.5;
    });
  }

  Map<String, dynamic> _diagnosticoJson() => {
    ...DiagnosticoScreen.diagnosticoJson(resultado!, perfilIa),
    'idioma': idiomaContenido,
    'idiomaNativo': nativo,
    'sectores': sectores,
    'objetivos': objetivos,
    'evidencias': evidencias,
    'version': 3,
    // Nombre comercial de la escala; `escala` identifica la del resultado.
    'escalaPresentacion': 'onelingo-10-a1-c1-v1',
    'orientativo': true,
    'feedbackInmediato': true,
    'noEvaluado': ['expresión oral'],
  };

  void _terminar(int nivel) {
    final r = resultado!;
    ref.read(prefsProvider).remove(_draftKey);

    Sync.instancia.evento('diagnostico', {
      'nivelEstimado': r.nivel,
      'cefr': r.cefr,
      'nivelElegido': nivel,
      'preguntas': r.preguntas,
      'precision': (r.precision * 100).round(),
      'idioma': idiomaContenido,
      'debilidades': r.debilidades,
    });
    final st = ref.read(progressProvider);
    if (st.onboardingDone && !esOnboarding) {
      ref.read(progressProvider.notifier).guardarPerfil(sectores, objetivos);
      ref
          .read(progressProvider.notifier)
          .guardarDiagnostico(
            _diagnosticoJson(),
            st.idiomaMeta == idiomaContenido ? nivel : st.nivelInicial,
          );
    }
    if (context.canPop()) {
      context.pop({..._diagnosticoJson(), 'elegido': nivel});
    } else {
      context.go('/inicio');
    }
  }

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context).textTheme;
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.close),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/inicio'),
        ),
        title: const Text('Diagnóstico de nivel'),
        actions: const [SoundToggle()],
      ),
      body: Movil(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 8, 20, 20),
          child: diag == null
              ? _intro(t)
              : resultado != null
              ? _resultado(t)
              : q != null && !cargando
              ? FeedbackMotion(key: ValueKey(q!.clave), child: _pregunta(t))
              : _pregunta(t),
        ),
      ),
    );
  }

  // ---------------- Intro ----------------
  Widget _intro(TextTheme t) {
    final meta = idioma(idiomaContenido);
    return ListView(
      children: [
        Text('Comprobemos tu ${meta.nombre}', style: t.headlineMedium),
        const SizedBox(height: 6),
        const Text(
          'Partimos del nivel elegido y ajustamos la dificultad. En inglés: 10 actividades de lectura, listening, vocabulario, gramática y escritura, con una explicación después de cada respuesta.',
          style: TextStyle(color: OL.gris, height: 1.4),
        ),
        const SizedBox(height: 16),
        if (!esOnboarding)
          for (var i = 0; i < _auto.length; i++)
            Padding(
              padding: const EdgeInsets.only(bottom: 10),
              child: Tarjeta(
                onTap: () => setState(() {
                  autoevaluacion = i;
                  declarado = _auto[i].$3;
                  Efectos.toque();
                }),
                borde: autoevaluacion == i ? OL.morado : null,
                color: autoevaluacion == i ? OL.moradoSuave : OL.blanco,
                child: Row(
                  children: [
                    Icon(
                      autoevaluacion == i
                          ? Icons.radio_button_checked
                          : Icons.radio_button_off,
                      color: autoevaluacion == i ? OL.morado : OL.grisClaro,
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            _auto[i].$1,
                            style: const TextStyle(fontWeight: FontWeight.w700),
                          ),
                          Text(
                            _auto[i].$2,
                            style: const TextStyle(
                              color: OL.gris,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
        if (!esOnboarding && autoevaluacion != null && autoevaluacion! > 0) ...[
          const SizedBox(height: 6),
          Text(
            'Ajusta el nivel en el que crees estar: $declarado de 10',
            style: const TextStyle(fontWeight: FontWeight.w700),
          ),
          Slider(
            value: declarado.toDouble(),
            min: 1,
            max: 10,
            divisions: 9,
            label: '$declarado',
            activeColor: OL.morado,
            onChanged: (v) => setState(() => declarado = v.round()),
          ),
          Text(
            'La prueba empieza en el nivel $declarado y se ajusta sola. Elegir bien ahorra preguntas.',
            style: const TextStyle(color: OL.gris, fontSize: 12),
          ),
        ],
        const SizedBox(height: 16),
        Text(
          'Punto de partida: nivel $declarado',
          style: const TextStyle(fontWeight: FontWeight.w700),
        ),
        if (!esOnboarding)
          PerfilSeleccion(
            sectores: sectores,
            objetivos: objetivos,
            onChanged: (s, o) => setState(() {
              sectores = s;
              objetivos = o;
            }),
          ),
        if (esOnboarding)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 12),
            child: Text(
              '${sectores.map((s) => sectoresAprendizaje[s] ?? s).join(' · ')}\n${objetivos.map((s) => objetivosAprendizaje[s] ?? s).join(' · ')}',
            ),
          ),
        const SizedBox(height: 16),
        ElevatedButton(
          onPressed:
              !bancoListo ||
                  !Sync.instancia.conectado ||
                  (personalizado && (sectores.isEmpty || objetivos.isEmpty))
              ? null
              : _empezar,
          child: const Text('EMPEZAR EL DIAGNÓSTICO'),
        ),
        const SizedBox(height: 8),
        if (!Sync.instancia.conectado)
          TextButton(
            onPressed: () => context.push('/login'),
            child: const Text('Inicia sesión para realizar el diagnóstico'),
          ),
        const Text(
          'Resultado orientativo para personalizar tu aprendizaje. La expresión oral no se evalúa en esta prueba.',
          textAlign: TextAlign.center,
          style: TextStyle(color: OL.gris, fontSize: 12),
        ),
      ],
    );
  }

  // ---------------- Pregunta ----------------
  Widget _pregunta(TextTheme t) {
    final d = diag!;
    final p = q;
    if (errorCarga != null) {
      return Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.cloud_off, size: 42, color: OL.morado),
          const SizedBox(height: 16),
          Text(errorCarga!, textAlign: TextAlign.center),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: _siguiente,
            child: const Text('REINTENTAR'),
          ),
        ],
      );
    }
    if (cargando || p == null) {
      return SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: ActivityLoading(
          label: 'Seleccionando una actividad para ti…',
          detail: 'Dificultad ${d.nivelActual} · ${d.n} respondidas',
        ),
      );
    }
    final respondida = correcto != null || evaluacion != null;
    final progreso = ((d.n + (respondida ? 0 : 1)) / d.minPreguntas).clamp(
      0.0,
      0.95,
    );
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Row(
          children: [
            Expanded(child: BarraProgreso(progreso, color: OL.naranja)),
            const SizedBox(width: 10),
            Etiqueta('Dificultad ${p.nivel}', color: OL.morado),
          ],
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 6,
          runSpacing: 6,
          children: [
            Etiqueta(
              'Pregunta ${d.n + (respondida ? 0 : 1)}${personalizado ? ' de 10' : ''}',
              color: OL.gris,
              fondo: OL.fondo,
            ),
            Etiqueta(
              skillsDiag[p.skill] ?? p.skill,
              color: OL.morado,
              fondo: OL.moradoSuave,
            ),
            Etiqueta(
              tiposDiagNombre[p.tipo] ?? '',
              color: OL.naranja,
              fondo: OL.naranjaSuave,
              icono: p.esAuditiva
                  ? Icons.headphones
                  : p.esEscritura
                  ? Icons.edit_outlined
                  : Icons.quiz_outlined,
            ),
            if (d.origenActual == 'ia')
              const Etiqueta(
                'IA',
                color: OL.verde,
                fondo: OL.verdeSuave,
                icono: Icons.auto_awesome,
              ),
          ],
        ),
        const SizedBox(height: 14),
        Expanded(
          child: ListView(
            children: [
              Text(
                p.instruccion,
                style: const TextStyle(
                  color: OL.gris,
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 6),
              if (!p.esAuditiva && p.imagen.isNotEmpty) ...[
                ClipRRect(
                  borderRadius: BorderRadius.circular(20),
                  child: Image.asset(
                    p.imagen,
                    height: 180,
                    width: double.infinity,
                    fit: BoxFit.cover,
                    excludeFromSemantics: true,
                  ),
                ),
                const SizedBox(height: 12),
              ],
              if (p.esAuditiva) _audio(p, respondida) else _enunciado(p),
              const SizedBox(height: 14),
              if (p.conOpciones) ..._opciones(p),
              if (p.tipo == TipoDiag.ordenar) _ordenar(p, respondida),
              if (!p.conOpciones &&
                  !p.esEscritura &&
                  p.tipo != TipoDiag.ordenar)
                _campo(p),
              if (p.esEscritura) _escritura(p),
            ],
          ),
        ),
        if (respondida) FeedbackDock(child: _feedback(p)),
        const SizedBox(height: 8),
        _boton(p, respondida),
      ],
    );
  }

  Widget _enunciado(PreguntaDiag p) => Tarjeta(
    color: OL.moradoSuave,
    sombra: false,
    child: Text(
      p.texto,
      style: const TextStyle(
        fontSize: 17,
        fontWeight: FontWeight.w600,
        height: 1.45,
      ),
    ),
  );

  Widget _audio(PreguntaDiag p, bool respondida) => Tarjeta(
    color: OL.moradoSuave,
    sombra: false,
    onTap: reproduciendo ? null : _escuchar,
    etiquetaSemantica: audioListo
        ? 'Volver a escuchar el audio'
        : 'Escuchar audio',
    child: Column(
      children: [
        AnimatedScale(
          scale: reproduciendo ? 1.08 : 1.0,
          duration: const Duration(milliseconds: 250),
          child: const IconoCuadro(
            Icons.volume_up_rounded,
            tamano: 72,
            radio: 36,
            relleno: true,
          ),
        ),
        const SizedBox(height: 10),
        Text(
          reproduciendo
              ? 'Preparando audio…'
              : audioListo
              ? 'Volver a escuchar'
              : 'Escuchar audio',
          style: const TextStyle(color: OL.gris, fontSize: 12),
        ),
        if (mostrarTexto || respondida) ...[
          const SizedBox(height: 10),
          Text(
            p.texto,
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              height: 1.4,
            ),
          ),
        ],
      ],
    ),
  );

  List<Widget> _opciones(PreguntaDiag p) => [
    for (final o in p.opciones)
      Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: AnimatedScale(
          scale: seleccion == o && correcto == null ? 1.03 : 1.0,
          duration: const Duration(milliseconds: 160),
          curve: Curves.easeOutBack,
          child: _Opcion(
            texto: o,
            seleccionada: seleccion == o,
            estado: correcto == null
                ? null
                : (o == p.respuestaCorrecta
                      ? true
                      : (seleccion == o ? false : null)),
            onTap: correcto == null
                ? () {
                    Efectos.toque();
                    setState(() => seleccion = o);
                  }
                : null,
          ),
        ),
      ),
  ];

  Widget _ordenar(PreguntaDiag p, bool respondida) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      const Text(
        'Toca las palabras para formar la frase. Toca una palabra elegida para devolverla.',
      ),
      const SizedBox(height: 12),
      Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: OL.moradoSuave,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Wrap(
          spacing: 6,
          runSpacing: 6,
          children: [
            if (orden.isEmpty) const Text('Tu frase aparecerá aquí'),
            for (final i in orden)
              ActionChip(
                label: Text(fichas[i]),
                onPressed: respondida
                    ? null
                    : () => setState(() => orden.remove(i)),
              ),
          ],
        ),
      ),
      const SizedBox(height: 12),
      Wrap(
        spacing: 6,
        runSpacing: 6,
        children: [
          for (var i = 0; i < fichas.length; i++)
            if (!orden.contains(i))
              ActionChip(
                label: Text(fichas[i]),
                onPressed: respondida
                    ? null
                    : () => setState(() => orden.add(i)),
              ),
        ],
      ),
    ],
  );

  Widget _campo(PreguntaDiag p) => TextField(
    controller: texto,
    enabled: correcto == null,
    autofocus: true,
    textInputAction: TextInputAction.done,
    onChanged: (_) => setState(() {}),
    onSubmitted: (_) => _comprobar(),
    decoration: InputDecoration(
      hintText: p.tipo == TipoDiag.dictado
          ? 'Escribe lo que oíste'
          : p.tipo == TipoDiag.completar
          ? 'Escribe la palabra que falta'
          : 'Escribe tu respuesta',
      prefixIcon: const Icon(Icons.edit_outlined),
    ),
  );

  Widget _escritura(PreguntaDiag p) {
    final palabras = texto.text.trim().isEmpty
        ? 0
        : texto.text.trim().split(RegExp(r'\s+')).length;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        TextField(
          controller: texto,
          enabled: evaluacion == null && !evaluando,
          maxLines: 6,
          minLines: 4,
          onChanged: (_) => setState(() {}),
          decoration: const InputDecoration(
            hintText: 'Escribe 3-5 frases en el idioma que estás aprendiendo, sin traductor.',
          ),
        ),
        const SizedBox(height: 6),
        Text(
          '$palabras palabras · responde a todos los puntos de la consigna',
          style: const TextStyle(color: OL.gris, fontSize: 12),
        ),
        if (errorEscritura != null)
          Text(errorEscritura!, style: const TextStyle(color: OL.rojo)),
        if (evaluando) ...[
          const SizedBox(height: 14),
          const ActivityLoading(
            compact: true,
            label: 'Revisando tu respuesta…',
          ),
        ],
      ],
    );
  }

  Widget _feedback(PreguntaDiag p) {
    final e = evaluacion;
    final ok = correcto ?? false;
    return AnswerFeedback(
      correct: ok,
      title: e != null
          ? 'Escritura: ${e.puntuacion.toStringAsFixed(1)} de 10'
          : ok
          ? '¡Correcto!'
          : 'Vamos a repasarlo',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (e == null && !ok && p.respuestaCorrecta.isNotEmpty) ...[
            const SizedBox(height: 6),
            Text(
              'Respuesta correcta: ${p.respuestaCorrecta}',
              style: const TextStyle(fontWeight: FontWeight.w600),
            ),
          ],
          if (e == null && p.explicacion.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text(
              p.explicacion,
              style: const TextStyle(
                color: OL.gris,
                fontSize: 13,
                height: 1.35,
              ),
            ),
          ],
          if (e != null) ...[
            if (e.correccion.isNotEmpty) ...[
              const SizedBox(height: 8),
              const Text(
                'Versión corregida',
                style: TextStyle(fontWeight: FontWeight.w700, fontSize: 12),
              ),
              Text(e.correccion, style: const TextStyle(height: 1.4)),
            ],
            if (e.comentario.isNotEmpty) ...[
              const SizedBox(height: 6),
              Text(
                e.comentario,
                style: const TextStyle(
                  color: OL.gris,
                  fontSize: 13,
                  height: 1.35,
                ),
              ),
            ],
            if (!e.porIa)
              const Padding(
                padding: EdgeInsets.only(top: 6),
                child: Text(
                  'Sin conexión con la IA: evaluación aproximada.',
                  style: TextStyle(color: OL.gris, fontSize: 11),
                ),
              ),
          ],
        ],
      ),
    );
  }

  Widget _boton(PreguntaDiag p, bool respondida) {
    if (respondida) {
      final ok = correcto ?? false;
      return ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: ok ? OL.verde : OL.rojo,
        ),
        onPressed: _siguiente,
        child: const Text('SIGUIENTE'),
      );
    }
    if (p.esEscritura) {
      final palabras = texto.text.trim().isEmpty
          ? 0
          : texto.text.trim().split(RegExp(r'\s+')).length;
      return ElevatedButton(
        onPressed: palabras >= (p.nivel <= 2 ? 1 : 3) && !evaluando
            ? _enviarEscritura
            : null,
        child: const Text('ENVIAR PARA EVALUAR'),
      );
    }
    final listo =
        (p.tipo == TipoDiag.ordenar
            ? orden.length == fichas.length && orden.isNotEmpty
            : p.conOpciones
            ? seleccion.isNotEmpty
            : texto.text.trim().isNotEmpty) &&
        (!p.esAuditiva || audioListo);
    return ElevatedButton(
      onPressed: listo ? _comprobar : null,
      child: const Text('COMPROBAR'),
    );
  }

  List<String> _planMostrado(ResultadoDiag r) {
    return r.plan;
  }

  // ---------------- Resultado ----------------
  Widget _resultado(TextTheme t) {
    final r = resultado!;
    final n = r.recomendado;
    final nivelTexto = r.nivel == r.nivel.roundToDouble()
        ? r.nivel.toInt().toString()
        : r.nivel.toStringAsFixed(1);
    return ListView(
      children: [
        const SizedBox(height: 6),
        Center(
          child: AnilloProgreso(
            valor: r.nivel / 10,
            tamano: 140,
            color: OL.morado,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  nivelTexto,
                  style: const TextStyle(
                    fontSize: 38,
                    fontWeight: FontWeight.w800,
                    height: 1,
                  ),
                ),
                const Text(
                  'de 10',
                  style: TextStyle(color: OL.gris, fontSize: 12),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 14),
        Text(
          n == 0
              ? 'Tu punto de partida: Fundamentos'
              : 'Nivel orientativo: $nivelTexto',
          textAlign: TextAlign.center,
          style: t.headlineMedium,
        ),
        const SizedBox(height: 4),
        Text(
          '${r.preguntas} actividades · ${evidencias.where((e) => e['correcta'] == true).length}/${evidencias.where((e) => e['correcta'] != null).length} respuestas objetivas correctas',
          textAlign: TextAlign.center,
          style: const TextStyle(color: OL.gris, fontSize: 13),
        ),
        const SizedBox(height: 16),
        const Text(
          'Perfil inicial basado en pocas muestras por competencia. Seguiremos afinándolo con la práctica. Expresión oral: no evaluada.',
          style: TextStyle(color: OL.gris, fontSize: 12),
        ),
        const SizedBox(height: 12),
        const TituloSeccion('Por competencia'),
        const SizedBox(height: 8),
        Tarjeta(
          child: Column(
            children: [
              for (final e in r.skills.entries)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 5),
                  child: Row(
                    children: [
                      SizedBox(
                        width: 150,
                        child: Text(
                          '${skillsDiag[e.key] ?? e.key} (${evidencias.where((x) => x['skill'] == e.key).length})',
                          style: const TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      Expanded(
                        child: BarraProgreso(
                          e.value / 10,
                          color: e.value >= r.nivel + 0.5
                              ? OL.verde
                              : e.value <= r.nivel - 0.5
                              ? OL.rojo
                              : OL.morado,
                        ),
                      ),
                      const SizedBox(width: 8),
                      SizedBox(
                        width: 34,
                        child: Text(
                          e.value.toStringAsFixed(1),
                          textAlign: TextAlign.right,
                          style: const TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
            ],
          ),
        ),
        if (r.fortalezas.isNotEmpty || r.debilidades.isNotEmpty) ...[
          const SizedBox(height: 12),
          Wrap(
            spacing: 6,
            runSpacing: 6,
            children: [
              for (final f in r.fortalezas)
                Etiqueta(
                  f,
                  color: OL.verde,
                  fondo: OL.verdeSuave,
                  icono: Icons.thumb_up_outlined,
                ),
              for (final d in r.debilidades)
                Etiqueta(
                  d,
                  color: OL.rojo,
                  fondo: OL.rojoSuave,
                  icono: Icons.fitness_center,
                ),
            ],
          ),
        ],
        if (r.refuerzo.isNotEmpty) ...[
          const SizedBox(height: 16),
          const TituloSeccion('Qué reforzar'),
          const SizedBox(height: 8),
          Tarjeta(
            color: OL.moradoSuave,
            sombra: false,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                for (final x in r.refuerzo.take(8))
                  Padding(
                    padding: const EdgeInsets.only(bottom: 4),
                    child: Text('• $x', style: const TextStyle(height: 1.35)),
                  ),
                if (r.recurrentes.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(top: 6),
                    child: Text(
                      'Errores repetidos: ${r.recurrentes.join(', ')}',
                      style: const TextStyle(color: OL.gris, fontSize: 12),
                    ),
                  ),
              ],
            ),
          ),
        ],
        if (perfilCargando || perfilIa != null) ...[
          const SizedBox(height: 16),
          const TituloSeccion('Lo que dice tu profesor de IA'),
          const SizedBox(height: 8),
          Tarjeta(
            child: perfilCargando
                ? const Row(
                    children: [
                      SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      ),
                      SizedBox(width: 10),
                      Text(
                        'Redactando tu resumen…',
                        style: TextStyle(color: OL.gris),
                      ),
                    ],
                  )
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        perfilIa!['resumen'] as String? ?? '',
                        style: const TextStyle(height: 1.45),
                      ),
                      const SizedBox(height: 8),
                      for (final rec
                          in ((perfilIa!['recomendaciones'] as List?) ?? [])
                              .cast<String>())
                        Padding(
                          padding: const EdgeInsets.only(bottom: 4),
                          child: Text(
                            '• $rec',
                            style: const TextStyle(fontSize: 13, height: 1.35),
                          ),
                        ),
                    ],
                  ),
          ),
        ],
        const SizedBox(height: 16),
        const TituloSeccion('Tu plan inicial'),
        const SizedBox(height: 8),
        Tarjeta(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              for (var i = 0; i < _planMostrado(r).length; i++)
                Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      CircleAvatar(
                        radius: 11,
                        backgroundColor: OL.morado,
                        child: Text(
                          '${i + 1}',
                          style: const TextStyle(
                            color: OL.blanco,
                            fontSize: 11,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          _planMostrado(r)[i],
                          style: const TextStyle(height: 1.35, fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              Text(
                n > 1
                    ? 'Tu punto de partida es el nivel $n. Esto no acredita el dominio de todas las habilidades anteriores: el refuerzo seguirá atendiendo sus dificultades.'
                    : n == 1
                    ? 'Empezarás desde el principio, con las bases del idioma.'
                    : 'Antes de formar frases aprenderás las letras y sus sonidos, los números, los colores y las palabras básicas.',
                style: const TextStyle(
                  color: OL.gris,
                  fontSize: 12,
                  height: 1.4,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        ElevatedButton(
          onPressed: perfilCargando ? null : () => _terminar(n),
          child: Text(
            n == 0 ? 'EMPEZAR POR FUNDAMENTOS' : 'EMPEZAR EN EL NIVEL $n',
          ),
        ),
        if (!perfilCargando && n > 1)
          TextButton(
            onPressed: () => _terminar(n - 1),
            child: Text('Prefiero empezar un nivel más abajo (Nivel ${n - 1})'),
          ),
        if (!perfilCargando && n == 1)
          TextButton(
            onPressed: () => _terminar(0),
            child: const Text(
              'Prefiero empezar por Fundamentos (letras y sonidos)',
            ),
          ),
      ],
    );
  }
}

class _Opcion extends StatelessWidget {
  const _Opcion({
    required this.texto,
    required this.seleccionada,
    this.estado,
    this.onTap,
  });
  final String texto;
  final bool seleccionada;
  final bool? estado;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final Color borde = estado == true
        ? OL.verde
        : estado == false
        ? OL.rojo
        : seleccionada
        ? OL.morado
        : OL.grisClaro;
    final Color fondo = estado == true
        ? OL.verdeSuave
        : estado == false
        ? OL.rojoSuave
        : seleccionada
        ? OL.moradoSuave
        : OL.blanco;
    return Material(
      color: fondo,
      borderRadius: BorderRadius.circular(14),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(14),
            border: Border.all(
              color: borde,
              width: seleccionada || estado != null ? 2 : 1.5,
            ),
          ),
          child: Row(
            children: [
              Expanded(
                child: Text(
                  texto,
                  style: const TextStyle(
                    fontWeight: FontWeight.w600,
                    height: 1.3,
                  ),
                ),
              ),
              if (estado == true)
                const Icon(Icons.check_circle, color: OL.verde, size: 20),
              if (estado == false)
                const Icon(Icons.cancel, color: OL.rojo, size: 20),
            ],
          ),
        ),
      ),
    );
  }
}
