import 'package:flutter/material.dart';

import '../../app/theme.dart';

/// Dos ilustraciones contextuales; las fotos originales siguen en las tarjetas.
class SituationIllustrations extends StatefulWidget {
  const SituationIllustrations(this.id, {super.key});
  final int id;
  @override
  State<SituationIllustrations> createState() => _SituationIllustrationsState();
}

class _SituationIllustrationsState extends State<SituationIllustrations> {
  int selected = 0;
  @override
  Widget build(BuildContext context) => Column(
    children: [
      SizedBox(
        height: 180,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(22),
          child: PageView.builder(
            itemCount: 2,
            onPageChanged: (v) => setState(() => selected = v),
            itemBuilder: (context, i) => Image.asset(
              'assets/img/situaciones/situacion-${widget.id.toString().padLeft(2, '0')}-${i + 1}.webp',
              fit: BoxFit.cover,
              semanticLabel: 'Ilustración de la situación, escena ${i + 1}',
              errorBuilder: (context, error, stack) => const ColoredBox(
                color: OL.moradoSuave,
                child: Center(
                  child: Icon(
                    Icons.auto_stories_rounded,
                    size: 48,
                    color: OL.morado,
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
      const SizedBox(height: 8),
      Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          for (var i = 0; i < 2; i++)
            AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              width: selected == i ? 22 : 7,
              height: 7,
              margin: const EdgeInsets.symmetric(horizontal: 3),
              decoration: BoxDecoration(
                color: selected == i ? OL.morado : OL.moradoClaro,
                borderRadius: BorderRadius.circular(8),
              ),
            ),
          const SizedBox(width: 8),
          Text(
            'Escena ${selected + 1} de 2 · desliza',
            style: const TextStyle(color: OL.gris, fontSize: 11),
          ),
        ],
      ),
    ],
  );
}
