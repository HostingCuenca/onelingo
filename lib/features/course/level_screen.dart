import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/curriculum.dart';
import '../../core/content/fotos.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Un nivel: 20 unidades × 5 lecciones con desbloqueo progresivo + examen final.
class LevelScreen extends ConsumerWidget {
  const LevelScreen({super.key, required this.nivel});
  final int nivel;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final lvl = nivelDe(nivel);
    final total = totalLeccionesDe(nivel);
    final unidades = unidadesDe(nivel);
    final lecciones = leccionesDe(nivel);
    final examenListo = s.examenDesbloqueado(nivel);

    return Scaffold(
      appBar: AppBar(title: Text(nivel == 0 ? 'Fundamentos · empieza de cero' : 'Nivel $nivel · ${lvl.nombre}')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
        children: [
          HeroCard(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Etiqueta(nivel == 0 ? 'Antes del Nivel 1' : 'Nivel $nivel de 10', color: OL.morado, fondo: OL.blanco),
              const SizedBox(height: 10),
              Text(lvl.descripcion,
                  style: const TextStyle(color: OL.blanco, fontSize: 15, fontWeight: FontWeight.w700, height: 1.35)),
              const SizedBox(height: 12),
              Row(children: [
                Expanded(child: BarraProgreso(s.progresoNivel(nivel), color: OL.blanco, fondo: OL.moradoOscuro)),
                const SizedBox(width: 10),
                Text('${s.completadasEnNivel(nivel)}/$total',
                    style: const TextStyle(color: OL.blanco, fontWeight: FontWeight.w800)),
              ]),
            ]),
          ),
          const SizedBox(height: 18),
          for (final u in unidades) _UnidadCard(u: u, lecciones: lecciones, s: s),
          const SizedBox(height: 6),
          Tarjeta(
            color: examenListo ? OL.naranjaSuave : OL.blanco,
            onTap: examenListo ? () => context.push('/examen/$nivel') : null,
            child: Row(children: [
              IconoCuadro(examenListo ? Icons.workspace_premium_outlined : Icons.lock_outline,
                  color: examenListo ? OL.naranja : OL.gris),
              const SizedBox(width: 12),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(nivel == 0 ? 'Prueba de fundamentos' : 'Examen final del nivel', style: const TextStyle(fontWeight: FontWeight.w700)),
                  Text(
                    examenListo
                        ? 'Necesitas 65 % para desbloquear el Nivel ${nivel + 1}'
                        : 'Se desbloquea al completar las 100 lecciones',
                    style: const TextStyle(color: OL.gris, fontSize: 12),
                  ),
                ]),
              ),
              if (examenListo) const Icon(Icons.chevron_right, color: OL.gris),
            ]),
          ),
        ],
      ),
    );
  }
}

class _UnidadCard extends StatelessWidget {
  const _UnidadCard({required this.u, required this.lecciones, required this.s});
  final Unit u;
  final List<Lesson> lecciones;
  final ProgressState s;

  @override
  Widget build(BuildContext context) {
    final propias = lecciones.where((l) => l.unidad == u.numero).toList();
    final hechas = propias.where((l) => s.completadas.contains(l.id)).length;
    final tieneActual = propias.any((l) => s.estadoLeccion(l) == LessonState.actual);
    final bloqueada = !tieneActual && hechas == 0;

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Tarjeta(
        padding: EdgeInsets.zero,
        child: Theme(
          data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
          child: ExpansionTile(
            initiallyExpanded: tieneActual,
            tilePadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
            leading: fotoUnidad(u.nivel, u.numero) == null
                ? IconoCuadro(u.icono, color: bloqueada ? OL.gris : u.color)
                : ClipRRect(
                    borderRadius: BorderRadius.circular(12),
                    child: ColorFiltered(
                      colorFilter: bloqueada
                          ? const ColorFilter.mode(Colors.grey, BlendMode.saturation)
                          : const ColorFilter.mode(Colors.transparent, BlendMode.dst),
                      child: Image.asset(fotoUnidad(u.nivel, u.numero)!, width: 44, height: 44, fit: BoxFit.cover),
                    ),
                  ),
            title: Text('Unidad ${u.numero} · ${u.titulo}',
                style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: bloqueada ? OL.gris : OL.texto)),
            subtitle: Padding(
              padding: const EdgeInsets.only(top: 6),
              child: Row(children: [
                Expanded(child: BarraProgreso(hechas / propias.length, color: u.color, alto: 6)),
                const SizedBox(width: 8),
                Text('$hechas/${propias.length}', style: const TextStyle(fontSize: 11, color: OL.gris, fontWeight: FontWeight.w700)),
              ]),
            ),
            children: [
              for (final l in propias) _LeccionRow(l: l, estado: s.estadoLeccion(l), color: u.color, pct: s.puntuaciones[l.id]),
            ],
          ),
        ),
      ),
    );
  }
}

class _LeccionRow extends StatelessWidget {
  const _LeccionRow({required this.l, required this.estado, required this.color, this.pct});
  final Lesson l;
  final LessonState estado;
  final Color color;
  final int? pct;

  @override
  Widget build(BuildContext context) {
    final habilitada = estado != LessonState.bloqueada;
    return InkWell(
      borderRadius: BorderRadius.circular(12),
      onTap: habilitada ? () => context.push('/leccion/${l.id}') : null,
      child: Container(
        margin: const EdgeInsets.only(top: 8),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 10),
        decoration: BoxDecoration(
          color: estado == LessonState.actual ? color.withValues(alpha: 0.08) : OL.fondo,
          borderRadius: BorderRadius.circular(12),
          border: estado == LessonState.actual ? Border.all(color: color.withValues(alpha: 0.5), width: 1.5) : null,
        ),
        child: Row(children: [
          EstadoLeccionIcono(estado, numero: l.numero, color: color),
          const SizedBox(width: 12),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(l.titulo.split(': ').first,
                  style: TextStyle(fontWeight: FontWeight.w700, fontSize: 13, color: habilitada ? OL.texto : OL.gris)),
              Text('${l.subtitulo} · ${l.steps.length} ejercicios${pct != null ? ' · $pct %' : ''}',
                  style: const TextStyle(color: OL.gris, fontSize: 11)),
            ]),
          ),
          if (estado == LessonState.actual)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(99)),
              child: const Text('Ir', style: TextStyle(color: OL.blanco, fontWeight: FontWeight.w800, fontSize: 12)),
            )
          else if (estado == LessonState.completada)
            const Icon(Icons.replay, size: 18, color: OL.gris),
        ]),
      ),
    );
  }
}
