import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/curriculum.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../shared/confeti.dart';
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
                    AnilloProgreso(
                      valor: pct / 100,
                      tamano: 150,
                      grosor: 12,
                      color: pct >= 65 ? OL.verde : OL.naranja,
                      child: Text(
                        '$pct%',
                        style: const TextStyle(
                          fontSize: 34,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                    ),
                    const SizedBox(height: 22),
                    Text(
                      pct == 100
                          ? '¡Perfecto, ${s.nombre.split(' ').first}!'
                          : '¡Lección completada!',
                      style: Theme.of(context).textTheme.headlineMedium,
                    ),
                    const SizedBox(height: 6),
                    const Text(
                      'Práctica completada. El dominio se confirma con ejercicios nuevos y repaso.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: OL.gris, fontSize: 12),
                    ),
                    Text(
                      l?.titulo ?? '',
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: OL.gris),
                    ),
                    const SizedBox(height: 22),
                    Row(
                      children: [
                        _Stat('${s.xp}', 'XP total', OL.naranja),
                        const SizedBox(width: 10),
                        _Stat('$aciertos/$total', 'Aciertos', OL.verde),
                        const SizedBox(width: 10),
                        _Stat('${s.rachaVigente}', 'Racha', OL.morado),
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
                                  const Text(
                                    'Siguiente lección',
                                    style: TextStyle(
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
                        child: const Text(
                          '¡Completaste las 100 lecciones! El examen final ya está desbloqueado.',
                          style: TextStyle(fontWeight: FontWeight.w700),
                        ),
                      ),
                    const Spacer(),
                    ElevatedButton(
                      onPressed: () {
                        if (nivelCompleto) {
                          context.go('/examen/${l.nivel}');
                        } else if (siguiente != null) {
                          context.go('/leccion/${siguiente.id}');
                        } else {
                          context.go('/inicio');
                        }
                      },
                      child: Text(nivelCompleto ? 'IR AL EXAMEN' : 'CONTINUAR'),
                    ),
                    const SizedBox(height: 10),
                    OutlinedButton(
                      onPressed: () => context.go('/leccion/$lessonId'),
                      child: const Text('Repetir lección'),
                    ),
                    TextButton(
                      onPressed: () => context.go('/inicio'),
                      child: const Text('Volver al inicio'),
                    ),
                  ],
                ),
              ),
            ),
          ),
          if (pct >= 60) const Confeti(),
        ],
      ),
    );
  }
}

class _Stat extends StatelessWidget {
  const _Stat(this.v, this.l, this.c);
  final String v, l;
  final Color c;

  @override
  Widget build(BuildContext context) => Expanded(
    child: Tarjeta(
      padding: const EdgeInsets.symmetric(vertical: 14),
      child: Column(
        children: [
          Text(
            v,
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.w800,
              color: c,
            ),
          ),
          Text(
            l,
            style: const TextStyle(
              color: OL.gris,
              fontSize: 11,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    ),
  );
}
