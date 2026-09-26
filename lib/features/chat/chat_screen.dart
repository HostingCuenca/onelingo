import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:http/http.dart' as http;

import '../../app/theme.dart';
import '../../core/biblioteca.dart';
import '../../core/conexion.dart';
import '../situations/situation_screen.dart';
import '../../core/content/situation_units.dart';
import '../../core/content/catalog.dart';
import '../../core/content/fotos.dart';
import '../../core/api/sync.dart';
import '../../core/perfil_aprendizaje.dart';
import '../../core/content/idiomas.dart';
import '../../core/voz.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Conversación con el tutor de IA (situación o libre).
///
/// Las respuestas y correcciones proceden del backend; los fallos permiten reintentar.
class ChatScreen extends ConsumerStatefulWidget {
  const ChatScreen({
    super.key,
    this.situacionId,
    this.leccionId,
    this.objetivoId,
    this.modo = 'practica',
  });
  final int? situacionId;
  final String? leccionId;
  final String? objetivoId;
  final String modo;

  @override
  ConsumerState<ChatScreen> createState() => _ChatScreenState();
}

class _Msg {
  _Msg(this.texto, {required this.mio, this.sub, this.correccion});
  final String texto;
  final bool mio;
  final String? sub;
  final (String, String, String)?
  correccion; // original, corregido, explicación
}

class _ChatScreenState extends ConsumerState<ChatScreen> {
  final mensajes = <_Msg>[];
  final input = TextEditingController();
  final scroll = ScrollController();
  int turno = 0;
  http.Client? _chatClient;
  bool escuchando = false;
  bool transcribiendo = false;
  bool mostrarAyuda = false;
  bool usoAyuda = false;
  List<String> sugerenciasIA = [];

  void _bajar() => Future.delayed(const Duration(milliseconds: 50), () {
    if (scroll.hasClients) {
      scroll.animateTo(
        scroll.position.maxScrollExtent,
        duration: const Duration(milliseconds: 250),
        curve: Curves.easeOut,
      );
    }
  });
  late final Situation? sit = widget.situacionId == null
      ? null
      : situaciones.where((s) => s.id == widget.situacionId).firstOrNull;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (!TickerMode.valuesOf(context).enabled) {
      escuchando = false;
      transcribiendo = false;
    }
  }

  bool get _visible => mounted && TickerMode.valuesOf(context).enabled;

  @override
  void dispose() {
    _chatClient?.close();
    Oido.instancia.cancelar();
    Voz.instancia.parar();
    super.dispose();
  }

  Future<void> _hablarAlTutor() async {
    if (escuchando) {
      await Oido.instancia.parar();
      if (!mounted) return;
      setState(() => escuchando = false);
      return;
    }
    setState(() {
      escuchando = true;
      input.clear();
    });
    final ok = await Oido.instancia.escuchar(
      _idm,
      (texto, fin) {
        if (!mounted) return;
        setState(() => input.text = texto);
        if (fin) {
          setState(() {
            escuchando = false;
            transcribiendo = false;
          });
          if (texto.trim().isNotEmpty) {
            _enviar(texto);
          }
        }
      },
      segundos: 60,
      silencio: const Duration(seconds: 3),
      onProcesando: () {
        if (mounted) {
          setState(() {
            escuchando = false;
            transcribiendo = true;
          });
        }
      },
      onFin: () {
        if (!mounted || (!escuchando && !transcribiendo)) return;
        setState(() {
          escuchando = false;
          transcribiendo = false;
        });
        if (input.text.trim().isEmpty) {
          final e = Oido.instancia.ultimoError;
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                e.isEmpty
                    ? 'No se escuchó nada. Acércate al micrófono e inténtalo otra vez.'
                    : 'No se pudo escuchar ($e). Comprueba el micrófono.',
              ),
            ),
          );
        }
      },
    );
    if (!ok && mounted) {
      setState(() => escuchando = false);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Micrófono no disponible en este dispositivo. Escribe tu respuesta.',
          ),
        ),
      );
    }
  }

  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      if (!mounted) return;
      if (widget.objetivoId != null) {
        _responderConIA(ref.read(progressProvider).nivelActual);
        return;
      }
      final n = ref.read(progressProvider).nivelActual;
      setState(
        () => mensajes.add(
          _Msg(_apertura(n), mio: false, sub: _traduccionApertura(n)),
        ),
      );
      Voz.instancia.hablar(
        _apertura(n),
        _idm,
        voz: ref.read(progressProvider).tutorId,
      );
    });
  }

  // --- Apertura de la conversación por situación y nivel ---

  String get _idm => ref.read(progressProvider).idiomaMeta;

  String _apertura(int n) {
    final s = sit;
    if (_idm != 'en' && n <= 3) return chatNivelBajo(_idm).apertura;
    if (s == null) {
      return n <= 3
          ? 'Hi! How are you today?'
          : "Hey! What's on your mind today? Tell me about your day.";
    }
    if (n <= 3) {
      return switch (s.categoria) {
        'Comida' => 'Hello! Welcome. Are you ready to order?',
        'Salud' => 'Good morning. What is the problem?',
        'Viajes' || 'Transporte' => 'Hello! Where are you going today?',
        'Trabajo' => 'Good morning. Please, tell me about you.',
        _ => 'Hello! How can I help you?',
      };
    }
    if (n <= 6) {
      return switch (s.categoria) {
        'Comida' => "Good evening, welcome to La Piazza! Have you had a chance to look at the menu, or would you like a recommendation?",
        'Salud' => "Good morning. What brings you in today? Could you describe your symptoms?",
        'Viajes' || 'Transporte' => "Hi there! Where are you headed today, and do you have any luggage to check in?",
        'Trabajo' => "Thanks for coming in. Could you start by telling me a bit about your background?",
        _ => "Hi! What can I do for you today?",
      };
    }
    return switch (s.categoria) {
      'Comida' => "Evening! I should mention we're out of the sea bass tonight, but the chef's tasting menu is superb. Any allergies I should flag for the kitchen?",
      'Salud' => "Morning. Your chart says you've had recurring headaches. Walk me through when they started and what seems to trigger them.",
      'Trabajo' => "Let's skip the formalities. Tell me about a project that didn't go as planned and what you'd do differently.",
      _ => "So, what's the situation? Give me the full picture and we'll sort it out together.",
    };
  }

  String? _traduccionApertura(int n) =>
      n <= 3 ? 'Toca para traducir · mantén pulsado para escuchar' : null;

  List<String> _sugerencias(int n) {
    if (sugerenciasIA.isNotEmpty) return sugerenciasIA;
    final s = sit;
    if (_idm != 'en' && n <= 3) return chatNivelBajo(_idm).sugerencias;
    if (s == null) {
      return n <= 3
          ? ['I am fine, thank you.', 'I am tired.', 'Very good!']
          : [
              'It was a busy day.',
              'Nothing special, and you?',
              'I want to talk about work.',
            ];
    }
    return switch (s.categoria) {
      'Comida' =>
        n <= 3
            ? ['Yes, please.', 'I want a coffee.', 'The menu, please.']
            : [
                "I'd like the special, please.",
                'What do you recommend?',
                'Is it spicy?',
              ],
      'Salud' =>
        n <= 3
            ? ['My head hurts.', 'I have a fever.', 'I am tired.']
            : [
                'I have had a headache since yesterday.',
                'Do I need a prescription?',
                'Is it serious?',
              ],
      'Trabajo' => [
        'I have three years of experience.',
        'I work well in a team.',
        'Could you repeat the question?',
      ],
      _ =>
        n <= 3
            ? ['Yes.', 'No, thank you.', 'I do not understand.']
            : [
                'Could you help me with this?',
                'Let me explain.',
                'Thanks, that helps.',
              ],
    };
  }

  void _enviar(String texto) {
    final t = texto.trim();
    if (t.isEmpty ||
        pensando ||
        transcribiendo ||
        escuchando ||
        errorConexion != null) {
      return;
    }
    input.clear();
    setState(() {
      mensajes.add(_Msg(t, mio: true));
    });
    _responderConIA(ref.read(progressProvider).nivelActual);
  }

  String? _respuestaEnCurso;
  bool pensando = false;
  String? errorConexion;

  /// No sustituye una respuesta de IA fallida por una simulación.
  Future<void> _responderConIA(int n) async {
    final st = ref.read(progressProvider);
    setState(() {
      pensando = true;
      _respuestaEnCurso = null;
      errorConexion = null;
    });
    final historial = [
      for (final m in mensajes)
        {'rol': m.mio ? 'alumno' : 'tutor', 'texto': m.texto},
    ];
    String? respuestaTemprana;
    _chatClient?.close();
    final client = http.Client();
    _chatClient = client;
    final r = await Sync.instancia.chat(
      client: client,
      onReply: (texto) {
        if (!mounted || _chatClient != client) return;
        respuestaTemprana = texto;
        setState(() => _respuestaEnCurso = texto);
        _bajar();
        if (_visible) {
          Voz.instancia.hablar(texto, _idm, voz: st.tutorId, progresivo: true);
        }
      },
      idiomaMeta: st.idiomaMeta,
      idiomaNativo: st.idiomaNativo,
      nivel: n,
      tutorId: st.tutorId,
      situacionId: sit?.id,
      objetivoId: widget.objetivoId,
      modo: widget.modo,
      situacion: sit?.nombre,
      objetivo: [
        if (sit != null)
          n <= 3
              ? 'responde con frases cortas'
              : n <= 6
              ? 'mantener la conversación y pedir detalles'
              : 'reaccionar a imprevistos y negociar',
        if (st.idiomaMeta == 'en') ...[
          'Contextos: ${st.sectores.map((s) => sectoresAprendizaje[s] ?? s).join(', ')}',
          'Objetivos personales: ${st.objetivos.map((s) => objetivosAprendizaje[s] ?? s).join(', ')}',
          'Prioridades basadas en práctica: ${RutaBiblioteca.prioridades(st.diagnostico, st.practicas).take(3).join(', ')}. Últimas dificultades: ${st.practicas.values.whereType<Map>().where((e) => e['correcta'] == false).take(5).map((e) => '${e['tema']}: ${e['feedback']}').join('; ')}. Usa estas evidencias para proponer refuerzo; no inventes unidades ni afirmes que son una certificación.',
          if (st.diagnostico?['idioma'] == 'en')
            'Temas a reforzar: ${((st.diagnostico?['refuerzo'] as List?) ?? []).take(5).join(', ')}. Competencias: ${st.diagnostico?['skills']}.',
          'Practica situaciones relacionadas sin examinar conocimientos profesionales; prioriza comunicar y corregir el inglés.',
        ],
      ].join('\n'),
      historial: historial,
    );
    if (!mounted) return;
    if (r != null) {
      if (sit != null && mensajes.any((m) => m.mio)) {
        final corrections = (r['corrections'] as List? ?? [])
            .whereType<Map>()
            .toList();
        final feedback = corrections
            .map(
              (c) => '${c['original']} → ${c['correcto']}: ${c['explicacion']}',
            )
            .join(' · ');
        ref.read(progressProvider.notifier).guardarTurnoSituacion(
          sit!.id,
          widget.objetivoId ?? 'libre',
          {
            'tema': sit!.nombre,
            'modo': widget.modo,
            'asistida': usoAyuda,
            'feedback': corrections.isEmpty
                ? 'Turno practicado sin correcciones textuales; dominio aún no evaluado.'
                : feedback.substring(0, feedback.length.clamp(0, 1200)),
            'correcciones': corrections.take(3).toList(),
          },
        );
      }
      // Correcciones reales de la IA sobre el último mensaje del alumno.
      final correcciones = (r['corrections'] as List? ?? []);
      if (correcciones.isNotEmpty && mensajes.isNotEmpty && mensajes.last.mio) {
        final c = correcciones.first as Map<String, dynamic>;
        final ultimo = mensajes.removeLast();
        mensajes.add(
          _Msg(
            ultimo.texto,
            mio: true,
            correccion: (
              c['original'] as String? ?? ultimo.texto,
              c['correcto'] as String? ?? '',
              c['explicacion'] as String? ?? '',
            ),
          ),
        );
        ref
            .read(progressProvider.notifier)
            .agregarError(
              skill: Skill.values.firstWhere(
                (k) => k.name == (c['skill'] ?? 'gramatica'),
                orElse: () => Skill.gramatica,
              ),
              original: c['original'] as String? ?? ultimo.texto,
              correccion: c['correcto'] as String? ?? '',
              explicacion: c['explicacion'] as String? ?? '',
              origen: sit?.nombre ?? 'Conversación libre',
            );
      }
      final texto = r['reply'] as String? ?? '';
      final rom = r['romanizacion'] as String? ?? '';
      final trad = r['traduccion'] as String? ?? '';
      setState(() {
        pensando = false;
        _respuestaEnCurso = null;
        mensajes.add(
          _Msg(
            rom.isEmpty ? texto : '$texto ($rom)',
            mio: false,
            sub: trad.isEmpty ? null : trad,
          ),
        );
        sugerenciasIA = (r['suggestions'] as List? ?? []).cast<String>();
        turno++;
      });
      if (respuestaTemprana == null) {
        if (_visible) {
          Voz.instancia.hablar(texto, _idm, voz: st.tutorId, progresivo: true);
        }
      }
      _bajar();
      return;
    }
    if (respuestaTemprana != null) {
      await Voz.instancia.parar();
    }
    await Conexion.comprobar();
    if (!mounted) return;
    setState(() {
      pensando = false;
      _respuestaEnCurso = null;
      errorConexion = !Sync.instancia.conectado
          ? 'Inicia sesión para practicar con el tutor.'
          : Conexion.estado.value == EstadoConexion.sinConexion
          ? 'Sin conexión con OneLingo. Tu mensaje se conserva; comprueba la conexión y reintenta.'
          : 'El tutor no está disponible en este momento. Tu mensaje se conserva; puedes reintentar.';
    });
  }

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final t = tutor(s.tutorId);
    final n = s.nivelActual;
    final perfil = perfilNivel(n);
    final color = sit?.color ?? OL.morado;

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.pop(),
        ),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              sit?.nombre ?? 'Conversación libre',
              style: const TextStyle(fontSize: 16),
            ),
            Text(
              '${t.nombre} · ${nombrePersonalidad(t.personalidad)} · Nivel $n',
              style: const TextStyle(
                fontSize: 11,
                color: OL.gris,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            tooltip: 'Cómo se adapta la IA a tu nivel',
            onPressed: () => showModalBottomSheet(
              context: context,
              builder: (_) => _PerfilSheet(perfil: perfil, tutor: t),
            ),
            icon: const Icon(Icons.tune),
          ),
        ],
      ),
      body: Movil(
        child: Column(
          children: [
            if (MediaQuery.viewInsetsOf(context).bottom == 0)
              Padding(
                padding: const EdgeInsets.fromLTRB(20, 4, 20, 8),
                child: Row(
                  children: [
                    ClipRRect(
                      borderRadius: BorderRadius.circular(18),
                      child: Image.asset(
                        fotoTutor(t.id),
                        alignment: encuadreTutor(t.id),
                        width: MediaQuery.viewInsetsOf(context).bottom > 0
                            ? 48
                            : 86,
                        height: MediaQuery.viewInsetsOf(context).bottom > 0
                            ? 62
                            : 110,
                        fit: BoxFit.cover,
                        semanticLabel: 'Tutor ${t.nombre}',
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            t.nombre,
                            style: const TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                          Text(
                            widget.modo == 'prueba'
                                ? 'Prueba de comunicación · sin pistas'
                                : 'Practica a tu ritmo · nivel $n',
                          ),
                          if (widget.objetivoId != null)
                            Text(
                              ref
                                      .watch(situationUnitsProvider)
                                      .asData
                                      ?.value
                                      .where((u) => u.id == sit?.id)
                                      .expand((u) => u.objectives)
                                      .where((o) => o.id == widget.objetivoId)
                                      .firstOrNull
                                      ?.title ??
                                  'Preparando tu objetivo',
                              style: const TextStyle(
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            if (sit != null &&
                _idm == 'en' &&
                MediaQuery.viewInsetsOf(context).bottom == 0)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: SituationSections(
                  selected: widget.modo == 'prueba' ? 3 : 2,
                  onSelected: (i) {
                    context.pushReplacement('/situacion/${sit!.id}?seccion=$i');
                  },
                ),
              ),
            if (escuchando || transcribiendo)
              Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 20,
                  vertical: 6,
                ),
                child: Row(
                  children: [
                    if (transcribiendo)
                      const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    else
                      const Icon(Icons.mic, color: OL.rojo, size: 20),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        transcribiendo
                            ? 'Transcribiendo tu respuesta…'
                            : 'Te escucho · termina tras 3 s de silencio',
                        style: const TextStyle(fontSize: 12),
                      ),
                    ),
                    if (escuchando)
                      TextButton(
                        onPressed: _hablarAlTutor,
                        child: const Text('Detener y enviar'),
                      ),
                  ],
                ),
              ),
            if (pensando) const LinearProgressIndicator(minHeight: 2),
            if (errorConexion != null)
              Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 20,
                  vertical: 8,
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Text(
                      errorConexion!,
                      style: const TextStyle(
                        color: OL.rojo,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 8),
                    OutlinedButton.icon(
                      onPressed: pensando ? null : () => _responderConIA(n),
                      icon: const Icon(Icons.refresh),
                      label: const Text('Reintentar mensaje'),
                    ),
                  ],
                ),
              ),
            Expanded(
              child: ListView.builder(
                controller: scroll,
                padding: const EdgeInsets.symmetric(
                  horizontal: 20,
                  vertical: 8,
                ),
                itemCount:
                    mensajes.length + (_respuestaEnCurso == null ? 0 : 1),
                itemBuilder: (_, i) => _Burbuja(
                  m: i < mensajes.length
                      ? mensajes[i]
                      : _Msg(
                          _respuestaEnCurso!,
                          mio: false,
                          sub: 'Preparando traducción y comentarios…',
                        ),
                  color: color,
                  tutor: t,
                  idm: _idm,
                ),
              ),
            ),
            if (widget.modo != 'prueba')
              Align(
                alignment: Alignment.centerLeft,
                child: TextButton.icon(
                  onPressed: () => setState(() {
                    mostrarAyuda = !mostrarAyuda;
                    if (mostrarAyuda) usoAyuda = true;
                  }),
                  icon: const Icon(Icons.lightbulb_outline),
                  label: Text(
                    mostrarAyuda ? 'Ocultar ayuda' : 'Necesito una pista',
                  ),
                ),
              ),
            if (mostrarAyuda && widget.modo != 'prueba')
              SizedBox(
                height: 40,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  children: [
                    for (final sug in _sugerencias(n))
                      Padding(
                        padding: const EdgeInsets.only(right: 8),
                        child: ActionChip(
                          label: Text(
                            sug,
                            style: TextStyle(
                              color: color,
                              fontWeight: FontWeight.w700,
                              fontSize: 12,
                            ),
                          ),
                          backgroundColor: OL.blanco,
                          side: BorderSide(color: color.withValues(alpha: 0.4)),
                          onPressed:
                              pensando ||
                                  transcribiendo ||
                                  escuchando ||
                                  errorConexion != null
                              ? null
                              : () => _enviar(sug),
                        ),
                      ),
                  ],
                ),
              ),
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 8, 20, 16),
              child: Row(
                children: [
                  IconButton.filled(
                    tooltip: escuchando
                        ? 'Detener y enviar'
                        : 'Grabar respuesta',
                    style: IconButton.styleFrom(
                      backgroundColor: escuchando ? OL.rojo : color,
                      fixedSize: const Size(48, 48),
                    ),
                    onPressed: pensando || transcribiendo
                        ? null
                        : _hablarAlTutor,
                    icon: Icon(
                      escuchando ? Icons.stop : Icons.mic,
                      color: OL.blanco,
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextField(
                      controller: input,
                      readOnly: escuchando || transcribiendo,
                      onSubmitted: _enviar,
                      textInputAction: TextInputAction.send,
                      decoration: InputDecoration(
                        hintText: transcribiendo
                            ? 'Transcribiendo tu respuesta…'
                            : escuchando
                            ? (Oido.instancia.modo == 'nube'
                                  ? 'Habla con calma…'
                                  : 'Escuchando…')
                            : 'Escribe tu respuesta...',
                      ),
                    ),
                  ),
                  const SizedBox(width: 6),
                  IconButton(
                    tooltip: 'Enviar mensaje',
                    onPressed:
                        pensando ||
                            transcribiendo ||
                            escuchando ||
                            errorConexion != null
                        ? null
                        : () => _enviar(input.text),
                    icon: Icon(Icons.send, color: color),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _Burbuja extends StatelessWidget {
  const _Burbuja({
    required this.m,
    required this.color,
    required this.tutor,
    required this.idm,
  });
  final _Msg m;
  final Color color;
  final Tutor tutor;
  final String idm;

  @override
  Widget build(BuildContext context) {
    final c = m.correccion;
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        mainAxisAlignment: m.mio
            ? MainAxisAlignment.end
            : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!m.mio) ...[
            CircleAvatar(
              radius: 16,
              backgroundColor: tutor.color,
              child: CircleAvatar(
                radius: 14,
                backgroundImage: AssetImage(fotoTutor(tutor.id)),
              ),
            ),
            const SizedBox(width: 8),
          ],
          Flexible(
            child: Column(
              crossAxisAlignment: m.mio
                  ? CrossAxisAlignment.end
                  : CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 11,
                  ),
                  decoration: BoxDecoration(
                    color: m.mio ? color : OL.blanco,
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: m.mio ? null : OL.sombra(0.06),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      GestureDetector(
                        onLongPress: m.mio
                            ? null
                            : () => Voz.instancia.hablar(
                                m.texto,
                                idm,
                                voz: tutor.id,
                              ),
                        child: Text(
                          m.texto,
                          style: TextStyle(
                            color: m.mio ? OL.blanco : OL.texto,
                            height: 1.4,
                          ),
                        ),
                      ),
                      if (m.sub != null)
                        Text(
                          m.sub!,
                          style: TextStyle(
                            color: m.mio ? const Color(0xFFE8E2FF) : OL.gris,
                            fontSize: 11,
                          ),
                        ),
                    ],
                  ),
                ),
                if (c != null)
                  Container(
                    margin: const EdgeInsets.only(top: 6),
                    padding: const EdgeInsets.all(12),
                    constraints: const BoxConstraints(maxWidth: 300),
                    decoration: BoxDecoration(
                      color: OL.blanco,
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: OL.rojoSuave, width: 2),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'CORRECCIÓN',
                          style: TextStyle(
                            color: OL.rojo,
                            fontSize: 10,
                            fontWeight: FontWeight.w800,
                            letterSpacing: 1,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          c.$1,
                          style: const TextStyle(
                            color: OL.gris,
                            decoration: TextDecoration.lineThrough,
                            fontSize: 13,
                          ),
                        ),
                        Text(
                          c.$2,
                          style: const TextStyle(
                            fontWeight: FontWeight.w700,
                            color: OL.verde,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          c.$3,
                          style: const TextStyle(
                            color: OL.gris,
                            fontSize: 12,
                            height: 1.3,
                          ),
                        ),
                      ],
                    ),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _PerfilSheet extends StatelessWidget {
  const _PerfilSheet({required this.perfil, required this.tutor});
  final LevelProfile perfil;
  final Tutor tutor;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.all(24),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Cómo se adapta la IA · Nivel ${perfil.nivel}',
          style: Theme.of(context).textTheme.headlineSmall,
        ),
        const SizedBox(height: 12),
        _F(
          'Tutor',
          '${tutor.nombre} · ${nombrePersonalidad(tutor.personalidad)}',
        ),
        _F(
          'Vocabulario',
          perfil.vocabularioMax == 0
              ? 'Sin límite'
              : 'Hasta ${perfil.vocabularioMax} palabras',
        ),
        _F('Tiempos verbales', perfil.tiempos),
        _F('Longitud de frase', perfil.longitudFrase),
        _F('Velocidad de habla', '${perfil.velocidad}x'),
        _F('Corrección', perfil.correccion),
        const SizedBox(height: 8),
        const Text(
          'Este perfil se inyecta en el prompt de la IA junto con la situación y tu idioma nativo (ARQUITECTURA §5).',
          style: TextStyle(color: OL.gris, fontSize: 12),
        ),
      ],
    ),
  );
}

class _F extends StatelessWidget {
  const _F(this.k, this.v);
  final String k, v;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 8),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: 130,
          child: Text(
            k,
            style: const TextStyle(color: OL.gris, fontWeight: FontWeight.w600),
          ),
        ),
        Expanded(
          child: Text(v, style: const TextStyle(fontWeight: FontWeight.w600)),
        ),
      ],
    ),
  );
}
