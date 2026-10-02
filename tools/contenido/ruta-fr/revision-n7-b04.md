# Revisión N7 · B4 (fr.n7.c16–c20)

GO

Revisor distinto del autor. Contrastado con las 5 fichas de `curriculo/fr/n7.json` (incl. plan de `ejercicios`) y la `nota` del nivel, `personajes` y `hechosDelReparto` de N1–N6, `ENCARGO_RUTA_FR.md` (Por nivel N7 + calibración 1–13), `ESQUEMA_CONTENIDO.md` y `PLAN_CLASES.md`.

Validación (n7-b01…b04, con N6 ya integrado en `assets/`): `0 error(es)`. También 0 errores con la cadena completa de borradores n7-b01…b10 (comprobado para detectar palabras que bloques posteriores usaran y yo hubiera quitado). `validar_plan.py fr`: ningún «título de la unidad difiere» para fr.n7.c16–c20. Sin avisos de contaminación en el bloque.

## Verificaciones sin cambios

- Contenido = fichas: títulos y objetivos idénticos; vocabulario de cada tarjeta (8, 8, 9, 9, 8 palabras) coincide con la ficha y se muestra en el paso `vocabulario`; los repasos (`participe-compose`, `voix-passive-complete`, `preposition-qui`, `selon-d-apres`, `une-fois-participe`, `forme-pronominale-passive`, `mise-en-relief`, `relatif-ou`, `present-historique`, `reprises-anaphoriques`) entran como repaso. El passé simple de c19 («vécut») y el presente histórico de c20 ya se enseñaron en c06–c07.
- Plan de ejercicios: cada clase contiene los ítems planeados con el mismo formato y clave (guiada 5, independiente 4, situación 2, evaluación 6). Cambios del autor y míos dentro de lo permitido (redacción, verbos de apoyo, distractores).
- Anatomía: explicación(es), tablas, 8 ejemplos, vocabulario, guiada con `pista`, independiente sin pista, situación y evaluación al final. Situaciones de 330–346 palabras (rango N5–N7: 300–500), con 2 ítems de comprensión coherentes con el texto.
- Evaluación (≥ 4 puntuables y ≥ 2 formatos; los `escribir` con `abierta: true` no cuentan): c16 6 puntuables (completar, elegir, ordenar, escribir cerrado); c17 5 (completar, relacionar, elegir); c18 5 (completar, elegir, ordenar); c19 5 (completar, ordenar, elegir, escuchar); c20 5 (elegir, relacionar, completar, escuchar). Cumple en las cinco.
- Producción abierta (punto 13): c17 c18 c19 c20 e6 tienen `abierta: true`, `minimoPalabras` 12–15 y modelo de 23–31 palabras (consignas «≈ 20–40»).
- Tipografía: U+202F antes de `? ! : ;` y dentro de « » en todo el francés; apóstrofo ’ (sin rectos). Comprobado con script en todos los campos franceses.
- Hablantes: nombres o papeles/documentos en francés (Hugo, Ana, Une visiteuse, Un visiteur, Une cliente, Un client, La première version, Le premier panneau, L’article d’Ana…), como en bloques anteriores; ninguno en español.
- Español neutro de América (tú/ustedes, estacionamiento, vestíbulo) e inglés americano (meters, theater); sin «coche/ordenador/billete/zumo…».
- Hechos históricos revisados: torre Eiffel 1889 (300 m, desmontaje previsto a los 20 años); Fulgence Bienvenüe, ingeniero del metro, obras 1898, primera línea 1900; Roland Moreno, tarjeta con chip, primera patente 1974; Minitel de los años 80, precursor de internet, origen en un proyecto de las telecomunicaciones francesas (años 70); tarte Tatin nacida en un hotel (hôtel Tatin); Limoges y el caolín, cocción a 1 400 °C; Victor Hugo 1802–1885 vivió en el Marais (place des Vosges: «la maison où vécut Victor Hugo»); recinto de Philippe Auguste como «vestigio del rempart»; anexión de 1860 (la ley de 1859 hizo efectiva la anexión de los suburbios a París el 1 de enero de 1860); haussmanización (1853–1870); Belle Époque (c. 1890–1914); siglo XX = 1901–2000 y III milenio desde 2001 (se explica «en sentido estricto»). Todo correcto.
- Hugo: guía-conferenciante con el máster terminado (nota de N7) que guía recorridos por el barrio (N7 c02: «hace de guía en el barrio»). El bloque lo muestra preparando fichas para sus visitas (c16), guiando a clientes del hotel (c18, c19) y conociendo la historia local por ellas (c20). Coherente; sus estudios de máster no aparecen en el bloque.
- Pronunciación: guías es/en con las convenciones del Nivel 0 (sh/zh, nasales, ü/ö definidas al aparecer) revisadas palabra por palabra; sin errores.

## Correcciones aplicadas

| Clase | Ítem / campo | Antes → después |
|---|---|---|
| c16 | explicación p1 (es/en) | decía que la diferencia con el español es que el francés concuerda el participio (falso: el español también) → «igual que en español, concuerda…; en inglés no cambia» |
| c16 | tabla «La concordancia» (p5) | filas mal etiquetadas («antes y pasiva» dos veces, «activa») para meter frases de ítems → renombrada «La concordancia y las construcciones vecinas» con etiquetas claras (participio compuesto, pasiva completa, voz activa, participio presente) |
| c16 | tabla «Para leer la situación» (p8) | 25 filas con relleno («une apposition, des appositions», «les visiteurs la photographient», preguntas…) → 14 filas (halle, fiche, lis-moi, ingénieur, métallique, repose sur, menacée, sauvée, apposition, condenser, antérieur, identité, édifier, «Quelle phrase est correcte ? / incorrecte ?») |
| c16 | situación (diálogo) | «photographient», «hauteur», «légèreté»: se simplificó el texto para no enseñar de más («Pour dire qu’elle est haute…»; ficha sin «légèreté»; el error plantado ahora es «les touristes aiment la halle»); fiche final sin repetir «quartier» tres veces |
| c16 | s1, s2 (comprensión) | opciones en es/en → francés: «un participe en apposition» / «À marquer l’identité du quartier» con `pregunta` en francés |
| c16 | g5, e5 | `pregunta` francesa que exigía enseñar «exprime l’antériorité», «passif complet» → se quita; la consigna es/en basta |
| c16 | i4 y e2 (distractor erróneo) | «les visiteurs / les touristes la photographient» → «les touristes aiment la halle / la façade» (solo palabras enseñadas); i4 añade `pregunta` |
| c16 | e2 feedback | «En la segunda frase…» pero la frase incorrecta era la primera → «En la frase de los turistas…» |
| c16 | i4 feedback | «classée se refiere a la halle» (la frase habla de la iglesia) → «a la iglesia» |
| c16 | e3 (ordenar) | token «spectaculaire» (no enseñado) → «magnifique» (enseñado), con la variante aceptada |
| c16 | tabla p3 fila 7 y e6 consigna | «Il est un ouvrage d’art majeur» (poco natural) → «C’est un ouvrage d’art majeur» |
| c16 | i3, e6 `aceptadas` | respuesta duplicada / «important» innecesario → depuradas |
| c17 | tablas «Para entender los ejemplos» (p4) y «Para leer» (p7) | 22 + 13 filas con duplicados («les télécommunications» dos veces, «attribuer, il attribue, attribuée à», «ce brevet remonte à 1974», «Qu’en penses-tu ?»…) → 9 + 6 filas; los nombres propios (Bienvenüe, Moreno, Minitel, Tatin) en filas breves con glosa |
| c17 | tabla p2 | texto «cuatro registros de precisión» (no encajaba con 6 fórmulas) → descripción real; «remonter à… (il remonte à…)» enseña la forma que usan los ejemplos |
| c17 | explicación p3 | decía que «être attribué à / avoir pour origine» son para mérito «colectivo», pero el diálogo y la tabla usan «être l’œuvre de» para un grupo → texto coherente (autor claro, persona o grupo: on doit / être l’œuvre de; duda: être attribué à; origen: avoir pour origine / trouver son origine dans; fecha: remonter à) |
| c17 | siglos romanos (ejemplo 4, error 2, g4) | «remonte au XVIe siècle» / «à le XVIe siècle»: los números romanos se enseñan en c20 (ficha posterior) → «remonte au Moyen Âge» y g4 «remonte ___ siècle dernier» |
| c17 | g5 (ordenar) | «un ingénieur lyonnais» (palabra no enseñada) → «un ingénieur français» |
| c17 | panel 2 | «à qui l’on doit aussi son premier brevet» (una patente no se «debe») → «à qui l’on doit cette trouvaille. Son premier brevet remonte à 1974» |
| c17 | diálogo | «Qu’en penses-tu ?» → «Tu es d’accord ?»; «d’ingénieurs» → «de plusieurs ingénieurs»; «certaines trouvailles remontent» → «la plus ancienne de ces inventions remonte» (evitan formas no enseñadas) |
| c17 | s1, s2 | opciones en es/en → francés («Roland Moreno.»; «On doit le métro à…») con `pregunta`; distractor «un fruit de» (no enseñado) → «a pour origine» |
| c17 | e6 (abierta) | modelo de 14 palabras con consigna «≈ 20–40» → modelo de 30 palabras con dos fórmulas de atribución |
| c18 | tabla p4 | primera columna con español dentro de celdas `texto` («une fois + participio», «forma pronominal»: se leían con voz francesa y contaban como francés) → «une fois + participe passé» y celda `apoyo` |
| c18 | tabla «Para leer» (p7) | 17 filas con frases de relleno → 11 filas (Limoges, kaolin, attentif, séchage, décoration, couvercle, mécanique, entièrement, abriter, fabriqué à la main, soumettre) |
| c18 | diálogo | «les pièces abîmées sont retirées» → «on met de côté les pièces abîmées» (sin palabra nueva) |
| c18 | g2 | `pregunta` «Quel verbe forme une périphrase passive ?» (exigía enseñar «périphrase») → se quita; la consigna ya lo dice |
| c18 | s1, s2 | opciones en es/en → francés («Le séchage.»; «Elle fait l’objet d’une cuisson.») con `pregunta` sin trazos de unión no enseñados |
| c18 | e3 | opciones sin mayúscula («on la contrôle.») → «On la contrôle.» etc. |
| c18 | e4 `aceptadas` | faltaba «On procède, au terme de la cuisson, à l’assemblage.» → añadida |
| c18 | e6 (abierta) | modelo de 12 palabras con consigna «≈ 20–40» → modelo de 23 |
| c19 | tablas p3 y p9 | p3 mezclaba adverbios, una frase y sustantivos bajo «Hablar del pasado» → «Hablar del pasado y del lugar» con filas coherentes; p9 «Para leer» de 19 filas (naguère/autrefois repetidos, 4 preguntas, «les cloches donnaient l’heure», …) → 5 filas |
| c19 | diálogo | «pavée» → se mantiene con fila; «Qu’y avait-il…» (guion) → «il y avait quoi autrefois ?»; «de quelle époque ?» → «de quand ?»; «Entrons», «terminons» → «Venez avec moi», «nous finissons»; «vendait du pain» → «se trouvait la boulangerie»; «marché aux fleurs» → «aux légumes»; «Il a le même nom que vous» (Hugo Durand no se apellida Hugo) → «Il s’appelle comme vous»; «Faites attention aux pavés, ils sont glissants» → con dos puntos |
| c19 | i1, i3 `pregunta` | «situer l’endroit exact», «renvoie à un passé lointain» (palabras no enseñadas) → «Pour dire « exactement ici »…», «Quelle expression parle du passé ?» |
| c19 | e4 | distractor «La maison où Victor Hugo vécut ici» (en realidad también es gramatical) → «La maison où vécut il est ici» (error enseñado), una sola respuesta correcta |
| c19 | s1, s2, e5 | opciones en es/en → francés («À gauche du groupe.», «Un marché.», «À gauche.») con `pregunta` en francés; e5 sin `pregunta` → «Où est le clocher ?» |
| c19 | e6 (abierta) | modelo de 19 palabras con consigna «≈ 20–40» → modelo de 27 |
| c20 | tablas p3, p6, p7 | p3 «del más preciso al más vago» (no es cierto) → «las expresiones de la clase»; p6 de 21 filas con frases del artículo + p7 «Para entender las consignas» (conclusion, introduction, titre, index, résumé) → una sola tabla de 13 filas; p7 eliminado y pasos renumerados p1–p12; p2 recibe «le XVe siècle» |
| c20 | g4 | distractores «conclusion, introduction, titre» / «résumé, index, notes» (6 palabras sin valor) → los tres órdenes posibles de «les origines, les transformations, la situation actuelle» (solo la cronológica es el plan enseñado) |
| c20 | g1, e1 | `pregunta` «Comment lit-on…» (token con guion sin enseñar) → «« Le XXe siècle » se lit : …» |
| c20 | e3 | «(décennie)» inducía a escribir «décennies» → consigna «Completa la expresión “en los años veinte”», sin pista en paréntesis |
| c20 | e6 (abierta) | «Le marché a été fondé en 1860» y «attirait» (formas no enseñadas) → «La gare a été construite en 1860» y presente histórico; modelo de 31 palabras |
| c20 | diálogo | EN de Ana perdía la última frase («I end with a question…»); «Que reste-t-il…» (guion sin enseñar) → «il reste quoi de toutes ces époques…» |
| c20 | s1, s2, e5 | opciones en es/en → francés («au XIXe siècle.», «Ce coin de Paris.», «Juste après la guerre.») con `pregunta` en francés; e5 con `pregunta` |
| c20 | error frecuente 1 | `correcto` con paréntesis explicativo → solo «Le XXe siècle commence en 1901.»; explicación aclara «en sentido estricto» |

Comprensión en francés: los 10 ítems de situación y los 2 `escuchar` (c19 e5, c20 e5) vuelven a tener opciones en francés (12 de 12).

## Hechos del reparto confirmados

- Hugo, con el máster terminado, trabaja como guía-conferenciante: prepara fichas para sus visitas (c16), guía a clientes del hotel de Ana por un barrio histórico (c19) y a Limoges (c18) y conoce la historia local por sus visitas (c20); Ana y él se tutean, y su apellido sigue siendo Durand (el visitante de c19 bromea con Victor Hugo y Hugo lo niega) / Hugo, his master’s finished, works as a licensed tour guide: he prepares fact sheets for his tours (c16), leads hotel guests through a historic neighborhood (c19) and to Limoges (c18), and knows the local history from his tours (c20); he and Ana use tu, and his surname is still Durand (a visitor in c19 jokes about Victor Hugo and Hugo says no).
- La halle, mercado cubierto del barrio, se construyó en 1868 por un ingeniero del barrio, mide 30 m, está clasificada monumento histórico, estuvo amenazada de destrucción hace unos cincuenta años, la salvaron los vecinos y se renovó hace dos años (coherente con N5 c34, reapertura del mercado cubierto de su barrio); es el centro de la ficha de Hugo (c16) y del artículo de Ana (c20) / The halle, the neighborhood’s covered market, was built in 1868 by an engineer from the neighborhood, is 30 m high, is a listed historic monument, was threatened with destruction about fifty years ago, saved by the residents and renovated two years ago (consistent with N5 c34, the reopening of the covered market); it is the subject of Hugo’s fact sheet (c16) and Ana’s article (c20).
- Ana coordina una pequeña exposición del hotel sobre inventos franceses (tres paneles en el vestíbulo más uno de bienvenida: metro, tarjeta con chip, Minitel y tarta Tatin), la prepara con Hugo y él irá a ayudarla con el montaje el sábado; el director (sin nombre) estará contento / Ana coordinates a small hotel exhibition on French inventions (three lobby panels plus a welcome panel: subway, smart card, Minitel and tarte Tatin), prepares it with Hugo, and he will help with the setup on Saturday; the director (unnamed) will be pleased.
- Ana organiza para los clientes de su hotel una salida a una fábrica de porcelana de Limoges; Hugo es el guía y Ana toma apuntes de las fases / Ana organizes an outing for her hotel’s guests to a porcelain factory in Limoges; Hugo is the guide and Ana takes notes on the stages.
- En el recorrido de c19 Ana, que organizó la visita, «cierra la marcha» y Hugo la trata de tú / On the c19 tour Ana, who organized the visit, brings up the rear and Hugo uses tu with her.
- Ana escribe para la revista del barrio (serie «Une Équatorienne à Paris») un artículo sobre la historia de su barrio (antiguo pueblo de jardineros, faubourg anexado a París en 1860, titulado «Un village devenu quartier»); Hugo lo lee para comprobar las fechas (tú) / Ana writes for the neighborhood magazine (series “Une Équatorienne à Paris”) an article on the history of her neighborhood (a former gardeners’ village, a suburb annexed to Paris in 1860, titled “Un village devenu quartier”); Hugo reads it to check the dates (tu).
- Ana habla de vous con el director y de tu con Hugo, como fija el canon (punto 12); no aparecen Roux, Lefort ni Dubois en el bloque.

## Sin resolver / avisos para el coordinador

- Palabras que quité o cambié y que otros bloques podían usar: se comprobó que ningún borrador n7-b05…b10 las usa sin enseñarlas (validador) ni los n8-b02…b09 actuales (comprobación por palabras, sin cadena completa). Se conservaron a propósito dos filas que SÍ usaban bloques posteriores: «lis-moi la fiche» (c16 → n7 c43) y «un élément» (c19 → n7 c42). Si se editan, hay que revisar esos bloques.
- Nombres propios (Bienvenüe, Fulgence, Moreno, Roland, Minitel, Tatin, Limoges, Victor Hugo): van como filas con glosa porque `palabrasLibres` está fuera del alcance de este encargo; el coordinador puede pasarlos a `palabrasLibres` en `curso.json` al integrar y entonces quitar sus filas (c17 p4/p7, c18 p7) sin riesgo.
- El texto de c16 y el de c20 mencionan la misma halle y las mismas fechas (1868, «il y a cinquante ans»); cualquier cambio en una debe repetirse en la otra.
- El script `scratchpad/val.sh` compartido fue sustituido por otro agente durante la revisión; la validación final se hizo con la orden del encargo.
