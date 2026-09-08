import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/content/fotos.dart';
import '../../core/api/sync.dart';
import '../../core/content/idiomas.dart';
import '../../core/voz.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Conversación con el tutor de IA (situación o libre).
///
/// FASE 1: la IA es un simulador local que sigue el mismo contrato que tendrá
/// el backend con Claude: `{reply, corrections[], suggestions[]}` y usa el
/// `LevelProfile` del nivel del alumno. En fase 2 solo cambia `_responder`.
class ChatScreen extends ConsumerStatefulWidget {
  const ChatScreen({super.key, this.situacionId, this.leccionId});
  final int? situacionId;
  final String? leccionId;

  @override
  ConsumerState<ChatScreen> createState() => _ChatScreenState();
}

class _Msg {
  _Msg(this.texto, {required this.mio, this.sub, this.correccion});
  final String texto;
  final bool mio;
  final String? sub;
  final (String, String, String)? correccion; // original, corregido, explicación
}

class _ChatScreenState extends ConsumerState<ChatScreen> {
  final mensajes = <_Msg>[];
  final input = TextEditingController();
  final scroll = ScrollController();
  int turno = 0;
  bool escuchando = false;
  List<String> sugerenciasIA = [];

  void _bajar() => Future.delayed(const Duration(milliseconds: 50), () {
        if (scroll.hasClients) scroll.animateTo(scroll.position.maxScrollExtent, duration: const Duration(milliseconds: 250), curve: Curves.easeOut);
      });
  late final Situation? sit = widget.situacionId == null ? null : situacion(widget.situacionId!);

  @override
  void dispose() {
    Oido.instancia.parar();
    Voz.instancia.parar();
    super.dispose();
  }

  Future<void> _hablarAlTutor() async {
    if (escuchando) {
      await Oido.instancia.parar();
      setState(() => escuchando = false);
      return;
    }
    setState(() => escuchando = true);
    final ok = await Oido.instancia.escuchar(_idm, (texto, fin) {
      if (!mounted) return;
      setState(() => input.text = texto);
      if (fin) {
        setState(() => escuchando = false);
        if (texto.trim().isNotEmpty) _enviar(texto);
      }
    }, segundos: 8, onFin: () {
      if (!mounted || !escuchando) return;
      setState(() => escuchando = false);
      if (input.text.trim().isEmpty) {
        final e = Oido.instancia.ultimoError;
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(e.isEmpty ? 'No se escuchó nada. Acércate al micrófono e inténtalo otra vez.' : 'No se pudo escuchar ($e). Comprueba el micrófono.'),
        ));
      }
    });
    if (!ok && mounted) {
      setState(() => escuchando = false);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Micrófono no disponible en este dispositivo. Escribe tu respuesta.')),
      );
    }
  }

  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      final n = ref.read(progressProvider).nivelActual;
      setState(() => mensajes.add(_Msg(_apertura(n), mio: false, sub: _traduccionApertura(n))));
      Voz.instancia.hablar(_apertura(n), _idm, voz: ref.read(progressProvider).tutorId);
    });
  }

  // --- Guion simulado por situación y nivel ---

  String get _idm => ref.read(progressProvider).idiomaMeta;

  String _apertura(int n) {
    final s = sit;
    if (_idm != 'en' && n <= 3) return chatNivelBajo(_idm).apertura;
    if (s == null) return n <= 3 ? 'Hi! How are you today?' : "Hey! What's on your mind today? Tell me about your day.";
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

  String? _traduccionApertura(int n) => n <= 3 ? 'Toca para traducir · mantén pulsado para escuchar' : null;

  List<String> _sugerencias(int n) {
    if (sugerenciasIA.isNotEmpty) return sugerenciasIA;
    final s = sit;
    if (_idm != 'en' && n <= 3) return chatNivelBajo(_idm).sugerencias;
    if (s == null) return n <= 3 ? ['I am fine, thank you.', 'I am tired.', 'Very good!'] : ['It was a busy day.', 'Nothing special, and you?', 'I want to talk about work.'];
    return switch (s.categoria) {
      'Comida' => n <= 3 ? ['Yes, please.', 'I want a coffee.', 'The menu, please.'] : ["I'd like the special, please.", 'What do you recommend?', 'Is it spicy?'],
      'Salud' => n <= 3 ? ['My head hurts.', 'I have a fever.', 'I am tired.'] : ['I have had a headache since yesterday.', 'Do I need a prescription?', 'Is it serious?'],
      'Trabajo' => ['I have three years of experience.', 'I work well in a team.', 'Could you repeat the question?'],
      _ => n <= 3 ? ['Yes.', 'No, thank you.', 'I do not understand.'] : ['Could you help me with this?', 'Let me explain.', 'Thanks, that helps.'],
    };
  }

  /// Detección de errores muy simple (la real la hará Claude en fase 2).
  (String, String, String, Skill)? _corregir(String t) {
    final l = t.trim();
    if (_idm != 'en') return null; // las reglas locales son de inglés; Claude cubrirá el resto
    if (RegExp(r'\bi am\b').hasMatch(l) && l.contains('i am')) {
      return (l, l.replaceAll('i am', 'I am'), 'El pronombre "I" siempre va en mayúscula.', Skill.escritura);
    }
    if (RegExp(r'\bhow you\b', caseSensitive: false).hasMatch(l)) {
      return (l, l.replaceAll(RegExp(r'how you', caseSensitive: false), 'how are you'), 'En preguntas no omitas el verbo "are".', Skill.gramatica);
    }
    if (RegExp(r'\bi have (\d+|two|three) years\b', caseSensitive: false).hasMatch(l) && !l.contains('of experience')) {
      return (l, '$l of experience', 'Para hablar de experiencia laboral se dice "years of experience".', Skill.vocabulario);
    }
    if (RegExp(r'\bpeoples\b', caseSensitive: false).hasMatch(l)) {
      return (l, l.replaceAll(RegExp(r'peoples', caseSensitive: false), 'people'), '"People" ya es plural; "peoples" solo se usa para pueblos/naciones.', Skill.vocabulario);
    }
    final want = RegExp(r"\b(want|wants|need|needs|would like)\s+(eat|drink|go|have|order|see|buy|pay|sleep|talk|speak|learn|study|work|travel|try)\b", caseSensitive: false);
    if (want.hasMatch(l)) {
      return (l, l.replaceAllMapped(want, (m) => '${m[1]} to ${m[2]}'), 'Después de "want / need / would like" el verbo va con "to": want to eat.', Skill.gramatica);
    }
    final tercera = RegExp(r"\b(he|she|it)\s+(go|eat|want|like|have|work|live|need|play|study)\b", caseSensitive: false);
    if (tercera.hasMatch(l)) {
      return (l, l.replaceAllMapped(tercera, (m) {
        final v = m[2]!.toLowerCase();
        final c = v == 'have' ? 'has' : (v == 'go' || v == 'study' ? (v == 'go' ? 'goes' : 'studies') : '${v}s');
        return '${m[1]} $c';
      }), 'En presente simple, he/she/it lleva -s en el verbo (she goes, he has).', Skill.conjugacion);
    }
    if (RegExp(r"\bi (no|not) (like|want|have|know|understand)\b", caseSensitive: false).hasMatch(l)) {
      return (l, l.replaceAllMapped(RegExp(r"\bi (no|not) (\w+)", caseSensitive: false), (m) => "I don't ${m[2]}"), 'La negación en presente es "I don\'t + verbo".', Skill.gramatica);
    }
    if (RegExp(r"\bi am agree\b", caseSensitive: false).hasMatch(l)) {
      return (l, l.replaceAll(RegExp(r"i am agree", caseSensitive: false), 'I agree'), '"Agree" es un verbo: se dice "I agree", no "I am agree".', Skill.vocabulario);
    }
    if (RegExp(r'\bmore better\b', caseSensitive: false).hasMatch(l)) {
      return (l, l.replaceAll(RegExp(r'more better', caseSensitive: false), 'better'), '"Better" ya es comparativo; no lleva "more".', Skill.gramatica);
    }
    if (l.isNotEmpty && l[0] == l[0].toLowerCase() && RegExp(r'[a-z]').hasMatch(l[0])) {
      return (l, l[0].toUpperCase() + l.substring(1), 'Las frases empiezan con mayúscula.', Skill.escritura);
    }
    return null;
  }

  String _respuesta(int n) {
    final s = sit;
    final base = s == null
        ? ['Nice! Tell me more about that.', 'Interesting. Why do you think so?', 'Got it. And what happened next?', 'Great, thanks for sharing.']
        : switch (s.categoria) {
            'Comida' => ['Great choice! Anything to drink?', 'Sure. Would you like a starter as well?', 'Perfect, it will take ten minutes.', 'Here you are. Enjoy your meal!'],
            'Salud' => ['I see. How long have you felt this way?', 'Do you have any other symptoms?', 'Let me check your temperature.', 'Take this twice a day and rest.'],
            'Trabajo' => ['Interesting. Can you give me an example?', 'What are your strengths?', 'Why do you want this job?', 'Thank you. We will call you.'],
            _ => ['Okay. Can you tell me more?', 'Sure, I can help with that.', 'Alright, anything else?', 'Perfect, thank you!'],
          };
    final r = base[turno % base.length];
    if (n > 2) return r;
    // Nivel 1-2: solo la primera frase, conservando su signo final.
    final m = RegExp(r'^[^.!?]*[.!?]').firstMatch(r);
    return m == null ? r : m.group(0)!;
  }

  /// Si hubo error, el tutor primero lo señala con la forma correcta (adaptado al nivel).
  String _respuestaCon(int n, (String, String, String, Skill)? corr) {
    final r = _respuesta(n);
    if (corr == null) return r;
    final c = corr.$2;
    return n <= 3 ? 'Good try! We say: "$c". $r' : 'Almost — a more natural way is "$c". $r';
  }

  void _enviar(String texto) {
    final t = texto.trim();
    if (t.isEmpty) return;
    input.clear();
    final n = ref.read(progressProvider).nivelActual;
    final corr = _corregir(t);
    setState(() {
      mensajes.add(_Msg(t, mio: true, sub: corr == null ? '✓ Bien dicho' : null, correccion: corr == null ? null : (corr.$1, corr.$2, corr.$3)));
    });
    if (corr != null) {
      ref.read(progressProvider.notifier).agregarError(
            skill: corr.$4,
            original: corr.$1,
            correccion: corr.$2,
            explicacion: corr.$3,
            origen: sit?.nombre ?? 'Conversación libre',
          );
    }
    _responderConIA(n, corr);
  }

  bool pensando = false;

  /// Intenta la IA real del backend; si no hay servidor/clave, usa el simulador local.
  Future<void> _responderConIA(int n, (String, String, String, Skill)? corrLocal) async {
    final st = ref.read(progressProvider);
    setState(() => pensando = true);
    final historial = [
      for (final m in mensajes) {'rol': m.mio ? 'alumno' : 'tutor', 'texto': m.texto},
    ];
    final r = await Sync.instancia.chat(
      idiomaMeta: st.idiomaMeta,
      idiomaNativo: st.idiomaNativo,
      nivel: n,
      tutorId: st.tutorId,
      situacionId: sit?.id,
      situacion: sit?.nombre,
      objetivo: sit == null ? null : (n <= 3 ? 'responde con frases cortas' : n <= 6 ? 'mantener la conversación y pedir detalles' : 'reaccionar a imprevistos y negociar'),
      historial: historial,
    );
    if (!mounted) return;
    if (r != null) {
      // Correcciones reales de la IA sobre el último mensaje del alumno.
      final correcciones = (r['corrections'] as List? ?? []);
      if (correcciones.isNotEmpty && mensajes.isNotEmpty && mensajes.last.mio) {
        final c = correcciones.first as Map<String, dynamic>;
        final ultimo = mensajes.removeLast();
        mensajes.add(_Msg(ultimo.texto, mio: true, correccion: (c['original'] as String? ?? ultimo.texto, c['correcto'] as String? ?? '', c['explicacion'] as String? ?? '')));
        ref.read(progressProvider.notifier).agregarError(
              skill: Skill.values.firstWhere((k) => k.name == (c['skill'] ?? 'gramatica'), orElse: () => Skill.gramatica),
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
        mensajes.add(_Msg(rom.isEmpty ? texto : '$texto ($rom)', mio: false, sub: trad.isEmpty ? null : trad));
        sugerenciasIA = (r['suggestions'] as List? ?? []).cast<String>();
        turno++;
      });
      Voz.instancia.hablar(texto, _idm, voz: st.tutorId);
      _bajar();
      return;
    }
    Future.delayed(const Duration(milliseconds: 400), () {
      if (!mounted) return;
      setState(() {
        pensando = false;
        final rr = _respuestaCon(n, corrLocal);
        mensajes.add(_Msg(rr, mio: false));
        Voz.instancia.hablar(rr, _idm, voz: st.tutorId);
        turno++;
      });
      Future.delayed(const Duration(milliseconds: 50), () {
        if (scroll.hasClients) scroll.animateTo(scroll.position.maxScrollExtent, duration: const Duration(milliseconds: 250), curve: Curves.easeOut);
      });
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
        leading: IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => context.pop()),
        title: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(sit?.nombre ?? 'Conversación libre', style: const TextStyle(fontSize: 16)),
          Text('${t.nombre} · ${nombrePersonalidad(t.personalidad)} · Nivel $n', style: const TextStyle(fontSize: 11, color: OL.gris, fontWeight: FontWeight.w500)),
        ]),
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
        child: Column(children: [
          if (sit != null)
            Container(
              margin: const EdgeInsets.fromLTRB(20, 4, 20, 8),
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(color: color.withValues(alpha: 0.12), borderRadius: BorderRadius.circular(14)),
              child: Row(children: [
                Icon(Icons.flag_outlined, color: color, size: 18),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    n <= 3
                        ? 'Objetivo: responde con frases cortas. La IA habla despacio.'
                        : n <= 6
                            ? 'Objetivo: mantén la conversación, pide detalles y explica tus preferencias.'
                            : 'Objetivo: reacciona a imprevistos, da tu opinión y negocia.',
                    style: TextStyle(color: color, fontWeight: FontWeight.w700, fontSize: 12),
                  ),
                ),
              ]),
            ),
          Expanded(
            child: ListView.builder(
              controller: scroll,
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
              itemCount: mensajes.length,
              itemBuilder: (_, i) => _Burbuja(m: mensajes[i], color: color, tutor: t, idm: _idm),
            ),
          ),
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
                      label: Text(sug, style: TextStyle(color: color, fontWeight: FontWeight.w700, fontSize: 12)),
                      backgroundColor: OL.blanco,
                      side: BorderSide(color: color.withValues(alpha: 0.4)),
                      onPressed: () => _enviar(sug),
                    ),
                  ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 8, 20, 16),
            child: Row(children: [
              IconButton.filled(
                style: IconButton.styleFrom(backgroundColor: escuchando ? OL.rojo : color, fixedSize: const Size(48, 48)),
                onPressed: _hablarAlTutor,
                icon: Icon(escuchando ? Icons.stop : Icons.mic, color: OL.blanco),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: TextField(
                  controller: input,
                  onSubmitted: _enviar,
                  textInputAction: TextInputAction.send,
                  decoration: InputDecoration(hintText: escuchando ? (Oido.instancia.modo == 'nube' ? 'Grabando… toca el botón rojo para enviar' : 'Escuchando…') : 'Escribe tu respuesta...'),
                ),
              ),
              const SizedBox(width: 6),
              IconButton(onPressed: () => _enviar(input.text), icon: Icon(Icons.send, color: color)),
            ]),
          ),
        ]),
      ),
    );
  }
}

class _Burbuja extends StatelessWidget {
  const _Burbuja({required this.m, required this.color, required this.tutor, required this.idm});
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
        mainAxisAlignment: m.mio ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!m.mio) ...[
            CircleAvatar(radius: 16, backgroundColor: tutor.color, child: CircleAvatar(radius: 14, backgroundImage: AssetImage(fotoTutor(tutor.id)))),
            const SizedBox(width: 8),
          ],
          Flexible(
            child: Column(crossAxisAlignment: m.mio ? CrossAxisAlignment.end : CrossAxisAlignment.start, children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 11),
                decoration: BoxDecoration(
                  color: m.mio ? color : OL.blanco,
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: m.mio ? null : OL.sombra(0.06),
                ),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  GestureDetector(
                    onLongPress: m.mio ? null : () => Voz.instancia.hablar(m.texto, idm, voz: tutor.id),
                    child: Text(m.texto, style: TextStyle(color: m.mio ? OL.blanco : OL.texto, height: 1.4)),
                  ),
                  if (m.sub != null) Text(m.sub!, style: TextStyle(color: m.mio ? const Color(0xFFE8E2FF) : OL.gris, fontSize: 11)),
                ]),
              ),
              if (c != null)
                Container(
                  margin: const EdgeInsets.only(top: 6),
                  padding: const EdgeInsets.all(12),
                  constraints: const BoxConstraints(maxWidth: 300),
                  decoration: BoxDecoration(color: OL.blanco, borderRadius: BorderRadius.circular(14), border: Border.all(color: OL.rojoSuave, width: 2)),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    const Text('CORRECCIÓN', style: TextStyle(color: OL.rojo, fontSize: 10, fontWeight: FontWeight.w800, letterSpacing: 1)),
                    const SizedBox(height: 4),
                    Text(c.$1, style: const TextStyle(color: OL.gris, decoration: TextDecoration.lineThrough, fontSize: 13)),
                    Text(c.$2, style: const TextStyle(fontWeight: FontWeight.w700, color: OL.verde)),
                    const SizedBox(height: 4),
                    Text(c.$3, style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.3)),
                  ]),
                ),
            ]),
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
        child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text('Cómo se adapta la IA · Nivel ${perfil.nivel}', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 12),
          _F('Tutor', '${tutor.nombre} · ${nombrePersonalidad(tutor.personalidad)}'),
          _F('Vocabulario', perfil.vocabularioMax == 0 ? 'Sin límite' : 'Hasta ${perfil.vocabularioMax} palabras'),
          _F('Tiempos verbales', perfil.tiempos),
          _F('Longitud de frase', perfil.longitudFrase),
          _F('Velocidad de habla', '${perfil.velocidad}x'),
          _F('Corrección', perfil.correccion),
          const SizedBox(height: 8),
          const Text('Este perfil se inyecta en el prompt de la IA junto con la situación y tu idioma nativo (ARQUITECTURA §5).',
              style: TextStyle(color: OL.gris, fontSize: 12)),
        ]),
      );
}

class _F extends StatelessWidget {
  const _F(this.k, this.v);
  final String k, v;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 8),
        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          SizedBox(width: 130, child: Text(k, style: const TextStyle(color: OL.gris, fontWeight: FontWeight.w600))),
          Expanded(child: Text(v, style: const TextStyle(fontWeight: FontWeight.w600))),
        ]),
      );
}
