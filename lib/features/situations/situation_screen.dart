import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/content/fotos.dart';
import '../../core/content/situation_units.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../core/efectos.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../shared/widgets/widgets.dart';
import '../../shared/widgets/situation_illustrations.dart';

class SituationScreen extends ConsumerStatefulWidget {
  const SituationScreen({super.key, required this.id, this.section = 0});
  final int id, section;
  @override
  ConsumerState<SituationScreen> createState() => _SituationScreenState();
}

class _SituationScreenState extends ConsumerState<SituationScreen> {
  late int section = widget.section.clamp(0, 3);
  int objective = 0;
  int question = 0;
  String? selected;
  bool checked = false;
  bool listening = false;
  int audioGeneration = 0;
  @override
  void dispose() {
    audioGeneration++;
    Voz.instancia.parar();
    super.dispose();
  }

  Future<void> listen(String text) async {
    final generation = ++audioGeneration;
    setState(() => listening = true);
    await Voz.instancia.hablar(
      text,
      'en',
      voz: ref.read(progressProvider).tutorId,
    );
    if (!mounted || generation != audioGeneration) return;
    setState(() => listening = false);
    if (VozNube.instancia.ultimoError.isNotEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'No se pudo cargar la voz natural. Comprueba la conexión para volver a intentarlo.',
          ),
        ),
      );
    }
  }

  void chat(SituationUnit unit, {bool test = false}) {
    Voz.instancia.parar();
    context.push(
      '/chat?situacion=${unit.id}&objetivo=${unit.objectives[objective].id}&modo=${test ? 'prueba' : 'practica'}',
    );
  }

  List<(String, String)> wordOptions(SituationUnit unit) {
    final answer = unit.words[question];
    final others = unit.words.where((w) => w.$2 != answer.$2).toList()
      ..shuffle(Random(unit.id * 31 + question));
    return [answer, ...others.take(3)]
      ..shuffle(Random(unit.id * 17 + question));
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(progressProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tu ruta de situación'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/practicar'),
        ),
      ),
      body: Movil(
        child: ref
            .watch(situationUnitsProvider)
            .when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (_, _) => Center(
                child: TextButton(
                  onPressed: () => ref.invalidate(situationUnitsProvider),
                  child: const Text('No se pudo cargar. Reintentar'),
                ),
              ),
              data: (units) {
                final matches = units.where((u) => u.id == widget.id);
                if (matches.isEmpty) {
                  return const Center(child: Text('Esta situación no existe.'));
                }
                final unit = matches.first;
                if (state.idiomaMeta != 'en') {
                  return Center(
                    child: FilledButton(
                      onPressed: () =>
                          context.push('/chat?situacion=${unit.id}'),
                      child: const Text('Practicar con el tutor'),
                    ),
                  );
                }
                final tutor = tutores.firstWhere(
                  (t) => t.id == state.tutorId,
                  orElse: () => tutores.first,
                );
                final evidence = situationEvidence(state.practicas, unit.id);
                final obj = unit.objectives[objective];
                return ListView(
                  padding: const EdgeInsets.fromLTRB(20, 4, 20, 28),
                  children: [
                    Text(
                      unit.name,
                      style: Theme.of(context).textTheme.headlineSmall
                          ?.copyWith(fontWeight: FontWeight.w800),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        ClipRRect(
                          borderRadius: BorderRadius.circular(22),
                          child: Image.asset(
                            fotoTutor(tutor.id),
                            alignment: encuadreTutor(tutor.id),
                            width: 108,
                            height: 138,
                            fit: BoxFit.cover,
                            semanticLabel: 'Tutor ${tutor.nombre}',
                          ),
                        ),
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Con ${tutor.nombre}',
                                style: const TextStyle(
                                  fontSize: 22,
                                  fontWeight: FontWeight.w800,
                                ),
                              ),
                              Text('Nivel ${state.nivelActual} · Inglés'),
                              const SizedBox(height: 8),
                              Text(
                                evidence.isEmpty
                                    ? 'Empieza con palabras útiles. Después úsalas para conversar.'
                                    : 'Retoma tu práctica. El tutor usará tus objetivos y correcciones guardadas.',
                              ),
                              TextButton(
                                onPressed: () => context.push('/tutores'),
                                child: const Text('Cambiar tutor'),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    SituationSections(
                      selected: section,
                      onSelected: (i) {
                        audioGeneration++;
                        Voz.instancia.parar();
                        setState(() {
                          section = i;
                          listening = false;
                        });
                      },
                    ),
                    const SizedBox(height: 18),
                    SituationIllustrations(unit.id),
                    const SizedBox(height: 18),
                    const Text(
                      '¿Qué quieres poder hacer?',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    for (var i = 0; i < unit.objectives.length; i++)
                      Padding(
                        padding: const EdgeInsets.only(top: 8),
                        child: OutlinedButton.icon(
                          style: OutlinedButton.styleFrom(
                            alignment: Alignment.centerLeft,
                            padding: const EdgeInsets.all(14),
                            backgroundColor: objective == i
                                ? tutor.color.withValues(alpha: .12)
                                : null,
                          ),
                          onPressed: () => setState(() => objective = i),
                          icon: Icon(
                            objective == i
                                ? Icons.radio_button_checked
                                : Icons.radio_button_off,
                          ),
                          label: Text(unit.objectives[i].title),
                        ),
                      ),
                    const SizedBox(height: 20),
                    if (section == 0) ...[
                      const Text(
                        'Vocabulario de esta situación',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      const Text(
                        'Toca una tarjeta para escuchar, recuerda el significado y usa la palabra en una frase propia.',
                      ),
                      for (final word in unit.words)
                        Padding(
                          padding: const EdgeInsets.only(top: 8),
                          child: Tarjeta(
                            padding: EdgeInsets.zero,
                            sombra: false,
                            onTap: listening ? null : () => listen(word.$1),
                            etiquetaSemantica: 'Escuchar ${word.$1}',
                            child: ListTile(
                              title: Text(
                                word.$1,
                                style: const TextStyle(
                                  fontWeight: FontWeight.w800,
                                ),
                              ),
                              subtitle: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(word.$2),
                                  for (final detail in unit.vocabulary.where(
                                    (v) => v.en == word.$1,
                                  )) ...[
                                    const SizedBox(height: 6),
                                    Text(
                                      detail.example,
                                      style: const TextStyle(
                                        fontStyle: FontStyle.italic,
                                        height: 1.4,
                                      ),
                                    ),
                                    Text(
                                      '${detail.category} · introducción sugerida: nivel ${detail.level}',
                                      style: const TextStyle(fontSize: 11),
                                    ),
                                  ],
                                ],
                              ),
                              trailing: const Tooltip(
                                message: 'Toca la tarjeta para escuchar',
                                child: Icon(
                                  Icons.volume_up_rounded,
                                  color: OL.morado,
                                ),
                              ),
                            ),
                          ),
                        ),
                      FilledButton(
                        onPressed: () => setState(() => section = 1),
                        child: const Text('Aprender a usarlas'),
                      ),
                    ],
                    if (section == 1) ...[
                      if (unit.patterns.isNotEmpty) ...[
                        const Text(
                          'Construye tus propias frases',
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                        const Text(
                          'Observa qué partes cambian. Sustituye el detalle del ejemplo por algo que tú necesitarías decir.',
                        ),
                        for (final pattern in unit.patterns)
                          Card(
                            child: Padding(
                              padding: const EdgeInsets.all(16),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.stretch,
                                children: [
                                  Text(
                                    pattern.template,
                                    style: const TextStyle(
                                      fontSize: 19,
                                      fontWeight: FontWeight.w800,
                                    ),
                                  ),
                                  Text(pattern.translation),
                                  if (pattern.note.isNotEmpty)
                                    Text(
                                      pattern.note,
                                      style: const TextStyle(
                                        fontSize: 12,
                                        fontStyle: FontStyle.italic,
                                      ),
                                    ),
                                  for (final example in pattern.examples) ...[
                                    const SizedBox(height: 12),
                                    Tarjeta(
                                      sombra: false,
                                      radio: 16,
                                      onTap: listening
                                          ? null
                                          : () => listen(example.$1),
                                      etiquetaSemantica:
                                          'Escuchar ${example.$1}',
                                      child: Row(
                                        children: [
                                          Expanded(
                                            child: Column(
                                              crossAxisAlignment:
                                                  CrossAxisAlignment.start,
                                              children: [
                                                Text(example.$1),
                                                Text(
                                                  example.$2,
                                                  style: const TextStyle(
                                                    fontSize: 13,
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                          const Icon(
                                            Icons.volume_up_rounded,
                                            color: OL.morado,
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ],
                              ),
                            ),
                          ),
                        const SizedBox(height: 16),
                      ],
                      Text(
                        obj.title,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      Tarjeta(
                        onTap: listening ? null : () => listen(obj.phrase),
                        etiquetaSemantica: 'Escuchar ${obj.phrase}',
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            Text(
                              obj.phrase,
                              style: const TextStyle(
                                fontSize: 22,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                            const SizedBox(height: 12),
                            Text(obj.translation),
                            const SizedBox(height: 12),
                            const Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.volume_up_rounded, color: OL.morado),
                                SizedBox(width: 8),
                                Text(
                                  'Toca la tarjeta para escuchar',
                                  style: TextStyle(
                                    color: OL.morado,
                                    fontWeight: FontWeight.w700,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                      const Text(
                        'Cambia los detalles para hablar de ti. El tutor ajustará las preguntas a tu nivel y te ayudará con las dificultades que vayan apareciendo.',
                      ),
                      const SizedBox(height: 12),
                      FilledButton(
                        onPressed: () => chat(unit),
                        child: const Text('Practicar este objetivo con IA'),
                      ),
                    ],
                    if (section == 2) ...[
                      const Text(
                        'Tu misión con el tutor',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      Text(obj.title),
                      const SizedBox(height: 8),
                      const Text(
                        'Habla o escribe. Recibirás correcciones y una nueva pregunta. Puedes pedir ayuda sin perder tu avance.',
                      ),
                      const SizedBox(height: 12),
                      FilledButton.icon(
                        onPressed: () => chat(unit),
                        icon: const Icon(Icons.mic_rounded),
                        label: const Text('Conversar con IA'),
                      ),
                      if (evidence.isNotEmpty) ...[
                        const SizedBox(height: 12),
                        const Text(
                          'Últimas evidencias · practicar no equivale a dominar',
                          style: TextStyle(fontWeight: FontWeight.w700),
                        ),
                        for (final e in evidence.take(3))
                          ListTile(
                            contentPadding: EdgeInsets.zero,
                            title: Text('${e['tema'] ?? 'Práctica'}'),
                            subtitle: Text(
                              '${e['feedback'] ?? 'Conversación registrada'}',
                            ),
                          ),
                      ],
                    ],
                    if (section == 3) ...[
                      const Text(
                        'Comprueba lo que recuerdas',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      const Text(
                        'Esta comprobación mide reconocimiento de vocabulario. La conversación comprueba cómo lo usas; no certifica tu nivel.',
                      ),
                      const SizedBox(height: 16),
                      Text(
                        '¿Qué significa «${unit.words[question].$1}»?',
                        style: const TextStyle(
                          fontSize: 21,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      for (final word in wordOptions(unit))
                        Padding(
                          padding: const EdgeInsets.only(top: 8),
                          child: OutlinedButton(
                            onPressed: checked
                                ? null
                                : () => setState(() => selected = word.$2),
                            style: OutlinedButton.styleFrom(
                              backgroundColor: selected == word.$2
                                  ? tutor.color.withValues(alpha: .14)
                                  : null,
                            ),
                            child: Text(word.$2),
                          ),
                        ),
                      const SizedBox(height: 12),
                      if (!checked)
                        FilledButton(
                          onPressed: selected == null
                              ? null
                              : () {
                                  final correct =
                                      selected == unit.words[question].$2;
                                  ref.read(progressProvider.notifier).registrarPractica(
                                    'situacion-en-${unit.id}-palabra-$question',
                                    {
                                      'idioma': 'en',
                                      'situacionId': unit.id,
                                      'tipo': 'comprobacion_guiada',
                                      'conApoyo': true,
                                      'habilidad': 'vocabulario',
                                      'tema': unit.words[question].$1,
                                      'correcta': correct,
                                      'feedback':
                                          '${unit.words[question].$1} significa ${unit.words[question].$2}.',
                                      'respuesta': selected,
                                    },
                                  );
                                  setState(() => checked = true);
                                  correct
                                      ? Efectos.correcto()
                                      : Efectos.incorrecto();
                                },
                          child: const Text('Comprobar'),
                        ),
                      if (checked) ...[
                        AnswerFeedback(
                          correct: selected == unit.words[question].$2,
                          title: selected == unit.words[question].$2
                              ? '¡Correcto!'
                              : 'Vamos a repasarlo',
                          child: Text(
                            '${unit.words[question].$1} significa ${unit.words[question].$2}.',
                            style: const TextStyle(fontSize: 17, height: 1.4),
                          ),
                        ),
                        OutlinedButton(
                          onPressed: () => setState(() {
                            question = (question + 1) % unit.words.length;
                            checked = false;
                            selected = null;
                          }),
                          child: const Text('Otra palabra'),
                        ),
                      ],
                      const SizedBox(height: 20),
                      FilledButton.icon(
                        onPressed: () => chat(unit, test: true),
                        icon: const Icon(Icons.record_voice_over),
                        label: const Text('Probar mi comunicación con IA'),
                      ),
                    ],
                  ],
                );
              },
            ),
      ),
    );
  }
}

class SituationSections extends StatelessWidget {
  const SituationSections({
    super.key,
    required this.selected,
    required this.onSelected,
  });
  final int selected;
  final ValueChanged<int> onSelected;
  @override
  Widget build(BuildContext context) => Column(
    children: [
      for (var row = 0; row < 2; row++)
        Padding(
          padding: const EdgeInsets.only(bottom: 6),
          child: Row(
            children: [
              for (var col = 0; col < 2; col++)
                Expanded(
                  child: Padding(
                    padding: EdgeInsets.only(left: col == 0 ? 0 : 6),
                    child: OutlinedButton.icon(
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(
                          vertical: 12,
                          horizontal: 6,
                        ),
                        backgroundColor: selected == row * 2 + col
                            ? Theme.of(context).colorScheme.primaryContainer
                            : null,
                      ),
                      onPressed: () => onSelected(row * 2 + col),
                      icon: Icon(
                        [
                          Icons.translate,
                          Icons.auto_stories,
                          Icons.mic,
                          Icons.fact_check,
                        ][row * 2 + col],
                        size: 18,
                      ),
                      label: Text(
                        [
                          'Vocabulario',
                          'Aprender',
                          'Practicar',
                          'Pruebas',
                        ][row * 2 + col],
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
    ],
  );
}
