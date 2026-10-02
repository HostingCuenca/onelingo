# Revisión N3 · B4 (fr.n3.c16–c20)

GO

Revisor distinto del autor. Contrastado con las 5 fichas de `curriculo/fr/n3.json` (títulos, objetivos, gramática, introduce / recicla, vocabulario, situación, tarea y plan de ejercicios), con la `nota` de N3, el reparto de N1 / N2, `ENCARGO_RUTA_FR.md` (Por nivel N3 y Calibración 1–10), `ESQUEMA_CONTENIDO.md` y B1–B3 de N3 (borradores).

**Validación (tras los cambios):**
- `python3 tools/validar_ruta.py fr --borrador n3-b01.json n3-b02.json n3-b03.json n3-b04.json` → **0 errores** (también encadenando `n3-b05.json`).
- `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún «título de la unidad difiere» para fr.n3.c16–c20 (títulos y objetivos idénticos a las fichas).

**Lo que ya estaba bien:** cada clase enseña exactamente lo de su ficha y nada posterior (condicional presente; si + imparfait; au cas où / sinon / à condition de + infinitivo; futur antérieur introductorio; avant de / pour / en attendant); los ejercicios del plan están todos (mismo formato y clave); 5 ítems puntuables en 5 formatos en cada evaluación más un `escribir` abierto (`abierta: true`) que no puntúa; `relacionar` en c20 g5 (3 pares, glosas distintas); todos los formatos del bloque; guiada con `pista`, independiente sin pista; 3–4 `erroresFrecuentes` por clase; tipografía (U+202F antes de ? ! : ; y ’; 0 apóstrofos rectos); guías de pronunciación según la Calibración 6 (sh / zh, nasales «en» / “an”, ü y ö definidas en c16); hablantes solo por nombre; es con tú y ustedes, en americano.

## Arreglos

### c16
- situación, **`contexto` y línea 1 de Hugo** (es / en / fr): «Tu es libre ce week-end ?» → «Tu es libre le week-end prochain ?» (contexto: «organizar el próximo fin de semana»). En N3 c11 el sábado es el viaje a Lyon y aquí Ana trabaja todo el sábado: sin esto parecían el mismo fin de semana (contradicción).
- **Léxico es no neutro**: «¿te apetece…?» → «¿te gustaría…?» (vocab `ça te dirait de`, explicación p7, patrón, ejemplo 3, g3 consigna y feedback, e4 consigna); en la situación, «¿Te apetece?» → «¿Qué te parece?» (2 líneas).
- i2 (escribir «Podríamos cenar en casa»), `aceptadas`: + «On pourrait dîner chez moi.», «On pourrait manger chez moi.».
- e4 (ordenar «¿Te gustaría ir al restaurante?»), `aceptadas`: + «D’aller au restaurant, ça te dirait ?» (orden natural con dislocación).

### c17
- **Viaje a Lyon coherente con c11** (misma salida, planificada aquí): situación, `contexto` (es / en): «…preparan el viaje en auto del sábado a Lyon, donde Ana va a conocer a la familia de Hugo…»; línea 1 de Ana: «Samedi, nous allons à Lyon chez la grand-mère de Hugo.» → «Samedi, nous allons à Lyon : je vais rencontrer la famille de Hugo chez sa grand-mère.» (c11: «Samedi, tu vas rencontrer toute ma famille à Lyon»; «rencontrer» ya está enseñada en N1 (B10) y en N3 c11).
- Última línea de Léa, es / en: «el sábado será un día genial» (repetía «¡Genial!») → «un día hermoso» / “a beautiful day”.

### c18
- `gramatica` solo traía `fr-g-au-cas-ou` y `concepto` `au-cas-ou`; la ficha introduce dos puntos → `gramatica`: + `fr-g-sinon-a-condition-de`; `concepto`: `au-cas-ou-sinon`.
- **Longitud de la situación**: 138 palabras (< 150 de «Por nivel» para N3) → 2 líneas nuevas (Hugo: «Et si quelqu’un était en retard ?»; Ana: «Alors appelle Léa au cas où tu serais en retard.»): 154 palabras (espacios) / 167 (tokens). Las preguntas s1 y s2 siguen teniendo una sola respuesta.
- i2 (escribir «Llama a Hugo por si llegara tarde»): consigna → «…con appeler:» (Appelle / Téléphone à eran ambos válidos).

### c19
- **Cita incoherente con N2 c20** (hechos del reparto): la cita con Monsieur Martin era «mardi à quatre heures»; N2 la fija el martes **a las 2** y Chloé la mueve al jueves a mediodía → «mardi à deux heures» en las 2 líneas de la situación (es / en) y en el modelo de e6.
- **Longitud de la situación**: 146 palabras → 2 líneas nuevas (Chloé ofrece «mercredi matin»; Ana: «Mercredi matin, j’ai cours. Jeudi à midi, ça m’arrange.»): 164 palabras. s1 («para cuándo propone Ana») sigue con una sola respuesta: «Jeudi à midi».
- `erroresFrecuentes` 1 («Je t’appellerai quand j’ai fini»): «hace falta el futur antérieur» → «lo correcto es el futur antérieur» (es / en); con quand + passé composé se oye en francés hablado, así que no se declara imposible.
- Ids de los pasos: `p1`, `p1b`, `p2`… → renumerados `p1`–`p14` (sin cambiar el contenido).

### c20
- **Situación de 150 palabras justas** → 1 línea nueva de Ana («D’accord. Et avant de sortir, ferme bien la porte !»): 159 palabras.
- e2 (elegir «Toma el metro para llegar más rápido» / «Il prend le métro…»): es ambiguo (imperativo vs. él) y no coincidía con el en («He takes») → «Él toma el metro para llegar más rápido.»
- e4 (ordenar): «él mira el horario» → «él verifica el horario» (los tokens llevan «vérifie»).
- e5 (escribir «Mientras espero el taxi, tomo un café»), `aceptadas`: + «Je prends un café en attendant le taxi.», «En attendant le taxi, je bois un café.», «Je bois un café en attendant le taxi.» («boire» y «prendre» un café son equivalentes).
- Ejemplo 7 («En attendant de partir, je prends un café.»), es: «Mientras espero para salir» → «Mientras espero la hora de salir».

### Todo el bloque
- **Posición de la respuesta correcta** en `elegir` / `escuchar`: las 35 estaban en la 1.ª opción (como en N3 b08) → redistribuida (12 / 12 / 11 en posiciones 1 / 0 / 2); solo se reordenan las opciones, `respuesta` actualizada. Ningún texto cambia.

## Decisiones del autor que se aceptan (no son errores)
- c18 s2: la ficha pide «à condition qu’il ne pleuve pas» (subjuntivo, que no se enseña hasta c26); el autor lo cambió por «à condition de venir chacun avec un plat» (à condition de + infinitivo, lo que dice `gramatica`). Correcto.
- c20: el contador (le compteur) del taxi sustituye al «contador de peso» de la ficha (que no existía); el diálogo sigue modelando avant de / pour / en attendant y el vocabulario de la ficha.
- Palabras añadidas al vocabulario además de las de la ficha (enseñadas en pasos y declaradas): c16 «ça me convient», «ça te dirait de»; c17 «le chauffeur / la chauffeuse», «se tromper de route», «le garage», «appeler»; c18 «emporter», «se dépêcher»; c20 «l’aéroport», «fermer». «le chauffeur» aparece en c17 porque la propia tarea de c17 lo usa; vuelve en la ficha de c20 como vocabulario (queda repetida, sin conflicto).
- c16–c19 son pasos de enseñanza largos (7–10 antes de la guiada): densos para 15 min, pero cada paso es corto y con ejemplos. Sin cambios.

## Palabras francesas eliminadas o renombradas
Ninguna: los cambios solo añaden formas ya enseñadas (famille, prochain, alors, quelqu’un, cours, bien, chez moi, boire, rencontrer). Los bloques B5–B10 no pierden nada. `n3-b05.json` valida encadenado con B1–B4 con 0 errores.

## Hechos del reparto confirmados

- Hugo llama a Ana para organizar un fin de semana posterior (no el del viaje a Lyon): propone ir al mercado el sábado; Ana trabaja todo el sábado en el hotel y contrapropone el domingo; acuerdan salir a las 9 h, almorzar juntos (con mesa reservada por Hugo) y que Hugo llame a Léa y Ana pregunte a Emma (c16) / Hugo phones Ana to plan a later weekend (not the Lyon one): he suggests going to the market on Saturday; Ana works all day Saturday at the hotel and counter-suggests Sunday; they agree to leave at 9, have lunch together (table booked by Hugo) and that Hugo calls Léa while Ana asks Emma (c16).
- El sábado Ana, Emma, Hugo y Léa van en auto a Lyon, a casa de la abuela de Hugo, donde Ana conoce a la familia de Hugo (viaje anunciado en c11); si hay un problema con el auto, el plan es tomar el tren todos juntos y Ana llamaría al taller; la abuela de Hugo almorzaría sin ellos y los esperaría si llegaran tarde (c17) / On Saturday Ana, Emma, Hugo and Léa drive to Lyon, to Hugo’s grandmother’s house, where Ana meets Hugo’s family (trip announced in c11); if the car has trouble, the plan is to take the train all together and Ana would call the garage; Hugo’s grandmother would eat lunch without them and wait for them if they were late (c17).
- Ana organiza por chat un barbecue del domingo a mediodía en el parque con Léa, Hugo y Emma: cada uno lleva un plato (Léa, verduras, es vegetariana; Emma, un postre: hace muy buen pastel; Hugo va en bicicleta y sale una hora antes); si llueve, el plan B es comer en casa de Ana (c18) / Ana organizes a Sunday-noon barbecue at the park by group chat with Léa, Hugo and Emma: everyone brings a dish (Léa, vegetables, she is a vegetarian; Emma, a dessert: she bakes a very good cake; Hugo bikes and leaves an hour early); if it rains, plan B is to eat at Ana’s place (c18).
- Ana tiene una cita con Monsieur Martin el martes a las 2 (trabaja en el hotel de 12 a 6 ese día); Chloé, la secretaria, la pasa al jueves a mediodía tras mirar el horario del profesor (Ana rechaza el miércoles por la mañana porque tiene clase); Ana entregará sus deberes el miércoles y llamará a Chloé cuando termine su turno; Ana y Chloé se tratan de vous (c19; coincide con N2 c20) / Ana has an appointment with Monsieur Martin on Tuesday at 2 (she works at the hotel from 12 to 6 that day); Chloé, the secretary, moves it to Thursday at noon after checking the teacher’s schedule (Ana turns down Wednesday morning because she has class); Ana will hand in her homework on Wednesday and call Chloé back after her shift; Ana and Chloé use vous (c19; consistent with N2 c20).
- Léa viaja en avión mañana; Ana le explica el trayecto al aeropuerto en VTC (precio en la aplicación) y le recuerda comprobar el horario del vuelo y guardar el boleto en el bolso; Léa le llamará antes de salir (c20) / Léa is flying tomorrow; Ana explains the ride to the airport by VTC (price in the app) and reminds her to check the flight time and keep her ticket in her bag; Léa will call her before leaving (c20).

## Sin resolver
- Nada bloqueante. Una nota para el coordinador: el destino del vuelo de Léa en c20 no se fija (ningún bloque posterior lo necesita; B5 sitúa el vuelo cancelado de Ana a Quito, hecho distinto). En c17 el «chauffeur» del viaje a Lyon es genérico (quien conduce el auto); N3 c04 dice que Léa aprobó el examen de conducir, así que no hay contradicción si un bloque posterior la pone al volante.
