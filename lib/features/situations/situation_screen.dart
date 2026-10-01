import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/content/catalog.dart';
import '../../core/content/situaciones.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/situation_illustrations.dart';
import '../../shared/widgets/widgets.dart';

/// Una situación en su tramo (Básico, Intermedio o Avanzado según el nivel
/// del alumno): objetivos para practicar con el tutor IA (chat o
/// videollamada), palabras, frases útiles y la prueba del tramo.
class SituationScreen extends ConsumerStatefulWidget {
  const SituationScreen({super.key, required this.id});
  final int id;

  @override
  ConsumerState<SituationScreen> createState() => _SituationScreenState();
}

class _SituationScreenState extends ConsumerState<SituationScreen> {
  /// Tramo que el alumno está mirando (por defecto, el de su nivel).
  Tramo? visto;

  @override
  void dispose() {
    VozNube.instancia.parar();
    super.dispose();
  }

  void _oir(String texto, String idioma) =>
      VozNube.instancia.reproducir(texto, idioma);

  void _chat(ObjetivoSituacion o) => context.push(
    '/chat?situacion=${widget.id}&objetivo=${o.id}&modo=practica',
  );

  void _llamada(ObjetivoSituacion o) {
    if (!kIsWeb) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('La videollamada está disponible en la versión web.'),
        ),
      );
      return;
    }
    context.push('/avatar/lumo?tema=${widget.id}&objetivo=${o.id}');
  }

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final nivel = ref.watch(nivelAlumnoProvider);
    final sit = situacion(widget.id.clamp(1, situaciones.length));
    final contenido = ref.watch(situacionesProvider(s.idiomaMeta));
    return Scaffold(
      appBar: AppBar(title: Text(sit.nombre)),
      body: Movil(
        child: contenido.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (_, _) => Center(
            child: TextButton(
              onPressed: () =>
                  ref.invalidate(situacionesProvider(s.idiomaMeta)),
              child: const Text('No se pudo cargar. Reintentar'),
            ),
          ),
          data: (todas) {
            final c = todas?[widget.id];
            if (c == null) return _SinContenido(nombre: sit.nombre);
            final propio = Tramo.deNivel(nivel);
            final tramo = visto ?? propio;
            final t = c.tramo(tramo);
            final estado = estadoTramo(s.practicas, s.idiomaMeta, c, tramo);
            return Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Expanded(
                  child: ListView(
                    padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
                    children: [
                      SituationIllustrations(widget.id),
                      const SizedBox(height: 14),
                      _SelectorTramo(
                        nivel: nivel,
                        propio: propio,
                        actual: tramo,
                        completado: (x) => estadoTramo(
                          s.practicas,
                          s.idiomaMeta,
                          c,
                          x,
                        ).completado,
                        onElegir: (x) => setState(() => visto = x),
                      ),
                      const SizedBox(height: 12),
                      _Avance(estado: estado),
                      const SizedBox(height: 20),
                      const TituloSeccion('Objetivos'),
                      const SizedBox(height: 4),
                      const Text(
                        'Practica cada objetivo con tu tutor, por chat o en videollamada.',
                        style: TextStyle(color: OL.gris, fontSize: 14),
                      ),
                      const SizedBox(height: 10),
                      for (final o in t.objetivos)
                        _TarjetaObjetivo(
                          objetivo: o,
                          practicado: s.practicas.containsKey(
                            claveObjetivoSituacion(
                              s.idiomaMeta,
                              widget.id,
                              o.id,
                            ),
                          ),
                          onOir: () => _oir(o.frase, s.idiomaMeta),
                          onChat: () => _chat(o),
                          onLlamada: () => _llamada(o),
                        ),
                      const SizedBox(height: 14),
                      const TituloSeccion('Palabras'),
                      const SizedBox(height: 10),
                      for (final p in t.vocabulario)
                        _Linea(
                          titulo: p.en,
                          traduccion: p.es,
                          ejemplo: p.ejemplo,
                          onOir: () => _oir(p.en, s.idiomaMeta),
                        ),
                      const SizedBox(height: 14),
                      const TituloSeccion('Frases útiles'),
                      const SizedBox(height: 10),
                      for (final f in t.frases)
                        _Linea(
                          titulo: f.en,
                          traduccion: f.es,
                          onOir: () => _oir(f.en, s.idiomaMeta),
                        ),
                    ],
                  ),
                ),
                _PiePrueba(
                  estado: estado,
                  onPrueba: () => context.push(
                    '/situacion/${widget.id}/prueba?tramo=${tramo.name}',
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}

class _SinContenido extends StatelessWidget {
  const _SinContenido({required this.nombre});
  final String nombre;

  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.all(20),
    children: [
      Text(
        'Las situaciones guiadas de este idioma están en preparación. Mientras tanto, practica «$nombre» con tu tutor.',
        style: const TextStyle(fontSize: 17, height: 1.4),
      ),
      const SizedBox(height: 16),
      BotonPrincipal(
        onPressed: () => context.push('/chat'),
        child: const Text('HABLAR CON MI TUTOR'),
      ),
    ],
  );
}

/// Básico · Intermedio · Avanzado. Los superiores se ven bloqueados con el
/// nivel en que se abren; nunca se elige un nivel.
class _SelectorTramo extends StatelessWidget {
  const _SelectorTramo({
    required this.nivel,
    required this.propio,
    required this.actual,
    required this.completado,
    required this.onElegir,
  });
  final int nivel;
  final Tramo propio, actual;
  final bool Function(Tramo) completado;
  final ValueChanged<Tramo> onElegir;

  @override
  Widget build(BuildContext context) => Row(
    children: [
      for (final t in Tramo.values) ...[
        if (t != Tramo.basico) const SizedBox(width: 8),
        Expanded(
          child: Semantics(
            button: true,
            selected: t == actual,
            child: InkWell(
              borderRadius: BorderRadius.circular(14),
              onTap: t.abiertoPara(nivel)
                  ? () => onElegir(t)
                  : () => ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(
                          '${t.nombre} se abre al llegar al Nivel ${t.nivelMinimo}.',
                        ),
                      ),
                    ),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 10),
                decoration: BoxDecoration(
                  color: t == actual ? OL.moradoSuave : OL.blanco,
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(
                    color: t == actual ? OL.morado : OL.grisClaro,
                    width: 2,
                  ),
                ),
                child: Column(
                  children: [
                    Icon(
                      !t.abiertoPara(nivel)
                          ? Icons.lock_rounded
                          : completado(t)
                          ? Icons.check_circle_rounded
                          : t == propio
                          ? Icons.star_rounded
                          : Icons.circle_outlined,
                      size: 20,
                      color: !t.abiertoPara(nivel)
                          ? OL.gris
                          : completado(t)
                          ? OL.verde
                          : OL.morado,
                    ),
                    const SizedBox(height: 2),
                    Text(
                      t.nombre,
                      style: TextStyle(
                        fontWeight: FontWeight.w800,
                        fontSize: 14,
                        color: t.abiertoPara(nivel) ? OL.texto : OL.gris,
                      ),
                    ),
                    Text(
                      t == propio ? 'Tu nivel' : t.niveles,
                      style: const TextStyle(fontSize: 11, color: OL.gris),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    ],
  );
}

class _Avance extends StatelessWidget {
  const _Avance({required this.estado});
  final EstadoTramo estado;

  @override
  Widget build(BuildContext context) => Tarjeta(
    color: estado.completado ? OL.verdeSuave : OL.blanco,
    sombra: false,
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          estado.completado ? '¡Tramo completado!' : 'Tu avance',
          style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 16),
        ),
        Text(
          '${estado.objetivosPracticados} de ${estado.totalObjetivos} objetivos practicados · '
          'prueba ${estado.pruebaAprobada ? 'aprobada' : 'pendiente'}',
          style: const TextStyle(color: OL.gris, fontSize: 13),
        ),
        const SizedBox(height: 8),
        BarraProgreso(estado.progreso, alto: 8),
      ],
    ),
  );
}

class _TarjetaObjetivo extends StatelessWidget {
  const _TarjetaObjetivo({
    required this.objetivo,
    required this.practicado,
    required this.onOir,
    required this.onChat,
    required this.onLlamada,
  });
  final ObjetivoSituacion objetivo;
  final bool practicado;
  final VoidCallback onOir, onChat, onLlamada;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Tarjeta(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            children: [
              Icon(
                practicado ? Icons.check_circle_rounded : Icons.flag_outlined,
                color: practicado ? OL.verde : OL.morado,
              ),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  objetivo.titulo,
                  style: const TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.w900,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          InkWell(
            onTap: onOir,
            borderRadius: BorderRadius.circular(10),
            child: Row(
              children: [
                const Icon(Icons.volume_up_rounded, color: OL.morado, size: 20),
                const SizedBox(width: 6),
                Expanded(
                  child: Text(
                    objetivo.frase,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
              ],
            ),
          ),
          Text(
            objetivo.traduccion,
            style: const TextStyle(color: OL.gris, fontSize: 14),
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: onChat,
                  icon: const Icon(Icons.chat_bubble_outline_rounded),
                  label: const Text('Chat'),
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: onLlamada,
                  icon: const Icon(Icons.videocam_outlined),
                  label: const Text('Videollamada'),
                ),
              ),
            ],
          ),
        ],
      ),
    ),
  );
}

class _Linea extends StatelessWidget {
  const _Linea({
    required this.titulo,
    required this.traduccion,
    this.ejemplo,
    required this.onOir,
  });
  final String titulo, traduccion;
  final String? ejemplo;
  final VoidCallback onOir;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 8),
    child: Tarjeta(
      sombra: false,
      onTap: onOir,
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.only(top: 2),
            child: Icon(Icons.volume_up_rounded, color: OL.morado, size: 20),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  titulo,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                Text(
                  traduccion,
                  style: const TextStyle(color: OL.gris, fontSize: 14),
                ),
                if (ejemplo != null) ...[
                  const SizedBox(height: 4),
                  Text(
                    ejemplo!,
                    style: const TextStyle(
                      fontSize: 14,
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    ),
  );
}

class _PiePrueba extends StatelessWidget {
  const _PiePrueba({required this.estado, required this.onPrueba});
  final EstadoTramo estado;
  final VoidCallback onPrueba;

  @override
  Widget build(BuildContext context) {
    final nota = estado.mejorNota;
    return DecoratedBox(
      decoration: const BoxDecoration(
        color: OL.fondo,
        border: Border(top: BorderSide(color: OL.grisClaro)),
      ),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(20, 4, 20, 12),
        child: BotonPrincipal(
          onPressed: onPrueba,
          child: Text(
            nota == null
                ? 'HACER LA PRUEBA'
                : 'REPETIR LA PRUEBA · MEJOR ${nota.$1}/${nota.$2}',
          ),
        ),
      ),
    );
  }
}
