import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../app/theme.dart';
import '../../core/content/curriculum.dart' show idiomas;
import '../../core/i18n/i18n.dart';
import '../../core/pagos/providers.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';
import 'estilo_plan.dart';

/// Plan Empresarial: qué incluye y el formulario de cotización
/// (`POST /cotizaciones`; el administrador la atiende desde el panel).
class EmpresaScreen extends ConsumerStatefulWidget {
  const EmpresaScreen({super.key});

  @override
  ConsumerState<EmpresaScreen> createState() => _EmpresaScreenState();
}

class _EmpresaScreenState extends ConsumerState<EmpresaScreen> {
  final _form = GlobalKey<FormState>();
  final _empresa = TextEditingController();
  final _empleados = TextEditingController();
  final _nombre = TextEditingController();
  late final _email = TextEditingController(text: ref.read(progressProvider).email);
  final _telefono = TextEditingController();
  final _mensaje = TextEditingController();
  final _idiomas = <String>{};
  bool _enviando = false;
  bool _faltanIdiomas = false;

  /// Correo al que se respondió (la solicitud ya se envió).
  String? _enviada;

  @override
  void dispose() {
    for (final c in [_empresa, _empleados, _nombre, _email, _telefono, _mensaje]) {
      c.dispose();
    }
    super.dispose();
  }

  Future<void> _enviar() async {
    setState(() => _faltanIdiomas = _idiomas.isEmpty);
    if (!(_form.currentState?.validate() ?? false) || _idiomas.isEmpty) return;
    setState(() => _enviando = true);
    final email = _email.text.trim();
    final r = await ref.read(pagosApiProvider).cotizacion({
      'empresa': _empresa.text.trim(),
      'empleados': int.parse(_empleados.text.trim()),
      'idiomas': [for (final c in idiomasDePago) if (_idiomas.contains(c)) c],
      'nombre': _nombre.text.trim(),
      'email': email,
      'telefono': _telefono.text.trim(),
      'mensaje': _mensaje.text.trim(),
    });
    if (!mounted) return;
    setState(() {
      _enviando = false;
      if (r.ok) _enviada = email;
    });
    if (!r.ok) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(r.error), backgroundColor: OL.rojo));
    }
  }

  String? _requerido(String? v) => (v ?? '').trim().isEmpty ? tr('Campo obligatorio') : null;

  @override
  Widget build(BuildContext context) {
    const e = EstiloPlan.empresa;
    final ventajas = [
      tr('Para equipos de cualquier tamaño'),
      tr('Cada persona con su propio perfil y progreso'),
      tr('Los 10 idiomas disponibles'),
      tr('Precio según el número de personas'),
      tr('Informes del avance de tu equipo'),
      tr('Disponible en app y web'),
    ];
    return Scaffold(
      appBar: AppBar(title: Text(tr('Plan Empresarial'))),
      body: Movil(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
          children: [
            Tarjeta(
              color: e.suave,
              borde: Colors.transparent,
              sombra: false,
              child: Row(children: [
                const IconoPlan(e, tamano: 64),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(tr('Empresarial'), style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800)),
                    Text(tr('Para empresas u organizaciones'), style: TextStyle(fontWeight: FontWeight.w800, color: e.color)),
                    Text(tr('Precios personalizados'), style: const TextStyle(color: OL.gris, fontSize: 12)),
                  ]),
                ),
              ]),
            ),
            const SizedBox(height: 14),
            for (final v in ventajas)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Row(children: [
                  Icon(Icons.check_circle_rounded, color: e.color, size: 20),
                  const SizedBox(width: 10),
                  Expanded(child: Text(v, style: const TextStyle(fontSize: 14))),
                ]),
              ),
            const SizedBox(height: 14),
            if (_enviada != null)
              Tarjeta(
                key: const ValueKey('cotizacion-enviada'),
                color: OL.verdeSuave,
                sombra: false,
                child: Row(children: [
                  const Icon(Icons.mark_email_read_outlined, color: OL.verde, size: 30),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(tr('Recibimos tu solicitud'), style: const TextStyle(fontWeight: FontWeight.w800)),
                      Text(tr('Te escribiremos a {email} con una propuesta.', {'email': _enviada!}),
                          style: const TextStyle(color: OL.gris, fontSize: 13, height: 1.4)),
                    ]),
                  ),
                ]),
              )
            else
              Form(
                key: _form,
                child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                  Text(tr('Solicita una cotización'), style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
                  const SizedBox(height: 10),
                  TextFormField(
                    key: const ValueKey('cot-empresa'),
                    controller: _empresa,
                    decoration: InputDecoration(labelText: tr('Nombre de la empresa *')),
                    validator: _requerido,
                  ),
                  const SizedBox(height: 10),
                  TextFormField(
                    key: const ValueKey('cot-empleados'),
                    controller: _empleados,
                    keyboardType: TextInputType.number,
                    inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                    decoration: InputDecoration(labelText: tr('Número de empleados *'), hintText: tr('Ej. 50')),
                    validator: (v) => (int.tryParse((v ?? '').trim()) ?? 0) < 1 ? tr('Indica cuántas personas') : null,
                  ),
                  const SizedBox(height: 14),
                  Text(tr('Idioma(s) de interés *'), style: const TextStyle(fontWeight: FontWeight.w700)),
                  const SizedBox(height: 6),
                  Wrap(spacing: 8, runSpacing: 8, children: [
                    for (final l in idiomas)
                      if (idiomasDePago.contains(l.code))
                        FilterChip(
                          key: ValueKey('cot-idioma-${l.code}'),
                          label: Text(l.nombre),
                          selected: _idiomas.contains(l.code),
                          onSelected: (v) => setState(() {
                            v ? _idiomas.add(l.code) : _idiomas.remove(l.code);
                            if (v) _faltanIdiomas = false;
                          }),
                        ),
                  ]),
                  if (_faltanIdiomas)
                    Padding(
                      padding: const EdgeInsets.only(top: 6),
                      child: Text(tr('Elige al menos un idioma'), style: const TextStyle(color: OL.rojo, fontSize: 12)),
                    ),
                  const SizedBox(height: 14),
                  TextFormField(
                    controller: _nombre,
                    decoration: InputDecoration(labelText: tr('Tu nombre')),
                  ),
                  const SizedBox(height: 10),
                  TextFormField(
                    key: const ValueKey('cot-email'),
                    controller: _email,
                    keyboardType: TextInputType.emailAddress,
                    autocorrect: false,
                    decoration: InputDecoration(labelText: tr('Correo de contacto *')),
                    validator: (v) => RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch((v ?? '').trim()) ? null : tr('Escribe un correo válido.'),
                  ),
                  const SizedBox(height: 10),
                  TextFormField(
                    controller: _telefono,
                    keyboardType: TextInputType.phone,
                    decoration: InputDecoration(labelText: tr('Teléfono (opcional)')),
                  ),
                  const SizedBox(height: 10),
                  TextFormField(
                    controller: _mensaje,
                    maxLines: 3,
                    maxLength: 2000,
                    decoration: InputDecoration(labelText: tr('Mensaje adicional (opcional)'), hintText: tr('Cuéntanos más sobre tus necesidades…')),
                  ),
                  const SizedBox(height: 8),
                  ElevatedButton.icon(
                    key: const ValueKey('cot-enviar'),
                    style: ElevatedButton.styleFrom(backgroundColor: e.color),
                    onPressed: _enviando ? null : _enviar,
                    icon: _enviando
                        ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: OL.blanco))
                        : const Icon(Icons.send_rounded),
                    label: Text(tr('Solicitar cotización')),
                  ),
                ]),
              ),
          ],
        ),
      ),
    );
  }
}
