import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../core/state/providers.dart';
import '../core/voz.dart';
import '../shared/widgets/app_navigation_icon.dart';
import '../features/library/library_screen.dart';
import '../features/ruta/ruta_screen.dart';
import '../features/ruta/unidad_screen.dart';
import '../features/library/grammar_screen.dart';
import '../features/library/learning_unit_screen.dart';
import '../features/chat/chat_screen.dart';
import '../features/avatar/avatar_screen.dart';
import '../features/situations/situation_screen.dart';
import '../features/course/level_screen.dart';
import '../features/course/levels_screen.dart';
import '../features/exam/exam_screen.dart';
import '../features/exam/program_complete_screen.dart';
import '../features/home/home_screen.dart';
import '../features/lesson/lesson_player_screen.dart';
import '../features/lesson/lesson_result_screen.dart';
import '../features/mistakes/mistakes_screen.dart';
import '../features/onboarding/login_screen.dart';
import '../features/onboarding/onboarding_screen.dart';
import '../features/onboarding/ubicacion_screen.dart';

import '../features/onboarding/welcome_screen.dart';
import '../features/plans/plans_screen.dart';
import '../features/plans/tutors_screen.dart';
import '../features/practice/practice_screen.dart';
import '../features/progress/progress_screen.dart';
import '../shared/widgets/widgets.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final onboardingDone = ref.watch(
    progressProvider.select((s) => s.onboardingDone),
  );
  return GoRouter(
    initialLocation: '/inicio',
    redirect: (context, state) {
      final enOnboarding =
          state.matchedLocation.startsWith('/bienvenida') ||
          state.matchedLocation.startsWith('/onboarding') ||
          state.matchedLocation.startsWith('/login') ||
          state.matchedLocation.startsWith('/prueba-nivel');
      if (!onboardingDone && !enOnboarding) return '/bienvenida';
      if (onboardingDone &&
          enOnboarding &&
          !state.matchedLocation.startsWith('/prueba-nivel')) {
        return '/inicio';
      }
      return null;
    },
    routes: [
      GoRoute(path: '/bienvenida', builder: (_, _) => const WelcomeScreen()),
      GoRoute(path: '/login', builder: (_, _) => const LoginScreen()),
      GoRoute(path: '/onboarding', builder: (_, _) => const OnboardingScreen()),
      StatefulShellRoute.indexedStack(
        builder: (context, state, shell) => _Shell(shell: shell),
        branches: [
          StatefulShellBranch(
            routes: [
              GoRoute(path: '/inicio', builder: (_, _) => const HomeScreen()),
              GoRoute(
                path: '/prueba-nivel',
                builder: (_, st) => PruebaNivelScreen(
                  idioma: st.uri.queryParameters['idioma'],
                  configuracion: st.extra is Map<String, dynamic>
                      ? st.extra as Map<String, dynamic>
                      : const {},
                ),
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/aprender',
                builder: (_, _) => const LevelsScreen(),
                routes: [
                  GoRoute(
                    path: 'nivel/:n',
                    builder: (_, s) =>
                        LevelScreen(nivel: int.parse(s.pathParameters['n']!)),
                  ),
                ],
              ),
              // Rutas de los demás niveles (esquema 2), p. ej. /ruta/a1-1.
              GoRoute(
                path: '/ruta/:nivel',
                builder: (_, state) =>
                    RutaScreen(nivel: state.pathParameters['nivel']!),
              ),
              // Ruta de fundamentos por idioma (esquema 2). Sustituye a la
              // pantalla foundations-v1; su progreso se lee por alias.
              GoRoute(
                path: '/fundamentos',
                builder: (_, _) => const RutaScreen(),
                routes: [
                  GoRoute(
                    path: 'unidad/:id',
                    builder: (_, state) => UnidadScreen(
                      unidadId: state.pathParameters['id']!,
                      repaso: state.uri.queryParameters['modo'] == 'repaso',
                    ),
                  ),
                ],
              ),
              GoRoute(
                path: '/estudiar',
                builder: (_, state) => LearningUnitScreen(
                  skill: state.uri.queryParameters['skill'] ?? 'comprension',
                  nivel:
                      int.tryParse(state.uri.queryParameters['nivel'] ?? '') ??
                      1,
                ),
              ),
              GoRoute(
                path: '/gramatica',
                builder: (_, state) => GrammarScreen(
                  nivel:
                      int.tryParse(state.uri.queryParameters['nivel'] ?? '') ??
                      1,
                ),
              ),
              GoRoute(
                path: '/biblioteca',
                builder: (_, st) => LibraryScreen(
                  skill: st.uri.queryParameters['skill'],
                  nivel: int.tryParse(st.uri.queryParameters['nivel'] ?? ''),
                ),
              ),
              GoRoute(
                path: '/leccion/:id',
                builder: (_, s) =>
                    LessonPlayerScreen(lessonId: s.pathParameters['id']!),
                routes: [
                  GoRoute(
                    path: 'resultado',
                    builder: (_, s) => LessonResultScreen(
                      lessonId: s.pathParameters['id']!,
                      aciertos: int.parse(
                        s.uri.queryParameters['aciertos'] ?? '0',
                      ),
                      total: int.parse(s.uri.queryParameters['total'] ?? '1'),
                    ),
                  ),
                ],
              ),
              GoRoute(
                path: '/examen/:n',
                builder: (_, s) =>
                    ExamScreen(nivel: int.parse(s.pathParameters['n']!)),
              ),
              GoRoute(
                path: '/completado',
                builder: (_, _) => const ProgramCompleteScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/practicar',
                builder: (_, _) => const PracticeScreen(),
              ),
              GoRoute(
                path: '/situacion/:id',
                builder: (_, s) => SituationScreen(
                  id: int.tryParse(s.pathParameters['id'] ?? '') ?? 0,
                  section:
                      int.tryParse(s.uri.queryParameters['seccion'] ?? '') ?? 0,
                ),
              ),
              GoRoute(
                path: '/chat',
                builder: (_, s) => ChatScreen(
                  situacionId: int.tryParse(
                    s.uri.queryParameters['situacion'] ?? '',
                  ),
                  leccionId: s.uri.queryParameters['leccion'],
                  objetivoId: s.uri.queryParameters['objetivo'],
                  modo: s.uri.queryParameters['modo'] ?? 'practica',
                ),
              ),
              // La galería de tutores es nativa (/tutores); /avatar/:id abre la
              // videollamada integrada con el tutor elegido.
              GoRoute(path: '/avatar', redirect: (_, _) => '/tutores'),
              GoRoute(
                path: '/avatar/:id',
                builder: (_, s) =>
                    AvatarScreen(tutorId: s.pathParameters['id'] ?? 'amara'),
              ),
              GoRoute(
                path: '/tutores',
                builder: (_, _) => const TutorsScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/perfil',
                builder: (_, _) => const ProgressScreen(),
              ),
              GoRoute(
                path: '/errores',
                builder: (_, _) => const MistakesScreen(),
              ),
              GoRoute(path: '/planes', builder: (_, _) => const PlansScreen()),
            ],
          ),
        ],
      ),
    ],
  );
});

class _Shell extends StatelessWidget {
  const _Shell({required this.shell});
  final StatefulNavigationShell shell;

  Future<void> _switchTab(BuildContext context, int index) async {
    await Future.wait([
      Oido.instancia.cancelar().catchError((_) {}),
      Voz.instancia.parar().catchError((_) {}),
    ]);
    if (!context.mounted) return;
    shell.goBranch(index, initialLocation: index == shell.currentIndex);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Movil(child: shell),
      bottomNavigationBar: Align(
        alignment: Alignment.bottomCenter,
        heightFactor: 1,
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 480),
          child: NavigationBar(
            selectedIndex: shell.currentIndex,
            onDestinationSelected: (i) => _switchTab(context, i),
            destinations: const [
              NavigationDestination(
                icon: AppNavigationIcon(0),
                selectedIcon: AppNavigationIcon(0, selected: true),
                label: 'Inicio',
              ),
              NavigationDestination(
                icon: AppNavigationIcon(1),
                selectedIcon: AppNavigationIcon(1, selected: true),
                label: 'Aprender',
              ),
              NavigationDestination(
                icon: AppNavigationIcon(2),
                selectedIcon: AppNavigationIcon(2, selected: true),
                label: 'Practicar',
              ),
              NavigationDestination(
                icon: AppNavigationIcon(3),
                selectedIcon: AppNavigationIcon(3, selected: true),
                label: 'Perfil',
              ),
            ],
          ),
        ),
      ),
    );
  }
}
