import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/cargador.dart';
import 'package:onelingo/core/aprendizaje/integridad.dart';

/// Morfología portuguesa de la integridad: espejo de `conocida_pt` en
/// tools/validar_ruta.py (flexiones de palabras y verbos ya enseñados).
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('plurales y femeninos de palabras enseñadas', () {
    expect(palabraConocidaPt('aberta', {'aberto'}), isTrue);
    expect(palabraConocidaPt('brasileiras', {'brasileiro'}), isTrue);
    expect(palabraConocidaPt('estações', {'estação'}), isTrue);
    expect(palabraConocidaPt('professora', {'professor'}), isTrue);
    expect(palabraConocidaPt('hotéis', {'hotel'}), isTrue);
    expect(basesFlexionPt('jovens'), contains('jovem'));
  });

  test('formas de verbos regulares con su cambio ortográfico', () {
    expect(palabraConocidaPt('escorregou', {'escorregar'}), isTrue);
    expect(palabraConocidaPt('liguei', {'ligar'}), isTrue);
    expect(palabraConocidaPt('fiquei', {'ficar'}), isTrue);
    expect(palabraConocidaPt('comecei', {'começar'}), isTrue);
    expect(palabraConocidaPt('compro', {'comprar'}), isTrue);
    expect(infinitivosPt('aceita'), contains('aceitar'));
    // Gerundio de verbos cortos.
    expect(palabraConocidaPt('indo', {'ir'}), isTrue);
    expect(palabraConocidaPt('sendo', {'ser'}), isTrue);
    expect(palabraConocidaPt('tendo', {'ter'}), isTrue);
    expect(palabraConocidaPt('pondo', {'pôr'}), isTrue);
    expect(palabraConocidaPt('compondo', {'pôr'}), isFalse); // solo «pondo»
  });

  test('ênclise: verbo + clítico enseñados', () {
    expect(palabraConocidaPt('registra-se', {'registrar', 'se'}), isTrue);
    expect(palabraConocidaPt('deixá-la', {'deixar', 'a'}), isTrue);
    expect(palabraConocidaPt('fazê-lo', {'fazer', 'o'}), isTrue);
  });

  test('formas irregulares desde verbos.json', () async {
    final indice = indiceFormasVerbales({
      'verbos': [
        {
          'infinitivo': 'Fazer',
          'tablas': {
            'preterito': ['fiz', 'fez'],
          },
          'formas': {'participio': 'feito'},
        },
      ],
    });
    expect(indice['fiz'], {'fazer'});
    expect(palabraConocidaPt('feito', {'fazer'}, indice), isTrue);
    expect(palabraConocidaPt('fiz', {'fazer'}), isFalse); // sin el índice
    // El asset real: «aberto» es el participio irregular de «abrir».
    final pt = await CargadorRuta().formasVerbales('pt');
    expect(pt['aberto'], contains('abrir'));
    expect(palabraConocidaPt('aberto', {'abrir'}, pt), isTrue);
    expect(palabraConocidaPt('aberto', {'abrir'}), isFalse);
  });

  test('negativos: nada se acepta sin su base enseñada', () {
    expect(palabraConocidaPt('aberta', const {}), isFalse);
    expect(palabraConocidaPt('brasileiras', {'brasil'}), isFalse);
    expect(palabraConocidaPt('escorregou', {'comer'}), isFalse);
    expect(palabraConocidaPt('liguei', {'lugar'}), isFalse);
    // Sin el clítico enseñado, o con dos guiones, la ênclise no vale.
    expect(palabraConocidaPt('registra-se', {'registrar'}), isFalse);
    expect(palabraConocidaPt('deixá-la', {'a'}), isFalse);
    expect(palabraConocidaPt('dá-se-lhe', {'dar', 'se', 'lhe'}), isFalse);
    expect(palabraConocidaPt('deixá-xy', {'deixar', 'a'}), isFalse);
    // Solo el portugués usa esta morfología: la regla general no la acepta.
    expect(palabraConocida('aberta', {'aberto'}), isFalse);
    expect(palabraConocida('liguei', {'ligar'}), isFalse);
  });
}
