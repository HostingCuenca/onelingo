import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../core/state/providers.dart';
import '../features/chat/chat_screen.dart';
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
import '../features/onboarding/diagnostico_screen.dart';
import '../features/onboarding/welcome_screen.dart';
import '../features/plans/plans_screen.dart';
import '../features/plans/tutors_screen.dart';
import '../features/practice/practice_screen.dart';
import '../features/progress/progress_screen.dart';
import '../shared/widgets/widgets.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final onboardingDone = ref.watch(progressProvider.select((s) => s.onboardingDone));
  return GoRouter(
    initialLocation: '/inicio',
    redirect: (context, state) {
      final enOnboarding = state.matchedLocation.startsWith('/bienvenida') ||
          state.matchedLocation.startsWith('/onboarding') ||
          state.matchedLocation.startsWith('/login') ||
          state.matchedLocation.startsWith('/prueba-nivel');
      if (!onboardingDone && !enOnboarding) return '/bienvenida';
      if (onboardingDone && enOnboarding && !state.matchedLocation.startsWith('/prueba-nivel')) return '/inicio';
      return null;
    },
    routes: [
      GoRoute(path: '/bienvenida', builder: (_, _) => const WelcomeScreen()),
      GoRoute(path: '/login', builder: (_, _) => const LoginScreen()),
      GoRoute(path: '/onboarding', builder: (_, _) => const OnboardingScreen()),
      GoRoute(path: '/prueba-nivel', builder: (_, st) => DiagnosticoScreen(idioma: st.uri.queryParameters['idioma'])),
      StatefulShellRoute.indexedStack(
        builder: (context, state, shell) => _Shell(shell: shell),
        branches: [
          StatefulShellBranch(routes: [
            GoRoute(path: '/inicio', builder: (_, _) => const HomeScreen()),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/aprender',
              builder: (_, _) => const LevelsScreen(),
              routes: [
                GoRoute(
                  path: 'nivel/:n',
                  builder: (_, s) => LevelScreen(nivel: int.parse(s.pathParameters['n']!)),
                ),
              ],
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/practicar', builder: (_, _) => const PracticeScreen()),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/perfil', builder: (_, _) => const ProgressScreen()),
          ]),
        ],
      ),
      GoRoute(
        path: '/leccion/:id',
        builder: (_, s) => LessonPlayerScreen(lessonId: s.pathParameters['id']!),
        routes: [
          GoRoute(
            path: 'resultado',
            builder: (_, s) => LessonResultScreen(
              lessonId: s.pathParameters['id']!,
              aciertos: int.parse(s.uri.queryParameters['aciertos'] ?? '0'),
              total: int.parse(s.uri.queryParameters['total'] ?? '1'),
            ),
          ),
        ],
      ),
      GoRoute(
        path: '/examen/:n',
        builder: (_, s) => ExamScreen(nivel: int.parse(s.pathParameters['n']!)),
      ),
      GoRoute(path: '/completado', builder: (_, _) => const ProgramCompleteScreen()),
      GoRoute(
        path: '/chat',
        builder: (_, s) => ChatScreen(
          situacionId: int.tryParse(s.uri.queryParameters['situacion'] ?? ''),
          leccionId: s.uri.queryParameters['leccion'],
        ),
      ),
      GoRoute(path: '/errores', builder: (_, _) => const MistakesScreen()),
      GoRoute(path: '/planes', builder: (_, _) => const PlansScreen()),
      GoRoute(path: '/tutores', builder: (_, _) => const TutorsScreen()),
    ],
  );
});

class _Shell extends StatelessWidget {
  const _Shell({required this.shell});
  final StatefulNavigationShell shell;

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
          onDestinationSelected: (i) =>
              shell.goBranch(i, initialLocation: i == shell.currentIndex),
          destinations: const [
            NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Inicio'),
            NavigationDestination(icon: Icon(Icons.school_outlined), selectedIcon: Icon(Icons.school), label: 'Aprender'),
            NavigationDestination(icon: Icon(Icons.forum_outlined), selectedIcon: Icon(Icons.forum), label: 'Practicar'),
            NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Perfil'),
          ],
          ),
        ),
      ),
    );
  }
}
