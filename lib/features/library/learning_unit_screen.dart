import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../app/theme.dart';
import '../../core/content/learning_units.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/widgets.dart';
import '../../shared/widgets/mascot_coach.dart';
import '../../shared/widgets/skill_badge.dart';

/// Teaching and formative checks. These answers do not certify proficiency.
class LearningUnitScreen extends ConsumerStatefulWidget {
  const LearningUnitScreen({super.key, required this.skill, this.nivel = 1});
  final String skill;
  final int nivel;
  @override
  ConsumerState<LearningUnitScreen> createState() => _LearningUnitState();
}

class _LearningUnitState extends ConsumerState<LearningUnitScreen> {
  late int level;
  int selectedUnit = 0;
  bool checking = false, busy = false, heard = false, transcript = false;
  final Set<String> transcriptsSeen = {};
  int audioGeneration = 0;
  final Map<String, int> choices = {};
  final Set<String> answered = {};
  bool get listening => widget.skill == 'listening';
  List<LearningQuestion> questionsFor(LearningUnit unit) {
    if (widget.skill != 'vocabulario') return unit.questions;
    final meanings = unit.words.map((w) => w.translation).toList();
    return List.generate(unit.words.length, (i) {
      final options = List<String>.of(meanings);
      final seed = '${unit.id}-$i'.codeUnits.fold<int>(
        17,
        (a, b) => a * 31 + b,
      );
      options.shuffle(Random(seed));
      return LearningQuestion(
        'vocab-$i',
        'En este contexto, ¿qué significa «${unit.words[i].word}»?',
        options,
        options.indexOf(meanings[i]),
        '${unit.words[i].word} significa ${unit.words[i].translation}. Observa cómo se usa en el ejemplo.',
        unit.words[i].example,
      );
    });
  }

  @override
  void initState() {
    super.initState();
    level = widget.nivel.clamp(1, 10);
  }

  @override
  void dispose() {
    audioGeneration++;
    VozNube.instancia.parar();
    super.dispose();
  }

  void changeUnit(VoidCallback change) {
    audioGeneration++;
    VozNube.instancia.parar();
    setState(() {
      change();
      checking = false;
      busy = false;
      heard = false;
      transcript = false;
    });
  }

  Future<void> listen(LearningUnit unit) async {
    final generation = ++audioGeneration;
    setState(() => busy = true);
    final ok = await VozNube.instancia.reproducir(
      unit.passage,
      'en',
      voz: ref.read(progressProvider).tutorId,
    );
    if (!mounted || generation != audioGeneration) return;
    setState(() {
      busy = false;
      heard = heard || ok;
    });
    if (!ok) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'No se pudo reproducir el audio. Comprueba tu conexión y vuelve a intentarlo.',
          ),
        ),
      );
    }
  }

  void check(LearningUnit unit, LearningQuestion q) {
    final key = 'learn-${widget.skill}-${unit.id}-${q.id}';
    if (answered.contains(key) || !choices.containsKey(key)) return;
    ref.read(progressProvider.notifier).registrarPractica(key, {
      'idioma': 'en',
      'skill': widget.skill,
      'nivel': level,
      'tema': unit.title,
      'tipo': 'comprobacion_guiada',
      'correcta': choices[key] == q.answerIndex,
      'respuesta': q.options[choices[key]!],
      'feedback': q.explanation,
      'conApoyo': listening ? transcriptsSeen.contains(unit.id) : true,
      'audioIniciado': heard,
    });
    setState(() => answered.add(key));
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: Text(
        listening
            ? 'Aprender listening'
            : widget.skill == 'vocabulario'
            ? 'Vocabulario en contexto'
            : 'Aprender lectura',
      ),
    ),
    body: Movil(
      child: ref
          .watch(learningUnitsProvider(widget.skill))
          .when(
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (_, _) => Center(
              child: TextButton(
                onPressed: () =>
                    ref.invalidate(learningUnitsProvider(widget.skill)),
                child: const Text('No se pudo cargar. Reintentar'),
              ),
            ),
            data: (units) {
              final available = units.where((u) => u.level == level).toList();
              if (available.isEmpty) {
                return const Center(
                  child: Text('Contenido en preparación para este nivel.'),
                );
              }
              final unit =
                  available[selectedUnit.clamp(0, available.length - 1)];
              final evidence = ref.watch(progressProvider).practicas;
              final checked = questionsFor(unit)
                  .where(
                    (q) => answered.contains(
                      'learn-${widget.skill}-${unit.id}-${q.id}',
                    ),
                  )
                  .length;
              return ListView(
                padding: const EdgeInsets.fromLTRB(20, 8, 20, 32),
                children: [
                  if (!checking)
                    MascotCoach(
                      listening: listening,
                      message: listening
                          ? 'Conoce las palabras y escucha con calma. Puedes repetir el audio.'
                          : 'Primero conoce las palabras. Luego busca cómo se usan en el texto.',
                    ),
                  Row(
                    children: [
                      InsigniaHabilidad(widget.skill),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          'Primero entiende.\nDespués comprueba.',
                          style: Theme.of(context).textTheme.headlineMedium,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  DropdownButtonFormField<int>(
                    initialValue: level,
                    isExpanded: true,
                    decoration: const InputDecoration(
                      labelText: 'Nivel interno',
                    ),
                    items: [
                      for (var n = 1; n <= 10; n++)
                        DropdownMenuItem(value: n, child: Text('Nivel $n')),
                    ],
                    onChanged: (n) {
                      if (n != null) {
                        changeUnit(() {
                          level = n;
                          selectedUnit = 0;
                        });
                      }
                    },
                  ),
                  const SizedBox(height: 12),
                  for (var i = 0; i < available.length; i++)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 8),
                      child: OutlinedButton.icon(
                        onPressed: () => changeUnit(() => selectedUnit = i),
                        icon: Icon(
                          i == selectedUnit
                              ? Icons.radio_button_checked
                              : Icons.radio_button_off,
                        ),
                        label: Text(available[i].title),
                      ),
                    ),
                  const SizedBox(height: 8),
                  Text(
                    unit.title,
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(unit.objective, style: const TextStyle(height: 1.45)),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: OutlinedButton(
                          onPressed: () => setState(() => checking = false),
                          child: const Text('Aprender'),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: FilledButton(
                          onPressed: () => setState(() => checking = true),
                          child: const Text('Comprobar'),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  if (!checking) ...[
                    Tarjeta(
                      color: OL.moradoSuave,
                      sombra: false,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Una estrategia para esta unidad',
                            style: TextStyle(fontWeight: FontWeight.w900),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            unit.strategy,
                            style: const TextStyle(fontSize: 16, height: 1.5),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 18),
                    const Text(
                      'Vocabulario antes de empezar',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                    for (final word in unit.words)
                      Padding(
                        padding: const EdgeInsets.only(top: 8),
                        child: Tarjeta(
                          sombra: false,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '${word.word} · ${word.translation}',
                                style: const TextStyle(
                                  fontWeight: FontWeight.w800,
                                  fontSize: 16,
                                ),
                              ),
                              const SizedBox(height: 6),
                              Text(
                                word.example,
                                style: const TextStyle(
                                  fontSize: 16,
                                  height: 1.4,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    const SizedBox(height: 18),
                  ],
                  if (listening) ...[
                    BotonPrincipal(
                      onPressed: busy ? null : () => listen(unit),
                      child: Text(
                        busy
                            ? 'PREPARANDO AUDIO…'
                            : heard
                            ? 'VOLVER A ESCUCHAR'
                            : 'ESCUCHAR EN INGLÉS',
                      ),
                    ),
                    const Text(
                      'Puedes escuchar varias veces. La voz requiere conexión.',
                      style: TextStyle(fontSize: 14, color: OL.gris),
                    ),
                    if (!checking)
                      TextButton(
                        onPressed: () => setState(() {
                          transcript = !transcript;
                          if (transcript) transcriptsSeen.add(unit.id);
                        }),
                        child: Text(
                          transcript
                              ? 'Ocultar transcripción'
                              : 'Ver transcripción de apoyo',
                        ),
                      ),
                  ],
                  if (!listening ||
                      (!checking && transcript) ||
                      (checking && checked == questionsFor(unit).length)) ...[
                    const SizedBox(height: 12),
                    Tarjeta(
                      sombra: false,
                      child: SelectableText(
                        unit.passage,
                        style: const TextStyle(fontSize: 17, height: 1.65),
                      ),
                    ),
                  ],
                  if (!checking) ...[
                    const SizedBox(height: 18),
                    BotonPrincipal(
                      onPressed: () => setState(() => checking = true),
                      child: const Text('COMPROBAR LO QUE ENTENDÍ'),
                    ),
                  ],
                  if (checking) ...[
                    const SizedBox(height: 12),
                    Text(
                      'Comprobación guiada · $checked/${questionsFor(unit).length}',
                      style: const TextStyle(
                        fontWeight: FontWeight.w900,
                        fontSize: 18,
                      ),
                    ),
                    const Text(
                      'Practicar este material no demuestra todavía retención a largo plazo.',
                      style: TextStyle(color: OL.gris, fontSize: 14),
                    ),
                    for (final q in questionsFor(unit))
                      Builder(
                        builder: (context) {
                          final key =
                              'learn-${widget.skill}-${unit.id}-${q.id}';
                          final done = answered.contains(key);
                          final previous = evidence[key] as Map?;
                          return Padding(
                            padding: const EdgeInsets.only(top: 16),
                            child: Tarjeta(
                              sombra: false,
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.stretch,
                                children: [
                                  Text(
                                    q.prompt,
                                    style: const TextStyle(
                                      fontWeight: FontWeight.w800,
                                      fontSize: 17,
                                    ),
                                  ),
                                  const SizedBox(height: 8),
                                  for (var i = 0; i < q.options.length; i++)
                                    Padding(
                                      padding: const EdgeInsets.only(bottom: 6),
                                      child: OutlinedButton(
                                        onPressed: done
                                            ? null
                                            : () => setState(
                                                () => choices[key] = i,
                                              ),
                                        style: OutlinedButton.styleFrom(
                                          backgroundColor: choices[key] == i
                                              ? OL.moradoSuave
                                              : null,
                                          alignment: Alignment.centerLeft,
                                        ),
                                        child: Text(q.options[i]),
                                      ),
                                    ),
                                  if (!done)
                                    FilledButton(
                                      onPressed:
                                          choices[key] == null ||
                                              (listening && !heard)
                                          ? null
                                          : () => check(unit, q),
                                      child: Text(
                                        listening && !heard
                                            ? 'Escucha el audio primero'
                                            : 'Comprobar respuesta',
                                      ),
                                    ),
                                  if (done) ...[
                                    if (choices[key] != q.answerIndex)
                                      TextButton.icon(
                                        onPressed: () => setState(() {
                                          answered.remove(key);
                                          choices.remove(key);
                                        }),
                                        icon: const Icon(Icons.refresh_rounded),
                                        label: const Text('INTENTAR OTRA VEZ'),
                                      ),
                                    Text(
                                      choices[key] == q.answerIndex
                                          ? 'Bien razonado'
                                          : 'Vamos a revisarlo',
                                      style: TextStyle(
                                        fontWeight: FontWeight.w900,
                                        color: choices[key] == q.answerIndex
                                            ? OL.verde
                                            : OL.rojo,
                                      ),
                                    ),
                                    const SizedBox(height: 6),
                                    Text(
                                      q.explanation,
                                      style: const TextStyle(
                                        fontSize: 16,
                                        height: 1.4,
                                      ),
                                    ),
                                    const SizedBox(height: 6),
                                    Text(
                                      'Evidencia: “${q.evidence}”',
                                      style: const TextStyle(
                                        fontStyle: FontStyle.italic,
                                      ),
                                    ),
                                    TextButton(
                                      onPressed: () =>
                                          setState(() => checking = false),
                                      child: const Text(
                                        'Volver a la explicación',
                                      ),
                                    ),
                                  ],
                                  if (!done && previous != null)
                                    const Text(
                                      'Ya practicaste esta pregunta. Este intento es un repaso.',
                                      style: TextStyle(
                                        fontSize: 14,
                                        color: OL.gris,
                                      ),
                                    ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                  ],
                ],
              );
            },
          ),
    ),
  );
}
