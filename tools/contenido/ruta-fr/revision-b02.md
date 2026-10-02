# Revisión independiente · N1 francés, bloque 2 (clases 6–10)

- **Archivo:** `tools/contenido/ruta-fr/n1-b02.json` (`fr.n1.c06` … `fr.n1.c10`)
- **Revisor:** IA independiente (no autora), perfil profesor A1 de francés de Francia, con español latinoamericano e inglés americano.
- **Fecha:** 2026-10-01
- **Validador:** `python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n1-b01.json tools/contenido/ruta-fr/n1-b02.json` → **0 errores**.
- **Comprobaciones propias adicionales:** (a) «nada sin enseñar» con criterio estricto (solo cuentan `ejemplos`, `vocabulario` con refs, `patron` y `tabla`, paso por paso; el validador acepta también todo el vocabulario declarado): 0 palabras sin enseñar en B2 (solo el distractor «Me aime» de c09, que es el error enseñado); (b) tipografía: 0 apóstrofos rectos y 0 signos sin U+202F en campos en francés ni en las citas de los textos de apoyo.

## Veredicto

GO

Es un bloque bien construido: tablas completas de parler, habiter, aimer, travailler y étudier con las 9 personas, columna de pronunciación, explicaciones bilingües cortas, sonido del día correcto en las 5 clases y diálogos naturales. Los problemas eran de coherencia de personajes con B1, una regla geográfica incompleta, pistas genéricas, ítems con más de una respuesta defendible y varias glosas de `relacionar` casi iguales. Todo está corregido en el archivo.

## Recuentos

| Clase | Concepto | Vocablos | Errores frecuentes | Ítems | Reciclaje en ejemplos (palabras de clases/f0 previas) |
|---|---|---|---|---|---|
| c06 | pronombres | 9 | 3 | 16 | 84 % |
| c07 | presente-er | 9 | 3 | 15 | 76 % |
| c08 | vivienda | 10 | 3 | 16 | 57 % |
| c09 | gustos | 10 | 3 | 17 | 46 % |
| c10 | trabajo | 10 | 3 | 16 | 55 % |

- **Ítems por formato (B2, 80):** completar 21 · elegir 18 · escuchar 12 · ordenar 10 · escribir 10 · relacionar 9.

Anatomía de cada clase: explicación (sonido del día + gramática), ejemplos (5–8), vocabulario (9–10, con artículo en los sustantivos), tabla/patrón, guiada (4–5), independiente (4), situación (5–6 líneas + 1–2 ítems de comprensión) y evaluación (5–6 ítems, 5–6 formatos). Los 6 formatos se usan a lo largo del bloque.

## Correcciones aplicadas (clase · ítem · antes → después)

### c06 · pronombres
1. **Situación (personajes, contradice B1).** Léa era «canadienne»; en B1 c05 es «française» de París. «C’est Léa. Elle est canadienne. Hugo et Léa sont amis.» → «C’est Léa. Elle est française. Hugo et Léa, ils sont amis.» (así el diálogo modela además «ils»). s1: respuesta correcta pasa de «De Canadá» a «De Francia» (índice 1 → 0) y feedback; s2: «___ est canadienne» → «___ est française».
2. **Vocabulario «eux» (ö sin definir).** «Suena «ö», como en «deux»» → «Suena como la «eu» de «deux» («ö»: di «e» con los labios redondeados)» (y en inglés). Así «ö» queda definido la primera vez que se usa en B2 (reaparece como «lö» en c09).
3. **g3 (pista).** «Mira la tabla de pronombres.» → «Lui y eux son las formas con énfasis de il e ils.» (ayuda a resolver ese relacionar).
4. **g1 y e3 (consigna).** «Elige el pronombre.» → «Elige el pronombre sujeto.» (en e3 «eux» es un distractor que podría defenderse como «pronombre»).
5. **i1 ordenar.** `aceptadas` + «Je suis de Quito, moi.»; consigna «Ordena con énfasis: «Yo soy de Quito», usando moi.»
6. **e4 ordenar.** `aceptadas` + «Le garçon, c’est lui.»
7. **e5 escribir.** `aceptadas` + «Nous, on est de Quito.»

### c07 · parler
1. **Explicación (en).** «In writing the endings change more than in English (I speak, he speaks)…» (comparación confusa) → «In English only he / she / it changes (I speak, you speak, he speaks); in French almost every person has its own ending in writing, but out loud four forms are identical…». Es y en: «el idioma va sin artículo» → «normalmente va sin artículo» (también se oye «parler le français»).
2. **Situación (personajes).** Lucas es canadiense en B1 y aquí decía «un peu» de francés y hablaba español e inglés, lo cual no encaja. Ahora es Ana (ecuatoriana) quien habla con Emma, en un intercambio «en línea» (antes «en París», lo que ponía a Ana de visita). Emma, estadounidense en B1, ahora dice «Moi, je parle anglais, français et italien.» (antes omitía el inglés, su lengua materna). s1: opción correcta «Francés e italiano» → «Inglés, francés e italiano»; feedback adaptado.
3. **g3 (pista).** «Allemand = alemán.» → «Fíjate en «allemand» (alemán) y en el pronombre vous.» (la opción «Hablamos alemán» se descarta por «vous»).
4. **g4 (pista).** «Mira las tarjetas de vocabulario.» → «Busca el parecido: italien → italiano, portugais → portugués.»
5. **i3 escribir.** `aceptadas` + «Je parle espagnol et un peu de français.» (la forma más natural en francés).
6. **e4 ordenar.** `aceptadas` + «Elles parlent anglais et français.»

### c08 · habiter
1. **Regla de países incompleta (error de contenido).** Explicación (es/en): «en + país femenino (…, en Équateur)». L’Équateur es masculino: lleva «en» porque empieza por vocal. → «en + país femenino o que empieza por vocal (en France, en Espagne, en Colombie, en Équateur)». Mismo ajuste en el `texto` de la tabla de países y en el tercer error frecuente («En es para los femeninos (en France) y para los que empiezan por vocal (en Équateur)»).
2. **Situación (personajes).** Chloé aparecía como «profesora» que vive «au Canada, dans un village»; en B1 Chloé es la secretaria de la escuela y en c06 es de París; el canadiense de B1 es Lucas. → Videollamada entre amigos: Lucas (canadiense) pregunta a Ana: «Salut, Ana ! Tu habites où ?» (añade el saludo), y es él quien vive «au Canada, dans un village». s1 y su feedback actualizados a Lucas.
3. **g2 (preguntaApoyo).** «Vivo en México.» (podía ser la ciudad, «à Mexico») → «Vivo en México (el país).»
4. **g3 (pista).** ««Où» = dónde.» (no distinguía «¿Dónde vive?» de «¿De dónde es?») → ««Habitez» viene de habiter = vivir.»
5. **g4 (pista).** Genérica → ««Appartement» se parece a «apartment»; un «quartier» es una zona dentro de la «ville».»

### c09 · aimer
1. **Vocabulario «le thé».** «La h no suena: «lö té»» → ««th» suena «t» (la h no suena): «lö té»». Y «ö» se define en el sonido del día: «le = «lö» (ö = la «eu» de «deux», con los labios redondeados)» (en inglés: «like the “eu” of “deux”, lips rounded»).
2. **Explicación (alcance con B3).** «Lo que te gusta lleva siempre artículo definido» → «Lo que te gusta (los gustos en general) lleva siempre artículo definido» (es/en), para que B3 profundice en el artículo.
3. **Relacionar ambiguo (g4).** «me gusta» frente a «me gusta (más suave)» (inglés «I like it» / «I quite like it») eran glosas casi iguales. Se quita el par «j’aime bien» y quedan 3 pares: j’adore = me encanta, j’aime = me gusta, je déteste = lo odio. Pista: «Adorer y détester se parecen a «adorar» y «detestar».» (antes genérica). En inglés, «I quite like it» (poco claro para un estadounidense) → «I like it (milder)» en la explicación, la tabla y la traducción de la situación.
4. **Ejemplos (l’).** No había ningún ejemplo con l’ ni con una lengua, pese a que la explicación lo anuncia. «Je déteste le lait.» → «J’aime l’espagnol. Je déteste le lait.» («Odio la leche» se conserva).
5. **e5 escribir.** `aceptadas` + «Tu aimes bien la danse ?» (coherente con la i3, que ya aceptaba «J’aime bien le chocolat.»).

### c10 · travailler / étudier
1. **Personajes (contradice B1).** Emma: «Je suis canadienne.» → «Je suis américaine.» (B1 c05: Emma es estadounidense). Traducciones es/en actualizadas.
2. **Sonido del día (afirmación inexacta).** «después de vocal, «ill» y «il» suenan «y»» era falso en general (la «ville» de c08 suena «vil», y «il» después de vocal solo suena «y» a final de palabra). → ««ill» suena «y» (fille = «fiy»)… Es distinto de «ville» (vil), que viste en la clase 8.»
3. **Vocabulario «médecin».** Sin pronunciación → «medsán» (es) / “mehd-san” (en).
4. **g3 (pista).** «Travaille = trabaja; étudie = estudia.» (étudie no aparece en el audio) → ««Travaille» = trabaja; «hôpital» se parece a «hospital».»
5. **g4 (pista).** Genérica → ««Hôpital» se parece a «hospital» y «école» a «escolar».»
6. **e4 ordenar.** `aceptadas` + «Je travaille dans un bureau et j’habite à Quito.»
7. **e5 escribir.** `aceptadas` + «Je parle espagnol et j’habite à Paris.»

## Revisado y sin cambios (puntos de la calibración de B1)

1. **Ordenar con todos los órdenes.** Revisados los 9 `ordenar`. Con un único orden natural (el resto): c07 i1 «Tu parles anglais ?», c08 i1 y e4, c09 i1 y e4 (el adverbio «beaucoup» va tras el verbo), c10 i1.
2. **Pistas y relacionar.** El resto de pistas ya ayudaba a ese ítem. Los demás relacionar tienen glosas claramente distintas (oficina/tienda/escuela/hospital, casa/departamento/ciudad/barrio, etc.).
3. **Fonética.** Sonido del día exacto en las 5 clases: ou/on nasal y s final muda en c06; -e/-es/-ent mudas y -ons/-ez audibles en c07; h muda, j’ y enlace en «nous‿habitons» en c08; «ai», l’, j’ y «elles‿aiment» («el-zem») en c09; ill/étudier en c10. Consonantes finales (CaReFuL): «sport» conserva la r en la nota («spor»), «chocolat», «croissants», «portugais» y «allemand» marcan correctamente la t/s/d final muda.
4. **Diálogos.** Modelan el objetivo de cada clase y la cortesía: «Et toi ?» devuelto en c06 y c08, tutoteo entre amigos coherente, preguntas de comprensión con una sola respuesta. c10 es una mini lectura (5 líneas de Emma) que cierra con «Et toi ?».
5. **Femeninos.** étudiante, seule, française, américaine, canadienne y las demás formas aparecen en femenino para personajes femeninos.
6. **Nada sin enseñar, tipografía y bilingüismo.** Ver las comprobaciones de arriba. Español con tú; inglés americano con comparaciones («English uses “in” for all of them», «unlike English “I’m a doctor”»).
7. **Alcance con B3.** c09 solo enseña aimer + artículo definido para gustos en general (le/la/l’/les); un/une/des y el plural en profundidad quedan para B3.

## Lo que no se pudo (o no se quiso) corregir

- Nada pendiente. Observaciones menores que se dejaron a propósito:
  - En la columna de pronunciación en español, la j francesa se escribe «y» («yabit») y en la nota de «le village» «sh» («vilash», con la explicación «j suave»). Es aproximado y coherente con la descripción; no confunde.
  - «Je habite» / «Je aime» etc. no se pueden aceptar como respuesta (son los errores enseñados).
  - El esquema aún no admite el formato «Repite» (igual que en B1).
