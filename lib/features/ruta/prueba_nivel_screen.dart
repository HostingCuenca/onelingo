import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/dominio.dart';
import '../../core/aprendizaje/modelos.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/efectos.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import 'item_view.dart';
import '../../core/i18n/i18n.dart';

/// Prueba para saltar un nivel: 20 preguntas de evaluación repartidas por
/// todo el nivel; con 16 aciertos el nivel cuenta como superado y se abre el
/// siguiente. Sin Lumo y sin reintentos, como una prueba de verdad.
class PruebaNivelRutaScreen extends ConsumerStatefulWidget {
  const PruebaNivelRutaScreen({super.key, required this.nivel});
  final String nivel;

  @override
  ConsumerState<PruebaNivelRutaScreen> createState() =>
      _PruebaNivelRutaScreenState();
}

enum _Fase { intro, pregunta, resultado }

class _PruebaNivelRutaScreenState extends ConsumerState<PruebaNivelRutaScreen> {
  _Fase fase = _Fase.intro;
  List<Item> items = const [];
  int indice = 0, aciertos = 0;
  bool respondida = false;

  void _empezar(RutaCargada ruta) {
    setState(() {
      items = itemsPruebaNivel(ruta, widget.nivel, Random());
      indice = 0;
      aciertos = 0;
      respondida = false;
      fase = _Fase.pregunta;
    });
  }

  void _siguiente(RutaCargada ruta) {
    if (indice + 1 < items.length) {
      setState(() {
        indice++;
        respondida = false;
      });
      return;
    }
    final aprobada =
        aciertos >= aciertosPruebaNivel * items.length / preguntasPruebaNivel;
    ref
        .read(progressProvider.notifier)
        .registrarPractica(ClaveRuta.pruebaNivel(ruta.curso.idioma, widget.nivel), {
          'idioma': ruta.curso.idioma,
          'skill': 'evaluacion',
          'tipo': 'prueba_nivel',
          'nivel': widget.nivel,
          'aciertos': aciertos,
          'total': items.length,
          // Una vez aprobada queda aprobada aunque se repita después.
          'aprobada':
              aprobada ||
              pruebaNivelAprobada(
                ref.read(progressProvider).practicas,
                ruta.curso.idioma,
                widget.nivel,
              ),
          'correcta': aprobada,
        });
    aprobada ? Efectos.completado() : Efectos.incorrecto();
    setState(() => fase = _Fase.resultado);
  }

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final ruta = ref.watch(rutaProvider(s.idiomaMeta)).valueOrNull;
    final datos = ruta?.curso.niveles
        .where((n) => n.id == widget.nivel)
        .firstOrNull;
    final nombreNivel = datos == null
        ? tr('este nivel')
        : tr('el Nivel {n}', {'n': datos.nivelInterno ?? ''});
    final nivelTitulo = datos == null
        ? tr('este nivel')
        : tr('Nivel {n}', {'n': datos.nivelInterno ?? ''});
    return Scaffold(
      appBar: AppBar(
        title: Text(tr('Prueba de {nivel}', {'nivel': nivelTitulo})),
        leading: IconButton(
          tooltip: tr('Salir'),
          icon: const Icon(Icons.close_rounded),
          onPressed: () => context.canPop()
              ? context.pop()
              : context.go('/ruta/${widget.nivel}'),
        ),
      ),
      body: Movil(
        child: ruta == null
            ? const Center(child: CircularProgressIndicator())
            : switch (fase) {
                _Fase.intro => _intro(ruta, nombreNivel),
                _Fase.pregunta => _pregunta(ruta, s),
                _Fase.resultado => _resultado(ruta, nombreNivel),
              },
      ),
    );
  }

  Widget _intro(RutaCargada ruta, String nombreNivel) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      Expanded(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 20),
          children: [
            const Icon(Icons.workspace_premium_rounded, color: OL.morado, size: 64),
            const SizedBox(height: 12),
            Text(
              tr('¿Ya dominas {nivel}?', {'nivel': nombreNivel}),
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w900),
            ),
            const SizedBox(height: 12),
            Text(
              tr(
                '{preguntas} preguntas de todo el nivel. Con '
                '{aciertos} aciertos lo das por superado y pasas al '
                'siguiente. Si no llegas, sigues aprendiendo donde estás: no '
                'pierdes nada y puedes intentarlo otra vez.',
                {
                  'preguntas': preguntasPruebaNivel,
                  'aciertos': aciertosPruebaNivel,
                },
              ),
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 16, height: 1.45),
            ),
          ],
        ),
      ),
      Padding(
        padding: const EdgeInsets.fromLTRB(20, 0, 20, 20),
        child: BotonPrincipal(
          onPressed: () => _empezar(ruta),
          child: Text(tr('EMPEZAR LA PRUEBA')),
        ),
      ),
    ],
  );

  Widget _pregunta(RutaCargada ruta, ProgressState s) {
    final item = items[indice];
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 12),
          child: Row(
            children: [
              Expanded(
                child: BarraProgreso((indice + 1) / items.length, alto: 8),
              ),
              const SizedBox(width: 12),
              Text(
                '${indice + 1} / ${items.length}',
                style: const TextStyle(color: OL.gris),
              ),
            ],
          ),
        ),
        Expanded(
          child: ItemView(
            key: ValueKey('${item.id}:$indice'),
            botonFijo: true,
            item: item,
            idioma: ruta.curso.idioma,
            cadena: cadenaDelAlumno(s, ruta.curso),
            guiada: false,
            permitirReintento: false,
            lumo: false,
            onComprobado: (correcta, _) {
              if (respondida) return;
              respondida = true;
              if (correcta) aciertos++;
            },
            onContinuar: () => _siguiente(ruta),
          ),
        ),
      ],
    );
  }

  Widget _resultado(RutaCargada ruta, String nombreNivel) {
    final aprobada =
        aciertos >= aciertosPruebaNivel * items.length / preguntasPruebaNivel;
    final siguiente = _nivelSiguiente(ruta);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Expanded(
          child: ListView(
            padding: const EdgeInsets.fromLTRB(20, 24, 20, 20),
            children: [
              Icon(
                aprobada
                    ? Icons.workspace_premium_rounded
                    : Icons.trending_up_rounded,
                color: aprobada ? OL.verde : OL.naranja,
                size: 72,
              ),
              const SizedBox(height: 12),
              Text(
                aprobada
                    ? tr('¡Superaste {nivel}!', {'nivel': nombreNivel})
                    : tr('Todavía no'),
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w900),
              ),
              const SizedBox(height: 8),
              Text(
                tr('{aciertos} de {total} aciertos.', {
                  'aciertos': aciertos,
                  'total': items.length,
                }),
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 12),
              Text(
                aprobada
                    ? tr('Este nivel queda superado y se abre el siguiente. Sus clases siguen disponibles para repasar.')
                    : tr(
                        'Necesitas {aciertos}. Sigue con las clases del nivel: cada una te acerca, y puedes repetir la prueba cuando quieras.',
                        {'aciertos': aciertosPruebaNivel},
                      ),
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 16, height: 1.45),
              ),
            ],
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 20),
          child: BotonPrincipal(
            onPressed: () => context.go(
              aprobada && siguiente != null
                  ? '/ruta/${siguiente.id}'
                  : '/ruta/${widget.nivel}',
            ),
            child: Text(
              aprobada && siguiente != null
                  ? tr('IR AL SIGUIENTE NIVEL')
                  : tr('VOLVER AL NIVEL'),
            ),
          ),
        ),
      ],
    );
  }

  NivelCurso? _nivelSiguiente(RutaCargada ruta) {
    final publicados = [
      for (final n in ruta.curso.niveles)
        if (n.estado == EstadoNivel.publicado && ruta.delNivel(n.id).isNotEmpty)
          n,
    ];
    final i = publicados.indexWhere((n) => n.id == widget.nivel);
    return i >= 0 && i + 1 < publicados.length ? publicados[i + 1] : null;
  }
}
