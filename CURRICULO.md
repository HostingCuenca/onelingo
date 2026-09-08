# OneLingo · Currículo (los 10 niveles → un camino real)

Los 10 niveles del cliente se alinean con el **Marco Común Europeo (CEFR)** y con
la progresión de los cursos de referencia de Oxford (*English File*, *Headway*) y
Cambridge (*Empower*, *Interchange*). Así el "camino" es el mismo que sigue un
alumno en una academia, y los exámenes de nivel se pueden calibrar contra pruebas
reales (Cambridge KET/PET/FCE/CAE/CPE).

| Nivel OneLingo | CEFR | Curso Oxford equivalente | Horas guiadas acumuladas (CEFR) | Vocabulario activo |
|---|---|---|---|---|
| 1 Básico | A1.1 | English File Beginner (Files 1-6) | 0-50 | 300 |
| 2 Básico | A1.2 | English File Beginner (7-12) / Elementary (1-3) | 50-100 | 600 |
| 3 Básico Avanzado | A2 | English File Elementary (4-12) | 100-200 | 1 000 |
| 4 Intermedio | B1.1 | English File Pre-intermediate | 200-300 | 1 500 |
| 5 Intermedio | B1.2 | English File Intermediate | 300-400 | 2 200 |
| 6 Intermedio Avanzado | B2.1 | English File Intermediate Plus | 400-500 | 3 000 |
| 7 Avanzado | B2.2 | English File Upper-Intermediate | 500-600 | 4 000 |
| 8 Avanzado | C1.1 | English File Advanced | 600-750 | 5 000 |
| 9 Avanzado Superior | C1.2 | English File Advanced Plus | 750-900 | 6 500 |
| 10 Dominio | C2 | Proficiency (CPE) | 900-1 000+ | 8 000+ |

Cada nivel = 100 lecciones = 20 unidades × 5 lecciones (vocabulario → frases →
escucha → práctica → repaso). A ~10 min por lección más práctica libre salen los
"3 meses o más" por nivel que pide el cliente.

## Gramática por nivel (CEFR, referencia Tracktest / Cambridge English Profile)
- **N1-N2 (A1)**: verbo *be*, *have got*, presente simple, artículos, plurales,
  posesivos, *there is/are*, *can/can't*, preposiciones de lugar y tiempo,
  imperativos, *like + -ing*, pasado de *be*, pasado simple regular; *going to*.
- **N3 (A2)**: pasado simple irregular, presente continuo (ahora y futuro),
  comparativos/superlativos, *should*, *have to*, *will* (decisiones), primer
  condicional, cuantificadores (*some/any/much/many*), adverbios de frecuencia,
  phrasal verbs básicos, pronombres reflexivos.
- **N4-N5 (B1)**: presente perfecto (+ *for/since*, *just/yet/already*), pasado
  continuo, futuro (*will/going to/presente continuo*), segundo condicional,
  *used to*, pasiva presente/pasado, *may/might*, *must/can't* (deducción),
  estilo indirecto básico, relativas, *-ed/-ing* adjectives, question tags.
- **N6-N7 (B2)**: presente perfecto continuo, pasado perfecto, tercer condicional
  y mixtos, pasiva en todos los tiempos, modales perfectos (*should have*),
  *have something done*, *be/get used to*, verbos de estado, relativas
  especificativas y explicativas, phrasal verbs separables, conectores.
- **N8-N9 (C1)**: inversión (*Not only… / Had I known…*), *wish / if only*,
  cleft sentences, modales en pasado, futuro perfecto/continuo, discurso
  indirecto avanzado, registro formal/informal, colocaciones, idioms, elipsis.
- **N10 (C2)**: dominio de matices, ironía y humor, registro académico y
  profesional, argumentación y negociación, comprensión de acentos y velocidades
  naturales, producción escrita extensa. Evaluación integral.

## Temas por nivel (para las 20 unidades)
Ya están en `lib/core/content/curriculum.dart` (`niveles[n].temario`). El Nivel 1
tiene vocabulario y frases reales; los niveles 2-10 usan bancos genéricos hasta que
el pipeline de contenido (ARQUITECTURA §1) genere las lecciones definitivas con IA
a partir de este documento.

## Cómo se usa en la app
- `Level.temario` → títulos de unidad.
- `perfilesNivel` (catalog.dart) → límites de vocabulario, tiempos y velocidad
  que se inyectan en la IA; los valores salen de la tabla de arriba.
- El examen final de cada nivel muestrea preguntas del banco del nivel; la nota
  mínima de 65 % la fija el cliente.

## Fuentes
- Oxford University Press, catálogo English File 5.ª ed.
  https://elt.oup.com/catalogue/items/global/adult_courses/english-file-fifth-edition/
- Tracktest, English grammar CEF level requirements
  https://tracktest.eu/english-grammar-cef-level-requirements/
- CEFR levels explained (horas y vocabulario por nivel)
  https://www.nona.academy/post/cefr-levels-explained ·
  https://practicetestgeeks.com/cefr/cefr-study-hours
