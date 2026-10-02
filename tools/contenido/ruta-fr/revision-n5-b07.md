# Revisión independiente · N5 francés, bloque 7 (clases 31–35)

- **Archivo:** `tools/contenido/ruta-fr/n5-b07.json` (`fr.n5.c31` … `fr.n5.c35`). Revisor distinto del autor.
- **Validador:** `python3 tools/validar_ruta.py fr --borrador …n5-b01.json … n5-b07.json` → **0 errores** (repetido tras los últimos cambios). Los borradores n4-b01…b10 ya están integrados en `assets/contenido/fr/ruta/`: se quitaron de la lista (con ellos daba «id duplicado»).
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún aviso «título de la unidad difiere» para c31–c35.
- Leídos también los borradores n5-b01…b06 y b08…b10 (solo sus `situacion` y hablantes) para buscar choques de reparto: no hay.

## Veredicto

GO

## Contraste con las fichas

Cada clase enseña lo que dice su ficha y nada posterior: c31 condicional periodístico (presente = hecho actual o próximo, pasado = hecho anterior, pasiva aurait été, selon / d’après, contraste con el indicativo confirmado); c32 il me semble que + indicativo, il semble que + subjuntivo, il semblerait que + subjuntivo, il paraîtrait que + indicativo, à en croire / si l’on en croit + condicional; c33 modalizadores (dans une certaine mesure, en quelque sorte, plus ou moins, a priori, en principe), dans la plupart des cas, en règle générale, la plupart des + plural, j’ai l’impression que + indicativo; c34 certes… mais, il est vrai que… cependant, quoique + subjuntivo, alors que / tandis que; c35 il est évident / clair / certain que + indicativo, il n’est pas certain que, est-il vrai que, croyez-vous que + subjuntivo. El vocabulario de las fichas está completo (10 + 9 + 9 + 9 + 9 palabras) y cada clase tiene `titulo` y `objetivo` iguales a los de la ficha.

Los ejercicios del plan están todos, con el mismo formato y la misma clave (guiada 5, independiente 4, situación 2, evaluación 6–7; c31–c34 con 6 ítems en evaluación, c35 con 7). Anatomía: 3 explicaciones → tablas → ejemplos (8) → vocabulario → guiada (5, todas con `pista`) → independiente (4, sin pista) → situación + 2 comprensiones → evaluación con ≥ 5 ítems puntuables en ≥ 4 formatos; el `escribir` abierto (`abierta: true`, no puntúa) es el último ítem de cada evaluación y se suma a esos ítems. Hay 2 `erroresFrecuentes` por clase. No hay «sonido del día» (N5). `orden` 531–535, prerrequisitos c30 → c31 → … → c35, `cefr` B2, `nivelInterno` 5.

## Cambios aplicados (clase · ítem · antes → después)

### Transversal
1. **Tipografía.** Guillemets con espacio normal (« texto ») en c32 (diálogo) y c35 (diálogo, `s1`) → U+202F dentro de « » (convención mayoritaria de N3–N5). Todo `? ! : ;` del francés ya llevaba U+202F; los apóstrofos son ’ en todo el bloque.

### c31
2. **p2 (explicación, es / en).** «Hecho actual: condicional presente» no cubría «Le propriétaire serait interrogé demain» (del diálogo y del modelo del `e6`) → «Hecho actual o próximo (un plan de mañana también): condicional presente» / “Current or upcoming event (tomorrow’s plans too)…”.
3. **e6 (feedback).** «serait interrogé (futuro cercano, condicional presente)» → «(hecho de mañana: condicional presente)» (es / en).
4. **e4 (ordenar).** Faltaba un orden natural con la fuente entre comas → + aceptada «L’incendie, selon la police, aurait fait trois victimes.»; feedback: «La fuente puede ir al final, al principio o entre comas.»

### c32
5. **Diálogo, línea 2 (Léa).** «À en croire ce site, on ne peut plus passer…» (indicativo tras à en croire, contra la explicación p3 que enseña el condicional) → «on ne pourrait plus passer depuis ce matin»; traducciones es / en adaptadas.
6. **Ejemplos 5 y 6 (en).** «Judging by this site, the conspiracy exists.» / «…the tiger escaped from the zoo.» perdían el condicional → «…the conspiracy supposedly exists.» / «…the tiger supposedly escaped from the zoo.»
7. **Diálogo, línea 3 (en).** «the tiger is in the park» → «the tiger would be in the park».
8. **i4 (escribir).** + aceptada «Le complot existerait, si l’on en croit ce site».

### c33
9. **Situación.** 308 palabras (justo sobre el mínimo del nivel) → 328: la conclusión de Hugo añade «Je ne dis donc pas que les réseaux sociaux sont mauvais : je dis seulement qu’il ne faut pas généraliser.» (es / en incluidos).
10. **g2 (completar).** Distractor «en» (el antiguo «en une certaine mesure» existe) → «sur»: opciones «dans / sur / par».
11. **i4 (escribir).** + aceptada «Les réseaux sociaux, dans une certaine mesure, isolent les jeunes».
12. **e5 (feedback, es / en).** «los videos virales casi nunca se verifican» / “rarely checked” (más fuerte que la frase) → «la mayoría de las veces los videos virales no se verifican» / “usually aren’t checked”.

### c34
13. **Errores frecuentes 1.** «Quoique ce est un journal sérieux» mezclaba dos errores (ce est + indicativo) → «Quoique c’est un journal sérieux, il se trompe parfois.» (solo el modo).
14. **g4 (completar).** «___ , le contenu est faible» (espacio suelto antes de la coma) → «___, le contenu est faible».
15. **g5 (relacionar).** Glosas de «certes… mais» y «il est vrai que… cependant» casi iguales → «ciertamente… pero (concesión)» / «es cierto que… sin embargo (más formal)» (en: “admittedly… but (concession)” / “it is true that… however (more formal)”).

### c35
16. **Diálogo, línea de Ana.** «Tu crois qu’on peut le vérifier…» (indicativo tras croire en pregunta, justo lo contrario de lo que enseña la clase con croyez-vous que) → «Est-ce qu’on peut le vérifier avec un chiffre ?» (es / en adaptadas; «peut-on» no está enseñado y el validador lo rechaza).
17. **Clasificación final de Hugo.** Clasificaba 8 enunciados y la tarea de la ficha habla de 10 → + hecho «l’an dernier, le budget était de 600 000 euros» y + opinión «dépenser autant est discutable» (4 hechos, 4 opiniones, 2 ideas recibidas), con es / en. La situación pasa a 408 palabras.

## Revisión punto por punto

1. **Francés de Francia.** Correctos: aurait + participio / serait + participio (partir, se cacher), aurait été, démissionnerait (futuro + -ait); il semble que / il semblerait que + subjuntivo (soit, soient, vienne, ait), il paraîtrait que + indicativo; à en croire / si l’on en croit + condicional; modalizadores, la plupart des + verbo en plural, j’ai l’impression que + indicativo; certes… mais, cependant, quoique + subjuntivo (soit, ait, puisse; quoiqu’ils), bien que, alors que / tandis que + indicativo; il est évident / clair / certain / incontestable que + indicativo, il n’est pas certain / évident que + subjuntivo, est-il vrai que, croyez-vous que + subjuntivo. Concordancias (surprise, payés, virale) bien.
2. **Explicaciones es / en.** Cortas y con ejemplos; es con tú y léxico neutro (celular, video, presupuesto); en americano (cell phone no aparece; sí “doctored”, “turnover”, “whereas”). Buenas comparaciones con el español («el sospechoso habría salido…») y con el inglés («reportedly», «allegedly»).
3. **Respuesta única y `aceptadas`.** Revisados todos los `completar` (con `opciones` donde hay riesgo), `ordenar` (c31 y c34 con la fuente / el quoique al inicio o al final; c32 con À en croire al inicio o al final; c33 y c35 con un solo orden natural) y los `escribir` puntuables. Distractores siempre erróneos.
4. **Pistas y relacionar.** Cada pista ayuda a su ítem (aurait + participio, condicional vs. passé composé, indicativo vs. subjuntivo según la estructura, à en + infinitivo, mesure / sorte). Glosas de los 8 `relacionar` claramente distintas tras el cambio 15.
5. **Guías de sonido.** j / g suave = «sh» («zh» en inglés), nasales in / ain → «en», an / en → «an», ü / ö definidas y recordadas en cada clase; avisos de consonantes finales (sí suena la t de correspondante y de partial, no suena la de complot / esprit); ç = «s», ni = «ny», ti = «sy».
6. **Hablantes.** Hugo, Léa, Ana y papeles / medios en francés (L’agence de presse, Le journaliste, Le Quotidien, L’Hebdo, L’auteur de la tribune): nunca en español.
7. **Situaciones (300–500 palabras).** c31 321 (6 líneas), c32 347 (8), c33 328 (7), c34 367 (9), c35 408 (8). Cada pregunta de comprensión tiene una sola respuesta correcta y coincide con el texto (primer titular sin fuente oficial; consejo de verificar las fuentes; las redes informan dans une certaine mesure; la mayoría de los influenceurs cobran; el segundo artículo es más objectif; el primero habla de éxito; «il n’est pas certain que…» = duda; el hecho es que el presupuesto aumentó).
8. **Anatomía y evaluación.** Todas las evaluaciones tienen ≥ 5 ítems puntuables y ≥ 4 formatos, más 1 `escribir` abierto con rango de palabras.
9. **Palabras retiradas.** Ninguna palabra francesa enseñada fue eliminada: los cambios solo reemplazan formas dentro de ítems y diálogos. No afecta a b08–b10 (verificado con el validador sobre b01–b07).

## Hechos del reparto confirmados

- Hugo estudia una maestría y analiza noticias de prensa para ella; ahí compara dos versiones de la noticia de un incendio en un almacén de las afueras (el despacho de agencia y el artículo del diario), y Ana le pregunta cómo lo anota (c31). / Hugo is doing a master’s program and analyzes news stories for it; there he compares two versions of a news story about a fire in a warehouse on the outskirts (the agency wire report and the newspaper article), and Ana asks him how he notes it (c31).
- Léa publica en su blog un análisis de tres titulares dudosos que vio en internet (puente cerrado, tigre escapado del zoo, metro gratuito) y aconseja verificar las fuentes antes de compartir; Hugo comenta su entrada y también verifica siempre dos fuentes (c32). / Léa posts an analysis on her blog of three dubious headlines she saw online (closed bridge, tiger escaped from the zoo, free subway) and advises checking sources before sharing; Hugo comments on her post and also always checks two sources (c32).
- Hugo escribe para su maestría un artículo de opinión, «Les réseaux sociaux : ami ou ennemi ?», que matiza sin generalizar; Léa le responde que ella lee los comentarios antes de compartir una publicación (c33). / For his master’s Hugo writes an opinion article, “Les réseaux sociaux : ami ou ennemi ?”, qualifying without overgeneralizing; Léa replies that she reads the comments before sharing a post (c33).
- Hugo compara para su maestría dos artículos de Le Quotidien (éxito) y L’Hebdo (fracaso) sobre la reapertura del mercado cubierto de su barrio (el diario cita más de mil visitantes de la alcaldía, el semanario vio trescientos); concluye que el segundo es más objetivo, y Ana le pregunta cuál prefiere (c34). / For his master’s Hugo compares two articles, one from Le Quotidien (success) and one from L’Hebdo (failure), on the reopening of his neighborhood’s covered market (the daily cites over a thousand visitors from city hall, the weekly counted three hundred); he concludes the second is more objective, and Ana asks which he prefers (c34).
- Hugo lee una tribuna sobre el proyecto de la nueva biblioteca del barrio (presupuesto de 800 000 euros frente a 600 000 el año anterior) y separa hechos, opiniones e ideas recibidas; Ana comenta que los jóvenes quizá leen en el celular (c35). / Hugo reads an opinion column about the neighborhood’s new-library project (800,000-euro budget versus 600,000 the year before) and separates facts, opinions and received ideas; Ana remarks that young people may be reading on their phones (c35).

Coherencia con lo ya fijado: Hugo empieza una maestría en París (N2 B2) y la usa en n5-b02 (c06, c08), c29 y c48; Léa es estudiante, bloguera de viajes en c13 y tutea a Hugo y a Ana; Ana trabaja en el hotel y se tutea con Hugo; sin contradicciones con N1–N4.

## Sin resolver (no bloquea)

- **c31, tarea de la ficha:** habla de reescribir 5 informaciones no confirmadas, pero el `escribir` de la evaluación (fijado por el plan) pide 3; el diálogo modela 5 (3 víctimas, salida del sospechoso, escondite, interrogatorio, versión del alcalde). Conviene que el coordinador alinee la ficha (3) o la tarea.
- **c32, tabla p5:** incluye la fila `croire` (il croit / il croie), que no se usa tras «que» en la clase; se conserva porque «crois / croit» se usan como opciones y en el diálogo. `n5.json` aún no trae `hechosDelReparto` del nivel; los de arriba son los que hay que copiar con `"bloque": 7`.
- **c35, registro:** croyez-vous que + subjuntivo es la forma cuidada; en la lengua hablada también se oye tu crois que + indicativo. El diálogo evita esa construcción para no contradecir la clase.
- **c34, ERR 2:** el uso de «aussi» al inicio de oración como conector (= por lo tanto) es literario; sirve como error de hispanohablantes («aussi» ≈ «así que»), pero es el único error de esa clase que depende de esa lectura.

Validación final: 0 errores.
