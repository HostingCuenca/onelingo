import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/content/curriculum.dart';
import '../../core/content/fotos.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/widgets.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final s = ref.watch(progressProvider);
    final n = s.nivelActual;
    final lvl = nivel(n);
    final actual = s.leccionActual(n);
    final meta = idioma(s.idiomaMeta);
    final restante = s.trialRestante;

    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 24),
          children: [
            Row(children: [
              CircleAvatar(
                radius: 20,
                backgroundColor: OL.moradoClaro,
                child: Text(s.nombre.isEmpty ? 'B' : s.nombre[0].toUpperCase(),
                    style: const TextStyle(color: OL.morado, fontWeight: FontWeight.w800)),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text('¡Hola, ${s.nombre.split(' ').first}!',
                    style: Theme.of(context).textTheme.headlineSmall),
              ),
              Etiqueta('${s.racha} ${s.racha == 1 ? 'día' : 'días'}', color: const Color(0xFFB8661E), fondo: OL.naranjaSuave,
                  icono: Icons.local_fire_department_outlined),
              const SizedBox(width: 6),
              Etiqueta('${s.xp} XP', icono: Icons.bolt_outlined),
            ]),
            const SizedBox(height: 16),
            if (s.planId.isEmpty)
              Padding(
                padding: const EdgeInsets.only(bottom: 16),
                child: Tarjeta(
                  color: restante == 0 ? OL.rojoSuave : OL.amarilloSuave,
                  sombra: false,
                  onTap: () => context.push('/planes'),
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  child: Row(children: [
                    Icon(Icons.timer_outlined, color: restante == 0 ? OL.rojo : const Color(0xFF9A6B00)),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        restante == 0
                            ? 'Tu hora gratis terminó · elige un plan para continuar'
                            : 'Prueba gratuita · te quedan ${restante ~/ 60} min',
                        style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                      ),
                    ),
                    const Icon(Icons.chevron_right, color: OL.gris),
                  ]),
                ),
              ),
            const TituloSeccion('Tu camino de aprendizaje'),
            const SizedBox(height: 10),
            Tarjeta(
              child: Row(children: [
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(meta.nombre,
                        style: const TextStyle(color: OL.morado, fontSize: 20, fontWeight: FontWeight.w800)),
                    Text(n == 0 ? 'Fundamentos · empieza de cero' : 'Nivel $n · ${lvl.nombre}', style: const TextStyle(color: OL.gris, fontSize: 13)),
                    Text('${s.completadasEnNivel(n)} de ${totalLeccionesDe(n)} lecciones',
                        style: const TextStyle(color: OL.gris, fontSize: 13)),
                    const SizedBox(height: 12),
                    SizedBox(
                      width: 140,
                      height: 40,
                      child: ElevatedButton(
                        onPressed: actual == null
                            ? () => context.push('/examen/$n')
                            : () => context.push('/leccion/${actual.id}'),
                        child: Text(actual == null ? 'Examen' : 'Continuar', style: const TextStyle(fontSize: 13)),
                      ),
                    ),
                  ]),
                ),
                AnilloProgreso(
                  valor: s.progresoNivel(n),
                  tamano: 84,
                  color: OL.verde,
                  child: Text('${(s.progresoNivel(n) * 100).round()}%',
                      style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 17)),
                ),
              ]),
            ),
            const SizedBox(height: 22),
            if (s.diagnostico != null && ((s.diagnostico!['plan'] as List?) ?? []).isNotEmpty) ...[
              const TituloSeccion('Tu plan de refuerzo'),
              const SizedBox(height: 10),
              Tarjeta(
                color: OL.moradoSuave,
                sombra: false,
                onTap: () => context.push('/perfil'),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(
                    'Diagnóstico: nivel ${s.diagnostico!['nivel']} · ${s.diagnostico!['cefr']}',
                    style: const TextStyle(fontWeight: FontWeight.w700),
                  ),
                  const SizedBox(height: 6),
                  for (final linea in ((s.diagnostico!['plan'] as List).cast<String>()).take(3))
                    Padding(padding: const EdgeInsets.only(bottom: 3), child: Text('• $linea', style: const TextStyle(fontSize: 13, height: 1.35))),
                ]),
              ),
              const SizedBox(height: 18),
            ],
            const TituloSeccion('Lección diaria'),
            const SizedBox(height: 10),
            if (actual != null)
              Tarjeta(
                color: OL.moradoClaro,
                sombra: false,
                onTap: () => context.push('/leccion/${actual.id}'),
                child: Row(children: [
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Row(children: [
                        Icon(unidadesDe(n)[actual.unidad - 1].icono, size: 18, color: OL.morado),
                        const SizedBox(width: 6),
                        Text('Lección ${actual.numero}',
                            style: const TextStyle(color: OL.morado, fontWeight: FontWeight.w700, fontSize: 13)),
                      ]),
                      const SizedBox(height: 4),
                      Text(actual.titulo, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 15)),
                      Text('${actual.subtitulo} · +${actual.xp} XP',
                          style: const TextStyle(color: OL.gris, fontSize: 12)),
                    ]),
                  ),
                  const IconoCuadro(Icons.play_arrow_rounded, relleno: true, tamano: 48, radio: 24),
                ]),
              )
            else
              Tarjeta(
                color: OL.verdeSuave,
                sombra: false,
                child: const Text('Completaste las 100 lecciones del nivel. ¡Es hora del examen final!'),
              ),
            const SizedBox(height: 22),
            TituloSeccion('Práctica libre con IA', accion: 'Ver las 50', onAccion: () => context.go('/practicar')),
            const SizedBox(height: 10),
            SizedBox(
              height: 118,
              child: ListView(
                scrollDirection: Axis.horizontal,
                children: [
                  for (final sit in [situacion(1), situacion(15), situacion(33), situacion(20), situacion(50)])
                    Padding(
                      padding: const EdgeInsets.only(right: 10),
                      child: SizedBox(
                        width: 140,
                        child: Tarjeta(
                          onTap: () => context.push('/chat?situacion=${sit.id}'),
                          padding: EdgeInsets.zero,
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(16),
                            child: Stack(fit: StackFit.expand, children: [
                              if (fotoSituacion(sit.id) != null)
                                Image.asset(fotoSituacion(sit.id)!, fit: BoxFit.cover)
                              else
                                Container(color: sit.color.withValues(alpha: 0.15)),
                              Container(
                                decoration: const BoxDecoration(
                                  gradient: LinearGradient(
                                    begin: Alignment.topCenter,
                                    end: Alignment.bottomCenter,
                                    colors: [Colors.transparent, Color(0xCC000000)],
                                  ),
                                ),
                              ),
                              Positioned(left: 8, top: 8, child: IconoCuadro(sit.icono, color: sit.color, tamano: 30, relleno: true)),
                              Positioned(
                                left: 10,
                                right: 10,
                                bottom: 10,
                                child: Text(sit.nombre,
                                    maxLines: 2,
                                    overflow: TextOverflow.ellipsis,
                                    style: const TextStyle(color: OL.blanco, fontWeight: FontWeight.w700, fontSize: 13)),
                              ),
                            ]),
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: 22),
            const TituloSeccion('Actividades diarias'),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final a in actividadesDiarias)
                  Etiqueta(a.$1, color: a.$4, icono: a.$3),
              ],
            ),
            const SizedBox(height: 22),
            const TituloSeccion('Progreso general'),
            const SizedBox(height: 10),
            Row(children: [
              _Stat('${s.completadas.length}', 'LECCIONES'),
              const SizedBox(width: 10),
              _Stat('${s.vocabularioAprendido}', 'PALABRAS'),
              const SizedBox(width: 10),
              _Stat('${s.segundosEstudio ~/ 60}', 'MINUTOS'),
            ]),
            const SizedBox(height: 22),
            HeroCard(
              child: Row(children: [
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: const [
                    Text('Aprende con IA',
                        style: TextStyle(color: OL.blanco, fontSize: 20, fontWeight: FontWeight.w800)),
                    SizedBox(height: 4),
                    Text('Habla con tu tutor sobre cualquier tema.\nSe adapta a tu nivel.',
                        style: TextStyle(color: Color(0xFFE0D8FF), fontSize: 13, height: 1.4)),
                  ]),
                ),
                IconButton.filled(
                  style: IconButton.styleFrom(backgroundColor: OL.blanco, foregroundColor: OL.morado),
                  onPressed: () => context.push('/chat'),
                  icon: const Icon(Icons.smart_toy_outlined),
                ),
              ]),
            ),
          ],
        ),
      ),
    );
  }
}

class _Stat extends StatelessWidget {
  const _Stat(this.valor, this.etiqueta);
  final String valor;
  final String etiqueta;

  @override
  Widget build(BuildContext context) => Expanded(
        child: Tarjeta(
          padding: const EdgeInsets.symmetric(vertical: 14),
          child: Column(children: [
            Text(valor, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
            Text(etiqueta,
                style: const TextStyle(color: OL.gris, fontSize: 10, fontWeight: FontWeight.w700, letterSpacing: 0.5)),
          ]),
        ),
      );
}
