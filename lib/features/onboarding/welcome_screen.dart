import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../app/theme.dart';
import '../../core/i18n/i18n.dart';
import '../../shared/widgets/selector_idioma_app.dart';
import '../../shared/widgets/widgets.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) => Scaffold(
    backgroundColor: OL.morado,
    body: SafeArea(
      child: Movil(
        child: LayoutBuilder(
          builder: (context, bounds) => SingleChildScrollView(
            child: ConstrainedBox(
              constraints: BoxConstraints(minHeight: bounds.maxHeight),
              child: Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 28,
                  vertical: 28,
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const Align(
                      alignment: Alignment.centerRight,
                      child: SelectorIdiomaApp(sobreColor: true),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      tr('ONE LINGO · A TU RITMO'),
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        color: OL.moradoClaro,
                        fontWeight: FontWeight.w800,
                        letterSpacing: 2,
                        fontSize: 12,
                      ),
                    ),
                    const SizedBox(height: 24),
                    TweenAnimationBuilder<double>(
                      tween: Tween(begin: 0, end: 1),
                      duration: MediaQuery.disableAnimationsOf(context)
                          ? Duration.zero
                          : const Duration(milliseconds: 600),
                      curve: Curves.easeOutCubic,
                      builder: (_, value, child) => Opacity(
                        opacity: value,
                        child: Transform.translate(
                          offset: Offset(0, (1 - value) * 18),
                          child: child,
                        ),
                      ),
                      child: SizedBox(
                        height: 190,
                        child: Stack(
                          alignment: Alignment.center,
                          children: [
                            Container(
                              width: 172,
                              height: 172,
                              decoration: BoxDecoration(
                                color: OL.blanco,
                                borderRadius: BorderRadius.circular(52),
                                boxShadow: const [
                                  BoxShadow(
                                    color: OL.moradoOscuro,
                                    offset: Offset(0, 8),
                                  ),
                                ],
                              ),
                              child: const Logo(tamano: 140),
                            ),
                            const Positioned(
                              left: 10,
                              top: 12,
                              child: _FlagBadge('en', angle: -.14),
                            ),
                            const Positioned(
                              right: 8,
                              top: 18,
                              child: _FlagBadge('fr', angle: .12),
                            ),
                            const Positioned(
                              left: 4,
                              bottom: 8,
                              child: _FlagBadge('ja', angle: .09),
                            ),
                            const Positioned(
                              right: 6,
                              bottom: 0,
                              child: _FlagBadge('es', angle: -.10),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 28),
                    Text(
                      tr('Un idioma.\nMil posibilidades.'),
                      textAlign: TextAlign.center,
                      style: Theme.of(context).textTheme.headlineLarge
                          ?.copyWith(
                            color: OL.blanco,
                            fontSize: 34,
                            height: 1.12,
                            fontWeight: FontWeight.w900,
                          ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      tr(
                        'Aprende, practica y atrévete a hablar.\nTu camino, con ayuda de la IA.',
                      ),
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        color: OL.moradoClaro,
                        fontSize: 16,
                        height: 1.5,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 24),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(
                          Icons.auto_awesome_rounded,
                          color: OL.naranja,
                          size: 20,
                        ),
                        const SizedBox(width: 8),
                        Flexible(
                          child: Text(
                            tr('Pequeños pasos. Grandes logros.'),
                            style: const TextStyle(
                              color: OL.blanco,
                              fontWeight: FontWeight.w700,
                              fontSize: 13,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 26),
                    BotonPrincipal(
                      color: OL.naranja,
                      onPressed: () => context.go('/onboarding'),
                      child: Text(tr('EMPEZAR MI CAMINO')),
                    ),
                    const SizedBox(height: 8),
                    OutlinedButton(
                      onPressed: () => context.go('/login'),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: OL.blanco,
                        side: const BorderSide(color: OL.moradoClaro, width: 2),
                      ),
                      child: Text(tr('YA TENGO CUENTA')),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    ),
  );
}

class _FlagBadge extends StatelessWidget {
  const _FlagBadge(this.code, {required this.angle});
  final String code;
  final double angle;
  @override
  Widget build(BuildContext context) => Transform.rotate(
    angle: angle,
    child: Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: OL.moradoSuave,
        borderRadius: BorderRadius.circular(16),
        boxShadow: const [
          BoxShadow(color: OL.moradoOscuro, offset: Offset(0, 4)),
        ],
      ),
      child: LanguageFlag(code, width: 43),
    ),
  );
}
