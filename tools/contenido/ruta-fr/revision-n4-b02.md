# Revisión N4 · B2 (fr.n4.c06–c10)

GO

Revisado contra las fichas de `curriculo/fr/n4.json` (títulos, objetivos, gramática, introduce/recicla, vocabulario, situación 45, tarea y plan de ejercicios), la `nota` del nivel, el reparto de N1–N3, `ENCARGO_RUTA_FR.md` (Por nivel N4 y Calibración 1–10) y `ESQUEMA_CONTENIDO.md`. Las 5 unidades enseñan exactamente lo que dicen sus fichas, no usan nada de clases posteriores (se buscó pour que, bien que, jusqu'à ce que, sans + infinitivo, ne… ni…, alors que, ce dont, il me semble que, etc.: ninguno aparece) y contienen los ejercicios planificados (mismo formato y clave; redacción pulida). Cada unidad tiene 8 ejemplos, 9–12 palabras de vocabulario, tres errores frecuentes, 5 ítems de guiada con pista, 4 independientes, 2 de comprensión y 6 de evaluación (5 puntuables en ≥ 3 formatos + 1 `escribir` abierto que no puntúa). Diálogos de 158–183 palabras (rango 150–250). Los seis formatos se usan a lo largo del bloque. Hablantes: nombres propios, nunca en español.

Validación: `validar_ruta.py fr --borrador n4-b01 … n4-b10` (sin los n3, ya integrados) → 0 errores; también con n4-b01+b02 solo. `validar_plan.py fr`: sin «título de la unidad difiere» para fr.n4.c06–c10.

## Correcciones aplicadas (clase, ítem: antes → después)

**c06**
- `v-voeux` nota (es/en), tablas p4/p5/p6 (títulos y columnas es): tipografía francesa, espacio normal antes de « ! » y « : » → U+202F.
- Situación, línea 3 de Ana: «Elle travaille ce soir au premier restaurant» → «… samedi soir …» (con «ce soir» parecía otra noche que la de la fiesta, que es el sábado); traducciones es/en ajustadas («El sábado por la noche…» / «on Saturday night»).
- Situación, traducción en de Karim: «turns out good» → «turns out well».
- e2, feedback: «con bien, futuro simple» (no explicaba nada) → «Espérer que + indicativo (no subjuntivo): futuro simple, tu dormiras.».

**c07**
- Español neutro de América: «el máster» → «la maestría» (vocabulario `v-master`, contexto de la situación y dos traducciones del diálogo). «Licenciatura» se mantiene.
- Tabla p5 (columnas es) y explicación p3 (es/en): U+202F antes de « : » y « ; » en los ejemplos franceses.

**c08**
- Explicaciones p2 y p3 (es/en): « Dommage ! » y « temps ! » con U+202F (en la versión inglesa faltaba el espacio fino).
- Tabla p6, fila «il y avoir» (forma inexistente) → «il y a» (el ejemplo ya muestra «il y avait»).

**c09**
- Tabla p6: la fila «La fenêtre est fermée. → Apparemment, elle n’a pas pris sa clé.» no tenía relación lógica entre pista y deducción → «La clé est sur la porte. → Apparemment, elle n’a pas pris sa clé.».
- Situación, mensaje de Madame Dubois: «Mon fils est passé ce matin pour prendre mon courrier» contradecía el buzón lleno que ven Ana y Emma → «… pour prendre un livre» (traducciones es/en ajustadas). Su hijo es compatible con «dos hijos» de N2.
- g4: «On ___ que Madame Dubois est partie : sa porte est ouverte» (una puerta abierta no indica que se fue) → «On ___ que quelqu’un est passé : la porte est ouverte.»; consigna es/en ajustada («Parece que alguien pasó por aquí»). Respuesta sin cambio: dirait.
- e2: «Les fenêtres sont ouvertes : quelqu’un ___ entrer» (fenêtre ya no se enseña tras el cambio de la tabla) → «La clé a disparu : quelqu’un ___ entrer.» (respuesta a dû; feedback es/en reescrito).
- i4: la consigna decía «con il doit…» y la respuesta usa «Quelqu’un doit être…» → «con devoir» (es/en).
- Explicaciones p0/p1, título de tabla p3 y feedback de i2: U+202F antes de « : ».

**c10**
- Vocabulario `sans doute`, nota de sonido: decía que la t de doute no suena; sí suena («dut») → «la s de sans no suena, pero la t de doute sí» (es/en).
- `possible`: «la s entre vocales» → «la ss suena «s»». `hasard`: se añade que la r final suena y la d no (CaReFuL).
- Explicación p3: el orden de certeza se presenta como «orden aproximado» y se añade il est possible que junto a il se peut que (no hay una jerarquía estricta entre ambos y peut-être).
- Tabla p4: «il est impossible que» estaba al final de una lista «de menos a más seguro»; pasa a la primera fila y el texto dice «De menos a más probable».
- Ejemplo 5: «la fenêtre est ouverte» → «la porte est ouverte» (es/en), para no dejar la palabra «fenêtre» sin uso después del cambio de c09.
- i1, opción 2 (distractor del falso amigo): «Seguro, sin ninguna duda, que está…» → «Sin duda alguna, está en una reunión.»
- i4: «los atascos» (de España) → «atrapado en el tráfico» (es/en: “stuck in traffic”); la respuesta francesa no cambia.
- e5 (relacionar): «puede que (poco seguro)» y «quizás (mitad y mitad)» eran gradaciones inventadas y casi sinónimas → «puede que (+ subjuntivo)», «quizás (+ indicativo)», «probablemente», «casi seguro»; consigna «con su sentido».

## Revisado sin cambios (para constancia)
- Francés de Francia, concordancias (ravie, inquiète, contente, déçue…), registro (Ana ↔ Karim y Madame Dubois: vous; Ana, Emma, Hugo, Léa: tu), apóstrofo ’ y U+202F en todos los campos franceses.
- `ordenar`: orden único; en c09 g5 se acepta además «Plus tôt, elle a dû partir.». `completar`/`escribir`: aceptadas con «a du», forma femenina/masculina (c07 i4), con y sin artículo (c08 i4).
- Pistas de guiada específicas de cada ítem. Pares de `relacionar` con glosas distintas. Guías de sonido: ü y ö definidos, j/g suave = «sh», nasales «en/an», r final marcada.
- Los ejercicios `escribir` de independiente son traducciones guiadas (una sola frase), más cerradas que el plan; no cambian formato ni clave y están en la tabla de aceptadas.
- Vocabulario adicional necesario para la situación: l’inauguration, les vœux (c06); la licence, le master, à l’étranger (c07); probablement (c10). Declarado en `vocabulario`.
- Ningún cambio retira palabras que usen los bloques n4-b03…b10 (cadena completa de borradores: 0 errores).

## Hechos del reparto confirmados
- Karim abre un segundo restaurante; la inauguración es un sábado: el restaurante abre al público a las 8 de la noche y los amigos llegan hacia las 7. Ana y Karim se tratan de vous. / Karim opens a second restaurant; the opening is on a Saturday: the restaurant opens to the public at 8 p.m. and friends arrive around 7. Ana and Karim use vous.
- Emma sigue trabajando los sábados por la noche en el primer restaurante de Karim; termina su turno a las 9 y va a la inauguración después. / Emma still works Saturday nights at Karim’s first restaurant; she finishes her shift at 9 and goes to the opening afterward.
- Hugo termina la licenciatura y en septiembre empieza una maestría en París (no se va al extranjero); da una fiesta el sábado a las 8 en su casa. / Hugo finishes his bachelor’s degree and starts a master’s in Paris in September (he is not going abroad); he throws a party on Saturday at 8 at his place.
- Léa se preocupa de que Hugo tenga menos tiempo para sus amigos; Ana y Emma se alegran por él. / Léa worries that Hugo will have less time for his friends; Ana and Emma are happy for him.
- Ana no puede ir a Quito al cumpleaños de su abuela (el vuelo es muy caro); su mamá trabaja mucho y no tiene vacaciones para ir a París; Ana y su abuela cantarán juntas por videollamada el domingo. / Ana can’t go to Quito for her grandmother’s birthday (the flight is too expensive); her mother works a lot and has no vacation to come to Paris; Ana and her grandmother will sing together on a video call on Sunday.
- Antes de c11 Ana y Emma siguen viviendo en el edificio de Madame Dubois (ella en la planta baja, ellas arriba); Madame Dubois se va varios días a casa de su hija con su gato. / Before c11 Ana and Emma still live in Madame Dubois’s building (she on the ground floor, they upstairs); Madame Dubois goes to her daughter’s for a few days with her cat.
- Madame Dubois tiene también un hijo (compatible con «dos hijos» de N2): pasó por su departamento y olvidó cerrar la puerta. / Madame Dubois also has a son (consistent with “two children” in N2): he stopped by her apartment and forgot to close the door.
- Lucas (estudiante, de Canadá) tiene exámenes y no responde a los mensajes de Ana durante dos días; Ana le envía un último mensaje. / Lucas (a student in Canada) has exams and doesn’t answer Ana’s messages for two days; Ana sends him one last message.

## Sin resolver
- Nada bloqueante. Nota de coordinación: la tabla de c09 y el ejemplo de c10 ya no enseñan «fenêtre» ni «fermée»; si otro bloque las necesitara, deben aparecer en un paso de enseñanza propio (hoy no hay errores en la cadena completa).
