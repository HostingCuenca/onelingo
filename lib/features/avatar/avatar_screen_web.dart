import 'dart:convert';
import 'dart:js_interop';
import 'dart:ui_web' as ui_web;

import 'package:web/web.dart' as web;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/api/sync.dart';
import '../../core/state/providers.dart';
import '../../core/biblioteca.dart';
import 'tutores_3d.dart';

/// Same-origin isolated viewer; credentials stay in memory and never in URLs.
class AvatarScreen extends ConsumerStatefulWidget {
  const AvatarScreen({super.key, required this.tutorId});

  /// Tutor elegido en «Tutores con IA»: el visor se abre integrado (sin su
  /// galería ni cabecera propias) y directamente con este tutor.
  final String tutorId;
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
            '/avatar/index.html?v=avatar24&embebido=1&tutor=${Uri.encodeComponent(widget.tutorId)}',
          )
          .toString()
      ..title = 'Practica con un tutor de IA'
      ..allow = 'microphone; autoplay'
      ..style.border = '0'
      ..style.width = '100%'
      ..style.height = '100%';
    listener = ((web.MessageEvent event) {
      if (event.origin != web.window.location.origin ||
          event.source != frame.contentWindow) {
        return;
      }
      if (event.data.dartify() != 'onelingo-avatar-ready') return;
      final s = ref.read(progressProvider);
      frame.contentWindow?.postMessage(
        jsonEncode({
          'type': 'onelingo-avatar-init',
          'api': Sync.baseUrl,
          'token': Sync.instancia.token,
          'nivel': s.nivelActual.clamp(1, 10),
          'idiomaMeta': s.idiomaMeta,
          'idiomaNativo': s.idiomaNativo,
          'contexto':
              'Sectores: ${s.sectores.join(', ')}. Objetivos: ${s.objetivos.join(', ')}. '
              'Prioridades de aprendizaje: ${RutaBiblioteca.prioridades(s.diagnostico, s.practicas).take(3).join(', ')}. '
              'Temas a reforzar: ${((s.diagnostico?['refuerzo'] as List?) ?? []).take(5).join(', ')}.',
        }).toJS,
        web.window.location.origin.toJS,
      );
    }).toJS;
    web.window.addEventListener('message', listener);
    ui_web.platformViewRegistry.registerViewFactory(viewType, (_) => frame);
  }

  @override
  void dispose() {
    web.window.removeEventListener('message', listener);
    frame.src = 'about:blank';
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      leading: IconButton(
        icon: const Icon(Icons.arrow_back),
        tooltip: 'Tutores',
        onPressed: () =>
            context.canPop() ? context.pop() : context.go('/tutores'),
      ),
      title: Text(
        '${tutor3d(widget.tutorId)?.nombre ?? 'Tutor'} · videollamada',
      ),
    ),
    body: Sync.instancia.token == null
        ? _SinSesion(nombre: tutor3d(widget.tutorId)?.nombre ?? 'tu tutor')
        : HtmlElementView(viewType: viewType),
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
            'Inicia sesión para hablar con $nombre',
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 6),
          const Text(
            'Tu tutor recuerda tu nivel, tus correcciones y lo que practicaste en otras llamadas.',
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: () => context.push('/login'),
            child: const Text('Iniciar sesión'),
          ),
        ],
      ),
    ),
  );
}
