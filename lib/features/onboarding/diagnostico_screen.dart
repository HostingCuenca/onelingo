import '../../core/barajar.dart';
import '../../shared/widgets/activity_loading.dart';
import '../../shared/widgets/feedback_experience.dart';

import 'dart:convert';

import 'package:flutter/material.dart';

import '../../core/aprendizaje/ubicacion.dart' show Autodeclaracion;
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
import '../../core/i18n/i18n.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/widgets.dart';
import '../ruta/opcion_respuesta.dart';

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
  /// «¿Cuánto sabes?» solo fija la dificultad de la primera pregunta (como
  /// la prueba v2 de inglés); el resultado sale únicamente de las respuestas.
  static Map<Autodeclaracion, String> get _etiquetasAuto => {
    Autodeclaracion.nada: tr('Nada'),
    Autodeclaracion.poco: tr('Un poco'),
    Autodeclaracion.defiendo: tr('Me defiendo'),
    Autodeclaracion.bastante: tr('Bastante'),
    Autodeclaracion.avanzado: tr('Avanzado'),
  };

  late Autodeclaracion autoevaluacion;
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
    // El nivel del registro solo elige el punto de partida (0/1/3/5/7).
    autoevaluacion = Autodeclaracion.desdeNivel(
      (widget.configuracion['nivel'] as int? ?? st.nivelInicial).clamp(0, 10),
    );
    declarado = autoevaluacion.inicio;
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
          errorCarga = tr(
            'No pudimos generar la pregunta. Comprueba tu conexión y reintenta; tus respuestas se conservan.',
          );
        });
      }
      return;
    }
    if (!mounted) return;
    setState(() {
      cargando = false;
      q = p;
      fichas = p?.tipo == TipoDiag.ordenar
          ? barajarDistinto(p!.aceptadas.first.split(RegExp(r'\s+')))
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
              banco: BancoDiag.de(idiomaContenido),
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
        SnackBar(
          content: Text(
            tr(
              'No se pudo reproducir el audio. Toca para reintentar; no afecta a tu puntuación.',
            ),
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
        errorEscritura = tr(
          'No pudimos evaluar tu texto. Puedes reenviarlo sin perderlo; no se asignó una nota.',
        );
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
        title: Text(tr('Diagnóstico de nivel')),
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
        Text(
          tr('Comprobemos tu {idioma}', {
            'idioma': _nombreIdioma(meta.code, meta.nombre),
          }),
          style: t.headlineMedium,
        ),
        const SizedBox(height: 6),
        Text(
          tr(
            'Partimos del nivel elegido y ajustamos la dificultad. En inglés: 10 actividades de lectura, listening, vocabulario, gramática y escritura, con una explicación después de cada respuesta.',
          ),
          style: const TextStyle(color: OL.gris, height: 1.4),
        ),
        const SizedBox(height: 16),
        if (!esOnboarding) ...[
          Text(
            tr('¿Cuánto {idioma} sabes?', {
              'idioma': _nombreIdioma(meta.code, meta.nombre),
            }),
            style: const TextStyle(fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              for (final a in Autodeclaracion.values)
                ChoiceChip(
                  label: Text(_etiquetasAuto[a]!),
                  selected: autoevaluacion == a,
                  onSelected: (_) => setState(() {
                    autoevaluacion = a;
                    declarado = a.inicio;
                    Efectos.toque();
                  }),
                ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            tr(
              'Solo decide por dónde empezamos. Tu nivel sale de tus respuestas.',
            ),
            style: const TextStyle(color: OL.gris, fontSize: 12),
          ),
          const SizedBox(height: 16),
        ],
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
              '${sectores.map(_sector).join(' · ')}\n${objetivos.map(_objetivo).join(' · ')}',
            ),
          ),
        const SizedBox(height: 16),
        BotonPrincipal(
          onPressed:
              !bancoListo ||
                  !Sync.instancia.conectado ||
                  (personalizado && (sectores.isEmpty || objetivos.isEmpty))
              ? null
              : _empezar,
          child: Text(tr('EMPEZAR EL DIAGNÓSTICO')),
        ),
        const SizedBox(height: 8),
        if (!Sync.instancia.conectado)
          TextButton(
            onPressed: () => context.push('/login'),
            child: Text(tr('Inicia sesión para realizar el diagnóstico')),
          ),
        Text(
          tr(
            'Tu resultado sale solo de tus respuestas. La expresión oral no se evalúa en esta prueba.',
          ),
          textAlign: TextAlign.center,
          style: const TextStyle(color: OL.gris, fontSize: 12),
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
          BotonPrincipal(
            onPressed: _siguiente,
            child: Text(tr('REINTENTAR')),
          ),
        ],
      );
    }
    if (cargando || p == null) {
      return SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: ActivityLoading(
          label: tr('Seleccionando una actividad para ti…'),
          detail: tr('Dificultad {nivel} · {n} respondidas', {
            'nivel': d.nivelActual,
            'n': d.n,
          }),
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
            Etiqueta(
              tr('Dificultad {nivel}', {'nivel': p.nivel}),
              color: OL.morado,
            ),
          ],
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 6,
          runSpacing: 6,
          children: [
            Etiqueta(
              personalizado
                  ? tr('Pregunta {n} de 10', {'n': d.n + (respondida ? 0 : 1)})
                  : tr('Pregunta {n}', {'n': d.n + (respondida ? 0 : 1)}),
              color: OL.gris,
              fondo: OL.fondo,
            ),
            Etiqueta(
              _skill(p.skill),
              color: OL.morado,
              fondo: OL.moradoSuave,
            ),
            Etiqueta(
              _tipo(p.tipo),
              color: OL.naranja,
              fondo: OL.naranjaSuave,
              icono: p.esAuditiva
                  ? Icons.headphones
                  : p.esEscritura
                  ? Icons.edit_outlined
                  : Icons.quiz_outlined,
            ),
            if (d.origenActual == 'ia')
              Etiqueta(
                tr('IA'),
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
        ? tr('Volver a escuchar el audio')
        : tr('Escuchar audio'),
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
              ? tr('Preparando audio…')
              : audioListo
              ? tr('Volver a escuchar')
              : tr('Escuchar audio'),
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
      OpcionRespuesta(
        texto: o,
        estado: correcto == null
            ? (seleccion == o ? EstadoOpcion.seleccionada : EstadoOpcion.normal)
            : (o == p.respuestaCorrecta
                  ? EstadoOpcion.correcta
                  : (seleccion == o
                        ? EstadoOpcion.incorrecta
                        : EstadoOpcion.normal)),
        onTap: correcto == null
            ? () {
                Efectos.toque();
                setState(() => seleccion = o);
              }
            : null,
      ),
  ];

  Widget _ordenar(PreguntaDiag p, bool respondida) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      Text(
        tr(
          'Toca las palabras para formar la frase. Toca una palabra elegida para devolverla.',
        ),
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
            if (orden.isEmpty) Text(tr('Tu frase aparecerá aquí')),
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
          ? tr('Escribe lo que oíste')
          : p.tipo == TipoDiag.completar
          ? tr('Escribe la palabra que falta')
          : tr('Escribe tu respuesta'),
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
          decoration: InputDecoration(
            hintText: tr(
              'Escribe 3-5 frases en el idioma que estás aprendiendo, sin traductor.',
            ),
          ),
        ),
        const SizedBox(height: 6),
        Text(
          tr(
            '{n} palabras · responde a todos los puntos de la consigna',
            {'n': palabras},
          ),
          style: const TextStyle(color: OL.gris, fontSize: 12),
        ),
        if (errorEscritura != null)
          Text(errorEscritura!, style: const TextStyle(color: OL.rojo)),
        if (evaluando) ...[
          const SizedBox(height: 14),
          ActivityLoading(
            compact: true,
            label: tr('Revisando tu respuesta…'),
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
          ? tr('Escritura: {nota} de 10', {
              'nota': e.puntuacion.toStringAsFixed(1),
            })
          : ok
          ? tr('¡Correcto!')
          : tr('Vamos a repasarlo'),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (e == null && !ok && p.respuestaCorrecta.isNotEmpty) ...[
            const SizedBox(height: 6),
            Text(
              tr('Respuesta correcta: {respuesta}', {
                'respuesta': p.respuestaCorrecta,
              }),
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
              Text(
                tr('Versión corregida'),
                style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 12),
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
              Padding(
                padding: const EdgeInsets.only(top: 6),
                child: Text(
                  tr('Sin conexión con la IA: evaluación aproximada.'),
                  style: const TextStyle(color: OL.gris, fontSize: 11),
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
      return BotonPrincipal(
        color: ok ? OL.verde : OL.rojo,
        onPressed: _siguiente,
        child: Text(tr('SIGUIENTE')),
      );
    }
    if (p.esEscritura) {
      final palabras = texto.text.trim().isEmpty
          ? 0
          : texto.text.trim().split(RegExp(r'\s+')).length;
      return BotonPrincipal(
        onPressed: palabras >= (p.nivel <= 2 ? 1 : 3) && !evaluando
            ? _enviarEscritura
            : null,
        child: Text(tr('ENVIAR PARA EVALUAR')),
      );
    }
    final listo =
        (p.tipo == TipoDiag.ordenar
            ? orden.length == fichas.length && orden.isNotEmpty
            : p.conOpciones
            ? seleccion.isNotEmpty
            : texto.text.trim().isNotEmpty) &&
        (!p.esAuditiva || audioListo);
    return BotonPrincipal(
      onPressed: listo ? _comprobar : null,
      child: Text(tr('COMPROBAR')),
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
                Text(
                  tr('de 10'),
                  style: const TextStyle(color: OL.gris, fontSize: 12),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 14),
        Text(
          n == 0
              ? tr('Tu punto de partida: Fundamentos')
              : tr('Tu nivel: {nivel}', {'nivel': nivelTexto}),
          textAlign: TextAlign.center,
          style: t.headlineMedium,
        ),
        const SizedBox(height: 4),
        Text(
          tr(
            '{actividades} actividades · {aciertos}/{total} respuestas objetivas correctas',
            {
              'actividades': r.preguntas,
              'aciertos': evidencias.where((e) => e['correcta'] == true).length,
              'total': evidencias.where((e) => e['correcta'] != null).length,
            },
          ),
          textAlign: TextAlign.center,
          style: const TextStyle(color: OL.gris, fontSize: 13),
        ),
        const SizedBox(height: 16),
        Text(
          tr(
            'Perfil inicial basado en pocas muestras por competencia. Seguiremos afinándolo con la práctica. Expresión oral: no evaluada.',
          ),
          style: const TextStyle(color: OL.gris, fontSize: 12),
        ),
        const SizedBox(height: 12),
        TituloSeccion(tr('Por competencia')),
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
                          '${_skill(e.key)} (${evidencias.where((x) => x['skill'] == e.key).length})',
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
          TituloSeccion(tr('Qué reforzar')),
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
                      tr('Errores repetidos: {errores}', {
                        'errores': r.recurrentes.join(', '),
                      }),
                      style: const TextStyle(color: OL.gris, fontSize: 12),
                    ),
                  ),
              ],
            ),
          ),
        ],
        if (perfilCargando || perfilIa != null) ...[
          const SizedBox(height: 16),
          TituloSeccion(tr('Lo que dice tu profesor de IA')),
          const SizedBox(height: 8),
          Tarjeta(
            child: perfilCargando
                ? Row(
                    children: [
                      const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      ),
                      const SizedBox(width: 10),
                      Text(
                        tr('Redactando tu resumen…'),
                        style: const TextStyle(color: OL.gris),
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
        TituloSeccion(tr('Tu plan inicial')),
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
                    ? tr(
                        'Tu punto de partida es el nivel {n}. Esto no acredita el dominio de todas las habilidades anteriores: el refuerzo seguirá atendiendo sus dificultades.',
                        {'n': n},
                      )
                    : n == 1
                    ? tr('Empezarás desde el principio, con las bases del idioma.')
                    : tr(
                        'Antes de formar frases aprenderás las letras y sus sonidos, los números, los colores y las palabras básicas.',
                      ),
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
        BotonPrincipal(
          onPressed: perfilCargando ? null : () => _terminar(n),
          child: Text(
            n == 0
                ? tr('EMPEZAR POR FUNDAMENTOS')
                : tr('EMPEZAR EN EL NIVEL {n}', {'n': n}),
          ),
        ),
        if (!perfilCargando && n > 1)
          TextButton(
            onPressed: () => _terminar(n - 1),
            child: Text(
              tr('Prefiero empezar un nivel más abajo (Nivel {n})', {
                'n': n - 1,
              }),
            ),
          ),
        if (!perfilCargando && n == 1)
          TextButton(
            onPressed: () => _terminar(0),
            child: Text(
              tr('Prefiero empezar por Fundamentos (letras y sonidos)'),
            ),
          ),
      ],
    );
  }
}

/// Nombre del idioma en el idioma de la interfaz.
String _nombreIdioma(String code, String nombre) => switch (code) {
  'en' => tr('Inglés'),
  'es' => tr('Español'),
  'fr' => tr('Francés'),
  'de' => tr('Alemán'),
  'pt' => tr('Portugués'),
  'it' => tr('Italiano'),
  'zh' => tr('Chino mandarín'),
  'ja' => tr('Japonés'),
  'ko' => tr('Coreano'),
  'ru' => tr('Ruso'),
  _ => nombre,
};

/// Competencia (`skillsDiag`) en el idioma de la interfaz.
String _skill(String k) => switch (k) {
  'listening' => tr('Listening'),
  'comprension' => tr('Lectura'),
  'vocabulario' => tr('Vocabulario'),
  'gramatica' => tr('Gramática'),
  'tiempos' => tr('Tiempos verbales'),
  'expresiones' => tr('Expresiones naturales'),
  'contexto' => tr('Comprensión contextual'),
  'cotidiano' => tr('Comunicación cotidiana'),
  'escritura' => tr('Escritura'),
  _ => skillsDiag[k] ?? k,
};

/// Formato de la pregunta (`tiposDiagNombre`) en el idioma de la interfaz.
String _tipo(TipoDiag t) => switch (t) {
  TipoDiag.eleccion => tr('Elige'),
  TipoDiag.natural => tr('La más natural'),
  TipoDiag.significado => tr('Significado'),
  TipoDiag.contexto => tr('Comprensión'),
  TipoDiag.situacion => tr('Situación'),
  TipoDiag.error => tr('Detecta el error'),
  TipoDiag.completar => tr('Completa'),
  TipoDiag.corta => tr('Respuesta corta'),
  TipoDiag.ordenar => tr('Ordena la frase'),
  TipoDiag.escucha => tr('Escucha'),
  TipoDiag.dictado => tr('Dictado'),
  TipoDiag.escritura => tr('Escribe'),
};

/// Sector (`sectoresAprendizaje`) en el idioma de la interfaz.
String _sector(String s) => switch (s) {
  'estudiante' => tr('Estudiante'),
  'tecnologia' => tr('Tecnología e ingeniería'),
  'salud' => tr('Salud y bienestar'),
  'negocios' => tr('Negocios y administración'),
  'ventas' => tr('Ventas y atención al cliente'),
  'educacion' => tr('Educación e investigación'),
  'turismo' => tr('Turismo y hostelería'),
  'general' => tr('Otros sectores / vida cotidiana'),
  _ => sectoresAprendizaje[s] ?? s,
};

/// Objetivo (`objetivosAprendizaje`) en el idioma de la interfaz.
String _objetivo(String s) => switch (s) {
  'conversar' => tr('Conversar con confianza'),
  'trabajar' => tr('Reuniones y trabajo en equipo'),
  'entrevistas' => tr('Entrevistas y oportunidades'),
  'viajar' => tr('Viajar y vivir en otro país'),
  'estudiar' => tr('Estudiar y entender contenidos'),
  'clientes' => tr('Atender y comunicarme con clientes'),
  'escribir' => tr('Escribir mensajes y correos'),
  'escuchar' => tr('Entender conversaciones y videos'),
  _ => objetivosAprendizaje[s] ?? s,
};
