# Revisión independiente · N3 francés, bloque 1 (clases 1–5)

- **Archivo:** `tools/contenido/ruta-fr/n3-b01.json` (`fr.n3.c01` … `fr.n3.c05`). Revisor distinto del autor.
- **Validador:** `python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n3-b01.json` → **0 errores**; encadenado con `n3-b02.json` … `n3-b10.json` → **0 errores** (tras los últimos cambios).
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 errores, 10 avisos conocidos; ningún «título de la unidad difiere» para fr.n3.c01–c05.
- **Longitud de la situación** (150–250 palabras): c01 183 (5 líneas), c02 173 (4), c03 185 (5), c04 177 (11 réplicas de chat), c05 172 (5). Coherentes con sus ítems de comprensión.
- **Evaluación:** 5 ítems puntuables y 5 formatos distintos por clase; el `escribir` abierto (`abierta: true`) se suma aparte. 3 `erroresFrecuentes` por clase.
- **Tipografía:** U+202F antes de ? ! : ; en todo el francés nuevo; 0 apóstrofos rectos. Los títulos de c01 y c04 llevan espacio normal ante «!» porque así están en la ficha del plan (ver «Sin resolver»).

## Veredicto

GO

## Contraste con las fichas

Títulos, objetivos, gramática, `introduce`, `recicla`, vocabulario (todas las palabras de cada ficha), situación y tarea coinciden con `curriculo/fr/n3.json`. Los ejercicios planificados están todos (mismo formato y clave); el autor pulió la redacción (p. ej. c01 g2 «vivimos en París desde hace dos años», c04 e1 «viaje» en vez de «puesto»), sin cambiar formato, clave ni lo evaluado. Nada de c06 en adelante. Extras del autor que se mantienen: `épreuve`, `devoirs`, `progrès` y `secrétariat` en el correo de c02; `s’inscrire / inscrit`, `reçu`, `rangé` en la tabla de participios de c03 (los exigen sus ítems).

## Cambios aplicados (clase · ítem · antes → después)

### Reparto y tiempo de la historia

1. **c01 · patrón, ejemplo 3.** «Ana et Emma vivent ensemble depuis un an.» (desde N2 B3 ya son unos 18 meses) → «Ana et Emma vivent ensemble depuis longtemps.» (es / en ajustados).
2. **c01 · e6 (modelo abierto).** «je travaille à l’hôtel depuis un an» (Ana ya trabajaba en el hotel en enero de N2) → «depuis deux ans». «Ma famille est à Quito, et ça fait deux ans que je ne l’ai pas vue» (N2 c50 anuncia un viaje a Quito; no se sabe si ya lo hizo) → «Mes parents vivent à Quito.»; «Hugo travaille beaucoup, alors ça fait deux mois que je ne l’ai pas vu» (Hugo es estudiante y su mejor amigo) → «Hugo étudie beaucoup, alors ça fait deux semaines que je ne l’ai pas vu».
3. **c03 · situación, línea 2 (Hugo).** «Je me suis déjà inscrit à la salle de sport, et j’y vais le mardi et le jeudi.» contradecía N2 c44 (Hugo y Ana ya entrenan en esa sala) y la ficha (zapatillas) → «J’ai déjà acheté des chaussures de sport.» (es «Ya compré zapatillas deportivas», en “sneakers”); s1 opción correcta: «Il a acheté des chaussures de sport.» y su feedback.
4. **c05 · situación, línea 3 (Emma).** «dans la maison de Madame Dubois» (la traducción decía «edificio»; N2: Madame Dubois vive en la planta baja del edificio) → «je vis avec Ana au premier étage, et Madame Dubois vit au rez-de-chaussée» (es «en la planta baja», en “ground floor”, con «second floor (1er étage)»).
5. **c05 · situación, línea 4.** Emma solo trabaja los fines de semana pero «solo tiene un día libre»: se explica → «Avec mes cours, je n’ai qu’un jour libre en semaine : le mercredi» (es «Con mis clases…», en “With my classes…”).
6. **c05 · tabla p7.** «Cette année, j’ai changé de quartier.» (Emma y Ana se mudaron en N2, no «este año») → «Ana a changé de quartier.»; «Emma est devenue plus organisée.» → «Cette année, Emma est devenue plus organisée.» (así «année» queda enseñada antes del ejemplo 7).

### Nada de clases posteriores

7. **c01 · e2 (elegir).** «Hace tres meses que no la veo» con «vue» anticipaba la concordancia de c02 → «Hace tres meses que no lo veo» / «___ trois mois que je ne l’ai pas vu.».
8. **c01 · situación, línea 4.** «Ça fait longtemps que je ne les ai pas vus.» (concordancia con COD antepuesto, de c02) → «Ça fait longtemps que je n’ai pas vu ces amis.» (es «Hace mucho que no veo a esos amigos», en “those friends”).
9. **c03 · situación, línea 3.** «ça fait un mois que j’y pense» (y = à + cosa es de c04) → «j’ai la guitare depuis un mois, mais je n’ai pas le temps» (es / en ajustados).

### Corrección y claridad

10. **c01 · práctica independiente i1 (opciones es / en).** Hablaba en tercera persona («No lo ve desde hace dos meses» / “He hasn’t seen him…”) sobre un audio en primera → «Hace dos meses que no lo veo.» / «Lo vi ayer.» / «Lo veré dentro de dos meses.» (en: “I haven’t seen him for two months.” …).
11. **c01 · e5 (aceptadas).** + «Emma vit depuis trois ans à Paris.»
12. **c02 · explicación p2 (es).** «Con el pronombre y la regla del sujeto no te confundas…» (ininteligible) → «No te dejes guiar por el sujeto, sino por el lugar del COD: … (el COD va detrás: sin concordancia) … (el COD va delante: con concordancia).» El en se amplía igual.
13. **c02 · ejemplo 7.** «Je n’ai pas atteint ma mention ; j’ai échoué à une épreuve.» (no es natural) → «Je n’ai pas atteint la mention « très bien », mais je n’ai pas échoué.» (es «No alcancé la mención «muy bien», pero no suspendí.»).
14. **c02 · tabla p4 y explicación p3.** La ficha nombra «ouverte» y no aparecía → fila `ouvrir / ouvert / ouverte` y guía de sonido en es («u-vèr» / «u-vèrt») y en (“oo-VAIR” / “oo-VAIRT”).
15. **c02 · e2 (consigna).** «Los concursos que pasaron eran fáciles» (en español «pasar» = aprobar, justo el falso amigo de la clase) → «que presentaron».
16. **c02 · e5 (aceptadas).** + «Je les ai vus hier.»
17. **c02 · situación, línea 4.** «venir le chercher au secrétariat avec Chloé» (sugería ir con ella) → «… au secrétariat.» (es / en sin «con Chloé» / “with Chloé”).
18. **c03 · explicación p2 (es / en).** El en decía que el adverbio «a menudo va en otro sitio» con un ejemplo cuyo orden coincide con el francés → compara «already / yet» al final (“I’ve signed it already”, “I haven’t started yet”). El es: «al principio o al final: «Ya firmé», «Firmé ya»; en francés va dentro del verbo».
19. **c03 · i2 (aceptadas).** + «J’ai enfin téléphoné à Emma.», «Enfin, j’ai téléphoné à Emma.» (llamar = appeler / téléphoner).
20. **c03 · e1 (aceptadas).** «Todavía no he leído este libro» admite también «toujours pas» → `aceptadas: ["toujours pas"]`.
21. **c04 · id `v-mériter` → `v-meriter`** (y su ref) para mantener ids ASCII.
22. **c04 · tabla p4.** Las etiquetas «penser à (avant)», «rêver de (avant)» → «(imparfait)».
23. **c04 · situación, última réplica.** «je suis très contente de vous» (suena a profesora) → «Merci à tous, vous êtes super !» (es / en ajustados).
24. **c04 · es neutro.** «te lo has ganado» → «te lo ganaste» (situación, tabla p6, ejemplo).
25. **c04 · e5 (aceptadas).** + «Félicitations, Emma, pour ton examen !», «Bravo, Emma, pour ton examen !», «Félicitations pour ton examen, Emma !» (con U+202F).
26. **c05 · explicación p1.** «ne… que rodea al auxiliar» era erróneo → «ne va antes del auxiliar y que antes de lo limitado, después del participio: Je n’ai vu qu’un film» (en añadido igual).
27. **c05 · pista g3.** «se mettre pierde la -t final» (impreciso) → «Con elle la forma es se met (una sola t); je me mets, il se met.»
28. **c05 · nota de «se mettre à».** «sö métr a» → «sö mètr a».
29. **c05 · i3 y e5 (aceptadas).** i3 + «Je ne vois Léa que le week-end / weekend.» (con y sin «Maintenant,»); e5 + «Je n’ai qu’une heure de libre.»

## Revisión punto por punto

1. **Francés de Francia.** vivre (je vis / il vit, j’ai vécu), ça fait… que + presente o passé composé con negación, depuis; participio con COD antepuesto (pronombre y que), sin concordancia con COD detrás; déjà / pas encore / toujours pas entre auxiliar y participio; y / en con cosas y pronombre tónico con personas; ne… que, ne… plus que, devenir, se mettre à (s’est mise), changer de. Correcto.
2. **Explicaciones es / en.** Cortas, con ejemplos; es con tú y léxico neutro (departamento, licencia, pasantía, auto, boleto, zapatillas); en en inglés americano.
3. **Respuesta única.** Revisados los 5 `ordenar` por clase (un orden natural; «Enfin,…» incluido donde cabe), los `completar` con `opciones`, los `escribir` y los `escuchar`.
4. **Pistas y relacionar.** Cada pista ayuda a su ítem; glosas distintas (c01 g4 duraciones deux / cinq ans, un mois; c04 g5 penser à → y, rêver de y profiter de → en con verbos distintos).
5. **Guías de sonido.** j / g suave = «sh» / “zh”; in / ain / un = «en»; an / en = «an»; ü y ö se definen en la primera explicación de sonido de cada clase y en las notas de las tarjetas; consonantes finales exactas (toujours, récompense, longtemps, but, routine).
6. **Hablantes.** Solo Lucas, Monsieur Martin, Hugo, Léa, Ana, Emma; nunca en español. Tuteo entre amigos; vous entre Monsieur Martin y Ana.
7. **Diálogos y cortesía.** Los textos modelan el objetivo (novedades con «Quoi de neuf ? Qu’est-ce que tu deviens ?», balance con déjà / pas encore, felicitaciones «Chapeau ! Tu l’as bien mérité», cambios de vida).
8. **Abiertos.** Los `escribir` de cierre llevan `abierta: true` con rango de palabras y no cuentan entre los 5 puntuables.

## Hechos del reparto confirmados

- Lucas vive ahora en Montreal (se mudó de su pueblo hace unos tres meses; departamento pequeño, estudia en una escuela grande y trabaja los sábados en un café); su hermana se casa en junio y vive con su novio desde hace tres años; sus padres han vivido siempre en el pueblo; dos amigos suyos se separaron; Lucas y Ana llevan casi un año sin escribirse (c01). / Lucas now lives in Montreal (he moved from his village about three months ago; small apartment, studies at a big school and works Saturdays at a café); his sister gets married in June and has lived with her boyfriend for three years; his parents have always lived in the village; two of his friends split up; Lucas and Ana haven’t written to each other for almost a year (c01).
- Ana lleva dos años en París, trabaja en la recepción del hotel y vive con Emma; Emma lleva tres años en París (c01). / Ana has lived in Paris for two years, works at the hotel front desk and lives with Emma; Emma has lived in Paris for three years (c01).
- Ana aprobó las cuatro pruebas del examen de fin de curso de Monsieur Martin con la mención «bien» (no «très bien»), sacó 82 puntos sobre 100 en el concurso de la escuela y recibe un libro de la escuela, que recoge en la secretaría; Ana y Monsieur Martin se tratan de vous (c02). / Ana passed all four tests of Monsieur Martin’s end-of-course exam with the grade “bien” (not “très bien”), scored 82 out of 100 in the school’s competitive exam and gets a book from the school, which she picks up at the office; Ana and Monsieur Martin use vous (c02).
- Léa presentó el examen de conducir en marzo y lo aprobó a la primera (lo anuncia en el chat de grupo); hablará del auto con su madre y su hermano pequeño quiere aprovecharlo; Ana todavía no tiene licencia; Hugo organiza una fiesta el sábado a las 8 en su casa (c02, c04). / Léa took her driving test in March and passed on the first try (she announces it in the group chat); she will talk about the car with her mother and her little brother wants to use it too; Ana doesn’t have a license yet; Hugo throws a party on Saturday at 8 at his place (c02, c04).
- Hugo, al hacer balance de sus buenos propósitos: ya compró zapatillas deportivas y terminó su informe de pasantía; todavía no ha empezado la guitarra (la tiene desde hace un mes); sigue sin escribirle a su abuela de Lyon (ella espera su carta desde hace dos meses); por fin encontró un curso de baile (va desde hace tres semanas); su meta es hacer deporte tres veces por semana (c03). / Hugo, reviewing his resolutions: he has already bought sneakers and finished his internship report; he hasn’t started the guitar yet (he’s had it for a month); he still hasn’t written to his grandmother in Lyon (she has been waiting for his letter for two months); he has finally found a dance class (going for three weeks); his goal is to exercise three times a week (c03).
- Emma se puso a correr por las mañanas; vive con Ana en el primer piso (Madame Dubois, en la planta baja); ya solo trabaja los fines de semana en el restaurante de Karim (antes, todas las noches); con sus clases solo tiene un día libre entre semana, el miércoles; se ha vuelto más organizada (c05). / Emma started running in the mornings; she lives with Ana on the second floor (1er étage), with Madame Dubois on the ground floor; she now only works weekends at Karim’s restaurant (before, every evening); with her classes she has only one day off during the week, Wednesday; she has become more organized (c05).

## Sin resolver (no bloquea)

- No se eliminó ni renombró ninguna palabra francesa que B2–B10 puedan usar: las que dejaron de aparecer en frases (p. ej. «salle de sport», «j’y vais») siguen enseñadas en N1 / N2; todos los bloques N3 encadenan con 0 errores.
- Los títulos de c01 y c04 en la ficha (`curriculo/fr/n3.json`) llevan espacio normal antes de «!» dentro del título en español («Ça fait longtemps ! Ponerse al día», «J’y suis arrivée ! Y y en con cosas»). El borrador los copia tal cual para que coincidan; si el coordinador corrige la ficha, habrá que poner U+202F en ambos sitios.
- «Hace casi un año que no se escriben» (c01, pedido por la ficha) convive con la visita de Lucas a París de N2 B7: se lee como un año sin escribirse tras esa visita, no como un año sin verse.
- La tarea abierta de c01 usa en el modelo una ficha de Ana (deux ans à Paris, hôtel depuis deux ans) válida si el «ahora» de N3 es otoño de 2028; si otros bloques fijan otra fecha, basta ajustar esas dos duraciones (no puntúan).
