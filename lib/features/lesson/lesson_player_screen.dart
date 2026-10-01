import '../../shared/widgets/feedback_experience.dart';

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/barajar.dart';
import '../../core/content/curriculum.dart';
import '../../core/efectos.dart';
import '../../core/voz.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Reproductor de lección: recorre los `steps` y muestra un widget por tipo.
/// Cuenta aciertos, registra errores y al final guarda el progreso.
class LessonPlayerScreen extends ConsumerStatefulWidget {
  const LessonPlayerScreen({super.key, required this.lessonId});
  final String lessonId;

  @override
  ConsumerState<LessonPlayerScreen> createState() => _LessonPlayerScreenState();
}

class _LessonPlayerScreenState extends ConsumerState<LessonPlayerScreen> {
  late final Lesson? lesson = leccionPorId(widget.lessonId);
  int i = 0;
  int aciertos = 0;
  int evaluados = 0;
  int vidas = 4;
  int racha = 0; // aciertos seguidos (combo)

  @override
  void initState() {
    super.initState();
    // Descarga en segundo plano las voces de la lección (una sola vez por frase).
    final l = lesson;
    if (l != null) {
      VozNube.instancia.precargar([
        for (final s in l.steps)
          if (s.type == StepType.flashcard ||
              s.type == StepType.speak ||
              s.type == StepType.listenWrite)
            s.prompt,
      ], idiomaContenido);
    }
  }

  void _resultado(bool correcto, LessonStep step, String respuestaUsuario) {
    evaluados++;
    if (correcto) {
      aciertos++;
      racha++;
    } else {
      racha = 0;
      vidas = (vidas - 1).clamp(0, 4);
      ref
          .read(progressProvider.notifier)
          .agregarError(
            skill: step.skill,
            original: respuestaUsuario.isEmpty
                ? '(sin respuesta)'
                : respuestaUsuario,
            correccion: step.answer.isEmpty ? step.prompt : step.answer,
            explicacion: _explicacion(step),
            origen: lesson!.id,
          );
    }
    setState(() {});
  }

  String _explicacion(LessonStep s) => switch (s.type) {
    StepType.orderWords =>
      'Fíjate en el orden de las palabras: la frase correcta es "${s.answer}".',
    StepType.fillBlank =>
      'Fíjate en el verbo y en la concordancia con el sujeto.',
    StepType.listenWrite => 'Escucha de nuevo y presta atención a cada palabra; revisa la ortografía.',
    StepType.matchPairs =>
      'Repasa el vocabulario de la unidad con las tarjetas.',
    _ =>
      'La forma correcta es "${s.answer.isEmpty ? s.prompt : s.answer}". Practícala en voz alta.',
  };

  void _siguiente() {
    if (i + 1 < lesson!.steps.length) {
      setState(() => i++);
      return;
    }
    final total = evaluados == 0 ? 1 : evaluados;
    ref
        .read(progressProvider.notifier)
        .completarLeccion(lesson!, aciertos: aciertos, total: total);
    context.go(
      '/leccion/${lesson!.id}/resultado?aciertos=$aciertos&total=$total',
    );
  }

  @override
  Widget build(BuildContext context) {
    final l = lesson;
    if (l == null) {
      return const Scaffold(body: Center(child: Text('Lección no encontrada')));
    }
    final step = l.steps[i];
    return Scaffold(
      body: Movil(
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(20, 8, 20, 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Row(
                  children: [
                    IconButton(
                      onPressed: () => context.canPop()
                          ? context.pop()
                          : context.go('/aprender/nivel/${l.nivel}'),
                      icon: const Icon(Icons.close, color: OL.gris),
                    ),
                    Expanded(
                      child: TweenAnimationBuilder<double>(
                        tween: Tween(end: (i + 1) / l.steps.length),
                        duration: const Duration(milliseconds: 450),
                        curve: Curves.easeOutCubic,
                        builder: (_, v, _) => BarraProgreso(v),
                      ),
                    ),
                    const SoundToggle(),
                    const SizedBox(width: 4),
                    AnimatedSwitcher(
                      duration: const Duration(milliseconds: 250),
                      transitionBuilder: (c, a) => ScaleTransition(
                        scale: CurvedAnimation(
                          parent: a,
                          curve: Curves.easeOutBack,
                        ),
                        child: c,
                      ),
                      child: racha >= 2
                          ? Padding(
                              key: ValueKey(racha),
                              padding: const EdgeInsets.only(right: 8),
                              child: Etiqueta(
                                'x$racha',
                                color: const Color(0xFFB8661E),
                                fondo: OL.naranjaSuave,
                                icono: Icons.bolt,
                              ),
                            )
                          : const SizedBox.shrink(),
                    ),
                    Etiqueta('$vidas', color: OL.rojo, icono: Icons.favorite),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  l.titulo,
                  style: const TextStyle(
                    color: OL.gris,
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 14),
                Expanded(
                  child: _StepView(
                    key: ValueKey('${l.id}-$i'),
                    step: step,
                    onResultado: (ok, resp) => _resultado(ok, step, resp),
                    onSiguiente: _siguiente,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _StepView extends StatefulWidget {
  const _StepView({
    super.key,
    required this.step,
    required this.onResultado,
    required this.onSiguiente,
  });
  final LessonStep step;
  final void Function(bool correcto, String respuesta) onResultado;
  final VoidCallback onSiguiente;

  @override
  State<_StepView> createState() => _StepViewState();
}

class _StepViewState extends State<_StepView> {
  bool? correcto; // null = sin comprobar
  String seleccion = '';
  List<String> banco = [];

  /// Opciones en orden aleatorio: en los datos la correcta suele ir primero.
  late final List<String> opciones = barajarDistinto(s.options);
  List<String> respuesta = [];
  final texto = TextEditingController();
  bool mostrarTraduccion = false;
  bool mostrarAudio = false;
  // matchPairs
  String? izq;
  final unidas = <String>{};
  int fallos = 0;
  // roleplay
  int replica = 0;
  // speak (repite en voz alta)
  bool grabando = false;
  String dicho = '';
  double? parecido; // 0..1 tras evaluar
  bool sinMicro = false;

  LessonStep get s => widget.step;

  @override
  void initState() {
    super.initState();
    if (s.type == StepType.orderWords) {
      banco = barajarDistinto(s.answer.split(' '));
    }
    if (s.type == StepType.roleplay) {
      final primera = _replicas().first;
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) {
          Voz.instancia.hablar(primera.$2, idiomaContenido, voz: 'narrador');
        }
      });
    }
    if (s.type == StepType.flashcard ||
        s.type == StepType.speak ||
        s.type == StepType.listenWrite) {
      // La palabra o frase suena sola al aparecer (voz del idioma que se aprende).
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) Voz.instancia.hablar(s.prompt, idiomaContenido);
      });
    }
  }

  @override
  void dispose() {
    Oido.instancia.cancelar();
    Voz.instancia.parar();
    super.dispose();
  }

  Future<void> _grabar() async {
    if (grabando) {
      await Oido.instancia.parar();
      if (!mounted) return;
      setState(() => grabando = false);
      return;
    }
    setState(() {
      grabando = true;
      dicho = '';
      parecido = null;
    });
    final ok = await Oido.instancia.escuchar(
      idiomaContenido,
      (texto, fin) {
        if (!mounted) return;
        setState(() {
          dicho = texto;
          if (fin) {
            grabando = false;
            parecido = similitud(texto, s.prompt);
            if (correcto == null) {
              correcto = parecido! >= 0.6;
              widget.onResultado(correcto!, texto);
            }
          }
        });
      },
      segundos: 60,
      silencio: const Duration(seconds: 3),
      onFin: () {
        if (!mounted) return;
        setState(() {
          grabando = false;
          // Sin voz captada: permitir reintentar y explicar la causa si el sistema la dio.
          if (parecido == null &&
              dicho.isEmpty &&
              Oido.instancia.ultimoError.isNotEmpty) {
            dicho = '';
            sinMicro =
                Oido.instancia.ultimoError.contains('audio') ||
                Oido.instancia.ultimoError.contains('permission');
          }
        });
      },
    );
    if (!ok && mounted) {
      setState(() {
        grabando = false;
        sinMicro = true;
      });
    }
  }

  String _norm(String t) => t
      .toLowerCase()
      .replaceAll(RegExp(r"[^\w\s']"), '')
      .trim()
      .replaceAll(RegExp(r'\s+'), ' ');

  void _comprobar() {
    final String resp;
    final bool ok;
    switch (s.type) {
      case StepType.orderWords:
        resp = respuesta.join(' ');
        ok = _norm(resp) == _norm(s.answer);
      case StepType.listenWrite:
        resp = texto.text;
        ok = _norm(resp) == _norm(s.answer);
      default:
        resp = seleccion;
        ok = seleccion == s.answer;
    }
    setState(() {
      correcto = ok;
      _panel = true;
    });
    ok ? Efectos.correcto() : Efectos.incorrecto();
    widget.onResultado(ok, resp);
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      if (!mounted) return;
      await mostrarPanelResultado(
        context,
        correcto: ok,
        titulo: ok ? '¡Correcto!' : 'Vamos a repasarlo',
        cuerpo: _cuerpoFeedback(),
      );
      if (!mounted) return;
      setState(() => _panel = false);
      widget.onSiguiente();
    });
  }

  /// Panel inferior abierto (lleva su propio SIGUIENTE).
  bool _panel = false;

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context).textTheme;
    final Widget cuerpo = switch (s.type) {
      StepType.flashcard => _flashcard(t),
      StepType.multipleChoice || StepType.fillBlank => _opciones(t),
      StepType.imageChoice => _imagen(t),
      StepType.orderWords => _ordena(t),
      StepType.listenWrite => _escucha(t),
      StepType.matchPairs => _parejas(t),
      StepType.speak => _habla(t),
      StepType.readText => _lectura(t),
      StepType.roleplay => _rol(t),
    };

    final sinComprobar = {
      StepType.flashcard,
      StepType.speak,
      StepType.roleplay,
      StepType.readText,
      StepType.matchPairs,
    }.contains(s.type);
    final puede = switch (s.type) {
      StepType.orderWords => respuesta.isNotEmpty,
      StepType.listenWrite => texto.text.trim().isNotEmpty,
      StepType.matchPairs => unidas.length == s.pairs.length * 2,
      StepType.roleplay => replica >= _replicas().length - 1,
      StepType.multipleChoice ||
      StepType.fillBlank ||
      StepType.imageChoice => seleccion.isNotEmpty,
      _ => true,
    };

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Expanded(child: SingleChildScrollView(child: cuerpo)),
        if (correcto != null && !_panel) FeedbackDock(child: _feedback()),
        const SizedBox(height: 10),
        if (_panel)
          const SizedBox.shrink()
        else if (correcto != null || sinComprobar)
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: correcto == false
                  ? OL.rojo
                  : (correcto == true ? OL.verde : OL.morado),
            ),
            onPressed: puede ? widget.onSiguiente : null,
            child: Text(sinComprobar ? 'CONTINUAR' : 'SIGUIENTE'),
          )
        else
          ElevatedButton(
            onPressed: puede ? _comprobar : null,
            child: const Text('COMPROBAR'),
          ),
      ],
    );
  }

  Widget _feedback() => AnswerFeedback(
    key: ValueKey(correcto),
    correct: correcto!,
    title: correcto! ? '¡Correcto!' : 'Vamos a repasarlo',
    child: _cuerpoFeedback(),
  );

  Widget _cuerpoFeedback() => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      if (!correcto!)
        Text(
          'Respuesta: ${s.answer}',
          style: const TextStyle(fontWeight: FontWeight.w600),
        ),
      if (s.translation.isNotEmpty)
        Text(
          s.translation,
          style: const TextStyle(color: OL.gris, fontSize: 13),
        ),
    ],
  );

  Widget _titulo(TextTheme t, String txt) => Padding(
    padding: const EdgeInsets.only(bottom: 14),
    child: Text(txt, style: t.headlineMedium),
  );

  Widget _flashcard(TextTheme t) => Column(
    children: [
      _titulo(t, 'Nueva palabra'),
      Tarjeta(
        padding: const EdgeInsets.symmetric(vertical: 40, horizontal: 20),
        onTap: () => Voz.instancia.hablar(s.prompt, idiomaContenido),
        etiquetaSemantica: 'Escuchar ${s.prompt}',
        child: Column(
          children: [
            const IconoCuadro(
              Icons.volume_up_outlined,
              tamano: 56,
              radio: 28,
              relleno: true,
            ),
            const SizedBox(height: 20),
            Text(s.prompt, textAlign: TextAlign.center, style: t.headlineLarge),
            const SizedBox(height: 8),
            AnimatedSwitcher(
              duration: const Duration(milliseconds: 200),
              child: mostrarTraduccion
                  ? Text(
                      s.translation,
                      key: const ValueKey('tr'),
                      style: const TextStyle(
                        color: OL.morado,
                        fontSize: 18,
                        fontWeight: FontWeight.w700,
                      ),
                    )
                  : const Text(
                      'Toca la tarjeta para escuchar',
                      key: ValueKey('hint'),
                      style: TextStyle(color: OL.gris),
                    ),
            ),
            TextButton(
              onPressed: () =>
                  setState(() => mostrarTraduccion = !mostrarTraduccion),
              child: Text(
                mostrarTraduccion ? 'OCULTAR TRADUCCIÓN' : 'VER TRADUCCIÓN',
              ),
            ),
          ],
        ),
      ),
    ],
  );

  Widget _opciones(TextTheme t) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      _titulo(
        t,
        s.type == StepType.fillBlank
            ? 'Completa la frase'
            : 'Elige la respuesta correcta',
      ),
      Tarjeta(
        color: OL.moradoSuave,
        sombra: false,
        child: Text(
          s.prompt,
          style: const TextStyle(
            fontSize: 17,
            fontWeight: FontWeight.w600,
            height: 1.4,
          ),
        ),
      ),
      const SizedBox(height: 14),
      for (final o in opciones)
        Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: AnimatedScale(
            scale: seleccion == o && correcto == null ? 1.03 : 1.0,
            duration: const Duration(milliseconds: 160),
            curve: Curves.easeOutBack,
            child: _Opcion(
              texto: o,
              seleccionada: seleccion == o,
              estado: correcto == null
                  ? null
                  : (o == s.answer ? true : (seleccion == o ? false : null)),
              onTap: correcto == null
                  ? () {
                      Efectos.toque();
                      setState(() => seleccion = o);
                      if (s.type == StepType.multipleChoice) {
                        Voz.instancia.hablar(o, idiomaContenido);
                      }
                    }
                  : null,
            ),
          ),
        ),
    ],
  );

  Widget _imagen(TextTheme t) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      _titulo(t, 'Elige la imagen'),
      Tarjeta(
        color: OL.moradoSuave,
        sombra: false,
        child: Text(
          s.prompt,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            height: 1.4,
          ),
        ),
      ),
      const SizedBox(height: 14),
      GridView.count(
        crossAxisCount: 2,
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        mainAxisSpacing: 12,
        crossAxisSpacing: 12,
        childAspectRatio: 1.05,
        children: [
          for (var k = 0; k < s.pairs.length; k++)
            _ImagenOpcion(
              etiqueta: '${k + 1}',
              ruta: s.pairs[k].$2,
              seleccionada: seleccion == s.pairs[k].$1,
              estado: correcto == null
                  ? null
                  : (s.pairs[k].$1 == s.answer
                        ? true
                        : (seleccion == s.pairs[k].$1 ? false : null)),
              onTap: correcto == null
                  ? () => setState(() => seleccion = s.pairs[k].$1)
                  : null,
            ),
        ],
      ),
    ],
  );

  Widget _ordena(TextTheme t) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      _titulo(t, 'Ordena la frase'),
      Tarjeta(
        color: OL.moradoSuave,
        sombra: false,
        child: Row(
          children: [
            const IconoCuadro(Icons.translate, tamano: 36, radio: 18),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    s.hint.isEmpty
                        ? 'Traduce al ${nombreIdiomaContenido()}'
                        : s.hint,
                    style: const TextStyle(
                      color: OL.gris,
                      fontSize: 11,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  Text(
                    s.prompt,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      const SizedBox(height: 14),
      Container(
        constraints: const BoxConstraints(minHeight: 70),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: OL.blanco,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: OL.grisClaro, width: 1.5),
        ),
        child: Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            for (var k = 0; k < respuesta.length; k++)
              _Ficha(
                respuesta[k],
                onTap: correcto == null
                    ? () => setState(() {
                        banco.add(respuesta.removeAt(k));
                      })
                    : null,
              ),
            if (respuesta.isEmpty)
              const Padding(
                padding: EdgeInsets.all(6),
                child: Text(
                  'Toca las palabras en orden',
                  style: TextStyle(color: OL.gris),
                ),
              ),
          ],
        ),
      ),
      const SizedBox(height: 14),
      Wrap(
        spacing: 8,
        runSpacing: 8,
        children: [
          for (var k = 0; k < banco.length; k++)
            _Ficha(
              banco[k],
              onTap: correcto == null
                  ? () => setState(() {
                      respuesta.add(banco.removeAt(k));
                    })
                  : null,
            ),
        ],
      ),
    ],
  );

  Widget _escucha(TextTheme t) {
    void reproducir() {
      Voz.instancia.hablar(s.prompt, idiomaContenido, velocidad: 0.4);
      setState(() => mostrarAudio = true);
      Timer(const Duration(milliseconds: 1800), () {
        if (mounted) setState(() => mostrarAudio = false);
      });
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        _titulo(t, 'Escucha y escribe'),
        Tarjeta(
          onTap: reproducir,
          etiquetaSemantica: 'Reproducir audio para escribir',
          child: Column(
            children: [
              const IconoCuadro(
                Icons.play_arrow_rounded,
                tamano: 72,
                radio: 36,
                relleno: true,
              ),
              const SizedBox(height: 10),
              AnimatedSwitcher(
                duration: const Duration(milliseconds: 200),
                child: mostrarAudio
                    ? const Text(
                        'Reproduciendo…',
                        key: ValueKey('a'),
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontWeight: FontWeight.w700,
                          color: OL.morado,
                        ),
                      )
                    : const Text(
                        'Toca para escuchar (puedes repetirlo las veces que quieras)',
                        key: ValueKey('b'),
                        textAlign: TextAlign.center,
                        style: TextStyle(color: OL.gris, fontSize: 12),
                      ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 14),
        TextField(
          controller: texto,
          enabled: correcto == null,
          onChanged: (_) => setState(() {}),
          minLines: 2,
          maxLines: 3,
          decoration: const InputDecoration(
            hintText: 'Escribe lo que escuches...',
          ),
        ),
        const SizedBox(height: 10),
        if (s.hint.isNotEmpty)
          Align(
            alignment: Alignment.centerLeft,
            child: Etiqueta('Pista: ${s.hint}', icono: Icons.lightbulb_outline),
          ),
      ],
    );
  }

  Widget _parejas(TextTheme t) {
    final izquierda = s.pairs.map((p) => p.$1).toList();
    final derecha = s.pairs.map((p) => p.$2).toList()..sort();
    Widget chip(String txt, bool esIzq) {
      final unida = unidas.contains(txt);
      final sel = esIzq && izq == txt;
      return Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: _Opcion(
          texto: txt,
          seleccionada: sel,
          estado: unida ? true : null,
          onTap: unida
              ? null
              : () {
                  if (esIzq) {
                    setState(() => izq = txt);
                    return;
                  }
                  if (izq == null) return;
                  final par = s.pairs.firstWhere((p) => p.$1 == izq);
                  if (par.$2 == txt) {
                    Efectos.correcto();
                    setState(() {
                      unidas.addAll([izq!, txt]);
                      izq = null;
                      if (unidas.length == s.pairs.length * 2) {
                        widget.onResultado(
                          fallos == 0,
                          fallos == 0 ? 'todas' : '$fallos fallos',
                        );
                      }
                    });
                  } else {
                    Efectos.incorrecto();
                    setState(() {
                      fallos++;
                      izq = null;
                    });
                  }
                },
        ),
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        _titulo(t, 'Une las parejas'),
        const Text(
          'Toca una palabra y luego su traducción',
          style: TextStyle(color: OL.gris),
        ),
        const SizedBox(height: 14),
        Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              child: Column(
                children: [for (final w in izquierda) chip(w, true)],
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                children: [for (final w in derecha) chip(w, false)],
              ),
            ),
          ],
        ),
        if (fallos > 0) Etiqueta('$fallos intentos fallidos', color: OL.rojo),
      ],
    );
  }

  Widget _habla(TextTheme t) {
    final Color estadoColor = parecido == null
        ? OL.gris
        : (parecido! >= 0.6 ? OL.verde : OL.rojo);
    final String mensaje = sinMicro
        ? 'Micrófono no disponible en este dispositivo. Puedes continuar.'
        : grabando
        ? (Oido.instancia.modo == 'nube'
              ? 'Grabando… toca detener al terminar o deja 3 segundos de silencio'
              : 'Escuchando… repite la frase')
        : parecido == null
        ? 'Toca el micrófono y repite la frase'
        : parecido! >= 0.9
        ? 'La transcripción coincide con las palabras del modelo.'
        : parecido! >= 0.6
        ? 'Se reconocieron varias palabras del modelo.'
        : 'No se entendió bien. Escucha el modelo y vuelve a intentarlo.';
    return Column(
      children: [
        _titulo(t, 'Repite en voz alta'),
        Tarjeta(
          padding: const EdgeInsets.symmetric(vertical: 26, horizontal: 20),
          onTap: () =>
              Voz.instancia.hablar(s.prompt, idiomaContenido, velocidad: 0.4),
          etiquetaSemantica: 'Escuchar modelo: ${s.prompt}',
          child: Column(
            children: [
              Text(
                s.prompt,
                textAlign: TextAlign.center,
                style: t.headlineMedium?.copyWith(color: OL.morado),
              ),
              const SizedBox(height: 6),
              Text(
                s.translation,
                style: const TextStyle(color: OL.gris),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 18),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Expanded(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.volume_up_outlined,
                          size: 22,
                          color: OL.morado,
                        ),
                        SizedBox(width: 8),
                        Flexible(
                          child: Text(
                            'Toca la tarjeta para escuchar',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              color: OL.morado,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 12),
                  IconButton.filled(
                    style: IconButton.styleFrom(
                      backgroundColor: grabando ? OL.rojo : OL.morado,
                      fixedSize: const Size(72, 72),
                    ),
                    onPressed: sinMicro ? null : _grabar,
                    icon: Icon(
                      grabando ? Icons.stop : Icons.mic,
                      color: OL.blanco,
                      size: 34,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Text(
                mensaje,
                style: TextStyle(
                  color: estadoColor,
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                ),
                textAlign: TextAlign.center,
              ),
              if (dicho.isNotEmpty) ...[
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 8,
                  ),
                  decoration: BoxDecoration(
                    color: OL.fondo,
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Text(
                    'Transcripción: "$dicho"',
                    style: const TextStyle(fontSize: 13),
                  ),
                ),
              ],
              if (parecido != null) ...[
                const SizedBox(height: 10),
                const Text(
                  'Coincidencia de palabras; no evalúa pronunciación ni entonación.',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 12, color: OL.gris),
                ),
                const SizedBox(height: 6),
                BarraProgreso(parecido!, color: estadoColor),
              ],
            ],
          ),
        ),
      ],
    );
  }

  List<(String, String, String)> _replicas() => [
    for (final linea in s.translation.split('\u0002'))
      if (linea.isNotEmpty)
        (
          linea.split('\u0001')[0],
          linea.split('\u0001')[1],
          linea.split('\u0001').length > 2 ? linea.split('\u0001')[2] : '',
        ),
  ];

  /// Gramática de la unidad + errores típicos de hispanohablantes.
  Widget _lectura(TextTheme t) {
    final errores = _replicas();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        _titulo(t, 'Antes de empezar'),
        if (s.prompt.isNotEmpty)
          Tarjeta(
            color: OL.moradoSuave,
            sombra: false,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'GRAMÁTICA DE LA UNIDAD',
                  style: TextStyle(
                    color: OL.morado,
                    fontSize: 11,
                    fontWeight: FontWeight.w800,
                    letterSpacing: .5,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  s.prompt,
                  style: const TextStyle(fontSize: 15, height: 1.5),
                ),
              ],
            ),
          ),
        if (errores.isNotEmpty) ...[
          const SizedBox(height: 14),
          const Text(
            'Ojo con estos errores',
            style: TextStyle(fontWeight: FontWeight.w800, fontSize: 15),
          ),
          const SizedBox(height: 8),
          for (final e in errores)
            Padding(
              padding: const EdgeInsets.only(bottom: 10),
              child: Tarjeta(
                padding: const EdgeInsets.all(14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.close, size: 16, color: OL.rojo),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            e.$1,
                            style: const TextStyle(
                              color: OL.rojo,
                              decoration: TextDecoration.lineThrough,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        const Icon(Icons.check, size: 16, color: OL.verde),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            e.$2,
                            style: const TextStyle(fontWeight: FontWeight.w700),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Text(
                      e.$3,
                      style: const TextStyle(
                        color: OL.gris,
                        fontSize: 12,
                        height: 1.4,
                      ),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ],
    );
  }

  /// Diálogo de situación real, réplica a réplica, con voz y traducción.
  Widget _rol(TextTheme t) {
    final lineas = _replicas();
    final visibles = lineas.take(replica + 1).toList();
    final fin = replica >= lineas.length - 1;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        _titulo(t, 'Situación real'),
        Text(
          s.prompt,
          style: const TextStyle(color: OL.gris, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 12),
        for (var i = 0; i < visibles.length; i++)
          Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: Align(
              alignment: i.isEven
                  ? Alignment.centerLeft
                  : Alignment.centerRight,
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 300),
                child: Tarjeta(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 11,
                  ),
                  color: i.isEven ? OL.blanco : OL.morado,
                  borde: i.isEven ? OL.grisClaro : OL.morado,
                  radio: 16,
                  sombra: i.isEven,
                  onTap: () => Voz.instancia.hablar(
                    visibles[i].$2,
                    idiomaContenido,
                    voz: i.isEven ? 'narrador' : 'narradora',
                  ),
                  etiquetaSemantica: 'Escuchar ${visibles[i].$2}',
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        visibles[i].$1,
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w700,
                          color: i.isEven ? OL.morado : const Color(0xFFE8E2FF),
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        visibles[i].$2,
                        style: TextStyle(
                          color: i.isEven ? OL.texto : OL.blanco,
                          height: 1.4,
                          fontSize: 15,
                        ),
                      ),
                      if (visibles[i].$3.isNotEmpty)
                        Text(
                          visibles[i].$3,
                          style: TextStyle(
                            color: i.isEven ? OL.gris : const Color(0xFFE8E2FF),
                            fontSize: 12,
                          ),
                        ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        const SizedBox(height: 6),
        if (!fin)
          OutlinedButton.icon(
            onPressed: () {
              setState(() => replica++);
              Voz.instancia.hablar(
                lineas[replica].$2,
                idiomaContenido,
                voz: replica.isEven ? 'narrador' : 'narradora',
              );
            },
            icon: const Icon(Icons.play_arrow_rounded),
            label: Text(
              replica.isEven
                  ? 'Tu turno: escucha y repite, luego sigue'
                  : 'Siguiente réplica',
            ),
          )
        else
          const Text(
            'Toca cualquier burbuja para volver a escucharla.',
            style: TextStyle(color: OL.gris, fontSize: 12),
            textAlign: TextAlign.center,
          ),
      ],
    );
  }
}

class _ImagenOpcion extends StatelessWidget {
  const _ImagenOpcion({
    required this.etiqueta,
    required this.ruta,
    required this.seleccionada,
    this.estado,
    this.onTap,
  });
  final String etiqueta;
  final String ruta;
  final bool seleccionada;
  final bool? estado;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final Color borde = estado == true
        ? OL.verde
        : estado == false
        ? OL.rojo
        : seleccionada
        ? OL.morado
        : OL.grisClaro;
    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: onTap,
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            border: Border.all(
              color: borde,
              width: seleccionada || estado != null ? 3 : 1.5,
            ),
            boxShadow: OL.sombra(0.06),
          ),
          clipBehavior: Clip.antiAlias,
          child: Stack(
            fit: StackFit.expand,
            children: [
              Image.asset(ruta, fit: BoxFit.cover),
              Positioned(
                left: 8,
                top: 8,
                child: CircleAvatar(
                  radius: 13,
                  backgroundColor: estado == true
                      ? OL.verde
                      : estado == false
                      ? OL.rojo
                      : seleccionada
                      ? OL.morado
                      : Colors.black54,
                  child: estado == true
                      ? const Icon(Icons.check, size: 16, color: OL.blanco)
                      : Text(
                          etiqueta,
                          style: const TextStyle(
                            color: OL.blanco,
                            fontSize: 12,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _Opcion extends StatelessWidget {
  const _Opcion({
    required this.texto,
    required this.seleccionada,
    this.estado,
    this.onTap,
  });
  final String texto;
  final bool seleccionada;
  final bool? estado; // true correcto, false incorrecto, null neutro
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final Color borde = estado == true
        ? OL.verde
        : estado == false
        ? OL.rojo
        : seleccionada
        ? OL.morado
        : OL.grisClaro;
    final Color fondo = estado == true
        ? OL.verdeSuave
        : estado == false
        ? OL.rojoSuave
        : seleccionada
        ? OL.moradoSuave
        : OL.blanco;
    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          decoration: BoxDecoration(
            color: fondo,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(
              color: borde,
              width: seleccionada || estado != null ? 2 : 1.5,
            ),
          ),
          child: Row(
            children: [
              Expanded(
                child: Text(
                  texto,
                  style: TextStyle(
                    fontWeight: FontWeight.w600,
                    color: estado == true ? OL.verde : OL.texto,
                  ),
                ),
              ),
              if (estado == true)
                const Icon(Icons.check_circle, color: OL.verde, size: 20),
              if (estado == false)
                const Icon(Icons.cancel, color: OL.rojo, size: 20),
              if (estado == null && seleccionada)
                const Icon(
                  Icons.radio_button_checked,
                  color: OL.morado,
                  size: 20,
                ),
            ],
          ),
        ),
      ),
    );
  }
}

class _Ficha extends StatelessWidget {
  const _Ficha(this.texto, {this.onTap});
  final String texto;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) => Material(
    color: Colors.transparent,
    child: InkWell(
      borderRadius: BorderRadius.circular(10),
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          color: OL.blanco,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: OL.grisClaro),
          boxShadow: OL.sombra(0.06),
        ),
        child: Text(texto, style: const TextStyle(fontWeight: FontWeight.w700)),
      ),
    ),
  );
}
