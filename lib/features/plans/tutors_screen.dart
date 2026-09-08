import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/content/fotos.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Avatares / tutores de IA con personalidad (REQUERIMIENTOS §5).
class TutorsScreen extends ConsumerWidget {
  const TutorsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => context.canPop() ? context.pop() : context.go('/practicar')),
        title: const Text('Tu tutor de IA'),
      ),
      body: Movil(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
          children: [
            const Text('Elige con quién quieres conversar. Todos se adaptan a tu nivel; cambia la personalidad y el estilo de corrección.',
                style: TextStyle(color: OL.gris, height: 1.4)),
            const SizedBox(height: 16),
            for (final t in tutores)
              Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: Tarjeta(
                  onTap: () => ref.read(progressProvider.notifier).elegirTutor(t.id),
                  borde: t.id == s.tutorId ? t.color : null,
                  child: Row(children: [
                    Container(
                      width: 60,
                      height: 60,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(color: t.color, width: 2.5),
                        image: DecorationImage(image: AssetImage(fotoTutor(t.id)), fit: BoxFit.cover),
                      ),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Row(children: [
                          Text(t.nombre, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
                          const SizedBox(width: 8),
                          Etiqueta(nombrePersonalidad(t.personalidad), color: t.color),
                        ]),
                        const SizedBox(height: 4),
                        Text(t.descripcion, style: const TextStyle(color: OL.gris, fontSize: 13, height: 1.3)),
                      ]),
                    ),
                    Icon(t.id == s.tutorId ? Icons.check_circle : Icons.circle_outlined, color: t.id == s.tutorId ? t.color : OL.grisClaro),
                  ]),
                ),
              ),
            const SizedBox(height: 8),
            Tarjeta(
              color: OL.moradoSuave,
              sombra: false,
              child: const Row(children: [
                Icon(Icons.record_voice_over_outlined, color: OL.morado),
                SizedBox(width: 12),
                Expanded(
                  child: Text('Voz y avatar animado de cada tutor se conectan en la fase 2 (STT/TTS + Claude).',
                      style: TextStyle(fontSize: 12, color: OL.morado, fontWeight: FontWeight.w600)),
                ),
              ]),
            ),
          ],
        ),
      ),
    );
  }
}
