import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/content/curriculum.dart';
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
    final categorias = ['Todas', ...{for (final x in situaciones) x.categoria}];
    final lista = situaciones.where((x) {
      final okCat = categoria == 'Todas' || x.categoria == categoria;
      final okBusq = busqueda.isEmpty || x.nombre.toLowerCase().contains(busqueda.toLowerCase());
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
            icon: CircleAvatar(radius: 12, backgroundColor: t.color, child: Text(t.nombre[0], style: const TextStyle(color: OL.blanco, fontSize: 12, fontWeight: FontWeight.w800))),
            label: Text(t.nombre),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
        children: [
          HeroCard(
            child: Row(children: [
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  const Text('Conversación libre', style: TextStyle(color: OL.blanco, fontSize: 20, fontWeight: FontWeight.w800)),
                  const SizedBox(height: 4),
                  Text('Habla de lo que quieras. La IA se adapta al Nivel ${s.nivelActual}.',
                      style: const TextStyle(color: Color(0xFFE0D8FF), fontSize: 13, height: 1.4)),
                  const SizedBox(height: 12),
                  Wrap(spacing: 6, runSpacing: 6, children: const [
                    Etiqueta('Mi día', color: OL.morado, fondo: OL.blanco),
                    Etiqueta('Trabajo', color: OL.morado, fondo: OL.blanco),
                    Etiqueta('Viajes', color: OL.morado, fondo: OL.blanco),
                    Etiqueta('Noticias', color: OL.morado, fondo: OL.blanco),
                  ]),
                ]),
              ),
              IconButton.filled(
                style: IconButton.styleFrom(backgroundColor: OL.blanco, foregroundColor: OL.morado, fixedSize: const Size(52, 52)),
                onPressed: () => abrir('/chat'),
                icon: const Icon(Icons.mic),
              ),
            ]),
          ),
          const SizedBox(height: 20),
          TituloSeccion('50 situaciones', accion: 'Nivel ${s.nivelActual} · ${nivel(s.nivelActual).nombre}'),
          const SizedBox(height: 4),
          const Text('Cada situación se adapta a tu nivel: no es lo mismo pedir en un restaurante en Nivel 1 que en Nivel 10.',
              style: TextStyle(color: OL.gris, fontSize: 12, height: 1.4)),
          const SizedBox(height: 12),
          TextField(
            onChanged: (v) => setState(() => busqueda = v),
            decoration: const InputDecoration(hintText: 'Buscar situación...', prefixIcon: Icon(Icons.search)),
          ),
          const SizedBox(height: 10),
          SizedBox(
            height: 36,
            child: ListView(
              scrollDirection: Axis.horizontal,
              children: [
                for (final c in categorias)
                  Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: ChoiceChip(
                      label: Text(c),
                      selected: categoria == c,
                      onSelected: (_) => setState(() => categoria = c),
                      selectedColor: OL.moradoClaro,
                      labelStyle: TextStyle(color: categoria == c ? OL.morado : OL.gris, fontWeight: FontWeight.w700, fontSize: 12),
                      side: BorderSide.none,
                      backgroundColor: OL.blanco,
                    ),
                  ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 2, mainAxisSpacing: 10, crossAxisSpacing: 10, childAspectRatio: 1.25),
            itemCount: lista.length,
            itemBuilder: (_, i) {
              final x = lista[i];
              final foto = fotoSituacion(x.id);
              return Tarjeta(
                onTap: () => abrir('/chat?situacion=${x.id}'),
                padding: EdgeInsets.zero,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(16),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Expanded(
                      child: Stack(fit: StackFit.expand, children: [
                        if (foto != null) Image.asset(foto, fit: BoxFit.cover) else Container(color: x.color.withValues(alpha: 0.12)),
                        Positioned(left: 8, top: 8, child: IconoCuadro(x.icono, color: x.color, tamano: 30, relleno: true)),
                        Positioned(
                          right: 8,
                          top: 8,
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                            decoration: BoxDecoration(color: Colors.black.withValues(alpha: 0.45), borderRadius: BorderRadius.circular(99)),
                            child: Text('${x.id}', style: const TextStyle(color: OL.blanco, fontSize: 11, fontWeight: FontWeight.w800)),
                          ),
                        ),
                      ]),
                    ),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(10, 8, 10, 10),
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text(x.nombre, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 13)),
                        Text(x.categoria, style: const TextStyle(color: OL.gris, fontSize: 11)),
                      ]),
                    ),
                  ]),
                ),
              );
            },
          ),
          const SizedBox(height: 20),
          const TituloSeccion('Actividades diarias'),
          const SizedBox(height: 4),
          const Text('Práctica complementaria al curso.', style: TextStyle(color: OL.gris, fontSize: 12)),
          const SizedBox(height: 10),
          for (final a in actividadesDiarias)
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Tarjeta(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                onTap: () => abrir('/chat?situacion=49'),
                child: Row(children: [
                  IconoCuadro(a.$3, color: a.$4, tamano: 38),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(a.$1, style: const TextStyle(fontWeight: FontWeight.w700)),
                      Text(a.$2, style: const TextStyle(color: OL.gris, fontSize: 12)),
                    ]),
                  ),
                  const Icon(Icons.chevron_right, color: OL.gris),
                ]),
              ),
            ),
        ],
      ),
    );
  }
}
