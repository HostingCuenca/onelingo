import 'dart:convert';

import '../../core/api/sync.dart';
import '../../core/biblioteca.dart';
import '../../core/state/providers.dart';

/// Sesión que la app entrega al visor de la videollamada (web/avatar) al
/// recibir «onelingo-avatar-ready». Va por mensaje, nunca en la URL.
String datosVisor(
  ProgressState s, {
  int? tema,
  String? objetivoId,
}) => jsonEncode({
  'type': 'onelingo-avatar-init',
  'api': Sync.baseUrl,
  'token': Sync.instancia.token,
  'nivel': s.nivelActual.clamp(1, 10),
  'idiomaMeta': s.idiomaMeta,
  'idiomaNativo': s.idiomaNativo,
  'tema': ?tema,
  'objetivoId': ?objetivoId,
  'contexto':
      'Sectores: ${s.sectores.join(', ')}. Objetivos: ${s.objetivos.join(', ')}. '
      'Prioridades de aprendizaje: ${RutaBiblioteca.prioridades(s.diagnostico, s.practicas).take(3).join(', ')}. '
      'Temas a reforzar: ${((s.diagnostico?['refuerzo'] as List?) ?? []).take(5).join(', ')}.',
});
