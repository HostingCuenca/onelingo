import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/dominio.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/state/providers.dart';
import 'widgets.dart';

/// Acceso a la ruta de Fundamentos del idioma que se estudia, con su avance.
class TarjetaFundamentos extends ConsumerWidget {
  const TarjetaFundamentos({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final ruta = ref.watch(rutaProvider(s.idiomaMeta)).valueOrNull;
    final estados = ruta == null ? null : estadosAlumno(ruta, s);
    final siguiente = ruta == null ? null : unidadRecomendada(ruta, estados!);
    // La tarjeta sigue al nivel de la próxima unidad (f0, luego A1…).
    final nivel = siguiente?.nivel ?? 'f0';
    final unidades = ruta?.delNivel(nivel) ?? const [];
    final aprobadas = estados == null
        ? 0
        : unidades
              .where((u) => estados[u.id]!.estado.alMenos(EstadoUnidad.aprobada))
              .length;
    final cadena = ruta == null ? const ['es'] : cadenaDelAlumno(s, ruta.curso);
    final completo = unidades.isNotEmpty && aprobadas == unidades.length;
    final tituloNivel = ruta?.curso.niveles
        .where((n) => n.id == nivel)
        .firstOrNull
        ?.titulo
        .en(cadena);
    return Tarjeta(
      onTap: () =>
          context.push(nivel == 'f0' ? '/fundamentos' : '/ruta/$nivel'),
      color: OL.moradoSuave,
      borde: OL.morado,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Icon(Icons.school_rounded, color: OL.morado, size: 32),
          const SizedBox(height: 10),
          Text(
            completo
                ? 'Fundamentos completados'
                : aprobadas == 0 && siguiente?.orden == 0
                ? 'Empieza desde cero'
                : 'Continuar: ${siguiente?.titulo.en(cadena) ?? 'Fundamentos'}',
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.w900,
              color: OL.morado,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            completo
                ? 'Repasa cuando te lo pidamos para asegurar lo aprendido.'
                : siguiente?.objetivo.en(cadena) ??
                      'Aprende las bases paso a paso.',
            style: const TextStyle(fontSize: 16, height: 1.4),
          ),
          const SizedBox(height: 12),
          BarraProgreso(unidades.isEmpty ? 0 : aprobadas / unidades.length),
          const SizedBox(height: 8),
          Text(
            nivel == 'f0'
                ? '$aprobadas de ${unidades.length} unidades aprobadas'
                : '${tituloNivel ?? ''} · $aprobadas de ${unidades.length} unidades aprobadas',
            style: const TextStyle(fontSize: 14, height: 1.4, color: OL.gris),
          ),
        ],
      ),
    );
  }
}
