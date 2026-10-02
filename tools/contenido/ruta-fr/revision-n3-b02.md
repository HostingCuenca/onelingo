# Revisión independiente · N3 francés, bloque 2 (clases 6–10)

- **Archivo:** `tools/contenido/ruta-fr/n3-b02.json` (`fr.n3.c06` … `fr.n3.c10`). Revisor distinto del autor.
- **Validador:** `python3 tools/validar_ruta.py fr --borrador …n3-b01.json …n3-b02.json` → **0 errores** (también encadenando `n3-b03.json` … `n3-b10.json`, tras todos mis cambios).
- **Plan:** `python3 tools/curriculo/validar_plan.py fr` → 0 errores, 10 avisos previos de N1; ningún «título de la unidad difiere» para fr.n3.c06–c10 (comprobé además a mano que títulos y objetivos del borrador son idénticos a los de las fichas).
- **Longitud de la situación** (150–250 palabras, contadas por palabras reales): antes 147 / 154 / 147 / 140 / 146; ahora c06 162, c07 154, c08 169, c09 156, c10 166.
- **Evaluación:** 5 ítems puntuables y 4–5 formatos por clase; el `escribir` abierto (`abierta: true`) se suma aparte. 3 `erroresFrecuentes` por clase.
- **Tipografía:** U+202F antes de ? ! : ; y dentro de «…» en todo el francés (también el que añadí); 0 apóstrofos rectos.

## Veredicto

GO

## Contraste con las fichas

Títulos, objetivos, gramática, `introduce`, `recicla`, vocabulario (las 10 / 9 / 10 / 10 / 8 palabras de cada ficha, con artículo) y tarea coinciden con `curriculo/fr/n3.json`. Los 5 ejercicios guiados, 3 independientes, 2 de comprensión y 6 de evaluación de cada clase están, con el formato y la clave del plan (el autor pulió consignas y completó `aceptadas`, pistas y feedback sin cambiar lo que se evalúa). Se usan los seis formatos en el bloque (relacionar en c06 g5, c08 e5, c09 g4, c10 g5). Nada de c11 en adelante: c09 solo menciona que «que + subjuntivo» llegará más adelante, sin enseñarlo; c10 e6 y las frases con «les a retrouvées» usan la concordancia ya vista en c02. Extras del autor que se mantienen (todos enseñados antes de usarse): `la police`, `sonner` (c06 / c07), `vers`, `marron`, `les papiers`, `le t-shirt` (c08), `l’horreur` (c09), `l’histoire` (c10).

## Cambios aplicados (clase · ítem · antes → después)

### c06
1. **i3 (escribir).** La consigna admitía «J’attendais au feu quand…» (imparfait simple, válido y no aceptado) y no entrenaba la clave → se fija el recurso: «Escribe en francés **con être en train de**: «Estaba esperando en el semáforo cuando pasó una moto»» (en: “Write in French with être en train de: …”).
2. **Situación (147 → 162 palabras).** + «Les voitures attendaient au feu.» (línea 2), + «Tout le monde parlait.» (línea 5), + «Il pleuvait toujours et j’avais froid.» (línea 6); traducciones es / en añadidas. Los ítems s1 / s2 siguen teniendo una sola respuesta.
3. **s2 (feedback).** Citaba «Au moment où le feu est passé au vert, une moto est arrivée» como si fuera literal; el texto dice «… au vert pour les voitures, une moto est arrivée» → cita exacta (es / en).

### c07
4. **s1 (feedback).** Citaba «Quand je suis sortie, le bus était déjà parti», frase que no aparece en el correo → «Je suis sortie très vite, mais le bus était déjà parti» (es / en).
5. **e5 (aceptadas).** «No había oído el despertador» admite también «mon réveil» y «… sonner» → + «Je n’avais pas entendu mon réveil.», «Je n’avais pas entendu le réveil sonner.», «Je n’avais pas entendu mon réveil sonner.».
6. **e6 (modelo abierto).** El modelo tenía 53 palabras (la tarea pide 60–80) y se contradecía («mon téléphone était à plat» pero «j’avais écrit à Chloé») → nuevo modelo de 63 palabras con 3 plus-que-parfait coherentes (réveil, bus, école); rango 50–100 → 55–95.
7. **Vocabulario `être à plat` (es).** «estar pinchado» (regional) → «estar descargado (batería), estar desinflado (llanta)».

### c08
8. **Tabla p5 (filas «a él / a ella» y «a ellos / ellas»).** La forma decía «on lui a volé» / «on leur a volé» y el ejemplo usaba «pris» → «On lui a volé son téléphone. On lui a pris son sac.» y «On leur a volé leurs papiers.» (se mantiene `prendre` como en la ficha).
9. **Vocabulario `le t-shirt` (guía es).** «ti-chört» (en español «ch» suena /tʃ/; el sonido francés es «sh») → «ti-shört».
10. **Situación (147 → 169).** + «J’ai acheté ce portefeuille il y a deux ans.» (Ana), + «Je vais appeler ma banque tout de suite.» y una réplica final del policía «De rien, madame. Bonne journée !» (cortesía de cierre); traducciones es / en.
11. **s2 (feedback).** Citaba «Appelez votre banque pour faire opposition»; el texto lleva «tout de suite» → cita exacta.

### c09
12. **Situación (140 → 156).** La réplica larga de Emma se parte en dos y entra una pregunta de Ana («Et la personne sur le vélo, elle va bien ?» / «Oui, heureusement, elle n’avait rien. Mais j’ai encore peur quand je pense à ça.») + «Je suis contente d’être à la maison.» al final (Emma). s1 y s2 no cambian.
13. **s2 (opciones).** Eran TextoApoyo es / en, mientras que el resto de las comprensiones del bloque (y el plan) usan opciones en francés → «Parce qu’Emma n’a rien. / Parce qu’Emma a gagné un voyage. / Parce que la police est arrivée.» (parce que ya enseñado en N2).
14. **e4 (consigna).** «Estaba sorprendida de verlos» se leía como «les voir» (pronombre aún no enseñado) y el token es «vous» → «Estaba sorprendida de verlos a ustedes» / “…to see you (plural)”.
15. **i2 (aceptadas).** «Estoy aliviado de encontrar mi cartera» también es «trouver» → + «Je suis soulagée de retrouver mon portefeuille.», «Je suis soulagé de trouver mon portefeuille.», «Je suis soulagée de trouver mon portefeuille.».
16. **g4 (pista).** «Piensa en la situación: ¿qué pasa cuando dices cada una?» (vaga) → «Piensa cuándo la dirías: cuando pasa un peligro, cuando no crees una noticia o ante algo terrible.» (en igual).

### c10
17. **Situación (146 → 166).** + «Il pleuvait et j’avais froid devant la gare.» (escena), + «Elle m’a dit : « Ce n’est pas grave ! »», + «avec un gâteau pour moi» (cierre); traducciones es / en. s1 y s2 intactos.
18. **e6 (abierto).** La consigna decía «100–120 palabras en clase» y el modelo tenía 64 (rango 60–150) → «Cuenta una anécdota en 100–120 palabras…» (en igual), modelo nuevo de 107 palabras (la veille, ce jour-là, au moment où, plus-que-parfait, deux jours plus tôt, le lendemain; narradora «je», sin mezclar a Hugo), rango 90–140.
19. **Tipografía.** Las comillas añadidas («…» con U+202F) siguen la convención del bloque.

## Revisión punto por punto

1. **Francés de Francia.** être en train de + imparfait (d’ ante vocal), au moment où / juste au moment où + passé composé o imparfait, escena (imparfait) frente a hecho (passé composé); plus-que-parfait con avoir / être / pronominales (auxiliar en imparfait, concordancia con el sujeto con être, negación alrededor del auxiliar, se tromper de + sustantivo sin artículo); on + pronombre COI + passé composé, se faire + infinitivo con fait invariable, en + materia, qui / que, contenir; être + adjetivo + de + infinitivo (concordancia), avoir peur / honte de, exclamaciones; la veille, le lendemain, ce jour-là, plus tôt / plus tard, auparavant, se rendre compte (rendu invariable, + que + plus-que-parfait), arriver à quelqu’un con être. Correcto.
2. **Explicaciones es / en.** Cortas, con ejemplos y comparación con el inglés donde ayuda (“had + participle”, passive vs on, “surprised to see”); es con tú y léxico neutro (celular, boleto, auto, acera, semáforo, departamento, almuerzo, pastel); en en inglés americano (cell phone, crosswalk, sidewalk, subway, wallet, bike). Revisados los dos idiomas con búsqueda de variantes peninsulares / británicas: ninguna restante.
3. **Respuesta única y `aceptadas`.** Revisados los 10 `ordenar` (todos los órdenes naturales con la marca temporal o el lugar al inicio o al final, p. ej. c06 g3 / e4, c07 e4, c10 g3 / e4), los `completar` con opciones sin doble respuesta, los `elegir` / `escuchar` con un solo distractor plausible y los `escribir` (c06 i3 y c07 e5, c09 i2 corregidos; c10 i2 / e5 con ambos órdenes).
4. **Pistas y relacionar.** Cada pista ayuda a su ítem; glosas distintas en los cuatro relacionar (escena / hecho / acción en curso; cuero / lana / algodón; alivio / incredulidad / horror; la veille / le lendemain / ce jour-là).
5. **Sonidos y guías (regla 6).** j / g suave y ch = «sh» / “zh” (shur, sho-ké, su-la-shé, pa-sash, an-bu-tè-yash); nasales in / ain / oin = «en» / «uen», an / en = «an», on = «on» (plent, té-muen, lan-dö-men); ü y ö definidas en la nota de pronunciación de cada clase (ü: conducteur, surpris, plus tôt; ö: heurter, contretemps, voleur, peur, lendemain); consonantes finales exactas (ouf sí suena la f; honte lleva la t; plat, temps, contretemps sin t / p / s); -ais / -ait = «è» en c07. Inglés con “zh” y nasal avisada.
6. **Hablantes.** Solo Ana, Emma, Hugo y «Le policier» (papel en francés); nunca en español. Tuteo entre amigos; vous con el policía y con Monsieur Martin.
7. **Diálogos y cortesía.** Los textos modelan el objetivo de cada clase (relato con escena y hechos; excusa formal «Je suis désolée de mon retard… Cordialement»; denuncia con «Bonjour, madame… Merci beaucoup… De rien, madame. Bonne journée !»; reacciones «Ouf ! Quelle horreur ! Sans blague !»; anécdota con «Voilà le dénouement ! Et toi… ? Bises !»).
8. **Abiertos.** Los `escribir` de cierre llevan `abierta: true` con rango de palabras y no cuentan entre los 5 puntuables; modelos de 61 / 63 / 42 / 63 / 107 palabras, consistentes con su rango y con el vocabulario ya enseñado (el validador comprueba también los modelos).
9. **Anatomía.** explicación (3: gramática, gramática, sonido) → tablas → ejemplos (7) → vocabulario → guiada 5 → independiente 3 → situación con 2 ítems → evaluación 6 (5 puntuables + 1 abierto).

## Hechos del reparto confirmados

- Ana, al volver de noche del hotel (llovía, mucha gente en la acera), presencia un accidente de moto en la calle del hotel: el conductor frena, la moto resbala y choca con un auto; nadie es atropellado; un testigo llama a la policía, que llega diez minutos después; se lo cuenta a Léa por mensaje (c06). / Ana, coming back from the hotel at night (it was raining, lots of people on the sidewalk), witnesses a motorcycle accident on the street by the hotel: the driver brakes, the motorcycle skids and hits a car; nobody is run over; a witness calls the police, who arrive ten minutes later; she tells Léa about it in a message (c06).
- Ana llega tarde a la clase de Monsieur Martin (a las 10, cuando la clase ya había empezado): la víspera trabajó hasta tarde en el hotel y se acostó pasada la medianoche, su despertador no sonó, su celular estaba sin batería, Emma ya se había ido, perdió el bus y había huelga y embotellamiento; no pudo avisar a la escuela pero ya avisó a Chloé; le escribe a Monsieur Martin de vous (c07). / Ana is late to Monsieur Martin’s class (she walks in at 10, after it had started): the night before she worked late at the hotel and went to bed after midnight, her alarm clock didn’t go off, her cell phone was dead, Emma had already left, she missed the bus and there was a strike and a traffic jam; she couldn’t let the school know but has already told Chloé; she writes to Monsieur Martin with vous (c07).
- A Ana le roban en el metro, ayer hacia las 8 de la noche, su cartera de cuero marrón, pequeña (la compró hace dos años; llevaba la tarjeta bancaria, sus documentos y 20 euros; su pasaporte estaba en casa); la denuncia en la comisaría a un policía que la trata de vous, que le dice que bloquee la tarjeta enseguida y firme la denuncia (c08). / Ana has her small brown leather wallet stolen on the subway yesterday around 8 p.m. (she bought it two years ago; it held her bank card, her ID papers and 20 euros; her passport was at home); she reports it at the police station to an officer who uses vous with her and tells her to cancel the card right away and sign the theft report (c08).
- Emma vuelve a casa impresionada tras ver en la calle un accidente de auto contra bicicleta (la persona de la bicicleta no tiene nada): tuvo miedo de resbalar al correr hacia allí, se sorprendió de que la policía llegara tan rápido y le dio vergüenza no hacer nada; Ana la tranquiliza y le ofrece un té (Emma, que odia el café, pide té) (c09). / Emma comes home shaken after seeing a car hit a bike on the street (the person on the bike is fine): she was afraid of slipping as she ran over, was astonished the police arrived so fast and was ashamed of doing nothing; Ana comforts her and offers tea (Emma, who hates coffee, asks for tea) (c09).
- Hugo, un sábado, se olvida el boleto del tren a Lyon sobre su escritorio y lo descubre en la estación, donde pierde el tren; su abuela de Lyon, a la que había avisado dos días antes, lo esperaba a mediodía con el almuerzo preparado y no se enoja; al día siguiente toma el primer tren y llega a su casa a mediodía (c10). / Hugo, on a Saturday, leaves his train ticket to Lyon on his desk and realizes it at the station, where he misses the train; his grandmother in Lyon, whom he had told two days earlier, was expecting him at noon with lunch ready and is not angry; the next day he takes the first train and gets to her place at noon (c10).

## Sin resolver (no bloquea)

- No se eliminó ni renombró ninguna palabra francesa que B3–B10 puedan usar: solo cambió la redacción de frases (p. ej. «écrit à Chloé» sale del modelo abierto de c07, «pris leurs papiers» de la tabla de c08, ambas palabras enseñadas en N1 / N2); todos los bloques N3 encadenan con 0 errores.
- c10 (Hugo) convive con B1 c03 («sigue sin escribirle a su abuela de Lyon»): c10 habla de avisarle y de visitarla, no de la carta, y no se contradicen. Las dos «anoche» de c06 y c08 son historias independientes de Ana y también compatibles.
- La tabla de c08 p7 (`contenir`) incluye una fila «nous contenons, vous contenez» con la nota «se usan poco con objetos»: cumple como paradigma y no se tocó.
