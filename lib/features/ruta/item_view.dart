import 'dart:async';

import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/correccion.dart';
import '../../core/aprendizaje/modelos.dart';
import '../../core/efectos.dart';
import '../../core/voz.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../shared/widgets/primary_button.dart';
import 'opcion_respuesta.dart';

/// Reproduce un texto del idioma meta en su idioma: voz de la nube con el
/// idioma forzado y, para sílabas sueltas no latinas o sin sesión, la voz
/// nativa del dispositivo.
Future<void> escucharTexto(
  BuildContext context,
  String texto,
  String idioma,
) => Voz.instancia.hablar(
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
  });
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
  String? opcionCompletar;
  bool? correcta;
  bool verPista = false;
  // relacionar
  int? izquierda;
  final emparejados = <int>{};
  int errores = 0;
  late final List<int> derecha = List.generate(widget.item.pares.length, (i) => i)
    ..shuffle();

  /// Las opciones se muestran barajadas para que la correcta no tenga una
  /// posición fija; la corrección usa siempre el índice original.
  late final List<int> ordenOpciones = List.generate(
    widget.item.opciones.length,
    (i) => i,
  )..shuffle();

  Item get item => widget.item;
  String t(TextoApoyo? texto) => texto?.en(widget.cadena) ?? '';

  @override
  void dispose() {
    escrito.dispose();
    super.dispose();
  }

  void reiniciar() => setState(() {
    elegido = null;
    orden.clear();
    escrito.clear();
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
      item.opciones.isNotEmpty ? (opcionCompletar ?? '') : escrito.text,
    FormatoItem.escribir => escrito.text,
    FormatoItem.relacionar => errores == 0 ? 'ok' : 'errores:$errores',
  };

  bool get listo => switch (item.formato) {
    FormatoItem.elegir || FormatoItem.escuchar => elegido != null,
    FormatoItem.ordenar => orden.length == item.tokens.length,
    FormatoItem.completar =>
      item.opciones.isNotEmpty
          ? opcionCompletar != null
          : escrito.text.trim().isNotEmpty,
    FormatoItem.escribir => escrito.text.trim().isNotEmpty,
    FormatoItem.relacionar => emparejados.length == item.pares.length,
  };

  void comprobar() {
    if (correcta != null || !listo) return;
    final respuesta = respuestaActual;
    final ok = corregir(
      item,
      switch (item.formato) {
        FormatoItem.elegir || FormatoItem.escuchar => elegido,
        FormatoItem.relacionar => errores == 0,
        _ => respuesta,
      },
      widget.idioma,
    );
    setState(() => correcta = ok);
    unawaited(VozNube.instancia.parar().catchError((_) {}));
    ok ? Efectos.correcto() : Efectos.incorrecto();
    widget.onComprobado(ok, respuesta);
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

  Widget opcionBoton(String texto, bool seleccionada, VoidCallback? onTap, {
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
    decoration: const InputDecoration(
      hintText: 'Escribe tu respuesta',
      border: OutlineInputBorder(),
    ),
    onChanged: (_) => setState(() {}),
    onSubmitted: (_) => comprobar(),
  );

  List<Widget> cuerpo() {
    final bloqueado = correcta != null;
    switch (item.formato) {
      case FormatoItem.elegir:
      case FormatoItem.escuchar:
        return [
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
          if (item.pregunta != null)
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
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
                  BotonAudio(texto: item.pregunta!, idioma: widget.idioma),
                ],
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
              for (var i = 0; i < item.tokens.length; i++)
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
        return [
          Text(
            (item.texto ?? '').replaceAll(
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
        ];
      case FormatoItem.relacionar:
        return [
          if (errores > 0 && !bloqueado)
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Text(
                'Esa pareja no coincide. Prueba con otra.',
                style: const TextStyle(color: OL.rojo, fontWeight: FontWeight.w700),
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
            Text(t(item.pista), style: const TextStyle(fontSize: 17, height: 1.4)),
        ],
        if (ok != null)
          FeedbackDock(
            child: AnswerFeedback(
              correct: ok,
              title: ok ? '¡Correcto!' : 'Vamos a repasarlo',
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (ok && soloFallanTildes(item, respuestaActual, widget.idioma))
                    Padding(
                      padding: const EdgeInsets.only(bottom: 6),
                      child: Text(
                        'Ojo con las tildes: ${item.respuesta}',
                        style: const TextStyle(
                          fontSize: 17,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                    ),
                  if (!ok && respuestaCorrectaTexto() != null)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 6),
                      child: Text(
                        'Respuesta: ${respuestaCorrectaTexto()}',
                        style: const TextStyle(
                          fontSize: 17,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                    ),
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
        if (ok == false && widget.permitirReintento)
          BotonPrincipal(
            color: OL.naranja,
            onPressed: reiniciar,
            child: const Text('INTENTAR OTRA VEZ'),
          ),
        // En la práctica guiada se sigue cuando se resuelve (con ayuda).
        if (ok == true || (ok == false && !widget.guiada))
          BotonPrincipal(
            // Verde tras acertar, como el feedback de la respuesta.
            color: ok == true ? OL.verde : OL.morado,
            onPressed: widget.onContinuar,
            child: const Text('CONTINUAR'),
          ),
      ],
    );
  }
}
