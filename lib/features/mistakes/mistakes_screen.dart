import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Sección de errores: error, forma correcta, explicación y práctica (§8).
class MistakesScreen extends ConsumerStatefulWidget {
  const MistakesScreen({super.key});

  @override
  ConsumerState<MistakesScreen> createState() => _MistakesScreenState();
}

class _MistakesScreenState extends ConsumerState<MistakesScreen> {
  Skill? filtro;

  @override
  Widget build(BuildContext context) {
    final s = ref.watch(progressProvider);
    final lista = s.errores.where((e) => filtro == null || e.skill == filtro).toList();
    final pendientes = s.errores.where((e) => !e.practicado).length;

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => context.canPop() ? context.pop() : context.go('/perfil')),
        title: const Text('Mis errores'),
      ),
      body: Movil(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
          children: [
            HeroCard(
              gradient: OL.gradienteRojo,
              child: Row(children: [
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    const Text('Repasa tus errores', style: TextStyle(color: OL.blanco, fontSize: 20, fontWeight: FontWeight.w800)),
                    const SizedBox(height: 4),
                    Text(
                      pendientes == 0
                          ? 'No tienes errores pendientes. ¡Sigue así!'
                          : 'Conviértelos en fortalezas: tienes $pendientes por practicar.',
                      style: const TextStyle(color: Color(0xFFFFE3E6), fontSize: 13, height: 1.4),
                    ),
                  ]),
                ),
                const Icon(Icons.fact_check_outlined, color: OL.blanco, size: 44),
              ]),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 36,
              child: ListView(
                scrollDirection: Axis.horizontal,
                children: [
                  _Filtro('Todos', filtro == null, () => setState(() => filtro = null)),
                  for (final k in Skill.values)
                    if (s.errores.any((e) => e.skill == k))
                      _Filtro(k.nombre, filtro == k, () => setState(() => filtro = k)),
                ],
              ),
            ),
            const SizedBox(height: 14),
            if (lista.isEmpty)
              const Padding(
                padding: EdgeInsets.symmetric(vertical: 40),
                child: Column(children: [
                  Icon(Icons.emoji_events_outlined, size: 48, color: OL.grisClaro),
                  SizedBox(height: 10),
                  Text('Aquí aparecerán los errores que cometas en lecciones, exámenes y conversaciones.',
                      textAlign: TextAlign.center, style: TextStyle(color: OL.gris)),
                ]),
              ),
            for (final e in lista) _ErrorCard(e: e),
          ],
        ),
      ),
    );
  }
}

class _Filtro extends StatelessWidget {
  const _Filtro(this.texto, this.activo, this.onTap);
  final String texto;
  final bool activo;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(right: 8),
        child: ChoiceChip(
          label: Text(texto),
          selected: activo,
          onSelected: (_) => onTap(),
          selectedColor: OL.rojoSuave,
          backgroundColor: OL.blanco,
          side: BorderSide.none,
          labelStyle: TextStyle(color: activo ? OL.rojo : OL.gris, fontWeight: FontWeight.w700, fontSize: 12),
        ),
      );
}

class _ErrorCard extends ConsumerWidget {
  const _ErrorCard({required this.e});
  final Mistake e;

  Color get _color => switch (e.skill) {
        Skill.gramatica || Skill.conjugacion => OL.naranja,
        Skill.vocabulario => OL.morado,
        Skill.listening || Skill.pronunciacion => OL.azul,
        _ => OL.verde,
      };

  String _hace() {
    final d = DateTime.now().difference(e.fecha);
    if (d.inMinutes < 1) return 'ahora';
    if (d.inHours < 1) return 'hace ${d.inMinutes} min';
    if (d.inDays < 1) return 'hace ${d.inHours} h';
    if (d.inDays == 1) return 'ayer';
    return 'hace ${d.inDays} días';
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) => Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: Tarjeta(
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              Etiqueta(e.skill.nombre, color: _color),
              const Spacer(),
              Icon(Icons.history, size: 14, color: OL.gris),
              const SizedBox(width: 4),
              Text(_hace(), style: const TextStyle(color: OL.gris, fontSize: 11)),
            ]),
            const SizedBox(height: 10),
            if (e.origen.isNotEmpty) Text(e.origen, style: const TextStyle(color: OL.gris, fontSize: 11, fontWeight: FontWeight.w600)),
            Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Icon(Icons.close, color: OL.rojo, size: 16),
              const SizedBox(width: 6),
              Expanded(child: Text(e.original, style: const TextStyle(color: OL.rojo, decoration: TextDecoration.lineThrough))),
            ]),
            const SizedBox(height: 4),
            Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Icon(Icons.check, color: OL.verde, size: 16),
              const SizedBox(width: 6),
              Expanded(child: Text(e.correccion, style: const TextStyle(fontWeight: FontWeight.w700))),
            ]),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(color: OL.fondo, borderRadius: BorderRadius.circular(10)),
              child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const Icon(Icons.menu_book_outlined, size: 16, color: OL.gris),
                const SizedBox(width: 8),
                Expanded(child: Text(e.explicacion, style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.4))),
              ]),
            ),
            const SizedBox(height: 10),
            if (e.practicado)
              const Etiqueta('Practicado', color: OL.verde, icono: Icons.check_circle_outline)
            else
              OutlinedButton.icon(
                style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(42)),
                onPressed: () => _practicar(context, ref),
                icon: const Icon(Icons.record_voice_over_outlined, size: 18),
                label: const Text('Practicar de nuevo'),
              ),
          ]),
        ),
      );

  void _practicar(BuildContext context, WidgetRef ref) {
    final ctrl = TextEditingController();
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Text('Escribe la forma correcta'),
        content: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(e.explicacion, style: const TextStyle(color: OL.gris, fontSize: 13)),
          const SizedBox(height: 12),
          TextField(controller: ctrl, autofocus: true, decoration: const InputDecoration(hintText: 'Tu respuesta')),
        ]),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancelar')),
          ElevatedButton(
            style: ElevatedButton.styleFrom(minimumSize: const Size(120, 44)),
            onPressed: () {
              final ok = ctrl.text.trim().toLowerCase().replaceAll(RegExp(r'[^\w\s]'), '') ==
                  e.correccion.toLowerCase().replaceAll(RegExp(r'[^\w\s]'), '');
              Navigator.pop(ctx);
              if (ok) ref.read(progressProvider.notifier).marcarErrorPracticado(e.id);
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                content: Text(ok ? '¡Correcto! Error superado.' : 'Casi. La forma correcta es: ${e.correccion}'),
                backgroundColor: ok ? OL.verde : OL.rojo,
              ));
            },
            child: const Text('Comprobar'),
          ),
        ],
      ),
    );
  }
}
