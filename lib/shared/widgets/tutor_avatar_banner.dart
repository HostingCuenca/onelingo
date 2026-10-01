import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import 'widgets.dart';

/// Entrada compacta al tutor con IA usando los retratos reales del roster 3D.
class TutorAvatarBanner extends StatelessWidget {
  const TutorAvatarBanner({super.key});

  static const _faces = [
    ('amara', 12.0, 42.0, 66.0),
    ('lucia', 74.0, 4.0, 60.0),
    ('mei', 82.0, 60.0, 64.0),
    ('malik', 9.0, 96.0, 62.0),
    ('kenji', 72.0, 116.0, 58.0),
  ];

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: 'Practica con nuestros tutores de inteligencia artificial',
    child: Tarjeta(
      onTap: () => context.push('/tutores'),
      padding: EdgeInsets.zero,
      color: OL.moradoSuave,
      borde: OL.moradoClaro,
      child: LayoutBuilder(
        builder: (context, constraints) {
          final compact = constraints.maxWidth < 350;
          final facesWidth = compact ? 146.0 : 174.0;
          final bannerHeight = compact ? 180.0 : 158.0;
          return SizedBox(
            height: bannerHeight,
            child: Stack(
              clipBehavior: Clip.hardEdge,
              children: [
                Positioned(
                  right: -20,
                  top: -44,
                  child: Container(
                    width: 190,
                    height: 190,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: OL.morado.withValues(alpha: .08),
                    ),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(
                    compact ? 14 : 18,
                    16,
                    facesWidth - 4,
                    14,
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Practica con nuestros avatares',
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(
                          fontSize: 18,
                          height: 1.08,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const SizedBox(height: 7),
                      const Text(
                        'Habla con un tutor de IA adaptado a tu idioma y nivel.',
                        maxLines: 3,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(fontSize: 13, height: 1.28),
                      ),
                      const Spacer(),
                      const FittedBox(
                        fit: BoxFit.scaleDown,
                        alignment: Alignment.centerLeft,
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              'ELEGIR TUTOR',
                              style: TextStyle(
                                color: OL.morado,
                                fontSize: 12,
                                fontWeight: FontWeight.w900,
                                letterSpacing: .3,
                              ),
                            ),
                            SizedBox(width: 3),
                            Icon(
                              Icons.arrow_forward_rounded,
                              size: 17,
                              color: OL.morado,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                Positioned(
                  right: compact ? -24 : -4,
                  top: 0,
                  width: facesWidth,
                  height: bannerHeight,
                  child: Stack(
                    children: [
                      for (var i = 0; i < _faces.length; i++)
                        Positioned(
                          top: _faces[i].$2,
                          left: _faces[i].$3,
                          child: _TutorFace(
                            id: _faces[i].$1,
                            size: compact ? _faces[i].$4 - 7 : _faces[i].$4,
                            color: [
                              OL.morado,
                              OL.naranja,
                              OL.verde,
                              OL.azul,
                              OL.rojo,
                            ][i],
                          ),
                        ),
                    ],
                  ),
                ),
              ],
            ),
          );
        },
      ),
    ),
  );
}

class _TutorFace extends StatelessWidget {
  const _TutorFace({required this.id, required this.size, required this.color});
  final String id;
  final double size;
  final Color color;

  @override
  Widget build(BuildContext context) => Container(
    width: size,
    height: size,
    padding: const EdgeInsets.all(3),
    decoration: BoxDecoration(
      color: OL.blanco,
      shape: BoxShape.circle,
      border: Border.all(color: color, width: 2),
      boxShadow: const [
        BoxShadow(
          color: Color(0x260D1330),
          blurRadius: 8,
          offset: Offset(0, 3),
        ),
      ],
    ),
    child: ClipOval(
      child: Image.asset(
        'assets/img/tutores/$id.webp',
        fit: BoxFit.cover,
        alignment: const Alignment(0, -.72),
        excludeFromSemantics: true,
      ),
    ),
  );
}
