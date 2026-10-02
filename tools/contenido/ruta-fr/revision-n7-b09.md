# Revisión independiente · N7 francés, bloque 9 (clases 41–45)

- **Archivo:** `tools/contenido/ruta-fr/n7-b09.json` (`fr.n7.c41` … `fr.n7.c45`). Revisor distinto del autor.
- **Validador:** `python3 tools/validar_ruta.py fr --borrador` con los borradores no integrados (N6 ya está en `assets/contenido/fr/ruta/`, así que se quitó de la lista; quedan n7-b01 … n7-b10) → **0 errores**.
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 avisos «título de la unidad difiere» para c41–c45 (títulos y objetivos idénticos a las fichas).
- Modo de vocabulario estricto: activo (el validador cuenta solo lo mostrado en tarjetas, ejemplos, patrones y tablas).

## Veredicto

GO

## Contraste con las fichas

Cada clase enseña lo que dice su ficha y nada de clases posteriores: c41 subjuntivo imperfecto y pluscuamperfecto en reconocimiento (3.ª persona, `eût-il su`, equivalentes actuales, repaso del passé simple); c42 estilo indirecto libre, tipos de narrador y focalización; c43 `à` de caracterización (au / aux / à la / à l’), `d’un air` / `l’air`, `avoir quelque chose de + adjetivo`; c44 puntuación del diálogo, inciso con inversión y verbos de habla; c45 `ne serait-ce que`, `mériter d’être`, `valoir la peine que`, `si ce n’est`. Vocabulario: las 8 palabras de cada ficha, exactas. El plan de ejercicios está completo (mismo formato y clave en guiada, independiente, comprensión y evaluación; la redacción está pulida y se completaron `aceptadas` y pistas).

**c41, reconocimiento solamente.** Ningún ítem exige producir una forma literaria: se identifican (elegir, escuchar), se relacionan con su equivalente actual (relacionar) o se convierten al francés actual (completar `soit`, escribir `Il fallait qu’elle parte…`). Los passés simples solo se reconocen (e5 pide los infinitivos). Ni c44 ni c45 piden escribir passé simple ni `ne fût-ce que` (se reconocen).

**Anatomía y tiempos:** explicación (3–4 textos) → tablas (3–5, con «Para leer…» reales: forma + sentido + frase) → ejemplos (8) → vocabulario (8 tarjetas) → guiada (5, con pista) → independiente (4, sin pista) → situación (7–10 líneas, 304–313 palabras con la cuenta más estricta, 321–343 con la de `wc`; rango N7 300–500; 2 ítems de comprensión coherentes con el texto) → evaluación. `erroresFrecuentes`: 3 por clase.

**Evaluación (≥ 4 puntuables en ≥ 2 formatos; los `escribir` con `abierta: true` no cuentan):** c41, 7 puntuables en 5 formatos (relacionar, elegir, completar, escuchar, escribir); c42, 5 en 4 (elegir, completar, relacionar, escuchar) + 1 abierta; c43, 5 en 2 (elegir, completar) + 1 abierta; c44, 5 en 4 (elegir, completar, relacionar, ordenar) + 1 abierta; c45, 5 en 2 (elegir, completar) + 1 abierta. Todas las abiertas llevan `minimoPalabras` y su modelo lo cumple (el validador lo exige). En el bloque aparecen los seis formatos.

**Opciones en francés (punto 14):** todas las opciones de elegir/escuchar están en francés. **Tablas «Para leer…» (punto 14):** sin celdas sueltas ni nombres propios; se añadió sentido donde faltaba (ver cambios).

**Tipografía (U+202F):** revisados los 634 textos franceses (ejemplos, tablas, diálogos, preguntas, opciones, respuestas, tokens) y las citas francesas dentro de consignas, feedback y explicaciones: espacio fino antes de ? ! : ; y dentro de « » en todos; apóstrofo ’.

## Cambios aplicados (clase · ítem · antes → después)

### c41
1. **p2 (explicación, es / en).** «El subjuntivo imperfecto siempre va después de que y lleva circunflejo» (falso para `eût-il su`) → «va después de que (salvo eût-il su…, con inversión) y, en la 3.ª persona, lleva circunflejo».
2. **p3 (explicación).** Se quita «Lo mismo pasa con ne fût-ce que… (la verás en la clase 45)»: adelantaba contenido de c45.
3. **p6 (tabla del passé simple).** Los infinitivos (regarder, prendre, ouvrir, sortir, demander, craindre, dire, vaincre) no tenían sentido → nueva columna «Sentido» (mirar, tomar, abrir, salir, preguntar, temer, decir, vencer).
4. **Situación, línea de Ana (Bien qu’il eût vu…).** «Cela fait déjà six formes littéraires» no cuadraba con el texto (hay cinco: partît, fût, eût vu, fût partie, eût-il su) → «cinq» (es / en ajustados).
5. **Situación, cierre de Ana.** El texto era de 281 palabras (mínimo N7: 300): se añade «C’est aussi un bon exercice pour moi : je lis un extrait, je cherche les formes littéraires, puis je les écris en français actuel.» (es / en). Sin palabras nuevas.
6. **e7 (escribir).** La consigna no mostraba la frase que había que reescribir → «Tarea: reescribe en francés actual la frase literaria: Il fallait qu’elle partît avant qu’il fût tard.» (la frase del plan) y `aceptadas`: «Il fallait qu’elle parte avant qu’il ne soit tard.» (con ne explétif, también válido).
7. **e5 (feedback).** Aclara que `vit` en una serie de passés simples viene de voir y no de vivre (el distractor «venir, vivre, vaincre» es plausible para un lector que piense en el presente de vivre).

### c42
8. **p3 (explicación, es).** «una voz extérior» (palabra francesa en el texto en español) → «una voz exterior».
9. **p6 (tabla).** Solo tenía francés → nueva columna «Sentido (directo → libre)» con cada cambio traducido (no iré → ella no iría, etc.).
10. **p7 (tabla «términos del análisis»), fila l’auteur.** La frase «L’auteur est un narrateur omniscient» contradecía el distractor de g2 («l’auteur omniscient» es falso) y la teoría (autor ≠ narrador) → «L’auteur écrit le roman ; le narrateur raconte l’histoire.»
11. **g4 (pista).** «Piensa en una definición para cada término de las tablas» (genérica) → una pista que describe cómo suena cada término (monólogo con «je», focalización = punto de vista, omnisciente lo sabe todo, indirecto libre sin verbo introductor).
12. **Situación (contexto, es / en) y reparto.** «Ana participa en un taller de escritura del barrio. Monsieur Martin, su profesor…» no decía quién dirige el taller → «…el taller de escritura del barrio, que dirige Monsieur Martin, su profesor de francés. Esta noche él propone leer…» (coherente con el «Bonsoir» de la primera línea).
13. **Situación (texto de 286 palabras).** Se añade en la línea de Martin: «Très bien. Regardez aussi « demain » : le narrateur garde le mot du personnage, il ne dit pas « le lendemain ».» (es / en), que modela la diferencia entre indirecto libre e indirecto que explica p2; 304 palabras.
14. **i3 y e6 (consignas).** Las citas francesas llevaban espacios normales antes de : y ? → U+202F.

### c43
15. **Situación, línea de Hugo.** «lis-moi» (palabra que enseña n7-b04 y no este bloque; el validador solo la aceptaba mientras el borrador de b04 la incluyera) → «Vas-y, j’écoute.» (palabras ya enseñadas, igual que en c45).
16. **Situación, línea de Ana.** «il a l’allure fatiguée» (poco idiomático) → «il a l’allure d’un homme fatigué» (es / en ajustados). Se añade en la línea de Hugo «Parle aussi du personnage secondaire : sa silhouette et son regard donnent une autre image du film.» y en el cierre de Ana «Je garde aussi la dernière scène et ton conseil sur la place des adjectifs.» (es / en): el texto pasa de 283 a 313 palabras.
17. **p2 (explicación).** «No se dice “d’air las” ni “un air las” solo» era erróneo (un air las existe como sustantivo: Il avait un air las) → «Como complemento de manera no se dice “d’air las” ni “Elle répondit un air triste”: falta la preposición d’».
18. **p6 (tabla «le même adjectif, deux sens»).** Sin sentido en la fila de grand ni en el resto → nueva columna «Sentido (antes / después)»: digno de lástima / sin dinero; un excolega / un colega de edad avanzada; un gran hombre / un hombre alto.

### c44
19. **Situación (texto de 272 palabras, línea duplicada de Ana, incoherencia).**
    - Dos líneas seguidas de Ana (la pregunta «Je vous la lis ?» y «Voici ma scène») → se intercala «Oui, je vous écoute, Ana.» de Martin.
    - Martin decía que la puntuación era correcta y Ana respondía «je corrige cela tout de suite» → Ana responde «Merci. Pour les verbes, j’ai cherché…», y Martin añade el caso que modela la norma de la clase: «Quand la réplique finit par un point d’exclamation ou d’interrogation, il n’y a pas de virgule avant l’incise : vous avez raison.»
    - Cierre de Martin: «Un lecteur doit voir les personnages et entendre leur voix : c’est le rôle de la réplique et de l’incise.»; cierre de Ana: «J’ai compris : une réplique, une ligne, un verbe précis.» (es / en). Total 305 palabras.
20. **Contexto (reparto).** Martin pasa a ser «su profesor y director del taller de escritura del barrio» (continuidad con c42).
21. **p6 (tabla del inciso en presente y passé simple).** Formas conjugadas sin sentido (murmure-t-elle, s’écrie-t-il, répondit-il…) → nueva columna «Sentido» (murmura ella, exclama él, responde él…) y fila nueva `demande-t-elle / demanda-t-elle` (aparece en el diálogo y en los ejemplos). Se enseña como tabla de patrón con sentido, no como palabras sueltas.
22. **Vocabulario `le retour à la ligne` (nota).** «la ü no aparece: ou = u» (confuso) → «ou = «u» española; gn = «ñ» (como en «niño»)» (es / en).
23. **g4 (pista).** «Mira la tabla de los verbos de habla» → pista por tono de voz (muy bajo, confuso, cansado, fuerte).
24. **i3 (consigna).** « Viens » con espacios normales → U+202F.

### c45
25. **Situación (incoherencia).** Ana contestaba «Pas encore» y después «J’ai lu le début, et c’est vrai», pero escribía una crítica completa del libro y de la película (incluida la reserva sobre el final de la película) sin haberlos leído ni visto → Ana contesta «Oui, je l’ai lu cet été et j’ai vu le film hier.»; «Justement. Pour moi, ce roman mérite…»; «Je suis d’accord : c’est le plus beau roman que j’aie lu cette année.» Contexto reescrito (Hugo lo recomendó; Ana ya leyó el libro y vio la película y le lee su crítica). Sin palabras nuevas.
26. **Situación, línea 8 de Ana.** «Je vais aussi parler du public visé» repetía lo que su texto ya decía («Le public visé est large») → «Je vais aussi ajouter que ce n’est pas un livre pour tout le monde, mais qu’il peut plaire à beaucoup de lecteurs.»
27. **p1 (explicación).** «Se coloca después de una coma, con pour + nombre» contradecía la última línea del texto de Ana («Ne fût-ce que par curiosité») → «con pour + nombre (pour la musique) o par + nombre (par curiosité)».
28. **Traducciones.** «vale la pena de verse» (p4, p8, diálogo; no es español natural) → «vale la pena verla»; vocabulario `le coup de cœur`: «el favorito del corazón» → «el favorito, la obra que nos enamora»; inglés «the cinema» → «the movies».
29. **g5 (aceptadas).** + «j’aie» (quien escribe la forma completa con el pronombre).

### Varios
30. **Tipografía en apoyos.** Espacios normales dentro de « » y ante ? ! : en las citas francesas de explicaciones, feedback y consignas (c42 p1, c44 p1 / p3 / feedback, etc.) → U+202F. El título de c44 se mantiene idéntico al de la ficha (que lleva espacios normales dentro de las comillas) para no activar el aviso «título de la unidad difiere».

## Comprobaciones sin cambios

- **Francés de Francia.** Verificados: subjuntivo imperfecto y pluscuamperfecto (fût, eût, fît, vînt, partît, vît, sût, pût, voulût; eût vu, fût partie, fût arrivé, eût fait; eût-il su = même s’il avait su / s’il avait su), passé simple (fit, vint, vit, vainquit, regarda, prit, ouvrit, sortit, craignit), estilo indirecto libre (conditionnel + imparfait, demain permitido), narradores y focalización, `aux / au / à la / à l’`, `d’un air + adjetivo masculino`, `quelque chose d’ / de`, posición del adjetivo (pauvre, ancien, grand), inciso con inversión y -t- (murmure-t-elle, s’écrie-t-il, répond-il, s’écrie Karim), `ne serait-ce que`, `mériter d’être + participio` (concordancia lu / lus / lue / lues), `valoir la peine que + subjonctif`, `si ce n’est`, superlativo + subjuntivo (aie, aies, ait, ayons, ayez).
- **Typografía de c44 (pedida por el coordinador).** Correcto: tras « … ? » o « … ! » no hay coma y el verbo del inciso va en minúscula (« Jamais ! » s’écrie Karim); si la réplica no termina en ? ni en !, la coma va después de las comillas (« Viens », murmure-t-elle); con tiret el inciso no lleva comillas; hay espacio fino antes de ? ! : ; y dentro de « ». Los errores frecuentes y los distractores (« Viens, » …, « Reste » murmure-t-il) son realmente incorrectos.
- **Una sola respuesta.** Revisados todos los completar (soit, partirait, viendrait, était, faisait, aux, à, d’, de, air, s’écrie, soupire-t-il, lu / lus, aie / ait / ayons), escribir (con `aceptadas` donde hay variantes: «ne soit», «a» sin acento ya lo normaliza la app) y ordenar (c44 i4 con las dos posiciones del inciso; e4 con una sola). Los relacionar tienen glosas distintas; los distractores de los elegir son siempre erróneos.
- **Idiomas de apoyo.** Español neutro con tú (usted solo en los diálogos con vous) e inglés americano (movie, gray…). Guías de pronunciación según las calibraciones (j/g = «sh», nasales, ü / ö definidas).
- **Anglicismos y regionalismos.** Ninguno de los listados en el punto 7.

## Hechos del reparto confirmados

- Madame Dubois, antigua casera de Ana que vive cerca y es amiga suya (se tratan de vous), le presta una novela realista del siglo XIX; Ana lee un fragmento en voz alta y lo pasa al francés actual (c41). / Madame Dubois, Ana’s former landlady who lives nearby and is her friend (they use vous), lends her a nineteenth-century realist novel; Ana reads an excerpt aloud and puts it into modern French (c41).
- Ana asiste al taller de escritura del barrio, que dirige Monsieur Martin, su profesor de francés (vous); es un taller nocturno y en él leen un relato breve narrado en estilo indirecto libre (c42). / Ana attends the neighborhood writing workshop, led by Monsieur Martin, her French teacher (vous); it meets in the evening and they read a short story told in free indirect speech (c42).
- Ana escribe una crítica de cine para la revista del barrio sobre una película francesa ficticia, «La Nuit blanche», y se la lee a Hugo, que trabaja como guía y conoce bien el cine francés (tu) (c43). / Ana writes a film review for the neighborhood magazine about a fictional French movie, “La Nuit blanche”, and reads it to Hugo, who works as a guide and knows French cinema well (tu) (c43).
- Ana participa con una escena de ocho réplicas, en presente, en el concurso de relatos de la revista del barrio y la trabaja con Monsieur Martin, su profesor y director del taller de escritura (vous) (c44). / Ana enters an eight-line scene, in the present tense, in the neighborhood magazine’s short-story contest and goes over it with Monsieur Martin, her teacher and the leader of the writing workshop (vous) (c44).
- Hugo recomienda a Ana la novela ficticia «La Rivière» (ochocientas páginas, con un premio literario, «coup de cœur» de Hugo) y su adaptación al cine; Ana la leyó este verano, vio la película ayer y escribe su crítica para la revista del barrio (tu) (c45). / Hugo recommends to Ana the fictional novel “La Rivière” (eight hundred pages, with a literary prize, Hugo’s “coup de cœur”) and its film adaptation; Ana read it this summer, saw the movie yesterday and writes her review for the neighborhood magazine (tu) (c45).

**Coherencia con N6 y N7 (comprobada).**
- Monsieur Martin: profesor de francés de Ana en la escuela de idiomas (N2), profesor de Hugo en la universidad y profesor invitado en su seminario (N6 b08: c39, c40), «profesor invitado» en el festival del barrio (N7 c05) y moderador del debate de la escuela de idiomas (N7 c30); trato de vous con Ana y con Hugo. Dirigir un taller de escritura del barrio por las tardes es un hecho nuevo que no contradice ninguno de esos papeles.
- Madame Dubois (N7 c06, c08, c10, c28, c49, c50): antigua casera, vive cerca, amiga de Ana; vous. No aparece como casera actual ni vive en el piso de abajo (esa es Madame Lefort).
- Hugo (N7): máster terminado, guía-conferenciante (c02, c16, c19, c46, c47, c50); tutea a Ana. Las revistas del barrio y la crónica «Une Équatorienne à Paris» enlazan con N7 c02, c11, c20, c21.
- Nadie trata de tu a Martin ni a Madame Dubois; Ana y Hugo se tutean.

## Pendiente / sin resolver

- **Dependencia entre bloques.** c43 ya no depende de «lis-moi» (que ahora enseña n7-b04). Las demás palabras del bloque se enseñan en N1–N6 o dentro de este bloque. Si el autor de un bloque anterior de N7 quita una palabra que c41–c45 usan, el validador lo señalaría.
- **Errores ajenos al bloque.** En una pasada intermedia el validador marcó `fruit` (n7-b04) y `finance` (c46 y c48 de n7-b10); en la última validación (0 errores) ya estaban corregidos por sus propios autores o revisores. No toqué esos archivos.
- **Título de c44.** La ficha escribe « Viens » con espacios normales; la unidad lo mantiene así por el comparador de títulos. Cosmético: se puede unificar con U+202F en la ficha y en la unidad a la vez.
- No se retiró ni renombró ninguna palabra francesa que enseñen los bloques siguientes de N7 (c46–c50); solo se añadieron filas y columnas de sentido, y las frases del diálogo modificadas usan vocabulario ya enseñado.
