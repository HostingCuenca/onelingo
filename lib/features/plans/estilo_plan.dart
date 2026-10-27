import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';
import '../../core/pagos/modelos.dart';

/// Color e icono de cada plan en la pantalla de planes (según cuántos idiomas
/// o personas incluye, no según su id: el administrador crea planes nuevos).
class EstiloPlan {
  const EstiloPlan(this.color, this.suave, this.icono);
  final Color color;
  final Color suave;
  final IconData icono;

  static const empresa = EstiloPlan(OL.rojo, OL.rojoSuave, Icons.apartment_rounded);

  static EstiloPlan de(PlanServidor p) => p.familiar
      ? const EstiloPlan(OL.naranja, OL.naranjaSuave, Icons.family_restroom_rounded)
      : switch (p.idiomas) {
          1 => const EstiloPlan(OL.azul, OL.azulSuave, Icons.public_rounded),
          2 => const EstiloPlan(OL.verde, OL.verdeSuave, Icons.forum_rounded),
          _ => const EstiloPlan(OL.morado, OL.moradoSuave, Icons.translate_rounded),
        };
}

/// «1 idioma», «3 idiomas», «Todos los idiomas» o «4 usuarios».
String subtituloPlan(PlanServidor p) => p.familiar
    ? tr('{n} usuarios', {'n': p.usuarios})
    : p.todosLosIdiomas
    ? tr('Todos los idiomas')
    : p.idiomas == 1
    ? tr('1 idioma')
    : tr('{n} idiomas', {'n': p.idiomas});

/// Icono del plan en un círculo de su color.
class IconoPlan extends StatelessWidget {
  const IconoPlan(this.estilo, {super.key, this.tamano = 56});
  final EstiloPlan estilo;
  final double tamano;

  @override
  Widget build(BuildContext context) => Container(
    width: tamano,
    height: tamano,
    decoration: BoxDecoration(
      shape: BoxShape.circle,
      gradient: LinearGradient(
        colors: [estilo.color, Color.lerp(estilo.color, OL.blanco, .35)!],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ),
    ),
    child: Icon(estilo.icono, color: OL.blanco, size: tamano * .52),
  );
}
