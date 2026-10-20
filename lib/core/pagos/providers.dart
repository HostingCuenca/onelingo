import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../api/pagos_api.dart';
import '../api/sync.dart';
import '../state/providers.dart';
import 'abrir_url_movil.dart'
    if (dart.library.js_interop) 'abrir_url_web.dart';
import 'modelos.dart';

export 'modelos.dart';

/// Cliente de pagos (se sustituye en las pruebas por uno con HTTP simulado).
final pagosApiProvider = Provider<PagosApi>((_) => PagosApi());

/// Abre Stripe: misma pestaña en web, navegador externo en Android.
final abrirUrlProvider = Provider<Future<bool> Function(String)>(
  (_) => abrirUrlPago,
);

/// Planes de `GET /planes`. Arranca con la última copia guardada (o los
/// planes fijos si nunca se bajaron) y se refresca con [refrescar]: al abrir
/// la app, al volver a primer plano y al abrir la pantalla de planes.
class CatalogoPlanesNotifier extends StateNotifier<CatalogoPlanes> {
  CatalogoPlanesNotifier(this._prefs, this._api) : super(_cargar(_prefs));

  static const clave = 'onelingo.planes.v1';
  final SharedPreferences _prefs;
  final PagosApi _api;

  static CatalogoPlanes _cargar(SharedPreferences p) {
    final raw = p.getString(clave);
    if (raw == null) return const CatalogoPlanes();
    try {
      return CatalogoPlanes.fromJson(
        jsonDecode(raw) as Map<String, dynamic>,
        origen: OrigenCatalogo.cache,
      );
    } catch (_) {
      return const CatalogoPlanes();
    }
  }

  Future<void> refrescar() async {
    final j = await _api.planes();
    if (j == null || !mounted) return;
    try {
      state = CatalogoPlanes.fromJson(j);
      await _prefs.setString(clave, jsonEncode(j));
    } catch (_) {
      /* Respuesta inesperada: se queda lo último bueno. */
    }
  }
}

final catalogoPlanesProvider =
    StateNotifierProvider<CatalogoPlanesNotifier, CatalogoPlanes>(
      (ref) => CatalogoPlanesNotifier(
        ref.watch(prefsProvider),
        ref.watch(pagosApiProvider),
      ),
    );

/// Suscripción del alumno según el servidor (`GET /usuarios/me/suscripcion`).
/// null para DEMO, sin sesión o si nunca se pudo bajar. Se guarda por usuario
/// para verla sin red. Se refresca al arrancar, al volver a primer plano,
/// tras iniciar sesión (cambia el correo) y al volver de pagar.
class SuscripcionNotifier extends StateNotifier<Suscripcion?> {
  SuscripcionNotifier(this._ref, this._prefs, this._api) : super(null) {
    state = _cache();
  }

  final Ref _ref;
  final SharedPreferences _prefs;
  final PagosApi _api;

  String get _clave => 'onelingo.suscripcion.${Sync.instancia.usuarioId}';
  bool get _activo => usaServidorPagos(_ref.read(progressProvider).email);

  Suscripcion? _cache() {
    if (!_activo) return null;
    final raw = _prefs.getString(_clave);
    if (raw == null) return null;
    try {
      return Suscripcion.fromJson(jsonDecode(raw) as Map<String, dynamic>);
    } catch (_) {
      return null;
    }
  }

  /// Otro usuario: se descarta lo anterior y se pide lo suyo.
  Future<void> cambioDeUsuario() {
    state = _cache();
    return refrescar();
  }

  Future<void> refrescar() async {
    if (!_activo) {
      if (state != null) state = null;
      return;
    }
    final usuario = Sync.instancia.usuarioId;
    final j = await _api.suscripcion();
    if (j == null || !mounted || usuario != Sync.instancia.usuarioId) return;
    aplicar(j);
  }

  /// Guarda una respuesta del servidor (suscripción o confirmación de pago)
  /// y deja el plan derivado en el progreso local.
  void aplicar(Map<String, dynamic> j) {
    if (!_activo) return;
    state = Suscripcion.fromJson(j);
    _prefs.setString(_clave, jsonEncode(j));
    sincronizarPlanLocal();
  }

  /// El plan local es el del idioma que se estudia: en un idioma no pagado
  /// la prueba gratuita (única para todos los idiomas) sigue contando.
  void sincronizarPlanLocal() {
    final s = state;
    if (s == null || !_activo) return;
    final progreso = _ref.read(progressProvider);
    _ref
        .read(progressProvider.notifier)
        .aplicarPlanServidor(s.planEfectivoEn(progreso.idiomaMeta));
  }
}

final suscripcionProvider =
    StateNotifierProvider<SuscripcionNotifier, Suscripcion?>((ref) {
      final n = SuscripcionNotifier(
        ref,
        ref.watch(prefsProvider),
        ref.watch(pagosApiProvider),
      );
      ref.listen(progressProvider.select((s) => s.email), (antes, ahora) {
        if (antes != ahora) n.cambioDeUsuario();
      });
      // Otro idioma meta: el plan y la prueba se evalúan en ese idioma.
      ref.listen(progressProvider.select((s) => s.idiomaMeta), (antes, ahora) {
        if (antes != ahora) n.sincronizarPlanLocal();
      });
      return n;
    });

/// Plan efectivo y prueba gratuita que ve el alumno.
final estadoPlanProvider = Provider<EstadoPlan>((ref) {
  final s = ref.watch(progressProvider);
  final catalogo = ref.watch(catalogoPlanesProvider);
  final sus = ref.watch(suscripcionProvider);
  final servidor = usaServidorPagos(s.email);
  if (servidor && sus != null) {
    final total = sus.prueba.minutos * 60;
    // El servidor toma el máximo; entre consultas el latido local sigue sumando.
    final usados = sus.prueba.segundosUsados > s.trialSegundos
        ? sus.prueba.segundosUsados
        : s.trialSegundos;
    // planId vacío o idioma no pagado: el alumno está en prueba gratuita.
    final planId = sus.planEfectivoEn(s.idiomaMeta);
    final conPlan = planId.isNotEmpty;
    final restante = conPlan ? total : (total - usados).clamp(0, total);
    return EstadoPlan(
      planId: planId,
      pruebaTotal: total,
      trialRestante: restante,
      trialAgotado: !conPlan && (sus.prueba.agotada || restante == 0),
      suscripcion: sus,
      servidor: true,
    );
  }
  final total = catalogo.pruebaSegundos;
  return EstadoPlan(
    planId: s.planId,
    pruebaTotal: total,
    trialRestante: s.trialRestanteDe(total),
    trialAgotado: s.trialAgotadoDe(total),
    servidor: servidor,
  );
});
