# Revisión de N8 · B3 (fr.n8.c11–c15)

GO

Revisado: `tools/contenido/ruta-fr/n8-b03.json` (c11 anáfora y ritmo ternario, c12 anglicismos, c13 ethos/pathos/logos, c14 argumento de venta, c15 «il nous appartient de»). Autor distinto del revisor. Se contrastó con las 5 fichas de `curriculo/fr/n8.json` (incl. `ejercicios`), la `nota` del nivel, `personajes` / `hechosDelReparto` de N1–N8, `ENCARGO_RUTA_FR.md` (Por nivel N8 y Calibración 1–15) y `ESQUEMA_CONTENIDO.md`. Cada clase enseña exactamente lo que dice su ficha, contiene todos los ejercicios planificados (mismo formato y clave; redacción pulida) y nada de clases posteriores.

## Validación

- `python3 tools/validar_ruta.py fr --borrador n8-b01.json n8-b02.json n8-b03.json` → 0 errores (n7-b01…b10 ya están integrados en `assets/contenido/fr/ruta/`, por eso se quitaron de la lista).
- `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún aviso «título de la unidad difiere» para fr.n8.c11–c15.
- Cadena completa n8-b01…b10: los errores que aparecen son de otros bloques (c25, c49, c50…). Ninguna palabra que quité de este bloque la usa un bloque posterior.

## Correcciones

### c14 (reparto)
1. **Situación / diálogo / contexto — coherencia del reparto.** Hugo ya no es vendedor de una tienda (era demasiada actividad: máster, guía, radio/pódcast, entrenador). Ahora **Hugo acompaña a Madame Dubois** a ayudarla a elegir el robot aspiradora y el **vendedor es «Le vendeur», sin nombre**; «La responsable» felicita al vendedor (tutoiement entre colegas, «Bravo. Tu as suivi les cinq étapes…»). Se mantuvo íntegro el contenido de venta (5 pasos, «Et si vous pouviez…», «Que vous soyez… ou…», dos objeciones, «Je vais réfléchir», código promo, garantía). Hugo tiene dos líneas breves (llegada y «Moi, je la prendrais»). Se quitó «Dites à Ana que je viendrai dimanche…» y «Vous êtes très convaincant, Hugo». Contexto es/en reescrito.
2. **Diálogo — orden lógico.** Antes la respuesta a «Je vais réfléchir» llegaba tras una pregunta sobre la entrega y daba dos «Bien sûr» seguidos. Ahora: «Je vais réfléchir» → «Bien sûr, mais n’oubliez pas que l’offre se termine ce soir…» → entrega → decisión. Se eliminó «La réparation est gratuite, pièces et transport compris» (redundante).
3. **s2** — «Hugo responde» → «El vendedor responde» (consigna, feedback, preguntaApoyo).
4. **e1 (ordenar) y e2 (relacionar)** — «Vous dormez tranquille» → «Vous dormiriez tranquille», para que los *bénéfices* vayan en condicional como enseña la explicación y la tabla (la forma ya estaba en `ejemplos`).
5. **e6 (escuchar)** — la opción 3 («Si vous dormiez tranquille.») también es imparfait, así que la consigna «elige la frase que sugiere con imparfait» tenía dos respuestas defendibles. Opción 3 → «Et si vous dormiriez tranquille ?» (error típico con condicional) y consigna «elige la frase correcta…».
6. **i3 (elegir)** — «Aujourd’hui seulement : moins vingt pour cent !» podía ser accroche o appel à l’action. → «Aujourd’hui seulement, ajoutez la garantie : moins vingt pour cent !» (imperativo = appel à l’action sin ambigüedad).
7. **g5 (escribir)** — la pista daba toda la respuesta; ahora orienta («ne plus jamais» = nunca más; «se soucier de» = preocuparse de; mira los ejemplos).

### c11
8. **s1 (elegir)** — la pregunta y el feedback citaban «chauds, légers, durables» (plural) pero el diálogo dice «chaud, léger, durable» → singular.
9. **Diálogo — figuras mezcladas.** El segundo anuncio mezclaba «marchez» (vous) con «Pour toi, pour nous, pour demain» (tu), y esa misma secuencia se llamaba «parallélisme» en el diálogo y «anaphore» en i1. → «Bon pour vous, bon pour la planète : marchez mieux, marchez plus loin !» y la periodista comenta «Le parallélisme “Bon pour vous, bon pour la planète”» (coincide con e2). Traducciones es/en actualizadas.
10. **Diálogo (Ana)** — «la première marque ne se contente pas d’être directe» no se entendía tras «Moi aussi» → «la première est moins directe : on ne remarque pas la répétition, on sent seulement le rythme».

### c12
11. **Contexto es/en** — decía «ficha de unas 150 palabras» pero la ficha del diálogo tiene unas 90 → «la ficha de producto de unas zapatillas».
12. **Vocabulario `placement de produit`** — es «colocación de producto» vs. ejemplo «emplazamiento de producto» → «emplazamiento de producto (product placement)» en ambos.
13. **Tabla «Para leer…»** — se quitó la fila «naturel» (no aparecía en ningún texto ni ejercicio: relleno). Quedan 9 filas.
14. **Léa y su pasantía** — compatible con N2–N7 (estudiante universitaria, 20 años; «stage» ya existe en el reparto; no se contradice con ningún hecho). Se deja.

### c13
15. **Nota de pronunciación de `l’égérie`** — «lé-she-rí» → «lé-shé-rí» (la segunda vocal es é); en inglés «PRÖV» en vez de «prövv» en `la preuve sociale`.
16. **Ejemplo es de «Deux fois moins cher qu’avant»** — «Dos veces más barato» (impreciso) → «A la mitad del precio de antes».
17. **g3 (completar)** — «L’annonce ___ sur l’argument d’autorité» admite también «joue» (la propia tabla de la clase) → `aceptadas: ["joue"]`.

### c15
18. **Diálogo (Léa)** — «dont dix seulement que je porte» era agramatical → «et je n’en porte que dix»; «Je ne dis pas que tout est de notre faute» → «…que tout soit de notre faute» (subjuntivo tras negación; ya coincidía con la traducción «sea culpa nuestra»); «vous savez que c’est possible» (sin conexión) → «vous pouvez agir dès demain». Traducciones es/en ajustadas.
19. **Explicación p1 (es)** — «… tenemos que) e il est de notre devoir de» → «y».
20. **Traducción en de «Que chacun prenne ses responsabilités !»** — «take their responsibilities» → «take responsibility» (ejemplo y diálogo).

### Todo el bloque
21. **Posición de la respuesta correcta.** En `elegir`/`escuchar`, las 42 respuestas estaban en la opción 0 (en bloques anteriores se redistribuyó). Reparto final 14 / 14 / 14 en posiciones 0 / 1 / 2 (solo se reordenaron opciones; `respuesta` actualizada).
22. **Fichas de `ordenar`** (c14 g1, c14 e1, c15 g3, c15 e5): `tokens` en el orden de la respuesta, como espera `item_view.dart` (que las desordena él mismo).
23. **Tipografía.** Se normalizaron a U+202F los espacios delante de `? ! : ;` y dentro de « » en las líneas nuevas del diálogo de c14 e i3. Escaneo final: 0 incidencias en todos los campos en francés. Nota: el título de c12 («Le feedback ou le retour ? Anglicismos…») lleva espacio normal antes de `?` porque el plan lo escribe así y `validar_plan` compara el texto exacto; si se quiere U+202F hay que cambiarlo a la vez en `curriculo/fr/n8.json`.

## Comprobaciones sin cambios
- **Situación (400–700 palabras en el diálogo):** c11 454, c12 473, c13 433, c14 424, c15 433; las preguntas de comprensión coinciden con el texto (una sola respuesta cada una).
- **Evaluación:** cada clase tiene 5–6 ítems puntuables en 4–5 formatos; los `escribir` abiertos (c11 e6, c13 e5, c14 e5, c15 e6) no puntúan y se suman aparte; los modelos cumplen `minimoPalabras`.
- **Tablas «Para leer…»:** c11 3, c12 9, c13 8, c14 4, c15 8 filas (≤ 15), todas con la palabra en uso.
- **Anatomía:** explicación → ejemplos → vocabulario (8 palabras de la ficha, con artículo) → tablas → guiada con pista → independiente → situación → evaluación. `erroresFrecuentes` = 3 por clase.
- **Pronunciación (guías es/en):** j/g suave = «sh»/«zh», nasales «en/an/on», ü y ö definidas la primera vez (ü en c11, ö en c13); consonantes finales correctas (retour, court, achat, client, vente).
- **Español neutro / inglés americano:** estacionamiento, tintorería, armario/closet, ustedes; sin peninsularismos.
- **Hablantes:** nombres o papeles franceses (Le vendeur, La responsable, La journaliste, La directrice du marketing, Le journaliste). Las etiquetas de documento («L’annonce», «La fiche produit», «Le courriel de Léa») siguen la práctica de N6–N8.
- **Ambigüedad conceptual aceptada (viene de la ficha):** «Plus de style, plus de confort, plus de plaisir» es gradation (explicada así en p2) aunque también repite «plus de»; no hay ninguna opción con «anaphore» en esos ítems.

## Hechos del reparto confirmados
- Ana espera una cita con Monsieur Martin en la escuela; Chloé (secretaria) y Ana se tratan de vous / Ana waits for an appointment with Monsieur Martin at the school; Chloé (the secretary) and Ana use vous (c11)
- Ana prepara un eslogan de tres frases (c11) y un análisis de 200 palabras (c13) para su preparación del DALF C1 / Ana prepares a three-sentence slogan (c11) and a 200-word analysis (c13) as part of her DALF C1 prep
- Léa, estudiante universitaria de 20 años, hace unas prácticas (stage) en una marca de calzado deportivo y pide ayuda a Ana (se tutean) con una ficha de producto (c12) / Léa, a 20-year-old university student, does an internship at a sports-footwear brand and asks Ana (they use tu) for help with a product sheet (c12)
- Léa es delegada de una asociación estudiantil y da un discurso contra la moda rápida en una plaza de París ante unas cien personas; tiene unas 40 prendas y solo usa 10; convoca un intercambio de ropa el sábado (c15) / Léa is a student-association delegate and gives a speech against fast fashion in a Paris square to about a hundred people; she owns about 40 garments and wears only 10; she calls a clothing swap for Saturday (c15)
- Hugo, guía-conferenciante, usa recursos persuasivos en sus visitas guiadas (c13) y llevará tres chaquetas al intercambio de ropa de Léa (c15) / Hugo, a tour guide, uses persuasion devices in his guided visits (c13) and will bring three jackets to Léa’s clothing swap (c15)
- Hugo **no** trabaja de vendedor: acompaña a Madame Dubois a una tienda de electrodomésticos y la ayuda a elegir (c14); se tratan de vous / Hugo is **not** a salesperson: he goes with Madame Dubois to an appliance store to help her choose (c14); they use vous
- Madame Dubois (antigua casera, vive cerca) compra un robot aspiradora y añade la garantía extendida (40 € más; 10 % menos con código promo); su aspiradora vieja funciona desde hace veinte años; entrega el sábado (c14) / Madame Dubois (Ana’s former landlady, lives nearby) buys a robot vacuum and adds the extended warranty (40 euros more; 10 percent off with a promo code); her old vacuum has worked for twenty years; delivery on Saturday (c14)
- El vendedor y la responsable de la tienda no tienen nombre (c14) / The salesperson and the store manager are unnamed (c14)

## Sin resolver
- Nada bloqueante. El título de c12 conserva el espacio normal antes de «?» para coincidir con el plan (ver punto 23).
- Para el integrador: `curso.json` aún no lista `fr.n8-b03` (se añade al integrar).
