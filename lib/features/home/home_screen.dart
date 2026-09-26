import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/content/catalog.dart';
import '../../core/content/curriculum.dart';
import '../../core/content/fotos.dart';
import '../../core/state/providers.dart';
import '../../shared/widgets/daily_activities.dart';
import '../../shared/widgets/mascot_coach.dart';
import '../../shared/widgets/streak_card.dart';
import '../../shared/widgets/tutor_avatar_banner.dart';
import '../../shared/widgets/widgets.dart';
import '../library/library_screen.dart';

// Respaldo reversible de la pantalla anterior:
// docs/backups/home_screen_before_home_reorganization_2026-09-25.dart.txt
// Para restaurarla, copiar ese archivo nuevamente sobre este archivo.
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
    final nombre = nombreLimpio(s.nombre, email: s.email).split(' ').first;

    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 14, 20, 28),
          children: [
            _HomeHeader(
              nombre: nombre,
              inicial: nombre.isEmpty ? 'A' : nombre[0].toUpperCase(),
              racha: s.rachaVigente,
              xp: s.xp,
              onProfile: () => context.go('/perfil'),
            ),
            const SizedBox(height: 16),
            _LearnTodayHero(
              onTap: () {
                // Destino según idioma y progreso: la ruta de fundamentos
                // mientras esté pendiente; en inglés, el camino de Aprender.
                if (s.fundamentosPendientes) {
                  context.go('/fundamentos');
                } else if (s.idiomaMeta == 'en') {
                  context.go('/aprender');
                } else if (actual != null) {
                  context.push('/leccion/${actual.id}');
                } else {
                  context.go('/aprender');
                }
              },
            ),
            const SizedBox(height: 20),
            TituloSeccion(
              'Elige cómo aprender',
              accion: 'Ver ruta',
              onAccion: () => context.go('/aprender'),
            ),
            const SizedBox(height: 10),
            _HomeActions(
              onAcademy: () => context.go('/aprender'),
              onSituations: () => context.go('/practicar'),
              onTutor: () => context.push('/avatar'),
              onProgress: () => context.go('/perfil'),
              onDiagnostic: () => context.push(
                '/prueba-nivel',
                extra: {'idioma': s.idiomaMeta, 'nivel': s.nivelInicial},
              ),
              // La biblioteca solo tiene contenido en inglés por ahora.
              onLibrary: () => s.idiomaMeta == 'en'
                  ? context.push('/biblioteca')
                  : context.go('/aprender'),
            ),
            const SizedBox(height: 18),
            const MascotCoach(
              idle: true,
              message: 'Un pequeño paso hoy también cuenta. Elige una actividad y avancemos juntos.',
            ),
            const SizedBox(height: 4),
            const StreakCard(),
            const SizedBox(height: 16),
            if (s.planId.isEmpty) _TrialBanner(restante: restante),
            if (s.planId.isEmpty) const SizedBox(height: 16),
            if (s.idiomaMeta == 'en') const CaminoPersonalizado(),
            if (s.idiomaMeta != 'en') ...[
              const TituloSeccion('Tu camino de aprendizaje'),
              const SizedBox(height: 10),
              Tarjeta(
                child: Row(
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            meta.nombre,
                            style: const TextStyle(
                              color: OL.morado,
                              fontSize: 20,
                              fontWeight: FontWeight.w900,
                            ),
                          ),
                          Text(
                            n == 0
                                ? 'Fundamentos · empieza de cero'
                                : 'Nivel $n · ${lvl.nombre}',
                            style: const TextStyle(color: OL.gris),
                          ),
                          Text(
                            '${s.completadasEnNivel(n)} de ${totalLeccionesDe(n)} lecciones',
                            style: const TextStyle(color: OL.gris),
                          ),
                          const SizedBox(height: 12),
                          SizedBox(
                            width: 200,
                            height: 44,
                            child: ElevatedButton(
                              onPressed: actual == null
                                  ? () => context.push('/examen/$n')
                                  : () => context.push('/leccion/${actual.id}'),
                              child: Text(
                                actual == null ? 'Hacer examen' : 'Continuar',
                                style: const TextStyle(fontSize: 14),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    AnilloProgreso(
                      valor: s.progresoNivel(n),
                      tamano: 84,
                      color: OL.verde,
                      child: Text(
                        '${(s.progresoNivel(n) * 100).round()}%',
                        style: const TextStyle(
                          fontWeight: FontWeight.w900,
                          fontSize: 17,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 22),
              if (s.diagnostico != null &&
                  ((s.diagnostico!['plan'] as List?) ?? []).isNotEmpty) ...[
                const TituloSeccion('Tu plan de refuerzo'),
                const SizedBox(height: 10),
                Tarjeta(
                  color: OL.moradoSuave,
                  sombra: false,
                  onTap: () => context.go('/perfil'),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Diagnóstico orientativo: nivel ${s.diagnostico!['nivel']}',
                        style: const TextStyle(fontWeight: FontWeight.w800),
                      ),
                      const SizedBox(height: 6),
                      for (final linea
                          in ((s.diagnostico!['plan'] as List).cast<String>())
                              .take(3))
                        Padding(
                          padding: const EdgeInsets.only(bottom: 3),
                          child: Text('• $linea'),
                        ),
                    ],
                  ),
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
                  child: Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Icon(
                                  unidadesDe(n)[actual.unidad - 1].icono,
                                  size: 18,
                                  color: OL.morado,
                                ),
                                const SizedBox(width: 6),
                                Text(
                                  'Lección ${actual.numero}',
                                  style: const TextStyle(
                                    color: OL.morado,
                                    fontWeight: FontWeight.w800,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 4),
                            Text(
                              actual.titulo,
                              style: const TextStyle(
                                fontWeight: FontWeight.w800,
                              ),
                            ),
                            Text(
                              '${actual.subtitulo} · +${actual.xp} XP',
                              style: const TextStyle(color: OL.gris),
                            ),
                          ],
                        ),
                      ),
                      const IconoCuadro(
                        Icons.play_arrow_rounded,
                        relleno: true,
                        tamano: 48,
                        radio: 24,
                      ),
                    ],
                  ),
                )
              else
                const Tarjeta(
                  color: OL.verdeSuave,
                  sombra: false,
                  child: Text(
                    'Completaste las 100 lecciones del nivel. ¡Es hora del examen final!',
                  ),
                ),
              const SizedBox(height: 22),
            ],
            const TutorAvatarBanner(),
            const SizedBox(height: 22),
            TituloSeccion(
              'Situaciones de la vida real',
              accion: 'Ver las 50',
              onAccion: () => context.go('/practicar'),
            ),
            const SizedBox(height: 10),
            const _SituationPreview(),
            const SizedBox(height: 22),
            const TituloSeccion('Actividades diarias'),
            const SizedBox(height: 10),
            const DailyActivities(),
            const SizedBox(height: 22),
            const TituloSeccion('Tu progreso en números'),
            const SizedBox(height: 10),
            Row(
              children: [
                _Stat(
                  '${s.idiomaMeta == 'en' ? s.practicas.length : s.completadas.length}',
                  s.idiomaMeta == 'en' ? 'ACTIVIDADES' : 'LECCIONES',
                ),
                const SizedBox(width: 10),
                _Stat(
                  '${s.idiomaMeta == 'en' ? s.practicas.values.whereType<Map>().where((e) => e['correcta'] == true).length : s.vocabularioAprendido}',
                  s.idiomaMeta == 'en' ? 'RESUELTAS' : 'PALABRAS',
                ),
                const SizedBox(width: 10),
                _Stat('${s.segundosEstudio ~/ 60}', 'MINUTOS'),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _TrialBanner extends StatelessWidget {
  const _TrialBanner({required this.restante});
  final int restante;

  @override
  Widget build(BuildContext context) => Tarjeta(
    color: restante == 0 ? OL.rojoSuave : OL.amarilloSuave,
    sombra: false,
    onTap: () => context.push('/planes'),
    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
    child: Row(
      children: [
        Icon(
          Icons.timer_outlined,
          color: restante == 0 ? OL.rojo : const Color(0xFF9A6B00),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Text(
            restante == 0
                ? 'Tu hora gratis terminó · elige un plan para continuar'
                : 'Prueba gratuita · te quedan ${restante ~/ 60} min',
            style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14),
          ),
        ),
        const Icon(Icons.chevron_right_rounded, color: OL.gris),
      ],
    ),
  );
}

class _HomeHeader extends StatelessWidget {
  const _HomeHeader({
    required this.nombre,
    required this.inicial,
    required this.racha,
    required this.xp,
    required this.onProfile,
  });

  final String nombre;
  final String inicial;
  final int racha;
  final int xp;
  final VoidCallback onProfile;

  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Row(
        children: [
          const Expanded(child: _OneLingoWordmark()),
          Semantics(
            button: true,
            label: 'Abrir perfil de $nombre',
            child: InkWell(
              onTap: onProfile,
              customBorder: const CircleBorder(),
              child: CircleAvatar(
                radius: 23,
                backgroundColor: OL.moradoClaro,
                child: Text(
                  inicial,
                  style: const TextStyle(
                    color: OL.morado,
                    fontSize: 18,
                    fontWeight: FontWeight.w900,
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
      const SizedBox(height: 10),
      Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Hola, $nombre',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const Text(
                  '¿Qué quieres aprender hoy?',
                  style: TextStyle(color: OL.gris, fontWeight: FontWeight.w700),
                ),
              ],
            ),
          ),
          const SizedBox(width: 8),
          Etiqueta(
            '$racha',
            color: const Color(0xFFB8661E),
            fondo: OL.naranjaSuave,
            icono: Icons.local_fire_department_rounded,
          ),
          const SizedBox(width: 6),
          Etiqueta('$xp XP', icono: Icons.bolt_rounded),
        ],
      ),
    ],
  );
}

class _OneLingoWordmark extends StatelessWidget {
  const _OneLingoWordmark();

  @override
  Widget build(BuildContext context) => Semantics(
    header: true,
    label: 'OneLingo. Un mundo, más oportunidades.',
    child: Align(
      alignment: Alignment.centerLeft,
      child: Image.asset(
        'assets/img/logo-oficial-transparente.png',
        width: 92,
        height: 76,
        fit: BoxFit.contain,
        alignment: Alignment.centerLeft,
        excludeFromSemantics: true,
      ),
    ),
  );
}

class _LearnTodayHero extends StatelessWidget {
  const _LearnTodayHero({required this.onTap});
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: 'Aprende hoy para crear un mejor mañana. Continuar aprendiendo.',
    child: Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(24),
        child: Ink(
          height: 188,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(24),
            border: Border.all(color: const Color(0xFFD7E8F6), width: 2),
            boxShadow: const [
              BoxShadow(
                color: Color(0x1F2E78D1),
                blurRadius: 18,
                offset: Offset(0, 6),
              ),
            ],
            image: const DecorationImage(
              image: AssetImage('assets/img/home-aprende-hoy.webp'),
              fit: BoxFit.cover,
            ),
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(22),
            child: Stack(
              fit: StackFit.expand,
              children: [
                const DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.centerLeft,
                      end: Alignment.centerRight,
                      stops: [0, .38, .74, 1],
                      colors: [
                        Color(0xFFFDF8F0),
                        Color(0xF5FDF8F0),
                        Color(0x69FDF8F0),
                        Color(0x00FDF8F0),
                      ],
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 18, 154, 16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Aprende hoy',
                        style: TextStyle(
                          fontSize: 25,
                          height: 1.02,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const Text(
                        'un mejor mañana',
                        style: TextStyle(
                          color: OL.morado,
                          fontSize: 24,
                          height: 1.08,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const Spacer(),
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 8,
                        ),
                        decoration: BoxDecoration(
                          color: OL.blanco.withValues(alpha: .88),
                          borderRadius: BorderRadius.circular(99),
                        ),
                        child: const Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              'CONTINUAR',
                              style: TextStyle(
                                color: OL.morado,
                                fontSize: 12,
                                fontWeight: FontWeight.w900,
                                letterSpacing: .45,
                              ),
                            ),
                            SizedBox(width: 4),
                            Icon(
                              Icons.arrow_forward_rounded,
                              color: OL.morado,
                              size: 17,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    ),
  );
}

class _HomeActions extends StatelessWidget {
  const _HomeActions({
    required this.onAcademy,
    required this.onSituations,
    required this.onTutor,
    required this.onProgress,
    required this.onDiagnostic,
    required this.onLibrary,
  });

  final VoidCallback onAcademy;
  final VoidCallback onSituations;
  final VoidCallback onTutor;
  final VoidCallback onProgress;
  final VoidCallback onDiagnostic;
  final VoidCallback onLibrary;

  @override
  Widget build(BuildContext context) => LayoutBuilder(
    builder: (context, constraints) => GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      mainAxisSpacing: 12,
      crossAxisSpacing: 12,
      childAspectRatio: constraints.maxWidth < 360 ? 1.18 : 1.36,
      children: [
        _HomeActionCard(
          asset: 'assets/img/home-icons/home-academia.webp',
          title: 'Academia',
          subtitle: 'Cursos por niveles',
          color: OL.azul,
          softColor: OL.azulSuave,
          onTap: onAcademy,
        ),
        _HomeActionCard(
          asset: 'assets/img/home-icons/home-situaciones.webp',
          title: '50 situaciones',
          subtitle: 'Inglés para la vida real',
          color: OL.verde,
          softColor: OL.verdeSuave,
          onTap: onSituations,
        ),
        _HomeActionCard(
          asset: 'assets/img/home-icons/home-tutor-ia.webp',
          title: 'Tutor con IA',
          subtitle: 'Conversa con un avatar',
          color: OL.morado,
          softColor: OL.moradoSuave,
          onTap: onTutor,
        ),
        _HomeActionCard(
          asset: 'assets/img/home-icons/home-progreso.webp',
          title: 'Progreso',
          subtitle: 'Avance, racha y logros',
          color: OL.naranja,
          softColor: OL.naranjaSuave,
          onTap: onProgress,
        ),
        _HomeActionCard(
          asset: 'assets/img/home-icons/home-diagnostico.webp',
          title: 'Diagnóstico',
          subtitle: 'Descubre qué reforzar',
          color: OL.rojo,
          softColor: OL.rojoSuave,
          onTap: onDiagnostic,
        ),
        _HomeActionCard(
          asset: 'assets/img/home-icons/home-biblioteca.webp',
          title: 'Biblioteca',
          subtitle: 'Lectura, audio y práctica',
          color: const Color(0xFF0799A8),
          softColor: const Color(0xFFDDF5F6),
          onTap: onLibrary,
        ),
      ],
    ),
  );
}

class _HomeActionCard extends StatelessWidget {
  const _HomeActionCard({
    required this.asset,
    required this.title,
    required this.subtitle,
    required this.color,
    required this.softColor,
    required this.onTap,
  });

  final String asset;
  final String title;
  final String subtitle;
  final Color color;
  final Color softColor;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Semantics(
    button: true,
    label: '$title. $subtitle',
    child: Tarjeta(
      onTap: onTap,
      color: softColor,
      borde: color.withValues(alpha: .24),
      padding: const EdgeInsets.all(14),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              SizedBox(
                width: 54,
                height: 54,
                child: Image.asset(
                  asset,
                  fit: BoxFit.contain,
                  excludeFromSemantics: true,
                  filterQuality: FilterQuality.medium,
                ),
              ),
              const Spacer(),
              Container(
                width: 30,
                height: 30,
                decoration: BoxDecoration(
                  color: OL.blanco.withValues(alpha: .72),
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  Icons.arrow_forward_rounded,
                  color: color,
                  size: 18,
                ),
              ),
            ],
          ),
          const Spacer(),
          Text(
            title,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(
              fontSize: 17,
              height: 1.05,
              fontWeight: FontWeight.w900,
            ),
          ),
          const SizedBox(height: 5),
          Text(
            subtitle,
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(
              color: OL.gris,
              fontSize: 13,
              height: 1.2,
              fontWeight: FontWeight.w700,
            ),
          ),
        ],
      ),
    ),
  );
}

class _SituationPreview extends StatelessWidget {
  const _SituationPreview();

  @override
  Widget build(BuildContext context) => SizedBox(
    height: 194,
    child: ListView(
      scrollDirection: Axis.horizontal,
      children: [
        for (final sit in [
          situacion(1),
          situacion(15),
          situacion(33),
          situacion(20),
          situacion(50),
        ])
          Padding(
            padding: const EdgeInsets.only(right: 12, bottom: 4),
            child: SizedBox(
              width: 200,
              child: Tarjeta(
                onTap: () => context.push('/situacion/${sit.id}'),
                padding: EdgeInsets.zero,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(20),
                  child: Stack(
                    fit: StackFit.expand,
                    children: [
                      if (fotoSituacion(sit.id) != null)
                        Image.asset(fotoSituacion(sit.id)!, fit: BoxFit.cover)
                      else
                        ColoredBox(color: sit.color.withValues(alpha: .15)),
                      const DecoratedBox(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            begin: Alignment.topCenter,
                            end: Alignment.bottomCenter,
                            colors: [Colors.transparent, Color(0xD9000000)],
                          ),
                        ),
                      ),
                      Positioned(
                        left: 10,
                        top: 10,
                        child: IconoCuadro(
                          sit.icono,
                          color: sit.color,
                          tamano: 34,
                          relleno: true,
                        ),
                      ),
                      Positioned(
                        left: 12,
                        right: 12,
                        bottom: 12,
                        child: Text(
                          sit.nombre,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                            color: OL.blanco,
                            fontWeight: FontWeight.w900,
                            fontSize: 16,
                            height: 1.15,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
      ],
    ),
  );
}

class _Stat extends StatelessWidget {
  const _Stat(this.valor, this.etiqueta);
  final String valor;
  final String etiqueta;

  @override
  Widget build(BuildContext context) => Expanded(
    child: Tarjeta(
      padding: const EdgeInsets.symmetric(vertical: 14),
      child: Column(
        children: [
          Text(
            valor,
            style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900),
          ),
          Text(
            etiqueta,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(
              color: OL.gris,
              fontSize: 11,
              fontWeight: FontWeight.w800,
              letterSpacing: .25,
            ),
          ),
        ],
      ),
    ),
  );
}
