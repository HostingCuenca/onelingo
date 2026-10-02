# Revisión de N6 · B4 (fr.n6.c16–c20)

GO

Revisado por un agente distinto del autor. Validación: `python3 tools/validar_ruta.py fr --borrador n5-b01…n5-b10 n6-b01…n6-b04` → 0 errores con mi última edición (modo de vocabulario estricto activo). Después apareció en el validador una regla nueva (el modelo de un `escribir` abierto debe tener ≥ `minimoPalabras`) que da 17 errores en ítems de N4, N5, n6-b01, n6-b02 y n6-b03; **ninguno en fr.n6.c16–c20** (mis cinco modelos tienen 31, 23, 41, 28 y 28 palabras frente a mínimos de 25, 20, 30, 25 y 25). `python3 tools/curriculo/validar_plan.py fr` → 0 errores y ningún «título de la unidad difiere» para fr.n6.c16–c20. Encadenando también n6-b05…n6-b10 solo aparecen errores propios de c48 (otro bloque); ninguna palabra que quité de este bloque la usa un bloque posterior.

Comprobado sin cambios necesarios: cada clase enseña lo que dice su ficha (título, objetivo, gramática, introduce/recicla, vocabulario de 8–10 palabras, tarea) y contiene los ejercicios del plan (mismo formato y clave); situación de 304–344 palabras (rango N5–N7: 300–500) coherente con sus ítems de comprensión; hablantes con nombre o papel en francés; tipografía (U+202F antes de ? ! : ; y apóstrofo ’); guías de pronunciación (ü y ö definidas en c16, nasales como «en», «sh»); español neutro de América y inglés americano; los `escribir` abiertos no cuentan. Los ordenar con fichas de varias palabras siguen la convención de N5.

Cada clase tiene **5 ítems puntuables** en la evaluación (más 1 `escribir` abierto que no puntúa) y ≥ 4 formatos distintos entre ellos:

| Clase | Puntuables | Formatos |
|---|---|---|
| c16 | e1–e5 | completar, elegir, escuchar, relacionar |
| c17 | e1–e5 | elegir, completar, escuchar, ordenar |
| c18 | e1–e5 | elegir, completar, escuchar, ordenar |
| c19 | e1–e5 | elegir, completar, escuchar, relacionar |
| c20 | e1–e5 | elegir, escuchar, ordenar, completar |

## Correcciones de reparto (obligatorias, punto 12)

- c20 (todo): **Madame Dubois → Madame Lefort** (diálogo, hablante, contexto es/en; los ítems s1/s2 no la nombran). Contexto: «Madame Lefort, su vecina, vive en el departamento de abajo; con ella tienen un acuerdo: nada de ruido después de las 22 h» (coherente con el acuerdo de N5 c40). Su primera línea ahora incluye «Il est dix heures passées.» y se quitó «à minuit» de la línea de Hugo para no contradecir ese acuerdo. Dubois ya no aparece en c20.
- c17: el director es hombre (Le directeur, vous). Ejemplo «avec la directrice» → «avec le directeur» (es: «con el director»); contexto es/en («por correo al director del hotel»); diálogo: «Madame la directrice, …» → «Monsieur le directeur, …»; hablante «La directrice» → «Le directeur»; «Je suis navrée» → «Je suis navré»; respuesta de Ana «Madame» → «Monsieur» (es «señor», en «sir»); tabla «a una jefa» → «a un jefe».
- c16–c17: Madame Dubois queda como amiga y antigua casera que vive cerca; c17 lo aclara en el contexto («su amiga y antigua casera que vive cerca») y es quien cuida el gato.

## Correcciones (clase, ítem: antes → después)

**c16**
- p1, tabla p3 (fila 3), tabla p3c (fila condicional), ejemplos p5, g3, e2, diálogo Hugo y Ana: «il me semblerait que» iba con indicativo («le sujet est délicat», «a été», «c’est plus sûr», «l’accueil était»), contra N5 b07 (y la tarjeta de audio i3, que ya traía «soient»), donde il semblerait que + subjuntivo → «le sujet soit délicat», «ait été», «ce soit plus sûr», «l’accueil soit». Se añadió una nota en p1 y p3c (es/en) de que lleva subjuntivo.
- Diálogo Madame Dubois: «Mais ce n’est pas à moi d’en juger, sauf erreur de ma part» (el atenuador no tenía sentido ahí) → «Mais ce n’est pas à moi d’en juger. Sauf erreur de ma part, sa mère est médecin, et chacun fait comme il veut avec son salaire.» (es/en ajustados).
- Diálogo Madame Dubois: «…soient d’accord, éventuellement les gens de ma génération» (uso incorrecto de éventuellement) → «On pourrait éventuellement garder cinq places, mais moi, je prends la voiture…» (es/en ajustados).
- Tarjeta «à mon humble avis»: guía de pronunciación sin el enlace de mon + humble → «a mon-nen-bl a-vi» (es) / «ah mohn-NUHN-bl ah-VEE» (en).

**c17**
- Traducción es de «demander si»: «Quería pedirle si podía…» → «Quería preguntarle si podía…» (ejemplo 1, diálogo Ana–director y Ana–cliente).
- Tabla p3b: «Pourriez-vous me rendre une faveur ?» (rendre una faveur = devolver un favor) → «Pourriez-vous me faire une faveur ?»; etiqueta «a un amigo» → «a un conocido» (es), «to an acquaintance» (en), porque se usa vous.
- Diálogo, respuesta de Ana al director: «Très bien, c’est parfait.» (ella pedía salir a las 18 h y le dan las 20 h) → «Très bien, je comprends.» (es «entiendo», en «I understand»).
- Explicación p2 (en): coma que faltaba («…do something, you already know merci de…»).

**c18**
- Tabla p3b: el título «Cuatro rechazos con alternativa» (tiene 5 filas y solo una con alternativa) → «Cinco formas de rechazar» / «Five ways to decline»; texto: «Algunas llevan una alternativa en condicional (je serais libre dimanche).»
- Ejemplo «Je ne suis pas vraiment libre samedi.» (es): «No estoy realmente libre…» (calco) → «No estoy del todo libre el sábado.»
- s2: «…mais j’ai un autre dîner.» → «…mais j’ai un dîner de famille.» (idéntico a lo que dice Léa en el diálogo).

**c19**
- ErrorFrecuente 3 («Nous avons un petit souci léger» → «un léger souci»): no era un error defendible (el adjetivo pospuesto existe). → «Le service laisse que désirer.» → «Le service laisse à désirer.» (explicación es/en: no calcar «dejar que desear»).
- Diálogo de Emma: «c’est un reproche qu’ils vont écouter» → «c’est une demande qu’ils vont écouter» (es «una petición», en «a request»; el punto es que la petición queda clara).
- i4 (escribir): `aceptadas` ampliada con «Ce n’est pas terrible, j’aurais aimé être prévenue.», «Ce n’était pas terrible. J’aurais aimé être prévenue.» y el orden inverso «J’aurais aimé être prévenue. Ce n’est pas terrible.»

**c20**
- Madame Dubois → Madame Lefort (ver arriba).
- Vocabulario «la gêne»: la guía «la shen» se leía como nasal (en la convención de este curso «en» es nasal) → «la shèn» y se avisa de que la n sí suena (es/en).
- g5 y e5 (completar «peut-être»): `aceptadas` + «peut être». i2 (completar «serait-il»): `aceptadas` + «serait il».
- Explicación p1 (es): «algo en que no había pensado» → «algo en lo que el otro no había pensado».
- Explicación p2: se quitó la referencia a c22 (la inversión tras peut-être) para no adelantar contenido; «Un buen anfitrión, o una buena invitada, es discreto: se cuida el tacto…» (concordancia y sentido) → «Un buen anfitrión y una buena invitada son discretos: tienen tacto y a veces deben prendre sur soi («contenerse»).» (es/en).
- Contexto es: «piso de abajo» → «departamento de abajo» (punto 7).

## Hechos del reparto confirmados

- Léa celebra una fiesta de cumpleaños y su madre, Sophie, le regaló un reloj de casi 600 € / Léa has a birthday party and her mother, Sophie, gave her a watch costing almost €600 (c16; coherente con Sophie médica y con Léa estudiante).
- Madame Dubois, antigua casera que vive cerca, asiste a la fiesta, toma el auto para ir al mercado y no ve bien la ciclovía / Madame Dubois, the former landlady who lives nearby, attends the party, drives to the market and is skeptical about the bike lane (c16; coherente con N3 auto pequeño y N5 mercado del sábado).
- Hugo va en bicicleta todos los días y un amigo suyo le pidió prestados mil euros / Hugo bikes every day and a friend asked him to lend a thousand euros (c16; coherente con N1–N2).
- La alcaldía quiere quitar diez estacionamientos para hacer una ciclovía en el barrio, y una vecina de la calle de Madame Dubois no habla con su hermano por una herencia / The city wants to remove ten parking spaces for a bike lane in the neighborhood, and a neighbor on Madame Dubois’s street no longer speaks to her brother over an inheritance (c16; hechos de fondo, sin conflicto).
- Ana tiene un gato (Madame Dubois también tiene uno, N2 c41) y Madame Dubois se lo cuida el sábado / Ana has a cat (Madame Dubois also has one, N2 c41) and Madame Dubois looks after it on Saturday (c17; hecho nuevo).
- Ana trabaja el sábado en el hotel; el director (hombre, vous) le deja salir a las 18 h solo parcialmente: propone terminar a las 20 h por un grupo grande, y ella puede salir antes el viernes / Ana works Saturday at the hotel; the director (a man, vous) offers an 8 p.m. finish because of a large group and lets her leave early on Friday (c17; coherente con N2 c01 y N5 «director»).
- Ana hace firmar un formulario a un cliente del hotel y pide el asiento a un desconocido en el metro, y se lo cuenta a Emma esa noche / Ana has a hotel guest sign a form, asks a stranger on the subway for his seat, and tells Emma that night (c17).
- Emma invita al grupo a una cena el sábado a las 20 h (pasta y pastel de chocolate); Ana acepta, Léa tiene una cena familiar y propone un té el domingo a las 16 h, Hugo tiene que trabajar en su mémoire y propone almorzar el domingo, que Emma pasa al lunes a mediodía / Emma invites the group to a Saturday 8 p.m. dinner (pasta and chocolate cake); Ana accepts, Léa has a family dinner and proposes tea on Sunday at 4, Hugo must work on his mémoire and proposes lunch on Sunday, which Emma moves to Monday at noon (c18; coherente con Hugo en el máster y Emma de N2 c01).
- Ana coordina un evento en el hotel y una agencia de eventos falla el montaje de la sala (cien invitados, retraso sin aviso); Ana y Emma (se tutean) reescriben la queja con tono suave y Ana la firma «Cordialement, Ana» / Ana coordinates an event at the hotel and an events agency botches the room setup (a hundred guests, an unannounced delay); Ana and Emma (who use tu) rewrite the complaint in a gentler tone and Ana signs it “Cordialement, Ana” (c19; coherente con Ana coordinadora en N5–N6).
- Ana y Emma dan una fiesta en su departamento nuevo; Madame Lefort (vecina de abajo, vous, duerme mal, acuerdo de convivencia de las 22 h) pide pasadas las diez que bajen la música; un invitado fuma en el balcón, hay celulares en la mesa y una invitada se queda pasada la medianoche; asisten Hugo y Léa / Ana and Emma throw a party in their new apartment; Madame Lefort (downstairs neighbor, vous, sleeps badly, 10 p.m. agreement) asks them after ten to turn the music down; a guest smokes on the balcony, phones are on the table and a guest stays past midnight; Hugo and Léa attend (c20; coherente con N5 b08 y el punto 12).

Tratamientos confirmados: Ana–Madame Dubois, Ana–director, Ana–cliente/desconocidos y Ana–Madame Lefort con vous; Ana–Emma/Hugo/Léa y Emma–Léa/Hugo con tu; Hugo trata de vous a Madame Dubois y a Madame Lefort.

## Sin resolver

- Nada bloqueante. Aviso para otros bloques: en este bloque «il me semblerait que» va con subjuntivo, igual que en N5 b07 y n6-b09.
