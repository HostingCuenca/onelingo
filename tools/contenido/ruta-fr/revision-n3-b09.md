# Revisión N3 · Bloque 9 (fr.n3.c41–c45)

GO

Revisor distinto del autor. Se leyeron las 5 fichas de `curriculo/fr/n3.json` (con su plan de `ejercicios`), la `nota` del nivel, `personajes` y `hechosDelReparto` de N1 y N2, `ENCARGO_RUTA_FR.md` (tabla N3 y calibración 1–10), `ESQUEMA_CONTENIDO.md` y los borradores `n3-b01`…`n3-b08`. Solo se editó `n3-b09.json`.

Validación final:
- `python3 tools/validar_ruta.py fr --borrador n3-b01 … n3-b09` → **0 errores** (con n3-b07 incluido; no hizo falta excluirlo).
- `python3 tools/curriculo/validar_plan.py fr` → 0 errores y ningún «título de la unidad difiere» para fr.n3.c41–c45 (solo los 10 avisos antiguos de N1).

Comprobaciones que pasaron sin cambios:
- Título y objetivo de cada unidad iguales a los de la ficha; las 10 palabras de `vocabulario` de cada ficha están en el paso de vocabulario; ids, `orden` 341–345, prerrequisitos en cadena (c41 → c40), `erroresFrecuentes` 3 por clase.
- Cada clase contiene los ejercicios del plan (5 guiados, 3 independientes, 2 de comprensión, 6 de evaluación) con el mismo formato y sobre la misma clave; la evaluación tiene 5 ítems puntuables y 3–5 formatos, y el ítem abierto (`abierta: true`) va aparte en las cinco clases.
- Situaciones: 165 / 161 / 170 / 172 / 163 palabras (rango N3: 150–250), hablantes con nombre o papel en francés («Le journaliste», Hugo, Ana, Léa), preguntas de comprensión con una sola respuesta defendible según el texto.
- Tipografía francesa: U+202F antes de ? ! : ; (112 casos, ningún espacio normal ni NBSP), apóstrofo ’, sin apóstrofos rectos.
- Español neutro (suspenso, policíaco, departamento…) e inglés americano (movie, binge); sin «piso», «móvil», «billete», etc.
- Guías de pronunciación según calibración 6 (j/g = «sh», nasales = «en»/«an», ü/ö definidas en c41 y repetidas), con la excepción explicada de «jazz» = «dyaz».
- `aceptadas` completas en ordenar (órdenes naturales con fuente al inicio o al final) y en escribir (selon / d’après, pasiva y presente, sûr / sûre, pense / crois, œ→oe lo normaliza el corrector).

## Correcciones aplicadas (clase, ítem, antes → después)

fr.n3.c41
- Explicación 2 (es/en): «(a / ont été = pasado compuesto de être; …)» → «(ont été = pasado compuesto de être: ont + été; …)», sin la forma suelta «a».
- Explicación 3 (es/en): «la clase 43 la explica; ahora quédate con la frase» → remite a la clase 21 (donde ya se enseñó à cause de) y a la 43 solo para el detalle.
- Tabla «La pasiva: ahora y antes», fila 3: «Con quién lo hizo» / «With who did it» → «Quién lo hizo (par)» / «Who did it (par)».
- g1 (pista): «Hay dos formas de decir «según»; vale cualquiera de las dos» → pista que orienta a ese ítem (la fuente va primero; selon o d’après).
- Situación, 5.ª línea y s2 (feedback): «Le festival aura lieu samedi prochain…» → «Les organisateurs disent que le festival aura lieu samedi prochain…» (es/en igual). Así el texto recicla el discurso indirecto, que la ficha lista en `recicla` y no aparecía.

fr.n3.c42
- Explicación 1 (es/en): «subjuntivo irregular (clases 26–27)» → «subjuntivo (clases 26–27)» (c26 es el regular, c27 el irregular).
- Situación, 4.ª línea (fr/es/en): «samedi soir / el sábado por la noche / Saturday night» → «dimanche soir / el domingo por la noche / Sunday night», para no chocar con la fiesta del sábado de c44 (playlist de Léa y Hugo) ni con el festival de c41.

fr.n3.c43
- g2 (pista): «La palabra que falta es el sustantivo de la expresión» → ««A causa de» se dice À ___ de: la palabra que falta se parece mucho a «causa»» (es/en).
- Situación, línea de Hugo: «Non, les acteurs sont très bons. C’est grâce à eux…» → «Non, ce que j’aime, ce sont les acteurs. C’est grâce à eux…» (es/en igual): recicla ce-qui-ce-que, que la ficha lista y no se usaba.
- g4 e i2 (consigna es): «suspense» → «suspenso», coherente con el resto de la clase y español de América.
- e5 (`aceptadas`): se añaden «À cause de la grève, je n’ai pas regardé l’épisode.» y «Je n’ai pas regardé l’épisode à cause de la grève.» (regarder es una traducción natural de «no vi»).

fr.n3.c44
- g1 (pista): «La expresión empieza por par: «par ___»» (regalaba la respuesta) → «Es el conector de la lengua oral para «en cambio» (cependant se usa más al escribir)» (es/en).

fr.n3.c45
- i1 (opción 1 y feedback, es): «Duda de la rumor» → «Duda del rumor» (concordancia: el rumor).

Ninguna palabra francesa enseñada se eliminó ni se renombró; no hay efecto en bloques posteriores. Las palabras añadidas en situaciones (disent, dimanche, ce sont) ya estaban enseñadas y el validador las acepta.

## Hechos del reparto confirmados

- Ana lee en el periódico del barrio que el festival del barrio fue cancelado ayer por la lluvia (se esperaban 300 personas en el parque) y que se repetirá el próximo sábado, en el mismo parque; luego se lo resume a Emma (c41) / Ana reads in the local paper that the neighborhood festival was canceled yesterday because of the rain (300 people were expected at the park) and will be held next Saturday in the same park; she later sums it up for Emma (c41)
- Hugo vio anoche un thriller en versión original con subtítulos (dura dos horas), se lo cuenta a Léa por mensaje y le propone verlo juntos el domingo por la noche (c42) / Hugo watched a thriller in the original version with subtitles last night (two hours long), tells Léa about it in a message and suggests watching it together Sunday night (c42)
- Ana ve una serie policíaca en una plataforma por consejo de Léa y ve tres episodios por noche; Hugo vio la temporada uno, le decepcionó el final porque un amigo le contó el desenlace (spoiler), y empieza la temporada dos esa noche por consejo de Ana (c43) / Ana watches a crime series on a streaming platform on Léa’s advice, three episodes a night; Hugo saw season one, was disappointed by the ending because a friend spoiled it, and starts season two that night on Ana’s advice (c43)
- Léa y Hugo preparan la playlist de la fiesta del sábado: a Léa le gusta el rap por las letras, Hugo prefiere el jazz (lo escucha todas las mañanas en vez de la radio), le gusta el rock pero nunca escucha metal; acuerdan mezclar rap y jazz (c44) / Léa and Hugo put together the playlist for Saturday’s party: Léa likes rap for the lyrics, Hugo prefers jazz (he listens to it every morning instead of the radio), likes rock but never listens to metal; they agree to mix rap and jazz (c44)
- Ana y Hugo clasifican las frases de un artículo sobre un cantante sin nombre (disco en 2024 y premio = hechos; separación del grupo y gira = rumores; letras «las mejores de su generación» = opinión; otro periódico, fuente no fiable, dice que está enfermo) (c45) / Ana and Hugo sort the sentences of an article about an unnamed singer (2024 album and prize = facts; leaving the band and a tour = rumors; lyrics “the best of his generation” = opinion; another paper, an unreliable source, says he is sick) (c45)

Coherencia con N1, N2 y N3 b01–b08: Hugo y Léa se tutean entre sí y con Ana; Ana es «sûre / contente» (femenino), Hugo «déçu»; la fiesta del sábado es la misma costumbre de Léa de N2 c16; ningún hecho contradice la `nota` del nivel ni `hechosDelReparto`.

## Sin resolver / observaciones

- Desvío menor respecto al plan de c45: la ficha dice que el rumor es «prepara un nuevo disco»; el borrador usa el rumor de la gira (tournée, vocabulario declarado) y hace que los fans estén «sûrs» de que prepara un nuevo disco. Es coherente dentro de la clase y con s1/s2, así que se deja.
- Las situaciones tienen pocas líneas largas (c41, c42, c45) o muchas cortas (c43, c44); en todas el total (161–172 palabras) cumple el rango N3 de 150–250.
