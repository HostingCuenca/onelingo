import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/i18n/i18n.dart';

/// Motivos de `POST /reportes-ia` (backend/src/routes/reportes.ts).
Map<String, String> get _motivos => {
  'ofensivo': tr('Ofensiva'),
  'incorrecto': tr('Incorrecta'),
  'inapropiado': tr('Inapropiada'),
  'otro': tr('Otro motivo'),
};

/// Denunciar una respuesta del tutor de IA (política de contenido generado por
/// IA de Google Play): hoja con el motivo y un comentario opcional. Al enviar,
/// «Gracias, lo revisaremos».
Future<void> reportarRespuestaIA(
  BuildContext context, {
  required String origen,
  required String texto,
  Map<String, Object?> contexto = const {},
}) async {
  final messenger = ScaffoldMessenger.maybeOf(context);
  final enviado = await showModalBottomSheet<bool>(
    context: context,
    isScrollControlled: true,
    showDragHandle: true,
    builder: (_) =>
        _HojaReporte(origen: origen, texto: texto, contexto: contexto),
  );
  if (enviado == true) {
    messenger?.showSnackBar(
      SnackBar(content: Text(tr('Gracias, lo revisaremos.'))),
    );
  }
}

class _HojaReporte extends StatefulWidget {
  const _HojaReporte({
    required this.origen,
    required this.texto,
    required this.contexto,
  });
  final String origen;
  final String texto;
  final Map<String, Object?> contexto;

  @override
  State<_HojaReporte> createState() => _HojaReporteState();
}

class _HojaReporteState extends State<_HojaReporte> {
  final comentario = TextEditingController();
  String? motivo;
  bool enviando = false;
  String? error;

  @override
  void dispose() {
    comentario.dispose();
    super.dispose();
  }

  Future<void> _enviar() async {
    setState(() {
      enviando = true;
      error = null;
    });
    final ok = await Sync.instancia.reportarIA(
      origen: widget.origen,
      texto: widget.texto,
      motivo: motivo!,
      comentario: comentario.text,
      contexto: widget.contexto,
    );
    if (!mounted) return;
    if (ok) {
      Navigator.pop(context, true);
      return;
    }
    setState(() {
      enviando = false;
      error = Sync.instancia.ultimoError == 'demasiados_reportes'
          ? tr('Enviaste muchos reportes. Inténtalo de nuevo más tarde.')
          : tr('No se pudo enviar el reporte. Inténtalo de nuevo.');
    });
  }

  @override
  Widget build(BuildContext context) => Padding(
    padding: EdgeInsets.fromLTRB(
      20,
      0,
      20,
      20 + MediaQuery.viewInsetsOf(context).bottom,
    ),
    child: SingleChildScrollView(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            tr('Reportar respuesta'),
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 6),
          Text(
            tr(
              'Cuéntanos qué está mal en esta respuesta del tutor. Nuestro equipo la revisará.',
            ),
            style: const TextStyle(color: OL.gris, fontSize: 14),
          ),
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: OL.moradoSuave,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              widget.texto,
              maxLines: 4,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(height: 1.35),
            ),
          ),
          const SizedBox(height: 14),
          Text(
            tr('¿Qué pasó?'),
            style: const TextStyle(fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              for (final m in _motivos.entries)
                ChoiceChip(
                  label: Text(m.value),
                  selected: motivo == m.key,
                  onSelected: enviando
                      ? null
                      : (_) => setState(() => motivo = m.key),
                ),
            ],
          ),
          const SizedBox(height: 14),
          TextField(
            controller: comentario,
            maxLength: 500,
            maxLines: 3,
            minLines: 2,
            enabled: !enviando,
            decoration: InputDecoration(hintText: tr('Comentario (opcional)')),
          ),
          if (error != null) ...[
            Text(
              error!,
              style: const TextStyle(
                color: OL.rojo,
                fontSize: 13,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 8),
          ],
          FilledButton(
            onPressed: motivo == null || enviando ? null : _enviar,
            child: Text(enviando ? tr('Enviando…') : tr('Enviar reporte')),
          ),
        ],
      ),
    ),
  );
}
