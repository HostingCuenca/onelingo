import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Prueba gratuita de 1 hora y los 3 planes (REQUERIMIENTOS §11-12).
class PlansScreen extends ConsumerWidget {
  const PlansScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final restante = s.trialRestante;

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => context.canPop() ? context.pop() : context.go('/inicio')),
        title: const Text('Planes y precios'),
      ),
      body: Movil(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
          children: [
            if (s.planId.isEmpty)
              Tarjeta(
                color: restante == 0 ? OL.rojoSuave : OL.amarilloSuave,
                sombra: false,
                child: Row(children: [
                  Icon(Icons.timer_outlined, color: restante == 0 ? OL.rojo : const Color(0xFF9A6B00), size: 30),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(restante == 0 ? 'Tu hora gratis terminó' : 'Prueba gratuita en curso',
                          style: const TextStyle(fontWeight: FontWeight.w800)),
                      Text(
                        restante == 0
                            ? 'Elige un plan para seguir aprendiendo. Tu progreso se conserva.'
                            : 'Te quedan ${restante ~/ 60} min de uso real. Después eliges tu plan.',
                        style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.4),
                      ),
                      const SizedBox(height: 6),
                      BarraProgreso(1 - restante / segundosPruebaGratis, color: restante == 0 ? OL.rojo : OL.naranja, fondo: OL.blanco, alto: 6),
                    ]),
                  ),
                ]),
              ),
            const SizedBox(height: 18),
            Text('Desbloquea tu potencial', style: Theme.of(context).textTheme.headlineMedium),
            const Text('Elige cuántos idiomas quieres aprender. Todos los planes incluyen el curso completo, la práctica libre y la IA.',
                style: TextStyle(color: OL.gris, height: 1.4)),
            const SizedBox(height: 16),
            for (final p in planes)
              Padding(
                padding: const EdgeInsets.only(bottom: 14),
                child: Tarjeta(
                  borde: p.id == s.planId ? OL.verde : (p.idiomas == 2 ? OL.morado : null),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Row(children: [
                      Text(p.nombre, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
                      const Spacer(),
                      if (p.idiomas == 2) const Etiqueta('POPULAR'),
                      if (p.id == s.planId) const Etiqueta('TU PLAN', color: OL.verde),
                    ]),
                    const SizedBox(height: 6),
                    Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
                      Text('\$${p.precio}', style: const TextStyle(fontSize: 34, fontWeight: FontWeight.w800, color: OL.morado, height: 1)),
                      const Padding(padding: EdgeInsets.only(bottom: 4, left: 4), child: Text('/ mes', style: TextStyle(color: OL.gris))),
                    ]),
                    const SizedBox(height: 12),
                    for (final i in p.incluye)
                      Padding(
                        padding: const EdgeInsets.only(bottom: 6),
                        child: Row(children: [
                          const Icon(Icons.check_circle, color: OL.verde, size: 18),
                          const SizedBox(width: 8),
                          Expanded(child: Text(i, style: const TextStyle(fontSize: 13))),
                        ]),
                      ),
                    const SizedBox(height: 8),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(backgroundColor: p.idiomas == 2 ? OL.morado : OL.moradoOscuro),
                      onPressed: p.id == s.planId
                          ? null
                          : () {
                              ref.read(progressProvider.notifier).elegirPlan(p.id);
                              ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                                content: Text('Plan "${p.nombre}" activado (pago real en la fase 2)'),
                                backgroundColor: OL.verde,
                              ));
                            },
                      child: Text(p.id == s.planId ? 'PLAN ACTUAL' : 'ELEGIR ${p.nombre.toUpperCase()}'),
                    ),
                  ]),
                ),
              ),
            const Text(
              'Pago mensual, cancela cuando quieras. En móvil se cobra por la tienda (Apple/Google); en web con tarjeta.',
              textAlign: TextAlign.center,
              style: TextStyle(color: OL.gris, fontSize: 11),
            ),
          ],
        ),
      ),
    );
  }
}
