import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/aprendizaje/ubicacion.dart';
import '../../core/content/curriculum.dart' show idioma;
import '../../core/diagnostico.dart';
import '../../core/efectos.dart';
import '../../core/i18n/i18n.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../ruta/item_view.dart';
import 'diagnostico_screen.dart';

/// Prueba de nivel v2 (DEC-025, FR-6): ~8 minutos, adaptativa por
/// habilidad. La usan los idiomas con ruta que tienen banco
/// (`assets/contenido/<idioma>/diagnostico-v2.json`); el resultado nunca
/// supera el nivel publicado más alto. Los demás siguen con el diagnóstico
/// antiguo (`PruebaNivelScreen`).
class UbicacionScreen extends ConsumerStatefulWidget {
  const UbicacionScreen({
    super.key,
    this.idioma,
    this.configuracion = const {},
  });

  /// Idioma que se evalúa; por defecto `configuracion['idioma']` o el
  /// idioma meta del alumno.
  final String? idioma;

  /// Igual que el diagnóstico antiguo: `onboarding` y `nivel` (el que eligió
  /// en el registro, 0–10).
  final Map<String, dynamic> configuracion;

  @override
  ConsumerState<UbicacionScreen> createState() => _UbicacionScreenState();
}

enum _Fase { cargando, pregunta, intro, test, escritura, resultado }

class _UbicacionScreenState extends ConsumerState<UbicacionScreen> {
  /// Puntos de partida con contenido en este idioma (sin «Avanzado» si el
  /// curso solo llega a N1).
  List<(Autodeclaracion, String, String)> get _opciones => [
    for (final o in _todasLasOpciones)
      if (Autodeclaracion.hasta(nivelMaximo).contains(o.$1)) o,
  ];

  List<(Autodeclaracion, String, String)> get _todasLasOpciones => [
    (
      Autodeclaracion.nada,
      tr('Nada, empiezo de cero'),
      tr('Nunca lo he estudiado'),
    ),
    (
      Autodeclaracion.poco,
      tr('Un poco'),
      tr('Saludos, palabras sueltas, frases simples'),
    ),
    (
      Autodeclaracion.defiendo,
      tr('Me defiendo'),
      tr('Conversaciones cotidianas sencillas'),
    ),
    (
      Autodeclaracion.bastante,
      tr('Bastante'),
      tr('Entiendo textos y conversaciones normales'),
    ),
    (
      Autodeclaracion.avanzado,
      tr('Avanzado'),
      tr('Uso el {idioma} en el trabajo o los estudios', {
        'idioma': _nombreIdioma(idioma),
      }),
    ),
  ];

  late final String idioma =
      widget.idioma ??
      widget.configuracion['idioma'] as String? ??
      ref.read(progressProvider).idiomaMeta;
  _Fase fase = _Fase.cargando;
  List<ItemUbicacion> banco = [];

  /// Nivel más alto que puede dar la prueba (banco ∩ niveles publicados).
  int nivelMaximo = 0;
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
      final b = await ref.read(bancoUbicacionProvider(idioma).future);
      if (b == null) throw StateError('sin banco v2 para $idioma');
      // Consignas y feedback en el idioma de la interfaz ({es, en}).
      banco = b.banco(ref.read(progressProvider).interfaz);
      nivelMaximo = b.nivelMaximo;
    } catch (e) {
      error = tr(
        'No pudimos cargar la prueba. Revisa la conexión e inténtalo otra vez.',
      );
    }
    if (!mounted) return;
    final nivel = widget.configuracion['nivel'];
    setState(() {
      // En el registro ya eligió su punto de partida: no se lo preguntamos
      // otra vez (salvo «desde cero», que confirma aquí).
      if (esOnboarding && nivel is int && nivel > 0 && nivelMaximo > 0) {
        _empezar(
          Autodeclaracion.desdeNivel(min(nivel, nivelMaximo)),
          mostrarIntro: true,
        );
      } else {
        fase = _Fase.pregunta;
      }
    });
  }

  void _empezar(Autodeclaracion d, {bool mostrarIntro = false}) {
    u = Ubicacion(banco: banco, declarado: d, nivelMaximo: nivelMaximo);
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
      'idioma': idioma,
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
      'idioma': idioma,
      'nivelMaximo': nivelMaximo,
    });
    final datos = _json(nivel);
    final st = ref.read(progressProvider);
    if (st.onboardingDone && !esOnboarding && st.idiomaMeta == idioma) {
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
        title: Text(tr('Prueba de nivel')),
        leading: IconButton(
          icon: const Icon(Icons.close),
          tooltip: tr('Salir'),
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
        tr('¿Cuánto {idioma} sabes?', {'idioma': _nombreIdioma(idioma)}),
        style: Theme.of(context).textTheme.headlineSmall
            ?.copyWith(fontWeight: FontWeight.w900),
      ),
      const SizedBox(height: 8),
      Text(
        tr(
          'Así empezamos la prueba en tu nivel. Dura unos 8 minutos y se adapta: '
          'sube de dificultad mientras aciertas y se detiene cuando llega a tu límite.',
        ),
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
        tr('Comprobemos tu {idioma}', {'idioma': _nombreIdioma(idioma)}),
        style: Theme.of(context).textTheme.headlineSmall
            ?.copyWith(fontWeight: FontWeight.w900),
      ),
      const SizedBox(height: 10),
      Text(
        tr(
          'Unos 8 minutos: escucha, lectura, gramática y vocabulario, y al final '
          'una o dos frases escritas. La prueba se adapta a ti: si algo es '
          'demasiado difícil, no pasa nada, es justo lo que buscamos.',
        ),
      ),
      const SizedBox(height: 24),
      FilledButton(onPressed: _siguiente, child: Text(tr('Empezar'))),
      const SizedBox(height: 8),
      TextButton(
        onPressed: () => setState(() {
          u = Ubicacion(
            banco: banco,
            declarado: Autodeclaracion.nada,
            nivelMaximo: nivelMaximo,
          );
          _mostrarResultado();
        }),
        child: Text(tr('Prefiero empezar desde cero')),
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
              label: Text(_habilidad(i.habilidad)),
              backgroundColor: OL.moradoSuave,
            ),
            const Spacer(),
            if (escritura)
              TextButton(
                onPressed: () {
                  u!.omitirEscritura();
                  _mostrarResultado();
                },
                child: Text(tr('Omitir')),
              ),
          ],
        ),
        if (escritura)
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Text(
              tr(
                'Último paso: escribe con tus palabras. Si prefieres, puedes omitirlo.',
              ),
            ),
          ),
        ItemView(
          key: ValueKey('${i.item.id}:$indice'),
          item: i.item,
          // Voz y corrección en el idioma evaluado.
          idioma: idioma,
          cadena: [ref.read(progressProvider).interfaz, 'es'],
          guiada: false,
          permitirReintento: false,
          // Prueba de nivel limpia, sin Lumo.
          lumo: false,
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
          r.desdeCero
              ? tr('Empiezas desde cero')
              : tr('Tu nivel: N{nivel}', {'nivel': r.nivel}),
          style: t.headlineMedium?.copyWith(fontWeight: FontWeight.w900),
        ),
        const SizedBox(height: 6),
        Text(
          r.desdeCero
              ? tr(
                  'Perfecto: te guiamos paso a paso desde los sonidos y las '
                  'primeras frases. Avanzarás rápido.',
                )
              : tr(
                  '{cefr} · {preguntas} preguntas. '
                  'Empieza en la primera clase del nivel; los niveles '
                  'anteriores quedan disponibles para repasar.',
                  {'cefr': cefrNivel(r.nivel), 'preguntas': r.preguntas},
                ),
        ),
        if (!r.desdeCero) ...[
          const SizedBox(height: 20),
          for (final e in r.habilidades.entries) _barra(e.key, e.value),
          if (r.escritura != null) _barra('escritura', r.escritura!),
          if (r.reforzar.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text(
              tr('Te conviene reforzar: {habilidades}.', {
                'habilidades': r.reforzar
                    .map((h) => _habilidad(h).toLowerCase())
                    .join(', '),
              }),
            ),
          ],
          const SizedBox(height: 20),
          Text(tr('¿Dónde quieres empezar?'), style: t.titleMedium),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            children: [
              // Se puede empezar más abajo, nunca más arriba: para subir está
              // la prueba de cada nivel.
              for (final n in {if (r.nivel > 1) r.nivel - 1, r.nivel})
                ChoiceChip(
                  label: Text(
                    n == r.nivel
                        ? tr('N{n} (recomendado)', {'n': n})
                        : 'N$n',
                  ),
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
            r.desdeCero
                ? tr('Empezar desde cero')
                : tr('Empezar en N{nivel}', {'nivel': nivel}),
          ),
        ),
      ],
    );
  }

  Widget _barra(String h, int nivel) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Row(
      children: [
        SizedBox(width: 110, child: Text(_habilidad(h))),
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
            nivel == 0 ? tr('inicio') : 'N$nivel',
            textAlign: TextAlign.end,
            style: const TextStyle(fontWeight: FontWeight.w800),
          ),
        ),
      ],
    ),
  );
}

/// Nombre del idioma evaluado dentro de una frase («¿Cuánto francés
/// sabes?»), en el idioma de la interfaz.
String _nombreIdioma(String code) => switch (code) {
  'en' => tr('inglés'),
  'fr' => tr('francés'),
  _ => idioma(code).nombre,
};

/// Nombre de la habilidad (`nombresHabilidad`) en el idioma de la interfaz.
String _habilidad(String h) => switch (h) {
  'escucha' => tr('Escucha'),
  'lectura' => tr('Lectura'),
  'gramatica' => tr('Gramática'),
  'vocabulario' => tr('Vocabulario'),
  'escritura' => tr('Escritura'),
  _ => nombresHabilidad[h] ?? h,
};

/// MCER de cada nivel del curso (escala cliente).
/// Ojo: también se guarda en el diagnóstico (`cefr`), por eso no se traduce aquí.
/// `/prueba-nivel`: los idiomas con ruta y banco v2 (inglés, francés…) usan
/// la prueba v2; los demás, el diagnóstico anterior.
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
    final anterior = DiagnosticoScreen(
      idioma: idioma,
      configuracion: configuracion,
    );
    if (!idiomasConRuta.contains(meta)) return anterior;
    return ref
        .watch(bancoUbicacionProvider(meta))
        .when(
          loading: () => const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          ),
          error: (_, _) => anterior,
          data: (b) => b == null
              ? anterior
              : UbicacionScreen(idioma: meta, configuracion: configuracion),
        );
  }
}
