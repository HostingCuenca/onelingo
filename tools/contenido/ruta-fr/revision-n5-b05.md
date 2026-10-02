GO

# Revisión N5 · B5 (fr.n5.c21–c25) — tratamientos, ciencia, causas, prevención y condiciones

Revisor independiente (francés de Francia, inglés americano, español neutro de América). Archivo revisado y corregido: `tools/contenido/ruta-fr/n5-b05.json` (copia del original en el scratchpad de la sesión). No se tocó ningún otro archivo ni se ejecutó git; no se leyó ningún `.env`.

## Validación

- `python3 tools/validar_ruta.py fr --borrador n5-b01 … n5-b05` (n4-b* ya integrados, omitidos): **0 errores**. También 0 errores añadiendo n5-b06 … n5-b09.
- `python3 tools/curriculo/validar_plan.py fr`: ningún «título de la unidad difiere» para fr.n5.c21–c25 (solo los 10 avisos de N1 sobre situaciones).
- Nota: durante la revisión `assets/contenido/fr/ruta/` pasó brevemente por un estado intermedio (n5-b01…b04 aparecían y desaparecían, con «id duplicado» en c19/c20); al final no hay n5-* integrados y la validación con los cinco borradores da 0 errores. Si el coordinador integra n5-b01…b04, hay que quitarlos de `--borrador`.

## Contraste con las fichas

Títulos, objetivos, gramática, `introduce` (finalite-formelle / passif-impersonnel / verbes-cause-effet / avant-que-de-peur-que + sans-que / a-condition-que), `recicla`, vocabulario (las 10 / 9 / 9 / 9 / 8 palabras de cada ficha con artículo, más extras enseñados antes de usarse: docteur, fatigue, infection, guérison, réduire, éviter, comprimé en c21; hypothèse, université, observer en c22; alimentation, sédentarité, pollen, entraîner, provenir, provoquer, conséquence, aliment, peau, auditeur, trouble en c23; maladie, consulter, soigner, gens en c24; séance, long, forcer en c25), situación y tarea coinciden con `curriculo/fr/n5.json`. Los planes de ejercicios están completos y en el mismo formato y clave (5 guiados con pista, 4 independientes sin pista, 2 de comprensión, 6 de evaluación por clase; comprobado por código). Nada de c26 en adelante; el único adelanto era la fila «suivre → le suivi» de la tabla de c22 (vocabulario de c25), ya eliminada.

Anatomía conforme a «Por nivel» N5 y al encargo: 3 explicaciones → 2–3 tablas → 8 ejemplos → vocabulario → guiada → independiente → situación → evaluación (5 ítems puntuables en 4 formatos: completar, elegir, ordenar, escuchar, más 1 `escribir` con `abierta: true` que no puntúa, con `minimoPalabras` / `maximoPalabras`). Errores frecuentes 3–4 por clase. Los seis formatos aparecen a lo largo del bloque (relacionar y escribir en guiada / independiente). Hablantes: Sophie, Madame Dubois, Léa, Hugo, Ana, La journaliste y las voces de documento L’ordonnance, L’article, Le dépliant (precedente publicado: Le dépliant, La brochure, La lettre, L’offre d’emploi). Guías de pronunciación coherentes con el Nivel 0 (sh para g suave, nasales «en» / «an» / «on», ü y ö definidas en la primera aparición de cada clase).

## Correcciones aplicadas

Todas las clases (situación): el texto estaba entre 271 y 305 palabras reales (c23 = 271, c24 = 271, c25 = 287, c22 = 296, c21 = 298), por debajo o al borde del rango 300–500 de N5. Ampliado con réplicas coherentes y solo con palabras ya enseñadas; ahora c21 = 330, c22 = 320, c23 = 320, c24 = 321, c25 = 322 (palabras con letras, contadas por espacios). Los dos ítems de comprensión de cada clase siguen siendo válidos con el texto ampliado.

c21
- Situación: +2 réplicas (cita para los análisis, «Oui, appelez demain de façon à avoir les résultats…») y «Si vous avez de la fièvre, appelez-moi tout de suite» en el cierre; se fusionaron dos réplicas seguidas de Sophie.
- Nota de pronunciación de `l’antibiotique` (es): «la u de qu = k» → «qu = k». `une infection` (es / en): «en = «an» nasal» era incorrecto → «in = «en» nasal» (en: «in is a nasal vowel»).
- Explicación 1 (es / en): «Las tres exigen el mismo sujeto» era inexacto (en vue de + sustantivo no tiene infinitivo) → «Con infinitivo, en vue de y de façon à exigen el mismo sujeto…».
- Tabla 1, fila «de manière à» (es): «de modo que evite» (pediría subjuntivo) → «para evitar los efectos secundarios».
- Error frecuente 1 (en): «“so as to sleep better” has no extra little word» era confuso → explica que el inglés dice “so as to” y que en francés la à se olvida fácil. Error frecuente 4 (es): redacción poco clara sobre «para que duerma» → «Pour que je dorme solo se usaría si el sujeto cambiara».
- i1 (`completar`, «en vue ___ voyage»): consigna «preposición contraída» era ambigua (`du` también es contraído) → «forma elidida de «de + un»» (es / en).

c22
- Ejemplo «Il a été prouvé que le sport réduit le stress» y explicación 3 (en): «sport» (británico) → «exercise».
- Situación: +1 réplica del artículo («Les chercheurs restent prudents…») y, en Léa, la frase sobre el tamaño de la muestra; fusionadas las dos réplicas seguidas de Léa.
- Tabla 3: eliminada la fila «suivre → le suivi» (palabra del vocabulario de c25, y no es una nominalización de este tipo). La validación sigue en 0 errores.

c23
- Situación: +2 réplicas (consecuencia más grave para un paciente) y frases sobre el azúcar y el tabaco.
- e2 (`completar`, «proviennent ___ manque de sommeil»): `du` también era correcto → la consigna fija el artículo indefinido «un» (es / en).
- Error frecuente 3: «Le tabac est dû à l’hypertension → Le tabac aggrave l’hypertension» → la forma correcta es ahora «L’hypertension est due au tabac» (corrige la frase de forma directa).

c24
- Situación: +1 réplica del dépliant (campaña de un mes, consultas abiertas a todos, «Consultez un médecin avant que…»), «Un contrôle dure vingt minutes, pas plus» y cierre de Sophie («il vaut mieux agir sans attendre la douleur»). Contexto (es / en) ahora indica que Ana da su testimonio y Sophie cierra con una nota (antes, Ana hablaba sin presentación).
- Vocabulario (es), neutro de América: «concienciación» → «concientización»; «cribado» → «tamizaje».
- i4 (`escribir`, «sans qu’on la voie»): `aceptadas` + «Elle est partie sans qu’on l’ait vue.» y «sans que l’on la voie.» (subjuntivo pasado y variante con l’on, ambos válidos).

c25
- Situación: +2 réplicas (ir a clases en autobús, «pourvu que vous ne marchiez pas trop») y fusión del cierre de Sophie en una sola réplica; «footing» (es) → «salir a correr» / «Nada de correr por ahora» (neutro de América).
- Coherencia con s2: Sophie decía «suivi court» por no forzar la rodilla, pero la ficha pide «Court, dans la mesure où Hugo se repose». Se intercambiaron las condiciones: la convalecencia es corta si no fuerza la rodilla; el seguimiento, si descansa. s2 opción correcta → «Court, dans la mesure où Hugo prend du repos» (con `force` / `repose` aún sin enseñar, se usó «prend du repos»).
- Explicación 1: «Sinon dice lo contrario» → define sinon («si no») y añade el ejemplo «faites vos séances ; sinon, le suivi sera long», porque `sinon` (recicla) no tenía ningún ejemplo. Explicación 2: «pourvu que… más oral» (dudoso) → «casi lo mismo que à condition que y suena algo más ligero».
- i4: `aceptadas` + «Pourvu que vous respectiez le traitement, vous vous rétablirez.».

## Revisado y sin cambios

finalidad con en vue de / de façon à / de manière à (mismo sujeto) frente a pour que / afin que + subjuntivo; il a été démontré / prouvé / observé / confirmé que (participio invariable); révéler, mettre en évidence, confirmer, démontrer; nominalización y selon / d’après; être dû (dû, due, dus, dues) à, résulter de, provenir de, entraîner, provoquer, favoriser, aggraver, réduire; avant que (+ ne explétif opcional, + avant de), de peur que / de crainte que / de peur de, sans que / sans + infinitivo; à condition que, à condition de, pourvu que, dans la mesure où + indicatif. Un solo resultado defendible en los ítems (los `completar` con opciones fijan la forma por la consigna; los `elegir` tienen un solo distractor gramatical). Todos los `ordenar` aceptan los órdenes naturales (c21 e4, c24 g5 / e4 y c25 e4 con la subordinada al inicio; en c22 y c23 el orden es único). Los `relacionar` tienen glosas claramente distintas; las pistas resuelven cada ítem. U+202F antes de ? ! : ; y apóstrofo ’ en todo el francés (0 apóstrofos rectos). Español sin peninsularismos (auto, pastilla, chequeo, tamizaje, rodilla, ustedes) e inglés americano (checkup, physical therapist, exercise, tablet / pill).

## Hechos del reparto confirmados

- Madame Dubois (68 años, viuda, antigua propietaria de Ana, vive cerca) consulta a Sophie, su médica de familia (se tratan de vous): cansada desde hace un mes, le duele la espalda por la noche y duerme mal; Sophie le receta un análisis de sangre y otros análisis, una pastilla por la noche para dormir mejor, y una vacuna para que no vuelva la infección grave que tuvo el invierno pasado; vuelve a verla en un mes; sigue usando su auto pequeño todos los días (c21). / Madame Dubois (68, a widow, Ana’s former landlady who lives nearby) sees Sophie, her family doctor (they use vous): tired for a month, her back hurts at night and she sleeps badly; Sophie prescribes a blood test and other lab tests, one tablet in the evening to sleep better, and a vaccine so the serious infection she had last winter doesn’t come back; she goes back in a month; she still drives her small car every day (c21).
- Léa lee en una revista científica un artículo sobre sueño y memoria para su clase de la universidad (debe resumirlo en 80 palabras); Hugo, que duerme poco (cinco horas entre semana, como en N3 c30), le promete acostarse temprano; se tutean (c22). / Léa reads an article on sleep and memory in a scientific journal for her university class (she must summarize it in 80 words); Hugo, who sleeps little (five hours on weekdays, as in N3 c30), promises to go to bed early; they use tu (c22).
- Sophie, médica de familia, da una entrevista en la radio del barrio sobre las causas y efectos de la obesidad (alimentación, sedentarismo, diabetes, hipertensión, alergias) (c23). / Sophie, a family doctor, gives an interview on the neighborhood radio about the causes and effects of obesity (diet, sedentary lifestyle, diabetes, high blood pressure, allergies) (c23).
- Sophie redacta un folleto de la campaña de salud dental del barrio, colgado en el consultorio y en la panadería; Ana da su testimonio: esperó tres días antes de ir al dentista por miedo a que le doliera y todo salió bien (coherente con N3 c27) (c24). / Sophie writes a leaflet for the neighborhood’s dental-health campaign, posted at her office and at the bakery; Ana gives her testimonial: she waited three days before seeing the dentist for fear it would hurt, and everything went well (consistent with N3 c27) (c24).
- Hugo se cae de la bicicleta cuando un auto llega muy rápido y se lastima la rodilla (no está rota): Sophie, que lo trata de vous y le manda saludos para Léa, le receta reposo, rehabilitación con un kiné, nada de footing, bicicleta ni gimnasio durante dos semanas, control en quince días y le aconseja usar casco; Hugo corre los miércoles y domingos y sueña con un maratón, y entrena en el gimnasio los martes y jueves (c25; coherente con N3 c29, c30 y c44). / Hugo falls off his bike when a car comes by very fast and hurts his knee (not broken): Sophie, who uses vous with him and sends her greetings to Léa, prescribes rest, rehabilitation with a physical therapist, no jogging, biking or gym for two weeks, a follow-up in two weeks, and advises him to wear a helmet; Hugo runs on Wednesdays and Sundays and dreams of a marathon, and works out at the gym on Tuesdays and Thursdays (c25; consistent with N3 c29, c30 and c44).

Sin contradicciones con N1–N4 (Sophie médica y madre de Léa; Madame Dubois viuda, antigua propietaria que vive cerca; Hugo sin auto, siempre en bicicleta, duerme poco; Ana fue al dentista tras tres días de dolor).

## Pendiente / sin resolver

- Ninguna palabra francesa de otros bloques se eliminó ni renombró: solo se quitó la fila «suivre → le suivi» de c22 (c25 sigue enseñando `le suivi`) y se cambió una opción de c25 s2; los bloques posteriores del nivel validan con 0 errores (n5-b06 … b09 incluidos).
- Fuera de este bloque, para el coordinador: según las situaciones de n5-b08 (c36, c37, c40), Madame Dubois es «la vecina de abajo» del edificio de Ana, lo que contradice la nota de reparto de N4 (desde N4 c11 es la antigua propietaria y vive cerca, con el nuevo propietario Monsieur Roux); la revisión de ese bloque debería alinearlo. Este bloque ya usa la versión de N4 (antigua propietaria que vive cerca).
- Un detalle de reparto a vigilar: n5-b01 c07 narra que Karim choca contra el auto de Sophie; no contradice nada de este bloque.
