import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/content/curriculum.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import 'diagnostico_screen.dart';
import '../../shared/widgets/widgets.dart';

/// Flujo de primera experiencia (REQUERIMIENTOS §10):
/// cuenta → idioma nativo → idioma a aprender → nivel → prueba gratuita.
class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});

  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
  int paso = 0;
  final nombre = TextEditingController(text: '');
  final correo = TextEditingController();
  final clave = TextEditingController();
  String? errorRegistro;
  String nativo = 'es';
  String meta = 'en';
  int nivelInicial = 1;

  static const _titulos = [
    'Crea tu cuenta',
    '¿Cuál es tu idioma nativo?',
    '¿Qué idioma quieres aprender?',
    '¿Cuál es tu nivel?',
    'Tu prueba gratuita',
  ];

  bool get _puedeSeguir => switch (paso) {
        0 => nombre.text.trim().isNotEmpty,
        2 => meta != nativo,
        _ => true,
      };

  bool creando = false;

  Future<void> _siguiente() async {
    if (paso < 4) {
      setState(() => paso++);
      return;
    }
    final conClave = correo.text.trim().isNotEmpty && clave.text.trim().isNotEmpty;
    if (conClave) {
      // Cuenta real: el servidor valida el correo y guarda la contraseña.
      setState(() => creando = true);
      final ok = await Sync.instancia.registrarConPassword(
        email: correo.text.trim().toLowerCase(), password: clave.text, nombre: nombre.text.trim(),
        idiomaNativo: nativo, idiomaMeta: meta, nivelInicial: nivelInicial.clamp(1, 10),
      );
      if (!mounted) return;
      setState(() => creando = false);
      if (!ok && Sync.instancia.ultimoError.isNotEmpty && !Sync.instancia.ultimoError.contains('conectar')) {
        setState(() {
          errorRegistro = Sync.instancia.ultimoError;
          paso = 0;
        });
        return;
      }
    }
    ref.read(progressProvider.notifier).terminarOnboarding(
          nombre: nombre.text.trim(),
          idiomaNativo: nativo,
          idiomaMeta: meta,
          nivelInicial: nivelInicial.clamp(1, 10),
          fundamentos: nivelInicial == 0,
          diagnostico: DiagnosticoScreen.ultimoResultado == null ? null : DiagnosticoScreen.diagnosticoJson(DiagnosticoScreen.ultimoResultado!, DiagnosticoScreen.ultimoPerfilIa),
          email: correo.text,
          password: conClave ? '' : '', // la cuenta real ya se creó arriba; sin clave se usa el registro demo
        );
    if (mounted) context.go('/inicio');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: paso == 0
            ? IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => context.go('/bienvenida'))
            : IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => setState(() => paso--)),
        title: SizedBox(
          width: 200,
          child: BarraProgreso((paso + 1) / 5),
        ),
        centerTitle: true,
      ),
      body: Movil(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(24, 8, 24, 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text('Paso ${paso + 1} de 5',
                  style: const TextStyle(color: OL.gris, fontWeight: FontWeight.w600)),
              const SizedBox(height: 6),
              Text(_titulos[paso], style: Theme.of(context).textTheme.headlineMedium),
              const SizedBox(height: 20),
              Expanded(child: _contenido()),
              ElevatedButton(
                onPressed: _puedeSeguir && !creando ? _siguiente : null,
                child: Text(creando ? 'CREANDO TU CUENTA…' : (paso == 4 ? 'COMENZAR MI HORA GRATIS' : 'CONTINUAR')),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _contenido() => switch (paso) {
        0 => _cuenta(),
        1 => _idiomas(nativo, (c) => setState(() => nativo = c), soloDisponibles: false),
        2 => _idiomas(meta, (c) => setState(() => meta = c), excluir: nativo),
        3 => _nivel(),
        _ => _trial(),
      };

  Widget _cuenta() => ListView(
        children: [
          const Text('Nombre completo', style: TextStyle(fontWeight: FontWeight.w600)),
          const SizedBox(height: 6),
          TextField(
            controller: nombre,
            onChanged: (_) => setState(() {}),
            decoration: const InputDecoration(
                hintText: 'Tu nombre', prefixIcon: Icon(Icons.person_outline)),
          ),
          const SizedBox(height: 14),
          const Text('Correo electrónico', style: TextStyle(fontWeight: FontWeight.w600)),
          const SizedBox(height: 6),
          TextField(
            controller: correo,
            keyboardType: TextInputType.emailAddress,
            decoration: const InputDecoration(
                hintText: 'tu@email.com', prefixIcon: Icon(Icons.mail_outline)),
          ),
          const SizedBox(height: 14),
          const Text('Contraseña', style: TextStyle(fontWeight: FontWeight.w600)),
          const SizedBox(height: 6),
          TextField(
            controller: clave,
            obscureText: true,
            onChanged: (_) => setState(() {}),
            decoration: const InputDecoration(
                hintText: 'Mínimo 6 caracteres', prefixIcon: Icon(Icons.lock_outline)),
          ),
          if (errorRegistro != null) ...[
            const SizedBox(height: 8),
            Text(errorRegistro!, style: const TextStyle(color: OL.rojo, fontSize: 12, fontWeight: FontWeight.w600)),
          ],
          const SizedBox(height: 24),
          const Row(children: [
            Expanded(child: Divider()),
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 12),
              child: Text('O CONTINUAR CON',
                  style: TextStyle(color: OL.gris, fontSize: 11, fontWeight: FontWeight.w700)),
            ),
            Expanded(child: Divider()),
          ]),
          const SizedBox(height: 16),
          OutlinedButton.icon(
            onPressed: () => setState(() => nombre.text = nombre.text.isEmpty ? 'Bryan' : nombre.text),
            icon: const Icon(Icons.g_mobiledata, size: 26),
            label: const Text('Google'),
          ),
          const SizedBox(height: 10),
          OutlinedButton.icon(
            onPressed: () => setState(() => nombre.text = nombre.text.isEmpty ? 'Bryan' : nombre.text),
            icon: const Icon(Icons.apple),
            label: const Text('Apple'),
          ),
        ],
      );

  Widget _idiomas(String sel, ValueChanged<String> onSel,
      {String? excluir, bool soloDisponibles = true}) {
    final lista = idiomas.where((l) => l.code != excluir).toList();
    return GridView.builder(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2, mainAxisSpacing: 12, crossAxisSpacing: 12, childAspectRatio: 1.35),
      itemCount: lista.length,
      itemBuilder: (_, i) {
        final l = lista[i];
        final activo = l.code == sel;
        final habilitado = l.disponible || !soloDisponibles;
        return Opacity(
          opacity: habilitado ? 1 : 0.45,
          child: Tarjeta(
            onTap: habilitado ? () => onSel(l.code) : null,
            borde: activo ? OL.morado : null,
            color: activo ? OL.moradoSuave : OL.blanco,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _Bandera(l.code),
                const SizedBox(height: 10),
                Text(l.nombre, style: const TextStyle(fontWeight: FontWeight.w700)),
                Text(l.disponible ? l.nombreNativo : 'Próximamente',
                    style: const TextStyle(color: OL.gris, fontSize: 11)),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _nivel() => ListView(
        children: [
          Tarjeta(
            color: OL.moradoSuave,
            sombra: false,
            onTap: () async {
              final r = await context.push<int>('/prueba-nivel?idioma=$meta');
              if (r != null && mounted) setState(() => nivelInicial = r);
            },
            child: Row(children: [
              const IconoCuadro(Icons.quiz_outlined, relleno: true),
              const SizedBox(width: 12),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  const Text('Hacer la prueba de nivel (recomendado)', style: TextStyle(fontWeight: FontWeight.w700)),
                  Text(nivelInicial > 1 ? 'Resultado: empezarás en el Nivel $nivelInicial' : nivelInicial == 0 ? 'Resultado: empezarás por Fundamentos (letras y sonidos)' : 'Adaptativa · 10-24 preguntas · 3-8 minutos',
                      style: const TextStyle(color: OL.gris, fontSize: 12)),
                ]),
              ),
              const Icon(Icons.chevron_right, color: OL.morado),
            ]),
          ),
          const SizedBox(height: 16),
          const Text('O elige tu nivel manualmente',
              style: TextStyle(color: OL.gris, fontWeight: FontWeight.w600)),
          const SizedBox(height: 10),
          for (final n in niveles)
            Padding(
              padding: const EdgeInsets.only(bottom: 10),
              child: Tarjeta(
                onTap: () => setState(() => nivelInicial = n.numero),
                borde: nivelInicial == n.numero ? OL.morado : null,
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                child: Row(children: [
                  EstadoLeccionIcono(
                    nivelInicial == n.numero ? LessonState.actual : LessonState.bloqueada,
                    numero: n.numero,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text('Nivel ${n.numero} · ${n.nombre}',
                          style: const TextStyle(fontWeight: FontWeight.w700)),
                      Text(n.descripcion,
                          style: const TextStyle(color: OL.gris, fontSize: 12)),
                    ]),
                  ),
                ]),
              ),
            ),
        ],
      );

  Widget _trial() => ListView(
        children: [
          HeroCard(
            gradient: OL.gradienteNaranja,
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: const [
              Etiqueta('PRUEBA GRATUITA', color: OL.naranja, fondo: OL.blanco),
              SizedBox(height: 12),
              Text('1 hora gratis',
                  style: TextStyle(color: OL.blanco, fontSize: 30, fontWeight: FontWeight.w800)),
              SizedBox(height: 6),
              Text(
                'Durante 60 minutos de uso real puedes probar todas las funciones '
                'principales: lecciones, práctica libre, conversación con IA y '
                'corrección de errores. Después eliges tu plan.',
                style: TextStyle(color: Color(0xFFFFF3E0), height: 1.5),
              ),
            ]),
          ),
          const SizedBox(height: 18),
          const Text('Qué vas a encontrar', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 16)),
          const SizedBox(height: 10),
          const _Punto(Icons.map_outlined, 'Curso estructurado',
              '10 niveles · 100 lecciones por nivel · examen final al 65 %'),
          const _Punto(Icons.forum_outlined, 'Práctica libre con IA',
              '50 situaciones reales adaptadas a tu nivel + conversación libre'),
          const _Punto(Icons.fact_check_outlined, 'Corrección de errores',
              'Cada error con su explicación y una nueva oportunidad para practicarlo'),
          const _Punto(Icons.insights_outlined, 'Progreso',
              'XP, racha, tiempo de estudio y habilidades'),
        ],
      );
}

class _Punto extends StatelessWidget {
  const _Punto(this.icono, this.titulo, this.texto);
  final IconData icono;
  final String titulo;
  final String texto;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          IconoCuadro(icono, tamano: 40),
          const SizedBox(width: 12),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(titulo, style: const TextStyle(fontWeight: FontWeight.w700)),
              Text(texto, style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.4)),
            ]),
          ),
        ]),
      );
}

/// Banderas vectoriales simples (sin emojis), mismas que en el diseño de Figma.
class _Bandera extends StatelessWidget {
  const _Bandera(this.code);
  final String code;

  @override
  Widget build(BuildContext context) {
    Widget franjas(List<Color> c, {bool vertical = false}) => Flex(
          direction: vertical ? Axis.horizontal : Axis.vertical,
          children: [for (final col in c) Expanded(child: Container(color: col))],
        );
    final Widget f = switch (code) {
      'en' => Stack(fit: StackFit.expand, children: [
          Container(color: const Color(0xFF012169)),
          Center(child: Container(width: 14, color: OL.blanco)),
          Center(child: Container(height: 14, color: OL.blanco)),
          Center(child: Container(width: 8, color: const Color(0xFFC8102E))),
          Center(child: Container(height: 8, color: const Color(0xFFC8102E))),
        ]),
      'es' => franjas(const [Color(0xFFAA151B), Color(0xFFF1BF00), Color(0xFFF1BF00), Color(0xFFAA151B)]),
      'fr' => franjas(const [Color(0xFF002395), OL.blanco, Color(0xFFED2939)], vertical: true),
      'de' => franjas(const [Color(0xFF111111), Color(0xFFDD0000), Color(0xFFFFCE00)]),
      'it' => franjas(const [Color(0xFF009246), OL.blanco, Color(0xFFCE2B37)], vertical: true),
      'pt' => Stack(fit: StackFit.expand, children: [
          franjas(const [Color(0xFF006600), Color(0xFFFF0000), Color(0xFFFF0000)], vertical: true),
          const Align(alignment: Alignment(-0.35, 0), child: CircleAvatar(radius: 7, backgroundColor: Color(0xFFFFCC00))),
        ]),
      'ja' => Stack(fit: StackFit.expand, children: [
          Container(color: OL.blanco),
          const Center(child: CircleAvatar(radius: 13, backgroundColor: Color(0xFFBC002D))),
        ]),
      'zh' => Stack(fit: StackFit.expand, children: [
          Container(color: const Color(0xFFDE2910)),
          const Align(alignment: Alignment(-0.4, -0.4), child: Icon(Icons.star, color: Color(0xFFFFDE00), size: 18)),
        ]),
      'ko' => Stack(fit: StackFit.expand, children: [
          Container(color: OL.blanco),
          Center(
            child: ClipOval(
              child: SizedBox(
                width: 26,
                height: 26,
                child: Column(children: [
                  Expanded(child: Container(color: const Color(0xFFCD2E3A))),
                  Expanded(child: Container(color: const Color(0xFF0047A0))),
                ]),
              ),
            ),
          ),
          Positioned(left: 6, top: 6, child: Container(width: 3, height: 10, color: Colors.black87)),
          Positioned(right: 6, bottom: 6, child: Container(width: 3, height: 10, color: Colors.black87)),
        ]),
      _ => franjas(const [OL.blanco, Color(0xFF0039A6), Color(0xFFD52B1E)]),
    };
    return Container(
      width: 48,
      height: 48,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        border: Border.all(color: Colors.black26, width: 1.5),
      ),
      clipBehavior: Clip.antiAlias,
      child: f,
    );
  }
}
