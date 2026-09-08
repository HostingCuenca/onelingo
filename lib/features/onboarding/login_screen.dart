import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:google_sign_in/google_sign_in.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/content/demo_users.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Inicio de sesión: cuenta real (correo + contraseña o Google) contra el
/// backend, y usuarios de prueba para recorrer la demo sin servidor.
class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final email = TextEditingController();
  final pass = TextEditingController();
  String? error;
  String? aviso;
  bool cargando = false;

  /// ID de cliente web de Google (necesario en web y como `serverClientId` en Android).
  static const _googleClientIdWeb = String.fromEnvironment('GOOGLE_CLIENT_ID_WEB');

  Future<void> _entrar() async {
    final correo = email.text.trim().toLowerCase();
    final demo = demoUserPorEmail(correo);
    if (demo != null && pass.text == DemoUser.password) {
      ref.read(progressProvider.notifier).cargar(demo.estado(), email: demo.email);
      context.go('/inicio');
      return;
    }
    if (correo.isEmpty || pass.text.isEmpty) {
      setState(() => error = 'Escribe tu correo y tu contraseña.');
      return;
    }
    setState(() { cargando = true; error = null; aviso = null; });
    final ok = await Sync.instancia.loginConPassword(correo, pass.text);
    if (!mounted) return;
    setState(() => cargando = false);
    if (!ok) {
      setState(() => error = Sync.instancia.ultimoError.isEmpty ? 'No se pudo iniciar sesión.' : Sync.instancia.ultimoError);
      return;
    }
    ref.read(progressProvider.notifier).iniciarSesionReal(
          email: correo,
          nombre: correo.split('@').first,
          estadoServidor: Sync.instancia.ultimoEstadoServidor,
        );
    context.go('/inicio');
  }

  Future<void> _google() async {
    setState(() { cargando = true; error = null; aviso = null; });
    try {
      final gs = GoogleSignIn.instance;
      await gs.initialize(clientId: kIsWeb && _googleClientIdWeb.isNotEmpty ? _googleClientIdWeb : null, serverClientId: _googleClientIdWeb.isNotEmpty ? _googleClientIdWeb : null);
      final cuenta = await gs.authenticate();
      final idToken = cuenta.authentication.idToken;
      if (idToken == null) throw Exception('Google no devolvió un token');
      final r = await Sync.instancia.loginConGoogle(idToken, idiomaNativo: 'es', idiomaMeta: 'en', nivelInicial: 1);
      if (!mounted) return;
      if (r == null) {
        setState(() => error = Sync.instancia.ultimoError);
        return;
      }
      ref.read(progressProvider.notifier).iniciarSesionReal(
            email: r['email'] as String? ?? cuenta.email,
            nombre: r['nombre'] as String? ?? cuenta.displayName ?? cuenta.email,
            estadoServidor: r['estado'] as Map<String, dynamic>?,
          );
      context.go('/inicio');
    } on GoogleSignInException catch (e) {
      setState(() => error = e.code == GoogleSignInExceptionCode.canceled ? null : 'Google: ${e.description ?? e.code.name}. Falta configurar el ID de cliente (ver AUTENTICACION.md).');
    } catch (e) {
      setState(() => error = 'Google Sign-In no está configurado todavía en esta app (ver AUTENTICACION.md).');
    } finally {
      if (mounted) setState(() => cargando = false);
    }
  }

  Future<void> _recuperar() async {
    final correo = email.text.trim().toLowerCase();
    if (correo.isEmpty || !correo.contains('@')) {
      setState(() => error = 'Escribe tu correo para enviarte el enlace.');
      return;
    }
    setState(() { cargando = true; error = null; });
    final msg = await Sync.instancia.recuperarPassword(correo);
    if (!mounted) return;
    setState(() {
      cargando = false;
      aviso = msg ?? (Sync.instancia.ultimoError.isEmpty ? 'No se pudo enviar el correo.' : Sync.instancia.ultimoError);
    });
  }

  void _usar(DemoUser u) => setState(() {
        email.text = u.email;
        pass.text = DemoUser.password;
        error = null;
      });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => context.go('/bienvenida')),
        title: const Text('Iniciar sesión'),
      ),
      body: Movil(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(24, 4, 24, 24),
          children: [
            const Center(child: Logo(tamano: 90)),
            const SizedBox(height: 8),
            Text('Bienvenido de nuevo', textAlign: TextAlign.center, style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 18),
            TextField(
              controller: email,
              keyboardType: TextInputType.emailAddress,
              autocorrect: false,
              decoration: const InputDecoration(hintText: 'Correo electrónico', prefixIcon: Icon(Icons.mail_outline)),
              onChanged: (_) => setState(() => error = null),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: pass,
              obscureText: true,
              decoration: const InputDecoration(hintText: 'Contraseña', prefixIcon: Icon(Icons.lock_outline)),
              onSubmitted: (_) => _entrar(),
            ),
            if (error != null) ...[
              const SizedBox(height: 8),
              Text(error!, style: const TextStyle(color: OL.rojo, fontSize: 12, fontWeight: FontWeight.w600)),
            ],
            if (aviso != null) ...[
              const SizedBox(height: 8),
              Text(aviso!, style: const TextStyle(color: OL.verde, fontSize: 12, fontWeight: FontWeight.w600)),
            ],
            const SizedBox(height: 14),
            ElevatedButton(onPressed: cargando ? null : _entrar, child: Text(cargando ? 'UN MOMENTO…' : 'ENTRAR')),
            const SizedBox(height: 6),
            Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
              TextButton(onPressed: cargando ? null : _recuperar, child: const Text('Olvidé mi contraseña')),
              TextButton(onPressed: () => context.go('/onboarding'), child: const Text('Crear cuenta nueva')),
            ]),
            const SizedBox(height: 6),
            const Row(children: [
              Expanded(child: Divider()),
              Padding(padding: EdgeInsets.symmetric(horizontal: 12), child: Text('O CONTINUAR CON', style: TextStyle(color: OL.gris, fontSize: 11, fontWeight: FontWeight.w700))),
              Expanded(child: Divider()),
            ]),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: cargando ? null : _google,
              icon: const Icon(Icons.g_mobiledata, size: 26),
              label: const Text('Google'),
            ),
            const SizedBox(height: 18),
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(color: OL.amarilloSuave, borderRadius: BorderRadius.circular(14)),
              child: const Row(children: [
                Icon(Icons.science_outlined, color: Color(0xFF9A6B00)),
                SizedBox(width: 10),
                Expanded(
                  child: Text(
                    'DEMO · Usuarios de prueba (no necesitan servidor). Toca uno y pulsa ENTRAR. Contraseña: 1234',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Color(0xFF6B4A00), height: 1.4),
                  ),
                ),
              ]),
            ),
            const SizedBox(height: 12),
            for (final u in demoUsers)
              Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: Tarjeta(
                  onTap: () => _usar(u),
                  borde: email.text == u.email ? OL.morado : null,
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  child: Row(children: [
                    CircleAvatar(radius: 20, backgroundColor: OL.moradoClaro, child: Text(u.nombre[0], style: const TextStyle(color: OL.morado, fontWeight: FontWeight.w800))),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text(u.nombre, style: const TextStyle(fontWeight: FontWeight.w700)),
                        Text(u.descripcion, style: const TextStyle(color: OL.gris, fontSize: 12)),
                        const SizedBox(height: 4),
                        Wrap(spacing: 6, runSpacing: 6, children: [
                          Etiqueta(u.email, color: OL.azul, icono: Icons.mail_outline),
                          const Etiqueta('1234', color: OL.gris, icono: Icons.key_outlined),
                        ]),
                      ]),
                    ),
                    IconButton(
                      tooltip: 'Entrar como ${u.nombre}',
                      onPressed: () { _usar(u); _entrar(); },
                      icon: const Icon(Icons.login, color: OL.morado),
                    ),
                  ]),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
