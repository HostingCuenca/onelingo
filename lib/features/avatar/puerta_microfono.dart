import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:record/record.dart';

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';
import '../../shared/widgets/widgets.dart';

/// Pide el permiso del micrófono (el diálogo de Android o del navegador) y dice
/// si quedó concedido; con `pedir: false` solo lo consulta, sin diálogo. Sin
/// plugin (pruebas de widgets) no se bloquea.
final permisoMicrofonoProvider = Provider<Future<bool> Function({bool pedir})>(
  (_) => ({pedir = true}) async {
    AudioRecorder? grabadora;
    try {
      grabadora = AudioRecorder();
      return await grabadora.hasPermission(request: pedir);
    } on MissingPluginException {
      return true;
    } catch (_) {
      return false;
    } finally {
      await grabadora?.dispose().catchError((_) {});
    }
  },
);

/// Sin permiso del micrófono no se entra al tutor (videollamada y chat): se
/// pide cada vez que se intenta entrar y, al volver de Ajustes, se comprueba
/// otra vez.
class PuertaMicrofono extends ConsumerStatefulWidget {
  const PuertaMicrofono({super.key, required this.child});
  final Widget child;

  @override
  ConsumerState<PuertaMicrofono> createState() => _PuertaMicrofonoState();
}

class _PuertaMicrofonoState extends ConsumerState<PuertaMicrofono>
    with WidgetsBindingObserver {
  bool? _permitido;
  bool _pidiendo = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _pedir();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState estado) {
    // Al volver (de Ajustes, o justo tras negar el diálogo) solo se consulta:
    // pedirlo aquí volvía a sacar el diálogo nada más negarlo.
    if (estado == AppLifecycleState.resumed && _permitido == false) {
      _pedir(pedir: false);
    }
  }

  Future<void> _pedir({bool pedir = true}) async {
    if (_pidiendo) return;
    _pidiendo = true;
    final ok = await ref.read(permisoMicrofonoProvider)(pedir: pedir);
    _pidiendo = false;
    if (mounted) setState(() => _permitido = ok);
  }

  @override
  Widget build(BuildContext context) {
    final permitido = _permitido;
    if (permitido == true) return widget.child;
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/tutores'),
        ),
      ),
      body: permitido == null
          ? const Center(child: CircularProgressIndicator())
          : Movil(
              child: Center(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const CircleAvatar(
                        radius: 36,
                        backgroundColor: OL.moradoSuave,
                        child: Icon(
                          Icons.mic_off_rounded,
                          size: 36,
                          color: OL.morado,
                        ),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        tr('Necesitamos tu micrófono'),
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        tr(
                          'Para hablar con tu tutor, OneLingo necesita usar el micrófono. Sin ese permiso no se puede entrar.',
                        ),
                        textAlign: TextAlign.center,
                        style: const TextStyle(color: OL.gris, height: 1.4),
                      ),
                      const SizedBox(height: 20),
                      FilledButton.icon(
                        style: FilledButton.styleFrom(
                          minimumSize: const Size.fromHeight(52),
                        ),
                        onPressed: _pidiendo ? null : _pedir,
                        icon: const Icon(Icons.mic_rounded),
                        label: Text(tr('Permitir micrófono')),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        kIsWeb
                            ? tr(
                                'Si lo bloqueaste, actívalo en el candado de la barra de direcciones del navegador.',
                              )
                            : tr(
                                'Si lo negaste antes, actívalo en Ajustes › Apps › OneLingo › Permisos › Micrófono.',
                              ),
                        textAlign: TextAlign.center,
                        style: const TextStyle(color: OL.gris, fontSize: 12),
                      ),
                    ],
                  ),
                ),
              ),
            ),
    );
  }
}
