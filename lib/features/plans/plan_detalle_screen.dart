import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../app/theme.dart';
import '../../core/api/pagos_api.dart';
import '../../core/i18n/i18n.dart';
import '../../core/pagos/google_play.dart';
import '../../core/pagos/providers.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import 'estilo_plan.dart';
import 'idiomas_plan.dart';
import 'plans_screen.dart' show abrirPagina, avisoPago, planSuscritoDe, textoPago;

/// Detalle de un plan: qué incluye, la duración (1, 3, 6 o 12 meses, con el
/// ahorro frente a pagar mes a mes) y el botón para suscribirse: en Android,
/// con Google Play dentro de la app; en la web, con Stripe Checkout.
class PlanDetalleScreen extends ConsumerStatefulWidget {
  const PlanDetalleScreen({super.key, required this.planId});
  final String planId;

  @override
  ConsumerState<PlanDetalleScreen> createState() => _PlanDetalleScreenState();
}

class _PlanDetalleScreenState extends ConsumerState<PlanDetalleScreen> {
  /// Duración elegida (null: la primera, la mensual).
  int? _meses;
  bool _esperando = false;

  /// Plan de N idiomas: primero se eligen (el idioma meta ya marcado); el plan
  /// «todos» va directo al pago. null si el alumno cerró la elección.
  Future<List<String>?> _elegirIdiomas(PlanServidor p) async {
    if (p.todosLosIdiomas) return const [];
    final r = await elegirIdiomasPlan(
      context,
      cantidad: p.idiomas,
      marcados: [ref.read(progressProvider).idiomaMeta],
    );
    return mounted ? r : null;
  }

  Future<void> _suscribirme(PlanServidor p, PagosApi api, int meses) async {
    final elegidos = await _elegirIdiomas(p);
    if (elegidos == null) return;
    await _abrir(() => api.checkout(p.id, elegidos, meses: meses));
  }

  /// Google Play: compra nueva (con idiomas) o cambio de una suscripción de
  /// Play (conserva sus idiomas; los que falten quedan por elegir).
  Future<void> _comprarPlay(PlanServidor p, int meses, {required bool cambio}) async {
    final elegidos = cambio ? const <String>[] : await _elegirIdiomas(p);
    if (elegidos == null) return;
    await ref.read(comprasPlayProvider.notifier).comprar(p, meses, elegidos);
  }

  Future<void> _abrir(Future<RespuestaPago> Function() pedir) async {
    setState(() => _esperando = true);
    await abrirPagina(context, ref, pedir);
    if (mounted) setState(() => _esperando = false);
  }

  @override
  Widget build(BuildContext context) {
    final interfaz = ref.watch(progressProvider.select((s) => s.interfaz));
    final catalogo = ref.watch(catalogoPlanesProvider);
    final ep = ref.watch(estadoPlanProvider);
    final api = ref.watch(pagosApiProvider);
    final p = catalogo.plan(widget.planId);
    if (p == null) {
      return Scaffold(
        appBar: AppBar(title: Text(tr('Planes y precios'))),
        body: Center(child: Text(tr('Este plan ya no está disponible.'))),
      );
    }
    final e = EstiloPlan.de(p);
    final duraciones = p.duraciones;
    final elegida = duraciones.where((d) => d.meses == _meses).firstOrNull ?? duraciones.first;
    final sus = ep.servidor ? ep.suscripcion : null;
    final planSuscrito = planSuscritoDe(ep);
    final enApp = ref.watch(pagoEnAppProvider);
    final precios = enApp ? ref.watch(preciosPlayProvider).valueOrNull ?? const <String, PrecioPlay>{} : const <String, PrecioPlay>{};
    ref.listen(comprasPlayProvider.select((s) => s.n), (_, _) {
      final s = ref.read(comprasPlayProvider);
      if (s.aviso == null) return;
      avisoPago(context, s.aviso!, color: s.exito ? OL.verde : OL.rojo);
      if (s.exito) Navigator.of(context).maybePop();
    });

    return Scaffold(
      appBar: AppBar(title: Text(p.nombreEn(interfaz))),
      body: Movil(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
          children: [
            Tarjeta(
              color: e.suave,
              borde: Colors.transparent,
              sombra: false,
              child: Row(children: [
                IconoPlan(e, tamano: 64),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(p.nombreEn(interfaz), style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800, height: 1.15)),
                    Text(subtituloPlan(p), style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: e.color)),
                  ]),
                ),
                Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
                  Text(p.precioTexto, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.w800, height: 1)),
                  Text(p.intervaloTexto, style: const TextStyle(color: OL.gris, fontSize: 12)),
                ]),
              ]),
            ),
            if (p.descripcionEn(interfaz).isNotEmpty) ...[
              const SizedBox(height: 10),
              Text(p.descripcionEn(interfaz), style: const TextStyle(color: OL.gris, height: 1.4)),
            ],
            const SizedBox(height: 14),
            for (final i in p.incluyeEn(interfaz))
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Icon(Icons.check_circle_rounded, color: e.color, size: 20),
                  const SizedBox(width: 10),
                  Expanded(child: Text(i, style: const TextStyle(fontSize: 14, height: 1.35))),
                ]),
              ),
            if (duraciones.length > 1) ...[
              const SizedBox(height: 12),
              Text(tr('Elige la duración de tu suscripción'), style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
              const SizedBox(height: 10),
              for (final d in duraciones)
                Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: _OpcionDuracion(
                    duracion: d,
                    moneda: p.moneda,
                    precioPlay: precios['${p.googleProducto}|${planBaseDeMeses(d.meses)}'],
                    ahorro: p.ahorro(d),
                    estilo: e,
                    elegida: d.meses == elegida.meses,
                    onTap: () => setState(() => _meses = d.meses),
                  ),
                ),
            ],
            const SizedBox(height: 8),
            _boton(p, ep, planSuscrito, catalogo, sus, api, interfaz, elegida, enApp),
            const SizedBox(height: 12),
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

  Widget _boton(
    PlanServidor p,
    EstadoPlan ep,
    String planSuscrito,
    CatalogoPlanes catalogo,
    Suscripcion? sus,
    PagosApi api,
    String interfaz,
    DuracionPlan duracion,
    bool enApp,
  ) {
    final estilo = ElevatedButton.styleFrom(backgroundColor: EstiloPlan.de(p).color);
    final compra = ref.watch(comprasPlayProvider);
    // En Play se puede cambiar de duración dentro del mismo plan.
    final otraDuracion = enApp && sus != null && sus.googleVigente && sus.googlePlanBase != planBaseDeMeses(duracion.meses);
    if (p.id == planSuscrito && !otraDuracion) {
      return ElevatedButton(style: estilo, onPressed: null, child: Text(tr('PLAN ACTUAL')));
    }
    // DEMO o sin servidor: se elige en el dispositivo, como antes.
    if (!ep.servidor) {
      return ElevatedButton(
        style: estilo,
        onPressed: () {
          if (ref.read(progressProvider.notifier).elegirPlan(p.id)) {
            avisoPago(context, tr('Plan "{plan}" activado (pago real en la fase 2)', {'plan': p.nombreEn(interfaz)}), color: OL.verde);
          }
        },
        child: Text(tr('ELEGIR {plan}', {'plan': p.nombreEn(interfaz).toUpperCase()})),
      );
    }
    const indicador = SizedBox(
      width: 18,
      height: 18,
      child: CircularProgressIndicator(strokeWidth: 2, color: OL.morado),
    );
    if (enApp) {
      // Android: solo Google Play. Una suscripción pagada en la web se gestiona allí.
      if (sus != null && sus.stripeVigente) {
        return OutlinedButton(onPressed: null, child: Text(tr('Tu suscripción se gestiona en la web')));
      }
      if (!catalogo.googleDisponible || p.googleProducto == null) {
        return ElevatedButton(style: estilo, onPressed: null, child: Text(tr('Pagos próximamente')));
      }
      final cambio = sus != null && sus.googleVigente;
      return ElevatedButton(
        key: const ValueKey('suscribirme'),
        style: estilo,
        onPressed: compra.procesando ? null : () => _comprarPlay(p, duracion.meses, cambio: cambio),
        child: compra.procesando
            ? indicador
            : Text(cambio ? (p.id == planSuscrito ? tr('Cambiar la duración') : tr('Cambiar a este plan')) : tr('Continuar')),
      );
    }
    // Ya paga con Stripe: los cambios de plan y de duración se hacen en el portal.
    if (sus != null && sus.stripeVigente && sus.puedeGestionar) {
      return OutlinedButton(
        onPressed: _esperando ? null : () => _abrir(api.portal),
        child: _esperando ? indicador : Text(tr('Cambiar de plan')),
      );
    }
    if (!catalogo.pagosDisponible) {
      return ElevatedButton(style: estilo, onPressed: null, child: Text(tr('Pagos próximamente')));
    }
    return ElevatedButton(
      key: const ValueKey('suscribirme'),
      style: estilo,
      onPressed: _esperando ? null : () => _suscribirme(p, api, duracion.meses),
      child: _esperando ? indicador : Text(tr('Continuar')),
    );
  }
}

/// Una duración: meses, precio total, precio por mes y ahorro.
class _OpcionDuracion extends StatelessWidget {
  const _OpcionDuracion({
    required this.duracion,
    required this.moneda,
    this.precioPlay,
    required this.ahorro,
    required this.estilo,
    required this.elegida,
    required this.onTap,
  });
  final DuracionPlan duracion;
  final String moneda;

  /// Precio de Google Play en la moneda del alumno (Android); si no, el del catálogo.
  final PrecioPlay? precioPlay;
  final int ahorro;
  final EstiloPlan estilo;
  final bool elegida;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final d = duracion;
    final texto = elegida ? OL.blanco : OL.texto;
    final suave = elegida ? OL.blanco.withValues(alpha: .85) : OL.gris;
    return Semantics(
      selected: elegida,
      child: Tarjeta(
        key: ValueKey('duracion-${d.meses}'),
        color: elegida ? estilo.color : OL.blanco,
        borde: elegida ? estilo.color : null,
        sombra: false,
        radio: 18,
        onTap: onTap,
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        child: Row(children: [
          Icon(elegida ? Icons.radio_button_checked_rounded : Icons.radio_button_unchecked_rounded, color: elegida ? OL.blanco : OL.gris),
          const SizedBox(width: 12),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(textoDuracion(d.meses), style: TextStyle(fontWeight: FontWeight.w800, color: texto)),
              Text(precioPlay?.texto ?? formatoPrecio(d.precio, moneda),
                  style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: texto, height: 1.1)),
              Text(tr('{precio} al mes', {'precio': precioPlay?.porMes(d.meses) ?? formatoPrecio((d.porMes * 100).round() / 100, moneda)}),
                  style: TextStyle(fontSize: 12, color: suave)),
            ]),
          ),
          Etiqueta(
            ahorro > 0 ? tr('Ahorra {n} %', {'n': ahorro}) : tr('Sin descuento'),
            color: elegida ? estilo.color : (ahorro > 0 ? OL.verde : OL.gris),
            fondo: elegida ? OL.blanco : null,
          ),
        ]),
      ),
    );
  }
}
