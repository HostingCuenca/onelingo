import 'dart:math';

/// Baraja una copia de [xs] y garantiza que no quede en el orden original
/// (si hay al menos dos elementos distintos): así un banco de palabras o una
/// lista de opciones nunca se resuelve tocando de izquierda a derecha.
List<T> barajarDistinto<T>(List<T> xs, [Random? rnd]) {
  final r = [...xs]..shuffle(rnd ?? Random());
  bool igual() {
    for (var i = 0; i < xs.length; i++) {
      if (r[i] != xs[i]) return false;
    }
    return true;
  }

  if (xs.toSet().length < 2) return r;
  for (var giro = 0; giro < xs.length && igual(); giro++) {
    r.add(r.removeAt(0));
  }
  return r;
}
