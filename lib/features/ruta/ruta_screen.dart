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

/// Ruta de un nivel (por defecto Fundamentos, nivel 0) del idioma que
/// estudia el alumno.
class RutaScreen extends ConsumerWidget {
  const RutaScreen({super.key, this.nivel = 'f0'});
  final String nivel;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final ruta = ref.watch(rutaProvider(s.idiomaMeta));
    final nombre = idioma(s.idiomaMeta).nombre;
    final r = ruta.valueOrNull;
    final nivelResuelto = r == null ? nivel : resolverNivelHistorico(r, nivel);
    final datosNivel = r?.curso.niveles
        .where((n) => n.id == nivelResuelto)
        .firstOrNull;
    final titulo = nivelResuelto == 'f0' || datosNivel == null
        ? 'Fundamentos de $nombre'
        : '${datosNivel.titulo.en(cadenaDelAlumno(s, r!.curso))} · $nombre';
    return Scaffold(
      appBar: AppBar(
        title: Text(titulo),
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
          error: (_, _) =>
              const Center(child: Text('No se pudo cargar la ruta.')),
          data: (r) => r == null
              ? _SinRuta(nombre: nombre)
              : _Ruta(
                  ruta: r,
                  estado: s,
                  nivel: resolverNivelHistorico(r, nivel),
                ),
        ),
      ),
    );
  }
}

/// Conserva enlaces guardados de la ruta inglesa anterior sin duplicar sus
/// 29 unidades. Ambos tramos A1 históricos aterrizan en el N1 editorial.
String resolverNivelHistorico(RutaCargada ruta, String solicitado) {
  if (ruta.delNivel(solicitado).isNotEmpty) return solicitado;
  if (ruta.curso.idioma == 'en' &&
      ruta.curso.usaEscalaCliente &&
      const {'a1-1', 'a1-2'}.contains(solicitado) &&
      ruta.delNivel('n1').isNotEmpty) {
    return 'n1';
  }
  return solicitado;
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
      BotonPrincipal(
        onPressed: () => context.go('/aprender'),
        child: const Text('IR A APRENDER'),
      ),
    ],
  );
}

/// Primera unidad recomendable del nivel; si no hay, una con repaso pendiente.
UnidadRuta? recomendadaEnNivel(
  RutaCargada ruta,
  Map<String, InfoUnidad> e,
  String nivel,
) {
  final unidades = ruta.delNivel(nivel);
  for (final u in unidades) {
    final i = e[u.id]!;
    if (!i.omitible &&
        i.estado != EstadoUnidad.bloqueada &&
        !i.estado.alMenos(EstadoUnidad.aprobada)) {
      return u;
    }
  }
  for (final u in unidades) {
    if (e[u.id]!.repasoPendiente) return u;
  }
  return null;
}

/// Siguiente nivel publicado con unidades, o null.
NivelCurso? nivelSiguiente(RutaCargada ruta, String nivel) {
  final publicados = [
    for (final n in ruta.curso.niveles)
      if (n.estado == EstadoNivel.publicado && ruta.delNivel(n.id).isNotEmpty)
        n,
  ];
  final i = publicados.indexWhere((n) => n.id == nivel);
  return i >= 0 && i + 1 < publicados.length ? publicados[i + 1] : null;
}

class _Ruta extends StatelessWidget {
  const _Ruta({required this.ruta, required this.estado, required this.nivel});
  final RutaCargada ruta;
  final ProgressState estado;
  final String nivel;

  @override
  Widget build(BuildContext context) {
    final cadena = cadenaDelAlumno(estado, ruta.curso);
    String t(TextoApoyo? x) => x?.en(cadena) ?? '';
    final unidades = ruta.delNivel(nivel);
    final estados = estadosAlumno(ruta, estado);
    final recomendada = recomendadaEnNivel(ruta, estados, nivel);
    final siguienteNivel = nivelSiguiente(ruta, nivel);
    final destinoSiguiente = siguienteNivel == null
        ? '/aprender'
        : '/ruta/${siguienteNivel.id}';
    final modulos = [
      for (final m in ruta.curso.modulos)
        if (m.nivel == nivel) m,
    ];
    final cefr =
        ruta.curso.niveles.where((n) => n.id == nivel).firstOrNull?.cefr ?? '';
    final aprobadas = unidades
        .where((u) => estados[u.id]!.estado.alMenos(EstadoUnidad.aprobada))
        .length;
    final completo = nivelAprobado(ruta, estados, nivel);
    final hayLeccionesExtra = nivel == 'f0' && leccionesDe(0).isNotEmpty;
    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
      children: [
        MascotCoach(
          message: completo
              ? '¡Terminaste este nivel! Repasa cuando te lo pida y sigue avanzando.'
              : 'Primero te enseño con ejemplos. Después practicas y, al final, compruebas lo que sabes.',
        ),
        Row(
          children: [
            Expanded(
              child: Text(
                t(
                  modulos.length == 1
                      ? modulos.first.titulo
                      : ruta.curso.niveles
                            .firstWhere((n) => n.id == nivel)
                            .titulo,
                ),
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.w900,
                ),
              ),
            ),
            if (ruta.curso.revisionInicial)
              const Tooltip(
                message: 'Contenido nuevo pendiente de revisión por hablantes nativos.',
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
          '$aprobadas de ${unidades.length} unidades aprobadas · $cefr',
          style: const TextStyle(color: OL.gris, fontSize: 16),
        ),
        const SizedBox(height: 8),
        BarraProgreso(
          unidades.isEmpty ? 0 : aprobadas / unidades.length,
          alto: 8,
        ),
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
              onTap: () => siguienteNivel == null
                  ? context.go(destinoSiguiente)
                  : context.push(destinoSiguiente),
              child: Row(
                children: [
                  const Icon(
                    Icons.emoji_events_outlined,
                    color: OL.verde,
                    size: 32,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      siguienteNivel == null
                          ? 'Nivel completado. Sigue practicando en Aprender.'
                          : 'Nivel completado. Continúa: ${t(siguienteNivel.titulo)}.',
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ),
                  const Icon(Icons.chevron_right_rounded),
                ],
              ),
            ),
          ),
        for (final u in unidades) ...[
          if (modulos.length > 1 &&
              (u == unidades.first ||
                  unidades[unidades.indexOf(u) - 1].modulo != u.modulo))
            Padding(
              padding: const EdgeInsets.fromLTRB(4, 8, 4, 10),
              child: Text(
                t(modulos.firstWhere((m) => m.id == u.modulo).titulo),
                style: const TextStyle(
                  fontSize: 19,
                  fontWeight: FontWeight.w900,
                ),
              ),
            ),
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
        ],
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
  if (info.omitible && !info.estado.alMenos(EstadoUnidad.practicada)) {
    return 'Opcional · según tu nivel';
  }
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
    final repaso =
        info.repasoPendiente && info.estado.alMenos(EstadoUnidad.aprobada);
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
              style: const TextStyle(
                color: OL.morado,
                fontWeight: FontWeight.w800,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              titulo,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900),
            ),
            const SizedBox(height: 6),
            Text(objetivo, style: const TextStyle(fontSize: 17, height: 1.4)),
            const SizedBox(height: 14),
            BotonPrincipal(
              onPressed: () => context.push(destino),
              child: Text(repaso ? 'REPASAR' : 'EMPEZAR'),
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
    final color = bloqueada
        ? OL.gris
        : hecha
        ? OL.verde
        : OL.morado;
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
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    bloqueada && previa != null
                        ? 'Puedes leerla. Para practicar, primero «$previa».'
                        : objetivo,
                    style: const TextStyle(
                      color: OL.gris,
                      fontSize: 15,
                      height: 1.3,
                    ),
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
