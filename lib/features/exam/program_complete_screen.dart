import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/curriculum.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Pantalla especial al aprobar el Nivel 10 (REQUERIMIENTOS §3).
class ProgramCompleteScreen extends ConsumerWidget {
  const ProgramCompleteScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: OL.gradienteMorado),
        child: Movil(
          child: SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(28),
              child: Column(
                children: [
                  const Spacer(),
                  Container(
                    padding: const EdgeInsets.all(24),
                    decoration: const BoxDecoration(
                      color: OL.blanco,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(
                      Icons.workspace_premium,
                      size: 80,
                      color: OL.naranja,
                    ),
                  ),
                  const SizedBox(height: 28),
                  const Text(
                    'PROGRAMA COMPLETADO',
                    style: TextStyle(
                      color: OL.naranja,
                      fontWeight: FontWeight.w800,
                      letterSpacing: 2,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '¡Felicidades, ${s.nombre.split(' ').first}!',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.headlineLarge
                        ?.copyWith(color: OL.blanco),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'Completaste los 10 niveles de ${idioma(s.idiomaMeta).nombre}: 1 000 lecciones, '
                    '10 exámenes y el Nivel Dominio. Ya te comunicas con naturalidad.',
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      color: Color(0xFFE0D8FF),
                      height: 1.5,
                    ),
                  ),
                  const SizedBox(height: 24),
                  Row(
                    children: [
                      _Dato('${s.xp}', 'XP totales'),
                      _Dato('${s.completadas.length}', 'Lecciones'),
                      _Dato('${s.segundosEstudio ~/ 3600} h', 'Estudio'),
                    ],
                  ),
                  const Spacer(),
                  BotonPrincipal(
                    color: OL.naranja,
                    onPressed: () => context.go('/practicar'),
                    child: const Text('SEGUIR PRACTICANDO CON IA'),
                  ),
                  const SizedBox(height: 10),
                  TextButton(
                    onPressed: () => context.go('/planes'),
                    child: const Text(
                      'Aprender otro idioma',
                      style: TextStyle(color: OL.blanco),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _Dato extends StatelessWidget {
  const _Dato(this.v, this.l);
  final String v, l;

  @override
  Widget build(BuildContext context) => Expanded(
    child: Column(
      children: [
        Text(
          v,
          style: const TextStyle(
            color: OL.blanco,
            fontSize: 22,
            fontWeight: FontWeight.w800,
          ),
        ),
        Text(l, style: const TextStyle(color: Color(0xFFE0D8FF), fontSize: 12)),
      ],
    ),
  );
}
