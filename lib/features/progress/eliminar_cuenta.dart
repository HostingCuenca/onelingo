import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/i18n/i18n.dart';
import '../../core/pagos/providers.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/enlaces_legales.dart';
import '../plans/plans_screen.dart' show urlGestionPlay;

/// Perfil → Eliminar cuenta (requisito de Google Play). Pide escribir la
/// palabra de confirmación, avisa si hay una suscripción de Google Play que
/// cancelar y, al terminar, cierra la sesión y vuelve al inicio. El servidor
/// rechaza las cuentas demo (`DELETE /usuarios/me` → 403).
Future<void> confirmarEliminarCuenta(
  BuildContext context,
  WidgetRef ref,
) async {
  final sus = ref.read(estadoPlanProvider).suscripcion;
  final google = sus != null && sus.googleVigente && !sus.cancelaAlFinal;
  final stripe = sus != null && sus.stripeVigente;
  final messenger = ScaffoldMessenger.maybeOf(context);
  final r = await showDialog<Map<String, dynamic>>(
    context: context,
    barrierDismissible: false,
    builder: (_) => _DialogoEliminar(google: google, stripe: stripe),
  );
  if (r == null || !context.mounted) return;
  final gp = r['googlePlay'];
  if (gp is Map && gp['debeCancelar'] == true) {
    final paquete = ref.read(catalogoPlanesProvider).googlePaquete;
    final producto = gp['producto'] as String?;
    await showDialog<void>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(tr('Cancela tu suscripción en Google Play')),
        content: Text(
          tr(
            'Tu cuenta se eliminó, pero la suscripción de Google Play sigue activa. Cancélala en Google Play para que no se renueve.',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: Text(tr('Entendido')),
          ),
          FilledButton(
            onPressed: () {
              Navigator.pop(ctx);
              abrirPaginaLegal(urlGestionPlay(paquete, producto));
            },
            child: Text(tr('Abrir Google Play')),
          ),
        ],
      ),
    );
  }
  // Sin sesión y con el estado local vacío, el router vuelve a la bienvenida.
  ref.read(progressProvider.notifier).reiniciar();
  messenger?.showSnackBar(
    SnackBar(content: Text(tr('Tu cuenta fue eliminada.'))),
  );
}

class _DialogoEliminar extends StatefulWidget {
  const _DialogoEliminar({required this.google, required this.stripe});
  final bool google;
  final bool stripe;

  @override
  State<_DialogoEliminar> createState() => _DialogoEliminarState();
}

class _DialogoEliminarState extends State<_DialogoEliminar> {
  final confirmacion = TextEditingController();
  bool eliminando = false;
  String? error;

  /// Palabra que hay que escribir (traducida: «DELETE» en inglés).
  String get _palabra => tr('ELIMINAR');
  bool get _escrita =>
      confirmacion.text.trim().toUpperCase() == _palabra.toUpperCase();

  @override
  void dispose() {
    confirmacion.dispose();
    super.dispose();
  }

  String _mensaje(String? codigo) => switch (codigo) {
    'cuenta_demo' => tr('Las cuentas de demostración no se pueden eliminar.'),
    'cancelacion_fallida' || 'cancelacion_no_disponible' => tr(
      'No pudimos cancelar tu suscripción, así que tu cuenta no se eliminó. Inténtalo más tarde o escríbenos a infoonelingo@gmail.com.',
    ),
    _ => tr(
      'No se pudo eliminar la cuenta. Revisa tu conexión e inténtalo de nuevo.',
    ),
  };

  Future<void> _eliminar() async {
    setState(() {
      eliminando = true;
      error = null;
    });
    final r = await Sync.instancia.eliminarCuenta();
    if (!mounted) return;
    if (r != null) {
      Navigator.pop(context, r);
      return;
    }
    setState(() {
      eliminando = false;
      error = _mensaje(Sync.instancia.ultimoCodigo);
    });
  }

  @override
  Widget build(BuildContext context) => AlertDialog(
    title: Text(tr('¿Eliminar tu cuenta?')),
    content: SingleChildScrollView(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            tr(
              'Se borrarán para siempre tu perfil, tu progreso, tus errores, tus conversaciones con los tutores y tu historial. No se puede deshacer.',
            ),
          ),
          if (widget.stripe) ...[
            const SizedBox(height: 8),
            Text(
              tr(
                'Tu suscripción pagada en la web se cancela al momento y no se te volverá a cobrar.',
              ),
              style: const TextStyle(color: OL.gris, fontSize: 13),
            ),
          ],
          if (widget.google) ...[
            const SizedBox(height: 10),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: OL.amarilloSuave,
                borderRadius: BorderRadius.circular(10),
              ),
              child: Text(
                tr(
                  'Tienes una suscripción de Google Play. Eliminar la cuenta no la cancela: cancélala en Google Play para que no se renueve.',
                ),
                style: const TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
          const SizedBox(height: 14),
          Text(
            tr('Escribe {palabra} para confirmar.', {'palabra': _palabra}),
            style: const TextStyle(fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 6),
          TextField(
            controller: confirmacion,
            enabled: !eliminando,
            autocorrect: false,
            textCapitalization: TextCapitalization.characters,
            onChanged: (_) => setState(() {}),
            decoration: InputDecoration(hintText: _palabra),
          ),
          if (error != null) ...[
            const SizedBox(height: 8),
            Text(
              error!,
              style: const TextStyle(
                color: OL.rojo,
                fontSize: 13,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
          const SizedBox(height: 4),
          TextButton(
            style: TextButton.styleFrom(padding: EdgeInsets.zero),
            onPressed: () => abrirPaginaLegal(urlEliminarCuenta),
            child: Text(tr('Qué se borra y qué se conserva')),
          ),
        ],
      ),
    ),
    actions: [
      TextButton(
        onPressed: eliminando ? null : () => Navigator.pop(context),
        child: Text(tr('Cancelar')),
      ),
      FilledButton(
        style: FilledButton.styleFrom(backgroundColor: OL.rojo),
        onPressed: _escrita && !eliminando ? _eliminar : null,
        child: Text(eliminando ? tr('Eliminando…') : tr('Eliminar cuenta')),
      ),
    ],
  );
}
