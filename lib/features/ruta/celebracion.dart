import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/efectos.dart';
import '../../shared/confeti.dart';

/// Estadística de la celebración (valor animado de 0 al final).
class FichaLogro {
  const FichaLogro(
    this.etiqueta,
    this.color,
    this.icono,
    this.valor,
    this.formato, {
    this.animar = true,
  });
  final String etiqueta;
  final Color color;
  final IconData icono;
  final int valor;
  final String Function(int) formato;
  final bool animar;

  static FichaLogro xp(int v) =>
      FichaLogro('XP GANADA', OL.amarillo, Icons.bolt_rounded, v, (x) => '+$x');
  static FichaLogro precision(int v) => FichaLogro(
    'PRECISIÓN',
    OL.verde,
    Icons.track_changes_rounded,
    v,
    (x) => '$x %',
  );
  static FichaLogro tiempo(Duration d) => FichaLogro(
    'TIEMPO',
    OL.azul,
    Icons.timer_outlined,
    0,
    (_) => '${d.inMinutes}:${(d.inSeconds % 60).toString().padLeft(2, '0')}',
    animar: false,
  );
  static FichaLogro racha(int dias) => FichaLogro(
    'RACHA',
    OL.naranja,
    Icons.local_fire_department_rounded,
    dias,
    (x) => '$x',
  );
}

/// Celebración al aprobar una unidad o completar un nivel: mascota, título,
/// y fichas animadas (XP, precisión, tiempo…) al estilo Duolingo.
/// Sin animaciones si el sistema o la app las desactivan.
class CelebracionUnidad extends StatefulWidget {
  const CelebracionUnidad({
    super.key,
    required this.titulo,
    required this.subtitulo,
    required this.fichas,
    this.nivelCompleto = false,
    this.sonido,
  });
  final String titulo, subtitulo;
  final List<FichaLogro> fichas;
  final bool nivelCompleto;

  /// Sonido que se reproduce una vez al aparecer (p. ej. `Efectos.completado`).
  final VoidCallback? sonido;

  @override
  State<CelebracionUnidad> createState() => _CelebracionUnidadState();
}

class _CelebracionUnidadState extends State<CelebracionUnidad> {
  String get titulo => widget.titulo;
  String get subtitulo => widget.subtitulo;
  List<FichaLogro> get fichas => widget.fichas;
  bool get nivelCompleto => widget.nivelCompleto;

  @override
  void initState() {
    super.initState();
    widget.sonido?.call();
  }

  @override
  Widget build(BuildContext context) {
    final animar =
        Efectos.animaciones.value && !MediaQuery.disableAnimationsOf(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        SizedBox(
          height: 190,
          child: Stack(
            alignment: Alignment.center,
            children: [
              if (animar)
                Positioned.fill(
                  child: Confeti(
                    particulas: nivelCompleto ? 170 : 110,
                    conSonido: false,
                  ),
                ),
              _Rebote(
                animar: animar,
                child: Container(
                  width: 150,
                  height: 150,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: nivelCompleto ? OL.amarilloSuave : OL.moradoSuave,
                    border: Border.all(
                      color: nivelCompleto ? OL.amarillo : OL.moradoClaro,
                      width: 4,
                    ),
                  ),
                  padding: const EdgeInsets.all(14),
                  child: Image.asset(
                    'assets/img/mascotas/lumo-sorprendido-alpha.webp',
                    semanticLabel: 'Lumo celebra contigo',
                  ),
                ),
              ),
              if (nivelCompleto)
                const Positioned(
                  top: 6,
                  right: 40,
                  child: Icon(
                    Icons.emoji_events_rounded,
                    color: OL.amarillo,
                    size: 52,
                  ),
                ),
            ],
          ),
        ),
        const SizedBox(height: 8),
        _Rebote(
          animar: animar,
          retraso: .15,
          child: Text(
            titulo,
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 30,
              fontWeight: FontWeight.w900,
              color: nivelCompleto ? OL.naranja : OL.morado,
            ),
          ),
        ),
        const SizedBox(height: 6),
        Text(
          subtitulo,
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 17, color: OL.gris, height: 1.4),
        ),
        const SizedBox(height: 20),
        Row(
          children: [
            for (var i = 0; i < fichas.length; i++) ...[
              if (i > 0) const SizedBox(width: 10),
              Expanded(
                child: _Ficha(ficha: fichas[i], animar: animar && fichas[i].animar),
              ),
            ],
          ],
        ),
      ],
    );
  }
}

/// Entrada con rebote elástico.
class _Rebote extends StatelessWidget {
  const _Rebote({required this.animar, required this.child, this.retraso = 0});
  final bool animar;
  final double retraso;
  final Widget child;
  @override
  Widget build(BuildContext context) {
    if (!animar) return child;
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0, end: 1),
      duration: const Duration(milliseconds: 900),
      curve: Interval(retraso, 1, curve: Curves.elasticOut),
      builder: (_, v, c) => Transform.scale(scale: v.clamp(0, 1.3), child: c),
      child: child,
    );
  }
}

/// Ficha de estadística con contador animado (estilo Duolingo).
class _Ficha extends StatelessWidget {
  const _Ficha({required this.ficha, required this.animar});
  final FichaLogro ficha;
  final bool animar;
  String get etiqueta => ficha.etiqueta;
  Color get color => ficha.color;
  IconData get icono => ficha.icono;
  int get valor => ficha.valor;
  String Function(int) get formato => ficha.formato;

  @override
  Widget build(BuildContext context) => Container(
    decoration: BoxDecoration(
      color: color,
      borderRadius: BorderRadius.circular(16),
    ),
    padding: const EdgeInsets.all(2.5),
    child: Column(
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 5),
          child: Text(
            etiqueta,
            style: const TextStyle(
              color: OL.blanco,
              fontSize: 12,
              fontWeight: FontWeight.w900,
              letterSpacing: .5,
            ),
          ),
        ),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: OL.blanco,
            borderRadius: BorderRadius.circular(13),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icono, color: color, size: 22),
              const SizedBox(width: 4),
              Flexible(
                child: animar
                    ? TweenAnimationBuilder<int>(
                        tween: IntTween(begin: 0, end: valor),
                        duration: const Duration(milliseconds: 1100),
                        curve: Curves.easeOutCubic,
                        builder: (_, v, _) => _valor(formato(v)),
                      )
                    : _valor(formato(valor)),
              ),
            ],
          ),
        ),
      ],
    ),
  );

  Widget _valor(String texto) => FittedBox(
    fit: BoxFit.scaleDown,
    child: Text(
      texto,
      style: TextStyle(
        fontSize: 20,
        fontWeight: FontWeight.w900,
        color: Color.lerp(color, OL.texto, .35),
      ),
    ),
  );
}
