import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/api/sync.dart';
import '../../core/content/contenido_json.dart';
import '../../core/content/curriculum.dart';
import '../../core/diagnostico.dart';
import '../../core/efectos.dart';
import '../../core/state/providers.dart';
import '../../core/voz.dart';
import '../../shared/widgets/widgets.dart';

/// Diagnóstico adaptativo de nivel: parte del nivel declarado, mide una
/// competencia distinta en cada pregunta (elegir, completar, escuchar, dictado,
/// detectar el error, producción escrita…), sube o baja la dificultad según las
/// respuestas y termina con un perfil por competencias y un plan de refuerzo.
class DiagnosticoScreen extends ConsumerStatefulWidget {
  const DiagnosticoScreen({super.key, this.idioma});
  final String? idioma;

  /// Último resultado completo (lo lee el onboarding al volver de la prueba).
  static ResultadoDiag? ultimoResultado;
  static Map<String, dynamic>? ultimoPerfilIa;

  /// Resultado + resumen y plan de la IA (si los hubo), listo para guardar en el alumno.
  static Map<String, dynamic> diagnosticoJson(ResultadoDiag r, Map<String, dynamic>? perfil) {
    final j = r.toJson();
    if (perfil != null) {
      j['resumenIa'] = perfil['resumen'];
      j['recomendacionesIa'] = perfil['recomendaciones'];
      if ((perfil['plan'] as List?)?.isNotEmpty ?? false) j['plan'] = perfil['plan'];
    }
    return j;
  }

  @override
  ConsumerState<DiagnosticoScreen> createState() => _DiagnosticoScreenState();
}

class _DiagnosticoScreenState extends ConsumerState<DiagnosticoScreen> {
  static const _auto = [
    ('Nunca lo he estudiado', 'Empiezo desde cero: letras, sonidos y palabras', 0),
    ('Sé lo básico', 'Saludos, números, frases sueltas', 2),
    ('Me defiendo', 'Situaciones sencillas: comprar, preguntar, presentarme', 4),
    ('Converso con soltura', 'Hablo de mi vida y mi trabajo sin mucho esfuerzo', 6),
    ('Nivel avanzado', 'Debato, leo textos largos, entiendo acentos', 8),
  ];

  int? autoevaluacion;
  int declarado = 4;
  Diagnostico? diag;
  PreguntaDiag? q;
  ResultadoDiag? resultado;
  String seleccion = '';
  bool? correcto;
  EvaluacionEscritura? evaluacion;
  bool evaluando = false;
  bool reproduciendo = false;
  bool mostrarTexto = false;
  final texto = TextEditingController();
  String? idiomaAnterior;
  bool bancoListo = false;
  bool cargando = false;
  Future<PreguntaDiag?>? _prefetch;
  Map<String, dynamic>? perfilIa;
  bool perfilCargando = false;

  @override
  void initState() {
    super.initState();
    if (widget.idioma != null && widget.idioma != idiomaContenido) {
      idiomaAnterior = idiomaContenido;
      idiomaContenido = widget.idioma!;
    }
    // El banco sembrado se carga aquí: desde el registro aún no se ha precargado el idioma.
    ContenidoJson.precargar(idiomaContenido).then((_) {
      if (mounted) setState(() => bancoListo = true);
    });
  }

  /// La IA redacta la pregunta que pide el motor (nivel, competencia, tipo); null si no hay servidor.
  Future<PreguntaDiag?> _generar(PeticionDiag peticion) async {
    final st = ref.read(progressProvider);
    final r = await Sync.instancia.generarPreguntaDiag({...peticion.toJson(), 'idiomaMeta': idiomaContenido, 'idiomaNativo': st.idiomaNativo});
    if (r == null) return null;
    try {
      return PreguntaDiag.fromJson(r);
    } catch (_) {
      return null;
    }
  }

  @override
  void dispose() {
    Voz.instancia.parar();
    texto.dispose();
    if (idiomaAnterior != null) idiomaContenido = idiomaAnterior!;
    super.dispose();
  }

  void _empezar() {
    diag = Diagnostico(declarado: declarado, banco: BancoDiag.de(idiomaContenido), generador: Sync.instancia.conectado ? _generar : null);
    setState(() {});
    _siguiente();
  }

  Future<void> _siguiente() async {
    final d = diag!;
    setState(() {
      cargando = true;
      seleccion = '';
      correcto = null;
      evaluacion = null;
      mostrarTexto = false;
      texto.clear();
    });
    final p = await (_prefetch ?? d.siguienteAsync());
    _prefetch = null;
    if (!mounted) return;
    setState(() {
      cargando = false;
      q = p;
      if (p == null) resultado = d.resultado();
    });
    if (p != null && p.esAuditiva) {
      WidgetsBinding.instance.addPostFrameCallback((_) => _escuchar());
    }
    if (p == null) {
      Efectos.completado();
      _pedirPerfil();
    }
  }

  /// Resumen y plan redactados por la IA a partir del resultado numérico.
  Future<void> _pedirPerfil() async {
    final r = resultado;
    if (r == null || !Sync.instancia.conectado) return;
    setState(() => perfilCargando = true);
    final st = ref.read(progressProvider);
    final p = await Sync.instancia.perfilDiag(idiomaMeta: idiomaContenido, idiomaNativo: st.idiomaNativo, resultado: r.toJson());
    if (!mounted) return;
    setState(() {
      perfilCargando = false;
      perfilIa = p;
    });
  }

  Future<void> _escuchar() async {
    final p = q;
    if (p == null) return;
    setState(() => reproduciendo = true);
    await Voz.instancia.hablar(p.texto, idiomaContenido, velocidad: p.nivel <= 3 ? 0.4 : null);
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) setState(() => reproduciendo = false);
    });
  }

  void _comprobar() {
    final p = q!;
    final respuesta = p.conOpciones ? seleccion : texto.text.trim();
    if (respuesta.isEmpty) return;
    final ok = diag!.responder(respuesta);
    ok ? Efectos.correcto() : Efectos.incorrecto();
    setState(() {
      correcto = ok;
      mostrarTexto = true;
    });
    // Mientras el alumno lee el feedback, la IA ya prepara la siguiente pregunta.
    _prefetch = diag!.siguienteAsync();
  }

  Future<void> _enviarEscritura() async {
    final p = q!;
    final t = texto.text.trim();
    if (t.split(RegExp(r'\s+')).length < 3) return;
    setState(() => evaluando = true);
    final st = ref.read(progressProvider);
    final r = await Sync.instancia.evaluarEscritura(
      idiomaMeta: idiomaContenido, idiomaNativo: st.idiomaNativo, nivelEstimado: diag!.estimacion, consigna: p.texto, texto: t,
    );
    final e = r == null
        ? Diagnostico.evaluarLocal(t, diag!.estimacion)
        : EvaluacionEscritura(
            puntuacion: (r['puntuacion'] as num).toDouble(),
            correccion: r['correccion'] as String? ?? '',
            comentario: r['comentario'] as String? ?? '',
            errores: ((r['errores'] as List?) ?? []).cast<String>(),
          );
    diag!.registrarEscritura(t, e);
    _prefetch = diag!.siguienteAsync();
    if (!mounted) return;
    Efectos.completado();
    setState(() {
      evaluando = false;
      evaluacion = e;
      correcto = e.puntuacion >= diag!.estimacion - 0.5;
    });
  }

  Map<String, dynamic> _diagnosticoJson() => DiagnosticoScreen.diagnosticoJson(resultado!, perfilIa);

  void _terminar(int nivel) {
    final r = resultado!;
    DiagnosticoScreen.ultimoResultado = r;
    DiagnosticoScreen.ultimoPerfilIa = perfilIa;
    Sync.instancia.evento('diagnostico', {
      'nivelEstimado': r.nivel, 'cefr': r.cefr, 'nivelElegido': nivel, 'preguntas': r.preguntas,
      'precision': (r.precision * 100).round(), 'idioma': idiomaContenido, 'debilidades': r.debilidades,
    });
    final st = ref.read(progressProvider);
    if (st.onboardingDone) {
      ref.read(progressProvider.notifier).cargar(st.copyWith(nivelInicial: nivel.clamp(1, 10), fundamentos: nivel == 0, diagnostico: _diagnosticoJson()));
    }
    if (context.canPop()) {
      context.pop(nivel);
    } else {
      context.go('/inicio');
    }
  }

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context).textTheme;
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(icon: const Icon(Icons.close), onPressed: () => context.canPop() ? context.pop() : context.go('/inicio')),
        title: const Text('Diagnóstico de nivel'),
      ),
      body: Movil(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 8, 20, 20),
          child: diag == null
              ? _intro(t)
              : resultado != null
                  ? _resultado(t)
                  : _pregunta(t),
        ),
      ),
    );
  }

  // ---------------- Intro ----------------
  Widget _intro(TextTheme t) {
    final meta = idioma(idiomaContenido);
    return ListView(children: [
      Text('¿Qué nivel de ${meta.nombre} tienes?', style: t.headlineMedium),
      const SizedBox(height: 6),
      const Text(
        'No es un examen fijo: empieza en el nivel que tú indiques y va subiendo o bajando según tus respuestas. Mide comprensión, vocabulario, gramática, escucha y escritura. Entre 10 y 25 preguntas.',
        style: TextStyle(color: OL.gris, height: 1.4),
      ),
      const SizedBox(height: 16),
      for (var i = 0; i < _auto.length; i++)
        Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: Tarjeta(
            onTap: () => setState(() {
              autoevaluacion = i;
              declarado = _auto[i].$3;
              Efectos.toque();
            }),
            borde: autoevaluacion == i ? OL.morado : null,
            color: autoevaluacion == i ? OL.moradoSuave : OL.blanco,
            child: Row(children: [
              Icon(autoevaluacion == i ? Icons.radio_button_checked : Icons.radio_button_off, color: autoevaluacion == i ? OL.morado : OL.grisClaro),
              const SizedBox(width: 12),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(_auto[i].$1, style: const TextStyle(fontWeight: FontWeight.w700)),
                  Text(_auto[i].$2, style: const TextStyle(color: OL.gris, fontSize: 12)),
                ]),
              ),
            ]),
          ),
        ),
      if (autoevaluacion != null && autoevaluacion! > 0) ...[
        const SizedBox(height: 6),
        Text('Ajusta el nivel en el que crees estar: $declarado de 10', style: const TextStyle(fontWeight: FontWeight.w700)),
        Slider(value: declarado.toDouble(), min: 1, max: 10, divisions: 9, label: '$declarado', activeColor: OL.morado, onChanged: (v) => setState(() => declarado = v.round())),
        Text('La prueba empieza en el nivel $declarado y se ajusta sola. Elegir bien ahorra preguntas.', style: const TextStyle(color: OL.gris, fontSize: 12)),
      ],
      const SizedBox(height: 16),
      ElevatedButton(onPressed: autoevaluacion == null || !bancoListo ? null : _empezar, child: Text(bancoListo ? 'EMPEZAR EL DIAGNÓSTICO' : 'Preparando el banco de preguntas…')),
      const SizedBox(height: 8),
      Text(
        Sync.instancia.conectado ? 'Con conexión, la IA redacta cada pregunta a medida; sin conexión se usa el banco de la app.' : 'Sin sesión en el servidor: se usa el banco de preguntas de la app.',
        textAlign: TextAlign.center,
        style: const TextStyle(color: OL.gris, fontSize: 11),
      ),
    ]);
  }

  // ---------------- Pregunta ----------------
  Widget _pregunta(TextTheme t) {
    final d = diag!;
    final p = q;
    if (cargando || p == null) {
      return Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        const CircularProgressIndicator(),
        const SizedBox(height: 16),
        Text(d.generador != null ? 'La IA está redactando tu siguiente pregunta…' : 'Preparando la siguiente pregunta…', style: const TextStyle(color: OL.gris, fontWeight: FontWeight.w600)),
        const SizedBox(height: 6),
        Text('Dificultad ${d.nivelActual} · ${d.n} respondidas', style: const TextStyle(color: OL.gris, fontSize: 12)),
      ]);
    }
    final respondida = correcto != null || evaluacion != null;
    final progreso = ((d.n + (respondida ? 0 : 1)) / d.minPreguntas).clamp(0.0, 0.95);
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      Row(children: [
        Expanded(child: BarraProgreso(progreso, color: OL.naranja)),
        const SizedBox(width: 10),
        Etiqueta('Dificultad ${p.nivel}', color: OL.morado),
      ]),
      const SizedBox(height: 8),
      Wrap(spacing: 6, runSpacing: 6, children: [
        Etiqueta('Pregunta ${d.n + (respondida ? 0 : 1)}', color: OL.gris, fondo: OL.fondo),
        Etiqueta(skillsDiag[p.skill] ?? p.skill, color: OL.morado, fondo: OL.moradoSuave),
        Etiqueta(tiposDiagNombre[p.tipo] ?? '', color: OL.naranja, fondo: OL.naranjaSuave, icono: p.esAuditiva ? Icons.headphones : p.esEscritura ? Icons.edit_outlined : Icons.quiz_outlined),
        if (d.origenActual == 'ia') const Etiqueta('IA', color: OL.verde, fondo: OL.verdeSuave, icono: Icons.auto_awesome),
      ]),
      const SizedBox(height: 14),
      Expanded(
        child: ListView(children: [
          Text(p.instruccion, style: const TextStyle(color: OL.gris, fontSize: 12, fontWeight: FontWeight.w600)),
          const SizedBox(height: 6),
          if (p.esAuditiva) _audio(p, respondida) else _enunciado(p),
          const SizedBox(height: 14),
          if (p.conOpciones) ..._opciones(p),
          if (!p.conOpciones && !p.esEscritura) _campo(p),
          if (p.esEscritura) _escritura(p),
          if (respondida) _feedback(p),
        ]),
      ),
      const SizedBox(height: 8),
      _boton(p, respondida),
    ]);
  }

  Widget _enunciado(PreguntaDiag p) => Tarjeta(
        color: OL.moradoSuave,
        sombra: false,
        child: Text(p.texto, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w600, height: 1.45)),
      );

  Widget _audio(PreguntaDiag p, bool respondida) => Tarjeta(
        color: OL.moradoSuave,
        sombra: false,
        child: Column(children: [
          GestureDetector(
            onTap: _escuchar,
            child: AnimatedScale(
              scale: reproduciendo ? 1.08 : 1.0,
              duration: const Duration(milliseconds: 250),
              child: const IconoCuadro(Icons.volume_up_rounded, tamano: 72, radio: 36, relleno: true),
            ),
          ),
          const SizedBox(height: 10),
          Text(reproduciendo ? 'Reproduciendo…' : 'Toca para escuchar otra vez', style: const TextStyle(color: OL.gris, fontSize: 12)),
          if (mostrarTexto || respondida) ...[
            const SizedBox(height: 10),
            Text(p.texto, textAlign: TextAlign.center, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600, height: 1.4)),
          ],
        ]),
      );

  List<Widget> _opciones(PreguntaDiag p) => [
        for (final o in p.opciones)
          Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: AnimatedScale(
              scale: seleccion == o && correcto == null ? 1.03 : 1.0,
              duration: const Duration(milliseconds: 160),
              curve: Curves.easeOutBack,
              child: _Opcion(
                texto: o,
                seleccionada: seleccion == o,
                estado: correcto == null ? null : (o == p.respuestaCorrecta ? true : (seleccion == o ? false : null)),
                onTap: correcto == null
                    ? () {
                        Efectos.toque();
                        setState(() => seleccion = o);
                      }
                    : null,
              ),
            ),
          ),
      ];

  Widget _campo(PreguntaDiag p) => TextField(
        controller: texto,
        enabled: correcto == null,
        autofocus: true,
        textInputAction: TextInputAction.done,
        onChanged: (_) => setState(() {}),
        onSubmitted: (_) => _comprobar(),
        decoration: InputDecoration(
          hintText: p.tipo == TipoDiag.dictado ? 'Escribe lo que oíste' : p.tipo == TipoDiag.completar ? 'Escribe la palabra que falta' : 'Escribe tu respuesta',
          prefixIcon: const Icon(Icons.edit_outlined),
        ),
      );

  Widget _escritura(PreguntaDiag p) {
    final palabras = texto.text.trim().isEmpty ? 0 : texto.text.trim().split(RegExp(r'\s+')).length;
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      TextField(
        controller: texto,
        enabled: evaluacion == null && !evaluando,
        maxLines: 6,
        minLines: 4,
        onChanged: (_) => setState(() {}),
        decoration: const InputDecoration(hintText: 'Escribe 3-5 frases en el idioma que estás aprendiendo, sin traductor.'),
      ),
      const SizedBox(height: 6),
      Text('$palabras palabras · esta respuesta pesa más que las de opción', style: const TextStyle(color: OL.gris, fontSize: 12)),
      if (evaluando) ...[
        const SizedBox(height: 14),
        const Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2)),
          SizedBox(width: 10),
          Text('La IA está evaluando tu texto…', style: TextStyle(color: OL.morado, fontWeight: FontWeight.w600)),
        ]),
      ],
    ]);
  }

  Widget _feedback(PreguntaDiag p) {
    final e = evaluacion;
    final ok = correcto ?? false;
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0, end: 1),
      duration: const Duration(milliseconds: 380),
      curve: Curves.easeOutBack,
      builder: (_, v, child) => Opacity(opacity: v.clamp(0, 1), child: Transform.translate(offset: Offset(0, (1 - v) * 24), child: child)),
      child: Container(
        margin: const EdgeInsets.only(top: 12),
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: ok ? OL.verdeSuave : OL.rojoSuave,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: ok ? OL.verde : OL.rojo, width: 1.5),
        ),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [
            Icon(ok ? Icons.check_circle : Icons.cancel, color: ok ? OL.verde : OL.rojo),
            const SizedBox(width: 8),
            Text(
              e != null ? 'Escritura: ${e.puntuacion.toStringAsFixed(1)} de 10' : ok ? '¡Correcto!' : 'Incorrecto',
              style: TextStyle(color: ok ? OL.verde : OL.rojo, fontWeight: FontWeight.w800, fontSize: 16),
            ),
          ]),
          if (e == null && !ok && p.respuestaCorrecta.isNotEmpty) ...[
            const SizedBox(height: 6),
            Text('Respuesta correcta: ${p.respuestaCorrecta}', style: const TextStyle(fontWeight: FontWeight.w600)),
          ],
          if (e == null && p.explicacion.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text(p.explicacion, style: const TextStyle(color: OL.gris, fontSize: 13, height: 1.35)),
          ],
          if (e != null) ...[
            if (e.correccion.isNotEmpty) ...[
              const SizedBox(height: 8),
              const Text('Versión corregida', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 12)),
              Text(e.correccion, style: const TextStyle(height: 1.4)),
            ],
            if (e.comentario.isNotEmpty) ...[
              const SizedBox(height: 6),
              Text(e.comentario, style: const TextStyle(color: OL.gris, fontSize: 13, height: 1.35)),
            ],
            if (!e.porIa) const Padding(padding: EdgeInsets.only(top: 6), child: Text('Sin conexión con la IA: evaluación aproximada.', style: TextStyle(color: OL.gris, fontSize: 11))),
          ],
        ]),
      ),
    );
  }

  Widget _boton(PreguntaDiag p, bool respondida) {
    if (respondida) {
      final ok = correcto ?? false;
      return ElevatedButton(
        style: ElevatedButton.styleFrom(backgroundColor: ok ? OL.verde : OL.rojo),
        onPressed: _siguiente,
        child: const Text('SIGUIENTE'),
      );
    }
    if (p.esEscritura) {
      final palabras = texto.text.trim().isEmpty ? 0 : texto.text.trim().split(RegExp(r'\s+')).length;
      return ElevatedButton(onPressed: palabras >= 3 && !evaluando ? _enviarEscritura : null, child: const Text('ENVIAR PARA EVALUAR'));
    }
    final listo = p.conOpciones ? seleccion.isNotEmpty : texto.text.trim().isNotEmpty;
    return ElevatedButton(onPressed: listo ? _comprobar : null, child: const Text('COMPROBAR'));
  }

  List<String> _planMostrado(ResultadoDiag r) {
    final ia = (perfilIa?['plan'] as List?)?.cast<String>();
    return (ia != null && ia.isNotEmpty) ? ia : r.plan;
  }

  // ---------------- Resultado ----------------
  Widget _resultado(TextTheme t) {
    final r = resultado!;
    final n = r.recomendado;
    final nivelTexto = r.nivel == r.nivel.roundToDouble() ? r.nivel.toInt().toString() : r.nivel.toStringAsFixed(1);
    return ListView(children: [
      const SizedBox(height: 6),
      Center(
        child: AnilloProgreso(
          valor: r.nivel / 10,
          tamano: 140,
          color: OL.morado,
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            Text(nivelTexto, style: const TextStyle(fontSize: 38, fontWeight: FontWeight.w800, height: 1)),
            const Text('de 10', style: TextStyle(color: OL.gris, fontSize: 12)),
          ]),
        ),
      ),
      const SizedBox(height: 14),
      Text(n == 0 ? 'Tu punto de partida: Fundamentos' : 'Tu nivel: $nivelTexto · ${r.cefr}', textAlign: TextAlign.center, style: t.headlineMedium),
      const SizedBox(height: 4),
      Text(
        '${r.preguntas} preguntas · ${(r.precision * 100).round()} % de aciertos · confianza ${(r.confianza * 100).round()} %',
        textAlign: TextAlign.center,
        style: const TextStyle(color: OL.gris, fontSize: 13),
      ),
      const SizedBox(height: 16),
      const TituloSeccion('Por competencia'),
      const SizedBox(height: 8),
      Tarjeta(
        child: Column(children: [
          for (final e in r.skills.entries)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 5),
              child: Row(children: [
                SizedBox(width: 150, child: Text(skillsDiag[e.key] ?? e.key, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600))),
                Expanded(child: BarraProgreso(e.value / 10, color: e.value >= r.nivel + 0.5 ? OL.verde : e.value <= r.nivel - 0.5 ? OL.rojo : OL.morado)),
                const SizedBox(width: 8),
                SizedBox(width: 34, child: Text(e.value.toStringAsFixed(1), textAlign: TextAlign.right, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700))),
              ]),
            ),
        ]),
      ),
      if (r.fortalezas.isNotEmpty || r.debilidades.isNotEmpty) ...[
        const SizedBox(height: 12),
        Wrap(spacing: 6, runSpacing: 6, children: [
          for (final f in r.fortalezas) Etiqueta(f, color: OL.verde, fondo: OL.verdeSuave, icono: Icons.thumb_up_outlined),
          for (final d in r.debilidades) Etiqueta(d, color: OL.rojo, fondo: OL.rojoSuave, icono: Icons.fitness_center),
        ]),
      ],
      if (r.refuerzo.isNotEmpty) ...[
        const SizedBox(height: 16),
        const TituloSeccion('Qué reforzar'),
        const SizedBox(height: 8),
        Tarjeta(
          color: OL.moradoSuave,
          sombra: false,
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            for (final x in r.refuerzo.take(8)) Padding(padding: const EdgeInsets.only(bottom: 4), child: Text('• $x', style: const TextStyle(height: 1.35))),
            if (r.recurrentes.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 6), child: Text('Errores repetidos: ${r.recurrentes.join(', ')}', style: const TextStyle(color: OL.gris, fontSize: 12))),
          ]),
        ),
      ],
      if (perfilCargando || perfilIa != null) ...[
        const SizedBox(height: 16),
        const TituloSeccion('Lo que dice tu profesor de IA'),
        const SizedBox(height: 8),
        Tarjeta(
          child: perfilCargando
              ? const Row(children: [SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2)), SizedBox(width: 10), Text('Redactando tu resumen…', style: TextStyle(color: OL.gris))])
              : Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(perfilIa!['resumen'] as String? ?? '', style: const TextStyle(height: 1.45)),
                  const SizedBox(height: 8),
                  for (final rec in ((perfilIa!['recomendaciones'] as List?) ?? []).cast<String>())
                    Padding(padding: const EdgeInsets.only(bottom: 4), child: Text('• $rec', style: const TextStyle(fontSize: 13, height: 1.35))),
                ]),
        ),
      ],
      const SizedBox(height: 16),
      const TituloSeccion('Tu plan inicial'),
      const SizedBox(height: 8),
      Tarjeta(
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          for (var i = 0; i < _planMostrado(r).length; i++)
            Padding(
              padding: const EdgeInsets.only(bottom: 6),
              child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                CircleAvatar(radius: 11, backgroundColor: OL.morado, child: Text('${i + 1}', style: const TextStyle(color: OL.blanco, fontSize: 11, fontWeight: FontWeight.w800))),
                const SizedBox(width: 10),
                Expanded(child: Text(_planMostrado(r)[i], style: const TextStyle(height: 1.35, fontSize: 13))),
              ]),
            ),
          Text(
            n > 1
                ? 'Los niveles 1 a ${n - 1} quedan convalidados. Puedes repasarlos cuando quieras, pero tu camino empieza en el Nivel $n.'
                : n == 1
                    ? 'Empezarás desde el principio, con las bases del idioma.'
                    : 'Antes de formar frases aprenderás las letras y sus sonidos, los números, los colores y las palabras básicas.',
            style: const TextStyle(color: OL.gris, fontSize: 12, height: 1.4),
          ),
        ]),
      ),
      const SizedBox(height: 16),
      ElevatedButton(onPressed: () => _terminar(n), child: Text(n == 0 ? 'EMPEZAR POR FUNDAMENTOS' : 'EMPEZAR EN EL NIVEL $n')),
      if (n > 1) TextButton(onPressed: () => _terminar(n - 1), child: Text('Prefiero empezar un nivel más abajo (Nivel ${n - 1})')),
      if (n == 1) TextButton(onPressed: () => _terminar(0), child: const Text('Prefiero empezar por Fundamentos (letras y sonidos)')),
      if (n < 10 && n > 0 && r.declarado > n) TextButton(onPressed: () => _terminar(n + 1), child: Text('Mantener el nivel que elegí (Nivel ${(n + 1).clamp(1, 10)})')),
    ]);
  }
}

class _Opcion extends StatelessWidget {
  const _Opcion({required this.texto, required this.seleccionada, this.estado, this.onTap});
  final String texto;
  final bool seleccionada;
  final bool? estado;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final Color borde = estado == true ? OL.verde : estado == false ? OL.rojo : seleccionada ? OL.morado : OL.grisClaro;
    final Color fondo = estado == true ? OL.verdeSuave : estado == false ? OL.rojoSuave : seleccionada ? OL.moradoSuave : OL.blanco;
    return Material(
      color: fondo,
      borderRadius: BorderRadius.circular(14),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          decoration: BoxDecoration(borderRadius: BorderRadius.circular(14), border: Border.all(color: borde, width: seleccionada || estado != null ? 2 : 1.5)),
          child: Row(children: [
            Expanded(child: Text(texto, style: const TextStyle(fontWeight: FontWeight.w600, height: 1.3))),
            if (estado == true) const Icon(Icons.check_circle, color: OL.verde, size: 20),
            if (estado == false) const Icon(Icons.cancel, color: OL.rojo, size: 20),
          ]),
        ),
      ),
    );
  }
}
