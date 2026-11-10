import 'package:flutter/material.dart';

import '../../core/api/sync.dart';
import '../../core/i18n/i18n.dart';
import '../../app/theme.dart';

/// Código de referido desde el perfil: para quien se registró con Google o no
/// lo escribió al crear la cuenta. Se guarda una sola vez; luego solo se ve.
Future<void> abrirCodigoReferido(BuildContext context) =>
    showDialog(context: context, builder: (_) => const _CodigoReferido());

class _CodigoReferido extends StatefulWidget {
  const _CodigoReferido();

  @override
  State<_CodigoReferido> createState() => _CodigoReferidoState();
}

class _CodigoReferidoState extends State<_CodigoReferido> {
  final campo = TextEditingController();
  bool cargando = true, guardando = false;
  String? actual, error;

  @override
  void initState() {
    super.initState();
    Sync.instancia.miReferido().then((c) {
      if (mounted) setState(() => (actual = c, cargando = false));
    });
  }

  @override
  void dispose() {
    campo.dispose();
    super.dispose();
  }

  Future<void> _guardar() async {
    if (campo.text.trim().isEmpty) return;
    setState(() => (guardando = true, error = null));
    final c = await Sync.instancia.ponerReferido(campo.text);
    if (!mounted) return;
    setState(() {
      guardando = false;
      if (c != null) {
        actual = c;
      } else {
        error = Sync.instancia.ultimoError;
      }
    });
  }

  @override
  Widget build(BuildContext context) => AlertDialog(
    title: Text(tr('Código de referido')),
    content: cargando
        ? const SizedBox(
            height: 60,
            child: Center(child: CircularProgressIndicator()),
          )
        : actual != null
        ? Text(tr('Tu cuenta tiene el código {codigo}.', {'codigo': actual}))
        : Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                tr(
                  'Si alguien te recomendó OneLingo, escribe su código. Solo se puede poner una vez.',
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: campo,
                autofocus: true,
                textCapitalization: TextCapitalization.characters,
                autocorrect: false,
                onSubmitted: (_) => _guardar(),
                decoration: InputDecoration(
                  hintText: tr('Código'),
                  prefixIcon: const Icon(Icons.handshake_outlined),
                ),
              ),
              if (error != null && error!.isNotEmpty) ...[
                const SizedBox(height: 8),
                Text(
                  error!,
                  style: const TextStyle(
                    color: OL.rojo,
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ],
          ),
    actions: [
      TextButton(
        onPressed: () => Navigator.pop(context),
        child: Text(actual != null ? tr('Cerrar') : tr('Cancelar')),
      ),
      if (!cargando && actual == null)
        TextButton(
          onPressed: guardando ? null : _guardar,
          child: Text(guardando ? tr('Guardando…') : tr('Guardar')),
        ),
    ],
  );
}
