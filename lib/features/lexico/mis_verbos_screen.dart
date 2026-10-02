import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/efectos.dart';
import '../../core/lexico/verbos.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../shared/widgets/widgets.dart';
import '../ruta/opcion_respuesta.dart';

enum _Filtro { minivel, irregulares, regulares, todos }

/// «Mis verbos»: los verbos con su tabla de conjugación y audio. Por defecto,
/// los del nivel del alumno; se puede ver la lista completa como consulta.
class MisVerbosScreen extends ConsumerStatefulWidget {
  const MisVerbosScreen({super.key});

  @override
  ConsumerState<MisVerbosScreen> createState() => _MisVerbosScreenState();
}

class _MisVerbosScreenState extends ConsumerState<MisVerbosScreen> {
  _Filtro filtro = _Filtro.minivel;
  String busqueda = '';

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final nivel = ref.watch(nivelAlumnoProvider);
    final datos = ref.watch(verbosProvider(s.idiomaMeta));
    return Scaffold(
      appBar: AppBar(title: const Text('Mis verbos')),
      body: Movil(
        child: datos.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (_, _) => const Center(child: Text('No se pudo cargar.')),
          data: (v) {
            if (v == null) {
              return const Padding(
                padding: EdgeInsets.all(24),
                child: Text(
                  'Los verbos de este idioma llegan con su nuevo curso.',
                  style: TextStyle(fontSize: 17),
                ),
              );
            }
            final q = busqueda.trim().toLowerCase();
            final lista = [
              for (final x in v.verbos)
                if ((switch (filtro) {
                      _Filtro.minivel => x.nivel <= nivel,
                      _Filtro.irregulares => x.irregular,
                      _Filtro.regulares => !x.irregular,
                      _Filtro.todos => true,
                    }) &&
                    (q.isEmpty ||
                        x.infinitivo.contains(q) ||
                        x.es.toLowerCase().contains(q) ||
                        x.formas.values.any((f) => f.contains(q))))
                  x,
            ];
            final practicables = [
              for (final x in v.verbos)
                if (x.nivel <= nivel) x,
            ];
            return Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Expanded(
                  child: ListView(
                    padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
                    children: [
                      const Text(
                        'Toca un verbo para ver cómo se conjuga y escucharlo. Los irregulares hay que memorizarlos: practícalos a menudo.',
                        style: TextStyle(color: OL.gris, fontSize: 15, height: 1.4),
                      ),
                      const SizedBox(height: 12),
                      TextField(
                        onChanged: (x) => setState(() => busqueda = x),
                        decoration: const InputDecoration(
                          hintText: 'Buscar verbo (go, went, ir…)',
                          prefixIcon: Icon(Icons.search),
                        ),
                      ),
                      const SizedBox(height: 10),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          for (final (f, nombre) in [
                            (_Filtro.minivel, 'De mi nivel'),
                            (_Filtro.irregulares, 'Irregulares'),
                            (_Filtro.regulares, 'Regulares'),
                            (_Filtro.todos, 'Todos'),
                          ])
                            ChoiceChip(
                              label: Text(nombre),
                              selected: filtro == f,
                              onSelected: (_) => setState(() => filtro = f),
                              selectedColor: OL.moradoClaro,
                            ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Text(
                        '${lista.length} verbos',
                        style: const TextStyle(color: OL.gris, fontSize: 14),
                      ),
                      const SizedBox(height: 6),
                      for (final x in lista)
                        Padding(
                          padding: const EdgeInsets.only(bottom: 6),
                          child: Tarjeta(
                            sombra: false,
                            onTap: () => context.push('/verbos/${x.id}'),
                            padding: const EdgeInsets.symmetric(
                              horizontal: 14,
                              vertical: 10,
                            ),
                            child: Row(
                              children: [
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        x.infinitivo,
                                        style: const TextStyle(
                                          fontSize: 17,
                                          fontWeight: FontWeight.w900,
                                        ),
                                      ),
                                      Text(
                                        x.es,
                                        style: const TextStyle(
                                          color: OL.gris,
                                          fontSize: 14,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                Flexible(
                                  child: Text(
                                    '${x.formas['pasado']} · ${x.formas['participio']}',
                                    textAlign: TextAlign.end,
                                    style: TextStyle(
                                      fontWeight: FontWeight.w800,
                                      color: x.irregular
                                          ? OL.naranja
                                          : OL.verde,
                                    ),
                                  ),
                                ),
                                const Icon(
                                  Icons.chevron_right_rounded,
                                  color: OL.gris,
                                ),
                              ],
                            ),
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
                    padding: const EdgeInsets.fromLTRB(20, 4, 20, 12),
                    child: BotonPrincipal(
                      onPressed: practicables.length < 3
                          ? null
                          : () => context.push('/verbos/practica'),
                      child: const Text('PRACTICAR VERBOS'),
                    ),
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}

/// Un verbo: formas, tabla por tiempo con audio y ejemplo.
class VerboScreen extends ConsumerStatefulWidget {
  const VerboScreen({super.key, required this.id});
  final String id;

  @override
  ConsumerState<VerboScreen> createState() => _VerboScreenState();
}

class _VerboScreenState extends ConsumerState<VerboScreen> {
  String? tiempo;

  @override
  void dispose() {
    VozNube.instancia.parar();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final idioma = ref.watch(progressProvider).idiomaMeta;
    final v = ref.watch(verbosProvider(idioma)).valueOrNull;
    final verbo = v?.porId(widget.id);
    void oir(String t) => VozNube.instancia.reproducir(t, idioma);
    return Scaffold(
      appBar: AppBar(title: Text(verbo?.infinitivo ?? 'Verbo')),
      body: Movil(
        child: v == null || verbo == null
            ? const Center(child: CircularProgressIndicator())
            : ListView(
                padding: const EdgeInsets.fromLTRB(20, 8, 20, 32),
                children: [
                  Tarjeta(
                    color: verbo.irregular ? OL.naranjaSuave : OL.verdeSuave,
                    sombra: false,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Expanded(
                              child: Text(
                                'to ${verbo.infinitivo}',
                                style: const TextStyle(
                                  fontSize: 26,
                                  fontWeight: FontWeight.w900,
                                ),
                              ),
                            ),
                            Etiqueta(
                              verbo.irregular ? 'Irregular' : 'Regular',
                              color: verbo.irregular ? OL.naranja : OL.verde,
                            ),
                          ],
                        ),
                        Text(verbo.es, style: const TextStyle(fontSize: 17)),
                        const SizedBox(height: 10),
                        InkWell(
                          onTap: () => oir(
                            '${verbo.infinitivo}, ${verbo.formas['pasado']}, ${verbo.formas['participio']}',
                          ),
                          child: Row(
                            children: [
                              const Icon(
                                Icons.volume_up_rounded,
                                color: OL.morado,
                              ),
                              const SizedBox(width: 6),
                              Expanded(
                                child: Text(
                                  '${verbo.infinitivo} · ${verbo.formas['pasado']} · ${verbo.formas['participio']}',
                                  style: const TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.w800,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        const Text(
                          'infinitivo · pasado · participio',
                          style: TextStyle(color: OL.gris, fontSize: 13),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 14),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      for (final t in v.tiempos)
                        ChoiceChip(
                          label: Text(t.nombre),
                          selected: (tiempo ?? v.tiempos.first.id) == t.id,
                          onSelected: (_) => setState(() => tiempo = t.id),
                          selectedColor: OL.moradoClaro,
                        ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Builder(
                    builder: (_) {
                      final t = v.tiempos.firstWhere(
                        (x) => x.id == (tiempo ?? v.tiempos.first.id),
                      );
                      final formas = verbo.tablas[t.id] ?? const [];
                      return Tarjeta(
                        sombra: false,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            Text(
                              t.uso,
                              style: const TextStyle(
                                color: OL.gris,
                                fontSize: 14,
                              ),
                            ),
                            const SizedBox(height: 6),
                            for (var i = 0;
                                i < formas.length && i < v.personas.length;
                                i++)
                              InkWell(
                                onTap: () =>
                                    oir('${v.personas[i].meta.split(' /').first} ${formas[i]}'),
                                child: Padding(
                                  padding: const EdgeInsets.symmetric(
                                    vertical: 7,
                                  ),
                                  child: Row(
                                    children: [
                                      SizedBox(
                                        width: 120,
                                        child: Column(
                                          crossAxisAlignment:
                                              CrossAxisAlignment.start,
                                          children: [
                                            Text(
                                              v.personas[i].meta,
                                              style: const TextStyle(
                                                fontSize: 15,
                                                fontWeight: FontWeight.w700,
                                              ),
                                            ),
                                            Text(
                                              v.personas[i].es,
                                              style: const TextStyle(
                                                color: OL.gris,
                                                fontSize: 12,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                      Expanded(
                                        child: Text(
                                          formas[i],
                                          style: const TextStyle(
                                            fontSize: 17,
                                            fontWeight: FontWeight.w800,
                                          ),
                                        ),
                                      ),
                                      const Icon(
                                        Icons.volume_up_rounded,
                                        color: OL.morado,
                                        size: 18,
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                          ],
                        ),
                      );
                    },
                  ),
                  const SizedBox(height: 14),
                  const TituloSeccion('Ejemplo'),
                  const SizedBox(height: 8),
                  Tarjeta(
                    sombra: false,
                    onTap: () => oir(verbo.ejemploMeta),
                    child: Row(
                      children: [
                        const Icon(Icons.volume_up_rounded, color: OL.morado),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                verbo.ejemploMeta,
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                              Text(
                                verbo.ejemploEs,
                                style: const TextStyle(color: OL.gris),
                              ),
                            ],
                          ),
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

/// Práctica de 10 preguntas con los verbos del nivel del alumno.
class PracticaVerbosScreen extends ConsumerStatefulWidget {
  const PracticaVerbosScreen({super.key});

  @override
  ConsumerState<PracticaVerbosScreen> createState() =>
      _PracticaVerbosScreenState();
}

class _PracticaVerbosScreenState extends ConsumerState<PracticaVerbosScreen> {
  List<PreguntaVerbo>? preguntas;
  int indice = 0, aciertos = 0;
  int? elegida;
  bool comprobada = false;

  void _comprobar() {
    final q = preguntas![indice];
    final bien = elegida == q.correcta;
    bien ? Efectos.correcto() : Efectos.incorrecto();
    final s = ref.read(progressProvider);
    ref.read(progressProvider.notifier).registrarPractica(
      'verbo:${s.idiomaMeta}:${q.verbo.id}',
      {
        'idioma': s.idiomaMeta,
        'skill': 'gramatica',
        'tipo': 'verbo',
        'tema': q.verbo.infinitivo,
        'correcta': bien,
      },
    );
    setState(() {
      comprobada = true;
      if (bien) aciertos++;
    });
  }

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final nivel = ref.watch(nivelAlumnoProvider);
    final v = ref.watch(verbosProvider(s.idiomaMeta)).valueOrNull;
    if (v != null && preguntas == null) {
      preguntas = preguntasVerbos(
        [
          for (final x in v.verbos)
            if (x.nivel <= nivel) x,
        ],
        Random(),
      );
    }
    final fin = preguntas != null && indice >= preguntas!.length;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Practicar verbos'),
        leading: IconButton(
          tooltip: 'Salir',
          icon: const Icon(Icons.close_rounded),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/verbos'),
        ),
      ),
      body: Movil(
        child: preguntas == null
            ? const Center(child: CircularProgressIndicator())
            : fin
            ? _final()
            : _pregunta(),
      ),
    );
  }

  Widget _pregunta() {
    final q = preguntas![indice];
    final bien = elegida == q.correcta;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 12),
          child: Row(
            children: [
              Expanded(
                child: BarraProgreso((indice + 1) / preguntas!.length, alto: 8),
              ),
              const SizedBox(width: 12),
              Text(
                '${indice + 1} / ${preguntas!.length}',
                style: const TextStyle(color: OL.gris),
              ),
            ],
          ),
        ),
        Expanded(
          child: ListView(
            padding: const EdgeInsets.fromLTRB(20, 4, 20, 20),
            children: [
              Text(
                q.enunciado,
                style: const TextStyle(
                  fontSize: 21,
                  fontWeight: FontWeight.w900,
                ),
              ),
              const SizedBox(height: 16),
              for (var i = 0; i < q.opciones.length; i++)
                OpcionRespuesta(
                  texto: q.opciones[i],
                  estado: !comprobada
                      ? (elegida == i
                            ? EstadoOpcion.seleccionada
                            : EstadoOpcion.normal)
                      : i == q.correcta
                      ? EstadoOpcion.correcta
                      : i == elegida
                      ? EstadoOpcion.incorrecta
                      : EstadoOpcion.normal,
                  onTap: comprobada ? null : () => setState(() => elegida = i),
                ),
            ],
          ),
        ),
        if (comprobada)
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            child: FeedbackDock(
              child: AnswerFeedback(
                correct: bien,
                title: bien ? '¡Bien!' : 'Casi',
                child: Text(q.explicacion, style: const TextStyle(height: 1.4)),
              ),
            ),
          ),
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 16),
          child: BotonPrincipal(
            color: !comprobada
                ? OL.morado
                : bien
                ? OL.verde
                : OL.rojo,
            onPressed: comprobada
                ? () => setState(() {
                    indice++;
                    elegida = null;
                    comprobada = false;
                    if (indice >= preguntas!.length) Efectos.completado();
                  })
                : (elegida == null ? null : _comprobar),
            child: Text(comprobada ? 'CONTINUAR' : 'COMPROBAR'),
          ),
        ),
      ],
    );
  }

  Widget _final() => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      Expanded(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 32, 20, 20),
          children: [
            const Center(child: FeedbackBadge(completed: true, size: 110)),
            const SizedBox(height: 16),
            Text(
              '$aciertos / ${preguntas!.length}',
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 40, fontWeight: FontWeight.w900),
            ),
            const SizedBox(height: 8),
            const Text(
              'Los irregulares se aprenden repitiendo: vuelve mañana y verás cómo salen solos.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16, height: 1.4, color: OL.gris),
            ),
          ],
        ),
      ),
      Padding(
        padding: const EdgeInsets.fromLTRB(20, 0, 20, 16),
        child: BotonPrincipal(
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/verbos'),
          child: const Text('VOLVER A MIS VERBOS'),
        ),
      ),
    ],
  );
}
