import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/nivel0/nivel0.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/skill_badge.dart';
import '../../shared/widgets/widgets.dart';
import '../../core/i18n/i18n.dart';

/// Biblioteca: material de consulta y práctica libre, siempre del nivel del
/// alumno (nunca se le pide elegir nivel). Lo que se enseña en orden vive en
/// Aprender (ruta); las conversaciones, en Practicar.
class BibliotecaScreen extends ConsumerWidget {
  const BibliotecaScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final nivel = s.nivelActual.clamp(1, 10);
    // Lecturas, escuchas y guías existen por ahora solo en inglés.
    final ingles = s.idiomaMeta == 'en';
    return Scaffold(
      appBar: AppBar(title: Text(tr('Biblioteca'))),
      body: Movil(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 8, 20, 32),
          children: [
            Text(
              tr(
                'Lee, escucha y consulta a tu ritmo. Todo está ajustado a tu nivel.',
              ),
              style: const TextStyle(color: OL.gris, fontSize: 15, height: 1.4),
            ),
            const SizedBox(height: 16),
            _Entrada(
              icono: Icons.style_rounded,
              titulo: tr('Mis palabras'),
              detalle: tr(
                'Todo lo que has aprendido, con repaso para que no se te olvide.',
              ),
              onTap: () => context.push('/palabras'),
            ),
            if (idiomasConNivel0.contains(s.idiomaMeta))
              _Entrada(
                icono: Icons.palette_outlined,
                titulo: tr('Mapa de sonidos'),
                detalle: tr(
                  'Cada sonido con su imagen y su color, para leer sin dudas.',
                ),
                onTap: () => context.push('/nivel0/sonidos'),
              ),
            if (ingles) ...[
              _Entrada(
                icono: Icons.swap_horiz_rounded,
                titulo: tr('Mis verbos'),
                detalle: tr(
                  'Cómo se conjugan, con audio y práctica de los irregulares.',
                ),
                onTap: () => context.push('/verbos'),
              ),
              _Entrada(
                habilidad: 'comprension',
                titulo: tr('Lecturas'),
                detalle: tr(
                  'Textos cortos con sus palabras clave y preguntas.',
                ),
                onTap: () => context.push('/estudiar?skill=comprension'),
              ),
              _Entrada(
                habilidad: 'listening',
                titulo: tr('Escuchas'),
                detalle: tr(
                  'Audios de tu nivel, con transcripción si la necesitas.',
                ),
                onTap: () => context.push('/estudiar?skill=listening'),
              ),
              _Entrada(
                habilidad: 'gramatica',
                titulo: tr('Guías de gramática'),
                detalle: tr('Reglas con ejemplos para consultar cuando dudes.'),
                onTap: () => context.push('/gramatica?nivel=$nivel'),
              ),
            ] else
              Tarjeta(
                color: OL.moradoSuave,
                sombra: false,
                child: Text(
                  tr(
                    'La biblioteca de este idioma llega con su nuevo curso. Mientras tanto, practica con tu tutor y las situaciones.',
                  ),
                  style: const TextStyle(fontSize: 15, height: 1.4),
                ),
              ),
          ],
        ),
      ),
    );
  }
}

class _Entrada extends StatelessWidget {
  const _Entrada({
    this.habilidad,
    this.icono,
    required this.titulo,
    required this.detalle,
    required this.onTap,
  });
  final String? habilidad;
  final IconData? icono;
  final String titulo, detalle;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Tarjeta(
      onTap: onTap,
      child: Row(
        children: [
          if (habilidad != null)
            InsigniaHabilidad(habilidad!, size: 48)
          else
            CircleAvatar(
              radius: 24,
              backgroundColor: OL.moradoSuave,
              child: Icon(icono, color: OL.morado),
            ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  titulo,
                  style: const TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  detalle,
                  style: const TextStyle(color: OL.gris, fontSize: 14),
                ),
              ],
            ),
          ),
          const Icon(Icons.chevron_right_rounded, color: OL.gris),
        ],
      ),
    ),
  );
}
