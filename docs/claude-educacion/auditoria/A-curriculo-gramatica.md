# Auditoría A — Currículo multilingüe y gramática

Agente A · 2026-09-26 · rama `claude/educacion-multilenguaje` · solo lectura del código.
Cifras obtenidas con scripts `python3` sobre `assets/contenido/*/*.json` y `lib/core/content/grammar_guides.dart`.

## Resumen

1. Los 10 idiomas tienen **el mismo esqueleto**: nivel 0 = 8 unidades (3 escritura + 5 vocabulario) y niveles 1–2 = 20 unidades cada uno, con **los mismos 40 temas en el mismo orden** que inglés (verificado: `tema` idéntico en los 10 idiomas). Es el temario del cliente (`curriculum.dart:27-163`) traducido; no hay una secuencia propia de cada idioma.
2. La "enseñanza" de cada unidad de niveles 1–2 es **un único párrafo `gramatica` de 150–224 caracteres de media**, más 2 `errores_tipicos`. Aparece una sola vez (paso `readText` de la lección 2 de 5, `curriculum.dart:595-603`). El resto son ejercicios genéricos: flashcard, elegir, ordenar y un hueco que **quita la palabra central de la frase**, sin relación con la gramática (`curriculum.dart:549-561`).
3. **Niveles 3–10 no tienen contenido real en ningún idioma.** Usan `_bancoGenerico` (6 palabras y 3 frases por nivel, **en inglés**, repetidas en las 20 unidades; `curriculum.dart:453`). Un alumno de ruso o japonés en el nivel 3 practicaría inglés.
4. Inglés tiene además 43 guías de gramática en `grammar_guides.dart`, repartidas 5/6/4/5/5/5/4/4/3/2 entre los niveles 1 y 10. Forman un segundo currículo **desconectado** de los JSON y con niveles distintos: el comparativo está en JSON N2-U9 y en la guía `comparisons` de nivel 4; el pasado, en N2-U4 y en `past` de nivel 3.
5. La secuencia de inglés en N1 usa *be*, posesivos, *do* y *can* desde la unidad 1, pero enseña *be* en la U14, *have* en la U15 y las preguntas con *do* en la U18. Hay evidencia unidad por unidad más abajo.
6. `foundations-v1` (`foundations.dart`, 6 microlecciones, ruta `/fundamentos`) es **solo de inglés y está escrito a mano**. `fundamentos.dart` es otra cosa: el **nivel 0 JSON** (letras, números, colores, palabras sueltas) de los 10 idiomas. Hay dos "Fundamentos" con el mismo nombre y contenido distinto.
7. `/fundamentos` (inglés) y `/gramatica` (guías inglesas) se ofrecen **sin filtrar por idioma** en `learning_path.dart:46` (nivel ≤ 2) y en `grammar_screen.dart:212`. Parece que un alumno de alemán vería material de inglés; conviene que el agente D lo verifique.
8. Propongo un grafo de inglés de 111 nodos `en-g-*`: 105 de pre-A1 a C1 y 6 C2 reservados sin nivel interno. De ellos, 43 están cubiertos por una guía o microlección existente, 27 solo en parte y 41 faltan.
9. Diseño rutas de fundamentos **propias** para los 9 idiomas restantes (escritura primero en ja/zh/ko/ru; género y V2 en de; ser/estar como ventaja en pt/es). El español se diseña para anglohablantes, con explicaciones en inglés (DEC-004 opción a).
10. Riesgos principales de implementación: el cargador exige exactamente 20 unidades por nivel (`contenido_json.dart:133`), y los IDs de lección `L<n>-NNN` dependen del orden de las unidades (`curriculum.dart:~480`). Reordenar las unidades cambia qué progreso se asocia a cada lección.

## Inventario real por idioma

### Cifras (idénticas en estructura para los 10 idiomas)

| Idioma | N0 unid. (escr/vocab) | N0 ítems | N0 examen | N1 unid. | N2 unid. | Vocab N1+N2 | Frases N1+N2 | Diálogos | Errores típicos | Examen | Long. media `gramatica` N1 / N2 (caracteres) | Extras |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| en | 8 (3/5) | 93 | 24 | 20 | 20 | 320 | 240 | 40 | 80 | 120 | 150 / 177 | biblioteca (116 preg.; 20 de gramática, 2 por nivel), reading 20, listening 20, situaciones 50, voc. situacional 50, diagnóstico 87, **43 guías de gramática**, foundations-v1 (6) |
| es | 8 (3/5) | 94 | 24 | 20 | 20 | 320 | 240 | 40 | 80 | 120 | 166 / 187 | — |
| fr | 8 (3/5) | 95 | 24 | 20 | 20 | 320 | 240 | 40 | 80 | 120 | 179 / 212 | — |
| de | 8 (3/5) | 95 | 24 | 20 | 20 | 320 | 240 | 40 | 80 | 120 | 174 / 224 | — |
| pt | 8 (3/5) | 93 | 24 | 20 | 20 | 320 | 240 | 40 | 80 | 120 | 172 / 205 | — |
| it | 8 (3/5) | 89 | 24 | 20 | 20 | 320 | 240 | 40 | 80 | 120 | 178 / 220 | — |
| zh | 8 (3/5) | 102 | 24 | 20 | 20 | 320 | 240 | 40 | 80 | 120 | 172 / 177 | — |
| ja | 8 (3/5) | 119 | 24 | 20 | 20 | 320 | 240 | 40 | 80 | 120 | 178 / 171 | — |
| ko | 8 (3/5) | 100 | 24 | 20 | 20 | 320 | 240 | 40 | 80 | 120 | 179 / 172 | — |
| ru | 8 (3/5) | 92 | 24 | 20 | 20 | 320 | 240 | 40 | 80 | 120 | 190 / 214 | — |
| **N3–N10** | — | — | — | 0 reales | — | 6 palabras y 3 frases en inglés por nivel, para los 10 idiomas (`curriculum.dart:50-113`, `:453`) | | | | | | |

### Qué enseña cada unidad y qué solo ejercita

| Tipo de unidad | Enseñanza (explicación y ejemplos) | Solo ejercicios |
|---|---|---|
| N0 JSON, 8 unidades × 10 idiomas | `descripcion` de 1–2 frases e ítems con símbolo, romanización, significado y ejemplo (se muestran como flashcards) | Lecciones "Descubre / Practica / Repaso" (`fundamentos.dart:103-127`) |
| N1–N2 JSON, 40 unidades × 10 idiomas | Párrafo `gramatica` (unos 150–224 caracteres), 2 errores típicos y un diálogo modelo | 4 de las 5 lecciones. El hueco no es gramatical (`curriculum.dart:549`). Todo el vocabulario sale de la misma lista |
| N3–N10 | **Ninguna** | Banco genérico en inglés |
| Guías de inglés (43) | `goal` y `rule` (1 párrafo), 1–2 ejemplos y un error común | 2 comprobaciones por guía (86 en total) |
| foundations-v1 de inglés (6) | 13 tarjetas con explicación | 12 comprobaciones guiadas |

Temas N1 (20 unidades, iguales en los 10 idiomas): Pronombres personales · Saludos y presentaciones · Alfabeto y sonidos · Números · Colores · Días, meses y fechas · Familia · Casa · Objetos cotidianos · Comida y bebidas · Ropa · Partes del cuerpo · Lugares comunes · Verbo ser/estar · Verbo tener · Verbos básicos · Presente simple · Preguntas y negaciones · Artículos y preposiciones · Conversaciones sencillas.
Temas N2: Verbos frecuentes · Conjugación · Presente · Pasado básico · Futuro básico · Preguntas y respuestas · Negaciones · Pronombres y posesivos · Adjetivos · Adverbios básicos · Preposiciones · Construcción de frases · Expresiones cotidianas · Listening · Lectura · Escritura · Pronunciación · Conversaciones básicas · Situaciones de la vida diaria · Repaso del nivel.

Hay adaptación dentro del párrafo de cada unidad (por ejemplo, ja N1-U14 explica です/います/あります y ru N1-U14 explica la omisión de "ser"). Pero el **orden** es el de inglés. Consecuencias concretas:
- **ja N1-U19** ("Artículos y preposiciones") presenta de golpe las 7 partículas は/が/を/に/で/の/と, que se usan desde la U1.
- **ko N1-U19** hace lo mismo con 은/는, 이/가, 을/를, 에, 에서, 의 y 하고.
- **ru N1-U19** mete en una sola unidad A1 el prepositivo, el acusativo, el genitivo y el instrumental.
- **de N1-U19** introduce el dativo (`mit`, `auf dem Tisch`) en A1 sin haber enseñado antes el acusativo.
- **es**: el curso es **monolingüe**. El vocabulario se glosa en español (`hola` → "saludo general") y N0-U2 enseña "la ñ" a hispanohablantes.

### Las 43 guías de gramática de inglés (`grammar_guides.dart`, línea de inicio · id · nivel interno)

| Nivel (CEFR según `diagnostico.dart:320`) | Guías, en orden de archivo |
|---|---|
| 1 (A1) | L29 `be` · L52 `pronouns-possessives` · L84 `order` · L107 `articles-plurals` · L137 `there-be` |
| 2 (A1) | L165 `object-possessive` · L198 `present` · L221 `questions` · L253 `ability` · L283 `frequency` · L315 `time-place` |
| 3 (A2) | L343 `past-be` · L371 `past` · L399 `continuous` · L427 `future-plans` |
| 4 (A2) | L455 `quantity` · L483 `comparisons` · L511 `advice` · L543 `obligation` · L571 `verb-patterns` |
| 5 (B1) | L599 `past-continuous` · L627 `perfect` · L650 `first-conditional` · L678 `relative` · L710 `passive-basic` |
| 6 (B1) | L742 `past-perfect` · L774 `second` · L797 `third-conditional` · L825 `reported` · L848 `reporting-questions` |
| 7 (B2) | L876 `future-perfect` · L906 `passive` · L933 `relative-extra` · L961 `cohesion` |
| 8 (B2) | L989 `mixed` · L1017 `modal-deduction` · L1049 `hedging` · L1077 `concession` |
| 9 (C1) | L1105 `reference` · L1137 `negative-inversion` · L1164 `condition-inversion` |
| 10 (C1) | L1192 `editing-register` · L1225 `were-it-not` |

## Problemas de secuencia en inglés (con evidencia)

| # | Problema | Evidencia |
|---|---|---|
| S1 | Se usa *be* antes de enseñarlo | `en/nivel-1.json` U1 "I am Ana.", "We are from Ecuador."; U2 "I'm Tom"; U4, en la gramática, "I am twenty". *Be* se enseña en **U14** |
| S2 | Posesivos antes de enseñarlos | U1 "You are my teacher", "He is my brother"; examen de U2 "___ name is Ana". Se enseñan en U7 y otra vez en N2-U8 |
| S3 | Preguntas y negación con *do* antes de enseñarlas | U3 "How do you spell…?"; U7 "Do you have children?"; U9 "Do you have a pen?"; U10 "I don't like fish". *Do/does* se enseña en **U18** |
| S4 | *Have* antes de enseñarlo | Gramática de U7 "I have two sisters" y examen "I ___ two brothers". *Have* se enseña en **U15** |
| S5 | Estructuras de A2 dentro de A1 | U7, diálogo: "Is she older than you?" (comparativo, que es N2-U9 y la guía de nivel 4). U10 "I would like…" (aceptable como bloque fijo, pero no se marca así). U9 activa el continuo "-ing" |
| S6 | -s de tercera persona antes de presentar el presente simple | Gramática de U16 "she works"; el presente simple es la U17 |
| S7 | Pasado irregular antes que el regular y que *was/were* | N2-U1 "go/went, make/made…"; N2-U4 enseña después *was/were* y -ed |
| S8 | Duplicados | Presente simple: N1-U17, N2-U2 y N2-U3. Preguntas y negación: N1-U18, N2-U6 y N2-U7. Preposiciones: N1-U6, N1-U8, N1-U19 y N2-U11. Posesivos: N1-U7 y N2-U8. Alfabeto: N0-U1/2 y N1-U3. Números: N0-U4 y N1-U4. Colores: N0-U5 y N1-U5. Frecuencia: N1-U17 y N2-U10. El temario N3 repite "Pasado", "Futuro" y "Presente continuo" (`curriculum.dart:60`) |
| S9 | Unidades de destreza metidas en el temario gramatical | N2-U14 "Listening", U15 "Lectura", U16 "Escritura" y U17 "Pronunciación" tienen "gramática" que no lo es (horas, carteles, -s/-ed) |
| S10 | Guías: *be* antes que pronombres; posesivo antes de enseñarlo | `be` (L29) va antes que `pronouns-possessives` (L52); la comprobación de `be` "My name ___ Leo" usa *my* |
| S11 | Guías: una sola guía de *be* cubre afirmación, negación y pregunta, pero **no** contracciones ni respuestas cortas | `grammar_guides.dart:33` |
| S12 | Guías con nivel dudoso | `third-conditional` en nivel 6 (B1); lo habitual es B2. `perfect` (nivel 5) junta experiencia, *since/for* y contraste con el pasado en una sola guía. `modal-deduction` y `hedging` (nivel 8) llegan antes que *may/might* básicos, que no tienen guía |
| S13 | Dos escalas incoherentes | Continuo: N2-U3 (JSON) frente a nivel 3 (guía). Futuro: N2-U5 frente a nivel 3. Pasado: N2-U4 frente a nivel 3. Comparativos: N2-U9 frente a nivel 4. Contables: N1-U10 *some* frente a nivel 4 |
| S14 | Temas aislados o sin continuidad | *There is/are* (N1-U8) no vuelve. *Imperativo* se usa en N1-U13 ("Turn left") y nunca se enseña. *Wear*/*hurt* (N1-U11/12) son vocabulario con "gramática" artificial |
| S15 | El hueco no es gramatical | `curriculum.dart:549-561` quita `palabras[len ~/ 2]`. En "I am Ana." quita *am* por casualidad; en otras frases quita un sustantivo |
| S16 | foundations-v1 no llega a *it/we/they*, negación ni preguntas | `foundations.dart:40-253`; el propio documento lo reconoce (`FUNDAMENTOS-DESDE-CERO.md`, "Continuación") |

## Grafo gramatical inglés pre-A1→C2

Convenciones:
- **Nivel** = nivel interno (0–10); C2 queda `null` (reservado, DEC-002).
- **Prerrequisitos**: solo los directos.
- **Estado**: EXISTE(id) = guía o microlección actual; PARCIAL(id) = la cubre de forma incompleta; FALTA = no hay nada.
- Las guías actuales se conservan como **alias** del nodo nuevo, para no perder la evidencia `grammar-guide-<id>-<n>`.

### Pre-A1 (nivel 0) — ruta de fundamentos

| ID | Título | Nv | CEFR | Prerrequisitos | Estado |
|---|---|---|---|---|---|
| en-g-sound-text | Sonido ↔ texto, saludos y cortesía | 0 | pre-A1 | — | PARCIAL (N0 JSON U1–3, U6) |
| en-g-subj-pron-1 | I / you | 0 | pre-A1 | sound-text | EXISTE(foundations `i-you`) |
| en-g-subj-pron-2 | he / she / it / we / they | 0 | pre-A1 | subj-pron-1 | PARCIAL(foundations `he-she`; guía `pronouns-possessives`) |
| en-g-be-affirm | *Be* afirmativo am/is/are | 0 | pre-A1 | subj-pron-2 | PARCIAL(`i-am`, `you-are`, `he-she`; guía `be`) |
| en-g-be-contractions | I'm / you're / he's / it's / we're / they're | 0 | pre-A1 | be-affirm | FALTA |
| en-g-be-adj-state | *Be* + adjetivo (ser y estar) | 0 | pre-A1 | be-affirm | EXISTE(`feelings`) |
| en-g-be-negative | isn't / aren't / I'm not | 0 | pre-A1 | be-contractions | PARCIAL(guía `be`) |
| en-g-be-yesno | Are you…? Is she…? | 0 | pre-A1 | be-negative | PARCIAL(guía `be`) |
| en-g-short-answers-be | Yes, I am / No, I'm not | 0 | pre-A1 | be-yesno | FALTA |
| en-g-wh-be | What / Where / How + *be* | 0 | pre-A1 | be-yesno | FALTA |
| en-g-introduce | Presentarse (name, from, how are you) | 0 | pre-A1 | wh-be | PARCIAL(`introduce`) |

### A1 (niveles 1–2)

| ID | Título | Nv | CEFR | Prerrequisitos | Estado |
|---|---|---|---|---|---|
| en-g-possessive-adj | my / your / his / her / its / our / their | 1 | A1 | subj-pron-2 | EXISTE(`pronouns-possessives`) |
| en-g-articles-a-an | a / an | 1 | A1 | be-affirm | PARCIAL(`order`, `articles-plurals`) |
| en-g-plural-nouns | Plural regular e irregular frecuente | 1 | A1 | articles-a-an | EXISTE(`articles-plurals`) |
| en-g-article-the | *the* frente a *a/an*; plural sin artículo | 1 | A1 | plural-nouns | PARCIAL(`articles-plurals`) |
| en-g-adj-position | Adjetivo invariable antes del sustantivo | 1 | A1 | articles-a-an | EXISTE(`order`) |
| en-g-demonstratives | this / that / these / those | 1 | A1 | plural-nouns | FALTA |
| en-g-possessive-s | Ana's book | 1 | A1 | possessive-adj | FALTA |
| en-g-there-is-are | there is / are (+ negativa y pregunta) | 1 | A1 | plural-nouns | EXISTE(`there-be`) |
| en-g-prep-place-basic | in / on / under / next to | 1 | A1 | there-is-are | PARCIAL(`time-place`) |
| en-g-imperatives | Sit down / Don't… | 1 | A1 | be-negative | FALTA |
| en-g-word-order | Sujeto + verbo + objeto + lugar + tiempo | 1 | A1 | adj-position | EXISTE(`order`) |
| en-g-have-got | have / have got (posesión, familia) | 1 | A1 | possessive-adj | FALTA |
| en-g-pres-simple-aff | Presente simple afirmativo (I/you/we/they) | 2 | A1 | word-order | PARCIAL(`present`) |
| en-g-pres-simple-3s | -s / -es / -ies en 3.ª persona | 2 | A1 | pres-simple-aff | PARCIAL(`present`) |
| en-g-do-negative | don't / doesn't | 2 | A1 | pres-simple-3s | PARCIAL(`present`) |
| en-g-do-questions | Do/Does…? + respuestas cortas | 2 | A1 | do-negative | PARCIAL(`present`, `questions`) |
| en-g-wh-do | Wh- + do/does; preguntas de sujeto con *who* | 2 | A1 | do-questions, wh-be | EXISTE(`questions`) |
| en-g-freq-adverbs | always…never (posición con *be* y con otros verbos) | 2 | A1 | pres-simple-3s | EXISTE(`frequency`) |
| en-g-prep-time | at / on / in (tiempo) | 2 | A1 | pres-simple-aff | EXISTE(`time-place`) |
| en-g-can-ability | can / can't | 2 | A1 | do-questions | EXISTE(`ability`) |
| en-g-like-ing | like / love / hate + sustantivo o -ing | 2 | A1 | pres-simple-3s | FALTA |
| en-g-object-pron | me / him / us / them | 2 | A1 | pres-simple-aff | EXISTE(`object-possessive`) |
| en-g-possessive-pron | mine / yours… / Whose? | 2 | A1 | object-pron | EXISTE(`object-possessive`) |
| en-g-some-any-basic | some / any con contables e incontables | 2 | A1 | there-is-are | PARCIAL(`quantity`) |
| en-g-pres-continuous | am/is/are + -ing (ahora) | 2 | A1 | be-yesno, pres-simple-3s | EXISTE(`continuous`, hoy nivel 3) |
| en-g-conj-basic | and / but / or / because / so | 2 | A1 | word-order | FALTA |

### A2 (niveles 3–4)

| ID | Título | Nv | CEFR | Prerrequisitos | Estado |
|---|---|---|---|---|---|
| en-g-simple-vs-cont | Presente simple frente a continuo; verbos de estado | 3 | A2 | pres-continuous | PARCIAL(`continuous`) |
| en-g-past-be | was / were | 3 | A2 | be-yesno | EXISTE(`past-be`) |
| en-g-past-regular | -ed (ortografía y pronunciación /t/ /d/ /ɪd/) | 3 | A2 | past-be | PARCIAL(`past`) |
| en-g-past-irregular | Irregulares frecuentes | 3 | A2 | past-regular | PARCIAL(`past`) |
| en-g-past-did | didn't / Did…? / Wh- + did | 3 | A2 | past-irregular, do-questions | PARCIAL(`past`) |
| en-g-going-to | be going to (planes) | 3 | A2 | pres-continuous | EXISTE(`future-plans`) |
| en-g-pres-cont-future | Continuo para acuerdos futuros | 3 | A2 | going-to | PARCIAL(`future-plans`) |
| en-g-will-basic | will (decisión, promesa, predicción) | 3 | A2 | going-to | PARCIAL(`future-plans`) |
| en-g-adverbs-manner | -ly; well / fast / hard | 3 | A2 | adj-position | FALTA |
| en-g-polite-requests | Could you…? / I'd like / Would you like…? | 3 | A2 | can-ability | FALTA |
| en-g-countable-uncount | Contable frente a incontable; a piece of | 4 | A2 | some-any-basic | PARCIAL(`quantity`) |
| en-g-quantifiers | much / many / a lot of / a few / a little / How much/many | 4 | A2 | countable-uncount | EXISTE(`quantity`) |
| en-g-comparatives | -er / more / than / irregulares | 4 | A2 | adj-position | EXISTE(`comparisons`) |
| en-g-superlatives | the -est / the most / in-of | 4 | A2 | comparatives | FALTA |
| en-g-as-as-too-enough | (not) as…as / too / enough | 4 | A2 | comparatives | FALTA |
| en-g-should | should (consejo) | 4 | A2 | can-ability | EXISTE(`advice`) |
| en-g-have-to-must | have to / must / mustn't / don't have to | 4 | A2 | should | EXISTE(`obligation`) |
| en-g-verb-ing-to | want to / enjoy -ing | 4 | A2 | like-ing | EXISTE(`verb-patterns`) |
| en-g-infinitive-purpose | to + verbo (finalidad) | 4 | A2 | verb-ing-to | FALTA |
| en-g-past-continuous | was/were + -ing; when / while | 4 | A2 | past-did, pres-continuous | EXISTE(`past-continuous`, hoy nivel 5) |
| en-g-prep-movement | to / into / across / from | 4 | A2 | prep-place-basic | FALTA |
| en-g-conj-time | when / before / after / then | 4 | A2 | past-did | FALTA |

### B1 (niveles 5–6)

| ID | Título | Nv | CEFR | Prerrequisitos | Estado |
|---|---|---|---|---|---|
| en-g-pp-experience | Present perfect: experiencia (ever / never) | 5 | B1 | past-irregular | PARCIAL(`perfect`) |
| en-g-pp-since-for | Present perfect: duración (since / for) | 5 | B1 | pp-experience | PARCIAL(`perfect`) |
| en-g-pp-just-yet-already | just / yet / already | 5 | B1 | pp-experience | FALTA |
| en-g-pp-vs-past | Present perfect frente a pasado simple | 5 | B1 | pp-since-for | PARCIAL(`perfect`) |
| en-g-used-to | used to / would (hábitos pasados) | 5 | B1 | past-did | FALTA |
| en-g-zero-conditional | Condicional 0 (hechos generales) | 5 | B1 | pres-simple-3s | FALTA |
| en-g-first-conditional | Condicional 1; unless / when | 5 | B1 | zero-conditional, will-basic | EXISTE(`first-conditional`) |
| en-g-may-might | may / might / could (posibilidad) | 5 | B1 | will-basic | FALTA |
| en-g-relative-defining | who / which / that / where | 5 | B1 | conj-basic | EXISTE(`relative`) |
| en-g-passive-basic | Pasiva en presente y pasado | 5 | B1 | past-irregular | EXISTE(`passive-basic`) |
| en-g-pp-continuous | Present perfect continuo | 6 | B1 | pp-since-for | FALTA |
| en-g-past-perfect | had + participio | 6 | B1 | pp-vs-past, past-continuous | EXISTE(`past-perfect`) |
| en-g-second-conditional | Condicional 2 (If I were you) | 6 | B1 | first-conditional | EXISTE(`second`) |
| en-g-reported-statements | Estilo indirecto: say / tell y cambio de tiempos | 6 | B1 | past-perfect | EXISTE(`reported`) |
| en-g-indirect-questions | Preguntas indirectas (Can you tell me where…?) | 6 | B1 | wh-do | PARCIAL(`reporting-questions`) |
| en-g-reported-questions | Preguntas en estilo indirecto (if / whether) | 6 | B1 | reported-statements, indirect-questions | EXISTE(`reporting-questions`) |
| en-g-phrasal-verbs-1 | Phrasal verbs frecuentes (get up, look for) | 6 | B1 | object-pron | FALTA |
| en-g-question-tags | Question tags | 6 | B1 | do-questions, past-did | FALTA |
| en-g-so-such-linkers | so / such; although / however (básico) | 6 | B1 | conj-basic | PARCIAL(`cohesion`, nivel 7) |

### B2 (niveles 7–8)

| ID | Título | Nv | CEFR | Prerrequisitos | Estado |
|---|---|---|---|---|---|
| en-g-third-conditional | Condicional 3 | 7 | B2 | second-conditional, past-perfect | EXISTE(`third-conditional`, hoy nivel 6) |
| en-g-future-cont-perfect | will be -ing / will have + participio | 7 | B2 | will-basic, pp-experience | EXISTE(`future-perfect`) |
| en-g-passive-all | Pasiva en todos los tiempos y con modales | 7 | B2 | passive-basic, pp-since-for | EXISTE(`passive`) |
| en-g-causative | have / get something done | 7 | B2 | passive-all | FALTA |
| en-g-relative-nondef | Relativas explicativas; whose / whom | 7 | B2 | relative-defining | EXISTE(`relative-extra`) |
| en-g-reporting-verbs | suggest / advise / deny + patrón | 7 | B2 | reported-statements, verb-ing-to | FALTA |
| en-g-gerund-inf-meaning | stop / remember / try + -ing o to | 7 | B2 | verb-ing-to | FALTA |
| en-g-phrasal-verbs-2 | Separables, inseparables y de tres partes | 7 | B2 | phrasal-verbs-1 | FALTA |
| en-g-linkers-cause-contrast | because of / due to / therefore / however (puntuación) | 7 | B2 | so-such-linkers | EXISTE(`cohesion`) |
| en-g-wish-if-only | wish / if only (presente y pasado) | 8 | B2 | second-conditional, third-conditional | FALTA |
| en-g-mixed-conditionals | Condicionales mixtos | 8 | B2 | third-conditional | EXISTE(`mixed`) |
| en-g-past-modals-regret | should have / could have / needn't have | 8 | B2 | third-conditional | FALTA |
| en-g-modal-deduction | must / might / can't have | 8 | B2 | may-might, past-modals-regret | EXISTE(`modal-deduction`) |
| en-g-hedging | seem / appear / tend to / may | 8 | B2 | may-might | EXISTE(`hedging`) |
| en-g-concession | although / despite / even though / whereas | 8 | B2 | linkers-cause-contrast | EXISTE(`concession`) |

### C1 (niveles 9–10)

| ID | Título | Nv | CEFR | Prerrequisitos | Estado |
|---|---|---|---|---|---|
| en-g-emphatic-do | Énfasis con auxiliar (I *do* like it) | 9 | C1 | do-questions | FALTA |
| en-g-cleft | It is…that / What I need is… | 9 | C1 | relative-defining | FALTA |
| en-g-negative-inversion | Never / Rarely / Not only / Only later… | 9 | C1 | emphatic-do | EXISTE(`negative-inversion`) |
| en-g-conditional-inversion | Had I / Should you / Were it | 9 | C1 | mixed-conditionals | EXISTE(`condition-inversion`) |
| en-g-participle-clauses | Having finished… / Built in… | 9 | C1 | relative-nondef, passive-all | FALTA |
| en-g-ellipsis-substitution | so / do so / one / elipsis | 9 | C1 | question-tags | FALTA |
| en-g-reference | Referencia no ambigua (this / which / such) | 9 | C1 | relative-nondef | EXISTE(`reference`) |
| en-g-advanced-modality | be to / be bound to / would rather / had better / need not | 9 | C1 | modal-deduction | FALTA |
| en-g-formal-hypothesis | Were it not for / Had it not been for | 10 | C1 | conditional-inversion | EXISTE(`were-it-not`) |
| en-g-nominalisation | Nominalización y estilo escrito | 10 | C1 | participle-clauses | FALTA |
| en-g-register-editing | Registro, concordancia y edición | 10 | C1 | reference, hedging | EXISTE(`editing-register`) |
| en-g-cohesion-extended | Cohesión de párrafo y texto (tema-rema, foco) | 10 | C1 | cleft, reference | FALTA |

### C2 (planificado · nivel interno reservado `null`)

| ID | Título | Prerrequisitos | Estado |
|---|---|---|---|
| en-g-c2-mandative-subjunctive | insist / demand that he *be* | formal-hypothesis | FALTA |
| en-g-c2-fronting-literary | Anteposición e inversión estilística (Down came the rain) | negative-inversion | FALTA |
| en-g-c2-modal-nuance | Matiz modal fino (might well, can't but, would have thought) | advanced-modality | FALTA |
| en-g-c2-register-shift | Cambio de registro y de tono en un mismo texto | register-editing | FALTA |
| en-g-c2-pragmatics | Ironía, *understatement*, cortesía indirecta | cohesion-extended | FALTA |
| en-g-c2-idiomatic-grammar | Estructuras idiomáticas (the more…the more, be that as it may) | concession | PARCIAL(`concession` menciona *be that as it may*) |

Recuento: 111 nodos (105 con nivel y 6 C2 reservados). De ellos, 43 son EXISTE, 27 PARCIAL y 41 FALTA. **Las 43 guías actuales quedan enlazadas**, algunas a varios nodos.

## Por idioma: sistema lingüístico, ruta de fundamentos, A1 inicial y mapa A2–C2

Regla común (decisión del usuario sobre DEC-004): todo texto de explicación, traducción, glosa, error típico y feedback se guarda como mapa `{es: …, en: …}` según el idioma de apoyo. Como mínimo habrá `es` en los 9 cursos actuales y `en` en el curso de español. Por eso las unidades se definen con **claves de contenido** y no con cadenas en español; el vocabulario de las tablas lleva la glosa `es`, que es la primera que se escribirá. La romanización (`romanizacion`) no depende del idioma de apoyo.

### Alemán (de)

**Sistema.**
- Alfabeto latino más ä, ö, ü y ß; todos los sustantivos con mayúscula.
- Tres géneros (der/die/das), poco predecibles: cada sustantivo se aprende **con su artículo** y su plural.
- Cuatro casos; en A1 solo nominativo y acusativo (el acusativo cambia solo en masculino: den/einen).
- Conjugación por persona (-e, -st, -t, -en, -t, -en). Tratamiento du/Sie, y la ambigüedad sie/Sie.
- **Verbo en segunda posición (V2)**, *Satzklammer* con modales y verbos separables, y verbo al final en las subordinadas.
- Negación con nicht o kein.
- Para hispanohablantes: vocales largas y cortas, ü/ö, ch (ich/ach), r uvular, z = [ts], w = [v], v = [f] y ensordecimiento final.

**Fundamentos (N0):**
- f0 sonidos y saludos
- f1 pronombres y du/Sie
- f2 *sein*, *heißen* y *kommen aus*
- f3 der/die/das y ein/eine
- f4 nicht y kein
- f5 preguntas W y V2
- f6 presentarse

**A1 inicial (N1–2):**
- Presente de verbos regulares (wohnen, lernen, arbeiten), *haben* y *möchten*.
- Acusativo con *haben*, *brauchen* y *möchten*.
- Plurales por patrones.
- Números, precio y hora.
- Artículos posesivos mein/dein/Ihr.
- *können* y la *Satzklammer*.
- Verbos separables (aufstehen, einkaufen).
- Imperativo con *Sie*.
- in/an + dativo de lugar, primero como fórmula fija.

**Mapa A2–C2:**
- **A2:** Perfekt (haben/sein + Partizip II), dativo completo, preposiciones de doble caso, subordinadas con weil/dass/wenn, comparativo, verbos reflexivos, *war*/*hatte*.
- **B1:** Präteritum narrativo, relativas, pasiva, Konjunktiv II, genitivo, *zu* + infinitivo, declinación completa del adjetivo.
- **B2:** pasiva con modales, Konjunktiv I (estilo indirecto), atributos de participio, estilo nominal, conectores dobles.
- **C1:** Funktionsverbgefüge, partículas modales, modales de uso subjetivo, registro académico.
- **C2:** estilística y variedades de Austria y Suiza.

### Japonés (ja)

**Sistema.**
- Tres escrituras: hiragana (46 + diacríticos), katakana (préstamos y nombres) y kanji (con furigana en A1).
- Cómputo por **moras**, vocales largas, っ (geminada) y ん; acento tonal.
- Las 5 vocales son muy parecidas a las españolas, una **ventaja**.
- Orden SOV.
- **Partículas** posposicionales: は (se lee *wa*), が, を (se lee *o*), に, で, の, も, か, と.
- No hay género, artículos ni plural obligatorio, y el sujeto se omite.
- Los verbos no se conjugan por persona sino por tiempo, polaridad y **nivel de cortesía** (です/ます primero; forma llana después).
- Adjetivos い/な.
- Contadores.

**Fundamentos (N0), primero la escritura:**
- f0 vocales y saludos
- f1 hiragana completo
- f2 diacríticos, ゃゅょ, っ y vocales largas
- f3 katakana y tu nombre
- f4 N は N です
- f5 自己紹介 (presentarse)

**A1 inicial:**
- これ/それ/あれ + の.
- も.
- Verbo en ます con を/に/で.
- あります/います.
- Números, precios, horas y contadores (〜えん, 〜じ, 〜つ).
- ました/ませんでした.
- Adjetivos い/な en presente.
- Preguntas con なに/どこ/だれ + か.
- Primeros 20 kanji (人, 日, 本, 一〜十).

**Mapa A2–C2:**
- **A2:** forma て (ています, てください, てもいい), forma llana (diccionario/ない/た), たい, comparación より/ほうが, から/けど.
- **B1:** forma potencial, condicionales と/ば/たら/なら, pasiva, あげる/くれる/もらう, そうだ/ようだ/らしい, 敬語 básico.
- **B2:** causativa y causativa-pasiva, 尊敬語/謙譲語, わけ/はず/べき, nominalizadores こと/の.
- **C1:** registro escrito (である), expresiones de nivel N2/N1, unos 2000 kanji.
- **C2:** keigo empresarial, matices literarios y dialectos (Kansai).

### Chino mandarín (zh)

**Sistema.**
- Hanzi simplificados, con **pinyin como andamio** que se retira de forma progresiva.
- **Cuatro tonos y el neutro**, con sandhi (3.º + 3.º, 不 y 一).
- Iniciales difíciles: aspiradas b/p, retroflejas zh/ch/sh/r, j/q/x y ü.
- Lengua aislante: **sin conjugación**, género ni plural (们 solo con personas).
- Tiempo y lugar van antes del verbo.
- Aspecto con 了/过/着 en lugar de tiempos verbales.
- **Clasificadores** obligatorios tras número o demostrativo.
- 是 solo une sustantivos; los adjetivos llevan 很.
- Preguntas con 吗, con A-不-A o con pronombre interrogativo en su sitio.

**Fundamentos (N0):**
- f0 tonos y saludos
- f1 iniciales del pinyin
- f2 finales y sandhi
- f3 trazos y 12 caracteres base
- f4 我/你/他 + 是 / 不是 + 吗
- f5 presentarse con 叫 y 人

**A1 inicial:**
- 很 + adjetivo y 呢.
- 的 posesivo.
- 有 / 没有 (se niega con 没).
- 这/那 + 个/本/杯.
- Números, 块 y 点.
- 在 + lugar.
- 想/要/会/能.
- 了 de acción terminada, en su uso básico.
- 什么/哪儿/谁/几/多少.

**Mapa A2–C2:**
- **A2:** 过, 了 de cambio de estado, complementos de resultado, 比, 正在, 就/才, 因为…所以.
- **B1:** complementos direccionales y potenciales, 把, 被, 是…的, 虽然…但是, 越来越.
- **B2:** 连…都, complementos complejos, registro formal, chengyu frecuentes.
- **C1:** 书面语 (之/其/以) y conectores formales.
- **C2:** alusiones literarias, chengyu en contexto y lectura en tradicional.

### Coreano (ko)

**Sistema.**
- **Hangul**: letras combinadas en bloques silábicos, con consonante final (받침) de 7 sonidos.
- Reglas fonológicas: enlace (연음), asimilación nasal y tensificación.
- Contraste **simple / aspirada / tensa** (ㄱ/ㅋ/ㄲ), difícil para hispanohablantes.
- Orden SOV.
- **Partículas** que alternan según la palabra termine en vocal o consonante (은/는, 이/가, 을/를).
- Los verbos se conjugan por tiempo y **nivel de habla** (해요체 primero, 합니다체 y 반말 después), no por persona.
- Honorífico -시-.
- **Dos sistemas numéricos**: nativo (하나, 둘) y sino-coreano (일, 이), con usos distintos.

**Fundamentos (N0):**
- f0 vocales y saludos
- f1 consonantes y bloques
- f2 aspiradas, tensas y 받침
- f3 reglas de sonido
- f4 이에요/예요 + 은/는
- f5 presentarse

**A1 inicial:**
- 있어요/없어요.
- 이거/그거/저거.
- Números sino-coreanos y precios (원).
- Números nativos con 개, 명 y 시.
- 해요체 en presente (-아요/-어요/해요).
- 을/를, 에/에서, negación con 안.
- -고 싶어요.
- Pasado -았/었어요.
- 이/가 frente a 은/는, en su contraste básico.

**Mapa A2–C2:**
- **A2:** -고, -아서/어서, -(으)면, -(으)ㄹ 거예요, -(으)ㄹ 수 있다, -지 마세요, 합니다체, irregulares ㅂ/ㄷ/ㅡ/르.
- **B1:** modificadores -(으)ㄴ/는/(으)ㄹ, -는데, -(으)니까, honoríficos -시- con su vocabulario, estilo indirecto básico.
- **B2:** pasiva y causativa (피동/사동), -더라고요, estilo indirecto -다고/-냐고, conjetura.
- **C1:** estilo escrito en -다, vocabulario sino-coreano académico, 속담.
- **C2:** pragmática fina, dialectos y prensa o literatura.

### Ruso (ru)

**Sistema.**
- **Cirílico** de 33 letras, con falsos amigos (В = v, Н = n, Р = r, С = s, У = u, Х = j).
- **Acento libre y móvil**, con reducción de vocales átonas (о átona suena [a]).
- Consonantes duras y blandas (ь, ъ, ы) y ensordecimiento final.
- **Sin "ser" en presente** (Я студент) y sin artículos.
- Tres géneros, reconocibles por la terminación.
- **Seis casos**: el nominativo primero, y el prepositivo de lugar como primer caso nuevo.
- Posesión con У меня есть.
- Conjugaciones 1.ª y 2.ª, **aspecto** perfectivo e imperfectivo, verbos de movimiento.
- Orden de palabras flexible.
- La romanización se retira al terminar f2.

**Fundamentos (N0):**
- f0 letras "amigas" y saludos
- f1 letras nuevas
- f2 acento, reducción, ь y ы
- f3 я/ты/вы sin verbo y Это…
- f4 género он/она/оно y мой/моя/моё
- f5 presentarse (Меня зовут, не)

**A1 inicial:**
- Plural en nominativo.
- Presente de la 1.ª conjugación (читать) y de la 2.ª (говорить).
- **Prepositivo** con в/на (в Москве, на работе).
- Acusativo de objeto inanimado.
- У меня есть.
- Adjetivo concordado en nominativo.
- Edad (мне … лет, como fórmula).
- Pasado en -л/-ла/-ло/-ли.

**Mapa A2–C2:**
- **A2:** genitivo (posesión, cantidad, нет), dativo (нравится, edad), instrumental (с, profesión), pares de aspecto, futuro, идти/ходить.
- **B1:** todos los casos en plural, verbos de movimiento con prefijo, imperativo, бы, который, comparativo.
- **B2:** participios y gerundios, pasiva, aspecto en imperativo y negación.
- **C1:** registro oficial y científico, matices aspectuales.
- **C2:** fraseología y estilística.

### Francés (fr)

**Sistema.**
- **Ortografía alejada de la pronunciación**: finales mudas, nasales (an/en, on, in, un), vocales redondeadas u/eu, e caduca y r uvular.
- **Liaison y enchaînement**.
- Dos géneros; el artículo suele ser **la única marca oral del plural**.
- Pronombre sujeto **obligatorio** (a diferencia del español).
- *être* y *avoir*; **edad con avoir** (j'ai 20 ans).
- Negación ne…pas (el *ne* se pierde en el habla oral).
- Tratamiento tu/vous; *on* = nosotros.
- Partitivo du/de la.
- Tres registros de pregunta: entonación, *est-ce que* e inversión.
- Falsos amigos con el español.

**Fundamentos (N0):**
- f0 sonidos y saludos
- f1 nasales y liaison
- f2 pronombres, tu/vous y on
- f3 *être*
- f4 género, artículos y concordancia del adjetivo
- f5 ne…pas y est-ce que
- f6 presentarse

**A1 inicial:**
- Verbos en -er.
- *avoir* (con la edad).
- *il y a*.
- Partitivo.
- mon/ma/mes.
- *aller*/*faire* y futur proche.
- à/de con contracciones (au, du).
- Posición del adjetivo.
- qu'est-ce que / où / quand.

**Mapa A2–C2:**
- **A2:** passé composé (avoir/être y concordancia), pronombres COD/COI, verbos pronominales, futur simple, comparativo.
- **B1:** imparfait frente a passé composé, subjuntivo presente, condicional, y/en, qui/que/où/dont, plus-que-parfait.
- **B2:** subjuntivo ampliado, pasiva, estilo indirecto, gérondif, conectores.
- **C1:** passé simple (solo reconocimiento), registro soutenu, nominalización.
- **C2:** estilística, argot y verlan.

### Italiano (it)

**Sistema.**
- Ortografía casi fonética, una **ventaja**. Lo difícil: ci/chi, ge/ghe, gli, gn, sc y las **consonantes dobles** (pala/palla).
- Pro-drop, como el español.
- Artículos variables según el sonido inicial: il/lo/la/l', un/uno/una/un'; plural i/gli/le.
- Plural por cambio de vocal.
- *essere* se usa también para el lugar (sono a casa) y *stare* para la salud (sto bene).
- Conjugaciones -are/-ere/-ire.
- *Lei* formal, en 3.ª persona.
- Preposiciones articuladas.
- Posesivo con artículo, salvo con familiares en singular.

**Fundamentos (N0):**
- f0 sonidos y saludos
- f1 c/g, gli/gn y dobles
- f2 io/tu/Lei
- f3 *essere*/*stare*
- f4 género y artículos
- f5 presentarse

**A1 inicial:**
- Verbos en -are.
- *avere* (con la edad).
- c'è / ci sono.
- Posesivos con artículo.
- Preposiciones articuladas.
- mi piace / mi piacciono.
- andare / fare / volere / potere.
- chi / che cosa / dove / quanto.

**Mapa A2–C2:**
- **A2:** passato prossimo (avere/essere y concordancia), reflexivos, futuro, pronombres directos, introducción al imperfetto.
- **B1:** imperfetto frente a prossimo, condizionale, ci/ne, congiuntivo presente, che/cui, trapassato.
- **B2:** congiuntivo imperfetto y trapassato, periodo ipotetico, pasiva con venire/andare, estilo indirecto.
- **C1:** passato remoto y registro burocrático.
- **C2:** estilística y variedades regionales.

### Portugués (pt, variante de Brasil: `localeVoz` = pt-BR)

**Sistema.**
- Nasales (ã, õ, -ão, -em) y vocales abiertas o cerradas (é/ê, ó/ô).
- Reducción átona (e suena [i] y o suena [u] en Brasil); t/d palatalizadas ante i.
- Dígrafos lh y nh.
- **ser/estar con un reparto casi igual al español, una ventaja clara**; se añade *ficar*.
- *você* va con verbo en 3.ª persona; *a gente* se usa como nosotros.
- Contracciones **obligatorias** (no, na, do, da, pelo).
- *gostar de* lleva preposición.
- Infinitivo personal y futuro de subjuntivo (en B1).
- **Falsos amigos** que conviene tratar pronto: esquisito, polvo, apelido, oficina, borracha.

**Fundamentos (N0):**
- f0 sonidos y saludos
- f1 nasales y vocales
- f2 eu/você/a gente
- f3 ser/estar
- f4 género y contracciones
- f5 presentarse y falsos amigos

**A1 inicial:**
- Verbos en -ar.
- *ter* (con la edad).
- *tem* = hay.
- meu/minha.
- ir + infinitivo.
- *gostar de*.
- querer/poder.
- o que / onde / quanto.
- Números y reales.

**Mapa A2–C2:**
- **A2:** pretérito perfeito, imperfeito, reflexivos, comparativos, pronombres objeto (uso coloquial de Brasil frente a la norma), estar + gerúndio.
- **B1:** futuro do pretérito, subjuntivo presente, futuro de subjuntivo, infinitivo personal, mais-que-perfeito composto.
- **B2:** subjuntivo imperfeito, pasiva, colocación pronominal culta, estilo indirecto.
- **C1:** registro formal y variedades de Brasil y Portugal.
- **C2:** estilística.

### Español (es) — para aprendices no hispanohablantes, empezando por nativos de inglés, con explicaciones en inglés (DEC-004 opción a)

**Problema actual.** El contenido es monolingüe:
- Glosas en español: `hola` → "saludo general".
- N0-U2 enseña "la ñ" en español.
- Toda explicación se escribe en español (`es/nivel-1.json`).

Para un nativo de inglés es incomprensible, y a un hispanohablante no le aporta nada. **Nada del contenido `es` actual sirve como texto de explicación; solo se reutilizan las frases meta** (diálogos y ejemplos), tras revisarlas.

**Sistema, visto por un anglohablante.**
- Vocales puras (5) y ortografía casi fonética.
- r/rr, j, ñ, ll/y (yeísmo), b = v, h muda.
- Acento gráfico.
- **Pro-drop**: se omite el sujeto.
- Dos géneros y concordancia de adjetivo y artículo.
- **ser/estar**, el gran escollo para anglohablantes.
- Conjugación por persona (6 formas).
- tú/usted (y vos o vosotros según la región; hay que decidir la variante).
- Clíticos.
- Pretérito frente a imperfecto.
- Subjuntivo.
- *gustar* con construcción inversa.

**Fundamentos (N0), explicaciones en `en`:**
- f0 sonidos y saludos
- f1 yo/tú/usted y pro-drop
- f2 *ser*
- f3 género y artículos
- f4 *estar* frente a *ser*
- f5 presentarse

**A1 inicial:**
- Verbos en -ar/-er/-ir en presente.
- *tener* (edad, hambre).
- *hay*.
- Posesivos.
- ir a + infinitivo.
- *gustar* (me gusta / me gustan).
- Preguntas (qué, dónde, cuánto).
- Números y precios.
- Irregulares frecuentes (ir, hacer, querer, poder).

**Mapa A2–C2:**
- **A2:** pretérito indefinido, imperfecto, reflexivos, pronombres de objeto directo e indirecto, comparativos, estar + gerundio.
- **B1:** indefinido frente a imperfecto, pretérito perfecto, futuro y condicional, subjuntivo presente (deseo, duda), imperativo, relativos.
- **B2:** subjuntivo imperfecto, condicionales 2 y 3, pasiva y *se*, estilo indirecto.
- **C1:** registro académico y variación americana y peninsular.
- **C2:** estilística y fraseología.

## Unidades iniciales implementables por idioma

Criterio de dominio común, que el agente C debe afinar: ≥ 85 % en una **comprobación independiente sin ayudas**, con ejemplos nuevos, **y** recuperación diferida (≥ 24 h), **y** una producción corta (oral o escrita) evaluada. Completar la práctica guiada solo significa "practicado con apoyo". En la tabla, el vocabulario va como *palabra (romanización) = glosa `es`*; en el español, la glosa es `en`.

### Inglés (en)

| ID | Objetivo comunicativo | Prerreq. | Gramática | Vocabulario | Pronunciación / escritura | Dominio |
|---|---|---|---|---|---|---|
| en-f0-primer-contacto | Saludar, despedirse, agradecer | — | Ninguna (bloques fijos) | hello = hola, hi = hola (informal), goodbye = adiós, bye = chao, please = por favor, thank you = gracias, yes = sí, no = no, sorry = perdón, excuse me = disculpe | La grafía no predice el sonido: *h* aspirada, th en *thank*, vocal de *bye* | Reconoce 8 de 10 solo por audio y responde a un saludo |
| en-f1-pronombres | Señalar quién habla o de quién se habla | f0 | I, you (singular y plural), he, she, it, we, they; sujeto obligatorio | I = yo, you = tú / usted / ustedes, he = él, she = ella, it = eso (cosa o animal), we = nosotros, they = ellos/ellas, man = hombre, woman = mujer, friend = amigo/a, dog = perro | *I* siempre en mayúscula; /ð/ de *they* | Elige el pronombre ante una imagen o situación (≥ 90 %) y distingue *it* de *he* |
| en-f2-be-afirmativo | Decir quién o cómo es alguien | f1 | am/is/are por persona; contracciones I'm / you're / he's / she's / it's / we're / they're; ser y estar con una sola forma | happy = feliz, tired = cansado/a, student = estudiante, teacher = profesor/a, from = de (origen), here = aquí, at home = en casa, ready = listo/a | Forma débil de *are*; *'s* suena /z/ | Produce la forma correcta con los 7 pronombres, 24 h después |
| en-f3-negacion | Negar datos personales | f2 | not; I'm not / isn't / aren't (*amn't* no existe) | hungry = con hambre, busy = ocupado/a, sad = triste, late = tarde, cold = frío (tener frío), hot = calor, sick = enfermo/a, OK = bien | Contracciones *isn't* /ɪznt/ y *aren't* | Transforma 8 frases afirmativas en negativas sin modelo |
| en-f4-preguntas | Preguntar y responder sí/no | f3 | Inversión Are you…? / Is she…?; respuestas cortas Yes, I am / No, I'm not (sin contracción en la afirmativa) | really? = ¿de verdad?, right? = ¿verdad?, now = ahora, today = hoy, sure = claro, maybe = quizás, too = también, OK? = ¿vale? | Entonación ascendente en preguntas sí/no | Responde 8 preguntas con la respuesta corta correcta y formula 3 preguntas |
| en-f5-presentarse | Presentarse y preguntar a otro | f4 | What's / Where + be; *my/your* como bloque (sin enseñarlos formalmente) | name = nombre, country = país, city = ciudad, Ecuador, Spain = España, Mexico = México, How are you? = ¿cómo estás?, fine = bien, Nice to meet you = mucho gusto, Where are you from? = ¿de dónde eres? | Formas débiles en *What's your name?* | Diálogo de 4 turnos con datos nuevos, sin modelo |

### Alemán (de)

| ID | Objetivo | Prerreq. | Gramática | Vocabulario | Pronunciación / escritura | Dominio |
|---|---|---|---|---|---|---|
| de-f0-laute-gruesse | Saludar y despedirse | — | Bloques fijos | Hallo = hola, Guten Morgen = buenos días, Guten Tag = buenos días (tarde), Guten Abend = buenas noches (saludo), Tschüss = chao, Auf Wiedersehen = adiós, danke = gracias, bitte = por favor / de nada, ja = sí, nein = no, Entschuldigung = perdón | ä, ö, ü; ei = [ai] frente a ie = [i:]; w = [v]; z = [ts]; ch; ß | Discrimina ei/ie y ü/u por audio (≥ 85 %) |
| de-f1-pronomen-du-sie | Elegir el tratamiento | f0 | ich, du, er, sie, es, wir, ihr, sie/**Sie**; du frente a Sie | ich = yo, du = tú, Sie = usted(es), er = él, sie = ella / ellos, es = ello, wir = nosotros, ihr = vosotros / ustedes (informal), Herr = señor, Frau = señora | *Sie* con mayúscula | Elige du o Sie en 8 situaciones sociales |
| de-f2-sein-heissen | Decir nombre y origen | f1 | sein (bin, bist, ist, sind, seid, sind); ich heiße / du heißt / Sie heißen; ich komme aus | Ecuador, Spanien = España, Mexiko = México, Deutschland = Alemania, Student/Studentin = estudiante, Lehrer/Lehrerin = profesor/a, müde = cansado/a, gut = bien, hier = aquí | ß en *heiße*; -er final = [ɐ] | Conjuga *sein* con las 8 personas y produce 3 frases de presentación |
| de-f3-der-die-das | Nombrar objetos con su artículo | f2 | Género; der/die/das y ein/eine en nominativo; sustantivos con mayúscula; plural *die* | der Tisch = la mesa, der Stuhl = la silla, der Mann = el hombre, die Frau = la mujer, die Tür = la puerta, die Lampe = la lámpara, das Buch = el libro, das Kind = el niño, das Haus = la casa, das Handy = el móvil, der Kaffee = el café, die Stadt = la ciudad | Mayúscula inicial del sustantivo; tarjeta de color por género | Recuerda el artículo de 10 sustantivos 24 h después (≥ 80 %, porque el género es arbitrario) |
| de-f4-nicht-kein | Negar | f3 | nicht (verbo o adjetivo) frente a kein/keine (sustantivo indefinido) | nicht = no, kein = ningún / no un, müde, krank = enfermo/a, verheiratet = casado/a, Zeit = tiempo, Problem = problema, Hunger = hambre | kein [kaɪn] | Elige nicht o kein correctamente en 10 frases nuevas |
| de-f5-fragen-v2 | Preguntar y responder | f4 | W-Frage con el verbo en posición 2; pregunta sí/no con el verbo en posición 1; V2 en la afirmación (Heute bin ich müde) | wie = cómo, wo = dónde, woher = de dónde, was = qué, wer = quién, wohnen = vivir, heute = hoy, jetzt = ahora | Entonación de la pregunta sí/no | Ordena 8 frases con V2 correcto y hace 3 preguntas W |

### Japonés (ja)

| ID | Objetivo | Prerreq. | Gramática | Vocabulario | Escritura / pronunciación | Dominio |
|---|---|---|---|---|---|---|
| ja-f0-kana-aisatsu | Leer vocales y saludar | — | Bloques fijos | こんにちは (konnichiwa) = hola, おはようございます (ohayō gozaimasu) = buenos días, ありがとう (arigatō) = gracias, すみません (sumimasen) = disculpe, はい (hai) = sí, いいえ (iie) = no, さようなら (sayōnara) = adiós, あい (ai) = amor, いえ (ie) = casa, うえ (ue) = arriba | あいうえお; ritmo por moras; は se lee *wa* en こんにちは | Lee las 5 vocales y 8 saludos sin romanización |
| ja-f1-hiragana | Leer hiragana | f0 | — | かさ (kasa) = paraguas, すし (sushi), ねこ (neko) = gato, いぬ (inu) = perro, さかな (sakana) = pescado, みず (mizu) = agua, なまえ (namae) = nombre, ほん (hon) = libro, やま (yama) = montaña, くるま (kuruma) = coche | 46 kana básicos con orden de trazos; ん | Lee 40 de 46 kana en menos de 3 s cada uno, 24 h después |
| ja-f2-dakuten-yoon | Leer sonidos derivados | f1 | — | がくせい (gakusei) = estudiante, せんせい (sensei) = profesor/a, でんしゃ (densha) = tren, きょう (kyō) = hoy, ちょっと (chotto) = un poco, がっこう (gakkō) = escuela, おかあさん (okāsan) = madre, ぎゅうにゅう (gyūnyū) = leche | Diacríticos ゛ y ゜; ゃゅょ; っ; vocales largas | Distingue largo/corto y geminada por audio (≥ 85 %) |
| ja-f3-katakana | Leer préstamos y escribir el propio nombre | f2 | — | コーヒー (kōhī) = café, パン (pan) = pan, テレビ (terebi) = televisión, ホテル (hoteru) = hotel, カメラ (kamera) = cámara, エクアドル (Ekuadoru) = Ecuador, メキシコ (Mekishiko) = México, スペイン (Supein) = España, アナ (Ana) | ー; adaptación fonológica de nombres extranjeros | Escribe su nombre en katakana y lee 10 préstamos |
| ja-f4-desu | Identificarse | f3 | N は N です / じゃありません / ですか; sujeto omitido; は = tema | わたし (watashi) = yo, がくせい = estudiante, せんせい = profesor/a, かいしゃいん (kaishain) = empleado/a, いしゃ (isha) = médico/a, 〜じん (-jin) = nacionalidad, にほん (Nihon) = Japón, はい/いいえ | は se lee *wa*; か sin signo de interrogación | Produce afirmación, negación y pregunta con 6 sustantivos nuevos |
| ja-f5-jikoshoukai | Presentarse con cortesía | f4 | の posesivo (わたしの なまえ); 〜から きました como bloque; さん con otros, nunca con uno mismo | はじめまして (hajimemashite) = encantado/a (primera vez), よろしく おねがいします (yoroshiku onegaishimasu) = un placer / cuento con usted, なまえ = nombre, 〜さん = señor/a, どうぞ = adelante, から (kara) = desde, おなまえは？ = ¿su nombre? | Pausa y reverencia como parte pragmática | Presentación de 4 frases y uso correcto de さん |

### Chino mandarín (zh)

| ID | Objetivo | Prerreq. | Gramática | Vocabulario | Escritura / pronunciación | Dominio |
|---|---|---|---|---|---|---|
| zh-f0-shengdiao | Oír los tonos y saludar | — | Bloques fijos | 你好 (nǐ hǎo) = hola, 谢谢 (xièxie) = gracias, 不客气 (bú kèqi) = de nada, 再见 (zàijiàn) = adiós, 对不起 (duìbuqǐ) = perdón, 没关系 (méi guānxi) = no pasa nada, 妈 (mā) = mamá, 马 (mǎ) = caballo, 骂 (mà) = regañar, 麻 (má) = cáñamo | 4 tonos y neutro; curva tonal visual | Identifica el tono de sílabas aisladas (≥ 85 %) |
| zh-f1-pinyin-shengmu | Leer iniciales | f0 | — | 爸爸 (bàba) = papá, 怕 (pà) = temer, 他 (tā) = él, 去 (qù) = ir, 学 (xué) = estudiar, 吃 (chī) = comer, 是 (shì) = ser, 人 (rén) = persona, 知道 (zhīdào) = saber, 茶 (chá) = té | Aspiración b/p y d/t; zh/ch/sh/r; j/q/x | Discrimina pares mínimos b/p, zh/j y sh/x (≥ 80 %) |
| zh-f2-yunmu-biandiao | Leer finales y aplicar el sandhi | f1 | — | 女 (nǚ) = mujer, 绿 (lǜ) = verde, 忙 (máng) = ocupado, 冷 (lěng) = frío, 很好 (hěn hǎo → hén hǎo) = muy bien, 不是 (bù shì → bú shì) = no ser, 一个 (yí ge) = uno, 你好 (ní hǎo) | ü; -n/-ng; sandhi de 3.º + 3.º, 不 y 一 | Lee 10 combinaciones con el sandhi correcto |
| zh-f3-bihua-hanzi | Reconocer caracteres base | f2 | — | 人 (rén) = persona, 口 (kǒu) = boca, 日 (rì) = sol / día, 月 (yuè) = luna / mes, 木 (mù) = árbol, 水 (shuǐ) = agua, 火 (huǒ) = fuego, 大 (dà) = grande, 小 (xiǎo) = pequeño, 中 (zhōng) = medio, 一 (yī) / 二 (èr) / 三 (sān) = 1 / 2 / 3 | 8 trazos básicos y orden de trazos | Reconoce 12 caracteres sin pinyin, 24 h después |
| zh-f4-wo-shi | Identificar personas | f3 | 我/你/他/她 + 们; 是 / 不是 (sin conjugación); pregunta con 吗 | 我 (wǒ) = yo, 你 (nǐ) = tú, 他/她 (tā) = él / ella, 我们 (wǒmen) = nosotros, 学生 (xuésheng) = estudiante, 老师 (lǎoshī) = profesor/a, 医生 (yīshēng) = médico/a, 中国人 (Zhōngguó rén) = chino/a | 他 y 她 suenan igual | Produce afirmación, negación y pregunta con 吗; no usa 是 con adjetivos |
| zh-f5-jieshao | Presentarse | f4 | 叫 + nombre; 什么 en su sitio; 很 + adjetivo (很高兴) | 叫 (jiào) = llamarse, 名字 (míngzi) = nombre, 什么 (shénme) = qué, 厄瓜多尔 (Èguāduō'ěr) = Ecuador, 墨西哥 (Mòxīgē) = México, 西班牙 (Xībānyá) = España, 哪国人 (nǎ guó rén) = ¿de qué país?, 很高兴认识你 (hěn gāoxìng rènshi nǐ) = encantado/a | Tonos en frase completa | Diálogo de 4 turnos con tonos inteligibles (evaluación humana o por IA) |

### Coreano (ko)

| ID | Objetivo | Prerreq. | Gramática | Vocabulario | Escritura / pronunciación | Dominio |
|---|---|---|---|---|---|---|
| ko-f0-moeum-insa | Leer vocales y saludar | — | Bloques fijos | 안녕하세요 (annyeonghaseyo) = hola, 감사합니다 (gamsahamnida) = gracias, 네 (ne) = sí, 아니요 (aniyo) = no, 죄송합니다 (joesonghamnida) = perdón, 안녕히 가세요 (annyeonghi gaseyo) = adiós (a quien se va), 안녕히 계세요 (annyeonghi gyeseyo) = adiós (a quien se queda), 아이 (ai) = niño, 오이 (oi) = pepino, 우유 (uyu) = leche | ㅏ ㅓ ㅗ ㅜ ㅡ ㅣ ㅐ ㅔ; ㅇ muda al inicio | Lee las 10 vocales básicas y distingue ㅓ de ㅗ por audio |
| ko-f1-jaeum-bloques | Formar sílabas | f0 | — | 나무 (namu) = árbol, 바다 (bada) = mar, 가수 (gasu) = cantante, 모자 (moja) = gorro, 사자 (saja) = león, 하나 (hana) = uno, 누나 (nuna) = hermana mayor (de un chico), 라디오 (radio) | 14 consonantes simples; bloques CV | Lee 20 sílabas CV nuevas (≥ 90 %) |
| ko-f2-gyeokeum-batchim | Distinguir los tres tipos de consonante y leer la final | f1 | — | 커피 (keopi) = café, 토마토 (tomato), 아빠 (appa) = papá, 싸요 (ssayo) = es barato, 물 (mul) = agua, 밥 (bap) = arroz / comida, 김치 (gimchi), 한국 (Hanguk) = Corea, 책 (chaek) = libro | ㄱ/ㅋ/ㄲ, ㄷ/ㅌ/ㄸ, ㅂ/ㅍ/ㅃ, ㅈ/ㅊ/ㅉ, ㅅ/ㅆ; los 7 sonidos del 받침 | Discrimina el trío de consonantes por audio (≥ 75 %, un contraste difícil) |
| ko-f3-eumun-gyuchik | Leer como se habla | f2 | — | 한국어 (han-gu-geo) = coreano, 음악 (eu-mak) = música, 감사합니다 (gam-sa-ham-ni-da), 옷이 (o-si) = la ropa, 십만 (sim-man) = 100 000, 앉아요 (an-ja-yo) = me siento | Enlace (연음), asimilación nasal (-ㅂ니다 se lee -mnida) | Lee 8 palabras aplicando la regla sin ayuda |
| ko-f4-ieyo-yeyo | Identificarse | f3 | N이에요 (tras consonante) / N예요 (tras vocal); negación 이/가 아니에요; 저는 con 은/는 como tema; pregunta con entonación | 저 (jeo) = yo (humilde), 학생 (haksaeng) = estudiante, 선생님 (seonsaengnim) = profesor/a, 의사 (uisa) = médico/a, 회사원 (hoesawon) = empleado/a, 사람 (saram) = persona, 이름 (ireum) = nombre, 친구 (chingu) = amigo/a | 받침 y la elección de la partícula | Elige 이에요 o 예요 y 은 o 는 en 12 casos nuevos (≥ 90 %) |
| ko-f5-jagisogae | Presentarse | f4 | 이름이 뭐예요?; 〜 사람이에요 (nacionalidad); 해요체 como nivel por defecto | 에콰도르 (Ekwadoreu) = Ecuador, 멕시코 (Meksiko) = México, 스페인 (Seupein) = España, 한국 사람 = coreano/a, 만나서 반가워요 (mannaseo bangawoyo) = encantado/a, 뭐 (mwo) = qué, 어디 (eodi) = dónde, 씨 (ssi) = sr./sra. (tras el nombre) | Entonación de 해요체 | Presentación de 4 frases sin romanización |

### Ruso (ru)

| ID | Objetivo | Prerreq. | Gramática | Vocabulario | Escritura / pronunciación | Dominio |
|---|---|---|---|---|---|---|
| ru-f0-kirillitsa-1 | Leer letras "amigas" y saludar | — | Bloques fijos | привет (privet) = hola (informal), здравствуйте (zdrávstvuyte) = hola (formal), спасибо (spasíbo) = gracias, пожалуйста (pozhálusta) = por favor / de nada, да (da) = sí, нет (net) = no, пока (poká) = chao, мама (máma) = mamá, кот (kot) = gato, такси (taksí) = taxi | А, К, М, О, Т, Е; falsos amigos В, Н, Р, С, У, Х | Lee 10 palabras con falsos amigos sin error de letra |
| ru-f1-kirillitsa-2 | Leer letras nuevas | f0 | — | дом (dom) = casa, Россия (Rossíya) = Rusia, чай (chai) = té, журнал (zhurnál) = revista, щи (shchi) = sopa, я (ya) = yo, юг (yug) = sur, эхо (ékho) = eco, фото (fóto) = foto, цирк (tsirk) = circo | Б Г Д Ж З И Й Л П Ф Ц Ч Ш Щ Э Ю Я | Transcribe 12 palabras oídas (≥ 80 %) |
| ru-f2-udarenie | Pronunciar con acento | f1 | — | молоко (malakó) = leche, хорошо (kharashó) = bien, вода (vadá) = agua, собака (sabáka) = perro, мы (my) = nosotros, мать (mat') = madre, объект (ob'yékt) = objeto, город (górad) = ciudad | Acento marcado con tilde; о átona suena [a]; ь blanda; ы; ensordecimiento final | Pronuncia 8 palabras con reducción correcta. La romanización deja de mostrarse |
| ru-f3-ya-eto | Identificar sin el verbo "ser" | f2 | я / ты / он / она / мы / вы / они; Я студент (sin verbo); Это…; Кто это? / Что это?; ты frente a вы | я = yo, ты = tú, вы = usted / ustedes, он = él, она = ella, они = ellos, это = esto es, кто = quién, что (shto) = qué, студент/студентка = estudiante, врач = médico/a | что se pronuncia [shto] | Produce 6 identificaciones y no inserta "есть" |
| ru-f4-rod | Reconocer el género y el posesivo | f3 | Género por terminación (consonante, -а/-я, -о/-е); он/она/оно; мой/моя/моё en nominativo | стол = mesa (m), книга = libro (f), окно = ventana (n), папа = papá (m, en -а), брат = hermano, сестра = hermana, имя = nombre (n), телефон = teléfono, машина = coche, море = mar | — | Asigna el género a 12 sustantivos nuevos (≥ 85 %), incluidas las excepciones |
| ru-f5-predstavlenie | Presentarse | f4 | Меня зовут… / Как тебя (вас) зовут?; Я из + genitivo como bloque; negación не | меня зовут = me llamo, как = cómo, из Эквадора = de Ecuador, из Мексики = de México, из Испании = de España, очень приятно = encantado/a, не = no, откуда = de dónde, тоже = también | Entonación de pregunta con palabra interrogativa | Diálogo de 4 turnos; elige ты o вы según la situación |

### Francés (fr)

| ID | Objetivo | Prerreq. | Gramática | Vocabulario | Pronunciación / escritura | Dominio |
|---|---|---|---|---|---|---|
| fr-f0-sons-salutations | Saludar | — | Bloques fijos | bonjour = buenos días / hola, bonsoir = buenas noches (saludo), salut = hola (informal), au revoir = adiós, merci = gracias, s'il vous plaît = por favor (formal), s'il te plaît = por favor, oui = sí, non = no, pardon = perdón | Consonantes finales mudas; r uvular; u [y] | Reconoce por audio 8 de 10 y pronuncia *merci* y *bonjour* de forma inteligible |
| fr-f1-nasales-liaison | Leer como se habla | f0 | — | pain = pan, vin = vino, bon = bueno, enfant = niño, un = uno, les amis [lezami] = los amigos, vous avez [vuzave] = usted tiene, deux = dos, bleu = azul | an/en, on, in/ain, un; eu; liaison obligatoria | Discrimina las nasales (≥ 80 %) y marca la liaison en 6 grupos |
| fr-f2-je-tu-vous | Elegir el tratamiento | f1 | je, tu, il, elle, **on**, nous, vous, ils, elles; sujeto obligatorio; tu frente a vous | je = yo, tu = tú, vous = usted / ustedes, il = él, elle = ella, on = nosotros (coloquial), nous = nosotros, ils/elles = ellos/ellas, monsieur = señor, madame = señora | Élision j' | Elige tu o vous en 8 situaciones; no omite el sujeto |
| fr-f3-etre | Identificarse y describirse | f2 | être (suis, es, est, sommes, êtes, sont); c'est | étudiant(e) = estudiante, professeur = profesor/a, content(e) = contento/a, fatigué(e) = cansado/a, français(e) = francés/a, équatorien(ne) = ecuatoriano/a, ici = aquí, à la maison = en casa | *est* [ɛ]; *es* y *est* suenan igual | Conjuga *être* con las 9 formas de sujeto, 24 h después |
| fr-f4-genre-articles | Nombrar con el artículo y concordar | f3 | un/une/des, le/la/l'/les; concordancia -e; plural oral marcado por el artículo | un livre = un libro, une table = una mesa, le café = el café, la maison = la casa, l'ami(e) = el/la amigo/a, les enfants = los niños, un garçon = un chico, une fille = una chica, grand(e) = grande, petit(e) = pequeño/a | *petit* frente a *petite* (consonante final) | Artículo correcto en 10 sustantivos nuevos (≥ 80 %) |
| fr-f5-ne-pas-questions | Negar y preguntar | f4 | ne…pas; est-ce que; entonación; *ne* ausente en el habla oral (solo reconocimiento) | ne…pas = no, est-ce que = ¿…? (partícula), pourquoi = por qué, où = dónde, comment = cómo, qui = quién, aussi = también, non plus = tampoco | Entonación ascendente | Transforma 8 frases en negativas y en preguntas |

(fr-f6 "Se présenter": je m'appelle, tu t'appelles comment ?, j'habite à…, je viens de l'Équateur, enchanté(e), et toi ? / et vous ?; prerrequisito f5.)

### Italiano (it)

| ID | Objetivo | Prerreq. | Gramática | Vocabulario | Pronunciación / escritura | Dominio |
|---|---|---|---|---|---|---|
| it-f0-suoni-saluti | Saludar | — | Bloques fijos | ciao = hola / chao, buongiorno = buenos días, buonasera = buenas tardes / noches, arrivederci = adiós, grazie = gracias, prego = de nada, per favore = por favor, sì = sí, no = no, scusi = disculpe (formal) | c + i/e = [tʃ] (*ciao*) | Reconoce 8 de 10 por audio |
| it-f1-c-g-doppie | Leer las grafías especiales | f0 | — | chiesa = iglesia, gelato = helado, ghiaccio = hielo, famiglia = familia, gnocchi, scuola = escuela, pesce = pescado, pizza, palla = pelota (frente a pala = pala), nonno = abuelo (frente a nono = noveno) | ci/chi, ge/ghe, gli, gn, sc; consonantes dobles | Discrimina simple y doble por audio (≥ 80 %) |
| it-f2-io-tu-lei | Tratamiento | f1 | io, tu, lui, lei, **Lei** (formal), noi, voi, loro; pro-drop como en español | io = yo, tu = tú, Lei = usted, lui = él, lei = ella, noi = nosotros, voi = vosotros / ustedes, loro = ellos, signore = señor, signora = señora | Mayúscula en *Lei* | Elige tu o Lei en 8 situaciones |
| it-f3-essere-stare | Ser, estar en un lugar y estar de salud | f2 | essere (sono, sei, è, siamo, siete, sono); *essere* para el lugar (sono a casa); stare para la salud (sto bene); falso paralelo con el español | stanco/a = cansado/a, contento/a = contento/a, studente/studentessa = estudiante, italiano/a, a casa = en casa, bene = bien, male = mal, qui = aquí, come stai? = ¿cómo estás? | è con acento frente a e (y) | Elige essere o stare en 10 frases (≥ 85 %) |
| it-f4-genere-articoli | Artículo según el sonido inicial | f3 | il/lo/la/l', un/uno/una/un', i/gli/le; plural -i/-e | il libro = el libro, lo studente = el estudiante, lo zaino = la mochila, l'amico = el amigo, la casa = la casa, l'amica = la amiga, i libri, gli studenti, le case, un'amica = una amiga | *lo* ante s + consonante y ante z | Artículo correcto en 12 sustantivos nuevos (≥ 80 %) |
| it-f5-presentarsi | Presentarse | f4 | mi chiamo / come ti chiami? / come si chiama?; sono di + ciudad; vengo da; negación con non | piacere = mucho gusto, mi chiamo = me llamo, di dove sei? = ¿de dónde eres?, Ecuador, Messico = México, Spagna = España, ecuadoriano/a, anche = también, non = no | Entonación de la pregunta | Diálogo de 4 turnos con registro tu o Lei coherente |

### Portugués (pt-BR)

| ID | Objetivo | Prerreq. | Gramática | Vocabulario | Pronunciación / escritura | Dominio |
|---|---|---|---|---|---|---|
| pt-f0-sons-saudacoes | Saludar | — | Bloques fijos | oi = hola, olá = hola, bom dia = buenos días, boa tarde = buenas tardes, boa noite = buenas noches, tchau = chao, obrigado/obrigada = gracias (según quien habla), por favor, com licença = con permiso, desculpa = perdón, sim = sí, não = no | *obrigado* concuerda con quien habla | Usa obrigado u obrigada según su género |
| pt-f1-nasais-vogais | Pronunciar nasales y vocales átonas | f0 | — | pão = pan, mãe = madre, irmão = hermano, bom = bueno, sim = sí, um = uno, avó = abuela, avô = abuelo, leite [ˈlejtʃi] = leche, tia [ˈtʃia] = tía | ã, õ, -ão; é/ê, ó/ô; t/d + i; e/o átonas | Discrimina avó/avô y pão/pau por audio (≥ 80 %) |
| pt-f2-eu-voce | Pronombres de Brasil | f1 | eu, você (+ 3.ª persona), ele, ela, nós, **a gente** (+ 3.ª persona), vocês, eles/elas | eu = yo, você = tú / usted, ele = él, ela = ella, nós = nosotros, a gente = nosotros (coloquial), vocês = ustedes, eles/elas = ellos/ellas, senhor/senhora = señor/a | — | Concuerda el verbo con *você* y *a gente* en 3.ª persona en 8 frases |
| pt-f3-ser-estar | Aprovechar el paralelo con el español | f2 | ser (sou, é, somos, são) y estar (estou, está, estamos, estão); mismo reparto que en español; *estar com fome* | estudante = estudiante, professor(a) = profesor/a, brasileiro/a = brasileño/a, cansado/a = cansado/a, feliz, em casa = en casa, com fome = con hambre, com sono = con sueño, aqui = aquí | *é* abierta | Ser/estar correcto en 10 frases (≥ 90 %); *com fome* en lugar de "tenho fome" también se acepta |
| pt-f4-genero-contracoes | Contraer siempre | f3 | o/a/os/as, um/uma; em + o = no, em + a = na, de + o = do, de + a = da | o livro = el libro, a mesa = la mesa, o café, a casa, no Brasil = en Brasil, na casa = en la casa, do Equador = de Ecuador, da Espanha = de España | — | Contracción correcta en 10 huecos (≥ 85 %) |
| pt-f5-apresentar-se | Presentarse y evitar falsos amigos | f4 | meu nome é / eu me chamo; sou de; tudo bem?; negación con não antes del verbo | prazer = mucho gusto, tudo bem? = ¿todo bien?, tudo bom, esquisito = raro (no "exquisito"), polvo = pulpo, apelido = apodo, oficina = taller, borracha = goma de borrar, escritório = oficina | — | Diálogo de 4 turnos e identifica 4 de 5 falsos amigos |

### Español (es) — para nativos de inglés; glosas y explicaciones en `en`

| ID | Objetivo | Prerreq. | Gramática | Vocabulario (glosa en inglés) | Pronunciación / escritura | Dominio |
|---|---|---|---|---|---|---|
| es-f0-sonidos-saludos | Saludar con vocales puras | — | Bloques fijos | hola = hello, buenos días = good morning, buenas tardes = good afternoon, adiós = goodbye, hasta luego = see you later, gracias = thank you, por favor = please, sí = yes, no = no, perdón = sorry | 5 vocales puras sin diptongar; h muda; ñ; r/rr; j | Vocales sin diptongar en 8 palabras (evaluación por audio) |
| es-f1-yo-tu-usted | Tratamiento y pro-drop | f0 | yo, tú, usted, él, ella, nosotros/as, ustedes, ellos/as; el sujeto se omite | yo = I, tú = you (informal), usted = you (formal), él = he, ella = she, nosotros = we, ustedes = you all, ellos = they, señor = Mr., señora = Mrs. | Tilde en *tú* y *él* | Elige tú o usted en 8 situaciones y acepta frases sin sujeto |
| es-f2-ser | Identidad y origen | f1 | ser (soy, eres, es, somos, son); ser de + lugar | estudiante = student, profesor/a = teacher, médico/a = doctor, de = from, Estados Unidos = USA, Inglaterra = England, estadounidense = American, inglés/inglesa = English | Acento en *está* frente a *esta* (anticipo) | Conjuga *ser* con 8 sujetos, 24 h después |
| es-f3-genero-articulos | Nombrar con género y concordar | f2 | el/la/los/las, un/una; -o/-a y excepciones (el día, la mano); concordancia del adjetivo | el libro = the book, la mesa = the table, el día = the day, la mano = the hand, la casa = the house, el coche = the car, alto/a = tall, pequeño/a = small, nuevo/a = new | — | Artículo y concordancia en 12 casos nuevos (≥ 85 %) |
| es-f4-estar-vs-ser | Estados y lugar frente a identidad | f3 | estar (estoy, estás, está, estamos, están) para estado y lugar; ser para identidad; contraste mínimo (es aburrido / está aburrido) | cansado/a = tired, contento/a = happy, enfermo/a = sick, en casa = at home, aquí = here, bien = fine / well, mal = bad(ly), listo/a = ready / clever | — | Ser o estar en 12 frases nuevas (≥ 85 %), con explicación en inglés del error |
| es-f5-presentarse | Presentarse | f4 | me llamo / ¿cómo te llamas? / ¿cómo se llama?; soy de…; mucho gusto; negación con no antes del verbo | me llamo = my name is, ¿de dónde eres? = where are you from?, mucho gusto = nice to meet you, encantado/a = pleased to meet you, ¿cómo estás? = how are you?, también = too / also, no = no / not | ¿…? y ¡…! | Diálogo de 4 turnos con registro coherente |

## Mapeo foundations-v1 → nuevas unidades

Claves actuales: `foundation-v1-<unitId>-<q>` con `resueltaConApoyo`, `conApoyo: true`, `idioma: 'en'` y `nivel: 1` (`foundations_screen.dart:105-119`; `foundations.dart:254-267`).

| foundations-v1 (6) | Nueva unidad | Nodo del grafo | Cobertura | Estado migrado |
|---|---|---|---|---|
| `i-you` | en-f1-pronombres (parcial) | en-g-subj-pron-1 | I, you | Ítems I/you "practicados con apoyo"; he, she, it, we, they pendientes |
| `i-am` | en-f2-be-afirmativo (parcial) | en-g-be-affirm | I am | Forma "am" practicada con apoyo |
| `you-are` | en-f2-be-afirmativo (parcial) | en-g-be-affirm | you are | Forma "are" (con *you*) practicada con apoyo |
| `he-she` | en-f1 (he/she) y en-f2 (is) | en-g-subj-pron-2, en-g-be-affirm | he, she, is | Idem; *it/we/they* y las contracciones pendientes |
| `feelings` | en-f2-be-afirmativo | en-g-be-adj-state | happy, tired, ser/estar | Vocabulario y uso practicados con apoyo |
| `introduce` | en-f5-presentarse (parcial) | en-g-introduce | I am + nombre / estado | Solo la parte "I am…"; *What's your name?* y *Where are you from?* pendientes |
| (nuevo) | en-f0-primer-contacto | en-g-sound-text | — | Se ofrece una **prueba rápida para saltarla** si el alumno ya completó foundations-v1 |
| (nuevo) | en-f3, en-f4 | be-negative, be-yesno, short-answers-be, wh-be | — | Pendientes para todos |

Reglas de migración:
1. **No borrar ni reescribir** las claves `foundation-v1-*`. Se leen como evidencia histórica, igual que se hará con `grammar-guide-<id>-<n>`.
2. Una tabla de equivalencias (`foundation-v1-<id>` → [ids de nodo o ítem]) marca como máximo **"practicado con apoyo"**, nunca "dominado". Así se cumple el propio documento (`FUNDAMENTOS-DESDE-CERO.md`: "Completar significa «practicado con ayuda», nunca «dominado»").
3. Para dominar en-f1 y en-f2, quien viene de v1 hace la comprobación independiente y la recuperación diferida. No repite la enseñanza, pero puede volver a ella.
4. No se vuelve a otorgar XP por actividades equivalentes (ya existe `primeraCorrecta`).
5. `/fundamentos` sigue funcionando hasta que la ruta nueva esté activa, y después redirige a en-f0/f1 con el progreso ya mapeado.

## Decisiones que requieren revisión humana

1. **Español (DEC-004), ya decidido como opción (a).** Hay que confirmar tres cosas:
   - La variante meta: neutra latinoamericana con *ustedes*, o peninsular con *vosotros*. Recomiendo la latinoamericana, con *vosotros* solo para reconocimiento.
   - Que el primer idioma de apoyo sea `en`.
   - Qué hacer con los 3 JSON `es` actuales: mantenerlos ocultos o retirarlos, porque no sirven para no hispanohablantes.
2. **Contenido multilingüe de apoyo**: aprobar el esquema `{es, en}` en explicaciones, glosas, errores y feedback (el agente D define el esquema). Hay que decidir quién traduce y revisa las glosas `en` de los 9 cursos si más adelante se abren a anglohablantes.
3. **Variante de portugués**: pt-BR, coherente con `localeVoz`. Hay que confirmar si pt-PT queda solo para reconocimiento.
4. **Chino**: solo simplificados, con tradicionales como reconocimiento en C2. Falta definir la política de retirada del pinyin (propuesta: desde A2, pinyin solo al pulsar).
5. **Japonés**: furigana siempre en A1. Hay que fijar cuándo se introducen los kanji (propuesta: 20 en A1 y unos 300 en A2) y si se enseña primero la forma llana o la ます (propuesta: ます).
6. **Coreano**: 해요체 como nivel inicial, con 합니다체 en A2. Hay que decidir si la romanización se retira tras ko-f3 (propuesta: sí).
7. **Ruso**: retirar la romanización tras ru-f2 y marcar el acento con tilde hasta B1.
8. **Reordenar N1–N2 de inglés**: cambia los IDs `L<n>-NNN` (`curriculum.dart:~480`) y el progreso asociado. Además, el cargador exige 20 unidades (`contenido_json.dart:133`). Hay dos caminos: (a) una ruta nueva basada en nodos, dejando los JSON como banco de práctica, o (b) reordenar y migrar. **Recomiendo (a).**
9. **Guías fuera de nivel**: bajar `continuous` a 2, bajar `past-continuous` a 4, subir `third-conditional` a 7. Mover una guía reasigna la evidencia `grammar-guide-*` a otro nivel.
10. **N3–N10 en los 9 idiomas no ingleses** muestran el banco en inglés. Hay que decidir si se bloquean hasta tener contenido (recomendado) o si se ocultan.
11. **Revisión nativa obligatoria** de las unidades f0–f5 de los 9 idiomas antes de publicarlas. Son una propuesta pedagógica: la gramática y las glosas son de conocimiento general, no se validaron con hablantes nativos.
12. **C2**: confirmar que se queda `planificado` con `nivelInterno: null` (DEC-002) y que los 6 nodos en-g-c2-* no se muestran al alumno.

## Fuentes

- No consulté fuentes externas en esta sesión (2026-09-26). El diseño lingüístico de los 9 idiomas se basa en conocimiento general de la gramática de cada lengua y **necesita revisión nativa** (ver decisión 11).
- Referencias internas usadas: `docs/MATRIZ-GRAMATICA-ESCOLAR.md`, que cita CEFR Companion Volume 2020, British Council A1–C1 y English Profile (fuentes consultadas por otros el 2026-09-19); `docs/FUNDAMENTOS-DESDE-CERO.md`; `docs/claude-educacion/DECISIONES.md` (DEC-002, DEC-003 y DEC-004).
- Código verificado:
  - `lib/core/content/{curriculum,contenido_json,fundamentos,foundations,grammar_guides,idiomas}.dart`
  - `lib/features/foundations/foundations_screen.dart`
  - `lib/features/library/grammar_screen.dart`
  - `lib/shared/widgets/learning_path.dart`
  - `lib/features/home/home_screen.dart`
  - `lib/core/diagnostico.dart:320`
