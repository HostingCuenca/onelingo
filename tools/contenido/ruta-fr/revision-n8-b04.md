# Revisión N8 · B4 (fr.n8.c16–c20) — Variedades del francés

GO

Condición única para integrar: añadir `Félix` a `palabrasLibres` de `curso.json` (el coordinador ya añadió Olivier, Mélanie, Aïssatou, Camille, Bruxelles, Lausanne, Genève, Dakar y Abidjan; Félix es el nombre nuevo del amigo de Lucas, ver corrección a). Sin esa línea el validador oficial da exactamente 1 error (`fr.n8.c16.p12.dialogo[2]: félix`). Con `Félix` añadido, validado en una copia de `curso.json` en el scratchpad: 0 errores. `validar_plan.py fr`: 0 errores y sin «título de la unidad difiere» para fr.n8.c16–c20.

Validación (n8-b01…b04, con n7 ya integrado): 0 errores en mi bloque. Durante la revisión otros bloques (n8-b03, n8-b02) estaban en edición y dieron errores propios transitorios (`profitez`, `fantôme`); no son de B4.

## Qué comprobé
- Las 5 unidades enseñan lo que dicen sus fichas (título, objetivo, gramática, introduce, recicla, vocabulario, situación, tarea) y llevan los ejercicios planificados con su formato y clave. No hay nada de fichas posteriores.
- Evaluación: c16, c17, c18, c19 y c20 tienen 5 ítems puntuables cada una (≥ 4) en 4 o 5 formatos distintos (≥ 2); el `escribir` abierto (`abierta: true`) es un sexto ítem y no cuenta.
- Anatomía de clase, tipografía (U+202F antes de ? ! : ; y en las comillas francesas, apóstrofo ’), español neutro de América (tú) e inglés americano: revisados con script en todo el bloque.
- Situaciones (palabras del diálogo): c16 405, c17 434, c18 418, c19 419, c20 400 (rango C1 400–700).
- Tablas «Para leer»: c16 4 filas, c17 3 filas (límite 15). La tabla más larga de B4 es «Quebec y Francia» (12 filas), tabla de enseñanza, no «Para leer».
- Fonética: guías «sh»/«zh», nasales «en»/«an», ü y ö definidas al aparecer.
- Exactitud lingüística de variedades (belgicismos, helvetismos, québécismes, africanismos, verlan): revisada; ver f).

## Correcciones

a) **Choque de nombre (Antoine = esposo de Chloé, N6 c03).**
- c16 situación, réplica 3 de Lucas: «mon chum Antoine … Antoine, lui, va te poser mille questions» → «mon ami Félix … Félix, lui, va te poser mille questions» (texto, es, en). También cambié «chum» por «ami»: con «ma blonde, Camille» al lado, «mon chum» leído como «novio» sugería otra cosa. «Félix» no se añade como vocabulario.

b) **Nombres/lugares ya en `palabrasLibres`.**
- c17 `vocabulario`: eliminadas las entradas ocultas `v-olivier` y `v-melanie` (no estaban en `refs`).
- c17 tabla p3 «La Belgique et la Suisse»: eliminada la columna «Ciudades» (Bruxelles; Lausanne, Genève); queda País + Adjetivo (la Belgique / belge, les Belges; la Suisse / suisse, les Suisses). Texto de la tabla ajustado (es/en).
- c18 `vocabulario`: eliminada la entrada oculta `v-aissatou`.
- c18 tabla p2: eliminadas las filas «Dakar» y «Abidjan»; título «Pays et villes» → «Les pays» (es «Países», en «The countries»). Se conservan l’Afrique, le français d’Afrique, le Sénégal y la Côte d’Ivoire, que sí enseñan palabras usadas en el texto.

c) **Visita de Lucas a París (N7 c09: viaje en tren del 3 al 24 de mayo, tres días en París, primera visita; N7 c36–c37).**
- c20 mantiene a Lucas en la cena de Chloé «de visita en París unos días» sin fecha ni «primera vez»: queda como una segunda visita sin tiempo fijado, compatible con mayo (c09), con la videollamada de agosto desde Montréal (c37) y con el mensaje de voz de c16 desde Montréal. No requiere cambios de texto; lo dejo anotado en los hechos.
- c16: Lucas dice «Hugo est déjà venu chez moi»: coincide con N3 c23 (Hugo, diez días en Montréal).

d) **Viaje de Ana a Bélgica y Suiza frente a su agenda de N8 (Quito c02/c04, Lyon c03, noche hacia el sur c05, y la invitación a Montréal en primavera de c16).**
- c17 contexto y diario: «lunes a sábado» (6 días, «trois jours» solo en Bruselas, con permiso del director) → viaje corto de **jueves a domingo**, «pour deux jours» de permiso más el fin de semana. Rehechas las etiquetas del diario (Jeudi → Vendredi → Samedi matin «avant de partir» → Samedi soir → Le lendemain → Dimanche) en francés, es y en. Trayecto Bruselas–Lausana plausible en un sábado. Contexto es/en actualizado.
- c17 diario, traducción inglesa de la réplica 2: «I ne sais pas venir» → «je ne sais pas venir».
- c16: Ana pide al director días libres para ir a Montréal «au printemps», sin confirmarlo; queda como proyecto, no como viaje hecho.

e) **Tablas ≤ 15 filas:** ya cumplido, sin cambios (ver arriba).

f) **Africanismos y variedades, exactitud y respeto.**
- c18 explicación p1: quitado «Argelia» de la lista de países con más francófonos (el francés allí no es lengua oficial; se mantienen Senegal, Costa de Marfil, Camerún, RDC y «muchos otros»).
- c18 situación, réplica 4 de Aïssatou: «Alors tu vas aimer le Sénégal ! » (no seguía de lo que dijo Ana) → «Alors tu vas aimer les mots du Sénégal ! ».
- c20, Olivier: «Chez nous, tout le monde l’utilise» (generalización que contradice el matiz que enseña c18) → «Chez nous, on l’utilise beaucoup».
- c19, error frecuente 3: «Il est lourd, ce prof : c’est un relou» → «Il est relou, ce prof» afirmaba que «relou» no es sustantivo, y es falso («un relou» existe). Sustituido por «Il est grave sympa.» → «Il est très sympa.» (intensificador familiar, no «grave» = serio; en situación formal, «très»).
- c19 p1: «hablar “a l’envers”» → «à l’envers». c19 traducción: «liceo» → «colegio» (es neutro).
- c17 p5: «el camarero» → «el mesero».

g) **Ítems y variantes (una sola respuesta defendible; todas las válidas en `aceptadas`).**
- c16 i3: consigna «usted, venir» → «“vous”, venir» (la respuesta es «Venez-vous»).
- c16 situación: «C’est pas loin : vingt minutes, pantoute ! » → «C’est pas loin, pantoute : vingt minutes. » (pantoute refuerza la negación). Ampliado el audio de Lucas con tres frases cortas para alcanzar el rango (380 → 405 palabras): «Ma ville est belle, même en hiver.», «Ici, en hiver, tout le monde porte une tuque.», «Ensuite, on revient en ville et on mange ensemble.» (es y en igualados).
- c20 g3 (ordenar): añadidos «Chez nous, on dirait la fin de semaine plutôt» y «On dirait plutôt … chez nous / la fin de semaine plutôt, chez nous».
- c20 e5 (ordenar): añadido el orden natural «Au juste, ça veut dire quoi ?».
- c20 g5 (escribir): la consigna no fijaba el vocabulario (alguien podía escribir «le déjeuner» en vez de «le repas de midi»): ahora pide «désigne», «le repas du soir», «le repas de midi» y «alors qu’au Québec», y `aceptadas` incluye las variantes con «tandis qu’» y con «il désigne» en la cláusula del Québec.
- c20 relacionar (p4, g4, e1): las glosas «pregunta por el sentido» y «pide una definición» se confundían; ahora «pregunta cómo usa la palabra el otro» / «pide una definición» (es y en).
- c20 situación, réplica de Ana: eliminado «au sens strict, « une fois » est un nombre ; au sens large, … » (uso incorrecto de sens strict/large: no es un caso de sentido estricto frente a amplio); se conserva la reformulación «viens une fois = viens».

## Hechos del reparto confirmados
- Lucas vive en Montréal y tiene novia, Camille (la «blonde» de c16), y un amigo, Félix; el sábado salen de compras, el domingo van a la «cabane à sucre» / Lucas lives in Montréal and has a girlfriend, Camille (his “blonde” in c16), and a friend, Félix; on Saturday they go shopping and on Sunday to the “cabane à sucre”
- Lucas invita a Ana a visitarlo en Montréal en primavera; Ana debe pedir días libres al director del hotel y no confirma / Lucas invites Ana to visit him in Montréal in the spring; Ana has to ask the hotel director for time off and does not confirm
- Hugo ya estuvo en casa de Lucas en Montréal (N3 c23) / Hugo has already stayed at Lucas’s place in Montréal (N3 c23)
- Olivier, belga de Bruselas y amigo de Chloé, recibe a Ana en Bruselas; tiene familia (muestra su foto) / Olivier, a Belgian from Brussels and a friend of Chloé’s, hosts Ana in Brussels; he has a family (he shows her a photo)
- Mélanie, suiza de Lausana y amiga de Lucas, estudió en Montréal y aloja a Ana / Mélanie, Swiss from Lausanne and a friend of Lucas’s, studied in Montréal and hosts Ana
- Ana viaja de jueves a domingo a Bruselas y Lausana, con dos días de permiso aprobados por el director del hotel / Ana travels Thursday to Sunday to Brussels and Lausanne, with two days off approved by the hotel director
- Aïssatou, senegalesa y amiga de Chloé, es profesora de letras en una universidad de Dakar y pasa una semana en París por una conferencia; Ana y ella se tutean y Chloé y Ana se tratan de vous / Aïssatou, a Senegalese friend of Chloé’s, is a literature professor at a university in Dakar and spends a week in Paris for a conference; Ana and she use tu, while Chloé and Ana use vous
- Chloé, nacida en Montréal (N5), dice «souper» y confirma que en Quebec también se dice «tantôt» / Chloé, born in Montréal (N5), says “souper” and confirms that “tantôt” is also used in Québec
- Ana, Hugo y Léa ven una serie juvenil en casa de Léa; Léa nunca habla así con su madre ni con Monsieur Martin, y Hugo cambia de registro en la universidad / Ana, Hugo and Léa watch a teen series at Léa’s place; Léa never talks like that with her mother or Monsieur Martin, and Hugo switches register at university
- Cena en casa de Chloé con Ana, Lucas (de paso por París unos días, segunda visita sin fecha tras su viaje de mayo), Aïssatou y Olivier (llegado de Bruselas para el fin de semana); Chloé cocina / Dinner at Chloé’s with Ana, Lucas (in Paris for a few days, a second visit with no set date after his May trip), Aïssatou and Olivier (come from Brussels for the weekend); Chloé does the cooking

## Sin resolver / avisos para el coordinador
1. **`Félix` en `palabrasLibres`** (condición del GO). Sin él, c16 falla.
2. «Camille» (la novia de Lucas) coincide con otras Camille de ejemplos de N-anteriores (prima / nieta de familias distintas). No hay choque con el reparto principal; si prefieres evitarlo, cambiar el nombre exige actualizar `palabrasLibres`.
3. Ningún término francés que otro bloque de N8 use ha sido retirado ni renombrado: lo eliminado son nombres propios ya libres (Olivier, Mélanie, Aïssatou, Dakar, Abidjan, Bruxelles, Lausanne, Genève). Si un bloque posterior de N8 se apoyaba en esas filas/entradas para «enseñar» esos nombres, ahora dependen de `palabrasLibres`.
4. Fuera de mi bloque (aviso, no lo toqué): en N8 B1, c02 describe a Ana volviendo de Quito en avión y c04 a Ana saliendo hacia Quito (tres semanas con sus padres); conviene fijar el orden (c04 antes que c02) para que la agenda de viajes de Ana, ya apretada con Lyon (c03), el tren nocturno (c05) y este viaje a Bélgica y Suiza (c17), sea creíble.
