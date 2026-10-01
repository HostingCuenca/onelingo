import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/nivel0/nivel0.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/lumo.dart';
import '../../shared/widgets/widgets.dart';
import 'palabra_color.dart';

/// Nivel 0 · Leer y pronunciar: unidades y lecciones con su progreso, y
/// acceso al Mapa de Sonidos. Lumo guía (un solo personaje en pantalla).
class Nivel0Screen extends ConsumerWidget {
  const Nivel0Screen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final nivel = ref.watch(nivel0Provider);
    final practicas = ref.watch(progressProvider).practicas;
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/inicio'),
        ),
        title: const Text('Nivel 0 · Leer y pronunciar'),
      ),
      body: nivel.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (_, _) =>
            const Center(child: Text('No se pudo cargar el Nivel 0.')),
        data: (n) {
          final hechas = n.lecciones
              .where((l) => leccionN0Completa(practicas, l.id))
              .length;
          final siguiente = siguienteN0(n, practicas);
          return Movil(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(20, 8, 20, 32),
              children: [
                Tarjeta(
                  color: OL.moradoSuave,
                  sombra: false,
                  child: Row(
                    children: [
                      const LumoReaccion(pose: PoseLumo.anima, size: 92),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              n.subtitulo,
                              style: const TextStyle(
                                fontSize: 15,
                                height: 1.35,
                              ),
                            ),
                            const SizedBox(height: 10),
                            BarraProgreso(
                              n.lecciones.isEmpty
                                  ? 0
                                  : hechas / n.lecciones.length,
                              alto: 8,
                            ),
                            const SizedBox(height: 4),
                            Text(
                              '$hechas de ${n.lecciones.length} lecciones',
                              style: const TextStyle(
                                color: OL.gris,
                                fontSize: 13,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 14),
                if (siguiente != null)
                  BotonPrincipal(
                    onPressed: () =>
                        context.push('/nivel0/leccion/${siguiente.id}'),
                    child: Text(
                      hechas == 0
                          ? 'EMPEZAR'
                          : 'CONTINUAR: ${siguiente.titulo.toUpperCase()}',
                    ),
                  ),
                const SizedBox(height: 10),
                OutlinedButton.icon(
                  onPressed: () => context.push('/nivel0/sonidos'),
                  icon: const Icon(Icons.palette_outlined),
                  label: const Text('Mapa de sonidos'),
                ),
                const SizedBox(height: 22),
                for (final u in n.unidades) ...[
                  Text(
                    u.titulo,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    u.objetivo,
                    style: const TextStyle(color: OL.gris, fontSize: 14),
                  ),
                  const SizedBox(height: 10),
                  for (final l in u.lecciones)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 8),
                      child: _FilaLeccion(
                        leccion: l,
                        completa: leccionN0Completa(practicas, l.id),
                        abierta: leccionN0Abierta(n, practicas, l.id),
                      ),
                    ),
                  const SizedBox(height: 14),
                ],
                const Tarjeta(
                  color: OL.amarilloSuave,
                  sombra: false,
                  child: Text(
                    'Próximamente: más sonidos (c, k, e, h, r…), la e mágica, vocales largas y la prueba final «Ya puedo leer inglés».',
                    style: TextStyle(fontSize: 14, height: 1.35),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}

class _FilaLeccion extends StatelessWidget {
  const _FilaLeccion({
    required this.leccion,
    required this.completa,
    required this.abierta,
  });
  final LeccionN0 leccion;
  final bool completa, abierta;

  @override
  Widget build(BuildContext context) => Tarjeta(
    onTap: abierta ? () => context.push('/nivel0/leccion/${leccion.id}') : null,
    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
    color: abierta ? OL.blanco : OL.fondo,
    sombra: abierta,
    child: Row(
      children: [
        Icon(
          completa
              ? Icons.check_circle_rounded
              : (abierta ? Icons.play_circle_fill_rounded : Icons.lock_rounded),
          color: completa ? OL.verde : (abierta ? OL.morado : OL.gris),
          size: 30,
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            leccion.titulo,
            style: TextStyle(
              fontSize: 17,
              fontWeight: FontWeight.w800,
              color: abierta ? OL.texto : OL.gris,
            ),
          ),
        ),
        if (abierta) const Icon(Icons.chevron_right_rounded, color: OL.gris),
      ],
    ),
  );
}

/// Mapa de Sonidos: cada sonido de vocal con su imagen y su color. Los que
/// aún no se han visto quedan atenuados con la unidad en la que se aprenden.
class MapaSonidosScreen extends ConsumerWidget {
  const MapaSonidosScreen({super.key});

  static const _grupos = {
    'corta': 'Vocales cortas',
    'larga': 'Vocales largas (dicen su nombre)',
    'diptongo': 'Vocales que se deslizan',
    'r': 'Vocales con R',
    'fantasma': 'La vocal fantasma',
  };

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final nivel = ref.watch(nivel0Provider);
    final practicas = ref.watch(progressProvider).practicas;
    return Scaffold(
      appBar: AppBar(title: const Text('Mapa de sonidos')),
      body: nivel.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (_, _) =>
            const Center(child: Text('No se pudo cargar el mapa.')),
        data: (n) {
          // Unidad más alta con alguna lección completa.
          var vista = 1;
          for (final u in n.unidades) {
            if (u.lecciones.any((l) => leccionN0Completa(practicas, l.id))) {
              vista = int.tryParse(u.id.replaceAll(RegExp(r'\D'), '')) ?? vista;
            }
          }
          return Movil(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(20, 8, 20, 32),
              children: [
                const Text(
                  'En inglés una misma letra puede sonar distinto. Cada sonido tiene una imagen y un color: así lo verás en las palabras. Toca una tarjeta para oírla.',
                  style: TextStyle(fontSize: 15, height: 1.4, color: OL.gris),
                ),
                const SizedBox(height: 14),
                for (final g in _grupos.entries) ...[
                  Text(
                    g.value,
                    style: const TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                  const SizedBox(height: 8),
                  LayoutBuilder(
                    builder: (context, c) {
                      final cols = c.maxWidth > 520 ? 3 : 2;
                      final ancho = (c.maxWidth - (cols - 1) * 10) / cols;
                      return Wrap(
                        spacing: 10,
                        runSpacing: 10,
                        children: [
                          for (final s in n.sonidos.where(
                            (s) => s.grupo == g.key,
                          ))
                            SizedBox(
                              width: ancho,
                              child: _TarjetaSonido(
                                n: n,
                                s: s,
                                aprendido: s.unidad <= vista,
                              ),
                            ),
                        ],
                      );
                    },
                  ),
                  const SizedBox(height: 16),
                ],
              ],
            ),
          );
        },
      ),
    );
  }
}

class _TarjetaSonido extends StatelessWidget {
  const _TarjetaSonido({
    required this.n,
    required this.s,
    required this.aprendido,
  });
  final Nivel0 n;
  final SonidoVocal s;
  final bool aprendido;

  @override
  Widget build(BuildContext context) => Opacity(
    opacity: aprendido ? 1 : .45,
    child: Semantics(
      button: true,
      label: '${s.nombre}, color ${s.colorNombre}',
      child: Tarjeta(
        onTap: () => decir(n, '${s.ancla}. ${s.ejemplos.join(', ')}.'),
        padding: const EdgeInsets.all(12),
        borde: s.color,
        child: Column(
          children: [
            ImagenPalabra(s.emoji, tamano: 52),
            Text(
              s.ancla,
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.w900,
                color: s.grupo == 'fantasma' ? OL.gris : s.color,
              ),
            ),
            Text(
              s.colorNombre,
              style: const TextStyle(fontSize: 12, color: OL.gris),
            ),
            const SizedBox(height: 4),
            Text(
              s.grafias.join(' · '),
              style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w800),
            ),
            Text(
              s.ejemplos.join(', '),
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 12, color: OL.gris),
            ),
            if (!aprendido)
              Text(
                'Unidad ${s.unidad}',
                style: const TextStyle(fontSize: 11, color: OL.gris),
              ),
          ],
        ),
      ),
    ),
  );
}
