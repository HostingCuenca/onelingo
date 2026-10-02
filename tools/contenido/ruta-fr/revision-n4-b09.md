# Revisión N4 · B9 (fr.n4.c41–c45)

GO

Validación final: `python3 tools/validar_ruta.py fr --borrador n4-b01 … n4-b09` (sin los n3-b*, ya integrados) → **0 errores**. `validar_plan.py fr`: ningún «título de la unidad difiere» para fr.n4.c41–c45 (los dos avisos de título que quedan son de fr.n4.c26 y fr.n5.c26, ajenos a este bloque).

Alcance revisado: las 5 fichas (títulos, objetivos, gramática, introduce/recicla, vocabulario, situación, tarea y plan de ejercicios), nada de clases posteriores, francés de Francia (concordancias, registro, U+202F, ’), explicaciones es/en, una sola respuesta por ítem, glosas de relacionar, longitud de la situación (170–203 palabras, dentro de 150–250), hablantes (nombres o «La secrétaire» / «Le journaliste»), anatomía de la clase y ≥ 4 ítems puntuables en cada evaluación (5 puntuables + 1 `escribir` abierto).

## Correcciones

### Los dos puntos del coordinador

1. **c44 (la llamada ya no es sobre la inauguración de Karim).** En fr.n4.c06 (b02) ya se invita a todos a la apertura de su segundo restaurante. La llamada trata ahora de la **fiesta del barrio** de c43 (Karim la organiza con los vecinos): fecha el 14, 20 h, rue Lafayette, entrada gratuita, cien invitados; Emma (que trabaja con Karim) está en la lista y Ana va con Léa y Hugo. Cambios concretos:
   - `contexto` (es/en) reescrito.
   - `dialogo` línea 2: «…les détails de l’inauguration» → «…les détails de la fête du quartier».
   - línea 4: «L’inauguration est le 14, n’est-ce pas ?» → «La fête est le 14, n’est-ce pas ?»
   - línea 5: se añade «Karim organise tout avec les voisins.» (enlaza con c43).
   - `ejemplos` 4: «Tu ne viens pas à l’inauguration ?» → «Tu ne viens pas à la fête du quartier ?»
   - `ejemplos` 7: «l’inauguration est à vingt heures» → «la fête du quartier commence à vingt heures».
   - s1 `preguntaApoyo`: «¿A qué hora es la inauguración?» → «¿A qué hora es la fiesta del barrio?»
   - vocabulario: se elimina «l’inauguration» (y su ref en p8). La enseña fr.n4.c06; ningún bloque posterior de N4 la usa desde c44.
2. **`escribir` abiertos fuera de práctica.** `i4` de c41–c45 (practica_independiente) eran `abierta: true`. Pasan a ítems cerrados «Escribe en francés: «…»» con `respuesta` + `aceptadas` (sin `abierta`, sin min/max de palabras, sin `pista` porque el validador solo la admite en la guiada). Los `e6` de las evaluaciones siguen abiertos y puntúan 5 ítems cerrados.
   - c41 i4: «En France on mange des crêpes, alors qu’en Équateur on joue avec de l’eau.» (+ variantes con comas y con la subordinada al inicio).
   - c42 i4: «Le gaspillage provoque beaucoup de déchets. Par conséquent, la ville est sale.» (+ variante con « ; »).
   - c43 i4: «Nous exigeons que la mairie recycle les déchets. Nous agissons pour que la ville soit plus propre.» (la consigna fija exiger que y pour que, así no cabe afin que).
   - c44 i4: «Le concert est à vingt heures, n’est-ce pas ?» (+ «20 heures» y sin signo).
   - c45 i4: «L’année où nous sommes arrivés au village, il y avait une grande foule.» (+ «arrivées», «beaucoup de monde», orden invertido).

### Otras correcciones

- **c41 g1 feedback (es):** «alors que au Japon» → «alors qu’au Japon» (elisión).
- **c41 p1:** «alors y tandis nunca van solos» → «en esta función alors y tandis nunca van solos» (alors solo existe como palabra suelta en otros usos); igual en en.
- **c41 p2 / p5 / situación (línea 5):** «À la différence du Canada, il n’y a pas de jour férié pour la Chandeleur» era ilógica (la Chandeleur tampoco es feriado en Canadá). Ahora: «À la différence du carnaval, il n’y a pas de jour férié pour la Chandeleur.» Se actualiza «Por eso: à la différence du carnaval, contrairement au carnaval», la fila de la tabla y la traducción es/en. Sigue demostrando de + le = du.
- **c41 vocabulario:** gloss de «le poisson d’avril» más claro (día de las bromas; literalmente «pez de abril»).
- **c42 e5 (relacionar):** en inglés «the useless use of resources» → «the wasteful use of resources» (par y feedback). c42 i4 en inglés: «Wasting resources causes a lot of garbage…».
- **c43 contexto de la situación:** decía «Se tutean», pero fr.n4.c06 fija que Ana y Karim se tratan de vous (y N2: Emma y Karim se tutean). Ahora: «Emma y Karim se tutean; Ana y Karim se tratan de vous». El diálogo ya era compatible (Karim se dirige a las dos con «Écoutez»).
- **c43 e5 (relacionar):** «recycler — reutilizar materiales» se confundía con «le gobelet réutilisable». Ahora «convertir materiales usados en materiales nuevos» / «to turn used materials into new ones» (par y feedback).
- **c44 p3 (es):** «Je vous le confirme (te lo confirmo)» → «(se lo confirmo)», coherente con vous.
- **c45 situación, línea 2:** «la fête de village où ma grand-mère et moi, nous sommes allés» (où con aller à un evento: incorrecto en registro cuidado) → «la fête de village à laquelle ma grand-mère et moi, nous sommes allés, près de Lyon» (traducción es ajustada: «a la que fuimos»). Además modela preposición + laquelle, que la ficha pide.
- **c45 s1 feedback:** reescrito (era una cita recortada que no respondía a la pregunta): el baile fue por la noche, el día de la fiesta del pueblo.

## Sin cambios (revisado y correcto)

- Gramática de cada ficha: alors que / tandis que + indicativo, à la différence de / contrairement à, on a l’habitude de, il est de tradition de (c41); par conséquent, c’est pour ça que, si bien que + indicativo, provoquer / entraîner / causer (c42); exiger / demander que + subj., pour que / afin que vs pour / afin de, il faudrait que (c43); n’est-ce pas / non / c’est bien ça, si, repetir el dato (c44); où temporal, cette année-là, todos los relativos (c45). Nada de contenido de c46+ (condicional pasado, bien que, etc. quedan fuera).
- Guías de pronunciación (ü, ö, sh, nasales como «en/an/on», -ent muda, r sonora) y versiones en inglés (zh, «la n no suena»).
- `aceptadas` ya correctas: alors / tandis (c41 g1, e1), n’est-ce pas / non (c44 g1, e1), Si / Mais si (c44 i2, e5), «-là» (c45 i3), órdenes alternativos de los ordenar (c41 e4, c42 i2, c44 e4, c45 e4).
- Pistas de la guiada específicas de cada ítem; glosas de relacionar distintas entre sí en los cinco relacionar.
- Español neutro (departamento, ciclovía, alcaldía, vasos, farolito) e inglés americano (city hall, faucet, party, cell phone no aparece).
- Aviso menor, no bloqueante: el `titulo` de c44 mantiene el espacio normal antes de «?» porque así está en `curriculo/fr/n4.json`; si el integrador lo normaliza a U+202F, conviene hacerlo también en el plan.

## Hechos del reparto confirmados

- Ana escribe a Lucas, su amigo canadiense (se tutean), y le compara la Chandeleur con el carnaval de Ecuador; Ana prefiere el carnaval, que en Ecuador es día festivo (c41). / Ana writes to Lucas, her Canadian friend (they use tu), comparing Candlemas with Ecuador’s carnival; Ana prefers carnival, which is a public holiday in Ecuador (c41).
- En casa de Hugo se acostumbra comer crêpes por la noche con toda la familia (c41); a Léa le gustan las crêpes. / At Hugo’s they usually eat crêpes in the evening with the whole family (c41); Léa likes crêpes.
- Ana lee sobre una ola de calor y sequía en su ciudad y lo comenta con Hugo, que se da duchas cortas y cierra la llave al lavarse los dientes (c42). / Ana reads about a heat wave and drought in her city and talks it over with Hugo, who takes short showers and turns off the faucet while brushing his teeth (c42).
- Karim y los vecinos del barrio de Ana y Emma redactan una petición a la alcaldía para una fiesta de barrio más ecológica; Karim ya clasifica los residuos en su restaurante; Ana y Emma también en casa y firman; Ana y Karim se tratan de vous, Emma y Karim se tutean (c43). / Karim and the neighbors in Ana and Emma’s neighborhood write a petition to city hall for a greener neighborhood party; Karim already sorts waste in his restaurant; Ana and Emma do too at home and sign; Ana and Karim use vous, Emma and Karim use tu (c43).
- La fiesta del barrio (la de la petición) es el 14, a las 20 h, en la rue Lafayette, entrada gratuita y cien invitados; Karim la organiza con los vecinos; Emma (que trabaja con Karim) está en la lista y Ana va con Léa y Hugo; Ana habla por teléfono con la secretaria del restaurante de Karim y se tratan de vous (c44; no es la apertura del segundo restaurante de c06). / The neighborhood party (the petition’s one) is on the 14th at 8 p.m. on rue Lafayette, free entrance, a hundred guests; Karim organizes it with the neighbors; Emma (who works for Karim) is on the list and Ana goes with Léa and Hugo; Ana phones the secretary of Karim’s restaurant and they use vous (c44; it is not the opening of the second restaurant from c06).
- Hugo, a los nueve años (verano de 2015, cuando su abuela ya vivía en Lyon), fue con ella a una fiesta de pueblo cerca de Lyon, donde la abuela tiene primos: bailó con una vecina de su edad con quien jugaba todos los veranos, ganó un concurso de disfraces con un traje que le hizo su abuela y vio el desfile con farolitos (c45). / At age nine (summer 2015, when his grandmother already lived in Lyon), Hugo went with her to a village festival near Lyon, where she has cousins: he danced with a neighbor his age he played with every summer, won a costume contest with a costume his grandmother made, and saw the lantern parade (c45).

Coherencia con el reparto previo: abuela de Hugo viva, de Lyon, vuelta allí en 2015, veranos de Hugo en Lyon (N2 B2); Hugo nacido el 14-08-2006 (9 años en 2015); Emma trabaja en el restaurante de Karim y la tutea; Ana y Karim, vous (N2 c26, c29, c30; N4 c06); Lucas canadiense (N1/N2/N3).

## Pendiente

Nada. Archivos tocados: `tools/contenido/ruta-fr/n4-b09.json` y este informe. Palabras francesas eliminadas: «l’inauguration» (c44, solo vocabulario y 3 usos); «Canada» ya no aparece en c41, pero es léxico anterior. Ningún bloque posterior depende de ellas.
