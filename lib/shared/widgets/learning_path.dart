import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/biblioteca.dart';
import '../../core/diagnostico.dart';
import 'widgets.dart';
import 'skill_badge.dart';
import 'tarjeta_fundamentos.dart';

/// Stable learning areas: recommendations never remove access to a subject.
class LearningPath extends StatelessWidget {
  const LearningPath({
    super.key,
    required this.nivel,
    required this.recommended,
    required this.practices,
  });
  final int nivel;
  final String recommended;
  final Map<String, dynamic> practices;
  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text(
          'Tu camino de aprendizaje',
          style: TextStyle(fontSize: 23, fontWeight: FontWeight.w900),
        ),
        const SizedBox(height: 6),
        const Text(
          'Aprende → practica → comprueba. Todas las áreas siguen disponibles para volver a ellas.',
          style: TextStyle(color: OL.gris, fontSize: 16, height: 1.4),
        ),
        const SizedBox(height: 16),
        if (nivel <= 2) ...[
          const TarjetaFundamentos(),
          const SizedBox(height: 16),
        ],
        for (var i = 0; i < RutaBiblioteca.habilidades.length; i++) ...[
          if (i > 0)
            SizedBox(
              height: 26,
              child: CustomPaint(painter: _PathLink(i.isEven)),
            ),
          Builder(
            builder: (context) {
              final skill = [
                'vocabulario',
                'gramatica',
                'comprension',
                'listening',
                'escritura',
              ][i];
              final recent = practices.values
                  .whereType<Map>()
                  .where(
                    (e) =>
                        e['skill'] == skill &&
                        (e['idioma'] == null || e['idioma'] == 'en'),
                  )
                  .length;
              final suggested = recommended == skill;
              return Padding(
                padding: EdgeInsets.only(
                  left: i.isEven ? 0 : 22,
                  right: i.isEven ? 22 : 0,
                ),
                child: Semantics(
                  button: true,
                  child: Tarjeta(
                    color: suggested ? OL.moradoSuave : OL.blanco,
                    borde: suggested ? OL.morado : OL.grisClaro,
                    onTap: () => context.push(
                      skill == 'gramatica'
                          ? '/gramatica?nivel=$nivel'
                          : skill == 'escritura'
                          ? '/biblioteca?skill=$skill'
                          : '/estudiar?skill=$skill&nivel=$nivel',
                    ),
                    child: Row(
                      children: [
                        InsigniaHabilidad(skill, size: 52),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                skillsDiag[skill]!,
                                style: const TextStyle(
                                  fontSize: 17,
                                  fontWeight: FontWeight.w900,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                skill == 'gramatica'
                                    ? 'Reglas, ejemplos y pruebas por nivel'
                                    : recent > 0
                                    ? '$recent actividades practicadas · sigue reforzando'
                                    : 'Descubre cómo practicar esta habilidad',
                                style: const TextStyle(
                                  fontSize: 16,
                                  height: 1.35,
                                  color: OL.gris,
                                ),
                              ),
                              if (suggested) ...[
                                const SizedBox(height: 6),
                                const Text(
                                  'RECOMENDADO PARA TI',
                                  style: TextStyle(
                                    fontWeight: FontWeight.w900,
                                    color: OL.morado,
                                    fontSize: 14,
                                    letterSpacing: .6,
                                  ),
                                ),
                              ],
                            ],
                          ),
                        ),
                        const SizedBox(width: 5),
                        const Icon(
                          Icons.chevron_right_rounded,
                          color: OL.morado,
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ],
      ],
    );
  }
}

class _PathLink extends CustomPainter {
  const _PathLink(this.reverse);
  final bool reverse;
  @override
  void paint(Canvas canvas, Size size) {
    final x = size.width * .5;
    final a = reverse ? 11.0 : -11.0;
    canvas.drawPath(
      Path()
        ..moveTo(x + a, 0)
        ..cubicTo(x + a, 14, x - a, 12, x - a, size.height),
      Paint()
        ..color = OL.moradoClaro
        ..strokeWidth = 6
        ..strokeCap = StrokeCap.round
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(_PathLink old) => old.reverse != reverse;
}
