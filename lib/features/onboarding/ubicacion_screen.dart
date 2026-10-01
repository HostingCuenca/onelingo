import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/aprendizaje/ubicacion.dart';
import '../../core/diagnostico.dart';
import '../../core/efectos.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../ruta/item_view.dart';
import 'diagnostico_screen.dart';

/// Prueba de nivel de inglés v2 (DEC-025): ~8 minutos, adaptativa por
/// habilidad. Sustituye al diagnóstico antiguo solo en inglés.
class UbicacionScreen extends ConsumerStatefulWidget {
  const UbicacionScreen({super.key, this.configuracion = const {}});

  /// Igual que el diagnóstico antiguo: `onboarding` y `nivel` (el que eligió
  /// en el registro, 0–10).
  final Map<String, dynamic> configuracion;

  @override
  ConsumerState<UbicacionScreen> createState() => _UbicacionScreenState();
}

enum _Fase { cargando, pregunta, intro, test, escritura, resultado }

class _UbicacionScreenState extends ConsumerState<UbicacionScreen> {
  static const _opciones = [
    (Autodeclaracion.nada, 'Nada, empiezo de cero', 'Nunca lo he estudiado'),
    (
      Autodeclaracion.poco,
      'Un poco',
      'Saludos, palabras sueltas, frases simples',
    ),
    (
      Autodeclaracion.defiendo,
      'Me defiendo',
      'Conversaciones cotidianas sencillas',
    ),
    (
      Autodeclaracion.bastante,
      'Bastante',
      'Entiendo textos y conversaciones normales',
    ),
    (
      Autodeclaracion.avanzado,
      'Avanzado',
      'Uso el inglés en el trabajo o los estudios',
    ),
  ];

  _Fase fase = _Fase.cargando;
  List<ItemUbicacion> banco = [];
  Ubicacion? u;
  ItemUbicacion? actual;
  int indice = 0;
  int? elegido;
  String? error;

  bool get esOnboarding => widget.configuracion['onboarding'] == true;

  @override
  void initState() {
    super.initState();
    _cargar();
  }

  @override
  void dispose() {
    Voz.instancia.parar();
    super.dispose();
  }

  Future<void> _cargar() async {
    try {
      final raw = await rootBundle.loadString(
        'assets/contenido/en/diagnostico-v2.json',
      );
      banco = ItemUbicacion.banco(jsonDecode(raw) as Map<String, dynamic>);
    } catch (e) {
      error = 'No pudimos cargar la prueba. Revisa la conexión e inténtalo otra vez.';
    }
    if (!mounted) return;
    final nivel = widget.configuracion['nivel'];
    setState(() {
      // En el registro ya eligió su punto de partida: no se lo preguntamos
      // otra vez (salvo «desde cero», que confirma aquí).
      if (esOnboarding && nivel is int && nivel > 0) {
        _empezar(Autodeclaracion.desdeNivel(nivel), mostrarIntro: true);
      } else {
        fase = _Fase.pregunta;
      }
    });
  }

  void _empezar(Autodeclaracion d, {bool mostrarIntro = false}) {
    u = Ubicacion(banco: banco, declarado: d);
    if (d == Autodeclaracion.nada) {
      _mostrarResultado();
      return;
    }
    fase = mostrarIntro ? _Fase.intro : _Fase.test;
    if (!mostrarIntro) _siguiente();
  }

  void _siguiente() {
    final x = u!;
    final i = x.siguiente();
    if (i != null) {
      setState(() {
        actual = i;
        indice++;
        fase = _Fase.test;
      });
      return;
    }
    final w = x.escritura();
    if (w != null) {
      setState(() {
        actual = w;
        indice++;
        fase = _Fase.escritura;
      });
      return;
    }
    _mostrarResultado();
  }

  void _mostrarResultado() {
    Efectos.completado();
    setState(() {
      fase = _Fase.resultado;
      elegido = u!.resultado().nivel;
    });
  }

  Map<String, dynamic> _json(int nivel) {
    final r = u!.resultado();
    return {
      'idioma': 'en',
      'version': 4,
      'escala': escalaDiagnosticoCliente,
      'escalaPresentacion': 'onelingo-10-a1-c1-v1',
      'nivelCliente': nivel,
      'recomendado': r.nivel,
      'elegido': nivel,
      'cefr': cefrNivel(nivel),
      'ubicacion': r.toJson(),
      'noEvaluado': ['expresión oral'],
      'fecha': DateTime.now().toIso8601String(),
    };
  }

  void _terminar(int nivel) {
    final r = u!.resultado();
    Sync.instancia.evento('diagnostico', {
      'version': 4,
      'nivelEstimado': r.nivel,
      'nivelElegido': nivel,
      'preguntas': r.preguntas,
      'aciertos': r.aciertos,
      'habilidades': r.habilidades,
      'escritura': r.escritura,
      'idioma': 'en',
    });
    final datos = _json(nivel);
    final st = ref.read(progressProvider);
    if (st.onboardingDone && !esOnboarding && st.idiomaMeta == 'en') {
      ref.read(progressProvider.notifier).guardarDiagnostico(datos, nivel);
    }
    if (context.canPop()) {
      context.pop(datos);
    } else {
      context.go('/inicio');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Prueba de nivel'),
        leading: IconButton(
          icon: const Icon(Icons.close),
          tooltip: 'Salir',
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/inicio'),
        ),
        bottom: fase == _Fase.test || fase == _Fase.escritura
            ? PreferredSize(
                preferredSize: const Size.fromHeight(6),
                child: LinearProgressIndicator(
                  value: u?.progreso ?? 0,
                  minHeight: 6,
                  color: OL.morado,
                  backgroundColor: OL.moradoClaro,
                ),
              )
            : null,
      ),
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 640),
            child: switch (fase) {
              _Fase.cargando => const Center(
                child: CircularProgressIndicator(),
              ),
              _Fase.pregunta => _pregunta(),
              _Fase.intro => _intro(),
              _Fase.test || _Fase.escritura => _item(),
              _Fase.resultado => _resultado(),
            },
          ),
        ),
      ),
    );
  }

  Widget _pregunta() => ListView(
    padding: const EdgeInsets.all(20),
    children: [
      Text(
        '¿Cuánto inglés sabes?',
        style: Theme.of(context).textTheme.headlineSmall
            ?.copyWith(fontWeight: FontWeight.w900),
      ),
      const SizedBox(height: 8),
      const Text(
        'Así empezamos la prueba en tu nivel. Dura unos 8 minutos y se adapta: '
        'sube de dificultad mientras aciertas y se detiene cuando llega a tu límite.',
      ),
      if (error != null) ...[
        const SizedBox(height: 12),
        Text(error!, style: const TextStyle(color: OL.rojo)),
      ],
      const SizedBox(height: 16),
      for (final (d, titulo, detalle) in _opciones)
        Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: Card(
            child: ListTile(
              title: Text(
                titulo,
                style: const TextStyle(fontWeight: FontWeight.w800),
              ),
              subtitle: Text(detalle),
              trailing: const Icon(Icons.chevron_right),
              onTap: banco.isEmpty && d != Autodeclaracion.nada
                  ? null
                  : () => setState(() => _empezar(d)),
            ),
          ),
        ),
    ],
  );

  Widget _intro() => ListView(
    padding: const EdgeInsets.all(20),
    children: [
      Text(
        'Comprobemos tu inglés',
        style: Theme.of(context).textTheme.headlineSmall
            ?.copyWith(fontWeight: FontWeight.w900),
      ),
      const SizedBox(height: 10),
      const Text(
        'Unos 8 minutos: escucha, lectura, gramática y vocabulario, y al final '
        'una o dos frases escritas. La prueba se adapta a ti: si algo es '
        'demasiado difícil, no pasa nada, es justo lo que buscamos.',
      ),
      const SizedBox(height: 24),
      FilledButton(onPressed: _siguiente, child: const Text('Empezar')),
      const SizedBox(height: 8),
      TextButton(
        onPressed: () => setState(() {
          u = Ubicacion(banco: banco, declarado: Autodeclaracion.nada);
          _mostrarResultado();
        }),
        child: const Text('Prefiero empezar desde cero'),
      ),
    ],
  );

  Widget _item() {
    final i = actual!;
    final escritura = fase == _Fase.escritura;
    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        Row(
          children: [
            Chip(
              label: Text(nombresHabilidad[i.habilidad] ?? i.habilidad),
              backgroundColor: OL.moradoSuave,
            ),
            const Spacer(),
            if (escritura)
              TextButton(
                onPressed: () {
                  u!.omitirEscritura();
                  _mostrarResultado();
                },
                child: const Text('Omitir'),
              ),
          ],
        ),
        if (escritura)
          const Padding(
            padding: EdgeInsets.only(bottom: 8),
            child: Text(
              'Último paso: escribe con tus palabras. Si prefieres, puedes omitirlo.',
            ),
          ),
        ItemView(
          key: ValueKey('${i.item.id}:$indice'),
          item: i.item,
          idioma: 'en',
          cadena: const [],
          guiada: false,
          permitirReintento: false,
          onComprobado: (correcta, _) => u!.responder(correcta),
          onContinuar: () {
            if (u!.actual != null) u!.responder(false);
            _siguiente();
          },
        ),
      ],
    );
  }

  Widget _resultado() {
    final r = u!.resultado();
    final t = Theme.of(context).textTheme;
    final nivel = elegido ?? r.nivel;
    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        Text(
          r.desdeCero ? 'Empiezas desde cero' : 'Tu nivel: N${r.nivel}',
          style: t.headlineMedium?.copyWith(fontWeight: FontWeight.w900),
        ),
        const SizedBox(height: 6),
        Text(
          r.desdeCero
              ? 'Perfecto: te guiamos paso a paso desde los sonidos y las '
                    'primeras frases. Avanzarás rápido.'
              : '${cefrNivel(r.nivel)} · ${r.preguntas} preguntas. '
                    'Empieza en la primera clase del nivel; los niveles '
                    'anteriores quedan disponibles para repasar.',
        ),
        if (!r.desdeCero) ...[
          const SizedBox(height: 20),
          for (final e in r.habilidades.entries) _barra(e.key, e.value),
          if (r.escritura != null) _barra('escritura', r.escritura!),
          if (r.reforzar.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text(
              'Te conviene reforzar: '
              '${r.reforzar.map((h) => nombresHabilidad[h]!.toLowerCase()).join(', ')}.',
            ),
          ],
          const SizedBox(height: 20),
          Text('¿Dónde quieres empezar?', style: t.titleMedium),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            children: [
              for (final n in {
                if (r.nivel > 1) r.nivel - 1,
                r.nivel,
                if (r.nivel < 10) r.nivel + 1,
              })
                ChoiceChip(
                  label: Text(n == r.nivel ? 'N$n (recomendado)' : 'N$n'),
                  selected: nivel == n,
                  onSelected: (_) => setState(() => elegido = n),
                ),
            ],
          ),
        ],
        const SizedBox(height: 24),
        FilledButton(
          onPressed: () => _terminar(nivel),
          child: Text(
            r.desdeCero ? 'Empezar desde cero' : 'Empezar en N$nivel',
          ),
        ),
      ],
    );
  }

  Widget _barra(String h, int nivel) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Row(
      children: [
        SizedBox(width: 110, child: Text(nombresHabilidad[h] ?? h)),
        Expanded(
          child: ClipRRect(
            borderRadius: BorderRadius.circular(6),
            child: LinearProgressIndicator(
              value: nivel / 10,
              minHeight: 10,
              color: OL.morado,
              backgroundColor: OL.moradoClaro,
            ),
          ),
        ),
        SizedBox(
          width: 52,
          child: Text(
            nivel == 0 ? 'inicio' : 'N$nivel',
            textAlign: TextAlign.end,
            style: const TextStyle(fontWeight: FontWeight.w800),
          ),
        ),
      ],
    ),
  );
}

/// MCER de cada nivel del curso (escala cliente).
String cefrNivel(int nivel) => switch (nivel) {
  <= 0 => 'Desde cero',
  1 => 'A1',
  2 => 'A2',
  3 || 4 => 'B1',
  5 || 6 || 7 => 'B2',
  _ => 'C1',
};

/// `/prueba-nivel`: inglés usa la prueba v2; los demás idiomas, el
/// diagnóstico anterior.
class PruebaNivelScreen extends ConsumerWidget {
  const PruebaNivelScreen({
    super.key,
    this.idioma,
    this.configuracion = const {},
  });
  final String? idioma;
  final Map<String, dynamic> configuracion;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final meta =
        configuracion['idioma'] as String? ??
        idioma ??
        ref.read(progressProvider).idiomaMeta;
    return meta == 'en'
        ? UbicacionScreen(configuracion: configuracion)
        : DiagnosticoScreen(idioma: idioma, configuracion: configuracion);
  }
}
