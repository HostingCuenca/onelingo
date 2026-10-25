import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/api/pagos_api.dart';
import '../../core/i18n/i18n.dart';
import '../../core/pagos/providers.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import 'idiomas_plan.dart';

/// Prueba gratuita y planes (contrato de pagos, fase 1). Los planes y la
/// suscripción salen del servidor; se paga en Stripe Checkout y se gestiona
/// en el Customer Portal. DEMO y sin servidor eligen el plan en local.
class PlansScreen extends ConsumerStatefulWidget {
  const PlansScreen({super.key});

  @override
  ConsumerState<PlansScreen> createState() => _PlansScreenState();
}

class _PlansScreenState extends ConsumerState<PlansScreen> {
  /// Plan cuyo botón espera al servidor ('portal' para «Gestionar»).
  String? _esperando;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      ref.read(catalogoPlanesProvider.notifier).refrescar();
      ref.read(suscripcionProvider.notifier).refrescar();
    });
  }

  Future<void> _abrir(Future<RespuestaPago> Function() pedir, String clave) async {
    setState(() => _esperando = clave);
    final r = await pedir();
    if (!mounted) return;
    final url = r.url;
    if (r.ok && url != null && url.isNotEmpty) {
      final abierta = await ref.read(abrirUrlProvider)(url);
      if (!mounted) return;
      setState(() => _esperando = null);
      if (!abierta) _aviso(tr('No se pudo abrir la página de pago.'));
      return;
    }
    setState(() => _esperando = null);
    if (r.codigo == 409) ref.read(suscripcionProvider.notifier).refrescar();
    _aviso(r.ok ? tr('No se pudo abrir la página de pago.') : r.error);
  }

  /// Plan de N idiomas: primero se eligen (el idioma meta ya marcado); el plan
  /// «todos» va directo a Checkout.
  Future<void> _suscribirme(PlanServidor p, PagosApi api) async {
    var elegidos = const <String>[];
    if (!p.todosLosIdiomas) {
      final r = await elegirIdiomasPlan(
        context,
        cantidad: p.idiomas,
        marcados: [ref.read(progressProvider).idiomaMeta],
      );
      if (r == null || !mounted) return;
      elegidos = r;
    }
    await _abrir(() => api.checkout(p.id, elegidos), p.id);
  }

  void _aviso(String texto, {Color color = OL.rojo}) =>
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(texto), backgroundColor: color),
      );

  @override
  Widget build(BuildContext context) {
    final interfaz = ref.watch(progressProvider.select((s) => s.interfaz));
    final ep = ref.watch(estadoPlanProvider);
    final catalogo = ref.watch(catalogoPlanesProvider);
    final api = ref.watch(pagosApiProvider);
    final sus = ep.servidor ? ep.suscripcion : null;
    final restante = ep.trialRestante;
    // Plan suscrito (aunque el idioma que se estudia no esté pagado).
    final planSuscrito = sus != null && sus.enCurso && sus.planId.isNotEmpty ? sus.planId : ep.planId;
    final planActual = catalogo.plan(planSuscrito);
    final idiomaNoPagado = !ep.tienePlan && sus != null && sus.vigente;

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => context.canPop() ? context.pop() : context.go('/inicio')),
        title: Text(tr('Planes y precios')),
      ),
      body: Movil(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
          children: [
            if (sus != null && sus.idiomasPorElegir > 0) ...[
              AvisoIdiomasPorElegir(suscripcion: sus),
              const SizedBox(height: 12),
            ],
            if (!ep.tienePlan && sus?.estado != 'impago')
              Tarjeta(
                color: restante == 0 ? OL.rojoSuave : OL.amarilloSuave,
                sombra: false,
                child: Row(children: [
                  Icon(Icons.timer_outlined, color: restante == 0 ? OL.rojo : const Color(0xFF9A6B00), size: 30),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      if (idiomaNoPagado)
                        Text(tr('Este idioma no está en tu plan: estás en la prueba gratuita'),
                            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: Color(0xFF9A6B00))),
                      Text(restante == 0 ? tr('Tu prueba gratuita terminó') : tr('Prueba gratuita en curso'),
                          style: const TextStyle(fontWeight: FontWeight.w800)),
                      Text(
                        restante == 0
                            ? tr('Elige un plan para seguir aprendiendo. Tu progreso se conserva.')
                            : tr('Te quedan {min} min de uso real. Después eliges tu plan.', {'min': restante ~/ 60}),
                        style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.4),
                      ),
                      const SizedBox(height: 6),
                      BarraProgreso(ep.pruebaTotal == 0 ? 1 : 1 - restante / ep.pruebaTotal, color: restante == 0 ? OL.rojo : OL.naranja, fondo: OL.blanco, alto: 6),
                    ]),
                  ),
                ]),
              ),
            if (sus != null && sus.stripeVigente) ...[
              if (!ep.tienePlan) const SizedBox(height: 12),
              _TarjetaSuscripcion(
                plan: catalogo.plan(sus.planId)?.nombreEn(interfaz) ?? sus.planId,
                suscripcion: sus,
                esperando: _esperando == 'portal',
                onGestionar: sus.puedeGestionar ? () => _abrir(api.portal, 'portal') : null,
              ),
            ],
            if (sus != null && sus.esCortesia)
              Tarjeta(
                color: OL.verdeSuave,
                sombra: false,
                child: Row(children: [
                  const Icon(Icons.card_giftcard_rounded, color: OL.verde, size: 30),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(planActual?.nombreEn(interfaz) ?? sus.planId, style: const TextStyle(fontWeight: FontWeight.w800)),
                      Text(
                        sus.periodoFin == null
                            ? tr('Acceso otorgado por el administrador')
                            : tr('Acceso otorgado por el administrador hasta el {fecha}', {'fecha': fechaCorta(sus.periodoFin!)}),
                        style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.4),
                      ),
                      const SizedBox(height: 8),
                      IdiomasDePago(suscripcion: sus),
                    ]),
                  ),
                ]),
              ),
            const SizedBox(height: 18),
            Text(tr('Desbloquea tu potencial'), style: Theme.of(context).textTheme.headlineMedium),
            Text(tr('Elige cuántos idiomas quieres aprender. Todos los planes incluyen el curso completo, la práctica libre y la IA.'),
                style: const TextStyle(color: OL.gris, height: 1.4)),
            if (ep.servidor && catalogo.modoPrueba) ...[
              const SizedBox(height: 10),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(color: OL.azulSuave, borderRadius: BorderRadius.circular(12)),
                child: Row(children: [
                  const Icon(Icons.science_outlined, size: 16, color: OL.azul),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(tr('Modo de prueba: usa la tarjeta 4242 4242 4242 4242'),
                        style: const TextStyle(fontSize: 12, color: OL.azul, fontWeight: FontWeight.w700)),
                  ),
                ]),
              ),
            ],
            const SizedBox(height: 16),
            for (final p in catalogo.planes)
              Padding(
                padding: const EdgeInsets.only(bottom: 14),
                child: Tarjeta(
                  borde: p.id == planSuscrito ? OL.verde : (p.destacado ? OL.morado : null),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Row(children: [
                      Expanded(child: Text(p.nombreEn(interfaz), style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800))),
                      if (p.destacado) Etiqueta(tr('POPULAR')),
                      if (p.id == planSuscrito) Etiqueta(tr('TU PLAN'), color: OL.verde),
                    ]),
                    if (p.todosLosIdiomas) ...[
                      const SizedBox(height: 4),
                      Etiqueta(tr('Todos los idiomas'), color: OL.verde, icono: Icons.public),
                    ],
                    if (p.descripcionEn(interfaz).isNotEmpty) ...[
                      const SizedBox(height: 4),
                      Text(p.descripcionEn(interfaz), style: const TextStyle(color: OL.gris, fontSize: 13, height: 1.35)),
                    ],
                    const SizedBox(height: 6),
                    Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
                      Text(p.precioTexto, style: const TextStyle(fontSize: 34, fontWeight: FontWeight.w800, color: OL.morado, height: 1)),
                      Padding(padding: const EdgeInsets.only(bottom: 4, left: 4), child: Text(p.intervaloTexto, style: const TextStyle(color: OL.gris))),
                    ]),
                    const SizedBox(height: 12),
                    for (final i in p.incluyeEn(interfaz))
                      Padding(
                        padding: const EdgeInsets.only(bottom: 6),
                        child: Row(children: [
                          const Icon(Icons.check_circle, color: OL.verde, size: 18),
                          const SizedBox(width: 8),
                          Expanded(child: Text(i, style: const TextStyle(fontSize: 13))),
                        ]),
                      ),
                    const SizedBox(height: 8),
                    _botonPlan(p, ep, planSuscrito, catalogo, sus, api, interfaz),
                  ]),
                ),
              ),
            Text(
              // Sin pagos activos los botones dicen «Pagos próximamente»: no
              // se promete Stripe.
              ep.servidor && catalogo.pagosDisponible
                  ? tr('Pago con tarjeta en la página segura de Stripe. Cancela cuando quieras desde «Gestionar suscripción».')
                  : tr('Pago mensual, cancela cuando quieras.'),
              textAlign: TextAlign.center,
              style: const TextStyle(color: OL.gris, fontSize: 11),
            ),
          ],
        ),
      ),
    );
  }

  Widget _botonPlan(
    PlanServidor p,
    EstadoPlan ep,
    String planSuscrito,
    CatalogoPlanes catalogo,
    Suscripcion? sus,
    PagosApi api,
    String interfaz,
  ) {
    final estilo = ElevatedButton.styleFrom(backgroundColor: p.destacado ? OL.morado : OL.moradoOscuro);
    if (p.id == planSuscrito) {
      return ElevatedButton(style: estilo, onPressed: null, child: Text(tr('PLAN ACTUAL')));
    }
    // DEMO o sin servidor: se elige en el dispositivo, como antes.
    if (!ep.servidor) {
      return ElevatedButton(
        style: estilo,
        onPressed: () {
          if (ref.read(progressProvider.notifier).elegirPlan(p.id)) {
            _aviso(tr('Plan "{plan}" activado (pago real en la fase 2)', {'plan': p.nombreEn(interfaz)}), color: OL.verde);
          }
        },
        child: Text(tr('ELEGIR {plan}', {'plan': p.nombreEn(interfaz).toUpperCase()})),
      );
    }
    final cargando = _esperando == p.id;
    // Morado: mientras espera el botón está deshabilitado (gris claro) y el
    // contorneado es transparente sobre blanco; el blanco no se veía.
    const indicador = SizedBox(
      width: 18,
      height: 18,
      child: CircularProgressIndicator(strokeWidth: 2, color: OL.morado),
    );
    // Ya paga con Stripe: los cambios de plan se hacen en el portal.
    if (sus != null && sus.stripeVigente && sus.puedeGestionar) {
      return OutlinedButton(
        onPressed: _esperando != null ? null : () => _abrir(api.portal, p.id),
        child: cargando ? indicador : Text(tr('Cambiar de plan')),
      );
    }
    if (!catalogo.pagosDisponible) {
      return ElevatedButton(style: estilo, onPressed: null, child: Text(tr('Pagos próximamente')));
    }
    return ElevatedButton(
      style: estilo,
      onPressed: _esperando != null ? null : () => _suscribirme(p, api),
      child: cargando ? indicador : Text(tr('Suscribirme')),
    );
  }
}

/// Suscripción de Stripe en curso: plan, estado, fecha y «Gestionar».
class _TarjetaSuscripcion extends StatelessWidget {
  const _TarjetaSuscripcion({
    required this.plan,
    required this.suscripcion,
    required this.esperando,
    required this.onGestionar,
  });
  final String plan;
  final Suscripcion suscripcion;
  final bool esperando;
  final VoidCallback? onGestionar;

  @override
  Widget build(BuildContext context) {
    final s = suscripcion;
    final fin = s.periodoFin == null ? null : fechaCorta(s.periodoFin!);
    final detalle = s.estado == 'impago'
        ? tr('No se pudo cobrar la última cuota. Actualiza tu tarjeta.')
        : fin == null
        ? null
        : s.cancelaAlFinal
        ? tr('Se cancela el {fecha}', {'fecha': fin})
        : s.estado == 'cancelada'
        ? tr('Acceso hasta el {fecha}', {'fecha': fin})
        : tr('Se renueva el {fecha}', {'fecha': fin});
    final aviso = s.estado == 'impago' || s.cancelaAlFinal;
    return Tarjeta(
      color: aviso ? OL.amarilloSuave : OL.verdeSuave,
      sombra: false,
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Icon(Icons.workspace_premium_outlined, color: aviso ? const Color(0xFF9A6B00) : OL.verde, size: 28),
          const SizedBox(width: 10),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(tr('Tu suscripción'), style: const TextStyle(color: OL.gris, fontSize: 12, fontWeight: FontWeight.w700)),
              Text(plan, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
            ]),
          ),
          Etiqueta(s.estadoTexto, color: aviso ? const Color(0xFF9A6B00) : OL.verde),
        ]),
        if (detalle != null) ...[
          const SizedBox(height: 8),
          Text(detalle, style: const TextStyle(color: OL.gris, fontSize: 13, height: 1.35)),
        ],
        const SizedBox(height: 8),
        IdiomasDePago(suscripcion: s),
        if (onGestionar != null) ...[
          const SizedBox(height: 10),
          OutlinedButton.icon(
            onPressed: esperando ? null : onGestionar,
            icon: esperando
                ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                : const Icon(Icons.open_in_new_rounded, size: 18),
            label: Text(tr('Gestionar suscripción')),
          ),
        ],
      ]),
    );
  }
}
