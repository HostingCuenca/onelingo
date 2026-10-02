# Revisión N4 · B7 (fr.n4.c31–c35) — «Personalidad, deportes y ocio»

GO

Revisor independiente. Validación final: `python3 tools/validar_ruta.py fr --borrador n4-b01.json … n4-b07.json` (sin los borradores n3, ya integrados) → **0 errores**. `python3 tools/curriculo/validar_plan.py fr` → 0 errores y ningún «título de la unidad difiere» para fr.n4.c31–c35.

## Qué se comprobó

- Las 5 unidades enseñan exactamente lo que dicen sus fichas (títulos, objetivos, `gramatica`, `introduce`, `recicla`, vocabulario de la ficha más palabras de apoyo, tarea). No hay nada de clases posteriores: pourvu que solo en c34 (y c34 usa el subjuntivo irregular ya visto en N3), n’importe / nulle part solo en c33, comparativos del adverbio solo en c32.
- El plan de ejercicios está completo: misma secuencia de formatos y misma clave en guiada, independiente, situación (2 ítems) y evaluación en las 5 clases (comprobado por script). Cambios de redacción permitidos: los `escribir` de la práctica independiente pasan de «describe libremente» a una traducción con `respuesta` y `aceptadas`; en c34 el par «quelle performance ! — admirar» de `relacionar` se sustituyó por «pourvu qu’on gagne ! — desear con inquietud» y g5 usa «Tu as gagné le match». Son pulidos válidos (mismo formato y clave).
- Anatomía: explicación → tablas → 8 ejemplos con audio → vocabulario → guiada (5, con `pista`) → independiente (4, sin `pista`) → situación (texto de 156–176 palabras, dentro de 150–250; hablantes con nombre o «La journaliste») → evaluación con 5 ítems puntuables + 1 `escribir` `abierta: true` que no cuenta (≥ 4 puntuables, 4–5 formatos). `erroresFrecuentes` 4 por clase. Todos los formatos del bloque se usan.
- Tipografía: U+202F antes de ? ! : ; y apóstrofo ’ en todo el texto francés (los títulos con espacio normal coinciden con los del plan y con la convención de N3 publicado). Español neutro (departamento no aplica; estacionar, hincha, bloqueador solar, salvavidas, ustedes) e inglés americano sin desvíos.
- Guías de pronunciación: nasales an/en/in/on, j/g = «sh», ü/ö, sin «y/j»; todas las notas revisadas.

## Correcciones aplicadas (clase, ítem, antes → después)

### c31 Trop timide pour…
- Diálogo [5] (Léa) y modelo de e6: «Moi, je n’ai pas assez de patience pour être arbitre» / «Léa n’a pas assez de patience pour être arbitre» → «Moi, je suis trop gentille pour être arbitre» / «Léa est trop gentille pour être arbitre». Motivo: contradice a N3 (hechos del reparto: Léa se parece a su madre, paciente y seria; generosa con sus amigos). Se conserva la estructura trop + adjetivo + pour. «patience» sigue enseñada en ejemplos y ejercicios con «je» sin personaje.
- i4 (escribir): se añade en `aceptadas` «Hugo est trop timide pour parler et a tendance à rester dans son coin.» (sin repetir il).
- e5 (relacionar), glosa EN de renfermé: «doesn’t share much about himself» → «shares little about themselves».
- Error frecuente «Elle a l’air fatigué»: la explicación decía que era incorrecto; en Francia el accord con el sujeto es lo habitual pero la forma invariable también se admite → se reformula como «la forma que se espera en este nivel».

### c32 Il court plus vite que moi
- Diálogo [0]: la traducción omitía «Il fait chaud» → «Hace calor y los hinchas están ahí» / “It’s hot and the fans are there!”.
- Diálogo [5] y [6]: «le score est de cinq à cinq» + «Léa bat Hugo, six à quatre» era imposible en un set de tenis → «le score est de quatre à quatre» (es/en actualizados); 4–4 y 6–4 son coherentes.
- Ejemplo «L’adversaire joue le moins calmement»: traducción ES «El adversario juega con menos calma» (leída como comparativo) → «El adversario es el que juega con menos calma» (superlativo); EN igual.
- i4: `aceptadas` ampliadas con «Hugo court plus rapidement que Léa.» y «… qu’elle.» (formas válidas con -ment, ya enseñadas en p6).
- p1: «Los adverbios en -ment se forman con el femenino» → «… en general …» (hay excepciones: évidemment, etc.). EN igual.

### c33 Quelque part, nulle part
- Diálogo [2] (Emma): «il n’y a nulle part de salle ouverte tard» (poco natural) → «on ne trouve nulle part un karaoké ouvert tard près de chez nous» (es/en actualizados).
- Diálogo [3] (Hugo): «… garer le vélo là-bas non plus» (referente confuso) → «Léa, il n’y a nulle part pour garer le vélo près de ton escape game.»; así la objeción se resuelve con Hugo [7] («près de la gare, il y a de la place») y el resto del chat.
- Diálogo [5] (Léa) y ejemplo p7 / fila `partout` de la tabla p4: «un escape game partout en ville» (singular absurdo) → «des escape games, il y en a partout en ville» (usa y/en de N3; «escape» sigue enseñado en un ejemplo, requisito del validador).
- Diálogo [9]: traducción «a las quince horas» → «a las 15 h».
- Vocab `nulle part`: la nota decía «las dos l suenan» (es una sola l) → «la e final no suena y la r final sí» (es/en).
- i4: `aceptadas` + «Il n’y a nulle part ici pour louer un kayak.».

### c34 Pourvu qu’on gagne !
- `vas-y`: «¡dale!» (no neutro) → «¡adelante, tú puedes!»; ejemplo «Vas-y, Hugo !» → «¡Adelante, Hugo!»; diálogo [2] igual.
- «fútbol sala» (España) → «fútbol de salón (futsal)» en contexto y traducción del diálogo [0].
- Diálogo [11]: terminaba con «Je vais applaudir très fort !» después del partido (incoherente) → la frase pasa al diálogo [2] (antes del partido) y el cierre es «À ce soir, Hugo ! Allez, courage !».
- Diálogo [6]: «médaille...» → «médaille…» (puntos suspensivos tipográficos).
- Nota EN de médaille: “may-DY” → “may-DYE”.

### c35 C’est dangereux de nager ici
- p2 (es/en) y pista de g3: «la cosa es el sujeto del infinitivo» (incorrecto: es el sujeto de la frase y el complemento implícito del infinitivo) → «el sujeto de la frase (es lo que se comprende, se hace o se ve)».
- Error frecuente 1: la explicación («como en “es peligroso de…”, pero en español se omite»; EN «English drops it») era confusa → «en español no hace falta preposición («es peligroso nadar»), pero en francés sí» / “English says ‘dangerous to swim’, but French needs de”.
- Nota de `le drapeau rouge`: mezclaba «sh» y «ruzh» → «rush» con la explicación de ou y g suave (es/en).
- Traducciones ES «cuando la bandera es roja» → «cuando la bandera está roja» (ejemplos, diálogo, ítems).
- i4: `aceptadas` + «C’est agréable à voir, la plage.».

No se eliminó ni renombró ninguna palabra francesa enseñada (todas las listas de `vocabulario` están intactas; solo cambian frases de diálogo y un ejemplo). Palabras usadas ahora y ya conocidas: «gentille» (c31), «des escape games, il y en a» (c33).

## Hechos del reparto confirmados

- Léa propone un equipo de voleibol de barrio para jugar los domingos: Ana es la capitana (ambiciosa, tiende a querer organizarlo todo), Emma anima al equipo (sociable), Hugo juega al centro (tímido, nervioso pero con energía) y Léa anota los puntos porque es demasiado amable para ser árbitro (c31). / Léa suggests a neighborhood volleyball team to play on Sundays: Ana is captain (ambitious, tends to want to organize everything), Emma livens up the team (sociable), Hugo plays in the middle (shy, nervous but energetic) and Léa keeps score because she is too nice to be a referee (c31).
- Hugo y Léa juegan un sábado la final de tenis del torneo de barrio: Hugo corre más rápido, Léa saca más fuerte, entrena más regularmente y juega mejor bajo presión; Hugo pierde el primer set, gana el segundo y Léa gana el último (6–4 tras 4–4); el próximo torneo es dentro de un mes (c32). / Hugo and Léa play the final of the neighborhood tennis tournament on a Saturday: Hugo runs faster, Léa serves harder, trains more regularly and plays better under pressure; Hugo loses the first set, wins the second and Léa wins the last one (6–4 after 4–4); the next tournament is in a month (c32).
- Ana, Emma, Hugo y Léa planean una salida el sábado: acaban eligiendo el bowling cerca de la estación a las 15 h, el karaoke queda para otro día y Hugo propone kayak el domingo; Hugo va en bicicleta, Emma casi nunca trabaja los domingos y Ana no trabaja ese sábado (c33). / Ana, Emma, Hugo and Léa plan a Saturday outing: they settle on bowling near the station at 3 p.m., karaoke is postponed and Hugo suggests kayaking on Sunday; Hugo goes by bike, Emma almost never works Sundays and Ana is not working that Saturday (c33).
- Hugo juega un torneo de futsal con su equipo; Léa y Emma van a verlo, pierden 3–2, Hugo mete un buen gol, Ana lo consuela y lo invita a cenar esa noche (c34). / Hugo plays in an indoor soccer tournament; Léa and Emma come to watch, they lose 3–2, Hugo scores a good goal, Ana comforts him and invites him to dinner that evening (c34).
- Ana, Léa y Hugo pasan un día en una playa de Bretagne (bandera roja, marea que sube, camping cercano); Léa y Hugo le explican a Ana las normas del cartel (c35). / Ana, Léa and Hugo spend a day at a beach in Brittany (red flag, rising tide, nearby campsite); Léa and Hugo explain the rules on the sign to Ana (c35).

Coherencia comprobada con N2–N3 y con los otros borradores N4: Léa paciente (N3) ya no se contradice; Hugo en bicicleta y sin auto (N1–N2, c37 b08 alquila uno); Ana no trabaja los domingos y a veces los sábados (N2), Emma trabaja el sábado por la noche (b02) y rara vez el domingo (N2), por eso las citas son el sábado a las 15 h y el domingo de día; Karim y el restaurante no aparecen. El viaje de c36 a Bretagne es otro viaje, posterior y con Emma: no choca con el día de playa de c35.

## Sin resolver / observaciones (no bloquean el GO)

- c34: el texto de la situación tiene 156 palabras (la ficha dice «unas 170»); está dentro del rango 150–250 de N4, pero sin margen.
- Hugo «trop timide pour être capitaine» (ficha) convive con su papel de organizador de fiestas y de proponer la colecta (N3): se acepta, porque lo tímido es liderar un equipo, y N3 lo describe como «muy serio».
- «Elle a l’air fatigué» / «fatiguée»: ambas formas existen en Francia; el bloque enseña (y evalúa) la concordancia con la persona, que es la que pide el nivel.
- Las explicaciones de sonido ü/ö aparecen en las notas de vocabulario de c32–c35 sin redefinirse (se definen en la nota de pronunciación de c31, la primera del bloque, y en el propio texto de las notas); no se tocó.
