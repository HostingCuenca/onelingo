import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/curriculum.dart';
import '../../core/models/models.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

/// Examen final del nivel: preguntas muestreadas del banco del nivel.
/// Mínimo 65 % (REQUERIMIENTOS §3). En la demo son 10 preguntas.
class ExamScreen extends ConsumerStatefulWidget {
  const ExamScreen({super.key, required this.nivel});
  final int nivel;

  @override
  ConsumerState<ExamScreen> createState() => _ExamScreenState();
}

class _ExamScreenState extends ConsumerState<ExamScreen> {
  static const totalPreguntas = 10;
  late final List<LessonStep> preguntas;
  int i = 0;
  int aciertos = 0;
  String seleccion = '';
  bool? correcto;
  bool terminado = false;
  bool empezado = false;

  @override
  void initState() {
    super.initState();
    // 1) Preguntas de examen generadas por el pipeline (una por unidad, mezcladas).
    final generadas = <LessonStep>[];
    for (final u in unidadesDe(widget.nivel)) {
      for (final q in u.examen) {
        if (q.$2.length < 2 || q.$3 < 0 || q.$3 >= q.$2.length) continue;
        generadas.add(LessonStep(
          type: StepType.multipleChoice,
          skill: Skill.gramatica,
          prompt: q.$1,
          answer: q.$2[q.$3],
          options: [...q.$2]..shuffle(),
          hint: q.$4,
        ));
      }
    }
    generadas.shuffle();
    // 2) Relleno con ejercicios de las lecciones si no hay suficientes generadas.
    final banco = <LessonStep>[];
    for (final l in leccionesDe(widget.nivel)) {
      banco.addAll(l.steps.where((s) =>
          (s.type == StepType.multipleChoice || s.type == StepType.fillBlank) && s.options.length >= 3));
    }
    banco.shuffle();
    preguntas = [...generadas.take(totalPreguntas), ...banco].take(totalPreguntas).toList();
  }

  int get pct => (aciertos * 100 / preguntas.length).round();

  void _comprobar() {
    final ok = seleccion == preguntas[i].answer;
    if (ok) aciertos++;
    setState(() => correcto = ok);
  }

  void _siguiente() {
    if (i + 1 < preguntas.length) {
      setState(() {
        i++;
        seleccion = '';
        correcto = null;
      });
    } else {
      ref.read(progressProvider.notifier).registrarExamen(widget.nivel, pct);
      setState(() => terminado = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!empezado) return _intro(context);
    if (terminado) return _resultado(context);

    final p = preguntas[i];
    return Scaffold(
      body: Movil(
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(20, 8, 20, 20),
            child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              Row(children: [
                IconButton(onPressed: () => context.pop(), icon: const Icon(Icons.close, color: OL.gris)),
                Expanded(child: BarraProgreso((i + 1) / preguntas.length, color: OL.naranja)),
                const SizedBox(width: 12),
                Text('${i + 1}/${preguntas.length}', style: const TextStyle(fontWeight: FontWeight.w700, color: OL.gris)),
              ]),
              const SizedBox(height: 14),
              Text('Examen final · Nivel ${widget.nivel}', style: const TextStyle(color: OL.gris, fontSize: 12, fontWeight: FontWeight.w600)),
              const SizedBox(height: 8),
              Text(p.type == StepType.fillBlank ? 'Completa la frase' : 'Elige la respuesta correcta',
                  style: Theme.of(context).textTheme.headlineMedium),
              const SizedBox(height: 14),
              Tarjeta(color: OL.naranjaSuave, sombra: false, child: Text(p.prompt, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w600))),
              const SizedBox(height: 14),
              for (final o in p.options)
                Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: OutlinedButton(
                    style: OutlinedButton.styleFrom(
                      alignment: Alignment.centerLeft,
                      backgroundColor: correcto == null
                          ? (seleccion == o ? OL.naranjaSuave : OL.blanco)
                          : (o == p.answer ? OL.verdeSuave : (seleccion == o ? OL.rojoSuave : OL.blanco)),
                      side: BorderSide(
                        color: correcto == null
                            ? (seleccion == o ? OL.naranja : OL.grisClaro)
                            : (o == p.answer ? OL.verde : (seleccion == o ? OL.rojo : OL.grisClaro)),
                        width: 2,
                      ),
                    ),
                    onPressed: correcto == null ? () => setState(() => seleccion = o) : null,
                    child: Text(o, style: const TextStyle(color: OL.texto)),
                  ),
                ),
              const Spacer(),
              if (correcto == null)
                ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: OL.naranja),
                  onPressed: seleccion.isEmpty ? null : _comprobar,
                  child: const Text('RESPONDER'),
                )
              else
                ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: correcto! ? OL.verde : OL.rojo),
                  onPressed: _siguiente,
                  child: Text(i + 1 < preguntas.length ? 'SIGUIENTE' : 'VER RESULTADO'),
                ),
            ]),
          ),
        ),
      ),
    );
  }

  Widget _intro(BuildContext context) => Scaffold(
        appBar: AppBar(title: Text('Examen · Nivel ${widget.nivel}')),
        body: Movil(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              HeroCard(
                gradient: OL.gradienteNaranja,
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: const [
                  Icon(Icons.workspace_premium_outlined, color: OL.blanco, size: 40),
                  SizedBox(height: 10),
                  Text('Examen final del nivel', style: TextStyle(color: OL.blanco, fontSize: 22, fontWeight: FontWeight.w800)),
                  SizedBox(height: 6),
                  Text('Demuestra lo que aprendiste en las 100 lecciones.', style: TextStyle(color: Color(0xFFFFF3E0))),
                ]),
              ),
              const SizedBox(height: 20),
              const _Regla(Icons.quiz_outlined, '$totalPreguntas preguntas mezcladas de todas las unidades'),
              const _Regla(Icons.percent, 'Necesitas 65 % o más para aprobar'),
              const _Regla(Icons.lock_open_outlined, 'Al aprobar se desbloquea el siguiente nivel automáticamente'),
              const _Regla(Icons.replay, 'Si no apruebas, repasa tus errores y vuelve a intentarlo'),
              const Spacer(),
              ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: OL.naranja),
                onPressed: preguntas.isEmpty ? null : () => setState(() => empezado = true),
                child: const Text('EMPEZAR EXAMEN'),
              ),
            ]),
          ),
        ),
      );

  Widget _resultado(BuildContext context) {
    final aprobado = pct >= Level.minimoAprobacion;
    final ultimo = widget.nivel == 10;
    return Scaffold(
      body: Movil(
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(children: [
              const Spacer(),
              AnilloProgreso(
                valor: pct / 100,
                tamano: 160,
                grosor: 12,
                color: aprobado ? OL.verde : OL.rojo,
                child: Text('$pct%', style: const TextStyle(fontSize: 36, fontWeight: FontWeight.w800)),
              ),
              const SizedBox(height: 20),
              Text(aprobado ? '¡APROBADO!' : 'NO APROBADO',
                  style: Theme.of(context).textTheme.headlineLarge?.copyWith(color: aprobado ? OL.verde : OL.rojo)),
              const SizedBox(height: 8),
              Text(
                aprobado
                    ? (ultimo ? 'Completaste el nivel máximo del programa.' : 'El Nivel ${widget.nivel + 1} ya está desbloqueado.')
                    : 'Necesitas 65 %. Repasa tus errores y vuelve a presentar el examen.',
                textAlign: TextAlign.center,
                style: const TextStyle(color: OL.gris, height: 1.5),
              ),
              const SizedBox(height: 20),
              Tarjeta(
                child: Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: [
                  _Dato('$aciertos/${preguntas.length}', 'Aciertos'),
                  _Dato('${Level.minimoAprobacion}%', 'Mínimo'),
                  _Dato(aprobado ? '+200' : '+20', 'XP'),
                ]),
              ),
              const Spacer(),
              ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: aprobado ? OL.verde : OL.morado),
                onPressed: () {
                  if (aprobado && ultimo) {
                    context.go('/completado');
                  } else if (aprobado) {
                    context.go('/aprender/nivel/${widget.nivel + 1}');
                  } else {
                    context.go('/errores');
                  }
                },
                child: Text(aprobado ? (ultimo ? 'VER MI LOGRO' : 'IR AL NIVEL ${widget.nivel + 1}') : 'REPASAR MIS ERRORES'),
              ),
              const SizedBox(height: 10),
              OutlinedButton(onPressed: () => context.go('/inicio'), child: const Text('Volver al inicio')),
            ]),
          ),
        ),
      ),
    );
  }
}

class _Regla extends StatelessWidget {
  const _Regla(this.icono, this.texto);
  final IconData icono;
  final String texto;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: Row(children: [
          IconoCuadro(icono, color: OL.naranja, tamano: 40),
          const SizedBox(width: 12),
          Expanded(child: Text(texto, style: const TextStyle(fontWeight: FontWeight.w600))),
        ]),
      );
}

class _Dato extends StatelessWidget {
  const _Dato(this.v, this.l);
  final String v, l;

  @override
  Widget build(BuildContext context) => Column(children: [
        Text(v, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800)),
        Text(l, style: const TextStyle(color: OL.gris, fontSize: 11)),
      ]);
}
