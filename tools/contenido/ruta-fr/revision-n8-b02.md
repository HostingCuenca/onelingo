GO

# Revisión de N8 · B2 (fr.n8.c06–c10) — Lo implícito

Revisor distinto del autor. Validación: `python3 tools/validar_ruta.py fr --borrador n8-b01.json n8-b02.json` → **0 errores** (N7 ya está integrado en `assets/contenido/fr/ruta/`, por eso se quitaron n7-b01…b10 de la lista; con ellos daba «id duplicado»). `python3 tools/curriculo/validar_plan.py fr`: sin «título de la unidad difiere» para fr.n8.c06–c10 (0 errores).

Comprobado contra las 5 fichas de `curriculo/fr/n8.json`: títulos, objetivos, gramática, `introduce`/`recicla`, 8 palabras de vocabulario por clase, situación y tarea, y los planes de ejercicios (mismos formatos y claves, orden respetado). No se enseña nada de fichas posteriores (c09 solo cita `il semblerait que`, c10 `conditionnel-attenuation` y c07/c10 la lítote, todos en `recicla`).

Situaciones (palabras de diálogo, conteo por espacios; mínimo 400 para N8): c06 ≈ 470, c07 ≈ 450, c08 ≈ 420, c09 ≈ 440, c10 ≈ 430. Todas con sus preguntas de comprensión coherentes con el texto.

Evaluación (≥ 4 puntuables y ≥ 2 formatos; el `escribir` abierto no cuenta): c06 5 ítems / 4 formatos; c07 5 / 3; c08 5 / 3; c09 5 / 4; c10 5 / 4. Todos los `escribir` abiertos cumplen `minimoPalabras` con su modelo (lo exige el validador).

## Arreglos hechos (clase, ítem, antes → después)

### Reparto y coherencia
- **c07, personajes de la serie:** «Margaux et Antoine» → **Margaux et Mathieu** (Antoine es el esposo de Chloé; «Julien» chocaba con el candidato de N9 b05, así que se eligió Mathieu, que no aparece en ningún nivel). Cambiados: hablante, consigna/feedback de s1 y la réplica de Léa («Quand Antoine dit…» → «Quand il dit…»). Margaux ya no nombra a su pareja en el diálogo («Antoine, je suis fatiguée.» → «Je suis fatiguée.»), para no necesitar un nombre propio nuevo en el texto francés.
- **c07, diálogo:** se quita «Quelle belle soirée ! Pardon…» de Margaux (ironía ambigua frente al vecino, que no se comenta) → «Pardon, nous allons tout ranger.»
- **c06, hora:** Léa decía que Hugo llevaba «une heure» sentado, pero estaban desde las 2:30 y eran las 3:00. → «il est exactement quatre heures» / «Depuis trois heures» (es/en alineados).
- **c06, e5 (modelo abierto):** «Léa a enfin trouvé un appartement. (Elle en cherchait un depuis longtemps.)» → «Karim a enfin trouvé un cuisinier. (Il a longtemps cherché.)» (no inventa un cambio de vivienda de Léa; además quita «cherchait», palabra no enseñada).
- **c08, director (insinuaciones suaves, sin caricatura):**
  - «À croire que le directeur est sourd» (ejemplos, tabla, error frecuente, g3) → «…est **distrait**» (es «un distraído», en “absent-minded”).
  - «À croire que le directeur est un fantôme» → «…est toujours en réunion : on ne le voit jamais le vendredi». Se quita la fila «le fantôme» de «Para leer».
  - «chaque fois qu’il y a un problème avec les comptes» (insinuaba irregularidad económica) → «chaque fois qu’il y a une réunion difficile».
  - Ana contrapesa: «Ce n’est pas que je défende le directeur, mais tu exagères un peu. **Il arrive aussi très tôt le matin.**»
  - «il part toujours tôt…» → «il part souvent tôt, comme par hasard, le jour du bilan», y la consigna de s1 cita ahora esa línea literal (antes citaba una frase que no estaba en el diálogo).
  - El director sale a las 16 h y falta los viernes solo en boca del compañero, quien reconoce al final que «c’était une blague» y Ana propone preguntar «poliment, sans reproche voilé».
- **c08, c09, c10, rol de Ana:** compatibles con N7 (coordina los eventos culturales del hotel). El `contexto` de las tres situaciones dice ahora que Ana «coordina los eventos culturales del hotel y cubre turnos en la recepción» (c08, c09) / «es la portavoz del equipo de recepción» (c10). En francés no cambia nada; Ana sigue hablando de vous al director.
- **c09, réplica de Ana:** decía que el director «se targue de tout contrôler» y «a peur», pero su correo dice «Je ne me targue pas d’avoir tout prévu» → «Il ne se targue pas d’avoir tout prévu, mais il veut convaincre l’équipe. Il demande notre avis, et ses collègues… lisent entre les lignes.»

### Corrección y respuestas
- **c09, e2:** «Il se ___ d’avoir tout fait à lui seul» tenía dos respuestas válidas → `aceptadas`: «targue», «vante». El feedback en inglés citaba otra frase («sauvé l’entreprise») → alineado con es.
- **c09, i3:** `aceptadas` + «censément» (la explicación lo cita como marca de distancia).
- **c07, g5:** `aceptadas` + formas femeninas (Ana es quien derrama el café): «Tu es maladroite», «Tu es très maladroite», «C’est très maladroit !», «C’est maladroit de ta part.»
- **c06, g5:** `aceptadas` + «J’en déduis qu’il fumait.», «…qu’avant, il fumait.», «…qu’il fumait auparavant.»
- **c10, e1 (relacionar):** glosas demasiado parecidas («No hay decisión» / «No prometemos nada» / «No la aceptamos por ahora») → «No la aceptamos, por ahora.» / «Todavía no hay ninguna decisión.» / «Lo anotamos, pero sin compromiso de actuar.» / «Quizá les avisemos.» (el original usaba «os», peninsular).
- **c07, español neutro:** «nevera» → «refrigerador» (tabla, g4 consigna y feedback, con concordancia).
- **Tipografía:** se aplicó U+202F dentro de las comillas francesas (« … »), como en N7 publicado, y antes de ? ! en las `aceptadas` nuevas. Los títulos de c06/c07 conservan el espacio normal porque son idénticos al plan (el validador del plan los compara).

### Tablas «Para leer…» (punto 15) y vocabulario estricto
- **c06:** de 13 filas a **2** («emprunter / il l’avait emprunté» y «il fumait»). Las demás (fumer, attendre, boire, dire, chercher, commander, courir, remarquer, assis, espérer, refuser, le test) solo existían para que el validador aceptara formas conjugadas de verbos básicos ya enseñados. Se reescribieron las frases con formas ya conocidas:
  - «Hugo, tu as commandé mon thé ?» → «Hugo, tu as pris un thé pour moi ?»; «Il t’attend sur la table» → «Oui, il est déjà sur la table»; «J’ai couru depuis le métro» → «Je suis venue vite».
  - «assis» y «remarqué» → «Tu es resté une heure à table» / «j’ai vu quelque chose»; «l’a remarqué» → «l’a compris».
  - «vous ne l’attendiez pas» (diálogo y explicación) → «c’est une surprise»; «Si Ana disait « jamais »» → «Si Ana avait dit « jamais »»; «on espère une réponse» → «on attend une réponse».
  - e2: «Avant, il buvait du café.» → «Avant, il prenait du café.»; e4: «refuserait» → «dirait non»; g2: «le test» → «l’examen».
  - Se conservan «emprunté» y «fumait» porque son contenido real (presuposición de «arrêter de», `ejemplos` con «l’avait emprunté»).
- **c07:** 6 filas, todas necesarias y con contenido real (épisode, déménager, indice, contradiction, exagération, points de suspension). **c08:** 6 → 5 (sin «fantôme»). **c09:** 6 (concurrence, extérieur, modernisation, s’interroger, sceptique, attitude). **c10:** 1 (envisager). Todas ≤ 15.

## Palabras francesas quitadas que un bloque posterior de N8 usa (aviso)
Con los borradores n8-b01…b10 encadenados el validador da **2 errores en n8-b05, fr.n8.c25** que antes salvaban mis filas retiradas:
- `fr.n8.c25.p12.dialogo[5]`: «fantômes» (venía de la fila «le fantôme» de c08).
- `fr.n8.c25.p12.dialogo[6]`: «assis» (venía de la fila «assis, assise» de c06).
El autor/revisor de B5 debe enseñarlas en su propia clase (una fila «Para leer») o reescribir esas dos réplicas; no se repuso la fila en B2 porque ya no tiene uso en c06/c08. Otras palabras retiradas (`test`, `disait`, `espère`) se siguen validando en b05–b10 sin errores, pero `test` aparece también en n9-b03 y n10-b04 (no validados aquí): conviene comprobarlo al encadenar N9/N10.

## Hechos del reparto confirmados
- Hugo dejó de fumar hace tres semanas (antes fumaba; Léa lo notó y su abuela lo notó por teléfono); no contradice N1–N7 (solo hay un invitado sin nombre que fuma en el balcón en N6 y el reglamento del gimnasio, que prohíbe fumar) / Hugo quit smoking three weeks ago (he used to smoke; Léa noticed and his grandmother noticed on the phone); this does not contradict N1–N7 (the only smoker is an unnamed guest on the balcony in N6, and the gym rules forbid smoking) (c06)
- Hugo no suele lavar los platos (coherente con N7 c22) / Hugo does not usually do the dishes (consistent with N7 c22) (c06, evaluación)
- Emma suele llegar tarde y olvidó sus llaves una vez el mes pasado; toma té, Hugo café, como siempre / Emma is usually late and forgot her keys once last month; she drinks tea and Hugo coffee, as always (c06)
- Lucas casi nunca responde en el grupo de mensajes; esta vez respondió sobre la fiesta del sábado / Lucas almost never answers in the group chat; this time he answered about Saturday’s party (c06)
- Ana rehízo su CV para pedir plaza en un curso nocturno de la universidad y todavía no tiene respuesta (coherente con el curso universitario de B9) / Ana redid her CV to apply for an evening course at the university and has not heard back yet (consistent with the university course in B9) (c06)
- Ana ve con Léa, en casa de Léa, una serie de comedia francesa ficticia sobre una pareja que se muda (Margaux y Mathieu, personajes de la serie, no del reparto) / Ana watches a fictional French comedy series about a couple moving house at Léa’s place (Margaux and Mathieu are characters in the series, not in the cast) (c07)
- Ana, que coordina los eventos culturales del hotel (N7), cubre también turnos en la recepción; con el compañero de turno (Le réceptionniste, sin nombre, se tutean) comenta que el director sale a las 16 h antes del balance mensual / Ana, who coordinates the hotel’s cultural events (N7), also covers front-desk shifts; with her shift colleague (Le réceptionniste, unnamed, they use tu) she talks about the director leaving at 4 p.m. before the monthly review (c08)
- El director del hotel (sin nombre; Ana lo trata de vous) llega muy temprano por la mañana; el compañero lo critica a medias por irse pronto y no estar los viernes, y Ana prefiere decírselo de frente / The hotel director (unnamed; Ana uses vous with him) arrives very early in the morning; the colleague half-criticizes him for leaving early and being absent on Fridays, and Ana prefers to tell him to his face (c08)
- La dirección anuncia un «plan de modernisation» que empieza el lunes (habitaciones del segundo piso listas al día siguiente); dos compañeros de recepción responden por escrito, uno con ironía y una colega con escepticismo cortés / Management announces a “modernization plan” starting Monday (rooms on the second floor, i.e. third floor in the US, ready the next day); two reception colleagues reply in writing, one ironically and one with polite skepticism (c09)
- Ana es la portavoz del equipo de recepción en una reunión con la dirección: piden un fin de semana de descanso al mes y menos horas extra (hicieron treinta el mes pasado) y que contraten a alguien para los fines de semana; el director responde con lengua de madera y promete informar; Ana pide respuesta por escrito antes del viernes / Ana is the reception team’s spokesperson in a meeting with management: they ask for one rest weekend per month, fewer overtime hours (they worked thirty last month) and someone hired for weekends; the director answers in wooden language and promises to keep them informed; Ana asks for a written answer before Friday (c10)

## Sin resolver
- n8-b05 c25: 2 palabras («fantômes», «assis») dependían de filas que se retiraron de B2 (ver arriba). Hay que resolverlo en B5.
- Los títulos de c06 y c07 llevan espacio normal antes de «?» y «!» (igual que el plan); si se quiere U+202F, hay que cambiar plan y borrador a la vez.
- N9/N10 no se validaron encadenados; `test` (n9-b03, n10-b04) debe quedar enseñado antes en N8.
