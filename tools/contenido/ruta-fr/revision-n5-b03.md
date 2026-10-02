# Revisión N5 · B3 (fr.n5.c11–c15)

GO

Revisor independiente. Se contrastó el bloque con las 5 fichas de `curriculo/fr/n5.json` (títulos, objetivos, gramática, introduce/recicla, vocabulario, situación, tarea y plan de ejercicios), el reparto de `n1.json`–`n3.json`, las calibraciones 1–10 de `ENCARGO_RUTA_FR.md` y las revisiones de N2 como referencia. Validación: `validar_ruta.py fr --borrador n5-b01 n5-b02 n5-b03` → 0 errores (los borradores n4-b01…b10 ya están integrados en `assets/contenido/fr/ruta/`; se quitaron de la lista). `validar_plan.py fr` → 0 errores y ningún «título de la unidad difiere» para fr.n5.c11–c15.

## Qué se comprobó y está bien

- Los 5 bloques de ejercicios planificados están presentes con el mismo formato y clave (guiada 5, independiente 4, situación 2, evaluación 6 en cada clase); solo se pulió la redacción. Cada evaluación tiene ≥ 5 ítems puntuables y ≥ 4 formatos; el `escribir` abierto (`abierta: true`) no cuenta.
- Anatomía: explicación → tablas → ejemplos (8) → vocabulario (8–10 palabras de la ficha) → guiada → independiente (sin pista) → situación → evaluación. Errores frecuentes 4–5 por clase.
- Situaciones de 302–321 palabras (rango N5: 300–500), con comprensión coherente con el texto.
- Tipografía: U+202F antes de ? ! : ; y apóstrofo ’ en todo el francés (68 U+202F, 0 espacios normales).
- Nada de gramática posterior a la ficha: relativos compuestos, superlativo + subjuntivo, adjetivos de sentido cambiante, à moins que / à moins de y causa formal; repasos solo de lo ya visto (dont, subjonctif passé c10, nominalisation c02, conditionnel passé c06, sauf si / au cas où / en cas de).
- Guías de pronunciación: j/g suave = «sh» (zh en inglés), nasales con «en/an/on», ü y ö definidas en cada nota donde aparecen.
- Hablantes: Ana, Lucas, Léa y «La compagnie».

## Correcciones aplicadas (clase, ítem: antes → después)

**c11**
- Situación: 299 palabras → 317 (se añadió «Si vous avez une question, venez nous voir à la réception : nous serons ravis de vous aider.» con traducción es/en), para cumplir el mínimo de 300.
- i2, consigna es: «clientes, masculino plural» (ambiguo en género) → ««les clients», masculino plural».
- Inglés: «holiday cottage» → «vacation cottage» (vocabulario y diálogo); «unless … cancelled» → «canceled» en todo el bloque (inglés americano).

**c12**
- Explicación p1: «como en la clase anterior de este nivel» (el subjuntivo pasado se vio en c10) → «como en la clase 10 de este nivel» (es y en).
- Explicación p2: «son “superlativos de hecho”» → «funcionan como superlativos» (incluye «el último»); «Con qui el sujeto es el mismo relativo» → «Con qui, el relativo es el sujeto del verbo… con que, el verbo lleva su propio sujeto».
- Tabla p5, fila 5: «le moment» → «le meilleur moment» (coincidía mal con el ejemplo).
- g4 (relacionar), pista genérica («Piensa en lo que dirías…») → pista concreta con las palabras clave (manquer, valoir, seul, premier).
- i4 (escribir): `aceptadas` ampliadas a todas las variantes naturales: belle/jolie × jamais vue / vue / vue de ma vie / jamais vue de ma vie.
- s2: consigna en inglés sin signo y agramatical → «Comprehension: how Lucas describes the waterfall.»

**c13**
- Situación, línea 2: «Ce n’est plus un château, mais c’est un château très ancien» se contradecía (ex-castillo y castillo antiguo a la vez) → «Ce n’est plus un château, mais ses murs sont très anciens : ils ont plus de huit cents ans» (modela además «anciens» pospuesto); traducciones es/en ajustadas.
- s1: la consigna revelaba la respuesta («el texto dice que hoy es un hotel») → «Responde según el texto» / «Answer based on the text»; feedback ajustado.
- Inglés: «authentic little shop» → «store».

**c14**
- Explicación p2: «Es la misma regla que avant de / avant que» (avant que se introduce en c24, ficha posterior) → «la misma regla que ya viste con avant de + infinitivo (avant de partir)» (es y en).
- Traducción es de la situación: «el primer lugar libre» → «el primer asiento libre».
- i4 (escribir): `aceptadas` ampliadas con el orden inverso (À moins que… , nous prendrons l’avion), con y sin «ne» explétif, y «On prendra».

**c15**
- e4: el feedback (es y en) decía «el remboursement» (español dentro del francés) → «le remboursement».
- s2: feedback con mezcla de idiomas («rembourse… y estudia la indemnización») → frases completas en es y en.
- Situación y tabla p8: «dont vous trouverez les justificatifs ci-joint» (ci-joint debe concordar tras el sustantivo) → «dont vous trouverez ci-joint les justificatifs»; igual en la fila de la tabla: «Vous trouverez ci-joint les justificatifs.»

## Palabras francesas retiradas o renombradas

Ninguna que use un bloque posterior. En c13 desaparece la expresión «un château très ancien» del texto de la situación (ancien y château siguen enseñados); en c12 no se tocó el vocabulario; «avant que» sale de una explicación (era una referencia, no un dato evaluable).

## Hechos del reparto confirmados

- Ana trabaja en la recepción de un hotel de un barrio tranquilo del centro de París, cerca de un gran parque; el hotel ofrece cada mañana una visita guiada gratuita del barrio, y ella escribe su presentación para la página web (c11) / Ana works at the front desk of a hotel in a quiet neighborhood in central Paris, near a big park; the hotel offers a free guided tour of the neighborhood every morning, and she writes its presentation for the website (c11)
- Lucas hizo una estadía de idiomas que le pareció excelente (c11) / Lucas took a language-study trip that he thought was excellent (c11)
- Lucas, que vive en Montreal, viajó tres semanas este verano por Canadá y publica en su blog «Mes coups de cœur»: la costa salvaje de la Gaspesia (ve ballenas desde la costa), una cascada cerca de Quebec, un glaciar en el oeste y un pueblo junto al mar; aconseja viajar en septiembre (c12) / Lucas, who lives in Montreal, traveled for three weeks in Canada this summer and posts on his blog “Mes coups de cœur”: the wild coast of Gaspésie (he sees whales from the shore), a waterfall near Quebec City, a glacier in the west and a village by the sea; he advises traveling in September (c12)
- Léa y Hugo pasaron un fin de semana (dos días) en un pueblo encaramado del sur de Francia, con un antiguo castillo convertido en hotel, una playa desierta, una chambre d’hôtes (cada uno con su cuarto) y un restaurante cuyo chef es alto y simpático; Léa lo cuenta en un blog de viajes (c13) / Léa and Hugo spent a weekend (two days) in a hilltop village in the south of France, with a former castle turned hotel, an empty beach, a chambre d’hôtes (each with their own room) and a restaurant whose chef is tall and friendly; Léa tells the story on a travel blog (c13)
- La víspera de su viaje a Quito (primera visita en dos años), con huelga de pilotos, Ana escribe a su familia en francés para practicar: sale mañana por la mañana, ya avisó a Emma, tiene seguro de viaje y le pide a su padre que la recoja en el aeropuerto de Quito; llegará como máximo en dos días (c14) / The day before her trip to Quito (her first visit in two years), with a pilots’ strike under way, Ana writes to her family in French to practice: she leaves tomorrow morning, has already told Emma, has travel insurance and asks her father to pick her up at the Quito airport; she will arrive in two days at the latest (c14)
- El vuelo de Ana a Quito se cancela el día de la salida por la huelga de pilotos y llega con un día de retraso; pasa la tarde en el aeropuerto, paga una habitación de hotel y reclama a la aerolínea una indemnización y el reembolso del hotel; la compañía ofrece una comida a todos, reembolsa el hotel con justificantes y dará el monto de la indemnización en quince días (c15) / Ana’s flight to Quito is canceled on the day of departure because of the pilots’ strike and she arrives a day late; she spends the evening at the airport, pays for a hotel room and claims compensation and a hotel refund from the airline; the company offers everyone a meal, refunds the hotel against receipts and will give the compensation amount within fifteen days (c15)

Coherencia con el reparto anterior: Ana trabaja en un hotel (N2–N3) y su familia vive en Quito (N1); lleva dos años sin verla (N3 c01); Lucas vive en Montreal (N3 c01); Léa y Hugo son amigos desde el colegio (N3); la cancelación por huelga, el vuelo con un día de retraso y la comida para todos coinciden con N3 c21/c25 (c14–c15 son esa misma cancelación contada desde la víspera y desde la reclamación posterior). Ningún hecho contradice N1–N3. N4 y N5 aún no tienen `hechosDelReparto` registrados.

## Pendiente / a vigilar (no bloquea)

- Las fichas c14/c15 del plan describen el vuelo cancelado de Ana a Quito, que ya es el de N3 c21–c25: el bloque lo trata como el mismo viaje (coherente). Si el coordinador quiere un viaje distinto, habría que cambiar «deux ans» y la secuencia en c14–c15.
- c14 tabla p6 («Para leer el mensaje de Ana») agrupa formas sueltas («perdre, nous raterons, nous resterons», «arrivera, partira-t-elle») solo para que el validador las dé por enseñadas; pedagógicamente es torpe pero inocuo.
- La ficha de c14 usa «cogerá» (español de España) en el plan; el contenido ya usa «tomará». Conviene limpiar la ficha.
- c12: «rester sur la route» para el glaciar es poco natural, pero «chemin» solo se enseña en c13, así que no se podía usar sin saltarse el orden.
