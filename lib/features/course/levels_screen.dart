import '../../shared/widgets/mascot_coach.dart';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/diagnostico.dart';
import '../library/library_screen.dart';
import '../../core/content/curriculum.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../core/aprendizaje/modelos.dart';
import '../../core/aprendizaje/providers.dart';
import '../../shared/widgets/tarjeta_fundamentos.dart';
import '../../shared/widgets/widgets.dart';

/// Mapa de los 10 niveles con su estado (bloqueado / en curso / aprobado).
class LevelsScreen extends ConsumerWidget {
  const LevelsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final meta = idioma(s.idiomaMeta);
    final ruta = ref.watch(rutaProvider(s.idiomaMeta)).valueOrNull;
    // Nivel del esquema 2 para un nivel interno, si ya tiene unidades.
    String? nivelRuta(int n) {
      for (final nv in ruta?.curso.niveles ?? const <NivelCurso>[]) {
        if (nv.nivelInterno == n && ruta!.delNivel(nv.id).isNotEmpty) {
          return nv.id;
        }
      }
      return null;
    }

    // MCER según la escala del curso (Nivel 2 = A2, Nivel 3 = B1…); la
    // equivalencia histórica solo si el curso no declara el nivel.
    String cefrNivel(int n) {
      for (final nv in ruta?.curso.niveles ?? const <NivelCurso>[]) {
        if (nv.id == 'n$n') return nv.cefr;
      }
      return cefrDe(n.toDouble());
    }

    return Scaffold(
      appBar: AppBar(title: Text('Curso de ${meta.nombre}')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
        children: [
          const MascotCoach(
            message:
                'Primero entiende el ejemplo; después practica a tu ritmo.',
          ),
          if (s.idiomaMeta == 'en') ...[
            const CaminoPersonalizado(),
            const SizedBox(height: 24),
            const TituloSeccion('Explora tus diez etapas'),
            const SizedBox(height: 12),
            for (var n = 1; n <= 10; n++)
              Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: Tarjeta(
                  onTap: () => nivelRuta(n) != null
                      ? context.push('/ruta/${nivelRuta(n)}')
                      : context.push('/biblioteca?nivel=$n'),
                  child: Row(
                    children: [
                      CircleAvatar(child: Text('$n')),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          'Nivel $n · ${cefrNivel(n)} · ${nivelRuta(n) != null
                              ? 'Ruta guiada'
                              : n.isOdd
                              ? 'Explora'
                              : 'Consolida'}',
                          style: const TextStyle(fontWeight: FontWeight.w700),
                        ),
                      ),
                      const Icon(Icons.arrow_forward_rounded),
                    ],
                  ),
                ),
              ),
          ] else ...[
            const Text(
              '10 niveles · 100 lecciones por nivel · examen final al 65 %',
              style: TextStyle(color: OL.gris, fontSize: 14),
            ),
            const SizedBox(height: 14),
            // Nivel 0 = ruta de fundamentos del idioma (DEC-007); las
            // lecciones antiguas quedan como práctica extra dentro de la ruta.
            const TarjetaFundamentos(),
            const SizedBox(height: 12),
            for (final lvl in niveles) _NivelCard(lvl: lvl, s: s),
          ],
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
    final color = aprobado
        ? OL.verde
        : esActual
        ? OL.morado
        : OL.gris;

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Opacity(
        opacity: desbloqueado ? 1 : 0.55,
        child: Tarjeta(
          onTap: desbloqueado ? () => context.push('/aprender/nivel/$n') : null,
          borde: esActual ? OL.moradoClaro : null,
          child: Row(
            children: [
              AnilloProgreso(
                valor: aprobado ? 1 : progreso,
                tamano: 56,
                grosor: 6,
                color: color,
                child: aprobado
                    ? const Icon(Icons.check, color: OL.verde)
                    : desbloqueado
                    ? Text(
                        '$n',
                        style: TextStyle(
                          fontWeight: FontWeight.w800,
                          color: color,
                        ),
                      )
                    : const Icon(Icons.lock_outline, color: OL.gris, size: 18),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      n == 0
                          ? 'Fundamentos · empieza de cero'
                          : 'Nivel $n · ${lvl.nombre}',
                      style: const TextStyle(
                        fontWeight: FontWeight.w700,
                        fontSize: 15,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      lvl.descripcion,
                      style: const TextStyle(
                        color: OL.gris,
                        fontSize: 14,
                        height: 1.3,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Expanded(
                          child: BarraProgreso(progreso, color: color, alto: 6),
                        ),
                        const SizedBox(width: 8),
                        Text(
                          '${s.completadasEnNivel(n)}/${totalLeccionesDe(n)}',
                          style: const TextStyle(
                            color: OL.gris,
                            fontSize: 14,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ],
                    ),
                    if (s.examenes.containsKey(n)) ...[
                      const SizedBox(height: 6),
                      Etiqueta(
                        aprobado
                            ? 'Examen aprobado · ${s.examenes[n]}%'
                            : 'Examen ${s.examenes[n]}% · repite',
                        color: aprobado ? OL.verde : OL.rojo,
                      ),
                    ],
                  ],
                ),
              ),
              const Icon(Icons.chevron_right, color: OL.gris),
            ],
          ),
        ),
      ),
    );
  }
}
