import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../shared/widgets/daily_activities.dart';
import '../../shared/widgets/mascot_coach.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/content/catalog.dart';
import '../../core/content/situaciones.dart';
import '../../core/content/fotos.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Práctica libre con IA: 50 situaciones + conversación libre (REQUERIMIENTOS §6-7).
class PracticeScreen extends ConsumerStatefulWidget {
  const PracticeScreen({super.key});

  @override
  ConsumerState<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends ConsumerState<PracticeScreen> {
  String categoria = 'Todas';
  String busqueda = '';

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final t = tutor(s.tutorId);
    final tramo = Tramo.deNivel(ref.watch(nivelAlumnoProvider));
    final contenido = ref
        .watch(situacionesProvider(s.idiomaMeta))
        .valueOrNull;
    EstadoTramo? estado(int id) {
      final c = contenido?[id];
      return c == null ? null : estadoTramo(s.practicas, s.idiomaMeta, c, tramo);
    }

    final categorias = [
      'Todas',
      ...{for (final x in situaciones) x.categoria},
    ];
    final lista = situaciones.where((x) {
      final okCat = categoria == 'Todas' || x.categoria == categoria;
      final okBusq =
          busqueda.isEmpty ||
          x.nombre.toLowerCase().contains(busqueda.toLowerCase());
      return okCat && okBusq;
    }).toList();

    void abrir(String ruta) {
      if (s.trialAgotado) {
        context.push('/planes');
      } else {
        context.push(ruta);
      }
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Práctica libre con IA'),
        actions: [
          TextButton.icon(
            onPressed: () => context.push('/tutores'),
            icon: CircleAvatar(
              radius: 12,
              backgroundColor: t.color,
              child: Text(
                t.nombre[0],
                style: const TextStyle(
                  color: OL.blanco,
                  fontSize: 14,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ),
            label: Text(t.nombre),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
        children: [
          const MascotCoach(
            listening: true,
            message: 'Elige una situación y ensaya a tu ritmo. Puedes escuchar, repetir y pedir ayuda.',
          ),
          HeroCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  'Conversación libre',
                  style: TextStyle(
                    color: OL.blanco,
                    fontSize: 22,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  'Habla de lo que quieras. La IA se adapta al nivel ${s.nivelActual} y a lo que necesitas reforzar.',
                  style: const TextStyle(
                    color: Color(0xFFE0D8FF),
                    fontSize: 16,
                    height: 1.5,
                  ),
                ),
                const SizedBox(height: 14),
                for (final row in [
                  [('Mi día', 49), ('Trabajo', 21)],
                  [('Viajes', 39), ('Noticias', 50)],
                ])
                  Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Row(
                      children: [
                        for (var i = 0; i < row.length; i++) ...[
                          if (i > 0) const SizedBox(width: 8),
                          Expanded(
                            child: FilledButton(
                              style: FilledButton.styleFrom(
                                backgroundColor: OL.blanco,
                                foregroundColor: OL.morado,
                              ),
                              onPressed: () => abrir('/situacion/${row[i].$2}'),
                              child: Text(row[i].$1),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                const SizedBox(height: 4),
                FilledButton.icon(
                  style: FilledButton.styleFrom(
                    backgroundColor: OL.blanco,
                    foregroundColor: OL.morado,
                    minimumSize: const Size.fromHeight(48),
                  ),
                  onPressed: () => abrir('/chat'),
                  icon: const Icon(Icons.mic_rounded),
                  label: const Text('Hablar con mi tutor'),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Tarjeta(
            onTap: () => abrir('/tutores'),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  'Practica con un tutor de IA',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
                ),
                const SizedBox(height: 8),
                const Text(
                  'Elige un tutor para tu idioma. Conversa con voz, gestos y refuerzo adaptado a tu nivel.',
                ),
                const SizedBox(height: 12),
                FilledButton.icon(
                  onPressed: () => abrir('/tutores'),
                  icon: const Icon(Icons.record_voice_over),
                  label: const Text('Elegir mi tutor'),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          const TituloSeccion('50 situaciones'),
          Text(
            'Tu tramo: ${tramo.nombre} · ${tramo.niveles}',
            style: const TextStyle(
              fontSize: 14,
              color: OL.morado,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            'Cada situación tiene tres tramos: Básico, Intermedio y Avanzado. Ves el de tu nivel y puedes repasar los anteriores.',
            style: TextStyle(color: OL.gris, fontSize: 14, height: 1.4),
          ),
          const SizedBox(height: 12),
          TextField(
            onChanged: (v) => setState(() => busqueda = v),
            decoration: const InputDecoration(
              hintText: 'Buscar situación...',
              prefixIcon: Icon(Icons.search),
            ),
          ),
          const SizedBox(height: 10),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              for (final c in categorias)
                ChoiceChip(
                  label: Text(c),
                  selected: categoria == c,
                  onSelected: (_) => setState(() => categoria = c),
                  materialTapTargetSize: MaterialTapTargetSize.padded,
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 10,
                  ),
                  selectedColor: OL.moradoClaro,
                  labelStyle: TextStyle(
                    color: categoria == c ? OL.morado : OL.texto,
                    fontWeight: FontWeight.w700,
                    fontSize: 14,
                  ),
                  side: BorderSide(
                    color: categoria == c ? OL.morado : OL.grisClaro,
                  ),
                  backgroundColor: OL.blanco,
                ),
            ],
          ),
          const SizedBox(height: 12),
          LayoutBuilder(
            builder: (context, constraints) {
              final largeText = MediaQuery.textScalerOf(context).scale(16) > 21;
              final columns = constraints.maxWidth < 340 || largeText ? 1 : 2;
              final width =
                  (constraints.maxWidth - (columns - 1) * 12) / columns;
              return Wrap(
                spacing: 12,
                runSpacing: 16,
                children: [
                  for (var i = 0; i < lista.length; i++)
                    SizedBox(
                      width: width,
                      child: Builder(
                        builder: (_) {
                          final x = lista[i];
                          final foto = fotoSituacion(x.id);
                          return Tarjeta(
                            onTap: () => abrir('/situacion/${x.id}'),
                            padding: EdgeInsets.zero,
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(16),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  AspectRatio(
                                    aspectRatio: 1.5,
                                    child: Stack(
                                      fit: StackFit.expand,
                                      children: [
                                        if (foto != null)
                                          Image.asset(foto, fit: BoxFit.cover)
                                        else
                                          Container(
                                            color: x.color.withValues(
                                              alpha: 0.12,
                                            ),
                                          ),
                                        Positioned(
                                          left: 8,
                                          top: 8,
                                          child: IconoCuadro(
                                            x.icono,
                                            color: x.color,
                                            tamano: 30,
                                            relleno: true,
                                          ),
                                        ),
                                        if (estado(x.id)?.completado ??
                                            false)
                                          const Positioned(
                                            right: 8,
                                            top: 8,
                                            child: CircleAvatar(
                                              radius: 14,
                                              backgroundColor: OL.verde,
                                              child: Icon(
                                                Icons.check_rounded,
                                                color: OL.blanco,
                                                size: 18,
                                              ),
                                            ),
                                          ),
                                      ],
                                    ),
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.fromLTRB(
                                      10,
                                      8,
                                      10,
                                      10,
                                    ),
                                    child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          x.nombre,
                                          style: const TextStyle(
                                            fontWeight: FontWeight.w800,
                                            fontSize: 17,
                                          ),
                                        ),
                                        Text(
                                          estado(x.id)?.empezado ?? false
                                              ? '${x.categoria} · ${(estado(x.id)!.progreso * 100).round()} %'
                                              : x.categoria,
                                          style: const TextStyle(
                                            color: OL.gris,
                                            fontSize: 14,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                ],
              );
            },
          ),
          if (lista.isEmpty)
            const Tarjeta(
              child: Text(
                'No encontramos esa situación. Prueba otra palabra o categoría.',
              ),
            ),
          const SizedBox(height: 20),
          const TituloSeccion('Actividades diarias'),
          const SizedBox(height: 4),
          const Text(
            'Práctica complementaria al curso.',
            style: TextStyle(color: OL.gris, fontSize: 14),
          ),
          const SizedBox(height: 10),
          const DailyActivities(),
        ],
      ),
    );
  }
}
