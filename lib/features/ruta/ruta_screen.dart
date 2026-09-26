import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/dominio.dart';
import '../../core/aprendizaje/modelos.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/content/curriculum.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/mascot_coach.dart';
import '../../shared/widgets/widgets.dart';

/// Ruta de Fundamentos (nivel 0) del idioma que estudia el alumno.
class RutaScreen extends ConsumerWidget {
  const RutaScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final ruta = ref.watch(rutaProvider(s.idiomaMeta));
    final nombre = idioma(s.idiomaMeta).nombre;
    return Scaffold(
      appBar: AppBar(
        title: Text('Fundamentos de $nombre'),
        leading: IconButton(
          tooltip: 'Volver',
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/aprender'),
        ),
      ),
      body: Movil(
        child: ruta.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (_, _) => const Center(child: Text('No se pudo cargar la ruta.')),
          data: (r) => r == null
              ? _SinRuta(nombre: nombre)
              : _Ruta(ruta: r, estado: s),
        ),
      ),
    );
  }
}

class _SinRuta extends StatelessWidget {
  const _SinRuta({required this.nombre});
  final String nombre;
  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.all(20),
    children: [
      Text(
        'La ruta de fundamentos de $nombre está en preparación.',
        style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
      ),
      const SizedBox(height: 16),
      FilledButton(
        onPressed: () => context.go('/aprender'),
        child: const Text('IR A APRENDER'),
      ),
    ],
  );
}

class _Ruta extends StatelessWidget {
  const _Ruta({required this.ruta, required this.estado});
  final RutaCargada ruta;
  final ProgressState estado;

  @override
  Widget build(BuildContext context) {
    final cadena = cadenaDelAlumno(estado, ruta.curso);
    String t(TextoApoyo? x) => x?.en(cadena) ?? '';
    final unidades = ruta.delNivel('f0');
    final estados = estadosRuta(ruta, estado.practicas);
    final recomendada = unidadRecomendada(ruta, estados);
    final aprobadas = unidades
        .where((u) => estados[u.id]!.estado.alMenos(EstadoUnidad.aprobada))
        .length;
    final completo = nivelAprobado(ruta, estados, 'f0');
    final hayLeccionesExtra = leccionesDe(0).isNotEmpty;
    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
      children: [
        MascotCoach(
          message: completo
              ? '¡Terminaste los fundamentos! Repasa cuando te lo pida y sigue en el Nivel 1.'
              : 'Primero te enseño con ejemplos. Después practicas y, al final, compruebas lo que sabes.',
        ),
        Row(
          children: [
            Expanded(
              child: Text(
                t(ruta.curso.modulos.first.titulo),
                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w900),
              ),
            ),
            if (ruta.curso.revisionInicial)
              const Tooltip(
                message:
                    'Contenido nuevo pendiente de revisión por hablantes nativos.',
                child: Etiqueta(
                  'Versión inicial',
                  color: OL.naranja,
                  fondo: OL.naranjaSuave,
                  icono: Icons.science_outlined,
                ),
              ),
          ],
        ),
        const SizedBox(height: 8),
        Text(
          '$aprobadas de ${unidades.length} unidades aprobadas · Pre-A1',
          style: const TextStyle(color: OL.gris, fontSize: 16),
        ),
        const SizedBox(height: 8),
        BarraProgreso(unidades.isEmpty ? 0 : aprobadas / unidades.length, alto: 8),
        const SizedBox(height: 18),
        if (recomendada != null)
          _Destacada(
            unidad: recomendada,
            info: estados[recomendada.id]!,
            titulo: t(recomendada.titulo),
            objetivo: t(recomendada.objetivo),
          ),
        if (completo)
          Padding(
            padding: const EdgeInsets.only(bottom: 16),
            child: Tarjeta(
              color: OL.verdeSuave,
              borde: OL.verde,
              onTap: () => context.go('/aprender'),
              child: const Row(
                children: [
                  Icon(Icons.emoji_events_outlined, color: OL.verde, size: 32),
                  SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'Fundamentos completados. Continúa en el Nivel 1.',
                      style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800),
                    ),
                  ),
                  Icon(Icons.chevron_right_rounded),
                ],
              ),
            ),
          ),
        for (final u in unidades)
          Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: _FilaUnidad(
              unidad: u,
              info: estados[u.id]!,
              titulo: t(u.titulo),
              objetivo: t(u.objetivo),
              previa: u.prerequisitos.isEmpty
                  ? null
                  : t(ruta.unidad(u.prerequisitos.first)?.titulo),
            ),
          ),
        const SizedBox(height: 8),
        const Text(
          'Aprobar una unidad no es dominarla: la marcamos como dominada cuando la recuerdas en un repaso días después.',
          style: TextStyle(color: OL.gris, fontSize: 15, height: 1.4),
        ),
        if (hayLeccionesExtra) ...[
          const SizedBox(height: 12),
          TextButton.icon(
            onPressed: () => context.push('/aprender/nivel/0'),
            icon: const Icon(Icons.library_books_outlined),
            label: const Text('Práctica extra: lecciones del Nivel 0'),
          ),
        ],
      ],
    );
  }
}

String etiquetaEstado(InfoUnidad info) {
  if (info.repasoPendiente) return 'Repaso pendiente';
  return switch (info.estado) {
    EstadoUnidad.bloqueada => 'Bloqueada',
    EstadoUnidad.disponible => 'Disponible',
    EstadoUnidad.enCurso => 'En curso',
    EstadoUnidad.practicada => 'Practicada · falta comprobar',
    EstadoUnidad.aprobada => 'Aprobada',
    EstadoUnidad.dominada => 'Dominada',
  };
}

IconData iconoEstado(InfoUnidad info) {
  if (info.repasoPendiente) return Icons.replay_rounded;
  return switch (info.estado) {
    EstadoUnidad.bloqueada => Icons.lock_outline,
    EstadoUnidad.disponible => Icons.play_circle_outline,
    EstadoUnidad.enCurso => Icons.timelapse_rounded,
    EstadoUnidad.practicada => Icons.fact_check_outlined,
    EstadoUnidad.aprobada => Icons.check_circle_outline,
    EstadoUnidad.dominada => Icons.workspace_premium_outlined,
  };
}

class _Destacada extends StatelessWidget {
  const _Destacada({
    required this.unidad,
    required this.info,
    required this.titulo,
    required this.objetivo,
  });
  final UnidadRuta unidad;
  final InfoUnidad info;
  final String titulo, objetivo;
  @override
  Widget build(BuildContext context) {
    final repaso = info.repasoPendiente &&
        info.estado.alMenos(EstadoUnidad.aprobada);
    final destino = repaso
        ? '/fundamentos/unidad/${unidad.id}?modo=repaso'
        : '/fundamentos/unidad/${unidad.id}';
    return Padding(
      padding: const EdgeInsets.only(bottom: 18),
      child: Tarjeta(
        color: OL.moradoSuave,
        borde: OL.morado,
        onTap: () => context.push(destino),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              repaso
                  ? 'Toca repasar'
                  : info.estado == EstadoUnidad.disponible
                  ? 'Siguiente paso'
                  : 'Continúa',
              style: const TextStyle(color: OL.morado, fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 6),
            Text(
              titulo,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900),
            ),
            const SizedBox(height: 6),
            Text(objetivo, style: const TextStyle(fontSize: 17, height: 1.4)),
            const SizedBox(height: 14),
            FilledButton(
              onPressed: () => context.push(destino),
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 12),
                child: Text(repaso ? 'REPASAR' : 'EMPEZAR'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _FilaUnidad extends StatelessWidget {
  const _FilaUnidad({
    required this.unidad,
    required this.info,
    required this.titulo,
    required this.objetivo,
    required this.previa,
  });
  final UnidadRuta unidad;
  final InfoUnidad info;
  final String titulo, objetivo;
  final String? previa;
  @override
  Widget build(BuildContext context) {
    final bloqueada = info.estado == EstadoUnidad.bloqueada;
    final hecha = info.estado.alMenos(EstadoUnidad.aprobada);
    final color = bloqueada ? OL.gris : hecha ? OL.verde : OL.morado;
    return Semantics(
      button: true,
      label: '$titulo. ${etiquetaEstado(info)}',
      child: Tarjeta(
        onTap: () => context.push('/fundamentos/unidad/${unidad.id}'),
        child: Row(
          children: [
            Icon(iconoEstado(info), color: color, size: 30),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '${unidad.orden}. $titulo',
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    bloqueada && previa != null
                        ? 'Puedes leerla. Para practicar, primero «$previa».'
                        : objetivo,
                    style: const TextStyle(color: OL.gris, fontSize: 15, height: 1.3),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    etiquetaEstado(info),
                    style: TextStyle(color: color, fontWeight: FontWeight.w800),
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
}
