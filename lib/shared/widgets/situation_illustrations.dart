import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';

/// Dos ilustraciones contextuales; las fotos originales siguen en las tarjetas.
class SituationIllustrations extends StatefulWidget {
  const SituationIllustrations(this.id, {super.key});
  final int id;
  @override
  State<SituationIllustrations> createState() => _SituationIllustrationsState();
}

/// Escenas rehechas con otro nombre de archivo: la 2 original salió casi igual
/// a la 1. Un parche de Shorebird no lleva assets nuevos, así que en una APK
/// sin el archivo nuevo se muestra solo la escena 1.
const _escenaNueva = {22: 'situacion-22-2b.webp'};
final _hayEscenaNueva = <int, Future<bool>>{};

String _ruta(int id, int i) {
  final n = id.toString().padLeft(2, '0');
  return 'assets/img/situaciones/${i == 1 && _escenaNueva.containsKey(id) ? _escenaNueva[id] : 'situacion-$n-${i + 1}.webp'}';
}

class _SituationIllustrationsState extends State<SituationIllustrations> {
  int selected = 0;
  int escenas = 2;

  @override
  void initState() {
    super.initState();
    if (!_escenaNueva.containsKey(widget.id)) return;
    escenas = 1;
    _hayEscenaNueva
        .putIfAbsent(
          widget.id,
          () => rootBundle
              .load(_ruta(widget.id, 1))
              .then((_) => true, onError: (_) => false),
        )
        .then((hay) {
          if (hay && mounted) setState(() => escenas = 2);
        });
  }

  @override
  Widget build(BuildContext context) => Column(
    children: [
      SizedBox(
        height: 180,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(22),
          child: PageView.builder(
            itemCount: escenas,
            onPageChanged: (v) => setState(() => selected = v),
            itemBuilder: (context, i) => Image.asset(
              _ruta(widget.id, i),
              fit: BoxFit.cover,
              semanticLabel: tr('Ilustración de la situación, escena {n}', {
                'n': i + 1,
              }),
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
      if (escenas > 1) ...[
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
              tr('Escena {n} de 2 · desliza', {'n': selected + 1}),
              style: const TextStyle(color: OL.gris, fontSize: 11),
            ),
          ],
        ),
      ],
    ],
  );
}
