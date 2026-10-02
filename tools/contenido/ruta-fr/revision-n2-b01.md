# Revisión independiente · N2 francés, bloque 1 (clases 1–5)

- **Archivo:** `tools/contenido/ruta-fr/n2-b01.json` (`fr.n2.c01` … `fr.n2.c05`). Revisor distinto del autor.
- **Validador:** `python3 tools/validar_ruta.py fr --borrador tools/contenido/ruta-fr/n2-b01.json` → **0 errores**; encadenado con `n2-b02.json` y `n2-b03.json` → **0 errores** (repetido tras los últimos cambios).
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 errores, 10 avisos conocidos; ningún aviso «título de la unidad difiere» para fr.n2.c01–c05.
- **Comprobación propia de vocabulario nuevo** (palabras de pasos de enseñanza, ítems y diálogos que no estaban en Fundamentos ni en N1): solo las de las fichas (frecuencia, verbos en -re, partir / sortir / dormir, commencer, pendant / avant / après, savoir / connaître, léxico de oficina, estudios y puesto). Nada de c06–c50. Tipografía: U+202F antes de ? ! : ; y 0 apóstrofos rectos en el francés.
- **Longitud de la situación:** c01 10 líneas (102 palabras), c02 8 (89), c03 8 (105), c04 8 (89), c05 8 (93): dentro de lo pedido para N2 (6–10 líneas, ≈ 80–120 palabras).

## Veredicto

GO

## Contraste con las fichas

Los títulos, objetivos, gramática y vocabulario coinciden con `curriculo/fr/n2.json`:

- **c01:** toujours / souvent / parfois / rarement / ne… jamais después del verbo conjugado, tous les jours / une fois par semaine / deux fois par mois, d’habitude y en général. No se usa ningún adverbio con passé composé (N1 no lo enseñó). Cada clase mantiene ≥ 4 ítems puntuables con ≥ 2 formatos en la evaluación (6 puntuables y 6 formatos en cada una); el `escribir` abierto (`abierta: true`) no puntúa y se suma aparte.
- **c02:** présent de attendre y de répondre, entendre, vendre, descendre, perdre (singular -s, -s, —; plural -ons, -ez, -ent), répondre à y attendre sin preposición. La guía de la d final es exacta (il attend «a-tan» / ils attendent «a-tand»).
- **c03:** partir, sortir, dormir con las dos raíces; partir de / sortir de + lugar (du, de la, de l’); commencer à / finir à + hora; asignaturas.
- **c04:** pendant + duración, avant / après + sustantivo sin de, de… à…, contraste depuis / pendant. El passé composé de los ejemplos con pendant (a travaillé, a joué) y «hier» ya se enseñaron en N1 (c46, c47, c48); es repaso, no gramática nueva.
- **c05:** savoir + infinitivo / que / interrogativo; connaître + persona, lugar o cosa; conjugación completa de ambos, con el circunflejo de il connaît; contraste savoir / pouvoir (reciclaje de la ficha).

**Extras del autor que se mantienen** (no figuran en las listas de la ficha, pero la ficha los exige): **durer** (c04; el objetivo es «decir cuánto dura cada actividad»; se enseña con tarjeta, tabla y ejemplos) y la tabla de **commencer** (c03; la ficha pide «commencer à / finir à + hora»).

## Cambios aplicados (clase · ítem · antes → después)

### Coherencia del reparto

1. **c01 · situación, línea de Hugo.** «Oui, j’étudie souvent le soir. En général, je finis à dix heures.» chocaba con c03, donde Hugo termina las clases a las cinco → «Oui, j’étudie souvent le soir à la maison. En général, je finis à dix heures.» (es / en con «en casa» / “at home”). Ahora es coherente: clases hasta las cinco (c03), estudio en casa hasta las diez, se acuesta a las once (c03) y duerme ocho horas.
2. **c01 · patrón, ejemplo 3.** «Hugo prend parfois le métro.» contradecía a Hugo (va siempre en bicicleta: «je prends toujours mon vélo» en la situación y el reparto) → «Léa prend parfois le métro.» («Léa a veces toma el metro» / “Léa sometimes takes the subway”).
3. **c03 · ejemplo «À midi, Hugo prend un sandwich à la cantine».** Hugo es universitario → «À midi, Ana prend un sandwich à la cantine de l’hôtel.» (la cantine queda como comedor de una empresa; Ana almuerza en el hotel donde trabaja por la tarde).
4. **c03 · situación (Léa y Hugo).** «Tu vas à la cantine à midi ?» (cantina de la escuela) → «Tu vas au resto U à midi ?» («¿Vas al comedor universitario al mediodía?»). El contexto pasa a «dos estudiantes de la universidad» / “two university students”.
5. **c03 · vocabulario.** Nueva tarjeta **le resto U** («el comedor universitario»; guía «lö rès-to ü», la U se dice ü) en `vocabulario` de la unidad y en el paso de tarjetas. La tarjeta de **la cantine** pasa de «el comedor (de la escuela)» a «el comedor (de una empresa o un colegio)» y su nota explica que en la universidad se dice «le resto U».
6. **c03 · patrón, ejemplo 2.** «Hugo sort de l’école à midi.» (Hugo es universitario) → «Ana sort de l’école à midi.» (Ana estudia francés por la mañana en la escuela de idiomas).

### Corrección y claridad

7. **c04 · explicación p1.** «En francés pendant es lo normal» era excesivo (el francés también omite pendant: «J’ai travaillé deux heures») → «en francés conviene decir pendant»; el inglés ahora dice que se usa «for» o se omite («I worked two hours»).
8. **c04 · tabla depuis / pendant.** Decía «pendant: la duración ya terminó», lo que contradecía la clase (rutina: «Je travaille pendant deux heures, puis…») → «pendant: una duración cerrada (terminó, es una rutina o un plan); para el pasado, con passé composé»; columnas «depuis: sigue hoy» / «pendant: duración cerrada» (es / en).
9. **c04 · situación, s2.** «¿Qué hace Monsieur Martin antes de la reunión?» tenía dos respuestas válidas (tiene su clase y responde a los correos, ambos antes de la reunión) → «¿… después de la reunión?»: Tiene la pausa del almuerzo / Responde a los correos / Tiene su clase (una sola, «Après la réunion, c’est la pause déjeuner»); feedback reescrito.
10. **c04 · ejemplo 7.** «La pause déjeuner dure une demi-heure.» (ya está en la tabla de durer y en el diálogo) → «Le stage de Hugo dure trois mois.» Así **le stage**, que estaba en la ficha pero no aparecía en ninguna frase, se usa con durer y encaja con la pasantía de Hugo.
11. **c05 · explicación p2 (es).** «ö es la e muda (je = «sö»)» → «je = «shö»» (la j se escribe «sh»; el inglés ya decía “zhö”).
12. **c05 · situación, s2 (feedback).** Citaba «je connais bien la responsable… elle a de l’expérience» y Ana nunca dice «je connais bien la responsable» → cita exacta «Elle a de l’expérience : elle sait tout !».
13. **c03 · práctica independiente i1 (aceptadas).** «Salgo de casa a las siete» admite también «chez moi» (enseñado en N1 c42): + «Je pars de chez moi à sept heures.», «Je sors de chez moi à sept heures.», «À sept heures, je pars / je sors de chez moi.».

### Guías de pronunciación (regla 6, inglés)

14. **c02, c03, c04, c05 · explicación de pronunciación (en).** Faltaba avisar de que la n de las nasales no suena: se añade «In nasal vowels (an, on / an, en) the n is not pronounced: do not close your mouth on it.» **c04 · tarjeta pendant (en):** + “(the n only colors the vowel)”. El resto de las guías (sh para j y g suave, in = «en», an / on, ü, ö, consonantes finales de toujours, attend / attendent, partons / partent, sais / savent) estaban bien; ü y ö se definen en c01 y se recuerdan en cada clase.

## Revisión punto por punto

1. **Francés de Francia.** Adverbios después del verbo conjugado y ne… jamais sin pas; tous con plural; verbos en -re sin -t en la tercera persona; partir / sortir / dormir (je pars, il part, ils partent); partir de / sortir de con du, de la, de l’; avant / après sin de; du lundi au vendredi; pendant con passé composé; savoir + infinitivo / que / où, connaître + objeto directo, il connaît con circunflejo. Correcto.
2. **Explicaciones es / en.** Claras y cortas; es con tú y léxico neutro (computadora, ustedes, pasantía, comedor); en compara con el inglés donde ayuda (orden del adverbio, «wait for» / «answer», «to know»).
3. **Respuesta única y `aceptadas`.** Revisados todos los `ordenar` (adverbio o expresión de frecuencia al inicio o al final; en général al principio, al final o tras el verbo), `completar` con `opciones`, `escribir` (femenino de client en c02 e5, le / la responsable en c05 i2) y `escuchar`.
4. **Pistas y relacionar.** Cada pista ayuda a su ítem; las glosas de los pares son distintas (attendre esperar / répondre responder / entendre oír; matière frente a asignaturas concretas; quart = 15 min / demi = 30 min; poste puesto / tâche tarea / accueil recepción).
5. **Hablantes.** Solo nombres del reparto (Ana, Hugo, Léa, Chloé) o «Monsieur Martin»; nunca en español.
6. **Diálogos y cortesía.** Tuteo entre amigos (Ana–Hugo, Léa–Hugo, Léa–Ana) y vous con Monsieur Martin (Ana, Chloé); los diálogos modelan el objetivo de cada clase.
7. **Anatomía.** Explicación → tablas / patrones → ejemplos (8) → tarjetas → guiada (5) → independiente (4) → situación (2 ítems) → evaluación (6 + 1 abierto). 3 `erroresFrecuentes` por clase.

## Hechos del reparto confirmados

- Ana vive en París y lleva un año allí: estudia francés por la mañana en la escuela de idiomas (c01, c02) y trabaja por la tarde en la recepción de un hotel (c01, c02, c03 «Ana part de l’hôtel à six heures», c05). / Ana lives in Paris and has been there a year: she studies French in the morning at the language school and works afternoons at a hotel front desk.
- Ana no trabaja los domingos, a veces los sábados; toma el metro o el bus y almuerza en la cantina del hotel (c03). / Ana does not work Sundays, sometimes Saturdays; she takes the subway or bus and has lunch in the hotel cafeteria.
- Hugo es estudiante universitario en París y va siempre en bicicleta (c01, c03). / Hugo is a university student in Paris and always bikes.
- Hugo: clases de lunes a viernes, empieza a las 8, termina las clases a las 5 (c03), estudia en casa por la noche hasta las 10 (c01), se acuesta a las 11 y duerme 8 horas (c03); hace una pasantía (stage) de tres meses (c04). / Hugo: classes Monday to Friday, starts at 8, classes end at 5, studies at home in the evening until 10, goes to bed at 11 and sleeps 8 hours; does a three-month internship (stage).
- Léa es estudiante universitaria: clases de historia (a las 10) e informática, sale de clase a las 4 y come en el resto U (c03). / Léa is a university student: history class at 10 and computer science, gets out at 4 and eats at the university cafeteria.
- Monsieur Martin es el profesor de Ana, se le trata de vous, tiene clase de 9 a 10:30, reunión a las 11 y pausa del almuerzo de media hora (c02, c04). / Monsieur Martin is Ana’s teacher, addressed with vous; class 9–10:30, meeting at 11, half-hour lunch break.
- Chloé es la secretaria de la escuela y organiza el planning de Monsieur Martin (c04). / Chloé is the school secretary and prepares Monsieur Martin’s schedule.
- Emma trabaja de noche en un restaurante y rara vez trabaja el domingo (c01 i2). / Emma works evenings at a restaurant and rarely works on Sundays.

## Sin resolver (no bloquea)

- No se eliminó ni renombró ninguna palabra francesa que B2 / B3 puedan usar: solo se **añade** «le resto U» y se cambian frases de ejemplo de c01, c03 y c04. Las palabras que dejaron de aparecer en ejemplos (p. ej. «prend un sandwich à la cantine» con Hugo, «Hugo prend parfois le métro») siguen enseñadas en otras partes de B1 y en N1. Comprobado: B2 y B3 validan con 0 errores encadenadas con B1; no usan «cantine», «stage» ni «durer».
- En c03 el modelo del `escribir` abierto (e7) sigue diciendo «À midi, je vais à la cantine»: es un modelo genérico de comedor de empresa o colegio y no puntúa.
- c02 e2 («Vous ___ à un e-mail ?») admite vous singular (de cortesía) o plural: la respuesta es la misma (répondez).

Validación final: 0 errores.
