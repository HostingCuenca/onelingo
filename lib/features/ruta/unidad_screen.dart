import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../app/theme.dart';
import '../../core/aprendizaje/dominio.dart';
import '../../core/aprendizaje/modelos.dart';
import '../../core/aprendizaje/providers.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/confeti.dart';
import '../../shared/widgets/widgets.dart';
import 'item_view.dart';

/// Una pantalla del recorrido de la unidad: un paso de enseñanza, el diálogo
/// de una situación o un ítem.
class _Pantalla {
  const _Pantalla(this.paso, [this.item]);
  final Paso paso;
  final Item? item;
}

List<_Pantalla> _pantallasDe(UnidadRuta u, {required bool repaso}) {
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
      res.addAll(p.items.map((i) => _Pantalla(p, i)));
    }
  }
  return res;
}

class UnidadScreen extends ConsumerWidget {
  const UnidadScreen({super.key, required this.unidadId, this.repaso = false});
  final String unidadId;
  final bool repaso;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final idioma = unidadId.split('.').first;
    final ruta = ref.watch(rutaProvider(idioma));
    return ruta.when(
      loading: () => const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (e, _) => Scaffold(
        appBar: AppBar(),
        body: const Center(child: Text('No se pudo cargar la unidad.')),
      ),
      data: (r) {
        final u = r?.unidad(unidadId);
        if (r == null || u == null) {
          return Scaffold(
            appBar: AppBar(),
            body: const Center(child: Text('Esta unidad no existe.')),
          );
        }
        return _UnidadRecorrido(ruta: r, unidad: u, repaso: repaso);
      },
    );
  }
}

class _UnidadRecorrido extends ConsumerStatefulWidget {
  const _UnidadRecorrido({
    required this.ruta,
    required this.unidad,
    required this.repaso,
  });
  final RutaCargada ruta;
  final UnidadRuta unidad;
  final bool repaso;
  @override
  ConsumerState<_UnidadRecorrido> createState() => _UnidadRecorridoState();
}

class _UnidadRecorridoState extends ConsumerState<_UnidadRecorrido> {
  late final pantallas = _pantallasDe(widget.unidad, repaso: widget.repaso);
  final scroll = ScrollController();
  int indice = 0;

  /// Primera respuesta de cada ítem puntuable en este intento.
  final primeras = <String, bool>{};
  bool terminado = false;
  bool? aprobada;
  bool nivelNuevo = false;

  UnidadRuta get u => widget.unidad;
  String get claveProgreso => 'onelingo.ruta.pos.${u.id}';
  List<String> get cadena =>
      cadenaDelAlumno(ref.read(progressProvider), widget.ruta.curso);
  String t(TextoApoyo? texto) => texto?.en(cadena) ?? '';

  @override
  void initState() {
    super.initState();
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
      if (mounted && seguro > 0 &&
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
            (widget.repaso || p.paso.tipo == TipoPaso.evaluacion))
          '${p.paso.id}:${p.item!.id}',
    ];
    final aciertos = puntuables.where((k) => primeras[k] == true).length;
    if (widget.repaso) {
      registro.repaso(u, aciertos, puntuables.length);
      setState(() {
        terminado = true;
        aprobada = puntuables.isNotEmpty && aciertos / puntuables.length >= u.umbral;
      });
      return;
    }
    final ok = registro.evaluacion(u, aciertos, puntuables.length);
    final nivel = ok && registro.comprobarNivel(widget.ruta, u.nivel);
    setState(() {
      terminado = true;
      aprobada = aciertos / puntuables.length >= u.umbral;
      nivelNuevo = nivel;
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
      TipoPaso.explicacion || TipoPaso.patron => 'Aprende',
      TipoPaso.ejemplos => 'Ejemplos',
      TipoPaso.vocabulario => 'Vocabulario',
      TipoPaso.practicaGuiada => 'Práctica con ayuda',
      TipoPaso.practicaIndependiente => 'Practica tú',
      TipoPaso.situacion => 'En situación',
      TipoPaso.evaluacion => 'Comprueba',
    };
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.repaso ? 'Repaso · ${t(u.titulo)}' : t(u.titulo)),
        leading: IconButton(
          tooltip: 'Volver a la ruta',
          icon: const Icon(Icons.close_rounded),
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/fundamentos'),
        ),
      ),
      body: Movil(
        child: ListView(
          controller: scroll,
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
          children: terminado
              ? _resultado(context)
              : [
                  BarraProgreso((indice + 1) / pantallas.length, alto: 8),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Etiqueta(nombreTipo),
                      const Spacer(),
                      Text(
                        '${indice + 1} / ${pantallas.length}',
                        style: const TextStyle(color: OL.gris),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  ..._contenido(context, pantalla),
                ],
        ),
      ),
    );
  }

  List<Widget> _contenido(BuildContext context, _Pantalla pantalla) {
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
                'Ya puedes leer esta unidad. Para practicarla, primero practica «${t(previa?.titulo)}».',
                style: const TextStyle(fontSize: 18, height: 1.4),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        BotonPrincipal(
          onPressed: () =>
              context.canPop() ? context.pop() : context.go('/fundamentos'),
          child: Text('VOLVER A LA RUTA'),
        ),
      ];
    }
    if (item != null) {
      final guiada = p.tipo == TipoPaso.practicaGuiada;
      final evalua = widget.repaso || p.tipo == TipoPaso.evaluacion;
      return [
        ItemView(
          key: ValueKey('${p.id}:${item.id}:$indice'),
          item: item,
          idioma: idioma,
          cadena: cadena,
          guiada: guiada,
          permitirReintento: !evalua,
          onComprobado: (correcta, respuesta) {
            if (evalua) {
              primeras.putIfAbsent('${p.id}:${item.id}', () => correcta);
            }
            ref.read(registroRutaProvider).item(
              u,
              p,
              item,
              correcta: correcta,
              respuesta: respuesta,
            );
          },
          onContinuar: siguiente,
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
            child: Text(t(p.texto), style: const TextStyle(fontSize: 19, height: 1.5)),
          ),
        );
        if (indice == 0) {
          vista.add(const SizedBox(height: 10));
          vista.add(_objetivo());
        }
      case TipoPaso.vocabulario:
        vista.add(
          const Text(
            'Toca el altavoz para escuchar cada palabra.',
            style: TextStyle(color: OL.gris, fontSize: 16),
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
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  decoration: BoxDecoration(
                    color: OL.moradoSuave,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: OL.morado),
                  ),
                  child: Column(
                    children: [
                      Text(
                        f.texto,
                        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900),
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
      case TipoPaso.situacion:
        vista.add(
          Tarjeta(
            color: OL.azulSuave,
            borde: OL.azul,
            child: Text(t(p.contexto), style: const TextStyle(fontSize: 18, height: 1.4)),
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
          child: const Text('VOLVER AL PASO ANTERIOR'),
        ),
      BotonPrincipal(
        onPressed: siguiente,
        child: Text(
            p.tipo == TipoPaso.situacion ? 'PARTICIPAR' : 'SIGUIENTE',
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
            'Objetivo: ${t(u.objetivo)}',
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
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (hablante != null)
                  Text(
                    hablante,
                    style: const TextStyle(color: OL.morado, fontWeight: FontWeight.w800),
                  ),
                Text(
                  texto,
                  style: const TextStyle(fontSize: 21, fontWeight: FontWeight.w800),
                ),
                if (rom != null)
                  Text(rom, style: const TextStyle(color: OL.gris, fontSize: 16)),
                Text(traduccion, style: const TextStyle(fontSize: 17)),
                if (nota.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(top: 4),
                    child: Text(
                      nota,
                      style: const TextStyle(color: OL.gris, fontSize: 15, height: 1.3),
                    ),
                  ),
              ],
            ),
          ),
          BotonAudio(texto: texto, idioma: u.idioma),
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
        if (p.item != null && primeras['${p.paso.id}:${p.item!.id}'] == false) p,
    ];
    return [
      if (ok) const SizedBox(height: 120, child: Confeti()),
      Tarjeta(
        color: ok ? OL.verdeSuave : OL.moradoSuave,
        borde: ok ? OL.verde : OL.moradoClaro,
        padding: const EdgeInsets.all(22),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Icon(
              ok ? Icons.emoji_events_outlined : Icons.school_outlined,
              size: 56,
              color: ok ? OL.verde : OL.morado,
            ),
            const SizedBox(height: 8),
            Text(
              widget.repaso
                  ? (ok ? '¡Lo recuerdas!' : 'Hay que repasarlo')
                  : ok
                  ? '¡Unidad aprobada!'
                  : 'Todavía no, vamos a repasarlo',
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w900),
            ),
            const SizedBox(height: 8),
            Text(
              '$aciertos de $puntuables correctas a la primera. Se necesita el ${(u.umbral * 100).round()} %.',
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 17),
            ),
            if (ok && !widget.repaso)
              const Padding(
                padding: EdgeInsets.only(top: 8),
                child: Text(
                  'Aprobar no es lo mismo que dominar: te pediremos un repaso breve dentro de unos días para comprobar que lo recuerdas.',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: OL.gris, fontSize: 15, height: 1.4),
                ),
              ),
          ],
        ),
      ),
      if (nivelNuevo) ...[
        const SizedBox(height: 14),
        Tarjeta(
          color: OL.amarilloSuave,
          borde: OL.amarillo,
          child: Text(
            u.nivel == 'f0'
                ? '¡Completaste los Fundamentos! Ya tienes el Nivel 1 disponible.'
                : '¡Completaste ${t(tituloNivel)}!',
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
          ),
        ),
      ],
      if (!ok && fallos.isNotEmpty) ...[
        const SizedBox(height: 16),
        const Text(
          'Repasa estos puntos:',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
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
            child: Text('VOLVER A LA EXPLICACIÓN'),
          ),
        const SizedBox(height: 8),
        OutlinedButton(
          onPressed: reintentarEvaluacion,
          child: const Padding(
            padding: EdgeInsets.symmetric(vertical: 14),
            child: Text('INTENTARLO DE NUEVO'),
          ),
        ),
      ],
      if (ok && siguienteUnidad != null && !widget.repaso)
        BotonPrincipal(
          onPressed: () => context.pushReplacement(
            '/fundamentos/unidad/${siguienteUnidad.id}',
          ),
          child: Text('SIGUIENTE: ${t(siguienteUnidad.titulo).toUpperCase()}'),
        ),
      const SizedBox(height: 8),
      OutlinedButton(
        onPressed: () => nivelNuevo
            ? context.go('/aprender')
            : (context.canPop() ? context.pop() : context.go('/fundamentos')),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 14),
          child: Text(nivelNuevo ? 'IR A APRENDER' : 'VER MI RUTA'),
        ),
      ),
    ];
  }
}
