import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/correccion.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';
import 'package:onelingo/core/aprendizaje/grafo.dart';
import 'package:onelingo/core/aprendizaje/migracion.dart';
import 'package:onelingo/core/aprendizaje/modelos.dart';
import 'package:onelingo/core/content/contenido_json.dart';
import 'package:onelingo/core/state/providers.dart';

/// Estados, desbloqueo, repaso y migración de la ruta (datos reales de inglés).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late RutaCargada ruta;
  setUpAll(() async {
    ruta = (await CargadorRuta().cargar('en'))!;
    // Como en la app: el contenido del nivel 0 se precarga al iniciar.
    await ContenidoJson.precargar('en');
    await ContenidoJson.precargar('fr');
  });

  UnidadRuta u(int orden) => ruta.unidades.firstWhere((x) => x.orden == orden);

  /// Evidencia de toda la práctica guiada resuelta de una unidad.
  Map<String, dynamic> guiadaResuelta(UnidadRuta unidad) => {
    for (final (p, i) in unidad.itemsDe(TipoPaso.practicaGuiada))
      ClaveRuta.item(unidad.id, p.id, i.id): {
        'correcta': true,
        'resueltaConApoyo': true,
      },
  };

  test('Estado inicial: solo la primera unidad disponible', () {
    final e = estadosRuta(ruta, {});
    expect(e[u(0).id]!.estado, EstadoUnidad.disponible);
    for (final x in ruta.unidades.skip(1)) {
      expect(e[x.id]!.estado, EstadoUnidad.bloqueada, reason: x.id);
    }
    expect(unidadRecomendada(ruta, e)!.id, u(0).id);
  });

  test('Practicar con ayuda desbloquea la siguiente, pero no aprueba', () {
    final e = estadosRuta(ruta, guiadaResuelta(u(0)));
    expect(e[u(0).id]!.estado, EstadoUnidad.practicada);
    expect(e[u(1).id]!.estado, EstadoUnidad.disponible);
    expect(e[u(2).id]!.estado, EstadoUnidad.bloqueada);
  });

  test('Evaluación: aprobar exige el umbral y no se revoca', () {
    final ahora = DateTime(2026, 9, 26, 10);
    final suspenso = resumenEvaluacion(u(0), 3, 5, null, ahora);
    expect(suspenso['aprobada'], isFalse);
    final aprobado = resumenEvaluacion(u(0), 4, 5, suspenso, ahora);
    expect(aprobado['aprobada'], isTrue);
    final peor = resumenEvaluacion(u(0), 1, 5, aprobado, ahora);
    expect(peor['aprobada'], isTrue);
    expect(peor['fechaAprobada'], aprobado['fechaAprobada']);
    final e = estadosRuta(ruta, {
      ...guiadaResuelta(u(0)),
      ClaveRuta.evaluacion(u(0).id): peor,
    }, ahora: ahora);
    expect(e[u(0).id]!.estado, EstadoUnidad.aprobada);
    expect(e[u(0).id]!.repasoPendiente, isFalse);
  });

  test('Dominio exige retención: repaso acertado al menos 1 día después', () {
    final dia0 = DateTime(2026, 9, 26, 10);
    final evaluacion = resumenEvaluacion(u(0), 5, 5, null, dia0);
    // Repaso el mismo día: suma caja pero no demuestra retención.
    final mismoDia = siguienteRepaso(u(0), evaluacion, null, 5, 5, dia0);
    expect(mismoDia['retencion'], isFalse);
    // Al día siguiente, el repaso vence.
    var e = estadosRuta(ruta, {
      ClaveRuta.evaluacion(u(0).id): evaluacion,
    }, ahora: dia0.add(const Duration(days: 1, hours: 1)));
    expect(e[u(0).id]!.repasoPendiente, isTrue);
    expect(unidadRecomendada(ruta, e)!.id, u(0).id);
    final alDia = siguienteRepaso(
      u(0),
      evaluacion,
      mismoDia,
      5,
      5,
      dia0.add(const Duration(days: 1, hours: 1)),
    );
    expect(alDia['retencion'], isTrue);
    e = estadosRuta(ruta, {
      ClaveRuta.evaluacion(u(0).id): evaluacion,
      ClaveRuta.repaso(u(0).id): alDia,
    }, ahora: dia0.add(const Duration(days: 1, hours: 2)));
    expect(e[u(0).id]!.estado, EstadoUnidad.dominada);
    expect(e[u(0).id]!.repasoPendiente, isFalse);
    // Un repaso fallado baja de caja y vuelve a pedirse pronto.
    final fallo = siguienteRepaso(
      u(0),
      evaluacion,
      alDia,
      1,
      5,
      dia0.add(const Duration(days: 5)),
    );
    expect(fallo['caja'], lessThan(alDia['caja'] as int));
    expect(
      fallo['retencion'],
      isTrue,
      reason: 'la retención ya demostrada se conserva',
    );
    expect(fallo['necesitaRefuerzo'], isTrue);
  });

  test('Nivel 0 completo solo con todas las unidades aprobadas', () {
    final ahora = DateTime(2026, 9, 26);
    final practicas = <String, dynamic>{};
    for (final x in ruta.delNivel('f0')) {
      expect(nivelAprobado(ruta, estadosRuta(ruta, practicas), 'f0'), isFalse);
      practicas.addAll(guiadaResuelta(x));
      practicas[ClaveRuta.evaluacion(x.id)] = resumenEvaluacion(
        x,
        5,
        5,
        null,
        ahora,
      );
    }
    expect(nivelAprobado(ruta, estadosRuta(ruta, practicas), 'f0'), isTrue);
  });

  test('Migración foundations-v1: practicado con apoyo, nunca aprobado', () {
    final antiguas = {
      for (final k in aliasFoundationV1.keys)
        k: {'correcta': true, 'resueltaConApoyo': true, 'conApoyo': true},
    };
    // Todos los destinos existen en el contenido real.
    for (final destino in aliasFoundationV1.values) {
      final partes = destino.split(':');
      final unidad = ruta.unidad(partes[1]);
      expect(unidad, isNotNull, reason: destino);
      final paso = unidad!.pasos.firstWhere((p) => p.id == partes[2]);
      expect(paso.tipo, TipoPaso.practicaGuiada, reason: destino);
      expect(paso.items.any((i) => i.id == partes[3]), isTrue, reason: destino);
    }
    final e = estadosRuta(ruta, antiguas);
    for (final info in e.values) {
      expect(info.estado.alMenos(EstadoUnidad.aprobada), isFalse);
    }
    // La evidencia antigua aparece como progreso de las unidades nuevas.
    expect(e['en.f0.pronombres']!.estado, EstadoUnidad.bloqueada);
    expect(evidenciaDe(antiguas, 'ruta:en.f0.pronombres:p4:g1'), isNotNull);
    // Pura e idempotente: no modifica las claves antiguas.
    expect(estadosRuta(ruta, antiguas).length, e.length);
    expect(antiguas.keys.toSet(), aliasFoundationV1.keys.toSet());
  });

  test('ProgressState: fundamentos terminan con la ruta y se conserva al serializar', () {
    final base = ProgressState(
      onboardingDone: true,
      idiomaMeta: 'en',
      nivelInicial: 1,
      fundamentos: true,
    );
    expect(base.fundamentosPendientes, isTrue);
    expect(base.nivelActual, 0);
    final hecho = base.copyWith(
      practicas: {
        'ruta:en.f0:completa': {'correcta': true},
      },
    );
    expect(hecho.fundamentosPendientes, isFalse);
    expect(hecho.nivelActual, 1);
    // La marca vive en `practicas`: sobrevive a toJson/fromJson.
    final vuelta = ProgressState.fromJson(hecho.toJson());
    expect(vuelta.rutaFundamentosAprobada, isTrue);
    // La marca de otro idioma no cuenta.
    expect(hecho.copyWith(idiomaMeta: 'fr').fundamentosPendientes, isTrue);
  });

  test('Diagnóstico: los niveles ya superados se pueden omitir', () {
    // Quien empieza de cero no omite nada.
    expect(nivelBaseDe(desdeCero: true, nivelInicial: 1), 0);
    var e = estadosRuta(ruta, {}, nivelBase: 0);
    expect(e.values.where((i) => i.omitible), isEmpty);
    // Ubicado en el Nivel 1: fundamentos opcionales, A1 disponible.
    final base = nivelBaseDe(desdeCero: false, nivelInicial: 1);
    e = estadosRuta(ruta, {}, nivelBase: base);
    for (final u in ruta.delNivel('f0')) {
      expect(e[u.id]!.omitible, isTrue, reason: u.id);
      expect(e[u.id]!.estado, isNot(EstadoUnidad.bloqueada), reason: u.id);
    }
    final siguiente = unidadRecomendada(ruta, e);
    expect(siguiente?.nivel, isNot('f0'));
    // Ubicado en A2 (nivel 3): todo A1 queda opcional.
    e = estadosRuta(ruta, {}, nivelBase: 3);
    for (final u in ruta.unidades.where((u) => (u.nivelInterno ?? 9) < 3)) {
      expect(e[u.id]!.omitible, isTrue, reason: u.id);
    }
    // Aprobar una unidad omitible la saca de «opcional».
    e = estadosRuta(ruta, {
      ClaveRuta.evaluacion(u(0).id): resumenEvaluacion(
        u(0),
        5,
        5,
        null,
        DateTime.now(),
      ),
    }, nivelBase: 1);
    expect(e[u(0).id]!.omitible, isFalse);
    expect(e[u(0).id]!.estado, EstadoUnidad.aprobada);
  });

  test('Grafo: detecta ciclos y prerrequisitos inexistentes', () {
    final a = ruta.unidades[0], b = ruta.unidades[1];
    UnidadRuta copia(UnidadRuta x, List<String> pre, int orden) => UnidadRuta(
      id: x.id,
      idioma: x.idioma,
      nivel: x.nivel,
      orden: orden,
      titulo: x.titulo,
      objetivo: x.objetivo,
      cefr: x.cefr,
      nivelInterno: x.nivelInterno,
      concepto: x.concepto,
      prerequisitos: pre,
      habilidades: x.habilidades,
      gramatica: x.gramatica,
      vocabulario: x.vocabulario,
      erroresFrecuentes: x.erroresFrecuentes,
      pasos: x.pasos,
      umbral: x.umbral,
      intervalosRepaso: x.intervalosRepaso,
      tutor: x.tutor,
    );
    expect(validarGrafo(ruta.unidades), isEmpty);
    expect(
      validarGrafo([
        copia(a, [b.id], 0),
        copia(b, [a.id], 1),
      ]),
      contains('ciclo de prerrequisitos'),
    );
    expect(
      validarGrafo([
        copia(a, ['en.f0.no-existe'], 0),
      ]).single,
      contains('inexistente'),
    );
  });

  test('Corrección normalizada y variantes aceptadas', () {
    final item = Item.fromJson({
      'id': 'x',
      'formato': 'escribir',
      'consigna': {'es': 'c'},
      'feedback': {'es': 'f'},
      'respuesta': "I'm not tired.",
      'aceptadas': ['I am not tired.'],
    });
    expect(corregir(item, 'i’m NOT tired', 'en'), isTrue);
    expect(corregir(item, 'I am not tired', 'en'), isTrue);
    expect(corregir(item, 'I am tired', 'en'), isFalse);
    final zh = Item.fromJson({
      'id': 'y',
      'formato': 'escribir',
      'consigna': {'es': 'c'},
      'feedback': {'es': 'f'},
      'respuesta': '我 是 学生',
    });
    expect(corregir(zh, '我是学生。', 'zh'), isTrue);
    // Error solo de tildes: se acepta y se avisa; una palabra distinta no.
    final pt = Item.fromJson({
      'id': 'z',
      'formato': 'escribir',
      'consigna': {'es': 'c'},
      'feedback': {'es': 'f'},
      'respuesta': 'Não, obrigada.',
    });
    expect(corregir(pt, 'nao obrigada', 'pt'), isTrue);
    expect(soloFallanTildes(pt, 'nao obrigada', 'pt'), isTrue);
    expect(soloFallanTildes(pt, 'Não, obrigada', 'pt'), isFalse);
    expect(corregir(pt, 'nao obrigado', 'pt'), isFalse);
  });
}
