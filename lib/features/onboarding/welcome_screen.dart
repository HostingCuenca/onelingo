import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../shared/widgets/widgets.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [OL.moradoOscuro, OL.morado],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Movil(
          child: SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 28),
              child: Column(
                children: [
                  const Spacer(),
                  Container(
                    padding: const EdgeInsets.all(18),
                    decoration: const BoxDecoration(color: OL.blanco, shape: BoxShape.circle),
                    child: const Logo(tamano: 150),
                  ),
                  const SizedBox(height: 40),
                  Text(
                    'UN IDIOMA\nTE ABRE PUERTAS.',
                    textAlign: TextAlign.center,
                    style: Theme.of(context)
                        .textTheme
                        .headlineLarge
                        ?.copyWith(color: OL.blanco, height: 1.15),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'Aprende todos.',
                    style: Theme.of(context)
                        .textTheme
                        .headlineMedium
                        ?.copyWith(color: OL.naranja),
                  ),
                  const SizedBox(height: 18),
                  const Text(
                    'OneLingo es la app todo en uno para aprender idiomas de manera '
                    'fácil, divertida y efectiva con inteligencia artificial.',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Color(0xFFD9D2FF), fontSize: 14, height: 1.5),
                  ),
                  const Spacer(),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(backgroundColor: OL.naranja),
                    onPressed: () => context.go('/onboarding'),
                    child: const Text('COMENZAR'),
                  ),
                  const SizedBox(height: 10),
                  TextButton(
                    onPressed: () => context.go('/login'),
                    child: const Text('Ya tengo cuenta · Iniciar sesión',
                        style: TextStyle(color: OL.blanco)),
                  ),
                  const SizedBox(height: 16),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
