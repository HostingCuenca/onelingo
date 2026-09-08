import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'app/router.dart';
import 'app/theme.dart';
import 'core/api/sync.dart';
import 'core/state/providers.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  Sync.instancia.inicializar(prefs);
  runApp(
    ProviderScope(
      overrides: [prefsProvider.overrideWithValue(prefs)],
      child: const OneLingoApp(),
    ),
  );
}

class OneLingoApp extends ConsumerWidget {
  const OneLingoApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp.router(
      title: 'OneLingo',
      debugShowCheckedModeBanner: false,
      theme: buildTheme(),
      routerConfig: ref.watch(routerProvider),
      locale: const Locale('es'),
      supportedLocales: const [Locale('es'), Locale('en')],
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      builder: (context, child) => _UsoTracker(child: child!),
    );
  }
}

/// Mide el tiempo de uso real (prueba gratuita de 1 hora y tiempo de estudio):
/// cada 30 s en primer plano suma 30 s. En fase 2 este latido va al servidor.
class _UsoTracker extends ConsumerStatefulWidget {
  const _UsoTracker({required this.child});
  final Widget child;

  @override
  ConsumerState<_UsoTracker> createState() => _UsoTrackerState();
}

class _UsoTrackerState extends ConsumerState<_UsoTracker> with WidgetsBindingObserver {
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _iniciar();
  }

  void _iniciar() {
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 30), (_) {
      if (ref.read(progressProvider).onboardingDone) {
        ref.read(progressProvider.notifier).sumarSegundos(30);
      }
    });
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      _iniciar();
    } else {
      _timer?.cancel();
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => widget.child;
}
