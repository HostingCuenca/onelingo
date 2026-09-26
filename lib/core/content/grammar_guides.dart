/// Guías introductorias: niveles internos, no certificación de dominio.
class GrammarCheck {
  const GrammarCheck(this.prompt, this.options, this.answer, this.feedback);
  final String prompt, feedback;
  final List<String> options;
  final int answer;
}

class GrammarGuide {
  const GrammarGuide(
    this.id,
    this.level,
    this.title,
    this.goal,
    this.rule,
    this.examples,
    this.commonError,
    this.checks,
  );
  final String id, title, goal, rule, commonError;
  final int level;
  final List<(String, String)> examples;
  final List<GrammarCheck> checks;
}

List<GrammarGuide> grammarForLevel(int level) =>
    grammarGuides.where((g) => g.level == level).toList(growable: false);
const grammarGuides = <GrammarGuide>[
  GrammarGuide(
    "be",
    1,
    "Presentarte con be",
    "Decir quién eres y cómo estás.",
    "Usa I am; he/she/it is; you/we/they are. Añade not para negar. En preguntas, coloca be delante del sujeto. En inglés normalmente no omitimos el sujeto.",
    [("I am ready. Is she ready?", "Estoy listo/a. ¿Ella está lista?")],
    "No digas I is ready. Di I am ready.",
    [
      GrammarCheck(
        "My name ___ Leo.",
        ["am", "is", "are"],
        1,
        "My name equivale a it: usamos is.",
      ),
      GrammarCheck(
        "Elige la pregunta neutral correcta.",
        ["Are you tired?", "Is you tired?", "Do you are tired?"],
        0,
        "Con be invertimos verbo y sujeto: Are you tired?",
      ),
    ],
  ),
  GrammarGuide(
    "pronouns-possessives",
    1,
    "Personas y posesión",
    "Identificar a alguien y decir de quién es algo.",
    "I, you, he, she, it, we y they pueden ser sujeto. My, your, his, her, its, our y their van delante del sustantivo para expresar posesión. No añadas artículo antes del posesivo.",
    [
      (
        "She is my friend. Her name is Lina.",
        "Ella es mi amiga. Se llama Lina.",
      ),
    ],
    "No digas the my bag. Usa my bag.",
    [
      GrammarCheck(
        "Leo has a sister. ___ sister is a nurse.",
        ["Her", "His", "He"],
        1,
        "Leo es el poseedor: his sister.",
      ),
      GrammarCheck(
        "Elige una frase completa.",
        [
          "They are our neighbours.",
          "Their are we neighbours.",
          "They are the our neighbours.",
        ],
        0,
        "They es sujeto; our indica de quiénes son los vecinos.",
      ),
    ],
  ),
  GrammarGuide(
    "order",
    1,
    "Construir una oración",
    "Unir sujeto, verbo y complemento.",
    "Una afirmación básica suele seguir sujeto + verbo + complemento. Los adjetivos van antes del sustantivo. Usa a/an con un singular contable no específico: an va antes de un sonido vocálico.",
    [("I have a red bag.", "Tengo una bolsa roja.")],
    "No digas a bag red. Di a red bag.",
    [
      GrammarCheck(
        "Elige una oración natural.",
        ["I have a blue pen.", "Have pen blue I.", "I a blue pen have."],
        0,
        "I es sujeto, have es verbo y a blue pen es complemento.",
      ),
      GrammarCheck(
        "He is ___ artist.",
        ["a", "an", "are"],
        1,
        "Artist comienza por sonido vocálico: an artist.",
      ),
    ],
  ),
  GrammarGuide(
    "articles-plurals",
    1,
    "Artículos y plurales",
    "Presentar algo nuevo y volver a hablar de ello.",
    "Usa a/an para presentar un singular contable no identificado; usa the cuando ya sabemos cuál es. Los plurales generales normalmente van sin artículo. Muchos plurales añaden -s/-es; algunos cambian, como child → children. A/an depende del sonido inicial: an apple, a university.",
    [
      (
        "I saw a dog. The dog was friendly.",
        "Vi un perro. El perro era amigable.",
      ),
      ("Children need time to play.", "Los niños necesitan tiempo para jugar."),
    ],
    "No digas a books: a/an solo acompaña singular. No añadas -s a children.",
    [
      GrammarCheck(
        "Ves un gato por primera vez: I can see ___ cat.",
        ["the", "a", "an"],
        1,
        "Presentamos un gato no identificado con a; cat empieza por sonido consonántico.",
      ),
      GrammarCheck(
        "Un niño, dos niños: one child, two ___.",
        ["childs", "child", "children"],
        2,
        "Children ya es el plural irregular de child.",
      ),
    ],
  ),

  GrammarGuide(
    "there-be",
    1,
    "Describir lo que hay",
    "Indicar la presencia de objetos o personas.",
    "There is presenta un singular o incontable; there are presenta un plural. Pregunta con Is there/Are there. Para negar usa there is not/there are not. La construcción significa hay, no allí.",
    [
      (
        "There is a desk. There are two chairs.",
        "Hay un escritorio. Hay dos sillas.",
      ),
    ],
    "No digas There is two chairs en una descripción formal básica: usa are con plural.",
    [
      GrammarCheck(
        "There ___ three windows in this room.",
        ["is", "am", "are"],
        2,
        "Three windows es plural: there are.",
      ),
      GrammarCheck(
        "___ a bank near here?",
        ["Is there", "Are there", "There is"],
        0,
        "Para preguntar por un banco singular invertimos is y there.",
      ),
    ],
  ),
  GrammarGuide(
    "object-possessive",
    2,
    "Pronombres: a quién y de quién",
    "Evitar repetir nombres sin perder el significado.",
    "Usa me, you, him, her, it, us y them como objeto del verbo o después de una preposición. My/your/his/her/our/their necesitan sustantivo; mine/yours/his/hers/ours/theirs pueden sustituirlo. His tiene la misma forma en ambos usos.",
    [
      (
        "Ana knows him. This is her bag.",
        "Ana lo conoce. Esta es su bolsa (de ella).",
      ),
      (
        "This bag is mine; that one is yours.",
        "Esta bolsa es mía; aquella es tuya.",
      ),
    ],
    "No digas mine bag ni This bag is my. Usa my bag o This bag is mine.",
    [
      GrammarCheck(
        "Hablo de Leo: I can help ___.",
        ["he", "his", "him"],
        2,
        "Leo recibe la ayuda; usamos el pronombre objeto him.",
      ),
      GrammarCheck(
        "Esta bicicleta me pertenece: This bike is ___.",
        ["my", "mine", "me"],
        1,
        "Mine sustituye my bike; no necesita un sustantivo después.",
      ),
    ],
  ),

  GrammarGuide(
    "present",
    2,
    "Rutinas en presente",
    "Contar hábitos y preguntar por ellos.",
    "Usa presente simple para hábitos. Con he/she/it añade -s o -es en afirmativas. Para negar usa do not/does not + verbo base. Para preguntar: Do/Does + sujeto + verbo base.",
    [("She works at home. Does he cook?", "Ella trabaja en casa. ¿Él cocina?")],
    "No digas Does she works? Después de does usamos work.",
    [
      GrammarCheck(
        "Tom ___ English every evening.",
        ["study", "studies", "studying"],
        1,
        "Con Tom (he), study cambia a studies.",
      ),
      GrammarCheck(
        "She does not ___ coffee.",
        ["drinks", "drinking", "drink"],
        2,
        "Does not ya marca tercera persona; el verbo queda en forma base.",
      ),
    ],
  ),
  GrammarGuide(
    "questions",
    2,
    "Preguntar con auxiliares",
    "Obtener información sin omitir partes de la pregunta.",
    "Cuando preguntas por un complemento de un verbo principal en presente, usa palabra interrogativa + do/does + sujeto + verbo base. Con be invierte be y sujeto. Si who o what es el sujeto, normalmente no añadas do/does en una pregunta afirmativa neutral: Who lives here? Where pregunta lugar; when momento; why motivo; how manera.",
    [
      (
        "Where does Eva work? Where is Eva?",
        "¿Dónde trabaja Eva? ¿Dónde está Eva?",
      ),
    ],
    "No digas Where she works? como pregunta directa. Usa Where does she work?",
    [
      GrammarCheck(
        "___ does your brother live? In Cuenca.",
        ["When", "Where", "Why"],
        1,
        "La respuesta da un lugar, por eso preguntamos where.",
      ),
      GrammarCheck(
        "Elige la pregunta directa correcta.",
        [
          "What time he starts?",
          "What time does he starts?",
          "What time does he start?",
        ],
        2,
        "Does marca persona y el verbo queda start.",
      ),
    ],
  ),
  GrammarGuide(
    "ability",
    2,
    "Capacidades con can y could",
    "Decir lo que puedes hacer ahora y lo que podías hacer antes.",
    "Can + verbo base expresa capacidad presente. Cannot/can’t niega esa capacidad. Could expresa capacidad general en el pasado. Para preguntas invierte can/could y sujeto, sin do. Para un logro concreto pasado suele ser mejor was/were able to o managed to; aquí practicamos capacidad general.",
    [
      ("I can swim, but I cannot dive.", "Puedo nadar, pero no puedo bucear."),
      (
        "When I was young, I could run fast.",
        "Cuando era joven, podía correr rápido.",
      ),
    ],
    "No digas She cans swim ni She can to swim: usa She can swim.",
    [
      GrammarCheck(
        "Mara sabe nadar: She can ___.",
        ["swim", "to swim", "swims"],
        0,
        "Después de can va el verbo base swim, sin to ni -s.",
      ),
      GrammarCheck(
        "Capacidad general de niño: When I was six, I ___ read simple stories.",
        ["can", "could", "could to"],
        1,
        "Could expresa esa capacidad general en el pasado.",
      ),
    ],
  ),

  GrammarGuide(
    "frequency",
    2,
    "Expresar frecuencia",
    "Explicar cuándo realizas tus rutinas.",
    "Usually, often y never suelen ir antes del verbo principal, pero después de be. Never ya expresa negación: no añadas not. Every day suele ir al final.",
    [
      (
        "I usually walk. She is always friendly.",
        "Normalmente camino. Ella siempre es amable.",
      ),
    ],
    "No digas I do not never walk para expresar nunca. Di I never walk.",
    [
      GrammarCheck(
        "Elige el orden neutral.",
        [
          "We often read at night.",
          "We often reading at night.",
          "We are often read at night.",
        ],
        0,
        "Often va antes del verbo principal read.",
      ),
      GrammarCheck(
        "He ___ late.",
        ["never is not", "is never", "does never is"],
        1,
        "Con be colocamos never después: is never late.",
      ),
    ],
  ),
  GrammarGuide(
    "time-place",
    2,
    "Situar acciones y objetos",
    "Usar referencias frecuentes de tiempo y lugar.",
    "Para tiempo usa at con horas, on con días o fechas e in con meses y años. Para lugar, in indica interior o área; on una superficie; at un punto o lugar de actividad. Son patrones básicos con expresiones particulares que aprenderás en contexto.",
    [
      (
        "We meet on Monday at six. The keys are on the table.",
        "Nos reunimos el lunes a las seis. Las llaves están sobre la mesa.",
      ),
    ],
    "No digas in Monday para el día: usa on Monday.",
    [
      GrammarCheck(
        "The lesson starts ___ 8:15.",
        ["in", "on", "at"],
        2,
        "Una hora concreta lleva at.",
      ),
      GrammarCheck(
        "La leche está dentro de la nevera: The milk is ___ the fridge.",
        ["in", "on", "at"],
        0,
        "Hablamos del interior de la nevera: in.",
      ),
    ],
  ),
  GrammarGuide(
    "past-be",
    3,
    "Describir el pasado con was y were",
    "Contar dónde estabas y cómo era una situación.",
    "El pasado de be es was con I/he/she/it y were con you/we/they. No necesitas did para negar ni preguntar con be: Was she...? They were not...",
    [
      (
        "I was tired. Were they at home?",
        "Estaba cansado/a. ¿Estaban en casa?",
      ),
    ],
    "No digas Did you were late? Usa Were you late?",
    [
      GrammarCheck(
        "We ___ at the museum yesterday.",
        ["was", "were", "are"],
        1,
        "We exige were en pasado.",
      ),
      GrammarCheck(
        "Elige una pregunta correcta sobre ayer.",
        ["Did she was ill?", "Was she ill?", "Does she was ill?"],
        1,
        "Be forma su pregunta sin did: Was she ill?",
      ),
    ],
  ),
  GrammarGuide(
    "past",
    3,
    "Contar lo que pasó",
    "Narrar acciones terminadas.",
    "El pasado simple describe acciones en tiempos terminados. Los regulares suelen llevar -ed; aprende las formas irregulares, como go → went. En preguntas y negaciones usa did/did not + verbo base.",
    [
      (
        "We visited Quito yesterday. Did you go?",
        "Visitamos Quito ayer. ¿Fuiste?",
      ),
    ],
    "No digas Did you went? Di Did you go?",
    [
      GrammarCheck(
        "Yesterday, Ana ___ a book.",
        ["buys", "bought", "buy"],
        1,
        "Buy es irregular: su pasado es bought.",
      ),
      GrammarCheck(
        "They did not ___ the museum.",
        ["visited", "visiting", "visit"],
        2,
        "Después de did not usamos visit, sin marca de pasado.",
      ),
    ],
  ),
  GrammarGuide(
    "continuous",
    3,
    "Acciones en curso",
    "Distinguir una acción actual de una rutina.",
    "Usa am/is/are + verbo -ing para acciones en curso. El presente simple expresa hábitos. Verbos de estado como know normalmente no se usan en continuo en su significado habitual.",
    [
      (
        "I am reading now. I read every morning.",
        "Estoy leyendo ahora. Leo cada mañana.",
      ),
    ],
    "No digas She working now: falta is.",
    [
      GrammarCheck(
        "Listen! The baby ___.",
        ["is crying", "cry", "is cry"],
        0,
        "Listen señala algo que ocurre ahora: is crying.",
      ),
      GrammarCheck(
        "I ___ the answer.",
        ["am knowing", "know", "knowing"],
        1,
        "Know describe un estado; aquí usamos presente simple.",
      ),
    ],
  ),
  GrammarGuide(
    "future-plans",
    3,
    "Hablar de planes",
    "Explicar una intención y reconocer un acuerdo futuro.",
    "Usa be going to + verbo base para intenciones previas. El presente continuo con referencia futura puede expresar un acuerdo organizado. Will es habitual en decisiones tomadas en el momento. Las formas pueden solaparse: aquí practicamos contextos claros, no una regla absoluta.",
    [
      (
        "I am going to study tonight. We are meeting the tutor at five.",
        "Voy a estudiar esta noche. Nos reunimos con el tutor a las cinco.",
      ),
    ],
    "No omitas be: I going to study necesita am.",
    [
      GrammarCheck(
        "She ___ going to call her teacher.",
        ["are", "is", "does"],
        1,
        "Going to requiere be; con she usamos is.",
      ),
      GrammarCheck(
        "Ya decidí aprender francés: I am going to ___.",
        ["learning French", "learn French", "learned French"],
        1,
        "Después de going to va verbo base: learn.",
      ),
    ],
  ),
  GrammarGuide(
    "quantity",
    4,
    "Cantidades: much y many",
    "Preguntar por cantidades contables e incontables.",
    "Many acompaña plurales contables; much acompaña incontables. A lot of sirve con ambos. A few indica una pequeña cantidad contable; a little una pequeña cantidad incontable.",
    [
      (
        "How many chairs? There is a little milk.",
        "¿Cuántas sillas? Hay un poco de leche.",
      ),
    ],
    "No digas many water. En este uso water es incontable.",
    [
      GrammarCheck(
        "How ___ time do we have?",
        ["many", "much", "a few"],
        1,
        "Time es incontable aquí: much time.",
      ),
      GrammarCheck(
        "We need a ___ eggs.",
        ["little", "much", "few"],
        2,
        "Eggs es plural contable: a few eggs.",
      ),
    ],
  ),
  GrammarGuide(
    "comparisons",
    4,
    "Comparar opciones",
    "Elegir y justificar una opción con comparativos.",
    "Muchos adjetivos cortos forman comparativo con -er; los más largos usan more. Usa than para introducir la comparación. Good → better y bad → worse son irregulares. Para igualdad: as + adjetivo + as.",
    [
      (
        "This room is smaller than mine. This route is as safe as that one.",
        "Esta habitación es más pequeña que la mía. Esta ruta es tan segura como aquella.",
      ),
    ],
    "No digas more cheaper: usa cheaper.",
    [
      GrammarCheck(
        "This bag is ___ than that one.",
        ["more cheap", "cheaper", "cheapest"],
        1,
        "Cheap forma comparativo con -er y se combina con than.",
      ),
      GrammarCheck(
        "Igualdad: This chair is as ___ as that chair.",
        ["comfortable", "more comfortable", "comfortabler"],
        0,
        "As...as necesita el adjetivo sin comparativo.",
      ),
    ],
  ),
  GrammarGuide(
    "advice",
    4,
    "Consejos con should",
    "Dar consejos sin convertirlos en órdenes.",
    "Usa should + verbo base para aconsejar. La negación es should not. No añadas to ni -s al verbo. Para preguntar: Should + sujeto + verbo base.",
    [
      (
        "You should rest. Should we call her?",
        "Deberías descansar. ¿Deberíamos llamarla?",
      ),
    ],
    "No digas He should to sleep. Di He should sleep.",
    [
      GrammarCheck(
        "You should ___ more water.",
        ["drink", "to drink", "drinks"],
        0,
        "Should se combina con verbo base: drink.",
      ),
      GrammarCheck(
        "Elige el consejo negativo.",
        [
          "You not should rush.",
          "You should not rush.",
          "You should not to rush.",
        ],
        1,
        "Not va después de should; rush queda en forma base.",
      ),
    ],
  ),
  GrammarGuide(
    "obligation",
    4,
    "Obligación y prohibición",
    "Distinguir lo obligatorio de lo opcional y lo prohibido.",
    "Have to expresa necesidad u obligación. Must not indica prohibición; do not have to significa que algo no es necesario. No confundir falta de obligación con prohibición. Después de must usa verbo base.",
    [
      (
        "You must not park here. You do not have to book.",
        "No debes estacionar aquí. No es necesario reservar.",
      ),
    ],
    "You do not have to pay no significa que esté prohibido pagar.",
    [
      GrammarCheck(
        "Entrada gratuita: You ___ pay.",
        ["must not", "do not have to", "have to"],
        1,
        "Gratis significa que no hay obligación de pagar.",
      ),
      GrammarCheck(
        "El reglamento prohíbe fumar: You ___ smoke here.",
        ["do not have to", "must not", "must"],
        1,
        "Must not expresa prohibición, no simplemente ausencia de obligación.",
      ),
    ],
  ),
  GrammarGuide(
    "verb-patterns",
    4,
    "Encadenar dos verbos",
    "Elegir -ing o infinitivo después de verbos frecuentes.",
    "Algunos verbos requieren -ing: enjoy, avoid, finish. Otros usan to + verbo: decide, hope, plan. Aprende el patrón con el verbo, no solo su traducción. Después de una preposición usamos normalmente -ing.",
    [
      (
        "I enjoy reading. We decided to leave.",
        "Disfruto leer. Decidimos irnos.",
      ),
    ],
    "No digas enjoy to read en este uso; usa enjoy reading.",
    [
      GrammarCheck(
        "She avoided ___ during the meeting.",
        ["to interrupt", "interrupting", "interrupt"],
        1,
        "Avoid se combina con forma -ing.",
      ),
      GrammarCheck(
        "They hope ___ soon.",
        ["returning", "return", "to return"],
        2,
        "Hope se combina con to + verbo base.",
      ),
    ],
  ),
  GrammarGuide(
    "past-continuous",
    5,
    "Narrar acciones interrumpidas",
    "Combinar el fondo de una historia y un suceso.",
    "Usa was/were + -ing para una acción en curso en el pasado. El pasado simple puede indicar el suceso que ocurre durante ella. When y while ayudan a organizar la secuencia, pero el sentido del contexto determina el tiempo.",
    [
      (
        "I was cooking when the phone rang.",
        "Estaba cocinando cuando sonó el teléfono.",
      ),
    ],
    "No digas I were cooking: con I se usa was.",
    [
      GrammarCheck(
        "At that moment, they ___ waiting outside.",
        ["was", "were", "did"],
        1,
        "They exige were y waiting expresa acción en curso.",
      ),
      GrammarCheck(
        "Una llamada interrumpe: I was reading when the phone ___.",
        ["rang", "was ring", "ringing"],
        0,
        "Rang es el suceso puntual que ocurre durante la lectura.",
      ),
    ],
  ),
  GrammarGuide(
    "perfect",
    5,
    "Conectar pasado y presente",
    "Expresar duración y experiencias.",
    "Present perfect: have/has + participio. Since introduce el punto inicial; for expresa duración. Se usa para experiencias sin fecha terminada o situaciones que continúan. Con yesterday normalmente usamos pasado simple.",
    [("I have lived here for two years.", "Vivo aquí desde hace dos años.")],
    "No digas since three years. Di for three years.",
    [
      GrammarCheck(
        "We have worked together ___ March.",
        ["for", "since", "during three"],
        1,
        "March indica el punto inicial: since March.",
      ),
      GrammarCheck(
        "I ___ him yesterday.",
        ["have seen", "saw", "have see"],
        1,
        "Yesterday es un tiempo terminado: saw.",
      ),
    ],
  ),
  GrammarGuide(
    "first-conditional",
    5,
    "Consecuencias posibles",
    "Explicar qué harás si ocurre una condición.",
    "Para una condición futura posible usa if + presente simple y will + verbo base en la consecuencia. También puede haber imperativos o modales. No añadas will a la condición en este patrón básico.",
    [
      (
        "If it rains tomorrow, we will stay inside.",
        "Si llueve mañana, nos quedaremos dentro.",
      ),
    ],
    "No digas If it will rain en esta condición básica: If it rains.",
    [
      GrammarCheck(
        "If she ___ early, we will have lunch together.",
        ["will arrive", "arrives", "arrived"],
        1,
        "La condición futura usa presente: arrives.",
      ),
      GrammarCheck(
        "If I finish tonight, I ___ you the report tomorrow.",
        ["sent", "will send", "sending"],
        1,
        "La consecuencia prevista usa will send.",
      ),
    ],
  ),
  GrammarGuide(
    "relative",
    5,
    "Precisar de quién hablas",
    "Describir personas y cosas con relativas.",
    "Who se refiere a personas y which a cosas. That puede sustituirlos en relativas que identifican al referente. No repitas un pronombre sujeto cuando who/which ya cumple esa función.",
    [
      (
        "The woman who lives next door is a nurse.",
        "La mujer que vive al lado es enfermera.",
      ),
    ],
    "No digas who she lives here. Who ya es sujeto.",
    [
      GrammarCheck(
        "The man ___ teaches us is Canadian.",
        ["which", "who", "where"],
        1,
        "El antecedente es una persona; who es sujeto de teaches.",
      ),
      GrammarCheck(
        "Elige la relativa correcta.",
        [
          "A phone which it works well.",
          "A phone which works well.",
          "A phone who works well.",
        ],
        1,
        "Which se refiere a la cosa y no necesita repetir it.",
      ),
    ],
  ),
  GrammarGuide(
    "passive-basic",
    5,
    "Elegir el foco de una frase",
    "Usar la pasiva para describir procesos y sucesos.",
    "La pasiva se forma con be en el tiempo adecuado + participio. Presenta primero quien recibe la acción. Añade by + agente cuando es importante. No todos los verbos admiten pasiva: hace falta un objeto que pueda pasar a sujeto.",
    [
      (
        "The bridge was built in 1998. The rooms are cleaned daily.",
        "El puente fue construido en 1998. Las habitaciones se limpian a diario.",
      ),
    ],
    "No digas The bridge was build: el participio es built.",
    [
      GrammarCheck(
        "These emails ___ sent every morning.",
        ["are", "is", "was"],
        0,
        "Emails es plural y every morning indica rutina: are sent.",
      ),
      GrammarCheck(
        "Activa equivalente a The letter was written by Ana.",
        [
          "Ana wrote the letter.",
          "Ana was written the letter.",
          "The letter wrote Ana.",
        ],
        0,
        "Ana realiza la acción; en activa es el sujeto.",
      ),
    ],
  ),
  GrammarGuide(
    "past-perfect",
    6,
    "Ordenar dos momentos pasados",
    "Mostrar qué ocurrió antes de otro hecho pasado.",
    "Past perfect: had + participio. Marca anterioridad respecto a un momento pasado. No se usa automáticamente para todo lo antiguo; necesitamos ese punto de comparación. Aprende participios frecuentes: gone, seen, written.",
    [
      (
        "When I arrived, the train had left.",
        "Cuando llegué, el tren ya se había ido.",
      ),
    ],
    "No digas had went. Go tiene participio gone.",
    [
      GrammarCheck(
        "By the time we arrived, the film had ___.",
        ["begin", "began", "begun"],
        2,
        "Begin tiene participio begun; had requiere participio.",
      ),
      GrammarCheck(
        "The guests had left before I called. ¿Qué pasó primero?",
        [
          "The guests left.",
          "I called.",
          "Both happened at exactly the same time.",
        ],
        0,
        "Had left marca el hecho anterior a la llamada.",
      ),
    ],
  ),
  GrammarGuide(
    "second",
    6,
    "Imaginar otra realidad",
    "Expresar hipótesis presentes poco probables.",
    "Usa if + pasado simple, would + verbo base. Aquí el pasado expresa distancia de la realidad, no necesariamente tiempo pasado. If I were you es una expresión habitual para aconsejar.",
    [("If I had time, I would travel.", "Si tuviera tiempo, viajaría.")],
    "No digas If I would have time en esta estructura. Usa If I had time.",
    [
      GrammarCheck(
        "If she knew the answer, she ___ tell us.",
        ["will", "would", "has"],
        1,
        "La hipótesis usa knew y su consecuencia would tell.",
      ),
      GrammarCheck(
        "If I ___ you, I would wait.",
        ["were", "will be", "would be"],
        0,
        "If I were you presenta un consejo hipotético.",
      ),
    ],
  ),
  GrammarGuide(
    "third-conditional",
    6,
    "Imaginar un pasado diferente",
    "Relacionar una condición pasada irreal y su resultado.",
    "Usa if + had + participio, would have + participio. Imagina otra versión de un hecho pasado. Antes de mezclarlo con consecuencias presentes, comprueba que ambas partes aquí se refieren al pasado.",
    [
      (
        "If I had left earlier, I would have caught the bus.",
        "Si hubiera salido antes, habría alcanzado el autobús.",
      ),
    ],
    "No digas would have catch: necesitas caught.",
    [
      GrammarCheck(
        "If we had booked, we ___ found a table.",
        ["would have", "would", "will"],
        0,
        "El resultado pasado irreal usa would have found.",
      ),
      GrammarCheck(
        "If he ___ checked the address, he would have arrived on time.",
        ["would", "has", "had"],
        2,
        "La condición necesita past perfect: had checked.",
      ),
    ],
  ),
  GrammarGuide(
    "reported",
    6,
    "Contar lo que alguien dijo",
    "Transmitir declaraciones desde otro momento.",
    "En relatos posteriores con said a menudo desplazamos el tiempo hacia el pasado y ajustamos pronombres. Si el hecho sigue vigente, ese cambio no siempre es obligatorio. Tell admite objeto personal directo; say requiere to ante la persona.",
    [("She told me she was tired.", "Me dijo que estaba cansada.")],
    "Di She told me o She said to me; no She said me.",
    [
      GrammarCheck(
        "She ___ me that the shop was closed.",
        ["said", "told", "spoke"],
        1,
        "Tell admite objeto personal: told me.",
      ),
      GrammarCheck(
        "Ayer dijo “I am ill”. Relato con cambio de tiempo:",
        ["He said I am ill.", "He said he was ill.", "He told he ill."],
        1,
        "Ajustamos I a he y am a was en este relato posterior.",
      ),
    ],
  ),
  GrammarGuide(
    "reporting-questions",
    6,
    "Transmitir preguntas sin invertir",
    "Incorporar preguntas dentro de otra oración.",
    "En preguntas indirectas usa orden de afirmación: palabra interrogativa + sujeto + verbo. Para preguntas sí/no usa if o whether. No mantengas do/does/did del interrogativo directo si ya no hace falta.",
    [
      (
        "She asked where I lived. Do you know when it starts?",
        "Preguntó dónde vivía. ¿Sabes cuándo empieza?",
      ),
    ],
    "No digas Do you know where is he? Usa where he is.",
    [
      GrammarCheck(
        "Could you tell me where ___?",
        ["is the office", "the office is", "does the office"],
        1,
        "La pregunta incorporada conserva orden sujeto + verbo.",
      ),
      GrammarCheck(
        "He asked ___ I needed help.",
        ["that", "whether", "what"],
        1,
        "Whether introduce una pregunta sí/no indirecta.",
      ),
    ],
  ),
  GrammarGuide(
    "future-perfect",
    7,
    "Antes de una fecha límite",
    "Hablar de acciones terminadas antes de un momento futuro.",
    "El futuro perfecto usa will have + participio para una acción terminada antes de un momento futuro; by señala el límite. El futuro continuo usa will be + verbo -ing para una acción en curso en un momento futuro. Compara: At eight, I will be working (a esa hora estaré trabajando) y By eight, I will have finished (para esa hora habré terminado). Elegimos la forma según el significado, no solo por una palabra aislada.",
    [
      ("By Monday, I will have finished.", "Para el lunes, habré terminado."),
      ("At nine, we will be travelling.", "A las nueve, estaremos viajando."),
    ],
    "No digas will have finish. Usa el participio finished.",
    [
      GrammarCheck(
        "By noon, they will have ___.",
        ["arrive", "arrived", "arriving"],
        1,
        "Will have requiere participio: arrived.",
      ),
      GrammarCheck(
        "A las ocho estaré en pleno trabajo:",
        [
          "I will be working at eight.",
          "I will have finished by eight.",
          "I have work at eight.",
        ],
        0,
        "Acción en curso en el futuro: will be + -ing.",
      ),
    ],
  ),
  GrammarGuide(
    "passive",
    7,
    "Poner el resultado primero",
    "Combinar la voz pasiva y los tiempos perfectos.",
    "La pasiva usa be + participio. En present perfect: has/have been + participio. En futuro perfecto: will have been + participio. La elegimos para destacar la acción o resultado, no quien lo hizo.",
    [("The report has been checked.", "El informe ha sido revisado.")],
    "No omitas been cuando el informe recibe la acción.",
    [
      GrammarCheck(
        "The files have ___ saved.",
        ["being", "been", "be"],
        1,
        "La pasiva perfecta es have been saved.",
      ),
      GrammarCheck(
        "Pasiva: They will have completed the work.",
        [
          "The work will have been completed.",
          "The work will have complete.",
          "The work will been completing.",
        ],
        0,
        "El objeto pasa a sujeto y añadimos been antes del participio.",
      ),
    ],
  ),
  GrammarGuide(
    "relative-extra",
    7,
    "Añadir información con relativas",
    "Separar identificación y comentario adicional.",
    "Una relativa no identificativa añade información sobre alguien o algo ya identificado y se separa con comas. Usa who/which, no that, en esta construcción. Whose expresa posesión. Las comas cambian cómo se interpreta la información.",
    [
      (
        "Lina, who lives nearby, works here.",
        "Lina, que vive cerca, trabaja aquí.",
      ),
    ],
    "No uses that tras la coma en una relativa explicativa: Lina, who..., no Lina, that...",
    [
      GrammarCheck(
        "My laptop, ___ is five years old, still works.",
        ["that", "which", "who"],
        1,
        "La relativa adicional sobre una cosa usa which.",
      ),
      GrammarCheck(
        "The colleague ___ desk is next to mine is away.",
        ["who", "which", "whose"],
        2,
        "Whose vincula a la persona con su escritorio: posesión.",
      ),
    ],
  ),
  GrammarGuide(
    "cohesion",
    7,
    "Conectar argumentos con precisión",
    "Distinguir causa, contraste y consecuencia.",
    "Because introduce causa; therefore presenta consecuencia; however marca contraste. However no une por sí solo dos oraciones con una simple coma en escritura cuidada: usa punto o punto y coma. El conector debe reflejar la relación real entre ideas.",
    [
      (
        "The road was closed. Therefore, we took another route.",
        "La carretera estaba cerrada. Por eso tomamos otra ruta.",
      ),
    ],
    "No trates because y therefore como equivalentes: uno introduce causa y el otro consecuencia.",
    [
      GrammarCheck(
        "It was expensive. ___, it was worth the money.",
        ["Therefore", "However", "Because"],
        1,
        "La segunda idea contrasta con el precio alto.",
      ),
      GrammarCheck(
        "La carretera cerrada CAUSA el desvío: We changed route ___ the road was closed.",
        ["because", "however", "therefore"],
        0,
        "Because introduce la causa del cambio.",
      ),
    ],
  ),
  GrammarGuide(
    "mixed",
    8,
    "Pasado hipotético, efecto actual",
    "Conectar decisiones pasadas con consecuencias presentes.",
    "Usa if + past perfect para la condición pasada irreal y would + verbo base para la consecuencia presente. Una consecuencia pasada usaría would have + participio. Observa las referencias temporales.",
    [
      (
        "If I had studied medicine, I would be a doctor now.",
        "Si hubiera estudiado medicina, ahora sería médico/a.",
      ),
    ],
    "No uses would have be para un estado actual. Di would be now.",
    [
      GrammarCheck(
        "If we had saved more, we ___ own a flat now.",
        ["would", "would have", "had"],
        0,
        "La consecuencia es presente: would own now.",
      ),
      GrammarCheck(
        "Consecuencia pasada: If he had called, I ___ answered.",
        ["would", "would have", "will have"],
        1,
        "La consecuencia pasada usa would have answered.",
      ),
    ],
  ),
  GrammarGuide(
    "modal-deduction",
    8,
    "Deducir sin confundir certeza",
    "Expresar una conclusión probable sobre un hecho pasado.",
    "Must have + participio expresa una deducción fuerte, no obligación pasada. Might have expresa posibilidad. Cannot/can’t have indica una conclusión de imposibilidad según la evidencia disponible. Elige la fuerza de la afirmación con cuidado.",
    [
      (
        "She might have missed the bus.",
        "Puede que no haya alcanzado el autobús.",
      ),
    ],
    "Must have left significa deducción; no que alguien estaba obligado a salir.",
    [
      GrammarCheck(
        "Solo es una posibilidad: He ___ forgotten the appointment.",
        ["must have", "might have", "cannot have"],
        1,
        "Might have mantiene la incertidumbre indicada.",
      ),
      GrammarCheck(
        "The office is dark; they must have left. ¿Qué expresa?",
        [
          "A past obligation to leave",
          "A strong inference that they left",
          "A request for them to leave",
        ],
        1,
        "Must have + participio comunica deducción en este contexto.",
      ),
    ],
  ),
  GrammarGuide(
    "hedging",
    8,
    "Matizar afirmaciones",
    "Expresar incertidumbre con precisión.",
    "May/might + verbo base expresan posibilidad. Appear/seem + to + verbo suavizan una afirmación. Para posibilidad pasada usa may/might have + participio. No conviertas una posibilidad en certeza al reformular.",
    [
      (
        "The results may indicate a problem.",
        "Los resultados podrían indicar un problema.",
      ),
    ],
    "No digas may indicates. Después de may va indicate.",
    [
      GrammarCheck(
        "The evidence appears ___ this interpretation.",
        ["support", "to support", "supporting to"],
        1,
        "Appear se combina aquí con to + verbo base.",
      ),
      GrammarCheck(
        "Posibilidad pasada: They might ___ the date.",
        ["have forgotten", "forgot", "to forget"],
        0,
        "Might have + participio expresa posibilidad pasada.",
      ),
    ],
  ),
  GrammarGuide(
    "concession",
    8,
    "Conceder sin abandonar una idea",
    "Conectar una concesión con el argumento principal.",
    "Be that as it may es una expresión fija: aun así. Although introduce una oración; despite introduce normalmente un sustantivo o -ing. Despite the fact that permite continuar con una oración completa.",
    [
      (
        "Despite being tired, she continued.",
        "A pesar de estar cansada, continuó.",
      ),
    ],
    "No digas despite she was tired. Usa although she was tired o despite being tired.",
    [
      GrammarCheck(
        "Be that as it ___, the question remains.",
        ["may", "would", "can"],
        0,
        "La expresión fija es Be that as it may.",
      ),
      GrammarCheck(
        "___ the delay, we finished on time.",
        ["Although", "Despite", "Even though"],
        1,
        "The delay es un grupo nominal; corresponde despite.",
      ),
    ],
  ),
  GrammarGuide(
    "reference",
    9,
    "Evitar referencias ambiguas",
    "Revisar a qué persona o idea remite un pronombre.",
    "Una oración puede ser gramatical y aun así resultar ambigua. Repite el nombre o reformula cuando he/she/they/it podrían señalar más de un referente. This puede resumir una idea, pero conviene nombrarla si el lector puede confundirla con otra.",
    [
      (
        "After Eva called Sara, Sara sent the form.",
        "Después de que Eva llamó a Sara, Sara envió el formulario.",
      ),
    ],
    "Eva called Sara after she arrived no aclara por sí sola quién llegó. No adivines: reformula según la intención.",
    [
      GrammarCheck(
        "Se quiere decir que Sara envió el formulario. ¿Qué versión es más clara?",
        [
          "Eva called Sara, and she sent the form.",
          "Eva called Sara, and Sara sent the form.",
          "She called her, and she sent it.",
        ],
        1,
        "Repetir Sara elimina la ambigüedad entre las dos personas.",
      ),
      GrammarCheck(
        "Leo emailed Omar after he finished. Sin contexto, ¿quién terminó?",
        ["Definitely Leo", "Definitely Omar", "The pronoun is ambiguous"],
        2,
        "He puede remitir a ambos nombres; la oración sola no permite decidir.",
      ),
    ],
  ),
  GrammarGuide(
    "negative-inversion",
    9,
    "Énfasis con inversión",
    "Interpretar expresiones restrictivas formales.",
    "Al empezar con Never, Rarely u Only later, invertimos auxiliar y sujeto. Si no hay auxiliar visible en pasado simple, añade did y deja el verbo base. Con Not until, la inversión aparece en la oración principal.",
    [("Only later did I understand.", "Solo más tarde lo entendí.")],
    "No digas did I understood. Did exige understand.",
    [
      GrammarCheck(
        "Only then ___ they realise the risk.",
        ["did", "had", "were"],
        0,
        "Realise en forma base requiere did en esta inversión de pasado.",
      ),
      GrammarCheck(
        "Elige la oración correcta.",
        [
          "Never I have seen this.",
          "Never have I seen this.",
          "Never have seen I this.",
        ],
        1,
        "Have se coloca antes del sujeto I.",
      ),
    ],
  ),
  GrammarGuide(
    "condition-inversion",
    9,
    "Condiciones en registro formal",
    "Reconocer condiciones sin if.",
    "Had + sujeto + participio equivale a If + sujeto + had + participio. Conserva el significado hipotético. No añadas if a la estructura invertida.",
    [
      (
        "Had I known, I would have helped.",
        "Si lo hubiera sabido, habría ayudado.",
      ),
    ],
    "No mezcles If had I known. Usa If I had known o Had I known.",
    [
      GrammarCheck(
        "Reformula If we had seen it: ___ it...",
        ["Had we seen", "If had we seen", "We had see"],
        0,
        "La inversión mueve had delante del sujeto y elimina if.",
      ),
      GrammarCheck(
        "Had she asked, I ___ agreed.",
        ["will", "would have", "have"],
        1,
        "La condición pasada irreal combina con would have agreed.",
      ),
    ],
  ),
  GrammarGuide(
    "editing-register",
    10,
    "Revisar precisión y registro",
    "Mejorar claridad sin añadir complejidad innecesaria.",
    "Un registro formal no exige oraciones largas. Comprueba concordancia, referentes y relaciones lógicas. Mantén la fuerza de la evidencia: cambiar may por proves modifica el significado. Prefiere una formulación clara que conserve exactamente la intención.",
    [
      (
        "The findings may suggest a link; they do not establish a cause.",
        "Los hallazgos podrían sugerir una relación; no establecen una causa.",
      ),
    ],
    "No conviertas una relación posible en causalidad segura al “mejorar” el estilo.",
    [
      GrammarCheck(
        "Reescribe con la misma cautela: The results may indicate a problem.",
        [
          "The results prove there is a problem.",
          "The results suggest that there could be a problem.",
          "The results rule out a problem.",
        ],
        1,
        "Suggest y could conservan posibilidad, sin convertirla en prueba concluyente.",
      ),
      GrammarCheck(
        "Concordancia: Each of the proposals ___ a clear objective.",
        ["have", "has", "are having"],
        1,
        "El núcleo each es singular; corresponde has.",
      ),
    ],
  ),

  GrammarGuide(
    "were-it-not",
    10,
    "Hipótesis formales precisas",
    "Distinguir condiciones presentes y pasadas.",
    "Were it not for + sustantivo equivale a If it were not for: condición presente irreal. Had it not been for equivale a If it had not been for: condición pasada irreal. Combina la consecuencia con el tiempo que quieres expresar.",
    [
      (
        "Were it not for your help, I would be lost.",
        "Si no fuera por tu ayuda, estaría perdido/a.",
      ),
    ],
    "No intercambies presente y pasado solo porque ambas estructuras suenan formales.",
    [
      GrammarCheck(
        "Hipótesis actual: ___ your support, I would be struggling now.",
        ["Were it not for", "If had it not for", "Were it not been for"],
        0,
        "Were it not for introduce la condición irreal actual.",
      ),
      GrammarCheck(
        "Had it not been for the warning, we ___ made a mistake.",
        ["would", "would have", "will"],
        1,
        "La consecuencia pasada necesita would have made.",
      ),
    ],
  ),
];
