import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/silencio.dart';

void main() {
  test('initial silence or one click does not end a turn', () {
    final d = FinPorSilencio();
    expect(d.actualizar(-90, const Duration(seconds: 8)), false);
    expect(d.actualizar(-20, const Duration(seconds: 9)), false);
    expect(d.actualizar(-90, const Duration(seconds: 15)), false);
  });
  test('Hi, pause, I am fine stays together, then waits three seconds', () {
    final d = FinPorSilencio();
    expect(d.actualizar(-25, const Duration(milliseconds: 200)), false);
    expect(d.actualizar(-25, const Duration(milliseconds: 400)), false);
    expect(d.actualizar(-90, const Duration(milliseconds: 1900)), false);
    expect(d.actualizar(-30, const Duration(milliseconds: 2100)), false);
    expect(d.actualizar(-30, const Duration(milliseconds: 2300)), false);
    expect(d.actualizar(-90, const Duration(milliseconds: 5299)), false);
    expect(
      d.actualizar(double.negativeInfinity, const Duration(milliseconds: 5300)),
      true,
    );
  });
  test(
    'long answers are not limited to eight seconds; bad samples do not stop',
    () {
      final d = FinPorSilencio();
      for (var i = 0; i < 200; i++)
        expect(d.actualizar(-30, Duration(milliseconds: i * 200)), false);
      expect(d.actualizar(double.nan, const Duration(seconds: 45)), false);
      expect(d.actualizar(-90, const Duration(seconds: 43)), true);
    },
  );
}
