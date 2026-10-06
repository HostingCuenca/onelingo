import 'package:flutter_test/flutter_test.dart';
import 'package:onelingo/core/aprendizaje/integridad.dart';

/// Morfología alemana de la integridad: espejo de `conocida_de` en
/// tools/validar_ruta.py (flexiones de palabras y verbos ya enseñados).
void main() {
  void conocidas(List<(String, String)> casos) {
    for (final (forma, base) in casos) {
      expect(
        palabraConocidaDe(forma, {base}),
        isTrue,
        reason: '$forma ← $base',
      );
    }
  }

  test('presente regular, e de unión y cambio vocálico', () {
    conocidas([
      ('arbeitest', 'arbeiten'), ('wartet', 'warten'), ('mache', 'machen'), //
      ('machst', 'machen'), ('komm', 'kommen'), ('wandert', 'wandern'),
      ('sammle', 'sammeln'), ('fährt', 'fahren'), ('liest', 'lesen'),
      ('nimmt', 'nehmen'), ('isst', 'essen'), ('gibt', 'geben'),
      ('spricht', 'sprechen'), ('läuft', 'laufen'), ('sieht', 'sehen'),
      ('hilft', 'helfen'), ('vergisst', 'vergessen'), ('besucht', 'besuchen'),
      ('studiert', 'studieren'),
    ]);
  });

  test('sein, haben, werden, tun y modales', () {
    conocidas([
      ('bin', 'sein'), ('ist', 'sein'), ('hat', 'haben'), ('wird', 'werden'), //
      ('tut', 'tun'), ('kann', 'können'), ('kannst', 'können'),
      ('können', 'können'), ('muss', 'müssen'), ('will', 'wollen'),
      ('darf', 'dürfen'), ('soll', 'sollen'), ('mag', 'mögen'),
      ('weiß', 'wissen'), ('möchte', 'mögen'), ('möchtest', 'möchten'),
    ]);
  });

  test('Partizip II regular, irregular y con prefijo', () {
    conocidas([
      ('gemacht', 'machen'),
      ('gearbeitet', 'arbeiten'),
      ('gekauft', 'kaufen'), //
      ('gewesen', 'sein'), ('gehabt', 'haben'), ('gegangen', 'gehen'),
      ('gekommen', 'kommen'), ('gesehen', 'sehen'), ('getrunken', 'trinken'),
      ('gegessen', 'essen'), ('geschrieben', 'schreiben'),
      ('gesprochen', 'sprechen'), ('genommen', 'nehmen'),
      ('verstanden', 'verstehen'), ('begonnen', 'beginnen'),
      ('bekommen', 'bekommen'),
      // Participio declinado como adjetivo.
      ('gekochte', 'kochen'), ('geschlossene', 'schließen'),
    ]);
  });

  test('Präteritum y Konjunktiv II', () {
    conocidas([
      ('war', 'sein'), ('waren', 'sein'), ('hatte', 'haben'), //
      ('hatten', 'haben'), ('wurde', 'werden'), ('konnte', 'können'),
      ('musste', 'müssen'), ('wollte', 'wollen'), ('durfte', 'dürfen'),
      ('sollte', 'sollen'), ('mochte', 'mögen'), ('machte', 'machen'),
      ('arbeiteten', 'arbeiten'), ('ging', 'gehen'), ('gingen', 'gehen'),
      ('kamst', 'kommen'), ('wäre', 'sein'), ('wären', 'sein'),
      ('hätte', 'haben'), ('hättest', 'haben'), ('würde', 'werden'),
      ('würden', 'werden'), ('könnte', 'können'), ('könntest', 'können'),
      ('müsste', 'müssen'), ('wüsste', 'wissen'),
    ]);
  });

  test('verbos separables: prefijo aparte, -ge- y -zu- intercalados', () {
    conocidas([
      ('angerufen', 'anrufen'), ('aufgestanden', 'aufstehen'), //
      ('eingekauft', 'einkaufen'), ('kennengelernt', 'kennenlernen'),
      ('anzurufen', 'anrufen'), ('ankommt', 'ankommen'),
      // «Ich rufe dich an»: el verbo y el prefijo, cada uno por su lado.
      ('rufe', 'anrufen'), ('an', 'anrufen'), ('stehe', 'aufstehen'),
    ]);
  });

  test('plurales, caso, adjetivos y grado', () {
    conocidas([
      ('tage', 'tag'), ('kinder', 'kind'), ('kindern', 'kind'), //
      ('frauen', 'frau'), ('autos', 'auto'), ('äpfel', 'apfel'),
      ('bücher', 'buch'), ('häuser', 'haus'), ('städte', 'stadt'),
      ('mütter', 'mutter'), ('freundinnen', 'freundin'), ('busse', 'bus'),
      ('herrn', 'herr'), ('hundes', 'hund'), ('mannes', 'mann'),
      ('kleine', 'klein'), ('kleinen', 'klein'), ('kleinem', 'klein'),
      ('kleiner', 'klein'), ('kleines', 'klein'), ('dunkle', 'dunkel'),
      ('teure', 'teuer'), ('älter', 'alt'), ('ältesten', 'alt'),
      ('schneller', 'schnell'), ('schnellsten', 'schnell'),
      ('größer', 'groß'), ('größte', 'groß'), ('besser', 'gut'),
      ('besten', 'gut'), ('mehr', 'viel'), ('lieber', 'gern'),
    ]);
    expect(basesFlexionDe('bücher'), contains('buch'));
  });

  test('grafías ß/ss y diéresis/ae-oe-ue', () {
    conocidas([
      ('strasse', 'straße'), ('straße', 'strasse'), ('strassen', 'straße'), //
      ('muesli', 'müsli'), ('schoen', 'schön'), ('grüße', 'gruesse'),
    ]);
    expect(grafiasDe('strasse'), containsAll(['strasse', 'straße']));
  });

  test('mayúsculas y comillas alemanas no forman parte de la palabra', () {
    expect(palabrasMeta('„Guten Tag“, sagt sie. ‚So‘ »gut« ›ja‹'), [
      'guten', 'tag', 'sagt', 'sie', 'so', 'gut', 'ja', //
    ]);
    expect(
      palabrasMeta('Die Straße')
          .every((w) => palabraConocidaDe(w, {'die', 'strasse'})),
      isTrue,
    );
  });

  test('formas de verbos.json (sin auxiliar ni trennbar nulo)', () {
    final indice = indiceFormasVerbales({
      'verbos': [
        {
          'infinitivo': 'aufstehen',
          'tablas': {
            'praesens': ['stehe auf', 'stehst auf'],
          },
          'formas': {
            'partizip2': 'aufgestanden',
            'auxiliar': 'sein',
            'trennbar': 'auf',
          },
        },
        {
          'infinitivo': 'machen',
          'formas': {'auxiliar': 'haben', 'trennbar': null},
        },
      ],
    });
    expect(indice['stehst'], {'aufstehen'});
    expect(indice.containsKey('sein'), isFalse);
    expect(indice.containsKey('haben'), isFalse);
    expect(palabraConocidaDe('stehst', {'aufstehen'}, indice), isTrue);
  });

  test('negativos: nada se acepta sin su base enseñada', () {
    for (final (forma, base) in const [
      // Palabras que parecen flexión de otra y no lo son.
      ('aber', 'ab'), ('unsere', 'uns'), ('dass', 'das'), ('das', 'da'), //
      ('wenn', 'wen'), ('denn', 'den'), ('neun', 'neu'), ('ihnen', 'ihn'),
      ('etwas', 'etwa'), ('eins', 'ein'), ('seit', 'sein'),
      // Bases distintas.
      ('kinder', 'kino'), ('gemacht', 'sagen'), ('fährt', 'führen'),
      ('katze', 'hund'), ('gegessen', 'vergessen'), ('auf', 'aus'),
      ('liest', 'lassen'), ('tische', 'tasche'), ('geld', 'gel'),
      ('und', 'un'), ('bild', 'bil'),
    ]) {
      expect(
        palabraConocidaDe(forma, {base}),
        isFalse,
        reason: '$forma ← $base',
      );
    }
    expect(palabraConocidaDe('gekocht', const {}), isFalse);
    // Un prefijo suelto solo vale si se enseñó un verbo con él.
    expect(palabraConocidaDe('an', {'anna'}), isFalse);
    expect(palabraConocidaDe('zu', {'zusammen'}), isFalse);
    // Solo el alemán usa esta morfología: la regla general no la acepta.
    expect(palabraConocida('fährt', {'fahren'}), isFalse);
    expect(palabraConocida('gegangen', {'gehen'}), isFalse);
  });
}
