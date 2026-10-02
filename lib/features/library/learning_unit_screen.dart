import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/learning_units.dart';
import '../../core/efectos.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../shared/widgets/mascot_coach.dart';
import '../../shared/widgets/skill_badge.dart';
import '../../shared/widgets/widgets.dart';
import '../ruta/opcion_respuesta.dart';
import '../../core/i18n/i18n.dart';

/// Pasos de una lectura/escucha graduada.
enum _Paso { elegir, antes, texto, pregunta, final_ }

/// «Lectura y escucha»: textos graduados del nivel del alumno, con palabras
/// clave antes de empezar y una pregunta por pantalla.
class LearningUnitScreen extends ConsumerStatefulWidget {
  const LearningUnitScreen({super.key, required this.skill, this.nivel = 1});
  final String skill;
  final int nivel;
  @override
  ConsumerState<LearningUnitScreen> createState() => _LearningUnitState();
}

class _LearningUnitState extends ConsumerState<LearningUnitScreen> {
  _Paso paso = _Paso.elegir;
  String? unitId;
  int pregunta = 0;
  int? eleccion;
  bool comprobada = false;
  int aciertos = 0;
  bool busy = false, heard = false, transcript = false;
  final Set<String> transcriptsSeen = {};
  int audioGeneration = 0;
  final scroll = ScrollController();

  /// Solo hay dos materiales: escucha y lectura (cualquier otro valor, como
  /// el antiguo 'vocabulario', se trata como lectura).
  String get skill => widget.skill == 'listening' ? 'listening' : 'reading';
  bool get listening => skill == 'listening';

  String clave(LearningUnit u, LearningQuestion q) =>
      'learn-$skill-${u.id}-${q.id}';

  @override
  void dispose() {
    audioGeneration++;
    VozNube.instancia.parar();
    scroll.dispose();
    super.dispose();
  }

  /// Nivel del alumno; si no tiene material, el nivel inferior más cercano.
  int nivelCon(List<LearningUnit> units) {
    final deseado =
        (widget.nivel != 1
                ? widget.nivel
                : ref.watch(progressProvider).nivelActual)
            .clamp(1, 10);
    final niveles = units.map((u) => u.level).toSet();
    for (var n = deseado; n >= 1; n--) {
      if (niveles.contains(n)) return n;
    }
    for (var n = deseado + 1; n <= 10; n++) {
      if (niveles.contains(n)) return n;
    }
    return deseado;
  }

  bool unidadSuperada(LearningUnit u, Map<String, dynamic> practicas) =>
      u.questions.isNotEmpty &&
      u.questions.every(
        (q) => (practicas[clave(u, q)] as Map?)?['correcta'] == true,
      );

  void irA(_Paso nuevo, {VoidCallback? cambio}) {
    audioGeneration++;
    VozNube.instancia.parar();
    setState(() {
      cambio?.call();
      paso = nuevo;
      busy = false;
    });
    if (scroll.hasClients) scroll.jumpTo(0);
  }

  void abrirUnidad(LearningUnit u) => irA(
    _Paso.antes,
    cambio: () {
      unitId = u.id;
      pregunta = 0;
      eleccion = null;
      comprobada = false;
      aciertos = 0;
      heard = false;
      transcript = false;
    },
  );

  void avisarSinAudio() {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          tr(
            'No se pudo reproducir el audio. Comprueba tu conexión y vuelve a intentarlo.',
          ),
        ),
      ),
    );
  }

  Future<void> escucharPalabra(String palabra) async {
    final p = ref.read(progressProvider);
    final ok = await VozNube.instancia.reproducir(
      palabra,
      p.idiomaMeta,
      voz: p.tutorId,
    );
    if (!ok) avisarSinAudio();
  }

  Future<void> listen(LearningUnit unit) async {
    final generation = ++audioGeneration;
    final p = ref.read(progressProvider);
    setState(() => busy = true);
    final ok = await VozNube.instancia.reproducir(
      unit.passage,
      p.idiomaMeta,
      voz: p.tutorId,
    );
    if (!mounted || generation != audioGeneration) return;
    setState(() {
      busy = false;
      heard = heard || ok;
    });
    if (!ok) avisarSinAudio();
  }

  void comprobar(LearningUnit unit, LearningQuestion q) {
    final elegida = eleccion;
    if (comprobada || elegida == null) return;
    final correcta = elegida == q.answerIndex;
    ref.read(progressProvider.notifier).registrarPractica(clave(unit, q), {
      'idioma': ref.read(progressProvider).idiomaMeta,
      'skill': skill,
      'nivel': unit.level,
      'tema': unit.title,
      'tipo': 'comprobacion_guiada',
      'correcta': correcta,
      'respuesta': q.options[elegida],
      'feedback': q.explanation,
      'conApoyo': listening ? transcriptsSeen.contains(unit.id) : true,
      'audioIniciado': heard,
    });
    correcta ? Efectos.correcto() : Efectos.incorrecto();
    setState(() {
      comprobada = true;
      if (correcta) aciertos++;
    });
  }

  void continuar(LearningUnit unit) {
    if (pregunta + 1 < unit.questions.length) {
      irA(
        _Paso.pregunta,
        cambio: () {
          pregunta++;
          eleccion = null;
          comprobada = false;
        },
      );
    } else {
      Efectos.completado();
      irA(_Paso.final_);
    }
  }

  void volver() {
    if (paso != _Paso.elegir) {
      irA(_Paso.elegir);
    } else {
      context.canPop() ? context.pop() : context.go('/inicio');
    }
  }

  @override
  Widget build(BuildContext context) => PopScope(
    canPop: paso == _Paso.elegir,
    onPopInvokedWithResult: (didPop, _) {
      if (!didPop) irA(_Paso.elegir);
    },
    child: Scaffold(
      appBar: AppBar(
        title: Text(listening ? tr('Escucha') : tr('Lectura')),
        leading: IconButton(
          tooltip: tr('Volver'),
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: volver,
        ),
      ),
      body: Movil(
        child: ref
            .watch(learningUnitsProvider(skill))
            .when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (_, _) => Center(
                child: TextButton(
                  onPressed: () => ref.invalidate(learningUnitsProvider(skill)),
                  child: Text(tr('No se pudo cargar. Reintentar')),
                ),
              ),
              data: (units) {
                final level = nivelCon(units);
                final available = units.where((u) => u.level == level).toList();
                if (available.isEmpty) {
                  return Center(
                    child: Text(tr('Pronto habrá material para tu nivel.')),
                  );
                }
                final unit = available.firstWhere(
                  (u) => u.id == unitId,
                  orElse: () => available.first,
                );
                return switch (paso) {
                  _Paso.elegir => _elegir(available, level),
                  _Paso.antes => _antes(unit),
                  _Paso.texto => _texto(unit),
                  _Paso.pregunta => _pregunta(unit),
                  _Paso.final_ => _final(unit, available),
                };
              },
            ),
      ),
    ),
  );

  /// Contenido desplazable con la acción principal fija abajo.
  Widget _marco(List<Widget> contenido, List<Widget> acciones) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      Expanded(
        child: SingleChildScrollView(
          controller: scroll,
          padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: contenido,
          ),
        ),
      ),
      if (acciones.isNotEmpty)
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
              children: acciones,
            ),
          ),
        ),
    ],
  );

  Widget _elegir(List<LearningUnit> available, int level) {
    final practicas = ref.watch(progressProvider).practicas;
    return _marco([
      Row(
        children: [
          InsigniaHabilidad(skill),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              listening ? tr('Elige qué escuchar') : tr('Elige qué leer'),
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ),
        ],
      ),
      const SizedBox(height: 6),
      Text(
        tr('Nivel {n}', {'n': level}),
        style: const TextStyle(color: OL.gris, fontWeight: FontWeight.w700),
      ),
      const SizedBox(height: 16),
      for (final u in available)
        Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: Tarjeta(
            sombra: false,
            borde: OL.grisClaro,
            etiquetaSemantica: u.title,
            onTap: () => abrirUnidad(u),
            child: Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        u.title,
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        u.objective,
                        style: const TextStyle(color: OL.gris, height: 1.4),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 12),
                unidadSuperada(u, practicas)
                    ? Icon(
                        Icons.check_circle_rounded,
                        color: OL.verde,
                        semanticLabel: tr('Completada'),
                      )
                    : const Icon(Icons.chevron_right_rounded, color: OL.morado),
              ],
            ),
          ),
        ),
    ], const []);
  }

  Widget _antes(LearningUnit unit) => _marco(
    [
      MascotCoach(
        listening: listening,
        message: listening
            ? tr(
                'Conoce estas palabras y luego escucha con calma. Puedes repetir el audio.',
              )
            : tr('Conoce estas palabras y luego búscalas en el texto.'),
      ),
      Text(
        tr('Antes de empezar'),
        style: Theme.of(context).textTheme.headlineMedium,
      ),
      const SizedBox(height: 4),
      Text(
        unit.title,
        style: const TextStyle(color: OL.gris, fontWeight: FontWeight.w700),
      ),
      const SizedBox(height: 16),
      Tarjeta(
        color: OL.moradoSuave,
        sombra: false,
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Icon(Icons.lightbulb_outline_rounded, color: OL.morado),
            const SizedBox(width: 10),
            Expanded(
              child: Text(
                unit.strategy,
                style: const TextStyle(fontSize: 16, height: 1.5),
              ),
            ),
          ],
        ),
      ),
      const SizedBox(height: 20),
      Text(
        tr('Palabras clave'),
        style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900),
      ),
      for (final word in unit.words)
        Padding(
          padding: const EdgeInsets.only(top: 10),
          child: Tarjeta(
            sombra: false,
            borde: OL.grisClaro,
            padding: const EdgeInsets.fromLTRB(16, 10, 8, 14),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SizedBox(height: 6),
                      Text.rich(
                        TextSpan(
                          children: [
                            TextSpan(
                              text: word.word,
                              style: const TextStyle(color: OL.morado),
                            ),
                            TextSpan(
                              text: ' · ${word.translation}',
                              style: const TextStyle(color: OL.texto),
                            ),
                          ],
                        ),
                        style: const TextStyle(
                          fontWeight: FontWeight.w800,
                          fontSize: 17,
                        ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        word.example,
                        style: const TextStyle(fontSize: 16, height: 1.4),
                      ),
                    ],
                  ),
                ),
                IconButton(
                  tooltip: tr('Escuchar «{palabra}»', {'palabra': word.word}),
                  onPressed: () => escucharPalabra(word.word),
                  icon: const Icon(Icons.volume_up_outlined, color: OL.morado),
                ),
              ],
            ),
          ),
        ),
    ],
    [
      BotonPrincipal(
        onPressed: () => irA(_Paso.texto),
        child: Text(listening ? tr('ESCUCHAR') : tr('EMPEZAR A LEER')),
      ),
    ],
  );

  Widget _botonEscuchar(LearningUnit unit, {bool compacto = false}) => Tarjeta(
    color: OL.moradoSuave,
    borde: OL.morado,
    sombra: false,
    etiquetaSemantica: heard ? tr('Volver a escuchar') : tr('Escuchar'),
    onTap: busy ? null : () => listen(unit),
    padding: EdgeInsets.symmetric(horizontal: 16, vertical: compacto ? 12 : 24),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        busy
            ? SizedBox.square(
                dimension: compacto ? 24 : 34,
                child: const CircularProgressIndicator(strokeWidth: 3),
              )
            : Icon(
                heard ? Icons.replay_rounded : Icons.volume_up_rounded,
                color: OL.morado,
                size: compacto ? 26 : 40,
              ),
        const SizedBox(width: 12),
        Flexible(
          child: Text(
            busy
                ? tr('PREPARANDO AUDIO…')
                : heard
                ? tr('VOLVER A ESCUCHAR')
                : tr('ESCUCHAR'),
            style: TextStyle(
              color: OL.morado,
              fontSize: compacto ? 16 : 20,
              fontWeight: FontWeight.w900,
            ),
          ),
        ),
      ],
    ),
  );

  Widget _textoPasaje(LearningUnit unit) => Tarjeta(
    sombra: false,
    borde: OL.grisClaro,
    child: SelectableText(
      unit.passage,
      style: const TextStyle(fontSize: 18, height: 1.65),
    ),
  );

  Widget _texto(LearningUnit unit) => _marco(
    [
      Text(
        unit.title,
        style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w900),
      ),
      const SizedBox(height: 16),
      if (!listening) _textoPasaje(unit),
      if (listening) ...[
        _botonEscuchar(unit),
        const SizedBox(height: 8),
        Text(
          tr('Puedes escucharlo varias veces.'),
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 14, color: OL.gris),
        ),
        const SizedBox(height: 8),
        Align(
          child: TextButton.icon(
            onPressed: () => setState(() {
              transcript = !transcript;
              if (transcript) transcriptsSeen.add(unit.id);
            }),
            icon: Icon(
              transcript
                  ? Icons.visibility_off_outlined
                  : Icons.visibility_outlined,
            ),
            label: Text(
              transcript
                  ? tr('Ocultar transcripción')
                  : tr('Ver transcripción'),
            ),
          ),
        ),
        if (transcript) _textoPasaje(unit),
      ],
    ],
    [
      BotonPrincipal(
        onPressed: () => irA(
          _Paso.pregunta,
          cambio: () {
            pregunta = 0;
            eleccion = null;
            comprobada = false;
            aciertos = 0;
          },
        ),
        child: Text(tr('RESPONDER')),
      ),
    ],
  );

  Widget _pregunta(LearningUnit unit) {
    final q = unit.questions[pregunta.clamp(0, unit.questions.length - 1)];
    final correcta = eleccion == q.answerIndex;
    final faltaAudio = listening && !heard;
    return _marco(
      [
        Row(
          children: [
            Expanded(
              child: BarraProgreso(
                pregunta / unit.questions.length +
                    (comprobada ? 1 / unit.questions.length : 0),
              ),
            ),
            const SizedBox(width: 12),
            Text(
              tr('{n} de {total}', {
                'n': pregunta + 1,
                'total': unit.questions.length,
              }),
              style: const TextStyle(
                color: OL.gris,
                fontWeight: FontWeight.w800,
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        if (listening) ...[
          _botonEscuchar(unit, compacto: true),
          const SizedBox(height: 16),
        ] else
          Align(
            alignment: Alignment.centerLeft,
            child: TextButton.icon(
              onPressed: () => setState(() => transcript = !transcript),
              icon: const Icon(Icons.menu_book_rounded),
              label: Text(
                transcript ? tr('Ocultar el texto') : tr('Ver el texto'),
              ),
            ),
          ),
        if (!listening && transcript) ...[
          _textoPasaje(unit),
          const SizedBox(height: 16),
        ],
        Text(
          q.prompt,
          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900),
        ),
        const SizedBox(height: 14),
        for (var i = 0; i < q.options.length; i++)
          OpcionRespuesta(
            texto: q.options[i],
            estado: comprobada && i == q.answerIndex
                ? EstadoOpcion.correcta
                : comprobada && i == eleccion
                ? EstadoOpcion.incorrecta
                : eleccion == i
                ? EstadoOpcion.seleccionada
                : EstadoOpcion.normal,
            onTap: comprobada
                ? null
                : () {
                    Efectos.toque();
                    setState(() => eleccion = i);
                  },
          ),
        if (faltaAudio && !comprobada)
          Text(
            tr('Escucha el audio primero.'),
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 14, color: OL.gris),
          ),
      ],
      [
        if (comprobada)
          FeedbackDock(
            child: AnswerFeedback(
              correct: correcta,
              title: correcta ? tr('¡Bien!') : tr('Casi'),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (!correcta)
                    Text(
                      tr('Respuesta: {respuesta}', {
                        'respuesta': q.options[q.answerIndex],
                      }),
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  Text(
                    q.explanation,
                    style: const TextStyle(fontSize: 16, height: 1.45),
                  ),
                  if (q.evidence.isNotEmpty) ...[
                    const SizedBox(height: 6),
                    Text(
                      tr('En el texto: “{cita}”', {'cita': q.evidence}),
                      style: const TextStyle(
                        fontSize: 15,
                        fontStyle: FontStyle.italic,
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ),
        if (!comprobada)
          BotonPrincipal(
            onPressed: eleccion == null || faltaAudio
                ? null
                : () => comprobar(unit, q),
            child: Text(tr('COMPROBAR')),
          )
        else
          BotonPrincipal(
            color: correcta ? OL.verde : OL.rojo,
            onPressed: () => continuar(unit),
            child: Text(tr('CONTINUAR')),
          ),
      ],
    );
  }

  Widget _final(LearningUnit unit, List<LearningUnit> available) {
    final total = unit.questions.length;
    final otra = available.length > 1
        ? available[(available.indexOf(unit) + 1) % available.length]
        : unit;
    return _marco(
      [
        const SizedBox(height: 24),
        const Center(child: FeedbackBadge(completed: true, size: 96)),
        const SizedBox(height: 12),
        Text(
          aciertos == total ? tr('¡Lo entendiste todo!') : tr('¡Terminaste!'),
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w900),
        ),
        const SizedBox(height: 8),
        Text(
          tr('{aciertos} de {total} correctas', {
            'aciertos': aciertos,
            'total': total,
          }),
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontSize: 18,
            color: OL.gris,
            fontWeight: FontWeight.w700,
          ),
        ),
        const SizedBox(height: 20),
        Tarjeta(
          sombra: false,
          borde: OL.grisClaro,
          child: Text(
            unit.title,
            textAlign: TextAlign.center,
            style: const TextStyle(fontWeight: FontWeight.w800),
          ),
        ),
      ],
      [
        BotonPrincipal(
          onPressed: () => abrirUnidad(otra),
          child: Text(listening ? tr('OTRA ESCUCHA') : tr('OTRA LECTURA')),
        ),
        TextButton(
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/inicio'),
          child: Text(tr('VOLVER')),
        ),
      ],
    );
  }
}
