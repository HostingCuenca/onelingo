import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/curriculum.dart';
import '../../core/i18n/i18n.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../core/efectos.dart';
import '../ruta/celebracion.dart';
import '../../shared/widgets/widgets.dart';

class LessonResultScreen extends ConsumerWidget {
  const LessonResultScreen({
    super.key,
    required this.lessonId,
    required this.aciertos,
    required this.total,
  });
  final String lessonId;
  final int aciertos;
  final int total;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l = leccionPorId(lessonId);
    final s = ref.watch(progressProvider);
    final pct = total == 0 ? 100 : (aciertos * 100 / total).round();
    final siguiente = l == null ? null : s.leccionActual(l.nivel);
    final nivelCompleto = l != null && s.examenDesbloqueado(l.nivel);

    return Scaffold(
      body: Stack(
        children: [
          Movil(
            child: SafeArea(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  children: [
                    const Spacer(),
                    // Recompensa al terminar (misma celebración que la ruta).
                    CelebracionUnidad(
                      nivelCompleto: nivelCompleto,
                      sonido: pct < 60
                          ? null
                          : nivelCompleto
                          ? Efectos.nivel
                          : Efectos.completado,
                      titulo: pct == 100
                          ? tr('¡Perfecto, {nombre}!', {'nombre': s.nombre.split(' ').first})
                          : tr('¡Lección completada!'),
                      subtitulo:
                          '${l?.titulo ?? ''}\n${tr('Práctica completada. El dominio se confirma con ejercicios nuevos y repaso.')}',
                      fichas: [
                        FichaLogro(
                          tr('ACIERTOS'),
                          OL.morado,
                          Icons.check_circle_rounded,
                          aciertos,
                          (v) => '$v/$total',
                        ),
                        FichaLogro.precision(pct),
                        FichaLogro.racha(s.rachaVigente),
                      ],
                    ),
                    const SizedBox(height: 16),
                    if (siguiente != null)
                      Tarjeta(
                        color: OL.moradoSuave,
                        sombra: false,
                        child: Row(
                          children: [
                            EstadoLeccionIcono(
                              LessonState.actual,
                              numero: siguiente.numero,
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    tr('Siguiente lección'),
                                    style: const TextStyle(
                                      color: OL.gris,
                                      fontSize: 11,
                                    ),
                                  ),
                                  Text(
                                    siguiente.titulo,
                                    style: const TextStyle(
                                      fontWeight: FontWeight.w700,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    if (nivelCompleto)
                      Tarjeta(
                        color: OL.naranjaSuave,
                        sombra: false,
                        child: Text(
                          tr('¡Completaste las 100 lecciones! El examen final ya está desbloqueado.'),
                          style: const TextStyle(fontWeight: FontWeight.w700),
                        ),
                      ),
                    const Spacer(),
                    BotonPrincipal(
                      onPressed: () {
                        if (nivelCompleto) {
                          context.go('/examen/${l.nivel}');
                        } else if (siguiente != null) {
                          context.go('/leccion/${siguiente.id}');
                        } else {
                          context.go('/inicio');
                        }
                      },
                      child: Text(nivelCompleto ? tr('IR AL EXAMEN') : tr('CONTINUAR')),
                    ),
                    const SizedBox(height: 10),
                    OutlinedButton(
                      onPressed: () => context.go('/leccion/$lessonId'),
                      child: Text(tr('Repetir lección')),
                    ),
                    TextButton(
                      onPressed: () => context.go('/inicio'),
                      child: Text(tr('Volver al inicio')),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
