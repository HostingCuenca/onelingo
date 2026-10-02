import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'app/router.dart';
import 'app/theme.dart';
import 'core/api/sync.dart';
import 'core/conexion.dart';
import 'core/efectos.dart';
import 'core/i18n/i18n.dart';
import 'core/voz.dart';
import 'shared/widgets/connection_banner.dart';
import 'core/state/providers.dart';
import 'shared/widgets/lumo.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  Sync.instancia.inicializar(prefs);
  Efectos.inicializar(prefs);
  await I18n.cargar();
  // Primera visita: la interfaz arranca en el idioma del dispositivo (español
  // si es español; si no, inglés). Luego se cambia en Perfil o en el registro.
  if (prefs.getString('onelingo.progress.v1') == null) {
    final dispositivo = PlatformDispatcher.instance.locale.languageCode;
    await prefs.setString(
      'onelingo.progress.v1',
      jsonEncode({'idiomaInterfaz': idiomaInterfazPara(dispositivo)}),
    );
  }
  Efectos.antesDeSonar = Voz.instancia.parar;
  unawaited(Efectos.precargar());
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
    final interfaz = ref.watch(progressProvider.select((s) => s.interfaz));
    I18n.idioma.value = interfaz;
    return MaterialApp.router(
      title: 'OneLingo',
      debugShowCheckedModeBanner: false,
      theme: buildTheme(),
      routerConfig: ref.watch(routerProvider),
      locale: Locale(interfaz),
      supportedLocales: const [Locale('es'), Locale('en')],
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      // Al cambiar el idioma de la interfaz se reconstruye todo el árbol
      // (la ubicación del router se conserva).
      builder: (context, child) => KeyedSubtree(
        key: ValueKey(interfaz),
        child: _UsoTracker(
          child: PrecargaLumo(
            child: _PrecargaEscritura(child: ConnectionBanner(child: child!)),
          ),
        ),
      ),
    );
  }
}

/// En la web, Flutter descarga la fuente de respaldo (Noto) de una escritura
/// la primera vez que la dibuja, y mientras tanto muestra cuadros vacíos.
/// Un texto invisible con signos del idioma que se estudia fuerza esa
/// descarga al abrir la app, antes de llegar a una tabla de kana o hangul.
class _PrecargaEscritura extends ConsumerWidget {
  const _PrecargaEscritura({required this.child});
  final Widget child;

  static const _muestras = {
    'ja': 'あいうアイウ日本語',
    'zh': '你好学生汉字',
    'ko': '안녕하세요 한글',
    'ru': 'Привет ёЁ',
  };

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final muestra = kIsWeb
        ? _muestras[ref.watch(progressProvider.select((s) => s.idiomaMeta))]
        : null;
    if (muestra == null) return child;
    return Stack(
      children: [
        child,
        Positioned(
          left: 0,
          top: 0,
          child: IgnorePointer(
            child: ExcludeSemantics(
              child: Opacity(
                opacity: 0,
                child: Text(muestra, style: const TextStyle(fontSize: 2)),
              ),
            ),
          ),
        ),
      ],
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

class _UsoTrackerState extends ConsumerState<_UsoTracker>
    with WidgetsBindingObserver {
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _iniciar();
    Conexion.comprobar();
  }

  void _iniciar() {
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 30), (_) {
      Conexion.comprobar();
      if (ref.read(progressProvider).onboardingDone) {
        ref.read(progressProvider.notifier).sumarSegundos(30);
      }
    });
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      Conexion.comprobar();
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
