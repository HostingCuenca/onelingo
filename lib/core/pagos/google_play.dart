import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:in_app_purchase/in_app_purchase.dart';
import 'package:in_app_purchase_android/billing_client_wrappers.dart' show ReplacementMode;
import 'package:in_app_purchase_android/in_app_purchase_android.dart';
import 'package:intl/intl.dart' show NumberFormat;
import 'package:shared_preferences/shared_preferences.dart';

import '../api/pagos_api.dart';
import '../api/sync.dart';
import '../i18n/i18n.dart';
import '../state/providers.dart';
import 'providers.dart';

/// Cobro dentro de la app Android con Google Play Billing. La app abre la
/// compra de Google y manda el token a `POST /pagos/google/verificar`; solo si
/// el servidor la acepta se completa (si nadie la reconoce en 3 días, Google
/// la reembolsa). En la web se sigue pagando con Stripe.
///
/// Ids en Play Console: producto `plan_<id>` (lo manda `GET /planes`) y un
/// plan base por duración (`mes-1`, `mes-3`, `mes-6`, `mes-12`).

/// Precio de un plan base en Google Play, en la moneda del alumno.
class PrecioPlay {
  const PrecioPlay({required this.texto, required this.valor, required this.moneda});

  /// «US$20.00», «€18,99»… tal como lo formatea Google.
  final String texto;
  final double valor;
  final String moneda;

  /// Precio equivalente por mes, con el símbolo de su moneda.
  String porMes(int meses) => NumberFormat.simpleCurrency(name: moneda.toUpperCase()).format(valor / meses);
}

enum EstadoCompraPlay { comprada, pendiente, cancelada, error }

/// Una compra que entrega Google Play (nueva, restaurada, pendiente o fallida).
class CompraPlay {
  const CompraPlay({required this.estado, this.token = '', this.producto = '', this.error, this.original});
  final EstadoCompraPlay estado;
  final String token;
  final String producto;
  final String? error;

  /// `PurchaseDetails` del plugin (para completarla).
  final Object? original;
}

/// Acceso a Google Play Billing: el real en Android; uno simulado en pruebas.
abstract class TiendaPlay {
  /// Compras nuevas o actualizadas (el plugin las entrega aquí, no en [comprar]).
  Stream<List<CompraPlay>> get compras;
  Future<bool> disponible();

  /// Precios de los planes base de [productos], con clave «producto|planBase».
  Future<Map<String, PrecioPlay>> precios(Set<String> productos);

  /// Abre la compra de Google. [productoAnterior]: suscripción de Play que se
  /// reemplaza (cambio de plan o de duración). false si no se pudo abrir.
  Future<bool> comprar({required String producto, required String planBase, required String cuenta, String? productoAnterior});

  /// Compras que Google ya cobró y aún no se completaron (p. ej. si la app se
  /// cerró antes de verificarlas).
  Future<List<CompraPlay>> sinCompletar();
  Future<void> completar(CompraPlay c);
}

class TiendaPlayReal implements TiendaPlay {
  InAppPurchase get _iap => InAppPurchase.instance;
  final _detalles = <String, GooglePlayProductDetails>{};

  static CompraPlay _desde(PurchaseDetails p) => CompraPlay(
    estado: switch (p.status) {
      PurchaseStatus.purchased || PurchaseStatus.restored => EstadoCompraPlay.comprada,
      PurchaseStatus.pending => EstadoCompraPlay.pendiente,
      PurchaseStatus.canceled => EstadoCompraPlay.cancelada,
      PurchaseStatus.error => EstadoCompraPlay.error,
    },
    token: p.verificationData.serverVerificationData,
    producto: p.productID,
    error: p.error?.message,
    original: p,
  );

  @override
  Stream<List<CompraPlay>> get compras => _iap.purchaseStream.map((l) => [for (final p in l) _desde(p)]);

  @override
  Future<bool> disponible() => _iap.isAvailable();

  @override
  Future<Map<String, PrecioPlay>> precios(Set<String> productos) async {
    final r = await _iap.queryProductDetails(productos);
    final m = <String, PrecioPlay>{};
    for (final d in r.productDetails.whereType<GooglePlayProductDetails>()) {
      final i = d.subscriptionIndex;
      final ofertas = d.productDetails.subscriptionOfferDetails;
      if (i == null || ofertas == null) continue;
      // Solo el plan base (sin ofertas de prueba o descuento).
      if (ofertas[i].offerId != null) continue;
      final clave = '${d.id}|${ofertas[i].basePlanId}';
      _detalles[clave] = d;
      m[clave] = PrecioPlay(texto: d.price, valor: d.rawPrice, moneda: d.currencyCode);
    }
    return m;
  }

  @override
  Future<bool> comprar({required String producto, required String planBase, required String cuenta, String? productoAnterior}) async {
    final clave = '$producto|$planBase';
    if (!_detalles.containsKey(clave)) await precios({producto});
    final d = _detalles[clave];
    if (d == null) return false;
    ChangeSubscriptionParam? cambio;
    if (productoAnterior != null) {
      final r = await _iap.getPlatformAddition<InAppPurchaseAndroidPlatformAddition>().queryPastPurchases();
      final viejo = r.pastPurchases.where((p) => p.productID == productoAnterior).firstOrNull;
      if (viejo != null) {
        cambio = ChangeSubscriptionParam(oldPurchaseDetails: viejo, replacementMode: ReplacementMode.withTimeProration);
      }
    }
    return _iap.buyNonConsumable(
      purchaseParam: GooglePlayPurchaseParam(
        productDetails: d,
        applicationUserName: cuenta,
        offerToken: d.offerToken,
        changeSubscriptionParam: cambio,
      ),
    );
  }

  @override
  Future<List<CompraPlay>> sinCompletar() async {
    final r = await _iap.getPlatformAddition<InAppPurchaseAndroidPlatformAddition>().queryPastPurchases();
    return [
      for (final p in r.pastPurchases)
        if (!p.billingClientPurchase.isAcknowledged) _desde(p),
    ];
  }

  @override
  Future<void> completar(CompraPlay c) async {
    final p = c.original;
    if (p is PurchaseDetails && p.pendingCompletePurchase) await _iap.completePurchase(p);
  }
}

/// ¿Esta plataforma cobra con Google Play? Android sí; la web usa Stripe.
final pagoEnAppProvider = Provider<bool>((_) => !kIsWeb && defaultTargetPlatform == TargetPlatform.android);

final tiendaPlayProvider = Provider<TiendaPlay>((_) => TiendaPlayReal());

/// Precios de Google Play de todos los planes («producto|planBase»). Vacío sin
/// Play o si falla: entonces se ven los precios del catálogo.
final preciosPlayProvider = FutureProvider<Map<String, PrecioPlay>>((ref) async {
  if (!ref.watch(pagoEnAppProvider)) return const {};
  final catalogo = ref.watch(catalogoPlanesProvider);
  final productos = {
    for (final p in catalogo.planes)
      if (p.googleProducto != null) p.googleProducto!,
  };
  if (!catalogo.googleDisponible || productos.isEmpty) return const {};
  final t = ref.watch(tiendaPlayProvider);
  try {
    if (!await t.disponible()) return const {};
    return await t.precios(productos);
  } catch (_) {
    return const {};
  }
});

/// Estado de la compra en curso y el último aviso para el alumno.
class EstadoComprasPlay {
  const EstadoComprasPlay({this.procesando = false, this.aviso, this.exito = false, this.n = 0});

  /// Compra abierta en Google o verificándose en el servidor.
  final bool procesando;
  final String? aviso;
  final bool exito;

  /// Sube con cada aviso (para mostrarlo una sola vez).
  final int n;

  EstadoComprasPlay conAviso(String texto, {bool exito = false}) =>
      EstadoComprasPlay(aviso: texto, exito: exito, n: n + 1);
}

/// Escucha las compras de Google Play desde que arranca la app, las verifica
/// en el servidor y solo entonces las completa.
class ComprasPlayNotifier extends StateNotifier<EstadoComprasPlay> {
  ComprasPlayNotifier(this._ref) : super(const EstadoComprasPlay()) {
    if (_ref.read(pagoEnAppProvider)) {
      _sub = _tienda.compras.listen(_procesar, onError: (_) {});
    }
  }

  final Ref _ref;
  StreamSubscription<List<CompraPlay>>? _sub;

  /// Idiomas elegidos para la compra abierta: se guardan por si la app se
  /// cierra antes de verificarla.
  static const clavePendiente = 'onelingo.compraPlay.pendiente';

  TiendaPlay get _tienda => _ref.read(tiendaPlayProvider);
  PagosApi get _api => _ref.read(pagosApiProvider);
  SharedPreferences get _prefs => _ref.read(prefsProvider);

  @override
  void dispose() {
    _sub?.cancel();
    super.dispose();
  }

  /// Abre la compra del plan [p] por [meses] meses. Si ya paga en Play, la
  /// nueva reemplaza a la anterior (Google prorratea el tiempo que queda).
  Future<void> comprar(PlanServidor p, int meses, List<String> idiomas) async {
    final producto = p.googleProducto;
    if (producto == null || state.procesando) return;
    final cuenta = Sync.instancia.usuarioId;
    if (cuenta == null || cuenta.isEmpty) {
      state = state.conAviso(tr('Inicia sesión para suscribirte.'));
      return;
    }
    await _prefs.setString(clavePendiente, jsonEncode({'producto': producto, 'idiomas': idiomas}));
    final sus = _ref.read(suscripcionProvider);
    final anterior = sus != null && sus.googleVigente ? sus.googleProducto : null;
    state = EstadoComprasPlay(procesando: true, n: state.n);
    bool abierta;
    try {
      abierta = await _tienda.comprar(producto: producto, planBase: planBaseDeMeses(meses), cuenta: cuenta, productoAnterior: anterior);
    } catch (_) {
      abierta = false;
    }
    if (!abierta) state = state.conAviso(tr('No se pudo abrir el pago de Google Play. Instala OneLingo desde Google Play e inténtalo de nuevo.'));
  }

  /// Al arrancar: compras ya cobradas que no llegaron a verificarse.
  Future<void> reintentarPendientes() async {
    if (!_ref.read(pagoEnAppProvider) || !_ref.read(catalogoPlanesProvider).googleDisponible) return;
    try {
      for (final c in await _tienda.sinCompletar()) {
        if (c.estado == EstadoCompraPlay.comprada) await _verificar(c, silencioso: true);
      }
    } catch (_) {
      /* Sin Play (APK instalado fuera de la tienda): nada que reintentar. */
    }
  }

  Future<void> _procesar(List<CompraPlay> compras) async {
    for (final c in compras) {
      switch (c.estado) {
        case EstadoCompraPlay.comprada:
          await _verificar(c);
        case EstadoCompraPlay.pendiente:
          state = state.conAviso(tr('Tu pago está pendiente. Tendrás tu plan en cuanto Google Play lo confirme.'));
        case EstadoCompraPlay.cancelada:
          state = EstadoComprasPlay(n: state.n);
        case EstadoCompraPlay.error:
          state = state.conAviso(c.error?.isNotEmpty == true ? c.error! : tr('No se pudo completar el pago.'));
      }
    }
  }

  Future<void> _verificar(CompraPlay c, {bool silencioso = false}) async {
    if (c.token.isEmpty) return;
    var idiomas = const <String>[];
    try {
      final p = jsonDecode(_prefs.getString(clavePendiente) ?? '{}') as Map<String, dynamic>;
      if (p['producto'] == c.producto) idiomas = (p['idiomas'] as List? ?? const []).whereType<String>().toList();
    } catch (_) {}
    if (!silencioso) state = EstadoComprasPlay(procesando: true, n: state.n);
    final r = await _api.verificarGoogle(c.token, idiomas);
    if (!mounted) return;
    if (r.ok) {
      _ref.read(suscripcionProvider.notifier).aplicar(r.cuerpo);
      await _tienda.completar(c);
      await _prefs.remove(clavePendiente);
      state = state.conAviso(tr('¡Listo! Tu plan ya está activo.'), exito: true);
    } else if (!silencioso) {
      // Sin completar: el servidor lo vuelve a intentar al abrir la app; si
      // nadie la reconoce en 3 días, Google la reembolsa.
      state = state.conAviso(r.codigo == 403 || r.codigo == 404
          ? r.error
          : tr('Recibimos tu pago, pero aún no pudimos confirmarlo. Lo intentaremos de nuevo al abrir la app.'));
    }
  }
}

final comprasPlayProvider = StateNotifierProvider<ComprasPlayNotifier, EstadoComprasPlay>(
  (ref) => ComprasPlayNotifier(ref),
);
