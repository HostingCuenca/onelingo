import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../app/theme.dart';
import '../../core/content/grammar_guides.dart';
import '../../core/content/grammar_production_tasks.dart';
import '../../core/efectos.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import '../../shared/widgets/mascot_coach.dart';
import '../ruta/opcion_respuesta.dart';

/// La enseñanza permanece visible, incluso después de comprobar respuestas.
class GrammarScreen extends ConsumerStatefulWidget {
  const GrammarScreen({super.key, this.nivel});
  final int? nivel;
  @override
  ConsumerState<GrammarScreen> createState() => _GrammarScreenState();
}

class _GrammarScreenState extends ConsumerState<GrammarScreen> {
  late int level;

  /// El enlace sin nivel llega como 1 (valor por defecto de la ruta): en ese
  /// caso se abre en el nivel actual del alumno.
  int? get _nivelPedido =>
      widget.nivel == null || widget.nivel == 1 ? null : widget.nivel;
  int topic = 0;
  int step = 0;
  int question = 0;
  final scroll = ScrollController();
  final Map<String, int> choices = {};
  final Map<String, String> drafts = {};
  final Set<String> checked = {};
  static const _clavePosicion = 'onelingo.gramatica.posicion';
  static const _prefijoBorrador = 'onelingo.gramatica.borrador.';

  @override
  void initState() {
    super.initState();
    level = (_nivelPedido ?? ref.read(progressProvider).nivelActual).clamp(
      1,
      10,
    );
    _restaurar();
  }

  /// Reanuda el último tema (y nivel, si no se pidió uno) y los borradores.
  Future<void> _restaurar() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final guardados = {
        for (final k in prefs.getKeys())
          if (k.startsWith(_prefijoBorrador))
            k.substring(_prefijoBorrador.length): prefs.getString(k) ?? '',
      };
      final partes = (prefs.getString(_clavePosicion) ?? '').split(':');
      final nivelGuardado = int.tryParse(partes.first);
      final temaGuardado = partes.length > 1 ? int.tryParse(partes[1]) : null;
      if (!mounted) return;
      setState(() {
        drafts.addAll(guardados);
        if (nivelGuardado != null &&
            temaGuardado != null &&
            (_nivelPedido == null || _nivelPedido == nivelGuardado) &&
            nivelGuardado >= 1 &&
            nivelGuardado <= 10 &&
            temaGuardado < grammarForLevel(nivelGuardado).length) {
          level = nivelGuardado;
          topic = temaGuardado;
        }
      });
    } catch (_) {}
  }

  void _guardarPosicion() => SharedPreferences.getInstance()
      .then((p) => p.setString(_clavePosicion, '$level:$topic'))
      .catchError((_) => true);

  void _guardarBorrador(String guia, String texto) {
    drafts[guia] = texto;
    SharedPreferences.getInstance()
        .then((p) => p.setString('$_prefijoBorrador$guia', texto))
        .catchError((_) => true);
  }

  /// Un tema está practicado si se respondió alguna de sus preguntas.
  bool practicado(GrammarGuide g) {
    final practicas = ref.read(progressProvider).practicas;
    return practicas.keys.any((k) => k.startsWith('grammar-guide-${g.id}-'));
  }

  void check(GrammarGuide guide, int index) {
    final id = 'grammar-guide-${guide.id}-$index';
    if (checked.contains(id) || !choices.containsKey(id)) return;
    final q = guide.checks[index];
    final correct = choices[id] == q.answer;
    ref.read(progressProvider.notifier).registrarPractica(id, {
      'idioma': ref.read(progressProvider).idiomaMeta,
      'skill': 'gramatica',
      'nivel': guide.level,
      'tema': guide.title,
      'tipo': 'practica_guiada',
      'correcta': correct,
      'respuesta': q.options[choices[id]!],
      'feedback': q.feedback,
    });
    correct ? Efectos.correcto() : Efectos.incorrecto();
    setState(() => checked.add(id));
  }

  @override
  void dispose() {
    scroll.dispose();
    super.dispose();
  }

  void showStep(int value) {
    FocusScope.of(context).unfocus();
    setState(() => step = value);
    _guardarPosicion();
    if (scroll.hasClients) scroll.jumpTo(0);
  }

  Future<void> chooseTopic() async {
    var selectedLevel = level;
    final chipActual = GlobalKey();
    // Al abrir, el chip del nivel en curso queda a la vista.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final ctx = chipActual.currentContext;
      if (ctx != null && ctx.mounted) {
        Scrollable.ensureVisible(ctx, alignment: .5);
      }
    });
    final selection = await showModalBottomSheet<(int, int)>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      constraints: const BoxConstraints(maxWidth: 560),
      builder: (context) => StatefulBuilder(
        builder: (context, update) => SafeArea(
          child: SizedBox(
            height: MediaQuery.sizeOf(context).height * .75,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Row(
                    children: [
                      const Expanded(
                        child: Text(
                          'Elige tu próximo tema',
                          style: TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                      ),
                      IconButton(
                        tooltip: 'Cerrar temario',
                        onPressed: () => Navigator.pop(context),
                        icon: const Icon(Icons.close_rounded),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: [
                        for (var n = 1; n <= 10; n++)
                          Padding(
                            padding: const EdgeInsets.only(right: 8),
                            child: ChoiceChip(
                              key: n == level ? chipActual : null,
                              label: Text('Nivel $n'),
                              selected: selectedLevel == n,
                              onSelected: (_) =>
                                  update(() => selectedLevel = n),
                            ),
                          ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),
                  Expanded(
                    child: ListView.separated(
                      itemCount: grammarForLevel(selectedLevel).length,
                      separatorBuilder: (_, _) => const SizedBox(height: 8),
                      itemBuilder: (context, i) {
                        final item = grammarForLevel(selectedLevel)[i];
                        final current = level == selectedLevel && topic == i;
                        return Material(
                          color: current ? OL.moradoSuave : OL.blanco,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(18),
                            side: BorderSide(
                              color: current ? OL.morado : OL.grisClaro,
                            ),
                          ),
                          child: ListTile(
                            contentPadding: const EdgeInsets.symmetric(
                              horizontal: 16,
                              vertical: 8,
                            ),
                            leading: CircleAvatar(
                              backgroundColor: OL.moradoClaro,
                              child: Text(
                                '${i + 1}',
                                style: const TextStyle(
                                  color: OL.morado,
                                  fontWeight: FontWeight.w900,
                                ),
                              ),
                            ),
                            title: Text(
                              item.title,
                              style: const TextStyle(
                                fontWeight: FontWeight.w800,
                              ),
                            ),
                            subtitle: Text(item.goal),
                            trailing: Icon(
                              current
                                  ? Icons.bookmark_rounded
                                  : practicado(item)
                                  ? Icons.check_circle_rounded
                                  : Icons.chevron_right_rounded,
                              color: !current && practicado(item)
                                  ? OL.verde
                                  : OL.morado,
                              semanticLabel: practicado(item)
                                  ? 'Practicado'
                                  : null,
                            ),
                            onTap: () =>
                                Navigator.pop(context, (selectedLevel, i)),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
    if (!mounted || selection == null) return;
    setState(() {
      level = selection.$1;
      topic = selection.$2;
      question = 0;
    });
    showStep(0);
  }

  /// Avanza a la siguiente pregunta, al siguiente tema o abre el temario.
  void _siguiente(GrammarGuide guide, List<GrammarGuide> guides) {
    if (question < guide.checks.length - 1) {
      setState(() => question++);
      showStep(2);
    } else if (topic + 1 < guides.length) {
      setState(() {
        topic++;
        question = 0;
      });
      showStep(0);
    } else {
      chooseTopic();
    }
  }

  /// Acción principal de cada paso, siempre fija abajo.
  List<Widget> _acciones(GrammarGuide guide, List<GrammarGuide> guides) {
    if (step == 0) {
      return [
        BotonPrincipal(
          onPressed: () => showStep(1),
          child: const Text('AHORA ME TOCA A MÍ'),
        ),
      ];
    }
    if (step == 1) {
      return [
        BotonPrincipal(
          onPressed: () => showStep(2),
          child: const Text('COMPROBAR CON EJEMPLOS'),
        ),
      ];
    }
    final id = 'grammar-guide-${guide.id}-$question';
    final q = guide.checks[question];
    if (!checked.contains(id)) {
      return [
        BotonPrincipal(
          onPressed: choices.containsKey(id)
              ? () => check(guide, question)
              : null,
          child: const Text('COMPROBAR'),
        ),
      ];
    }
    final correct = choices[id] == q.answer;
    final ultima = question == guide.checks.length - 1;
    return [
      FeedbackDock(
        child: AnswerFeedback(
          correct: correct,
          title: correct ? '¡Bien razonado!' : 'Vamos a entenderlo',
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (!correct)
                Text(
                  'Respuesta: ${q.options[q.answer]}',
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              Text(
                q.feedback,
                style: const TextStyle(fontSize: 16, height: 1.5),
              ),
              if (!correct)
                TextButton.icon(
                  onPressed: () => setState(() {
                    checked.remove(id);
                    choices.remove(id);
                  }),
                  icon: const Icon(Icons.refresh_rounded),
                  label: const Text('INTENTAR OTRA VEZ'),
                ),
            ],
          ),
        ),
      ),
      BotonPrincipal(
        color: correct ? OL.verde : OL.morado,
        onPressed: () => _siguiente(guide, guides),
        child: Text(
          !ultima
              ? 'SIGUIENTE PREGUNTA'
              : topic + 1 < guides.length
              ? 'SIGUIENTE TEMA'
              : 'ELEGIR OTRO TEMA',
        ),
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    final guides = grammarForLevel(level);
    final guide = guides[topic];
    final answered = checked.contains('grammar-guide-${guide.id}-$question');
    final reduced =
        MediaQuery.disableAnimationsOf(context) || !Efectos.animaciones.value;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gramática'),
        leading: IconButton(
          tooltip: 'Volver',
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/inicio'),
        ),
      ),
      body: Movil(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(
              child: ListView(
                controller: scroll,
                padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
                children: [
                  if (step == 0)
                    const MascotCoach(
                      message:
                          'Lee un ejemplo conmigo. Después puedes crear tu propia frase.',
                    ),
                  if (level == 1)
                    TextButton.icon(
                      onPressed: () => context.push('/fundamentos'),
                      icon: const Icon(Icons.school_outlined),
                      label: const Text(
                        '¿Empiezas desde cero? Aprende paso a paso',
                      ),
                    ),
                  Wrap(
                    alignment: WrapAlignment.spaceBetween,
                    crossAxisAlignment: WrapCrossAlignment.center,
                    spacing: 12,
                    children: [
                      Text(
                        'Nivel $level · Tema ${topic + 1} de ${guides.length}',
                        style: const TextStyle(
                          color: OL.gris,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      TextButton.icon(
                        onPressed: chooseTopic,
                        icon: const Icon(Icons.grid_view_rounded, size: 18),
                        label: const Text('Temario'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    guide.title,
                    style: const TextStyle(
                      fontSize: 27,
                      fontWeight: FontWeight.w900,
                      height: 1.15,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    guide.goal,
                    style: const TextStyle(color: OL.gris, height: 1.4),
                  ),
                  const SizedBox(height: 20),
                  _pasos(),
                  const SizedBox(height: 20),
                  AnimatedSwitcher(
                    duration: reduced
                        ? Duration.zero
                        : const Duration(milliseconds: 220),
                    child: Column(
                      key: ValueKey('${guide.id}-$step-$question'),
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        if (step == 0) _aprende(guide),
                        if (step == 1) ...[
                          _crea(guide),
                          TextButton.icon(
                            onPressed: () => showStep(0),
                            icon: const Icon(Icons.auto_stories_rounded),
                            label: const Text('Consultar el ejemplo'),
                          ),
                        ],
                        if (step == 2) ...[
                          Text(
                            'Pregunta ${question + 1} de ${guide.checks.length}',
                            style: const TextStyle(
                              fontWeight: FontWeight.w800,
                              color: OL.gris,
                            ),
                          ),
                          const SizedBox(height: 8),
                          _question(guide, question),
                          if (answered &&
                              question == guide.checks.length - 1) ...[
                            const Text(
                              '¡Has practicado este tema!',
                              style: TextStyle(
                                fontSize: 21,
                                fontWeight: FontWeight.w900,
                              ),
                            ),
                            const SizedBox(height: 8),
                            const Text(
                              'Puedes volver a los ejemplos cuando lo necesites.',
                              style: TextStyle(color: OL.gris, height: 1.4),
                            ),
                            const SizedBox(height: 8),
                          ],
                          if (question > 0)
                            TextButton(
                              onPressed: () {
                                setState(() => question--);
                                showStep(2);
                              },
                              child: const Text('Revisar pregunta anterior'),
                            ),
                          TextButton.icon(
                            onPressed: () => showStep(0),
                            icon: const Icon(Icons.menu_book_rounded),
                            label: const Text('VOLVER A LA EXPLICACIÓN'),
                          ),
                        ],
                      ],
                    ),
                  ),
                ],
              ),
            ),
            DecoratedBox(
              decoration: const BoxDecoration(
                color: OL.fondo,
                border: Border(top: BorderSide(color: OL.grisClaro)),
              ),
              child: Padding(
                padding: EdgeInsets.fromLTRB(
                  20,
                  12,
                  20,
                  20 + MediaQuery.paddingOf(context).bottom,
                ),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: _acciones(guide, guides),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _pasos() => Row(
    children: [
      for (var i = 0; i < 3; i++) ...[
        if (i > 0) const SizedBox(width: 6),
        Expanded(
          child: Semantics(
            selected: step == i,
            button: true,
            child: InkWell(
              borderRadius: BorderRadius.circular(14),
              onTap: () => showStep(i),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 4),
                decoration: BoxDecoration(
                  color: step == i ? OL.morado : OL.moradoSuave,
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Column(
                  children: [
                    Icon(
                      [
                        Icons.auto_stories_rounded,
                        Icons.edit_note_rounded,
                        Icons.fact_check_rounded,
                      ][i],
                      color: step == i ? OL.blanco : OL.morado,
                      size: 22,
                    ),
                    const SizedBox(height: 4),
                    Text(
                      ['Aprende', 'Crea', 'Prueba'][i],
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: step == i ? OL.blanco : OL.morado,
                        fontSize: 14,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    ],
  );

  Widget _aprende(GrammarGuide guide) => Tarjeta(
    sombra: false,
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text(
          'La idea clave',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w900),
        ),
        const SizedBox(height: 10),
        Text(guide.rule, style: const TextStyle(fontSize: 16, height: 1.55)),
        const SizedBox(height: 16),
        for (final example in guide.examples)
          Container(
            margin: const EdgeInsets.only(bottom: 8),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: OL.moradoSuave,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  example.$1,
                  style: const TextStyle(
                    fontSize: 19,
                    fontWeight: FontWeight.w800,
                    color: OL.morado,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  example.$2,
                  style: const TextStyle(fontSize: 16, height: 1.4),
                ),
              ],
            ),
          ),
        Material(
          color: Colors.transparent,
          child: ExpansionTile(
            key: ValueKey('tip-${guide.id}'),
            tilePadding: EdgeInsets.zero,
            title: const Text(
              'Un consejo para recordarlo',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.w700),
            ),
            children: [
              Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: Text(
                  guide.commonError,
                  style: const TextStyle(fontSize: 16, height: 1.5),
                ),
              ),
            ],
          ),
        ),
      ],
    ),
  );

  Widget _crea(GrammarGuide guide) => Tarjeta(
    sombra: false,
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text(
          'Dilo a tu manera',
          style: TextStyle(fontSize: 21, fontWeight: FontWeight.w900),
        ),
        const SizedBox(height: 10),
        Text(
          grammarProductionTasks[guide.id]!,
          style: const TextStyle(fontSize: 16, height: 1.5),
        ),
        const SizedBox(height: 16),
        TextFormField(
          key: ValueKey('production-${guide.id}'),
          initialValue: drafts[guide.id] ?? '',
          minLines: 3,
          maxLines: 6,
          onChanged: (v) => _guardarBorrador(guide.id, v),
          decoration: const InputDecoration(
            labelText: 'Tus propias frases',
            hintText: 'Escribe tu ejemplo en inglés…',
            alignLabelWithHint: true,
          ),
        ),
        const SizedBox(height: 10),
        const Text(
          'Escribe sin miedo: tu borrador se guarda y no lleva nota.',
          style: TextStyle(fontSize: 14, color: OL.gris, height: 1.4),
        ),
      ],
    ),
  );

  Widget _question(GrammarGuide guide, int index) {
    final id = 'grammar-guide-${guide.id}-$index';
    final q = guide.checks[index];
    final answered = checked.contains(id);
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            q.prompt,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 14),
          for (var i = 0; i < q.options.length; i++)
            OpcionRespuesta(
              texto: q.options[i],
              estado: answered && i == q.answer
                  ? EstadoOpcion.correcta
                  : answered && choices[id] == i
                  ? EstadoOpcion.incorrecta
                  : choices[id] == i
                  ? EstadoOpcion.seleccionada
                  : EstadoOpcion.normal,
              onTap: answered
                  ? null
                  : () {
                      Efectos.toque();
                      setState(() => choices[id] = i);
                    },
            ),
        ],
      ),
    );
  }
}
