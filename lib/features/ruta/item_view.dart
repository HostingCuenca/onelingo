import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/correccion.dart';
import '../../core/aprendizaje/modelos.dart';
import '../../core/efectos.dart';
import '../../core/voz.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../shared/widgets/lumo.dart';
import '../../shared/widgets/widgets.dart';
import 'opcion_respuesta.dart';

/// Reproduce un texto del idioma meta en su idioma: voz de la nube con el
/// idioma forzado y, para sílabas sueltas no latinas o sin sesión, la voz
/// nativa del dispositivo.
Future<void> escucharTexto(BuildContext context, String texto, String idioma) =>
    Voz.instancia.hablar(
      texto,
      idioma,
      sistema: mejorConVozDelSistema(texto, idioma),
    );

/// Botón de audio reutilizable.
class BotonAudio extends StatelessWidget {
  const BotonAudio({
    super.key,
    required this.texto,
    required this.idioma,
    this.etiqueta,
    this.grande = false,
  });
  final String texto, idioma;
  final String? etiqueta;
  final bool grande;
  @override
  Widget build(BuildContext context) {
    final boton = grande
        ? FilledButton.tonalIcon(
            onPressed: () => escucharTexto(context, texto, idioma),
            icon: const Icon(Icons.volume_up_rounded, size: 30),
            label: Padding(
              padding: const EdgeInsets.symmetric(vertical: 14),
              child: Text(etiqueta ?? 'Escuchar'),
            ),
          )
        : IconButton(
            tooltip: etiqueta ?? 'Escuchar',
            onPressed: () => escucharTexto(context, texto, idioma),
            icon: const Icon(Icons.volume_up_outlined, color: OL.morado),
          );
    return Semantics(button: true, label: etiqueta ?? 'Escuchar', child: boton);
  }
}

/// Un ejercicio de la ruta: muestra el formato, corrige y da feedback.
class ItemView extends StatefulWidget {
  const ItemView({
    super.key,
    required this.item,
    required this.idioma,
    required this.cadena,
    required this.guiada,
    required this.permitirReintento,
    required this.onComprobado,
    required this.onContinuar,
    this.lumo = true,
  });

  /// Lumo acompaña (escucha, pista, panel). La prueba de nivel lo desactiva.
  final bool lumo;
  final Item item;
  final String idioma;
  final List<String> cadena;

  /// Práctica guiada: muestra la pista.
  final bool guiada;

  /// Permite volver a intentar tras un error (no en evaluación).
  final bool permitirReintento;
  final void Function(bool correcta, String respuesta) onComprobado;
  final VoidCallback onContinuar;
  @override
  State<ItemView> createState() => _ItemViewState();
}

class _ItemViewState extends State<ItemView> {
  int? elegido;
  final orden = <int>[];
  final escrito = TextEditingController();
  late final List<TextEditingController> escritosPartes = [
    for (var i = 0; i < widget.item.textosPartes.length; i++)
      TextEditingController(),
  ];
  String? opcionCompletar;
  bool? correcta;
  bool verPista = false;
  // relacionar
  int? izquierda;
  final emparejados = <int>{};
  int errores = 0;
  late final List<int> derecha = List.generate(
    widget.item.pares.length,
    (i) => i,
  )..shuffle();

  /// Las opciones se muestran barajadas para que la correcta no tenga una
  /// posición fija; la corrección usa siempre el índice original.
  late final List<int> ordenOpciones = List.generate(
    widget.item.opciones.length,
    (i) => i,
  )..shuffle();

  /// Las fichas de «ordenar» llegan en el orden de la respuesta: se muestran
  /// desordenadas (siempre igual para el mismo ítem) y nunca en el orden
  /// correcto, para que no baste tocarlas de izquierda a derecha.
  late final List<int> ordenFichas = _desordenar(widget.item);

  static List<int> _desordenar(Item item) {
    final n = item.tokens.length;
    final indices = List.generate(n, (i) => i)
      ..shuffle(
        Random(
          item.id.codeUnits.fold<int>(7, (h, c) => (h * 31 + c) & 0x3fffffff),
        ),
      );
    String texto(List<int> orden) =>
        [for (final i in orden) item.tokens[i]].join(' ');
    final correcto = item.tokens.join(' ');
    for (
      var giro = 0;
      giro < n && n > 1 && texto(indices) == correcto;
      giro++
    ) {
      indices.add(indices.removeAt(0));
    }
    return indices;
  }

  Item get item => widget.item;
  String t(TextoApoyo? texto) => texto?.en(widget.cadena) ?? '';

  @override
  void dispose() {
    escrito.dispose();
    for (final controller in escritosPartes) {
      controller.dispose();
    }
    super.dispose();
  }

  void reiniciar() => setState(() {
    elegido = null;
    orden.clear();
    escrito.clear();
    for (final controller in escritosPartes) {
      controller.clear();
    }
    opcionCompletar = null;
    correcta = null;
    izquierda = null;
    emparejados.clear();
    errores = 0;
  });

  String get respuestaActual => switch (item.formato) {
    FormatoItem.elegir || FormatoItem.escuchar => '${elegido ?? ''}',
    FormatoItem.ordenar => [for (final i in orden) item.tokens[i]].join(' '),
    FormatoItem.completar =>
      esCompletarMultipartes
          ? escritosPartes.map((controller) => controller.text).join(' | ')
          : item.opciones.isNotEmpty
          ? (opcionCompletar ?? '')
          : escrito.text,
    FormatoItem.escribir => escrito.text,
    FormatoItem.relacionar => relacionAprobada ? 'ok' : 'errores:$errores',
  };

  bool get esCompletarMultipartes =>
      item.textosPartes.isNotEmpty &&
      item.textosPartes.length == item.respuestasPartes.length;

  bool get completarMultipartesAprobado {
    if (!esCompletarMultipartes) return false;
    final partesCorrectas = <bool>[];
    for (var i = 0; i < escritosPartes.length; i++) {
      partesCorrectas.add(
        item.respuestasPartes[i].any(
          (respuesta) =>
              mismaRespuesta(escritosPartes[i].text, respuesta, widget.idioma),
        ),
      );
    }
    final partes = item.partesPuntuables ?? item.respuestasPartes.length;
    final minimo = item.minimoCorrectas ?? partes;
    final obligatoriasCorrectas = item.partesObligatorias.every(
      (index) =>
          index >= 0 &&
          index < partesCorrectas.length &&
          partesCorrectas[index],
    );
    return partesCorrectas.where((correcta) => correcta).length >= minimo &&
        obligatoriasCorrectas;
  }

  bool get relacionAprobada {
    final partes = item.partesPuntuables ?? item.pares.length;
    final minimo = item.minimoCorrectas ?? partes;
    final erroresPermitidos = (partes - minimo).clamp(0, partes);
    return errores <= erroresPermitidos;
  }

  bool get listo => switch (item.formato) {
    FormatoItem.elegir || FormatoItem.escuchar => elegido != null,
    FormatoItem.ordenar => orden.length == item.tokens.length,
    FormatoItem.completar =>
      esCompletarMultipartes
          ? escritosPartes.every(
              (controller) => controller.text.trim().isNotEmpty,
            )
          : item.opciones.isNotEmpty
          ? opcionCompletar != null
          : escrito.text.trim().isNotEmpty,
    FormatoItem.escribir =>
      item.abierta
          ? produccionAbiertaCompleta(item, escrito.text)
          : escrito.text.trim().isNotEmpty,
    FormatoItem.relacionar => emparejados.length == item.pares.length,
  };

  void comprobar() {
    if (correcta != null || !listo) return;
    final respuesta = respuestaActual;
    final ok = esCompletarMultipartes
        ? completarMultipartesAprobado
        : corregir(item, switch (item.formato) {
            FormatoItem.elegir || FormatoItem.escuchar => elegido,
            FormatoItem.relacionar => relacionAprobada,
            _ => respuesta,
          }, widget.idioma);
    setState(() {
      correcta = ok;
      panelAbierto = !item.abierta;
    });
    unawaited(VozNube.instancia.parar().catchError((_) {}));
    ok ? Efectos.correcto() : Efectos.incorrecto();
    widget.onComprobado(ok, respuesta);
    if (!item.abierta) {
      WidgetsBinding.instance.addPostFrameCallback((_) => abrirPanel(ok));
    }
  }

  /// Explicación del resultado (se muestra en el panel inferior).
  Widget cuerpoFeedback(bool ok) {
    final item = widget.item;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (ok && soloFallanTildes(item, respuestaActual, widget.idioma))
          Padding(
            padding: const EdgeInsets.only(bottom: 6),
            child: Text(
              'Ojo con las tildes: ${item.respuesta}',
              style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800),
            ),
          ),
        if (!ok && respuestaCorrectaTexto() != null)
          Padding(
            padding: const EdgeInsets.only(bottom: 6),
            child: Text(
              'Respuesta: ${respuestaCorrectaTexto()}',
              style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800),
            ),
          ),
        Text(
          t(item.feedback),
          style: const TextStyle(fontSize: 17, height: 1.4),
        ),
      ],
    );
  }

  bool panelAbierto = false;

  Future<void> abrirPanel(bool ok) async {
    if (!mounted) return;
    final r = await mostrarPanelResultado(
      context,
      correcto: ok,
      titulo: ok ? '¡Correcto!' : 'Vamos a repasarlo',
      cuerpo: cuerpoFeedback(ok),
      reintentar: !ok && widget.permitirReintento,
      lumo: widget.lumo,
    );
    if (!mounted) return;
    setState(() => panelAbierto = false);
    if (r == 'reintentar') {
      reiniciar();
    } else {
      widget.onContinuar();
    }
  }

  void tocarDerecha(int d) {
    final i = izquierda;
    if (i == null || correcta != null) return;
    if (d == i) {
      setState(() {
        emparejados.add(i);
        izquierda = null;
      });
      if (emparejados.length == item.pares.length) comprobar();
    } else {
      setState(() {
        errores++;
        izquierda = null;
      });
      Efectos.incorrecto();
    }
  }

  String textoOpcion(Opcion o) => o.meta ?? t(o.apoyo);

  Widget opcionBoton(
    String texto,
    bool seleccionada,
    VoidCallback? onTap, {
    bool? acierto,
    bool compacta = false,
  }) => OpcionRespuesta(
    texto: texto,
    compacta: compacta,
    estado: acierto == true
        ? EstadoOpcion.correcta
        : acierto == false
        ? EstadoOpcion.incorrecta
        : seleccionada
        ? EstadoOpcion.seleccionada
        : EstadoOpcion.normal,
    onTap: onTap == null
        ? null
        : () {
            Efectos.toque();
            onTap();
          },
  );

  Widget campoTexto() => TextField(
    controller: escrito,
    enabled: correcta == null,
    autocorrect: false,
    enableSuggestions: false,
    textCapitalization: TextCapitalization.none,
    style: const TextStyle(fontSize: 20),
    minLines: item.abierta ? 4 : 1,
    maxLines: item.abierta ? 8 : 1,
    decoration: const InputDecoration(
      hintText: 'Escribe tu respuesta',
      border: OutlineInputBorder(),
    ),
    onChanged: (_) => setState(() {}),
    onSubmitted: (_) => comprobar(),
  );

  /// Audio del enunciado para formatos que no son de opción (ordenar o
  /// completar lo que se escucha).
  List<Widget> audioEnunciado() => [
    if (item.audio != null)
      Padding(
        padding: const EdgeInsets.only(bottom: 16),
        child: BotonAudio(
          texto: item.audio!,
          idioma: widget.idioma,
          etiqueta: 'Escuchar el audio',
          grande: true,
        ),
      ),
  ];

  List<Widget> cuerpo() {
    final bloqueado = correcta != null;
    switch (item.formato) {
      case FormatoItem.elegir:
      case FormatoItem.escuchar:
        return [
          if (item.audio != null)
            Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: Row(
                children: [
                  // Lumo escucha contigo en los ejercicios de audio.
                  // Solo antes de responder: con el panel abierto ya hay otro Lumo.
                  if (widget.lumo &&
                      item.formato == FormatoItem.escuchar &&
                      correcta == null) ...[
                    const LumoReaccion(pose: PoseLumo.escucha, size: 64),
                    const SizedBox(width: 8),
                  ],
                  Expanded(
                    child: BotonAudio(
                      texto: item.audio!,
                      idioma: widget.idioma,
                      etiqueta: 'Escuchar el audio',
                      grande: true,
                    ),
                  ),
                ],
              ),
            ),
          if (item.audio == null && item.texto?.trim().isNotEmpty == true)
            Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: Tarjeta(
                color: OL.moradoSuave,
                sombra: false,
                child: Text(
                  item.texto!,
                  style: const TextStyle(fontSize: 17, height: 1.4),
                ),
              ),
            ),
          if (item.pregunta != null)
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Tarjeta(
                sombra: false,
                padding: const EdgeInsets.fromLTRB(16, 12, 8, 12),
                onTap: () =>
                    escucharTexto(context, item.pregunta!, widget.idioma),
                etiquetaSemantica: 'Escuchar ${item.pregunta!}',
                child: Row(
                  children: [
                    Expanded(
                      child: Text(
                        item.pregunta!,
                        style: const TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),
                    const Padding(
                      padding: EdgeInsets.all(8),
                      child: Icon(Icons.volume_up_outlined, color: OL.morado),
                    ),
                  ],
                ),
              ),
            ),
          if (item.preguntaApoyo != null)
            Padding(
              padding: const EdgeInsets.only(bottom: 14),
              child: Text(
                t(item.preguntaApoyo),
                style: const TextStyle(fontSize: 19, height: 1.4),
              ),
            ),
          for (final i in ordenOpciones)
            opcionBoton(
              textoOpcion(item.opciones[i]),
              elegido == i,
              bloqueado ? null : () => setState(() => elegido = i),
              acierto: bloqueado && (i == item.indiceRespuesta || i == elegido)
                  ? i == item.indiceRespuesta
                  : null,
            ),
        ];
      case FormatoItem.ordenar:
        return [
          ...audioEnunciado(),
          Container(
            constraints: const BoxConstraints(minHeight: 64),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: OL.moradoSuave,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: OL.moradoClaro),
            ),
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                if (orden.isEmpty)
                  const Text(
                    'Toca las palabras en orden',
                    style: TextStyle(color: OL.gris, fontSize: 16),
                  ),
                for (final i in orden)
                  opcionBoton(
                    item.tokens[i],
                    true,
                    bloqueado ? null : () => setState(() => orden.remove(i)),
                    acierto: bloqueado ? correcta : null,
                    compacta: true,
                  ),
              ],
            ),
          ),
          const SizedBox(height: 14),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              for (final i in ordenFichas)
                if (!orden.contains(i))
                  opcionBoton(
                    item.tokens[i],
                    false,
                    bloqueado ? null : () => setState(() => orden.add(i)),
                    compacta: true,
                  ),
            ],
          ),
        ];
      case FormatoItem.completar:
        if (esCompletarMultipartes) {
          return [
            ...audioEnunciado(),
            if (item.texto?.trim().isNotEmpty == true)
              Padding(
                padding: const EdgeInsets.only(bottom: 16),
                child: Tarjeta(
                  color: OL.moradoSuave,
                  sombra: false,
                  child: Text(
                    item.texto!,
                    style: const TextStyle(fontSize: 17, height: 1.4),
                  ),
                ),
              ),
            for (var i = 0; i < item.textosPartes.length; i++) ...[
              Text(
                '${i + 1}. ${item.textosPartes[i]}',
                style: const TextStyle(
                  fontSize: 19,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 8),
              TextField(
                controller: escritosPartes[i],
                enabled: !bloqueado,
                autocorrect: false,
                enableSuggestions: false,
                textCapitalization: TextCapitalization.none,
                decoration: InputDecoration(
                  hintText: 'Respuesta ${i + 1}',
                  border: const OutlineInputBorder(),
                ),
                onChanged: (_) => setState(() {}),
                onSubmitted: (_) {
                  if (listo) comprobar();
                },
              ),
              const SizedBox(height: 16),
            ],
          ];
        }
        // «Lee y completa»: el texto de lectura va en una tarjeta y la frase
        // con el hueco debajo, separados por una línea en blanco.
        final textoCompleto = item.texto ?? '';
        final corte = textoCompleto.lastIndexOf('\n\n');
        final lectura = corte < 0 ? null : textoCompleto.substring(0, corte);
        final frase = corte < 0
            ? textoCompleto
            : textoCompleto.substring(corte + 2);
        return [
          ...audioEnunciado(),
          if (lectura != null)
            Padding(
              padding: const EdgeInsets.only(bottom: 14),
              child: Tarjeta(
                color: OL.moradoSuave,
                sombra: false,
                child: Text(
                  lectura,
                  style: const TextStyle(fontSize: 17, height: 1.4),
                ),
              ),
            ),
          Text(
            frase.replaceAll(
              '___',
              opcionCompletar ?? (escrito.text.isEmpty ? '____' : escrito.text),
            ),
            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 16),
          if (item.opciones.isNotEmpty)
            for (final o in [for (final i in ordenOpciones) item.opciones[i]])
              opcionBoton(
                textoOpcion(o),
                opcionCompletar == textoOpcion(o),
                bloqueado
                    ? null
                    : () => setState(() => opcionCompletar = textoOpcion(o)),
              )
          else
            campoTexto(),
        ];
      case FormatoItem.escribir:
        return [
          if (item.audio == null && item.texto?.trim().isNotEmpty == true)
            Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: Tarjeta(
                color: OL.moradoSuave,
                sombra: false,
                child: Text(
                  item.texto!,
                  style: const TextStyle(fontSize: 17, height: 1.4),
                ),
              ),
            ),
          if (item.audio != null)
            Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: BotonAudio(
                texto: item.audio!,
                idioma: widget.idioma,
                etiqueta: 'Escuchar y escribir',
                grande: true,
              ),
            ),
          campoTexto(),
          if (item.abierta)
            Padding(
              padding: const EdgeInsets.only(top: 8),
              child: Text(
                '${contarPalabras(escrito.text)} palabras · se piden '
                '${item.maximoPalabras == null ? 'al menos ${item.minimoPalabras ?? 1}' : 'entre ${item.minimoPalabras ?? 1} y ${item.maximoPalabras}'}',
                style: const TextStyle(color: OL.gris, fontSize: 15),
              ),
            ),
        ];
      case FormatoItem.relacionar:
        return [
          if (item.texto?.trim().isNotEmpty == true)
            Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: Tarjeta(
                color: OL.moradoSuave,
                sombra: false,
                child: Text(
                  item.texto!,
                  style: const TextStyle(fontSize: 17, height: 1.4),
                ),
              ),
            ),
          if (errores > 0 && !bloqueado)
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Text(
                'Esa pareja no coincide. Prueba con otra.',
                style: const TextStyle(
                  color: OL.rojo,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Column(
                  children: [
                    for (var i = 0; i < item.pares.length; i++)
                      opcionBoton(
                        item.pares[i].$1,
                        izquierda == i,
                        emparejados.contains(i) || bloqueado
                            ? null
                            : () => setState(() => izquierda = i),
                        acierto: emparejados.contains(i) ? true : null,
                      ),
                  ],
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  children: [
                    for (final d in derecha)
                      opcionBoton(
                        t(item.pares[d].$2),
                        false,
                        emparejados.contains(d) || bloqueado
                            ? null
                            : () => tocarDerecha(d),
                        acierto: emparejados.contains(d) ? true : null,
                      ),
                  ],
                ),
              ),
            ],
          ),
        ];
    }
  }

  String? respuestaCorrectaTexto() => switch (item.formato) {
    FormatoItem.elegir || FormatoItem.escuchar =>
      item.indiceRespuesta == null
          ? null
          : textoOpcion(item.opciones[item.indiceRespuesta!]),
    FormatoItem.relacionar => null,
    _ => item.respuesta,
  };

  @override
  Widget build(BuildContext context) {
    final ok = correcta;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          t(item.consigna),
          style: const TextStyle(fontSize: 21, fontWeight: FontWeight.w800),
        ),
        if (item.imagen != null) ...[
          const SizedBox(height: 14),
          Semantics(
            image: true,
            label: item.imagenAlt,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(18),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxHeight: 280),
                child: Image.asset(
                  item.imagen!,
                  fit: BoxFit.contain,
                  semanticLabel: item.imagenAlt,
                  excludeFromSemantics: true,
                ),
              ),
            ),
          ),
        ],
        const SizedBox(height: 16),
        ...cuerpo(),
        if (widget.guiada && item.pista != null && ok == null) ...[
          Align(
            alignment: Alignment.centerLeft,
            child: TextButton.icon(
              onPressed: () => setState(() => verPista = !verPista),
              icon: const Icon(Icons.lightbulb_outline),
              label: Text(verPista ? 'Ocultar pista' : 'Ver una pista'),
            ),
          ),
          if (verPista)
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (widget.lumo) ...[
                  const LumoReaccion(pose: PoseLumo.pensando, size: 60),
                  const SizedBox(width: 8),
                ],
                Expanded(
                  child: Text(
                    t(item.pista),
                    style: const TextStyle(fontSize: 17, height: 1.4),
                  ),
                ),
              ],
            ),
        ],
        if (ok != null && item.abierta)
          FeedbackDock(
            child: AnswerFeedback(
              correct: true,
              title: '¡Texto listo! Compáralo con el modelo',
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    item.respuesta ?? '',
                    style: const TextStyle(
                      fontSize: 17,
                      height: 1.4,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    t(item.feedback),
                    style: const TextStyle(fontSize: 17, height: 1.4),
                  ),
                ],
              ),
            ),
          ),
        const SizedBox(height: 16),
        if (ok == null && item.formato != FormatoItem.relacionar)
          BotonPrincipal(
            onPressed: listo ? comprobar : null,
            child: const Text('COMPROBAR'),
          ),
        // Tras responder siempre se puede seguir; un fallo en la práctica
        // vuelve al final del bloque (lo gestiona la unidad).
        // Respuesta calificada: el panel inferior lleva SIGUIENTE. Este botón
        // solo aparece en la producción abierta o si el panel se cerró.
        if (ok != null && (item.abierta || !panelAbierto))
          BotonPrincipal(
            color: ok ? OL.verde : OL.rojo,
            onPressed: widget.onContinuar,
            child: const Text('SIGUIENTE'),
          ),
        if (ok == false && widget.permitirReintento && !panelAbierto)
          TextButton.icon(
            onPressed: reiniciar,
            icon: const Icon(Icons.replay_rounded),
            label: const Text('Intentar otra vez ahora'),
          ),
      ],
    );
  }
}
