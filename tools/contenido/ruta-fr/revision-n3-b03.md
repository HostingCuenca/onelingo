# Revisión independiente · N3 francés, bloque 3 (clases 11–15)

- **Archivo:** `tools/contenido/ruta-fr/n3-b03.json` (`fr.n3.c11` … `fr.n3.c15`). Revisor distinto del autor.
- **Validador:** `python3 tools/validar_ruta.py fr --borrador …n3-b01.json …n3-b02.json …n3-b03.json` → **0 errores** (repetido tras los últimos cambios).
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún «título de la unidad difiere» para c11–c15.

## Veredicto

GO

## Contraste con las fichas

Cada clase enseña lo que dice su ficha y nada de clases posteriores: c11 `dont` (de + persona o cosa, «cuyo» con artículo, elección qui / que / où / dont); c12 verbos recíprocos (presente con nous / on, passé composé con être y concordancia, sin concordancia con COI: se parler, se téléphoner); c13 ce qui / ce que, con c’est y tout ce qui / tout ce que; c14 ressembler à, le même… que, pareil que, comme, contrairement à, différent de; c15 manquer à y rendre + adjetivo (faire plaisir, pronombres COI). El participio con COD antepuesto ya se vio en c02, así que la nota sobre «tu m’as manqué» de c15 es repaso. Los planes de ejercicios están completos (mismo formato y clave; redacción pulida: c15 g4 usa Léa / Hugo en lugar del «Elle lui manque» genérico, c13 i2 usa «ma grand-mère» en lugar de «elle… qu’»). Anatomía: explicaciones (con nota de pronunciación) → tablas → ejemplos (8) → vocabulario (11–14 refs) → guiada (5, con pista) → independiente (3) → situación (172 / 183 / 161 / 170 / 167 palabras, 12–14 líneas; rango del nivel 150–250) → evaluación (6 ítems: 5 puntuables en 5 formatos + 1 `escribir` abierto, que no puntúa y se suma). Cada unidad tiene 4–5 errores frecuentes. Formatos del bloque: elegir, escuchar, ordenar, completar, escribir y relacionar (c11 g4, c14 g5, c15 g5, con glosas distintas). Hablantes: Hugo, Ana, Léa, Emma, Madame Dubois (nunca en español). Tipografía: U+202F antes de ? ! : ; y apóstrofo ’ en todo el bloque.

Vocabulario añadido por la gramática (declarado en `vocabulario` y enseñado en un paso): dont, Paul, Camille, Louis (c11); le lycée (c12); plaire, important (c13); le même, pareil, différent, contrairement à (c14); rendre, la voix, je t’embrasse (c15).

## Cambios aplicados (clase · ítem · antes → después)

### Francés y gramática
1. **c12 · explicación p3 (es / en).** El «truco» «si el verbo lleva à + persona no hay concordancia» chocaba con `se confier` (que lleva à y concuerda, y el propio bloque lo enseña así en la tabla y en el ejemplo «Léa se confie à sa mère»). → Se quita el truco y se añade la excepción: «se confier también lleva à (elle se confie à sa mère), pero ahí se es complemento directo: elles se sont confiées»; la lista de verbos con concordancia incluye ahora se confier.
2. **c12 · g4 `ordenar` (aceptadas).** «Ma sœur et moi, nous nous entendons bien.» → eliminada: no se puede formar con los tokens (`on`, `s’entend`). Queda «On s’entend bien, ma sœur et moi.»
3. **c13 · e4 `ordenar` (aceptadas).** (sin alternativa) → añadida «La tradition, c’est ce que je préfère.» (orden natural posible con los mismos tokens).
4. **c14 · i2 `escribir` (aceptadas).** Una variante → se añaden «Nous avons les mêmes défauts, ma mère et moi.» y «Ma mère et moi avons les mêmes défauts.»
5. **c11 · situación, línea de Louis.** «C’est Louis, le neveu de ma tante, dont la mère habite aussi à Lyon.» (dont se leía como complemento de «ma tante») → «C’est Louis, le neveu de ma tante. C’est le petit garçon dont la mère habite aussi à Lyon. Il a six ans.» (es / en actualizados: «Es Louis, el sobrino de mi tía. Es el niño cuya madre también vive en Lyon…»).
6. **c15 · e3 `escuchar`.** Audio «Ses amis lui manquent, alors ça lui fait plaisir quand ils téléphonent.» (sujeto de género indefinido; opciones con «elle» y consigna en inglés con «him») → «Les amis de Léa lui manquent, alors ça lui fait plaisir quand ils téléphonent.»; consigna en inglés «makes her happy» y feedback es / en actualizados.

### Reparto (coherencia con la historia)
7. **c12 · situación (contexto es / en, línea de Léa) y c14 · situación (línea de Emma).** El hermano de Léa tiene 12 años en N2 (11 en N1); N3 es un año después de N2 → «douze ans» / «12 años» / «twelve» → «treize ans» / «13 años» / «thirteen». **Ojo:** la ficha de c12 en `curriculo/fr/n3.json` aún dice «hermano de 12 años» (ver «Sin resolver»).
8. **c12 · situación, última réplica de Léa.** «Si, une fois, mais nous nous sommes parlé tout de suite…» («solo una vez» contradecía los ítems del propio bloque en que Hugo y Léa se enfadan «ayer») → «Si, mais nous nous sommes parlé tout de suite et nous nous sommes réconciliés.» (es: «Sí, pero nos hablamos enseguida e hicimos las paces.»).
9. **c11 · ejemplos.** «Ma marraine, que j’aime beaucoup, habite à Paris.» → «… habite à Lyon.» (es / en): en la situación y en el audio i1 la madrina de Hugo vive en Lyon.

### Español neutro de América / inglés americano
10. **c15 · todo el texto en español.** «echar de menos» (peninsular) → «extrañar»: «Te echo de menos» → «Te extraño»; «me echan de menos» → «me extrañan»; «Echo de menos a mi familia» → «Extraño a mi familia»; «la echa de menos» → «la extraña»; «Te eché de menos» → «Te extrañé»; encabezados de tabla y título de p1 («lo que extrañas»), consigna de e6 («a quién extrañas»). Las explicaciones siguen contrastando con «tú me haces falta».
11. **c12 · i3 consigna y vocabulario `se fâcher`.** «Hugo y Léa se enfadaron ayer» → «se enojaron»; «enojarse, enfadarse» → «enojarse, molestarse».
12. **c13 · i1 y e3 (consigna en inglés).** «what she likes» → «what the speaker likes» (los audios no fijan el género).
13. **c14 · error frecuente «Je ressemble mon père» (en).** «hides the preposition in English» → «English “I look like my father” has no “to”, but French needs à».
14. **c15 · error frecuente «Je te manque» (es).** Se sustituye «En español y en inglés el orden es el contrario» por «En español («te extraño») y en inglés («I miss you») el sujeto es quien siente; en francés es quien falta».

### Pronunciación, pistas y tipografía
15. **c15 · `faire plaisir` (nota es).** «fèr plé-zir» → «fèr plè-zir» (plaisir lleva è).
16. **c11 · g1 pista (es / en).** Daba la respuesta («es dont») → «el “de la tante” queda dentro del relativo; busca el relativo que equivale a “de la que”».
17. **c13 · p2 y c14 · s2 feedback.** Espacio normal antes de ? ! ; en francés citado dentro de texto de apoyo → U+202F (4 casos × es / en).

## Hechos del reparto confirmados

- La familia de Hugo vive en Lyon: su tía (que además es su madrina, la tía «dont je t’ai parlé»), su tío Paul (su padrino), cuyo hijo es chef en un restaurante de Lyon y cuya hija Camille es médica y su prima de la que está orgulloso, y Louis, un niño de seis años sobrino de la tía, cuya madre también vive en Lyon. / Hugo’s family lives in Lyon: his aunt (also his godmother, the aunt “dont je t’ai parlé”), his uncle Paul (his godfather), whose son is a chef at a Lyon restaurant and whose daughter Camille is a doctor and the cousin Hugo is proud of, and Louis, a six-year-old nephew of the aunt, whose mother also lives in Lyon (c11).
- La abuela de Hugo tiene cuatro nietos: Camille, Louis, el hijo de Paul y Hugo. Antes del sábado en Lyon, Hugo enseña a Ana las fotos de su familia. / Hugo’s grandmother has four grandchildren: Camille, Louis, Paul’s son and Hugo. Before the Saturday in Lyon, Hugo shows Ana his family photos (c11).
- Léa se lleva muy bien con su madre Sophie (se confían todo, se ven casi todos los domingos) y se pelea a menudo con su hermano de 13 años, que quiere usar su computadora; ayer se enojaron y enseguida hicieron las paces. / Léa gets along very well with her mother Sophie (they confide everything and see each other almost every Sunday) and argues often with her 13-year-old brother, who always wants her computer; yesterday they fell out and quickly made up (c12).
- Léa y Hugo se conocieron en el colegio hace cinco años, se llaman casi todos los días y, si se pelean, se hablan enseguida y hacen las paces. / Léa and Hugo met in high school five years ago, phone each other almost every day and, when they argue, talk right away and make up (c12).
- Ana y Emma nunca se pelean, se llevan muy bien y se hablan todas las noches; Emma está contenta de vivir con Ana. / Ana and Emma never argue, get along very well and talk every evening; Emma is happy to live with Ana (c12).
- Madame Dubois, viuda, celebra la Nochebuena en casa de su hija con toda la familia (gran comida y regalos para los niños); lo que más le gusta es reunirse con la familia, y desde la muerte de su marido lo importante para ella es la familia. Invita a Ana a un té un domingo por la tarde. / Madame Dubois, a widow, celebrates Christmas Eve at her daughter’s with the whole family (a big meal and gifts for the children); what she likes most is getting the family together, and since her husband’s death what matters to her is family. She invites Ana for tea on a Sunday afternoon (c13).
- En Quito la familia de Ana celebra la Nochebuena el 24, en familia, con una gran comida y música; lo que más le gusta a Ana es la música. / In Quito Ana’s family celebrates Christmas Eve on the 24th, with a big meal and music; what Ana likes best is the music (c13).
- Léa se parece a su madre Sophie (las dos son pacientes y serias); su hermano se parece a su padre (hablador) y, a diferencia de ella, es testarudo; Emma dice que no se parece a nadie de su familia y que es un poco celosa; Léa es más habladora que Emma y Emma más seria que Léa; las dos son generosas con sus amigos. / Léa takes after her mother Sophie (both patient and serious); her brother takes after their father (talkative) and, unlike her, is stubborn; Emma says she takes after no one in her family and is a little jealous; Léa is more talkative than Emma and Emma more serious than Léa; both are generous with their friends (c14).
- Hugo y su padre tienen el mismo carácter: los dos son muy serios. / Hugo and his father have the same personality: both are very serious (c14, audio de evaluación).
- Ana escribe en francés una tarjeta para el cumpleaños de su abuela de Quito (que no entiende francés) y se la lee a Emma para practicar; también la enviará en español. Emma la extraña cuando Ana trabaja en el hotel. / Ana writes a birthday card in French for her grandmother in Quito (who doesn’t understand French) and reads it to Emma to practice; she will also send it in Spanish. Emma misses Ana when she works at the hotel (c15).

## Sin resolver

- **Plan (`curriculo/fr/n3.json`, c12 `ejercicios.situacion.texto`):** dice «su hermano de 12 años». El bloque usa 13 (11 en N1, 12 en N2, 13 en N3). El coordinador debe actualizar la ficha (y, al copiar los hechos con `reparto.py`, el dato de edad del hermano de Léa para el resto de N3). No toqué el plan.
- Ninguna palabra francesa del bloque se eliminó o renombró; los bloques posteriores del nivel que reciclan `dont` (c31, c46) y ce qui / ce que (c22, c37, c43) no se ven afectados.
