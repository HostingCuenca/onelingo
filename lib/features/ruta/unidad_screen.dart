import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/aprendizaje/biblioteca_adaptador.dart';
import '../../core/aprendizaje/dominio.dart';
import '../../core/aprendizaje/modelos.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/widgets.dart';
import '../../core/efectos.dart';
import 'celebracion.dart';
import 'item_view.dart';
import 'ruta_screen.dart';
import 'tabla_ruta.dart';
import '../../core/i18n/i18n.dart';

/// Una pantalla del recorrido de la unidad: un paso de enseñanza, el diálogo
/// de una situación o un ítem.
class _Pantalla {
  const _Pantalla(
    this.paso, [
    this.item,
    this.repetida = false,
    this.variantId,
    this.libraryVersion,
    this.selectionId,
  ]);
  final Paso paso;
  final Item? item;
  final String? variantId, libraryVersion, selectionId;

  /// Ejercicio fallado que vuelve al final de su bloque.
  final bool repetida;
}

const _nombreIdioma = {
  'en': 'inglés',
  'es': 'español',
  'fr': 'francés',
  'de': 'alemán',
  'pt': 'portugués',
  'it': 'italiano',
  'zh': 'chino',
  'ja': 'japonés',
  'ko': 'coreano',
  'ru': 'ruso',
};

/// Ejercicios extra hechos con el material ya revisado de la clase, para que
/// cada clase no sea siempre elegir/completar/ordenar/escuchar: «Une las
/// parejas» con su vocabulario y «Escribe en …» con uno de sus ejemplos
/// (lo corrige la IA si no coincide exactamente).
({Item? unir, Item? escribir}) _ejerciciosDeClase(
  UnidadRuta u,
  List<String> cadena,
) {
  // Solo las clases editoriales N1–N10 (siempre la misma plantilla); las
  // unidades de Fundamentos tienen una secuencia diseñada a mano.
  if (!_claseEditorial.hasMatch(u.id)) return (unir: null, escribir: null);
  final semilla = u.id.codeUnits.fold<int>(
    7,
    (h, c) => (h * 31 + c) & 0x3fffffff,
  );
  Item? unir, escribir;
  final vocab = u.pasos.where((p) => p.tipo == TipoPaso.vocabulario);
  final palabras = <Vocablo>[];
  final vistos = <String>{};
  for (final p in vocab) {
    for (final id in p.refs) {
      final v = u.vocablo(id);
      final sentido = v?.traduccion.en(cadena).trim().toLowerCase() ?? '';
      if (v == null || v.texto.trim().isEmpty || sentido.isEmpty) continue;
      if (!vistos.add(sentido) || !vistos.add(v.texto.toLowerCase())) continue;
      palabras.add(v);
    }
  }
  if (palabras.length >= 3) {
    palabras.shuffle(Random(semilla));
    unir = Item(
      id: '${u.id}.dinamico.unir',
      formato: FormatoItem.relacionar,
      consigna: const TextoApoyo({'es': 'Une cada palabra con su significado'}),
      feedback: const TextoApoyo({
        'es': 'Son palabras de esta clase: repásalas en voz alta.',
      }),
      pares: [for (final v in palabras.take(4)) (v.texto, v.traduccion)],
    );
  }
  final ejemplos = [
    for (final p in u.pasos.where((p) => p.tipo == TipoPaso.ejemplos))
      ...p.frases.where(
        (f) => f.texto.trim().isNotEmpty && !f.traduccion.isEmpty,
      ),
  ];
  if (ejemplos.isNotEmpty) {
    final f = ejemplos[semilla % ejemplos.length];
    escribir = Item(
      id: '${u.id}.dinamico.escribir',
      formato: FormatoItem.escribir,
      consigna: TextoApoyo({
        'es': 'Escribe esta frase en ${_nombreIdioma[u.idioma] ?? u.idioma}',
      }),
      feedback: const TextoApoyo({'es': 'Es uno de los ejemplos de la clase.'}),
      texto: f.traduccion.en(cadena),
      respuesta: f.texto,
      aceptadas: [f.texto],
    );
  }
  return (unir: unir, escribir: escribir);
}

final _claseEditorial = RegExp(r'\.n\d+\.class-');

/// Añade el ejercicio extra solo si ese formato no aparece ya en el bloque
/// que verá el alumno.
void _anadirSiFalta(
  List<_Pantalla> bloque,
  Paso paso,
  Item? item, {
  bool alInicio = false,
}) {
  if (item == null || bloque.any((p) => p.item?.formato == item.formato)) {
    return;
  }
  bloque.insert(alInicio ? 0 : bloque.length, _Pantalla(paso, item));
}

/// Alterna los formatos: evita dos ejercicios seguidos del mismo tipo cuando
/// hay otro disponible (sin cambiar qué ejercicios se hacen).
List<_Pantalla> _alternar(List<_Pantalla> bloque) {
  final pendientes = [...bloque], res = <_Pantalla>[];
  while (pendientes.isNotEmpty) {
    final anterior = res.isEmpty ? null : res.last.item?.formato;
    final i = pendientes.indexWhere((p) => p.item?.formato != anterior);
    res.add(pendientes.removeAt(i < 0 ? 0 : i));
  }
  return res;
}

/// Formatos de los ejercicios de una clase en el orden en que se ven.
@visibleForTesting
List<FormatoItem> formatosDeClase(
  UnidadRuta u, {
  List<String> cadena = const ['es'],
}) => [
  for (final p in _pantallasDe(u, repaso: false, cadena: cadena))
    if (p.item != null) p.item!.formato,
];

List<_Pantalla> _pantallasDe(
  UnidadRuta u, {
  required bool repaso,
  BibliotecaUnidadRuntime? runtime,
  List<String> cadena = const ['es'],
}) {
  if (runtime?.activa == true) {
    return _pantallasBiblioteca(
      u,
      repaso: repaso,
      runtime: runtime!,
      cadena: cadena,
    );
  }
  final extra = repaso ? null : _ejerciciosDeClase(u, cadena);
  final practicaExtra = Paso(
    id: '${u.id}.dinamico',
    tipo: TipoPaso.practicaIndependiente,
  );
  final res = <_Pantalla>[];
  for (final p in u.pasos) {
    if (repaso) {
      if (p.tipo == TipoPaso.practicaIndependiente ||
          p.tipo == TipoPaso.evaluacion) {
        res.addAll(p.items.map((i) => _Pantalla(p, i)));
      }
      continue;
    }
    if (p.tipo.ensena) {
      res.add(_Pantalla(p));
    } else {
      if (p.tipo == TipoPaso.situacion) res.add(_Pantalla(p));
      final bloque = [for (final i in p.items) _Pantalla(p, i)];
      if (p.tipo == TipoPaso.practicaGuiada) {
        _anadirSiFalta(bloque, practicaExtra, extra?.unir, alInicio: true);
      }
      if (p.tipo == TipoPaso.practicaIndependiente) {
        _anadirSiFalta(bloque, practicaExtra, extra?.escribir);
      }
      res.addAll(
        p.tipo == TipoPaso.evaluacion || !_claseEditorial.hasMatch(u.id)
            ? bloque
            : _alternar(bloque),
      );
    }
  }
  return res;
}

List<_Pantalla> _pantallasBiblioteca(
  UnidadRuta u, {
  required bool repaso,
  required BibliotecaUnidadRuntime runtime,
  List<String> cadena = const ['es'],
}) {
  final result = <_Pantalla>[];
  final extra = repaso ? null : _ejerciciosDeClase(u, cadena);
  final practicaExtra = Paso(
    id: '${u.id}.dinamico',
    tipo: TipoPaso.practicaIndependiente,
  );

  void addPool(
    String pool,
    TipoPaso type,
    String suffix, {
    Item? antes,
    Item? despues,
  }) {
    final selection = runtime.pool(pool);
    if (selection == null) return;
    final step = Paso(
      id: '${u.id}.$suffix',
      tipo: type,
      items: [
        for (final variant in selection.variants) itemDesdeVariante(variant),
      ],
    );
    final bloque = <_Pantalla>[];
    for (var index = 0; index < step.items.length; index++) {
      final variant = selection.variants[index];
      bloque.add(
        _Pantalla(
          step,
          step.items[index],
          false,
          variant.id,
          runtime.libraryVersion,
          selection.selectionId,
        ),
      );
    }
    _anadirSiFalta(bloque, practicaExtra, antes, alInicio: true);
    _anadirSiFalta(bloque, practicaExtra, despues);
    result.addAll(
      type == TipoPaso.evaluacion || !_claseEditorial.hasMatch(u.id)
          ? bloque
          : _alternar(bloque),
    );
  }

  if (repaso) {
    addPool('review', TipoPaso.practicaIndependiente, 'review');
    return result;
  }
  for (final step in u.pasos.where((step) => step.tipo.ensena)) {
    result.add(_Pantalla(step));
  }
  addPool(
    'practiceGuided',
    TipoPaso.practicaGuiada,
    'guided',
    antes: extra?.unir,
  );
  addPool(
    'practice',
    TipoPaso.practicaIndependiente,
    'practice',
    despues: extra?.escribir,
  );
  for (final step in u.pasos.where((step) => step.tipo == TipoPaso.situacion)) {
    result.add(_Pantalla(step));
    // Ítem propio de la situación (enriquecimiento editorial). Las clases aún
    // sin enriquecer traen una copia de la práctica (`situation-check`), que
    // no se repite.
    result.addAll(
      step.items
          .where((item) => !item.id.contains('situation-check'))
          .map((item) => _Pantalla(step, item)),
    );
  }
  addPool('evaluation', TipoPaso.evaluacion, 'evaluation');
  return result;
}

class UnidadScreen extends ConsumerWidget {
  const UnidadScreen({super.key, required this.unidadId, this.repaso = false});
  final String unidadId;
  final bool repaso;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final idioma = unidadId.split('.').first;
    final ruta = ref.watch(rutaProvider(idioma));
    final runtime = ref.watch(
      bibliotecaUnidadRuntimeProvider((idioma: idioma, unidad: unidadId)),
    );
    return ruta.when(
      loading: () =>
          const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (e, _) => Scaffold(
        appBar: AppBar(),
        body: Center(child: Text(tr('No se pudo cargar la unidad.'))),
      ),
      data: (r) {
        final u = r?.unidad(unidadId);
        if (r == null || u == null) {
          // Unidades retiradas al reorganizar el curso (p. ej. el A1 de 29
          // unidades pasó a Nivel 1): se ofrece el nivel que las sustituye.
          final nivel = unidadId.startsWith('en.a1.') ? 'a1-1' : null;
          final sustituto = r == null || nivel == null
              ? null
              : resolverNivelHistorico(r, nivel);
          if (sustituto != null &&
              sustituto != nivel &&
              r!.delNivel(sustituto).isNotEmpty) {
            return Scaffold(
              appBar: AppBar(),
              body: Center(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        tr('Esta lección se renovó y ahora forma parte de un nivel nuevo.'),
                        textAlign: TextAlign.center,
                        style: const TextStyle(fontSize: 18),
                      ),
                      const SizedBox(height: 20),
                      BotonPrincipal(
                        onPressed: () => context.go('/ruta/$sustituto'),
                        child: Text(tr('IR AL NIVEL')),
                      ),
                    ],
                  ),
                ),
              ),
            );
          }
          return Scaffold(
            appBar: AppBar(),
            body: Center(child: Text(tr('Esta unidad no existe.'))),
          );
        }
        return runtime.when(
          loading: () =>
              const Scaffold(body: Center(child: CircularProgressIndicator())),
          error: (_, _) => Scaffold(
            appBar: AppBar(),
            body: Center(
              child: Text(tr('No se pudo preparar la biblioteca de ejercicios.')),
            ),
          ),
          data: (resolved) {
            if (resolved.diagnostico.activacion == EstadoBiblioteca.active &&
                !resolved.activa) {
              return Scaffold(
                appBar: AppBar(),
                body: Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Text(
                      '${tr('Esta clase está temporalmente fuera de servicio. '
                          'No se sustituyó silenciosamente por contenido antiguo.')}'
                      '\n\n${resolved.diagnostico.errores.join('\n')}',
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
              );
            }
            return _UnidadRecorrido(
              ruta: r,
              unidad: u,
              repaso: repaso,
              runtime: resolved,
            );
          },
        );
      },
    );
  }
}

class _UnidadRecorrido extends ConsumerStatefulWidget {
  const _UnidadRecorrido({
    required this.ruta,
    required this.unidad,
    required this.repaso,
    required this.runtime,
  });
  final RutaCargada ruta;
  final UnidadRuta unidad;
  final bool repaso;
  final BibliotecaUnidadRuntime runtime;
  @override
  ConsumerState<_UnidadRecorrido> createState() => _UnidadRecorridoState();
}

class _UnidadRecorridoState extends ConsumerState<_UnidadRecorrido> {
  late final List<_Pantalla> pantallas = _pantallasDe(
    widget.unidad,
    repaso: widget.repaso,
    runtime: widget.runtime,
    cadena: cadenaDelAlumno(ref.read(progressProvider), widget.ruta.curso),
  );

  /// Un ejercicio de práctica fallado vuelve al final de su bloque (una vez
  /// pendiente a la vez), en lugar de bloquear el avance.
  void _repetirAlFinal(Paso paso, Item item) {
    final yaPendiente = pantallas
        .skip(indice + 1)
        .any((p) => p.paso.id == paso.id && p.item?.id == item.id);
    if (yaPendiente) return;
    final ultimo = pantallas.lastIndexWhere((p) => p.paso.id == paso.id);
    final current = pantallas[indice];
    pantallas.insert(
      ultimo + 1,
      _Pantalla(
        paso,
        item,
        true,
        current.variantId,
        current.libraryVersion,
        current.selectionId,
      ),
    );
  }

  final scroll = ScrollController();
  int indice = 0;

  /// Primera respuesta de cada ítem puntuable en este intento.
  final primeras = <String, bool>{};
  bool terminado = false;
  bool? aprobada;
  bool nivelNuevo = false;

  /// Para la celebración: XP ganada y tiempo dedicado en esta sesión.
  late final int xpInicial = ref.read(progressProvider).xp;
  final reloj = Stopwatch()..start();
  int xpGanada = 0;
  Duration duracion = Duration.zero;

  UnidadRuta get u => widget.unidad;
  String get claveProgreso => 'onelingo.ruta.pos.${u.id}';
  List<String> get cadena =>
      cadenaDelAlumno(ref.read(progressProvider), widget.ruta.curso);
  String t(TextoApoyo? texto) => texto?.en(cadena) ?? '';

  @override
  void initState() {
    super.initState();
    xpInicial;
    if (!widget.repaso) {
      // Modificar el estado durante el build lanza una excepción en Riverpod.
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) ref.read(registroRutaProvider).visto(u);
      });
      unawaited(_reanudar());
    }
  }

  Future<void> _reanudar() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final guardado = prefs.getInt(claveProgreso) ?? 0;
      // Se reanuda en la enseñanza o práctica, nunca a mitad de la evaluación.
      final seguro = guardado.clamp(0, pantallas.length - 1);
      if (mounted &&
          seguro > 0 &&
          pantallas[seguro].paso.tipo != TipoPaso.evaluacion) {
        setState(() => indice = seguro);
      }
    } catch (_) {}
  }

  void _guardarPosicion() {
    if (widget.repaso) return;
    unawaited(
      SharedPreferences.getInstance()
          .then((p) => p.setInt(claveProgreso, indice))
          .catchError((_) => true),
    );
  }

  @override
  void dispose() {
    unawaited(VozNube.instancia.parar().catchError((_) {}));
    scroll.dispose();
    super.dispose();
  }

  bool get bloqueada {
    final estados = estadosAlumno(widget.ruta, ref.read(progressProvider));
    return estados[u.id]?.estado == EstadoUnidad.bloqueada;
  }

  void ir(int nuevo) {
    unawaited(VozNube.instancia.parar().catchError((_) {}));
    setState(() => indice = nuevo);
    _guardarPosicion();
    if (scroll.hasClients) scroll.jumpTo(0);
  }

  void siguiente() {
    if (indice < pantallas.length - 1) {
      ir(indice + 1);
    } else {
      _terminar();
    }
  }

  void _terminar() {
    final registro = ref.read(registroRutaProvider);
    final puntuables = [
      for (final p in pantallas)
        if (p.item != null &&
            !p.item!.abierta &&
            (widget.repaso || p.paso.tipo == TipoPaso.evaluacion))
          '${p.paso.id}:${p.item!.id}',
    ];
    final aciertos = puntuables.where((k) => primeras[k] == true).length;
    duracion = reloj.elapsed;
    reloj.stop();
    if (widget.repaso) {
      registro.repaso(u, aciertos, puntuables.length);
      final superado = superaUmbral(aciertos, puntuables.length, u.umbral);
      if (superado) Efectos.completado();
      setState(() {
        terminado = true;
        aprobada = superado;
        xpGanada = ref.read(progressProvider).xp - xpInicial;
      });
      return;
    }
    final ok = registro.evaluacion(u, aciertos, puntuables.length);
    final nivel = ok && registro.comprobarNivel(widget.ruta, u.nivel);
    final aprobadaAhora = superaUmbral(aciertos, puntuables.length, u.umbral);
    // Recompensa sonora: fanfarria al completar el nivel, campanas al aprobar.
    if (nivel) {
      Efectos.nivel();
    } else if (aprobadaAhora) {
      Efectos.completado();
    }
    setState(() {
      terminado = true;
      aprobada = aprobadaAhora;
      nivelNuevo = nivel;
      xpGanada = ref.read(progressProvider).xp - xpInicial;
    });
    if (aprobada == true) _guardarPosicionInicio();
  }

  void _guardarPosicionInicio() => unawaited(
    SharedPreferences.getInstance()
        .then((p) => p.remove(claveProgreso))
        .catchError((_) => true),
  );

  void reintentarEvaluacion() {
    final inicioEval = pantallas.indexWhere(
      (p) => p.paso.tipo == TipoPaso.evaluacion,
    );
    primeras.clear();
    setState(() {
      terminado = false;
      aprobada = null;
    });
    ir(widget.repaso ? 0 : inicioEval);
  }

  void volverAEnsenar() {
    primeras.clear();
    setState(() {
      terminado = false;
      aprobada = null;
    });
    ir(0);
  }

  @override
  Widget build(BuildContext context) {
    ref.watch(progressProvider);
    final pantalla = pantallas[indice];
    final nombreTipo = switch (pantalla.paso.tipo) {
      TipoPaso.explicacion ||
      TipoPaso.patron ||
      TipoPaso.tabla => tr('Aprende'),
      TipoPaso.ejemplos => tr('Ejemplos'),
      TipoPaso.vocabulario => tr('Vocabulario'),
      TipoPaso.practicaGuiada => tr('Práctica con ayuda'),
      TipoPaso.practicaIndependiente => tr('Practica tú'),
      TipoPaso.situacion => tr('En situación'),
      TipoPaso.evaluacion => tr('Comprueba'),
    };
    return Scaffold(
      appBar: AppBar(
        title: Text(
          widget.repaso
              ? tr('Repaso · {titulo}', {'titulo': t(u.titulo)})
              : t(u.titulo),
        ),
        leading: IconButton(
          tooltip: tr('Volver a la ruta'),
          icon: const Icon(Icons.close_rounded),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/fundamentos'),
        ),
      ),
      body: Movil(
        child: !terminado && pantalla.item != null && !bloqueada
            // Ejercicio: cabecera arriba, ejercicio desplazable y el botón
            // COMPROBAR / SIGUIENTE fijo abajo, siempre a la vista.
            ? Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Padding(
                    padding: const EdgeInsets.fromLTRB(20, 12, 20, 12),
                    child: _cabeceraPaso(pantalla, nombreTipo),
                  ),
                  Expanded(
                    child: _contenido(context, pantalla, fijo: true).single,
                  ),
                ],
              )
            : ListView(
                controller: scroll,
                padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
                children: terminado
                    ? _resultado(context)
                    : [
                        _cabeceraPaso(pantalla, nombreTipo),
                        const SizedBox(height: 16),
                        ..._contenido(context, pantalla),
                      ],
              ),
      ),
    );
  }

  /// Progreso de la unidad y tipo de paso (común a lecciones y ejercicios).
  Widget _cabeceraPaso(_Pantalla pantalla, String nombreTipo) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      BarraProgreso((indice + 1) / pantallas.length, alto: 8),
      const SizedBox(height: 12),
      Row(
        children: [
          Expanded(
            child: Wrap(
              spacing: 8,
              runSpacing: 6,
              children: [
                Etiqueta(nombreTipo),
                if (pantalla.repetida)
                  Etiqueta(
                    tr('Otra vez'),
                    color: OL.naranja,
                    fondo: OL.naranjaSuave,
                    icono: Icons.replay_rounded,
                  ),
              ],
            ),
          ),
          Text(
            '${indice + 1} / ${pantallas.length}',
            style: const TextStyle(color: OL.gris),
          ),
        ],
      ),
    ],
  );

  List<Widget> _contenido(
    BuildContext context,
    _Pantalla pantalla, {
    bool fijo = false,
  }) {
    final p = pantalla.paso;
    final item = pantalla.item;
    final idioma = u.idioma;
    if (item != null && bloqueada) {
      final previa = widget.ruta.unidad(u.prerequisitos.first);
      return [
        Tarjeta(
          color: OL.moradoSuave,
          borde: OL.moradoClaro,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(Icons.lock_outline, color: OL.morado, size: 40),
              const SizedBox(height: 10),
              Text(
                tr(
                  'Ya puedes leer esta unidad. Para practicarla, primero practica «{previa}».',
                  {'previa': t(previa?.titulo)},
                ),
                style: const TextStyle(fontSize: 18, height: 1.4),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        BotonPrincipal(
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/fundamentos'),
          child: Text(tr('VOLVER A LA RUTA')),
        ),
      ];
    }
    if (item != null) {
      final guiada = p.tipo == TipoPaso.practicaGuiada;
      final evalua = widget.repaso || p.tipo == TipoPaso.evaluacion;
      return [
        ItemView(
          botonFijo: fijo,
          encabezado: [
            // La pregunta de una situación se responde con el diálogo a la vista.
            if (p.tipo == TipoPaso.situacion && p.frases.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(bottom: 16),
                child: Tarjeta(
                  color: OL.azulSuave,
                  sombra: false,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      for (final linea in p.frases)
                        Padding(
                          padding: const EdgeInsets.symmetric(vertical: 3),
                          child: Text.rich(
                            TextSpan(
                              children: [
                                if (linea.hablante != null)
                                  TextSpan(
                                    text: '${linea.hablante}: ',
                                    style: const TextStyle(
                                      fontWeight: FontWeight.w800,
                                      color: OL.azul,
                                    ),
                                  ),
                                TextSpan(text: linea.texto),
                              ],
                            ),
                            style: const TextStyle(fontSize: 16, height: 1.35),
                          ),
                        ),
                    ],
                  ),
                ),
              ),
          ],
          key: ValueKey('${p.id}:${item.id}:$indice'),
          item: item,
          idioma: idioma,
          cadena: cadena,
          guiada: guiada,
          permitirReintento: !evalua,
          onComprobado: (correcta, respuesta) {
            // La producción abierta no puntúa: solo se compara con el modelo.
            if (evalua && !item.abierta) {
              primeras.putIfAbsent('${p.id}:${item.id}', () => correcta);
            } else if (!correcta) {
              setState(() => _repetirAlFinal(p, item));
            }
            ref
                .read(registroRutaProvider)
                .item(
                  u,
                  p,
                  item,
                  correcta: correcta,
                  respuesta: respuesta,
                  variantId: pantalla.variantId,
                  libraryVersion: pantalla.libraryVersion,
                  selectionId: pantalla.selectionId,
                );
          },
          onContinuar: siguiente,
          // Frases escritas: la IA acepta cualquier forma correcta (no solo
          // las previstas) y explica qué cambiar.
          revisarConIa: (item, respuesta) {
            final s = ref.read(progressProvider);
            return Sync.instancia.revisarEscritura(
              idiomaMeta: idioma,
              idiomaNativo: s.idiomaNativo,
              nivel: s.nivelActual.clamp(1, 10),
              itemId: item.id,
              consigna: item.consigna.en(cadena),
              texto: [
                item.texto,
                item.pregunta,
              ].whereType<String>().join(' · '),
              modelo: item.respuesta ?? '',
              aceptadas: item.aceptadas,
              respuesta: respuesta,
              abierta: item.abierta,
            );
          },
        ),
      ];
    }
    final vista = <Widget>[
      if (p.titulo != null)
        Text(
          t(p.titulo),
          style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w900),
        ),
      if (p.titulo != null) const SizedBox(height: 12),
    ];
    switch (p.tipo) {
      case TipoPaso.explicacion:
        vista.add(
          Tarjeta(
            color: OL.moradoSuave,
            borde: OL.moradoClaro,
            padding: const EdgeInsets.all(20),
            child: Text(
              t(p.texto),
              style: const TextStyle(fontSize: 19, height: 1.5),
            ),
          ),
        );
        if (indice == 0) {
          vista.add(const SizedBox(height: 10));
          vista.add(_objetivo());
        }
      case TipoPaso.vocabulario:
        vista.add(
          Text(
            tr('Toca cualquier parte de la tarjeta para escuchar cada palabra.'),
            style: const TextStyle(color: OL.gris, fontSize: 16),
          ),
        );
        vista.add(const SizedBox(height: 10));
        for (final id in p.refs) {
          final v = u.vocablo(id);
          if (v == null) continue;
          vista.add(_tarjetaFrase(v.texto, v.rom, t(v.traduccion), t(v.nota)));
        }
      case TipoPaso.ejemplos:
        for (final f in p.frases) {
          vista.add(_tarjetaFrase(f.texto, f.rom, t(f.traduccion), t(f.nota)));
        }
      case TipoPaso.patron:
        if (p.texto != null) {
          vista.add(Text(t(p.texto), style: const TextStyle(fontSize: 18)));
          vista.add(const SizedBox(height: 10));
        }
        vista.add(
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              for (final f in p.formula)
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 10,
                  ),
                  decoration: BoxDecoration(
                    color: OL.moradoSuave,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: OL.morado),
                  ),
                  child: Column(
                    children: [
                      Text(
                        f.texto,
                        style: const TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      if (f.nota != null)
                        Text(t(f.nota), style: const TextStyle(color: OL.gris)),
                    ],
                  ),
                ),
            ],
          ),
        );
        vista.add(const SizedBox(height: 14));
        for (final f in p.frases) {
          vista.add(_tarjetaFrase(f.texto, f.rom, t(f.traduccion), t(f.nota)));
        }
      case TipoPaso.tabla:
        if (p.texto != null) {
          vista.add(
            Text(t(p.texto), style: const TextStyle(fontSize: 18, height: 1.4)),
          );
          vista.add(const SizedBox(height: 10));
        }
        vista.add(TablaRuta(paso: p, idioma: u.idioma, cadena: cadena));
        vista.add(const SizedBox(height: 8));
        vista.add(
          Text(
            tr('Toca cada casilla para escucharla.'),
            style: const TextStyle(color: OL.gris, fontSize: 15),
          ),
        );
      case TipoPaso.situacion:
        vista.add(
          Tarjeta(
            color: OL.azulSuave,
            borde: OL.azul,
            child: Text(
              t(p.contexto),
              style: const TextStyle(fontSize: 18, height: 1.4),
            ),
          ),
        );
        vista.add(const SizedBox(height: 12));
        for (final linea in p.frases) {
          final propio = linea.hablante == 'Tú' || linea.hablante == 'You';
          vista.add(
            Align(
              alignment: propio ? Alignment.centerRight : Alignment.centerLeft,
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 340),
                child: Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: _tarjetaFrase(
                    linea.texto,
                    linea.rom,
                    t(linea.traduccion),
                    '',
                    hablante: linea.hablante,
                    color: propio ? OL.moradoSuave : OL.blanco,
                  ),
                ),
              ),
            ),
          );
        }
      default:
        break;
    }
    vista.addAll([
      const SizedBox(height: 18),
      if (indice > 0)
        TextButton(
          onPressed: () => ir(indice - 1),
          child: Text(tr('VOLVER AL PASO ANTERIOR')),
        ),
      BotonPrincipal(
        onPressed: siguiente,
        child: Text(
          p.tipo == TipoPaso.situacion &&
                  p.items.any((i) => !i.id.contains('situation-check'))
              ? tr('PARTICIPAR')
              : tr('SIGUIENTE'),
        ),
      ),
    ]);
    return vista;
  }

  Widget _objetivo() => Tarjeta(
    child: Row(
      children: [
        const Icon(Icons.flag_outlined, color: OL.naranja),
        const SizedBox(width: 10),
        Expanded(
          child: Text(
            tr('Objetivo: {objetivo}', {'objetivo': t(u.objetivo)}),
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700),
          ),
        ),
      ],
    ),
  );

  Widget _tarjetaFrase(
    String texto,
    String? rom,
    String traduccion,
    String nota, {
    String? hablante,
    Color color = OL.blanco,
  }) => Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: Tarjeta(
      color: color,
      padding: const EdgeInsets.fromLTRB(16, 12, 6, 12),
      etiquetaSemantica: tr('Escuchar {texto}', {'texto': texto}),
      onTap: () => escucharTexto(context, texto, u.idioma),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (hablante != null)
                  Text(
                    hablante,
                    style: const TextStyle(
                      color: OL.morado,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                Text(
                  texto,
                  style: const TextStyle(
                    fontSize: 21,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                if (rom != null)
                  Text(
                    rom,
                    style: const TextStyle(color: OL.gris, fontSize: 16),
                  ),
                Text(traduccion, style: const TextStyle(fontSize: 17)),
                if (nota.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(top: 4),
                    child: Text(
                      nota,
                      style: const TextStyle(
                        color: OL.gris,
                        fontSize: 15,
                        height: 1.3,
                      ),
                    ),
                  ),
              ],
            ),
          ),
          const Padding(
            padding: EdgeInsets.all(12),
            child: Icon(Icons.volume_up_outlined, color: OL.morado),
          ),
        ],
      ),
    ),
  );

  List<Widget> _resultado(BuildContext context) {
    final puntuables = primeras.length;
    final aciertos = primeras.values.where((v) => v).length;
    final ok = aprobada == true;
    // La siguiente en orden, aunque sea del nivel siguiente (f0 → A1).
    final siguienteUnidad = widget.ruta.unidades
        .where((x) => x.orden > u.orden)
        .firstOrNull;
    final tituloNivel = widget.ruta.curso.niveles
        .where((n) => n.id == u.nivel)
        .firstOrNull
        ?.titulo;
    final fallos = [
      for (final p in pantallas)
        if (p.item != null && primeras['${p.paso.id}:${p.item!.id}'] == false)
          p,
    ];
    final precision = puntuables == 0
        ? 100
        : (aciertos * 100 / puntuables).round();
    return [
      if (ok)
        CelebracionUnidad(
          nivelCompleto: nivelNuevo,
          titulo: widget.repaso
              ? tr('¡Repaso superado!')
              : nivelNuevo
              ? tr('¡Nivel completado!')
              : tr('¡Lección completada!'),
          subtitulo: widget.repaso
              ? tr('Lo recuerdas: esta unidad queda más firme.')
              : nivelNuevo
              ? (u.nivel == 'f0'
                    ? tr('Completaste los Fundamentos. Ya tienes el Nivel 1 disponible.')
                    : tr('Completaste {nivel}.', {'nivel': t(tituloNivel)}))
              : tr('Aprobar no es lo mismo que dominar: te pediremos un repaso breve dentro de unos días.'),
          fichas: [
            FichaLogro.xp(xpGanada),
            FichaLogro.precision(precision),
            FichaLogro.tiempo(duracion),
          ],
        )
      else
        Tarjeta(
          color: OL.moradoSuave,
          borde: OL.moradoClaro,
          padding: const EdgeInsets.all(22),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(Icons.school_outlined, size: 56, color: OL.morado),
              const SizedBox(height: 8),
              Text(
                widget.repaso
                    ? tr('Hay que repasarlo')
                    : tr('Todavía no, vamos a repasarlo'),
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.w900,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                tr(
                  '{aciertos} de {total} correctas a la primera. Se necesitan {necesarias}.',
                  {
                    'aciertos': aciertos,
                    'total': puntuables,
                    'necesarias': aciertosNecesarios(puntuables, u.umbral),
                  },
                ),
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 17),
              ),
            ],
          ),
        ),
      if (!ok && fallos.isNotEmpty) ...[
        const SizedBox(height: 16),
        Text(
          tr('Repasa estos puntos:'),
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
        ),
        const SizedBox(height: 8),
        for (final f in fallos)
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Tarjeta(
              child: Text(
                '${t(f.item!.consigna)}\n${t(f.item!.feedback)}',
                style: const TextStyle(fontSize: 16, height: 1.4),
              ),
            ),
          ),
      ],
      const SizedBox(height: 18),
      if (!ok) ...[
        if (!widget.repaso)
          BotonPrincipal(
            onPressed: volverAEnsenar,
            child: Text(tr('VOLVER A LA EXPLICACIÓN')),
          ),
        const SizedBox(height: 8),
        OutlinedButton(
          onPressed: reintentarEvaluacion,
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 14),
            child: Text(tr('INTENTARLO DE NUEVO')),
          ),
        ),
      ],
      if (ok && siguienteUnidad != null && !widget.repaso)
        BotonPrincipal(
          onPressed: () => context.pushReplacement(
            '/fundamentos/unidad/${siguienteUnidad.id}',
          ),
          child: Text(
            tr('SIGUIENTE: {unidad}', {
              'unidad': t(siguienteUnidad.titulo).toUpperCase(),
            }),
          ),
        ),
      const SizedBox(height: 8),
      OutlinedButton(
        onPressed: () => nivelNuevo
            ? context.go('/aprender')
            : (context.canPop() ? context.pop() : context.go('/fundamentos')),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 14),
          child: Text(nivelNuevo ? tr('IR A APRENDER') : tr('VER MI RUTA')),
        ),
      ),
    ];
  }
}
