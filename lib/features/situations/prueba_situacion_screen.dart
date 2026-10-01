import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/content/situaciones.dart';
import '../../core/efectos.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../shared/widgets/widgets.dart';
import '../ruta/opcion_respuesta.dart';

/// Una pregunta de la prueba de un tramo.
class PreguntaSituacion {
  const PreguntaSituacion({
    required this.enunciado,
    required this.opciones,
    required this.correcta,
    required this.explicacion,
    this.audio,
  });
  final String enunciado, explicacion;
  final List<String> opciones;
  final int correcta;

  /// Texto que se escucha antes de responder (preguntas de escucha).
  final String? audio;
}

/// 10 preguntas del tramo, distintas en cada intento: 6 de significado,
/// 2 de escucha y 2 de «qué dirías» con los objetivos.
List<PreguntaSituacion> preguntasPruebaSituacion(TramoSituacion t, Random rnd) {
  final res = <PreguntaSituacion>[];
  final palabras = [...t.vocabulario]..shuffle(rnd);
  PreguntaSituacion significado(PalabraSituacion p, {required bool oir}) {
    final otras = [
      for (final o in t.vocabulario)
        if (o.id != p.id && o.es != p.es) o.es,
    ]..shuffle(rnd);
    final opciones = [p.es, ...otras.take(3)]..shuffle(rnd);
    return PreguntaSituacion(
      enunciado: oir
          ? 'Escucha. ¿Qué significa?'
          : '¿Qué significa «${p.en}»?',
      opciones: opciones,
      correcta: opciones.indexOf(p.es),
      explicacion: '${p.en} = ${p.es}. ${p.ejemplo}',
      audio: oir ? p.en : null,
    );
  }

  for (final p in palabras.take(6)) {
    res.add(significado(p, oir: false));
  }
  for (final p in palabras.skip(6).take(2)) {
    res.add(significado(p, oir: true));
  }
  final objetivos = [...t.objetivos]..shuffle(rnd);
  for (final o in objetivos.take(2)) {
    final opciones = [for (final x in t.objetivos) x.frase]..shuffle(rnd);
    res.add(
      PreguntaSituacion(
        enunciado: 'Quieres: ${o.titulo.toLowerCase()}. ¿Qué dices?',
        opciones: opciones,
        correcta: opciones.indexOf(o.frase),
        explicacion: '«${o.frase}» = ${o.traduccion}',
      ),
    );
  }
  return res;
}

class PruebaSituacionScreen extends ConsumerStatefulWidget {
  const PruebaSituacionScreen({
    super.key,
    required this.id,
    required this.tramo,
  });
  final int id;
  final Tramo tramo;

  @override
  ConsumerState<PruebaSituacionScreen> createState() =>
      _PruebaSituacionScreenState();
}

class _PruebaSituacionScreenState
    extends ConsumerState<PruebaSituacionScreen> {
  List<PreguntaSituacion>? preguntas;
  int indice = 0, aciertos = 0;
  int? elegida;
  bool comprobada = false, oida = false, terminada = false;

  @override
  void dispose() {
    VozNube.instancia.parar();
    super.dispose();
  }

  String get _idioma => ref.read(progressProvider).idiomaMeta;

  Future<void> _oir(String texto) async {
    final ok = await VozNube.instancia.reproducir(texto, _idioma);
    if (mounted && ok) setState(() => oida = true);
  }

  void _comprobar() {
    final q = preguntas![indice];
    final bien = elegida == q.correcta;
    bien ? Efectos.correcto() : Efectos.incorrecto();
    setState(() {
      comprobada = true;
      if (bien) aciertos++;
    });
  }

  void _siguiente() {
    if (indice + 1 < preguntas!.length) {
      setState(() {
        indice++;
        elegida = null;
        comprobada = false;
        oida = false;
      });
      return;
    }
    final total = preguntas!.length;
    final aprobada = aciertos >= aciertosPruebaSituacion(total);
    final clave = clavePruebaSituacion(_idioma, widget.id, widget.tramo);
    final anterior =
        ref.read(progressProvider).practicas[clave] as Map? ?? const {};
    final mejor = max((anterior['mejor'] as num? ?? 0).toInt(), aciertos);
    ref.read(progressProvider.notifier).registrarPractica(clave, {
      'idioma': _idioma,
      'skill': 'vocabulario',
      'tipo': 'prueba_situacion',
      'situacionId': widget.id,
      'tramo': widget.tramo.name,
      'aciertos': aciertos,
      'total': total,
      'mejor': mejor,
      // Una vez aprobada queda aprobada aunque se repita después.
      'aprobada': aprobada || anterior['aprobada'] == true,
      'correcta': aprobada,
    });
    aprobada ? Efectos.completado() : Efectos.incorrecto();
    setState(() => terminada = true);
  }

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final sit = situacion(widget.id.clamp(1, situaciones.length));
    final contenido = ref
        .watch(situacionesProvider(s.idiomaMeta))
        .valueOrNull?[widget.id];
    if (contenido != null && preguntas == null) {
      preguntas = preguntasPruebaSituacion(
        contenido.tramo(widget.tramo),
        Random(),
      );
    }
    return Scaffold(
      appBar: AppBar(
        title: Text('Prueba · ${widget.tramo.nombre}'),
        leading: IconButton(
          tooltip: 'Salir',
          icon: const Icon(Icons.close_rounded),
          onPressed: () => context.canPop()
              ? context.pop()
              : context.go('/situacion/${widget.id}'),
        ),
      ),
      body: Movil(
        child: preguntas == null
            ? const Center(child: CircularProgressIndicator())
            : terminada
            ? _resultado(sit.nombre)
            : _pregunta(),
      ),
    );
  }

  Widget _pregunta() {
    final q = preguntas![indice];
    final bien = elegida == q.correcta;
    final puede = elegida != null && (q.audio == null || oida);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 12),
          child: Row(
            children: [
              Expanded(
                child: BarraProgreso(
                  (indice + 1) / preguntas!.length,
                  alto: 8,
                ),
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
              if (q.audio != null) ...[
                const SizedBox(height: 12),
                OutlinedButton.icon(
                  onPressed: () => _oir(q.audio!),
                  icon: const Icon(Icons.volume_up_rounded),
                  label: Text(oida ? 'Escuchar otra vez' : 'Escuchar'),
                ),
              ],
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
                child: Text(
                  q.explicacion,
                  style: const TextStyle(height: 1.4),
                ),
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
            onPressed: comprobada ? _siguiente : (puede ? _comprobar : null),
            child: Text(
              comprobada
                  ? (indice + 1 < preguntas!.length ? 'CONTINUAR' : 'VER MI NOTA')
                  : q.audio != null && !oida
                  ? 'ESCUCHA PRIMERO'
                  : 'COMPROBAR',
            ),
          ),
        ),
      ],
    );
  }

  Widget _resultado(String nombre) {
    final total = preguntas!.length;
    final aprobada = aciertos >= aciertosPruebaSituacion(total);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Expanded(
          child: ListView(
            padding: const EdgeInsets.fromLTRB(20, 32, 20, 20),
            children: [
              Center(
                child: FeedbackBadge(correct: aprobada, completed: aprobada, size: 110),
              ),
              const SizedBox(height: 16),
              Text(
                '$aciertos / $total',
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 40, fontWeight: FontWeight.w900),
              ),
              const SizedBox(height: 8),
              Text(
                aprobada
                    ? '¡Aprobaste el tramo ${widget.tramo.nombre} de «$nombre»!'
                    : 'Necesitas ${aciertosPruebaSituacion(total)}. Repasa las palabras y vuelve a intentarlo.',
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 17, height: 1.4),
              ),
              if (aprobada) ...[
                const SizedBox(height: 8),
                const Text(
                  'Para completarlo, practica al menos un objetivo con tu tutor.',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: OL.gris, fontSize: 15),
                ),
              ],
            ],
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 16),
          child: BotonPrincipal(
            onPressed: () => context.canPop()
                ? context.pop()
                : context.go('/situacion/${widget.id}'),
            child: const Text('VOLVER A LA SITUACIÓN'),
          ),
        ),
      ],
    );
  }
}
