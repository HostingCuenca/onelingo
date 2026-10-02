import 'package:flutter/material.dart';

import '../../core/conexion.dart';
import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';

class ConnectionBanner extends StatelessWidget {
  const ConnectionBanner({super.key, required this.child});
  final Widget child;
  @override
  Widget build(BuildContext context) => ValueListenableBuilder<EstadoConexion>(
    valueListenable: Conexion.estado,
    builder: (context, estado, _) => Column(
      // El aviso se pinta después del navegador para que BlockSemantics
      // de sus rutas no lo oculte a lectores de pantalla.
      verticalDirection: VerticalDirection.up,
      children: [
        Expanded(
          child: LayoutBuilder(
            builder: (context, constraints) => MediaQuery(
              data: MediaQuery.of(context).copyWith(size: constraints.biggest),
              child: child,
            ),
          ),
        ),
        if (estado == EstadoConexion.sinConexion ||
            estado == EstadoConexion.servicioNoDisponible)
          Semantics(
            liveRegion: true,
            child: Material(
              color: OL.naranjaSuave,
              child: SafeArea(
                bottom: false,
                child: Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 8,
                  ),
                  child: Row(
                    children: [
                      const Icon(
                        Icons.wifi_off_rounded,
                        color: OL.morado,
                        size: 22,
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          estado == EstadoConexion.sinConexion
                              ? tr(
                                  'Sin conexión con OneLingo. Comprueba tu conexión.',
                                )
                              : tr(
                                  'El servidor no está disponible temporalmente.',
                                ),
                          style: const TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      TextButton(
                        onPressed: Conexion.comprobar,
                        child: Text(tr('Reintentar')),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
      ],
    ),
  );
}
