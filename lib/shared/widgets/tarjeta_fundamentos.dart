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
    final unidades = ruta?.delNivel('f0') ?? const [];
    final estados = ruta == null ? null : estadosRuta(ruta, s.practicas);
    final aprobadas = estados == null
        ? 0
        : unidades
              .where((u) => estados[u.id]!.estado.alMenos(EstadoUnidad.aprobada))
              .length;
    final siguiente = ruta == null ? null : unidadRecomendada(ruta, estados!);
    final cadena = ruta == null ? const ['es'] : cadenaDelAlumno(s, ruta.curso);
    final completo = unidades.isNotEmpty && aprobadas == unidades.length;
    return Tarjeta(
      onTap: () => context.push('/fundamentos'),
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
            '$aprobadas de ${unidades.length} unidades aprobadas',
            style: const TextStyle(fontSize: 14, height: 1.4, color: OL.gris),
          ),
        ],
      ),
    );
  }
}
