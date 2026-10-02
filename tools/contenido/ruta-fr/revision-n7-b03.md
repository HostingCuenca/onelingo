# Revisión N7 · B3 (fr.n7.c11–c15) · «Le fait divers»

GO

Revisor independiente. Archivo revisado y corregido: `tools/contenido/ruta-fr/n7-b03.json` (únicas ediciones). Validación: `validar_ruta.py fr --borrador n6-b01…n6-b10 n7-b01 n7-b02 n7-b03` → 0 errores; `validar_plan.py fr` sin «título de la unidad difiere» para fr.n7.c11–c15. También validé con todos los borradores n7/n8 presentes: ningún error nuevo atribuible a este bloque.

## Contraste con las fichas

- Títulos, objetivos, gramática, `introduce`, `recicla`, vocabulario (8 palabras de la ficha en tarjeta + 1–3 de apoyo por clase), situación (29/30/29/29/30) y tarea coinciden con `curriculo/fr/n7.json`. Nada de clases posteriores.
- El plan de ejercicios está completo en formato y clave en las cinco clases (guiada 5, independiente 4, situación 2, evaluación 6–7).
- Situaciones: 375 / 328 / 349 / 330 / 345 palabras de diálogo (rango N5–N7: 300–500).
- Evaluación puntuable: c11 6 ítems / 5 formatos; c12 7 / 5; c13 7 / 6; c14 6 / 4 (+ `abierta`); c15 5 / 3 (+ `abierta`). Todas ≥ 4 ítems y ≥ 2 formatos, sin contar los `abierta`.
- Producción abierta: c14 e7 (modelo 17 palabras ≥ 12) y c15 e6 (16 ≥ 10). Cumplen el punto 13.
- Hablantes: nombres o papeles franceses (Le témoin, L’expert, Le commissaire, Un journaliste, Le policier, Ana, Hugo).
- Tipografía: U+202F antes de ? ! : ; y dentro de « », ’ en todo el francés (corregido donde faltaba).
- Pronunciación: guías revisadas (sh/zh, nasales, ü/ö definidos al aparecer). Un error corregido (ver c15).

## Correcciones (clase, ítem: antes → después)

### Opciones/preguntas en español-inglés → francés (pedido del coordinador)
Se enseñó lo necesario con tabla/ejemplos o se eligieron palabras ya enseñadas; no se tocó ninguna tarjeta de vocabulario.

- c11 g2: opciones es/en (Subjuntivo / Indicativo / Condicional) → `pregunta` «Que + ___ en tête de phrase : quel mode ?» con subjonctif / indicatif / conditionnel.
- c11 e5 (escuchar): opciones es/en (De sorpresa / De alegría / De indiferencia) → «Il est surpris. / Il est content. / Il est triste.»
- c11 s2: `preguntaApoyo` es/en → «Qu’est-ce qu’Ana trouve étonnant ?»
- c12 g2, s1, s2: `preguntaApoyo` → «Quelle phrase est une hypothèse sans si ?», «Selon l’expert, que se serait-il passé sans le camion ?», «Qu’est-ce qui a rendu l’accident plus grave ?»
- c12 i4 (escuchar): opciones es/en → «Que s’est-il passé ?» + «Un camion a causé l’accident. / Il n’y avait pas de camion. / Rien n’est arrivé.»
- c13 g4 y e4 (se douter): opciones es/en → «Il le soupçonne. / Il en doute. / Il le défend. (o le sait)». Palabra nueva enseñada: **soupçonne**, en la fila de la tabla («Il se doute que son voisin est coupable : il le soupçonne.»); la fila de douter ahora lleva «Il doute que son voisin soit coupable : il n’y croit pas.» y la explicación p2 (es/en) cita «il le soupçonne».
- c13 i1: opciones es/en → «« Nul doute que le témoin a vu la scène » : quel degré ?» con une certitude / un doute / une hypothèse.
- c13 e5 (escuchar): opciones es/en → «Quel degré ?» con Le doute. / La certitude. / La possibilité.
- c13 s1, s2: `preguntaApoyo` → «Que dit le commissaire du gardien ?», «Quelle piste est très probable ?»
- c14 g3 y e3 (si tant est que): opciones es/en → paráfrasis francesas con «À supposer qu’il ait bien regardé / vraiment vu la scène.» (el repaso a-supposer-que se practica en francés).
- c14 e5 (escuchar): opciones es/en → «Le témoin est-il certain ? Non, il reste prudent. / Oui, il est sûr.»
- c14 s1, s2: opciones/`preguntaApoyo` → «Pourquoi Ana dit « autant que je m’en souvienne » ?» (Elle n’est pas sûre de tout. / Elle veut cacher la vérité. / Elle est fatiguée.) y «Avant le vol, qu’est-ce que le portier avait déjà fait ?» (Il avait fermé la porte. / Il avait appelé la police. / Il avait vu le voleur.)
- c15 g3, g4, s1, s2: opciones es/en y `preguntaApoyo` → francés («« À défaut de témoins » signifie : …», «…l’information est… confirmée / non confirmée», «Quelle information n’est pas confirmée ?», «Que font les enquêteurs sans témoins ?»).

### Corrección de contenido y de francés
- c12 tabla p3: mezcla de español dentro de celdas francesas («si + plus-que-parfait (repaso)», «en + gérondif (el sujeto no cambia)») → celdas solo en francés («si + plus-que-parfait», «en + gérondif (même sujet)»); la glosa va en la columna de apoyo. Se evitó duplicar el gerundio (la primera fila dice «por una acción»; la segunda, «quien hace la acción es quien evita»).
- c14 tabla p3: «que je sache (fórmula fija)», «à ma connaissance (sin que)» → solo francés; la glosa pasa a la columna de apoyo.
- c15 tabla p3: la fila «conditionnel présent» mostraba «aurait roulé» (¡condicional pasado!) → fila présent con «Le conducteur serait en garde à vue…», fila nueva «conditionnel passé» con «aurait roulé trop vite…» y fila «conditionnel passé, voix passive» con «aurait été interpellé…». Se conserva todo el léxico enseñado.
- c15 g1: «Faute de ___, l’affaire a été classée.» admitía preuves / témoins / motifs → se añadió la pista del plan «(les preuves)» y `aceptadas: ["preuve"]`.
- c14 g4: «Le voleur était déjà parti : le portier ___ la porte avant.» (incoherente) → «Le portier ___ la porte avant le vol. (fermer)» (avait fermé).
- c14 e4: «le voleur ___ déjà. (partir)» obligaba a «était parti déjà» → «Le voleur ___ quand la police est arrivée. (partir)».
- c13 e7: la consigna fijaba selon toute vraisemblance pero `aceptadas` admitía otra fórmula → consigna ahora pide «una fórmula de probabilidad alta (selon toute vraisemblance o il y a tout lieu de croire que)»; feedback y `aceptadas` cubren ambas y los dos órdenes.
- c12 e7: `aceptadas` ampliada con «Avec une meilleure visibilité, il aurait évité l’angle mort.» y «Il aurait évité l’angle mort avec une meilleure visibilité.»
- c14 g5 y e6 (ordenar): `aceptadas` con el orden natural alternativo («Il n’y avait personne dans la rue, que je sache.», «Il n’a rien pris, que je sache.»).
- c15 situación: Hugo decía que dos vecinos daban versiones y luego Ana hablaba de «à défaut de témoins» (contradicción) → Hugo: «On dit dans le quartier que le feu ne marchait pas, et aussi que le conducteur roulait vite. Mais personne n’a vu l’accident…» (es/en actualizados). Hugo ya no dice «pour ta revue» sino «pour la revue du quartier».
- c15 nota de pronunciación de «le conducteur mis en cause» decía que la s de mis no suena, pero la guía escrita «mi zan koz» y el francés real enlazan → «la s de mis se enlaza con en y suena como z (mi zan)» (es/en).
- c13 traducción es del diálogo: «Entre las dos horas no vino nadie» → «Entre una hora y otra no vino nadie».
- Inglés/español de EE. UU. y América: c12 «insurance assessor» → «insurance adjuster» (contexto y glosa de l’expert); c13 glosa de le commissaire «police chief (superintendent)» → «police commissioner (senior police officer)».

### Reparto y encaje con el hotel
- c11: Ana tenía solo su crónica «Une Équatorienne à Paris» (b01–b02). Para que la sección de sucesos encaje, el contexto y la primera réplica dicen ahora «En plus de ma chronique, j’écris cette fois un article de fait divers pour la revue du quartier» (es/en actualizados).
- c14: Ana sale del hotel a las 22 h «après un événement» (coordina los eventos del hotel), contexto es/en actualizado.

## Comprobaciones sin cambios

- Una sola respuesta defendible en todos los ítems puntuables; `relacionar` (c13 g1/e1, c15 e5) con glosas claramente distintas; pistas específicas de cada ítem.
- c12: hipótesis sin si correctas (sans/avec/à moins de/gérondif con mismo sujeto/yuxtaposición/inversión Aurait-il…); errores frecuentes coherentes.
- c13: certeza + indicativo; probabilidad alta + indicativo; il se pourrait que / je n’exclus pas que / rien ne prouve que + subjuntivo; se douter (indicativo) vs douter (subjuntivo).
- c14: pour autant que / autant que je m’en souvienne / que je sache + subjuntivo; à ma connaissance sin que; si tant est que; tres tiempos del pasado.
- c15: faute de / faute d’avoir / à défaut de; condicional periodístico; escenarios y que + subjuntivo al inicio como repaso.
- Español neutro de América y inglés americano en explicaciones, glosas, feedback y traducciones.

## Hechos del reparto confirmados

- Ana colabora de forma puntual en la sección de sucesos (fait divers) de la revista del barrio, además de su crónica «Une Équatorienne à Paris»; entrevista a un testigo, a un perito de seguros y a un comisario / Besides her column “Une Équatorienne à Paris”, Ana occasionally contributes to the news (fait divers) section of the neighborhood magazine; she interviews a witness, an insurance adjuster and a police commissioner
- Ana coordina los eventos culturales del hotel y sale a veces tarde: una noche hacia las 22 h, tras un evento, presencia un robo con arrebato de bolsa frente al hotel (llovía) y declara ante un policía (c14) / Ana coordinates the hotel’s cultural events and sometimes leaves late: one night around 10 p.m., after an event, she witnesses a bag snatching in front of the hotel (it was raining) and gives a statement to a police officer (c14)
- El hotel tiene un portero (le portier), sin nombre: había cerrado la puerta antes del robo y llamó a la policía; la policía llegó diez minutos después (c14) / The hotel has an unnamed doorman (le portier) who had closed the door before the theft and called the police; the police arrived ten minutes later (c14)
- Hugo vive cerca de un cruce (carrefour) donde un auto chocó contra un escúter; oyó el choque desde su departamento sin ver nada y le lleva el suceso a Ana para la revista del barrio (c15) / Hugo lives near an intersection (carrefour) where a car hit a scooter; he heard the crash from his apartment without seeing anything and brings the story to Ana for the neighborhood magazine (c15)
- Los casos de c11 (robo en una tienda, testigo con dos versiones), c12 (choque en cadena en la circunvalación, martes por la noche), c13 (robo nocturno con rueda de prensa del comisario) y c15 (accidente en el cruce) son sucesos distintos del barrio y sin personajes recurrentes; los interlocutores son roles sin nombre (Le témoin, L’expert, Le commissaire, Le policier) / The cases in c11 (store theft, witness with two versions), c12 (pile-up on the beltway, Tuesday night), c13 (overnight robbery and the commissioner’s press conference) and c15 (intersection accident) are separate neighborhood incidents with no recurring characters; the interlocutors are unnamed roles (Le témoin, L’expert, Le commissaire, Le policier)
- Ana trata de vous al testigo, al perito, al comisario y al policía, y de tu a Hugo (coherente con el reparto canónico) / Ana uses vous with the witness, the adjuster, the commissioner and the police officer, and tu with Hugo (consistent with the canonical cast)

Sin choque con el reparto canónico (punto 12): no aparecen Monsieur Roux, Madame Lefort ni Madame Dubois; el director del hotel no interviene.

## Pendiente / avisos

- Nada pendiente en este bloque.
- Palabras francesas retiradas de pasos de enseñanza: ninguna que usen bloques posteriores (solo fragmentos en español dentro de celdas y las frases «Je me doute que le voisin est parti» / «Je doute que le voisin soit parti», sustituidas por frases con las mismas palabras). Palabra nueva enseñada: «soupçonne» (c13, tabla).
- Aviso para B4+: c11 (gérant, ancien employé) y c13 (ancien employé, gardien) comparten ambientes pero son casos distintos (hora de cierre 20 h frente a medianoche); si un bloque posterior los retoma, no deben unirse en un mismo caso.
