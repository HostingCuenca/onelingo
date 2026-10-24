import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/efectos.dart';
import '../../core/lexico/imagenes.dart';
import '../../core/lexico/lexico.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../shared/widgets/widgets.dart';
import '../ruta/opcion_respuesta.dart';
import '../../core/i18n/i18n.dart';

/// Formas de preguntar una palabra; se alternan dentro de la sesión.
/// `imagen`: escucha la palabra y elige su ilustración entre cuatro.
enum FormaPregunta { significado, inversa, escucha, imagen }

class PreguntaPalabra {
  const PreguntaPalabra(this.entrada, this.forma, this.opciones, this.correcta);
  final EntradaLexico entrada;
  final FormaPregunta forma;

  /// Textos o, en la forma `imagen`, rutas de las ilustraciones.
  final List<String> opciones;
  final int correcta;
  bool get escucha =>
      forma == FormaPregunta.escucha || forma == FormaPregunta.imagen;
}

/// «Escucha y elige la imagen»: la de la palabra y tres de otras familias
/// (que no se confundan a la vista); null si no hay con qué armarla.
PreguntaPalabra? preguntaImagen(
  EntradaLexico e,
  ImagenesVocab imagenes,
  Random rnd,
) {
  final propia = imagenes.porClave[e.clave];
  if (propia == null) return null;
  final otras = distractoresImagen(propia, imagenes.archivos, rnd);
  if (otras.length < 3) return null;
  final opciones = [propia, ...otras]..shuffle(rnd);
  return PreguntaPalabra(e, FormaPregunta.imagen, [
    for (final a in opciones) rutaImagenVocab(a),
  ], opciones.indexOf(propia));
}

/// Pregunta de una palabra con 3 distractores del mismo idioma, preferidos de
/// un nivel parecido y siempre distintos en significado.
PreguntaPalabra preguntaPalabra(
  EntradaLexico e,
  FormaPregunta forma,
  List<EntradaLexico> banco,
  Random rnd,
) {
  final inversa = forma == FormaPregunta.inversa;
  String texto(EntradaLexico x) => inversa ? x.texto : x.traduccion;
  final candidatos =
      [
          for (final x in banco)
            if (x.clave != e.clave &&
                x.traduccion.toLowerCase() != e.traduccion.toLowerCase() &&
                texto(x).toLowerCase() != texto(e).toLowerCase())
              x,
        ]
        ..shuffle(rnd)
        ..sort(
          (a, b) =>
              (a.nivel - e.nivel).abs().compareTo((b.nivel - e.nivel).abs()),
        );
  final opciones = <String>[texto(e)];
  for (final x in candidatos) {
    if (opciones.length == 4) break;
    if (!opciones.contains(texto(x))) opciones.add(texto(x));
  }
  opciones.shuffle(rnd);
  return PreguntaPalabra(e, forma, opciones, opciones.indexOf(texto(e)));
}

class RepasoPalabrasScreen extends ConsumerStatefulWidget {
  const RepasoPalabrasScreen({super.key});

  @override
  ConsumerState<RepasoPalabrasScreen> createState() =>
      _RepasoPalabrasScreenState();
}

class _RepasoPalabrasScreenState extends ConsumerState<RepasoPalabrasScreen> {
  final rnd = Random();
  List<PreguntaPalabra>? cola;
  final respondidas = <String>{};
  int indice = 0, aciertos = 0, total = 0;
  int? elegida;
  bool comprobada = false, oida = false;

  @override
  void dispose() {
    VozNube.instancia.parar();
    super.dispose();
  }

  String get _idioma => ref.read(progressProvider).idiomaMeta;

  void _preparar(
    List<EntradaLexico> mias,
    LexicoIndice lexico,
    ImagenesVocab imagenes,
  ) {
    final s = ref.read(progressProvider);
    // Con lector de pantalla las imágenes no se distinguen: esa forma no se usa.
    final conImagen = !MediaQuery.accessibleNavigationOf(context);
    final sesion = seleccionarRepaso(
      mias,
      repasoLexico(s.practicas, s.idiomaMeta),
      DateTime.now(),
    );
    final banco = mias.length >= 8 ? mias : lexico.entradas.values.toList();
    PreguntaPalabra pregunta(int i) {
      final forma = FormaPregunta.values[i % FormaPregunta.values.length];
      return (forma == FormaPregunta.imagen && conImagen
              ? preguntaImagen(sesion[i], imagenes, rnd)
              : null) ??
          preguntaPalabra(
            sesion[i],
            forma == FormaPregunta.imagen ? FormaPregunta.escucha : forma,
            banco,
            rnd,
          );
    }

    cola = [for (var i = 0; i < sesion.length; i++) pregunta(i)];
    total = sesion.length;
  }

  void _comprobar() {
    final q = cola![indice];
    final bien = elegida == q.correcta;
    bien ? Efectos.correcto() : Efectos.incorrecto();
    // Solo la primera respuesta de la sesión cuenta para el repaso.
    if (respondidas.add(q.entrada.clave)) {
      if (bien) aciertos++;
      final s = ref.read(progressProvider);
      final nuevo = responderPalabra(
        repasoLexico(s.practicas, _idioma)[q.entrada.clave],
        bien,
        DateTime.now(),
      );
      ref.read(progressProvider.notifier).guardarRepasoPalabras(_idioma, {
        q.entrada.clave: nuevo.toJson(),
      }, bien ? 1 : 0);
      // La fallada vuelve al final, preguntada de otra forma.
      if (!bien) {
        final banco = [for (final p in cola!) p.entrada];
        cola!.add(
          preguntaPalabra(q.entrada, FormaPregunta.significado, banco, rnd),
        );
      }
    }
    setState(() => comprobada = true);
  }

  void _siguiente() => setState(() {
    indice++;
    elegida = null;
    comprobada = false;
    oida = false;
    if (indice >= cola!.length) Efectos.completado();
  });

  Future<void> _oir(String texto) async {
    final ok = await VozNube.instancia.reproducir(texto, _idioma);
    if (mounted && ok) setState(() => oida = true);
  }

  @override
  Widget build(BuildContext context) {
    final mias = ref.watch(misPalabrasProvider).valueOrNull;
    final lexico = ref.watch(lexicoProvider).valueOrNull;
    final imagenes = ref.watch(imagenesVocabProvider(_idioma)).valueOrNull;
    if (cola == null && mias != null && lexico != null && imagenes != null) {
      _preparar(mias, lexico, imagenes);
    }
    return Scaffold(
      appBar: AppBar(
        title: Text(tr('Repaso de palabras')),
        leading: IconButton(
          tooltip: tr('Salir'),
          icon: const Icon(Icons.close_rounded),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/palabras'),
        ),
      ),
      body: Movil(
        child: cola == null
            ? const Center(child: CircularProgressIndicator())
            : cola!.isEmpty || indice >= cola!.length
            ? _final()
            : _pregunta(),
      ),
    );
  }

  Widget _pregunta() {
    final q = cola![indice];
    final bien = elegida == q.correcta;
    final puede = elegida != null && (!q.escucha || oida);
    final enunciado = switch (q.forma) {
      FormaPregunta.significado => tr('¿Qué significa «{palabra}»?', {
        'palabra': q.entrada.texto,
      }),
      FormaPregunta.inversa => tr('¿Cómo se dice «{palabra}»?', {
        'palabra': q.entrada.traduccion,
      }),
      FormaPregunta.escucha => tr('Escucha. ¿Qué significa?'),
      FormaPregunta.imagen => tr('Escucha y elige la imagen'),
    };
    EstadoOpcion estado(int i) => !comprobada
        ? (elegida == i ? EstadoOpcion.seleccionada : EstadoOpcion.normal)
        : i == q.correcta
        ? EstadoOpcion.correcta
        : i == elegida
        ? EstadoOpcion.incorrecta
        : EstadoOpcion.normal;
    final imagen = ref
        .watch(imagenesVocabProvider(_idioma))
        .valueOrNull
        ?.de(q.entrada.texto);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 12),
          child: Row(
            children: [
              Expanded(
                child: BarraProgreso((indice + 1) / cola!.length, alto: 8),
              ),
              const SizedBox(width: 12),
              Text(
                '${indice + 1} / ${cola!.length}',
                style: const TextStyle(color: OL.gris),
              ),
            ],
          ),
        ),
        Expanded(
          child: ListView(
            padding: const EdgeInsets.fromLTRB(20, 4, 20, 20),
            children: [
              if (indice >= total)
                Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: Etiqueta(
                      tr('Otra vez'),
                      color: OL.naranja,
                      fondo: OL.naranjaSuave,
                      icono: Icons.replay_rounded,
                    ),
                  ),
                ),
              Text(
                enunciado,
                style: const TextStyle(
                  fontSize: 21,
                  fontWeight: FontWeight.w900,
                ),
              ),
              if (q.escucha) ...[
                const SizedBox(height: 12),
                OutlinedButton.icon(
                  onPressed: () => _oir(q.entrada.texto),
                  icon: const Icon(Icons.volume_up_rounded),
                  label: Text(oida ? tr('Escuchar otra vez') : tr('Escuchar')),
                ),
              ],
              const SizedBox(height: 16),
              if (q.forma == FormaPregunta.imagen)
                GridView.count(
                  crossAxisCount: 2,
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 2,
                  childAspectRatio: .9,
                  children: [
                    for (var i = 0; i < q.opciones.length; i++)
                      OpcionRespuesta(
                        texto: tr('Imagen {n}', {'n': i + 1}),
                        imagen: q.opciones[i],
                        estado: estado(i),
                        onTap: comprobada
                            ? null
                            : () => setState(() => elegida = i),
                      ),
                  ],
                )
              else
                for (var i = 0; i < q.opciones.length; i++)
                  OpcionRespuesta(
                    texto: q.opciones[i],
                    estado: estado(i),
                    onTap: comprobada
                        ? null
                        : () => setState(() => elegida = i),
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
                title: bien ? tr('¡Bien!') : tr('Casi'),
                child: Row(
                  children: [
                    if (imagen != null) ...[
                      ImagenVocab(imagen, lado: 56, radio: 12),
                      const SizedBox(width: 12),
                    ],
                    Expanded(
                      child: Text(
                        '${q.entrada.texto} = ${q.entrada.traduccion}'
                        '${q.entrada.ejemplo == null ? '' : '\n${q.entrada.ejemplo}'}',
                        style: const TextStyle(height: 1.4),
                      ),
                    ),
                  ],
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
                  ? tr('CONTINUAR')
                  : q.escucha && !oida
                  ? tr('ESCUCHA PRIMERO')
                  : tr('COMPROBAR'),
            ),
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
              total == 0
                  ? tr('Todo al día')
                  : tr('{aciertos} de {total} a la primera', {
                      'aciertos': aciertos,
                      'total': total,
                    }),
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 28, fontWeight: FontWeight.w900),
            ),
            const SizedBox(height: 10),
            Text(
              tr(
                'Las que aciertas vuelven cada vez más espaciadas; las que fallas, mañana. Así se quedan en la memoria.',
              ),
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 16, height: 1.4, color: OL.gris),
            ),
          ],
        ),
      ),
      Padding(
        padding: const EdgeInsets.fromLTRB(20, 0, 20, 16),
        child: BotonPrincipal(
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/palabras'),
          child: Text(tr('VOLVER A MIS PALABRAS')),
        ),
      ),
    ],
  );
}
