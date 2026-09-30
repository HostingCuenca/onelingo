import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/diagnostico.dart';
import 'package:onelingo/core/state/providers.dart';

void main() {
  test('estado legacy conserva nivel original y deriva nivel cliente', () {
    final state = ProgressState.fromJson({
      'nivelInicial': 10,
      'idiomaMeta': 'en',
    });
    expect(state.nivelInicial, 10);
    expect(state.nivelEscala, escalaDiagnosticoLegacy);
    expect(state.nivelCliente, 8);

    final roundTrip = ProgressState.fromJson(state.toJson());
    expect(roundTrip.nivelInicial, 10);
    expect(roundTrip.nivelCliente, 8);
    expect(state.toJson().containsKey('nivelClienteInicial'), isFalse);
  });

  test('estado cliente conserva las dos ubicaciones explícitas', () {
    const state = ProgressState(
      nivelInicial: 4,
      nivelEscala: escalaDiagnosticoCliente,
      nivelClienteInicial: 7,
    );
    final json = state.toJson();
    expect(json['nivelInicial'], 4);
    expect(json['nivelEscala'], escalaDiagnosticoCliente);
    expect(json['nivelClienteInicial'], 7);

    final restored = ProgressState.fromJson(json);
    expect(restored.nivelInicial, 4);
    expect(restored.nivelCliente, 7);
  });

  test(
    'estado cliente antiguo sin campo explícito no se interpreta como legacy',
    () {
      final state = ProgressState.fromJson({
        'nivelInicial': 7,
        'nivelEscala': escalaDiagnosticoCliente,
      });
      expect(state.nivelCliente, 7);
    },
  );
}
