import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/i18n/i18n.dart';

/// Piezas del registro y la recuperación con código por correo: teléfono con
/// código de país, el campo del código con su «Reenviar», la recuperación de
/// la contraseña y los datos de contacto que faltan en las cuentas de Google.

/// Códigos de país del selector del teléfono (el primero es el de por defecto).
List<(String, String)> get prefijosTelefono => [
  ('+1', tr('Estados Unidos / Canadá')),
  ('+52', tr('México')),
  ('+57', tr('Colombia')),
  ('+593', tr('Ecuador')),
  ('+51', tr('Perú')),
  ('+56', tr('Chile')),
  ('+54', tr('Argentina')),
  ('+58', tr('Venezuela')),
  ('+591', tr('Bolivia')),
  ('+595', tr('Paraguay')),
  ('+598', tr('Uruguay')),
  ('+502', tr('Guatemala')),
  ('+503', tr('El Salvador')),
  ('+504', tr('Honduras')),
  ('+505', tr('Nicaragua')),
  ('+506', tr('Costa Rica')),
  ('+507', tr('Panamá')),
  ('+53', tr('Cuba')),
  ('+34', tr('España')),
  ('+55', tr('Brasil')),
  ('+44', tr('Reino Unido')),
  ('+33', tr('Francia')),
  ('+49', tr('Alemania')),
  ('+39', tr('Italia')),
  ('+351', tr('Portugal')),
  ('+7', tr('Rusia')),
  ('+86', tr('China')),
  ('+81', tr('Japón')),
  ('+82', tr('Corea del Sur')),
];

/// Teléfono completo (`+<país><número>`) o '' si el número es muy corto.
String telefonoCompleto(String prefijo, String numero) {
  final digitos = numero.replaceAll(RegExp(r'\D'), '');
  return digitos.length >= 6 ? '$prefijo$digitos' : '';
}

/// Selector del código de país + número.
class CampoTelefono extends StatelessWidget {
  const CampoTelefono({
    super.key,
    required this.prefijo,
    required this.numero,
    required this.onPrefijo,
    required this.onChanged,
  });

  final String prefijo;
  final TextEditingController numero;
  final ValueChanged<String> onPrefijo;
  final VoidCallback onChanged;

  @override
  Widget build(BuildContext context) {
    final opciones = prefijosTelefono;
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: 112,
          child: DropdownButtonFormField<String>(
            initialValue: prefijo,
            isExpanded: true,
            decoration: const InputDecoration(),
            selectedItemBuilder: (_) => [
              for (final (codigo, _) in opciones) Text(codigo),
            ],
            items: [
              for (final (codigo, pais) in opciones)
                DropdownMenuItem(
                  value: codigo,
                  child: Text(
                    '$codigo  $pais',
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
            ],
            onChanged: (v) {
              if (v != null) onPrefijo(v);
            },
          ),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: TextField(
            controller: numero,
            keyboardType: TextInputType.phone,
            autofillHints: const [AutofillHints.telephoneNumberNational],
            inputFormatters: [
              FilteringTextInputFormatter.allow(RegExp(r'[0-9 ]')),
            ],
            onChanged: (_) => onChanged(),
            decoration: InputDecoration(
              hintText: tr('Número de teléfono'),
              prefixIcon: const Icon(Icons.phone_outlined),
            ),
          ),
        ),
      ],
    );
  }
}

/// Campo del código de 6 dígitos (el teclado lo puede autocompletar).
class CampoCodigo extends StatelessWidget {
  const CampoCodigo({
    super.key,
    required this.controller,
    required this.onChanged,
    this.onCompleto,
  });

  final TextEditingController controller;
  final VoidCallback onChanged;
  final VoidCallback? onCompleto;

  @override
  Widget build(BuildContext context) => TextField(
    controller: controller,
    autofocus: true,
    keyboardType: TextInputType.number,
    autofillHints: const [AutofillHints.oneTimeCode],
    maxLength: 6,
    textAlign: TextAlign.center,
    inputFormatters: [FilteringTextInputFormatter.digitsOnly],
    style: const TextStyle(
      fontSize: 28,
      fontWeight: FontWeight.w800,
      letterSpacing: 10,
    ),
    onChanged: (v) {
      onChanged();
      if (v.length == 6) onCompleto?.call();
    },
    decoration: const InputDecoration(counterText: '', hintText: '······'),
  );
}

/// «Reenviar código» con la cuenta atrás que pide el servidor (60 s).
class ReenviarCodigo extends StatefulWidget {
  const ReenviarCodigo({super.key, required this.reenviar, this.espera = 60});

  /// Pide otro código; devuelve los segundos de espera hasta el siguiente.
  final Future<int> Function() reenviar;
  final int espera;

  @override
  State<ReenviarCodigo> createState() => _ReenviarCodigoState();
}

class _ReenviarCodigoState extends State<ReenviarCodigo> {
  late int _faltan = widget.espera;
  Timer? _reloj;
  bool _enviando = false;

  @override
  void initState() {
    super.initState();
    _contar();
  }

  void _contar() {
    _reloj?.cancel();
    _reloj = Timer.periodic(const Duration(seconds: 1), (t) {
      if (!mounted) return t.cancel();
      setState(() => _faltan--);
      if (_faltan <= 0) t.cancel();
    });
  }

  @override
  void dispose() {
    _reloj?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => TextButton(
    onPressed: _faltan > 0 || _enviando
        ? null
        : () async {
            setState(() => _enviando = true);
            final espera = await widget.reenviar();
            if (!mounted) return;
            setState(() {
              _enviando = false;
              _faltan = espera;
            });
            _contar();
          },
    child: Text(
      _faltan > 0
          ? tr('Reenviar código en {s} s', {'s': _faltan})
          : tr('Reenviar código'),
    ),
  );
}

/// «Olvidé mi contraseña» con código: correo → código + contraseña nueva.
/// Devuelve true si quedó con la sesión iniciada.
Future<bool> recuperarConCodigo(BuildContext context, String correo) async =>
    await showModalBottomSheet<bool>(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      builder: (_) => _RecuperarClave(correo: correo),
    ) ??
    false;

class _RecuperarClave extends StatefulWidget {
  const _RecuperarClave({required this.correo});
  final String correo;

  @override
  State<_RecuperarClave> createState() => _RecuperarClaveState();
}

class _RecuperarClaveState extends State<_RecuperarClave> {
  late final email = TextEditingController(text: widget.correo);
  final codigo = TextEditingController();
  final clave = TextEditingController();
  bool enviado = false, cargando = false;
  String? error;

  @override
  void dispose() {
    email.dispose();
    codigo.dispose();
    clave.dispose();
    super.dispose();
  }

  String get _correo => email.text.trim().toLowerCase();

  Future<void> _pedir() async {
    if (!_correo.contains('@')) {
      setState(() => error = tr('Escribe tu correo.'));
      return;
    }
    setState(() {
      cargando = true;
      error = null;
    });
    final ok = await Sync.instancia.pedirCodigoClave(_correo);
    if (!mounted) return;
    setState(() {
      cargando = false;
      enviado = ok || Sync.instancia.reenviarEn != null;
      error = ok ? null : Sync.instancia.ultimoError;
    });
  }

  Future<void> _cambiar() async {
    if (codigo.text.length != 6 || clave.text.length < 6) return;
    setState(() {
      cargando = true;
      error = null;
    });
    final ok = await Sync.instancia.restablecerConCodigo(
      _correo,
      codigo.text,
      clave.text,
    );
    if (!mounted) return;
    if (ok) return Navigator.pop(context, true);
    setState(() {
      cargando = false;
      error = Sync.instancia.ultimoError;
    });
  }

  @override
  Widget build(BuildContext context) => Padding(
    padding: EdgeInsets.fromLTRB(
      24,
      20,
      24,
      24 + MediaQuery.viewInsetsOf(context).bottom,
    ),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          tr('Recuperar contraseña'),
          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900),
        ),
        const SizedBox(height: 6),
        Text(
          enviado
              ? tr(
                  'Si {correo} tiene una cuenta, te enviamos un código de 6 dígitos. Escríbelo y elige tu contraseña nueva.',
                  {'correo': _correo},
                )
              : tr('Te enviaremos un código de 6 dígitos a tu correo.'),
          style: const TextStyle(color: OL.gris, height: 1.4),
        ),
        const SizedBox(height: 16),
        if (!enviado)
          TextField(
            controller: email,
            keyboardType: TextInputType.emailAddress,
            autofillHints: const [AutofillHints.email],
            decoration: InputDecoration(
              hintText: tr('Correo electrónico'),
              prefixIcon: const Icon(Icons.mail_outline),
            ),
          )
        else ...[
          CampoCodigo(controller: codigo, onChanged: () => setState(() {})),
          const SizedBox(height: 10),
          TextField(
            controller: clave,
            obscureText: true,
            autofillHints: const [AutofillHints.newPassword],
            onChanged: (_) => setState(() {}),
            decoration: InputDecoration(
              hintText: tr('Contraseña nueva (mínimo 6 caracteres)'),
              prefixIcon: const Icon(Icons.lock_outline),
            ),
          ),
          ReenviarCodigo(
            reenviar: () async {
              await Sync.instancia.pedirCodigoClave(_correo);
              return Sync.instancia.reenviarEn ?? 60;
            },
          ),
        ],
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
        const SizedBox(height: 14),
        FilledButton(
          style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(52)),
          onPressed: cargando
              ? null
              : !enviado
              ? _pedir
              : codigo.text.length == 6 && clave.text.length >= 6
              ? _cambiar
              : null,
          child: Text(
            cargando
                ? tr('Un momento…')
                : enviado
                ? tr('CAMBIAR CONTRASEÑA Y ENTRAR')
                : tr('ENVIAR CÓDIGO'),
          ),
        ),
      ],
    ),
  );
}

/// Las cuentas de Google llegan sin teléfono: se piden nombre, apellido y
/// teléfono una vez, al entrar por primera vez.
Future<void> pedirContacto(BuildContext context, {String nombre = ''}) =>
    showDialog<void>(
      context: context,
      barrierDismissible: false,
      builder: (_) => _DatosContacto(nombre: nombre),
    );

class _DatosContacto extends StatefulWidget {
  const _DatosContacto({required this.nombre});
  final String nombre;

  @override
  State<_DatosContacto> createState() => _DatosContactoState();
}

class _DatosContactoState extends State<_DatosContacto> {
  late final nombre = TextEditingController(text: widget.nombre);
  final apellido = TextEditingController();
  final numero = TextEditingController();
  String prefijo = prefijosTelefono.first.$1;
  bool cargando = false;
  String? error;

  @override
  void dispose() {
    nombre.dispose();
    apellido.dispose();
    numero.dispose();
    super.dispose();
  }

  bool get _listo =>
      nombre.text.trim().isNotEmpty &&
      apellido.text.trim().isNotEmpty &&
      telefonoCompleto(prefijo, numero.text).isNotEmpty;

  Future<void> _guardar() async {
    setState(() {
      cargando = true;
      error = null;
    });
    final ok = await Sync.instancia.guardarContacto(
      nombre: nombre.text.trim(),
      apellido: apellido.text.trim(),
      telefono: telefonoCompleto(prefijo, numero.text),
    );
    if (!mounted) return;
    if (ok) return Navigator.pop(context);
    setState(() {
      cargando = false;
      error = Sync.instancia.ultimoError;
    });
  }

  @override
  Widget build(BuildContext context) => AlertDialog(
    title: Text(tr('Completa tus datos')),
    content: SingleChildScrollView(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          TextField(
            controller: nombre,
            textCapitalization: TextCapitalization.words,
            onChanged: (_) => setState(() {}),
            decoration: InputDecoration(hintText: tr('Nombre')),
          ),
          const SizedBox(height: 10),
          TextField(
            controller: apellido,
            textCapitalization: TextCapitalization.words,
            onChanged: (_) => setState(() {}),
            decoration: InputDecoration(hintText: tr('Apellido')),
          ),
          const SizedBox(height: 10),
          CampoTelefono(
            prefijo: prefijo,
            numero: numero,
            onPrefijo: (v) => setState(() => prefijo = v),
            onChanged: () => setState(() {}),
          ),
          if (error != null && error!.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text(error!, style: const TextStyle(color: OL.rojo, fontSize: 12)),
          ],
        ],
      ),
    ),
    actions: [
      FilledButton(
        onPressed: _listo && !cargando ? _guardar : null,
        child: Text(tr('Guardar')),
      ),
    ],
  );
}
