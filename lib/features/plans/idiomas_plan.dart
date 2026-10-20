import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/curriculum.dart' show idioma, idiomas;
import '../../core/i18n/i18n.dart';
import '../../core/pagos/providers.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Idiomas por suscripción (anexo del contrato de pagos): elegir los N idiomas
/// de un plan, cambiarlos y avisar al estudiar un idioma que no está pagado.

/// Selector de exactamente [cantidad] idiomas, con [marcados] ya elegidos.
/// Devuelve los códigos en el orden de la lista, o null si se cierra.
Future<List<String>?> elegirIdiomasPlan(
  BuildContext context, {
  required int cantidad,
  required List<String> marcados,
  String? titulo,
}) => showModalBottomSheet<List<String>>(
  context: context,
  isScrollControlled: true,
  showDragHandle: true,
  backgroundColor: OL.fondo,
  builder: (_) => _SelectorIdiomasPlan(
    cantidad: cantidad,
    marcados: marcados,
    titulo: titulo,
  ),
);

class _SelectorIdiomasPlan extends StatefulWidget {
  const _SelectorIdiomasPlan({
    required this.cantidad,
    required this.marcados,
    this.titulo,
  });
  final int cantidad;
  final List<String> marcados;
  final String? titulo;

  @override
  State<_SelectorIdiomasPlan> createState() => _SelectorIdiomasPlanState();
}

class _SelectorIdiomasPlanState extends State<_SelectorIdiomasPlan> {
  late final Set<String> elegidos = {
    ...widget.marcados.where(idiomasDePago.contains).take(widget.cantidad),
  };

  @override
  Widget build(BuildContext context) {
    final completo = elegidos.length == widget.cantidad;
    return SafeArea(
      child: ConstrainedBox(
        constraints: BoxConstraints(
          maxHeight: MediaQuery.of(context).size.height * .85,
          maxWidth: 480,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 4),
              child: Text(
                widget.titulo ??
                    (widget.cantidad == 1
                        ? tr('Elige el idioma de tu plan')
                        : tr('Elige los {n} idiomas de tu plan', {'n': widget.cantidad})),
                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 8),
              child: Text(
                tr('{n} de {total} elegidos', {'n': elegidos.length, 'total': widget.cantidad}),
                style: TextStyle(color: completo ? OL.verde : OL.gris, fontWeight: FontWeight.w700),
              ),
            ),
            Flexible(
              child: ListView(
                shrinkWrap: true,
                padding: const EdgeInsets.symmetric(horizontal: 12),
                children: [
                  for (final l in idiomas)
                    if (idiomasDePago.contains(l.code))
                      CheckboxListTile(
                        key: ValueKey('idioma-plan-${l.code}'),
                        value: elegidos.contains(l.code),
                        onChanged: elegidos.contains(l.code) || !completo
                            ? (v) => setState(() {
                                if (v == true) {
                                  elegidos.add(l.code);
                                } else {
                                  elegidos.remove(l.code);
                                }
                              })
                            : null,
                        secondary: LanguageFlag(l.code, width: 34),
                        title: Text(l.nombre, style: const TextStyle(fontWeight: FontWeight.w700)),
                        controlAffinity: ListTileControlAffinity.trailing,
                      ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 8, 20, 12),
              child: BotonPrincipal(
                onPressed: completo
                    ? () => Navigator.of(context).pop([
                        for (final c in idiomasDePago)
                          if (elegidos.contains(c)) c,
                      ])
                    : null,
                child: Text(tr('Continuar')),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// Cambia o completa los idiomas pagados con `PUT /usuarios/me/suscripcion/idiomas`.
/// [incluir] se marca si cabe (p. ej. el idioma nuevo que se quiere pagar).
Future<void> cambiarIdiomasSuscripcion(
  BuildContext context,
  WidgetRef ref,
  Suscripcion sus, {
  String? incluir,
}) async {
  final cantidad = sus.idiomasDelPlan;
  if (cantidad <= 0) return;
  final marcados = [
    ...sus.idiomas,
    if (incluir != null &&
        !sus.idiomas.contains(incluir) &&
        sus.idiomas.length < cantidad)
      incluir,
  ];
  final elegidos = await elegirIdiomasPlan(
    context,
    cantidad: cantidad,
    marcados: marcados,
  );
  if (elegidos == null || !context.mounted) return;
  final r = await ref.read(pagosApiProvider).cambiarIdiomas(elegidos);
  if (!context.mounted) return;
  final notifier = ref.read(suscripcionProvider.notifier);
  if (r.ok && r.cuerpo.containsKey('estado')) {
    notifier.aplicar(r.cuerpo);
  } else {
    await notifier.refrescar();
  }
  if (!context.mounted) return;
  final proximo = r.cuerpo['proximoCambio'];
  final fecha = proximo is String ? DateTime.tryParse(proximo) : null;
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      backgroundColor: r.ok ? OL.verde : OL.rojo,
      content: Text(
        r.ok
            ? tr('Idiomas de tu plan actualizados')
            : fecha != null
            ? '${r.error} · ${tr('Próximo cambio: {fecha}', {'fecha': fechaCorta(fecha)})}'
            : r.error,
      ),
    ),
  );
}

/// Cambia el idioma que se estudia y, si el alumno paga otros idiomas pero no
/// este, le avisa de que aquí sigue en la prueba gratuita.
Future<void> cambiarIdiomaMetaConAviso(
  BuildContext context,
  WidgetRef ref,
  String codigo,
) async {
  final progreso = ref.read(progressProvider);
  if (codigo == progreso.idiomaMeta) return;
  ref.read(progressProvider.notifier).cambiarIdiomaMeta(codigo);
  final sus = ref.read(suscripcionProvider);
  if (!usaServidorPagos(progreso.email) ||
      sus == null ||
      !sus.vigente ||
      sus.accesoEn(codigo)) {
    return;
  }
  await mostrarAvisoIdiomaNoPagado(context, ref, sus, codigo);
}

/// «Este idioma no está en tu plan: estás en la prueba gratuita».
Future<void> mostrarAvisoIdiomaNoPagado(
  BuildContext context,
  WidgetRef ref,
  Suscripcion sus,
  String codigo,
) async {
  final puedeCambiar =
      !sus.todosLosIdiomas &&
      sus.idiomasDelPlan > 0 &&
      sus.cambioIdiomas.permitido;
  final accion = await showDialog<String>(
    context: context,
    builder: (ctx) => AlertDialog(
      title: Text(idioma(codigo).nombre),
      content: Text(
        tr('Este idioma no está en tu plan: estás en la prueba gratuita'),
      ),
      actionsOverflowDirection: VerticalDirection.down,
      actionsOverflowButtonSpacing: 4,
      actions: [
        TextButton(
          onPressed: () => Navigator.of(ctx).pop(),
          child: Text(tr('Seguir con la prueba')),
        ),
        if (puedeCambiar)
          TextButton(
            onPressed: () => Navigator.of(ctx).pop('cambiar'),
            child: Text(tr('Cambiar un idioma de mi plan')),
          ),
        ElevatedButton(
          onPressed: () => Navigator.of(ctx).pop('anadir'),
          child: Text(tr('Añadirlo a mi plan')),
        ),
      ],
    ),
  );
  if (!context.mounted) return;
  if (accion == 'anadir') context.push('/planes');
  if (accion == 'cambiar') {
    await cambiarIdiomasSuscripcion(context, ref, sus, incluir: codigo);
  }
}

/// Selector del idioma que se estudia (Perfil).
Future<void> elegirIdiomaQueEstudias(BuildContext context, WidgetRef ref) async {
  final actual = ref.read(progressProvider).idiomaMeta;
  final sus = ref.read(estadoPlanProvider).suscripcion;
  final codigo = await showModalBottomSheet<String>(
    context: context,
    showDragHandle: true,
    isScrollControlled: true,
    backgroundColor: OL.fondo,
    builder: (ctx) => SafeArea(
      child: ConstrainedBox(
        constraints: BoxConstraints(maxHeight: MediaQuery.of(ctx).size.height * .85),
        child: ListView(
          shrinkWrap: true,
          padding: const EdgeInsets.fromLTRB(12, 0, 12, 12),
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(8, 0, 8, 8),
              child: Text(
                tr('Idioma que estudias'),
                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
              ),
            ),
            for (final l in idiomas)
              ListTile(
                key: ValueKey('idioma-meta-${l.code}'),
                leading: LanguageFlag(l.code, width: 34),
                title: Text(l.nombre, style: const TextStyle(fontWeight: FontWeight.w700)),
                subtitle: sus != null && sus.vigente && sus.accesoEn(l.code)
                    ? Text(tr('En tu plan'), style: const TextStyle(color: OL.verde, fontSize: 12))
                    : null,
                trailing: l.code == actual
                    ? const Icon(Icons.check_circle, color: OL.verde)
                    : null,
                onTap: () => Navigator.of(ctx).pop(l.code),
              ),
          ],
        ),
      ),
    ),
  );
  if (codigo == null || !context.mounted) return;
  await cambiarIdiomaMetaConAviso(context, ref, codigo);
}

/// Idiomas pagados (chips) y «Cambiar idiomas» según `cambioIdiomas`.
class IdiomasDePago extends ConsumerWidget {
  const IdiomasDePago({super.key, required this.suscripcion});
  final Suscripcion suscripcion;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = suscripcion;
    if (s.todosLosIdiomas) {
      return Etiqueta(tr('Todos los idiomas'), color: OL.verde, icono: Icons.public);
    }
    if (s.idiomas.isEmpty && s.idiomasPorElegir == 0) return const SizedBox.shrink();
    final motivo = s.cambioIdiomas.motivo;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Wrap(
          spacing: 6,
          runSpacing: 6,
          children: [
            for (final c in s.idiomas)
              Chip(
                key: ValueKey('chip-idioma-$c'),
                avatar: LanguageFlag(c, width: 22),
                label: Text(idioma(c).nombre),
                visualDensity: VisualDensity.compact,
                backgroundColor: OL.blanco,
                side: const BorderSide(color: OL.grisClaro),
              ),
          ],
        ),
        if (s.idiomas.isNotEmpty) ...[
          const SizedBox(height: 4),
          if (motivo == null)
            TextButton.icon(
              onPressed: () => cambiarIdiomasSuscripcion(context, ref, s),
              icon: const Icon(Icons.swap_horiz_rounded, size: 18),
              label: Text(tr('Cambiar idiomas')),
            )
          else
            Text(motivo, style: const TextStyle(color: OL.gris, fontSize: 12)),
        ],
      ],
    );
  }
}

/// Aviso para completar los idiomas «por elegir» del plan.
class AvisoIdiomasPorElegir extends ConsumerWidget {
  const AvisoIdiomasPorElegir({super.key, required this.suscripcion});
  final Suscripcion suscripcion;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final n = suscripcion.idiomasPorElegir;
    return Tarjeta(
      color: OL.naranjaSuave,
      sombra: false,
      // Sin ninguno elegido (Stripe sin idiomas): el idioma meta va marcado.
      onTap: () => cambiarIdiomasSuscripcion(
        context,
        ref,
        suscripcion,
        incluir: ref.read(progressProvider).idiomaMeta,
      ),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      child: Row(
        children: [
          const Icon(Icons.translate_rounded, color: OL.naranja),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              n == 1
                  ? tr('Te falta elegir 1 idioma de tu plan')
                  : tr('Te faltan {n} idiomas de tu plan por elegir', {'n': n}),
              style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14),
            ),
          ),
          Text(tr('Elegir'), style: const TextStyle(color: OL.naranja, fontWeight: FontWeight.w800)),
        ],
      ),
    );
  }
}
