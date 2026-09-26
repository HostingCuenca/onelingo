import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/efectos.dart';

enum EstadoOpcion { normal, seleccionada, correcta, incorrecta }

/// Opción de respuesta con pedestal, el mismo lenguaje visual que
/// `BotonPrincipal`. Al acertar hace un «pop»; al fallar, una sacudida suave.
/// Sin animaciones si el sistema o la app las desactivan.
class OpcionRespuesta extends StatefulWidget {
  const OpcionRespuesta({
    super.key,
    required this.texto,
    required this.estado,
    required this.onTap,
    this.compacta = false,
  });
  final String texto;
  final EstadoOpcion estado;
  final VoidCallback? onTap;

  /// Ficha pequeña (ordenar palabras).
  final bool compacta;

  @override
  State<OpcionRespuesta> createState() => _OpcionRespuestaState();
}

class _OpcionRespuestaState extends State<OpcionRespuesta>
    with SingleTickerProviderStateMixin {
  late final AnimationController _anim = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 380),
  );
  bool _presionada = false;

  bool get _animar =>
      Efectos.animaciones.value && !MediaQuery.disableAnimationsOf(context);

  @override
  void didUpdateWidget(OpcionRespuesta anterior) {
    super.didUpdateWidget(anterior);
    final cambio = anterior.estado != widget.estado;
    if (cambio &&
        (widget.estado == EstadoOpcion.correcta ||
            widget.estado == EstadoOpcion.incorrecta) &&
        _animar) {
      _anim.forward(from: 0);
    }
  }

  @override
  void dispose() {
    _anim.dispose();
    super.dispose();
  }

  (Color fondo, Color borde, Color pedestal, Color texto) get _colores =>
      switch (widget.estado) {
        EstadoOpcion.normal => (OL.blanco, OL.grisClaro, OL.grisClaro, OL.texto),
        EstadoOpcion.seleccionada => (
          OL.moradoSuave,
          OL.morado,
          Color.lerp(OL.morado, OL.texto, .25)!,
          OL.morado,
        ),
        EstadoOpcion.correcta => (
          OL.verdeSuave,
          OL.verde,
          Color.lerp(OL.verde, OL.texto, .25)!,
          Color.lerp(OL.verde, OL.texto, .35)!,
        ),
        EstadoOpcion.incorrecta => (
          OL.rojoSuave,
          OL.rojo,
          Color.lerp(OL.rojo, OL.texto, .25)!,
          Color.lerp(OL.rojo, OL.texto, .35)!,
        ),
      };

  @override
  Widget build(BuildContext context) {
    final (fondo, borde, pedestal, colorTexto) = _colores;
    final activa = widget.onTap != null;
    final hundida = _presionada && activa;
    final radio = widget.compacta ? 14.0 : 16.0;
    final tarjeta = AnimatedContainer(
      duration: const Duration(milliseconds: 90),
      margin: EdgeInsets.only(top: hundida ? 3 : 0),
      decoration: BoxDecoration(
        color: pedestal,
        borderRadius: BorderRadius.circular(radio),
      ),
      padding: EdgeInsets.only(bottom: hundida ? 1 : 4),
      child: Container(
        width: widget.compacta ? null : double.infinity,
        padding: widget.compacta
            ? const EdgeInsets.symmetric(horizontal: 14, vertical: 10)
            : const EdgeInsets.symmetric(horizontal: 16, vertical: 15),
        decoration: BoxDecoration(
          color: fondo,
          borderRadius: BorderRadius.circular(radio),
          border: Border.all(color: borde, width: 2),
        ),
        child: Text(
          widget.texto,
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w800,
            color: colorTexto,
          ),
        ),
      ),
    );
    return Padding(
      padding: EdgeInsets.only(bottom: widget.compacta ? 0 : 10),
      child: Semantics(
        button: true,
        selected: widget.estado != EstadoOpcion.normal,
        enabled: activa,
        child: GestureDetector(
          onTapDown: activa ? (_) => setState(() => _presionada = true) : null,
          onTapCancel: () => setState(() => _presionada = false),
          onTapUp: activa ? (_) => setState(() => _presionada = false) : null,
          onTap: widget.onTap,
          child: AnimatedBuilder(
            animation: _anim,
            builder: (context, child) {
              final t = _anim.value;
              if (t == 0 || t == 1) return child!;
              if (widget.estado == EstadoOpcion.correcta) {
                // Pop: crece un poco y vuelve.
                final escala = 1 + .06 * math.sin(t * math.pi);
                return Transform.scale(scale: escala, child: child);
              }
              // Sacudida suave que se amortigua.
              final dx = 7 * math.sin(t * math.pi * 5) * (1 - t);
              return Transform.translate(offset: Offset(dx, 0), child: child);
            },
            child: tarjeta,
          ),
        ),
      ),
    );
  }
}
