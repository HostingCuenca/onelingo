# Revisión N10 · bloque 1 (fr.n10.c01–c05)

GO

Revisor independiente. Archivo revisado y corregido: `tools/contenido/ruta-fr/n10-b01.json`. Contrastado con las 5 fichas de `curriculo/fr/n10.json`, la `nota` del nivel, el reparto de `n1.json`/`n2.json`, los hechos de N2–N7, las notas de N8–N9, `ENCARGO_RUTA_FR.md` (puntos 1–15) y `ESQUEMA_CONTENIDO.md`.

## Validación

- `python3 tools/validar_ruta.py fr --borrador n9-b01 … n9-b09 (copia) n10-b01` → **0 errores**.
- Los borradores de N8 ya están integrados en `assets/contenido/fr/ruta/` y se quitaron de la lista (daban «id duplicado»).
- Existen n9-b01…b09; **no existe n9-b10 (c50)**. Se validó una copia en el scratchpad con el prerrequisito de `fr.n10.c01` reescrito a `fr.n9.c45` (última unidad existente de N9). El archivo real conserva `fr.n9.c50`, que reescribe el integrador. Con la cadena real el vocabulario disponible solo puede crecer, así que no aparecerán errores nuevos de «palabras no enseñadas».
- `python3 tools/curriculo/validar_plan.py fr` → 0 errores; ningún «título de la unidad difiere» para c01–c05.

## Estructura y evaluación

- Cada clase sigue la anatomía del encargo: explicaciones y tablas, ejemplos con audio, vocabulario (8–9 tarjetas, todas las de la ficha), práctica guiada (5 ítems con `pista`), independiente (3, sin pista), situación (diálogo + 2 ítems) y evaluación.
- **Evaluación: 5 ítems puntuables en 5 formatos distintos en cada clase** (c01–c05), más un `escribir` abierto (`abierta: true`, no puntúa) que no sustituye a los 4. Modelos de las abiertas por encima de `minimoPalabras`.
- Los ejercicios coinciden con el plan de cada ficha (mismo formato y misma clave). El bloque usa los seis formatos.
- Situación: 411–440 palabras por diálogo (rango N8–N10: 400–700), coherentes con sus ítems de comprensión. Hablantes: nombres o papeles en francés (`Le courriel` tiene precedente en N5–N9).
- Tipografía: 0 espacios normales antes de ? ! : ; en francés (U+202F) y 0 apóstrofos rectos.

## Correcciones obligatorias del coordinador

- (a) c02, Karim: ya no «abre su segundo restaurante» (existe desde N4 c06). Ahora **abre la terraza el 15 del mes próximo** (apertura de temporada; N5 ya fija que Karim tiene terraza). La función del diálogo se mantiene (en parlant de, justement, d’ailleurs). Cambios: contexto es/en; diálogo (Emma: «ta terrasse ouvre bientôt, non ?»; Karim: «On ouvre la terrasse le quinze du mois prochain.»; Ana: «…au menu de la terrasse ?»; traducciones «apertura» en lugar de «inauguración»); ítem i1 («su terraza»).
- (b) c05, Hugo: ya no es una pasantía de máster con tutor. Ahora es su **primera semana en un proyecto nuevo del servicio de patrimonio de la alcaldía, con una jefa de proyecto (mujer, sin nombre) a la que trata de vous**. El correo sigue siendo el ejercicio de registro (Madame, / vous / cordialement). Cambios: contexto; «cette première semaine sur le nouveau projet»; «ta responsable» / «ma responsable» (3 réplicas); correo «ma première semaine sur le projet»; s2 (consigna, feedback, opción «sa responsable»); error frecuente 1. Ya no queda «stage», «tutrice», «pasantía» ni «tutora».
- (c) Ana no vuelve al hotel en c01–c05. Los «hôtel» que quedan son el alojamiento del viaje a Bretaña y de Karim (c02) y el hotel de Léa en Marsella (c04). Se quitó «monsieur le Directeur» (el director del hotel de Ana) de c03 y c04. Ana dice «à mon travail» (c03) sin precisar el lugar y no hay ninguna réplica en recepción.

## Correcciones (clase, ítem: antes → después)

**c01**
- Ejemplos y diálogo, es: «Habríamos debido salir» → «Deberíamos haber salido» (español de América). «Hacen treinta y cinco grados» → «Hay treinta y cinco grados» (ejemplo y diálogo).
- Diálogo, es: «Tampoco a mí, te digo» → «Yo tampoco, te digo».
- g4 (relacionar): carrément «totalmente, claro que sí» → «totalmente, del todo» (chocaba con «tu m’étonnes = claro, no me extraña»).
- i1: se añade a `aceptadas` «Si, si, elle est dans mon sac.».

**c02**
- Errores frecuentes: la explicación de «à propos» se reescribe (la en decía que «speaking of» no lleva preposición, lo cual es falso); la de «revenir sur» ahora explica que existe con otro sentido (reconsiderar) en lugar de culpar a «la traducción literal».
- Contexto: se quita «nuevo restaurante»; Ana y Karim se tratan de usted y el resto de tú.
- Réplica sobre la terraza: pasa de Hugo a **Emma** (Emma y Karim se tutean por hecho canónico; el tuteo Hugo–Karim no estaba fijado en ningún nivel).
- i1: «Eres Hugo» → «Eres Emma y tuteas a Karim, tu jefe»; respuesta modelo «En parlant de cuisine, ta terrasse ouvre bientôt ?».

**c03**
- Diálogo: «Si, si, depuis lundi» (respuesta a «Déjà ?», que no es negativa) → «Oui, oui, depuis lundi». Se mantiene el «Si, si, cent euros !» de Emma porque contradice «C’est pas vrai !».
- Diálogo: «Oui, au hasard !» → «Oui, par hasard !» («au hasard» significa «al azar»).
- Diálogo: «c’est pour mon cours de français» → «je note toujours les nouvelles expressions» (en N9–N10 Ana ya no tiene clases de francés: aprobó el DALF y trabaja).
- Explicación de registro y error frecuente 3: «Monsieur le Directeur» → «Madame Mercier» (la jefa de Ana en N9–N10).
- e2: «Imagina que Emma te cuenta…» (ejercicio hipotético; no crea un hecho del reparto).

**c04**
- Diálogo y ejemplo: «tu voulais aussi lui montrer que tu es grande» (de una adulta, «grande» suena a «alta») → «que tu peux voyager seule», con traducciones es/en.
- Error frecuente 3: «Monsieur le Directeur» → «Madame Mercier».
- i1: «Imagina que eres Emma y que Karim, tu jefe, al que tuteas, te cuenta…» (antes Ana, que trata a Karim de vous, usaba «ah ouais ?» con él, y el hecho era un dato nuevo del reparto).
- e4 (ordenar): se añade a `aceptadas` «Et avec ton chef, comment ça s’est passé ?» (orden natural alternativo).
- e5 (relacionar): «et alors ? = pido que siga» y «raconte ! = invito a contar» eran casi iguales → «pregunto qué pasó después» / «pido que me cuente la historia».

**c05**
- e5 (ordenar): la alternativa de `aceptadas` no se podía formar con los tokens → «Ta soirée, elle était vachement sympa !» (sí se puede formar y es natural).
- i3 (escribir puntuable): se añaden los órdenes inversos («Je n’ai pas envie de cuisiner, je suis très fatigué(e)» y variantes con «et»).
- Resto: lo descrito en (b).

## Lo que estaba bien

Francés de Francia correcto (concordancias «arrivées/parties», «m’a vue», «on s’est fâchées», «Si on était parties… on aurait eu»); «si» solo tras negación; explicaciones es/en claras y cortas; tablas de 4–12 filas (ninguna «Para leer»); consignas que fijan una sola respuesta (ver c03 g4, con «Zut» y «Mince» aceptados); relacionar con glosas distintas; pistas útiles; español neutro de América (departamento, auto, celular, mesero); inglés americano (subway, 95 degrees, cell phone).

## Hechos del reparto confirmados

- Un sábado de agosto, Léa y Ana pasan la tarde en la playa de Biarritz; Hugo llega a la mañana siguiente (c01). / On a Saturday in August, Léa and Ana spend the afternoon at the beach in Biarritz; Hugo arrives the next morning (c01).
- Ana se quemó una vez con el sol en Quito, en una hora; Léa nunca se quema (c01). / Ana once got sunburned in Quito within an hour; Léa never gets sunburned (c01).
- Cena en casa de Hugo con Ana, Léa, Emma y Karim para planear un viaje a Bretaña: 500 € por persona, hotel sencillo, salida el primer sábado del mes a las 7 h; Emma reserva el tren (c02). / Dinner at Hugo’s with Ana, Léa, Emma and Karim to plan a trip to Brittany: €500 per person, a simple hotel, leaving the first Saturday of the month at 7 a.m.; Emma books the train (c02).
- Madame Dubois le pide a Ana que cuide su gato el mes próximo (coherente con N2 c41); el hermano pequeño de Léa sigue teniendo su gato (c02). / Madame Dubois asks Ana to look after her cat next month (consistent with N2 c41); Léa’s younger brother still has his cat (c02).
- Karim abre la terraza de su restaurante el día 15 del mes próximo (apertura de temporada; no es la apertura del segundo restaurante de N4 c06): Emma hace el servicio y Ana, que lo trata de vous, se ofrece a ayudar en la caja; Karim conoce un hotel pequeño y barato cerca del mar (c02). / Karim opens his restaurant’s terrace on the 15th of next month (seasonal opening; not the opening of the second restaurant from N4 c06): Emma works the service and Ana, who uses vous with him, offers to help at the cash register; Karim knows a small, inexpensive hotel near the sea (c02).
- Léa recibe un ascenso en su trabajo (desde el lunes; la más joven del equipo en ese puesto; su jefe está orgulloso) (c03). / Léa gets a promotion at work (since Monday; the youngest on the team in that position; her boss is proud) (c03).
- Emma perdió un tren y esperó tres horas, y una cita quedó cancelada; un cliente dejó 100 € de propina en el restaurante de Karim (c03). / Emma missed a train and waited three hours, and an appointment was canceled; a customer left a €100 tip at Karim’s restaurant (c03).
- Ana vio un ratón en la cocina y ganó en su trabajo dos entradas para un concierto de jazz en el centro cultural del barrio, el próximo sábado, a las que invita a Léa y Emma (c03). / Ana saw a mouse in the kitchen and won two tickets at work for a jazz concert at the neighborhood cultural center next Saturday, and invites Léa and Emma (c03).
- El hermano pequeño de Léa perdió su gato una noche y lo encontró por la mañana en el armario (c03). / Léa’s younger brother lost his cat one evening and found it in the wardrobe the next morning (c03).
- Léa pasó un fin de semana en Marsella con su madre Sophie, que tenía una conferencia: se equivocó de autobús, un señor mayor la ayudó y la invitó a comer sopa de pescado; Sophie se enfadó y se reconciliaron al día siguiente; Léa quiere volver con Hugo quizá en septiembre y Ana irá con ellos (c04). / Léa spent a weekend in Marseille with her mother Sophie, who had a conference there: she took the wrong bus, an elderly gentleman helped her and treated her to fish soup; Sophie was furious and they made up the next day; Léa wants to go back with Hugo, maybe in September, and Ana will join them (c04).
- Hugo, que trabaja en el servicio de patrimonio de la alcaldía, empieza un proyecto nuevo; su jefa de proyecto (mujer, sin nombre) le dice que su informe está impecable y él la trata de vous (c05). / Hugo, who works in the city hall’s heritage department, starts a new project; his project manager (a woman, unnamed) tells him his report is spotless and he uses vous with her (c05).
- Ana y Karim se tratan de vous; Emma y Karim, de tú; Ana, Léa, Emma y Hugo se tutean entre sí (c01–c05). / Ana and Karim use vous; Emma and Karim use tu; Ana, Léa, Emma and Hugo use tu with each other (c01–c05).

## Pendiente (no bloquea el GO)

1. **Plan (`curriculo/fr/n10.json`)**: el ejemplo de `ejercicios.independiente` de c02 sigue diciendo «su nuevo restaurante» y la situación y la `tarea` de c05 siguen hablando de prácticas y tutora. Hay que actualizarlos a la terraza y a la jefa de proyecto, igual que el borrador (el validador del plan no lo detecta). Los ejemplos del plan de c04 (Karim, estrella; Léa ha dejado su trabajo) son hipotéticos; en el borrador se presentan como «Imagina…» o como «un amigo».
2. **`nota` de N10**: dice que Ana «crea su propia agencia» («Passerelles», B6), mientras que N9 y el coordinador la sitúan en la agencia de Madame Mercier. Este bloque solo dice «mon travail» y «Madame Mercier», sin contradecir ninguna de las dos versiones; conviene aclarar la transición (¿deja la agencia de Madame Mercier en B6?) antes de escribir B6.
3. El prerrequisito de `fr.n10.c01` (`fr.n9.c50`) depende de que exista n9-b10.
4. Si más adelante se fija que Léa ya no es estudiante ni becaria (N8 c12 la muestra en prácticas), el ascenso de c03 queda a favor de esa línea; ninguna ficha de N10 B1 lo contradice.
5. Palabras retiradas del bloque (solo en diálogos, nunca enseñadas aquí): «stage», «tutrice», «deuxième», «cours de français». Ningún bloque posterior de N10 depende de ellas por este bloque.
