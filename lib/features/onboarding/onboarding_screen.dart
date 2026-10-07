import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';

import '../../shared/widgets/perfil_seleccion.dart';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/providers.dart' show idiomasConRuta;
import '../../core/api/sync.dart';
import '../../core/content/curriculum.dart';
import '../../core/i18n/i18n.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/selector_idioma_app.dart';
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
  List<String> sectores = [], objetivos = [];
  Map<String, dynamic>? diagnostico;
  bool sesionPreparada = false;

  static const _draftKey = 'onelingo.onboarding.draft.v2';

  @override
  void initState() {
    super.initState();
    final raw = ref.read(prefsProvider).getString(_draftKey);
    if (raw == null) return;
    try {
      final d = jsonDecode(raw) as Map<String, dynamic>;
      if (!Sync.instancia.conectado || d['correo'] != Sync.instancia.email) {
        return;
      }
      nombre.text = d['nombre'] as String;
      correo.text = d['correo'] as String;
      nativo = d['nativo'] as String;
      meta = d['meta'] as String;
      sectores = List<String>.from(d['sectores'] as List);
      objetivos = List<String>.from(d['objetivos'] as List);
      nivelInicial = d['nivel'] as int;
      paso = (d['paso'] as int).clamp(1, 6);
      diagnostico = (d['diagnostico'] as Map?)?.cast<String, dynamic>();
      sesionPreparada = true;
    } catch (_) {
      /* Un borrador antiguo no bloquea el registro. */
    }
  }

  void _persistir() {
    if (!sesionPreparada) return;
    ref
        .read(prefsProvider)
        .setString(
          _draftKey,
          jsonEncode({
            'nombre': nombre.text,
            'correo': correo.text.trim().toLowerCase(),
            'nativo': nativo,
            'meta': meta,
            'sectores': sectores,
            'objetivos': objetivos,
            'nivel': nivelInicial,
            'paso': paso,
            'diagnostico': diagnostico,
          }),
        );
  }

  @override
  void dispose() {
    nombre.dispose();
    correo.dispose();
    clave.dispose();
    super.dispose();
  }

  static List<String> get _titulos => [
    tr('Crea tu cuenta'),
    tr('¿Cuál es tu idioma nativo?'),
    tr('¿Qué idioma quieres aprender?'),
    tr('¿A qué te dedicas?'),
    tr('Tus objetivos'),
    tr('¿Cuál es tu nivel?'),
    tr('Tu prueba gratuita'),
  ];

  bool get _puedeSeguir => switch (paso) {
    0 =>
      sesionPreparada ||
          nombre.text.trim().isNotEmpty &&
              correo.text.contains('@') &&
              clave.text.length >= 6,
    2 => meta != nativo,
    3 => sectores.isNotEmpty,
    4 => objetivos.isNotEmpty,
    _ => true,
  };

  bool creando = false;

  Future<void> _siguiente() async {
    if (paso == 0 && !sesionPreparada) {
      setState(() {
        creando = true;
        errorRegistro = null;
      });
      final ok = await Sync.instancia.registrarConPassword(
        email: correo.text.trim().toLowerCase(),
        password: clave.text,
        nombre: nombre.text.trim(),
        idiomaNativo: nativo,
        idiomaMeta: meta,
        nivelInicial: nivelInicial.clamp(1, 10),
      );
      if (!mounted) return;
      setState(() {
        creando = false;
        sesionPreparada = ok;
      });
      if (!ok) {
        setState(
          () => errorRegistro = Sync.instancia.ultimoError.isEmpty
              ? tr(
                  'No pudimos crear la cuenta. Comprueba la conexión e inténtalo otra vez.',
                )
              : Sync.instancia.ultimoError,
        );
        return;
      }
    }
    _persistir();
    // El nivel elegido es solo el punto de partida: la prueba decide en todos
    // los idiomas (nadie se ubica alto sin demostrarlo). Desde cero, sin prueba.
    // Idiomas sin ruta nueva (it, ja, ko, ru, zh): no hay prueba de nivel;
    // se empieza desde cero.
    if (paso == 5 && !idiomasConRuta.contains(meta)) {
      nivelInicial = 0;
    } else if (paso == 5 && (meta == 'en' || nivelInicial > 0)) {
      final r = await context.push<Map<String, dynamic>>(
        '/prueba-nivel',
        extra: {
          'idioma': meta,
          'nativo': nativo,
          'nivel': nivelInicial,
          'sectores': sectores,
          'objetivos': objetivos,
          'onboarding': true,
        },
      );
      if (!mounted || r == null) return;
      setState(() {
        diagnostico = r;
        nivelInicial = r['elegido'] as int;
        paso++;
      });
      _persistir();
      return;
    }
    if (paso < 6) {
      setState(() => paso++);
      _persistir();
      return;
    }
    ref
        .read(progressProvider.notifier)
        .terminarOnboarding(
          nombre: nombre.text.trim(),
          idiomaNativo: nativo,
          idiomaMeta: meta,
          nivelInicial: nivelInicial.clamp(1, 10),
          fundamentos: nivelInicial == 0,
          diagnostico: diagnostico,
          email: correo.text,
          sectores: sectores,
          objetivos: objetivos,
          sesionPreparada: true,
        );
    ref.read(prefsProvider).remove(_draftKey);
    if (mounted) context.go('/inicio');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: paso == 0
            ? IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: () => context.go('/bienvenida'),
              )
            : IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: creando
                    ? null
                    : () => setState(
                        () =>
                            paso = paso == 1 && sesionPreparada ? 1 : paso - 1,
                      ),
              ),
        title: SizedBox(width: 200, child: BarraProgreso((paso + 1) / 7)),
        centerTitle: true,
      ),
      body: Movil(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(24, 8, 24, 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                tr('Paso {n} de 7', {'n': paso + 1}),
                style: const TextStyle(
                  color: OL.gris,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                _titulos[paso],
                style: Theme.of(context).textTheme.headlineMedium,
              ),
              const SizedBox(height: 20),
              Expanded(
                child: AnimatedSwitcher(
                  duration: MediaQuery.disableAnimationsOf(context)
                      ? Duration.zero
                      : const Duration(milliseconds: 260),
                  transitionBuilder: (child, animation) => FadeTransition(
                    opacity: animation,
                    child: SlideTransition(
                      position: Tween<Offset>(
                        begin: const Offset(0, .04),
                        end: Offset.zero,
                      ).animate(animation),
                      child: child,
                    ),
                  ),
                  child: KeyedSubtree(key: ValueKey(paso), child: _contenido()),
                ),
              ),
              BotonPrincipal(
                onPressed: _puedeSeguir && !creando ? _siguiente : null,
                child: Text(
                  creando
                      ? tr('CREANDO TU CUENTA…')
                      : (paso == 6
                            ? tr('COMENZAR MI HORA GRATIS')
                            : paso == 5 && meta == 'en'
                            ? tr('COMPROBAR MI NIVEL')
                            : tr('CONTINUAR')),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _contenido() => switch (paso) {
    0 => _cuenta(),
    1 => Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Expanded(child: _idiomaNativo()),
        const SizedBox(height: 10),
        // El idioma de la app sigue al nativo, pero se puede cambiar aquí.
        Text(
          tr('Idioma de la app'),
          style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 15),
        ),
        const SizedBox(height: 6),
        const SelectorIdiomaApp(),
      ],
    ),
    2 => _idiomas(
      meta,
      (c) => setState(() {
        meta = c;
        diagnostico = null;
      }),
      excluir: nativo,
    ),
    3 => _perfil(false),
    4 => _perfil(true),
    5 => _nivel(),
    _ => _trial(),
  };

  Widget _cuenta() => ListView(
    children: [
      Text(
        tr('Nombre completo'),
        style: const TextStyle(fontWeight: FontWeight.w600),
      ),
      const SizedBox(height: 6),
      TextField(
        controller: nombre,
        onChanged: (_) => setState(() {}),
        decoration: InputDecoration(
          hintText: tr('Tu nombre'),
          prefixIcon: const Icon(Icons.person_outline),
        ),
      ),
      const SizedBox(height: 14),
      Text(
        tr('Correo electrónico'),
        style: const TextStyle(fontWeight: FontWeight.w600),
      ),
      const SizedBox(height: 6),
      TextField(
        controller: correo,
        onChanged: (_) => setState(() {}),
        keyboardType: TextInputType.emailAddress,
        decoration: InputDecoration(
          hintText: tr('tu@email.com'),
          prefixIcon: const Icon(Icons.mail_outline),
        ),
      ),
      const SizedBox(height: 14),
      Text(
        tr('Contraseña'),
        style: const TextStyle(fontWeight: FontWeight.w600),
      ),
      const SizedBox(height: 6),
      TextField(
        controller: clave,
        obscureText: true,
        onChanged: (_) => setState(() {}),
        decoration: InputDecoration(
          hintText: tr('Mínimo 6 caracteres'),
          prefixIcon: const Icon(Icons.lock_outline),
        ),
      ),
      if (errorRegistro != null) ...[
        const SizedBox(height: 8),
        Text(
          errorRegistro!,
          style: const TextStyle(
            color: OL.rojo,
            fontSize: 12,
            fontWeight: FontWeight.w600,
          ),
        ),
      ],
      const SizedBox(height: 16),
      TextButton(
        onPressed: () => context.go('/login'),
        child: Text(tr('Ya tengo una cuenta · Iniciar sesión')),
      ),
      if (kDebugMode)
        OutlinedButton.icon(
          icon: const Icon(Icons.science_outlined),
          label: Text(tr('Rellenar usuario demo de pruebas')),
          onPressed: () => setState(() {
            final id = DateTime.now().microsecondsSinceEpoch;
            nombre.text = 'Demo onboarding';
            correo.text = 'demo.$id@onelingo.test';
            clave.text = 'Demo-local-$id!';
          }),
        ),
    ],
  );

  Widget _perfil(bool metas) => SingleChildScrollView(
    child: PerfilSeleccion(
      sectores: sectores,
      objetivos: objetivos,
      soloObjetivos: metas,
      soloSectores: !metas,
      onChanged: (s, o) => setState(() {
        sectores = s;
        objetivos = o;
        diagnostico = null;
      }),
    ),
  );

  Widget _idiomaNativo() => _idiomas(
      nativo,
      (c) {
        setState(() {
          nativo = c;
          diagnostico = null;
        });
        // La app pasa al idioma nativo elegido (si lo tiene; si no, inglés).
        // Antes se guarda el borrador: cambiar de idioma reconstruye la app.
        _persistir();
        ref
            .read(progressProvider.notifier)
            .elegirIdiomaInterfaz(idiomaInterfazPara(c));
      },
      soloDisponibles: false,
    );

  Widget _idiomas(
    String sel,
    ValueChanged<String> onSel, {
    String? excluir,
    bool soloDisponibles = true,
  }) {
    final lista = idiomas.toList();
    return LayoutBuilder(
      builder: (context, bounds) {
        final columnas = bounds.maxWidth >= 520 ? 3 : 2;
        final filas = (lista.length / columnas).ceil();
        final alto = ((bounds.maxHeight - (filas - 1) * 8) / filas).clamp(
          56.0,
          110.0,
        );
        return GridView.builder(
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: columnas,
            mainAxisSpacing: 8,
            crossAxisSpacing: 8,
            mainAxisExtent: alto,
          ),
          itemCount: lista.length,
          itemBuilder: (_, i) {
            final l = lista[i];
            final activo = l.code == sel;
            final habilitado =
                l.code != excluir && (l.disponible || !soloDisponibles);
            return AnimatedContainer(
              duration: MediaQuery.disableAnimationsOf(context)
                  ? Duration.zero
                  : const Duration(milliseconds: 180),
              decoration: BoxDecoration(
                color: activo ? OL.moradoSuave : OL.blanco,
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: activo ? OL.moradoClaro : OL.grisClaro,
                    offset: const Offset(0, 3),
                  ),
                ],
                border: Border.all(
                  color: activo ? OL.morado : OL.grisClaro,
                  width: 2,
                ),
              ),
              child: Semantics(
                selected: activo,
                button: true,
                enabled: habilitado,
                child: InkWell(
                  onTap: habilitado ? () => onSel(l.code) : null,
                  borderRadius: BorderRadius.circular(14),
                  child: Padding(
                    padding: const EdgeInsets.all(8),
                    child: Row(
                      children: [
                        SizedBox(
                          width: 40,
                          height: 30,
                          child: LanguageFlag(l.code),
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            _nombreIdioma(l.code, l.nombre),
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w700,
                              color: habilitado ? OL.morado : OL.gris,
                            ),
                          ),
                        ),
                        if (activo)
                          const Icon(
                            Icons.check_circle,
                            size: 16,
                            color: OL.morado,
                          ),
                      ],
                    ),
                  ),
                ),
              ),
            );
          },
        );
      },
    );
  }

  Widget _nivel() => ListView(
    children: [
      Text(
        tr(
          'Elige tu punto de partida. Después una prueba corta confirma tu nivel: empezarás donde de verdad estás.',
        ),
      ),
      const SizedBox(height: 12),
      ListTile(
        title: Text(tr('Empiezo desde cero')),
        leading: Icon(
          nivelInicial == 0
              ? Icons.radio_button_checked
              : Icons.radio_button_off,
        ),
        onTap: () => setState(() => nivelInicial = 0),
      ),
      for (final n in niveles)
        Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: Tarjeta(
            onTap: () => setState(() => nivelInicial = n.numero),
            borde: nivelInicial == n.numero ? OL.morado : null,
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            child: Row(
              children: [
                EstadoLeccionIcono(
                  nivelInicial == n.numero
                      ? LessonState.actual
                      : LessonState.bloqueada,
                  numero: n.numero,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        tr('Nivel {n} · {nombre}', {
                          'n': n.numero,
                          'nombre': _nombreNivel(n.nombre),
                        }),
                        style: const TextStyle(fontWeight: FontWeight.w700),
                      ),
                      Text(
                        n.descripcion,
                        style: const TextStyle(color: OL.gris, fontSize: 12),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
    ],
  );

  Widget _trial() => ListView(
    children: [
      HeroCard(
        gradient: OL.gradienteNaranja,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Etiqueta(
              tr('PRUEBA GRATUITA'),
              color: OL.naranja,
              fondo: OL.blanco,
            ),
            const SizedBox(height: 12),
            Text(
              tr('1 hora gratis'),
              style: const TextStyle(
                color: OL.blanco,
                fontSize: 30,
                fontWeight: FontWeight.w800,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              tr(
                'Durante 60 minutos de uso real puedes probar todas las funciones '
                'principales: lecciones, práctica libre, conversación con IA y '
                'corrección de errores. Después eliges tu plan.',
              ),
              style: const TextStyle(color: Color(0xFFFFF3E0), height: 1.5),
            ),
          ],
        ),
      ),
      const SizedBox(height: 18),
      Text(
        tr('Qué vas a encontrar'),
        style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16),
      ),
      const SizedBox(height: 10),
      _Punto(
        Icons.map_outlined,
        tr('Curso estructurado'),
        tr('10 niveles · 100 lecciones por nivel · examen final al 65 %'),
      ),
      _Punto(
        Icons.forum_outlined,
        tr('Práctica libre con IA'),
        tr('50 situaciones reales adaptadas a tu nivel + conversación libre'),
      ),
      _Punto(
        Icons.fact_check_outlined,
        tr('Corrección de errores'),
        tr(
          'Cada error con su explicación y una nueva oportunidad para practicarlo',
        ),
      ),
      _Punto(
        Icons.insights_outlined,
        tr('Progreso'),
        tr('XP, racha, tiempo de estudio y habilidades'),
      ),
    ],
  );
}

/// Nombre del idioma en el idioma de la interfaz.
String _nombreIdioma(String code, String nombre) => switch (code) {
  'en' => tr('Inglés'),
  'es' => tr('Español'),
  'fr' => tr('Francés'),
  'de' => tr('Alemán'),
  'pt' => tr('Portugués'),
  'it' => tr('Italiano'),
  'zh' => tr('Chino mandarín'),
  'ja' => tr('Japonés'),
  'ko' => tr('Coreano'),
  'ru' => tr('Ruso'),
  _ => nombre,
};

/// Nombre del nivel (curriculum.dart) en el idioma de la interfaz.
String _nombreNivel(String nombre) => switch (nombre) {
  'Básico' => tr('Básico'),
  'Básico Avanzado' => tr('Básico Avanzado'),
  'Intermedio' => tr('Intermedio'),
  'Intermedio Avanzado' => tr('Intermedio Avanzado'),
  'Avanzado' => tr('Avanzado'),
  'Avanzado Superior' => tr('Avanzado Superior'),
  'Dominio' => tr('Dominio'),
  _ => nombre,
};

class _Punto extends StatelessWidget {
  const _Punto(this.icono, this.titulo, this.texto);
  final IconData icono;
  final String titulo;
  final String texto;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 12),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        IconoCuadro(icono, tamano: 40),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(titulo, style: const TextStyle(fontWeight: FontWeight.w700)),
              Text(
                texto,
                style: const TextStyle(
                  color: OL.gris,
                  fontSize: 12,
                  height: 1.4,
                ),
              ),
            ],
          ),
        ),
      ],
    ),
  );
}
