import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';
import '../../core/voz.dart';

/// Medidor de voz del micrófono: barras que siguen el nivel real mientras
/// el alumno habla y, al cerrar la grabación, el aviso de que se transcribe.
/// Así se ve que la app oye y cuándo terminó de escuchar.
class OndaVoz extends StatelessWidget {
  const OndaVoz({super.key, this.color = OL.morado, this.alto = 40});
  final Color color;
  final double alto;

  // Las barras del centro suben más: parece una onda, no un ecualizador.
  static const _perfil = [.45, .7, .9, 1.0, .9, .7, .45];

  @override
  Widget build(BuildContext context) => ValueListenableBuilder<bool>(
    valueListenable: Oido.instancia.procesando,
    builder: (_, procesando, _) => procesando
        ? SizedBox(
            height: alto,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(
                    strokeWidth: 2.5,
                    color: color,
                  ),
                ),
                const SizedBox(width: 10),
                Flexible(
                  child: Text(
                    tr('Transcribiendo tu respuesta…'),
                    style: TextStyle(color: color, fontWeight: FontWeight.w700),
                  ),
                ),
              ],
            ),
          )
        : ValueListenableBuilder<double>(
            valueListenable: Oido.instancia.nivel,
            builder: (_, nivel, _) => SizedBox(
              height: alto,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  for (final p in _perfil)
                    AnimatedContainer(
                      duration: const Duration(milliseconds: 110),
                      margin: const EdgeInsets.symmetric(horizontal: 2.5),
                      width: 6,
                      height: alto * (.14 + .86 * nivel * p),
                      decoration: BoxDecoration(
                        color: color,
                        borderRadius: BorderRadius.circular(3),
                      ),
                    ),
                ],
              ),
            ),
          ),
  );
}
