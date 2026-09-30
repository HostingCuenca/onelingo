import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/diagnostico.dart';
import 'package:onelingo/core/aprendizaje/dominio.dart';

void main() {
  test('conserva diagnóstico legacy y expone equivalencia cliente', () {
    const r = ResultadoDiag(
      declarado: 4,
      nivel: 4,
      cefr: 'A2',
      confianza: .8,
      preguntas: 10,
      aciertos: 8,
      skills: {},
      fortalezas: [],
      debilidades: [],
      recurrentes: [],
      refuerzo: [],
      recomendado: 4,
      plan: [],
    );
    final json = r.toJson();
    expect(json['escala'], escalaDiagnosticoLegacy);
    expect(json['nivelCliente'], 2);
    expect(nivelClienteDeDiagnostico(json), 2);
  });

  test('lectura de diagnósticos nuevos no altera el respaldo histórico', () {
    expect(
      nivelClienteDeDiagnostico({
        'escala': escalaDiagnosticoCliente,
        'nivelCliente': 7,
        'recomendado': 2,
      }),
      7,
    );
    expect(nivelClienteDeDiagnostico({'recomendado': 2}), 1);
    expect(nivelBaseClienteDe(desdeCero: false, nivelInicial: 2), 1);
    expect(nivelClienteDesdeLegacy(8), 5);
    expect(nivelClienteDesdeLegacy(10), 8);
  });
}
