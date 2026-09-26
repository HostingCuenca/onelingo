import '../../shared/widgets/skill_badge.dart';
import '../../shared/widgets/learning_path.dart';
import '../../shared/widgets/learning_primer.dart';
import '../../shared/widgets/activity_loading.dart';
import '../../core/efectos.dart';
import '../../shared/widgets/feedback_experience.dart';

import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/biblioteca.dart';
import '../../core/content/situation_units.dart';
import '../../core/content/catalog.dart';
import '../../core/diagnostico.dart';
import '../../core/state/providers.dart';
import '../../core/api/sync.dart';
import '../../core/voz.dart';
import '../../shared/widgets/widgets.dart';

class CaminoPersonalizado extends ConsumerWidget {
  const CaminoPersonalizado({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final diag = s.diagnostico?['idioma'] == 'en' ? s.diagnostico : null;
    final prioridades = RutaBiblioteca.prioridades(diag, s.practicas);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(24),
          child: Stack(
            children: [
              Image.asset(
                'assets/img/lectura-equipo.png',
                height: 190,
                width: double.infinity,
                fit: BoxFit.cover,
                excludeFromSemantics: true,
              ),
              Positioned.fill(
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [
                        Colors.transparent,
                        Colors.black.withValues(alpha: .7),
                      ],
                    ),
                  ),
                ),
              ),
              Positioned(
                left: 18,
                bottom: 16,
                right: 18,
                child: Text(
                  'Tu inglés, paso a paso\nNivel ${s.nivelActual} · ${cefrDe(s.nivelActual.toDouble())} orientativo',
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w800,
                    fontSize: 20,
                  ),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 14),
        Tarjeta(
          onTap: () => context.push(
            '/situacion/${suggestedSituation(s.practicas, s.objetivos)}',
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                'Llévalo a una conversación',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 8),
              Text(
                situacion(suggestedSituation(s.practicas, s.objetivos)).nombre,
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 6),
              const Text(
                'Retoma tu situación reciente o empieza por tus objetivos. El tutor usará las dificultades del diagnóstico para orientar la práctica.',
              ),
              const SizedBox(height: 8),
              const Text(
                'Vocabulario → Aprender → Practicar → Pruebas',
                style: TextStyle(color: OL.morado),
              ),
            ],
          ),
        ),
        const SizedBox(height: 14),
        LearningPath(
          nivel: s.nivelActual,
          recommended: prioridades.first,
          practices: s.practicas,
        ),
        const SizedBox(height: 16),
        SizedBox(
          width: double.infinity,
          child: OutlinedButton.icon(
            onPressed: () => context.push('/biblioteca'),
            icon: const Icon(Icons.auto_stories_rounded),
            label: const Text('Explorar biblioteca'),
          ),
        ),
        const SizedBox(height: 8),
        SizedBox(
          width: double.infinity,
          child: FilledButton.icon(
            onPressed: () => context.push('/chat'),
            icon: const Icon(Icons.auto_awesome),
            label: const Text('Práctica con IA'),
          ),
        ),
      ],
    );
  }
}

class LibraryScreen extends ConsumerStatefulWidget {
  const LibraryScreen({super.key, this.skill, this.nivel});
  final String? skill;
  final int? nivel;
  @override
  ConsumerState<LibraryScreen> createState() => _LibraryState();
}

class _LibraryState extends ConsumerState<LibraryScreen> {
  bool loading = true, evaluating = false, played = false, playing = false;
  String? error;
  late int level;
  String skill = 'comprension';
  List<PreguntaDiag> questions = [];
  int index = 0;
  bool started = false, done = false;
  bool? correct;
  String choice = '', feedback = '';
  final input = TextEditingController();
  List<String> words = [];
  List<int> order = [];
  int successes = 0;
  bool manualLevel = false;
  final random = Random();
  PreguntaDiag get q => questions[index];
  @override
  void initState() {
    super.initState();
    skill = widget.skill ?? 'comprension';
    manualLevel = widget.nivel != null;
    final s = ref.read(progressProvider);
    level =
        widget.nivel?.clamp(1, 10) ??
        RutaBiblioteca.nivelSugerido(
          skill,
          s.nivelActual,
          s.diagnostico,
          s.practicas,
        );
    BancoDiag.precargar('en').then((_) {
      if (mounted) {
        setState(() => loading = false);
        // Explain the skill before practice, even on a direct link.
      }
    });
  }

  @override
  void dispose() {
    input.dispose();
    VozNube.instancia.parar();
    super.dispose();
  }

  void begin() {
    final s = ref.read(progressProvider);
    final selected = RutaBiblioteca.seleccionar(
      banco: BancoDiag.de('en'),
      nivel: level,
      nivelFijo: manualLevel,
      skill: skill,
      practicas: s.practicas,
      sectores: s.sectores,
      objetivos: s.objetivos,
    );
    setState(() {
      questions = selected.map((p) => p.barajada(random)).toList();
      index = 0;
      successes = 0;
      started = questions.isNotEmpty;
      done = false;
      error = started ? null : 'No hay actividades para esta selección.';
      if (started) resetQuestion();
    });
  }

  void resetQuestion() {
    correct = null;
    choice = '';
    feedback = '';
    input.clear();
    played = false;
    playing = false;
    error = null;
    order = [];
    words = q.tipo == TipoDiag.ordenar
        ? (q.aceptadas.first.split(RegExp(r'\s+'))..shuffle(random))
        : [];
  }

  Future<void> listen() async {
    if (playing) return;
    final pregunta = q;
    setState(() => playing = true);
    final ok = await VozNube.instancia.reproducir(
      pregunta.texto,
      'en',
      lento: pregunta.nivel <= 3,
    );
    if (!mounted || q != pregunta) return;
    setState(() {
      playing = false;
      played = played || ok;
      error = ok ? null : 'No se pudo reproducir el audio. Reintenta; no se ha evaluado la respuesta.';
    });
  }

  Future<void> submit() async {
    if (correct != null || evaluating || (q.esAuditiva && !played)) return;
    final answer = q.tipo == TipoDiag.ordenar
        ? order.map((i) => words[i]).join(' ')
        : q.conOpciones
        ? choice
        : input.text.trim();
    if (answer.isEmpty) return;
    double? score;
    bool ok;
    String message;
    if (q.esEscritura) {
      setState(() {
        evaluating = true;
        error = null;
      });
      final r = await Sync.instancia.evaluarEscritura(
        idiomaMeta: 'en',
        idiomaNativo: ref.read(progressProvider).idiomaNativo,
        nivelEstimado: q.nivel.toDouble(),
        consigna: q.texto,
        texto: answer,
      );
      if (!mounted) return;
      if (r == null) {
        setState(() {
          evaluating = false;
          error = 'La evaluación con IA no está disponible. Tu texto sigue aquí; reintenta para recibir retroalimentación.';
        });
        return;
      }
      score = (r['puntuacion'] as num).toDouble();
      ok = score >= q.nivel - .5;
      message =
          '${r['comentario'] ?? ''}\n\nVersión revisada:\n${r['correccion'] ?? ''}';
    } else {
      final d = Diagnostico(declarado: level, banco: [])..actual = q;
      ok = d.responder(answer);
      message =
          '${ok ? '' : 'Respuesta: ${q.respuestaCorrecta}\n\n'}${q.explicacion}';
    }
    ok ? Efectos.correcto() : Efectos.incorrecto();
    ref.read(progressProvider.notifier).registrarPractica(q.id, {
      'idioma': 'en',
      'skill': q.skill,
      'tema': q.tema,
      'nivel': q.nivel,
      'correcta': ok,
      'respuesta': answer,
      'feedback': message,
      'puntuacion': ?score,
    });
    setState(() {
      correct = ok;
      feedback = message;
      evaluating = false;
      if (ok) successes++;
    });
  }

  Future<void> next() async {
    await VozNube.instancia.parar();
    if (!mounted) return;
    setState(() {
      if (index + 1 >= questions.length) {
        done = true;
        Efectos.completado();
      } else {
        index++;
        resetQuestion();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tu biblioteca de inglés'),
        actions: const [SoundToggle()],
      ),
      body: Movil(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
          child: loading
              ? const SingleChildScrollView(
                  padding: EdgeInsets.all(24),
                  child: ActivityLoading(),
                )
              : done
              ? finish()
              : started
              ? FeedbackMotion(key: ValueKey(q.clave), child: exercise())
              : choose(),
        ),
      ),
    );
  }

  Widget choose() => ListView(
    children: [
      const Text(
        'Pequeños pasos.\nMás confianza.',
        style: TextStyle(
          fontSize: 30,
          fontWeight: FontWeight.w800,
          height: 1.1,
        ),
      ),
      const SizedBox(height: 12),
      const Text(
        'Automática selecciona ejercicios según tu nivel, objetivos y práctica anterior. La escritura recibe evaluación con IA.',
        style: TextStyle(color: OL.gris, height: 1.5),
      ),
      const SizedBox(height: 20),
      DropdownButtonFormField<int>(
        key: ValueKey(level),
        initialValue: level,
        decoration: const InputDecoration(labelText: 'Nivel de práctica'),
        items: [
          for (var n = 1; n <= 10; n++)
            DropdownMenuItem(
              value: n,
              child: Text(
                'Nivel $n · ${cefrDe(n.toDouble())} · ${n.isOdd ? 'Explora' : 'Consolida'}',
              ),
            ),
        ],
        onChanged: (n) => setState(() {
          level = n!;
          manualLevel = true;
        }),
      ),
      const SizedBox(height: 18),
      for (final h in RutaBiblioteca.habilidades)
        Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: Tarjeta(
            color: skill == h ? OL.moradoSuave : OL.blanco,
            onTap: () => setState(() {
              skill = h;
              if (!manualLevel) {
                final s = ref.read(progressProvider);
                level = RutaBiblioteca.nivelSugerido(
                  h,
                  s.nivelActual,
                  s.diagnostico,
                  s.practicas,
                );
              }
            }),
            child: Row(
              children: [
                InsigniaHabilidad(h),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    skillsDiag[h]!,
                    style: const TextStyle(fontWeight: FontWeight.w700),
                  ),
                ),
                Icon(
                  skill == h ? Icons.check_circle : Icons.circle_outlined,
                  color: OL.morado,
                ),
              ],
            ),
          ),
        ),
      LearningPrimer(skill: skill, nivel: level),
      if (skill != 'escritura' && skill != 'gramatica')
        Padding(
          padding: const EdgeInsets.only(top: 12),
          child: OutlinedButton.icon(
            onPressed: () =>
                context.push('/estudiar?skill=$skill&nivel=$level'),
            icon: const Icon(Icons.menu_book_rounded),
            label: const Text('Aprender con vocabulario y contexto'),
          ),
        ),
      const SizedBox(height: 12),
      if (error != null) Text(error!),
      const SizedBox(height: 12),
      ElevatedButton(onPressed: begin, child: const Text('COMENZAR PRÁCTICA')),
      TextButton(
        onPressed: () => context.push('/chat'),
        child: const Text('Prefiero practicar con IA'),
      ),
      const Text(
        'Equivalencias orientativas. Banco piloto; no es un examen de certificación.',
        style: TextStyle(color: OL.gris, fontSize: 14),
      ),
    ],
  );
  Widget finish() => ListView(
    children: [
      const SizedBox(height: 40),
      const Center(child: FeedbackBadge(completed: true, size: 120)),
      const SizedBox(height: 20),
      const Text(
        'Un paso más en tu camino',
        textAlign: TextAlign.center,
        style: TextStyle(fontWeight: FontWeight.w800, fontSize: 26),
      ),
      const SizedBox(height: 16),
      Text(
        '$successes de ${questions.length} actividades resueltas al nivel de práctica.\nTu siguiente recomendación tendrá en cuenta estas respuestas.',
        textAlign: TextAlign.center,
      ),
      const SizedBox(height: 24),
      ElevatedButton(
        onPressed: () => context.go('/inicio'),
        child: const Text('VER MI SIGUIENTE PASO'),
      ),
      TextButton(
        onPressed: () => setState(() {
          started = false;
          done = false;
        }),
        child: const Text('Explorar otra habilidad'),
      ),
    ],
  );
  Widget exercise() {
    final answered = correct != null;
    final ready = q.tipo == TipoDiag.ordenar
        ? order.length == words.length
        : q.conOpciones
        ? choice.isNotEmpty
        : input.text.trim().isNotEmpty;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Row(
          children: [
            InsigniaHabilidad(q.skill, size: 36),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                '${skillsDiag[q.skill]} · Nivel ${q.nivel}',
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
            ),
            Text('${index + 1}/${questions.length}'),
          ],
        ),
        const SizedBox(height: 12),
        TweenAnimationBuilder<double>(
          tween: Tween(
            begin: 0,
            end: (index + (answered ? 1 : 0)) / questions.length,
          ),
          duration:
              MediaQuery.disableAnimationsOf(context) ||
                  !Efectos.animaciones.value
              ? Duration.zero
              : const Duration(milliseconds: 350),
          builder: (_, value, _) => LinearProgressIndicator(
            value: value,
            minHeight: 8,
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        const SizedBox(height: 16),
        Expanded(
          child: ListView(
            children: [
              if (q.imagen.isNotEmpty && !q.esAuditiva) ...[
                ClipRRect(
                  borderRadius: BorderRadius.circular(20),
                  child: Image.asset(
                    q.imagen,
                    height: 180,
                    width: double.infinity,
                    fit: BoxFit.cover,
                    excludeFromSemantics: true,
                  ),
                ),
                const SizedBox(height: 12),
              ],
              if (q.esAuditiva) ...[
                const Text(
                  'Escucha antes de responder',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
                ),
                const SizedBox(height: 10),
                OutlinedButton.icon(
                  onPressed: playing ? null : listen,
                  icon: Icon(
                    playing ? Icons.graphic_eq : Icons.volume_up_rounded,
                  ),
                  label: Text(
                    playing
                        ? 'Reproduciendo…'
                        : played
                        ? 'Volver a escuchar'
                        : 'Escuchar audio',
                  ),
                ),
                if (answered)
                  Text(q.texto, style: const TextStyle(height: 1.6)),
              ] else if (q.tipo != TipoDiag.ordenar) ...[
                Text(
                  q.pasajeId.isEmpty
                      ? 'Tu actividad'
                      : 'LECTURA · puedes volver al texto en cada pregunta',
                  style: const TextStyle(
                    fontSize: 14,
                    color: OL.morado,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  q.texto,
                  style: TextStyle(
                    height: 1.7,
                    fontSize: q.pasajeId.isEmpty ? 19 : 16,
                  ),
                ),
              ],
              const SizedBox(height: 16),
              Text(
                q.instruccion,
                style: const TextStyle(
                  fontWeight: FontWeight.w800,
                  fontSize: 17,
                ),
              ),
              const SizedBox(height: 12),
              if (q.conOpciones)
                for (final o in q.opciones)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: OutlinedButton(
                      style: OutlinedButton.styleFrom(
                        alignment: Alignment.centerLeft,
                        padding: const EdgeInsets.all(16),
                        backgroundColor: answered && o == q.respuestaCorrecta
                            ? OL.verdeSuave
                            : choice == o
                            ? OL.moradoSuave
                            : null,
                        disabledForegroundColor:
                            answered && o == q.respuestaCorrecta
                            ? const Color(0xFF197D58)
                            : OL.gris,
                      ),
                      onPressed: answered
                          ? null
                          : () => setState(() => choice = o),
                      child: Text(o),
                    ),
                  ),
              if (q.tipo == TipoDiag.ordenar) ...[
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: OL.moradoSuave,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Wrap(
                    spacing: 6,
                    runSpacing: 6,
                    children: [
                      if (order.isEmpty)
                        const Text('Toca las palabras para construir la frase'),
                      for (final i in order)
                        InputChip(
                          label: Text(words[i]),
                          onDeleted: answered
                              ? null
                              : () => setState(() => order.remove(i)),
                        ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 6,
                  runSpacing: 6,
                  children: [
                    for (var i = 0; i < words.length; i++)
                      if (!order.contains(i))
                        ActionChip(
                          label: Text(words[i]),
                          onPressed: answered
                              ? null
                              : () => setState(() => order.add(i)),
                        ),
                  ],
                ),
              ],
              if (!q.conOpciones && q.tipo != TipoDiag.ordenar)
                TextField(
                  controller: input,
                  enabled: !answered && !evaluating,
                  minLines: q.esEscritura ? 5 : 1,
                  maxLines: q.esEscritura ? 10 : 2,
                  onChanged: (_) => setState(() {}),
                  decoration: const InputDecoration(
                    hintText: 'Tu respuesta en inglés',
                    border: OutlineInputBorder(),
                  ),
                ),
              if (error != null)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  child: Text(error!, style: const TextStyle(color: OL.rojo)),
                ),
              if (evaluating)
                const Padding(
                  padding: EdgeInsets.all(20),
                  child: ActivityLoading(
                    compact: true,
                    label: 'Revisando tu respuesta…',
                  ),
                ),
            ],
          ),
        ),
        if (answered)
          FeedbackDock(
            child: AnswerFeedback(
              correct: correct!,
              title: correct! ? '¡Bien resuelto!' : 'Vamos a repasarlo',
              child: Text(feedback, style: const TextStyle(height: 1.5)),
            ),
          ),
        const SizedBox(height: 12),
        ElevatedButton(
          onPressed: answered
              ? next
              : ready && !evaluating && (!q.esAuditiva || played)
              ? submit
              : null,
          child: Text(
            answered
                ? 'CONTINUAR'
                : q.esEscritura
                ? 'EVALUAR CON IA'
                : 'COMPROBAR',
          ),
        ),
      ],
    );
  }
}
