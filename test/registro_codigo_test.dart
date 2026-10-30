import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/features/onboarding/codigo_correo.dart';

void main() {
  test('teléfono: código de país + solo dígitos; vacío si es muy corto', () {
    expect(telefonoCompleto('+1', '555 123 4567'), '+15551234567');
    expect(telefonoCompleto('+52', '55-1234-5678'), '+525512345678');
    expect(telefonoCompleto('+1', '123'), '');
  });

  test('el selector de país empieza por +1 y no repite códigos', () {
    final codigos = prefijosTelefono.map((p) => p.$1).toList();
    expect(codigos.first, '+1');
    expect(codigos.toSet().length, codigos.length);
  });
}
