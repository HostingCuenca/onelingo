import '../../shared/widgets/mascot_coach.dart';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/diagnostico.dart';
import '../../core/i18n/i18n.dart';
import '../../core/content/curriculum.dart';
import '../../core/state/providers.dart';
import '../../core/aprendizaje/dominio.dart';
import '../../core/aprendizaje/modelos.dart';
import '../../core/aprendizaje/providers.dart';
import '../../shared/widgets/tarjeta_en_preparacion.dart';
import '../../shared/widgets/tarjeta_fundamentos.dart';
import '../nivel0/tarjeta_nivel0.dart';
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
    String cefrDelNivel(int n) {
      for (final nv in ruta?.curso.niveles ?? const <NivelCurso>[]) {
        if (nv.id == 'n$n') return nv.cefr;
      }
      return cefrNivel(n);
    }

    return Scaffold(
      appBar: AppBar(title: Text(tr('Curso de {idioma}', {'idioma': meta.nombre}))),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
        children: [
          MascotCoach(
            message:
                tr('Primero entiende el ejemplo; después practica a tu ritmo.'),
          ),
          if (idiomasConRuta.contains(s.idiomaMeta)) ...[
            TituloSeccion(tr('Tus diez niveles')),
            const SizedBox(height: 12),
            // Nivel 0 · Leer y pronunciar (desde cero), antes de los diez niveles.
            const TarjetaNivel0(),
            const SizedBox(height: 10),
            const TarjetaFundamentos(),
            const SizedBox(height: 10),
            for (var n = 1; n <= 10; n++)
              _TarjetaNivelRuta(
                numero: n,
                cefr: cefrDelNivel(n),
                nivelId: nivelRuta(n),
                ruta: ruta,
                estado: s,
              ),
          ] else ...[
            TarjetaEnPreparacion(idioma: meta.nombre),
          ],
        ],
      ),
    );
  }
}

/// Nivel de la ruta (inglés): superado, en curso o bloqueado. Se sube
/// terminando sus clases o aprobando su prueba; nunca eligiendo el nivel.
class _TarjetaNivelRuta extends StatelessWidget {
  const _TarjetaNivelRuta({
    required this.numero,
    required this.cefr,
    required this.nivelId,
    required this.ruta,
    required this.estado,
  });
  final int numero;
  final String cefr;
  final String? nivelId;
  final RutaCargada? ruta;
  final ProgressState estado;

  @override
  Widget build(BuildContext context) {
    final id = nivelId;
    final r = ruta;
    if (id == null || r == null) {
      return _fila(
        context,
        icono: Icons.schedule_rounded,
        color: OL.gris,
        detalle: tr('Próximamente'),
        onTap: null,
      );
    }
    final estados = estadosAlumno(r, estado);
    final unidades = r.delNivel(id);
    final superado = nivelSuperado(r, estados, estado.practicas, id);
    final primera = estados[unidades.first.id]!;
    final abierto =
        primera.omitible || primera.estado != EstadoUnidad.bloqueada;
    final aprobadas = unidades
        .where((u) => estados[u.id]!.estado.alMenos(EstadoUnidad.aprobada))
        .length;
    return _fila(
      context,
      icono: superado
          ? Icons.check_circle_rounded
          : abierto
          ? Icons.play_circle_fill_rounded
          : Icons.lock_rounded,
      color: superado
          ? OL.verde
          : abierto
          ? OL.morado
          : OL.gris,
      detalle: superado
          ? tr('Superado')
          : primera.omitible
          ? tr('Opcional: está por debajo de tu nivel')
          : abierto
          ? tr('{hechas} de {total} clases', {'hechas': aprobadas, 'total': unidades.length})
          : tr('Termina el nivel anterior o aprueba su prueba'),
      onTap: () => context.push('/ruta/$id'),
    );
  }

  Widget _fila(
    BuildContext context, {
    required IconData icono,
    required Color color,
    required String detalle,
    required VoidCallback? onTap,
  }) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Tarjeta(
      onTap: onTap,
      color: onTap == null ? OL.fondo : OL.blanco,
      sombra: onTap != null,
      child: Row(
        children: [
          Icon(icono, color: color, size: 34),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  tr('Nivel {n} · {cefr}', {'n': numero, 'cefr': cefr}),
                  style: const TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                Text(
                  detalle,
                  style: const TextStyle(color: OL.gris, fontSize: 14),
                ),
              ],
            ),
          ),
          if (onTap != null)
            const Icon(Icons.chevron_right_rounded, color: OL.gris),
        ],
      ),
    ),
  );
}
