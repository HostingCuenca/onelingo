/// Migración de foundations-v1 (6 microlecciones, 12 claves) a la ruta en.f0.
///
/// Es un alias de lectura: no escribe ni borra nada, así que es idempotente y
/// sobrevive a clientes antiguos. La evidencia antigua era guiada
/// (`conApoyo: true`), por eso solo puede aportar a «practicada», nunca a
/// «aprobada» ni «dominada». Detalle en docs/claude-educacion/MIGRACION_FUNDAMENTOS.md.
library;

const aliasFoundationV1 = <String, String>{
  'foundation-v1-i-you-0': 'ruta:en.f0.pronombres:p4:g1',
  'foundation-v1-i-you-1': 'ruta:en.f0.pronombres:p4:g2',
  'foundation-v1-he-she-0': 'ruta:en.f0.pronombres:p4:g3',
  'foundation-v1-i-am-0': 'ruta:en.f0.be-afirmativo:p6:g1',
  'foundation-v1-i-am-1': 'ruta:en.f0.be-afirmativo:p6:g1',
  'foundation-v1-you-are-0': 'ruta:en.f0.be-afirmativo:p6:g2',
  'foundation-v1-you-are-1': 'ruta:en.f0.be-afirmativo:p6:g2',
  'foundation-v1-he-she-1': 'ruta:en.f0.be-afirmativo:p6:g3',
  'foundation-v1-feelings-0': 'ruta:en.f0.be-afirmativo:p6:g4',
  'foundation-v1-feelings-1': 'ruta:en.f0.be-afirmativo:p6:g4',
  'foundation-v1-introduce-0': 'ruta:en.f0.presentarse:p4:g3',
  'foundation-v1-introduce-1': 'ruta:en.f0.presentarse:p4:g3',
};

final Map<String, List<String>> _inverso = () {
  final m = <String, List<String>>{};
  aliasFoundationV1.forEach((antigua, nueva) => (m[nueva] ??= []).add(antigua));
  return m;
}();

/// Claves antiguas que cuentan como evidencia de [claveNueva].
List<String> aliasHistoricos(String claveNueva) =>
    _inverso[claveNueva] ?? const [];
