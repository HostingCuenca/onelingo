import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/integridad.dart';

/// Morfología italiana de la integridad: espejo de `conocida_it` en
/// tools/validar_ruta.py (elisión, acentos, flexiones y verbos enseñados).
void main() {
  void conocidas(List<(String, Set<String>)> casos) {
    for (final (forma, saber) in casos) {
      expect(
        palabraConocidaIt(forma, saber),
        isTrue,
        reason: '$forma ← $saber',
      );
    }
  }

  void desconocidas(List<(String, Set<String>)> casos) {
    for (final (forma, saber) in casos) {
      expect(
        palabraConocidaIt(forma, saber),
        isFalse,
        reason: '$forma ← $saber',
      );
    }
  }

  test('elisión: artículo, preposición articulada y clíticos', () {
    conocidas([
      // «l'» enseñado queda como «l» tras palabrasMeta.
      ("l'amico", {'l', 'amico'}), ("l'amico", {'il', 'amico'}), //
      ("l'amica", {'la', 'amica'}), ("l'hotel", {'lo', 'hotel'}),
      ("dell'acqua", {'della', 'acqua'}), ("dell'acqua", {'di', 'il', 'acqua'}),
      ("nell'ufficio", {'nella', 'ufficio'}), ("all'una", {'alla', 'una'}),
      ("sull'autobus", {'su', 'la', 'autobus'}),
      ("un'amica", {'una', 'amica'}), ("un'amica", {'un', 'amica'}),
      ("c'è", {'ci', 'è'}), ("c'è", {'ci', 'essere'}),
      ("dov'è", {'dove', 'è'}), ("com'è", {'come', 'essere'}),
      ("cos'è", {'cosa', 'è'}), ("quest'anno", {'questo', 'anno'}),
      ("anch'io", {'anche', 'io'}), ("vent'anni", {'venti', 'anno'}),
      // Una elisión ya enseñada sirve para otra palabra.
      ("l'acqua", {"l'amico", 'acqua'}),
    ]);
    desconocidas([
      ("l'amico", {'amico'}), ("l'amico", {'l'}), ("c'è", {'essere'}), //
      ("dell'acqua", {'acqua'}), ("un'amica", {'amica'}),
    ]);
  });

  test('acentos, truncamientos y lo visto tras un apóstrofo', () {
    conocidas([
      ('perché', {'perché'}), ('perchè', {'perché'}), ('città', {'città'}), //
      ('caffé', {'caffè'}), ('po', {'poco'}), ('buon', {'buono'}),
      ('signor', {'signore'}), ('è', {"dov'è"}),
    ]);
    // è (verbo) y e (conjunción) no se confunden.
    desconocidas([
      ('è', {'e'}),
      ('e', {'è'}),
      ('città', {'citta'}),
    ]);
  });

  test('mayúsculas, comillas y apóstrofos tipográficos', () {
    expect(palabrasMeta("«Dov'è l’ufficio?» Un po' di caffè. Perché?"), [
      "dov'è", "l'ufficio", 'un', 'po', 'di', 'caffè', 'perché', //
    ]);
    expect(palabrasMeta("L'Insegnante È qui"), ["l'insegnante", 'è', 'qui']);
    final saber = {...palabrasMeta("l' insegnante essere qui dove ufficio")};
    expect(
      palabrasMeta("L'insegnante è qui. Dov'è l’ufficio?")
          .every((w) => palabraConocidaIt(w, saber)),
      isTrue,
    );
  });

  test('plurales, femeninos, -issimo y -mente', () {
    conocidas([
      ('amici', {'amico'}), ('amiche', {'amica'}), ('amiche', {'amico'}), //
      ('italiane', {'italiano'}), ('chiavi', {'chiave'}),
      ('tedeschi', {'tedesco'}), ('case', {'casa'}), ('libri', {'libro'}),
      ('arance', {'arancia'}), ('orologi', {'orologio'}),
      ('uomini', {'uomo'}), ('bellissima', {'bello'}),
      ('grandissimo', {'grande'}), ('lentamente', {'lento'}),
      ('facilmente', {'facile'}), ('attrice', {'attore'}),
    ]);
    desconocidas([
      ('anche', {'anca'}), ('dei', {'dea'}), ('gatto', {'cane'}), //
      ('cane', {'cono'}), ('amici', {'amare'}),
    ]);
  });

  test('verbos regulares, -isc-, irregulares y participios', () {
    conocidas([
      ('parlo', {'parlare'}), ('parliamo', {'parlare'}), //
      ('parlato', {'parlare'}), ('mangi', {'mangiare'}),
      ('mangerò', {'mangiare'}), ('cerchi', {'cercare'}),
      ('prendo', {'prendere'}), ('dormono', {'dormire'}),
      ('finisco', {'finire'}), ('capisce', {'capire'}),
      ('è', {'essere'}), ('sono', {'essere'}), ('ho', {'avere'}),
      ('vado', {'andare'}), ('andata', {'andare'}), ('fatto', {'fare'}),
      ('fatta', {'fare'}), ('scritte', {'scrivere'}), ('vorrei', {'volere'}),
      ('può', {'potere'}), ('conosciuto', {'conoscere'}),
      ('traduco', {'tradurre'}), ('rifatto', {'rifare'}),
      ('chiamo', {'chiamarsi'}),
    ]);
    desconocidas([
      ('parlo', {'parola'}),
      ('ho', {'essere'}),
    ]);
  });

  test('enclíticos: el pronombre también debe estar enseñado', () {
    conocidas([
      ('chiamarsi', {'chiamare', 'si'}), ('vederlo', {'vedere', 'lo'}), //
      ('dimmi', {'dire', 'mi'}), ('fallo', {'fare', 'lo'}),
    ]);
    desconocidas([
      ('vederlo', {'vedere'}),
      ('dimmi', {'mi'}),
    ]);
  });

  test('formas de verbos.json, si existe', () {
    final indice = indiceFormasVerbales({
      'verbos': [
        {
          'infinitivo': 'andare',
          'tablas': {
            'presente': ['vado', 'vai', 'va'],
          },
          'formas': {'participio': 'andato', 'auxiliar': 'essere'},
        },
      ],
    });
    expect(indice['vai'], {'andare'});
    expect(indice.containsKey('essere'), isFalse);
    expect(palabraConocidaIt('vai', {'andare'}, indice), isTrue);
  });

  test('solo el italiano usa esta morfología', () {
    expect(palabraConocida("l'amico", {'il', 'amico'}), isFalse);
    expect(palabraConocida('amiche', {'amica'}), isFalse);
  });
}
