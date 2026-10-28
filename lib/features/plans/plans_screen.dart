import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/api/pagos_api.dart';
import '../../core/i18n/i18n.dart';
import '../../core/pagos/google_play.dart';
import '../../core/pagos/providers.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import 'empresa_screen.dart';
import 'estilo_plan.dart';
import 'familia_screen.dart';
import 'idiomas_plan.dart';
import 'plan_detalle_screen.dart';
import 'tabla_precios_screen.dart';

/// Prueba gratuita y planes (contrato de pagos, fase 1). Los planes y la
/// suscripción salen del servidor; cada plan abre su detalle con la duración
/// ([PlanDetalleScreen]) y se paga con Google Play en Android (se gestiona en
/// Play) o con Stripe Checkout en la web (se gestiona en el Customer Portal).
/// DEMO y sin servidor eligen el plan en local.
class PlansScreen extends ConsumerStatefulWidget {
  const PlansScreen({super.key});

  @override
  ConsumerState<PlansScreen> createState() => _PlansScreenState();
}

class _PlansScreenState extends ConsumerState<PlansScreen> {
  /// «Gestionar suscripción» espera al servidor.
  bool _esperandoPortal = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      ref.read(catalogoPlanesProvider.notifier).refrescar();
      ref.read(suscripcionProvider.notifier).refrescar();
    });
  }

  Future<void> _portal(PagosApi api) async {
    setState(() => _esperandoPortal = true);
    await abrirPagina(context, ref, api.portal);
    if (mounted) setState(() => _esperandoPortal = false);
  }

  void _ir(Widget pantalla) =>
      Navigator.of(context).push(MaterialPageRoute<void>(builder: (_) => pantalla));

  @override
  Widget build(BuildContext context) {
    final interfaz = ref.watch(progressProvider.select((s) => s.interfaz));
    final ep = ref.watch(estadoPlanProvider);
    final catalogo = ref.watch(catalogoPlanesProvider);
    final api = ref.watch(pagosApiProvider);
    final sus = ep.servidor ? ep.suscripcion : null;
    final restante = ep.trialRestante;
    final planSuscrito = planSuscritoDe(ep);
    final planActual = catalogo.plan(planSuscrito);
    final idiomaNoPagado = !ep.tienePlan && sus != null && sus.vigente;
    final enApp = ref.watch(pagoEnAppProvider);

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
            if (sus != null && sus.pagoVigente) ...[
              if (!ep.tienePlan) const SizedBox(height: 12),
              _TarjetaSuscripcion(
                plan: catalogo.plan(sus.planId)?.nombreEn(interfaz) ?? sus.planId,
                suscripcion: sus,
                esperando: _esperandoPortal,
                // Play: la gestión (cancelar, tarjeta) es de Google. Stripe: su portal, solo en la web.
                onGestionar: sus.googleVigente
                    ? () => ref.read(abrirUrlProvider)(urlGestionPlay(catalogo.googlePaquete, sus.googleProducto))
                    : sus.puedeGestionar && !enApp
                    ? () => _portal(api)
                    : null,
                nota: sus.stripeVigente && enApp ? tr('Pagada en la web: se gestiona desde onelingo.org.') : null,
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
            if (sus != null && (sus.titularFamiliar || (sus.familiar && sus.enCurso))) ...[
              const SizedBox(height: 12),
              Tarjeta(
                key: const ValueKey('tarjeta-familia'),
                color: OL.naranjaSuave,
                sombra: false,
                onTap: () => _ir(const FamiliaScreen()),
                child: Row(children: [
                  const Icon(Icons.family_restroom_rounded, color: OL.naranja, size: 30),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(sus.familiar ? tr('Formas parte de un plan familiar') : tr('Tu plan familiar'),
                          style: const TextStyle(fontWeight: FontWeight.w800)),
                      Text(
                        sus.familiar
                            ? tr('Tu acceso lo paga quien te invitó. Tu progreso es solo tuyo.')
                            : tr('Añade hasta {n} personas: cada una con su propia cuenta y progreso.', {'n': (sus.usuariosPlan ?? 1) - 1}),
                        style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.4),
                      ),
                      if (sus.familiar) ...[
                        const SizedBox(height: 8),
                        IdiomasDePago(suscripcion: sus),
                      ],
                    ]),
                  ),
                  const Icon(Icons.chevron_right_rounded, color: OL.gris),
                ]),
              ),
            ],
            const SizedBox(height: 18),
            Text(tr('Elige tu plan'), style: Theme.of(context).textTheme.headlineMedium),
            Text(tr('Aprende uno o varios idiomas y alcanza tus metas. Todos los planes incluyen el curso completo, la práctica libre y la IA.'),
                style: const TextStyle(color: OL.gris, height: 1.4)),
            if (ep.servidor && catalogo.modoPrueba && !enApp) ...[
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
                padding: const EdgeInsets.only(bottom: 12),
                child: _TarjetaPlan(
                  plan: p,
                  interfaz: interfaz,
                  actual: p.id == planSuscrito,
                  onTap: () => _ir(PlanDetalleScreen(planId: p.id)),
                ),
              ),
            _TarjetaEmpresa(onTap: () => _ir(const EmpresaScreen())),
            const SizedBox(height: 6),
            TextButton.icon(
              onPressed: () => _ir(const TablaPreciosScreen()),
              icon: const Icon(Icons.table_chart_outlined, size: 18),
              label: Text(tr('Ver la tabla de precios completa')),
            ),
            Text(
              textoPago(ep, catalogo, enApp),
              textAlign: TextAlign.center,
              style: const TextStyle(color: OL.gris, fontSize: 11),
            ),
          ],
        ),
      ),
    );
  }
}

/// Cómo se paga, bajo los planes. Sin pagos activos los botones dicen «Pagos
/// próximamente»: no se promete ningún medio de pago.
String textoPago(EstadoPlan ep, CatalogoPlanes catalogo, bool enApp) => !ep.servidor
    ? tr('Pago mensual, cancela cuando quieras.')
    : enApp
    ? catalogo.googleDisponible
          ? tr('Pago seguro con Google Play. Cancela cuando quieras desde Google Play.')
          : tr('Pago mensual, cancela cuando quieras.')
    : catalogo.pagosDisponible
    ? tr('Pago con tarjeta en la página segura de Stripe. Cancela cuando quieras desde «Gestionar suscripción».')
    : tr('Pago mensual, cancela cuando quieras.');

/// Página de Google Play para gestionar (cancelar, cambiar el medio de pago)
/// la suscripción [producto] de la app.
String urlGestionPlay(String paquete, String? producto) => Uri.https('play.google.com', '/store/account/subscriptions', {
  'sku': ?producto,
  'package': paquete,
}).toString();

/// Plan suscrito (aunque el idioma que se estudia no esté pagado).
String planSuscritoDe(EstadoPlan ep) {
  final sus = ep.servidor ? ep.suscripcion : null;
  return sus != null && sus.enCurso && sus.planId.isNotEmpty ? sus.planId : ep.planId;
}

/// Abre Stripe (Checkout o portal) con la URL que devuelve [pedir]; avisa si falla.
Future<void> abrirPagina(BuildContext context, WidgetRef ref, Future<RespuestaPago> Function() pedir) async {
  final r = await pedir();
  if (!context.mounted) return;
  final url = r.url;
  if (r.ok && url != null && url.isNotEmpty) {
    final abierta = await ref.read(abrirUrlProvider)(url);
    if (!abierta && context.mounted) avisoPago(context, tr('No se pudo abrir la página de pago.'));
    return;
  }
  if (r.codigo == 409) ref.read(suscripcionProvider.notifier).refrescar();
  avisoPago(context, r.ok ? tr('No se pudo abrir la página de pago.') : r.error);
}

void avisoPago(BuildContext context, String texto, {Color color = OL.rojo}) =>
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(texto), backgroundColor: color),
    );

/// Plan en la lista: icono, nombre, idiomas o usuarios, precio y flecha.
class _TarjetaPlan extends StatelessWidget {
  const _TarjetaPlan({required this.plan, required this.interfaz, required this.actual, required this.onTap});
  final PlanServidor plan;
  final String interfaz;
  final bool actual;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final p = plan;
    final e = EstiloPlan.de(p);
    final descripcion = p.descripcionEn(interfaz);
    return Tarjeta(
      key: ValueKey('plan-${p.id}'),
      color: e.suave,
      borde: actual ? OL.verde : (p.destacado ? e.color : Colors.transparent),
      onTap: onTap,
      padding: const EdgeInsets.fromLTRB(14, 14, 12, 14),
      etiquetaSemantica: '${p.nombreEn(interfaz)}, ${subtituloPlan(p)}, ${p.precioTexto} ${p.intervaloTexto}',
      child: Row(children: [
        IconoPlan(e),
        const SizedBox(width: 12),
        Expanded(
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(p.nombreEn(interfaz), style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800, height: 1.15)),
            Text(subtituloPlan(p), style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: e.color)),
            if (descripcion.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text(descripcion, maxLines: 2, overflow: TextOverflow.ellipsis,
                    style: const TextStyle(color: OL.gris, fontSize: 12.5, height: 1.3)),
              ),
            if (p.destacado || actual)
              Padding(
                padding: const EdgeInsets.only(top: 6),
                child: Wrap(spacing: 6, runSpacing: 4, children: [
                  if (p.destacado) Etiqueta(tr('POPULAR'), color: e.color),
                  if (actual) Etiqueta(tr('TU PLAN'), color: OL.verde),
                ]),
              ),
          ]),
        ),
        const SizedBox(width: 8),
        Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
          Text(p.precioTexto, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w800, height: 1)),
          Text(p.intervaloTexto, style: const TextStyle(color: OL.gris, fontSize: 12)),
          const SizedBox(height: 8),
          CircleAvatar(
            radius: 15,
            backgroundColor: e.color,
            child: const Icon(Icons.chevron_right_rounded, color: OL.blanco, size: 22),
          ),
        ]),
      ]),
    );
  }
}

/// Plan Empresarial: cotización a medida.
class _TarjetaEmpresa extends StatelessWidget {
  const _TarjetaEmpresa({required this.onTap});
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    const e = EstiloPlan.empresa;
    return Tarjeta(
      key: const ValueKey('plan-empresa'),
      color: e.suave,
      borde: Colors.transparent,
      onTap: onTap,
      padding: const EdgeInsets.fromLTRB(14, 14, 12, 14),
      child: Row(children: [
        const IconoPlan(e),
        const SizedBox(width: 12),
        Expanded(
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(tr('Empresarial'), style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800, height: 1.15)),
            Text(tr('Para empresas'), style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: e.color)),
            Text(tr('Cotización personalizada para que tu equipo aprenda idiomas.'),
                style: const TextStyle(color: OL.gris, fontSize: 12.5, height: 1.3)),
          ]),
        ),
        const SizedBox(width: 8),
        CircleAvatar(
          radius: 15,
          backgroundColor: e.color,
          child: const Icon(Icons.chevron_right_rounded, color: OL.blanco, size: 22),
        ),
      ]),
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
    this.nota,
  });
  final String plan;
  final Suscripcion suscripcion;
  final bool esperando;
  final VoidCallback? onGestionar;

  /// Aviso bajo los idiomas (p. ej. suscripción de la web vista en Android).
  final String? nota;

  @override
  Widget build(BuildContext context) {
    final s = suscripcion;
    final fin = s.periodoFin == null ? null : fechaCorta(s.periodoFin!);
    final detalle = s.estado == 'impago'
        ? (s.esGoogle
              ? tr('Google Play no pudo cobrar la última cuota. Actualiza tu medio de pago en Google Play.')
              : tr('No se pudo cobrar la última cuota. Actualiza tu tarjeta.'))
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
        if ((s.meses ?? 1) > 1)
          Text(tr('Pago cada {n} meses', {'n': s.meses!}), style: const TextStyle(color: OL.gris, fontSize: 13, height: 1.35)),
        const SizedBox(height: 8),
        IdiomasDePago(suscripcion: s),
        if (nota != null) ...[
          const SizedBox(height: 8),
          Text(nota!, style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.35)),
        ],
        if (onGestionar != null) ...[
          const SizedBox(height: 10),
          OutlinedButton.icon(
            onPressed: esperando ? null : onGestionar,
            icon: esperando
                ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                : const Icon(Icons.open_in_new_rounded, size: 18),
            label: Text(s.esGoogle ? tr('Gestionar en Google Play') : tr('Gestionar suscripción')),
          ),
        ],
      ]),
    );
  }
}
