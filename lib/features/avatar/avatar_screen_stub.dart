import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'tutores_3d.dart';

class AvatarScreen extends StatelessWidget {
  const AvatarScreen({
    super.key,
    required this.tutorId,
    this.tema,
    this.objetivoId,
  });
  final String tutorId;
  final int? tema;
  final String? objetivoId;
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: Text(tutor3d(tutorId)?.nombre ?? 'Tutor con IA')),
    body: Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'La videollamada está disponible en la versión web.',
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: () => context.push('/chat'),
              child: const Text('Hablar con mi tutor por voz'),
            ),
          ],
        ),
      ),
    ),
  );
}
