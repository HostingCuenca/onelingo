import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';
import '../../core/pagos/providers.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Vuelta de Stripe en la web: `#/pago?estado=ok&session_id=…`,
/// `?estado=cancelado` o `?estado=portal` (contrato de pagos).
class PagoScreen extends ConsumerStatefulWidget {
  const PagoScreen({super.key, required this.estado, this.sessionId});
  final String estado;
  final String? sessionId;

  @override
  ConsumerState<PagoScreen> createState() => _PagoScreenState();
}

class _PagoScreenState extends ConsumerState<PagoScreen> {
  bool _cargando = true;
  bool _ok = false;
  String _mensaje = '';
  Timer? _volver;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _procesar());
  }

  @override
  void dispose() {
    _volver?.cancel();
    super.dispose();
  }

  Future<void> _procesar() async {
    if (!mounted) return;
    final suscripcion = ref.read(suscripcionProvider.notifier);
    switch (widget.estado) {
      case 'ok':
        final id = widget.sessionId ?? '';
        if (id.isEmpty) {
          _terminar(false, tr('No se pudo confirmar el pago.'));
          return;
        }
        final r = await ref.read(pagosApiProvider).confirmar(id);
        if (!mounted) return;
        if (!r.ok) {
          _terminar(false, r.error);
          return;
        }
        suscripcion.aplicar(r.cuerpo);
        final s = Suscripcion.fromJson(r.cuerpo);
        if (!s.acceso) {
          _terminar(false, tr('Tu pago aún no se confirma. Vuelve a revisar en unos minutos.'));
          return;
        }
        final interfaz = ref.read(progressProvider).interfaz;
        final plan =
            ref.read(catalogoPlanesProvider).plan(s.planId)?.nombreEn(interfaz) ??
            s.planId;
        _terminar(true, tr('¡Listo! Tu plan {plan} está activo', {'plan': plan}));
        _volver = Timer(const Duration(seconds: 4), _alInicio);
      case 'cancelado':
        _terminar(false, tr('Pago cancelado'));
      case 'portal':
        await suscripcion.refrescar();
        if (mounted) context.go('/planes');
      default:
        _alInicio();
    }
  }

  void _terminar(bool ok, String mensaje) {
    if (!mounted) return;
    setState(() {
      _cargando = false;
      _ok = ok;
      _mensaje = mensaje;
    });
  }

  void _alInicio() {
    _volver?.cancel();
    if (mounted) context.go('/inicio');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Movil(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(24, 24, 24, 16),
            child: Column(
              children: [
                Expanded(
                  child: Center(
                    child: _cargando
                        ? Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const CircularProgressIndicator(),
                              const SizedBox(height: 16),
                              Text(tr('Confirmando tu pago…'), style: const TextStyle(color: OL.gris)),
                            ],
                          )
                        : Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(
                                _ok ? Icons.check_circle_rounded : Icons.info_outline_rounded,
                                size: 72,
                                color: _ok ? OL.verde : OL.naranja,
                              ),
                              const SizedBox(height: 16),
                              Text(
                                _mensaje,
                                textAlign: TextAlign.center,
                                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800, height: 1.3),
                              ),
                            ],
                          ),
                  ),
                ),
                BotonPrincipal(
                  onPressed: _cargando ? null : _alInicio,
                  child: Text(tr('Volver al inicio')),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
