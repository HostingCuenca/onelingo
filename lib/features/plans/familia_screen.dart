import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../app/theme.dart';
import '../../core/api/pagos_api.dart';
import '../../core/i18n/i18n.dart';
import '../../core/pagos/providers.dart';
import '../../shared/widgets/widgets.dart';
import 'plans_screen.dart' show avisoPago;

/// Plan familiar: el titular añade o quita personas por correo; un miembro ve
/// quién paga su plan y puede salir. Cada persona usa su propia cuenta.
class FamiliaScreen extends ConsumerStatefulWidget {
  const FamiliaScreen({super.key});

  @override
  ConsumerState<FamiliaScreen> createState() => _FamiliaScreenState();
}

class _FamiliaScreenState extends ConsumerState<FamiliaScreen> {
  Familia? _familia;
  String? _error;
  bool _enviando = false;
  final _correo = TextEditingController();

  @override
  void initState() {
    super.initState();
    _cargar();
  }

  @override
  void dispose() {
    _correo.dispose();
    super.dispose();
  }

  Future<void> _cargar() async {
    final r = await ref.read(pagosApiProvider).familia();
    if (!mounted) return;
    setState(() {
      _familia = r.ok ? Familia.fromJson(r.cuerpo) : null;
      _error = r.ok ? null : r.error;
    });
  }

  /// Aplica la respuesta (la familia actualizada) y refresca la suscripción.
  Future<bool> _accion(Future<RespuestaPago> Function() pedir) async {
    setState(() => _enviando = true);
    final r = await pedir();
    if (!mounted) return false;
    setState(() {
      _enviando = false;
      if (r.ok) _familia = Familia.fromJson(r.cuerpo);
    });
    if (!r.ok) avisoPago(context, r.error);
    ref.read(suscripcionProvider.notifier).refrescar();
    return r.ok;
  }

  Future<void> _invitar() async {
    final email = _correo.text.trim().toLowerCase();
    if (!RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(email)) {
      avisoPago(context, tr('Escribe un correo válido.'));
      return;
    }
    if (await _accion(() => ref.read(pagosApiProvider).invitarFamiliar(email)) && mounted) {
      _correo.clear();
      final activo = _familia?.miembros.where((m) => m.email == email).firstOrNull?.activo ?? false;
      avisoPago(
        context,
        activo
            ? tr('{email} ya tiene acceso a tu plan.', {'email': email})
            : tr('Invitación enviada a {email}: tendrá acceso al crear su cuenta con ese correo.', {'email': email}),
        color: OL.verde,
      );
    }
  }

  Future<bool> _confirmar(String titulo, String texto, String boton) async =>
      await showDialog<bool>(
        context: context,
        builder: (c) => AlertDialog(
          title: Text(titulo),
          content: Text(texto),
          actions: [
            TextButton(onPressed: () => Navigator.pop(c, false), child: Text(tr('Cancelar'))),
            TextButton(onPressed: () => Navigator.pop(c, true), child: Text(boton)),
          ],
        ),
      ) ??
      false;

  Future<void> _quitar(MiembroFamilia m) async {
    if (!await _confirmar(
      tr('¿Quitar a {email}?', {'email': m.email}),
      tr('Dejará de tener acceso por tu plan. Su progreso se conserva en su cuenta.'),
      tr('Quitar'),
    )) {
      return;
    }
    await _accion(() => ref.read(pagosApiProvider).quitarFamiliar(m.email));
  }

  Future<void> _salir() async {
    if (!await _confirmar(
      tr('¿Salir del plan familiar?'),
      tr('Perderás el acceso que te da este plan. Tu progreso se conserva.'),
      tr('Salir'),
    )) {
      return;
    }
    if (await _accion(() => ref.read(pagosApiProvider).salirDeFamilia()) && mounted) {
      Navigator.of(context).maybePop();
    }
  }

  @override
  Widget build(BuildContext context) {
    final f = _familia;
    return Scaffold(
      appBar: AppBar(title: Text(tr('Plan familiar'))),
      body: Movil(
        child: f == null
            ? Center(
                child: _error == null
                    ? const CircularProgressIndicator()
                    : Padding(
                        padding: const EdgeInsets.all(24),
                        child: Column(mainAxisSize: MainAxisSize.min, children: [
                          Text(_error!, textAlign: TextAlign.center),
                          const SizedBox(height: 12),
                          OutlinedButton(onPressed: _cargar, child: Text(tr('Reintentar'))),
                        ]),
                      ),
              )
            : ListView(
                padding: const EdgeInsets.fromLTRB(20, 4, 20, 24),
                children: f.esTitular
                    ? _titular(f)
                    : f.esMiembro
                    ? _miembro(f)
                    : [
                        Text(tr('Tu plan no es familiar'), style: Theme.of(context).textTheme.headlineSmall),
                        const SizedBox(height: 8),
                        Text(tr('Con el plan Familiar, tú y 3 personas más aprenden con una sola suscripción.'),
                            style: const TextStyle(color: OL.gris, height: 1.4)),
                      ],
              ),
      ),
    );
  }

  List<Widget> _titular(Familia f) => [
    Text(tr('Personas en tu plan'), style: Theme.of(context).textTheme.headlineSmall),
    const SizedBox(height: 4),
    Text(
      tr('Puedes añadir hasta {n} personas. Cada una entra con su propio correo, elige su idioma y lleva su propio progreso.', {'n': f.plazas}),
      style: const TextStyle(color: OL.gris, height: 1.4),
    ),
    const SizedBox(height: 14),
    for (final m in f.miembros)
      Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: Tarjeta(
          key: ValueKey('miembro-${m.email}'),
          sombra: false,
          padding: const EdgeInsets.fromLTRB(14, 10, 6, 10),
          child: Row(children: [
            CircleAvatar(
              backgroundColor: OL.naranjaSuave,
              child: Text(
                (m.nombre.isNotEmpty ? m.nombre : m.email).characters.first.toUpperCase(),
                style: const TextStyle(color: OL.naranja, fontWeight: FontWeight.w800),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(m.nombre.isNotEmpty ? m.nombre : m.email, style: const TextStyle(fontWeight: FontWeight.w800), overflow: TextOverflow.ellipsis),
                if (m.nombre.isNotEmpty) Text(m.email, style: const TextStyle(color: OL.gris, fontSize: 12), overflow: TextOverflow.ellipsis),
                const SizedBox(height: 4),
                m.activo
                    ? Etiqueta(tr('Activo'), color: OL.verde)
                    : Etiqueta(tr('Pendiente'), color: const Color(0xFF9A6B00)),
              ]),
            ),
            IconButton(
              tooltip: tr('Quitar'),
              onPressed: _enviando ? null : () => _quitar(m),
              icon: const Icon(Icons.person_remove_outlined, color: OL.gris),
            ),
          ]),
        ),
      ),
    Text(
      tr('{n} de {total} personas', {'n': f.miembros.length, 'total': f.plazas}),
      style: TextStyle(color: f.completa ? OL.verde : OL.gris, fontWeight: FontWeight.w700),
    ),
    if (!f.completa) ...[
      const SizedBox(height: 14),
      TextField(
        key: const ValueKey('correo-familiar'),
        controller: _correo,
        keyboardType: TextInputType.emailAddress,
        autocorrect: false,
        textInputAction: TextInputAction.done,
        onSubmitted: (_) => _enviando ? null : _invitar(),
        decoration: InputDecoration(labelText: tr('Correo de la persona'), prefixIcon: const Icon(Icons.mail_outline)),
      ),
      const SizedBox(height: 10),
      ElevatedButton.icon(
        style: ElevatedButton.styleFrom(backgroundColor: OL.naranja),
        onPressed: _enviando ? null : _invitar,
        icon: const Icon(Icons.person_add_alt_1_rounded),
        label: Text(tr('Añadir a mi plan')),
      ),
      const SizedBox(height: 8),
      Text(
        tr('Si aún no tiene cuenta, le enviamos un correo y tendrá acceso al crearla con ese correo.'),
        style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.4),
      ),
    ],
  ];

  List<Widget> _miembro(Familia f) => [
    Text(tr('Formas parte de un plan familiar'), style: Theme.of(context).textTheme.headlineSmall),
    const SizedBox(height: 8),
    Text(
      tr('Tu acceso lo paga {nombre}. Tu progreso, tus idiomas y tus conversaciones son solo tuyos.', {'nombre': f.titular ?? ''}),
      style: const TextStyle(color: OL.gris, height: 1.4),
    ),
    const SizedBox(height: 20),
    OutlinedButton.icon(
      onPressed: _enviando ? null : _salir,
      icon: const Icon(Icons.logout_rounded),
      label: Text(tr('Salir del plan familiar')),
    ),
  ];
}
