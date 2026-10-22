import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/content/fotos.dart';
import '../../core/i18n/i18n.dart';
import '../../core/i18n/nombres_idioma.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import '../avatar/tutores_3d.dart';

/// Tutores con IA: una sola pantalla para la videollamada con un tutor 3D y
/// el chat de voz y texto (antes eran dos experiencias separadas).
class TutorsScreen extends ConsumerWidget {
  const TutorsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final idioma = nombreIdiomaEnFrase(s.idiomaMeta);
    final recomendados = recomendados3d(s.idiomaMeta);
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/practicar'),
        ),
        title: Text(tr('Tutores con IA')),
      ),
      body: Movil(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                tr(
                  'Practica {idioma} conversando. Tu tutor te escucha, te responde con voz, corrige tus errores y se adapta a tu nivel.',
                  {'idioma': idioma},
                ),
                style: const TextStyle(color: OL.gris, height: 1.4),
              ),
              const SizedBox(height: 20),
              _Seccion(
                icono: Icons.videocam_rounded,
                titulo: tr('Videollamada con un tutor'),
                texto: tr('Cara a cara, por voz o escribiendo.'),
              ),
              // Los tutores realistas en vivo van primero, en una fila que se
              // desliza, antes de las tarjetas de Ana y Lumo.
              Text(
                tr('Nuevos tutores en vivo'),
                style: const TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 8),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                clipBehavior: Clip.none,
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    for (final t in tutoresVivo)
                      Padding(
                        padding: const EdgeInsets.only(right: 12),
                        child: SizedBox(
                          width: 148,
                          height: 236,
                          child: _TarjetaTutor3d(
                            tutor: t,
                            recomendado: false,
                            enVivo: true,
                            onTap: () => _abrirVideollamada(context, t.id),
                          ),
                        ),
                      ),
                  ],
                ),
              ),
              const SizedBox(height: 16),
              _TarjetaDestacada(
                tutor: anaTutor,
                titulo: tr('Llamada en vivo con Ana'),
                etiqueta: tr('En vivo'),
                recortar: true,
                onTap: () => _abrirVideollamada(context, 'ana'),
              ),
              const SizedBox(height: 12),
              _TarjetaDestacada(
                tutor: lumoTutor,
                titulo: tr('Habla con Lumo'),
                etiqueta: tr('Nuevo'),
                onTap: () => _abrirVideollamada(context, 'lumo'),
              ),
              const SizedBox(height: 12),
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
                          onTap: () => _abrirVideollamada(context, t.id),
                        ),
                    ],
                  );
                },
              ),
              const SizedBox(height: 28),
              _Seccion(
                icono: Icons.forum_rounded,
                titulo: tr('Chat de voz y texto'),
                texto: tr(
                  'Elige la personalidad de tu tutor; recuerda tus objetivos y correcciones.',
                ),
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
                label: Text(tr('Hablar con mi tutor')),
              ),
              const SizedBox(height: 12),
              Tarjeta(
                color: OL.moradoSuave,
                sombra: false,
                child: Row(
                  children: [
                    const Icon(Icons.wifi_rounded, color: OL.morado),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        tr(
                          'Para conversar con la IA necesitas conexión a internet.',
                        ),
                        style: const TextStyle(
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

void _abrirVideollamada(BuildContext context, String id) =>
    context.push('/avatar/$id');

/// Tutor destacado (Ana en vivo, Lumo): un solo personaje en la tarjeta,
/// sin animación de entrada.
class _TarjetaDestacada extends StatelessWidget {
  const _TarjetaDestacada({
    required this.tutor,
    required this.titulo,
    required this.etiqueta,
    required this.onTap,
    this.recortar = false,
  });
  final Tutor3d tutor;
  final String titulo, etiqueta;
  final VoidCallback onTap;

  /// Retrato realista: llena el cuadro con esquinas redondeadas.
  final bool recortar;

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: tr('Videollamada con {tutor}', {'tutor': tutor.nombre}),
    child: Tarjeta(
      onTap: onTap,
      color: OL.moradoSuave,
      borde: OL.moradoClaro,
      padding: const EdgeInsets.fromLTRB(8, 8, 16, 8),
      child: Row(
        children: [
          SizedBox(
            width: 108,
            height: 132,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(recortar ? 16 : 0),
              child: Image.asset(
                tutor.retrato,
                fit: recortar ? BoxFit.cover : BoxFit.contain,
                alignment: Alignment.topCenter,
                excludeFromSemantics: true,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Etiqueta(etiqueta, color: OL.blanco, fondo: OL.naranja),
                const SizedBox(height: 6),
                Text(
                  titulo,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  tutor.estilo,
                  style: const TextStyle(
                    color: OL.gris,
                    fontSize: 13,
                    height: 1.3,
                  ),
                ),
              ],
            ),
          ),
          const Icon(Icons.videocam_rounded, color: OL.morado),
        ],
      ),
    ),
  );
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
    this.enVivo = false,
  });
  final Tutor3d tutor;
  final bool recomendado;

  /// Tutor de la llamada en vivo (micrófono abierto).
  final bool enVivo;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: tr('Videollamada con {tutor}', {'tutor': tutor.nombre}),
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
                if (enVivo)
                  Positioned(
                    top: 8,
                    left: 8,
                    child: Etiqueta(
                      tr('En vivo'),
                      color: OL.blanco,
                      fondo: OL.morado,
                    ),
                  ),
                if (recomendado)
                  Positioned(
                    top: 8,
                    left: 8,
                    child: Etiqueta(
                      tr('Recomendado'),
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
