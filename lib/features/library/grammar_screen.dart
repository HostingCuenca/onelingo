import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/grammar_guides.dart';
import '../../core/content/grammar_production_tasks.dart';
import '../../core/efectos.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import '../../shared/widgets/mascot_coach.dart';

/// La enseñanza permanece visible, incluso después de comprobar respuestas.
class GrammarScreen extends ConsumerStatefulWidget {
  const GrammarScreen({super.key, this.nivel});
  final int? nivel;
  @override
  ConsumerState<GrammarScreen> createState() => _GrammarScreenState();
}

class _GrammarScreenState extends ConsumerState<GrammarScreen> {
  late int level;
  int topic = 0;
  int step = 0;
  int question = 0;
  final scroll = ScrollController();
  final Map<String, int> choices = {};
  final Map<String, String> drafts = {};
  final Set<String> checked = {};
  @override
  void initState() {
    super.initState();
    level = (widget.nivel ?? ref.read(progressProvider).nivelInicial).clamp(
      1,
      10,
    );
  }

  void check(GrammarGuide guide, int index) {
    final id = 'grammar-guide-${guide.id}-$index';
    if (checked.contains(id) || !choices.containsKey(id)) return;
    final q = guide.checks[index];
    final correct = choices[id] == q.answer;
    ref.read(progressProvider.notifier).registrarPractica(id, {
      'idioma': 'en',
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
    if (scroll.hasClients) scroll.jumpTo(0);
  }

  Future<void> chooseTopic() async {
    var selectedLevel = level;
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
                  DropdownButtonFormField<int>(
                    initialValue: selectedLevel,
                    isExpanded: true,
                    decoration: const InputDecoration(
                      labelText: 'Explorar nivel',
                    ),
                    items: [
                      for (var n = 1; n <= 10; n++)
                        DropdownMenuItem(value: n, child: Text('Nivel $n')),
                    ],
                    onChanged: (n) {
                      if (n != null) update(() => selectedLevel = n);
                    },
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
                                  : Icons.chevron_right_rounded,
                              color: OL.morado,
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
        child: ListView(
          controller: scroll,
          padding: const EdgeInsets.fromLTRB(20, 8, 20, 28),
          children: [
            if (step == 0)
              const MascotCoach(
                message: 'Lee un ejemplo conmigo. Después puedes crear tu propia frase.',
              ),
            if (level == 1)
              TextButton.icon(
                onPressed: () => context.push('/fundamentos'),
                icon: const Icon(Icons.school_outlined),
                label: const Text('¿Empiezas desde cero? Aprende paso a paso'),
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
            Row(
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
                          padding: const EdgeInsets.symmetric(
                            vertical: 12,
                            horizontal: 4,
                          ),
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
            ),
            const SizedBox(height: 20),
            AnimatedSwitcher(
              duration: reduced
                  ? Duration.zero
                  : const Duration(milliseconds: 220),
              child: Column(
                key: ValueKey('${guide.id}-$step-$question'),
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  if (step == 0) ...[
                    Tarjeta(
                      sombra: false,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          const Text(
                            'La idea clave',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w900,
                            ),
                          ),
                          const SizedBox(height: 10),
                          Text(
                            guide.rule,
                            style: const TextStyle(fontSize: 16, height: 1.55),
                          ),
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
                                    style: const TextStyle(
                                      fontSize: 16,
                                      height: 1.4,
                                    ),
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
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                              children: [
                                Padding(
                                  padding: const EdgeInsets.only(bottom: 12),
                                  child: Text(
                                    guide.commonError,
                                    style: const TextStyle(
                                      fontSize: 16,
                                      height: 1.5,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),
                    BotonPrincipal(
                      onPressed: () => showStep(1),
                      child: const Text('AHORA ME TOCA A MÍ'),
                    ),
                  ],
                  if (step == 1) ...[
                    Tarjeta(
                      sombra: false,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          const Text(
                            'Dilo a tu manera',
                            style: TextStyle(
                              fontSize: 21,
                              fontWeight: FontWeight.w900,
                            ),
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
                            onChanged: (v) => drafts[guide.id] = v,
                            decoration: const InputDecoration(
                              labelText: 'Tus propias frases',
                              hintText: 'Escribe tu ejemplo en inglés…',
                              alignLabelWithHint: true,
                            ),
                          ),
                          const SizedBox(height: 10),
                          const Text(
                            'Puedes probar sin miedo. Este borrador se conserva mientras estás en esta pantalla y no recibe una nota automática.',
                            style: TextStyle(
                              fontSize: 14,
                              color: OL.gris,
                              height: 1.4,
                            ),
                          ),
                        ],
                      ),
                    ),
                    TextButton.icon(
                      onPressed: () => showStep(0),
                      icon: const Icon(Icons.auto_stories_rounded),
                      label: const Text('Consultar el ejemplo'),
                    ),
                    const SizedBox(height: 8),
                    BotonPrincipal(
                      onPressed: () => showStep(2),
                      child: const Text('COMPROBAR CON EJEMPLOS'),
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
                    if (answered && question < guide.checks.length - 1)
                      BotonPrincipal(
                        onPressed: () {
                          setState(() => question++);
                          showStep(2);
                        },
                        child: const Text('SIGUIENTE PREGUNTA'),
                      ),
                    if (answered && question == guide.checks.length - 1) ...[
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
                      const SizedBox(height: 16),
                      BotonPrincipal(
                        onPressed: () {
                          if (topic + 1 < guides.length) {
                            setState(() {
                              topic++;
                              question = 0;
                            });
                            showStep(0);
                          } else {
                            chooseTopic();
                          }
                        },
                        child: Text(
                          topic + 1 < guides.length
                              ? 'SIGUIENTE TEMA'
                              : 'ELEGIR OTRO TEMA',
                        ),
                      ),
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
    );
  }

  Widget _question(GrammarGuide guide, int index) {
    final id = 'grammar-guide-${guide.id}-$index';
    final q = guide.checks[index];
    final answered = checked.contains(id);
    final correct = choices[id] == q.answer;
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Tarjeta(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              '${index + 1}. ${q.prompt}',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 10),
            for (var i = 0; i < q.options.length; i++)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: OutlinedButton(
                  onPressed: answered
                      ? null
                      : () => setState(() => choices[id] = i),
                  style: OutlinedButton.styleFrom(
                    alignment: Alignment.centerLeft,
                    padding: const EdgeInsets.all(14),
                    disabledForegroundColor: OL.texto,
                    backgroundColor: answered && i == q.answer
                        ? OL.verdeSuave
                        : choices[id] == i
                        ? OL.moradoSuave
                        : null,
                  ),
                  child: Text(q.options[i]),
                ),
              ),
            if (!answered)
              FilledButton(
                onPressed: choices.containsKey(id)
                    ? () => check(guide, index)
                    : null,
                child: const Text('COMPROBAR'),
              ),
            if (answered)
              AnswerFeedback(
                correct: correct,
                title: correct ? '¡Bien razonado!' : 'Vamos a entenderlo',
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (!correct) Text('Respuesta: ${q.options[q.answer]}'),
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
          ],
        ),
      ),
    );
  }
}
