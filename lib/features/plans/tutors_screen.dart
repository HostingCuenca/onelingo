import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/content/fotos.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import '../avatar/tutores_3d.dart';

const _idiomas = {
  'en': 'inglés',
  'es': 'español',
  'fr': 'francés',
  'de': 'alemán',
  'pt': 'portugués',
  'it': 'italiano',
  'zh': 'chino',
  'ja': 'japonés',
  'ko': 'coreano',
  'ru': 'ruso',
};

/// Tutores con IA: una sola pantalla para la videollamada con un tutor 3D y
/// el chat de voz y texto (antes eran dos experiencias separadas).
class TutorsScreen extends ConsumerWidget {
  const TutorsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final idioma = _idiomas[s.idiomaMeta] ?? 'inglés';
    final recomendados = recomendados3d(s.idiomaMeta);
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/practicar'),
        ),
        title: const Text('Tutores con IA'),
      ),
      body: Movil(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                'Practica $idioma conversando. Tu tutor te escucha, te responde con voz, corrige tus errores y se adapta a tu nivel.',
                style: const TextStyle(color: OL.gris, height: 1.4),
              ),
              const SizedBox(height: 20),
              const _Seccion(
                icono: Icons.videocam_rounded,
                titulo: 'Videollamada con un tutor',
                texto: 'Cara a cara, por voz o escribiendo.',
              ),
              if (!kIsWeb)
                Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: Tarjeta(
                    color: OL.amarilloSuave,
                    sombra: false,
                    child: const Text(
                      'La videollamada está disponible en la versión web. Mientras tanto, usa el chat de voz de abajo.',
                      style: TextStyle(fontSize: 13, height: 1.35),
                    ),
                  ),
                ),
              LayoutBuilder(
                builder: (context, c) {
                  final columnas = c.maxWidth > 560 ? 3 : 2;
                  return GridView.count(
                    crossAxisCount: columnas,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    mainAxisSpacing: 12,
                    crossAxisSpacing: 12,
                    childAspectRatio: .66,
                    children: [
                      for (final t in tutores3dPara(s.idiomaMeta))
                        _TarjetaTutor3d(
                          tutor: t,
                          recomendado: recomendados.contains(t.id),
                          onTap: () {
                            if (kIsWeb) {
                              context.push('/avatar/${t.id}');
                            } else {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text(
                                    'La videollamada está disponible en la versión web.',
                                  ),
                                ),
                              );
                            }
                          },
                        ),
                    ],
                  );
                },
              ),
              const SizedBox(height: 28),
              const _Seccion(
                icono: Icons.forum_rounded,
                titulo: 'Chat de voz y texto',
                texto: 'Elige la personalidad de tu tutor; recuerda tus objetivos y correcciones.',
              ),
              for (final t in tutores)
                Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: Tarjeta(
                    onTap: () =>
                        ref.read(progressProvider.notifier).elegirTutor(t.id),
                    borde: t.id == s.tutorId ? t.color : null,
                    child: Row(
                      children: [
                        Container(
                          width: 104,
                          height: 136,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: t.color, width: 2.5),
                            image: DecorationImage(
                              image: AssetImage(fotoTutor(t.id)),
                              alignment: encuadreTutor(t.id),
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Wrap(
                                spacing: 4,
                                runSpacing: 6,
                                children: [
                                  Text(
                                    t.nombre,
                                    style: const TextStyle(
                                      fontSize: 16,
                                      fontWeight: FontWeight.w800,
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  Etiqueta(
                                    nombrePersonalidad(t.personalidad),
                                    color: t.color,
                                  ),
                                ],
                              ),
                              const SizedBox(height: 4),
                              Text(
                                t.descripcion,
                                style: const TextStyle(
                                  color: OL.gris,
                                  fontSize: 13,
                                  height: 1.3,
                                ),
                              ),
                            ],
                          ),
                        ),
                        Icon(
                          t.id == s.tutorId
                              ? Icons.check_circle
                              : Icons.circle_outlined,
                          color: t.id == s.tutorId ? t.color : OL.grisClaro,
                        ),
                      ],
                    ),
                  ),
                ),
              const SizedBox(height: 4),
              FilledButton.icon(
                style: FilledButton.styleFrom(
                  minimumSize: const Size.fromHeight(52),
                ),
                onPressed: () => context.push('/chat'),
                icon: const Icon(Icons.mic_rounded),
                label: const Text('Hablar con mi tutor'),
              ),
              const SizedBox(height: 12),
              Tarjeta(
                color: OL.moradoSuave,
                sombra: false,
                child: const Row(
                  children: [
                    Icon(Icons.wifi_rounded, color: OL.morado),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'Para conversar con la IA necesitas conexión a internet.',
                        style: TextStyle(
                          fontSize: 12,
                          color: OL.morado,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _Seccion extends StatelessWidget {
  const _Seccion({
    required this.icono,
    required this.titulo,
    required this.texto,
  });
  final IconData icono;
  final String titulo, texto;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 12),
    child: Row(
      children: [
        IconoCuadro(icono, tamano: 40, radio: 12),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                titulo,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w900,
                ),
              ),
              Text(texto, style: const TextStyle(color: OL.gris, fontSize: 13)),
            ],
          ),
        ),
      ],
    ),
  );
}

class _TarjetaTutor3d extends StatelessWidget {
  const _TarjetaTutor3d({
    required this.tutor,
    required this.recomendado,
    required this.onTap,
  });
  final Tutor3d tutor;
  final bool recomendado;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: 'Videollamada con ${tutor.nombre}',
    child: Tarjeta(
      onTap: onTap,
      padding: EdgeInsets.zero,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            child: Stack(
              fit: StackFit.expand,
              children: [
                ClipRRect(
                  borderRadius: const BorderRadius.vertical(
                    top: Radius.circular(18),
                  ),
                  child: ColoredBox(
                    color: OL.moradoSuave,
                    child: Image.asset(
                      tutor.retrato,
                      fit: BoxFit.cover,
                      alignment: Alignment.topCenter,
                      excludeFromSemantics: true,
                    ),
                  ),
                ),
                if (recomendado)
                  Positioned(
                    top: 8,
                    left: 8,
                    child: Etiqueta(
                      'Recomendado',
                      color: OL.blanco,
                      fondo: OL.naranja,
                    ),
                  ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(12, 10, 12, 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  tutor.nombre,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  tutor.estilo,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    color: OL.gris,
                    fontSize: 12,
                    height: 1.25,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    ),
  );
}
