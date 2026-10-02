# Revisión fr.n7-b10 (c46–c50)

GO

Validación: `python3 tools/validar_ruta.py fr --borrador n7-b01 … n7-b10` → 0 errores (n6 y n5 ya están integrados en `assets/contenido/fr/ruta/`, por eso solo se encadenó n7-b01…b10; con los borradores n6 en la lista da «id duplicado»). `python3 tools/curriculo/validar_plan.py fr`: 0 errores y ningún «título de la unidad difiere» para fr.n7.c46–c50.

Contrastado con las fichas de `curriculo/fr/n7.json`: cada clase enseña lo que dicen `introduce`/`gramatica`/`vocabulario`, no adelanta nada de clases posteriores y contiene los ejercicios del plan (mismo formato y clave). Cambios respecto al plan, todos por coherencia: c50 usa 1868 en vez de 1860 (ver abajo) y c49 amplía la evaluación a 26 ítems (24 puntuables + 2 abiertos), como pidió el coordinador. Longitud de la lectura (palabras francesas): c46 571 (ficha: 500–600), c47 319 (300–400), c48 342 (300–500), c49 312 (300–400), c50 405 (400–500). El artículo de c46 tiene unas 304 palabras y la contracción de Ana cuenta de verdad 71 (rango 67–82 para 75). Hablantes: solo Ana, Hugo y Madame Dubois. Tú/vous correcto (Ana–Hugo tú; vous solo en la simulación de c48; Ana–Madame Dubois vous). Tipografía: 0 incidencias (U+202F, ’, « »).

Evaluación puntuable (≥ 4 ítems y ≥ 2 formatos), sin contar los `abierta`:
- c46: 6 ítems, 5 formatos (elegir, completar, relacionar, ordenar, escuchar) + 1 abierto.
- c47: 5 ítems, 2 formatos (completar, elegir) + 1 abierto.
- c48: 5 ítems, 3 formatos (completar, elegir, ordenar) + 1 abierto.
- c49: 24 ítems, 6 formatos + 2 abiertos.
- c50: 6 ítems, 3 formatos (elegir, completar, escuchar) + 1 abierto.
Todos los modelos de los `abierta` cumplen su `minimoPalabras` (lo exige el validador).

c49, cobertura B1–B9 con ítems puntuables: B1 e6 (je ne saurais), e16 (registro); B2 e2 (futuro en el pasado), e7 (passé simple); B3 e1, e12, e13, e20; B4 e8 (aposición), e24 (faire l’objet de); B5 e9 (metáfora); B6 e14, e17, e21, e22; B7 e3, e23; B8 e4, e15; B9 e5, e10, e11, e25; B10 e18 (contracción). Cada ítem tiene una sola respuesta defendible; los distractores no son válidos.

## Correcciones

c46
- pw «Palabras para leer el artículo»: 16 filas → 10. Se quitan le revenu, apporter, le monument, le million, quitter, la culture (palabras ya enseñadas y transparentes; el validador no las necesitaba). Con «la culture» desaparecía la única frase que enseñaba «finance», así que la fila «financer» pasa a «Le tourisme finance la culture ; les billets d’entrée financent l’entretien des monuments.». Total de «Para leer» de la clase: 22 → 16 filas (pw 10 + pw2 6), todas necesarias para el validador y usadas en la situación (renchérir, épuiser, abordable, découvrir, proximité, fléau, habitable, enrichir, essentiel, financer, condensé, formulation, détériorer, disparition, nominaliser, au profit de).
- i3 (escribir): `aceptadas` + 4 variantes (orden de los dos verbos; «une source de revenus»).

c47
- Diálogo, Ana (carta): «Enfin, les commerces de proximité disparaissent» → «Ensuite, …» (es «Por último» → «Luego», en «Finally» → «Next»). La carta anuncia dos argumentos; «enfin» sugería un tercero.
- g4 (ordenar): `aceptadas` + «Sur le surtourisme, je tiens à réagir à votre article.»
- i3 (escribir): `aceptadas` + variante con «il n’en reste pas moins… si utile que soit le tourisme».

c48
- Error frecuente 3, `correcto`: «une liberté ; je» → con U+202F antes de «;».
- g4 (ordenar): `aceptadas` + «J’exposerai mes arguments dans un premier temps.»
- e4 (ordenar): `aceptadas` + «Je montrerai d’une part les atouts ; d’autre part, les limites.»
- i3 (escribir): `aceptadas` + 2 variantes con «traite du surtourisme».

c49
- Pasaje de las memorias (diálogo[2]) y fila «il reverrait / il reviendrait» de la tabla del passé simple: «Il ne reviendrait que trente ans plus tard.» → «Il ne reviendrait jamais y vivre.» (es «No volvería nunca a vivir allí», en «He would never live there again»). Motivo: c08 (n7-b02) cuenta que Joseph vuelve al pueblo al año siguiente por la enfermedad de su padre, y c10 dice «il ne reviendrait jamais y vivre». «Treinta años» chocaba con las dos; con la nueva frase concuerda con c06 (nace en Lyon en 1905, la familia se instala en un pueblo, se va a París a los 18 en un mañana lluviosa de octubre de 1923), con c08 y con c10 (la casa se recompra en 1985 por su hija Jeanne, lo que ya no depende de él). Se mantiene «il ne reverrait pas sa mère de longtemps».
- Madame Dubois, primera réplica: «mon grand-père» → «mon grand-père Joseph» (y es/en), para enlazar con c06.
- «Para leer» pw2: 19 → 12 filas (se quitan la lecture, l’infinitif, la négation, revenir, tomber, raconter, littéraire); pw: 24 → 11 filas (se quitan coupable, la preuve, le camion, avoir lieu, le tarif, patient, échouer, s’entraîner, la raison, maintenir, talentueux, contester, le minibus). Eran palabras ya enseñadas y casi todas transparentes; quedan las que ayudan de verdad a leer el pasaje y las frases de repaso (le vol, la vraisemblance, le témoin, mentir, classer une affaire, démonter, la restauration, la pénalité, le détour, la nuance, piger, l’aube, le facteur, debout, le seuil, le regard, accompagner, il fallait que, exprimer, familier, pleurer, employer, le fond).
- e18 (completar «100»): `aceptadas` + «cent».

c50
- Una sola fecha de fundación del mercado/halle: c16 y c20 (n7-b04) dicen que la halle se construyó en 1868 y que el barrio se anexó a París en 1860; el mercado funciona en la halle. Todas las apariciones de «fondé en 1860» → «fondé en 1868» (explicación, error frecuente, tabla, ejemplos, g2, diálogo y sus traducciones: 16 cadenas). Se evita mencionar la anexión de 1860 para no abrir otro frente.
- «Créée en 1880, la place…» (fila de la tabla y e2) → «la bibliothèque» (traducciones y feedback incluidos): la plaza donde está la halle ya existía en 1868 (c16), así que «place créée en 1880» chocaba. «bibliothèque» ya está enseñada desde N1.
- Orden cronológico de la historia (diálogo, Ana) alineado con c20: tournant du siècle → años 1920 → lendemain de la guerre (en c20 la reconstrucción de después de la guerra viene tras los años 20). Antes ponía «lendemain de la guerre» antes de los años 20. En la tabla se intercambian esas dos filas.
- Debate local: «La mairie propose de rénover le marché» → «… la place du marché» (diálogo, fila de «rénover», contexto es/en). c16 y c20 dicen que la halle ya se renovó hace dos años; renovar «la plaza del mercado» enlaza además con el foro de N5 sobre la place du Marché.
- e5 (escuchar): la consigna no hacía la pregunta y las opciones «Deux. / Une. / Trois.» quedaban sin sentido. Ahora: «Escucha la frase y elige cuántas posturas resume.» (en: «Listen to the sentence and choose how many positions it sums up.»).

## Sin cambios (revisado y correcto)

- c46: la pista de cada ítem guiado ayuda a ese ítem; g5 y e4 con glosas distintas; el ordenar e5 admite un único orden natural; el resto del «Para leer» (16 filas) son ayudas reales con palabra, frase y sentido, sin celdas sueltas.
- c47–c50: opciones de comprensión en francés (punto 14); sin vocablo escondido en `vocabulario`; es neutro de América con tú («departamento», «alquiler» ya establecido en N2–N7); en americano.
- c50: Madame Lefort «habite l’immeuble depuis quarante ans»: N5 c36–c40 y N6 c20/c47 solo la presentan como vecina mayor de abajo, sin años; no hay contradicción. Madame Dubois «membre de l’association des habitants»: coherente con la regla canónica 12 (asociación de barrio) y con N7 c28 («J’habite le quartier depuis quarante ans»).

## Hechos del reparto confirmados

- Ana prepara el DELF B2 con Hugo (guía-conferenciante): él hace de examinador en la simulación oral (usted/vous solo durante la simulación; fuera de ella se tutean) / Ana prepares the DELF B2 with Hugo (a licensed tour guide): he plays the examiner in the oral simulation (vous only during the simulation; tu outside it) (c46, c48).
- Hugo encuentra un artículo de unas 300 palabras sobre el turismo urbano en París y Ana lo contrae a 71 palabras / Hugo finds an article of about 300 words on urban tourism in Paris and Ana contracts it to 71 words (c46).
- Ana escribe al correo de los lectores de la revista del barrio, reaccionando a un editorial sobre el surtourisme aparecido el 3 de marzo; en su calle varios departamentos se alquilan por semanas y la librería de su calle cerró el mes pasado / Ana writes to the neighborhood magazine’s letters page in response to an editorial on overtourism published on March 3; on her street several apartments are rented out by the week and the bookstore on her street closed last month (c47).
- El pasaje de las memorias de Joseph (abuelo de Madame Dubois, tercera persona y passé simple): el día en que deja el pueblo en tren bajo la lluvia, tras una carta esperada durante meses; su madre no lo acompaña a la estación; nunca volvería a vivir en el pueblo. Madame Dubois se lo da a leer a Ana (vous) en una prueba tipo DELF B2 / Joseph’s memoir passage (Madame Dubois’s grandfather, third person, passé simple): the day he leaves the village by train in the rain, after a letter awaited for months; his mother does not go with him to the station; he would never live in the village again. Madame Dubois has Ana read it (vous) in a DELF B2-style test (c49).
- El mercado del barrio funciona en la halle, construida en 1868; el barrio era un faubourg de jardines a principios del siglo XIX; la biblioteca del barrio se creó en 1880; hacia 1900 el barrio ya tenía más de cien tiendas; en los años veinte sus cafés acogían a artistas / The neighborhood market operates in the halle, built in 1868; the neighborhood was a faubourg of gardens at the beginning of the 19th century; the neighborhood library was created in 1880; around 1900 the neighborhood already had more than a hundred shops; in the 1920s its cafés welcomed artists (c50).
- Madame Lefort, la vecina de abajo, vive en el edificio desde hace cuarenta años, tiene la voz grave y los gestos lentos; tras una noche de música demasiado fuerte de Emma les ofreció un trozo de pastel / Madame Lefort, the downstairs neighbor, has lived in the building for forty years, has a deep voice and slow gestures; after a night when Emma played the music too loud she offered them a piece of cake (c50).
- Madame Dubois es miembro de la asociación de vecinos del barrio; la alcaldía propone renovar la place du marché; Hugo apoya el proyecto y Madame Dubois teme que se pierda el alma del mercado / Madame Dubois is a member of the neighborhood residents’ association; the city hall proposes renovating the market square; Hugo supports the project and Madame Dubois fears the market’s soul will be lost (c50).
- Ana escribe una crónica de unas 400 palabras («Chronique d’un quartier») para el número especial de la revista del barrio y la presenta en cinco minutos / Ana writes a column of about 400 words («Chronique d’un quartier») for the neighborhood magazine’s special issue and presents it in five minutes (c50).

## Sin resolver (fuera de este bloque)

- n7-b02, c08 vs c10: c08 sitúa la carta que dice que Joseph conoce a Marie en «l’hiver 1924… au printemps» y c10 dice «dix ans plus tôt» de 1935, es decir 1925; las dos fechas no concuerdan exactamente. No afecta a b10 (c49 no da esa fecha).
- c49 dice que Joseph esperó «cette lettre pendant des mois»; c06 cuenta que encontró trabajo ya en París. No hay contradicción mientras la carta no sea una oferta de trabajo (el pasaje no dice de qué carta se trata).
- Ninguna palabra francesa de b10 quitada o renombrada es usada por un bloque posterior de N7 (b10 es el último); las filas eliminadas de los «Para leer» de c46 y c49 eran de palabras que el validador da por enseñadas antes de b10 (en niveles anteriores o en n7-b01…b09). Si un borrador de N8 dependiera de alguna («la culture», «le camion», etc.), el validador de N8 lo avisará.
- c47 mantiene «Certes… Ensuite, les commerces…» en la carta: es aceptable, pero un autor de N8 no debe copiar el patrón.
