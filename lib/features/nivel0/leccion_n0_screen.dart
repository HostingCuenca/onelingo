import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/efectos.dart';
import '../../core/nivel0/nivel0.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/feedback_experience.dart';
import '../../shared/widgets/lumo.dart';
import '../../shared/widgets/widgets.dart';
import '../../shared/widgets/romanizacion.dart';
import 'palabra_color.dart';
import '../../core/i18n/i18n.dart';

/// Lección del Nivel 0: pasos cortos de escuchar, mirar, juntar sonidos,
/// construir y leer. Un solo personaje a la vez (Lumo en la explicación o
/// en el panel de resultado, nunca los dos).
class LeccionN0Screen extends ConsumerStatefulWidget {
  const LeccionN0Screen({super.key, required this.leccionId});
  final String leccionId;
  @override
  ConsumerState<LeccionN0Screen> createState() => _LeccionN0ScreenState();
}

class _LeccionN0ScreenState extends ConsumerState<LeccionN0Screen> {
  int indice = 0, aciertos = 0, respondidas = 0;
  bool terminado = false;

  void salir() => context.canPop() ? context.pop() : context.go('/nivel0');

  bool respondiendo = false;

  Future<void> responder(LeccionN0 l, bool ok, Widget cuerpo) async {
    // Un doble toque en COMPROBAR no debe abrir dos paneles ni saltar un paso.
    if (respondiendo) return;
    respondiendo = true;
    respondidas++;
    if (ok) aciertos++;
    ok ? Efectos.correcto() : Efectos.incorrecto();
    await mostrarPanelResultado(
      context,
      correcto: ok,
      titulo: ok ? tr('¡Muy bien!') : tr('Casi, mira cómo es'),
      cuerpo: cuerpo,
    );
    respondiendo = false;
    if (mounted) seguir(l);
  }

  void seguir(LeccionN0 l) {
    unawaited(Voz.instancia.parar());
    if (indice + 1 < l.pasos.length) {
      setState(() => indice++);
      return;
    }
    ref.read(progressProvider.notifier).registrarPractica(
      claveN0(ref.read(progressProvider).idiomaMeta, l.id),
      {
        'completa': true,
        'correcta': true,
        'aciertos': aciertos,
        'total': respondidas,
        'skill': 'lectura',
        'nivel0': true,
      },
    );
    final n = ref.read(nivel0Provider).valueOrNull;
    if (n != null &&
        siguienteN0(n, ref.read(progressProvider).practicas) == null) {
      ref.read(progressProvider.notifier).registrarPractica(
        claveN0Completo(n.idioma),
        {'correcta': true, 'skill': 'lectura'},
      );
    }
    setState(() => terminado = true);
  }

  @override
  Widget build(BuildContext context) {
    final nivel = ref.watch(nivel0Provider);
    return nivel.when(
      loading: () =>
          const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (_, _) => Scaffold(
        body: Center(child: Text(tr('No se pudo cargar la lección.'))),
      ),
      data: (n) {
        final l = n?.leccion(widget.leccionId);
        if (n == null || l == null) {
          return Scaffold(
            appBar: AppBar(),
            body: Center(child: Text(tr('Lección no encontrada.'))),
          );
        }
        _precargar(n, l);
        return Scaffold(
          appBar: AppBar(
            leading: IconButton(
              tooltip: tr('Salir'),
              icon: const Icon(Icons.close_rounded),
              onPressed: salir,
            ),
            title: terminado
                ? Text(l.titulo)
                : BarraProgreso((indice + 1) / l.pasos.length, alto: 10),
          ),
          body: Movil(
            child: terminado
                ? _Final(
                    nivel: n,
                    leccion: l,
                    aciertos: aciertos,
                    total: respondidas,
                  )
                : _paso(n, l, l.pasos[indice]),
          ),
        );
      },
    );
  }

  bool _precargado = false;

  /// Todas las imágenes de la lección se descargan al abrirla (en web cada
  /// imagen se pide al dibujarla por primera vez y aparecía con retraso).
  void _precargar(Nivel0 n, LeccionN0 l) {
    if (_precargado) return;
    _precargado = true;
    final codigos = <String>{
      for (final p in l.pasos) ...[
        for (final w in [...p.palabras, ...p.opciones]) ?w.emoji,
        if (p.sonido != null) ?n.porId[p.sonido]?.emoji,
      ],
      '1f422',
    };
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      for (final c in codigos) {
        precacheImage(AssetImage(rutaEmoji(c)), context, onError: (_, _) {});
      }
    });
  }

  Widget _paso(Nivel0 n, LeccionN0 l, PasoN0 p) {
    final k = ValueKey('${l.id}:$indice');
    void sig() => seguir(l);
    void res(bool ok, Widget cuerpo) => responder(l, ok, cuerpo);
    return switch (p.tipo) {
      'lumo' => _PasoLumo(key: k, paso: p, onSeguir: sig),
      'escucha' => _PasoEscucha(key: k, n: n, paso: p, onSeguir: sig),
      'mira' => _PasoMira(key: k, n: n, paso: p, onSeguir: sig),
      'mezcla' => _PasoMezcla(key: k, n: n, paso: p, onSeguir: sig),
      'repite' => _PasoRepite(key: k, n: n, paso: p, onSeguir: sig),
      'letras' => _PasoLetras(key: k, n: n, paso: p, onSeguir: sig),
      'escucha_elige' ||
      'toca_sonido' ||
      'elige_significado' ||
      'escucha_letra' ||
      'lee' => _PasoElegir(key: k, n: n, paso: p, onRespuesta: res),
      'deletreo' =>
        esDeletreoOrdena(p)
            ? _PasoOrdena(key: k, n: n, paso: p, onRespuesta: res)
            : _PasoElegir(key: k, n: n, paso: p, onRespuesta: res),
      'construye' => _PasoConstruye(key: k, n: n, paso: p, onRespuesta: res),
      'cambia' => _PasoCambia(key: k, n: n, paso: p, onRespuesta: res),
      _ => _PasoLumo(
        key: k,
        paso: PasoN0('lumo', {'texto': tr('Sigamos.'), 'pose': 'anima'}),
        onSeguir: sig,
      ),
    };
  }
}

/// Contenido desplazable con el botón fijo abajo (siempre a la vista).
class _Marco extends StatelessWidget {
  const _Marco({required this.children, required this.boton});
  final List<Widget> children;
  final Widget boton;

  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      Expanded(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: children,
          ),
        ),
      ),
      Padding(
        padding: EdgeInsets.fromLTRB(
          20,
          8,
          20,
          20 + MediaQuery.paddingOf(context).bottom,
        ),
        child: boton,
      ),
    ],
  );
}

Widget _titulo(String t) => Padding(
  padding: const EdgeInsets.only(bottom: 16),
  child: Text(
    t,
    style: const TextStyle(
      fontSize: 22,
      fontWeight: FontWeight.w900,
      height: 1.25,
    ),
  ),
);

/// Botones de escuchar: normal y tortuga (más lento).
class _BotonesAudio extends StatelessWidget {
  const _BotonesAudio({required this.onNormal, required this.onLento});
  final VoidCallback onNormal, onLento;

  // El tema da ancho infinito a los botones: en una fila van con Expanded.
  @override
  Widget build(BuildContext context) => Row(
    children: [
      Expanded(
        child: FilledButton.icon(
          onPressed: onNormal,
          icon: const Icon(Icons.volume_up_rounded),
          label: Text(tr('Escuchar')),
        ),
      ),
      const SizedBox(width: 10),
      Expanded(
        child: OutlinedButton.icon(
          onPressed: onLento,
          icon: const ImagenPalabra('1f422', tamano: 22),
          label: Text(tr('Lento')),
        ),
      ),
    ],
  );
}

PoseLumo _pose(String? p) => switch (p) {
  'celebra' => PoseLumo.celebra,
  'sorprendido' => PoseLumo.sorprendido,
  'pensando' => PoseLumo.pensando,
  'escucha' => PoseLumo.escucha,
  _ => PoseLumo.anima,
};

class _PasoLumo extends StatelessWidget {
  const _PasoLumo({super.key, required this.paso, required this.onSeguir});
  final PasoN0 paso;
  final VoidCallback onSeguir;

  @override
  Widget build(BuildContext context) => _Marco(
    boton: BotonPrincipal(onPressed: onSeguir, child: Text(tr('SIGUIENTE'))),
    children: [
      const SizedBox(height: 12),
      Center(child: LumoReaccion(pose: _pose(paso.pose), size: 150)),
      const SizedBox(height: 12),
      Tarjeta(
        color: OL.moradoSuave,
        sombra: false,
        child: Text(
          paso.texto,
          style: const TextStyle(
            fontSize: 19,
            height: 1.45,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    ],
  );
}

/// Tarjeta de palabra: imagen, palabra coloreada y traducción. Tocar = oír.
class _TarjetaPalabra extends StatelessWidget {
  const _TarjetaPalabra({
    required this.n,
    required this.palabra,
    this.seleccionada = false,
    this.onTap,
    this.mostrarRom = true,
  });
  final Nivel0 n;
  final Palabra palabra;
  final bool seleccionada;
  final VoidCallback? onTap;

  /// En los pasos de escucha la romanización delataría la respuesta.
  final bool mostrarRom;
  static const tamano = 30.0;

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: palabra.texto.isEmpty ? tr('Imagen') : palabra.texto,
    child: Tarjeta(
      onTap: onTap,
      borde: seleccionada ? OL.morado : null,
      color: seleccionada ? OL.moradoSuave : OL.blanco,
      padding: const EdgeInsets.all(12),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (palabra.emoji != null) ImagenPalabra(palabra.emoji, tamano: 64),
          if (palabra.marcado.isNotEmpty) ...[
            const SizedBox(height: 6),
            PalabraColor(palabra.marcado, nivel: n, tamano: tamano),
            if (mostrarRom) TextoRom(palabra.rom, alineacion: TextAlign.center),
          ],
          if (palabra.traduccion != null)
            Text(
              palabra.traduccion!,
              textAlign: TextAlign.center,
              style: const TextStyle(color: OL.gris, fontSize: 14),
            ),
        ],
      ),
    ),
  );
}

Widget _cuadricula(List<Widget> hijos) => LayoutBuilder(
  builder: (context, c) {
    final columnas = c.maxWidth > 520 ? 3 : 2;
    final ancho = (c.maxWidth - (columnas - 1) * 12) / columnas;
    return Wrap(
      spacing: 12,
      runSpacing: 12,
      alignment: WrapAlignment.center,
      children: [for (final h in hijos) SizedBox(width: ancho, child: h)],
    );
  },
);

class _PasoEscucha extends StatefulWidget {
  const _PasoEscucha({
    super.key,
    required this.n,
    required this.paso,
    required this.onSeguir,
  });
  final Nivel0 n;
  final PasoN0 paso;
  final VoidCallback onSeguir;
  @override
  State<_PasoEscucha> createState() => _PasoEscuchaState();
}

class _PasoEscuchaState extends State<_PasoEscucha> {
  final oidas = <int>{};

  @override
  void initState() {
    super.initState();
    final ps = widget.paso.palabras;
    if (ps.isNotEmpty) Future.microtask(() => tocar(0, ps.first));
  }

  void tocar(int i, Palabra p) {
    setState(() => oidas.add(i));
    decir(widget.n, p.texto);
  }

  @override
  Widget build(BuildContext context) {
    final ps = widget.paso.palabras;
    return _Marco(
      boton: BotonPrincipal(
        onPressed: oidas.isEmpty ? null : widget.onSeguir,
        child: Text(tr('SIGUIENTE')),
      ),
      children: [
        _titulo(tr('Escucha y mira')),
        _cuadricula([
          for (var i = 0; i < ps.length; i++)
            _TarjetaPalabra(
              n: widget.n,
              palabra: ps[i],
              seleccionada: oidas.contains(i),
              onTap: () => tocar(i, ps[i]),
            ),
        ]),
        const SizedBox(height: 12),
        Text(
          tr('Toca cada tarjeta para oírla.'),
          textAlign: TextAlign.center,
          style: const TextStyle(color: OL.gris),
        ),
      ],
    );
  }
}

class _PasoMira extends StatelessWidget {
  const _PasoMira({
    super.key,
    required this.n,
    required this.paso,
    required this.onSeguir,
  });
  final Nivel0 n;
  final PasoN0 paso;
  final VoidCallback onSeguir;

  @override
  Widget build(BuildContext context) {
    final sonido = paso.sonido == null ? null : n.porId[paso.sonido];
    final texto = textoPlano(paso.marcado);
    return _Marco(
      boton: BotonPrincipal(onPressed: onSeguir, child: Text(tr('SIGUIENTE'))),
      children: [
        if (sonido != null)
          Center(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
              decoration: BoxDecoration(
                color: sonido.color.withValues(alpha: .12),
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: sonido.color),
              ),
              child: Text(
                sonido.nombre,
                style: TextStyle(
                  color: sonido.color,
                  fontWeight: FontWeight.w900,
                ),
              ),
            ),
          ),
        const SizedBox(height: 16),
        if (sonido != null)
          Center(child: ImagenPalabra(sonido.emoji, tamano: 110)),
        const SizedBox(height: 8),
        PalabraColor(paso.marcado, nivel: n, tamano: 64),
        TextoRom(paso.rom, tamano: 20, alineacion: TextAlign.center),
        const SizedBox(height: 12),
        _BotonesAudio(
          onNormal: () => decir(n, texto),
          onLento: () => decir(n, texto, lento: true),
        ),
        const SizedBox(height: 16),
        Tarjeta(
          color: OL.moradoSuave,
          sombra: false,
          child: Text(
            paso.texto,
            style: const TextStyle(fontSize: 18, height: 1.45),
          ),
        ),
      ],
    );
  }
}

/// Juntar sonidos: las letras se iluminan una a una mientras suena despacio
/// y luego la palabra completa («c… a… t → cat»).
class _PasoMezcla extends StatefulWidget {
  const _PasoMezcla({
    super.key,
    required this.n,
    required this.paso,
    required this.onSeguir,
  });
  final Nivel0 n;
  final PasoN0 paso;
  final VoidCallback onSeguir;
  @override
  State<_PasoMezcla> createState() => _PasoMezclaState();
}

class _PasoMezclaState extends State<_PasoMezcla> {
  int activo = -1;
  bool listo = false;
  Timer? timer;

  late final List<Segmento> segs = segmentos(widget.paso.marcado);

  @override
  void initState() {
    super.initState();
    Future.microtask(reproducir);
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  Future<void> reproducir() async {
    timer?.cancel();
    final texto = textoPlano(widget.paso.marcado);
    setState(() => activo = 0);
    unawaited(decir(widget.n, texto, lento: true));
    timer = Timer.periodic(const Duration(milliseconds: 420), (t) {
      if (!mounted) return t.cancel();
      if (activo + 1 >= segs.length) {
        t.cancel();
        setState(() {
          activo = -1;
          listo = true;
        });
        Future.delayed(const Duration(milliseconds: 500), () {
          if (mounted) decir(widget.n, texto);
        });
        return;
      }
      setState(() => activo++);
    });
  }

  @override
  Widget build(BuildContext context) {
    final base = const TextStyle(
      fontSize: 64,
      fontWeight: FontWeight.w800,
      color: OL.texto,
      letterSpacing: 2,
    );
    return _Marco(
      boton: BotonPrincipal(
        onPressed: listo ? widget.onSeguir : null,
        child: Text(tr('SIGUIENTE')),
      ),
      children: [
        _titulo(tr('Junta los sonidos')),
        Text(
          widget.n.texto('junta'),
          style: TextStyle(color: OL.gris, fontSize: 16),
        ),
        const SizedBox(height: 24),
        Text.rich(
          TextSpan(
            children: [
              for (var i = 0; i < segs.length; i++)
                TextSpan(
                  text: segs[i].texto,
                  style: estiloSegmento(segs[i], base, widget.n).copyWith(
                    backgroundColor: i == activo ? OL.amarilloSuave : null,
                  ),
                ),
            ],
          ),
          textAlign: TextAlign.center,
        ),
        TextoRom(widget.paso.rom, tamano: 18, alineacion: TextAlign.center),
        if (widget.paso.traduccion != null)
          Text(
            widget.paso.traduccion!,
            textAlign: TextAlign.center,
            style: const TextStyle(color: OL.gris, fontSize: 16),
          ),
        const SizedBox(height: 20),
        Center(
          child: OutlinedButton.icon(
            onPressed: reproducir,
            icon: const Icon(Icons.replay_rounded),
            label: Text(tr('Otra vez')),
          ),
        ),
      ],
    );
  }
}

/// Repetir en voz alta: la IA transcribe y compara (no bloquea si falla el micrófono).
class _PasoRepite extends StatefulWidget {
  const _PasoRepite({
    super.key,
    required this.n,
    required this.paso,
    required this.onSeguir,
  });
  final Nivel0 n;
  final PasoN0 paso;
  final VoidCallback onSeguir;
  @override
  State<_PasoRepite> createState() => _PasoRepiteState();
}

class _PasoRepiteState extends State<_PasoRepite> {
  bool grabando = false, intentado = false;
  String dicho = '';
  double? parecido;
  String aviso = '';

  String get texto => textoPlano(widget.paso.marcado);

  @override
  void initState() {
    super.initState();
    Future.microtask(() => decir(widget.n, texto));
  }

  Future<void> grabar() async {
    if (grabando) {
      await Oido.instancia.parar();
      return;
    }
    setState(() {
      grabando = true;
      dicho = '';
      parecido = null;
      aviso = '';
    });
    final ok = await Oido.instancia.escuchar(
      widget.n.idioma,
      (t, fin) {
        if (!mounted) return;
        setState(() {
          dicho = t;
          if (fin) {
            grabando = false;
            intentado = true;
            parecido = similitud(t, texto);
          }
        });
      },
      segundos: 10,
      silencio: const Duration(milliseconds: 1500),
      onFin: () {
        if (mounted) setState(() => grabando = false);
      },
    );
    if (!ok && mounted) {
      setState(() {
        grabando = false;
        intentado = true;
        aviso = tr('No se pudo usar el micrófono. Dilo en voz alta y sigue.');
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final bien = (parecido ?? 0) >= .6;
    return _Marco(
      boton: BotonPrincipal(
        onPressed: widget.onSeguir,
        child: Text(intentado ? tr('SIGUIENTE') : tr('SALTAR')),
      ),
      children: [
        _titulo(tr('Escucha y repite')),
        PalabraColor(widget.paso.marcado, nivel: widget.n, tamano: 46),
        TextoRom(widget.paso.rom, tamano: 18, alineacion: TextAlign.center),
        if (widget.paso.traduccion != null)
          Text(
            widget.paso.traduccion!,
            textAlign: TextAlign.center,
            style: const TextStyle(color: OL.gris, fontSize: 16),
          ),
        const SizedBox(height: 14),
        _BotonesAudio(
          onNormal: () => decir(widget.n, texto),
          onLento: () => decir(widget.n, texto, lento: true),
        ),
        const SizedBox(height: 28),
        Center(
          child: Semantics(
            button: true,
            label: grabando ? tr('Terminar de grabar') : tr('Grabar mi voz'),
            child: InkWell(
              onTap: grabar,
              customBorder: const CircleBorder(),
              child: Container(
                width: 96,
                height: 96,
                decoration: BoxDecoration(
                  color: grabando ? OL.rojo : OL.morado,
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  grabando ? Icons.stop_rounded : Icons.mic_rounded,
                  color: OL.blanco,
                  size: 44,
                ),
              ),
            ),
          ),
        ),
        const SizedBox(height: 10),
        Text(
          grabando ? tr('Te escucho…') : tr('Toca el micrófono y dilo'),
          textAlign: TextAlign.center,
          style: const TextStyle(color: OL.gris, fontWeight: FontWeight.w700),
        ),
        if (parecido != null) ...[
          const SizedBox(height: 14),
          Tarjeta(
            color: bien ? OL.verdeSuave : OL.amarilloSuave,
            sombra: false,
            child: Text(
              bien
                  ? tr('¡Muy bien! Se entiende «{texto}».', {'texto': texto})
                  : tr(
                      'Oímos «{dicho}». Escucha otra vez y vuelve a intentarlo.',
                      {'dicho': dicho},
                    ),
              style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w700),
            ),
          ),
        ],
        if (aviso.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(top: 12),
            child: Text(aviso, textAlign: TextAlign.center),
          ),
      ],
    );
  }
}

class _PasoLetras extends StatelessWidget {
  const _PasoLetras({
    super.key,
    required this.n,
    required this.paso,
    required this.onSeguir,
  });
  final Nivel0 n;
  final PasoN0 paso;
  final VoidCallback onSeguir;

  @override
  Widget build(BuildContext context) => _Marco(
    boton: BotonPrincipal(onPressed: onSeguir, child: Text(tr('SIGUIENTE'))),
    children: [
      _titulo(tr('El nombre de las letras')),
      Wrap(
        spacing: 10,
        runSpacing: 10,
        alignment: WrapAlignment.center,
        children: [
          for (final l in paso.letras)
            Semantics(
              button: true,
              label: tr('Letra {letra}', {'letra': l}),
              child: Tarjeta(
                onTap: () => decir(n, l, letra: true),
                padding: const EdgeInsets.symmetric(
                  horizontal: 18,
                  vertical: 10,
                ),
                child: Text(
                  l,
                  style: const TextStyle(
                    fontSize: 40,
                    fontWeight: FontWeight.w900,
                    color: OL.morado,
                  ),
                ),
              ),
            ),
        ],
      ),
      const SizedBox(height: 14),
      Center(
        child: OutlinedButton.icon(
          onPressed: () => decir(n, '${paso.letras.join(', ')}.'),
          icon: const Icon(Icons.volume_up_rounded),
          label: Text(tr('Escuchar todas')),
        ),
      ),
      if ((paso.j['nota'] as String?) != null) ...[
        const SizedBox(height: 14),
        Tarjeta(
          color: OL.moradoSuave,
          sombra: false,
          child: Text(
            paso.j['nota'] as String,
            style: const TextStyle(fontSize: 17),
          ),
        ),
      ],
    ],
  );
}

/// Pasos de elegir una opción: escuchar y elegir, tocar el sonido, significado,
/// letra, deletreo y leer una frase.
class _PasoElegir extends StatefulWidget {
  const _PasoElegir({
    super.key,
    required this.n,
    required this.paso,
    required this.onRespuesta,
  });
  final Nivel0 n;
  final PasoN0 paso;
  final void Function(bool ok, Widget cuerpo) onRespuesta;
  @override
  State<_PasoElegir> createState() => _PasoElegirState();
}

class _PasoElegirState extends State<_PasoElegir> {
  int? elegida;
  late final List<int> orden = List.generate(opcionesN, (i) => i)..shuffle();

  PasoN0 get p => widget.paso;
  int get opcionesN =>
      p.tipo == 'escucha_letra' ||
          p.tipo == 'deletreo' ||
          p.tipo == 'elige_significado'
      ? p.textos.length
      : p.opciones.length;

  /// Lo que se oye en este paso.
  String get audio => switch (p.tipo) {
    'escucha_elige' => (p.j['audio'] as String?) ?? '',
    'escucha_letra' => (p.j['letra'] as String?) ?? '',
    // Formato A: se oye la palabra deletreada. Formato B con opciones
    // sueltas (sin `palabra`): se oye la palabra `m`.
    'deletreo' =>
      p.j['palabra'] is String
          ? '${(p.j['palabra'] as String).split('').join(', ')}.'
          : textoPlano(p.marcado),
    'elige_significado' || 'lee' => textoPlano(p.marcado),
    _ => '',
  };

  int get correcta => p.tipo == 'escucha_letra'
      ? p.textos.indexOf((p.j['letra'] as String?) ?? '')
      : p.correcta;

  /// Pasos de reconocer lo que se oye: la romanización de las opciones
  /// delataría la respuesta y solo aparece al corregir.
  bool get esEscucha => const {
    'escucha_elige',
    'toca_sonido',
    'escucha_letra',
    'deletreo',
  }.contains(p.tipo);

  /// Romanización de la respuesta correcta (panel de resultado).
  String? get romCorrecta => switch (p.tipo) {
    'escucha_letra' => p.letraRom ?? p.romOpcion(correcta),
    'deletreo' => p.rom,
    'elige_significado' => p.rom,
    _ =>
      correcta >= 0 && correcta < p.opciones.length
          ? p.opciones[correcta].rom
          : null,
  };

  void oir({bool lento = false}) {
    if (audio.isEmpty) return;
    decir(widget.n, audio, lento: lento, letra: p.tipo == 'escucha_letra');
  }

  @override
  void initState() {
    super.initState();
    if (p.tipo == 'escucha_elige' ||
        p.tipo == 'escucha_letra' ||
        p.tipo == 'deletreo') {
      Future.microtask(oir);
    }
  }

  Widget opcion(int i) {
    final sel = elegida == i;
    if (p.tipo == 'escucha_letra' ||
        p.tipo == 'deletreo' ||
        p.tipo == 'elige_significado') {
      final t = p.textos[i];
      return Tarjeta(
        onTap: () => setState(() => elegida = i),
        borde: sel ? OL.morado : null,
        color: sel ? OL.moradoSuave : OL.blanco,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              t,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: p.tipo == 'elige_significado' ? 20 : 34,
                fontWeight: FontWeight.w900,
                color: OL.morado,
              ),
            ),
            if (!esEscucha)
              TextoRom(p.romOpcion(i), alineacion: TextAlign.center),
          ],
        ),
      );
    }
    final o = p.opciones[i];
    return _TarjetaPalabra(
      n: widget.n,
      palabra: o,
      seleccionada: sel,
      mostrarRom: !esEscucha,
      onTap: () {
        setState(() => elegida = i);
        // Tocar el sonido: al tocar se oye la palabra (es parte de la tarea).
        if (p.tipo == 'toca_sonido' && o.texto.isNotEmpty) {
          decir(widget.n, o.texto);
        }
      },
    );
  }

  Widget cuerpo(bool ok) {
    final buena = correcta >= 0 && correcta < opcionesN
        ? (p.tipo == 'escucha_letra' ||
                  p.tipo == 'deletreo' ||
                  p.tipo == 'elige_significado'
              ? Text(
                  p.textos[correcta],
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.w900,
                  ),
                )
              : p.opciones[correcta].marcado.isEmpty
              ? ImagenPalabra(p.opciones[correcta].emoji, tamano: 56)
              : PalabraColor(
                  p.opciones[correcta].marcado,
                  nivel: widget.n,
                  tamano: 30,
                  centrar: false,
                ))
        : const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (!ok)
          Text(tr('La respuesta es:'), style: const TextStyle(fontSize: 16)),
        buena,
        TextoRom(romCorrecta, tamano: 16),
        if (p.tipo == 'lee' && p.traduccion != null)
          Text(
            '«${p.traduccion}»',
            style: const TextStyle(fontSize: 16, color: OL.gris),
          ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final sonido = p.sonido == null ? null : widget.n.porId[p.sonido];
    return _Marco(
      boton: BotonPrincipal(
        onPressed: elegida == null
            ? null
            : () => widget.onRespuesta(
                elegida == correcta,
                cuerpo(elegida == correcta),
              ),
        child: Text(tr('COMPROBAR')),
      ),
      children: [
        _titulo(p.pregunta.isEmpty ? tr('Elige') : p.pregunta),
        if (p.tipo == 'toca_sonido' && sonido != null) ...[
          Center(child: ImagenPalabra(sonido.emoji, tamano: 72)),
          Center(
            child: Text(
              sonido.nombre,
              style: TextStyle(
                color: sonido.color,
                fontSize: 18,
                fontWeight: FontWeight.w900,
              ),
            ),
          ),
          const SizedBox(height: 16),
        ],
        if (p.tipo == 'elige_significado' || p.tipo == 'lee') ...[
          _FraseTocable(n: widget.n, marcado: p.marcado),
          TextoRom(p.rom, tamano: 18, alineacion: TextAlign.center),
          const SizedBox(height: 10),
        ],
        if (audio.isNotEmpty) ...[
          _BotonesAudio(onNormal: oir, onLento: () => oir(lento: true)),
          const SizedBox(height: 18),
        ],
        _cuadricula([for (final i in orden) opcion(i)]),
      ],
    );
  }
}

/// Frase en la que cada palabra se puede tocar para oírla.
class _FraseTocable extends StatelessWidget {
  const _FraseTocable({required this.n, required this.marcado});
  final Nivel0 n;
  final String marcado;

  @override
  Widget build(BuildContext context) => Wrap(
    alignment: WrapAlignment.center,
    spacing: 10,
    runSpacing: 6,
    children: [
      for (final w in marcado.split(' '))
        InkWell(
          onTap: () =>
              decir(n, textoPlano(w).replaceAll(RegExp(r'[.,!?]'), '')),
          borderRadius: BorderRadius.circular(10),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
            child: PalabraColor(w, nivel: n, tamano: 38),
          ),
        ),
    ],
  );
}

/// Construir la palabra que oyes con fichas de letras.
class _PasoConstruye extends StatefulWidget {
  const _PasoConstruye({
    super.key,
    required this.n,
    required this.paso,
    required this.onRespuesta,
  });
  final Nivel0 n;
  final PasoN0 paso;
  final void Function(bool ok, Widget cuerpo) onRespuesta;
  @override
  State<_PasoConstruye> createState() => _PasoConstruyeState();
}

class _PasoConstruyeState extends State<_PasoConstruye> {
  final usadas = <int>[];
  late final String objetivo = textoPlano(widget.paso.marcado);
  late final List<String> fichas = () {
    final f = [...widget.paso.fichas];
    // Nunca en el orden de la respuesta.
    final r = Random(objetivo.hashCode);
    for (var i = 0; i < 6; i++) {
      f.shuffle(r);
      if (f.take(objetivo.length).join() != objetivo) break;
    }
    return f;
  }();

  @override
  void initState() {
    super.initState();
    Future.microtask(() => decir(widget.n, objetivo));
  }

  String get formada => usadas.map((i) => fichas[i]).join();

  @override
  Widget build(BuildContext context) => _Marco(
    boton: BotonPrincipal(
      onPressed: formada.length == objetivo.length
          ? () => widget.onRespuesta(
              formada.toLowerCase() == objetivo.toLowerCase(),
              // Las fichas no muestran romanización (delatarían lo que se
              // oye): solo la palabra corregida la lleva.
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  PalabraColor(
                    widget.paso.marcado,
                    nivel: widget.n,
                    tamano: 36,
                    centrar: false,
                  ),
                  TextoRom(widget.paso.rom, tamano: 16),
                ],
              ),
            )
          : null,
      child: Text(tr('COMPROBAR')),
    ),
    children: [
      _titulo(tr('Escribe la palabra que oyes')),
      _BotonesAudio(
        onNormal: () => decir(widget.n, objetivo),
        onLento: () => decir(widget.n, objetivo, lento: true),
      ),
      const SizedBox(height: 24),
      Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          for (var i = 0; i < objetivo.length; i++)
            GestureDetector(
              onTap: i < usadas.length
                  ? () => setState(() => usadas.removeAt(i))
                  : null,
              child: Container(
                width: 58,
                height: 66,
                margin: const EdgeInsets.symmetric(horizontal: 4),
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: OL.blanco,
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(
                    color: i < usadas.length ? OL.morado : OL.grisClaro,
                    width: 2,
                  ),
                ),
                child: Text(
                  i < usadas.length ? fichas[usadas[i]] : '',
                  style: const TextStyle(
                    fontSize: 34,
                    fontWeight: FontWeight.w900,
                  ),
                ),
              ),
            ),
        ],
      ),
      const SizedBox(height: 28),
      Wrap(
        alignment: WrapAlignment.center,
        spacing: 10,
        runSpacing: 10,
        children: [
          for (var i = 0; i < fichas.length; i++)
            Opacity(
              opacity: usadas.contains(i) ? .25 : 1,
              child: Tarjeta(
                onTap: usadas.contains(i) || formada.length >= objetivo.length
                    ? null
                    : () => setState(() => usadas.add(i)),
                padding: const EdgeInsets.symmetric(
                  horizontal: 18,
                  vertical: 8,
                ),
                child: Text(
                  fichas[i],
                  style: const TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.w900,
                    color: OL.morado,
                  ),
                ),
              ),
            ),
        ],
      ),
    ],
  );
}

/// Paso `deletreo` de formato B para ORDENAR: sin `palabra`, con `m` y con
/// `opciones` que son piezas sueltas (una letra, jamo o kana cada una) en el
/// orden correcto. Si alguna opción es más larga (un correo, una palabra) el
/// paso es de elegir y lo resuelve `_PasoElegir`.
bool esDeletreoOrdena(PasoN0 p) {
  if (p.tipo != 'deletreo' || p.j['palabra'] is String) return false;
  if (p.marcado.isEmpty) return false;
  final piezas = p.textos;
  return piezas.length >= 2 && piezas.every((t) => t.runes.length == 1);
}

/// Ordenar las letras de la palabra que oyes (`deletreo` formato B). La
/// respuesta es la lista `opciones` en orden; se compara pieza a pieza (vale
/// con jamo y con letras repetidas, que son intercambiables).
class _PasoOrdena extends StatefulWidget {
  const _PasoOrdena({
    super.key,
    required this.n,
    required this.paso,
    required this.onRespuesta,
  });
  final Nivel0 n;
  final PasoN0 paso;
  final void Function(bool ok, Widget cuerpo) onRespuesta;
  @override
  State<_PasoOrdena> createState() => _PasoOrdenaState();
}

class _PasoOrdenaState extends State<_PasoOrdena> {
  final usadas = <int>[];
  late final String palabra = textoPlano(widget.paso.marcado);
  late final List<String> correctas = widget.paso.textos;
  late final List<String> fichas = () {
    final f = [...correctas];
    // Nunca en el orden de la respuesta (si todas son iguales, da igual).
    final r = Random(palabra.hashCode);
    for (var i = 0; i < 30; i++) {
      f.shuffle(r);
      if (f.join('\u0000') != correctas.join('\u0000')) break;
    }
    return f;
  }();

  @override
  void initState() {
    super.initState();
    Future.microtask(() => decir(widget.n, palabra));
  }

  bool get completa => usadas.length == correctas.length;

  bool get acierto {
    for (var i = 0; i < correctas.length; i++) {
      if (fichas[usadas[i]] != correctas[i]) return false;
    }
    return true;
  }

  @override
  Widget build(BuildContext context) => _Marco(
    boton: BotonPrincipal(
      onPressed: completa
          ? () => widget.onRespuesta(
              acierto,
              // Las fichas no muestran romanización (delatarían lo que se
              // oye): solo la palabra corregida la lleva.
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  PalabraColor(
                    widget.paso.marcado,
                    nivel: widget.n,
                    tamano: 36,
                    centrar: false,
                  ),
                  TextoRom(widget.paso.rom, tamano: 16),
                ],
              ),
            )
          : null,
      child: Text(tr('COMPROBAR')),
    ),
    children: [
      _titulo(
        widget.paso.pregunta.isEmpty
            ? tr('Ordena las letras de la palabra que oyes')
            : widget.paso.pregunta,
      ),
      _BotonesAudio(
        onNormal: () => decir(widget.n, palabra),
        onLento: () => decir(widget.n, palabra, lento: true),
      ),
      const SizedBox(height: 24),
      LayoutBuilder(
        builder: (context, c) {
          final ancho = ((c.maxWidth - 8.0 * fichas.length) / fichas.length)
              .clamp(34.0, 58.0);
          return Wrap(
            alignment: WrapAlignment.center,
            spacing: 8,
            runSpacing: 8,
            children: [
              for (var i = 0; i < fichas.length; i++)
                GestureDetector(
                  key: ValueKey('hueco$i'),
                  onTap: i < usadas.length
                      ? () => setState(() => usadas.removeAt(i))
                      : null,
                  child: Container(
                    width: ancho,
                    height: 66,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      color: OL.blanco,
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(
                        color: i < usadas.length ? OL.morado : OL.grisClaro,
                        width: 2,
                      ),
                    ),
                    child: Text(
                      i < usadas.length ? fichas[usadas[i]] : '',
                      style: const TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                  ),
                ),
            ],
          );
        },
      ),
      const SizedBox(height: 28),
      Wrap(
        alignment: WrapAlignment.center,
        spacing: 10,
        runSpacing: 10,
        children: [
          for (var i = 0; i < fichas.length; i++)
            Opacity(
              opacity: usadas.contains(i) ? .25 : 1,
              child: Tarjeta(
                key: ValueKey('ficha$i'),
                onTap: usadas.contains(i) || completa
                    ? null
                    : () => setState(() => usadas.add(i)),
                padding: const EdgeInsets.symmetric(
                  horizontal: 18,
                  vertical: 8,
                ),
                child: Text(
                  fichas[i],
                  style: const TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.w900,
                    color: OL.morado,
                  ),
                ),
              ),
            ),
        ],
      ),
    ],
  );
}

/// Cambiar una letra: de «sat» a «sit». Se oye la palabra nueva y se elige
/// la letra que falta.
class _PasoCambia extends StatefulWidget {
  const _PasoCambia({
    super.key,
    required this.n,
    required this.paso,
    required this.onRespuesta,
  });
  final Nivel0 n;
  final PasoN0 paso;
  final void Function(bool ok, Widget cuerpo) onRespuesta;
  @override
  State<_PasoCambia> createState() => _PasoCambiaState();
}

class _PasoCambiaState extends State<_PasoCambia> {
  String? elegida;
  late final String de = textoPlano((widget.paso.j['de'] as String?) ?? '');
  late final String a = textoPlano((widget.paso.j['a'] as String?) ?? '');
  late final int pos = () {
    for (var i = 0; i < min(de.length, a.length); i++) {
      if (de[i] != a[i]) return i;
    }
    return 0;
  }();

  @override
  void initState() {
    super.initState();
    Future.microtask(() => decir(widget.n, a));
  }

  @override
  Widget build(BuildContext context) {
    final hueco = elegida ?? '_';
    final nueva = a.isEmpty
        ? ''
        : '${a.substring(0, pos)}$hueco${a.substring(pos + 1)}';
    return _Marco(
      boton: BotonPrincipal(
        onPressed: elegida == null
            ? null
            : () => widget.onRespuesta(
                elegida == a[pos],
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    PalabraColor(
                      (widget.paso.j['a'] as String?) ?? a,
                      nivel: widget.n,
                      tamano: 36,
                      centrar: false,
                    ),
                    TextoRom(widget.paso.aRom, tamano: 16),
                  ],
                ),
              ),
        child: Text(tr('COMPROBAR')),
      ),
      children: [
        _titulo(tr('Cambia una letra')),
        PalabraColor(
          (widget.paso.j['de'] as String?) ?? de,
          nivel: widget.n,
          tamano: 40,
        ),
        TextoRom(widget.paso.deRom, tamano: 16, alineacion: TextAlign.center),
        const Center(
          child: Icon(Icons.arrow_downward_rounded, size: 36, color: OL.gris),
        ),
        Text(
          nueva,
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontSize: 46,
            fontWeight: FontWeight.w900,
            letterSpacing: 3,
          ),
        ),
        const SizedBox(height: 10),
        _BotonesAudio(
          onNormal: () => decir(widget.n, a),
          onLento: () => decir(widget.n, a, lento: true),
        ),
        const SizedBox(height: 18),
        Text(
          tr('¿Qué letra cambia?'),
          textAlign: TextAlign.center,
          style: const TextStyle(color: OL.gris, fontWeight: FontWeight.w700),
        ),
        const SizedBox(height: 10),
        Wrap(
          alignment: WrapAlignment.center,
          spacing: 12,
          children: [
            for (final l in widget.paso.textos)
              Tarjeta(
                onTap: () => setState(() => elegida = l),
                borde: elegida == l ? OL.morado : null,
                color: elegida == l ? OL.moradoSuave : OL.blanco,
                padding: const EdgeInsets.symmetric(
                  horizontal: 22,
                  vertical: 8,
                ),
                child: Text(
                  l,
                  style: const TextStyle(
                    fontSize: 34,
                    fontWeight: FontWeight.w900,
                    color: OL.morado,
                  ),
                ),
              ),
          ],
        ),
      ],
    );
  }
}

class _Final extends ConsumerWidget {
  const _Final({
    required this.nivel,
    required this.leccion,
    required this.aciertos,
    required this.total,
  });
  final Nivel0 nivel;
  final LeccionN0 leccion;
  final int aciertos, total;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final practicas = ref.watch(progressProvider).practicas;
    final siguiente = siguienteN0(nivel, practicas);
    return _Marco(
      boton: BotonPrincipal(
        onPressed: () => siguiente == null
            ? context.go('/nivel0')
            : context.pushReplacement('/nivel0/leccion/${siguiente.id}'),
        child: Text(
          siguiente == null ? tr('VOLVER AL NIVEL 0') : tr('SIGUIENTE LECCIÓN'),
        ),
      ),
      children: [
        const SizedBox(height: 16),
        const Center(child: LumoReaccion(pose: PoseLumo.celebra, size: 170)),
        const SizedBox(height: 12),
        Text(
          tr('¡Lección completada!'),
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w900),
        ),
        const SizedBox(height: 6),
        if (total > 0)
          Text(
            tr('{aciertos} de {total} respuestas bien', {
              'aciertos': aciertos,
              'total': total,
            }),
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 18, color: OL.gris),
          ),
        const SizedBox(height: 16),
        Center(
          child: TextButton(
            onPressed: () => context.go('/nivel0'),
            child: Text(tr('Ver todas las lecciones')),
          ),
        ),
      ],
    );
  }
}
