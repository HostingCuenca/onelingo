import 'package:flutter/material.dart';

import '../../app/theme.dart';
import '../models/models.dart';
import 'contenido_json.dart';
import 'fundamentos.dart';
import 'fotos.dart';
import 'idiomas.dart';

/// Los 10 idiomas del contrato, en el orden acordado con el cliente.
const idiomas = [
  Language(code: 'en', nombre: 'Inglés', nombreNativo: 'English'),
  Language(code: 'es', nombre: 'Español', nombreNativo: 'Español'),
  Language(code: 'fr', nombre: 'Francés', nombreNativo: 'Français'),
  Language(code: 'de', nombre: 'Alemán', nombreNativo: 'Deutsch'),
  Language(code: 'pt', nombre: 'Portugués', nombreNativo: 'Português'),
  Language(code: 'it', nombre: 'Italiano', nombreNativo: 'Italiano'),
  Language(code: 'zh', nombre: 'Chino mandarín', nombreNativo: '普通话'),
  Language(code: 'ja', nombre: 'Japonés', nombreNativo: '日本語'),
  Language(code: 'ko', nombre: 'Coreano', nombreNativo: '한국어'),
  Language(code: 'ru', nombre: 'Ruso', nombreNativo: 'Русский'),
];

Language idioma(String code) => idiomas.firstWhere((l) => l.code == code);

/// Los 10 niveles tal como los definió el cliente.
const niveles = [
  Level(
    numero: 1,
    nombre: 'Básico',
    descripcion: 'Las bases del idioma: saludos, números, familia, presente simple.',
    temario: [
      'Pronombres personales', 'Saludos y presentaciones', 'Alfabeto y sonidos',
      'Números', 'Colores', 'Días, meses y fechas', 'Familia', 'Casa',
      'Objetos cotidianos', 'Comida y bebidas', 'Ropa', 'Partes del cuerpo',
      'Lugares comunes', 'Verbo ser/estar', 'Verbo tener', 'Verbos básicos',
      'Presente simple', 'Preguntas y negaciones', 'Artículos y preposiciones',
      'Conversaciones sencillas',
    ],
  ),
  Level(
    numero: 2,
    nombre: 'Básico',
    descripcion: 'Amplía las bases: pasado y futuro básicos, posesivos, vida diaria.',
    temario: [
      'Verbos frecuentes', 'Conjugación', 'Presente', 'Pasado básico',
      'Futuro básico', 'Preguntas y respuestas', 'Negaciones',
      'Pronombres y posesivos', 'Adjetivos', 'Adverbios básicos', 'Preposiciones',
      'Construcción de frases', 'Expresiones cotidianas', 'Listening', 'Lectura',
      'Escritura', 'Pronunciación', 'Conversaciones básicas',
      'Situaciones de la vida diaria', 'Repaso del nivel',
    ],
  ),
  Level(
    numero: 3,
    nombre: 'Básico Avanzado',
    descripcion: 'Hacia conversaciones naturales: irregulares, continuo, comparaciones.',
    temario: [
      'Verbos regulares e irregulares', 'Pasado', 'Futuro', 'Presente continuo',
      'Comparaciones', 'Cantidades', 'Expresiones frecuentes',
      'Preguntas más complejas', 'Párrafos sencillos', 'Gramática intermedia inicial',
      'Listening', 'Lectura', 'Escritura', 'Pronunciación', 'Conversación',
      'Situaciones reales', 'Comprensión de conversaciones', 'Vocabulario ampliado',
      'Práctica integrada', 'Repaso del nivel',
    ],
  ),
  Level(
    numero: 4,
    nombre: 'Intermedio',
    descripcion: 'Desenvolverse en situaciones reales: trabajo, viajes, opiniones.',
    temario: [
      'Gramática intermedia', 'Tiempos verbales', 'Verbos irregulares',
      'Expresiones comunes', 'Vocabulario cotidiano ampliado',
      'Conversaciones más largas', 'Listening', 'Lectura', 'Escritura',
      'Pronunciación', 'Situaciones laborales', 'Viajes', 'Problemas cotidianos',
      'Expresar opiniones', 'Hacer preguntas', 'Explicar situaciones',
      'Mantener conversaciones', 'Práctica integrada', 'Simulaciones', 'Repaso del nivel',
    ],
  ),
  Level(
    numero: 5,
    nombre: 'Intermedio',
    descripcion: 'Comunicarse con independencia: historias, vida profesional y social.',
    temario: [
      'Gramática intermedia avanzada', 'Vocabulario amplio',
      'Verbos y expresiones avanzadas', 'Conversaciones naturales', 'Listening',
      'Lectura de textos largos', 'Escritura', 'Pronunciación', 'Expresar opiniones',
      'Explicar situaciones', 'Contar historias', 'Situaciones profesionales',
      'Conversaciones sociales', 'Resolver problemas', 'Conversación con IA',
      'Práctica integrada', 'Simulaciones', 'Debate inicial', 'Presentaciones cortas',
      'Repaso del nivel',
    ],
  ),
  Level(
    numero: 6,
    nombre: 'Intermedio Avanzado',
    descripcion: 'Bastante fluidez: phrasal verbs, negociaciones y debates sencillos.',
    temario: [
      'Gramática avanzada', 'Vocabulario avanzado', 'Expresiones naturales',
      'Phrasal verbs', 'Tiempos verbales combinados', 'Conversaciones largas',
      'Listening avanzado', 'Lectura avanzada', 'Escritura', 'Pronunciación',
      'Situaciones profesionales', 'Negociaciones sencillas',
      'Opiniones complejas', 'Explicar problemas', 'Debates sencillos',
      'Conversaciones espontáneas', 'Práctica integrada', 'Simulaciones',
      'Presentaciones', 'Repaso del nivel',
    ],
  ),
  Level(
    numero: 7,
    nombre: 'Avanzado',
    descripcion: 'Comunicación avanzada: modismos, argumentación, entrevistas.',
    temario: [
      'Gramática avanzada', 'Vocabulario avanzado', 'Expresiones idiomáticas',
      'Conversaciones complejas', 'Debates', 'Opiniones', 'Argumentación',
      'Situaciones profesionales', 'Presentaciones', 'Entrevistas',
      'Listening avanzado', 'Lectura avanzada', 'Escritura avanzada',
      'Pronunciación', 'Conversación espontánea', 'Práctica integrada',
      'Simulaciones', 'Textos de opinión', 'Cultura y contexto', 'Repaso del nivel',
    ],
  ),
  Level(
    numero: 8,
    nombre: 'Avanzado',
    descripcion: 'Fluidez y naturalidad: vocabulario especializado, distintas velocidades.',
    temario: [
      'Conversación avanzada', 'Expresiones idiomáticas', 'Vocabulario especializado',
      'Gramática avanzada', 'Conversaciones profesionales', 'Debates',
      'Presentaciones', 'Entrevistas de trabajo', 'Negociaciones',
      'Distintas velocidades de habla', 'Lectura avanzada', 'Escritura avanzada',
      'Pronunciación', 'Conversaciones espontáneas', 'Práctica integrada',
      'Simulaciones', 'Acentos y registros', 'Humor y matices', 'Textos técnicos',
      'Repaso del nivel',
    ],
  ),
  Level(
    numero: 9,
    nombre: 'Avanzado Superior',
    descripcion: 'Conversaciones complejas y naturales en contextos académicos y laborales.',
    temario: [
      'Vocabulario especializado', 'Expresiones naturales', 'Modismos',
      'Gramática avanzada', 'Conversaciones complejas', 'Debates', 'Argumentación',
      'Presentaciones profesionales', 'Negociaciones', 'Situaciones académicas',
      'Situaciones laborales', 'Listening avanzado', 'Lectura avanzada',
      'Escritura avanzada', 'Pronunciación', 'Conversación libre',
      'Práctica integrada', 'Simulaciones', 'Textos académicos', 'Repaso del nivel',
    ],
  ),
  Level(
    numero: 10,
    nombre: 'Dominio',
    descripcion: 'Nivel máximo: simulación de situaciones reales y evaluaciones integrales.',
    temario: [
      'Conversación avanzada y natural', 'Vocabulario profesional',
      'Vocabulario especializado', 'Expresiones idiomáticas', 'Modismos',
      'Gramática avanzada', 'Debates', 'Argumentación', 'Presentaciones',
      'Entrevistas', 'Negociaciones', 'Situaciones profesionales',
      'Situaciones sociales', 'Listening avanzado', 'Lectura avanzada',
      'Escritura avanzada', 'Pronunciación', 'Conversación libre con IA',
      'Simulación de situaciones reales', 'Evaluaciones integrales',
    ],
  ),
];

Level nivel(int n) => n == 0 ? nivelFundamentos : niveles[n - 1];

/// Alias para usar dentro de widgets cuyo campo también se llama `nivel`.
Level nivelDe(int n) => nivel(n);

/// Lecciones que tiene un nivel: 100 en los niveles 1-10; el nivel 0 (Fundamentos) es variable.
int totalLeccionesDe(int n) => n == 0 ? leccionesDe(0).length : Level.totalLecciones;

IconData iconoUnidad(int numero) => _iconosUnidad[(numero - 1) % _iconosUnidad.length];
Color colorUnidad(int numero) => _coloresUnidad[(numero - 1) % _coloresUnidad.length];

const _coloresUnidad = [
  OL.morado, OL.azul, OL.naranja, OL.verde, OL.rojo,
];

const _iconosUnidad = [
  Icons.waving_hand_outlined, Icons.abc, Icons.pin_outlined, Icons.palette_outlined,
  Icons.calendar_month_outlined, Icons.family_restroom_outlined, Icons.house_outlined,
  Icons.chair_outlined, Icons.restaurant_outlined, Icons.checkroom_outlined,
  Icons.accessibility_new_outlined, Icons.location_city_outlined, Icons.person_outline,
  Icons.inventory_2_outlined, Icons.directions_run_outlined, Icons.schedule_outlined,
  Icons.help_outline, Icons.text_fields_outlined, Icons.chat_bubble_outline,
  Icons.forum_outlined,
];

/// Nivel 1 con contenido real (inglés para hispanohablantes). Es la muestra que
/// prueba el reproductor; el resto de niveles usa bancos genéricos hasta que el
/// pipeline de contenido (ARQUITECTURA §1) genere las lecciones reales.
final _unidadesNivel1 = <Unit>[
  _u(1, 1, 'Saludos y presentaciones', [
    ('Hello', 'Hola'), ('Good morning', 'Buenos días'), ('Goodbye', 'Adiós'),
    ('Please', 'Por favor'), ('Thank you', 'Gracias'), ('My name is', 'Me llamo'),
  ], [
    ('My name is Ana.', 'Me llamo Ana.'), ('Nice to meet you.', 'Mucho gusto.'),
    ('How are you today?', '¿Cómo estás hoy?'),
  ]),
  _u(1, 2, 'Pronombres personales', [
    ('I', 'Yo'), ('You', 'Tú'), ('He', 'Él'), ('She', 'Ella'), ('We', 'Nosotros'),
    ('They', 'Ellos'),
  ], [
    ('I am a student.', 'Yo soy estudiante.'), ('She is my friend.', 'Ella es mi amiga.'),
    ('They are at home.', 'Ellos están en casa.'),
  ]),
  _u(1, 3, 'Alfabeto y sonidos', [
    ('Letter', 'Letra'), ('Vowel', 'Vocal'), ('Word', 'Palabra'), ('Sound', 'Sonido'),
    ('Spell', 'Deletrear'), ('Repeat', 'Repetir'),
  ], [
    ('How do you spell it?', '¿Cómo se deletrea?'), ('Repeat, please.', 'Repite, por favor.'),
    ('The word has five letters.', 'La palabra tiene cinco letras.'),
  ]),
  _u(1, 4, 'Números', [
    ('One', 'Uno'), ('Two', 'Dos'), ('Three', 'Tres'), ('Ten', 'Diez'), ('Twenty', 'Veinte'),
    ('One hundred', 'Cien'),
  ], [
    ('I have two brothers.', 'Tengo dos hermanos.'), ('It costs ten dollars.', 'Cuesta diez dólares.'),
    ('There are three cats.', 'Hay tres gatos.'),
  ]),
  _u(1, 5, 'Colores', [
    ('Red', 'Rojo'), ('Blue', 'Azul'), ('Green', 'Verde'), ('Yellow', 'Amarillo'),
    ('Black', 'Negro'), ('White', 'Blanco'),
  ], [
    ('The car is red.', 'El carro es rojo.'), ('I like the blue shirt.', 'Me gusta la camisa azul.'),
    ('The sky is blue.', 'El cielo es azul.'),
  ]),
  _u(1, 6, 'Días, meses y fechas', [
    ('Monday', 'Lunes'), ('Friday', 'Viernes'), ('Weekend', 'Fin de semana'),
    ('January', 'Enero'), ('Today', 'Hoy'), ('Tomorrow', 'Mañana'),
  ], [
    ('Today is Monday.', 'Hoy es lunes.'), ('My birthday is in January.', 'Mi cumpleaños es en enero.'),
    ('See you tomorrow.', 'Nos vemos mañana.'),
  ]),
  _u(1, 7, 'Familia', [
    ('Mother', 'Madre'), ('Father', 'Padre'), ('Sister', 'Hermana'), ('Brother', 'Hermano'),
    ('Son', 'Hijo'), ('Grandmother', 'Abuela'),
  ], [
    ('This is my mother.', 'Esta es mi madre.'), ('I have one sister.', 'Tengo una hermana.'),
    ('My father is a doctor.', 'Mi padre es médico.'),
  ]),
  _u(1, 8, 'Casa', [
    ('Kitchen', 'Cocina'), ('Bedroom', 'Dormitorio'), ('Bathroom', 'Baño'), ('Door', 'Puerta'),
    ('Window', 'Ventana'), ('Table', 'Mesa'),
  ], [
    ('The kitchen is big.', 'La cocina es grande.'), ('Open the window, please.', 'Abre la ventana, por favor.'),
    ('The keys are on the table.', 'Las llaves están en la mesa.'),
  ]),
  _u(1, 9, 'Objetos cotidianos', [
    ('Phone', 'Teléfono'), ('Book', 'Libro'), ('Bag', 'Bolso'), ('Keys', 'Llaves'),
    ('Watch', 'Reloj'), ('Pen', 'Bolígrafo'),
  ], [
    ('Where is my phone?', '¿Dónde está mi teléfono?'), ('This book is new.', 'Este libro es nuevo.'),
    ('I need a pen.', 'Necesito un bolígrafo.'),
  ]),
  _u(1, 10, 'Comida y bebidas', [
    ('Water', 'Agua'), ('Bread', 'Pan'), ('Coffee', 'Café'), ('Apple', 'Manzana'),
    ('Chicken', 'Pollo'), ('Rice', 'Arroz'),
  ], [
    ('I want a coffee, please.', 'Quiero un café, por favor.'), ('The bread is fresh.', 'El pan está fresco.'),
    ('Do you like apples?', '¿Te gustan las manzanas?'),
  ]),
  _u(1, 11, 'Ropa', [
    ('Shirt', 'Camisa'), ('Shoes', 'Zapatos'), ('Jacket', 'Chaqueta'), ('Hat', 'Sombrero'),
    ('Dress', 'Vestido'), ('Pants', 'Pantalones'),
  ], [
    ('I like your jacket.', 'Me gusta tu chaqueta.'), ('These shoes are new.', 'Estos zapatos son nuevos.'),
    ('She wears a red dress.', 'Ella lleva un vestido rojo.'),
  ]),
  _u(1, 12, 'Partes del cuerpo', [
    ('Head', 'Cabeza'), ('Hand', 'Mano'), ('Eye', 'Ojo'), ('Foot', 'Pie'), ('Arm', 'Brazo'),
    ('Mouth', 'Boca'),
  ], [
    ('My head hurts.', 'Me duele la cabeza.'), ('Wash your hands.', 'Lávate las manos.'),
    ('She has blue eyes.', 'Ella tiene ojos azules.'),
  ]),
  _u(1, 13, 'Lugares comunes', [
    ('School', 'Escuela'), ('Hospital', 'Hospital'), ('Bank', 'Banco'), ('Park', 'Parque'),
    ('Store', 'Tienda'), ('Airport', 'Aeropuerto'),
  ], [
    ('The bank is near the park.', 'El banco está cerca del parque.'), ('I go to school.', 'Voy a la escuela.'),
    ('Where is the hospital?', '¿Dónde está el hospital?'),
  ]),
  _u(1, 14, 'Verbo ser/estar', [
    ('I am', 'Yo soy / estoy'), ('You are', 'Tú eres / estás'), ('He is', 'Él es / está'),
    ('We are', 'Nosotros somos'), ('Happy', 'Feliz'), ('Tired', 'Cansado'),
  ], [
    ('I am happy.', 'Estoy feliz.'), ('We are tired.', 'Estamos cansados.'),
    ('He is a teacher.', 'Él es profesor.'),
  ]),
  _u(1, 15, 'Verbo tener', [
    ('I have', 'Yo tengo'), ('You have', 'Tú tienes'), ('She has', 'Ella tiene'),
    ('We have', 'Nosotros tenemos'), ('Time', 'Tiempo'), ('Money', 'Dinero'),
  ], [
    ('I have a dog.', 'Tengo un perro.'), ('She has two cars.', 'Ella tiene dos carros.'),
    ('We have time.', 'Tenemos tiempo.'),
  ]),
  _u(1, 16, 'Verbos básicos', [
    ('Eat', 'Comer'), ('Drink', 'Beber'), ('Go', 'Ir'), ('Work', 'Trabajar'), ('Sleep', 'Dormir'),
    ('Study', 'Estudiar'),
  ], [
    ('I eat breakfast at eight.', 'Desayuno a las ocho.'), ('They work every day.', 'Ellos trabajan cada día.'),
    ('We study English.', 'Estudiamos inglés.'),
  ]),
  _u(1, 17, 'Presente simple', [
    ('Every day', 'Cada día'), ('Always', 'Siempre'), ('Sometimes', 'A veces'), ('Never', 'Nunca'),
    ('Usually', 'Normalmente'), ('Often', 'A menudo'),
  ], [
    ('She works every day.', 'Ella trabaja cada día.'), ('I always drink coffee.', 'Siempre bebo café.'),
    ('He never eats meat.', 'Él nunca come carne.'),
  ]),
  _u(1, 18, 'Preguntas y negaciones', [
    ('What', 'Qué'), ('Where', 'Dónde'), ('When', 'Cuándo'), ('Who', 'Quién'), ('Not', 'No'),
    ('Why', 'Por qué'),
  ], [
    ('Where do you live?', '¿Dónde vives?'), ('I do not like tea.', 'No me gusta el té.'),
    ('What is your name?', '¿Cómo te llamas?'),
  ]),
  _u(1, 19, 'Artículos y preposiciones', [
    ('The', 'El / la'), ('A', 'Un / una'), ('In', 'En'), ('On', 'Sobre'), ('Under', 'Debajo de'),
    ('Next to', 'Al lado de'),
  ], [
    ('The cat is under the table.', 'El gato está debajo de la mesa.'), ('A book is on the chair.', 'Un libro está sobre la silla.'),
    ('I live in a small city.', 'Vivo en una ciudad pequeña.'),
  ]),
  _u(1, 20, 'Conversaciones sencillas', [
    ('Excuse me', 'Disculpe'), ('Sorry', 'Lo siento'), ('Of course', 'Claro'), ('Help', 'Ayuda'),
    ('I understand', 'Entiendo'), ('Again', 'Otra vez'),
  ], [
    ('Excuse me, can you help me?', 'Disculpe, ¿puede ayudarme?'), ('Sorry, I do not understand.', 'Lo siento, no entiendo.'),
    ('Can you say it again?', '¿Puede repetirlo?'),
  ]),
];

Unit _u(int nivel, int n, String titulo, List<(String, String)> vocab,
        List<(String, String)> frases) =>
    Unit(
      nivel: nivel,
      numero: n,
      titulo: titulo,
      icono: _iconosUnidad[(n - 1) % _iconosUnidad.length],
      color: _coloresUnidad[(n - 1) % _coloresUnidad.length],
      vocab: vocab,
      frases: frases,
    );

/// Bancos genéricos por nivel para que las 900 lecciones restantes existan y sean
/// navegables mientras se genera el contenido real.
const _bancoGenerico = <int, (List<(String, String)>, List<(String, String)>)>{
  2: (
    [('Yesterday', 'Ayer'), ('Went', 'Fui / fue'), ('Will', 'Voy a / irá'), ('Mine', 'Mío'),
     ('Quickly', 'Rápidamente'), ('Between', 'Entre')],
    [('I went to the market yesterday.', 'Fui al mercado ayer.'),
     ('She will call you tomorrow.', 'Ella te llamará mañana.'),
     ('This book is mine.', 'Este libro es mío.')],
  ),
  3: (
    [('Bigger', 'Más grande'), ('Enough', 'Suficiente'), ('Running', 'Corriendo'),
     ('Bought', 'Compró'), ('Maybe', 'Quizás'), ('Although', 'Aunque')],
    [('I am running to the station.', 'Estoy corriendo a la estación.'),
     ('This house is bigger than mine.', 'Esta casa es más grande que la mía.'),
     ('We bought enough food.', 'Compramos suficiente comida.')],
  ),
  4: (
    [('Meeting', 'Reunión'), ('Deadline', 'Fecha límite'), ('Flight', 'Vuelo'),
     ('Complaint', 'Queja'), ('Opinion', 'Opinión'), ('Schedule', 'Horario')],
    [('In my opinion, the flight is too early.', 'En mi opinión, el vuelo es muy temprano.'),
     ('Could you explain the problem?', '¿Podría explicar el problema?'),
     ('We have a meeting at nine.', 'Tenemos una reunión a las nueve.')],
  ),
  5: (
    [('Experience', 'Experiencia'), ('Suddenly', 'De repente'), ('Solve', 'Resolver'),
     ('Colleague', 'Colega'), ('Actually', 'En realidad'), ('Deal', 'Acuerdo')],
    [('Suddenly, the lights went out.', 'De repente, se fue la luz.'),
     ('Let me tell you what happened.', 'Déjame contarte lo que pasó.'),
     ('We need to solve this today.', 'Tenemos que resolver esto hoy.')],
  ),
  6: (
    [('Give up', 'Rendirse'), ('Figure out', 'Descubrir'), ('Negotiate', 'Negociar'),
     ('Point of view', 'Punto de vista'), ('However', 'Sin embargo'), ('Issue', 'Asunto')],
    [('I need to figure out the schedule.', 'Necesito descubrir el horario.'),
     ('From my point of view, it is fair.', 'Desde mi punto de vista, es justo.'),
     ('However, we can negotiate the price.', 'Sin embargo, podemos negociar el precio.')],
  ),
  7: (
    [('Break the ice', 'Romper el hielo'), ('Argument', 'Argumento'), ('Interview', 'Entrevista'),
     ('Nevertheless', 'No obstante'), ('Persuade', 'Persuadir'), ('Outline', 'Esquema')],
    [('Let me outline the main argument.', 'Déjame esbozar el argumento principal.'),
     ('Nevertheless, I disagree with you.', 'No obstante, no estoy de acuerdo contigo.'),
     ('She tried to break the ice.', 'Ella intentó romper el hielo.')],
  ),
  8: (
    [('Leverage', 'Aprovechar'), ('Stakeholder', 'Parte interesada'), ('Hit the ground running', 'Empezar con todo'),
     ('Trade-off', 'Compromiso'), ('Whereas', 'Mientras que'), ('Benchmark', 'Referencia')],
    [('We can leverage our experience here.', 'Podemos aprovechar nuestra experiencia aquí.'),
     ('There is a trade-off between cost and speed.', 'Hay un compromiso entre costo y velocidad.'),
     ('The new hire hit the ground running.', 'El nuevo empleado empezó con todo.')],
  ),
  9: (
    [('Hypothesis', 'Hipótesis'), ('Nuance', 'Matiz'), ('Off the record', 'Extraoficialmente'),
     ('Consensus', 'Consenso'), ('Albeit', 'Aunque'), ('Rhetoric', 'Retórica')],
    [('The findings, albeit preliminary, are promising.', 'Los hallazgos, aunque preliminares, son prometedores.'),
     ('We reached a consensus after the debate.', 'Llegamos a un consenso tras el debate.'),
     ('There is a subtle nuance in that phrase.', 'Hay un matiz sutil en esa frase.')],
  ),
  10: (
    [('Eloquent', 'Elocuente'), ('Ambiguity', 'Ambigüedad'), ('Cut to the chase', 'Ir al grano'),
     ('Paradigm', 'Paradigma'), ('Notwithstanding', 'A pesar de'), ('Rapport', 'Sintonía')],
    [('Let us cut to the chase.', 'Vayamos al grano.'),
     ('Notwithstanding the risks, the plan is sound.', 'A pesar de los riesgos, el plan es sólido.'),
     ('She built rapport with the audience quickly.', 'Ella conectó con el público rápidamente.')],
  ),
};

/// Idioma meta cuyo contenido se está generando/mostrando. Lo fija el estado de
/// progreso al cargar o cambiar de idioma (ver providers.dart).
String idiomaContenido = 'en';

String nombreIdiomaContenido() => idioma(idiomaContenido).nombre;

final Map<String, List<Unit>> _cacheUnidades = {};

/// Se llama cuando llega contenido JSON nuevo para un idioma (ContenidoJson.precargar).
void invalidarCacheContenido(String idioma) {
  _cacheUnidades.removeWhere((k, _) => k.startsWith('$idioma-'));
  _cacheLecciones.removeWhere((k, _) => k.startsWith('$idioma-'));
}

List<Unit> unidadesDe(int n) {
  final idm = idiomaContenido;
  return _cacheUnidades.putIfAbsent('$idm-$n', () {
    // 0) Fundamentos (nivel 0): tramo previo para empezar de cero.
    if (n == 0) return Fundamentos.comoUnits(idm);
    // 1) Contenido generado por el pipeline, si está empaquetado en assets.
    final json = ContenidoJson.unidades(idm, n);
    if (json != null) {
      return [
        for (final u in json)
          ContenidoJson.aUnit(u, n, _iconosUnidad[(u.numero - 1) % _iconosUnidad.length], _coloresUnidad[(u.numero - 1) % _coloresUnidad.length])
      ];
    }
    // 2) Bancos escritos a mano (semilla).
    if (n == 1 && idm == 'en') return _unidadesNivel1;
    if (n == 1) {
      // Nivel 1 en otro idioma: mismos títulos de unidad, banco del idioma.
      return List.generate(20, (i) {
        final base = _unidadesNivel1[i];
        final b = bancoNivel1(idm, i + 1)!;
        return _u(1, i + 1, base.titulo, b.vocab, b.frases);
      });
    }
    final lvl = nivel(n);
    final banco = _bancoGenerico[n]!;
    return List.generate(20, (i) {
      final titulo = lvl.temario[i % lvl.temario.length];
      return _u(n, i + 1, titulo, banco.$1, banco.$2);
    });
  });
}

/// Las 5 lecciones de una unidad siguen siempre el mismo patrón didáctico:
/// vocabulario → frases → escucha → práctica → repaso.
const _patronLecciones = [
  ('Vocabulario', 'Palabras clave de la unidad'),
  ('Frases', 'Construye oraciones'),
  ('Escucha', 'Comprensión auditiva'),
  ('Práctica', 'Ejercicios mixtos'),
  ('Repaso', 'Consolida lo aprendido'),
];

final Map<String, List<Lesson>> _cacheLecciones = {};

List<Lesson> leccionesDe(int n) {
  return _cacheLecciones.putIfAbsent('$idiomaContenido-$n', () {
    if (n == 0) return Fundamentos.lecciones(idiomaContenido);
    final out = <Lesson>[];
    for (final u in unidadesDe(n)) {
      for (var k = 0; k < Unit.leccionesPorUnidad; k++) {
        final numero = (u.numero - 1) * Unit.leccionesPorUnidad + k + 1;
        out.add(Lesson(
          id: 'L$n-${numero.toString().padLeft(3, '0')}',
          nivel: n,
          numero: numero,
          unidad: u.numero,
          titulo: '${_patronLecciones[k].$1}: ${u.titulo}',
          subtitulo: _patronLecciones[k].$2,
          steps: _pasos(u, k),
          xp: 20 + n * 2,
        ));
      }
    }
    return out;
  });
}

Lesson? leccionPorId(String id) {
  final n = int.tryParse(id.split('-').first.substring(1));
  if (n == null) return null;
  for (final l in leccionesDe(n)) {
    if (l.id == id) return l;
  }
  return null;
}

List<LessonStep> _pasos(Unit u, int k) {
  final v = u.vocab;
  final f = u.frases;
  final idm = idiomaContenido;
  final sinEspacios = idiomasSinEspacios.contains(idm);
  final nombreIdioma = nombreIdiomaContenido();
  (String, String) vv(int i) => v[i % v.length];
  (String, String) ff(int i) => f[i % f.length];

  LessonStep flash(int i) => LessonStep(
        type: StepType.flashcard,
        skill: Skill.vocabulario,
        prompt: vv(i).$1,
        translation: vv(i).$2,
      );
  LessonStep elige(int i) => LessonStep(
        type: StepType.multipleChoice,
        skill: Skill.vocabulario,
        prompt: '¿Cómo se dice "${vv(i).$2}"?',
        answer: vv(i).$1,
        options: [vv(i).$1, vv(i + 1).$1, vv(i + 2).$1, vv(i + 3).$1]..shuffle(),
      );
  LessonStep parejas(int i) => LessonStep(
        type: StepType.matchPairs,
        skill: Skill.vocabulario,
        prompt: 'Une cada palabra con su traducción',
        pairs: [vv(i), vv(i + 1), vv(i + 2), vv(i + 3)],
      );
  LessonStep ordena(int i) => LessonStep(
        type: StepType.orderWords,
        skill: Skill.frases,
        prompt: ff(i).$2,
        answer: ff(i).$1,
        translation: ff(i).$2,
        hint: 'Traduce al $nombreIdioma',
      );
  // Elegir la frase correcta entre tres (para idiomas sin espacios o como variante).
  LessonStep eligeFrase(int i) => LessonStep(
        type: StepType.multipleChoice,
        skill: Skill.frases,
        prompt: '¿Cómo se dice en $nombreIdioma: "${soloNativo(ff(i).$2)}"?',
        answer: ff(i).$1,
        options: [ff(i).$1, ff(i + 1).$1, ff(i + 2).$1]..shuffle(),
      );
  LessonStep hueco(int i) {
    final palabras = ff(i).$1.split(' ');
    final idx = palabras.length ~/ 2;
    final resp = palabras[idx].replaceAll(RegExp(r'[.,?!]'), '');
    final frase = [...palabras]..[idx] = '____';
    return LessonStep(
      type: StepType.fillBlank,
      skill: Skill.gramatica,
      prompt: frase.join(' '),
      answer: resp,
      options: [resp, vv(i).$1, vv(i + 2).$1]..shuffle(),
      translation: ff(i).$2,
    );
  }
  LessonStep escucha(int i) => LessonStep(
        type: StepType.listenWrite,
        skill: Skill.listening,
        prompt: ff(i).$1,
        answer: ff(i).$1,
        translation: ff(i).$2,
        hint: 'Empieza con "${ff(i).$1.split(' ').first}"',
      );
  LessonStep habla(int i) => LessonStep(
        type: StepType.speak,
        skill: Skill.pronunciacion,
        prompt: ff(i).$1,
        translation: ff(i).$2,
      );

  const palabrasImagen = [
    'Breakfast', 'Family', 'City', 'Beach', 'Kitchen', 'School', 'Office', 'Restaurant',
    'Hospital', 'Airport', 'Train', 'Bus', 'Coffee', 'Party', 'Gym', 'Hotel',
  ];
  final pal = palabrasImagen[(u.numero + u.nivel) % palabrasImagen.length];
  final imagen = LessonStep(
    type: StepType.imageChoice,
    skill: Skill.vocabulario,
    prompt: 'Selecciona la imagen que corresponde a: "$pal"',
    answer: pal,
    pairs: opcionesImagen(pal),
  );

  // En chino/japonés (sin espacios en la escritura real) se prioriza reconocer la
  // frase completa; ordenar palabras se mantiene porque el banco lleva espacios.
  LessonStep ordenaOElige(int i) => sinEspacios && i.isOdd ? eligeFrase(i) : ordena(i);

  // Paso de lectura: gramática de la unidad + errores típicos (solo si hay contenido generado).
  final lectura = u.gramatica.isEmpty && u.erroresTipicos.isEmpty
      ? null
      : LessonStep(
          type: StepType.readText,
          skill: Skill.gramatica,
          prompt: u.gramatica,
          translation: u.erroresTipicos.map((e) => '${e.$1}\u0001${e.$2}\u0001${e.$3}').join('\u0002'),
        );
  // Paso de rol: el diálogo de situación de la unidad, réplica a réplica.
  final rol = u.dialogo.isEmpty
      ? null
      : LessonStep(
          type: StepType.roleplay,
          skill: Skill.conversacion,
          prompt: u.titulo,
          translation: u.dialogo.map((d) => '${d.$1}\u0001${d.$2}\u0001${d.$3}').join('\u0002'),
        );
  List<LessonStep> con(List<LessonStep> base, {LessonStep? primero, LessonStep? ultimo}) =>
      [?primero, ...base, ?ultimo];

  switch (k) {
    case 0:
      return [flash(0), flash(1), flash(2), elige(0), parejas(0), elige(3)];
    case 1:
      return con([flash(3), ordenaOElige(0), hueco(0), ordenaOElige(1), elige(1)], primero: lectura);
    case 2:
      return con([escucha(0), elige(2), escucha(1), hueco(1), habla(0)], ultimo: rol);
    case 3:
      return [imagen, parejas(2), ordenaOElige(2), hueco(2), escucha(2), elige(4)];
    default:
      return con([parejas(0), ordenaOElige(0), habla(1), elige(5), escucha(0), habla(2)], primero: rol);
  }
}
