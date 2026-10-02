# Revisión N6 · B1 (fr.n6.c01–c05)

GO

Bloque revisado por un agente distinto del autor, contra sus 5 fichas de `curriculo/fr/n6.json` (incl. plan de ejercicios), la `nota` del nivel, el reparto de N1–N4, `ENCARGO_RUTA_FR.md` (Por nivel N6 y Calibración 1–11) y `ESQUEMA_CONTENIDO.md`.

Validación (con `n5-b01…n5-b10` y `n6-b01` como borradores): `python3 tools/validar_ruta.py fr --borrador …` → **0 errores**. `python3 tools/curriculo/validar_plan.py fr` → 0 errores, sin «título de la unidad difiere» para fr.n6.c01–c05.

Contraste con las fichas: títulos, objetivos, gramática, `introduce`/`recicla`, tareas y situaciones coinciden; los ejercicios del plan están todos (mismo formato y misma clave, orden idéntico en guiada, independiente, preguntas de situación y evaluación). Nada de clases posteriores. Situaciones de 321–357 palabras (rango N5–N7: 300–500). Cada evaluación tiene 5 ítems puntuables en 4–5 formatos más 1 `escribir` abierto (`abierta: true`) que no cuenta. Hablantes: nombres o papeles en francés. Tipografía (U+202F, ’) correcta en todo el bloque. Vocabulario estricto: todo lo que aparece en situaciones e ítems se muestra en tarjetas, ejemplos o tablas (validador en modo estricto, 0 errores). Sin regionalismos de España ni británicos.

## Correcciones aplicadas (clase, ítem: antes → después)

### fr.n6.c01
- Errores frecuentes nº 3: «Je trouve que c’est injuste que les pères n’ont pas de congé.» → «Je trouve injuste que les pères n’ont pas de congé.» (correcto: «…n’aient pas de congé.»). La forma «je trouve que c’est injuste que + subjuntivo» es francés correcto; el error real era el indicativo. Explicación es/en reescrita («Tras je trouve + adjetivo + que va el subjuntivo: n’aient, no n’ont»).
- Explicación p2: «sin “c’est”… no je trouve que c’est injuste que…» (afirmaba que esa forma era incorrecta) → la forma corta es la que se practica; «je trouve que c’est injuste que…» se menciona como variante más pesada que también lleva subjuntivo (es/en). Coherente con las `aceptadas` de i4, que ya la admitían.
- i4 (escribir, traducción): añadidas `aceptadas` con «des enfants» y las variantes «ça» / «que c’est» (antes solo «de leurs enfants»).

### fr.n6.c02
- Explicación p1: la glosa «mis padres eran tan estrictos como permisivo soy yo» (español forzado) → «tan estrictos como eran mis padres, tan permisivo soy yo»; EN: “As strict as my parents were, that is how permissive I am”.
- Vocabulario `v-baby-boomers`, nota de sonido: «casi como en inglés» / “Said almost as in English” (inexacto: en francés se dice «bé-bi-bu-mör») → «bé-bi-bu-mör» (ö, r final sí suena) / “bay-bee-boo-MUHR”.
- Ejemplo «Autant tu lisais le journal…», traducción EN: contenía una frase ajena («For me, work is important…») → “You used to read the newspaper as much as I read social media.”
- Diálogo (réplica 5 de Hugo), traducción EN: faltaba la última frase y el tiempo era erróneo → completa («…you used to read…» + «For me, work is important, but not at any price: I also want free time.»).
- e4 (ordenar): token compuesto «À l’instar» → dos tokens «À», «l’instar»; `aceptadas` ampliadas con «Hugo, à l’instar de son père, est très sérieux.» (además de la ya existente con la locución al final).
- e5 (relacionar): consigna «con el vocabulario generacional que mejor lo describe» → «con su descripción» (es/en).

### fr.n6.c03
- Reparto: la ficha dice que Chloé conoció a su marido hace **seis** años y lleva **cinco** casada (igual que N1). El autor lo había cambiado a diez/nueve. Restituido en contexto (es/en) y en el diálogo (réplicas 2, 10 y 12: «il y a six ans», «Au bout de six ans», «Depuis cinq ans») con sus traducciones. Ver «Sin resolver».
- Contexto: «Se tratan de vous.» → «Ana y Chloé se tratan de vous.» (línea de reparto corregida; es/en).
- g3 y e4 (ordenar): token compuesto «À peine» → «À», «peine».
- Tabla p3, etiqueta de fila «yo (ella)» → «yo (mujer)».
- Vocabulario: «beau-père» aparecía en la tabla y en el diálogo sin glosa en ningún sitio → nueva tarjeta `v-beau-pere` («le beau-père / la belle-mère», con nota de sonido), añadida a los `refs` del paso de vocabulario (la clase queda en 11 palabras).

### fr.n6.c04
- Tabla p4, fila «non seulement… mais encore»: «…mais il est encore rentable» (encore = «todavía») → «Non seulement il est utile, mais encore il est rentable.»
- g3 (ordenar): token compuesto «Non seulement» → «Non», «seulement».
- g2 (pista): «Se repite la palabra que abre la segunda opción» (vaga) → pista concreta que remite a «soit on accepte la situation».
- g4 (completar, ne… ni… ni): el hueco cubría «ni le temps ni l’argent» (varias respuestas defendibles: «ni temps ni argent», orden invertido) → «Il n’a ___ le temps ni l’argent pour une garde d’enfants.» → «ni» (una sola respuesta; pista y feedback ajustados). Mismo formato y clave del plan.
- e5 (completar, ne… ni… ni): «Elle n’a ___ vélo» con respuesta «ni voiture ni» (la palabra «voiture» no se deduce: indefendible) → «Elle n’a ___ voiture ni vélo, donc elle prend le métro.» → «ni».
- i2 (escribir, traducción): añadida `aceptada` con «salariés».
- Ejemplo «J’ai la conviction que…»: traducción ES «Estoy convencido de que…» → «Tengo la convicción de que…» (muestra el vocablo de la clase).
- Ejemplo «Vous essayez de me persuader, mais ce n’est pas de la mauvaise foi.» (sentido forzado) → «…mais je n’aime pas la mauvaise foi.» (es/en); sigue enseñando «essayez» y «mauvaise foi», que el diálogo usa.
- Diálogo (réplica de Ana): «Ni les parents ni les jeunes ne veulent plus…» (ni… ni con sujeto, estructura no enseñada) → «Les parents et les jeunes ne veulent plus des horaires impossibles.» (es/en).

### fr.n6.c05
- e5 (ordenar): añadido el orden natural «Il s’avère que depuis dix ans la natalité baisse.» a `aceptadas`.
- i4 (escribir, traducción): `aceptadas` ampliadas con «habitent seules» (y «les personnes âgées»).

## Hechos del reparto confirmados

- Ana y Chloé se tratan de vous; Ana también trata de vous a la moderadora (c01) y al director del hotel (c04); Ana y Hugo se tutean, y Hugo y su abuela de Lyon se tutean. / Ana and Chloé use vous with each other; Ana also uses vous with the moderator (c01) and the hotel director (c04); Ana and Hugo use tu, and Hugo and his Lyon grandmother use tu.
- Hugo y Ana asisten a un debate de tarde en la mairie del distrito sobre los nuevos modelos de familia (moderadora y tres vecinos); Ana defiende el congé parental compartido; Hugo cuenta que su abuela era profesora en París cuando los padres no tomaban licencia (coherente con N2: en París desde 1972, profesora desde 1975). / Hugo and Ana attend an evening debate at the district town hall (mairie) on new family models (a moderator and three neighbors); Ana defends shared parental leave; Hugo says his grandmother was a teacher in Paris at a time when fathers took no leave (consistent with N2: in Paris from 1972, teaching from 1975).
- Hugo prepara una exposición de su maestría sobre la brecha generacional y llama por video a su abuela de Lyon (nacida en 1950, baby-boomer, profesora durante cuarenta años, 1975–2015): su padre era estricto y su madre tierna, ella transmitió a sus hijos el gusto por los libros, y Hugo, como su abuelo, ama leer; Hugo y su abuela se llaman los domingos. / Hugo prepares a master’s presentation on the generation gap and video-calls his Lyon grandmother (born 1950, a baby boomer, a teacher for forty years, 1975–2015): her father was strict and her mother tender, she passed on a love of books to her children, and Hugo, like his grandfather, loves to read; Hugo and his grandmother call each other on Sundays.
- Chloé conoció a su esposo Antoine hace seis años en la fiesta de una amiga (hablaron tres horas en el balcón) y lleva cinco años casada; a los tres meses se mudaron juntos, rompieron brevemente en una misma semana y volvieron; en la primera cena con los suegros su suegro había preparado todo desde la mañana; la petición de matrimonio la interrumpió una llamada de la madre de Antoine; cada año vuelven a la fiesta de esa amiga. / Chloé met her husband Antoine six years ago at a friend’s party (they talked for three hours on the balcony) and has been married for five years; after three months they moved in together, broke up briefly within a single week and got back together; at the first dinner with his parents, her father-in-law had prepared everything since morning; the marriage proposal was interrupted by a call from Antoine’s mother; every year they go back to that friend’s party.
- Ana coordina un pequeño equipo en el hotel y defiende ante el director los horarios flexibles: un colega de su equipo ya teletrabaja un día por semana y no llega tarde; dos colegas tienen otras ofertas; propone una prueba de tres meses en su equipo y el director espera su propuesta escrita el lunes. / Ana coordinates a small team at the hotel and argues for flexible schedules before the director: a colleague on her team already works from home one day a week and is no longer late; two colleagues have other offers; she proposes a three-month trial in her team and the director expects her written proposal on Monday.
- Hugo lee con Ana un artículo de prensa (cita al INSEE) para su maestría; Ana cuenta que en su equipo del hotel algunas madres llegan cansadas y que en Quito tres generaciones suelen vivir en la misma casa. / Hugo reads a press article (citing the INSEE) with Ana for his master’s; Ana says that some mothers on her hotel team arrive tired and that in Quito three generations often live in the same house.

## Sin resolver / notas para el coordinador

- **Cronología de Chloé (c03).** Se restituyó «hace seis años / cinco casada» porque lo fija la ficha de c03 (y N1). Pero N6 ocurre varios años después de N1 (Ana lleva ≥ 3 años en París en N4); si se quiere cronología estricta, habría que subir ambas cifras en la ficha y en este diálogo (el autor había puesto diez y nueve, igual a «+4 años»). No afecta a ningún ítem de comprensión; es un cambio de seis cifras en un solo diálogo (réplicas 2, 10 y 12 y el contexto).
- Palabras añadidas por el autor fuera de las 8–10 de la ficha (necesarias para la gramática y justificadas): c01 `la loi`, `l’employeur`, `protéger`, `reconnaître` (13 tarjetas, una más que el tope de 12 del encargo); c02 `la stabilité`; c03 `le beau-père / la belle-mère` (añadida en esta revisión); c04 `la thèse`, `concilier travail et famille`; c05 `les personnes âgées`, `l’INSEE`.
- c05: la ficha pide un artículo de unas 400 palabras; el texto de la situación (artículo + comentarios) suma 341, dentro del rango N5–N7 (300–500), con el artículo en la mitad aproximadamente. No se amplió para no desbalancear los dos ítems de comprensión.
- c05: el hablante «L’article» es un texto, no una persona; sigue siendo francés y se muestra igual en es/en, por lo que se deja.
- No se eliminó ni renombró ninguna palabra francesa de vocabulario que bloques posteriores de N6 puedan usar (solo se quitó la construcción «ni… ni» con sujeto del diálogo de c04 y se reescribió un ejemplo de c04 que conserva «essayer», «persuader» y «mauvaise foi»).
- Chloé en N6 (≈2030): conoció a Antoine hace diez años y lleva nueve casada (N1, 2026: seis y cinco). Coordinación ajustó c03.
