/// Original introductory sequence. Guided practice never certifies a level.
class FoundationCard {
  const FoundationCard(
    this.english,
    this.spanish,
    this.explanation,
    this.visual,
  );
  final String english, spanish, explanation, visual;
}

class FoundationCheck {
  const FoundationCheck(
    this.prompt,
    this.options,
    this.answer,
    this.feedback, {
    this.order = false,
  });
  final String prompt, answer, feedback;
  final List<String> options;
  final bool order;
}

class FoundationUnit {
  const FoundationUnit(
    this.id,
    this.title,
    this.goal,
    this.requires,
    this.cards,
    this.checks,
  );
  final String id, title, goal;
  final List<String> requires;
  final List<FoundationCard> cards;
  final List<FoundationCheck> checks;
}

const foundationUnits = <FoundationUnit>[
  FoundationUnit(
    'i-you',
    'Yo y tú',
    'Reconocer a la persona que habla y a quien escucha.',
    [],
    [
      FoundationCard(
        'I',
        'yo',
        'Cuando hablo de mí, uso I. Se escribe siempre con mayúscula. No necesitas saber todavía qué es un pronombre.',
        'self',
      ),
      FoundationCard(
        'you',
        'tú',
        'Cuando hablo contigo, uso you. En estos primeros ejemplos significa tú. Más adelante también lo usaremos para usted y ustedes.',
        'you',
      ),
    ],
    [
      FoundationCheck(
        'Estás hablando de ti. ¿Qué palabra significa «yo»?',
        ['you', 'I'],
        'I',
        'I significa yo: la persona que está hablando.',
      ),
      FoundationCheck(
        'Ahora hablas con otra persona. ¿Qué palabra significa «tú»?',
        ['I', 'you'],
        'you',
        'You señala a la persona con quien hablas: tú.',
      ),
    ],
  ),
  FoundationUnit(
    'i-am',
    'Digo mi nombre',
    'Presentarte con una frase corta.',
    ['i-you'],
    [
      FoundationCard(
        'I am',
        'yo soy',
        'Ya conoces I: yo. Para decir quién soy, añado am. I am significa yo soy en esta presentación.',
        'self',
      ),
      FoundationCard(
        'I am Ana.',
        'Soy Ana.',
        'Ana es un nombre de ejemplo. La frase tiene tres partes: I + am + nombre. Am es una forma del verbo be: aquí expresa ser.',
        'self',
      ),
    ],
    [
      FoundationCheck(
        'Elige el modelo para decir «Soy Ana».',
        ['Ana am I.', 'I am Ana.'],
        'I am Ana.',
        'Primero I, después am y al final el nombre: I am Ana.',
      ),
      FoundationCheck(
        'En «I am Ana», ¿qué expresa «I am»?',
        ['Yo soy', 'Tú'],
        'Yo soy',
        'En una presentación, I am expresa yo soy. No hace falta memorizar todas las formas de be ahora.',
      ),
    ],
  ),
  FoundationUnit(
    'you-are',
    'Hablo contigo',
    'Decir quién es la persona con quien hablas.',
    ['i-am'],
    [
      FoundationCard(
        'you are',
        'tú eres',
        'Ya conoces you: tú. Con you usamos are. Aprende las dos palabras juntas: you are.',
        'you',
      ),
      FoundationCard(
        'You are Leo.',
        'Tú eres Leo.',
        'Leo es otro nombre de ejemplo. Si hablo de mí: I am Ana. Si hablo contigo: You are Leo.',
        'you',
      ),
    ],
    [
      FoundationCheck(
        'Hablas con Leo. ¿Cómo dices «Tú eres Leo»?',
        ['You am Leo.', 'You are Leo.'],
        'You are Leo.',
        'You va con are. I va con am. Son combinaciones distintas.',
      ),
      FoundationCheck(
        '¿Qué combinación significa «yo soy»?',
        ['you are', 'I am'],
        'I am',
        'I am habla de mí; you are habla de la persona con quien converso.',
      ),
    ],
  ),
  FoundationUnit(
    'he-she',
    'Presento a alguien',
    'Hablar de otra persona.',
    ['you-are'],
    [
      FoundationCard(
        'she',
        'ella',
        'Mia es una mujer de nuestro ejemplo. Para hablar de ella, usamos she.',
        'she',
      ),
      FoundationCard(
        'he',
        'él',
        'Leo es un hombre de nuestro ejemplo. Para hablar de él, usamos he.',
        'he',
      ),
      FoundationCard(
        'She is Mia. He is Leo.',
        'Ella es Mia. Él es Leo.',
        'Con she y he usamos is. Is también es una forma de be. Aquí significa es: she is, he is.',
        'pair',
      ),
    ],
    [
      FoundationCheck(
        '¿Qué frase significa «Ella es Mia»?',
        ['He is Mia.', 'She is Mia.'],
        'She is Mia.',
        'She significa ella. She is Mia significa Ella es Mia.',
      ),
      FoundationCheck(
        'Hablas de Leo: «Él es Leo». Elige la frase.',
        ['He is Leo.', 'He am Leo.'],
        'He is Leo.',
        'He significa él y va con is: He is Leo.',
      ),
    ],
  ),
  FoundationUnit(
    'feelings',
    'Digo cómo estoy',
    'Expresar dos estados sencillos.',
    ['he-she'],
    [
      FoundationCard(
        'happy',
        'feliz',
        'Esta palabra describe cómo te sientes. Primero aprende su significado: happy, feliz.',
        'happy',
      ),
      FoundationCard(
        'tired',
        'cansado o cansada',
        'Tired significa cansado o cansada. La palabra inglesa no cambia según quién habla.',
        'tired',
      ),
      FoundationCard(
        'I am happy. I am tired.',
        'Estoy feliz. Estoy cansado/a.',
        'Ya conoces I am. Antes decía quién soy; ahora expresa cómo estoy. Be puede expresar ser o estar según el contexto.',
        'happy',
      ),
    ],
    [
      FoundationCheck(
        '¿Qué frase significa «Estoy feliz»?',
        ['I am tired.', 'I am happy.'],
        'I am happy.',
        'Happy significa feliz. I am happy expresa cómo te sientes.',
      ),
      FoundationCheck(
        '¿Qué significa «I am tired»?',
        ['Estoy feliz', 'Estoy cansado/a'],
        'Estoy cansado/a',
        'Tired significa cansado o cansada. No cambies am: con I seguimos usando am.',
      ),
    ],
  ),
  FoundationUnit(
    'introduce',
    'Mi primera presentación',
    'Combinar tu nombre y cómo estás.',
    ['feelings'],
    [
      FoundationCard(
        'I am Ana. I am happy.',
        'Soy Ana. Estoy feliz.',
        'Son dos frases con palabras que ya aprendiste: primero quién eres; después cómo estás. Puedes usar un nombre inventado.',
        'self',
      ),
    ],
    [
      FoundationCheck(
        'Ordena las palabras para decir «Soy Ana».',
        ['Ana.', 'I', 'am'],
        'I am Ana.',
        'La persona va primero: I. Luego am. Después el nombre: Ana.',
        order: true,
      ),
      FoundationCheck(
        'Ahora forma «Estoy feliz».',
        ['happy.', 'am', 'I'],
        'I am happy.',
        'Reutilizas I am y añades happy. Puedes decir la frase en voz alta para practicar.',
        order: true,
      ),
    ],
  ),
];
String foundationKey(FoundationUnit unit, int question) =>
    'foundation-v1-${unit.id}-$question';
bool foundationPracticed(FoundationUnit unit, Map<String, dynamic> evidence) =>
    List.generate(
      unit.checks.length,
      (i) => evidence[foundationKey(unit, i)],
    ).every((e) => e is Map && e['resueltaConApoyo'] == true);
bool foundationAvailable(FoundationUnit unit, Map<String, dynamic> evidence) =>
    unit.requires.every(
      (id) => foundationPracticed(
        foundationUnits.firstWhere((u) => u.id == id),
        evidence,
      ),
    );
