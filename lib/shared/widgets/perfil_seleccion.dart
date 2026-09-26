import 'package:flutter/material.dart';

import '../../core/perfil_aprendizaje.dart';

class PerfilSeleccion extends StatelessWidget {
  const PerfilSeleccion({
    super.key,
    required this.sectores,
    required this.objetivos,
    required this.onChanged,
    this.soloObjetivos = false,
    this.soloSectores = false,
  });
  final List<String> sectores, objetivos;
  final void Function(List<String>, List<String>) onChanged;
  final bool soloObjetivos, soloSectores;
  @override
  Widget build(BuildContext context) {
    Widget opciones(
      Map<String, String> lista,
      List<String> seleccion,
      bool sector,
    ) => Wrap(
      spacing: 8,
      runSpacing: 8,
      children: [
        for (final e in lista.entries)
          FilterChip(
            label: Text(e.value),
            selected: seleccion.contains(e.key),
            onSelected: (activo) {
              final nueva = [...seleccion];
              if (activo) {
                nueva.add(e.key);
              } else {
                nueva.remove(e.key);
              }
              onChanged(sector ? nueva : sectores, sector ? objetivos : nueva);
            },
          ),
      ],
    );
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (!soloObjetivos) ...[
          const Text(
            'Elige uno o varios sectores',
            style: TextStyle(fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 12),
          opciones(sectoresAprendizaje, sectores, true),
        ],
        if (!soloSectores) ...[
          const SizedBox(height: 20),
          const Text(
            '¿Qué quieres lograr con el inglés?',
            style: TextStyle(fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 12),
          opciones(objetivosAprendizaje, objetivos, false),
        ],
      ],
    );
  }
}
