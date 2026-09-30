import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../app/theme.dart';
export 'language_flag.dart';
export 'primary_button.dart';
import '../../core/models/models.dart';

class Tarjeta extends StatefulWidget {
  const Tarjeta({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(16),
    this.color = OL.blanco,
    this.borde,
    this.onTap,
    this.radio = 22,
    this.sombra = true,
    this.etiquetaSemantica,
  });
  final Widget child;
  final EdgeInsets padding;
  final Color color;
  final Color? borde;
  final VoidCallback? onTap;
  final double radio;
  final bool sombra;
  final String? etiquetaSemantica;

  @override
  State<Tarjeta> createState() => _TarjetaState();
}

class _TarjetaState extends State<Tarjeta> {
  bool presionada = false;

  @override
  Widget build(BuildContext context) {
    final interactiva = widget.onTap != null;
    final reducirMovimiento = MediaQuery.disableAnimationsOf(context);
    final colorPresionado = Color.alphaBlend(
      OL.morado.withValues(alpha: 0.09),
      widget.color,
    );
    final box = AnimatedContainer(
      duration: reducirMovimiento
          ? Duration.zero
          : const Duration(milliseconds: 90),
      curve: Curves.easeOut,
      padding: widget.padding,
      decoration: BoxDecoration(
        color: presionada ? colorPresionado : widget.color,
        borderRadius: BorderRadius.circular(widget.radio),
        border: Border.all(
          color: presionada ? OL.morado : widget.borde ?? OL.grisClaro,
          width: presionada ? 3 : 2,
        ),
        boxShadow: widget.sombra
            ? [
                BoxShadow(
                  color: presionada
                      ? OL.morado.withValues(alpha: 0.38)
                      : widget.borde ?? OL.grisClaro,
                  offset: Offset(0, presionada ? 1 : 4),
                ),
              ]
            : null,
      ),
      child: widget.child,
    );
    if (!interactiva) return box;
    return Semantics(
      button: true,
      label: widget.etiquetaSemantica,
      child: AnimatedScale(
        scale: presionada ? 0.98 : 1,
        duration: reducirMovimiento
            ? Duration.zero
            : const Duration(milliseconds: 90),
        curve: Curves.easeOut,
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            borderRadius: BorderRadius.circular(widget.radio),
            onHighlightChanged: (value) {
              if (presionada != value) setState(() => presionada = value);
            },
            onTap: widget.onTap,
            child: box,
          ),
        ),
      ),
    );
  }
}

class HeroCard extends StatelessWidget {
  const HeroCard({
    super.key,
    required this.child,
    this.gradient = OL.gradienteMorado,
  });
  final Widget child;
  final Gradient gradient;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(22),
    decoration: BoxDecoration(
      gradient: gradient,
      borderRadius: BorderRadius.circular(20),
      boxShadow: OL.sombra(0.18),
    ),
    child: child,
  );
}

class Etiqueta extends StatelessWidget {
  const Etiqueta(
    this.texto, {
    super.key,
    this.color = OL.morado,
    this.fondo,
    this.icono,
  });
  final String texto;
  final Color color;
  final Color? fondo;
  final IconData? icono;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
    decoration: BoxDecoration(
      color: fondo ?? color.withValues(alpha: 0.12),
      borderRadius: BorderRadius.circular(99),
    ),
    child: Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (icono != null) ...[
          Icon(icono, size: 14, color: color),
          const SizedBox(width: 5),
        ],
        Text(
          texto,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w700,
            color: color,
          ),
        ),
      ],
    ),
  );
}

class BarraProgreso extends StatelessWidget {
  const BarraProgreso(
    this.valor, {
    super.key,
    this.color = OL.morado,
    this.fondo = OL.grisClaro,
    this.alto = 12,
  });
  final double valor;
  final Color color;
  final Color fondo;
  final double alto;

  @override
  Widget build(BuildContext context) => ClipRRect(
    borderRadius: BorderRadius.circular(99),
    child: TweenAnimationBuilder<double>(
      tween: Tween(end: valor.clamp(0, 1)),
      duration: MediaQuery.disableAnimationsOf(context)
          ? Duration.zero
          : const Duration(milliseconds: 320),
      curve: Curves.easeOutCubic,
      builder: (_, value, _) => LinearProgressIndicator(
        value: value,
        minHeight: alto,
        backgroundColor: fondo,
        valueColor: AlwaysStoppedAnimation(color),
      ),
    ),
  );
}

class AnilloProgreso extends StatelessWidget {
  const AnilloProgreso({
    super.key,
    required this.valor,
    this.tamano = 72,
    this.grosor = 8,
    this.color = OL.morado,
    this.fondo = OL.grisClaro,
    this.child,
  });
  final double valor;
  final double tamano;
  final double grosor;
  final Color color;
  final Color fondo;
  final Widget? child;

  @override
  Widget build(BuildContext context) => SizedBox(
    width: tamano,
    height: tamano,
    child: CustomPaint(
      painter: _AnilloPainter(valor.clamp(0, 1), grosor, color, fondo),
      child: Center(child: child),
    ),
  );
}

class _AnilloPainter extends CustomPainter {
  _AnilloPainter(this.valor, this.grosor, this.color, this.fondo);
  final double valor, grosor;
  final Color color, fondo;

  @override
  void paint(Canvas canvas, Size size) {
    final rect = Offset.zero & size;
    final r = rect.deflate(grosor / 2);
    final base = Paint()
      ..color = fondo
      ..style = PaintingStyle.stroke
      ..strokeWidth = grosor;
    final fg = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = grosor
      ..strokeCap = StrokeCap.round;
    canvas.drawArc(r, 0, math.pi * 2, false, base);
    canvas.drawArc(r, -math.pi / 2, math.pi * 2 * valor, false, fg);
  }

  @override
  bool shouldRepaint(_AnilloPainter old) =>
      old.valor != valor || old.color != color || old.grosor != grosor;
}

class IconoCuadro extends StatelessWidget {
  const IconoCuadro(
    this.icono, {
    super.key,
    this.color = OL.morado,
    this.tamano = 44,
    this.radio = 12,
    this.relleno = false,
  });
  final IconData icono;
  final Color color;
  final double tamano;
  final double radio;
  final bool relleno;

  @override
  Widget build(BuildContext context) => Container(
    width: tamano,
    height: tamano,
    decoration: BoxDecoration(
      color: relleno ? color : color.withValues(alpha: 0.12),
      borderRadius: BorderRadius.circular(radio),
    ),
    child: Icon(icono, color: relleno ? OL.blanco : color, size: tamano * 0.5),
  );
}

class TituloSeccion extends StatelessWidget {
  const TituloSeccion(this.texto, {super.key, this.accion, this.onAccion});
  final String texto;
  final String? accion;
  final VoidCallback? onAccion;

  @override
  Widget build(BuildContext context) => Row(
    mainAxisAlignment: MainAxisAlignment.spaceBetween,
    children: [
      Expanded(
        child: Text(texto, style: Theme.of(context).textTheme.headlineSmall),
      ),
      if (accion != null) TextButton(onPressed: onAccion, child: Text(accion!)),
    ],
  );
}

class EstadoLeccionIcono extends StatelessWidget {
  const EstadoLeccionIcono(
    this.estado, {
    super.key,
    required this.numero,
    this.color = OL.morado,
  });
  final LessonState estado;
  final int numero;
  final Color color;

  @override
  Widget build(BuildContext context) {
    final (bg, fg, child) = switch (estado) {
      LessonState.completada => (
        OL.verdeSuave,
        OL.verde,
        const Icon(Icons.check, size: 18),
      ),
      LessonState.actual => (color, OL.blanco, Text('$numero')),
      LessonState.bloqueada => (
        OL.grisClaro,
        OL.gris,
        const Icon(Icons.lock_outline, size: 16),
      ),
    };
    return Container(
      width: 36,
      height: 36,
      decoration: BoxDecoration(color: bg, shape: BoxShape.circle),
      alignment: Alignment.center,
      child: DefaultTextStyle(
        style: TextStyle(color: fg, fontWeight: FontWeight.w700, fontSize: 14),
        child: IconTheme(
          data: IconThemeData(color: fg),
          child: child,
        ),
      ),
    );
  }
}

class Logo extends StatelessWidget {
  const Logo({super.key, this.tamano = 120});
  final double tamano;

  @override
  Widget build(BuildContext context) => Image.asset(
    'assets/img/logo.png',
    width: tamano,
    height: tamano,
    fit: BoxFit.contain,
  );
}

/// Contenedor centrado con ancho máximo para que la demo web no se estire.
class Movil extends StatelessWidget {
  const Movil({super.key, required this.child});
  final Widget child;

  @override
  Widget build(BuildContext context) => Center(
    child: ConstrainedBox(
      constraints: const BoxConstraints(maxWidth: 480),
      child: child,
    ),
  );
}
