import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/foundations.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../core/efectos.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../shared/widgets/widgets.dart';
import '../../shared/widgets/mascot_coach.dart';

/// Teaching and supported practice, deliberately separate from placement exams.
class FoundationsScreen extends ConsumerStatefulWidget {
  const FoundationsScreen({super.key});
  @override
  ConsumerState<FoundationsScreen> createState() => _FoundationsScreenState();
}

class _FoundationsScreenState extends ConsumerState<FoundationsScreen> {
  int? unitIndex;
  int audioRequest = 0;
  int card = 0, question = 0;
  bool practicing = false, finished = false, listening = false;
  bool? correct;
  String? selected;
  final tokens = <String>[];
  final scroll = ScrollController();
  void stopAudio() {
    audioRequest++;
    listening = false;
    unawaited(VozNube.instancia.parar().catchError((_) {}));
  }

  void change(VoidCallback action) {
    stopAudio();
    setState(action);
    if (scroll.hasClients) scroll.jumpTo(0);
  }

  void open(int index) => change(() {
    unitIndex = index;
    card = 0;
    question = 0;
    practicing = false;
    finished = false;
    correct = null;
    selected = null;
    tokens.clear();
  });
  @override
  void dispose() {
    stopAudio();
    scroll.dispose();
    super.dispose();
  }

  Future<void> listen(String text) async {
    final request = ++audioRequest;
    setState(() => listening = true);
    bool ok = false;
    try {
      ok = await VozNube.instancia.reproducir(text, 'en', voz: 'narradora');
    } catch (_) {}
    if (!mounted || request != audioRequest) return;
    setState(() => listening = false);
    if (!ok) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'No se pudo reproducir el audio. Revisa tu conexión e inténtalo otra vez.',
          ),
        ),
      );
    }
  }

  Widget button(String text, VoidCallback? action) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 6),
    child: FilledButton(
      onPressed: action,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Text(text, textAlign: TextAlign.center),
      ),
    ),
  );
  Widget panel(
    List<Widget> children, {
    VoidCallback? onTap,
    String? etiquetaSemantica,
  }) => Tarjeta(
    padding: const EdgeInsets.all(22),
    color: OL.moradoSuave,
    borde: OL.moradoClaro,
    onTap: onTap,
    etiquetaSemantica: etiquetaSemantica,
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: children,
    ),
  );
  void check(FoundationUnit unit) {
    if (correct != null) return;
    final q = unit.checks[question];
    final answer = q.order ? tokens.join(' ') : selected;
    final passed = answer == q.answer;
    final id = foundationKey(unit, question);
    final previous = ref.read(progressProvider).practicas[id];
    ref.read(progressProvider.notifier).registrarPractica(id, {
      'idioma': 'en',
      'skill': unit.id == 'i-you' ? 'vocabulario' : 'gramatica',
      'nivel': 1,
      'ruta': 'fundamentos-v1',
      'tema': unit.title,
      'tipo': 'comprobacion_guiada',
      'conApoyo': true,
      'correcta': passed,
      'resueltaConApoyo':
          passed || (previous is Map && previous['resueltaConApoyo'] == true),
      'respuesta': answer,
      'feedback': q.feedback,
    });
    setState(() => correct = passed);
    passed ? Efectos.correcto() : Efectos.incorrecto();
  }

  @override
  Widget build(BuildContext context) {
    final evidence = ref.watch(progressProvider).practicas;
    final unit = unitIndex == null ? null : foundationUnits[unitIndex!];
    return Scaffold(
      appBar: AppBar(
        title: const Text('Inglés desde cero'),
        leading: IconButton(
          tooltip: 'Volver',
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () {
            if (unit != null) {
              change(() => unitIndex = null);
            } else if (context.canPop()) {
              context.pop();
            } else {
              context.go('/aprender');
            }
          },
        ),
      ),
      body: Movil(
        child: ListView(
          controller: scroll,
          padding: const EdgeInsets.all(20),
          children: [
            if (unit == null) ...[
              const MascotCoach(
                message: 'Vamos paso a paso. Primero un ejemplo; después lo intentamos juntos.',
              ),
              const Text(
                'Primero te enseñamos. Después lo intentas.',
                style: TextStyle(fontSize: 26, fontWeight: FontWeight.w900),
              ),
              const SizedBox(height: 12),
              const Text(
                'No necesitas conocer los pronombres ni el verbo be. Avanza con ejemplos en español y vuelve a ellos cuando lo necesites.',
              ),
              const SizedBox(height: 20),
              for (var i = 0; i < foundationUnits.length; i++)
                Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: OutlinedButton(
                    onPressed: foundationAvailable(foundationUnits[i], evidence)
                        ? () => open(i)
                        : null,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(vertical: 18),
                      child: Row(
                        children: [
                          Icon(
                            foundationPracticed(foundationUnits[i], evidence)
                                ? Icons.check_circle_outline
                                : foundationAvailable(
                                    foundationUnits[i],
                                    evidence,
                                  )
                                ? Icons.school_outlined
                                : Icons.lock_outline,
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  '${i + 1}. ${foundationUnits[i].title}',
                                  style: const TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                Text(
                                  foundationPracticed(
                                        foundationUnits[i],
                                        evidence,
                                      )
                                      ? 'Practicado con apoyo · puedes repetir'
                                      : foundationAvailable(
                                          foundationUnits[i],
                                          evidence,
                                        )
                                      ? foundationUnits[i].goal
                                      : 'Primero practica «${foundationUnits[i - 1].title}»',
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              const Text(
                'Estos pasos son práctica guiada. No certifican tu nivel. Las demás áreas siguen disponibles en Aprender.',
              ),
            ] else ...[
              Text(
                'Paso ${unitIndex! + 1} de ${foundationUnits.length} · ${unit.title}',
                style: const TextStyle(
                  color: OL.morado,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 10),
              Text(
                unit.goal,
                style: const TextStyle(
                  fontSize: 23,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 20),
              if (finished) ...[
                panel([
                  const Icon(
                    Icons.celebration_outlined,
                    size: 56,
                    color: OL.morado,
                  ),
                  const Text(
                    '¡Lo practicaste con ayuda!',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    unitIndex == foundationUnits.length - 1
                        ? 'Ahora puedes ensayar: I am + tu nombre. I am happy / tired. Elige cómo te sientes. No se evalúa tu voz en este paso.'
                        : 'Vuelve a estos ejemplos cuando lo necesites. Recordarlos otro día será otro paso del aprendizaje.',
                  ),
                ]),
                if (unitIndex! < foundationUnits.length - 1)
                  button('SIGUIENTE PASO', () => open(unitIndex! + 1)),
                button(
                  'VER MI RECORRIDO',
                  () => change(() => unitIndex = null),
                ),
              ] else if (!practicing) ...[
                Text('Descubre · ${card + 1} de ${unit.cards.length}'),
                const SizedBox(height: 12),
                panel(
                  [
                    Icon(
                      switch (unit.cards[card].visual) {
                        'happy' => Icons.sentiment_satisfied_alt,
                        'tired' => Icons.bedtime_outlined,
                        'pair' => Icons.people_outline,
                        'you' => Icons.waving_hand_outlined,
                        _ => Icons.person_outline,
                      },
                      size: 64,
                      color: OL.morado,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      unit.cards[card].english,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                    Text(
                      unit.cards[card].spanish,
                      textAlign: TextAlign.center,
                      style: const TextStyle(fontSize: 24),
                    ),
                    const SizedBox(height: 18),
                    Text(
                      unit.cards[card].explanation,
                      style: const TextStyle(fontSize: 18, height: 1.5),
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.volume_up_outlined, color: OL.morado),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            listening
                                ? 'Preparando audio…'
                                : 'Toca la tarjeta para escuchar',
                            textAlign: TextAlign.center,
                            style: const TextStyle(
                              color: OL.morado,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                  onTap: listening
                      ? null
                      : () => listen(unit.cards[card].english),
                  etiquetaSemantica:
                      'Escuchar ${unit.cards[card].english} en inglés',
                ),
                if (card > 0)
                  TextButton(
                    onPressed: () => change(() => card--),
                    child: const Text('VOLVER AL EJEMPLO ANTERIOR'),
                  ),
                button(
                  card < unit.cards.length - 1
                      ? 'SIGUIENTE EJEMPLO'
                      : 'PRACTICAR CON AYUDA',
                  () => change(() {
                    if (card < unit.cards.length - 1) {
                      card++;
                    } else {
                      practicing = true;
                    }
                  }),
                ),
              ] else ...[
                MascotCoach(
                  key: ValueKey('mascot-${unit.id}-$question'),
                  listening: true,
                  message:
                      'Puedes volver a los ejemplos siempre que lo necesites.',
                ),
                Text(
                  'Práctica con apoyo · ${question + 1} de ${unit.checks.length}',
                ),
                const SizedBox(height: 12),
                Text(
                  unit.checks[question].prompt,
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 14),
                if (unit.checks[question].order) ...[
                  panel([
                    Text(
                      tokens.isEmpty
                          ? 'Toca las palabras en orden'
                          : tokens.join(' '),
                      style: const TextStyle(fontSize: 24),
                    ),
                  ]),
                  Wrap(
                    spacing: 8,
                    children: [
                      for (final word in unit.checks[question].options)
                        OutlinedButton(
                          onPressed: correct != null || tokens.contains(word)
                              ? null
                              : () => setState(() => tokens.add(word)),
                          child: Text(word),
                        ),
                    ],
                  ),
                  TextButton(
                    onPressed: correct == null
                        ? () => setState(tokens.clear)
                        : null,
                    child: const Text('Volver a ordenar'),
                  ),
                ] else
                  for (final option in unit.checks[question].options)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 10),
                      child: OutlinedButton(
                        onPressed: correct != null
                            ? null
                            : () => setState(() => selected = option),
                        style: OutlinedButton.styleFrom(
                          backgroundColor: selected == option
                              ? OL.moradoSuave
                              : null,
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(14),
                          child: Text(
                            '${selected == option ? '✓ ' : ''}$option',
                            style: const TextStyle(fontSize: 21),
                          ),
                        ),
                      ),
                    ),
                TextButton(
                  onPressed: () => change(() {
                    practicing = false;
                    card = 0;
                  }),
                  child: const Text('VER LOS EJEMPLOS OTRA VEZ'),
                ),
                if (correct == null)
                  button(
                    'COMPROBAR',
                    (unit.checks[question].order
                            ? tokens.length ==
                                  unit.checks[question].options.length
                            : selected != null)
                        ? () => check(unit)
                        : null,
                  ),
                if (correct != null) ...[
                  AnswerFeedback(
                    correct: correct!,
                    title: correct!
                        ? '¡Bien! Mira por qué:'
                        : 'Vamos a repasarlo:',
                    child: Text(
                      unit.checks[question].feedback,
                      style: const TextStyle(fontSize: 18, height: 1.4),
                    ),
                  ),
                  button(
                    correct! ? 'CONTINUAR' : 'INTENTAR CON ESTA AYUDA',
                    () => change(() {
                      if (correct!) {
                        if (question + 1 < unit.checks.length) {
                          question++;
                        } else {
                          finished = true;
                        }
                      }
                      correct = null;
                      selected = null;
                      tokens.clear();
                    }),
                  ),
                ],
              ],
            ],
          ],
        ),
      ),
    );
  }
}
