import 'modelos.dart';

/// Problemas estructurales de una ruta (vacío = válida).
List<String> validarGrafo(List<UnidadRuta> unidades) {
  final errores = <String>[];
  final porId = <String, UnidadRuta>{};
  for (final u in unidades) {
    if (porId.containsKey(u.id)) errores.add('${u.id}: id duplicado');
    porId[u.id] = u;
  }
  for (final u in unidades) {
    for (final p in u.prerequisitos) {
      final pre = porId[p];
      if (pre == null) {
        errores.add('${u.id}: prerrequisito inexistente $p');
      } else if (pre.orden >= u.orden) {
        errores.add('${u.id}: orden no posterior a $p');
      }
    }
  }
  // Kahn: si no se pueden ordenar todas, hay un ciclo.
  final pendientes = {
    for (final u in unidades)
      u.id: u.prerequisitos.where(porId.containsKey).length,
  };
  final cola = [
    for (final e in pendientes.entries)
      if (e.value == 0) e.key,
  ];
  var ordenadas = 0;
  while (cola.isNotEmpty) {
    final id = cola.removeLast();
    ordenadas++;
    for (final u in unidades) {
      if (u.prerequisitos.contains(id)) {
        pendientes[u.id] = pendientes[u.id]! - 1;
        if (pendientes[u.id] == 0) cola.add(u.id);
      }
    }
  }
  if (ordenadas < porId.length) errores.add('ciclo de prerrequisitos');
  return errores;
}

/// Prerrequisitos transitivos de una unidad (sin incluirla).
Set<String> prerequisitosTransitivos(RutaCargada ruta, String id) {
  final res = <String>{};
  void visitar(String actual) {
    for (final p in ruta.unidad(actual)?.prerequisitos ?? const <String>[]) {
      if (res.add(p)) visitar(p);
    }
  }

  visitar(id);
  return res;
}
