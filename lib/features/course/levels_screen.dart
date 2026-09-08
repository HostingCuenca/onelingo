import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/curriculum.dart';
import '../../core/content/fundamentos.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Mapa de los 10 niveles con su estado (bloqueado / en curso / aprobado).
class LevelsScreen extends ConsumerWidget {
  const LevelsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final meta = idioma(s.idiomaMeta);
    return Scaffold(
      appBar: AppBar(title: Text('Curso de ${meta.nombre}')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
        children: [
          const Text('10 niveles · 100 lecciones por nivel · examen final al 65 %',
              style: TextStyle(color: OL.gris, fontSize: 13)),
          const SizedBox(height: 14),
          if (leccionesDe(0).isNotEmpty) _NivelCard(lvl: nivelFundamentos, s: s),
          for (final lvl in niveles) _NivelCard(lvl: lvl, s: s),
        ],
      ),
    );
  }
}

class _NivelCard extends StatelessWidget {
  const _NivelCard({required this.lvl, required this.s});
  final Level lvl;
  final ProgressState s;

  @override
  Widget build(BuildContext context) {
    final n = lvl.numero;
    final desbloqueado = s.nivelDesbloqueado(n);
    final aprobado = s.examenAprobado(n);
    final progreso = s.progresoNivel(n);
    final esActual = desbloqueado && !aprobado;
    final color = aprobado ? OL.verde : esActual ? OL.morado : OL.gris;

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Opacity(
        opacity: desbloqueado ? 1 : 0.55,
        child: Tarjeta(
          onTap: desbloqueado ? () => context.push('/aprender/nivel/$n') : null,
          borde: esActual ? OL.moradoClaro : null,
          child: Row(children: [
            AnilloProgreso(
              valor: aprobado ? 1 : progreso,
              tamano: 56,
              grosor: 6,
              color: color,
              child: aprobado
                  ? const Icon(Icons.check, color: OL.verde)
                  : desbloqueado
                      ? Text('$n', style: TextStyle(fontWeight: FontWeight.w800, color: color))
                      : const Icon(Icons.lock_outline, color: OL.gris, size: 18),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(n == 0 ? 'Fundamentos · empieza de cero' : 'Nivel $n · ${lvl.nombre}', style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 15)),
                const SizedBox(height: 2),
                Text(lvl.descripcion, style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.3)),
                const SizedBox(height: 8),
                Row(children: [
                  Expanded(child: BarraProgreso(progreso, color: color, alto: 6)),
                  const SizedBox(width: 8),
                  Text('${s.completadasEnNivel(n)}/${totalLeccionesDe(n)}', style: const TextStyle(color: OL.gris, fontSize: 11, fontWeight: FontWeight.w700)),
                ]),
                if (s.examenes.containsKey(n)) ...[
                  const SizedBox(height: 6),
                  Etiqueta(
                    aprobado ? 'Examen aprobado · ${s.examenes[n]}%' : 'Examen ${s.examenes[n]}% · repite',
                    color: aprobado ? OL.verde : OL.rojo,
                  ),
                ],
              ]),
            ),
            const Icon(Icons.chevron_right, color: OL.gris),
          ]),
        ),
      ),
    );
  }
}
