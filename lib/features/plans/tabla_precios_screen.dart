import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';
import '../../core/pagos/providers.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import 'estilo_plan.dart';

/// Todos los planes y duraciones en una tabla: precio total y precio por mes.
class TablaPreciosScreen extends ConsumerWidget {
  const TablaPreciosScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final interfaz = ref.watch(progressProvider.select((s) => s.interfaz));
    final planes = ref.watch(catalogoPlanesProvider).planes;
    final meses = {for (final p in planes) ...p.duraciones.map((d) => d.meses)}.toList()..sort();
    const celda = EdgeInsets.symmetric(horizontal: 10, vertical: 12);
    return Scaffold(
      appBar: AppBar(title: Text(tr('Tabla de precios'))),
      body: Movil(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 4, 16, 24),
          children: [
            Text(tr('Todos los planes y duraciones'), style: const TextStyle(color: OL.gris)),
            const SizedBox(height: 12),
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Table(
                defaultColumnWidth: const IntrinsicColumnWidth(),
                defaultVerticalAlignment: TableCellVerticalAlignment.middle,
                border: TableBorder(horizontalInside: BorderSide(color: OL.grisClaro)),
                children: [
                  TableRow(
                    decoration: const BoxDecoration(color: OL.moradoSuave),
                    children: [
                      Padding(padding: celda, child: Text(tr('Plan'), style: const TextStyle(fontWeight: FontWeight.w800))),
                      for (final m in meses)
                        Padding(padding: celda, child: Text(textoDuracion(m), textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.w800))),
                    ],
                  ),
                  for (final p in planes)
                    TableRow(
                      decoration: BoxDecoration(color: EstiloPlan.de(p).suave.withValues(alpha: .55)),
                      children: [
                        Padding(
                          padding: celda,
                          child: Row(mainAxisSize: MainAxisSize.min, children: [
                            IconoPlan(EstiloPlan.de(p), tamano: 30),
                            const SizedBox(width: 8),
                            Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                              Text(p.nombreEn(interfaz), style: const TextStyle(fontWeight: FontWeight.w800)),
                              Text(subtituloPlan(p), style: TextStyle(fontSize: 12, color: EstiloPlan.de(p).color, fontWeight: FontWeight.w700)),
                            ]),
                          ]),
                        ),
                        for (final m in meses)
                          Padding(
                            padding: celda,
                            child: () {
                              final d = p.duraciones.where((x) => x.meses == m).firstOrNull;
                              if (d == null) return const Text('—', textAlign: TextAlign.center, style: TextStyle(color: OL.gris));
                              return Column(children: [
                                Text(formatoPrecio(d.precio, p.moneda), style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
                                if (m > 1)
                                  Text(tr('{precio} al mes', {'precio': formatoPrecio((d.porMes * 100).round() / 100, p.moneda)}),
                                      style: const TextStyle(fontSize: 11, color: OL.gris)),
                              ]);
                            }(),
                          ),
                      ],
                    ),
                ],
              ),
            ),
            const SizedBox(height: 14),
            Text(tr('Plan Empresarial: precio a medida según el número de personas.'),
                style: const TextStyle(color: OL.gris, fontSize: 12)),
          ],
        ),
      ),
    );
  }
}
