import 'dart:js_interop';
import 'dart:ui_web' as ui_web;

import 'package:web/web.dart' as web;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/api/sync.dart';
import '../../core/state/providers.dart';
import '../../core/i18n/i18n.dart';
import 'tutores_3d.dart';
import 'visor_datos.dart';

/// Same-origin isolated viewer; credentials stay in memory and never in URLs.
class AvatarScreen extends ConsumerStatefulWidget {
  const AvatarScreen({
    super.key,
    required this.tutorId,
    this.tema,
    this.objetivoId,
  });

  /// Tutor elegido en «Tutores con IA»: el visor se abre integrado (sin su
  /// galería ni cabecera propias) y directamente con este tutor.
  final String tutorId;

  /// Situación y objetivo con que empieza la llamada (desde una situación).
  final int? tema;
  final String? objetivoId;
  @override
  ConsumerState<AvatarScreen> createState() => _AvatarScreenState();
}

class _AvatarScreenState extends ConsumerState<AvatarScreen> {
  late final web.HTMLIFrameElement frame;
  late final String viewType;
  late final JSFunction listener;
  @override
  void initState() {
    super.initState();
    viewType = 'avatar-${DateTime.now().microsecondsSinceEpoch}';
    frame = web.HTMLIFrameElement()
      ..src = Uri.base
          .resolve(
            '/avatar/index.html?v=avatar32&embebido=1&tutor=${Uri.encodeComponent(widget.tutorId)}&ui=${I18n.idioma.value}',
          )
          .toString()
      ..title = tr('Practica con un tutor de IA')
      ..allow = 'microphone; autoplay'
      ..style.border = '0'
      ..style.width = '100%'
      ..style.height = '100%';
    listener = ((web.MessageEvent event) {
      if (event.origin != web.window.location.origin ||
          event.source != frame.contentWindow) {
        return;
      }
      final dato = event.data.dartify();
      // La flecha de la llamada (dentro del visor) vuelve a «Tutores con IA».
      if (dato == 'onelingo-avatar-salir') {
        if (mounted) context.canPop() ? context.pop() : context.go('/tutores');
        return;
      }
      if (dato != 'onelingo-avatar-ready') return;
      frame.contentWindow?.postMessage(
        datosVisor(
          ref.read(progressProvider),
          tema: widget.tema,
          objetivoId: widget.objetivoId,
        ).toJS,
        web.window.location.origin.toJS,
      );
    }).toJS;
    web.window.addEventListener('message', listener);
    ui_web.platformViewRegistry.registerViewFactory(viewType, (_) => frame);
  }

  // En otra pestaña de la app el visor sigue montado (IndexedStack): se pausa.
  bool _visible = true;
  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final visible = TickerMode.valuesOf(context).enabled;
    if (visible == _visible) return;
    _visible = visible;
    frame.contentWindow?.postMessage(
      '{"type":"onelingo-avatar-${visible ? 'reanudar' : 'pausa'}"}'.toJS,
      web.window.location.origin.toJS,
    );
  }

  @override
  void dispose() {
    web.window.removeEventListener('message', listener);
    frame.src = 'about:blank';
    super.dispose();
  }

  @override
  // La llamada ocupa toda la pantalla (como una videollamada): su cabecera,
  // con el nombre del tutor y la flecha para volver, está dentro del visor.
  Widget build(BuildContext context) => Sync.instancia.token == null
      ? Scaffold(
          appBar: AppBar(
            leading: IconButton(
              icon: const Icon(Icons.arrow_back),
              tooltip: tr('Tutores'),
              onPressed: () =>
                  context.canPop() ? context.pop() : context.go('/tutores'),
            ),
            title: Text(
              tr('{tutor} · videollamada', {
                'tutor': tutor3d(widget.tutorId)?.nombre ?? tr('Tutor'),
              }),
            ),
          ),
          body: _SinSesion(
            nombre: tutor3d(widget.tutorId)?.nombre ?? tr('tu tutor'),
          ),
        )
      : Scaffold(
          backgroundColor: Colors.white,
          body: SafeArea(
            bottom: false,
            child: HtmlElementView(viewType: viewType),
          ),
        );
}

/// Sin sesión el tutor no puede conversar: se pide iniciarla en lugar de
/// abrir una videollamada que no respondería.
class _SinSesion extends StatelessWidget {
  const _SinSesion({required this.nombre});
  final String nombre;

  @override
  Widget build(BuildContext context) => Center(
    child: Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.lock_outline_rounded, size: 40),
          const SizedBox(height: 12),
          Text(
            tr('Inicia sesión para hablar con {nombre}', {'nombre': nombre}),
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 6),
          Text(
            tr(
              'Tu tutor recuerda tu nivel, tus correcciones y lo que practicaste en otras llamadas.',
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () => context.push('/login'),
            child: Text(tr('Iniciar sesión')),
          ),
        ],
      ),
    ),
  );
}
